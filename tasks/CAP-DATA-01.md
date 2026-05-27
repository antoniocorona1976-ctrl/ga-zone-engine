# CAP-DATA-01 — Convenzione dati storici e politica di rollover

**Status:** QUEUED (parte solo dopo chiusura Parte 7 + esito PASS da Review)
**Tipo:** Parte 8 del nuovo doc metodologico v2 (`docs/methodology_v2/`)
**Posizione nel documento:** Parte 8, immediatamente prima dell'Appendice (che diventa Parte 9)
**Predecessor:** Parte 7
**Successor:** Parte 9 (Appendice)
**Task operativo gemello (fuori doc metodologico):** CAP-DATA-02 — Specifica della richiesta tecnica a Portara
**Owner deliverable:** Development agent (Claude Code)
**Supervisore:** AC

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

- File `docs/methodology_v2/parte_08_convenzione_dati_storici.md` creato e completo degli otto punti 3.1–3.8
- File `data/sessions/fib_session_calendar.csv` creato con tabella sessioni per epoca, date verificate da `borsaitaliana.it`
- `_build_order.yaml` (o equivalente) aggiornato: Parte 8 aggiunta in coda al corpo principale, immediatamente prima dell'Appendice (che è/diventa Parte 9). Nessuna rinumerazione di Parti precedenti.
- Tutti i riferimenti incrociati a Parti 1–7 verificati e citati con il numero di Parte definitivo
- `reports/REPORT_CAP_DATA_01.md` generato secondo template supervisore (cosa è stato deciso, cosa è stato escluso, rollback criteria per ciascuna decisione)
- ACTIVE_TASK.md aggiornato: CAP-DATA-01 → DONE
- Commit firmato sul branch `feature/parte-08-dati`, PR aperta, attesa Review

---

## 6. Rollback criteria

Ciascuna delle 8 decisioni del §3 ha un proprio criterio di reversibilità documentato nel `REPORT_CAP_DATA_01.md`. In particolare:
- decisione 3.2 (ratio-adjusted come ufficiale): reversibile se la sanity validation §3.7 rileva discrepanze >3σ → ritorno al Planner
- decisione 3.3 (N=3 filtro pre-expiry): reversibile se Portara conferma roll rule diversa in CAP-DATA-02 → aggiornamento minore di Parte 8 senza ritorno al Planner
- decisione 3.4 (forward-fill griglia 1-min): non reversibile senza nuovo task Planner (è invariante semantico, ancorato alla gap semantics del doc v2)
- decisione 3.6 (fasizzazione PHASE-1/PHASE-2): non reversibile senza nuovo task Planner (è scelta di roadmap del progetto, non scelta tecnica isolata)
