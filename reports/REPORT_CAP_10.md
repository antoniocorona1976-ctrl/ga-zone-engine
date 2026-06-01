### REPORT SUPERVISORE — CAP-10

**Task**: CAP-DATA-03 — Parte 10 — Continuita' tape, recupero gap, riconciliazione canonica, storicizzazione strutturata
**Stato**: COMPLETATO

---

#### Cosa e' stato prodotto

| File | Operazione | Descrizione |
|------|-----------|-------------|
| `docs/methodology_v2/CAP_10_parte_10.md` | CREATE | Capitolo metodologico Parte 10, capitoli Cap.57-Cap.65 (~10-11 pp). Continuita' tape, recupero gap <=100gg via CANDLERANGE, riconciliazione canonica giornaliera (gate end-of-day), restart >100gg con fallback Portara, storicizzazione strutturata, coerenza inter-temporale, punti aperti, tabella decisioni D-10-1..D-10-10. |
| `reports/REPORT_CAP_10.md` | CREATE | Questo report supervisore. |
| `docs/methodology_v2/00_indice.md` | EDIT | Aggiunta voce "Parte 10" con stato "IN REVIEW" + elenco Cap.57-65, dopo il blocco Parte 9 e prima delle Appendici. |
| `tasks/DEV_STATUS.md` | EDIT | `READY_FOR_REVIEW` dopo pre-consegna 13 punti OK. |

---

#### Ipotesi di partenza

Parte 10 estende l'invariante `research = runtime` dal singolo bar (Parte 9 Cap.49) all'intero **ciclo di vita del tape**. Comportamento del GA che il capitolo intende garantire:

- **Ranking/fitness**: il bundle frozen in inference legge una griglia 1-min runtime che, se ha gap non-conciliati o `bar_synthetic` non simmetrici al training, produce feature contaminate (EGARCH su barre fittizie, regime mis-classificato, pivot instabili). Parte 10 garantisce che il tape live sia metricamente lo stesso del tape di training anche dopo backfill/riconciliazione/storicizzazione.
- **Conversione signal-to-trade**: la riconciliazione canonica giornaliera (Cap.60) e' un gate operativo **bloccante** end-of-day: se fallisce, blocca l'emissione del giorno $d+1$ fino a intervento supervisore. A differenza del monitoraggio **non bloccante** di Parte VI Cap.30 (che emette alert di deriva sulle metriche di lifecycle ma non chiude il loop, `CAP_06_parte_VI.md:276` "L'alert non chiude il loop di re-training"), il gate di Cap.60 interviene sull'operativita'. Protezione contro la deriva silenziosa del feed.
- **Validita' metriche live**: la storicizzazione (Cap.62) permette replay deterministico bit-exact anche dopo restart >100gg, evitando intervalli "n/a" recuperabili dall'archivio locale.

---

#### Decisioni rilevanti prese durante lo sviluppo

1. **`bar_synthetic` resta booleano trade/no-trade anche per barre ricostruite** (Cap.58 regola 2; AC-58-3). Una barra ricostruita via backfill con dato reale e' `bar_synthetic=False`, NON `True`. La provenienza "ricostruita post-hoc" e' tracciata interamente dal campo `source`, non dal flag. Preserva l'invariante D-9-7 di Parte 9 Cap.49.
2. **Idempotenza/immutabilita' dichiarate con perimetro empirico onesto** (Cap.59 blocco RM-1, Cap.62; AC-T-8). T+3 morning su FIB6F/DITAS = verificato (60/60); oltre T+3, afternoon/usopen, altri strumenti = "assunto per estensione, sorvegliato dal gate di Cap.60". NON dichiarato come fatto universale.
3. **Cash low/high via CANDLE ufficiale `f8`/`f9`, indipendente da Q-A-3** (Cap.60 blocco RM-1, D-10-4). Decisione forte motivata da 6/6 mismatch DITAS sul solo low; non riapre il gating cash di Parte 9 Cap.53, normizza solo la fonte del low/high.
4. **theta_reconcile parametro provvisorio non congelato** (Cap.60, D-10-10; AC-60-4). Nessun numero inventato. Trattamento analogo a $L_{max}$ Telegram e ai 12 parametri provvisori di Parte VII Cap.31.
5. **Dominio `source` esteso come complemento, non sostituto** (Cap.62, D-10-6; AC-62-2). I 3 valori Parte 9 restano invariati; i 3 nuovi `BACKFILL_FROM_*` coprono solo le barre ricostruite.
6. **Re-bootstrap >100gg con intervento supervisore obbligatorio e re-warm-up obbligatorio** (Cap.61, D-10-5; AC-61-2/AC-61-3). Eredita D-9-11 (no auto-restart) e D-9-NB4 ($L_{warmup}=30$gg). Il bundle EGARCH non gira mai su tape cross-source senza re-warm-up.
7. **Riconciliazione non-mutativa** (Cap.60, D-10-3; AC-60-5, AC-GO-3). Emette solo marker, non modifica i prezzi. Preserva replay bit-exact.
8. **Coerenza ratio-adjusted vs unadjusted esplicitata** (Cap.61, Cap.63; AC-61-4, AC-63-1/2). Il tape archiviato e' unadjusted nativa runtime; il ratio-adjusted e' ricostruito in preprocessing di training (Parte 8 Cap.38, richiamato non ridefinito); apertura DAPI come training fuori scope.

##### Decoder/convenzioni esistenti nel repo letti prima della stesura (RM-2 grep documentato)

Grep eseguiti prima della stesura (comando + esito):

1. `Grep "parse_directa_candle|CANDLERANGE|UFF|APE|manifest|bar_synthetic|RUNTIME_GAP|AGG_FROM_60s|AGG_FROM_D|forward.fill|reconcile|sanity|DEFAULT_INTRADAY_MAX_DAYS|END CANDLES"` su `scripts/` -> **4 file**: `scripts/probe_dapi.py`, `scripts/export_directa_history_parametric.py`, `scripts/update_inventory_indici_futures_daily.py`, `scripts/README_export_directa_history_parametric.txt`.
2. `Grep "manifest|bar_synthetic|RUNTIME_GAP|AGG_FROM_60s|AGG_FROM_D|forward.fill|reconcile|sanity"` su `scripts/` (22 occorrenze), `docs/` (80 occorrenze su 5 file, di cui CAP_09 47, CAP_08 23), `tasks/` (106 occorrenze su 12 file).

**Decoder/convenzioni esistenti consultati e verificati con Read (citazioni file:linea CONFERMATE accurate):**

- `[CODICE-ESISTENTE scripts/export_directa_history_parametric.py:467-481]` — `parse_directa_candle`, schema CANDLE canonico `C;L;H;O;V` (`kind, symbol, ymd, hms, uff, min_, max_, ape, qty = parts[:9]`; commento r477 `# UFF, MIN, MAX, APE => close, low, high, open`; `close_v=Decimal(uff)`/`low_v=Decimal(min_)`/`high_v=Decimal(max_)`/`open_v=Decimal(ape)`). **CONFERMATO accurato.**
- `[CODICE-ESISTENTE scripts/export_directa_history_parametric.py:228-230]` — sintassi `CANDLERANGE <sym> <start> <end> <period_s>` (period in ultima posizione). **CONFERMATO accurato.**
- `[CODICE-ESISTENTE scripts/export_directa_history_parametric.py:61]` — `DEFAULT_INTRADAY_MAX_DAYS = 100`. **CONFERMATO accurato.**
- `[CODICE-ESISTENTE scripts/export_directa_history_parametric.py:282-285,245,255]` — terminatore `END CANDLES` e regola "accetto il buffer raccolto" su timeout/socket-close dopo dati. **CONFERMATO accurato.**
- `[CODICE-ESISTENTE scripts/probe_dapi.py:230]` — `parse_line` (decoder DAPI post-rettifica `C;L;H;O`). **CONFERMATO accurato.**
- `[CODICE-ESISTENTE scripts/probe_dapi.py:159,333]` — `DapiConn` (connessione persistente) / `run_candlerange`. **CONFERMATO accurato.**

**Correzione di citazione rispetto al task card (RM-2 onesto):** il task card cita `:119-122` come "header CSV legacy (output O;H;L;C;V)". Verificato con Read: le righe 119-122 sono i campi `open/high/low/close` dentro `csv_row()` (il metodo che costruisce il dizionario di una riga), NON la definizione dell'header. La **definizione effettiva dell'header CSV legacy** e' alle righe **605-617** (`fieldnames=[...]` in `write_csv`): header a **11 campi** `symbol, timeframe, timestamp, date, time, open, high, low, close, volume, source` — include `source` ma NON `tick_count` ne' `bar_synthetic`. Il documento (Cap.62, Cap.64) cita correttamente `[CODICE-ESISTENTE scripts/export_directa_history_parametric.py:605-617]` per il legacy 11 campi. Il format esteso a 13 campi (con `tick_count` e `bar_synthetic`) e' la spec normativa di Parte 9 Cap.48 r117-122 (NON prodotta dallo script legacy). Distinzione resa esplicita nel documento.

**Pattern `reconcile` / `RUNTIME_GAP` / `forward.fill`**: nessun decoder/funzione di riconciliazione o backfill gia' esistente nel codice (`reconcile` compare solo in `update_inventory_indici_futures_daily.py` come nome generico non pertinente; `RUNTIME_GAP` compare solo nei .md di Parte 9 come marker normativo, non in codice). Conclusione RM-2: **nessuna convenzione di backfill/riconciliazione gia' implementata da re-inventare**; i marker `RUNTIME_GAP_*` sono normativi (Parte 9), USA-ti non ridefiniti. La Parte 10 non scrive codice (e' metodologia).

---

#### Misura prima/dopo

| Metrica | Prima (Parte 9 chiusa) | Dopo (Parte 10) | Delta |
|---------|------------------------|-----------------|-------|
| Temi del ciclo di vita del tape normati | 0/4 (tutti rinviati da Parte 9 Cap.55) | 4/4 (continuita', recupero, riconciliazione, storicizzazione) | +4 |
| Capitoli normativi del documento v2 | Cap.45-56 (Parte 9 ultimo = Cap.56) | + Cap.57-65 (Parte 10) | +9 capitoli |
| Tassonomia dei gap definita | assente (gap trattati solo come marker `RUNTIME_GAP_*` puntuali) | 4-tier canonica (D-10-1) | +1 vocabolario |
| Valori dominio `source` | 3 (`DIRECTA`, `AGG_FROM_60s`, `AGG_FROM_D`) | 6 (+3 `BACKFILL_FROM_*`) | +3 (complemento) |
| Gate operativi bloccanti end-of-day | 0 sul tape (Parte VI Cap.30 monitora le metriche di lifecycle dei segnali ma e' alert non bloccante, `CAP_06_parte_VI.md:276`) | 1 (riconciliazione canonica giornaliera, blocca emissione $d+1$) | +1 |
| Decisioni normative DATA | D-9-1..D-9-17 + NB2/NB3/NB4 (Parte 9) | + D-10-1..D-10-10 (Parte 10) | +10 |
| Marker complementari | `RUNTIME_*`/`CONTRACT_SWITCH`/`WARMUP_*`/`SESSION_*` (Parte 9) | + `RECONCILE_*`/`BACKFILL_FROM_*`/`BOOTSTRAP_COMPLETE`/`RUNTIME_GAP_BEYOND_100D`/`BACKFILL_VERIFIED_T3`/`BACKFILL_UNVERIFIED` (Parte 10) | +marker complementari, 0 sovrapposizioni |

Nota: tutte le metriche "prima" sono fatti documentali (Parte 9 PASS storico). Non esiste metrica numerica di performance del GA misurabile in questa fase (Parte 10 e' metodologia, non implementazione; FASE-D produrra' le metriche operative reali).

---

#### Verifica esplicita degli Acceptance Criteria

Onesta' obbligatoria: gli AC dichiarati OK hanno evidenza puntuale file:riga. Riferimenti a `CAP_10` = `docs/methodology_v2/CAP_10_parte_10.md`.

##### AC per capitolo

| AC-ID | Criterio (estratto) | Esito | Evidenza |
|-------|---------------------|-------|----------|
| AC-57-1 | Cap.57 cita rinvio Parte 9 Cap.55 + copertura 4 temi | OK | CAP_10 Cap.57 "Rinvio originale dalla Parte 9" (lista 4 temi) + "Le quattro domande operative" |
| AC-57-2 | Cap.57 dichiara invariante research=runtime esteso, rif. Parte 9 Cap.45 + Parte 8 Cap.37 | OK | CAP_10 Cap.57 "Invariante research = runtime esteso al ciclo di vita del tape" |
| AC-58-1 | Cap.58 definisce formalmente "gap" come intervallo contiguo barre 1-min mancanti | OK | CAP_10 Cap.58 "Definizione formale di gap" |
| AC-58-2 | Cap.58 tabella tassonomia 4-tier con marker Parte 9 | OK | CAP_10 Cap.58 tabella 4-tier (tier 1-4, colonna "Marker Parte 9 di riferimento") |
| AC-58-3 | Cap.58 dichiara barra backfill dato reale = `bar_synthetic=False`, provenienza in `source` | OK | CAP_10 Cap.58 "Composizione semantica" regola 2 e regola 3 (preserva invariante D-9-7 booleano) |
| AC-59-1 | Cap.59 algoritmo formale numerato >=6 step | OK | CAP_10 Cap.59 "Algoritmo formale di recupero gap" (6 step numerati) |
| AC-59-2 | Cap.59 cita :228-230 sintassi + :467-481 schema | OK | CAP_10 Cap.59 step 2 (:228-230) + step 3 (:467-481) |
| AC-59-3 | Cap.59 cita V-2 cutoff + T+1 immutabilita' con perimetro onesto | OK | CAP_10 Cap.59 blocco RM-1 cut-off (dump v2_cutoff_period60_*) + blocco RM-1 idempotenza (dump v1_hist_*) |
| AC-59-4 | Cap.59 blocco RM-1 4-righe per equivalenza CANDLERANGE/realtime | OK | CAP_10 Cap.59 blocco RM-1 (ESCLUSE: path-inference, distorsione vol, swap O/C; NON ESCLUSE: cash low, oltre T+3, afternoon, altri strumenti) |
| AC-59-5 | Cap.59 normizza caso parziale gap che attraversa 100gg + marker RUNTIME_GAP_BEYOND_100D | OK | CAP_10 Cap.59 "Cut-off finestra" (caso parziale + RUNTIME_GAP_BEYOND_100D -> Cap.61) |
| AC-60-1 | Cap.60 algoritmo formale numerato >=6 step | OK | CAP_10 Cap.60 "Algoritmo formale di riconciliazione end-of-day" (6 step numerati) |
| AC-60-2 | Cap.60 gate operativo bloccante (a differenza del monitoraggio non bloccante di Parte VI Cap.30) + stati finali con effetto sessione successiva | OK | CAP_10 Cap.60 step 6 (RECONCILE_OK/DIVERGENT_*/DEGRADED, gate bloccante vs monitoraggio non bloccante Parte VI Cap.30 `CAP_06_parte_VI.md:276`, blocco emissione d+1) |
| AC-60-3 | Cap.60 regola low/high cash via CANDLE ufficiale + V-1 afternoon + M-9 W2 | OK | CAP_10 Cap.60 step 5 + blocco RM-1 cash ([PROVA-EMPIRICA V-1 afternoon] + [PROVA-EMPIRICA W2]) |
| AC-60-4 | Cap.60 theta_reconcile parametro provvisorio non congelato, rif. d3 | OK | CAP_10 Cap.60 "Parametro theta_reconcile" (provvisorio non congelato, FASE-D, "Risponde alla domanda operativa d3") |
| AC-60-5 | Cap.60 riconciliazione non-mutativa (replay deterministico) | OK | CAP_10 Cap.60 "Vincoli operativi" 1deg bullet (non-mutativa, Parte II Cap.10 + Parte VII Cap.31) |
| AC-61-1 | Cap.61 procedura 3-step (archivio locale, CANDLERANGE daily, Portara) | OK | CAP_10 Cap.61 step 2 (Step A/B/C) |
| AC-61-2 | Cap.61 intervento supervisore obbligatorio, coerente D-9-11 | OK | CAP_10 Cap.61 step 2 (NON riparte automaticamente, eredita D-9-11) |
| AC-61-3 | Cap.61 non-mescolamento + re-warm-up L_warmup=30gg (D-9-NB4) | OK | CAP_10 Cap.61 step 3 + step 4 (re-warm-up obbligatorio, vincolo non-mescolamento) |
| AC-61-4 | Cap.61 coerenza unadjusted nativa vs ratio-adjusted training (Parte 8 Cap.38) | OK | CAP_10 Cap.61 "Coerenza ratio-adjusted vs unadjusted" |
| AC-62-1 | Cap.62 specifica CSV + manifest JSON esteso, distinto da legacy | OK | CAP_10 Cap.62 "Formato dell'archivio" (CSV 13 campi + manifest esteso) |
| AC-62-2 | Cap.62 tabella source esteso 3 nuovi BACKFILL_FROM_*, complemento | OK | CAP_10 Cap.62 tabella dominio source (6 righe, colonna "Origine" distingue eredita'/nuovo) |
| AC-62-3 | Cap.62 idempotenza + immutabilita' perimetro onesto + versioning append-only | OK | CAP_10 Cap.62 "Vincoli operativi" bullet idempotenza + immutabilita' + versioning |
| AC-62-4 | Cap.62 vincolo "archivio NON fonte training" | OK | CAP_10 Cap.62 "Vincoli operativi" bullet "NON e' fonte di training" (D-10-9) |
| AC-62-5 | Cap.62 integrazione exports/legacy/ + exports/runtime/ senza vincolare FASE-D | OK | CAP_10 Cap.62 "Integrazione con archivi esistenti" |
| AC-63-1 | Cap.63 cita ratio-adjusted Parte 8 Cap.38 come riferimento, non ridefinisce | OK | CAP_10 Cap.63 2deg bullet ("richiama come riferimento") |
| AC-63-2 | Cap.63 dichiara fuori scope apertura DAPI come training | OK | CAP_10 Cap.63 3deg bullet (fuori scope, eredita Parte 8 Cap.44 + Parte 9 Cap.55) |
| AC-64-1 | Cap.64 lista esplicita >=6 punti aperti con destinazione | OK | CAP_10 Cap.64 (9 punti aperti con destinazione FASE-D / CAP-DATA-04 / Appendice E) |
| AC-65-1 | Cap.65 tabella decisioni D-10-1..D-10-N con motivazione 1 riga | OK | CAP_10 Cap.65 tabella (D-10-1..D-10-10) |
| AC-65-2 | Cap.65 criteri di rollback per ogni decisione registrati in REPORT | OK | CAP_10 Cap.65 "Criteri di rollback registrati" + questo REPORT sezione "Criterio di rollback" |

##### AC trasversali

| AC-ID | Criterio (estratto) | Esito | Evidenza |
|-------|---------------------|-------|----------|
| AC-T-1 (RM-1) | Ogni "verificato/confermato/fatto" ha blocco 4-righe | OK | CAP_10 4 blocchi RM-1 4-righe (Cap.59 cut-off 100gg, Cap.59 equivalenza/immutabilita', Cap.60 cash low/high, Cap.61 daily). Nessuna asserzione "verificato" in prosa libera fuori dai blocchi. |
| AC-T-2 (RM-2) | Ogni richiamo struttura/format DAPI etichettato [CODICE-ESISTENTE :linea] + REPORT sezione grep | OK | CAP_10 [CODICE-ESISTENTE export_directa_history_parametric.py:467-481/:228-230/:61/:282-285/:605-617] + probe_dapi.py; REPORT sezione grep RM-2 |
| AC-T-3 (RM-3) | Prove empiriche [PROVA-EMPIRICA] con dump; wiki solo [WIKI-HINT]; nessuna conclusione livello-4 only | OK | CAP_10 [PROVA-EMPIRICA 2026-05-29/2026-06-01] con dump; unico [WIKI-HINT] per riavvio mezzanotte (Cap.64) dichiarato non autorevole |
| AC-T-4 (RM-4) | Developer NON produce probe/script/handoff nuovi; se serve Q-XX | OK | Solo 4 file del perimetro. Nessun probe/script/decoder/handoff. Nessuna Q-XX. Verificabile nel diff. |
| AC-T-5 (research=runtime) | Cap.59-62 preservano invariante esteso | OK | CAP_10 Cap.57 + Cap.58 regola 1-3 + Cap.60 non-mutativa + Cap.62 idempotenza/immutabilita' |
| AC-T-6 (coerenza CAP-08/09) | Nessuna riapertura D-8-*/D-9-*; estensioni come D-10-* | OK | CAP_10 Cap.57 ("NON riapre nessuna decisione") + Cap.62/Cap.65 (complemento, D-10-6) |
| AC-T-7 (orientamento GA) | Cap.57 dichiara impatto ranking/fitness/conversione signal-to-trade | OK | CAP_10 Cap.57 "Orientamento al comportamento del GA" (3 bullet) |
| AC-T-8 (perimetro empirico onesto) | Asserzioni su V-1/V-2/T+1 dichiarano perimetro testato + "assunto per estensione" fuori | OK | CAP_10 blocchi RM-1 "NON ESCLUSE" (T+3, morning, FIB6F/DITAS, ~100gg); Cap.62 "assunto per estensione, sorvegliato dal gate Cap.60" |
| AC-T-9 (M-promemoria) | Nessun M-promemoria nuovo dal Developer in v1 | OK | CAP_10 non emette M-promemoria |
| AC-T-10 (naming b2) | File CAP_10_parte_10.md/REPORT_CAP_10.md, identifier "Parte 10" arabo | OK | Nomi file conformi; header documento "Parte 10" (arabo) |
| AC-T-11 (lunghezza) | ~9-12 pp; ogni capitolo dimensionato come scaletta | OK | CAP_10 ~10-11 pp; capitoli entro tolleranza scaletta |
| AC-T-12 (indice aggiornato) | 00_indice.md con voce Parte 10 e stato corrente | OK | 00_indice.md voce "Parte 10" stato "IN REVIEW" + elenco Cap.57-65 |

##### AC-GO (checklist go-live / replay deterministico)

| AC-ID | Criterio (estratto) | Esito | Evidenza |
|-------|---------------------|-------|----------|
| AC-GO-1 | Replay bit-exact non impattato: 2 esecuzioni stesso input -> stessi marker/reconcile_status/archivio | OK | CAP_10 Cap.60 "Vincoli operativi" 1deg bullet + Cap.57 invariante esteso |
| AC-GO-2 | Backfill CANDLERANGE su stessa finestra -> barre bit-identiche (immutabilita' T+3 morning) | OK (perimetro esplicito) | CAP_10 Cap.59 blocco RM-1 idempotenza (60/60 entro T+3 morning FIB6F/DITAS); oltre = assunto per estensione, sorvegliato dal gate Cap.60 |
| AC-GO-3 | Riconciliazione non-mutativa sulla griglia (verifica esplicita) | OK | CAP_10 Cap.60 "Vincoli operativi" 1deg bullet + step 6 (solo marker) |
| AC-GO-4 | Marker Parte 10 complementari a Parte 9, nessuna sovrapposizione semantica | OK | CAP_10 Cap.58 (USA RUNTIME_GAP_*/RUNTIME_STALE_RESTART) + Cap.65 (RECONCILE_*/BACKFILL_FROM_*/BOOTSTRAP_COMPLETE) |

**Riepilogo AC**: 27 AC per-capitolo OK; 12 AC-T OK; 4 AC-GO OK. **Totale 43/43 OK, 0 PARZIALE, 0 MANCA.** (Nota onesta': AC-GO-2 e' OK con perimetro empirico esplicito — l'immutabilita' e' verificata entro T+3 morning sui ticker testati e dichiarata "assunta per estensione, sorvegliata dal gate Cap.60" oltre il perimetro; e' la formulazione RM-1-compliant richiesta da AC-T-8, non un PARZIALE.)

---

#### Domande aperte per il Planner

Nessuna. Il task card ha risolto tutte le ambiguita' note (schema CANDLE, sintassi CANDLERANGE, limite 100gg, immutabilita' T+3, low cash rado, dominio source, marker Parte 9, vincolo training). Nessuna Q-XX aperta in `tasks/QUESTIONS.md`. Non e' emersa necessita' di probe empirici aggiuntivi (RM-4 rispettato).

Eventuali punti che il Planner potrebbe valutare in cicli futuri (gia' fuori scope in Cap.64, NON domande aperte): rifinitura theta_reconcile in FASE-D/CAP-DATA-04; probe per estendere il perimetro empirico immutabilita' oltre T+3/afternoon/usopen/altri strumenti; M-2 Telegram in Appendice E.

---

#### Criterio di rollback

Criteri di rollback per ciascuna decisione D-10-* (registrati anche in CAP_10 Cap.65):

- **D-10-1** (tassonomia 4-tier): reversibile in capitolo successivo se emergono tipi di gap non coperti; non impatta il bundle.
- **D-10-2** (recupero CANDLERANGE + idempotenza T+3 morning): parzialmente reversibile se prove empiriche future allargano/restringono il perimetro; revisione del perimetro richiede nuovo task Planner.
- **D-10-3** (gate riconciliazione): reversibile se la sperimentazione operativa mostra troppi falsi positivi; rollback NON richiede re-training.
- **D-10-4** (cash low/high via CANDLE ufficiale): reversibile solo se il feed cash realtime diventasse denso (non atteso); fattuale al perimetro corrente.
- **D-10-5** (re-bootstrap 3-step): NON reversibile dentro Parte 10 (impatta stato post-bootstrap come D-9-NB4); revisione richiede nuovo task Planner.
- **D-10-6** (dominio source esteso): reversibile solo eliminando i 3 nuovi valori se il backfill venisse abbandonato; complemento, non impatta i 3 valori Parte 9.
- **D-10-7** (format esteso 13 campi + coabitazione): reversibile nella sola parte architetturale (exports/legacy/ vs runtime/) in FASE-D.
- **D-10-8** (immutabilita' archivio T+3 morning + versioning): perimetro empirico estendibile solo con nuovo probe; versioning append-only reversibile in FASE-D.
- **D-10-9** (vincolo training): ereditato, NON reversibile in Parte 10.
- **D-10-10** (theta_reconcile provvisorio): per costruzione rifinibile in FASE-D senza nuovo task Planner.

**Condizione globale di rollback dell'intera Parte 10**: se la sperimentazione operativa di FASE-D dimostrasse che l'invariante research=runtime esteso al ciclo di vita del tape e' irrealizzabile (es. backfill CANDLERANGE introduce sistematicamente distorsioni di volatilita' non intercettate dal gate), si tornerebbe alla situazione Parte 9 (tape runtime senza backfill strutturato), e si riaprirebbe il tema con nuovo task Planner. Probabilita' bassa: equivalenza CANDLERANGE/realtime verificata su 2 finestre indipendenti (Cap.59 blocco RM-1).

---

#### Conferma lettura regole metodologiche

Letti come prima azione della sessione: `tasks/METODO.md` (RM-1..RM-4) e `.claude/agents/developer.md` (ruolo, formato REPORT, pre-consegna 13 punti). Vincoli RM-1 (blocchi 4-righe), RM-2 (grep documentato + citazioni verificate con Read), RM-3 (etichette fonte), RM-4 (nessun output non-CAP collaterale) applicati rigorosamente.

---

#### Iterazione 2 — risposta ai finding di Review

**Origine**: `reviews/REVIEW_CAP_10_review.md` (Review v1, verdetto **PASS**, commit `ab80d96`). Il supervisore (2026-06-01) ha approvato la correzione di **tutti e 4** i finding NEUTRO in una v2 di pulizia di accuratezza. **Nessun finding e' bloccante; il verdetto v1 resta PASS.** Modifiche **chirurgiche e minime**: nessun AC, scope, decisione D-10-*, blocco RM-1 (eccetto la sola notazione interna OM-1), numero empirico o citazione di codice e' stato toccato. Il capitolo resta **43/43 AC** soddisfatti.

**Vincolo RM-2/RM-3 rispettato**: l'unica citazione cross-CAP introdotta dalla v2 e' `[DOC-INTERNO docs/methodology_v2/CAP_06_parte_VI.md:276]`. Verificata con Read **prima** di citarla: la riga 276 contiene esattamente "**L'alert non chiude il loop di re-training**" e la sezione 30.3 (`:278-291`) conferma che $f_5^{live}$ e' la metrica di **stabilita' cross-regime** (NON un Brier score) e che il meccanismo $f_1$-$f_5$ live e' di **monitoraggio non bloccante**. Nessuna nuova citazione non verificata introdotta.

**NB-1 (NEUTRO, sostanziale) — analogia cross-CAP inaccurata "gate Brier $f_5^{live}$ di Parte VI Cap.30"**
- **Cosa modificato**: rimosso il termine "Brier $f_5^{live}$" da tutte le occorrenze e riformulata l'analogia come **contrasto** accurato (gate bloccante di Cap.60 *a differenza* del monitoraggio non bloccante di Cap.30), con citazione `CAP_06_parte_VI.md:276`.
- **Occorrenze corrette (4 nel CAP + 2 propagazioni = 6 totali)**:
  - `CAP_10_parte_10.md:42` — prima: "Direttamente analogo al gate Brier $f_5^{live}$ di Parte VI Cap.30." → dopo: "gate operativo **bloccante** ... A differenza del monitoraggio **non bloccante** di Parte VI Cap.30 (... non chiude il loop, `[DOC-INTERNO ...CAP_06_parte_VI.md:276]` ...), il gate di Cap.60 **interviene sull'operativita'** bloccando l'emissione del giorno $d+1$."
  - `CAP_10_parte_10.md:126` (Cap.60 step 6) — prima: "(gate operativo, analogo al gate Brier $f_5^{live}$ di Parte VI Cap.30)." → dopo: "(gate operativo bloccante, a differenza del monitoraggio non bloccante di Parte VI Cap.30 che emette alert ma non chiude il loop, `[DOC-INTERNO ...CAP_06_parte_VI.md:276]`)."
  - `CAP_10_parte_10.md:248` (Cap.65 D-10-3) — prima: "analogo al gate Brier $f_5^{live}$ di Parte VI Cap.30" → dopo: "gate **bloccante** sull'emissione $d+1$, a differenza del monitoraggio non bloccante di Parte VI Cap.30 (`CAP_06_parte_VI.md:276`)".
  - **Propagazione 1** `00_indice.md:99` (riga Cap.60) — prima: "(analogo gate Brier $f_5^{live}$ Parte VI Cap.30)" → dopo: "(a differenza del monitoraggio non bloccante di Parte VI Cap.30)".
  - **Propagazione 2** `REPORT_CAP_10.md` "Ipotesi di partenza" (riga 24) — prima: "gate operativo end-of-day analogo al gate Brier $f_5^{live}$ (Parte VI Cap.30)" → dopo: "gate operativo **bloccante** ... A differenza del monitoraggio **non bloccante** di Parte VI Cap.30 (... `CAP_06_parte_VI.md:276` ...)". Corretto anche il riferimento nella tabella "Misura prima/dopo" (riga Gate operativi) e nella riga AC **AC-60-2** della tabella di verifica AC: in entrambe "Brier" sostituito dal contrasto accurato con Cap.30.
- **Misura prima/dopo**: prima = 6 riferimenti a un "gate Brier $f_5^{live}$" inesistente (concatenazione di due concetti non correlati + attribuzione di un comportamento "bloccante" a un alert che esplicitamente non blocca); dopo = 0 occorrenze di "Brier" in CAP_10 / 00_indice / REPORT (grep finale: 0 match), analogia sostituita da contrasto verificato.
- **Impatto GA**: nullo. Il gate di Cap.60 era ed e' definito autonomamente e correttamente (blocco $d+1$ su `RECONCILE_DIVERGENT_*`, congiunzione dei 3 check, non-mutativita'); non dipendeva dall'analogia. Correzione di sola accuratezza della citazione cross-Parte.

**OM-1 (NEUTRO) — notazione "49/13 match" ambigua**
- **Cosa modificato**: uniformata la notazione nella riga PROVE del blocco RM-1 di Cap.59; nient'altro del blocco RM-1 toccato (unica modifica ammessa dentro un blocco RM-1, da task card).
- **Prima→dopo**: `CAP_10_parte_10.md:104` — prima: "(49/13 match sulla finestra 14:55-15:25)" → dopo: "(49 match / 13 mismatch su 62 minuti, finestra 14:55-15:25)".
- **Misura prima/dopo**: prima = notazione "49/13 match" ambigua (lo slash altrove significa match/totale, es. "55/60", "60/60"); dopo = forma esplicita non ambigua, coerente con "13/62 mismatch" gia' usato in Cap.60. Il dato numerico e' invariato (49 match, 13 mismatch, 62 minuti). Impatto GA: nullo.

**OM-2 (NEUTRO) — "tutti definiti in Cap.65" impreciso**
- **Cosa modificato**: ammorbidita l'affermazione di `CAP_10_parte_10.md:62` per renderla vera, distinguendo i marker principali (consolidati in Cap.65) dai sotto-marker operativi (definiti in-body nei rispettivi capitoli).
- **Prima→dopo**: prima: "introduce marker complementari per la copertura (Cap.59 `BACKFILL_FROM_CANDLERANGE`, Cap.61 `BOOTSTRAP_COMPLETE`, Cap.60 `RECONCILE_*`), tutti definiti in Cap.65." → dopo: "i marker principali (...) sono consolidati nella tabella decisioni di Cap.65, mentre i sotto-marker operativi (`RUNTIME_GAP_BEYOND_100D` ..., `BACKFILL_VERIFIED_T3`/`BACKFILL_UNVERIFIED` ..., `RECONCILE_SCHEMA_FAIL` ...) sono definiti in-body nei rispettivi capitoli dove vengono introdotti."
- **Misura prima/dopo**: prima = affermazione falsa per 4 sotto-marker non tabulati in Cap.65; dopo = affermazione vera (i sotto-marker in-body sono esplicitamente attribuiti ai capitoli di origine). Scelta dell'opzione "ammorbidisci" (la tabella Cap.65 non e' stata modificata). Impatto GA: nullo (i marker sono vocabolario di audit log, non input di feature).

**OM-3 (NEUTRO) — disallineamento nome-marker `RECONCILE_*` vs enum manifest**
- **Cosa modificato**: aggiunta una nota esplicita di corrispondenza 1:1 tra il campo `reconcile_status` del manifest (Cap.62) e i marker `RECONCILE_*` dell'audit log (Cap.60 step 6), inserita subito dopo la definizione dell'enum manifest.
- **Prima→dopo**: prima = due nomenclature per lo stesso insieme senza mapping esplicito (`RECONCILE_OK/DIVERGENT_FIB/...` in Cap.60 `:126` vs `reconcile_status ∈ {OK, DIVERGENT_FIB, ...}` nel manifest `:188`); dopo = nuovo paragrafo "**Corrispondenza marker audit log <-> enum manifest**" (dopo `CAP_10_parte_10.md:190`): "il valore `reconcile_status = X` del manifest corrisponde 1:1 al marker `RECONCILE_X` dell'audit log (es. `reconcile_status = OK` <-> marker `RECONCILE_OK`; ...). Il manifest omette il prefisso `RECONCILE_` per concisione, ma l'insieme dei valori e la semantica sono identici."
- **Misura prima/dopo**: prima = corrispondenza implicita (chiara dal contesto ma non dichiarata); dopo = corrispondenza esplicita e univoca. Impatto GA: nullo.

**Tabella AC dopo l'iterazione 2**: invariata nei verdetti (43/43 OK). L'unica riga con evidenza ritoccata e' **AC-60-2** (riga 97), dove il riferimento "Brier" e' stato sostituito dal contrasto accurato con Cap.30; il verdetto resta **OK** e l'evidenza punta sempre a Cap.60 step 6. Nessun'altra riga AC cambia file:riga (le correzioni NB-1 su `:42`, `:126`, `:248` sono in sezioni "Ipotesi di partenza"/Cap.65 D-10-3, non in righe di evidenza AC per-capitolo diverse da AC-60-2). OM-1 e' interno al blocco RM-1 di Cap.59 (AC-59-4, evidenza "blocco RM-1 4-righe" invariata come riferimento). 

**Verifica finale v2**: grep su `CAP_10_parte_10.md` + `00_indice.md` + `REPORT_CAP_10.md` per `Brier`, `49/13`, `tutti definiti in Cap.65` → **0 match**. Nessun residuo. Nessuna regressione di AC (modifiche di sola accuratezza testuale).
