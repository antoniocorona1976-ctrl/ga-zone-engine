# TASK ATTIVO: CAP-03 — Parte III del documento metodologico v2 (Layer quantitativo single-instrument)

**Assegnato da**: Planner
**Output atteso**: `docs/methodology_v2/CAP_03_parte_III.md`
**Stato**: IN ATTESA

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
