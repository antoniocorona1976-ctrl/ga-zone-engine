# ESITO_M0-T1-FIX-01 — chiusura findings review (#1 + DEC-E)

**Data/ora**: 2026-07-05 03:55 CET
**Verdetto**: COMPLETATO
**Esecutore**: `prog_developer` (card `Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_M0-T1-FIX-01.md`, eseguita §0..§5; instradamento AC su REVIEW_M0-T1 `225057d`: #1 qui, #5 chiuso con DEC-E, #4 → M0-T2, #2/#3/#6 ignorati)

---

## 1. Precondizioni (§0) e DEC-E (§0-bis)

- §0: **PASSATE** (contesto autoritativo dell'Orchestratore) — `225057d` (REVIEW M0-T1) in history e pushato, branch in pari; ultimo stato `tasks/DEV_STATUS.md` = `REVIEW M0-T1: CONDITIONAL — 2026-07-05`. Riscontro locale: `git log --oneline -4` = `01c53aa`, `225057d`, `101335e`, `d701918`; `tail -3 tasks/DEV_STATUS.md` conferma la riga CONDITIONAL.
- §0-bis: **GIÀ ESEGUITO dall'Orchestratore** — DEC-E registrato in `Codice/Piano_di_lavoro/DECISIONI.md`, **commit `01c53aa`**, pushato. `DECISIONI.md` non toccato da questa esecuzione.

## 2. Fix #1 — fixture tracciata (GC-3)

- **Commit `c78c358`** `M0-T1-FIX: fixture ISP tracciata (GC-3)` — add esplicito del solo `data/samples/portara_isp/ISP2023Z.txt` (staging controllato prima del commit: unica voce), 1000 inserzioni. Pushato (`01c53aa..c78c358`).
- Da questo commit la fixture è nel repo: la suite gira su qualunque clone senza dati esterni (GC-3, `tasks/METODO.md:305-309`); prova su worktree pulito in §6 (appendice).

### Diff docstring (claim falsi → stato reale)

| File:riga (pre-fix) | Prima | Dopo |
|---|---|---|
| `src/data_layer/isp_loader.py:4` | `Fixture: data/samples/portara_isp/ISP2023Z.txt (committata, GC-3).` | `Fixture (GC-3): data/samples/portara_isp/ISP2023Z.txt, tracciata nel repo dal commit c78c358 "M0-T1-FIX: fixture ISP tracciata (GC-3)".` |
| `src/data_layer/isp_loader.py:37-43` | paragrafo "Politica giornate troncate (decisione di modulo...)" | paragrafo "Politica giorni parziali — DEC-E (commit 01c53aa)": bordi parziali esclusi + report; interne = anomalia riportata; sessioni corte da calendario → M0-T2 |
| `src/data_layer/isp_loader.py:215-216` | commento `nel sample committato non accade` | `sul sample tracciato non accade ... contatore diagnostico rinviato a M0-T2 (review M0-T1, finding #4)` (nessuna logica toccata: #4 fuori scope) |
| `tests/data_layer/test_isp_loader.py:1,4` | `Test M0-T1 (T1..T8)...` / `Fixture committata (GC-3): ...` | `Test M0-T1 (T1..T9)...` / `Fixture (GC-3): ..., tracciata nel repo dal commit c78c358 ...` |
| `tests/data_layer/test_isp_loader.py:20` | `PROVA-EMPIRICA 2026-07-05 sul sample committato` | `PROVA-EMPIRICA 2026-07-05 sul sample tracciato in repo` |
| `src/data_layer/__init__.py:3` | `loader del sample ISP (fixture committata)` | `loader del sample ISP (fixture data/samples/portara_isp/ISP2023Z.txt, tracciata nel repo dal commit c78c358)` |

Nota: il claim analogo in `tasks/ACTIVE_TASK.md` (segnalato dalla review al finding #1) diventa vero col commit `c78c358`; il file non è nell'elenco dei toccabili di questa card (§3) e non è stato modificato.

## 3. DEC-E implementato + T9 (chiude finding #5)

- `build_canonical_grid` ora restituisce `GridResult` (`frame` + `report`):
  - giorni di **bordo** (primo/ultimo osservato) a copertura parziale → **esclusi** dalla griglia ed elencati in `report.excluded_edge_days` (`PartialDay`: data CET, `rows_observed` = ampiezza copertura [prima reale, ultima reale] in minuti, `real_bars`, prima/ultima barra reale) — mai scarto silenzioso;
  - parzialità nei giorni **interni** → `report.internal_partial_days` (anomalia riportata; il giorno resta in griglia sull'intervallo osservato; gestione decisa in M0-T2, come da DEC-E);
  - giorno completo = prima barra reale alle 08:00 CET E ultima alle 21:59 CET (finestra R-9.3, `docs/spec_funzionale/SPEC_FUNZ_01.md:1224`).
- **Report DEC-E sul sample** (output reale del loader):

```
escluso: PartialDay(date='2023-12-13', rows_observed=262, real_bars=211, first_time='17:38:00', last_time='21:59:00')
escluso: PartialDay(date='2023-12-15', rows_observed=65, real_bars=43, first_time='08:00:00', last_time='09:04:00')
parzialita interne: ()
```

  Attesi dalla card §2: 2 giorni, 262 e 65 — riscontrati. `rows_observed` = righe che la copertura osservata avrebbe prodotto in griglia (262 = 17:38–21:59; 65 = 08:00–09:04), coerente con i numeri del reviewer (1167 = 262 + 840 + 65). `real_bars`: 211 e 43 (le 44 righe raw del 15/12 comprendono la settle-row, filtrata a monte: 211+745+43 = 999).
- **T9** pinna DEC-E: griglia = 840 righe, tutte del 2023-12-14; esclusi = `[("2023-12-13", 262), ("2023-12-15", 65)]`; `real_bars` = `[211, 43]`; parzialità interne = 0.

## 4. Tabella asserzioni vecchio → nuovo

| Test | Vecchio | Nuovo | Motivo |
|---|---|---|---|
| fixture pytest `grid` | `build_canonical_grid(...)` → `DataFrame` | fixture `result` (`GridResult`) + `grid` (`result.frame`) + `report` (`result.report`) | nuova API con report DEC-E |
| T2 | ricostruiva la griglia in-test (`g = build_canonical_grid(...)`) | usa la fixture `grid`; asserzione `volume==0 ⇔ bar_synthetic` invariata | adattamento API, nessun cambio di sostanza |
| T5 | `len(reali) == len(parsed.bars)` (999); `n_synth > 0` (168 di fatto) | `len(reali) == 745`; `n_synth == 95` | DEC-E: in griglia restano le sole barre della giornata completa (745 reali + 95 sintetiche = 840) |
| T6 | hash su CSV a 1167 righe (sha256 `1267cb3a…`, riprodotto dal reviewer) | stessa logica, CSV a 840 righe (sha256 `c1d9a8287c111f0b17cf9e38e108d011480490ef01461682ef6e29973bcdb8db`), `res.frame` | DEC-E cambia il contenuto deterministico; doppio run rieseguito byte-identico |
| T7 | barra intatta pinnata su `high==30319`; reali `== 999` | barra intatta pinnata su `open/high==30389` (14/12, in griglia); il 30319 (13/12) resta nei finding della diagnostica (su barre raw valide, invariata) e il suo giorno è nel report esclusi; reali `== 745` | il giorno del 30319 è un bordo escluso da DEC-E: non alterato, escluso con report |
| T8 | stampava 3 giornate dalla griglia | stampa la giornata in griglia + i 2 bordi esclusi dal report; aggiunti assert su coperture dei bordi (17:38–21:59, 08:00–09:04) | la prova tz sui bordi ora passa dal report |
| T9 | — (non esisteva) | nuovo: pinna DEC-E (840/2023-12-14; esclusi 262+65; interne 0) | card FIX-01 §2 |
| T1, T3, T4 | — | invariati (T4 già sulla sola giornata completa) | nessun impatto DEC-E |

Correzione in corso d'opera (trasparenza TDD): la prima stesura di T9 attendeva `real_bars` 15/12 = 44 (conteggio righe raw della giornata); run rosso → corretto a 43 (44 raw − 1 settle-row). L'errore era nella costante attesa del test, non nel modulo.

## 5. Output pytest ×2 (suite completa T1–T9, forma finale)

Run 1 — `python -m pytest tests/data_layer/ -v`:

```
============================= test session starts =============================
platform win32 -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\AN\miniconda3\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\AN\Documents\Projects\ga-zone-engine
plugins: anyio-4.12.1
collecting ... collected 9 items

tests/data_layer/test_isp_loader.py::test_t1_parser_legge_fixture_integrale_con_conteggi PASSED [ 11%]
tests/data_layer/test_isp_loader.py::test_t2_zero_settle_row_nell_output PASSED [ 22%]
tests/data_layer/test_isp_loader.py::test_t3_header_13_campi_tipi_e_valori_costanti PASSED [ 33%]
tests/data_layer/test_isp_loader.py::test_t4_giornata_completa_840_timestamp_monotoni_passo_60s PASSED [ 44%]
tests/data_layer/test_isp_loader.py::test_t5_forward_fill_minuti_no_trade_e_bar_synthetic PASSED [ 55%]
tests/data_layer/test_isp_loader.py::test_t6_determinismo_output_byte_identico PASSED [ 66%]
tests/data_layer/test_isp_loader.py::test_t7_diagnostica_tick_grid_rileva_30319_senza_alterare PASSED [ 77%]
tests/data_layer/test_isp_loader.py::test_t8_timezone_prima_ultima_barra_reale_per_giornata PASSED [ 88%]
tests/data_layer/test_isp_loader.py::test_t9_dec_e_giorni_bordo_esclusi_e_contati PASSED [100%]

============================== 9 passed in 1.11s ==============================
```

Run 2 — `python -m pytest tests/data_layer/ -q`:

```
.........                                                                [100%]
9 passed in 1.06s
```

Stampa T8 (`pytest -s`):

```
2023-12-14: prima barra reale 08:00:00 ultima barra reale 21:59:00 (CET)
2023-12-13: prima barra reale 17:38:00 ultima barra reale 21:59:00 (CET) — bordo escluso, DEC-E
2023-12-15: prima barra reale 08:00:00 ultima barra reale 09:04:00 (CET) — bordo escluso, DEC-E
```

## 6. Hash commit, prova GC-3 (worktree), stato finale

- Commit DEC-E (§0-bis, Orchestratore): **`01c53aa`**, pushato.
- Commit fixture (§1): **`c78c358`**, pushato.
- Commit fix finale (§4): messaggio esatto `M0-T1-FIX-01: GC-3 fixture + DEC-E giorni di bordo + T9 - suite verde su worktree pulito`; add espliciti di `src/data_layer/`, `tests/data_layer/`, card FIX-01, questo ESITO, `tasks/DEV_STATUS.md` (append `FIX M0-T1: READY_FOR_RE-REVIEW — 2026-07-05`, nessuna riga preesistente riscritta). L'hash non può stare nel commit che introduce questo file: è registrato nell'appendice §7 (commit di chiusura dedicato), insieme alla prova GC-3 su worktree (che deve girare su HEAD con la suite in forma finale, quindi dopo il commit).

## 7. Appendice di chiusura (post-commit) — hash finale + prova GC-3 integrale

- **Hash commit fix finale**: **`e656315`** — 6 file, 348 inserzioni / 46 rimozioni (i soli file della add-list §4). Push eseguito: `c78c358..e656315 main -> main`.
- **Prova GC-3 su worktree pulito** (card §1.3) — comando di creazione:
  `git worktree add "C:\Users\AN\AppData\Local\Temp\claude\C--Users-AN-Documents-Projects-ga-zone-engine\2eeaf63e-745e-4032-a8bd-907c1fda672c\scratchpad\wt_m0t1fix" HEAD`
  (worktree da HEAD = `e656315`, detached: contiene i SOLI file tracciati — suite in forma finale, T1..T9). Esecuzione nel worktree: `python -m pytest tests/data_layer/ -v`. Output integrale:

```
platform win32 -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\AN\miniconda3\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\AN\AppData\Local\Temp\claude\C--Users-AN-Documents-Projects-ga-zone-engine\2eeaf63e-745e-4032-a8bd-907c1fda672c\scratchpad\wt_m0t1fix
plugins: anyio-4.12.1
collecting ... collected 9 items

tests/data_layer/test_isp_loader.py::test_t1_parser_legge_fixture_integrale_con_conteggi PASSED [ 11%]
tests/data_layer/test_isp_loader.py::test_t2_zero_settle_row_nell_output PASSED [ 22%]
tests/data_layer/test_isp_loader.py::test_t3_header_13_campi_tipi_e_valori_costanti PASSED [ 33%]
tests/data_layer/test_isp_loader.py::test_t4_giornata_completa_840_timestamp_monotoni_passo_60s PASSED [ 44%]
tests/data_layer/test_isp_loader.py::test_t5_forward_fill_minuti_no_trade_e_bar_synthetic PASSED [ 55%]
tests/data_layer/test_isp_loader.py::test_t6_determinismo_output_byte_identico PASSED [ 66%]
tests/data_layer/test_isp_loader.py::test_t7_diagnostica_tick_grid_rileva_30319_senza_alterare PASSED [ 77%]
tests/data_layer/test_isp_loader.py::test_t8_timezone_prima_ultima_barra_reale_per_giornata PASSED [ 88%]
tests/data_layer/test_isp_loader.py::test_t9_dec_e_giorni_bordo_esclusi_e_contati PASSED [100%]

============================== 9 passed in 1.16s ==============================
```

  **9/9 PASSED su soli file tracciati** (GC-3 dimostrata: la fixture arriva dal commit `c78c358`, nessun dato esterno). Worktree rimosso a fine prova (`git worktree remove ...`; `git worktree list` → solo il repo principale).
- **`git status --short` finale**: zero modifiche su file tracciati (`git status --short | grep -v "^??"` → vuoto, prima di questo commit di chiusura); `git status` = `Your branch is up to date with 'origin/main'`. Restano le voci untracked `??` preesistenti al task (noise di progetto), non toccate — la fixture e `ISTRUZIONI_M0-T1-FIX-01.md` non ne fanno più parte (ora tracciate).
- Questo aggiornamento (sezione 7) è il commit di chiusura dedicato al solo `ESITO_M0-T1-FIX-01.md` (stesso schema della deviazione D1 già classificata NEUTRO in review: l'hash del commit non può vivere dentro il commit stesso; la suite non è toccata, la prova GC-3 resta valida su `e656315`).
