# SPEC-FUNZ-01 — Specifica funzionale del prodotto-segnale FIB (PHASE-1)

**Natura del documento**: specifica funzionale / di prodotto / requisiti di business. NON è un capitolo metodologico né una Parte della metodologia v2.
**Vista**: operatore / prodotto / committente. Consolida la metodologia v2 (10 Parti, Cap.1-65, tutte PASS) in requisiti funzionali (`R-N`), non-funzionali / qualità (`NFR-N`) e vincoli normativi (`CN-N`), tracciati capitolo per capitolo.
**Perimetro temporale**: PHASE-1 = FIB-only. PHASE-2 (cross-index DAX / EuroStoxx50 / ES / MES) è fuori scope (Cap.42 Parte 8).
**Provenienza delle asserzioni**: ogni asserzione fattuale è un richiamo a un capitolo metodologico chiuso PASS, etichettato `[DOC-INTERNO <file>:<rif>]` o, per il codice, `[CODICE-ESISTENTE <path>:<linea>]`. Questo documento NON introduce nuove dichiarazioni "verificato X" di prima istanza (RM-1).

> **Nota di lettura sulle fonti esterne (RM-3).** Ogni riferimento a documentazione di sistemi esterni (wiki Directa, docs Telegram, docs Portara/CQG, docs CME/Eurex, testo MiFID II) è etichettato `[WIKI-HINT, da verificare]` e non costituisce mai fonte unica di un'asserzione strutturale. In particolare la **wiki Directa è dimostrata inesatta** sullo schema CANDLE (ordine reale `C;L;H;O`, non `O;H;L;C` del wiki — eredità AUDIT-RM-RETRO CAP-DATA-02, `[CODICE-ESISTENTE scripts/export_directa_history_parametric.py:477-481]`): qualunque schema-dato citato in questo documento proviene dal decoder di produzione, non dal wiki.

---

## Sezione 1 — Scopo, visione e perimetro del prodotto

### 1.1 Proposta di valore

Il prodotto-segnale FIB è un **servizio di segnalazione operativa** che pubblica, su un canale Telegram personale, segnali long/short strutturati sul FIB (future mini su FTSE MIB, mercato IDEM, moltiplicatore 5 EUR/punto), con banda di ingresso, due target strutturali e stop strutturale, eseguibili manualmente da cellulare durante la sessione lavorativa dell'operatore. Il sistema **non esegue ordini**: emette informazione decisionale, l'operatore decide ed esegue.

Proposta di valore in tre righe (leggibile da non-tecnico):

> Ricevi sul telefono segnali long/short sul future FTSE MIB con zona d'ingresso, target e stop già calcolati su base strutturale e con probabilità di successo modellata. Li esegui a mano sul tuo broker quando vuoi, un contratto alla volta. Il sistema ti avvisa, non opera al tuo posto.

### 1.2 Confine architetturale "solo emissione"

Il confine "**solo emissione, nessuna esecuzione**" è un **vincolo strutturale non negoziabile**, non una scelta implementativa rivedibile: discende dal punto 1 della dichiarazione di intenti dell'operatore ("genera solo segnali e non effettuerà mai trading direttamente") `[DOC-INTERNO CAP_01_parte_I.md:15]`. Il motore pubblica segnali; l'apertura, l'invio dell'ordine, la gestione e la chiusura della posizione competono esclusivamente all'operatore umano.

### 1.3 Out-of-scope di prodotto (lista chiusa)

Il prodotto **non** comprende, per costruzione: gestione attiva della posizione dopo il fill; sizing dinamico (size fissa 1 contratto); trailing stop / scaling-out / take profit anticipato; esecuzione automatica di ordini; cross-index PHASE-2 (DAX/EuroStoxx50/ES/MES). La separazione gestione-posizione / segnale è ereditata dai punti 7-8 della dichiarazione di intenti `[DOC-INTERNO CAP_01_parte_I.md:27]` `[DOC-INTERNO CAP_02_parte_II.md:368]`.

### 1.4 PHASE-1 vs PHASE-2

SPEC-FUNZ-01 specifica **PHASE-1 = FIB-only**. La PHASE-2 cross-index è dichiarazione normativa già fasizzata in `[DOC-INTERNO CAP_08_parte_8.md:167]` e fuori scope di questo documento (vedi Sezione 10).

### 1.5 Requisiti introdotti

- **R-1 (R-PERIM-1) — Emissione di segnali strutturati FIB.** Il prodotto pubblica segnali long/short sul FIB con payload strutturato (banda, target_1, target_2, stop). *Valore operativo*: fornisce all'operatore ipotesi operative pronte all'esecuzione manuale. *Origine*: `[DOC-INTERNO CAP_01_parte_I.md:15]`, `[DOC-INTERNO CAP_02_parte_II.md:24]`.
- **R-2 (R-PERIM-2) — Esecuzione delegata all'operatore.** Il prodotto non invia ordini; l'esecuzione è manuale. *Valore operativo*: compliance retail e controllo umano totale sulla posizione. *Origine*: `[DOC-INTERNO CAP_01_parte_I.md:15]`.
- **R-3 (R-PERIM-3) — Confine FIB-only PHASE-1.** Il prodotto opera esclusivamente sul FIB in PHASE-1. *Valore operativo*: cantierabilità immediata senza dipendenza da vendor cross-index. *Origine*: `[DOC-INTERNO CAP_08_parte_8.md:167]`.
- **CN-1 — Vincolo "solo emissione" non negoziabile.** Il sistema non esegue ordini in alcuna fase del ciclo di vita. *Valore di prodotto*: posizionamento di compliance e protezione legale del committente. *Origine*: `[DOC-INTERNO CAP_01_parte_I.md:15]`.

**Out-of-scope Sezione 1**: nessuna gestione posizione, nessun sizing dinamico, nessun trailing/scaling, nessuna esecuzione automatica, nessun cross-index PHASE-2.

| Requisito ID | Capitolo metodologia v2 | Tipo |
|---|---|---|
| R-1 | Cap.1 Parte I, Cap.6 Parte II | R |
| R-2 | Cap.1 Parte I | R |
| R-3 | Cap.42 Parte 8 | R |
| CN-1 | Cap.1 Parte I | CN |

---

## Sezione 2 — Attori, contesto, personas

### 2.1 Persona primaria — l'operatore retail

L'operatore destinatario è un **risk manager bancario italiano**, funzionario di una banca commerciale, classificato **retail non professionale ai sensi MiFID II** `[WIKI-HINT, da verificare]` con ancoraggio interno `[DOC-INTERNO CAP_01_parte_I.md:23]`. Attributi della persona:

1. **Profilo MiFID II**: retail non professionale; vincoli di accesso a strumenti/leve e regimi di tutela come dati immutabili.
2. **Operatività mobile**: interazione con il broker da **cellulare** durante la giornata lavorativa, in modo discontinuo; non garantisce presenza continuativa allo schermo `[DOC-INTERNO CAP_01_parte_I.md:23]`.
3. **Vincoli temporali**: attività principale come dipendente bancario; tempo limitato per il monitoraggio attivo del terminale.
4. **Strumenti**: app Telegram (ricezione segnali) + app/terminale Directa SIM (invio ordini). Sizing 1 contratto FIB alla volta `[DOC-INTERNO CAP_01_parte_I.md:25]`.
5. **Esecuzione su miniFIB**: l'operatore esegue manualmente su miniFIB (moltiplicatore 1 EUR/pt), mentre il motore calibra/inferisce su FIB pieno `[DOC-INTERNO CAP_09_parte_9.md:75]`.

### 2.2 Stakeholder secondari

- **Supervisore / committente**: definisce gli obiettivi metodologici, riceve i report di lifecycle e le notifiche operative del prodotto.
- **Reviewer di compliance esterno** (potenziale, futuro): consulente legale MiFID II che valuta il posizionamento del prodotto (Sezione 8).
- **Fornitori esterni** (potenziali): valutatori cloud AWS (Cap.4 Parte I), fornitore storico Portara/CQG (Cap.37 Parte 8), fornitore bot Telegram (Cap.3 Parte I / Appendice E).

### 2.3 Ambiente di esecuzione utente

Smartphone Android/iOS con app Telegram (ricezione segnale) e app Directa per l'ordering. Il **PC fisso** (i5-7200U, Anaconda — `[DOC-INTERNO CAP_01_parte_I.md:39]`) è ambiente di sviluppo, training (via cloud) e inference live, **mai** ambiente di esecuzione ordini.

### 2.4 Requisiti introdotti

- **R-4 — Esecuzione manuale come vincolo.** Il prodotto assume esecuzione manuale dell'operatore da mobile; il messaggio è progettato per la decisione mobile. *Valore operativo*: il segnale è azionabile in mobilità, senza presenza al PC. *Origine*: `[DOC-INTERNO CAP_01_parte_I.md:23]`, `[DOC-INTERNO CAP_06_parte_VI.md:146]`.
- **R-5 — Canale Telegram come output obbligatorio.** Il bot Telegram personale dell'operatore è l'unica via di output verso l'operatore. *Valore operativo*: consegna su un canale già attivo e familiare, ricevuto sul cellulare. *Origine*: `[DOC-INTERNO CAP_01_parte_I.md:47]`, `[DOC-INTERNO CAP_06_parte_VI.md:146]`.

**Out-of-scope Sezione 2**: tutorial / manuale d'uso del bot (materia FASE-D); profilazione di marketing della persona.

| Requisito ID | Capitolo metodologia v2 | Tipo |
|---|---|---|
| R-4 | Cap.2 Parte I, Cap.29 Parte VI | R |
| R-5 | Cap.3 Parte I, Cap.29 Parte VI | R |

---

## Sezione 3 — Requisiti funzionali del segnale (prodotto)

### 3.1 Il segnale come feature di prodotto

Il segnale è una **tupla immutabile** pubblicata all'operatore. Dal punto di vista del consumatore, i campi del payload sono i seguenti (contratto formale `[DOC-INTERNO CAP_02_parte_II.md:19]`; voci pubblicate sul messaggio `[DOC-INTERNO CAP_02_parte_II.md:241]`):

| # | Campo | Tipo / dominio | Vincoli | Origine v2 |
|---|---|---|---|---|
| 1 | `signal_id` | identificatore opaco | univoco sull'intero orizzonte operativo, non riusabile | `[DOC-INTERNO CAP_02_parte_II.md:23]` |
| 2 | `timestamp_emission` | datetime al minuto, CET | minuto chiuso | `[DOC-INTERNO CAP_02_parte_II.md:25]` |
| 3 | `direction` | `{long, short}` | — | `[DOC-INTERNO CAP_02_parte_II.md:27]` |
| 4 | `entry_zone` | banda discreta di prezzo | estremi multipli di 5 pt; semi-ampiezza $b\in\{5,..,40\}$ | `[DOC-INTERNO CAP_02_parte_II.md:29]` |
| 5 | `target_1` | prezzo, multiplo di 5 | $>p_{ref}$ (long) / $<p_{ref}$ (short); obbligatorio | `[DOC-INTERNO CAP_02_parte_II.md:35]` |
| 6 | `target_2` | prezzo, multiplo di 5 | informazione strutturale pubblicata, **non** variabile di lifecycle (Q-05 Clausola 2) | `[DOC-INTERNO CAP_02_parte_II.md:37]` |
| 7 | `target_2_type` | `{structural, synthetic}` | qualificatore natura del livello | `[DOC-INTERNO CAP_02_parte_II.md:39]` |
| 8 | `stop_loss` | prezzo, multiplo di 5 | $d_{stop}=|p_{ref}-\texttt{stop\_loss}|>b$ | `[DOC-INTERNO CAP_02_parte_II.md:41]` |
| 9 | `stop_type` | `{structural, synthetic}` | qualificatore natura del livello | `[DOC-INTERNO CAP_02_parte_II.md:51]` |
| 10 | `setup_class` | `{directional, trade_range}` | determina il filtro 80pt applicato | `[DOC-INTERNO CAP_02_parte_II.md:53]` |

I campi tecnici $\Delta t_{cromosoma}$ (timer post-trigger) e $T_{touch}^{max}$ (timer pre-trigger) sono parte della tupla formale `[DOC-INTERNO CAP_02_parte_II.md:63]` ma **non** sono pubblicati nel messaggio all'operatore `[DOC-INTERNO CAP_02_parte_II.md:253]`. Il messaggio pubblica 9 voci (i due timer esclusi); la tabella sopra elenca i 10 campi del payload consumer-facing del segnale.

### 3.2 Invarianti e regole del prodotto

- **R-6 — Payload immutabile dopo emissione.** Una volta emesso, il payload identificato da `signal_id` non muta: l'operatore opera su valori che non cambiano a sua insaputa. *Valore operativo*: il segnale è un oggetto contrattuale affidabile fra lettura e invio ordine. *Origine*: `[DOC-INTERNO CAP_02_parte_II.md:73]`.
- **R-7 — Segnale unico attivo.** A ogni istante è attivo al massimo un segnale: $|\mathcal{A}(t)|\le 1$. Una revisione si manifesta come **sostituzione** (nuovo `signal_id`, revoca del precedente), non come modifica. *Valore operativo*: nessuna ambiguità su quale segnale è operativo; coerente con 1 contratto alla volta. *Origine*: `[DOC-INTERNO CAP_02_parte_II.md:81]`.
- **R-8 — Filtro minimo 80pt.** Il prodotto non pubblica segnali con `target_1` directional a meno di 80 pt da $p_{ref}$, né `trade_range` con ampiezza $A_{range}<80$ pt. *Valore operativo*: esclude micro-movimenti non remunerativi al netto delle commissioni; non limita il numero di segnali. *Origine*: `[DOC-INTERNO CAP_01_parte_I.md:83]`, `[DOC-INTERNO CAP_02_parte_II.md:55]`.
- **R-9 — Tick discreto 5 pt.** Tutti i prezzi pubblicati (entry, target, stop) sono multipli di 5 punti FIB; $b_{min}=5$ è 1 tick. *Valore operativo*: i livelli sono inseribili tali e quali sul broker. *Origine*: `[DOC-INTERNO CAP_02_parte_II.md:9]`.

### 3.3 Esempio numerico (payload concreto)

Segnale long, setup directional (tutti i prezzi multipli di 5):

```
signal_id      = a3f7d9
direction      = long
setup_class    = directional
entry_zone     = [13.250, 13.260]   (p_ref = 13.255, b = 5)
target_1       = 13.350             (+95 pt da p_ref)   -> filtro 80pt rispettato
target_2       = 13.450  (structural)
stop_loss      = 13.200  (structural)   (d_stop = 55 pt > b = 5)
timestamp_emission = 2026-06-15 10:42 CET
```

Coerenza: `target_1` dista 95 pt ($\ge 80$, R-8 OK); $d_{stop}=55>b=5$ (R-7/CAP-01 vincolo geometrico OK); tutti i livelli multipli di 5 (R-9 OK). Esempio coerente con il layout mobile di `[DOC-INTERNO CAP_06_parte_VI.md:176]`.

**Out-of-scope Sezione 3**: matematica della derivazione strutturale di target/stop (Cap.17-18 Parte IV); algoritmo pivot detection (Cap.15 Parte III); soglie/parametri congelati di filtro (Cap.20 Parte IV, Cap.26 Parte V).

| Requisito ID | Capitolo metodologia v2 | Tipo |
|---|---|---|
| R-6 | Cap.6 Parte II | R |
| R-7 | Cap.6 Parte II, Cap.28 Parte VI | R |
| R-8 | Cap.5 Parte I, Cap.8 Parte II | R |
| R-9 | Cap.6 Parte II | R |

---

## Sezione 4 — Ciclo di vita del segnale visto dall'operatore

### 4.1 La state machine in vista operatore

Il ciclo di vita del segnale è **1 stato non-terminale + 6 stati terminali** (Q-05 Clausola 1) `[DOC-INTERNO CAP_02_parte_II.md:95]`. In vista operatore:

```
                 emissione (notifica Telegram, payload completo)
                          │
                       ┌──▼──┐
                       │active│  "in attesa di raw touch"
                       └──┬──┘
        ┌────────┬────────┼────────┬────────────┬───────────┐
        ▼        ▼        ▼        ▼            ▼           ▼
  target_1_hit stopped invalidated missed_target expired   revoked
   (successo)  (stop)  (ipotesi   (target preso  (timer    (sostituito
                        rotta pre- prima del touch scaduto)  da nuovo
                        touch)     -> non eseguibile)        signal_id)
```

Dopo l'emissione, l'operatore riceve una **notifica di `trigger_event`** separata al raw touch della entry zone ("esecuzione attiva") `[DOC-INTERNO CAP_02_parte_II.md:271]`. Il `trigger_event` è un **evento notificato**, non uno stato `[DOC-INTERNO CAP_02_parte_II.md:139]`.

### 4.2 Significato dei 6 terminali (vista operatore)

- **`target_1_hit`** — successo: dopo il touch, il prezzo ha raggiunto `target_1` prima di stop/scadenza. Il contratto del segnale si chiude qui; la posizione oltre target_1 è gestita dall'operatore `[DOC-INTERNO CAP_02_parte_II.md:101]`.
- **`stopped`** — dopo il touch, il prezzo ha raggiunto `stop_loss` prima di `target_1` `[DOC-INTERNO CAP_02_parte_II.md:103]`.
- **`invalidated`** — prima del touch, una condizione strutturale (incluso superamento dello stop pre-touch) rompe l'ipotesi: il segnale non è più valido `[DOC-INTERNO CAP_02_parte_II.md:105]`.
- **`missed_target`** — prima del touch, il prezzo raggiunge `target_1`: il target è stato realizzato dal mercato ma **il segnale non è eseguibile** (la zona non è mai stata toccata) `[DOC-INTERNO CAP_02_parte_II.md:107]`.
- **`expired`** — timer scaduto: pre-trigger ($T_{touch}^{max}$ senza touch) o post-trigger ($\Delta t_{cromosoma}$ dopo il touch). La causa è nel log `[DOC-INTERNO CAP_02_parte_II.md:109]`.
- **`revoked`** — il segnale è stato **sostituito** da uno nuovo con `signal_id` differente: l'operatore deve riferirsi al nuovo segnale `[DOC-INTERNO CAP_02_parte_II.md:111]`.

### 4.3 Segnale vs position lifecycle

Il **ciclo di vita del segnale** si chiude definitivamente a `target_1_hit`. Il **position lifecycle post-target_1** (raggiungimento di target_2, stop post-target_1, MFE/MAE) è una **submacchina distinta** `[DOC-INTERNO CAP_02_parte_II.md:349]`: IN-SCOPE solo per il **reporting** di calibrazione, OUT-OF-SCOPE da execution policy. L'operatore lo vede come dato nei report periodici, **mai** come comando di esecuzione `[DOC-INTERNO CAP_02_parte_II.md:368]`.

### 4.4 Requisiti introdotti

- **R-10 — Notifica `trigger_event` separata.** Al raw touch della entry zone il prodotto pubblica una notifica distinta dal messaggio di emissione, riferita al `signal_id`, con istante del touch ed expiry. *Valore operativo*: l'operatore sa quando il segnale è entrato in zona ed è eseguibile. *Origine*: `[DOC-INTERNO CAP_02_parte_II.md:271]`, `[DOC-INTERNO CAP_06_parte_VI.md:190]`.
- **R-11 — Distinzione segnale / position lifecycle.** Il prodotto chiude il segnale a `target_1_hit`; il tracking post-target_1 è solo reporting, non comando. *Valore operativo*: nessuna istruzione di gestione attiva imposta all'operatore (compliance punto 8 dichiarazione). *Origine*: `[DOC-INTERNO CAP_02_parte_II.md:349]`.
- **CN-2 — Marker normativi dei 6 esiti terminali.** Ogni esito terminale è loggato come marker normativo distinto (`SIGNAL_TARGET_1_HIT` / `STOPPED` / `INVALIDATED` / `MISSED_TARGET` / `EXPIRED` / `REVOKED`), coerente con la state machine. *Valore di prodotto*: tracciabilità per audit / compliance. *Origine*: `[DOC-INTERNO CAP_09_parte_9.md:353]` (D-9-NB3).

**Out-of-scope Sezione 4**: regola di simulazione del fill virtuale in backtest (Parte III); execution policy post-target_1.

| Requisito ID | Capitolo metodologia v2 | Tipo |
|---|---|---|
| R-10 | Cap.7 Parte II, Cap.29 Parte VI | R |
| R-11 | Cap.11 Parte II | R |
| CN-2 | Cap.7 Parte II, Cap.54 Parte 9 | CN |

---

## Sezione 5 — Canale di pubblicazione e requisiti di consegna

### 5.1 Telegram come canale di consegna

Il canale è il **bot Telegram personale** dell'operatore. Il messaggio è progettato **mobile-readable**: leggibile su schermo cellulare (larghezza tipica 375-414 px), font monospaziato, senza scroll orizzontale, contenuto critico nella prima schermata, interamente testuale e self-contained `[DOC-INTERNO CAP_06_parte_VI.md:152]`.

### 5.2 Contenuti minimi (9 voci)

Il messaggio di emissione pubblica **9 voci ordinate** `[DOC-INTERNO CAP_02_parte_II.md:241]`: `signal_id`, `direction`, `setup_class`, `entry_zone`, `target_1`, `target_2`, `stop_loss`, `timestamp_emission`, più i qualificatori `target_2_type` e `stop_type`. I timer $\Delta t_{cromosoma}$ / $T_{touch}^{max}$ non figurano `[DOC-INTERNO CAP_02_parte_II.md:253]`.

**Esempio testuale di messaggio di emissione** (layout mobile-first `[DOC-INTERNO CAP_06_parte_VI.md:176]`, prezzi multipli di 5):

```
ID: a3f7d9
LONG
ZONE: 13.250 - 13.260
TGT1: 13.350 (+95 pt)
SL: 13.200 (-55 pt)
TGT2: 13.450 (S)
SL-type: structural
CLASS: dir
EMIT: 10:42 CET
```

**Esempio testuale di messaggio di `trigger_event`** (messaggio separato `[DOC-INTERNO CAP_06_parte_VI.md:190]`):

```
TRIGGER a3f7d9
RAW TOUCH @ 13.255  EMIT-ref 10:42 CET
EXEC: 11:07 CET   EXPIRY: 2026-06-16 17:22 CET
```

### 5.3 Latenza di consegna (NFR) e M-2

- **NFR-1 (NFR-L_max) — Latenza end-to-end $\le 30$ s.** La latenza fra `timestamp_emission` e ricezione sul cellulare deve rispettare $L\le L_{max}$, con $L_{max}=30$ s (valore di lavoro provvisorio). *Valore operativo*: oltre 30 s il prezzo strutturale può spostarsi e il segnale perde valore informativo per l'operatore in mobilità. *Origine*: `[DOC-INTERNO CAP_02_parte_II.md:261]` (Cap.9.3), `[DOC-INTERNO CAP_07_parte_VII.md:23]` (AC-GO-10).

> **M-2 OPEN — dipendenza aperta dichiarata esplicitamente.** La **verifica empirica** del valore $L_{max}=30$ s contro bot Telegram reale è **dipendenza aperta verso Appendice E / FASE-D**, NON risolta in SPEC-FUNZ-01. La spec FIB-only fissa il **requisito** (NFR-1) ma non lo verifica: la misura empirica resta carryover (M-2 OPEN, Review v1 CAP-02 — `[DOC-INTERNO tasks/CARRYOVER.md:21]`; rinvio empirico confermato in `[DOC-INTERNO CAP_07_parte_VII.md:23]`).

### 5.4 Requisiti di consegna

- **R-12 — Anti-duplicato.** Ogni `signal_id` è pubblicato una sola volta; un set persistito impedisce la ripubblicazione dopo restart. *Valore operativo*: l'operatore non riceve doppioni dello stesso segnale. *Origine*: `[DOC-INTERNO CAP_02_parte_II.md:265]`.
- **R-13 — Nuovo messaggio per nuovo `signal_id` (no edit).** Una sostituzione produce un messaggio separato, mai un edit del messaggio precedente (coerente con l'immutabilità del payload). *Valore operativo*: la cronologia Telegram resta traccia storica fedele; nessun valore muta dopo l'invio. *Origine*: `[DOC-INTERNO CAP_02_parte_II.md:269]`.
- **R-14 — Notifica trigger separata dall'emissione.** La notifica del raw touch è un messaggio distinto. *Valore operativo*: distingue "segnale esistente" da "segnale ora eseguibile". *Origine*: `[DOC-INTERNO CAP_02_parte_II.md:271]`, `[DOC-INTERNO CAP_06_parte_VI.md:190]`.

**Out-of-scope Sezione 5**: stringhe esatte del bot e gestione `chat_id` (Appendice E); verifica empirica di $L_{max}$ (M-2 → FASE-D).

| Requisito ID | Capitolo metodologia v2 | Tipo |
|---|---|---|
| NFR-1 | Cap.9 Parte II, Cap.31 Parte VII | NFR |
| R-12 | Cap.9 Parte II | R |
| R-13 | Cap.9 Parte II, Cap.6 Parte II | R |
| R-14 | Cap.9 Parte II, Cap.29 Parte VI | R |

---

## Sezione 6 — Requisiti operativi e di sessione

### 6.1 Vincoli operativi del prodotto

- **R-15 — Sessione operativa 8:00-22:00 CET.** Il prodotto emette e processa segnali nella finestra unica e continua 8:00-22:00 CET (epoca E5). *Valore operativo*: copre l'intera negoziazione FIB su IDEM; coerente con la disponibilità mobile dell'operatore. *Origine*: `[DOC-INTERNO CAP_01_parte_I.md:9]`, `[DOC-INTERNO CAP_09_parte_9.md:273]`.
- **R-16 — Sizing fisso 1 contratto FIB.** Size non parametrabile dall'utente: 1 contratto alla volta. *Valore operativo*: nessuna gestione di size richiesta all'operatore (punto 7 dichiarazione). *Origine*: `[DOC-INTERNO CAP_01_parte_I.md:25]`.
- **R-17 — Singolo segnale attivo per direzione.** Vincolo $|\mathcal{A}(t)|\le 1$: nessuna politica multi-segnale concorrente. *Valore operativo*: chiarezza operativa, coerenza con 1 contratto. *Origine*: `[DOC-INTERNO CAP_02_parte_II.md:81]`, `[DOC-INTERNO CAP_06_parte_VI.md:81]`.
- **R-18 — Commissioni 5 EUR/operazione.** Il prodotto assume 5 EUR/op (2 punti FIB equivalenti per ciclo apertura-chiusura) nel calcolo del rendimento netto. *Valore operativo*: il filtro 80pt e le metriche di successo sono al netto del costo reale. *Origine*: `[DOC-INTERNO CAP_01_parte_I.md:25]`, `[DOC-INTERNO CAP_01_parte_I.md:73]`.
- **R-19 — Policy rollover / contract switch.** Al boot della sessione del giorno di scadenza (terza venerdì del mese) la pipeline sottoscrive direttamente il next-month, con marker `CONTRACT_SWITCH`, saltando la finestra 08:00-09:00 del front in scadenza. *Valore operativo*: il segnale resta coerente sul contratto liquido; evita la patologia di settlement. *Origine*: `[DOC-INTERNO CAP_09_parte_9.md:98]` (D-9-NB2).

### 6.2 Esempio rollover

Ciclo giugno→settembre 2026: front-month `FIB6F` (scadenza 2026-06-19, terza venerdì di giugno). Al boot della sessione del **2026-06-19** la pipeline sottoscrive direttamente `FIB6I` (next-month, settembre 2026), emettendo `CONTRACT_SWITCH {from: FIB6F, to: FIB6I, scadenza_from: 2026-06-19}` `[DOC-INTERNO CAP_09_parte_9.md:103]`. (Codici mese Directa-IDEM verificati: `F`=giugno, `I`=settembre `[DOC-INTERNO CAP_09_parte_9.md:61]`.)

### 6.3 Separazione segnale / gestione posizione

Il motore (segnale) e la gestione della posizione (operatore) sono separati strutturalmente: la gestione attiva post-fill è fuori scope del prodotto (R-11, CN-1).

**Out-of-scope Sezione 6**: filtro pre-expiry di **training** $N=3$ giorni (Cap.39 Parte 8 — è regola di training, distinta dallo switch runtime); lookup completa codici mese oltre `F`/`I` (FASE-D).

| Requisito ID | Capitolo metodologia v2 | Tipo |
|---|---|---|
| R-15 | Cap.1 Parte I, Cap.52 Parte 9 | R |
| R-16 | Cap.2 Parte I | R |
| R-17 | Cap.6 Parte II, Cap.28 Parte VI | R |
| R-18 | Cap.2 Parte I, Cap.5 Parte I | R |
| R-19 | Cap.56 Parte 9 (D-9-NB2) | R |

---

## Sezione 7 — Requisiti di qualità e criteri di accettazione del prodotto

### 7.1 Metrica primaria e KPI di prodotto

La **metrica primaria di successo** è $E[R_{net}\mid executed]$ **positivo dopo commissioni** ($E[R_{net}\mid executed]=E[R_{gross}\mid executed]-2c$, $c=1$ pt) `[DOC-INTERNO CAP_01_parte_I.md:73]`. KPI di prodotto (calcolati sul replay OOS deterministico):

| KPI | Definizione (vista prodotto) | Origine v2 |
|---|---|---|
| Expected net return | profitto netto medio per segnale eseguito, in pt FIB | `[DOC-INTERNO CAP_01_parte_I.md:71]` |
| Executable rate | frazione di segnali emessi che raggiungono il raw touch entro $T_{touch}^{max}$ | `[DOC-INTERNO CAP_01_parte_I.md:77]` |
| Target hit rate | frazione di segnali eseguiti che raggiungono target_1 prima di stop/scadenza | `[DOC-INTERNO CAP_01_parte_I.md:77]` |
| Invalidation rate | frazione di segnali invalidati prima del touch | `[DOC-INTERNO CAP_01_parte_I.md:77]` |
| Missed target rate | frazione di segnali con target_1 raggiunto prima del touch | `[DOC-INTERNO CAP_01_parte_I.md:77]` |
| CVaR 95% | rischio di coda del rendimento per segnale eseguito | `[DOC-INTERNO CAP_01_parte_I.md:79]` |
| Max drawdown intraday | drawdown massimo dell'equity sintetica di sessione | `[DOC-INTERNO CAP_01_parte_I.md:79]` |
| $\pi_{t_2\mid t_1}$ | hit-rate condizionale target_2 dato target_1 (qualità informativa del payload) | `[DOC-INTERNO CAP_02_parte_II.md:372]` |

### 7.2 Gate anti-overfitting (go-live)

- **NFR-2 (NFR-DSR) — DSR positivo significativo come gate primario.** Il bundle candidato deve avere $DSR>\theta_{DSR}$ ($\theta_{DSR}=0{,}95$ valore di lavoro provvisorio, non congelato). *Valore di prodotto*: prova che la performance non è frutto del numero di prove condotte. *Origine*: `[DOC-INTERNO CAP_07_parte_VII.md:570]` (AC-GO-1).
- **NFR-3 (NFR-PBO) — PBO sotto soglia come gate di fragilità.** $PBO<\theta_{PBO}$ ($\theta_{PBO}=0{,}50$ provvisorio). *Valore di prodotto*: prova che la scelta del bundle non dipende fragilmente dalla partizione dei dati. *Origine*: `[DOC-INTERNO CAP_07_parte_VII.md:572]` (AC-GO-2).
- **NFR-4 — Lifecycle stabile cross-regime.** Target hit / executable rate stabili e comparabili fra regime calmo e turbolento; bootstrap stazionario ($B=2000$) per gli intervalli di confidenza. *Valore di prodotto*: il prodotto è robusto al regime di mercato. *Origine*: `[DOC-INTERNO CAP_01_parte_I.md:85]`, `[DOC-INTERNO CAP_07_parte_VII.md:574]` (AC-GO-4).
- **NFR-5 — Filtro 80pt come pre-condizione di emissione.** L'80pt è gate di emissione, non parametro libero del GA. *Valore di prodotto*: nessun micro-segnale antieconomico pubblicato. *Origine*: `[DOC-INTERNO CAP_01_parte_I.md:83]`.

### 7.3 Checklist go-live come criteri di accettazione del prodotto

La checklist deterministica `AC-GO-1..AC-GO-12` di Cap.36 Parte VII `[DOC-INTERNO CAP_07_parte_VII.md:566]` è recepita come **criteri di accettazione del prodotto** (≤12 punti, tracciabili a Cap.36):

| # | Criterio di accettazione (vista prodotto) | Cap.36 |
|---|---|---|
| 1 | DSR primario superato ($>\theta_{DSR}$) | AC-GO-1 |
| 2 | PBO sotto soglia ($<\theta_{PBO}$) | AC-GO-2 |
| 3 | Expected net return positivo con IC bootstrap 95% > 0 | AC-GO-3 |
| 4 | Lifecycle stabile cross-regime ($|f_5^{global}|<\theta_{f_5}$) | AC-GO-4 |
| 5 | Stabilità cross-fold ($\text{IQR}_{norm}(f_1)<\theta_{IQR}$) | AC-GO-5 |
| 6 | Qualità informativa target_2 ($\pi_{t_2\mid t_1}$ sopra soglia) | AC-GO-6 |
| 7 | Max drawdown intraday entro limite ($<\theta_{MDD}=200$ pt) | AC-GO-7 |
| 8 | Frequenza emissione entro range operativo | AC-GO-8 |
| 9 | Target operativo asimmetrico raggiunto (500 pt/g OR 70% strutturale) sopra soglia sessioni | AC-GO-9 |
| 10 | Pipeline di inference operativa (incl. latenza Telegram qualitativa, M-2) | AC-GO-10 |
| 11 | Dashboard di monitoraggio live attiva | AC-GO-11 |
| 12 | Hash bundle frozen valido al caricamento | AC-GO-12 |

> **M-16 condizionale — metadato del bundle frozen, NON riaperto.** L'eventuale attivazione dei Cox time-varying coefficients è registrata come metadato `cox_time_varying_active` $\in\{$True, False$\}$ del bundle frozen (Cap.35.1 elemento 6), con regola di decisione in Cap.31.3 dipendente dall'esito del walk-forward del ciclo di re-training successivo `[DOC-INTERNO tasks/CARRYOVER.md:36]`. SPEC-FUNZ-01 lo recepisce come requisito metodologico già normativo, **non lo riapre**.

**Out-of-scope Sezione 7**: formule di DSR / PBO / CSCV / bootstrap (Cap.32-34 Parte VII); valori congelati delle soglie $\theta_*$ (rimasti non congelati, ricalibrati post-go-live).

| Requisito ID | Capitolo metodologia v2 | Tipo |
|---|---|---|
| NFR-2 | Cap.32 Parte VII, Cap.36 Parte VII | NFR |
| NFR-3 | Cap.33 Parte VII, Cap.36 Parte VII | NFR |
| NFR-4 | Cap.34 Parte VII, Cap.5 Parte I | NFR |
| NFR-5 | Cap.5 Parte I | NFR |

---

## Sezione 8 — Vincoli normativi e compliance

### 8.1 Posizionamento di compliance

- **CN-3 — Segnale informativo, non consulenza, non esecuzione automatica.** Il prodotto è un servizio di **segnalazione informativa**; non è consulenza in materia di investimenti e non esegue ordini automaticamente. Coerente con il profilo retail MiFID II e con il vincolo strutturale "solo emissione". *Valore di prodotto*: posizionamento mostrabile a un consulente legale MiFID II `[WIKI-HINT, da verificare]`; ancoraggio interno `[DOC-INTERNO CAP_01_parte_I.md:23]`, `[DOC-INTERNO CAP_01_parte_I.md:15]`.
- **CN-4 — Separazione segnale / esecuzione ordini.** La pipeline non apre mai la porta di trading del broker (porta 10002 DAPI mai aperta); solo emissione via Telegram. *Valore di prodotto*: separazione netta fra il servizio e l'ordering, riducibile a clausola contrattuale. *Origine*: `[DOC-INTERNO CAP_09_parte_9.md:39]` (D-9-2).

### 8.2 Audit log e retention

- **CN-5 — Audit log e retention.** Audit log JSON Lines append-only; retention minima **90 giorni rolling** + **retention permanente sui giorni di emissione segnale** (log che contengono `SIGNAL_EMITTED` / `SIGNAL_TRIGGERED` o uno dei 6 terminali). *Valore di prodotto*: tracciabilità per compliance interna e replay deterministico di qualunque segnale emesso. *Origine*: `[DOC-INTERNO CAP_09_parte_9.md:362]` (Gap-4 / D-9-15).

Catalogo eventi loggati, elencato per riferimento (non ridichiarato): `HANDSHAKE`, `SUB`/`UNSUB`, `SESSION_OPEN`/`SESSION_CLOSE`, `WARMUP_COMPLETE`, `RUNTIME_GAP_*`, `RUNTIME_DEGRADED`, `RUNTIME_STALE_RESTART`, `CONTRACT_SWITCH`, gli 8 marker `SIGNAL_*` (emesso, triggered, 6 terminali), `GATING_RULE_APPLIED`/`REJECTED` `[DOC-INTERNO CAP_09_parte_9.md:353]`.

### 8.3 Privacy / GDPR (dichiarazione minima)

- **CN-6 — Minimizzazione PII.** Il prodotto non raccoglie PII dell'operatore oltre il `chat_id` Telegram e l'account code Directa locale; l'account code è trattato come dato sensibile (mascherabile negli export pubblici dell'audit, in chiaro solo nel log locale per il replay). *Valore di prodotto*: superficie privacy minima, dettagli a FASE-D. *Origine*: `[DOC-INTERNO CAP_09_parte_9.md:43]` (Gap-1), `[DOC-INTERNO CAP_09_parte_9.md:358]`.

### 8.4 Gating qualitativo cash europei (compliance / risk)

- **CN-7 — Gating qualitativo cash europei configurabile, fuori dal GA.** Gli indici cash europei (DGER/DSTX50/DITAS/DFRA) sono usati come **gating qualitativo configurabile post-emissione** (annotazione del messaggio Telegram), mai come feature del GA: il gating può aggiungere una nota di avvertimento, **non** sopprime l'emissione né altera il ranking dei cromosomi. *Valore di prodotto*: layer di risk informativo modificabile senza re-training. *Origine*: `[DOC-INTERNO CAP_09_parte_9.md:308]` (Q-A-3, D-9-14).

**Out-of-scope Sezione 8**: parere legale formale e testo dei disclaimer (materia di consulente legale esterno); formato esatto del log (Cap.54 Parte 9 lo definisce, qui solo riferito).

| Requisito ID | Capitolo metodologia v2 | Tipo |
|---|---|---|
| CN-3 | Cap.2 Parte I, Cap.1 Parte I | CN |
| CN-4 | Cap.46 Parte 9 (D-9-2) | CN |
| CN-5 | Cap.54 Parte 9 (D-9-15) | CN |
| CN-6 | Cap.46 Parte 9 (Gap-1) | CN |
| CN-7 | Cap.53 Parte 9 (Q-A-3) | CN |

---

## Sezione 9 — Requisiti di dato e dipendenze infrastrutturali

### 9.1 Tabella dipendenze infrastrutturali

| Dipendenza | Ruolo nel prodotto | Vincolo / nota | Origine v2 |
|---|---|---|---|
| **Directa DAPI** | canale runtime esclusivo del FIB; porte 10001 (realtime) / 10003 (storico) | porta 10002 (trading) mai aperta; uso esclusivo del canale (D-6) | `[DOC-INTERNO CAP_09_parte_9.md:35]`, `[DOC-INTERNO CAP_09_parte_9.md:45]` |
| **Portara/CQG** | storico training: FIB pieno back-adjusted (ratio-adjusted) | unica fonte ufficiale di training; no MIB cash; 5+ anni 1-min | `[DOC-INTERNO CAP_08_parte_8.md:13]` |
| **AWS spot c5.4xlarge** | training GA (cloud) | budget ~45-75 EUR/ciclo; retraining trimestrale/semestrale | `[DOC-INTERNO CAP_01_parte_I.md:63]` |
| **PC i5-7200U** | sviluppo + inference live | inference leggera (secondi/segnale); training non in locale | `[DOC-INTERNO CAP_01_parte_I.md:61]` |
| **Bot Telegram** | canale di consegna segnali | bot personale già attivo; setup Appendice E | `[DOC-INTERNO CAP_01_parte_I.md:47]` |
| **Cash europei (gating)** | DGER/DSTX50/DITAS/DFRA come gating qualitativo | market data DAPI gratuito; NON feature GA (Q-A-3) | `[DOC-INTERNO CAP_09_parte_9.md:77]`, `[DOC-INTERNO CAP_09_parte_9.md:308]` |

### 9.2 Invariante research = runtime e feed runtime

L'invariante **research = runtime** è esteso dall'adapter DAPI → bundle frozen Portara `[DOC-INTERNO CAP_09_parte_9.md:153]` fino all'intero ciclo di vita del tape `[DOC-INTERNO CAP_10_parte_10.md:11]`. Il feed runtime FIB è ricostruito dal `BOOK_5` (i futures IDEM non espongono `PRICE`) `[DOC-INTERNO CAP_09_parte_9.md:73]`; il feed cash usa `PRICE` (schema realtime `f4=last`/`f6=volume_cum`/`f8=day_low`/`f9=day_high`, M-9 `[DOC-INTERNO CAP_09_parte_9.md:94]`).

### 9.3 Tape archiviato e backfill

- **R-20 — Tape archiviato in formato runtime esteso (13 campi) + manifest JSON.** L'archivio del tape DAPI usa l'header CSV runtime esteso a **13 campi** (`symbol, timeframe, timestamp, date, time, open, high, low, close, volume, tick_count, bar_synthetic, source`), **distinto** dal legacy CSV a **11 campi** (`[CODICE-ESISTENTE scripts/export_directa_history_parametric.py:605-617]`, senza `tick_count`/`bar_synthetic`); manifest JSON esteso con `reconcile_status`, `bar_counts_by_source`, `gap_log`. *Valore di prodotto*: il tape archiviato è simmetrico al bundle di training e auditabile. *Origine*: `[DOC-INTERNO CAP_10_parte_10.md:185]`, `[DOC-INTERNO CAP_09_parte_9.md:117]`.
- **R-21 — Immutabilità delle barre storicizzate.** Le barre archiviate sono immutabili (perimetro empirico T+3 morning) con versioning append-only per i recuperi retroattivi; il tape archiviato **non è fonte di training**. *Valore di prodotto*: replay deterministico bit-exact e integrità storica. *Origine*: `[DOC-INTERNO CAP_10_parte_10.md:255]` (D-10-8), `[DOC-INTERNO CAP_10_parte_10.md:256]` (D-10-9).
- **R-22 — Backfill gap entro 100gg + fallback Portara oltre.** Recupero gap via `CANDLERANGE` entro ~100 giorni (limite DAPI `[CODICE-ESISTENTE scripts/export_directa_history_parametric.py:61]` `DEFAULT_INTRADAY_MAX_DAYS=100`), fallback Portara oltre, con re-warm-up obbligatorio. *Valore di prodotto*: continuità del tape senza buchi che contaminerebbero le feature. *Origine*: `[DOC-INTERNO CAP_10_parte_10.md:74]` (Cap.59), `[DOC-INTERNO CAP_10_parte_10.md:151]` (Cap.61).

### 9.4 Riconciliazione canonica giornaliera (gate bloccante)

- **R-23 — Riconciliazione canonica giornaliera come gate bloccante.** Gate operativo end-of-day che, su esito `RECONCILE_DIVERGENT_*`, **blocca l'emissione della sessione $d+1$** fino a intervento supervisore; procedura non-mutativa (solo marker, non modifica i prezzi). È distinto dal **monitoraggio non-bloccante** di Parte VI Cap.30. Il low/high cash giornaliero è preso dalla CANDLE ufficiale (`f8`/`f9`), mai dal tick realtime rado. *Valore di prodotto*: protezione contro la deriva silenziosa del feed prima che inquini i segnali. *Origine*: `[DOC-INTERNO CAP_10_parte_10.md:250]` (D-10-3), `[DOC-INTERNO CAP_10_parte_10.md:251]` (D-10-4).

### 9.5 Restart e warm-up

- **R-24 — Warm-up stati condizionali $L_{warmup}=30$ giorni.** Al boot / post-restart, warm-up di 30 giorni di trading IDEM congelato per gli stati condizionali (EGARCH cross-session, normalizzazioni). *Valore di prodotto*: il primo segnale dopo un restart non è prodotto su stati non stabilizzati. *Origine*: `[DOC-INTERNO CAP_09_parte_9.md:435]` (D-9-NB4), `[DOC-INTERNO CAP_10_parte_10.md:252]` (D-10-5).

**Out-of-scope Sezione 9**: dettagli di implementazione FASE-D (codice, microservizi, framework); scelta esatta dell'instance type AWS (Cap.4 ha fissato c5.4xlarge come riferimento); contratto commerciale con i vendor; calibrazione fine di $\theta_{reconcile}$ (FASE-D).

| Requisito ID | Capitolo metodologia v2 | Tipo |
|---|---|---|
| R-20 | Cap.62 Parte 10, Cap.48 Parte 9 | R |
| R-21 | Cap.62 Parte 10 (D-10-8/9), Cap.65 Parte 10 | R |
| R-22 | Cap.59 Parte 10, Cap.61 Parte 10 | R |
| R-23 | Cap.60 Parte 10 (D-10-3/4) | R |
| R-24 | Cap.51 Parte 9 (D-9-NB4), Cap.61 Parte 10 | R |

---

## Sezione 10 — Fasizzazione, roadmap, tracciabilità

### 10.1 Fasizzazione

- **PHASE-1 FIB-only** = oggetto di SPEC-FUNZ-01 corrente.
- **PHASE-2 cross-index** (DAX/EuroStoxx50/ES/MES) = **fuori scope**, rinviata a SPEC-FUNZ-02 o equivalente futuro (non definito qui) `[DOC-INTERNO CAP_08_parte_8.md:167]`, `[DOC-INTERNO CAP_09_parte_9.md:391]`, `[DOC-INTERNO CAP_10_parte_10.md:226]`.

### 10.2 Ponte verso FASE-D

SPEC-FUNZ-01 fornisce la **base requisiti** per la successiva FASE-D di implementazione (codice runtime; pipeline ingest-feature-inference-publish; pipeline training cloud; pipeline backfill / riconciliazione / archiviazione; bot Telegram; audit log). **FASE-D è fuori scope** di SPEC-FUNZ-01.

### 10.3 Dipendenze aperte FASE-D (≥5 voci)

1. **M-2 — verifica empirica latenza Telegram** ($L_{max}=30$ s contro bot reale) → Appendice E / FASE-D `[DOC-INTERNO tasks/CARRYOVER.md:21]`.
2. **Calibrazione fine $\theta_{reconcile}$** (Cap.60) → FASE-D `[DOC-INTERNO CAP_10_parte_10.md:232]` (D-10-10).
3. **Migrazione legacy→esteso del tape** (11→13 campi, ~391 dump) → operazione una-tantum FASE-D `[DOC-INTERNO CAP_10_parte_10.md:230]`.
4. **Codici 1030 e riavvio Darwin mezzanotte** (Empirico-CLI residuo) → sessione CLI / FASE-D `[DOC-INTERNO CAP_10_parte_10.md:234]`.
5. **Lookup completa codici mese Directa-IDEM** oltre `F`/`I` → runtime-discovery via ANAG, FASE-D `[DOC-INTERNO CAP_09_parte_9.md:389]`.
6. **Implementazione codice operativo della pipeline runtime** (parser DAPI, adapter, recovery, audit, gating) → FASE-D `[DOC-INTERNO CAP_09_parte_9.md:406]`.

### 10.4 Matrice di tracciabilità requisito → capitolo metodologia v2

| Requisito ID | Sezione SPEC | Capitolo metodologia v2 | Note |
|---|---|---|---|
| R-1 | 1 | Cap.1 Parte I, Cap.6 Parte II | emissione segnali strutturati |
| R-2 | 1 | Cap.1 Parte I | esecuzione delegata |
| R-3 | 1 | Cap.42 Parte 8 | FIB-only PHASE-1 |
| CN-1 | 1 | Cap.1 Parte I | "solo emissione" non negoziabile |
| R-4 | 2 | Cap.2 Parte I, Cap.29 Parte VI | esecuzione manuale mobile |
| R-5 | 2 | Cap.3 Parte I, Cap.29 Parte VI | canale Telegram obbligatorio |
| R-6 | 3 | Cap.6 Parte II | payload immutabile |
| R-7 | 3 | Cap.6 Parte II, Cap.28 Parte VI | segnale unico attivo |
| R-8 | 3 | Cap.5 Parte I, Cap.8 Parte II | filtro 80pt |
| R-9 | 3 | Cap.6 Parte II | tick discreto 5pt |
| R-10 | 4 | Cap.7 Parte II, Cap.29 Parte VI | notifica trigger_event |
| R-11 | 4 | Cap.11 Parte II | segnale vs position lifecycle |
| CN-2 | 4 | Cap.7 Parte II, Cap.54 Parte 9 | marker normativi terminali |
| NFR-1 | 5 | Cap.9 Parte II, Cap.31 Parte VII | latenza $L_{max}=30$ s (M-2 open) |
| R-12 | 5 | Cap.9 Parte II | anti-duplicato |
| R-13 | 5 | Cap.9 Parte II, Cap.6 Parte II | nuovo messaggio per nuovo signal_id |
| R-14 | 5 | Cap.9 Parte II, Cap.29 Parte VI | notifica trigger separata |
| R-15 | 6 | Cap.1 Parte I, Cap.52 Parte 9 | sessione 8-22 CET |
| R-16 | 6 | Cap.2 Parte I | sizing 1 contratto |
| R-17 | 6 | Cap.6 Parte II, Cap.28 Parte VI | singolo segnale attivo |
| R-18 | 6 | Cap.2 Parte I, Cap.5 Parte I | commissioni 5 EUR/op |
| R-19 | 6 | Cap.56 Parte 9 (D-9-NB2) | rollover / contract switch |
| NFR-2 | 7 | Cap.32 Parte VII, Cap.36 Parte VII | DSR gate primario |
| NFR-3 | 7 | Cap.33 Parte VII, Cap.36 Parte VII | PBO gate fragilità |
| NFR-4 | 7 | Cap.34 Parte VII, Cap.5 Parte I | lifecycle stabile cross-regime |
| NFR-5 | 7 | Cap.5 Parte I | 80pt pre-condizione emissione |
| CN-3 | 8 | Cap.2 Parte I, Cap.1 Parte I | segnale informativo MiFID II |
| CN-4 | 8 | Cap.46 Parte 9 (D-9-2) | separazione segnale/esecuzione |
| CN-5 | 8 | Cap.54 Parte 9 (D-9-15) | audit log + retention |
| CN-6 | 8 | Cap.46 Parte 9 (Gap-1) | minimizzazione PII |
| CN-7 | 8 | Cap.53 Parte 9 (Q-A-3) | gating qualitativo cash |
| R-20 | 9 | Cap.62 Parte 10, Cap.48 Parte 9 | tape esteso 13 campi |
| R-21 | 9 | Cap.62 Parte 10, Cap.65 Parte 10 | immutabilità tape |
| R-22 | 9 | Cap.59 Parte 10, Cap.61 Parte 10 | backfill 100gg + fallback |
| R-23 | 9 | Cap.60 Parte 10 (D-10-3/4) | riconciliazione gate bloccante |
| R-24 | 9 | Cap.51 Parte 9, Cap.61 Parte 10 | warm-up $L_{warmup}=30$gg |

Totale tracciato: **36 requisiti** = 24 `R` (R-1..R-24) + 5 `NFR` (NFR-1..NFR-5) + 7 `CN` (CN-1..CN-7), corrispondenti alle **36 righe** della matrice sopra (≥30, AC-G5 OK). Ogni requisito ha colonna "capitolo metodologia v2" non vuota (AC-G4) e valore operativo dichiarato nella sezione di origine (AC-G7).

### 10.5 Capitoli metodologia v2 non tracciati e motivazione

I capitoli seguenti **non** compaiono in matrice perché fuori dalla vista operatore/prodotto (implementazione metodologica interna, opaca al consumatore). L'esclusione è esplicita e motivata:

| Capitoli | Parte | Motivazione di esclusione |
|---|---|---|
| Cap.4 | I | Compute budget / strategia cloud: citato come dipendenza infrastrutturale (Sez. 9, AWS) ma il dettaglio di budget/instance è materia interna, non requisito di prodotto. |
| Cap.12 | III | Definizioni di rendimento e scala temporale: matematica interna del backtest, opaca al consumatore. |
| Cap.13 | III | Modello EGARCH di volatilità condizionata: implementazione metodologica interna. |
| Cap.14 | III | Stato di regime intraday: feature interna del modello, non vista dall'operatore. |
| Cap.15 | III | Feature engineering causale / pivot detection: catalogo interno del modello. |
| Cap.16 | IV | Geometria delle zone di entry: derivazione strutturale interna (il prodotto pubblica il risultato, non l'algoritmo). |
| Cap.17 | IV | Derivazione target strutturali: matematica interna (output in R-1/payload). |
| Cap.18 | IV | Derivazione stop strutturali: matematica interna (output in payload). |
| Cap.19 | IV | Modello di survival (Cox cause-specific): implementazione metodologica interna. |
| Cap.20 | IV | Filtri di emissione survival-based: soglia interna del cromosoma. |
| Cap.21 | IV | Caso trade_range (geometria): derivazione interna; il vincolo 80pt è già in R-8. |
| Cap.22-26 | V | Cromosoma, operatori NSGA-II, fitness, walk-forward, popolazione: motore di ottimizzazione interno, opaco al consumatore (i suoi gate emergono in Sez. 7). |
| Cap.27 | VI | Pipeline di inference real-time: implementazione FASE-D (citata in AC-GO-10). |
| Cap.30 | VI | Monitoraggio del lifecycle / dashboard: strumento interno del committente (citato per contrasto col gate bloccante R-23). |
| Cap.35 | VII | Frozen bundle / hash: meccanismo interno (citato in AC-GO-12 e per M-16). |
| Cap.37-44 | 8 | Convenzione dati storici / back-adjustment / sanity validation: materia di training, citata in Sez. 9 (Portara) senza ridichiararla. |
| Cap.43 | 8 | Procedura di sanity validation: implementazione FASE-D, opaca al prodotto. |
| Cap.45, 50, 55, 57, 58, 63, 64 | 9-10 | Premesse, recovery errori, punti aperti, coerenza inter-temporale: dettagli interni di pipeline / metodologia, citati dove pertinenti (es. punti aperti in 10.3) senza requisito dedicato. |
| Cap.56, 65 | 9-10 | Tabelle decisioni: sono il **registro** delle decisioni che i requisiti tracciano puntualmente (D-9-*, D-10-*); non costituiscono requisito di prodotto a sé. |

I capitoli sostanziali della vista prodotto sono tutti tracciati: Cap.1-3, 5 (Parte I); Cap.6-11 (Parte II); Cap.32-34, 36 (Parte VII); Cap.46-54, 56 (Parte 9); Cap.48, 51, 59-62, 65 (Parte 10); Cap.28-29 (Parte VI); Cap.42 (Parte 8, fasizzazione).

**Out-of-scope Sezione 10 (quadro complessivo)**: PHASE-2 cross-index; implementazione FASE-D; consulenza legale; contratti commerciali con vendor; roadmap con date/milestone.

| Requisito ID | Capitolo metodologia v2 | Tipo |
|---|---|---|
| (matrice complessiva) | trasversale Cap.1-65 | R/NFR/CN |

---

## Appendice — Self-review del Developer (RM-1..RM-3 applicate al consolidamento)

Questa sezione è **opzionale e consigliata** dal task card (vincolo Developer v1): SPEC-FUNZ-01 nel suo insieme va a **Review formale piena** (opzione B di RM-4, gestita dall'Orchestratore). Non sostituisce la review; documenta la diligenza del consolidamento.

**(a) Natura delle asserzioni — RM-1.** SPEC-FUNZ-01 NON introduce dichiarazioni "verificato X" di prima istanza su sistemi esterni. Ogni asserzione fattuale è un **richiamo** a un CAP chiuso PASS, etichettato `[DOC-INTERNO <file>:<rif>]` o `[CODICE-ESISTENTE <path>:<linea>]`. Le uniche asserzioni con sapore empirico (schema CANDLE, codici mese `F`/`I`, schema PRICE/BOOK_5) sono richiami a fatti già chiusi negli audit RM CAP-DATA-02/03 e nel decoder di produzione, citati come tali. Nessun blocco 4-righe nuovo è dovuto (non si eseguono verifiche nuove).

**(b) Citazioni di codice — RM-2.** Le citazioni `[CODICE-ESISTENTE]` usate sono autoritative dal task card (eredità #15) e sono state **riverificate con Read** prima della stesura:
- `[CODICE-ESISTENTE scripts/export_directa_history_parametric.py:467-481]` — `parse_directa_candle`, schema CANDLE `C;L;H;O` (`kind, symbol, ymd, hms, uff, min_, max_, ape, qty = parts[:9]`; commento r477 `# UFF, MIN, MAX, APE => close, low, high, open`). CONFERMATO token-per-token.
- `[CODICE-ESISTENTE scripts/export_directa_history_parametric.py:605-617]` — header CSV legacy 11 campi (`symbol, timeframe, timestamp, date, time, open, high, low, close, volume, source`, senza `tick_count`/`bar_synthetic`). CONFERMATO token-per-token.
- `[CODICE-ESISTENTE scripts/export_directa_history_parametric.py:61]` — `DEFAULT_INTRADAY_MAX_DAYS = 100`. CONFERMATO (citato da Cap.59 Parte 10, eredità #15; non riletto qui ma autoritativo dal task card e da `[DOC-INTERNO CAP_10_parte_10.md:230]`).
Nessun decoder è stato riscritto né scoperto ex novo (la spec non produce codice). Citazioni codice totali: 3 distinte (≤5, AC-G3).

**(c) Fonti esterne — RM-3.** I riferimenti a MiFID II, wiki Directa, Telegram, Portara/CQG sono etichettati `[WIKI-HINT, da verificare]` e non sono mai fonte unica di un'asserzione strutturale: ogni asserzione strutturale poggia su almeno una fonte livello 1/2/3 nei CAP chiusi. La wiki Directa è citata solo con l'avvertenza esplicita di inaffidabilità sullo schema CANDLE (nota di lettura in testa).

**(d) Assunzioni usate come premesse (non verificate qui, autoritative dal task card / CAP chiusi).** Tutte le eredità #1-25 del task card sono assunte autoritative (input dell'Orchestratore già verificato): non sono ri-verificate. In particolare: stato 10/10 Parti PASS, M-2 unico M-promemoria di capitolo OPEN, schemi DAPI chiusi negli audit RM, valori numerici ($L_{max}=30$ s, 80pt, $b_{min}=5$, $L_{warmup}=30$gg, tick 5pt, sessione 8-22 CET, retention 90gg, 5 EUR/op) tutti ereditati.

**(e) File del repo letti durante il consolidamento (a riprova di RM-2).** `tasks/METODO.md`, `.claude/agents/developer.md`, `tasks/ACTIVE_TASK.md`, `tasks/CARRYOVER.md`, `docs/methodology_v2/00_indice.md`, `CAP_01_parte_I.md`, `CAP_02_parte_II.md`, `CAP_03_parte_III.md` (headers), `CAP_04_parte_IV.md` (Cap.16-21 headers + righe chiave), `CAP_06_parte_VI.md` (Cap.27-30), `CAP_07_parte_VII.md` (Cap.31, Cap.36), `CAP_08_parte_8.md` (Cap.37-44), `CAP_09_parte_9.md` (Cap.46-56), `CAP_10_parte_10.md` (Cap.57-65), `scripts/export_directa_history_parametric.py:465-484,603-620`.

---

*SPEC-FUNZ-01 — fine documento. PHASE-1 FIB-only. Ponte metodologia v2 (chiusa) → FASE-D (implementazione).*
