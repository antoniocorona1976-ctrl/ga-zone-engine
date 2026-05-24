# Parte IV — Geometria delle zone di entry, target strutturali, stop strutturali e modello di survival

La Parte IV formalizza il ponte tra i blocchi quantitativi della Parte III e il cromosoma della Parte V. Essa risponde a quattro domande distinte e interdipendenti: come si costruisce geometricamente la zona di entry attorno a un livello strutturale (Cap.16); come si selezionano target_1 e target_2 dalla geometria dei pivot confermati (Cap.17); come si determina lo stop strutturale garantendo la validità geometrica del cromosoma (Cap.18); come si stima la probabilità condizionata di raggiungere target_1 prima dello stop, e come tale stima filtra l'emissione (Cap.19–20). Il Cap.21 tratta il caso trade_range, che differisce dal caso directional nella geometria della zona, nella regola di filtro 80 punti e nella classificazione del setup.

La Parte IV non contiene il cromosoma, gli operatori GA, la fitness multi-obiettivo (Parte V), né il walk-forward, DSR e PBO (Parti V e VII). Non contiene il congelamento definitivo di alcun parametro: ogni valore numerico proposto in questa Parte è dichiarato come provvisorio e rinviato al congelamento empirico in Parte V sulla base dello storico Portara/CQG FIB 1-min, in coerenza con la policy stabilita in CAP-01 (Q-03).

I blocchi quantitativi consumati come input da questa Parte sono: la stima $\hat{\sigma}_{\text{pt}}(t) = \hat{\sigma}(t) \cdot p_t$ in punti FIB (Cap.13.1 di Parte III); la classificazione di regime $R_t \in \{\text{calmo}, \text{turbolento}\}$ (Cap.14 di Parte III); il catalogo delle 37 feature causali normalizzate $\tilde{\mathbf{x}}_t$ (Cap.15 di Parte III); l'algoritmo di pivot detection con $n_c = 3$ e $\delta_{pivot} = 10$ pt provvisori, con disponibilità del pivot confermato dalla barra $t + n_c + 1$ (Cap.15.3 di Parte III). Il contratto del segnale consumato come input è: payload $\mathcal{S}$ con $p_{ref}$, entry_zone, target_1, target_2, stop_loss, setup_class, $\Delta t_{cromosoma}$, $T_{touch}^{max}$ (Cap.6 di Parte II); state machine con 1 stato non-terminale e 6 terminali (Cap.7 di Parte II); condizioni di emissione $E_{vol}$, $E_{liq}$, $E_{dist}^{\sigma}$ (Cap.8 di Parte II); fill virtuale worst-case (Cap.12.4 di Parte III); position lifecycle distinto (Cap.11 di Parte II).

Il tick size del FIB è 5 punti: tutti i livelli strutturali — $p_{ref}$, bordi della zona, target_1, target_2, stop_loss — sono multipli di 5. Questa proprietà discreta è non negoziabile e si applica a ogni formula, esempio numerico e regola algoritmica della Parte IV.

---

## Capitolo 16 — Definizione delle zone di entry

### 16.1 Ancoraggio strutturale e prezzo di riferimento

La zona di entry è una banda di prezzo discreta costruita attorno a un **prezzo strutturale di riferimento** $p_{ref}$, derivato dall'ultimo pivot strutturale confermato nella sessione corrente. La motivazione dell'ancoraggio al pivot è duplice: il pivot confermato costituisce il livello di prezzo più recente in cui il mercato ha invertito la direzione, rendendolo una zona di attesa strutturalmente plausibile per un nuovo punto di ingresso; il pivot è prodotto dall'algoritmo di Cap.15.3 di Parte III in modo deterministico e causale, con disponibilità garantita dalla barra $t + n_c + 1$.

**Algoritmo di selezione di $p_{ref}$.** Sia $\mathcal{P}_{high}(t)$ l'insieme dei pivot high confermati nella sessione corrente e disponibili come feature alla barra $t$, e $\mathcal{P}_{low}(t)$ l'insieme dei pivot low confermati e disponibili. I due insiemi sono aggiornati a ogni barra secondo l'algoritmo di Cap.15.3 di Parte III. Si denoti con $\tau_{conf}(p)$ il timestamp di conferma del pivot $p$, ovvero la barra $t_p + n_c$ alla cui chiusura il pivot rilevato a $t_p$ è stato confermato dall'algoritmo frattale di Cap.15.3 di Parte III; la disponibilità del pivot $p$ come feature inizia dalla barra $\tau_{conf}(p) + 1$. Il prezzo di riferimento $p_{ref}$ per il segnale emesso alla barra $t$ è il **livello del pivot più recente per timestamp di conferma** nella direzione del segnale:

- **Segnale long**: $p_{ref}(t) = \mathrm{level}\!\Big( \arg\max_{p \in \mathcal{P}_{low}(t)} \tau_{conf}(p) \Big)$, ovvero il livello del pivot low il cui timestamp di conferma è il più recente nella sessione corrente. Il segnale long anticipa un'inversione dal basso: la zona di entry è costruita attorno all'ultimo minimo strutturale confermato in ordine cronologico di conferma.
- **Segnale short**: $p_{ref}(t) = \mathrm{level}\!\Big( \arg\min_{p \in \mathcal{P}_{high}(t)} \big(-\tau_{conf}(p)\big) \Big) = \mathrm{level}\!\Big( \arg\max_{p \in \mathcal{P}_{high}(t)} \tau_{conf}(p) \Big)$, ovvero il livello del pivot high il cui timestamp di conferma è il più recente nella sessione corrente. Il segnale short anticipa un'inversione dall'alto: la zona di entry è costruita attorno all'ultimo massimo strutturale confermato in ordine cronologico di conferma.

Il livello $p_{ref}$ è sempre un multiplo di 5 punti FIB, poiché i pivot sono prezzi OHLC del FIB e il tick size è 5 punti.

**Razionale del criterio temporale.** Il criterio del pivot più recente per timestamp di conferma — anziché del pivot estremo in prezzo entro l'insieme — è motivato dalla maggiore reattività al regime corrente: il pivot più recente è il livello strutturale più vicino al momento decisionale e riflette la struttura di mercato attualmente vigente, mentre un pivot estremo in prezzo può essere stato confermato molte barre prima e non rispecchiare più la dinamica corrente. In presenza di più pivot low (o high) confermati nella sessione, il pivot estremo in prezzo (massimo dei minimi per long, minimo dei massimi per short) e il pivot più recente in tempo possono differire: il documento adotta il criterio temporale come **unico criterio**, in modo che formula e testo coincidano sotto ogni implementazione conforme.

**Determinismo della selezione.** L'algoritmo frattale di Cap.15.3 di Parte III conferma un pivot per volta alla chiusura di ogni barra $t_p + n_c$, dunque due pivot dello stesso tipo non possono avere lo stesso timestamp di conferma per costruzione: $\arg\max_{p \in \mathcal{P}_{low}(t)} \tau_{conf}(p)$ ammette soluzione unica per ogni $t$, e l'algoritmo di selezione di $p_{ref}$ è deterministico bit-exact senza necessità di regole di tie-break.

Esempio numerico (tick FIB = 5 pt). Sessione corrente con due pivot low confermati: pivot a livello 27.300 con $\tau_{conf} = $ 10:15 e pivot a livello 27.250 con $\tau_{conf} = $ 11:30. Segnale long emesso alle 12:00. Applicando il criterio temporale: $\arg\max\{10{:}15,\, 11{:}30\} = 11{:}30$, dunque $p_{ref} = 27.250$. Il pivot estremo in prezzo (27.300) non è selezionato perché meno recente. Simmetricamente per uno short con due pivot high confermati 27.700 (10:15) e 27.750 (11:30): $p_{ref} = 27.750$.

**Coerenza con la causalità temporale.** Il prezzo $p_{ref}$ è derivato esclusivamente da pivot confermati e disponibili in $\mathcal{F}_{t-1}$: la barra di conferma $t + n_c$ di un pivot a $t$ rende il pivot disponibile dalla barra $t + n_c + 1$, quindi $p_{ref}$ calcolato alla barra $t_{emission}$ utilizza solo informazione in $\mathcal{F}_{t_{emission}-1}$. Non si utilizza il prezzo corrente della barra aperta.

### 16.2 Trattamento del warm-up: assenza di pivot confermati nella sessione corrente

Nelle prime barre di sessione, il pool di pivot confermati $\mathcal{P}_{high}(t)$ e $\mathcal{P}_{low}(t)$ è vuoto. In accordo con l'M-1 (v2 CAP-03) della Review v2 di CAP-03, questa situazione deve essere trattata esplicitamente: il motore non può emettere segnali privi di ancoraggio strutturale.

**Regola di sospensione dell'emissione in warm-up strutturale.** Se alla barra $t_{emission}$ vale $\mathcal{P}_{low}(t_{emission}) = \emptyset$ (per segnali long) o $\mathcal{P}_{high}(t_{emission}) = \emptyset$ (per segnali short), il motore **non emette** il segnale corrispondente. Nessun `signal_id` viene generato, nessuna zona viene costruita. Il motore continua a valutare le condizioni di emissione alle barre successive e riprende a emettere non appena il primo pivot rilevante viene confermato.

Questa regola produce una **latenza di emissione minima dall'apertura della sessione** dipendente dalla geometria del prezzo nelle prime barre. Con $n_c = 3$ e $\delta_{pivot} = 10$ pt provvisori (Cap.15.3 di Parte III), il primo pivot non può essere confermato prima della barra $n_c + 1 = 4$ della sessione; la disponibilità come feature inizia dalla barra $n_c + 2 = 5$. La latenza effettiva media è parametro empirico da stimare sullo storico Portara/CQG (valore di lavoro provvisorio $N_{pivot} = 30$ barre, coerente con Cap.15.3 di Parte III).

**Caso: pivot della sessione precedente come âncora di fallback.** Se la sessione corrente è aperta ma nessun pivot è ancora confermato nella sessione corrente (periodo di warm-up strutturale), il motore non utilizza i pivot della sessione precedente come âncora per la zona. Questa scelta è conservativa e motivata dalla condizione 4 dell'algoritmo frattale (Cap.15.3 di Parte III): la finestra $[t - n_c, t + n_c]$ di un pivot deve rientrare interamente nella sessione corrente. I pivot della sessione precedente sono livelli strutturali di una sessione chiusa; la loro rilevanza per la sessione corrente è catturata indirettamente dalle feature di struttura del catalogo (Cap.15.2.4 di Parte III), non come âncora diretta della zona di entry. In assenza di pivot confermati nella sessione corrente, il motore sospende l'emissione, in accordo con la regola di sospensione sopra.

**Interazione con i parametri di warm-up della Parte III.** Le prime $T_{warmup,\text{norm}} = 100$ barre della sessione sono marcate `unusable` per le feature normalizzate (Cap.15.4 di Parte III). La sospensione dell'emissione in warm-up strutturale è complementare ma distinta: anche dopo che il primo pivot è confermato (tipicamente prima della barra 30), l'emissione rimane sospesa fino alla barra 100 per mancanza di feature normalizzate valide. Il vincolo più stringente tra i due (warm-up strutturale vs warm-up normalizzazione) determina la prima barra ammissibile per l'emissione.

### 16.3 Costruzione della zona di entry

Dato $p_{ref}$ e la semi-ampiezza $b$, parametro libero del cromosoma con dominio $b \in \{5, 10, 15, 20, 25, 30, 35, 40\}$ punti FIB e $b_{min} = 5$ provvisorio (ereditato da Cap.6.1 di Parte II), la zona di entry è l'insieme discreto di livelli

$$\texttt{entry\_zone} = \{p_{ref} - b,\; p_{ref} - b + 5,\; \ldots,\; p_{ref} + b - 5,\; p_{ref} + b\}$$

La cardinalità della zona è $(2b/5) + 1$ livelli discreti (ereditata da Cap.6.1 di Parte II). Poiché $b$ è multiplo di 5 e $p_{ref}$ è multiplo di 5, tutti i livelli della zona sono multipli di 5 punti FIB.

Esempi numerici con tick FIB = 5 pt:
- $p_{ref} = 27.500$, $b = 20$ pt: entry\_zone $= \{27.480, 27.485, 27.490, 27.495, 27.500, 27.505, 27.510, 27.515, 27.520\}$, cardinalità 9.
- $p_{ref} = 27.500$, $b = 5$ pt (valore minimo): entry\_zone $= \{27.495, 27.500, 27.505\}$, cardinalità 3.

### 16.4 Condizione di raw touch

Il **raw touch** della zona di entry è l'evento in cui la barra 1-min chiusa interseca per la prima volta l'entry\_zone. La formalizzazione in termini di OHLC della barra 1-min è la seguente.

Sia $[\text{low}_t, \text{high}_t]$ l'intervallo di prezzo della barra 1-min al tempo $t$, con $\text{low}_t \leq \text{high}_t$ e entrambi multipli di 5. Il raw touch avviene alla barra $t$ se e solo se

$$[\text{low}_t,\; \text{high}_t] \cap \texttt{entry\_zone} \neq \emptyset$$

ovvero se esiste almeno un livello $q \in \texttt{entry\_zone}$ tale che $\text{low}_t \leq q \leq \text{high}_t$.

Condizione equivalente con i bordi della zona: poiché la zona è l'intervallo continuo $[p_{ref} - b, p_{ref} + b]$ campionato su multipli di 5, la condizione di intersezione è:

$$\text{low}_t \leq p_{ref} + b \quad \text{e} \quad \text{high}_t \geq p_{ref} - b$$

Il raw touch è valutato a partire dalla barra $t_{emission} + 1$ (la prima barra chiusa dopo l'emissione), in coerenza con l'edge case (a) di Cap.7.3 di Parte II. La barra $t_{emission}$ non è valutata.

**Direzione del raw touch.** La definizione di raw touch non impone alcuna condizione sulla direzione di provenienza del prezzo: la prima barra il cui intervallo high-low contenga almeno un livello della zona produce il raw touch, indipendentemente dalla direzione del prezzo nella barra stessa. Questa scelta, ereditata da Cap.7.3 di Parte II, recepisce il vincolo operativo che l'operatore riceve la notifica del trigger e agisce manualmente: la direzione di provenienza del prezzo è visibile all'operatore e influenza la sua decisione, ma non è un filtro del motore.

**Coerenza con il fill virtuale worst-case.** Una volta che il raw touch avviene, il fill virtuale in backtest è assegnato al bordo più sfavorevole della zona, in accordo con Cap.12.4 di Parte III:
- **Segnale long**: fill al bordo superiore $p_{ref} + b$ (costo di acquisto più alto entro la zona).
- **Segnale short**: fill al bordo inferiore $p_{ref} - b$ (prezzo di vendita più basso entro la zona).

Entrambi i bordi sono multipli di 5. Il survival model di Cap.19 condiziona la propria stima al prezzo di fill worst-case, non al centro $p_{ref}$ della zona.

### 16.5 Invalidazione strutturale pre-touch

L'invalidazione strutturale pre-touch è la transizione `active` → `invalidated` che si verifica prima del raw touch quando le condizioni geometriche che giustificavano l'emissione del segnale sono state smentite dal mercato. Le condizioni di invalidazione qui formalizzate integrano quelle già dichiarate in Cap.7.1 di Parte II.

**Condizione I1 — Superamento del livello stop nella direzione avversa.** Questa condizione è già inclusa nel contratto di Parte II (Cap.7.1 e 7.2): per segnali long, $p(t) \leq \texttt{stop\_loss}$ con $t < t_{touch}$; per segnali short, $p(t) \geq \texttt{stop\_loss}$ con $t < t_{touch}$. La condizione è valutata sul prezzo di chiusura della barra 1-min $p_t$ (prezzo close).

**Condizione I2 — Allontanamento dalla zona oltre la soglia $d_{inv}$.** Se il prezzo si allontana dalla zona di entry verso la direzione avversa al segnale di una distanza superiore a $d_{inv}$ punti FIB rispetto al bordo più vicino della zona, il segnale viene invalidato. Formalmente:

- **Segnale long**: il prezzo close si è allontanato verso il basso oltre $d_{inv}$ dalla zona: $p_t < p_{ref} - b - d_{inv}$.
- **Segnale short**: il prezzo close si è allontanato verso l'alto oltre $d_{inv}$ dalla zona: $p_t > p_{ref} + b + d_{inv}$.

Il parametro $d_{inv}$ è un parametro del cromosoma (dominio: multipli di 5 pt, floor $d_{inv,min} = 5$ pt provvisorio), congelato in Parte V. Il razionale è che un prezzo che si allontana significativamente dalla zona segnala che la struttura che ha motivato il segnale è stata invalidata da un nuovo movimento direzionale.

**Condizione I3 — Formazione di un nuovo pivot strutturale che rende obsoleta la zona.** Se durante il periodo di attesa del raw touch viene confermato un nuovo pivot dello stesso tipo di $p_{ref}$ (un nuovo pivot low per segnale long, un nuovo pivot high per segnale short) a un livello significativamente diverso da $p_{ref}$, la zona esistente è obsoleta. La soglia di "diversità significativa" è $|p_{new\_pivot} - p_{ref}| \geq d_{obsolete}$, dove $d_{obsolete}$ è un parametro del cromosoma (dominio: multipli di 5 pt, floor provvisorio $d_{obsolete,min} = 5$ pt), congelato in Parte V. In questo caso il segnale viene invalidato e il motore può emettere un nuovo segnale basato sul pivot aggiornato, secondo la regola di sostituzione di Cap.6.3 di Parte II.

**Precedenza delle transizioni.** In caso di coincidenza temporale di più eventi (raw touch e invalidazione nella stessa barra), si applica la precedenza dichiarata in Cap.7.2 di Parte II: expiry > invalidazione > missed_target > raw touch. La condizione I2 e I3 sono classificate come invalidazione e hanno precedenza sul raw touch.

**Dichiarazione di provvisorietà.** I parametri $d_{inv}$ e $d_{obsolete}$ sono dichiarati provvisori e congelati in Parte V sulla base dell'analisi empirica dei tassi di invalidazione e della correlazione con le metriche di lifecycle.

### 16.6 Condizione di tempo residuo minimo di sessione

Il segnale non può essere emesso se il tempo residuo di sessione è inferiore a una soglia minima $T_{min,session}$. Formalmente:

$$T_{residuo}(t_{emission}) = t_{session\_end} - t_{emission} \geq T_{min,session}$$

dove $t_{session\_end}$ è la chiusura della sessione alle 22:00 CET e il tempo residuo è misurato in minuti di trading.

Il parametro $T_{min,session}$ è un parametro del cromosoma (dominio: interi positivi in minuti di trading, floor provvisorio $T_{min,session,min} = 15$ minuti), congelato in Parte V. La motivazione è duplice: (a) un segnale emesso con meno di $T_{min,session}$ minuti di sessione residua ha probabilità di successo molto bassa, poiché il survival model (Cap.19) condizionerà $\hat{p}_{hit}$ a un $T_{residuo}$ basso, producendo una stima sotto la soglia $\tau_{surv}$; (b) l'emissione a fine sessione produce lifecycle troncati che distorcono le metriche di validazione OOS.

Il filtro di tempo residuo si applica a valle di tutte le altre condizioni di emissione (Cap.8.3 di Parte II) e prima della costruzione della zona: se $T_{residuo}(t_{emission}) < T_{min,session}$, il motore non costruisce la zona e non valuta le altre condizioni.

---

## Capitolo 17 — Target strutturali

### 17.1 Algoritmo di selezione di target_1

Il target_1 è il primo livello strutturale di obiettivo del segnale, derivato dall'insieme dei pivot strutturali confermati nella sessione corrente e disponibili alla barra $t_{emission}$. Il target_1 è sempre un multiplo di 5 punti FIB.

**Insieme dei livelli candidati.** Per un segnale long, i livelli target candidati sono i pivot high confermati nella sessione corrente con livello superiore a $p_{ref}$:

$$\mathcal{T}^+_{high}(t) = \{p \in \mathcal{P}_{high}(t) : p > p_{ref}\}$$

Per un segnale short, i livelli target candidati sono i pivot low confermati con livello inferiore a $p_{ref}$:

$$\mathcal{T}^-_{low}(t) = \{p \in \mathcal{P}_{low}(t) : p < p_{ref}\}$$

**Regola di selezione — pivot più prossimo.** Il target_1 è il livello candidato più vicino a $p_{ref}$ nella direzione del segnale:

$$\texttt{target\_1} = \begin{cases} \min \mathcal{T}^+_{high}(t) & \text{per segnale long} \\ \max \mathcal{T}^-_{low}(t) & \text{per segnale short} \end{cases}$$

Il pivot più prossimo è selezionato perché è il primo livello strutturale che il prezzo deve raggiungere nella direzione del segnale, e quindi quello su cui il survival model può stimare la probabilità di successo con maggior affidabilità. La scelta del pivot più prossimo come target primario è coerente con la filosofia di segnali intraday con validità breve (cap 2 giorni di trading, Q-04 di CAP-01): livelli strutturali molto distanti hanno probabilità di raggiungimento bassa nell'orizzonte temporale del segnale.

**Caso: insieme candidati vuoto.** Se $\mathcal{T}^+_{high}(t) = \emptyset$ (per long) o $\mathcal{T}^-_{low}(t) = \emptyset$ (per short), non esiste un livello target strutturale nella direzione del segnale e il motore **non emette** il segnale. Questa situazione è plausibile nelle prime barre di sessione quando non sono ancora stati confermati pivot nella direzione del target.

**Determinismo.** Dato lo storico OHLC e i parametri $(n_c, \delta_{pivot})$, l'insieme $\mathcal{P}_{high}(t)$ e $\mathcal{P}_{low}(t)$ è univocamente determinato (Cap.15.3 di Parte III), e quindi target_1 è univocamente determinato. La selezione non contiene componenti stocastiche.

### 17.2 Vincolo minimo 80 punti per setup directional

Per i setup di classe `directional`, il target_1 selezionato deve soddisfare il vincolo di distanza minima ereditato da Cap.5 di Parte I e Cap.6.1 di Parte II:

$$|\texttt{target\_1} - p_{ref}| \geq 80\;\text{punti FIB}$$

Se il pivot più prossimo nella direzione del segnale è a meno di 80 punti da $p_{ref}$, il motore verifica se esiste un pivot più lontano che soddisfi il vincolo:

$$\mathcal{T}^+_{80}(t) = \{p \in \mathcal{T}^+_{high}(t) : p - p_{ref} \geq 80\} \quad \text{(per long)}$$

$$\mathcal{T}^-_{80}(t) = \{p \in \mathcal{T}^-_{low}(t) : p_{ref} - p \geq 80\} \quad \text{(per short)}$$

Se $\mathcal{T}^+_{80}(t) = \emptyset$ (o $\mathcal{T}^-_{80}(t) = \emptyset$ per short), nessun livello strutturale disponibile soddisfa il vincolo 80 pt e il motore **non emette** il segnale directional. La regola è un vincolo assoluto non allentabile dal cromosoma, in coerenza con il punto 4 della dichiarazione di intenti.

Se l'insieme non è vuoto, target_1 viene ridefinito come:

$$\texttt{target\_1} = \begin{cases} \min \mathcal{T}^+_{80}(t) & \text{per long} \\ \max \mathcal{T}^-_{80}(t) & \text{per short} \end{cases}$$

ovvero il primo livello strutturale che soddisfa il vincolo 80 pt nella direzione del segnale.

Esempio numerico (tick FIB = 5 pt): $p_{ref} = 27.500$, segnale long. Pivot high confermati nella sessione: $\{27.540, 27.570, 27.600\}$. Il pivot più prossimo è 27.540 (distanza 40 pt < 80 pt), non ammesso. Il pivot successivo è 27.570 (distanza 70 pt < 80 pt), non ammesso. Il pivot 27.600 (distanza 100 pt ≥ 80 pt) è il primo che soddisfa il vincolo: target_1 = 27.600.

### 17.3 Condizione di distanza in sigma-units

La condizione di distanza strutturale in sigma-units di Cap.8.2 di Parte II si applica a target_1 dopo la selezione:

$$\frac{|\texttt{target\_1} - p_{ref}|}{\hat{\sigma}_{\text{pt}}(t_{emission})} \geq \tau_{dist}^{\sigma}$$

dove $\hat{\sigma}_{\text{pt}}(t_{emission})$ è la stima EGARCH in punti FIB (Cap.13.1 di Parte III) e $\tau_{dist}^{\sigma}$ è parametro del cromosoma. Il filtro 80 pt e la condizione sigma-units sono **vincoli separati e indipendenti**: entrambi devono essere soddisfatti simultaneamente. Il più restrittivo dei due domina in ogni contesto di mercato specifico.

In regime di bassa volatilità ($\hat{\sigma}_{\text{pt}}$ piccolo), la condizione sigma-units può essere più restrittiva del filtro 80 pt: ad esempio, con $\hat{\sigma}_{\text{pt}} = 15$ pt e $\tau_{dist}^{\sigma} = 6$, si richiede $|\texttt{target\_1} - p_{ref}| \geq 90$ pt, maggiore di 80 pt. In regime di alta volatilità ($\hat{\sigma}_{\text{pt}}$ elevato), il filtro 80 pt è il più restrittivo: con $\hat{\sigma}_{\text{pt}} = 50$ pt e $\tau_{dist}^{\sigma} = 2$, si richiede $|\texttt{target\_1} - p_{ref}| \geq 100$ pt, ancora maggiore di 80 pt nel caso specifico ma parametrizzabile in modo più flessibile dal cromosoma.

La regola di emissione complessiva (Cap.8.3 di Parte II) richiede il soddisfacimento simultaneo di $E_{vol}$, $E_{liq}$, $E_{dist}^{\sigma}$, $E_{80pt}$, $E_{surv}$ (Cap.20): l'AND logico di tutte le condizioni.

### 17.4 Algoritmo di selezione di target_2

Il target_2 è il secondo livello strutturale di obiettivo, informazione strutturale pubblicata nel payload $\mathcal{S}$ (decisione Q-05, Clausola 2 di Parte II). Il target_2 è sempre un multiplo di 5 e soddisfa il vincolo

$$|\texttt{target\_2}| > |\texttt{target\_1}| \text{ nella direzione del segnale}$$

ovvero: per long, $\texttt{target\_2} > \texttt{target\_1} > p_{ref}$; per short, $\texttt{target\_2} < \texttt{target\_1} < p_{ref}$.

**Algoritmo di selezione.** Il target_2 è selezionato dall'insieme dei pivot strutturali confermati nella direzione del segnale con livello più lontano di target_1:

$$\mathcal{T}^+_2(t) = \{p \in \mathcal{P}_{high}(t) : p > \texttt{target\_1}\} \quad \text{(per long)}$$

$$\mathcal{T}^-_2(t) = \{p \in \mathcal{P}_{low}(t) : p < \texttt{target\_1}\} \quad \text{(per short)}$$

$$\texttt{target\_2} = \begin{cases} \min \mathcal{T}^+_2(t) & \text{per long} \\ \max \mathcal{T}^-_2(t) & \text{per short} \end{cases}$$

Il target_2 è il prossimo pivot strutturale oltre target_1, ovvero il secondo obiettivo strutturale naturale nella direzione del segnale.

**Caso: target_2 non disponibile.** Se l'insieme $\mathcal{T}^+_2(t)$ (o $\mathcal{T}^-_2(t)$) è vuoto — perché non esistono pivot strutturali confermati oltre target_1 nella sessione corrente — il target_2 è stimato come livello strutturale sintetico derivato da una regola deterministica basata su $\hat{\sigma}_{\text{pt}}$:

$$\texttt{target\_2} = \texttt{target\_1} + k_{t2} \cdot \hat{\sigma}_{\text{pt}}(t_{emission}) \quad \text{(per long, arrotondato al multiplo di 5 più vicino)}$$

$$\texttt{target\_2} = \texttt{target\_1} - k_{t2} \cdot \hat{\sigma}_{\text{pt}}(t_{emission}) \quad \text{(per short, arrotondato al multiplo di 5 più vicino)}$$

dove $k_{t2}$ è un parametro del cromosoma (dominio: $\mathbb{R}^+$, valore provvisorio $k_{t2} = 2$, congelato in Parte V). Questo livello sintetico non è un pivot strutturale confermato; il fatto che sia derivato da un parametro del modello viene esplicitato nel **payload formale del segnale** mediante il campo obbligatorio `target_2_type` $\in \{\text{structural}, \text{synthetic}\}$ aggiunto alla tupla $\mathcal{S}$ in Cap.6.1 di Parte II (mini-patch Iterazione 4 di CAP-02, chiusura O-3 / M-12 v2). Il valore del campo è popolato deterministicamente dall'algoritmo di selezione di target_2: `structural` quando target_2 è scelto da $\mathcal{T}^+_2(t)$ o $\mathcal{T}^-_2(t)$ (caso pivot strutturale disponibile); `synthetic` quando si applica la regola di fallback basata su $\hat{\sigma}_{\text{pt}}$ e $k_{t2}$ qui sopra (caso pivot oltre target_1 non disponibile). Il consumer Telegram dell'operatore (Cap.9.2 di Parte II) usa questo campo per qualificare la natura del livello pubblicato.

**Determinismo.** La selezione di target_2 è deterministica dato lo storico OHLC e i parametri del modello. L'eventuale livello sintetico è calcolato deterministicamente da $\hat{\sigma}_{\text{pt}}$ e $k_{t2}$.

---

## Capitolo 18 — Stop strutturali

### 18.1 Algoritmo di derivazione dello stop strutturale

Lo stop strutturale è il livello di prezzo nella direzione opposta al segnale che chiude il contratto del segnale se raggiunto dopo il raw touch (transizione `active` → `stopped`, Cap.7.1 di Parte II). Lo stop è sempre un multiplo di 5 punti FIB.

**Insieme dei livelli candidati per stop.** Per un segnale long, lo stop è derivato dall'insieme dei pivot low confermati con livello inferiore alla zona di entry:

$$\mathcal{S}^-_{low}(t) = \{p \in \mathcal{P}_{low}(t) : p < p_{ref} - b\}$$

Il candidato naturale per lo stop long è il pivot low più recente sotto la zona (il supporto strutturale appena violato):

$$\texttt{stop\_loss}^{(pivot)} = \max \mathcal{S}^-_{low}(t) \quad \text{(per long)}$$

Per un segnale short, lo stop è derivato dall'insieme dei pivot high confermati con livello superiore alla zona:

$$\mathcal{S}^+_{high}(t) = \{p \in \mathcal{P}_{high}(t) : p > p_{ref} + b\}$$

$$\texttt{stop\_loss}^{(pivot)} = \min \mathcal{S}^+_{high}(t) \quad \text{(per short)}$$

**Regola di fallback basata su $\hat{\sigma}_{\text{pt}}$.** Se l'insieme dei candidati pivot per lo stop è vuoto — nessun pivot nella direzione avversa è confermato nella sessione corrente — lo stop viene calcolato come livello derivato da $\hat{\sigma}_{\text{pt}}$:

$$\texttt{stop\_loss}^{(\sigma)} = p_{ref} - d_{stop,\sigma} \cdot \hat{\sigma}_{\text{pt}}(t_{emission}) \quad \text{(per long, arrotondato al multiplo di 5 inferiore)}$$

$$\texttt{stop\_loss}^{(\sigma)} = p_{ref} + d_{stop,\sigma} \cdot \hat{\sigma}_{\text{pt}}(t_{emission}) \quad \text{(per short, arrotondato al multiplo di 5 superiore)}$$

dove $d_{stop,\sigma}$ è un parametro del cromosoma (dominio: $\mathbb{R}^+$, valore provvisorio $d_{stop,\sigma} = 3$, congelato in Parte V). Questo stop sintetico non è un pivot strutturale confermato.

**Flag `stop_type` nel payload formale (chiusura O-3 / M-12 v2).** La natura strutturale o sintetica dello stop è esplicitata nel **payload formale del segnale** mediante il campo obbligatorio `stop_type` $\in \{\text{structural}, \text{personal}\}$ aggiunto alla tupla $\mathcal{S}$ in Cap.6.1 di Parte II (mini-patch Iterazione 4 di CAP-02). Il dominio è dichiarato `{structural, personal}` in coerenza con la separazione di Cap.18.3 di questa Parte IV fra stop strutturale (prodotto dal motore) e stop personale (decisione esclusiva dell'operatore, fuori scope dal contratto). Per i segnali emessi dal motore, il valore del campo `stop_type` è popolato come `structural` in tutti i casi (sia quando `stop_loss` deriva dal candidato pivot, sia quando deriva dal candidato sigma di fallback): entrambi i candidati appartengono alla famiglia degli stop **strutturali del motore** in contrapposizione allo stop personale dell'operatore di Cap.18.3, esterno al payload. Il valore `personal` non viene mai assegnato dal motore al campo del payload pubblicato — esso è riservato come segnaposto formale per l'eventuale tracciamento dello stop personale in registri esterni al motore (es. diario operativo), fuori scope dal presente documento. La distinzione interna fra candidato pivot e candidato sigma è registrata nel log di emissione (Cap.10.2 di Parte II) come campo strutturato di diagnostica e alimenta la metrica di qualità strutturale dello stop in Parte V.

**Scelta tra candidato pivot e candidato sigma.** Quando entrambi sono disponibili, si utilizza il candidato pivot, che è l'ancora strutturale prioritaria. Il candidato sigma è il fallback esclusivo per l'assenza di pivot.

**Determinismo.** L'algoritmo è deterministico: dato lo storico OHLC, i parametri $(n_c, \delta_{pivot})$ e il modello EGARCH calibrato, lo stop_loss è univocamente determinato.

### 18.2 Vincolo geometrico $d_{stop} > b$

Il vincolo geometrico obbligatorio ereditato da Cap.2 di Parte I e Cap.6.1 di Parte II è:

$$d_{stop} = |p_{ref} - \texttt{stop\_loss}| > b$$

Questo vincolo garantisce che lo stop sia fuori dalla zona di entry, impedendo che un fill al bordo della zona coincida con lo stop. Il vincolo si applica allo stop sia pivot sia sigma.

**Verifica del vincolo dopo la selezione dello stop.** Dopo aver determinato `stop_loss` secondo l'algoritmo di Cap.18.1, il motore verifica che $d_{stop} > b$. Se il vincolo è violato — il pivot stop è troppo vicino a $p_{ref}$, ovvero $|p_{ref} - \texttt{stop\_loss}^{(pivot)}| \leq b$ — il candidato pivot viene scartato e il motore ricerca il pivot stop più distante che rispetti il vincolo:

$$\texttt{stop\_loss} = \begin{cases} \max\{p \in \mathcal{S}^-_{low}(t) : p_{ref} - p > b\} & \text{per long} \\ \min\{p \in \mathcal{S}^+_{high}(t) : p - p_{ref} > b\} & \text{per short} \end{cases}$$

Se nessun pivot soddisfa $d_{stop} > b$, si utilizza il candidato sigma, verificando che anch'esso soddisfi il vincolo (il che è garantito scegliendo $d_{stop,\sigma} > b/\hat{\sigma}_{\text{pt}}$, condizione verificata dal cromosoma). Cromosomi che producono stop_loss con $d_{stop} \leq b$ in assenza di alternative sono dichiarati non validi e non entrano nella popolazione del GA, in coerenza con Cap.6.1 di Parte II.

Esempio numerico (tick FIB = 5 pt): $p_{ref} = 27.500$, $b = 20$ pt. La zona di entry è $[27.480, 27.520]$. Lo stop per un segnale long deve soddisfare $27.500 - \texttt{stop\_loss} > 20$, ovvero $\texttt{stop\_loss} < 27.480$. Se il pivot low più recente è a 27.460 (distanza 40 pt > 20 pt), il vincolo è rispettato. Se il pivot low è a 27.490 (distanza 10 pt < 20 pt), il vincolo è violato e si cerca il pivot più distante.

### 18.3 Separazione stop strutturale vs stop personale dell'operatore

Lo stop strutturale pubblicato nel payload $\mathcal{S}$ è il livello strutturale che definisce il contratto del segnale. Esso viene utilizzato dal motore per:
- produrre la transizione `active` → `stopped` in backtest quando il prezzo post-trigger raggiunge `stop_loss`;
- produrre la transizione `active` → `invalidated` pre-touch quando il prezzo scende sotto `stop_loss` (per long) o sale sopra `stop_loss` (per short), secondo Cap.7.1 di Parte II;
- alimentare le metriche MAE, MFE e $f_{stop \mid t_1}$ della submacchina di position lifecycle (Cap.11 di Parte II).

L'operatore può adottare uno stop personale più stretto del livello strutturale pubblicato — in conformità con il punto 2 della dichiarazione di intenti ("inserisco -200 pt di stop") — ma questa decisione è fuori scope dal motore e non modifica il contratto del segnale. La separazione è formalmente dichiarata in Cap.2 di Parte I e in Cap.11 di Parte II; qui si riconferma per completezza della Parte IV. Il payload pubblicato dal motore reca sempre `stop_type = structural` (Cap.18.1 di questa Parte IV); il valore `personal` del dominio del campo è riservato a registri esterni e non viene mai prodotto dal motore.

### 18.4 Risk-reward ratio strutturale

La distanza target e la distanza stop determinano il **risk-reward ratio strutturale** del segnale:

$$\text{RR} = \frac{d_{target}}{d_{stop}} = \frac{|\texttt{target\_1} - p_{ref}|}{|p_{ref} - \texttt{stop\_loss}|}$$

Questa grandezza è osservabile per ogni segnale emesso e alimenta il reporting fold-by-fold del walk-forward (Parte V). Non viene imposto un vincolo rigido floor/cap sul ratio RR in Parte IV: il GA ottimizza implicitamente RR attraverso la fitness, selezionando cromosomi che producono setup con ratio strutturalmente favorevole. Un eventuale floor esplicito su RR (es. RR ≥ 1) è materia di Parte V, dove sarà valutato sulla base dell'evidenza empirica.

Il calcolo del rendimento netto in punti FIB per segnale eseguito consuma $d_{target}$ e $d_{stop}$:
- rendimento lordo in caso di `target_1_hit`: $+d_{target} - 2c$ (long) o $+d_{target} - 2c$ (short), dove $c = 1$ pt equivalente per commissione;
- rendimento lordo in caso di `stopped`: $-d_{stop} - 2c$.

Il GA massimizza il valore atteso del rendimento netto ottimizzando congiuntamente $d_{target}$ (attraverso la selezione di target_1 e la scelta di $p_{ref}$) e $d_{stop}$ (attraverso la selezione dello stop strutturale e il parametro $d_{stop,\sigma}$).

### 18.5 Condizionalità dello stop al regime

Il motore consente al cromosoma di specificare parametri di stop condizionali al regime $R_t \in \{\text{calmo}, \text{turbolento}\}$ (Cap.14 di Parte III), in analogia con la condizionalità di $\tau_{vol}$ dichiarata in Cap.14.4 di Parte III e in Cap.8.2 di Parte II.

**Stop strutturale regime-dipendente.** Il parametro $d_{stop,\sigma}$ può essere condizionale al regime:

$$d_{stop,\sigma} = \begin{cases} d_{stop,\sigma,\text{calmo}} & \text{se } R_{t_{emission}} = \text{calmo} \\ d_{stop,\sigma,\text{turbolento}} & \text{se } R_{t_{emission}} = \text{turbolento} \end{cases}$$

I due parametri $d_{stop,\sigma,\text{calmo}}$ e $d_{stop,\sigma,\text{turbolento}}$ sono parametri del cromosoma, con $d_{stop,\sigma,\text{turbolento}} \geq d_{stop,\sigma,\text{calmo}}$ come vincolo di ammissibilità opzionale (uno stop più ampio in regime turbolento è strutturalmente motivato dalla maggiore volatilità). Il vincolo $d_{stop} > b$ si applica in entrambi i regimi.

La condizionalità al regime è **opzionale**: il cromosoma può specificare un unico valore comune $d_{stop,\sigma}$ applicabile in entrambi i regimi, oppure due valori distinti. La scelta è materia della struttura del cromosoma (Parte V).

---

## Capitolo 19 — Modello di survival per il target

### 19.1 Variabile obiettivo e formulazione del problema

Il modello di survival stima la probabilità condizionata che un segnale eseguito (dopo il raw touch della zona con fill virtuale worst-case) raggiunga target_1 prima di raggiungere stop_loss, condizionata sulle feature di mercato disponibili al momento dell'emissione.

**Variabile obiettivo.** Sia $\tau$ il tempo in minuti di trading trascorso dal fill virtuale (raw touch alla barra $t_{exec}$, fill al bordo worst-case della zona) all'evento terminale del segnale post-trigger. L'evento terminale è uno dei seguenti:
- **target_1_hit**: il prezzo ha raggiunto `target_1` — evento di successo;
- **stopped**: il prezzo ha raggiunto `stop_loss` — evento di fallimento;
- **expired**: il timer post-trigger $\Delta t_{cromosoma}$ è scaduto senza hit né stop — censoring a destra.

La variabile $\tau$ è una durata in minuti di trading, misurata sul calendario della sessione 8:00-22:00 CET (i minuti fuori sessione non avanzano il contatore, in coerenza con il timer post-trigger di Cap.7.4 di Parte II).

**Competing risks.** Il target_1_hit e lo stopped sono **rischi concorrenti** (competing risks): entrambi possono terminare il segnale, e la probabilità di ciascuno dipende congiuntamente dalle feature di mercato, dalla distanza target-stop e dal tempo residuo. Il modello di survival tratta esplicitamente i rischi concorrenti, non li collassa in un unico evento terminale.

### 19.2 Formulazione matematica del modello candidato primario

Il modello candidato primario è il **modello di Cox a rischi proporzionali** (Cox proportional hazards, Cox 1972), esteso al caso di rischi concorrenti mediante la specificazione di una **cause-specific hazard function** per ciascun tipo di evento.

**Notazione.** Sia $j \in \{1, 2\}$ l'indice del tipo di evento: $j=1$ per target_1_hit, $j=2$ per stopped. Sia $\mathbf{x}$ il vettore delle feature causali normalizzate disponibili alla barra $t_{emission}$ (sottoinsieme delle 37 feature del catalogo di Cap.15 di Parte III, selezione rinviata a Parte V/VII). Sia $T_{residuo}$ il tempo residuo di sessione (o di validità del segnale, con cap 2 giorni di trading) in minuti di trading.

**Cause-specific hazard function.** La funzione di rischio causa-specifica per l'evento $j$ al tempo $\tau$ dalla fill è:

$$h_j(\tau \mid \mathbf{x}, T_{residuo}) = h_{0,j}(\tau) \cdot \exp\!\Big(\boldsymbol{\beta}_j^\top \mathbf{x} + \gamma_j \cdot T_{residuo}\Big)$$

dove:
- $h_{0,j}(\tau)$ è la **baseline hazard** causa-specifica, stimata non parametricamente (stima di Breslow) o parametricamente (Weibull, log-normal) — scelta in Parte V via criterio OOS;
- $\boldsymbol{\beta}_j$ è il vettore dei coefficienti delle feature per l'evento $j$, stimato dalla MLE del modello di Cox;
- $\gamma_j$ è il coefficiente del tempo residuo $T_{residuo}$, che cattura l'effetto di scadenza imminente sulla probabilità di ciascun evento.

Il riferimento metodologico per i modelli di competing risks nel contesto finanziario è: **Fine e Gray (1999)** "A Proportional Hazards Model for the Subdistribution of a Competing Risk", *Journal of the American Statistical Association* 94(446), 496–509, che introducono il modello per la subdistribuzione come alternativa alla cause-specific hazard per la stima diretta della probabilità cumulativa di incidenza.

La scelta della **cause-specific hazard** (approccio Cox) come modello primario rispetto al modello Fine-Gray è motivata dall'interpretabilità: i coefficienti $\boldsymbol{\beta}_j$ hanno un'interpretazione diretta come log-hazard ratio per ciascun evento causa-specifica, permettendo al supervisore di verificare che le feature abbiano effetti strutturalmente plausibili (es. alta volatilità $\hat{\sigma}_{\text{pt}}$ dovrebbe aumentare $h_2$ — il rischio di stopped — più di $h_1$). Il confronto empirico tra i due approcci è rinviato a Parte V come benchmark di robustezza.

**Funzione di survival complessiva.** La funzione di survival complessiva (probabilità di non aver raggiunto né target_1 né stop al tempo $\tau$) è:

$$\hat{S}(\tau \mid \mathbf{x}, T_{residuo}) = \exp\!\left(-\int_0^\tau \big[h_1(u \mid \mathbf{x}, T_{residuo}) + h_2(u \mid \mathbf{x}, T_{residuo})\big]\,du\right)$$

**Probabilità di successo del segnale.** La quantità di interesse operativo è la **probabilità cumulativa di incidenza** del target_1_hit entro il tempo residuo $T_{residuo}$, condizionata sulle feature e sul regime:

$$\hat{p}_{hit}(\mathbf{x}, T_{residuo}, R) = \Pr\!\big(\text{target\_1\_hit prima di stopped, entro } T_{residuo} \mid \mathbf{x}, R\big)$$

$$= \int_0^{T_{residuo}} h_1(\tau \mid \mathbf{x}, T_{residuo}) \cdot \hat{S}(\tau \mid \mathbf{x}, T_{residuo})\,d\tau$$

Questa quantità è la **probabilità di successo del segnale**, consumata dal filtro di emissione survival-based di Cap.20.

**Condizionalità al regime.** Il regime $R_t \in \{\text{calmo}, \text{turbolento}\}$ entra nel modello in due modi alternativi (scelta in Parte V): (a) come feature aggiuntiva nel vettore $\mathbf{x}$ (modello unico con l'indicatore di regime come predittore); (b) come stratificazione: il modello di Cox viene stimato separatamente per il regime calmo e per il regime turbolento, con baseline hazard $h_{0,j,calmo}$ e $h_{0,j,turbolento}$ distinte e coefficienti $\boldsymbol{\beta}_{j,calmo}$, $\boldsymbol{\beta}_{j,turbolento}$ potenzialmente diversi. La stratificazione cattura interazioni non lineari tra regime e feature che il singolo indicatore binario potrebbe non catturare.

### 19.3 Feature input del modello di survival

Il vettore di feature $\mathbf{x}$ è un sottoinsieme delle 37 feature causali normalizzate del catalogo di Cap.15 di Parte III. Le feature ammissibili come input al survival sono quelle disponibili in $\mathcal{F}_{t_{emission}-1}$, già normalizzate via z-score MAD (Cap.15.4 di Parte III). Il modello consuma feature normalizzate $\tilde{\mathbf{x}}$, non le feature raw.

**Feature strutturalmente rilevanti per il survival.** Alcune feature del catalogo sono particolarmente rilevanti a priori per la probabilità di successo del segnale:

- $\hat{\sigma}_{\text{pt}}(t_{emission})$ (feature di volatilità): la volatilità condizionata influenza la velocità di raggiungimento del target e la probabilità di stopped.
- Distanza $|\texttt{target\_1} - p_{ref}| / \hat{\sigma}_{\text{pt}}$ (distanza target in sigma-units): feature derivata dalle scelte geometriche del cromosoma e dallo stato di mercato.
- $T_{residuo}$ (tempo residuo di sessione): cattura l'effetto di scadenza imminente.
- Feature di struttura pivot (Cap.15.2.4 di Parte III): distanza dal pivot più recente, numero di pivot confermati, durata del regime corrente.
- $R_t$ (classificazione di regime, Cap.14 di Parte III): stato calmo/turbolento al momento dell'emissione.

**Selezione del sottoinsieme.** La selezione effettiva delle feature da includere nel vettore $\mathbf{x}$ del survival è materia del cromosoma (Parte V) o del wrapper di validazione (Parte VII). La Parte IV definisce il catalogo ammissibile, non il sottoinsieme selezionato. La dimensionalità massima di $\mathbf{x}$ è un parametro del modello, congelato in Parte V per evitare overfitting del survival sulle feature del cromosoma.

### 19.4 Calibrazione fold-per-fold

Il survival model è calibrato esclusivamente sui dati di backtest della finestra in-sample del walk-forward, separatamente per ciascun fold, in coerenza con la cadenza di calibrazione dell'EGARCH di Cap.13.3 di Parte III. La procedura è la seguente.

**Input di calibrazione.** Per ogni fold $k$ del walk-forward, l'input del survival è la sequenza di triplette $(\tau_i, \delta_i, \mathbf{x}_i)$ derivate dal replay deterministico del motore sulla finestra in-sample del fold $k$:
- $\tau_i$: durata osservata in minuti di trading dall'evento di fill all'evento terminale (o alla censura);
- $\delta_i \in \{0, 1, 2\}$: indicatore di evento (0 = censurato, 1 = target_1_hit, 2 = stopped);
- $\mathbf{x}_i$: vettore di feature normalizzate al momento dell'emissione del segnale $i$.

**Censoring a destra.** I segnali che raggiungono l'`expired` con causa `posttrigger_timeout` (Cap.7.1 di Parte II) senza aver raggiunto né target_1 né stop_loss sono censurati a destra a $\tau_i = \Delta t_{cromosoma}$ minuti di trading. I segnali che raggiungono l'`expired` con causa `pretrigger_timeout` (timeout pre-trigger di Cap.7.5 di Parte II) non entrano nel campione del survival post-fill, poiché non hanno avuto un raw touch e dunque non hanno un istante $t_{exec}$ di fill da cui far decorrere $\tau$.

**Assunzione di censoring non-informativo (chiusura O-5 / M-7 v2).** Il modello di Cox cause-specific qui formalizzato assume che il meccanismo di censoring sia **non-informativo rispetto ai tempi di evento, condizionatamente al vettore di covariate $\tilde{\mathbf{x}}_t$**. Formalmente, denotato con $C$ il tempo di censoring e con $T_j$ il tempo dell'evento causa-specifica $j \in \{1, 2\}$, vale

$$
T_j \perp\!\!\!\perp C \mid \tilde{\mathbf{x}}_t, \quad j \in \{1, 2\},
$$

ovvero condizionatamente alle covariate del momento dell'emissione, il tempo residuo di sessione e dunque il timeout di censoring non porta informazione aggiuntiva sui tempi di hit o di stop. L'assunzione è **plausibile a priori** per due ragioni strutturali: (a) il timeout di sessione che genera il censoring è fissato dall'orario di chiusura (22:00 CET, Cap.7.4 di Parte II) e non dipende dalla dinamica del prezzo né dalle decisioni dell'operatore; (b) il timer post-trigger $\Delta t_{cromosoma}$ è un parametro del cromosoma calibrato sul training set, frozen sul fold in-sample e applicato uniformemente a tutti i segnali del fold OOS — la sua scelta non è correlata con le realizzazioni intra-fold dei tempi di evento $T_j$. Tuttavia, l'assunzione **non è verificata empiricamente in Parte IV**: la diagnostica formale è rinviata a Parte V (capitolo di calibrazione e diagnostica survival).

**Metodi di verifica empirica rinviati a Parte V.** La verifica empirica dell'assunzione di censoring non-informativo prevista in Parte V comprende: (i) il **test sui residui di Cox-Snell** [Cox e Snell, 1968, *Journal of the Royal Statistical Society B*, 30(2), 248–275] applicati separatamente alle due funzioni di rischio causa-specifica $h_1$ e $h_2$; in assenza di violazioni dell'assunzione e a modello correttamente specificato, i residui di Cox-Snell seguono una distribuzione esponenziale unitaria, verificabile graficamente con un plot della funzione di sopravvivenza cumulativa empirica dei residui contro la diagonale teorica $-\log S$; (ii) la **diagnostica di Schoenfeld stratificata per evento vs censoring** [Grambsch e Therneau, 1994, *Biometrika*, 81(3), 515–526], che esamina la dipendenza dal tempo dei residui di Schoenfeld separatamente per le osservazioni che sperimentano un evento e quelle censurate, individuando deviazioni sistematiche che indicano correlazione residua fra censoring e tempi di evento condizionata sulle covariate. L'esito di tali test sul fold in-sample è registrato nel log di calibrazione del fold; il superamento o la violazione dei test informa la scelta del modello survival da congelare per il fold OOS corrispondente.

**Stima MLE.** Il modello di Cox a rischi concorrenti è stimato via massima verosimiglianza parziale per i parametri $\boldsymbol{\beta}_j$. La baseline hazard $h_{0,j}$ è stimata non parametricamente tramite la stima di Breslow sul campione in-sample del fold. Il seed dell'ottimizzatore è parte del bundle di calibrazione, in coerenza con il determinismo bit-exact di Cap.10 di Parte II.

**Output del fold $k$.** Alla fine della calibrazione del fold $k$, il modello produce i parametri stimati $\{\hat{\boldsymbol{\beta}}_{1,k}, \hat{\boldsymbol{\beta}}_{2,k}, \hat{\gamma}_{1,k}, \hat{\gamma}_{2,k}, \hat{h}_{0,1,k}(\cdot), \hat{h}_{0,2,k}(\cdot)\}$, che vengono congelati e usati per la stima di $\hat{p}_{hit}$ durante il fold OOS corrispondente.

**Diagnostica.** La diagnostica del modello di survival include il test di Schoenfeld per la verifica dell'assunzione di proporzionalità degli hazard (proporzional hazards assumption). Il riferimento metodologico è: **Grambsch e Therneau (1994)** "Proportional Hazards Tests and Diagnostics Based on Weighted Residuals", *Biometrika* 81(3), 515–526. Il risultato della diagnostica è registrato nel log di calibrazione del fold e non blocca automaticamente la procedura, ma segnala la necessità di estendere il modello a hazard non proporzionali in Parte V.

### 19.5 Output operativo e determinismo

**Output principale.** Per ogni segnale candidato all'emissione alla barra $t_{emission}$, il modello di survival produce:

1. La **funzione di survival condizionata** $\hat{S}(\tau \mid \tilde{\mathbf{x}}, T_{residuo})$: la probabilità che al tempo $\tau$ il segnale non sia ancora terminato (né target_1_hit né stopped).
2. La **probabilità di successo** $\hat{p}_{hit}(\tilde{\mathbf{x}}, T_{residuo}, R_{t_{emission}})$: la probabilità cumulativa di incidenza di target_1_hit prima di stopped entro $T_{residuo}$ minuti di trading, consumata dal filtro di emissione di Cap.20.

**Determinismo e causalità.** Il modello di survival soddisfa il vincolo di causalità temporale: il vettore $\tilde{\mathbf{x}}$ contiene esclusivamente feature in $\mathcal{F}_{t_{emission}-1}$; il tempo residuo $T_{residuo}$ è calcolato dalla barra $t_{emission}$ sulla base dell'orario di sessione noto; il modello calibrato è frozen sul fold in-sample precedente. La stima $\hat{p}_{hit}$ è deterministica dato il modello frozen e il vettore di feature: due esecuzioni indipendenti del motore sulla stessa barra producono lo stesso $\hat{p}_{hit}$, in coerenza con il determinismo bit-exact di Cap.10 di Parte II.

---

## Capitolo 20 — Filtri di emissione basati sul survival

### 20.1 Soglia di probabilità minima $\tau_{surv}$

Il segnale viene emesso solo se la stima di probabilità di successo $\hat{p}_{hit}$ prodotta dal modello di survival (Cap.19.5) supera una soglia minima:

$$\hat{p}_{hit}(\tilde{\mathbf{x}}, T_{residuo}, R_{t_{emission}}) \geq \tau_{surv}$$

Il parametro $\tau_{surv} \in (0, 1)$ è un **parametro del cromosoma**, congelato in Parte V. Il dominio è l'intervallo continuo $(0, 1)$; in pratica il GA ottimizza questo parametro nell'intervallo $[0{,}1, 0{,}9]$ (floor e tetto provvisori), con il valore di lavoro $\tau_{surv} = 0{,}5$ (50% di probabilità di successo come soglia minima provvisoria).

Il senso operativo del filtro è escludere segnali per i quali il modello stima che la probabilità di raggiungere target_1 prima dello stop sia troppo bassa. Un $\tau_{surv}$ elevato riduce il numero di segnali emessi ma aumenta la qualità media dei segnali emessi; un $\tau_{surv}$ basso aumenta il numero di segnali ma riduce la qualità media. Il GA ottimizza questo trade-off attraverso la fitness multi-obiettivo (Parte V).

### 20.2 Integrazione AND logico con le condizioni di Cap.8 di Parte II

La condizione survival-based si aggiunge all'AND logico delle condizioni di emissione di Cap.8.3 di Parte II. La regola di emissione completa è:

$$E_{vol}(t_{emission}) \land E_{liq}(t_{emission}) \land E_{dist}^{\sigma}(t_{emission}) \land E_{80pt}(t_{emission}) \land E_{surv}(t_{emission}) = \text{vero}$$

dove $E_{surv}(t_{emission}) = \mathbb{1}[\hat{p}_{hit}(\tilde{\mathbf{x}}, T_{residuo}, R) \geq \tau_{surv}]$.

Il segnale deve soddisfare **tutte** le condizioni simultaneamente. Il filtro survival non sostituisce né indebolisce le condizioni di Cap.8: le condizioni di volatilità $E_{vol}$, liquidità $E_{liq}$ e distanza sigma-units $E_{dist}^{\sigma}$ restano gate hard indipendenti. Il survival aggiunge un layer probabilistico che cattura aspetti del setup — probabilità di raggiungimento del target, interazione tra feature di struttura e probabilità di successo — non catturati dai gate precedenti.

**Interazione con la condizione di distanza sigma-units.** La distanza target-entry $|\texttt{target\_1} - p_{ref}| / \hat{\sigma}_{\text{pt}}$ è inclusa come feature nel vettore $\tilde{\mathbf{x}}$ del survival (Cap.19.3), quindi il survival incorpora parzialmente l'informazione della distanza. Tuttavia, la condizione $E_{dist}^{\sigma}$ resta un gate hard separato: essa filtra segnali con distanza target insufficiente indipendentemente dalla stima probabilistica del survival. La distinzione è architetturale: $E_{dist}^{\sigma}$ è un vincolo deterministico che il cromosoma controlla direttamente tramite $\tau_{dist}^{\sigma}$; $E_{surv}$ è una stima probabilistica che dipende dal modello statistico e dal vettore di feature intero.

### 20.3 Condizionalità al regime

Il parametro $\tau_{surv}$ può essere condizionale al regime $R_{t_{emission}}$, in analogia con la condizionalità di $\tau_{vol}$ (Cap.14.4 di Parte III) e di $d_{stop,\sigma}$ (Cap.18.5):

$$\tau_{surv} = \begin{cases} \tau_{surv,\text{calmo}} & \text{se } R_{t_{emission}} = \text{calmo} \\ \tau_{surv,\text{turbolento}} & \text{se } R_{t_{emission}} = \text{turbolento} \end{cases}$$

I due parametri $\tau_{surv,\text{calmo}}$ e $\tau_{surv,\text{turbolento}}$ sono parametri del cromosoma, congelati in Parte V. Il cromosoma può specificare un unico valore comune o due valori distinti; la scelta è materia della struttura del cromosoma in Parte V.

### 20.4 Filtro implicito di fine sessione via $T_{residuo}$

Il modello di survival condiziona la stima $\hat{p}_{hit}$ al tempo residuo di sessione $T_{residuo}$. Quando $T_{residuo}$ decresce verso zero (fine sessione), la probabilità di raggiungere target_1 prima della scadenza cala sistematicamente:

$$\lim_{T_{residuo} \to 0} \hat{p}_{hit}(\tilde{\mathbf{x}}, T_{residuo}, R) = 0$$

poiché l'integrale della funzione di incidenza cumulativa su un intervallo di durata zero è zero. Questo produce un **filtro implicito di fine sessione**: nelle ultime barre della sessione, il valore $\hat{p}_{hit}$ cala sotto la soglia $\tau_{surv}$ e la condizione $E_{surv}$ diventa falsa, inibendo l'emissione di segnali.

Questo meccanismo è preferibile a un filtro esplicito di tipo "non emettere dopo le ore $H$" per due ragioni: (a) è adattivo — la soglia effettiva di fine-sessione dipende dalla struttura del segnale (distanza target, distanza stop) e dal contesto di mercato (regime, volatilità), non da un orario fisso; (b) è coerente — usa la stessa stima probabilistica che guida tutta la logica di emissione.

Il parametro $T_{min,session}$ di Cap.16.6 funge da vincolo esplicito aggiuntivo che previene la costruzione di zone nelle ultime $T_{min,session}$ barre: è un gate hard che precede la valutazione del survival. Il filtro implicito via $T_{residuo}$ e il gate hard $T_{min,session}$ si complementano: il gate hard previene le barre terminali, il filtro implicito gestisce le barre prossime alla fine sessione in modo adattivo.

---

## Capitolo 21 — Caso trade_range

### 21.1 Definizione del range e classificazione del setup

Il setup di tipo `trade_range` identifica un rettangolo di prezzo in cui il mercato ha oscillato in modo contenuto tra due livelli strutturali opposti senza breakout. La geometria del range è derivata da due pivot strutturali confermati di tipo opposto:

- **pivot high del range**: $p_{high} \in \mathcal{P}_{high}(t_{emission})$ — il massimo strutturale che definisce il bordo superiore del range.
- **pivot low del range**: $p_{low} \in \mathcal{P}_{low}(t_{emission})$ — il minimo strutturale che definisce il bordo inferiore del range.

L'ampiezza del range è:

$$A_{range} = p_{high} - p_{low}$$

espressa in punti FIB, con $A_{range}$ multiplo di 5. Il requisito minimo di ampiezza per l'ammissibilità del setup trade_range è $A_{range} \geq 80$ pt (ereditato da Cap.5 di Parte I e Cap.6.1 di Parte II come eccezione al filtro 80 pt directional), in luogo del vincolo $|\texttt{target\_1} - p_{ref}| \geq 80$ pt dei setup directional.

### 21.2 Regola algoritmica di classificazione directional vs trade_range

La classificazione del setup è deterministica e si basa sulla geometria dei pivot confermati nella sessione corrente alla barra $t_{emission}$.

**Algoritmo di classificazione.** Il motore classifica il setup come `trade_range` se valgono simultaneamente le seguenti condizioni:

1. Esistono almeno un pivot high $p_{high} \in \mathcal{P}_{high}(t_{emission})$ e un pivot low $p_{low} \in \mathcal{P}_{low}(t_{emission})$ con $p_{high} - p_{low} \geq 80$ pt.
2. Il prezzo corrente $p_{t_{emission}-1}$ è all'interno o in prossimità del range $[p_{low}, p_{high}]$: $p_{low} - \epsilon \leq p_{t_{emission}-1} \leq p_{high} + \epsilon$, dove $\epsilon = b$ (la semi-ampiezza della zona) è il margine di prossimità.
3. Il numero di oscillazioni del prezzo all'interno del range $[p_{low}, p_{high}]$ nelle ultime $N_{osc}$ barre è maggiore o uguale a $n_{osc,min}$: $n_{osc}(t_{emission}) \geq n_{osc,min}$, dove $n_{osc}(\cdot)$ è il conteggio formale definito qui sotto. Questa condizione verifica che il range sia "attivo" (il prezzo lo ha percorso più volte) e non un artifact di due pivot isolati. I parametri $N_{osc}$ e $n_{osc,min}$ sono parametri del modello, valori provvisori $N_{osc} = 60$ barre e $n_{osc,min} = 2$ oscillazioni, congelati in Parte V.
4. Non esiste un breakout confermato del range nelle ultime $N_{break}$ barre: nessuna barra 1-min nella finestra $[t_{emission} - N_{break}, t_{emission}]$ ha chiuso al di fuori del range $[p_{low}, p_{high}]$ per più di $\delta_{break}$ punti FIB. Parametri del modello: $N_{break} = 20$ barre e $\delta_{break} = \delta_{pivot} = 10$ pt provvisori, congelati in Parte V.

Se le condizioni 1-4 sono verificate, il setup è classificato `trade_range`; altrimenti è classificato `directional`. La classificazione è deterministica dato lo storico OHLC e i parametri del modello.

**Definizione algoritmica di oscillazione (chiusura NB-2 v2).** Si definisce formalmente *oscillazione del prezzo nel range* $[p_{low}, p_{high}]$ il completamento di un **crossing completo del range** dal bordo inferiore al bordo superiore (o viceversa) sulla sequenza chiusa di barre 1-min, secondo la regola seguente.

Sia $\epsilon$ una **tolleranza di prossimità ai bordi**, parametro provvisorio del modello con valore di lavoro $\epsilon = 5$ pt = 1 tick FIB, congelato in Parte V. Una *barra che tocca il bordo inferiore* alla barra $t_a$ è una barra 1-min chiusa tale che $\mathrm{close}(t_a) \in [p_{low} - \epsilon,\, p_{low} + \epsilon]$; simmetricamente, una *barra che tocca il bordo superiore* è una barra tale che $\mathrm{close}(t_a) \in [p_{high} - \epsilon,\, p_{high} + \epsilon]$. Una *oscillazione completata* è una coppia ordinata di barre $(t_a, t_b)$ con $t_b > t_a$ tale che $t_a$ tocca un bordo e $t_b$ tocca il bordo opposto, e tale che nessuna barra $t_c$ con $t_a < t_c < t_b$ tocchi il bordo opposto a quello di $t_a$ prima di $t_b$. Le due barre $(t_a, t_b)$ definiscono **una sola** oscillazione: tocchi successivi del medesimo bordo dopo $t_a$ e prima di $t_b$ non incrementano il conteggio; analogamente, dopo $t_b$ il conteggio della successiva oscillazione richiede che una nuova barra $t_b' > t_b$ tocchi il bordo opposto a quello di $t_b$.

Formalmente, il conteggio $n_{osc}(t)$ alla barra $t$ sulla finestra $[t - N_{osc} + 1,\, t]$ è calcolato dall'algoritmo seguente, deterministico e causale:

$$
\begin{aligned}
&\text{Input: sequenza chiusa di } \mathrm{close}(s) \text{ per } s \in [t - N_{osc} + 1,\, t-1],\ p_{low},\ p_{high},\ \epsilon. \\
&\text{Init: } n_{osc} \leftarrow 0;\ \text{bordo\_corrente} \leftarrow \texttt{NONE}. \\
&\text{Per ogni } s \text{ da } t - N_{osc} + 1 \text{ a } t - 1: \\
&\quad \text{se } \mathrm{close}(s) \in [p_{low} - \epsilon,\, p_{low} + \epsilon]: \text{ tocco} \leftarrow \texttt{LOW}; \\
&\quad \text{altrimenti se } \mathrm{close}(s) \in [p_{high} - \epsilon,\, p_{high} + \epsilon]: \text{ tocco} \leftarrow \texttt{HIGH}; \\
&\quad \text{altrimenti: } \text{tocco} \leftarrow \texttt{NONE}, \text{ continua al passo successivo}; \\
&\quad \text{se } \text{bordo\_corrente} = \texttt{NONE}: \text{ bordo\_corrente} \leftarrow \text{tocco}; \\
&\quad \text{altrimenti se } \text{tocco} \neq \text{bordo\_corrente}: \\
&\quad\quad n_{osc} \leftarrow n_{osc} + 1;\ \text{bordo\_corrente} \leftarrow \text{tocco}. \\
&\text{Output: } n_{osc}.
\end{aligned}
$$

L'algoritmo è **deterministico** (passa una sola volta sulla finestra, condizioni di confronto univoche), **causale** (consuma esclusivamente $\mathrm{close}(s)$ per $s \leq t - 1$, in coerenza con $\mathcal{F}_{t-1}$), e produce conteggio **bit-exact** identico fra qualsiasi implementazione conforme. Il caso *intervalli di prossimità sovrapposti* ($\epsilon \geq A_{range}/2$) non si verifica per costruzione: la condizione 1 impone $A_{range} \geq 80$ pt e il valore di lavoro $\epsilon = 5$ pt implica $\epsilon \ll A_{range}/2$ in ogni configurazione ammissibile; il vincolo $\epsilon < A_{range}/2$ è dichiarato come ammissibilità implicita del cromosoma quando $\epsilon$ sarà congelato in Parte V.

Esempio numerico (tick FIB = 5 pt, $\epsilon = 5$ pt). Range $[27.400,\, 27.500]$, $N_{osc} = 60$ barre. Sequenza di close (estratti): barra $t-50$ close 27.402 (tocco LOW), barra $t-45$ close 27.450 (NONE, nel mezzo), barra $t-40$ close 27.498 (tocco HIGH, crossing 1 completato, $n_{osc} = 1$), barra $t-30$ close 27.495 (HIGH, stesso bordo, no incremento), barra $t-20$ close 27.403 (tocco LOW, crossing 2 completato, $n_{osc} = 2$), barra $t-10$ close 27.450 (NONE). Conteggio finale $n_{osc}(t) = 2$. Con $n_{osc,min} = 2$, la condizione 3 è soddisfatta.

**Selezione dei pivot del range.** Quando più coppie $(p_{high}, p_{low})$ soddisfano le condizioni 1-4, si seleziona la coppia che massimizza $A_{range}$ tra le coppie con i pivot più recenti: si prendono il pivot high più recente e il pivot low più recente soddisfacenti le condizioni.

**Coerenza con il contratto del segnale.** La classificazione `setup_class \in \{\text{directional}, \text{trade\_range}\}` è un campo del payload $\mathcal{S}$ (Cap.6.1 di Parte II), immutabile dopo l'emissione. La regola di classificazione qui formalizzata è l'algoritmo deterministico che produce questo campo.

### 21.3 Geometria della zona di entry nel range

Per il setup `trade_range`, la zona di entry è costruita ai bordi del range, in accordo con la logica di mean-reversion: si entra in acquisto quando il prezzo tocca il bordo inferiore del range (attesa di rimbalzo verso il bordo superiore), e in vendita quando il prezzo tocca il bordo superiore (attesa di ritorno verso il bordo inferiore).

- **Segnale long trade_range**: $p_{ref} = p_{low}$, la zona è costruita attorno al bordo inferiore del range: $\texttt{entry\_zone} = [p_{low} - b, p_{low} + b]$.
- **Segnale short trade_range**: $p_{ref} = p_{high}$, la zona è costruita attorno al bordo superiore del range: $\texttt{entry\_zone} = [p_{high} - b, p_{high} + b]$.

La semi-ampiezza $b$ è lo stesso parametro del cromosoma del caso directional ($b \in \{5, 10, 15, 20, 25, 30, 35, 40\}$ pt). Il vincolo $d_{stop} > b$ si applica anche al trade_range.

### 21.4 Target e stop nel range

**target_1 nel trade_range.** Per il setup trade_range, il target_1 è il bordo opposto del range:

- **Segnale long trade_range**: $\texttt{target\_1} = p_{high}$, il bordo superiore del range.
- **Segnale short trade_range**: $\texttt{target\_1} = p_{low}$, il bordo inferiore del range.

Questa scelta riflette la logica mean-reverting del trade_range: il target è il bordo opposto del rettangolo di prezzo. La distanza target è $|\texttt{target\_1} - p_{ref}| = A_{range}$. Poiché la condizione di ammissibilità del trade_range impone $A_{range} \geq 80$ pt (Cap.21.1), il vincolo 80 pt è automaticamente soddisfatto per i setup trade_range, e il target non deve superare una verifica aggiuntiva del vincolo directional.

**target_2 nel trade_range.** Il target_2 per il trade_range è un livello strutturale oltre il bordo opposto del range: si applica l'algoritmo di selezione di Cap.17.4 partendo da $\texttt{target\_1}$ come riferimento. Se non esistono pivot strutturali confermati oltre il bordo opposto del range, si utilizza il livello sintetico di Cap.17.4 con parametro $k_{t2}$.

**stop_loss nel trade_range.** Lo stop è fuori dal range nella direzione avversa:

- **Segnale long trade_range**: lo stop è sotto il bordo inferiore del range: $\texttt{stop\_loss} < p_{low} - b$ (soddisfa il vincolo $d_{stop} > b$ per costruzione se $\texttt{stop\_loss} < p_{low} - b$).
- **Segnale short trade_range**: lo stop è sopra il bordo superiore del range: $\texttt{stop\_loss} > p_{high} + b$.

La derivazione dello stop segue l'algoritmo di Cap.18.1: si cerca il pivot strutturale al di fuori del range nella direzione avversa; in assenza, si usa il candidato sigma con $d_{stop,\sigma}$ parametro del cromosoma. Il vincolo $d_{stop} > b$ è verificato per entrambi i candidati (Cap.18.2).

Esempio numerico (tick FIB = 5 pt): range $[27.400, 27.500]$ ($A_{range} = 100$ pt ≥ 80 pt), segnale long, $b = 15$ pt. Zona di entry: $[27.385, 27.415]$. target_1 = 27.500. Se il pivot low più distante sotto il range è 27.360: $d_{stop} = 27.400 - 27.360 = 40$ pt > 15 pt ($b$), vincolo rispettato. Stop_loss = 27.360.

### 21.5 Survival nel trade_range

**Estensione locale del catalogo causale — feature condizionale (chiusura O-4 / M-13 v2).** Il modello survival per il regime trade_range usa un'**estensione locale del catalogo causale** con la feature condizionale $x^{(A_{range})}$ definita più sotto, attiva **esclusivamente quando lo stato di mercato è classificato `trade_range`** (Cap.21.2 della presente Parte IV; classificazione di regime di Cap.14 di Parte III). Il **catalogo globale del cromosoma per il regime directional resta a 37 feature** (Cap.15.2 di CAP-03 invariato): la feature aggiuntiva non è inclusa nel catalogo principale e non incrementa la dimensionalità del vettore $\tilde{\mathbf{x}}$ del survival in regime directional. La scelta di trattare $x^{(A_{range})}$ come feature condizionale al regime — anziché come 38-esima feature del catalogo — preserva la coerenza con CAP-03 e impedisce l'introduzione di rumore strutturale (valori non definiti) nel survival directional, dove il range non esiste.

Il modello di survival di Cap.19 opera in modo identico per il setup trade_range e per il setup directional, con un'unica differenza nel vettore di feature in input. Per il setup trade_range il vettore $\tilde{\mathbf{x}}_{\text{trade\_range}}$ è ottenuto estendendo localmente il vettore directional $\tilde{\mathbf{x}}$ con la feature condizionale

$$x^{(A_{range})} = \frac{A_{range}}{\hat{\sigma}_{\text{pt}}(t_{emission})}$$

espressa in sigma-units FIB, normalizzata per coerenza con il dominio delle feature del catalogo (analoga alla distanza target in sigma-units). Questa feature cattura la dimensione relativa del range rispetto alla volatilità corrente: un range di 100 pt in regime di alta volatilità ($\hat{\sigma}_{\text{pt}} = 50$ pt) ha un'ampiezza relativa di 2 sigma; in regime di bassa volatilità ($\hat{\sigma}_{\text{pt}} = 15$ pt) l'ampiezza relativa è circa 6{,}7 sigma.

La stima $\hat{p}_{hit}$ prodotta per il trade_range è la probabilità di raggiungere il bordo opposto del range prima dello stop, condizionata su $\tilde{\mathbf{x}}_{\text{trade\_range}}$ (con la feature aggiuntiva $x^{(A_{range})}$), $T_{residuo}$ e $R_{t_{emission}}$. Il filtro survival-based di Cap.20 si applica al trade_range con la stessa soglia $\tau_{surv}$ (o i suoi valori condizionali per regime). Il modello di Cox cause-specific (Cap.19.2) è calibrato sulle osservazioni di setup trade_range del fold in-sample con il vettore esteso; il modello di Cox per il setup directional è calibrato sulle osservazioni directional con il vettore originario a $K \leq 37$ feature. La selezione effettiva del sottoinsieme di feature in ciascun modello è materia del cromosoma (Parte V).

---

## Riepilogo dei parametri provvisori della Parte IV

Tutti i valori numerici proposti in questa Parte sono provvisori e rinviati al congelamento empirico in Parte V sulla base dello storico Portara/CQG FIB 1-min, in coerenza con Q-03 di CAP-01.

| Parametro | Dominio | Valore provvisorio | Tipo | Capitolo |
|-----------|---------|-------------------|------|----------|
| $d_{inv}$ — soglia di allontanamento dalla zona (invalidazione I2) | Multipli di 5 pt, $\geq 5$ | 30 pt | Cromosoma | Cap.16.5 |
| $d_{obsolete}$ — soglia di obsolescenza pivot (invalidazione I3) | Multipli di 5 pt, $\geq 5$ | 20 pt | Cromosoma | Cap.16.5 |
| $T_{min,session}$ — tempo residuo minimo di sessione per emissione | Interi positivi (min trading), $\geq 15$ | 30 min | Cromosoma | Cap.16.6 |
| $k_{t2}$ — moltiplicatore sigma per target_2 sintetico | $\mathbb{R}^+$ | 2{,}0 | Cromosoma | Cap.17.4 |
| $d_{stop,\sigma}$ — moltiplicatore sigma per stop sintetico | $\mathbb{R}^+$ | 3{,}0 | Cromosoma | Cap.18.1 |
| $d_{stop,\sigma,\text{calmo}}$, $d_{stop,\sigma,\text{turbolento}}$ — variante regime-dipendente | $\mathbb{R}^+$ | — | Cromosoma (opzionale) | Cap.18.5 |
| $\tau_{surv}$ — soglia probabilità survival | $(0{,}1;\,0{,}9)$ | 0{,}5 | Cromosoma | Cap.20.1 |
| $\tau_{surv,\text{calmo}}$, $\tau_{surv,\text{turbolento}}$ — variante regime-dipendente | $(0{,}1;\,0{,}9)$ | — | Cromosoma (opzionale) | Cap.20.3 |
| $N_{osc}$ — finestra barre per conteggio oscillazioni nel range | Intero positivo | 60 barre | Modello | Cap.21.2 |
| $n_{osc,min}$ — oscillazioni minime nel range | Intero positivo | 2 | Modello | Cap.21.2 |
| $\epsilon$ — tolleranza di prossimità ai bordi del range per conteggio oscillazioni | Multipli di 5 pt, $\geq 5$, $< A_{range}/2$ | 5 pt (= 1 tick FIB) | Modello | Cap.21.2 |
| $N_{break}$ — finestra barre per rilevazione breakout | Intero positivo | 20 barre | Modello | Cap.21.2 |
| $\delta_{break}$ — soglia breakout | Multipli di 5 pt | 10 pt (= $\delta_{pivot}$) | Modello | Cap.21.2 |

I parametri ereditati da Parte III e già dichiarati provvisori in quella sede ($n_c$, $\delta_{pivot}$, $T_{warmup,\text{EMA}}$, $T_{warmup,\text{norm}}$, $W$, $p$, $N_{reg}$, $T_{persist}$, $N_{pivot}$, $W_{norm}$, $\lambda$) non sono duplicati in questa tabella: rimangono soggetti al congelamento in Parte V come dichiarato in Parte III.

---

*Fine della Parte IV. Le definizioni geometriche delle zone di entry (Cap.16), dei target strutturali (Cap.17), degli stop strutturali (Cap.18), del modello di survival (Cap.19), dei filtri di emissione survival-based (Cap.20) e della geometria trade_range (Cap.21) sono ora formalmente specificate e pronte per essere consumate dalla Parte V (cromosoma, struttura del genoma, fitness multi-obiettivo). Il cromosoma di Parte V parametrizza i gradi di libertà geometrici definiti in questa Parte: $b$, $d_{inv}$, $d_{obsolete}$, $T_{min,session}$, $k_{t2}$, $d_{stop,\sigma}$ (e le varianti regime-dipendenti), $\tau_{surv}$ (e le varianti regime-dipendenti). Il modello di survival è calibrato fold-per-fold in coerenza con la procedura di walk-forward di Parte V, su feature derivate dal catalogo di Parte III. Il caso trade_range è trattato con la stessa architettura geometrica e probabilistica del caso directional, con l'eccezione del filtro 80 pt che si applica all'ampiezza del range $A_{range}$ anziché alla distanza target.*
