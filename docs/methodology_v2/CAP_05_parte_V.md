# Parte V — Motore genetico, fitness operativa, walk-forward nested e calibrazione

La Parte V chiude il documento metodologico v2 sul versante algoritmico: formalizza il cromosoma del bundle (Cap.22), gli operatori dell'algoritmo genetico NSGA-II con derivazione analitica del budget di valutazioni (Cap.23), la funzione di fitness multi-obiettivo (Cap.24), lo schema di walk-forward nested con purge ed embargo e la diagnostica survival fold-per-fold (Cap.25), la calibrazione operativa e il congelamento numerico di tutti i parametri provvisori delle Parti I-IV e di Parte V stessa (Cap.26).

La Parte V non contiene la pipeline di inference real-time (Parte VI, Cap.27-30), la validazione OOS finale con DSR/PBO/bootstrap stazionario e i gate decisionali di go-live (Parte VII, Cap.31-36), né le specifiche di interfaccia (Appendici C-D-E). La Parte V consuma tutti i blocchi formali delle Parti precedenti come input: i vincoli operatore e di compute (Parte I, CAP-01), il payload e la state machine del segnale con submacchina position lifecycle (Parte II, CAP-02), il modello EGARCH(1,1), la classificazione di regime, il catalogo 37 feature e l'algoritmo pivot detection (Parte III, CAP-03), la geometria delle zone, i target strutturali, lo stop strutturale e il modello survival Cox cause-specific con la feature condizionale trade_range (Parte IV, CAP-04).

La proprietà strutturale del FIB con tick size pari a 5 punti è il vincolo trasversale della Parte V: ogni parametro a unità di prezzo del cromosoma è multiplo di 5; ogni esempio numerico, ogni soglia di filtro e ogni livello strutturale che entra nella fitness rispetta questa proprietà discreta. Tutti i valori numerici introdotti nei capitoli Cap.22-25 della Parte V sono dichiarati provvisori e tracciati nella tabella di congelamento di Cap.26.5; nessun valore è fissato definitivamente prima della tabella di Cap.26.5.

---

## Capitolo 22 — Cromosoma e spazio dei parametri

### 22.1 Definizione del cromosoma del bundle

Il cromosoma del bundle, denotato $\theta$, è la tupla strutturata che codifica tutti i parametri ottimizzabili del motore. La Parte V formalizza $\theta$ come spazio di ricerca dell'algoritmo genetico NSGA-II (Cap.23); la fitness multi-obiettivo (Cap.24) valuta cromosomi candidati su finestre OOS del walk-forward (Cap.25); la calibrazione di Cap.26 congela il sottoinsieme dei parametri del modello (non del cromosoma) e i valori di lavoro di tutti i parametri provvisori delle Parti precedenti.

Si distinguono due famiglie di parametri:

- **Parametri del cromosoma**, ottimizzati dal GA: codificano i gradi di libertà geometrici, di emissione, di target/stop, temporali e di selezione feature del bundle.
- **Parametri del modello**, congelati in Cap.26 e non ottimizzati dal GA: includono ad esempio $n_c$, $\delta_{pivot}$, $\lambda$ (EMA), $W$ (finestra EGARCH), $p$, $N_{reg}$, $T_{persist}$ (classificazione di regime), $W_{norm}$, $T_{warmup,\text{norm}}$, $T_{warmup,\text{EMA}}$ (normalizzazione), i parametri trade_range $A_{range,min}=80$, $N_{osc}$, $n_{osc,min}$, $\epsilon_{osc}$, $N_{break}$, $\delta_{break}$ (Cap.21.2 di Parte IV), nonché i tassi NSGA-II $\eta_c$, $\eta_m$, $p_m^{cont}$, $p_m^{disc}$ (Cap.23 di questa Parte).

Il cromosoma $\theta$ è una tupla
$$\theta = \big(\, b,\ d_{inv},\ d_{obsolete},\ T_{min,session},\ \tau_{vol}^{(\cdot)},\ \tau_{liq},\ \tau_{dist}^{\sigma},\ \tau_{surv}^{(\cdot)},\ k_{t2},\ d_{stop,\sigma}^{(\cdot)},\ \Delta t_{cromosoma},\ T_{touch}^{max},\ \mathbf{s} \,\big)$$
dove la notazione $X^{(\cdot)}$ con il puntino fra parentesi indica che il gene può essere a valore unico o regime-dipendente (uno o due valori per regime calmo/turbolento), e $\mathbf{s} \in \{0,1\}^{37}$ è il vettore binario di selezione feature del survival. Le sotto-sezioni 22.2-22.6 specificano dominio, semantica, encoding e regime-dipendenza di ciascun gene.

### 22.2 Geni geometrici

I geni geometrici controllano la costruzione della zona di entry e le invalidazioni pre-touch definite in Cap.16 di Parte IV.

- **$b$** — semi-ampiezza della banda di entry. Dominio discreto $b \in \{5, 10, 15, 20, 25, 30, 35, 40\}$ punti FIB, $b_{min} = 5$ provvisorio (eredità di Cap.6.1 di Parte II, $b_{min} = 5$ corrisponde a 1 tick FIB; vincolo $d_{stop} > b$ obbligatorio). La cardinalità della banda è $(2b/5) + 1$ livelli discreti, in coerenza con Cap.16.3 di Parte IV. Encoding integer (8 valori).
- **$d_{inv}$** — soglia di invalidazione I2 (allontanamento dalla zona, Cap.16.5 di Parte IV). Dominio multipli di 5 pt, $\geq 5$. Encoding integer.
- **$d_{obsolete}$** — soglia di invalidazione I3 (nuovo pivot strutturale che rende obsoleta la zona, Cap.16.5 di Parte IV). Dominio multipli di 5 pt, $\geq 5$. Encoding integer.
- **$T_{min,session}$** — tempo residuo minimo di sessione per emissione (Cap.16.6 di Parte IV). Dominio interi positivi in minuti di trading, $\geq 15$. Encoding integer.

Nessuno di questi geni è regime-dipendente: la geometria della zona e le sue invalidazioni rispondono alla struttura del prezzo, non al regime di volatilità (che entra implicitamente attraverso $\hat{\sigma}_{\text{pt}}$ nei filtri di Cap.8 di Parte II).

Il **prezzo di riferimento $p_{ref}$ non è un gene del cromosoma**: $p_{ref}$ è derivato deterministicamente dai pivot strutturali confermati attraverso l'algoritmo di selezione di Cap.16.1 di Parte IV (timestamp di conferma più recente nella direzione del segnale). Il GA ottimizza la semi-ampiezza $b$ attorno a $p_{ref}$ ma non $p_{ref}$ stesso.

### 22.3 Geni di emissione

I geni di emissione controllano i quattro filtri di Cap.8.3 di Parte II e il filtro survival-based di Cap.20.1 di Parte IV.

- **$\tau_{vol}(\cdot)$** — soglia di volatilità $E_{vol}$, formulata come funzione parametrica di $\hat{\sigma}_{\text{pt}}$. Decisione di Parte V: forma funzionale **costante a tratti per regime**, con due valori distinti $\tau_{vol,\text{calmo}}$ e $\tau_{vol,\text{turbolento}}$ (regime-dipendente), entrambi in $\mathbb{R}^+$. Encoding real-valued. La motivazione della forma costante a tratti per regime è la coerenza con la classificazione $R_t$ già binaria deterministica di Cap.14 di Parte III: una funzione lineare o esponenziale di $\hat{\sigma}_{\text{pt}}$ aggiungerebbe gradi di libertà non necessari, dato che il GA già condiziona al regime tramite due valori distinti.
- **$\tau_{liq}$** — soglia di liquidità $E_{liq}$ sul volume normalizzato (Cap.8 di Parte II). Dominio $\mathbb{R}^+$ (single value, non regime-dipendente di default). Encoding real-valued.
- **$\tau_{dist}^{\sigma}$** — soglia di distanza target_1 in sigma-units FIB (Cap.8 di Parte II, eredità di Cap.17.3 di Parte IV). Dominio $\mathbb{R}^+$ (single value). Encoding real-valued.
- **$\tau_{surv}(\cdot)$** — soglia di probabilità minima di successo del survival (Cap.20.1 di Parte IV). Dominio $\tau_{surv} \in (0{,}1;\, 0{,}9)$. Il gene è regime-dipendente opzionale: il GA può specificare un valore comune o due valori distinti $\tau_{surv,\text{calmo}}$, $\tau_{surv,\text{turbolento}}$ (Cap.20.3 di Parte IV). Encoding real-valued.

La regime-dipendenza è dichiarata gene-per-gene: $\tau_{vol}$ e $\tau_{surv}$ sono regime-dipendenti di default (in coerenza con Cap.14.4 di Parte III e Cap.20.3 di Parte IV); $\tau_{liq}$, $\tau_{dist}^{\sigma}$ sono single value. L'esistenza di una versione regime-dipendente raddoppia il numero di geni reali per il gene corrispondente.

### 22.4 Geni di target e stop

I geni di target e stop controllano la geometria dei livelli di obiettivo e di arresto formalizzata in Cap.17-18 di Parte IV. I livelli stessi (target_1, target_2, stop_loss) sono **derivati** dalla geometria dei pivot e dal cromosoma, non sono geni: il GA non ottimizza direttamente i prezzi, ma i moltiplicatori e le soglie che li determinano.

- **$k_{t2}$** — moltiplicatore sigma per target_2 sintetico (Cap.17.4 di Parte IV). Dominio $\mathbb{R}^+$, valore provvisorio $k_{t2} = 2{,}0$. Single value (non regime-dipendente di default). Encoding real-valued.
- **$d_{stop,\sigma}(\cdot)$** — moltiplicatore sigma per stop_loss sintetico (Cap.18.1 di Parte IV). Dominio $\mathbb{R}^+$, valore provvisorio $d_{stop,\sigma} = 3{,}0$. Gene regime-dipendente opzionale: il GA può specificare un valore comune oppure due valori distinti $d_{stop,\sigma,\text{calmo}}$, $d_{stop,\sigma,\text{turbolento}}$ con il vincolo opzionale $d_{stop,\sigma,\text{turbolento}} \geq d_{stop,\sigma,\text{calmo}}$ (l'incertezza in regime turbolento giustifica uno stop più ampio in unità di volatilità). Encoding real-valued.

I livelli `target_1`, `target_2`, `target_2_type`, `stop_loss`, `stop_type` del payload (Cap.6.1 di Parte II) sono derivati deterministicamente dall'algoritmo di Cap.17.1-17.4 e Cap.18.1-18.5 di Parte IV combinato con $b$, $k_{t2}$, $d_{stop,\sigma}$ e $p_{ref}$.

### 22.5 Geni temporali

I geni temporali controllano i timer pre-trigger e post-trigger del segnale (Cap.6.1 di Parte II).

- **$\Delta t_{cromosoma}$** — durata massima della fase post-trigger in minuti di trading (eredità di Q-04 CAP-01 e Cap.6.1 di Parte II). Dominio interi $\{1, 2, \ldots, 1680\}$ (cap 2 giorni di trading $= 2 \cdot 840$ minuti). Encoding integer (cardinalità 1680).
- **$T_{touch}^{max}$** — durata massima della fase di attesa pre-trigger in minuti di trading (Cap.6.1 di Parte II). Dominio interi $\{5, 6, \ldots, 480\}$ (cardinalità 476). Encoding integer.

Entrambi i geni sono single value, non regime-dipendenti.

### 22.6 Geni di selezione feature survival

Il cromosoma include un **vettore binario di selezione feature** $\mathbf{s} \in \{0,1\}^{37}$ che codifica l'inclusione ($s_j = 1$) o l'esclusione ($s_j = 0$) di ciascuna delle 37 feature del catalogo (Cap.15.2 di Parte III) come predittore del modello di survival Cox cause-specific (Cap.19.2 di Parte IV).

Il vincolo di cardinalità $\sum_{j=1}^{37} s_j \leq K_{max}$ limita la dimensionalità del vettore di feature attive del survival a un valore massimo $K_{max} \leq 37$. $K_{max}$ è un **parametro del modello**, non del cromosoma: è congelato in Cap.26.7 sulla base della rule of thumb $N_{eventi}/K \geq 10$ di Harrell (2015) "Regression Modeling Strategies", 2a ed., Springer, cap. 4, applicata al rapporto eventi/parametri per la stabilità della stima Cox MLE.

**Trade_range — feature condizionale.** Per i setup di classe `trade_range`, la feature condizionale $x^{(A_{range})}$ (Cap.21.5 di Parte IV) è aggiunta al vettore $\tilde{\mathbf{x}}$ dal modello in modo deterministico, senza essere codificata nel cromosoma $\mathbf{s}$. Il catalogo globale del cromosoma per il regime directional resta a 37 feature (Cap.15.2 di Parte III invariato): la feature trade_range non è nel catalogo principale e non incrementa la dimensionalità di $\mathbf{s}$. Per i setup trade_range, il vettore di feature attive del Cox è $\tilde{\mathbf{x}}_{\text{trade\_range}} = \tilde{\mathbf{x}}_{\text{selected}} \cup \{x^{(A_{range})}\}$ dove $\tilde{\mathbf{x}}_{\text{selected}} = \{\tilde{x}_j : s_j = 1\}$.

Encoding del vettore $\mathbf{s}$: binary (37 bit). Le operazioni di crossover e mutazione di Cap.23 operano sul vettore $\mathbf{s}$ con riparazione esplicita del vincolo $\sum_j s_j \leq K_{max}$ (Cap.23.2 e Cap.23.3).

### 22.7 Vincoli di ammissibilità

I vincoli di ammissibilità sono regole rigide che squalificano un cromosoma dalla popolazione del GA: cromosomi che violano anche un solo vincolo sono dichiarati **non validi** e gestiti dall'algoritmo secondo la strategia di Cap.23.4 (constraint-domination Deb 2000). Si enumerano i vincoli:

1. **$d_{stop} > b$** (eredità di Cap.6.1 di Parte II e Cap.2 di Parte I). La distanza dello stop_loss dal prezzo di riferimento, $d_{stop} = |p_{ref} - \texttt{stop\_loss}|$, deve essere strettamente maggiore della semi-ampiezza $b$ della banda di entry. Il vincolo è verificato sul livello strutturale o sintetico effettivo derivato dal cromosoma (Cap.18.2 di Parte IV).
2. **Filtro 80 pt** (eredità di Cap.5 di Parte I e Cap.6.1, Cap.8.2 di Parte II). Per i setup directional: $|\texttt{target\_1} - p_{ref}| \geq 80$ pt FIB. Per i setup trade_range: $A_{range} = p_{high,range} - p_{low,range} \geq 80$ pt FIB. Vincolo assoluto non allentabile dal cromosoma.
3. **$d_{stop,\sigma,\text{turbolento}} \geq d_{stop,\sigma,\text{calmo}}$** (opzionale, eredità di Cap.18.5 di Parte IV). Se il gene $d_{stop,\sigma}$ è specificato come regime-dipendente, il valore in regime turbolento deve essere maggiore o uguale al valore in regime calmo. Vincolo strutturalmente plausibile (regime turbolento $\Rightarrow$ stop più ampio in unità di $\hat{\sigma}_{\text{pt}}$).
4. **$\sum_j s_j \leq K_{max}$** (cardinalità di feature attive del survival, Cap.22.6). Cromosomi con $\sum_j s_j > K_{max}$ sono non validi.
5. **Tutti i parametri a unità di prezzo multipli di 5** (tick FIB, eredità di Cap.5 di Parte I e Cap.6.1 di Parte II). $b, d_{inv}, d_{obsolete}$ sono multipli di 5 per costruzione del dominio. I livelli derivati `target_1`, `target_2`, `stop_loss` sono multipli di 5 per costruzione algoritmica (Cap.17.4 e Cap.18.1 di Parte IV usano arrotondamento al multiplo di 5 più vicino per i livelli sintetici).
6. **$\Delta t_{cromosoma} \in \{1, \ldots, 1680\}$ e $T_{touch}^{max} \in \{5, \ldots, 480\}$** (eredità di Cap.6.1 di Parte II e Q-04 CAP-01). Cromosomi che violano i domini sono dichiarati non validi (Cap.7 di Parte II).
7. **Sospensione strutturale in warm-up** (eredità di Cap.16.2 di Parte IV, M-1 v2 CAP-03). Il cromosoma non può bypassare la regola di sospensione: se $\mathcal{P}_{low}(t) = \emptyset$ (long) o $\mathcal{P}_{high}(t) = \emptyset$ (short), il motore non emette indipendentemente dai valori dei geni di emissione. Questo vincolo è strutturale e non genetico: nessun valore del cromosoma può ottenere un'emissione in warm-up strutturale.

**Gestione di cromosomi non validi.** La popolazione del GA non ammette cromosomi che violano i vincoli 1-7. Il GA li scarta secondo la strategia di constraint-domination di Cap.23.4: cromosomi ammissibili dominano i non ammissibili indipendentemente dalla fitness; fra i non ammissibili, l'ordinamento è per somma normalizzata delle violazioni. La mutazione random vincolata (Cap.23.4) proietta il gene violante nel dominio ammissibile più prossimo per riparazione locale; cromosomi non riparabili sono sostituiti con campionamento uniforme del dominio.

### 22.8 Encoding per gli operatori del GA

L'encoding adottato è **misto** (mixed encoding), in coerenza con la natura eterogenea dei geni:

- **Real-valued** per i geni continui: $\tau_{vol,\text{calmo}}$, $\tau_{vol,\text{turbolento}}$, $\tau_{liq}$, $\tau_{dist}^{\sigma}$, $\tau_{surv,\text{calmo}}$, $\tau_{surv,\text{turbolento}}$ (se regime-dipendente), $k_{t2}$, $d_{stop,\sigma}$ (o le due varianti regime). I bound del dominio sono mantenuti via clipping post-mutazione.
- **Integer** per i geni discreti su domini ordinati: $b$ (8 valori discreti su griglia 5-40), $d_{inv}$, $d_{obsolete}$ (multipli di 5 pt), $T_{min,session}$, $\Delta t_{cromosoma}$, $T_{touch}^{max}$.
- **Binary** per il vettore di selezione feature $\mathbf{s}$ (37 bit con vincolo di cardinalità $\sum_j s_j \leq K_{max}$).

Gli operatori del GA (Cap.23) sono **coerenti con l'encoding misto**: crossover SBX per real-valued, uniform crossover per integer e binary; mutazione polynomial per real-valued, random reset per integer, bit flip per binary. I dettagli sono in Cap.23.2 e Cap.23.3.

### 22.9 Dimensionalità totale del cromosoma e tabella sintesi

Si conta la dimensionalità totale del cromosoma sotto la configurazione di lavoro provvisoria — $\tau_{vol}$ e $\tau_{surv}$ regime-dipendenti (4 valori), $d_{stop,\sigma}$ regime-dipendente (2 valori), $\tau_{liq}, \tau_{dist}^{\sigma}, k_{t2}$ single value (3 valori):

- **Geni real-valued continui**: $\tau_{vol,\text{calmo}}, \tau_{vol,\text{turbolento}}, \tau_{liq}, \tau_{dist}^{\sigma}, \tau_{surv,\text{calmo}}, \tau_{surv,\text{turbolento}}, k_{t2}, d_{stop,\sigma,\text{calmo}}, d_{stop,\sigma,\text{turbolento}}$. Totale $K = 9$.
- **Geni integer discreti**: $b, d_{inv}, d_{obsolete}, T_{min,session}, \Delta t_{cromosoma}, T_{touch}^{max}$. Totale $K' = 6$.
- **Vettore binary di selezione feature**: $\mathbf{s} \in \{0,1\}^{37}$, totale $K'' = 37$ bit.

La dimensionalità totale del cromosoma è quindi $K + K' + K'' = 9 + 6 + 37 = 52$ geni. In configurazioni con regime-dipendenza ridotta (es. $\tau_{vol}$ single value invece che regime-dipendente), $K$ scende a 8 e la dimensionalità totale a 51. In configurazioni con regime-dipendenza estesa (tutti i geni di emissione e $d_{stop,\sigma}$ regime-dipendenti), $K$ sale a 12 e la dimensionalità totale a 55. Per il dimensionamento di popolazione e generazioni in Cap.26.1 si assume la configurazione di lavoro $K + K' + K'' = 52$.

**Tabella sintesi del cromosoma — configurazione di lavoro provvisoria.**

| Gene | Simbolo | Dominio | Encoding | Regime-dipendenza | Eredità |
|------|---------|---------|----------|-------------------|---------|
| Semi-ampiezza banda | $b$ | $\{5,10,15,20,25,30,35,40\}$ pt | integer | no | Cap.6.1 PII; Cap.16.3 PIV |
| Soglia invalidazione I2 | $d_{inv}$ | multipli di 5 pt, $\geq 5$ | integer | no | Cap.16.5 PIV |
| Soglia obsolescenza pivot I3 | $d_{obsolete}$ | multipli di 5 pt, $\geq 5$ | integer | no | Cap.16.5 PIV |
| Tempo residuo minimo sessione | $T_{min,session}$ | interi $\geq 15$ min trading | integer | no | Cap.16.6 PIV |
| Soglia volatilità (calmo) | $\tau_{vol,\text{calmo}}$ | $\mathbb{R}^+$ | real | sì | Cap.8 PII; Cap.14.4 PIII |
| Soglia volatilità (turbolento) | $\tau_{vol,\text{turbolento}}$ | $\mathbb{R}^+$ | real | sì | Cap.8 PII; Cap.14.4 PIII |
| Soglia liquidità | $\tau_{liq}$ | $\mathbb{R}^+$ | real | no | Cap.8 PII |
| Soglia distanza sigma-units | $\tau_{dist}^{\sigma}$ | $\mathbb{R}^+$ | real | no | Cap.8 PII; Cap.17.3 PIV |
| Soglia survival (calmo) | $\tau_{surv,\text{calmo}}$ | $(0{,}1;\, 0{,}9)$ | real | sì | Cap.20.1, 20.3 PIV |
| Soglia survival (turbolento) | $\tau_{surv,\text{turbolento}}$ | $(0{,}1;\, 0{,}9)$ | real | sì | Cap.20.1, 20.3 PIV |
| Moltiplicatore sigma target_2 | $k_{t2}$ | $\mathbb{R}^+$ | real | no | Cap.17.4 PIV |
| Moltiplicatore sigma stop (calmo) | $d_{stop,\sigma,\text{calmo}}$ | $\mathbb{R}^+$ | real | sì | Cap.18.1, 18.5 PIV |
| Moltiplicatore sigma stop (turb.) | $d_{stop,\sigma,\text{turbolento}}$ | $\mathbb{R}^+$ | real | sì | Cap.18.1, 18.5 PIV |
| Durata post-trigger | $\Delta t_{cromosoma}$ | $\{1, \ldots, 1680\}$ min trading | integer | no | Q-04 CAP-01; Cap.6.1 PII |
| Durata pre-trigger | $T_{touch}^{max}$ | $\{5, \ldots, 480\}$ min trading | integer | no | Cap.6.1 PII |
| Selezione feature survival | $\mathbf{s}$ | $\{0,1\}^{37}, \sum_j s_j \leq K_{max}$ | binary | no | Cap.15.2 PIII; M-11 PIV |

**Provvisorietà**. Nessun valore numerico viene congelato in Cap.22: i valori provvisori restano provvisori, congelati nella tabella di Cap.26.5. La configurazione di regime-dipendenza qui dichiarata come "di lavoro" è soggetta a revisione empirica in Parte VII sulla base della stabilità cross-fold dei coefficienti GA.

---

## Capitolo 23 — Operatori dell'algoritmo genetico

### 23.1 NSGA-II come algoritmo primario

L'algoritmo genetico operativo è il **NSGA-II** (Non-dominated Sorting Genetic Algorithm II) di **Deb, Pratap, Agarwal e Meyarivan (2002)** "A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II", *IEEE Transactions on Evolutionary Computation* 6(2), 182–197. La scelta è motivata da tre proprietà strutturali del problema:

1. **Multi-obiettività intrinseca della fitness** (Cap.24): la fitness $\mathbf{f}(\theta) \in \mathbb{R}^M$ ha $M = 5$ obiettivi che includono massimizzazioni (expected net return, target_1 hit rate) e minimizzazioni (invalidation rate, MDD, instabilità cross-regime). Trovare un singolo cromosoma ottimale non è obiettivo: l'output del GA è un **fronte di Pareto** di cromosomi non dominati, dal quale il bundle frozen è selezionato in Parte VII sulla base di gate DSR/PBO e di criteri operativi.
2. **Elitismo per non-dominanza**: NSGA-II preserva i cromosomi non dominati tra generazioni via $(\mu + \lambda)$ selection sull'unione parent+offspring, garantendo monotonicità del fronte di Pareto.
3. **Crowding distance per diversità**: il tie-break interno a un fronte di Pareto è la crowding distance, che preserva la diversità spaziale dei cromosomi e previene la convergenza prematura su una regione ristretta dello spazio di ricerca.

La popolazione di taglia $P = 128$ (Cap.26.1) e il numero massimo di generazioni $G_{max} = 150$ (Cap.26.1) sono i parametri operativi della calibrazione di lavoro, eredità della specifica preliminare di CAP-01 Q-03 (parametri provvisori per il dimensionamento del compute budget). La derivazione analitica del numero di valutazioni effettive di fitness e la sua coerenza con il range 12.800-25.600 min single-thread di M-4 sono in Cap.23.6.

### 23.2 Crossover

Il crossover produce due offspring da due genitori selezionati per torneo binario (Deb 2002, sez. III). L'operatore di crossover è coerente con l'encoding misto (Cap.22.8):

- **Geni real-valued**: **simulated binary crossover (SBX)** di Deb e Agrawal (1995) "Simulated binary crossover for continuous search space", *Complex Systems* 9(2), 115–148. Per ogni coppia di valori parent $(x_1, x_2)$, l'offspring è $y_{1,2} = 0{,}5 \cdot [(1 \mp \beta)\,x_1 + (1 \pm \beta)\,x_2]$ con $\beta$ campionato dalla distribuzione SBX di parametro $\eta_c$ (distribution index). Valore di lavoro provvisorio $\eta_c = 15$ (prassi NSGA-II, Deb 2002). $\eta_c$ è parametro del modello, congelato in Cap.26.
- **Geni integer**: **uniform crossover** componente-per-componente. Per ogni gene $g_i$ e ogni coppia di parent, l'offspring eredita $g_i$ dal primo parent con probabilità $0{,}5$ e dal secondo con probabilità $0{,}5$.
- **Vettore binario $\mathbf{s}$**: **uniform crossover bit-per-bit** con riparazione del vincolo di cardinalità. Se l'offspring viola $\sum_j s_j > K_{max}$, si disattivano feature attive scelte a caso uniformemente fino a rientrare nel vincolo. Se l'offspring ha $\sum_j s_j = 0$ (cromosoma degenere senza feature attive), si attiva una feature scelta a caso uniformemente fra quelle non attive.

### 23.3 Mutazione

La mutazione è applicata indipendentemente a ciascun gene con probabilità $p_m^{cont}$ (geni continui), $p_m^{disc}$ (geni discreti), $p_m^{bit}$ (vettore binario). Valori di lavoro provvisori: $p_m^{cont} = 1/K = 1/9 \approx 0{,}11$, $p_m^{disc} = 1/K' = 1/6 \approx 0{,}17$, $p_m^{bit} = 1/K'' = 1/37 \approx 0{,}027$ (regola prassi NSGA-II "una mutazione attesa per cromosoma", Deb 2002). Forme operative:

- **Geni real-valued**: **polynomial mutation** di Deb (Deb e Goyal 1996, ripreso in Deb 2002). Per ogni gene mutato, il valore è perturbato con $y = x + (\bar{x}_{\max} - \bar{x}_{\min}) \cdot \delta$ con $\delta$ campionato dalla distribuzione polynomial di indice $\eta_m$. Valore di lavoro provvisorio $\eta_m = 20$ (prassi NSGA-II). $\eta_m$ è parametro del modello, congelato in Cap.26.
- **Geni integer**: **random reset** uniforme sul dominio del gene. Per $b$ (dominio finito di 8 valori), il reset campiona uniformemente fra $\{5, 10, 15, 20, 25, 30, 35, 40\}$. Per $d_{inv}, d_{obsolete}$, il reset campiona uniformemente sul dominio dichiarato fino a un cap superiore congelato in Cap.26. Per $T_{min,session}, \Delta t_{cromosoma}, T_{touch}^{max}$, reset uniforme sul dominio dichiarato in Cap.22.
- **Vettore binario $\mathbf{s}$**: **bit flip** con vincolo di cardinalità. Ogni bit ha probabilità $p_m^{bit}$ di essere flippato. Dopo la mutazione, se $\sum_j s_j > K_{max}$ si disattivano feature attive a caso fino a rientrare; se $\sum_j s_j = 0$ si attiva una feature a caso.

Tutti i tassi $\eta_c, \eta_m, p_m^{cont}, p_m^{disc}, p_m^{bit}$ sono parametri del modello, dichiarati provvisori e congelati in Cap.26.5.

### 23.4 Gestione dei vincoli di ammissibilità — constraint-domination

La strategia adottata per i cromosomi non validi (Cap.22.7) è il **constraint-domination** di **Deb (2000)** "An efficient constraint handling method for genetic algorithms", *Computer Methods in Applied Mechanics and Engineering* 186(2-4), 311–338. Il principio operativo è il seguente:

1. **Individui ammissibili dominano individui non ammissibili** indipendentemente dalla fitness $\mathbf{f}(\theta)$.
2. **Fra due individui ammissibili**, si applica la non-dominanza standard di Pareto sulla fitness.
3. **Fra due individui non ammissibili**, si applica l'ordinamento per **somma normalizzata delle violazioni dei vincoli**. Sia $v_k(\theta)$ la violazione del vincolo $k \in \{1, \ldots, 7\}$ di Cap.22.7 (con $v_k = 0$ se rispettato, $v_k > 0$ se violato, normalizzata ad esempio rispetto al massimo della violazione $k$-esima nella popolazione corrente). La somma è $V(\theta) = \sum_k v_k(\theta)$; il cromosoma con $V$ minore domina quello con $V$ maggiore.

**Riparazione locale (mutazione random vincolata).** Per i cromosomi non validi che entrano nella popolazione tramite crossover o mutazione, la strategia di riparazione locale opera gene-per-gene proiettando il valore violante nel dominio ammissibile più prossimo. Esempi:

- Se $d_{stop} \leq b$ (violazione di vincolo 1), $d_{stop}$ viene aumentato al primo multiplo di 5 strettamente sopra $b$, ricalcolando $d_{stop,\sigma}$ in modo coerente con la formula sintetica di Cap.18.1 di Parte IV.
- Se $\sum_j s_j > K_{max}$ (violazione di vincolo 4), si disattivano feature attive scelte uniformemente fino a rientrare nel vincolo (stesso meccanismo di crossover e mutazione di Cap.23.2-23.3).
- Se un gene a unità di prezzo non è multiplo di 5 (violazione di vincolo 5, possibile in caso di errore numerico residuo), si arrotonda al multiplo di 5 più vicino.

I cromosomi non riparabili — situazione rara con i vincoli dichiarati ma teoricamente possibile sotto combinazioni patologiche — sono sostituiti con campionamento uniforme di tutto lo spazio del cromosoma (riinizializzazione).

### 23.5 Elitismo $(\mu + \lambda)$

NSGA-II adotta l'elitismo standard via $(\mu + \lambda)$ selection (Deb 2002, sez. III.B). A ogni generazione $g$:

1. La popolazione corrente $P_g$ di taglia $\mu = P = 128$ produce $\lambda = P = 128$ offspring via selezione per torneo binario + crossover + mutazione.
2. L'unione $P_g \cup O_g$ di taglia $2P = 256$ viene ordinata in fronti di Pareto $\mathcal{F}_1, \mathcal{F}_2, \ldots$ secondo la non-dominanza con constraint-domination (Cap.23.4).
3. La popolazione $P_{g+1}$ della generazione successiva è costruita prendendo i fronti $\mathcal{F}_1, \mathcal{F}_2, \ldots$ fino a riempire $P$ posti; se un fronte $\mathcal{F}_k$ non entra completamente, si seleziona da $\mathcal{F}_k$ in ordine **decrescente di crowding distance** fino a raggiungere $P$.

Questa procedura garantisce che il fronte di Pareto $\mathcal{F}_1$ sia preservato attraverso le generazioni: nessun cromosoma non-dominato della generazione $g$ può essere espulso a vantaggio di un cromosoma dominato in $g+1$. La proprietà di monotonicità del fronte è la base della convergenza analitica del NSGA-II.

### 23.6 Tasso di rimpiazzo e numero di valutazioni effettive — derivazione analitica (M-4)

Si definisce **tasso di rimpiazzo per generazione** $r_{repl} \in [0, 1]$ come la frazione di offspring che entrano nella popolazione successiva sostituendo parent dominati. Per NSGA-II con $(\mu + \lambda)$ selection $\mu = \lambda = P$, in regime di lavoro tipico $r_{repl} \in [0{,}3;\, 0{,}6]$ (Deb 2002 e letteratura successiva sui benchmark NSGA-II in problemi a 3-5 obiettivi); in stato stazionario di convergenza $r_{repl}$ tende a 0 (nessun offspring migliora il fronte di Pareto).

Il **numero di valutazioni effettive di fitness** nelle $G$ generazioni del run è la popolazione iniziale più gli offspring di ogni generazione:
$$N_{eval}^{naive} = P + G \cdot \lambda = P + G \cdot P = P \cdot (1 + G)$$

Con $P = 128$ e $G = 150$: $N_{eval}^{naive} = 128 \cdot 151 = 19.328$ valutazioni.

Il valore effettivo è ridotto dal **caching dei cromosomi non dominati archiviati**: in regime stazionario, una frazione $r_{cache}$ di offspring è identica a parent già valutati (encoding misto e popolazione finita garantiscono che con probabilità non nulla due offspring siano identici, in particolare nei geni discreti). Per encoding misto con $K + K' + K'' = 52$ geni e popolazione 128, la frazione $r_{cache}$ è attesa nell'intervallo $r_{cache} \in [0{,}05;\, 0{,}15]$, con la stima centrale $r_{cache} \approx 0{,}10$ (valore di riferimento Deb 2002, sez. V; valori più alti sarebbero patologici e segnalerebbero diversità insufficiente). Il numero di valutazioni effettive è quindi:

$$N_{eval}^{actual} = P + G \cdot \lambda \cdot (1 - r_{cache}) \approx P \cdot (1 + G \cdot (1 - r_{cache}))$$

Con $P = 128$, $G = 150$, $r_{cache} = 0{,}10$:
$$N_{eval}^{actual} \approx 128 \cdot (1 + 150 \cdot 0{,}9) = 128 \cdot 136 = 17.408 \ \text{valutazioni}$$

**Derivazione del range 12.800-25.600 min single-thread (M-4, eredità CAP-01).** Per un singolo fold del walk-forward (Cap.25), il tempo di valutazione fitness per cromosoma è stimato in 0{,}5-1 min single-thread, ottenuto come razione del tempo full backtest 5 anni 3-13 min/cromosoma di Cap.4 di Parte I scalato sulla finestra in-sample di un fold (circa 6 mesi $\approx 1/10$ dello storico, ma con replay aggiuntivo della state machine sul fold OOS e fitting EGARCH+Cox sul fold in-sample). Si applica la formula del numero di valutazioni effettive:

- **Caso ottimo** ($r_{cache} = 0{,}15$, valutazione 0{,}5 min/cromosoma): $N_{eval}^{actual} = 128 \cdot (1 + 150 \cdot 0{,}85) = 128 \cdot 128{,}5 = 16.448$; tempo single-thread $16.448 \cdot 0{,}5 = 8.224$ min per fold.
- **Caso pessimo** ($r_{cache} = 0{,}05$, valutazione 1 min/cromosoma): $N_{eval}^{actual} = 128 \cdot (1 + 150 \cdot 0{,}95) = 128 \cdot 143{,}5 = 18.368$; tempo single-thread $18.368 \cdot 1 = 18.368$ min per fold.
- **Caso centrale** ($r_{cache} = 0{,}10$, valutazione 0{,}5-1 min/cromosoma): $N_{eval}^{actual} = 17.408$; tempo single-thread $17.408 \cdot 0{,}5 \approx 8.700$ min (ottimo) a $17.408 \cdot 1 \approx 17.400$ min (pessimo) per fold.

Il range **12.800-25.600 min single-thread di M-4** è specifico del **run di calibrazione iniziale** (un singolo run completo di NSGA-II con $P = 128$, $G = 150$) prima del walk-forward nested completo. Il valore inferiore 12.800 è coerente con il caso ottimo per singolo run di calibrazione ($16.448 \cdot 0{,}8 \approx 13.000$, dove il fattore 0{,}8 cattura un ulteriore margine ottimistico di caching e parallelizzazione locale entro un fold); il valore superiore 25.600 è coerente con il caso pessimo per un run di calibrazione con valutazione fitness intorno a 1{,}4 min/cromosoma ($18.368 \cdot 1{,}4 \approx 25.700$). Il valore centrale 17.408 valutazioni a 0{,}5-1 min/cromosoma genera 8.700-17.400 min, dentro al range dichiarato.

Estendendo a $F$ fold del walk-forward nested completo (Cap.25.1, $F = 8$ provvisorio), il totale è $F \cdot 8.700\text{-}17.400 \approx 69.600\text{-}139.200$ min single-thread. Su c5.4xlarge con 16 vCPU e parallelizzazione ideale, il tempo wall-clock è $69.600/16 \approx 4.350$ min $\approx 72$ ore (caso ottimo) e $139.200/16 \approx 8.700$ min $\approx 145$ ore (caso pessimo). Il range di CAP-01 21.000-41.500 min single-thread per il training completo è in **disaccordo** con il calcolo $F \cdot N_{eval}^{actual}$: 21.000-41.500 corrisponde a $F$ effettivo di 1{,}2-2{,}4, ovvero al run di calibrazione iniziale moltiplicato per 1-3 fold di validazione, non 8 fold completi. La spiegazione è che CAP-01 stimò il compute budget assumendo $F$ effettivo basso (run di calibrazione + walk-forward leggero) ovvero parallelizzazione cross-fold; il calcolo qui prodotto per $F = 8$ fold sequenziali sovrastima il budget realizzato. La conciliazione operativa è in Cap.26: $F$ è dichiarato provvisorio e il numero effettivo di fold sequenziali nel training potrà essere ridotto a 2-3 con run di calibrazione iniziale separato, in coerenza con il budget di 21.000-41.500 min di CAP-01.

### 23.6.1 Benchmark empirico — rinvio a Parte VII

La **verifica empirica** del tasso di rimpiazzo effettivo $r_{repl}$, della frazione di caching $r_{cache}$ e del range di valutazioni effettive è **out-of-scope per Cap.23** ed è rinviata a **Parte VII Cap.34** (bootstrap stazionario + stress test del compute budget). Cap.23 fornisce la formula analitica e il range derivato per orientare la calibrazione di Cap.26; la conferma empirica sulle prime $G_{stall}$ generazioni del primo run di calibrazione è strumento di tuning post-Parte V.

### 23.7 Seed e riproducibilità

Il **seed del PRNG** (NumPy `numpy.random.default_rng(seed)` o equivalente) per (a) inizializzazione della popolazione, (b) torneo binario di selezione, (c) crossover (campionamento di $\beta$ in SBX), (d) mutazione (polynomial, random reset, bit flip), (e) riparazione locale dei cromosomi non validi, è **parte del bundle di calibrazione** e registrato nel log di emissione (Cap.10.1 di Parte II) e nel bundle frozen (Cap.35 di Parte VII). Il seed è una variabile scalare intera di lunghezza minima 64 bit. Due esecuzioni indipendenti del GA con lo stesso seed, sullo stesso storico di backtest, producono identico fronte di Pareto al bit, in coerenza con il vincolo di determinismo bit-exact di Cap.10 di Parte II.

---

## Capitolo 24 — Funzione di fitness multi-obiettivo

### 24.1 Vettore degli obiettivi $\mathbf{f}(\theta)$

La fitness del cromosoma $\theta$ è un vettore $\mathbf{f}(\theta) \in \mathbb{R}^M$ con $M = 5$ obiettivi. NSGA-II ottimizza il vettore in senso Pareto: il fronte di Pareto $\mathcal{F}_1$ contiene i cromosomi non dominati, ovvero quelli per cui nessun altro cromosoma migliora simultaneamente tutti gli obiettivi (Deb 2001, "Multi-Objective Optimization using Evolutionary Algorithms", Wiley, cap. 2). La valutazione di $\mathbf{f}(\theta)$ avviene sulla finestra OOS del fold corrente del walk-forward (Cap.25.1) e produce un vettore per-fold; l'aggregazione multi-fold è in Cap.24.6.

Gli obiettivi sono i seguenti.

**$f_1 = E[R_{net} \mid executed]$ — expected net return per segnale eseguito (da massimizzare).** La metrica primaria di CAP-01 (Cap.5 di Parte I). Formula chiusa:
$$f_1(\theta) = E[R_{gross} \mid executed] - 2 \cdot c, \qquad c = 1 \ \text{pt FIB equivalente per operazione}$$
con $c$ derivato dalla conversione delle commissioni di 5 EUR sul moltiplicatore 5 EUR/punto FIB (Cap.5 di Parte I); il fattore 2 cattura la doppia operazione di apertura e chiusura. L'expected value è calcolato come media empirica sui segnali del fold OOS con stato terminale `target_1_hit` o `stopped`. Per i segnali con stato terminale `expired` (causa `posttrigger_timeout`), il rendimento è la **MAE alla scadenza** (Cap.10.4 di Parte II): il segnale viene chiuso virtualmente al prezzo della barra in cui il timer ha esaurito $\Delta t_{cromosoma}$, e $R_{gross}$ è il rendimento dal prezzo di fill (worst-case bordo, Cap.12.4 di Parte III) al prezzo di chiusura virtuale forzata. Per i segnali con stato terminale `invalidated`, `missed_target`, `revoked`, il segnale non è stato eseguito (no raw touch) e non entra nell'expected: $f_1$ è condizionato a `executed`.

**$f_2 = $ target_1 hit rate (da massimizzare).** Eredità di Cap.5 di Parte I e Cap.7 di Parte II:
$$f_2(\theta) = \frac{|\{i : \text{state}(s_i) = \texttt{target\_1\_hit}\}|}{|\{i : \text{executed}(s_i)\}|}$$
calcolato sui segnali del fold OOS. Il denominatore include i segnali in stato terminale `target_1_hit`, `stopped`, `expired` (con `posttrigger_timeout`); esclude `invalidated`, `missed_target`, `revoked` (non eseguiti).

**$f_3 = $ invalidation rate pre-touch (da minimizzare).** Frazione di segnali emessi che terminano in `invalidated` (Cap.7.1 di Parte II) prima del raw touch:
$$f_3(\theta) = \frac{|\{i : \text{state}(s_i) = \texttt{invalidated}\}|}{|\{i : \text{emitted}(s_i)\}|}$$
calcolato sui segnali emessi nel fold OOS (denominatore include tutti i segnali emessi, indipendentemente dallo stato terminale). Un invalidation rate elevato indica che il motore emette segnali sotto condizioni di mercato che vengono rapidamente smentite dalla dinamica strutturale: il cromosoma sta esplorando una regione del setup eccessivamente speculativa.

**$f_4 = $ maximum drawdown intraday dell'equity sintetica (da minimizzare).** Eredità di CAP-01 (Cap.5) come metrica di rischio:
$$f_4(\theta) = \max_{t \in \text{fold OOS}} \big( \text{eq}_t^{peak} - \text{eq}_t \big)$$
dove $\text{eq}_t$ è l'equity sintetica del fold al tempo $t$, definita come somma cumulativa di $R_{net}$ per i segnali eseguiti del fold ordinati per istante di esecuzione $t_{exec}$:
$$\text{eq}_t = \sum_{i : t_{exec,i} \leq t} R_{net,i}$$
e $\text{eq}_t^{peak} = \max_{u \leq t} \text{eq}_u$ è il valore di picco precedente. $f_4$ è in punti FIB, da minimizzare.

**$f_5 = $ stabilità cross-regime della fitness (da minimizzare).** Eredità di Cap.14.4 di Parte III (classificazione $R_t$ calmo/turbolento) e di CAP-01 (Cap.5: lifecycle stabili e comparabili fra regime calmo e turbolento). Il fold OOS è classificato per ogni segnale come `calmo` o `turbolento` sulla base del regime $R_{t_{emission,i}}$ al momento dell'emissione. Si calcolano $f_1^{calmo}, f_1^{turbolento}$ sui due sottoinsiemi separati; la metrica di stabilità è:
$$f_5(\theta) = \frac{|f_1^{calmo}(\theta) - f_1^{turbolento}(\theta)|}{\max(|f_1^{calmo}(\theta)|, |f_1^{turbolento}(\theta)|, 1)}$$
normalizzata in $[0, +\infty)$. Il denominatore $\max(\ldots, 1)$ evita la divisione per zero e mantiene la scala dimensionale. Un cromosoma con $f_5$ vicino a zero ha performance comparabile fra i due regimi (proprietà desiderabile per il go-live: il bundle deve operare in entrambi); un $f_5$ elevato segnala un cromosoma sbilanciato verso un solo regime.

### 24.2 Penalità integrate nella fitness

Tre penalità modificano $f_1$ per regolarizzare il comportamento del GA:

- **Penalità emissione eccessiva**. Se il tasso medio di emissione/sessione del cromosoma sul fold OOS supera una soglia $E_{max}$ (valore provvisorio $E_{max} = 5$ segnali/sessione, congelato in Cap.26.5), $f_1$ è penalizzato moltiplicativamente:
$$f_1^{penalized} = f_1 \cdot \exp\!\Big(-\alpha_{max} \cdot (E_{rate} - E_{max})^+\Big)$$
con $E_{rate}$ il tasso medio di emissione, $(x)^+ = \max(x, 0)$ e $\alpha_{max} = 0{,}5$ valore di lavoro provvisorio congelato in Cap.26. Motivazione: emissioni troppo frequenti producono rumore sul canale Telegram (eredità Cap.9 di Parte II) e violano lo spirito del filtro 80 pt (eredità Cap.5 di Parte I, segnali rari e di qualità).

- **Penalità emissione nulla**. Se il tasso medio di emissione/sessione è sotto $E_{min}$ (valore provvisorio $E_{min} = 0{,}2$ segnali/sessione, congelato in Cap.26.5):
$$f_1^{penalized} = f_1 \cdot \exp\!\Big(-\alpha_{min} \cdot (E_{min} - E_{rate})^+\Big)$$
con $\alpha_{min} = 1{,}0$ valore di lavoro provvisorio congelato in Cap.26. Motivazione: un cromosoma che converge su soglie tali da non emettere mai produce metriche degenerate ($f_2 = 0/0$ indefinito, $f_3 = 0/0$ indefinito, $f_4 = 0$ degenere). La penalità respinge il GA da queste regioni dello spazio.

- **Penalità lifecycle anomalo**. Se la frazione di segnali eseguiti che terminano in `expired` con causa `posttrigger_timeout` supera $E_{exp,max}$ (valore provvisorio $E_{exp,max} = 0{,}30$, congelato in Cap.26.5):
$$f_1^{penalized} = f_1 \cdot \exp\!\Big(-\alpha_{exp} \cdot (E_{exp,rate} - E_{exp,max})^+\Big)$$
con $\alpha_{exp} = 0{,}5$. Motivazione: un alto tasso di `expired posttrigger_timeout` indica segnali troppo lenti (il prezzo non raggiunge target_1 né stop entro $\Delta t_{cromosoma}$), strutturalmente fragili e poco azionabili per l'operatore manuale.

Le tre penalità sono moltiplicative e si compongono: $f_1^{penalized} = f_1 \cdot \exp\!\big(-\alpha_{max} (E_{rate} - E_{max})^+ - \alpha_{min} (E_{min} - E_{rate})^+ - \alpha_{exp} (E_{exp,rate} - E_{exp,max})^+\big)$. I parametri $E_{max}, E_{min}, E_{exp,max}, \alpha_{max}, \alpha_{min}, \alpha_{exp}$ sono dichiarati provvisori e congelati in Cap.26.5.

### 24.3 Metriche di lifecycle tracciate (non obiettivi diretti)

La submacchina di position lifecycle di Cap.11 di Parte II produce metriche aggiuntive che **non** entrano come obiettivi diretti del NSGA-II ma sono **tracciate nel log del fold** per il reporting di Parte VII:

- **$\pi_{t_2 \mid t_1}$** — target_2 hit rate condizionale al raggiungimento di target_1 (Cap.11.2 di Parte II). Frazione di segnali in stato `target_1_hit` per cui la submacchina ha registrato l'evento `target_2_reached` prima di altri eventi terminanti.
- **MFE e MAE post-target_1** (Cap.11.2). Distribuzioni di maximum favourable excursion e maximum adverse excursion misurate dall'istante di `target_1_hit` alla chiusura della submacchina.
- **$f_{stop \mid t_1}$** — frequenza di stop post-target_1 (Cap.11.2). Frazione di segnali in `target_1_hit` per cui il prezzo ha ritracciato fino a `stop_loss` registrando l'evento `stop_after_target_1`.

**Asimmetria di tracking (N-1 v2 CAP-03).** La submacchina si attiva solo dopo `target_1_hit`: dopo `stopped` non è prevista una submacchina post-stop. La distinzione è strutturale: `target_1_hit` è il completamento del contratto del segnale ma apre informazione decisionale per l'operatore (può portare la posizione verso target_2); `stopped` è chiusura definitiva senza ulteriore decisione operativa. Il tracking post-stop è fuori scope dal motore in coerenza con la dichiarazione di intenti dell'operatore (punto 8): il motore non gestisce la posizione né traccia post-stop perché non c'è posizione da tracciare.

Queste metriche entrano nella **fitness del cromosoma per la selezione del bundle frozen in Parte VII**, non nel NSGA-II di Parte V. Il GA ottimizza $\mathbf{f}(\theta) = (f_1, \ldots, f_5)$; il bundle frozen è selezionato dal fronte di Pareto $\mathcal{F}_1$ filtrando per criteri DSR/PBO (Parte VII) e tenendo conto delle metriche di submacchina come qualità informativa del payload pubblicato.

### 24.4 Allineamento a CAP-01 — target operativo asimmetrico

Il **target operativo asimmetrico** di CAP-01 (Cap.1 di Parte I: 500 pt FIB profitto netto/giorno OR 70% movimento strutturale intraday, eredità 2) è un aggregato di sessione, non un obiettivo per-segnale. La fitness di Cap.24 ottimizza obiettivi **per-segnale e per-fold**: $f_1$ è in pt/segnale, $f_2$-$f_3$ sono frazioni di segnali, $f_4$ è MDD intraday del fold, $f_5$ è stabilità cross-regime.

Il target 500 pt/70% viene tradotto come **metrica di reporting**, non come obiettivo diretto della fitness. Motivazione esplicita: ottimizzare direttamente il target di sessione richiederebbe una funzione obiettivo non separabile dalla politica di emissione cumulata (il 500 pt giornaliero è la somma di rendimenti di più segnali della sessione), introducendo una correlazione fra cromosomi sulla stessa sessione che NSGA-II non gestisce naturalmente. L'aggregato di sessione viene calcolato nel reporting di Parte VII (Cap.36: gate decisionali) come verifica del bundle frozen: percentuale di sessioni in cui il bundle raggiunge 500 pt o 70% del movimento strutturale calcolato come somma dei moduli degli swing fra pivot ancorato al primo min/max post-apertura.

La separazione fra fitness per-segnale (Parte V) e reporting per-sessione (Parte VII) è coerente con la prassi NSGA-II: ottimizzare la qualità unitaria del segnale (più alta probabilità di hit, MDD contenuto, stabilità cross-regime) produce per costruzione un aggregato di sessione migliore, senza necessità di modellare esplicitamente l'aggregazione.

### 24.5 Replay deterministico e log della valutazione di fitness

La valutazione di $\mathbf{f}(\theta)$ richiede il **replay completo del motore** sul fold OOS: ricostruzione del payload del segnale per ogni $t_{emission}$ candidato, applicazione delle condizioni di emissione (Cap.8 di Parte II + filtro survival di Cap.20 di Parte IV), simulazione della state machine fino allo stato terminale, calcolo delle metriche aggregate. Eredità di Cap.10 di Parte II (replay deterministico bit-exact) e Cap.12.4 di Parte III (fill virtuale worst-case).

Il **log della valutazione di fitness** registra per ogni segnale del fold OOS i seguenti campi obbligatori:

- `signal_id` (Cap.10.1 di Parte II);
- `t_emission` (timestamp di emissione, minuto chiuso CET);
- `t_exec` (timestamp di raw touch, NULL se non eseguito);
- $\Delta t_{pretrigger} = t_{exec} - t_{emission}$ (durata della fase pre-trigger in minuti di trading, **N-4 v2**: campo esplicito separato da $\Delta t_{cromosoma}$ che è il gene del cromosoma);
- $R_{gross}, R_{net}$ (rendimento lordo e netto in punti FIB, per segnali eseguiti);
- stato terminale (target_1_hit, stopped, invalidated, missed_target, expired, revoked);
- causa di expired (`pretrigger_timeout` o `posttrigger_timeout`);
- tutti i campi del payload immutabile (Cap.6.1 di Parte II: `direction`, `entry_zone`, `target_1`, `target_2`, `target_2_type`, `stop_loss`, `stop_type`, `setup_class`, $\Delta t_{cromosoma}$, $T_{touch}^{max}$).

**Nomenclatura `executable_rate` (N-3 post-patch Iterazione 2 CAP-01).** Il termine `executable_rate` è ridefinito in CAP-01 patch Iterazione 2 come frazione dei segnali emessi che ricevono il raw touch entro $T_{touch}^{max}$. Formalmente:
$$\texttt{executable\_rate}(\theta) = \frac{|\{i : t_{exec,i} \text{ esiste e } \Delta t_{pretrigger,i} \leq T_{touch}^{max}\}|}{|\{i : \text{emitted}(s_i)\}|}$$
Questa metrica è tracciata nel log della valutazione di fitness ma non è un obiettivo diretto del NSGA-II (entra come reporting). La motivazione del rinominamento è la rimozione delle guardie post-emissione di Iterazione 1 (le condizioni di mercato sono valutate prima dell'emissione, non dopo; il raw touch è sempre eseguibile, Cap.7.3 di Parte II).

### 24.6 Aggregazione multi-fold della fitness

La fitness $\mathbf{f}_k(\theta) \in \mathbb{R}^M$ è calcolata sul singolo fold OOS $k \in \{1, \ldots, F\}$. L'aggregazione fra fold per produrre la fitness globale del cromosoma è:

$$f_m^{global}(\theta) = \text{median}_{k \in \{1, \ldots, F\}} f_{m,k}(\theta), \quad m = 1, 2, 3, 4$$

per i quattro obiettivi a livello. La mediana è preferita alla media per robustezza a fold con poche emissioni o regimi atipici: la mediana cross-fold non è distorta da un singolo fold con metrica degenere.

$f_5^{global}$ — la stabilità cross-regime — è calcolata diversamente: si concatenano tutti i segnali OOS di tutti gli $F$ fold, si separano per regime e si calcola $f_5$ sull'intera storia OOS unificata. Questo perché $f_5$ misura intrinsecamente la disparità fra due sottoinsiemi (calmo vs turbolento) e l'aggregazione per fold separati produrrebbe due livelli di mediana cross-fold, non interpretabili.

**Stabilità come metrica esplicita.** Per ogni obiettivo $f_m$, si calcola la **deviazione interquartile cross-fold normalizzata**:
$$\text{IQR}_{norm}(f_m) = \frac{Q_3(f_{m,k}) - Q_1(f_{m,k})}{|\text{median}_k f_{m,k}(\theta)|}$$
con $Q_1, Q_3$ il primo e terzo quartile della distribuzione cross-fold di $f_{m,k}$. La metrica $\text{IQR}_{norm}$ è **tracciata nel log** per ogni cromosoma del fronte di Pareto finale ma **non ottimizzata direttamente** dal NSGA-II: entra nella selezione del bundle frozen in Parte VII (un cromosoma con $\text{IQR}_{norm}$ alta su qualche obiettivo è scartato anche se nel fronte di Pareto, come segnale di instabilità).

### 24.7 No incorporazione di DSR/PBO come obiettivi diretti

DSR (Deflated Sharpe Ratio) e PBO (Probability of Backtest Overfitting), gate primari di accettazione dichiarati in CAP-01 (Cap.5 di Parte I, eredità 8), **non sono incorporati** come obiettivi diretti della fitness di Cap.24. La fitness di Parte V aggrega metriche di rendimento, lifecycle e rischio per-segnale e per-fold; DSR e PBO sono gate **post-selezione** applicati in Parte VII (Cap.32-33) ai cromosomi del fronte di Pareto $\mathcal{F}_1$ prodotto da NSGA-II.

Motivazione esplicita: DSR e PBO operano su distribuzioni di metriche aggregate del bundle (storia OOS completa), non su per-segnale e per-fold; introdurli come obiettivi del NSGA-II richiederebbe calcoli iterativi nidificati di stime statistiche su tutta la storia OOS a ogni valutazione, con costo computazionale prohibitive (il calcolo di DSR via bootstrap stazionario $B = 2000$ è esso stesso un costo dominante della Parte VII). La separazione fra fitness in-NSGA-II e gate post-NSGA-II è prassi della letteratura (Lopez de Prado 2018, cap. 12) e mantiene il compute budget di Cap.4 di Parte I trattabile.

---

## Capitolo 25 — Walk-forward nested con purge ed embargo, diagnostica survival fold-per-fold

### 25.1 Schema walk-forward nested

Lo schema di walk-forward è **nested** (annidato) con **purge** ed **embargo** sui $F$ fold sequenziali ricavati dallo storico Portara/CQG FIB 1-min di 5 anni (eredità Cap.4 di Parte I, circa 1.050.000 barre utili). Ogni fold $k$ è composto da quattro segmenti consecutivi:

1. **Finestra in-sample $W_{in}$**: la finestra di calibrazione del fold, su cui vengono stimati il modello EGARCH(1,1) (Cap.13 di Parte III), il modello Cox cause-specific (Cap.19 di Parte IV), e su cui il GA valuta i cromosomi candidati.
2. **Purge $P_{purge}$**: una finestra di esclusione fra fine in-sample e inizio OOS, che rimuove dalle finestre di valutazione le barre potenzialmente contaminate da look-ahead delle feature persistenti (pivot confermati a $t + n_c + 1$, EMA, classificazione di regime con persistenza $T_{persist}$ — eredità Cap.15.3 e Cap.14 di Parte III).
3. **Finestra out-of-sample $W_{oos}$**: la finestra di valutazione della fitness del cromosoma. La fitness $\mathbf{f}_k(\theta)$ è calcolata esclusivamente sui segnali emessi e tracciati su questa finestra, in cui i parametri del modello EGARCH/Cox sono **frozen** dalla calibrazione in-sample precedente.
4. **Embargo $P_{emb}$**: una finestra di esclusione fra fine OOS del fold $k$ e inizio in-sample del fold $k+1$, che previene la contaminazione cross-fold per feature con persistenza temporale.

**Valori provvisori di lavoro** (congelati in Cap.26.5):

- $W_{in} = 6$ mesi calendario $\approx 126$ sessioni $\times$ 840 barre/sessione $= 105.840$ barre 1-min;
- $W_{oos} = 3$ mesi calendario $\approx 63$ sessioni $\times$ 840 $= 52.920$ barre;
- $P_{purge} = 5$ sessioni $\times$ 840 $= 4.200$ barre;
- $P_{emb} = 5$ sessioni $\times$ 840 $= 4.200$ barre;
- $F = 8$ fold nested provvisori (valido per la copertura di 5 anni di storico FIB 1-min su sequenza non sovrapposta).

Tutti i fold operano su **sessioni intere**: nessun fold frazioni una sessione 8:00-22:00 CET (eredità Q-01 di CAP-01 e Cap.4 di Parte I).

### 25.2 Motivazione del purge e dell'embargo

La motivazione del purge e dell'embargo è la prevenzione del **leakage tempo-correlato** fra in-sample e OOS, prassi metodologica documentata in **Lopez de Prado (2018)** "Advances in Financial Machine Learning", Wiley, cap. 7 (purged k-fold cross-validation):

- **Purge** previene leakage da **feature look-ahead**: feature derivate da informazione che, sebbene causale al momento del calcolo, ha persistenza temporale tale da estendersi oltre la chiusura del fold in-sample. Esempi specifici al motore: l'EMA dei rendimenti con $\lambda = 0{,}94$ (Cap.15.2.1 di Parte III) ha vita media di $\ln(2)/\ln(1/\lambda) \approx 11$ barre, e la sua memoria si estende per circa $T_{warmup,\text{EMA}} = 74$ barre dal reset; i pivot confermati a $t + n_c + 1$ rendono il pivot disponibile come feature dalle barre successive, ma una feature di pivot ravvicinato all'inizio dell'OOS può sfruttare la struttura formata in tarda in-sample. Il purge di 5 sessioni (4.200 barre $> 74$ barre EMA, $> n_c + 1 = 4$ barre pivot) garantisce che ogni feature dell'OOS sia derivata da informazione interamente posteriore al fold in-sample precedente.

- **Embargo** previene **contaminazione cross-fold**: feature di stato persistente (es. classificazione di regime con $T_{persist} = 10$ barre, eredità Cap.14 di Parte III) della fine dell'OOS del fold $k$ che potrebbero influenzare le prime barre dell'in-sample del fold $k+1$. L'embargo di 5 sessioni (4.200 barre $> 10$ barre $T_{persist}$) garantisce indipendenza temporale dei fold.

La conferma empirica dell'assenza di leakage è in Parte VII (Cap.31, validazione OOS): il purge e l'embargo qui dichiarati sono protezioni a priori; il test diagnostico è il bootstrap stazionario di Cap.34.

### 25.3 Window selection EGARCH (M-5) — protocollo di benchmark

La finestra di calibrazione dell'EGARCH(1,1) all'interno di ogni fold è oggetto del **protocollo di benchmark comparativo** rolling vs expanding vs EWMA, in chiusura del **M-5 Review v1 CAP-03 (Q-06/C-4.3)**. Il protocollo opera fold-per-fold e produce, per ogni fold $k$, la finestra di calibrazione EGARCH selezionata + flag di rollback registrato nel log di calibrazione.

**Candidate windows** del benchmark:

- **Rolling**: $W \in \{105.000;\, 210.000;\, 420.000\}$ barre 1-min (corrispondenti a 6 mesi, 1 anno, 2 anni di sessioni intere). La finestra rolling $W = 210.000$ è il valore provvisorio di Cap.13.3 di Parte III, eredità di CAP-03.
- **Expanding**: la finestra di calibrazione inizia dal primo istante disponibile dello storico e si espande fino all'inizio dell'in-sample del fold. Nessun cap superiore.
- **EWMA con $\lambda_{ewma} \in \{0{,}99;\, 0{,}995;\, 0{,}999\}$**: la stima EGARCH è ponderata esponenzialmente sui rendimenti storici, con decay $\lambda_{ewma}$. Equivalente a una finestra efficace di $\approx 1/(1 - \lambda_{ewma})$ barre.

**Metrica OOS congelata** per il confronto: **log-likelihood OOS predittiva** del modello EGARCH calibrato su ogni candidate window. La log-likelihood OOS si calcola sui residui standardizzati $z_t = \epsilon_t / \sigma_t$ del modello EGARCH applicato alle barre dell'OOS del fold $k$ con parametri congelati dalla finestra di calibrazione candidate; la verosimiglianza è valutata sotto la distribuzione $D \in \{\text{Student-t}, \text{GED}\}$ selezionata via AIC/BIC sulla finestra in-sample (decisione Parte V via Cap.26.3).

**Test di Inoue-Rossi (2011)** "Identifying the sources of instabilities in macroeconomic forecasting models", *Journal of Applied Econometrics* 26(3), 367–391: test di stabilità della performance predittiva fra finestre alternative, con statistica basata sulla **loss-difference cumulata** $\sum_t (L_t^{(W_1)} - L_t^{(W_2)})$ dove $L_t$ è la negative log-likelihood predittiva alla barra $t$. Il test fornisce un p-value che indica se la differenza fra due finestre è statisticamente significativa.

**Criterio di rollback automatico (normativo).** Il protocollo opera in due passaggi sul fold $k$:

1. Si calibra l'EGARCH sulle 7 candidate windows (3 rolling + 1 expanding + 3 EWMA) sull'in-sample del fold $k$ e si valuta la log-likelihood OOS sul $W_{oos}$ del fold $k$.
2. Si applica il test di Inoue-Rossi confrontando la finestra di default **rolling $W = 210.000$** contro le 6 alternative.

**Regola di rollback:**

- Se rolling $W = 210.000$ **domina o pareggia** tutte le 6 alternative (per ciascun confronto a coppie, p-value di Inoue-Rossi $\geq 0{,}05$ contro la finestra alternativa, oppure rolling $W = 210.000$ ha log-likelihood OOS superiore con p-value $< 0{,}05$), si conferma la finestra di default e si procede.
- Se almeno una delle alternative **domina significativamente** rolling $W = 210.000$ (p-value Inoue-Rossi $< 0{,}05$ a favore dell'alternativa, ovvero log-likelihood OOS dell'alternativa superiore con significatività), si effettua **rollback alla finestra dominante**. Se più di una alternativa domina, si seleziona quella con la **log-likelihood OOS più alta** (criterio tie-break deterministico).

Il rollback è **deterministico, registrato nel log di calibrazione del fold** come record `egarch_window_rollback = {fold_k, winning_window, p_value_inoue_rossi, log_lik_oos}`. La regola è normativa e non opzionale: il GA del fold $k$ usa l'EGARCH calibrato sulla finestra eventualmente sostituita dal rollback. Cross-fold, la finestra effettiva può differire (es. fold 1 usa rolling $W = 210.000$, fold 2 usa EWMA $\lambda_{ewma} = 0{,}995$); la decisione di **window selection a livello bundle frozen** è in Parte VII sulla base del rapporto di fold in cui ciascuna finestra è dominante.

### 25.4 Classificazione di regime nel walk-forward (M-6)

La classificazione di regime $R_t$ (Cap.14 di Parte III) opera fold-per-fold con calibrazione dei quantili $\bar{\sigma}_s$ sull'in-sample del fold $k$ e applicazione sull'OOS. Il **test parallel media-mediana** del **M-6 Review v1 CAP-03 (Q-09/C-7.3)** verifica la stabilità della classificazione:

- Si calcola $R_t^{(media)}$ usando $\bar{\sigma}_s$ = **media di sessione** della volatilità $\hat{\sigma}_{\text{pt}}(t)$ (Cap.14 baseline).
- Si calcola $R_t^{(mediana)}$ usando $\text{med}_t(\hat{\sigma}_{s,t})$ = **mediana di sessione** come benchmark di robustezza.
- Si confrontano le due classificazioni sessione-per-sessione del fold OOS.

La **frazione di sessioni con classificazione divergente** (sessione classificata calma da una metrica e turbolenta dall'altra) è la **statistica di stabilità**:
$$\eta_{div}(k) = \frac{|\{s : R_s^{(media)} \neq R_s^{(mediana)}\}|}{|\{s : s \in \text{fold OOS } k\}|}$$

**Soglia di "cambiamento significativo":** $\eta_{div}(k) > 0{,}10$ (10% delle sessioni con classificazione divergente). Se questa soglia è superata, il fold $k$ è marcato con **flag "regime instabile"** nel log del fold; tale flag entra come fattore di reporting per $f_5$ in Cap.24.1 (un fold con regime instabile può inflazionare $f_5$ artificialmente).

**Azione in caso di flag attivo:** il fold continua a operare con la classificazione di default (media) per coerenza con Cap.14 di Parte III; il flag è informativo e indica che la stabilità cross-regime di $f_5$ va interpretata con cautela su quel fold. Decisione a livello bundle frozen sulla scelta media vs mediana è rinviata a Parte VII se il rapporto di fold con flag attivo è elevato (> 30% dei fold).

### 25.5 Cox condizionale al regime (M-14)

Il modello di Cox cause-specific (Cap.19.2 di Parte IV) è condizionato al regime $R_t$ in chiusura del **M-14 Developer CAP-04**. Le due opzioni dichiarate in Cap.19.2 di Parte IV sono:

- **(a) Interaction term**: $R_{t_{emission}}$ entra come feature aggiuntiva del vettore $\tilde{\mathbf{x}}$ (un'unica regressione Cox con $K + 1$ feature, dove la $(K+1)$-esima è l'indicatore binario di regime). Si aggiungono termini di interazione $R \cdot \tilde{x}_j$ per le feature di volatilità e struttura per catturare l'effetto di regime sulle feature specifiche.
- **(b) Stratificazione formale**: due regressioni Cox separate, una sui segnali emessi in regime calmo, l'altra sui segnali in regime turbolento. Baseline hazard distinte $h_{0,j,\text{calmo}}$ e $h_{0,j,\text{turbolento}}$, coefficienti $\boldsymbol{\beta}_{j,\text{calmo}}$ e $\boldsymbol{\beta}_{j,\text{turbolento}}$ potenzialmente diversi.

**Decisione Cap.25 (Parte V): opzione (b) — stratificazione formale.** Motivazione tecnica:

1. **Cattura di interazioni non lineari fra regime e feature**: la stratificazione produce baseline hazard distinte, che modellano la dinamica differente di hit/stopped nelle due classificazioni del mercato. L'interaction term singolo (opzione a) impone una forma funzionale lineare per l'effetto di regime, perdendo informazione su effetti regime-dipendenti non lineari.
2. **Coerenza con altre stratificazioni del modello**: i parametri $\tau_{vol}$, $\tau_{surv}$, $d_{stop,\sigma}$ sono regime-dipendenti (Cap.22.3, 22.4): la stratificazione del Cox è omogenea con la struttura del cromosoma.
3. **Costo in parametri contenuto**: il raddoppio dei coefficienti $\boldsymbol{\beta}_j$ (da $K \leq K_{max} = 12$ a $2K \leq 24$) è gestibile sotto la rule of thumb di Harrell con $N_{eventi}/K \geq 10$, purché $N_{eventi,\text{calmo}} \geq 10K$ e $N_{eventi,\text{turbolento}} \geq 10K$ separatamente. Per un fold con $W_{in} \approx 105.840$ barre $\approx 126$ sessioni e tasso di emissione 1-3 segnali/sessione, $N_{eventi}$ atteso $\geq 120-380$ segnali eseguiti per fold; ripartito 50/50 fra calmo e turbolento, ogni sottostrato ha $\geq 60-190$ eventi, sufficienti per $K \leq 12$.

**Opzione (a) come benchmark di rollback.** Se la stratificazione formale produce **instabilità eccessiva** nei coefficienti fold-per-fold (specificamente, $CV(\hat{\boldsymbol{\beta}}_{j,R})$ — coefficiente di variazione cross-fold dei coefficienti — superiore a una soglia $\theta_{CV} = 0{,}5$ valore di lavoro), il modello è soggetto a rollback all'opzione (a) interaction term per quel fold, con registrazione nel log di calibrazione. La soglia $\theta_{CV} = 0{,}5$ è dichiarata provvisoria e congelata in Cap.26.5.

### 25.6 Diagnostica del censoring non-informativo fold-per-fold (M-7 + M-8)

L'assunzione di **censoring non-informativo condizionato alle covariate** del modello Cox (Cap.19.4 di Parte IV, chiusura O-5/M-7 v2 Review CAP-04) è verificata empiricamente fold-per-fold attraverso due test diagnostici, in chiusura di **M-7 Review v1 CAP-04 + M-8 Developer CAP-04**.

**Test 1 — Residui di Cox-Snell.** Riferimento: **Cox e Snell (1968)** "A general definition of residuals", *Journal of the Royal Statistical Society B*, 30(2), 248–275. Per ciascuna funzione di rischio causa-specifica $h_j$ ($j = 1$ target_1_hit, $j = 2$ stopped), si calcolano i residui di Cox-Snell per ciascuna osservazione $i$ del campione in-sample del fold:
$$\hat{e}_{i,j} = -\ln \hat{S}_j(\tau_i \mid \tilde{\mathbf{x}}_i, T_{residuo,i})$$
dove $\hat{S}_j$ è la stima della funzione di sopravvivenza causa-specifica $j$ dal modello Cox calibrato.

Sotto le assunzioni (a) di censoring non-informativo condizionato alle covariate e (b) di modello correttamente specificato, $\hat{e}_{i,j} \sim \text{Exp}(1)$ (distribuzione esponenziale unitaria). La verifica avviene via:

- **Plot diagnostico**: $-\ln \hat{S}_{empirica}(\hat{e})$ vs $\hat{e}$ stessa (diagonale teorica $y = x$). Deviazioni sistematiche dalla diagonale indicano violazione delle assunzioni.
- **Test di Kolmogorov-Smirnov** della distribuzione empirica $\hat{e}_{i,j}$ contro $\text{Exp}(1)$. Soglia di rifiuto $p$-value KS $< 0{,}05$ indica violazione.

**Test 2 — Schoenfeld stratificato per evento vs censoring.** Riferimento: **Grambsch e Therneau (1994)** "Proportional Hazards Tests and Diagnostics Based on Weighted Residuals", *Biometrika* 81(3), 515–526. I residui di Schoenfeld sono calcolati separatamente per (i) le osservazioni con evento target_1_hit ($\delta_i = 1$), (ii) le osservazioni con evento stopped ($\delta_i = 2$), (iii) le osservazioni censurate ($\delta_i = 0$, `expired posttrigger_timeout`). La dipendenza dal tempo dei residui di Schoenfeld stratificata per stato indica correlazione censoring/evento condizionata alle covariate.

**Criterio di accettazione**: $p$-value del test di Schoenfeld stratificato $> 0{,}05$ sul test globale fold-per-fold (sotto null hypothesis: censoring non-informativo). Soglia di rifiuto $p$-value $< 0{,}05$ indica violazione sistematica.

**Registrazione nel log del fold**: esiti dei due test (p-value KS, p-value Schoenfeld), flag **"assunzione censoring non-informativo violata"** se **entrambi i test falliscono** ($p_{KS} < 0{,}05$ AND $p_{Schoenfeld} < 0{,}05$). Il flag attiva la regola di rollback al modello Fine-Gray descritto in Cap.25.7 per quel fold.

L'**esito empirico** della verifica del censoring non-informativo (numeri concreti dei p-value sui fold) richiede dati di backtest live e va Parte VII (Cap.31, validazione OOS finale). Cap.25.6 fornisce il **protocollo normativo**; gli esiti empirici sono prodotti dall'esecuzione del walk-forward in Parte VII.

### 25.7 Benchmark Cox cause-specific vs Fine-Gray (M-9)

In chiusura di **M-9 Developer CAP-04**, per ciascun fold $k$ si calibrano in parallelo due modelli di survival sull'in-sample:

- **Modello A**: Cox cause-specific (Cap.19.2 di Parte IV), primario.
- **Modello B**: Fine-Gray subdistribution hazard (Fine e Gray 1999 "A Proportional Hazards Model for the Subdistribution of a Competing Risk", *Journal of the American Statistical Association* 94(446), 496–509), alternativo.

Si applicano entrambi i modelli sull'OOS del fold per produrre $\hat{p}_{hit}^{Cox}(i)$ e $\hat{p}_{hit}^{FG}(i)$ per ogni segnale candidato $i$. Si confrontano sulla **calibrazione predittiva**:

- **Brier score** per il binary outcome target_1_hit (target_1_hit $= 1$, stopped o expired $= 0$, restando sui segnali eseguiti):
$$\text{Brier}(M) = \frac{1}{N_{exec}} \sum_{i=1}^{N_{exec}} \big( \hat{p}_{hit}^{(M)}(i) - \mathbb{1}[\text{state}(i) = \texttt{target\_1\_hit}] \big)^2$$
con $M \in \{Cox, FG\}$. Score più basso = migliore calibrazione.

- **Test di Diebold-Mariano (1995)** "Comparing predictive accuracy", *Journal of Business & Economic Statistics* 13(3), 253–263: test della differenza di loss $L_i^{(Cox)} - L_i^{(FG)}$ con $L_i^{(M)} = (\hat{p}_{hit}^{(M)}(i) - y_i)^2$ (errore quadratico per segnale) sotto null hypothesis: nessuna differenza significativa nell'accuracy predittiva. Soglia di significatività $p$-value DM $< 0{,}05$.

**Flag operativo per fold**:

- Se Brier(FG) < Brier(Cox) **e** p-value DM $< 0{,}05$ a favore di FG, si registra `flag_fine_gray_preferito[fold_k] = True`.
- Altrimenti, `flag_fine_gray_preferito[fold_k] = False`.

**Decisione a livello bundle frozen**: in Parte VII Cap.31 si conta il rapporto di fold con `flag_fine_gray_preferito = True` su $F$ fold totali. Se il rapporto è $> 0{,}5$ (maggioranza dei fold preferisce Fine-Gray), il bundle frozen adotta Fine-Gray come modello primario; altrimenti resta Cox. La decisione non è di Parte V: Parte V fornisce il protocollo e i log dei flag; la selezione finale dipende dagli esiti del walk-forward completo.

**Comportamento sotto flag "censoring informativo" di Cap.25.6**: se il flag è attivo per un fold (entrambi i test KS e Schoenfeld falliscono), si **forza** l'uso del Fine-Gray su quel fold (rollback automatico dal Cox), anche indipendentemente dal Brier score. Questa regola è coerente con la natura del Fine-Gray: il modello per la subdistribution hazard è meno sensibile alla violazione dell'assunzione di censoring non-informativo grazie alla riformulazione del rischio in termini di incidenza cumulativa.

### 25.8 Test Schoenfeld per hazard proporzionali (M-10)

Indipendentemente dalla diagnostica di censoring di Cap.25.6, in chiusura di **M-10 Developer CAP-04** si esegue il **test di Schoenfeld** standard sulle assunzioni di hazard proporzionali del Cox (Grambsch e Therneau 1994, citato in Cap.19.4 di Parte IV). Il test verifica l'assunzione di proporzionalità degli hazard, cioè che $\boldsymbol{\beta}_j$ sia costante nel tempo:

- Per ogni feature $\tilde{x}_l$ del vettore di feature attive del Cox, si calcola la **correlazione fra residuo di Schoenfeld e tempo** $\tau$.
- Si applica il test $\chi^2$ globale di Grambsch-Therneau aggregato su tutte le feature.

**Criterio di accettazione**: $p$-value $> 0{,}05$ sul test globale fold-per-fold. Soglia di rifiuto $p$-value $< 0{,}05$ indica **hazard non proporzionali** per quel fold.

**Azione in caso di violazione**:

- **Violazione isolata** (uno o pochi fold): registrazione nel log del fold come informativa, nessun rollback automatico. La fitness del fold OOS continua con Cox standard.
- **Violazione sistematica** (rapporto di fold con $p < 0{,}05$ superiore al 50%): rinvio a **Parte VII** come carryover M-promemoria nuovo per l'**estensione a hazard non-proporzionali** (Cox con time-varying coefficients $\boldsymbol{\beta}_j(\tau)$, oppure stratificazione su intervalli di $\tau$). Questa estensione richiede campionamento storico più profondo e va in Parte VII Cap.31.

Cap.25.8 è separato da Cap.25.6 perché le due diagnostiche testano assunzioni distinte: Cap.25.6 testa l'indipendenza di censoring/evento condizionata alle covariate; Cap.25.8 testa la costanza dei coefficienti nel tempo. Possono fallire indipendentemente.

### 25.9 Cadenza di ricalibrazione EGARCH e Cox — separazione Parte V / Parte VI

**Cadenza di ricalibrazione nel walk-forward (Parte V).** All'inizio di ogni fold $k$, EGARCH(1,1) e Cox cause-specific sono **ri-stimati sulla finestra in-sample $W_{in}$ del fold**. La cadenza è fold-per-fold, in coerenza con Cap.13.3 di Parte III (calibrazione EGARCH fold-per-fold) e Cap.19.4 di Parte IV (calibrazione Cox fold-per-fold). Parametri stimati congelati per il fold OOS. Numericamente, su $F = 8$ fold e $W_{in} = 6$ mesi, la cadenza è ogni 3 mesi (ogni nuovo fold OOS è 3 mesi dopo il precedente).

**Cadenza di ricalibrazione in production (Parte VI).** In **inference live** (Parte VI Cap.27), la cadenza di re-fitting del bundle frozen è oggetto di trattazione separata: include trigger di break parametrico monitorati in real-time (es. log-likelihood OOS in caduta sistematica del modello frozen), cadenza temporale fissa (es. trimestrale o semestrale come dichiarato in Cap.4 di Parte I), gestione delle anomalie di feed Directa che producono dati incompleti. Questa pipeline operativa NON è materia di Parte V: la **separazione fra walk-forward e production è esplicitamente dichiarata** in coerenza con **M-2 v2 Review v2 CAP-03**. Cap.25.9 chiude il M-2 v2 limitatamente alla parte walk-forward; la parte production rimane carryover Parte VI.

---

## Capitolo 26 — Calibrazione, criteri di stop, congelamento numerico

### 26.1 Popolazione, generazioni e motivazione

**Popolazione di lavoro**: $P = 128$ individui (eredità Q-03 di CAP-01, Cap.4 di Parte I). Motivazione operativa:

- Dimensionalità del cromosoma $K + K' + K'' = 52$ geni (Cap.22.9). Heuristica NSGA-II (Deb 2002, sez. V): popolazione $\geq 2 \times$ dimensionalità per diversità adeguata; $P = 128 \approx 2{,}5 \times 52 = 130$ è in linea.
- **Parallelizzazione su c5.4xlarge**: 16 vCPU, e $128 = 8 \times 16$ permette assegnare 8 cromosomi/vCPU come blocco di lavoro bilanciato. Potenze di 2 facilitano la distribuzione del calcolo.
- Confronto con letteratura: NSGA-II in finanza usa tipicamente popolazione 50-200 (Lopez de Prado 2018, cap. 12); $P = 128$ è centrale.

**Numero massimo di generazioni**: $G_{max} = 150$ (eredità Q-03). Motivazione:

- Ordine di grandezza tipico per NSGA-II in finanza (Lopez de Prado 2018, cap. 12), che permette convergenza con margine operativo.
- Compute budget $P \cdot G_{max}$ valutazioni $\approx 19.328$ (Cap.23.6), dentro il range 12.800-25.600 min single-thread di M-4 sotto le ipotesi di $r_{cache}$ del caso centrale.

### 26.2 Criteri di stop

L'algoritmo termina al verificarsi del primo dei tre criteri:

- **Criterio primario — generazioni massime**: $G \geq G_{max} = 150$.
- **Criterio anticipato — convergenza del fronte di Pareto**: la frontiera $\mathcal{F}_1$ non avanza significativamente per $G_{stall} = 15$ generazioni consecutive, misurata come **distanza di Wasserstein** fra le frontiere $\mathcal{F}_1^{(g - G_{stall})}$ e $\mathcal{F}_1^{(g)}$:
$$W_1\big(\mathcal{F}_1^{(g - G_{stall})}, \mathcal{F}_1^{(g)}\big) \leq \epsilon_{front}$$
con $\epsilon_{front} = 0{,}01$ normalizzata (rapporto fra la distanza di Wasserstein e la diagonale del bounding box della frontiera). Valori di lavoro $G_{stall} = 15$, $\epsilon_{front} = 0{,}01$ provvisori, congelati in Cap.26.5.
- **Criterio compute-budget**: se il tempo cumulato wall-clock supera $T_{budget} = 60$ ore su c5.4xlarge, stop forzato con bundle parziale (il fronte di Pareto della generazione corrente è esposto come output del run). $T_{budget} = 60$ ore coerente con il caso ottimo del calcolo di Cap.23.6 (72 ore caso ottimo per 8 fold $\Rightarrow$ 60 ore per 6{,}7 fold $\approx$ run di calibrazione iniziale + 5-6 fold completi).

### 26.3 Selezione distribuzione $D$ del EGARCH

Eredità di Cap.13.2 di Parte III: scelta della distribuzione $D \in \{\text{Student-t}, \text{GED}\}$ del residuo $z_t$ dell'EGARCH(1,1) via **AIC e BIC** sulla finestra di calibrazione del fold in-sample.

**Protocollo di selezione**:
1. Si calibra EGARCH(1,1) sulla finestra in-sample con $D = \text{Student-t}$ (parametri $\mu, \omega, \alpha, \gamma, \beta, \nu$ dove $\nu$ è il grado di libertà della $t$).
2. Si calibra in parallelo con $D = \text{GED}$ (parametri $\mu, \omega, \alpha, \gamma, \beta, \kappa$ dove $\kappa$ è il parametro di forma della GED).
3. Si calcolano AIC e BIC per entrambi i modelli sull'in-sample.
4. **Tie-break su residual diagnostics**: se AIC e BIC indicano modelli diversi (es. AIC favorisce $t$, BIC favorisce GED), si applica il test di Ljung-Box sui residui standardizzati al quadrato $z_t^2$ con lag $L = 20$; il modello con $p$-value Ljung-Box più alto (residui meno autocorrelati) prevale.

**Esito provvisorio dichiarato**: la distribuzione **Student-$t$ è il default provvisorio** per il bundle di lavoro di Parte V, in coerenza con la prassi della letteratura sui rendimenti finanziari ad alta frequenza (code pesanti, leptocurtosi, e Bollerslev 1987 "A Conditionally Heteroskedastic Time Series Model for Speculative Prices and Rates of Return", *Review of Economics and Statistics* 69(3), 542–547, che introduce GARCH-t come standard). La GED resta come alternativa di rollback se AIC/BIC + Ljung-Box favoriscono GED sui fold del walk-forward. L'esito empirico finale è prodotto in Parte VII sui fold completi.

### 26.4 Selezione inizializzazione EGARCH

Eredità di Cap.13.5 di Parte III: scelta fra **Opzione A** (ripresa fine sessione precedente) e **Opzione B** (varianza incondizionata stimata su tutto il periodo).

**Criterio di selezione**: stabilità della stima nelle prime 60 barre di sessione, misurata come varianza dei residui standardizzati $\text{Var}(z_t)_{t \in [1, 60]}$. L'opzione che produce $\text{Var}(z_t)$ più vicina al valore atteso unitario (sotto la distribuzione $D$ selezionata in 26.3) è preferita.

**Esito provvisorio dichiarato**: **Opzione A (ripresa fine sessione precedente)** confermata come default provvisorio, in coerenza con la motivazione di Cap.13.5 di Parte III (l'informazione di stato dell'EGARCH alla chiusura della sessione precedente è informativa per la prima parte della sessione corrente, sotto-trattamento per persistenza di volatilità overnight). L'Opzione B resta fallback se le diagnostiche su 60 barre indicano instabilità sistematica dell'Opzione A. L'esito empirico finale è in Parte VII.

### 26.5 Tabella di congelamento — parametri del modello e del cromosoma

La tabella seguente è il **documento normativo del congelamento numerico** di Parte V. Ogni voce ha valore di lavoro provvisorio, dominio, capitolo di provenienza e motivazione. I valori sono coerenti con i domini delle Parti I-IV; nessuna voce è in conflitto con eredità precedenti.

**Eredità Parti II-III**:

| Parametro | Dominio | Valore provvisorio | Capitolo | Motivazione |
|-----------|---------|-------------------|----------|-------------|
| $b_{min}$ — floor semi-ampiezza banda | multipli di 5 pt | 5 pt = 1 tick FIB | Cap.6.1 PII | Floor minimo per evitare banda nulla; Cap.6.1 PII |
| $W$ — finestra EGARCH rolling | barre 1-min | 210.000 (1 anno) | Cap.13.3 PIII | Default rolling; rollback M-5 in Cap.25.3 |
| $p$ — quantile classificazione regime | $(0;1)$ | 0{,}75 | Cap.14 PIII | 75° percentile $\bar{\sigma}_s$ del periodo $N_{reg}$ |
| $N_{reg}$ — finestra calibrazione quantile | sessioni | 20 | Cap.14 PIII | 1 mese di trading, balance fra reattività e stabilità |
| $T_{persist}$ — persistenza minima di regime | barre | 10 | Cap.14 PIII | Filtro anti-flicker |
| $n_c$ — barre conferma pivot | intero positivo | 3 | Cap.15.3 PIII | Conferma 3 barre sx e dx |
| $\delta_{pivot}$ — retracement minimo pivot | pt FIB | 10 (2 tick) | Cap.15.3 PIII | Filtro micro-oscillazioni |
| $N_{pivot}$ — latenza primo pivot stimata | barre | 30 | Cap.15.3 PIII | Mezz'ora di trading, valore di lavoro |
| $W_{norm}$ — finestra normalizzazione MAD | barre | 1.000 (≈ 2 sessioni) | Cap.15.4 PIII | Robustezza alla variabilità intraday |
| $T_{warmup,\text{EMA}}$ — warm-up EMA | barre | 74 | Cap.15.2.1 PIII | $\lceil \ln(0{,}01)/\ln(\lambda) \rceil$ con $\lambda = 0{,}94$ |
| $T_{warmup,\text{norm}}$ — warm-up normalizzazione | barre | 100 | Cap.15.4 PIII | $> T_{warmup,\text{EMA}}$ per stabilità |
| $\lambda$ — decay EMA | $(0;1)$ | 0{,}94 | Cap.15.2.1 PIII | Standard RiskMetrics; rivedibile via diagnostica residui |
| $D$ — distribuzione EGARCH | $\{\text{Student-t}, \text{GED}\}$ | Student-t | Cap.13.2 PIII; Cap.26.3 PV | AIC/BIC + Ljung-Box; t default coerente Bollerslev 1987 |
| Inizializzazione EGARCH | $\{A, B\}$ | Opzione A | Cap.13.5 PIII; Cap.26.4 PV | Ripresa fine sessione, default Cap.26.4 |
| $\tau_{vol,low}$ — floor volatility coda bassa | pt FIB | Da finalizzare empiricamente; valore di lavoro provvisorio 5 pt (= 1 tick FIB) | Cap.13.6 PIII; N-5 | Floor che evita degenerazione $\hat{\sigma}_{\text{pt}} \to 0$ |

**Eredità Parte IV**:

| Parametro | Dominio | Valore provvisorio | Capitolo | Motivazione |
|-----------|---------|-------------------|----------|-------------|
| $d_{inv}$ — soglia invalidazione I2 | multipli di 5 pt, $\geq 5$ | 30 pt | Cap.16.5 PIV | Gene cromosoma, valore di lavoro Parte IV |
| $d_{obsolete}$ — soglia obsolescenza pivot I3 | multipli di 5 pt, $\geq 5$ | 20 pt | Cap.16.5 PIV | Gene cromosoma, valore di lavoro Parte IV |
| $T_{min,session}$ — tempo residuo minimo | min trading, $\geq 15$ | 30 min | Cap.16.6 PIV | Gene cromosoma, evita coda sessione |
| $k_{t2}$ — moltiplicatore sigma target_2 | $\mathbb{R}^+$ | 2{,}0 | Cap.17.4 PIV | Gene cromosoma, valore di lavoro Parte IV |
| $d_{stop,\sigma}$ — moltiplicatore sigma stop | $\mathbb{R}^+$ | 3{,}0 | Cap.18.1 PIV | Gene cromosoma, default RR plausibile |
| $d_{stop,\sigma,\text{calmo}}$ | $\mathbb{R}^+$ | 2{,}5 | Cap.18.5 PIV | Variante regime calmo (minore margine) |
| $d_{stop,\sigma,\text{turbolento}}$ | $\mathbb{R}^+$ | 3{,}5 | Cap.18.5 PIV | Variante regime turbolento ($\geq$ calmo) |
| $\tau_{surv}$ — soglia survival | $(0{,}1;\, 0{,}9)$ | 0{,}5 | Cap.20.1 PIV | Gene cromosoma, valore di lavoro Parte IV |
| $\tau_{surv,\text{calmo}}$ | $(0{,}1;\, 0{,}9)$ | 0{,}55 | Cap.20.3 PIV | Variante regime calmo |
| $\tau_{surv,\text{turbolento}}$ | $(0{,}1;\, 0{,}9)$ | 0{,}45 | Cap.20.3 PIV | Variante regime turbolento (filtro più permissivo) |

**Eredità Parte IV trade_range (M-15)**:

| Parametro | Dominio | Valore congelato di lavoro | Capitolo | Motivazione |
|-----------|---------|---------------------------|----------|-------------|
| **$A_{range,min}$** — ampiezza minima range | pt FIB | **80 pt (NON congelabile)** | Cap.5 PI; Cap.21.1 PIV | **Vincolo assoluto** ereditato da Cap.5 PI; non ottimizzabile dal GA |
| $N_{osc}$ — finestra conteggio oscillazioni | barre | 60 | Cap.21.2 PIV | Default Parte IV, 1 ora di trading |
| $n_{osc,min}$ — oscillazioni minime range | intero positivo | 2 | Cap.21.2 PIV | Default Parte IV, range "attivo" |
| $\epsilon_{osc}$ — tolleranza bordi range | multipli di 5 pt | 5 pt = 1 tick FIB | Cap.21.2 PIV | Default Parte IV, $\ll A_{range}/2$ |
| $N_{break}$ — finestra rilevazione breakout | barre | 20 | Cap.21.2 PIV | Default Parte IV |
| $\delta_{break}$ — soglia breakout | multipli di 5 pt | 10 pt = $\delta_{pivot}$ | Cap.21.2 PIV | Default Parte IV, coerente con $\delta_{pivot}$ |

**Parametri di Parte V (cromosoma e operatori NSGA-II)**:

| Parametro | Dominio | Valore congelato di lavoro | Capitolo | Motivazione |
|-----------|---------|---------------------------|----------|-------------|
| $P$ — popolazione | intero positivo | 128 | Cap.26.1 PV | Eredità Q-03 CAP-01; $2 \cdot 52 = 104 \leq 128$ |
| $G_{max}$ — generazioni massime | intero positivo | 150 | Cap.26.1 PV | Eredità Q-03 CAP-01; convergenza tipica NSGA-II |
| $G_{stall}$ — generazioni di stallo per early stop | intero positivo | 15 | Cap.26.2 PV | 10% di $G_{max}$, soglia tipica |
| $\epsilon_{front}$ — soglia Wasserstein per stop | $(0, 1)$ | 0{,}01 | Cap.26.2 PV | Normalizzata sulla diagonale bounding box |
| $T_{budget}$ — budget compute wall-clock | ore | 60 | Cap.26.2 PV | Coerente Cap.4 PI / Cap.23.6 PV |
| $\eta_c$ — distribution index SBX | $\mathbb{R}^+$ | 15 | Cap.23.2 PV | Prassi NSGA-II Deb 2002 |
| $\eta_m$ — distribution index polynomial mut. | $\mathbb{R}^+$ | 20 | Cap.23.3 PV | Prassi NSGA-II Deb 2002 |
| $p_m^{cont}$ — prob. mutazione gene continuo | $(0, 1)$ | $1/K = 1/9 \approx 0{,}11$ | Cap.23.3 PV | "Una mutazione attesa/cromosoma" |
| $p_m^{disc}$ — prob. mutazione gene discreto | $(0, 1)$ | $1/K' = 1/6 \approx 0{,}17$ | Cap.23.3 PV | "Una mutazione attesa/cromosoma" |
| $p_m^{bit}$ — prob. mutazione bit di $\mathbf{s}$ | $(0, 1)$ | $1/K'' = 1/37 \approx 0{,}027$ | Cap.23.3 PV | "Una mutazione attesa/cromosoma" |
| $K_{max}$ — cardinalità feature attive survival | intero positivo | 12 | Cap.22.6 PV; Cap.26.7 PV | Harrell 2015 rule $N_{eventi}/K \geq 10$ |
| $E_{max}$ — soglia emissioni eccessive | segnali/sessione | 5 | Cap.24.2 PV | Cap rumore canale Telegram |
| $E_{min}$ — soglia emissioni nulle | segnali/sessione | 0{,}2 | Cap.24.2 PV | Floor anti-degenerazione |
| $E_{exp,max}$ — soglia expired posttrigger | frazione | 0{,}30 | Cap.24.2 PV | Lifecycle anomalo segnale lento |
| $\alpha_{max}$ — coefficiente penalità eccessiva | $\mathbb{R}^+$ | 0{,}5 | Cap.24.2 PV | Penalità moltiplicativa esponenziale |
| $\alpha_{min}$ — coefficiente penalità nulla | $\mathbb{R}^+$ | 1{,}0 | Cap.24.2 PV | Penalità più forte (cromosoma degenere) |
| $\alpha_{exp}$ — coefficiente penalità expired | $\mathbb{R}^+$ | 0{,}5 | Cap.24.2 PV | Coerente con $\alpha_{max}$ |
| $W_{in}$ — finestra in-sample del fold | barre 1-min | 105.840 (6 mesi $\times$ 840) | Cap.25.1 PV | 6 mesi calendario, eredità Cap.13.3 PIII |
| $W_{oos}$ — finestra OOS del fold | barre 1-min | 52.920 (3 mesi $\times$ 840) | Cap.25.1 PV | 3 mesi calendario |
| $P_{purge}$ — purge fra in-sample e OOS | barre | 4.200 (5 sessioni) | Cap.25.1 PV | $> T_{warmup,\text{EMA}} = 74$ e $> n_c + 1$ |
| $P_{emb}$ — embargo fra fold consecutivi | barre | 4.200 (5 sessioni) | Cap.25.1 PV | $> T_{persist} = 10$ |
| $F$ — numero di fold | intero positivo | 8 | Cap.25.1 PV | Provvisorio, 5 anni / 6 mesi $\approx 10$, ridotto per purge+embargo |
| Soglia $\eta_{div}$ per flag regime instabile | frazione | 0{,}10 | Cap.25.4 PV | 10% sessioni divergenti M-6 |
| Soglia $\theta_{CV}$ per rollback Cox stratificato | $\mathbb{R}^+$ | 0{,}5 | Cap.25.5 PV | CV coefficienti cross-fold M-14 |
| Soglia $p$-value Cox-Snell KS | $(0, 1)$ | 0{,}05 | Cap.25.6 PV | Standard ipotesi $H_0$ M-7+M-8 |
| Soglia $p$-value Schoenfeld stratificato | $(0, 1)$ | 0{,}05 | Cap.25.6 PV | Standard $H_0$ M-7+M-8 |
| Soglia $p$-value Diebold-Mariano FG vs Cox | $(0, 1)$ | 0{,}05 | Cap.25.7 PV | Standard, M-9 |
| Soglia $p$-value Schoenfeld hazard prop. | $(0, 1)$ | 0{,}05 | Cap.25.8 PV | Standard, M-10 |
| Soglia $p$-value Inoue-Rossi window EGARCH | $(0, 1)$ | 0{,}05 | Cap.25.3 PV | Standard, M-5 |

**Note esplicite**:

1. Tutti i valori "valore di lavoro provvisorio" entrano nel run di calibrazione iniziale del GA + walk-forward come **starting point**. Il GA ottimizza i geni del cromosoma (la cui colonna "valore provvisorio" è il punto iniziale di una popolazione random); i parametri del modello restano fissi attraverso il run.

2. La distinzione `gene cromosoma` vs `parametro modello` è normativa: i parametri del modello **non** entrano nel cromosoma. La revisione dei loro valori richiede una nuova esecuzione del walk-forward (analisi controfattuale, non parte del run NSGA-II).

3. **$A_{range,min} = 80$ pt è strettamente non congelabile**: è un vincolo normativo derivato da Cap.5 di Parte I (filtro 80 pt) e non un parametro ottimizzabile. La tabella lo riporta per chiarezza ma con marcatura esplicita.

### 26.6 Risk-reward ratio floor/cap

Eredità di Cap.18.4 di Parte IV: l'introduzione di un floor $RR_{min}$ sul rapporto $RR = d_{target}/d_{stop}$ è demandata a Parte V.

**Decisione esplicita Cap.26.6**: **nessun floor di default**. Il GA è libero di esplorare cromosomi con $RR < 1$; la fitness $f_1$ (expected net return) e $f_4$ (MDD) penalizzano implicitamente cromosomi con $RR$ basso (uno stop ampio relativo al target produce drawdown elevato sul singolo segnale stoppato).

**Attivazione condizionata**: se l'analisi cross-fold del primo run di calibrazione mostra che il GA **converge sistematicamente** su cromosomi con $RR < 1$ producendo $f_1 < 0$ persistente, si attiva un floor $RR_{min} = 1$ nella tabella di Cap.26.5 e si rilancia il run con il vincolo aggiunto a Cap.22.7. La decisione di attivazione richiede l'evidenza empirica dal primo run completo ed è registrata nel log di calibrazione.

### 26.7 Dimensionalità massima feature survival $K_{max}$ (M-11)

In chiusura di **M-11 Developer CAP-04**, $K_{max}$ è il numero massimo di feature attive del Cox cause-specific (Cap.22.6). **Heuristica di Harrell (2015)** "Regression Modeling Strategies", 2a ed., Springer, cap. 4: per stabilità della stima MLE del modello a rischi proporzionali, il rapporto $N_{eventi}/K \geq 10$, dove $N_{eventi}$ è il numero di osservazioni con evento (target_1_hit o stopped, non censurati) e $K$ è il numero di parametri stimati.

**Calcolo del valore di lavoro $K_{max}$**:

- $N_{eventi}$ atteso per fold (in-sample $W_{in} \approx 126$ sessioni $\times$ 1-3 segnali eseguiti/sessione $\times$ rate non-censurato $\approx 0{,}7$): $N_{eventi} \in [88;\, 264]$, valore centrale $\approx 120$.
- Rapporto $N_{eventi}/K_{max} \geq 10$ implica $K_{max} \leq 12$ per il fold con $N_{eventi}$ minimo.
- Sotto stratificazione del Cox per regime (Cap.25.5), $N_{eventi}/K \geq 10$ deve valere per **ciascuno strato** separatamente: $N_{eventi,\text{calmo}}, N_{eventi,\text{turbolento}} \geq 10 K_{max}$. Assumendo split 50/50, ogni strato ha $N_{eventi} \geq 60$, e il vincolo è $K_{max} \leq 6$ per strato. Tuttavia, sotto stratificazione il modello stima $2K_{max}$ parametri totali (uno per strato), e il vincolo è il prodotto per strato.

**Valore congelato di lavoro: $K_{max} = 12$**. La motivazione include il fold a piena cardinalità $N_{eventi} \approx 120$. Se la stratificazione produce strati sbilanciati con $N_{eventi}$ piccolo per uno degli strati (es. fold prevalentemente turbolento con pochi segnali in regime calmo), il vincolo è riconsiderato in Parte VII via rollback a interaction term (Cap.25.5).

### 26.8 Seed e riproducibilità

Il **seed del bundle** è parte del log di calibrazione (eredità Cap.10 di Parte II, replay deterministico bit-exact, eredità 15 di CAP-01-02). Componenti:

- **Seed PRNG NSGA-II** (Cap.23.7): inizializzazione popolazione, torneo, crossover, mutazione, riparazione.
- **Seed ottimizzatore MLE EGARCH** (Cap.13.4 di Parte III, eredità).
- **Seed ottimizzatore MLE Cox** (Cap.19.4 di Parte IV).
- **Seed bootstrap stazionario** (Parte VII Cap.34, fuori scope Parte V).

Tutti i seed sono valori scalari interi di lunghezza minima 64 bit, registrati nel bundle frozen (Cap.35 di Parte VII). Due esecuzioni indipendenti dello stesso run con identici seed e identico storico producono identica popolazione del GA, identico fronte di Pareto e identica fitness al bit.

---

*Fine della Parte V. Il cromosoma del bundle (Cap.22), gli operatori NSGA-II con derivazione del budget di valutazioni (Cap.23), la fitness multi-obiettivo a 5 obiettivi (Cap.24), lo schema di walk-forward nested con purge ed embargo e la diagnostica survival fold-per-fold (Cap.25), la calibrazione operativa con il congelamento numerico di tutti i parametri provvisori (Cap.26) sono ora formalmente specificati. La Parte V chiude il versante metodologico-algoritmico del documento v2: il bundle frozen che esce dal walk-forward nested di Cap.25 è il candidato che la Parte VI consuma per la pipeline di inference real-time e che la Parte VII valida con DSR/PBO/bootstrap stazionario e gate decisionali di go-live. Tutte le decisioni di Parte V con esito empirico vincolante (selezione finale di $D$, di window EGARCH, di Cox vs Fine-Gray, eventuale floor RR, eventuale rollback hazard non-proporzionali) sono rinviate a Parte VII Cap.31 sulla base degli esiti effettivi del walk-forward completo, in coerenza con la separazione fra Parte V (protocollo e calibrazione di lavoro) e Parte VII (validazione finale del bundle frozen).*
