# SPEC FUNZIONALE — Blocco B3: State-machine & lifecycle del segnale

> **Blocco 3 di 8** di una business-spec ricostruita ex-novo a blocchi (B1→B8). Questo file è **autonomo** e verrà ricomposto con gli altri 7 in un task di assemblaggio dedicato dopo B8 (l'assemblaggio è fuori scope di B3). B1 (Ambito & operatore) e B2 (Payload del segnale) sono già chiusi PASS e qui **non** vengono ridefiniti: i fatti di ambito/payload che servono come premessa sono citati dal CAP-fonte, non dai documenti B1/B2.
>
> **Fonte unica e autoritativa**: `docs/methodology_v2/CAP_02_parte_II.md` ("Parte II — Contratto del segnale FIB"), capitolo **chiuso PASS `a1625df`** (`tasks/STATO_CORRENTE.md:10`), congelato (freeze G-09: sola lettura). Perimetro derivato: **Capitolo 7 (sezioni 7.1–7.6) e Capitolo 11 (sezioni 11.1–11.5)**, con preambolo Parte II (`:1-9`) e clausola Q-05 (`:7`) come contesto citabile.
>
> **Scopo di B3**: consolidare la **semantica dinamica del ciclo di vita del segnale** — gli stati che il segnale attraversa, gli eventi che ne provocano le transizioni, la temporizzazione (timer pre/post-trigger come meccanica di scadenza), il contratto di osservazione real-time del primo pivot, e la submacchina distinta che traccia la posizione oltre target_1. Esclusi (rinviati ad altri blocchi): lo schema-payload come dato, le condizioni/regola di emissione, la pubblicazione Telegram, il formato dei log e il determinismo del replay, l'algoritmo di pivot detection e la definizione delle condizioni strutturali di invalidazione (vedi §8, nota di rinvio).

---

## Schema degli identificatori dei requisiti

Schema **auto-assegnato per questo blocco** (numerazione locale di B3, non importata da alcuna spec preesistente né da altri blocchi):

- **`B3-R-NN`** — requisiti **funzionali / di lifecycle**: stati, transizioni, eventi, meccanica dei timer, contratto della submacchina di tracking.
- **`B3-CN-NN`** — requisiti **invarianti / strutturali** del lifecycle: terminalità assoluta, precedenza degli eventi come condizione di determinismo, indipendenza della submacchina, invariante evento-vs-stato.
- **`B3-NFR-NN`** — requisiti **non-funzionali / di contratto di osservazione**: il contratto di osservazione real-time del primo pivot (cadenza, disponibilità entro un tetto di barre), di natura interfaccia/qualità-di-servizio.

Ogni requisito porta: la **proposizione** (atomica, N1), la **tracciabilità** `[DOC-INTERNO CAP_02_parte_II.md:<riga>]`, e il **valore** (operativo per default; *di sistema/validazione* per i soli invarianti di puro determinismo/replay, dichiarato esplicitamente).

---

## Sezione 1 — Stati del segnale e semantica

### 1.1 Architettura della state machine

**B3-R-01** — La state machine del segnale è costituita da **un solo stato non-terminale** (`active`) e **sei stati terminali** (`target_1_hit`, `stopped`, `invalidated`, `missed_target`, `expired`, `revoked`). `[DOC-INTERNO CAP_02_parte_II.md:95]` `[DOC-INTERNO CAP_02_parte_II.md:7]`
*Valore operativo*: definisce in modo chiuso l'insieme degli esiti possibili di un segnale, così che l'operatore retail sappia che ogni segnale ricevuto può concludersi solo in uno di sei esiti noti e non in stati indefiniti.

**B3-R-02** — Lo stato `target_2_hit` **non** fa parte della state machine del segnale (rimosso per decisione Q-05, Clausola 1). `[DOC-INTERNO CAP_02_parte_II.md:7]` `[DOC-INTERNO CAP_02_parte_II.md:129]`
*Valore operativo*: l'operatore sa che il sistema non gestisce target_2 come esito del segnale; il raggiungimento di target_2 è gestione di posizione di sua competenza (vedi Sezione 7).

### 1.2 Lo stato non-terminale `active`

**B3-R-03** — Un segnale entra nello stato `active` quando è stato emesso e la sua tupla è pubblicata; in `active` il segnale è in attesa di un evento che lo porti in uno stato terminale. `[DOC-INTERNO CAP_02_parte_II.md:97]`
*Valore operativo*: l'operatore che riceve un segnale `active` sa che il segnale è "vivo" e in attesa di azione/evento, non già concluso.

**B3-R-04** — Mentre il segnale è `active`, il motore osserva il prezzo corrente e calcola gli eventi di mercato pertinenti (raw touch della entry zone, raggiungimento di target o stop prima del raw touch, scadenza del timer pre/post-trigger, invalidazione strutturale, decisione di sostituzione) applicando le transizioni previste. `[DOC-INTERNO CAP_02_parte_II.md:97]`
*Valore operativo*: garantisce all'operatore che, finché il segnale è attivo, il sistema continua a monitorare le condizioni che possono chiudere il segnale, senza che l'operatore debba calcolarle a mano.

### 1.3 Gli stati terminali e le loro condizioni d'ingresso

**B3-R-05** — `target_1_hit` è lo stato terminale di **successo** del contratto del segnale. `[DOC-INTERNO CAP_02_parte_II.md:101]`
*Valore operativo*: comunica all'operatore che il segnale ha centrato il proprio primo obiettivo strutturale, l'esito atteso del trade.

**B3-R-06** — La condizione d'ingresso in `target_1_hit` è: dopo il raw touch della entry zone, il prezzo raggiunge `target_1` prima di `stop_loss`, prima della scadenza del timer post-trigger e prima di un'eventuale invalidazione strutturale. `[DOC-INTERNO CAP_02_parte_II.md:101]` `[DOC-INTERNO CAP_02_parte_II.md:122]`
*Valore operativo*: definisce senza ambiguità quando il segnale è "vinto", così che l'operatore riconosca l'esito anche osservando il prezzo da sé.

**B3-R-07** — Il raggiungimento di `target_1_hit` **chiude definitivamente il contratto del segnale**. `[DOC-INTERNO CAP_02_parte_II.md:101]`
*Valore operativo*: dice all'operatore che, una volta raggiunto target_1, quel segnale non verrà più sostituito né riaperto e la gestione della posizione oltre target_1 è interamente sua.

**B3-R-08** — `stopped` è lo stato terminale in cui il segnale entra quando, dopo il raw touch della entry zone, il prezzo raggiunge `stop_loss` prima di `target_1`, prima della scadenza del timer post-trigger e prima di un'eventuale invalidazione strutturale. `[DOC-INTERNO CAP_02_parte_II.md:103]` `[DOC-INTERNO CAP_02_parte_II.md:123]`
*Valore operativo*: comunica all'operatore l'esito di perdita "ordinaria" (stop colpito dopo essere entrato), distinto dagli esiti in cui l'ingresso non è mai avvenuto.

**B3-R-09** — `invalidated` è lo stato terminale in cui il segnale entra quando, **prima** del raw touch della entry zone, si verifica una condizione di invalidazione strutturale che rompe l'ipotesi del setup. `[DOC-INTERNO CAP_02_parte_II.md:105]` `[DOC-INTERNO CAP_02_parte_II.md:124]`
*Valore operativo*: avverte l'operatore che il setup è decaduto **prima** di poter entrare, quindi non deve eseguire alcun ordine su quel segnale.

**B3-R-10** — Fra le condizioni di invalidazione esplicitamente incluse nel contratto del segnale rientra il superamento del livello `stop_loss` da parte del prezzo, nella direzione contraria all'ipotesi del segnale, prima del raw touch (per i long, $p(t) \leq \texttt{stop\_loss}$ con $t < t_{touch}$; simmetricamente per gli short). `[DOC-INTERNO CAP_02_parte_II.md:105]` `[DOC-INTERNO CAP_02_parte_II.md:124]`
*Valore operativo*: chiarisce all'operatore che un prezzo che sfonda lo stop prima ancora di toccare la zona segnala un'ipotesi già smentita, e il segnale non va eseguito.

**B3-CN-01** — Lo stato `invalidated` (invalidazione strutturale prima del raw touch, incluso lo stop attraversato pre-touch) è **distinto** da `stopped` (che richiede un raw touch precedente). `[DOC-INTERNO CAP_02_parte_II.md:105]`
*Valore operativo*: distingue per l'operatore due esiti di segno opposto in termini di azione richiesta — `stopped` significa "sei entrato e hai preso lo stop", `invalidated` significa "non saresti dovuto entrare".

**B3-R-11** — `missed_target` è lo stato terminale in cui il segnale entra quando, **prima** del raw touch della entry zone, il prezzo raggiunge `target_1`. `[DOC-INTERNO CAP_02_parte_II.md:107]` `[DOC-INTERNO CAP_02_parte_II.md:125]`
*Valore operativo*: comunica all'operatore che il target strutturale è stato realizzato dal mercato ma il setup non si è eseguito perché la zona di ingresso non è mai stata toccata (occasione "persa", non perdita).

**B3-R-12** — La metrica/riferimento di `missed_target` è ancorata a `target_1` e **non** a `target_2`. `[DOC-INTERNO CAP_02_parte_II.md:107]`
*Valore operativo*: stabilisce che il sistema misura le occasioni perse rispetto al primo obiettivo strutturale, coerentemente con la chiusura di prodotto, senza che l'operatore debba interpretare metriche su target_2.

**B3-R-13** — `expired` è lo stato terminale in cui il segnale entra alla scadenza di un timer di validità. `[DOC-INTERNO CAP_02_parte_II.md:109]`
*Valore operativo*: garantisce all'operatore che nessun segnale resta indefinitamente "aperto": alla scadenza viene chiuso e non richiede più attenzione.

**B3-R-14** — Lo stato `expired` registra la causa della scadenza tramite un **campo causale strutturato** con due valori (`posttrigger_timeout`, `pretrigger_timeout`), **non** tramite due stati distinti. `[DOC-INTERNO CAP_02_parte_II.md:109]`
*Valore di sistema/validazione*: mantiene il vincolo di 6 soli stati terminali (Q-05, Clausola 1) preservando nel log la distinzione fra scadenza pre- e post-ingresso, necessaria all'analisi della calibrazione dei timer; per l'operatore l'esito vissuto è unico ("scaduto").

**B3-R-15** — `revoked` è lo stato terminale in cui il segnale entra quando è stato **superseduto** dall'emissione di un nuovo `signal_id`. `[DOC-INTERNO CAP_02_parte_II.md:111]`
*Valore operativo*: avverte l'operatore che il segnale precedente non è più valido perché il motore ne ha emesso uno nuovo aggiornato, e va abbandonato a favore del nuovo.

> *Premessa di seam (B2, citata, non ri-consolidata)*: il **meccanismo** della supersessione — "segnale superseduto da nuovo `signal_id`", proprietà di segnale unico attivo / sostituzione-non-edit — è consolidato come proprietà del payload in Cap.6.3 `[DOC-INTERNO CAP_02_parte_II.md:77]` ed è materia di B2. In B3 lo si richiama come premessa per giustificare la transizione `active→revoked` (B3-R-23), senza ri-derivarlo.

**B3-R-16** — La revoca avviene **contestualmente** all'emissione del nuovo segnale e interrompe il lifecycle del precedente. `[DOC-INTERNO CAP_02_parte_II.md:111]`
*Valore operativo*: garantisce all'operatore che non esiste un istante in cui due segnali sono validi insieme: nel momento in cui arriva il nuovo, il vecchio è già revocato.

### 1.4 Terminalità assoluta e NB-9

**B3-CN-02** — Nessuno stato terminale ammette transizioni uscenti: il ciclo di vita del segnale è definitivamente chiuso all'ingresso in qualsiasi stato terminale. `[DOC-INTERNO CAP_02_parte_II.md:99]`
*Valore operativo*: assicura all'operatore che un esito comunicato è definitivo — un segnale "vinto", "stoppato" o "scaduto" non potrà più cambiare stato e tornare a richiedere azione.

**B3-CN-03** — La transizione `target_1_hit → revoked` **non esiste**: un segnale già concluso in successo non è sostituibile, perché il vincolo $|\mathcal{A}(t)| \leq 1$ si applica ai soli segnali attivi e un segnale terminato non è attivo. `[DOC-INTERNO CAP_02_parte_II.md:113]`
*Valore operativo*: rimuove ogni ambiguità per l'operatore — dopo aver raggiunto target_1, nessuna "revoca" successiva può annullare quel successo; un eventuale nuovo segnale è un contratto indipendente.

---

## Sezione 2 — Transizioni ammesse e precedenza degli eventi

### 2.1 Insieme delle transizioni

**B3-R-17** — La creazione del segnale (emissione, generazione del `signal_id`, scrittura del log di emissione) porta il segnale nello stato `active`. `[DOC-INTERNO CAP_02_parte_II.md:121]`
*Valore operativo*: definisce il punto d'ingresso del lifecycle, l'istante a partire dal quale l'operatore ha in mano un segnale su cui può agire.

**B3-R-18** — È ammessa la transizione `active → target_1_hit` con la condizione di B3-R-06 (raw touch, poi target_1 prima di stop/expiry/invalidazione). `[DOC-INTERNO CAP_02_parte_II.md:122]`
*Valore operativo*: è la transizione che comunica all'operatore l'esito di successo del segnale eseguito.

**B3-R-19** — È ammessa la transizione `active → stopped` con la condizione di B3-R-08 (raw touch, poi stop_loss prima di target_1/expiry/invalidazione). `[DOC-INTERNO CAP_02_parte_II.md:123]`
*Valore operativo*: comunica all'operatore l'esito di stop dopo ingresso.

**B3-R-20** — È ammessa la transizione `active → invalidated` con la condizione di B3-R-09/B3-R-10 (invalidazione strutturale prima del raw touch). `[DOC-INTERNO CAP_02_parte_II.md:124]`
*Valore operativo*: comunica all'operatore che il segnale è decaduto prima dell'ingresso.

**B3-R-21** — È ammessa la transizione `active → missed_target` con la condizione di B3-R-11 (target_1 raggiunto prima del raw touch). `[DOC-INTERNO CAP_02_parte_II.md:125]`
*Valore operativo*: comunica all'operatore l'occasione persa (target colpito senza ingresso).

**B3-R-22** — È ammessa la transizione `active → expired`, con le due cause registrate nel campo causale: (a) `posttrigger_timeout` quando $t \geq t_{exec} + \Delta t_{cromosoma}$ minuti di trading e il segnale è ancora `active`; (b) `pretrigger_timeout` quando $t \geq t_{emission} + T_{touch}^{max}$ minuti di trading e il segnale è ancora `active` senza raw touch. `[DOC-INTERNO CAP_02_parte_II.md:126]`
*Valore operativo*: comunica all'operatore la chiusura per scadenza, distinguendo nel registro se è scaduto in attesa di ingresso o dopo l'ingresso.

**B3-R-23** — È ammessa la transizione `active → revoked` quando il motore emette un nuovo `signal_id` (sostituzione). `[DOC-INTERNO CAP_02_parte_II.md:127]` *(meccanismo della supersessione come premessa: `[DOC-INTERNO CAP_02_parte_II.md:77]`)*
*Valore operativo*: comunica all'operatore che il segnale è stato sostituito da uno nuovo, da seguire al posto del precedente.

### 2.2 Chiusura dell'insieme e precedenza

**B3-CN-04** — Nessuna transizione esce dagli stati terminali; in particolare `target_1_hit` non transita verso `target_2_hit` (rimosso), `revoked`, `stopped`, `expired` o qualsiasi altro stato. `[DOC-INTERNO CAP_02_parte_II.md:129]`
*Valore operativo*: ribadisce in forma di transizioni la definitività di ogni esito, così che l'operatore non si attenda mai un cambio di stato dopo la chiusura.

**B3-CN-05** — A parità di timestamp, la precedenza degli eventi è: `expiry > invalidazione > missed_target > raw touch > azione post-trigger`. `[DOC-INTERNO CAP_02_parte_II.md:131]`
*Valore di sistema/validazione*: garantisce un replay deterministico e riproducibile a parità di dati (premessa per l'audit monetario e per la validazione DSR/PBO della fitness); non ha un valore vissuto direttamente dall'operatore al cellulare, perché ordina eventi simultanei nella ricostruzione del lifecycle.

---

## Sezione 3 — Raw touch come evento ed esecuzione

### 3.1 Definizione ed eseguibilità

**B3-R-24** — Il raw touch della entry zone è l'**evento** in cui il prezzo del FIB, osservato sulla barra 1-min chiusa, assume per la prima volta un valore appartenente all'insieme discreto della `entry_zone`. `[DOC-INTERNO CAP_02_parte_II.md:135]`
*Valore operativo*: definisce con precisione l'istante in cui l'operatore deve considerare il segnale "entrato" e può eseguire manualmente l'ordine.

**B3-R-25** — La definizione di raw touch **non impone alcun vincolo sulla direzione di provenienza** del prezzo: la prima barra 1-min il cui intervallo high-low contiene almeno uno dei livelli discreti della zona produce il raw touch. `[DOC-INTERNO CAP_02_parte_II.md:135]`
*Valore operativo*: rassicura l'operatore che il contatto con la zona conta a prescindere da come il prezzo l'ha raggiunta, evitando interpretazioni soggettive.

**B3-R-26** — Al raw touch il motore produce un evento, denotato `trigger_event`, riferito al `signal_id` del segnale corrente. `[DOC-INTERNO CAP_02_parte_II.md:137]`
*Valore operativo*: è l'evento che segnala all'operatore l'attivazione concreta del segnale precedentemente emesso.

> *Confine (B4)*: la **pubblicazione** del `trigger_event` sul canale Telegram (contratto informativo della notifica, latenza, anti-duplicato) è materia di B4 (Cap.9) e **non** è consolidata qui. In B3 il `trigger_event` è trattato solo come evento del lifecycle.

**B3-R-27** — **Il raw touch è sempre eseguibile**: non esistono nel contratto del segnale guardie o filtri post-emissione che blocchino il trigger una volta che il prezzo è entrato nella zona. `[DOC-INTERNO CAP_02_parte_II.md:137]`
*Valore operativo*: garantisce all'operatore che, una volta toccata la zona, non ci sono blocchi nascosti che invalidino l'ingresso: la decisione di emettere è già stata presa prima e il trigger è netto.

### 3.2 `trigger_event` come evento, non stato

**B3-CN-06** — Il `trigger_event` **non è uno stato** della state machine: al raw touch il segnale **resta in `active`** finché un evento successivo (target_1, stop_loss, invalidazione, scadenza, revoca) non lo porta in uno stato terminale. `[DOC-INTERNO CAP_02_parte_II.md:139]`
*Valore operativo*: chiarisce all'operatore che "essere entrato" (raw touch) non è un esito ma una fase intermedia; il segnale è ancora vivo e può ancora andare a target o a stop.

**B3-R-28** — Il motore **non osserva il fill manuale** dell'operatore sul broker, perché il motore non esegue ordini e l'operatore agisce manualmente dal cellulare. `[DOC-INTERNO CAP_02_parte_II.md:139]`
*Valore operativo*: chiarisce all'operatore che il sistema non sa se e quando ha effettivamente eseguito; il lifecycle del segnale è calcolato sul prezzo di mercato, non sul suo riempimento reale.

> *Confine (Parte III)*: il trattamento del `trigger_event` come **fill virtuale** in backtest e la relativa regola di simulazione sono materia di Parte III `[DOC-INTERNO CAP_02_parte_II.md:141]` e **non** alterano la state machine pubblica del segnale; non sono consolidati qui.

### 3.3 Edge case del raw touch (NB-8)

**B3-R-29** — *(edge case a — prezzo già in zona all'emissione)* Il motore valuta il raw touch a partire dalla barra $t_{emission} + 1$ (prima barra chiusa dopo l'emissione); la barra di emissione stessa non è valutata. Se il prezzo è già in zona alla chiusura di $t_{emission}$ e vi rimane, il raw touch è registrato alla prima barra $t_{emission}+1$ il cui high-low contiene un livello della zona (con $t_{exec} = t_{emission}+1$); se il prezzo era in zona a $t_{emission}$ ma ne è uscito a $t_{emission}+1$, non vi è raw touch immediato e il segnale resta `active`. `[DOC-INTERNO CAP_02_parte_II.md:145]`
*Valore operativo*: garantisce all'operatore che il trigger non scatta su una barra che non poteva ancora vedere sul cellulare, evitando ingressi non azionabili.

**B3-R-30** — *(edge case b — gap overnight dentro/oltre la zona)* Un gap di apertura overnight con prezzo dentro o oltre la zona **non azzera** il raw touch: se la barra di apertura del giorno successivo (prima barra delle 8:00 CET) ha un intervallo high-low che contiene almeno un livello di `entry_zone`, il raw touch è registrato su quella barra ($t_{exec}$ = prima barra del giorno successivo). `[DOC-INTERNO CAP_02_parte_II.md:147]`
*Valore operativo*: assicura all'operatore che un segnale lasciato aperto da un giorno all'altro si attiva regolarmente se il mercato riapre dentro la zona, senza "saltare" il trigger per il solo fatto del gap.

**B3-R-31** — *(edge case c — gap che salta la zona nella direzione opposta)* Se l'open della barra è sul lato della zona verso cui il segnale non punta: (i) se il prezzo si è allontanato verso il lato che coincide con la direzione di `stop_loss`, il motore valuta se la condizione di `invalidated` (stop attraversato) sia soddisfatta, altrimenti il segnale resta `active` in attesa di rientro nella zona; (ii) un gap che porta il prezzo oltre `target_1` senza raw touch determina la transizione in `missed_target`. `[DOC-INTERNO CAP_02_parte_II.md:149]`
*Valore operativo*: dice all'operatore come si comporta il segnale quando il mercato "salta" la zona — verso lo stop diventa potenzialmente invalidato, verso il target diventa occasione persa — senza richiedere un suo intervento interpretativo.

---

## Sezione 4 — Semantica dei timer (pre/post-trigger)

> *Confine (B2)*: i **domini** discreti $\Delta t_{cromosoma}$ e $T_{touch}^{max}$ **come campi del payload** sono consolidati in B2 (Cap.6) e qui sono citati come premessa, non ri-derivati. B3 consolida solo la **meccanica di decorrenza e scadenza** dei due timer. Il calendario di trading (finestra 8:00–22:00 CET, cap di 2 giorni) è ammesso come **calendario/semantica su cui i counter avanzano**, già fissato nei CAP chiusi e citato come dato; restano fuori i **valori-soglia congelati** (vedi §8).

### 4.1 Timer post-trigger ($\Delta t_{cromosoma}$)

**B3-R-32** — Il timer post-trigger decorre **dal raw touch**: al raw touch a istante $t_{exec}$, il motore calcola `expiry = t_exec + Δt_cromosoma` minuti di **trading**. `[DOC-INTERNO CAP_02_parte_II.md:155]`
*Valore operativo*: dice all'operatore da quando parte il conto alla rovescia di validità del segnale eseguito — dall'ingresso, non dall'emissione.

**B3-R-33** — La somma del timer post-trigger è valutata sul **calendario di trading** dello strumento, non sul calendario solare. `[DOC-INTERNO CAP_02_parte_II.md:157]`
*Valore operativo*: assicura all'operatore che la "scadenza" del segnale è misurata in tempo di mercato effettivo, non in ore di orologio comprese le notti chiuse.

**B3-R-34** — Il counter del timer post-trigger avanza **esclusivamente** nei minuti compresi nella finestra **8:00–22:00 CET** dei giorni di trading e **si arresta** nelle interruzioni notturne (22:00–8:00), nei weekend e nei festivi di mercato. `[DOC-INTERNO CAP_02_parte_II.md:157]`
*Valore operativo*: l'operatore sa che un segnale non "consuma" validità mentre il mercato è chiuso, quindi un segnale aperto venerdì sera è ancora valido lunedì in apertura per i minuti residui.

**B3-R-35** — Il timer post-trigger è valutato dal motore a ogni barra 1-min: appena $t \geq \texttt{expiry}$ e il segnale è ancora `active`, il segnale transita in `expired` con causa `posttrigger_timeout`. `[DOC-INTERNO CAP_02_parte_II.md:159]`
*Valore operativo*: garantisce all'operatore che un segnale entrato ma non andato né a target né a stop entro il tempo previsto viene chiuso automaticamente per scadenza, senza restare appeso.

### 4.2 Timer pre-trigger ($T_{touch}^{max}$, NB-7)

**B3-R-36** — Il timer pre-trigger decorre **dalla `timestamp_emission`**: il segnale emesso resta `active` in attesa del raw touch e il counter parte dall'emissione. `[DOC-INTERNO CAP_02_parte_II.md:163]` `[DOC-INTERNO CAP_02_parte_II.md:165]`
*Valore operativo*: dice all'operatore da quando parte il tempo massimo di attesa di un ingresso che non è ancora avvenuto.

**B3-R-37** — Il counter del timer pre-trigger avanza **esclusivamente** nei minuti di trading 8:00–22:00 CET, scavalcando le interruzioni notturne e i weekend, esattamente come il counter post-trigger. `[DOC-INTERNO CAP_02_parte_II.md:163]`
*Valore operativo*: assicura all'operatore che l'attesa di un ingresso si misura in tempo di mercato effettivo, coerentemente con il timer post-trigger.

**B3-R-38** — Allo scadere del timer pre-trigger senza che sia avvenuto alcun raw touch, il segnale transita in `expired` con causa `pretrigger_timeout`. `[DOC-INTERNO CAP_02_parte_II.md:165]`
*Valore operativo*: evita che l'operatore resti in attesa indefinita di un raw touch che non arriva: il segnale non eseguito viene chiuso dopo il tempo massimo di attesa.

**B3-R-39** — Il razionale del timer pre-trigger è eliminare la patologia "segnale `active` per un tempo indefinitamente lungo in attesa del raw touch", che produrrebbe strategie degeneri (emissione rara e attesa illimitata) gonfiando artificialmente l'`executable_rate`. `[DOC-INTERNO CAP_02_parte_II.md:167]`
*Valore di sistema/validazione*: protegge la metrica `executable_rate` da degenerazioni del GA; per l'operatore il beneficio indiretto è ricevere segnali eseguibili in tempi ragionevoli anziché segnali che restano aperti senza mai attivarsi.

---

## Sezione 5 — Contratto di osservazione del primo pivot real-time (M-1)

> *Confine (Parte III)*: l'**algoritmo** di pivot detection e la regola di confermabilità del pivot sono materia di Parte III (Cap.15) e **non** sono consolidati qui. B3 prende di Cap.7.6 solo il **contratto di osservazione e la cadenza**.

**B3-NFR-01** — Il motore osserva la sequenza delle barre 1-min a partire dall'apertura della sessione alle **8:00 CET**; a ciascuna barra chiusa valuta se la barra costituisce un candidato pivot strutturale (minimo o massimo) sulla sequenza disponibile. `[DOC-INTERNO CAP_02_parte_II.md:171]` `[DOC-INTERNO CAP_02_parte_II.md:173]`
*Valore operativo*: garantisce all'operatore che il punto di riferimento strutturale del segnale (l'ancora del prezzo di riferimento e del target di sessione) è calcolato osservando il mercato fin dall'apertura, non a posteriori.

**B3-NFR-02** — Vale come vincolo di contratto che il **primo pivot strutturale post-apertura** deve essere **disponibile**, in fase di calibrazione del motore, entro un numero massimo $N_{pivot}$ di barre 1-min dall'apertura della sessione (valore numerico di $N_{pivot}$ **non** fissato in Parte II → Parte V). `[DOC-INTERNO CAP_02_parte_II.md:173]`
*Valore operativo*: assicura all'operatore che l'ancora strutturale è disponibile in tempo utile nella finestra iniziale di sessione, senza la quale i segnali della prima parte della giornata sarebbero privi di riferimento.

**B3-NFR-03** — La cadenza di valutazione della regola di pivot è la barra 1-min **chiusa**; il motore **non** opera su tick intra-bar per la pivot detection. `[DOC-INTERNO CAP_02_parte_II.md:175]`
*Valore operativo*: garantisce all'operatore coerenza fra ciò che il motore osserva (barre chiuse) e i livelli che pubblica, senza scatti dovuti a oscillazioni intra-minuto.

---

## Sezione 6 — Position lifecycle: submacchina distinta

### 6.1 Separazione formale segnale vs posizione

**B3-CN-07** — Il lifecycle del segnale (il contratto del motore, ottimizzato dal GA) si **chiude definitivamente** in `target_1_hit` o in qualsiasi altro stato terminale; il position lifecycle è una **submacchina distinta** di tracking degli eventi post-target_1. `[DOC-INTERNO CAP_02_parte_II.md:349]` `[DOC-INTERNO CAP_02_parte_II.md:351]` `[DOC-INTERNO CAP_02_parte_II.md:352]` `[DOC-INTERNO CAP_02_parte_II.md:7]`
*Valore operativo*: chiarisce all'operatore il confine netto fra "cosa fa il sistema" (porta a target_1) e "cosa fa lui" (gestisce la posizione oltre), senza sovrapposizioni di responsabilità.

**B3-R-40** — Nel contesto del motore (che emette segnali senza eseguire ordini), il "boundary" del lifecycle del segnale coincide con `target_1_hit`: oltre tale soglia la gestione della posizione è responsabilità dell'operatore umano, con il solo supporto informativo della submacchina di tracking. `[DOC-INTERNO CAP_02_parte_II.md:362]`
*Valore operativo*: dice all'operatore che dopo target_1 ha il pieno controllo della posizione e riceve dal sistema solo informazione, non istruzioni operative.

### 6.2 Perimetro OUT/IN-scope

**B3-R-41** — Sono **OUT-OF-SCOPE dal motore**: execution policy, scaling-out automatico, trailing stop, dynamic sizing, take profit anticipato e qualsiasi decisione operativa post-target_1; la gestione della posizione oltre target_1 è interamente dell'operatore manuale (punto 8 della dichiarazione di intenti). `[DOC-INTERNO CAP_02_parte_II.md:368]`
*Valore operativo*: rassicura l'operatore che il sistema non interferisce con la sua gestione della posizione oltre target_1 (niente take/stop profit calcolati dal segnale), come da sua esplicita richiesta.

**B3-R-42** — Sono **IN-SCOPE per reporting e validazione** le metriche prodotte dalla submacchina: hit-rate condizionale di target_2 dato target_1 ($\pi_{t_2 \mid t_1}$), distribuzioni di MFE e MAE post-target_1, frequenza di stop post-target_1 ($f_{stop \mid t_1}$), distribuzione dei tempi di permanenza post-target_1. `[DOC-INTERNO CAP_02_parte_II.md:370]` `[DOC-INTERNO CAP_02_parte_II.md:372]` `[DOC-INTERNO CAP_02_parte_II.md:373]` `[DOC-INTERNO CAP_02_parte_II.md:374]` `[DOC-INTERNO CAP_02_parte_II.md:375]`
*Valore operativo*: queste metriche misurano quanto sono "buoni" i livelli target_2 e stop_loss pubblicati, informando l'operatore (via reporting) sulla qualità strutturale dei livelli che riceve, anche se non guidano una sua azione automatica.

### 6.3 Struttura della submacchina

**B3-R-43** — L'**evento di ingresso** della submacchina è il raggiungimento di `target_1_hit` da parte del segnale associato; a quel momento la submacchina registra il prezzo di `target_1`, di `stop_loss`, di `target_2` (dal payload immutabile) e l'istante di ingresso. `[DOC-INTERNO CAP_02_parte_II.md:381]`
*Valore operativo*: definisce con precisione quando inizia il tracking della posizione, allineato all'istante in cui l'operatore prende in carico la gestione manuale.

**B3-R-44** — Lo **stato iniziale** della submacchina è `tracking_active`, che indica che la submacchina sta osservando la dinamica del prezzo successiva a `target_1_hit`. `[DOC-INTERNO CAP_02_parte_II.md:383]`
*Valore operativo*: distingue lo stato di tracking attivo della posizione dallo stato (terminato) del segnale, così che il reporting sia leggibile.

**B3-R-45** — La submacchina registra gli **eventi** `target_2_reached`, `stop_after_target_1`, `retracement_to_entry`, `position_close_event` come **eventi della submacchina, non stati del segnale**. `[DOC-INTERNO CAP_02_parte_II.md:385]` `[DOC-INTERNO CAP_02_parte_II.md:386]` `[DOC-INTERNO CAP_02_parte_II.md:387]` `[DOC-INTERNO CAP_02_parte_II.md:388]` `[DOC-INTERNO CAP_02_parte_II.md:389]`
*Valore operativo*: fornisce all'operatore (via reporting) una traccia di cosa è successo dopo target_1 — se la posizione ha raggiunto target_2, è tornata allo stop o alla zona — senza che questi eventi modifichino l'esito già registrato del segnale.

**B3-CN-08** — `target_2_reached` è un **evento** della submacchina e **non** uno stato/transizione del segnale (coerente con la rimozione di `target_2_hit`, B3-R-02). `[DOC-INTERNO CAP_02_parte_II.md:386]` `[DOC-INTERNO CAP_02_parte_II.md:374]`
*Valore operativo*: ribadisce all'operatore che il raggiungimento di target_2 è informazione sulla gestione della posizione (sua), non un esito del contratto del segnale.

**B3-R-46** — Lo **stato terminale** della submacchina è `tracking_closed`; la submacchina termina al verificarsi del primo evento terminante dichiarato in Parte V (in backtest: `target_2_reached`, `stop_after_target_1` o fine sessione, quello che avviene prima). `[DOC-INTERNO CAP_02_parte_II.md:391]`
*Valore operativo*: definisce quando il tracking della posizione si conclude nel reporting, chiudendo il ciclo informativo post-target_1.

**B3-CN-09** — La submacchina **non modifica mai lo stato del segnale**: il segnale è terminato in `target_1_hit` prima che la submacchina inizi a tracciare; i log della submacchina sono separati e referenziati dal `signal_id`. `[DOC-INTERNO CAP_02_parte_II.md:393]`
*Valore operativo*: garantisce all'operatore che l'esito registrato del segnale (`target_1_hit`) resta inalterato qualunque cosa accada alla posizione dopo, preservando l'integrità del track record.

### 6.4 Impatto sul GA

**B3-CN-10** — Lo **space search del cromosoma del GA non viene esteso** da policy decisionali post-target_1: il GA non ottimizza trailing stop, take profit anticipato, scaling-out né alcuna regola di gestione della posizione oltre `target_1_hit`. `[DOC-INTERNO CAP_02_parte_II.md:397]`
*Valore operativo*: garantisce all'operatore che il sistema resta nel perimetro concordato (emette segnali, non gestisce posizioni), e che la complessità del modello non cresce con regole che non gli servono.

**B3-R-47** — Le metriche della submacchina ($\pi_{t_2 \mid t_1}$, MFE/MAE post-target_1, $f_{stop \mid t_1}$) entrano nella fitness multi-obiettivo del GA come **obiettivi di qualità informativa del payload**, **non** come variabili decisionali del cromosoma. `[DOC-INTERNO CAP_02_parte_II.md:399]`
*Valore operativo*: assicura all'operatore che il GA è spinto a pubblicare livelli target_2 e stop_loss strutturalmente robusti (realizzati dal mercato con alta probabilità), migliorando la qualità informativa dei segnali che riceve.

---

## Sezione 7 — Invarianti di modellazione del lifecycle (riepilogo)

Questa sezione raccoglie, per evidenza, le proprietà **invarianti/strutturali** del lifecycle già introdotte in linea sopra (non re-tracciate qui se già tracciate al loro requisito):

- **Terminalità assoluta** degli stati terminali → B3-CN-02; chiusura definitiva di `target_1_hit` → B3-R-07; assenza di transizioni uscenti in forma di transizioni → B3-CN-04; non-esistenza di `target_1_hit → revoked` (NB-9) → B3-CN-03.
- **Invariante evento-vs-stato**: il `trigger_event`/raw touch è evento, non stato → B3-CN-06; gli eventi della submacchina (`target_2_reached`, ecc.) sono eventi, non stati del segnale → B3-R-45, B3-CN-08.
- **Precedenza degli eventi** come condizione del determinismo del replay → B3-CN-05.
- **Indipendenza della submacchina** (non modifica mai lo stato del segnale) → B3-CN-09.

**B3-CN-11** — Il vincolo $|\mathcal{A}(t)| \leq 1$ si riferisce ai **soli segnali attivi**: un segnale terminato non è attivo, quindi non è soggetto a sostituzione. `[DOC-INTERNO CAP_02_parte_II.md:113]`
*Valore di sistema/validazione*: disambigua la sostituzione `active→revoked` rispetto agli stati terminali (premessa per la coerenza del lifecycle e del replay). *Nota di confine*: il vincolo $|\mathcal{A}(t)| \leq 1$ **come tale** (proprietà del payload-oggetto) è consolidato in B2 (Cap.6.3); qui è richiamato solo per la sua conseguenza sul lifecycle (inapplicabilità della revoca a un segnale terminato), non ri-derivato.

---

## Sezione 8 — Matrice di tracciabilità + nota di rinvio

### 8.1 Matrice di tracciabilità

| ID | Proposizione (sintesi) | Citazione `CAP_02_parte_II.md:` | Valore |
|----|------------------------|----------------------------------|--------|
| B3-R-01 | 1 stato non-terminale + 6 terminali | :95, :7 | operativo |
| B3-R-02 | `target_2_hit` rimosso | :7, :129 | operativo |
| B3-R-03 | `active`: emesso, in attesa di evento | :97 | operativo |
| B3-R-04 | in `active` il motore osserva e applica transizioni | :97 | operativo |
| B3-R-05 | `target_1_hit` = successo | :101 | operativo |
| B3-R-06 | condizione d'ingresso `target_1_hit` | :101, :122 | operativo |
| B3-R-07 | `target_1_hit` chiude il contratto | :101 | operativo |
| B3-R-08 | `stopped`: stop dopo raw touch | :103, :123 | operativo |
| B3-R-09 | `invalidated`: invalidazione pre-raw touch | :105, :124 | operativo |
| B3-R-10 | stop attraversato pre-touch incluso in `invalidated` | :105, :124 | operativo |
| B3-R-11 | `missed_target`: target_1 pre-raw touch | :107, :125 | operativo |
| B3-R-12 | `missed_target` ancorato a target_1 | :107 | operativo |
| B3-R-13 | `expired`: scadenza timer | :109 | operativo |
| B3-R-14 | causa `expired` = campo, non stati | :109 | sistema/validazione |
| B3-R-15 | `revoked`: superseduto da nuovo signal_id | :111 | operativo |
| B3-R-16 | revoca contestuale all'emissione del nuovo | :111 | operativo |
| B3-R-17 | creazione → `active` | :121 | operativo |
| B3-R-18 | `active → target_1_hit` | :122 | operativo |
| B3-R-19 | `active → stopped` | :123 | operativo |
| B3-R-20 | `active → invalidated` | :124 | operativo |
| B3-R-21 | `active → missed_target` | :125 | operativo |
| B3-R-22 | `active → expired` (2 cause) | :126 | operativo |
| B3-R-23 | `active → revoked` (premessa :77) | :127, :77 | operativo |
| B3-R-24 | raw touch = evento su barra 1-min chiusa | :135 | operativo |
| B3-R-25 | raw touch senza vincolo di direzione | :135 | operativo |
| B3-R-26 | `trigger_event` prodotto al raw touch | :137 | operativo |
| B3-R-27 | raw touch sempre eseguibile | :137 | operativo |
| B3-R-28 | motore non osserva il fill manuale | :139 | operativo |
| B3-R-29 | edge case (a) prezzo già in zona | :145 | operativo |
| B3-R-30 | edge case (b) gap overnight non azzera | :147 | operativo |
| B3-R-31 | edge case (c) gap che salta la zona | :149 | operativo |
| B3-R-32 | timer post-trigger decorre da $t_{exec}$ | :155 | operativo |
| B3-R-33 | timer post-trigger su calendario di trading | :157 | operativo |
| B3-R-34 | counter post-trigger 8:00–22:00, arresto notte/weekend/festivi | :157 | operativo |
| B3-R-35 | scadenza post-trigger → `expired`/`posttrigger_timeout` | :159 | operativo |
| B3-R-36 | timer pre-trigger decorre da `timestamp_emission` | :163, :165 | operativo |
| B3-R-37 | counter pre-trigger 8:00–22:00 | :163 | operativo |
| B3-R-38 | scadenza pre-trigger → `expired`/`pretrigger_timeout` | :165 | operativo |
| B3-R-39 | razionale anti-degenerazione `executable_rate` | :167 | sistema/validazione |
| B3-R-40 | boundary lifecycle = `target_1_hit` | :362 | operativo |
| B3-R-41 | OUT-OF-SCOPE post-target_1 | :368 | operativo |
| B3-R-42 | IN-SCOPE metriche di reporting | :370, :372, :373, :374, :375 | operativo |
| B3-R-43 | evento di ingresso submacchina = `target_1_hit` | :381 | operativo |
| B3-R-44 | stato iniziale `tracking_active` | :383 | operativo |
| B3-R-45 | eventi submacchina, non stati del segnale | :385, :386, :387, :388, :389 | operativo |
| B3-R-46 | terminale `tracking_closed` | :391 | operativo |
| B3-R-47 | metriche in fitness come qualità informativa | :399 | operativo |
| B3-CN-01 | `invalidated` distinto da `stopped` | :105 | operativo |
| B3-CN-02 | terminalità assoluta (no transizioni uscenti) | :99 | operativo |
| B3-CN-03 | `target_1_hit → revoked` non esiste (NB-9) | :113 | operativo |
| B3-CN-04 | nessuna transizione esce dai terminali | :129 | operativo |
| B3-CN-05 | precedenza eventi a parità di timestamp | :131 | sistema/validazione |
| B3-CN-06 | `trigger_event` non è stato; resta `active` | :139 | operativo |
| B3-CN-07 | separazione segnale vs submacchina | :349, :351, :352, :7 | operativo |
| B3-CN-08 | `target_2_reached` evento, non stato | :386, :374 | operativo |
| B3-CN-09 | submacchina non modifica lo stato del segnale | :393 | operativo |
| B3-CN-10 | space search GA non esteso | :397 | operativo |
| B3-CN-11 | $|\mathcal{A}(t)| \leq 1$ sui soli segnali attivi | :113 | sistema/validazione |
| B3-NFR-01 | osservazione barre 1-min da 8:00 CET | :171, :173 | operativo |
| B3-NFR-02 | primo pivot disponibile entro $N_{pivot}$ (valore → Parte V) | :173 | operativo |
| B3-NFR-03 | cadenza = barra 1-min chiusa, no tick intra-bar | :175 | operativo |

### 8.2 Nota di rinvio (materia adiacente al lifecycle, deliberatamente NON consolidata in B3)

Le seguenti materie sono **adiacenti** al lifecycle ma **rinviate** ad altri blocchi/Parti; la loro assenza in B3 è una scelta, non un gap di copertura:

- **Schema-payload come dato** (campi della tupla, domini, banda $b$ e cardinalità, target_1/2 come campi, `stop_loss`/$d_{stop}$/vincolo $d_{stop}>b$, qualificatori, i **domini** dei timer $\Delta t_{cromosoma}$/$T_{touch}^{max}$ come campi, immutabilità del payload 6.2, segnale unico attivo come proprietà-del-payload 6.3) → **B2** (Cap.6). In B3 questi sono citati come premessa, non ri-consolidati.
- **Condizioni / regola di emissione** (volatilità, liquidità, distanza, **filtro 80pt come regola**) → **B4** (Cap.8).
- **Pubblicazione Telegram** del `trigger_event` e dell'emissione, contratto informativo della notifica, ordine dei campi pubblicati, latenza, anti-duplicato, retry → **B4** (Cap.9).
- **Formato dei tre log** (emissione/transizioni/chiusura) e **determinismo bit-exact del replay**, granularità/persistenza del log → **B5/Cap.10**.
- **Sessione operativa come requisito** e verifica empirica della finestra 8:00–22:00 CET (M-GOV-1) → **B5** (in B3 la finestra compare solo come calendario su cui avanzano i counter dei timer).
- **Algoritmo** di pivot detection (Cap.15, Parte III); **definizione** delle condizioni strutturali di invalidazione (Parte IV); **regola di fill virtuale** in backtest (Parte III) → CAP chiusi / Parti III-IV (in B3 solo come rinvio).
- **Valori numerici congelati**: il tetto $N_{pivot}$ e i **valori** dei domini dei timer/soglie → **Parte V**. In B3 sono ammessi solo il calendario (finestra 8:00–22:00 CET) e il cap di 2 giorni come semantica su cui i counter avanzano, già fissati nei CAP chiusi.

---

*Documento B3 prodotto in cieco dai soli Cap.7 (7.1–7.6) e Cap.11 (11.1–11.5) di `CAP_02_parte_II.md` (chiuso PASS `a1625df`). Il confronto-copertura con la spec v2 congelata è compito esclusivo del Reviewer.*
