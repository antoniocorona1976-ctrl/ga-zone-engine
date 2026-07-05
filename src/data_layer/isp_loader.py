"""M0-T1 — loader fixture ISP (Portara sample 9-colonne) -> griglia canonica 13-campi.

Card: Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_M0-T1_v2.md (SS3) + ciclo di fix
Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_M0-T1-FIX-01.md (SS1-SS2).
Fixture (GC-3): data/samples/portara_isp/ISP2023Z.txt, tracciata nel repo dal
commit c78c358 "M0-T1-FIX: fixture ISP tracciata (GC-3)".

Requisiti-fonte (GC-2):
- R-9.3  docs/spec_funzionale/SPEC_FUNZ_01.md:1224 — griglia 1-min uniforme per la
  sessione 08:00-22:00 CET; minuti senza trade: Open=High=Low=Close=Close del minuto
  precedente, Volume=0, tick_count=0.
- R-9.14 docs/spec_funzionale/SPEC_FUNZ_01.md:1279 — bar_synthetic=False se la barra
  compare nel dato di partenza, True altrimenti (forward-fill su Close).
- CN-9.5 docs/spec_funzionale/SPEC_FUNZ_01.md:1335 — header CSV esteso a 13 campi esatti.
- CN-9.7 docs/spec_funzionale/SPEC_FUNZ_01.md:1341 — tick_count intero >=0 oppure NULL;
  bar_synthetic booleano True/False.
- CN-9.9 docs/spec_funzionale/SPEC_FUNZ_01.md:1347 — timestamp = chiave normativa di
  allineamento (start-of-bar); date/time campi derivati di comodita'.
- DEC-C (Codice/Piano_di_lavoro/DECISIONI.md): source = "PORTARA" per tutte le barre
  del dataset di training M0, reali e sintetiche.
- DEC-D (Codice/Piano_di_lavoro/DECISIONI.md): symbol = "FIB"; timeframe = token della
  convenzione del decoder legacy: "60s"
  [CODICE-ESISTENTE scripts/export_directa_history_parametric.py:797 `base_tf =
  f"{fallback_period_seconds}s"`, usato come timeframe a r.802 con
  fallback_period_seconds=60 (r.885-887); concorde con il dominio AGG_FROM_60s di
  CN-9.8, docs/spec_funzionale/SPEC_FUNZ_01.md:1344].

Formati di timestamp/date/time: stesse convenzioni del decoder legacy
[CODICE-ESISTENTE scripts/export_directa_history_parametric.py:65,67,116-118]:
"%Y-%m-%d %H:%M:%S" / "%Y-%m-%d" / "%H:%M:%S".

Formato del sample (PROVA-EMPIRICA 2026-07-05, dettaglio e alternative escluse nei
blocchi RM-1 di Codice/Piano_di_lavoro/Esito/ESITO_M0-T1.md):
  col1=symbol, col2=date YYYYMMDD, col3=time HHMM (start-of-bar, tz del vendor),
  col4=open, col5=high, col6=low, col7=close, col8=tick_count, col9=volume.
Discriminante settle-row: volume == 0 (unica riga del sample; flat, prezzo off-tick,
orario fuori sequenza in coda al file).

Politica giorni parziali — DEC-E (Codice/Piano_di_lavoro/DECISIONI.md, commit
01c53aa): i giorni a copertura parziale ai BORDI del dataset (primo/ultimo giorno
osservato, incompleti rispetto alla sessione 08:00-22:00) sono ESCLUSI dalla
griglia, con conteggio ed elenco espliciti nel report del loader
(`GridReport.excluded_edge_days`) — mai scarto silenzioso. Parzialita' nei giorni
INTERNI = anomalia riportata in `GridReport.internal_partial_days` (il giorno resta
in griglia sull'intervallo osservato; gestione decisa in M0-T2). Sessioni corte da
calendario di borsa: policy rinviata a M0-T2.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

# CN-9.5 (docs/spec_funzionale/SPEC_FUNZ_01.md:1335): 13 campi esatti, in quest'ordine.
CANONICAL_HEADER = [
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
    "tick_count",
    "bar_synthetic",
    "source",
]

SYMBOL_DEFAULT = "FIB"  # DEC-D
TIMEFRAME_DEFAULT = "60s"  # DEC-D + [CODICE-ESISTENTE export_directa_history_parametric.py:797]
SOURCE_DEFAULT = "PORTARA"  # DEC-C

# R-9.3 (docs/spec_funzionale/SPEC_FUNZ_01.md:1224): sessione 08:00-22:00 CET.
SESSION_START = time(8, 0)
SESSION_END = time(22, 0)  # esclusivo: ultimo start-of-bar della griglia = 21:59
SESSION_MINUTES = 840

# FIB: tick da 5 punti (memoria di progetto; il sample ISP mostra print off-tick
# residui, da diagnosticare senza clamping ne' drop — card SS3.6).
TICK_SIZE = 5

# "CET" del contratto = ora locale italiana (zona IANA con gestione CEST).
CET_ZONE = "Europe/Rome"

_TS_FMT = "%Y-%m-%d %H:%M:%S"
_DATE_FMT = "%Y-%m-%d"
_TIME_FMT = "%H:%M:%S"


@dataclass(frozen=True)
class RawBar:
    """Barra 1-min del sample, nelle coordinate native del vendor (tz sorgente)."""

    symbol: str
    date: str  # YYYYMMDD
    time: str  # HHMM (start-of-bar)
    open: int
    high: int
    low: int
    close: int
    tick_count: int
    volume: int


@dataclass(frozen=True)
class ParseResult:
    bars: tuple[RawBar, ...]  # barre valide (settle-row escluse)
    settle_rows: tuple[RawBar, ...]  # righe con volume == 0 (discriminante settle)
    n_raw: int  # righe totali lette dal file


@dataclass(frozen=True)
class OffTick:
    """Prezzo non allineato alla griglia tick (valore % TICK_SIZE != 0)."""

    date: str  # YYYYMMDD nativo del sample
    time: str  # HHMM nativo del sample
    field: str  # open / high / low / close
    value: int


@dataclass(frozen=True)
class PartialDay:
    """Giorno a copertura parziale rispetto alla sessione 08:00-22:00 CET (DEC-E)."""

    date: str  # YYYY-MM-DD (CET)
    rows_observed: int  # ampiezza copertura [prima reale, ultima reale] in minuti
    real_bars: int  # barre reali osservate nel giorno
    first_time: str  # prima barra reale (HH:MM:SS CET)
    last_time: str  # ultima barra reale (HH:MM:SS CET)


@dataclass(frozen=True)
class GridReport:
    """Report del loader (DEC-E): esclusioni ed anomalie, mai scarto silenzioso."""

    excluded_edge_days: tuple[PartialDay, ...]  # giorni di bordo parziali ESCLUSI
    internal_partial_days: tuple[PartialDay, ...]  # anomalie interne (gestione M0-T2)


@dataclass(frozen=True)
class GridResult:
    """Griglia canonica (frame) + report DEC-E del loader."""

    frame: pd.DataFrame
    report: GridReport


def parse_isp_file(path: str | Path) -> ParseResult:
    """Legge il sample ISP 9-colonne e filtra le settle-row (volume == 0).

    Nessun clamping, nessun drop oltre al filtro settle: gli off-tick restano
    nelle barre e vengono elencati da :func:`tick_grid_findings` (card SS3.6).
    """
    bars: list[RawBar] = []
    settle: list[RawBar] = []
    n_raw = 0
    with open(path, "r", encoding="ascii") as handle:
        for lineno, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) != 9:
                raise ValueError(
                    f"{path}:{lineno}: attese 9 colonne, trovate {len(parts)}"
                )
            bar = RawBar(
                symbol=parts[0],
                date=parts[1],
                time=parts[2].zfill(4),
                open=int(parts[3]),
                high=int(parts[4]),
                low=int(parts[5]),
                close=int(parts[6]),
                tick_count=int(parts[7]),
                volume=int(parts[8]),
            )
            n_raw += 1
            if bar.volume == 0:
                settle.append(bar)
            else:
                bars.append(bar)
    return ParseResult(bars=tuple(bars), settle_rows=tuple(settle), n_raw=n_raw)


def tick_grid_findings(
    bars: tuple[RawBar, ...] | list[RawBar], tick_size: int = TICK_SIZE
) -> tuple[OffTick, ...]:
    """Diagnostica tick-grid: elenca ogni prezzo O/H/L/C non multiplo del tick.

    Solo rilevazione (finding): le barre non vengono alterate (card SS3.6).
    """
    findings: list[OffTick] = []
    for bar in bars:
        for field in ("open", "high", "low", "close"):
            value = getattr(bar, field)
            if value % tick_size != 0:
                findings.append(
                    OffTick(date=bar.date, time=bar.time, field=field, value=value)
                )
    return tuple(findings)


def _to_cet(bar: RawBar, src_zone: ZoneInfo, cet_zone: ZoneInfo) -> datetime:
    """Converte lo start-of-bar nativo del vendor in orario CET (naive)."""
    naive = datetime.strptime(bar.date + bar.time, "%Y%m%d%H%M")
    return naive.replace(tzinfo=src_zone).astimezone(cet_zone).replace(tzinfo=None)


def build_canonical_grid(
    bars: tuple[RawBar, ...] | list[RawBar],
    *,
    tz: str,
    symbol: str = SYMBOL_DEFAULT,
    timeframe: str = TIMEFRAME_DEFAULT,
    source: str = SOURCE_DEFAULT,
) -> GridResult:
    """Costruisce la griglia canonica 1-min a 13 campi (CN-9.5) in CET + report DEC-E.

    - ``tz``: zona IANA dei timestamp nativi del sample (parametro esplicito,
      card SS3.1); la normalizzazione avviene sempre verso ``Europe/Rome`` (CET).
    - griglia per giornata CET: passo 60s, chiave ``timestamp`` start-of-bar
      (CN-9.9), finestra di sessione 08:00-21:59 CET (R-9.3).
    - DEC-E (DECISIONI.md, commit 01c53aa): i giorni di bordo a copertura parziale
      sono esclusi dalla griglia ed elencati in ``report.excluded_edge_days``
      (data, righe osservate, barre reali); parzialita' nei giorni interni =
      anomalia in ``report.internal_partial_days`` (giorno tenuto in griglia
      sull'intervallo osservato; gestione decisa in M0-T2).
    - minuti no-trade: forward-fill R-9.3 con ``bar_synthetic=True``; barre
      presenti nel sample: ``bar_synthetic=False`` (R-9.14).
    """
    src_zone = ZoneInfo(tz)
    cet_zone = ZoneInfo(CET_ZONE)

    reals: dict[datetime, RawBar] = {}
    for bar in bars:
        cet_dt = _to_cet(bar, src_zone, cet_zone)
        if not (SESSION_START <= cet_dt.time() < SESSION_END):
            # fuori sessione: non entra nella griglia (R-9.3); sul sample
            # tracciato non accade (accertamento ESITO_M0-T1.md); contatore
            # diagnostico rinviato a M0-T2 (review M0-T1, finding #4)
            continue
        if cet_dt in reals:
            raise ValueError(f"barra duplicata sul minuto CET {cet_dt}")
        reals[cet_dt] = bar

    observed_days = sorted({dt.date() for dt in reals})
    excluded_edge: list[PartialDay] = []
    internal_partial: list[PartialDay] = []
    grid_days: list = []
    for idx, day in enumerate(observed_days):
        day_minutes = sorted(dt for dt in reals if dt.date() == day)
        first_real, last_real = day_minutes[0], day_minutes[-1]
        last_session_minute = datetime.combine(day, SESSION_END) - timedelta(minutes=1)
        is_complete = (
            first_real == datetime.combine(day, SESSION_START)
            and last_real == last_session_minute
        )
        if is_complete:
            grid_days.append(day)
            continue
        coverage = PartialDay(
            date=day.strftime(_DATE_FMT),
            rows_observed=int((last_real - first_real).total_seconds() // 60) + 1,
            real_bars=len(day_minutes),
            first_time=first_real.strftime(_TIME_FMT),
            last_time=last_real.strftime(_TIME_FMT),
        )
        if idx in (0, len(observed_days) - 1):
            # DEC-E: giorno di bordo parziale -> escluso e contato nel report
            excluded_edge.append(coverage)
        else:
            # DEC-E: parzialita' interna -> anomalia riportata, giorno tenuto
            # in griglia sull'intervallo osservato (gestione decisa in M0-T2)
            internal_partial.append(coverage)
            grid_days.append(day)

    rows: list[tuple] = []
    for day in grid_days:
        day_minutes = sorted(dt for dt in reals if dt.date() == day)
        grid_start = max(datetime.combine(day, SESSION_START), day_minutes[0])
        last_session_minute = (
            datetime.combine(day, SESSION_END) - timedelta(minutes=1)
        )
        grid_end = min(last_session_minute, day_minutes[-1])

        prev_close: int | None = None
        current = grid_start
        while current <= grid_end:
            bar = reals.get(current)
            if bar is not None:
                o, h, l, c = bar.open, bar.high, bar.low, bar.close
                volume = bar.volume
                tick_count = bar.tick_count
                synthetic = False
                prev_close = bar.close
            else:
                # R-9.3: minuto no-trade -> O=H=L=C=Close precedente,
                # Volume=0, tick_count=0; R-9.14: bar_synthetic=True
                assert prev_close is not None  # garantito: griglia parte da barra reale
                o = h = l = c = prev_close
                volume = 0
                tick_count = 0
                synthetic = True
            rows.append(
                (
                    symbol,
                    timeframe,
                    current.strftime(_TS_FMT),
                    current.strftime(_DATE_FMT),
                    current.strftime(_TIME_FMT),
                    o,
                    h,
                    l,
                    c,
                    volume,
                    tick_count,
                    synthetic,
                    source,
                )
            )
            current += timedelta(minutes=1)

    frame = pd.DataFrame(rows, columns=CANONICAL_HEADER)
    for col in ("open", "high", "low", "close", "volume", "tick_count"):
        frame[col] = frame[col].astype("int64")
    frame["bar_synthetic"] = frame["bar_synthetic"].astype(bool)
    report = GridReport(
        excluded_edge_days=tuple(excluded_edge),
        internal_partial_days=tuple(internal_partial),
    )
    return GridResult(frame=frame, report=report)


def write_canonical_csv(frame: pd.DataFrame, path: str | Path) -> None:
    """Scrive il CSV canonico 13-campi in modo deterministico (newline fisso)."""
    frame.to_csv(path, index=False, lineterminator="\n", encoding="utf-8")
