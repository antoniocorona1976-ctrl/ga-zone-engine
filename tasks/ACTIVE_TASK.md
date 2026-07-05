# TASK ATTIVO: M0-T1 — loader fixture ISP → griglia canonica 13-campi

> **Track**: FASE-CODICE (GOV-CODICE-01, `tasks/METODO.md:281-317`). **Sede**: CLI.
> **Card autoritativa**: `Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_M0-T1_v2.md` (sostituisce integralmente la v1).
> **Ruolo esecutore**: `prog_developer` (`.claude/agents/prog_developer.md`).

## Sintesi scope (fa fede la card)

- Parser del sample committato `data/samples/portara_isp/ISP2023Z.txt` (9 colonne) → barre 1-min, settle-row filtrate (discriminante `volume == 0`).
- Grid builder → griglia canonica sessione 08:00–22:00 CET (R-9.3, `docs/spec_funzionale/SPEC_FUNZ_01.md:1224`), 840 righe/giornata completa, passo 60s, `timestamp` start-of-bar chiave (CN-9.9, `:1347`), forward-fill minuti no-trade con `bar_synthetic=True` (R-9.14, `:1279`).
- Output CSV header 13 campi esatti (CN-9.5, `:1335`), tipi CN-9.7 (`:1341`); `source=PORTARA` (DEC-C), `symbol=FIB`, `timeframe=60s` (DEC-D, token decoder legacy `scripts/export_directa_history_parametric.py:797,802,885-887`).
- Diagnostica tick-grid: off-tick rilevati e loggati come finding (incluso il noto `30319`), nessun clamping, nessun drop.
- Done-when: test T1..T8 della card verdi con pytest su fixture committata (GC-3).

## Layout

- Codice: `src/data_layer/` — Test: `tests/data_layer/` — Esito: `Codice/Piano_di_lavoro/Esito/ESITO_M0-T1.md`.

## Decreti applicati (registrati in commit 55dc943, NON riaprire)

- DEC-C: `source = PORTARA` per tutte le barre del dataset training M0 (reali e sintetiche).
- DEC-D: `symbol = FIB`; `timeframe` = token della convenzione del decoder legacy (`60s`), fallback `1min` non necessario.
