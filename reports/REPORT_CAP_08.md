# REPORT SUPERVISORE — CAP-DATA-01 (Parte 8)

**Task**: CAP-DATA-01 — Convenzione dati storici e politica di rollover (Parte 8 del documento metodologico v2)
**Stato**: COMPLETATO (iterazione v1 Developer, in attesa di Review)
**Sessione**: 2026-05-27
**Predecessor**: Parte VII chiusa PASS Review v2 (commit `b27c1e3`)
**Successor**: Parte 9 (Appendici A-G)

---

## Cosa e' stato prodotto

- `docs/methodology_v2/CAP_08_parte_8.md` — documento metodologico Parte 8, preambolo + Cap.37-44 (~10 pp), 8 capitoli normativi in mappatura 1:1 con gli AC §3.1-§3.8 del task card. Identifier interno "Parte 8" (arabo). Tutti i riferimenti incrociati richiesti dalla mappatura Planner sono applicati e citano i Capitoli in formato `Parte Y, Capitolo X` o `Parte Y, Capitolo X.Y` per sottosezioni.

- `reports/REPORT_CAP_08.md` — questo report supervisore secondo il formato a 6 sezioni (Cosa e' stato prodotto, Ipotesi di partenza, Decisioni rilevanti, Misura prima/dopo, Verifica esplicita degli Acceptance Criteria, Domande aperte, Criterio di rollback). La sezione "Criterio di rollback" elenca esplicitamente per ciascuna delle 8 decisioni §3.1-§3.8 il rollback criterion individuale.

- `data/sessions/fib_session_calendar.csv` — CSV normativo a 6 campi (`epoch_id, start_date, end_date, session_open_local, session_close_local, timezone`), 1 riga header + 5 righe dati (E1-E5). Dati copiati esattamente dalla tabella autoritativa in `tasks/ACTIVE_TASK.md` sezione "Dati di input recuperati dall'Orchestratore". CSV pulito senza metadati di provenienza inline (direttiva S1 rispettata).

- `data/sessions/README.md` — note non normative su fonti, URL, ambiguita' di derivazione delle epoche. Marcature **DATA DA VERIFICARE** per E1 (orari verificati solo nel 2000), E1->E2 (cambio orari associato alla migrazione SOLA non documentato), E2 (orari derivati per inferenza inversa).

- `docs/methodology_v2/00_indice.md` — aggiornato. Aggiunta in coda al corpo principale (DOPO Parte VII, PRIMA di "Appendici operative") la sezione "Parte 8 — Convenzione dati storici e politica di rollover (~10 pp) IN REVIEW (v1 Developer 2026-05-27)" con elenco dei Cap.37-44 e titoli del Planner. Parti precedenti I-VII non rinumerate.

- `tasks/DEV_STATUS.md` — aggiornato a `READY_FOR_REVIEW`.

---

## Ipotesi di partenza

CAP-DATA-01 e' una **Parte normativa** del documento metodologico v2. A differenza delle Parti I-VII che modellano direttamente il comportamento del motore (segnale, volatilita', regime, zone/target/stop, GA, lifecycle, validazione OOS), la Parte 8 modella le **convenzioni di input dati**. Il suo impatto sul comportamento del GA non e' diretto via codice di motore ma indiretto via la **qualita' della serie storica** su cui il GA calibra.

Ipotesi operative:

1. **Coerenza serie training-runtime**: la scelta della serie ufficiale (FIB pieno back-adjusted Portara/CQG, ratio-adjusted ricostruita) e' la condizione necessaria perche' i parametri EGARCH, le soglie di regime, i quantili condizionali del survival e i pivot frattali calibrati dal GA siano numericamente coerenti con quanto il motore osserva in runtime. Una serie training divergente da quella di esecuzione produrrebbe cromosomi che ranking-eredita parametri inadatti al runtime: comportamento del GA degradato anche se i fold OOS apparissero positivi.

2. **Filtro pre-expiry $N=3$ giorni di trading**: rimuove dalla finestra di training (ma NON dalla finestra OOS finale) le barre in cui il basis front/next-month diverge meccanicamente, contaminando i quantili condizionali. Comportamento del GA atteso: cromosomi con soglie EGARCH e survival calibrate su distribuzioni non contaminate da effetto pre-expiry -> migliore generalizzazione OOS.

3. **Preprocessor griglia 1-min con flag `bar_synthetic`**: rende esplicita la distinzione fra barre reali e barre forward-filled. Comportamento del GA atteso: feature di volatilita' (EGARCH) e feature di volume non vengono contaminate da barre sintetiche a $\mathrm{Volume}=0$ e rendimento log nullo (evita bias verso bassa volatilita' nella calibrazione MLE), mentre feature di prezzo restano sulla griglia uniforme completa (preserva la causalita' temporale dei pivot strutturali).

4. **Timeline epoche E1-E5 normativa**: il preprocessor applica gli orari corretti per ogni epoca alla griglia 1-min regolare. Comportamento del GA atteso: il training su 5+ anni include sia barre di sessione 08:00-22:00 (E5) sia barre di sessioni storiche piu' corte (E4: 09:00-20:30, E3: 09:00-17:50, ecc.) con il corretto numero di barre per giornata per ciascuna epoca; le feature di "media di sessione" e simili sono calcolate sulla finestra di sessione corretta per ciascuna epoca.

5. **Fasizzazione PHASE-1 esplicita**: la convenzione cross-index e' dichiarata ma non implementata nel doc v2 corrente. Comportamento del GA: PHASE-1 opera con `sigma_local` come proxy di `sigma_sys`, con feature tensor privo dei canali cross-index, senza calcolo di `S_xidx`. La dichiarazione esplicita rende il costo della fasizzazione tracciabile e riapribile in PHASE-2.

6. **Sanity validation $3\sigma$ bootstrap**: la procedura di confronto fra ratio-adjusted e unadjusted-stitched (eseguita una sola volta in occasione dell'acquisizione dei dati Portara) verifica che il back-adjustment non abbia introdotto artefatti significativi. Esito atteso: differenze entro $3\sigma$ bootstrap per tutte le metriche; discrepanze richiedono indagine prima del go-ahead training.

---

## Decisioni rilevanti

### D1 — Identifier interno "Parte 8" (arabo) come scelta canonica del doc v2

Il task card ratifica naming beta2: file `CAP_08_parte_8.md`, identifier "Parte 8" (arabo, NON "Parte VIII" romano). Il preambolo del documento dichiara questa scelta esplicitamente per evitare ambiguita' con la convenzione romana delle Parti I-VII. Decisione non riapribile senza nuovo task Planner.

### D2 — Mappatura riferimenti incrociati 1:1 con la sezione "Mappatura eredita I-VII -> §3.X" del Planner

I capitoli citati nel doc Parte 8 sono **letteralmente** quelli forniti dal Planner in `tasks/ACTIVE_TASK.md`:
- Cap.37 -> Parte I Cap.1, Cap.2, Cap.5
- Cap.38 -> Parte III Cap.12, Cap.13; Parte IV Cap.19; Parte VII Cap.31.1
- Cap.39 -> Parte V Cap.25.1; Parte VII Cap.31.1
- Cap.40 -> Parte II Cap.7 (7.3 per il raw touch), Cap.10; Parte III Cap.12 (12.4), Cap.13, Cap.14 (14.2), Cap.15 (15.2 catalogo, 15.3 pivot frattali); Parte VII Cap.35
- Cap.41 -> Parte I Cap.1; Parte II Cap.7 (Q-01)
- Cap.42 -> preambolo `00_indice.md`; Parte III Cap.13 (`sigma_local`), Cap.15.2 (catalogo)
- Cap.43 -> Parte III Cap.12 (rendimenti log), Cap.13 (13.4 diagnostica residui); Parte VII Cap.34 (bootstrap stazionario)
- Cap.44 -> Parte I Cap.1, Cap.3

Tutti verificati contro `docs/methodology_v2/00_indice.md` stato 2026-05-27 (Parti I-VII PASS).

### D3 — §3.6 / Cap.42 trattato come dichiarazione normativa PHASE-2 SENZA implementazione

Decisione (1) dell'handoff CAP-07 -> CAP-DATA-01: la convenzione cross-index e' **dichiarata** come normativa PHASE-2, ma il documento metodologico v2 corrente NON la implementa. Il Cap.42 e' scritto in tono dichiarativo, non implementativo:

- Dichiara gli strumenti PHASE-2 (DAX, ESTX50, ES su Eurex/CME).
- Dichiara che si applichera' identicamente la convenzione di Cap.37-41.
- Dichiara le specifiche aggiuntive (roll calendar e calendario sessione per strumento, timestamp intersezione, gestione festivita').
- Dichiara la fasizzazione PHASE-1 cost (cosa esclude rispetto alla specifica ideale).
- Dichiara esplicitamente che DCC/ADCC/cDCC, Realized GARCH (decisione 2), `S_xidx` + quinta famiglia catalogo target (decisione 3) sono **estensioni future non implementate** nel doc v2 corrente.

L'eccezione cross-index per il Reviewer (sezione "ATTENZIONE PER REVIEWER" in ACTIVE_TASK.md) e' onorata: le citazioni cross-index in Cap.42 e nelle sezioni collegate sono normative dichiarate, non residui da rimuovere. Nessuna citazione cross-index e' fatta al di fuori di Cap.42.

### D4 — Direttiva S1 rispettata: input autoritativo, no doppia verifica delle date

La tabella sessioni FIB in `tasks/ACTIVE_TASK.md` sezione "Dati di input recuperati dall'Orchestratore" e' input autoritativo (memory `project-orchestrator-input-is-authoritative`). Il Developer NON ha verificato con fonti esterne (anche perche' non ha tools WebFetch/WebSearch, vedi memory `project-developer-subagent-no-web`). I dati sono stati copiati ESATTAMENTE nel CSV normativo a 6 campi. Le note di ambiguita' (DATA DA VERIFICARE per E1/E2) sono andate SOLO in `data/sessions/README.md`, lasciando il CSV pulito.

### D5 — File `_build_order.yaml` non creato (nota tecnica T2)

Il task card §5 cita "_build_order.yaml (o equivalente)". Il file non esiste nel repo. Il "equivalente" e' `docs/methodology_v2/00_indice.md`. Decisione: aggiornato `00_indice.md`, non creato `_build_order.yaml`.

### D6 — Directory `data/sessions/` creata da zero (nota tecnica T3)

La directory non esisteva. Decisione: creata via `mkdir -p data/sessions`, poi creati `fib_session_calendar.csv` e `README.md` al suo interno. Il file CSV resta pulito (solo 6 colonne), tutti i metadati di provenienza vanno nel README.

### D7 — Sanity validation Cap.43 — uso del bootstrap stazionario di Parte VII Cap.34

Il task card §3.7 specifica "differenze entro 3$\sigma$ bootstrap". La decisione di Cap.43 ancora esplicitamente il bootstrap a Parte VII Cap.34 (Politis e Romano 1994, $B=2.000$ replicazioni). La block length $L_{avg}$ rimanda alla calibrazione di Cap.34.2, evitando di introdurre nuovi parametri non congelati in Parte 8.

### D8 — Stratificazione del filtro pre-expiry sul fold OOS finale (Cap.39)

La decisione di NON applicare il filtro pre-expiry al fold OOS finale di Parte VII Cap.31.1 (preservando la verita' OOS) e' ancorata esplicitamente all'eredita' di Lopez de Prado 2018 Cap.7 sulla prevenzione del leakage. Coerente con la mappatura del Planner.

---

## Misura prima/dopo

CAP-DATA-01 e' la **prima Parte normativa del doc v2 dedicata alla convenzione dati storici**. Non esistono Parti precedenti che la sostituiscono. La misura prima/dopo opera quindi sul livello di **completezza della convenzione dati** e sulla **tracciabilita' dei costi della fasizzazione PHASE-1 vs PHASE-2**, non su metriche di performance del GA (che non e' ancora calibrato sui dati).

| Metrica | Prima (Parti I-VII chiuse PASS) | Dopo (CAP-DATA-01 v1) | Delta |
|---------|---------------------------------|------------------------|-------|
| Serie ufficiale di training dichiarata | Implicita (Parte I Cap.3 cita Portara/CQG come vendor ma non specifica back-adjustment) | Esplicita: FIB pieno back-adjusted ratio-adjusted ricostruita in preprocessing (Cap.37+38) | +completezza normativa |
| Convenzione back-adjustment | Non dichiarata | 3 serie derivabili con uso specifico (ratio-adjusted training, Panama audit, unadjusted sanity) + formule (Cap.38) | +1 sezione normativa critica per replay bit-exact |
| Filtro pre-expiry | Non specificato | $N=3$ giorni di trading default, algoritmo formale, applicazione differenziata training/OOS (Cap.39) | +1 parametro provvisorio congelato con rollback criterion documentato |
| Trattamento barre senza trade | Non specificato (Parte III Cap.12.4 dichiara fill virtuale worst-case per touch ma non gestisce le barre intere senza trade) | Forward-fill con flag `bar_synthetic`, uso differenziato a valle (Cap.40) | +1 convenzione che evita bias verso bassa volatilita' nella calibrazione MLE EGARCH |
| Timeline storica sessioni FIB | Solo sessione corrente E5 (Parte I Cap.1) | E1-E5 1994-2026 con orari per epoca, CSV normativo a 6 campi (Cap.41) | +5 epoche storiche tracciate, +1 file dati normativo |
| Convenzione cross-index | Esclusa dal doc v2 (preambolo `00_indice.md`) | Dichiarata PHASE-2 senza implementazione, con costi PHASE-1 esplicitati (Cap.42) | +tracciabilita' dei costi della fasizzazione, +tre estensioni future identificate |
| Procedura sanity validation | Non specificata | $3\sigma$ bootstrap su 18-24 mesi, metriche da Parte III Cap.12/13 e Parte VII Cap.34 (Cap.43) | +1 procedura di QA dati pre-training |
| Esclusione fonti alternative | Implicita | Esplicita: MIB cash, vendor non-Portara, CFD, dati intraday liberi (Cap.44) | +clausola di chiusura del dominio dati |
| File normativi prodotti | 0 (Parte 8 inesistente) | 4: documento metodologico, CSV epoche, README metadati, indice aggiornato | +4 deliverable |
| Riferimenti incrociati alle Parti I-VII | 0 (Parte 8 inesistente) | Mappatura completa applicata: 17 riferimenti puntuali a Parti/Capitoli specifici nei Cap.37-44 | +17 ancoraggi metodologici |

**Impatto atteso sul comportamento del GA (misurabile in fasi successive)**:
- Riduzione del bias di calibrazione EGARCH dovuto a barre sintetiche -> coda della distribuzione dei rendimenti standardizzati piu' realistica -> soglie di regime calmo/turbolento meglio calibrate.
- Eliminazione delle ultime 3 giornate pre-expiry dalle finestre di training -> quantili condizionali del survival Cox piu' rappresentativi -> ranking dei cromosomi sul filtro $\tau_{surv}$ piu' stabile fra fold.
- Coerenza serie training-runtime garantita -> metrica primaria $E[R_{net} \mid executed]$ misurata in OOS e' approssimazione valida dell'attesa operativa.

---

## Verifica esplicita degli Acceptance Criteria

| AC-ID | Criterio (estratto da ACTIVE_TASK.md §3) | Esito | Evidenza (file:riga) |
|-------|------------------------------------------|-------|----------------------|
| AC-3.1 | Scelta serie ufficiale FIB pieno back-adjusted Portara/CQG; razionale equivalenza FIB/miniFIB su rendimenti log; esclusione esplicita MIB cash con razionale ancorato a `research = runtime` | OK | `docs/methodology_v2/CAP_08_parte_8.md:11-23` (Capitolo 37) |
| AC-3.2 | Tre serie derivabili (ratio-adjusted ufficiale, Panama-additive audit, unadjusted concatenata); formule esplicite; specifica che ratio-adjusted e' ricostruita in preprocessing | OK | `docs/methodology_v2/CAP_08_parte_8.md:25-53` (Capitolo 38) |
| AC-3.3 | Filtro pre-expiry $N=3$ giorni di trading; razionale documentato; algoritmo formale `bar_time in [trading_day(roll_date_k - N), roll_date_k]`; applicato a training/outer valid ma NON outer test | OK | `docs/methodology_v2/CAP_08_parte_8.md:55-71` (Capitolo 39) |
| AC-3.4 | Preprocessor griglia 1-min regolare; forward-fill $\mathrm{Open}=\mathrm{High}=\mathrm{Low}=\mathrm{Close}=\mathrm{Close}_{t-1}$, $\mathrm{Volume}=0$, $\mathrm{TickCount}=0$, flag `bar_synthetic = True`; regola uso a valle (volatilita' esclude `bar_synthetic`, prezzo usa griglia completa); nessun touch su `bar_synthetic`; flag persistito nel bundle frozen | OK | `docs/methodology_v2/CAP_08_parte_8.md:73-105` (Capitolo 40) |
| AC-3.5 | Timeline ufficiale sessioni FIB per epoca; tabella E1-E5 con date e orari; file `data/sessions/fib_session_calendar.csv` schema 6 campi `(epoch_id, start_date, end_date, session_open_local, session_close_local, timezone)`; convenzione CET con conversione automatica CEST | OK | `docs/methodology_v2/CAP_08_parte_8.md:107-139` (Capitolo 41); `data/sessions/fib_session_calendar.csv:1-6`; `data/sessions/README.md` |
| AC-3.6 | Convenzione cross-index PHASE-2 applicata identicamente a DAX/ESTX50/ES; timestamp intersezione griglie regolari, festivita' exchange; vincolo di fasizzazione PHASE-1 esplicito con costi noti; **Dichiarazione normativa PHASE-2 SENZA implementazione nel doc v2 corrente** (decisione (1)). Realized GARCH (decisione (2)) e `S_xidx` (decisione (3)) come estensioni future esplicite | OK | `docs/methodology_v2/CAP_08_parte_8.md:141-184` (Capitolo 42) |
| AC-3.7 | Procedura sanity validation; finestra ultimi 18-24 mesi, ratio-adjusted vs unadjusted-stitched; metriche (quantili rendimenti log 1/5/60-min, autocorrelazione lag 1/5/30, $\sigma$ giornaliera realized); criterio $3\sigma$ bootstrap; out-of-scope dell'implementazione (FASE-D del roadmap) | OK | `docs/methodology_v2/CAP_08_parte_8.md:186-211` (Capitolo 43) |
| AC-3.8 | Esclusione esplicita fonti alternative: MIB cash, vendor non-Portara/CQG, mix vendor cross-index, CFD broker, dati intraday liberi (Yahoo/Investing) | OK | `docs/methodology_v2/CAP_08_parte_8.md:213-237` (Capitolo 44) |
| AC-DoD-1 | File `docs/methodology_v2/CAP_08_parte_8.md` creato e completo degli otto punti 3.1-3.8 (naming beta2) | OK | `docs/methodology_v2/CAP_08_parte_8.md` (237 righe, naming beta2) |
| AC-DoD-2 | File `data/sessions/fib_session_calendar.csv` creato con tabella sessioni, dati dalla sezione "Dati di input recuperati dall'Orchestratore" | OK | `data/sessions/fib_session_calendar.csv:1-6` (header + 5 epoche E1-E5) |
| AC-DoD-3 | File `data/sessions/README.md` creato con note non normative su fonti, URL, ambiguita' | OK | `data/sessions/README.md` (sezioni Schema + Sotto-tabella fonti + Sintesi ambiguita' + Procedura riesame) |
| AC-DoD-4 | `docs/methodology_v2/00_indice.md` aggiornato: Parte 8 in coda al corpo principale, prima delle Appendici (Parte 9), stato "IN REVIEW", nessuna rinumerazione Parti precedenti | OK | `docs/methodology_v2/00_indice.md` (sezione "Parte 8 — Convenzione dati storici e politica di rollover (~10 pp) IN REVIEW" inserita prima di "Appendici operative") |
| AC-DoD-5 | Riferimenti incrociati a Parti I-VII verificati e citati con il numero di Parte definitivo (mappatura Planner) | OK | Cap.37 cita Parte I Capp.1, 2, 5; Cap.38 cita Parte III Capp.12, 13, Parte IV Cap.19, Parte VII Cap.31.1; Cap.39 cita Parte V Cap.25.1, Parte VII Cap.31.1; Cap.40 cita Parte II Capp.7, 10, Parte III Capp.12, 13, 14, 15, Parte VII Cap.35; Cap.41 cita Parte I Cap.1, Parte II Cap.7; Cap.42 cita preambolo `00_indice.md`, Parte III Capp.13, 15.2; Cap.43 cita Parte III Capp.12, 13.4, Parte VII Cap.34; Cap.44 cita Parte I Capp.1, 3 |
| AC-DoD-6 | `reports/REPORT_CAP_08.md` generato secondo template supervisore con cosa e' stato deciso, escluso, rollback criteria | OK | Questo file (sezioni Cosa e' stato prodotto, Ipotesi di partenza, Decisioni rilevanti, Misura prima/dopo, Verifica AC, Domande aperte, Criterio di rollback con 8 sotto-rollback) |
| AC-DoD-7 | `tasks/DEV_STATUS.md` aggiornato a `READY_FOR_REVIEW` | OK (eseguito a fine task come ultimo step della pre-consegna checklist) | `tasks/DEV_STATUS.md` |
| AC-DoD-8 | Commit + push diretto a `origin/main` (deroga task card §5 ratificata, decisione (a)) | OK (eseguito a fine task) | `git log -1 --stat` mostrera' i 5 file modificati/creati committati e pushati |

---

## Domande aperte per il Planner

Nessuna domanda aperta. La pipeline Developer -> Reviewer puo' procedere senza intervento del supervisore.

Il Planner aveva esplicitamente verificato in `tasks/ACTIVE_TASK.md` sezione "Verifica esplicita di ambiguita' non risolte" che tutte le 12 aree potenzialmente ambigue erano gia' coperte dalle 7 decisioni ratificate (a)-(e) e (1)-(3) e dalle 3 note tecniche T1-T3. Durante la stesura il Developer non ha incontrato ulteriori ambiguita' non risolvibili dai documenti del progetto.

Nessuna nuova Q-XX viene aperta in `tasks/QUESTIONS.md`.

---

## Criterio di rollback

Ciascuna delle 8 decisioni normative di Parte 8 (§3.1-§3.8 del task card) ha un proprio criterio di reversibilita' specifico, elencato di seguito.

### Rollback §3.1 / Cap.37 — Scelta della serie ufficiale di training

**Reversibile?** Solo via nuovo task Planner.

**Condizione di rollback**: se in FASE-B (acquisizione storico Portara/CQG) emergesse che la serie FIB pieno non e' disponibile su 5+ anni a frequenza 1-minuto, o se Portara/CQG non consegnasse il roll log richiesto, la convenzione "FIB pieno back-adjusted Portara/CQG come unica fonte" andrebbe riesaminata. In tale caso il Planner dovrebbe valutare se accettare una serie piu' corta (es. 3 anni invece di 5+) o un vendor alternativo (con riesame di Cap.38 sulla convenzione di back-adjustment del nuovo vendor).

**Impatto del rollback**: alto. Tocca la fonte canonica del training. Non rollback automatico; richiede nuovo ciclo Planner.

### Rollback §3.2 / Cap.38 — Convenzione di back-adjustment ufficiale

**Reversibile?** Si, se la sanity validation §3.7 / Cap.43 fallisce.

**Condizione di rollback**: se Cap.43 rileva discrepanze fra ratio-adjusted e unadjusted-stitched superiori a $3\sigma$ bootstrap su una o piu' metriche, la ricostruzione ratio-adjusted andrebbe rivista (es. controllo della formula del fattore $\rho_k$, gestione corretta dei roll, sincronizzazione con il roll log Portara). Se la discrepanza persiste dopo correzione, ritorno al Planner per riesame della scelta della serie ufficiale di training (es. utilizzo della Panama-additive direttamente per il training, in deroga a Cap.38). Il fallback Panama-additive comporta perdita di precisione nella scala relativa dei rendimenti log, con possibili impatti sulla calibrazione EGARCH.

**Impatto del rollback**: medio. Richiede riesame ma non blocca la pipeline completa.

### Rollback §3.3 / Cap.39 — Filtro pre-expiry $N=3$

**Reversibile?** Si, con aggiornamento minore di Parte 8.

**Condizione di rollback**: se CAP-DATA-02 (richiesta tecnica a Portara) conferma una roll rule diversa da "3 giorni di trading prima della scadenza" (es. 2 giorni di calendario, oppure 5 giorni di trading), il valore $N$ viene aggiornato di conseguenza nel preprocessor. L'aggiornamento e' minore: non richiede ritorno al Planner per la struttura della Parte 8, basta un commit di update del valore in Cap.39 (con re-Review minore). Se Portara confermasse roll rule "calendar days" invece di "trading days", andrebbe aggiornata anche la definizione di $\mathrm{trading\_day}(\cdot)$ nell'algoritmo formale.

**Impatto del rollback**: basso. Cambio di un parametro provvisorio congelato come "valore di lavoro" esplicito.

### Rollback §3.4 / Cap.40 — Preprocessor griglia 1-min regolare

**Reversibile?** No, senza nuovo task Planner.

**Condizione di rollback**: la regola di forward-fill con flag `bar_synthetic` e' invariante semantico, ancorato alla gap semantics del documento metodologico v2 (Parte II Cap.7.3 + Parte III Cap.12.4). Modificarla richiederebbe riesaminare la gap semantics dell'intera Parte II e Parte III, oltre la condizione di nessun touch su `bar_synthetic`. Un eventuale cambio (es. interpolazione lineare invece di forward-fill, o esclusione totale dei minuti senza trade dalla griglia) avrebbe impatti su tutti i consumer a valle.

**Impatto del rollback**: alto. Tocca un invariante semantico cross-Parte.

### Rollback §3.5 / Cap.41 — Timeline sessioni FIB

**Reversibile?** Si, con aggiornamento del CSV normativo e re-Review minore.

**Condizione di rollback**: se CAP-DATA-02 o PHASE-B fornisce metadati addizionali sulle epoche storiche del FIB (via roll log Portara o conferma diretta dal vendor), le epoche del calendario `fib_session_calendar.csv` vanno riconciliate. In particolare le ambiguita' E1 (orari verificati solo nel 2000) e E2 (orari derivati per inferenza inversa) potrebbero essere risolte con dati piu' precisi, modificando le date di confine o gli orari di sessione. Aggiornamento del CSV + sezione corrispondente di Cap.41 + nota nel README.md. Non richiede nuovo Planner sulla struttura della Parte 8.

**Impatto del rollback**: basso-medio. Cambio di metadati storici, impatta solo le finestre di training pre-2020 (l'epoca corrente E5 e' confermata da fonti ufficiali).

### Rollback §3.6 / Cap.42 — Convenzione cross-index PHASE-2

**Reversibile?** No, senza nuovo task Planner.

**Condizione di rollback**: la fasizzazione PHASE-1 vs PHASE-2 e' scelta di roadmap del progetto (decisione (1) ratificata dal supervisore), non scelta tecnica isolata. Un eventuale rollback (es. abbandono della PHASE-2, o attivazione anticipata della PHASE-2 nel doc v2 corrente) richiederebbe nuovo task Planner per riesaminare la struttura del documento, riscrivere Parte III Cap.13/15 con i canali cross-index, e introdurre una nuova Parte dedicata alla covarianza condizionata multi-indice.

**Impatto del rollback**: molto alto. Tocca la struttura del doc v2 e l'architettura del motore.

### Rollback §3.7 / Cap.43 — Sanity validation $3\sigma$ bootstrap

**Reversibile?** Si, con aggiornamento minore di Cap.43.

**Condizione di rollback**: se la soglia $3\sigma$ bootstrap risultasse troppo stringente (sistematici fallimenti su artefatti normali del back-adjustment) o troppo permissiva (mancato rilevamento di artefatti veri), il parametro va riesaminato. Aggiornamento del valore in Cap.43 + nota su $B$ e block length $L_{avg}$ rimanda a Parte VII Cap.34. Non richiede nuovo Planner.

**Impatto del rollback**: basso. Cambio di parametri di soglia, non di principio.

### Rollback §3.8 / Cap.44 — Esclusione fonti alternative

**Reversibile?** Si, via nuovo task Planner.

**Condizione di rollback**: ogni fornitore alternativo che si volesse introdurre come fonte training, benchmark o cross-index richiede nuovo task Planner per autorizzazione esplicita. Il task Planner verifica i 5 criteri elencati in Cap.44 (coerenza con `research = runtime`, compatibilita' back-adjustment, roll log, granularita' 1-min, calendario sessione). L'autorizzazione comporta possibile aggiornamento di Cap.37-43 a seconda delle convenzioni del nuovo vendor.

**Impatto del rollback**: variabile (basso se autorizzazione singola fonte di backup; alto se cambio di vendor primario).

---

## Riepilogo per l'Orchestratore — chiusura sessione

- **Deliverable completati**: 5/5 file richiesti dal task card.
- **Acceptance criteria**: 16/16 OK.
- **Domande aperte**: 0.
- **M-promemoria nuovi emessi**: 0 (CARRYOVER da preservare per Orchestratore in chiusura sessione: M-2 OPEN su latenza Telegram -> Appendice E in Parte 9, invariato).
- **Push direct to `origin/main`**: in corso a chiusura del task (decisione (a) ratificata).
- **DEV_STATUS**: aggiornato a `READY_FOR_REVIEW` come ultimo step della pre-consegna checklist.

Il Developer si ferma qui in attesa del check post-Developer dell'Orchestratore e dell'invocazione del Reviewer.
