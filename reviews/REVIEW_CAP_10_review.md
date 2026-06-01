# Review CAP-10 — Parte 10 Continuità tape, recupero gap, riconciliazione canonica, storicizzazione strutturata

**Sede**: CLI locale (Windows). **Modalità**: CAP-review PIENA. **Data**: 2026-06-01. **Iterazione**: v1.
**Conferma lettura regole**: letti `tasks/METODO.md` (RM-1..RM-4) e `.claude/agents/reviewer.md` (ruolo, check, formato, regole di verdetto) come prime azioni.

**Vincolo di sede rispettato**: NON ho ri-eseguito V-1/V-2/T+1 né lanciato DAPI. Le fondamenta empiriche (schema CANDLE `C;L;H;O`, cut-off ~100gg, immutabilità T+3, low cash rado) sono già chiuse e autoritative (AUDIT-RM-RETRO CAP-DATA-02 PASS WEB+CLI + probe `687c744`). Ho auditato l'**uso** che il capitolo fa di questi fatti (accuratezza citazioni, onestà del perimetro nei blocchi RM-1) e ho verificato le citazioni `[CODICE-ESISTENTE]` **leggendo il codice committato** (sola lettura).

---

## Verdetto: **PASS**

Nessun problema bloccante. Un problema non bloccante (cross-CAP citation inaccurate, zero impatto GA) e tre osservazioni minori. Il contenuto normativo del capitolo è corretto, completo sui 43 AC, RM-1/2/3-compliant, senza residui multi-indice né leakage temporale. La metodologia regge; l'unico difetto è una citazione cross-Parte imprecisa che non altera alcun comportamento del motore.

---

## Problemi bloccanti (causano FAIL)

Nessuno.

---

## Problemi non bloccanti (causano CONDITIONAL — qui non determinano FAIL, segnalati per correzione)

### NB-1 — Analogia cross-CAP "gate Brier $f_5^{live}$ di Parte VI Cap.30" inaccurata (4 occorrenze)

Il capitolo descrive il gate di riconciliazione di Cap.60 come "Direttamente analogo al **gate Brier $f_5^{live}$** di Parte VI Cap.30". La citazione è inaccurata su **due** punti, verificati leggendo `CAP_06_parte_VI.md` Cap.30 e cercando "Brier" in tutto `docs/methodology_v2/`:

1. **Non è "Brier".** In Parte VI Cap.30.3 (`CAP_06_parte_VI.md:278-291`), $f_5^{live}$ è la metrica di **stabilità cross-regime** ($f_5 = |f_1^{calmo}-f_1^{turbolento}| / \max(\ldots)$), non un Brier score. Il Brier score nel documento appartiene a un contesto diverso: selezione Fine-Gray vs Cox su `target_1_hit` (`CAP_05_parte_V.md:463-471` + `CAP_07_parte_VII.md:65`). Non esiste alcun "gate Brier $f_5^{live}$": il termine concatena due concetti non correlati.
2. **Non è un "gate" (blocco).** Il meccanismo $f_1$-$f_5$ live di Cap.30 è un **alert/monitoraggio non bloccante**: `CAP_06_parte_VI.md:276` dichiara esplicitamente "**L'alert non chiude il loop** di re-training; la decisione ... è materia di Parte VII Cap.36, non di Cap.30". Il gate di Cap.60 di Parte 10 invece **blocca** l'emissione del giorno $d+1$. L'analogia a un "gate" bloccante è strutturalmente errata: Cap.30 non blocca nulla.

Occorrenze: `CAP_10_parte_10.md:42`, `:126`, `:248` (Cap.65 D-10-3) + `00_indice.md:99` (propagato). Anche il `REPORT_CAP_10.md` (sezioni "Ipotesi di partenza" e AC-60-2) ripete l'analogia.

**Impatto GA**: NESSUNO. Il gate di Cap.60 è definito autonomamente e correttamente (blocco $d+1$ su `RECONCILE_DIVERGENT_*`, congiunzione dei 3 check, non-mutatività, marker dettagliati); non dipende dall'analogia. Il difetto è puramente di **accuratezza della citazione cross-Parte** — un valore alto in questo progetto (cfr. cultura RM-2/RM-3), motivo per cui lo segnalo, ma non è un BUG REALE in senso GA (non distorce ranking/fitness/conversione signal-to-trade/correttezza del motore). Correzione suggerita: rimuovere "Brier" e riformulare l'analogia come "gate operativo (a differenza del monitoraggio non-bloccante di Cap.30, che emette alert ma non blocca)" oppure citare il riferimento corretto per un gate bloccante se ne esiste uno in Parte VII Cap.36.

---

## Osservazioni minori (solo impatto reale, non cosmesi sostanziale)

### OM-1 — Notazione "49/13 match" in Cap.59 RM-1 (riga 104)
Il blocco RM-1 di equivalenza (Cap.59) scrive l'afternoon come "(49/13 match sulla finestra 14:55-15:25)". Il valore canonico (probe §2.4.4, `STATO_CORRENTE.md:32`) è **49 match / 13 mismatch su 62-63 minuti**. La notazione "49/13 match" è ambigua (mescola match e mismatch in uno slash che altrove significa match/totale, es. "55/60 match" e "60/60"). Cap.60 (riga 122) usa invece la forma corretta "13/62 mismatch". Il dato è giusto, la notazione di Cap.59 è imprecisa. Impatto GA: nullo (numero corretto, recuperabile dal contesto). Suggerimento: uniformare a "49 match / 13 mismatch su 62".

### OM-2 — "tutti definiti in Cap.65" non del tutto vero per 3 sotto-marker
`CAP_10_parte_10.md:62` afferma che i marker complementari sono "tutti definiti in Cap.65". In realtà la tabella Cap.65 (D-10-1..D-10-10) tabula solo `BACKFILL_FROM_*`, `BOOTSTRAP_COMPLETE`, `RECONCILE_*`. I marker `RUNTIME_GAP_BEYOND_100D` (Cap.59 cut-off), `BACKFILL_VERIFIED_T3`/`BACKFILL_UNVERIFIED` (Cap.59 step 4) e `RECONCILE_SCHEMA_FAIL` (Cap.60 step 3) sono definiti **in-body** dove introdotti, ma non consolidati in Cap.65. Impatto GA: nullo (i marker sono vocabolario di audit log, non input di feature). Suggerimento: aggiungere una riga di nota in Cap.65 o nel REPORT che elenchi i sotto-marker definiti in-body, oppure ammorbidire "tutti definiti in Cap.65" → "i principali consolidati in Cap.65, i sotto-marker definiti nei rispettivi capitoli".

### OM-3 — Disallineamento nome-marker vs enum manifest (`RECONCILE_` prefix)
Cap.60 step 6 usa i marker `RECONCILE_OK`/`RECONCILE_DIVERGENT_FIB`/`RECONCILE_DIVERGENT_HIGHLOW`/`RECONCILE_DEGRADED`; il manifest (`:188`) usa `reconcile_status ∈ {OK, DIVERGENT_FIB, DIVERGENT_HIGHLOW, DEGRADED}` (senza prefisso). Semanticamente allineati (1:1), ma due nomenclature per lo stesso insieme. Impatto GA: nullo. Suggerimento: dichiarare esplicitamente la corrispondenza marker↔enum o uniformare. (Non bloccante: è chiaro dal contesto.)

---

## Citazioni problematiche dal testo

- "Direttamente analogo al **gate Brier $f_5^{live}$** di Parte VI Cap.30." (`CAP_10_parte_10.md:42`, ripetuta `:126`, `:248`, `00_indice.md:99`) — problema: il referente Parte VI Cap.30 NON contiene un "gate Brier $f_5^{live}$"; $f_5^{live}$ è la stabilità cross-regime (non Brier) ed è un alert **non bloccante** (`CAP_06_parte_VI.md:276`). Classificazione: **NEUTRO** (zero impatto GA; difetto di accuratezza citazione da correggere).

---

## Esito dei check RM (verifica indipendente)

### RM-1 — formato 4-righe — **COMPLIANT**
4 blocchi RM-1, tutti nel formato esatto `VERIFICA / PROVE / ALTERNATIVE COMPATIBILI ESCLUSE / ALTERNATIVE COMPATIBILI NON ESCLUSE` (`tasks/METODO.md:28-33`), verificati con grep dei token di header:
- Cap.59 cut-off ~100gg (`:79-82`): NON ESCLUSE = period diversi da 60, conteggio in giorni di trading, variabilità nel tempo. ✓
- Cap.59 equivalenza/immutabilità (`:103-106`): NON ESCLUSE = low cash rado, oltre T+3 non testato, afternoon/usopen non testato, strumenti ≠ FIB6F/DITAS non testato; perimetro onesto "T+3, morning, FIB6F/DITAS, ~100gg" esplicito. ✓
- Cap.60 cash low/high (`:136-139`): NON ESCLUSE = densità ~6 tick/min stima, DGER/DSTX50/DFRA assunti per estensione, FIB non si applica. ✓
- Cap.61 daily senza cut-off (`:168-171`): NON ESCLUSE = profondità massima esatta, daily non surrogato di 1-min. ✓

Il perimetro empirico onesto (T+3, morning, FIB6F/DITAS, ~100gg) è sistematicamente in "ALTERNATIVE NON ESCLUSE". **Nessuna asserzione "verificato/confermato/fatto/dimostrato/stabilito" in prosa libera fuori dai blocchi**: ho cercato `verificat|confermat|fatto|stabilito|dimostrat|provato|accertat` su tutto il file; tutte le occorrenze sono (a) dentro i blocchi RM-1, (b) lead-in immediato a un blocco, (c) commento post-blocco con back-reference esplicita e qualificatore di perimetro, o (d) etichetta `[WIKI-HINT, da verificare]` / condizione normativa prescrittiva. Conforme.

### RM-2 — grep + citazioni di codice — **COMPLIANT**
Grep eseguito da me su `scripts/`: pattern `parse_directa_candle|CANDLERANGE|UFF|APE|DEFAULT_INTRADAY_MAX_DAYS|END CANDLES|bar_synthetic|manifest|reconcile|RUNTIME_GAP|AGG_FROM` → 4 file (probe_dapi.py, export_directa_history_parametric.py, update_inventory_indici_futures_daily.py, README), coerente col REPORT. Verifica **riga-per-riga** di ogni citazione `[CODICE-ESISTENTE]` leggendo il file:

| Citazione nel CAP-10 | Contenuto atteso | Esito verifica |
|---|---|---|
| `export_..._parametric.py:467-481` | `parse_directa_candle`, schema `C;L;H;O;V` | **CONFERMATO ESATTO**: r.467 def, r.471 `kind,symbol,ymd,hms,uff,min_,max_,ape,qty=parts[:9]`, r.477 commento `# UFF, MIN, MAX, APE => close, low, high, open`, r.478-481 `close_v=Decimal(uff)/low_v=Decimal(min_)/high_v=Decimal(max_)/open_v=Decimal(ape)` |
| `:228-230` | sintassi CANDLERANGE, period ultimo | **CONFERMATO ESATTO**: r.228-230 `f"CANDLERANGE {symbol} {start} {end} {period_seconds}"` |
| `:61` | `DEFAULT_INTRADAY_MAX_DAYS=100` | **CONFERMATO ESATTO**: r.61 |
| `:282-285` | terminatore `END CANDLES` | **CONFERMATO ESATTO**: r.282-285 gestione `END CANDLES` |
| `:245,255` | "accetto il buffer raccolto" su timeout/socket-close | **CONFERMATO ESATTO**: r.245 (timeout), r.255 (socket chiuso) |
| `:605-617` (header legacy 11 campi) | `fieldnames=[...]` 11 campi con `source`, senza `tick_count`/`bar_synthetic` | **CONFERMATO ESATTO**: r.605-617 `fieldnames` = symbol,timeframe,timestamp,date,time,open,high,low,close,volume,source |
| `probe_dapi.py:230` | `parse_line` decoder `C;L;H;O` | **CONFERMATO**: r.230 def `parse_line`; r.247-270 schema `CANDLE;...;UFF;MIN;MAX;APE;V` → close=p[4],low=p[5],high=p[6],open=p[7] |
| `probe_dapi.py:159,333` | `DapiConn` / `run_candlerange` | **CONFERMATO ESATTO**: r.159 `class DapiConn`, r.333 `def run_candlerange` |

**Correzione `:605-617` vs `:119-122` del task card — GIUSTA.** Il task card (riga 46) citava `:119-122` come "header CSV legacy". Verificato leggendo il file: r.119-122 sono i campi `open/high/low/close` **dentro `csv_row()`** (il dict builder per-riga), NON la definizione dell'header. La definizione effettiva dell'header (la lista `fieldnames` in `write_csv`) è a **r.605-617**. La correzione del Developer è corretta su entrambi i punti: (a) la posizione giusta è `:605-617`, (b) il conteggio è **11 campi** (con `source`, senza `tick_count`/`bar_synthetic`). Distinzione legacy-11 vs runtime-esteso-13 resa esplicita nel documento (Cap.62, Cap.64). Coerente con RACC-METODO-2: la verifica include il diff con lo schema canonico (legacy 11 ≠ esteso 13 di Parte 9 Cap.48 r117-122, `CAP_09_parte_9.md:120` confermato).

Nessun decoder/parser di backfill/riconciliazione pre-esistente non citato: grep `reconcile|RUNTIME_GAP|forward.fill` conferma che `reconcile` compare solo come nome generico in `update_inventory_*` (non pertinente) e `RUNTIME_GAP` solo nei .md di Parte 9 (marker normativo, non codice). Parte 10 è metodologia, non scrive codice. Conforme.

### RM-3 — fonti etichettate — **COMPLIANT**
Ogni `[PROVA-EMPIRICA <data>]` ha dump citato; i 4 dump cardine **esistono** su `probe_out/` (verificato con ls): `v2_cutoff_period60_20260529_104927.csv`, `v2_cutoff_period86400_20260529_105739.csv`, `v1_hist_20260529_fetched_20260529_094821.csv`, `v1_hist_20260529_fetched_20260601_135432.csv`. Il wiki Directa compare **solo** come `[WIKI-HINT, da verificare]` (Cap.64 `:231`, riavvio mezzanotte) con dichiarazione esplicita "il wiki Directa è dimostrato inesatto sullo schema CANDLE". Nessuna conclusione si appoggia solo a livello 4. I numeri empirici citati combaciano con le fonti autoritative:
- cut-off intraday: satura `2026-02-18 09:56`, 38.567 candele da N=80 → **MATCH** probe §4.2.
- cut-off daily: N=160 → first_ts `2026-01-05` → **MATCH** probe §4.3.
- morning 55/60 match tol 0.05 → **MATCH** probe §2.3.
- afternoon 49 match/13 mismatch → **MATCH** probe §2.4.4 + `STATO_CORRENTE.md:32`.
- T+1/T+3 immutabilità 60/60 → **MATCH** probe §2.5.
- cash DITAS 6/6 mismatch sul solo low → **MATCH** probe §2.4.5 lettera A.
- schema PRICE `f4=last, f6=volume_cum, f8=day_low, f9=day_high` → **MATCH** `STATO_CORRENTE.md:73` M-9 [PROVA-EMPIRICA 2026-06-01 W2] (ipotesi Web "bid/ask" falsificata, come dichiarato). Conforme.

---

## Coerenza strutturale (verifica indipendente)

- **(a) Nessuna riapertura D-8-*/D-9-***: il capitolo dichiara estensioni come complemento (dominio `source`, marker, format) e nuove D-10-*. Verificato: nessuna D-8/D-9 toccata. ✓
- **(b) Citazioni cross-CAP verso Parte 8 e Parte 9 — verificate a campione leggendo i referenti**:
  - Parte 9 marker `RUNTIME_GAP_START/END` (Cap.50 `:224,229`), `RUNTIME_DEGRADED` (Cap.50 `:233`), `WARMUP_COMPLETE` (Cap.51 `:257`), `CONTRACT_SWITCH` (Cap.47 `:103`), `SESSION_OPEN` (Cap.52 `:299`) — **TUTTI ESISTONO e contengono ciò che CAP-10 afferma**. ✓
  - `RUNTIME_STALE_RESTART` = **D-9-11** (Parte 9 Cap.51 `:259-263` body "B-6" + tabella decisioni `:426` D-9-11): la citazione CAP-10 "RUNTIME_STALE_RESTART (Cap.51 D-9-11)" è **accurata** (il body lo chiama B-6 ma la decisione tabulata è D-9-11, che è proprio RUNTIME_STALE_RESTART + rinvio CAP-DATA-03). ✓
  - dominio `source D-9-5` (`:420`, `:135-137`), `L_warmup=30gg` D-9-NB4 (`:435`), `bar_synthetic` booleano trade/no-trade (`:181`), regola touch su sintetiche (`:189`), schema storico CANDLERANGE→bar_synthetic da presenza-in-risposta (`:178`) — **TUTTI CONFERMATI**. ✓
  - Rinvio originale Parte 9 Cap.55 (AC-57-1, "r393-398") — **CONFERMATO**: `CAP_09_parte_9.md:393-398` contiene esattamente i 4 temi rinviati a CAP-DATA-03. ✓
  - Parte 8 Cap.40 forward-fill+`bar_synthetic` (`:79-94`), Cap.41 epoca E5 08:00-22:00 (`:119,133`), Cap.38 ratio-adjusted da `UnadjustedClose+RollSpread+roll log` (`:13,27`), Cap.39 filtro pre-expiry N=3 (`:55,157`), Cap.43 sanity metrics (`:49,194,201`), Cap.44 esclusione fonti — **TUTTI CONFERMATI**. ✓
  - Parte II Cap.10 replay deterministico (`CAP_02_parte_II.md:23,131`) — esiste, accurato. ✓
  - schema PRICE `f8`/`f9`: CAP-10 cita correttamente l'autoritativo M-9 (2026-06-01 W2) e NON riapre Parte 9 Cap.47 (che aveva lo schema PRICE con `bid_qty?`/`ask_qty?` flaggati incerti, poi raffinati da W2). Mossa corretta. ✓
  - **UNICA citazione cross-CAP non confermata**: "gate Brier $f_5^{live}$ Parte VI Cap.30" (vedi NB-1). Il referente NON contiene ciò che il capitolo afferma.
- **(c) research = runtime esteso correttamente**: l'invariante è esteso dal singolo bar (Parte 9 Cap.49) al ciclo di vita del tape; backfill usa la regola storica di bar_synthetic (presenza-in-risposta), simmetrica al training (trade-presence Parte 8 Cap.40), preservando l'invariante. Nessuna asimmetria live/storico introdotta. ✓
- **(d) Nessun residuo multi-indice (DCC/ADCC/BEKK/N≥8/covarianza)**: cercato; gli unici riferimenti cross-index (`:234`) sono **esclusioni esplicite** PHASE-2 fuori scope. Specializzazione FIB N=1 preservata. ✓
- **(e) Nessun leakage temporale**: la riconciliazione end-of-day usa solo dati del giorno $d$ chiuso; il gate blocca $d+1$ (causalità corretta, nessun dato futuro nel modello). La CANDLE di controllo è richiesta a 22:30 CET post-chiusura. Backfill ricostruisce il passato, non anticipa. ✓
- **(f) Marker Parte 10 complementari (no sovrapposizione semantica con Parte 9)**: `RECONCILE_*`/`BACKFILL_FROM_*`/`BOOTSTRAP_COMPLETE`/`RUNTIME_GAP_BEYOND_100D` coprono riconciliazione/backfill/bootstrap, semanticamente disgiunti dai `RUNTIME_*`/`CONTRACT_SWITCH`/`WARMUP_*`/`SESSION_*` di Parte 9 (che CAP-10 USA, non ridefinisce). AC-GO-4 sostanzialmente soddisfatto (vedi OM-2 per la nota di consolidamento). ✓
- **(g) Formalizzazione/registro/LaTeX coerenti**: definizione formale di gap (insieme massimale contiguo su griglia 840-barre), 840 = 14h×60min (08:00-22:00 CET) coerente con Parte 8 Cap.41 + Parte 9 D-9-NB4. Notazione LaTeX coerente coi capitoli esistenti. Registro italiano formale tecnico. ✓

---

## Completezza AC — verifica indipendente (claim → evidenza)

Ho verificato i 43 AC del task card contro il documento, non fidandomi degli "OK" del REPORT. Esito: **43/43 sostanzialmente soddisfatti**, evidenza puntuale confermata.

- **27 AC per-capitolo (AC-57-1..AC-65-2)**: tutti soddisfatti. Campioni controllati a fondo: AC-59-2 (`:88` step2 :228-230 + `:89` step3 :467-481 ✓), AC-59-4 (blocco RM-1 4-righe con ESCLUSE path-inference/distorsione vol/swap O/C ✓), AC-60-3 (regola cash f8/f9 + V-1 afternoon + W2 ✓), AC-60-5 (non-mutativa ✓), AC-61-2 (intervento supervisore D-9-11 ✓), AC-61-3 (re-warm-up L_warmup=30gg D-9-NB4 ✓), AC-62-2 (tabella source 6 righe, 3 nuovi BACKFILL complemento ✓), AC-65-2 (rollback in REPORT ✓).
- **12 AC-T (trasversali)**: tutti soddisfatti. AC-T-1 (RM-1 4 blocchi, nessuna prosa libera ✓), AC-T-2 (RM-2 citazioni + sezione grep REPORT ✓), AC-T-3 (RM-3 ✓), AC-T-4 (nessun probe/script/handoff nuovo — solo 4 file del perimetro, verificato col diff ✓), AC-T-5/6/7/8 (perimetro empirico onesto sistematico ✓), AC-T-10/11/12 (naming, lunghezza ~10-11pp, indice ✓).
- **4 AC-GO**: AC-GO-1 (replay bit-exact non impattato — riconciliazione non-mutativa ✓), AC-GO-2 (immutabilità T+3 morning con perimetro esplicito ✓), AC-GO-3 (non-mutativa ✓), AC-GO-4 (marker complementari ✓, con OM-2 minore).
- **14 Done-when (d1..d14)**: tutte risposte. d1/d2 (Cap.58 composizione + source ✓), d3 (θ_reconcile provvisorio ✓), d4 (caso parziale RUNTIME_GAP_BEYOND_100D ✓), d5 (backoff + marker ✓), d6/d7 (ordine 3 check + gate d+1 ✓), d8 (cash via CANDLE ufficiale ✓), d9/d10/d11 (header 13 + manifest esteso + versioning ✓), d12/d13 (3-step + re-warm-up obbligatorio ✓), d14 (NO training, vincolo invariato ✓).

**Conteggio: 43/43 AC verificati OK, 0 non soddisfatti.** L'autodichiarazione 43/43 del Developer è **confermata indipendentemente** (con la riserva NB-1 che non è un AC ma una citazione cross-CAP inaccurata, e OM-1/2/3 osservazioni minori).

---

## Lista "Empirico-CLI da verificare"

**VUOTA.** Nessuna asserzione del capitolo richiede una prova DAPI non già chiusa. Tutte le `[PROVA-EMPIRICA]` puntano a dump esistenti e già autoritativi (V-1/V-2/T+1/W2 chiusi in AUDIT-RM-RETRO CAP-DATA-02 + probe `687c744`). Il capitolo USA i fatti chiusi, non ne introduce di nuovi. Coerente con l'attesa del task (Sede CLI, fatti empirici già chiusi).

---

## Classificazione per il supervisore

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|------------------------|
| 1 | Analogia "gate Brier $f_5^{live}$ Parte VI Cap.30" inaccurata: Cap.30 non ha un gate Brier; $f_5^{live}$ è stabilità cross-regime ed è alert **non bloccante** (Cap.30 ":276" non chiude il loop) | `CAP_10_parte_10.md:42,126,248` + `00_indice.md:99` + `REPORT_CAP_10.md` (Ipotesi + AC-60-2) | **NEUTRO** (zero impatto GA; difetto di accuratezza citazione) | A discrezione del supervisore — è una correzione di accuratezza testuale, non un BUG REALE. Default: opzionale |
| 2 | Notazione "49/13 match" ambigua (corretto: 49 match/13 mismatch su 62) | `CAP_10_parte_10.md:104` | **NEUTRO** | NO — dato corretto, solo notazione |
| 3 | "tutti definiti in Cap.65" non vero per `RUNTIME_GAP_BEYOND_100D`/`BACKFILL_VERIFIED_T3`/`BACKFILL_UNVERIFIED`/`RECONCILE_SCHEMA_FAIL` (definiti in-body, non in Cap.65) | `CAP_10_parte_10.md:62` vs Cap.65 | **NEUTRO** | NO — vocabolario audit, non feature; consolidamento opzionale |
| 4 | Disallineamento nome-marker `RECONCILE_*` vs enum manifest `{OK,DIVERGENT_*,DEGRADED}` | `CAP_10_parte_10.md:127` vs `:188` | **NEUTRO** | NO — semanticamente 1:1, chiaro dal contesto |

Nessun finding **BUG REALE**, **MIGLIORA PERFORMANCE** o **RISCHIO PEGGIORAMENTO**. Tutti NEUTRO. Il verdetto è PASS perché nessuno è bloccante e nessuno impatta comportamento GA / ranking / fitness / conversione signal-to-trade / correttezza.

---

## Applicazione RM-1 a me stesso (Reviewer)

- "Citazioni di codice CONFERMATE": ho letto ogni range citato in `export_directa_history_parametric.py` (r.61, 119-122, 228-230, 240-289, 460-489, 598-622) e `probe_dapi.py` (r.155-166, 222-285, 329-340), confrontando token-per-token con la citazione. ALTERNATIVE ESCLUSE: citazione a riga sbagliata (controllato che la riga citata contenga davvero il costrutto, non una riga adiacente); schema divergente (confrontato la mappatura `uff→close/ape→open` letterale). NON ESCLUSE: che righe NON citate dal documento contengano decoder concorrenti — mitigato dal grep su 4 pattern di dominio (nessun decoder candle/backfill aggiuntivo trovato), ma non ho letto le ~620 righe integrali dello script.
- "Numeri empirici MATCH": ho confrontato i numeri del capitolo con `tasks/PROBE_RECUPERO_GAP_DAPI.md` e `tasks/STATO_CORRENTE.md` (fonti autoritative committate). NON ho ri-eseguito i probe (vincolo di sede: fatti già chiusi). "MATCH" = i numeri citati coincidono con quelli nelle fonti chiuse, non = ho ri-misurato contro DAPI.
- "Cross-CAP CONFERMATI": ho aperto `CAP_08`, `CAP_09`, `CAP_06`, `CAP_02` e letto i referenti citati. "Coerente" = ho cercato la decisione/marker citato e verificato che esista e dica ciò che CAP-10 afferma. ALTERNATIVE ESCLUSE per NB-1: ho cercato "Brier" in TUTTO `docs/methodology_v2/` (non solo Cap.30) per escludere che un gate Brier esistesse altrove e fosse citato con riferimento sbagliato — non esiste alcun gate Brier in nessuna Parte. NON ESCLUSE: non ho letto integralmente Parte VII Cap.36 (gate decisionali post-go-live), dove potrebbe esistere un meccanismo bloccante diverso; ma anche se esistesse, non sarebbe "Brier $f_5^{live}$ di Parte VI Cap.30" come scritto.

---
PASS: nessun problema bloccante (4 osservazioni NEUTRO ammesse). Il capitolo è RM-1/2/3-compliant, 43/43 AC soddisfatti, citazioni di codice esatte (inclusa la correzione `:605-617` giusta), nessun residuo multi-indice né leakage. L'unico difetto sostanziale (NB-1) è una citazione cross-Parte inaccurata a impatto GA nullo, classificata NEUTRO e lasciata alla decisione del supervisore.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
