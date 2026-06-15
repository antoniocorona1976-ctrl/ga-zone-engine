# SPEC_FUNZ_01_B2 — Payload del segnale

> **Track**: Business-spec (SPEC-FUNZ). **Blocco**: 2 di 8 (B2) della spec funzionale ricostruita a blocchi. **Sede ciclo**: CLI. **Tag commit**: `[SPEC-FUNZ-01-B2]`.
>
> Documento **autonomo**: copre il *payload del segnale* come oggetto contrattuale immutabile. Sarà ricomposto con gli altri 7 blocchi in un'unica spec consolidata da un task di assemblaggio dedicato **dopo B8** (assemblaggio fuori scope di B2).

---

## 1. Intestazione e scopo del blocco

### 1.1 Cosa copre B2

B2 specifica **il payload del segnale FIB come oggetto-dato contrattuale e immutabile**: l'insieme dei campi che compongono la tupla del segnale pubblicato, il dominio e i vincoli di ciascun campo, e le proprietà invarianti che il payload deve soddisfare (immutabilità post-emissione; segnale unico attivo e sostituzione-non-edit). B2 **non** copre il ciclo di vita del segnale (state machine, stati terminali, raw touch come evento, semantica dei timer), le condizioni di emissione, il contratto Telegram, il log/replay, né la submacchina del position lifecycle: questi sono materia di blocchi successivi (vedi §8, nota di rinvio).

### 1.2 Fonte e pin

Fonte unica e autoritativa di B2: `docs/methodology_v2/CAP_02_parte_II.md` ("Parte II — Contratto del segnale FIB"), **Capitolo 6 (Schema del segnale e invarianti), sezioni 6.1 / 6.2 / 6.3**, più il preambolo della Parte II per i richiami strutturali allo strumento.

- **CAP-02 è chiuso PASS con SHA `a1625df`**; capitolo congelato (freeze G-09), citato in sola lettura.
- Grafia di citazione: `[DOC-INTERNO CAP_02_parte_II.md:<riga>]`.

### 1.3 Schema ID requisito (auto-assegnato)

Lo schema ID di questo blocco è **locale e autonomo**, numerato da zero:

- **`B2-R-NN`** — requisiti di schema-payload (campo, dominio, vincolo funzionale, ordinamento).
- **`B2-CN-NN`** — requisiti **invarianti / strutturali / di compliance contrattuale** (immutabilità, segnale unico attivo, sostituzione-non-edit, vincolo geometrico $d_{stop}>b$).

Ogni requisito è **atomico** (una sola proposizione verificabile), **tracciato** ad almeno una riga del Cap.6, e dichiara il proprio **valore operativo** per l'operatore retail FIB che riceve ed esegue manualmente il segnale da cellulare.

---

## 2. Il segnale come oggetto-payload immutabile

Il segnale emesso dal motore è una **tupla strutturata $\mathcal{S}$**, completa, che descrive in modo esaustivo l'ipotesi operativa pubblicata all'operatore, ed è **congelata al momento dell'emissione** `[DOC-INTERNO CAP_02_parte_II.md:17]`. La tupla è composta dai campi:

$$\mathcal{S} = \big(\texttt{signal\_id},\ \texttt{timestamp\_emission},\ \texttt{direction},\ \texttt{entry\_zone},\ \texttt{target\_1},\ \texttt{target\_2},\ \texttt{target\_2\_type},\ \texttt{stop\_loss},\ \texttt{stop\_type},\ \texttt{setup\_class},\ \Delta t_{cromosoma},\ T_{touch}^{max}\big)$$

`[DOC-INTERNO CAP_02_parte_II.md:19]`

Questa sezione consolida la natura del payload come oggetto-dato. Il *ciclo di vita* della tupla (gli stati che il segnale attraversa, gli eventi che ne provocano la chiusura) **non** è materia di B2.

**B2-R-01** — Il payload del segnale è una **tupla strutturata $\mathcal{S}$** composta esattamente dai dodici campi `signal_id`, `timestamp_emission`, `direction`, `entry_zone`, `target_1`, `target_2`, `target_2_type`, `stop_loss`, `stop_type`, `setup_class`, $\Delta t_{cromosoma}$, $T_{touch}^{max}$.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:17, :19]`.
- *Valore operativo*: l'operatore riceve un oggetto unico e completo con tutti i parametri necessari alla decisione di ingresso, senza dover integrare informazioni da fonti esterne; un payload a struttura fissa rende la lettura mobile prevedibile (sempre gli stessi campi nello stesso ruolo).

---

## 3. Campi del payload (schema-dato)

### 3.1 `signal_id`

**B2-R-02** — `signal_id` è l'**identificatore univoco** del segnale, assegnato dal motore all'emissione, e funge da chiave primaria del segnale.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:23]`.
- *Valore operativo*: dà all'operatore una chiave non ambigua con cui riconoscere a quale segnale si riferiscono le successive comunicazioni; senza una chiave univoca l'operatore non potrebbe distinguere un segnale da un altro nella cronologia.

**B2-R-03** — `signal_id` è un valore **opaco non riutilizzabile**.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:23]`.
- *Valore operativo*: la non-riusabilità garantisce che lo stesso identificatore non torni mai a designare un secondo segnale diverso; l'operatore non rischia di confondere un vecchio segnale con uno nuovo che ne riusi la chiave.

**B2-R-04** — L'unicità di `signal_id` è garantita sull'**intero orizzonte operativo del motore**, non soltanto sulla sessione corrente.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:23]`.
- *Valore operativo*: anche a distanza di giorni o mesi un `signal_id` resta una chiave non collidente; le tracce storiche sul cellulare dell'operatore restano riferibili senza ambiguità a un singolo segnale.

### 3.2 `timestamp_emission`

**B2-R-05** — `timestamp_emission` è l'**istante di emissione** del segnale, espresso **al minuto chiuso**.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:25]`.
- *Valore operativo*: comunica all'operatore quanto è "fresco" il segnale rispetto al momento in cui lo legge sul cellulare; la precisione al minuto è coerente con la granularità (barre 1-min) su cui il segnale è calcolato.

**B2-R-06** — Il riferimento orario di `timestamp_emission` è **CET**.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:25]`.
- *Valore operativo*: fissa un fuso univoco; l'operatore italiano legge l'orario nel proprio fuso locale senza conversioni, evitando errori di interpretazione temporale sul momento di emissione.

### 3.3 `direction`

**B2-R-07** — `direction` ha dominio $\{\text{long}, \text{short}\}$.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:27]`.
- *Valore operativo*: è l'informazione che dice all'operatore se comprare o vendere; un dominio binario chiuso elimina ogni ambiguità sul verso dell'operazione da inviare al broker.

### 3.4 `entry_zone` e banda di ingresso

(Il dominio e la cardinalità della semi-ampiezza $b$ sono trattati in dettaglio al §4; qui si fissa `entry_zone` come campo.)

**B2-R-08** — `entry_zone` è una **banda di prezzo discreta** attorno al prezzo strutturale di riferimento $p_{ref}$, definita come insieme dei livelli $\{p_{ref}-b,\ p_{ref}-b+5,\ \ldots,\ p_{ref}+b-5,\ p_{ref}+b\}$.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:29, :31]`.
- *Valore operativo*: dice all'operatore l'intervallo di prezzo entro cui posizionarsi per l'ingresso; esprimerla come insieme di livelli discreti (anziché come fascia continua) è coerente con il fatto che i prezzi del FIB esistono solo a multipli di 5, così l'operatore lavora su livelli realmente quotabili.

**B2-R-09** — Il prezzo di riferimento $p_{ref}$ è **multiplo di 5** ed è **fissato al momento dell'emissione**.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:33]`.
- *Valore operativo*: ancora la banda a un livello realmente quotabile sul FIB e ne fissa il centro all'emissione, così l'operatore sa che il riferimento non si muove dopo la pubblicazione.

### 3.5 `target_1` e `target_2`

**B2-R-10** — `target_1` è un **prezzo strutturale di obiettivo**, **obbligatorio**.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:35]`.
- *Valore operativo*: dà all'operatore il primo livello di presa di profitto; la sua obbligatorietà garantisce che ogni segnale arrivi con un obiettivo esplicito, non aperto.

**B2-R-11** — `target_2` è un **prezzo strutturale di obiettivo**, **obbligatorio**.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:35]`.
- *Valore operativo*: dà all'operatore un secondo livello di riferimento strutturale per gestire la posizione oltre il primo obiettivo; la sua obbligatorietà garantisce che sia sempre pubblicato.

**B2-R-12** — `target_1` e `target_2` sono **distinti** (valori diversi).
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:35]`.
- *Valore operativo*: due livelli distinti danno all'operatore due riferimenti di prezzo separati; la distinzione evita un payload degenere in cui i due obiettivi coincidano, privando il secondo target di significato.

**B2-R-13** — `target_1` è **multiplo di 5**.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:35]`.
- *Valore operativo*: l'obiettivo è espresso a un livello realmente quotabile sul FIB, immediatamente impostabile dall'operatore come ordine limite.

**B2-R-14** — `target_2` è **multiplo di 5**.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:35]`.
- *Valore operativo*: il secondo obiettivo è espresso a un livello realmente quotabile sul FIB, coerente con la granularità dello strumento.

**B2-R-15** — Per i segnali **long** vale l'ordine $\texttt{target\_1} > p_{ref}$.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:35]`.
- *Valore operativo*: per un long il primo obiettivo è sopra il riferimento; l'operatore vede coerenza fra il verso dell'operazione e la posizione dell'obiettivo, riducendo il rischio di errori di lettura.

**B2-R-16** — Per i segnali **long** vale l'ordine $\texttt{target\_2} > \texttt{target\_1}$.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:35]`.
- *Valore operativo*: per un long il secondo obiettivo è più lontano del primo nella direzione del profitto; l'operatore ha un ordine di presa di profitto crescente e prevedibile.

**B2-R-17** — Per i segnali **short** vale l'ordine $\texttt{target\_1} < p_{ref}$.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:35]`.
- *Valore operativo*: per uno short il primo obiettivo è sotto il riferimento; coerenza immediata fra verso dell'operazione e posizione dell'obiettivo.

**B2-R-18** — Per i segnali **short** vale l'ordine $\texttt{target\_2} < \texttt{target\_1}$.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:35]`.
- *Valore operativo*: per uno short il secondo obiettivo è più lontano del primo verso il basso; presa di profitto ordinata e prevedibile nel verso corretto.

**B2-R-19** — `target_1` e `target_2` sono entrambi **ancorati a livelli strutturali** del prezzo (non sono obiettivi arbitrari non strutturali).
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:35]`.
- *Valore operativo*: gli obiettivi pubblicati corrispondono a livelli che il prezzo riconosce strutturalmente; l'operatore opera su riferimenti dotati di significato di mercato, non su numeri tirati a caso.

**B2-R-20** — `target_2` è **informazione strutturale pubblicata**, non variabile di lifecycle del segnale: è un attributo informativo del payload, mentre il contratto del segnale si chiude al raggiungimento di `target_1` (Q-05, Clausola 2).
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:37]` (decisione Q-05 al `:7`).
- *Valore operativo*: l'operatore riceve `target_2` come secondo riferimento decisionale per gestire manualmente la posizione oltre il primo obiettivo, sapendo che è un'informazione strutturale e non un secondo "trade" gestito dal motore. *(L'eventuale raggiungimento di target_2 come **evento** del position lifecycle è materia di blocco successivo — vedi §8.)*

### 3.6 `target_2_type`

**B2-R-21** — `target_2_type` è un **campo del payload** con dominio $\{\text{structural}, \text{synthetic}\}$, che qualifica la natura del livello `target_2` pubblicato.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:39]`.
- *Valore operativo*: dice all'operatore se il secondo obiettivo poggia su una struttura confermata del prezzo o è un livello calcolato; informazione utile per pesare quanta fiducia dare al secondo target in lettura mobile.

**B2-R-22** — Nel campo `target_2_type`, il valore `synthetic` ha **natura informativa derivata da una regola del modello** (livello calcolato), distinta dal valore `structural` che indica un livello derivato da struttura confermata del prezzo.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:39]`.
- *Valore operativo*: rende esplicito all'operatore che un `target_2` `synthetic` è meno "ancorato" di uno `structural`; l'operatore può modulare la propria gestione manuale della posizione di conseguenza.

### 3.7 `stop_loss`

**B2-R-23** — `stop_loss` è un **prezzo strutturale di stop**, **multiplo di 5**.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:41]`.
- *Valore operativo*: dà all'operatore il livello di protezione della posizione a un prezzo realmente quotabile sul FIB, immediatamente impostabile come stop.

**B2-R-24** — Si definisce la distanza dello stop dal riferimento come $d_{stop} = |p_{ref} - \texttt{stop\_loss}|$, in punti FIB.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:43]`.
- *Valore operativo*: quantifica per l'operatore l'ampiezza del rischio (distanza dal riferimento allo stop), grandezza centrale per dimensionare mentalmente la perdita massima attesa per contratto.

*(Il vincolo geometrico $d_{stop}>b$ è reso come requisito invariante — vedi B2-CN-01 al §3.10.)*

### 3.8 `stop_type`

**B2-R-25** — `stop_type` è un **campo del payload** con dominio $\{\text{structural}, \text{synthetic}\}$, che qualifica la natura del livello `stop_loss` pubblicato.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:51]`.
- *Valore operativo*: dice all'operatore se lo stop poggia su una struttura confermata del prezzo o è un livello calcolato; informazione utile per valutare la robustezza del livello di protezione in lettura mobile.

**B2-R-26** — Nel campo `stop_type`, il valore `synthetic` ha **natura informativa derivata da una regola del modello**, distinta dal valore `structural` che indica un livello derivato da struttura confermata del prezzo.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:51]`.
- *Valore operativo*: rende esplicito all'operatore che uno `stop_loss` `synthetic` è derivato da una regola del modello e non da una struttura confermata; l'operatore valuta la natura del proprio livello di protezione.

**B2-R-27** — Il dominio di `stop_type` **non** include valori prodotti dall'operatore: il motore **non gestisce stop manuali**.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:51]`.
- *Valore operativo*: chiarisce il confine di responsabilità — lo stop nel payload è quello strutturale del motore; l'operatore sa che ogni stop personale che decidesse di adottare è fuori dal contratto del segnale e di sua esclusiva responsabilità.

### 3.9 `setup_class`

**B2-R-28** — `setup_class` è un **campo del payload** con dominio $\{\text{directional}, \text{trade\_range}\}$, che classifica la natura del setup.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:53]`.
- *Valore operativo*: dice all'operatore di che tipo di setup si tratta (movimento direzionale vs operatività entro un range), informazione di contesto per la lettura del segnale.

**B2-R-29** — A ciascun valore di `setup_class` è **associato un filtro di emissione di 80 punti FIB** (per `directional`: $|\texttt{target\_1} - p_{ref}| \geq 80$; per `trade_range`: $A_{range} \geq 80$).
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:53, :55, :59]`.
- *Valore operativo*: garantisce all'operatore che ogni segnale pubblicato abbia un'ampiezza minima significativa (almeno 80 punti), così che un fill valga il costo operativo (commissioni, attenzione); il filtro qualifica il campo `setup_class`. *(La **regola di emissione** che applica questo filtro — il quando e il come l'emissione viene bloccata — è materia di blocco successivo; vedi §8. La definizione operativa di $A_{range}$ è in Parte IV, fuori B2.)*

### 3.10 $\Delta t_{cromosoma}$ e $T_{touch}^{max}$ (campi/parametri del payload)

**B2-R-30** — $\Delta t_{cromosoma}$ è un **campo/parametro del payload** di dominio discreto intero $\{1, 2, \ldots, 1680\}$ minuti di trading.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:63]`.
- *Valore operativo*: è il parametro che fissa la durata massima della fase post-trigger del segnale; pur essendo un parametro tecnico, fa parte integrante del payload congelato e quindi del contratto del segnale che l'operatore riceve. *(La **semantica del timer** — decorrenza dal raw touch, scadenza → stato terminale, conteggio sui soli minuti di trading — è materia di blocco successivo; vedi §8.)*

**B2-R-31** — $T_{touch}^{max}$ è un **campo/parametro del payload** di dominio discreto intero $\{5, 6, \ldots, 480\}$ minuti di trading.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:69]`.
- *Valore operativo*: è il parametro che fissa la durata massima della fase di attesa pre-trigger del segnale; fa parte del payload congelato e quindi del contratto del segnale. *(La **semantica del timer** — decorrenza dall'emissione, scadenza → stato terminale, conteggio sui soli minuti di trading — è materia di blocco successivo; vedi §8.)*

---

## 4. Banda di ingresso $b$

**B2-R-32** — La semi-ampiezza della banda $b$ ha **dominio discreto** $\{5, 10, 15, 20, 25, 30, 35, 40\}$ punti FIB (cardinalità 8).
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:33]` (preambolo `:5`, `:9`).
- *Valore operativo*: definisce l'insieme finito di ampiezze possibili della zona di ingresso; un dominio chiuso e discreto rende prevedibile per l'operatore quanto "larga" possa essere al massimo una zona di ingresso (al più 40 punti per lato).

**B2-R-33** — La semi-ampiezza $b$ è **multipla di 5** (punti FIB), coerentemente col tick dello strumento.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:9, :33]`.
- *Valore operativo*: i bordi della banda cadono su livelli realmente quotabili sul FIB; l'operatore lavora su prezzi effettivamente disponibili a mercato.

**B2-R-34** — Il valore minimo $b_{min} = 5$ punti FIB corrisponde esattamente a **1 tick** del FIB.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:9, :33]`.
- *Valore operativo*: stabilisce la zona di ingresso più stretta possibile come un singolo tick di larghezza per lato; l'operatore sa che la banda minima non è mai nulla, c'è sempre almeno un livello operabile.

**B2-R-35** — `entry_zone` è l'**insieme discreto** dei livelli multipli di 5 da $p_{ref}-b$ a $p_{ref}+b$ a passo 5.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:29, :31]`.
- *Valore operativo*: l'operatore vede esattamente quali livelli di prezzo costituiscono la zona, tutti realmente quotabili; non c'è ambiguità su cosa "conti" come ingresso valido.

**B2-R-36** — La **cardinalità** della banda è $(2b/5) + 1$ livelli discreti.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:33]`.
- *Valore operativo*: rende calcolabile e prevedibile quanti livelli compongono la zona per ogni $b$; informazione coerente con la natura discreta dei prezzi FIB su cui l'operatore opera.

**B2-R-37** — Il floor $b_{min}=5$ esiste per **evitare una banda di ingresso nulla** (convergenza del modello su zone a banda zero).
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:33]`.
- *Valore operativo*: garantisce all'operatore che ogni segnale arrivi con una zona di ingresso effettivamente operabile (mai a larghezza zero), preservando l'azionabilità del segnale.

---

## 5. Invariante di payload immutabile

**B2-CN-02** *(invariante strutturale)* — Una volta emesso, il segnale identificato da `signal_id` **non subisce alcuna modifica al proprio payload**: la tupla $\mathcal{S}$ è **congelata al momento dell'emissione**.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:73]`.
- *Valore operativo*: l'operatore che legge il segnale sul cellulare opera su valori che non cambiano fra il momento della lettura e quello dell'invio dell'ordine; nessun parametro muta a sua insaputa.

**B2-CN-03** *(invariante strutturale)* — **Non esiste** un'operazione di refresh o di edit del segnale che lasci invariato `signal_id` e modifichi uno qualsiasi dei campi del payload.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:73]`.
- *Valore operativo*: a parità di `signal_id` l'operatore ha la garanzia assoluta che i valori siano sempre quelli pubblicati; la chiave del segnale identifica un contenuto immutabile, eliminando il rischio di operare su dati silenziosamente cambiati.

---

## 6. Segnale unico attivo e sostituzione come proprietà del payload

**B2-CN-04** *(invariante strutturale)* — Vale il vincolo **segnale unico attivo**: $|\mathcal{A}(t)| \leq 1$ per ogni $t$ (al massimo un solo segnale attivo a ogni istante), dove $\mathcal{A}(t)$ è l'insieme dei segnali attivi al tempo $t$.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:79, :81]`.
- *Valore operativo*: l'operatore ha al più un segnale operabile per volta, coerente con l'operatività a 1 contratto alla volta; nessuna sovrapposizione di segnali concorrenti da gestire manualmente sul cellulare.

**B2-CN-05** *(invariante strutturale)* — Una "revisione" del segnale **non è un edit** del payload esistente: il motore emette un **nuovo `signal_id`** con una **nuova tupla $\mathcal{S}'$ completa e indipendente**, anch'essa congelata.
- *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:77, :83]`.
- *Valore operativo*: quando le condizioni cambiano l'operatore riceve un segnale nuovo e riconoscibile (nuova chiave, nuovo payload completo) invece di un aggiornamento silenzioso del precedente; sa sempre se sta guardando un segnale nuovo o uno già visto. *(La **meccanica delle transizioni di stato** della sostituzione — revoca del segnale precedente, stati terminali, state machine — è materia di blocco successivo; vedi §8.)*

---

## 7. Nota RM-1 — aderenza alla fonte

Tutti i requisiti di B2 sono **richiami** a fatti già asseriti e chiusi nel Cap.6 di `CAP_02_parte_II.md` (CAP-02 PASS `a1625df`, frozen): B2 **non** introduce dichiarazioni "verificato X" di prima istanza su sistemi esterni. Nessuna fonte esterna `[WIKI-HINT]` è usata in questo blocco (il payload è materia interna del contratto del segnale). Pertanto non è stato necessario applicare la formula RM-1 a 4 righe ad alcun requisito: ogni proposizione resta entro ciò che il CAP-fonte afferma.

---

## 8. Matrice di tracciabilità + nota di rinvio

### 8.1 Matrice di tracciabilità

| ID | Proposizione (sintesi) | Citazione `CAP_02_parte_II.md` | Valore operativo (sintesi) |
|----|------------------------|-------------------------------|----------------------------|
| B2-R-01 | Payload = tupla $\mathcal{S}$ di 12 campi | :17, :19 | oggetto unico e completo per la decisione |
| B2-R-02 | `signal_id` identificatore univoco | :23 | chiave non ambigua del segnale |
| B2-R-03 | `signal_id` opaco non riutilizzabile | :23 | nessuna confusione fra segnali |
| B2-R-04 | unicità su intero orizzonte operativo | :23 | tracce storiche riferibili senza ambiguità |
| B2-R-05 | `timestamp_emission` al minuto chiuso | :25 | freschezza del segnale |
| B2-R-06 | `timestamp_emission` in CET | :25 | fuso univoco, niente conversioni |
| B2-R-07 | `direction` $\in\{$long,short$\}$ | :27 | verso operazione non ambiguo |
| B2-R-08 | `entry_zone` banda discreta attorno a $p_{ref}$ | :29, :31 | intervallo di ingresso operabile |
| B2-R-09 | $p_{ref}$ multiplo di 5, fissato all'emissione | :33 | centro quotabile e stabile |
| B2-R-10 | `target_1` obbligatorio | :35 | primo obiettivo esplicito |
| B2-R-11 | `target_2` obbligatorio | :35 | secondo riferimento sempre presente |
| B2-R-12 | `target_1` ≠ `target_2` (distinti) | :35 | due riferimenti separati |
| B2-R-13 | `target_1` multiplo di 5 | :35 | obiettivo quotabile |
| B2-R-14 | `target_2` multiplo di 5 | :35 | obiettivo quotabile |
| B2-R-15 | long: `target_1` > $p_{ref}$ | :35 | coerenza verso/obiettivo |
| B2-R-16 | long: `target_2` > `target_1` | :35 | presa profitto ordinata |
| B2-R-17 | short: `target_1` < $p_{ref}$ | :35 | coerenza verso/obiettivo |
| B2-R-18 | short: `target_2` < `target_1` | :35 | presa profitto ordinata |
| B2-R-19 | target ancorati a livelli strutturali | :35 | obiettivi con significato di mercato |
| B2-R-20 | `target_2` informazione strutturale pubblicata (Q-05 Cl.2) | :37 (:7) | secondo riferimento decisionale |
| B2-R-21 | `target_2_type` $\in\{$structural,synthetic$\}$ | :39 | natura del 2° obiettivo |
| B2-R-22 | `synthetic` = livello calcolato (vs `structural`) | :39 | quanta fiducia dare al target |
| B2-R-23 | `stop_loss` strutturale, multiplo di 5 | :41 | protezione a livello quotabile |
| B2-R-24 | $d_{stop}=|p_{ref}-\texttt{stop\_loss}|$ | :43 | misura del rischio |
| B2-R-25 | `stop_type` $\in\{$structural,synthetic$\}$ | :51 | natura dello stop |
| B2-R-26 | `synthetic` = livello calcolato (vs `structural`) | :51 | robustezza dello stop |
| B2-R-27 | dominio `stop_type` esclude stop dell'operatore | :51 | confine di responsabilità |
| B2-R-28 | `setup_class` $\in\{$directional,trade_range$\}$ | :53 | tipo di setup |
| B2-R-29 | a `setup_class` associato filtro 80pt | :53, :55, :59 | ampiezza minima significativa |
| B2-R-30 | $\Delta t_{cromosoma}\in\{1,\ldots,1680\}$ | :63 | durata max fase post-trigger |
| B2-R-31 | $T_{touch}^{max}\in\{5,\ldots,480\}$ | :69 | durata max attesa pre-trigger |
| B2-R-32 | $b\in\{5,\ldots,40\}$ discreto (card. 8) | :33 (:5,:9) | ampiezze possibili della zona |
| B2-R-33 | $b$ multiplo di 5 | :9, :33 | bordi quotabili |
| B2-R-34 | $b_{min}=5$ = 1 tick | :9, :33 | zona minima non nulla |
| B2-R-35 | `entry_zone` insieme discreto multipli di 5 | :29, :31 | livelli operabili espliciti |
| B2-R-36 | cardinalità banda $(2b/5)+1$ | :33 | numero livelli prevedibile |
| B2-R-37 | floor $b_{min}$ evita banda nulla | :33 | zona sempre operabile |
| B2-CN-01 | vincolo geometrico $d_{stop}>b$ (vedi §3.10) | :47, :49 | nessun stop sul tick del fill |
| B2-CN-02 | payload congelato all'emissione | :73 | valori stabili fra lettura e ordine |
| B2-CN-03 | nessun edit a parità di `signal_id` | :73 | chiave = contenuto immutabile |
| B2-CN-04 | segnale unico attivo $|\mathcal{A}(t)|\le1$ | :79, :81 | un solo segnale operabile per volta |
| B2-CN-05 | sostituzione = nuovo `signal_id`+nuova tupla, non edit | :77, :83 | segnale nuovo riconoscibile |

> **Nota su B2-CN-01** (vincolo geometrico $d_{stop}>b$): reso come requisito **invariante** data la sua rilevanza contrattuale.
>
> **B2-CN-01** *(invariante strutturale)* — Vale il **vincolo geometrico obbligatorio** $d_{stop} > b$: la distanza dello stop dal riferimento deve essere strettamente maggiore della semi-ampiezza della banda. Cromosomi che producono segnali in violazione sono dichiarati non validi.
> - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:47, :49]`.
> - *Valore operativo*: evita che un fill al bordo opposto della banda coincida con il prezzo di stop, cioè un segnale eseguito e immediatamente stoppato nello stesso tick; protegge l'operatore da un'operazione strutturalmente perdente per costruzione.

### 8.2 Nota di rinvio (materia deliberatamente NON consolidata in B2)

Le seguenti materie, **adiacenti al payload** ma fuori dal perimetro Cap.6 (6.1/6.2/6.3), sono **deliberatamente rinviate** ad altri blocchi; la loro assenza in B2 è una scelta di scope, **non** un'omissione:

- **State machine del segnale** (stati `active` + terminali, transizioni), **raw touch come evento**, **semantica dei timer** $\Delta t_{cromosoma}$/$T_{touch}^{max}$ (decorrenza, scadenza → stato terminale, conteggio sui minuti di trading), **meccanica della transizione di sostituzione** (revoca del segnale precedente) → **blocco state-machine & lifecycle** (Cap.7 di Parte II).
- **Position lifecycle / submacchina** post-target_1, **target_2 come evento** raggiunto e relative metriche → **blocco lifecycle / submacchina** (Cap.11 di Parte II).
- **Condizioni di emissione** (volatilità, liquidità, distanza in sigma-units) e **regola di emissione** che applica il **filtro 80pt** (qui B2 consolida solo l'associazione del filtro al campo `setup_class`, non la regola); **definizione operativa di $A_{range}$** (Parte IV) → **blocco emissione** (Cap.8 di Parte II / Parte IV).
- **Contratto informativo del messaggio Telegram**, ordine dei campi pubblicati, **latenza** di consegna, anti-duplicato, retry, errori di pubblicazione → **blocco emissione & consegna** (Cap.9 di Parte II).
- **Log di emissione/transizioni/chiusura**, replay/determinismo, persistenza → **blocco runtime/compliance** (Cap.10 di Parte II).
- **Derivazione matematica** dei livelli (geometria del prezzo, $p_{ref}$ derivato, $\hat{\sigma}_{\text{pt}}$, calcolo dei livelli `synthetic`) → Parti III/IV della metodologia (fuori spec).

---

*Documento B2 prodotto in cieco dal solo Cap.6 (6.1/6.2/6.3) di `CAP_02_parte_II.md` (PASS `a1625df`, frozen). Nessun file di spec preesistente, di B1 o di chunking è stato aperto o citato. ID auto-assegnati da zero.*
