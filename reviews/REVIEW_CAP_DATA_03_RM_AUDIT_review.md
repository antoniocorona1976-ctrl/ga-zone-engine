# AUDIT-RM CAP-DATA-03 — audit indipendente RM-1/2/3 sul perimetro A-D (Parte 10)

**Perimetro auditato (4 oggetti di prima classe)**:
- **A** = `docs/methodology_v2/CAP_10_parte_10.md` (Cap.57-65, capitolo CAP-DATA-03)
- **B** = `reports/REPORT_CAP_10.md` (report supervisore Developer, 43 AC + Iterazione 2)
- **C** = `tasks/PROBE_RECUPERO_GAP_DAPI.md` (documento-sorgente empirico V-1/V-2/T+1 + self-review RM-4)
- **D** = `scripts/export_directa_history_parametric.py` (decoder canonico di produzione, fonte CODICE-ESISTENTE level-2, **NON modificabile**)

**Sede**: CLI locale (Windows). **Modalità**: AUDIT-RM mirato a 4 sorgenti contemporaneamente (NON CAP-review piena — Parte 10 è già PASS v1 `ab80d96` + v2 `48171e4` —; NON probe-review standard). Task card autoritativo: `tasks/ACTIVE_TASK.md` (commit `bf6ad13`).
**Conferma lettura regole**: letti come prime azioni `tasks/METODO.md` (RM-1: verifica vs assunzione + blocco 4-righe; RM-2: grep nel repo prima di assumere format esterno; RM-3: doc esterna non è fonte di verità + etichette livello; RM-4: output non-CAP) e `.claude/agents/reviewer.md` (ruolo ostile, 4 check probe-review, divieti di sede CLI, formato output, regole di verdetto).

**Vincolo di sede rispettato**: NON ho eseguito alcun probe DAPI né aperto socket. Le fondamenta empiriche (inputs autoritativi #5..#15 del task card: schema CANDLE `C;L;H;O;V`, cut-off ~100gg intraday / daily illimitato, equivalenza V-1 morning+afternoon, immutabilità T+3 morning, cash low/high `f8`/`f9`, codici errore, cooldown refutato, BOOK_5 certificato) sono **CHIUSE e autoritative**: ne ho controllato l'**USO** dentro A/B/C, **NON** le ho ri-derivate. Le citazioni `[CODICE-ESISTENTE]` sono verificate **leggendo i sorgenti committati con Read** (sola lettura). I dump `probe_out/*` sono verificati per **sola esistenza** con Glob (NON ri-aperti contro DAPI live).

---

## Verdetto: **PASS**

Perimetro A-D **RM-compliant** anche a un secondo sguardo ostile esteso a B/C/D come oggetti di prima classe. 0 BUG REALE, 0 MIGLIORA PERFORMANCE, 0 RISCHIO PEGGIORAMENTO. 1 sola osservazione NEUTRO (phrasing "OHLCV coincidenti" in un blocco RM-1, impatto GA nullo, dettaglio sotto). I 4 finding NEUTRO di v1 (NB-1 + OM-1/2/3) reggono e non sono regrediti. Lista "Empirico-CLI da verificare": **VUOTA** (atteso). Regola di decisione applicata: PASS se 0 BUG REALE e 0 finding bloccante (AC-11).

**Dichiarazione di indipendenza** (AC-13): NON ho copia-incollato sezioni di v1/v2. Le ho usate come consapevolezza (sapere che NB-1/OM-1/2/3 erano già chiusi). Ho **esteso** l'audit dove v1/v2 hanno toccato meno: (a) **B come perimetro a sé** — onestà claim→evidenza dei 43 AC + veridicità della sezione "Decoder esistenti" + RACC-METODO-2 sui diff con D; (b) **C come perimetro a sé** — fedeltà delle citazioni A→C, copertura del self-review RM-4, coincidenza numeri canonici, e la distinzione wire-schema `C;L;H;O;V` vs CSV-output-order `O;H;L;C;V` (§7.3); (c) **D letto direttamente** alle righe citate come fonte di verità token-per-token. Tutti i grep di dominio sono stati ri-eseguiti **da me** (non ripresi dal REPORT né dalle review precedenti).

---

## Voci W auditate

15 voci dell'inventario W del task card (W1-W15) + **1 voce W16** emersa nel secondo giro ostile (phrasing "OHLCV coincidenti"). Esito sintetico per voce:

| W | Asserzione | Esito audit |
|---|------------|-------------|
| W1 | Schema CANDLE `C;L;H;O;V` = `UFF;MIN;MAX;APE;V` | **OK** — citazione level-2 D `:467-481` verificata token-per-token; A non dichiara "verificato" lo schema senza il riferimento level-2 |
| W2 | Cut-off intraday ~100gg, tronca al minuto (sat. `2026-02-18 09:56`, 38.567 candele da N=80) | **OK** — blocco RM-1 4-righe formato esatto; D `:61`; numeri coincidono A↔C §4.2 |
| W3 | CANDLERANGE daily nessun limite a 100gg (first_ts → `2026-01-05` a N=160) | **OK** — blocco RM-1 4-righe; coerente con W2 (intraday vs daily distinti); C §4.3 |
| W4 | Sintassi CANDLERANGE period-LAST 4 arg | **OK** — D `:228-230` verificata token-per-token |
| W5 | Equivalenza realtime↔CANDLERANGE 2 finestre (morning 55/60 + afternoon 49/13), nessuno swap O/C su 7 FIB6F | **OK** (con W16 sotto) — blocco RM-1 4-righe; test discriminante `local_O≠hist_C` coerente C §2.4.5 |
| W6 | Immutabilità T+3 morning (60/60), perimetro empirico onesto | **OK** — perimetro "T+3, morning, FIB6F/DITAS, ~100gg" sistematicamente in NON ESCLUSE; D-10-2/D-10-8 coerenti |
| W7 | Cash low/high via CANDLE ufficiale `f8`/`f9` (6/6 mismatch DITAS sul solo low) | **OK** — blocco RM-1 4-righe; coerente C §2.4.5 lettera A + STATO M-9 |
| W8 | Schema PRICE `f4/f6/f8/f9`, `f5`/`f7` parziali, "bid/ask" Web falsificata | **OK** — coerente con STATO M-9 (W2); verifica parziale di `f5`/`f7` dichiarata |
| W9 | CSV runtime esteso 13 campi vs legacy 11; dominio `source` esteso 3+3 | **OK** — legacy 11 = D `:605-617` (verificato, no `tick_count`/`bar_synthetic`); esteso 13 = CAP_09 `:120` (verificato); D-9-5 = CAP_09 `:420` (verificato) |
| W10 | Codici errore DAPI come trigger backoff; semantica "verifica parziale ereditata" | **OK** — etichetta [PROVA-EMPIRICA] accurata; A **sotto-claim** (conservativo, non over-claim); coerente M-3 (1030 non riprodotto) |
| W11 | Marker Parte 10 complementari (no sovrapposizione Parte 9) | **OK** — `RUNTIME_GAP_*` Cap.50 `:224,229`, `WARMUP_COMPLETE` Cap.51 `:257`, `SESSION_OPEN` Cap.52 `:299`, `RUNTIME_STALE_RESTART`/D-9-11 Cap.51 `:259-263` (payload verbatim) tutti verificati; fix OM-2 (sotto-marker in-body) regge |
| W12 | Citazione `CAP_06_parte_VI.md:276` (post-fix NB-1) | **OK** — riga 276 verbatim "L'alert non chiude il loop di re-training"; §30.3 `:280` conferma `f_5^{live}`=stabilità cross-regime, NON Brier; Cap.30 non-bloccante. Fix NB-1 accurato, non regredito |
| W13 | Invariante research=runtime esteso al ciclo di vita del tape; `bar_synthetic` booleano | **OK** — D-9-7 = CAP_09 `:181,:422` (verificato); Parte 8 Cap.40 `:79,82` forward-fill; replay Cap.10 preservato; nessuna asimmetria live/storico |
| W14 | Onestà claim→evidenza 43 AC del REPORT | **OK** — campione ≥15 AC verificato direttamente in A (sotto); 0 AC con evidenza vuota/generica/errata |
| W15 | Self-review RM-4 di C (r.384-433) | **OK** — blocco 4-righe per asserzione (a) afternoon + (b) immutabilità; grep RM-2 documentato; etichette RM-3; assunzioni non testate esplicite |
| **W16** | (nuova) Phrasing "OHLCV coincidenti" in blocco RM-1 Cap.59 `:105` | **NEUTRO** — vedi dettaglio sotto, impatto GA nullo |

---

## Check A — RM-1 (formato 4-righe + sostanza) per ogni W

**A.1/A.2 — Localizzazione + formato.** I 4 blocchi RM-1 attesi in A esistono e sono nel formato esatto `VERIFICA / PROVE / ALTERNATIVE COMPATIBILI ESCLUSE / ALTERNATIVE COMPATIBILI NON ESCLUSE` (`tasks/METODO.md:28-33`):
- Cap.59 cut-off ~100gg — `:79-82` ✓
- Cap.59 equivalenza/immutabilità — `:103-106` ✓
- Cap.60 cash low/high — `:136-139` ✓
- Cap.61 daily senza cut-off — `:168-171` ✓

**Asserzioni "verificato/confermato/fatto/dimostrato/stabilito" fuori dai 4 blocchi (prosa libera)**: grep `verificat|confermat|dimostrat|provato|accertat|stabilito|comprovato` su A → tutte le occorrenze sono (a) dentro i 4 blocchi RM-1, (b) lead-in immediato a un blocco (`:76` "Il limite è stabilito empiricamente:" → blocco `:79-82`), (c) tabella Cap.65 D-10-* con back-reference esplicita a un blocco RM-1 (`:249` "verificata 60/60", `:255`), oppure (d) **condizione normativa prescrittiva** (`:219` "a condizione che la coerenza … sia verificata [dalla riconciliazione Cap.60]" — futuro prescrittivo, NON asserzione di fatto empirico) o etichetta `[WIKI-HINT, da verificare]` (`:233`). **Nessuna asserzione "verificato" in prosa libera che richieda un blocco 4-righe mancante.** Conforme (AC-1).

**A.3 — Sostanza.** Le ALTERNATIVE ESCLUSE sono effettivamente escluse dai dati osservati e le NON ESCLUSE sono davvero compatibili:
- Cut-off `:81`: "limite al giorno intero" escluso dal minuto preciso `09:56`; "limite del solo period 60" escluso dalla simultaneità 3 ticker → sostanza coerente con C §4.2 (saturazione identica FIB6F/DITAS/CM.MESM6). ✓
- Equivalenza `:105-106`: swap O/C escluso dal discriminante `local_O==hist_C` mai verificato su 7 FIB6F; rewriting escluso da 60/60 attraverso weekend; NON ESCLUSE = cash low rado, oltre T+3, afternoon/usopen, strumenti ≠ FIB6F/DITAS → tutte effettivamente non testate (coerente C §2.4.6/§2.5.1). ✓
- Cash `:138-139`: low realtime corretto escluso da 6/6 mismatch sul solo low; swap di schema escluso (high coincide) → coerente C §2.4.5 lettera A. ✓
- Daily `:170-171`: limite 100gg sul daily escluso dal first_ts che regredisce → coerente C §4.3. ✓

**A.5 — Confronto con inputs autoritativi #5..#15.** Nessuna contraddizione con gli inputs autoritativi: schema CANDLE, sintassi CANDLERANGE, cut-off intraday/daily, equivalenza, immutabilità T+3, cash low/high, codici errore, schema PRICE sono tutti **ridichiarati fedelmente** in A/B/C. Nessun "verificato universalmente" di ciò che gli inputs limitano a un perimetro empirico: il perimetro (T+3, morning, FIB6F/DITAS, ~100gg) è in ALTERNATIVE NON ESCLUSE in ogni blocco pertinente e ribadito in Cap.62 `:208` e Cap.64 `:234`. Conforme.

---

## Check B — RM-2 (grep + citazioni verso D-canonico)

**B.1 — Grep dei pattern di dominio (ri-eseguiti dal Reviewer).** Comandi e esiti sintetici:

1. `Grep "O;L;H;C|O;H;L;C"` su perimetro A/B/C/D + probe_dapi.py → in **A: 0** occorrenze come schema canonico (solo `C;L;H;O;V`); in **B `:56`**: `O;H;L;C;V` compare solo come **citazione del testo del task card** che B sta correggendo (contesto di correzione); in **C**: tutte le occorrenze in contesti di **rifiuto/correzione** (§3.1 fatto errato, §3.2 correzione, §7.2 "inventata", self-review `:395` "decoder errato O;L;H;C"); in **probe_dapi.py** solo `[WIKI-HINT, smentito]` (`:15`) e commenti "ERRATO" (`:251`). **Esito atteso confermato**: nessuna occorrenza dello schema sbagliato come "canonico" nel perimetro.
2. `Grep "C;L;H;O"` su perimetro → A `:89` cita `C;L;H;O;V` con `[CODICE-ESISTENTE :467-481]`; C usa `C;L;H;O` (senza `;V`) coerentemente; nessun conflitto.
3. `Grep "CANDLERANGE|period_seconds|86400"` su D → `:228-230` comando (period last), `:526/:733/:741` daily 86400. ✓
4. `Grep "DEFAULT_INTRADAY_MAX_DAYS|2026-02-18|38.567|100 giorni"` su perimetro → D `:61` costante, `:22` docstring "chunk max 100 giorni", `:1030` uso; numeri cut-off coincidenti A↔C. ✓
5. `Grep "fieldnames|tick_count|bar_synthetic"` su D → `fieldnames` **solo** `:605`; `tick_count`/`bar_synthetic` **assenti** da D → conferma header legacy 11 campi (non 13). ✓
6. `Grep "RUNTIME_GAP|BACKFILL_FROM|RECONCILE_|BOOTSTRAP_COMPLETE|…"` su A → 43 occorrenze (marker normativi, vocabolario audit). ✓
7. `Grep "f8|f9|day_low|day_high|6/6|tick/min"` su A/C/STATO → A `:136-139` cash, coerente C §2.4.5 + STATO M-9 `:75`. ✓
8. `Grep "RUNTIME_STALE_RESTART|D-9-11|D-9-5|D-9-7|D-9-NB4|L_warmup"` su CAP_09 → tutti verificati (vedi Check D). ✓

**B.2 — Verifica file:linea delle citazioni `[CODICE-ESISTENTE]` (leggendo D e probe_dapi.py con Read):**

| Citazione nel perimetro | File:linea | Contenuto atteso | Esito verifica |
|---|---|---|---|
| A `:89`, B `:49`, C `:413`, self-review C `:413` | `export_..._parametric.py:467-481` | `parse_directa_candle`, schema `C;L;H;O;V`, commento r.477 | **CONFERMATO ESATTO** — r.467 `def parse_directa_candle`, r.471 `kind,symbol,ymd,hms,uff,min_,max_,ape,qty=parts[:9]`, r.477 `# Documentazione Directa: UFF, MIN, MAX, APE => close, low, high, open.`, r.478-481 `close_v=Decimal(uff)/low_v=Decimal(min_)/high_v=Decimal(max_)/open_v=Decimal(ape)`, r.482 `volume_v=int(Decimal(qty))` |
| A `:88`, B `:50`, C §2.2/§4.1 | `export_..._parametric.py:228-230` | sintassi `CANDLERANGE … period_seconds` (period ultimo) | **CONFERMATO ESATTO** — r.228-230 `f"CANDLERANGE {symbol} {start_dt.strftime(DIRECTA_TS_FMT)} {end_dt.strftime(DIRECTA_TS_FMT)} {period_seconds}"`, `period_seconds` parametro a r.223, LAST |
| A `:80`, B `:51` | `export_..._parametric.py:61` | `DEFAULT_INTRADAY_MAX_DAYS=100` | **CONFERMATO ESATTO** — r.61 `DEFAULT_INTRADAY_MAX_DAYS = 100` |
| A `:89`, B `:52` | `export_..._parametric.py:282-285,245,255` | terminatore `END CANDLES` + "accetto buffer raccolto" su timeout/socket-close | **CONFERMATO ESATTO** — r.282-285 gestione `END CANDLES` (`text.startswith/in`), r.245 warning timeout "accetto il buffer raccolto", r.255 warning socket chiuso idem |
| A `:185`, `:210`, `:230`, B `:56` | `export_..._parametric.py:605-617` | header CSV legacy 11 campi, con `source`, senza `tick_count`/`bar_synthetic` | **CONFERMATO ESATTO** — r.605-617 `fieldnames=[symbol,timeframe,timestamp,date,time,open,high,low,close,volume,source]` (11 campi); `tick_count`/`bar_synthetic` assenti in tutto D |
| B `:53`, C `:414`, self-review | `probe_dapi.py:230` | `parse_line` decoder | **CONFERMATO** — r.230 `def parse_line(line: str) -> dict:` |
| B `:54`, C `:414` | `probe_dapi.py:159,333` | `DapiConn` / `run_candlerange` | **CONFERMATO ESATTO** — r.159 `class DapiConn:`, r.333 `def run_candlerange(...)` |

**B.3 — Coerenza A/C ↔ D canonico.** Tutti gli schemi/format DAPI in A e C combaciano con D alle righe esatte (tabella sopra). **Sottolineatura ostile — wire-schema vs CSV-output-order**: C §7.3 `:357` afferma che "gli artefatti storici si possono leggere con la convenzione `O;H;L;C;V` dei CSV". Verificato che NON è una contraddizione con lo schema wire `C;L;H;O;V`: la riga si riferisce all'**ordine delle colonne** del CSV output di `write_csv`, che da D `:605-617` è effettivamente `open, high, low, close, volume` (= O,H,L,C,V come ordine di colonna), mentre il **wire DAPI** è `UFF;MIN;MAX;APE;V` (= C,L,H,O,V come ordine dei campi sul filo). C distingue esplicitamente i due piani (§3.2/§7.5 wire `C;L;H;O;V`; §7.3 output CSV `O;H;L;C;V`). Coerente con D. Nessuna divergenza.

**B.4 — RACC-METODO-2 (diff puntuale col decoder canonico per ogni AC su schema esterno).** Onorata. Gli AC di B che dichiarano "schema X OK" hanno il **diff puntuale** con D, non la sola completezza strutturale:
- AC-59-2 (`:92`): cita `:228-230` + `:467-481` con il contenuto verificato. ✓
- AC-62-1/AC-62-2 (`:105-106`): la distinzione legacy-11 (D `:605-617`) vs runtime-esteso-13 (CAP_09 `:120`) è il diff puntuale richiesto — B `:56` lo esplicita correttamente (i 2 campi differenza: `tick_count`, `bar_synthetic`). ✓
- AC-T-2 (`:121`): elenca le citazioni `[CODICE-ESISTENTE]` con le righe. ✓
Inoltre la sezione "Decoder esistenti" di B (`:47-58`) è **veritiera**: i 6 decoder/righe citati esistono e contengono ciò che B afferma (verificato sopra).

**B.5 — Decoder pre-esistenti non citati.** Nessuno. Grep su `parse_directa_candle|UFF|MIN|MAX|APE` → 4 file (probe_dapi.py, export_…_parametric.py, update_inventory_…, README). `update_inventory_indici_futures_daily.py` non contiene un decoder candle alternativo (uso generico). `reconcile`/`RUNTIME_GAP`/`forward.fill` non esistono come codice di backfill/riconciliazione (solo marker normativi nei .md di Parte 9 + nome generico in update_inventory). **Conclusione RM-2: nessuna convenzione di backfill/riconciliazione già implementata da re-inventare; Parte 10 è metodologia, non scrive codice.** Conforme (AC-2).

---

## Check C — RM-3 (etichettatura fonti per livello)

**C.1 — Etichette presenti.** Ogni evidenza nel perimetro è etichettata: `[PROVA-EMPIRICA <data>]` (V-1/V-2/T+1/W2), `[CODICE-ESISTENTE <path>:<linea>]` (decoder), `[DOC-INTERNO <path>]` (cross-CAP), `[WIKI-HINT, da verificare]` (un solo riferimento). Conforme.

**C.2 — Livello adeguato.** Nessuna conclusione del perimetro si appoggia **solo** a livello 4. L'unico riferimento wiki Directa è in A Cap.64 `:233` (riavvio Darwin mezzanotte), etichettato `[WIKI-HINT, da verificare]` con dichiarazione esplicita "il wiki Directa è dimostrato inesatto sullo schema CANDLE e va trattato come hint anche qui". C §7.4 (M-11) e self-review `:420` ribadiscono l'inaffidabilità del wiki (`O;H;L;C`). Ogni asserzione strutturale ha almeno una fonte livello 1/2/3. Conforme (AC-3).

**C.3 — Numeri canonici (coincidenza A ↔ C ↔ STATO M-*):**

| Numero | A | C | STATO M-* | Esito |
|---|---|---|---|---|
| morning 55/60 match tol 0.05 | `:104` | §2.3 `:68` | — | **MATCH** |
| afternoon 49 match / 13 mismatch su 62 | `:104` | §2.4.4 `:124-128` | — | **MATCH** |
| saturazione cut-off `2026-02-18 09:56`, 38.567 candele, da N=80 | `:80` | §4.2 `:238-244` | — | **MATCH** |
| daily first_ts → `2026-01-05` a N=160 | `:169` | §4.3 `:256` | — | **MATCH** |
| immutabilità T+3 morning 60/60 OHLCV | `:104` | §2.5 `:158` | — | **MATCH** |
| cash 6/6 mismatch DITAS sul solo low, ~6 tick/min | `:137` | §2.4.5 lettera A `:132` | — | **MATCH** |
| schema PRICE `f4=last,f6=volume_cum,f8=day_low,f9=day_high`, `f5`/`f7` parziali, "bid/ask" falsificata | `:137` | — | M-9 `:75` | **MATCH** |
| codici 1004/1007/1017/1015/1003 ri-auditati, 1030 non riprodotto | `:97` | — | M-3 `:69` | **MATCH** |
| griglia 840 barre = 14h×60min (08:00-22:00 CET) | `:49`,`:120` | — | (CAP_08 `:65`, CAP_09 D-9-NB4 `:435`) | **MATCH** |

Nessuna discrepanza numerica. Conforme.

**C.4 — Dump esistenti (Glob `probe_out/*`, sola esistenza).** Tutti i dump citati da A/B/C esistono: `v2_cutoff_period60_20260529_104927.csv` ✓, `v2_cutoff_period86400_20260529_105739.csv` ✓, `v1_hist_20260529_fetched_20260529_094821.csv` (T+0) ✓, `v1_hist_20260529_fetched_20260601_135432.csv` (T+1/T+3) ✓, `v1_now_20260601_145507.decoded.csv` ✓, `v1_now_hist_20260601_152554.csv` ✓, `v1_compare_20260601_152556.json` ✓, `v1_compare_20260529_100125.json` (morning) ✓, dump M-3/M-9 (`w4_errcodes_20260529.json`, `w5_w10_20260601_111246.json`, `w2_w3_w6_20260601_111350.json`) ✓. Conforme.

**C.5 — Perimetro empirico onesto.** A dichiara sistematicamente il perimetro empirico nei blocchi RM-1 (ALTERNATIVE NON ESCLUSE: oltre T+3 / afternoon-usopen / strumenti ≠ FIB6F-DITAS / period diversi da 60 / densità cash stima) e lo ribadisce in Cap.62 `:208` ("assunto per estensione, sorvegliato dal gate Cap.60") e Cap.64 `:234`. Nessun "verificato universalmente" senza qualificatore di perimetro. Conforme.

---

## Check D — Coerenza inter-file (A ↔ B ↔ C ↔ D + cross-CAP)

**D.1 — Citazioni di A verso C.** "[PROVA-EMPIRICA V-1 afternoon §2.4.5 lettera A — 6/6 mismatch DITAS sul solo low]" (A `:137`) → C contiene esattamente §2.4.5 lettera A con 6/6 mismatch DITAS sul solo low (`:132`). Tutti i §-reference di A verso C (§2.3, §2.4, §2.4.5, §2.5) esistono e contengono i numeri citati. ✓

**D.2 — Citazioni di A verso D.** I ranges `:467-481`, `:228-230`, `:61`, `:282-285`, `:605-617` esistono e contengono i costrutti dichiarati (Check B.2). ✓

**D.3 — Citazioni cross-CAP (referenti letti con Read):**
- `CAP_06_parte_VI.md:276` — verbatim "**L'alert non chiude il loop di re-training**: la decisione di ritraining … è materia di Parte VII Cap.36 … non di Cap.30." + §30.3 `:280` `f_5^{live}`=stabilità cross-regime (formula esplicita, NON Brier). **CONFERMATO** (W12). ✓
- `CAP_09_parte_9.md` marker: `RUNTIME_GAP_START/END` Cap.50 `:224,229` ✓; `WARMUP_COMPLETE` Cap.51 `:257` ✓; `SESSION_OPEN` Cap.52 `:299` ✓; `RUNTIME_STALE_RESTART`/D-9-11 Cap.51 `:259-263` (body "B-6", payload `{downtime_days:N, reason:"gap_exceeds_DAPI_100d_window"}` **verbatim** in A Cap.61) ✓.
- `CAP_09_parte_9.md` decisioni: D-9-5 dominio `source∈{DIRECTA,AGG_FROM_60s,AGG_FROM_D}` `:420` ✓; D-9-7 `bar_synthetic` propagato runtime=training `:422` + body `:181` (booleano trade/no-trade, discriminante realtime/storico = porta) ✓; D-9-NB4 `L_warmup=30gg` `:435` (con "30 sessioni × 840 barre") ✓; header runtime 13 campi Cap.48 `:120` ✓.
- `CAP_09_parte_9.md` Cap.55 rinvio 4 temi → `:391-400` + D-9-17 `:432` (continuità tape / recupero gap / riconciliazione / storicizzazione rinviati a CAP-DATA-03 / Parte 10) **CONFERMATO** (A Cap.57). ✓
- `CAP_08_parte_8.md` Cap.40 forward-fill+`bar_synthetic` `:79,82,84` ✓; Cap.41 epoca E5 / 840 barre `:65` ✓; Cap.38 ratio-adjusted `UnadjustedClose+RollSpread+roll log` (richiamato a `:94`) ✓.
- `CAP_02_parte_II.md` Cap.10 replay deterministico bit-exact (richiamato da CAP_08 `:94` + CAP_09 `:181`). ✓

**D.4 — Coerenza B ↔ A.** Ogni AC dichiarato OK in B con evidenza "Cap.X step Y" punta a una riga di A che effettivamente lo soddisfa (Check E.1). B non afferma di A cose che A non dice. ✓

**D.5 — Coerenza C ↔ A.** Il self-review RM-4 di C copre realmente (a) afternoon (49/13 + nessuno swap O/C, `:393-396`) e (b) immutabilità T+3 morning (60/60, `:402-405`); i numeri di C coincidono con A (Check C.3). ✓

**D.6 — Coerenza interna A.** Nessuna auto-contraddizione:
- Tassonomia 4-tier coerente Cap.58 `:55-60` ↔ Cap.65 D-10-1 `:248`. ✓
- Marker Parte 10 ↔ enum manifest 1:1: Cap.60 step 6 `:124-127` (`RECONCILE_OK/DIVERGENT_FIB/DIVERGENT_HIGHLOW/DEGRADED`) ↔ Cap.62 manifest `:188` (`{OK,DIVERGENT_FIB,DIVERGENT_HIGHLOW,DEGRADED}`) con paragrafo di corrispondenza esplicita `:192` (fix OM-3) — insieme e semantica identici. ✓
- Dominio `source` 6 valori coerente Cap.58 regola 3 `:68` ↔ Cap.59 step 5 `:91` ↔ Cap.62 tabella `:196-204`. ✓

Conforme (AC-4).

---

## Check E — Onestà claim → evidenza (B, e per scrupolo A)

**E.1 — Campione AC del REPORT (≥15 verificati direttamente leggendo A).** Ho verificato **24 AC** (ben oltre il minimo di 15), tutti con evidenza puntuale reale in A:

| AC | Evidenza dichiarata | Verifica in A | Esito |
|---|---|---|---|
| AC-57-1 | rinvio Cap.55 + 4 temi | Cap.57 `:15-22` | OK |
| AC-58-1 | def formale gap | Cap.58 `:49` (insieme massimale contiguo) | OK |
| AC-58-2 | tabella 4-tier | Cap.58 `:55-60` | OK |
| AC-58-3 | backfill dato reale = `bar_synthetic=False` | Cap.58 regola 2 `:67` | OK |
| AC-59-1 | algoritmo ≥6 step | Cap.59 `:85-92` (6 step) | OK |
| AC-59-2 | cita `:228-230` + `:467-481` | Cap.59 step 2/3 `:88-89` | OK |
| AC-59-3 | V-2 cutoff + T+1 perimetro onesto | Cap.59 blocchi RM-1 `:79-82`,`:103-106` | OK |
| AC-59-4 | blocco RM-1 4-righe equivalenza | Cap.59 `:103-106` | OK |
| AC-59-5 | caso parziale + `RUNTIME_GAP_BEYOND_100D` | Cap.59 `:98` | OK |
| AC-60-1 | algoritmo ≥6 step | Cap.60 `:117-127` (6 step) | OK |
| AC-60-2 | gate bloccante vs Cap.30 non-bloccante | Cap.60 step 6 `:126` (`:276` corretto) | OK |
| AC-60-3 | cash via CANDLE + V-1 afternoon + W2 | Cap.60 step 5 `:123` + RM-1 `:136-139` | OK |
| AC-60-4 | θ_reconcile provvisorio | Cap.60 `:131` | OK |
| AC-60-5 | riconciliazione non-mutativa | Cap.60 `:146` | OK |
| AC-61-2 | intervento supervisore D-9-11 | Cap.61 step 2 `:158` | OK |
| AC-61-3 | re-warm-up L_warmup=30gg | Cap.61 step 3/4 `:162-163` | OK |
| AC-61-4 | coerenza unadjusted vs ratio-adjusted | Cap.61 `:174` | OK |
| AC-62-1 | CSV + manifest esteso vs legacy | Cap.62 `:185-188` | OK |
| AC-62-2 | tabella source 6 righe complemento | Cap.62 `:196-204` + `:194` | OK |
| AC-62-4 | archivio NON fonte training | Cap.62 `:209` (D-10-9) | OK |
| AC-T-1 | 4 blocchi RM-1, no prosa libera | verificato Check A | OK |
| AC-T-8 | perimetro empirico onesto | NON ESCLUSE + `:208`,`:234` | OK |
| AC-GO-2 | immutabilità T+3 morning perimetro esplicito | Cap.59 `:103-106` | OK |
| AC-GO-4 | marker complementari no sovrapposizione | Cap.58/Cap.65 | OK |

**0 AC con evidenza vuota, generica o errata.** L'autodichiarazione 43/43 OK del REPORT è confermata sul campione esteso. Conforme (AC-5, AC-14 del task W14).

**E.2 — Iterazione 2 regge (no regressione):**
- **NB-1**: grep `Brier` su A → **0 match**. Le uniche occorrenze di "Brier" in `docs/` pertinenti sono il contesto EGARCH σ² calibration (Q-06 / Parte V), non il perimetro A. Fix accurato: citazione `:276` verbatim, Cap.30 non-bloccante, `f_5^{live}` non-Brier. ✓
- **OM-1**: A `:104` "(49 match / 13 mismatch su 62 minuti, finestra 14:55-15:25)" — notazione disambiguata. Resto del blocco RM-1 intatto. ✓
- **OM-2**: A `:62` distingue marker principali (Cap.65) da sotto-marker in-body (`RUNTIME_GAP_BEYOND_100D` `:98`, `BACKFILL_VERIFIED_T3`/`BACKFILL_UNVERIFIED` `:90`, `RECONCILE_SCHEMA_FAIL` `:121`). Vero. ✓
- **OM-3**: paragrafo corrispondenza 1:1 `:192` (Check D.6). ✓
Nessun fix ha sostituito un errore con un altro. Conforme (AC-6).

**E.3 — Domande aperte.** REPORT dichiara "Nessuna". Verificato `tasks/QUESTIONS.md`: Q-01..Q-09 tutte CHIUSA; M-5/M-6 sono carryover per **Parte V** (benchmark window EGARCH, regime media/mediana), NON pertinenti al perimetro Parte 10. Nessuna Q-XX aperta pertinente. Conforme.

**E.4 — Criterio di rollback.** Per ogni D-10-1..D-10-10 il rollback è registrato in REPORT `:158-167` con motivazione coerente con A Cap.65 `:259-267` (verificata corrispondenza 1:1 delle 10 voci). Conforme.

---

## Osservazione NEUTRO (W16) — phrasing "OHLCV coincidenti" nel blocco RM-1 Cap.59

**A `:105`** (riga ALTERNATIVE COMPATIBILI ESCLUSE) motiva l'esclusione di path-inference/distorsione volatilità con "…escluso dall'equivalenza su 2 finestre indipendenti (morning + afternoon) **con OHLCV coincidenti**". Lettura ostile: C §2.4.5(B) documenta che sui 7 minuti FIB6F afternoon in mismatch l'open (o close) scarta di **1-6 tick** al confine del minuto (es. `dO +30` = 6 tick = 30pt), quindi gli OHLCV NON coincidono *tutti* esattamente — ci sono 13 mismatch su 62.

**Perché NON è BUG REALE**: (1) la VERIFICA `:103` qualifica già "indistinguibili dalle barre live **a eccezione del low del cash rado**" e le NON ESCLUSE `:106` elencano esplicitamente cash low / oltre-T+3 / afternoon / strumenti come non testati → il blocco **non nasconde** i mismatch; (2) la claim effettivamente esclusa è "path-inference / distorsione di volatilità / swap O/C", tutte e tre realmente escluse: i 13 mismatch sono scarti di **confine minuto** (quale tick è "primo del minuto" nella cattura realtime, artefatto di SUB timing) + **low cash rado**, NON distorsione del range; (3) **high coincide su tutti i 7 FIB6F e low coincide su tutti i 7 FIB6F** (C §2.4.5(B)), quindi il **range H-L** — ciò che alimenta le feature di volatilità EGARCH (Parte III Cap.13) — è esatto; lo scarto è solo sull'open di confine in un segmento veloce (15:11-18, prezzo in caduta). **Impatto GA = NULLO** (range/volatilità esatti; nessuna distorsione di ranking/fitness/conversione). Suggerimento testuale opzionale (NON necessario per PASS): sostituire "con OHLCV coincidenti" con "con range OHLC coincidente e scarti residui solo su open/low di confine minuto (≤6 tick, non sistematici)". **Classificazione: NEUTRO** — è una sfumatura di phrasing dentro la riga ESCLUSE, non un fatto falso; la sostanza (no distorsione, no swap) è corretta e le eccezioni sono dichiarate nello stesso blocco.

---

## Lista "Empirico-CLI da verificare"

**VUOTA** (atteso, AC-9). Nessuna asserzione del perimetro A-D richiede una prova DAPI live non già chiusa. Tutte le `[PROVA-EMPIRICA]` puntano a dump esistenti e autoritativi (V-1 morning+afternoon, V-2 intraday+daily, T+1/T+3, W2 schema PRICE), chiusi negli inputs autoritativi #5..#15. Il perimetro **USA** i fatti empirici chiusi senza introdurne di nuovi che eccedano il perimetro empirico già stabilito. Nessuna asserzione eccede il perimetro empirico chiuso.

---

## Tabella classificazione per il supervisore

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|------------------------|
| 1 | Phrasing "OHLCV coincidenti" nella riga ESCLUSE del blocco RM-1 Cap.59 (i 7 FIB6F afternoon hanno scarti open/low di confine minuto ≤6 tick; range H-L esatto, eccezioni già dichiarate in VERIFICA + NON ESCLUSE) | `CAP_10_parte_10.md:105` | **NEUTRO** (impatto GA nullo; sostanza corretta, sfumatura di phrasing) | NO — opzionale; la sostanza regge, le eccezioni sono già disclosed nello stesso blocco |

Nessun finding **BUG REALE**, **MIGLIORA PERFORMANCE** o **RISCHIO PEGGIORAMENTO**. L'unico finding è NEUTRO. Verdetto PASS perché nessuno è bloccante e nessuno impatta comportamento GA / ranking / fitness / conversione signal-to-trade / correttezza matematica / conformità RM.

---

## Acceptance criteria dell'audit — esito

| AC | Esito |
|---|---|
| AC-1 (RM-1 perimetro A: 4 blocchi formato esatto + sostanza, no prosa libera) | **PASS** |
| AC-2 (RM-2 grep + citazioni D verificate token-per-token + RACC-METODO-2) | **PASS** |
| AC-3 (RM-3 fonti etichettate, no livello-4-only, numeri canonici) | **PASS** |
| AC-4 (coerenza inter-file A↔B↔C↔D + cross-CAP + auto-coerenza A) | **PASS** |
| AC-5 (onestà claim→evidenza B: ≥15 AC verificati, qui 24) | **PASS** |
| AC-6 (Iterazione 2 regge: NB-1/OM-1/2/3 chiusi, no regressione) | **PASS** |
| AC-7 (self-review RM-4 di C copre afternoon + T+3, formato 4-righe) | **PASS** |
| AC-8 (RM-1 applicato al Reviewer: sezione presente, sostegno operativo) | **PASS** |
| AC-9 (lista Empirico-CLI esplicita, VUOTA) | **PASS** |
| AC-10 (tabella classificazione supervisore) | **PASS** |
| AC-11 (verdetto motivato + regola di decisione) | **PASS** |
| AC-12 (naming + path output `REVIEW_CAP_DATA_03_RM_AUDIT_review.md`, NON RETRO) | **PASS** |
| AC-13 (audit indipendente, non copia-incolla v1/v2, esteso a B/C/D) | **PASS** |

---

## Applicazione RM-1 a me stesso (Reviewer)

- **"Citazioni `[CODICE-ESISTENTE]` CONFERMATE token-per-token"**: ho letto con Read ogni range citato in `export_directa_history_parametric.py` (r.55-64, 100-134, 220-294, 460-499, 600-623) e `probe_dapi.py` (r.159, 230, 333), confrontando il token cercato con la riga citata. **ALTERNATIVE ESCLUSE**: citazione a riga adiacente sbagliata — escluso controllando il numero di riga esatto nel cat -n (es. `fieldnames` compare SOLO a `:605`, non altrove → l'header è inequivocabilmente lì); schema divergente — escluso confrontando la mappatura letterale `uff→close/min_→low/max_→high/ape→open` r.478-481. **ALTERNATIVE NON ESCLUSE**: che righe di D NON lette contengano un secondo decoder candle — mitigato dal grep su `parse_directa_candle|UFF|MIN|MAX|APE` (un solo decoder candle, a `:467-481`) ma non ho letto integralmente le ~1030 righe di D.
- **"Numeri empirici MATCH"**: ho confrontato i numeri di A con C (`PROBE_RECUPERO_GAP_DAPI.md`) e `STATO_CORRENTE.md` §5 (fonti autoritative committate). "MATCH" = i numeri citati coincidono con le fonti chiuse, **NON** = ho ri-misurato contro DAPI (vincolo di sede CLI: empirico chiuso, niente probe di zelo). **ALTERNATIVE NON ESCLUSE**: i dump `probe_out/*` sono verificati per sola esistenza (Glob), non ri-computati — coerente col divieto di sede.
- **"Cross-CAP CONFERMATI"**: ho aperto `CAP_06_parte_VI.md` (r.272-281), `CAP_09_parte_9.md` (r.117-300, 385-445), `CAP_08_parte_8.md` (r.65-103) e letto i referenti citati. "CONFERMATO" = ho trovato la decisione/marker/riga citata e verificato che esista e dica ciò che A afferma. **ALTERNATIVE ESCLUSE** per W12 (NB-1): grep `Brier` su A → 0 match (escluso che un "gate Brier" sopravviva nel perimetro normativo). **ALTERNATIVE NON ESCLUSE**: non ho riletto integralmente Parte VII Cap.36 (gate decisionali post-go-live) — irrilevante al fix, che afferma solo che Cap.30 **non** chiude il loop, fatto verificato verbatim a `:276`.
- **"Nessun finding bloccante"**: il secondo giro ostile ha prodotto 1 sola osservazione NEUTRO (W16, phrasing). **ALTERNATIVE ESCLUSE**: che "OHLCV coincidenti" nasconda una distorsione di volatilità — escluso perché H e L coincidono su tutti i 7 FIB6F (range esatto) e i mismatch sono open-boundary + cash-low, non sistematici. **NON ESCLUSE**: che esistano asserzioni W17+ a rischio in porzioni di A/B/C non lette integralmente — mitigato avendo letto A (268 righe), B (214 righe), C (434 righe) per intero e i ranges D/cross-CAP citati; ritengo la copertura sufficiente per un audit confermativo su perimetro già PASS×2.

---
**PASS**: perimetro A-D RM-1/2/3-compliant a un secondo sguardo ostile indipendente esteso a B/C/D. 0 BUG REALE / 0 MIGLIORA PERFORMANCE / 0 RISCHIO PEGGIORAMENTO; 1 osservazione NEUTRO a impatto GA nullo. I fix di v1 (NB-1 + OM-1/2/3) reggono e non sono regrediti. Tutte le citazioni `[CODICE-ESISTENTE]` verso D verificate token-per-token; tutti i numeri canonici coincidenti A↔C↔STATO M-*; tutti i cross-CAP verificati con Read; tutti i dump citati esistenti. Self-review RM-4 di C copre realmente afternoon + immutabilità T+3. Lista "Empirico-CLI da verificare" VUOTA. Conferma di simmetria col trattamento AUDIT-RM ricevuto da CAP-DATA-01/02: l'apparato RM (formato e sostanza) è pratica stabile del progetto sul perimetro esteso, non solo sul singolo CAP.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
