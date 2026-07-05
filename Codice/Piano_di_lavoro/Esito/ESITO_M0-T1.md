# ESITO_M0-T1 — loader fixture ISP → griglia canonica 13-campi

**Data/ora**: 2026-07-05 03:08 CET
**Verdetto**: COMPLETATO
**Esecutore**: `prog_developer` (card `Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_M0-T1_v2.md`, eseguita §1..§7)

---

## 1. Precondizioni (§0) e decreti (§0-bis)

- Precondizioni §0: **PASSATE** — accertate dall'Orchestratore (input autoritativo del prompt di invocazione): commit `774f9d3` / `4b877db` / `bb8d625` in history e pushati; slot libero; fixture `data/samples/portara_isp/ISP2023Z.txt` presente (52.499 byte). Riscontro locale: `git log --oneline -3` mostra `55dc943`, `774f9d3`, `4b877db` in testa; `ls -la data/samples/portara_isp/` mostra `ISP2023Z.txt` 52499 byte.
- §0-bis: **GIÀ ESEGUITO dall'Orchestratore** — DEC-C (`source=PORTARA`) e DEC-D (`symbol=FIB`; `timeframe` = token decoder legacy) registrati in `Codice/Piano_di_lavoro/DECISIONI.md`; chiusura v1.1 in `tasks/STATO_CORRENTE.md`. **Commit `55dc943`**, pushato. `DECISIONI.md` e `STATO_CORRENTE.md` non toccati da questa esecuzione.

## 2. Letture-fonte eseguite (GC-4 — range mirati, nessun dump integrale)

| Fonte | Righe lette | Motivo |
|---|---|---|
| `docs/spec_funzionale/SPEC_FUNZ_01.md` | 1218-1232 (R-9.1..R-9.4), 1275-1284 (R-9.13..R-9.15), 1330-1352 (CN-9.5..CN-9.9) | requisiti contratto del task (griglia, sinteticità, header, tipi, chiave timestamp, dominio source) |
| `scripts/export_directa_history_parametric.py` | 96-130, 598-642, 793-812, 880-889 (+ grep `timeframe/1M/period_seconds`) | convenzioni legacy: token timeframe, formati timestamp/date/time, header 11-campi |
| `Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_M0-T1_v2.md` | 1-80 (integrale — è la card, lettura integrale richiesta) | specifica del task |
| `Codice/PROMPT_RECUPERO_SAMPLE_ISP.md` | riga 6, 12-14 (via grep) | fatti interni sul sample (tz Chicago, penultima colonna = tickCount) |
| `tasks/METODO.md`, `.claude/BASE_COMUNE.md`, `.claude/agents/prog_developer.md` | integrali | letture obbligatorie di ruolo (normativa, non spec) |

RM-2 (grep decoder esistenti prima di assumere il formato): eseguito `grep -i "ISP2023Z|portara_isp|PORTARA"` su tutto il repo → **nessun parser/decoder esistente per il formato sample 9-colonne** (solo documenti di piano/istruzioni e il prompt di recupero); eseguito grep su `export_directa_history_parametric.py` per le convenzioni legacy (citazioni sotto, ricontrollate con Read).

## 3. Mappatura colonne del sample (PROVA-EMPIRICA 2026-07-05)

Sample: 1000 righe, tutte a 9 colonne, simbolo unico `ISP2023Z`, date 20231213/14/15.

**Mappatura accertata**: `col1=symbol, col2=date YYYYMMDD, col3=time HHMM (start-of-bar), col4=open, col5=high, col6=low, col7=close, col8=tick_count, col9=volume`.

```
VERIFICA: ordine colonne prezzi = O(col4), H(col5), L(col6), C(col7)
PROVE: test esaustivo delle 24 permutazioni (O,H,L,C) su col4..7 contro il vincolo
  H=max e L=min su tutte le 1000 righe: sole 2 permutazioni compatibili,
  (O,H,L,C) e (C,H,L,O). Disambiguazione O vs C con la continuità inter-barra
  intra-giornata: media |O_t − C_(t−1)| = 3.72 punti per (O,H,L,C) contro
  10.17 punti per (C,H,L,O) (fattore 2.7). Hint concordante di livello 4:
  convenzione OHLC dell'ASCII Portara [WIKI-HINT, non determinante].
ALTERNATIVE COMPATIBILI ESCLUSE: le 22 permutazioni con H o L fuori posizione
  (almeno 1 riga incompatibile ciascuna); (C,H,L,O) esclusa su base statistica
  dalla continuità inter-barra (metrica 2.7x peggiore su 997 coppie consecutive).
ALTERNATIVE COMPATIBILI NON ESCLUSE: nessuna con prova a vincolo rigido —
  l'esclusione di (C,H,L,O) è statistica (forte) e non tick-by-tick; sul tape
  pagato M0-T2 la si può riconfermare col roll-log/contract data del vendor.
```

```
VERIFICA: col8 = tick_count, col9 = volume
PROVE: (i) [DOC-INTERNO Codice/PROMPT_RECUPERO_SAMPLE_ISP.md:6] "penultima
  colonna = tickCount"; (ii) col8 ≤ col9 su 999/1000 righe — sotto la mappatura
  inversa (col8=volume) la riga 1 avrebbe volume=6 con 48 trade, impossibile in
  un mercato a lotti interi (ogni trade ≥ 1 lotto ⇒ volume ≥ n. trade);
  (iii) le 146 righe con col8=0 sono tutte barre flat infra-sessione con
  col9>0 (coerente con tickCount = variazioni di prezzo, incoerente con
  volume=0 su 146 minuti sparsi); (iv) l'unica riga con col9=0 è la settle-row
  (vedi blocco successivo).
ALTERNATIVE COMPATIBILI ESCLUSE: col8=volume/col9=tickCount (esclusa da (ii));
  col8 o col9 = open interest su file a 9 colonne (esclusa da (i) + dal
  comportamento (iii)-(iv): un OI non sarebbe ≤ dell'altra colonna su 999/1000
  righe né nullo solo sulla settle-row).
ALTERNATIVE COMPATIBILI NON ESCLUSE: la semantica fine di tickCount (n. trade
  vs n. variazioni di prezzo) non è discriminata dal sample; non impatta M0-T1
  (la colonna è propagata as-is). Da chiarire su documentazione tape M0-T2.
```

## 4. Discriminante settle-row (PROVA-EMPIRICA 2026-07-05)

```
VERIFICA: la settle-row si discrimina con volume == 0 (col9), come atteso dalla card (§3.1)
PROVE: nel sample esiste esattamente 1 riga con col9=0:
  `ISP2023Z,20231215,1038,30434,30434,30434,30434,1,0` — è l'ULTIMA riga del
  file, flat sui 4 prezzi, prezzo 30434 off-tick (non multiplo di 5, tipico
  prezzo di settlement), orario 1038 fuori sequenza rispetto al flusso 1-min
  della giornata (che termina a 0204). Quattro segnali concordanti.
ALTERNATIVE COMPATIBILI ESCLUSE: discriminante col8==0 (146 righe regolari
  infra-sessione, con volume>0 — non settle); discriminante "barra flat"
  (320 righe regolari); discriminante "prezzo off-tick" (presente anche in
  2 barre negoziate, es. high=30319 con volume 48).
ALTERNATIVE COMPATIBILI NON ESCLUSE: sul tape pagato il vendor potrebbe emettere
  anche righe no-trade legittime con volume=0 (non osservabili in questo sample):
  il discriminante volume==0 da solo andrà riconfermato in M0-T2 (eventualmente
  raffinato con flat+fuori-sequenza).
```

Il parser filtra la settle-row prima della griglia: T2 controlla che zero righe a volume 0 raggiungano l'output e che tutte le barre a volume 0 in griglia siano le sole sintetiche.

## 5. Timezone accertato (PROVA-EMPIRICA 2026-07-05)

```
VERIFICA: timestamp nativi del sample in ora di Chicago (America/Chicago); con
  tz=America/Chicago la giornata piena si normalizza esattamente alla sessione
  FIB 08:00–21:59 CET (R-9.3)
PROVE: prima/ultima barra reale per giornata (nativo → CET con America/Chicago,
  CST=UTC-6 a dicembre):
    20231213: 1038 → 17:38  |  1459 → 21:59   (giornata iniziale troncata)
    20231214: 0100 → 08:00  |  1459 → 21:59   (giornata piena: 745 barre reali)
    20231215: 0100 → 08:00  |  0204 → 09:04   (giornata finale troncata)
  La finestra nativa 0100–1459 combacia al minuto con la sessione 08:00–21:59
  CET della spec (R-9.3, docs/spec_funzionale/SPEC_FUNZ_01.md:1224).
  Concordante: [DOC-INTERNO Codice/PROMPT_RECUPERO_SAMPLE_ISP.md:6] "dati in
  ora di Chicago".
ALTERNATIVE COMPATIBILI ESCLUSE: tz nativo CET (sessione risulterebbe
  01:00–14:59, priva di senso per il FIB); UTC (02:00–15:59 CET); America/
  New_York (07:00–20:59 CET, disallineata di 1h dalla finestra R-9.3).
ALTERNATIVE COMPATIBILI NON ESCLUSE: nessuna fra i tz plausibili di un vendor
  CQG per la finestra osservata.
```

```
VERIFICA: convenzione temporale del sample = start-of-bar (SOB), coerente con CN-9.9
PROVE: la giornata piena espone gli stamp 0100..1459; sotto la convenzione
  end-of-bar gli stamp sarebbero 0101..1500. La presenza dello stamp 0100 e
  l'assenza dello stamp 1500 (su 745 barre reali) seleziona SOB.
ALTERNATIVE COMPATIBILI ESCLUSE: end-of-bar (esclusa dagli estremi osservati).
ALTERNATIVE COMPATIBILI NON ESCLUSE: nessuna.
```

Il loader prende `tz` come **parametro esplicito** (`build_canonical_grid(..., tz=...)`) e normalizza sempre a CET (zona IANA `Europe/Rome`), come da card §3.1. I test passano `tz="America/Chicago"`.

## 6. Token `timeframe` (DEC-D) — citazione decoder legacy

- **Token adottato: `60s`** (esiste token univoco: il fallback `1min` della card non è necessario).
- [CODICE-ESISTENTE scripts/export_directa_history_parametric.py:797] `base_tf = f"{fallback_period_seconds}s"`, usato come valore del campo `timeframe` a r.802 (`timeframe=base_tf`), con `fallback_period_seconds=60` in tutte le chiamate (r.885-887) → per le barre a 60 secondi il decoder legacy scrive `timeframe="60s"`. Citazioni ricontrollate con Read.
- Concordante col contratto: il dominio `source` di CN-9.8 contiene `AGG_FROM_60s` (docs/spec_funzionale/SPEC_FUNZ_01.md:1344), generato dal decoder come `f"AGG_FROM_{base_tf}"` (r.817-827) — lo stesso token `60s`.
- Nota: la docstring del decoder (r.25) menziona "1M" in prosa, ma nessun record dati usa "1M" come valore di `timeframe`: il token effettivo scritto nei CSV legacy è `60s`.

## 7. Implementazione consegnata

| File | Contenuto |
|---|---|
| `src/data_layer/__init__.py` | export API del modulo |
| `src/data_layer/isp_loader.py` | `parse_isp_file` (parser 9-col + filtro settle), `build_canonical_grid` (griglia CN-9.5 con forward-fill R-9.3/R-9.14, tz param → CET), `tick_grid_findings` (diagnostica off-tick, nessun clamping/drop), `write_canonical_csv` (CSV deterministico) |
| `tests/data_layer/conftest.py` | `src/` importabile senza installazione (suite autosufficiente, GC-3) |
| `tests/data_layer/test_isp_loader.py` | test T1..T8 della card |

Requisiti implementati, con fonte (GC-2): R-9.3 `docs/spec_funzionale/SPEC_FUNZ_01.md:1224`; R-9.14 `:1279`; CN-9.5 `:1335`; CN-9.7 `:1341`; CN-9.9 `:1347`; DEC-C/DEC-D `Codice/Piano_di_lavoro/DECISIONI.md` (commit 55dc943). Formati `timestamp/date/time` mutuati dal decoder legacy [CODICE-ESISTENTE scripts/export_directa_history_parametric.py:65,67,116-118].

**Decisione di modulo documentata (giornate troncate del sample)**: la griglia di ogni giornata copre `[max(08:00 CET, prima barra reale), min(21:59 CET, ultima barra reale)]`. Su giornata a copertura piena coincide con l'intera finestra R-9.3 (840 minuti — è il caso T4). Razionale: i minuti a monte della prima barra reale non hanno un Close precedente da propagare; i minuti a valle dell'ultima barra reale di una giornata troncata sono un artefatto di taglio del sample (1000 righe), non minuti no-trade — riempirli spaccerebbe la troncatura per assenza di scambi. Da riesaminare sul tape pieno in M0-T2.

## 8. Output pytest integrale (T1–T8)

Comando: `python -m pytest tests/data_layer/ -v` (Python 3.13.13, pytest 9.1.1, pandas 3.0.3, numpy 2.5.1 — installati in questa esecuzione, ammessi da card §2).

```
============================= test session starts =============================
platform win32 -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\AN\miniconda3\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\AN\Documents\Projects\ga-zone-engine
plugins: anyio-4.12.1
collecting ... collected 8 items

tests/data_layer/test_isp_loader.py::test_t1_parser_legge_fixture_integrale_con_conteggi PASSED [ 12%]
tests/data_layer/test_isp_loader.py::test_t2_zero_settle_row_nell_output PASSED [ 25%]
tests/data_layer/test_isp_loader.py::test_t3_header_13_campi_tipi_e_valori_costanti PASSED [ 37%]
tests/data_layer/test_isp_loader.py::test_t4_giornata_completa_840_timestamp_monotoni_passo_60s PASSED [ 50%]
tests/data_layer/test_isp_loader.py::test_t5_forward_fill_minuti_no_trade_e_bar_synthetic PASSED [ 62%]
tests/data_layer/test_isp_loader.py::test_t6_determinismo_output_byte_identico PASSED [ 75%]
tests/data_layer/test_isp_loader.py::test_t7_diagnostica_tick_grid_rileva_30319_senza_alterare PASSED [ 87%]
tests/data_layer/test_isp_loader.py::test_t8_timezone_prima_ultima_barra_reale_per_giornata PASSED [100%]

============================== 8 passed in 1.81s ==============================
```

TDD rispettato: primo run (test scritti, modulo assente) → `ModuleNotFoundError: No module named 'data_layer'`, 1 errore di collection; poi implementazione → 8/8 PASSED.

Stampa T8 (prima/ultima barra reale per giornata, `pytest -s`):

```
2023-12-13: prima barra reale 17:38:00 ultima barra reale 21:59:00 (CET)
2023-12-14: prima barra reale 08:00:00 ultima barra reale 21:59:00 (CET)
2023-12-15: prima barra reale 08:00:00 ultima barra reale 09:04:00 (CET)
```

## 9. Conteggi

| Grandezza | Valore |
|---|---|
| Righe raw lette | 1000 |
| Settle-row filtrate | 1 |
| Barre valide | 999 |
| Righe griglia canonica totali | 1167 |
| — di cui reali (`bar_synthetic=False`) | 999 |
| — di cui sintetiche (`bar_synthetic=True`) | 168 |
| Righe per giornata (CET) | 2023-12-13: 262 · 2023-12-14: **840** · 2023-12-15: 65 |
| Barre fuori sessione 08:00–22:00 CET | 0 |

## 10. Finding tick-grid (diagnostica, nessun clamping/nessun drop)

Off-tick sulle barre valide (prezzo non multiplo di 5):

| date | time (nativo) | campo | valore |
|---|---|---|---|
| 20231213 | 1038 | high | **30319** (il noto, card §3.6) |
| 20231214 | 1039 | open | 30389 |
| 20231214 | 1039 | high | 30389 |

Le barre restano intatte in griglia (T7 controlla `high==30319` presente e conteggio barre reali invariato). Nota: anche la settle-row filtrata è interamente off-tick (30434 sui 4 campi) — ulteriore segnale concordante della sua natura di settlement, non entra nei finding delle barre valide.

## 11. Commit, push, stato finale

- Commit finale (§6): `M0-T1: loader sample ISP -> griglia canonica 13-campi (fixture) - test verdi` — add espliciti dei soli file: `src/data_layer/`, `tests/data_layer/`, `tasks/ACTIVE_TASK.md`, `Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_M0-T1_v2.md`, `Codice/Piano_di_lavoro/Esito/ESITO_M0-T1.md`.
- **Hash commit finale**: il file non può contenere l'hash del commit che lo introduce; l'hash è registrato nella sezione 12 (appendice di chiusura, commit successivo dedicato) e nel messaggio all'Orchestratore.

## 12. Appendice di chiusura (post-commit)

*Compilata nel commit di chiusura, dopo il push del commit finale.*
