# TASK ATTIVO: CAP-03 — Parte III del documento metodologico v2 (Layer quantitativo single-instrument)

**Assegnato da**: Planner / Orchestratore (rework v4 post-Review v1 CONDITIONAL e decisioni supervisore 2026-05-24)
**Output atteso**: `docs/methodology_v2/CAP_03_parte_III.md` (versione v4)
**Stato**: IN CORSO — rework v4 con 3 BUG REALI + 1 BUG REALE riclassificato (C-5.1) + 3 MIGLIORA PERFORMANCE approvati dal supervisore

## Obiettivo

Scrivere la Parte III del documento metodologico v2: **Layer quantitativo single-instrument**. Questa parte risponde a: come si definiscono i rendimenti sul FIB a barre 1-min, quale modello di volatilita' condizionata alimenta le condizioni di emissione del segnale (Cap.8 di Parte II), come si classifica il regime intraday calmo/turbolento che condiziona il comportamento del GA, e quali feature il GA puo' usare per costruire le zone e calibrare i target senza violare la causalita' temporale.

Non contiene la geometria delle zone (Parte IV), ne' il cromosoma o la fitness (Parte V). Contiene i **blocchi quantitativi elementari** — rendimento, volatilita', regime, feature — che le Parti successive consumano come input. L'impatto diretto sul GA e': (1) il modello EGARCH alimenta la condizione di emissione $\tau_{vol}$ e la condizione di distanza $\tau_{dist}^{\sigma}$ (Cap.8 Parte II); (2) la classificazione del regime determina quali fold del walk-forward sono "calmo" e quali "turbolento", condizionando la metrica di stabilita' cross-regime della fitness; (3) le feature causali sono gli input al modello di survival (Parte IV) e al cromosoma (Parte V).

## Eredita' obbligatoria da CAP-01 e CAP-02

### Da CAP-01 (Q-01..Q-04 chiuse)

1. **Sessione operativa**: 8:00-22:00 CET, finestra unica e continua. Ogni definizione di rendimento, volatilita', regime deve usare questa finestra come perimetro temporale (Q-01).
2. **Storico**: FIB continuo 1-min, Portara/CQG, profondita' minima 5 anni. 1.050.000 osservazioni utili (250 gg x 840 min) — Cap.4 Parte I.
3. **Movimento strutturale**: somma moduli swing fra pivot, ancorato al primo min/max post-apertura dalle 8:00 CET (Q-02). L'algoritmo di pivot detection e' materia di Cap.15 di questa Parte III.
4. **Parametri GA provvisori**: 128/150/B=2000, congelati in Parte V (Q-03).
5. **Tick FIB = 5 punti**: prezzi multipli di 5 in ogni formula e esempio.

### Da CAP-02 (Q-05 chiusa)

6. **Condizione di volatilita' (Cap.8)**: $r_{1m}(t_{emission}) \leq \tau_{vol}(\hat{\sigma}(t_{emission}))$. Il modello EGARCH deve produrre $\hat{\sigma}(t)$ a frequenza 1-min con le proprieta' richieste da questa condizione. La Parte III definisce il modello; la soglia $\tau_{vol}$ e' parametro libero del cromosoma congelato in Parte V.
7. **Condizione di distanza in sigma-units (Cap.8)**: $|\texttt{target\_1} - p_{ref}| / \hat{\sigma}(t_{emission}) \geq \tau_{dist}^{\sigma}$. Il $\hat{\sigma}$ usato e' quello prodotto dall'EGARCH di questa Parte III.
8. **M-1 di CAP-01 / NB-3 di Review v1 CAP-02**: la regola di pivot detection deve produrre il primo candidato di sessione entro $N_{pivot}$ barre dall'apertura. $N_{pivot}$ e' valore provvisorio da congeleare in Parte V con misura empirica sullo storico. La Parte III definisce l'algoritmo; il vincolo quantitativo e' rinviato.
9. **Determinismo bit-exact (Cap.10 Parte II)**: ogni modello (EGARCH, regime, feature) deve essere deterministico e riproducibile dato lo stesso storico e lo stesso seed. Nessuna componente stocastica non seedata.
10. **Regola di fill virtuale**: Cap.7.3 di Parte II rinvia a Parte III la specifica della regola deterministica di fill virtuale per il backtest (N-6 di Review v1 CAP-02). La Parte III deve fissare questa regola nel capitolo pertinente (Cap.12 o Cap.15).
11. **Position lifecycle (Cap.11 Parte II)**: la submacchina del position lifecycle calcola MFE e MAE post-target_1. Le definizioni di rendimento di Cap.12 devono essere coerenti con le grandezze consumate dalla submacchina.

### M-promemoria censiti dalle Review precedenti

| M-ID | Origine | Contenuto | Pertinenza CAP-03 |
|------|---------|-----------|-------------------|
| M-1 | Review v3 CAP-01 | Primo pivot post-apertura: regola di pivot detection e latenza massima $N_{pivot}$ | **SI'** — Cap.15 (feature engineering causale). L'algoritmo di pivot detection va definito qui. Il vincolo $N_{pivot}$ come valore provvisorio va dichiarato, congelamento in Parte V. |
| M-2 | Review v1 CAP-02 | Verifica empirica latenza Telegram ($L_{max}=30$s) | NO — carryover Appendice E |
| M-4 | Review v4 CAP-01 | Tasso di rimpiazzo NSGA-II che giustifica baseline 12.800-25.600 min | NO — carryover Parte V (Cap.23) |
| N-1 | Review v1 CAP-02 | Asimmetria tracking `stopped` vs `target_*_hit` (MFE post-stop) | NO — carryover Parte V (Cap.24 fitness) |
| N-2 | Review v1 CAP-02 | Netto non registrato nel log di chiusura — cambio modello commissioni | NO — carryover Parte VII |
| N-3 | Review v1 CAP-02 | `executable_rate` nomenclatura post-eliminazione guardie | NO — carryover Parte V/VI |
| N-4 | Review v2 CAP-02 | Log chiusura: $\Delta t$ pre-trigger non esplicitato come campo | NO — carryover Parte V |
| N-5 | Review v2 CAP-02 | Condizione volatilita' $\leq$ filtra solo coda alta (no coda bassa) | **SI'** — Cap.13 (EGARCH). Va almeno dichiarato se il modello produce informazione anche sulla coda bassa e se la Parte V puo' introdurre un floor. |
| N-6 | Review v2 CAP-02 | Regola fill virtuale rinviata a Parte III | **SI'** — Cap.12 o Cap.15. Va fissata la regola deterministica. |
| N-7 | Review v3 CAP-02 | CAP-01 riga 75 "guardie di esecuzione" residuo | **CHIUSO** — patch Iterazione 3 di CAP-01 applicata in questo ciclo. |
| N-8 | Review v3 CAP-02 | CAP-01 Cap.5 "target 2 hit rate" semantica cambiata dopo Q-05 | **CHIUSO** — patch Iterazione 3 di CAP-01 applicata in questo ciclo. |
| M-4 | Review v3 CAP-02 | Residuo patch CAP-01 riga 75 | **CHIUSO** — patch Iterazione 3 di CAP-01 applicata in questo ciclo. |

## Capitoli da produrre (~8 pagine totali in italiano formale)

### Capitolo 12 — Definizioni di rendimento e scala temporale (~1.5 pp)

Definire formalmente:
- Rendimento logaritmico 1-min: $r_t = \ln(p_t / p_{t-1})$ dove $p_t$ e' il prezzo di chiusura della barra 1-min $t$.
- Chiarire il trattamento del primo rendimento della sessione ($t=1$ delle 8:00 CET): base di calcolo = close della barra precedente (21:59 del giorno precedente per sessioni consecutive; handling gap overnight/weekend).
- Aggregazione a scale temporali superiori (5-min, 15-min, 60-min) per le feature di Cap.15: metodo additivo dei log-return. Specificare se le barre aggregate sono prodotte da sampling dei close ogni $k$ barre o da OHLC compositi.
- Trattamento del gap di sessione: la prima barra 1-min delle 8:00 puo' contenere un gap rispetto al close delle 22:00 del giorno precedente. Dichiarare come il rendimento della prima barra viene trattato nel modello EGARCH (incluso nella serie? escluso e sostituito? winsorizzato?).
- **Regola deterministica di fill virtuale per il backtest** (carryover N-6 di Review v2 CAP-02): quando il raw touch avviene su una barra 1-min il cui intervallo high-low contiene piu' livelli della entry zone, specificare a quale prezzo il fill virtuale viene assegnato. Regola proposta: fill al livello discreto della zona piu' sfavorevole per l'operatore (bordo superiore per long, bordo inferiore per short — worst-case conservativo). Questa regola e' deterministica e coerente con il vincolo di replay bit-exact di Cap.10. Motivazione: evita di gonfiare le performance in backtest con fill favorevoli non garantiti dall'OHLC.

Vincolo: tutte le definizioni devono rispettare il tick FIB = 5 punti dove applicabile (prezzi strutturali, zone, target).

### Capitolo 13 — Modello di volatilita' condizionata (~2.5 pp)

Specificare il modello EGARCH(1,1) single-instrument sul FIB 1-min:
- Equazione della media: $r_t = \mu + \epsilon_t$, con $\epsilon_t = \sigma_t z_t$, $z_t \sim D(0,1)$.
- Equazione della varianza: $\ln(\sigma_t^2) = \omega + \alpha (|z_{t-1}| - E[|z_{t-1}|]) + \gamma z_{t-1} + \beta \ln(\sigma_{t-1}^2)$.
- Scelta della distribuzione $D$: Student-$t$ o GED. Non fissare la scelta definitiva: dichiarare che la distribuzione e' selezionata in Parte V via AIC/BIC sulla finestra di calibrazione.
- Calibrazione: metodo MLE, finestra di calibrazione rolling o expanding. Specificare che la lunghezza della finestra di calibrazione e' parametro del modello, non del cromosoma (il GA non la ottimizza). Valore di lavoro provvisorio: 1 anno rolling di barre 1-min (~210.000 osservazioni). Congelamento in Parte V.
- Diagnostica obbligatoria dei residui standardizzati $z_t = \epsilon_t / \sigma_t$: test di Ljung-Box su $z_t^2$, QQ-plot, ACF dei quadrati. Criterio di accettazione: p-value Ljung-Box > 0.05 su lag 10 e 20 dei quadrati. Rinvio a Parte V per la procedura di accettazione formale nel walk-forward.
- Output del modello: $\hat{\sigma}_t$ a frequenza 1-min, consumato da Cap.8 Parte II (condizione di volatilita' e condizione di distanza in sigma-units) e da Cap.14 (regime) e Cap.15 (feature).
- Trattamento del gap di sessione nella ricorsione EGARCH: come si inizializza $\sigma_t$ alla prima barra delle 8:00? Due opzioni da dichiarare (ripresa dal valore delle 22:00 vs re-inizializzazione a varianza incondizionata). Scelta definitiva rinviata a Parte V con evidenza empirica.
- **Osservazione N-5** (coda bassa della volatilita'): il modello EGARCH produce $\hat{\sigma}_t$ sia per valori anomalmente alti che anomalmente bassi. Dichiarare esplicitamente che la Parte V puo' introdurre un floor sulla condizione di emissione ($r_{1m} \geq \tau_{vol,low}$) se la misura empirica mostra che barre a range eccessivamente basso precedono sistematicamente eventi avversi. La Parte III non fissa questa soglia ma produce l'informazione necessaria.

### Capitolo 14 — Stato di regime intraday (~2 pp)

Classificazione binaria del regime di mercato nella sessione corrente:
- Due stati: **calmo** e **turbolento**. La classificazione e' deterministica e calcolata in tempo reale (no look-ahead).
- Input: $\hat{\sigma}_t$ dall'EGARCH di Cap.13, eventualmente integrato con volume e/o range delle barre recenti.
- Metodo: soglia derivata da quantili rolling della distribuzione di $\hat{\sigma}_t$ su una finestra storica. Specificare: quale quantile (es. mediana, 75esimo, 90esimo), quale finestra rolling (es. 20 sessioni), e come si gestisce il warm-up all'inizio dello storico.
- **Persistenza minima**: il regime non cambia a ogni barra 1-min; una volta dichiarato (calmo o turbolento), persiste per almeno $T_{persist}$ barre prima di poter transire allo stato opposto. $T_{persist}$ e' parametro del modello (non del cromosoma), valore di lavoro provvisorio da congeleare in Parte V.
- Impatto sul GA: il regime determina (a) quale valore di $\tau_{vol}$ la condizione di emissione di Cap.8 confronta con $r_{1m}$ (la soglia puo' dipendere dal regime via il cromosoma); (b) la suddivisione dei fold del walk-forward in "fold calmo" e "fold turbolento" per la metrica di stabilita' cross-regime della fitness (Parte V, Cap.24); (c) la condizionalita' delle metriche di lifecycle di Cap.5 Parte I ("target hit rate ed executable rate stabili e comparabili fra regime calmo e turbolento").
- Dichiarare esplicitamente che la classificazione non e' una feature del cromosoma ma uno stato del contesto: il cromosoma puo' avere parametri condizionali al regime (es. $\tau_{vol,calmo}$ e $\tau_{vol,turbolento}$), ma la classificazione stessa non e' ottimizzabile dal GA. Questo evita che il GA manipoli la definizione di regime per gonfiare le metriche.

### Capitolo 15 — Feature engineering causale (~2 pp)

Definire il set di feature che il modello consuma come input, con il vincolo fondamentale di causalita' temporale (no look-ahead):
- **Vincolo di causalita'**: ogni feature $x_t$ usata per una decisione al tempo $t$ (emissione, valutazione del cromosoma, classificazione del regime) deve essere calcolata esclusivamente con informazione disponibile a $t-1$ o precedenti. La barra 1-min $t$ contribuisce a $x_t$ solo dopo la sua chiusura. Formalizzare il vincolo come $x_t \in \mathcal{F}_{t-1}$ dove $\mathcal{F}_{t-1}$ e' la filtrazione fino alla chiusura della barra $t-1$.
- **Categorie di feature**:
  - Feature di prezzo: rendimenti a varie scale (1-min, 5-min, 15-min, 60-min — da Cap.12), momentum, mean-reversion.
  - Feature di volume: volume cumulato nella sessione, rapporto volume corrente / volume medio storico per lo stesso minuto della sessione.
  - Feature di volatilita': $\hat{\sigma}_t$ dall'EGARCH, realized volatility su finestre rolling di $k$ barre, rapporto $\hat{\sigma}_t / \bar{\sigma}$ (volatilita' corrente vs media storica).
  - Feature di struttura: distanza dal pivot strutturale piu' recente, numero di pivot identificati nella sessione corrente, posizione del prezzo rispetto alla zona di entry del segnale attivo (se presente).
- **Algoritmo di pivot detection** (carryover M-1): definire la regola operativa per identificare i pivot strutturali intraday. L'algoritmo deve essere deterministico e causale. Specificare: criterio di conferma del pivot (es. retracement minimo di $\delta_{pivot}$ punti dopo l'estremo), latenza di conferma in barre. Dichiarare il vincolo $N_{pivot}$: la regola deve produrre il primo candidato di sessione entro $N_{pivot}$ barre dall'apertura delle 8:00. Valore di lavoro provvisorio $N_{pivot}$ da misurare empiricamente sullo storico e congeleare in Parte V. Il Planner registra che un valore provvisorio ragionevole potrebbe essere $N_{pivot} = 30$ (mezz'ora dall'apertura, proposta della Review v1 CAP-02 NB-3), ma il documento non lo deve fissare come definitivo: dichiara il parametro e rinvia.
- **Normalizzazione robusta**: ogni feature deve essere normalizzata per essere consumabile dal modello di survival (Parte IV) e dal cromosoma (Parte V). Metodo: z-score rolling con mediana e MAD (median absolute deviation) su finestra storica (non media/deviazione standard, per robustezza a outlier). Lunghezza finestra rolling: parametro del modello, valore di lavoro provvisorio da congeleare in Parte V.
- **Dimensionalita' e selezione**: dichiarare il numero massimo di feature candidate. Non selezionare le feature in questa sede: la selezione e' materia del cromosoma (Parte V) o del wrapper di validazione (Parte VII). La Parte III definisce il catalogo delle feature ammissibili, non il sottoinsieme usato.

## Acceptance criteria — tutti devono essere soddisfatti per PASS in Review

- [ ] I 4 capitoli (Cap 12-15) sono presenti, completi, nell'ordine corretto
- [ ] Tutte le 11 eredita' (5 di CAP-01 + 6 di CAP-02) sono citate esplicitamente almeno una volta nei capitoli pertinenti
- [ ] Cap 12: rendimento log 1-min definito formalmente con $r_t = \ln(p_t / p_{t-1})$
- [ ] Cap 12: trattamento esplicito del gap di sessione (prima barra 8:00 vs close 22:00 giorno precedente)
- [ ] Cap 12: aggregazione a scale temporali superiori con metodo dichiarato
- [ ] Cap 12: regola deterministica di fill virtuale per il backtest fissata (carryover N-6), coerente con replay bit-exact di Cap.10 Parte II
- [ ] Cap 13: equazioni EGARCH(1,1) complete (media + varianza log) con notazione
- [ ] Cap 13: distribuzione $D$ dichiarata come scelta aperta (Student-$t$ o GED) con criterio AIC/BIC rinviato a Parte V
- [ ] Cap 13: calibrazione MLE con finestra rolling, lunghezza come parametro del modello (non del cromosoma), valore di lavoro provvisorio dichiarato
- [ ] Cap 13: diagnostica residui standardizzati con Ljung-Box su $z_t^2$, criterio di accettazione esplicito
- [ ] Cap 13: output $\hat{\sigma}_t$ a frequenza 1-min, consumatori dichiarati (Cap.8 Parte II, Cap.14, Cap.15)
- [ ] Cap 13: trattamento inizializzazione $\sigma_t$ alla prima barra della sessione dichiarato come scelta aperta con rinvio a Parte V
- [ ] Cap 13: osservazione N-5 (coda bassa volatilita') trattata esplicitamente — la Parte V puo' introdurre un floor
- [ ] Cap 14: classificazione binaria calmo/turbolento deterministica, no look-ahead
- [ ] Cap 14: metodo basato su quantili rolling di $\hat{\sigma}_t$, finestra e quantile come parametri del modello
- [ ] Cap 14: persistenza minima $T_{persist}$ dichiarata come parametro del modello con valore di lavoro provvisorio
- [ ] Cap 14: impatto sul GA dichiarato (condizionalita' di $\tau_{vol}$, suddivisione fold walk-forward, stabilita' cross-regime)
- [ ] Cap 14: la classificazione del regime non e' feature ottimizzabile dal GA — dichiarato esplicitamente
- [ ] Cap 15: vincolo di causalita' temporale formalizzato ($x_t \in \mathcal{F}_{t-1}$)
- [ ] Cap 15: categorie di feature elencate (prezzo, volume, volatilita', struttura) con almeno un esempio per categoria
- [ ] Cap 15: algoritmo di pivot detection definito (criterio di conferma, latenza, determinismo, causalita') — carryover M-1
- [ ] Cap 15: vincolo $N_{pivot}$ dichiarato come parametro provvisorio con rinvio a Parte V per misura empirica
- [ ] Cap 15: normalizzazione robusta con z-score rolling (mediana + MAD), lunghezza finestra come parametro del modello
- [ ] Cap 15: numero massimo di feature candidate dichiarato; selezione rinviata a Parte V/VII
- [ ] Tick FIB = 5pt rispettato in ogni esempio numerico dove applicabile
- [ ] Determinismo: ogni modello e regola e' deterministico e riproducibile (coerenza Cap.10 Parte II)
- [ ] Nessun parametro fissato definitivamente: tutti i valori numerici sono provvisori e rinviati a Parte V
- [ ] Registro tecnico italiano formale, formule in LaTeX inline e display
- [ ] Il REPORT_CAP_03.md include la sezione "Misura prima/dopo" con impatto sul comportamento del GA

## Out-of-scope — Development NON include queste cose in CAP-03

- **Geometria delle zone di entry, target strutturali, stop strutturali** → Parte IV (Cap.16-18). La Parte III definisce le feature che alimentano la geometria, non la geometria stessa.
- **Modello di survival** → Parte IV (Cap.19). La Parte III produce $\hat{\sigma}_t$ e le feature che il survival consuma.
- **Cromosoma, operatori GA, fitness multi-obiettivo** → Parte V. I parametri del modello EGARCH e della classificazione del regime sono parametri del modello, non del cromosoma.
- **Soglie congelate** ($\tau_{vol}$, $\tau_{dist}^{\sigma}$, $T_{persist}$, lunghezza finestra calibrazione, $N_{pivot}$, etc.) → Parte V. La Parte III dichiara i parametri e i loro domini, non li congela.
- **Walk-forward, DSR, PBO** → Parti V e VII.
- **Selezione delle feature** (quale sottoinsieme usare) → Parte V (cromosoma) o Parte VII (wrapper di validazione).
- **Tasso di rimpiazzo NSGA-II** (M-4) → Parte V.
- **Verifica empirica latenza Telegram** (M-2) → Appendice E.
- **Position lifecycle tracking concreto** (Cap.11 Parte II) → le definizioni di rendimento di Cap.12 devono essere coerenti con la submacchina ma non la definiscono.

## Done when

Il documento risponde senza ambiguita' a queste domande:
1. Come si calcola il rendimento del FIB a barre 1-min, e come si gestisce il gap di sessione nella serie? (Cap 12)
2. Come si stima la volatilita' condizionata $\hat{\sigma}_t$ del FIB a frequenza 1-min, e quali sono le proprieta' diagnostiche richieste? (Cap 13)
3. In che stato di regime (calmo/turbolento) si trova il mercato FIB in un dato minuto della sessione, e come la classificazione impatta il GA? (Cap 14)
4. Quali feature il GA puo' consumare, e come si garantisce che nessuna feature violi la causalita' temporale? (Cap 15)
5. Come si identifica il primo pivot strutturale della sessione, e qual e' la latenza massima accettabile? (Cap 15)
6. A quale prezzo il backtest registra il fill virtuale quando la barra 1-min attraversa piu' livelli della zona? (Cap 12)

## Pipeline attesa

Development v1 → Review v1 audit ostile con classificazione GA → punto di controllo supervisore se CONDITIONAL/FAIL → fix → ... → PASS

---

## Finding di Review v1 da risolvere (rework v4)

Review v1 di CAP-03 (commit `916f3d4`) ha emesso verdetto **CONDITIONAL** con 3 BUG REALI + 4 MIGLIORA PERFORMANCE + 4 NEUTRO. Il supervisore (decisioni 2026-05-24, vedi Q-06..Q-09 in `tasks/QUESTIONS.md`) ha approvato **tutti e 4 i MIGLIORA PERFORMANCE per fix in Developer v4**, riclassificando inoltre C-5.1 da MIGLIORA PERFORMANCE a **BUG REALE**.

### BUG REALI obbligatori (sempre a Developer)

#### **NB-1** — Look-ahead off-by-one nella pivot detection (Cap.15.3)
**Problema**: la condizione di conferma del pivot richiede $\text{high}_{t+n_c}$ che è disponibile solo a $t+n_c$ (chiusura della barra), quindi la feature è in $\mathcal{F}_{t+n_c}$, non $\mathcal{F}_{t+n_c-1}$. Il pivot confermato a $t$ è feature disponibile a $t+n_c+1$, non $t+n_c$.

**Fix v4**: riformulare in Cap.15.3 con timestamp esatto di disponibilità della feature: "il pivot a $t$ è confermato dopo la chiusura di $t+n_c$ ed entra come feature disponibile dalla barra $t + n_c + 1$ in poi". Aggiornare l'esempio numerico coerentemente.

#### **NB-2** — Formula $E[|z|]$ per GED errata (Cap.13.2)
**Problema**: la formula $E[|z|] = 2^{1/\kappa}\,\Gamma(2/\kappa)/\Gamma(1/\kappa)$ è corretta solo per $\kappa = 2$ (Normale). Per $\kappa = 1$ (Laplace) restituisce 2.0 anziché 0.707 atteso. Distorce $\hat{\sigma}$ se il GA seleziona GED.

**Fix v4**: in Cap.13.2 sostituire con la formula corretta che include il fattore di scala $c = [\Gamma(1/\kappa)/(2^{2/\kappa}\Gamma(3/\kappa))]^{1/2}$:
$$E[|z|] = \frac{c \cdot 2^{1/\kappa}\,\Gamma(2/\kappa)}{\Gamma(1/\kappa)}$$
Verificare i casi limite ($\kappa=2$ deve dare $\sqrt{2/\pi} \approx 0{,}7979$; $\kappa=1$ deve dare $1/\sqrt{2} \approx 0{,}7071$).

#### **NB-3** — Unità di misura di $\hat{\sigma}$ non riconciliate con Cap.8 Parte II (Cap.13.1 + Cap.8.2 Parte II)
**Problema**: $\hat{\sigma}$ è in unità di log-return (ordine $10^{-4}$). Il range $r_{1m}$ è in punti FIB (ordine 10-100). La condizione $|target_1 - p_{ref}|/\hat{\sigma}$ produce rapporto non adimensionale. Inoltre il riferimento "Parte III Cap.12" in Cap.8 Parte II è errato (corretto: Cap.13).

**Fix v4**: in Cap.13.1 introdurre **conversione esplicita** della stima di volatilità in punti FIB:
$$\hat{\sigma}_{\text{pt}}(t) = \hat{\sigma}(t) \cdot p_t$$
dove $\hat{\sigma}(t)$ è la stima EGARCH in log-return e $p_t$ è il prezzo corrente (in punti FIB). La condizione di Cap.8 va riformulata usando $\hat{\sigma}_{\text{pt}}(t)$. Aggiornare anche il riferimento errato in Cap.8.2 Parte II da "Cap.12" a "Cap.13" (mini-patch CAP-02).

#### **C-5.1 (riclassificato BUG REALE da MIGLIORA PERF)** — Bug formula EMA (Cap.15.2.1)
**Problema**: la formula $(1-\lambda)\sum_{j=1}^{\infty}\lambda^j r_{t-j}$ ha un fattore $\lambda$ in più rispetto alla forma standard EMA.

**Fix v4** (Q-07): formula corretta
$$x_t^{(\text{ema},\lambda)} = (1-\lambda) \sum_{j=0}^{n_t - 1} \lambda^j r_{t-j}$$
con sommatoria che parte da $j=0$ e considera la somma dei pesi $(1-\lambda^{n_t})$ durante il warm-up.

### MIGLIORA PERFORMANCE approvati dal supervisore

#### **NB-4 / Q-06** — Rolling vs expanding window EGARCH (Cap.13.3): decisione **β-rigorosa**

- **C-4.1**: mantenere rolling $W = 210.000$ in CAP-03 come baseline FIB, **con dichiarazione esplicita di divergenza dal baseline hard-locked**. Giustificazione testuale che cita:
  - (i) inapplicabilità letterale di $T_{roll} = 1500$ del baseline perché calibrato per daily (1500 barre 1-min = 1.8 giorni, insufficienti per stimare EGARCH(1,1) Student-$t$);
  - (ii) **Pesaran-Timmermann (2007)** "Selection of estimation window in the presence of breaks" come riferimento teorico per rolling in presenza di structural breaks parametrici.
- **C-4.2**: cambiare cadenza di ricalibrazione da "all'apertura di ogni sessione" a **"fold-per-fold del walk-forward"**, coerente con Cap. 14.3 del baseline. Aggiornare Cap.13.3 di conseguenza.
- **C-4.3**: aggiungere acceptance criterion per Parte V (M-promemoria sotto): benchmark comparativo rolling vs expanding vs EWMA su FIB con test **Inoue-Rossi (2011)**, e criterio di rollback automatico se rolling $W = 210.000$ non domina almeno una alternativa su metrica OOS congelata (log-likelihood OOS, Brier sulla calibrazione $\sigma^2$, MSE).

#### **NB-5 / Q-07 / C-5.2** — Cross-session reset EMA (Cap.15.2.1)

- **Reset EMA all'apertura di ogni sessione 8:00 CET**. Le prime $T_{warmup,\text{EMA}}$ barre della sessione sono marcate come `unusable` ed escluse dal training del GA.
- Default operativo provvisorio:
  $$T_{warmup,\text{EMA}} \geq \frac{\ln(0{,}01)}{\ln(\lambda)}$$
  che per $\lambda = 0{,}94$ dà $T_{warmup,\text{EMA}} \geq 74$ barre = 74 minuti. Congelato in Parte V.
- **Citazione testuale obbligatoria** nel Cap.15.2.1: **Engle-Sokalska (2012)** "Forecasting intraday volatility in the US equity market", *Journal of Financial Econometrics*, come riferimento metodologico per reset cross-session in equity con sessione netta.

#### **NB-6 / Q-08** — Formalizzazione esplicita pivot detection (Cap.15.3)

Pivot high a $t$ confermato a $t + n_c$ se e solo se valgono **tutte e quattro le condizioni**:

1. $\text{high}_t > \text{high}_{t-i}$ per ogni $i \in [1, n_c]$
2. $\text{high}_t > \text{high}_{t+j}$ per ogni $j \in [1, n_c]$
3. $\min(\text{low}_{t+1}, \ldots, \text{low}_{t+n_c}) \leq \text{high}_t - \delta_{pivot}$
4. La finestra temporale $[t - n_c, t + n_c]$ rientra interamente nella sessione operativa 8:00-22:00 corrente (coerenza con C-5.2: reset cross-session)

Simmetrica per pivot low. Confermare $n_c = 3$ come valore provvisorio congelato in Parte V (era già dichiarato in Parte III v1).

#### **NB-7 / Q-09** — Statistica di sessione di $\hat{\sigma}$ per regime (Cap.14.2)

- **C-7.1**: baseline normativo
  $$\bar{\sigma}_s = \frac{1}{N_s} \sum_{t \in s} \hat{\sigma}_{s,t} \quad \text{con } N_s = 840$$
- **C-7.2**: benchmark di robustezza riportato nei report di sessione: $\text{med}_t(\hat{\sigma}_{s,t})$.
- **C-7.3**: acceptance criterion per Parte V (M-promemoria sotto): se in validation OOS la classificazione di regime cambia significativamente fra media e mediana, va investigato come segnale di sessioni con picchi anomali.
- **Citazione testuale obbligatoria** nel Cap.14.2: **Corsi (2009)** "A Simple Approximate Long-Memory Model of Realized Volatility", *Journal of Financial Econometrics*.

### M-promemoria per Parte V (nuovi, da Q-06 e Q-09)

| M-ID | Origine | Contenuto | Pertinenza CAP-05 (Parte V) |
|------|---------|-----------|------------------------------|
| **M-5** | Q-06 / C-4.3 | Benchmark comparativo rolling vs expanding vs EWMA su FIB con test Inoue-Rossi (2011); criterio di rollback automatico | SÌ — Cap. di window selection del walk-forward (probabilmente Cap.25 secondo indice attuale) |
| **M-6** | Q-09 / C-7.3 | Classificazione di regime in parallelo media e mediana; test di stabilità con soglia da definire | SÌ — Cap. di gestione regimi nel walk-forward (Cap.25 o Cap.26) |

### Vincoli aggiuntivi per il rework v4

- **Standard "no implicit" del baseline hard-locked (Cap. 5.6)**: ogni grado di libertà va chiuso. Niente formule ambigue, niente default impliciti, niente comportamenti border-case non specificati.
- **Citazioni testuali agli articoli** (Pesaran-Timmermann 2007, Engle-Sokalska 2012, Corsi 2009, Inoue-Rossi 2011) entrano **nel testo del capitolo dove pertinenti** (Cap.13.3, Cap.15.2.1, Cap.14.2; Inoue-Rossi è citato come riferimento per il futuro acceptance criterion di Parte V). **NON nelle bibliografie finali**: la gestione bibliografica è pertinenza dell'indice generale.
- **Mini-patch CAP-02 Cap.8.2**: correggere il riferimento "Parte III Cap.12" in "Parte III Cap.13" (segnalato da NB-3). È modifica chirurgica di 1 parola, va eseguita nello stesso commit del rework CAP-03 v4 con nota in REPORT_CAP_02.md "Iterazione 4 — correzione cross-ref Cap.8.2 da Cap.12 a Cap.13".

### Acceptance criteria aggiuntivi per la v4

- [ ] **AC-v4-1**: NB-1 chiuso: nel testo di Cap.15.3 la disponibilità del pivot confermato è esplicita come "feature disponibile a $t + n_c + 1$"
- [ ] **AC-v4-2**: NB-2 chiuso: formula $E[|z|]$ per GED corretta con fattore di scala $c$, verifica numerica $\kappa=2$ e $\kappa=1$
- [ ] **AC-v4-3**: NB-3 chiuso: $\hat{\sigma}_{\text{pt}}(t) = \hat{\sigma}(t) \cdot p_t$ introdotta in Cap.13.1; Cap.8.2 Parte II aggiornato per usare $\hat{\sigma}_{\text{pt}}$
- [ ] **AC-v4-4**: C-5.1 chiuso: formula EMA corretta con $j$ da 0 a $n_t - 1$
- [ ] **AC-v4-5**: Q-06/C-4.1 implementata: divergenza rolling vs expanding dichiarata esplicitamente; citazione Pesaran-Timmermann (2007) testuale
- [ ] **AC-v4-6**: Q-06/C-4.2 implementata: cadenza ricalibrazione "fold-per-fold del walk-forward"
- [ ] **AC-v4-7**: Q-07/C-5.2 implementata: reset EMA cross-session; $T_{warmup,\text{EMA}} \geq \ln(0{,}01)/\ln(\lambda) = 74$ barre per $\lambda=0{,}94$; citazione Engle-Sokalska (2012) testuale
- [ ] **AC-v4-8**: Q-08 implementata: 4 condizioni esplicite per pivot detection, simmetria long/short, condizione di sessione
- [ ] **AC-v4-9**: Q-09 implementata: $\bar{\sigma}_s$ come baseline, mediana come benchmark di robustezza; citazione Corsi (2009) testuale
- [ ] **AC-v4-10**: M-5 e M-6 dichiarati come carryover per Parte V nel REPORT_CAP_03 e in QUESTIONS.md
- [ ] **AC-v4-11**: REPORT_CAP_03.md include sezione "Iterazione 4 — risposta ai finding di Review v1 + decisioni supervisore Q-06..Q-09"
- [ ] **AC-v4-12**: REPORT_CAP_02.md include sezione "Iterazione 4 — mini-patch Cap.8.2 cross-ref Cap.13"
- [ ] **AC-v4-13**: tutti i 29 AC originali restano soddisfatti dopo le modifiche
- [ ] **AC-v4-14**: niente bibliografia generale aggiunta al documento (le citazioni Pesaran-Timmermann, Engle-Sokalska, Corsi, Inoue-Rossi sono inline nel testo dei capitoli, non in bibliografia finale)

### Pipeline rework v4

Development v4 (chiusura 3 BUG + 1 BUG riclassificato + 3 MIGLIORA PERF + mini-patch Cap.8.2) → Review v2 di CAP-03 → ... → PASS.

---

## Finding di Review v2 da risolvere (rework v5)

Review v2 di CAP-03 (commit `6d959c6`) ha emesso verdetto **CONDITIONAL** con 1 BUG REALE + 2 MIGLIORA PERFORMANCE + 2 NEUTRO + 2 PROMEMORIA. **Decisione supervisore 2026-05-24**: B-1 obbligatorio + entrambi i NB-1 v2 e NB-2 v2 approvati per Developer. NEUTRO e PROMEMORIA non vanno a Developer (carryover legittimi).

Stato dei finding di Review v1 (verificato in Review v2): 8/9 chiusi correttamente. La regressione B-1 è introdotta dal fix C-5.1, non un finding ricorrente.

### BUG REALE obbligatorio

#### **B-1 v2** — Regressione look-ahead nel fix EMA (Cap.15.2.1, riga 271)

**Problema**: la formula v4 $x_t^{(\text{ema},\lambda)} = (1-\lambda)\sum_{j=0}^{n_t-1}\lambda^j r_{t-j}$ a $j=0$ usa $r_t = \ln(p_t / p_{t-1})$, che richiede $p_t$ (close della barra $t$). Ma $p_t$ appartiene a $\mathcal{F}_t$, non $\mathcal{F}_{t-1}$. Il testo di Cap.15.2.1 (riga 273) afferma "$r_t \in \mathcal{F}_{t-1}$" che è **falso** per la definizione di rendimento di Cap.12.1. Le altre feature di prezzo (rendimento $x_t^{(r,1)} = r_{t-1}$, cumulato $\sum_{j=1}^{k} r_{t-j}$, momentum) partono correttamente da $r_{t-1}$, mai da $r_t$.

**Impatto GA**: look-ahead di 1 barra sistematico nella EMA. Il backtest vedrebbe il futuro, il forward run no → ranking dei cromosomi distorto.

**Fix v5**: sostituire l'indice della sommatoria da $r_{t-j}$ a $r_{t-1-j}$ (oppure equivalentemente $\sum_{j=1}^{n_t}\lambda^{j-1} r_{t-j}$). Pesi invariati (la somma resta $(1-\lambda)\sum\lambda^j$ con $\lambda < 1$); cambia solo l'indice del rendimento più recente usato, che diventa $r_{t-1}$ (causale). Aggiornare la frase a riga 273 in modo da affermare correttamente che $r_{t-1} \in \mathcal{F}_{t-1}$. Verificare che il warm-up $T_{warmup,\text{EMA}} = 74$ resti coerente.

### MIGLIORA PERFORMANCE approvati dal supervisore

#### **NB-1 v2** — Feature distanza pivot: denominatore in unità sbagliate (Cap.15.2.4, riga 306)

**Problema**: $x_t^{(piv)} = (p_{t-1} - p_{pivot}) / \hat{\sigma}_{t-1}$ è dichiarata in "sigma-units". Ma il numeratore è in punti FIB (ordine $10$-$100$), mentre $\hat{\sigma}_{t-1}$ è in log-return (ordine $10^{-4}$). Il rapporto è di ordine $10^5$, non adimensionale.

**Impatto GA funzionale**: trascurabile (lo z-score con mediana e MAD di Cap.15.4 corregge la scala dell'output). Impatto semantico: la definizione formale è incoerente con quella di Cap.13.1 ($\hat{\sigma}$ vs $\hat{\sigma}_{\text{pt}}$).

**Fix v5**: sostituire $\hat{\sigma}_{t-1}$ con $\hat{\sigma}_{\text{pt}, t-1}$ in Cap.15.2.4 riga 306 (coerente con NB-3 chiuso in v4 che ha introdotto $\hat{\sigma}_{\text{pt}}$).

#### **NB-2 v2** — Residuo mini-patch CAP-02: formula condizione volatilità Cap.8.2 (riga 189)

**Problema**: il testo di Cap.8.2 di CAP-02 (post mini-patch v4) usa $\hat{\sigma}_{\text{pt}}$ correttamente nella condizione di distanza (riga 201), ma la formula della condizione di volatilità a riga 189 ancora dichiara $\tau_{vol}(\hat{\sigma})$ invece di $\tau_{vol}(\hat{\sigma}_{\text{pt}})$. Stessa incoerenza in Cap.10.2 riga 298 (log della condizione).

**Impatto GA funzionale**: nullo ($\tau_{vol}$ è funzione parametrica, il GA la adatta). Impatto semantico: incoerenza testuale fra Cap.8.2 (formula volatilità $\hat{\sigma}$) e Cap.8.2 (formula distanza $\hat{\sigma}_{\text{pt}}$) e con CAP-03 Cap.13.1.

**Fix v5**: sostituire $\tau_{vol}(\hat{\sigma}(t_{emission}))$ con $\tau_{vol}(\hat{\sigma}_{\text{pt}}(t_{emission}))$ in CAP-02 Cap.8.2 riga 189 e nelle righe coerenti di Cap.10.2.

### Carryover (NON a Developer)

- **N-1** (NEUTRO): ambiguità $Q_p$ calcolato su statistiche di sessione o di barra (Cap.14.2). Carryover Parte V.
- **N-2** (NEUTRO): $\hat{\sigma}_{\text{pt}}$ definito con $p_t$ invece di $p_{t-1}$ — differenza numerica $< 0{,}02\%$ trascurabile. Carryover documentazione interna.
- **M-1** (PROMEMORIA): pivot all'inizio e alla fine della sessione non confermabili (conseguenza condizione 4 di Q-08, finestra $[t-n_c, t+n_c]$ in sessione). È **design corretto** ma va segnalato nel report. Carryover Parte VI.
- **M-2** (PROMEMORIA): cadenza ricalibrazione EGARCH in production non specificata (la cadenza "fold-per-fold" di C-4.2 è per backtest/walk-forward; in production manca). Carryover Parte V/VI.

### Acceptance criteria aggiuntivi per la v5

- [ ] **AC-v5-1**: B-1 v2 chiuso: formula EMA con $r_{t-1-j}$ o equivalentemente sommatoria $\sum_{j=1}^{n_t}\lambda^{j-1} r_{t-j}$; riga 273 di Cap.15.2.1 afferma correttamente $r_{t-1} \in \mathcal{F}_{t-1}$
- [ ] **AC-v5-2**: NB-1 v2 chiuso: Cap.15.2.4 riga 306 usa $\hat{\sigma}_{\text{pt}, t-1}$ al denominatore (non più $\hat{\sigma}_{t-1}$)
- [ ] **AC-v5-3**: NB-2 v2 chiuso: CAP-02 Cap.8.2 riga 189 (formula condizione volatilità) usa $\hat{\sigma}_{\text{pt}}$; coerenza propagata in Cap.10.2 dove pertinente
- [ ] **AC-v5-4**: 14 AC v4 + 29 AC originali restano soddisfatti (verifica esplicita, non implicita)
- [ ] **AC-v5-5**: REPORT_CAP_03.md aggiornato con sezione "Iterazione 5 — chiusura B-1 + NB-1/NB-2 di Review v2" con misura prima/dopo
- [ ] **AC-v5-6**: REPORT_CAP_02.md aggiornato con sezione "Iterazione 5 — residuo formula condizione volatilità Cap.8.2"
- [ ] **AC-v5-7**: M-1 e M-2 di Review v2 dichiarati come carryover in REPORT_CAP_03 + tracciati in QUESTIONS.md o nel report con destinazione esplicita (Parte V/VI)

### Pipeline rework v5

Development v5 (3 fix chirurgici: 1 indice EMA + 1 simbolo Cap.15.2.4 + 1-2 simboli CAP-02 Cap.8.2/10.2) → Review v3 di CAP-03 → attesa PASS.

---

## Finding di Review EXTRA da risolvere (rework v6)

Review EXTRA post-PASS di CAP-03 (`reviews/REVIEW_CAP_03_extra_review.md`, audit extra-ostile richiesto dal supervisore dopo il PASS di Review v3 al commit `9467a07`) ha emesso verdetto **CONDITIONAL** con 4 finding MIGLIORA PERFORMANCE nuovi, nessun BUG REALE, nessuna regressione dai fix v4/v5. Il supervisore (decisione 2026-05-24) ha approvato **tutti e 4 i finding** per chiusura in un micro-rework v6.

Natura del rework: 4 fix chirurgici di disambiguazione. Nessun refactoring strutturale. Nessuna modifica a CAP-01 o CAP-02. Atteso PASS in 1 sola iterazione.

### MIGLIORA PERFORMANCE approvati dal supervisore (4/4)

#### **E-1** — Cap.14.2 riga 208: disambiguare insieme di calcolo di $Q_p$

**Problema**: il testo a riga 208 dice "$Q_p(\hat{\sigma} \mid \mathcal{W}_t)$ e' il quantile $p$ della distribuzione di $\hat{\sigma}$ calcolata sulla finestra rolling $\mathcal{W}_t$ delle $N_{reg}$ sessioni piu' recenti", ma non chiarisce se $Q_p$ e' calcolato sulle $N_{reg}$ medie di sessione $\bar{\sigma}_s$ (un valore per sessione) o sulle $N_{reg} \times 840$ barre singole. Due implementazioni divergenti: la prima produce $N_{reg}$ valori e un quantile liscio; la seconda produce $N_{reg} \times 840$ valori con variabilita' intra-sessione. La classificazione di regime e la suddivisione dei fold calmo/turbolento nel walk-forward cambiano fra le due implementazioni.

**Fix v6**: aggiungere a Cap.14.2 una frase esplicita: "$Q_p$ e' il quantile della distribuzione delle medie di sessione $\bar{\sigma}_s$ delle $N_{reg}$ sessioni piu' recenti -- quindi $N_{reg}$ valori, uno per sessione, coerenti con la definizione di statistica di sessione di Cap.14.2 (baseline C-7.1, Q-09) e con la citazione Corsi (2009) HAR-RV che aggrega per intervalli temporali, non per singola osservazione".

**Nota**: questo finding e' l'upgrade del carryover N-1 di Review v2 (allora classificato NEUTRO, ora riclassificato MIGLIORA PERFORMANCE per implementazioni divergenti).

#### **E-2** — Cap.15.2.1 riga 268: eliminare la feature momentum (identita' banale)

**Problema**: $x_t^{(\text{mom},k)} = \text{sign}(\sum r_{t-j}) \cdot |\sum r_{t-j}|$ e' identicamente uguale a $\sum r_{t-j} = x_t^{(r,k)}$ (replica esatta del rendimento cumulato). Spreca 3 slot su 40 e introduce collinearita' perfetta nel modello survival.

**Fix v6**: eliminare il bullet a riga 268 dal catalogo. Aggiornare il conteggio massimo di feature candidate a Cap.15.2 (era 40, diventa 37) oppure mantenere 40 dichiarando che la riduzione e' disponibile per future feature da definire in Parte V.

#### **E-3** — Cap.15.2.2 riga 290: disambiguare indice di sommatoria del volume cumulato

**Problema**: $x_t^{(v,\text{cum})} = \sum_{j=1}^{t-1} v_{1m}(j)$ usa $j=1$ ambiguo (storico globale vs prima barra di sessione). Implementazione letterale produce feature inutilizzabile (cresce all'infinito attraverso sessioni).

**Fix v6**: sostituire con $x_t^{(v,\text{cum})} = \sum_{j=t_{\text{open}(s_t)}}^{t-1} v_{1m}(j)$, dove $t_{\text{open}(s_t)}$ e' l'indice globale della prima barra della sessione corrente $s_t$. Aggiungere mezza riga di definizione del simbolo $t_{\text{open}}$.

#### **E-4** — Cap.15.4: normalizzazione MAD attraversa confine di sessione per feature con reset

**Problema**: $W_{norm} = 1000$ barre $\approx$ 1.19 sessioni. Per feature con reset di sessione (EMA, volume cumulato dopo fix E-3) la finestra contiene barre della sessione precedente con valori "alti" e barre della sessione corrente con valori "appena resettati" -- mediana e MAD distorte -- z-score anomalo nelle prime ~50-100 barre di ogni sessione.

**Fix v6**: aggiungere a Cap.15.4 una frase: "Per le feature con reset di sessione (EMA dei rendimenti, volume cumulato di sessione), la finestra di normalizzazione e' limitata alla sessione corrente: $\text{Med}$ e $\text{MAD}$ sono calcolate su $\{x_{t_{\text{open}}}, \ldots, x_{t-1}\}$. Conseguenza: per queste feature la normalizzazione e' effettivamente attiva solo a partire da $T_{warmup,\text{norm}}$ barre dall'apertura (valore di lavoro provvisorio $T_{warmup,\text{norm}} = 100$ barre, congelato in Parte V); le barre precedenti sono marcate `unusable` per coerenza con il warm-up EMA". Aggiungere $T_{warmup,\text{norm}}$ all'elenco dei parametri provvisori in chiusura del Cap.15.4 e nel paragrafo finale del documento.

### Acceptance criteria aggiuntivi per la v6

- [ ] **AC-v6-1**: E-1 chiuso: testo Cap.14.2 disambigua esplicitamente che $Q_p$ e' calcolato sulle $N_{reg}$ medie di sessione $\bar{\sigma}_s$, non sulle singole barre; coerenza con C-7.1/Q-09 e citazione Corsi (2009)
- [ ] **AC-v6-2**: E-2 chiuso: bullet momentum a riga 268 eliminato dal catalogo; conteggio max feature aggiornato (37) oppure mantenuto a 40 con dichiarazione esplicita che la riduzione e' disponibile per future feature in Parte V
- [ ] **AC-v6-3**: E-3 chiuso: formula Cap.15.2.2 volume cumulato usa $t_{\text{open}(s_t)}$ come estremo inferiore della sommatoria; simbolo $t_{\text{open}}$ definito
- [ ] **AC-v6-4**: E-4 chiuso: Cap.15.4 contiene la frase sulla finestra di normalizzazione limitata alla sessione corrente per feature con reset; $T_{warmup,\text{norm}} = 100$ dichiarato come parametro provvisorio congelato in Parte V; coerenza con warm-up EMA
- [ ] **AC-v6-5**: REPORT_CAP_03.md aggiornato con sezione "Iterazione 6 -- chiusura E-1/E-2/E-3/E-4 di Review EXTRA"
- [ ] **AC-v6-6**: nessuna regressione su AC v4, v5, originali; verifica esplicita nel report
- [ ] **AC-v6-7**: nessuna modifica a CAP-01 o CAP-02 in questo rework (i 4 fix sono tutti interni a CAP-03)

### Pipeline rework v6

Development v6 (4 fix chirurgici: 1 disambiguazione Cap.14.2 + 1 eliminazione feature Cap.15.2.1 + 1 formula Cap.15.2.2 + 1 frase Cap.15.4) --> Review v4 di CAP-03 --> atteso PASS.
