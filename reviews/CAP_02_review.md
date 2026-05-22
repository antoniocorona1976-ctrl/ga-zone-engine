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
