# TASK ATTIVO: CAP-05 -- Parte V del documento metodologico v2 (Motore genetico, fitness operativa, walk-forward, calibrazione)

**Assegnato da**: Planner
**Output atteso**: `docs/methodology_v2/CAP_05_parte_V.md`
**Stato**: NUOVO

## Obiettivo

Scrivere la Parte V del documento metodologico v2: **Motore genetico strutturale, fitness multi-obiettivo, walk-forward nested con purge ed embargo, calibrazione di popolazione/generazioni/criteri di stop, congelamento numerico dei parametri provvisori delle Parti precedenti**. Questa Parte risponde a: (1) come si rappresenta lo spazio di ottimizzazione (cromosoma del bundle, vincoli di ammissibilita') e quali gradi di liberta' geometrici/probabilistici di Parte II-IV diventano geni ottimizzati dal GA; (2) come opera l'algoritmo genetico (NSGA-II con elitismo, crossover, mutazione, gestione dei vincoli) e che cosa giustifica analiticamente il budget di valutazioni dichiarato in CAP-01 (range 12.800-25.600 min single-thread, M-4); (3) come e' definita la fitness multi-obiettivo che guida la selezione (expected net return per segnale eseguito, target hit rate, invalidation rate, drawdown, penalita' per emissione eccessiva o nulla); (4) come si articola il walk-forward nested con purge ed embargo che protegge dalla leakage tempo-correlata (regola di rolling/expanding/EWMA con benchmark Inoue-Rossi 2011 e criterio di rollback automatico M-5; classificazione di regime per fold M-6; stratificazione del Cox per regime M-14; verifica empirica del censoring non-informativo M-7+M-8; benchmark Cox cause-specific vs Fine-Gray M-9; test Schoenfeld per hazard proporzionali M-10; dimensionalita' massima del vettore feature survival M-11); (5) come e perche' la popolazione e' fissata a 128 individui e le generazioni a 150, quali criteri di convergenza e di stop si adottano, quale e' la cadenza di ricalibrazione fra fold (regime, M-2 v2); (6) il **congelamento numerico** dei parametri provvisori delle Parti precedenti, con tabella esplicita prima/dopo (parametri del modello e del cromosoma) e impatto atteso sul comportamento del GA. Il congelamento di Parte V include anche i parametri trade_range $A_{range,min}=80$, $N_{osc}$, $n_{osc,min}$, $\epsilon_{osc}$, $N_{break}$, $\delta_{break}$ e le soglie delle 4 condizioni di classificazione (M-15).

La Parte V non contiene la pipeline di inference real-time (Parte VI), la validazione OOS finale con DSR/PBO/bootstrap stazionario e i gate decisionali di go-live (Parte VII), ne' le specifiche di interfaccia (Appendici C-D-E). La Parte V consuma tutti i blocchi formali delle Parti I-IV come input: payload e state machine del segnale (Parte II); fill virtuale worst-case, EGARCH(1,1), regime calmo/turbolento, catalogo 37 feature, algoritmo pivot detection con 4 condizioni e $n_c=3$/$\delta_{pivot}=10$ pt (Parte III); geometria zone con $p_{ref}$ dal pivot piu' recente per timestamp di conferma, target_1 strutturale o ammissibile $\geq 80$ pt, target_2 strutturale o sintetico, stop strutturale o sintetico (sigma fallback), modello survival Cox cause-specific su feature $\tilde{\mathbf{x}}$ con censoring non-informativo dichiarato condizionatamente alle covariate, filtri Cap.20, caso trade_range con feature condizionale $x^{(A_{range})}$ (Parte IV).

**Impatto sul GA**: la Parte V e' il motore stesso. Il cromosoma definito qui (Cap.22) determina lo spazio in cui il GA ottimizza; gli operatori di Cap.23 determinano la velocita' di convergenza; la fitness di Cap.24 determina cosa significa "buono" per il sistema; il walk-forward di Cap.25 determina su quali dati si misura "buono" senza leakage; la calibrazione di Cap.26 determina quando ci si ferma. Senza Parte V, nessun bundle frozen puo' essere prodotto e il sistema non ha policy operativa di emissione segnali: tutte le parti precedenti restano vincoli formali senza un algoritmo di selezione.

## Eredita' obbligatoria da CAP-01, CAP-02, CAP-03, CAP-04

Tutte le eredita' qui elencate devono essere citate esplicitamente almeno una volta nei capitoli di Parte V che le consumano. La mancata citazione in un capitolo pertinente e' un finding di Review.

### Da CAP-01 (Parte I, Q-01..Q-04 chiuse + vincoli operatore)

1. **Sessione operativa 8:00-22:00 CET**, finestra unica e continua, 840 barre/sessione (Q-01). Il walk-forward (Cap.25) opera su sessioni intere; nessun fold puo' frazionare una sessione.
2. **Target operativo asimmetrico**: 500 pt FIB profitto netto/giorno OR 70% movimento strutturale intraday (somma moduli swing fra pivot, ancorato al primo min/max post-apertura 8:00 CET, Q-02). Il movimento strutturale e' input alla fitness multi-obiettivo (Cap.24) come scaler per misurare la quota di profitto catturato.
3. **Parametri GA di lavoro** dichiarati provvisori in CAP-01: popolazione 128 individui, generazioni 150, schema walk-forward nested con purge+embargo, bootstrap stazionario B=2000 (Q-03). La Parte V valuta empiricamente questi valori e li **congela** o li corregge documentando lo scostamento.
4. **Cap 2 giorni di trading** dal raw touch per $\Delta t_{cromosoma} \in \{1,\ldots,1680\}$ minuti (Q-04). Lo spazio del cromosoma di Cap.22 include $\Delta t_{cromosoma}$ con questo dominio discreto.
5. **Tick FIB = 5 punti** (tutti i livelli sono multipli di 5). Ogni esempio numerico, ogni dominio di parametro a unita' di prezzo, ogni soglia di Cap.24-26 rispetta questo vincolo.
6. **Filtro emissione $\geq 80$ pt** su target_1 directional, ampiezza $A_{range} \geq 80$ pt per trade_range (Cap.5 Parte I). Vincolo assoluto non allentabile dal cromosoma; cromosomi violanti sono non validi.
7. **Banda $b \in \{5,10,15,20,25,30,35,40\}$ pt**, $b_{min}=5$ provvisorio; vincolo $d_{stop}>b$ obbligatorio (Cap.6 Parte II). Cromosomi violanti sono non validi e non entrano nella popolazione del GA.
8. **DSR e PBO come gate primari di accettazione** (Cap.5 Parte I). Soglie e procedura operativa sono materia di Parte VII; Parte V dichiara che la fitness aggrega le metriche di lifecycle/rischio ma non incorpora DSR/PBO come obiettivi diretti (questi sono gate post-selezione).
9. **Compute budget cloud AWS c5.4xlarge**, range training stimato 21.000-41.500 min single-thread (Cap.4 Parte I). Parte V deve giustificare con derivazione esplicita il range effettivo del numero di valutazioni di fitness e produrre la stima compute aggiornata coerente con il valore stimato in CAP-01 (M-4).

### Da CAP-02 (Parte II, Q-05 chiusa)

10. **Payload del segnale** (Cap.6.1, esteso in Iterazione 4-5): tupla $\mathcal{S}$ con `signal_id, timestamp_emission, direction, entry_zone, target_1, target_2, target_2_type` $\in\{\text{structural, synthetic}\}$, `stop_loss, stop_type` $\in\{\text{structural, synthetic}\}$, `setup_class` $\in\{\text{directional, trade\_range}\}$, $\Delta t_{cromosoma}$, $T_{touch}^{max}$. Cap.22 esplicita quali campi del payload sono ottimizzati dal cromosoma (es. $b$ via geometria, $\Delta t_{cromosoma}$, $T_{touch}^{max}$ direttamente) vs derivati deterministicamente da $p_{ref}$ e geometria (es. `target_1, target_2, stop_loss, target_2_type, stop_type`).
11. **Vincolo segnale unico attivo** $|\mathcal{A}(t)| \leq 1$ (Cap.6.3). La fitness di Cap.24 valuta sequenze di segnali singoli sostituiti, non politiche multi-segnale concorrente.
12. **State machine 1 non-terminale + 6 terminali**, `target_1_hit` chiude il contratto (Q-05 Clausola 1). La fitness di Cap.24 valuta gli stati terminali del segnale e i metric della submacchina position lifecycle (Cap.11 Parte II) per target_2 hit rate condizionale $\pi_{t_2|t_1}$.
13. **Condizioni di emissione AND logico**: $E_{vol} \land E_{liq} \land E_{dist}^{\sigma} \land E_{80pt} \land E_{surv}$ (Cap.8 Parte II + Cap.20 Parte IV). Il cromosoma ottimizza $\tau_{vol}(\cdot)$, $\tau_{liq}$, $\tau_{dist}^{\sigma}$, $\tau_{surv}$ (e le varianti regime-dipendenti).
14. **Position lifecycle submacchina post-target_1** (Cap.11): traccia $\pi_{t_2|t_1}$, MFE, MAE, stop post-target_1. Questi indicatori entrano nella fitness di Cap.24 come metrica di calibrazione, non come obiettivi diretti di selezione (out-of-scope dal contratto del segnale).
15. **Replay deterministico bit-exact** (Cap.10 Parte II). Ogni valutazione di fitness in Cap.24 ed ogni stima del survival in Cap.25 sono deterministiche dato seed e bundle.
16. **Pubblicazione su Telegram, 9 voci ordinate** (Cap.9.2 esteso Iterazione 5). Nessun impatto diretto sul GA, ma il cromosoma non puo' produrre payload con campi mancanti.

### Da CAP-03 (Parte III)

17. **EGARCH(1,1) con distribuzione $D \in \{\text{Student-}t, \text{GED}\}$** (Cap.13.1-13.2). La scelta della distribuzione $D$ e' **decisione di Parte V via AIC/BIC** sulla finestra di calibrazione (Cap.13.2 rinvia esplicitamente a Parte V). Parte V deve includere il protocollo di selezione (criterio decisionale + tie-break) e l'esito provvisorio sulla finestra di lavoro Portara/CQG.
18. **Finestra di calibrazione EGARCH $W = 210.000$ barre rolling** provvisoria (Cap.13.3, M-5). Parte V deve includere il **benchmark rolling vs expanding vs EWMA con test Inoue-Rossi (2011)** e definire il **criterio di rollback automatico** se rolling $W=210.000$ non domina almeno un'alternativa su metrica OOS congelata. La regola di rollback e' parte normativa di Cap.25.
19. **Cadenza ricalibrazione EGARCH fold-per-fold** del walk-forward (Cap.13.3 + M-2 v2). Parte V articola la cadenza dentro il walk-forward di Cap.25; la cadenza in **inference live (production)** resta in Parte VI -- la separazione e' dichiarata esplicitamente.
20. **Inizializzazione cross-session Opzione A o B** del EGARCH (Cap.13.5). Scelta in Parte V via diagnostica residui e stabilita' stima nelle prime barre. Cap.26 riporta l'esito e congela.
21. **Floor $\tau_{vol,low}$ sulla coda bassa della volatilita'** (Cap.13.6, N-5). Parametro provvisorio del modello, congelato in Cap.26 sulla base dell'analisi empirica.
22. **Classificazione regime calmo/turbolento** binaria deterministica, $\bar{\sigma}_s$ media di sessione baseline, mediana benchmark di robustezza, $p=0{,}75$, $N_{reg}=20$ sessioni, $T_{persist}=10$ barre (Cap.14). Parte V tratta esplicitamente media vs mediana con test di stabilita' (M-6); congelamento di $p$, $N_{reg}$, $T_{persist}$ in Cap.26.
23. **Catalogo 37 feature causali normalizzate $\tilde{\mathbf{x}}_t$** (Cap.15.2): 4 categorie (prezzo, volume, volatilita', struttura), vincolo $x_t \in \mathcal{F}_{t-1}$, normalizzazione z-score MAD con $W_{norm}=1000$ e $T_{warmup,\text{norm}}=100$. Cap.22 (cromosoma) specifica come il GA seleziona il sottoinsieme di feature per il survival.
24. **Algoritmo pivot detection 4 condizioni** con $n_c=3$, $\delta_{pivot}=10$ pt provvisori, $N_{pivot}=30$ valore di lavoro (Cap.15.3). Congelamento in Cap.26 con misura empirica della distribuzione effettiva di $N_{pivot}$ sullo storico.
25. **EMA $\lambda=0{,}94$**, $T_{warmup,\text{EMA}}=74$ derivato dalla formula $\lceil \ln(0{,}01)/\ln(\lambda) \rceil$ (Cap.15.2.1). Parte V congela $\lambda$ via diagnostica residui; $T_{warmup,\text{EMA}}$ resta funzione di $\lambda$.

### Da CAP-04 (Parte IV)

26. **Algoritmo selezione $p_{ref}$ via timestamp di conferma del pivot** (Cap.16.1, fix NB-1 v2). Cap.22 (cromosoma) parametrizza $b$ ma NON $p_{ref}$: $p_{ref}$ e' derivato deterministicamente dai pivot confermati, non e' un gene.
27. **Sospensione emissione in warm-up strutturale** (Cap.16.2, M-1 v2 CAP-03): se $\mathcal{P}_{low}(t)=\emptyset$ (long) o $\mathcal{P}_{high}(t)=\emptyset$ (short), niente segnale. Cap.22 non ammette cromosomi che bypassano questa regola; il vincolo e' strutturale.
28. **Invalidazione pre-touch** I1 (stop attraversato), I2 ($d_{inv}$), I3 ($d_{obsolete}$, nuovo pivot) (Cap.16.5). I parametri $d_{inv}$, $d_{obsolete}$ sono geni del cromosoma, dominio multipli di 5 pt $\geq 5$.
29. **Condizione tempo residuo minimo $T_{min,session}$** (Cap.16.6). Gene del cromosoma, dominio interi positivi $\geq 15$ min, valore provvisorio 30 min.
30. **target_1: pivot piu' prossimo nella direzione, ridefinito al primo livello $\geq 80$ pt se necessario** (Cap.17.1-17.2). Cap.22 specifica che target_1 e' derivato (non e' gene). $\tau_{dist}^{\sigma}$ e' gene del cromosoma (Cap.17.3).
31. **target_2: pivot oltre target_1 o livello sintetico $\texttt{target\_1} \pm k_{t2} \cdot \hat{\sigma}_{\text{pt}}$, $k_{t2}$ gene cromosoma, valore provvisorio 2** (Cap.17.4). Congelamento $k_{t2}$ in Cap.26.
32. **stop_loss: pivot in direzione avversa con $d_{stop}>b$, o fallback sigma $\texttt{stop\_loss}^{(\sigma)} = p_{ref} \mp d_{stop,\sigma} \cdot \hat{\sigma}_{\text{pt}}$, $d_{stop,\sigma}$ gene cromosoma, valore provvisorio 3** (Cap.18.1-18.2). Eventuali varianti regime-dipendenti $d_{stop,\sigma,\text{calmo}}$, $d_{stop,\sigma,\text{turbolento}}$ sono geni opzionali (Cap.18.5). Cap.22 dichiara la struttura del gene (uno o due valori per regime).
33. **Risk-reward ratio strutturale $\text{RR} = d_{target}/d_{stop}$** osservabile, eventuale floor/cap rinviato a Parte V (Cap.18.4). Parte V decide se introdurre il vincolo (es. $\text{RR} \geq 1$) sulla base dell'evidenza empirica; la decisione e' in Cap.26.
34. **Modello survival Cox cause-specific** $h_j(\tau|\mathbf{x},T_{residuo}) = h_{0,j}(\tau) \cdot \exp(\boldsymbol{\beta}_j^\top \mathbf{x} + \gamma_j T_{residuo})$ con $j\in\{1,2\}$ (target_1_hit vs stopped) (Cap.19.2). Calibrazione fold-per-fold su finestra in-sample, censoring a destra a $\tau=\Delta t_{cromosoma}$, output $\hat{p}_{hit}$ (Cap.19.4-19.5).
35. **Censoring non-informativo condizionato a $\tilde{\mathbf{x}}_t$** dichiarato in Cap.19.4 (chiusura O-5/M-7 v2; razionale (a) rimosso in NB-v2-3 v3). Verifica empirica via residui di Cox-Snell e Schoenfeld stratificato e' demandata a Parte V (M-7+M-8). Parte V deve eseguire la verifica e registrare l'esito nel log di calibrazione del fold.
36. **Benchmark Cox cause-specific vs Fine-Gray sub-distribution** (M-9). Cap.25 implementa il benchmark e ne riporta gli esiti come criterio di robustezza, senza scartare il Cox primario se non a vantaggio empirico significativo.
37. **Test Schoenfeld per hazard proporzionali** [Grambsch-Therneau 1994] (Cap.19.4 + M-10). Cap.25 esegue il test fold-per-fold, registra l'esito nel log di calibrazione, segnala estensione a hazard non-proporzionali se violazione sistematica.
38. **Stratificazione del Cox per regime calmo/turbolento** -- interaction term vs stratificazione formale -- (M-14, materia di Parte V). Cap.25 decide la forma di condizionalita' al regime (a) regime come feature aggiuntiva di $\tilde{\mathbf{x}}$, oppure (b) stratificazione del Cox separatamente per calmo e turbolento con baseline hazard distinte (Cap.19.2 Parte IV rinvia esplicitamente a Parte V).
39. **Dimensionalita' massima del vettore $\tilde{\mathbf{x}}$ del survival** (M-11). Cap.22 specifica il sotto-spazio del cromosoma che codifica la selezione feature; Cap.26 congela la dimensionalita' massima sulla base del rischio di overfitting (Cap.19.3 Parte IV rinvia).
40. **Soglia $\tau_{surv} \in (0{,}1; 0{,}9)$**, valore provvisorio 0{,}5, regime-dipendente opzionale (Cap.20.1-20.3). Gene del cromosoma; congelamento del dominio operativo in Cap.26.
41. **Filtro implicito fine sessione via $T_{residuo}$** (Cap.20.4). Nessun parametro aggiuntivo; verifica empirica del meccanismo come stress test in Cap.24-25.
42. **Trade_range con feature condizionale $x^{(A_{range})}$** (Cap.21.5, chiusura O-4/M-13 v2). Cap.22 dichiara: catalogo globale del cromosoma per regime directional = 37 feature; vettore $\tilde{\mathbf{x}}_{\text{trade\_range}}$ = $\tilde{\mathbf{x}} \cup \{x^{(A_{range})}\}$ in regime trade_range. La feature non e' nel catalogo principale (M-15).
43. **Parametri trade_range classificazione**: $A_{range,min}=80$ pt (vincolo assoluto, non ottimizzabile); $N_{osc}=60$ barre, $n_{osc,min}=2$, $\epsilon_{osc}=5$ pt, $N_{break}=20$, $\delta_{break}=10$ pt (provvisori) (Cap.21.2). Congelamento numerico in Cap.26 sulla base dell'analisi empirica (M-15).
44. **Tabella riepilogo parametri provvisori di Parte IV** (Cap.21 fine documento): $d_{inv}, d_{obsolete}, T_{min,session}, k_{t2}, d_{stop,\sigma}$ (e varianti regime), $\tau_{surv}$ (e varianti regime), $N_{osc}, n_{osc,min}, \epsilon_{osc}, N_{break}, \delta_{break}$. Cap.26 produce la tabella analoga di Parte V con valori congelati e motivazione.

## M-promemoria censiti pertinenti CAP-05

L'Orchestratore della sessione corrente verifica che ogni M-promemoria sotto sia trattato esplicitamente nel capitolo indicato. Un M-promemoria pertinente a CAP-05 non integrato nel Development e' un finding di Review.

| M-ID | Origine | Contenuto | Pertinenza CAP-05 |
|------|---------|-----------|-------------------|
| M-2 | Review v1 CAP-02 | Verifica empirica latenza Telegram $L_{max}=30$s | NO -- resta carryover Appendice E |
| M-4 | Review v4 CAP-01 | Tasso di rimpiazzo NSGA-II che giustifica baseline 12.800-25.600 min | **SI'** -- Cap.23 (operatori NSGA-II): formula del tasso di rimpiazzo + derivazione analitica del range; benchmark empirico vero proprio resta Parte VII |
| M-5 | Review v1 CAP-03 (Q-06 / C-4.3) | Benchmark rolling vs expanding vs EWMA con test Inoue-Rossi (2011); criterio di rollback automatico | **SI'** -- Cap.25 (window selection del walk-forward): protocollo benchmark + criterio di rollback normativo |
| M-6 | Review v1 CAP-03 (Q-09 / C-7.3) | Classificazione regime media vs mediana; test di stabilita' con soglia da definire | **SI'** -- Cap.25 (gestione regime nel walk-forward): test parallel media-mediana, soglia di "cambiamento significativo" definita |
| M-2 v2 CAP-03 | Review v2 CAP-03 | Cadenza ricalibrazione EGARCH in production | **SI' (parziale)** -- Cap.25 tratta la cadenza nel walk-forward; la cadenza in production resta Parte VI. La separazione e' dichiarata esplicitamente |
| M-7 | Review v1 CAP-04 (O-5) | Censoring informativo nel Cox cause-specific: verifica dell'assunzione (indipendenza censoring/evento) | **SI'** -- Cap.25 (diagnostica survival fold-per-fold): test residui Cox-Snell + Schoenfeld stratificato per evento vs censoring |
| M-8 | Developer CAP-04 | Verifica empirica del censoring non-informativo nel survival | **SI'** -- congruente con M-7, raggruppato in Cap.25 sotto-sezione "diagnostica survival" |
| M-9 | Developer CAP-04 | Benchmark Cox cause-specific vs Fine-Gray sub-distribution | **SI'** -- Cap.25 sotto-sezione "benchmark modelli survival" |
| M-10 | Developer CAP-04 | Test Schoenfeld per assunzione hazard proporzionali | **SI'** -- Cap.25 sotto-sezione "diagnostica hazard proporzionali" |
| M-11 | Developer CAP-04 | Dimensionalita' massima del vettore feature $\tilde{\mathbf{x}}$ nel survival | **SI'** -- Cap.22 (struttura del cromosoma): dichiarazione dello spazio di selezione delle feature survival; Cap.26 congela la dimensionalita' massima |
| M-14 | Developer CAP-04 | Stratificazione del Cox per regime calmo/turbolento (interaction term o stratificazione formale) | **SI'** -- Cap.25 sotto-sezione "Cox condizionale al regime": decisione fra interaction term e stratificazione formale, motivata e congelata |
| M-15 | Developer CAP-04 | Parametri trade_range $A_{range,min}=80$, $N_{osc}$, $n_{osc,min}$, $\epsilon_{osc}$, $N_{break}$, $\delta_{break}$ e le soglie delle 4 condizioni di classificazione: congelamento numerico | **SI'** -- Cap.26 (calibrazione): tabella riepilogo parametri trade_range con valori congelati; $A_{range,min}=80$ resta vincolo assoluto non ottimizzabile (Cap.5 Parte I) |
| N-2 (v1) | Review v1 CAP-02 | Netto non registrato nel log di chiusura | NO -- carryover Parte VII |
| N-3 (v1) | Review v1 CAP-02 | `executable_rate` nomenclatura post-eliminazione guardie | **SI'** -- Cap.24 (fitness): nomenclatura definitiva e formule chiuse delle metriche di lifecycle, allineate a CAP-01 post-patch Iterazione 2 |
| N-4 (v2) | Review v2 CAP-02 | Log chiusura: $\Delta t$ pre-trigger non esplicitato come campo | **SI'** -- Cap.24 (replay deterministico nel walk-forward): il log della valutazione di fitness deve includere $\Delta t$ pre-trigger separatamente da $\Delta t_{cromosoma}$ |
| N-5 (v2) | Review v2 CAP-02 | Coda bassa volatilita': floor $\tau_{vol,low}$ | **SI'** -- Cap.26 (calibrazione): congelamento di $\tau_{vol,low}$ sulla base dell'analisi empirica di Cap.13.6 Parte III |
| N-1 (v2 CAP-03) | Review v2 CAP-03 | Asimmetria tracking stopped vs target_*_hit (MFE post-stop) | **SI'** -- Cap.24 (fitness): la submacchina di position lifecycle (Cap.11 Parte II) traccia MFE/MAE post-target_1; eventuale tracking post-stop e' fuori scope (lo stop e' terminale del segnale, no submacchina post-stop) -- dichiarazione esplicita |

### Decisioni di scope del Planner sui M-promemoria

Tre decisioni di scope sono prese qui dal Planner per evitare ambiguita' nel Development:

**(a) Trattamento dei M-promemoria survival in Cap.25 (no Cap.25bis).** Mantengo il numero di capitoli a 5 (Cap.22-26) come da scope indice. M-7, M-8, M-9, M-10, M-14 sono raggruppati come **sotto-sezioni di Cap.25** "walk-forward + diagnostica survival fold-per-fold". Lo splitting in capitoli separati produrrebbe un Cap.25bis ridondante e una Parte V di lunghezza eccessiva rispetto alle ~10 pagine target. La struttura attesa di Cap.25 e' (a) schema walk-forward nested con purge+embargo (~0,7 pp); (b) window selection EGARCH (M-5) (~0,4 pp); (c) classificazione regime nel walk-forward (M-6) (~0,3 pp); (d) Cox condizionale al regime (M-14) (~0,3 pp); (e) diagnostica survival fold-per-fold: censoring non-informativo via Cox-Snell + Schoenfeld stratificato (M-7+M-8) (~0,3 pp); (f) benchmark Cox vs Fine-Gray (M-9) (~0,2 pp); (g) test Schoenfeld hazard proporzionali (M-10) (~0,2 pp); (h) cadenza ricalibrazione nel walk-forward + rinvio production a Parte VI (M-2 v2) (~0,1 pp). Totale Cap.25 ~2,5 pp.

**(b) Collocazione M-15 (congelamento parametri trade_range) in Cap.26.** I parametri $A_{range,min}, N_{osc}, n_{osc,min}, \epsilon_{osc}, N_{break}, \delta_{break}$ sono **parametri del modello** non del cromosoma (Cap.21.2 Parte IV li dichiara esplicitamente come "parametri del modello"); il loro congelamento appartiene quindi a Cap.26 (calibrazione/congelamento). Cap.22 li cita ma non li include nel genoma. **Eccezione esplicita**: $A_{range,min}=80$ resta vincolo assoluto di filtro emissione (Cap.5 Parte I, Cap.6.1 Parte II), non ottimizzabile e non congelabile (e' un dato di input normativo).

**(c) Separazione M-2 v2 fra Parte V e Parte VI.** Cap.25 tratta la **cadenza di ricalibrazione EGARCH dentro il walk-forward** (fold-per-fold, gia' dichiarata in Cap.13.3 Parte III). La **pipeline operativa di re-fitting in production** (cadenza di ricalibrazione del bundle frozen in live, gestione dei break parametrici in real-time, trigger di re-training) resta materia di Parte VI Cap.27. La separazione e' dichiarata esplicitamente nel testo di Cap.25 con un paragrafo dedicato.

## Capitoli da produrre (~10 pagine totali in italiano formale)

### Capitolo 22 -- Cromosoma e spazio dei parametri (~2 pp)

**Scope.** Definire formalmente il cromosoma del bundle: la struttura del genoma, lo spazio dei parametri (continuo, discreto, condizionato al regime), i vincoli rigidi di ammissibilita', l'encoding adottato per gli operatori del GA.

**Contenuto obbligatorio.**

- **22.1 Definizione del cromosoma**: il cromosoma $\theta$ del bundle e' una tupla strutturata che codifica tutti i parametri ottimizzabili del motore. Specificare per ogni gene: simbolo, dominio, semantica, capitolo di provenienza (Parte II-IV), regime-dipendenza (uno o due valori).
- **22.2 Geni geometrici (Parti II-IV)**: $b$ (banda, $\{5,10,15,20,25,30,35,40\}$ pt -- eredita' 7), $d_{inv}$ (multipli di 5 pt $\geq 5$ -- eredita' 28), $d_{obsolete}$ (multipli di 5 pt $\geq 5$ -- eredita' 28), $T_{min,session}$ (interi positivi $\geq 15$ min -- eredita' 29).
- **22.3 Geni di emissione (Parte II + IV)**: $\tau_{vol}(\cdot)$ funzione parametrica di $\hat{\sigma}_{\text{pt}}$ (forma funzionale: lineare, esponenziale o costante a tratti -- decisione di Parte V), $\tau_{liq}$ (soglia volume, dominio $\mathbb{R}^+$), $\tau_{dist}^{\sigma}$ (sigma-units FIB, $\mathbb{R}^+$ -- eredita' 30 + 13), $\tau_{surv}$ (eredita' 40, $(0{,}1; 0{,}9)$). Per ciascuno: dichiarare se e' regime-dipendente (gene unico vs due geni per regime calmo/turbolento). Default: $\tau_{vol}$ e $\tau_{surv}$ regime-dipendenti opzionali; $\tau_{liq}$, $\tau_{dist}^{\sigma}$ singolo per default.
- **22.4 Geni target/stop (Parte IV)**: $k_{t2}$ (moltiplicatore sigma per target_2 sintetico, $\mathbb{R}^+$ -- eredita' 31), $d_{stop,\sigma}$ (moltiplicatore sigma per stop sintetico, $\mathbb{R}^+$ -- eredita' 32), eventuali varianti regime-dipendenti $d_{stop,\sigma,\text{calmo}}, d_{stop,\sigma,\text{turbolento}}$.
- **22.5 Geni temporali (Parte II)**: $\Delta t_{cromosoma}$ (interi in $\{1,\ldots,1680\}$ minuti di trading -- eredita' 4), $T_{touch}^{max}$ (interi in $\{5,\ldots,480\}$ -- eredita' Cap.6.1 Parte II $T_{touch}^{max}$).
- **22.6 Geni di selezione feature survival (M-11)**: il cromosoma include un vettore binario $\mathbf{s} \in \{0,1\}^{37}$ che codifica l'inclusione/esclusione di ciascuna feature del catalogo (Cap.15.2 Parte III) come predittore del Cox. Dichiarare la dimensionalita' massima $K_{max} \leq 37$ del numero di feature attive ($\sum s_j \leq K_{max}$) come parametro del modello, congelato in Cap.26 sulla base dell'analisi del rischio di overfitting. Per setup `trade_range`, la feature condizionale $x^{(A_{range})}$ e' attiva di default (non codificata in $\mathbf{s}$, e' aggiunta dal modello al vettore $\tilde{\mathbf{x}}_{\text{trade\_range}}$ -- eredita' 42).
- **22.7 Vincoli di ammissibilita'**: enumerare i vincoli rigidi che squalificano un cromosoma dalla popolazione: (a) $d_{stop} > b$ (eredita' 7); (b) target_1 ammissibile $\geq 80$ pt directional, $A_{range} \geq 80$ pt trade_range (eredita' 6); (c) $d_{stop,\sigma,\text{turbolento}} \geq d_{stop,\sigma,\text{calmo}}$ opzionale (eredita' 32); (d) $K_{max}$ vincolo sulla cardinalita' di feature attive (22.6); (e) tutti i parametri a unita' di prezzo multipli di 5 (eredita' 5). Specificare cosa fa il GA quando un cromosoma e' non valido: scarto immediato + sostituzione via mutazione random vincolata.
- **22.8 Encoding per gli operatori del GA**: scelta dell'encoding (binario fisso vs real-valued vs mixed). Decisione di Parte V: encoding **misto** -- variabili continue ($\tau_{vol}$ parametri, $k_{t2}$, $d_{stop,\sigma}$, $\tau_{surv}$, $\tau_{dist}^{\sigma}$) in real-valued con bound; variabili discrete ($b$, $\Delta t_{cromosoma}$, $T_{touch}^{max}$, $d_{inv}$, $d_{obsolete}$, $T_{min,session}$, $\mathbf{s}$) in integer/binary. Crossover e mutazione di Cap.23 operano coerentemente con l'encoding misto.
- **22.9 Tabella sintesi del cromosoma**: tabella finale con tutte le voci (gene, simbolo, dominio, encoding, regime-dipendenza, eredita').

**Vincoli trasversali Cap.22.** Nessun valore numerico viene congelato in Cap.22 (i valori provvisori restano provvisori, congelati in Cap.26). La dimensionalita' totale del cromosoma e' un numero specifico da derivare e dichiarare nel testo (es. "il cromosoma ha $K$ parametri continui e $K'$ discreti, totale $K+K'$ geni"; $K, K'$ specifici di Parte V).

### Capitolo 23 -- Operatori GA (~2 pp)

**Scope.** Definire l'algoritmo genetico operativo: NSGA-II con elitismo, crossover, mutazione, gestione dei vincoli di ammissibilita', tasso di rimpiazzo. Giustificare analiticamente il range del budget di valutazioni dichiarato in CAP-01.

**Contenuto obbligatorio.**

- **23.1 NSGA-II come algoritmo primario**: motivazione della scelta (Deb et al. 2002, IEEE Trans. Evolutionary Computation): ranking per non-dominanza, crowding distance per diversita', elitismo basato su unione parent+offspring. Citare il riferimento.
- **23.2 Crossover misto**: per geni continui simulated binary crossover (SBX) con eta_c parametro del modello; per geni discreti uniform crossover binario; per il vettore $\mathbf{s}$ di selezione feature, uniform crossover su componenti con vincolo $\sum s_j \leq K_{max}$ (riparazione: se l'offspring viola, disattiva feature random fino a rientrare).
- **23.3 Mutazione**: per geni continui polynomial mutation con eta_m parametro del modello; per geni discreti random reset con probabilita' $p_m^{disc}$; per $\mathbf{s}$, bit flip con vincolo cardinalita'. Tassi $p_m$ congelati in Cap.26.
- **23.4 Gestione vincoli di ammissibilita'**: cromosomi che violano i vincoli rigidi (Cap.22.7) sono dichiarati non validi. Strategia: **constraint-domination** (Deb 2000): individui ammissibili dominano individui non ammissibili indipendentemente dalla fitness; tra non ammissibili, ordinamento per somma normalizzata delle violazioni. Riparazione (se attivata): nella mutazione random vincolata si proietta il gene violante nel dominio ammissibile piu' prossimo (es. se $d_{stop} \leq b$, $d_{stop}$ viene aumentato al primo multiplo di 5 sopra $b$).
- **23.5 Elitismo**: NSGA-II elitismo standard via $(\mu + \lambda)$ selection sull'unione parent+offspring di taglia $2P$, ranking per fronte di non-dominanza, troncamento a $P$ con tie-break su crowding distance.
- **23.6 Tasso di rimpiazzo (M-4) -- derivazione analitica**: definire formalmente il **tasso di rimpiazzo per generazione** $r_{repl}$ come la frazione di offspring che entrano nella popolazione successiva sostituendo parent dominati. Per NSGA-II con $(\mu+\lambda)$ selection $\mu=\lambda=P$, in regime di lavoro tipico $r_{repl} \in [0{,}3; 0{,}6]$ (citare letteratura: Deb 2002, Eyalsing et al.). Sotto questa ipotesi, il **numero di valutazioni effettive di fitness** nelle $G$ generazioni e' $N_{eval} = P + G \cdot \lambda$ (popolazione iniziale + offspring per generazione) ridotto dal **caching dei cromosomi non dominati** archiviati: in regime stazionario, $N_{eval}^{actual} \approx P + G \cdot \lambda \cdot (1 - r_{cache})$ dove $r_{cache}$ e' la frazione di offspring identici a parent gia' valutati (atteso piccolo per encoding misto, $r_{cache} \in [0{,}05; 0{,}15]$).
- **23.6.1 Derivazione del range 12.800-25.600 min single-thread (CAP-01)**: con $P=128$, $G=150$, valutazione fitness 0{,}5-1 min/cromosoma single-thread (range stimato in CAP-01 sulla base di 3-13 min/cromosoma full backtest 5 anni Cap.4 PI scalato sul singolo fold del walk-forward): $N_{eval}^{actual} \approx 128 + 150 \cdot 128 \cdot 0{,}9 = 17.408$ valutazioni (con $r_{cache}=0{,}1$). Tempo totale $17.408 \cdot 0{,}5\text{-}1 \approx 8.700\text{-}17.400$ min single-thread per **un singolo fold**; estendendo a tutti i $F$ fold del walk-forward nested ($F$ definito in Cap.25), il totale e' $F \cdot 8.700\text{-}17.400$ min, congruente con il range 21.000-41.500 min di CAP-01 per $F \in [2; 3]$. Il range 12.800-25.600 min single-thread di M-4 e' specifico del compute alla popolazione 128 e generazioni 150 SENZA walk-forward, ovvero il run di calibrazione iniziale prima del walk-forward nested completo. Specificare numericamente la derivazione.
- **23.6.2 Benchmark empirico**: la verifica empirica del tasso di rimpiazzo effettivo $r_{repl}$ e del range di valutazioni e' **out-of-scope per Cap.23** e rinviata a **Parte VII Cap.34** (bootstrap stazionario + stress test del compute budget). Cap.23 fornisce la formula analitica e il range derivato; la conferma empirica e' Parte VII.
- **23.7 Seed e riproducibilita'**: il seed del PRNG (numpy) per inizializzazione popolazione, mutazione e crossover e' parte del bundle di calibrazione e registrato nel log, coerente con Cap.10 Parte II (eredita' 15).

**Vincoli trasversali Cap.23.** Citazione di Deb et al. (2002) "A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II", *IEEE Transactions on Evolutionary Computation* 6(2), 182--197 obbligatoria. Tutti i tassi $\eta_c, \eta_m, p_m$ sono dichiarati come parametri del modello, valori di lavoro provvisori (e.g. $\eta_c=15, \eta_m=20, p_m^{cont}=1/K, p_m^{disc}=1/K'$ secondo prassi NSGA-II), congelati in Cap.26.

### Capitolo 24 -- Funzione di fitness multi-obiettivo (~2 pp)

**Scope.** Definire la fitness multi-obiettivo che il GA massimizza/minimizza. Lista esplicita degli obiettivi, formule, penalita' per emissione anomala, integrazione con metriche di lifecycle (Cap.11 Parte II) e movimento strutturale (eredita' 2). Allineamento esplicito con la metrica primaria di CAP-01 (expected net return per segnale eseguito).

**Contenuto obbligatorio.**

- **24.1 Obiettivi della fitness -- vettore $\mathbf{f}(\theta) \in \mathbb{R}^M$**:
  - $f_1$ = **expected net return per segnale eseguito** $E[R_{net} | executed]$ (eredita' Cap.5 Parte I): da **massimizzare**. Formula: $E[R_{net} | executed] = E[R_{gross} | executed] - 2c$ con $c=1$ pt equivalente per commissione. Calcolo sull'OOS del fold (Cap.25). Sui segnali expired in $\Delta t_{cromosoma}$ il rendimento e' MAE alla scadenza (closing forzato logico): dichiarare esplicitamente la regola di chiusura virtuale.
  - $f_2$ = **target_1 hit rate** = $|\{s : \text{state}(s)=\text{target\_1\_hit}\}| / |\{s : \text{executed}(s)\}|$ (eredita' 12): da **massimizzare**. Calcolo sull'OOS del fold.
  - $f_3$ = **invalidation rate pre-touch** = $|\{s : \text{state}(s)=\text{invalidated}\}| / |\{s : \text{emitted}(s)\}|$: da **minimizzare**. Calcolo sull'OOS del fold.
  - $f_4$ = **maximum drawdown intraday dell'equity sintetica** $MDD$ (eredita' 8): da **minimizzare**. Equity sintetica = somma cumulativa $R_{net}$ per segnale eseguito ordinato per $t_{exec}$. $MDD = \max_t (\text{eq}_t^{peak} - \text{eq}_t)$.
  - $f_5$ = **stabilita' cross-regime della fitness** (eredita' 22 + Cap.14.4): la fitness deve essere comparabile fra fold prevalentemente calmi e prevalentemente turbolenti. Misura: $|f_1^{calmo} - f_1^{turbolento}|$ normalizzata, da **minimizzare**. La classificazione del fold come prevalentemente calmo/turbolento e' materia di Cap.25.
- **24.2 Penalita' integrate nella fitness**:
  - **Penalita' emissione eccessiva**: se il tasso medio di emissione/sessione supera una soglia $E_{max}$ provvisoria (es. 5 segnali/sessione), penalizzare $f_1$. Motivazione: emissioni troppo frequenti producono rumore al canale Telegram e violano lo spirito del filtro 80 pt.
  - **Penalita' emissione nulla**: se il tasso medio di emissione/sessione e' sotto $E_{min}$ (es. 0{,}2 segnali/sessione), penalizzare $f_1$. Motivazione: un GA che converge su cromosomi che non emettono mai produce metriche degenerate (0/0).
  - **Penalita' lifecycle anomalo**: tasso di `expired posttrigger_timeout` $> E_{exp,max}$ (es. 30%) penalizza $f_1$ (segnale troppo lento). Dichiarare $E_{max}, E_{min}, E_{exp,max}$ provvisori, congelati in Cap.26.
- **24.3 Metriche di lifecycle aggiuntive (no obiettivi diretti, tracking)**: dalla submacchina position lifecycle (Cap.11 Parte II, eredita' 14): $\pi_{t_2 | t_1}$ (target_2 hit rate condizionale), MFE/MAE aggregati, $f_{stop|t_1}$ (frazione di stop post-target_1). Queste metriche sono **tracciate nel log del fold** e usate per reporting (Parte VII) ma non sono obiettivi diretti del NSGA-II.
- **24.4 Allineamento a CAP-01: target operativo asimmetrico**: il target 500 pt FIB/giorno OR 70% movimento strutturale (eredita' 2) viene tradotto come **metrica di reporting**, non come obiettivo diretto della fitness. Motivazione: gli obiettivi $f_1$-$f_5$ sono per-segnale; il target di sessione 500 pt/70% e' un aggregato di sessione. L'aggregato di sessione viene calcolato nel reporting di Parte VII; il GA ottimizza per-segnale e per-fold. Dichiarare esplicitamente questa separazione.
- **24.5 Replay deterministico per la valutazione di fitness** (eredita' 15): la valutazione di $\mathbf{f}(\theta)$ richiede il replay completo del motore sul fold OOS. Specificare il log del replay con campi obbligatori per ogni segnale: $signal\_id$, $t_{emission}$, $t_{exec}$ (o NULL se non eseguito), $\Delta t_{pretrigger} = t_{exec} - t_{emission}$ separato da $\Delta t_{cromosoma}$ (N-4 v2), $R_{gross}, R_{net}$ (N-2 carryover Parte VII, ma replay log gia' contiene), stato terminale, causa (per `expired`), tutti i campi del payload (eredita' 10). Nomenclatura `executable_rate` post-eliminazione guardie: la frazione di emessi che raggiungono raw touch entro $T_{touch}^{max}$ (N-3, eredita' Cap.5 Parte I post-patch Iterazione 2 CAP-01).
- **24.6 Aggregazione multi-fold della fitness**: la fitness sul singolo fold OOS produce un vettore $\mathbf{f}_k(\theta) \in \mathbb{R}^M$ per il fold $k$. L'aggregazione fra fold per produrre la fitness globale del cromosoma e':
  - $f_m^{global}(\theta) = \text{mediana}_k f_{m,k}(\theta)$ per gli obiettivi a livello (per essere robusto a fold con poche emissioni o regimi atipici);
  - $f_5^{global}$ e' calcolata direttamente sull'intera storia con la separazione regime.
  - **Stabilita' come metrica esplicita**: deviazione interquartile cross-fold $IQR(f_{m,k})/median$ tracciata per ogni obiettivo, non ottimizzata direttamente ma riportata per la selezione finale del bundle in Parte VII.
- **24.7 No incorporazione di DSR/PBO come obiettivi diretti** (eredita' 8): DSR e PBO sono gate post-selezione in Parte VII; la fitness di Parte V non li incorpora. Dichiarazione esplicita.

**Vincoli trasversali Cap.24.** Numero esplicito di obiettivi $M$ del vettore $\mathbf{f}(\theta)$ deve essere dichiarato (es. $M=5$). Citare Pareto-dominance e il principio di non-dominanza di Deb (2001). Le formule sono complete e operative -- niente "approssimativamente" o "tipicamente".

### Capitolo 25 -- Walk-forward nested con purge ed embargo, diagnostica survival fold-per-fold (~2,5 pp)

**Scope.** Definire lo schema temporale del walk-forward nested, la gestione di purge ed embargo, la window selection EGARCH con benchmark e rollback (M-5), la classificazione di regime nel walk-forward (M-6), il Cox condizionale al regime (M-14), la diagnostica survival fold-per-fold (M-7+M-8+M-9+M-10), la cadenza di ricalibrazione (M-2 v2 parte Parte V).

**Contenuto obbligatorio.**

- **25.1 Schema walk-forward nested**: $F$ fold annidati su 5 anni di storico (eredita' Cap.4 Parte I), ciascun fold composto da finestra in-sample $W_{in}$ + purge $P_{purge}$ + finestra OOS $W_{oos}$ + embargo $P_{emb}$. Valori provvisori: $W_{in} = 6$ mesi calendario (circa 126 sessioni $\times$ 840 = 105.840 barre), $W_{oos} = 3$ mesi calendario (circa 63 sessioni $\times$ 840 = 52.920 barre), $P_{purge} = 5$ sessioni $\times$ 840 = 4.200 barre, $P_{emb} = 5$ sessioni $\times$ 840 = 4.200 barre. Numero di fold nested $F = 8$ (provvisorio, valido per 5 anni di storico). Tutti i parametri congelati in Cap.26.
- **25.2 Motivazione del purge e dell'embargo**: la purge previene leakage da feature look-ahead (es. EMA, pivot confermati a $t+n_c+1$, $\hat{\sigma}_t$ con dipendenza ricorsiva dal $\sigma_{t-1}$ -- eredita' 24, 25). L'embargo previene contaminazione fra fold consecutivi per feature persistenti. Citare Lopez de Prado (2018) "Advances in Financial Machine Learning" cap. 7 (purged k-fold).
- **25.3 Window selection EGARCH (M-5)**: protocollo di **benchmark comparativo rolling vs expanding vs EWMA**. Specificare:
  - **Candidate windows**: rolling $W \in \{105.000; 210.000; 420.000\}$ barre (6m, 1y, 2y); expanding da inizio dello storico; EWMA con $\lambda_{ewma}$ in $\{0{,}99; 0{,}995; 0{,}999\}$.
  - **Metrica OOS congelata** per il confronto: log-likelihood OOS predittiva del modello EGARCH calibrato su ogni candidate window. La log-likelihood OOS e' calcolata sui residui standardizzati prodotti dal modello fittato sulla finestra precedente al fold OOS.
  - **Test Inoue-Rossi (2011)** "Identifying the sources of instabilities in macroeconomic forecasting models" *Journal of Applied Econometrics* 26(3), 367--391: test di stabilita' della performance predittiva fra finestre alternative, con statistica di confronto basata su loss-difference cumulata.
  - **Criterio di rollback normativo**: se rolling $W=210.000$ **non domina** (p-value Inoue-Rossi $<0{,}05$) almeno una delle alternative su metrica OOS congelata, **si effettua rollback** alla finestra con migliore performance OOS dominante. Il rollback e' deterministico, registrato nel log di calibrazione del fold.
- **25.4 Classificazione di regime nel walk-forward (M-6)**: ogni fold OOS e' classificato come "prevalentemente calmo" o "prevalentemente turbolento" sulla base della frazione di barre in stato $R_t = $ turbolento (eredita' 22). Test parallel media-mediana: la media di sessione $\bar{\sigma}_s$ e la mediana $\text{med}_t(\hat{\sigma}_{s,t})$ producono due classificazioni; la **frazione di sessioni con classificazione divergente** (es. una calma, l'altra turbolenta sulla stessa sessione) e' la statistica di stabilita'. Soglia di "cambiamento significativo": divergenza $> 10\%$ delle sessioni del fold attiva il flag "regime instabile" nel log del fold, che entra nella stabilita' cross-regime di Cap.24.1 $f_5$.
- **25.5 Cox condizionale al regime (M-14)**: decisione fra (a) interaction term: $R_{t_{emission}}$ entra come feature aggiuntiva di $\tilde{\mathbf{x}}$ + termini di interazione $R \cdot x_j$ per le feature di volatilita' e struttura; (b) stratificazione formale: Cox separato per calmo e turbolento, baseline hazard distinte $h_{0,j,calmo}, h_{0,j,turbolento}$, coefficienti $\boldsymbol{\beta}_{j,calmo}, \boldsymbol{\beta}_{j,turbolento}$. **Decisione Cap.25**: opzione (b) stratificazione formale, motivazione: cattura interazioni non lineari fra regime e feature; il maggior costo in parametri (raddoppio dei coefficienti) e' contenuto dato $K_{max}$ di Cap.22.6. L'opzione (a) e' rinviata come **benchmark di robustezza** in Cap.25.7 (Cox vs Fine-Gray): se l'opzione (b) produce instabilita' eccessiva nei coefficienti fold-per-fold ($CV(\hat{\boldsymbol{\beta}}_{j,R})$ alta), si fallback a (a) con interaction term. Criterio di rollback registrato.
- **25.6 Diagnostica survival fold-per-fold (M-7+M-8)**: applicata su ogni fold dopo la stima MLE del Cox sul fold in-sample:
  - **Test residui di Cox-Snell** (Cox e Snell 1968): per ciascuna funzione di rischio causa-specifica $h_1, h_2$, calcolare i residui $\hat{e}_{i,j} = -\ln \hat{S}_j(\tau_i | \tilde{\mathbf{x}}_i)$. Sotto assunzione di censoring non-informativo + modello correttamente specificato, $\hat{e}_{i,j} \sim \text{Exp}(1)$. Verifica via plot $-\ln \hat{S}_{empirica}(\hat{e})$ vs diagonale teorica + test di Kolmogorov-Smirnov.
  - **Test di Schoenfeld stratificato per evento vs censoring** (Grambsch-Therneau 1994): residui di Schoenfeld separati per le osservazioni con evento target_1_hit, stopped, e censurate. Dipendenza dal tempo sistematica indica correlazione censoring/evento; criterio di accettazione: $p > 0{,}05$ sul test globale fold-per-fold.
  - **Registrazione nel log del fold**: esiti dei test + flag "assunzione censoring non-informativo violata" se entrambi test falliscono. Il flag attiva la regola di rollback al modello Fine-Gray (Cap.25.7).
- **25.7 Benchmark Cox cause-specific vs Fine-Gray sub-distribution (M-9)**: per ciascun fold OOS, calibrare entrambi i modelli e confrontare la metrica di **calibrazione predittiva** della $\hat{p}_{hit}$ (es. Brier score per il binary outcome target_1_hit) sull'OOS. Se Fine-Gray produce Brier score significativamente migliore (test di Diebold-Mariano), si registra il flag "Fine-Gray preferito sul fold" nel log. La decisione **a livello bundle frozen** sulla scelta primaria (Cox vs Fine-Gray) e' presa in Parte VII sulla base del rapporto di flag positivi/totali.
- **25.8 Test Schoenfeld per hazard proporzionali (M-10)**: separato dalla diagnostica censoring (25.6). Su ciascun fold in-sample, calcolare il test di Schoenfeld globale sulla feature: violazione (p < 0{,}05 sistematicamente) indica hazard non proporzionale. Registrazione nel log del fold; estensione a modello con hazard non-proporzionale (Cox con time-varying coefficients) e' rinviata a Parte VII come carryover M-promemoria se violazione strutturale.
- **25.9 Cadenza ricalibrazione EGARCH e Cox -- separazione fra Parte V e Parte VI (M-2 v2)**: dentro il walk-forward, ricalibrazione fold-per-fold (eredita' 19): all'inizio di ogni fold OOS, EGARCH e Cox vengono ri-stimati sulla finestra in-sample del fold. In **production live** (Parte VI), la cadenza di re-fitting del bundle frozen e' funzione del tempo di vita del bundle (es. trimestrale o semestrale come dichiarato in Cap.4 Parte I) + trigger di break parametrico monitorato in real-time -- materia di Cap.27 Parte VI. La separazione fra walk-forward e production e' dichiarata esplicitamente in un paragrafo dedicato.

**Vincoli trasversali Cap.25.** Citazioni obbligatorie: Lopez de Prado (2018), Inoue-Rossi (2011), Cox-Snell (1968), Grambsch-Therneau (1994), Fine-Gray (1999), Diebold-Mariano (1995). Tutti i parametri ($W_{in}, W_{oos}, P_{purge}, P_{emb}, F$) provvisori, congelati in Cap.26.

### Capitolo 26 -- Calibrazione, congelamento numerico, criteri di stop (~1,5 pp)

**Scope.** Specificare la calibrazione operativa del GA: popolazione 128, generazioni fino a 150, criteri di convergenza e di stop, gestione seed. Soprattutto: **congelare numericamente** tutti i parametri provvisori delle Parti I-IV, con tabella esplicita e motivazione per ciascun valore.

**Contenuto obbligatorio.**

- **26.1 Popolazione e generazioni**: $P=128$, $G_{max}=150$ (eredita' 3 + 9). Motivazione del numero di individui: $P=128$ produce diversita' sufficiente per NSGA-II in spazio misto con dimensionalita' $K + K' + 37 \approx 50$ geni; potenze di 2 facilitano parallelizzazione su c5.4xlarge (eredita' 9). Motivazione di $G_{max}=150$: ordine di grandezza tipico per NSGA-II in finanza (Lopez de Prado 2018), permette convergenza con margine operativo.
- **26.2 Criteri di stop**:
  - **Criterio primario**: $G_{max}=150$ generazioni raggiunte.
  - **Criterio anticipato (convergenza)**: la frontiera di Pareto non avanza significativamente per $G_{stall}=15$ generazioni consecutive, misurato come distanza Wasserstein tra le frontiere di Pareto $\mathcal{F}_{g-G_{stall}}$ e $\mathcal{F}_g$ inferiore a una soglia $\epsilon_{front}=0{,}01$ (normalizzato). Valori $G_{stall}, \epsilon_{front}$ provvisori, congelati nella tabella di 26.5.
  - **Criterio compute-budget**: se la stima cumulata di tempo supera $T_{budget}=60$ ore wall-clock su c5.4xlarge, stop forzato con bundle parziale. Coerenza con eredita' 9.
- **26.3 Selezione distribuzione $D$ del EGARCH (eredita' 17)**: protocollo di selezione AIC/BIC su finestra di calibrazione iniziale; tie-break su residual diagnostics (Ljung-Box). Esito provvisorio: dichiarare quale distribuzione e' scelta sulla finestra di lavoro Portara/CQG (decisione: Student-t come default provvisorio, GED come alternativa; finalita' di Parte V e' produrre l'esito).
- **26.4 Selezione inizializzazione EGARCH (eredita' 20)**: scelta fra Opzione A (ripresa fine sessione precedente) e Opzione B (varianza incondizionata). Esito provvisorio: Opzione A confermata se stabilita' stima nelle prime barre $\geq$ Opzione B (criterio: minore varianza dei residui standardizzati nelle prime 60 barre di sessione).
- **26.5 Tabella di congelamento -- parametri del modello e del cromosoma**: tabella esplicita prima/dopo. Colonne: parametro, capitolo di provenienza, dominio, valore provvisorio, **valore congelato di lavoro Parte V**, motivazione. Voci obbligatorie:
  - Eredita' Parte II-III: $b_{min}$, $W$, $p$, $N_{reg}$, $T_{persist}$, $n_c$, $\delta_{pivot}$, $N_{pivot}$, $W_{norm}$, $T_{warmup,\text{EMA}}$, $T_{warmup,\text{norm}}$, $\lambda$ (EMA), distribuzione $D$, inizializzazione EGARCH (A o B), $\tau_{vol,low}$ (N-5).
  - Eredita' Parte IV: $d_{inv}, d_{obsolete}, T_{min,session}, k_{t2}, d_{stop,\sigma}, \tau_{surv}$, eventuali varianti regime-dipendenti.
  - Eredita' Parte IV trade_range (M-15): $A_{range,min}=80$ (vincolo assoluto, **non congelabile** -- dichiarazione esplicita), $N_{osc}, n_{osc,min}, \epsilon_{osc}, N_{break}, \delta_{break}$.
  - Parametri di Parte V: $P=128$, $G_{max}=150$, $G_{stall}, \epsilon_{front}$, $\eta_c, \eta_m, p_m^{cont}, p_m^{disc}, K_{max}$, $E_{max}, E_{min}, E_{exp,max}$ (Cap.24.2 penalita').
- **26.6 Risk-reward ratio floor/cap (eredita' 33)**: decisione di Parte V sulla base dell'evidenza empirica. Default provvisorio: NO floor esplicito su RR (lasciato all'ottimizzazione implicita via fitness). Se analisi empirica mostra che il GA converge sistematicamente su cromosomi con $RR<1$ producendo segnali strutturalmente perdenti, attivare floor $RR_{min}=1$ in Cap.26.5.
- **26.7 Dimensionalita' massima $K_{max}$ feature survival (M-11)**: regola heuristica: $K_{max} = \min(15, K_{37}/3)$ dove $K_{37}=37$, dunque $K_{max}=12$ valore di lavoro provvisorio. Motivazione: rapporto $N_{eventi}/K \geq 10$ per stabilita' del Cox (rule of thumb Harrell 2015, "Regression Modeling Strategies" cap. 4). Con $N_{eventi}$ atteso per fold $\geq 120$, $K_{max}=12$ rispetta la soglia.
- **26.8 Seed e riproducibilita'**: il seed del bundle e' parte del log di calibrazione (coerenza con Cap.10 PII, eredita' 15). Replay bit-exact su seed identico.

**Vincoli trasversali Cap.26.** Tabella di 26.5 e' il documento normativo del congelamento. Ogni voce ha valore numerico specifico (non "circa", non "tipicamente"). Le motivazioni sono brevi (1-2 righe ciascuna) ma non assenti. Tutti i valori sono coerenti con i domini delle Parti I-IV; nessuna contraddizione con eredita' precedenti.

## Acceptance criteria -- tutti devono essere soddisfatti per PASS in Review

### Struttura e completezza generale

- [ ] **AC-1**: i 5 capitoli (Cap.22-26) sono presenti, completi, nell'ordine corretto. Lunghezza totale ~10 pp.
- [ ] **AC-2**: tutte le 44 eredita' (9 CAP-01 + 7 CAP-02 + 9 CAP-03 + 19 CAP-04) sono citate esplicitamente almeno una volta nel capitolo pertinente. Verifica esplicita nel REPORT con mappa eredita'-citazione.
- [ ] **AC-3**: tutti i 16 M-promemoria pertinenti (M-2 v2, M-4, M-5, M-6, M-7, M-8, M-9, M-10, M-11, M-14, M-15, N-1 v2 CAP-03, N-3, N-4 v2, N-5) sono trattati nei capitoli indicati nella tabella di pertinenza. Verifica esplicita nel REPORT con tabella M-ID/capitolo/trattamento.
- [ ] **AC-4**: il REPORT_CAP_05.md include sezione "Misura prima/dopo" con impatto sul comportamento del GA per ogni decisione di Cap.22-26.
- [ ] **AC-5**: il documento e' in italiano formale, registro tecnico, formule LaTeX inline e display dove appropriato. Citazioni scientifiche inline (non bibliografia finale separata).

### Cap.22 -- Cromosoma

- [ ] **AC-22-1**: il cromosoma $\theta$ e' definito formalmente con tabella riepilogo che enumera ogni gene (simbolo, dominio, encoding, regime-dipendenza, eredita').
- [ ] **AC-22-2**: tutti i geni geometrici (eredita' 7, 28, 29), di emissione (eredita' 13, 30, 40), target/stop (eredita' 31, 32) e temporali (eredita' 4, Cap.6.1 Parte II) sono inclusi.
- [ ] **AC-22-3**: il vettore $\mathbf{s}$ di selezione feature survival e' definito con dominio $\{0,1\}^{37}$ e vincolo $\sum s_j \leq K_{max}$ (M-11).
- [ ] **AC-22-4**: i vincoli di ammissibilita' (Cap.22.7) sono enumerati esplicitamente e collegati alle eredita' (6, 7, 5).
- [ ] **AC-22-5**: encoding misto (real/integer/binary) dichiarato e coerente con gli operatori di Cap.23.
- [ ] **AC-22-6**: dimensionalita' totale del cromosoma dichiarata numericamente (es. "$K$ geni continui + $K'$ discreti + 37 binari").
- [ ] **AC-22-7**: nessun valore numerico congelato in Cap.22 (i provvisori restano provvisori, rinvio esplicito a Cap.26).

### Cap.23 -- Operatori GA

- [ ] **AC-23-1**: NSGA-II dichiarato come algoritmo primario con citazione Deb et al. (2002).
- [ ] **AC-23-2**: crossover (SBX continuo, uniform discreto, uniform vincolato per $\mathbf{s}$), mutazione (polynomial continuo, random reset discreto, bit flip vincolato per $\mathbf{s}$), elitismo $(\mu+\lambda)$ tutti specificati.
- [ ] **AC-23-3**: strategia di gestione vincoli di ammissibilita' (constraint-domination Deb 2000) dichiarata.
- [ ] **AC-23-4**: tasso di rimpiazzo $r_{repl}$ definito formalmente; formula del numero di valutazioni effettive $N_{eval}^{actual} = P + G \cdot \lambda \cdot (1 - r_{cache})$ presente (M-4).
- [ ] **AC-23-5**: derivazione analitica del range 12.800-25.600 min single-thread coerente con CAP-01 (M-4): produce numeri specifici (es. 17.408 valutazioni per singolo fold).
- [ ] **AC-23-6**: rinvio esplicito del benchmark empirico del tasso di rimpiazzo a Parte VII (no benchmark vero proprio in Cap.23).
- [ ] **AC-23-7**: seed e PRNG dichiarati parte del bundle (eredita' 15).

### Cap.24 -- Fitness multi-obiettivo

- [ ] **AC-24-1**: vettore $\mathbf{f}(\theta) \in \mathbb{R}^M$ definito con $M$ esplicito e ogni obiettivo formalizzato come massimizzazione o minimizzazione.
- [ ] **AC-24-2**: $f_1 = E[R_{net}|executed]$ con formula completa $E[R_{net}|executed] = E[R_{gross}|executed] - 2c$ ($c=1$ pt) coerente con CAP-01 Cap.5.
- [ ] **AC-24-3**: $f_2$ (target_1 hit rate), $f_3$ (invalidation rate), $f_4$ (MDD), $f_5$ (stabilita' cross-regime) formalizzati.
- [ ] **AC-24-4**: penalita' emissione eccessiva, nulla, lifecycle anomalo (Cap.24.2) con parametri $E_{max}, E_{min}, E_{exp,max}$ dichiarati provvisori, congelati in Cap.26.
- [ ] **AC-24-5**: metriche di lifecycle aggiuntive (Cap.11 Parte II): $\pi_{t_2|t_1}$, MFE, MAE, $f_{stop|t_1}$ tracciate in log, non obiettivi diretti (N-1 v2 CAP-03).
- [ ] **AC-24-6**: target 500 pt/70% (eredita' 2) trattato come reporting, non obiettivo diretto, con motivazione esplicita.
- [ ] **AC-24-7**: replay deterministico log specifica $\Delta t_{pretrigger}$ separato da $\Delta t_{cromosoma}$ (N-4 v2).
- [ ] **AC-24-8**: nomenclatura `executable_rate` aggiornata post-eliminazione guardie (N-3).
- [ ] **AC-24-9**: aggregazione multi-fold tramite mediana cross-fold + IQR esplicitata.
- [ ] **AC-24-10**: nessuna incorporazione DSR/PBO come obiettivi diretti (eredita' 8) -- dichiarazione esplicita.

### Cap.25 -- Walk-forward + diagnostica survival

- [ ] **AC-25-1**: schema walk-forward nested con $W_{in}, W_{oos}, P_{purge}, P_{emb}, F$ definiti con valori numerici provvisori specifici.
- [ ] **AC-25-2**: motivazione purge ed embargo con citazione Lopez de Prado (2018).
- [ ] **AC-25-3**: protocollo benchmark window EGARCH (M-5): candidate windows specificate (rolling 105.000/210.000/420.000 + expanding + EWMA), metrica OOS congelata definita, test Inoue-Rossi (2011) citato.
- [ ] **AC-25-4**: criterio di rollback automatico (M-5) normativo: regola operativa esplicita con soglia p-value e azione conseguente.
- [ ] **AC-25-5**: classificazione regime nel walk-forward (M-6) con test parallel media-mediana, soglia di "cambiamento significativo" definita (es. 10%).
- [ ] **AC-25-6**: Cox condizionale al regime (M-14) -- decisione (b) stratificazione formale dichiarata con motivazione; opzione (a) interaction term come benchmark di rollback.
- [ ] **AC-25-7**: diagnostica censoring non-informativo (M-7+M-8): test residui Cox-Snell + Schoenfeld stratificato, citati Cox-Snell (1968) e Grambsch-Therneau (1994), criterio di accettazione $p>0{,}05$.
- [ ] **AC-25-8**: benchmark Cox vs Fine-Gray (M-9): protocollo Brier score + test Diebold-Mariano, decisione bundle-level rinviata a Parte VII con criterio operativo (rapporto flag positivi/totali).
- [ ] **AC-25-9**: test Schoenfeld per hazard proporzionali (M-10): separato dalla diagnostica censoring, criterio di accettazione $p>0{,}05$, estensione a non-proporzionali rinviata a Parte VII.
- [ ] **AC-25-10**: separazione cadenza ricalibrazione fra Parte V e Parte VI (M-2 v2): dichiarazione esplicita in paragrafo dedicato.

### Cap.26 -- Calibrazione e congelamento

- [ ] **AC-26-1**: popolazione $P=128$ e $G_{max}=150$ confermati con motivazione esplicita coerente con eredita' 3 + 9.
- [ ] **AC-26-2**: criteri di stop (primario, anticipato Wasserstein, compute-budget) tutti specificati con valori numerici provvisori.
- [ ] **AC-26-3**: selezione distribuzione $D$ EGARCH (eredita' 17) -- esito provvisorio dichiarato (Student-t default + GED alternativa, criterio AIC/BIC).
- [ ] **AC-26-4**: selezione inizializzazione EGARCH (eredita' 20) -- esito provvisorio dichiarato (Opzione A default).
- [ ] **AC-26-5**: tabella di congelamento completa per Cap.26.5 con valori specifici per **tutti** i parametri provvisori delle Parti I-IV + Parte V. Nessuna voce con valore "circa" o "da definire empiricamente" senza valore numerico di lavoro.
- [ ] **AC-26-6**: trade_range $A_{range,min}=80$ dichiarato non congelabile (vincolo assoluto Cap.5 PI); altri parametri trade_range con valori congelati di lavoro (M-15).
- [ ] **AC-26-7**: RR floor/cap (eredita' 33) -- decisione esplicita: no floor di default, attivazione condizionata.
- [ ] **AC-26-8**: $K_{max}$ dimensionalita' feature survival (M-11) -- valore numerico (es. 12) con motivazione rule of thumb Harrell (2015).
- [ ] **AC-26-9**: seed registrato nel log del bundle (coerenza con Cap.10 PII, eredita' 15).

### Vincoli trasversali

- [ ] **AC-T-1**: tick FIB = 5 pt rispettato in ogni formula, esempio numerico, livello strutturale dei capitoli Cap.22-26.
- [ ] **AC-T-2**: determinismo bit-exact dichiarato per replay del walk-forward e valutazione fitness.
- [ ] **AC-T-3**: causalita' $\mathcal{F}_{t-1}$ rispettata per il calcolo della fitness, le diagnostiche survival, la classificazione regime.
- [ ] **AC-T-4**: tutti i valori numerici introdotti in Cap.22-25 sono provvisori e tracciati nella tabella di Cap.26.5; nessun valore "fissato definitivamente" prima della tabella di Cap.26.5.
- [ ] **AC-T-5**: registro tecnico italiano formale, formule LaTeX, esempi numerici dove rilevanti (specialmente Cap.22 e Cap.26).
- [ ] **AC-T-6**: citazioni scientifiche obbligatorie tutte presenti: Deb et al. (2002) NSGA-II, Deb (2000) constraint-domination, Lopez de Prado (2018) purged k-fold, Inoue-Rossi (2011), Cox-Snell (1968), Grambsch-Therneau (1994), Fine-Gray (1999), Diebold-Mariano (1995), Harrell (2015) rule of thumb $N_{eventi}/K$.
- [ ] **AC-T-7**: REPORT_CAP_05.md ha le 5 sezioni del formato supervisore: Cosa prodotto / Ipotesi di partenza / Decisioni rilevanti / Misura prima/dopo / Domande aperte + Criterio di rollback.
- [ ] **AC-T-8**: 00_indice.md aggiornato per riflettere Parte V come "IN REVIEW v1" (questa modifica e' del Developer, non del Planner).
- [ ] **AC-T-9**: tutti i file modificati committati e pushati su `origin/main`. Working tree pulito.

## Out-of-scope -- Development NON include queste cose in CAP-05

- **Pipeline di inference real-time, gestione anti-doppio-segnale, formato messaggio Telegram operativo, monitoraggio lifecycle in production** $\to$ Parte VI Cap.27-30. Cap.25.9 dichiara esplicitamente la separazione fra cadenza walk-forward e cadenza production.
- **Validazione OOS finale, DSR, PBO via CSCV, bootstrap stazionario B=2000, gate decisionali per go-live, frozen bundle e immutabilita'** $\to$ Parte VII Cap.31-36. Cap.23.6.2 e Cap.25.7-25.8 esplicitano i rinvii.
- **Verifica empirica latenza Telegram $L_{max}=30$s** (M-2) $\to$ Appendice E.
- **Setup PC, ambiente Python, GitHub, Claude Code, Telegram bot, agenti Planner/Developer/Reviewer, glossario** $\to$ Appendici A, B, E, F, G.
- **API Directa e storico Portara/CQG** $\to$ Appendici C, D.
- **Schema messaggio Telegram dettagliato** $\to$ Appendice E.
- **Benchmark compute budget verificato empiricamente** (vs derivazione analitica Cap.23.6.1) $\to$ Parte VII (compute stress test).
- **Decisione finale Cox vs Fine-Gray a livello bundle frozen** $\to$ Parte VII (Cap.25.7 dichiara la regola operativa di selezione sulla base del rapporto flag positivi/totali, ma la decisione e' Parte VII).
- **Estensione a hazard non proporzionali (Cox time-varying coefficients)** se violazione strutturale Schoenfeld $\to$ M-promemoria nuovo per Parte VII.
- **Patch retroattive a CAP-01, CAP-02, CAP-03, CAP-04**: nessuna modifica retroattiva alle Parti gia' chiuse PASS. Eventuali incoerenze rilevate da Developer di Parte V che richiedono mini-patch retroattive vanno segnalate come M-promemoria nuovi nel REPORT_CAP_05; la decisione di applicare la mini-patch spetta al supervisore in checkpoint Review.

## Done when

Il documento Parte V risponde senza ambiguita' a queste domande:

1. Qual e' la struttura completa del cromosoma del bundle (lista esaustiva di geni, domini, encoding)? (Cap.22)
2. Quale algoritmo genetico opera, come gestisce i vincoli di ammissibilita', e come si giustifica analiticamente il budget di valutazioni di CAP-01? (Cap.23, M-4)
3. Quali sono gli obiettivi della fitness multi-obiettivo, come si aggregano sui fold del walk-forward, e come si separano dagli obiettivi di reporting (target 500 pt/70%)? (Cap.24)
4. Come e' strutturato il walk-forward nested con purge ed embargo, e quali test verificano l'assenza di leakage tempo-correlata? (Cap.25)
5. Come si sceglie la finestra rolling/expanding/EWMA del EGARCH, e quale criterio di rollback automatico interviene se la default fallisce il test Inoue-Rossi? (Cap.25, M-5)
6. Come e' classificato il regime nel walk-forward, e come si trattano le sessioni con classificazione media-mediana divergente? (Cap.25, M-6)
7. Il Cox e' stratificato per regime calmo/turbolento o usa interaction term, e con quale criterio di rollback se la prima opzione e' instabile? (Cap.25, M-14)
8. Come si verifica fold-per-fold l'assunzione di censoring non-informativo e l'assunzione di hazard proporzionali, e cosa succede in caso di violazione? (Cap.25, M-7+M-8+M-10)
9. Quale modello survival (Cox cause-specific o Fine-Gray) viene scelto a livello bundle frozen, e su che criterio operativo? (Cap.25, M-9)
10. Quali sono i valori congelati di lavoro per **tutti** i parametri provvisori delle Parti I-IV e di Parte V, con motivazione per ciascun valore? (Cap.26, M-15 + altri)
11. Qual e' la dimensionalita' massima del vettore di feature survival, e su quale rule of thumb e' giustificata? (Cap.22.6 + Cap.26.7, M-11)
12. Qual e' la separazione fra cadenza di ricalibrazione nel walk-forward (Parte V) e in production (Parte VI)? (Cap.25.9, M-2 v2)

## Pipeline attesa

Development v1 $\to$ Review v1 audit ostile con classificazione GA $\to$ punto di controllo supervisore se CONDITIONAL/FAIL (decisione su finding MIGLIORA PERFORMANCE e RISCHIO PEGGIORAMENTO; BUG REALI obbligatori, NEUTRO ignorati di default) $\to$ rework v2 $\to$ Review v2 $\to$ ... $\to$ PASS.

**Atteso numero di iterazioni**: 2-3 cicli, coerente con la complessita' della Parte V (motore stesso del progetto) e con il numero di M-promemoria da integrare (16, di cui 11 attivi in CAP-05). Il primo ciclo Review v1 probabilmente trovera' 4-8 finding totali (BUG REALI + MIGLIORA + NEUTRO); la decisione del supervisore sui finding non-BUG seguira' la prassi standard del progetto.

**Criterio di rollback in caso di fallimento**: se Review v2 trova ancora BUG REALI strutturali su Cap.22-26, si valuta uno splitting di Parte V in Parte V.A (Cap.22-24 motore + fitness) e Parte V.B (Cap.25-26 walk-forward + calibrazione), con due cicli Review distinti. Decisione di rollback rinviata al supervisore al primo CONDITIONAL.

---

## Finding di Review v1 da risolvere (rework v2)

Review v1 di CAP-05 (commit `bd8ce34`) ha emesso verdetto **CONDITIONAL** con 3 BUG REALI + 3 RISCHIO PEGGIORAMENTO + 5 NEUTRO. **Decisione supervisore 2026-05-26**:
- 3 BUG REALI obbligatori (NB-1, NB-2, NB-3)
- RP-1 approvato (aumenta T_budget a 75-80h)
- RP-2 ignorato (la motivazione no-double-median del Developer tiene; effetto Simpson resta rischio teorico; Reviewer Parte VII potra' riprendere con dati empirici)
- RP-3 approvato in forma "starting point Parte VII" (dichiara $\theta_{CV}=0,5$ come valore di lavoro per primo run, riconsiderato empiricamente in Parte VII; nessuna citazione di facciata)
- 5 NEUTRO (O-1...O-5) ignorati come da default

Pipeline attesa rework v2: 5 fix chirurgici (3 BUG REALI + RP-1 + RP-3) -> Review v2 -> PASS (alta confidenza, nessuno dei fix tocca l'architettura del motore).

### BUG REALI obbligatori

#### **NB-1** -- Derivazione 12.800-25.600 min M-4 incoerente nelle unita' (Cap.23.6 righe 209-215)

**Problema**: Cap.23.6 a riga 215 scrive "$16.448 \times 0,8 \approx 13.000$, dove il fattore 0,8 cattura un ulteriore margine ottimistico di caching" -- ma $16.448 \times 0,8$ e' un numero di **valutazioni**, non di **minuti** single-thread. M-4 di CAP-01 e' in minuti. La derivazione confonde unita': applica un fattore alle valutazioni e poi etichetta il risultato come minuti.

**Fix v2**: riallineare le unita' in Cap.23.6. Due strade equivalenti -- il Developer sceglie e motiva nel REPORT:

(a) **Preserva CAP-01 M-4 [12.800; 25.600] min** dichiarando esplicitamente il range di valutazione fitness $t_{eval} \in [0,74; 1,47]$ min/cromosoma coerente con $N_{eval}^{actual} = 17.408$:
$$N_{eval}^{actual} \cdot t_{eval} = 17.408 \cdot [0,74; 1,47] = [12.882; 25.590] \approx [12.800; 25.600] \text{ min single-thread}$$
Rimuovere la riga errata "$16.448 \times 0,8$". Aggiornare anche Cap.4 PI o REPORT_CAP_01 se necessario per coerenza inter-capitolo.

(b) **Ridichiara M-4 effettivo** coerente con $t_{eval} \in [0,5; 1,0]$ min/cromosoma e $N_{eval}^{actual} \in [16.448; 18.368]$, che produce $[8.224; 18.368]$ min single-thread per singolo run di calibrazione. Aggiornare CAP-01 (mini-patch Cap.4 PI) per allineare la stima compute con il nuovo range.

**Scelta raccomandata**: (a), che preserva CAP-01 senza mini-patch retroattivo. Verificare con un esempio numerico esplicito che la derivazione regga.

#### **NB-2** -- $K_{max}=12$ congelato vs decisione stratificazione Cap.25.5 incompatibili sotto Harrell (Cap.26.7 righe 645-649, Cap.25.5 riga 421)

**Problema**: Cap.25.5 dichiara stratificazione formale come default di Parte V; Cap.26.7 riconosce esplicitamente che sotto stratificazione con split 50/50 ogni strato ha $N_{eventi} \geq 60$ e Harrell richiede $K_{max} \leq 6$ per strato. Tuttavia Cap.26.7 congela $K_{max}=12$ comunque. La stima Cox cause-specific stratificata risulta sovra-parametrizzata, con coefficienti $\beta_{j,R}$ instabili cross-fold; la stima $\hat{p}_{hit}$ e' biased; il filtro $E_{surv}$ di Cap.20 PIV usa stima distorta; il ranking del fronte di Pareto e' alterato.

**Fix v2**: scegliere una delle 3 opzioni, motivata nel REPORT (sezione "Decisioni rilevanti"):

(a) **Congela $K_{max}=6$** in Cap.26.5 e Cap.26.7. Aggiornare Cap.25.5 per dichiarare che con $K \leq 6$ la stratificazione rispetta Harrell. Minimizza il rischio overfitting; preserva la stratificazione come default.

(b) **Mantieni $K_{max}=12$ e cambia Cap.25.5** da stratificazione formale default a **interaction term default** (modello unico con $K+1$ feature, regime come indicator). La stratificazione resta come opzione di rollback condizionata a $N_{eventi,strato} \geq 10 K_{max}$. Coerente con Harrell su modello non stratificato.

(c) **Mantieni entrambi $K_{max}=12$ + stratificazione** ammorbidendo Harrell a $N_{eventi}/K \geq 5$ con citazione esplicita di una fonte specifica che giustifichi il salto. Sconsigliato: fragile in audit, fonte specifica difficile da reperire.

**Scelta raccomandata**: (a) o (b). Il Developer motiva la scelta sulla base di: simmetria fra strati (a vs b), interpretabilita' clinica del modello, robustezza compute (b non duplica i coefficienti).

#### **NB-3** -- Nomenclatura "MAE alla scadenza" incoerente con regola operativa (Cap.24.1 riga 239)

**Problema**: Cap.24.1 scrive "il rendimento e' la MAE alla scadenza (Cap.10.4 di Parte II): il segnale viene chiuso virtualmente al prezzo della barra in cui il timer ha esaurito $\Delta t_{cromosoma}$". MAE (Maximum Adverse Excursion) e' per definizione il massimo movimento avverso durante l'intero segnale, NON il rendimento al momento dell'expiry. La regola operativa e' univoca (rendimento dal fill al prezzo di chiusura virtuale forzata), ma la nomenclatura confonde.

**Fix v2**: sostituire "MAE alla scadenza" con **"rendimento di chiusura virtuale forzata"** (o equivalente: "rendimento al timeout post-trigger", "rendimento di expiry forzato"). Mantenere la regola operativa invariata. Costo: 1 sostituzione di etichetta in Cap.24.1 riga 239. Verificare che il termine "MAE" non riemerga nel resto di Cap.24 con la stessa accezione scorretta.

### RP approvati dal supervisore

#### **RP-1** -- Tensione $F=8$ vs $T_{budget}=60$ ore (Cap.26.2 riga 517, Cap.26.5 riga 614)

**Problema**: nel caso ottimo Cap.23.6, walk-forward nested richiede ~72 ore wall-clock (8 fold $\times$ 9 ore/fold). $T_{budget}=60$ ore e' insufficiente per coprire il caso ottimo; il GA fermato a $T_{budget}$ ha solo 6,7 fold completi. Aggregazione cross-fold meno robusta.

**Decisione supervisore**: aumenta $T_{budget}$ a **75-80 ore** per coprire il caso ottimo $F=8$.

**Fix v2**:
1. **Cap.26.2 riga 517**: aggiornare $T_{budget}=60$ ore con il nuovo valore. Il Developer sceglie fra 75 e 80 (suggerito 80 per margine; 75 e' floor minimo). Motivare la scelta.
2. **Cap.26.5 riga 614**: aggiornare la tabella di congelamento (voce $T_{budget}$).
3. **Cap.23.6**: aggiornare il commento sulla tensione $F$ vs $T_{budget}$ (riga 217 e dintorni) -- ora la tensione e' risolta nel caso ottimo.
4. **REPORT_CAP_05 sezione "Misura prima/dopo"**: aggiungere riga sull'aggiornamento $T_{budget}$.

#### **RP-3** -- Soglia $\theta_{CV}=0,5$ senza fonte (Cap.25.5 riga 423, Cap.26.5 riga 616)

**Problema**: $\theta_{CV}=0,5$ e' trigger di rollback dal Cox stratificato (default) all'interaction term. Valore non motivato da rule of thumb o citazione.

**Decisione supervisore**: opzione 2 -- dichiara $\theta_{CV}=0,5$ come **starting point** per primo run di calibrazione, riconsiderato empiricamente in Parte VII. Nessuna citazione di facciata.

**Fix v2**:
1. **Cap.25.5 riga 423**: aggiornare la formulazione. Aggiungere ~2 righe del tipo: "Il valore $\theta_{CV}=0,5$ e' starting point per il primo run di calibrazione (in assenza di rule of thumb consolidata in letteratura per CV di coefficienti Cox come threshold di stabilita'). La soglia e' riconsiderata empiricamente in Parte VII sulla base degli esiti cross-fold dei coefficienti $\beta_{j,R}$; eventuale ridiscussione formale e' rinviata al ciclo di validazione OOS."
2. **Cap.26.5 riga 616**: aggiornare la voce $\theta_{CV}$ con flag "starting point, riconsiderato Parte VII".
3. **REPORT_CAP_05 sezione "Domande aperte"** o "Criterio di rollback": annotare che $\theta_{CV}$ e' candidato a ridiscussione in Parte VII.

### Acceptance criteria aggiuntivi per la v2

- [ ] **AC-v2-1**: NB-1 chiuso. Cap.23.6 ha derivazione M-4 coerente nelle unita' (val $\times$ min/val = min). Il valore inferiore 12.800 min e' giustificato senza confusione di unita'. Esempio numerico verificabile.
- [ ] **AC-v2-2**: NB-2 chiuso. Scelta motivata fra opzioni (a), (b), (c) nel REPORT. Cap.25.5 e Cap.26.7 coerenti fra loro sotto la scelta selezionata. Nessuna contraddizione residua sulla rule of thumb Harrell.
- [ ] **AC-v2-3**: NB-3 chiuso. Cap.24.1 riga 239 non contiene piu' "MAE alla scadenza"; sostituita con nomenclatura coerente con la regola operativa. Termine "MAE" assente come nomenclatura per il rendimento di chiusura virtuale forzata nel resto del documento.
- [ ] **AC-v2-4**: RP-1 chiuso. $T_{budget}$ aggiornato a 75-80 ore in Cap.26.2 e Cap.26.5. Cap.23.6 aggiornato sulla tensione risolta. Scelta del valore preciso motivata nel REPORT.
- [ ] **AC-v2-5**: RP-3 chiuso. Cap.25.5 dichiara $\theta_{CV}=0,5$ come starting point Parte VII; Cap.26.5 con flag corrispondente. REPORT annota la riconsiderazione Parte VII.
- [ ] **AC-v2-6**: nessuna regressione sugli AC v1 (52 voci: 47 OK + 4 PARZIALI promossi a OK ove possibile + 1 condizionale gia' OK). Verifica esplicita nel REPORT con tabella prima/dopo dove rilevante.
- [ ] **AC-v2-7**: REPORT_CAP_05.md include sezione "## Iterazione 2 -- risposta ai finding di Review v1 + decisioni RP-1/RP-3" con: per ogni finding, modifica applicata + misura prima/dopo + AC chiuso. Sezione "Decisioni rilevanti" aggiornata con la scelta motivata per NB-2 (opzione a/b/c).
- [ ] **AC-v2-8**: CARRYOVER.md aggiornato se nuovi M-promemoria emergono (atteso: nessuno; Review v1 ha dichiarato "Nessun M-promemoria nuovo emerge da questa Review per Parte VI/VII").
- [ ] **AC-v2-9**: 00_indice.md riflette CAP-05 IN REVIEW v2.
- [ ] **AC-v2-10**: tutti i file modificati committati e pushati su origin/main. Working tree pulito sui file di task. `tasks/DEV_STATUS.md` = `READY_FOR_REVIEW` dopo la consegna.

### Pipeline rework v2

Development v2 (3 fix BUG REALI + RP-1 + RP-3 + correzione REPORT) -> Review v2 di CAP-05 -> atteso PASS in 1 iterazione (correzioni chirurgiche tutte $\leq$ 10 righe; nessuna decisione di design strutturale aperta dopo la scelta NB-2).
