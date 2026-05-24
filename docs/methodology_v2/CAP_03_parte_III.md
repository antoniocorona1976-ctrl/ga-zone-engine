# Parte III — Layer quantitativo single-instrument

La Parte III formalizza i blocchi quantitativi elementari che alimentano il motore genetico nelle Parti successive: la definizione operativa del rendimento logaritmico del FIB a barre 1-min e la sua aggregazione a scale temporali superiori (Cap.12); il modello di volatilità condizionata EGARCH(1,1) che produce la stima $\hat{\sigma}_t$ consumata dalle condizioni di emissione di Cap.8 della Parte II (Cap.13); la classificazione binaria del regime intraday calmo/turbolento che condiziona il comportamento del GA (Cap.14); il set di feature causali che il GA può consumare come input per costruire le zone e calibrare i parametri (Cap.15).

La Parte III non contiene la geometria delle zone di entry, target e stop (Parte IV), il cromosoma o la fitness del GA (Parte V), né il modello di survival (Parte IV, Cap.19). Essa definisce il catalogo dei blocchi quantitativi — rendimento, volatilità, regime, feature — che le Parti successive consumano come input già calcolati. Tutti i parametri numerici di questa Parte sono dichiarati come provvisori e rinviati al congelamento in Parte V, in coerenza con la policy stabilita in CAP-01 (Q-03): nessun valore numerico viene fissato definitivamente in questa sede senza evidenza empirica sullo storico Portara/CQG.

Il perimetro temporale di tutti i modelli e di tutte le feature è la sessione operativa 8:00-22:00 CET, intesa come finestra unica e continua di negoziazione dello strumento (Q-01, ereditata da CAP-01). Il tick size del FIB è 5 punti: tutti i prezzi strutturali, le zone e i valori dimensionati in punti FIB sono multipli di 5 (vincolo ereditato da CAP-01 e riconfermato nel corpo della Parte II).

---

## Capitolo 12 — Definizioni di rendimento e scala temporale

### 12.1 Rendimento logaritmico a frequenza 1-minuto

Sia $p_t$ il prezzo di chiusura della barra 1-minuto $t$, dove $t$ indicizza le barre all'interno della sessione operativa 8:00-22:00 CET nella nomenclatura dello storico Portara/CQG FIB continuo. Il **rendimento logaritmico 1-minuto** è definito come

$$r_t = \ln\!\left(\frac{p_t}{p_{t-1}}\right)$$

La serie $\{r_t\}$ è la serie di input primaria per il modello EGARCH(1,1) di Cap.13. La grandezza $p_t$ è sempre un multiplo di 5 punti FIB (tick size); questa proprietà discreta non altera la definizione continua del log-return, ma implica che il set di valori realizzabili di $r_t$ non è denso: sono ammessi solo rapporti $p_t / p_{t-1}$ con numeratore e denominatore multipli di 5.

La sessione operativa è la finestra 8:00-22:00 CET, che comprende 840 barre 1-min per ogni giornata di trading ordinaria. Lo storico utilizzato copre una profondità minima di 5 anni (circa 1.050.000 barre utili, pari a 250 sessioni per anno moltiplicato per 840 barre per sessione), in coerenza con il Cap.4 di CAP-01.

### 12.2 Trattamento del gap di sessione e della prima barra delle 8:00 CET

La prima barra della sessione corrente, con chiusura alle 8:01 CET, ha come prezzo di riferimento $p_{t-1}$ il prezzo di chiusura dell'ultima barra della sessione precedente (chiusura alle 22:00 CET del giorno di trading precedente). Il rendimento della prima barra è quindi

$$r_1^{(d)} = \ln\!\left(\frac{p_{8:01}^{(d)}}{p_{22:00}^{(d-1)}}\right)$$

dove $d$ indica il giorno di trading corrente e $d-1$ il giorno di trading immediatamente precedente nel calendario FIB (escludendo sabato, domenica e festività IDEM). Questo rendimento incorpora il **gap overnight**: la variazione di prezzo avvenuta fuori dalla finestra operativa, comprensiva di eventuali movimenti sugli indici internazionali (S&P futures, Nikkei, DAX premarket) e di notizie macro intervenute durante la chiusura del FIB.

**Trattamento del gap overnight nel modello EGARCH.** Il rendimento della prima barra viene incluso nella serie di stima del modello EGARCH come osservazione regolare, senza esclusione né sostituzione. La motivazione è duplice: (a) escludere sistematicamente la prima barra introdurrebbe una distorsione nella stima della volatilità media, poiché i gap overnight contribuiscono alla varianza totale del rendimento; (b) il gap overnight è un'informazione strutturalmente rilevante che il regime di volatilità deve incorporare. La scelta di non winsorizzare il gap è conservativa: in presenza di gap estremi (eventi macro, aperture a gap molto ampio), il modello registrerà un picco di volatilità stimata che influirà sull'emissione del segnale nella prima parte della sessione, riducendo la frequenza di emissione in condizioni potenzialmente avverse. Questa scelta è dichiarata come provvisoria e suscettibile di revisione empirica in Parte V sulla base della diagnostica dei residui standardizzati.

Casi particolari: (a) **Weekend e festività**: il giorno di trading precedente è l'ultimo giorno di trading effettivo, indipendentemente dal numero di giorni calendario intercorsi; (b) **Prima sessione dello storico** (warm-up): per le prime barre della finestra di stima iniziale dell'EGARCH, si utilizza la varianza incondizionata stimata sul periodo disponibile come valore di inizializzazione $\sigma_0^2$ (descritto in dettaglio in Cap.13.5).

### 12.3 Aggregazione a scale temporali superiori

Le feature di Cap.15 richiedono rendimenti a scale temporali superiori al minuto: 5-min, 15-min, 60-min. L'aggregazione è realizzata mediante **somma additiva dei log-return**. Per una scala di $k$ barre 1-min, il rendimento aggregato alla barra composita $T$ è

$$R_T^{(k)} = \sum_{j=0}^{k-1} r_{T \cdot k - j} = \ln\!\left(\frac{p_{T \cdot k}}{p_{(T-1) \cdot k}}\right)$$

dove l'ultima espressione segue dalla telescopicità del logaritmo e mostra che $R_T^{(k)}$ è equivalente al log-return calcolato direttamente sul prezzo di chiusura della barra composita rispetto al prezzo di chiusura della barra composita precedente. Le barre aggregate sono prodotte per **sampling dei prezzi di chiusura** ogni $k$ barre 1-min chiuse: non si costruisce un OHLC composito per la stima del modello principale, ma si utilizza il campionamento dei close come metodo computazionalmente efficiente e coerente con la definizione di $r_t$.

Le scale disponibili per le feature sono le seguenti:

| Scala | $k$ (barre 1-min) | Barre per sessione (840 min) |
|-------|-------------------|------------------------------|
| 1-min | 1 | 840 |
| 5-min | 5 | 168 |
| 15-min | 15 | 56 |
| 60-min | 60 | 14 |

Il vincolo di causalità (formalizzato in Cap.15.1) si applica anche alle scale aggregate: $R_T^{(k)}$ è disponibile come feature al tempo $t$ solo se $t \geq T \cdot k$, ovvero solo dopo che tutte le $k$ barre 1-min che lo compongono si sono chiuse.

### 12.4 Regola deterministica di fill virtuale per il backtest

In simulazione di backtest, il raw touch della entry zone viene trattato come **fill virtuale** a un prezzo determinato deterministicamente. La regola è definita in questa sede in risposta al carryover N-6 di Review v2 CAP-02, che rinviava la specifica operativa dalla Parte II alla Parte III.

**Regola worst-case conservativa.** Quando la barra 1-min $t$ produce un raw touch — ovvero il suo intervallo $[\text{low}_t, \text{high}_t]$ interseca la entry zone del segnale attivo — il fill virtuale è assegnato al livello discreto della zona più sfavorevole per l'operatore, secondo le seguenti regole direzionali:

- **Segnale long**: il fill virtuale è assegnato al **bordo superiore** della entry zone, ovvero al prezzo massimo della banda $p_{ref} + b$. Questo prezzo rappresenta il costo di ingresso più alto possibile entro la zona, il caso peggiore per un operatore long che acquista.
- **Segnale short**: il fill virtuale è assegnato al **bordo inferiore** della entry zone, ovvero al prezzo minimo della banda $p_{ref} - b$. Questo prezzo rappresenta il costo di ingresso più basso possibile entro la zona, il caso peggiore per un operatore short che vende.

In entrambi i casi il prezzo di fill è un multiplo di 5 punti FIB, coerentemente con il tick size dello strumento. La regola si applica indipendentemente dall'effettiva posizione del prezzo di apertura, chiusura, massimo o minimo della barra all'interno della zona.

**Motivazione.** La scelta del worst-case conservativo persegue due obiettivi: (a) evitare di gonfiare le performance in backtest assegnando fill favorevoli che non sarebbero garantiti dall'operatore umano — il quale, operando da cellulare in modo discontinuo, non può assicurarsi il prezzo migliore della banda; (b) produrre stime di performance sistematicamente conservative, coerenti con il principio di prudenza che guida la valutazione del motore genetico. Qualsiasi cromosoma che risulti redditizio sotto questa regola lo sarà a maggior ragione in forward run con fill non sistematicamente al peggior livello.

**Coerenza con il replay deterministico.** La regola è deterministica: dato lo storico delle barre 1-min (OHLC) e il payload del segnale attivo (entry zone con $p_{ref}$ e $b$), il fill virtuale è univocamente determinato. Questa proprietà è la condizione necessaria per il replay bit-exact descritto in Cap.10 della Parte II: due esecuzioni indipendenti del motore sulla stessa finestra storica producono esattamente lo stesso fill virtuale per ogni segnale, senza variabilità stocastica.

---

## Capitolo 13 — Modello di volatilità condizionata

### 13.1 Architettura del modello EGARCH(1,1)

Il modello di volatilità condizionata adottato è il modello **EGARCH(1,1)** (Exponential GARCH, ordine 1,1) di Nelson (1991), applicato alla serie dei rendimenti logaritmici 1-min del FIB all'interno della sessione operativa 8:00-22:00 CET. La scelta del modello EGARCH rispetto ai modelli GARCH simmetrici è motivata da due proprietà strutturali del FIB: (a) la **asimmetria della risposta alla volatilità** (leverage effect): movimenti negativi ampi tendono a produrre incrementi di volatilità maggiori rispetto a movimenti positivi di uguale ampiezza; (b) la **parametrizzazione in forma logaritmica** della varianza condizionata, che garantisce la positività di $\sigma_t^2$ senza vincoli espliciti sui parametri durante la stima MLE.

Il modello si compone di due equazioni.

**Equazione della media:**

$$r_t = \mu + \epsilon_t, \qquad \epsilon_t = \sigma_t \, z_t, \qquad z_t \sim D(0,1)$$

dove $\mu$ è la media incondizionata del processo (stimata congiuntamente agli altri parametri), $\epsilon_t$ è il termine di errore, $\sigma_t > 0$ è la deviazione standard condizionata al tempo $t$, e $z_t$ è l'innovazione standardizzata estratta da una distribuzione $D$ di media zero e varianza unitaria.

**Equazione della varianza:**

$$\ln(\sigma_t^2) = \omega + \alpha \Big(|z_{t-1}| - \mathbb{E}[|z_{t-1}|]\Big) + \gamma \, z_{t-1} + \beta \ln(\sigma_{t-1}^2)$$

I parametri del modello sono $(\mu, \omega, \alpha, \gamma, \beta)$:

- $\omega$ — costante della varianza in forma log; determina il livello della varianza incondizionata.
- $\alpha$ — coefficiente della componente simmetrica dell'innovazione $|z_{t-1}| - \mathbb{E}[|z_{t-1}|]$; misura la risposta della volatilità alla grandezza dell'innovazione, indipendentemente dal segno.
- $\gamma$ — coefficiente della componente asimmetrica (leverage); valori $\gamma < 0$ indicano che innovazioni negative producono aumenti di volatilità maggiori di innovazioni positive di uguale modulo.
- $\beta$ — coefficiente di persistenza; valori $|\beta|$ prossimi a 1 indicano alta persistenza della volatilità condizionata nel tempo.

Il termine $\mathbb{E}[|z_{t-1}|]$ dipende dalla distribuzione $D$ scelta (descritto in Cap.13.2). L'equazione della varianza è formulata in forma logaritmica: ciò garantisce $\sigma_t^2 > 0$ per qualsiasi valore dei parametri, eliminando i vincoli di non-negatività presenti nel GARCH standard.

La stima di volatilità prodotta dal modello è $\hat{\sigma}_t$ — la radice quadrata della varianza condizionata $\hat{\sigma}_t^2 = \exp(\widehat{\ln(\sigma_t^2)})$, espressa nelle stesse unità del rendimento logaritmico (adimensionale, ordine $10^{-4}$) e disponibile a frequenza 1-min.

**Conversione in punti FIB.** Poiché le condizioni di emissione di Cap.8 della Parte II operano su grandezze espresse in punti FIB (range della barra $r_{1m}(t)$ in punti, distanza $|\texttt{target\_1} - p_{ref}|$ in punti), la stima EGARCH deve essere convertita nelle stesse unità prima di essere usata come denominatore o come argomento della funzione di soglia. La conversione è:

$$\hat{\sigma}_{\text{pt}}(t) = \hat{\sigma}(t) \cdot p_t$$

dove $\hat{\sigma}(t)$ è la stima EGARCH in unità di log-return e $p_t$ è il prezzo corrente del FIB espresso in punti indice (multiplo di 5, per il tick size dello strumento). La grandezza $\hat{\sigma}_{\text{pt}}(t)$ è espressa in punti FIB e ha ordine di grandezza comparabile con le distanze strutturali tipiche del FIB (10–100 punti). Questa conversione rende adimensionali i rapporti $r_{1m}(t)/\hat{\sigma}_{\text{pt}}(t)$ e $|\texttt{target\_1} - p_{ref}|/\hat{\sigma}_{\text{pt}}(t)$ — entrambi numeri puri espressi in unità di sigma FIB.

**Nota**: nei capitoli successivi la notazione $\hat{\sigma}(t)$ indica la stima EGARCH in log-return, mentre $\hat{\sigma}_{\text{pt}}(t)$ indica la stima convertita in punti FIB. Le condizioni di emissione usano sempre $\hat{\sigma}_{\text{pt}}(t)$.

Questa grandezza è il **principale output del Cap.13** e viene consumata da:

1. **Cap.8 Parte II — condizione di volatilità**: $r_{1m}(t_{emission}) \leq \tau_{vol}(\hat{\sigma}_{\text{pt}}(t_{emission}))$, dove la soglia $\tau_{vol}$ è funzione parametrica di $\hat{\sigma}_{\text{pt}}(t)$ ottimizzata dal cromosoma, con argomento e soglia entrambi in punti FIB.
2. **Cap.8 Parte II — condizione di distanza in sigma-units**: $|\texttt{target\_1} - p_{ref}| / \hat{\sigma}_{\text{pt}}(t_{emission}) \geq \tau_{dist}^{\sigma}$, dove il denominatore è la stima EGARCH in punti FIB — il rapporto risultante è un numero puro (sigma-units FIB).
3. **Cap.14** — classificazione del regime intraday: il confronto di $\hat{\sigma}_t$ con il suo quantile rolling determina lo stato calmo/turbolento (la classificazione di regime usa $\hat{\sigma}(t)$ o $\hat{\sigma}_{\text{pt}}(t)$ indifferentemente, poiché il prezzo $p_t$ è un fattore di scala positivo costante nel breve periodo).
4. **Cap.15** — feature engineering: $\hat{\sigma}_t$ entra come feature di volatilità e come denominatore per normalizzazioni di grandezze in sigma-units (con la conversione $\hat{\sigma}_{\text{pt}}$ dove il denominatore è in punti FIB).

### 13.2 Distribuzione dell'innovazione standardizzata

La distribuzione $D$ dell'innovazione $z_t$ non viene fissata definitivamente in questa sede. Le due candidate sono:

- **Student-$t$ con $\nu$ gradi di libertà** ($\nu > 2$): $z_t \sim t_\nu(0,1)$ standardizzata. Per questa distribuzione $\mathbb{E}[|z|] = 2\sqrt{\nu-2}\,\Gamma\!\left(\frac{\nu+1}{2}\right) / \big[(\nu-1)\Gamma\!\left(\frac{\nu}{2}\right)\sqrt{\pi}\big]$, con $\nu$ stimato congiuntamente agli altri parametri via MLE. La Student-$t$ è la scelta di default provvisoria: produce code più pesanti rispetto alla Normale, coerenti con l'osservazione empirica di eccesso di curtosi nei rendimenti intraday dei futures su indice.
- **GED (Generalized Error Distribution) con parametro di forma $\kappa$**: $z_t \sim \text{GED}(\kappa)$ standardizzata. Per una GED standardizzata a varianza unitaria, il fattore di scala è $c = \left[\Gamma(1/\kappa) / \big(2^{2/\kappa}\,\Gamma(3/\kappa)\big)\right]^{1/2}$ e il valore atteso del modulo dell'innovazione è:

  $$\mathbb{E}[|z|] = \frac{c \cdot 2^{1/\kappa}\,\Gamma(2/\kappa)}{\Gamma(1/\kappa)}$$

  Verifica dei casi limite: per $\kappa = 2$ (Normale) si ottiene $\mathbb{E}[|z|] = \sqrt{2/\pi} \approx 0{,}7979$; per $\kappa = 1$ (Laplace) si ottiene $\mathbb{E}[|z|] = 1/\sqrt{2} \approx 0{,}7071$. Entrambi i valori sono coerenti con la letteratura (Nelson 1991; Zhu e Galbraith 2010). La GED è una candidata alternativa che generalizza la Normale ($\kappa=2$) verso code più pesanti ($\kappa < 2$) o più leggere ($\kappa > 2$).

La selezione definitiva tra Student-$t$ e GED avviene in **Parte V** mediante i criteri AIC e BIC calcolati sulla finestra di calibrazione di riferimento. Il criterio AIC premia il fit sul campione, il BIC introduce una penalità più severa per la complessità del modello. Il confronto è tra due modelli con diverso numero di parametri (il grado di libertà $\nu$ per la Student-$t$, il parametro di forma $\kappa$ per la GED); la scelta definitiva è quella che produce il minor AIC/BIC sulla finestra di calibrazione, salva la diagnostica dei residui (Cap.13.4). In ogni capitolo e formula successiva, la notazione $D(0,1)$ si intende come la distribuzione selezionata via AIC/BIC in Parte V.

### 13.3 Calibrazione: metodo MLE e finestra di stima

Il modello EGARCH(1,1) è calibrato mediante **massima verosimiglianza (MLE)**, massimizzando la log-verosimiglianza condizionata

$$\ell(\theta) = \sum_{t=1}^{T} \ln f_D\!\left(\frac{r_t - \mu}{\sigma_t}; \theta\right) - \ln \sigma_t$$

rispetto al vettore di parametri $\theta = (\mu, \omega, \alpha, \gamma, \beta, \nu\text{ o }\kappa)$, dove $f_D$ è la densità di $D$ valutata sull'innovazione standardizzata $z_t = (r_t - \mu)/\sigma_t$.

**Finestra di calibrazione — divergenza dichiarata dal baseline hard-locked.** Il baseline metodologico di riferimento (`ENGINE_ALGO_INTEGRATO_HARD_LOCKED.pdf`) adotta di default una finestra **expanding** (expanding window) con $T_{roll} = 1500$ barre come punto di partenza. Per la presente applicazione al FIB 1-min si adotta invece una finestra di tipo **rolling** (non expanding), con motivazione esplicita di divergenza.

La ragione dell'inapplicabilità del baseline al contesto FIB 1-min è duplice: (i) 1500 barre 1-min corrispondono a circa 1,8 giorni di trading — una finestra del tutto insufficiente per stimare in modo stabile un modello EGARCH(1,1) con distribuzione Student-$t$ (5 parametri: $\mu, \omega, \alpha, \gamma, \beta, \nu$), che richiede un campione di almeno alcune centinaia di sessioni per evitare degenerazioni della MLE; (ii) la finestra expanding accumula peso su periodi storici lontani, riducendo la reattività del modello ai cambiamenti strutturali del mercato FIB — problema ben documentato per strumenti ad alta variabilità intraday. A supporto teorico della scelta rolling in presenza di structural breaks parametrici si cita: **Pesaran e Timmermann (2007)** "Selection of estimation window in the presence of breaks", *Journal of Econometrics* 137(1), 134–161, che dimostrano come la finestra rolling domina l'expanding quando la probabilità di breaks parametrici è non trascurabile.

La stima è quindi condotta su una finestra rolling $[t - W + 1, t]$ di $W$ barre 1-min. La lunghezza $W$ della finestra è un **parametro del modello**, non del cromosoma: il GA non ottimizza $W$. Il valore di lavoro provvisorio è $W = 210.000$ barre 1-min, equivalente a circa 1 anno di trading (250 sessioni $\times$ 840 barre), congelato in Parte V sulla base dell'analisi empirica del trade-off tra adattabilità e stabilità della stima. Un M-promemoria per Parte V (M-5) richiede un benchmark comparativo rolling vs expanding vs EWMA con test Inoue-Rossi (2011) e criterio di rollback automatico se rolling $W = 210.000$ non domina almeno un'alternativa su metrica OOS congelata.

**Cadenza di ricalibratura.** La ricalibratura avviene **fold-per-fold del walk-forward** (non giornalmente): all'inizio di ogni fold OOS nella procedura di walk-forward di Parte V, il modello EGARCH viene ri-stimato sulla finestra rolling di $W$ barre precedenti al fold corrente, in coerenza con Cap. 14.3 del baseline hard-locked. Questa cadenza di ricalibratura è motivata dalla coerenza metodologica con la procedura di validazione: ri-stimare il modello a ogni sessione durante il walk-forward introdurrebbe una discrepanza tra la frequenza di ricalibrazione in training e quella usata in OOS. I parametri stimati all'inizio del fold restano fissi per tutta la durata del fold. Questa scelta è anche motivata dal costo computazionale della MLE su 210.000 osservazioni (non compatibile con la ricalibratura minuto-per-minuto sull'hardware disponibile descritto in CAP-01, Cap.3). La ricorrenza fold-per-fold è parametro del modello, rinviata a verifica empirica in Parte V.

**Inizializzazione e seed.** Il seed del generatore pseudo-casuale utilizzato per l'inizializzazione dell'ottimizzatore MLE è parte del bundle di calibrazione (insieme ai parametri stimati $\hat{\theta}$) e viene registrato nel log di calibrazione. Questo garantisce la riproducibilità bit-exact dell'intera stima, in coerenza con il vincolo di determinismo di Cap.10 della Parte II.

### 13.4 Diagnostica dei residui standardizzati

Dopo la stima del modello, i residui standardizzati $\hat{z}_t = (r_t - \hat{\mu}) / \hat{\sigma}_t$ devono essere sottoposti alla seguente diagnostica obbligatoria.

**Test di Ljung-Box sui quadrati.** Si testa l'autocorrelazione dei quadrati $\hat{z}_t^2$ mediante il test di Ljung-Box con statistica

$$Q(m) = n(n+2) \sum_{k=1}^{m} \frac{\hat{\rho}_k^2(\hat{z}^2)}{n-k}$$

dove $n$ è la dimensione del campione e $\hat{\rho}_k(\hat{z}^2)$ è l'autocorrelazione campionaria di $\hat{z}_t^2$ al lag $k$. Il criterio di accettazione del modello è: $p\text{-value}(Q(10)) > 0{,}05$ e $p\text{-value}(Q(20)) > 0{,}05$. Un modello che non soddisfi questo criterio indica che la struttura EGARCH(1,1) non ha catturato completamente la dipendenza nei quadrati delle innovazioni; in tal caso si registra il fallimento diagnostico nel log di calibrazione e si attiva il protocollo di fallback descritto in Parte V.

**Test ARCH-LM sui residui.** Si applica il test di Engle (ARCH Lagrange Multiplier) su $\hat{z}_t^2$ ai lag 5 e 10. Il criterio di accettazione è $p\text{-value} > 0{,}05$: un $p$-value inferiore indica effetti ARCH residui non catturati dal modello.

**QQ-plot.** Si costruisce il QQ-plot di $\hat{z}_t$ rispetto alla distribuzione $D$ teorica scelta (Student-$t$ o GED con i parametri stimati) per ispezione visiva. Il QQ-plot è prodotto per la sessione di diagnostica ma non entra nei criteri di accettazione automatica.

**ACF dei quadrati.** Si produce il grafico dell'autocorrelazione campionaria di $\hat{z}_t^2$ fino al lag 40, per verifica visiva della struttura residua.

La diagnostica è condotta sia sulla finestra di calibrazione sia, in Parte V, sulle finestre OOS del walk-forward. Il dettaglio della procedura di accettazione nel walk-forward è rinviato a Parte V.

### 13.5 Trattamento del gap di sessione nella ricorsione EGARCH

L'equazione della varianza EGARCH è una ricorsione: $\ln(\sigma_t^2)$ dipende da $\ln(\sigma_{t-1}^2)$. All'inizio di ogni sessione di trading (prima barra delle 8:00 CET), il modello deve essere inizializzato con un valore di $\sigma^2$ di partenza. Esistono due opzioni, entrambe dichiarate come aperte in attesa di selezione empirica in Parte V:

**Opzione A — Ripresa dal valore di fine sessione precedente.** La ricorsione riprende da $\sigma_{0,\text{sessione}}^2 = \hat{\sigma}_{840,\text{sessione} \, d-1}^2$, ovvero dalla stima dell'ultima barra della sessione precedente. Questo approccio preserva la continuità della ricorsione e consente al modello di incorporare lo stato di volatilità con cui si è chiusa la sessione precedente.

**Opzione B — Re-inizializzazione alla varianza incondizionata.** La ricorsione reinizia da $\sigma_{0,\text{sessione}}^2 = \hat{\sigma}^2_{\text{unconditional}}$, dove $\hat{\sigma}^2_{\text{unconditional}} = \exp(\hat{\omega} / (1 - \hat{\beta}))$ è la varianza incondizionata di lungo periodo del modello stimato. Questo approccio tratta ogni sessione come indipendente, ignorando la struttura di dipendenza cross-sessione, ma produce una inizializzazione più stabile e meno sensibile a spike di volatilità di fine sessione.

La scelta definitiva tra Opzione A e Opzione B è rinviata a Parte V, dove sarà condotta su base empirica confrontando la diagnostica dei residui e la stabilità delle stime $\hat{\sigma}_t$ nelle prime barre di sessione. Il valore di lavoro provvisorio è l'Opzione A, che preserva la struttura ricorsiva del modello.

Per la **prima sessione della finestra di stima** (warm-up iniziale), $\sigma_0^2$ è inizializzata alla varianza campionaria dei rendimenti $r_t$ sulla finestra di calibrazione disponibile: $\sigma_0^2 = \text{Var}(r_t)_{\text{campione}}$.

### 13.6 Osservazione sulla coda bassa della volatilità (N-5)

Il modello EGARCH produce $\hat{\sigma}_t$ per l'intera distribuzione della volatilità, inclusi i valori anomalmente bassi (coda sinistra della distribuzione di $\hat{\sigma}_t$). La condizione di volatilità di Cap.8 della Parte II è formulata come $r_{1m}(t) \leq \tau_{vol}(\hat{\sigma}(t))$: essa filtra solo la **coda alta** della volatilità, impedendo l'emissione in barre ad alta variazione di prezzo. Non impone nessun filtro sulla coda bassa.

È opportuno dichiarare esplicitamente che il modello EGARCH è in grado di segnalare anche le situazioni di volatilità anomalmente bassa (barre a range molto contenuto, tipicamente inferiori a 5-10 punti FIB), e che queste situazioni possono precedere sistematicamente eventi avversi — in particolare una riduzione artificiale della liquidità che rende i prezzi strutturali meno affidabili. La Parte V può quindi introdurre un **floor sulla condizione di emissione** della forma

$$r_{1m}(t) \geq \tau_{vol,low}$$

se l'analisi empirica sullo storico Portara/CQG mostra che barre a range eccessivamente basso precedono sistematicamente segnali con performance inferiore alla media. La Parte III non fissa questa soglia: produce il $\hat{\sigma}_t$ necessario per calcolarla e la misura empirica della coda bassa della distribuzione di $r_{1m}(t)$ condizionata a $\hat{\sigma}_t$.

---

## Capitolo 14 — Stato di regime intraday

### 14.1 Definizione della classificazione binaria

Il **stato di regime intraday** al tempo $t$ è una variabile binaria $R_t \in \{\text{calmo}, \text{turbolento}\}$ che classifica le condizioni di mercato nella sessione corrente sulla base della volatilità condizionata $\hat{\sigma}_t$ prodotta dal modello EGARCH di Cap.13.

La classificazione è **deterministica e calcolata in tempo reale**: il regime al tempo $t$ utilizza esclusivamente informazione disponibile fino alla chiusura della barra $t-1$, senza look-ahead sulla sessione corrente o sulle sessioni future. La classificazione non è una feature ottimizzabile dal GA: il GA non può modificare la definizione di regime o la soglia di classificazione per gonfiare le metriche. Il regime è uno **stato del contesto** — una grandezza derivata oggettivamente dallo storico — che il cromosoma può condizionare i propri parametri (ad esempio, parametri distinti per regime calmo e turbolento), ma che non può essere ridefinita o manipolata dall'ottimizzazione genetica. Questa separazione è fondamentale: senza di essa, il GA potrebbe imparare a classificare arbitrariamente più sessioni come "calme" per ridurre la volatilità stimata e allentare le condizioni di emissione, producendo overfitting che non si generalizza in forward run.

### 14.2 Metodo di classificazione basato su quantili rolling

Il regime è classificato sulla base del confronto tra $\hat{\sigma}_t$ e il suo quantile rolling calcolato su una finestra storica di sessioni passate.

**Statistica di sessione — baseline normativo e benchmark di robustezza.** La statistica riassuntiva di $\hat{\sigma}$ per la sessione $s$, usata come input per la classificazione di regime, è definita come la **media aritmetica** delle stime EGARCH su tutte le barre della sessione:

$$\bar{\sigma}_s = \frac{1}{N_s} \sum_{t \in s} \hat{\sigma}_{s,t} \quad \text{con } N_s = 840$$

dove la somma è estesa a tutte le $N_s = 840$ barre 1-min della sessione operativa 8:00-22:00 CET. Questo è il **baseline normativo** per la classificazione di regime. Il riferimento teorico per l'uso della media come statistica di aggregazione della volatilità di sessione è: **Corsi (2009)** "A Simple Approximate Long-Memory Model of Realized Volatility", *Journal of Financial Econometrics* 7(2), 174–196, che utilizza aggregazioni temporali della volatilità realizzata (componente giornaliera, settimanale, mensile) per costruire il modello HAR-RV.

Come **benchmark di robustezza**, nei report di sessione prodotti dal motore viene riportato in parallelo il valore $\text{med}_t(\hat{\sigma}_{s,t})$ — la mediana delle stime EGARCH sulla sessione. La mediana è meno sensibile a picchi anomali di volatilità (spike intraday) rispetto alla media. Se in validazione OOS la classificazione di regime cambia significativamente fra media e mediana su una frazione rilevante di sessioni, ciò va interpretato come segnale di sessioni con picchi anomali; il trattamento di questo caso è materia di un M-promemoria per Parte V (M-6). La soglia di "cambiamento significativo" è parametro del modello da definire in Parte V.

**Definizione formale.** Sia $\hat{\sigma}_{s,\bar{t}} = \bar{\sigma}_s$ la statistica di sessione calcolata come sopra. Sia $Q_p(\hat{\sigma} \mid \mathcal{W}_t)$ il quantile di livello $p$ della distribuzione di $\hat{\sigma}$ calcolata sulla finestra rolling $\mathcal{W}_t$ delle $N_{reg}$ sessioni più recenti precedenti alla sessione corrente. La classificazione è:

$$R_t = \begin{cases} \text{turbolento} & \text{se } \hat{\sigma}_t > Q_p\!\big(\hat{\sigma} \mid \mathcal{W}_t\big) \\ \text{calmo} & \text{altrimenti} \end{cases}$$

I parametri del metodo sono:
- $p$ — livello del quantile di soglia; **valore di lavoro provvisorio**: $p = 0{,}75$ (75° percentile della distribuzione rolling di $\hat{\sigma}$, da congelare in Parte V). Un valore $p = 0{,}75$ implica che circa il 25% delle barre siano classificate come turbolente.
- $N_{reg}$ — numero di sessioni nella finestra rolling; **valore di lavoro provvisorio**: $N_{reg} = 20$ sessioni (circa un mese di trading, da congelare in Parte V).

**Integrazione opzionale di volume e range.** Oltre a $\hat{\sigma}_t$, la classificazione del regime può essere integrata con il volume medio di sessione e il range medio di sessione come indicatori di liquidità e di ampiezza del movimento. L'integrazione è opzionale e la sua forma specifica è rinviata a Parte V sulla base dell'evidenza empirica: in Parte III si dichiara che il metodo primario è il quantile rolling di $\hat{\sigma}_t$, e che l'eventuale integrazione con volume e range è un'estensione non obbligatoria.

### 14.3 Persistenza minima e anti-flickering

Il regime non cambia a ogni barra 1-min. Una volta classificato il regime corrente in uno stato (calmo o turbolento), esso persiste per un numero minimo di barre prima di potere transire allo stato opposto.

**Regola di persistenza.** Il regime può cambiare da $R_t$ a $R_{t+1} \neq R_t$ solo se la nuova classificazione è confermata da almeno $T_{persist}$ barre consecutive in cui il confronto $\hat{\sigma}_t$ vs $Q_p$ produce il nuovo stato. Formalmente, una transizione da calmo a turbolento al tempo $t^*$ è accettata solo se $\hat{\sigma}_{t} > Q_p$ per tutti i $t \in [t^* - T_{persist} + 1, t^*]$.

Il parametro $T_{persist}$ è un **parametro del modello**, non del cromosoma. Il valore di lavoro provvisorio è $T_{persist} = 10$ barre 1-min (10 minuti di trading), da congelare in Parte V. La motivazione è anti-flickering: in assenza di persistenza minima, micro-oscillazioni di $\hat{\sigma}_t$ attorno alla soglia $Q_p$ produrrebbero transizioni di regime spurie ogni pochi minuti, rendendo la classificazione instabile e inutilizzabile per la suddivisione dei fold del walk-forward.

**Gestione del warm-up.** Per le prime $N_{reg}$ sessioni dello storico (periodo di warm-up della finestra rolling), il quantile $Q_p$ non è calcolabile su $N_{reg}$ sessioni complete. Durante il warm-up si utilizza il quantile calcolato sul sottoinsieme di sessioni disponibili. Le barre prodotte durante il warm-up sono escluse dalle metriche di valutazione del GA in Parte V (non entrano nei fold del walk-forward come dati valutabili), ma contribuiscono alla stima del modello EGARCH e al calcolo dei quantili rolling.

### 14.4 Impatto sul GA

La classificazione del regime $R_t$ influisce sul GA attraverso tre canali:

1. **Condizionalità della soglia di emissione $\tau_{vol}$.** Il cromosoma del GA può specificare due valori distinti della funzione di soglia $\tau_{vol}(\hat{\sigma}(t))$: uno per il regime calmo ($\tau_{vol,\text{calmo}}$) e uno per il regime turbolento ($\tau_{vol,\text{turbolento}}$). Analogamente, la soglia $\tau_{dist}^{\sigma}$ della condizione di distanza in sigma-units può essere condizionale al regime. Il cromosoma ottimizza i parametri condizionali, ma non ridefinisce la classificazione di regime.

2. **Suddivisione dei fold del walk-forward in calmo/turbolento.** In Parte V, la procedura di walk-forward classifica ogni fold (finestra OOS) come prevalentemente calmo o prevalentemente turbolento sulla base della distribuzione di $R_t$ nei minuti del fold. La metrica di **stabilità cross-regime della fitness** misura quanto le prestazioni del cromosoma siano omogenee tra fold calmi e fold turbolenti. Un cromosoma che performa bene solo in regime calmo e male in regime turbolento (o viceversa) penalizza la fitness di stabilità cross-regime, incentivando il GA a selezionare cromosomi robusti ai cambi di regime.

3. **Condizionalità delle metriche di lifecycle.** Le metriche di lifecycle di Cap.5 della Parte I — `executable_rate`, `target_1_hit_rate`, durata media del segnale — sono calcolate separatamente per regime calmo e regime turbolento. La specifica della stabilità cross-regime ("metriche stabili e comparabili tra regime calmo e turbolento") richiede che il GA non produca cromosomi che funzionano solo in un regime.

---

## Capitolo 15 — Feature engineering causale

### 15.1 Vincolo fondamentale di causalità temporale

Il vincolo di causalità temporale è il principio organizzativo di tutta la Parte III. Esso impone che ogni feature $x_t$ usata per una decisione al tempo $t$ — emissione del segnale, valutazione del cromosoma, classificazione del regime — sia calcolata esclusivamente con informazione disponibile fino alla chiusura della barra $t-1$.

**Formalizzazione.** Sia $\mathcal{F}_{t-1}$ la filtrazione (sigma-algebra) generata da tutti i prezzi, volumi, rendimenti e grandezze derivate disponibili fino alla chiusura della barra 1-min $t-1$. La barra $t$ contribuisce a $\mathcal{F}$ solo dopo la sua chiusura. Il vincolo di causalità è:

$$x_t \in \mathcal{F}_{t-1} \quad \text{per ogni feature } x_t \text{ e per ogni } t$$

Questo vincolo è più stringente della semplice assenza di look-ahead in senso stretto (che proibirebbe l'uso di dati futuri $s > t$): esso proibisce anche l'uso del prezzo corrente della barra aperta $t$ come input per la feature calcolata a $t$. La barra $t$ è "visibile" al motore solo dopo la sua chiusura.

**Conseguenza operativa.** Una feature calcolata su una finestra di $k$ barre storiche e usata alla barra $t$ deve utilizzare le barre $\{t-1, t-2, \ldots, t-k\}$, non la barra $t$ in corso. Il modello EGARCH produce $\hat{\sigma}_t$ usando i residui fino a $t-1$ (l'equazione della varianza è $\ln(\sigma_t^2) = f(\ln(\sigma_{t-1}^2), z_{t-1})$, che non richiede la barra $t$): il vincolo di causalità è soddisfatto per costruzione.

**Determinismo.** Tutte le feature sono deterministiche dato lo storico: non contengono componenti stocastiche non seedate. La combinazione di causalità e determinismo garantisce la riproducibilità bit-exact del backtest (Cap.10, Parte II).

### 15.2 Catalogo delle feature per categoria

La Parte III definisce il **catalogo completo** delle feature ammissibili, organizzato in quattro categorie. La selezione del sottoinsieme di feature effettivamente usato dal modello è materia del cromosoma (Parte V) o del wrapper di validazione (Parte VII): la Parte III si limita a definire le feature calcolabili.

Il numero massimo di feature candidate del catalogo è dichiarato come **parametro del modello**, non del cromosoma. Il valore di lavoro provvisorio è un massimo di 40 feature candidate, da congelare in Parte V sulla base dell'analisi della dimensionalità e del rischio di overfitting. La selezione è rinviata a Parte V/VII.

#### 15.2.1 Feature di prezzo

Le feature di prezzo catturano la dinamica recente del rendimento a diverse scale temporali:

- **Rendimento logaritmico 1-min corrente**: $x_t^{(r,1)} = r_{t-1}$ (il log-return della barra appena chiusa, $\in \mathcal{F}_{t-1}$).
- **Rendimento cumulato su finestra rolling**: $x_t^{(r,k)} = \sum_{j=1}^{k} r_{t-j}$ per $k \in \{5, 15, 60\}$ barre 1-min, equivalente al log-return a scala $k$ della barra composita più recente completamente chiusa.
- **Momentum logaritmico**: $x_t^{(\text{mom},k)} = \text{sign}\!\left(\sum_{j=1}^{k} r_{t-j}\right) \cdot \left|\sum_{j=1}^{k} r_{t-j}\right|$ — in pratica il rendimento cumulato firmato, per la direzione e la forza del trend recente.
- **Media mobile esponenziale dei rendimenti**: la formula corretta della EMA troncata al warm-up è

  $$x_t^{(\text{ema},\lambda)} = (1-\lambda) \sum_{j=0}^{n_t - 1} \lambda^j \, r_{t-1-j}$$

  dove la sommatoria parte da $j = 0$ con il rendimento più recente disponibile $r_{t-1}$ (la barra appena chiusa, $r_{t-1} \in \mathcal{F}_{t-1}$) e $n_t$ è il numero di barre disponibili dall'inizio del warm-up di sessione. La somma dei pesi è $(1 - \lambda^{n_t})$, che converge a 1 solo asintoticamente per $n_t \to \infty$. Nelle prime barre della sessione, con $n_t$ piccolo, la EMA è normalizzata implicitamente dalla somma dei pesi effettivi. Il termine $r_t$ (close della barra corrente ancora aperta) non compare nella formula: $r_t \in \mathcal{F}_t \setminus \mathcal{F}_{t-1}$ e non è disponibile al momento del calcolo della feature alla barra $t$.

  Il parametro $\lambda$ è parametro del modello (valore provvisorio $\lambda = 0{,}94$, congelato in Parte V). L'EMA dei rendimenti cattura il trend smussato.

  **Reset cross-session.** La EMA viene resettata all'apertura di ogni sessione (8:00 CET): la sommatoria riparte da $n_t = 1$ alla prima barra utile della nuova sessione, senza trasportare osservazioni della sessione precedente. Questa scelta elimina la contaminazione cross-sessione che si produrrebbe con una somma infinita non interrotta. Le prime $T_{warmup,\text{EMA}}$ barre della sessione sono marcate come `unusable` ed escluse dal training del GA (non entrano nei fold del walk-forward come dati valutabili). Il criterio per $T_{warmup,\text{EMA}}$ è che il peso delle osservazioni pre-warm-up sia inferiore all'1%:

  $$T_{warmup,\text{EMA}} \geq \frac{\ln(0{,}01)}{\ln(\lambda)}$$

  Per $\lambda = 0{,}94$: $T_{warmup,\text{EMA}} \geq \ln(0{,}01)/\ln(0{,}94) \approx 74$ barre (74 minuti di trading). Il valore $T_{warmup,\text{EMA}} = 74$ è il **default operativo provvisorio** congelato in Parte V. Il riferimento metodologico per il reset cross-session in contesti con sessione operativa netta è: **Engle e Sokalska (2012)** "Forecasting intraday volatility in the US equity market. Multiplicative component GARCH", *Journal of Financial Econometrics* 10(1), 54–83, che motivano esplicitamente il reset delle componenti intraday all'apertura di ogni sessione per evitare la contaminazione overnight.

Esempio numerico (tick FIB = 5pt): se $p_{t-1} = 27.500$ e $p_{t-2} = 27.480$, allora $r_{t-1} = \ln(27500/27480) \approx 7{,}28 \times 10^{-4}$; i prezzi sono multipli di 5 come richiesto.

#### 15.2.2 Feature di volume

Le feature di volume catturano le condizioni di liquidità e l'attività di mercato:

- **Volume relativo di sessione**: $x_t^{(v,\text{rel})} = v_{1m}(t-1) / \bar{v}_{h,m}$, dove $\bar{v}_{h,m}$ è il volume medio storico per il minuto $h$ e il mese $m$ della sessione, calcolato sulla finestra storica di calibrazione. Questo ratio confronta il volume della barra appena chiusa con il volume atteso per quella fascia oraria, normalizzando per il ciclo stagionale intraday.
- **Volume cumulato di sessione**: $x_t^{(v,\text{cum})} = \sum_{j=1}^{t-1} v_{1m}(j)$ — il volume totale contrattato dall'apertura delle 8:00 fino alla barra $t-1$ inclusa.
- **Rapporto volume rolling / media storica**: $x_t^{(v,\text{ma})} = \frac{(1/k)\sum_{j=1}^{k} v_{1m}(t-j)}{\bar{v}}$, dove $\bar{v}$ è il volume medio sull'intera finestra di calibrazione.

#### 15.2.3 Feature di volatilità

Le feature di volatilità catturano il livello e la variazione della volatilità condizionata:

- **Volatilità condizionata corrente**: $x_t^{(\sigma)} = \hat{\sigma}_{t-1}$ — la stima EGARCH della barra appena chiusa (disponibile in $\mathcal{F}_{t-1}$ per costruzione dell'equazione di ricorsione).
- **Volatilità realizzata rolling**: $x_t^{(\sigma,\text{rv},k)} = \sqrt{(1/k)\sum_{j=1}^{k} r_{t-j}^2}$ per $k \in \{10, 30, 60\}$ barre 1-min. La volatilità realizzata è un proxy non parametrico della volatilità corrente, calcolato esclusivamente da dati della finestra $[t-k, t-1]$.
- **Rapporto EGARCH / media storica**: $x_t^{(\sigma,\text{ratio})} = \hat{\sigma}_{t-1} / \bar{\sigma}$, dove $\bar{\sigma}$ è la media storica di $\hat{\sigma}_t$ sulla finestra di calibrazione. Questo ratio esprime il livello corrente di volatilità in unità della volatilità media storica.
- **Variazione della volatilità**: $x_t^{(\Delta\sigma)} = \hat{\sigma}_{t-1} - \hat{\sigma}_{t-2}$ — la variazione di un passo della stima EGARCH, che cattura se la volatilità sta aumentando o diminuendo.

#### 15.2.4 Feature di struttura

Le feature di struttura catturano la geometria del prezzo rispetto ai livelli strutturali identificati nella sessione:

- **Distanza dal pivot più recente**: $x_t^{(\text{piv})} = (p_{t-1} - \hat{p}_{\text{pivot}}) / \hat{\sigma}_{\text{pt}, t-1}$, espressa in sigma-units rispetto alla volatilità EGARCH corrente convertita in punti FIB, dove $\hat{p}_{\text{pivot}}$ è il livello dell'ultimo pivot confermato (definito in Cap.15.3) e $\hat{\sigma}_{\text{pt}, t-1} = \hat{\sigma}_{t-1} \cdot p_{t-1}$ è la stima EGARCH in punti FIB (coerente con la definizione di Cap.13.1). Il numeratore $(p_{t-1} - \hat{p}_{\text{pivot}})$ è in punti FIB; il denominatore $\hat{\sigma}_{\text{pt}, t-1}$ è in punti FIB; il rapporto è adimensionale (sigma-units FIB). La normalizzazione in sigma-units consente il confronto tra sessioni con diverso livello di volatilità.
- **Numero di pivot confermati nella sessione corrente**: $x_t^{(N_{\text{piv}})} = |\{\text{pivot confermati in} [8:00, t-1]\}|$ — un contatore intero che cresce durante la sessione man mano che i pivot vengono confermati dall'algoritmo di Cap.15.3.
- **One-hot di regime**: $x_t^{(R)} = \mathbb{1}[R_{t-1} = \text{turbolento}] \in \{0, 1\}$ — indicatore binario che segnala il regime classificato dalla barra precedente.
- **Durata del regime corrente**: $x_t^{(D_R)} = t - t_{R,\text{start}}$, dove $t_{R,\text{start}}$ è il tempo di inizio del regime corrente (l'istante in cui è diventata definitiva la transizione al regime corrente, dopo la persistenza minima $T_{persist}$). Questa feature cattura da quante barre il regime è stabile, informazione strutturalmente rilevante per la probabilità di persistenza futura.

### 15.3 Algoritmo di pivot detection causale

Il **pivot strutturale** è un livello di prezzo locale che il motore utilizza come ancora per la geometria del segnale (Parte IV) e come input per le feature di struttura di Cap.15.2.4. L'algoritmo deve essere deterministico e causale: un pivot al tempo $t$ è identificabile solo dopo che la sua natura di estremo locale è stata **confermata** da barre successive, senza utilizzo di dati futuri. La conferma introduce una **latenza**: il pivot a $t$ viene confermato al tempo $t + n_c$, dove $n_c$ è il numero di barre di conferma.

**Algoritmo frattale con conferma — quattro condizioni.** Il pivot di tipo high (massimo locale) alla barra $t$ è confermato alla chiusura della barra $t + n_c$ se e solo se valgono simultaneamente tutte e quattro le condizioni seguenti:

1. $\text{high}_t > \text{high}_{t-i}$ per ogni $i \in [1, n_c]$ — il massimo di $t$ supera tutti i massimi delle $n_c$ barre precedenti;
2. $\text{high}_t > \text{high}_{t+j}$ per ogni $j \in [1, n_c]$ — il massimo di $t$ supera tutti i massimi delle $n_c$ barre successive;
3. $\min\!\big(\text{low}_{t+1}, \ldots, \text{low}_{t+n_c}\big) \leq \text{high}_t - \delta_{pivot}$ — il prezzo si è allontanato dal massimo di almeno $\delta_{pivot}$ punti FIB nelle barre di conferma (filtro di retracement, vedi sotto);
4. la finestra temporale $[t - n_c,\, t + n_c]$ rientra interamente nella sessione operativa 8:00-22:00 CET corrente — il pivot non può estendersi su più sessioni (coerenza con il reset cross-session di Cap.15.2.1).

Analogamente, il pivot di tipo low (minimo locale) alla barra $t$ è confermato alla chiusura della barra $t + n_c$ se e solo se:

1. $\text{low}_t < \text{low}_{t-i}$ per ogni $i \in [1, n_c]$;
2. $\text{low}_t < \text{low}_{t+j}$ per ogni $j \in [1, n_c]$;
3. $\max\!\big(\text{high}_{t+1}, \ldots, \text{high}_{t+n_c}\big) \geq \text{low}_t + \delta_{pivot}$;
4. la finestra temporale $[t - n_c,\, t + n_c]$ rientra interamente nella sessione operativa 8:00-22:00 CET corrente.

Il parametro $n_c$ (numero di barre a sinistra e a destra richieste per la conferma) è un **parametro del modello**, non del cromosoma. Il valore di lavoro provvisorio è $n_c = 3$ barre (conferma su 3 barre a sinistra e 3 a destra dell'estremo locale), congelato in Parte V.

**Disponibilità temporale come feature — correzione look-ahead.** La conferma del pivot a $t$ richiede di osservare $\text{high}_{t+n_c}$ (o $\text{low}_{t+n_c}$), il quale è disponibile solo dopo la chiusura della barra $t + n_c$, ossia appartiene a $\mathcal{F}_{t+n_c}$ (non a $\mathcal{F}_{t+n_c-1}$). Di conseguenza, il pivot a $t$ **diventa disponibile come feature alla barra $t + n_c + 1$**, non alla barra $t + n_c$. Il vincolo di causalità è quindi: il pivot confermato alla barra $t$ entra in $\mathcal{F}_{t+n_c+1}$ ed è utilizzabile solo dalla barra $t + n_c + 1$ in poi.

**Primo pivot post-apertura e vincolo $N_{pivot}$.** Il primo pivot della sessione è il primo massimo locale o minimo locale che viene confermato dopo l'apertura delle 8:00 CET. Poiché la conferma richiede $n_c$ barre adiacenti, il primo pivot confermato non può essere identificato prima della barra $n_c + 1$ della sessione (ovvero almeno 4 barre dopo l'apertura con $n_c = 3$). Il vincolo operativo ereditato da CAP-01 (M-1) è che il primo pivot deve essere identificabile entro $N_{pivot}$ barre dall'apertura. Si definisce:

$$N_{pivot} = \min\!\big\{t : \text{esiste almeno un pivot confermato in} [8:00, t]\big\}$$

Il valore di $N_{pivot}$ dipende dalla geometria del prezzo nella prima parte della sessione e non è fissabile a priori senza evidenza empirica. Il valore di lavoro provvisorio è $N_{pivot} = 30$ barre (mezz'ora di trading, proposta dalla Review v1 CAP-02 come ordine di grandezza ragionevole, confermata dal Planner come valore di lavoro non definitivo), da verificare empiricamente sullo storico Portara/CQG e congelare in Parte V con misura della distribuzione effettiva della latenza del primo pivot nelle 1.050.000 barre storiche disponibili.

**Soglia di retracement minimo.** La condizione 3 nelle quattro condizioni sopra costituisce il filtro di retracement minimo. Essa richiede che il prezzo si sia allontanato dal massimo (o minimo) candidato di almeno $\delta_{pivot}$ punti FIB, misurato sul minimo dei low (o massimo degli high) delle barre di conferma $[t+1, t+n_c]$. La valutazione è quindi esplicita: per pivot high, si controlla che $\min(\text{low}_{t+1}, \ldots, \text{low}_{t+n_c}) \leq \text{high}_t - \delta_{pivot}$. Il parametro $\delta_{pivot}$ è un **parametro del modello**, valore di lavoro provvisorio $\delta_{pivot} = 10$ punti FIB (2 tick FIB), congelato in Parte V.

Esempio numerico (con $n_c = 3$, $\delta_{pivot} = 10$ pt, prezzi multipli di 5 FIB): sia $\text{high}_{t} = 27.500$, $\text{high}_{t-1} = \text{high}_{t-2} = \text{high}_{t-3} = 27.480$ (condizione 1 verificata), $\text{high}_{t+1} = 27.490$, $\text{high}_{t+2} = 27.485$, $\text{high}_{t+3} = 27.475$ (condizione 2 verificata). Il retracement minimo nelle barre di conferma è $\min(\text{low}_{t+1}, \text{low}_{t+2}, \text{low}_{t+3})$; se questo minimo è $\leq 27.490 = 27.500 - 10$, la condizione 3 è verificata. Supponendo che tutta la finestra $[t-3, t+3]$ sia nella sessione 8:00-22:00 CET, la condizione 4 è verificata. La conferma avviene alla chiusura della barra $t+3$; il pivot entra come feature disponibile dalla barra $t+4 = t + n_c + 1$.

**Determinismo.** L'algoritmo è deterministico: dato lo storico OHLC e i parametri $(n_c, \delta_{pivot})$, la sequenza dei pivot confermati è univocamente determinata. Non vi è alcuna componente stocastica.

### 15.4 Normalizzazione robusta delle feature

Prima di essere consumate dal modello di survival (Parte IV) e dal cromosoma (Parte V), tutte le feature devono essere normalizzate in modo da avere scala comparabile e distribuzione robusta agli outlier. Il metodo adottato è la **normalizzazione z-score con mediana e MAD** (Median Absolute Deviation) su finestra storica rolling.

**Formula.** Per ogni feature $x$ e ogni istante $t$:

$$\tilde{x}_t = \frac{x_t - \text{Med}(x_{t-1}, \ldots, x_{t-W_{norm}})}{\text{MAD}(x_{t-1}, \ldots, x_{t-W_{norm}}) \cdot c}$$

dove:
- $\text{Med}(\cdot)$ è la mediana campionaria della finestra di normalizzazione $[t - W_{norm}, t-1]$;
- $\text{MAD}(\cdot) = \text{Med}(|x_j - \text{Med}(x)|)$ è la deviazione assoluta mediana della stessa finestra;
- $c = 1{,}4826$ è la costante di consistenza che rende la MAD un'estimazione consistente della deviazione standard sotto la distribuzione Normale.

La scelta di mediana e MAD in luogo di media e deviazione standard è motivata dalla robustezza agli outlier: i rendimenti e la volatilità del FIB presentano code pesanti, e singole osservazioni estreme non devono distorcere la scala di normalizzazione dell'intera finestra.

La lunghezza della finestra di normalizzazione $W_{norm}$ è un **parametro del modello**, valore di lavoro provvisorio $W_{norm} = 1.000$ barre 1-min (circa 2 giorni di trading), da congelare in Parte V. La normalizzazione è calcolata esclusivamente su dati della finestra $[t - W_{norm}, t-1]$ ($\in \mathcal{F}_{t-1}$), in coerenza con il vincolo di causalità.

**Gestione dei casi degeneri.** Se $\text{MAD} = 0$ (feature costante nella finestra rolling, possibile per feature binarie o contatori), si adotta la convenzione $\tilde{x}_t = 0$ (o equivalentemente si sostituisce MAD con un valore floor $\epsilon > 0$ parametro del modello). Questo caso è raro per le feature continue ma può verificarsi per la feature one-hot di regime $x_t^{(R)}$ in sessioni con regime costante.

---

*Fine della Parte III. I blocchi quantitativi elementari — rendimento (Cap.12), volatilità condizionata (Cap.13), regime intraday (Cap.14), feature causali (Cap.15) — sono ora formalmente definiti e pronti per essere consumati dalla Parte IV (geometria delle zone, survival model) e dalla Parte V (cromosoma, operatori GA, fitness multi-obiettivo). Il parametro $W$, $p$, $N_{reg}$, $T_{persist}$, $N_{pivot}$, $n_c$, $\delta_{pivot}$, $W_{norm}$ e la distribuzione $D$ sono tutti dichiarati come provvisori e congelati in Parte V previo confronto empirico sullo storico Portara/CQG FIB 1-min.*
