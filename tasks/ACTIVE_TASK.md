# CAP-DATA-01 — Convenzione dati storici e politica di rollover

**Status:** IN CORSO (apertura sessione 2026-05-27)
**Tipo:** Parte 8 del nuovo doc metodologico v2 (`docs/methodology_v2/`)
**Posizione nel documento:** Parte 8, immediatamente prima dell'Appendice (che diventa Parte 9)
**Predecessor:** Parte 7 (CAP-07 v2 chiuso PASS Review v2 commit `b27c1e3` del 2026-05-27)
**Successor:** Parte 9 (Appendici A-G)
**Task operativo gemello (fuori doc metodologico):** CAP-DATA-02 — Specifica della richiesta tecnica a Portara
**Owner deliverable:** Development agent (Claude Code)
**Supervisore:** AC

<!-- ORCH-NOTE: NON RIMUOVERE — eccezione strutturale autorizzata dal supervisore -->
## ⚠️ ATTENZIONE PER REVIEWER — eccezione alla regola "residui multi-indice = bloccante"

Il subagente `reviewer` (`.claude/agents/reviewer.md` riga 38) dichiara come regola assoluta:

> "Specializzazione FIB N=1: ci sono residui di multi-indice (DCC, ADCC, BEKK, N>=8, covarianza cross-index)? Se si, e' un problema bloccante."

Questa regola e' stata scritta quando il doc v2 era esplicitamente single-instrument FIB. Il task CAP-DATA-01 §3.6 introduce **deliberatamente** DCC/ADCC/cDCC come **dichiarazione normativa PHASE-2**, decisione ratificata dal supervisore (AC) in conversazione del 2026-05-27, decisione (1): "dichiarazione normativa senza implementazione nel doc v2". Vedi commit `f497022` e file `tasks/SESSION_HANDOFF_CAP-07_to_CAP-DATA-01.md` §4.

**Il Reviewer NON deve classificare come bloccanti** le citazioni cross-index in §3.6 e nelle sue sezioni collegate (fasizzazione PHASE-1/PHASE-2, `S_xidx`, quinta famiglia catalogo target, Realized GARCH come esempio futuro). Sono normative dichiarate, non residui da rimuovere.

**La regola "residui multi-indice = bloccante" resta valida** per qualunque citazione cross-index al di FUORI di §3.6 (es. se il Developer inserisse DCC in §3.4 preprocessor griglia 1-min o in altre sezioni non legate alla fasizzazione PHASE-2).

Decisioni collegate ratificate (handoff §4):
- (1) Cross-index DCC/ADCC/cDCC: dichiarazione normativa nel doc v2 SENZA implementazione
- (2) Realized GARCH: estensione futura, non in Parte 8 (citare con cautela come esempio futuro o omettere se crea ambiguita')
- (3) `S_xidx` + quinta famiglia catalogo target: estensione futura, non in Parte 8 (coerente con (1))

<!-- ORCH-NOTE: fine eccezione -->

---

## Dati di input recuperati dall'Orchestratore

Questa sezione contiene la tabella sessioni FIB recuperata dall'Orchestratore al passo STEP 2 della sequenza operativa via WebFetch/WebSearch su fonti ufficiali Borsa Italiana e archivi storici. **E' INPUT AUTORITATIVO** per il Developer (vedi memory `project-orchestrator-input-is-authoritative`): il Developer NON verifica nuovamente le date, NON propone modifiche, NON ridiscute orari. Copia i dati nel CSV normativo a 6 campi `data/sessions/fib_session_calendar.csv` rispettando lo schema del task card §3.5. Eventuali metadati di provenienza (URL fonte, data consultazione ISO, note di ambiguita') vanno SOLO in `data/sessions/README.md`, lasciando il CSV pulito.

### Tabella sessioni FIB — schema normativo §3.5

| epoch_id | start_date | end_date | session_open_local | session_close_local | timezone |
|----------|------------|----------|--------------------|--------------------|----------|
| E1 | 1994-11-28 | 2010-11-07 | 09:15 | 17:30 | CET |
| E2 | 2010-11-08 | 2015-11-22 | 09:00 | 17:40 | CET |
| E3 | 2015-11-23 | 2017-07-02 | 09:00 | 17:50 | CET |
| E4 | 2017-07-03 | 2020-02-16 | 09:00 | 20:30 | CET |
| E5 | 2020-02-17 | 2026-05-27 | 08:00 | 22:00 | CET |

**Note di interpretazione:**
- `session_open_local` indica l'inizio della **sessione di negoziazione continua** (escludendo la fase di asta di apertura, che esiste in tutte le epoche ma con timing variabile e non rilevante per la semantica del segnale).
- `session_close_local` indica la chiusura della sessione di negoziazione continua. Per E4 (2017-2020) gli orari sono single continuous session 09:00-20:30 con marcatore convenzionale di transizione fra "diurna" e "serale" alle 17:50, ma da Cap.10 PII del doc v2 in poi la sessione e' trattata come finestra continua singola; il marker 17:50 NON e' una pausa di mercato.
- `end_date` indica l'ultimo giorno in cui l'epoca era in vigore (giorno PRIMA della data di entrata in vigore della epoca successiva). Per E5 la `end_date` e' la data corrente di consultazione (2026-05-27); la timeline va estesa quando emergeranno nuove epoche.
- Tutti i timestamp sono in **CET**: la pipeline gestira' la conversione automatica CEST in vigore (ultima domenica di marzo → ultima domenica di ottobre) coerentemente con le convenzioni del task card §3.5 e della semantica eventi/timestamp del doc v2.
- Tick FIB = 5 punti indice. Multiplier FIB pieno = 5 EUR/punto (miniFIB = 1 EUR/punto). Coerenti con preambolo `00_indice.md` e con [[project-fib-instrument]].

### Sotto-tabella fonti e ambiguita'

| epoch_id | fonte_url | data_consultazione_ISO | note_ambiguita |
|----------|-----------|------------------------|----------------|
| E1 (data inizio) | https://www.bankpedia.org/termine.php?c_id=20457 | 2026-05-27 | Lancio mercato IDEM 1994-11-28 confermato da bankpedia e Wikipedia IDEM; **prima negoziazione FIB30 quel giorno**. Sottostante: indice MIB30 (predecessore di FTSE MIB, transizione MIB30 → S&P/MIB → FTSE MIB avvenuta nel 2003-2004 e poi 2009; il **contratto FIB e' continuativo** nella serie Portara back-adjusted). |
| E1 (orari) | https://www.borsaitaliana.it/borsaitaliana/ufficio-stampa/comunicati-stampa/2000/000613minifib.htm | 2026-05-27 | Orari **09:15-17:30 CET** confermati per il 2000 dal comunicato lancio miniFIB. **DATA DA VERIFICARE**: la fonte conferma gli orari nel 2000, NON il periodo intero 1994-2010. Possibili modifiche intermedie non documentate dalle fonti consultate. Si assume continuita' 1994-2010 in mancanza di evidenze contrarie. |
| E1 (data fine) | https://www.thetradenews.com/borsa-italiana-derivatives-market-moves-to-sola-platform/ + Avviso Borsa n.15413 del 21/10/2010 | 2026-05-27 | Migrazione SOLA dichiarata per 2010-11-08 (Avviso n.15413: "IDEM - SOLA migration: postponement to 8th November 2010"). **DATA DA VERIFICARE**: l'associazione fra migrazione SOLA e cambio orari 09:15→09:00 / 17:30→17:40 e' un'**inferenza** non documentata esplicitamente nelle fonti consultate. Plausibile ma non confermata. |
| E2 (orari) | https://www.borsaitaliana.it/borsaitaliana/ufficio-stampa/comunicati-stampa/2015/orarinegoziazione.htm | 2026-05-27 | Orari **09:00-17:40 CET** derivati per **inferenza inversa** dal comunicato Borsa Italiana del 2015 che cita "17:40 (IDEM - calcolato dalla differenza)" come orario precedente all'estensione a 17:50. L'orario di apertura 09:00 e' coerente con il modello IDEM noto e con il comunicato 2017 (`https://www.borsaitaliana.it/derivati/derivati/estensioneorarifibeminifib.en.htm`) che dichiara come orari pre-2017 "9 am to 5.50 pm CET". **DATA DA VERIFICARE**: la transizione 09:15→09:00 e 17:30→17:40 non e' documentata da un comunicato ufficiale diretto nei risultati delle ricerche. |
| E3 (estensione 17:40 → 17:50) | https://www.borsaitaliana.it/borsaitaliana/ufficio-stampa/comunicati-stampa/2015/orarinegoziazione.htm | 2026-05-27 | Data **2015-11-23** confermata da comunicato Borsa Italiana ufficiale. Cita esplicitamente IDEM equity derivatives: "fase di negoziazione continua viene estesa fino alle 17.50" con "posticipamento di 10 minuti rispetto alla chiusura precedente" (17:40). |
| E4 (estensione 17:50 → 20:30) | https://www.borsaitaliana.it/borsaitaliana/ufficio-stampa/comunicati-stampa/2017/idem.en.htm + https://www.borsaitaliana.it/derivati/derivati/estensioneorarifibeminifib.en.htm | 2026-05-27 | Data **2017-07-03** confermata da comunicato Borsa Italiana ufficiale: "As from today, IDEM ... has extended its trading hours" (data pubblicazione 2017-07-03). Orari: "continuous trading from 09:00 to 20:30" con sessione diurna 09:00-17:50 e serale 17:50-20:30, single continuous session (no pausa). |
| E5 (estensione 20:30 → 22:00) | https://www.borsaitaliana.it/borsaitaliana/ufficio-stampa/comunicati-stampa/2020/estensioneorariidem.htm + https://www.borsaitaliana.it/derivati/nuovi-orari-di-negoziazione-fib-e-minifib.en.htm | 2026-05-27 | Data **2020-02-17** confermata da comunicato Borsa Italiana ufficiale: "a partire da oggi, 17 febbraio 2020". Orari: "Dalle 07:45 alle 8:00 la fase di asta di apertura (pre-asta, validazione, apertura) e dalle 8:00 fino alle 22:00 la negoziazione in continua". Per la metodologia (sessione = continuous trading), `session_open_local=08:00`. |

### Nota per il Developer su come usare questa tabella

> "La tabella sessioni FIB inserita in ACTIVE_TASK.md dalla sezione 'Dati di input recuperati dall'Orchestratore' e' INPUT AUTORITATIVO. NON verificare con fonti esterne. NON proporre modifiche. NON ridiscutere date o orari. Copia i dati nel CSV normativo a 6 campi `data/sessions/fib_session_calendar.csv` rispettando esattamente lo schema del task card §3.5 (epoch_id, start_date, end_date, session_open_local, session_close_local, timezone). Eventuali metadati di provenienza (URL fonte, data consultazione ISO, note di ambiguita') vanno SOLO in `data/sessions/README.md`, lasciando il CSV pulito."

Razionale: il Developer subagente non ha tools web (memory `project-developer-subagent-no-web`); inoltre le date sono gia' state verificate dall'Orchestratore nel passo STEP 2 contro le fonti ufficiali Borsa Italiana. Una doppia verifica da parte del Developer non aggiungerebbe valore e introdurrebbe rischio di divergenza fra dati in ACTIVE_TASK e dati nel CSV. Vedi memory `project-orchestrator-input-is-authoritative`.

### Sintesi metadati ambiguita' per il Developer (riassunto README)

Il `data/sessions/README.md` deve riportare esplicitamente:
- per **E1**, **E2**: gli orari di queste epoche sono parzialmente derivati per inferenza (orari E1 verificati solo nel 2000; transizioni intermedie 09:15→09:00 e 17:30→17:40 non documentate da un comunicato ufficiale specifico)
- la **data 2010-11-08** come confine E1/E2 e' inferita dalla migrazione SOLA (data documentata) ma non confermata come effettiva data di cambio orari
- le **date 2015-11-23**, **2017-07-03**, **2020-02-17** sono confermate da comunicati Borsa Italiana ufficiali
- il calendario completo va riesaminato in CAP-DATA-02 (richiesta tecnica a Portara) o in PHASE-B (acquisizione storico), che potrebbe fornire epoche piu' precise via roll log Portara

---

## Note tecniche T2/T3

### T2 — File `_build_order.yaml` citato nel task card §5

Il task card §5 (Definition of Done) cita "_build_order.yaml (o equivalente) aggiornato: Parte 8 aggiunta in coda al corpo principale...". Il file `_build_order.yaml` **NON esiste** in questo repo (verificato con Glob al 2026-05-27 commit `f497022`). Il file "equivalente" che il progetto ha sempre usato e' `docs/methodology_v2/00_indice.md`. La condizione 4 della checklist di chiusura sessione (vedi `.claude/CLAUDE.md`) gia' richiede l'aggiornamento di `00_indice.md`.

**Implicazione per il Developer**: il riferimento "_build_order.yaml (o equivalente)" del task card §5 va letto come riferimento a `docs/methodology_v2/00_indice.md`. NON creare un nuovo file `_build_order.yaml`. Aggiornare `00_indice.md` aggiungendo la sezione "Parte 8 — ..." in coda al corpo principale e prima delle Appendici, con stato iniziale "IN REVIEW" (poi PASS Review v(N) con hash a chiusura sessione, come da decisione (d) ratificata).

### T3 — Directory `data/sessions/` non esistente

Il task card §3.5 richiede produzione di `data/sessions/fib_session_calendar.csv`. La directory `data/sessions/` **NON esiste** nel repo (verificato con Glob al 2026-05-27 commit `f497022`).

**Implicazione per il Developer**: creare la directory `data/sessions/` come parte del deliverable §3.5 (in PowerShell: `New-Item -ItemType Directory -Force data/sessions`). Produrre dentro la directory due file:
- `fib_session_calendar.csv` — CSV normativo a 6 campi conforme allo schema task card §3.5 (epoch_id, start_date, end_date, session_open_local, session_close_local, timezone)
- `README.md` — note non normative su fonti, ambiguita' (vedi "Sintesi metadati ambiguita' per il Developer" sopra)

---

## 0. Note di integrazione nel doc v2

- CAP-DATA-01 è una **Parte normativa del doc v2**, allo stesso rango delle Parti già scritte (1–7). Non è appendice, non è documento esterno, non è capitolo intercalato.
- Si aggiunge **in coda** al corpo principale del doc v2, prima della Parte 9 (Appendice). **Non richiede rinumerazione** di nessuna Parte precedente.
- Deve fare **riferimenti incrociati espliciti** alle Parti già scritte del doc v2 dove pertinente, in particolare:
  - all'invariante `research semantics = runtime semantics` (Parte sulle decisioni normative hard-locked)
  - alla gap semantics (Parte sull'execution gate / runtime)
  - al protocollo OOS, purge ed embargo (Parte sulla validazione)
  - al layer di covarianza cross-index (Parte sulla covarianza condizionale multi-indice)
- I riferimenti incrociati usano i numeri di Parte definitivi del doc v2; se durante la stesura emergesse un'ambiguità sulla numerazione, Development chiede chiarimento prima di proseguire (non assume).

---

## 1. Obiettivo

Congelare nel doc metodologico v2 la convenzione ufficiale di:
- scelta della serie storica per training GA
- metodo di back-adjustment e ricostruzione delle convenzioni alternative
- gestione del rollover e filtro pre-expiry
- gestione della griglia temporale 1-min con barre mancanti
- timeline delle sessioni FIB per epoca
- esclusione esplicita di fonti alternative (MIB cash, vendor diversi da Portara/CQG)
- replica della convenzione sul layer cross-index (DAX, ESTX50, ES)

L'output di questa Parte è normativo: tutto il preprocessing dei dati storici, in tutte le fasi successive del progetto, deve rispettarlo. Qualunque deviazione successiva richiede ritorno al Planner.

---

## 2. Input richiesti

- `ENGINE_ALGO_INTEGRATO_HARD_LOCKED.pdf` (capitoli 5, 6, 9, 12, 13, 14, 23, 24, 30)
- Parti 1–7 del nuovo doc v2 già scritte (per coerenza terminologica e riferimenti incrociati)
- Scambio email con Portara del 15/05/2026 (sintesi sotto)
- Roadmap del progetto: PHASE-1 FIB-only, PHASE-2 cross-index (DAX+ESTX50+ES)

### Sintesi vincoli operativi noti da Portara
- Serie disponibile dal 1995 (FIB pieno, non miniFIB)
- Back-adjustment default: Panama-additive su base settle
- Disponibili in CSV: `Date, Time, O, H, L, C, V, TickCount, ContractName, UnadjustedClose, RollSpread, CumulativeSpread` + roll log allegato
- Roll rule default: 3 giorni prima della scadenza (da chiarire se calendario o trading — vedi CAP-DATA-02)
- Timestamps default: SOB exchange time
- Barre senza trade: omesse (no zero-volume bar fill)
- Volume reale dal 2000 in poi
- Nessuna marcatura di sessione nel file

---

## 3. Acceptance criteria

La Parte 8 è accettata se contiene, congelato in forma normativa, **tutti** i punti seguenti.

### 3.1 Scelta della serie ufficiale di training
- **Decisione:** FIB pieno back-adjusted Portara/CQG come unica fonte ufficiale per il training del GA su strumento target
- **Razionale documentato:**
  - rendimenti log e struttura di volatilità di FIB e miniFIB sono numericamente equivalenti (stesso sottostante, stesso tick, stesso exchange)
  - FIB ha storia di liquidità più profonda e continua del miniFIB sull'intero periodo 1995–oggi
  - esecuzione su miniFIB è solo questione di moltiplicatore, non altera la semantica del segnale
- **Esclusione esplicita di MIB cash come fonte training**, con razionale ancorato al principio `research semantics = runtime semantics`: cash differisce su orari, microstruttura, basis, gap di apertura e non corrisponde allo strumento di esecuzione

### 3.2 Convenzione di back-adjustment ufficiale
Vanno congelate **tre serie derivabili** dal file Portara, ciascuna con uso specifico:

| Serie | Formula | Uso |
|---|---|---|
| **Ratio-adjusted (ufficiale per training)** | `P_t = P_t^unadj × Π_{r∈rolls, r<t} (P_r^next / P_r^curr)` | input a tutti i modelli che operano su rendimenti log (GARCH/EGARCH/DCC/quantili condizionali, survival hazard) |
| **Panama-additive (ufficiale per audit monetario)** | fornita direttamente da Portara come back-adjusted settle | audit PnL in €/punto, sanity check visivo, replay |
| **Unadjusted concatenata** | `UnadjustedClose` riga per riga, con marker di roll | sanity check contratto-per-contratto, validazione recente |

Va specificato che la **ratio-adjusted** è ricostruita in preprocessing da `UnadjustedClose + RollSpread + roll log`, non richiesta direttamente a Portara (loro forniscono solo Panama).

### 3.3 Filtro pre-expiry
- **Regola:** rimozione delle ultime **N giorni di trading** prima della scadenza di ciascun contratto dal training set
- **Default normativo:** N = 3 giorni di trading (allineato al roll Portara, da confermare in CAP-DATA-02)
- **Razionale documentato:** il basis tra front e next month diverge meccanicamente nell'ultima settimana, contaminando i quantili condizionali e la dinamica EGARCH; il filtro elimina la finestra in cui la serie back-adjusted è strutturalmente meno informativa
- **Algoritmo formale:** dato `roll_log[k] = (contract_k, expiry_date_k, roll_date_k)`, esclusione delle barre con `bar_time ∈ [trading_day(roll_date_k - N), roll_date_k]` per ogni `k`
- Va specificato che il filtro si applica a **training** e **outer valid**, ma **non** a outer test (per non alterare la verità OOS) — coerente con la Parte sul protocollo OOS del doc v2

### 3.4 Preprocessor griglia 1-min regolare
- **Problema:** Portara omette barre senza trade. La specifica del doc v2 assume input causalmente uniforme.
- **Soluzione normativa:** preprocessor che produce griglia 1-min regolare su `[session_open, session_close]` per ogni giornata di sessione, con per ogni minuto mancante:
  - `Open = High = Low = Close = Close_{t-1}` (forward-fill)
  - `Volume = 0`
  - `TickCount = 0`
  - `bar_synthetic = True` (flag obbligatorio nello schema)
- **Regola di uso a valle:**
  - features di volatilità (EGARCH, Realized GARCH measurement equation) calcolate **solo su barre con `bar_synthetic = False`** ma con timestamp allineato alla griglia uniforme per il time-indexing
  - features di prezzo (livelli, distanze da zone) usano la griglia uniforme completa
  - il flag `bar_synthetic` entra nel feature schema persistito nel bundle frozen
- Va specificato che il forward-fill su `Close` è una convenzione, **non** un'inferenza di path: nessun touch può essere dichiarato su una `bar_synthetic` (coerente con la gap semantics della Parte sull'execution gate del doc v2)

### 3.5 Timeline ufficiale delle sessioni FIB
Va prodotta una **tabella per epoca** con date di switch verificate dalla fonte ufficiale (`borsaitaliana.it`). Struttura minima:

| Epoca | Periodo | Continuous trading | Note |
|---|---|---|---|
| E1 | 1995-XX-XX → 20YY-XX-XX | HH:MM–HH:MM CET | sessione singola |
| E2 | 20YY-XX-XX → 20YY-XX-XX | HH:MM–HH:MM CET | introduzione sessione serale |
| ... | ... | ... | ... |
| En | 20YY-XX-XX → presente | 09:00–22:00 CET | sessione attuale |

**Le date esatte vanno verificate da fonte ufficiale durante l'esecuzione del task, non assunte.** Tutti i timestamp dichiarati `CET` includono la conversione automatica CEST quando in vigore (per coerenza con la Parte sulla semantica eventi/timestamp del doc v2).

Output: tabella nella Parte 8 + file `data/sessions/fib_session_calendar.csv` con schema `(epoch_id, start_date, end_date, session_open_local, session_close_local, timezone)`.

### 3.6 Convenzione cross-index (PHASE-2)
Stessa convenzione (ratio-adjusted ufficiale, Panama per audit, filtro N=3, preprocessor griglia 1-min, calendario sessione per epoca) applicata identicamente a:
- **DAX** (FDAX, Eurex)
- **EuroStoxx 50** (FESX, Eurex)
- **S&P 500 mini** (ES, CME)

Va specificato esplicitamente che:
- ciascuna serie ha il **proprio** roll calendar e calendario sessione
- la stima DCC/ADCC/cDCC opera su **timestamp intersezione** delle griglie regolari (coerente con la Parte sulla covarianza condizionale multi-indice del doc v2), non su forward-fill cross-asset
- i giorni di festività di un singolo exchange escludono quella riga dal calcolo cross-index per quel giorno

**Vincolo di fasizzazione (PHASE-1 vs PHASE-2):** va dichiarato esplicitamente nella Parte 8 che la convenzione cross-index è normativa, ma la sua attivazione operativa è prevista in PHASE-2 del progetto. PHASE-1 (FIB-only) è una fasizzazione esplicita e dichiarata, non una semplificazione silenziosa. Va elencato esplicitamente cosa la fasizzazione PHASE-1 implica:
- `sigma_sys` cross-index ridotta a `sigma_local` (degradazione documentata)
- feature tensor privo dei canali cross-index obbligatori del doc v2 (regime di funzionamento esplicito)
- `S_xidx` dello score strutturale non calcolabile, quinta famiglia del catalogo target ("proiezioni cross-index coerenti") esclusa
- report per regime privo della riga "Contagio cross-index"

La fasizzazione **non sostituisce** la spec, la istanzia in modo parziale per PHASE-1 con costi noti.

### 3.7 Procedura di sanity validation
- Su una finestra di **ultimi 18–24 mesi**, replicare la pipeline contratto-per-contratto sulla serie **unadjusted concatenata** (senza adjustment)
- Confrontare le seguenti metriche tra `ratio-adjusted` e `unadjusted-stitched`:
  - distribuzione dei rendimenti log a 1-min, 5-min, 60-min (quantili 1/5/25/50/75/95/99)
  - autocorrelazione dei rendimenti al lag 1, 5, 30
  - autocorrelazione dei rendimenti quadrati al lag 1, 5, 30
  - σ giornaliera realized
- **Criterio di accettazione:** differenze entro **3σ bootstrap** per ciascuna metrica. Discrepanze superiori richiedono indagine prima del go-ahead training
- **Out-of-scope di questo task:** l'implementazione del check (è task separato di Development, vivrà in FASE-D del roadmap); va specificata solo la procedura normativa

### 3.8 Esclusione esplicita di fonti alternative
Va inserita una sottosezione di chiusura che elenca cosa **non** è ammesso come fonte training:
- MIB cash (razionale: invariante `research = runtime`)
- Dati vendor diversi da Portara/CQG senza nuovo task Planner
- Mix di vendor diversi per cross-index (DAX da X, ESTX50 da Y) — tutto Portara/CQG
- Dati ricostruiti da CFD broker
- Dati intraday liberi (Yahoo, Investing, ecc.) — non usabili nemmeno come benchmark di confronto, coerente con la data-matching policy di Portara

---

## 4. Out-of-scope

- Implementazione Python del preprocessor (è task Development separato a valle, FASE-D del roadmap)
- Download/parsing del CSV Portara (è task Development separato, dopo l'acquisto, FASE-B del roadmap)
- Schema database / persistenza (è task separato, FASE-D)
- Verifica empirica dei dati (richiede dati acquistati — quindi successiva a CAP-DATA-02 e a FASE-B)
- Scelta di N diverso da 3 nel filtro pre-expiry — il default è 3, eventuali varianti sono ricerca esplorativa
- Modifica di Parti già scritte del doc v2 (1–7): se durante la stesura di Parte 8 emergesse un conflitto con quelle Parti, **stop e ritorno al Planner**, non auto-modifica
- Stesura di CAP-DATA-02 (è task gemello operativo, vive in `docs/operations/`, non in questa Parte)

---

## 5. Definition of Done

**Nota Orchestratore (decisione (a) ratificata)**: push diretto a `origin/main` (no feature branch, no PR — deroga task card §5). Aggiornato di conseguenza.

- File `docs/methodology_v2/CAP_08_parte_8.md` creato e completo degli otto punti 3.1–3.8 (naming β2 ratificato, decisione (b)+(c))
- File `data/sessions/fib_session_calendar.csv` creato con tabella sessioni per epoca, dati copiati dalla sezione "Dati di input recuperati dall'Orchestratore" sopra
- File `data/sessions/README.md` creato con note non normative su fonti, URL, ambiguita' (vedi "Sintesi metadati ambiguita'" sopra)
- `docs/methodology_v2/00_indice.md` (vedi nota T2) aggiornato: Parte 8 aggiunta in coda al corpo principale, immediatamente prima dell'Appendice (che è/diventa Parte 9). Stato iniziale "IN REVIEW", poi PASS Review v(N) a chiusura sessione. Nessuna rinumerazione di Parti precedenti.
- Tutti i riferimenti incrociati a Parti 1–7 verificati e citati con il numero di Parte definitivo (vedi Planner subagente per la mappatura eredita)
- `reports/REPORT_CAP_08.md` generato secondo template supervisore (naming β2 ratificato, decisione (b)+(c)); contiene cosa è stato deciso, cosa è stato escluso, rollback criteria per ciascuna decisione
- `tasks/DEV_STATUS.md` aggiornato a `READY_FOR_REVIEW`
- Commit + push diretto a `origin/main`

---

## 6. Rollback criteria

Ciascuna delle 8 decisioni del §3 ha un proprio criterio di reversibilità documentato nel `reports/REPORT_CAP_08.md`. In particolare:
- decisione 3.2 (ratio-adjusted come ufficiale): reversibile se la sanity validation §3.7 rileva discrepanze >3σ → ritorno al Planner
- decisione 3.3 (N=3 filtro pre-expiry): reversibile se Portara conferma roll rule diversa in CAP-DATA-02 → aggiornamento minore di Parte 8 senza ritorno al Planner
- decisione 3.4 (forward-fill griglia 1-min): non reversibile senza nuovo task Planner (è invariante semantico, ancorato alla gap semantics del doc v2)
- decisione 3.6 (fasizzazione PHASE-1/PHASE-2): non reversibile senza nuovo task Planner (è scelta di roadmap del progetto, non scelta tecnica isolata)
