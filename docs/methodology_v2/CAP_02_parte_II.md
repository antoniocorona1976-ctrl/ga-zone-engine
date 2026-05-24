# Parte II — Contratto del segnale FIB

La Parte II formalizza il contratto del segnale che il motore emette verso l'operatore. Definisce che cosa è un segnale come oggetto strutturato, quali stati può attraversare nel proprio ciclo di vita, sotto quali condizioni di mercato il motore decide di emettere il segnale, in quale formato il segnale viene pubblicato sul canale Telegram, quale formato di log consente di ricostruire deterministicamente l'intero lifecycle a partire dallo storico delle barre 1-min, e come viene tracciato il position lifecycle post-target_1 come sottosistema distinto dal lifecycle del segnale. La Parte II non contiene la matematica del modello (volatilità condizionata, survival, geometria delle zone) né i parametri numerici congelati delle soglie e dei timer: la prima è demandata alle Parti III-IV, i secondi sono congelati in Parte V. La Parte II contiene il contratto che il motore deve onorare, che il GA ottimizza, e la submacchina di tracking che alimenta il reporting di calibrazione.

Le decisioni del supervisore prese in CAP-01 entrano qui come vincoli rigidi (heredità 1-10 elencate in ACTIVE_TASK.md): sessione FIB 8:00-22:00 CET come finestra unica e continua di negoziazione (Q-01); banda di ingresso $b \in \{5, 10, 15, 20, 25, 30, 35, 40\}$ punti FIB con $b_{min} = 5$ provvisorio; vincolo geometrico $d_{stop} > b$ obbligatorio; target_1 e target_2 entrambi obbligatori e ancorati a livelli strutturali, con target_2 informazione strutturale pubblicata (Q-05, Clausola 2); cap di validità $\leq 2$ giorni di trading decorrenti dal raw touch (non dall'emissione — patch CAP-01 Iterazione 2, commit `fc7531b`); movimento strutturale definito dalla somma dei moduli degli swing fra pivot strutturali, ancorato al primo min/max identificato dopo l'apertura della sessione (Q-02); filtro di emissione $\geq 80$ punti FIB su target_1 o ampiezza del rettangolo trade_range $\geq 80$ punti; nessuna esecuzione di ordini da parte del motore (punto 1 dichiarazione di intenti); tick size FIB = 5 punti; `executable_rate` ridefinita come frazione di segnali emessi che raggiungono il raw touch entro il timer di attesa pre-esecuzione, con il raw touch sempre eseguibile e le condizioni di mercato valutate prima dell'emissione (patch CAP-01 Iterazione 2).

La decisione del supervisore Q-05 (Opzione D raffinata, 2026-05-23) introduce tre clausole non separabili: (Clausola 1) la state machine del segnale è ridotta a 1 stato non-terminale + 6 stati terminali, con target_2_hit rimosso; (Clausola 2) target_2 resta campo obbligatorio del payload come informazione strutturale pubblicata; (Clausola 3) il position lifecycle post-target_1 è oggetto di una submacchina distinta (Cap.11), fuori scope dal motore ma in scope per il reporting.

Un fatto strutturale dello strumento permea tutta la Parte II e non è negoziabile: il FIB ha **tick size pari a 5 punti indice**. Tutti i prezzi del FIB si muovono per step discreti di 5 punti, non in continuum. Conseguenze immediate: $p_{ref}$, target_1, target_2, stop_loss sono multipli di 5; i bordi della banda di ingresso sono multipli di 5; la semi-ampiezza $b$ è essa stessa multipla di 5; $b_{min} = 5$ corrisponde esattamente a 1 tick. La cardinalità del dominio di $b$ è di 8 valori discreti: $\{5, 10, 15, 20, 25, 30, 35, 40\}$ punti FIB.

---

## Capitolo 6 — Schema del segnale e invarianti

### 6.1 Payload del segnale

Il segnale emesso dal motore è una tupla strutturata, immutabile dopo l'emissione, che descrive in modo completo l'ipotesi operativa pubblicata all'operatore. Si denota con $\mathcal{S}$ la tupla del segnale e con i seguenti campi i suoi attributi:

$$\mathcal{S} = \big( \texttt{signal\_id},\ \texttt{timestamp\_emission},\ \texttt{direction},\ \texttt{entry\_zone},\ \texttt{target\_1},\ \texttt{target\_2},\ \texttt{stop\_loss},\ \texttt{setup\_class},\ \Delta t_{cromosoma},\ T_{touch}^{max} \big)$$

Il significato e i vincoli di ciascun campo sono i seguenti.

**`signal_id`** — identificatore univoco del segnale, assegnato dal motore al momento dell'emissione. È un valore opaco non riutilizzabile, che funge da chiave primaria nei log di lifecycle (Cap.10) e nel messaggio Telegram (Cap.9). L'unicità è garantita all'interno dell'intero orizzonte operativo del motore, non soltanto della sessione corrente.

**`timestamp_emission`** — istante di emissione del segnale, espresso al minuto chiuso. Il riferimento orario è CET, coerente con la sessione operativa 8:00-22:00 CET definita in CAP-01 come finestra unica e continua di negoziazione. La precisione al minuto è coerente con la granularità delle barre 1-min usate dal motore in inference e in backtest.

**`direction`** — direzione del segnale, dominio $\{\text{long}, \text{short}\}$.

**`entry_zone`** — banda di prezzo discreta attorno al prezzo strutturale di riferimento $p_{ref}$, definita come

$$\texttt{entry\_zone} = \{p_{ref} - b,\ p_{ref} - b + 5,\ \ldots,\ p_{ref} + b - 5,\ p_{ref} + b\}$$

dove $b \in \{5, 10, 15, 20, 25, 30, 35, 40\}$ è la semi-ampiezza della banda espressa in punti FIB, parametro libero del cromosoma del GA, con $b_{min} = 5$ provvisorio congelato in Parte V. Il prezzo strutturale di riferimento $p_{ref}$ è derivato dalla geometria del prezzo (Parte IV) ed è anch'esso multiplo di 5, fissato al momento dell'emissione. La cardinalità della banda è $(2b/5) + 1$ livelli discreti. Il dominio di $b$ recepisce il vincolo del punto 2 della dichiarazione di intenti e introduce un floor $b_{min} = 5$ pari a un tick del FIB per evitare convergenza del GA su cromosomi con banda nulla.

**`target_1`** e **`target_2`** — due prezzi strutturali di obiettivo, entrambi obbligatori e distinti, multipli di 5. Per i segnali long valgono i vincoli $\texttt{target\_1} > p_{ref}$ e $\texttt{target\_2} > \texttt{target\_1}$; per i segnali short, simmetricamente, $\texttt{target\_1} < p_{ref}$ e $\texttt{target\_2} < \texttt{target\_1}$. Entrambi i target sono ancorati a livelli strutturali del prezzo, in coerenza con la decisione del supervisore in CAP-01 che proibisce target arbitrari non strutturali.

**Nota esplicita (decisione Q-05, Clausola 2)**: target_2 è informazione strutturale pubblicata, non variabile di lifecycle del segnale; il suo eventuale raggiungimento è evento del position lifecycle, fuori scope dal motore (vedi Cap.11). Il motore pubblica due livelli strutturali come informazione decisionale per l'operatore, ma il contratto del segnale si chiude al raggiungimento di target_1.

**`stop_loss`** — prezzo strutturale di stop, multiplo di 5, ancorato anch'esso alla geometria del prezzo (Parte IV, Cap.17). Si definisce la distanza dello stop dal prezzo di riferimento come

$$d_{stop} = |p_{ref} - \texttt{stop\_loss}|$$

espressa in punti FIB. Vale il vincolo geometrico obbligatorio

$$d_{stop} > b$$

ereditato da CAP-01. Cromosomi che producono segnali in violazione di questo vincolo sono dichiarati non validi e non entrano nella popolazione del GA. La motivazione è dichiarata in CAP-01: in assenza del vincolo, un fill al bordo opposto della banda potrebbe coincidere con il prezzo di stop, producendo un segnale eseguito e immediatamente stoppato nello stesso tick.

**`setup_class`** — classificazione del setup, dominio $\{\text{directional}, \text{trade\_range}\}$. Definisce la natura strutturale del segnale e la regola di filtro di emissione che gli si applica. Per i setup di classe `directional` vale il filtro

$$|\texttt{target\_1} - p_{ref}| \geq 80\ \text{punti FIB}$$

ovvero la distanza del primo target dal prezzo di riferimento non può essere inferiore a 80 punti. Per i setup di classe `trade_range` vale il filtro alternativo

$$|\texttt{target\_1} - \texttt{stop\_loss}| \geq 80\ \text{punti FIB}$$

ovvero l'ampiezza del rettangolo di prezzo entro cui il setup opera non può essere inferiore a 80 punti. Il vincolo degli 80 punti è un filtro di emissione, non un parametro libero del motore genetico, ed è applicato a valle della valutazione del cromosoma in coerenza con il punto 4 della dichiarazione di intenti e con quanto stabilito in CAP-01.

**$\Delta t_{cromosoma}$** — durata massima della fase post-trigger, espressa come intero in minuti di trading, dominio $\{1, 2, \ldots, 1680\}$, parametro libero del cromosoma del GA. La cardinalità 1680 corrisponde a $2 \times 840$ minuti, ovvero a due sessioni complete 8:00-22:00 CET (cap di validità di 2 giorni di trading ereditato da CAP-01, decorrente dal raw touch). L'`expiry` del segnale è calcolato al verificarsi del raw touch a istante $t_{exec}$:

$$\texttt{expiry} = t_{exec} + \Delta t_{cromosoma}\ \text{minuti di trading}$$

dove la somma è valutata sul calendario di trading dello strumento, non sul calendario solare. Cromosomi che producono valori di $\Delta t_{cromosoma}$ fuori dal dominio $\{1, \ldots, 1680\}$ sono dichiarati non validi. Questo campo era precedentemente denominato `expiry` nel payload; il nome $\Delta t_{cromosoma}$ è adottato in questa versione per enfatizzare che esso è il parametro ottimizzabile dal GA, non l'istante di scadenza calcolato.

**$T_{touch}^{max}$** — durata massima della fase di attesa pre-trigger (dall'emissione al raw touch), espressa come intero in minuti di trading, dominio $\{5, 6, \ldots, 480\}$ (cardinalità 476), parametro libero del cromosoma del GA. Floor $T_{touch}^{min} = 5$ minuti: un timer di attesa inferiore a 5 minuti di trading renderebbe l'emissione operativamente inutile dato che il messaggio Telegram ha latenza massima $L_{max}$ (Cap.9.3). Tetto $T_{touch}^{max} = 480$ minuti = 8 ore di trading: un segnale che non riceve raw touch entro 8 ore di trading dalla sua emissione ha presumibilmente perso il contesto strutturale che ne giustificava l'emissione. Allo scadere di questo timer senza raw touch, il segnale transita in stato terminale `expired` con causa `pretrigger_timeout` registrata nel log delle transizioni (Cap.10.3). La dipendenza funzionale di $T_{touch}^{max}$ dal regime di volatilità e dalla distanza corrente del prezzo rispetto a $p_{ref}$ è materia di Parte III/IV; in Parte II si fissa il contratto del parametro come leva ottimizzabile dal cromosoma.

### 6.2 Invariante di payload immutabile

Una volta emesso, il segnale identificato da `signal_id` non subisce alcuna modifica al proprio payload. La tupla $\mathcal{S}$ è congelata al momento dell'emissione: `entry_zone`, `target_1`, `target_2`, `stop_loss`, `setup_class`, $\Delta t_{cromosoma}$, $T_{touch}^{max}$ restano esattamente quelli pubblicati. Non esiste un'operazione di refresh o di edit del segnale che lasci invariato il `signal_id` e modifichi uno dei campi. L'invariante di payload immutabile è la condizione necessaria perché il segnale sia un oggetto contrattuale: l'operatore che lo riceve sul cellulare opera su quei valori e non su valori che possano mutare a sua insaputa fra il momento della lettura e il momento dell'invio dell'ordine al broker.

### 6.3 Regola di sostituzione e segnale unico attivo

Quando il motore valuta che le condizioni di mercato richiedono di rivedere il segnale corrente — perché il prezzo strutturale di riferimento è cambiato, perché i target strutturali sono stati ridefiniti dalla nuova geometria del prezzo, o perché il livello di stop non è più coerente con la struttura — esso non modifica il segnale esistente. Emette un nuovo segnale, contraddistinto da un nuovo `signal_id` univoco, con una propria tupla $\mathcal{S}'$ completa, indipendente dalla precedente. Contestualmente, il segnale precedente esce dall'insieme dei segnali attivi: viene revocato e transita nello stato terminale `revoked` (Cap.7), interrompendo qualsiasi prosecuzione del proprio lifecycle.

Sia $\mathcal{A}(t)$ l'insieme dei segnali attivi al tempo $t$. Vale il vincolo

$$|\mathcal{A}(t)| \leq 1\ \text{per ogni}\ t$$

ovvero a ogni istante è attivo al massimo un solo segnale. Questo vincolo recepisce contestualmente due decisioni dichiarate in CAP-01: il punto 7 della dichiarazione di intenti dell'operatore, che fissa l'operatività a 1 contratto alla volta; e il punto 6 della stessa dichiarazione, che prevede la revisione continua del segnale in funzione del prezzo strutturale corrente. La revisione, nell'architettura del contratto qui formalizzata, si manifesta come sostituzione: emissione di un nuovo `signal_id` con la nuova tupla congelata e revoca del precedente.

La regola di sostituzione si applica ai segnali in stato `active` (fase di attesa pre-trigger). Una volta che il segnale è transitato in un qualsiasi stato terminale (incluso `target_1_hit`), il contratto del segnale è chiuso e nessuna sostituzione ha effetto su quel `signal_id`. Il position lifecycle eventualmente avviato dopo `target_1_hit` è oggetto della submacchina distinta di Cap.11.

La regola di sostituzione produce due conseguenze operative rilevanti per il GA. La prima è che il GA ottimizza non soltanto la qualità del singolo segnale, ma anche la politica di sostituzione: emettere un nuovo segnale revocando il precedente comporta un costo (canale Telegram, log, lifecycle interrotto) e il cromosoma deve giustificarlo con un miglioramento atteso. La seconda è che il vincolo di segnale unico attivo elimina dal dominio del GA tutte le politiche multi-segnale concorrente, riconducendo il problema a una sequenza di segnali singoli sostituiti.

---

## Capitolo 7 — Stati del segnale e state machine

### 7.1 Stati e semantica

La state machine del segnale è costruita su un solo stato non-terminale e su sei stati terminali (decisione Q-05, Clausola 1). Lo stato non-terminale è il seguente.

**`active`** — il segnale è stato emesso, la sua tupla $\mathcal{S}$ è pubblicata, e il segnale è in attesa di un evento che lo porti in uno stato terminale. Mentre il segnale è `active`, il motore osserva il prezzo corrente, calcola gli eventi di mercato pertinenti (raw touch della entry zone, raggiungimento di target o stop prima del raw touch, scadenza del timer pre-trigger o post-trigger, invalidazione strutturale, decisione di sostituzione) e applica le transizioni previste.

Gli stati terminali, in cui il segnale conclude il proprio ciclo di vita e non transita ulteriormente, sono i seguenti. Nessun stato terminale ammette transizioni uscenti: il ciclo di vita del segnale è definitivamente chiuso all'ingresso in qualsiasi stato terminale.

**`target_1_hit`** — dopo il raw touch della entry zone, il prezzo ha raggiunto `target_1` prima di raggiungere `stop_loss`, prima della scadenza del timer post-trigger e prima di un'eventuale invalidazione strutturale. Stato terminale di successo del contratto del segnale. **Il contratto del segnale si chiude definitivamente qui**: il raggiungimento eventuale di target_2 dopo target_1 NON è una transizione di stato del segnale ma un evento del position lifecycle (Cap.11). Il segnale termina definitivamente in `target_1_hit` e non ammette transizioni uscenti verso alcun altro stato, incluso `revoked` o stati relativi a target_2. La gestione della posizione aperta oltre target_1 è dell'operatore manuale (punto 8 della dichiarazione di intenti).

**`stopped`** — dopo il raw touch della entry zone, il prezzo ha raggiunto `stop_loss` prima di raggiungere `target_1`, prima della scadenza del timer post-trigger e prima di un'eventuale invalidazione strutturale.

**`invalidated`** — prima del raw touch della entry zone, si è verificata una condizione di invalidazione strutturale che rompe l'ipotesi del setup. La definizione formale e completa delle condizioni di invalidazione strutturale è demandata a Parte IV; fra le condizioni esplicitamente incluse nel contratto del segnale rientra il superamento del livello `stop_loss` da parte del prezzo, nella direzione contraria all'ipotesi del segnale, prima del raw touch: per i segnali long, $p(t) \leq \texttt{stop\_loss}$ con $t < t_{touch}$; simmetricamente per gli short. La motivazione è strutturale: un prezzo che, prima ancora che la zona di ingresso sia toccata, supera il livello di stop del setup, dimostra che l'ipotesi del segnale è stata smentita dal mercato. Questo sotto-caso di `invalidated` è distinto da `stopped` (che richiede raw touch precedente) ed è necessario per coprire il percorso di prezzo che scende direttamente allo stop senza transitare nella zona di ingresso.

**`missed_target`** — prima del raw touch della entry zone, il prezzo ha raggiunto `target_1`. Il segnale si conclude in stato `missed_target`: il target strutturale è stato realizzato dal mercato ma il setup non si è eseguito perché la zona di ingresso non è mai stata toccata. La metrica missed_target_rate definita in CAP-01 è riferita esplicitamente a `target_1` e non a `target_2`, in coerenza con la chiusura Q-03 di CAP-01 da parte del supervisore: l'assenza di tracciamento di target_2 dopo `missed_target` è una scelta esplicita e non una svista. La simmetria con `target_1_hit` si ferma alla registrazione del solo primo target: in backtest, il GA riceve dalla metrica `missed_target_rate` informazioni sufficienti a calibrare la distanza della zona di ingresso rispetto al target_1 strutturale.

**`expired`** — il segnale è transitato in questo stato per una delle due cause seguenti, distinte nel log delle transizioni dal campo causale: (a) causa `posttrigger_timeout`: dopo il raw touch della entry zone ($t_{exec}$), sono trascorsi $\Delta t_{cromosoma}$ minuti di trading senza che il segnale transitasse in alcun altro stato terminale — il timer post-trigger ha esaurito il dominio $\{1, \ldots, 1680\}$ minuti; (b) causa `pretrigger_timeout`: il segnale era ancora in stato `active` senza aver ricevuto alcun raw touch alla data di scadenza del timer pre-trigger $T_{touch}^{max}$ — il motore ha contato $T_{touch}^{max}$ minuti di trading dall'emissione senza che il prezzo toccasse `entry_zone`. Entrambe le cause producono lo stesso stato terminale `expired`: la distinzione causale è registrata nel log delle transizioni come campo strutturato e non come stato dedicato, in coerenza con il vincolo di 6 soli stati terminali (Q-05, Clausola 1).

**`revoked`** — il segnale è stato superseduto dall'emissione di un nuovo `signal_id`, secondo la regola di sostituzione di Cap.6.3. La revoca avviene contestualmente all'emissione del nuovo segnale e interrompe il lifecycle del precedente. La regola di sostituzione si applica solo a segnali in stato `active`; nessuna sostituzione può revocare un segnale già terminato in `target_1_hit` o in qualsiasi altro stato terminale.

**Nota esplicita (chiusura NB-9)**: poiché `target_1_hit` è uno stato rigorosamente terminale senza transizioni uscenti, la transizione `target_1_hit → revoked` non esiste nella state machine del segnale. Se dopo il `target_1_hit` il motore emette un nuovo segnale, quel nuovo `signal_id` è un segnale indipendente; il segnale precedente è già definitivamente concluso. Nessuna ambiguità di interpretazione è pertanto possibile: il vincolo $|\mathcal{A}(t)| \leq 1$ si applica ai segnali attivi, e un segnale terminato non è attivo.

### 7.2 Transizioni ammesse

L'insieme delle transizioni ammesse dalla state machine, denotate $s \to s'$, è il seguente.

| Da | A | Condizione |
|----|---|------------|
| (creazione) | `active` | Emissione del segnale, generazione del `signal_id`, scrittura del log di emissione |
| `active` | `target_1_hit` | Dopo raw touch della entry zone ($t_{exec}$), il prezzo raggiunge `target_1` prima di `stop_loss`, prima dell'expiry post-trigger e prima di invalidazione strutturale |
| `active` | `stopped` | Dopo raw touch della entry zone ($t_{exec}$), il prezzo raggiunge `stop_loss` prima di `target_1`, prima dell'expiry e prima di invalidazione |
| `active` | `invalidated` | Prima del raw touch: si verifica condizione di invalidazione strutturale (Parte IV); fra cui esplicitamente $p(t) \leq \texttt{stop\_loss}$ per i long e $p(t) \geq \texttt{stop\_loss}$ per gli short con $t < t_{touch}$ |
| `active` | `missed_target` | Prima del raw touch: il prezzo raggiunge `target_1` |
| `active` | `expired` | (a) causa `posttrigger_timeout`: $t \geq t_{exec} + \Delta t_{cromosoma}$ min di trading e segnale ancora `active`; (b) causa `pretrigger_timeout`: $t \geq t_{emission} + T_{touch}^{max}$ min di trading, segnale ancora `active` senza raw touch |
| `active` | `revoked` | Il motore emette un nuovo `signal_id` (sostituzione, Cap.6.3) |

Nessuna transizione esce dagli stati terminali. In particolare, `target_1_hit` non ammette transizioni verso `target_2_hit` (rimosso dalla state machine), verso `revoked`, verso `stopped`, verso `expired` o verso qualsiasi altro stato: il contratto del segnale è concluso definitivamente al raggiungimento di target_1.

La precedenza degli eventi a parità di timestamp è: expiry > invalidazione > missed_target > raw touch > azione post-trigger. Questa precedenza, coerente con l'ordine dichiarato al Cap. 21.2 del baseline hard-locked, è essenziale per rendere deterministico il replay (Cap.10).

### 7.3 Raw touch ed esecuzione: un evento, non uno stato

Si definisce raw touch della entry zone del segnale $\mathcal{S}$ l'evento in cui il prezzo del FIB, osservato dal motore sulla barra 1-min chiusa, assume per la prima volta un valore appartenente all'insieme discreto $\texttt{entry\_zone} = \{p_{ref}-b, p_{ref}-b+5, \ldots, p_{ref}+b\}$. La definizione non impone alcun vincolo di direzione di provenienza del prezzo: la prima barra 1-min il cui intervallo high-low contenga almeno uno dei livelli discreti della zona produce il raw touch. Per i segnali long il livello operativamente atteso dall'operatore è tipicamente il bordo inferiore $p_{ref} - b$; per gli short il bordo superiore $p_{ref} + b$. Ma il contratto del segnale registra il raw touch indipendentemente da quale dei livelli discreti della zona è stato toccato per primo.

Al raw touch, il motore produce un evento, denotato `trigger_event`, che viene notificato all'operatore sul canale Telegram (Cap.9) con riferimento al `signal_id` del segnale corrente. **Il raw touch è sempre eseguibile**: non esistono nel contratto del segnale guardie o filtri post-emissione che blocchino il trigger una volta che il prezzo è entrato nella zona. La decisione di emettere o non emettere il segnale è già stata presa dal motore prima dell'emissione, sulla base delle condizioni di emissione di Cap.8. Una volta emesso il segnale, il raw touch è l'evento di esecuzione, senza ulteriori filtri.

Il `trigger_event` non è uno stato della state machine: il segnale resta in `active` finché un evento successivo (raggiungimento di `target_1` o `stop_loss`, invalidazione, scadenza, revoca) non lo porta in uno stato terminale. Il motore non osserva il fill manuale dell'operatore sul broker Directa, in quanto il motore non esegue ordini (vincolo del punto 1 della dichiarazione di intenti, ereditato da CAP-01) e l'operatore agisce manualmente dal cellulare. Mantenere `active` come unico stato non-terminale, e degradare il trigger a evento notificato, è una scelta di aderenza al perimetro operativo.

In simulazione di backtest il `trigger_event` viene trattato come fill virtuale a un prezzo determinato deterministicamente dalla regola di simulazione. La regola di riferimento è il fill al primo livello discreto della zona toccato dalla barra 1-min in cui si verifica il raw touch; il dettaglio operativo della regola di simulazione è specificato in Parte III. La regola di simulazione non altera la state machine pubblica del segnale.

**Edge case del raw touch (NB-8)**. Tre situazioni operative richiedono una regola esplicita.

**(a) Barra di emissione con prezzo già nella zona.** Il segnale è emesso alla chiusura della barra $t_{emission}$. Il motore valuta il raw touch a partire dalla barra $t_{emission} + 1$ (la prima barra chiusa dopo l'emissione). La barra di emissione stessa non è valutata: il payload non è ancora pubblicato al cellulare dell'operatore durante la barra di emissione e un raw touch sulla barra di emissione non è operativamente azionabile. Se il prezzo è già nella zona alla chiusura di $t_{emission}$ e rimane nella zona alle barre successive, il raw touch viene registrato alla prima barra $t_{emission} + 1$ il cui high-low contenga un livello della zona. Questa convenzione produce $t_{exec} = t_{emission} + 1$ minuto e il timer post-trigger $\Delta t_{cromosoma}$ decorre da tale istante. Se il prezzo era nella zona a $t_{emission}$ ma ne è già uscito a $t_{emission} + 1$, non vi è raw touch immediato e il segnale resta `active` in attesa del prossimo contatto.

**(b) Gap di apertura overnight con prezzo dentro o oltre la zona.** Un segnale emesso il giorno $D$ che non ha ricevuto raw touch entra nella sessione del giorno $D+1$ con la prima barra delle 8:00 CET. Se la barra di apertura del giorno $D+1$ apre con gap e il suo intervallo high-low contiene almeno un livello di `entry_zone`, il raw touch è registrato su quella barra di apertura ($t_{exec}$ = prima barra del giorno $D+1$). In backtest, il fill virtuale è convenzionalmente attribuito al livello della `entry_zone` più vicino all'open di apertura (bordo della zona dalla parte dell'open); se l'open è all'interno della zona, fill al livello della zona più vicino all'open. La regola deterministica di fill intrabar è specificata in dettaglio in Parte III, ma il contratto di Parte II fissa che il gap overnight **non** azzera il raw touch: il prezzo che apre dentro o attraverso la zona produce un trigger regolare.

**(c) Gap che salta interamente la zona nella direzione opposta.** Esempio: segnale long con entry_zone $[40990, 41010]$ e il prezzo apre a 40970 (sotto la zona), oppure segnale short con entry_zone $[41090, 41110]$ e il prezzo apre a 41130 (sopra la zona). In entrambi i casi, l'open della barra è sul lato della zona verso cui il segnale non punta strutturalmente. La regola è: se il prezzo si è allontanato dalla zona verso il lato che coincide con la direzione di `stop_loss` (es. per il long, il prezzo è sceso sotto la zona), il motore valuta se la condizione di `invalidated` (stop attraversato) sia soddisfatta; in caso contrario, il segnale resta `active` e attende che il prezzo rientri nella zona. Un gap che porta il prezzo al di sopra della zona per un segnale long (superamento di `target_1` senza raw touch) determina la transizione in `missed_target`.

### 7.4 Timer di scadenza post-esecuzione

Il cap di validità di 2 giorni di trading è implementato come timer concreto associato al singolo segnale e decorre dal raw touch. Come formalizzato in Cap.6.1, al verificarsi del raw touch a istante $t_{exec}$, il motore calcola:

$$\texttt{expiry} = t_{exec} + \Delta t_{cromosoma}\ \text{minuti di trading}$$

dove $\Delta t_{cromosoma} \in \{1, 2, \ldots, 1680\}$ è l'intero in minuti di trading ottimizzato dal cromosoma e la somma è valutata sul calendario di trading dello strumento, non sul calendario solare. Il counter $\Delta t_{cromosoma}$ avanza esclusivamente nei minuti compresi nella finestra 8:00-22:00 CET dei giorni di trading e si arresta nelle interruzioni notturne (22:00-8:00 del giorno successivo), nei weekend e nei festivi di mercato. Esempio: per un raw touch a $t_{exec}$ = lunedì 21:55 CET con $\Delta t_{cromosoma} = 1680$, il counter consuma 5 minuti il lunedì (21:55 → 22:00), riparte alle 8:00 del martedì, consuma 840 minuti martedì (8:00 → 22:00), riparte mercoledì alle 8:00, consuma i restanti 835 minuti (8:00 → 21:55). L'expiry è quindi mercoledì 21:55 CET.

Il timer è valutato dal motore ad ogni barra 1-min: appena $t \geq \texttt{expiry}$ e il segnale è ancora `active`, viene emesso l'evento di scadenza e il segnale transita in `expired` con causa `posttrigger_timeout`. Cromosomi che producono valori di $\Delta t_{cromosoma}$ fuori dal dominio $\{1, \ldots, 1680\}$ sono dichiarati non validi e non entrano nella popolazione del GA.

### 7.5 Timer pre-trigger di attesa al raw touch (NB-7)

Il segnale emesso resta in stato `active` in attesa del raw touch. Come formalizzato in Cap.6.1, il timer pre-trigger $T_{touch}^{max} \in \{5, 6, \ldots, 480\}$ minuti di trading è parametro libero del cromosoma. Il counter $T_{touch}^{max}$ avanza esclusivamente nei minuti di trading 8:00-22:00 CET, scavalcando le interruzioni notturne e i weekend, esattamente come il counter post-trigger $\Delta t_{cromosoma}$.

Allo scadere di $T_{touch}^{max}$ minuti di trading dalla `timestamp_emission` senza che sia avvenuto alcun raw touch, il segnale transita in `expired` con causa `pretrigger_timeout` nel log delle transizioni. La distinzione causale (`pretrigger_timeout` vs `posttrigger_timeout`) è un campo strutturato del log, non uno stato distinto della state machine: il vincolo di 6 soli stati terminali (Q-05, Clausola 1) è rispettato.

La patologia "segnale `active` per un tempo indefinitamente lungo in attesa del raw touch" — che potrebbe produrre strategie degeneri con emissione rara e attesa illimitata, gonfiando artificialmente l'`executable_rate` — è eliminata da questo timer. Il GA può tarare $T_{touch}^{max}$ liberamente nel dominio discreto $\{5, \ldots, 480\}$ minuti: un cromosoma che punta a zone strutturali molto distanti dal prezzo corrente può selezionare $T_{touch}^{max}$ più alto; un cromosoma che opera su zone ravvicinate selezionerà $T_{touch}^{max}$ più basso. La dipendenza funzionale ottimale di $T_{touch}^{max}$ dalla distanza $|p(t_{emission}) - p_{ref}|$ e dal regime di volatilità è materia di Parte III/IV (modello di first passage time); in Parte II si fissa il contratto del parametro come leva del cromosoma.

### 7.6 Identificazione real-time del primo pivot strutturale post-apertura (M-1)

In CAP-01 (Review carryover, M-1) è stato stabilito che il primo pivot strutturale post-apertura, usato come ancora del target di sessione 70% e del prezzo strutturale di riferimento, va trattato a livello di interfaccia in Parte II. L'algoritmo concreto di pivot detection è materia di Parte III (Cap.15); in Parte II si fissa il contratto di osservazione real-time del motore.

Il motore osserva la sequenza delle barre 1-min a partire dall'apertura della sessione alle 8:00 CET. A ciascuna barra chiusa il motore valuta se la barra appena conclusa costituisce, in retrospettiva sulla sequenza disponibile, un candidato pivot strutturale (minimo o massimo). La regola di confermabilità del pivot è demandata a Parte III, ma in Parte II vale come vincolo del contratto che il primo pivot strutturale post-apertura deve essere disponibile, in fase di calibrazione del motore, entro un numero massimo di barre 1-min dall'apertura della sessione. Il valore numerico del tetto $N_{pivot}$ non è fissato in Parte II: la sua quantificazione richiede misura empirica sullo storico FIB 1-min ed è congelata in Parte V sulla base della regola di pivot detection scelta in Parte III. Il vincolo metodologico, tuttavia, è dichiarato qui: la regola di pivot detection scelta in Parte III non può produrre un primo candidato di sessione con latenza tale da rendere di fatto inattiva la finestra iniziale di sessione, vanificando l'ancoraggio del target 70% al primo pivot post-apertura deciso dal supervisore in CAP-01 (chiusura Q-02).

La cadenza di valutazione della regola di pivot è la stessa cadenza di inference del motore, ovvero la barra 1-min chiusa. Il motore non opera su tick intra-bar per la pivot detection.

---

## Capitolo 8 — Condizioni di emissione del segnale

### 8.1 Filosofia del contratto di emissione

Il motore decide se emettere un segnale **prima** dell'emissione, sulla base di condizioni di mercato osservate al momento della valutazione. Una volta emesso il segnale, il contratto è semplice: il raw touch della entry zone è sempre eseguibile e produce il `trigger_event` (Cap.7.3). Non esistono nel contratto guardie o filtri post-emissione che blocchino il trigger.

La motivazione di questa architettura è triplice. **Primo**, è coerente con il punto 1 della dichiarazione di intenti dell'operatore: il motore emette segnali, l'esecuzione è dell'operatore. Un meccanismo di filtri post-emissione che bloccasse il trigger introdurrebbe una decisione di esecuzione mascherata da decisione di segnale. **Secondo**, le condizioni di emissione devono essere addestrabili sul GA, ovvero calcolabili sulla serie storica del FIB disponibile per il training. Lo storico Portara/CQG FIB 1-min copre OHLC e volume; non copre lo spread bid-ask né la profondità del book, che richiederebbero acquisti aggiuntivi di dati storici esplicitamente esclusi dall'infrastruttura definita in CAP-01. La condizione di spread è pertanto **eliminata**: nessuna condizione del contratto di emissione richiede dati non disponibili nello storico pianificato. **Terzo**, una volta che il segnale è stato emesso e l'operatore ha ricevuto il payload, l'operatore stesso valuta in tempo reale sul broker le condizioni di esecuzione visibili a lui (spread istantaneo, profondità del book, candela in corso) e decide se entrare manualmente.

Le condizioni di emissione qui formalizzate sono pertanto calcolabili dal motore in real-time esclusivamente sulla base di grandezze derivabili dalle barre 1-min del feed Directa, omogenee con le grandezze disponibili nello storico Portara/CQG per il training del GA.

### 8.2 Le tre condizioni di emissione

**Condizione di volatilità.** Il range della barra 1-min al momento della valutazione di emissione, definito come differenza fra prezzo massimo e prezzo minimo della barra appena chiusa, deve essere inferiore o uguale a una soglia $\tau_{vol}$ derivata dal modello di volatilità condizionata. Sia $r_{1m}(t)$ il range della barra 1-min al tempo $t$. La condizione è soddisfatta se

$$r_{1m}(t_{emission}) \leq \tau_{vol}\big(\hat{\sigma}_{\text{pt}}(t_{emission})\big)$$

dove $\hat{\sigma}_{\text{pt}}(t_{emission})$ è la stima di volatilità condizionata fornita dal modello EGARCH al tempo dell'emissione, **convertita in punti FIB** secondo la definizione $\hat{\sigma}_{\text{pt}}(t) = \hat{\sigma}(t) \cdot p_t$ (Parte III, Cap.13), e $\tau_{vol}(\cdot)$ è una funzione di soglia parametrizzata dal cromosoma del GA. Il senso operativo della condizione è impedire al motore di emettere segnali in barre di volatilità anomala, in cui il prezzo strutturale di riferimento è instabile e il payload del segnale rischia di essere immediatamente superseduto dalla regola di sostituzione. La forma esplicita di $\tau_{vol}$ è in Parte III.

**Condizione di liquidità.** Il volume della barra 1-min al momento della valutazione di emissione deve essere superiore o uguale a una soglia $\tau_{liq}$. Sia $v_{1m}(t)$ il volume contrattato sulla barra 1-min al tempo $t$. La condizione è soddisfatta se

$$v_{1m}(t_{emission}) \geq \tau_{liq}$$

Il senso operativo della condizione è impedire al motore di emettere segnali quando il mercato è anomalmente sottile, in quanto in tali condizioni il prezzo strutturale di riferimento può essere il risultato di poche operazioni non rappresentative. La soglia $\tau_{liq}$ è parametro libero del cromosoma, congelato in Parte V. La grandezza è disponibile sia nel feed real-time Directa sia nello storico Portara/CQG.

**Condizione di distanza strutturale in sigma-units (NB-10, opzione $\beta$ confermata).** La distanza fra il prezzo strutturale di riferimento del segnale candidato e il target_1 strutturale, espressa in sigma-units rispetto alla volatilità condizionata corrente, deve essere superiore o uguale a una soglia $\tau_{dist}^{\sigma}$. La condizione è

$$\frac{|\texttt{target\_1} - p_{ref}|}{\hat{\sigma}_{\text{pt}}(t_{emission})} \geq \tau_{dist}^{\sigma}$$

dove $\hat{\sigma}_{\text{pt}}(t_{emission})$ è la stima di volatilità condizionata fornita dal modello EGARCH, **convertita in punti FIB** secondo $\hat{\sigma}_{\text{pt}}(t) = \hat{\sigma}(t) \cdot p_t$ (Parte III, Cap.13), e $\tau_{dist}^{\sigma}$ è un numero puro (sigma-units FIB), parametro libero del cromosoma del GA. Il senso operativo della condizione è il seguente: distanze in punti FIB assoluti non sono confrontabili tra regimi di volatilità diversi — 80 punti sono una distanza moderata in regime turbolento, molto ampia in regime calmo. Esprimere la condizione in sigma-units consente al GA di tarare la distanza minima coerentemente con il regime in corso. La soglia $\tau_{dist}^{\sigma}$ ha dominio strettamente positivo e nessun floor inferiore assoluto in unità di sigma: il GA è libero di ottimizzarla nell'intero intervallo positivo, congelato in Parte V.

Il filtro 80 punti CAP-01 resta come vincolo assoluto a valle e non è sostituito dalla condizione in sigma-units: per setup directional $|\texttt{target\_1} - p_{ref}| \geq 80$ pt; per setup trade_range $|\texttt{target\_1} - \texttt{stop\_loss}| \geq 80$ pt. L'emissione richiede il soddisfacimento simultaneo di entrambi: la condizione in sigma-units come leva ottimizzabile del GA, il filtro 80pt come vincolo assoluto non allentabile. In regime di alta volatilità ($\hat{\sigma}$ elevato) il GA può richiedere distanze maggiori in sigma-units pur rispettando il floor di 80 pt in punti assoluti; in regime di bassa volatilità, i due vincoli possono coincidere o la condizione sigma-units può essere quella più stringente. In nessun caso il cromosoma può allentare il floor di 80 pt.

La separazione fra la condizione in sigma-units (parametro libero del cromosoma) e il filtro 80pt (vincolo fisso del contratto) è architetturalmente equivalente a quella fra il parametro $b_{min}=5$ (floor fisso della banda) e il parametro $b$ (valore ottimizzato dal cromosoma nel dominio $\{5, \ldots, 40\}$).

### 8.3 Regola di emissione

L'emissione del segnale $\mathcal{S}$ avviene se e solo se al tempo $t_{emission}$ valgono simultaneamente le tre condizioni di emissione e il filtro 80pt del `setup_class`. Sia $E_{vol}(t)$, $E_{liq}(t)$, $E_{dist}^{\sigma}(t)$, $E_{80pt}(t)$ il valore logico delle tre condizioni e del filtro al tempo $t$; il motore emette il segnale se e solo se

$$E_{vol}(t_{emission}) \land E_{liq}(t_{emission}) \land E_{dist}^{\sigma}(t_{emission}) \land E_{80pt}(t_{emission}) = \text{vero}$$

Se almeno una delle condizioni non è soddisfatta, il segnale candidato non viene emesso: nessun `signal_id` viene generato, nessuna pubblicazione Telegram avviene, nessun log di emissione viene scritto. Il motore continua a valutare le condizioni alle barre 1-min successive.

Le soglie $\tau_{vol}(\cdot)$, $\tau_{liq}$, $\tau_{dist}^{\sigma}$ sono parametri liberi del cromosoma del GA, ottimizzati dal motore genetico e congelati in Parte V. Le formule del modello di volatilità che alimentano $\hat{\sigma}_{\text{pt}}$ e la conversione in punti FIB sono in Parte III, Cap.13.

### 8.4 Assenza di filtri post-emissione e di fasi speciali nella sessione 8:00-22:00 CET

Una volta che il motore ha emesso il segnale, il raw touch della entry zone è sempre eseguibile (Cap.7.3): non esistono nel contratto guardie o filtri ulteriori che blocchino il `trigger_event`. Eventuali condizioni patologiche di mercato al momento del raw touch (spread istantaneo allargato sul broker, candela in corso violenta) sono valutate in autonomia dall'operatore manuale prima dell'invio dell'ordine; non sono filtrate dal motore.

Le condizioni di emissione di Cap.8.2 si applicano uniformemente lungo l'intera finestra 8:00-22:00 CET. Non si introducono fasi speciali (apertura, regolare, after-hours, asta) né soglie differenziate per fascia oraria. Questa scelta recepisce il chiarimento del supervisore che ha ritirato l'osservazione M-3 di Review v4 di CAP-01 (presunta fase d'asta 8:00-9:00) confermando che il FIB negozia in modo continuo nell'intera finestra 8:00-22:00.

---

## Capitolo 9 — Politica di pubblicazione su Telegram

### 9.1 Contesto del canale e vincolo operativo

Il canale di pubblicazione dei segnali è un bot Telegram personale dell'operatore, già attivo, come dichiarato in CAP-01. L'operatore opera da cellulare durante l'orario di lavoro presso l'istituto bancario di appartenenza, in modo discontinuo, e legge il segnale sul cellulare prima di inviare manualmente l'ordine al broker Directa. Il formato del messaggio deve essere progettato per la lettura mobile in condizioni di attenzione limitata, e il canale deve garantire una latenza di consegna compatibile con l'urgenza operativa del segnale.

Il dettaglio tecnico del setup del bot, della gestione del `chat_id` e delle stringhe esatte del messaggio è rinviato all'Appendice E. In Parte II si fissano il contratto informativo del messaggio (quali campi del payload del segnale sono pubblicati e in quale ordine), il vincolo di latenza, la politica anti-duplicato, la regola di emissione di messaggi nuovi per segnali nuovi, e la gestione di errori di pubblicazione.

### 9.2 Contratto informativo del messaggio

Il messaggio Telegram pubblicato in corrispondenza dell'emissione di un segnale $\mathcal{S}$ contiene, in ordine obbligatorio, i seguenti campi del payload, presentati in forma leggibile da operatore mobile:

1. `signal_id` — l'identificatore del segnale, riportato in chiaro come chiave operativa
2. `direction` — direzione long o short, evidenziata in modo immediato
3. `setup_class` — directional o trade_range, per distinguere il senso del filtro 80 punti applicato
4. `entry_zone` — banda di prezzo discreta, esplicitata come intervallo $[p_{ref}-b, p_{ref}+b]$ in punti FIB
5. `target_1` e `target_2` — i due target strutturali, distinti e ordinati
6. `stop_loss` — il prezzo strutturale di stop
7. `timestamp_emission` — l'istante di emissione, riportato come data e ora CET

I campi $\Delta t_{cromosoma}$ e $T_{touch}^{max}$ non figurano nel messaggio all'operatore: sono parametri tecnici del modello rilevanti per il log interno (Cap.10) ma non per la decisione operativa dell'operatore, che deve soltanto valutare se entrare al raw touch della zona pubblicata. Il messaggio non contiene istruzioni di gestione attiva della posizione (incrementi, scaling out, take profit anticipato, stop profit), in coerenza con il punto 8 della dichiarazione di intenti che riserva queste decisioni all'operatore.

### 9.3 Latenza di consegna

Si definisce latenza di consegna del segnale, $L$, l'intervallo di tempo tra l'istante in cui il motore conclude la valutazione dell'emissione (`timestamp_emission`) e l'istante in cui il messaggio è ricevuto sul cellulare dell'operatore. Vale il vincolo

$$L \leq L_{max}$$

dove $L_{max}$ è la latenza massima ammissibile, congelata in Parte V. Il valore di lavoro provvisorio è $L_{max} = 30$ secondi: oltre questa soglia, il segnale perde valore informativo perché il prezzo strutturale di riferimento può essersi spostato in modo non trascurabile rispetto al momento dell'emissione. La verifica empirica della latenza effettiva del canale Telegram e la definizione operativa del valore congelato sono materia di Appendice E.

### 9.4 Politica anti-duplicato

Il motore pubblica ciascun `signal_id` una sola volta. La regola è formalizzata come segue: sia $\mathcal{P}$ l'insieme dei `signal_id` per cui il motore ha già pubblicato un messaggio Telegram con successo; per ogni nuovo segnale $\mathcal{S}$ con identificatore `signal_id`, il motore pubblica il messaggio se e solo se `signal_id` $\notin \mathcal{P}$, e contestualmente aggiunge `signal_id` a $\mathcal{P}$. L'insieme $\mathcal{P}$ è persistito su disco insieme al log di emissione (Cap.10), in modo che restart del motore non comportino ripubblicazione di segnali già notificati.

### 9.5 Nuovo segnale come messaggio separato; notifica del trigger_event

Quando il motore emette un nuovo segnale $\mathcal{S}'$ in sostituzione di un segnale precedente $\mathcal{S}$, secondo la regola di sostituzione di Cap.6.3, il messaggio Telegram corrispondente a $\mathcal{S}'$ è pubblicato come messaggio separato, con il proprio `signal_id` distinto. Non viene effettuata alcuna operazione di modifica o di edit sul messaggio Telegram precedente. Il messaggio del segnale revocato resta visibile nella cronologia della chat come traccia storica, ma non rappresenta più un segnale attivo: lo stato `revoked` è registrato nel log interno (Cap.10). La scelta di emettere messaggi separati anziché editare il messaggio esistente è coerente con l'invariante di payload immutabile di Cap.6.2: editare il messaggio del segnale precedente equivarrebbe a modificare il suo payload pubblicato, violando la regola.

Al verificarsi del `trigger_event` (raw touch della entry zone) il motore pubblica una notifica separata sul canale Telegram, che fa riferimento al `signal_id` del segnale corrente, all'istante $t_{exec}$ del raw touch e all'`expiry` calcolata. La notifica del `trigger_event` è funzionalmente distinta dal messaggio di emissione: l'emissione comunica all'operatore l'esistenza del segnale e i suoi parametri, la notifica del trigger gli comunica che il prezzo è entrato nella zona e che il segnale è eseguibile. Il dettaglio del contratto informativo della notifica del trigger è in Appendice E; in Parte II si fissa il vincolo che essa sia pubblicata come messaggio separato e non come edit, contestualmente al riconoscimento del raw touch da parte del motore.

### 9.6 Gestione degli errori di pubblicazione

In caso di errore nella chiamata all'API Telegram (timeout, errori di rete, indisponibilità temporanea del servizio), il motore applica una politica di retry. La politica prevede:

- numero massimo di tentativi $n_{retry}$, valore di lavoro provvisorio $n_{retry} = 3$
- backoff esponenziale fra i tentativi, con base provvisoria $\Delta t_{retry} = 2$ secondi raddoppiata a ogni tentativo
- in caso di fallimento finale (tutti i tentativi esauriti), registrazione dell'errore nel log di emissione e nessuna ulteriore pubblicazione; il `signal_id` non viene aggiunto a $\mathcal{P}$ e il segnale è registrato come non pubblicato

Il fallimento di pubblicazione è tracciato nel log e non rimane implicito. I parametri $n_{retry}$, $\Delta t_{retry}$ e $L_{max}$ sono congelati in Parte V; le specifiche di interazione con l'API Telegram sono in Appendice E.

---

## Capitolo 10 — Replay e riproducibilità del lifecycle

### 10.1 Obiettivo del log e requisito di determinismo

Il log del lifecycle del segnale deve consentire di ricostruire, a partire dallo storico delle barre 1-min del FIB e da quello dei feed ausiliari utilizzati dal motore (contesto cross-index, volumi), l'esatta sequenza degli stati attraversati da ogni segnale emesso, con i timestamp e i prezzi che hanno innescato ciascuna transizione.

**Requisito di determinismo.** Dato lo stesso storico delle barre 1-min e dei feed ausiliari e lo stesso bundle frozen (cromosoma con parametri congelati e versione del codice congelata), il replay del motore deve produrre esattamente la stessa sequenza di emissioni, di `signal_id`, di transizioni di stato, e degli stessi timestamp di transizione. Vale

$$\forall\ \text{storico}\ H,\ \forall\ \text{bundle}\ B:\quad \texttt{replay}(H, B) = \texttt{replay}(H, B)\ \text{(bit-exact)}$$

dove $\texttt{replay}(\cdot,\cdot)$ è la funzione di replay del motore. Nessuna sorgente di non-determinismo è introdotta dal motore: in particolare, non si utilizzano generatori pseudo-casuali non seedati, e qualsiasi componente che richieda inizializzazione casuale (es. inizializzazioni del modello EGARCH, jitter di latenza simulato per test) deve essere seedata e il seed deve essere parte del bundle congelato.

Il determinismo del replay è la condizione necessaria perché le metriche di lifecycle calcolate sul replay OOS abbiano valore probatorio: una metrica calcolata su un replay non riproducibile non è verificabile e non può essere usata come gate decisionale per il go-live (Parte VII, Cap.35).

### 10.2 Log di emissione

In corrispondenza di ogni emissione di un nuovo segnale, il motore scrive un log di emissione contenente:

- l'intero payload del segnale $\mathcal{S}$ (tutti i campi di Cap.6.1, fissati al momento dell'emissione), inclusi $\Delta t_{cromosoma}$ e $T_{touch}^{max}$
- lo snapshot delle tre condizioni di emissione al momento $t_{emission}$: valori di $r_{1m}$, $v_{1m}$ e $|\texttt{target\_1} - p_{ref}| / \hat{\sigma}_{\text{pt}}$, con le soglie correnti $\tau_{vol}(\hat{\sigma}_{\text{pt}}(t_{emission}))$, $\tau_{liq}$, $\tau_{dist}^{\sigma}$ in vigore al momento (cromosoma frozen del bundle); esito del filtro 80pt per `setup_class`
- lo snapshot delle feature del modello al momento dell'emissione: $\hat{\sigma}(t_{emission})$, classificazione di regime, valore corrente delle feature causali utilizzate dal cromosoma per la decisione di emissione
- il `signal_id` dell'eventuale segnale precedente revocato per sostituzione, se l'emissione è una sostituzione (Cap.6.3)
- esito della pubblicazione Telegram: successo o fallimento, numero di tentativi, eventuale codice di errore (Cap.9.6)

Il log di emissione è scritto in formato strutturato, idoneo a essere consumato sia dal modulo di replay sia dagli strumenti di analisi delle metriche OOS. Il formato esatto è definito in Appendice B.

### 10.3 Log delle transizioni di stato

Per ogni transizione di stato registrata dalla state machine di Cap.7, il motore scrive una riga di log con:

- `signal_id` del segnale interessato
- timestamp della transizione (al minuto chiuso, coerente con la granularità del modello)
- stato precedente e stato nuovo (uno dei valori ammessi di Cap.7.1)
- prezzo che ha innescato la transizione, quando applicabile (prezzo di raw touch per `trigger_event`, prezzo di `target_1` per la transizione a `target_1_hit`, prezzo di `stop_loss` per `stopped` o `invalidated` per stop attraversato pre-touch, e così via)
- in caso di transizione causata da una condizione non riducibile a un singolo prezzo (`invalidated` per condizioni strutturali diverse dal superamento di stop, `revoked`, `expired`): una descrizione strutturata della causa, con campo causale obbligatorio per `expired` ($\{\texttt{pretrigger\_timeout}, \texttt{posttrigger\_timeout}\}$)

Il `trigger_event` di Cap.7.3 viene registrato nel log delle transizioni come evento associato al segnale, con la nota esplicita che non è una transizione di stato (il segnale resta in `active`) ma un evento notificato sul canale Telegram; la registrazione nel log assicura che il replay possa ricostruire l'istante esatto $t_{exec}$ da cui decorre il timer post-trigger $\Delta t_{cromosoma}$.

### 10.4 Log di chiusura

Quando il segnale entra in uno stato terminale (Cap.7.1), il motore scrive un log di chiusura contenente:

- `signal_id`
- stato terminale finale
- causa (per `expired`: `pretrigger_timeout` o `posttrigger_timeout`)
- timestamp di chiusura
- statistiche aggregate del segnale: rendimento lordo realizzato in punti FIB (se il segnale è stato eseguito, ovvero ha generato un `trigger_event`); MAE (maximum adverse excursion) e MFE (maximum favourable excursion) misurate dal momento del `trigger_event` al momento della chiusura; durata totale del lifecycle in minuti di trading dal `timestamp_emission` alla chiusura; durata della fase pre-trigger in minuti di trading da `timestamp_emission` a $t_{exec}$ (esplicitata come campo a sé stante, non solo derivabile per differenza); durata della fase post-trigger in minuti di trading da $t_{exec}$ alla chiusura

Il rendimento netto per segnale eseguito è derivato dal rendimento lordo applicando la formula di CAP-01 (Cap.5): $E[R_{net}\mid executed] = E[R_{gross}\mid executed] - 2 \cdot c$ con $c = 1$ punto FIB equivalente per operazione. Il calcolo del rendimento netto non è registrato nel log di chiusura come campo aggiuntivo, in quanto derivabile deterministicamente dal lordo: il valore probatorio della grandezza è preservato dal determinismo del replay.

### 10.5 Granularità temporale e fonte del prezzo

I timestamp riportati nei log di emissione, transizione e chiusura sono espressi al minuto chiuso e si riferiscono al fuso CET, coerente con la sessione FIB 8:00-22:00 CET ereditata da CAP-01. La fonte dei prezzi utilizzati per valutare le transizioni di stato è la barra 1-min consolidata del FIB; per la sessione live, la barra è prodotta dal motore consolidando il feed real-time di Directa DAPI (porta 10001), secondo la specifica dell'Appendice C. In backtest, la barra è quella dello storico Portara/CQG (Appendice D). La consistenza fra la barra real-time consolidata in produzione e la barra storica usata in backtest è un requisito di qualità dei dati verificato all'ingresso (Parte III) e non un parametro del modello.

### 10.6 Persistenza e versionamento del log

I tre log (emissione, transizioni, chiusura) sono persistiti in modo che il replay possa essere ricostruito anche dopo un restart del motore o un cambio di macchina di esecuzione. La persistenza è ortogonale alla persistenza dell'insieme $\mathcal{P}$ dei `signal_id` pubblicati (Cap.9.4): le due strutture sono coerenti per costruzione, in quanto il log di emissione contiene già l'esito della pubblicazione Telegram. Il versionamento del bundle frozen utilizzato per generare ciascuna emissione è registrato nel log di emissione: ogni transizione e ogni chiusura sono pertanto associabili al cromosoma e alla versione di codice che le hanno prodotte. Il dettaglio del meccanismo di versionamento del bundle frozen è in Parte VII (Cap.34).

---

## Capitolo 11 — Position lifecycle e tracking out-of-scope dal motore

### 11.1 Separazione formale segnale vs position lifecycle

La decisione del supervisore Q-05 (Opzione D raffinata, Clausola 3) introduce una separazione architetturale esplicita tra due sottosistemi distinti per natura e per responsabilità:

1. **Lifecycle del segnale** (Cap.6-10): il contratto del motore, ottimizzato dal GA, che si chiude definitivamente al raggiungimento di `target_1_hit` o di qualsiasi altro stato terminale.
2. **Position lifecycle** (questo capitolo): la submacchina di tracking degli eventi post-target_1, oggetto del reporting per la validazione del GA, fuori scope dal motore per quanto riguarda le decisioni operative.

Il fondamento metodologico di questa separazione è formalizzato nel baseline hard-locked. Al Cap. 21.1 del documento `docs/reference/ENGINE_ALGO_INTEGRATO_HARD_LOCKED.pdf` si legge:

> "Il lifecycle della posizione oltre il fill è un sottosistema distinto e non va confuso con il lifecycle del contratto di segnale."

Al Cap. 22.6 dello stesso documento:

> "La gestione fine dei partial fill viene trattata come submacchina della posizione e dunque come boundary del presente documento. [...] Il modo più semplice di rispettare il boundary è trattare il primo partial fill come passaggio del segnale in EXECUTED, spostando la gestione quantitativa della posizione in un sottosistema distinto."

Nel contesto del presente motore, che emette segnali senza eseguire ordini, il "fill" corrisponde al raw touch della entry zone (`trigger_event`), e il "boundary" citato al Cap. 22.6 coincide con `target_1_hit`: il segnale si chiude in `target_1_hit` e la gestione della posizione oltre tale soglia è responsabilità dell'operatore umano, con il solo supporto informativo della submacchina di tracking.

### 11.2 Perimetro della submacchina: OUT-OF-SCOPE e IN-SCOPE

La separazione dei perimetri è la seguente.

**OUT-OF-SCOPE dal motore** (decisione Q-05, Clausola 3): execution policy, scaling-out automatico, trailing stop, dynamic sizing, take profit anticipato, qualsiasi decisione operativa post-target_1. La gestione della posizione oltre target_1 è interamente e irrevocabilmente dell'operatore manuale (punto 8 della dichiarazione di intenti: "non deve calcolare e proporre take o stop profit nel segnale dove ha definito il target, take o stop profit li gestisco io"). Nessun parametro del cromosoma del GA e nessuna regola del motore governa la posizione dopo che il segnale è terminato in `target_1_hit`.

**IN-SCOPE per reporting e validazione**: la submacchina di tracking produce metriche che alimentano i report fold-by-fold del walk-forward (Parte V, Cap.23). Le metriche sono:

- **hit-rate condizionale di target_2 dato target_1** ($\pi_{t_2 \mid t_1}$): frequenza con cui il prezzo raggiunge target_2 nelle sessioni di backtest che si sono chiuse in `target_1_hit`. Questa metrica informa il GA sulla qualità strutturale dei livelli target_2 pubblicati nel payload: un $\pi_{t_2 \mid t_1}$ elevato segnala che target_2 è un livello strutturale robusto; uno $\pi_{t_2 \mid t_1}$ basso segnala che il payload pubblica un livello nominalmente strutturale ma non realizzato dal mercato con frequenza sufficiente.
- **Distribuzioni di MFE e MAE post-target_1**: maximum favourable excursion e maximum adverse excursion a partire dall'istante di `target_1_hit`, misurate fino alla chiusura della posizione o all'evento successivo registrato. Queste distribuzioni sono input alla validazione della robustezza strutturale del setup in Parte IV/V.
- **Frequenza di stop post-target_1** ($f_{stop \mid t_1}$): frequenza con cui il prezzo, dopo aver raggiunto target_1, ritraccia fino al livello di stop_loss originale del segnale. Questo evento non è registrato come stato del segnale (che è già terminato in `target_1_hit`) ma come evento della submacchina, rilevante per la valutazione della qualità strutturale dello stop_loss pubblicato.
- **Distribuzione dei tempi di permanenza post-target_1**: distribuzione dell'intervallo di tempo in minuti di trading fra `target_1_hit` e il successivo evento terminale della submacchina (raggiungimento target_2, stop post-target_1, chiusura a tempo). Informa la calibrazione del timing implicito della gestione manuale.

### 11.3 Struttura della submacchina di tracking

La submacchina di position lifecycle è una macchina a stati distinta e indipendente dalla state machine del segnale. Essa si attiva quando il segnale associato transita in `target_1_hit` e opera in parallelo rispetto al lifecycle del segnale, che nel frattempo è definitivamente concluso.

**Evento di ingresso**: il segnale ha raggiunto `target_1_hit`. A quel momento, la submacchina registra il prezzo di `target_1`, il prezzo di `stop_loss` del segnale, il prezzo di `target_2` (recuperato dal payload immutabile), e l'istante di ingresso.

**Stato iniziale della submacchina**: `tracking_active`. Indica che la submacchina sta osservando la dinamica del prezzo successiva a `target_1_hit`.

**Eventi registrati dalla submacchina** (non stati del segnale):
- `target_2_reached`: il prezzo ha raggiunto il livello `target_2` del payload originale del segnale.
- `stop_after_target_1`: il prezzo ha ritracciato fino al livello `stop_loss` del segnale originale dopo aver raggiunto `target_1`.
- `retracement_to_entry`: il prezzo è tornato all'interno dell'`entry_zone` del segnale originale dopo `target_1_hit` (evento informativo per l'analisi della struttura del setup).
- `position_close_event`: la posizione è stata chiusa dall'operatore. In backtest, la convenzione di chiusura simulata è specificata in Parte III/V (es. fine sessione, raggiungimento di target_2 o di stop).

**Stato terminale della submacchina**: `tracking_closed`. La submacchina termina al verificarsi del primo evento terminante dichiarato in Parte V (in backtest: raggiungimento di `target_2_reached`, `stop_after_target_1` o fine sessione, quello che avviene prima).

**Indipendenza dalla state machine del segnale**: la submacchina **non modifica lo stato del segnale** in nessuna circostanza. Il segnale è terminato in `target_1_hit` prima ancora che la submacchina inizi a tracciare. I log della submacchina sono separati dai log del lifecycle del segnale (Cap.10) e sono scritti in un registro distinto, referenziato dal `signal_id` del segnale che ha innescato il tracking.

### 11.4 Impatto sul GA e sullo space search del cromosoma

**Lo space search del cromosoma del GA non viene esteso.** Nessuna policy decisionale post-target_1 entra nel cromosoma: il GA non ottimizza trailing stop, take profit anticipato, scaling-out, né alcuna regola di gestione della posizione oltre `target_1_hit`. Questa è una conseguenza diretta della Clausola 3 della decisione Q-05 e del vincolo del punto 8 della dichiarazione di intenti.

Le metriche prodotte dalla submacchina ($\pi_{t_2 \mid t_1}$, MFE post-target_1, MAE post-target_1, $f_{stop \mid t_1}$) entrano nella fitness multi-obiettivo del GA come **obiettivi di qualità informativa del payload**, non come variabili decisionali del cromosoma. In altri termini: il GA ottimizza la capacità del segnale di pubblicare livelli target_2 e stop_loss strutturalmente robusti — quelli che il mercato realizza con alta probabilità — ma non la politica di gestione della posizione una volta che target_1 è stato raggiunto.

Il razionale metodologico è il seguente. Un cromosoma che pubblica un target_2 con $\pi_{t_2 \mid t_1}$ elevato fornisce all'operatore informazione strutturale di valore: l'operatore può scegliere di tenere la posizione puntando al secondo livello con una probabilità favorevole. Questo aspetto della qualità del segnale è misurabile, ottimizzabile dal GA, e coerente con il perimetro del motore. Al contrario, la policy "come gestire la posizione dopo target_1" è dell'operatore e non deve essere nel cromosoma: introdurla violerebbe il punto 8 della dichiarazione di intenti e esploderebbe combinatoriamente lo space search senza produrre segnali migliori, solo cromosomi più complessi e più soggetti a overfitting (DSR/PBO meno robusti).

### 11.5 Relazione con il reporting fold-by-fold del walk-forward

Le metriche della submacchina alimentano i report fold-by-fold del walk-forward (Parte V, Cap.23). Per ogni fold OOS, il report di validazione include:

- la distribuzione di $\pi_{t_2 \mid t_1}$ per i segnali del fold che hanno raggiunto `target_1_hit`
- le statistiche di MFE e MAE post-target_1 per lo stesso insieme
- la frequenza di stop post-target_1 ($f_{stop \mid t_1}$)

Queste statistiche contribuiscono alla valutazione della robustezza strutturale del cromosoma nel fold: un cromosoma con alta frequenza di `target_1_hit` ma basso $\pi_{t_2 \mid t_1}$ e alta $f_{stop \mid t_1}$ segnala setup strutturalmente fragili, in cui il prezzo raggiunge target_1 ma poi retrocede frequentemente. La metrica primaria di successo del motore rimane il profitto netto al netto delle commissioni in punti FIB realizzato dai segnali eseguiti: $\pi_{t_2 \mid t_1}$, MFE, MAE e $f_{stop \mid t_1}$ sono strumenti di verifica e calibrazione, non la definizione di successo.
