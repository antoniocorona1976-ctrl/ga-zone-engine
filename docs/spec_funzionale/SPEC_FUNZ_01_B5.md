# SPEC_FUNZ_01 — Blocco B5: Runtime DAPI, sessione & compliance

> **Track**: Business-spec (SPEC-FUNZ). **Blocco**: 5 di 8 (blocco unico). **Tag**: `[SPEC-FUNZ-01-B5]`.
> **Natura**: ricostruzione cieca (modalità B) del perimetro runtime/sessione/compliance (Sez.7 della v2).
> **Fonte-perimetro**: `docs/methodology_v2/CAP_09_parte_9.md` (Cap.46, 47, 52, 53, 54; Cap.45/50 inquadramento/contesto) + `docs/methodology_v2/CAP_01_parte_I.md` (Cap.1, tocco). Capitoli chiusi PASS, congelati (freeze G-09): qui consolidati, non ri-verificati.

---

## 1. Scopo, schema-ID e conferma cecità

### 1.1 Scopo

Questo blocco consolida i requisiti funzionali di **prodotto** del runtime DAPI per la pubblicazione di segnali FIB in produzione: come si connette il canale dati, quale contratto si sottoscrive e come si gestisce il rollover, qual è la finestra operativa, come entrano i cash europei come contesto, e cosa registra l'audit log. È il ponte fra la metodologia v2 (Parte 9) e la FASE-D implementativa.

### 1.2 Schema degli identificatori

- `B5-R-NN` — requisito funzionale operativo (comportamento osservabile del runtime).
- `B5-CN-NN` — vincolo (constraint) / invariante di sistema o di replay.
- `B5-NFR-NN` — requisito non-funzionale (compliance, retention, sicurezza locale).

Ogni requisito è **atomico** (una sola proposizione verificabile, N1), porta la **tracciabilità** alla riga-fonte `[DOC-INTERNO <file>:<riga>]` e un **valore dichiarato** (operativo di prodotto, oppure di sistema/replay per gli invarianti).

### 1.3 Conferma di cecità (§0.1 della card)

I requisiti di questo blocco sono derivati **dai soli** capitoli del perimetro-fonte sopra. Nessun ID-requisito, contenuto o numerazione è stato importato da `SPEC_FUNZ_01.md` (v2 congelata), da `*_v1_storico*`, dai file di chunking (`PROPOSTA_SUDDIVISIONE_SPEC*.md`) o dai documenti dei blocchi B1/B2/B3/B4. Gli ID `B5-*` sono auto-assegnati da zero. Il confronto-copertura con la v2 è compito del Reviewer.

### 1.4 Premesse vs derivazioni (CARDINE di B5)

B5 tocca molti blocchi vicini. Regola: **consolida il fatto runtime/sessione/compliance; cita come premessa ciò che vive altrove, non lo ri-deriva.** Le premesse citate (e non consolidate) in questo documento sono raccolte nella **§7 — Matrice di tracciabilità e nota di rinvio**. Nessun requisito `B5-*` consolida materia di B1/B2/B3/B4/B6/B7/B8.

---

## 2. Canale DAPI (Cap.46)

Il canale dati live del runtime è **Directa DAPI** sul gateway Darwin, servizio locale `[DOC-INTERNO CAP_09_parte_9.md:27]`.

### B5-R-01 — Connessione esclusiva in loopback
La pipeline runtime si connette al gateway Darwin **esclusivamente in loopback su `127.0.0.1`**, mai da rete esterna o da macchina diversa.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:27]`.
*Valore*: operativo — il modello di sicurezza locale-only è la condizione perché l'operatore possa far girare il runtime sulla propria macchina senza esporre il canale; nessuna superficie di rete da proteggere.

### B5-R-02 — Sottoscrizione datafeed sulla porta 10001
La pipeline apre la porta **`10001`** (datafeed realtime) per ricevere il push di mercato (`PRICE`, `BOOK_5`, `ANAG`) sul FIB front-month e sui cash europei.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:35]`.
*Valore*: operativo — è la porta che alimenta l'inference live con i tick di mercato.

### B5-R-03 — Richieste storico sulla porta 10003
La pipeline apre la porta **`10003`** (richieste storico: `CANDLERANGE`, `CANDLE`, `TBT`, `TBTRANGE`) per il pull storico (warm-up degli stati condizionali al boot, fino a 100 giorni).
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:37]`.
*Valore*: operativo — alimenta il warm-up necessario perché la pipeline non parta con stato non inizializzato.

### B5-CN-01 — La porta ordini 10002 non è mai aperta
La porta **`10002`** (submission ordini) **non è mai aperta** dalla pipeline runtime.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:39]`.
*Valore*: di sistema — è la clausola di chiusura architetturale del vincolo "solo emissione, nessuna esecuzione": il sistema pubblica segnali, l'operatore esegue manualmente. La premessa "no order routing" come scelta di prodotto vive in `CAP_01 Cap.1`/Cap.9 (vedi §7); qui si consolida il fatto runtime che la porta resta chiusa.

### B5-R-04 — Handshake via banner con prefix-match
Alla connessione la pipeline riconosce il gateway tramite il **banner** `DARWIN_STATUS;CONN_OK;TRUE;Release ...` con **prefix-match** sul prefisso `DARWIN_STATUS;CONN_OK;TRUE;Release`, **non** match esatto sull'intera stringa.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:29]`. Banner osservato `DARWIN_STATUS;CONN_OK;TRUE;Release 2.5.1 build 04/02/2025` `[PROVA-EMPIRICA 2026-05-27, CAP_09_parte_9.md:27,29]`.
*Valore*: operativo — il prefix-match rende l'handshake robusto al cambio di release del gateway (campo variabile), evitando falsi fallimenti di connessione a ogni aggiornamento Darwin.

### B5-NFR-01 — File `APIPortSettings.txt` come dato PII, sola lettura, escluso dal repo
Il file `APIPortSettings.txt` (identificatore locale di account + porte) è **letto in sola lettura** dalla pipeline (mai scritto), è trattato come **dato sensibile / PII** ed è **escluso dal repo via `.gitignore`**.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:41,43]`.
*Valore*: di sistema (compliance) — l'account code lega un'azione di mercato a una persona fisica; la sola-lettura e l'esclusione dal repo sono la garanzia di non versionare un dato personale.

### B5-CN-02 — Uso esclusivo del canale (D-6): nessun workaround automatico
In presenza di conflitto sul gateway (sessione DGo o TradingView-Directa concorrente sui socket `127.0.0.1:10001`/`10003`), la pipeline **non tenta workaround automatici**: rileva il conflitto, marca lo stato `RUNTIME_DEGRADED` in audit, notifica il supervisore via Telegram ed esce. La decisione di rimedio è del supervisore, non automatica.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:45]`.
*Valore*: operativo — evita che la pipeline mascheri un conflitto di canale con retry ciechi; consegna al supervisore una diagnosi netta (chiudere DGo/TradingView).

### B5-CN-03 — Una singola connessione persistente per porta
La pipeline usa **una sola connessione persistente per porta** (10001 e 10003), mai aperture/chiusure per comando.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:47]`.
*Valore*: di sistema — scelta architetturale prudente che evita per costruzione qualunque regime di burst di connessioni, indipendentemente dalla soglia di cooldown (la soglia "14 conn / ~30 s" è verifica parziale RM-1, smentita come costante nel regime ~1Hz `[DOC-INTERNO CAP_09_parte_9.md:47,51]`).

---

## 3. Catalogo simboli & rollover (Cap.47)

Il catalogo dei simboli del runtime FIB è chiuso e fissato `[DOC-INTERNO CAP_09_parte_9.md:57]`.

### B5-R-05 — Sottoscrizione del FIB pieno front-month per l'inference
La pipeline sottoscrive il **FIB pieno front-month** (`FIB6F` o `FIB6I` secondo il front-month corrente) sulla porta 10001 per il calcolo delle feature e la valutazione del bundle.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:75]`. Convenzione ticker IDEM `<CODE><YEAR><MONTH>` `[DOC-INTERNO CAP_09_parte_9.md:61]`.
*Valore*: operativo — è lo strumento su cui il motore calcola e valuta i segnali, coerente con la calibrazione sul FIB pieno (premessa B1, moltiplicatore 5€/pt — vedi §7).

### B5-R-06 — Derivazione automatica del front-month via ANAG
Al boot la pipeline **deriva automaticamente** il ticker front-month: esegue SUB sui ticker candidati, ne parsa la risposta `ANAG`, estrae la data di scadenza dalla descrizione (es. `GIU26`, `SET26`) e seleziona il **primo contratto in scadenza non ancora oltrepassato**.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:96]`.
*Valore*: operativo — il runtime non richiede configurazione manuale del contratto: si auto-allinea al front-month corrente leggendo l'anagrafica.

### B5-R-07 — Codici mese Directa-IDEM noti: F=giugno, I=settembre
La decodifica del codice mese segue la convenzione proprietaria Directa-IDEM (non lo standard CME): il codice **`F` = giugno** e il codice **`I` = settembre** sono i codici noti usati dal runtime.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:61]`. `FIB6I`=settembre 2026 `[PROVA-EMPIRICA 2026-05-27, CAP_09_parte_9.md:61]`; `FIB6F`=giugno 2026 `[PROVA-EMPIRICA 2026-05-29 M-4, CAP_09_parte_9.md:61]`.
*Valore*: operativo — la decodifica corretta del mese è ciò che permette di selezionare il contratto giusto al boot e al rollover.
*Nota*: la lookup completa oltre `F`/`I` (in particolare i codici di **marzo e dicembre**) è **PENDING-empirico** (da derivare via ANAG a mercato aperto, fuori scope Cap.55) `[DOC-INTERNO CAP_09_parte_9.md:61]` — vedi §7.4.

### B5-R-08 — Switch al next-month al boot del giorno di scadenza (CONTRACT_SWITCH)
Allo **scadere del front-month** (terza venerdì del mese, negoziazione che chiude alle 09:00 CET), la pipeline **al boot della sessione del giorno di scadenza** sottoscrive direttamente il **next-month**, saltando la finestra 08:00–09:00 CET del front in scadenza; non sottoscrive il front in scadenza.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:98]`, `[DOC-INTERNO CAP_09_parte_9.md:104]`.
*Valore*: operativo — evita di propagare la discontinuità da settlement (liquidità marginale + evento delle 09:00) nello stato condizionato EGARCH del bundle frozen.

### B5-R-09 — Marker CONTRACT_SWITCH in audit al rollover
Al rollover la pipeline registra in audit (Cap.54) il marker **`CONTRACT_SWITCH`** con payload `{from, to, scadenza_from, trigger: "boot_session_third_friday"}`.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:103]`.
*Valore*: operativo/compliance — traccia esplicita del cambio di contratto, necessaria per ricostruire a posteriori quale strumento era attivo in ciascuna sessione.

### B5-CN-04 — Lo switch di runtime è distinto dal filtro pre-expiry di training
Lo switch di runtime (dal giorno di scadenza `t` in poi sul next-month, operatività normale fino a `t-1` sul front) è **distinto e non sovrapposto** al filtro pre-expiry di **training** ($N=3$ giorni `t-3..t-1`, Parte 8 Cap.39): le due regole non coincidono.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:107]`.
*Valore*: di sistema — preserva l'invariante research = runtime senza confondere una regola di training con una di runtime; previene un errore di sovrapposizione.

### B5-R-10 — Dualità strumento: calibrazione/inference su FIB pieno, esecuzione operatore su miniFIB
Il runtime calibra e valuta sul **FIB pieno** (`FIB6F`/`FIB6I`), mentre l'**operatore retail esegue manualmente sul miniFIB** (`MINI6F`/`MINI6I`/…, 1 EUR/pt). La separazione fra strumento di calibrazione/inference e strumento di esecuzione è fattuale nel runtime.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:75]`. miniFIB 1 EUR/pt come strumento di esecuzione operativa `[DOC-INTERNO CAP_09_parte_9.md:69]`.
*Valore*: operativo — chiarisce all'operatore su quale strumento agire (mini, 1€) rispetto a quello su cui il motore ragiona (pieno). Il moltiplicatore **5 EUR/pt del FIB pieno** è premessa di B1 (vedi §7), qui non ri-asserito; B5 consolida la parte miniFIB (1€, esecuzione).

---

## 4. Sessione operativa (Cap.52)

### B5-R-11 — Finestra operativa 08:00–22:00 CET
La pipeline runtime opera **esclusivamente** nella finestra **08:00–22:00 CET** (epoca corrente E5).
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:273]`.
*Valore*: operativo — definisce quando il motore è attivo; è la finestra in cui i segnali sono emessi e processati. L'origine normativa della finestra (epoca E5 / `fib_session_calendar.csv`) è premessa di B8 Cap.41 (vedi §7); qui si consolida la regola operativa.

### B5-R-12 — Stand-by fuori sessione
Fuori dalla finestra 08:00–22:00 CET la pipeline è in **stand-by**: resta connessa al gateway per il monitoraggio del riavvio mezzanotte, **non emette segnali e non valuta il bundle**.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:273]`.
*Valore*: operativo — il runtime non produce segnali fuori orario, ma non perde la connessione né lo stato.

### B5-R-13 — Marker SESSION_OPEN all'apertura
All'apertura di sessione (08:00 CET di ogni giorno di trading) la pipeline verifica il banner, esegue il warm-up, sottoscrive FIB front-month + cash opzionali, e registra il marker **`SESSION_OPEN`** in audit con timestamp UTC e data sessione; da quel momento è in regime steady-state.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:294]`, `[DOC-INTERNO CAP_09_parte_9.md:299]`.
*Valore*: operativo/compliance — delimita l'inizio dell'operatività della sessione in modo tracciabile.

### B5-R-14 — Marker SESSION_CLOSE e UNSUB cash alla chiusura
Alla chiusura (22:00 CET) la pipeline registra il marker **`SESSION_CLOSE`** in audit con timestamp UTC, esegue **UNSUB** delle sottoscrizioni realtime sui cash europei, e conserva la connessione storica per il monitoraggio del riavvio mezzanotte.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:302]`.
*Valore*: operativo — chiude in modo ordinato la sessione liberando le sottoscrizioni di contesto, senza perdere la connessione di servizio.

### B5-CN-05 — La chiusura 22:00 non chiude un segnale `active`
Un segnale in stato **`active`** alla chiusura 22:00 CET **non viene chiuso automaticamente** dalla pipeline: la transizione terminale è governata esclusivamente dal counter cromosoma-specifico della state machine (timer post-trigger $\Delta t_{cromosoma}$), **mai dalla chiusura di sessione**.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:292]`, `[DOC-INTERNO CAP_09_parte_9.md:302]`.
*Valore*: di sistema — preserva la semantica multiday del segnale: il dominio temporale (fino a ~due giornate, $\Delta t$ fino a 1680 min) scavalca l'interruzione notturna. La state machine e i suoi stati terminali sono premessa di B3 Cap.7 (vedi §7); qui si consolida la sola regola "22:00 non chiude active".

### B5-CN-06 — Persistenza dello stato del segnale attraverso l'interruzione notturna
Fuori sessione la pipeline **mantiene lo stato del segnale `active` in memoria persistente** (su disco); al boot del giorno successivo lo riprende e, se il counter $\Delta t_{cromosoma}$ è scaduto fuori sessione, applica la transizione al primo boot utile marcandola in audit con timestamp coerente.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:292]`.
*Valore*: di sistema/replay — garantisce continuità del lifecycle del segnale fra sessione `d` e `d+1`, coerente con l'invariante research = runtime.

---

## 5. Gating cash europei (Cap.53)

### B5-R-15 — Cash europei come logging operativo di contesto
I cash europei accessibili gratuitamente via DAPI base (DGER=DAX, DSTX50=EuroStoxx50, DITAS=FTSE MIB cash, DFRA=CAC 40) entrano nella pipeline come **logging operativo**: i loro tick `PRICE` sono loggati in audit come canale di contesto, in osservazione passiva.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:310]`. Catalogo cash `[DOC-INTERNO CAP_09_parte_9.md:308]`.
*Valore*: operativo — fornisce contesto di mercato registrato per debug/analisi post-hoc, senza toccare il motore.

### B5-R-16 — Gating qualitativo POST-EMISSIONE come annotazione del messaggio Telegram
Il **gating qualitativo** opera **dopo** l'emissione del segnale ed esclusivamente sul **payload del messaggio Telegram**: aggiunge una **nota di avvertimento** (es. `[GATING-cash-europei: DGER -2.3% intraday]`) basata sulla condizione cash osservata al momento dell'emissione, senza modificare la decisione di emettere né il contenuto strutturale del segnale (banda, target_1, stop).
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:311]`, `[DOC-INTERNO CAP_09_parte_9.md:324]`.
*Valore*: operativo — dà all'operatore un'avvertenza di contesto sul messaggio, lasciandogli la decisione manuale. Il **contratto del messaggio Telegram** è premessa di B4 (vedi §7); qui si consolida solo l'attacco dell'annotazione di gating.

### B5-CN-07 — Il gating non sopprime mai l'emissione del segnale
Il gating qualitativo **non sopprime mai** l'emissione: il segnale è **sempre emesso** dalla state machine, sempre tracciato in audit con `SIGNAL_EMITTED`, sempre conteggiato nelle metriche di lifecycle.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:311]`.
*Valore*: di sistema — separa nettamente la decisione di emettere (motore) dall'annotazione informativa (payload pubblicato); è la condizione che mantiene il gating fuori dalla logica decisionale del segnale.

### B5-CN-08 — Il cash europeo è fuori dal GA (feature/cromosoma/state machine/walk-forward)
Il cash europeo **non entra** nel feature tensor del GA, **non entra** nella state machine del segnale, **non entra** nel cromosoma e **non entra** nel walk-forward nested.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:315]`, `[DOC-INTERNO CAP_09_parte_9.md:316]`, `[DOC-INTERNO CAP_09_parte_9.md:317]`, `[DOC-INTERNO CAP_09_parte_9.md:318]`.
*Valore*: di sistema — vincolo di perimetro hard che tiene il motore single-instrument FIB; nessun parametro `cash_eur_threshold` né regola "if DGER drop then blocca" entra nel motore.

### B5-NFR-02 — Regole di gating in config versionato fuori dal genoma
Le regole di gating qualitativo vivono in un **file di configurazione versionato** fuori dal genoma del bundle (`config/gating_rules.yaml`), modificabile **senza re-training** del bundle.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:311]`, `[DOC-INTERNO CAP_09_parte_9.md:320]`.
*Valore*: operativo — cambiare una soglia di gating non richiede di ri-eseguire il walk-forward: separazione netta config/genoma.

### B5-R-17 — Marker GATING_RULE_APPLIED in audit con riferimento al signal_id
Quando una regola di gating è attiva, la nota aggiunta al messaggio è tracciata in audit come marker **`GATING_RULE_APPLIED`** con riferimento al `signal_id` della state machine.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:325]`.
*Valore*: operativo/compliance — rende l'annotazione di gating ricostruibile e legata al segnale a cui si riferisce.

### B5-CN-09 — Replay bit-exact preservato: il gating è meta-informazione fuori dal lifecycle del segnale
Lo **stesso segnale è sempre emesso** dal bundle frozen indipendentemente dal valore corrente di `config/gating_rules.yaml`; due replay sulla stessa finestra producono lo stesso event log `SIGNAL_EMITTED` con lo stesso payload strutturale, e solo il campo `nota_gating` del messaggio può variare. Le metriche lifecycle non sono inquinate dal gating (contano i segnali emessi, non i messaggi pubblicati).
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:328]`.
*Valore*: di sistema/replay — preserva il vincolo di replay deterministico bit-exact sull'event log del segnale.

---

## 6. Audit & compliance (Cap.54)

### B5-NFR-03 — Audit log strutturato, immutabile, append-only
L'audit log è **strutturato, immutabile e append-only** (mai sovrascritto), una riga per evento; formato consigliato JSON Lines con campi obbligatori `timestamp_utc`, `event_type`, `payload`.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:360]`.
*Valore*: di sistema/compliance — l'immutabilità append-only è la base della riproducibilità del replay e della prova storica del comportamento del motore.

### B5-R-18 — Contenuto loggato: comandi, risposte, transizioni, segnali, gating
Per ogni evento operativo il log registra timestamp UTC, tipologia evento (`HANDSHAKE`, `SUB`, `UNSUB`, `CANDLERANGE_REQUEST`, `CANDLE_RESPONSE`, `BOOK_RESPONSE`, `PRICE_RESPONSE`, `ANAG_RESPONSE`, `ERR`, `SESSION_OPEN`, `SESSION_CLOSE`, `WARMUP_COMPLETE`, `RUNTIME_*`, `CONTRACT_SWITCH`, eventi lifecycle del segnale, `GATING_*`) e payload strutturato.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:353]`, `[DOC-INTERNO CAP_09_parte_9.md:356]`.
*Valore*: operativo/compliance — copre l'intera traccia comandi-risposte-stato necessaria a ricostruire il comportamento del runtime.

### B5-R-19 — Eventi del lifecycle del segnale loggati per-stato (sei terminali distinti)
Gli eventi del lifecycle del segnale sono loggati **distinti per stato**: marker pre-terminali `SIGNAL_EMITTED`, `SIGNAL_TRIGGERED` e **sei eventi terminali distinti** (`SIGNAL_TARGET_1_HIT`, `SIGNAL_STOPPED`, `SIGNAL_INVALIDATED`, `SIGNAL_MISSED_TARGET`, `SIGNAL_EXPIRED`, `SIGNAL_REVOKED`), in luogo di un evento aggregato `SIGNAL_CLOSED`.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:353]`, `[DOC-INTERNO CAP_09_parte_9.md:355]`.
*Valore*: operativo — eventi puntuali per-stato consentono di calcolare metriche di lifecycle disaggregate senza ricostruzione a posteriori. I sei stati terminali e la state machine sono premessa di B3 Cap.7 (vedi §7); qui si consolida solo la granularità per-stato del log.

### B5-R-20 — Campo `timeout_cause` obbligatorio su SIGNAL_MISSED_TARGET
Per l'evento `SIGNAL_MISSED_TARGET`, il payload JSON registra il campo **obbligatorio** `timeout_cause ∈ {pretrigger, posttrigger}`, che distingue il timeout pre-trigger (raw touch non avvenuto entro $T_{touch}^{max}$) dal timeout post-trigger (trade aperto senza target_1 entro $\Delta t_{cromosoma}$).
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:355]`.
*Valore*: operativo — disambigua la causa del miss, abilitando metriche di miss-rate per causa.

### B5-NFR-04 — Banner Darwin e account code loggati su HANDSHAKE (PII mascherabile)
Il **banner Darwin** è loggato in `HANDSHAKE` (registrazione esplicita della release) e l'**account code** è loggato su `HANDSHAKE` come dato PII/sensibile: **mascherabile** negli export pubblici dell'audit, **in chiaro** nel log locale per replay deterministico.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:357]`, `[DOC-INTERNO CAP_09_parte_9.md:358]`.
*Valore*: di sistema/compliance — concilia riproducibilità del replay (banner+account in chiaro localmente) e protezione del dato personale (mascheratura negli export).

### B5-NFR-05 — Retention minima 90 giorni rolling
Ogni log file deve garantire accessibilità per **almeno 90 giorni rolling** dalla data di creazione (dalla creazione alla compattazione/archiviazione).
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:364]`.
*Valore*: di sistema/compliance — permette il debug a posteriori di anomalie rilevate fino a 3 mesi dopo l'evento.

### B5-NFR-06 — Retention permanente sui giorni di emissione segnale
Tutti i log che contengono almeno un evento `SIGNAL_EMITTED`, `SIGNAL_TRIGGERED` o uno dei sei eventi terminali sono **conservati permanentemente** (mai cancellati, nemmeno dopo i 90 giorni rolling).
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:365]`.
*Valore*: di sistema/compliance — abilita il replay deterministico di qualunque segnale emesso in qualunque finestra storica, per audit interno o ricostruzione post-hoc.

### B5-NFR-07 — Tolleranza dell'addebito DAPI Datafeed 20 EUR/mese senza interruzione
Sotto commissioni mensili `< 200 EUR` la pipeline **tollera** l'addebito automatico di **20 EUR/mese** del DAPI Datafeed senza interrompere il servizio, notifica il supervisore via Telegram con un singolo messaggio mensile, e **non** intraprende azioni automatiche di riduzione consumo dati.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:373]`, `[DOC-INTERNO CAP_09_parte_9.md:376]`, `[DOC-INTERNO CAP_09_parte_9.md:377]`.
*Valore*: operativo — il DAPI Datafeed di base è necessario al funzionamento; la pipeline non lo sospende mai da sé, la decisione economica resta al supervisore. (Il vincolo D-1 "no market data Eurex/CME extra" è distinto e resta invariato sui cross-index `[DOC-INTERNO CAP_09_parte_9.md:375]`.)

---

## 7. Matrice di tracciabilità e nota di rinvio

### 7.1 Matrice requisiti → fonte

| ID | Sez. | Tracciabilità (riga-fonte) | Valore |
|----|------|----------------------------|--------|
| B5-R-01 | 2 | CAP_09:27 | operativo |
| B5-R-02 | 2 | CAP_09:35 | operativo |
| B5-R-03 | 2 | CAP_09:37 | operativo |
| B5-CN-01 | 2 | CAP_09:39 | di sistema |
| B5-R-04 | 2 | CAP_09:29 (+ PROVA-EMPIRICA 2026-05-27) | operativo |
| B5-NFR-01 | 2 | CAP_09:41,43 | di sistema (compliance) |
| B5-CN-02 | 2 | CAP_09:45 | operativo |
| B5-CN-03 | 2 | CAP_09:47 | di sistema |
| B5-R-05 | 3 | CAP_09:75 (+ :61) | operativo |
| B5-R-06 | 3 | CAP_09:96 | operativo |
| B5-R-07 | 3 | CAP_09:61 (+ PROVA-EMPIRICA 2026-05-27 / M-4) | operativo |
| B5-R-08 | 3 | CAP_09:98,104 | operativo |
| B5-R-09 | 3 | CAP_09:103 | operativo/compliance |
| B5-CN-04 | 3 | CAP_09:107 | di sistema |
| B5-R-10 | 3 | CAP_09:75 (+ :69) | operativo |
| B5-R-11 | 4 | CAP_09:273 | operativo |
| B5-R-12 | 4 | CAP_09:273 | operativo |
| B5-R-13 | 4 | CAP_09:294,299 | operativo/compliance |
| B5-R-14 | 4 | CAP_09:302 | operativo |
| B5-CN-05 | 4 | CAP_09:292,302 | di sistema |
| B5-CN-06 | 4 | CAP_09:292 | di sistema/replay |
| B5-R-15 | 5 | CAP_09:310,308 | operativo |
| B5-R-16 | 5 | CAP_09:311,324 | operativo |
| B5-CN-07 | 5 | CAP_09:311 | di sistema |
| B5-CN-08 | 5 | CAP_09:315,316,317,318 | di sistema |
| B5-NFR-02 | 5 | CAP_09:311,320 | operativo |
| B5-R-17 | 5 | CAP_09:325 | operativo/compliance |
| B5-CN-09 | 5 | CAP_09:328 | di sistema/replay |
| B5-NFR-03 | 6 | CAP_09:360 | di sistema/compliance |
| B5-R-18 | 6 | CAP_09:353,356 | operativo/compliance |
| B5-R-19 | 6 | CAP_09:353,355 | operativo |
| B5-R-20 | 6 | CAP_09:355 | operativo |
| B5-NFR-04 | 6 | CAP_09:357,358 | di sistema/compliance |
| B5-NFR-05 | 6 | CAP_09:364 | di sistema/compliance |
| B5-NFR-06 | 6 | CAP_09:365 | di sistema/compliance |
| B5-NFR-07 | 6 | CAP_09:373,376,377 | operativo |

Conteggio: **35 requisiti** (`B5-R`: 20, `B5-CN`: 9, `B5-NFR`: 7).

### 7.2 Nota di rinvio — premesse citate (NON consolidate qui)

| Fatto citato come premessa | Dove vive (blocco) | Dove è citato in B5 |
|----------------------------|--------------------|---------------------|
| Emission-only / no order routing come scelta di prodotto (Cap.1, Cap.9) | **B1/B2** (R-1.2 emission-only; Cap.27-28 elaborazione runtime) | B5-CN-01 (qui solo: porta 10002 mai aperta) |
| Moltiplicatore **5 EUR/pt** del FIB pieno (calibrazione) | **B1** | B5-R-10 (qui solo: dualità, miniFIB 1€ esecuzione) |
| **Contratto del messaggio Telegram** (banda, target_1, stop, payload) | **B4** | B5-R-16 (qui solo: attacco dell'annotazione di gating) |
| **State machine & 6 stati terminali** del segnale (Cap.7) | **B3** | B5-CN-05, B5-R-19 (qui solo: 22:00-non-chiude-active; granularità per-stato del log) |
| **Epoca E5 / `fib_session_calendar.csv`** (origine normativa finestra) | **B8** (Cap.41) | B5-R-11 (qui solo: regola operativa 08:00–22:00) |
| **Schema-dato DAPI** (CANDLE/PRICE/BOOK_5, decoder, format canonico) | **B6** (Cap.48/49/51) | dato ricevuto sui canali (B5-R-02/03/15); decoder/format non consolidato |
| Pipeline inference, EGARCH-recalibration, anti-doppio, latenza, determinismo replay (Cap.27-28) | **B1/B2/B4/B6** (R-1.2, R-3.10, NFR-6.2, CN-9.4) | non consolidati: 0 requisiti B5 propri |

### 7.3 Fuori-scope (con destinazione)

| Materia | Destinazione |
|---------|--------------|
| Schema-dato/decoder/format canonico DAPI (Cap.48/49/51) | **B6** |
| Corredo bundle frozen / gate di go-live (Cap.35, Sez.8) | **B7** |
| Dashboard di monitoraggio lifecycle (Cap.30) — l'audit è suo *input* | **fuori perimetro spec (FASE-D)** |
| Errori/recovery/riavvio Darwin (Cap.50) | contesto runtime, non fonda requisiti di Sez.7 |
| Warm-up stati condizionali (Cap.51) | premessa per il pull storico (B5-R-03); dettaglio in B6 |
| Esecuzione/gestione attiva post-fill, commissioni di trade (5€/op) | **B3 / B1** — già coperti |

### 7.4 PENDING-empirico (marcati, NON asseriti come verificati)

| Riferimento | Stato | Cosa serve per chiudere |
|-------------|-------|--------------------------|
| Codici mese **Mar / Dic** Directa-IDEM (oltre F/I) — in B5-R-07 | PENDING-empirico (non listati, fuori scope Cap.55) | decodifica via ANAG a mercato aperto |
| Comportamento **rollover / CONTRACT_SWITCH a scadenza reale** — in B5-R-08/09 | PENDING-empirico (probe V-3) | osservazione di un rollover reale alla terza venerdì |
| **Convenzione calendario / giorni-di-trading** della finestra — in B5-R-11 | PENDING-empirico (probe V-2) | verifica empirica del calendario IDEM (festività, weekend) |

> Non sono pending: il **valore** della finestra 08:00–22:00 CET e i fatti già `[PROVA-EMPIRICA 2026-05-27]` (banner del gateway, porte 10001/10002/10003) — citati con lo stato empirico esatto, non sovra-marcati.

### 7.5 Nota RM-3 (fonti esterne)

Le porte, il banner e le convenzioni provenienti dal wiki Directa sono trattati come `[WIKI-HINT, da verificare]` **salvo** dove esiste già una `[PROVA-EMPIRICA <data>]` (banner del gateway e porte: 2026-05-27; codici mese F/I: 2026-05-27 / 2026-05-29). Nessuna conclusione strutturale di questo blocco poggia su solo livello-4.
