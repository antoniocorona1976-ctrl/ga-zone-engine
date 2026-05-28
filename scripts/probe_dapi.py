#!/usr/bin/env python3
"""
DAPI probe runner — strumento per V-1 (equivalenza realtime vs CANDLERANGE)
e V-2 (cut-off temporale CANDLERANGE), come da tasks/PROBE_RECUPERO_GAP_DAPI
e INDAGINE_DIRECTA_CROSS_INDEX appendici A/B.

Scoperte empiriche incorporate (sessione 2026-05-28):
  - schema CANDLE reale: O;L;H;C;V  (wiki DAPI dichiara O;H;L;C — INESATTO)
  - terminatore stream history: "END CANDLES"
  - sintassi CANDLERANGE:
       CANDLERANGE <sym> <yyyyMMddHHmmss_start> <yyyyMMddHHmmss_end> <period_s>
  - codici errore osservati:
       1004 = comando non valido (es. HELP/INFO sulla 10001)
       1007 = ticker non abilitato per l'account (porta 10003 storici)
       1017 = sintassi del comando malformata
       1030 = market data realtime non sottoscritto (porta 10001)
  - convenzione mese Directa-IDEM (parziale): F=Giugno, I=Settembre
  - convenzione ticker
       Eurex: EU.<CODE><MONTH><YEAR>   es. EU.DJ50M6
       CME:   CM.<CODE><MONTH><YEAR>   es. CM.ESM6
       IDEM:  <CODE><YEAR><MONTH>       es. FIB6F
  - pattern architetturale: socket PERSISTENTE per la 10001 (realtime) e per
       la 10003 (history); aprire/chiudere a raffica innesca cooldown ~30s
       dopo la 14a connessione consecutiva (osservato in App. A.4).

Uso:
  python scripts/probe_dapi.py sanity
  python scripts/probe_dapi.py v1-capture --window morning   --tickers FIB6F,DITAS
  python scripts/probe_dapi.py v1-capture --window afternoon --tickers FIB6F,DITAS
  python scripts/probe_dapi.py v1-fetch   --tickers FIB6F,DITAS --date 2026-05-29
  python scripts/probe_dapi.py v1-compare --capture probe_out/v1_morning_20260529.decoded.csv \
                                          --hist    probe_out/v1_hist_20260529_fetched_...csv
  python scripts/probe_dapi.py v2-cutoff  --tickers FIB6F,DITAS,CM.MESM6 --period 60
  python scripts/probe_dapi.py v2-cutoff  --tickers FIB6F,DITAS,CM.MESM6 --period 86400

Output: directory probe_out/ in cwd, NON committata (vedi .gitignore).

Prerequisiti operativi:
  - DGo aperto, Darwin avviato, banner DARWIN_STATUS;CONN_OK;TRUE atteso
  - TradingView Directa CHIUSO  (vincolo D-6)
  - una sola istanza Darwin attiva sulla macchina
"""
from __future__ import annotations

import argparse
import csv
import json
import socket
import sys
import time
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

HOST = "127.0.0.1"
PORT_RT = 10001
PORT_HIST = 10003

RECV_BUF = 8192
BANNER_TIMEOUT = 2.0
HIST_TIMEOUT = 15.0            # serializzazione candele intraday richiede tempo
END_MARKER = b"END CANDLES"
DEFAULT_TICKERS_V1 = ["FIB6F", "DITAS"]
DEFAULT_TICKERS_V2 = ["FIB6F", "DITAS", "CM.MESM6"]
CUTOFF_DAYS = [50, 80, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 160]

WINDOWS = {
    "morning":   ("09:00:00", "09:30:00"),
    "afternoon": ("14:30:00", "15:00:00"),
}

OUTDIR = Path("probe_out")


# ---------------------------------------------------------------------------
# Connessione persistente
# ---------------------------------------------------------------------------

class DapiConn:
    def __init__(self, port: int, label: str, banner_timeout: float = BANNER_TIMEOUT):
        self.port = port
        self.label = label
        self.sock = socket.socket()
        self.sock.settimeout(3.0)
        self.sock.connect((HOST, port))
        self.banner = self._drain_banner(banner_timeout)

    def _drain_banner(self, timeout: float) -> str:
        self.sock.settimeout(timeout)
        try:
            data = self.sock.recv(RECV_BUF)
        except socket.timeout:
            return ""
        return data.decode("utf-8", "replace").strip()

    def send(self, cmd: str) -> None:
        self.sock.sendall((cmd + "\n").encode("utf-8"))

    def read_until_any(self, markers: tuple[bytes, ...], max_seconds: float) -> bytes:
        deadline = time.time() + max_seconds
        chunks: list[bytes] = []
        joined = b""
        while time.time() < deadline:
            self.sock.settimeout(max(0.2, deadline - time.time()))
            try:
                c = self.sock.recv(RECV_BUF)
                if not c:
                    break
                chunks.append(c)
                joined = b"".join(chunks)
                if any(m in joined for m in markers):
                    return joined
            except socket.timeout:
                break
        return joined

    def stream_for(self, duration_seconds: float, on_line) -> None:
        """Legge linee per duration_seconds chiamando on_line(str). Per realtime."""
        deadline = time.time() + duration_seconds
        leftover = b""
        while time.time() < deadline:
            self.sock.settimeout(max(0.2, deadline - time.time()))
            try:
                c = self.sock.recv(RECV_BUF)
                if not c:
                    break
                data = leftover + c
                lines = data.split(b"\n")
                leftover = lines[-1]
                for raw in lines[:-1]:
                    s = raw.decode("utf-8", "replace").strip()
                    if s:
                        on_line(s)
            except socket.timeout:
                continue
        if leftover.strip():
            on_line(leftover.decode("utf-8", "replace").strip())

    def close(self) -> None:
        try:
            self.sock.close()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Decoder
# ---------------------------------------------------------------------------

def parse_line(line: str) -> dict:
    """
    Decode di una singola riga DAPI.
    kind ∈ { banner, end_candles, err, candle, candle_malformed, anag, price, book5, unknown }
    """
    if line.startswith("DARWIN_STATUS"):
        return {"kind": "banner", "raw": line}
    if line.startswith("END CANDLES"):
        return {"kind": "end_candles", "raw": line}
    if line.startswith("ERR"):
        p = line.split(";")
        return {
            "kind": "err",
            "ticker": p[1] if len(p) > 1 else "",
            "code":   p[2] if len(p) > 2 else "",
            "raw": line,
        }
    if line.startswith("CANDLE;"):
        # Schema reale verificato 2026-05-28:
        # CANDLE;<ticker>;<yyyyMMdd>;<HH:mm:ss>;<O>;<L>;<H>;<C>;<V>
        p = line.split(";")
        if len(p) >= 9:
            try:
                vol_str = p[8].strip()
                volume = int(vol_str) if vol_str.lstrip("-").isdigit() else float(vol_str)
                return {
                    "kind":   "candle",
                    "ticker": p[1],
                    "date":   p[2],
                    "time":   p[3],
                    "open":   float(p[4]),
                    "low":    float(p[5]),
                    "high":   float(p[6]),
                    "close":  float(p[7]),
                    "volume": volume,
                    "raw": line,
                }
            except ValueError:
                return {"kind": "candle_malformed", "raw": line}
        return {"kind": "candle_malformed", "raw": line}
    if line.startswith("ANAG;"):
        # ANAG;<ticker>;<HH:mm:ss>;<ISIN>;<descr>;<ref_price>;<close_prev>;<flag>
        p = line.split(";")
        if len(p) >= 8:
            return {
                "kind":       "anag",
                "ticker":     p[1],
                "time":       p[2],
                "isin":       p[3],
                "descr":      p[4],
                "ref_price":  p[5],
                "close_prev": p[6],
                "flag":       p[7],
                "raw": line,
            }
    if line.startswith("PRICE;"):
        # PRICE;<ticker>;<HH:mm:ss>;<last>;<extra...>
        # (schema esatto dei campi extra non documentato, varia tra cash e future)
        p = line.split(";")
        last = None
        if len(p) >= 4:
            try:
                last = float(p[3])
            except ValueError:
                last = None
        return {
            "kind":         "price",
            "ticker":       p[1] if len(p) > 1 else "",
            "time":         p[2] if len(p) > 2 else "",
            "last":         last,
            "fields_extra": p[4:],
            "raw": line,
        }
    if line.startswith("BOOK_5;"):
        # BOOK_5;<ticker>;<HH:mm:ss>; bid1_lots;bid1_ord;bid1_price; ... (x5)
        #                              ask1_lots;ask1_ord;ask1_price; ... (x5)
        p = line.split(";")
        return {
            "kind":   "book5",
            "ticker": p[1] if len(p) > 1 else "",
            "time":   p[2] if len(p) > 2 else "",
            "fields": p[3:],
            "raw": line,
        }
    return {"kind": "unknown", "raw": line}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def ensure_outdir() -> None:
    OUTDIR.mkdir(exist_ok=True)


def fmt_dt_compact(d: datetime) -> str:
    return d.strftime("%Y%m%d%H%M%S")


def run_candlerange(hist: DapiConn, sym: str, start: str, end: str, period_s: int,
                    timeout: float = HIST_TIMEOUT) -> tuple[list[dict], list[dict], bool]:
    cmd = f"CANDLERANGE {sym} {start} {end} {period_s}"
    hist.send(cmd)
    data = hist.read_until_any((END_MARKER, b"ERR;"), timeout)
    lines = data.decode("utf-8", "replace").splitlines()
    candles: list[dict] = []
    errs: list[dict] = []
    end_marker = False
    for line in lines:
        if not line.strip():
            continue
        d = parse_line(line)
        if d["kind"] == "candle":
            candles.append(d)
        elif d["kind"] == "err":
            errs.append(d)
        elif d["kind"] == "end_candles":
            end_marker = True
    return candles, errs, end_marker


# ---------------------------------------------------------------------------
# Comandi
# ---------------------------------------------------------------------------

def cmd_sanity(_args) -> None:
    ensure_outdir()
    print(f"[sanity] HOST={HOST} ports={PORT_RT},{PORT_HIST}")
    hist = DapiConn(PORT_HIST, "HIST")
    print(f"[sanity] banner 10003: {hist.banner!r}")
    rt = DapiConn(PORT_RT, "RT")
    print(f"[sanity] banner 10001: {rt.banner!r}")

    today = date.today()
    start = (today - timedelta(days=10)).strftime("%Y%m%d") + "000000"
    end = today.strftime("%Y%m%d") + "235959"
    for sym in DEFAULT_TICKERS_V1:
        candles, errs, end_marker = run_candlerange(hist, sym, start, end, 86400)
        print(f"[sanity] CANDLERANGE {sym} D 10g → candles={len(candles)} end={end_marker} errs={len(errs)}")
        if candles:
            c = candles[0]
            print(f"          first {c['date']} {c['time']}  O={c['open']} L={c['low']} H={c['high']} C={c['close']} V={c['volume']}")
        for e in errs[:3]:
            print(f"          ERR ticker={e.get('ticker')!r} code={e.get('code')!r}")
    hist.close()
    rt.close()


def cmd_v1_capture(args) -> None:
    ensure_outdir()
    win = args.window
    if win not in WINDOWS:
        sys.exit(f"window {win!r} non riconosciuta. Valori: {list(WINDOWS)}")
    start_hms, end_hms = WINDOWS[win]
    tickers = [t.strip() for t in args.tickers.split(",") if t.strip()]

    now = datetime.now()
    print(f"[v1-capture] ora locale = {now.strftime('%H:%M:%S')}  finestra = {start_hms} → {end_hms}")
    target_start = datetime.combine(now.date(), datetime.strptime(start_hms, "%H:%M:%S").time())
    target_end = datetime.combine(now.date(), datetime.strptime(end_hms, "%H:%M:%S").time())

    if now < target_start:
        wait_s = (target_start - now).total_seconds()
        print(f"[v1-capture] attendo {wait_s:.0f}s fino a {target_start.strftime('%H:%M:%S')}...")
        time.sleep(max(0.0, wait_s))
    elif now > target_end:
        sys.exit(f"[v1-capture] finestra {win} già conclusa (ora={now.strftime('%H:%M:%S')}, end={end_hms})")

    duration = max(1.0, (target_end - datetime.now()).total_seconds())
    print(f"[v1-capture] durata cattura = {duration:.0f}s tickers={tickers}")

    stamp = now.strftime("%Y%m%d")
    raw_path = OUTDIR / f"v1_{win}_{stamp}.raw.log"
    decoded_path = OUTDIR / f"v1_{win}_{stamp}.decoded.csv"

    rt = DapiConn(PORT_RT, "RT")
    print(f"[v1-capture] banner = {rt.banner!r}")
    for t in tickers:
        rt.send(f"SUB {t}")
        print(f"[v1-capture] SUB {t}")

    counters: dict[str, int] = defaultdict(int)
    with raw_path.open("w", encoding="utf-8") as raw_fp, \
         decoded_path.open("w", encoding="utf-8", newline="") as dec_fp:
        dec_w = csv.writer(dec_fp)
        dec_w.writerow(["host_ts", "kind", "ticker", "time", "last", "raw"])

        def on_line(s: str) -> None:
            host_ts = datetime.now().isoformat(timespec="microseconds")
            raw_fp.write(f"{host_ts}\t{s}\n")
            d = parse_line(s)
            counters[d["kind"]] += 1
            dec_w.writerow([
                host_ts,
                d.get("kind", ""),
                d.get("ticker", ""),
                d.get("time", ""),
                d.get("last", "") if d.get("last") is not None else "",
                d.get("raw", ""),
            ])

        rt.stream_for(duration, on_line=on_line)

    for t in tickers:
        try:
            rt.send(f"UNSUB {t}")
        except Exception:
            pass
    rt.close()

    print(f"[v1-capture] eventi per tipo: {dict(counters)}")
    print(f"[v1-capture] raw     → {raw_path}")
    print(f"[v1-capture] decoded → {decoded_path}")


def cmd_v1_fetch(args) -> None:
    """CANDLERANGE 1-min per le due finestre V-1 del giorno indicato."""
    ensure_outdir()
    d = datetime.strptime(args.date, "%Y-%m-%d").date()
    tickers = [t.strip() for t in args.tickers.split(",") if t.strip()]

    hist = DapiConn(PORT_HIST, "HIST")
    print(f"[v1-fetch] banner = {hist.banner!r}")

    fetch_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = OUTDIR / f"v1_hist_{d.strftime('%Y%m%d')}_fetched_{fetch_stamp}.csv"
    with out_path.open("w", encoding="utf-8", newline="") as fp:
        w = csv.writer(fp)
        w.writerow(["fetch_host_ts", "window", "ticker", "date", "time",
                    "open", "low", "high", "close", "volume"])
        for win, (start_hms, end_hms) in WINDOWS.items():
            start = d.strftime("%Y%m%d") + start_hms.replace(":", "")
            end = d.strftime("%Y%m%d") + end_hms.replace(":", "")
            for sym in tickers:
                candles, errs, end_marker = run_candlerange(hist, sym, start, end, 60)
                fetch_iso = datetime.now().isoformat(timespec="seconds")
                for c in candles:
                    w.writerow([fetch_iso, win, c["ticker"], c["date"], c["time"],
                                c["open"], c["low"], c["high"], c["close"], c["volume"]])
                print(f"[v1-fetch] {win:9s} {sym:14s} candles={len(candles):4d} end={end_marker} errs={len(errs)}")
                for e in errs[:2]:
                    print(f"             ERR ticker={e.get('ticker')!r} code={e.get('code')!r}")
                time.sleep(0.6)
    hist.close()
    print(f"[v1-fetch] csv → {out_path}")


def cmd_v1_compare(args) -> None:
    """
    Costruisce barre 1-min locali dai tick PRICE catturati (decoded CSV V-1 capture)
    e le confronta con le barre da CANDLERANGE (CSV V-1 fetch) sullo stesso minuto.
    """
    ensure_outdir()
    cap_path = Path(args.capture)
    hist_path = Path(args.hist)
    if not cap_path.exists():
        sys.exit(f"capture CSV non trovato: {cap_path}")
    if not hist_path.exists():
        sys.exit(f"hist CSV non trovato: {hist_path}")

    # 1) Aggrega tick PRICE per (ticker, minuto)
    local_ticks: dict[tuple[str, str], list[tuple[str, float]]] = defaultdict(list)
    with cap_path.open(encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            if row["kind"] != "price":
                continue
            t = row["time"]
            if len(t) < 5:
                continue
            try:
                last = float(row["last"]) if row["last"] else None
            except ValueError:
                last = None
            if last is None:
                continue
            minute = t[:5] + ":00"
            local_ticks[(row["ticker"], minute)].append((t, last))

    local_ohlc: dict[tuple[str, str], dict] = {}
    for key, ticks in local_ticks.items():
        ticks.sort()
        prices = [p for _, p in ticks]
        local_ohlc[key] = {
            "open":    prices[0],
            "low":     min(prices),
            "high":    max(prices),
            "close":   prices[-1],
            "n_ticks": len(prices),
        }

    # 2) Indicizza candele storiche per (ticker, minuto)
    # Attenzione: il ticker realtime per il cash index può essere "dITAS" (minuscolo)
    # nel campo PRICE.ticker, mentre la CANDLE arriva con "DITAS" maiuscolo.
    # Normalizziamo entrambi a uppercase per il match.
    hist_idx: dict[tuple[str, str], dict] = {}
    with hist_path.open(encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            sym = row["ticker"].upper()
            minute = row["time"][:5] + ":00"
            hist_idx[(sym, minute)] = row

    local_norm = {(s.upper(), m): v for (s, m), v in local_ohlc.items()}

    # 3) Diff
    keys = sorted(set(local_norm) | set(hist_idx))
    matches = mismatches = only_local = only_hist = 0
    diffs = []
    for k in keys:
        ll = local_norm.get(k)
        hh = hist_idx.get(k)
        if ll and not hh:
            only_local += 1
            continue
        if hh and not ll:
            only_hist += 1
            continue
        same = (
            float(hh["open"])  == ll["open"]  and
            float(hh["low"])   == ll["low"]   and
            float(hh["high"])  == ll["high"]  and
            float(hh["close"]) == ll["close"]
        )
        if same:
            matches += 1
        else:
            mismatches += 1
            diffs.append({
                "ticker": k[0],
                "minute": k[1],
                "local":  ll,
                "hist":   {"open":  hh["open"],  "low":   hh["low"],
                           "high":  hh["high"], "close": hh["close"],
                           "volume": hh["volume"]},
            })

    summary = {
        "minuti_totali": len(keys),
        "matches":       matches,
        "mismatches":    mismatches,
        "only_local":    only_local,
        "only_hist":     only_hist,
    }
    print(f"[v1-compare] {summary}")
    out = OUTDIR / f"v1_compare_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps({"summary": summary, "diffs": diffs[:200]},
                              indent=2, default=str), encoding="utf-8")
    print(f"[v1-compare] dettaglio → {out}")


def cmd_v2_cutoff(args) -> None:
    """V-2: CANDLERANGE all'indietro con range crescente, cerca il punto di rottura."""
    ensure_outdir()
    tickers = [t.strip() for t in args.tickers.split(",") if t.strip()]
    period = int(args.period)
    days_list = [int(x) for x in args.days.split(",")] if args.days else CUTOFF_DAYS
    gap_s = float(args.gap)

    hist = DapiConn(PORT_HIST, "HIST")
    print(f"[v2-cutoff] banner = {hist.banner!r}")
    print(f"[v2-cutoff] period={period}s tickers={tickers} days={days_list} gap={gap_s}s")

    out_path = OUTDIR / f"v2_cutoff_period{period}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with out_path.open("w", encoding="utf-8", newline="") as fp:
        w = csv.writer(fp)
        w.writerow(["ticker", "days_requested", "period_s", "start", "end",
                    "candles_received", "first_ts", "last_ts",
                    "err_code", "end_marker"])

        now = datetime.now()
        for sym in tickers:
            for n in days_list:
                start_dt = now - timedelta(days=n)
                start = fmt_dt_compact(start_dt)
                end = fmt_dt_compact(now)
                candles, errs, end_marker = run_candlerange(hist, sym, start, end, period)
                first_ts = f"{candles[0]['date']} {candles[0]['time']}" if candles else ""
                last_ts = f"{candles[-1]['date']} {candles[-1]['time']}" if candles else ""
                err_code = errs[0].get("code", "") if errs else ""
                w.writerow([sym, n, period, start, end, len(candles),
                            first_ts, last_ts, err_code, end_marker])
                print(f"[v2-cutoff] {sym:14s} days={n:3d}  candles={len(candles):6d}  "
                      f"first={first_ts:19s}  err={err_code or '-':4s}  end={end_marker}")
                time.sleep(gap_s)
    hist.close()
    print(f"[v2-cutoff] csv → {out_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="DAPI probe runner — V-1 e V-2")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("sanity",
                       help="banner + CANDLERANGE daily 10g FIB6F+DITAS")
    s.set_defaults(func=cmd_sanity)

    c = sub.add_parser("v1-capture",
                       help="cattura realtime SUB nelle finestre 9:00-9:30 o 14:30-15:00")
    c.add_argument("--window", required=True, choices=list(WINDOWS))
    c.add_argument("--tickers", default=",".join(DEFAULT_TICKERS_V1))
    c.set_defaults(func=cmd_v1_capture)

    f = sub.add_parser("v1-fetch",
                       help="CANDLERANGE 1-min per le due finestre V-1 di una data")
    f.add_argument("--date", required=True, help="yyyy-mm-dd")
    f.add_argument("--tickers", default=",".join(DEFAULT_TICKERS_V1))
    f.set_defaults(func=cmd_v1_fetch)

    d = sub.add_parser("v1-compare",
                       help="diff bit-a-bit barre locali vs CANDLERANGE")
    d.add_argument("--capture", required=True, help="CSV decoded da v1-capture")
    d.add_argument("--hist",    required=True, help="CSV barre da v1-fetch")
    d.set_defaults(func=cmd_v1_compare)

    v = sub.add_parser("v2-cutoff",
                       help="CANDLERANGE indietro con range crescente per cut-off")
    v.add_argument("--tickers", default=",".join(DEFAULT_TICKERS_V2))
    v.add_argument("--period",  default="60",
                   help="period_s: 60=1min, 86400=daily")
    v.add_argument("--days",    default="",
                   help="lista giorni csv (default lista standard 50..160)")
    v.add_argument("--gap",     default="0.6",
                   help="gap secondi tra comandi (rate-limit, default 0.6s)")
    v.set_defaults(func=cmd_v2_cutoff)
    return p


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
