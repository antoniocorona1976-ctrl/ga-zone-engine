# Review CAP-02 v1 — Parte II: Contratto del segnale FIB (primo giro ostile)

**Verdetto**: CONDITIONAL

Motivazione sintetica: il documento copre i 14 acceptance criteria e cita esplicitamente le 8 eredità di CAP-01. La struttura della state machine è solida nell'intento (1 non-terminale + 7 terminali + trigger come evento). Tuttavia emergono **due bug reali bloccanti (B)** sulla coerenza della state machine — il caso "stop raggiunto senza raw touch eseguibile" non è coperto dalla tabella delle transizioni, e la regola di `missed_target` come definita in Cap.7.1 entra in conflitto con la chiarificazione di Cap.8.3 — e **alcuni NB significativi** su transizioni mancanti dopo `missed_target`, ambiguità sulla granularità di $\Delta t_{cromosoma}$, e formulazioni vaghe del vincolo M-1. Il documento è complessivamente di buon livello ma necessita di rework chirurgico sulla state machine prima del PASS.

---

## Finding classificati

### B-1 — BUG REALE BLOCCANTE: la state machine non copre il caso "prezzo raggiunge stop_loss senza alcun raw touch (o senza raw touch eseguibile) prima"

**Posizione**: Cap.7.2 (tabella transizioni, righe 105-114), Cap.7.1 (definizione `stopped`, riga 91), Cap.8.3 (riga 188).

**Citazione**:
- Cap.7.1, riga 91: "`stopped` — dopo il primo raw touch della entry zone, il prezzo ha raggiunto `stop_loss` prima di raggiungere `target_1`..."
- Tabella Cap.7.2 (riga 110): "`active` → `stopped` — Dopo raw touch della entry zone, il prezzo raggiunge `stop_loss` senza prima raggiungere `target_1`"
- Cap.8.3 (riga 188): "il raggiungimento di `target_1` prima di un raw touch eseguibile... porta il segnale in `missed_target`, indipendentemente dal fatto che vi fossero stati raw touch con guardie non superate precedenti"

**Motivazione**: il contratto della state machine impone che `stopped` richieda un raw touch precedente. Ma cosa accade se:
- il prezzo si muove direttamente contro l'ipotesi e tocca lo `stop_loss` prima di toccare la entry zone (es. segnale long con $p_{ref}=41000$, $b=10$, $\texttt{stop\_loss}=40970$; il prezzo dopo l'emissione scende a $40970$ senza mai toccare $[40990, 41010]$)?
- il prezzo entra nella entry zone solo con guardie NON superate (raw touch ignorati), poi scende fino allo stop?

Nel primo caso, la state machine non ha alcuna transizione applicabile: `stopped` richiede raw touch precedente, `invalidated` richiede "condizione di invalidazione strutturale (Parte IV, Cap.15)" che è demandata altrove e non automaticamente attivata da "prezzo che tocca stop". Il segnale resterebbe `active` fino a `expired`, registrando una perdita strutturale (lo stop è strutturalmente saltato) come "scadenza". Questo è **incoerente con la realtà operativa** (lo stop esiste come livello e va monitorato anche pre-touch) e **corrompe direttamente il ranking dei cromosomi** del GA: i cromosomi che emettono segnali con stop strutturali ravvicinati ma mai raggiunti via raw touch non vengono penalizzati come dovrebbero.

Nel secondo caso, stessa lacuna: i raw touch ignorati per guardie non superate non risolvono il caso "prezzo che poi prosegue verso lo stop senza toccare effettivamente la zona con guardie OK".

Il caso simmetrico per `target_1` è invece coperto da `missed_target` (target raggiunto prima del raw touch). Manca lo speculare per `stop_loss`.

**Classificazione**: **B**

**Proposta correttiva**: aggiungere uno stato terminale (o ridefinire `invalidated`) che catturi il caso "il prezzo ha raggiunto `stop_loss` prima di un raw touch eseguibile". Due opzioni:
- Opzione A: estendere `invalidated` esplicitamente includendo come condizione di invalidazione strutturale "il prezzo raggiunge `stop_loss` prima di un raw touch eseguibile della entry zone";
- Opzione B: introdurre uno stato `missed_stop` analogo a `missed_target` (porta a 8 stati terminali — richiederebbe rinegoziare l'acceptance criterion #5 con il supervisore).

L'opzione A è più conservativa e mantiene 7 stati terminali ma necessita di una nota esplicita in Cap.7.1 e l'aggiunta della riga corrispondente nella tabella 7.2.

---

### B-2 — BUG REALE BLOCCANTE: contraddizione interna fra Cap.7.1 (`missed_target`) e Cap.8.3 sulla definizione operativa di "prima del raw touch"

**Posizione**: Cap.7.1 (riga 95), Cap.7.2 tabella (riga 112), Cap.8.3 (riga 188).

**Citazione**:
- Cap.7.1, riga 95: "`missed_target` — prima del primo raw touch della entry zone, il prezzo ha raggiunto `target_1`."
- Cap.7.2, riga 112: "`active` → `missed_target` — Prima del raw touch, il prezzo raggiunge `target_1`"
- Cap.8.3, riga 188: "il raggiungimento di `target_1` prima di un **raw touch eseguibile** (cioè prima di un raw touch in cui tutte e quattro le guardie siano superate) porta il segnale in `missed_target`, **indipendentemente dal fatto che vi fossero stati raw touch con guardie non superate precedenti**"

**Motivazione**: ci sono due definizioni operazionali in contrasto. In Cap.7.1 e nella tabella 7.2 la condizione è "prima del primo raw touch" (raw touch è raw touch, eseguibile o no). In Cap.8.3 la condizione è esplicitamente "prima di un raw touch **eseguibile**" — cioè raw touch con guardie superate. Le due definizioni divergono nel comportamento: se il prezzo entra nella zona con guardie OFF, poi torna fuori, poi raggiunge `target_1`, **secondo Cap.7.1 il segnale NON è `missed_target` (c'è stato un raw touch)**; secondo Cap.8.3 il segnale **È `missed_target`** (il raw touch non era eseguibile).

Il GA ranking dipende criticamente da questa metrica (la missed_target rate è una metrica di lifecycle di CAP-01 Cap.5): una definizione ambigua produce metriche non riproducibili e contraddice il requisito di determinismo di Cap.10.1.

**Classificazione**: **B**

**Proposta correttiva**: armonizzare le due formulazioni. Modificare Cap.7.1 e la tabella di Cap.7.2 per usare "prima del primo raw touch **eseguibile**" (definizione di Cap.8.3, che è quella operativamente corretta per il GA: un raw touch con guardie OFF non è economicamente differente dal non-touch). Eventualmente definire formalmente "raw touch eseguibile" in Cap.8.1 o all'inizio del Cap.7 come termine tecnico riusabile.

---

### NB-1 — Transizioni mancanti dopo `missed_target` per simmetria con `target_1_hit` → `target_2_hit`

**Posizione**: Cap.7.2 (riga 116), Cap.7.1 (riga 95).

**Citazione**: la nota a piè di pagina (riga 116) afferma che dopo `missed_target` il segnale è "definitivamente concluso".

**Motivazione**: Cap.7.1 sostiene la simmetria interpretativa "il mercato ha realizzato il target ma il setup non si è eseguito". Per coerenza interna sarebbe naturale registrare anche `target_2` qualora raggiunto dal mercato dopo `missed_target`: il GA otterrebbe in questo modo una metrica simmetrica `missed_target_2_rate` confrontabile con `target_2_hit_rate`. Asimmetria attuale: il segnale eseguito tiene traccia del target 2 (terminale `target_2_hit` post `target_1_hit`), il segnale non eseguito no. Si crea uno squilibrio nella valutazione delle ipotesi "target_2 strutturalmente plausibile".

Decisione formale del supervisore in CAP-01 (Q-03) ha chiuso `missed_target_rate` sul solo target 1 — quindi non è strettamente bloccante — ma la mancata simmetria va almeno motivata esplicitamente nel testo.

**Classificazione**: **NB**

**Proposta correttiva**: aggiungere una riga in Cap.7.1 o Cap.7.2 che chiarisca la scelta esplicita di non tracciare `target_2` dopo `missed_target` (citando Q-03 di CAP-01), evitando che la lettura del documento susciti l'interpretazione di una svista.

---

### NB-2 — Granularità di $\Delta t_{cromosoma}$ non specificata

**Posizione**: Cap.7.4 (riga 130-134), Cap.6.1 (riga 43-47).

**Citazione**: "$\texttt{expiry} = \texttt{timestamp\_emission} + \Delta t_{cromosoma}$" con "$0 < \Delta t_{cromosoma} \leq 2$ giorni di trading"; e prima "$\texttt{expiry}$ — istante di scadenza del segnale, espresso al minuto chiuso".

**Motivazione**: la granularità di $\Delta t_{cromosoma}$ — il parametro libero del cromosoma che il GA ottimizza — non è specificata. È un intero in minuti? Un valore continuo? In "barre di trading" o in "minuti di trading"? Lo spazio dei parametri del cromosoma (Parte V, Cap.21) dipende criticamente da questa scelta: se $\Delta t$ è continuo serve mutazione gaussiana; se discreto in minuti il dominio ha cardinalità $\sim 1680$ (2 × 840), se in 5-minute steps cardinalità $\sim 336$. La Parte II è la sede in cui il contratto del payload viene fissato e l'inferenza del dominio del cromosoma per la Parte V parte da qui.

**Classificazione**: **NB**

**Proposta correttiva**: aggiungere in Cap.7.4 una riga che dichiari la granularità di $\Delta t_{cromosoma}$ (proposta: "intero in minuti di trading, $\Delta t_{cromosoma} \in \{1, 2, \dots, 1680\}$", oppure rinviare esplicitamente a Parte V con la nota che la granularità minima è la barra 1-min).

---

### NB-3 — Vincolo M-1 formulato in modo vago e non operazionalizzabile

**Posizione**: Cap.7.5 (riga 138-142).

**Citazione**: "la regola di confermabilità del pivot... [vale] come vincolo del contratto che l'ancora del prezzo strutturale di riferimento per il primo segnale della sessione **deve essere disponibile entro una latenza compatibile con l'emissione di segnali significativi nella prima fase della finestra 8:00-22:00 CET**".

**Motivazione**: "latenza compatibile con l'emissione di segnali significativi" è una formulazione vaga del tipo che CAP-01 v3 ha imparato a evitare. Non c'è alcun valore quantitativo (anche provvisorio, qualificato come tale) né una procedura operativa per misurare se il vincolo è soddisfatto. È la stessa categoria di "compatibile con / coerente con" che il task ACTIVE identifica come "buco semantico" (punto 7 della checklist di audit). Senza una quantificazione, la Parte III può scegliere una regola di pivot detection arbitraria e dichiarare il vincolo soddisfatto.

**Classificazione**: **NB**

**Proposta correttiva**: convertire in vincolo operativo, anche con valore provvisorio: "la regola di pivot detection deve produrre il primo candidato di sessione entro un numero massimo $N_{pivot}$ di barre 1-min dall'apertura della sessione; valore di lavoro provvisorio $N_{pivot} = 30$ (mezz'ora dall'apertura), congelato in Parte V". Oppure rinviare esplicitamente a Parte V/Cap.14 segnalando che il valore è da fissare con misura empirica sullo storico.

---

### NB-4 — Caso "emissione vicino alla chiusura di sessione 22:00" non trattato nel timer di scadenza

**Posizione**: Cap.7.4 (riga 130-134).

**Citazione**: "2 giorni di trading sono l'unione delle finestre 8:00-22:00 CET di due giornate consecutive di negoziazione, scavalcando le interruzioni notturne e i weekend."

**Motivazione**: se un segnale è emesso alle 21:55 CET con $\Delta t_{cromosoma} = 2$ giorni di trading, $\texttt{expiry}$ cade in che istante esattamente? Tre interpretazioni:
- (a) 21:55 di due giorni di trading dopo (cioè il segnale ha 5 min + 14h + 14h = 28h05min di sessione attiva);
- (b) 22:00 del secondo giorno di trading successivo (ossia consuma sempre 2 sessioni intere indipendentemente dall'ora di emissione);
- (c) somma esatta di minuti di trading: $\Delta t_{cromosoma} = 2 \times 840 = 1680$ min di trading, ossia 5 min nel giorno di emissione + 1675 min nei due giorni successivi.

L'interpretazione (c) è la più rigorosa ma il testo non la specifica. Il GA può tarare il timing di chiusura solo se sa quanti minuti effettivi di trading entrano nel cap. Ambiguità impatta direttamente l'ottimizzazione del timing di chiusura.

**Classificazione**: **NB**

**Proposta correttiva**: aggiungere in Cap.7.4 una formula esplicita: "$\Delta t_{cromosoma}$ è espresso in minuti di trading; $\texttt{expiry}$ è raggiunto quando il numero di minuti di trading trascorsi dall'emissione raggiunge $\Delta t_{cromosoma}$, scavalcando le interruzioni notturne e i weekend".

---

### NB-5 — Direzione del raw touch in funzione di `direction` non esplicitata

**Posizione**: Cap.8.1 (riga 150), Cap.6.1 (riga 23-29).

**Citazione**: "Si definisce raw touch della entry zone... l'evento in cui il prezzo del FIB... entra per la prima volta nell'intervallo $[p_{ref} - b, p_{ref} + b]$ dopo l'emissione del segnale."

**Motivazione**: la entry zone è simmetrica attorno a $p_{ref}$, ma per un segnale long il bordo strutturalmente rilevante per il fill è il bordo INFERIORE (prezzo che scende fino a entrare nella zona di acquisto); per uno short, il bordo SUPERIORE. La definizione di Cap.8.1 dice "entra... nell'intervallo": è generica, non specifica la direzione di entrata. Se il prezzo, dopo l'emissione di un long con $p_{ref}=41000, b=10$, parte da $40985$ (sotto la zona) e sale a $40990$ (entra dal basso → ha già attraversato il punto strutturale di fill?), l'interpretazione operativa è ambigua.

Operativamente l'operatore manuale piazza l'ordine al limite inferiore della zona long (o superiore della zona short), quindi il "raw touch" rilevante è la traiettoria che porta il prezzo dal lato non-tradeato a quello tradeato.

**Classificazione**: **NB**

**Proposta correttiva**: precisare in Cap.8.1 (o in Cap.6.1 nella definizione di `entry_zone`) che per un segnale long il raw touch è il primo istante in cui $p(t) \leq p_{ref} + b$ provenendo dall'alto (analogamente con segno opposto per short). Il documento corrente non rende impossibile una lettura operativa coerente, ma la lascia implicita.

---

### NB-6 — "Decisione del supervisore in chiusura M-3" formula erronea

**Posizione**: Cap.8.4 (riga 194).

**Citazione**: "Questa scelta recepisce la decisione del supervisore in chiusura M-3 di Review v4 di CAP-01, che ha chiarito che il FIB negozia in modo continuo nell'intera finestra 8:00-22:00 senza fase d'asta separata."

**Motivazione**: REVIEW_CAP_01 v4 (riga 91) dichiara M-3 **"RITIRATA"**, non "chiusa": "il promemoria assumeva la presenza di una fase d'asta 8:00-9:00 con price discovery discontinuo. Il supervisore ha chiarito che il FIB negozia in modo continuo... **M-3 non è più una osservazione valida** e non va girata a Parte II/Appendice D". La formulazione attuale ("decisione del supervisore in chiusura M-3") suggerisce che M-3 sia stata una decisione formalizzata; era invece un'osservazione del review ritirata su chiarimento del supervisore. Imprecisione di citazione che ha rilevanza di tracciabilità per cicli successivi.

**Classificazione**: **NB**

**Proposta correttiva**: sostituire con "Questa scelta recepisce il chiarimento del supervisore che ha ritirato l'osservazione M-3 di Review v4 di CAP-01 (presunta fase d'asta 8:00-9:00) confermando che il FIB negozia in modo continuo nell'intera finestra 8:00-22:00."

---

### N-1 — Asimmetria di trattamento del `target_2` per `stopped`

**Posizione**: Cap.7.1 (riga 91), Cap.7.2.

**Motivazione**: Il segnale "stoppato" non registra mai cosa avrebbe fatto il prezzo se non fosse stato stoppato (e.g. avrebbe raggiunto target_1, o target_2?). In coerenza con il replay deterministico (Cap.10) e con il calcolo di MAE/MFE (Cap.10.4), si potrebbe argomentare che la metrica MFE post-stop catturi questa informazione — ma non è esplicitato nel contratto. Non bloccante per CAP-02 ma osservazione per Parte V (fitness): se il GA ha solo `stopped` come segnale binario, perde informazione strutturale rispetto al "quanto era buona l'ipotesi anche se è stata stoppata in itinere".

**Classificazione**: **N**

---

### N-2 — Cap.10.4: rendimento netto "derivabile deterministicamente dal lordo" senza registrazione

**Posizione**: Cap.10.4 (riga 297).

**Citazione**: "Il calcolo del rendimento netto non è registrato nel log di chiusura come campo aggiuntivo, in quanto derivabile deterministicamente dal lordo: il valore probatorio della grandezza è preservato dal determinismo del replay."

**Motivazione**: scelta legittima, ma se il modello di commissioni dovesse evolvere (es. broker passa a fee fissa o variabile), tutti i log storici dovrebbero essere ricalcolati. Non bloccante in Parte II — il vincolo del punto 10 della dichiarazione di intenti fissa $c=1$ pt — ma è osservazione per Parte VII (gate decisionali sul bundle frozen): un cambio di $c$ richiede ricalcolo completo del netto storico.

**Classificazione**: **N**

---

### N-3 — `executable_rate` di CAP-01 priva di state machine corrispondente

**Posizione**: trasversale, riferimento a CAP-01 Cap.5 (riga 77).

**Motivazione**: CAP-01 Cap.5 definisce "executable rate, frazione di segnali emessi che raggiungono il raw touch della zona di ingresso superando le guardie di esecuzione". In CAP-02 il "trigger_event" è degradato a evento (non stato) per coerenza con il vincolo "no execution". Conseguenza: la metrica `executable_rate` di CAP-01 non corrisponde più a una transizione di stato (non c'è uno stato `executable` da contare): va ridefinita come "frazione dei segnali per cui è stato emesso un `trigger_event`". Per la Parte V il GA conserva la leva (le 4 guardie), ma la nomenclatura va armonizzata. Non bloccante per CAP-02 ma rilevante per CAP-V/VI.

**Classificazione**: **N** (carryover per Parte V, Cap.23, e Parte VI, Cap.29).

---

### M-1 — Carryover M-1 CAP-01 (pivot real-time) parzialmente assorbito

**Posizione**: Cap.7.5.

**Motivazione**: M-1 carryover di CAP-01 è formalmente trattato in Cap.7.5 a livello di interfaccia, come richiesto. Resta come carryover residuo per Parte III/Cap.14 il vincolo quantitativo (vedi NB-3): la regola di pivot detection deve produrre il candidato entro $N_{pivot}$ barre. Da girare a Parte III quando affrontata.

**Classificazione**: **M** (carryover Parte III).

---

### M-2 — Verifica empirica latenza Telegram

**Posizione**: Cap.9.3 (riga 227).

**Motivazione**: $L_{max} = 30$ s è "valore di lavoro provvisorio". La verifica empirica del canale (latenza effettiva push API Bot in copertura mobile italiana) è rinviata ad Appendice E. Da non dimenticare in fase di scrittura Appendice E.

**Classificazione**: **M** (carryover Appendice E).

---

## Tabella verifica acceptance criteria (14 punti)

| # | Criterio | Esito | Citazione/Posizione |
|---|----------|-------|---------------------|
| 1 | I 5 capitoli (Cap 6-10) presenti, completi, ordine corretto | OK | Sezioni `## Capitolo 6` ... `## Capitolo 10` (righe 9, 77, 146, 198, 251) |
| 2 | 8 eredità CAP-01 citate esplicitamente | OK | Sessione 8-22 (righe 5, 21, 47, 134, 194, 301); banda $b \in [b_{min},40]$ (riga 29); $d_{stop}>b$ (riga 39); target 1+2 obbligatori (riga 31); $\leq$2gg trading (righe 45, 130); primo pivot post-apertura (riga 138); filtro 80pt (righe 51, 55); no execution (riga 122) |
| 3 | Cap 6: payload come tupla, tutti i campi, vincoli | OK | Cap.6.1 (righe 13-57) |
| 4 | Cap 6: payload immutabile + regola sostituzione | OK | Cap.6.2 (riga 61) e Cap.6.3 (righe 63-73) |
| 5 | Cap 7: 1 non-terminale + 7 terminali + transizioni + trigger come evento | OK | Cap.7.1 (righe 81-99), Cap.7.2 tabella (righe 105-116), Cap.7.3 (righe 118-124). **NOTA**: la state machine è incompleta — vedi B-1 (mancanza transizione "stop pre-touch"). Formalmente i 7 stati ci sono, ma operativamente non coprono tutti i percorsi del prezzo. |
| 6 | Cap 7: cap 2gg trading come timer concreto | OK con riserva | Cap.7.4 (righe 128-134). Formula presente ma granularità di $\Delta t_{cromosoma}$ non specificata — NB-2. Caso 21:55 non chiarito — NB-4. |
| 7 | Cap 7: M-1 a livello di interfaccia | OK con riserva | Cap.7.5 (righe 138-142). Trattato ma con formulazione vaga — NB-3. |
| 8 | Cap 8: 4 guardie nominate + rinvio Parte V soglie | OK | Cap.8.2 (righe 154-180) volatilità/spread/liquidità/distanza; Cap.8.3 (riga 190) rinvio Parte V |
| 9 | Cap 8: nessuna assunzione fasi speciali (M-3 ritirato) | OK con riserva | Cap.8.4 (riga 194). Sostanza OK, ma citazione di M-3 come "decisione del supervisore in chiusura" è imprecisa: M-3 fu ritirata — NB-6. |
| 10 | Cap 9: anti-duplicato + nuovo messaggio per nuovo signal_id (no edit) | OK | Cap.9.4 (riga 231), Cap.9.5 (righe 235-237) |
| 11 | Cap 10: determinismo del replay come vincolo, non desiderio | OK | Cap.10.1 (riga 259) formula bit-exact |
| 12 | Registro tecnico italiano formale | OK | Tutto il documento |
| 13 | LaTeX inline e display | OK | Cap.6.1, Cap.6.3, Cap.7.4, Cap.8.2, Cap.10.1 |
| 14 | Niente moltiplicazioni misleading o numeri inventati | OK | $L_{max}=30$s, $n_{retry}=3$, $\Delta t_{retry}=2$s tutti qualificati "valore di lavoro provvisorio" e rinviati a Parte V/Appendice E |

---

## Tabella verifica eredità CAP-01 (8 punti)

| # | Eredità | Esito | Posizione |
|---|---------|-------|-----------|
| 1 | Sessione 8:00-22:00 CET come finestra unica e continua | OK | Cap.6 intro (riga 5), Cap.6.1 (riga 21), Cap.7.4 (riga 134), Cap.8.4 (riga 194), Cap.10.5 (riga 301) |
| 2 | Banda $b \in [b_{min}, 40]$, $b_{min}=5$ provvisorio | OK | Cap.6.1 (riga 29) |
| 3 | Vincolo geometrico $d_{stop} > b$ obbligatorio | OK | Cap.6.1 (righe 35-41) |
| 4 | Target 1 e target 2 entrambi obbligatori, ancorati a strutturali | OK | Cap.6.1 (riga 31) |
| 5 | Cap validità $\leq$ 2 giorni di trading | OK | Cap.6.1 (riga 45), Cap.7.4 (riga 130) |
| 6 | Movimento strutturale ancorato a primo min/max post-apertura | OK | Cap.7.5 (riga 138) cita il "primo pivot strutturale post-apertura" e la sua funzione di ancora |
| 7 | Filtro emissione $\geq 80$ pt FIB | OK | Cap.6.1 (righe 49-57): formula direzionale e formula trade_range |
| 8 | No execution (punto 1 dichiarazione) | OK | Cap.7.3 (riga 122): citazione esplicita del vincolo |

Tutte le 8 eredità citate. Buon livello di tracciabilità formale.

---

## Tabella classificazione per il supervisore

| # | Problema | Classificazione | Mandare a Development? |
|---|----------|-----------------|------------------------|
| B-1 | Mancanza transizione "stop raggiunto senza raw touch eseguibile" | **B** | SÌ — rework chirurgico Cap.7.1 e tabella Cap.7.2 |
| B-2 | Contraddizione `missed_target` "prima del raw touch" (Cap.7) vs "prima del raw touch eseguibile" (Cap.8.3) | **B** | SÌ — armonizzazione Cap.7.1 + Cap.7.2 + Cap.8.3 |
| NB-1 | Mancata simmetria `missed_target_2` rispetto a `target_2_hit` | NB | Decisione supervisore: motivare esplicitamente la scelta di non tracciare o accettare lacuna |
| NB-2 | Granularità di $\Delta t_{cromosoma}$ non specificata | NB | SÌ — riga aggiuntiva Cap.7.4 |
| NB-3 | Vincolo M-1 "latenza compatibile" vago | NB | SÌ — quantificare anche provvisoriamente |
| NB-4 | Caso emissione vicino chiusura 22:00 non trattato in timer expiry | NB | SÌ — formalizzare somma in minuti di trading |
| NB-5 | Direzione del raw touch per long/short non esplicitata | NB | SÌ — precisazione Cap.8.1 |
| NB-6 | "Decisione del supervisore in chiusura M-3" — M-3 era ritirata, non chiusa | NB | SÌ — correzione formulazione Cap.8.4 |
| N-1 | Asimmetria `stopped` vs `target_*_hit` per tracking percorso post-evento | N | NO — osservazione per Parte V |
| N-2 | Netto non registrato in log_chiusura | N | NO — osservazione per Parte VII |
| N-3 | `executable_rate` CAP-01 priva di stato corrispondente | N | NO — carryover Parte V/VI |
| M-1 | Quantificazione $N_{pivot}$ per pivot detection | M | NO — carryover Parte III/Cap.14 |
| M-2 | Verifica empirica latenza Telegram | M | NO — carryover Appendice E |

**Conteggio**: B = 2, NB = 6, N = 3, M = 2.

---

## Sintesi finale per il supervisore (< 200 parole)

**Verdetto v1**: **CONDITIONAL**. Primo giro ostile su Parte II completato. Il documento copre i 14 acceptance criteria e cita esplicitamente le 8 eredità CAP-01. Tuttavia emergono due bug bloccanti sulla coerenza della state machine: (B-1) la state machine non copre il caso "prezzo raggiunge stop_loss senza alcun raw touch eseguibile precedente" — il segnale resterebbe `active` fino a `expired` corrompendo il ranking dei cromosomi con stop ravvicinati; (B-2) `missed_target` è definito come "prima del raw touch" in Cap.7.1 e tabella 7.2, ma come "prima del raw touch **eseguibile**" in Cap.8.3 — contraddizione interna che rende la metrica non riproducibile e contraddice il vincolo di determinismo di Cap.10.1.

Sei NB significativi (granularità $\Delta t_{cromosoma}$, vincolo M-1 vago, caso 21:55, direzione raw touch, simmetria missed_target_2, citazione M-3) sono correzioni chirurgiche.

**Raccomandazione**: **rework Development**. I due B vanno corretti insieme ai sei NB; gli N e M restano carryover legittimi. Non procedere a CAP-03 prima del PASS di CAP-02. Atteso ciclo v2.


---

## Review v2 — Re-audit ostile dopo riscrittura integrale

**Verdetto**: **CONDITIONAL**

Motivazione sintetica: la riscrittura integrale chiude in modo sostanzialmente corretto i due B di Review v1 e i sei NB della v1; le due decisioni strutturali del supervisore (decorrenza expiry dal raw touch; Cap.8 come condizioni pre-emissione) sono implementate in modo coerente nel testo di Parte II. Tuttavia emergono due nuovi bug reali (B-3 ambiguità formale dello stato `target_1_hit` non-terminale di fatto; B-4 incoerenza fra Parte II v2 e CAP-01 v2 sulla decorrenza del cap 2gg e sulle "guardie di esecuzione" residue in CAP-01) e quattro NB nuovi (assenza di timer pre-touch, edge case raw touch su barra di emissione/gap apertura, ambiguità del fill virtuale intrabar, mancata transizione `target_1_hit → revoked`). Il documento è di alta qualità nella sostanza ma la propagazione retroattiva su CAP-01 non è stata eseguita, lasciando il corpus internamente incoerente.

---

## Verifica di chiusura dei finding di Review v1

| ID v1 | Esito chiusura v2 | Posizione/citazione | Note |
|-------|-------------------|---------------------|------|
| **B-1** stop pre-touch | **CHIUSO** | Cap.7.1 (definizione `invalidated` riga 95): "fra le condizioni esplicitamente incluse nel contratto del segnale rientra il superamento del livello `stop_loss` da parte del prezzo, nella direzione contraria all'ipotesi del segnale, prima del raw touch: per i segnali long, $p(t) \leq \texttt{stop\_loss}$ con $t < t_{touch}$; simmetricamente per gli short". Tabella Cap.7.2 riga 113 contiene la riga `active → invalidated` con condizione esplicita. | Opzione A della proposta v1 applicata correttamente. |
| **B-2** missed_target contraddizione | **CHIUSO** | Cap.7.3 riga 124: "**Il raw touch è sempre eseguibile**: non esistono nel contratto del segnale guardie o filtri post-emissione che blocchino il trigger". Cap.7.1 riga 97 e Cap.7.2 riga 114: `missed_target` definito solo come "prima del raw touch" senza il qualificatore "eseguibile". Il concetto "raw touch eseguibile" è scomparso dal testo. | Cade per costruzione con la nuova architettura Cap.8 pre-emissione. |
| **NB-1** asimmetria missed_target_2 | **CHIUSO** | Cap.7.1 riga 97: "La metrica missed target rate definita in CAP-01 è riferita esplicitamente a `target_1` e non a `target_2`, in coerenza con la chiusura Q-03 di CAP-01 [...] l'asimmetria [...] è una scelta esplicita e non una svista". | Motivazione esplicita inserita. |
| **NB-2** granularità $\Delta t_{cromosoma}$ | **CHIUSO** | Cap.7.4 riga 134: $\Delta t_{cromosoma} \in \{1, 2, \ldots, 1680\}$ minuti di trading. | Dominio discreto dichiarato. |
| **NB-3** vincolo M-1 vago | **CHIUSO con riserva** | Cap.7.5 riga 150: rinvio a Parte V con misura empirica, vincolo metodologico esplicito ("non può produrre un primo candidato di sessione con latenza tale da rendere di fatto inattiva la finestra iniziale"). | Manca ancora una soglia provvisoria — accettabile come carryover Parte III/V. |
| **NB-4** caso emissione 21:55 | **CHIUSO** | Cap.7.4 riga 140: esempio esplicito "raw touch a $t_{exec}$ = lunedì 21:55 CET con $\Delta t_{cromosoma} = 1680$ [...] expiry è quindi mercoledì 21:55 CET". | Formula in minuti di trading scavalca interruzioni. |
| **NB-5** direzione raw touch | **CHIUSO con cambio semantica** | Cap.7.3 riga 122: "La definizione non impone alcun vincolo di direzione di provenienza del prezzo". Tick FIB=5pt formalizzato in introduzione Parte II e Cap.6.1. | Soluzione differente dalla proposta v1 (entrata da una direzione specifica): in v2 si è scelto raw touch direzione-agnostico. Coerente con barra OHLC senza tick stream. |
| **NB-6** citazione M-3 errata | **CHIUSO** | Cap.8.4 riga 204: "il chiarimento del supervisore che ha **ritirato** l'osservazione M-3 di Review v4 di CAP-01". | Formulazione corretta. |
| **N-1, N-2, N-3** | Carryover legittimi (Parte V/VI/VII) | — | Confermati. |
| **M-1, M-2** | Carryover legittimi (Parte III/Appendice E) | — | Confermati. |

**Conclusione**: tutti i finding v1 sono effettivamente chiusi nel testo di Parte II v2.

---

## Nuovi finding introdotti dalla riscrittura

### B-3 — BUG REALE BLOCCANTE: `target_1_hit` non è formalmente terminale ma è dichiarato tale; ambiguità di transizioni uscenti

**Posizione**: Cap.7.1 riga 91, Cap.7.2 tabella riga 111, nota asterisco riga 118.

**Citazione**:
- Cap.7.1 riga 91: "**`target_2_hit`** — dopo il raggiungimento di `target_1`, [...] Lo stato `target_2_hit` è terminale e succede sequenzialmente a `target_1_hit`: la transizione diretta da `active` a `target_2_hit` senza passaggio implicito da `target_1_hit` non è ammessa."
- Tabella Cap.7.2 riga 111: "`target_1_hit`* → `target_2_hit` — Dopo `target_1_hit`, il prezzo raggiunge `target_2` senza prima toccare `stop_loss`, senza scadere e senza invalidazione".
- Nota riga 118: "`target_1_hit`, **sebbene terminale come stato del segnale per la finalità del log di chiusura**, ammette **in via eccezionale la sola transizione successiva a `target_2_hit`** per registrare l'eventuale raggiungimento del secondo target."

**Motivazione**: la nota cerca di tenere insieme due affermazioni mutualmente esclusive — "terminale" e "ammette transizione uscente" — con la formula "terminale per il log di chiusura, non-terminale per la state machine". Il problema non è semantico ma operativo:

1. La tabella di Cap.7.2 riga 111 richiede che la transizione `target_1_hit → target_2_hit` avvenga "senza prima toccare `stop_loss`, senza scadere e senza invalidazione". Ma se il segnale è in `target_1_hit` e poi il prezzo torna giù e tocca `stop_loss`, cosa accade? Non c'è transizione `target_1_hit → stopped` nella tabella. Resta in `target_1_hit`? Diventa `stopped`? Il log di chiusura è già scritto (per la prima clausola) o no?
2. Se il segnale è in `target_1_hit` e l'expiry decorre, cosa accade? Non c'è transizione `target_1_hit → expired`.
3. Se in `target_1_hit` il motore emette un nuovo segnale per sostituzione, c'è transizione `target_1_hit → revoked`? Non è in tabella.
4. Il log di chiusura (Cap.10.4) viene scritto a `target_1_hit` (perché "terminale") o a `target_2_hit/stopped/expired/...` successivi? La definizione del log è scritta una volta, ma se può essere riscritta a `target_2_hit` la chiusura non è definitiva.

Il GA dipende criticamente da questa metrica: `target_2_hit_rate` è una metrica primaria (CAP-01 Cap.5) e la sua definizione operativa richiede uno stato pre-`target_2_hit` non-terminale. L'attuale formulazione "terminale + transizione uscente unica" è una contraddizione formale che produce un comportamento di state machine non specificato per gli scenari (1)-(3).

**Classificazione**: **B**

**Proposta correttiva**: due opzioni:
- **Opzione A** (preferita per minimi cambi): rinominare `target_1_hit` da "terminale" a "**stato non-terminale di osservazione post-trigger**" e aggiungere in tabella Cap.7.2 le transizioni mancanti: `target_1_hit → stopped` (prezzo torna a `stop_loss`), `target_1_hit → expired` (timer expiry decorso post-target_1), `target_1_hit → revoked` (sostituzione). Il documento avrebbe 2 stati non-terminali (`active`, `target_1_hit`) + 6 terminali (`target_2_hit`, `stopped`, `invalidated`, `missed_target`, `expired`, `revoked`). Richiede rinegoziazione esplicita con il supervisore dell'AC #5 ("1 non-terminale + 7 terminali") — ma è l'unica soluzione formalmente consistente.
- **Opzione B**: mantenere 7 terminali eliminando `target_2_hit` come stato a sé stante e registrandolo come metrica aggiuntiva del log di chiusura di `target_1_hit` (campo `target_2_reached: bool`). Riduce la cardinalità della state machine a 6 terminali + 1 non-terminale, ma sacrifica la simmetria visiva fra `target_1_hit` e `target_2_hit`.

---

### B-4 — BUG REALE BLOCCANTE: incoerenza retroattiva fra Parte II v2 e CAP-01 v2 sulla decorrenza del cap 2gg trading e sulle "guardie di esecuzione"

**Posizione**: trasversale fra `docs/methodology_v2/CAP_01_parte_I.md` (righe 13, 75, 77) e `docs/methodology_v2/CAP_02_parte_II.md` (righe 5, 45, 47, 99, 132).

**Citazione**:
- **CAP-01 riga 13**: "Il limite massimo di estensione della validità del segnale è fissato a 2 giorni di trading **dall'emissione**: il motore genetico può ottimizzare il timing di chiusura entro questo tetto come parametro del cromosoma, ma non oltrepassarlo."
- **CAP-02 v2 riga 45**: "il timer di 2 giorni di trading decorre dal momento dell'esecuzione, ovvero dal raw touch della entry zone (Cap.7), **non dal `timestamp_emission`**".
- **CAP-01 riga 75**: "Non si introducono in questa sede slippage di esecuzione o spread bid-ask, modellati invece **nelle guardie di esecuzione della Parte II**."
- **CAP-01 riga 77**: "executable rate, frazione di segnali emessi che raggiungono il raw touch della zona di ingresso **superando le guardie di esecuzione**".

**Motivazione**: il corpus del documento metodologico v2 è formato da CAP-01 (PASS chiuso con tag b76c32c) e CAP-02 (oggetto della presente review). La Parte II v2 ha cambiato sotto i piedi a CAP-01 due fatti dichiarati:

1. **Decorrenza expiry**: CAP-01 dice "dall'emissione", CAP-02 dice "dal raw touch". Sono due semantiche operativamente diverse. Un cromosoma del GA con $\Delta t_{cromosoma} = 1680$ minuti significa cose diverse nei due documenti: in CAP-01 il segnale può vivere al massimo 1680 minuti di trading da emissione (sia attesa che post-trigger); in CAP-02 v2 il segnale può attendere infinitamente il raw touch e poi vivere 1680 minuti post-trigger. Le metriche di lifecycle che il GA ottimizza dipendono criticamente da quale delle due semantiche è la verità del corpus.
2. **Guardie di esecuzione**: CAP-01 menziona due volte le "guardie di esecuzione" della Parte II come elemento del modello (riga 75 e 77). Le guardie sono state eliminate dal supervisore in Iterazione 2. CAP-01 contiene quindi un riferimento a un costrutto inesistente. La metrica `executable_rate` di CAP-01 Cap.5 è definita come "frazione di segnali che superano le guardie": senza guardie, la definizione operativa è priva di referente.

L'iterazione 2 di Development ha esplicitamente segnalato il punto come "Patch CAP-01 (riga 13)" nelle "Domande aperte" del report (`reports/REPORT_CAP_02.md`), ma non l'ha eseguita "perché spetta al supervisore decidere se applicarla con o senza passaggio in Review". Tuttavia il documento corrente, presentato per Review v2, contiene **due capitoli internamente coerenti che si contraddicono fra loro**. Per il Review Agent questo è un finding bloccante: il corpus v2 nel suo stato attuale è incoerente e non può ricevere PASS senza risoluzione della propagazione retroattiva.

**Impatto GA**: un cromosoma valutato sul backtest deterministico produce metriche diverse a seconda di quale semantica del cap viene implementata. La metrica `executable_rate` di CAP-01 Cap.5 senza "guardie di esecuzione" è semanticamente vuota e impatta il ranking dei cromosomi.

**Classificazione**: **B**

**Proposta correttiva**: applicare immediatamente la patch CAP-01 prima del PASS di CAP-02, in modo da chiudere il giro v2 con corpus coerente. La patch è puntuale:
- CAP-01 riga 13: "fissato a 2 giorni di trading dall'esecuzione (raw touch della zona di ingresso, Cap.7 Parte II)";
- CAP-01 riga 75: "modellati invece nelle condizioni di emissione (Cap.8 Parte II)";
- CAP-01 riga 77: "executable rate, frazione di segnali emessi che raggiungono il raw touch della zona di ingresso (Cap.7.3 Parte II)". L'`executable_rate` diventa "trigger_event rate", ridefinizione coerente con Cap.7.3.

In alternativa, il supervisore può classificare la patch CAP-01 come tag `[FIX-CARRYOVER]` da applicare in parallelo all'eventuale PASS di CAP-02. Il fatto strutturale rimane: il PASS di CAP-02 v2 senza patch CAP-01 lascia il documento internamente incoerente.

---

### NB-7 — assenza di un timer pre-trigger: il segnale può vivere `active` indefinitamente

**Posizione**: Cap.6.1 riga 49, Cap.7.4 (intero), Cap.7.2 (transizioni `active → revoked` e `active → invalidated` come uniche uscite per segnali mai eseguiti).

**Citazione**:
- Cap.6.1 riga 49: "La fase di attesa pre-esecuzione (dall'emissione al raw touch) **non è governata da questo timer** e resta materia del contratto di emissione di Cap.8."
- Cap.8 non introduce alcun timer pre-trigger.

**Motivazione**: con la chiarificazione semantica del supervisore (timer expiry dal raw touch, non dall'emissione), un segnale che non riceve mai un raw touch resta `active` per un tempo arbitrariamente lungo, finché non viene `revoked` (sostituzione) o `invalidated` (stop attraversato pre-touch). Conseguenze GA:

1. Un cromosoma può "imboscare" un segnale con entry zone lontana dal prezzo, attendere indefinitamente, e produrre statistiche di lifecycle (`executable_rate`, `missed_target_rate`) calcolate su un denominatore che cresce nel tempo senza saturarsi. Il GA potrebbe trovare una strategia degenere "emetti raramente, attendi sempre" che gonfia artificialmente il ranking.
2. Il task list di Development (item #9, `pending`) riporta esplicitamente: "Rework v2: introdurre `time_to_touch_max` come timer pre-trigger". L'item è stato lasciato pending dal supervisore con la motivazione (REPORT_CAP_02.md riga 113): "Non incluso in Parte II v2 per scelta del supervisore di chiudere prima i finding di Review v1. Rimane in tavola come tema di Parte II v3 se il supervisore lo riterrà necessario."
3. In assenza di `time_to_touch_max`, la regola di sostituzione di Cap.6.3 è l'**unico** meccanismo che evita la patologia "attesa indefinita". Ma la regola di sostituzione è una decisione del motore basata su "condizioni di mercato che richiedono di rivedere il segnale": è un trigger pull-based del motore, non un timer push-based del contratto. Cromosomi che sostituiscono raramente lasciano segnali `active` per giorni.

**Classificazione**: **NB**

**Proposta correttiva**: due opzioni:
- riaprire il tema `time_to_touch_max` come parametro libero del cromosoma in Cap.6.1/Cap.7.4 (analogamente a $\Delta t_{cromosoma}$ ma decorrente da `timestamp_emission`);
- dichiarare in Cap.7.4 il vincolo formale "ogni segnale `active` senza raw touch entro la fine della sessione di emissione transita in `invalidated` per scadenza di sessione" (timer implicito = fine sessione corrente). Questa è una semantica più stringente ma non richiede un nuovo parametro.

In assenza di scelta, il rischio GA va almeno menzionato esplicitamente nel testo (sezione "criterio di rollback" del documento o nota dichiarativa in Cap.7.4).

---

### NB-8 — edge case raw touch: barra di emissione con prezzo già nella zona; gap di apertura

**Posizione**: Cap.7.3 riga 122.

**Citazione**: "Si definisce raw touch della entry zone del segnale $\mathcal{S}$ l'evento in cui il prezzo del FIB, osservato dal motore sulla barra 1-min chiusa, assume **per la prima volta dopo l'emissione** un valore appartenente all'insieme discreto [...]. La definizione non impone alcun vincolo di direzione di provenienza del prezzo: la **prima barra 1-min successiva all'emissione** il cui high-low intervallo contenga almeno uno dei livelli discreti della zona produce il raw touch."

**Motivazione**: tre edge case operativi non sono trattati.

1. **Barra di emissione con prezzo nella zona**: il motore emette il segnale al minuto chiuso $t_{emission}$ basandosi sul prezzo strutturale di riferimento $p_{ref}$ derivato dalla barra appena chiusa. Per costruzione, $p_{ref}$ è una grandezza vicina al prezzo del FIB al tempo $t_{emission}$. La barra di emissione (chiusa al minuto $t_{emission}$) potrebbe già avere il suo intervallo high-low che interseca la zona $[p_{ref}-b, p_{ref}+b]$. La definizione attuale dice "prima barra **successiva** all'emissione": esclude la barra di emissione dal calcolo del raw touch. Conseguenza: se il prezzo immediatamente dopo l'emissione resta entro la zona ma poi esce e rientra alla barra successiva, il raw touch è il rientro? O se non rientra mai (resta dentro la zona per N barre poi si allontana), non c'è raw touch? Il caso non è coperto.
2. **Gap di apertura overnight**: tra le 22:00 e le 8:00 del giorno successivo il mercato è chiuso. Un segnale emesso il giorno $D$ alle 21:55 con zona $[40990, 41010]$ potrebbe trovare la prima barra 1-min del giorno $D+1$ (alle 8:00) con un gap che apre direttamente a 41030 (sopra la zona). La barra 8:00 del giorno $D+1$ ha low=41015, high=41040: l'intervallo high-low **non contiene** alcun livello della zona — eppure il prezzo è passato attraverso la zona durante l'overnight chiuso. Il raw touch è considerato avvenuto o no? L'OHLC non lo registra.
3. **Barra che attraversa interamente la zona in 1 minuto**: una barra con low < $p_{ref}-b$ e high > $p_{ref}+b$ (intervallo che contiene tutta la zona). Per un segnale long, l'operatore reale può essere entrato a uno qualunque dei livelli della zona, ma la "regola di simulazione" del backtest (Cap.7.3 riga 128: "fill al primo livello discreto della zona toccato dalla barra 1-min in cui si verifica il raw touch") non specifica quale: dal solo OHLC non si conosce la direzione intrabar. Cap.7.3 rinvia genericamente a Parte III, ma il rinvio non risolve il fatto che la regola di simulazione deterministica deve essere definita in modo unico (vedi vincolo determinismo Cap.10.1) ed entra direttamente nel `rendimento lordo` del log di chiusura.

**Classificazione**: **NB**

**Proposta correttiva**:
- specificare in Cap.7.3 che il raw touch include anche la barra di emissione se l'high-low di quella barra contiene un livello della zona (in tal caso $t_{exec} = t_{emission}$), oppure dichiarare esplicitamente che il raw touch è ammesso solo a $t > t_{emission}$ e motivare la scelta;
- specificare il trattamento del gap di apertura: una barra che apre con prezzo oltre il bordo opposto della zona conta come raw touch implicito sul livello di apertura della zona (es. apertura a 41030 con zona $[40990, 41010]$: $t_{exec}$ = apertura, fill virtuale al bordo superiore 41010);
- specificare in Cap.7.3 (non rinviare a Parte III) la regola deterministica di fill virtuale per barra che attraversa l'intera zona: convenzione, es. "fill al bordo della zona dalla parte di provenienza, dedotta dal close della barra precedente".

---

### NB-9 — `target_1_hit → revoked` mancante (sostituzione post-target_1)

**Posizione**: Cap.7.2 tabella, Cap.6.3.

**Motivazione**: la regola di sostituzione di Cap.6.3 stabilisce $|\mathcal{A}(t)| \leq 1$. Ma se un segnale è in `target_1_hit` (terminale per il log, in attesa di `target_2_hit`/altri esiti secondo la lettura B-3), e nel frattempo il motore emette un nuovo segnale di sostituzione, cosa accade al segnale `target_1_hit`? Per coerenza con $|\mathcal{A}(t)| \leq 1$ esso dovrebbe transitare in `revoked` (la sua osservazione post-target_1 viene troncata dalla nuova emissione). Ma la tabella Cap.7.2 non contiene la riga `target_1_hit → revoked`. Né esplicita se `target_1_hit` conta come "segnale attivo" ai fini del vincolo $|\mathcal{A}(t)| \leq 1$.

Edge case sussidiario: durante `target_1_hit`, l'operatore reale potrebbe avere ancora la posizione aperta (puntando al target_2 o gestendo manualmente lo stop). Se il motore emette un nuovo `signal_id` di sostituzione, l'operatore riceve segnali contraddittori (un segnale in osservazione di target_2 + un nuovo segnale di apertura). Il punto 7 dichiarazione di intenti (1 contratto alla volta) è violato di fatto.

**Classificazione**: **NB**

**Proposta correttiva**: aggiungere riga `target_1_hit → revoked` in Cap.7.2 (allineata con B-3 opzione A); oppure dichiarare esplicitamente in Cap.6.3 che la regola di sostituzione si applica solo a segnali `active` propri (pre-trigger) e non a segnali in `target_1_hit` (post-trigger). La seconda opzione rinforza il principio "l'operatore gestisce la posizione aperta" ma richiede chiarimento su cosa il motore osservi durante `target_1_hit`.

---

### NB-10 — sovrapposizione $\tau_{dist}$ vs filtro 80pt CAP-01: parametro libero degenere

**Posizione**: Cap.8.2 riga 180-188.

**Citazione**: "$\texttt{target\_1} - p_{ref} \geq \max(\tau_{dist},\ 80)$ [...] La soglia $\tau_{dist}$ è parametro libero del cromosoma con vincolo inferiore di 80 punti FIB (filtro di emissione CAP-01); il cromosoma può sceglierla più stringente, mai più lassista."

**Motivazione**: il filtro CAP-01 è $\geq 80$ punti, hardcoded. La condizione $\tau_{dist}$ del Cap.8.2 è parametro libero del cromosoma con floor 80. La formula $\max(\tau_{dist}, 80)$ implica:
- se il cromosoma sceglie $\tau_{dist} \leq 80$, la condizione è equivalente al filtro CAP-01 fisso: il parametro è di fatto inattivo;
- se il cromosoma sceglie $\tau_{dist} > 80$, la condizione è più stringente.

Il dominio effettivo della leva del cromosoma è quindi $\tau_{dist} \in (80, \tau_{max}]$ con $\tau_{max}$ non specificato. L'intervallo $[0, 80]$ del cromosoma è uno spazio nullo del GA: la mutazione su questo intervallo non produce variazioni di fitness. Edge case: il GA potrebbe convergere su $\tau_{dist} = 0$ (default) e la condizione $E_{dist}$ è di fatto sempre attiva solo per il floor di 80, ovvero il filtro CAP-01. La condizione $E_{dist}$ non aggiungerebbe alcuna leva.

**Classificazione**: **NB**

**Proposta correttiva**: ridefinire $\tau_{dist}$ con dominio strettamente $> 80$ (es. $\tau_{dist} \in (80, 500]$ punti) oppure come **moltiplicatore della distanza** rispetto a una grandezza strutturale (es. $\tau_{dist}$ misurato in unità di volatilità $\hat{\sigma}$ corrente — coerente con il principio metodologico "coerenza distanze ↔ volatilità" del report Development punto 3 dei "punti aperti rinviati"). In alternativa, eliminare la condizione $E_{dist}$ dal Cap.8 (decisione coerente con il criterio di rollback 5 del REPORT_CAP_02.md) demandando il vincolo distanza al filtro CAP-01 + alla geometria delle zone di Parte IV.

---

### N-4 — log di chiusura non registra $\Delta t$ pre-trigger (attesa raw touch)

**Posizione**: Cap.10.4 riga 309.

**Motivazione**: il log di chiusura registra "durata totale del lifecycle in minuti di trading dal `timestamp_emission` alla chiusura; **durata della fase post-trigger** in minuti di trading da $t_{exec}$ alla chiusura". Per differenza è ricostruibile la "durata pre-trigger" $t_{exec} - t_{emission}$, ma non è esplicitata nel log come campo a sé stante. Per il GA è una metrica direttamente rilevante (rapporto attesa/esecuzione, distribuzione del tempo di attesa pre-touch); rifletterla esplicitamente nel log evita derivazioni nel modulo analisi a valle. Non bloccante.

**Classificazione**: **N**

---

### N-5 — Cap.8.2 condizione di volatilità con $\leq$ filtra una sola coda

**Posizione**: Cap.8.2 riga 168-172.

**Motivazione**: $r_{1m}(t_{emission}) \leq \tau_{vol}(\hat{\sigma}(t_{emission}))$ impedisce emissione in barre estreme di volatilità (range alto). Ma non impedisce emissione in barre di range eccessivamente basso (mercato anomalmente fermo, possibile pre-anuncio macro). Il GA può preferire setup in regime di range strettamente positivo (escludendo barre quasi-piatte) ma non ha leva per esprimerlo nel contratto attuale. Osservazione per Parte III/V — non bloccante in Parte II.

**Classificazione**: **N**

---

### N-6 — backtest fill virtuale: rinvio a Parte III viola Cap.10.1 (determinismo)

**Posizione**: Cap.7.3 riga 128.

**Citazione**: "In simulazione di backtest il `trigger_event` viene trattato come fill virtuale a un prezzo determinato deterministicamente dalla regola di simulazione. La regola di riferimento è il fill al primo livello discreto della zona toccato dalla barra 1-min in cui si verifica il raw touch; **il dettaglio operativo della regola di simulazione è specificato in Parte III**."

**Motivazione**: il vincolo di determinismo di Cap.10.1 ($\texttt{replay}(H, B) = \texttt{replay}(H, B)$ bit-exact) si applica al replay del lifecycle, e il prezzo di fill è componente del log di chiusura (rendimento lordo). Se la regola è "specificata in Parte III", Parte II v2 non è autosufficiente per il replay deterministico. Coerente con la separazione delle responsabilità del documento, ma da segnalare come dipendenza esplicita: Parte III deve fissare la regola di fill virtuale **prima** che Cap.10.1 sia operativamente verificabile.

**Classificazione**: **N** (carryover Parte III).

---

### M-3 — patch CAP-01 da applicare a chiusura di CAP-02 v2

**Posizione**: trasversale, vedi B-4.

**Motivazione**: la propagazione retroattiva su CAP-01 (decorrenza cap 2gg + eliminazione "guardie di esecuzione" + ridefinizione `executable_rate`) è elemento del PASS del corpus v2. Da girare al supervisore come fix atomica.

**Classificazione**: **M**

---

## Tabella verifica acceptance criteria v2 (14 punti)

| # | Criterio | Esito v2 | Citazione/Posizione |
|---|----------|----------|---------------------|
| 1 | I 5 capitoli (Cap 6-10) presenti, completi, ordine corretto | OK | Sezioni `## Capitolo 6` ... `## Capitolo 10` |
| 2 | 8 eredità CAP-01 citate esplicitamente | OK con riserva | Tutte citate (intro Parte II e Cap.6.1); ma l'eredità #5 ("cap dall'emissione") è citata in forma divergente dall'originale CAP-01 — vedi B-4 |
| 3 | Cap 6: payload come tupla, tutti i campi, vincoli | OK | Cap.6.1 |
| 4 | Cap 6: payload immutabile + regola sostituzione | OK | Cap.6.2 e Cap.6.3 |
| 5 | Cap 7: 1 non-terminale + 7 terminali + transizioni + trigger come evento | OK con riserva | Cap.7.1, Cap.7.2, Cap.7.3. Conflitto formale su `target_1_hit` — vedi B-3 |
| 6 | Cap 7: cap 2gg come timer concreto | OK | Cap.7.4 (1680 min trading, esempio 21:55 chiuso) |
| 7 | Cap 7: M-1 a livello di interfaccia | OK | Cap.7.5 |
| 8 | Cap 8: 4 guardie nominate + rinvio Parte V soglie | **SUPERATO PER DECISIONE SUPERVISORE**: Cap.8 ora 3 condizioni di emissione | Cap.8.2 (volatilità/liquidità/distanza); Cap.8.3 (rinvio Parte V). AC formalmente non soddisfatto sulle "4 guardie" ma la riarchitettura è autorizzata. |
| 9 | Cap 8: nessuna assunzione fasi speciali (M-3 ritirato) | OK | Cap.8.4 con citazione corretta |
| 10 | Cap 9: anti-duplicato + nuovo messaggio per nuovo signal_id (no edit) | OK | Cap.9.4, Cap.9.5 |
| 11 | Cap 10: determinismo come vincolo, non desiderio | OK con riserva | Cap.10.1 (formula bit-exact). Dipendenza implicita da Parte III per regola di fill virtuale — N-6 |
| 12 | Registro tecnico italiano formale | OK | Tutto il documento |
| 13 | LaTeX inline e display | OK | Diverse sedi |
| 14 | Niente moltiplicazioni misleading o numeri inventati | OK | I provvisori ($L_{max}=30$s, $n_{retry}=3$, etc.) sono dichiarati come tali e rinviati a Parte V/Appendice E |

---

## Tabella verifica eredità CAP-01 (8 punti)

| # | Eredità | Esito v2 | Note |
|---|---------|----------|------|
| 1 | Sessione 8:00-22:00 CET finestra unica continua | OK | Intro Parte II, Cap.6.1, Cap.7.4, Cap.8.4, Cap.10.5 |
| 2 | Banda $b \in [b_{min}, 40]$, $b_{min}=5$ provvisorio | OK migliorato | Reso discreto $\{5,10,...,40\}$ (8 valori) coerente con tick FIB=5pt — vedi memory project_fib_instrument |
| 3 | Vincolo $d_{stop} > b$ | OK | Cap.6.1 |
| 4 | Target 1 e target 2 entrambi obbligatori | OK | Cap.6.1 |
| 5 | Cap validità $\leq 2$ giorni di trading | **DIVERGENTE** | CAP-01 dice "dall'emissione", Parte II v2 dice "dal raw touch". Coerenza retroattiva non eseguita — vedi B-4 |
| 6 | Movimento strutturale ancorato a primo pivot post-apertura | OK | Cap.7.5 |
| 7 | Filtro 80 pt FIB | OK | Cap.6.1; condizione $E_{dist}$ Cap.8.2 con $\max(\tau_{dist}, 80)$ — vedi NB-10 |
| 8 | No execution (punto 1 dichiarazione) | OK | Cap.7.3, Cap.8.1 |

---

## Tabella classificazione per il supervisore

| # | Problema | Classificazione | Azione richiesta |
|---|----------|-----------------|------------------|
| B-3 | `target_1_hit` formalmente non-terminale ma dichiarato tale; transizioni uscenti mancanti per scenari `stopped/expired/revoked` post-target_1 | **B** | Rework Cap.7 — opzione A (preferita): 2 non-terminali; richiede rinegoziazione AC #5 con supervisore |
| B-4 | Incoerenza retroattiva CAP-01 vs Parte II v2: cap 2gg dall'emissione (CAP-01) vs dal raw touch (Parte II); "guardie di esecuzione" residue in CAP-01 | **B** | Patch CAP-01 (righe 13, 75, 77). Da eseguire in parallelo o prima del PASS di CAP-02 v2 |
| NB-7 | Assenza timer pre-trigger: segnale può vivere `active` indefinitamente | NB | Decisione supervisore: reintrodurre `time_to_touch_max` oppure clausola "fine sessione di emissione" |
| NB-8 | Edge case raw touch: barra di emissione, gap apertura, barra che attraversa interamente la zona | NB | Specificare in Cap.7.3 le tre regole |
| NB-9 | Mancata transizione `target_1_hit → revoked` (e altre uscite post-target_1) | NB | Aggiunta righe tabella Cap.7.2 (allineata con B-3) |
| NB-10 | $\tau_{dist}$ con floor 80 produce intervallo $[0, 80]$ nullo del GA | NB | Ridefinire dominio o passare a moltiplicatore di $\hat{\sigma}$ |
| N-4 | Log chiusura non registra $\Delta t$ pre-trigger esplicito | N | Osservazione Cap.10.4 |
| N-5 | Condizione volatilità $\leq$ filtra solo coda alta | N | Osservazione Parte III/V |
| N-6 | Regola fill virtuale rinviata a Parte III contraddice determinismo Cap.10.1 | N | Carryover Parte III |
| M-3 | Patch CAP-01 (decorrenza, guardie, executable_rate) | M | Fix atomica trasversale |

**Conteggio v2**: B = 2, NB = 4, N = 3, M = 1.

---

## Sintesi finale per il supervisore (< 200 parole)

**Verdetto v2**: **CONDITIONAL**. La riscrittura integrale di Parte II v2 chiude correttamente tutti i finding di Review v1 (B-1, B-2, NB-1..NB-6) e implementa coerentemente le due decisioni strutturali del supervisore (decorrenza expiry dal raw touch; Cap.8 come condizioni pre-emissione + tick FIB=5pt formalizzato + banda discreta). Tuttavia emergono **due nuovi B**: (B-3) lo stato `target_1_hit` è formalmente non-terminale (ha una transizione uscente verso `target_2_hit`) ma è dichiarato terminale, con le transizioni `target_1_hit → stopped/expired/revoked` non specificate — il comportamento della state machine è non definito per gli scenari post-target_1; (B-4) il corpus v2 è internamente incoerente perché CAP-01 v2 chiuso a tag b76c32c dichiara ancora "cap 2gg dall'emissione" e "guardie di esecuzione" mentre Parte II v2 ha cambiato semantica — la patch CAP-01 segnalata nelle "Domande aperte" del REPORT_CAP_02.md non è stata eseguita. Quattro NB nuovi (timer pre-trigger assente, edge case raw touch, transizione `target_1_hit → revoked`, sovrapposizione $\tau_{dist}$ vs 80pt) richiedono rework.

**Raccomandazione**: rework Cap.7 per B-3 (opzione A: 2 non-terminali); patch CAP-01 per B-4 in tag atomico `[FIX-CARRYOVER]`; NB chirurgici. PASS atteso al ciclo v3.

