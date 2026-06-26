# SPEC-FUNZ-01 — Specifica funzionale di prodotto (PHASE-1 FIB-only) — assemblato loss-less della serie B1..B8

**Track**: Business-spec (non-CAP). **Versione**: assemblato (merge editoriale loss-less degli 8 blocchi B1..B8 già chiusi PASS e post-AUDITFIX-01). Rimpiazza la v2 (archiviata in `SPEC_FUNZ_01_v2_storico.md`).
**Scopo**: consolidare in **un unico documento autoritativo** tutti i requisiti di prodotto del motore di segnali FIB (PHASE-1 FIB-only), ottenuti dal merge fedele degli 8 blocchi della ricostruzione a blocchi. Ogni requisito è tracciabile 1-a-1 al proprio ID-blocco originario e alla riga-CAP della metodologia v2 (matrice unica + tabella di mapping, §11).
**Vista**: operatore/prodotto. Questo NON è un capitolo metodologico: non ridefinisce metodologia, non introduce parametri del GA, non riapre decisioni `D-*-N` né AC delle Review dei capitoli. È il ponte fra il documento metodologico chiuso e la successiva FASE-D di implementazione.

---

## Nota di testa — provenienza e cautele di fonte (RM-1/RM-3)

- **Natura dell'assemblato**: questo documento è il **merge loss-less** degli 8 documenti-blocco `SPEC_FUNZ_01_B1.md` .. `SPEC_FUNZ_01_B8.md` (fonte autoritativa del merge), ciascuno già chiuso PASS nel proprio ciclo e già emendato dall'audit `SPEC-FUNZ-01-AUDITFIX-01` (review `392a3f5`). I **375 requisiti-blocco** entrano nell'assemblato con mappatura 1-a-1; nessun requisito è perso o inventato (vedi §11 tabella di mapping; il conteggio 375 — non 374 — è dovuto a B5 che ha 36 requisiti effettivi, non 35, vedi nota §11.1). I **CAP della metodologia v2 NON sono toccati** (freeze G-09): le citazioni `[DOC-INTERNO CAP_XX:riga]` sono richiami in sola lettura, già verificate token-per-token nei rispettivi cicli-blocco e nell'AUDITFIX-01.
- **Fonte unica e autoritativa di ogni requisito**: i capitoli metodologia v2 **chiusi PASS** (`docs/methodology_v2/CAP_*.md`), congelati G-09. Ogni asserzione fattuale è un **richiamo etichettato** a un capitolo chiuso (`[DOC-INTERNO CAP_XX_parte_*.md:<riga>]`), a codice di produzione (`[CODICE-ESISTENTE path:linea]`, grafia canonica), o a una prova già chiusa (`[PROVA-EMPIRICA <data>]`). L'assemblato **non introduce** nuove dichiarazioni "verificato X" di prima istanza: i blocchi `VERIFICA/PROVE/ALTERNATIVE` esistenti (B1-NFR-02 → R-1.13; schemi CANDLE/PRICE/BOOK_5 di B6 → Sez.9) sono **preservati verbatim** dai blocchi, non riscritti né estesi.
- **SHA-review pinnabili dei capitoli-fonte** (riportati come effettivamente presenti nei blocchi-fonte, non inventati): CAP-01 Parte I `b76c32c`; CAP-02 Parte II `a1625df`; CAP-07 Parte VII `b27c1e3`; CAP-01 Cap.5 via `e8d5424`; CAP-08 Parte 8 `015c47a`; CAP-09 Parte 9 `28cfd2d`; CAP-10 Parte 10 `41447d3`. Il blocco B4-EXT (Sez.6, materia di consegna CAP_06 Parte VI Cap.29) cita `CAP_06_parte_VI.md` senza pin SHA esplicito nel blocco-fonte: l'assemblato non ne inventa uno (RM-1).
- **Documentazione esterna** (MiFID II, wiki Directa, Telegram Bot API, Borsa Italiana, Portara/CQG, CME/Eurex): sempre `[WIKI-HINT, da verificare]`, mai fonte unica di un'asserzione strutturale. La **wiki Directa è dimostrata inesatta** sullo schema CANDLE (`O;H;L;C` dichiarato, `C;L;H;O` reale): citata solo con avvertenza esplicita (vedi Sez.9, R-9.4 e blocco RM-1).
- **Grafia etichette**: `[CODICE-ESISTENTE …]` (canonica). La grafia storica deprecata (con "X" al posto di "S") è vietata in questo documento.
- **Cardine edge-PENDING (eredità B7/B8, vincolante)**: l'assemblato **non emette alcuna asserzione d'esito d'edge** (DSR/PBO/OOS/`E[R_net]`/GO-NO-GO). Criteri e soglie sono riportati come **dichiarati/provvisori**, mai come esiti. I verbi vietati ("il bundle supera/passa il gate", "DSR è positivo/significativo", "l'edge esiste/è confermato", "GO") sono assenti. L'esito d'edge è esclusiva del ruolo `validator` in FASE-D (vedi Sez.8 nota di confine e §13).
- **Blocchi aperti incardinati**: B-1 (latenza Telegram $L_{max}=30$s, M-2 OPEN) e B-2 (orario sessione FIB, M-GOV-1 in attesa di upgrade a PROVA-EMPIRICA). Vedi §13 "Blocchi / Domande aperte". I requisiti dipendenti portano il tag `[B-1 PROVVISORIO]` / `[B-2 PROVVISORIO]`.
- **Schema-ID dell'assemblato**: sezione-based `R-x.y` / `NFR-x.y` / `CN-x.y`, con `x` = numero di Sezione (1..10) e `y` progressivo per famiglia dentro la sezione. La mappatura 1-a-1 con l'ID-blocco originario è nella tabella di mapping §11.2.

---

## Sezione 1 — Obiettivo di prodotto, ambito, vincolo "solo emissione" (da B1)

**Valore di prodotto della sezione**: definisce *cosa fa* il prodotto, su quale strumento e sessione opera, qual è il target dichiarato, e il confine non negoziabile fra segnale (motore) ed esecuzione (operatore), da cui discende l'intera compliance del sistema.

### 1.1 Ambito del prodotto-segnale

- **R-1.1** — Il sistema genera segnali di tipo *long* e *short* sul FIB.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:9]`.
  - *Valore operativo*: definisce univocamente la natura di ciò che l'operatore riceve sul cellulare — indicazioni direzionali (comprare/vendere), non analisi generiche; ogni notifica è un'istruzione direzionale azionabile manualmente.

- **R-1.2** — Lo strumento operativo è il FIB, contratto futures mini sull'indice FTSE MIB negoziato sul mercato IDEM di Borsa Italiana (codice strumento MIB).
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:9]`. Hint esterno concordante: `[WIKI-HINT Borsa Italiana / IDEM, da verificare]` (non fonte unica).
  - *Valore operativo*: l'operatore opera su un solo strumento noto, quotato sul mercato regolamentato italiano accessibile dal suo broker; nessuna ambiguità su quale contratto inserire da cellulare.

- **R-1.3** — La sessione operativa di riferimento è la finestra FIB **8:00-22:00 CET**, intesa come finestra unica e continua di negoziazione.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:9]`. Hint esterno concordante: `[WIKI-HINT Borsa Italiana Trading Hours, da verificare]` (non fonte unica).
  - *Valore operativo*: l'operatore sa entro quale finestra giornaliera attendersi segnali e quando deve essere reperibile/attento al cellulare; fuori da questa finestra non riceve segnali da gestire.
  - *(Nota: la sessione come **requisito operativo runtime** è consolidata in Sez.7 / R-7.11, con la dipendenza aperta M-GOV-1; qui è ambito.)*

- **R-1.4** — I segnali sono emessi e processati esclusivamente all'interno della finestra 8:00-22:00 CET.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:9]`.
  - *Valore operativo*: l'operatore non deve presidiare il cellulare al di fuori della sessione per timore di segnali fuori orario; il perimetro di attenzione è circoscritto e prevedibile.

- **R-1.5** — Una delle due formulazioni del target operativo dichiarato è **500 punti FIB di profitto netto giornaliero**.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:11]`.
  - *Valore operativo*: dà all'operatore un obiettivo di rendimento giornaliero esprimibile in punti (quindi in euro, via moltiplicatore), con cui misurare se la giornata operativa è in linea con le aspettative.

- **R-1.6** — La formulazione alternativa del target operativo è il **70% del movimento strutturale intraday** dello strumento.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:11]`.
  - *Valore operativo*: nelle giornate a basso movimento, dove i 500 punti sono irrealistici, l'operatore dispone di un metro di successo proporzionato al movimento effettivamente disponibile, evitando di considerare "fallita" una giornata strutturalmente povera.

- **R-1.7** — Il movimento strutturale intraday è definito come la **somma dei moduli degli swing fra i prezzi strutturali** (pivot) identificati nella sessione, distinto dal range max−min di sessione.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:11]`.
  - *Valore operativo*: chiarisce che il metro di successo del target-70% non è la sola escursione massima della giornata, ma quanto movimento utile è stato concretamente disponibile lungo i pivot.

- **R-1.8** — Il 70% si applica al movimento strutturale calcolato dall'intervallo che va dal **primo minimo o primo massimo post-apertura** (dalle 8:00 CET) fino alla chiusura della sessione alle 22:00 CET.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:11]`; decisione del supervisore `[DOC-INTERNO tasks/QUESTIONS.md:Q-02]` (autoritativa, non riaperta).
  - *Valore operativo*: garantisce che il target-70% esista in ogni sessione indipendentemente dal fatto che il sistema emetta o no segnali; l'operatore ha sempre un riferimento di giornata ben definito.

- **R-1.9** — Nelle sessioni ad alto movimento strutturale, i 500 punti rappresentano una **soglia minima assoluta** sotto la quale il motore è considerato sub-performante.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:11]`.
  - *Valore operativo*: l'operatore sa che, quando il mercato offre molto movimento, il sistema deve comunque consegnare almeno 500 punti; protegge dall'accontentarsi di poco in giornate ricche.

- **R-1.10** — I segnali generati sono di **natura intraday**.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:13]`.
  - *Valore operativo*: imposta l'aspettativa di default — la posizione si apre e tipicamente si chiude nell'arco della giornata, compatibile con un monitoraggio discontinuo da cellulare.

- **R-1.11** — La validità del segnale **può estendersi oltre la chiusura della sessione corrente** (multiday) laddove le condizioni di mercato lo consentano e vi sia evidente possibilità di incrementare il profitto o recuperare la perdita.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:13]`.
  - *Valore operativo*: l'operatore è avvisato che alcuni segnali possono richiedere di mantenere la posizione oltre la giornata; deve organizzarsi per non chiudere meccanicamente tutto a fine sessione quando il segnale resta valido.

- **R-1.12** — L'estensione della validità del segnale eseguito non supera **2 giorni di trading** decorrenti dall'esecuzione (raw touch della entry zone).
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:13]`; decisione del supervisore `[DOC-INTERNO tasks/QUESTIONS.md:Q-04]` (autoritativa, non riaperta).
  - *Valore operativo*: dà all'operatore un limite certo entro cui una posizione tenuta multiday va comunque chiusa; nessuna posizione resta indefinitamente aperta.

- **R-1.13** — Il sistema utilizza il contesto degli indici correlati (DAX, EuroStoxx50, S&P futures) per **classificare il regime di mercato** sul FIB (movimento idiosincratico vs sistemico).
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:17]`.
  - *Valore operativo*: spiega all'operatore perché i segnali tengono conto del quadro europeo/globale e non solo del FTSE MIB.

- **R-1.14** — Il sistema utilizza il contesto degli indici correlati anche per **validare la direzione del segnale** rispetto al contesto macro.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:17]`.
  - *Valore operativo*: l'operatore ha maggiore fiducia che la direzione long/short suggerita non sia in contrasto evidente con il contesto di mercato più ampio.

- **R-1.15** — Il sistema utilizza il contesto degli indici correlati per **stimare la componente di rischio sistemico** nella volatilità del FIB.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:17]`.
  - *Valore operativo*: contribuisce a che i segnali riflettano il rischio sistemico in corso, informazione utile all'operatore che gestisce manualmente l'esposizione.

### 1.2 Caratteristiche economiche rilevanti del FIB

- **R-1.16** — Il contratto FIB ha un moltiplicatore di **5 EUR per punto indice**: ogni movimento di un punto del sottostante vale 5 EUR di variazione del valore della posizione (a 1 contratto).
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:9]`, `[DOC-INTERNO CAP_01_parte_I.md:25]`.
  - *Valore operativo*: consente di convertire ogni segnale espresso in punti nel suo controvalore in euro, base per ogni valutazione di rischio/rendimento dell'esecuzione manuale.

- **NFR-1.1** — I prezzi/livelli strutturali del FIB sono trattati su una griglia a passo 5 punti (esempio di banda `41100 41140`).
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:27]` (esempio di banda `+- 40pt ad es 41100 41140`).
  - *Stato RM-1* — il CAP-fonte **non** asserisce esplicitamente "tick 5pt"; la griglia a 5pt è **desunta** dall'esempio numerico, non verificata di prima istanza (blocco preservato verbatim da B1-NFR-02):
    ```
    VERIFICA: il tick/granularità del FIB è 5 punti (prezzi multipli di 5).
    PROVE: esempio di banda nel CAP-fonte, livelli 41100 e 41140 (entrambi multipli di 5) [DOC-INTERNO CAP_01_parte_I.md:27].
    ALTERNATIVE ESCLUSE: nessuna esclusa dal solo esempio.
    ALTERNATIVE NON ESCLUSE: che la griglia reale del FIB abbia tick diverso (es. 1pt) e che 41100/41140 siano solo valori d'esempio arrotondati. La conferma del tick è materia empirica/di schema-dato (rinvio a Sez.9), non asserita come verificata qui.
    ```
  - *Valore operativo*: l'operatore inserisce manualmente prezzi coerenti con la granularità dello strumento; la conferma del tick effettivo è rinviata (Sez.9) e non va data per acquisita su base di questo solo requisito.

### 1.3 Vincolo strutturale "solo emissione, nessuna esecuzione di ordini"

- **CN-1.1** — Il sistema **non esegue ordini autonomamente in alcuna fase** del suo ciclo di vita; questa proprietà è un **vincolo strutturale, non una scelta implementativa rivedibile**.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:15]`.
  - *Valore operativo*: garanzia di compliance e di controllo per l'operatore retail — nessun ordine parte mai senza la sua azione; il sistema non può aprire o chiudere posizioni al posto suo. *(Clausola di chiusura runtime: porta ordini 10002 mai aperta → Sez.7 / CN-7.1.)*

- **CN-1.2** — Il sistema **pubblica segnali strutturati su un canale di notifica** (l'output del sistema è la pubblicazione del segnale).
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:15]`.
  - *Valore operativo*: l'operatore sa che riceverà i segnali come notifiche e che il prodotto si esaurisce nella pubblicazione, non nell'azione di mercato.

- **CN-1.3** — La decisione di apertura, l'invio dell'ordine, la gestione della posizione e la chiusura **competono esclusivamente all'operatore umano**, che agisce manualmente attraverso l'interfaccia del broker.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:15]`.
  - *Valore operativo*: definisce con precisione il confine di responsabilità — l'operatore resta l'unico decisore e attuatore di ogni operazione.

**Out-of-scope della Sezione 1**:
| Voce | Destinazione |
|---|---|
| Payload del segnale come schema (campi, domini, banda $b$, target/stop) | **Sez.3** (da B2) |
| Lifecycle/state-machine, timer, raw touch come evento | **Sez.4** (da B3) |
| Matematica del movimento strutturale e pivot detection | Parti III/IV (CAP chiusi, vedi §12) |
| Sessione come requisito operativo runtime + verifica empirica orario (M-GOV-1) | **Sez.7** (da B5) |
| Definizione quantitativa del successo, $E[R_{net}]$, DSR/PBO, filtro 80pt, metriche lifecycle/rischio | **Sez.8** (gate di go-live, da B7) |

---

## Sezione 2 — Destinatario, modalità di consumo, canale e infrastruttura (da B1)

**Valore di prodotto della sezione**: definisce *chi* è l'operatore, con quali vincoli opera, qual è il dimensionamento, su quale canale/broker passano feed e segnali a livello di ambito, e quali precondizioni-dato il prodotto richiede.

### 2.1 Profilo operatore e vincoli operativi

- **CN-2.1** — L'operatore destinatario è classificato come **operatore retail non professionale ai sensi della direttiva MiFID II**, e tale classificazione è un dato immutabile per il sistema.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:23]`. Riferimento normativo esterno: `[WIKI-HINT MiFID II, da verificare]` (non fonte unica).
  - *Valore operativo*: la classificazione retail determina vincoli di accesso a strumenti/leve e regimi di tutela che il sistema assume come dati.

- **R-2.1** — L'operatore interagisce con il broker **da cellulare durante la giornata lavorativa**.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:23]`.
  - *Valore operativo*: è il canale fisico con cui l'operatore esegue i segnali; vincola il prodotto a essere usabile da mobile.

- **R-2.2** — L'operatore opera in modo **discontinuo** e non può garantire presenza continuativa di fronte allo schermo.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:23]`.
  - *Valore operativo*: il prodotto non può presupporre attenzione costante; i segnali devono restare gestibili anche se l'operatore non è presente in ogni istante.

- **NFR-2.1** — I segnali devono essere **interpretabili e azionabili** da un operatore che non può garantire presenza continuativa di fronte allo schermo.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:23]`.
  - *Valore operativo*: requisito di qualità del prodotto — un segnale chiaro e auto-contenuto consente di agire correttamente anche dopo un'assenza, da cellulare, senza ricostruire il contesto.

- **R-2.3** — Il dimensionamento della posizione è fissato a **1 contratto FIB alla volta**; la gestione della size è esplicitamente esclusa dal perimetro del sistema.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:25]`.
  - *Valore operativo*: l'operatore non riceve mai indicazioni di size; opera sempre con un solo contratto, semplificando l'esecuzione manuale e il calcolo del P&L.

- **CN-2.2** — Le commissioni del broker sono assunte pari a **5 EUR per operazione**, sia di apertura sia di chiusura.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:25]`. Riferimento esterno: `[WIKI-HINT tariffe Directa, da verificare]` (non fonte unica).
  - *Valore operativo*: l'operatore conosce il costo per operazione da scontare dal rendimento lordo di ogni eseguito.

- **R-2.4** — In punti FIB equivalenti, 5 EUR corrispondono a **1 punto**, e ciascun ciclo completo apertura-chiusura grava sul rendimento lordo per **2 punti FIB**.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:25]`.
  - *Valore operativo*: dà la regola immediata per convertire le commissioni in punti e capire quanto un trade deve guadagnare lordo per essere in pari netto (≥ 2 punti).

- **R-2.5** — Lo **stop loss strutturale del segnale** si distingue dallo **stop loss personale dell'operatore**: quest'ultimo (di norma a −200 punti dopo il fill) è una misura di prudenza dell'utilizzatore, non un parametro del modello e non calibrato dal sistema.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:31]`.
  - *Valore operativo*: l'operatore capisce che lo stop comunicato dal sistema (strutturale) è cosa diversa dallo stop di emergenza che lui stesso imposta; non li confonde nell'esecuzione manuale.

- **R-2.6** — La gestione del **rollover** dello strumento in scadenza è riconosciuta come **problematica operativa specifica del FIB**, di cui il sistema deve tenere conto producendo segnali consistenti sul contratto correntemente attivo.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:33]`.
  - *Valore operativo*: avvisa l'operatore che in avvicinamento alla scadenza c'è il tema del passaggio di contratto; il dettaglio della policy di switch runtime è in Sez.7 (R-7.4..R-7.6).

### 2.2 Canale e infrastruttura a livello di ambito

- **NFR-2.2** — L'infrastruttura locale di sviluppo, backtest leggero e forward-run è un **personal computer mobile dell'operatore**, sul quale il sistema deve poter essere sviluppato, eseguito in inference real-time e operato.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:39]`.
  - *Valore operativo*: il prodotto deve girare sull'hardware che l'operatore già possiede per il forward-run; nessuna dipendenza locale da macchine non disponibili.

- **NFR-2.3** — Il **broker operativo è Directa SIM** e il **feed real-time della sessione deve provenire da Directa**, non da fornitori terzi.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:41]`. Riferimento esterno: `[WIKI-HINT Directa SIM, da verificare]` (non fonte unica).
  - *Valore operativo*: l'operatore usa il proprio broker sia per ricevere i dati che alimentano il sistema sia per eseguire; coerenza fra ciò che vede il sistema e ciò su cui l'operatore opera.

- **R-2.7** — Il sistema richiede una **serie storica del FIB** a barre 1-minuto, di profondità minima cinque anni, per l'addestramento.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:43]`.
  - *Valore operativo*: a livello di ambito chiarisce che la qualità dei segnali dipende dalla disponibilità di uno storico adeguato; è una precondizione del prodotto (dettaglio fornitore/formato → Sez.9 e §12).

- **R-2.8** — Il sistema richiede **dati storici e real-time sugli indici DAX, EuroStoxx50 e S&P futures** per la componente cross-index di classificazione del regime.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:45]`.
  - *Valore operativo*: è la precondizione-dato che abilita i requisiti di contesto (R-1.13/1.14/1.15).

- **R-2.9** — Il canale di pubblicazione dei segnali emessi in forward-run è un **bot Telegram personale dell'operatore**, già attivo (a livello di ambito: "i segnali sono pubblicati via Telegram").
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:47]`. Riferimento esterno: `[WIKI-HINT Telegram Bot, da verificare]` (non fonte unica).
  - *Valore operativo*: l'operatore riceve i segnali su Telegram dal proprio cellulare, canale che già usa; il **dettaglio di consegna** (schema messaggio, latenza, mobile-first) è in Sez.6.

**Out-of-scope della Sezione 2**:
| Voce | Destinazione |
|---|---|
| Dettaglio consegna Telegram: schema messaggio, ordine campi, latenza, mobile-first | **Sez.6** (da B4) |
| Policy di rollover runtime (switch su scadenza, CONTRACT_SWITCH) | **Sez.7** (da B5) |
| Interfacce Directa (Darwin/DAPI), porte 10001/10003, tariffa DAPI | **Sez.7** (canale, da B5) / **Sez.9** (schema-dato, da B6) |
| Storico: fornitore Portara/CQG, stitching, formato, costo | **Sez.9** (da B6) / Appendice D |
| Dualità miniFIB (1€)/FIB-pieno (5€) per l'esecuzione | **Sez.7 / R-7.10** (da B5) |
| Compute budget e strategia cloud (Cap.4) | non tracciato in spec / §12 |

---

## Sezione 3 — Payload del segnale (da B2)

**Valore di prodotto della sezione**: specifica il payload del segnale FIB come oggetto-dato contrattuale e immutabile — i campi della tupla pubblicata, dominio e vincoli di ciascun campo, e le proprietà invarianti (immutabilità post-emissione; segnale unico attivo; sostituzione-non-edit).

### 3.1 Il segnale come oggetto-payload immutabile

- **R-3.1** — Il payload del segnale è una **tupla strutturata $\mathcal{S}$** composta esattamente dai dodici campi `signal_id`, `timestamp_emission`, `direction`, `entry_zone`, `target_1`, `target_2`, `target_2_type`, `stop_loss`, `stop_type`, `setup_class`, $\Delta t_{cromosoma}$, $T_{touch}^{max}$.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:17, :19]`.
  - *Valore operativo*: l'operatore riceve un oggetto unico e completo con tutti i parametri necessari alla decisione di ingresso; un payload a struttura fissa rende la lettura mobile prevedibile.

### 3.2 `signal_id`

- **R-3.2** — `signal_id` è l'**identificatore univoco** del segnale, assegnato dal motore all'emissione, e funge da chiave primaria del segnale.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:23]`.
  - *Valore operativo*: dà all'operatore una chiave non ambigua con cui riconoscere a quale segnale si riferiscono le comunicazioni successive.

- **R-3.3** — `signal_id` è un valore **opaco non riutilizzabile**.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:23]`.
  - *Valore operativo*: lo stesso identificatore non torna mai a designare un secondo segnale diverso; l'operatore non rischia di confondere un vecchio segnale con uno nuovo che ne riusi la chiave.

- **R-3.4** — L'unicità di `signal_id` è garantita sull'**intero orizzonte operativo del motore**, non soltanto sulla sessione corrente.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:23]`.
  - *Valore operativo*: anche a distanza di mesi un `signal_id` resta una chiave non collidente; le tracce storiche restano riferibili senza ambiguità.

### 3.3 `timestamp_emission`

- **R-3.5** — `timestamp_emission` è l'**istante di emissione** del segnale, espresso **al minuto chiuso**.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:25]`.
  - *Valore operativo*: comunica quanto è "fresco" il segnale; la precisione al minuto è coerente con la granularità (barre 1-min) su cui il segnale è calcolato.

- **R-3.6** — Il riferimento orario di `timestamp_emission` è **CET**.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:25]`.
  - *Valore operativo*: fissa un fuso univoco; l'operatore italiano legge l'orario nel proprio fuso locale senza conversioni.

### 3.4 `direction`

- **R-3.7** — `direction` ha dominio $\{\text{long}, \text{short}\}$.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:27]`.
  - *Valore operativo*: è l'informazione che dice se comprare o vendere; un dominio binario chiuso elimina ogni ambiguità sul verso dell'operazione.

### 3.5 `entry_zone` e banda di ingresso

- **R-3.8** — `entry_zone` è una **banda di prezzo discreta** attorno al prezzo strutturale di riferimento $p_{ref}$, definita come insieme dei livelli $\{p_{ref}-b,\ p_{ref}-b+5,\ \ldots,\ p_{ref}+b-5,\ p_{ref}+b\}$.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:29, :31]`.
  - *Valore operativo*: dice l'intervallo di prezzo entro cui posizionarsi per l'ingresso; esprimerla come insieme di livelli discreti è coerente col fatto che i prezzi del FIB esistono solo a multipli di 5.

- **R-3.9** — Il prezzo di riferimento $p_{ref}$ è **multiplo di 5** ed è **fissato al momento dell'emissione**.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:33]`.
  - *Valore operativo*: ancora la banda a un livello realmente quotabile sul FIB e ne fissa il centro all'emissione.

### 3.6 `target_1` e `target_2`

- **R-3.10** — `target_1` è un **prezzo strutturale di obiettivo**, **obbligatorio**.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:35]`.
  - *Valore operativo*: dà il primo livello di presa di profitto; l'obbligatorietà garantisce che ogni segnale arrivi con un obiettivo esplicito.

- **R-3.11** — `target_2` è un **prezzo strutturale di obiettivo**, **obbligatorio**.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:35]`.
  - *Valore operativo*: dà un secondo livello di riferimento strutturale per gestire la posizione oltre il primo obiettivo.

- **R-3.12** — `target_1` e `target_2` sono **distinti** (valori diversi).
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:35]`.
  - *Valore operativo*: due livelli distinti danno due riferimenti separati; evita un payload degenere coi due obiettivi coincidenti.

- **R-3.13** — `target_1` è **multiplo di 5**.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:35]`.
  - *Valore operativo*: l'obiettivo è espresso a un livello realmente quotabile, impostabile come ordine limite.

- **R-3.14** — `target_2` è **multiplo di 5**.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:35]`.
  - *Valore operativo*: il secondo obiettivo è quotabile sul FIB, coerente con la granularità dello strumento.

- **R-3.15** — Per i segnali **long** vale l'ordine $\texttt{target\_1} > p_{ref}$.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:35]`.
  - *Valore operativo*: per un long il primo obiettivo è sopra il riferimento; coerenza fra verso dell'operazione e posizione dell'obiettivo.

- **R-3.16** — Per i segnali **long** vale l'ordine $\texttt{target\_2} > \texttt{target\_1}$.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:35]`.
  - *Valore operativo*: per un long il secondo obiettivo è più lontano del primo nella direzione del profitto; presa di profitto crescente e prevedibile.

- **R-3.17** — Per i segnali **short** vale l'ordine $\texttt{target\_1} < p_{ref}$.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:35]`.
  - *Valore operativo*: per uno short il primo obiettivo è sotto il riferimento; coerenza immediata fra verso e posizione dell'obiettivo.

- **R-3.18** — Per i segnali **short** vale l'ordine $\texttt{target\_2} < \texttt{target\_1}$.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:35]`.
  - *Valore operativo*: per uno short il secondo obiettivo è più lontano del primo verso il basso; presa di profitto ordinata nel verso corretto.

- **R-3.19** — `target_1` e `target_2` sono entrambi **ancorati a livelli strutturali** del prezzo (non sono obiettivi arbitrari non strutturali).
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:35]`.
  - *Valore operativo*: gli obiettivi corrispondono a livelli che il prezzo riconosce strutturalmente; l'operatore opera su riferimenti dotati di significato di mercato.

- **R-3.20** — `target_2` è **informazione strutturale pubblicata**, non variabile di lifecycle del segnale: è un attributo informativo del payload, mentre il contratto del segnale si chiude al raggiungimento di `target_1` (Q-05, Clausola 2).
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:37]` (decisione Q-05 al `:7`).
  - *Valore operativo*: l'operatore riceve `target_2` come secondo riferimento decisionale per gestire manualmente la posizione oltre il primo obiettivo, sapendo che è informazione strutturale e non un secondo "trade" gestito dal motore. *(target_2 come **evento** del position lifecycle → Sez.4 / R-4.41, R-4.45, CN-4.8.)*

### 3.7 `target_2_type`

- **R-3.21** — `target_2_type` è un **campo del payload** con dominio $\{\text{structural}, \text{synthetic}\}$, che qualifica la natura del livello `target_2` pubblicato.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:39]`.
  - *Valore operativo*: dice se il secondo obiettivo poggia su una struttura confermata o è un livello calcolato; informazione utile per pesare la fiducia nel target.

- **R-3.22** — Nel campo `target_2_type`, il valore `synthetic` ha **natura informativa derivata da una regola del modello** (livello calcolato), distinta dal valore `structural` che indica un livello derivato da struttura confermata del prezzo.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:39]`.
  - *Valore operativo*: rende esplicito che un `target_2` `synthetic` è meno "ancorato" di uno `structural`.

### 3.8 `stop_loss`

- **R-3.23** — `stop_loss` è un **prezzo strutturale di stop**, **multiplo di 5**.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:41]`.
  - *Valore operativo*: dà il livello di protezione a un prezzo realmente quotabile, impostabile come stop.

- **R-3.24** — Si definisce la distanza dello stop dal riferimento come $d_{stop} = |p_{ref} - \texttt{stop\_loss}|$, in punti FIB.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:43]`.
  - *Valore operativo*: quantifica l'ampiezza del rischio (distanza dal riferimento allo stop), grandezza centrale per dimensionare la perdita massima attesa per contratto.

### 3.9 `stop_type`

- **R-3.25** — `stop_type` è un **campo del payload** con dominio $\{\text{structural}, \text{synthetic}\}$, che qualifica la natura del livello `stop_loss` pubblicato.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:51]`.
  - *Valore operativo*: dice se lo stop poggia su una struttura confermata o è un livello calcolato; informazione utile per valutare la robustezza del livello di protezione.

- **R-3.26** — Nel campo `stop_type`, il valore `synthetic` ha **natura informativa derivata da una regola del modello**, distinta dal valore `structural` che indica un livello derivato da struttura confermata del prezzo.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:51]`.
  - *Valore operativo*: rende esplicito che uno `stop_loss` `synthetic` è derivato da una regola del modello e non da una struttura confermata.

- **R-3.27** — Il dominio di `stop_type` **non** include valori prodotti dall'operatore: il motore **non gestisce stop manuali**.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:51]`.
  - *Valore operativo*: chiarisce il confine di responsabilità — lo stop nel payload è quello strutturale del motore; ogni stop personale è fuori dal contratto del segnale e di esclusiva responsabilità dell'operatore.

### 3.10 `setup_class`

- **R-3.28** — `setup_class` è un **campo del payload** con dominio $\{\text{directional}, \text{trade\_range}\}$, che classifica la natura del setup.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:53]`.
  - *Valore operativo*: dice di che tipo di setup si tratta (movimento direzionale vs operatività entro un range), contesto per la lettura del segnale.

- **R-3.29** — A ciascun valore di `setup_class` è **associato un filtro di emissione di 80 punti FIB** (per `directional`: $|\texttt{target\_1} - p_{ref}| \geq 80$; per `trade_range`: $A_{range} \geq 80$).
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:53, :55, :59]`.
  - *Valore operativo*: garantisce che ogni segnale pubblicato abbia un'ampiezza minima significativa (almeno 80 punti). *(La **regola di emissione** che applica il filtro è materia di Sez.5 / R-5.4; la definizione operativa di $A_{range}$ è Parte IV, §12.)*

### 3.11 $\Delta t_{cromosoma}$ e $T_{touch}^{max}$ (campi/parametri del payload)

- **R-3.30** — $\Delta t_{cromosoma}$ è un **campo/parametro del payload** di dominio discreto intero $\{1, 2, \ldots, 1680\}$ minuti di trading.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:63]`.
  - *Valore operativo*: fissa la durata massima della fase post-trigger del segnale; pur tecnico, fa parte del payload congelato. *(Semantica del timer → Sez.4 / R-4.32..35.)*

- **R-3.31** — $T_{touch}^{max}$ è un **campo/parametro del payload** di dominio discreto intero $\{5, 6, \ldots, 480\}$ minuti di trading.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:69]`.
  - *Valore operativo*: fissa la durata massima della fase di attesa pre-trigger; fa parte del payload congelato. *(Semantica del timer → Sez.4 / R-4.36..38.)*

### 3.12 Banda di ingresso $b$

- **R-3.32** — La semi-ampiezza della banda $b$ ha **dominio discreto** $\{5, 10, 15, 20, 25, 30, 35, 40\}$ punti FIB (cardinalità 8).
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:33]` (preambolo `:5`, `:9`).
  - *Valore operativo*: definisce l'insieme finito di ampiezze possibili della zona di ingresso; un dominio chiuso e discreto rende prevedibile quanto larga possa essere al massimo la zona (al più 40 punti per lato).

- **R-3.33** — La semi-ampiezza $b$ è **multipla di 5** (punti FIB), coerentemente col tick dello strumento.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:9, :33]`.
  - *Valore operativo*: i bordi della banda cadono su livelli realmente quotabili sul FIB.

- **R-3.34** — Il valore minimo $b_{min} = 5$ punti FIB corrisponde esattamente a **1 tick** del FIB.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:9, :33]`.
  - *Valore operativo*: stabilisce la zona di ingresso più stretta possibile come un singolo tick di larghezza per lato; la banda minima non è mai nulla.

- **R-3.35** — `entry_zone` è l'**insieme discreto** dei livelli multipli di 5 da $p_{ref}-b$ a $p_{ref}+b$ a passo 5.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:29, :31]`.
  - *Valore operativo*: l'operatore vede esattamente quali livelli di prezzo costituiscono la zona, tutti realmente quotabili.

- **R-3.36** — La **cardinalità** della banda è $(2b/5) + 1$ livelli discreti.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:33]`.
  - *Valore operativo*: rende calcolabile e prevedibile quanti livelli compongono la zona per ogni $b$.

- **R-3.37** — Il floor $b_{min}=5$ esiste per **evitare una banda di ingresso nulla** (convergenza del modello su zone a banda zero).
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:33]`.
  - *Valore operativo*: garantisce che ogni segnale arrivi con una zona di ingresso effettivamente operabile (mai a larghezza zero).

### 3.13 Invarianti contrattuali del payload

- **CN-3.1** *(invariante strutturale)* — Vale il **vincolo geometrico obbligatorio** $d_{stop} > b$: la distanza dello stop dal riferimento deve essere strettamente maggiore della semi-ampiezza della banda. Cromosomi che producono segnali in violazione sono dichiarati non validi.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:47, :49]`.
  - *Valore operativo*: evita che un fill al bordo opposto della banda coincida con il prezzo di stop (segnale eseguito e immediatamente stoppato nello stesso tick); protegge da un'operazione strutturalmente perdente per costruzione.

- **CN-3.2** *(invariante strutturale)* — Una volta emesso, il segnale identificato da `signal_id` **non subisce alcuna modifica al proprio payload**: la tupla $\mathcal{S}$ è **congelata al momento dell'emissione**.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:73]`.
  - *Valore operativo*: l'operatore opera su valori che non cambiano fra il momento della lettura e quello dell'invio dell'ordine; nessun parametro muta a sua insaputa.

- **CN-3.3** *(invariante strutturale)* — **Non esiste** un'operazione di refresh o di edit del segnale che lasci invariato `signal_id` e modifichi uno qualsiasi dei campi del payload.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:73]`.
  - *Valore operativo*: a parità di `signal_id` l'operatore ha la garanzia assoluta che i valori siano sempre quelli pubblicati; la chiave identifica un contenuto immutabile.

- **CN-3.4** *(invariante strutturale)* — Vale il vincolo **segnale unico attivo**: $|\mathcal{A}(t)| \leq 1$ per ogni $t$ (al massimo un solo segnale attivo a ogni istante), dove $\mathcal{A}(t)$ è l'insieme dei segnali attivi al tempo $t$.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:79, :81]`.
  - *Valore operativo*: l'operatore ha al più un segnale operabile per volta, coerente con l'operatività a 1 contratto alla volta; nessuna sovrapposizione di segnali concorrenti.

- **CN-3.5** *(invariante strutturale)* — Una "revisione" del segnale **non è un edit** del payload esistente: il motore emette un **nuovo `signal_id`** con una **nuova tupla $\mathcal{S}'$ completa e indipendente**, anch'essa congelata.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:77, :83]`.
  - *Valore operativo*: quando le condizioni cambiano l'operatore riceve un segnale nuovo e riconoscibile invece di un aggiornamento silenzioso del precedente. *(La **meccanica delle transizioni** della sostituzione — revoca, stati terminali — è Sez.4 / R-4.15, R-4.16, R-4.23.)*

**Out-of-scope della Sezione 3**:
| Voce | Destinazione |
|---|---|
| State machine, raw touch come evento, semantica dei timer, meccanica della sostituzione | **Sez.4** (da B3) |
| Condizioni di emissione e regola che applica il filtro 80pt; definizione di $A_{range}$ | **Sez.5** (da B4) / Parte IV (§12) |
| Contratto del messaggio Telegram, ordine campi, latenza, anti-duplicato | **Sez.6** (da B4) |
| Log di emissione/transizioni/chiusura, replay/determinismo | **Sez.7/Sez.9** |
| Derivazione matematica dei livelli (geometria del prezzo, $\hat{\sigma}_{pt}$, livelli synthetic) | Parti III/IV (§12) |

---

## Sezione 4 — State-machine & lifecycle del segnale (da B3)

**Valore di prodotto della sezione**: consolida la semantica dinamica del ciclo di vita del segnale — gli stati che il segnale attraversa, gli eventi che ne provocano le transizioni, la temporizzazione (timer pre/post-trigger), il contratto di osservazione real-time del primo pivot, e la submacchina distinta che traccia la posizione oltre `target_1`. La submacchina di posizione (Cap.11) arriva qui dalle citazioni **corrette** del blocco B3 (vedi §10 auto-check no-reintroduzione).

### 4.1 Stati del segnale e semantica

- **R-4.1** — La state machine del segnale è costituita da **un solo stato non-terminale** (`active`) e **sei stati terminali** (`target_1_hit`, `stopped`, `invalidated`, `missed_target`, `expired`, `revoked`). `[DOC-INTERNO CAP_02_parte_II.md:95]` `[DOC-INTERNO CAP_02_parte_II.md:7]`
  - *Valore operativo*: definisce in modo chiuso l'insieme degli esiti possibili di un segnale, così che l'operatore sappia che ogni segnale può concludersi solo in uno di sei esiti noti e non in stati indefiniti.

- **R-4.2** — Lo stato `target_2_hit` **non** fa parte della state machine del segnale (rimosso per decisione Q-05, Clausola 1). `[DOC-INTERNO CAP_02_parte_II.md:7]` `[DOC-INTERNO CAP_02_parte_II.md:129]`
  - *Valore operativo*: l'operatore sa che il sistema non gestisce target_2 come esito del segnale; il raggiungimento di target_2 è gestione di posizione di sua competenza (vedi §4.6).

- **R-4.3** — Un segnale entra nello stato `active` quando è stato emesso e la sua tupla è pubblicata; in `active` il segnale è in attesa di un evento che lo porti in uno stato terminale. `[DOC-INTERNO CAP_02_parte_II.md:97]`
  - *Valore operativo*: l'operatore che riceve un segnale `active` sa che il segnale è "vivo" e in attesa di azione/evento, non già concluso.

- **R-4.4** — Mentre il segnale è `active`, il motore osserva il prezzo corrente e calcola gli eventi di mercato pertinenti (raw touch della entry zone, raggiungimento di target o stop prima del raw touch, scadenza del timer pre/post-trigger, invalidazione strutturale, decisione di sostituzione) applicando le transizioni previste. `[DOC-INTERNO CAP_02_parte_II.md:97]`
  - *Valore operativo*: garantisce che, finché il segnale è attivo, il sistema continua a monitorare le condizioni che possono chiuderlo, senza che l'operatore debba calcolarle a mano.

- **R-4.5** — `target_1_hit` è lo stato terminale di **successo** del contratto del segnale. `[DOC-INTERNO CAP_02_parte_II.md:101]`
  - *Valore operativo*: comunica all'operatore che il segnale ha centrato il proprio primo obiettivo strutturale, l'esito atteso del trade.

- **R-4.6** — La condizione d'ingresso in `target_1_hit` è: dopo il raw touch della entry zone, il prezzo raggiunge `target_1` prima di `stop_loss`, prima della scadenza del timer post-trigger e prima di un'eventuale invalidazione strutturale. `[DOC-INTERNO CAP_02_parte_II.md:101]` `[DOC-INTERNO CAP_02_parte_II.md:122]`
  - *Valore operativo*: definisce senza ambiguità quando il segnale è "vinto", così che l'operatore riconosca l'esito anche osservando il prezzo da sé.

- **R-4.7** — Il raggiungimento di `target_1_hit` **chiude definitivamente il contratto del segnale**. `[DOC-INTERNO CAP_02_parte_II.md:101]`
  - *Valore operativo*: dice che, una volta raggiunto target_1, quel segnale non verrà più sostituito né riaperto e la gestione della posizione oltre target_1 è interamente dell'operatore.

- **R-4.8** — `stopped` è lo stato terminale in cui il segnale entra quando, dopo il raw touch della entry zone, il prezzo raggiunge `stop_loss` prima di `target_1`, prima della scadenza del timer post-trigger e prima di un'eventuale invalidazione strutturale. `[DOC-INTERNO CAP_02_parte_II.md:103]` `[DOC-INTERNO CAP_02_parte_II.md:123]`
  - *Valore operativo*: comunica l'esito di perdita "ordinaria" (stop colpito dopo essere entrato), distinto dagli esiti in cui l'ingresso non è mai avvenuto.

- **R-4.9** — `invalidated` è lo stato terminale in cui il segnale entra quando, **prima** del raw touch della entry zone, si verifica una condizione di invalidazione strutturale che rompe l'ipotesi del setup. `[DOC-INTERNO CAP_02_parte_II.md:105]` `[DOC-INTERNO CAP_02_parte_II.md:124]`
  - *Valore operativo*: avverte che il setup è decaduto **prima** di poter entrare, quindi l'operatore non deve eseguire alcun ordine su quel segnale.

- **R-4.10** — Fra le condizioni di invalidazione esplicitamente incluse nel contratto del segnale rientra il superamento del livello `stop_loss` da parte del prezzo, nella direzione contraria all'ipotesi del segnale, prima del raw touch (per i long, $p(t) \leq \texttt{stop\_loss}$ con $t < t_{touch}$; simmetricamente per gli short). `[DOC-INTERNO CAP_02_parte_II.md:105]` `[DOC-INTERNO CAP_02_parte_II.md:124]`
  - *Valore operativo*: chiarisce che un prezzo che sfonda lo stop prima ancora di toccare la zona segnala un'ipotesi già smentita, e il segnale non va eseguito.

- **CN-4.1** — Lo stato `invalidated` (invalidazione strutturale prima del raw touch, incluso lo stop attraversato pre-touch) è **distinto** da `stopped` (che richiede un raw touch precedente). `[DOC-INTERNO CAP_02_parte_II.md:105]`
  - *Valore operativo*: distingue due esiti di segno opposto in termini di azione richiesta — `stopped` = "sei entrato e hai preso lo stop", `invalidated` = "non saresti dovuto entrare".

- **R-4.11** — `missed_target` è lo stato terminale in cui il segnale entra quando, **prima** del raw touch della entry zone, il prezzo raggiunge `target_1`. `[DOC-INTERNO CAP_02_parte_II.md:107]` `[DOC-INTERNO CAP_02_parte_II.md:125]`
  - *Valore operativo*: comunica che il target strutturale è stato realizzato dal mercato ma il setup non si è eseguito perché la zona di ingresso non è mai stata toccata (occasione "persa", non perdita).

- **R-4.12** — La metrica/riferimento di `missed_target` è ancorata a `target_1` e **non** a `target_2`. `[DOC-INTERNO CAP_02_parte_II.md:107]`
  - *Valore operativo*: il sistema misura le occasioni perse rispetto al primo obiettivo strutturale, coerentemente con la chiusura di prodotto.

- **R-4.13** — `expired` è lo stato terminale in cui il segnale entra alla scadenza di un timer di validità. `[DOC-INTERNO CAP_02_parte_II.md:109]`
  - *Valore operativo*: garantisce che nessun segnale resta indefinitamente "aperto": alla scadenza viene chiuso e non richiede più attenzione.

- **R-4.14** — Lo stato `expired` registra la causa della scadenza tramite un **campo causale strutturato** con due valori (`posttrigger_timeout`, `pretrigger_timeout`), **non** tramite due stati distinti. `[DOC-INTERNO CAP_02_parte_II.md:109]`
  - *Valore di sistema/validazione*: mantiene il vincolo di 6 soli stati terminali (Q-05, Clausola 1) preservando nel log la distinzione fra scadenza pre- e post-ingresso, necessaria all'analisi della calibrazione dei timer; per l'operatore l'esito vissuto è unico ("scaduto").

- **R-4.15** — `revoked` è lo stato terminale in cui il segnale entra quando è stato **superseduto** dall'emissione di un nuovo `signal_id`. `[DOC-INTERNO CAP_02_parte_II.md:111]`
  - *Valore operativo*: avverte che il segnale precedente non è più valido perché il motore ne ha emesso uno nuovo aggiornato, e va abbandonato a favore del nuovo.
  - *(Premessa di seam: il **meccanismo** della supersessione — segnale superseduto da nuovo `signal_id`, segnale unico attivo / sostituzione-non-edit — è consolidato come proprietà del payload in Sez.3 / CN-3.4, CN-3.5 (`[DOC-INTERNO CAP_02_parte_II.md:77]`); qui se ne richiama la conseguenza sul lifecycle, senza ri-derivarlo.)*

- **R-4.16** — La revoca avviene **contestualmente** all'emissione del nuovo segnale e interrompe il lifecycle del precedente. `[DOC-INTERNO CAP_02_parte_II.md:111]`
  - *Valore operativo*: garantisce che non esiste un istante in cui due segnali sono validi insieme: nel momento in cui arriva il nuovo, il vecchio è già revocato.

- **CN-4.2** — Nessuno stato terminale ammette transizioni uscenti: il ciclo di vita del segnale è definitivamente chiuso all'ingresso in qualsiasi stato terminale. `[DOC-INTERNO CAP_02_parte_II.md:99]`
  - *Valore operativo*: assicura che un esito comunicato è definitivo — un segnale "vinto", "stoppato" o "scaduto" non potrà più cambiare stato e tornare a richiedere azione.

- **CN-4.3** — La transizione `target_1_hit → revoked` **non esiste**: un segnale già concluso in successo non è sostituibile, perché il vincolo $|\mathcal{A}(t)| \leq 1$ si applica ai soli segnali attivi e un segnale terminato non è attivo. `[DOC-INTERNO CAP_02_parte_II.md:113]`
  - *Valore operativo*: dopo aver raggiunto target_1, nessuna "revoca" successiva può annullare quel successo; un eventuale nuovo segnale è un contratto indipendente.

### 4.2 Transizioni ammesse e precedenza degli eventi

- **R-4.17** — La creazione del segnale (emissione, generazione del `signal_id`, scrittura del log di emissione) porta il segnale nello stato `active`. `[DOC-INTERNO CAP_02_parte_II.md:121]`
  - *Valore operativo*: definisce il punto d'ingresso del lifecycle, l'istante a partire dal quale l'operatore ha in mano un segnale su cui può agire.

- **R-4.18** — È ammessa la transizione `active → target_1_hit` con la condizione di R-4.6 (raw touch, poi target_1 prima di stop/expiry/invalidazione). `[DOC-INTERNO CAP_02_parte_II.md:122]`
  - *Valore operativo*: è la transizione che comunica l'esito di successo del segnale eseguito.

- **R-4.19** — È ammessa la transizione `active → stopped` con la condizione di R-4.8 (raw touch, poi stop_loss prima di target_1/expiry/invalidazione). `[DOC-INTERNO CAP_02_parte_II.md:123]`
  - *Valore operativo*: comunica l'esito di stop dopo ingresso.

- **R-4.20** — È ammessa la transizione `active → invalidated` con la condizione di R-4.9/R-4.10 (invalidazione strutturale prima del raw touch). `[DOC-INTERNO CAP_02_parte_II.md:124]`
  - *Valore operativo*: comunica che il segnale è decaduto prima dell'ingresso.

- **R-4.21** — È ammessa la transizione `active → missed_target` con la condizione di R-4.11 (target_1 raggiunto prima del raw touch). `[DOC-INTERNO CAP_02_parte_II.md:125]`
  - *Valore operativo*: comunica l'occasione persa (target colpito senza ingresso).

- **R-4.22** — È ammessa la transizione `active → expired`, con le due cause registrate nel campo causale: (a) `posttrigger_timeout` quando $t \geq t_{exec} + \Delta t_{cromosoma}$ minuti di trading e il segnale è ancora `active`; (b) `pretrigger_timeout` quando $t \geq t_{emission} + T_{touch}^{max}$ minuti di trading e il segnale è ancora `active` senza raw touch. `[DOC-INTERNO CAP_02_parte_II.md:126]`
  - *Valore operativo*: comunica la chiusura per scadenza, distinguendo nel registro se è scaduto in attesa di ingresso o dopo l'ingresso.

- **R-4.23** — È ammessa la transizione `active → revoked` quando il motore emette un nuovo `signal_id` (sostituzione). `[DOC-INTERNO CAP_02_parte_II.md:127]` *(meccanismo della supersessione come premessa: `[DOC-INTERNO CAP_02_parte_II.md:77]`)*
  - *Valore operativo*: comunica che il segnale è stato sostituito da uno nuovo, da seguire al posto del precedente.

- **CN-4.4** — Nessuna transizione esce dagli stati terminali; in particolare `target_1_hit` non transita verso `target_2_hit` (rimosso), `revoked`, `stopped`, `expired` o qualsiasi altro stato. `[DOC-INTERNO CAP_02_parte_II.md:129]`
  - *Valore operativo*: ribadisce in forma di transizioni la definitività di ogni esito, così che l'operatore non si attenda mai un cambio di stato dopo la chiusura.

- **CN-4.5** — A parità di timestamp, la precedenza degli eventi è: `expiry > invalidazione > missed_target > raw touch > azione post-trigger`. `[DOC-INTERNO CAP_02_parte_II.md:131]`
  - *Valore di sistema/validazione*: garantisce un replay deterministico e riproducibile a parità di dati (premessa per l'audit monetario e per la validazione DSR/PBO della fitness); ordina eventi simultanei nella ricostruzione del lifecycle.

### 4.3 Raw touch come evento ed esecuzione

- **R-4.24** — Il raw touch della entry zone è l'**evento** in cui il prezzo del FIB, osservato sulla barra 1-min chiusa, assume per la prima volta un valore appartenente all'insieme discreto della `entry_zone`. `[DOC-INTERNO CAP_02_parte_II.md:135]`
  - *Valore operativo*: definisce con precisione l'istante in cui l'operatore deve considerare il segnale "entrato" e può eseguire manualmente l'ordine.

- **R-4.25** — La definizione di raw touch **non impone alcun vincolo sulla direzione di provenienza** del prezzo: la prima barra 1-min il cui intervallo high-low contiene almeno uno dei livelli discreti della zona produce il raw touch. `[DOC-INTERNO CAP_02_parte_II.md:135]`
  - *Valore operativo*: rassicura che il contatto con la zona conta a prescindere da come il prezzo l'ha raggiunta, evitando interpretazioni soggettive.

- **R-4.26** — Al raw touch il motore produce un evento, denotato `trigger_event`, riferito al `signal_id` del segnale corrente. `[DOC-INTERNO CAP_02_parte_II.md:137]`
  - *Valore operativo*: è l'evento che segnala l'attivazione concreta del segnale precedentemente emesso. *(La **pubblicazione** del `trigger_event` sul canale Telegram è Sez.6 / R-6.12, R-6.21; qui è solo evento del lifecycle.)*

- **R-4.27** — **Il raw touch è sempre eseguibile**: non esistono nel contratto del segnale guardie o filtri post-emissione che blocchino il trigger una volta che il prezzo è entrato nella zona. `[DOC-INTERNO CAP_02_parte_II.md:137]`
  - *Valore operativo*: garantisce che, una volta toccata la zona, non ci sono blocchi nascosti che invalidino l'ingresso: la decisione di emettere è già stata presa prima e il trigger è netto. *(Cfr. Sez.5 / CN-5.1, CN-5.4 — assenza di filtri post-emissione.)*

- **CN-4.6** — Il `trigger_event` **non è uno stato** della state machine: al raw touch il segnale **resta in `active`** finché un evento successivo (target_1, stop_loss, invalidazione, scadenza, revoca) non lo porta in uno stato terminale. `[DOC-INTERNO CAP_02_parte_II.md:139]`
  - *Valore operativo*: chiarisce che "essere entrato" (raw touch) non è un esito ma una fase intermedia; il segnale è ancora vivo e può ancora andare a target o a stop.

- **R-4.28** — Il motore **non osserva il fill manuale** dell'operatore sul broker, perché il motore non esegue ordini e l'operatore agisce manualmente dal cellulare. `[DOC-INTERNO CAP_02_parte_II.md:139]`
  - *Valore operativo*: il sistema non sa se e quando l'operatore ha effettivamente eseguito; il lifecycle del segnale è calcolato sul prezzo di mercato, non sul suo riempimento reale.

- **R-4.29** — *(edge case a — prezzo già in zona all'emissione)* Il motore valuta il raw touch a partire dalla barra $t_{emission} + 1$ (prima barra chiusa dopo l'emissione); la barra di emissione stessa non è valutata. Se il prezzo è già in zona alla chiusura di $t_{emission}$ e vi rimane, il raw touch è registrato alla prima barra $t_{emission}+1$ il cui high-low contiene un livello della zona (con $t_{exec} = t_{emission}+1$); se il prezzo era in zona a $t_{emission}$ ma ne è uscito a $t_{emission}+1$, non vi è raw touch immediato e il segnale resta `active`. `[DOC-INTERNO CAP_02_parte_II.md:145]`
  - *Valore operativo*: garantisce che il trigger non scatti su una barra che non poteva ancora vedere sul cellulare, evitando ingressi non azionabili.

- **R-4.30** — *(edge case b — gap overnight dentro/oltre la zona)* Un gap di apertura overnight con prezzo dentro o oltre la zona **non azzera** il raw touch: se la barra di apertura del giorno successivo (prima barra delle 8:00 CET) ha un intervallo high-low che contiene almeno un livello di `entry_zone`, il raw touch è registrato su quella barra ($t_{exec}$ = prima barra del giorno successivo). `[DOC-INTERNO CAP_02_parte_II.md:147]`
  - *Valore operativo*: assicura che un segnale lasciato aperto da un giorno all'altro si attiva regolarmente se il mercato riapre dentro la zona, senza "saltare" il trigger per il solo fatto del gap.

- **R-4.31** — *(edge case c — gap che salta la zona nella direzione opposta)* Se l'open della barra è sul lato della zona verso cui il segnale non punta: (i) se il prezzo si è allontanato verso il lato che coincide con la direzione di `stop_loss`, il motore valuta se la condizione di `invalidated` (stop attraversato) sia soddisfatta, altrimenti il segnale resta `active` in attesa di rientro nella zona; (ii) un gap che porta il prezzo oltre `target_1` senza raw touch determina la transizione in `missed_target`. `[DOC-INTERNO CAP_02_parte_II.md:149]`
  - *Valore operativo*: dice come si comporta il segnale quando il mercato "salta" la zona — verso lo stop diventa potenzialmente invalidato, verso il target diventa occasione persa — senza richiedere un intervento interpretativo dell'operatore.

### 4.4 Semantica dei timer (pre/post-trigger)

> *Confine: i **domini** discreti $\Delta t_{cromosoma}$ e $T_{touch}^{max}$ **come campi del payload** sono in Sez.3 (R-3.30/R-3.31) e qui sono citati come premessa, non ri-derivati. Questa sezione consolida solo la **meccanica di decorrenza e scadenza** dei due timer. Il calendario di trading (finestra 8:00–22:00 CET, cap di 2 giorni) è il calendario su cui i counter avanzano, già fissato nei CAP chiusi; i **valori-soglia congelati** restano fuori (vedi §12).*

- **R-4.32** — Il timer post-trigger decorre **dal raw touch**: al raw touch a istante $t_{exec}$, il motore calcola `expiry = t_exec + Δt_cromosoma` minuti di **trading**. `[DOC-INTERNO CAP_02_parte_II.md:155]`
  - *Valore operativo*: dice da quando parte il conto alla rovescia di validità del segnale eseguito — dall'ingresso, non dall'emissione.

- **R-4.33** — La somma del timer post-trigger è valutata sul **calendario di trading** dello strumento, non sul calendario solare. `[DOC-INTERNO CAP_02_parte_II.md:157]`
  - *Valore operativo*: la "scadenza" del segnale è misurata in tempo di mercato effettivo, non in ore di orologio comprese le notti chiuse.

- **R-4.34** — Il counter del timer post-trigger avanza **esclusivamente** nei minuti compresi nella finestra **8:00–22:00 CET** dei giorni di trading e **si arresta** nelle interruzioni notturne (22:00–8:00), nei weekend e nei festivi di mercato. `[DOC-INTERNO CAP_02_parte_II.md:157]`
  - *Valore operativo*: un segnale non "consuma" validità mentre il mercato è chiuso, quindi un segnale aperto venerdì sera è ancora valido lunedì in apertura per i minuti residui.

- **R-4.35** — Il timer post-trigger è valutato dal motore a ogni barra 1-min: appena $t \geq \texttt{expiry}$ e il segnale è ancora `active`, il segnale transita in `expired` con causa `posttrigger_timeout`. `[DOC-INTERNO CAP_02_parte_II.md:159]`
  - *Valore operativo*: un segnale entrato ma non andato né a target né a stop entro il tempo previsto viene chiuso automaticamente per scadenza, senza restare appeso.

- **R-4.36** — Il timer pre-trigger decorre **dalla `timestamp_emission`**: il segnale emesso resta `active` in attesa del raw touch e il counter parte dall'emissione. `[DOC-INTERNO CAP_02_parte_II.md:163]` `[DOC-INTERNO CAP_02_parte_II.md:165]`
  - *Valore operativo*: dice da quando parte il tempo massimo di attesa di un ingresso che non è ancora avvenuto.

- **R-4.37** — Il counter del timer pre-trigger avanza **esclusivamente** nei minuti di trading 8:00–22:00 CET, scavalcando le interruzioni notturne e i weekend, esattamente come il counter post-trigger. `[DOC-INTERNO CAP_02_parte_II.md:163]`
  - *Valore operativo*: l'attesa di un ingresso si misura in tempo di mercato effettivo, coerentemente con il timer post-trigger.

- **R-4.38** — Allo scadere del timer pre-trigger senza che sia avvenuto alcun raw touch, il segnale transita in `expired` con causa `pretrigger_timeout`. `[DOC-INTERNO CAP_02_parte_II.md:165]`
  - *Valore operativo*: evita che l'operatore resti in attesa indefinita di un raw touch che non arriva: il segnale non eseguito viene chiuso dopo il tempo massimo di attesa.

- **R-4.39** — Il razionale del timer pre-trigger è eliminare la patologia "segnale `active` per un tempo indefinitamente lungo in attesa del raw touch", che produrrebbe strategie degeneri (emissione rara e attesa illimitata) gonfiando artificialmente l'`executable_rate`. `[DOC-INTERNO CAP_02_parte_II.md:167]`
  - *Valore di sistema/validazione*: protegge la metrica `executable_rate` da degenerazioni del GA; per l'operatore il beneficio indiretto è ricevere segnali eseguibili in tempi ragionevoli.

### 4.5 Contratto di osservazione del primo pivot real-time

> *Confine: l'**algoritmo** di pivot detection e la regola di confermabilità del pivot sono materia di Parte III (Cap.15) e non sono consolidati qui (vedi §12). Questa sezione prende solo il **contratto di osservazione e la cadenza**.*

- **NFR-4.1** — Il motore osserva la sequenza delle barre 1-min a partire dall'apertura della sessione alle **8:00 CET**; a ciascuna barra chiusa valuta se la barra costituisce un candidato pivot strutturale (minimo o massimo) sulla sequenza disponibile. `[DOC-INTERNO CAP_02_parte_II.md:171]` `[DOC-INTERNO CAP_02_parte_II.md:173]`
  - *Valore operativo*: il punto di riferimento strutturale del segnale (l'ancora del prezzo di riferimento e del target di sessione) è calcolato osservando il mercato fin dall'apertura, non a posteriori.

- **NFR-4.2** — Vale come vincolo di contratto che il **primo pivot strutturale post-apertura** deve essere **disponibile**, in fase di calibrazione del motore, entro un numero massimo $N_{pivot}$ di barre 1-min dall'apertura della sessione (valore numerico di $N_{pivot}$ **non** fissato in Parte II → Parte V). `[DOC-INTERNO CAP_02_parte_II.md:173]`
  - *Valore operativo*: l'ancora strutturale è disponibile in tempo utile nella finestra iniziale di sessione, senza la quale i segnali della prima parte della giornata sarebbero privi di riferimento.

- **NFR-4.3** — La cadenza di valutazione della regola di pivot è la barra 1-min **chiusa**; il motore **non** opera su tick intra-bar per la pivot detection. `[DOC-INTERNO CAP_02_parte_II.md:175]`
  - *Valore operativo*: coerenza fra ciò che il motore osserva (barre chiuse) e i livelli che pubblica, senza scatti dovuti a oscillazioni intra-minuto.

### 4.6 Position lifecycle: submacchina distinta

- **CN-4.7** — Il lifecycle del segnale (il contratto del motore, ottimizzato dal GA) si **chiude definitivamente** in `target_1_hit` o in qualsiasi altro stato terminale; il position lifecycle è una **submacchina distinta** di tracking degli eventi post-target_1. `[DOC-INTERNO CAP_02_parte_II.md:349]` `[DOC-INTERNO CAP_02_parte_II.md:351]` `[DOC-INTERNO CAP_02_parte_II.md:352]` `[DOC-INTERNO CAP_02_parte_II.md:7]`
  - *Valore operativo*: chiarisce il confine netto fra "cosa fa il sistema" (porta a target_1) e "cosa fa lui" (gestisce la posizione oltre), senza sovrapposizioni di responsabilità.

- **R-4.40** — Nel contesto del motore (che emette segnali senza eseguire ordini), il "boundary" del lifecycle del segnale coincide con `target_1_hit`: oltre tale soglia la gestione della posizione è responsabilità dell'operatore umano, con il solo supporto informativo della submacchina di tracking. `[DOC-INTERNO CAP_02_parte_II.md:362]`
  - *Valore operativo*: dopo target_1 l'operatore ha il pieno controllo della posizione e riceve dal sistema solo informazione, non istruzioni operative.

- **R-4.41** — Sono **OUT-OF-SCOPE dal motore**: execution policy, scaling-out automatico, trailing stop, dynamic sizing, take profit anticipato e qualsiasi decisione operativa post-target_1; la gestione della posizione oltre target_1 è interamente dell'operatore manuale (punto 8 della dichiarazione di intenti). `[DOC-INTERNO CAP_02_parte_II.md:368]`
  - *Valore operativo*: il sistema non interferisce con la gestione della posizione oltre target_1 (niente take/stop profit calcolati dal segnale), come da esplicita richiesta dell'operatore.

- **R-4.42** — Sono **IN-SCOPE per reporting e validazione** le metriche prodotte dalla submacchina: hit-rate condizionale di target_2 dato target_1 ($\pi_{t_2 \mid t_1}$), distribuzioni di MFE e MAE post-target_1, frequenza di stop post-target_1 ($f_{stop \mid t_1}$), distribuzione dei tempi di permanenza post-target_1. `[DOC-INTERNO CAP_02_parte_II.md:370]` `[DOC-INTERNO CAP_02_parte_II.md:372]` `[DOC-INTERNO CAP_02_parte_II.md:373]` `[DOC-INTERNO CAP_02_parte_II.md:374]` `[DOC-INTERNO CAP_02_parte_II.md:375]`
  - *Valore operativo*: queste metriche misurano quanto sono "buoni" i livelli target_2 e stop_loss pubblicati, informando l'operatore (via reporting) sulla qualità strutturale dei livelli che riceve.

- **R-4.43** — L'**evento di ingresso** della submacchina è il raggiungimento di `target_1_hit` da parte del segnale associato; a quel momento la submacchina registra il prezzo di `target_1`, di `stop_loss`, di `target_2` (dal payload immutabile) e l'istante di ingresso. `[DOC-INTERNO CAP_02_parte_II.md:381]`
  - *Valore operativo*: definisce con precisione quando inizia il tracking della posizione, allineato all'istante in cui l'operatore prende in carico la gestione manuale.

- **R-4.44** — Lo **stato iniziale** della submacchina è `tracking_active`, che indica che la submacchina sta osservando la dinamica del prezzo successiva a `target_1_hit`. `[DOC-INTERNO CAP_02_parte_II.md:383]`
  - *Valore operativo*: distingue lo stato di tracking attivo della posizione dallo stato (terminato) del segnale, così che il reporting sia leggibile.

- **R-4.45** — La submacchina registra gli **eventi** `target_2_reached`, `stop_after_target_1`, `retracement_to_entry`, `position_close_event` come **eventi della submacchina, non stati del segnale**. `[DOC-INTERNO CAP_02_parte_II.md:385]` `[DOC-INTERNO CAP_02_parte_II.md:386]` `[DOC-INTERNO CAP_02_parte_II.md:387]` `[DOC-INTERNO CAP_02_parte_II.md:388]` `[DOC-INTERNO CAP_02_parte_II.md:389]`
  - *Valore operativo*: fornisce all'operatore (via reporting) una traccia di cosa è successo dopo target_1 — se la posizione ha raggiunto target_2, è tornata allo stop o alla zona — senza che questi eventi modifichino l'esito già registrato del segnale.

- **CN-4.8** — `target_2_reached` è un **evento** della submacchina e **non** uno stato/transizione del segnale (coerente con la rimozione di `target_2_hit`, R-4.2). `[DOC-INTERNO CAP_02_parte_II.md:386]` `[DOC-INTERNO CAP_02_parte_II.md:374]`
  - *Valore operativo*: ribadisce che il raggiungimento di target_2 è informazione sulla gestione della posizione (dell'operatore), non un esito del contratto del segnale.

- **R-4.46** — Lo **stato terminale** della submacchina è `tracking_closed`; la submacchina termina al verificarsi del primo evento terminante dichiarato in Parte V (in backtest: `target_2_reached`, `stop_after_target_1` o fine sessione, quello che avviene prima). `[DOC-INTERNO CAP_02_parte_II.md:391]`
  - *Valore operativo*: definisce quando il tracking della posizione si conclude nel reporting, chiudendo il ciclo informativo post-target_1.

- **CN-4.9** — La submacchina **non modifica mai lo stato del segnale**: il segnale è terminato in `target_1_hit` prima che la submacchina inizi a tracciare. `[DOC-INTERNO CAP_02_parte_II.md:393]`
  - *Valore operativo*: l'esito registrato del segnale (`target_1_hit`) resta inalterato qualunque cosa accada alla posizione dopo, preservando l'integrità del track record.

- **CN-4.12** — I **log della submacchina sono separati** dai log del lifecycle del segnale e referenziati dal `signal_id` del segnale che ha innescato il tracking. `[DOC-INTERNO CAP_02_parte_II.md:393]`
  - *Valore operativo*: la traccia di ciò che accade alla posizione dopo `target_1_hit` è registrata distintamente dall'esito del segnale, così che reporting e track record restino leggibili e non si mescolino.

- **CN-4.10** — Lo **space search del cromosoma del GA non viene esteso** da policy decisionali post-target_1: il GA non ottimizza trailing stop, take profit anticipato, scaling-out né alcuna regola di gestione della posizione oltre `target_1_hit`. `[DOC-INTERNO CAP_02_parte_II.md:397]`
  - *Valore operativo*: il sistema resta nel perimetro concordato (emette segnali, non gestisce posizioni), e la complessità del modello non cresce con regole che non servono.

- **R-4.47** — Le metriche della submacchina ($\pi_{t_2 \mid t_1}$, MFE/MAE post-target_1, $f_{stop \mid t_1}$) entrano nella fitness multi-obiettivo del GA come **obiettivi di qualità informativa del payload**, **non** come variabili decisionali del cromosoma. `[DOC-INTERNO CAP_02_parte_II.md:399]`
  - *Valore operativo*: il GA è spinto a pubblicare livelli target_2 e stop_loss strutturalmente robusti (realizzati dal mercato con alta probabilità), migliorando la qualità informativa dei segnali.

- **R-4.48** — La metrica **primaria** di successo del motore è il **profitto netto al netto delle commissioni** (in punti FIB) realizzato dai segnali eseguiti; le metriche della submacchina ($\pi_{t_2 \mid t_1}$, MFE, MAE, $f_{stop \mid t_1}$) sono **strumenti di verifica e calibrazione subordinati**, non la definizione di successo. `[DOC-INTERNO CAP_02_parte_II.md:411]`
  - *Valore operativo*: dichiara senza ambiguità che cosa il prodotto considera "successo" (il profitto netto realizzato dall'operatore, già al netto dei 5 EUR/op), così che le metriche strutturali della submacchina siano lette come supporto di calibrazione e non come obiettivo a sé. **Criterio dichiarato, non esito d'edge**: nessun valore di profitto è asserito qui; l'esito d'edge resta PENDING-empirico, esclusiva del ruolo `validator` in FASE-D.

### 4.7 Invarianti di modellazione del lifecycle (riepilogo)

- **CN-4.11** — Il vincolo $|\mathcal{A}(t)| \leq 1$ si riferisce ai **soli segnali attivi**: un segnale terminato non è attivo, quindi non è soggetto a sostituzione. `[DOC-INTERNO CAP_02_parte_II.md:113]`
  - *Valore di sistema/validazione*: disambigua la sostituzione `active→revoked` rispetto agli stati terminali (premessa per la coerenza del lifecycle e del replay). *Nota di confine*: il vincolo $|\mathcal{A}(t)| \leq 1$ **come tale** (proprietà del payload-oggetto) è consolidato in Sez.3 / CN-3.4; qui è richiamato solo per la sua conseguenza sul lifecycle (inapplicabilità della revoca a un segnale terminato), non ri-derivato.

**Out-of-scope della Sezione 4**:
| Voce | Destinazione |
|---|---|
| Schema-payload come dato (campi, domini, banda $b$, timer come campi, immutabilità, segnale unico attivo) | **Sez.3** (da B2) — citati come premessa |
| Condizioni / regola di emissione, filtro 80pt come regola | **Sez.5** (da B4) |
| Pubblicazione Telegram del `trigger_event` e dell'emissione, latenza, anti-duplicato | **Sez.6** (da B4) |
| Formato dei tre log, determinismo bit-exact del replay | **Sez.7 / Sez.9** |
| Sessione operativa come requisito runtime + verifica empirica (M-GOV-1) | **Sez.7** (da B5) |
| Algoritmo di pivot detection; definizione condizioni di invalidazione; regola di fill virtuale | Parti III-IV (§12) |
| Valori numerici congelati ($N_{pivot}$, valori dei timer/soglie) | Parte V (§12) |

---

## Sezione 5 — Condizioni e regola di emissione (da B4)

**Valore di prodotto della sezione**: definisce *come e quando* il motore EMETTE un segnale — la filosofia del contratto di emissione, le tre condizioni di mercato valutate prima dell'emissione, il filtro 80 pt come regola, la regola di emissione (AND logico) e le conseguenze della non-emissione, l'assenza di filtri post-emissione e di fasi speciali per orario.

> **Carve-out numeri**: la finestra 8:00–22:00 CET è citata come calendario già fissato nei CAP chiusi; il valore-soglia 80 pt e i valori di lavoro provvisori ($\tau_{vol}/\tau_{liq}/\tau_{dist}^\sigma$) sono materia Parte V (§12): qui si enuncia la **regola**, non il valore.

### 5.1 Filosofia del contratto di emissione

- **R-5.1** — Il motore decide se emettere un segnale **prima** dell'emissione, sulla base di condizioni di mercato osservate al momento della valutazione. `[DOC-INTERNO CAP_02_parte_II.md:183]`
  - *Valore operativo*: l'operatore riceve solo segnali per cui il motore ha già verificato, sui dati di mercato, che le condizioni di emissione erano soddisfatte; non riceve segnali "condizionati" da rivalutare dopo.

- **CN-5.1** *(invariante di contratto)* — Una volta emesso il segnale, il raw touch dell'entry zone è sempre eseguibile e produce il `trigger_event`; il contratto **non** prevede guardie o filtri post-emissione che blocchino il trigger. `[DOC-INTERNO CAP_02_parte_II.md:183]` (Il `trigger_event` come evento del lifecycle è premessa di Sez.4, qui non ri-derivata.)
  - *Valore operativo*: l'operatore sa che, una volta ricevuto un segnale, nessun meccanismo nascosto del motore può invalidarne l'eseguibilità al raw touch; la decisione di entrare resta sua e basata su ciò che vede sul broker.

- **R-5.2** — L'assenza di filtri post-emissione è coerente con il punto 1 della dichiarazione di intenti (il motore emette segnali, l'esecuzione è dell'operatore): un filtro post-emissione che bloccasse il trigger introdurrebbe una decisione di esecuzione mascherata da decisione di segnale. `[DOC-INTERNO CAP_02_parte_II.md:185]`
  - *Valore operativo*: garantisce che il motore non si appropri della decisione di esecuzione, che resta interamente dell'operatore.

- **R-5.3** — Le condizioni di emissione devono essere calcolabili sulla serie storica del FIB disponibile per il training; lo storico Portara/CQG FIB 1-min copre OHLC e volume, omogenei con le grandezze del feed real-time. `[DOC-INTERNO CAP_02_parte_II.md:185]` `[DOC-INTERNO CAP_02_parte_II.md:187]`
  - *Valore operativo*: il segnale è prodotto da una regola realmente ottimizzata e validata su dati storici, non da una regola che usa dati non disponibili in addestramento.

- **R-5.4** — Lo spread bid-ask e la profondità del book non sono disponibili nello storico pianificato (richiederebbero acquisti di dati esplicitamente esclusi in CAP-01); pertanto la condizione di spread è **eliminata** dal contratto di emissione. `[DOC-INTERNO CAP_02_parte_II.md:185]`
  - *Valore operativo*: nessuna condizione di emissione dipende da dati che il motore non possiede in addestramento, così la regola è coerente fra training e produzione; lo spread istantaneo lo valuta l'operatore in tempo reale.

- **R-5.5** — Una volta ricevuto il payload, l'operatore valuta in tempo reale sul broker le condizioni di esecuzione visibili a lui (spread istantaneo, profondità del book, candela in corso) e decide se entrare manualmente. `[DOC-INTERNO CAP_02_parte_II.md:185]`
  - *Valore operativo*: il sistema delega all'operatore la sola valutazione che richiede dati real-time non modellabili, sfruttando il fatto che esegue manualmente.

### 5.2 Le tre condizioni di emissione

- **R-5.6** — Il range della barra 1-min al momento della valutazione (massimo meno minimo della barra appena chiusa) deve essere $\leq \tau_{vol}\big(\hat\sigma_{\text{pt}}(t_{emission})\big)$, soglia derivata dal modello di volatilità condizionata. `[DOC-INTERNO CAP_02_parte_II.md:191]` `[DOC-INTERNO CAP_02_parte_II.md:193]`
  - *Valore operativo*: impedisce che l'operatore riceva un segnale costruito in una barra di volatilità anomala, in cui il prezzo strutturale di riferimento è instabile e il payload rischia di essere subito superseduto. *(Forma di $\tau_{vol}$, EGARCH, conversione $\hat\sigma_{pt}$ → Parte III, §12; valore soglia → Parte V.)*

- **R-5.7** — Il volume della barra 1-min al momento della valutazione deve essere $\geq \tau_{liq}$. `[DOC-INTERNO CAP_02_parte_II.md:197]` `[DOC-INTERNO CAP_02_parte_II.md:199]`
  - *Valore operativo*: evita che l'operatore riceva un segnale costruito su un prezzo strutturale di riferimento non rappresentativo, risultato di poche operazioni in un mercato anomalmente sottile. *(Soglia $\tau_{liq}$ → Parte V.)*

- **R-5.8** — La distanza fra prezzo strutturale di riferimento e target_1, espressa in sigma-units, deve essere $|\texttt{target\_1}-p_{ref}|/\hat\sigma_{\text{pt}}(t_{emission}) \geq \tau_{dist}^{\sigma}$, con $\tau_{dist}^{\sigma}$ numero puro. `[DOC-INTERNO CAP_02_parte_II.md:203]` `[DOC-INTERNO CAP_02_parte_II.md:205]`
  - *Valore operativo*: garantisce che la distanza minima fino al primo target sia tarata coerentemente con il regime di volatilità in corso, così che il segnale abbia un'estensione attesa significativa rispetto al rumore del momento, e non solo in punti assoluti. *(Dominio $\tau_{dist}^{\sigma}$ → Parte V; conversione $\hat\sigma_{pt}$ → Parte III, §12.)*

### 5.3 Il filtro 80 pt come regola di emissione

- **R-5.9** — L'emissione richiede che il filtro 80 pt del `setup_class` sia soddisfatto: per setup directional $|\texttt{target\_1}-p_{ref}| \geq 80$ pt; per setup trade_range $A_{range} \geq 80$ pt. `[DOC-INTERNO CAP_02_parte_II.md:209]`
  - *Valore operativo*: assicura che ogni segnale che l'operatore riceve abbia un'estensione minima in punti assoluti tale da rendere l'operazione economicamente sensata (a fronte di commissioni e tick), indipendentemente dal regime. *(Valore 80 citato come dato già congelato in CAP-01; congelamento → Parte V. Definizione operativa di $A_{range}$ → Parte IV, §12.)*

- **CN-5.2** *(invariante)* — Il filtro 80 pt resta vincolo assoluto a valle, **non sostituito** dalla condizione in sigma-units; l'emissione richiede il soddisfacimento **simultaneo** di entrambi (sigma-units come leva ottimizzabile del GA, filtro 80pt come vincolo fisso); **in nessun caso** il cromosoma può allentare il floor di 80 pt. `[DOC-INTERNO CAP_02_parte_II.md:209]`
  - *Valore operativo*: garantisce che la soglia minima di estensione del trade non possa mai essere abbassata dall'ottimizzazione, qualunque parametro il GA scelga — una protezione fissa del contratto, non rivedibile.

- **CN-5.3** *(invariante)* — La separazione fra la condizione in sigma-units (parametro libero del cromosoma) e il filtro 80 pt (vincolo fisso del contratto) è architetturalmente equivalente a quella fra il floor fisso della banda $b_{min}=5$ e il parametro $b$ ottimizzato dal cromosoma nel dominio $\{5,\ldots,40\}$. `[DOC-INTERNO CAP_02_parte_II.md:211]`
  - *Valore di sistema*: chiarisce in modo non ambiguo, per chi audita il contratto, quali grandezze il GA può muovere e quali sono floor fissi, prevenendo letture errate che tratterebbero il filtro 80 pt come parametro ottimizzabile.

### 5.4 Regola di emissione e conseguenze della non-emissione

- **R-5.10** — L'emissione del segnale avviene **se e solo se** al tempo $t_{emission}$ valgono simultaneamente le tre condizioni e il filtro 80 pt: $E_{vol}\land E_{liq}\land E_{dist}^{\sigma}\land E_{80pt}=\text{vero}$. `[DOC-INTERNO CAP_02_parte_II.md:215]` `[DOC-INTERNO CAP_02_parte_II.md:217]`
  - *Valore operativo*: definisce in modo deterministico la sola condizione sotto cui l'operatore riceve un segnale, così che non esistano emissioni "borderline" a discrezione.

- **CN-5.4** *(invariante)* — Se almeno una delle quattro condizioni non è soddisfatta, il segnale candidato **non** viene emesso. `[DOC-INTERNO CAP_02_parte_II.md:219]`
  - *Valore operativo*: l'operatore non riceve mai un segnale che soddisfa solo parte delle condizioni di qualità; la barra è "tutto o niente".

- **R-5.11** — In caso di non-emissione, nessun `signal_id` viene generato. `[DOC-INTERNO CAP_02_parte_II.md:219]`
  - *Valore di sistema*: garantisce che non esistano identificatori "fantasma" associati a segnali mai esistiti, premessa di un registro dei segnali pulito e auditabile.

- **R-5.12** — In caso di non-emissione, nessuna pubblicazione Telegram avviene. `[DOC-INTERNO CAP_02_parte_II.md:219]`
  - *Valore operativo*: l'operatore non riceve notifiche per segnali non emessi, evitando rumore sul canale e falsi inviti all'azione.

- **R-5.13** — In caso di non-emissione, nessun log di emissione viene scritto. `[DOC-INTERNO CAP_02_parte_II.md:219]`
  - *Valore di sistema*: il log di emissione contiene solo segnali effettivamente emessi, premessa di un audit trail coerente con ciò che l'operatore ha ricevuto.

- **R-5.14** — Se non emette, il motore continua a valutare le condizioni alle barre 1-min successive. `[DOC-INTERNO CAP_02_parte_II.md:219]`
  - *Valore operativo*: una barra non favorevole non chiude l'opportunità; l'operatore può ricevere il segnale appena le condizioni si verificano in una barra successiva.

### 5.5 Assenza di filtri post-emissione e di fasi speciali

- **CN-5.5** *(invariante)* — Una volta emesso il segnale, il raw touch dell'entry zone è sempre eseguibile; non esistono nel contratto guardie o filtri ulteriori che blocchino il `trigger_event`. `[DOC-INTERNO CAP_02_parte_II.md:225]`
  - *Valore operativo*: l'operatore ha la certezza contrattuale che il segnale ricevuto sarà eseguibile al raw touch senza condizioni nascoste sopravvenute lato motore.

- **R-5.15** — Eventuali condizioni patologiche di mercato al momento del raw touch (spread istantaneo allargato, candela in corso violenta) sono valutate in autonomia dall'operatore prima dell'invio dell'ordine; non sono filtrate dal motore. `[DOC-INTERNO CAP_02_parte_II.md:225]`
  - *Valore operativo*: l'operatore sa esattamente cosa resta a suo carico (la lettura del mercato istantaneo al momento dell'ingresso), senza aspettarsi un filtro automatico che non esiste.

- **R-5.16** — Le condizioni di emissione si applicano uniformemente lungo l'intera finestra 8:00–22:00 CET; non si introducono fasi speciali (apertura, regolare, after-hours, asta) né soglie differenziate per fascia oraria. `[DOC-INTERNO CAP_02_parte_II.md:227]`
  - *Valore operativo*: l'operatore riceve segnali con gli stessi criteri di qualità a qualunque ora della finestra; non deve interpretare diversamente un segnale del mattino da uno serale. *(La finestra 8:00–22:00 CET è citata come calendario già fissato nei CAP chiusi. Il **requisito di sessione operativa** in sé, con la sua verifica empirica, è Sez.7 / R-7.11.)*

**Out-of-scope della Sezione 5**:
| Voce | Destinazione |
|---|---|
| Formule del modello di volatilità EGARCH, $\hat\sigma_{pt}$, forma di $\tau_{vol}$, definizione di $A_{range}$ | Parti III/IV (§12) |
| Valori congelati delle soglie $\tau_{vol}/\tau_{liq}/\tau_{dist}^{\sigma}$, valore 80 del filtro | Parte V (§12) |
| Contratto del messaggio Telegram, ordine campi, latenza, anti-duplicato, notifiche | **Sez.6** (da B4) |
| Sessione operativa come requisito runtime (verifica empirica della finestra) | **Sez.7** (da B5) |

---

## Sezione 6 — Consegna Telegram del segnale (da B4)

**Valore di prodotto della sezione**: definisce *come* il segnale (e la notifica del suo trigger) viene CONSEGNATO all'operatore via Telegram — contesto del canale, contratto informativo del messaggio e ordine dei campi, latenza di consegna, anti-duplicato, messaggio separato + notifica del trigger, errori di pubblicazione, layout mobile-first e le 3 notifiche standard per segnale.

> **Carve-out numeri**: i valori di lavoro provvisori $L_{max}=30$ s, $n_{retry}=3$, $\Delta t_{retry}=2$ s sono citati dal CAP **come provvisori**; i valori definitivi sono Parte V (§12). La latenza effettiva del canale è **PENDING-empirico** (B-1, §13).

### 6.1 Contesto del canale Telegram

- **NFR-6.1** — Il canale è un bot Telegram personale dell'operatore (già attivo, CAP-01); l'operatore opera da cellulare in modo discontinuo durante l'orario di lavoro e legge il segnale prima di inviare manualmente l'ordine; il formato del messaggio deve essere progettato per la **lettura mobile in condizioni di attenzione limitata**. `[DOC-INTERNO CAP_02_parte_II.md:235]`
  - *Valore operativo*: permette all'operatore di cogliere il segnale a colpo d'occhio dal cellulare, in pause brevi e con attenzione parziale, riducendo il rischio di errori di lettura prima dell'invio manuale.

- **NFR-6.2** — Il canale deve garantire una latenza di consegna compatibile con l'urgenza operativa del segnale. `[DOC-INTERNO CAP_02_parte_II.md:235]`
  - *Valore operativo*: assicura che il segnale arrivi sul cellulare in tempo utile perché l'operatore possa ancora agire sul prezzo strutturale di riferimento. *(Il vincolo quantitativo è NFR-6.3.)*

### 6.2 Contratto informativo del messaggio

- **CN-6.1** *(invariante)* — I campi pubblicati seguono un **ordine obbligatorio** (1→9 sotto). `[DOC-INTERNO CAP_02_parte_II.md:241]`
  - *Valore operativo*: un ordine fisso permette di trovare ogni informazione sempre nella stessa posizione, accelerando la lettura mobile e riducendo gli errori.

- **R-6.1** — È pubblicato `signal_id`, l'identificatore del segnale, in chiaro come chiave operativa (pos. 1). `[DOC-INTERNO CAP_02_parte_II.md:243]`
  - *Valore operativo*: dà una chiave univoca per riferirsi al segnale (e correlarlo alla successiva notifica di trigger).

- **R-6.2** — È pubblicata `direction` (long o short), evidenziata in modo immediato (pos. 2). `[DOC-INTERNO CAP_02_parte_II.md:244]`
  - *Valore operativo*: comunica subito il verso dell'operazione, l'informazione più critica per non sbagliare lato.

- **R-6.3** — È pubblicato `setup_class` (directional o trade_range), per distinguere il senso del filtro 80 pt applicato (pos. 3). `[DOC-INTERNO CAP_02_parte_II.md:245]`
  - *Valore operativo*: l'operatore capisce di che tipo di setup si tratta e come è stata misurata l'estensione minima del trade.

- **R-6.4** — È pubblicata `entry_zone`, banda di prezzo discreta, esplicitata come intervallo $[p_{ref}-b,\,p_{ref}+b]$ in punti FIB (pos. 4). `[DOC-INTERNO CAP_02_parte_II.md:246]`
  - *Valore operativo*: dà la fascia di prezzo esatta entro cui il raw touch è valido, pronta da confrontare col book sul broker.

- **R-6.5** — Sono pubblicati `target_1` e `target_2`, i due target strutturali, distinti e ordinati (pos. 5). `[DOC-INTERNO CAP_02_parte_II.md:247]`
  - *Valore operativo*: l'operatore vede entrambi i livelli obiettivo, distinti e in ordine, per pianificare la gestione manuale della posizione.

- **R-6.6** — È pubblicato `stop_loss`, il prezzo strutturale di stop (pos. 6). `[DOC-INTERNO CAP_02_parte_II.md:248]`
  - *Valore operativo*: comunica il livello di uscita in perdita, essenziale per dimensionare il rischio prima di entrare.

- **R-6.7** — È pubblicato `timestamp_emission`, l'istante di emissione, riportato come data e ora CET (pos. 7). `[DOC-INTERNO CAP_02_parte_II.md:249]`
  - *Valore operativo*: permette di valutare quanto è "fresco" il segnale prima di agire (coerente con il vincolo di latenza).

- **R-6.8** — È pubblicato `target_2_type`, qualificatore della natura del livello target_2, dominio $\{\text{structural},\text{synthetic}\}$ (pos. 8). `[DOC-INTERNO CAP_02_parte_II.md:250]`
  - *Valore operativo*: permette al consumer mobile di distinguere un target_2 derivato da una struttura confermata da uno sintetico calcolato dal modello. *(Algoritmo che popola il valore → Parte IV, §12.)*

- **R-6.9** — È pubblicato `stop_type`, qualificatore della natura del livello stop_loss, dominio $\{\text{structural},\text{synthetic}\}$ (pos. 9). `[DOC-INTERNO CAP_02_parte_II.md:251]`
  - *Valore operativo*: permette al consumer mobile di distinguere uno stop derivato da una struttura confermata da uno sintetico. *(Algoritmo che popola il valore → Parte IV, §12.)*

- **CN-6.2** *(invariante)* — La presenza di `target_2_type` e `stop_type` permette di valutare la natura strutturale dei livelli **senza alcun impatto** sulla decisione di ingresso, che resta vincolata al raw touch dell'`entry_zone`. `[DOC-INTERNO CAP_02_parte_II.md:253]`
  - *Valore operativo*: chiarisce che i due qualificatori sono solo contesto informativo e non modificano la regola di ingresso.

- **R-6.10** — I campi $\Delta t_{cromosoma}$ e $T_{touch}^{max}$ **non** figurano nel messaggio all'operatore: sono parametri tecnici rilevanti per il log interno ma non per la decisione operativa. `[DOC-INTERNO CAP_02_parte_II.md:253]`
  - *Valore operativo*: il messaggio resta sgombro di parametri che l'operatore non usa per decidere, sostenendo la leggibilità mobile.

- **CN-6.3** *(invariante)* — Il messaggio **non** contiene istruzioni di gestione attiva della posizione (incrementi, scaling out, take profit anticipato, stop profit), in coerenza con il punto 8 della dichiarazione di intenti che riserva queste decisioni all'operatore. `[DOC-INTERNO CAP_02_parte_II.md:253]`
  - *Valore operativo*: l'operatore mantiene piena titolarità della gestione della posizione; il messaggio non lo induce ad azioni di gestione che il contratto riserva a lui.

### 6.3 Latenza di consegna

- **NFR-6.3** `[B-1 PROVVISORIO]` — Definita la latenza di consegna $L$ come intervallo tra `timestamp_emission` e l'istante di ricezione del messaggio sul cellulare dell'operatore, vale il vincolo $L \leq L_{max}$. `[DOC-INTERNO CAP_02_parte_II.md:257]` `[DOC-INTERNO CAP_02_parte_II.md:259]`
  - *Valore operativo*: garantisce che, quando l'operatore legge e agisce, il prezzo strutturale di riferimento non si sia spostato in modo non trascurabile rispetto al momento dell'emissione, così che il segnale conservi valore informativo.

- **NFR-6.4** `[B-1 PROVVISORIO]` — Il valore di lavoro provvisorio di $L_{max}$ è 30 secondi (oltre questa soglia il segnale perde valore informativo); il valore congelato definitivo è materia di Parte V, e **la verifica empirica della latenza effettiva del canale Telegram è materia di Appendice E**. `[DOC-INTERNO CAP_02_parte_II.md:261]` Il valore 30 s è citato dal CAP **come provvisorio**; la latenza effettiva del canale è **PENDING-empirico** (non verificata).
  - *Valore di sistema*: fissa un riferimento di lavoro tracciabile per il vincolo $L\leq L_{max}$ tenendo esplicito che il numero non è definitivo e la sua verifica resta aperta (vedi §13, B-1).

### 6.4 Politica anti-duplicato e regola del messaggio separato

- **CN-6.4** *(invariante)* — Il motore pubblica ciascun `signal_id` **una sola volta**: dato l'insieme $\mathcal{P}$ dei `signal_id` già pubblicati con successo, il motore pubblica il messaggio se e solo se `signal_id`$\notin\mathcal{P}$, e contestualmente aggiunge `signal_id` a $\mathcal{P}$. `[DOC-INTERNO CAP_02_parte_II.md:265]`
  - *Valore operativo*: l'operatore non riceve due volte lo stesso segnale e non rischia di aprire per errore due posizioni sullo stesso segnale.

- **CN-6.5** *(invariante)* — L'insieme $\mathcal{P}$ è persistito su disco insieme al log di emissione, in modo che i restart del motore non comportino ripubblicazione di segnali già notificati. `[DOC-INTERNO CAP_02_parte_II.md:265]`
  - *Valore di sistema*: garantisce che l'anti-duplicato sopravviva ai restart del motore, premessa di un comportamento di pubblicazione riproducibile e auditabile. *(Lo schema del log di emissione è Sez.7/Sez.9; qui si prende solo che $\mathcal{P}$ è persistito a fini anti-ripubblicazione.)*

- **R-6.11** — Quando il motore emette un nuovo segnale in sostituzione di un precedente, il messaggio Telegram corrispondente è pubblicato come **messaggio separato**, con il proprio `signal_id` distinto. `[DOC-INTERNO CAP_02_parte_II.md:269]`
  - *Valore operativo*: l'operatore vede ogni nuovo segnale come messaggio a sé, con la sua chiave, senza confondersi con il precedente. *(Regola di sostituzione e evento del lifecycle → Sez.4 / R-4.15, R-4.23.)*

- **CN-6.6** *(invariante, coerente con l'immutabilità del payload)* — Non viene effettuata alcuna operazione di modifica o edit sul messaggio Telegram precedente; il messaggio del segnale revocato resta visibile come traccia storica ma non rappresenta più un segnale attivo. La scelta di emettere messaggi separati anziché editare è coerente con l'invariante di payload immutabile (Sez.3 / CN-3.2): editare equivarrebbe a modificare il payload pubblicato. `[DOC-INTERNO CAP_02_parte_II.md:269]`
  - *Valore operativo*: l'operatore ha la garanzia che un messaggio già ricevuto non cambi mai sotto i suoi occhi, così ciò che ha letto e su cui ha agito resta verità storica.

- **R-6.12** — Al verificarsi del `trigger_event` (raw touch dell'entry zone) il motore pubblica una **notifica separata** sul canale Telegram, che fa riferimento al `signal_id` del segnale corrente, all'istante $t_{exec}$ del raw touch e all'`expiry` calcolata. `[DOC-INTERNO CAP_02_parte_II.md:271]`
  - *Valore operativo*: avvisa l'operatore nel preciso momento in cui il prezzo è entrato in zona e il segnale è eseguibile, informazione tempestiva e azionabile. *(Il `trigger_event` come evento del lifecycle è Sez.4 / R-4.26; qui si consolida la sua **pubblicazione**.)*

- **CN-6.7** *(invariante)* — La notifica del `trigger_event` è funzionalmente distinta dal messaggio di emissione: l'emissione comunica l'esistenza del segnale e i suoi parametri; la notifica del trigger comunica che il prezzo è entrato nella zona e che il segnale è eseguibile. In Parte II si fissa il vincolo che essa sia pubblicata come **messaggio separato e non come edit**, contestualmente al riconoscimento del raw touch. `[DOC-INTERNO CAP_02_parte_II.md:271]`
  - *Valore operativo*: l'operatore distingue nettamente "esiste un segnale con questi parametri" da "ora puoi eseguire", senza ambiguità sul significato dei due messaggi. *(Dettaglio del contratto informativo della notifica del trigger → Appendice E, §12.)*

### 6.5 Gestione degli errori di pubblicazione

- **R-6.13** — In caso di errore nella chiamata all'API Telegram (timeout, errori di rete, indisponibilità temporanea), il motore applica una politica di retry. `[DOC-INTERNO CAP_02_parte_II.md:275]`
  - *Valore operativo*: un errore transitorio del canale non fa perdere il segnale all'operatore; il motore ritenta automaticamente.

- **R-6.14** — La politica prevede un numero massimo di tentativi $n_{retry}$, valore di lavoro provvisorio $n_{retry}=3$. `[DOC-INTERNO CAP_02_parte_II.md:277]` Il valore 3 è citato dal CAP **come provvisorio**; il valore definitivo è Parte V.
  - *Valore di sistema*: limita il numero di ritentativi a un tetto definito e tracciabile, premessa di un comportamento di pubblicazione deterministico e auditabile.

- **R-6.15** — Fra i tentativi si applica un backoff esponenziale, con base provvisoria $\Delta t_{retry}=2$ secondi raddoppiata a ogni tentativo. `[DOC-INTERNO CAP_02_parte_II.md:278]` Il valore 2 s è citato dal CAP **come provvisorio**; il valore definitivo è Parte V.
  - *Valore di sistema*: distanzia i ritentativi in modo crescente per non insistere su un canale temporaneamente indisponibile, premessa di una gestione robusta degli errori transitori.

- **R-6.16** — In caso di fallimento finale (tutti i tentativi esauriti), l'errore è registrato nel log di emissione e non avviene nessuna ulteriore pubblicazione. `[DOC-INTERNO CAP_02_parte_II.md:279]`
  - *Valore di sistema*: il fallimento di consegna lascia una traccia esplicita anziché restare implicito, premessa per diagnosticare i segnali non arrivati all'operatore. *(Il formato del log è Sez.7/Sez.9; qui si prende la politica.)*

- **CN-6.8** *(invariante)* — In caso di fallimento finale, il `signal_id` **non** viene aggiunto a $\mathcal{P}$ e il segnale è registrato come **non pubblicato**. `[DOC-INTERNO CAP_02_parte_II.md:279]`
  - *Valore di sistema*: mantiene coerente l'invariante anti-duplicato (CN-6.4): solo i segnali effettivamente consegnati entrano in $\mathcal{P}$, così un eventuale ritentativo futuro resta legittimo e lo stato riflette la realtà della consegna.

- **CN-6.9** *(invariante)* — Il fallimento di pubblicazione è tracciato nel log e non rimane implicito. `[DOC-INTERNO CAP_02_parte_II.md:281]`
  - *Valore di sistema*: garantisce che ogni mancata consegna sia esplicitamente registrata, premessa di un audit trail completo e di un'eventuale azione correttiva.

### 6.6 Layout mobile-first (estensione CAP_06 PVI Cap.29)

> Materia di **consegna** di CAP_06 Parte VI Cap.29 (recupera NFR-6.1 e R-6.4 della v2). Le 9 voci del contratto a 9 campi (§6.2) e la pubblicazione della notifica `trigger_event` (§6.4) sono **citate come premessa**, non ri-elencate.

- **NFR-6.5** — Il messaggio di consegna è progettato perché l'operatore lo legga e ci agisca da schermo di cellulare in condizioni di attenzione limitata e discontinua durante la giornata lavorativa; questo profilo operativo è il criterio di progettazione del messaggio Telegram in Cap.29 (mobile-first). `[DOC-INTERNO CAP_06_parte_VI.md:146]`
  - *Valore operativo*: chi opera da cellulare in pause brevi coglie il segnale a colpo d'occhio e può agire subito, riducendo il rischio di errore di lettura prima dell'invio manuale dell'ordine.

- **NFR-6.6** — Il layout mobile-first **rappresenta** le 9 voci del payload formale di §6.2 riordinandole per priorità di lettura: **nessun campo nuovo** è introdotto e nessuno è omesso; la distinzione dichiarata è *payload formale (immutabile) vs rappresentazione mobile (cosmetica)*. `[DOC-INTERNO CAP_06_parte_VI.md:146]` `[DOC-INTERNO CAP_06_parte_VI.md:148]`
  - *Valore operativo*: l'operatore vede sempre le stesse informazioni del contratto (niente in più che lo distragga, niente in meno che gli manchi), solo disposte per la lettura mobile; ciò che legge sul cellulare è esattamente ciò che il motore ha pubblicato e loggato. *(Il contratto a 9 voci è §6.2 / CN-6.1, R-6.1..9; Cap.9.2 di Parte II resta il riferimento normativo del contenuto.)*

- **NFR-6.7** — Il messaggio è interamente testuale e self-contained ed è progettato per schermi mobile di larghezza tipica, leggibile **senza scroll orizzontale** (linee corte) e con il contenuto critico (direzione, entry_zone, target_1, stop_loss) visibile **entro la prima schermata** (senza scroll verticale eccessivo). `[DOC-INTERNO CAP_06_parte_VI.md:152]`
  - *Valore operativo*: l'operatore legge le informazioni che servono per decidere senza dover scorrere il messaggio, evitando di perdere un campo critico (es. il lato o lo stop) in fondo a un testo lungo.

### 6.7 Le 3 notifiche standard per segnale (estensione CAP_06 PVI Cap.29)

- **R-6.17** — Per ogni segnale il canale Telegram pubblica **esattamente 3 notifiche standard**: (i) **emissione** (R-6.18), (ii) **`trigger_event`** se avviene il raw touch (R-6.19), (iii) **transizione a stato terminale** (R-6.21). `[DOC-INTERNO CAP_06_parte_VI.md:220]`
  - *Valore operativo*: l'operatore sa in anticipo quante e quali comunicazioni riceverà per ciascun segnale, così non resta in attesa di messaggi che non arriveranno né teme di averne persi.

- **R-6.18** — La prima delle 3 notifiche standard è il **messaggio di emissione**, che pubblica le 9 voci del payload nel layout mobile-first al momento dell'emissione del segnale. `[DOC-INTERNO CAP_06_parte_VI.md:220]` `[DOC-INTERNO CAP_06_parte_VI.md:156]`
  - *Valore operativo*: l'operatore è avvisato dell'esistenza del segnale e ne riceve i parametri appena il motore lo emette, in tempo per valutare l'ingresso. *(La pubblicazione del messaggio di emissione e il suo contratto informativo a 9 voci sono §6.2; qui si consolida il suo ruolo di **prima delle 3 notifiche standard**.)*

- **R-6.19** — La seconda delle 3 notifiche standard è la notifica **`trigger_event`**, pubblicata **se avviene** il raw touch della `entry_zone`, come messaggio Telegram separato dal messaggio di emissione. `[DOC-INTERNO CAP_06_parte_VI.md:220]` `[DOC-INTERNO CAP_06_parte_VI.md:192]`
  - *Valore operativo*: l'operatore è avvisato nel momento esatto in cui il prezzo è entrato in zona e il segnale è eseguibile, informazione tempestiva e azionabile. *(La **pubblicazione** della notifica `trigger_event` come messaggio separato è §6.4 / R-6.12, CN-6.7; il `trigger_event` come **evento** del lifecycle è Sez.4 / R-4.26. Qui si consolida il suo ruolo di **seconda delle 3 notifiche standard**.)*

- **R-6.20** — La notifica `trigger_event` è un messaggio distinto che **non** modifica il messaggio di emissione (no edit, no append) e riporta esplicitamente il `signal_id` del segnale originario. `[DOC-INTERNO CAP_06_parte_VI.md:192]`
  - *Valore operativo*: l'operatore distingue nettamente la comunicazione "esiste un segnale" da "ora puoi eseguire", e il messaggio già letto non gli cambia sotto gli occhi; il `signal_id` gli permette di correlare le due notifiche. *(Coerente con l'invariante no-edit/immutabilità di §6.4 / CN-6.6; qui ribadito a livello di consegna mobile sulla notifica `trigger_event`.)*

- **R-6.21** — La terza delle 3 notifiche standard è il **messaggio di chiusura**, pubblicato alla transizione del segnale dallo stato `active` a uno degli **stati terminali** del lifecycle, e informa l'operatore della conclusione del segnale e del risultato. `[DOC-INTERNO CAP_06_parte_VI.md:220]` `[DOC-INTERNO CAP_06_parte_VI.md:223]` `[DOC-INTERNO CAP_06_parte_VI.md:225]`
  - *Valore operativo*: l'operatore sa quando il segnale è concluso e con quale esito, così può chiudere mentalmente la posizione e non resta in attesa di un segnale già terminato. *(Gli **stati terminali** e le transizioni del lifecycle sono Sez.4 (R-4.1, CN-4.4); qui si consolida solo la **notifica** della transizione.)*

- **R-6.22** — La notifica di chiusura riporta lo **stato terminale finale** raggiunto dal segnale, uno fra i sei stati terminali del lifecycle. `[DOC-INTERNO CAP_06_parte_VI.md:230]`
  - *Valore operativo*: l'operatore conosce il motivo preciso della chiusura (target raggiunto, stop, scadenza, invalidazione, mancato target, revoca) e può registrarlo per la propria contabilità manuale. *(L'**insieme** dei sei stati terminali è Sez.4 / R-4.1; qui si consolida solo che la notifica li **veicola** alla consegna.)*

- **R-6.23** — La notifica di chiusura riporta il risultato **$R_{gross}$** in punti FIB (positivo, negativo o nullo) per i segnali eseguiti, e **vuoto o `n/a`** per i segnali non eseguiti. `[DOC-INTERNO CAP_06_parte_VI.md:232]`
  - *Valore operativo*: l'operatore legge a chiusura il risultato lordo del segnale in punti, utile per la propria contabilità, con la distinzione esplicita fra segnali eseguiti e segnali mai entrati.

- **R-6.24** — Tra una notifica standard e la successiva l'operatore **non** riceve aggiornamenti di stato del segnale: il motore monitora silenziosamente e l'operatore segue lo stato sul terminale Telegram in modo statico, senza polling né refresh. `[DOC-INTERNO CAP_06_parte_VI.md:220]`
  - *Valore operativo*: il canale resta sgombro tra un evento e l'altro; l'operatore non è bombardato da aggiornamenti continui e dedica attenzione solo ai tre momenti che contano.

**Out-of-scope della Sezione 6**:
| Voce | Destinazione |
|---|---|
| Campi come dato/dominio/immutabilità del payload | **Sez.3** (da B2) — premessa |
| `trigger_event`/stati terminali come evento del lifecycle | **Sez.4** (da B3) — premessa |
| Formato/schema dei log, persistenza, determinismo del replay | **Sez.7/Sez.9** |
| Pipeline di inference real-time, EGARCH (Cap.27); anti-doppio operazionale, tie-break, logging candidati, determinismo (Cap.28) | **Sez.7** (runtime, da B5) |
| Valori congelati ($L_{max}$, $n_{retry}$, $\Delta t_{retry}$ definitivi, soglie $\tau$) | Parte V (§12) |
| Dettaglio tecnico canale Telegram: setup bot, `chat_id`, stringhe esatte, contratto notifica trigger, specifiche API | Appendice E (FASE-D, §12) |

---

## Sezione 7 — Runtime DAPI, sessione & compliance (da B5)

**Valore di prodotto della sezione**: consolida i requisiti funzionali di prodotto del runtime DAPI per la pubblicazione di segnali FIB in produzione — come si connette il canale dati, quale contratto si sottoscrive e come si gestisce il rollover, qual è la finestra operativa, come entrano i cash europei come contesto, e cosa registra l'audit log. È il ponte fra la metodologia v2 (Parte 9) e la FASE-D implementativa.

### 7.1 Canale DAPI

Il canale dati live del runtime è **Directa DAPI** sul gateway Darwin, servizio locale `[DOC-INTERNO CAP_09_parte_9.md:27]`.

- **R-7.1** — La pipeline runtime si connette al gateway Darwin **esclusivamente in loopback su `127.0.0.1`**, mai da rete esterna o da macchina diversa. `[DOC-INTERNO CAP_09_parte_9.md:27]`
  - *Valore operativo*: il modello di sicurezza locale-only è la condizione perché l'operatore possa far girare il runtime sulla propria macchina senza esporre il canale; nessuna superficie di rete da proteggere.

- **R-7.2** — La pipeline apre la porta **`10001`** (datafeed realtime) per ricevere il push di mercato (`PRICE`, `BOOK_5`, `ANAG`) sul FIB front-month e sui cash europei. `[DOC-INTERNO CAP_09_parte_9.md:35]`
  - *Valore operativo*: è la porta che alimenta l'inference live con i tick di mercato.

- **R-7.3** — La pipeline apre la porta **`10003`** (richieste storico: `CANDLERANGE`, `CANDLE`, `TBT`, `TBTRANGE`) per il pull storico (warm-up degli stati condizionali al boot, fino a 100 giorni). `[DOC-INTERNO CAP_09_parte_9.md:37]`
  - *Valore operativo*: alimenta il warm-up necessario perché la pipeline non parta con stato non inizializzato.

- **CN-7.1** — La porta **`10002`** (submission ordini) **non è mai aperta** dalla pipeline runtime. `[DOC-INTERNO CAP_09_parte_9.md:39]`
  - *Valore di sistema*: è la clausola di chiusura architetturale del vincolo "solo emissione, nessuna esecuzione": il sistema pubblica segnali, l'operatore esegue manualmente. La premessa "no order routing" come scelta di prodotto è Sez.1 (CN-1.1, CN-1.3); qui si consolida il fatto runtime che la porta resta chiusa.

- **R-7.4** — Alla connessione la pipeline riconosce il gateway tramite il **banner** `DARWIN_STATUS;CONN_OK;TRUE;Release ...` con **prefix-match** sul prefisso `DARWIN_STATUS;CONN_OK;TRUE;Release`, **non** match esatto sull'intera stringa. `[DOC-INTERNO CAP_09_parte_9.md:29]` Banner osservato `DARWIN_STATUS;CONN_OK;TRUE;Release 2.5.1 build 04/02/2025` `[PROVA-EMPIRICA 2026-05-27, CAP_09_parte_9.md:27,29]`.
  - *Valore operativo*: il prefix-match rende l'handshake robusto al cambio di release del gateway (campo variabile), evitando falsi fallimenti di connessione a ogni aggiornamento Darwin.

- **NFR-7.1** — Il file `APIPortSettings.txt` (identificatore locale di account + porte) è **letto in sola lettura** dalla pipeline (mai scritto), è trattato come **dato sensibile / PII** ed è **escluso dal repo via `.gitignore`**. `[DOC-INTERNO CAP_09_parte_9.md:41,43]`
  - *Valore di sistema (compliance)*: l'account code lega un'azione di mercato a una persona fisica; la sola-lettura e l'esclusione dal repo sono la garanzia di non versionare un dato personale.

- **CN-7.2** — In presenza di conflitto sul gateway (sessione DGo o TradingView-Directa concorrente sui socket `127.0.0.1:10001`/`10003`), la pipeline **non tenta workaround automatici**: rileva il conflitto, marca lo stato `RUNTIME_DEGRADED` in audit, notifica il supervisore via Telegram ed esce. La decisione di rimedio è del supervisore, non automatica. `[DOC-INTERNO CAP_09_parte_9.md:45]`
  - *Valore operativo*: evita che la pipeline mascheri un conflitto di canale con retry ciechi; consegna al supervisore una diagnosi netta (chiudere DGo/TradingView).

- **CN-7.3** — La pipeline usa **una sola connessione persistente per porta** (10001 e 10003), mai aperture/chiusure per comando. `[DOC-INTERNO CAP_09_parte_9.md:47]`
  - *Valore di sistema*: scelta architetturale prudente che evita per costruzione qualunque regime di burst di connessioni, indipendentemente dalla soglia di cooldown (la soglia "14 conn / ~30 s" è verifica parziale RM-1, smentita come costante nel regime ~1Hz `[DOC-INTERNO CAP_09_parte_9.md:47,51]`).

### 7.2 Catalogo simboli & rollover

Il catalogo dei simboli del runtime FIB è chiuso e fissato `[DOC-INTERNO CAP_09_parte_9.md:57]`.

- **R-7.5** — La pipeline sottoscrive il **FIB pieno front-month** (`FIB6F` o `FIB6I` secondo il front-month corrente) sulla porta 10001 per il calcolo delle feature e la valutazione del bundle. `[DOC-INTERNO CAP_09_parte_9.md:75]` Convenzione ticker IDEM `<CODE><YEAR><MONTH>` `[DOC-INTERNO CAP_09_parte_9.md:61]`.
  - *Valore operativo*: è lo strumento su cui il motore calcola e valuta i segnali, coerente con la calibrazione sul FIB pieno (premessa Sez.1, moltiplicatore 5€/pt → R-1.16).

- **R-7.6** — Al boot la pipeline **deriva automaticamente** il ticker front-month: esegue SUB sui ticker candidati, ne parsa la risposta `ANAG`, estrae la data di scadenza dalla descrizione (es. `GIU26`, `SET26`) e seleziona il **primo contratto in scadenza non ancora oltrepassato**. `[DOC-INTERNO CAP_09_parte_9.md:96]`
  - *Valore operativo*: il runtime non richiede configurazione manuale del contratto: si auto-allinea al front-month corrente leggendo l'anagrafica.

- **R-7.7** — La decodifica del codice mese segue la convenzione proprietaria Directa-IDEM (non lo standard CME): il codice **`F` = giugno** e il codice **`I` = settembre** sono i codici noti usati dal runtime. `[DOC-INTERNO CAP_09_parte_9.md:61]` `FIB6I`=settembre 2026 `[PROVA-EMPIRICA 2026-05-27, CAP_09_parte_9.md:61]`; `FIB6F`=giugno 2026 `[PROVA-EMPIRICA 2026-05-29 M-4, CAP_09_parte_9.md:61]`.
  - *Valore operativo*: la decodifica corretta del mese è ciò che permette di selezionare il contratto giusto al boot e al rollover.
  - *Nota*: la lookup completa oltre `F`/`I` (in particolare i codici di **marzo e dicembre**) è **PENDING-empirico** (da derivare via ANAG a mercato aperto, fuori scope Cap.55) `[DOC-INTERNO CAP_09_parte_9.md:61]` — vedi §13 e B8 / R-10.7.

- **R-7.8** — Allo **scadere del front-month** (terza venerdì del mese, negoziazione che chiude alle 09:00 CET), la pipeline **al boot della sessione del giorno di scadenza** sottoscrive direttamente il **next-month**, saltando la finestra 08:00–09:00 CET del front in scadenza; non sottoscrive il front in scadenza. `[DOC-INTERNO CAP_09_parte_9.md:98]`, `[DOC-INTERNO CAP_09_parte_9.md:104]`
  - *Valore operativo*: evita di propagare la discontinuità da settlement (liquidità marginale + evento delle 09:00) nello stato condizionato EGARCH del bundle frozen.

- **R-7.9** — Al rollover la pipeline registra in audit (Cap.54) il marker **`CONTRACT_SWITCH`** con payload `{from, to, scadenza_from, trigger: "boot_session_third_friday"}`. `[DOC-INTERNO CAP_09_parte_9.md:103]`
  - *Valore operativo/compliance*: traccia esplicita del cambio di contratto, necessaria per ricostruire a posteriori quale strumento era attivo in ciascuna sessione.

- **CN-7.4** — Lo switch di runtime (dal giorno di scadenza `t` in poi sul next-month, operatività normale fino a `t-1` sul front) è **distinto e non sovrapposto** al filtro pre-expiry di **training** ($N=3$ giorni `t-3..t-1`, Parte 8 Cap.39): le due regole non coincidono. `[DOC-INTERNO CAP_09_parte_9.md:107]`
  - *Valore di sistema*: preserva l'invariante research = runtime senza confondere una regola di training con una di runtime; previene un errore di sovrapposizione.

- **R-7.10** — Il runtime calibra e valuta sul **FIB pieno** (`FIB6F`/`FIB6I`), mentre l'**operatore retail esegue manualmente sul miniFIB** (`MINI6F`/`MINI6I`/…, 1 EUR/pt). La separazione fra strumento di calibrazione/inference e strumento di esecuzione è fattuale nel runtime. `[DOC-INTERNO CAP_09_parte_9.md:75]` miniFIB 1 EUR/pt come strumento di esecuzione operativa `[DOC-INTERNO CAP_09_parte_9.md:69]`.
  - *Valore operativo*: chiarisce all'operatore su quale strumento agire (mini, 1€) rispetto a quello su cui il motore ragiona (pieno). Il moltiplicatore **5 EUR/pt del FIB pieno** è premessa di Sez.1 (R-1.16), qui non ri-asserito; questa sezione consolida la parte miniFIB (1€, esecuzione).

### 7.3 Sessione operativa

- **R-7.11** `[B-2 PROVVISORIO]` — La pipeline runtime opera **esclusivamente** nella finestra **08:00–22:00 CET** (epoca corrente E5). `[DOC-INTERNO CAP_09_parte_9.md:273]`
  - *Valore operativo*: definisce quando il motore è attivo; è la finestra in cui i segnali sono emessi e processati. L'origine normativa della finestra (epoca E5 / `fib_session_calendar.csv`) è premessa di Sez.10 / Cap.41 (vedi §13); qui si consolida la regola operativa. **L'upgrade empirico dell'orario (M-GOV-1) è dipendenza aperta** (B-2, §13): la regola è in vigore, è PENDING l'upgrade del valore a `[PROVA-EMPIRICA]`.

- **R-7.12** — Fuori dalla finestra 08:00–22:00 CET la pipeline è in **stand-by**: resta connessa al gateway per il monitoraggio del riavvio mezzanotte, **non emette segnali e non valuta il bundle**. `[DOC-INTERNO CAP_09_parte_9.md:273]`
  - *Valore operativo*: il runtime non produce segnali fuori orario, ma non perde la connessione né lo stato.

- **R-7.13** — All'apertura di sessione (08:00 CET di ogni giorno di trading) la pipeline verifica il banner, esegue il warm-up, sottoscrive FIB front-month + cash opzionali, e registra il marker **`SESSION_OPEN`** in audit con timestamp UTC e data sessione; da quel momento è in regime steady-state. `[DOC-INTERNO CAP_09_parte_9.md:294]`, `[DOC-INTERNO CAP_09_parte_9.md:299]`
  - *Valore operativo/compliance*: delimita l'inizio dell'operatività della sessione in modo tracciabile.

- **R-7.14** — Alla chiusura (22:00 CET) la pipeline registra il marker **`SESSION_CLOSE`** in audit con timestamp UTC, esegue **UNSUB** delle sottoscrizioni realtime sui cash europei, e conserva la connessione storica per il monitoraggio del riavvio mezzanotte. `[DOC-INTERNO CAP_09_parte_9.md:302]`
  - *Valore operativo*: chiude in modo ordinato la sessione liberando le sottoscrizioni di contesto, senza perdere la connessione di servizio.

- **CN-7.5** — Un segnale in stato **`active`** alla chiusura 22:00 CET **non viene chiuso automaticamente** dalla pipeline: la transizione terminale è governata esclusivamente dal counter cromosoma-specifico della state machine (timer post-trigger $\Delta t_{cromosoma}$), **mai dalla chiusura di sessione**. `[DOC-INTERNO CAP_09_parte_9.md:292]`, `[DOC-INTERNO CAP_09_parte_9.md:302]` Il dettaglio numerico "$\Delta t$ fino a 1680 min / ~due giornate" è ancorato a `[DOC-INTERNO CAP_09_parte_9.md:290]` (unica occorrenza del numero 1680: "dominio fino a 1680 minuti, scavalca le interruzioni notturne fra sessioni").
  - *Valore di sistema*: preserva la semantica multiday del segnale: il dominio temporale (fino a ~due giornate, $\Delta t$ fino a 1680 min `[DOC-INTERNO CAP_09_parte_9.md:290]`) scavalca l'interruzione notturna. La state machine e i suoi stati terminali sono premessa di Sez.4 (R-4.1); qui si consolida la sola regola "22:00 non chiude active".

- **CN-7.6** — Fuori sessione la pipeline **mantiene lo stato del segnale `active` in memoria persistente** (su disco); al boot del giorno successivo lo riprende e, se il counter $\Delta t_{cromosoma}$ è scaduto fuori sessione, applica la transizione al primo boot utile marcandola in audit con timestamp coerente. `[DOC-INTERNO CAP_09_parte_9.md:292]`
  - *Valore di sistema/replay*: garantisce continuità del lifecycle del segnale fra sessione `d` e `d+1`, coerente con l'invariante research = runtime.

### 7.4 Gating cash europei

- **R-7.15** — I cash europei accessibili gratuitamente via DAPI base (DGER=DAX, DSTX50=EuroStoxx50, DITAS=FTSE MIB cash, DFRA=CAC 40) entrano nella pipeline come **logging operativo**: i loro tick `PRICE` sono loggati in audit come canale di contesto, in osservazione passiva. `[DOC-INTERNO CAP_09_parte_9.md:310]` Catalogo cash `[DOC-INTERNO CAP_09_parte_9.md:308]`.
  - *Valore operativo*: fornisce contesto di mercato registrato per debug/analisi post-hoc, senza toccare il motore.

- **R-7.16** — Il **gating qualitativo** opera **dopo** l'emissione del segnale ed esclusivamente sul **payload del messaggio Telegram**: aggiunge una **nota di avvertimento** (es. `[GATING-cash-europei: DGER -2.3% intraday]`) basata sulla condizione cash osservata al momento dell'emissione, senza modificare la decisione di emettere né il contenuto strutturale del segnale (banda, target_1, stop). `[DOC-INTERNO CAP_09_parte_9.md:311]`, `[DOC-INTERNO CAP_09_parte_9.md:324]`
  - *Valore operativo*: dà all'operatore un'avvertenza di contesto sul messaggio, lasciandogli la decisione manuale. Il **contratto del messaggio Telegram** è premessa di Sez.6; qui si consolida solo l'attacco dell'annotazione di gating.

- **CN-7.7** — Il gating qualitativo **non sopprime mai** l'emissione: il segnale è **sempre emesso** dalla state machine, sempre tracciato in audit con `SIGNAL_EMITTED`, sempre conteggiato nelle metriche di lifecycle. `[DOC-INTERNO CAP_09_parte_9.md:311]`
  - *Valore di sistema*: separa nettamente la decisione di emettere (motore) dall'annotazione informativa (payload pubblicato); è la condizione che mantiene il gating fuori dalla logica decisionale del segnale.

- **CN-7.8** — Il cash europeo **non entra** nel feature tensor del GA, **non entra** nella state machine del segnale, **non entra** nel cromosoma e **non entra** nel walk-forward nested. `[DOC-INTERNO CAP_09_parte_9.md:315]`, `[DOC-INTERNO CAP_09_parte_9.md:316]`, `[DOC-INTERNO CAP_09_parte_9.md:317]`, `[DOC-INTERNO CAP_09_parte_9.md:318]`
  - *Valore di sistema*: vincolo di perimetro hard che tiene il motore single-instrument FIB; nessun parametro `cash_eur_threshold` né regola "if DGER drop then blocca" entra nel motore.

- **NFR-7.2** — Le regole di gating qualitativo vivono in un **file di configurazione versionato** fuori dal genoma del bundle (`config/gating_rules.yaml`), modificabile **senza re-training** del bundle. `[DOC-INTERNO CAP_09_parte_9.md:311]`, `[DOC-INTERNO CAP_09_parte_9.md:320]`
  - *Valore operativo*: cambiare una soglia di gating non richiede di ri-eseguire il walk-forward: separazione netta config/genoma.

- **R-7.17** — Quando una regola di gating è attiva, la nota aggiunta al messaggio è tracciata in audit come marker **`GATING_RULE_APPLIED`** con riferimento al `signal_id` della state machine. `[DOC-INTERNO CAP_09_parte_9.md:325]`
  - *Valore operativo/compliance*: rende l'annotazione di gating ricostruibile e legata al segnale a cui si riferisce.

- **CN-7.9** — Lo **stesso segnale è sempre emesso** dal bundle frozen indipendentemente dal valore corrente di `config/gating_rules.yaml`; due replay sulla stessa finestra producono lo stesso event log `SIGNAL_EMITTED` con lo stesso payload strutturale, e solo il campo `nota_gating` del messaggio può variare. Le metriche lifecycle non sono inquinate dal gating (contano i segnali emessi, non i messaggi pubblicati). `[DOC-INTERNO CAP_09_parte_9.md:328]`
  - *Valore di sistema/replay*: preserva il vincolo di replay deterministico bit-exact sull'event log del segnale.

### 7.5 Audit & compliance

- **NFR-7.3** — L'audit log è **strutturato, immutabile e append-only** (mai sovrascritto), una riga per evento; formato consigliato JSON Lines con campi obbligatori `timestamp_utc`, `event_type`, `payload`. `[DOC-INTERNO CAP_09_parte_9.md:360]`
  - *Valore di sistema/compliance*: l'immutabilità append-only è la base della riproducibilità del replay e della prova storica del comportamento del motore.

- **R-7.18** — Per ogni evento operativo il log registra timestamp UTC, tipologia evento (`HANDSHAKE`, `SUB`, `UNSUB`, `CANDLERANGE_REQUEST`, `CANDLE_RESPONSE`, `BOOK_RESPONSE`, `PRICE_RESPONSE`, `ANAG_RESPONSE`, `ERR`, `SESSION_OPEN`, `SESSION_CLOSE`, `WARMUP_COMPLETE`, `RUNTIME_*`, `CONTRACT_SWITCH`, eventi lifecycle del segnale, `GATING_*`) e payload strutturato. `[DOC-INTERNO CAP_09_parte_9.md:353]`, `[DOC-INTERNO CAP_09_parte_9.md:356]`
  - *Valore operativo/compliance*: copre l'intera traccia comandi-risposte-stato necessaria a ricostruire il comportamento del runtime.

- **R-7.19** — Gli eventi del lifecycle del segnale sono loggati **distinti per stato**: marker pre-terminali `SIGNAL_EMITTED`, `SIGNAL_TRIGGERED` e **sei eventi terminali distinti** (`SIGNAL_TARGET_1_HIT`, `SIGNAL_STOPPED`, `SIGNAL_INVALIDATED`, `SIGNAL_MISSED_TARGET`, `SIGNAL_EXPIRED`, `SIGNAL_REVOKED`), in luogo di un evento aggregato `SIGNAL_CLOSED`. `[DOC-INTERNO CAP_09_parte_9.md:353]`, `[DOC-INTERNO CAP_09_parte_9.md:355]`
  - *Valore operativo*: eventi puntuali per-stato consentono di calcolare metriche di lifecycle disaggregate senza ricostruzione a posteriori. I sei stati terminali e la state machine sono premessa di Sez.4 (R-4.1); qui si consolida solo la granularità per-stato del log.

- **R-7.20** — Per l'evento `SIGNAL_MISSED_TARGET`, il payload JSON registra il campo **obbligatorio** `timeout_cause ∈ {pretrigger, posttrigger}`, che distingue il timeout pre-trigger (raw touch non avvenuto entro $T_{touch}^{max}$) dal timeout post-trigger (trade aperto senza target_1 entro $\Delta t_{cromosoma}$). `[DOC-INTERNO CAP_09_parte_9.md:355]`
  - *Valore operativo*: disambigua la causa del miss, abilitando metriche di miss-rate per causa.

- **NFR-7.4** — Il **banner Darwin** è loggato in `HANDSHAKE` (registrazione esplicita della release) e l'**account code** è loggato su `HANDSHAKE` come dato PII/sensibile: **mascherabile** negli export pubblici dell'audit, **in chiaro** nel log locale per replay deterministico. `[DOC-INTERNO CAP_09_parte_9.md:357]`, `[DOC-INTERNO CAP_09_parte_9.md:358]`
  - *Valore di sistema/compliance*: concilia riproducibilità del replay (banner+account in chiaro localmente) e protezione del dato personale (mascheratura negli export).

- **NFR-7.5** — Ogni log file deve garantire accessibilità per **almeno 90 giorni rolling** dalla data di creazione (dalla creazione alla compattazione/archiviazione). `[DOC-INTERNO CAP_09_parte_9.md:364]`
  - *Valore di sistema/compliance*: permette il debug a posteriori di anomalie rilevate fino a 3 mesi dopo l'evento.

- **NFR-7.6** — Tutti i log che contengono almeno un evento `SIGNAL_EMITTED`, `SIGNAL_TRIGGERED` o uno dei sei eventi terminali sono **conservati permanentemente** (mai cancellati, nemmeno dopo i 90 giorni rolling). `[DOC-INTERNO CAP_09_parte_9.md:365]`
  - *Valore di sistema/compliance*: abilita il replay deterministico di qualunque segnale emesso in qualunque finestra storica, per audit interno o ricostruzione post-hoc.

- **NFR-7.7** — Sotto commissioni mensili `< 200 EUR` la pipeline **tollera** l'addebito automatico di **20 EUR/mese** del DAPI Datafeed senza interrompere il servizio, notifica il supervisore via Telegram con un singolo messaggio mensile, e **non** intraprende azioni automatiche di riduzione consumo dati. `[DOC-INTERNO CAP_09_parte_9.md:373]`, `[DOC-INTERNO CAP_09_parte_9.md:376]`, `[DOC-INTERNO CAP_09_parte_9.md:377]`
  - *Valore operativo*: il DAPI Datafeed di base è necessario al funzionamento; la pipeline non lo sospende mai da sé, la decisione economica resta al supervisore. (Il vincolo D-1 "no market data Eurex/CME extra" è distinto e resta invariato sui cross-index `[DOC-INTERNO CAP_09_parte_9.md:375]`.)

**Out-of-scope della Sezione 7**:
| Voce | Destinazione |
|---|---|
| Schema-dato/decoder/format canonico DAPI (CANDLE/PRICE/BOOK_5, Cap.48/49/51) | **Sez.9** (da B6) — dato ricevuto sui canali (R-7.2/3/15), decoder non consolidato qui |
| State machine & 6 stati terminali del segnale | **Sez.4** (da B3) — premessa |
| Contratto del messaggio Telegram (banda, target_1, stop, payload) | **Sez.6** (da B4) — premessa (attacco gating in R-7.16) |
| Epoca E5 / `fib_session_calendar.csv` (origine normativa finestra) | **Sez.10** (Cap.41) — premessa (regola operativa in R-7.11) |
| Pipeline inference, EGARCH-recalibration, anti-doppio, latenza, determinismo replay (Cap.27-28) | premesse di Sez.1/3/6/9 — 0 requisiti propri di Sez.7 |
| Corredo bundle frozen / gate di go-live | **Sez.8** (da B7) |
| Dashboard di monitoraggio lifecycle (Cap.30) — l'audit è suo input | fuori perimetro spec (FASE-D, §12) |
| Esecuzione/gestione attiva post-fill, commissioni di trade (5€/op) | Sez.1/Sez.4 — già coperti |

---

## Sezione 8 — Gate di go-live (da B7)

**Valore di prodotto della sezione**: consolida in requisiti di prodotto i **criteri di gate dichiarati dal metodo** per il go-live del motore — definizione operativa del successo, procedura di validazione OOS, gate statistico DSR, gate di fragilità PBO via CSCV, bootstrap stazionario, immutabilità del frozen bundle, checklist decisionale dei 12 criteri di go-live. È il ponte fra la metodologia v2 (validazione finale) e FASE-D (esecuzione del validator).

> **⚠️ NOTA DI CONFINE DI RUOLO — edge PENDING-empirico / validator (cardine).** Questa sezione consolida **CRITERI DICHIARATI, MAI verdetti né valori d'edge**. Ogni gate è formulato come *criterio/definizione/soglia/procedura dichiarata dal metodo*. Ogni grandezza misurabile — il valore effettivo di DSR, PBO, $E[R_{net}]$, CVaR, MDD, $r_{emit}$, $\rho_{sessions}$; l'esito dei 12 criteri di go-live; la decisione GO/NO-GO — è **PENDING-empirico (validator / FASE-D)** e **mai** asserita come "verificata/superata/confermata". L'emissione di tali verdetti è **esclusiva del ruolo `validator`** (in panchina fino a FASE-D). Verbi vietati su grandezze d'esito ("il bundle supera/passa il gate", "DSR è positivo/significativo", "l'edge esiste/è confermato", "GO") sono assenti. La lista completa delle grandezze PENDING-empirico è in §13.

### 8.1 Definizione operativa del successo (Cap.5 di Parte I)

- **R-8.1** — Il criterio dichiarato definisce come **metrica primaria** l'expected net return per segnale eseguito $E[R_{net}\mid executed]$, valore atteso del rendimento netto in punti FIB di un segnale che ha completato il proprio ciclo di vita fino all'esecuzione e alla chiusura. `[DOC-INTERNO CAP_01_parte_I.md:71]`
  - *Valore*: dà all'operatore una misura unica e confrontabile della redditività attesa del segnale al netto dei costi.

- **R-8.2** — Il criterio dichiarato fissa la relazione lineare $E[R_{net}\mid executed] = E[R_{gross}\mid executed] - 2\cdot c$, con $c = 1$ punto FIB equivalente per operazione (conversione delle commissioni di 5 EUR sul moltiplicatore 5 EUR/punto) e fattore 2 per la doppia operazione apertura+chiusura. `[DOC-INTERNO CAP_01_parte_I.md:73-75]`
  - *Valore*: rende esplicito che il successo è misurato dopo commissioni, coerente con l'operatività reale (5 EUR/op).

- **R-8.3** — Il criterio dichiarato richiede il calcolo, sul replay OOS della state machine, delle metriche di lifecycle: emission count, executable rate, target_1 hit rate, target_2 hit rate ($\pi_{t_2\mid t_1}$), invalidation rate, missed-target rate. `[DOC-INTERNO CAP_01_parte_I.md:77]`
  - *Valore*: descrive il comportamento del segnale lungo tutto il suo ciclo, non solo l'esito finale, dando visibilità su quanti segnali sono eseguibili e quanti convertono.

- **R-8.4** — Il criterio dichiarato richiede il calcolo, sullo stesso replay, delle metriche di rischio: CVaR al 95% del rendimento per segnale eseguito, maximum drawdown intraday dell'equity sintetica di sessione, MAE e MFE aggregati condizionati allo stato di lifecycle terminale. `[DOC-INTERNO CAP_01_parte_I.md:79]`
  - *Valore*: quantifica il rischio di coda e di drawdown a cui l'operatore retail (1 contratto/volta) è esposto.

- **R-8.5** — Il criterio dichiarato subordina la selezione del bundle frozen a gate basati su DSR (filtro primario + significatività al netto del numero di prove) e su PBO via CSCV (fragilità della scelta rispetto a partizioni alternative dei dati). `[DOC-INTERNO CAP_01_parte_I.md:81]`
  - *Valore*: protegge l'operatore dal pubblicare un bundle che funziona solo "sulla carta" per effetto del numero di tentativi (overfitting).

- **R-8.6** — Il criterio dichiarato definisce il motore **accettato per il go-live** se, sui dati OOS della prima campagna, il bundle candidato presenta: DSR positivo e significativo; PBO sotto la soglia calibrata in Parte VII; $E[R_{net}\mid executed]$ positivo dopo commissioni; target hit rate ed executable rate stabili e comparabili fra regime calmo e turbolento; CVaR al 95% e MDD intraday entro limiti dichiarati. Questo è il **criterio di accettazione dichiarato**, il cui *esito* è PENDING-empirico (validator / FASE-D). `[DOC-INTERNO CAP_01_parte_I.md:85]`
  - *Valore*: stabilisce, prima di qualunque misura, la condizione complessiva sotto cui un bundle può essere pubblicato come segnale operativo.

- **CN-8.1** — Il successo del motore è definito **in termini quantitativi e verificabili del segnale**, ed è **distinto** dal risultato economico aggregato dell'operatività dell'utilizzatore. Le componenti governate dall'operatore e non dal motore — esecuzione manuale, disciplina sullo stop personale, gestione del rollover, qualità del feed Directa — **non rientrano** nel criterio di successo del motore. `[DOC-INTERNO CAP_01_parte_I.md:69]`, `[DOC-INTERNO CAP_01_parte_I.md:85]`
  - *Valore*: evita di attribuire al segnale colpe/meriti dell'esecuzione manuale; tutela la valutazione corretta del motore e le aspettative dell'operatore.

### 8.2 Procedura di validazione OOS (Cap.31 di Parte VII)

- **NFR-8.1** — Tutte le metriche di gate sono calcolate dalla **fonte canonica unica** = log di replay deterministico bit-exact (invariante ereditato come premessa da `CAP_02_parte_II.md` Cap.10, non ri-derivato qui), generato durante la valutazione della fitness multi-obiettivo, sulla finestra OOS aggregata. `[DOC-INTERNO CAP_07_parte_VII.md:21]`, `[DOC-INTERNO CAP_07_parte_VII.md:7]`
  - *Valore*: garantisce che la validazione sia riproducibile al bit e auditabile, requisito di fiducia per l'operatore e per FASE-D.

- **CN-8.2** — Il criterio dichiarato impone che **nessuna metrica di Parte VII sia calcolata su fill effettivi del broker**: la verifica di go-live opera interamente sui log di replay, in coerenza col vincolo "solo emissione" (eredità invariante Cap.1 di Parte I). `[DOC-INTERNO CAP_07_parte_VII.md:21]`
  - *Valore*: il motore non esegue ordini; valutarlo sui propri segnali (non sui fill) è coerente col perimetro "segnali, non esecuzione" e protegge da contaminazioni dell'esecuzione manuale.

- **R-8.7** — Il criterio dichiarato definisce la **finestra OOS aggregata** come concatenazione temporale dei $W_{oos}$ degli $F$ fold del walk-forward nested effettivamente completati, **con esclusione** dei blocchi di purge ($P_{purge}=4.200$ barre) ed embargo ($P_{emb}=4.200$ barre) fra in-sample e out-of-sample di ciascun fold, in prevenzione del leakage. `[DOC-INTERNO CAP_07_parte_VII.md:15-19]`
  - *Valore*: assicura che la valutazione del segnale avvenga su dati realmente fuori campione, evitando di sovrastimare la bontà del segnale per leakage.

- **R-8.8** — Il criterio dichiarato impone che la selezione del cromosoma vincente $\theta^*$ (bundle candidato) dal fronte di Pareto $\mathcal{F}_1$ sia **deterministica e lessicografica**, applicando in sequenza sei filtri ordinati più un criterio finale di massimizzazione con tie-break esplicito, coerente col replay bit-exact. `[DOC-INTERNO CAP_07_parte_VII.md:29]`
  - *Valore*: un'unica selezione riproducibile elimina arbitrarietà; lo stesso input produce sempre lo stesso bundle, requisito di audit.

- **R-8.9** — Il criterio dichiarato (Filtro 1) seleziona i cromosomi con $DSR(\theta^{(k)}) > \theta_{DSR} = 0{,}95$, eliminando i cromosomi statisticamente non distinguibili dal benchmark deflazionato. (Esito su singolo cromosoma = PENDING-empirico.) `[DOC-INTERNO CAP_07_parte_VII.md:31]`
  - *Valore*: come primo setaccio, scarta segnali la cui performance può essere frutto del numero di prove.

- **R-8.10** — Il criterio dichiarato (Filtro 2) seleziona, fra i sopravvissuti al Filtro 1, i cromosomi con $PBO(\theta^{(k)}) < \theta_{PBO} = 0{,}50$, eliminando quelli la cui scelta dipende fragilmente dalla partizione del dato OOS. (Esito = PENDING-empirico.) `[DOC-INTERNO CAP_07_parte_VII.md:33]`
  - *Valore*: scarta segnali la cui bontà è un artefatto di quale fetta di dati è stata usata.

- **R-8.11** — Il criterio dichiarato (Filtro 3) seleziona, fra i sopravvissuti al Filtro 2, i cromosomi con $|f_5^{global}(\theta^{(k)})| < \theta_{f_5} = 0{,}30$ (stabilità cross-regime sulla finestra OOS aggregata), eliminando i cromosomi sbilanciati verso un solo regime. `[DOC-INTERNO CAP_07_parte_VII.md:35]`
  - *Valore*: privilegia segnali che funzionano sia in mercato calmo sia turbolento, riducendo il rischio per l'operatore al cambio di regime.

- **R-8.12** — Il criterio dichiarato (Filtro 4) seleziona, fra i sopravvissuti al Filtro 3, i cromosomi con $\text{IQR}_{norm}(f_1)(\theta^{(k)}) < \theta_{IQR} = 0{,}40$, eliminando i cromosomi con metrica $f_1$ instabile fra fold. `[DOC-INTERNO CAP_07_parte_VII.md:37]`
  - *Valore*: privilegia segnali la cui redditività attesa è stabile nel tempo, non concentrata in pochi periodi fortunati.

- **R-8.13** — Il criterio dichiarato (Filtro 5) seleziona, fra i sopravvissuti al Filtro 4, i cromosomi con $\pi_{t_2\mid t_1}^{aggregated}(\theta^{(k)}) > \theta_{t_2} = 0{,}30$, eliminando i cromosomi che producono molti `target_1_hit` di scarsa qualità informativa per la submachine. `[DOC-INTERNO CAP_07_parte_VII.md:39]`
  - *Valore*: privilegia segnali il cui primo target tende a proseguire verso il secondo, informazione utile alla gestione manuale della posizione.

- **R-8.14** — Il criterio dichiarato seleziona, fra i sopravvissuti ai filtri 1-5, il cromosoma $\theta^*$ con $f_1^{global}$ (mediana cross-fold) massimo; in caso di parità entro tolleranza $\epsilon_{f_1}=10^{-6}$ pt FIB applica un tie-break lessicografico crescente in tre livelli: minimo $\text{IQR}_{norm}(f_1)$, minimo $|f_5^{global}|$, hash deterministico del cromosoma. `[DOC-INTERNO CAP_07_parte_VII.md:41]`, `[DOC-INTERNO CAP_07_parte_VII.md:43-46]`
  - *Valore*: chiude la selezione su un unico bundle in modo deterministico anche a parità, garantendo riproducibilità totale.

- **R-8.15** — Il criterio dichiarato stabilisce che, se nessun cromosoma del fronte $\mathcal{F}_1$ sopravvive ai filtri 1-5, il run è dichiarato **fallito di go-live** e si produce un report di fallimento con motivazione esplicita (quale filtro ha eliminato l'ultimo candidato e su quale soglia). La decisione di ricalibrazione è rinviata alla sessione operativa post-fallimento. (L'occorrenza effettiva = PENDING-empirico.) `[DOC-INTERNO CAP_07_parte_VII.md:50]`
  - *Valore*: garantisce che, in assenza di un bundle valido, il sistema **non pubblichi** segnali, proteggendo l'operatore; e che il fallimento sia tracciato per la correzione successiva.

### 8.3 Gate statistico primario — DSR (Cap.32 di Parte VII)

- **R-8.16** — Il criterio dichiarato definisce il DSR come gate primario di significatività della performance al netto di: (i) numero $N_{trials}$ di prove (bias di selezione), (ii) lunghezza finita $n$ del campione, (iii) non-normalità (skewness $\hat\gamma_3$, curtosi $\hat\gamma_4$). La formula adottata è la formulazione canonica Bailey-López de Prado 2014 (CDF normale di $(\widehat{SR}-SR^*)\sqrt{n-1}$ corretta per skew/curtosi), con $N_{trials}=|\mathcal{F}_1|$. `[DOC-INTERNO CAP_07_parte_VII.md:139]`, `[DOC-INTERNO CAP_07_parte_VII.md:143]`. Riferimento bibliografico del capitolo: Bailey-López de Prado 2014 `[WIKI-HINT, da verificare]` (citato dal capitolo, non fonte di prima istanza).
  - *Valore*: traduce in un singolo numero la domanda "questo segnale è migliore del caso, dato che ho provato molti cromosomi?", proteggendo dall'illusione statistica.

- **R-8.17** — Il criterio dichiarato fissa la soglia $\theta_{DSR}=0{,}95$ (test a un solo lato al 5% contro $H_0: SR\le SR^*$), **valore di lavoro provvisorio non congelato in Parte VII, riconsiderato post-go-live**. Il valore *effettivo* di $DSR(\theta^*)$ è PENDING-empirico (validator). `[DOC-INTERNO CAP_07_parte_VII.md:202]`, `[DOC-INTERNO CAP_07_parte_VII.md:204]`, `[DOC-INTERNO CAP_07_parte_VII.md:244]`
  - *Valore*: stabilisce in anticipo l'asticella di significatività; dichiararla provvisoria evita che venga trattata come legge definitiva prima dei dati di produzione.

### 8.4 Gate di fragilità — PBO via CSCV (Cap.33 di Parte VII)

- **R-8.18** — Il criterio dichiarato definisce il PBO come probabilità che il cromosoma vincente in-sample sia overfit (OOS sotto la mediana del fronte), stimato via **Combinatorially Symmetric Cross-Validation** in **sei passi** (partizione in $S$ sotto-finestre contigue, enumerazione $\binom{S}{S/2}$, rank Sharpe in-sample, rank OOS del vincente, logit-rank, frazione di combinazioni con logit-rank negativa). `[DOC-INTERNO CAP_07_parte_VII.md:252]`, `[DOC-INTERNO CAP_07_parte_VII.md:254]`. Riferimento bibliografico del capitolo: Bailey-Borwein-López de Prado-Zhu 2017 `[WIKI-HINT, da verificare]`.
  - *Valore*: misura se la bontà del segnale resiste a partizioni alternative dei dati, proteggendo da segnali fragili.

- **R-8.19** — Il criterio dichiarato fissa il numero di sotto-finestre $S$ secondo la regola deterministica $S = 2F$ (2 blocchi per fold), con $S$ pari e $S \in \{12,14,16\}$ ($S=12$ per $F=6$, $S=14$ per $F=7$, $S=16$ per $F=8$), preservando la struttura temporale di ciascun fold. `[DOC-INTERNO CAP_07_parte_VII.md:294-298]`, `[DOC-INTERNO CAP_07_parte_VII.md:322]`
  - *Valore*: lega il numero di partizioni alla struttura reale dei dati in modo riproducibile, evitando rotture artificiali della dipendenza temporale.

- **R-8.20** — Il criterio dichiarato fissa la soglia $PBO(\theta^*) < \theta_{PBO}=0{,}50$ (gate minimo), **valore di lavoro provvisorio non congelato in Parte VII, riconsiderato post-go-live** (possibile innalzamento a $0{,}40$ post-go-live). Il valore *effettivo* di $PBO(\theta^*)$ è PENDING-empirico (validator). `[DOC-INTERNO CAP_07_parte_VII.md:304]`, `[DOC-INTERNO CAP_07_parte_VII.md:308]`, `[DOC-INTERNO CAP_07_parte_VII.md:344]`
  - *Valore*: stabilisce in anticipo la soglia di fragilità tollerata; la provvisorietà evita di trattarla come definitiva prima dei dati.

### 8.5 Intervalli di confidenza — bootstrap stazionario (Cap.34 di Parte VII)

> *Nota framing*: il bootstrap stazionario è il *meccanismo statistico interno* che produce gli $IC_{95\%}$ usati dal gate R-8.26 ($E[R_{net}]>0$ con IC che esclude lo zero). I requisiti R-8.21/22/23 ne fissano procedura, replicazione e uso, a corredo del gate sull'$E[R_{net}]$.

- **R-8.21** — Il criterio dichiarato definisce il bootstrap stazionario (Politis-Romano 1994) come ricampionamento a **blocchi di lunghezza aleatoria geometrica** ($p=1/L_{avg}$) sui rendimenti $R_{net}$ dei segnali eseguiti, con wrap modulo $n$ che garantisce la stazionarietà del processo bootstrappato. `[DOC-INTERNO CAP_07_parte_VII.md:352]`, `[DOC-INTERNO CAP_07_parte_VII.md:354-356]`, `[DOC-INTERNO CAP_07_parte_VII.md:358]`. Riferimento bibliografico del capitolo: Politis-Romano 1994 `[WIKI-HINT, da verificare]`.
  - *Valore*: produce intervalli di confidenza che rispettano la dipendenza temporale dei rendimenti del segnale, dando una stima onesta dell'incertezza.

- **R-8.22** — Il criterio dichiarato fissa $B = 2.000$ replicazioni bootstrap (eredità Cap.4 di Parte I, compute budget cloud), producendo la distribuzione empirica da cui si ricavano gli $IC_{95\%}$ via percentile method (default; BCa alternativa per metriche skewed). `[DOC-INTERNO CAP_07_parte_VII.md:359]`, `[DOC-INTERNO CAP_07_parte_VII.md:379-381]`, `[DOC-INTERNO CAP_07_parte_VII.md:449]`
  - *Valore*: fissa un numero di repliche sufficiente a stabilizzare gli intervalli, dentro il budget di calcolo del progetto.

- **R-8.23** — Il criterio dichiarato impone la calibrazione automatica di $L_{avg}$ via Politis-White 2004 su ogni run; il valore $L_{avg}=10$ segnali è **default di lavoro provvisorio non congelato in Parte VII**, solo starting point (con troncamenti ai bordi $L_{avg}\in[1, n/5]$). Il valore *effettivo* calibrato è PENDING-empirico. `[DOC-INTERNO CAP_07_parte_VII.md:369]`, `[DOC-INTERNO CAP_07_parte_VII.md:371]`, `[DOC-INTERNO CAP_07_parte_VII.md:373]`, `[DOC-INTERNO CAP_07_parte_VII.md:449]`
  - *Valore*: adatta la lunghezza dei blocchi all'autocorrelazione reale dei segnali, senza fissare a priori un valore arbitrario.

- **NFR-8.2** — Il criterio dichiarato impone che il seed PRNG del bootstrap sia parte dell'identità del bundle frozen e separato dagli altri seed; due esecuzioni con stesso seed, stessi log e stesso $L_{avg}$ producono **identici intervalli di confidenza al bit**, in coerenza col vincolo di replay bit-exact. `[DOC-INTERNO CAP_07_parte_VII.md:445]`, `[DOC-INTERNO CAP_07_parte_VII.md:447]`
  - *Valore*: rende gli intervalli di confidenza riproducibili e auditabili, requisito di fiducia per FASE-D.

### 8.6 Frozen bundle e immutabilità (Cap.35 di Parte VII)

- **CN-8.3** — Il criterio dichiarato definisce il **bundle frozen** come artefatto digitale **immutabile** composto da sei elementi: (1) parametri congelati di Parte V; (2) geni del cromosoma vincente $\theta^*$; (3) modelli stimati (EGARCH, Cox/Fine-Gray, quantili regime); (4) definizione formale della tupla payload $\mathcal{S}$; (5) seed PRNG; (6) metadati di tracciabilità. `[DOC-INTERNO CAP_07_parte_VII.md:457]`, `[DOC-INTERNO CAP_07_parte_VII.md:459]`, `[DOC-INTERNO CAP_07_parte_VII.md:461-466]`, `[DOC-INTERNO CAP_07_parte_VII.md:483-500]`
  - *Valore*: ciò che va in produzione è un oggetto unico, completo e congelato; nulla cambia "in silenzio" dopo la pubblicazione del segnale.

- **CN-8.4** — Il criterio dichiarato impone il calcolo deterministico di un **hash crittografico SHA-256** sull'intero contenuto dei sei elementi (serializzazione canonica), registrato nel bundle come campo `bundle_hash`. `[DOC-INTERNO CAP_07_parte_VII.md:506]`, `[DOC-INTERNO CAP_07_parte_VII.md:509-510]`
  - *Valore*: dà un'impronta univoca al bundle, base per integrità e tracciabilità di ogni segnale emesso.

- **CN-8.5** — Il criterio dichiarato impone che, a ogni caricamento del bundle in pipeline, l'hash sia ricalcolato e confrontato col `bundle_hash` registrato; se i due hash **non coincidono al bit**, il caricamento **fallisce e la pipeline si rifiuta di girare**, con log esplicito dell'errore di integrità. `[DOC-INTERNO CAP_07_parte_VII.md:512-517]`
  - *Valore*: protegge l'operatore da un bundle corrotto o alterato — meglio nessun segnale che un segnale prodotto da un bundle compromesso.

- **R-8.24** — Il criterio dichiarato governa la sostituzione del bundle con quattro regole esplicite — (1) pianificata trimestrale/semestrale, (2) anticipata su trigger di deriva, (3) anticipata su Cox time-varying attivato, (4) anticipata su fallimento di go-live — con regola comune: i segnali in stato `active` alla transizione **continuano la propria state machine con il bundle precedente** fino a uno stato terminale; solo le nuove emissioni usano il nuovo bundle. La motivazione è registrata in `replacement_reason`. `[DOC-INTERNO CAP_07_parte_VII.md:523]`, `[DOC-INTERNO CAP_07_parte_VII.md:525]`, `[DOC-INTERNO CAP_07_parte_VII.md:533]`
  - *Valore*: garantisce continuità del servizio (un segnale in corso non cambia regole a metà) e tracciabilità del motivo di ogni sostituzione.

### 8.7 Gate decisionali di go-live (Cap.36 di Parte VII)

> I 12 criteri di go-live sono consolidati come **12 requisiti distinti** (atomicità N1: un criterio binario OK/NOT-OK ciascuno). **Ogni criterio è un gate *dichiarato*; l'esito di ciascuno e la decisione complessiva sono PENDING-empirico (validator / FASE-D).** *(NB ordinamento: il capitolo enumera AC-GO-2 = gate PBO e AC-GO-3 = expected net return; per atomicità i requisiti tracciano uno-a-uno ai criteri — R-8.26 traccia ad AC-GO-3 `:574`, R-8.27 traccia ad AC-GO-2 `:572`. La numerazione `R-8.*` non riproduce l'ordine `AC-GO-*`; la corrispondenza puntuale è in §11.1.)*

- **R-8.25** — Criterio di go-live 1, OK/NOT-OK: $DSR(\theta^*) > \theta_{DSR}=0{,}95$. (Esito = PENDING-empirico.) `[DOC-INTERNO CAP_07_parte_VII.md:570]`
  - *Valore*: ribadisce come gate esplicito di go-live la significatività statistica della performance.

- **R-8.26** — Criterio di go-live 3 (AC-GO-3), OK/NOT-OK: $E[R_{net}\mid executed](\theta^*) = f_1^{global}(\theta^*) > 0$ **con $IC_{95\%}$ bootstrap $[a,b]$ tale che $a>0$**. (Esito e IC effettivi = PENDING-empirico.) `[DOC-INTERNO CAP_07_parte_VII.md:574]`
  - *Valore*: richiede che la redditività attesa netta sia non solo positiva ma statisticamente distinta da zero, alzando la garanzia per l'operatore.

- **R-8.27** — Criterio di go-live 2 (AC-GO-2), OK/NOT-OK: $PBO(\theta^*) < \theta_{PBO}=0{,}50$. (Esito = PENDING-empirico.) `[DOC-INTERNO CAP_07_parte_VII.md:572]`
  - *Valore*: ribadisce come gate esplicito di go-live la non-fragilità della scelta del bundle.

- **R-8.28** — Criterio di go-live 4, OK/NOT-OK: $|f_5^{global}(\theta^*)| < \theta_{f_5}=0{,}30$ (riverifica esplicita del Filtro 3 come gate di go-live). (Esito = PENDING-empirico.) `[DOC-INTERNO CAP_07_parte_VII.md:576]`
  - *Valore*: conferma in fase di go-live che il segnale è bilanciato fra regimi calmo/turbolento.

- **R-8.29** — Criterio di go-live 5, OK/NOT-OK: $\text{IQR}_{norm}(f_1)(\theta^*) < \theta_{IQR}=0{,}40$ (riverifica esplicita del Filtro 4). (Esito = PENDING-empirico.) `[DOC-INTERNO CAP_07_parte_VII.md:578]`
  - *Valore*: conferma in fase di go-live che la redditività attesa è stabile nel tempo.

- **R-8.30** — Criterio di go-live 6, OK/NOT-OK: $\text{CVaR}_{95\%}(\theta^*) > \theta_{CVaR}=-100$ pt FIB, **valore di lavoro provvisorio, non congelato in Parte VII, riconsiderato post-go-live**. (Esito = PENDING-empirico.) `[DOC-INTERNO CAP_07_parte_VII.md:580]`
  - *Valore*: limita la perdita media nei segnali peggiori (worst-5%) a 100 pt, coerente con stop strutturali tipici di FIB intraday e col profilo retail 1 contratto/volta.

- **R-8.31** — Criterio di go-live 7, OK/NOT-OK: $\text{MDD}_{intraday}(\theta^*) < \theta_{MDD}=200$ pt FIB, **valore di lavoro provvisorio, non congelato in Parte VII, riconsiderato post-go-live** ($200\cdot 5 = 1.000$ EUR per contratto). (Esito = PENDING-empirico.) `[DOC-INTERNO CAP_07_parte_VII.md:582]`
  - *Valore*: limita il drawdown intraday massimo a un livello compatibile col profilo retail mobile (1 contratto/volta).

- **R-8.32** — Criterio di go-live 8, OK/NOT-OK: $r_{emit}(\theta^*) \in [E_{min}=0{,}2; E_{max}=5]$ segnali/sessione (riverifica esplicita sul fold OOS aggregato). (Esito = PENDING-empirico.) `[DOC-INTERNO CAP_07_parte_VII.md:584]`
  - *Valore*: garantisce che il motore non sia né silente né iperattivo, coerente con un operatore che esegue manualmente da cellulare.

- **R-8.33** — Criterio di go-live 9, OK/NOT-OK: $\rho_{sessions} > \theta_{sessions}=0{,}60$ (**valore di lavoro provvisorio, non congelato in Parte VII, riconsiderato post-go-live**), dove $\rho_{sessions}$ è la frazione di sessioni del fold OOS aggregato che raggiungono il **target operativo asimmetrico di Cap.1 di Parte I** — 500 pt FIB profitto netto/giorno (soglia assoluta $T_{abs}$) **OR** 70% del movimento strutturale intraday (soglia relativa $T_{rel}$), condizione OR $T(d)=T_{abs}(d)\lor T_{rel}(d)$. (Esito e $\rho_{sessions}$ effettivo = PENDING-empirico.) `[DOC-INTERNO CAP_07_parte_VII.md:586]`, `[DOC-INTERNO CAP_07_parte_VII.md:609-625]`, `[DOC-INTERNO CAP_07_parte_VII.md:629-631]`
  - *Valore*: lega il go-live all'obiettivo operativo concreto dichiarato per il prodotto, tarato sul singolo giorno di trading.

- **R-8.34** — Criterio di go-live 10, OK/NOT-OK **unico** sulla verifica funzionale della pipeline di inference real-time, il cui contenuto di verifica enumera quattro sotto-condizioni: (a) carica correttamente il bundle frozen con hash SHA-256 valido al caricamento; (b) processa un feed di test e produce un payload bit-exact identico alla specifica della tupla a 12 campi; (c) pubblica messaggi Telegram di test conformi al layout mobile-first; (d) la latenza end-to-end rispetta il vincolo qualitativo $L_{max}=30$ s (la verifica numerica empirica di $L_{max}$ resta carryover, vedi NFR-8.3). Le quattro sotto-condizioni sono il contenuto di verifica di un **unico** criterio binario, non requisiti separati. (Esito funzionale = PENDING-empirico, FASE-D.) `[DOC-INTERNO CAP_07_parte_VII.md:588]`, `[DOC-INTERNO CAP_07_parte_VII.md:589-592]`
  - *Valore*: garantisce che il segnale arrivi davvero all'operatore via Telegram, correttamente formattato e in tempi accettabili, prima di dichiarare il go-live.

- **R-8.35** — Criterio di go-live 11, OK/NOT-OK **unico** sulla verifica che la dashboard di monitoring live è configurata e attiva, il cui contenuto di verifica enumera tre sotto-condizioni: (a) tracciamento di tutte le metriche live ($f_1^{live}..f_5^{live}$, $B(t)$, $r_{emit}^{live}$); (b) tutti gli alert configurati e testati (deriva fitness, deriva $f_5^{live}$, break parametrico EGARCH, frequenza emissione fuori range); (c) reporting opzionale lifecycle aggiuntivo. Le tre sotto-condizioni sono il contenuto di verifica di un **unico** criterio binario. (Esito funzionale = PENDING-empirico, FASE-D.) `[DOC-INTERNO CAP_07_parte_VII.md:594]`, `[DOC-INTERNO CAP_07_parte_VII.md:595-597]`
  - *Valore*: garantisce che, una volta live, il comportamento del segnale sia monitorato e gli scostamenti generino alert, proteggendo l'operatore da derive non rilevate.

- **R-8.36** — Criterio di go-live 12, OK/NOT-OK **singolo** (già atomico): il bundle frozen del run corrente ha hash SHA-256 valido all'avvio della pipeline, ovvero il caricamento iniziale non produce errore di integrità (riverifica del meccanismo di CN-8.4/CN-8.5 nel primo caricamento operativo). (Esito = PENDING-empirico, FASE-D.) `[DOC-INTERNO CAP_07_parte_VII.md:599]`
  - *Valore*: ultimo controllo prima del go-live che il bundle pubblicato è integro al primo avvio operativo.

- **CN-8.6** — Il criterio dichiarato definisce la **procedura** di decisione binaria: GO se **tutti i 12 criteri** sono OK; NO-GO se **anche un solo** criterio è NOT-OK, con motivazione esplicita su quale criterio è fallito + raccomandazione operativa per classe (gate statistici → re-applicazione Parte V o ritocco soglie; metriche operative → revisione cromosoma; infrastruttura → correzione tecnica senza re-training). **Questa sezione consolida la procedura; l'esito GO/NO-GO è esclusiva del ruolo `validator`** (PENDING-empirico, FASE-D), mai asserito qui. `[DOC-INTERNO CAP_07_parte_VII.md:601]`, `[DOC-INTERNO CAP_07_parte_VII.md:602-605]`
  - *Valore*: rende la decisione di pubblicazione totalmente deterministica e tracciabile, senza discrezionalità; separa nettamente "chi definisce la regola" (metodo/spec) da "chi emette il verdetto" (validator).

- **R-8.37** — Il criterio dichiarato impone che $\rho_{sessions}$ sia calcolata anche separatamente per sessioni calmo e turbolento, producendo $\rho_{sessions}^{calmo}$ e $\rho_{sessions}^{turbolento}$; la differenza $|\rho^{calmo}-\rho^{turbolento}|$ è **metrica di reporting, non gate binario**. (Valori effettivi = PENDING-empirico.) `[DOC-INTERNO CAP_07_parte_VII.md:633]`
  - *Valore*: dà visibilità su quanto il rendimento operativo dipenda dal regime di mercato, informazione utile per l'operatore senza vincolare il go-live.

- **CN-8.7** — Il criterio dichiarato stabilisce che i 10 parametri di tuning operativo di Parte VI **rimangono starting point con i default proposti di Parte VI** per il primo run di produzione; il loro congelamento empirico richiede dati di produzione live (distribuzione degli alert, frequenza break EGARCH, $r_{emit}^{live}$ effettiva) ed è attività di monitoring post-go-live a 3-6 mesi, **non task di Parte VII**. `[DOC-INTERNO CAP_07_parte_VII.md:637]`, `[DOC-INTERNO CAP_07_parte_VII.md:641]`
  - *Valore*: chiarisce che alcuni parametri si tarano solo con la produzione reale, evitando false certezze prima del go-live.

- **R-8.38** — Il criterio dichiarato definisce che, se gli alert di Parte VI scattano in modo persistente su almeno uno di quattro trigger paralleli (deriva fitness; deriva $f_5^{live}$; break parametrico EGARCH; frequenza emissione fuori range), il ciclo di ritraining è **anticipato** rispetto alla cadenza pianificata, via Regola 2 di sostituzione del bundle; il bundle non si riottimizza in produzione ma si sostituisce con un nuovo bundle frozen. `[DOC-INTERNO CAP_07_parte_VII.md:645]`, `[DOC-INTERNO CAP_07_parte_VII.md:647-654]`, `[DOC-INTERNO CAP_07_parte_VII.md:656]`
  - *Valore*: garantisce che il segnale resti aggiornato quando il mercato cambia, senza alterare in produzione un bundle congelato (coerenza con immutabilità).

- **NFR-8.3** `[B-1 PROVVISORIO]` — Il criterio dichiarato pone come obiettivo qualitativo della catena ingest-feature-inference-Telegram una latenza end-to-end entro $L_{max}=30$ s (**valore di lavoro provvisorio, non congelato in Parte VII, riconsiderato post-go-live**), componente di R-8.34. La **verifica numerica empirica** di $L_{max}$ effettivo su bot reale resta carryover di Appendice E (M-2 OPEN) → **PENDING-empirico**, mai asserita verificata qui. `[DOC-INTERNO CAP_07_parte_VII.md:23]`, `[DOC-INTERNO CAP_07_parte_VII.md:592]`. M-promemoria: M-2 OPEN (CARRYOVER, Appendice E).
  - *Valore*: fissa un'aspettativa di tempestività del segnale per l'operatore mobile, distinguendo l'obiettivo dichiarato dalla sua misura (rinviata). Vedi §13, B-1.

- **NFR-8.4** — Il criterio dichiarato stabilisce che il post-processing di Parte VII (PBO + bootstrap) assorbe **al massimo ~15% del compute budget** (PBO ~1% per $S=12$, fino a ~10% per $S=16$; bootstrap <5%), e che il bootstrap $B=2.000$ gira su istanza cloud (non in locale) come post-processing del walk-forward, entro $T_{budget}=80$h wall-clock. `[DOC-INTERNO CAP_07_parte_VII.md:439]`, `[DOC-INTERNO CAP_07_parte_VII.md:441]`
  - *Valore*: garantisce che i gate statistici non facciano esplodere costo/tempo del ciclo di validazione, mantenendo sostenibile il retraining trimestrale/semestrale.

**Out-of-scope della Sezione 8**:
| Voce | Destinazione |
|---|---|
| Determinismo/replay bit-exact (invariante formale) | premessa `CAP_02 Cap.10` — consolidato come invariante che la procedura OOS preserva (NFR-8.1, NFR-8.2) |
| Fronte di Pareto $\mathcal{F}_1$, NSGA-II, $f_1$-$f_5$, walk-forward nested, purge/embargo | Parte V (§12) — consumati come input |
| Modello EGARCH / regime calmo-turbolento | Parte III (§12) — usato per il reporting separato |
| Pipeline inference (Cap.27), layout Telegram (Cap.29), dashboard+alert (Cap.30) | Parte VI — oggetto di verifica di R-8.34/R-8.35, non ri-specificati |
| Submachine post-target_1 ($\pi_{t_2\mid t_1}$, MFE/MAE) | **Sez.4** (Cap.11) — premessa, usata in R-8.13 e nelle metriche di rischio |
| Target operativo asimmetrico (500 pt / 70% strutturale), pivot detection | Sez.1 (Cap.1) + Parte III (§12) — soglia di R-8.33 |
| Risultati numerici/verdetti GO-NO-GO/valori d'edge effettivi | FASE-D / validator — PENDING-empirico (§13) |
| Congelamento empirico delle soglie; monitoraggio di produzione | post-go-live / FASE-D |

---

## Sezione 9 — Schema-dato DAPI & continuità tape (da B6)

**Valore di prodotto della sezione**: specifica lo **schema-dato DAPI** (decodifica dei record del gateway Directa Darwin) e la **continuità del tape** runtime — come la pipeline traduce i record DAPI in barre normative simmetriche al training, come preserva il replay deterministico, come gestisce warm-up, gap, riconciliazione e storicizzazione.

> **Cautela RM massima**: questa sezione consolida lo schema-dato di un sistema esterno (Directa DAPI), il territorio che ha generato RM-1..RM-4 (incidente schema CANDLE `O;H;L;C` errato). La materia di schema è in larga parte già certificata `[PROVA-EMPIRICA]` (audit CAP-DATA-02, PASS contro DAPI live) e/o ancorata al **decoder di produzione**: ogni claim di schema porta una citazione `path:line` (decoder o CAP chiuso) o `[PROVA-EMPIRICA <data>]`; **nessuna conclusione strutturale poggia sul solo wiki Directa** (RM-3). I blocchi `VERIFICA/PROVE/ALTERNATIVE` (CANDLE/PRICE/BOOK_5) sono **preservati verbatim** dal blocco B6, non riscritti né estesi (AC-G2).

### 9.1 Adapter & schema-dato

- **R-9.1** — La pipeline runtime deve applicare un **adapter DAPI → bundle frozen** che traduce, per ogni minuto della griglia 1-min della sessione corrente, un record DAPI in un record con **esattamente lo stesso schema operativo** del preprocessor di training, in modo che il bundle frozen sia applicato senza re-calibrazione.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:153]`. *Valore*: garantisce che il modello in produzione legga la stessa struttura-dato su cui è stato calibrato (continuità research↔runtime).

- **R-9.2** — L'adapter deve essere un layer di **normalizzazione di schema**, non un layer di traduzione semantica del segnale: produce in tempo reale la stessa griglia 1-min con gli stessi campi e gli stessi flag del bundle frozen di training; il bundle frozen non legge mai dati DAPI grezzi.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:191]`. *Valore*: confina la complessità del canale esterno nell'adapter, isolando il motore da formati e patologie DAPI.

- **R-9.3** — L'adapter deve produrre per la sessione 08:00-22:00 CET una griglia 1-min **uniforme**, con una riga per ogni minuto della finestra di sessione, applicando le stesse regole di forward-fill del training (per i minuti senza trade: Open = High = Low = Close = Close del minuto precedente, Volume = 0, `tick_count = 0`).
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:127]`. *Valore*: la griglia uniforme è la struttura attesa dal feature engineering downstream.

#### 9.1.1 Schema CANDLE — ordine campi certificato (RM-1 + RM-2)

- **R-9.4** — Il payload `CANDLE` del gateway Directa ha l'ordine campi `UFF;MIN;MAX;APE;V`, mappato su `close;low;high;open;volume` (schema canonico `C;L;H;O;V`).
  - *Tracciabilità*: `[CODICE-ESISTENTE export_directa_history_parametric.py:477-481]` (decoder canonico di produzione: commento `# Documentazione Directa: UFF, MIN, MAX, APE => close, low, high, open.`, con `close_v = Decimal(uff)`, `low_v = Decimal(min_)`, `high_v = Decimal(max_)`, `open_v = Decimal(ape)`) + `[CODICE-ESISTENTE probe_dapi.py:247-270]` (`"close": float(p[4]) # UFF`, `"low": float(p[5]) # MIN`, `"high": float(p[6]) # MAX`, `"open": float(p[7]) # APE`) + `[PROVA-EMPIRICA 2026-05-29 V-1]` (M-1, tick-by-tick) + `[DOC-INTERNO CAP_09_parte_9.md:158]`. *Valore*: lo schema corretto dei prezzi è il prerequisito di ogni feature di prezzo; un ordine sbagliato (incidente CANDLE) corrompe tutto il motore.

> **Diff col decoder canonico (RACC-METODO-2)**: i due decoder di produzione concordano token-per-token. `parse_directa_candle` (`export_directa_history_parametric.py:471`) splitta `parts[:9] = kind, symbol, ymd, hms, uff, min_, max_, ape, qty` e mappa `close←uff, low←min_, high←max_, open←ape` (`:477-481`); il decoder runtime `probe_dapi.py:247-270` mappa `p[4]=UFF→close, p[5]=MIN→low, p[6]=MAX→high, p[7]=APE→open`. **Nessun diff**: lo schema in questa spec è identico a entrambi i decoder canonici.

> **Esclusione delle permutazioni alternative (RM-1)**
> ```
> VERIFICA: il payload CANDLE Directa ha nelle posizioni campo UFF;MIN;MAX;APE;V mappate su close;low;high;open;volume.
> PROVE: decoder canonico export_directa_history_parametric.py:471 (split parts[:9]) e :477-481 (UFF→close, MIN→low, MAX→high, APE→open), che ha già processato ~647 dump storici [CODICE-ESISTENTE]; decoder runtime probe_dapi.py:247-270 concorde; V-1 tick-by-tick del 2026-05-29 [PROVA-EMPIRICA 2026-05-29 M-1].
> ALTERNATIVE COMPATIBILI ESCLUSE: ordine wiki Directa O;H;L;C — FALSIFICATO da V-1, che sui tick realtime ha distinto Open da Close (sui soli daily O e C erano indistinguibili, da cui l'errore originale dell'incidente CANDLE). Il wiki Directa è [WIKI-HINT, da verificare], dimostrato inesatto sullo schema CANDLE.
> ALTERNATIVE COMPATIBILI NON ESCLUSE: nessuna.
> ```

- **R-9.5** — `bar_open` (Open della barra) deve essere copiato dal campo `CANDLE` `APE` (open).
  - *Tracciabilità*: `[CODICE-ESISTENTE export_directa_history_parametric.py:481]` (`open_v = Decimal(ape)`) + `[DOC-INTERNO CAP_09_parte_9.md:167]`. *Valore*: campo prezzo della barra normativa.

- **R-9.6** — `bar_high` (High della barra) deve essere copiato dal campo `CANDLE` `MAX` (high).
  - *Tracciabilità*: `[CODICE-ESISTENTE export_directa_history_parametric.py:480]` (`high_v = Decimal(max_)`) + `[DOC-INTERNO CAP_09_parte_9.md:168]`. *Valore*: campo prezzo della barra normativa.

- **R-9.7** — `bar_low` (Low della barra) deve essere copiato dal campo `CANDLE` `MIN` (low).
  - *Tracciabilità*: `[CODICE-ESISTENTE export_directa_history_parametric.py:479]` (`low_v = Decimal(min_)`) + `[DOC-INTERNO CAP_09_parte_9.md:169]`. *Valore*: campo prezzo della barra normativa.

- **R-9.8** — `bar_close` (Close della barra) deve essere copiato dal campo `CANDLE` `UFF` (close = prezzo ufficiale).
  - *Tracciabilità*: `[CODICE-ESISTENTE export_directa_history_parametric.py:478]` (`close_v = Decimal(uff)`) + `[PROVA-EMPIRICA 2026-05-29 V-1]` (M-1) + `[DOC-INTERNO CAP_09_parte_9.md:170]`. *Valore*: campo prezzo della barra normativa; Close è la base del forward-fill.

- **R-9.9** — `volume` (contratti scambiati nella barra) deve essere copiato dal campo `CANDLE` `V` (qty).
  - *Tracciabilità*: `[CODICE-ESISTENTE export_directa_history_parametric.py:471,482]` (`qty` da `parts[:9]`, `volume_v = int(Decimal(qty))`) + `[DOC-INTERNO CAP_09_parte_9.md:171]`. *Valore*: input per le feature di volume.

#### 9.1.2 `tick_count` — input dell'adapter da BOOK_5

- **R-9.10** — Il campo DAPI `CANDLE` **non espone** un `TickCount`: lo schema `CANDLE` ha 9 campi (posizioni 1-9), nessuno dei quali è il count tick.
  - *Tracciabilità*: `[CODICE-ESISTENTE export_directa_history_parametric.py:471]` (`parts[:9]` = `kind, symbol, ymd, hms, uff, min_, max_, ape, qty`, nessun campo tick_count) + `[DOC-INTERNO CAP_09_parte_9.md:172]`. *Valore*: chiarisce che `tick_count` è un campo **derivato** dall'adapter, non un campo nativo DAPI.

- **R-9.11** — In **regime realtime** (porta 10001), l'adapter deve derivare `tick_count` del minuto `t` come **numero di eventi `BOOK_5`** osservati nel minuto `t` sul ticker FIB front-month.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:172]`. *Valore*: proxy puntuale dell'attività di book (microstruttura), simmetrico al `tick_count` reale del training.

- **R-9.12** — In **regime storico** (porta 10003, risposta `CANDLERANGE`), l'adapter deve impostare `tick_count = NULL` (marker assente, non `NaN` numerico), perché lo schema `CANDLE` del gateway non espone tick count.
  - *Tracciabilità*: `[CODICE-ESISTENTE export_directa_history_parametric.py:471]` (nessun tick count nel payload) + `[DOC-INTERNO CAP_09_parte_9.md:172]`. *Valore*: separa onestamente il dato derivabile (realtime) dal dato non disponibile (storico), evitando valori inventati.

- **CN-9.1** — Il discriminante fra regime realtime e regime storico per `tick_count` deve essere la **porta sorgente** del record (10001 vs 10003), **non** il flag `bar_synthetic`.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:172]`. *Valore*: tiene separati due assi ortogonali (provenienza del dato vs presenza-di-trade), evitando confusione semantica.

#### 9.1.3 `bar_synthetic` — input dell'adapter da BOOK_5/PRICE

- **CN-9.2** — Il flag `bar_synthetic` deve essere **booleano** e distinguere **esclusivamente trade vs no-trade**, mai realtime vs storico.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:173]`. *Valore*: invariante di dominio del flag, condizione perché il bundle frozen tratti barre live e storiche allo stesso modo.

- **R-9.13** — Per il FIB futures in **regime realtime** (porta 10001, push `BOOK_5`), la barra 1-min `t` deve essere marcata reale (`bar_synthetic = False`) se nel minuto è stato osservato almeno un evento `BOOK_5` con `bid1_lots >= 1` AND `ask1_lots >= 1`; altrimenti `bar_synthetic = True` con forward-fill del mid level-1 dell'ultima barra reale (`Open = High = Low = Close = (bid1_price + ask1_price) / 2`).
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:173,177]` + posizioni `BOOK_5` certificate (vedi R-9.19..21). *Valore*: regola di sinteticità del FIB realtime, che governa quali barre alimentano le feature di volatilità.

- **R-9.14** — Per il FIB futures in **regime storico** (porta 10003, `CANDLERANGE`), la barra 1-min `t` deve essere marcata reale (`bar_synthetic = False`) se il timestamp `t` compare nella risposta `CANDLE` del gateway; altrimenti `bar_synthetic = True` con forward-fill su Close (`Open = High = Low = Close = Close del minuto precedente`).
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:173,178]`. *Valore*: regola di sinteticità del FIB in warm-up/backfill, simmetrica al training.

- **R-9.15** — Per i cash europei in **regime realtime** (porta 10001, push `PRICE`), la barra 1-min `t` deve essere marcata reale (`bar_synthetic = False`) se nel minuto è stato osservato almeno un evento `PRICE`; altrimenti `bar_synthetic = True` con forward-fill su `last`.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:173,179]`. *Valore*: regola di sinteticità del cash, usata solo dal layer di gating qualitativo, mai dal feature tensor del GA.

- **CN-9.3** — PRICE e BOOK_5 sono **input dell'adapter** (Cap.49), non materia del canale: l'adapter consuma `CANDLE` (OHLCV), `BOOK_5` (`tick_count` realtime + regola `bar_synthetic` del FIB) e `PRICE` (regola `bar_synthetic` del cash per il gating).
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:172-173,177-179]`. *Valore*: posiziona correttamente lo schema PRICE/BOOK_5 come schema-dato consumato dall'adapter; il canale (porte/handshake/sottoscrizione) è premessa di Sez.7.

#### 9.1.4 Schema PRICE realtime — campi certificati e separazione per tipo-messaggio (RM-1)

- **R-9.16** — Lo schema `PRICE` realtime del FIB cash ha `f4 = last`, `f6 = volume cumulato`, `f8 = day_low`, `f9 = day_high` (estremi di giornata).
  - *Tracciabilità*: `[PROVA-EMPIRICA 2026-06-01 W2]` (M-9) + `[DOC-INTERNO CAP_10_parte_10.md:123]` (`f8=day_low, f9=day_high`) + `[CODICE-ESISTENTE probe_dapi.py:289-306]` (decoder runtime: `last = float(p[3])`, campi extra `p[4:]` non disambiguati nel decoder). *Valore*: i campi `f8`/`f9` sono la fonte normativa del low/high giornaliero per la riconciliazione cash (§9.5).

> **Diff col decoder canonico (RACC-METODO-2)**: il decoder di produzione `probe_dapi.py:289-306` decodifica **solo** `last = p[3]` e tratta i campi successivi come `fields_extra = p[4:]` (commento `:290-291`: "schema esatto dei campi extra non documentato, varia tra cash e future"). Quindi la semantica di `f6`/`f8`/`f9` **non ha supporto di codice di produzione (level-2)**: è ancorata a `[PROVA-EMPIRICA 2026-06-01 W2]` (level-1) e al CAP chiuso. Il diff col decoder è esplicito: il decoder copre `last`, la semantica dei campi-estremo è certificata empiricamente, non da codice.

> **Esclusione delle permutazioni alternative su `f8`/`f9` (RM-1)**
> ```
> VERIFICA: nello schema PRICE realtime, f8=day_low e f9=day_high (estremi di giornata).
> PROVE: [PROVA-EMPIRICA 2026-06-01 W2 M-9], cross-check daily CANDLE L/H; cash untraded (DGER) → f5=f6=f7=0 con f8/f9 valorizzati.
> ALTERNATIVE COMPATIBILI ESCLUSE: (a) f8/f9 = best bid/ask — FALSIFICATA dal BOOK_5 simultaneo (M-9, STATO_CORRENTE: l'ipotesi Web "bid/ask" è smentita dal book a 5 livelli osservato nello stesso istante); (b) confusione con la coppia f8/f9 della CANDLE-daily — esclusa: f8/f9 della CANDLE daily (riconciliazione, vedi R-9.17) e f8/f9 del PRICE realtime sono campi di DUE messaggi diversi (namespace per-tipo-messaggio), la coincidenza dell'indice NON implica namespace condiviso.
> ALTERNATIVE COMPATIBILI NON ESCLUSE: f5/f7 (contatori cumulativi) restano NON disambiguati (verifica parziale, §13 PENDING).
> ```

- **R-9.17** — Per la riconciliazione (Cap.60), il low/high ufficiale daily del FIB è preso dai campi `f8`/`f9` della **CANDLE ufficiale daily** (period 86400); questi `f8`/`f9` appartengono allo schema `CANDLE daily`, distinto dallo schema `PRICE realtime` di R-9.16.
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:123]` + `[PROVA-EMPIRICA 2026-06-01 W2]` (M-9). *Valore*: ancora la fonte normativa del low/high per il gate di riconciliazione (§9.5), tenendola separata dal PRICE realtime.

- **CN-9.4** — I campi `f8`/`f9` compaiono in **due schemi distinti** (CANDLE daily per la riconciliazione; PRICE realtime per il canale): la spec li nomina **separati per tipo-messaggio** e non deduce l'uno dall'altro.
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:123]` + `[PROVA-EMPIRICA 2026-06-01 W2]` (M-9, F3). *Valore*: evita una confusione cross-schema che sarebbe un errore di tipo-incidente-CANDLE su namespace condiviso.

#### 9.1.5 Schema BOOK_5 — posizioni certificate (RM-1, RM-2)

- **R-9.18** — Lo schema `BOOK_5` è `BOOK_5;<ticker>;<HH:mm:ss>;` seguito da **10 triple `(lots, orders, price)`** = `[BID×5 best-first][ASK×5 best-first]` (5 livelli BID poi 5 livelli ASK, ciascuno triplo).
  - *Tracciabilità*: `[PROVA-EMPIRICA 2026-06-01 W3]` (M-10) + `[CODICE-ESISTENTE probe_dapi.py:307-317]` (decoder runtime: `BOOK_5;<ticker>;<HH:mm:ss>; bid1_lots;bid1_ord;bid1_price; ... (x5) ask1_lots;ask1_ord;ask1_price; ... (x5)`, con `fields = p[3:]`) + `[DOC-INTERNO CAP_09_parte_9.md:93]`. *Valore*: lo schema del book è la fonte di `tick_count` e della regola `bar_synthetic` del FIB realtime.

> **Diff col decoder canonico (RACC-METODO-2)**: il decoder runtime `probe_dapi.py:307-317` documenta lo schema nel commento (`:308-309`) ma **non parsea le triple** (`fields = p[3:]`, lista grezza). Quindi le posizioni dei singoli campi **non hanno supporto level-2 strutturato**: sono certificate a livello-1 da `[PROVA-EMPIRICA 2026-06-01 W3 / M-10]` (29 eventi / 290 triple su FIB6F front-month liquido). Il diff col decoder è esplicito: il decoder conferma il commento di schema, la certificazione delle posizioni è empirica diretta.

- **R-9.19** — Nello schema `BOOK_5`, `bid1_lots` è il campo 4, `bid1_orders` il campo 5, `bid1_price` il campo 6.
  - *Tracciabilità*: `[PROVA-EMPIRICA 2026-06-01 W3]` (M-10) + `[CODICE-ESISTENTE probe_dapi.py:308]`. *Valore*: posizioni del primo livello BID, usate dalla regola `bar_synthetic` (R-9.13).

- **R-9.20** — Nello schema `BOOK_5`, `ask1_lots` è il campo 19 e `ask1_price` il campo 21.
  - *Tracciabilità*: `[PROVA-EMPIRICA 2026-06-01 W3]` (M-10) + `[CODICE-ESISTENTE probe_dapi.py:309]` (i 5 livelli BID occupano i campi 4-18, i livelli ASK iniziano dal campo 19). *Valore*: posizioni del primo livello ASK, usate dalla regola `bar_synthetic` (R-9.13).

- **R-9.21** — Il mid level-1 usato nel forward-fill della barra FIB realtime sintetica è `(bid1_price + ask1_price) / 2` con `bid1_price` = campo 6 e `ask1_price` = campo 21.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:173]` + `[PROVA-EMPIRICA 2026-06-01 W3]` (M-10). *Valore*: definisce il prezzo del forward-fill realtime in modo univoco sui campi certificati.

> **Esclusione delle permutazioni alternative su BOOK_5 (RM-1)**
> ```
> VERIFICA: lo schema BOOK_5 è [BID×5 best-first][ASK×5 best-first], ogni livello triplo (lots, orders, price); bid1_lots=campo4, bid1_price=campo6, ask1_lots=campo19, ask1_price=campo21.
> PROVE: [PROVA-EMPIRICA 2026-06-01 W3 M-10], 29 eventi / 290 triple su FIB6F front-month liquido [rif. reviews/REVIEW_CAP_DATA_02_RM_RETRO_CLI_review.md].
> ALTERNATIVE COMPATIBILI ESCLUSE: (a) triplo invertito (orders, lots, price) — esclusa da lots >= orders su 290/290 triple; (b) ordine dei blocchi ASK-poi-BID — escluso (blocco 1 sempre discendente = BID su 29/29 eventi); (c) inversione di schema suggerita dall'anomalia bid1>ask1 del campione 27/05 — esclusa: NON riprodotta sul front-month liquido (bid1_price < ask1_price su 29/29), era artefatto del contratto illiquido FIB6I a scadenza lontana, non inversione di schema.
> ALTERNATIVE COMPATIBILI NON ESCLUSE: nessuna sulle posizioni qui asserite.
> ```

#### 9.1.6 Format/header come contesto (Cap.48 — framing)

- **CN-9.5** — Ogni file CSV prodotto dalla pipeline runtime ha header esteso a **13 campi esatti**: `symbol, timeframe, timestamp, date, time, open, high, low, close, volume, tick_count, bar_synthetic, source`.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:117,120]`. *Valore*: contenitore canonico del format runtime; i 13 campi sono enumerati esattamente (no abbreviazioni).

- **CN-9.6** — Il format runtime esteso (13 campi, con `tick_count`/`bar_synthetic`) è distinto dal format **legacy** a 11 campi (`symbol, timeframe, timestamp, date, time, open, high, low, close, volume, source`, senza `tick_count` e `bar_synthetic`).
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:129]` + `[CODICE-ESISTENTE export_directa_history_parametric.py:605-617]` (header legacy del decoder: i 11 campi senza tick_count/bar_synthetic). *Valore*: i due format coabitano; la distinzione evita di rompere la riproducibilità dei sample legacy.

- **CN-9.7** — La colonna `tick_count` del CSV è intero ≥ 0 oppure `NULL`; la colonna `bar_synthetic` è booleano `True`/`False`.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:117]`. *Valore*: vincolo di dominio dei due campi che rendono il CSV simmetrico al bundle frozen.

- **CN-9.8** — Il campo `source` di ogni record CSV runtime (Cap.48) ha dominio chiuso a tre valori: `DIRECTA`, `AGG_FROM_60s`, `AGG_FROM_D`.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:131-138]`. *Valore*: traccia la provenienza del record; è il dominio-base esteso poi dalla storicizzazione (§9.6).

- **CN-9.9** — Il campo `timestamp` è la chiave normativa di allineamento temporale della griglia 1-min; `date` e `time` sono campi derivati di comodità.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:125]`. *Valore*: definisce la chiave di join/allineamento downstream.

### 9.2 Replay deterministico (invariante research = runtime)

- **NFR-9.1** — Il replay del motore deve essere **bit-exact**: a parità di storico delle barre 1-min, di feed ausiliari e di bundle frozen, due esecuzioni indipendenti producono esattamente la stessa sequenza di emissioni, `signal_id`, transizioni di stato e timestamp di transizione.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:291,293]` (premessa, fondazione formale). *Valore*: condizione necessaria perché le metriche di lifecycle abbiano valore probatorio. **Nota di rinvio**: la fondazione formale del replay bit-exact è materia di `CAP_02 Cap.10` (premessa); qui è **consolidata come invariante che l'adapter preserva**, non ri-derivata dal motore.

- **NFR-9.2** — L'adapter DAPI deve preservare l'invariante `research semantics = runtime semantics`: la griglia 1-min prodotta in runtime ha lo stesso schema operativo del tape di training, senza re-calibrazione e senza re-mappatura dello schema.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:21]` (preambolo: replay bit-exact applicato al motore in produzione) + premessa `[DOC-INTERNO CAP_02_parte_II.md:291]`. *Valore*: estende l'invariante formale al layer di ingest, garantendo che il bundle non distingua training da runtime.

- **NFR-9.3** — Il replay runtime deve propagare in modo identico la distinzione fra barre reali e barre sintetiche (`bar_synthetic`) tra due esecuzioni indipendenti sulla medesima finestra storica DAPI.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:21]`. *Valore*: la riproducibilità del flag `bar_synthetic` è precondizione del determinismo delle feature di volatilità.

- **NFR-9.4** — Il flag `bar_synthetic` deve essere propagato nei record runtime del bundle frozen esattamente come nel training, preservando il vincolo di replay bit-exact.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:181]` + premessa `[DOC-INTERNO CAP_02_parte_II.md:293]`. *Valore*: chiude il cerchio fra regola di sinteticità (§9.1.3) e invariante di replay (§9.2).

### 9.3 Warm-up & continuità

#### 9.3.1 Warm-up degli stati condizionali (Cap.51)

- **R-9.22** — Al boot di ogni sessione operativa, la pipeline deve eseguire un **warm-up** degli stati condizionali via pull storico `CANDLERANGE` su porta 10003, con lookback `L_warmup = 30` **giorni di trading IDEM** (valore congelato in Parte 9, NB-4 Opzione A).
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:254]` + sintassi comando `[CODICE-ESISTENTE export_directa_history_parametric.py:228-230]` (`CANDLERANGE <symbol> <start> <end> <period_seconds>`). *Valore*: re-inizializza EGARCH, classificazione di regime e normalizzazione prima che il motore emetta segnali. Il valore `L_warmup = 30` è **esatto** (non "~30").

- **CN-9.10** — Il valore `L_warmup = 30` giorni di trading è **congelato** dentro la metodologia: ogni revisione richiede un nuovo task Planner (rollback non reversibile dentro la Parte).
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:254]`. *Valore*: vincolo di immutabilità del parametro di warm-up.

- **R-9.23** — Al completamento del warm-up, la pipeline deve inserire il marker `WARMUP_COMPLETE` nel log di audit; solo da quel momento entra in regime steady-state e può emettere segnali validi.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:257]`. *Valore*: gate che impedisce emissioni con stato condizionato non inizializzato.

- **CN-9.11** — Il warm-up deve ricalcolare solo lo **stato condizionato corrente** (es. la varianza condizionata corrente, il quantile di regime sulla finestra storica), mantenendo **congelati** i parametri EGARCH cross-session del bundle frozen (nessuna re-calibrazione).
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:256]`. *Valore*: distingue ri-inizializzazione di stato da re-calibrazione, preservando il bundle frozen.

#### 9.3.2 Recupero gap entro la finestra 100gg (Cap.59)

- **R-9.24** — Per gap di durata ≤ ~100 giorni di calendario, la pipeline deve recuperare le barre mancanti via richiesta `CANDLERANGE` su porta 10003 (sintassi: `CANDLERANGE <ticker_front_month> <YYYYMMDDHHMMSS_start> <YYYYMMDDHHMMSS_end> 60`, period in ultima posizione).
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:88]` + `[CODICE-ESISTENTE export_directa_history_parametric.py:228-230]`. *Valore*: ripristina la continuità del tape entro la finestra coperta dal DAPI intraday.

- **CN-9.12** — La finestra di recupero `CANDLERANGE` intraday (period 60) è limitata a ~100 giorni di calendario (finestra scorrevole che tronca al minuto esatto del limite).
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:79-83]` (`[PROVA-EMPIRICA 2026-05-29 V-2]`: saturazione del first_ts a partire da N=80) + `[CODICE-ESISTENTE export_directa_history_parametric.py:61]` (`DEFAULT_INTRADAY_MAX_DAYS = 100`). *Valore*: definisce il confine fra recupero-gap (≤100gg) e restart-stale (>100gg).

- **R-9.25** — Le barre ricostruite dal backfill `CANDLERANGE` devono essere inserite nella griglia 1-min con `source = BACKFILL_FROM_CANDLERANGE`, `bar_synthetic` derivato dalla regola Cap.49 (R-9.14) e `tick_count = NULL` (regime storico).
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:91]`. *Valore*: traccia la provenienza del backfill mantenendo lo schema invariato.

- **R-9.26** — Il recupero gap deve essere **idempotente**: una barra ricostruita che coincide con una già archiviata è un no-op; una divergenza apre una nuova versione dell'archivio (Cap.62), non sovrascrive.
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:90]`. *Valore*: protegge l'integrità dell'archivio dai backfill ripetuti.

- **CN-9.13** — Se un gap attraversa il limite ~100gg, la pipeline deve recuperare la parte entro finestra e marcare il complemento fuori finestra con `RUNTIME_GAP_BEYOND_100D`, instradandolo al fallback di restart >100gg (R-9.27).
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:98]`. *Valore*: gestione esplicita del caso-limite parziale, senza perdita silenziosa di copertura.

#### 9.3.3 Restart >100gg (Cap.61) — requisito distinto

- **R-9.27** — Per downtime continuativo > 100 giorni (oltre la finestra `CANDLERANGE` intraday), la pipeline deve entrare nello stato `RUNTIME_STALE_RESTART` e **non ripartire automaticamente** (intervento del supervisore obbligatorio).
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:157-158]` + `[DOC-INTERNO CAP_09_parte_9.md:260-261]`. *Valore*: protegge il motore dall'esecuzione su un warm-up cross-source non sufficiente. **Requisito distinto** da R-9.24 (recupero-gap entro finestra): trigger, scala temporale e capitolo diversi.

- **R-9.28** — Nel re-bootstrap >100gg, la copertura del periodo di gap deve seguire una procedura a tre step in ordine: (A) recupero da archivio locale `exports/` con `source = BACKFILL_FROM_ARCHIVE`; (B) recupero `CANDLERANGE` daily (period 86400) per cross-check di riconciliazione; (C) fallback all'archivio Portara/CQG con `source = BACKFILL_FROM_PORTARA`.
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:158-161]`. *Valore*: scala dei fallback dal dato più locale al dato di training, massimizzando la copertura.

- **CN-9.14** — La `CANDLERANGE` daily (period 86400) non ha il cut-off ~100gg dell'intraday: il first_ts regredisce col crescere di N, permettendo cross-check di riconciliazione retroattiva su profondità pluriennale.
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:168-170]` (`[PROVA-EMPIRICA 2026-05-29 V-2]`: first_ts daily non satura fino a N=160). *Valore*: distingue il daily (cross-check profondo) dall'intraday (limitato a 100gg); il daily NON è surrogato delle barre 1-min.

- **R-9.29** — Dopo il re-bootstrap >100gg è **obbligatorio** un re-warm-up completo (`L_warmup = 30` giorni di trading), eseguito solo dopo che il periodo di gap è coperto (step A/B/C completati); al completamento, marker `BOOTSTRAP_COMPLETE`.
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:162]`. *Valore*: garantisce che il bundle EGARCH non venga mai eseguito su un tape mescolato cross-source senza re-warm-up.

- **CN-9.15** — Durante il re-bootstrap >100gg, il tape non è ammesso come input dell'inference live (la pipeline resta in `RUNTIME_STALE_RESTART`); solo dopo `BOOTSTRAP_COMPLETE` + `WARMUP_COMPLETE` la pipeline può tornare a emettere segnali.
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:163-164]`. *Valore*: vincolo di non-mescolamento che impedisce emissioni durante il bootstrap.

- **CN-9.16** — Le barre Portara dello step C entrano convertite alla convenzione **runtime** (unadjusted nativa del front-month corrente), NON ratio-adjusted (che è convenzione di training).
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:161,174]`. *Valore*: preserva la coerenza di back-adjustment fra tape archiviato e convenzione runtime, senza violare l'invariante.

### 9.4 Regola di consumo a valle per-categoria-di-feature (gap-closure AUDITFIX-01, Cap.49 / Cap.40)

> A valle dell'adapter, il consumo delle barre dipende dalla **categoria di feature**: le regole d'uso congelate in Parte 8 Cap.40 si applicano simmetricamente al runtime (identiche a training). La distinzione decisiva è fra feature che **devono ignorare le barre sintetiche** (volatilità, volume, touch) e feature che **usano la griglia uniforme completa** (prezzo, struttura).

- **R-9.38** — Le feature di **volatilità** (EGARCH, classificazione di regime, dispersione realized) devono essere calcolate **esclusivamente su barre con `bar_synthetic = False`** (barre reali), mai su barre sintetiche.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:185]`. *Valore*: includere barre sintetiche (rendimento log identicamente nullo) introdurrebbe bias verso bassa volatilità e contaminerebbe lo stato condizionato; la regola tiene la stima di volatilità in produzione identica a quella di training.

- **R-9.39** — Le feature di **prezzo** (livelli, distanze da zone, distanze da pivot strutturali) devono usare la **griglia uniforme completa**, inclusi i minuti sintetici.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:186]`. *Valore*: i livelli e le distanze sono definiti su ogni minuto della griglia (un prezzo esiste anche nei minuti senza trade, via forward-fill); escludere i minuti sintetici romperebbe l'allineamento temporale con il training.

- **R-9.40** — Le feature di **volume** devono usare **esclusivamente barre con `bar_synthetic = False`** (le barre sintetiche hanno `volume = 0` per costruzione).
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:187]`. *Valore*: contare i minuti sintetici (volume zero per costruzione) distorcerebbe le statistiche di volume; la regola è identica a training.

- **R-9.41** — Le feature di **struttura** (pivot frattali, EMA con reset cross-session) devono usare la **griglia uniforme completa** per il time-indexing; i pivot non sono spostati dalle barre sintetiche.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:188]`. *Valore*: la struttura (pivot, EMA) è indicizzata sull'intera griglia temporale; le barre sintetiche partecipano al time-indexing senza spostare i pivot, preservando la simmetria con training.

- **R-9.42** — Il **touch della entry zone** (raw touch) **non deve mai essere dichiarato su una barra con `bar_synthetic = True`**.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:189]`. *Valore*: dichiarare un touch su una barra sintetica (prezzo forward-fillato, nessun trade reale) genererebbe un trigger su un evento di prezzo mai accaduto sul mercato; la gap semantics è simmetrica fra training e runtime per l'invariante research = runtime.

### 9.5 Riconciliazione canonica giornaliera (Cap.60)

- **R-9.30** — A fine sessione (chiusura 22:00 CET, marker `SESSION_CLOSE`), la pipeline deve eseguire la **riconciliazione canonica giornaliera** come gate operativo end-of-day sul tape del giorno `d`.
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:119]`. *Valore*: verifica end-of-day che protegge contro la deriva silenziosa del feed.

- **R-9.31** — La riconciliazione deve verificare l'integrità di schema: header CSV esteso (13 campi), dominio `source` esteso, dominio `bar_synthetic` booleano, presenza di tutti gli 840 timestamp 1-min attesi, monotonia temporale stretta; il fallimento produce il marker `RECONCILE_SCHEMA_FAIL` + notifica supervisore.
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:121]`. *Valore*: primo check del gate, blocca tape strutturalmente malformati.

- **R-9.32** — La riconciliazione deve verificare la coerenza CANDLE 1-min: il tape composto del giorno `d` è confrontato con una `CANDLERANGE` di controllo dello stesso giorno; divergenza oltre tolleranza (≤1 tick = ≤5pt FIB) su più di `θ_reconcile` minuti produce il marker `RECONCILE_DIVERGENT_FIB` + notifica supervisore.
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:122]`. *Valore*: secondo check del gate, intercetta divergenze diffuse sui minuti.

- **R-9.33** — La riconciliazione deve verificare il low/high giornaliero del FIB confrontandolo con i campi `day_low`/`day_high` (`f8`/`f9`) della CANDLE ufficiale daily (period 86400), tolleranza ≤1 tick FIB (5pt); divergenza oltre tolleranza produce `RECONCILE_DIVERGENT_HIGHLOW`.
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:123]` + `[PROVA-EMPIRICA 2026-06-01 W2]` (M-9). *Valore*: terzo check del gate, verifica gli estremi di giornata.

- **CN-9.17** — Per i ticker cash europei, la riconciliazione del low/high deve usare **esclusivamente** la CANDLE ufficiale daily (`f8`/`f9`), **mai** l'aggregato dei tick realtime, perché il feed `PRICE` cash è rado e perde i minimi intraday.
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:123,136-139]` (`[PROVA-EMPIRICA 2026-06-01 V-1 afternoon §2.4.5]`: 6/6 mismatch DITAS sul solo low). *Valore*: evita falsi `RECONCILE_DIVERGENT_HIGHLOW` dovuti alla radezza del feed cash.

- **R-9.34** — Il verdetto della riconciliazione deve essere la **congiunzione** dei tre check (integrità schema, coerenza CANDLE 1-min, coerenza low/high): `RECONCILE_OK` se tutti passano; `RECONCILE_DIVERGENT_*` se uno o più check di coerenza falliscono; `RECONCILE_DEGRADED` se il tape è incompleto.
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:124-127]`. *Valore*: regola di propagazione fail-stop del gate.

- **CN-9.18** — In caso di `RECONCILE_DIVERGENT_*`, la pipeline deve impostare un flag che **blocca l'emissione di segnali del giorno `d+1`** finché il supervisore non interviene (gate operativo bloccante).
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:126]`. *Valore*: protezione operativa contro l'emissione di segnali su un feed la cui coerenza è in dubbio.

- **CN-9.19** — La riconciliazione deve essere **non-mutativa** sui prezzi delle barre composte (layer di sola verifica che emette marker), preservando il replay deterministico.
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:146]` + premessa `[DOC-INTERNO CAP_02_parte_II.md:291]`. *Valore*: garantisce che il gate non introduca non-determinismo modificando il tape.

- **CN-9.20** — La soglia `θ_reconcile` è un **parametro provvisorio non congelato**, la cui calibrazione fine è rinviata a FASE-D; nessun valore numerico è fissato qui.
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:131]`. *Valore*: dichiara onestamente che la soglia è ancora da calibrare, senza inventare numeri. *(Dipendenza aperta → Sez.10 / R-10.4, §13.)*

### 9.6 Storicizzazione strutturata del tape (Cap.62)

- **R-9.35** — Il tape DAPI runtime deve confluire in un **archivio canonico locale** con struttura cartelle `exports/directa_history/<TICKER>_<START_YYYYMMDD>_<END_YYYYMMDD>/` (una cartella per ticker per finestra temporale chiusa).
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:184]` + `[CODICE-ESISTENTE export_directa_history_parametric.py]` (pattern di cartella del decoder di riferimento). *Valore*: organizzazione persistente del tape per riconciliazione, replay e bootstrap futuro.

- **R-9.36** — I file CSV dell'archivio devono usare l'header **runtime esteso a 13 campi** (`symbol, timeframe, timestamp, date, time, open, high, low, close, volume, tick_count, bar_synthetic, source`), NON il format legacy a 11 campi.
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:185]`. *Valore*: simmetria con il bundle frozen Portara; coerenza con il format runtime (§9.1.6).

- **R-9.37** — Ogni esecuzione di archiviazione deve produrre un **manifest JSON** con i campi ereditati Cap.48 (`symbol`, `start_date`, `end_date`, `host`, `port_historic`, `account_code` mascherabile, `banner_darwin`, `config_resolved`; per timeframe: `mode`, `rows_received`, `first_timestamp`, `last_timestamp`, `commands_sent`, `warnings`) più le estensioni Parte 10 (`reconcile_status`, `bar_counts_by_source`, `gap_log`, `partial`, `bootstrap_completed_at`).
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:186-188]`. *Valore*: corredo auditabile per il replay deterministico e la tracciabilità della provenienza.

- **CN-9.21** — Il dominio `source` dell'archivio estende quello di Cap.48 con tre nuovi valori (`BACKFILL_FROM_CANDLERANGE`, `BACKFILL_FROM_ARCHIVE`, `BACKFILL_FROM_PORTARA`), come **complemento** (non sostituzione) dei tre valori Cap.48 (`DIRECTA`, `AGG_FROM_60s`, `AGG_FROM_D`).
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:194,196-203]`. *Valore*: traccia la provenienza delle barre ricostruite senza rompere il dominio-base.

- **CN-9.22** — La scrittura dell'archivio deve essere **append-only**: la scrittura di un giorno `d` già archiviato è un no-op se identico; se divergente, apre una nuova versione (`version = N+1` nel manifest), mai sovrascrittura.
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:207]`. *Valore*: immutabilità dell'archivio, condizione per il replay retroattivo.

- **CN-9.23** — La provenienza "barra del flusso nominale vs barra ricostruita via backfill" deve essere catturata interamente dal campo `source`, non dal flag `bar_synthetic`: il bundle frozen ignora `source` nel calcolo delle feature (legge solo OHLCV + `tick_count` + `bar_synthetic`).
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:68]`. *Valore*: preserva l'invariante research=runtime — il motore non distingue una barra live da una ricostruita.

- **CN-9.24** — L'archivio del tape DAPI **NON è fonte di training** del bundle: serve esclusivamente per riconciliazione, replay e bootstrap futuro; l'apertura del flusso DAPI come fonte di training richiederebbe un nuovo task Planner con riesame di Cap.38/Cap.39.
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:209]` + premessa `[DOC-INTERNO CAP_08_parte_8.md Cap.44]`. *Valore*: vincolo negativo hard-locked; tiene separato lo strumento di calibrazione (Portara ratio-adjusted) dal tape runtime archiviato.

### 9.7 Vincoli gap-closure AUDITFIX-01 (encoding e routing backfill)

- **CN-9.25** — Ogni file CSV prodotto dalla pipeline runtime deve avere **header con BOM UTF-8** (encoding del file: UTF-8 con Byte Order Mark).
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:117]` ("Ogni file CSV prodotto dalla pipeline runtime ha header obbligatorio BOM UTF-8 ...") + `[DOC-INTERNO CAP_09_parte_9.md:145]` (lo script di riferimento "definisce ... il header CSV con BOM UTF-8"). *Valore*: il vincolo di encoding è un concern distinto dall'enumerazione dei 13 campi (CN-9.5): fissa la codifica byte del file, garantendo che i consumer downstream leggano l'header correttamente e che il diff byte-per-byte del test di regressione sia stabile rispetto all'encoding.

- **R-9.43** — Nella validazione di idempotenza del backfill `CANDLERANGE`, l'adapter deve marcare l'esito con `BACKFILL_VERIFIED_T3` se la finestra recuperata rientra nell'orizzonte empirico testato (T+3 morning); altrimenti deve marcare `BACKFILL_UNVERIFIED` con flag operativo che **instrada il record al check di riconciliazione di Cap.60** (gate end-of-day).
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:90]` ("Marker di esito: `BACKFILL_VERIFIED_T3` se la finestra rientra nell'orizzonte empirico testato; altrimenti `BACKFILL_UNVERIFIED` con flag operativo che richiede il check di riconciliazione di Cap.60."). *Valore*: separa onestamente il backfill la cui immutabilità è attestata empiricamente in modo diretto (T+3 morning) da quello assunto-per-estensione, instradando quest'ultimo al gate di sorveglianza periodica (Cap.60) invece di trattarlo come dato certo — coerente con il perimetro empirico esplicito di Cap.59 e con la dipendenza aperta Sez.10 / R-10.13.

**Out-of-scope della Sezione 9**:
| Voce | Destinazione |
|---|---|
| Canale DAPI: porte/handshake/sottoscrizione/loopback (Cap.46/47); eventi audit (Cap.54) | **Sez.7** (da B5) — premessa (origine del dato) |
| Preprocessor / back-adjustment Portara, ratio-adjusted, filtro pre-expiry (Cap.40/38/39) | Parte 8 (§12) — premessa |
| State machine / lifecycle del segnale | **Sez.4** (da B3) — premessa |
| Determinismo bit-exact (invariante formale) | premessa `CAP_02 Cap.10` — consolidato come invariante che l'adapter preserva (NFR-9.1..4) |
| Tape come fonte training | fuori scope (vincolo D-10-9; Parte 8 Cap.44 + Parte 9 Cap.55) — consolidato come vincolo negativo CN-9.24 |
| Riavvio Darwin a mezzanotte (Cap.50, infra-giornaliero) | **Sez.7** — premessa (distinto da `RUNTIME_STALE_RESTART` >100gg, in-scope qui R-9.27..29) |

---

## Sezione 10 — Confine / fasizzazione PHASE-1/PHASE-2 & dipendenze aperte verso FASE-D (da B8)

**Valore di prodotto della sezione**: traduce in requisiti di prodotto il **confine** della specifica — cosa il prodotto dichiara come in vigore ora (PHASE-1 FIB-only), cosa dichiara come previsto ma non implementato (PHASE-2 cross-index), e quali dipendenze restano aperte e dove sono rinviate (FASE-D / monitoring post-go-live / Appendice E / ruolo `validator`). Le dipendenze sono **dichiarate aperte, MAI risolte**.

### 10.1 Fasizzazione PHASE-1 / PHASE-2 (Cap.42)

- **R-10.1** — Il prodotto **dichiara** che la PHASE-1 (fase corrente in vigore) è **FIB-only, single-instrument**: la specifica del motore è istanziata esclusivamente sul FIB, senza il layer di covarianza cross-index `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:167]`. La fasizzazione PHASE-1 è **esplicita e dichiarata, non una semplificazione silenziosa** `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:143]`; il documento metodologico v2 è esplicitamente single-instrument FIB, con il preambolo che dichiara la "rimozione dei layer multi-indice (DCC/ADCC/BEKK, covarianza cross-index, N>=8)" `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:145]`.
  - *Valore operativo*: l'operatore retail FIB sa che il prodotto in PHASE-1 produce segnali sul **solo FIB**; non deve aspettarsi segnali o copertura cross-index, che non esistono nella fase corrente.

- **R-10.2** — Il prodotto **dichiara** la convenzione cross-index per gli strumenti correlati al FIB come **dichiarazione normativa PHASE-2 senza implementazione** nel doc v2 corrente; la sua attivazione operativa è **rinviata a un futuro ciclo di estensione**, fuori scope dal corpo del documento corrente `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:143]`. Il layer di covarianza cross-index **non esiste** nel doc v2 corrente: nessun riferimento implementativo è fatto per quel layer `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:145]`.
  - *Valore di sistema*: il confine è chiarito — la convenzione cross-index esiste come **norma scritta**, non come funzione erogata. Chi legge la spec non confonde "dichiarato" con "implementato".

- **CN-10.1** — Il prodotto **dichiara** che gli strumenti previsti per la PHASE-2 sono **DAX** (futures FDAX su Eurex), **EuroStoxx 50** (futures FESX su Eurex) e **S&P 500 mini** (futures ES su CME) `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:147]` (`:149-:151`). Questi strumenti entrano nella specifica **solo come previsione normativa di PHASE-2**: non sono erogati né implementati in PHASE-1 (vincolo di fasizzazione di R-10.1/R-10.2).
  - *Valore di sistema*: enumera con precisione **quali** strumenti la PHASE-2 prevederebbe, senza promettere che il prodotto corrente li tratti.

- **CN-10.2** — Il prodotto **dichiara** come **non implementate** nel doc v2 corrente tre classi di estensione cross-index: i **modelli di covarianza condizionata cross-index** (DCC, ADCC, cDCC); il **Realized GARCH**; lo **score `S_xidx` e la quinta famiglia del catalogo target ("proiezioni cross-index coerenti")** `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:176]` (`:178-:180`). Nessuno di questi tre elementi entra come parte dell'impegno corrente del documento metodologico v2 `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:182]`.
  - *Valore di sistema*: fissa il **confine metodologico** della PHASE-1 — quali tecniche restano fuori dalla fase corrente — evitando che la loro citazione nel capitolo sia letta come impegno implementativo.

- **CN-10.3** — Il prodotto **dichiara** che la fasizzazione PHASE-1 **non sostituisce la specifica ideale, la istanzia in modo parziale con costi noti** `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:174]`. I costi dichiarati della PHASE-1 sono: la varianza sistemica cross-index $\sigma_{sys}$ è **ridotta a** $\sigma_{local}$ (varianza condizionata locale del FIB da EGARCH(1,1)), degradazione metodologica dichiarata `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:169]`; il feature tensor è **privo dei canali cross-index** della specifica ideale (catalogo 37 feature calibrato single-instrument FIB) `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:170]`; lo score $S_{xidx}$ **non è calcolabile** in PHASE-1 e la quinta famiglia del catalogo target è esclusa `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:171]`; il report per regime di volatilità è **privo della riga "Contagio cross-index"** `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:172]`.
  - *Valore di sistema*: rende esplicito **a quale prezzo metodologico** il prodotto eroga la PHASE-1, così che il costo non sia scoperto a posteriori e sia un input consapevole per la valutazione PHASE-2.

- **CN-10.4** — Il prodotto **dichiara** il confine fine tra cash europei e cross-index PHASE-2: i cash europei **DGER, DSTX50, DITAS, DFRA non sono "cross-index PHASE-2"** — sono **canali di contesto live** (logging + gating qualitativo), accessibili gratuitamente sul DAPI base, distinti dai futures cross-index `[DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:338]` (premessa Cap.53, citata per riga). Quando PHASE-2 sarà attivata, i **futures** cross-index (FDAX, FESX, ES) entreranno nel layer di covarianza, mentre i cash europei resteranno gating qualitativo `[DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:338]`.
  - *Valore di sistema*: previene la confusione fra due materie distinte (cash di contesto, già in PHASE-1 come gating qualitativo — Sez.7; futures cross-index, in PHASE-2). Il requisito consolida **solo il confine**; il gating runtime/`gating_rules.yaml` è Sez.7 (R-7.16, CN-7.7..9), non ri-derivato qui.

- **CN-10.5** — Il prodotto **dichiara** che la convenzione tape/storicizzazione runtime (Parte 10) **NON si applica ai cross-index PHASE-2**: la convenzione cross-index Parte 8 Cap.42 è **invariata**, e la Parte 10 resta dentro il confine PHASE-1 (fuori scope i cross-index) `[DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:236]`.
  - *Valore di sistema*: chiude il confine PHASE-1 anche sul versante della pipeline tape/archiviazione, coerente con R-10.1/R-10.2: nessuna parte del prodotto corrente (incluso il ciclo di vita del tape) tratta i cross-index.

### 10.2 Dipendenze aperte verso FASE-D (Cap.55 + Cap.64, premessa Cap.36.3)

> Le dipendenze sono **dichiarate aperte, MAI risolte**: questa sezione consolida l'esistenza, lo stato e la destinazione della dipendenza — fatti del capitolo — non il merito (non calibra, non misura, non sceglie). L'esito/valore di ciascuna è **PENDING-empirico** (§13).

- **R-10.3** `[B-1 PROVVISORIO]` — Il prodotto **dichiara** la verifica empirica della latenza del canale Telegram ($L_{max}=30$s) come **dipendenza aperta** (M-promemoria M-2, `OPEN`), carryover ad **Appendice E** del documento; non si chiude nei capitoli di confine perché tratta il canale di pubblicazione Telegram, fuori perimetro DAPI `[DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:402]`. Lo stesso stato è ribadito sul versante tape: Telegram $L_{max}=30$s (M-2 OPEN), Appendice E, fuori perimetro DAPI `[DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:237]`.
  - *Stato esatto*: **aperta**, rinviata ad **Appendice E** (sessione futura). La **misura empirica** del valore è PENDING-empirico (§13), mai asserita.
  - *Valore di sistema*: rende esplicito che il vincolo di latenza del canale di consegna esiste come dichiarazione, ma il suo valore numerico non è ancora verificato — da chiudere prima/durante FASE-D.

- **R-10.4** — Il prodotto **dichiara** la soglia $\theta_{reconcile}$ (numero massimo di minuti divergenti oltre tolleranza tollerati prima di `RECONCILE_DIVERGENT_FIB`) come **parametro provvisorio non congelato**, la cui calibrazione fine è **rinviata a FASE-D** su dati operativi reali (o a un futuro CAP-DATA-04 / monitoring post-go-live); nessun valore numerico è inventato `[DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:131]`. La voce è ribadita come fuori scope di Parte 10, con carryover a CAP-DATA-04 / monitoring post-go-live `[DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:232]`.
  - *Stato esatto*: **provvisoria, non congelata**, rinviata a **FASE-D / CAP-DATA-04 / monitoring post-go-live**. La calibrazione è PENDING-empirico (§13); nessun valore assegnato.
  - *Valore di sistema*: rende esplicito che il gate di riconciliazione end-of-day dipende da un parametro non ancora fissato, da calibrare su dati reali — input per FASE-D.

- **R-10.5** — Il prodotto **dichiara** i 10 parametri di tuning operativo di Parte VI ($T_{recal,EGARCH}, \theta_B, T_{B,persist}, W_B, W_{prod}, T_{drift,persist}, T_{emit,persist}, \epsilon_p, N_{reg,\min}^{live}, \alpha_{f_5}$) come **starting point con i default proposti** per il primo run di produzione, **senza congelamento empirico** `[DOC-INTERNO docs/methodology_v2/CAP_07_parte_VII.md:637]` (premessa Cap.36.3, citata per riga). La riconsiderazione empirica è attività di **monitoring post-go-live a 3-6 mesi** di produzione live, dichiarata come carryover esplicito e **non** task corrente `[DOC-INTERNO docs/methodology_v2/CAP_07_parte_VII.md:641]`.
  - *Stato esatto*: **aperta** (parametri non congelati empiricamente), rinviata al **monitoring post-go-live (3-6 mesi)**. Il congelamento è PENDING-empirico (§13).
  - *Valore di sistema*: rende esplicito che i parametri operativi del prodotto sono default provvisori da raffinare in produzione, non valori finali — premessa di Sez.8 (CN-8.7), qui citata solo come dipendenza aperta, non ri-derivata.

- **R-10.6** — Il prodotto **dichiara** che l'esito d'edge (es. DSR/PBO/OOS e valori d'esito) è materia del **ruolo `validator`** in FASE-D e resta **dipendenza aperta**: i parametri di tuning provvisori (es. $\theta_{DSR}, \theta_{PBO}$) sono trattati come provvisori non congelati `[DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:131]`, analogamente a $\theta_{reconcile}$ e $L_{max}$ Telegram. Questa sezione **cita** l'edge come dipendenza aperta e **non asserisce alcun esito** (eredità del cardine Sez.8).
  - *Stato esatto*: **aperta**, PENDING-empirico, esclusiva del ruolo `validator` (FASE-D). Nessun valore d'edge è asserito (§13).
  - *Valore di sistema*: rende esplicito che il prodotto **non dichiara** un edge misurato; l'esistenza/misura dell'edge è rinviata al validator, da risolvere in FASE-D prima del go-live.

- **R-10.7** — Il prodotto **dichiara** che la lookup completa dei codici mese Directa-IDEM è una **dipendenza aperta**: nel doc v2 corrente sono congelati solo i due codici verificati (`F = giugno`, `I = settembre`), mentre gli altri restano **lookup runtime-discovery**, da derivare via comando `ANAG` sul gateway per ciascun ticker candidato, con tabella arricchita progressivamente nel **ciclo operativo (FASE-D)** `[DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:389]`.
  - *Stato esatto*: **aperta** (solo 2 codici congelati), rinviata a **runtime-discovery / FASE-D**. La decodifica dei codici mancanti è PENDING-empirico (§13).
  - *Valore di sistema*: rende esplicito che il catalogo dei codici mese non è completo e va completato a mercato aperto — input operativo per FASE-D.

- **R-10.8** — Il prodotto **dichiara** l'abilitazione FDAX standard (DAX Future Eurex, 25 EUR/pt) come **dipendenza aperta fuori scope** per il vincolo D-1 (niente market data a pagamento sui cross-index futures): la verifica empirica 2026-05-27 ha rilevato che l'account `B6086` **non è abilitato** al ticker `FDAX` standard (tutte le varianti hanno restituito `ERR;<sym>;1007`), mentre sono abilitati i ticker Mini-DAX e Micro-DAX; l'abilitazione FDAX standard sarebbe parte della valutazione solo **se in PHASE-2** si decidesse di attivare i futures cross-index `[DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:387]`.
  - *Stato esatto*: **aperta**, rinviata alla valutazione **PHASE-2** (non decisa nel doc corrente). Il dato 2026-05-27 è riportato come **già dichiarato dal capitolo frozen** (PROVA-EMPIRICA del capitolo), non ri-verificato.
  - *Valore di sistema*: rende esplicito che un eventuale futuro uso del DAX richiederebbe un'abilitazione che il prodotto corrente non possiede — confine commerciale di PHASE-2.

- **R-10.9** — Il prodotto **dichiara** la scelta di un **vendor cross-index pluriennale** (necessario per il training cross-index PHASE-2, perché il limite 100 giorni intraday del DAPI è strutturale) come **dipendenza aperta**, con la decisione **rinviata a futuri cicli di estensione (attivazione PHASE-2)** `[DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:391]`.
  - *Stato esatto*: **aperta**, rinviata all'**attivazione PHASE-2**. La scelta del vendor è PENDING (§13 — dipende dall'attivazione PHASE-2).
  - *Valore di sistema*: rende esplicito che il training cross-index della PHASE-2 dipende da una fonte dati pluriennale ancora non scelta — confine dati di PHASE-2.

- **R-10.10** — Il prodotto **dichiara** l'apertura del flusso DAPI come fonte di training come **esplicitamente fuori scope / dipendenza aperta**: il vincolo Parte 8 (FIB Portara/CQG come unica fonte ufficiale di training) è invariato; una eventuale persistenza strutturale del flusso DAPI richiederebbe un **nuovo task Planner** con riesame delle convenzioni di back-adjustment, roll log e filtro pre-expiry `[DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:404]`. Lo stesso confine è ribadito sul versante tape: l'apertura del flusso DAPI come fonte di training è fuori scope e richiederebbe nuovo task Planner `[DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:238]`.
  - *Stato esatto*: **aperta** (esplicitamente fuori scope corrente), rinviata a **nuovo task Planner**. Non risolta qui.
  - *Valore di sistema*: rende esplicito che il tape DAPI archiviato non è (oggi) fonte di training e che cambiarlo è una decisione strutturale futura — confine dati del prodotto.

- **R-10.11** — Il prodotto **dichiara** la migrazione del formato legacy→esteso dei 391 dump live esistenti come **operazione una-tantum di FASE-D, non normata in metodologia**: i dump legacy a 11 campi restano per il test di regressione, i dump nuovi adottano il format esteso a 13 campi `[DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:230]`. La coabitazione legacy/esteso dei sample è dichiarata senza vincolare la scelta architetturale FASE-D `[DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:235]`.
  - *Stato esatto*: **aperta**, rinviata a **FASE-D** (operazione una-tantum, scelta architetturale non vincolata). Non risolta qui.
  - *Valore di sistema*: rende esplicito che la convivenza dei due formati di archivio è un debito di migrazione da chiudere in FASE-D — confine implementativo del ciclo di vita del tape.

- **R-10.12** — Il prodotto **dichiara** che l'**implementazione del codice operativo** della pipeline runtime (parser DAPI realtime/storico, adapter DAPI→bundle frozen, layer di recovery, audit, gating qualitativo) vive in **FASE-D del roadmap**: i capitoli di confine sono **metodologia, non codice** `[DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:406]`. Lo stesso vale per la pipeline di backfill, riconciliazione e archiviazione, rinviata a FASE-D `[DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:231]`.
  - *Stato esatto*: **aperta**, rinviata a **FASE-D**. La codifica non è materia della spec corrente (metodologia/prodotto, non implementazione).
  - *Valore di sistema*: rende esplicito il confine fra specifica (chiusa con la serie B1..B8 e questo assemblato) e implementazione (FASE-D), così che il go-live non sia confuso con la disponibilità di codice eseguibile.

- **R-10.13** — Il prodotto **dichiara** l'estensione del perimetro di immutabilità delle barre `CANDLERANGE` **oltre l'orizzonte T+3** (e oltre la finestra morning / su finestre afternoon e usopen / su strumenti non testati) come **dipendenza aperta**: il perimetro empirico onesto entro cui l'immutabilità è attestata empiricamente in modo diretto è T+3 morning sui ticker FIB6F/DITAS; oltre tale perimetro l'immutabilità è **assunta per estensione, sorvegliata dal gate di riconciliazione (Cap.60)**, e una eventuale estensione **richiede un nuovo probe empirico** (Q-XX al Planner, NON dentro Parte 10), da rifinire con probe addizionale in **FASE-D** se emerge necessità `[DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:234]`.
  - *Stato esatto*: **aperta**, PENDING-empirico, rinviata a **FASE-D** (probe addizionale) / sorvegliata dal gate Cap.60 (Sez.9 / R-9.43, CN-9.18) nel frattempo. L'estensione del perimetro di immutabilità **non è risolta** qui e **non è asserita** come dimostrata oltre T+3 morning.
  - *Valore di sistema*: rende esplicito che la garanzia di idempotenza/immutabilità del backfill `CANDLERANGE` vale solo entro il perimetro empirico testato (T+3 morning, FIB6F/DITAS); fuori da quel perimetro è un'assunzione sorvegliata, non un fatto dimostrato — input per FASE-D prima di affidarvi backfill oltre quell'orizzonte.

**Out-of-scope della Sezione 10**:
| Voce | Destinazione |
|---|---|
| Implementazione PHASE-2 cross-index (layer covarianza, S_xidx, 5ª famiglia, feature cross-index) | spec futura (SPEC-FUNZ-02 o equivalente) — qui solo il confine dichiarato |
| Risoluzione delle dipendenze aperte (misura L_max, calibrazione θ_reconcile, congelamento 10 param, run validator edge, lookup codici mese, abilitazione FDAX, vendor cross-index) | FASE-D / validator / monitoring post-go-live — qui dichiarate aperte |
| Assemblaggio della serie B1..B8 / indicizzazione / avvio FASE-D | task/fasi separate — questo documento è esso stesso l'assemblaggio; l'avvio FASE-D è fase successiva |
| Verdetti d'edge / valori effettivi (DSR/PBO/E[R_net]/OOS) | FASE-D / ruolo `validator` — PENDING-empirico, MAI asserito |
| Materia di Sez.1..9 (gate Cap.36, gating Cap.53, sessione Cap.52, schema-dato) | sezioni rispettive — premessa, non ri-derivare |

---

## Sezione 11 — Matrice di tracciabilità unica + tabella di mapping ID-assemblato ↔ ID-blocco

### 11.1 Matrice di tracciabilità (requisito → capitolo metodologia v2)

La **matrice di tracciabilità puntuale per ogni requisito** vive **in linea** in ogni requisito delle Sezioni 1-10 (campo *Tracciabilità* / *Fonte* con citazione `[DOC-INTERNO CAP_XX:riga]` o `[CODICE-ESISTENTE path:linea]` / `[PROVA-EMPIRICA <data>]`): ogni requisito-assemblato è una riga della matrice, con la propria citazione risolvibile sul CAP frozen. La tabella sotto è la **sintesi per Sezione** che aggrega le 375 righe-per-requisito al capitolo/Parte di origine; è riconciliata 1-a-1 con i requisiti definiti nelle Sez.1-10 (0 mancanti, 0 orfani).

| Sezione | Famiglia ID | Capitolo/Parte metodologia v2 (fonte) | # req |
|---|---|---|---|
| Sez.1 | R-1.* / NFR-1.* / CN-1.* | CAP-01 Parte I (Cap.1-3) | 20 |
| Sez.2 | R-2.* / NFR-2.* / CN-2.* | CAP-01 Parte I (Cap.2-3) | 14 |
| Sez.3 | R-3.* / NFR-3.* / CN-3.* | CAP-02 Parte II (Cap.6) | 42 |
| Sez.4 | R-4.* / NFR-4.* / CN-4.* | CAP-02 Parte II (Cap.7,11) | 63 |
| Sez.5 | R-5.* / NFR-5.* / CN-5.* | CAP-02 Parte II (Cap.8) | 21 |
| Sez.6 | R-6.* / NFR-6.* / CN-6.* | CAP-02 Parte II (Cap.9) + CAP-06 Parte VI (Cap.29) | 40 |
| Sez.7 | R-7.* / NFR-7.* / CN-7.* | CAP-09 Parte 9 (Cap.46,47,52,53,54) + CAP-01 (Cap.1) | 36 |
| Sez.8 | R-8.* / NFR-8.* / CN-8.* | CAP-07 Parte VII (Cap.31-36) + CAP-01 (Cap.5) | 49 |
| Sez.9 | R-9.* / NFR-9.* / CN-9.* | CAP-09 Parte 9 (Cap.48,49,51) + CAP-10 Parte 10 (Cap.59-62) + decoder/PROVA-EMPIRICA + CAP-02 Cap.10 (premessa) | 72 |
| Sez.10 | R-10.* / NFR-10.* / CN-10.* | CAP-08 Parte 8 (Cap.42) + CAP-09 (Cap.55) + CAP-10 (Cap.64) + premesse Cap.36.3/53/41 | 18 |
| **TOTALE** | | | **375** |

> **Nota sul conteggio (375 vs 374)**: il totale reale dei requisiti-assemblato è **375**, non 374. La differenza è interamente in **Sez.7 (da B5) = 36 requisiti** (20 R + 9 CN + 7 NFR = **36**), non 35 come dichiarato nell'aritmetica interna del file-blocco B5 (`SPEC_FUNZ_01_B5.md:281`) e nella task card. Il file B5 elenca tutti e 36 i requisiti (B5-R-01..20, B5-CN-01..09, B5-NFR-01..07) ma ne somma erroneamente 35. Tutti i 36 sono mappati 1-a-1 in Sez.7. L'aritmetica finale è verità di documento (RM-1): l'assemblato è loss-less su **375** requisiti-blocco. Vedi REPORT, sezione discrepanze di conteggio.

### 11.2 Tabella di mapping ID-assemblato ↔ ID-blocco (loss-less, 1-a-1)

Copertura completa dei **375 requisiti-blocco** della serie B1..B8 (B1=34, B2=42, B3=63, B4=61, **B5=36**, B6=72, B7=49, B8=18). Mappatura **1-a-1**, **0 dedup** di premesse (nessun requisito-blocco è collassato: le premesse condivise sono risolte come **riferimenti interni** nel corpo dei requisiti, non come fusione di ID — vedi nota sotto), **0 requisiti persi, 0 inventati**. La citazione CAP di ogni riga è quella in-linea del requisito-assemblato corrispondente (§Sez.1-10).

> **Nota dedup (AC-ASM-3)**: in questo merge **nessuna coppia di requisiti-blocco è stata collassata** in un solo ID-assemblato. Le premesse condivise fra blocchi (es. "state machine & 6 stati terminali" possedute da B3→Sez.4 e usate come premessa in B4/B5/B6; "moltiplicatore 5€/pt" posseduto da B1→Sez.1 e premessa in B5; "contratto messaggio Telegram" posseduto da B4→Sez.6 e premessa in B5; "replay bit-exact CAP_02 Cap.10" premessa in B5/B6/B7) **non sono requisiti atomici duplicati**: ognuna è **un solo requisito** nel blocco che la possiede come materia, e gli altri blocchi la **citano come riferimento interno** (cross-ref risolto, AC-ASM-4). Quindi il numero di ID-assemblato = numero di requisiti-blocco = 375, senza riduzione.

| ID-assemblato | ID-blocco originario | citazione CAP (fonte primaria) |
|---|---|---|
| R-1.1 | B1-R-01 | [DOC-INTERNO CAP_01_parte_I.md:9] |
| R-1.2 | B1-R-02 | [DOC-INTERNO CAP_01_parte_I.md:9] |
| R-1.3 | B1-R-03 | [DOC-INTERNO CAP_01_parte_I.md:9] |
| R-1.4 | B1-R-04 | [DOC-INTERNO CAP_01_parte_I.md:9] |
| R-1.5 | B1-R-05 | [DOC-INTERNO CAP_01_parte_I.md:11] |
| R-1.6 | B1-R-06 | [DOC-INTERNO CAP_01_parte_I.md:11] |
| R-1.7 | B1-R-07 | [DOC-INTERNO CAP_01_parte_I.md:11] |
| R-1.8 | B1-R-08 | [DOC-INTERNO CAP_01_parte_I.md:11] |
| R-1.9 | B1-R-09 | [DOC-INTERNO CAP_01_parte_I.md:11] |
| R-1.10 | B1-R-10 | [DOC-INTERNO CAP_01_parte_I.md:13] |
| R-1.11 | B1-R-11 | [DOC-INTERNO CAP_01_parte_I.md:13] |
| R-1.12 | B1-R-12 | [DOC-INTERNO CAP_01_parte_I.md:13] |
| R-1.13 | B1-R-13 | [DOC-INTERNO CAP_01_parte_I.md:17] |
| R-1.14 | B1-R-14 | [DOC-INTERNO CAP_01_parte_I.md:17] |
| R-1.15 | B1-R-15 | [DOC-INTERNO CAP_01_parte_I.md:17] |
| R-1.16 | B1-R-22 | [DOC-INTERNO CAP_01_parte_I.md:9] |
| NFR-1.1 | B1-NFR-02 | [DOC-INTERNO CAP_01_parte_I.md:27] |
| CN-1.1 | B1-CN-01 | [DOC-INTERNO CAP_01_parte_I.md:15] |
| CN-1.2 | B1-CN-02 | [DOC-INTERNO CAP_01_parte_I.md:15] |
| CN-1.3 | B1-CN-03 | [DOC-INTERNO CAP_01_parte_I.md:15] |
| CN-2.1 | B1-CN-04 | [DOC-INTERNO CAP_01_parte_I.md:23] |
| R-2.1 | B1-R-16 | [DOC-INTERNO CAP_01_parte_I.md:23] |
| R-2.2 | B1-R-17 | [DOC-INTERNO CAP_01_parte_I.md:23] |
| NFR-2.1 | B1-NFR-01 | [DOC-INTERNO CAP_01_parte_I.md:23] |
| R-2.3 | B1-R-18 | [DOC-INTERNO CAP_01_parte_I.md:25] |
| CN-2.2 | B1-CN-05 | [DOC-INTERNO CAP_01_parte_I.md:25] |
| R-2.4 | B1-R-19 | [DOC-INTERNO CAP_01_parte_I.md:25] |
| R-2.5 | B1-R-20 | [DOC-INTERNO CAP_01_parte_I.md:31] |
| R-2.6 | B1-R-21 | [DOC-INTERNO CAP_01_parte_I.md:33] |
| NFR-2.2 | B1-NFR-03 | [DOC-INTERNO CAP_01_parte_I.md:39] |
| NFR-2.3 | B1-NFR-04 | [DOC-INTERNO CAP_01_parte_I.md:41] |
| R-2.7 | B1-R-23 | [DOC-INTERNO CAP_01_parte_I.md:43] |
| R-2.8 | B1-R-24 | [DOC-INTERNO CAP_01_parte_I.md:45] |
| R-2.9 | B1-R-25 | [DOC-INTERNO CAP_01_parte_I.md:47] |
| R-3.1 | B2-R-01 | [DOC-INTERNO CAP_02_parte_II.md:17, :19] |
| R-3.2 | B2-R-02 | [DOC-INTERNO CAP_02_parte_II.md:23] |
| R-3.3 | B2-R-03 | [DOC-INTERNO CAP_02_parte_II.md:23] |
| R-3.4 | B2-R-04 | [DOC-INTERNO CAP_02_parte_II.md:23] |
| R-3.5 | B2-R-05 | [DOC-INTERNO CAP_02_parte_II.md:25] |
| R-3.6 | B2-R-06 | [DOC-INTERNO CAP_02_parte_II.md:25] |
| R-3.7 | B2-R-07 | [DOC-INTERNO CAP_02_parte_II.md:27] |
| R-3.8 | B2-R-08 | [DOC-INTERNO CAP_02_parte_II.md:29, :31] |
| R-3.9 | B2-R-09 | [DOC-INTERNO CAP_02_parte_II.md:33] |
| R-3.10 | B2-R-10 | [DOC-INTERNO CAP_02_parte_II.md:35] |
| R-3.11 | B2-R-11 | [DOC-INTERNO CAP_02_parte_II.md:35] |
| R-3.12 | B2-R-12 | [DOC-INTERNO CAP_02_parte_II.md:35] |
| R-3.13 | B2-R-13 | [DOC-INTERNO CAP_02_parte_II.md:35] |
| R-3.14 | B2-R-14 | [DOC-INTERNO CAP_02_parte_II.md:35] |
| R-3.15 | B2-R-15 | [DOC-INTERNO CAP_02_parte_II.md:35] |
| R-3.16 | B2-R-16 | [DOC-INTERNO CAP_02_parte_II.md:35] |
| R-3.17 | B2-R-17 | [DOC-INTERNO CAP_02_parte_II.md:35] |
| R-3.18 | B2-R-18 | [DOC-INTERNO CAP_02_parte_II.md:35] |
| R-3.19 | B2-R-19 | [DOC-INTERNO CAP_02_parte_II.md:35] |
| R-3.20 | B2-R-20 | [DOC-INTERNO CAP_02_parte_II.md:37] |
| R-3.21 | B2-R-21 | [DOC-INTERNO CAP_02_parte_II.md:39] |
| R-3.22 | B2-R-22 | [DOC-INTERNO CAP_02_parte_II.md:39] |
| R-3.23 | B2-R-23 | [DOC-INTERNO CAP_02_parte_II.md:41] |
| R-3.24 | B2-R-24 | [DOC-INTERNO CAP_02_parte_II.md:43] |
| R-3.25 | B2-R-25 | [DOC-INTERNO CAP_02_parte_II.md:51] |
| R-3.26 | B2-R-26 | [DOC-INTERNO CAP_02_parte_II.md:51] |
| R-3.27 | B2-R-27 | [DOC-INTERNO CAP_02_parte_II.md:51] |
| R-3.28 | B2-R-28 | [DOC-INTERNO CAP_02_parte_II.md:53] |
| R-3.29 | B2-R-29 | [DOC-INTERNO CAP_02_parte_II.md:53, :55, :59] |
| R-3.30 | B2-R-30 | [DOC-INTERNO CAP_02_parte_II.md:63] |
| R-3.31 | B2-R-31 | [DOC-INTERNO CAP_02_parte_II.md:69] |
| R-3.32 | B2-R-32 | [DOC-INTERNO CAP_02_parte_II.md:33] |
| R-3.33 | B2-R-33 | [DOC-INTERNO CAP_02_parte_II.md:9, :33] |
| R-3.34 | B2-R-34 | [DOC-INTERNO CAP_02_parte_II.md:9, :33] |
| R-3.35 | B2-R-35 | [DOC-INTERNO CAP_02_parte_II.md:29, :31] |
| R-3.36 | B2-R-36 | [DOC-INTERNO CAP_02_parte_II.md:33] |
| R-3.37 | B2-R-37 | [DOC-INTERNO CAP_02_parte_II.md:33] |
| CN-3.1 | B2-CN-01 | [DOC-INTERNO CAP_02_parte_II.md:47, :49] |
| CN-3.2 | B2-CN-02 | [DOC-INTERNO CAP_02_parte_II.md:73] |
| CN-3.3 | B2-CN-03 | [DOC-INTERNO CAP_02_parte_II.md:73] |
| CN-3.4 | B2-CN-04 | [DOC-INTERNO CAP_02_parte_II.md:79, :81] |
| CN-3.5 | B2-CN-05 | [DOC-INTERNO CAP_02_parte_II.md:77, :83] |
| R-4.1 | B3-R-01 | [DOC-INTERNO CAP_02_parte_II.md:95] |
| R-4.2 | B3-R-02 | [DOC-INTERNO CAP_02_parte_II.md:7] |
| R-4.3 | B3-R-03 | [DOC-INTERNO CAP_02_parte_II.md:97] |
| R-4.4 | B3-R-04 | [DOC-INTERNO CAP_02_parte_II.md:97] |
| R-4.5 | B3-R-05 | [DOC-INTERNO CAP_02_parte_II.md:101] |
| R-4.6 | B3-R-06 | [DOC-INTERNO CAP_02_parte_II.md:101] |
| R-4.7 | B3-R-07 | [DOC-INTERNO CAP_02_parte_II.md:101] |
| R-4.8 | B3-R-08 | [DOC-INTERNO CAP_02_parte_II.md:103] |
| R-4.9 | B3-R-09 | [DOC-INTERNO CAP_02_parte_II.md:105] |
| R-4.10 | B3-R-10 | [DOC-INTERNO CAP_02_parte_II.md:105] |
| R-4.11 | B3-R-11 | [DOC-INTERNO CAP_02_parte_II.md:107] |
| R-4.12 | B3-R-12 | [DOC-INTERNO CAP_02_parte_II.md:107] |
| R-4.13 | B3-R-13 | [DOC-INTERNO CAP_02_parte_II.md:109] |
| R-4.14 | B3-R-14 | [DOC-INTERNO CAP_02_parte_II.md:109] |
| R-4.15 | B3-R-15 | [DOC-INTERNO CAP_02_parte_II.md:111] |
| R-4.16 | B3-R-16 | [DOC-INTERNO CAP_02_parte_II.md:111] |
| R-4.17 | B3-R-17 | [DOC-INTERNO CAP_02_parte_II.md:121] |
| R-4.18 | B3-R-18 | [DOC-INTERNO CAP_02_parte_II.md:122] |
| R-4.19 | B3-R-19 | [DOC-INTERNO CAP_02_parte_II.md:123] |
| R-4.20 | B3-R-20 | [DOC-INTERNO CAP_02_parte_II.md:124] |
| R-4.21 | B3-R-21 | [DOC-INTERNO CAP_02_parte_II.md:125] |
| R-4.22 | B3-R-22 | [DOC-INTERNO CAP_02_parte_II.md:126] |
| R-4.23 | B3-R-23 | [DOC-INTERNO CAP_02_parte_II.md:127] |
| R-4.24 | B3-R-24 | [DOC-INTERNO CAP_02_parte_II.md:135] |
| R-4.25 | B3-R-25 | [DOC-INTERNO CAP_02_parte_II.md:135] |
| R-4.26 | B3-R-26 | [DOC-INTERNO CAP_02_parte_II.md:137] |
| R-4.27 | B3-R-27 | [DOC-INTERNO CAP_02_parte_II.md:137] |
| R-4.28 | B3-R-28 | [DOC-INTERNO CAP_02_parte_II.md:139] |
| R-4.29 | B3-R-29 | [DOC-INTERNO CAP_02_parte_II.md:145] |
| R-4.30 | B3-R-30 | [DOC-INTERNO CAP_02_parte_II.md:147] |
| R-4.31 | B3-R-31 | [DOC-INTERNO CAP_02_parte_II.md:149] |
| R-4.32 | B3-R-32 | [DOC-INTERNO CAP_02_parte_II.md:155] |
| R-4.33 | B3-R-33 | [DOC-INTERNO CAP_02_parte_II.md:157] |
| R-4.34 | B3-R-34 | [DOC-INTERNO CAP_02_parte_II.md:157] |
| R-4.35 | B3-R-35 | [DOC-INTERNO CAP_02_parte_II.md:159] |
| R-4.36 | B3-R-36 | [DOC-INTERNO CAP_02_parte_II.md:163] |
| R-4.37 | B3-R-37 | [DOC-INTERNO CAP_02_parte_II.md:163] |
| R-4.38 | B3-R-38 | [DOC-INTERNO CAP_02_parte_II.md:165] |
| R-4.39 | B3-R-39 | [DOC-INTERNO CAP_02_parte_II.md:167] |
| R-4.40 | B3-R-40 | [DOC-INTERNO CAP_02_parte_II.md:362] |
| R-4.41 | B3-R-41 | [DOC-INTERNO CAP_02_parte_II.md:368] |
| R-4.42 | B3-R-42 | [DOC-INTERNO CAP_02_parte_II.md:370] |
| R-4.43 | B3-R-43 | [DOC-INTERNO CAP_02_parte_II.md:381] |
| R-4.44 | B3-R-44 | [DOC-INTERNO CAP_02_parte_II.md:383] |
| R-4.45 | B3-R-45 | [DOC-INTERNO CAP_02_parte_II.md:385] |
| R-4.46 | B3-R-46 | [DOC-INTERNO CAP_02_parte_II.md:391] |
| R-4.47 | B3-R-47 | [DOC-INTERNO CAP_02_parte_II.md:399] |
| R-4.48 | B3-R-48 | [DOC-INTERNO CAP_02_parte_II.md:411] |
| CN-4.1 | B3-CN-01 | [DOC-INTERNO CAP_02_parte_II.md:105] |
| CN-4.2 | B3-CN-02 | [DOC-INTERNO CAP_02_parte_II.md:99] |
| CN-4.3 | B3-CN-03 | [DOC-INTERNO CAP_02_parte_II.md:113] |
| CN-4.4 | B3-CN-04 | [DOC-INTERNO CAP_02_parte_II.md:129] |
| CN-4.5 | B3-CN-05 | [DOC-INTERNO CAP_02_parte_II.md:131] |
| CN-4.6 | B3-CN-06 | [DOC-INTERNO CAP_02_parte_II.md:139] |
| CN-4.7 | B3-CN-07 | [DOC-INTERNO CAP_02_parte_II.md:349] |
| CN-4.8 | B3-CN-08 | [DOC-INTERNO CAP_02_parte_II.md:386] |
| CN-4.9 | B3-CN-09 | [DOC-INTERNO CAP_02_parte_II.md:393] |
| CN-4.10 | B3-CN-10 | [DOC-INTERNO CAP_02_parte_II.md:397] |
| CN-4.11 | B3-CN-11 | [DOC-INTERNO CAP_02_parte_II.md:113] |
| CN-4.12 | B3-CN-12 | [DOC-INTERNO CAP_02_parte_II.md:393] |
| NFR-4.1 | B3-NFR-01 | [DOC-INTERNO CAP_02_parte_II.md:171] |
| NFR-4.2 | B3-NFR-02 | [DOC-INTERNO CAP_02_parte_II.md:173] |
| NFR-4.3 | B3-NFR-03 | [DOC-INTERNO CAP_02_parte_II.md:175] |
| R-5.1 | B4-R-01 | [DOC-INTERNO CAP_02_parte_II.md:183] |
| CN-5.1 | B4-CN-01 | [DOC-INTERNO CAP_02_parte_II.md:183] |
| R-5.2 | B4-R-02 | [DOC-INTERNO CAP_02_parte_II.md:185] |
| R-5.3 | B4-R-03 | [DOC-INTERNO CAP_02_parte_II.md:185] |
| R-5.4 | B4-R-04 | [DOC-INTERNO CAP_02_parte_II.md:185] |
| R-5.5 | B4-R-05 | [DOC-INTERNO CAP_02_parte_II.md:185] |
| R-5.6 | B4-R-06 | [DOC-INTERNO CAP_02_parte_II.md:191] |
| R-5.7 | B4-R-07 | [DOC-INTERNO CAP_02_parte_II.md:197] |
| R-5.8 | B4-R-08 | [DOC-INTERNO CAP_02_parte_II.md:203] |
| R-5.9 | B4-R-09 | [DOC-INTERNO CAP_02_parte_II.md:209] |
| CN-5.2 | B4-CN-02 | [DOC-INTERNO CAP_02_parte_II.md:209] |
| CN-5.3 | B4-CN-03 | [DOC-INTERNO CAP_02_parte_II.md:211] |
| R-5.10 | B4-R-10 | [DOC-INTERNO CAP_02_parte_II.md:215] |
| CN-5.4 | B4-CN-04 | [DOC-INTERNO CAP_02_parte_II.md:219] |
| R-5.11 | B4-R-11 | [DOC-INTERNO CAP_02_parte_II.md:219] |
| R-5.12 | B4-R-12 | [DOC-INTERNO CAP_02_parte_II.md:219] |
| R-5.13 | B4-R-13 | [DOC-INTERNO CAP_02_parte_II.md:219] |
| R-5.14 | B4-R-14 | [DOC-INTERNO CAP_02_parte_II.md:219] |
| CN-5.5 | B4-CN-05 | [DOC-INTERNO CAP_02_parte_II.md:225] |
| R-5.15 | B4-R-15 | [DOC-INTERNO CAP_02_parte_II.md:225] |
| R-5.16 | B4-R-16 | [DOC-INTERNO CAP_02_parte_II.md:227] |
| NFR-6.1 | B4-NFR-01 | [DOC-INTERNO CAP_02_parte_II.md:235] |
| NFR-6.2 | B4-NFR-02 | [DOC-INTERNO CAP_02_parte_II.md:235] |
| CN-6.1 | B4-CN-06 | [DOC-INTERNO CAP_02_parte_II.md:241] |
| R-6.1 | B4-R-17 | [DOC-INTERNO CAP_02_parte_II.md:243] |
| R-6.2 | B4-R-18 | [DOC-INTERNO CAP_02_parte_II.md:244] |
| R-6.3 | B4-R-19 | [DOC-INTERNO CAP_02_parte_II.md:245] |
| R-6.4 | B4-R-20 | [DOC-INTERNO CAP_02_parte_II.md:246] |
| R-6.5 | B4-R-21 | [DOC-INTERNO CAP_02_parte_II.md:247] |
| R-6.6 | B4-R-22 | [DOC-INTERNO CAP_02_parte_II.md:248] |
| R-6.7 | B4-R-23 | [DOC-INTERNO CAP_02_parte_II.md:249] |
| R-6.8 | B4-R-24 | [DOC-INTERNO CAP_02_parte_II.md:250] |
| R-6.9 | B4-R-25 | [DOC-INTERNO CAP_02_parte_II.md:251] |
| CN-6.2 | B4-CN-07 | [DOC-INTERNO CAP_02_parte_II.md:253] |
| R-6.10 | B4-R-26 | [DOC-INTERNO CAP_02_parte_II.md:253] |
| CN-6.3 | B4-CN-08 | [DOC-INTERNO CAP_02_parte_II.md:253] |
| NFR-6.3 | B4-NFR-03 | [DOC-INTERNO CAP_02_parte_II.md:257] |
| NFR-6.4 | B4-NFR-04 | [DOC-INTERNO CAP_02_parte_II.md:261] |
| CN-6.4 | B4-CN-09 | [DOC-INTERNO CAP_02_parte_II.md:265] |
| CN-6.5 | B4-CN-10 | [DOC-INTERNO CAP_02_parte_II.md:265] |
| R-6.11 | B4-R-27 | [DOC-INTERNO CAP_02_parte_II.md:269] |
| CN-6.6 | B4-CN-11 | [DOC-INTERNO CAP_02_parte_II.md:269] |
| R-6.12 | B4-R-28 | [DOC-INTERNO CAP_02_parte_II.md:271] |
| CN-6.7 | B4-CN-12 | [DOC-INTERNO CAP_02_parte_II.md:271] |
| R-6.13 | B4-R-29 | [DOC-INTERNO CAP_02_parte_II.md:275] |
| R-6.14 | B4-R-30 | [DOC-INTERNO CAP_02_parte_II.md:277] |
| R-6.15 | B4-R-31 | [DOC-INTERNO CAP_02_parte_II.md:278] |
| R-6.16 | B4-R-32 | [DOC-INTERNO CAP_02_parte_II.md:279] |
| CN-6.8 | B4-CN-13 | [DOC-INTERNO CAP_02_parte_II.md:279] |
| CN-6.9 | B4-CN-14 | [DOC-INTERNO CAP_02_parte_II.md:281] |
| NFR-6.5 | B4-NFR-05 | [DOC-INTERNO CAP_06_parte_VI.md:146] |
| NFR-6.6 | B4-NFR-06 | [DOC-INTERNO CAP_06_parte_VI.md:146] |
| NFR-6.7 | B4-NFR-07 | [DOC-INTERNO CAP_06_parte_VI.md:152] |
| R-6.17 | B4-R-33 | [DOC-INTERNO CAP_06_parte_VI.md:220] |
| R-6.18 | B4-R-35 | [DOC-INTERNO CAP_06_parte_VI.md:220] |
| R-6.19 | B4-R-36 | [DOC-INTERNO CAP_06_parte_VI.md:220] |
| R-6.20 | B4-R-37 | [DOC-INTERNO CAP_06_parte_VI.md:192] |
| R-6.21 | B4-R-38 | [DOC-INTERNO CAP_06_parte_VI.md:220] |
| R-6.22 | B4-R-39 | [DOC-INTERNO CAP_06_parte_VI.md:230] |
| R-6.23 | B4-R-40 | [DOC-INTERNO CAP_06_parte_VI.md:232] |
| R-6.24 | B4-R-34 | [DOC-INTERNO CAP_06_parte_VI.md:220] |
| R-7.1 | B5-R-01 | [DOC-INTERNO CAP_09_parte_9.md:27] |
| R-7.2 | B5-R-02 | [DOC-INTERNO CAP_09_parte_9.md:35] |
| R-7.3 | B5-R-03 | [DOC-INTERNO CAP_09_parte_9.md:37] |
| R-7.4 | B5-R-04 | [DOC-INTERNO CAP_09_parte_9.md:29] |
| R-7.5 | B5-R-05 | [DOC-INTERNO CAP_09_parte_9.md:75] |
| R-7.6 | B5-R-06 | [DOC-INTERNO CAP_09_parte_9.md:96] |
| R-7.7 | B5-R-07 | [DOC-INTERNO CAP_09_parte_9.md:61] |
| R-7.8 | B5-R-08 | [DOC-INTERNO CAP_09_parte_9.md:98] |
| R-7.9 | B5-R-09 | [DOC-INTERNO CAP_09_parte_9.md:103] |
| R-7.10 | B5-R-10 | [DOC-INTERNO CAP_09_parte_9.md:75] |
| R-7.11 | B5-R-11 | [DOC-INTERNO CAP_09_parte_9.md:273] |
| R-7.12 | B5-R-12 | [DOC-INTERNO CAP_09_parte_9.md:273] |
| R-7.13 | B5-R-13 | [DOC-INTERNO CAP_09_parte_9.md:294] |
| R-7.14 | B5-R-14 | [DOC-INTERNO CAP_09_parte_9.md:302] |
| R-7.15 | B5-R-15 | [DOC-INTERNO CAP_09_parte_9.md:310] |
| R-7.16 | B5-R-16 | [DOC-INTERNO CAP_09_parte_9.md:311] |
| R-7.17 | B5-R-17 | [DOC-INTERNO CAP_09_parte_9.md:325] |
| R-7.18 | B5-R-18 | [DOC-INTERNO CAP_09_parte_9.md:353] |
| R-7.19 | B5-R-19 | [DOC-INTERNO CAP_09_parte_9.md:353] |
| R-7.20 | B5-R-20 | [DOC-INTERNO CAP_09_parte_9.md:355] |
| CN-7.1 | B5-CN-01 | [DOC-INTERNO CAP_09_parte_9.md:39] |
| CN-7.2 | B5-CN-02 | [DOC-INTERNO CAP_09_parte_9.md:45] |
| CN-7.3 | B5-CN-03 | [DOC-INTERNO CAP_09_parte_9.md:47] |
| CN-7.4 | B5-CN-04 | [DOC-INTERNO CAP_09_parte_9.md:107] |
| CN-7.5 | B5-CN-05 | [DOC-INTERNO CAP_09_parte_9.md:292] |
| CN-7.6 | B5-CN-06 | [DOC-INTERNO CAP_09_parte_9.md:292] |
| CN-7.7 | B5-CN-07 | [DOC-INTERNO CAP_09_parte_9.md:311] |
| CN-7.8 | B5-CN-08 | [DOC-INTERNO CAP_09_parte_9.md:315] |
| CN-7.9 | B5-CN-09 | [DOC-INTERNO CAP_09_parte_9.md:328] |
| NFR-7.1 | B5-NFR-01 | [DOC-INTERNO CAP_09_parte_9.md:41,43] |
| NFR-7.2 | B5-NFR-02 | [DOC-INTERNO CAP_09_parte_9.md:311] |
| NFR-7.3 | B5-NFR-03 | [DOC-INTERNO CAP_09_parte_9.md:360] |
| NFR-7.4 | B5-NFR-04 | [DOC-INTERNO CAP_09_parte_9.md:357] |
| NFR-7.5 | B5-NFR-05 | [DOC-INTERNO CAP_09_parte_9.md:364] |
| NFR-7.6 | B5-NFR-06 | [DOC-INTERNO CAP_09_parte_9.md:365] |
| NFR-7.7 | B5-NFR-07 | [DOC-INTERNO CAP_09_parte_9.md:373] |
| R-8.1 | B7-R-01 | [DOC-INTERNO CAP_01_parte_I.md:71] |
| R-8.2 | B7-R-02 | [DOC-INTERNO CAP_01_parte_I.md:73-75] |
| R-8.3 | B7-R-03 | [DOC-INTERNO CAP_01_parte_I.md:77] |
| R-8.4 | B7-R-04 | [DOC-INTERNO CAP_01_parte_I.md:79] |
| R-8.5 | B7-R-05 | [DOC-INTERNO CAP_01_parte_I.md:81] |
| R-8.6 | B7-R-06 | [DOC-INTERNO CAP_01_parte_I.md:85] |
| R-8.7 | B7-R-07 | [DOC-INTERNO CAP_07_parte_VII.md:15-19] |
| R-8.8 | B7-R-08 | [DOC-INTERNO CAP_07_parte_VII.md:29] |
| R-8.9 | B7-R-09 | [DOC-INTERNO CAP_07_parte_VII.md:31] |
| R-8.10 | B7-R-10 | [DOC-INTERNO CAP_07_parte_VII.md:33] |
| R-8.11 | B7-R-11 | [DOC-INTERNO CAP_07_parte_VII.md:35] |
| R-8.12 | B7-R-12 | [DOC-INTERNO CAP_07_parte_VII.md:37] |
| R-8.13 | B7-R-13 | [DOC-INTERNO CAP_07_parte_VII.md:39] |
| R-8.14 | B7-R-14 | [DOC-INTERNO CAP_07_parte_VII.md:41] |
| R-8.15 | B7-R-15 | [DOC-INTERNO CAP_07_parte_VII.md:50] |
| R-8.16 | B7-R-16 | [DOC-INTERNO CAP_07_parte_VII.md:139] |
| R-8.17 | B7-R-17 | [DOC-INTERNO CAP_07_parte_VII.md:202] |
| R-8.18 | B7-R-18 | [DOC-INTERNO CAP_07_parte_VII.md:252] |
| R-8.19 | B7-R-19 | [DOC-INTERNO CAP_07_parte_VII.md:294-298] |
| R-8.20 | B7-R-20 | [DOC-INTERNO CAP_07_parte_VII.md:304] |
| R-8.21 | B7-R-21 | [DOC-INTERNO CAP_07_parte_VII.md:352] |
| R-8.22 | B7-R-22 | [DOC-INTERNO CAP_07_parte_VII.md:359] |
| R-8.23 | B7-R-23 | [DOC-INTERNO CAP_07_parte_VII.md:369] |
| R-8.24 | B7-R-24 | [DOC-INTERNO CAP_07_parte_VII.md:523] |
| R-8.25 | B7-R-25 | [DOC-INTERNO CAP_07_parte_VII.md:570] |
| R-8.26 | B7-R-26 | [DOC-INTERNO CAP_07_parte_VII.md:574] |
| R-8.27 | B7-R-27 | [DOC-INTERNO CAP_07_parte_VII.md:572] |
| R-8.28 | B7-R-28 | [DOC-INTERNO CAP_07_parte_VII.md:576] |
| R-8.29 | B7-R-29 | [DOC-INTERNO CAP_07_parte_VII.md:578] |
| R-8.30 | B7-R-30 | [DOC-INTERNO CAP_07_parte_VII.md:580] |
| R-8.31 | B7-R-31 | [DOC-INTERNO CAP_07_parte_VII.md:582] |
| R-8.32 | B7-R-32 | [DOC-INTERNO CAP_07_parte_VII.md:584] |
| R-8.33 | B7-R-33 | [DOC-INTERNO CAP_07_parte_VII.md:586] |
| R-8.34 | B7-R-34 | [DOC-INTERNO CAP_07_parte_VII.md:588] |
| R-8.35 | B7-R-35 | [DOC-INTERNO CAP_07_parte_VII.md:594] |
| R-8.36 | B7-R-36 | [DOC-INTERNO CAP_07_parte_VII.md:599] |
| R-8.37 | B7-R-37 | [DOC-INTERNO CAP_07_parte_VII.md:633] |
| R-8.38 | B7-R-38 | [DOC-INTERNO CAP_07_parte_VII.md:645] |
| CN-8.1 | B7-CN-01 | [DOC-INTERNO CAP_01_parte_I.md:69] |
| CN-8.2 | B7-CN-02 | [DOC-INTERNO CAP_07_parte_VII.md:21] |
| CN-8.3 | B7-CN-03 | [DOC-INTERNO CAP_07_parte_VII.md:457] |
| CN-8.4 | B7-CN-04 | [DOC-INTERNO CAP_07_parte_VII.md:506] |
| CN-8.5 | B7-CN-05 | [DOC-INTERNO CAP_07_parte_VII.md:512-517] |
| CN-8.6 | B7-CN-06 | [DOC-INTERNO CAP_07_parte_VII.md:601] |
| CN-8.7 | B7-CN-07 | [DOC-INTERNO CAP_07_parte_VII.md:637] |
| NFR-8.1 | B7-NFR-01 | [DOC-INTERNO CAP_07_parte_VII.md:21] |
| NFR-8.2 | B7-NFR-02 | [DOC-INTERNO CAP_07_parte_VII.md:445] |
| NFR-8.3 | B7-NFR-03 | [DOC-INTERNO CAP_07_parte_VII.md:23] |
| NFR-8.4 | B7-NFR-04 | [DOC-INTERNO CAP_07_parte_VII.md:439] |
| R-9.1 | B6-R-01 | [DOC-INTERNO CAP_09_parte_9.md:153] |
| R-9.2 | B6-R-02 | [DOC-INTERNO CAP_09_parte_9.md:191] |
| R-9.3 | B6-R-03 | [DOC-INTERNO CAP_09_parte_9.md:127] |
| R-9.4 | B6-R-04 | [CODICE-ESISTENTE export_directa_history_parametric.py:477-481] |
| R-9.5 | B6-R-05 | [CODICE-ESISTENTE export_directa_history_parametric.py:481] |
| R-9.6 | B6-R-06 | [CODICE-ESISTENTE export_directa_history_parametric.py:480] |
| R-9.7 | B6-R-07 | [CODICE-ESISTENTE export_directa_history_parametric.py:479] |
| R-9.8 | B6-R-08 | [CODICE-ESISTENTE export_directa_history_parametric.py:478] |
| R-9.9 | B6-R-09 | [CODICE-ESISTENTE export_directa_history_parametric.py:471,482] |
| R-9.10 | B6-R-10 | [CODICE-ESISTENTE export_directa_history_parametric.py:471] |
| R-9.11 | B6-R-11 | [DOC-INTERNO CAP_09_parte_9.md:172] |
| R-9.12 | B6-R-12 | [CODICE-ESISTENTE export_directa_history_parametric.py:471] |
| R-9.13 | B6-R-13 | [DOC-INTERNO CAP_09_parte_9.md:173,177] |
| R-9.14 | B6-R-14 | [DOC-INTERNO CAP_09_parte_9.md:173,178] |
| R-9.15 | B6-R-15 | [DOC-INTERNO CAP_09_parte_9.md:173,179] |
| R-9.16 | B6-R-16 | [PROVA-EMPIRICA 2026-06-01 W2] |
| R-9.17 | B6-R-17 | [DOC-INTERNO CAP_10_parte_10.md:123] |
| R-9.18 | B6-R-18 | [PROVA-EMPIRICA 2026-06-01 W3] |
| R-9.19 | B6-R-19 | [PROVA-EMPIRICA 2026-06-01 W3] |
| R-9.20 | B6-R-20 | [PROVA-EMPIRICA 2026-06-01 W3] |
| R-9.21 | B6-R-21 | [DOC-INTERNO CAP_09_parte_9.md:173] |
| R-9.22 | B6-R-22 | [DOC-INTERNO CAP_09_parte_9.md:254] |
| R-9.23 | B6-R-23 | [DOC-INTERNO CAP_09_parte_9.md:257] |
| R-9.24 | B6-R-24 | [DOC-INTERNO CAP_10_parte_10.md:88] |
| R-9.25 | B6-R-25 | [DOC-INTERNO CAP_10_parte_10.md:91] |
| R-9.26 | B6-R-26 | [DOC-INTERNO CAP_10_parte_10.md:90] |
| R-9.27 | B6-R-27 | [DOC-INTERNO CAP_10_parte_10.md:157-158] |
| R-9.28 | B6-R-28 | [DOC-INTERNO CAP_10_parte_10.md:158-161] |
| R-9.29 | B6-R-29 | [DOC-INTERNO CAP_10_parte_10.md:162] |
| R-9.30 | B6-R-30 | [DOC-INTERNO CAP_10_parte_10.md:119] |
| R-9.31 | B6-R-31 | [DOC-INTERNO CAP_10_parte_10.md:121] |
| R-9.32 | B6-R-32 | [DOC-INTERNO CAP_10_parte_10.md:122] |
| R-9.33 | B6-R-33 | [DOC-INTERNO CAP_10_parte_10.md:123] |
| R-9.34 | B6-R-34 | [DOC-INTERNO CAP_10_parte_10.md:124-127] |
| R-9.35 | B6-R-35 | [DOC-INTERNO CAP_10_parte_10.md:184] |
| R-9.36 | B6-R-36 | [DOC-INTERNO CAP_10_parte_10.md:185] |
| R-9.37 | B6-R-37 | [DOC-INTERNO CAP_10_parte_10.md:186-188] |
| R-9.38 | B6-R-38 | [DOC-INTERNO CAP_09_parte_9.md:185] |
| R-9.39 | B6-R-39 | [DOC-INTERNO CAP_09_parte_9.md:186] |
| R-9.40 | B6-R-40 | [DOC-INTERNO CAP_09_parte_9.md:187] |
| R-9.41 | B6-R-41 | [DOC-INTERNO CAP_09_parte_9.md:188] |
| R-9.42 | B6-R-42 | [DOC-INTERNO CAP_09_parte_9.md:189] |
| R-9.43 | B6-R-43 | [DOC-INTERNO CAP_10_parte_10.md:90] |
| CN-9.1 | B6-CN-01 | [DOC-INTERNO CAP_09_parte_9.md:172] |
| CN-9.2 | B6-CN-02 | [DOC-INTERNO CAP_09_parte_9.md:173] |
| CN-9.3 | B6-CN-03 | [DOC-INTERNO CAP_09_parte_9.md:172-173,177-179] |
| CN-9.4 | B6-CN-04 | [DOC-INTERNO CAP_10_parte_10.md:123] |
| CN-9.5 | B6-CN-05 | [DOC-INTERNO CAP_09_parte_9.md:117,120] |
| CN-9.6 | B6-CN-06 | [DOC-INTERNO CAP_09_parte_9.md:129] |
| CN-9.7 | B6-CN-07 | [DOC-INTERNO CAP_09_parte_9.md:117] |
| CN-9.8 | B6-CN-08 | [DOC-INTERNO CAP_09_parte_9.md:131-138] |
| CN-9.9 | B6-CN-09 | [DOC-INTERNO CAP_09_parte_9.md:125] |
| CN-9.10 | B6-CN-10 | [DOC-INTERNO CAP_09_parte_9.md:254] |
| CN-9.11 | B6-CN-11 | [DOC-INTERNO CAP_09_parte_9.md:256] |
| CN-9.12 | B6-CN-12 | [DOC-INTERNO CAP_10_parte_10.md:79-83] |
| CN-9.13 | B6-CN-13 | [DOC-INTERNO CAP_10_parte_10.md:98] |
| CN-9.14 | B6-CN-14 | [DOC-INTERNO CAP_10_parte_10.md:168-170] |
| CN-9.15 | B6-CN-15 | [DOC-INTERNO CAP_10_parte_10.md:163-164] |
| CN-9.16 | B6-CN-16 | [DOC-INTERNO CAP_10_parte_10.md:161,174] |
| CN-9.17 | B6-CN-17 | [DOC-INTERNO CAP_10_parte_10.md:123,136-139] |
| CN-9.18 | B6-CN-18 | [DOC-INTERNO CAP_10_parte_10.md:126] |
| CN-9.19 | B6-CN-19 | [DOC-INTERNO CAP_10_parte_10.md:146] |
| CN-9.20 | B6-CN-20 | [DOC-INTERNO CAP_10_parte_10.md:131] |
| CN-9.21 | B6-CN-21 | [DOC-INTERNO CAP_10_parte_10.md:194,196-203] |
| CN-9.22 | B6-CN-22 | [DOC-INTERNO CAP_10_parte_10.md:207] |
| CN-9.23 | B6-CN-23 | [DOC-INTERNO CAP_10_parte_10.md:68] |
| CN-9.24 | B6-CN-24 | [DOC-INTERNO CAP_10_parte_10.md:209] |
| CN-9.25 | B6-CN-25 | [DOC-INTERNO CAP_09_parte_9.md:117] |
| NFR-9.1 | B6-NFR-01 | [DOC-INTERNO CAP_02_parte_II.md:291,293] |
| NFR-9.2 | B6-NFR-02 | [DOC-INTERNO CAP_09_parte_9.md:21] |
| NFR-9.3 | B6-NFR-03 | [DOC-INTERNO CAP_09_parte_9.md:21] |
| NFR-9.4 | B6-NFR-04 | [DOC-INTERNO CAP_09_parte_9.md:181] |
| R-10.1 | B8-R-01 | [DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:167] |
| R-10.2 | B8-R-02 | [DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:143] |
| R-10.3 | B8-R-03 | [DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:402] |
| R-10.4 | B8-R-04 | [DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:131] |
| R-10.5 | B8-R-05 | [DOC-INTERNO docs/methodology_v2/CAP_07_parte_VII.md:637] |
| R-10.6 | B8-R-06 | [DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:131] |
| R-10.7 | B8-R-07 | [DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:389] |
| R-10.8 | B8-R-08 | [DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:387] |
| R-10.9 | B8-R-09 | [DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:391] |
| R-10.10 | B8-R-10 | [DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:404] |
| R-10.11 | B8-R-11 | [DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:230] |
| R-10.12 | B8-R-12 | [DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:406] |
| R-10.13 | B8-R-13 | [DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:234] |
| CN-10.1 | B8-CN-01 | [DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:147] |
| CN-10.2 | B8-CN-02 | [DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:176] |
| CN-10.3 | B8-CN-03 | [DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:174] |
| CN-10.4 | B8-CN-04 | [DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:338] |
| CN-10.5 | B8-CN-05 | [DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:236] |

---

## Sezione 12 — Capitoli non tracciati (con motivazione)

Capitoli della metodologia v2 **non** mappati a un requisito di prodotto, con motivazione. Sono matematica/motore interni, opachi al consumatore del segnale, oppure dettagli interni già coperti via altre Parti in vista prodotto. Sezione **ricostruita dalla v2 e verificata coerente coi blocchi**: rispetto alla v2, le righe sono aggiornate allo stato post-blocchi (alcuni capitoli che la v2 elencava qui come "non tracciati" sono in realtà **tracciati** nell'assemblato via i blocchi corretti — annotato dove pertinente).

| Capitolo (Parte) | Motivo del non-tracciamento |
|---|---|
| **Cap.4 (Parte I)** — compute budget / strategia cloud | Dipendenza infrastrutturale (AWS spot, TCO), non requisito di prodotto. Citato in Sez.8 (NFR-8.4, compute budget post-processing) come dipendenza, non consolidato come requisito a sé. |
| **Cap.10 (Parte II)** — replay/determinismo (fondazione formale) | Il *requisito* di determinismo bit-exact è tracciato (NFR-9.1..4, NFR-8.1/8.2); la **fondazione formale** del replay e il formato esatto dei tre log restano dettaglio interno → premessa citata, Appendice B/FASE-D. |
| **Cap.12 (Parte III)** — definizioni rendimento/scala temporale | Matematica interna del modello, opaca al consumatore: il prodotto pubblica il risultato (payload), non la derivazione. |
| **Cap.13 (Parte III)** — modello di volatilità condizionata (EGARCH) | Matematica interna; alimenta le condizioni di emissione (tracciate in Sez.5, R-5.6/5.8) ma la formula è opaca al consumatore. |
| **Cap.14 (Parte III)** — stato di regime intraday | Matematica interna; il regime calmo/turbolento entra negli NFR di stabilità cross-regime (Sez.8, R-8.11/8.28) ma la classificazione è interna. |
| **Cap.15 (Parte III)** — feature engineering causale + pivot detection | Catalogo 37 feature e algoritmo di pivot detection, matematica interna del motore, opaca al consumatore. Il *contratto di osservazione* del primo pivot è tracciato (Sez.4, NFR-4.1..3); l'algoritmo no. |
| **Cap.16 (Parte IV)** — definizione zone di entry | Derivazione geometrica interna; il prodotto pubblica `entry_zone` (R-3.8/3.35), non la geometria che la produce. |
| **Cap.17 (Parte IV)** — target strutturali | Derivazione geometrica interna; il prodotto pubblica `target_1`/`target_2`/`target_2_type` (R-3.10/3.11/3.21), non la derivazione. |
| **Cap.18 (Parte IV)** — stop strutturali | Derivazione geometrica interna; il prodotto pubblica `stop_loss`/`stop_type` (R-3.23/3.25), non la derivazione. |
| **Cap.19 (Parte IV)** — modello di survival per il target | Matematica interna (Cox); alimenta filtri di emissione e tie-break, opaca al consumatore. |
| **Cap.20 (Parte IV)** — filtri di emissione basati sul survival | Filtro $E_{surv}$ interno; il prodotto espone l'esito (segnale emesso o no, Sez.5), non la matematica del survival. |
| **Cap.21 (Parte IV)** — caso trade_range | Derivazione interna di $A_{range}$; il prodotto espone `setup_class=trade_range` e il filtro 80pt (R-3.28/3.29, CN-5.2), non la derivazione. |
| **Cap.22-26 (Parte V)** — cromosoma, NSGA-II, fitness, walk-forward, calibrazione | Motore GA interno, opaco al consumatore. I suoi *gate* emergono come NFR via Parte VII (Sez.8); la meccanica del GA e i valori-soglia congelati (es. $N_{pivot}$, $\tau_{vol}/\tau_{liq}/\tau_{dist}^{\sigma}$, valori dei timer) non sono prodotto. |
| **Cap.27 (Parte VI)** — pipeline di inference real-time | Interna/FASE-D; citata per il vincolo emissione-only (Sez.5) e come oggetto di verifica del gate di go-live R-8.34, non requisito a sé. *(In B5 dichiarata 0 requisiti propri: Cap.27/28 fondano requisiti già in Sez.1/3/6/9.)* |
| **Cap.28 (Parte VI)** — anti-doppio operazionale, non-refresh, tie-break, logging candidati, determinismo replay | Interna/FASE-D (runtime); i requisiti corrispondenti (anti-duplicato, immutabilità, determinismo) sono tracciati in Sez.6 (CN-6.4/6.5) e Sez.9 (NFR-9.1..4); la meccanica operazionale di Cap.28 è premessa, non requisito a sé. |
| **Cap.30 (Parte VI)** — monitoraggio/dashboard | Interna/FASE-D; citata per contrasto col gate bloccante di riconciliazione (Sez.9, CN-9.18) e come oggetto di verifica del gate R-8.35, non requisito a sé. |
| **Cap.34 (Parte VII)** — bootstrap stazionario | Meccanismo statistico interno; la **procedura** dichiarata è consolidata a corredo del gate sull'$E[R_{net}]$ (Sez.8, R-8.21/8.22/8.23, NFR-8.2), ma la matematica interna del ricampionamento non è requisito a sé oltre la procedura dichiarata. |
| **Cap.35 (Parte VII)** — frozen bundle / hash | La specifica di immutabilità del bundle è **tracciata** (Sez.8, CN-8.3/8.4/8.5, R-8.24, R-8.36); la serializzazione canonica interna e i dettagli di implementazione dell'hash restano interni/FASE-D. |
| **Cap.37-44 (Parte 8) salvo Cap.42** — dati storici/back-adjustment/sanity/esclusione fonti | Materia di training; dipendenza infrastrutturale (Portara/CQG) citata in Sez.2/Sez.9. Cap.44 citato in Sez.9 (CN-9.24, esclusione fonti training). Solo Cap.42 (fasizzazione) è tracciato (Sez.10, R-10.1/CN-10.1). |
| **Cap.45 (Parte 9)** — premessa/collocazione del runtime | Premessa di contesto; nessun requisito di Sez.7 lo fonda come fonte primaria (capitolo di framing). |
| **Cap.50 (Parte 9)** — errori/recovery/riavvio Darwin | Dettaglio interno di recovery del canale; il riavvio Darwin a mezzanotte è premessa (Sez.7/Sez.9), distinto da `RUNTIME_STALE_RESTART` (>100gg, tracciato in Sez.9 R-9.27..29). |
| **Cap.55 (Parte 9)** — punti aperti fuori scope | Capitolo di rinvii; le sue voci aperte sono recepite in Sez.10 (R-10.7/10.8/10.9/10.10/10.12), non requisito a sé. |
| **Cap.57, 58, 63, 65 (Parte 10)** — premessa, tassonomia gap, coerenza inter-temporale, tabella decisioni | Premesse/tassonomia/coerenza/rinvii interni; i requisiti operativi (backfill, riconciliazione, archivio) sono tracciati in Sez.9 (R-9.24..43, CN-9.12..25), questi capitoli di cornice no. |
| **Cap.64 (Parte 10)** — punti aperti fuori scope | Capitolo di rinvii; le voci aperte sono recepite in Sez.10 (R-10.4/10.11/10.13), non requisito a sé. |

**Parti interamente non tracciate**: **Parte III** (Cap.12-15), **Parte IV** (Cap.16-21), **Parte V** (Cap.22-26) — matematica/motore interni, opachi al consumatore del segnale, come da tabella sopra.

> **Coerenza coi blocchi (verifica)**: rispetto alla v2-storico, questa sezione corregge tre righe in cui la v2 elencava come "non tracciati" capitoli che nell'assemblato **sono tracciati** via i blocchi: **Cap.29** (consegna mobile-first + 3 notifiche) è ora tracciato in Sez.6 (NFR-6.5..7, R-6.17..24) via B4-EXT, quindi **non** compare qui; **Cap.34/35** (bootstrap, frozen bundle) hanno la loro procedura/specifica dichiarata tracciata in Sez.8 via B7 (le righe sopra ne riportano la parte tracciata vs la parte interna). Nessun capitolo che fonda un requisito-blocco è erroneamente listato come "non tracciato".

---

## Sezione 13 — Blocchi / Domande aperte

Due blocchi aperti incardinati (latenza Telegram, orario sessione) + le dipendenze aperte enumerate da B8 (Sez.10). I requisiti dipendenti dai due blocchi portano il tag `[B-1 PROVVISORIO]` / `[B-2 PROVVISORIO]`.

### 13.1 Blocchi aperti incardinati (con tag provvisorio)

- **B-1 — Latenza Telegram $L_{max}$ non verificata empiricamente (M-2 OPEN)**.
  - *Requisiti dipendenti (tag `[B-1 PROVVISORIO]`)*: **NFR-6.3**, **NFR-6.4** (Sez.6), **NFR-8.3** (Sez.8), **R-10.3** (Sez.10).
  - *Motivo*: il valore $L_{max}=30$ s è valore di lavoro provvisorio; la verifica empirica della latenza effettiva del canale Telegram non è stata eseguita ed è carryover di Appendice E / FASE-D. `[DOC-INTERNO CAP_09_parte_9.md:402]`, `[DOC-INTERNO CAP_07_parte_VII.md:23]`, `[DOC-INTERNO CAP_10_parte_10.md:237]`.
  - *Cosa serve per sbloccarlo*: probe empirico sulla latenza del bot Telegram reale (Appendice E / FASE-D) → upgrade del requisito da provvisorio a verificato.
  - *Stato M*: M-2 **OPEN** (CARRYOVER). L'assemblaggio **non chiude** M-2: lo incardina nello stesso stato OPEN in cui vive nei blocchi.

- **B-2 — Orario di sessione FIB in attesa di upgrade a PROVA-EMPIRICA (M-GOV-1)**.
  - *Requisito dipendente (tag `[B-2 PROVVISORIO]`)*: **R-7.11** (Sez.7).
  - *Motivo*: l'orario 08:00-22:00 CET è recepito da decisione AC 13/06/2026 + `[WIKI-HINT Borsa Italiana, da verificare]`; l'upgrade a `[PROVA-EMPIRICA]` dal primo probe V-1 sul tape DAPI è APERTO (M-GOV-1, namespace governance). L'origine normativa della finestra (epoca E5 / `fib_session_calendar.csv`) è premessa di Sez.10 / Cap.41.
  - *Cosa serve per sbloccarlo*: primo probe V-1 che confermi empiricamente la finestra di negoziazione continua sul tape DAPI (e probe V-2 per il calendario IDEM) → upgrade del requisito da provvisorio a verificato.
  - *Stato M*: M-GOV-1 **APERTO** (CARRYOVER). L'assemblaggio **non chiude** M-GOV-1: la regola operativa di sessione (R-7.11) è in vigore; ciò che è PENDING è l'**upgrade empirico** del valore.

### 13.2 Dipendenze aperte verso FASE-D (da B8 / Sez.10) — riepilogo

Le dipendenze aperte enumerate in Sez.10 sono **dichiarate aperte, MAI risolte**. Il loro **esito/valore** è PENDING-empirico — marcato, non asserito. Riepilogo:

| Dipendenza aperta | Requisito che la dichiara | Destinazione | Stato |
|---|---|---|---|
| Latenza $L_{max}=30$s Telegram effettiva (M-2 OPEN) | R-10.3 (+ NFR-6.3/6.4, NFR-8.3) | Appendice E / FASE-D | aperta; valore non misurato |
| Upgrade empirico orario di sessione (M-GOV-1) | R-7.11 (premessa Cap.41) | probe V-1 (tape DAPI) / V-2 (calendario IDEM) / FASE-D | aperta; upgrade non eseguito |
| Calibrazione fine $\theta_{reconcile}$ (provvisorio) | R-10.4 (+ CN-9.20) | FASE-D / CAP-DATA-04 / monitoring post-go-live | aperta; nessun valore assegnato |
| Congelamento empirico dei 10 parametri di tuning | R-10.5 (+ CN-8.7) | monitoring post-go-live 3-6 mesi | aperta; default provvisori |
| Run del validator sull'edge (DSR/PBO/OOS, valori d'edge) | R-10.6 (+ Sez.8 cardine) | ruolo `validator` / FASE-D | aperta; nessun esito d'edge asserito |
| Decodifica codici mese Directa-IDEM mancanti (oltre `F`/`I`) | R-10.7 (+ R-7.7) | runtime-discovery (ANAG) / FASE-D | aperta; lookup incompleta |
| Abilitazione FDAX standard (account non abilitato 2026-05-27) | R-10.8 | valutazione PHASE-2 | aperta; non decisa |
| Scelta vendor cross-index pluriennale (training PHASE-2) | R-10.9 | attivazione PHASE-2 | aperta; non scelto |
| Apertura flusso DAPI come fonte di training | R-10.10 | nuovo task Planner | aperta; fuori scope corrente |
| Migrazione formato legacy→esteso dei dump | R-10.11 | FASE-D (una-tantum) | aperta; debito di migrazione |
| Implementazione codice operativo della pipeline | R-10.12 | FASE-D | aperta; specifica ≠ implementazione |
| Estensione immutabilità `CANDLERANGE` oltre T+3 | R-10.13 (+ R-9.43, CN-9.18) | probe addizionale FASE-D / gate Cap.60 nel frattempo | aperta; immutabilità oltre T+3 morning assunta per estensione, non dimostrata |

### 13.3 PENDING-empirico residui (marcati, non asseriti)

Oltre alle dipendenze sopra, restano marcati come PENDING-empirico (ereditati dai blocchi, mai asseriti come verificati): PRICE `f5`/`f7` (contatori cumulativi non disambiguati, Sez.9 R-9.16); ticker 1030 (realtime non sottoscritto, verifica parziale / PHASE-2 gated); riavvio Darwin a mezzanotte (comportamento notturno, premessa Sez.7/Sez.9); base calendario-vs-giorni-di-trading delle finestre 30/100 (V-2; il valore `L_warmup=30` è congelato, è pendente solo la mappatura sul calendario IDEM); tutte le grandezze d'esito d'edge di Sez.8 (DSR/PBO/$E[R_{net}]$/CVaR/MDD/$r_{emit}$/$\rho_{sessions}$ effettivi, esito 12 criteri, decisione GO/NO-GO, $L_{avg}$ calibrato, $F$ effettivo).

**Nota**: la dipendenza da CAP-01/02/03 a SHA congelati (freeze G-09) è dichiarata in nota di testa e **non** è un blocco aperto (i capitoli sono chiusi e congelati, citabili). Nessun altro blocco aperto oltre B-1 e B-2.

---

*Documento SPEC-FUNZ-01 (assemblato). Merge editoriale loss-less della serie B1..B8 (375 requisiti-blocco, 1-a-1, 0 dedup, 0 persi, 0 inventati). Rimpiazza la v2 (archiviata in `SPEC_FUNZ_01_v2_storico.md`, tag git `spec-funz-01-v2-storico`). Nessun CAP toccato (freeze G-09). Nessun file-blocco B1..B8 modificato. Costruito dai blocchi corretti, non dalla v2: i 6 difetti SOLO-v2 non sono re-introdotti (vedi REPORT, auto-check no-reintroduzione). Edge-PENDING intatto: 0 asserzioni d'esito d'edge (vedi REPORT, auto-check edge-PENDING).*
