# Parte VI — Emissione segnali e lifecycle senza execution

La Parte VI mette in produzione il bundle frozen prodotto dal walk-forward nested di Parte V e ne governa l'operatività in regime live, senza alcun layer di execution. Il documento formalizza in quattro capitoli: la pipeline di inference real-time che, dato il feed Directa DAPI e il bundle frozen, produce i segnali pubblicabili (Cap.27); la politica anti-doppio-segnale che operazionalizza il vincolo normativo $|\mathcal{A}(t)| \leq 1$ di Cap.6.3 di Parte II in presenza di candidati concorrenti (Cap.28); la gestione dell'operatività su mobile con un layout mobile-first del messaggio Telegram che estende senza duplicare il contratto informativo a 9 voci di Cap.9.2 di Parte II (Cap.29); il monitoraggio del lifecycle in produzione con metriche live, dashboard di sintesi lato motore e alert su deriva (Cap.30).

La Parte VI non contiene la validazione OOS finale con DSR/PBO/bootstrap stazionario (Parte VII Cap.31-34), i gate decisionali di go-live (Parte VII Cap.36), il processo di freezing del bundle (Parte VII Cap.35), né le specifiche di interfaccia (Appendici C-D-E). La Parte VI non contiene alcuna logica di esecuzione ordini, order routing, gestione fill, slippage di esecuzione, calcolo di posizione netta: il sistema rimane "solo emissione" come dichiarato in Cap.1 di Parte I. La Parte VI non contiene logica di re-training del GA in production: il bundle frozen non viene riottimizzato in live, e l'unica ricalibrazione real-time consentita riguarda i parametri runtime del modello di volatilità EGARCH (Cap.27.5), con cadenza fissa e trigger di break parametrico monitorati in Cap.30.4.

Tutti i parametri introdotti in Parte VI come variabili di tuning operativo ($T_{recal,\text{EGARCH}}$, $\theta_B$, $T_{B,\text{persist}}$, $W_B$, $W_{prod}$, $T_{drift,\text{persist}}$, $T_{emit,\text{persist}}$, $\epsilon_p$, $N_{reg,\min}^{live}$, $\alpha_{f_5}$) sono dichiarati **non congelati in Parte VI, riconsiderati post-go-live**: la Parte VI non aggiunge una propria tabella di congelamento e non modifica la tabella di Cap.26.5 di Parte V, che resta invariata. Le soglie $E_{max} = 5$, $E_{min} = 0{,}2$, $E_{exp,max} = 0{,}30$ utilizzate in Cap.30 sono ereditate da Cap.26.5 di Parte V già congelate e Cap.30 le riusa senza ridichiararle.

---

## Capitolo 27 — Pipeline di inference real-time

### 27.1 Architettura della pipeline e vincolo emissione-only

Il motore opera in **modalità emissione-only**: produce e pubblica segnali ma non esegue ordini, non instrada richieste di acquisto/vendita al broker e non gestisce posizione. Questo vincolo strutturale discende dal punto 1 della dichiarazione di intenti dell'operatore e dal Cap.1 di Parte I, e si applica integralmente alla pipeline di inference real-time qui formalizzata. La pipeline opera durante la **finestra di sessione 8:00-22:00 CET** di Cap.1 di Parte I (840 barre 1-min per sessione), che coincide con la finestra di emissione e processamento dei segnali del motore. La pipeline gira **in locale sul personal computer dell'operatore** (Intel Core i5-7200U/8 GB, Cap.3 di Parte I) e non delega a infrastruttura cloud alcuna funzione di inference: il cloud è utilizzato esclusivamente per la fase di training periodico del bundle (Cap.4 di Parte I), non per la produzione live. La fonte del feed real-time è **Directa SIM DAPI** (porta 10001), in coerenza con Cap.3 di Parte I; nessuna chiamata di execution viene effettuata verso DAPI.

La pipeline è strutturata come sequenza deterministica di blocchi, eseguita a ogni nuova barra 1-min chiusa proveniente dal feed Directa DAPI:

1. **Ingest feed Directa DAPI**: ricezione delle barre OHLCV 1-min real-time secondo la specifica di Appendice C. La latenza di ricezione fa parte del bilancio complessivo del vincolo di Cap.27.2.
2. **Calcolo delle barre 1-min e aggregazione**: consolidamento della barra appena chiusa, allineamento al fuso CET e alla griglia 1-min, in coerenza con Cap.12 di Parte III. Le barre sono memorizzate nello stato interno del motore per il calcolo delle feature successive.
3. **Calcolo delle feature live sul catalogo 37**: produzione del vettore delle feature causali $\mathbf{x}_t$ secondo Cap.15.2 di Parte III, rispettando il vincolo $x_t \in \mathcal{F}_{t-1}$ (le feature al tempo $t$ sono calcolate sulla barra appena chiusa $t-1$, non sulla barra in formazione). Il catalogo è quello congelato della tabella di Cap.26.5 di Parte V.
4. **Inference EGARCH(1,1) con parametri runtime**: produzione della stima $\hat{\sigma}_{\text{pt}}(t)$ secondo Cap.13 di Parte III; i parametri del modello sono quelli stimati nel fold di calibrazione corrente (Cap.27.3) e ri-stimati con cadenza $T_{recal,\text{EGARCH}}$ (Cap.27.5).
5. **Classificazione regime live**: produzione di $R_t \in \{\text{calmo}, \text{turbolento}\}$ secondo Cap.14 di Parte III, con parametri $\bar{\sigma}_s$, $p = 0{,}75$, $N_{reg} = 20$, $T_{persist} = 10$ congelati in Cap.26.5 di Parte V.
6. **Algoritmo pivot detection live**: applicazione dell'algoritmo di Cap.15.3 di Parte III con parametri $n_c = 3$ e $\delta_{pivot} = 10$ pt congelati; produzione dell'insieme dei pivot strutturali confermati al tempo $t$. La regola di sospensione strutturale in warm-up di Cap.16.2 di Parte IV vale anche in produzione: in assenza di pivot strutturali confermati nella direzione richiesta, il motore non emette indipendentemente dai valori dei filtri.
7. **Costruzione del candidate signal dal bundle frozen**: applicazione delle regole di Cap.16-18 di Parte IV per derivare $p_{ref}$, `entry_zone`, `target_1`, `target_2`, `target_2_type`, `stop_loss`, `stop_type`, `setup_class`, $\Delta t_{cromosoma}$, $T_{touch}^{max}$, a partire dai geni $b$, $k_{t2}$, $d_{stop,\sigma}$, $\Delta t_{cromosoma}$, $T_{touch}^{max}$ del cromosoma frozen e dalla geometria dei pivot al tempo $t$. Calcolo di $\hat{p}_{hit}$ live tramite il modello Cox cause-specific di Cap.19 di Parte IV (coefficienti del fold di calibrazione corrente, stratificazione regime di Cap.25.5 di Parte V preservata).
8. **Valutazione dei filtri di emissione in AND logico**: applicazione del filtro composto
$$E_{vol}(t) \land E_{liq}(t) \land E_{dist}^{\sigma}(t) \land E_{80\text{pt}}(t) \land E_{surv}(t)$$
secondo Cap.8 di Parte II e Cap.20 di Parte IV. Le soglie $\tau_{vol}(\cdot)$, $\tau_{liq}$, $\tau_{dist}^{\sigma}$, $\tau_{surv}(\cdot)$ sono lette dal bundle frozen (output Parte V). Il filtro $E_{80\text{pt}}$ è il vincolo assoluto di Cap.5 di Parte I (filtro $\geq 80$ pt sul target_1 per i setup directional, o sull'ampiezza $A_{range}$ per i setup trade_range), già incorporato nei vincoli del bundle frozen e non rivalutato runtime separatamente.
9. **Emissione Telegram in caso di passaggio del filtro**: se l'AND logico restituisce vero e la politica di Cap.28 ammette l'emissione (segnale unico attivo), produzione e pubblicazione del messaggio Telegram secondo il layout mobile-first di Cap.29.

Tra il blocco (8) e il blocco (9) interviene la politica anti-doppio-segnale di Cap.28, che può scartare silenziosamente il candidato se al tempo $t$ esiste già un segnale attivo (politica di no-refresh). La pipeline gira con cadenza minutale, in coerenza con la granularità delle barre 1-min del modello.

### 27.2 Latenza end-to-end e vincoli temporali

La latenza end-to-end della pipeline, definita come intervallo fra l'arrivo della barra 1-min chiusa dal feed Directa DAPI al motore e la consegna del messaggio Telegram al cellulare dell'operatore, deve restare entro vincoli compatibili con l'utilità operativa del segnale. Il vincolo qualitativo è dichiarato come obiettivo: la latenza complessiva non deve eccedere l'ordine di grandezza dichiarato come $L_{max}$ qualitativo di Cap.9.3 di Parte II ($L_{max} = 30$ s valore di lavoro provvisorio), oltre il quale il prezzo strutturale di riferimento $p_{ref}$ può essersi spostato significativamente rispetto al momento dell'emissione.

La **verifica numerica empirica** del valore di $L_{max}$ effettivo del canale Telegram resta carryover di Appendice E (M-2 OPEN, Review v1 CAP-02): non è risolta in Parte VI. Cap.27.2 ne cita il vincolo qualitativo come obiettivo di progettazione della pipeline; il dimensionamento numerico operativo è demandato all'Appendice E sulla base di misure empiriche su bot Telegram reale.

### 27.3 Bundle frozen come input invariante

Il bundle frozen consumato dalla pipeline di inference live è l'**output dell'ultimo fold di calibrazione del walk-forward nested** di Parte V (Cap.25.1 con $F = 8$ fold provvisori, $W_{in} = 105.840$ barre, $W_{oos} = 52.920$, $P_{purge} = P_{emb} = 4.200$ barre). La selezione del bundle dal fronte di Pareto $\mathcal{F}_1$ prodotto dal NSGA-II e la sua **promozione formale a "produzione"** sono decisioni di Parte VII (Cap.31-36, in particolare Cap.36 gate decisionali go-live): Cap.27.3 cita esplicitamente questo rinvio. Una volta promosso, il bundle frozen è **input invariante** della pipeline di inference: i suoi parametri (sia parametri del modello sia geni del cromosoma frozen) sono letti dalla **tabella di congelamento di Cap.26.5 di Parte V senza alcuna modifica runtime**. Nessun gene del cromosoma viene ri-ottimizzato in produzione; nessun parametro del modello (es. $W$ rolling EGARCH, $p$ quantile regime, $K_{max}$ feature attive Cox) viene rivisto runtime.

L'unica ricalibrazione consentita in produzione riguarda i parametri runtime del modello EGARCH (Cap.27.5), che vengono ri-stimati con cadenza fissa per mantenere aderenza al regime di volatilità corrente; questa ricalibrazione **non modifica i geni del cromosoma frozen** né le soglie del bundle, e non costituisce re-training del GA.

Il **seed** del bundle frozen (Cap.26.8 di Parte V e Cap.10 di Parte II) è parte dell'identità del bundle e **viene loggato in ogni emissione live** insieme al `signal_id`, in coerenza con il requisito di replay deterministico bit-exact di Cap.10 di Parte II.

### 27.4 Pipeline di emissione del payload

Il payload del segnale prodotto dalla pipeline in inference live è **bit-exact identico al payload formale di Cap.6.1 di Parte II** (Iterazione 4 con $\mathcal{S}$ esteso a 12 campi `signal_id, timestamp_emission, direction, entry_zone, target_1, target_2, target_2_type, stop_loss, stop_type, setup_class, $\Delta t_{cromosoma}$, $T_{touch}^{max}$`). La pipeline non aggiunge campi runtime, non rimuove campi e non rinomina campi: il payload pubblicato in produzione è la tupla $\mathcal{S}$ di Parte II senza estensioni né riduzioni.

I valori dei campi sono prodotti dalla derivazione deterministica documentata in Parte IV:

- **`entry_zone`** è la banda discreta $\{p_{ref} - b, p_{ref} - b + 5, \ldots, p_{ref} + b\}$ secondo Cap.16.3 di Parte IV con $b$ letto dal cromosoma frozen e $p_{ref}$ ricavato da Cap.16.1 (timestamp di conferma del pivot strutturale più recente nella direzione del segnale).
- **`target_1`, `target_2`, `target_2_type`** sono derivati secondo Cap.17 di Parte IV; il qualificatore `target_2_type` $\in \{\text{structural}, \text{synthetic}\}$ è prodotto dall'algoritmo di Cap.17.4 in funzione della disponibilità di pivot strutturali oltre target_1 (`structural`) o dell'attivazione del fallback sintetico $\texttt{target\_2} = \texttt{target\_1} \pm k_{t2} \cdot \hat{\sigma}_{\text{pt}}(t)$ arrotondato a multiplo di 5 (`synthetic`).
- **`stop_loss`, `stop_type`** sono derivati secondo Cap.18 di Parte IV con $d_{stop,\sigma}$ dal cromosoma frozen; il qualificatore `stop_type` $\in \{\text{structural}, \text{synthetic}\}$ è prodotto dall'algoritmo di Cap.18.1 in funzione della disponibilità di pivot strutturali nella direzione avversa coerenti con il vincolo $d_{stop} > b$ (`structural`) o dell'attivazione del fallback sintetico (`synthetic`).
- **`setup_class`** $\in \{\text{directional}, \text{trade\_range}\}$ è classificato secondo Cap.21 di Parte IV.
- **$\Delta t_{cromosoma}$, $T_{touch}^{max}$** sono letti dal cromosoma frozen.
- **`timestamp_emission`** è il minuto chiuso CET di emissione; **`signal_id`** è generato come **hash deterministico dei campi del payload** secondo Cap.10 di Parte II, garantendo replay bit-exact.
- **`direction`** è long o short, deciso dalla geometria dei pivot al tempo $t$.

Il logging deterministico bit-exact, in coerenza con Cap.10 di Parte II, registra integralmente il payload emesso, gli snapshot dei filtri (valori di $r_{1m}, v_{1m}, |\texttt{target\_1} - p_{ref}|/\hat{\sigma}_{\text{pt}}$, $\hat{p}_{hit}$, $R_t$), il seed del bundle, l'identificatore di versione del cromosoma frozen, e la finestra di calibrazione EGARCH attiva al tempo $t$ (con timestamp di ultima ricalibrazione). Il file di log prodotto in produzione è **canonico**: ricalcolato offline sullo stesso feed e con lo stesso bundle frozen, riproduce esattamente la stessa sequenza di emissioni e di payload al bit (Cap.30 lo utilizza come fonte canonica per il calcolo delle metriche live).

### 27.5 Cadenza di ricalibrazione EGARCH in production e trigger di break parametrico

La sotto-sezione 27.5 chiude la parte production residua di **M-2 v2 Review v2 CAP-03** (CLOSED-CAP-05 parziale, residuo Parte VI). La separazione operativa è dichiarata esplicitamente: **Cap.27.5 definisce il meccanismo** (cadenza temporale + flag $B(t)$ + soglia + trigger di anticipo); **Cap.30.4 calcola live il flag $B(t)$ sul feed real-time e produce l'alert** al superamento della soglia, eventualmente anticipando la ricalibrazione.

**Cadenza temporale fissa $T_{recal,\text{EGARCH}}$**. In produzione, i parametri del modello EGARCH(1,1) (Cap.13 di Parte III) vengono ri-stimati a cadenza temporale fissa $T_{recal,\text{EGARCH}}$. La ri-stima utilizza la finestra di calibrazione corrente del bundle frozen (Cap.13.3 di Parte III + Cap.25.3 di Parte V, finestra eventualmente selezionata dal protocollo M-5 di rollback rolling/expanding/EWMA), preservando la specifica strutturale del modello (distribuzione $D$, inizializzazione cross-session). $T_{recal,\text{EGARCH}}$ è **parametro di tuning operativo** con dominio temporale tipico **settimanale-mensile**; il valore di **default proposto per il primo run di produzione** è $T_{recal,\text{EGARCH}} = $ 21 sessioni di trading (≈ 1 mese calendario di FIB), coerente con la cadenza di calibrazione fold-per-fold del walk-forward nested di Parte V (Cap.25.9: ogni fold è 3 mesi, e una cadenza intermedia mensile in produzione rappresenta circa un quarto della finestra di fold). Il valore è dichiarato **non congelato in Parte VI** e riconsiderato post-go-live sulla base degli esiti empirici delle prime sessioni di produzione.

**Flag di break parametrico $B(t)$**. Si definisce $B(t)$ una statistica scalare calcolata sui residui standardizzati $z_t = \epsilon_t / \sigma_t$ del modello EGARCH in finestra recente, che misura la **stabilità dei parametri del modello fra la calibrazione corrente e i dati real-time più recenti**. La formulazione adottata è il **test di Nyblom (1989)** "Testing for the Constancy of Parameters Over Time", *Journal of the American Statistical Association* 84(405), 223–230, applicato in chiave di rolling diagnostic sui parametri del modello GARCH/EGARCH secondo la prassi consolidata di letteratura (estensione applicata da Lee e Hansen 1994 "Asymptotic Theory for the GARCH(1,1) Quasi-Maximum Likelihood Estimator", *Econometric Theory* 10(1), 29–52, e successiva applicazione in contesto rolling). La statistica di Nyblom valuta l'ipotesi nulla di costanza dei parametri contro l'alternativa di parametri non costanti via la statistica cumulata
$$L = \frac{1}{n^2} \sum_{t=1}^{n} S_t' \hat{V}^{-1} S_t$$
dove $S_t = \sum_{i=1}^{t} \hat{\mathbf{g}}_i$ è la somma cumulata dei gradienti della log-verosimiglianza ai parametri stimati e $\hat{V}$ è una stima della matrice di covarianza asintotica. Si pone $B(t) = L$ calcolata sulla finestra recente $[t - W_{B}, t]$ con $W_B$ ampiezza tipica 1-5 sessioni di trading (parametro tecnico, valore di lavoro proposto $W_B = $ 3 sessioni $= 2.520$ barre 1-min, dichiarato non congelato). Una formulazione alternativa accettabile, qualora l'implementazione di Nyblom risulti onerosa, è il **test di Engle e Sheppard (2001)** "Theoretical and Empirical Properties of Dynamic Conditional Correlation Multivariate GARCH", NBER Working Paper 8554, adattato per il caso univariato sui residui standardizzati $z_t^2$ (autocorrelazione di Ljung-Box rolling, con soglia $\theta_B$ tarata in modo equivalente sulla statistica $\chi^2$ corrispondente); la scelta della formulazione esatta è demandata all'implementazione, con vincolo di **citazione bibliografica esplicita nel codice di produzione**.

**Soglia $\theta_B$**. La soglia di alert $\theta_B > 0$ è **parametro di tuning operativo**. Per la statistica di Nyblom il valore critico al 5% sotto $H_0$ per un singolo parametro è $\theta_B \approx 0{,}47$ (tabella di Nyblom 1989; corrispondente al quantile 95% della distribuzione asintotica di $L$); per un EGARCH(1,1) con $D$ Student-t i parametri stimati congiuntamente sono nell'ordine di 6 ($\mu, \omega, \alpha, \gamma, \beta, \nu$), e il valore critico congiunto al 5% aumenta corrispondentemente (tabella di Nyblom 1989, valori per $k$ parametri). Il **default proposto per il primo run di produzione** è $\theta_B = $ valore critico al 5% della tabella di Nyblom per il numero di parametri effettivi del modello EGARCH stimato (es. $\theta_B \approx 1{,}68$ per 6 parametri). Il valore è dichiarato **non congelato in Parte VI** e riconsiderato post-go-live sulla base della distribuzione empirica di $B(t)$ osservata nelle prime sessioni di produzione.

**Meccanismo di trigger anticipato**. Se $B(t) > \theta_B$ per più di $T_{B,\text{persist}}$ barre 1-min consecutive (parametro di tuning operativo, valore di **default proposto** $T_{B,\text{persist}} = $ 60 barre $= 1$ ora di trading, **non congelato in Parte VI**), la ricalibrazione EGARCH è anticipata rispetto alla cadenza $T_{recal,\text{EGARCH}}$ fissa: il motore esegue immediatamente la ri-stima sui dati più recenti (con la stessa finestra di calibrazione del bundle frozen), aggiorna i parametri runtime e resetta il counter di $T_{recal,\text{EGARCH}}$. La logica di anticipo è registrata nel log come evento `egarch_recalibration_triggered` con causa (`scheduled` o `parametric_break_alert`), in coerenza con Cap.10 di Parte II.

La separazione **Cap.27.5 (definizione del meccanismo) / Cap.30.4 (calcolo live di $B(t)$ + alert)** è dichiarata esplicitamente: Cap.27.5 dichiara come è costruito $B(t)$, quali sono i parametri e come opera il trigger; Cap.30.4 dichiara come $B(t)$ viene calcolato sul feed real-time barra-per-barra, come viene tracciata la sua serie temporale, e in quali condizioni viene emesso l'alert visualizzato sulla dashboard di Cap.30.6.

---

## Capitolo 28 — Politica anti-doppio-segnale

### 28.1 Citazione del vincolo normativo di Cap.6.3 di Parte II

Il vincolo $|\mathcal{A}(t)| \leq 1$ — a ogni istante $t$ è attivo al massimo un solo segnale — è **vincolo normativo già fissato in Cap.6.3 di Parte II** e non viene modificato da Cap.28. Cap.6.3 lo fonda sui punti 6 e 7 della dichiarazione di intenti dell'operatore (operatività 1 contratto/volta + revisione continua come sostituzione, non come refresh). Cap.28 **estende operativamente** il vincolo: ne definisce il comportamento del motore in due scenari runtime che Cap.6.3 menziona senza esaurirne le regole (politica di non-refresh in presenza di candidati concorrenti con segnale attivo; politica di tie-break deterministico per emissioni simultanee in assenza di segnale attivo).

L'estensione di Cap.28 è **operativa, non normativa**: il vincolo $|\mathcal{A}(t)| \leq 1$ resta quello di Cap.6.3 di Parte II; Cap.28 non lo allenta, non lo rafforza, non lo riformula. Cap.28 fornisce le regole deterministiche del motore in produzione che garantiscono il rispetto del vincolo in ogni edge case.

### 28.2 Politica di non-refresh

Sia $\mathcal{A}(t)$ l'insieme dei segnali attivi al tempo $t$ secondo Cap.6.3 di Parte II. La regola opera come segue.

**Enunciato.** Se al tempo $t$ vale $|\mathcal{A}(t)| = 1$, cioè esiste un segnale $\mathcal{S}_a \in \mathcal{A}(t)$ in stato `active`, e nello stesso istante $t$ il bundle frozen produce un candidate signal $\mathcal{S}_c$ tale che le condizioni di emissione in AND logico di Cap.8 di Parte II e Cap.20 di Parte IV restituiscono vero ($E_{vol}(t) \land E_{liq}(t) \land E_{dist}^{\sigma}(t) \land E_{80\text{pt}}(t) \land E_{surv}(t) = \text{vero}$), allora $\mathcal{S}_c$ è **scartato silenziosamente**. Operativamente:

- **Nessuna notifica Telegram** è inviata all'operatore. L'operatore non viene a conoscenza dell'esistenza del candidato $\mathcal{S}_c$, in coerenza con il vincolo di 3 notifiche standard del canale (emissione, `trigger_event`, transizione terminale) dichiarato in Cap.29.4. Notificare $\mathcal{S}_c$ confonderebbe la decisione di esecuzione manuale del segnale $\mathcal{S}_a$ già pubblicato.
- **Nessuna marcatura speciale** è applicata a $\mathcal{S}_a$: il segnale attivo non viene rinominato, non riceve flag, non vede il proprio payload modificato (in coerenza con l'invariante di payload immutabile di Cap.6.2 di Parte II).
- **Logging nel file di replay** del candidato scartato, con causa esplicita. Il record di log include `signal_id` ipotetico di $\mathcal{S}_c$ (generato deterministicamente come hash dei suoi campi secondo Cap.10 di Parte II per replay), timestamp, snapshot dei filtri al momento, e campo causale `dropped_due_to_active_signal` (terminologia adottata in coerenza con Cap.10.2 di Parte II; varianti equivalenti sono accettabili purché documentate). Il logging permette il replay bit-exact della politica di non-refresh.
- **Lo slot di segnale attivo resta occupato da $\mathcal{S}_a$ fino a transizione a uno degli stati terminali** di Cap.7 di Parte II (`target_1_hit`, `stopped`, `invalidated`, `missed_target`, `expired`, `revoked`). Solo dopo la transizione terminale di $\mathcal{S}_a$, il motore può emettere nuovi segnali. La transizione `active → revoked` rimane prerogativa esclusiva della regola di sostituzione di Cap.6.3 di Parte II (emissione di un nuovo `signal_id` con tupla $\mathcal{S}'$ diversa nei livelli strutturali) e non viene attivata dalla politica di Cap.28.2.

**Motivazione operativa.** La politica di non-refresh è argomentata operativamente, non solo formalmente: l'operatore retail bancario esegue manualmente da cellulare in modo discontinuo (Cap.2 di Parte I); un refresh continuo del segnale con sovrascrittura (anche solo logica, anche senza nuovo Telegram) introdurrebbe ambiguità sul payload effettivo che l'operatore deve eseguire. Inoltre, il principio "1 contratto/volta" del punto 7 della dichiarazione di intenti implica che, una volta che l'operatore ha letto il segnale $\mathcal{S}_a$ e lo sta valutando per l'esecuzione manuale, qualunque ridefinizione del segnale corrente prima del raw touch produrrebbe una decisione operativa difficile da risolvere in tempo reale sul cellulare. La politica di non-refresh elimina questa ambiguità per costruzione: lo slot è occupato fino alla terminazione.

**Edge case di sostituzione legittima (Cap.6.3).** La politica di non-refresh di Cap.28.2 non si confonde con la **regola di sostituzione** di Cap.6.3 di Parte II, che governa il caso in cui il motore valuta che le condizioni strutturali richiedono la revoca esplicita di $\mathcal{S}_a$ (perché $p_{ref}$ è cambiato, perché i target strutturali sono stati ridefiniti dalla nuova geometria, perché il livello di stop non è più coerente). La sostituzione di Cap.6.3 è una scelta architetturale del motore (basata su criteri strutturali specifici), non un riconoscimento di candidato ammissibile generico: la politica di no-refresh di Cap.28.2 scarta i candidati generici che soddisfano i filtri AND ma non soddisfano i criteri di sostituzione strutturale di Cap.6.3. In sintesi: la sostituzione è un evento raro, governato da criteri strutturali; la politica di no-refresh è la regola di default per tutti i candidati che non rientrano nella sostituzione.

### 28.3 Tie-break deterministico per emissioni simultanee

L'edge case considerato è il seguente: al tempo $t$ vale $|\mathcal{A}(t)| = 0$ (nessun segnale attivo) e il bundle frozen produce **due o più candidate signal ammissibili** nello stesso istante $t$, tutti con i filtri AND di Cap.8 di Parte II e Cap.20 di Parte IV verificati. Sotto il vincolo $|\mathcal{A}(t)| \leq 1$ di Cap.6.3 di Parte II, è ammissibile solo l'emissione di **un solo** segnale: si rende necessaria una regola di tie-break deterministica.

**Dichiarazione obbligata anche per bundle a cromosoma singolo.** Il bundle frozen di Parte V (Cap.25-26) produce **un solo cromosoma vincente** dal fronte di Pareto, e in normale operatività i candidati simultanei sono rari (un solo cromosoma genera al massimo un candidato per istante $t$ per direzione). La regola di Cap.28.3 va comunque dichiarata in modo completo per due ragioni: (i) il **replay deterministico bit-exact** di Cap.10 di Parte II richiede che ogni edge case, anche improbabile, sia gestito deterministicamente; (ii) **estendibilità del contratto** verso scenari multi-cromosoma futuri (es. se Parte VII decidesse di promuovere un ensemble di cromosomi del fronte di Pareto), in cui più cromosomi generassero candidati simultanei sulla stessa direzione o su direzioni opposte. La regola di Cap.28 è valida in entrambi i regimi e non richiede revisione se il bundle frozen evolve.

**Ordine di tie-break in 4 livelli, in ordine di precedenza decrescente.**

1. **$\hat{p}_{hit}$ più alto sul candidato**. Si seleziona il candidato $\mathcal{S}_c^*$ tale che $\hat{p}_{hit}(\mathcal{S}_c^*) = \max_c \hat{p}_{hit}(\mathcal{S}_c)$, dove $\hat{p}_{hit}$ è la stima di probabilità di hit del target_1 prodotta dal modello Cox cause-specific di Cap.19.5 di Parte IV, calcolata live sul vettore di feature $\tilde{\mathbf{x}}_t$ del candidato corrispondente (coefficienti del Cox dal fold di calibrazione corrente, stratificazione regime di Cap.25.5 di Parte V preservata). Il candidato con probabilità di hit più alta è atteso essere quello strutturalmente più solido.
2. **In caso di tie su $\hat{p}_{hit}$**, entro tolleranza numerica $\epsilon_p$ (cioè $|\hat{p}_{hit}(\mathcal{S}_{c_1}) - \hat{p}_{hit}(\mathcal{S}_{c_2})| \leq \epsilon_p$), si seleziona il candidato con **`setup_class` $=$ `directional` prima di `trade_range`**. La preferenza è motivata dalla natura strutturale dei setup `directional` (target_1 ancorato a pivot strutturali, distanze in genere maggiori): in tie strutturale, il setup direzionale è preferito al setup trade_range che opera su rettangoli più stretti. $\epsilon_p$ è **parametro tecnico** con valore tipico $10^{-6}$ (tolleranza di confronto in virgola mobile a doppia precisione), **dichiarato in Cap.28.3 ma non congelato in Parte VI**.
3. **In caso di tie ulteriore** (stesso $\hat{p}_{hit}$ entro $\epsilon_p$, stessa `setup_class`), si seleziona il candidato con **$\Delta t_{cromosoma}$ più breve**, dove $\Delta t_{cromosoma}$ è il gene del cromosoma di Cap.6.1 di Parte II. La motivazione è che, in tie strutturale, il candidato con orizzonte temporale post-trigger più breve è meno esposto a deriva di regime durante la fase post-trigger; l'operatore manuale beneficia di un timer più stretto in termini di durata della decisione.
4. **In caso di tie residuo** (improbabile, perché richiede coincidenza esatta di $\hat{p}_{hit}$, `setup_class`, $\Delta t_{cromosoma}$), si applica l'**ordinamento lessicografico crescente del `signal_id`**, generato come hash deterministico dei campi del payload secondo Cap.10 di Parte II. L'ordinamento lessicografico è deterministico per costruzione (l'hash è una funzione deterministica del payload, e due payload distinti producono `signal_id` distinti); la regola garantisce risoluzione di ogni tie senza ricorso a sorgenti non deterministiche (RNG, timestamp wall-clock).

**Convenzione operativa di tie sul livello 1.** Il confine fra livello 1 (selezione per $\hat{p}_{hit}$ massimo) e livello 2 (tie su $\hat{p}_{hit}$) è dichiarato esplicitamente come segue: dati due candidati $\mathcal{S}_{c_1}, \mathcal{S}_{c_2}$, se $|\hat{p}_{hit}(\mathcal{S}_{c_1}) - \hat{p}_{hit}(\mathcal{S}_{c_2})| > \epsilon_p$ allora la selezione è risolta al livello 1 a favore del candidato con $\hat{p}_{hit}$ numericamente maggiore; se $|\hat{p}_{hit}(\mathcal{S}_{c_1}) - \hat{p}_{hit}(\mathcal{S}_{c_2})| \leq \epsilon_p$ allora i due candidati sono considerati in tie sul livello 1 e si applica il livello 2. La convenzione è simmetrica e transitiva per costruzione e garantisce replay bit-exact a parità di valore di $\epsilon_p$ usato dall'implementazione (vincolo Cap.10 di Parte II).

**Esempio numerico di tie-break.** Si considerino due candidati simultanei al tempo $t$, generati da un ipotetico bundle multi-cromosoma: $\mathcal{S}_{c_1}$ con $\hat{p}_{hit} = 0{,}620\,000$, `setup_class` = `trade_range`, $\Delta t_{cromosoma} = 60$ min; $\mathcal{S}_{c_2}$ con $\hat{p}_{hit} = 0{,}620\,000\,3$, `setup_class` = `directional`, $\Delta t_{cromosoma} = 45$ min. Con $\epsilon_p = 10^{-6}$, la differenza $|0{,}620\,000\,3 - 0{,}620\,000| = 3 \cdot 10^{-7} \leq \epsilon_p$: i due candidati sono in tie sul livello 1. Si passa al livello 2: $\mathcal{S}_{c_2}$ ha `setup_class` = `directional` e $\mathcal{S}_{c_1}$ ha `setup_class` = `trade_range`, quindi $\mathcal{S}_{c_2}$ è selezionato. Se invece $\epsilon_p = 10^{-9}$, la stessa differenza $3 \cdot 10^{-7} > \epsilon_p$ farebbe vincere $\mathcal{S}_{c_2}$ direttamente al livello 1 (per $\hat{p}_{hit}$ marginalmente maggiore). L'esempio rende esplicita la dipendenza del replay dal valore di $\epsilon_p$ adottato in produzione.

La regola di tie-break opera **prima** dell'emissione: si seleziona deterministicamente il candidato $\mathcal{S}_c^*$ e si emette solo quello; i candidati scartati per tie-break sono **loggati con causa esplicita `dropped_due_to_tiebreak_loss`** (terminologia di esempio, coerente con Cap.10.2 di Parte II), per replay bit-exact.

### 28.4 Determinismo del replay e logging dei candidati

Il replay deterministico bit-exact di Cap.10 di Parte II è garantito dalla pipeline di Cap.27 e dalla politica di Cap.28 sotto le seguenti condizioni di logging.

**Per ogni candidato signal generato dal bundle frozen al tempo $t$** (emesso o scartato), il file di log di Parte VI registra:

- `signal_id` (anche se il candidato non viene emesso, l'identificatore è prodotto deterministicamente come hash dei campi del payload secondo Cap.10 di Parte II — permette di tracciare il candidato univocamente nel log);
- `timestamp` del candidato (minuto chiuso CET);
- **stato di gating**: campo strutturato con valore in $\{\texttt{accepted}, \texttt{dropped\_due\_to\_active\_signal}, \texttt{dropped\_due\_to\_tiebreak\_loss}, \texttt{dropped\_due\_to\_filter\_fail}\}$ (terminologia di esempio adottata in Cap.28 e Cap.27; varianti equivalenti sono accettabili purché documentate nello schema del log di Parte VI in Appendice E);
- **output dei filtri AND** di Cap.8 di Parte II + Cap.20 di Parte IV: valori scalari di $r_{1m}, v_{1m}, |\texttt{target\_1} - p_{ref}|/\hat{\sigma}_{\text{pt}}, \hat{p}_{hit}$ e flag booleano per ciascuna delle 5 condizioni $E_{vol}, E_{liq}, E_{dist}^{\sigma}, E_{80\text{pt}}, E_{surv}$;
- **payload integrale** del candidato (tutti i campi di Cap.6.1 di Parte II), anche se scartato;
- **identificatore di versione** del bundle frozen e seed di Cap.26.8 di Parte V.

Il replay offline sullo **stesso feed Directa DAPI** (o sullo stesso file di feed registrato) e **stesso bundle frozen** riproduce **bit-exact** la stessa sequenza di emissioni e di scarti, inclusa la sequenza dei `signal_id`, gli stati di gating, e i tie-break risolti. La verifica è strumentale per la validazione delle metriche live di Cap.30 (che usano i log di replay come fonte canonica) e per la riproducibilità delle decisioni del motore in caso di audit interno.

**Nessun valore numerico congelato di Parte VI in Cap.28.** $\epsilon_p$ è dichiarato come parametro tecnico di tolleranza in virgola mobile con valore tipico $10^{-6}$ ma **non congelato**: il valore esatto è demandato all'implementazione e riconsiderato post-go-live se la distribuzione empirica di $\hat{p}_{hit}$ in produzione mostra tie frequenti a precisione superiore a $\epsilon_p$.

---

## Capitolo 29 — Gestione dell'operatività su mobile

### 29.1 Vincoli operativi mobile-first

Il canale di pubblicazione dei segnali è il **bot Telegram personale dell'operatore**, dichiarato come **unica via di output verso l'operatore** in Cap.3 di Parte I. L'operatore è un risk manager bancario italiano, retail non professionale MiFID II, che esegue manualmente da cellulare in modo discontinuo durante la giornata lavorativa (Cap.2 di Parte I, eredità del punto 7 della dichiarazione di intenti — 1 contratto/volta, esecuzione manuale, separazione segnale/gestione posizione). La progettazione del messaggio Telegram in Cap.29 risponde direttamente a questo profilo operativo: il payload formale di Cap.6.1 di Parte II viene **rappresentato** in un layout mobile-first ottimizzato per lettura su schermo cellulare in condizioni di attenzione limitata.

Il **contenuto formale del messaggio** è quello di **Cap.9.2 di Parte II** a **9 voci pubblicate ordinate** (Iterazione 5 di Cap.9.2: `signal_id, direction, setup_class, entry_zone, target_1, target_2, stop_loss, timestamp_emission, target_2_type, stop_type`, dove `target_2_type` e `stop_type` sono i qualificatori $\in \{\text{structural}, \text{synthetic}\}$ aggiunti in Iterazione 5). Cap.29 **non duplica** Cap.9.2 di Parte II — Cap.9.2 resta il riferimento normativo del contenuto del messaggio. Cap.29 **estende la rappresentazione visiva** delle stesse 9 voci, riordinandole per priorità di lettura mobile e adottando abbreviazioni standard. **Nessun campo nuovo viene introdotto nel payload formale**: il payload di Cap.6.1 di Parte II Iterazione 4 resta esattamente quello pubblicato e quello loggato. La distinzione operativa è dichiarata esplicitamente: **payload formale (immutabile, Cap.6.1 di Parte II) vs rappresentazione mobile (cosmetica, Cap.29)**.

**Vincolo di latenza Telegram (qualitativo).** La latenza $L$ di consegna del messaggio Telegram (da `timestamp_emission` alla ricezione sul cellulare) deve restare entro un valore $L_{max}$ qualitativo coerente con l'utilità operativa del segnale, in coerenza con Cap.9.3 di Parte II (valore di lavoro provvisorio $L_{max} = 30$ s). Cap.29 cita il vincolo qualitativamente come obiettivo di progettazione del canale Telegram; la **verifica numerica empirica** di $L_{max}$ effettivo resta carryover di **Appendice E** (M-2 OPEN, Review v1 CAP-02): **Cap.29 non risolve numericamente $L_{max}$ in Parte VI**.

**Vincoli tecnici di leggibilità mobile.** Il layout del messaggio è progettato per schermi mobile di larghezza tipica 375-414 px (intervallo coperto da gran parte dei dispositivi iOS/Android in uso commerciale), font monospaziato di Telegram (corretto per allineamento di valori numerici tabellari), messaggio leggibile **senza scroll orizzontale** (linee corte), contenuto critico (direzione, entry_zone, target_1, stop_loss) visibile **senza scroll verticale eccessivo** (entro la prima schermata). L'uso di Markdown limitato del bot Telegram (bold per la direzione, monospace per i valori numerici) è ammesso; nessuna immagine, nessun media allegato, nessun link esterno: il messaggio è interamente testuale e self-contained.

### 29.2 Layout mobile-first del messaggio di emissione

Le 9 voci pubblicate di Cap.9.2 di Parte II Iterazione 5 sono riordinate per **priorità di lettura mobile**: i campi che richiedono decisione operativa immediata in posizione alta (visibili senza scroll), i campi di contesto e qualificazione in posizione bassa. **Il numero totale di voci pubblicate è esattamente 9**, identico al contratto di Cap.9.2 di Parte II Iterazione 5 (`signal_id, direction, setup_class, entry_zone, target_1, target_2, stop_loss, timestamp_emission, target_2_type, stop_type` con `target_1` e `target_2` raggruppate alla voce 5 secondo Cap.9.2 paragrafo 247): nessuna voce aggiuntiva, nessuna voce omessa.

**Convenzione di posizionamento del `signal_id`.** Per coerenza normativa rigorosa con Cap.9.2 di Parte II Iterazione 5 (che colloca `signal_id` in posizione 1 come "identificatore del segnale, riportato in chiaro come chiave operativa", paragrafo 243), il layout mobile-first di Cap.29.2 pubblica `signal_id` come **prima voce di intestazione** (testa del messaggio, abbreviato per leggibilità mobile ai primi 6-8 caratteri dell'hash deterministico). La convenzione è dichiarata esplicitamente: `signal_id` in testa permette all'operatore di identificare immediatamente il segnale nello scroll della cronologia Telegram e mantiene l'ordinamento normativo di Cap.9.2 al primo posto; il riordino successivo riguarda solo le 8 voci di contenuto operativo.

Ordinamento delle 9 voci di Cap.9.2 di Parte II Iterazione 5 per priorità mobile:

1. **`signal_id`** — identificatore abbreviato in testa, formato `ID: <prefisso6-8>` (primi 6-8 caratteri dell'hash deterministico del payload secondo Cap.10 di Parte II), sufficiente per disambiguazione visiva fra emissioni successive.
2. **`direction`** — LONG o SHORT in caps, evidenza visiva forte (Markdown bold quando ammesso dal bot).
3. **`entry_zone`** — banda numerica formattata come intervallo discreto $[p_{ref} - b, p_{ref} + b]$ in punti FIB, valori multipli di 5 per costruzione (Cap.6.1 di Parte II + tick FIB 5 pt Cap.5 di Parte I).
4. **`target_1`** — prezzo in punti FIB e **distanza dal centro della banda** $|\texttt{target\_1} - p_{ref}|$ in pt, formato `TGT1: <prezzo> (<+/-distanza> pt)` per leggibilità immediata della distanza operativa.
5. **`stop_loss`** — prezzo in punti FIB e distanza $d_{stop} = |p_{ref} - \texttt{stop\_loss}|$ in pt, formato `SL: <prezzo> (<+/-distanza> pt)`.
6. **`target_2`** con qualificatore **`target_2_type`** ($\in \{\text{structural}, \text{synthetic}\}$ di Cap.6.1 di Parte II Iterazione 4 + Cap.9.2 Iterazione 5), formato `TGT2: <prezzo> (<S|s>)` dove `S` indica `structural` e `s` indica `synthetic`. La voce `target_2_type` di Cap.9.2 paragrafo 250 è qui pubblicata insieme al valore di `target_2` come qualificatore in linea, in coerenza con la rappresentazione mobile compatta.
7. **`stop_type`** con qualificatore $\in \{\text{structural}, \text{synthetic}\}$ di Cap.6.1 di Parte II Iterazione 4 + Cap.9.2 Iterazione 5 (paragrafo 251), associato a `stop_loss` con notazione analoga, es. `SL-type: structural`.
8. **`setup_class`** $\in \{\text{directional}, \text{trade\_range}\}$, abbreviato come `CLASS: dir` o `CLASS: range`.
9. **`timestamp_emission`** in CET, formato `EMIT: <HH:MM> CET` (minuto chiuso secondo Cap.6.1 di Parte II).

I campi $\Delta t_{cromosoma}$ e $T_{touch}^{max}$ (geni del cromosoma di Cap.6.1 di Parte II) **non figurano nel messaggio Telegram** in coerenza con il paragrafo 253 di Cap.9.2 di Parte II Iterazione 5, che li dichiara esplicitamente "parametri tecnici del modello rilevanti per il log interno (Cap.10) ma non per la decisione operativa dell'operatore". La loro inclusione nel layout di Cap.29.2 sarebbe estensione del contratto informativo di Cap.9.2 di Parte II Iterazione 5 e violerebbe il principio "payload formale (immutabile, Cap.6.1) vs rappresentazione mobile (cosmetica, Cap.29)" dichiarato in Cap.29.1: la rappresentazione mobile riordina le voci pubblicate, non ne aggiunge di nuove. Il layout pubblica esattamente le 9 voci di Cap.9.2 di Parte II Iterazione 5; nient'altro.

**Esempio numerico completo del messaggio di emissione** (rispetta tick FIB 5 pt, valori multipli di 5):

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

Tutti i valori numerici dell'esempio sono multipli di 5 (Cap.5 di Parte I + Cap.6.1 di Parte II). Il `timestamp_emission` è formattato al minuto chiuso CET in coerenza con Cap.6.1 di Parte II. La lettura sul cellulare richiede una sola schermata mobile e permette all'operatore di leggere `signal_id`, direzione, banda e distanze in pochi secondi.

### 29.3 Notifica `trigger_event` come messaggio separato

Al verificarsi del raw touch della `entry_zone` (Cap.7.3 di Parte II), il motore pubblica una **notifica `trigger_event` come messaggio Telegram separato** dal messaggio di emissione, in coerenza con Cap.9.5 di Parte II. Il messaggio è distinto, ha `signal_id` esplicito (riferimento al segnale originario), e non modifica il messaggio di emissione (no edit, no append; conserva l'invariante di payload immutabile di Cap.6.2 di Parte II).

**Contenuto minimo della notifica `trigger_event`**:

- riferimento al **`signal_id`** del segnale originario (footer abbreviato come nel messaggio di emissione, es. `ID: a3f7d9`);
- **timestamp del trigger** $t_{exec}$ in CET (minuto chiuso);
- **prezzo di trigger** in punti FIB (il livello della `entry_zone` toccato per primo dalla barra 1-min, Cap.7.3 di Parte II);
- **$\Delta t$ pre-trigger** $= t_{exec} - t_{emission}$ in minuti di trading (campo esplicito separato da $\Delta t_{cromosoma}$, in coerenza con il campo `t_exec` e con la definizione $\Delta t_{pretrigger}$ di Cap.24.5 di Parte V — chiusura N-4 v2);
- **conferma dello stato `active`** post-trigger: il segnale resta in stato `active` (Cap.7 di Parte II), il `trigger_event` è un evento, non una transizione di stato (Cap.7.3 di Parte II).

**Esempio numerico completo della notifica `trigger_event`**:

```
TRIGGER
ID: a3f7d9
TRIG: 11:18 CET @ 13.255
WAITED: 36min pre-trig
STATUS: active
```

Il valore `13.255` è multiplo di 5 (tick FIB Cap.5 di Parte I); il `timestamp` del trigger è formattato al minuto chiuso CET in coerenza con Cap.6.1 di Parte II; `WAITED: 36min pre-trig` è la fase di attesa $\Delta t_{pretrigger}$ in minuti di trading.

### 29.4 Gestione duplicati di lettura e idempotenza

L'operatore retail bancario può aprire l'app Telegram più volte nella giornata, può scorrere indietro nella cronologia della chat per consultare segnali emessi in precedenza, può ricevere notifiche push ritardate per limiti di connettività mobile. La gestione di questi casi è interamente affidata al modello di interazione del bot Telegram, non a logica di motore:

- **Il messaggio di emissione resta invariato** dopo la pubblicazione (no edit del messaggio originale da parte del motore, no append, no aggiornamento). L'invariante di payload immutabile di Cap.6.2 di Parte II vale anche sulla rappresentazione mobile: modificare il messaggio Telegram pubblicato sarebbe equivalente a modificare il payload pubblicato, violando l'invariante.
- **Il `signal_id` deterministico** (hash dei campi del payload secondo Cap.10 di Parte II) permette **disambiguazione visiva fra emissioni successive**: l'operatore che scorre la cronologia distingue i segnali per `signal_id` (footer abbreviato) anche se hanno direzione o setup_class identici.
- **Nessuna notifica Telegram di "stato corrente del segnale"** è inviata in modo continuativo: il canale pubblica **esattamente 3 notifiche standard per segnale**: (i) emissione (Cap.29.2); (ii) `trigger_event` se avviene il raw touch (Cap.29.3); (iii) transizione a stato terminale (Cap.29.5). Tra una notifica e la successiva, l'operatore non riceve aggiornamenti di stato: il segnale è monitorato silenziosamente dal motore e l'operatore segue lo stato sul terminale Telegram in modo statico (no polling, no refresh).
- **La politica anti-duplicato di Cap.9.4 di Parte II** garantisce che ogni `signal_id` sia pubblicato una sola volta sul canale (anche in caso di restart del motore, l'insieme persistito $\mathcal{P}$ dei `signal_id` pubblicati impedisce ripubblicazione).

### 29.5 Notifica di transizione terminale

Alla transizione del segnale da `active` a uno degli stati terminali di Cap.7 di Parte II (`target_1_hit`, `stopped`, `invalidated`, `missed_target`, `expired`, `revoked`), il motore pubblica un **messaggio Telegram di chiusura** che informa l'operatore della conclusione del contratto del segnale e del risultato.

**Contenuto minimo della notifica di transizione terminale**:

- riferimento al **`signal_id`** del segnale (footer abbreviato);
- **stato terminale finale**, uno dei 6 di Cap.7.1 di Parte II;
- **prezzo del trigger** se applicabile (valore di chiusura del segnale: per `target_1_hit` il prezzo di target_1; per `stopped` il prezzo di stop_loss; per `expired` il prezzo dell'ultima barra del timer; per `invalidated` o `missed_target` il prezzo che ha innescato la condizione; per `revoked` nessun prezzo, ma riferimento al `signal_id` del segnale sostituto);
- **$R_{gross}$** in punti FIB (positivo, negativo o nullo), calcolato come differenza fra il prezzo di chiusura e il prezzo di fill virtuale (definizione Cap.7.3 di Parte II; uso nel log di chiusura Cap.10.4 di Parte II) per i segnali eseguiti; vuoto o `n/a` per i segnali non eseguiti (`invalidated`, `missed_target`, `revoked` pre-trigger).

**Esempio numerico completo della notifica di transizione terminale** (caso `target_1_hit` di un segnale LONG eseguito con $R_{gross} = +95$ pt):

```
CLOSE
ID: a3f7d9
STATE: target_1_hit
PRICE: 13.350
R_gross: +95 pt
```

Tutti i valori numerici dell'esempio sono multipli di 5 (tick FIB Cap.5 di Parte I).

---

## Capitolo 30 — Monitoraggio del lifecycle in produzione

### 30.1 Metriche di fitness live

Il monitoraggio del lifecycle in produzione calcola **counterpart live** delle metriche di fitness del NSGA-II di **Cap.24.1 di Parte V**. Cap.30.1 tratta le quattro metriche marginali $f_1, f_2, f_3, f_4$, calcolate su una **finestra rolling di produzione** $W_{prod}$ che aggrega i segnali emessi nelle sessioni più recenti; la quinta metrica $f_5$ (stabilità cross-regime) è trattata separatamente in Cap.30.3 come metrica a frequenza più bassa, in coerenza con la sua natura intrinseca di disparità fra due sottoinsiemi (calmo vs turbolento). La definizione delle metriche live coincide formalmente con quella di Cap.24.1; cambia il dominio di calcolo (segnali di produzione invece che fold OOS del walk-forward).

$W_{prod}$ è **parametro di tuning operativo** con dominio temporale tipico di alcune settimane-mese di trading; il **default proposto per il primo run di produzione** è $W_{prod} = 21$ sessioni di trading rolling di 8:00-22:00 CET ($\approx$ 1 mese calendario di FIB, totale 17.640 barre 1-min), coerente con la cadenza di ricalibrazione EGARCH proposta in Cap.27.5 e con la persistenza del flag di regime di Cap.25.4 di Parte V. Il valore è dichiarato **non congelato in Parte VI** e riconsiderato post-go-live sulla base degli esiti empirici di stabilità delle metriche live.

Le 4 metriche live sono:

- **$f_1^{live}(t) = E[R_{net} \mid \text{executed}]$** su $W_{prod}$. Media empirica del rendimento netto in punti FIB sui segnali eseguiti del fold di produzione rolling. La definizione di $R_{net}$ include il commissioning $c = 1$ pt FIB equivalente per operazione (eredità Cap.2 di Parte I, conversione 5 EUR commissione / 5 EUR per punto FIB), coerente con la formula di Cap.24.1 di Parte V: $f_1 = E[R_{gross} \mid \text{executed}] - 2c$. La nomenclatura `executed`, la gestione dei segnali in stato terminale `expired posttrigger_timeout` (chiusura virtuale forzata), e l'esclusione dei segnali non eseguiti (`invalidated`, `missed_target`, `revoked`) sono identiche a Cap.24.1 di Parte V.
- **$f_2^{live}(t)$** $=$ target_1 hit rate su $W_{prod}$. Frazione di segnali in stato terminale `target_1_hit` sul totale dei segnali eseguiti del fold di produzione rolling. Denominatore: $|\{i : \text{executed}(s_i)\}|$ secondo Cap.24.1 di Parte V (include `target_1_hit, stopped, expired posttrigger_timeout`).
- **$f_3^{live}(t)$** $=$ invalidation rate pre-touch su $W_{prod}$. Frazione di segnali in stato terminale `invalidated` sul totale dei segnali emessi del fold rolling. Denominatore: $|\{i : \text{emitted}(s_i)\}|$ secondo Cap.24.1 di Parte V.
- **$f_4^{live}(t)$** $=$ maximum drawdown intraday dell'equity sintetica calcolata su $W_{prod}$. Definizione coerente con Cap.24.1 di Parte V: $f_4 = \max_t (\text{eq}_t^{peak} - \text{eq}_t)$ con $\text{eq}_t$ somma cumulativa di $R_{net}$ per i segnali eseguiti del fold ordinati per $t_{exec}$.

Le 4 metriche live sono calcolate aggiornandosi a ogni nuovo segnale che entra in stato terminale all'interno di $W_{prod}$. Il calcolo utilizza come fonte canonica il file di log di replay prodotto dalla pipeline di Cap.27 (logging deterministico bit-exact di Cap.10 di Parte II), che contiene tutti i campi necessari (payload, $R_{gross}$, $R_{net}$, stato terminale, $t_{emission}, t_{exec}$).

### 30.2 Confronto con distribuzione cross-fold del walk-forward

Per ciascuna metrica live $f_m^{live}(t)$ con $m \in \{1, 2, 3, 4\}$, il confronto con la **distribuzione cross-fold** $\{f_{m,k}\}_{k=1}^{F}$ delle stesse metriche aggregate sui $F = 8$ fold del walk-forward nested di **Cap.25 di Parte V** (eredità Cap.25.1 con $F = 8$ provvisorio) produce una **misura di deriva** del bundle frozen rispetto al regime di mercato corrente.

La **soglia di deriva** è basata sull'**intervallo interquartile** $[Q_1, Q_3]$ della distribuzione cross-fold dei $F = 8$ fold del walk-forward, calcolato per ciascuna delle 4 metriche separatamente. L'intervallo IQR è preferito a soglie basate su media $\pm k \sigma$ perché robusto a fold con metrica degenere o regime atipico (la mediana e l'IQR sono già le metriche cross-fold robuste preferite in Cap.24.6 di Parte V).

**Regola di alert**. Si emette un alert di deriva sulla metrica $f_m^{live}$ se vale:
$$f_m^{live}(t) \notin [Q_1(\{f_{m,k}\}_{k=1}^{F}), Q_3(\{f_{m,k}\}_{k=1}^{F})] \quad \text{per più di } T_{drift,\text{persist}} \text{ giorni di trading consecutivi}$$

dove $T_{drift,\text{persist}}$ è **parametro di tuning operativo** con dominio tipico alcuni giorni di trading; il **default proposto per il primo run di produzione** è $T_{drift,\text{persist}} = 5$ giorni di trading consecutivi (filtro anti-falsi-positivi: un singolo giorno fuori IQR non genera alert, ma una settimana di trading consecutiva sì). Il valore è dichiarato **non congelato in Parte VI** e riconsiderato post-go-live.

L'alert è visualizzato sulla dashboard di Cap.30.6 con riferimento esplicito alla metrica derivata, al valore live, ai valori $Q_1, Q_3$ della distribuzione cross-fold, e al numero di giorni di trading consecutivi fuori intervallo. **L'alert non chiude il loop di re-training**: la decisione di ritraining del GA in risposta a deriva persistente è materia di Parte VII Cap.36 (gate decisionali post-go-live), non di Cap.30.

### 30.3 Metrica $f_5^{live}$ — stabilità cross-regime live

Cap.30.3 calcola live la **contropartita live di $f_5$ stabilità cross-regime** (quinto obiettivo del NSGA-II di **Cap.24.1 di Parte V**, definizione paragrafo 261-263: $f_5(\theta) = |f_1^{calmo}(\theta) - f_1^{turbolento}(\theta)| / \max(|f_1^{calmo}(\theta)|, |f_1^{turbolento}(\theta)|, 1)$), come metrica di lifecycle a **frequenza più bassa** rispetto a $f_1^{live}$-$f_4^{live}$ di Cap.30.1.

**Definizione di $f_5^{live}(t)$**. Sulla finestra rolling di produzione $W_{prod}$ (Cap.30.1, default proposto 21 sessioni di 8:00-22:00 CET) si segmenta l'insieme dei segnali eseguiti del fold rolling in due sottoinsiemi sulla base della **classificazione regime live $R_{t_{emission,i}} \in \{\text{calmo}, \text{turbolento}\}$** (Cap.14 di Parte III, classificazione prodotta dal blocco 5 della pipeline di Cap.27.1) al momento dell'emissione del segnale $i$-esimo. Si calcolano le due medie condizionate
$$f_1^{calmo,live}(t) = E[R_{net} \mid \text{executed}, R_{t_{emission}} = \text{calmo}] \quad \text{su } W_{prod}$$
$$f_1^{turbolento,live}(t) = E[R_{net} \mid \text{executed}, R_{t_{emission}} = \text{turbolento}] \quad \text{su } W_{prod}$$
e si definisce
$$f_5^{live}(t) = \frac{|f_1^{calmo,live}(t) - f_1^{turbolento,live}(t)|}{\max(|f_1^{calmo,live}(t)|, |f_1^{turbolento,live}(t)|, 1)}$$
coerentemente con la formula di Cap.24.1 di Parte V applicata al fold di produzione rolling al posto del fold OOS del walk-forward.

**Frequenza di calcolo più bassa di $f_1$-$f_4$**. Diversamente da $f_1^{live}$-$f_4^{live}$ che si aggiornano a ogni segnale che entra in stato terminale all'interno di $W_{prod}$, $f_5^{live}$ richiede **una popolazione minima per ciascun regime** nei due sottoinsiemi per essere statisticamente significativa: il calcolo è eseguito **al massimo una volta per giornata di trading** (es. end-of-session aggregato), e solo quando la cardinalità del sottoinsieme meno rappresentato sui segnali eseguiti del $W_{prod}$ corrente supera una soglia minima $N_{reg,\min}^{live}$ (parametro di tuning operativo, valore di **default proposto** $N_{reg,\min}^{live} = 10$ segnali eseguiti per ogni regime, **non congelato in Parte VI**). Se $N_{reg,\min}^{live}$ non è soddisfatto in entrambi i regimi sul $W_{prod}$ corrente, $f_5^{live}(t)$ è dichiarato `n/a` per quell'aggiornamento; il calcolo viene ripetuto quando il pool di segnali raggiunge la soglia.

**Confronto con la distribuzione cross-fold di $f_5$**. Anche $f_5^{live}$ ammette confronto con la distribuzione $f_5^{global}$ del walk-forward di **Cap.24.6 di Parte V** (paragrafo 330: $f_5^{global}$ calcolato concatenando tutti i segnali OOS dei $F = 8$ fold separati per regime). La distribuzione di riferimento di $f_5$ è puntuale (uno scalare $f_5^{global}$ aggregato) e non un IQR cross-fold come per $f_1$-$f_4$: di conseguenza la soglia di deriva di Cap.30.2 (intervallo IQR cross-fold) non è direttamente applicabile a $f_5^{live}$. Si emette **alert di deriva di stabilità cross-regime** se $f_5^{live}(t) > f_5^{global} \cdot (1 + \alpha_{f_5})$ per più di $T_{drift,\text{persist}}$ giorni di trading consecutivi, con $\alpha_{f_5}$ parametro di tuning operativo (tolleranza relativa, valore di **default proposto** $\alpha_{f_5} = 0{,}25$ — incremento del 25% rispetto al valore di walk-forward, **non congelato in Parte VI**). La motivazione è che un cromosoma frozen calibrato per stabilità cross-regime $f_5^{global}$ può degradare la propria stabilità in produzione (es. shock di mercato che modifica la distribuzione dei regimi calmo/turbolento) senza che gli alert di Cap.30.2 lo rilevino — gli alert di Cap.30.2 monitorano $f_1$-$f_4$ marginali, non la disparità cross-regime di $f_1$.

**Impatto sul GA**. Il NSGA-II di Cap.24.1 di Parte V ha selezionato il cromosoma frozen tenendo conto di $f_5$ insieme a $f_1$-$f_4$ come quinto obiettivo del fronte di Pareto. Senza $f_5^{live}$ il monitoraggio della deriva è incompleto su uno dei 5 assi di selezione: un bundle frozen può conservare $f_1^{live}$-$f_4^{live}$ entro $[Q_1, Q_3]$ ma degradare $f_5^{live}$ in modo che la disparità $|f_1^{calmo} - f_1^{turbolento}|$ aumenti — segnale strutturale di deriva del regime non visibile dalle metriche marginali. Cap.30.3 chiude esplicitamente questa lacuna.

### 30.3bis Metriche di lifecycle tracciate (eredità Cap.24.3 di Parte V)

Cap.30.3bis traccia live le **metriche di lifecycle aggiuntive** di **Cap.24.3 di Parte V**, prodotte dalla submacchina position lifecycle di Cap.11 di Parte II. Queste metriche sono di **reporting**, non producono alert (in coerenza con Cap.24.3 di Parte V: non sono obiettivi diretti del NSGA-II, ma indicatori di qualità informativa del payload).

- **$\pi_{t_2 \mid t_1}^{live}(t)$** — target_2 hit rate condizionale al raggiungimento di target_1, calcolato sui segnali del fold di produzione rolling $W_{prod}$ che hanno raggiunto `target_1_hit` e per i quali la submacchina position lifecycle di Cap.11.3 di Parte II ha registrato l'evento `target_2_reached` prima di altri eventi terminanti della submacchina.
- **MFE/MAE aggregati live** — distribuzioni di maximum favourable excursion e maximum adverse excursion misurate dal momento del `trigger_event` $t_{exec}$ alla chiusura del segnale (per i segnali eseguiti), secondo la definizione di Cap.10.4 di Parte II. La submacchina position lifecycle di Cap.11.2 di Parte II traccia inoltre MFE/MAE post-target_1 (dal momento di `target_1_hit` alla chiusura della submacchina) per i segnali che hanno raggiunto target_1: anche queste distribuzioni sono tracciate live.
- **$f_{stop \mid t_1}^{live}(t)$** — frequenza di stop post-target_1, frazione di segnali in `target_1_hit` per cui la submacchina ha registrato l'evento `stop_after_target_1` (ritracciamento del prezzo fino al livello `stop_loss` originale dopo `target_1_hit`).

Tali metriche entrano nella dashboard di Cap.30.6 come **tabelle/grafici di reporting**, senza soglie di alert. Servono al supervisore come segnale di qualità informativa del payload pubblicato (Cap.24.3 di Parte V e Cap.11.4 di Parte II: un bundle con $\pi_{t_2 \mid t_1}$ live basso e $f_{stop \mid t_1}$ alto rivela setup strutturalmente fragili, indipendentemente dalla fitness $f_1$-$f_4$).

### 30.4 Calcolo live del flag di break parametrico $B(t)$ e alert

Cap.30.4 chiude la parte **calcolo live + alert** del residuo di **M-2 v2 Review v2 CAP-03** (decisione di scope Planner: Cap.27.5 dichiara il meccanismo, Cap.30.4 calcola live e produce alert).

Il flag $B(t)$ definito in **Cap.27.5** (statistica di Nyblom 1989 sui residui standardizzati del modello EGARCH, formulazione equivalente accettata) viene **calcolato live sul feed real-time barra-per-barra** nella finestra $[t - W_B, t]$ con $W_B$ ampiezza tipica 1-5 sessioni di trading (default proposto $W_B = 3$ sessioni). La pipeline di Cap.27 espone $B(t)$ come output diagnostico del blocco (4) (inference EGARCH) e Cap.30.4 ne traccia la serie temporale nella dashboard di Cap.30.6.

**Regola di alert**. Si emette un alert di break parametrico EGARCH se vale:
$$B(t) > \theta_B \quad \text{per più di } T_{B,\text{persist}} \text{ barre 1-min consecutive}$$

con $\theta_B$ soglia di tuning operativo (default proposto basato sul valore critico al 5% della tabella di Nyblom 1989 per il numero di parametri effettivi del modello EGARCH stimato, **non congelato in Parte VI**, vedi Cap.27.5) e $T_{B,\text{persist}}$ parametro di tuning operativo (default proposto $T_{B,\text{persist}} = 60$ barre $= 1$ ora di trading, **non congelato in Parte VI**, vedi Cap.27.5).

L'alert su Cap.30.4 ha due effetti operativi: (i) **visualizzazione nella dashboard** di Cap.30.6 con riferimento alla finestra di superamento e al valore di $B(t)$; (ii) **anticipo della ricalibrazione EGARCH** rispetto alla cadenza fissa $T_{recal,\text{EGARCH}}$ definita in Cap.27.5 (trigger anticipato). La logica di anticipo è eseguita dalla pipeline di Cap.27 (Cap.27.5 enuncia la regola: $B(t) > \theta_B$ per $T_{B,\text{persist}}$ barre $\Rightarrow$ ricalibrazione anticipata + reset counter $T_{recal,\text{EGARCH}}$); l'evento è loggato come `egarch_recalibration_triggered` con causa `parametric_break_alert` (Cap.27.5).

### 30.5 Frequenza di emissione e alert di deriva del cromosoma

Cap.30.5 traccia live la **frequenza di emissione** $r_{emit}^{live}(t)$, definita come numero medio di segnali emessi per sessione di trading sul fold di produzione rolling $W_{prod}$. La metrica è la counterpart live di $E_{rate}$ utilizzata in **Cap.24.2 di Parte V** per le penalità integrate nella fitness (penalità emissione eccessiva $E_{max}$ e penalità emissione nulla $E_{min}$).

**Soglie ereditate**. Le soglie $E_{max} = 5$ segnali/sessione e $E_{min} = 0{,}2$ segnali/sessione sono **ereditate da Cap.26.5 di Parte V già congelate** e Cap.30.5 le **riusa** senza ridichiararle. Allo stesso modo $E_{exp,max} = 0{,}30$ (penalità lifecycle anomalo, Cap.24.2 di Parte V) è ereditata già congelata.

**Regola di alert**. Si emette un alert di **deriva del cromosoma** rispetto al regime di training se vale almeno una delle seguenti condizioni:
- $r_{emit}^{live}(t) > E_{max} = 5$ segnali/sessione per più di $T_{emit,\text{persist}}$ giorni di trading consecutivi (cromosoma sovra-emittente: il bundle frozen sta emettendo troppi segnali rispetto al regime di mercato corrente, possibile deriva delle soglie del filtro AND);
- $r_{emit}^{live}(t) < E_{min} = 0{,}2$ segnali/sessione per più di $T_{emit,\text{persist}}$ giorni di trading consecutivi (cromosoma silente: il bundle frozen non emette segnali sufficienti, possibile deriva del regime fuori dal dominio di calibrazione).

dove $T_{emit,\text{persist}}$ è **parametro di tuning operativo** con dominio tipico alcuni giorni di trading; il **default proposto per il primo run di produzione** è $T_{emit,\text{persist}} = 10$ giorni di trading consecutivi (filtro anti-falsi-positivi su singole sessioni atipiche). Il valore è dichiarato **non congelato in Parte VI** e riconsiderato post-go-live.

**Motivazione operativa.** Una frequenza di emissione fuori dai bound $[E_{min}, E_{max}]$ in modo persistente è il segnale principale di **deriva del bundle frozen** rispetto al regime di mercato in produzione: i geni del cromosoma sono ottimizzati per la distribuzione di regimi del walk-forward (Cap.25 di Parte V), e un cambio strutturale del regime di mercato in produzione che porti la frequenza fuori da $[E_{min}, E_{max}]$ indica che le penalità di Cap.24.2 di Parte V starebbero spingendo il GA a riallocare il cromosoma in modo diverso, ma il bundle frozen non viene ri-ottimizzato in produzione (vincolo Cap.27.3). L'alert di Cap.30.5 è informativo per il supervisore: la **decisione di re-training del GA** in risposta a deriva persistente è materia di **Parte VII Cap.36** (gate decisionali post-go-live), non di Cap.30. Cap.30 emette alert; non chiude il loop.

### 30.6 Dashboard di sintesi lato motore

La **dashboard di Cap.30** è **lato motore** (PC dell'operatore, eventualmente esposta via interfaccia web locale o file di log + visualizzazione offline), **non sul cellulare**. Il cellulare riceve **esclusivamente Telegram** (Cap.3 di Parte I, eredità Cap.29.4: 3 notifiche standard per segnale). Cap.30.6 non aggiunge alcuna interazione del cellulare con il monitoring di lifecycle: l'operatore retail bancario è già impegnato manualmente sulla decisione di esecuzione del segnale via Telegram, e duplicare le metriche di monitoring sul cellulare confonderebbe il vincolo "1 contratto/volta" (Cap.2 di Parte I) e violerebbe la separazione segnale/gestione posizione.

**Contenuto della dashboard lato motore**:

- **Tabella delle 4 metriche live $f_1$-$f_4$** di Cap.30.1 con valore corrente, $Q_1, Q_3$ della distribuzione cross-fold di Cap.30.2, giorni consecutivi fuori intervallo, flag di alert attivo.
- **Riga dedicata a $f_5^{live}$ stabilità cross-regime** di Cap.30.3 con valore corrente, cardinalità dei due regimi (calmo/turbolento) sul $W_{prod}$ corrente, valore di riferimento $f_5^{global}$ del walk-forward (Cap.24.6 di Parte V), giorni consecutivi sopra soglia $(1 + \alpha_{f_5}) \cdot f_5^{global}$, flag di alert attivo. Se la cardinalità minima $N_{reg,\min}^{live}$ non è raggiunta in entrambi i regimi, la riga riporta `n/a` con indicazione della cardinalità mancante.
- **Tabella delle metriche di lifecycle tracciate** di Cap.30.3bis ($\pi_{t_2 \mid t_1}^{live}$, MFE/MAE aggregati, $f_{stop \mid t_1}^{live}$) con valori correnti e finestra di calcolo $W_{prod}$.
- **Grafico della serie temporale di $B(t)$** di Cap.30.4 con linea di soglia $\theta_B$ e marcatori di alert.
- **Grafico della frequenza di emissione $r_{emit}^{live}(t)$** di Cap.30.5 con linee di soglia $E_{min}$ e $E_{max}$ e marcatori di alert.
- **Lista degli alert attivi**: per ogni alert di Cap.30.2, Cap.30.3 (deriva di $f_5^{live}$), Cap.30.4, Cap.30.5, riepilogo del trigger e dell'orario di prima rilevazione.

**Nessuna interazione execution-side**. La dashboard è puramente di monitoraggio: non espone bottoni di emissione manuale, non permette di sopprimere alert, non interagisce con il broker Directa per execution. La conformità al vincolo "solo emissione, nessuna esecuzione" di Cap.1 di Parte I si estende al monitoring: la dashboard può mostrare lo stato dei segnali e delle metriche, ma non può intervenire sull'operatività.

### 30.7 No calcolo live di DSR/PBO

Cap.30 **non calcola live DSR** (Deflated Sharpe Ratio) **né PBO** (Probability of Backtest Overfitting), in coerenza con la decisione di **Cap.24.7 di Parte V** (no incorporazione di DSR/PBO come obiettivi diretti del NSGA-II) e con la dichiarazione che DSR e PBO operano su distribuzioni di metriche aggregate del bundle, non per-segnale.

DSR e PBO sono **gate di selezione post-walk-forward applicati in Parte VII Cap.31-36** (in particolare: Cap.32 DSR come gate primario di selezione del bundle frozen; Cap.33 PBO via CSCV come misura di fragilità). Il calcolo richiede bootstrap stazionario $B = 2000$ ricampionamenti (Cap.34 Parte VII), operazione che non ha valore informativo se eseguita live su finestra di produzione rolling: la stima richiede l'intera distribuzione OOS aggregata e il dominio di applicazione è la selezione del bundle frozen e i gate decisionali di go-live, non il monitoring continuo.

Cap.30 si limita a tracciare le metriche di fitness (Cap.30.1) e lifecycle (Cap.30.3) **direttamente confrontabili** con le metriche del walk-forward via IQR cross-fold (Cap.30.2): il rinvio a Parte VII per DSR/PBO è esplicito.

---

*Fine della Parte VI. La pipeline di inference real-time del bundle frozen (Cap.27) con il meccanismo di ricalibrazione EGARCH e trigger di break parametrico (Cap.27.5 chiusura M-2 v2 CAP-03 residuo), la politica anti-doppio-segnale che operazionalizza il vincolo $|\mathcal{A}(t)| \leq 1$ di Cap.6.3 di Parte II (Cap.28), il layout mobile-first del messaggio Telegram che estende senza duplicare Cap.9.2 di Parte II (Cap.29), il monitoraggio del lifecycle in produzione con metriche live (incluse le contropartite delle 5 fitness $f_1$-$f_5$ del NSGA-II di Cap.24.1 di Parte V), dashboard lato motore e alert su deriva (Cap.30) sono ora formalmente specificati. Il bundle frozen prodotto dal walk-forward nested di Parte V è operativamente in produzione, l'operatore riceve segnali bit-exact identici al contratto di Parte II via Telegram, e la deriva del cromosoma rispetto al regime di mercato corrente è monitorata in tempo reale su tutti e 5 gli assi di selezione del fronte di Pareto; le decisioni di re-training del GA in risposta a deriva persistente sono rinviate a Parte VII Cap.36 (gate decisionali post-go-live). Parte VI non aggiunge una tabella di congelamento propria: i parametri di tuning operativo ($T_{recal,\text{EGARCH}}, \theta_B, T_{B,\text{persist}}, W_B, W_{prod}, T_{drift,\text{persist}}, T_{emit,\text{persist}}, \epsilon_p, N_{reg,\min}^{live}, \alpha_{f_5}$) sono dichiarati non congelati e riconsiderati post-go-live; le soglie già congelate in Cap.26.5 di Parte V ($E_{max} = 5, E_{min} = 0{,}2, E_{exp,max} = 0{,}30$) sono riusate senza ridichiarazione. La Parte VII consuma il bundle frozen e il log di replay live per la validazione OOS finale, i gate decisionali di go-live e la decisione formale di re-training.*
