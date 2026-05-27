#!/usr/bin/env python3
from __future__ import annotations

"""
Programma standalone e parametrico per scaricare da Directa/Darwin la serie storica
di un ticker qualsiasi nei timeframe W, D, 1H, 15M, 5M.

Come si usa nel modo più semplice:
1) modifica il file JSON:
       scripts/directa_history_export_config.json
   impostando almeno:
       - symbol
       - start
       - end
2) esegui:
       python scripts/export_directa_history_parametric.py
   oppure il launcher CMD dedicato.

Cosa fa:
- si connette al socket locale delle chiamate storiche di Darwin/Directa;
- usa i comandi CANDLERANGE previsti dalle API Directa;
- spezza automaticamente le richieste intraday in chunk da massimo 100 giorni;
- salva un CSV per timeframe, un CSV unificato e un manifest JSON;
- prova il weekly diretto; se non disponibile lo ricostruisce dal daily;
- prova 1H/15M/5M direttamente; se necessario ricostruisce da 1M;
- permette di cambiare ticker e range date senza toccare la logica del programma.

Output predefinito:
    <root_progetto>/exports/directa_history/<symbol>_<start>_<end>/

Esempio base:
    python scripts/export_directa_history_parametric.py

Esempio con profilo alternativo:
    python scripts/export_directa_history_parametric.py --config scripts/mio_profilo.json

Override da riga di comando:
    python scripts/export_directa_history_parametric.py --symbol MINI6C --start 2025-09-23 --end 2026-03-13

Requisiti operativi:
- Darwin aperta e loggata con API abilitate.
- Socket storico attivo sulla porta locale delle chiamate storiche.
"""

import argparse
import csv
import json
import socket
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Iterable, Sequence

DEFAULT_SYMBOL = "MINI5L"
DEFAULT_START = date(2025, 6, 25)
DEFAULT_END = date(2025, 12, 19)
DEFAULT_HOST = "127.0.0.1"
DEFAULT_TIMEOUT_SECONDS = 45.0
DEFAULT_INTRADAY_MAX_DAYS = 100
DEFAULT_PORT_SETTINGS = Path.home() / ".directa" / "engine" / "APIPortSettings.txt"
DEFAULT_CONFIG_FILENAME = "directa_history_export_config.json"

DATE_ONLY_FMT = "%Y-%m-%d"
DIRECTA_TS_FMT = "%Y%m%d%H%M%S"
CSV_TS_FMT = "%Y-%m-%d %H:%M:%S"

CONFIG_KEYS = {
    "symbol",
    "start",
    "end",
    "host",
    "historical_port",
    "account_code",
    "port_settings_path",
    "output_dir",
    "timeout_seconds",
    "delimiter",
}

BUILTIN_DEFAULTS: dict[str, Any] = {
    "symbol": DEFAULT_SYMBOL,
    "start": DEFAULT_START.strftime(DATE_ONLY_FMT),
    "end": DEFAULT_END.strftime(DATE_ONLY_FMT),
    "host": DEFAULT_HOST,
    "historical_port": None,
    "account_code": None,
    "port_settings_path": str(DEFAULT_PORT_SETTINGS),
    "output_dir": None,
    "timeout_seconds": DEFAULT_TIMEOUT_SECONDS,
    "delimiter": ",",
}


class DirectaError(RuntimeError):
    """Errore generico del protocollo Directa."""


@dataclass(frozen=True)
class Candle:
    symbol: str
    timeframe: str
    ts: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int
    source: str

    def csv_row(self) -> dict[str, str | int]:
        return {
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "timestamp": self.ts.strftime(CSV_TS_FMT),
            "date": self.ts.strftime(DATE_ONLY_FMT),
            "time": self.ts.strftime("%H:%M:%S"),
            "open": dec_to_str(self.open),
            "high": dec_to_str(self.high),
            "low": dec_to_str(self.low),
            "close": dec_to_str(self.close),
            "volume": self.volume,
            "source": self.source,
        }


@dataclass
class FetchResult:
    timeframe: str
    candles: list[Candle]
    mode: str
    commands: list[str]
    warnings: list[str]

    def summary(self) -> dict[str, str | int | list[str] | None]:
        return {
            "timeframe": self.timeframe,
            "mode": self.mode,
            "rows": len(self.candles),
            "first_timestamp": self.candles[0].ts.strftime(CSV_TS_FMT) if self.candles else None,
            "last_timestamp": self.candles[-1].ts.strftime(CSV_TS_FMT) if self.candles else None,
            "commands": self.commands,
            "warnings": self.warnings,
        }


class SocketLineReader:
    def __init__(self, sock: socket.socket, *, encoding: str = "utf-8") -> None:
        self.sock = sock
        self.encoding = encoding
        self.buffer = b""

    def readline(self, timeout_seconds: float) -> str | None:
        self.sock.settimeout(timeout_seconds)
        while b"\n" not in self.buffer:
            chunk = self.sock.recv(4096)
            if not chunk:
                if self.buffer:
                    line = self.buffer
                    self.buffer = b""
                    return line.decode(self.encoding, errors="replace").rstrip("\r")
                return None
            self.buffer += chunk
        raw_line, self.buffer = self.buffer.split(b"\n", 1)
        return raw_line.decode(self.encoding, errors="replace").rstrip("\r")


class DirectaHistoricalClient:
    def __init__(
        self,
        *,
        host: str,
        port: int,
        timeout_seconds: float,
        verbose: bool = True,
    ) -> None:
        self.host = host
        self.port = port
        self.timeout_seconds = timeout_seconds
        self.verbose = verbose
        self.sock: socket.socket | None = None
        self.reader: SocketLineReader | None = None
        self.banner: str | None = None
        self.command_log: list[str] = []

    def __enter__(self) -> "DirectaHistoricalClient":
        self.sock = socket.create_connection((self.host, self.port), timeout=self.timeout_seconds)
        self.reader = SocketLineReader(self.sock)
        try:
            self.banner = self.reader.readline(self.timeout_seconds)
        except socket.timeout:
            self.banner = None
        if self.verbose:
            if self.banner:
                print(f"[Directa] banner: {self.banner}")
            else:
                print("[Directa] nessun banner iniziale ricevuto, proseguo comunque.")
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.sock is not None:
            try:
                self.sock.close()
            except OSError:
                pass

    def send(self, command: str) -> None:
        if self.sock is None:
            raise RuntimeError("Socket non inizializzato")
        payload = (command + "\n").encode("utf-8")
        self.sock.sendall(payload)
        self.command_log.append(command)
        if self.verbose:
            print(f"[TX] {command}")

    def request_candles(
        self,
        *,
        symbol: str,
        start_dt: datetime,
        end_dt: datetime,
        period_seconds: int,
    ) -> tuple[list[str], list[str], str]:
        if self.reader is None:
            raise RuntimeError("Reader non inizializzato")

        command = (
            f"CANDLERANGE {symbol} {start_dt.strftime(DIRECTA_TS_FMT)} "
            f"{end_dt.strftime(DIRECTA_TS_FMT)} {period_seconds}"
        )
        self.send(command)

        raw_candles: list[str] = []
        warnings: list[str] = []
        seen_any_data = False
        seen_end = False

        while True:
            try:
                line = self.reader.readline(self.timeout_seconds)
            except socket.timeout as exc:
                if seen_any_data:
                    warnings.append(
                        "Timeout dopo ricezione dati: nessun END CANDLES ricevuto, accetto il buffer raccolto."
                    )
                    break
                raise DirectaError(
                    f"Timeout in attesa della risposta al comando {command!r}."
                ) from exc

            if line is None:
                if seen_any_data:
                    warnings.append(
                        "Socket chiuso dopo ricezione dati: nessun END CANDLES ricevuto, accetto il buffer raccolto."
                    )
                    break
                raise DirectaError(
                    f"Socket chiuso senza dati utili per il comando {command!r}."
                )

            text = line.strip()
            if not text:
                continue
            if text == "H":
                continue
            if text.startswith("DARWIN_STATUS"):
                if self.verbose:
                    print(f"[RX] {text}")
                continue
            if self.verbose:
                print(f"[RX] {text}")

            candle_lines = extract_candle_lines(text)
            if candle_lines:
                raw_candles.extend(candle_lines)
                seen_any_data = True

            if is_error_line(text):
                raise DirectaError(f"Risposta di errore Directa per {command!r}: {text}")

            if text.startswith("END CANDLES") or text == "END CANDLES":
                seen_end = True
                break
            if "END CANDLES" in text and candle_lines:
                seen_end = True
                break

        status = "END_RECEIVED" if seen_end else "END_NOT_RECEIVED"
        return raw_candles, warnings, status


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Esporta lo storico Directa in CSV per W, D, 1H, 15M, 5M. "
            "Ticker e date possono essere presi dal file di configurazione JSON."
        )
    )
    parser.add_argument(
        "--config",
        default=None,
        help=(
            f"Profilo JSON da usare. Se omesso provo il file {DEFAULT_CONFIG_FILENAME} "
            "nella stessa cartella dello script."
        ),
    )
    parser.add_argument(
        "--symbol",
        default=None,
        help="Ticker Directa da scaricare. Se omesso uso il file config o il default integrato.",
    )
    parser.add_argument(
        "--start",
        default=None,
        help="Data iniziale inclusa, formato YYYY-MM-DD. Override del file config.",
    )
    parser.add_argument(
        "--end",
        default=None,
        help="Data finale inclusa, formato YYYY-MM-DD. Override del file config.",
    )
    parser.add_argument("--host", default=None, help="Host locale del socket Directa.")
    parser.add_argument(
        "--historical-port",
        type=int,
        default=None,
        help="Porta storica Directa. Se omessa provo config/file APIPortSettings.txt.",
    )
    parser.add_argument(
        "--account-code",
        default=None,
        help="Codice utenza da usare nel file APIPortSettings.txt. Se omesso uso config o la prima riga.",
    )
    parser.add_argument(
        "--port-settings-path",
        default=None,
        help="Percorso del file APIPortSettings.txt generato da Darwin.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Cartella di output. Se omessa uso exports/directa_history/<symbol>_<start>_<end>.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=None,
        help="Timeout massimo di inattività per singola lettura socket.",
    )
    parser.add_argument(
        "--delimiter",
        default=None,
        help="Separatore CSV finale. Default: ',' . Per Excel IT puoi usare ';'.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Riduce l'output a console.",
    )
    return parser.parse_args()


def sidecar_config_path() -> Path:
    return Path(__file__).with_name(DEFAULT_CONFIG_FILENAME)


def load_job_config(config_path: Path) -> tuple[dict[str, Any], list[str]]:
    warnings: list[str] = []
    if not config_path.exists():
        return {}, warnings

    try:
        raw = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"Il file di configurazione {config_path} non è un JSON valido: {exc}"
        ) from exc

    if not isinstance(raw, dict):
        raise SystemExit(f"Il file di configurazione {config_path} deve contenere un oggetto JSON.")

    unknown = sorted(set(raw) - CONFIG_KEYS)
    if unknown:
        warnings.append(
            "Chiavi sconosciute nel file config ignorate: " + ", ".join(unknown)
        )

    config = {key: raw.get(key) for key in CONFIG_KEYS if key in raw}
    return config, warnings


def merge_runtime_options(args: argparse.Namespace, config_data: dict[str, Any]) -> dict[str, Any]:
    merged = dict(BUILTIN_DEFAULTS)
    for key, value in config_data.items():
        merged[key] = value

    cli_map = {
        "symbol": args.symbol,
        "start": args.start,
        "end": args.end,
        "host": args.host,
        "historical_port": args.historical_port,
        "account_code": args.account_code,
        "port_settings_path": args.port_settings_path,
        "output_dir": args.output_dir,
        "timeout_seconds": args.timeout_seconds,
        "delimiter": args.delimiter,
    }
    for key, value in cli_map.items():
        if value is not None:
            merged[key] = value

    return merged


def is_error_line(text: str) -> bool:
    low = text.lower()
    if text.startswith("ERR"):
        return True
    if text.startswith("Wrong "):
        return True
    if text.startswith("Not enough parameters"):
        return True
    return any(token in low for token in ("error", "errore", "not enabled", "not valid"))


def extract_candle_lines(text: str) -> list[str]:
    if "CANDLE;" not in text:
        return []

    out: list[str] = []
    for idx, chunk in enumerate(text.split("CANDLE;")):
        if idx == 0:
            continue
        piece = "CANDLE;" + chunk
        if "END CANDLES" in piece:
            piece = piece.split("END CANDLES", 1)[0].strip()
        piece = piece.strip()
        if piece:
            out.append(piece)
    return out


def parse_date_only(value: str) -> date:
    try:
        return datetime.strptime(value, DATE_ONLY_FMT).date()
    except ValueError as exc:
        raise SystemExit(f"Data non valida: {value!r}. Atteso formato YYYY-MM-DD.") from exc


def start_of_day(d: date) -> datetime:
    return datetime(d.year, d.month, d.day, 0, 0, 0)


def end_of_day(d: date) -> datetime:
    return datetime(d.year, d.month, d.day, 23, 59, 59)


def dec_to_str(value: Decimal) -> str:
    s = format(value, "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s or "0"


def parse_directa_candle(line: str, *, timeframe: str, source: str) -> Candle:
    parts = line.split(";")
    if len(parts) < 9:
        raise DirectaError(f"Linea CANDLE non valida: {line!r}")
    kind, symbol, ymd, hms, uff, min_, max_, ape, qty = parts[:9]
    if kind != "CANDLE":
        raise DirectaError(f"Tipo record non valido: {line!r}")

    ts = datetime.strptime(f"{ymd}{hms.replace(':', '')}", DIRECTA_TS_FMT)
    try:
        # Documentazione Directa: UFF, MIN, MAX, APE => close, low, high, open.
        close_v = Decimal(uff)
        low_v = Decimal(min_)
        high_v = Decimal(max_)
        open_v = Decimal(ape)
        volume_v = int(Decimal(qty))
    except (InvalidOperation, ValueError) as exc:
        raise DirectaError(f"Valori numerici non validi nella linea {line!r}") from exc

    return Candle(
        symbol=symbol,
        timeframe=timeframe,
        ts=ts,
        open=open_v,
        high=high_v,
        low=low_v,
        close=close_v,
        volume=volume_v,
        source=source,
    )


def sort_and_deduplicate(candles: Iterable[Candle]) -> list[Candle]:
    by_key: dict[tuple[str, datetime], Candle] = {}
    for candle in candles:
        by_key[(candle.timeframe, candle.ts)] = candle
    return [by_key[key] for key in sorted(by_key, key=lambda item: item[1])]


def chunk_ranges(
    start_dt: datetime,
    end_dt: datetime,
    *,
    max_days: int,
) -> list[tuple[datetime, datetime]]:
    if max_days <= 0:
        raise ValueError("max_days deve essere positivo")

    out: list[tuple[datetime, datetime]] = []
    cursor = start_dt
    max_span = timedelta(days=max_days) - timedelta(seconds=1)
    while cursor <= end_dt:
        chunk_end = min(cursor + max_span, end_dt)
        out.append((cursor, chunk_end))
        cursor = chunk_end + timedelta(seconds=1)
    return out


def floor_timestamp(dt: datetime, period_seconds: int) -> datetime:
    if period_seconds >= 86400:
        return datetime(dt.year, dt.month, dt.day, 0, 0, 0)
    day_start = datetime(dt.year, dt.month, dt.day, 0, 0, 0)
    seconds = dt.hour * 3600 + dt.minute * 60 + dt.second
    bucket = (seconds // period_seconds) * period_seconds
    return day_start + timedelta(seconds=bucket)


def aggregate_fixed_period(
    candles: Sequence[Candle],
    *,
    target_timeframe: str,
    target_period_seconds: int,
    source_label: str,
) -> list[Candle]:
    groups: dict[datetime, list[Candle]] = defaultdict(list)
    for candle in candles:
        bucket = floor_timestamp(candle.ts, target_period_seconds)
        groups[bucket].append(candle)

    out: list[Candle] = []
    for bucket in sorted(groups):
        bars = sorted(groups[bucket], key=lambda c: c.ts)
        first = bars[0]
        last = bars[-1]
        high = max(c.high for c in bars)
        low = min(c.low for c in bars)
        volume = sum(c.volume for c in bars)
        out.append(
            Candle(
                symbol=first.symbol,
                timeframe=target_timeframe,
                ts=bucket,
                open=first.open,
                high=high,
                low=low,
                close=last.close,
                volume=volume,
                source=source_label,
            )
        )
    return out


def aggregate_weekly_from_daily(daily: Sequence[Candle], *, target_timeframe: str = "W") -> list[Candle]:
    groups: dict[date, list[Candle]] = defaultdict(list)
    for candle in daily:
        monday = candle.ts.date() - timedelta(days=candle.ts.weekday())
        groups[monday].append(candle)

    out: list[Candle] = []
    for monday in sorted(groups):
        bars = sorted(groups[monday], key=lambda c: c.ts)
        first = bars[0]
        last = bars[-1]
        high = max(c.high for c in bars)
        low = min(c.low for c in bars)
        volume = sum(c.volume for c in bars)
        out.append(
            Candle(
                symbol=first.symbol,
                timeframe=target_timeframe,
                ts=first.ts,
                open=first.open,
                high=high,
                low=low,
                close=last.close,
                volume=volume,
                source="AGG_FROM_D",
            )
        )
    return out


def write_csv(path: Path, candles: Sequence[Candle], *, delimiter: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "symbol",
                "timeframe",
                "timestamp",
                "date",
                "time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "source",
            ],
            delimiter=delimiter,
        )
        writer.writeheader()
        for candle in candles:
            writer.writerow(candle.csv_row())


def discover_historical_port(
    port_settings_path: Path,
    *,
    account_code: str | None,
) -> tuple[int, str | None, list[str]]:
    warnings: list[str] = []
    if not port_settings_path.exists():
        raise SystemExit(
            f"File porte Directa non trovato: {port_settings_path}. "
            "Apri Darwin oppure passa --historical-port manualmente."
        )

    rows: list[tuple[str, int]] = []
    for raw in port_settings_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split(";")]
        if len(parts) < 4:
            continue
        user_code = parts[0]
        try:
            historical_port = int(parts[3])
        except ValueError:
            continue
        rows.append((user_code, historical_port))

    if not rows:
        raise SystemExit(
            f"Nessuna porta storica valida trovata in {port_settings_path}. "
            "Passa --historical-port manualmente."
        )

    if account_code is not None:
        for user_code, historical_port in rows:
            if user_code == account_code:
                return historical_port, user_code, warnings
        raise SystemExit(
            f"Codice utenza {account_code!r} non trovato in {port_settings_path}."
        )

    if len(rows) > 1:
        warnings.append(
            "Più utenze trovate in APIPortSettings.txt: uso la prima riga. "
            "Per forzare una utenza specifica passa --account-code."
        )
    return rows[0][1], rows[0][0], warnings


def fetch_direct(
    client: DirectaHistoricalClient,
    *,
    symbol: str,
    timeframe: str,
    period_seconds: int,
    start_dt: datetime,
    end_dt: datetime,
    intraday_max_days: int,
) -> tuple[list[Candle], list[str], list[str]]:
    warnings: list[str] = []
    commands_before = len(client.command_log)
    raw_lines: list[str] = []

    ranges = (
        chunk_ranges(start_dt, end_dt, max_days=intraday_max_days)
        if period_seconds < 86400
        else [(start_dt, end_dt)]
    )

    for chunk_start, chunk_end in ranges:
        chunk_lines, chunk_warnings, end_status = client.request_candles(
            symbol=symbol,
            start_dt=chunk_start,
            end_dt=chunk_end,
            period_seconds=period_seconds,
        )
        if end_status != "END_RECEIVED":
            warnings.append(
                f"{timeframe} {chunk_start.strftime(CSV_TS_FMT)} -> {chunk_end.strftime(CSV_TS_FMT)}: END CANDLES non ricevuto."
            )
        warnings.extend(chunk_warnings)
        raw_lines.extend(chunk_lines)

    candles = [parse_directa_candle(line, timeframe=timeframe, source="DIRECTA") for line in raw_lines]
    candles = [c for c in candles if start_dt <= c.ts <= end_dt]
    candles = sort_and_deduplicate(candles)
    commands = client.command_log[commands_before:]
    return candles, warnings, commands


def build_fetch_plan(
    client: DirectaHistoricalClient,
    *,
    symbol: str,
    start_dt: datetime,
    end_dt: datetime,
    intraday_max_days: int,
) -> tuple[dict[str, FetchResult], list[str]]:
    all_warnings: list[str] = []
    results: dict[str, FetchResult] = {}
    cache: dict[str, list[Candle]] = {}

    def fetch_daily() -> list[Candle]:
        if "D" not in cache:
            candles, warnings, commands = fetch_direct(
                client,
                symbol=symbol,
                timeframe="D",
                period_seconds=86400,
                start_dt=start_dt,
                end_dt=end_dt,
                intraday_max_days=intraday_max_days,
            )
            results["D"] = FetchResult(
                timeframe="D",
                candles=candles,
                mode="DIRECTA_86400",
                commands=commands,
                warnings=list(warnings),
            )
            cache["D"] = candles
            all_warnings.extend(warnings)
        return cache["D"]

    def fetch_or_aggregate_intraday(
        *,
        timeframe: str,
        direct_period_seconds: int,
        fallback_period_seconds: int | None = None,
    ) -> None:
        warnings: list[str] = []
        commands_before = len(client.command_log)
        try:
            candles, direct_warnings, _ = fetch_direct(
                client,
                symbol=symbol,
                timeframe=timeframe,
                period_seconds=direct_period_seconds,
                start_dt=start_dt,
                end_dt=end_dt,
                intraday_max_days=intraday_max_days,
            )
            warnings.extend(direct_warnings)
            if candles:
                results[timeframe] = FetchResult(
                    timeframe=timeframe,
                    candles=candles,
                    mode=f"DIRECTA_{direct_period_seconds}",
                    commands=client.command_log[commands_before:],
                    warnings=warnings,
                )
                cache[timeframe] = candles
                all_warnings.extend(warnings)
                return
            warnings.append(
                f"Nessun dato ricevuto direttamente per {timeframe} ({direct_period_seconds}s)."
            )
        except DirectaError as exc:
            warnings.append(str(exc))

        if fallback_period_seconds is None:
            results[timeframe] = FetchResult(
                timeframe=timeframe,
                candles=[],
                mode=f"DIRECTA_{direct_period_seconds}_FAILED",
                commands=client.command_log[commands_before:],
                warnings=warnings,
            )
            cache[timeframe] = []
            all_warnings.extend(warnings)
            return

        base_tf = f"{fallback_period_seconds}s"
        if base_tf not in cache:
            base_candles, base_warnings, _ = fetch_direct(
                client,
                symbol=symbol,
                timeframe=base_tf,
                period_seconds=fallback_period_seconds,
                start_dt=start_dt,
                end_dt=end_dt,
                intraday_max_days=intraday_max_days,
            )
            cache[base_tf] = base_candles
            all_warnings.extend(base_warnings)
            if base_warnings:
                warnings.extend(base_warnings)

        aggregated = aggregate_fixed_period(
            cache[base_tf],
            target_timeframe=timeframe,
            target_period_seconds=direct_period_seconds,
            source_label=f"AGG_FROM_{base_tf}",
        )
        aggregated = [c for c in aggregated if start_dt <= c.ts <= end_dt]
        aggregated = sort_and_deduplicate(aggregated)
        warnings.append(
            f"{timeframe} ricostruito aggregando i dati {base_tf} perché il diretto non era disponibile o non ha restituito barre."
        )
        results[timeframe] = FetchResult(
            timeframe=timeframe,
            candles=aggregated,
            mode=f"AGG_FROM_{base_tf}",
            commands=client.command_log[commands_before:],
            warnings=warnings,
        )
        cache[timeframe] = aggregated
        all_warnings.extend(warnings)

    fetch_daily()

    weekly_warnings: list[str] = []
    weekly_commands_before = len(client.command_log)
    try:
        weekly_direct, direct_warnings, _ = fetch_direct(
            client,
            symbol=symbol,
            timeframe="W",
            period_seconds=604800,
            start_dt=start_dt,
            end_dt=end_dt,
            intraday_max_days=intraday_max_days,
        )
        weekly_warnings.extend(direct_warnings)
        if weekly_direct:
            results["W"] = FetchResult(
                timeframe="W",
                candles=weekly_direct,
                mode="DIRECTA_604800",
                commands=client.command_log[weekly_commands_before:],
                warnings=weekly_warnings,
            )
            cache["W"] = weekly_direct
            all_warnings.extend(weekly_warnings)
        else:
            weekly_warnings.append("Nessun weekly diretto ricevuto: ricostruisco dal daily.")
            weekly_from_daily = aggregate_weekly_from_daily(fetch_daily())
            results["W"] = FetchResult(
                timeframe="W",
                candles=weekly_from_daily,
                mode="AGG_FROM_D",
                commands=client.command_log[weekly_commands_before:],
                warnings=weekly_warnings,
            )
            cache["W"] = weekly_from_daily
            all_warnings.extend(weekly_warnings)
    except DirectaError as exc:
        weekly_warnings.append(str(exc))
        weekly_warnings.append("Weekly ricostruito dal daily.")
        weekly_from_daily = aggregate_weekly_from_daily(fetch_daily())
        results["W"] = FetchResult(
            timeframe="W",
            candles=weekly_from_daily,
            mode="AGG_FROM_D",
            commands=client.command_log[weekly_commands_before:],
            warnings=weekly_warnings,
        )
        cache["W"] = weekly_from_daily
        all_warnings.extend(weekly_warnings)

    fetch_or_aggregate_intraday(timeframe="1H", direct_period_seconds=3600, fallback_period_seconds=60)
    fetch_or_aggregate_intraday(timeframe="15M", direct_period_seconds=900, fallback_period_seconds=60)
    fetch_or_aggregate_intraday(timeframe="5M", direct_period_seconds=300, fallback_period_seconds=60)

    return results, all_warnings


def make_default_output_dir(script_file: Path, *, symbol: str, start_d: date, end_d: date) -> Path:
    project_root = script_file.resolve().parents[1]
    return (
        project_root
        / "exports"
        / "directa_history"
        / f"{symbol}_{start_d.strftime('%Y%m%d')}_{end_d.strftime('%Y%m%d')}"
    )


def write_manifest(
    path: Path,
    *,
    symbol: str,
    start_d: date,
    end_d: date,
    host: str,
    historical_port: int,
    account_code: str | None,
    port_settings_path: Path,
    banner: str | None,
    results: dict[str, FetchResult],
    warnings: list[str],
    generated_files: list[str],
    command_log: list[str],
    config_path: Path,
    config_payload: dict[str, Any],
) -> None:
    payload = {
        "symbol": symbol,
        "requested_range": {
            "start": start_d.strftime(DATE_ONLY_FMT),
            "end": end_d.strftime(DATE_ONLY_FMT),
        },
        "connection": {
            "host": host,
            "historical_port": historical_port,
            "account_code": account_code,
            "port_settings_path": str(port_settings_path),
            "banner": banner,
        },
        "config": {
            "config_path": str(config_path),
            "resolved_values": config_payload,
        },
        "timeframes": {key: value.summary() for key, value in results.items()},
        "warnings": warnings,
        "generated_files": generated_files,
        "commands_sent": command_log,
        "generated_at": datetime.now().strftime(CSV_TS_FMT),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    args = parse_args()
    verbose = not args.quiet

    config_path = Path(args.config).expanduser() if args.config else sidecar_config_path()
    config_data, config_warnings = load_job_config(config_path)
    resolved = merge_runtime_options(args, config_data)

    symbol = str(resolved["symbol"]).strip().upper()
    start_d = parse_date_only(str(resolved["start"]))
    end_d = parse_date_only(str(resolved["end"]))
    if end_d < start_d:
        raise SystemExit("La data finale deve essere maggiore o uguale alla data iniziale.")

    host = str(resolved["host"]).strip()
    timeout_seconds = float(resolved["timeout_seconds"])
    delimiter = str(resolved["delimiter"])

    port_settings_path = Path(str(resolved["port_settings_path"])).expanduser()
    account_code = None if resolved["account_code"] in (None, "") else str(resolved["account_code"]).strip()
    output_dir_value = resolved["output_dir"]
    historical_port_value = resolved["historical_port"]

    start_dt = start_of_day(start_d)
    end_dt = end_of_day(end_d)

    port_warnings: list[str] = []
    resolved_account_code: str | None
    if historical_port_value is None:
        historical_port, resolved_account_code, port_warnings = discover_historical_port(
            port_settings_path,
            account_code=account_code,
        )
    else:
        historical_port = int(historical_port_value)
        resolved_account_code = account_code

    output_dir = (
        Path(str(output_dir_value)).expanduser()
        if output_dir_value not in (None, "")
        else make_default_output_dir(Path(__file__), symbol=symbol, start_d=start_d, end_d=end_d)
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    resolved_config_snapshot = {
        "symbol": symbol,
        "start": start_d.strftime(DATE_ONLY_FMT),
        "end": end_d.strftime(DATE_ONLY_FMT),
        "host": host,
        "historical_port": historical_port_value,
        "account_code": account_code,
        "port_settings_path": str(port_settings_path),
        "output_dir": str(output_dir) if output_dir_value not in (None, "") else None,
        "timeout_seconds": timeout_seconds,
        "delimiter": delimiter,
    }

    if verbose:
        print(f"[INFO] Config path    : {config_path}")
        print(f"[INFO] Symbol         : {symbol}")
        print(f"[INFO] Range          : {start_d} -> {end_d}")
        print(f"[INFO] Host/Port      : {host}:{historical_port}")
        if resolved_account_code:
            print(f"[INFO] Account code   : {resolved_account_code}")
        print(f"[INFO] Output dir     : {output_dir}")
        if config_warnings:
            for item in config_warnings:
                print(f"[WARN] {item}")
        if port_warnings:
            for item in port_warnings:
                print(f"[WARN] {item}")

    with DirectaHistoricalClient(
        host=host,
        port=historical_port,
        timeout_seconds=timeout_seconds,
        verbose=verbose,
    ) as client:
        results, all_warnings = build_fetch_plan(
            client,
            symbol=symbol,
            start_dt=start_dt,
            end_dt=end_dt,
            intraday_max_days=DEFAULT_INTRADAY_MAX_DAYS,
        )

        generated_files: list[str] = []
        ordered_timeframes = ["W", "D", "1H", "15M", "5M"]
        merged: list[Candle] = []

        for timeframe in ordered_timeframes:
            fetch_result = results.get(timeframe)
            if fetch_result is None:
                fetch_result = FetchResult(
                    timeframe=timeframe,
                    candles=[],
                    mode="NOT_RUN",
                    commands=[],
                    warnings=[],
                )
                results[timeframe] = fetch_result
            csv_path = output_dir / f"{symbol}_{timeframe}.csv"
            write_csv(csv_path, fetch_result.candles, delimiter=delimiter)
            generated_files.append(str(csv_path))
            merged.extend(fetch_result.candles)
            if verbose:
                print(
                    f"[OK] {timeframe:<4} -> {len(fetch_result.candles):>6} righe | "
                    f"modo={fetch_result.mode} | file={csv_path.name}"
                )
                for warning in fetch_result.warnings:
                    print(f"[WARN] {timeframe}: {warning}")

        merged = sort_and_deduplicate(merged)
        merged_path = output_dir / f"{symbol}_ALL.csv"
        write_csv(merged_path, merged, delimiter=delimiter)
        generated_files.append(str(merged_path))

        manifest_path = output_dir / f"{symbol}_manifest.json"
        all_warnings = config_warnings + port_warnings + all_warnings
        write_manifest(
            manifest_path,
            symbol=symbol,
            start_d=start_d,
            end_d=end_d,
            host=host,
            historical_port=historical_port,
            account_code=resolved_account_code,
            port_settings_path=port_settings_path,
            banner=client.banner,
            results=results,
            warnings=all_warnings,
            generated_files=generated_files + [str(manifest_path)],
            command_log=client.command_log,
            config_path=config_path,
            config_payload=resolved_config_snapshot,
        )
        generated_files.append(str(manifest_path))

    if verbose:
        print("[DONE] File generati:")
        for item in generated_files:
            print(f"       - {item}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
