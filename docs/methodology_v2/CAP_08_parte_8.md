# Parte 8 — Convenzione dati storici e politica di rollover

Documento metodologico v2 — Motore genetico strutturale per segnali FIB. La Parte 8 formalizza la convenzione normativa dei dati storici utilizzati per il training del motore genetico, la politica di rollover del contratto FIB e la gestione della griglia temporale 1-minuto. La Parte si colloca in coda al corpo principale del documento, immediatamente prima della Parte 9 (Appendici operative); non rinumera le Parti precedenti (I-VII) e non introduce modifiche alle decisioni gia' ratificate in quelle Parti. Eventuali deviazioni da questa convenzione in fasi successive del progetto richiedono ritorno al Planner.

La Parte 8 eredita gli invarianti metodologici dichiarati nelle Parti I-VII e li applica alla dimensione dati: in particolare l'invariante `research semantics = runtime semantics` (Parte I, Capitolo 1), la gap semantics e la regola deterministica di fill virtuale (Parte II, Capitolo 7; Parte III, Capitolo 12), il protocollo walk-forward nested con purge ed embargo (Parte V, Capitolo 25), la fonte canonica del replay e dell'OOS aggregata (Parte II, Capitolo 10; Parte VII, Capitolo 31). La fasizzazione del progetto in PHASE-1 (FIB-only) e PHASE-2 (cross-index) e' dichiarata esplicitamente come scelta documentale: PHASE-1 e' una istanziazione parziale della convenzione, con costi noti, non una semplificazione silenziosa.

La Parte 8 si compone di otto capitoli normativi (Cap.37-44), ciascuno dedicato a una decisione di convenzione dati con razionale documentato, regola operativa e criterio di rollback registrato nel report supervisore `reports/REPORT_CAP_08.md`.

---

## Capitolo 37 — Scelta della serie ufficiale di training

La serie storica ufficiale per il training del motore genetico sullo strumento target e' la serie FIB pieno back-adjusted di Portara/CQG, con back-adjustment di tipo ratio-adjusted ricostruito in preprocessing (vedi Cap.38 per le tre serie derivabili e le loro convenzioni d'uso). Non sono ammesse fonti alternative per la calibrazione dei modelli probabilistici del documento metodologico v2; le esclusioni esplicite sono congelate in Cap.44.

**Razionale dell'equivalenza FIB pieno / miniFIB.** Il contratto FIB pieno e il contratto miniFIB sul mercato IDEM di Borsa Italiana condividono il medesimo sottostante (indice FTSE MIB), il medesimo tick (5 punti indice), il medesimo exchange e la medesima sessione operativa. Le strutture di volatilita' condizionata e i rendimenti log a 1-minuto delle due serie sono numericamente equivalenti: differiscono esclusivamente per il moltiplicatore monetario (5 EUR/punto per il FIB pieno, 1 EUR/punto per il miniFIB; vedi Parte I, Capitolo 2). L'esecuzione operativa dell'operatore avviene su miniFIB ma la calibrazione del modello su FIB pieno e' metodologicamente equivalente: il moltiplicatore monetario interviene solo nella conversione finale del PnL in EUR e nel calcolo dell'impatto delle commissioni (Parte I, Capitolo 5, dove $c = 1$ punto FIB equivalente per operazione e' invariante per moltiplicatore). L'invariante `research semantics = runtime semantics` (Parte I, Capitolo 1) e' rispettato: la serie su cui il GA calibra e' la stessa famiglia di strumento su cui l'operatore esegue.

**Razionale della scelta di FIB pieno come fonte ufficiale.** Il FIB pieno ha storia di liquidita' piu' profonda e continua del miniFIB nell'intero periodo 1995-oggi: il miniFIB e' stato introdotto solo nel 2000 mentre il FIB pieno e' negoziato dal lancio del mercato IDEM nel novembre 1994 (vedi Cap.41 per la timeline storica). La maggior profondita' temporale del FIB pieno consente al GA di operare su una finestra di training piu' estesa, con maggiore copertura di regimi storici e di shock di volatilita'. Inoltre il volume realmente osservato sul FIB pieno e' superiore al miniFIB su gran parte della finestra storica, riducendo l'incidenza di barre 1-minuto senza trade (vedi Cap.40 sulla regolarizzazione della griglia).

**Esclusione esplicita di MIB cash come fonte training.** L'indice MIB cash (FTSE MIB cash) non e' ammesso come fonte training. Il razionale e' ancorato all'invariante `research semantics = runtime semantics` (Parte I, Capitolo 1): l'indice cash differisce dal contratto futures su orari di calcolo (l'indice cash e' calcolato sulla sessione delle azioni componenti, che non coincide con la sessione FIB), microstruttura (sul cash non c'e' un single ticker negoziabile, l'indice e' calcolato per aggregazione), basis (il prezzo del futures differisce dal cash per cost-of-carry e dividendi attesi), gap di apertura (il cash apre con prezzi di asta delle singole azioni, mentre il futures e' negoziato in continua dall'inizio della sessione IDEM). La calibrazione su cash produrrebbe parametri EGARCH e quantili condizionali numericamente distinti da quelli necessari al runtime sul futures; il segnale prodotto dal motore non sarebbe coerente con la microstruttura dello strumento di esecuzione. La regola di esclusione vale per tutta la pipeline del modello: nessun layer (volatilita', regime, survival, feature engineering) puo' essere calibrato su cash. Per ulteriore generalizzazione dell'esclusione di fonti alternative vedi Cap.44.

**Coerenza con il successo operativo del motore.** La definizione operativa di successo del motore in Parte I Capitolo 5 prevede metriche calcolate su rendimenti netti in punti FIB e su replay deterministico della state machine del segnale. Il replay e' eseguito sulla serie ufficiale di training: la coerenza fra serie training, serie OOS e serie runtime e' condizione necessaria perche' la metrica primaria $E[R_{net} \mid executed]$ misurata in validazione sia un'approssimazione valida dell'attesa operativa.

---

## Capitolo 38 — Convenzione di back-adjustment ufficiale

Dal file Portara grezzo (campi disponibili: `Date, Time, O, H, L, C, V, TickCount, ContractName, UnadjustedClose, RollSpread, CumulativeSpread` + roll log allegato, vedi Parte I Capitolo 3) sono ricostruite in preprocessing tre serie distinte, ciascuna con uso normativo specifico nel documento metodologico v2.

| Serie | Definizione | Uso normativo |
|-------|-------------|---------------|
| Ratio-adjusted (**ufficiale per training**) | $P_t = P_t^{\text{unadj}} \cdot \prod_{r \in \text{rolls}, r < t} \dfrac{P_r^{\text{next}}}{P_r^{\text{curr}}}$ | Input a tutti i modelli che operano su rendimenti log: EGARCH (Parte III, Capitolo 13), classificazione di regime (Parte III, Capitolo 14), feature engineering (Parte III, Capitolo 15), survival Cox cause-specific (Parte IV, Capitolo 19). |
| Panama-additive (**ufficiale per audit monetario**) | Fornita direttamente da Portara come `back-adjusted settle` (additivo, somma cumulata degli spread di roll). | Audit del PnL in EUR/punto, sanity check visivo del segnale, replay di controllo. Non entra nei modelli probabilistici. |
| Unadjusted concatenata | Sequenza riga per riga di `UnadjustedClose` con marker di roll, senza adjustment. | Sanity check contratto-per-contratto, validazione su finestra recente (Cap.43). |

**Formula della serie ratio-adjusted.** Sia $\text{rolls} = \{r_1, r_2, \ldots, r_K\}$ l'insieme delle date di rollover ordinate cronologicamente. Per ciascuna data di roll $r_k$, indichiamo con $P_{r_k}^{\text{curr}}$ il prezzo di chiusura del contratto front-month nell'ultima barra di trading prima del roll (giorno $r_k - 1$) e con $P_{r_k}^{\text{next}}$ il prezzo di chiusura del contratto next-month nella stessa barra temporale. Il fattore di adjustment per il roll $r_k$ e' quindi $\rho_k = P_{r_k}^{\text{next}} / P_{r_k}^{\text{curr}}$. La serie ratio-adjusted alla barra $t$ e':

$$P_t = P_t^{\text{unadj}} \cdot \prod_{k : r_k < t} \rho_k$$

dove il prodotto e' esteso a tutti i roll precedenti l'istante $t$. La serie cosi' ricostruita e' continua, priva di salti meccanici di basis ai roll, e i rendimenti log $r_t = \log(P_t / P_{t-1})$ coincidono al di fuori dei roll con i rendimenti log della serie unadjusted (essendo $\rho_k$ una costante moltiplicativa per ogni segmento fra due roll consecutivi). Alla barra esatta del roll il rendimento log della serie ratio-adjusted e' nullo per convenzione: il roll non genera un rendimento osservabile sulla serie continua, dato che il salto e' assorbito dal fattore $\rho_k$.

**Ricostruzione in preprocessing.** Portara fornisce nativamente la serie Panama-additive (back-adjusted settle), non la ratio-adjusted. Il preprocessor del progetto ricostruisce la ratio-adjusted partendo dal file grezzo Portara, utilizzando le tre colonne `UnadjustedClose`, `RollSpread` (lo spread `next - curr` alla data di roll, nelle unita' di prezzo del FIB) e il roll log allegato (che lista date e contratti). La ricostruzione e' deterministica: dato il file Portara, la serie ratio-adjusted e' univocamente determinata.

**Uso specifico delle tre serie.**

- La serie **ratio-adjusted** entra come input nei modelli che richiedono rendimenti log su scala relativa, in particolare nella media e nella varianza condizionate di EGARCH (Parte III, Capitolo 13.3, dove la calibrazione MLE su finestra rolling $W=210.000$ fold-per-fold richiede coerenza nella scala dei rendimenti) e nelle feature di volatilita' del catalogo (Parte III, Capitolo 15.2). Il modello di survival Cox cause-specific (Parte IV, Capitolo 19) e' consumer indiretto della serie ratio-adjusted via il catalogo feature.

- La serie **Panama-additive** entra come input nell'audit del PnL in EUR/punto: il replay deterministico (Parte II, Capitolo 10) ricostruisce sulla serie Panama il valore monetario delle posizioni eseguite e dei target raggiunti, in coerenza con il fatto che il moltiplicatore del FIB e' 5 EUR/punto sulla scala originale dei prezzi (Parte I, Capitolo 2). La serie Panama non entra nei modelli probabilistici perche' i suoi rendimenti log non sono coerenti con il payoff economico per scala (gli spread additivi distorcono la varianza relativa).

- La serie **unadjusted concatenata** serve esclusivamente per il sanity check di Cap.43: il confronto della distribuzione dei rendimenti log e dell'autocorrelazione fra ratio-adjusted e unadjusted-stitched permette di verificare che il back-adjustment non abbia introdotto artefatti di distribuzione significativi rispetto alla serie naturale dei contratti.

**Coerenza con la fonte canonica delle metriche (Parte VII Capitolo 31.1).** Le metriche OOS aggregate del documento metodologico v2 (Parte VII, Capitolo 31.1) sono calcolate sul log di replay bit-exact (Parte II, Capitolo 10). Il replay e' eseguito sulla serie ratio-adjusted per la valutazione del segnale e sulla serie Panama per la conversione del PnL in EUR. La coerenza fra le due serie nelle barre non di roll e' garantita dal fatto che entrambe derivano dallo stesso file Portara grezzo e dallo stesso roll log: la differenza fra rendimento log ratio-adjusted e rendimento log Panama nelle barre non di roll e' di ordine zero (entrambe le serie coincidono in scala relativa al netto del salto di roll, assorbito in modo equivalente dai due metodi).

---

## Capitolo 39 — Filtro pre-expiry e gestione rollover

Il filtro pre-expiry rimuove dal training set le ultime $N$ giorni di trading prima della scadenza di ciascun contratto. Il valore di lavoro normativo e' $N = 3$ giorni di trading, allineato alla roll rule default di Portara (3 giorni di trading prima della scadenza). Il valore $N=3$ e' valore di lavoro non congelato: la conferma definitiva e' rinviata a CAP-DATA-02 (richiesta tecnica a Portara per chiarire se i 3 giorni sono giorni di calendario o giorni di trading; in mancanza di conferma il preprocessor assume giorni di trading). Se Portara confermasse una roll rule diversa, l'aggiornamento di $N$ sarebbe minore (non richiede ritorno al Planner per quanto riguarda la struttura della Parte 8, vedi `reports/REPORT_CAP_08.md` rollback criteria).

**Razionale documentato.** Nelle ultime giornate prima della scadenza il basis fra contratto front e contratto next-month diverge meccanicamente: i partecipanti spostano la liquidita' dal front al next, il volume sul front decade, e lo spread relativo fra i due contratti varia in modo strutturale per effetto del cost-of-carry residuo. Su finestra di 1-3 giorni prima della scadenza, i rendimenti log del front-month osservato (e quindi della serie unadjusted, e indirettamente della serie ratio-adjusted nelle barre subito precedenti il roll) sono contaminati da questo effetto: i quantili condizionali stimati da modelli probabilistici e la dinamica dei residui EGARCH diventano strutturalmente meno informativi. Il filtro pre-expiry elimina la finestra in cui la serie back-adjusted e' strutturalmente meno informativa, garantendo che il training calibri i modelli su una finestra di osservazioni rappresentativa del regime di negoziazione normale.

**Algoritmo formale.** Sia $\text{roll\_log} = \{(c_k, e_k, r_k)\}_{k=1}^{K}$ la sequenza dei record di roll, dove $c_k$ identifica il contratto $k$-esimo, $e_k$ la sua data di scadenza ed $r_k$ la sua data di roll (definita come la data in cui il preprocessor sposta la "frontness" sul contratto successivo). Sia $\mathrm{trading\_day}(d, -N)$ la funzione che, data la data $d$ del calendario di trading IDEM, restituisce la data del giorno di trading $N$ posizioni prima (esclude weekend e festivita' IDEM). Il filtro pre-expiry esclude dal training set tutte le barre con:

$$\text{bar\_time} \in \left[ \mathrm{trading\_day}(r_k, -N),\; r_k \right] \quad \text{per ogni } k = 1, \ldots, K$$

L'esclusione e' applicata barra per barra dal preprocessor. Il numero di barre escluse per ciascun contratto e' approssimativamente $N \cdot 840$ (barre 1-minuto della sessione FIB attuale), variabile a seconda dell'epoca della sessione (Cap.41).

**Ambito di applicazione del filtro.** Il filtro $N=3$ si applica alle finestre $W_{in}$ (in-sample) e outer valid del walk-forward nested (Parte V, Capitolo 25.1, schema con finestre $W_{in}$, $P_{purge}$, $W_{oos}$, $P_{emb}$). Il filtro **non** si applica al fold OOS finale della Parte VII Capitolo 31.1 (finestra OOS aggregata e fonte canonica delle metriche): la finestra OOS aggregata e' esplicitamente esclusa dal filtro pre-expiry per preservare la verita' OOS. Le barre pre-expiry presenti nel fold OOS rappresentano condizioni di mercato reali su cui il modello deve dimostrare di operare; rimuoverle introdurrebbe un bias di selezione sulla finestra di validazione finale. Questa regola e' coerente con l'eredita' di Lopez de Prado 2018, Capitolo 7, sulla prevenzione del leakage e sul mantenimento dell'integrita' della finestra OOS.

**Coerenza con la state machine del segnale.** Il filtro pre-expiry esclude barre dal training, ma non altera il comportamento della state machine del segnale (Parte II, Capitolo 7): durante il runtime, il motore opera sul contratto corrente con il payload del segnale ancorato al prezzo strutturale del momento. La gestione del rollover sul lato runtime (decisione di switch operativo sullo strumento in scadenza in funzione dello spread futures/cash) e' di competenza dell'operatore (Parte I, Capitolo 2). La policy di switch del contratto correntemente attivo in produzione non e' oggetto della Parte 8 ed e' demandata alle componenti di runtime del progetto.

---

## Capitolo 40 — Preprocessor griglia 1-min regolare

Portara omette dal file consegnato le barre 1-minuto senza trade (no zero-volume bar fill, vedi Parte I Capitolo 3 e sintesi vincoli Portara). La specifica del documento metodologico v2 assume invece input causalmente uniforme su griglia 1-minuto regolare, con ogni minuto della sessione di negoziazione presente. Il preprocessor del progetto colma il gap producendo una griglia 1-min regolare su $[\text{session\_open}, \text{session\_close}]$ per ogni giornata di sessione, sulle epoche definite in Cap.41.

**Regola di fill virtuale normativa.** Per ogni minuto $t$ della griglia regolare in cui Portara non riporta una barra (assenza di trade nel minuto), il preprocessor inserisce una barra sintetica con i seguenti valori:

- $\mathrm{Open}_t = \mathrm{High}_t = \mathrm{Low}_t = \mathrm{Close}_t = \mathrm{Close}_{t-1}$ (forward-fill del Close della barra precedente; le quattro OHLC coincidono)
- $\mathrm{Volume}_t = 0$
- $\mathrm{TickCount}_t = 0$
- `bar_synthetic` $= \text{True}$ (flag boolean obbligatorio nello schema)

Per le barre con trade reale, il flag `bar_synthetic` e' $\text{False}$ e i campi OHLC/Volume/TickCount sono quelli forniti da Portara.

**Eredita' metodologica dal fill virtuale di Parte III Capitolo 12.4.** La regola di forward-fill su `Close` con flag `bar_synthetic` e' l'eredita' del fill virtuale di Parte III Capitolo 12.4 (regola deterministica di fill virtuale worst-case per il backtest, carryover N-6 di CAP-02). Cap.12.4 specifica che, per il backtest sui dati storici, il raw touch della entry zone in una barra produce un fill virtuale a un prezzo determinato deterministicamente: il forward-fill di Cap.40 ne e' la realizzazione operativa per le barre senza trade. Il flag `bar_synthetic` rende esplicito quali barre sono frutto di forward-fill e quali no, permettendo ai consumer a valle di applicare regole di uso differenziate (vedi sotto).

**Regola di uso a valle.**

- Le **feature di volatilita'** (EGARCH, classificazione di regime, dispersione realized) sono calcolate **solo su barre con `bar_synthetic = False`**, con timestamp allineato alla griglia uniforme per il time-indexing. La calibrazione MLE EGARCH (Parte III, Capitolo 13.3) richiede osservazioni reali: includere barre sintetiche con rendimento log nullo introdurrebbe un bias verso bassa volatilita' e contaminerebbe il fit dei parametri $(\omega, \alpha, \beta, \gamma)$ del modello asimmetrico. La media di sessione $\bar{\sigma}_s$ (Parte III, Capitolo 14.2) usata per la classificazione di regime calmo/turbolento e' anch'essa calcolata escludendo barre sintetiche, per coerenza con la calibrazione EGARCH.

- Le **feature di prezzo** (livelli, distanze da zone, distanze da pivot strutturali) usano la **griglia uniforme completa**, inclusi i minuti sintetici: a livello di prezzo strutturale il forward-fill del Close e' una convenzione di propagazione temporale coerente con l'assenza di trade (il prezzo "ultimo" rimane quello di Cap.12.4) e non altera la dinamica strutturale (un minuto senza trade non sposta i pivot frattali di Parte III Capitolo 15.3). Il catalogo feature di Parte III Capitolo 15.2 e' coerente con questa regola: le feature di prezzo sono causalmente determinate $\mathcal{F}_{t-1}$-misurabili sulla griglia regolare, le feature di volatilita' sono $\mathcal{F}_{t-1}$-misurabili con esclusione delle barre sintetiche dall'input EGARCH.

- Il flag `bar_synthetic` **entra nel feature schema persistito nel bundle frozen** (Parte VII, Capitolo 35): il bundle frozen contiene, per ciascun timestamp della griglia, l'intero record OHLCV + TickCount + `bar_synthetic`. La presenza del flag nel bundle frozen e' condizione necessaria per il replay bit-exact (Parte II, Capitolo 10): due esecuzioni indipendenti del motore sulla stessa finestra storica devono propagare in modo identico la distinzione fra barre reali e sintetiche.

**Convenzione, non inferenza di path: nessun touch su barre sintetiche.** Il forward-fill su `Close` e' una convenzione di propagazione, **non** un'inferenza di path. In particolare, nessun touch della entry zone (raw touch, vedi Parte II Capitolo 7.3) puo' essere dichiarato su una barra con `bar_synthetic = True`. La regola e' coerente con la gap semantics della Parte II Capitolo 7.3: il raw touch e' sempre eseguibile post-emissione ed e' un evento che richiede una barra reale (con $\mathrm{High} \geq \text{bordo zona}$ per i long, o $\mathrm{Low} \leq \text{bordo zona}$ per gli short). Su una barra sintetica con $\mathrm{High}=\mathrm{Low}=\mathrm{Close}_{t-1}$ il range non puo' attraversare la zona di entry per costruzione (a meno che la zona non contenga gia' $\mathrm{Close}_{t-1}$, nel qual caso il touch sarebbe gia' stato dichiarato nella barra reale precedente).

**Implicazioni per le quattro famiglie di feature del catalogo (Parte III Capitolo 15.2).** Il catalogo 37 feature (prezzo, volume, volatilita', struttura) di Parte III Capitolo 15.2 e' coerente con la regola di uso a valle:

- Feature di prezzo (livelli, distanze da zone): usano la griglia uniforme completa.
- Feature di volume: usano solo barre con `bar_synthetic = False` (le barre sintetiche hanno $\mathrm{Volume}=0$ per costruzione, includere queste barre nella media mobile del volume produrrebbe sottostima sistematica).
- Feature di volatilita' (EGARCH, dispersione realized): usano solo barre con `bar_synthetic = False`.
- Feature di struttura (pivot frattali, EMA): usano la griglia uniforme completa per il time-indexing, ma il loro calcolo non e' contaminato dalla presenza di barre sintetiche (il pivot frattale di Parte III Capitolo 15.3 richiede un confronto sui prezzi High/Low, che sono propagati per forward-fill ma non alterano la condizione di pivot finche' una nuova barra reale non li sposta).

---

## Capitolo 41 — Timeline ufficiale delle sessioni FIB

La timeline normativa delle sessioni di negoziazione del contratto FIB sul mercato IDEM e' organizzata per epoche, ciascuna identificata da `epoch_id` univoco crescente e da un intervallo di date $[\text{start\_date}, \text{end\_date}]$ in cui l'epoca e' in vigore. Per ciascuna epoca sono dichiarati gli orari della **sessione di negoziazione continua** (escludendo la fase di asta di apertura, presente in tutte le epoche ma con timing variabile e non rilevante per la semantica del segnale).

**Tabella delle epoche.**

| `epoch_id` | `start_date` | `end_date` | `session_open_local` | `session_close_local` | `timezone` |
|------------|--------------|------------|----------------------|------------------------|------------|
| E1 | 1994-11-28 | 2010-11-07 | 09:15 | 17:30 | CET |
| E2 | 2010-11-08 | 2015-11-22 | 09:00 | 17:40 | CET |
| E3 | 2015-11-23 | 2017-07-02 | 09:00 | 17:50 | CET |
| E4 | 2017-07-03 | 2020-02-16 | 09:00 | 20:30 | CET |
| E5 | 2020-02-17 | 2026-05-27 | 08:00 | 22:00 | CET |

**Note di interpretazione.**

- `session_open_local` indica l'inizio della sessione di negoziazione **continua**, escludendo la fase di asta di apertura (la pre-asta, validazione, apertura) che precede la negoziazione in continua. La pipeline di preprocessing assume `session_open_local` come prima barra utile della griglia 1-min regolare (Cap.40).

- `session_close_local` indica la chiusura della sessione di negoziazione continua. Per l'epoca E4 (2017-07-03 → 2020-02-16) gli orari sono single continuous session 09:00-20:30 con un marcatore convenzionale di transizione fra "diurna" (09:00-17:50) e "serale" (17:50-20:30): il marker 17:50 **non e' una pausa di mercato**. La pipeline tratta E4 come finestra continua singola, coerentemente con la decisione che la sessione FIB e' negoziazione continua su tutta la finestra dichiarata (Q-01 chiusa, Parte II Capitolo 7).

- `end_date` indica l'ultimo giorno di calendario in cui l'epoca e' in vigore, ovvero il giorno PRIMA della `start_date` dell'epoca successiva. Per l'epoca corrente E5, la `end_date` 2026-05-27 corrisponde alla data di consultazione delle fonti al momento della stesura della Parte 8; il calendario va esteso quando emergeranno nuove epoche (nuove estensioni della sessione decise da Borsa Italiana).

- Tutti i timestamp dichiarati `CET` includono la conversione automatica `CEST` quando in vigore: la pipeline gestisce la transizione automatica fra ora solare (CET) e ora legale (CEST) coerentemente con il calendario europeo (ultima domenica di marzo → ultima domenica di ottobre), in coerenza con la semantica eventi/timestamp del documento metodologico v2 (Parte II, Capitolo 7).

- Tick FIB = 5 punti indice. Moltiplicatore FIB pieno = 5 EUR/punto; miniFIB = 1 EUR/punto. La timeline e' coerente con il preambolo `00_indice.md` del documento e con la dichiarazione dello strumento di Parte I Capitolo 1.

**Riferimento alla sessione runtime corrente.** L'epoca corrente E5 corrisponde alla sessione 08:00-22:00 CET dichiarata in Parte I Capitolo 1 come finestra unica e continua di negoziazione operativa del motore. Il motore in runtime opera esclusivamente su barre della sessione corrente (E5); il training e' invece esteso su tutta la timeline storica (E1-E5), con il preprocessor che applica gli orari corretti per ogni epoca alla griglia 1-min regolare di Cap.40.

**File normativo associato.** La timeline e' persistita nel file CSV normativo `data/sessions/fib_session_calendar.csv` con schema a 6 campi `(epoch_id, start_date, end_date, session_open_local, session_close_local, timezone)`. Il file CSV e' il riferimento operativo per il preprocessor: la lookup di `(session_open_local, session_close_local)` per una data di sessione $d$ e' eseguita selezionando la riga $e$ del CSV tale che $\text{start\_date}_e \leq d \leq \text{end\_date}_e$.

**Note di provenienza e ambiguita' (non normative).** Le note di provenienza delle date e degli orari, con riferimenti alle fonti consultate (comunicati ufficiali Borsa Italiana, Avvisi Borsa, archivi storici) e le ambiguita' residue (in particolare per le epoche E1 e E2, dove alcuni orari sono derivati per inferenza inversa o non sono confermati da un comunicato ufficiale specifico) sono raccolte nel file non normativo `data/sessions/README.md`. Le ambiguita' residue verranno riesaminate in CAP-DATA-02 (richiesta tecnica a Portara) o in PHASE-B (acquisizione storico Portara), che potrebbero fornire metadati addizionali sulle epoche storiche via roll log Portara o conferma diretta dal vendor.

---

## Capitolo 42 — Convenzione cross-index (PHASE-2)

La convenzione cross-index per gli strumenti correlati al FIB e' **dichiarazione normativa PHASE-2 senza implementazione nel doc v2 corrente**. La sua attivazione operativa e' rinviata a un futuro ciclo di estensione del documento, fuori scope dal corpo Parti I-VIII del doc v2 corrente. La fasizzazione PHASE-1 (FIB-only) e' esplicita e dichiarata, non semplificazione silenziosa.

Il documento metodologico v2 e' esplicitamente single-instrument FIB: il preambolo dichiarato in `docs/methodology_v2/00_indice.md` recita "rimozione dei layer multi-indice (DCC/ADCC/BEKK, covarianza cross-index, N>=8)". La presente sezione Cap.42 introduce la convenzione cross-index come **dichiarazione di estensione normativa PHASE-2**, in deroga esplicita al preambolo, ratificata dal supervisore (decisione (1) dell'handoff CAP-07 → CAP-DATA-01). Nessun riferimento implementativo alle Parti I-VII per il layer cross-index e' fatto in questa sezione: il layer di covarianza cross-index non esiste nel doc v2 corrente.

**Strumenti cross-index della PHASE-2.** Gli strumenti previsti per la PHASE-2 sono:

- **DAX** — contratto futures FDAX su Eurex (indice DAX, sottostante azionario tedesco)
- **EuroStoxx 50** — contratto futures FESX su Eurex (indice EuroStoxx 50, sottostante azionario eurozona)
- **S&P 500 mini** — contratto futures ES su CME (indice S&P 500, sottostante azionario USA)

**Convenzione normativa cross-index.** Quando PHASE-2 sara' attivata in un futuro ciclo di estensione del doc v2, la stessa convenzione normativa stabilita per il FIB (Capitoli 37-41 di Parte 8) si applichera' identicamente agli strumenti cross-index:

- Serie ufficiale di training: futures pieno back-adjusted Portara/CQG, ratio-adjusted ricostruita in preprocessing (Cap.37, Cap.38).
- Tre serie derivabili: ratio-adjusted per training, Panama-additive per audit monetario, unadjusted concatenata per sanity check (Cap.38).
- Filtro pre-expiry $N = 3$ giorni di trading di default, allineato alla roll rule del vendor (Cap.39).
- Preprocessor griglia 1-min regolare con forward-fill e flag `bar_synthetic` (Cap.40).
- Calendario sessione per epoca, ciascuno strumento con il **proprio** calendario di sessione e roll calendar (Cap.41).

**Specifiche aggiuntive proprie del layer cross-index.**

- Ciascuna serie ha il **proprio** roll calendar e il **proprio** calendario sessione: i roll del DAX (terza venerdi del mese di scadenza) non coincidono con i roll del FIB, e gli orari di sessione di Eurex, IDEM e CME sono distinti.
- La stima dei modelli di covarianza condizionata cross-index (eventualmente DCC, ADCC, cDCC: estensioni future, vedi sotto) opera su **timestamp intersezione** delle griglie regolari, non su forward-fill cross-asset. La griglia intersezione e' definita come l'insieme dei timestamp 1-min in cui tutti gli strumenti dichiarati hanno simultaneamente una barra reale (`bar_synthetic = False`) nelle rispettive griglie regolari.
- I giorni di festivita' di un singolo exchange escludono la corrispondente riga dal calcolo cross-index per quel giorno: se IDEM e' chiuso ma Eurex e CME sono aperti, la riga del giorno e' esclusa dall'aggregato cross-index (non c'e' osservazione sul FIB) ma le serie monoindice di DAX, ESTX50, ES restano disponibili per le rispettive analisi single-instrument se necessarie.

**Vincolo di fasizzazione PHASE-1 vs PHASE-2.** Va dichiarato esplicitamente che la convenzione cross-index e' normativa **come dichiarazione**, ma la sua attivazione operativa e' rinviata alla PHASE-2 del progetto. La PHASE-1 (FIB-only) e' una fasizzazione esplicita: il documento metodologico v2 corrente istanzia la specifica del motore esclusivamente sul FIB, senza il layer di covarianza cross-index. Quanto la fasizzazione PHASE-1 implica rispetto alla specifica ideale:

- La varianza sistemica cross-index $\sigma_{sys}$ ridotta a $\sigma_{local}$ (la varianza condizionata locale del FIB stimata da EGARCH(1,1) in Parte III Capitolo 13). La degradazione metodologica e' dichiarata: in PHASE-1, $\sigma_{local}$ e' il proxy operativo della componente sistemica.
- Il feature tensor di Parte III Capitolo 15.2 e' privo dei canali cross-index obbligatori della specifica ideale: il catalogo 37 feature e' calibrato single-instrument FIB. La presenza dei canali cross-index, prevista nella specifica ideale, e' un regime di funzionamento esplicito della PHASE-2.
- Lo score strutturale $S_{xidx}$ del catalogo target, previsto dalla specifica ideale come componente di sintesi della direzione coerente cross-index, **non e' calcolabile** in PHASE-1. La quinta famiglia del catalogo target ("proiezioni cross-index coerenti") e' esclusa dalla PHASE-1.
- Il report per regime di volatilita' del motore (calmo/turbolento) e' privo della riga "Contagio cross-index": la metrica di contagio sistemico fra indici non e' calcolata in PHASE-1.

La fasizzazione **non sostituisce la specifica ideale**, la istanzia in modo parziale per la PHASE-1 con costi noti. La PHASE-2 ripristinera' i layer cross-index in un futuro ciclo di estensione del documento.

**Estensioni future esplicite.** Le seguenti estensioni sono dichiarate esplicitamente come **non implementate** nel doc v2 corrente:

- **Modelli di covarianza condizionata cross-index** (DCC, ADCC, cDCC) — citati come opzioni candidate per la PHASE-2, non implementate nel doc v2 corrente.
- **Realized GARCH** — citato esclusivamente come esempio futuro di modello di volatilita' che richiederebbe `bar_synthetic = False` come input rigoroso (decisione (2) dell'handoff CAP-07 → CAP-DATA-01: estensione futura, non in Parte 8). Non implementato nel doc v2 corrente.
- **`S_xidx` e quinta famiglia del catalogo target ("proiezioni cross-index coerenti")** — citati come componenti della specifica ideale, esclusi dalla PHASE-1 e dal doc v2 corrente (decisione (3) dell'handoff CAP-07 → CAP-DATA-01: estensione futura, coerente con (1)).

Nessuno di questi tre elementi entra come parte dell'impegno corrente del documento metodologico v2.

---

## Capitolo 43 — Procedura di sanity validation

La procedura di sanity validation della serie back-adjusted e' una **procedura normativa** che il progetto applica una sola volta in occasione dell'acquisizione dei dati Portara e prima dell'avvio del training operativo. La procedura confronta la serie ratio-adjusted ufficiale (Cap.38) con la serie unadjusted concatenata (Cap.38), su una finestra temporale recente, per verificare che il back-adjustment non abbia introdotto artefatti di distribuzione significativi rispetto alla serie naturale dei contratti.

**Finestra di validazione.** La finestra di confronto e' definita come gli **ultimi 18-24 mesi** del file Portara consegnato. La scelta della finestra recente garantisce che il confronto sia condotto su un periodo in cui la microstruttura del FIB e' verosimilmente stabile (sessione 08:00-22:00 CET, epoca E5 di Cap.41) e in cui il numero di roll e' sufficiente (sei rolls per anno sul FIB con scadenze trimestrali, dodici-quattordici roll nella finestra di 18-24 mesi) per consentire un confronto statistico significativo fra le due serie.

**Metriche di confronto.** Per ciascuna delle due serie (ratio-adjusted e unadjusted-stitched), sul medesimo intervallo della finestra di validazione, sono calcolate le seguenti metriche:

- **Distribuzione dei rendimenti log a 1-min, 5-min e 60-min**, con quantili al $1\%, 5\%, 25\%, 50\%, 75\%, 95\%, 99\%$. I rendimenti sono calcolati come $r_t = \log(P_t / P_{t-1})$ a 1-min; le aggregazioni a 5-min e 60-min seguono la convenzione di Parte III Capitolo 12 (somma dei rendimenti log a 1-min entro la barra aggregata).
- **Autocorrelazione dei rendimenti log** al lag 1, 5, 30. Stimata con stimatore consistente sotto eteroschedasticita' (Newey-West 1987 con bandwidth $L_{NW} = \lfloor 4 \cdot (T/100)^{2/9} \rfloor$, dove $T$ e' la lunghezza della finestra).
- **Autocorrelazione dei rendimenti quadrati** $r_t^2$ al lag 1, 5, 30. Stimata con lo stesso metodo.
- **$\sigma$ giornaliera realized**, definita come $\sigma_d = \sqrt{\sum_{t \in d} r_t^2}$ sulle 1-min della giornata $d$. Per ciascuna serie si calcola la distribuzione di $\{\sigma_d\}_{d \in \text{finestra}}$ con quantili $25\%, 50\%, 75\%$.

**Criterio di accettazione.** Le differenze fra le metriche calcolate sulle due serie devono restare entro **3$\sigma$ bootstrap** per ciascuna metrica considerata. L'intervallo di confidenza bootstrap e' calcolato con bootstrap stazionario (Politis e Romano 1994) con $B = 2.000$ replicazioni, in coerenza con il protocollo bootstrap normativo del doc v2 (Parte VII, Capitolo 34). La block length media $L_{avg}$ del bootstrap stazionario e' quella calibrata su dati FIB in Parte VII Capitolo 34.2; in mancanza di calibrazione operativa, il sanity check utilizza $L_{avg}$ pari al valore di default congelato in Parte VII (vedi Capitolo 34.2 per il valore corrente).

L'inferenza di accettazione e' una decisione binaria per ciascuna metrica: se per tutte le metriche la differenza fra ratio-adjusted e unadjusted-stitched e' entro $3\sigma$ bootstrap, la serie ratio-adjusted e' considerata accettabile come serie ufficiale di training. Discrepanze superiori a $3\sigma$ su una o piu' metriche richiedono indagine prima del go-ahead training: la fonte della discrepanza va identificata (anomalia in un singolo roll, artefatto di calcolo del fattore $\rho_k$ di Cap.38, ecc.) e risolta prima di procedere.

**Coerenza con le metriche del doc v2.** Le metriche di confronto sono allineate alla normativa del doc v2:

- I rendimenti log a 1-min, 5-min e 60-min seguono la definizione di Parte III Capitolo 12 (rendimenti log e aggregazione a barre superiori).
- L'autocorrelazione dei rendimenti e dei rendimenti quadrati e' coerente con la diagnostica residui EGARCH di Parte III Capitolo 13.4 (Ljung-Box, ARCH-LM).
- Il bootstrap stazionario per gli intervalli di confidenza e' coerente con Parte VII Capitolo 34.

**Out-of-scope per CAP-DATA-01.** L'implementazione del check di sanity validation **non e' oggetto di CAP-DATA-01**. Cap.43 e' normativa di procedura, non di implementazione. L'implementazione vivra' in FASE-D del roadmap del progetto, dopo l'acquisizione dei dati Portara (FASE-B) e prima dell'avvio del training operativo. CAP-DATA-01 stabilisce solo la convenzione che la procedura sia eseguita, con i parametri ($3\sigma$ bootstrap, $B = 2.000$, finestra 18-24 mesi) congelati.

---

## Capitolo 44 — Esclusione esplicita di fonti alternative

La presente sezione e' clausola di chiusura normativa della Parte 8. Rende esplicito il dominio di applicabilita' della convenzione dati congelata in Cap.37-43, elencando le fonti che **non sono ammesse** come input alla pipeline del documento metodologico v2.

**Fonti escluse.**

- **MIB cash (FTSE MIB cash)** — esclusa per violazione dell'invariante `research semantics = runtime semantics` (Parte I, Capitolo 1). La motivazione completa e' in Cap.37 (esclusione esplicita di MIB cash come fonte training): differenze su orari, microstruttura, basis, gap di apertura rispetto al contratto futures di esecuzione.

- **Dati vendor diversi da Portara/CQG senza nuovo task Planner** — il vendor di riferimento normativo del progetto e' Portara/CQG (Parte I, Capitolo 3, dove lo storico Portara/CQG e' dichiarato come fonte ufficiale per il training). L'utilizzo di un vendor alternativo (Bloomberg, Refinitiv, Reuters, qualunque altro vendor) richiede un nuovo task Planner per autorizzazione esplicita, con riesame della convenzione di back-adjustment (Cap.38), del roll log e della politica di rollover (Cap.39).

- **Mix di vendor diversi per cross-index** (DAX da un vendor X, ESTX50 da un vendor Y, ES da un vendor Z) — esclusa per il layer cross-index della PHASE-2 (Cap.42). La convenzione PHASE-2 prevede che tutti gli strumenti cross-index siano forniti dallo stesso vendor (Portara/CQG di default), per garantire coerenza nella convenzione di back-adjustment, nel roll log e nella sincronizzazione dei timestamp. Un mix di vendor introduce rischio di discrepanze sulla griglia 1-min intersezione (Cap.42) e contamina la stima dei modelli di covarianza cross-index.

- **Dati ricostruiti da CFD broker** — esclusi. I CFD (Contract for Difference) sono strumenti derivati OTC con microstruttura propria del broker (spread bid-ask variabile, slippage, finestre di liquidita' specifiche), non comparabili al contratto futures negoziato in centralized order book sul mercato regolamentato IDEM. La ricostruzione di una serie storica da CFD broker introdurrebbe bias di microstruttura non controllabili.

- **Dati intraday liberi** (Yahoo Finance, Investing.com, qualunque altra fonte free) — esclusi. Non sono utilizzabili nemmeno come benchmark di confronto, coerentemente con la data-matching policy di Portara. La motivazione: i dati intraday free sono tipicamente snapshot occasionali con risoluzione temporale non coerente con la griglia 1-min causale richiesta dal modello (Parte III, Capitolo 15.1, vincolo $x_t \in \mathcal{F}_{t-1}$). Inoltre la fonte free non garantisce continuita' storica su 5+ anni a frequenza 1-minuto, requisito minimo per il training del motore.

**Regola di estensione.** Ogni fornitore alternativo che si volesse introdurre come fonte training, o come benchmark di confronto, o come fonte cross-index, richiede un nuovo task Planner per autorizzazione esplicita. Il task Planner deve verificare:

- coerenza con l'invariante `research = runtime` (Parte I, Capitolo 1);
- compatibilita' della convenzione di back-adjustment del nuovo vendor con Cap.38;
- compatibilita' del roll log e della politica pre-expiry con Cap.39;
- compatibilita' della granularita' 1-min e del trattamento delle barre senza trade con Cap.40;
- compatibilita' del calendario sessione con Cap.41 (per il FIB) o con il calendario sessione dello specifico exchange (per gli strumenti cross-index della PHASE-2).

In assenza di autorizzazione esplicita via nuovo task Planner, la sola fonte ammessa resta Portara/CQG per il FIB, con possibile estensione a Portara/CQG sugli strumenti DAX/ESTX50/ES per la PHASE-2 (Cap.42).
