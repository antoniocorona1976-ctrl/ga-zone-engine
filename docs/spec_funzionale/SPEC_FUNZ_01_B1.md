# SPEC FUNZIONALE — Blocco B1: Ambito & operatore

> **Track**: Business-spec (SPEC-FUNZ). **Blocco**: B1 (1/8) della spec ricostruita a blocchi.
> **Stato**: documento **autonomo**; sarà ricomposto con B2..B8 in un'unica spec consolidata da un task di assemblaggio dedicato (fuori scope B1).
> **Fonte unica e autoritativa**: `docs/methodology_v2/CAP_01_parte_I.md`, **Capitoli 1, 2 e 3**, capitolo chiuso **PASS, SHA `b76c32c`**, **congelato** (freeze G-09): sola lettura.
> **Modalità di costruzione**: ricostruzione **cieca** (modalità B) dai soli Cap.1-3 — nessun riuso di ID o frasi da spec preesistenti.

---

## 0. Scopo del blocco

Questo blocco consolida, in forma di requisiti di prodotto verificabili, il **perimetro operativo di ambito e operatore** del sistema di generazione segnali sul FIB, così come formalizzato nei Capitoli 1-3 della Parte I della metodologia v2. Risponde, da solo, alle domande: *cosa fa il prodotto, su quale strumento e sessione opera, qual è il target dichiarato, esegue ordini?, chi è l'operatore e con quali vincoli, su quale canale/broker passano feed e segnali a livello di ambito*.

**Non** copre: payload formale del segnale, state-machine, condizioni di emissione, dettaglio consegna Telegram, schema-dato DAPI, gate di go-live, compute budget. Queste materie sono rinviate ai blocchi B2..B8 e ai capitoli metodologici (vedi §8 e la nota di rinvio §7.2).

Ogni requisito porta: un **ID auto-assegnato** (schema §1), una **proposizione atomica** (una sola asserzione verificabile, N1), una **tracciabilità** `[DOC-INTERNO CAP_01_parte_I.md:<riga>]` e un **valore operativo** per l'operatore retail FIB che riceve ed esegue manualmente il segnale da cellulare.

---

## 1. Schema degli ID requisito (auto-assegnato, NON importato)

Schema locale di questo blocco, numerazione propria che parte da zero:

- **`B1-R-NN`** — requisiti **funzionali / di ambito** (cosa fa o entro quale perimetro opera il prodotto).
- **`B1-CN-NN`** — requisiti **compliance / normativi / strutturali** (vincoli non rivedibili: classificazione MiFID II, "no esecuzione ordini").
- **`B1-NFR-NN`** — requisiti **non funzionali** (qualità/proprietà del prodotto: interpretabilità, fonte del feed, infrastruttura locale).

La numerazione è interna a B1 e non riusa la numerazione di alcuna spec preesistente.

**Convenzione tracciabilità**: la grafia canonica delle citazioni è `[DOC-INTERNO CAP_01_parte_I.md:<riga>]`. I riferimenti a documentazione esterna (MiFID II, Borsa Italiana / orari, Telegram, Directa, AWS) sono etichettati `[WIKI-HINT, da verificare]` e **non sono mai fonte unica**: ogni requisito regge sul CAP-fonte; l'esterno è solo hint concordante.

---

## 2. Ambito del prodotto-segnale (Cap.1)

### B1-R-01 — Oggetto del prodotto: generazione di segnali long/short sul FIB
**Proposizione**: il sistema genera segnali di tipo *long* e *short* sul FIB.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:9]`.
**Valore operativo**: definisce univocamente la natura di ciò che l'operatore riceve sul cellulare — indicazioni direzionali (comprare/vendere), non analisi generiche; l'operatore sa che ogni notifica è un'istruzione direzionale azionabile manualmente.

### B1-R-02 — Strumento: FIB, futures mini su FTSE MIB, mercato IDEM
**Proposizione**: lo strumento operativo è il FIB, contratto futures mini sull'indice FTSE MIB negoziato sul mercato IDEM di Borsa Italiana (codice strumento MIB).
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:9]`. Hint esterno concordante: `[WIKI-HINT Borsa Italiana / IDEM, da verificare]` (non fonte unica).
**Valore operativo**: l'operatore opera su un solo strumento noto, quotato sul mercato regolamentato italiano accessibile dal suo broker; nessuna ambiguità su quale contratto inserire da cellulare.

### B1-R-03 — Sessione operativa di ambito: 8:00-22:00 CET, finestra unica e continua
**Proposizione**: la sessione operativa di riferimento è la finestra FIB **8:00-22:00 CET**, intesa come finestra unica e continua di negoziazione.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:9]`. Hint esterno concordante: `[WIKI-HINT Borsa Italiana Trading Hours, da verificare]` (non fonte unica).
**Valore operativo**: l'operatore sa entro quale finestra giornaliera attendersi segnali e quando deve essere reperibile/attento al cellulare; fuori da questa finestra non riceve segnali da gestire.

### B1-R-04 — Perimetro di emissione coincidente con la sessione
**Proposizione**: i segnali sono emessi e processati esclusivamente all'interno della finestra 8:00-22:00 CET.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:9]`.
**Valore operativo**: l'operatore non deve presidiare il cellulare al di fuori della sessione per timore di segnali fuori orario; il perimetro di attenzione è circoscritto e prevedibile.

### B1-R-05 — Target operativo, prima formulazione: 500 punti FIB di profitto netto giornaliero
**Proposizione**: una delle due formulazioni del target operativo dichiarato è **500 punti FIB di profitto netto giornaliero**.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:11]`.
**Valore operativo**: dà all'operatore un obiettivo di rendimento giornaliero esprimibile in punti (quindi in euro, via moltiplicatore), con cui misurare se la giornata operativa è in linea con le aspettative.

### B1-R-06 — Target operativo, seconda formulazione: 70% del movimento strutturale intraday
**Proposizione**: la formulazione alternativa del target operativo è il **70% del movimento strutturale intraday** dello strumento.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:11]`.
**Valore operativo**: nelle giornate a basso movimento, dove i 500 punti sono irrealistici, l'operatore dispone di un metro di successo proporzionato al movimento effettivamente disponibile, evitando di considerare "fallita" una giornata strutturalmente povera.

### B1-R-07 — Definizione di movimento strutturale intraday
**Proposizione**: il movimento strutturale intraday è definito come la **somma dei moduli degli swing fra i prezzi strutturali** (pivot) identificati nella sessione, distinto dal range max−min di sessione.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:11]`.
**Valore operativo**: chiarisce all'operatore che il metro di successo del target-70% non è la sola escursione massima della giornata, ma quanto movimento utile è stato concretamente disponibile lungo i pivot — coerente con un'operatività che cattura più swing.

### B1-R-08 — Ancoraggio del movimento strutturale al primo pivot post-apertura
**Proposizione**: il 70% si applica al movimento strutturale calcolato dall'intervallo che va dal **primo minimo o primo massimo post-apertura** (dalle 8:00 CET) fino alla chiusura della sessione alle 22:00 CET.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:11]`; decisione del supervisore `[DOC-INTERNO tasks/QUESTIONS.md:Q-02]` (autoritativa, non riaperta).
**Valore operativo**: garantisce che il target-70% esista in ogni sessione indipendentemente dal fatto che il sistema emetta o no segnali; l'operatore ha sempre un riferimento di giornata ben definito.

### B1-R-09 — Soglia minima asimmetrica dei 500 punti nelle sessioni ad alto movimento
**Proposizione**: nelle sessioni ad alto movimento strutturale, i 500 punti rappresentano una **soglia minima assoluta** sotto la quale il motore è considerato sub-performante.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:11]`.
**Valore operativo**: l'operatore sa che, quando il mercato offre molto movimento, il sistema deve comunque consegnare almeno 500 punti; protegge dall'accontentarsi di poco in giornate ricche.

### B1-R-10 — Natura intraday del segnale
**Proposizione**: i segnali generati sono di **natura intraday**.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:13]`.
**Valore operativo**: imposta l'aspettativa di default dell'operatore — la posizione si apre e tipicamente si chiude nell'arco della giornata, compatibile con un monitoraggio discontinuo da cellulare durante l'orario di lavoro.

### B1-R-11 — Estensione multiday condizionata della validità
**Proposizione**: la validità del segnale **può estendersi oltre la chiusura della sessione corrente** (multiday) laddove le condizioni di mercato lo consentano e vi sia evidente possibilità di incrementare il profitto o recuperare la perdita.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:13]`.
**Valore operativo**: l'operatore è avvisato che alcuni segnali possono richiedere di mantenere la posizione oltre la giornata; deve organizzarsi per non chiudere meccanicamente tutto a fine sessione quando il segnale resta valido.

### B1-R-12 — Tetto massimo di estensione multiday: 2 giorni di trading dal raw touch
**Proposizione**: l'estensione della validità del segnale eseguito non supera **2 giorni di trading** decorrenti dall'esecuzione (raw touch della entry zone).
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:13]`; decisione del supervisore `[DOC-INTERNO tasks/QUESTIONS.md:Q-04]` (autoritativa, non riaperta).
**Valore operativo**: dà all'operatore un limite certo entro cui una posizione tenuta multiday va comunque chiusa; nessuna posizione resta indefinitamente aperta in attesa.

### B1-R-13 — Contesto cross-index per la classificazione del regime (a livello di ambito)
**Proposizione**: il sistema utilizza il contesto degli indici correlati (DAX, EuroStoxx50, S&P futures) per **classificare il regime di mercato** sul FIB (movimento idiosincratico vs sistemico).
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:17]`.
**Valore operativo**: spiega all'operatore perché i segnali tengono conto del quadro europeo/globale e non solo del FTSE MIB; la classificazione di regime contribuisce a contestualizzare i segnali che riceve.

### B1-R-14 — Uso del contesto cross-index per validare la direzione del segnale (a livello di ambito)
**Proposizione**: il sistema utilizza il contesto degli indici correlati anche per **validare la direzione del segnale** rispetto al contesto macro.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:17]`.
**Valore operativo**: l'operatore ha maggiore fiducia che la direzione long/short suggerita non sia in contrasto evidente con il contesto di mercato più ampio.

### B1-R-15 — Uso del contesto cross-index per la componente di rischio sistemico (a livello di ambito)
**Proposizione**: il sistema utilizza il contesto degli indici correlati per **stimare la componente di rischio sistemico** nella volatilità del FIB.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:17]`.
**Valore operativo**: contribuisce a che i segnali riflettano il rischio sistemico in corso, informazione utile all'operatore che gestisce manualmente l'esposizione.

---

## 3. Vincolo strutturale "solo emissione, nessuna esecuzione di ordini" (Cap.1)

### B1-CN-01 — Il sistema non esegue ordini in alcuna fase (vincolo strutturale)
**Proposizione**: il sistema **non esegue ordini autonomamente in alcuna fase** del suo ciclo di vita; questa proprietà è un **vincolo strutturale, non una scelta implementativa rivedibile**.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:15]`.
**Valore operativo**: garanzia di compliance e di controllo per l'operatore retail — nessun ordine parte mai senza la sua azione; il sistema non può aprire o chiudere posizioni al posto suo.

### B1-CN-02 — Il sistema pubblica segnali su un canale di notifica
**Proposizione**: il sistema **pubblica segnali strutturati su un canale di notifica** (l'output del sistema è la pubblicazione del segnale).
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:15]`.
**Valore operativo**: l'operatore sa che riceverà i segnali come notifiche e che il prodotto si esaurisce nella pubblicazione, non nell'azione di mercato.

### B1-CN-03 — Apertura, invio, gestione e chiusura competono all'operatore umano
**Proposizione**: la decisione di apertura, l'invio dell'ordine, la gestione della posizione e la chiusura **competono esclusivamente all'operatore umano**, che agisce manualmente attraverso l'interfaccia del broker.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:15]`.
**Valore operativo**: definisce con precisione il confine di responsabilità — l'operatore resta l'unico decisore e attuatore di ogni operazione, coerentemente con la sua esecuzione manuale da cellulare.

---

## 4. Profilo operatore e vincoli operativi (Cap.2)

### B1-CN-04 — Operatore retail non professionale ai sensi MiFID II
**Proposizione**: l'operatore destinatario è classificato come **operatore retail non professionale ai sensi della direttiva MiFID II**, e tale classificazione è un dato immutabile per il sistema.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:23]`. Riferimento normativo esterno: `[WIKI-HINT MiFID II, da verificare]` (non fonte unica).
**Valore operativo**: la classificazione retail determina vincoli di accesso a strumenti/leve e regimi di tutela che il sistema assume come dati; l'operatore opera entro il regime di protezione previsto per il retail.

### B1-R-16 — Interazione da cellulare durante la giornata lavorativa
**Proposizione**: l'operatore interagisce con il broker **da cellulare durante la giornata lavorativa**.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:23]`.
**Valore operativo**: è il canale fisico con cui l'operatore esegue i segnali; vincola il prodotto a essere usabile da mobile.

### B1-R-17 — Monitoraggio discontinuo
**Proposizione**: l'operatore opera in modo **discontinuo** e non può garantire presenza continuativa di fronte allo schermo.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:23]`.
**Valore operativo**: il prodotto non può presupporre attenzione costante; i segnali devono restare gestibili anche se l'operatore non è presente in ogni istante.

### B1-NFR-01 — Segnali interpretabili e azionabili da operatore non continuativo
**Proposizione**: i segnali devono essere **interpretabili e azionabili** da un operatore che non può garantire presenza continuativa di fronte allo schermo.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:23]`.
**Valore operativo**: requisito di qualità del prodotto — un segnale chiaro e auto-contenuto consente all'operatore di agire correttamente anche dopo un'assenza, da cellulare, senza dover ricostruire il contesto.

### B1-R-18 — Dimensionamento fisso: 1 contratto FIB alla volta
**Proposizione**: il dimensionamento della posizione è fissato a **1 contratto FIB alla volta**; la gestione della size è esplicitamente esclusa dal perimetro del sistema.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:25]`.
**Valore operativo**: l'operatore non riceve mai indicazioni di size; opera sempre con un solo contratto, semplificando l'esecuzione manuale e rendendo immediato il calcolo del P&L.

### B1-CN-05 — Commissione di 5 EUR per operazione
**Proposizione**: le commissioni del broker sono assunte pari a **5 EUR per operazione**, sia di apertura sia di chiusura.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:25]`. Riferimento esterno: `[WIKI-HINT tariffe Directa, da verificare]` (non fonte unica).
**Valore operativo**: l'operatore conosce il costo per operazione da scontare dal rendimento lordo di ogni eseguito.

### B1-R-19 — Equivalenza commissione-punti: 5 EUR = 1 punto FIB; ciclo completo = 2 punti
**Proposizione**: in punti FIB equivalenti, 5 EUR corrispondono a **1 punto**, e ciascun ciclo completo apertura-chiusura grava sul rendimento lordo per **2 punti FIB**.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:25]`.
**Valore operativo**: dà all'operatore la regola immediata per convertire le commissioni in punti e capire quanto un trade deve guadagnare lordo per essere in pari netto (≥ 2 punti).

### B1-R-20 — Distinzione fra stop loss strutturale del segnale e stop personale dell'operatore
**Proposizione**: lo **stop loss strutturale del segnale** si distingue dallo **stop loss personale dell'operatore**: quest'ultimo (di norma a −200 punti dopo il fill) è una misura di prudenza dell'utilizzatore, non un parametro del modello e non calibrato dal sistema.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:31]`.
**Valore operativo**: l'operatore capisce che lo stop che il sistema gli comunica (strutturale) è cosa diversa dallo stop di emergenza che lui stesso imposta; non li confonde nell'esecuzione manuale.

### B1-R-21 — Rollover come vincolo operativo di ambito
**Proposizione**: la gestione del **rollover** dello strumento in scadenza è riconosciuta come **problematica operativa specifica del FIB**, di cui il sistema deve tenere conto producendo segnali consistenti sul contratto correntemente attivo.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:33]`.
**Valore operativo**: avvisa l'operatore che in avvicinamento alla scadenza c'è il tema del passaggio di contratto; il dettaglio della policy è rinviato (vedi §7.2), ma a livello di ambito l'operatore sa che i segnali si riferiscono al contratto attivo.

---

## 5. Strumento FIB — caratteristiche economiche rilevanti (Cap.1-2)

### B1-R-22 — Moltiplicatore: 5 EUR per punto indice
**Proposizione**: il contratto FIB ha un moltiplicatore di **5 EUR per punto indice**: ogni movimento di un punto del sottostante vale 5 EUR di variazione del valore della posizione (a 1 contratto).
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:9]`, `[DOC-INTERNO CAP_01_parte_I.md:25]`.
**Valore operativo**: consente all'operatore di convertire ogni segnale espresso in punti nel suo controvalore in euro, base per ogni valutazione di rischio/rendimento dell'esecuzione manuale.

### B1-NFR-02 — Granularità del prezzo desumibile dall'esempio di banda (tick 5pt — assunzione esplicita, RM-1)
**Proposizione**: i prezzi/livelli strutturali del FIB sono trattati su una griglia a passo 5 punti (esempio di banda `41100 41140`).
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:27]` (esempio di banda `+- 40pt ad es 41100 41140`).
**Stato RM-1** — il CAP-fonte **non** asserisce esplicitamente "tick 5pt"; la griglia a 5pt è **desunta** dall'esempio numerico, non verificata di prima istanza in questo blocco:
```
VERIFICA: il tick/granularità del FIB è 5 punti (prezzi multipli di 5).
PROVE: esempio di banda nel CAP-fonte, livelli 41100 e 41140 (entrambi multipli di 5) [DOC-INTERNO CAP_01_parte_I.md:27].
ALTERNATIVE ESCLUSE: nessuna esclusa dal solo esempio.
ALTERNATIVE NON ESCLUSE: che la griglia reale del FIB abbia tick diverso (es. 1pt) e che 41100/41140 siano solo valori d'esempio arrotondati. La conferma del tick è materia empirica/di schema-dato (rinvio a B6/CAP-DATA), non asserita come verificata qui.
```
**Valore operativo**: l'operatore inserisce manualmente prezzi coerenti con la granularità dello strumento; la conferma del tick effettivo è rinviata e non va data per acquisita su base di questo solo blocco.

---

## 6. Canale e infrastruttura a livello di ambito (Cap.3)

### B1-NFR-03 — Infrastruttura locale: PC mobile dell'operatore
**Proposizione**: l'infrastruttura locale di sviluppo, backtest leggero e forward-run è un **personal computer mobile dell'operatore**, sul quale il sistema deve poter essere sviluppato, eseguito in inference real-time e operato.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:39]`.
**Valore operativo**: il prodotto deve girare sull'hardware che l'operatore già possiede per il forward-run; nessuna dipendenza locale da macchine non disponibili.

### B1-NFR-04 — Feed real-time proveniente da Directa SIM
**Proposizione**: il **broker operativo è Directa SIM** e il **feed real-time della sessione deve provenire da Directa**, non da fornitori terzi.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:41]`. Riferimento esterno: `[WIKI-HINT Directa SIM, da verificare]` (non fonte unica).
**Valore operativo**: l'operatore usa il proprio broker sia per ricevere i dati che alimentano il sistema sia per eseguire; coerenza fra ciò che vede il sistema e ciò su cui l'operatore opera.

### B1-R-23 — Necessità di storico FIB per il training (a livello di ambito)
**Proposizione**: il sistema richiede una **serie storica del FIB** a barre 1-minuto, di profondità minima cinque anni, per l'addestramento.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:43]`.
**Valore operativo**: a livello di ambito chiarisce che la qualità dei segnali dipende dalla disponibilità di uno storico adeguato; è una precondizione del prodotto (il dettaglio fornitore/formato è rinviato — §7.2).

### B1-R-24 — Necessità di dati cross-index storici e real-time (a livello di ambito)
**Proposizione**: il sistema richiede **dati storici e real-time sugli indici DAX, EuroStoxx50 e S&P futures** per la componente cross-index di classificazione del regime.
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:45]`.
**Valore operativo**: è la precondizione-dato che abilita i requisiti di contesto (B1-R-13/14/15); a livello di ambito l'operatore/progetto sa che servono questi feed aggiuntivi.

### B1-R-25 — Canale di pubblicazione dei segnali: bot Telegram personale (a livello di ambito)
**Proposizione**: il canale di pubblicazione dei segnali emessi in forward-run è un **bot Telegram personale dell'operatore**, già attivo (a livello di ambito: "i segnali sono pubblicati via Telegram").
**Tracciabilità**: `[DOC-INTERNO CAP_01_parte_I.md:47]`. Riferimento esterno: `[WIKI-HINT Telegram Bot, da verificare]` (non fonte unica).
**Valore operativo**: l'operatore riceve i segnali su Telegram dal proprio cellulare, canale che già usa; il **dettaglio di consegna** (schema messaggio, chat ID, latenza) è esplicitamente rinviato (vedi §7.2).

---

## 7. Matrice di tracciabilità e nota di rinvio

### 7.1 — Matrice di tracciabilità del blocco

| ID | Proposizione (sintesi) | Citazione CAP | Valore operativo (sintesi) |
|---|---|---|---|
| B1-R-01 | Genera segnali long/short sul FIB | `:9` | natura direzionale dell'output |
| B1-R-02 | Strumento FIB, FTSE MIB, IDEM | `:9` | strumento unico e noto |
| B1-R-03 | Sessione 8:00-22:00 CET, continua | `:9` | finestra di reperibilità |
| B1-R-04 | Emissione solo entro la sessione | `:9` | perimetro di attenzione circoscritto |
| B1-R-05 | Target: 500 punti netti/giorno | `:11` | obiettivo giornaliero misurabile |
| B1-R-06 | Target alt.: 70% movimento strutturale | `:11` | metro proporzionato nelle giornate povere |
| B1-R-07 | Def. movimento strutturale (somma moduli swing) | `:11` | metro = movimento utile, non solo range |
| B1-R-08 | Ancoraggio al primo pivot post-apertura | `:11` + Q-02 | target sempre definito |
| B1-R-09 | 500 punti = soglia minima (alto movimento) | `:11` | non accontentarsi nelle giornate ricche |
| B1-R-10 | Natura intraday del segnale | `:13` | aspettativa di default infragiornaliera |
| B1-R-11 | Estensione multiday condizionata | `:13` | non chiudere meccanicamente a fine sessione |
| B1-R-12 | Tetto 2 giorni di trading dal raw touch | `:13` + Q-04 | limite certo di durata |
| B1-R-13 | Cross-index per classificazione regime | `:17` | contestualizzazione dei segnali |
| B1-R-14 | Cross-index per validazione direzione | `:17` | direzione coerente col macro |
| B1-R-15 | Cross-index per rischio sistemico | `:17` | segnali consapevoli del rischio sistemico |
| B1-CN-01 | No esecuzione ordini (vincolo strutturale) | `:15` | compliance/controllo operatore |
| B1-CN-02 | Pubblica segnali su canale di notifica | `:15` | output = notifica |
| B1-CN-03 | Apertura/gestione/chiusura all'operatore | `:15` | confine di responsabilità |
| B1-CN-04 | Operatore retail non professionale MiFID II | `:23` | regime di tutela retail |
| B1-R-16 | Interazione da cellulare in giornata lavorativa | `:23` | canale fisico di esecuzione |
| B1-R-17 | Monitoraggio discontinuo | `:23` | nessuna presenza continua richiesta |
| B1-NFR-01 | Segnali interpretabili/azionabili | `:23` | usabilità da mobile dopo assenza |
| B1-R-18 | 1 contratto FIB alla volta | `:25` | nessuna gestione size |
| B1-CN-05 | Commissione 5 EUR/operazione | `:25` | costo per operazione noto |
| B1-R-19 | 5 EUR = 1 punto; ciclo = 2 punti | `:25` | break-even in punti |
| B1-R-20 | Stop strutturale ≠ stop personale | `:31` | non confondere i due stop |
| B1-R-21 | Rollover come vincolo di ambito | `:33` | segnali sul contratto attivo |
| B1-R-22 | Moltiplicatore 5 EUR/punto | `:9`, `:25` | conversione punti↔euro |
| B1-NFR-02 | Griglia 5pt (assunzione RM-1) | `:27` | coerenza prezzi inseriti a mano |
| B1-NFR-03 | Infrastruttura: PC mobile dell'operatore | `:39` | gira sull'hardware esistente |
| B1-NFR-04 | Feed real-time da Directa SIM | `:41` | coerenza dati/esecuzione |
| B1-R-23 | Storico FIB 1-min ≥5 anni (ambito) | `:43` | precondizione di qualità |
| B1-R-24 | Dati cross-index storici e RT (ambito) | `:45` | precondizione-dato del contesto |
| B1-R-25 | Canale Telegram (ambito) | `:47` | ricezione segnali su mobile |

**Conteggio per famiglia**: `B1-R` = 25 (R-01..R-25), `B1-CN` = 5 (CN-01..CN-05), `B1-NFR` = 4 (NFR-01..NFR-04, di cui B1-NFR-02 con cautela RM-1). **Totale = 34 requisiti.**

### 7.2 — Nota di rinvio (materia di Cap.1-3 deliberatamente NON consolidata in B1)

Le seguenti materie sono **presenti nei Cap.1-3** ma **deliberatamente rinviate** ad altri blocchi/sedi, per rispetto del confine "tutto e solo" di B1. Non sono omissioni: sono rinvii motivati.

| Materia di Cap.1-3 non consolidata in B1 | Perché fuori da B1 | Destinazione |
|---|---|---|
| Payload del segnale: direzione + banda $b$ + target 1/2 + stop strutturale come **schema** (`:25`, `:27`) | B1 è ambito/operatore, non struttura del payload | **B2** (payload) |
| Dominio della semi-ampiezza $b \in [b_{min},40]$, $b_{min}=5$, vincolo $d_{stop} > b$ (`:27`, `:29`) | parametri/vincoli geometrici del cromosoma, non ambito | **B2** (payload) |
| Timer di attesa pre-esecuzione, raw touch, ottimizzazione timing post-esecuzione (`:13`) | lifecycle/state-machine del segnale | **B3** (state-machine & lifecycle) |
| Dettaglio consegna Telegram: schema messaggio, chat ID, latenza (`:47`) | è dettaglio di consegna, non ambito di canale | **B4** (emissione & consegna) |
| Policy di rollover (regola di switch su spread futures/cash) (`:33`) | dettaglio di policy operativa | **Parte VI** (capitolo dedicato) / blocco compliance **B5** |
| Sessione come **requisito operativo** runtime + verifica empirica orario (M-GOV-1) (`:9`) | in B1 la sessione è solo ambito; il runtime è altrove | **B5** (runtime, sessione & compliance) |
| Storico: fornitore Portara/CQG, stitching, formato, costo (`:43`) | dettaglio di approvvigionamento dati | **Appendice D** / blocco schema-dato **B6** |
| Sorgenti dati cross-index: feed/granularità/costo (`:45`) | qualificazione sorgenti, non ambito | **Appendice C** / **B6** |
| Interfacce Directa (Darwin/DAPI/Visual Trader), porte 10001/10003, tariffa DAPI (`:41`) | dettaglio tecnico delle interfacce | **Appendice C** / schema-dato **B6** |
| Compute budget e strategia cloud (Cap.4) | non è ambito/operatore; dimensionamento infra | non tracciato in spec / Appendice operativa |
| Definizione quantitativa del successo, $E[R_{net}]$, DSR/PBO, filtro 80pt, metriche lifecycle/rischio (Cap.5) | gate di go-live, non ambito | **B7** (gate di go-live) |

---

## 8. Confine di scope (riepilogo)

B1 copre **tutto e solo** l'ambito di prodotto e il profilo operatore dei Capitoli 1-3 della Parte I: oggetto e strumento del prodotto, sessione di ambito, target operativo (doppia formulazione), natura intraday/multiday di ambito, contesto cross-index di ambito, vincolo strutturale "solo emissione", profilo e vincoli dell'operatore retail, caratteristiche economiche del FIB, canale e infrastruttura a livello di ambito. Tutto ciò che attiene a payload, lifecycle, emissione/consegna di dettaglio, schema-dato, gate di go-live, compute budget e fasizzazione è rinviato (§7.2 e tabella out-of-scope della task card).
