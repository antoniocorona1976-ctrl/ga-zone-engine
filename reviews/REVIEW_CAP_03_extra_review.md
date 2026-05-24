# Review EXTRA post-PASS di CAP-03 -- Parte III: Layer quantitativo single-instrument

**Verdetto**: CONDITIONAL

**Commit oggetto della review PASS**: `2bf47ef` (Review v3 ufficiale: commit `9467a07`)
**Data**: 2026-05-24
**Natura**: audit extra-ostile post-PASS, richiesto dal supervisore. **Non sostituisce** la Review v3 PASS. **Non apre rework automatico**. Serve a sondare se i 3 cicli di review hanno mancato qualcosa.

---

## Premessa

Riesame integrale di CAP-03 (367 righe, Cap.12-15) con focus su aree non coperte dalle review v1-v3. I finding gia' chiusi nelle iterazioni precedenti (NB-1 pivot off-by-one, NB-2 formula GED, NB-3 unita' sigma, C-5.1 EMA pesi, B-1 EMA look-ahead, NB-1v2 pivot sigma_pt, NB-2v2 CAP-02 residuo) NON sono ripetuti. I carryover N-1, N-2, M-1, M-2 di Review v2 NON sono ripetuti tali quali (E-1 sotto e' un upgrade di N-1 v2 con motivazione esplicita).

---

## Problemi bloccanti (causano FAIL)

Nessuno.

---

## Problemi non bloccanti (causano CONDITIONAL)

### E-1 -- Incoerenza regime: classificazione operante su barra 1-min ma definita su statistica di sessione (Cap.14.2)

**Posizione**: Cap.14.2, formula a riga 210 vs definizione statistica di sessione a righe 200-204.

**Problema**: la definizione formale del regime a riga 210 classifica la barra corrente confrontando $\hat{\sigma}_t$ (volatilita' della singola barra) con $Q_p(\hat{\sigma} \mid \mathcal{W}_t)$. Ma $Q_p$ e' calcolato sulla distribuzione di $\bar{\sigma}_s$ -- la media di sessione (righe 200-204). Le due grandezze hanno scala diversa: $\hat{\sigma}_t$ ha variabilita' intra-sessione, $Q_p(\bar{\sigma}_s)$ e' liscio (un valore per sessione). Conseguenze: in regime turbolento quasi tutte le barre successive a uno spike saranno classificate turbolente; in regime calmo quasi tutte le barre saranno calme -- granularita' molto bassa. Se l'intenzione e' confrontare barra con statistica di sessione, e' funzionalmente corretto ma il testo non lo chiarisce. Se l'intenzione e' confrontare sessione con sessione, la formula a riga 210 e' sbagliata (dovrebbe usare $\bar{\sigma}_{s_{corrente}}$ a sinistra della disuguaglianza).

Nota: il finding era stato sollevato come N-1 in Review v2 e classificato NEUTRO. Lo riclassifico CONDITIONAL/MIGLIORA PERFORMANCE perche' produce due implementazioni con comportamento del regime strutturalmente diverso (granularita' barra vs sessione), che condiziona la suddivisione dei fold calmo/turbolento nel walk-forward e il ranking dei cromosomi per stabilita' cross-regime.

**Impatto GA**: due implementazioni divergenti della stessa specifica producono classificazioni di regime incompatibili. La suddivisione fold calmo/turbolento nel walk-forward (Cap.14.4 punto 2) cambia. Il ranking dei cromosomi per stabilita' cross-regime ne risente.

**Fix proposto**: chiarire nel testo che $Q_p$ e' calcolato sulle statistiche di sessione $\bar{\sigma}_s$ delle $N_{reg}$ sessioni passate ma il confronto avviene con $\hat{\sigma}_t$ della barra corrente -- intenzionalmente, per granularita' alta. Oppure, se la classificazione e' a livello di sessione, usare $\bar{\sigma}_{s_{corrente}}$ a sinistra della disuguaglianza.

**Classificazione**: MIGLIORA PERFORMANCE.

---

### E-2 -- Momentum logaritmico e' identita' del rendimento cumulato (Cap.15.2.1, riga 268)

**Posizione**: Cap.15.2.1, definizione di momentum logaritmico.

**Problema**: la formula $x_t^{(\text{mom},k)} = \text{sign}\!\left(\sum_{j=1}^{k} r_{t-j}\right) \cdot \left|\sum_{j=1}^{k} r_{t-j}\right|$ e' identicamente uguale a $\sum_{j=1}^{k} r_{t-j}$ per ogni valore reale della somma ($\text{sign}(x) \cdot |x| = x$ per ogni $x \in \mathbb{R}$). Il "momentum logaritmico" e' quindi replica esatta della feature "rendimento cumulato" $x_t^{(r,k)}$ e non porta informazione aggiuntiva. Se incluso nel catalogo delle 40 feature candidate, spreca slot senza aggiungere segnale.

**Impatto GA**: impatto funzionale basso. Il GA con normalizzazione MAD tratta le due feature come identiche. Non distorce il ranking. Spreca 3 slot feature (k = 5, 15, 60) su 40 disponibili, riducendo il potere espressivo del catalogo del 7.5%.

**Fix proposto**: o eliminare la feature "momentum logaritmico" dal catalogo, o ridefinirla come qualcosa di non triviale (es. momentum direzionale pesato per volatilita', o momentum con segno ma scala diversa).

**Classificazione**: MIGLIORA PERFORMANCE.

---

### E-3 -- Volume cumulato: indice di sommatoria ambiguo (Cap.15.2.2, riga 290)

**Posizione**: Cap.15.2.2, definizione $x_t^{(v,\text{cum})}$.

**Problema**: la formula $x_t^{(v,\text{cum})} = \sum_{j=1}^{t-1} v_{1m}(j)$ usa l'indice $j$ da 1 a $t-1$, ma $t$ in questa formula indicizza le barre dall'inizio della sessione corrente o dall'inizio dello storico? Se $t$ e' indice globale, la somma accumula il volume di tutte le sessioni precedenti -- grandezza che cresce senza limite e non ha significato economico. Se $t$ e' indice di sessione (barra 1 = apertura 8:00), la feature e' corretta ma $t$ assume significato diverso dalla convenzione usata ovunque nel documento. Il testo dice "dall'apertura delle 8:00 fino alla barra $t-1$" ma la formula non resetta a zero a ogni sessione.

**Impatto GA**: se implementato letteralmente con $j=1$ globale, la feature e' inutilizzabile (cresce senza limite). Se implementato con reset a sessione, e' corretto ma non formalizzato. Due implementazioni divergenti.

**Fix proposto**: riscrivere come $x_t^{(v,\text{cum})} = \sum_{j=t_{open}}^{t-1} v_{1m}(j)$ dove $t_{open}$ e' l'indice della prima barra della sessione corrente (barra delle 8:01 CET).

**Classificazione**: MIGLIORA PERFORMANCE.

---

### E-4 -- Normalizzazione MAD cross-session: finestra $W_{norm}=1000$ barre attraversa il confine di sessione (Cap.15.4)

**Posizione**: Cap.15.4, riga 360.

**Problema**: la finestra di normalizzazione $W_{norm} = 1000$ barre corrisponde a circa 1.2 sessioni (840 barre per sessione). La finestra $[t - W_{norm}, t-1]$ conterra' barre della sessione corrente piu' barre della sessione precedente, inclusa la prima barra (gap overnight). Per feature con reset a sessione (EMA, volume cumulato), la finestra di normalizzazione attraversa un confine di sessione dove le feature subiscono una discontinuita' strutturale (reset a zero). Questo distorce mediana e MAD: la mediana sara' trascinata verso valori bassi dalla seconda meta' della finestra (che include le prime barre post-reset con valori vicini a zero per il volume cumulato). Il documento non tratta questo caso.

**Impatto GA**: distorsione della normalizzazione per feature con reset di sessione. Lo z-score delle prime barre della sessione sara' sistematicamente anomalo. Impatto attenuato dal warm-up EMA che esclude le prime 74 barre, ma non azzerato per le altre feature con reset.

**Fix proposto**: dichiarare nel testo che per le feature con reset di sessione (EMA, volume cumulato), la finestra di normalizzazione $W_{norm}$ deve usare solo barre della sessione corrente (oppure solo barre complete di sessioni precedenti, escludendo la transizione). Oppure usare $W_{norm}$ in sessioni (non barre) per queste feature.

**Classificazione**: MIGLIORA PERFORMANCE.

---

## Osservazioni minori (non-finding o ritirate dopo verifica)

### E-5 -- Log-verosimiglianza EGARCH (Cap.13.3, riga 132) -- RITIRATO

Sospetta omissione del fattore $-\frac{1}{2}$ nel termine Jacobiano. Dopo verifica: la formula scritta usa $-\ln \sigma_t$, che e' equivalente a $-\frac{1}{2}\ln \sigma_t^2$. Nessun errore.

### E-6 -- Varianza incondizionata Cap.13.5 Opzione B: divergenza per $|\beta| \geq 1$

La varianza incondizionata $\hat{\sigma}^2_{\text{unconditional}} = \exp(\hat{\omega} / (1 - \hat{\beta}))$ diverge per $\hat{\beta} = 1$ e degenera per $\hat{\beta} > 1$. Il documento non menziona vincolo $|\hat{\beta}| < 1$ ne' fallback. **Classificazione**: NEUTRO -- l'Opzione A e' il default; l'Opzione B e' dichiarata aperta con scelta empirica in Parte V; il caso degenere e' raro per EGARCH stabili.

### E-7 -- Esempio numerico pivot Cap.15.3 -- RITIRATO

Sospetta non-multiplo di 5. Verifica: $27.485 = 5 \times 5497$, multiplo. Nessun errore.

---

## Secondo giro ostile -- verifica sistematica

1. **Causalita' rendimento aggregato Cap.12.3 nelle feature Cap.15.2.1**: $\sum r_{t-j}$ con $j \in [1, k]$ -- tutte in $\mathcal{F}_{t-1}$. No look-ahead.
2. **Volume relativo**: $v_{1m}(t-1)$ e' barra chiusa; $\bar{v}_{h,m}$ storico. In $\mathcal{F}_{t-1}$. No look-ahead.
3. **Volatilita' realizzata rolling**: $r_{t-j}^2$ con $j \in [1, k]$. In $\mathcal{F}_{t-1}$. No look-ahead.
4. **Variazione volatilita'**: $\hat{\sigma}_{t-1} - \hat{\sigma}_{t-2}$. In $\mathcal{F}_{t-1}$. No look-ahead.
5. **One-hot regime $R_{t-1}$**: la persistenza richiede $T_{persist}$ barre passate. In $\mathcal{F}_{t-1}$. No look-ahead.
6. **Durata regime $t - t_{R,\text{start}}$**: nessun dato futuro. No look-ahead.
7. **Citazioni inline**: Pesaran-Timmermann (2007) J. Econometrics 137(1); Engle-Sokalska (2012) JFE 10(1); Corsi (2009) JFE 7(2); Inoue-Rossi (2011) come M-promemoria; Zhu-Galbraith (2010) GED. Tutte plausibili. Nessuna falsificata.
8. **Single-instrument N=1**: CAP-03 Cap.14 opera solo su $\hat{\sigma}_t$ del FIB. Nessun residuo DCC/ADCC/BEKK. Rispettato.
9. **Fill virtuale Cap.12.4 vs stop pre-touch Cap.7.1 CAP-02**: fill virtuale al raw touch; stop pre-touch (invalidated) prima del raw touch. Non si sovrappongono.
10. **Parametri congelati vs provvisori**: $W=210000$, $p=0.75$, $N_{reg}=20$, $T_{persist}=10$, $n_c=3$, $\delta_{pivot}=10$, $N_{pivot}=30$, $\lambda=0.94$, $T_{warmup,EMA}=74$, $W_{norm}=1000$, max feature $=40$. Tutti dichiarati provvisori con rinvio a Parte V. Nessuno congelato definitivamente.
11. **Determinismo bit-exact**: ogni formula deterministica. L'unica componente con seed e' l'ottimizzatore MLE (Cap.13.3 riga 144). Coerente con Cap.10 Parte II.
12. **Cross-reference Cap.13.1 verso CAP-02 Cap.8 e Cap.10**: Cap.8.2 righe 189 e 201 usano $\hat{\sigma}_{\text{pt}}$; Cap.10.2 riga 298 idem. Coerenti.
13. **11 eredita' obbligatorie**: tutte verificate presenti (sessione 8-22, storico 5 anni, pivot detection, parametri GA provvisori, tick 5pt, condizione volatilita', condizione distanza, M-1 pivot, determinismo, fill virtuale, position lifecycle). 11/11 OK.

---

## Classificazione per il supervisore

| # | Problema | Classificazione | Default |
|---|----------|-----------------|---------|
| E-1 | Regime: confronto barra vs statistica sessione non disambiguato | MIGLIORA PERFORMANCE | Attesa decisione supervisore (upgrade di N-1 v2 da NEUTRO a MIGLIORA PERF per implementazioni divergenti) |
| E-2 | Momentum = identita' del rendimento cumulato | MIGLIORA PERFORMANCE | Attesa decisione supervisore (spreco 3 slot su 40 feature) |
| E-3 | Volume cumulato: indice ambiguo sessione vs globale | MIGLIORA PERFORMANCE | Attesa decisione supervisore (implementazioni divergenti) |
| E-4 | Normalizzazione MAD cross-session per feature con reset | MIGLIORA PERFORMANCE | Attesa decisione supervisore (distorsione z-score prime barre) |
| E-6 | Varianza incondizionata diverge per $|\beta| \geq 1$ | NEUTRO | NON va a Developer (Opzione A e' default; Opzione B rinviata a Parte V) |

---

## Sintesi

L'audit extra-ostile post-PASS ha identificato **4 finding MIGLIORA PERFORMANCE nuovi** non sollevati nelle review v1-v3. **Nessun BUG REALE**. Nessun look-ahead. Nessuna regressione dai fix v4/v5. Nessuna citazione falsificata. Tutte le 11 eredita' presenti. Tutti i parametri provvisori. Single-instrument N=1 rispettato. Determinismo preservato.

I 4 finding sono tutti nella categoria "due implementatori produrrebbero risultati diversi" o "spreco di risorse nel catalogo feature". Nessuno distorce direttamente il ranking dei cromosomi (la normalizzazione MAD corregge la scala in tutti i casi). Tuttavia, E-1 (regime) e E-3 (volume cumulato) producono implementazioni divergenti su grandezze che influenzano la suddivisione dei fold nel walk-forward e quindi meritano disambiguazione.

**Verdetto**: CONDITIONAL -- 4 finding MIGLIORA PERFORMANCE nuovi, nessun bloccante. Il verdetto PASS di Review v3 rimane valido come chiusura del ciclo formale. Questa review extra serve al supervisore per decidere se aprire un micro-rework di disambiguazione prima di procedere a CAP-04, oppure ignorarli come carryover Parte V/VII.

---

## Decisione supervisore (2026-05-24)

Il supervisore ha approvato **tutti e 4 i finding MIGLIORA PERFORMANCE** (E-1, E-2, E-3, E-4) per chiusura in un micro-rework v6 di CAP-03. E-6 (NEUTRO) resta non a Developer come da default. Pipeline approvata: Planner → ACTIVE_TASK v6 → Developer v6 → Review v4 → atteso PASS.
