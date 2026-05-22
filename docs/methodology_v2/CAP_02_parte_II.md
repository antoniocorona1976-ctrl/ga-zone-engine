# Parte II — Contratto del segnale FIB

La Parte II formalizza il contratto del segnale che il motore emette verso l'operatore. Definisce che cosa è un segnale come oggetto strutturato, quali stati può attraversare nel proprio ciclo di vita, sotto quali condizioni di mercato il motore decide di emettere il segnale, in quale formato il segnale viene pubblicato sul canale Telegram, e quale formato di log consente di ricostruire deterministicamente l'intero lifecycle a partire dallo storico delle barre 1-min. La Parte II non contiene la matematica del modello (volatilità condizionata, survival, geometria delle zone) né i parametri numerici congelati delle soglie e dei timer: la prima è demandata alle Parti III-IV, i secondi sono congelati in Parte V. La Parte II contiene il contratto che il motore deve onorare e che il GA ottimizza.

Le decisioni del supervisore prese in CAP-01 entrano qui come vincoli rigidi: sessione FIB 8:00-22:00 CET come finestra unica e continua di negoziazione; banda di ingresso $b \in [b_{min}, 40]$ punti FIB con $b_{min} = 5$ provvisorio; vincolo geometrico $d_{stop} > b$ obbligatorio; target 1 e target 2 entrambi obbligatori e ancorati a livelli strutturali; cap di validità $\leq 2$ giorni di trading dall'esecuzione; movimento strutturale definito dalla somma dei moduli degli swing fra pivot strutturali, ancorato al primo min/max identificato dopo l'apertura della sessione; filtro di emissione $\geq 80$ punti FIB su target 1 o ampiezza del rettangolo trade range $\geq 80$ punti; nessuna esecuzione di ordini da parte del motore, in coerenza con il punto 1 della dichiarazione di intenti dell'operatore.

Un fatto strutturale dello strumento permea tutta la Parte II e non è negoziabile: il FIB ha **tick size pari a 5 punti indice**. Tutti i prezzi del FIB si muovono per step discreti di 5 punti, non in continuum. Conseguenze immediate: $p_{ref}$, target_1, target_2, stop_loss sono multipli di 5; i bordi della banda di ingresso sono multipli di 5; la semi-ampiezza $b$ è essa stessa multipla di 5; $b_{min} = 5$ corrisponde esattamente a 1 tick. La cardinalità del dominio di $b$ è di 8 valori discreti: $\{5, 10, 15, 20, 25, 30, 35, 40\}$ punti FIB.

---

## Capitolo 6 — Schema del segnale e invarianti

### 6.1 Payload del segnale

Il segnale emesso dal motore è una tupla strutturata, immutabile dopo l'emissione, che descrive in modo completo l'ipotesi operativa pubblicata all'operatore. Si denota con $\mathcal{S}$ la tupla del segnale e con i seguenti campi i suoi attributi:

$$\mathcal{S} = \big( \texttt{signal\_id},\ \texttt{timestamp\_emission},\ \texttt{direction},\ \texttt{entry\_zone},\ \texttt{target\_1},\ \texttt{target\_2},\ \texttt{stop\_loss},\ \texttt{expiry},\ \texttt{setup\_class} \big)$$

Il significato e i vincoli di ciascun campo sono i seguenti.

**`signal_id`** — identificatore univoco del segnale, assegnato dal motore al momento dell'emissione. È un valore opaco non riutilizzabile, che funge da chiave primaria nei log di lifecycle (Cap.10) e nel messaggio Telegram (Cap.9). L'unicità è garantita all'interno dell'intero orizzonte operativo del motore, non soltanto della sessione corrente.

**`timestamp_emission`** — istante di emissione del segnale, espresso al minuto chiuso. Il riferimento orario è CET, coerente con la sessione operativa 8:00-22:00 CET definita in CAP-01 come finestra unica e continua di negoziazione. La precisione al minuto è coerente con la granularità delle barre 1-min usate dal motore in inference (Parte VI) e in backtest (Parte III).

**`direction`** — direzione del segnale, dominio $\{\text{long}, \text{short}\}$.

**`entry_zone`** — banda di prezzo discreta attorno al prezzo strutturale di riferimento $p_{ref}$, definita come

$$\texttt{entry\_zone} = \{p_{ref} - b,\ p_{ref} - b + 5,\ \ldots,\ p_{ref} + b - 5,\ p_{ref} + b\}$$

dove $b \in \{5, 10, 15, 20, 25, 30, 35, 40\}$ è la semi-ampiezza della banda espressa in punti FIB, parametro libero del cromosoma del GA, con $b_{min} = 5$ provvisorio congelato in Parte V. Il prezzo strutturale di riferimento $p_{ref}$ è derivato dalla geometria del prezzo (Parte IV) ed è anch'esso multiplo di 5, fissato al momento dell'emissione. La cardinalità della banda è $(2b/5) + 1$ livelli discreti. Il dominio recepisce il vincolo del punto 2 della dichiarazione di intenti, che pone il tetto superiore a 40 punti, e introduce un floor $b_{min} = 5$ pari a un tick del FIB per evitare convergenza del GA su cromosomi con banda nulla.

**`target_1`** e **`target_2`** — due prezzi strutturali di obiettivo, entrambi obbligatori e distinti, multipli di 5. Per i segnali long valgono i vincoli $\texttt{target\_1} > p_{ref}$ e $\texttt{target\_2} > \texttt{target\_1}$; per i segnali short, simmetricamente, $\texttt{target\_1} < p_{ref}$ e $\texttt{target\_2} < \texttt{target\_1}$. Entrambi i target sono ancorati a livelli strutturali del prezzo, in coerenza con la decisione del supervisore in CAP-01 che proibisce target arbitrari non strutturali.

**`stop_loss`** — prezzo strutturale di stop, multiplo di 5, ancorato anch'esso alla geometria del prezzo (Parte IV, Cap.17). Si definisce la distanza dello stop dal prezzo di riferimento come

$$d_{stop} = |p_{ref} - \texttt{stop\_loss}|$$

espressa in punti FIB. Vale il vincolo geometrico obbligatorio

$$d_{stop} > b$$

ereditato da CAP-01. Cromosomi che producono segnali in violazione di questo vincolo sono dichiarati non validi e non entrano nella popolazione del GA. La motivazione è dichiarata in CAP-01: in assenza del vincolo, un fill al bordo opposto della banda potrebbe coincidere con il prezzo di stop, producendo un segnale eseguito e immediatamente stoppato nello stesso tick.

**`expiry`** — istante di scadenza del segnale, espresso al minuto chiuso. Vale il cap di validità ereditato da CAP-01, qui specificato semanticamente come applicabile alla **fase di vita post-esecuzione** del segnale: il timer di 2 giorni di trading decorre dal momento dell'esecuzione, ovvero dal raw touch della entry zone (Cap.7), non dal `timestamp_emission`. Il vincolo formale è

$$\texttt{expiry} - t_{exec} \leq 2\ \text{giorni di trading}$$

dove $t_{exec}$ è l'istante del raw touch e per "giorno di trading" si intende l'unione delle sessioni FIB 8:00-22:00 CET dei giorni di calendario in cui lo strumento è negoziato. Il motore genetico può ottimizzare il timing di chiusura entro questo tetto come parametro del cromosoma, ma non oltrepassarlo. La fase di attesa pre-esecuzione (dall'emissione al raw touch) non è governata da questo timer e resta materia del contratto di emissione di Cap.8.

**`setup_class`** — classificazione del setup, dominio $\{\text{directional}, \text{trade\_range}\}$. Definisce la natura strutturale del segnale e la regola di filtro di emissione che gli si applica. Per i setup di classe `directional` vale il filtro

$$|\texttt{target\_1} - p_{ref}| \geq 80\ \text{punti FIB}$$

ovvero la distanza del primo target dal prezzo di riferimento non può essere inferiore a 80 punti. Per i setup di classe `trade_range` vale il filtro alternativo

$$|\texttt{target\_1} - \texttt{stop\_loss}| \geq 80\ \text{punti FIB}$$

ovvero l'ampiezza del rettangolo di prezzo entro cui il setup opera non può essere inferiore a 80 punti. Il vincolo degli 80 punti è un filtro di emissione, non un parametro libero del motore genetico, ed è applicato a valle della valutazione del cromosoma in coerenza con il punto 4 della dichiarazione di intenti e con quanto stabilito in CAP-01.

### 6.2 Invariante di payload immutabile

Una volta emesso, il segnale identificato da `signal_id` non subisce alcuna modifica al proprio payload. La tupla $\mathcal{S}$ è congelata al momento dell'emissione: `entry_zone`, `target_1`, `target_2`, `stop_loss`, `expiry` e `setup_class` restano esattamente quelli pubblicati. Non esiste un'operazione di refresh o di edit del segnale che lasci invariato il `signal_id` e modifichi uno dei campi. L'invariante di payload immutabile è la condizione necessaria perché il segnale sia un oggetto contrattuale: l'operatore che lo riceve sul cellulare opera su quei valori e non su valori che possano mutare a sua insaputa fra il momento della lettura e il momento dell'invio dell'ordine al broker.

### 6.3 Regola di sostituzione e segnale unico attivo

Quando il motore valuta che le condizioni di mercato richiedono di rivedere il segnale corrente — perché il prezzo strutturale di riferimento è cambiato, perché i target strutturali sono stati ridefiniti dalla nuova geometria del prezzo, o perché il livello di stop non è più coerente con la struttura — esso non modifica il segnale esistente. Emette un nuovo segnale, contraddistinto da un nuovo `signal_id` univoco, con una propria tupla $\mathcal{S}'$ completa, indipendente dalla precedente. Contestualmente, il segnale precedente esce dall'insieme dei segnali attivi: viene revocato e transita nello stato terminale `revoked` (Cap.7), interrompendo qualsiasi prosecuzione del proprio lifecycle.

Sia $\mathcal{A}(t)$ l'insieme dei segnali attivi al tempo $t$. Vale il vincolo

$$|\mathcal{A}(t)| \leq 1\ \text{per ogni}\ t$$

ovvero a ogni istante è attivo al massimo un solo segnale. Questo vincolo recepisce contestualmente due decisioni dichiarate in CAP-01: il punto 7 della dichiarazione di intenti dell'operatore, che fissa l'operatività a 1 contratto alla volta e che il motore traduce in 1 segnale attivo alla volta; e il punto 6 della stessa dichiarazione, che prevede la revisione continua del segnale in funzione del prezzo strutturale corrente. La revisione, nell'architettura del contratto qui formalizzata, si manifesta come sostituzione: emissione di un nuovo `signal_id` con la nuova tupla congelata e revoca del precedente.

La regola di sostituzione produce due conseguenze operative rilevanti per il GA. La prima è che il GA ottimizza non soltanto la qualità del singolo segnale, ma anche la politica di sostituzione: emettere un nuovo segnale revocando il precedente comporta un costo (Cap.9 sul canale di pubblicazione, Cap.10 sulla tracciabilità del lifecycle) e il cromosoma deve giustificarlo con un miglioramento atteso. La seconda è che il vincolo di segnale unico attivo elimina dal dominio del GA tutte le politiche multi-segnale concorrente, riconducendo il problema a una sequenza di segnali singoli sostituiti, non a un portafoglio di segnali simultanei.

---

## Capitolo 7 — Stati del segnale e state machine

### 7.1 Stati e semantica

La state machine del segnale è costruita su un solo stato non-terminale e su sette stati terminali. Lo stato non-terminale è il seguente.

**`active`** — il segnale è stato emesso, la sua tupla $\mathcal{S}$ è pubblicata, e il segnale è in attesa di un evento che lo porti in uno stato terminale. Mentre il segnale è `active`, il motore osserva il prezzo corrente, calcola gli eventi di mercato pertinenti (raw touch della entry zone, raggiungimento di target o stop, scadenza, invalidazione strutturale, decisione di sostituzione) e applica le transizioni previste.

Gli stati terminali, in cui il segnale conclude il proprio ciclo di vita e non transita ulteriormente, sono i seguenti.

**`target_1_hit`** — dopo il raw touch della entry zone, il prezzo ha raggiunto `target_1` prima di raggiungere `stop_loss`, prima della scadenza `expiry` e prima di un'eventuale invalidazione strutturale.

**`target_2_hit`** — dopo il raggiungimento di `target_1`, il prezzo ha raggiunto anche `target_2` prima di raggiungere `stop_loss`, prima della scadenza e prima di un'eventuale invalidazione. Lo stato `target_2_hit` è terminale e succede sequenzialmente a `target_1_hit`: la transizione diretta da `active` a `target_2_hit` senza passaggio implicito da `target_1_hit` non è ammessa.

**`stopped`** — dopo il raw touch della entry zone, il prezzo ha raggiunto `stop_loss` prima di raggiungere `target_1`, prima della scadenza e prima di un'eventuale invalidazione.

**`invalidated`** — prima del raw touch della entry zone, si è verificata una condizione di invalidazione strutturale che rompe l'ipotesi del setup. La definizione formale e completa delle condizioni di invalidazione strutturale è demandata a Parte IV (Cap.15); fra le condizioni esplicitamente incluse nel contratto del segnale rientra il superamento del livello `stop_loss` da parte del prezzo, nella direzione contraria all'ipotesi del segnale, prima del raw touch: per i segnali long, $p(t) \leq \texttt{stop\_loss}$ con $t < t_{touch}$; simmetricamente per gli short. La motivazione è strutturale: un prezzo che, prima ancora che la zona di ingresso sia toccata, supera il livello di stop del setup, dimostra che l'ipotesi del segnale è stata smentita dal mercato e che la geometria del prezzo strutturale di riferimento è da rivedere.

**`missed_target`** — prima del raw touch della entry zone, il prezzo ha raggiunto `target_1`. Il segnale si conclude in stato `missed_target`: il target strutturale è stato realizzato dal mercato ma il setup non si è eseguito perché la zona di ingresso non è mai stata toccata. La metrica missed target rate definita in CAP-01 è riferita esplicitamente a `target_1` e non a `target_2`, in coerenza con la chiusura Q-03 di CAP-01 da parte del supervisore: l'asimmetria fra la sequenza `target_1_hit` → `target_2_hit` (entrambi tracciati come stati terminali distinti per il segnale eseguito) e `missed_target` (chiuso al solo target_1 per il segnale non eseguito) è una scelta esplicita e non una svista.

**`expired`** — sono trascorsi 2 giorni di trading dal raw touch della entry zone (Cap.6.1) senza che il segnale sia transitato in alcuno degli altri stati terminali. A $t = \texttt{expiry}$ il segnale, se ancora `active`, transita in `expired`.

**`revoked`** — il segnale è stato superseduto dall'emissione di un nuovo `signal_id`, secondo la regola di sostituzione di Cap.6.3. La revoca avviene contestualmente all'emissione del nuovo segnale e interrompe il lifecycle del precedente, indipendentemente dal fatto che il raw touch fosse o non fosse già avvenuto.

### 7.2 Transizioni ammesse

L'insieme delle transizioni ammesse dalla state machine, denotate $s \to s'$, è il seguente.

| Da | A | Condizione |
|----|---|------------|
| (creazione) | `active` | Emissione del segnale, generazione del `signal_id`, scrittura del log di emissione |
| `active` | `target_1_hit` | Dopo raw touch della entry zone, il prezzo raggiunge `target_1` (sequenza richiesta: raw touch $\to$ target_1) |
| `target_1_hit`* | `target_2_hit` | Dopo `target_1_hit`, il prezzo raggiunge `target_2` senza prima toccare `stop_loss`, senza scadere e senza invalidazione |
| `active` | `stopped` | Dopo raw touch della entry zone, il prezzo raggiunge `stop_loss` senza prima raggiungere `target_1` |
| `active` | `invalidated` | Prima del raw touch, si verifica una condizione di invalidazione strutturale (Parte IV, Cap.15); fra cui esplicitamente $p(t) \leq \texttt{stop\_loss}$ per i long e $p(t) \geq \texttt{stop\_loss}$ per gli short |
| `active` | `missed_target` | Prima del raw touch, il prezzo raggiunge `target_1` |
| `active` | `expired` | A $t = \texttt{expiry}$ il segnale è ancora in `active` (timer decorrente dal raw touch) |
| `active` | `revoked` | Il motore emette un nuovo `signal_id` (sostituzione, Cap.6.3) |

\* `target_1_hit`, sebbene terminale come stato del segnale per la finalità del log di chiusura, ammette in via eccezionale la sola transizione successiva a `target_2_hit` per registrare l'eventuale raggiungimento del secondo target. Nessun'altra transizione esce da `target_1_hit`. Una volta entrato in `target_2_hit`, `stopped`, `invalidated`, `missed_target`, `expired` o `revoked`, il segnale è definitivamente concluso.

### 7.3 Raw touch ed esecuzione: un evento, non uno stato

Si definisce raw touch della entry zone del segnale $\mathcal{S}$ l'evento in cui il prezzo del FIB, osservato dal motore sulla barra 1-min chiusa, assume per la prima volta dopo l'emissione un valore appartenente all'insieme discreto $\texttt{entry\_zone} = \{p_{ref}-b, p_{ref}-b+5, \ldots, p_{ref}+b\}$. La definizione non impone alcun vincolo di direzione di provenienza del prezzo: la prima barra 1-min successiva all'emissione il cui high-low intervallo contenga almeno uno dei livelli discreti della zona produce il raw touch. Per i segnali long il livello operativamente atteso dall'operatore è tipicamente il bordo inferiore $p_{ref} - b$; per gli short il bordo superiore $p_{ref} + b$. Ma il contratto del segnale registra il raw touch indipendentemente da quale dei livelli discreti della zona è stato toccato per primo.

Al raw touch, il motore produce un evento, denotato `trigger_event`, che viene notificato all'operatore sul canale Telegram (Cap.9) con riferimento al `signal_id` del segnale corrente. **Il raw touch è sempre eseguibile**: non esistono nel contratto del segnale guardie o filtri post-emissione che blocchino il trigger una volta che il prezzo è entrato nella zona. La decisione di emettere o non emettere il segnale è già stata presa dal motore prima dell'emissione, sulla base delle condizioni di emissione di Cap.8. Una volta emesso il segnale, il raw touch è l'evento di esecuzione, senza ulteriori filtri.

Il `trigger_event` non è uno stato della state machine: il segnale resta in `active` finché un evento successivo (raggiungimento di `target_1` o `stop_loss`, invalidazione, scadenza, revoca) non lo porta in uno stato terminale. La distinzione "executable / executed", presente nella formulazione preliminare dell'indice del documento, non viene introdotta nel contratto del segnale. La motivazione è strutturale, non cosmetica: in real-time il motore non osserva il fill manuale dell'operatore, in quanto il motore non esegue ordini (vincolo del punto 1 della dichiarazione di intenti, ereditato da CAP-01) e l'operatore agisce manualmente dal cellulare sull'interfaccia del broker Directa. Uno stato `executed` distinto da `active` richiederebbe che il motore ricevesse conferma del fill dal broker, cosa che non rientra nel perimetro del sistema. Mantenere `active` come unico stato non-terminale, e degradare il trigger a evento notificato, è quindi una scelta di aderenza al perimetro operativo.

In simulazione di backtest il `trigger_event` viene trattato come fill virtuale a un prezzo determinato deterministicamente dalla regola di simulazione. La regola di riferimento è il fill al primo livello discreto della zona toccato dalla barra 1-min in cui si verifica il raw touch; il dettaglio operativo della regola di simulazione è specificato in Parte III. La regola di simulazione non altera la state machine pubblica del segnale e in backtest come in forward-run il segnale resta `active` fra il `trigger_event` e l'eventuale evento terminale successivo.

### 7.4 Timer di scadenza post-esecuzione

Il cap di validità di 2 giorni di trading è implementato come timer concreto associato al singolo segnale e decorre dal raw touch. All'emissione, il motore fissa nel payload il parametro

$$\Delta t_{cromosoma} \in \{1, 2, \ldots, 1680\}\ \text{minuti di trading}$$

espresso come intero in minuti della sessione di trading. La cardinalità 1680 corrisponde a $2 \times 840$ minuti, ovvero a due sessioni complete 8:00-22:00 CET. $\Delta t_{cromosoma}$ è parametro libero del cromosoma del GA. Al verificarsi del raw touch a istante $t_{exec}$, il motore calcola

$$\texttt{expiry} = t_{exec} + \Delta t_{cromosoma}\ \text{minuti di trading}$$

dove la somma è valutata sul calendario di trading dello strumento, non sul calendario solare. Il counter $\Delta t_{cromosoma}$ avanza esclusivamente nei minuti compresi nella finestra 8:00-22:00 CET dei giorni di trading e si arresta nelle interruzioni notturne (22:00-8:00 del giorno successivo), nei weekend e nei festivi di mercato. Esempio: per un raw touch a $t_{exec}$ = lunedì 21:55 CET con $\Delta t_{cromosoma} = 1680$, il counter consuma 5 minuti il lunedì (21:55 → 22:00), riparte alle 8:00 del martedì, consuma 840 minuti martedì (8:00 → 22:00), riparte mercoledì alle 8:00, consuma i restanti 835 minuti (8:00 → 21:55). L'expiry è quindi mercoledì 21:55 CET.

Il timer è valutato dal motore ad ogni barra 1-min: appena $t \geq \texttt{expiry}$ e il segnale è ancora `active`, viene emesso l'evento di scadenza e il segnale transita in `expired`. L'implementazione del timer come barra 1-min anziché come tick è coerente con la granularità del modello di inference, e garantisce che il valore $\texttt{expiry}$ pubblicato sia rispettato a meno della risoluzione di un minuto.

Cromosomi che producono valori di $\Delta t_{cromosoma}$ fuori dal dominio $\{1, \ldots, 1680\}$ sono dichiarati non validi e non entrano nella popolazione del GA.

### 7.5 Identificazione real-time del primo pivot strutturale post-apertura (M-1)

In CAP-01 (Review v3 carryover, M-1 in Review v4) è stato segnalato che il primo pivot strutturale post-apertura, usato come ancora del target di sessione 70% e del prezzo strutturale di riferimento per i segnali emessi nella prima parte della finestra di negoziazione, va trattato a livello di interfaccia in Parte II. L'algoritmo concreto di pivot detection è materia di Parte III (Cap.14, feature engineering causale); in Parte II si fissa il contratto di osservazione real-time del motore.

Il motore osserva la sequenza delle barre 1-min a partire dall'apertura della sessione alle 8:00 CET. A ciascuna barra chiusa il motore valuta se la barra appena conclusa costituisce, in retrospettiva sulla sequenza disponibile, un candidato pivot strutturale (minimo o massimo). La regola di confermabilità del pivot è demandata a Parte III, ma in Parte II vale come vincolo del contratto che il primo pivot strutturale post-apertura deve essere disponibile, in fase di calibrazione del motore, entro un numero massimo di barre 1-min dall'apertura della sessione. Il valore numerico del tetto $N_{pivot}$ non è fissato in Parte II e nemmeno in valore provvisorio: la sua quantificazione richiede misura empirica sullo storico FIB 1-min e viene congelata in Parte V sulla base della regola di pivot detection scelta in Parte III. Il vincolo metodologico, tuttavia, è dichiarato qui: la regola di pivot detection scelta in Parte III non può produrre un primo candidato di sessione con latenza tale da rendere di fatto inattiva la finestra iniziale di sessione, vanificando l'ancoraggio del target 70% al primo pivot post-apertura deciso dal supervisore in CAP-01 (chiusura Q-02).

La cadenza di valutazione della regola di pivot è la stessa cadenza di inference del motore, ovvero la barra 1-min chiusa. Il motore non opera su tick intra-bar per la pivot detection.

---

## Capitolo 8 — Condizioni di emissione del segnale

### 8.1 Filosofia del contratto di emissione

Il motore decide se emettere un segnale **prima** dell'emissione, sulla base di condizioni di mercato osservate al momento della valutazione. Una volta emesso il segnale, il contratto è semplice: il raw touch della entry zone è sempre eseguibile e produce il `trigger_event` (Cap.7.3). Non esistono nel contratto guardie o filtri post-emissione che blocchino il trigger.

La motivazione di questa architettura è triplice. **Primo**, è coerente con il punto 1 della dichiarazione di intenti dell'operatore: il motore emette segnali, l'esecuzione è dell'operatore. Un meccanismo di filtri post-emissione che bloccasse il trigger introdurrebbe una decisione di esecuzione mascherata da decisione di segnale. **Secondo**, le condizioni di emissione devono essere addestrabili sul GA, ovvero calcolabili sulla serie storica del FIB disponibile per il training. Lo storico Portara/CQG FIB 1-min copre OHLC e volume; non copre lo spread bid-ask né la profondità del book, che richiederebbero acquisti aggiuntivi di dati storici esplicitamente esclusi dall'infrastruttura definita in CAP-01. **Terzo**, una volta che il segnale è stato emesso e l'operatore ha ricevuto il payload, l'operatore stesso valuta in tempo reale sul broker le condizioni di esecuzione visibili a lui (spread istantaneo, profondità del book, candela in corso) e decide se entrare manualmente. Un filtro automatico aggiuntivo sul broker sarebbe ridondante con la sua valutazione e contraddirebbe l'autonomia di esecuzione.

Le condizioni di emissione qui formalizzate sono pertanto calcolabili dal motore in real-time esclusivamente sulla base di grandezze derivabili dalle barre 1-min del feed Directa, omogenee con le grandezze disponibili nello storico Portara/CQG per il training del GA. Nessuna condizione richiede dati che non siano nella serie storica già pianificata per il training in CAP-01.

### 8.2 Le tre condizioni di emissione

**Condizione di volatilità.** Il range della barra 1-min al momento della valutazione di emissione, definito come differenza fra prezzo massimo e prezzo minimo della barra appena chiusa, deve essere inferiore o uguale a una soglia $\tau_{vol}$ derivata dal modello di volatilità condizionata. Sia $r_{1m}(t)$ il range della barra 1-min al tempo $t$. La condizione è soddisfatta se

$$r_{1m}(t_{emission}) \leq \tau_{vol}\big(\hat{\sigma}(t_{emission})\big)$$

dove $\hat{\sigma}(t_{emission})$ è la stima di volatilità condizionata fornita dal modello EGARCH al tempo dell'emissione (Parte III, Cap.12) e $\tau_{vol}(\cdot)$ è una funzione di soglia parametrizzata dal cromosoma del GA. Il senso operativo della condizione è impedire al motore di emettere segnali in barre di volatilità anomala, in cui il prezzo strutturale di riferimento è instabile e il payload del segnale rischia di essere immediatamente superseduto dalla regola di sostituzione. La forma esplicita di $\tau_{vol}$ e i parametri del modello EGARCH che la alimentano sono in Parte III.

**Condizione di liquidità.** Il volume della barra 1-min al momento della valutazione di emissione deve essere superiore o uguale a una soglia $\tau_{liq}$. Sia $v_{1m}(t)$ il volume contrattato sulla barra 1-min al tempo $t$. La condizione è soddisfatta se

$$v_{1m}(t_{emission}) \geq \tau_{liq}$$

Il senso operativo della condizione è impedire al motore di emettere segnali quando il mercato è anomalmente sottile, in quanto in tali condizioni il prezzo strutturale di riferimento può essere il risultato di poche operazioni non rappresentative e la regola di sostituzione è esposta a movimenti spuri. La soglia $\tau_{liq}$ è parametro libero del cromosoma, congelato in Parte V. La grandezza è disponibile sia nel feed real-time Directa sia nello storico Portara/CQG.

**Condizione di distanza dal target_1.** La distanza, espressa in punti FIB e nella direzione coerente con `direction`, fra il prezzo strutturale di riferimento del segnale candidato e il target_1 strutturale candidato, deve essere superiore o uguale a una soglia $\tau_{dist}$ vincolata inferiormente dal filtro di emissione di CAP-01 ($\geq 80$ punti per i setup directional). Per i segnali long:

$$\texttt{target\_1} - p_{ref} \geq \max(\tau_{dist},\ 80)$$

per i segnali short la condizione è simmetrica:

$$p_{ref} - \texttt{target\_1} \geq \max(\tau_{dist},\ 80)$$

Il senso operativo della condizione è impedire al motore di emettere segnali in cui il payoff strutturale atteso, misurato come spazio fra $p_{ref}$ e target_1, non giustifica il rischio di stop espresso da $d_{stop}$. La soglia $\tau_{dist}$ è parametro libero del cromosoma con vincolo inferiore di 80 punti FIB (filtro di emissione CAP-01); il cromosoma può sceglierla più stringente, mai più lassista.

### 8.3 Regola di emissione

L'emissione del segnale $\mathcal{S}$ avviene se e solo se al tempo $t_{emission}$ valgono simultaneamente le tre condizioni di emissione. Sia $E_{vol}(t)$, $E_{liq}(t)$, $E_{dist}(t)$ il valore logico delle tre condizioni al tempo $t$; il motore emette il segnale se e solo se al tempo di valutazione vale

$$E_{vol}(t_{emission}) \land E_{liq}(t_{emission}) \land E_{dist}(t_{emission}) = \text{vero}$$

Se almeno una delle tre condizioni non è soddisfatta, il segnale candidato non viene emesso: nessun `signal_id` viene generato, nessuna pubblicazione Telegram avviene, nessun log di emissione viene scritto. Il motore continua a valutare le condizioni alle barre 1-min successive.

Le soglie $\tau_{vol}(\cdot)$, $\tau_{liq}$, $\tau_{dist}$ sono parametri liberi del cromosoma del GA, ottimizzati dal motore genetico e congelati in Parte V. Le formule del modello di volatilità che alimentano $\tau_{vol}(\cdot)$ sono in Parte III, Cap.12.

### 8.4 Assenza di filtri post-emissione e di fasi speciali nella sessione 8:00-22:00 CET

Una volta che il motore ha emesso il segnale, il raw touch della entry zone è sempre eseguibile (Cap.7.3): non esistono nel contratto guardie o filtri ulteriori che blocchino il `trigger_event`. Eventuali condizioni patologiche di mercato al momento del raw touch (es. spread istantaneo allargato sul broker, candela in corso violenta) sono valutate in autonomia dall'operatore manuale prima dell'invio dell'ordine; non sono filtrate dal motore.

Le condizioni di emissione di Cap.8.2 si applicano uniformemente lungo l'intera finestra 8:00-22:00 CET. Non si introducono fasi speciali (apertura, regolare, after-hours, asta) né soglie differenziate per fascia oraria. Questa scelta recepisce il chiarimento del supervisore che ha ritirato l'osservazione M-3 di Review v4 di CAP-01 (presunta fase d'asta 8:00-9:00) confermando che il FIB negozia in modo continuo nell'intera finestra 8:00-22:00.

---

## Capitolo 9 — Politica di pubblicazione su Telegram

### 9.1 Contesto del canale e vincolo operativo

Il canale di pubblicazione dei segnali è un bot Telegram personale dell'operatore, già attivo, come dichiarato in CAP-01. L'operatore opera da cellulare durante l'orario di lavoro presso l'istituto bancario di appartenenza, in modo discontinuo, e legge il segnale sul cellulare prima di inviare manualmente l'ordine al broker Directa. Il formato del messaggio deve essere progettato per la lettura mobile in condizioni di attenzione limitata, e il canale deve garantire una latenza di consegna compatibile con l'urgenza operativa del segnale.

Il dettaglio tecnico del setup del bot, della gestione del `chat_id` e delle stringhe esatte del messaggio è rinviato all'Appendice E. In Parte II si fissano il contratto informativo del messaggio (quali campi del payload del segnale sono pubblicati e in quale ordine), il vincolo di latenza, la politica anti-duplicato, la regola di emissione di messaggi nuovi per segnali nuovi, e la gestione di errori di pubblicazione.

### 9.2 Contratto informativo del messaggio

Il messaggio Telegram pubblicato in corrispondenza dell'emissione di un segnale $\mathcal{S}$ contiene, in ordine obbligatorio, i seguenti campi del payload, presentati in forma leggibile da operatore mobile:

1. `signal_id` — l'identificatore del segnale, riportato in chiaro come chiave operativa per qualunque comunicazione successiva
2. `direction` — direzione long o short, evidenziata in modo immediato
3. `setup_class` — directional o trade_range, per distinguere il senso del filtro 80 punti applicato
4. `entry_zone` — banda di prezzo discreta $\{p_{ref}-b, \ldots, p_{ref}+b\}$, esplicitata come intervallo $[p_{ref}-b, p_{ref}+b]$ in punti FIB
5. `target_1` e `target_2` — i due target strutturali, distinti e ordinati
6. `stop_loss` — il prezzo strutturale di stop
7. `timestamp_emission` — l'istante di emissione, riportato come data e ora CET

Il campo `expiry` non è fissato al momento dell'emissione (decorre dal raw touch, Cap.6.1 e Cap.7.4) e quindi non figura nel messaggio iniziale; la sua eventuale comunicazione all'operatore al verificarsi del raw touch è materia della politica di notifica del `trigger_event` (vedi 9.5).

Il messaggio non contiene parametri tecnici del modello (volatilità stimata, valore delle condizioni di emissione al momento dell'emissione, stato del regime), che restano nel log interno (Cap.10) e non sono rilevanti per l'operatore. Il messaggio non contiene istruzioni di gestione attiva della posizione (incrementi, scaling out, take profit anticipato, stop profit), in coerenza con il punto 8 della dichiarazione di intenti che riserva queste decisioni all'operatore.

### 9.3 Latenza di consegna

Si definisce latenza di consegna del segnale, $L$, l'intervallo di tempo tra l'istante in cui il motore conclude la valutazione dell'emissione (`timestamp_emission`) e l'istante in cui il messaggio è ricevuto sul cellulare dell'operatore. Vale il vincolo

$$L \leq L_{max}$$

dove $L_{max}$ è la latenza massima ammissibile, congelata in Parte V. Il valore di lavoro provvisorio è $L_{max} = 30$ secondi: oltre questa soglia, il segnale perde valore informativo perché il prezzo strutturale di riferimento può essersi spostato in modo non trascurabile rispetto al momento dell'emissione. La verifica empirica della latenza effettiva del canale Telegram (API Bot, instradamento, tempo di consegna push al cellulare in copertura mobile italiana) e la definizione operativa del valore congelato sono materia di Appendice E.

### 9.4 Politica anti-duplicato

Il motore pubblica ciascun `signal_id` una sola volta. La regola è formalizzata come segue: sia $\mathcal{P}$ l'insieme dei `signal_id` per cui il motore ha già pubblicato un messaggio Telegram con successo; per ogni nuovo segnale $\mathcal{S}$ con identificatore `signal_id`, il motore pubblica il messaggio se e solo se `signal_id` $\notin \mathcal{P}$, e contestualmente aggiunge `signal_id` a $\mathcal{P}$. L'insieme $\mathcal{P}$ è persistito su disco insieme al log di emissione (Cap.10), in modo che restart del motore non comportino ripubblicazione di segnali già notificati.

### 9.5 Nuovo segnale come messaggio separato; notifica del trigger_event

Quando il motore emette un nuovo segnale $\mathcal{S}'$ in sostituzione di un segnale precedente $\mathcal{S}$, secondo la regola di sostituzione di Cap.6.3, il messaggio Telegram corrispondente a $\mathcal{S}'$ è pubblicato come messaggio separato, con il proprio `signal_id` distinto. Non viene effettuata alcuna operazione di modifica o di edit sul messaggio Telegram precedente. Il messaggio del segnale revocato resta visibile nella cronologia della chat come traccia storica, ma non rappresenta più un segnale attivo: lo stato `revoked` è registrato nel log interno (Cap.10) e implicito nel fatto che un nuovo messaggio con nuovo `signal_id` è stato pubblicato successivamente.

La scelta di emettere messaggi separati anziché editare il messaggio esistente è coerente con l'invariante di payload immutabile di Cap.6.2: editare il messaggio del segnale precedente equivarrebbe a modificare il suo payload pubblicato, violando la regola.

Al verificarsi del `trigger_event` (raw touch della entry zone) il motore pubblica una notifica separata sul canale Telegram, che fa riferimento al `signal_id` del segnale corrente e all'istante $t_{exec}$ del raw touch. La notifica del `trigger_event` è funzionalmente distinta dal messaggio di emissione: l'emissione comunica all'operatore l'esistenza del segnale e i suoi parametri, la notifica del trigger gli comunica che il prezzo è entrato nella zona e che il segnale è eseguibile. Il dettaglio del contratto informativo della notifica del trigger è in Appendice E; in Parte II si fissa il vincolo che essa sia pubblicata, come messaggio separato e non come edit, contestualmente al riconoscimento del raw touch da parte del motore.

### 9.6 Gestione degli errori di pubblicazione

In caso di errore nella chiamata all'API Telegram (timeout, errori di rete, indisponibilità temporanea del servizio), il motore applica una politica di retry. La politica prevede:

- numero massimo di tentativi $n_{retry}$, valore di lavoro provvisorio $n_{retry} = 3$
- backoff esponenziale fra i tentativi, con base provvisoria $\Delta t_{retry} = 2$ secondi raddoppiata a ogni tentativo
- in caso di fallimento finale (tutti i tentativi esauriti), registrazione dell'errore nel log di emissione e nessuna ulteriore pubblicazione; il `signal_id` non viene aggiunto a $\mathcal{P}$ e il segnale è registrato come non pubblicato

L'opzione di considerare un segnale non pubblicato come automaticamente revocato è una scelta di policy demandata a Parte VI (Cap.27); in Parte II si fissa il vincolo che il fallimento di pubblicazione sia tracciato nel log e non rimanga implicito. I parametri $n_{retry}$, $\Delta t_{retry}$ e $L_{max}$ sono congelati in Parte V; le specifiche di interazione con l'API Telegram sono in Appendice E.

---

## Capitolo 10 — Replay e riproducibilità del lifecycle

### 10.1 Obiettivo del log e requisito di determinismo

Il log del lifecycle del segnale deve consentire di ricostruire, a partire dallo storico delle barre 1-min del FIB e da quello dei feed ausiliari utilizzati dal motore (contesto cross-index, volumi), l'esatta sequenza degli stati attraversati da ogni segnale emesso, con i timestamp e i prezzi che hanno innescato ciascuna transizione. Il requisito è formalizzato come vincolo, non come obiettivo desiderabile.

**Requisito di determinismo.** Dato lo stesso storico delle barre 1-min e dei feed ausiliari e lo stesso bundle frozen (cromosoma con parametri congelati e versione del codice congelata), il replay del motore deve produrre esattamente la stessa sequenza di emissioni, di `signal_id`, di transizioni di stato, e degli stessi timestamp di transizione. Vale

$$\forall\ \text{storico}\ H,\ \forall\ \text{bundle}\ B:\quad \texttt{replay}(H, B) = \texttt{replay}(H, B)\ \text{(bit-exact)}$$

dove $\texttt{replay}(\cdot,\cdot)$ è la funzione di replay del motore. Nessuna sorgente di non-determinismo è introdotta dal motore: in particolare, non si utilizzano generatori pseudo-casuali non seedati, e qualsiasi componente che richieda inizializzazione casuale (es. inizializzazioni del modello EGARCH, jitter di latenza simulato per test) deve essere seedata e il seed deve essere parte del bundle congelato.

Il determinismo del replay è la condizione necessaria perché le metriche di lifecycle calcolate sul replay OOS (CAP-01, Cap.5) abbiano valore probatorio: una metrica calcolata su un replay non riproducibile non è verificabile e non può essere usata come gate decisionale per il go-live (Parte VII, Cap.35).

### 10.2 Log di emissione

In corrispondenza di ogni emissione di un nuovo segnale, il motore scrive un log di emissione contenente:

- l'intero payload del segnale $\mathcal{S}$ (gli otto campi di Cap.6.1, fissati al momento dell'emissione)
- lo snapshot delle condizioni di emissione al momento $t_{emission}$: valori di $r_{1m}$, $v_{1m}$ e distanza $|\texttt{target\_1} - p_{ref}|$, con le soglie correnti $\tau_{vol}(\hat{\sigma}(t_{emission}))$, $\tau_{liq}$, $\tau_{dist}$ in vigore al momento (cromosoma frozen del bundle)
- lo snapshot delle feature del modello al momento dell'emissione: $\hat{\sigma}(t_{emission})$, classificazione di regime (calmo o turbolento, secondo Parte III Cap.13), valore corrente delle feature causali utilizzate dal cromosoma per la decisione di emissione
- il `signal_id` dell'eventuale segnale precedente revocato per sostituzione, se l'emissione è una sostituzione (Cap.6.3)
- esito della pubblicazione Telegram: successo o fallimento, numero di tentativi, eventuale codice di errore (Cap.9.6)

Il log di emissione è scritto in formato strutturato, idoneo a essere consumato sia dal modulo di replay sia dagli strumenti di analisi delle metriche OOS. Il formato esatto (campi, tipi, schema, modalità di persistenza) è definito in Appendice B; in Parte II si fissa l'elenco delle informazioni che il log deve contenere.

### 10.3 Log delle transizioni di stato

Per ogni transizione di stato registrata dalla state machine di Cap.7, il motore scrive una riga di log con:

- `signal_id` del segnale interessato
- timestamp della transizione (al minuto chiuso, coerente con la granularità del modello)
- stato precedente e stato nuovo (uno dei valori ammessi di Cap.7.1)
- prezzo che ha innescato la transizione, quando applicabile (prezzo di raw touch per `trigger_event`, prezzo di `target_1` per la transizione a `target_1_hit`, prezzo di `stop_loss` per la transizione a `stopped` o `invalidated` per stop attraversato pre-touch, e così via)
- in caso di transizione causata da una condizione non riducibile a un singolo prezzo (es. `invalidated` per condizioni strutturali diverse dal superamento di stop, `revoked`), una descrizione strutturata della causa coerente con la regola di transizione di Cap.7.2

Il `trigger_event` di Cap.7.3 viene registrato nel log delle transizioni come evento associato al segnale, con la nota esplicita che non è una transizione di stato (il segnale resta in `active`) ma un evento notificato sul canale Telegram; la registrazione nel log assicura che il replay possa ricostruire l'istante esatto in cui l'evento di esecuzione è stato notificato all'operatore e, in particolare, l'istante $t_{exec}$ da cui decorre il timer expiry (Cap.7.4).

### 10.4 Log di chiusura

Quando il segnale entra in uno stato terminale (Cap.7.1), il motore scrive un log di chiusura contenente:

- `signal_id`
- stato terminale finale
- timestamp di chiusura
- statistiche aggregate del segnale: rendimento lordo realizzato in punti FIB (se il segnale è stato eseguito, ovvero ha generato un `trigger_event`); MAE (maximum adverse excursion) e MFE (maximum favourable excursion) misurate dal momento del `trigger_event` al momento della chiusura; durata totale del lifecycle in minuti di trading dal `timestamp_emission` alla chiusura; durata della fase post-trigger in minuti di trading da $t_{exec}$ alla chiusura

Il rendimento netto per segnale eseguito è derivato dal rendimento lordo applicando la formula di CAP-01 (Cap.5): $E[R_{net}\mid executed] = E[R_{gross}\mid executed] - 2 \cdot c$ con $c = 1$ punto FIB equivalente per operazione. Il calcolo del rendimento netto non è registrato nel log di chiusura come campo aggiuntivo, in quanto derivabile deterministicamente dal lordo: il valore probatorio della grandezza è preservato dal determinismo del replay.

### 10.5 Granularità temporale e fonte del prezzo

I timestamp riportati nei log di emissione, transizione e chiusura sono espressi al minuto chiuso e si riferiscono al fuso CET, coerente con la sessione FIB 8:00-22:00 CET ereditata da CAP-01. La fonte dei prezzi utilizzati per valutare le transizioni di stato è la barra 1-min consolidata del FIB; per la sessione live, la barra è prodotta dal motore consolidando il feed real-time di Directa DAPI (porta 10001), secondo la specifica dell'Appendice C. In backtest, la barra è quella dello storico Portara/CQG (Appendice D). La consistenza fra la barra real-time consolidata in produzione e la barra storica usata in backtest è un requisito di qualità dei dati che il motore verifica all'ingresso (Parte III, Cap.11) e non un parametro del modello.

### 10.6 Persistenza e versionamento del log

I tre log (emissione, transizioni, chiusura) sono persistiti in modo che il replay possa essere ricostruito anche dopo un restart del motore o un cambio di macchina di esecuzione. La persistenza è ortogonale alla persistenza dell'insieme $\mathcal{P}$ dei `signal_id` pubblicati (Cap.9.4): le due strutture sono coerenti per costruzione, in quanto il log di emissione contiene già l'esito della pubblicazione Telegram. Il versionamento del bundle frozen utilizzato per generare ciascuna emissione è registrato nel log di emissione: ogni transizione e ogni chiusura sono pertanto associabili al cromosoma e alla versione di codice che le hanno prodotte. Il dettaglio del meccanismo di versionamento del bundle frozen è in Parte VII (Cap.34).
