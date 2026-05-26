# Parte VII — Validazione OOS, frozen bundle, gate decisionali

La Parte VII chiude il documento metodologico v2 sul versante della validazione finale del bundle candidato e dei gate decisionali per il go-live. La Parte VII risponde, in sei capitoli, a sei domande operative: (i) come si trasforma il fronte di Pareto $\mathcal{F}_1$ prodotto dal walk-forward nested di Parte V in uno specifico bundle candidato promosso a produzione (Cap.31); (ii) come si calcola, si stima e si interpreta il **Deflated Sharpe Ratio** (DSR) di Bailey e Lopez de Prado (2014) come gate primario di significatività della performance al netto del numero di prove condotte (Cap.32); (iii) come si stima la **Probability of Backtest Overfitting** (PBO) via Combinatorially Symmetric Cross-Validation (CSCV) di Bailey-Borwein-Lopez de Prado-Zhu (2017) come gate di fragilità della scelta del bundle (Cap.33); (iv) come si applica il **bootstrap stazionario** di Politis e Romano (1994) con $B = 2.000$ replicazioni per produrre intervalli di confidenza sulle metriche aggregate del bundle e per condurre il compute stress test del walk-forward (Cap.34); (v) come si congela il bundle con hash di riferimento immutabile e quale regola governa la sua sostituzione (Cap.35); (vi) quale checklist deterministica di gate autorizza il go-live operativo (Cap.36).

La Parte VII non contiene la pipeline di inference real-time (Parte VI, Cap.27-30), la specifica del cromosoma e degli operatori NSGA-II (Parte V, Cap.22-26), la geometria delle zone e dei target (Parte IV, Cap.16-21), il modello quantitativo (Parte III, Cap.12-15), il payload e la state machine (Parte II, Cap.6-11), il perimetro operatore (Parte I, Cap.1-5). La Parte VII non contiene alcuna logica di esecuzione ordini (vincolo "solo emissione" di Cap.1 di Parte I, eredità invariante) né alcuna logica di re-training del GA in produzione: la decisione di ritraining è presente in Cap.36 come regola condizionata agli alert di Cap.30 di Parte VI e al periodo trimestrale-semestrale di Cap.4 di Parte I, ma il ritraining stesso re-applica il protocollo Parte V su nuovo storico, non è attività di Parte VII.

I parametri di tuning provvisori introdotti in Parte VII ($\theta_{DSR}, \theta_{PBO}, \theta_{f_5}, \theta_{IQR}, \theta_{t_2}, \epsilon_{f_1}, \theta_{CVaR}, \theta_{MDD}, \theta_{sessions}, S, L_{avg}, \theta_{cost}$) sono tutti dichiarati **non congelati in Parte VII, riconsiderati post-go-live**: la Parte VII non aggiunge una propria tabella di congelamento e non modifica la tabella di Cap.26.5 di Parte V, che resta invariata. La fonte canonica di tutte le metriche di Parte VII è il **log di replay deterministico bit-exact** di Cap.10 di Parte II, calcolato sulla finestra OOS aggregata del walk-forward nested di Parte V; nessuna metrica è calcolata su fill effettivi del broker (vincolo "solo emissione").

---

## Capitolo 31 — Procedura di validazione OOS

### 31.1 Finestra OOS aggregata e fonte canonica delle metriche

Si definisce **finestra OOS aggregata** la concatenazione temporale dei $W_{oos}$ degli $F$ fold del walk-forward nested di Cap.25.1 di Parte V effettivamente completati nel run di training. Con $W_{oos} = 52.920$ barre 1-min per fold ($\approx 3$ mesi calendario di FIB sotto sessione 8:00-22:00 CET, eredità Cap.1 di Parte I, 840 barre/sessione) e $F$ effettivo $\in \{6, 7, 8\}$ atteso (Cap.26.2 di Parte V rework v3: bundle parziale $F \approx 6$ atteso sotto $T_{budget} = 80$h, decisione operativa rinviata a Cap.34.4 sotto), la finestra aggregata totale risulta:

$$W_{oos,agg} = W_{oos} \cdot F = 52.920 \cdot F \quad \text{barre 1-min}$$

con valori espliciti $52.920 \cdot 6 = 317.520$ barre ($\approx 18$ mesi calendario) per $F = 6$ atteso, $52.920 \cdot 7 = 370.440$ barre ($\approx 21$ mesi) per $F = 7$, $52.920 \cdot 8 = 423.360$ barre ($\approx 24$ mesi) per $F = 8$ ideale. La finestra aggregata esclude i blocchi di **purge** $P_{purge} = 4.200$ barre e di **embargo** $P_{emb} = 4.200$ barre fra in-sample e out-of-sample di ciascun fold (Cap.25.1 di Parte V), in coerenza con la prevenzione del leakage di López de Prado (2018, cap. 7).

La **fonte canonica** di tutte le metriche di Parte VII è il **log di replay deterministico bit-exact** di Cap.10 di Parte II, generato durante la valutazione della fitness multi-obiettivo del NSGA-II di Cap.23-24 di Parte V. Il log registra integralmente per ogni segnale del fold OOS aggregato: payload emesso (12 campi della tupla $\mathcal{S}$ di Cap.6.1 di Parte II Iterazione 4), transizioni della state machine (Cap.7 di Parte II), valori dei filtri di emissione di Cap.8 di Parte II e Cap.20 di Parte IV, snapshot $\hat{p}_{hit}$ del modello Cox cause-specific (Cap.19 di Parte IV), rendimento $R_{net}$ per segnale eseguito, sub-machine post-target_1 (Cap.11 di Parte II: $\pi_{t_2|t_1}$, MFE, MAE, $f_{stop|t_1}$). **Nessuna metrica di Parte VII è calcolata su fill effettivi del broker**: la verifica di go-live opera interamente sui log di replay, in coerenza con il vincolo "solo emissione" di Cap.1 di Parte I (eredità invariante).

La **catena end-to-end della pipeline di emissione** in inference live (Cap.27 di Parte VI) è inclusa come componente qualitativa della procedura di validazione OOS: il bundle candidato deve essere caricabile dalla pipeline operativa di Cap.27 di Parte VI (verifica funzionale via feed mock o storico recente, riverificata in Cap.36.1 AC-GO-10), e il vincolo qualitativo di latenza end-to-end ($L_{max} = 30$ s valore di lavoro provvisorio di Cap.9.3 di Parte II) è obiettivo della catena ingest-feature-inference-Telegram. La **verifica numerica empirica** di $L_{max}$ effettivo del canale Telegram resta carryover di Appendice E (M-2 OPEN, Review v1 CAP-02) e non viene risolta in Parte VII; Cap.31.1 ne cita il vincolo qualitativo come componente del gate di go-live (Cap.36.1 AC-GO-10), con rinvio Appendice E per la misura empirica su bot reale.

### 31.2 Selezione del bundle candidato dal fronte di Pareto $\mathcal{F}_1$

Sia $\mathcal{F}_1 = \{\theta^{(1)}, \ldots, \theta^{(|\mathcal{F}_1|)}\}$ il fronte di Pareto prodotto dal NSGA-II di Cap.23.1 di Parte V: contiene tutti i cromosomi non dominati sui $M = 5$ obiettivi $(f_1, f_2, f_3, f_4, f_5)$ di Cap.24.1 di Parte V (eredità Cap.5 di Parte I). La cardinalità tipica di $\mathcal{F}_1$ per problemi a 5 obiettivi con popolazione $P = 128$ è $|\mathcal{F}_1| \in [20, 60]$ (López de Prado 2018, cap. 12), con upper bound teorico $|\mathcal{F}_1| \leq P = 128$.

La selezione del **cromosoma vincente** $\theta^* \in \mathcal{F}_1$ — il bundle candidato promosso a produzione — è **deterministica e lessicografica**, in coerenza con il vincolo di replay bit-exact di Cap.10 di Parte II. La procedura applica in sequenza sei filtri ordinati e un criterio finale di massimizzazione, con tie-break esplicito:

**Filtro 1 — DSR positivo significativo (gate primario).** Selezionare i cromosomi con $DSR(\theta^{(k)}) > \theta_{DSR} = 0{,}95$ (Cap.32 sotto), dove $\theta_{DSR} = 0{,}95$ è valore di lavoro provvisorio non congelato (dominio $(0,1)$, riconsiderato post-go-live). Il filtro 1 elimina cromosomi statisticamente non distinguibili dal benchmark deflazionato.

**Filtro 2 — PBO sotto soglia (gate fragilità).** Fra i cromosomi sopravvissuti al filtro 1, selezionare quelli con $PBO(\theta^{(k)}) < \theta_{PBO} = 0{,}50$ (Cap.33 sotto), dove $\theta_{PBO} = 0{,}50$ è valore di lavoro provvisorio non congelato (dominio $(0,1)$, riconsiderato post-go-live). Il filtro 2 elimina cromosomi la cui scelta dipende fragilmente da quale partizione del dato OOS è stata usata in-sample (Bailey-Borwein-Lopez de Prado-Zhu 2017, sez. 3).

**Filtro 3 — Lifecycle stabile cross-regime.** Fra i cromosomi sopravvissuti al filtro 2, selezionare quelli con $|f_5^{global}(\theta^{(k)})| < \theta_{f_5} = 0{,}30$, dove $f_5^{global}$ è la stabilità cross-regime calcolata sulla finestra OOS aggregata secondo Cap.24.6 di Parte V paragrafo 330 (concatenazione di tutti i segnali OOS dei $F$ fold, separazione per regime calmo/turbolento di Cap.14 di Parte III, calcolo di $f_5$ sull'intera storia OOS unificata). $\theta_{f_5} = 0{,}30$ è valore di lavoro provvisorio non congelato (dominio $(0, +\infty)$, riconsiderato post-go-live). Il filtro 3 elimina cromosomi sbilanciati verso un solo regime.

**Filtro 4 — IQR cross-fold normalizzata su $f_1$.** Fra i cromosomi sopravvissuti al filtro 3, selezionare quelli con $\text{IQR}_{norm}(f_1)(\theta^{(k)}) < \theta_{IQR} = 0{,}40$, dove $\text{IQR}_{norm}$ è la deviazione interquartile cross-fold normalizzata di Cap.24.6 di Parte V paragrafi 332-334 (formula $\text{IQR}_{norm}(f_m) = (Q_3 - Q_1)/|\text{median}_k f_{m,k}|$). $\theta_{IQR} = 0{,}40$ è valore di lavoro provvisorio non congelato (dominio $(0, +\infty)$, riconsiderato post-go-live). Il filtro 4 elimina cromosomi con metrica $f_1$ instabile fra fold.

**Filtro 5 — Probabilità di proseguimento $\pi_{t_2|t_1}$ minima.** Fra i cromosomi sopravvissuti al filtro 4, selezionare quelli con $\pi_{t_2|t_1}^{aggregated}(\theta^{(k)}) > \theta_{t_2} = 0{,}30$, dove $\pi_{t_2|t_1}^{aggregated}$ è la probabilità empirica di proseguimento da `target_1_hit` a `target_2_hit` calcolata sulla submachine post-target_1 di Cap.11 di Parte II e Cap.24.3 di Parte V (numero di segmenti che raggiungono target_2 sul numero di segmenti che hanno raggiunto target_1, aggregato cross-fold). $\theta_{t_2} = 0{,}30$ è valore di lavoro provvisorio non congelato (dominio $(0,1)$, riconsiderato post-go-live). Il filtro 5 elimina cromosomi che producono molti `target_1_hit` ma di scarsa qualità informativa per la submachine.

**Selezione finale per massimizzazione di $f_1^{global}$.** Fra i cromosomi sopravvissuti ai filtri 1-5, selezionare il cromosoma $\theta^*$ con $f_1^{global}(\theta^*) = \text{median}_{k \in \{1,\ldots,F\}} f_1(\theta^*; k)$ massimo, dove la mediana cross-fold è quella di Cap.24.6 di Parte V paragrafo 326.

**Tie-break in tre livelli.** Se due o più cromosomi sopravvissuti hanno $f_1^{global}$ entro tolleranza $\epsilon_{f_1} = 10^{-6}$ pt FIB, applicare ordinamento lessicografico crescente:
1. minimo $\text{IQR}_{norm}(f_1)$;
2. minimo $|f_5^{global}|$;
3. hash deterministico del cromosoma (ordinamento sui geni del cromosoma stesso secondo convenzione canonica di Cap.35.2 sotto).

$\epsilon_{f_1} = 10^{-6}$ pt FIB è valore di lavoro provvisorio non congelato (dominio $(0, 1)$, riconsiderato post-go-live; ordine di grandezza dimensionalmente coerente con la precisione numerica dei rendimenti FIB).

**Caso di fallimento di go-live.** Se nessun cromosoma del fronte $\mathcal{F}_1$ sopravvive ai filtri 1-5, il run è dichiarato **fallito di go-live** e si produce un **report di fallimento** con motivazione esplicita: quale filtro (1, 2, 3, 4 o 5) ha eliminato l'ultimo candidato e su quale soglia. Le raccomandazioni operative post-fallimento sono due e si applicano alla sessione operativa successiva, non a Cap.31:

- **(a) Re-applicazione del protocollo Parte V su nuovo storico**, se la causa è cambio di regime di mercato (es. distribuzione empirica dei rendimenti FIB nel periodo di training significativamente diversa da quella del periodo OOS aggregato);
- **(b) Ritocco delle soglie $\theta_{DSR}, \theta_{PBO}, \theta_{f_5}, \theta_{IQR}, \theta_{t_2}$**, se la causa è soglia troppo stringente in presenza di una distribuzione empirica borderline.

La decisione di ricalibrazione delle soglie è rinviata alla sessione operativa post-fallimento, non a un sotto-capitolo di Cap.31: Cap.31.2 dichiara il caso ma non lo risolve, in coerenza con la separazione fra metodologia (Parte VII) e ricalibrazione empirica (post-go-live).

### 31.3 Chiusura delle tre decisioni condizionali di Parte V

Tre decisioni condizionali del walk-forward nested di Parte V (Cap.25.5-25.8 di Parte V, eredità delle diagnostiche survival fold-per-fold) si chiudono in Parte VII sulla base del rapporto di fold in cui ciascuna condizione si verifica.

**(i) Cox cause-specific vs Fine-Gray sub-distribution** (chiusura di M-9, Cap.25.7 di Parte V). Si definisce il rapporto:

$$r_{FG} = \frac{|\{k \in \{1, \ldots, F\} : \texttt{flag\_fine\_gray\_preferito}[k] = \text{True}\}|}{F}$$

dove $\texttt{flag\_fine\_gray\_preferito}[k]$ è il flag fold-per-fold del log di calibrazione di Cap.25.7 di Parte V (test di Brier score + Diebold-Mariano 1995 su `target_1_hit` come outcome binario). La regola di chiusura è:

- Se $r_{FG} > 0{,}50$ (maggioranza dei fold preferiscono Fine-Gray), il bundle frozen adotta **Fine-Gray sub-distribution** (Fine-Gray 1999) come modello survival primario; il metadato `cox_model_type = "fine_gray"` è registrato nel bundle frozen (Cap.35.1 elemento 6).
- Altrimenti ($r_{FG} \leq 0{,}50$), il bundle frozen adotta **Cox cause-specific** (Cap.25.5 di Parte V default); il metadato `cox_model_type = "cause_specific"` è registrato.

**(ii) Stratificazione formale vs interaction term per regime calmo/turbolento** (chiusura di M-14, Cap.25.5 di Parte V). Si definisce il rapporto:

$$r_{CV} = \frac{|\{k \in \{1, \ldots, F\} : CV(\hat{\boldsymbol{\beta}}_{j,R})_k > \theta_{CV} = 0{,}50\}|}{F}$$

dove $CV(\hat{\boldsymbol{\beta}}_{j,R})_k$ è il coefficient of variation cross-strato (calmo/turbolento) dei coefficienti Cox stratificati nel fold $k$, e $\theta_{CV} = 0{,}50$ è la soglia provvisoria di Cap.25.5 di Parte V. La regola di chiusura è:

- Se $r_{CV} > 0{,}50$ (instabilità sistematica cross-strato), fallback all'opzione (a) **interaction term**: il bundle frozen adotta un singolo modello Cox con termine di interazione regime $\times$ feature, in luogo della stratificazione formale; il metadato `cox_stratification = "interaction_term"` è registrato. Inoltre, la **riconsiderazione di $\theta_{CV} = 0{,}50$** stessa è registrata come carryover esplicito al ciclo successivo (Cap.31.5 sotto).
- Altrimenti ($r_{CV} \leq 0{,}50$), stratificazione formale (Cap.25.5 di Parte V default); metadato `cox_stratification = "formal_strata"` registrato.

**(iii) Estensione a Cox time-varying coefficients (chiusura condizionale di M-10 e M-16).** Si definisce il rapporto:

$$r_{Schoenfeld} = \frac{|\{k \in \{1, \ldots, F\} : p_{Schoenfeld,k} < 0{,}05\}|}{F}$$

dove $p_{Schoenfeld,k}$ è il p-value del test di Schoenfeld $\chi^2$ globale di Grambsch-Therneau (1994) "Proportional hazards tests and diagnostics based on weighted residuals", *Biometrika* 81(3), 515-526, applicato fold-per-fold secondo Cap.25.8 di Parte V. La regola di chiusura **chiude M-16 OPEN-CONDIZIONALE** in Parte VII:

- Se $r_{Schoenfeld} > 0{,}50$ (violazione sistematica dell'assunzione di hazard proporzionali), **M-16 è attivato**: l'estensione a Cox time-varying coefficients $\boldsymbol{\beta}_j(\tau)$ secondo Therneau e Grambsch (2000) "Modeling Survival Data: Extending the Cox Model", Springer, cap. 6, si applica **nel ciclo successivo di training** (re-applicazione del protocollo Parte V su nuovo storico con specifica Cox estesa, non in Parte VII di questo ciclo). Il bundle frozen del ciclo corrente registra il metadato `cox_time_varying_active = True` (Cap.35.1 elemento 6). Carryover esplicito al ciclo successivo: la riapplicazione del protocollo Parte V con specifica Cox time-varying produrrà nuova diagnostica Schoenfeld, e la regola di chiusura sarà riapplicata nel nuovo Cap.31.3.
- Altrimenti ($r_{Schoenfeld} \leq 0{,}50$), **M-16 è CLOSED-CAP-07 senza attivazione**: il bundle frozen registra il metadato `cox_time_varying_active = False`, e il monitoraggio Schoenfeld è preservato nel ciclo successivo (la riapplicazione del protocollo Parte V con specifica Cox cause-specific standard produrrà nuova diagnostica Schoenfeld, e la regola sarà riapplicata).

La decisione di Cap.31.3 sull'estensione time-varying è **registrata nel bundle frozen come metadato** (Cap.35.1 elemento 6), in coerenza con la decisione di scope (b) del Planner per CAP-07: il bundle frozen porta con sé l'informazione sulla scelta condizionale presa nel suo ciclo di produzione, garantendo tracciabilità cross-bundle (Cap.35.4 sotto).

### 31.4 Chiusura M-5 (window EGARCH) e Cap.26.3-26.4 di Parte V ($D$ + inizializzazione)

Tre decisioni residue di Parte V sulla specifica EGARCH si chiudono in Parte VII sulla base del rapporto di fold in cui ciascuna candidata domina.

**Window EGARCH effettiva (chiusura di M-5, Cap.25.3 di Parte V).** Le sette candidate windows del protocollo di rollback Inoue-Rossi 2011 sono: rolling $W = 105.000$, rolling $W = 210.000$ (default), rolling $W = 420.000$, expanding, EWMA con $\lambda \in \{0{,}99; 0{,}995; 0{,}999\}$. Si definisce, per ciascuna candidata $w$, il rapporto di fold in cui $w$ domina secondo il criterio di Inoue-Rossi (test di $p < 0{,}05$ contro l'alternativa di Diebold-Mariano sulla loss MSPE dei residui EGARCH):

$$r_w = \frac{|\{k \in \{1, \ldots, F\} : w \text{ domina nel fold } k\}|}{F}$$

La regola di chiusura è:

- Se $r_{rolling, W=210.000} \geq 0{,}50$ (rolling $W = 210.000$ default domina o pareggia in almeno metà dei fold), il bundle frozen adotta **rolling $W = 210.000$**; metadato `egarch_window = "rolling_210000"` registrato.
- Altrimenti, **rollback** alla candidata $w^*$ con $r_{w^*}$ massimo. Se più candidate hanno $r$ massimo, tie-break crescente sull'ordinamento canonico delle sette candidate (rolling 105.000 < rolling 210.000 < rolling 420.000 < expanding < EWMA $\lambda = 0{,}999$ < EWMA $\lambda = 0{,}995$ < EWMA $\lambda = 0{,}99$). Il metadato `egarch_window` registra la candidata adottata.

**Distribuzione $D$ effettiva (chiusura di Cap.26.3 di Parte V).** Le due candidate sono Student-t (default) e GED. Si definisce il rapporto:

$$r_{Student} = \frac{|\{k \in \{1, \ldots, F\} : \text{Student-t favorito da AIC/BIC + Ljung-Box tie-break nel fold } k\}|}{F}$$

La regola di chiusura è:

- Se $r_{Student} \geq 0{,}50$, il bundle frozen adotta **Student-t**; metadato `egarch_distribution = "student_t"` registrato.
- Altrimenti, GED; metadato `egarch_distribution = "ged"` registrato.

**Opzione di inizializzazione EGARCH effettiva (chiusura di Cap.26.4 di Parte V).** Le due candidate sono Opzione A (ripresa fine sessione, default) e Opzione B (varianza incondizionata). Si definisce il rapporto:

$$r_{A} = \frac{|\{k \in \{1, \ldots, F\} : \text{Opzione A produce } \text{Var}(z_t)_{t \in [1, 60]} \text{ più vicina a 1 nel fold } k\}|}{F}$$

dove la varianza dei residui standardizzati $z_t$ nelle prime 60 barre di ciascuna sessione è il criterio di valutazione di Cap.26.4 di Parte V. La regola di chiusura è:

- Se $r_A \geq 0{,}50$, il bundle frozen adotta **Opzione A** (ripresa fine sessione); metadato `egarch_init_option = "A_resume"` registrato.
- Altrimenti, Opzione B (varianza incondizionata); metadato `egarch_init_option = "B_unconditional"` registrato.

### 31.5 Carryover esplicito di riconsiderazione delle soglie metodologiche

Due soglie metodologiche provvisorie sono **rinviate al ciclo successivo** come carryover esplicito, sulla base della distribuzione empirica osservata nel run corrente.

**Riconsiderazione di $\theta_{CV} = 0{,}50$ di Cap.25.5 di Parte V.** Se la distribuzione cross-fold empirica di $CV(\hat{\boldsymbol{\beta}}_{j,R})$ è sistematicamente concentrata nella regione $[0{,}30; 0{,}70]$ (regione di indeterminazione attorno alla soglia $\theta_{CV} = 0{,}50$ provvisoria), la **revisione formale** di $\theta_{CV}$ basata sulla distribuzione empirica osservata (es. $\theta_{CV} = $ percentile 75% della distribuzione cross-fold) è rinviata al ciclo successivo come direzione metodologica. La decisione **non è attivata in questo Cap.31**: richiede dati empirici prodotti dal run successivo per la calibrazione del nuovo percentile.

**Riconsiderazione di $K_{max}^{strict} = 4$ Harrell-strict di Cap.26.7 di Parte V.** Se il monitoraggio fold-per-fold del rapporto $N_{eventi}^{strato}/K_{max}$ (con $K_{max} = 6$ corrente e $N_{eventi}^{strato}$ nell'accezione "segnali eseguiti" allineata fra Cap.25.5 e Cap.26.7 di Parte V dal rework v3) mostra che $N_{eventi}^{strato}/K_{max} < 10$ in maggioranza dei fold (violazione sistematica del criterio di Harrell 2015 stretto, eredità di Cap.26.7 di Parte V), e/o se la diagnostica fold-per-fold del run corrente segnala instabilità dei coefficienti Cox sotto $K_{max} = 6$, l'attivazione del fallback **Harrell-strict $K_{max}^{strict} = 4$** si applica nel ciclo successivo di training. Il bundle frozen del ciclo corrente registra il metadato `K_max_effective = 6` (valore congelato corrente) con eventuale flag `K_max_strict_recommended = True` se la diagnostica del run corrente raccomanda il fallback.

Entrambe le riconsiderazioni sono carryover esplicito: la decisione metodologica formale è del Planner del ciclo successivo, non di questo Cap.31.5. Il REPORT_CAP_07.md registra le distribuzioni empiriche osservate nel run corrente come input per il Planner successivo.

I cinque parametri di tuning provvisori introdotti in Cap.31 ($\theta_{PBO}, \theta_{f_5}, \theta_{IQR}, \theta_{t_2}, \epsilon_{f_1}$) sono dichiarati **non congelati in Parte VII**, con dominio e default proposto esplicitati sopra, riconsiderati post-go-live. La selezione del bundle dal fronte di Pareto è deterministica e lessicografica, garantendo replay bit-exact (Cap.10 di Parte II). Le citazioni esplicite di questa sezione richiamano Cap.23.1 di Parte V (fronte $\mathcal{F}_1$), Cap.24.1 di Parte V (cinque obiettivi $f_1$-$f_5$), Cap.24.6 di Parte V (mediana cross-fold + $\text{IQR}_{norm}$), Cap.24.7 di Parte V (no DSR/PBO in NSGA-II), Cap.25.3-25.8 di Parte V (decisioni condizionali del walk-forward), Cap.26.3-26.4-26.5-26.7 di Parte V (specifica EGARCH e $K_{max}$), Cap.5 di Parte I (definizione operativa del successo), Cap.10 di Parte II (replay bit-exact), Cap.11 di Parte II (submachine post-target_1), Cap.14 di Parte III (classificazione regime), Cap.19 di Parte IV (modello Cox), Appendice E (M-2 OPEN $L_{max}$ Telegram).

---

## Capitolo 32 — Deflated Sharpe Ratio (DSR)

### 32.1 Definizione formale del DSR

Il **Deflated Sharpe Ratio** è introdotto da Bailey e López de Prado (2014) "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality", *Journal of Portfolio Management* 40(5), 94-107 (cfr. anche López de Prado 2018, "Advances in Financial Machine Learning", Wiley, cap. 12), come gate primario di significatività della performance di una strategia al netto: (i) del numero $N_{trials}$ di prove condotte (correzione bias di selezione), (ii) della lunghezza finita $n$ del campione, (iii) della non-normalità della distribuzione dei rendimenti (correzione per skewness $\gamma_3$ e curtosi $\gamma_4$).

La formula adottata è la formulazione canonica di Bailey-López de Prado 2014:

$$DSR = \Phi\!\left(\frac{(\widehat{SR} - SR^*)\sqrt{n - 1}}{\sqrt{1 - \hat{\gamma}_3 \widehat{SR} + \frac{\hat{\gamma}_4 - 1}{4} \widehat{SR}^2}}\right)$$

dove:
- $\Phi(\cdot)$ è la **CDF normale standard**;
- $\widehat{SR}$ è il **Sharpe Ratio osservato** del bundle candidato sulla finestra OOS aggregata di Cap.31.1 (Cap.32.2 sotto);
- $SR^*$ è lo **Sharpe Ratio benchmark deflazionato** che corregge il bias di selezione (Cap.32.3 sotto);
- $n$ è il numero di osservazioni — qui il **numero di segnali eseguiti aggregati cross-fold** del bundle candidato sulla finestra OOS aggregata;
- $\hat{\gamma}_3, \hat{\gamma}_4$ sono **skewness e curtosi empiriche** della distribuzione di $R_{net}$ (Cap.32.3 sotto).

Lo Sharpe Ratio benchmark deflazionato $SR^*$ ha forma chiusa di Bailey-López de Prado 2014:

$$SR^* = \sqrt{\text{Var}\!\big(\{\widehat{SR}_k\}_{k=1}^{N_{trials}}\big)} \cdot \left[ (1 - \gamma_E) \, \Phi^{-1}\!\big(1 - \tfrac{1}{N_{trials}}\big) + \gamma_E \, \Phi^{-1}\!\big(1 - \tfrac{1}{e \cdot N_{trials}}\big) \right]$$

dove:
- $\gamma_E \approx 0{,}5772$ è la **costante di Eulero-Mascheroni**;
- $e \approx 2{,}71828$ è la **costante di Nepero**;
- $N_{trials} = |\mathcal{F}_1|$ è il **numero di cromosomi candidati testati**, qui pari alla cardinalità del fronte di Pareto prodotto dal NSGA-II di Cap.23.1 di Parte V;
- $\{\widehat{SR}_k\}_{k=1}^{N_{trials}}$ è la **distribuzione empirica degli Sharpe Ratio** dei cromosomi del fronte di Pareto sulla stessa finestra OOS aggregata.

Il DSR è una probabilità sotto $H_0: SR \leq SR^*$ contro $H_1: SR > SR^*$: $DSR$ vicino a 1 segnala che il bundle candidato ha uno Sharpe osservato statisticamente superiore al benchmark deflazionato, $DSR$ vicino a 0 segnala l'opposto. Il bundle candidato passa il gate primario se $DSR > \theta_{DSR}$ (Cap.32.4 sotto). La motivazione del gate è esposta da López de Prado 2018 cap. 12: la deflazione corregge il bias di selezione tipico dei processi GA multi-trial (Cap.24.7 di Parte V dichiara che DSR è applicato come gate post-NSGA-II, non come obiettivo diretto del NSGA-II stesso).

### 32.2 Calcolo del Sharpe Ratio osservato $\widehat{SR}$

Lo Sharpe Ratio osservato del bundle candidato $\theta^* \in \mathcal{F}_1$ è calcolato sui **segnali eseguiti** della finestra OOS aggregata di Cap.31.1:

$$\widehat{SR}(\theta^*) = \frac{\bar{R}_{net}(\theta^*)}{\hat{\sigma}_{R_{net}}(\theta^*)}, \qquad \bar{R}_{net}(\theta^*) = \frac{1}{n} \sum_{i=1}^{n} R_{net,i}, \quad \hat{\sigma}_{R_{net}}(\theta^*) = \sqrt{\frac{1}{n-1} \sum_{i=1}^{n} (R_{net,i} - \bar{R}_{net})^2}$$

dove $n$ è il numero di segnali eseguiti aggregati cross-fold (segnali con $t_{exec}$ esistente, ovvero terminati in `target_1_hit`, `stopped` o `expired` con `posttrigger_timeout`, eredità di Cap.24.1 di Parte V $f_1 = E[R_{net} \mid executed]$). Il rendimento $R_{net,i}$ per il segnale $i$-esimo è il rendimento netto al fill virtuale di chiusura (eredità Cap.10.4 di Parte II per `expired` con `posttrigger_timeout`; eredità Cap.7 di Parte II per `target_1_hit` e `stopped`), già al netto delle commissioni $2 \cdot c = 2$ pt FIB per round-trip (Cap.2 di Parte I, $c = 1$ pt FIB equivalente per operazione).

**Nessuna annualizzazione** del Sharpe è applicata: lo Sharpe è **per-segnale**, coerente con l'unità di misura di $f_1 = E[R_{net} \mid executed]$ in pt FIB/segnale di Cap.24.1 di Parte V. La scelta dell'unità per-segnale evita assunzioni sulla frequenza di emissione annuale, che dipende da $r_{emit}$ (numero di segnali per sessione) e dal numero di sessioni di trading nell'anno (250 giorni $\times$ 14 ore di sessione effettiva $\approx$ 3.500 ore/anno).

Una **conversione a Sharpe annualizzato** è citata come **reporting opzionale** per confronto con benchmark di letteratura:

$$\widehat{SR}_{annual} = \widehat{SR} \cdot \sqrt{n_{segnali/anno}}$$

dove $n_{segnali/anno}$ è il numero atteso di segnali emessi all'anno (es. $n_{segnali/anno} \approx 250 \cdot r_{emit}$ con $r_{emit} \in [E_{min} = 0{,}2; E_{max} = 5]$ segnali/sessione di Cap.24.2 di Parte V, ovvero $n_{segnali/anno} \in [50; 1.250]$). Il gate primario di Cap.32 opera sullo Sharpe **per-segnale**; l'annualizzato è solo informativo.

### 32.3 Stima dei parametri di deflazione

I parametri di deflazione del DSR sono stimati empiricamente sulla finestra OOS aggregata e sulla popolazione del fronte di Pareto.

**Skewness e curtosi della distribuzione di $R_{net}$.** Si stimano via momenti centrali standardizzati di ordine 3 e 4:

$$\hat{\gamma}_3 = \frac{1}{n} \sum_{i=1}^{n} \!\left(\frac{R_{net,i} - \bar{R}_{net}}{\hat{\sigma}_{R_{net}}}\right)^{\!3}, \qquad \hat{\gamma}_4 = \frac{1}{n} \sum_{i=1}^{n} \!\left(\frac{R_{net,i} - \bar{R}_{net}}{\hat{\sigma}_{R_{net}}}\right)^{\!4}$$

dove $\hat{\sigma}_{R_{net}}$ è la deviazione standard empirica di Cap.32.2. La convenzione $\hat{\gamma}_4$ include la curtosi normale (valore $3$ per distribuzione normale); la formulazione di Bailey-López de Prado 2014 prevede il termine $\hat{\gamma}_4 - 1$ a denominatore, coerente con questa convenzione (vedi formula di Cap.32.1).

**Numero di prove $N_{trials}$.** Si fissa $N_{trials} = |\mathcal{F}_1|$, ovvero il numero di cromosomi del fronte di Pareto prodotto dal NSGA-II. La cardinalità $|\mathcal{F}_1|$ è registrata come metadato del bundle frozen (Cap.35.1 elemento 6). La scelta $N_{trials} = |\mathcal{F}_1|$ riflette il numero effettivo di candidati che entrano nel processo di selezione del bundle: cromosomi dominati e scartati dal NSGA-II non contano come trial, in coerenza con la definizione di Bailey-López de Prado 2014 (numero di strategie testate da cui si seleziona quella vincente).

**Varianza degli Sharpe Ratio dei cromosomi del fronte.** Si calcola empiricamente:

$$\text{Var}\!\big(\{\widehat{SR}_k\}_{k=1}^{N_{trials}}\big) = \frac{1}{N_{trials} - 1} \sum_{k=1}^{N_{trials}} \big(\widehat{SR}_k - \overline{\widehat{SR}}\big)^2$$

dove $\widehat{SR}_k$ è lo Sharpe del cromosoma $k$-esimo del fronte, calcolato sulla stessa finestra OOS aggregata di Cap.31.1, e $\overline{\widehat{SR}}$ è la media campionaria degli $\widehat{SR}_k$. Questa varianza misura la **dispersione delle prove**: una varianza elevata implica un benchmark $SR^*$ alto, ovvero una deflazione più severa.

### 32.4 Soglia di accettazione del DSR

Il gate primario di Cap.32 opera con soglia:

$$DSR(\theta^*) > \theta_{DSR} = 0{,}95$$

valore di lavoro provvisorio non congelato (dominio $(0, 1)$, riconsiderato post-go-live). La motivazione di $\theta_{DSR} = 0{,}95$ è il **test a un solo lato al 5% di significatività** contro $H_0: SR(\theta^*) \leq SR^*$ (Bailey-López de Prado 2014, sez. 4): rigettare $H_0$ equivale a $DSR > 1 - \alpha$ con $\alpha = 0{,}05$. Il livello $\alpha = 0{,}05$ è scelta convenzionale della letteratura statistica (Lopez de Prado 2018 cap. 12), accettata in Parte VII come valore di lavoro.

**Riconsiderazione post-go-live.** Se la distribuzione empirica di $DSR$ sui cromosomi del fronte $\mathcal{F}_1$ è sistematicamente concentrata vicino a $0{,}9$ in più cicli di training consecutivi (segnale che il gate è borderline al 5%), la **revisione formale** di $\theta_{DSR}$ è rinviata come carryover post-go-live: possibili scelte sono $\theta_{DSR} = 0{,}99$ (test all'1%, più conservativo, accettabile se il numero di cromosomi nel fronte tende a salire e il bias di selezione cresce) oppure $\theta_{DSR} = 0{,}90$ (test al 10%, più permissivo, accettabile se il bundle passa il gate al 5% ma con buffer ridotto rispetto a varianza di stima del DSR).

**Comportamento ai bordi.** Se $\widehat{SR}(\theta^*) < 0$ (cromosoma con net return atteso negativo, ovvero $\bar{R}_{net} < 0$), il numeratore di $DSR$ è negativo (poiché $SR^* > 0$ sempre per costruzione di $\Phi^{-1}$ in Cap.32.1), e $DSR = \Phi(\text{argomento negativo}) \approx 0$. Il cromosoma è automaticamente scartato dal filtro 1 di Cap.31.2, senza necessità di valutazione esplicita di $DSR$.

### 32.5 Esempio numerico illustrativo

L'esempio è **illustrativo** (non è un risultato empirico del backtest, che sarà disponibile in produzione/ciclo successivo). Si suppongono i seguenti valori sulla finestra OOS aggregata di Cap.31.1:

- $\widehat{SR} = 0{,}15$ per-segnale (Sharpe osservato del bundle candidato);
- $n = 2.000$ segnali eseguiti aggregati cross-fold (eredità Cap.25.5 di Parte V: $N_{eventi} \in [120; 380]$ per fold $\times F \in \{6, 7, 8\}$, ordine di grandezza centrale $\sim 2.000$);
- $\hat{\gamma}_3 = -0{,}30$ (skewness negativa, tipica di stop strutturali su FIB intraday);
- $\hat{\gamma}_4 = 5{,}20$ (curtosi $> 3$, eccesso di code, tipico di rendimenti finanziari ad alta frequenza);
- $N_{trials} = |\mathcal{F}_1| = 20$ cromosomi del fronte;
- $\text{Var}(\{\widehat{SR}_k\}) = 0{,}01$ (deviazione standard cross-cromosoma $\approx 0{,}1$).

**Calcolo di $SR^*$:**
$$\Phi^{-1}\!\big(1 - \tfrac{1}{20}\big) = \Phi^{-1}(0{,}95) \approx 1{,}6449$$
$$\Phi^{-1}\!\big(1 - \tfrac{1}{e \cdot 20}\big) = \Phi^{-1}\!\big(1 - \tfrac{1}{54{,}366}\big) = \Phi^{-1}(0{,}9816) \approx 2{,}0853$$
$$SR^* = \sqrt{0{,}01} \cdot \big[(1 - 0{,}5772) \cdot 1{,}6449 + 0{,}5772 \cdot 2{,}0853\big]$$
$$SR^* = 0{,}10 \cdot \big[0{,}4228 \cdot 1{,}6449 + 0{,}5772 \cdot 2{,}0853\big] = 0{,}10 \cdot [0{,}6953 + 1{,}2036] = 0{,}10 \cdot 1{,}8989 \approx 0{,}1899$$

**Calcolo del numeratore di $DSR$:**
$$\widehat{SR} - SR^* = 0{,}15 - 0{,}1899 = -0{,}0399$$
$$\sqrt{n - 1} = \sqrt{1.999} \approx 44{,}71$$
$$(\widehat{SR} - SR^*) \sqrt{n - 1} = -0{,}0399 \cdot 44{,}71 \approx -1{,}7839$$

**Calcolo del denominatore di $DSR$:**
$$1 - \hat{\gamma}_3 \widehat{SR} + \frac{\hat{\gamma}_4 - 1}{4} \widehat{SR}^2 = 1 - (-0{,}30)(0{,}15) + \frac{5{,}20 - 1}{4}(0{,}15)^2$$
$$= 1 + 0{,}0450 + 1{,}05 \cdot 0{,}0225 = 1 + 0{,}0450 + 0{,}0236 = 1{,}0686$$
$$\sqrt{1{,}0686} \approx 1{,}0337$$

**Calcolo finale di $DSR$:**
$$DSR = \Phi\!\left(\frac{-1{,}7839}{1{,}0337}\right) = \Phi(-1{,}7257) \approx 0{,}042$$

Il bundle candidato dell'esempio illustrativo ha $DSR \approx 0{,}042 \ll \theta_{DSR} = 0{,}95$: **fallisce il gate primario**. L'esempio mostra che con $\widehat{SR}$ osservato ($0{,}15$) inferiore al benchmark deflazionato $SR^*$ ($0{,}1899$), il cromosoma non passa il filtro 1 di Cap.31.2 anche se è nel fronte di Pareto. La distribuzione cross-cromosoma $\text{Var}(\widehat{SR}_k) = 0{,}01$ relativamente alta produce un benchmark $SR^*$ severo: $N_{trials} = 20$ cromosomi che competono richiede uno Sharpe osservato ben sopra $0{,}19$ per superare il gate.

I valori numerici di questo esempio rispettano il tick FIB di 5 pt nei rendimenti per-segnale (i valori di $\widehat{SR}, \hat{\gamma}_3, \hat{\gamma}_4$ sono adimensionali, non livelli di prezzo). L'esempio è dichiarato **illustrativo** e non costituisce risultato empirico del backtest, che richiede l'esecuzione del walk-forward nested completo di Parte V.

I parametri di tuning provvisori introdotti in Cap.32 sono $\theta_{DSR} = 0{,}95$ (unico valore), dichiarato non congelato in Parte VII. Le citazioni esplicite di questa sezione richiamano Bailey-López de Prado 2014, López de Prado 2018 cap. 12, Cap.24.1 di Parte V ($f_1 = E[R_{net} \mid executed]$), Cap.24.7 di Parte V (no DSR/PBO in NSGA-II), Cap.31.1 (fold OOS aggregato), Cap.5 di Parte I (definizione operativa del successo).

---

## Capitolo 33 — Probability of Backtest Overfitting (PBO) via CSCV

### 33.1 Definizione formale del PBO via CSCV

La **Probability of Backtest Overfitting** (PBO) è introdotta da Bailey, Borwein, López de Prado e Zhu (2017) "The Probability of Backtest Overfitting", *Journal of Computational Finance* 20(4), 39-70 (cfr. anche Bailey-Borwein-Lopez de Prado-Zhu 2016 working paper preliminare in *Notices of the American Mathematical Society* 61(5)), come misura della probabilità che il cromosoma vincente in-sample sia overfit, ovvero che in OOS performi sotto la mediana del fronte di Pareto. Il PBO è stimato via **Combinatorially Symmetric Cross-Validation** (CSCV).

La procedura formale CSCV opera in **sei passi**:

**Passo 1 — Partizione della finestra OOS aggregata.** La finestra OOS aggregata di Cap.31.1 è partizionata in $S$ sotto-finestre temporalmente contigue di pari lunghezza, con $S$ pari (vincolo strutturale del CSCV, necessario per la partizione simmetrica). Il valore di lavoro provvisorio di $S$ è funzione di $F$ effettivo: $S = 16$ per $F = 8$ ideale, $S = 12$ per $F = 6$ atteso. Cap.33.2 motiva la scelta sotto.

**Passo 2 — Enumerazione delle combinazioni $\binom{S}{S/2}$.** Tutte le combinazioni di $S/2$ sotto-finestre fra le $S$ disponibili sono considerate come "in-sample CSCV"; le rimanenti $S/2$ formano l'OOS CSCV complementare. Il numero totale di combinazioni è $\binom{S}{S/2}$: per $S = 16$, $\binom{16}{8} = 12.870$; per $S = 12$, $\binom{12}{6} = 924$.

**Passo 3 — Calcolo del rank Sharpe in-sample.** Per ciascuna combinazione $j \in \{1, \ldots, \binom{S}{S/2}\}$ e per ciascun cromosoma $c \in \mathcal{F}_1$ del fronte di Pareto, si calcola lo Sharpe Ratio sull'in-sample CSCV della combinazione $j$:

$$\widehat{SR}^{IS}_{c, j} = \frac{\bar{R}_{net}^{IS}_{c, j}}{\hat{\sigma}^{IS}_{R_{net}, c, j}}$$

dove la media e la deviazione standard sono calcolate sui segnali eseguiti del cromosoma $c$ ristretti alle sotto-finestre dell'in-sample CSCV della combinazione $j$. I cromosomi sono ordinati per $\widehat{SR}^{IS}_{c, j}$ decrescente; il cromosoma con rank 1 è il **vincente in-sample** della combinazione $j$, denotato $c^*_j$.

**Passo 4 — Calcolo del rank OOS del vincente in-sample.** Per il cromosoma $c^*_j$ vincente in-sample della combinazione $j$, si calcola lo Sharpe sull'OOS CSCV complementare:

$$\widehat{SR}^{OOS}_{c^*_j, j} = \frac{\bar{R}_{net}^{OOS}_{c^*_j, j}}{\hat{\sigma}^{OOS}_{R_{net}, c^*_j, j}}$$

I cromosomi $c \in \mathcal{F}_1$ sono ordinati per $\widehat{SR}^{OOS}_{c, j}$ decrescente sulla finestra OOS CSCV. Si definisce il **rank OOS relativo** del vincente in-sample $c^*_j$:

$$r_j = \frac{\text{rank}^{OOS}(c^*_j, j)}{|\mathcal{F}_1|} \in (0, 1]$$

dove $\text{rank}^{OOS}(c^*_j, j) \in \{1, \ldots, |\mathcal{F}_1|\}$ è il rank OOS del cromosoma $c^*_j$ (rank 1 = miglior cromosoma OOS, rank $|\mathcal{F}_1|$ = peggior cromosoma OOS).

**Passo 5 — Logit-rank.** Si calcola la trasformazione logit del rank OOS relativo:

$$\lambda_j = \ln\!\left(\frac{r_j}{1 - r_j}\right)$$

con convenzione di troncamento per $r_j$ vicino a 0 o 1 (per evitare divergenze): nell'implementazione, $r_j$ è ridefinito come $r_j \in [1/(|\mathcal{F}_1| + 1); |\mathcal{F}_1|/(|\mathcal{F}_1| + 1)]$ per garantire $\lambda_j$ finita.

**Passo 6 — Stima del PBO.** Il PBO è la **frazione di combinazioni con logit-rank negativa**:

$$PBO = \frac{|\{j \in \{1, \ldots, \binom{S}{S/2}\} : \lambda_j < 0\}|}{\binom{S}{S/2}}$$

Equivalentemente, $\lambda_j < 0 \iff r_j < 0{,}5 \iff$ il cromosoma vincente in-sample della combinazione $j$ è OOS **sotto la mediana del fronte di Pareto**: un valore di $PBO$ vicino a $0{,}5$ implica che il vincente in-sample è OOS sotto la mediana nel 50% delle combinazioni, ovvero la scelta del bundle è statisticamente indistinguibile dalla casualità della partizione.

### 33.2 Block-CSCV per finestra OOS temporalmente strutturata

La finestra OOS aggregata di Cap.31.1 è **temporalmente strutturata** come concatenazione dei $F$ fold $W_{oos}$ del walk-forward nested. Il CSCV standard a sotto-finestre contigue rispetta già la struttura temporale, evitando rotture artificiali della dipendenza temporale dei rendimenti $R_{net}$.

La **scelta di $S$** è funzione di $F$ effettivo e segue la regola di allineamento ai fold del walk-forward:

- **$F = 8$ ideale**: $S = 16$ blocchi di lunghezza $W_{oos}/2 = 26.460$ barre 1-min ciascuno (mezza finestra OOS per fold). Il vincolo $S$ pari è soddisfatto.
- **$F = 6$ atteso**: $S = 12$ blocchi di lunghezza $W_{oos}/2 = 26.460$ barre 1-min ciascuno. Il vincolo $S$ pari è soddisfatto.
- **$F = 7$ intermedio**: $S = 14$ blocchi di lunghezza $W_{oos}/2 = 26.460$ barre 1-min ciascuno.

L'allineamento $S = 2F$ produce 2 blocchi per fold, garantendo che la struttura $W_{oos}$ di ciascun fold sia preservata (no spezzettamento di un fold in più di 2 blocchi, che produrrebbe rotture intra-fold non motivate). Bailey-Borwein-López de Prado-Zhu 2017, sez. 3, raccomandano $S \in [10, 16]$ come ordine di grandezza tipico per problemi di selezione di strategie su backtest finanziari; la scelta $S \in \{12, 14, 16\}$ adottata qui rientra in questa raccomandazione.

### 33.3 Soglia di accettazione del PBO

Il gate di fragilità di Cap.33 opera con soglia:

$$PBO(\theta^*) < \theta_{PBO} = 0{,}50$$

valore di lavoro provvisorio non congelato (dominio $(0, 1)$, riconsiderato post-go-live). La motivazione di $\theta_{PBO} = 0{,}50$ è il **gate minimo** raccomandato da Bailey-Borwein-López de Prado-Zhu 2017: $PBO \geq 0{,}5$ significa che il cromosoma vincente in-sample è OOS sotto la mediana in almeno metà delle combinazioni CSCV, ovvero la scelta del bundle è equivalente a una selezione casuale dal fronte di Pareto. $PBO < 0{,}5$ indica che il vincente in-sample tende a essere sopra la mediana in OOS, ovvero la selezione produce informazione genuinamente predittiva e non un artefatto di overfitting.

Bailey-Borwein-López de Prado-Zhu 2017 raccomandano anche un **gate forte** $PBO < 0{,}40$ per applicazioni che richiedono robustezza più elevata (sez. 5). Cap.33 adotta il **gate minimo** $\theta_{PBO} = 0{,}50$ come default proposto per Parte VII, con possibile innalzamento a $\theta_{PBO} = 0{,}40$ riconsiderato post-go-live qualora la distribuzione empirica di $PBO$ sui cicli di training successivi mostri sistematicamente valori inferiori a $0{,}40$ (segnale che il gate al 50% è troppo permissivo) o valori sistematicamente vicini a $0{,}5$ (segnale che il gate al 50% è borderline).

### 33.4 Costo computazionale e dichiarazione di $S$ provvisorio

Il costo computazionale del PBO via CSCV è dominato dal numero di combinazioni $\binom{S}{S/2}$ moltiplicato per il numero di cromosomi del fronte $|\mathcal{F}_1|$ e per due valutazioni di Sharpe Ratio (in-sample CSCV + OOS CSCV) per ciascuna combinazione e ciascun cromosoma.

**Stima per $S = 16$** ($F = 8$ ideale): $\binom{16}{8} = 12.870$ combinazioni; $|\mathcal{F}_1| \sim 30$ cromosomi tipici (López de Prado 2018 cap. 12); 2 valutazioni Sharpe per combinazione $\times$ cromosoma; ordine di grandezza totale $12.870 \cdot 30 \cdot 2 \approx 7{,}7 \cdot 10^5$ valutazioni di Sharpe Ratio. Ogni valutazione richiede $O(n_{segnali, CSCV})$ operazioni con $n_{segnali, CSCV} \approx n / 2 \approx 1.000$ segnali per sotto-finestra CSCV (eredità $n \approx 2.000$ segnali totali aggregati). Totale operazioni $\sim 7{,}7 \cdot 10^5 \cdot 10^3 \approx 7{,}7 \cdot 10^8$ operazioni elementari.

**Stima per $S = 12$** ($F = 6$ atteso): $\binom{12}{6} = 924$ combinazioni; ordine di grandezza totale $924 \cdot 30 \cdot 2 \approx 5{,}5 \cdot 10^4$ valutazioni di Sharpe Ratio; operazioni totali $\sim 5{,}5 \cdot 10^4 \cdot 10^3 \approx 5{,}5 \cdot 10^7$ operazioni elementari. Significativamente più leggero (un ordine di grandezza in meno rispetto a $S = 16$).

Il calcolo del PBO è confrontato con il training NSGA-II di Parte V, che produce $\sim 10^9$ operazioni per fold (Cap.23.6 di Parte V: $17.408$ valutazioni $\times t_{eval}$ con $t_{eval}$ contenente complessità di replay state machine + survival + fitness). Per $F = 8$ fold completi, il training totale è $\sim 8 \cdot 10^9$ operazioni; per $F = 6$, $\sim 6 \cdot 10^9$. Il PBO con $S = 16$ è $\sim 7{,}7 \cdot 10^8$, ovvero $\sim 10\%$ del training $F = 8$; con $S = 12$ è $\sim 5{,}5 \cdot 10^7$, ovvero $\sim 1\%$ del training $F = 6$.

**Frazione del compute budget** assorbita dal PBO è dunque inferiore al **5%** del totale (coerente con la dichiarazione globale di Cap.34.4 sotto sul compute budget aggregato del bootstrap + PBO + DSR). Il PBO non aggrava significativamente il compute stress test e non è la causa del bundle parziale $F \approx 6$ atteso di Cap.26.2 di Parte V, che è dovuto al training NSGA-II stesso.

La scelta di $S$ è dichiarata come **parametro di tuning provvisorio**: $S = 16$ default per $F = 8$ ideale, $S = 12$ default per $F = 6$ atteso, $S = 14$ per $F = 7$ intermedio. La regola di selezione è deterministica ($S = 2F$). Il valore effettivo di $S$ è registrato come metadato del bundle frozen (Cap.35.1 elemento 6).

### 33.5 Esempio numerico illustrativo

L'esempio è **illustrativo** (non è un risultato empirico del backtest). Si suppongono i seguenti valori sulla finestra OOS aggregata di Cap.31.1:

- $|\mathcal{F}_1| = 30$ cromosomi nel fronte di Pareto;
- $F = 8$ ideale, $S = 16$ sotto-finestre, $\binom{16}{8} = 12.870$ combinazioni;
- Cromosoma candidato $c^*$ vincente nell'in-sample CSCV in $8.500$ delle $12.870$ combinazioni (cromosoma con buona stabilità in-sample);
- Rank OOS medio del vincente in-sample $c^*$ nelle altre $4.370$ combinazioni (dove $c^*$ è secondo o terzo in-sample) è $\sim 8$ su $30$ (cromosoma a un quarto del fronte OOS, segnale di buona predittività OOS);
- Sulle $8.500$ combinazioni in cui $c^*$ vince in-sample, il rank OOS è distribuito come segue (illustrativa): $4.500$ combinazioni con $r_j < 0{,}5$ (vincente in-sample sotto la mediana OOS = overfit), $4.000$ combinazioni con $r_j \geq 0{,}5$ (vincente in-sample sopra la mediana OOS = non-overfit).

**Calcolo di $PBO$:**

Considerando l'intera popolazione di $12.870$ combinazioni (non solo quelle in cui $c^*$ vince in-sample, ma tutte le combinazioni con il rispettivo vincente in-sample della combinazione), il conteggio totale delle combinazioni con $\lambda_j < 0$ (cioè $r_j < 0{,}5$) è $\sim 4.500$ delle $12.870$:

$$PBO \approx \frac{4.500}{12.870} \approx 0{,}3497$$

Il bundle candidato dell'esempio ha $PBO \approx 0{,}35 < \theta_{PBO} = 0{,}50$: **passa il gate di fragilità**. L'interpretazione: in circa il $35\%$ delle combinazioni CSCV il cromosoma vincente in-sample è OOS sotto la mediana, valore inferiore al $50\%$ del gate minimo, indicando che la selezione del bundle produce informazione genuinamente predittiva.

Anche questo esempio rispetta il tick FIB di 5 pt nei rendimenti per-segnale (i valori di $PBO$ sono adimensionali, frazioni nel range $[0, 1]$); l'esempio è dichiarato **illustrativo** e non costituisce risultato empirico del backtest.

I parametri di tuning provvisori introdotti in Cap.33 sono $\theta_{PBO} = 0{,}50$ e $S \in \{12, 14, 16\}$ (regola $S = 2F$ deterministica), dichiarati non congelati in Parte VII. Le citazioni esplicite di questa sezione richiamano Bailey-Borwein-López de Prado-Zhu 2017, López de Prado 2018 cap. 11-12, Cap.23.1 di Parte V (fronte $\mathcal{F}_1$), Cap.24.7 di Parte V (no PBO in NSGA-II), Cap.31.1 (fold OOS aggregato), Cap.5 di Parte I (definizione operativa del successo).

---

## Capitolo 34 — Bootstrap stazionario

### 34.1 Definizione del bootstrap stazionario

Il **bootstrap stazionario** è introdotto da Politis e Romano (1994) "The stationary bootstrap", *Journal of the American Statistical Association* 89(428), 1303-1313, come metodo di ricampionamento per serie temporali dipendenti che preserva la stazionarietà del processo bootstrappato. La procedura formale è:

**Dato** un campione $\{X_1, X_2, \ldots, X_n\}$ con dipendenza temporale (qui $X_i = R_{net,i}$ per $i \in \{1, \ldots, n\}$ rendimenti netti dei segnali eseguiti aggregati cross-fold), **generare** un campione bootstrap $\{X_1^*, X_2^*, \ldots, X_n^*\}$ tramite campionamento di **blocchi di lunghezza aleatoria geometrica**:

1. Si fissa la **probabilità di terminazione del blocco** $p = 1/L_{avg}$, con $L_{avg}$ block length media (parametro del bootstrap, Cap.34.2 sotto). La lunghezza di un blocco è $L \sim \text{Geom}(p)$, ovvero $P(L = \ell) = p \cdot (1 - p)^{\ell - 1}$ per $\ell = 1, 2, \ldots$; il valore atteso è $E[L] = 1/p = L_{avg}$.
2. Per costruire $\{X_1^*, \ldots, X_n^*\}$, si parte da $X_1^*$ campionando $t_1 \sim \text{Uniform}(\{1, \ldots, n\})$ e si pone $X_1^* = X_{t_1}$.
3. Iterativamente, per $i = 2, \ldots, n$: con probabilità $p$ si avvia un nuovo blocco, campionando $t_i \sim \text{Uniform}(\{1, \ldots, n\})$ e ponendo $X_i^* = X_{t_i}$; con probabilità $1 - p$ si continua il blocco corrente, ponendo $X_i^* = X_{t_{i-1} + 1}$ (con wrap modulo $n$: se $t_{i-1} + 1 > n$, si pone $X_i^* = X_{(t_{i-1} \mod n) + 1}$, garantendo la **stazionarietà** del processo bootstrappato).
4. Si replica la procedura $B = 2.000$ volte (eredità Cap.4 di Parte I + Cap.34.4 sotto), producendo $B$ campioni bootstrap $\{X_1^{*(b)}, \ldots, X_n^{*(b)}\}_{b=1}^{B}$.

Il wrap modulo $n$ (passo 3) è la differenza essenziale fra bootstrap stazionario e bootstrap a blocchi non sovrapposti (Carlstein 1986) o sovrapposti (Künsch 1989): il wrap garantisce che il campione bootstrap sia stazionario, ovvero la distribuzione marginale di $X_i^*$ è la stessa per ogni $i$.

**Coerenza con la sessione operativa.** Il campionamento bootstrap di Cap.34.1 opera sui rendimenti $R_{net}$ dei **segnali eseguiti** della finestra OOS aggregata, non sulle barre 1-min. Poiché i segnali eseguiti hanno durata variabile (eredità Cap.7 di Parte II: state machine con timer $\Delta t_{cromosoma}, T_{touch}^{max}$) e sono filtrati dalla politica di no-refresh di Cap.28 di Parte VI (vincolo $|\mathcal{A}(t)| \leq 1$), la sequenza $\{R_{net,i}\}_{i=1}^{n}$ è la sequenza ordinata temporalmente dei segnali eseguiti, dove $n$ è il totale segnali eseguiti cross-fold. Non si bootstrappano barre 1-min direttamente: il bootstrap opera al livello dei segnali, preservando la separazione fra segnali simultanei (impossibili per Cap.6.3 di Parte II) e segnali sequenziali (segnale $i+1$ inizia dopo terminazione del segnale $i$). Il bootstrap **non genera segnali simultanei artificiali**, in coerenza con il vincolo segnale unico attivo di Cap.6.3 di Parte II.

**Coerenza con la finestra operativa 8:00-22:00 CET.** I segnali eseguiti della finestra OOS aggregata sono tutti emessi nella finestra di sessione 8:00-22:00 CET di Cap.1 di Parte I (840 barre 1-min/sessione). Il bootstrap non campiona segnali overnight (nessun segnale esiste in quella finestra). Il bootstrap rispetta dunque per costruzione la finestra operativa.

### 34.2 Scelta della block length $L_{avg}$

La block length media $L_{avg}$ è calibrata automaticamente tramite il criterio di **Politis e White (2004)** "Automatic block-length selection for the dependent bootstrap", *Econometric Reviews* 23(1), 53-70: $L_{avg}$ è funzione dell'autocorrelazione empirica della serie $\{R_{net,i}\}_{i=1}^{n}$. La procedura di Politis-White stima il **flat-top spectral density estimator** della serie e calcola $L_{avg}$ come funzione del rapporto fra autocorrelazione cumulata e varianza spettrale al centro.

Per FIB intraday, l'autocorrelazione di $R_{net}$ per-segnale è tipicamente **bassa**: il signal lifecycle è multi-bar (durata media stimata $\sim 30-60$ minuti per segnale, eredità Cap.7 di Parte II + Cap.24.3 di Parte V), ma i $R_{net}$ per-segnale sono pseudo-iid sotto la fitness multi-fold del NSGA-II (Cap.24.6 di Parte V: aggregazione mediana cross-fold + segnali separati da $|\mathcal{A}(t)| \leq 1$). L'ordine di grandezza atteso è $L_{avg} \in [5, 20]$ segnali. Il **valore di lavoro di default** è $L_{avg} = 10$ segnali, dichiarato non congelato in Parte VII (dominio $[1, +\infty)$, riconsiderato sulla base della stima Politis-White empirica del run corrente).

**Calibrazione automatica obbligatoria.** Il valore $L_{avg} = 10$ è solo starting point: l'implementazione deve eseguire la procedura Politis-White su ogni run e adottare il valore stimato. La calibrazione automatica via Politis-White è obbligatoria in Parte VII; il valore effettivo di $L_{avg}$ è registrato come metadato del bundle frozen (Cap.35.1 elemento 6).

**Comportamento ai bordi.** Se Politis-White stima $L_{avg} > n/5$ (block length troppo lungo rispetto al campione), si tronca a $L_{avg} = n/5$ per evitare ricampionamenti degenere (blocchi che coprono la maggior parte del campione, riducendo l'effetto del bootstrap). Se Politis-White stima $L_{avg} < 1$ (segnali pseudo-iid completo, autocorrelazione trascurabile), si tronca a $L_{avg} = 1$ (bootstrap iid standard).

### 34.3 Intervalli di confidenza bootstrap

Per ogni metrica aggregata $\theta$ del bundle candidato, si calcola la statistica bootstrappata $\hat{\theta}^{*(b)}$ su ciascuno dei $B = 2.000$ campioni bootstrap. La distribuzione empirica $\{\hat{\theta}^{*(b)}\}_{b=1}^{B}$ produce l'**intervallo di confidenza al 95%** tramite **percentile method**:

$$IC_{95\%}(\theta) = \big[\hat{\theta}^{*}_{[2{,}5\%]};\; \hat{\theta}^{*}_{[97{,}5\%]}\big]$$

dove $\hat{\theta}^{*}_{[\alpha\%]}$ è il percentile $\alpha\%$ della distribuzione bootstrappata.

**Tredici metriche bootstrappate**, esplicitamente:

1. $DSR(\theta^*)$ — Deflated Sharpe Ratio del bundle candidato (Cap.32);
2. $PBO(\theta^*)$ — Probability of Backtest Overfitting (Cap.33);
3. $f_1^{global}(\theta^*) = E[R_{net} \mid executed]$ — expected net return per segnale (Cap.24.1 di Parte V);
4. $f_2^{global}(\theta^*)$ — target_1 hit rate (Cap.24.1 di Parte V);
5. $f_3^{global}(\theta^*)$ — invalidation rate (Cap.24.1 di Parte V);
6. $f_4^{global}(\theta^*)$ — Maximum Drawdown intraday (Cap.24.1 di Parte V);
7. $f_5^{global}(\theta^*)$ — stabilità cross-regime (Cap.24.1 di Parte V);
8. $\pi_{t_2 \mid t_1}^{aggregated}(\theta^*)$ — probabilità di proseguimento target_2 condizionato a target_1 hit (Cap.11 di Parte II + Cap.24.3 di Parte V);
9. $\text{MFE}_{aggregated}(\theta^*)$ — Maximum Favourable Excursion mediana cross-segmento post-target_1 (Cap.11 di Parte II);
10. $\text{MAE}_{aggregated}(\theta^*)$ — Maximum Adverse Excursion mediana cross-segmento post-target_1 (Cap.11 di Parte II);
11. $f_{stop \mid t_1}^{aggregated}(\theta^*)$ — frazione segmenti post-target_1 terminati con stop personale (Cap.11 di Parte II + Cap.24.3 di Parte V);
12. $\text{CVaR}_{95\%}(\theta^*)$ — Conditional Value at Risk al 95% per-segnale eseguito (Cap.5 di Parte I + Cap.24.1 di Parte V eredità $f_4$);
13. $\text{MDD}_{intraday}(\theta^*)$ — Maximum Drawdown intraday aggregato sul fold OOS (Cap.5 di Parte I + Cap.24.1 di Parte V eredità $f_4$).

**Metodo BCa alternativo.** Per metriche con distribuzione bootstrappata sistematicamente skewed (asimmetrica), il **Bias-Corrected and Accelerated bootstrap** (BCa) di Efron (1987) "Better bootstrap confidence intervals", *Journal of the American Statistical Association* 82(397), 171-185, è alternativa accettabile. Il BCa corregge sia il bias mediano $z_0 = \Phi^{-1}(P^*(\hat{\theta}^{*(b)} < \hat{\theta}))$ sia l'accelerazione $a$ via jackknife (Efron 1987 sez. 3). L'intervallo BCa è:

$$IC^{BCa}_{95\%}(\theta) = \big[\hat{\theta}^{*}_{[\alpha_1]};\; \hat{\theta}^{*}_{[\alpha_2]}\big]$$

dove $\alpha_1 = \Phi\!\big(z_0 + (z_0 + z_{0{,}025})/(1 - a(z_0 + z_{0{,}025}))\big)$ e $\alpha_2$ è analogo con $z_{0{,}975}$. La scelta del metodo (percentile vs BCa) è demandata all'implementazione con citazione bibliografica esplicita nel codice di produzione; il percentile method è il **default** di Parte VII.

### 34.4 Compute stress test obbligatorio

Il compute stress test misura empiricamente il tempo wall-clock del walk-forward nested di Parte V + post-processing DSR/PBO/bootstrap su c5.4xlarge 16 vCPU (eredità Cap.4 di Parte I + Cap.26.2 di Parte V rework v3). Il bundle parziale $F \approx 6$ atteso di Cap.26.2 di Parte V impone una **regola di decisione deterministica** fra tre opzioni operative.

**Aritmetica del vincolo $t_{eval}$ per opzione (i).** Sotto $T_{budget} = 80$h wall-clock su 16 vCPU con $F = 8$ fold sequenziali e $N_{eval}^{actual} = 17.408$ valutazioni per fold (Cap.23.6 di Parte V, caso centrale $r_{cache} = 0{,}10$), il tempo medio per valutazione fitness single-thread deve essere:

$$t_{eval, target}^{single} \leq \frac{T_{budget} \cdot 60 \cdot n_{vCPU}}{N_{eval}^{actual} \cdot F} = \frac{80 \cdot 60 \cdot 16}{17.408 \cdot 8} \approx 0{,}551 \quad \text{min/cromosoma single-thread}$$

Tenendo conto della parallelizzazione 16-vCPU non perfettamente lineare (coefficiente di efficienza $\eta_{par} = 0{,}90$ tipico per workload mixed CPU+IO), il vincolo reale del tempo per cromosoma è:

$$t_{eval, target}^{eff} \leq t_{eval, target}^{single} \cdot \eta_{par} = 0{,}551 \cdot 0{,}90 \approx 0{,}496 \quad \text{min/cromosoma}$$

Per il **caso centrale** $r_{cache} = 0{,}10$, $N_{eval}^{actual} = 17.408$: il vincolo è $t_{eval} \leq 0{,}496$ min/cromosoma. Per il **caso ottimo del caching** $r_{cache} = 0{,}15$, $N_{eval}^{actual} = 16.448$: il vincolo si rilassa a $\sim 0{,}525$ min/cromosoma. Per il **caso pessimo** $r_{cache} = 0{,}05$, $N_{eval}^{actual} = 18.368$: si stringe a $\sim 0{,}470$ min/cromosoma.

Confronto con il range $t_{eval} \in [0{,}74; 1{,}47]$ min/cromosoma di Cap.23.6 di Parte V (caso centrale, riallineato M-4 NB-1): il bound inferiore $t_{eval} = 0{,}74$ è **già sopra** il vincolo necessario di $0{,}496$ min/cromosoma, ovvero opzione (i) **non è fattibile senza ottimizzazione del calcolo fitness** (es. caching aggressivo dei residui EGARCH, vettorializzazione del replay state machine, eliminazione di chiamate Python pure in favore di NumPy/Numba). La conformità di opzione (i) è quindi **condizionata** al risultato del compute stress test empirico.

**Regola di decisione deterministica fra le tre opzioni.**

- **Opzione (i) — $F = 8$ completo con ottimizzazione del calcolo fitness.** Se la misura empirica del compute stress test mostra $t_{eval}^{measured} \leq 0{,}496$ min/cromosoma su c5.4xlarge dopo ottimizzazione (caching residui EGARCH + vettorializzazione replay + Numba), **adottare opzione (i)**. Metadato del bundle: `F_effective = 8`.
- **Opzione (ii) — $F = 8$ completo con parallelizzazione $> 16$ vCPU.** Altrimenti, se la migrazione a c5.9xlarge (36 vCPU, $\sim 0{,}765$ USD/h spot) o c5.18xlarge (72 vCPU, $\sim 1{,}53$ USD/h spot) produce un **differenziale di costo** $\leq \theta_{cost} = 100$ USD/run rispetto a c5.4xlarge 80h (15 USD/h spot $\cdot$ 80h $= \sim 12$ USD/run di base, con margine; il differenziale cresce con vCPU aggiuntive ma anche il tempo wall-clock si riduce in proporzione 16/36 = $\sim 0{,}44$ o 16/72 = $\sim 0{,}22$), **adottare opzione (ii)**. Aritmetica esplicita per c5.9xlarge: tempo wall-clock $\approx 107 \cdot 16/36 \approx 47{,}6$ h, costo $\approx 47{,}6 \cdot 0{,}765 \approx 36{,}4$ USD/run; differenziale vs c5.4xlarge $\approx 36{,}4 - 12 = 24{,}4$ USD/run, ben sotto $\theta_{cost} = 100$ USD/run. Per c5.18xlarge: $107 \cdot 16/72 \approx 23{,}8$ h, costo $\approx 23{,}8 \cdot 1{,}53 \approx 36{,}4$ USD/run; differenziale $\approx 24{,}4$ USD/run, anche qui sotto soglia. Entrambe le sotto-opzioni sono fattibili sotto $\theta_{cost}$; la scelta fra c5.9xlarge e c5.18xlarge è ulteriormente raffinata in base a disponibilità spot dell'istanza. Metadato del bundle: `F_effective = 8`, con sotto-metadato `compute_instance = "c5.9xlarge"` o `"c5.18xlarge"`.
- **Opzione (iii) — $F \approx 6$ atteso con varianza inflated accettata.** Altrimenti (opzione (i) non fattibile, opzione (ii) differenziale di costo $> \theta_{cost}$), **adottare opzione (iii)**: si accetta il bundle parziale a $F$ effettivo $\sim 6$ con varianza inflated cross-fold dell'aggregazione mediana di Cap.24.6 di Parte V. La varianza inflated è **quantificata empiricamente dal bootstrap di Cap.34.3** sui $\sim 6$ fold ottenuti: l'intervallo di confidenza al 95% di $f_1^{global}, f_2^{global}, f_3^{global}, f_4^{global}$ è calcolato direttamente sui 6 valori cross-fold disponibili, con effettiva larghezza maggiore rispetto al caso $F = 8$. Metadato del bundle: `F_effective = 6` (o valore effettivamente ottenuto, $\in \{5, 6, 7\}$).

La **regola di decisione** è deterministica e l'esito è funzione della misura empirica del compute stress test: il Developer di Parte VII **dichiara la regola e l'aritmetica**, non simula gli esiti. La misura empirica sarà disponibile in produzione/ciclo successivo; il bundle frozen del run corrente registra come metadato $F_{effective}$ il valore effettivo ottenuto. Riferimenti incrociati: Cap.23.6 di Parte V riga 223 (raccomandazione $F = 2-3$ storica vs Cap.26.2 di Parte V $F \approx 6$ atteso, O-v4-1 Review v4 NEUTRO) sono riconciliati empiricamente in questo Cap.34.4 tramite la regola deterministica fra le tre opzioni.

**Costo computazionale del bootstrap stesso.** Per ciascuna delle 13 metriche bootstrappate di Cap.34.3 e $B = 2.000$ replicazioni, ciascuna replicazione richiede $O(n_{segnali})$ operazioni di ricalcolo della metrica sul campione bootstrap. Con $n_{segnali} \in [1.500; 3.000]$ (eredità Cap.25.5 di Parte V $N_{eventi} \in [120; 380]$ per fold $\times F \in \{6, 7, 8\}$), il numero totale di operazioni elementari del bootstrap è:

$$N_{bootstrap}^{ops} = 13 \cdot B \cdot n_{segnali} = 13 \cdot 2.000 \cdot n_{segnali} = 26.000 \cdot n_{segnali}$$

con range $[26.000 \cdot 1.500; 26.000 \cdot 3.000] = [3{,}9 \cdot 10^7; 7{,}8 \cdot 10^7]$ operazioni elementari. Confronto con il training NSGA-II di Cap.23.6 di Parte V: $\sim 10^9$ operazioni per fold, totale $\sim 6 \cdot 10^9$ ($F = 6$) o $\sim 8 \cdot 10^9$ ($F = 8$) operazioni per training. La **frazione di compute budget assorbita dal bootstrap stesso** è dunque:

$$\frac{N_{bootstrap}^{ops}}{N_{training}^{ops}} = \frac{[3{,}9; 7{,}8] \cdot 10^7}{[6; 8] \cdot 10^9} \in [0{,}005; 0{,}013]$$

ovvero **< 5%** del compute budget totale. Il bootstrap non aggrava significativamente il compute stress test e **non è la causa** del bundle parziale $F \approx 6$ atteso di Cap.26.2 di Parte V (che è dovuto al training NSGA-II stesso). Sommando PBO ($\sim 1\%$ per $S = 12$, fino a $\sim 10\%$ per $S = 16$, Cap.33.4) e bootstrap ($< 5\%$), il post-processing totale di Parte VII assorbe **al massimo $\sim 15\%$ del compute budget**.

**Cloud per bootstrap stazionario.** Il bootstrap stazionario $B = 2.000$ **non è eseguibile in locale** (Intel Core i5-7200U/8 GB di Cap.3 di Parte I) entro tempi ragionevoli: $B \cdot n_{segnali}$ operazioni $\sim 10^7$ per ciascuna delle 13 metriche, totale $\sim 10^8$ operazioni con overhead di replay state machine per ricostruire le metriche complesse (sub-machine post-target_1, CVaR, MDD intraday) ai blocchi bootstrap. Il bootstrap gira su c5.4xlarge (16 vCPU, $\sim 15$ USD/h spot) **come post-processing aggiuntivo del walk-forward stesso**, all'interno del compute budget di Cap.4 di Parte I e Cap.26.2 di Parte V. Il bootstrap rientra nel $< 5\%$ del compute budget; il run aggregato Parte V + Parte VII si conclude entro $T_{budget} = 80$h wall-clock sotto le opzioni (i)/(ii)/(iii).

### 34.5 Bootstrap stazionario e replay bit-exact

Il **seed PRNG** del bootstrap stazionario (campionamento dei blocchi $L \sim \text{Geom}(p)$ + posizioni $t_i \sim \text{Uniform}$) è **parte dell'identità del bundle frozen** (Cap.35.1 elemento 5). Due esecuzioni del bootstrap con stesso seed, stessi log di replay del walk-forward e stesso $L_{avg}$ calibrato da Politis-White producono **identici intervalli di confidenza al bit**, in coerenza con il vincolo di replay bit-exact di Cap.10 di Parte II.

Il seed PRNG del bootstrap è una variabile scalare intera di lunghezza minima 64 bit (es. NumPy `numpy.random.default_rng(seed_bootstrap)`), separata e indipendente dal seed PRNG del NSGA-II (Cap.23.7 di Parte V) e dei modelli EGARCH e Cox stimati nei fold. La separazione dei seed garantisce che la stima del PRNG del bootstrap non interferisca con la riproducibilità del fronte di Pareto di Parte V. Il seed bootstrap è registrato nel bundle frozen come campo `seed_bootstrap` (Cap.35.1 elemento 5).

I parametri di tuning provvisori introdotti in Cap.34 sono $\theta_{cost} = 100$ USD/run e $L_{avg} = 10$ (default Politis-White), dichiarati non congelati in Parte VII. Il valore $B = 2.000$ ricampionamenti è eredità di Cap.4 di Parte I (compute budget cloud). Le citazioni esplicite di questa sezione richiamano Politis-Romano 1994, Politis-White 2004, Efron 1987 (BCa), López de Prado 2018 cap. 12, Cap.4 di Parte I (compute budget cloud), Cap.23.6 di Parte V (compute calcolo + range $t_{eval}$), Cap.24.1-24.6 di Parte V (metriche $f_1$-$f_5$ + $\text{IQR}_{norm}$), Cap.25.1 di Parte V ($F = 8$ provvisorio), Cap.26.2 di Parte V ($T_{budget} = 80$h + bundle parziale $F \approx 6$ atteso).

---

## Capitolo 35 — Frozen bundle e immutabilità

### 35.1 Specifica formale del bundle frozen

Il **bundle frozen** è un **artefatto digitale immutabile** prodotto dalla procedura di Parte VII a partire dal cromosoma vincente $\theta^*$ selezionato in Cap.31.2 e dai modelli stimati nel walk-forward nested di Parte V. Il bundle frozen è composto da **sei elementi**:

**Elemento 1 — Parametri congelati di Parte V.** Tutti i parametri della **tabella di congelamento di Cap.26.5 di Parte V** sono inclusi nel bundle. La tabella copre: parametri del modello EGARCH ($W$ rolling default $= 210.000$, $D$ default Student-t, opzione di inizializzazione default Opzione A — valori effettivi del ciclo registrati come metadati Cap.31.4); classificazione regime ($\bar{\sigma}_s$, $p = 0{,}75$, $N_{reg} = 20$, $T_{persist} = 10$); pivot detection ($n_c = 3$, $\delta_{pivot} = 10$ pt); trade_range ($A_{range,min} = 80$ pt, $N_{osc} = 60$, $n_{osc,min} = 2$, $\epsilon_{osc} = 5$ pt, $N_{break} = 20$, $\delta_{break} = 10$ pt); parametri NSGA-II ($\eta_c, \eta_m, p_m, P = 128, G_{max} = 150, G_{stall} = 15, \epsilon_{front} = 0{,}01$); walk-forward ($W_{in} = 105.840$, $W_{oos} = 52.920$, $P_{purge} = 4.200$, $P_{emb} = 4.200$, $F$ effettivo registrato come `F_effective`); soglie diagnostica survival ($\theta_{CV} = 0{,}50$ provvisoria, $p_{Schoenfeld} = 0{,}05$); $K_{max} = 6$ vettore feature selection (Cap.26.7 di Parte V); ogni altra voce della tabella senza eccezioni.

**Elemento 2 — Geni del cromosoma vincente.** Tutti i geni del cromosoma $\theta^* \in \mathcal{F}_1$ selezionato in Cap.31.2:
- **Geni geometrici** (Cap.22.1 di Parte V): $b$ (semi-ampiezza banda entry), $d_{inv}$ (distanza invalidazione), $d_{obsolete}$ (distanza obsolescenza), $T_{min,session}$ (tempo residuo minimo);
- **Geni di emissione** (Cap.22.2-22.4 di Parte V): $\tau_{vol}$ (soglia volatilità), $\tau_{liq}$ (soglia liquidità), $\tau_{dist}^{\sigma}$ (soglia distanza in sigma-units), $\tau_{surv}$ (soglia survival $\hat{p}_{hit}$);
- **Geni target/stop** (Cap.22.3 di Parte V): $k_{t2}$ (moltiplicatore target_2 sintetico), $d_{stop,\sigma}$ (distanza stop in sigma-units);
- **Geni temporali** (Cap.22.4 di Parte V): $\Delta t_{cromosoma}$ (timer post-trigger), $T_{touch}^{max}$ (timer pre-trigger);
- **Vettore selezione feature** (Cap.22.6 di Parte V + Cap.26.7 di Parte V): $\mathbf{s} \in \{0, 1\}^{37}$ con cardinalità $|\mathbf{s}|_1 \leq K_{max} = 6$ (per regime directional) o $\mathbf{s} \in \{0, 1\}^{38}$ con cardinalità $\leq 6$ per regime trade_range (eredità M-13 chiusa, feature $x^{(A_{range})}$ condizionale).

**Elemento 3 — Modelli stimati.** I modelli stimati nell'**ultimo fold di calibrazione** del walk-forward nested di Parte V:
- **Coefficienti EGARCH(1,1)** $(\mu, \omega, \alpha, \gamma, \beta, \nu)$, con $\nu$ parametro della distribuzione $D$ (Student-t o GED secondo Cap.31.4), valori scalari in doppia precisione IEEE 754;
- **Coefficienti Cox cause-specific (o Fine-Gray sub-distribution, secondo Cap.31.3)** $\boldsymbol{\beta}_{j, R}$ per ciascuna causa $j \in \{1, 2\}$ (target_1_hit, stopped) e per ciascuno strato $R \in \{\text{calmo}, \text{turbolento}\}$ (oppure modello unico con interaction term se Cap.31.3 fallback a opzione (a) interaction term); baseline hazard $h_{0, j, R}(\tau)$ tabulate sui valori discreti di $\tau$ osservati nel fold;
- **Quantili regime** $\bar{\sigma}_s$ calibrati nell'ultimo fold (eredità Cap.14 di Parte III): valore scalare per regime calmo/turbolento al quantile $p = 0{,}75$.

**Elemento 4 — Definizione formale della tupla payload $\mathcal{S}$.** La specifica formale della tupla $\mathcal{S}$ di Cap.6.1 di Parte II Iterazione 4 (12 campi: `signal_id`, `timestamp_emission`, `direction`, `entry_zone`, `target_1`, `target_2`, `target_2_type`, `stop_loss`, `stop_type`, `setup_class`, $\Delta t_{cromosoma}$, $T_{touch}^{max}$) è inclusa nel bundle frozen come **definizione strutturale invariante**. Garantisce che modifiche future al payload (es. aggiunta di un campo) richiedano **un nuovo ciclo Parte II + Parte V + Parte VII**, non possono essere introdotte da un rilascio del bundle frozen.

**Elemento 5 — Seed PRNG.** Tutti i seed dei generatori pseudo-casuali utilizzati nel ciclo di produzione del bundle:
- `seed_nsga2` (Cap.23.7 di Parte V): per inizializzazione popolazione, torneo binario, SBX crossover, polynomial mutation, riparazione locale;
- `seed_egarch_mle` (Cap.13 di Parte III): per inizializzazione MLE dell'EGARCH (ottimizzazione numerica del log-likelihood);
- `seed_cox_mle` (Cap.19 di Parte IV): per inizializzazione MLE del Cox cause-specific o Fine-Gray;
- `seed_bootstrap` (Cap.34.5): per campionamento blocchi $L \sim \text{Geom}(p)$ e posizioni $t_i \sim \text{Uniform}$ del bootstrap stazionario.

Tutti i seed sono valori scalari interi di lunghezza minima 64 bit.

**Elemento 6 — Metadati di tracciabilità.** I metadati registrati nel bundle frozen come dati strutturali del run di produzione:
- **`F_effective`** $\in \{5, 6, 7, 8\}$: numero di fold effettivamente completati dal walk-forward nested (eredità Cap.34.4: dipende dalla regola di decisione fra opzioni (i)/(ii)/(iii));
- **`compute_instance`** $\in \{\text{"c5.4xlarge"}, \text{"c5.9xlarge"}, \text{"c5.18xlarge"}\}$: istanza cloud utilizzata (eredità Cap.34.4);
- **`r_FG`** $\in [0, 1]$: rapporto fold con `flag_fine_gray_preferito = True` (Cap.31.3);
- **`r_CV`** $\in [0, 1]$: rapporto fold con $CV(\hat{\boldsymbol{\beta}}_{j,R}) > \theta_{CV}$ (Cap.31.3);
- **`r_Schoenfeld`** $\in [0, 1]$: rapporto fold con $p_{Schoenfeld} < 0{,}05$ (Cap.31.3);
- **`cox_model_type`** $\in \{\text{"cause\_specific"}, \text{"fine\_gray"}\}$: modello survival adottato (Cap.31.3);
- **`cox_stratification`** $\in \{\text{"formal\_strata"}, \text{"interaction\_term"}\}$: schema di stratificazione (Cap.31.3);
- **`cox_time_varying_active`** $\in \{\text{True}, \text{False}\}$: flag di attivazione condizionale M-16 (Cap.31.3);
- **`egarch_window`**: finestra EGARCH effettiva del ciclo (Cap.31.4);
- **`egarch_distribution`** $\in \{\text{"student\_t"}, \text{"ged"}\}$: distribuzione $D$ effettiva (Cap.31.4);
- **`egarch_init_option`** $\in \{\text{"A\_resume"}, \text{"B\_unconditional"}\}$: opzione di inizializzazione effettiva (Cap.31.4);
- **`K_max_effective`** $= 6$ (valore congelato corrente), con `K_max_strict_recommended` $\in \{\text{True}, \text{False}\}$ se la diagnostica del ciclo raccomanda fallback Harrell-strict (Cap.31.5);
- **`N_trials`** $= |\mathcal{F}_1|$: numero di cromosomi del fronte di Pareto (Cap.32.3);
- **`L_avg_bootstrap`**: block length media effettiva calibrata via Politis-White (Cap.34.2);
- **`S_CSCV`** $\in \{12, 14, 16\}$: numero di sotto-finestre CSCV (Cap.33.2, regola $S = 2F$);
- **`timestamp_freezing`**: data/ora del freezing del bundle in formato ISO 8601;
- **`code_version`**: versione del codice produttore (es. tag git del commit di produzione).

L'insieme dei 6 elementi forma il **contenuto del bundle frozen** ed è la base per il calcolo dell'hash di riferimento di Cap.35.2.

### 35.2 Hash di riferimento immutabile

Il bundle frozen include un **hash crittografico SHA-256** calcolato deterministicamente su tutto il contenuto dei 6 elementi di Cap.35.1. La procedura di calcolo dell'hash è:

1. **Serializzazione canonica del contenuto**: i 6 elementi sono serializzati in formato **JSON canonical form** (RFC 8785, ordinamento lessicografico delle chiavi a tutti i livelli di annidamento, encoding UTF-8 senza BOM, escape standard); alternativamente, una tupla lessicograficamente ordinata di campi con encoding binario IEEE 754 per i valori scalari floating-point e UTF-8 per le stringhe. La convenzione di serializzazione esatta è demandata all'implementazione con citazione esplicita nel codice di produzione (RFC 8785 o equivalente).
2. **Calcolo dell'hash SHA-256**: applicazione del digest SHA-256 (FIPS PUB 180-4) sul flusso di byte serializzato, producendo un valore di 32 byte (256 bit), tipicamente rappresentato come stringa esadecimale di 64 caratteri.
3. **Incorporamento nel bundle**: l'hash è registrato nel bundle stesso come **campo `bundle_hash`** (stringa esadecimale di 64 caratteri).

**Validazione di integrità all'avvio della pipeline.** A ogni caricamento del bundle frozen in pipeline di inference live (Cap.27.3 di Parte VI), il motore:
1. Legge il contenuto dei 6 elementi del bundle (escludendo il campo `bundle_hash`);
2. Ricalcola l'hash SHA-256 secondo la stessa procedura di freezing (passi 1-2);
3. Confronta l'hash ricalcolato con il valore registrato nel campo `bundle_hash`;
4. Se i due hash coincidono al bit, il caricamento procede;
5. Se i due hash non coincidono, il **caricamento fallisce e la pipeline si rifiuta di girare**, con log esplicito dell'errore di integrità.

La validazione all'avvio protegge da corruzioni accidentali del bundle (es. modifica del file durante trasferimento, perdita di precisione numerica durante deserializzazione, alterazione manuale dei parametri). Il vincolo di integrità è coerente con la richiesta di replay bit-exact di Cap.10 di Parte II: due esecuzioni del motore con lo stesso `bundle_hash` e lo stesso feed Directa DAPI producono identica sequenza di emissioni al bit.

### 35.3 Regola di sostituzione del bundle frozen

La sostituzione del bundle frozen in produzione è governata da **quattro regole** esplicite, che si applicano sequenzialmente in base al trigger osservato.

**Regola 1 — Sostituzione pianificata trimestrale o semestrale.** Eredità di Cap.4 di Parte I (compute budget cloud) e del piano di ritraining periodico: un nuovo ciclo Parte V + Parte VII produce un bundle aggiornato con cadenza **trimestrale o semestrale**, parametro di pianificazione del progetto. La transizione dal bundle frozen corrente al nuovo bundle frozen **non interrompe la pipeline di inference live** di Cap.27 di Parte VI: il nuovo bundle entra in vigore alla **prossima emissione** post-transizione. Segnali in stato `active` al momento della transizione **continuano la propria state machine con il bundle precedente** fino al raggiungimento di uno degli stati terminali di Cap.7 di Parte II (`target_1_hit`, `stopped`, `invalidated`, `missed_target`, `expired`, `revoked`); solo le nuove emissioni post-transizione usano il nuovo bundle frozen. Il log di transizione registra: `bundle_id` precedente, `bundle_hash` precedente, `bundle_id` nuovo, `bundle_hash` nuovo, timestamp di transizione, segnali `active` al momento della transizione (con `signal_id` e stato corrente).

**Regola 2 — Sostituzione anticipata su trigger di deriva.** Eredità di Cap.30 di Parte VI alert. Se gli alert di Cap.30.2 di Parte VI (deriva $f_m^{live}$ fuori IQR cross-fold per $> T_{drift,persist}$ giorni) **oppure** Cap.30.3 di Parte VI (deriva $f_5^{live}$ fuori $f_5^{global} \cdot (1 + \alpha_{f_5})$ per $> T_{drift,persist}$ giorni) **oppure** Cap.30.4 di Parte VI (break parametrico $B(t) > \theta_B$ per $> T_{B,persist}$ barre) **oppure** Cap.30.5 di Parte VI (frequenza emissione $r_{emit}^{live}$ fuori $[E_{min}, E_{max}]$ per $> T_{emit,persist}$ giorni) scattano in modo persistente, il ciclo di ritraining è **anticipato** rispetto alla cadenza trimestrale/semestrale pianificata. Le soglie di persistenza ($T_{drift,persist}$, $T_{B,persist}$, $T_{emit,persist}$, $\alpha_{f_5}$) sono parametri di tuning operativo di Parte VI (eredità della decisione di scope (c) del Planner per CAP-07: rimangono starting point con default proposti di Parte VI per il primo run di produzione, riconsiderati a 3-6 mesi di produzione live; Cap.36.4 sotto dichiara la conseguenza operativa).

**Regola 3 — Sostituzione anticipata su Cox time-varying coefficients attivato.** Se Cap.31.3 ha registrato `cox_time_varying_active = True` nel bundle frozen del ciclo corrente, il ciclo successivo di ritraining applica il protocollo Parte V con **specifica Cox time-varying coefficients** $\boldsymbol{\beta}_j(\tau)$ secondo Therneau-Grambsch 2000 cap. 6. Il nuovo bundle frozen registra `cox_time_varying_active` aggiornato sulla base del nuovo monitoraggio Schoenfeld del ciclo successivo. La transizione fra bundle segue la stessa regola di gestione dei segnali `active` di Regola 1.

**Regola 4 — Sostituzione anticipata su fallimento di go-live.** Eredità di Cap.31.2 caso di fallimento. Se nessun cromosoma del fronte $\mathcal{F}_1$ del run corrente sopravvive ai filtri 1-5 di Cap.31.2, il run è dichiarato fallito di go-live e si attiva un nuovo ciclo Parte V + Parte VII con eventuale **revisione delle soglie** $\theta_{DSR}, \theta_{PBO}, \theta_{f_5}, \theta_{IQR}, \theta_{t_2}$ (vedi Cap.31.2). Il bundle frozen precedente rimane in produzione fino all'attivazione del nuovo bundle prodotto dal ciclo correttivo; durante la finestra di attesa, la pipeline opera con il bundle precedente, accettando il rischio di deriva fino al ritraining.

La regola di sostituzione applicata è **registrata nel log di transizione** del bundle, con motivazione esplicita: `replacement_reason` $\in \{\text{"scheduled"}, \text{"drift\_trigger"}, \text{"cox\_time\_varying\_active"}, \text{"go\_live\_failure"}\}$.

### 35.4 Versioning del bundle e tracciabilità cross-bundle

Ogni bundle frozen ha un **identificatore progressivo** `bundle_id` (es. `bundle_v1`, `bundle_v2`, $\ldots$) + l'hash SHA-256 calcolato in Cap.35.2. Il `bundle_id` è registrato nel log di emissione di Cap.10 di Parte II per **ogni segnale emesso** dal motore: questo garantisce **tracciabilità cross-bundle**, ovvero è sempre possibile risalire al bundle frozen specifico che ha prodotto un dato segnale, anche dopo molte transizioni successive di bundle.

Una **tabella storica dei bundle** (`bundle_history`) è mantenuta dal sistema di produzione, con riga per ciascun bundle frozen prodotto:

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `bundle_id` | string | Identificatore progressivo (es. `bundle_v1`) |
| `bundle_hash` | string (64 char esa) | Hash SHA-256 del contenuto |
| `timestamp_freezing` | ISO 8601 | Data/ora del freezing |
| `timestamp_activation` | ISO 8601 | Data/ora dell'attivazione in produzione |
| `timestamp_deactivation` | ISO 8601 (opzionale) | Data/ora della disattivazione (sostituzione) |
| `F_effective` | int $\in \{5, 6, 7, 8\}$ | Numero fold effettivamente completati |
| `compute_instance` | string | Istanza cloud utilizzata |
| `DSR_estimate` | float | Stima DSR del bundle |
| `DSR_CI_95` | (float, float) | Intervallo di confidenza 95% DSR bootstrap |
| `PBO_estimate` | float | Stima PBO del bundle |
| `f_1_global` | float | $f_1^{global}$ aggregato |
| `f_5_global` | float | $f_5^{global}$ aggregato |
| `replacement_reason` | string (opzionale) | Motivazione della sostituzione (per bundle precedente disattivato) |
| `cox_time_varying_active` | bool | Flag M-16 |

La tabella `bundle_history` è output del processo di Parte VII e input del monitoring di Cap.30 di Parte VI: confronti longitudinali fra bundle (es. drift della stima $f_5^{global}$ fra bundle successivi) sono parte del reporting post-go-live.

Le citazioni esplicite di Cap.35 richiamano Cap.6.1 di Parte II (payload 12 campi), Cap.10 di Parte II (replay bit-exact + log), Cap.7 di Parte II (state machine + transizione segnali active), Cap.26.5 di Parte V (tabella congelati), Cap.26.8 di Parte V (seed), Cap.27.3 di Parte VI (input invariante pipeline), Cap.30 di Parte VI (alert + dashboard), Cap.31.2 (caso fallimento), Cap.31.3 (decisioni condizionali + M-16).

---

## Capitolo 36 — Gate decisionali per il go-live

### 36.1 Checklist di go-live — AC binari

La decisione binaria di **go-live** del bundle frozen è governata da una **checklist deterministica** di **12 AC binari** (OK / NOT OK), ordinati e verificabili in modo replicabile. La checklist sintetizza tutte le verifiche di Parte VII (DSR, PBO, lifecycle, copertura compute, pipeline operativa) come **AC oggettivi**:

**AC-GO-1 — Gate primario DSR.** $DSR(\theta^*) > \theta_{DSR} = 0{,}95$ (Cap.32.4). Valore numerico di $DSR(\theta^*)$ riportato nel report finale (Cap.36.5 sotto).

**AC-GO-2 — Gate fragilità PBO.** $PBO(\theta^*) < \theta_{PBO} = 0{,}50$ (Cap.33.3). Valore numerico di $PBO(\theta^*)$ riportato nel report finale.

**AC-GO-3 — Expected net return positivo con IC bootstrap.** $E[R_{net} \mid executed](\theta^*) = f_1^{global}(\theta^*) > 0$ **con intervallo di confidenza al 95% bootstrap escluso lo zero** (Cap.34.3 metrica 3). Verifica: $IC_{95\%}(f_1)$ è un intervallo $[a, b]$ con $a > 0$.

**AC-GO-4 — Lifecycle stabile cross-regime.** $|f_5^{global}(\theta^*)| < \theta_{f_5} = 0{,}30$ (Cap.31.2 filtro 3). Il cromosoma $\theta^*$ ha già superato il filtro 3 di Cap.31.2 per essere selezionato come bundle candidato; AC-GO-4 riverifica come gate esplicito di go-live, con riporto del valore numerico.

**AC-GO-5 — Stabilità cross-fold.** $\text{IQR}_{norm}(f_1)(\theta^*) < \theta_{IQR} = 0{,}40$ (Cap.31.2 filtro 4 + Cap.24.6 di Parte V). Riverifica esplicita del filtro 4 con riporto del valore.

**AC-GO-6 — CVaR entro limite.** $\text{CVaR}_{95\%}(\theta^*) > \theta_{CVaR} = -100$ pt FIB (valore di lavoro provvisorio, $\text{CVaR}$ per-segnale eseguito espresso in negativo, entro $-100$ pt FIB). Eredità Cap.5 di Parte I (definizione operativa del successo, $\text{CVaR}_{95\%}$ entro limite dichiarato). $\theta_{CVaR} = -100$ pt FIB equivale a una perdita media nei worst-5%-segnali contenuta entro 100 punti, ordine di grandezza compatibile con stop strutturali tipici di FIB intraday (eredità Cap.18 di Parte IV).

**AC-GO-7 — MDD intraday entro limite.** $\text{MDD}_{intraday}(\theta^*) < \theta_{MDD} = 200$ pt FIB (valore di lavoro provvisorio, MDD aggregato sul fold OOS espresso in positivo come modulo, entro 200 pt FIB). Eredità Cap.5 di Parte I. $\theta_{MDD} = 200$ pt FIB equivale a $200 \cdot 5 = 1.000$ EUR di drawdown intraday massimo per contratto, compatibile con il profilo retail mobile di Cap.2 di Parte I (1 contratto/volta).

**AC-GO-8 — Frequenza emissione entro range.** $r_{emit}(\theta^*) \in [E_{min} = 0{,}2; E_{max} = 5]$ segnali/sessione (eredità Cap.24.2 di Parte V + Cap.26.5 di Parte V). Il cromosoma $\theta^*$ ha già il vincolo $r_{emit} \in [E_{min}, E_{max}]$ verificato nel walk-forward di Parte V; AC-GO-8 riverifica come gate esplicito di go-live sul fold OOS aggregato di Cap.31.1.

**AC-GO-9 — Target operativo asimmetrico raggiunto.** Percentuale di sessioni del fold OOS aggregato di Cap.31.1 che raggiungono il target operativo asimmetrico di Cap.1 di Parte I (500 pt FIB profitto netto/giorno **OR** 70% movimento strutturale intraday) **superiore a** $\theta_{sessions} = 0{,}60$ (valore di lavoro provvisorio). Cap.36.2 sotto dettaglia la formula della verifica aggregata di sessione.

**AC-GO-10 — Pipeline Cap.27 di Parte VI operativa.** Verifica funzionale che la pipeline di inference real-time di Cap.27 di Parte VI:
- (a) carica correttamente il bundle frozen (Cap.27.3 di Parte VI + hash SHA-256 valido al caricamento, Cap.35.2);
- (b) processa un feed di test (mock o storico recente, non feed live di mercato) e produce un payload bit-exact identico alla specifica di Cap.6.1 di Parte II Iterazione 4 (12 campi, Cap.27.4 di Parte VI);
- (c) pubblica messaggi Telegram di test conformi al layout mobile-first di Cap.29 di Parte VI;
- (d) la latenza end-to-end della catena ingest-feature-inference-Telegram rispetta il vincolo qualitativo $L_{max} = 30$ s (M-2 OPEN qualitativo di Cap.27.2 di Parte VI; verifica numerica empirica di $L_{max}$ effettivo resta carryover di Appendice E, decisione di scope (a) del Planner per CAP-07).

**AC-GO-11 — Dashboard Cap.30 di Parte VI operativa.** Verifica che la dashboard di monitoring live di Cap.30.6 di Parte VI è configurata e attiva con:
- (a) tracciamento di tutte le metriche live: $f_1^{live}, f_2^{live}, f_3^{live}, f_4^{live}$ (Cap.30.2), $f_5^{live}$ (Cap.30.3), $B(t)$ (Cap.30.4), $r_{emit}^{live}$ (Cap.30.5);
- (b) tutti gli alert configurati e testati: alert di deriva fitness (Cap.30.2), alert di deriva $f_5^{live}$ (Cap.30.3), alert di break parametrico EGARCH (Cap.30.4), alert di frequenza emissione fuori range (Cap.30.5);
- (c) reporting opzionale lifecycle aggiuntivo di Cap.30.3bis di Parte VI ($\pi_{t_2 \mid t_1}^{live}$, MFE, MAE, $f_{stop \mid t_1}^{live}$).

**AC-GO-12 — Hash bundle frozen valido.** Il bundle frozen del run corrente ha hash SHA-256 (Cap.35.2) **valido all'avvio della pipeline** di Cap.27.3 di Parte VI: il caricamento iniziale non produce errore di integrità. Riverifica del meccanismo di Cap.35.2 nel contesto del primo caricamento operativo.

**Decisione binaria GO / NO-GO.** Se **tutti i 12 AC** sono OK, si dichiara **GO**: il bundle frozen è promosso a produzione live e la pipeline di Cap.27 di Parte VI è attivata. Se **anche un solo AC** è NOT OK, si dichiara **NO-GO** con motivazione esplicita su quale AC è fallito + raccomandazione operativa:
- AC-GO-1, AC-GO-2 fallito $\to$ il bundle non passa i gate statistici; raccomandazione: re-applicazione del protocollo Parte V su nuovo storico oppure ritocco delle soglie $\theta_{DSR}, \theta_{PBO}$ (carryover ciclo successivo).
- AC-GO-3, AC-GO-4, AC-GO-5, AC-GO-6, AC-GO-7, AC-GO-8 fallito $\to$ la metrica operativa del bundle è insufficiente; raccomandazione: revisione del cromosoma vincente (selezione successiva dal fronte di Pareto $\mathcal{F}_1$ se altri cromosomi sopravvivono ai filtri 1-5 di Cap.31.2; altrimenti re-applicazione Parte V).
- AC-GO-9 fallito $\to$ il target operativo asimmetrico di Cap.1 di Parte I non è raggiunto sulla finestra OOS aggregata; raccomandazione: revisione del cromosoma o re-applicazione Parte V.
- AC-GO-10, AC-GO-11, AC-GO-12 fallito $\to$ problema infrastrutturale (pipeline, dashboard, hash bundle); raccomandazione: correzione tecnica del codice/setup prima del nuovo tentativo di go-live, senza re-training del GA.

### 36.2 Verifica aggregata di sessione e target operativo Cap.1 di Parte I

La verifica aggregata di sessione di AC-GO-9 opera sul fold OOS aggregato di Cap.31.1. Per ciascuna sessione $d$ del fold OOS aggregato (con $d \in \{1, \ldots, D\}$ e $D$ numero totale di sessioni della finestra OOS aggregata; per $F = 6$ atteso, $D \approx 6 \cdot 63 = 378$ sessioni a $W_{oos}/840 = 63$ sessioni per fold; per $F = 8$, $D \approx 504$ sessioni), si calcola il **target operativo asimmetrico** di Cap.1 di Parte I:

**(a) Soglia assoluta** $T_{abs}$: la sessione $d$ raggiunge il target assoluto se la somma dei rendimenti netti dei segnali eseguiti nella sessione è almeno 500 pt FIB:

$$T_{abs}(d) = \mathbb{1}\!\left[\sum_{i \in \mathcal{I}(d)} R_{net,i} \geq 500 \text{ pt FIB}\right]$$

dove $\mathcal{I}(d)$ è l'insieme degli indici dei segnali eseguiti emessi nella sessione $d$.

**(b) Soglia relativa** $T_{rel}$: la sessione $d$ raggiunge il target relativo se la somma dei rendimenti netti è almeno 70% del movimento strutturale intraday:

$$T_{rel}(d) = \mathbb{1}\!\left[\sum_{i \in \mathcal{I}(d)} R_{net,i} \geq 0{,}70 \cdot M_{structural,intraday}(d)\right]$$

dove $M_{structural,intraday}(d)$ è la **somma dei moduli degli swing strutturali** fra pivot ancorato al primo min/max post-apertura della sessione $d$ secondo Cap.1 di Parte I (definizione di movimento strutturale intraday, eredità in coerenza con Cap.15.3 di Parte III sull'algoritmo pivot detection frattale).

Il **target operativo asimmetrico** è raggiunto se **almeno una** delle due soglie è soddisfatta (condizione OR):

$$T(d) = T_{abs}(d) \lor T_{rel}(d)$$

La **percentuale di sessioni con target raggiunto** sul fold OOS aggregato è:

$$\rho_{sessions} = \frac{1}{D} \sum_{d=1}^{D} T(d)$$

AC-GO-9 è OK se $\rho_{sessions} > \theta_{sessions} = 0{,}60$ (provvisoria). $\theta_{sessions} = 0{,}60$ equivale al 60% delle sessioni che raggiungono almeno una delle due soglie, ordine di grandezza coerente con l'obiettivo del motore di Cap.1 di Parte I (target operativo asimmetrico come obiettivo realistico, non garanzia di copertura totale).

**Reporting per regime calmo / turbolento separato.** La percentuale $\rho_{sessions}$ è anche calcolata separatamente per le sessioni classificate come calmo (Cap.14 di Parte III) e turbolento, producendo due valori $\rho_{sessions}^{calmo}$ e $\rho_{sessions}^{turbolento}$. La differenza $|\rho_{sessions}^{calmo} - \rho_{sessions}^{turbolento}|$ è metrica di reporting (non gate AC binario), in coerenza con la separazione fra reporting di sessione e obiettivi NSGA-II di Cap.24.4 di Parte V (target di sessione è reporting, non obiettivo NSGA-II diretto).

### 36.3 Carryover dei 10 parametri di tuning operativo di Parte VI al post-go-live

Cap.36.3 dichiara esplicitamente, in coerenza con la **decisione di scope (c) del Planner per CAP-07**, che i 10 parametri di tuning operativo non congelati di Parte VI ($T_{recal,EGARCH}, \theta_B, T_{B,persist}, W_B, W_{prod}, T_{drift,persist}, T_{emit,persist}, \epsilon_p, N_{reg,\min}^{live}, \alpha_{f_5}$) **rimangono starting point con i default proposti di Parte VI per il primo run di produzione**. Nessun congelamento empirico in Parte VII.

**Motivazione esplicita.** I 10 parametri sono dichiarati in Parte VI come "non congelati in Parte VI, riconsiderati post-go-live" (preambolo Parte VI, riga 7); il loro congelamento empirico richiede **dati di produzione live** che il backtest OOS di Parte VII non possiede. Le metriche live di Cap.30 di Parte VI sono **counterpart live** delle metriche di Parte V e Parte VII (le distribuzioni di $f_1^{live}, f_2^{live}, \ldots, f_5^{live}$ sono confrontate con le distribuzioni cross-fold del walk-forward), ma il backtest OOS **non è produzione live**: non genera la distribuzione empirica degli alert, della frequenza di break parametrico EGARCH, della frequenza emissione $r_{emit}^{live}$ effettiva, della cardinalità dei regimi calmo/turbolento osservati in produzione. Parametri come $T_{drift,persist}, T_{emit,persist}, T_{B,persist}, \alpha_{f_5}, N_{reg,\min}^{live}, W_B, \epsilon_p$ dipendono dalla distribuzione empirica degli alert sulla pipeline live, non sui log di replay del backtest.

**Carryover esplicito al monitoring post-go-live.** La riconsiderazione empirica dei 10 parametri è attività di **monitoring post-go-live** a 3-6 mesi di produzione live, sulla base degli esiti empirici dei segnali emessi, della distribuzione degli alert e della rate di ricalibrazione EGARCH effettiva. Cap.36.3 dichiara questa separazione come carryover esplicito: **non è task di Parte VII**.

### 36.4 Regola di anticipo del ritraining su trigger di deriva

Eredità di Cap.30 di Parte VI alert + Cap.35.3 Regola 2. Cap.36.4 dichiara la **conseguenza operativa** della Regola 2 di sostituzione del bundle: se gli alert di Cap.30 di Parte VI scattano **in modo persistente** (definizione di "persistente" data dai parametri $T_{drift,persist}, T_{B,persist}, T_{emit,persist}$ di Parte VI, eredità della decisione di scope (c)), il ciclo di ritraining è **anticipato** rispetto alla cadenza pianificata trimestrale/semestrale.

La **regola di anticipo** opera su quattro trigger paralleli:

- **Trigger 1 — Deriva fitness** (Cap.30.2 di Parte VI): $\exists m \in \{1, 2, 3, 4\}: f_m^{live}(t)$ fuori dall'intervallo $[Q_1(f_{m,k}); Q_3(f_{m,k})]$ delle distribuzioni cross-fold di $f_m$ per $> T_{drift,persist}$ giorni consecutivi.
- **Trigger 2 — Deriva $f_5^{live}$** (Cap.30.3 di Parte VI): $f_5^{live}(t) > f_5^{global} \cdot (1 + \alpha_{f_5})$ per $> T_{drift,persist}$ giorni consecutivi.
- **Trigger 3 — Break parametrico EGARCH** (Cap.30.4 di Parte VI): $B(t) > \theta_B$ per $> T_{B,persist}$ barre consecutive (con $B(t)$ statistica di Nyblom 1989 di Cap.27.5 di Parte VI).
- **Trigger 4 — Frequenza emissione fuori range** (Cap.30.5 di Parte VI): $r_{emit}^{live}(t)$ fuori $[E_{min} = 0{,}2; E_{max} = 5]$ per $> T_{emit,persist}$ giorni consecutivi.

Se almeno uno dei trigger scatta in modo persistente, si attiva la **sostituzione anticipata** del bundle frozen via Cap.35.3 Regola 2. Il nuovo ciclo di ritraining produce un nuovo bundle frozen che sostituisce il bundle corrente alla prossima emissione post-transizione (gestione segnali `active` secondo Cap.35.3 Regola 1).

La regola di anticipo è **operativa, non di metodologia**: la metodologia (definizione dei trigger, formule degli alert) è in Parte VI; la conseguenza operativa (anticipo del ritraining) è in Cap.36.4. Il bundle frozen del ciclo corrente non si riottimizza in produzione: si **sostituisce con un nuovo bundle frozen** prodotto dal ciclo successivo.

### 36.5 Reporting finale del run Parte VII

Il run Parte VII produce un **report finale** del go-live, articolato come segue:

**(a) Tabella checklist Cap.36.1.** Tabella dei 12 AC binari (AC-GO-1 .. AC-GO-12) con: criterio, valore numerico calcolato, soglia, esito (OK / NOT OK), motivazione (se NOT OK).

**(b) Tabella metriche aggregate con intervalli di confidenza bootstrap.** Le 13 metriche di Cap.34.3 ($DSR, PBO, f_1$-$f_5, \pi_{t_2|t_1}, \text{MFE}_{agg}, \text{MAE}_{agg}, f_{stop|t_1}, \text{CVaR}_{95\%}, \text{MDD}_{intraday}$) con: valore puntuale, intervallo di confidenza al 95% bootstrap (percentile method o BCa), unità di misura (pt FIB, frazione, ecc.).

**(c) Tabella chiusura tre decisioni condizionali di Cap.31.3.** Rapporti $r_{FG}, r_{CV}, r_{Schoenfeld}$ con valore numerico e scelta adottata (`cox_model_type`, `cox_stratification`, `cox_time_varying_active`).

**(d) Tabella chiusura M-5 e Cap.26.3-26.4 di Parte V di Cap.31.4.** Rapporti di fold per ciascuna candidata (window EGARCH, distribuzione $D$, opzione di inizializzazione) con scelta adottata (`egarch_window`, `egarch_distribution`, `egarch_init_option`).

**(e) Bundle frozen artifact.** Identificazione del bundle: `bundle_id`, `bundle_hash` (esadecimale 64 caratteri), `F_effective`, `compute_instance`, `timestamp_freezing`, `code_version`.

**(f) Decisione finale.** **GO** se tutti i 12 AC sono OK; **NO-GO** con motivazione esplicita su AC falliti + raccomandazione operativa per il ciclo successivo.

Il report finale è archiviato come **output canonico** del run Parte VII, in coerenza con il vincolo di tracciabilità di Cap.10 di Parte II. Una copia del report è inclusa nel pacchetto di deployment del bundle frozen, per audit retrospettivi e analisi longitudinali della catena `bundle_history`.

I parametri di tuning provvisori introdotti in Cap.36 sono $\theta_{CVaR} = -100$ pt FIB, $\theta_{MDD} = 200$ pt FIB, $\theta_{sessions} = 0{,}60$, dichiarati non congelati in Parte VII. Tutti i numeri della checklist Cap.36.1 rispettano il tick FIB di 5 pt nei livelli di prezzo (i valori in pt FIB, $-100$ e $200$, sono multipli di 5; le soglie adimensionali, $0{,}60$ ecc., non hanno unità di prezzo). Le citazioni esplicite di Cap.36 richiamano Cap.5 di Parte I (definizione operativa del successo, eredità 9), Cap.1 di Parte I (target operativo asimmetrico, eredità 10), Cap.2 di Parte I (profilo operatore retail mobile), Cap.24.1-24.2 di Parte V ($f_1$-$f_5$ + $E_{min}, E_{max}$), Cap.27 di Parte VI (pipeline operativa), Cap.30 di Parte VI (dashboard + alert), Cap.31-35 (gate e bundle), Appendice E (M-2 OPEN $L_{max}$ Telegram).

Il **registro di criteri di successo** di Parte VII chiude la **definizione operativa del successo** di Cap.5 di Parte I come checklist verificabile: i 12 AC binari di Cap.36.1, applicati al bundle frozen del run corrente, decidono in modo deterministico la promozione del bundle a produzione live, completando il passaggio da fronte di Pareto $\mathcal{F}_1$ a bundle operativo unico.

---

**Conclusione della Parte VII.** La Parte VII converte il fronte di Pareto $\mathcal{F}_1$ prodotto dal NSGA-II di Parte V in **un bundle frozen specifico** identificato univocamente dall'hash SHA-256 di Cap.35.2 e promosso a produzione live attraverso la **checklist binaria** dei 12 AC di Cap.36.1. La selezione del bundle è **deterministica e lessicografica** (Cap.31.2), la validità statistica è verificata dal **DSR di Bailey-López de Prado 2014** (Cap.32) e dalla **PBO via CSCV di Bailey-Borwein-López de Prado-Zhu 2017** (Cap.33), gli intervalli di confidenza sulle metriche aggregate sono prodotti dal **bootstrap stazionario di Politis-Romano 1994** con block length adattiva via Politis-White 2004 (Cap.34), il bundle è congelato come **artefatto immutabile** con regole di sostituzione esplicite (Cap.35), il go-live è autorizzato dalla **decisione binaria GO/NO-GO** (Cap.36). Tre decisioni condizionali del walk-forward di Parte V (Cox vs Fine-Gray, stratificazione vs interaction term, time-varying coefficients M-16) si chiudono in Cap.31.3 sulla base del rapporto di fold; M-5 (window EGARCH), Cap.26.3 di Parte V (distribuzione $D$), Cap.26.4 di Parte V (opzione di inizializzazione) si chiudono in Cap.31.4 con la stessa regola di rapporto. La riconsiderazione di $\theta_{CV} = 0{,}50$ di Cap.25.5 di Parte V e di $K_{max}^{strict} = 4$ Harrell-strict di Cap.26.7 di Parte V resta carryover esplicito al ciclo successivo (Cap.31.5). Il congelamento empirico dei 10 parametri di tuning operativo di Parte VI resta carryover al monitoring post-go-live a 3-6 mesi di produzione live (Cap.36.3). Il documento metodologico v2 si conclude con la Parte VII come gate finale: tutte le decisioni metodologiche rinviate alle Parti precedenti trovano qui la regola di decisione.
