"""Test M0-T1 (T1..T9) — loader fixture ISP -> griglia canonica 13-campi.

Card: Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_M0-T1_v2.md (SS3-SS4) +
ciclo di fix Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_M0-T1-FIX-01.md (SS1-SS2).
Fixture (GC-3): data/samples/portara_isp/ISP2023Z.txt (1000 righe, 9 colonne),
tracciata nel repo dal commit c78c358 "M0-T1-FIX: fixture ISP tracciata (GC-3)".

Requisiti-fonte citati (GC-2):
- R-9.3  docs/spec_funzionale/SPEC_FUNZ_01.md:1224 — griglia 1-min uniforme sessione
  08:00-22:00 CET, forward-fill minuti no-trade (O=H=L=C=Close prec., Volume=0, tick_count=0).
- R-9.14 docs/spec_funzionale/SPEC_FUNZ_01.md:1279 — semantica bar_synthetic:
  barra presente nel dato -> False, altrimenti True con forward-fill su Close.
- CN-9.5 docs/spec_funzionale/SPEC_FUNZ_01.md:1335 — header CSV a 13 campi esatti.
- CN-9.7 docs/spec_funzionale/SPEC_FUNZ_01.md:1341 — tick_count intero >=0 oppure NULL;
  bar_synthetic booleano True/False.
- CN-9.9 docs/spec_funzionale/SPEC_FUNZ_01.md:1347 — timestamp chiave normativa (SOB);
  date/time campi derivati.
- DEC-C / DEC-D: Codice/Piano_di_lavoro/DECISIONI.md — source=PORTARA, symbol=FIB,
  timeframe=token del decoder legacy ("60s",
  scripts/export_directa_history_parametric.py:797,802,885-887).
- DEC-E: Codice/Piano_di_lavoro/DECISIONI.md (commit 01c53aa) — giorni di bordo a
  copertura parziale ESCLUSI dalla griglia, con conteggio ed elenco nel report;
  parzialita' interne = anomalia da riportare (attese: 0 sul sample).

Costanti empiriche attese: PROVA-EMPIRICA 2026-07-05 sul sample tracciato in repo
(accertamento documentato in Codice/Piano_di_lavoro/Esito/ESITO_M0-T1.md, blocchi RM-1;
aggiornamento DEC-E in ESITO_M0-T1-FIX-01.md).
"""

import hashlib
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import pytest

from data_layer.isp_loader import (
    CANONICAL_HEADER,
    OffTick,
    build_canonical_grid,
    parse_isp_file,
    tick_grid_findings,
    write_canonical_csv,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE = REPO_ROOT / "data" / "samples" / "portara_isp" / "ISP2023Z.txt"
FIXTURE_TZ = "America/Chicago"  # PROVA-EMPIRICA 2026-07-05: vedi test T8 + ESITO_M0-T1.md

# Costanti empiriche del sample (PROVA-EMPIRICA 2026-07-05, ESITO_M0-T1.md + FIX-01)
N_RAW = 1000
N_SETTLE = 1
N_BARS = 999
COMPLETE_DAY = "2023-12-14"  # unica giornata con copertura sessione piena post-normalizzazione
N_REAL_COMPLETE_DAY = 745  # barre reali della giornata completa (sole barre in griglia, DEC-E)
N_SYNTH_COMPLETE_DAY = 95  # 840 - 745 minuti no-trade forward-fillati
# DEC-E: giorni di bordo esclusi attesi — (data CET, righe osservate = ampiezza
# copertura [prima reale, ultima reale] in minuti; card FIX-01 SS2: 262 e 65)
EXPECTED_EXCLUDED_EDGE_DAYS = [("2023-12-13", 262), ("2023-12-15", 65)]
EXPECTED_OFFTICKS = {
    OffTick(date="20231213", time="1038", field="high", value=30319),
    OffTick(date="20231214", time="1039", field="open", value=30389),
    OffTick(date="20231214", time="1039", field="high", value=30389),
}


@pytest.fixture(scope="module")
def parsed():
    return parse_isp_file(FIXTURE)


@pytest.fixture(scope="module")
def result(parsed):
    return build_canonical_grid(parsed.bars, tz=FIXTURE_TZ)


@pytest.fixture(scope="module")
def grid(result):
    return result.frame


@pytest.fixture(scope="module")
def report(result):
    return result.report


def test_t1_parser_legge_fixture_integrale_con_conteggi(parsed):
    """T1 — lettura integrale senza eccezioni; conteggi raw/settle/valide."""
    assert parsed.n_raw == N_RAW
    assert len(parsed.settle_rows) == N_SETTLE
    assert len(parsed.bars) == N_BARS
    assert parsed.n_raw == len(parsed.bars) + len(parsed.settle_rows)


def test_t2_zero_settle_row_nell_output(parsed, grid):
    """T2 — discriminante settle-row: volume == 0 (colonna 9 del sample).

    Prova empirica (RM-1, dettaglio nel blocco VERIFICA di ESITO_M0-T1.md):
    nel sample esiste esattamente 1 riga con volume==0; e' l'ultima riga del
    file, flat a 30434 (prezzo off-tick, non multiplo di 5), con orario 1038
    fuori sequenza rispetto al flusso 1-min della giornata. Alternative al
    discriminante (col8==0; barra flat; prezzo off-tick) escluse: contano
    rispettivamente 146, 319 (piu' la settle stessa) e 3 righe di barre
    regolari infra-sessione.
    """
    assert all(b.volume > 0 for b in parsed.bars)
    assert len(parsed.settle_rows) == 1
    settle = parsed.settle_rows[0]
    assert settle.volume == 0
    assert settle.date == "20231215"
    assert settle.time == "1038"
    assert settle.open == settle.high == settle.low == settle.close == 30434
    # nessuna settle-row raggiunge la griglia canonica: le sole righe a
    # volume 0 sono i minuti sintetici del forward-fill
    assert (grid["volume"] == 0).sum() == int(grid["bar_synthetic"].sum())


def test_t3_header_13_campi_tipi_e_valori_costanti(grid):
    """T3 — CN-9.5 header esatto; CN-9.7 tipi; CN-9.9 date/time derivati;
    DEC-C source=PORTARA; DEC-D symbol=FIB, timeframe=60s (token decoder legacy,
    scripts/export_directa_history_parametric.py:797,802,885-887)."""
    assert list(grid.columns) == CANONICAL_HEADER
    assert CANONICAL_HEADER == [
        "symbol", "timeframe", "timestamp", "date", "time",
        "open", "high", "low", "close", "volume",
        "tick_count", "bar_synthetic", "source",
    ]
    # CN-9.7: tick_count intero >= 0; bar_synthetic booleano
    assert pd.api.types.is_integer_dtype(grid["tick_count"])
    assert (grid["tick_count"] >= 0).all()
    assert pd.api.types.is_bool_dtype(grid["bar_synthetic"])
    for col in ("open", "high", "low", "close", "volume"):
        assert pd.api.types.is_integer_dtype(grid[col])
    # CN-9.9: timestamp chiave, date/time derivati coerenti
    assert (grid["timestamp"] == grid["date"] + " " + grid["time"]).all()
    # valori costanti da decreti
    assert (grid["source"] == "PORTARA").all()
    assert (grid["symbol"] == "FIB").all()
    assert (grid["timeframe"] == "60s").all()


def test_t4_giornata_completa_840_timestamp_monotoni_passo_60s(grid):
    """T4 — R-9.3: per la giornata completa 840 righe, 08:00-21:59 CET,
    passo 60s, zero buchi, zero duplicati, monotonia stretta."""
    day = grid[grid["date"] == COMPLETE_DAY]
    assert len(day) == 840
    ts = pd.to_datetime(day["timestamp"])
    assert ts.is_monotonic_increasing
    assert ts.is_unique
    deltas = ts.diff().dropna()
    assert (deltas == timedelta(seconds=60)).all()
    assert day["time"].iloc[0] == "08:00:00"
    assert day["time"].iloc[-1] == "21:59:00"
    # zero buchi: 840 minuti attesi = 840 osservati (giа garantito da passo+estremi)
    assert ts.iloc[-1] - ts.iloc[0] == timedelta(minutes=839)


def test_t5_forward_fill_minuti_no_trade_e_bar_synthetic(parsed, grid):
    """T5 — R-9.3 forward-fill: minuti no-trade O=H=L=C=Close precedente,
    volume=0, tick_count=0, bar_synthetic=True; R-9.14: barra presente nel
    sample -> bar_synthetic=False."""
    # mappa (date,time) raw -> barra, per il confronto delle barre reali
    raw_by_key = {(b.date, b.time): b for b in parsed.bars}

    prev_close = None
    prev_date = None
    n_synth = 0
    for row in grid.itertuples(index=False):
        if row.date != prev_date:
            prev_close = None
            prev_date = row.date
        if row.bar_synthetic:
            n_synth += 1
            assert prev_close is not None
            assert row.open == row.high == row.low == row.close == prev_close
            assert row.volume == 0
            assert row.tick_count == 0
        prev_close = row.close
    assert n_synth == int(grid["bar_synthetic"].sum())
    assert n_synth == N_SYNTH_COMPLETE_DAY  # 95 minuti no-trade nella giornata completa

    # ogni barra reale della griglia = barra del sample (OHLC+volume+tick_count)
    reali = grid[~grid["bar_synthetic"]]
    # DEC-E: in griglia restano le sole barre reali della giornata completa
    assert len(reali) == N_REAL_COMPLETE_DAY
    # confronto puntuale: ricostruisco la chiave raw dalla conversione tz
    # usata dal loader (stessa strada del modulo)
    from zoneinfo import ZoneInfo

    cet = ZoneInfo("Europe/Rome")
    src = ZoneInfo(FIXTURE_TZ)
    for row in reali.itertuples(index=False):
        cet_dt = datetime.strptime(row.timestamp, "%Y-%m-%d %H:%M:%S")
        raw_dt = cet_dt.replace(tzinfo=cet).astimezone(src)
        key = (raw_dt.strftime("%Y%m%d"), raw_dt.strftime("%H%M"))
        b = raw_by_key[key]
        assert (row.open, row.high, row.low, row.close) == (b.open, b.high, b.low, b.close)
        assert row.volume == b.volume
        assert row.tick_count == b.tick_count


def test_t6_determinismo_output_byte_identico(parsed, tmp_path):
    """T6 — due run indipendenti -> CSV byte-identico (hash sha256 uguale)."""
    hashes = []
    for i in (1, 2):
        p = parse_isp_file(FIXTURE)
        res = build_canonical_grid(p.bars, tz=FIXTURE_TZ)
        out = tmp_path / f"run{i}.csv"
        write_canonical_csv(res.frame, out)
        hashes.append(hashlib.sha256(out.read_bytes()).hexdigest())
    assert hashes[0] == hashes[1]


def test_t7_diagnostica_tick_grid_rileva_30319_senza_alterare(parsed, grid, report):
    """T7 — diagnostica off-tick: rileva il noto 30319, elenca ogni altro
    off-tick, nessun clamping/drop (le barre restano intatte)."""
    findings = tick_grid_findings(parsed.bars)
    values = {f.value for f in findings}
    assert 30319 in values
    # elenco esaustivo degli off-tick delle barre valide del sample
    assert set(findings) == EXPECTED_OFFTICKS
    # nessuna alterazione: la barra col 30389 (giornata completa) e' in griglia
    # con open/high intatti
    hit = grid[(grid["high"] == 30389) & (~grid["bar_synthetic"])]
    assert len(hit) == 1
    assert hit["open"].iloc[0] == 30389
    # la barra col 30319 appartiene a un giorno di bordo escluso (DEC-E):
    # non alterata ne' scartata in silenzio — il giorno e' elencato nel report
    assert "2023-12-13" in {d.date for d in report.excluded_edge_days}
    # nessun drop dentro la giornata completa: conteggio barre reali atteso
    assert len(grid[~grid["bar_synthetic"]]) == N_REAL_COMPLETE_DAY


def test_t8_timezone_prima_ultima_barra_reale_per_giornata(parsed, grid, report, capsys):
    """T8 — coerenza tz: con tz=America/Chicago la giornata completa copre
    esattamente la sessione 08:00-21:59 CET (R-9.3). Stampa prima/ultima
    barra reale per giornata (griglia + giorni di bordo esclusi dal report)."""
    reali = grid[~grid["bar_synthetic"]]
    for day, sub in reali.groupby("date"):
        print(f"{day}: prima barra reale {sub['time'].iloc[0]} "
              f"ultima barra reale {sub['time'].iloc[-1]} (CET)")
    for d in report.excluded_edge_days:
        print(f"{d.date}: prima barra reale {d.first_time} "
              f"ultima barra reale {d.last_time} (CET) — bordo escluso, DEC-E")
    day = reali[reali["date"] == COMPLETE_DAY]
    # 0100 America/Chicago (CST, UTC-6) == 08:00 CET; 1459 == 21:59 CET
    assert day["time"].iloc[0] == "08:00:00"
    assert day["time"].iloc[-1] == "21:59:00"
    # tutte le barre reali in griglia cadono nella finestra di sessione
    assert (reali["time"] >= "08:00:00").all()
    assert (reali["time"] <= "21:59:00").all()
    # coerenza tz anche sui bordi esclusi (copertura entro la sessione CET)
    assert report.excluded_edge_days[0].first_time == "17:38:00"
    assert report.excluded_edge_days[0].last_time == "21:59:00"
    assert report.excluded_edge_days[1].first_time == "08:00:00"
    assert report.excluded_edge_days[1].last_time == "09:04:00"


def test_t9_dec_e_giorni_bordo_esclusi_e_contati(grid, report):
    """T9 — pinna DEC-E (Codice/Piano_di_lavoro/DECISIONI.md, commit 01c53aa):
    output della fixture = sole giornate complete (840 righe, tutte del
    14/12/2023); report con i 2 giorni di bordo esclusi (262 e 65 righe
    osservate); zero parzialita' interne."""
    assert len(grid) == 840
    assert set(grid["date"]) == {COMPLETE_DAY}
    assert [(d.date, d.rows_observed) for d in report.excluded_edge_days] == (
        EXPECTED_EXCLUDED_EDGE_DAYS
    )
    # barre reali osservate nei giorni esclusi (trasparenza, mai scarto
    # silenzioso): 211 (13/12) e 43 (15/12: 44 righe raw meno la settle-row)
    assert [d.real_bars for d in report.excluded_edge_days] == [211, 43]
    # parzialita' interne: anomalia da riportare — attese 0 sul sample
    assert report.internal_partial_days == ()
