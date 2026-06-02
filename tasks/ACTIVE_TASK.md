# TASK ATTIVO: SPEC-FUNZ-01 — Specifica funzionale del prodotto-segnale FIB (PHASE-1)

**Assegnato da**: Planner
**Output atteso**: `docs/spec_funzionale/SPEC_FUNZ_01.md` (cartella nuova, greenfield — non esiste ancora; il Developer la crea contestualmente al primo commit)
**Report atteso**: `reports/REPORT_SPEC_FUNZ_01.md` con le 5 sezioni del formato supervisore (Cosa è stato prodotto / Ipotesi di partenza / Decisioni rilevanti / Misura prima/dopo / Domande aperte / Criterio di rollback)
**Stato**: IN ATTESA
**Workflow**: Standard `Planner → Developer → Reviewer` (Developer v1 → Review v1 → eventuale classificazione finding al supervisore → fix → ... → PASS).
**Sede Reviewer**: **WEB** (documento + grep nel repo + lettura dei CAP committati; nessuna esecuzione DAPI, nessuna probe empirica nuova prevista — il track non produce fatti empirici).
**Modalità di review**: **Review formale piena adattata al non-CAP** (CAP-review piena nei suoi 5 check ostili, con scope adattato al fatto che SPEC-FUNZ-01 non è un capitolo metodologico — vedi sezione "Pipeline attesa" sotto).

---

## Natura del track e perimetro non-CAP

SPEC-FUNZ-01 **non è un capitolo metodologico** (non è CAP-XX né "Parte N" della metodologia v2). Non ridefinisce metodologia, non introduce nuovi parametri del GA, non modifica decisioni `D-*-N` chiuse, non riapre AC delle Review v1..v4 dei capitoli metodologici già PASS, non riapre il merito di alcun Q-XX chiuso.

SPEC-FUNZ-01 è un **documento di requisiti funzionali / di prodotto / business**, in **vista operatore/prodotto**. Consolida la metodologia v2 (10 Parti, Cap.1-65, tutti PASS) in **requisiti funzionali (R-N)** + **requisiti non-funzionali / qualità (NFR-N)** + **vincoli normativi (CN-N)** + **matrice di tracciabilità requisito → capitolo metodologia v2**, e fa da **ponte fra il documento metodologico chiuso e la successiva FASE-D di implementazione**.

**Criterio di valore del track** (sostituisce la regola "orientamento al comportamento del GA" del Planner — qui reinterpretata): ogni requisito SPEC-FUNZ-01 traccia simultaneamente a (a) un valore operativo / di prodotto reale per l'operatore retail FIB E (b) un capitolo della metodologia v2 da cui deriva. Un requisito senza tracciabilità a metodologia o senza valore operativo dichiarato è un requisito sbagliato e il Reviewer lo segnala come BUG REALE.

**Cosa il track NON è**:
- Non è un audit RM dei CAP (gli audit RM-RETRO/RM su CAP-DATA-01/02/03 sono task separati, già chiusi PASS).
- Non è un'analisi di compute / costo / TCO (Cap.4 Parte I ha già fissato il budget cloud; SPEC-FUNZ-01 lo cita, non lo ridiscute).
- Non è la specifica di implementazione FASE-D (i dettagli di codice, struttura dei microservizi, scelta dei framework, pipeline CI/CD restano fuori).
- Non è un piano roadmap di progetto (cita PHASE-1/PHASE-2 come fasi già decise in Cap.42 Parte 8, non le ridefinisce).
- Non è la spec PHASE-2 cross-index (DAX/EuroStoxx50/ES/MES — fuori scope esplicito, vincolo di Cap.42 Parte 8 e Cap.55 Parte 9).

---

## Obiettivo

SPEC-FUNZ-01 risponde a tre domande operative chiave del progetto, in vista business / prodotto / operatore:

1. **Che cos'è il prodotto-segnale FIB che il sistema pubblica, dal punto di vista del consumatore (operatore retail) e del committente (supervisore)?** Quali sono i suoi attributi, il suo ciclo di vita visto dall'operatore, i suoi SLA di consegna, i suoi vincoli di compliance.
2. **Quali sono i requisiti funzionali e non-funzionali che la successiva implementazione FASE-D deve soddisfare**, in forma di lista numerata `R-N` (funzionali), `NFR-N` (qualità/quantitativi), `CN-N` (compliance/normativi), tracciabile capitolo per capitolo alla metodologia v2.
3. **Come si misura il successo del prodotto** in produzione, dal punto di vista del committente (criteri di accettazione del prodotto, gate go-live tradotti in linguaggio prodotto, KPI operativi, criteri di rollback).

SPEC-FUNZ-01 NON risponde (e il Reviewer segnala come finding se il Developer dovesse rispondere):
- Quale algoritmo di volatilità condizionata si usa per stimare $\hat{\sigma}$ (è materia di Cap.13 Parte III, già chiuso PASS — la spec dice "il sistema applica una stima EGARCH conforme a Cap.13" e basta, non riderivare).
- Quali sono i parametri congelati / non congelati del cromosoma (è materia di Cap.22-26 Parte V — la spec dice "il sistema applica il cromosoma frozen dichiarato in Parte V" e basta).
- Quale formato esatto ha il payload DAPI di una candela storica (è materia di Cap.49 Parte 9 + CAP-DATA-03 — la spec dice "il sistema usa il decoder canonico riferito in Parte 9 / `scripts/export_directa_history_parametric.py:467-481`" come fatto chiuso).
- Quali eventi marker normativi vengono loggati (è materia di Cap.54 Parte 9 + Cap.65 Parte 10 — la spec li elenca per riferimento alla compliance, senza redefinirli).

Il track si fa **adesso** perché:
- Il documento metodologico v2 è chiuso (10 Parti, Cap.1-65 PASS) sui versanti modello + dati storici + runtime DAPI + ciclo di vita tape; il ponte verso FASE-D richiede un consolidamento di requisiti che oggi non esiste.
- Il consolidamento di requisiti deve precedere la cantierabilità: il supervisore necessita di un documento di prodotto che possa essere mostrato anche fuori dal team metodologico (consulenti legali per compliance MiFID II, valutatori AWS per stima cloud, fornitori storico Portara/CQG per acquisto del feed FIB, fornitori bot Telegram). I CAP-XX non sono leggibili da un esterno; SPEC-FUNZ-01 lo è.
- M-2 (verifica empirica latenza Telegram $L_{max}=30$s) è l'unico M-promemoria di capitolo ancora **OPEN** in `CARRYOVER.md`. La spec lo incardina come requisito non-funzionale del prodotto e ne traccia la dipendenza con FASE-D / Appendice E senza risolverlo qui (la verifica empirica resta dipendenza aperta).

---

## Eredità obbligatoria — da metodologia v2 chiusa, da QUESTIONS chiuse, da CARRYOVER

### Da input autoritativo dell'Orchestratore (NON ri-verificare, NON riaprire)

1. **Solo emissione, nessuna esecuzione ordini**. Il prodotto è un servizio di segnalazione; non interagisce con l'order router del broker. (Fonte: Cap.1 Parte I, eredità di tutta la metodologia v2.)
2. **1 contratto FIB alla volta**. Sizing fisso, non parametrabile dall'utente. (Fonte: Cap.2 Parte I, eredità.)
3. **Tick FIB discreto da 5 punti indice, moltiplicatore 5 EUR/punto**. Tutti i prezzi, le bande, i target, gli stop pubblicati dal segnale sono multipli di 5 punti FIB. $b_{min}=5$ è 1 tick. (Fonte: Cap.2 Parte I, Cap.6 Parte II.)
4. **Sessione operativa 8:00-22:00 CET**, finestra unica e continua di negoziazione FIB su IDEM. Coerente con epoca E5 di Cap.41 Parte 8 e Cap.52 Parte 9. (Fonte: Q-01 chiusa, Cap.1 Parte I, Cap.52 Parte 9.)
5. **Operatore retail non professionale MiFID II**, esecuzione manuale da cellulare, broker Directa SIM (DAPI come canale tecnico esclusivo del FIB), canale di consegna Telegram, commissioni 5 EUR/operazione (2 punti FIB equivalenti per ciclo apertura-chiusura). (Fonte: Cap.2 Parte I, Cap.46 Parte 9, decisione D-1/D-6 Parte 9.)
6. **PHASE-1 = FIB-only**. PHASE-2 (cross-index DAX/EuroStoxx50/ES/MES) è **fuori scope** della spec corrente. (Fonte: Cap.42 Parte 8, Cap.55 Parte 9, Cap.64 Parte 10.)

### Da decisioni del supervisore (QUESTIONS chiuse) — vincoli di prodotto rigidi

7. **Q-04 chiuso**: cap di validità multiday del segnale eseguito ≤ 2 giorni di trading, decorrenti dal raw touch (NON dall'emissione). Patch retroattiva (commit `fc7531b`) integrata in Cap.1 Parte I + Cap.6 Parte II ($\Delta t_{cromosoma}$). La spec lo recepisce come vincolo del prodotto-segnale.
8. **Q-05 chiuso (Opzione D raffinata)**: state machine del segnale = 1 non-terminale (`active`) + 6 terminali (`target_1_hit`, `stopped`, `invalidated`, `missed_target`, `expired`, `revoked`); `target_2` è informazione strutturale pubblicata, non variabile di lifecycle; position lifecycle post-target_1 è submacchina distinta (Cap.11 Parte II) IN-SCOPE per reporting / OUT-OF-SCOPE da execution policy. La spec recepisce e racconta questo ciclo di vita in vista operatore (Sezione 4).
9. **Q-01 chiuso**: sessione 8:00-22:00 CET come finestra unica continua. (Vedi punto 4.)
10. **Q-A-3 chiuso** (Cap.53 Parte 9): indici cash europei DGER/DSTX50/DITAS/DFRA come gating qualitativo configurabile post-emissione, **NON feature del GA**. La spec recepisce come requisito di compliance/risk (gating può sospendere emissione, non altera ranking GA).
11. **D-9-NB3 chiusa** (Cap.56 Parte 9): catalogo eventi terminali pubblicati = 6 marker normativi distinti (`SIGNAL_TARGET_1_HIT` / `STOPPED` / `INVALIDATED` / `MISSED_TARGET` / `EXPIRED` / `REVOKED`), coerenti con state machine Cap.7 Parte II. La spec elenca questi marker come componenti del payload pubblicato.
12. **D-9-NB4 chiusa** (Cap.56 Parte 9): $L_{warmup}=30$ giorni di trading IDEM congelato per warm-up stati condizionali post-restart. La spec lo recepisce come requisito di restart procedure.
13. **D-10-2 / D-10-4 / D-10-8 chiuse** (Cap.65 Parte 10): idempotenza T+3 morning sul tape backfill (perimetro empirico FIB6F/DITAS ~100gg); cash low/high via CANDLE ufficiale `f8`/`f9`, MAI tick realtime (densità ~6 tick/min); immutabilità barre storicizzate. La spec le recepisce come requisiti di gestione del tape e dei dati cash.

### Da `tasks/METODO.md` (RM-1..RM-4) — vincoli metodologici sul track

14. **RM-1 — verifica vs assunzione**. SPEC-FUNZ-01 consolida fatti **già verificati e chiusi** nei CAP. Quindi: la spec **NON deve introdurre nuove dichiarazioni "verificato X"** su sistemi esterni (DAPI/Telegram/Portara). Ogni asserzione che sembri "fatto verificato" deve essere un **richiamo** a un fatto già chiuso, etichettato con la sua provenienza (`[CODICE-ESISTENTE <path>:<linea>]`, `[PROVA-EMPIRICA <data>]`, `[DOC-INTERNO <CAP-XX>:<riga>]`). Nuovi blocchi RM-1 a 4 righe `VERIFICA / PROVE / ALTERNATIVE COMPATIBILI ESCLUSE / ALTERNATIVE COMPATIBILI NON ESCLUSE` **non sono richiesti** per la spec (non sta facendo verifiche nuove), ma se il Developer dichiarasse "verificato X" senza richiamo a fatto chiuso, il Reviewer lo classifica come BUG REALE (RM-1).
15. **RM-2 — grep nel repo**. Pertinente solo se il Developer cita decoder/parser DAPI esistenti: in tal caso le citazioni devono essere `[CODICE-ESISTENTE <path>:<linea>]` puntuali, verificabili dal Reviewer con Read. Decoder canonici già censiti nella metodologia v2: `scripts/export_directa_history_parametric.py:467-481` (schema CANDLE `C;L;H;O;V`), `:228-230` (sintassi CANDLERANGE), `:61` (`DEFAULT_INTRADAY_MAX_DAYS=100`), `:282-285` (terminatore `END CANDLES`), `:605-617` (header CSV legacy 11 campi); `scripts/probe_dapi.py:159` (`DapiConn`), `:230` (`parse_line`), `:333` (`run_candlerange`). Il Developer NON deve grepare per scoprirli ex novo (sono autoritativi da metodologia v2 chiusa); deve solo citarli correttamente se li richiama.
16. **RM-3 — fonti esterne**. Ogni riferimento a wiki Directa / docs Telegram / docs Portara / docs CME è etichettato `[WIKI-HINT, da verificare]` con avvertenza esplicita ereditata da Cap.49 Parte 9 + audit RM CAP-DATA-02 (la wiki Directa è dimostrata inesatta sullo schema CANDLE). La spec NON si appoggia mai a livello 4 come unica fonte di un'asserzione: ogni asserzione strutturale ha almeno una fonte livello 1/2/3 nei CAP chiusi.
17. **RM-4 — output non-CAP determinanti**. SPEC-FUNZ-01 stesso rientra in RM-4 (è un documento determinante che produrrà asserzioni citate in FASE-D). Per questo motivo la pipeline include la **Review formale leggera del Reviewer in modalità CAP-review adattata** (opzione B di RM-4) — vedi sezione "Pipeline attesa". L'opzione A (self-review esplicita del Developer come blocco in fondo al documento) NON è sufficiente, perché il diff aggregato del commit supererà N=200 righe e il track introduce asserzioni destinate a essere citate altrove (FASE-D, eventuali documenti di valutazione fornitori).

### Da `tasks/CARRYOVER.md` — M-promemoria di capitolo aperti

Censimento sistematico degli M-promemoria ancora aperti (RM-Planner: ogni M-XX deve essere integrato nel task corrente o rinviato con motivazione esplicita):

18. **M-2 OPEN** (Review v1 CAP-02): "Verifica empirica latenza Telegram ($L_{max}=30$s)" — destinazione carryover **Appendice E**. **Decisione del Planner per SPEC-FUNZ-01: opzione (a) — la spec fissa il requisito di consegna $L_{max}=30$s come NFR del prodotto (NFR-N "latenza end-to-end di consegna del segnale all'operatore") e dichiara la verifica empirica come dipendenza aperta FASE-D / Appendice E. Motivazione**: un documento di prodotto deve obbligatoriamente dichiarare lo SLA consumer-facing; non dichiararlo lascerebbe la spec amputata di un requisito fondamentale del canale di consegna (cellulare, operatore in mobilità). La verifica empirica del valore $L_{max}=30$s contro bot reale è materia di FASE-D / Appendice E, NON di SPEC-FUNZ-01; ma il **requisito**, come obbligo del prodotto, va incardinato qui. La spec cita Cap.9.3 Parte II + Cap.31.1 Parte VII (vincolo qualitativo già citato come gate go-live AC-GO-10) come riferimenti autoritativi e dichiara M-2 come dipendenza esterna non risolta in SPEC-FUNZ-01.
19. **Tutti gli altri M-N (M-1, M-4, M-5, M-6, M-7..M-16)**: **CLOSED** in CAP-04/05/06/07. Non aperti, non pertinenti a SPEC-FUNZ-01. La spec li può citare come fatti chiusi se serve tracciabilità, ma non li riapre.
20. **M-16 condizionale CLOSED-CAP-07**: regola di attivazione/disattivazione Cox time-varying coefficients dipendente dal walk-forward nested del ciclo training successivo, registrata come metadato bundle frozen `cox_time_varying_active` in Cap.35 Parte VII. La spec lo recepisce come requisito metodologico già normativo (NON lo riapre), nella sezione "Requisiti di qualità e accettazione" (gate go-live).

### Da `tasks/CARRYOVER.md` — RACC-METODO (namespace separato)

21. **RACC-METODO-1 OPEN**: de-numerizzazione rimandi `METODO.md:NN` / `reviewer.md:NN` residui. **NON pertinente a SPEC-FUNZ-01** (è manutenzione di file di processo `.claude/*` e `tasks/METODO.md`, non del documento di prodotto). Citata per completezza del censimento; non si applica.
22. **RACC-METODO-2 OPEN — onorata in CAP-DATA-03**: AC su schema-dato di sistemi esterni richiedono diff puntuale col decoder canonico. **Pertinente come vincolo di review trasversale**: se il Developer di SPEC-FUNZ-01 cita uno schema DAPI/Telegram come fatto chiuso, il Reviewer applica RACC-METODO-2 e verifica diff col decoder canonico (atteso `scripts/export_directa_history_parametric.py`). La spec NON ridichiara gli schemi (li cita come chiusi).

### Da `tasks/STATO_CORRENTE.md` — M-promemoria di sessione (input critico)

23. **M-9** (schema PRICE realtime `f4=last`/`f6=volume_cum`/`f8=day_low`/`f9=day_high`): autoritativo per il requisito "feed runtime DAPI" della spec; se la spec cita PRICE, lo cita conforme a M-9.
24. **M-10** (BOOK_5 certificato): supporto level-2; non centrale per la spec di prodotto, ma se serve la spec lo cita come chiuso.
25. **M-1 + M-3**: schema CANDLE `C;L;H;O;V` + codici errore DAPI: autoritativi.

---

## Sezioni da produrre (target ~12-16 pagine totali, 10 sezioni)

Il Developer rispetta i nomi e l'ordine delle 10 sezioni sotto. Può fondere sotto-elementi se la coerenza espositiva lo richiede, ma il numero totale di sezioni resta 10 e il contenuto di ciascuna deve coprire lo scope dichiarato. Ogni sezione include, a fine sezione, una **mini-tabella di tracciabilità** `Requisito ID | Capitolo metodologia v2 | Tipo` (R/NFR/CN). Per ogni requisito introdotto in sezione, ID univoco progressivo: `R-1`, `R-2`, ..., `NFR-1`, ..., `CN-1`, ...

### Sezione 1 — Scopo, visione e perimetro del prodotto (~1.5 pp)

**Scope**: cos'è il prodotto-segnale FIB. Proposta di valore per l'operatore retail (segnali strutturati intraday/multiday su FIB con probabilità target-hit modellata, pubblicati su Telegram, eseguibili manualmente da mobile durante la sessione lavorativa). Confine architetturale "**solo emissione, nessuna esecuzione**" come vincolo strutturale, non implementativo. Out-of-scope esplicito di prodotto: nessuna gestione attiva della posizione, nessuna size dinamica, nessun trailing stop/scaling, nessuna esecuzione automatica. **PHASE-1 vs PHASE-2** dichiarato esplicitamente (FIB-only ora; cross-index futuro).

**Tracciabilità**: Cap.1 Parte I, Cap.2 Parte I, Cap.5 Parte I, Cap.42 Parte 8.

**Acceptance criteria sezione**:
- [ ] Frase di proposta di valore in ≤3 righe, leggibile da non-tecnico.
- [ ] Almeno 3 requisiti funzionali `R-N` di perimetro (R-PERIM-*).
- [ ] Vincolo "solo emissione" dichiarato come `CN-1` (vincolo non negoziabile, ancoraggio Cap.1 Parte I).
- [ ] Out-of-scope di prodotto in lista chiusa esplicita (almeno: gestione posizione, sizing dinamico, trailing/scaling, esecuzione automatica, cross-index PHASE-2).

### Sezione 2 — Attori, contesto, personas (~1 pp)

**Scope**: chi consuma il prodotto e in quale contesto. **Personas**: operatore retail non professionale MiFID II (risk manager bancario italiano), esecuzione manuale mobile durante orario lavorativo, broker Directa SIM, canale Telegram, mercato IDEM. Stakeholder secondari: supervisore (committente metodologico), reviewer esterno compliance (potenziale, futuro). Ambiente di esecuzione utente: smartphone Android/iOS con app Telegram + app Directa per ordering. Vincoli di accesso al PC fisso: sviluppo, training, inference live — non per esecuzione ordini.

**Tracciabilità**: Cap.2 Parte I, Cap.3 Parte I, Cap.46 Parte 9, Cap.52 Parte 9, Cap.53 Parte 9.

**Acceptance criteria sezione**:
- [ ] Persona operatore descritta con almeno 5 attributi (profilo MiFID II, mobile, vincoli temporali, esperienza, strumenti).
- [ ] Almeno 2 requisiti `R-N` di contesto (esecuzione manuale come vincolo, canale Telegram come obbligo).
- [ ] Stakeholder secondari elencati.

### Sezione 3 — Requisiti funzionali del segnale (prodotto) (~2 pp)

**Scope**: il segnale come **feature di prodotto**. Componenti del payload pubblicato dal punto di vista del consumatore: direzione (`long`/`short`), banda di entry (estremi discreti multipli di 5 pt), `target_1` strutturale, `target_2` strutturale (informazione decisionale pubblicata, non variabile di lifecycle — Q-05 Clausola 2), `stop_loss` strutturale, `setup_class` (`directional` / `trade_range`), qualificatori `target_2_type` / `stop_type` (`structural`/`synthetic`), timer pre-trigger $T_{touch}^{max}$ e timer post-trigger $\Delta t_{cromosoma}$, identificatore `signal_id`, timestamp di emissione. Invariante "payload immutabile dopo emissione" (Cap.6.2 Parte II). Regola "segnale unico attivo" (Cap.6.3 / Cap.28 Parte VI). Filtro minimo 80pt su `target_1` directional o $A_{range}$ trade_range (Cap.5 Parte I + Cap.8 Parte II).

**NON in questa sezione**: matematica della derivazione strutturale di target/stop (Cap.17-18 Parte IV); algoritmo pivot detection (Cap.15 Parte III); soglie/parametri congelati di filtro (Cap.20 Parte IV, Cap.26 Parte V).

**Tracciabilità**: Cap.6 Parte II, Cap.8 Parte II, Cap.17 Parte IV, Cap.18 Parte IV, Cap.21 Parte IV.

**Acceptance criteria sezione**:
- [ ] Tabella dei campi del payload con ≥9 voci (coerente con Cap.9.2 Parte II esteso a 9 voci Iterazione 5).
- [ ] Per ogni campo: tipo, dominio, vincoli, capitolo v2 di origine.
- [ ] Invariante immutabilità e regola segnale unico attivo dichiarate esplicitamente come `R-N`.
- [ ] Filtro minimo 80pt come `R-N`.
- [ ] Almeno 1 esempio numerico (payload concreto, prezzi multipli di 5 pt FIB).

### Sezione 4 — Ciclo di vita del segnale visto dall'operatore (~1.5 pp)

**Scope**: la state machine in vista operatore. Stati nel modo in cui l'operatore li vive: emissione (notifica Telegram con payload completo), notifica di **trigger_event** separata (raw touch della entry zone), esito terminale (uno dei 6: `target_1_hit`, `stopped`, `invalidated`, `missed_target`, `expired`, `revoked`). Timer pre-trigger (operatore vede "in attesa di raw touch") e timer post-trigger (operatore vede "esecuzione attiva"). Cosa significa per l'operatore ricevere `revoked` (il segnale è sostituito da uno nuovo con `signal_id` differente) o `missed_target` (target_1 raggiunto prima del raw touch — il segnale non è eseguibile). Position lifecycle post-target_1: l'operatore lo vede come dato di reporting nei report periodici, NON come comando di esecuzione (Cap.11 Parte II IN-SCOPE solo per reporting).

**Tracciabilità**: Cap.7 Parte II, Cap.11 Parte II, Cap.30 Parte VI, Cap.54 Parte 9 (eventi loggati).

**Acceptance criteria sezione**:
- [ ] Diagramma testuale (o tabella) della state machine: 1 non-terminale + 6 terminali.
- [ ] Ogni terminale spiegato in 1-2 righe in vista operatore.
- [ ] Notifica `trigger_event` come evento separato (`R-N`) e marker normativo (`CN-N`).
- [ ] Distinzione esplicita "ciclo di vita del segnale (chiuso a target_1) vs position lifecycle post-target_1 (reporting only)".

### Sezione 5 — Canale di pubblicazione e requisiti di consegna (~1.5 pp)

**Scope**: Telegram come canale di consegna. Formato messaggio **mobile-readable** (consumabile dal cellulare in 5-10 secondi durante orario lavorativo). Contenuti minimi obbligatori: 9 voci di Cap.9.2 Parte II (`signal_id`, direzione, entry zone, target_1, target_2, stop_loss, setup_class, qualificatori type, timestamp di emissione). Latenza ammissibile end-to-end: **NFR `L_{max}=30$ s** (eredità Cap.9.3 Parte II + Cap.31.1 Parte VII AC-GO-10). Anti-duplicato. Nuovo messaggio per nuovo `signal_id` (no edit del messaggio esistente — coerente con invariante immutabilità payload). Notifica `trigger_event` come messaggio separato dal messaggio di emissione (Cap.9 Parte II, Cap.29 Parte VI).

**M-2 OPEN dichiarata esplicitamente**: la verifica empirica del valore $L_{max}=30$ s contro bot reale resta **dipendenza aperta FASE-D / Appendice E**, NON risolta in SPEC-FUNZ-01. La spec FIB-only fissa il **requisito** ma non lo verifica. Dichiarazione esplicita nella sezione: "M-2 (verifica empirica latenza Telegram) è dipendenza aperta verso Appendice E e FASE-D; SPEC-FUNZ-01 dichiara il requisito $L_{max}=30$ s come NFR del prodotto e demanda la verifica al ciclo di test FASE-D".

**Tracciabilità**: Cap.9 Parte II, Cap.29 Parte VI, Cap.31.1 Parte VII (AC-GO-10), Appendice E (outline).

**Acceptance criteria sezione**:
- [ ] Esempio testuale di messaggio Telegram di emissione (con 9 voci minime, prezzi multipli di 5 pt, mobile-readable).
- [ ] Esempio testuale di messaggio Telegram di `trigger_event`.
- [ ] NFR `NFR-L_max` con valore 30 s, riferimento Cap.9.3 Parte II + Cap.31.1 Parte VII, **dipendenza M-2 dichiarata esplicitamente** come "verifica empirica aperta FASE-D / Appendice E".
- [ ] Almeno 3 requisiti `R-N` (anti-duplicato, nuovo messaggio per nuovo signal_id, notifica trigger separata).

### Sezione 6 — Requisiti operativi e di sessione (~1 pp)

**Scope**: vincoli operativi del prodotto. Sessione 8:00-22:00 CET (finestra unica continua). 1 contratto FIB alla volta. Singolo segnale attivo per direzione (vincolo "segnale unico attivo" $|\mathcal{A}(t)| \leq 1$ — Cap.6.3 Parte II / Cap.28 Parte VI). Commissioni 5 EUR/op (2 punti FIB equivalenti per ciclo). Policy di rollover / contract switch con marker `CONTRACT_SWITCH` (D-9-NB2 Cap.56 Parte 9, switch al boot del giorno t = terza venerdì del mese di scadenza). Separazione strutturale segnale (motore) vs gestione posizione (operatore — fuori scope).

**Tracciabilità**: Cap.2 Parte I, Cap.28 Parte VI, Cap.52 Parte 9, Cap.56 Parte 9 (D-9-NB2).

**Acceptance criteria sezione**:
- [ ] Almeno 5 requisiti `R-N` operativi (sessione, sizing, segnale unico, commissioni, rollover).
- [ ] Policy rollover citata fedelmente da D-9-NB2 con esempio FIB6F → FIB6I al 2026-06-19 (data terza venerdì giugno 2026).

### Sezione 7 — Requisiti di qualità e criteri di accettazione del prodotto (~1.5-2 pp)

**Scope**: metriche di successo tradotte in **requisiti di qualità / SLA verificabili** (NFR-N + criteri di accettazione di go-live). Metrica primaria di prodotto: $E[R_{net} \mid executed]$ positivo dopo commissioni (Cap.5 Parte I). Metriche di lifecycle: `executable_rate`, `target_hit_rate`, `invalidation_rate`, `missed_target_rate`, $\pi_{t_2 \mid t_1}$. Filtro minimo strutturale 80pt come pre-condizione di emissione. Metriche di rischio: CVaR 95%, maximum drawdown intraday, MFE/MAE aggregati. Metriche anti-overfitting come **gate di go-live**: DSR positivo, PBO sotto soglia (Cap.32-33 Parte VII), bootstrap stazionario per intervalli di confidenza (Cap.34). Checklist go-live `AC-GO-1..AC-GO-12` di Cap.36 Parte VII recepita come "criteri di accettazione del prodotto" della spec.

**Tracciabilità**: Cap.5 Parte I, Cap.32-36 Parte VII.

**Acceptance criteria sezione**:
- [ ] Tabella dei KPI di prodotto con ≥6 voci (expected net return, executable rate, target hit rate, invalidation rate, CVaR 95%, max DD).
- [ ] DSR/PBO citati come gate di go-live (NFR-DSR / NFR-PBO).
- [ ] Checklist go-live riassunta in ≤12 punti tracciabili a Cap.36.
- [ ] M-16 condizionale `cox_time_varying_active` dichiarata come metadato del bundle frozen (riferimento Cap.35 Parte VII), NON riaperta.

### Sezione 8 — Vincoli normativi e compliance (~1 pp)

**Scope**: vincoli normativi che il prodotto deve rispettare. Posizionamento esplicito: "**segnale informativo, non consulenza in materia di investimenti, non esecuzione automatica di ordini**" — coerente con MiFID II retail e con vincolo strutturale "solo emissione" della metodologia. Separazione dalla gestione ordini. Audit log e retention: 90 giorni rolling + retention permanente sui giorni di emissione segnale (Cap.54 Parte 9, D-4 / "Gap-4"). Eventi loggati: `HANDSHAKE`, `SUB`, `SIGNAL_*`, `GATING_*`, `RUNTIME_*`. Privacy / GDPR — dichiarazione minima (il prodotto non raccoglie PII dell'operatore oltre il chat ID Telegram; vincolo qualitativo, FASE-D dettagli).

**NON in questa sezione**: parere legale formale; testi di disclaimer (sono materia di consulente legale, fuori scope spec).

**Tracciabilità**: Cap.2 Parte I, Cap.54 Parte 9, Cap.65 Parte 10 (decisioni D-10-* su retention/audit log).

**Acceptance criteria sezione**:
- [ ] Posizionamento "segnale informativo" dichiarato come `CN-N` con riferimento MiFID II retail.
- [ ] Separazione segnale/esecuzione come `CN-N`.
- [ ] Retention audit log come `CN-N` con valori (90gg rolling + permanente sui giorni di emissione).
- [ ] Catalogo eventi loggati elencato per riferimento (Cap.54 Parte 9), non ridichiarato.

### Sezione 9 — Requisiti di dato e dipendenze infrastrutturali (~1.5 pp)

**Scope**: fonti dati e dipendenze. **Runtime**: Directa DAPI come canale esclusivo del FIB (D-6 Cap.46 Parte 9), porte 10001 (realtime) / 10003 (storico), invariante `research = runtime` esteso all'adapter DAPI → bundle Portara (Cap.45-49 Parte 9). **Storico training**: FIB pieno back-adjusted Portara/CQG (Cap.37-38 Parte 8). **Tape archiviato**: format CSV runtime esteso 13 campi + manifest JSON (Cap.62 Parte 10), distinto da legacy CSV 11 campi di `scripts/export_directa_history_parametric.py:605-617`. **Backfill**: `CANDLERANGE` entro ~100gg, fallback Portara oltre (Cap.59 Parte 10, Cap.61 Parte 10). **Riconciliazione canonica giornaliera**: gate bloccante sulla sessione $d+1$ (Cap.60 Parte 10, distinto da monitoraggio non-bloccante Cap.30 Parte VI). **Compute**: PC i5-7200U per dev/inference, AWS spot c5.4xlarge per training GA (Cap.3-4 Parte I). **Canale Telegram**: bot personale dell'operatore (Cap.3 Parte I, Appendice E). **Indici cash europei**: DGER/DSTX50/DITAS/DFRA come gating qualitativo (Cap.53 Parte 9, NON feature GA).

**NON in questa sezione**: dettagli di implementazione FASE-D (codice, microservizi, framework); scelta esatta dell'instance type AWS (Cap.4 ha fissato c5.4xlarge come riferimento); contratto commerciale con Portara/CQG (consulente acquisti).

**Tracciabilità**: Cap.3 Parte I, Cap.4 Parte I, Cap.37-44 Parte 8, Cap.45-56 Parte 9, Cap.57-65 Parte 10.

**Acceptance criteria sezione**:
- [ ] Tabella dipendenze infrastrutturali con ≥6 voci (DAPI runtime, Portara training, AWS training, PC inference, Telegram, gating cash).
- [ ] Distinzione legacy CSV 11-campi vs runtime esteso 13-campi dichiarata correttamente (riferimento Cap.62 Parte 10 + decoder canonico `:605-617`).
- [ ] Almeno 2 requisiti `R-N` su tape archiviato (immutabilità, format) — tracciabili a Cap.62 + D-10-* Cap.65.
- [ ] Riconciliazione canonica giornaliera dichiarata come gate bloccante (distinta da monitoraggio non-bloccante Cap.30 Parte VI).

### Sezione 10 — Fasizzazione, roadmap, tracciabilità (~1.5 pp)

**Scope**: dove siamo nel percorso e dove si va. **PHASE-1 FIB-only** = oggetto di SPEC-FUNZ-01 corrente. **PHASE-2 cross-index** = fuori scope (rinviata a SPEC-FUNZ-02 o equivalente futuro, NON definito qui). **Ponte verso FASE-D**: SPEC-FUNZ-01 fornisce la base requisiti per la successiva FASE-D di implementazione (codice runtime, pipeline ingest-feature-inference-publish, pipeline training cloud, pipeline backfill/riconciliazione/archiviazione, bot Telegram, audit log). FASE-D è fuori scope di SPEC-FUNZ-01. **Dipendenze aperte FASE-D**: lista esplicita (M-2 latenza Telegram empirica; calibrazione fine $\theta_{reconcile}$ Cap.64 Parte 10; migrazione legacy→esteso del tape Cap.64; codici 1030 e riavvio Darwin mezzanotte come Empirico-CLI residui; etc.).

**Matrice di tracciabilità requisito → capitolo metodologia v2**: tabella riassuntiva di TUTTI i requisiti `R-N` / `NFR-N` / `CN-N` introdotti in Sezioni 1-9, con colonna "capitolo metodologia v2 di origine". Lo scopo è verificare che ogni requisito sia tracciabile e che nessun capitolo metodologico chiuso PASS sia stato omesso senza motivazione (rinvio esplicito fuori scope ammesso per Cap.42 PHASE-2).

**Tracciabilità**: Cap.42 Parte 8 (PHASE-2 fuori scope), Cap.55 Parte 9 (punti aperti), Cap.64 Parte 10 (punti aperti FASE-D), trasversale.

**Acceptance criteria sezione**:
- [ ] Sezione dichiara PHASE-1 vs PHASE-2 esplicitamente.
- [ ] Lista dipendenze aperte FASE-D con ≥5 voci, ognuna tracciata.
- [ ] **Matrice di tracciabilità completa**: ≥30 righe `Requisito ID | Sezione SPEC | Capitolo metodologia v2 | Note`. Ogni capitolo della metodologia v2 (Cap.1-65) che NON appare in matrice è giustificato esplicitamente in una sezione "Capitoli metodologia v2 non tracciati e motivazione" (es. Cap.13 modello EGARCH, Cap.15 catalogo feature, Cap.19 modello Cox — sono fuori dalla vista operatore/prodotto, motivazione "implementazione metodologica interna, opaca al consumatore").

---

## Acceptance criteria globali — tutti devono essere soddisfatti per PASS in Review

### AC di metodo (RM-1/RM-3 / vincoli del Planner)

- [ ] **AC-G1 (RM-1 — no nuovi "verificato X")**: SPEC-FUNZ-01 NON contiene dichiarazioni "verificato X" / "confermato X" / "dimostrato X" come asserzioni nuove di prima istanza. Ogni asserzione fattuale è un richiamo a un capitolo metodologico chiuso, etichettato `[DOC-INTERNO <CAP-XX>:<riga>]` o equivalente. Asserzioni di "fatto verificato" prive di richiamo a CAP chiuso = BUG REALE (RM-1).
- [ ] **AC-G2 (RM-3 — fonti esterne etichettate)**: ogni riferimento a wiki Directa / docs Telegram / docs Portara / docs CME / docs MiFID-II è `[WIKI-HINT, da verificare]`. Nessuna conclusione strutturale si appoggia solo a livello 4. Wiki Directa, se citata, compare con avvertenza esplicita di inaffidabilità (eredità AUDIT-RM-RETRO CAP-DATA-02).
- [ ] **AC-G3 (RM-2 — citazioni di codice puntuali)**: se la spec cita decoder/parser DAPI esistenti (es. schema CANDLE, sintassi CANDLERANGE, header CSV legacy), le citazioni sono `[CODICE-ESISTENTE <path>:<linea>]` puntuali e verificabili dal Reviewer con Read. Atteso: ≤5 citazioni codice (il documento è di prodotto, non tecnico-implementativo); ogni citazione corretta token-per-token.

### AC di tracciabilità

- [ ] **AC-G4 (tracciabilità requisito → metodologia)**: ogni requisito `R-N` / `NFR-N` / `CN-N` introdotto in Sezioni 1-9 ha colonna "capitolo metodologia v2 di origine" non vuota. Requisiti senza tracciabilità = BUG REALE.
- [ ] **AC-G5 (matrice di tracciabilità completa)**: la sezione 10 contiene una matrice riassuntiva con ≥30 righe. Capitoli metodologia v2 non tracciati hanno motivazione esplicita di esclusione (sotto-sezione "Capitoli non tracciati e motivazione").
- [ ] **AC-G6 (no contraddizioni con CAP chiusi)**: nessuna asserzione della spec contraddice un fatto / una decisione chiusa in CAP-01..CAP-DATA-03. Il Reviewer verifica per scrupolo i punti più rischiosi (vincolo "solo emissione", state machine 1+6, target_2 informazione, 80pt minimo, tick FIB 5pt, sessione 8-22 CET, M-2 ancora open, $L_{warmup}=30$gg, riconciliazione bloccante).

### AC di valore di prodotto

- [ ] **AC-G7 (valore operativo dichiarato)**: ogni requisito ha una colonna o nota di "valore operativo per l'operatore retail" o "valore di prodotto / business per il committente". Requisiti senza valore operativo dichiarato = BUG REALE (criterio di valore del track).
- [ ] **AC-G8 (M-2 incardinato come dipendenza aperta)**: NFR-N di latenza Telegram $L_{max}=30$ s è presente in Sezione 5; M-2 OPEN è dichiarata esplicitamente come dipendenza aperta verso Appendice E / FASE-D, non risolta dalla spec corrente. La verifica empirica resta carryover.
- [ ] **AC-G9 (out-of-scope sistematico)**: ogni sezione ha lista esplicita di "out-of-scope" dove serve (es. Sezione 3 non contiene matematica strutturale; Sezione 7 non contiene formule DSR/PBO; Sezione 9 non contiene dettagli FASE-D). Sezione 10 contiene il quadro complessivo out-of-scope (PHASE-2, FASE-D, consulenza legale, contratti commerciali).

### AC editoriali

- [ ] **AC-G10 (lunghezza target)**: 12-16 pagine totali; deviazione ≥20% = finding non-bloccante (MIGLIORA PROCESSO), ≥40% = BUG REALE (la spec o è amputata o è bloated).
- [ ] **AC-G11 (italiano formale, tecnico, conciso)**: stile coerente con i CAP della metodologia v2. Niente paragrafi divulgativi non necessari.
- [ ] **AC-G12 (formato output)**: file `docs/spec_funzionale/SPEC_FUNZ_01.md` (cartella nuova), `reports/REPORT_SPEC_FUNZ_01.md` con le 5 sezioni del formato supervisore. Commit con tag `[SPEC-FUNZ-01]` (v1 / v2 / ... per iterazioni). Nessun altro file modificato dal Developer in v1 (l'indice `00_indice.md` NON va modificato — questa spec NON è una Parte della metodologia v2; eventuale aggiunta di rinvio in `00_indice.md` è decisione del Planner a chiusura PASS, non in v1).

### AC di review (vincoli per il Reviewer)

- [ ] **AC-G13 (Reviewer applica RM-1 a se stesso)**: ogni "verificato", "MATCH", "coerente", "non trovato dopo grep" del Reviewer ha sostegno operativo (citazione + esito) nell'audit. Sezione finale "Applicazione RM-1 a me stesso" nella review.
- [ ] **AC-G14 (Reviewer non riapre CAP chiusi)**: il Reviewer NON contesta decisioni metodologiche dei CAP-XX chiusi PASS. Le usa come autoritative. Se trova che la spec contraddice un CAP, il finding è sulla **spec** (BUG REALE), NON sul CAP.
- [ ] **AC-G15 (RACC-METODO-2 applicata)**: se la spec cita uno schema-dato esterno (CANDLE, PRICE, BOOK_5, manifest, header CSV), il Reviewer applica RACC-METODO-2 e verifica il diff puntuale col decoder canonico `scripts/export_directa_history_parametric.py`. Cita comando e esito.

---

## Out-of-scope esplicito — Developer NON include questi argomenti

Per ogni argomento out-of-scope: motivazione e destinazione.

- **Riderivare matematica del modello** (EGARCH, Cox, NSGA-II, walk-forward, DSR, PBO, bootstrap). **Destinazione**: già chiusi in Cap.13 Parte III, Cap.19 Parte IV, Cap.22-26 Parte V, Cap.32-34 Parte VII. La spec cita questi capitoli come fatti chiusi.
- **Ridichiarare schemi DAPI** (CANDLE, PRICE, BOOK_5, manifest JSON). **Destinazione**: già chiusi in Cap.48-49 Parte 9 + Cap.62 Parte 10 + audit RM-RETRO CAP-DATA-01/02 + AUDIT-RM CAP-DATA-03. La spec li cita per riferimento al massimo, mai per ridefinirli.
- **Parametri congelati del cromosoma** ($b_{min}$, $n_c$, $\delta_{pivot}$, $\lambda$, $W$, $p$, $N_{reg}$, $T_{persist}$, $W_{norm}$, $T_{warmup,\text{EMA}}$, $T_{warmup,\text{norm}}$, $A_{range,min}=80$, $N_{osc}$, $n_{osc,min}$, $\epsilon_{osc}$, $N_{break}$, $\delta_{break}$, etc.). **Destinazione**: già congelati in tabella Cap.26.5 Parte V. La spec ne cita i nominali se serve (es. 80pt, $b_{min}=5$), non li riapre.
- **Parametri di tuning provvisori Parte VII** ($\theta_{DSR}, \theta_{PBO}, \theta_{f_5}, \theta_{IQR}, \theta_{t_2}, \epsilon_{f_1}, \theta_{CVaR}, \theta_{MDD}, \theta_{sessions}, S, L_{avg}, \theta_{cost}$). **Destinazione**: rimasti non congelati in Parte VII, ricalibrati post-go-live. La spec li cita come gate qualitativi senza fissarne il valore.
- **Implementazione FASE-D** (codice runtime, pipeline ingest-feature-inference-publish, microservizi, framework, CI/CD, deployment AWS, bot Telegram). **Destinazione**: fuori scope della spec; SPEC-FUNZ-01 fornisce la base requisiti, non l'implementazione. FASE-D sarà oggetto di task / spec separati.
- **PHASE-2 cross-index** (DAX, EuroStoxx50, ES, MES futures). **Destinazione**: fuori scope (Cap.42 Parte 8, Cap.55 Parte 9, Cap.64 Parte 10). Sezione 10 dichiara esplicitamente la fasizzazione.
- **Consulenza legale formale / testo dei disclaimer**. **Destinazione**: fuori scope (materia di consulente legale esterno; la spec dichiara il posizionamento di compliance, non scrive il legalese).
- **Contratti commerciali con vendor** (Portara/CQG, AWS, Directa SIM, Telegram). **Destinazione**: fuori scope (materia di consulente acquisti / sales del committente).
- **Tutorial per l'operatore / manuale d'uso del bot Telegram**. **Destinazione**: fuori scope (sarà materia di documentazione FASE-D post-go-live).
- **Analisi di mercato / benchmark competitivo** ("segnali simili sul mercato"). **Destinazione**: fuori scope (è un documento di requisiti del prodotto, non un business plan / pitch deck).
- **Roadmap di progetto con date / milestone**. **Destinazione**: fuori scope (Sezione 10 cita fasizzazione PHASE-1/PHASE-2 / ponte FASE-D senza date specifiche; la pianificazione temporale è responsabilità del committente).
- **Riapertura M-2 (verifica empirica latenza Telegram)**. **Destinazione**: M-2 OPEN resta dipendenza FASE-D / Appendice E. Sezione 5 la dichiara, non la risolve.
- **Modifica `docs/methodology_v2/00_indice.md`** in v1 del Developer. **Destinazione**: l'indice è la fonte dello stato della metodologia v2 (Parti I-X tutte PASS). SPEC-FUNZ-01 non è una Parte della metodologia. Eventuale aggiunta di rinvio decorativo in `00_indice.md` è decisione del Planner a chiusura PASS (non in v1 Developer).
- **Apertura di nuove Q-XX in `tasks/QUESTIONS.md`**. **Destinazione**: l'audit / la review può aprire Q-XX se trova ambiguità non risolvibili dai documenti; il Developer NON apre Q-XX di sua iniziativa (la spec non è un track di decisioni metodologiche aperte).
- **Audit retroattivo dei CAP chiusi**. **Destinazione**: tutti gli audit RM-RETRO / RM sono task separati già chiusi PASS (CAP-DATA-01, CAP-DATA-02, CAP-DATA-03). La spec assume i CAP come autoritativi.
- **Nuova probe empirica DAPI / Telegram / Portara**. **Destinazione**: il track non produce fatti empirici (vincolo di sede WEB Reviewer; criterio "il track consolida fatti chiusi"). Eventuali residui empirici (M-2; codici 1030; riavvio Darwin mezzanotte; mesi Mar/Dic; etc.) restano carryover di sessioni FASE-D / CLI future.

---

## Done when — domande operative a cui SPEC-FUNZ-01 deve rispondere

La spec, una volta PASS, deve rispondere univocamente a queste domande:

1. **Cosa è il prodotto?** Sezione 1 risponde in ≤3 righe di proposta di valore + lista chiusa di out-of-scope di prodotto.
2. **Chi lo consuma e in quale contesto?** Sezione 2 risponde con personas + ambiente di esecuzione utente.
3. **Cosa contiene il segnale pubblicato?** Sezione 3 risponde con tabella ≥9 voci del payload + invariante immutabilità + segnale unico attivo + filtro 80pt.
4. **Come vive l'operatore il ciclo di vita del segnale?** Sezione 4 risponde con diagramma state machine 1+6 + significato di ciascun terminale in vista operatore + distinzione segnale vs position lifecycle.
5. **Come e con quale SLA viene consegnato?** Sezione 5 risponde con formato Telegram + 9 voci minime + NFR latenza $L_{max}=30$ s + M-2 come dipendenza aperta.
6. **Quali vincoli operativi/di sessione si applicano?** Sezione 6 risponde con sessione 8-22 + sizing 1 contratto + segnale unico + commissioni + rollover.
7. **Come si misura il successo?** Sezione 7 risponde con KPI di prodotto + DSR/PBO come gate go-live + checklist AC-GO-1..AC-GO-12 di Cap.36.
8. **Quali vincoli normativi / di compliance si applicano?** Sezione 8 risponde con posizionamento "segnale informativo MiFID II retail" + separazione segnale/esecuzione + retention audit log.
9. **Quali dati e infrastrutture servono?** Sezione 9 risponde con tabella dipendenze ≥6 voci.
10. **Dove siamo nel percorso e dove si va?** Sezione 10 risponde con PHASE-1 vs PHASE-2 + ponte FASE-D + dipendenze aperte + matrice di tracciabilità ≥30 righe.
11. **Ogni requisito traccia a un capitolo metodologia v2?** AC-G4 + AC-G5 + matrice Sezione 10.
12. **Ogni requisito ha un valore operativo dichiarato?** AC-G7.
13. **La spec contraddice un fatto chiuso nei CAP?** AC-G6 dice di no; il Reviewer verifica.
14. **M-2 (latenza Telegram empirica) è gestita correttamente?** AC-G8 dice come: NFR fissato in Sezione 5, verifica come dipendenza FASE-D/Appendice E.
15. **Capitoli metodologici non tracciati hanno motivazione?** AC-G5 dice di sì; Sezione 10 contiene la sotto-sezione "Capitoli non tracciati e motivazione".

---

## Pipeline attesa

```
Planner (questo task card)
  ↓ Orchestratore committa task card
Developer v1 (Web, scrive docs/spec_funzionale/SPEC_FUNZ_01.md + reports/REPORT_SPEC_FUNZ_01.md, push diretto su origin/main)
  ↓ DEV_STATUS = READY_FOR_REVIEW
Check post-Developer dell'Orchestratore (6 controlli standard CLAUDE.md):
  • file SPEC_FUNZ_01.md esiste e non vuoto
  • file REPORT_SPEC_FUNZ_01.md esiste con 5 sezioni
  • indice metodologia v2 NON modificato (eccezione del task)
  • working tree pulito
  • commit pushato
  • commit copre i file attesi
  ↓ se OK
Reviewer v1 (Web, sede WEB dichiarata; modalità CAP-review adattata al non-CAP)
  ↓ verdetto PASS / CONDITIONAL / FAIL
  ↓ se PASS → chiusura sessione + indice metodologia v2 NON tocco (decisione Planner sulla pertinenza di un rinvio "vedi anche" è separata)
  ↓ se CONDITIONAL/FAIL → punto di controllo supervisore con tabella classificazione BUG REALE / MIGLIORA PERFORMANCE / NEUTRO / RISCHIO PEGGIORAMENTO
  ↓ fix Developer v2 sui finding approvati → Reviewer v2 → ... → PASS
```

**Vincoli per il Developer v1**:
- Scrive `docs/spec_funzionale/SPEC_FUNZ_01.md` + `reports/REPORT_SPEC_FUNZ_01.md`. **Crea la cartella** `docs/spec_funzionale/` con il commit.
- Legge come prima azione `tasks/METODO.md` (RM-1..RM-4). Poi questo `ACTIVE_TASK.md`. Poi i CAP della metodologia v2 pertinenti (almeno: CAP-01 Parte I; CAP-02 Parte II Cap.6-11; CAP-06 Parte VI Cap.27-30; CAP-07 Parte VII Cap.31-36; outline Appendice E in `00_indice.md`; CAP-08 Parte 8; CAP-09 Parte 9; CAP-10 Parte 10).
- **NON riapre AC dei CAP chiusi**; **NON contraddice decisioni `D-*-N`**; **NON ridichiara schemi DAPI**; **NON dichiara "verificato X"** come asserzioni di prima istanza (RM-1).
- Cita i capitoli v2 come autoritativi (`[DOC-INTERNO CAP_XX_*.md:NN]` o equivalente). Decoder canonico citato puntualmente se serve (RM-2).
- **NON modifica `00_indice.md`** né file `tasks/STATO_CORRENTE.md` né `tasks/CARRYOVER.md` né `tasks/QUESTIONS.md`.
- Aggiorna `tasks/DEV_STATUS.md` con `READY_FOR_REVIEW` quando ha finito. Push diretto su `origin/main` (Push policy).
- Self-review opzionale: il Developer può includere in fondo al documento una sezione "Self-review del Developer (RM-1..RM-3 applicate al consolidamento)" che dichiari: (a) lista delle asserzioni cita-CAP usate come premesse; (b) check che ogni asserzione cita-CAP è verificata leggendo il CAP referente; (c) etichette `[DOC-INTERNO]` / `[CODICE-ESISTENTE]` corrette. Non è obbligatoria perché la pipeline include Review formale piena (opzione B di RM-4), ma è consigliata.

**Vincoli per il Reviewer v1**:
- Sede WEB. NON esegue DAPI. NON apre socket. NON ri-verifica fatti chiusi dei CAP.
- Modalità di review: **CAP-review piena adattata** — verifica gli AC globali del task card (AC-G1..AC-G15) + AC sezione-per-sezione (sotto ciascuna sezione 1-10). Niente AC nuovi al di là di quelli del task card.
- Applica RM-1 a sé stesso (AC-G13).
- Applica RM-2 con grep nel repo sui pattern di dominio (schema CANDLE, sintassi CANDLERANGE, header CSV, marker Parte 9/Parte 10) se la spec cita questi schemi; conferma con Read del decoder canonico.
- Applica RM-3: verifica che ogni richiamo a wiki sia `[WIKI-HINT, da verificare]`.
- Applica RACC-METODO-2 (AC-G15) per ogni AC della spec su schemi esterni.
- Produce `reviews/REVIEW_SPEC_FUNZ_01_review.md` con: header (perimetro, sede, modalità); verdetto sintetico in apertura; check ostili per ogni sezione 1-10 con tabella `AC | Stato | Evidenza`; check ostili AC globali AC-G1..AC-G15; tabella di classificazione finding per il supervisore; sezione finale "Applicazione RM-1 a me stesso".
- Push diretto su `origin/main` con tag `[REVIEW] SPEC-FUNZ-01 — verdetto: <PASS|CONDITIONAL|FAIL>`.

**In caso di rework Developer (se supervisore approva finding)**:
- L'Orchestratore aggiorna questo `ACTIVE_TASK.md` con sezione "Finding di Review da risolvere" (solo finding approvati con classificazione BUG REALE / MIGLIORA PERFORMANCE — NEUTRO/RISCHIO PEGGIORAMENTO non vanno a Developer per default).
- Developer modifica `SPEC_FUNZ_01.md` e/o `REPORT_SPEC_FUNZ_01.md` con patch chirurgiche; aggiorna REPORT con sezione "Iterazione N — risposta ai finding di Review" prima/dopo + impatto valore di prodotto.
- Reviewer v2 verifica chiusura finding + nessuna regressione (≤ 3 iterazioni totali per terminazione del loop, CLAUDE.md regola di terminazione).

---

## Self-review del Planner (RM-1 applicato al task card)

Per coerenza con la regola RM-1 applicata anche al task card stesso, dichiaro esplicitamente le mie scelte di scope e le loro motivazioni:

- **VERIFICATO (level-3) — letti i CAP autoritativi**: ho letto `tasks/METODO.md` integrale, `docs/methodology_v2/00_indice.md` integrale (217 righe), `tasks/CARRYOVER.md` integrale (63 righe), `tasks/QUESTIONS.md` integrale (167 righe), `tasks/STATO_CORRENTE.md` r.1-141 integrale, `tasks/ACTIVE_TASK.md` precedente r.1-374 integrale, `CAP_01_parte_I.md` r.1-86 (Cap.1-5 integrali), `CAP_02_parte_II.md` r.1-80 (Cap.6.1 + Cap.6.2 + Cap.6.3 integrali), `CAP_05_parte_V.md` r.1-30 (intro Parte V + Cap.22 intro), `CAP_07_parte_VII.md` r.1-30 (intro Parte VII + Cap.31.1 con citazione esplicita di $L_{max}=30$ s e M-2 OPEN come carryover Appendice E). **ALTERNATIVE COMPATIBILI ESCLUSE**: ho escluso l'opzione "M-2 come dipendenza referenziata senza requisito esplicito" (opzione b dell'Orchestratore) perché un documento di prodotto deve dichiarare lo SLA consumer-facing; ho escluso l'opzione "spec con seed-outline diverso" (es. 8 sezioni o 15) perché 10 sezioni equilibrate coprono i 6 livelli classici di una spec funzionale (scopo, contesto, requisiti funzionali, requisiti non-funzionali, vincoli, roadmap) con granularità leggibile. **NON ESCLUSE**: non ho letto integralmente CAP-03 / CAP-04 / CAP-06 / CAP-08 / CAP-09 / CAP-10 — è esplicito che il Developer lo farà in fase di scrittura; il task card cita questi CAP come autoritativi senza re-derivarne il contenuto.

- **VERIFICATO (level-3)**: M-2 è l'unico M-promemoria di capitolo ancora OPEN in `CARRYOVER.md` (riga 21). Verifica fatta leggendo l'intera tabella (righe 19-37). Tutti gli altri M-N (M-1, M-4..M-16) sono CLOSED-CAP-XX con riferimento esplicito al capitolo di chiusura. **ALTERNATIVE ESCLUSE**: nessun altro M-N attivo.

- **VERIFICATO (level-3)**: M-2 destinazione è "Appendice E" (riga 21 di CARRYOVER). Cap.31.1 Parte VII conferma il rinvio empirico ad Appendice E (`CAP_07_parte_VII.md:23` "La **verifica numerica empirica** di $L_{max}$ effettivo del canale Telegram resta carryover di Appendice E (M-2 OPEN, Review v1 CAP-02)..."). **ALTERNATIVE ESCLUSE**: nessuna altra destinazione (Cap.30 Parte VI ha monitoring non-bloccante della latenza ma non risolve il valore di $L_{max}$).

- **VERIFICATO (level-2 / per costruzione del task card)**: ho costruito la decisione M-2 opzione (a) come scelta del Planner motivata; NON è un'ambiguità non risolvibile (non apro Q-XX). Motivazione: scope dei documenti di prodotto richiede SLA esplicito. Se il supervisore preferisse opzione (b) — referenza senza requisito — interviene al punto di controllo; il default è opzione (a).

- **NON dichiarato come "verificato" dal Planner**:
  - Non ho letto integralmente le Appendici (sono solo in outline nell'indice). Il Developer della spec NON deve scrivere il contenuto delle Appendici (sono futuro chapter della metodologia v2, fuori scope SPEC-FUNZ-01); deve solo citarle per rinvio.
  - Non ho letto integralmente i 65 capitoli della metodologia. I rinvii nel task card e nelle 10 sezioni sono al **livello giusto di granularità** per un Planner (capitolo + sezione, non riga); il Developer della spec, in fase di redazione, verifica ogni rinvio con Read e cita correttamente.
  - La lunghezza attesa (12-16 pp) è una stima del Planner basata su 10 sezioni di lunghezza media 1.2-1.6 pp; il Developer può deviare ≤20% senza finding (AC-G10).

- **AMBIGUITÀ POTENZIALI risolte come Planner (NON Q-XX)**:
  - Cartella nuova `docs/spec_funzionale/`: greenfield, decisa qui come default sensato (il documento non è una Parte della metodologia v2, quindi non va in `docs/methodology_v2/`; un nome neutro "spec_funzionale" è coerente con la natura del track).
  - Naming output `SPEC_FUNZ_01.md` (NON `SPEC-FUNZ-01.md`): coerente con convenzione progetto (snake_case + maiuscole sigle, vedi `CAP_10_parte_10.md`).
  - Modalità di review = opzione B (Reviewer formale leggero adattato), NON opzione A (self-review dell'autore) — perché il diff aggregato supererà 200 righe e il documento è destinato a essere citato altrove; criterio meccanico (c) di RM-4 (`CLAUDE.md`).
  - Sede Reviewer = WEB (NON CLI) — non c'è esecuzione contro DAPI; non c'è probe empirico; è documento + grep + Read di CAP committati.
  - PHASE-2 cross-index esplicitamente fuori scope: non è un'ambiguità (Cap.42 Parte 8 chiude la fasizzazione).
  - Modifica `00_indice.md` esplicitamente fuori scope dal Developer v1 — perché SPEC-FUNZ-01 NON è una Parte della metodologia v2; eventuale rinvio decorativo dall'indice è decisione del Planner a PASS, non patch del Developer.

---

## Checklist del "secondo giro di completezza" del Planner — autoverifica prima di pubblicare

- [x] Tutte le decisioni del supervisore (Q-XX chiuse) pertinenti sono citate nell'eredità (Q-01, Q-04, Q-05, Q-A-3 sono ereditati esplicitamente nei punti 4, 7, 8, 9, 10 della sezione "Eredità").
- [x] Tutti gli M-promemoria aperti delle Review precedenti sono stati censiti e assegnati: M-2 OPEN integrato nel task corrente (Sezione 5 + AC-G8); tutti gli altri M-N CLOSED-CAP-XX dichiarati esplicitamente.
- [x] Lo scope non lascia ambiguità su cosa è dentro e cosa è fuori (vedi sezione "Out-of-scope esplicito" con 14 voci).
- [x] Per ogni sezione del task ci sono acceptance criteria verificabili (Acceptance criteria sezione 1-10 + AC globali AC-G1..AC-G15).
- [x] La sezione "Out-of-scope" è esplicita e indica dove ciascun argomento rinviato verrà trattato (motivazione + destinazione per ogni voce).
- [x] La sezione "Done when" elenca 15 domande operative a cui il documento deve rispondere.
- [x] Non ci sono numeri o soglie inventati dal Planner: i numeri citati ($L_{max}=30$ s, 80pt, $b_{min}=5$, $L_{warmup}=30$gg, tick 5pt, sessione 8-22 CET, retention 90gg, 1 contratto, 5 EUR/op) sono tutti eredità di CAP-XX chiusi PASS, citati con riferimento al CAP di origine.
- [x] Il task ha un impatto identificabile per il committente / l'operatore (criterio reinterpretato del valore di prodotto, non del GA): SPEC-FUNZ-01 produce un documento di requisiti cantierabile da FASE-D e leggibile da esterni (consulenza legale MiFID II, valutatori AWS, fornitori Portara/CQG, fornitori bot Telegram); AC-G7 obbliga ogni requisito a dichiarare il proprio valore operativo / di prodotto.
- [x] **RM-1**: ogni "fatto verificato" preso da CAP precedenti come premessa è dichiarato come tale (eredità #1-13). Il task card NON introduce nuove dichiarazioni "verificato X" di prima istanza. AC-G1 estende il vincolo al Developer della spec.
- [x] **RM-2**: il task tocca parsing di sistemi esterni solo per richiamo. I decoder esistenti nel repo sono citati con path:linea (eredità #15). AC-G3 estende il vincolo al Developer.
- [x] **RM-3**: ogni riferimento futuro a wiki/docs esterni nel task è etichettato `[WIKI-HINT, da verificare]` (eredità #16). AC-G2 estende il vincolo al Developer.
- [x] **RM-4**: per output tecnici determinanti previsti dal task, la modalità di review è specificata (opzione B di RM-4 — Review formale leggera del Reviewer in modalità CAP-review adattata — perché il diff aggregato del commit supererà 200 righe e SPEC-FUNZ-01 introduce asserzioni destinate a essere citate in FASE-D; criterio meccanico (c) di RM-4 in `CLAUDE.md`). Sede Reviewer dichiarata: WEB.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---

## Finding di Review da risolvere (Review v1 PASS `d8a40a0` — 3 NEUTRO approvati dal supervisore — Iterazione v2)

**Contesto**: Review v1 ha emesso **PASS** (0 bloccanti, 0 BUG REALE). Il supervisore ha approvato l'applicazione dei 3 finding **NEUTRO** come micro-pass di igiene-citazione (iterazione v2). NON sono BUG REALI: la spec è già corretta e tracciabilmente solida. Patch **chirurgiche**, nessuna re-stesura. Dettaglio completo e mapping autorevole in `reviews/REVIEW_SPEC_FUNZ_01_review.md` (sezione "Osservazioni minori" OM-1/OM-2/OM-3 + tabella "Classificazione per il supervisore"). **Leggere quel file come fonte dei mapping esatti.**

- **OM-1** — correggere i 6 numeri di riga citati che puntano all'intestazione del capitolo / riga adiacente invece che alla riga esatta dell'asserzione. **Verificare OGNI nuovo numero con Read di `docs/methodology_v2/...` PRIMA di scriverlo** (RM-1: la citazione deve risolvere alla riga esatta). Mapping (da review OM-1):
  - `[DOC-INTERNO CAP_10_parte_10.md:11]` → `:5` (invariante research=runtime esteso al ciclo di vita del tape)
  - `[DOC-INTERNO CAP_10_parte_10.md:74]` → `:76` (limite ~100gg)
  - `[DOC-INTERNO CAP_10_parte_10.md:151]` → riga esatta del corpo Cap.61 col fallback Portara (review indica r151=header: trovare la riga del costrutto con Read)
  - `[DOC-INTERNO CAP_10_parte_10.md:226]` → `:236` (cross-index PHASE-2 fuori scope PHASE-1)
  - `[DOC-INTERNO CAP_10_parte_10.md:234]` → `:233` (riavvio Darwin mezzanotte, residuo Empirico-CLI)
  - `[DOC-INTERNO CAP_07_parte_VII.md:574]` → `:576` (AC-GO-4 lifecycle cross-regime)
- **OM-2** — `SPEC_FUNZ_01.md` R-17 (Sez.6): rimuovere "per direzione" dal **titolo** di R-17; il vincolo corretto $|\mathcal{A}(t)|\le 1$ **globale** è già enunciato in-linea — allinearlo a R-7 (Sez.3.2). Verificare che il constraint resti $|\mathcal{A}(t)|\le 1$ (`CAP_02_parte_II.md:81`/`:87`).
- **OM-3** — `SPEC_FUNZ_01.md` Sez.9.2: aggiungere l'ancora puntuale `[DOC-INTERNO STATO_CORRENTE.md:76]` (M-9) come provenienza della numerazione `f4/f6/f8/f9` dello schema PRICE, mantenendo il richiamo descrittivo a `CAP_09_parte_9.md`.

**Output Developer v2**:
- Patch chirurgiche a `docs/spec_funzionale/SPEC_FUNZ_01.md` (solo le 3 zone OM-1/2/3; nessun'altra modifica).
- Sezione nuova `## Iterazione 2 — risposta ai finding di Review` in `reports/REPORT_SPEC_FUNZ_01.md`: per ogni OM, cosa cambiato + riga prima/dopo + impatto (nullo sulla correttezza, +precisione di citazione).
- **NON** modificare i CAP, `00_indice.md`, `STATO_CORRENTE.md`, `CARRYOVER.md`. Commit tag `[SPEC-FUNZ-01]` v2, push su `origin/main`. `DEV_STATUS` → `READY_FOR_REVIEW`.
- Re-review **leggera focalizzata** attesa (conferma OM-1/2/3 + nessuna regressione).
