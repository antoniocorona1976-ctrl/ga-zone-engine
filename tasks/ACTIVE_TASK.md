# TASK ATTIVO: CAP-06 -- Parte VI del documento metodologico v2 (Emissione segnali e lifecycle senza execution)

**Assegnato da**: Planner
**Output atteso**: `docs/methodology_v2/CAP_06_parte_VI.md`
**Stato**: NUOVO

## Obiettivo

Scrivere la Parte VI del documento metodologico v2: **pipeline di inference real-time, politica anti-doppio-segnale, gestione dell'operativita' su mobile, monitoraggio del lifecycle in produzione**. Questa Parte risponde a: (1) come il bundle frozen prodotto da Parte V viene messo in funzione su feed real-time Directa per produrre segnali pubblicabili (Cap.27); (2) come il motore garantisce determinismo e unicita' del segnale attivo in presenza di emissioni candidate concorrenti, integrando il vincolo normativo $|\mathcal{A}(t)| \leq 1$ di Cap.6.3 di Parte II con una politica esplicita di non-refresh e di gestione dei tie (Cap.28); (3) come il payload del segnale viene reso operativamente fruibile da un operatore retail che esegue manualmente dal cellulare, estendendo (senza duplicare) il formato Telegram a 9 voci di Cap.9.2 di Parte II con un layout mobile-first (Cap.29); (4) quali metriche di lifecycle sono calcolate live in produzione, come si articola la dashboard di sintesi e su quali condizioni si emettono alert di deriva (Cap.30).

La Parte VI **non contiene** la validazione OOS finale con DSR/PBO/bootstrap stazionario (Parte VII Cap.31-34), i gate decisionali di go-live (Parte VII Cap.36), il processo di freezing del bundle (Parte VII Cap.35), ne' le specifiche di interfaccia (Appendici C-D-E). La Parte VI **non contiene** alcuna logica di esecuzione ordini, order routing, gestione dei fill, slippage di esecuzione, calcolo di posizione netta: il sistema rimane "solo emissione" come dichiarato in Cap.1 di Parte I. La Parte VI **non contiene** logica di re-training del GA in production: il bundle frozen non viene riottimizzato in live; l'unica ricalibrazione real-time consentita riguarda i parametri runtime del modello di volatilita' (EGARCH), trattata in Cap.27 come cadenza fissa + trigger di break parametrico.

La Parte VI consuma tutti i blocchi formali delle Parti I-V come input. Dalla Parte I: vincoli operatore retail mobile, sessione 8:00-22:00 CET, infrastruttura locale PC i5-7200U/8GB per inference, tick FIB 5 pt, filtro $\geq 80$ pt, canale Telegram come unico canale operatore. Dalla Parte II: payload del segnale esteso a 11 campi (Iterazione 4), state machine 1 non-terminale + 6 terminali, vincolo segnale unico attivo, condizioni di emissione in AND logico, formato Telegram a 9 voci, replay deterministico bit-exact. Dalla Parte III: EGARCH(1,1) con $D$ via AIC/BIC su finestra rolling $W=210.000$, classificazione regime calmo/turbolento, catalogo 37 feature causali normalizzate, algoritmo pivot detection. Dalla Parte IV: geometria zone, target strutturali/sintetici, stop strutturali/sintetici, Cox cause-specific, filtri Cap.20. Dalla Parte V: bundle frozen come output del walk-forward nested (Cap.25), parametri congelati di Cap.26.5, definizione delle metriche di fitness e lifecycle che Cap.30 calcola live.

**Impatto sul GA**. La Parte VI rende **operativamente sfruttabili** in produzione le decisioni del GA. Senza Cap.27 il bundle frozen e' un artefatto inerte; senza Cap.28 il vincolo $|\mathcal{A}(t)| \leq 1$ resta normativo ma non operazionalizzato in presenza di emissioni candidate multiple; senza Cap.29 il payload formale non raggiunge l'operatore con la chiarezza necessaria per una decisione manuale; senza Cap.30 la deriva fra performance del GA in walk-forward e performance live resta invisibile, impedendo qualunque feedback diagnostico. La Parte VI **non** modifica la fitness, **non** modifica il cromosoma, **non** modifica gli operatori GA; **abilita** la messa in produzione del bundle e definisce gli alert che, in caso di deriva persistente, impongono ritraining del GA (la decisione operativa di ritraining e' Parte VII Cap.36 + materia post-go-live).

## Eredita' obbligatoria da CAP-01, CAP-02, CAP-03, CAP-04, CAP-05

Tutte le eredita' qui elencate devono essere citate esplicitamente almeno una volta nei capitoli di Parte VI che le consumano. La mancata citazione in un capitolo pertinente e' un finding di Review.

### Da CAP-01 (Parte I)

1. **Vincolo "solo emissione, nessuna esecuzione"** (Cap.1 PI). Cap.27 non contiene order routing/fill/slippage di esecuzione. Citazione obbligatoria in apertura di Cap.27 e di Cap.29.
2. **Profilo operatore retail mobile** (Cap.2 PI): 1 contratto/volta, esecuzione manuale da cellulare, separazione segnale/gestione posizione. Cap.29 deve citare esplicitamente l'esecuzione manuale come vincolo di leggibilita' del payload.
3. **Sessione operativa 8:00-22:00 CET** (Cap.1 PI, Q-01 chiusa). Cap.27 dichiara la finestra di emissione del motore; Cap.30 dichiara la finestra di calcolo delle metriche live coerente con la finestra operativa.
4. **Infrastruttura locale PC i5-7200U/8GB** (Cap.3 PI). Cap.27 deve dichiarare che l'inference real-time gira in locale sul PC dell'operatore (no cloud) e che la latenza end-to-end del motore (ingest -> emissione) deve restare entro vincoli compatibili con feed Directa DAPI (vincolo qualitativo; il valore numerico empirico di latenza Telegram $L_{max}=30$s resta carryover Appendice E -- M-2 OPEN).
5. **Broker Directa SIM DAPI** (Cap.3 PI). Cap.27 cita DAPI come fonte feed real-time; nessuna chiamata broker per execution.
6. **Tick FIB = 5 punti** (Cap.5 PI). Tutti i livelli mostrati in payload Telegram (Cap.29) sono multipli di 5; ogni esempio numerico in Cap.27-30 rispetta il tick.
7. **Filtro emissione $\geq 80$ pt** (Cap.5 PI). Cap.27 cita il filtro come vincolo strutturale gia' incorporato nel bundle frozen (no ricontrollo runtime separato).
8. **Commissioni 5 EUR/op** (Cap.2 PI). Cap.30 deve includere il commissioning come componente del calcolo live del net return (coerente con Cap.24.1 di Parte V $f_1 = E[R_{gross}|executed] - 2c$ con $c=1$ pt equivalente per commissione FIB moltiplicatore 5 EUR/punto).
9. **Canale Telegram unico canale operatore** (Cap.3 PI). Cap.29 dichiara Telegram come unica via di output verso l'operatore; nessuna dashboard mobile lato Directa; eventuale dashboard di Cap.30 e' lato motore (server-side/PC dell'operatore via interfaccia web locale o file di log), non sul cellulare.

### Da CAP-02 (Parte II)

10. **Payload del segnale esteso** (Cap.6.1 PII Iterazione 4): tupla $\mathcal{S}$ con i campi `signal_id, timestamp_emission, direction, entry_zone, target_1, target_2, target_2_type` $\in \{\text{structural, synthetic}\}$, `stop_loss, stop_type` $\in \{\text{structural, synthetic}\}$, `setup_class` $\in \{\text{directional, trade\_range}\}$, $\Delta t_{cromosoma}$, $T_{touch}^{max}$. Cap.27 deve dichiarare che il payload prodotto dal motore in inference live e' **bit-exact identico** al payload formale di Cap.6.1 PII (no campi aggiuntivi runtime, no campi mancanti, no rinominazione).
11. **State machine 1 non-terminale + 6 terminali** (Cap.7 PII). Cap.27 cita la state machine come driver dello stato persistente del segnale dopo l'emissione; Cap.30 calcola le frequenze di stato terminale live.
12. **Vincolo segnale unico attivo $|\mathcal{A}(t)| \leq 1$** (Cap.6.3 PII). Cap.28 **estende operativamente** questo vincolo definendo il comportamento del motore quando emerge un candidate signal concorrente: regole di no-refresh, regole di tie-break deterministico per emissioni simultanee, regole di superamento (un segnale attivo non viene mai sostituito da un nuovo segnale: lo "slot" resta occupato fino a transizione terminale). La citazione del vincolo Cap.6.3 PII e' obbligatoria in apertura di Cap.28.
13. **Condizioni di emissione in AND logico** (Cap.8 PII + Cap.20 PIV): $E_{vol} \land E_{liq} \land E_{dist}^{\sigma} \land E_{80pt} \land E_{surv}$. Cap.27 cita l'AND come gating runtime per la decisione di emissione; le soglie $\tau_{vol}, \tau_{liq}, \tau_{dist}^{\sigma}, \tau_{surv}$ sono lette dal bundle frozen (output Parte V).
14. **Pubblicazione Telegram 9 voci ordinate** (Cap.9.2 PII Iterazione 5). Cap.29 **estende senza duplicare** il formato Telegram con un layout mobile-first: ordinamento dei campi per priorita' di lettura mobile (es. direzione + entry_zone + target_1 in alto), uso di abbreviazioni standard, gestione visualizzazione su singolo schermo cellulare. Cap.29 cita esplicitamente Cap.9.2 PII come riferimento normativo del contenuto del messaggio; non lo riscrive.
15. **Notifica `trigger_event` separata** (Cap.7 PII + Cap.9 PII implicito). Cap.29 dichiara il formato della notifica `trigger_event` come messaggio Telegram aggiuntivo (distinto dall'emissione iniziale), con anti-duplicato e signal_id che lega il `trigger_event` al segnale originario.
16. **Replay deterministico bit-exact** (Cap.10 PII). Cap.27 dichiara che il logging real-time produce file di replay che, ricalcolati offline sullo stesso feed e stesso bundle, riproducono il payload identico al bit. Cap.30 fa riferimento ai log di replay come fonte canonica delle metriche live.
17. **Submacchina position lifecycle post-target_1** (Cap.11 PII): $\pi_{t_2|t_1}$, MFE, MAE, stop post-target_1. Cap.30 traccia live queste metriche come contributo al monitoraggio (eredita' Cap.24.3 PV: tracking, non obiettivi diretti).

### Da CAP-03 (Parte III)

18. **EGARCH(1,1) con $D$ via AIC/BIC e finestra rolling $W=210.000$** (Cap.13 PIII + Cap.26.5 PV congelati). Cap.27 dichiara: in inference live il modello EGARCH gira con i parametri stimati nel fold di calibrazione corrente; la cadenza di ricalibrazione runtime in production e' definita in Cap.27.5 come parametro temporale fisso (es. ricalibrazione settimanale o mensile; valore numerico **da decidere** come parametro di tuning operativo, dichiarato come variabile di tuning non congelata in Parte VI) **piu'** un trigger di break parametrico real-time che forza ricalibrazione anticipata se il flag di break supera la soglia. Il flag e la soglia sono definiti in Cap.27.5; il flag viene **calcolato live** in Cap.30 sul feed real-time, con alert al superamento. (Risoluzione M-2 v2 CAP-03 carryover.)
19. **Classificazione regime calmo/turbolento** (Cap.14 PIII). Cap.27 dichiara che la classificazione di regime gira live sul feed real-time con i parametri $\bar{\sigma}_s, p=0{,}75, N_{reg}=20, T_{persist}=10$ congelati in Cap.26.5 PV; Cap.30 traccia la distribuzione live dei regimi per fold-equivalente di produzione.
20. **Catalogo 37 feature causali normalizzate** (Cap.15.2 PIII). Cap.27 cita il catalogo come input al calcolo feature live; il vincolo di causalita' $x_t \in \mathcal{F}_{t-1}$ vale anche in inference (le feature sono calcolate sulla barra appena chiusa, non sulla barra in formazione).
21. **Algoritmo pivot detection** (Cap.15.3 PIII). Cap.27 cita l'algoritmo come componente del calcolo feature live; il vincolo di Cap.16.2 PIV sulla sospensione strutturale in warm-up vale anche in produzione.

### Da CAP-04 (Parte IV)

22. **Geometria zone con $p_{ref}$ via timestamp di conferma del pivot** (Cap.16.1 PIV). Cap.27 cita il meccanismo di selezione $p_{ref}$ live: la zona di entry e' costruita attorno al $p_{ref}$ corrente, aggiornato deterministicamente alla conferma di un nuovo pivot piu' recente.
23. **Target strutturali e sintetici, stop strutturali e sintetici** (Cap.17-18 PIV). Cap.27 cita la derivazione dei campi `target_1, target_2, target_2_type, stop_loss, stop_type` del payload come funzione deterministica del cromosoma frozen, di $p_{ref}$, di $\hat{\sigma}_{\text{pt}}(t)$ e della geometria dei pivot al tempo $t$.
24. **Modello Cox cause-specific** (Cap.19 PIV). Cap.27 cita il modello come componente del filtro $E_{surv}$ in inference: $\hat{p}_{hit}$ e' calcolato live sul vettore di feature $\tilde{\mathbf{x}}_t$ del candidato segnale; i coefficienti del Cox sono quelli del fold di calibrazione corrente (stratificazione regime di Cap.25.5 PV preservata).
25. **Filtri Cap.20 PIV** ($\tau_{vol}, \tau_{liq}, \tau_{dist}^{\sigma}, \tau_{surv}$). Cap.27 cita i filtri come gating runtime dell'emissione; i valori delle soglie sono letti dal bundle frozen.

### Da CAP-05 (Parte V)

26. **Bundle frozen come output del walk-forward nested** (Cap.25-26 PV). Cap.27 dichiara che il bundle frozen consumato in inference live e' l'output dell'ultimo fold di calibrazione del walk-forward nested (Cap.25.1 PV con $F=8$ fold provvisori, $W_{in}=105.840$ barre in-sample, $W_{oos}=52.920$ barre OOS, purge $P_{purge}=4.200$, embargo $P_{emb}=4.200$). La promozione del bundle a "produzione" e' decisione di Parte VII Cap.31-36 (Cap.27 cita il rinvio).
27. **Tabella congelati Cap.26.5 PV**. Cap.27 cita la tabella come fonte normativa di tutti i parametri runtime del motore (sia parametri del modello sia geni cromosoma del bundle frozen specifico in produzione).
28. **Fitness multi-obiettivo $M=5$ obiettivi** (Cap.24.1 PV): $f_1$ expected net return, $f_2$ target_1 hit rate, $f_3$ invalidation rate pre-touch, $f_4$ max drawdown intraday, $f_5$ stabilita' cross-regime. Cap.30 calcola **live** le contropartite di $f_1, f_2, f_3, f_4$ su finestra rolling di produzione (Cap.30.2 definira' la finestra) e le confronta con la distribuzione cross-fold del walk-forward; $f_5$ richiede dati cross-regime aggregati e viene calcolato come metrica a piu' bassa frequenza (Cap.30.3).
29. **Metriche tracciate (non obiettivi diretti) Cap.24.3 PV**: $\pi_{t_2|t_1}$, MFE/MAE aggregati, $f_{stop|t_1}$. Cap.30 traccia queste metriche live.
30. **Penalita' integrate nella fitness** (Cap.24.2 PV): $E_{max}=5$ segnali/sessione, $E_{min}=0{,}2$ segnali/sessione, $E_{exp,max}=0{,}30$ frazione expired post-trigger; coefficienti $\alpha_{max}, \alpha_{min}, \alpha_{exp}$ congelati. Cap.30 calcola live la frequenza di emissione e produce alert se la frequenza esce dai bound $[E_{min}, E_{max}]$ in modo persistente (deriva del cromosoma rispetto al training).
31. **Seed bundle frozen** (Cap.26.8 PV). Cap.27 dichiara che il seed e' parte dell'identita' del bundle frozen e viene loggato in ogni emissione live per garantire replay (eredita' 16).
32. **No incorporazione DSR/PBO come obiettivi diretti** (Cap.24.7 PV, eredita' Cap.5 PI). Cap.30 **non calcola live DSR/PBO** (sono gate post-selezione di Parte VII); Cap.30 traccia solo le metriche di fitness e lifecycle definite in Parte V.

## M-promemoria pertinenti CAP-06

L'Orchestratore della sessione corrente verifica che ogni M-promemoria sotto sia trattato esplicitamente nel sotto-capitolo indicato. Un M-promemoria pertinente a CAP-06 non integrato nel Development e' un finding di Review.

| M-ID | Origine | Contenuto | Pertinenza CAP-06 | Sotto-capitolo destinazione |
|------|---------|-----------|-------------------|------------------------------|
| M-2 | Review v1 CAP-02 | Verifica empirica latenza Telegram $L_{max}=30$s | **NO** -- resta carryover Appendice E (OPEN). Cap.29 puo' citare il vincolo $L_{max}$ qualitativamente come obiettivo di latenza Telegram, ma **non lo risolve numericamente**: il valore numerico empirico resta materia di Appendice E | Citazione qualitativa in Cap.29.1; nessuna risoluzione numerica |
| M-2 v2 CAP-03 | Review v2 CAP-03 | Cadenza ricalibrazione EGARCH in production + trigger break parametrico real-time | **SI'** -- residuo CLOSED-CAP-05 parziale. Cap.27.5 dichiara la cadenza temporale fissa (parametro di tuning operativo, valore numerico **da decidere** rinviato come variabile non congelata di Parte VI) + meccanismo di trigger break parametrico (definizione del flag); Cap.30.4 calcola live il flag su feed real-time e produce alert al superamento della soglia | Cap.27.5 (definizione meccanismo) + Cap.30.4 (calcolo live del flag + alert) |
| M-16 condizionale | Review v1 CAP-05 (Cap.25.8 trigger) | Estensione a Cox time-varying coefficients se test Schoenfeld viola sistematicamente in >50% dei fold | **NO** -- resta OPEN-CONDIZIONALE Parte VII. Cap.27 cita il Cox con stratificazione regime di Cap.25.5 PV come modello in inference; eventuale evoluzione a time-varying e' decisione Parte VII | Nessuna integrazione in Parte VI; rinvio esplicito a Parte VII |

Tutti gli altri M-promemoria storici (M-1 v2 CAP-03, M-4, M-5, M-6, M-7, M-8, M-9, M-10, M-11, M-12, M-13, M-14, M-15) sono gia' CLOSED su CAP-04 o CAP-05 e non richiedono trattamento in Parte VI.

### Decisioni di scope del Planner sui M-promemoria

Tre decisioni di scope sono prese qui dal Planner per evitare ambiguita' nel Development. Il Developer **non puo' deviare** da queste decisioni; eventuali divergenze sono finding di Review.

**(a) Collocazione M-2 v2 CAP-03 residuo (cadenza EGARCH production + trigger break parametrico).** Decisione: **Cap.27 dichiara il meccanismo, Cap.30 calcola live il flag**. Cap.27.5 contiene (i) la dichiarazione della cadenza temporale fissa di ricalibrazione EGARCH in production (parametro temporale, valore numerico non congelato qui ma dichiarato come variabile di tuning operativo `T_{recal,EGARCH}` con dominio temporale tipico settimanale-mensile e default proposto per il primo run di produzione, riconsiderato in Parte VII post-go-live) e (ii) la definizione del **flag di break parametrico** $B(t)$ come funzione dei residui standardizzati del modello in finestra recente (es. test di Nyblom 1989 sulla stabilita' dei parametri di un modello GARCH, oppure test di Engle-Sheppard 2001 sui residui standardizzati, oppure equivalenti consolidati; il Developer sceglie la formulazione con citazione bibliografica esplicita) e (iii) la soglia $\theta_B$ del flag come parametro di tuning operativo (analogo a `T_{recal,EGARCH}`). Cap.30.4 (i) calcola live $B(t)$ sul feed real-time, (ii) traccia la serie temporale di $B(t)$, (iii) produce un alert se $B(t) > \theta_B$ per piu' di una finestra di persistenza $T_{B,persist}$ (parametro di tuning operativo). La separazione "definizione meccanismo in Cap.27 / calcolo live + alert in Cap.30" e' dichiarata esplicitamente nel testo di Cap.27.5 e Cap.30.4.

**(b) Cap.28 anti-doppio-segnale: relazione con vincolo $|\mathcal{A}(t)| \leq 1$ di Cap.6.3 PII.** Decisione: **Cap.28 estende Cap.6.3 PII operativamente, senza modificare il vincolo normativo**. Cap.28 contiene: (i) citazione esplicita di Cap.6.3 PII come vincolo normativo gia' fissato; (ii) la **politica di non-refresh**: un segnale attivo $\mathcal{S}_a$ non viene mai sostituito da un candidato $\mathcal{S}_c$ anche se $\mathcal{S}_c$ sarebbe ammissibile per i filtri AND di Cap.8 PII + Cap.20 PIV. Il candidato $\mathcal{S}_c$ viene **scartato silenziosamente** e loggato (no notifica Telegram, no marcatura). Lo slot resta occupato fino a transizione terminale del segnale attivo; (iii) la **politica di tie-break deterministico per emissioni simultanee** $|\mathcal{A}(t)| = 0$ con due o piu' candidati ammissibili nello stesso istante (edge case improbabile col vincolo $|\mathcal{A}(t)| \leq 1$ ma teoricamente possibile se in scenari multi-cromosoma futuri il bundle frozen contenesse piu' cromosomi che generano segnali simultanei -- non e' il caso del bundle frozen di Parte V che produce **un solo cromosoma vincente**, ma il vincolo deterministico va comunque dichiarato): regola di selezione = cromosoma con $\hat{p}_{hit}$ piu' alto sul candidato; in caso di tie, cromosoma con setup_class `directional` prima di `trade_range`; in caso di tie ulteriore, cromosoma con $\Delta t_{cromosoma}$ piu' breve; in caso di tie residuo (improbabile), ordinamento lessicografico sul signal_id (generato come hash deterministico dei campi del payload). La regola completa va dichiarata anche se il bundle frozen di Parte V produce un solo cromosoma vincente, perche' (i) Cap.28 e' parte di un contratto di Parte VI valido anche in scenari multi-cromosoma futuri e (ii) replay deterministico bit-exact richiede che ogni edge case sia gestito deterministicamente.

**(c) Cap.29 -- payload visualizzato vs payload formale.** Decisione: **Cap.29 non duplica Cap.9.2 PII, riordina visivamente le SOLE 9 voci di Cap.9.2 PII Iterazione 5; nessun campo aggiuntivo nel messaggio Telegram**. Cap.29 contiene: (i) citazione esplicita di Cap.9.2 PII Iterazione 5 a 9 voci come formato normativo del contenuto del messaggio; (ii) un **layout mobile-first** che riordina **esattamente le 9 voci di Cap.9.2 PII Iterazione 5** per priorita' di lettura mobile, **senza introdurre $\Delta t_{cromosoma}$ ne' $T_{touch}^{max}$** (Cap.9.2 PII paragrafo 253 li esclude esplicitamente dal messaggio Telegram in quanto parametri tecnici del modello, rilevanti per il log interno ma non per la decisione operativa dell'operatore). L'ordinamento mobile-first proposto e': posizione 1 direction (LONG/SHORT in caps, prima riga), posizione 2 entry_zone (banda numerica formattata), posizione 3 target_1 (con distanza in pt), posizione 4 stop_loss (con distanza in pt), posizione 5 target_2 + qualificatore target_2_type, posizione 6 stop_type, posizione 7 setup_class, posizione 8 timestamp_emission, posizione 9 signal_id (footer abbreviato accettabile, oppure prima voce di intestazione; il Developer sceglie la convenzione di posizionamento coerente con Cap.9.2 PII Iterazione 5 senza introdurre ambiguita'). **Vincolo assoluto**: il numero totale di voci pubblicate nel messaggio Telegram resta **esattamente 9**, identico a Cap.9.2 PII Iterazione 5; nessuna voce aggiuntiva, nessuna voce omessa; (iii) **abbreviazioni standard** (es. "TGT1", "TGT2", "SL") per evitare lo scroll del messaggio su schermi mobile tipici (375-414 px di larghezza); (iv) **gestione duplicati di lettura** (operatore che apre Telegram piu' volte): il messaggio resta invariato (no edit, no append), il signal_id e' incluso per disambiguazione; (v) **notifica trigger_event** come messaggio Telegram separato (eredita' 15) con riferimento esplicito al signal_id originario. Cap.29 **non** introduce campi nuovi nel payload formale (che resta come da Cap.6.1 PII Iterazione 4); aggiunge solo la **rappresentazione**. La distinzione "payload formale (immutabile) vs rappresentazione mobile (cosmetica)" e' dichiarata esplicitamente. **Nota di rework v2 CAP-06**: la decisione (c) originaria della v1 elencava erroneamente $\Delta t_{cromosoma}$ e $T_{touch}^{max}$ fra le posizioni 5-9 del layout; tale formulazione e' stata riallineata via A (riallineamento a Cap.9.2 PII paragrafo 253) come risposta al BUG REALE #2 della Review v1. Nessuna patch retroattiva a CAP-02 e' introdotta.

## Capitoli da produrre (~6 pagine totali in italiano formale)

### Capitolo 27 -- Pipeline di inference real-time (~1,5 pp)

**Scope.** Definire la pipeline operativa che, dato il bundle frozen di Parte V e il feed Directa DAPI live, produce in inference real-time i segnali pubblicabili. La pipeline opera in **modalita' emissione-only** (no execution layer). La cadenza di ricalibrazione runtime del modello EGARCH e il meccanismo di trigger break parametrico sono dichiarati qui (M-2 v2 CAP-03 residuo).

**Contenuto obbligatorio.**

- **27.1 Architettura della pipeline (~0,3 pp)**: descrivere i blocchi sequenziali della pipeline: (i) ingest feed Directa DAPI (eredita' 5); (ii) calcolo barre 1-min e aggregazione (eredita' Cap.12 PIII); (iii) calcolo feature live sul catalogo 37 (eredita' 20, con vincolo causalita' $x_t \in \mathcal{F}_{t-1}$); (iv) inference EGARCH(1,1) con parametri runtime (eredita' 18); (v) classificazione regime live (eredita' 19); (vi) algoritmo pivot detection live (eredita' 21); (vii) costruzione candidate signal dal bundle frozen (eredita' 22-25); (viii) valutazione filtri AND $E_{vol} \land E_{liq} \land E_{dist}^{\sigma} \land E_{80pt} \land E_{surv}$ (eredita' 13); (ix) emissione Telegram via Cap.29 in caso di pass. Dichiarare esplicitamente che la pipeline gira **in locale sul PC dell'operatore** (eredita' 4) e che non chiama API broker per execution (eredita' 1).
- **27.2 Latenza end-to-end e vincoli temporali (~0,2 pp)**: dichiarare il vincolo qualitativo di latenza fra ingest e pubblicazione Telegram (compatibile con feed DAPI). Citare M-2 OPEN come carryover di Appendice E per la verifica numerica empirica di $L_{max}$.
- **27.3 Bundle frozen come input invariante (~0,2 pp)**: il bundle frozen consumato in inference live e' l'output dell'ultimo fold di calibrazione del walk-forward nested di Parte V (eredita' 26), promosso a "produzione" attraverso i gate decisionali di Parte VII Cap.36 (citazione del rinvio). I parametri del bundle (sia parametri del modello sia geni del cromosoma frozen) sono letti dalla tabella congelati di Cap.26.5 PV (eredita' 27) **senza** modifica runtime. Il seed e' loggato in ogni emissione (eredita' 31).
- **27.4 Pipeline di emissione del payload (~0,2 pp)**: il payload del segnale prodotto in inference live e' **bit-exact identico** al payload formale di Cap.6.1 PII (eredita' 10), prodotto dalla derivazione deterministica di Cap.17-18 PIV (eredita' 23) applicata a $p_{ref}$ corrente (eredita' 22) e ai geni $b, k_{t2}, d_{stop,\sigma}$ del cromosoma frozen. Logging deterministico bit-exact in coerenza con Cap.10 PII (eredita' 16).
- **27.5 Cadenza ricalibrazione EGARCH in production + trigger break parametrico (~0,6 pp)** (chiusura M-2 v2 CAP-03 residuo, decisione di scope (a)): la sotto-sezione contiene (i) la cadenza temporale fissa di ricalibrazione EGARCH come parametro di tuning operativo `T_{recal,EGARCH}` (dominio temporale tipico settimanale-mensile, default proposto per il primo run di produzione **da decidere e dichiarato come variabile di tuning non congelata in Parte VI**, riconsiderato in Parte VII post-go-live); (ii) la definizione del **flag di break parametrico** $B(t)$ come funzione dei residui standardizzati del modello EGARCH in finestra recente (Developer sceglie la formulazione con citazione bibliografica esplicita: opzioni possibili includono il test di Nyblom 1989 sulla stabilita' dei parametri di un modello GARCH, oppure il test di Engle-Sheppard 2001 sui residui standardizzati, oppure equivalenti consolidati); (iii) la soglia $\theta_B$ del flag come parametro di tuning operativo, con dichiarazione che il valore numerico **non e' congelato in Parte VI** ma e' rinviato come variabile di tuning operativo; (iv) il **meccanismo di trigger anticipato**: se $B(t) > \theta_B$ per piu' di $T_{B,persist}$ barre consecutive (con $T_{B,persist}$ parametro di tuning operativo), la ricalibrazione EGARCH e' anticipata rispetto a `T_{recal,EGARCH}`; (v) la separazione esplicita "Cap.27.5 dichiara il meccanismo; Cap.30.4 calcola live $B(t)$ e produce l'alert".

**Vincoli trasversali Cap.27**: nessun valore numerico congelato di Parte VI; tutti i parametri di tuning operativo (`T_{recal,EGARCH}`, $\theta_B$, $T_{B,persist}$) sono dichiarati con dominio temporale/dimensionale e default proposto per il primo run, **non congelati**. Citazione esplicita di Cap.6.1 PII (payload formale), Cap.8 PII (filtri AND), Cap.10 PII (replay bit-exact), Cap.13 PIII (EGARCH), Cap.14 PIII (regime), Cap.16 PIV ($p_{ref}$), Cap.17-18 PIV (target/stop), Cap.19-20 PIV (Cox + filtri), Cap.25-26 PV (walk-forward + bundle frozen).

### Capitolo 28 -- Politica anti-doppio-segnale (~1,5 pp)

**Scope.** Estendere operativamente il vincolo normativo $|\mathcal{A}(t)| \leq 1$ di Cap.6.3 PII con (i) la politica di non-refresh in presenza di candidati concorrenti con segnale gia' attivo e (ii) la regola di tie-break deterministico per emissioni simultanee (edge case). La regola e' dichiarata anche se il bundle frozen di Parte V produce un solo cromosoma vincente: il replay deterministico bit-exact richiede gestione deterministica di ogni edge case (decisione di scope (b)).

**Contenuto obbligatorio.**

- **28.1 Citazione del vincolo normativo Cap.6.3 PII (~0,2 pp)**: $|\mathcal{A}(t)| \leq 1$ e' vincolo gia' fissato in Parte II e non viene modificato. Cap.28 lo **estende operativamente**.
- **28.2 Politica di non-refresh (~0,5 pp)**: enunciato formale: se al tempo $t$ esiste un segnale attivo $\mathcal{S}_a$ (i.e. $|\mathcal{A}(t)| = 1$) e un candidato $\mathcal{S}_c$ ammissibile per i filtri AND di Cap.8 PII + Cap.20 PIV viene generato dal bundle frozen, allora $\mathcal{S}_c$ e' **scartato silenziosamente**: nessuna notifica Telegram (no notifica all'operatore), nessuna marcatura speciale, **logging in file di replay** con causa esplicita (terminologia da scegliere dal Developer, coerente con Cap.10 PII; suggerito `dropped_due_to_active_signal` o equivalente). Lo slot resta occupato dal segnale attivo $\mathcal{S}_a$ fino a transizione a uno dei 6 stati terminali (Cap.7 PII). Solo dopo la transizione terminale il motore puo' emettere nuovi segnali. Motivazione: l'operatore esegue manualmente da cellulare (eredita' 2); un refresh continuo del segnale con sovrascrittura confonderebbe la decisione di esecuzione manuale e violerebbe il principio "1 contratto/volta" (eredita' 2). Citazione esplicita di Cap.6.3 PII e Cap.7 PII.
- **28.3 Tie-break deterministico per emissioni simultanee (~0,5 pp)** (edge case multi-cromosoma): enunciato formale della regola di selezione quando $|\mathcal{A}(t)| = 0$ e due o piu' candidati ammissibili sono generati nello stesso istante. La regola e' dichiarata anche se il bundle frozen di Parte V produce un solo cromosoma vincente (motivazione: replay deterministico bit-exact + estendibilita' del contratto). Ordine di tie-break:
  1. cromosoma con $\hat{p}_{hit}$ piu' alto sul candidato corrispondente (eredita' Cap.19.5 PIV, output del Cox cause-specific);
  2. in caso di tie su $\hat{p}_{hit}$ (entro tolleranza numerica $\epsilon_{p}$, parametro tecnico tipo $10^{-6}$, dichiarato in Cap.28.3 ma **non congelato** in Parte VI), cromosoma con `setup_class` $=$ `directional` prima di `trade_range`;
  3. in caso di tie ulteriore, cromosoma con $\Delta t_{cromosoma}$ piu' breve (eredita' Cap.6.1 PII);
  4. in caso di tie residuo (improbabile), ordinamento lessicografico crescente del signal_id (generato come hash deterministico dei campi del payload secondo Cap.10 PII, eredita' 16).
- **28.4 Determinismo del replay e logging (~0,3 pp)**: la pipeline registra in log di replay, per ogni candidato (anche scartato), il signal_id (se generato), il timestamp, lo stato di gating (es. `accepted`, `dropped_due_to_active_signal`, `dropped_due_to_tiebreak_loss`, `dropped_due_to_filter_fail` -- terminologia di esempio, il Developer puo' adottarla o variarla con coerenza interna), e gli output dei filtri AND. Il replay offline sullo stesso feed e bundle riproduce **bit-exact** la stessa sequenza di emissioni/scarti (eredita' 16). Citazione di Cap.10 PII.

**Vincoli trasversali Cap.28**: nessun valore numerico congelato di Parte VI; $\epsilon_p$ tolleranza numerica per tie-break dichiarata come parametro tecnico **non congelato**. La citazione di Cap.6.3 PII, Cap.7 PII, Cap.10 PII e' obbligatoria. La politica di non-refresh deve essere argomentata **operativamente** (eredita' 2 esecuzione manuale mobile), non solo formalmente.

### Capitolo 29 -- Gestione dell'operativita' su mobile (~1,5 pp)

**Scope.** Estendere il formato Telegram di Cap.9.2 PII a 9 voci con un layout mobile-first che ottimizza la leggibilita' su cellulare per un operatore retail che esegue manualmente. Cap.29 **non duplica** Cap.9.2 PII (che resta normativo per il contenuto); aggiunge la **rappresentazione visiva** ottimizzata per mobile (decisione di scope (c)). Nessun campo nuovo nel payload formale.

**Contenuto obbligatorio.**

- **29.1 Vincoli operativi mobile-first (~0,3 pp)**: citazione esplicita di Cap.2 PI (operatore retail mobile, 1 contratto/volta, esecuzione manuale, eredita' 2), Cap.3 PI (Telegram unico canale operatore, eredita' 9), Cap.9.2 PII (formato 9 voci, eredita' 14). Dichiarare il vincolo qualitativo di latenza Telegram come obiettivo qualitativo (M-2 OPEN -- la verifica numerica empirica resta Appendice E; Cap.29 cita il vincolo qualitativamente). Vincoli di leggibilita' mobile: larghezza schermo tipica 375-414 px, font monospaziato Telegram, messaggio leggibile senza scroll orizzontale, contenuto critico visibile senza scroll verticale eccessivo.
- **29.2 Layout mobile-first del messaggio di emissione (~0,5 pp)**: ordinamento delle 9 voci di Cap.9.2 PII per priorita' di lettura mobile:
  1. **direzione** (LONG/SHORT in caps, prima riga, evidenza visiva);
  2. **entry_zone** (banda numerica formattata, multipli di 5 pt, ad esempio "13.250 -- 13.260");
  3. **target_1** in pt e in distanza dal centro della banda (ad esempio "TGT1: 13.350 (+95 pt)");
  4. **stop_loss** in pt e in distanza (ad esempio "SL: 13.200 (-55 pt)");
  5. **target_2** con tipo (`structural` / `synthetic`) (ad esempio "TGT2: 13.450 (S)");
  6. **$\Delta t_{cromosoma}$** in minuti di trading (ad esempio "EXP: 60min post-trig");
  7. **$T_{touch}^{max}$** in minuti di trading (ad esempio "WAIT: 30min pre-trig");
  8. **setup_class** (`directional` / `trade_range`);
  9. **timestamp_emission** in CET (ad esempio "EMIT: 10:42:15 CET").
  Il signal_id e' incluso come **footer compatto** (es. ultima riga, abbreviato come "ID: a3f7..."). Includere un **esempio numerico completo** del messaggio formattato in Cap.29 (livelli multipli di 5 pt, eredita' 6).
- **29.3 Notifica trigger_event come messaggio separato (~0,3 pp)** (eredita' 15): definire il formato della notifica `trigger_event` Telegram come **messaggio separato** dall'emissione originaria, con riferimento esplicito al signal_id e contenuto minimo: timestamp del trigger, prezzo di trigger, $\Delta t$ pre-trigger (i.e. $t_{exec} - t_{emission}$, eredita' Cap.24.5 PV N-4 v2), conferma dello stato `active` post-trigger. Esempio numerico del messaggio.
- **29.4 Gestione duplicati di lettura e idempotenza (~0,2 pp)**: l'operatore puo' aprire Telegram piu' volte; il messaggio resta invariato (no edit del messaggio originale, no append). Il signal_id include hash deterministico dei campi (eredita' Cap.10 PII) per disambiguazione visiva fra emissioni successive. Nessuna notifica Telegram di "stato corrente del segnale" oltre alle 3 notifiche standard (emissione, trigger_event, transizione terminale): l'operatore segue lo stato sul terminale Telegram in modo statico, senza polling.
- **29.5 Notifica di transizione terminale (~0,2 pp)**: messaggio Telegram alla transizione a uno dei 6 stati terminali (eredita' 11). Contenuto minimo: signal_id, stato terminale (`target_1_hit`, `stopped`, `invalidated`, `missed_target`, `expired`, `revoked`), prezzo del trigger se applicabile, $R_{gross}$ in pt (positivo o negativo). Esempio numerico.

**Vincoli trasversali Cap.29**: nessun campo nuovo nel payload formale (resta come da Cap.6.1 PII Iterazione 4, eredita' 10). Tutti i valori numerici di esempio rispettano il tick FIB 5 pt (eredita' 6). Citazione esplicita di Cap.9.2 PII (contenuto formale), Cap.2 PI (mobile manuale), Cap.3 PI (Telegram).

### Capitolo 30 -- Monitoraggio del lifecycle in produzione (~1,5 pp)

**Scope.** Definire le metriche di lifecycle calcolate live in produzione, la dashboard di sintesi (lato motore, non sul cellulare), gli alert su deriva. Le metriche di Cap.30 sono **counterpart live** delle metriche di Parte V Cap.24 (fitness $f_1$-$f_4$) e delle metriche tracciate Cap.24.3 PV. Cap.30 traccia anche il flag di break parametrico $B(t)$ definito in Cap.27.5 (decisione di scope (a)). Nessun calcolo live di DSR/PBO (eredita' 32, gate Parte VII).

**Contenuto obbligatorio.**

- **30.1 Metriche di fitness live (~0,4 pp)**: definire la **finestra rolling di produzione** $W_{prod}$ su cui calcolare le contropartite live di $f_1, f_2, f_3, f_4$ (eredita' 28). $W_{prod}$ e' un parametro di tuning operativo, dichiarato con dominio temporale tipico (es. 21 sessioni rolling = 1 mese di trading), default proposto **non congelato** in Parte VI, riconsiderato post-go-live. Calcolare:
  - $f_1^{live}(t) = E[R_{net} | executed]$ su $W_{prod}$;
  - $f_2^{live}(t)$ = target_1 hit rate su $W_{prod}$;
  - $f_3^{live}(t)$ = invalidation rate pre-touch su $W_{prod}$;
  - $f_4^{live}(t)$ = maximum drawdown intraday dell'equity sintetica calcolata su $W_{prod}$;
  - le metriche live includono il commissioning $c=1$ pt equivalente (eredita' 8) coerente con Cap.24.1 PV.
- **30.2 Confronto con distribuzione cross-fold del walk-forward (~0,3 pp)**: per ciascuna $f_m^{live}(t)$, confronto con la distribuzione $\{f_{m,k}\}_{k=1}^{F}$ delle stesse metriche aggregate sui $F=8$ fold del walk-forward nested di Parte V (eredita' Cap.25.1 PV con $F=8$ provvisorio). Definire la **soglia di deriva**: alert se $f_m^{live}(t)$ esce dall'intervallo interquartile $[Q_1, Q_3]$ della distribuzione cross-fold per piu' di $T_{drift,persist}$ giorni di trading consecutivi (parametro di tuning operativo, default proposto non congelato in Parte VI). Citazione esplicita Cap.24, Cap.25 PV.
- **30.3 Metriche tracciate (lifecycle aggiuntive, eredita' 29) (~0,2 pp)**: tracciare live $\pi_{t_2|t_1}^{live}(t)$, MFE/MAE aggregati live, $f_{stop|t_1}^{live}(t)$ (frazione di stop post-target_1). Queste metriche sono **reporting**, non alert (eredita' Cap.24.3 PV).
- **30.4 Calcolo live del flag di break parametrico $B(t)$ e alert (~0,3 pp)** (chiusura M-2 v2 CAP-03 residuo, decisione di scope (a)): calcolare live $B(t)$ secondo la definizione di Cap.27.5, tracciare la serie temporale, produrre alert se $B(t) > \theta_B$ per piu' di $T_{B,persist}$ barre consecutive (eredita' Cap.27.5). L'alert puo' anticipare la ricalibrazione EGARCH rispetto alla cadenza fissa `T_{recal,EGARCH}` (eredita' Cap.27.5). Citazione esplicita Cap.27.5.
- **30.5 Frequenza di emissione e alert di deriva del cromosoma (~0,2 pp)** (eredita' 30): tracciare live la frequenza di emissione/sessione $r_{emit}^{live}(t)$; alert se $r_{emit}^{live}(t) > E_{max} = 5$ segnali/sessione (eredita' Cap.24.2 PV $E_{max}$ congelato in Cap.26.5 PV) o $r_{emit}^{live}(t) < E_{min} = 0{,}2$ segnali/sessione (eredita' $E_{min}$ congelato in Cap.26.5 PV) per piu' di $T_{emit,persist}$ giorni di trading consecutivi (parametro di tuning operativo, default proposto non congelato). Motivazione: una frequenza fuori bound indica deriva del cromosoma frozen rispetto al regime di mercato corrente; la decisione di ritraining e' Parte VII Cap.36 (citazione del rinvio). Citazione esplicita di Cap.26.5 PV e Cap.24.2 PV.
- **30.6 Dashboard di sintesi lato motore (~0,1 pp)**: la dashboard di Cap.30 e' **lato motore** (PC dell'operatore, interfaccia web locale o file di log + visualizzazione offline), **non sul cellulare**. Il cellulare riceve solo Telegram (eredita' 9). La dashboard espone tabelle/grafici delle metriche live $f_1$-$f_4$ + tracciate + $B(t)$ + $r_{emit}$ + lista degli alert attivi. Nessuna interazione execution-side (eredita' 1).

**Vincoli trasversali Cap.30**: nessun valore numerico congelato di Parte VI per i parametri di tuning operativo ($W_{prod}$, $T_{drift,persist}$, $T_{emit,persist}$, $T_{B,persist}$, $\theta_B$); tutti dichiarati con dominio e default proposto. Le soglie $E_{max}=5$, $E_{min}=0{,}2$, $E_{exp,max}=0{,}30$ sono ereditate da Cap.26.5 PV gia' congelate (eredita' 30) e Cap.30 le **usa** senza ridichiararle. Nessun calcolo live di DSR/PBO (eredita' 32). Citazione esplicita Cap.24 PV (fitness), Cap.25 PV (walk-forward $F=8$ fold), Cap.26.5 PV (soglie congelate), Cap.27.5 (definizione $B(t)$).

## Acceptance criteria -- tutti devono essere soddisfatti per PASS in Review

Acceptance criteria numerati e oggettivi, verificabili dal Reviewer in modo binario (OK/NOT OK).

### Cap.27

- **AC-27-1**: Cap.27 dichiara esplicitamente in apertura il vincolo "solo emissione, nessuna esecuzione" (eredita' 1) e che la pipeline gira in locale sul PC dell'operatore (eredita' 4).
- **AC-27-2**: Cap.27.1 elenca i blocchi sequenziali della pipeline in modo completo: ingest DAPI -> calcolo barre -> calcolo feature live (catalogo 37) -> EGARCH live -> classificazione regime live -> pivot detection live -> costruzione candidate signal -> filtri AND -> emissione Telegram.
- **AC-27-3**: Cap.27.4 dichiara che il payload prodotto in inference live e' **bit-exact identico** al payload formale di Cap.6.1 PII (eredita' 10).
- **AC-27-4**: Cap.27.3 dichiara che il bundle frozen e' input invariante (parametri letti dalla tabella Cap.26.5 PV senza modifica runtime; seed loggato per replay) e cita Cap.25-26 PV.
- **AC-27-5**: Cap.27.5 contiene tutti i 5 elementi della chiusura M-2 v2 CAP-03 residuo: (i) cadenza temporale fissa `T_{recal,EGARCH}` come parametro di tuning operativo non congelato; (ii) definizione del flag di break parametrico $B(t)$ con citazione bibliografica esplicita (Nyblom 1989 o Engle-Sheppard 2001 o equivalente consolidato); (iii) soglia $\theta_B$ come parametro di tuning non congelato; (iv) meccanismo di trigger anticipato; (v) separazione esplicita Cap.27.5 (meccanismo) / Cap.30.4 (calcolo live + alert).
- **AC-27-6**: Cap.27 cita esplicitamente Cap.6.1 PII, Cap.8 PII, Cap.10 PII, Cap.13 PIII, Cap.14 PIII, Cap.16 PIV, Cap.17-18 PIV, Cap.19-20 PIV, Cap.25-26 PV (almeno una citazione per ciascuna).
- **AC-27-7**: nessun valore numerico congelato di Parte VI in Cap.27. Tutti i parametri di tuning operativo (`T_{recal,EGARCH}`, $\theta_B$, $T_{B,persist}$) sono dichiarati con dominio + default proposto + marcatura "non congelato".

### Cap.28

- **AC-28-1**: Cap.28.1 cita esplicitamente Cap.6.3 PII come vincolo normativo gia' fissato e dichiara che Cap.28 lo **estende operativamente** senza modificarlo.
- **AC-28-2**: Cap.28.2 enuncia formalmente la politica di non-refresh: un candidato $\mathcal{S}_c$ ammissibile in presenza di segnale attivo $\mathcal{S}_a$ e' scartato silenziosamente (no Telegram), loggato con causa esplicita. Lo slot resta occupato fino a transizione terminale. La motivazione operativa (eredita' 2 esecuzione manuale mobile, 1 contratto/volta) e' presente.
- **AC-28-3**: Cap.28.3 enuncia formalmente la regola di tie-break deterministico in 4 livelli ordinati: (1) $\hat{p}_{hit}$ massimo; (2) `directional` prima di `trade_range`; (3) $\Delta t_{cromosoma}$ minimo; (4) ordinamento lessicografico signal_id. La regola e' dichiarata anche se il bundle frozen di Parte V produce un solo cromosoma vincente (motivazione: replay deterministico + estendibilita').
- **AC-28-4**: Cap.28.4 dichiara che il replay offline sullo stesso feed e bundle riproduce bit-exact la stessa sequenza di emissioni e scarti, con campi di log di gating esplicitati. Citazione Cap.10 PII.
- **AC-28-5**: nessun valore numerico congelato di Parte VI in Cap.28. $\epsilon_p$ tolleranza numerica e' dichiarata come parametro tecnico non congelato.

### Cap.29

- **AC-29-1**: Cap.29 cita esplicitamente Cap.9.2 PII (formato 9 voci) come riferimento normativo del contenuto e dichiara che Cap.29 **non duplica** Cap.9.2 ma estende la rappresentazione visiva mobile-first.
- **AC-29-2**: Cap.29 non introduce campi nuovi nel payload formale (resta come da Cap.6.1 PII Iterazione 4, eredita' 10). La distinzione "payload formale (immutabile) vs rappresentazione mobile (cosmetica)" e' dichiarata esplicitamente.
- **AC-29-3**: Cap.29.2 fornisce l'ordinamento delle 9 voci per priorita' mobile (lista numerata 1-9), include un esempio numerico completo del messaggio formattato con valori multipli di 5 pt (eredita' 6).
- **AC-29-4**: Cap.29.3 definisce il formato della notifica `trigger_event` come messaggio Telegram **separato**, con riferimento al signal_id originario, $\Delta t$ pre-trigger esplicito (eredita' Cap.24.5 PV N-4 v2). Esempio numerico presente.
- **AC-29-5**: Cap.29.5 definisce il formato della notifica di transizione terminale (eredita' 11): signal_id, stato terminale (uno dei 6), $R_{gross}$ in pt. Esempio numerico presente.
- **AC-29-6**: Cap.29.1 cita esplicitamente $L_{max}$ come obiettivo qualitativo e rinvia a Appendice E (M-2 OPEN) per la verifica numerica; **non risolve** numericamente $L_{max}$ in Parte VI.

### Cap.30

- **AC-30-1**: Cap.30.1 definisce le 4 metriche live $f_1^{live}, f_2^{live}, f_3^{live}, f_4^{live}$ come contropartite di Cap.24.1 PV (eredita' 28), include il commissioning $c=1$ pt equivalente (eredita' 8 + Cap.24.1 PV).
- **AC-30-2**: Cap.30.2 definisce la soglia di deriva basata sull'intervallo interquartile $[Q_1, Q_3]$ della distribuzione cross-fold dei $F=8$ fold (eredita' 26 + Cap.25.1 PV con $F=8$ provvisorio), con persistenza $T_{drift,persist}$ come parametro di tuning operativo non congelato.
- **AC-30-3**: Cap.30.3 traccia le metriche di lifecycle aggiuntive (eredita' 29 + Cap.24.3 PV): $\pi_{t_2|t_1}^{live}$, MFE/MAE, $f_{stop|t_1}^{live}$. Esplicitato che sono reporting, non alert.
- **AC-30-4**: Cap.30.4 contiene il calcolo live di $B(t)$ (definito in Cap.27.5) e l'alert su soglia $\theta_B$ + persistenza $T_{B,persist}$. Citazione esplicita di Cap.27.5.
- **AC-30-5**: Cap.30.5 traccia la frequenza di emissione $r_{emit}^{live}$ e produce alert se fuori da $[E_{min}, E_{max}]$ (eredita' Cap.26.5 PV con $E_{max}=5$, $E_{min}=0{,}2$ gia' congelati: non ricongelati, riusati) per piu' di $T_{emit,persist}$ giorni di trading. Citazione esplicita di Cap.26.5 PV e Cap.24.2 PV.
- **AC-30-6**: Cap.30.6 dichiara che la dashboard e' **lato motore** (PC dell'operatore, non sul cellulare); il cellulare riceve solo Telegram (eredita' 9). Nessuna interazione execution-side (eredita' 1).
- **AC-30-7**: Cap.30 dichiara esplicitamente di **non calcolare** live DSR/PBO (eredita' 32 + Cap.24.7 PV); il rinvio a Parte VII Cap.31-36 e' esplicito.
- **AC-30-8**: nessun valore numerico nuovo congelato di Parte VI per i parametri di tuning operativo ($W_{prod}$, $T_{drift,persist}$, $T_{emit,persist}$, $T_{B,persist}$). $E_{max}=5$, $E_{min}=0{,}2$, $E_{exp,max}=0{,}30$ sono ereditate da Cap.26.5 PV senza ridichiarazione.

### Trasversali

- **AC-T-1**: tutte le 32 eredita' elencate sopra (CAP-01..CAP-05) sono citate esplicitamente almeno una volta nei capitoli di Parte VI che le consumano. Mancata citazione in un capitolo pertinente = finding di Review.
- **AC-T-2**: gli M-promemoria pertinenti CAP-06 sono integrati: M-2 v2 CAP-03 residuo trattato in Cap.27.5 + Cap.30.4 (chiusura). M-2 e M-16 condizionale **non** sono integrati in Parte VI (restano OPEN/OPEN-CONDIZIONALE con rinvio esplicito ad Appendice E e Parte VII rispettivamente; menzionati nel testo dove pertinente).
- **AC-T-3**: nessuna logica di execution ordini in Parte VI. Cap.27, Cap.28, Cap.29, Cap.30 non contengono order routing, gestione fill, slippage di esecuzione, calcolo posizione netta. Verifica negativa: il documento NON deve usare termini come "order routing", "fill", "slippage", "broker execution", "posizione netta" in senso operativo execution (citazioni di Cap.1 PI "solo emissione" sono ammesse e necessarie).
- **AC-T-4**: nessun re-training del GA in production trattato in Parte VI. La decisione di ritraining post-deriva e' rinviata esplicitamente a Parte VII Cap.36 + materia post-go-live. Cap.30 produce alert; non chiude il loop.
- **AC-T-5**: tutti gli esempi numerici del documento usano valori multipli di 5 (tick FIB, eredita' 6).
- **AC-T-6**: tutti i parametri di tuning operativo di Parte VI (`T_{recal,EGARCH}`, $\theta_B$, $T_{B,persist}$, $W_{prod}$, $T_{drift,persist}$, $T_{emit,persist}$, $\epsilon_p$) sono dichiarati con dominio + default proposto + marcatura esplicita **"non congelato in Parte VI, riconsiderato post-go-live"**. Nessun valore numerico di questi parametri entra nella tabella congelati di Parte V (che resta invariata) o in una tabella congelati di Parte VI (che **non esiste**: Parte VI non congela parametri).
- **AC-T-7**: lunghezza target rispettata: Cap.27 ~1,5 pp; Cap.28 ~1,5 pp; Cap.29 ~1,5 pp; Cap.30 ~1,5 pp; totale Parte VI ~6 pp.
- **AC-T-8**: italiano formale, tecnico, conciso. Nessun paragrafo divulgativo; nessuna ridondanza vs Parti precedenti (Parte VI cita ma non riscrive).
- **AC-T-9**: REPORT_CAP_06.md ha le 5 sezioni del formato supervisore: Cosa e' stato prodotto / Ipotesi di partenza / Decisioni rilevanti / Misura prima/dopo / Domande aperte + Criterio di rollback.
- **AC-T-10**: 00_indice.md aggiornato per riflettere Parte VI come "IN REVIEW v1" (questa modifica e' del Developer, non del Planner).
- **AC-T-11**: tutti i file modificati committati e pushati su `origin/main`. Working tree pulito.

## Out-of-scope -- Development NON include queste cose in CAP-06

- **Execution ordini, order routing, fill, slippage di esecuzione, broker execution API** -> resta fuori dal documento metodologico v2 (Cap.1 PI vincola "solo emissione").
- **Validazione OOS finale, DSR, PBO, bootstrap stazionario, gate decisionali go-live** -> Parte VII Cap.31-36.
- **Processo di freezing del bundle, hash di riferimento, regola di sostituzione** -> Parte VII Cap.35.
- **Re-training del GA in production** -> Parte VII Cap.36 + post-go-live. Cap.30 emette alert su deriva ma non chiude il loop.
- **Specifiche di API Directa, qualificazione Darwin/DAPI/Visual Trader** -> Appendice C.
- **Specifiche di storico Portara/CQG** -> Appendice D.
- **Setup Telegram bot, gestione chat ID, schema messaggio dettaglio implementativo** -> Appendice E. Cap.29 definisce il **layout mobile-first** ma non il setup tecnico del bot.
- **Verifica numerica empirica di $L_{max}=30$s latenza Telegram** -> Appendice E (M-2 OPEN). Cap.29 cita il vincolo qualitativamente.
- **Estensione a Cox time-varying coefficients** -> Parte VII (M-16 condizionale, attivo solo se Schoenfeld viola sistematicamente in >50% dei fold).
- **Re-derivazione di payload, state machine, condizioni di emissione, formato Telegram a 9 voci** -> Parte II (Cap.6-10). Parte VI **cita** ma non **riscrive**.
- **Re-derivazione di EGARCH, regime, feature, pivot** -> Parte III (Cap.12-15). Parte VI cita.
- **Re-derivazione di geometria zone, target, stop, Cox, filtri Cap.20** -> Parte IV. Parte VI cita.
- **Re-derivazione di cromosoma, NSGA-II, fitness, walk-forward, calibrazione/congelamento** -> Parte V. Parte VI cita.
- **Congelamento di parametri di tuning operativo di Parte VI** -> non avviene in Parte VI. La tabella congelati di Parte V (Cap.26.5) resta invariata; Parte VI non ne aggiunge una propria. I parametri di tuning operativo sono **non congelati**, riconsiderati post-go-live.
- **Patch retroattive a CAP-01, CAP-02, CAP-03, CAP-04, CAP-05**: nessuna modifica retroattiva alle Parti gia' chiuse PASS. Eventuali incoerenze rilevate da Developer di Parte VI che richiedono mini-patch retroattive vanno segnalate come M-promemoria nuovi nel REPORT_CAP_06; la decisione di applicare la mini-patch spetta al supervisore in checkpoint Review.

## Done when

Il documento Parte VI risponde senza ambiguita' a queste domande:

1. **Come gira il bundle frozen in inference real-time?** (Cap.27.1)
2. **Da dove vengono i parametri runtime del motore in produzione?** (Cap.27.3)
3. **Il payload emesso in live e' identico al payload formale di Parte II?** (Cap.27.4)
4. **Con che cadenza si ricalibra EGARCH in produzione e quando si attiva un trigger di break parametrico anticipato?** (Cap.27.5) -- chiusura M-2 v2 CAP-03 residuo.
5. **Cosa succede se al tempo $t$ c'e' un segnale attivo e il bundle frozen vorrebbe emettere un nuovo segnale?** (Cap.28.2: no-refresh, scarto silenzioso, log)
6. **Cosa succede se due candidati ammissibili sono generati nello stesso istante e non c'e' segnale attivo?** (Cap.28.3: tie-break deterministico 4 livelli)
7. **Come si traduce il payload formale di Cap.6.1 PII in un messaggio Telegram leggibile su cellulare?** (Cap.29.2: layout mobile-first 9 voci ordinate per priorita')
8. **L'operatore riceve un solo messaggio per segnale o piu' notifiche?** (Cap.29: 3 notifiche standard -- emissione, trigger_event, transizione terminale)
9. **Quali metriche si calcolano live in produzione e con quale frequenza?** (Cap.30.1-30.3: $f_1$-$f_4$ + tracciate + $B(t)$ + $r_{emit}$ su $W_{prod}$)
10. **Quando si emette un alert di deriva?** (Cap.30.2: fuori IQR cross-fold per $T_{drift,persist}$ giorni; Cap.30.4: $B(t) > \theta_B$ per $T_{B,persist}$ barre; Cap.30.5: $r_{emit}$ fuori $[E_{min}, E_{max}]$ per $T_{emit,persist}$ giorni)
11. **DSR/PBO si calcolano live?** (Cap.30.7: NO, gate Parte VII)
12. **La dashboard di Cap.30 e' sul cellulare?** (Cap.30.6: NO, lato motore; cellulare riceve solo Telegram)
13. **Cap.30 attiva re-training del GA in caso di deriva?** (No: Cap.30 emette alert; decisione re-training Parte VII Cap.36 + post-go-live)

## Output files attesi

1. `docs/methodology_v2/CAP_06_parte_VI.md` -- italiano formale, ~6 pp (target lunghezza 4 capitoli ~1,5 pp ciascuno).
2. `reports/REPORT_CAP_06.md` -- 5 sezioni formato supervisore:
   - **Cosa e' stato prodotto**: sintesi dei 4 capitoli, scelte di scope applicate.
   - **Ipotesi di partenza**: eredita' da CAP-01..CAP-05 + M-promemoria pertinenti integrati / rinviati.
   - **Decisioni rilevanti**: in particolare le 3 decisioni di scope del Planner (collocazione M-2 v2; estensione operativa Cap.6.3 PII; payload visualizzato vs formale); la scelta della formulazione del flag $B(t)$ (Nyblom o Engle-Sheppard o equivalente con motivazione bibliografica); default proposti dei parametri di tuning operativo con motivazione qualitativa.
   - **Misura prima/dopo**: cosa il GA puo' fare ora che Parte VI esiste rispetto al prima (sintesi: senza Parte VI il bundle frozen e' inerte; con Parte VI il bundle e' messo in produzione con politica di emissione operazionalizzata, layout mobile-first, monitoring live + alert).
   - **Domande aperte**: $L_{max}$ empirico (M-2 OPEN, Appendice E); valori numerici default dei parametri di tuning operativo (riconsiderati post-go-live); attivazione condizionale M-16 (Parte VII).
   - **Criterio di rollback**: condizioni sotto cui Parte VI andrebbe rivista (es. se in Parte VII si decide che il bundle frozen include piu' cromosomi vincenti, la politica di tie-break Cap.28.3 diventa centrale e va testata empiricamente; se in post-go-live la cadenza di ricalibrazione EGARCH si rivela inadeguata, `T_{recal,EGARCH}` viene rivisto; se la dashboard di Cap.30 non riesce a calcolare $B(t)$ in tempo reale su PC i5-7200U, la finestra di calcolo $B(t)$ viene allargata o spostata batch).
3. Aggiornamento `docs/methodology_v2/00_indice.md` -- Parte VI marcata "IN REVIEW v1" dopo Developer (lo stato cambia in PASS dopo Reviewer PASS in chiusura sessione).

## Pipeline attesa

Development v1 -> Review v1 -> [classificazione GA al supervisore se CONDITIONAL/FAIL] -> fix -> ... -> PASS

L'Orchestratore della sessione corrente esegue il check post-Developer (6 controlli del CLAUDE.md) prima di chiamare Reviewer. La chiusura sessione richiede tutte e 7 le condizioni (CLAUDE.md), incluso l'aggiornamento di `tasks/CARRYOVER.md` con i nuovi M-promemoria eventualmente emessi dalla Review di CAP-06.

**Atteso numero di iterazioni**: 1-2 cicli. Parte VI ha complessita' modesta rispetto a Parte V (motore stesso del progetto): consuma eredita' senza ridefinire architettura. Il primo ciclo Review v1 probabilmente trovera' 3-6 finding totali (BUG REALI + MIGLIORA + NEUTRO); la decisione del supervisore sui finding non-BUG seguira' la prassi standard del progetto.

**Criterio di rollback in caso di fallimento**: se Review v2 trova ancora BUG REALI strutturali sui 4 capitoli di Parte VI (es. M-2 v2 CAP-03 non chiuso adeguatamente, politica anti-doppio-segnale non deterministica, layout mobile-first incoerente con Cap.9.2 PII), si valuta uno splitting di Parte VI in Parte VI.A (Cap.27-28 pipeline + anti-doppio-segnale) e Parte VI.B (Cap.29-30 mobile + monitoring), con due cicli Review distinti. Decisione di rollback rinviata al supervisore al primo CONDITIONAL.

---

## Finding di Review da risolvere (rework v2)

Origine: `reviews/REVIEW_CAP_06_review.md` (commit `5b9bc8d`, verdetto **FAIL**). Decisione del supervisore: **passare al Developer tutti i 3 BUG REALI + tutti gli 8 NEUTRO con le soluzioni A/B raccomandate dall'Orchestratore**. La decisione di scope (c) del Planner e' stata riformulata sopra (via A: riallineamento a Cap.9.2 PII paragrafo 253; rimozione di $\Delta t_{cromosoma}$ e $T_{touch}^{max}$ dalle voci pubblicate; 9 voci esatte di Cap.9.2 PII Iterazione 5).

Il Developer deve risolvere **tutti** gli 11 finding sotto e produrre `CAP_06_parte_VI.md` v2 + `REPORT_CAP_06.md` v2 + aggiornamento `00_indice.md` (resta "IN REVIEW Review v2"). Ogni finding deve essere richiamato esplicitamente nel REPORT_CAP_06.md v2 con evidenza puntuale (riga/sezione del documento) di come e' stato risolto.

### BUG REALI (3) -- obbligatori

**Finding #1 -- $f_5$ stabilita' cross-regime omessa in Cap.30 (eredita' 28 violata).**
- **Problema**: il documento v1 Cap.30.1 calcola live $f_1, f_2, f_3, f_4$ ma omette $f_5$. Cap.30.3 v1 contiene metriche di lifecycle (eredita' 29: $\pi_{t_2|t_1}$, MFE/MAE, $f_{stop|t_1}$) confondendola con eredita' 28.
- **Soluzione richiesta**: Cap.30.3 v2 (o nuova sotto-sezione Cap.30.3bis se serve riorganizzare) deve **calcolare live $f_5^{live}(t)$** come counterpart live di $f_5(\theta) = |f_1^{calmo}(\theta) - f_1^{turbolento}(\theta)| / \max(|f_1^{calmo}(\theta)|, |f_1^{turbolento}(\theta)|, 1)$ di Cap.24.1 PV. La metrica deve essere calcolata su segmentazione del fold di produzione $W_{prod}$ per regime calmo vs turbolento (classificazione regime Cap.14 PIII applicata live). Deve avere frequenza piu' bassa di $f_1$-$f_4$ (dichiarata esplicitamente come "metrica a piu' bassa frequenza"). Le metriche di lifecycle aggiuntive (eredita' 29) restano in una sotto-sezione propria (es. Cap.30.3bis o Cap.30.3 mantenuto, con $f_5^{live}$ in posizione separata). Aggiornare di conseguenza dashboard Cap.30.6 (tabella metriche live deve includere $f_5^{live}$).

**Finding #2 -- Cap.29.2 v1 include $\Delta t_{cromosoma}$ in violazione di Cap.9.2 PII; auto-contraddizione interna.**
- **Problema**: Cap.29.2 v1 elenca 9 voci che includono $\Delta t_{cromosoma}$ come voce 7 (`EXP: 60min post-trig`), in violazione di Cap.9.2 PII paragrafo 253. Il paragrafo successivo dello stesso Cap.29.2 v1 dichiara "Delta_t_cromosoma non figura nel messaggio Telegram... Il layout pubblica le 9 voci dichiarate in Cap.9.2; nient'altro" -- auto-contraddizione strutturale.
- **Soluzione richiesta** (via A, supervisore approvato): la decisione di scope (c) del Planner e' stata riformulata sopra. Cap.29.2 v2 deve elencare **esattamente le 9 voci di Cap.9.2 PII Iterazione 5** (verificare il testo esatto di Cap.9.2 PII Iterazione 5 per il conteggio e l'ordinamento), **senza $\Delta t_{cromosoma}$ ne' $T_{touch}^{max}$**, secondo l'ordinamento mobile-first dichiarato nella nuova decisione di scope (c): 1. direction; 2. entry_zone; 3. target_1 (con distanza); 4. stop_loss (con distanza); 5. target_2 + target_2_type; 6. stop_type; 7. setup_class; 8. timestamp_emission; 9. signal_id (in footer compatto oppure prima voce intestazione, Developer sceglie convenzione). Aggiornare l'esempio numerico di Cap.29.2 di conseguenza (rimuovere riga `EXP: 60min post-trig`). Rimuovere il paragrafo auto-contraddittorio "Il campo $T_{touch}^{max}$... la sua presenza nel layout di Cap.29.2 sarebbe estensione..." (riga 166 v1): non e' piu' necessario, perche' il layout v2 non include piu' $\Delta t_{cromosoma}$.

**Finding #3 -- Cap.27.4 dichiara "11 campi" ma ne elenca 12.**
- **Problema**: Cap.27.4 v1 (riga 49) dichiara "$\mathcal{S}$ esteso a 11 campi" ed elenca 12 campi. Il payload di Cap.6.1 PII Iterazione 4 ha effettivamente 12 campi.
- **Soluzione richiesta**: sostituire "11 campi" con "12 campi" in Cap.27.4. **Importante**: l'eredita' 10 di questo `ACTIVE_TASK.md` (riga 35) replica lo stesso errore -- non e' compito del Developer correggere il task, ma e' compito del Developer **non propagare l'errore** nel documento. Il documento v2 deve dichiarare correttamente "12 campi".

### NEUTRO (8) -- approvati dal supervisore con soluzioni A/B

**Finding #4 -- Sessione 8:00-22:00 CET non esplicitata (eredita' 3).** Soluzione **A**: aggiungere una frase esplicita in **Cap.27.1** (es. "La pipeline opera durante la finestra di sessione 8:00-22:00 CET di Cap.1 di Parte I, 840 barre 1-min per sessione") e una in **Cap.30.1** (es. "la finestra rolling $W_{prod}$ aggrega segnali di 21 sessioni di 8:00-22:00 CET, totale 17.640 barre 1-min"). Risolve eredita' 3 violata.

**Finding #5 -- Cap.30.1 cita "Cap.5 PI" come fonte commissioning invece di Cap.2 PI.** Soluzione **A**: sostituire **"(eredita' Cap.5 di Parte I"** con **"(eredita' Cap.2 di Parte I"** nella formula di $R_{net}$ (riga 253 di Cap.30.1). Il valore $c=1$ pt FIB resta invariato.

**Finding #6 -- $W_B$ omesso dalla lista del preambolo (Cap.27.5 lo introduce).** Soluzione **A**: aggiungere $W_B$ alla lista del preambolo (riga 7 di CAP_06_parte_VI.md). La lista diventa di 8 parametri di tuning operativo: $T_{recal,EGARCH}, \theta_B, T_{B,persist}, W_B, W_{prod}, T_{drift,persist}, T_{emit,persist}, \epsilon_p$. La distinzione "parametro tecnico vs parametro di tuning operativo" eventualmente presente nel testo v1 viene rimossa (tutti i parametri non congelati sono di tuning operativo).

**Finding #7 -- Cap.10.4 PII citato come fonte di "fill virtuale" (definizione in Cap.7.3 PII).** Soluzione **B**: sostituire la citazione singola **"(Cap.10.4 di Parte II)"** in Cap.29.5 (riga 227) con **citazione doppia**: "(definizione Cap.7.3 di Parte II; uso nel log di chiusura Cap.10.4 di Parte II)".

**Finding #8 -- Tie-break Cap.28.3: confine $\epsilon_p$ non esplicito.** Soluzione **B**: aggiungere **un paragrafo dopo l'enumerazione dei 4 livelli** (dopo riga 117 di Cap.28.3 v1) che dichiara esplicitamente la **convenzione operativa di tie**: "Il livello $k+1$ del tie-break e' attivato se e solo se la differenza al criterio del livello $k$ e' inferiore o uguale alla tolleranza numerica del livello stesso. Per il livello 1: il candidato $\mathcal{S}_c^*$ e' selezionato a livello 1 se vale $\hat{p}_{hit}(\mathcal{S}_c^*) - \max_{c \neq c^*} \hat{p}_{hit}(\mathcal{S}_c) > \epsilon_p$; altrimenti (cioe' $|\hat{p}_{hit}(\mathcal{S}_{c_1}) - \hat{p}_{hit}(\mathcal{S}_{c_2})| \leq \epsilon_p$ per la coppia in tie) si passa al livello 2. Convenzioni analoghe valgono per i livelli successivi (es. tolleranza di confronto sull'enumerazione discreta di setup_class al livello 2 e' implicita -- confronto categoriale; tolleranza al livello 3 sul confronto intero $\Delta t_{cromosoma}$ e' nulla -- confronto esatto)." La convenzione esplicita e' essenziale per il replay deterministico bit-exact di Cap.10 PII.

**Finding #9 -- Esempi `timestamp_emission` con secondi violano Cap.6.1 PII "minuto chiuso".** Soluzione **A**: sostituire negli esempi:
- Cap.29.2 esempio: `EMIT: 10:42:15 CET` -> `EMIT: 10:42 CET`
- Cap.29.3 esempio: `TRIG: 11:18:00 CET @ 13.255` -> `TRIG: 11:18 CET @ 13.255`
- (eventuali altri esempi con timestamp che includono secondi devono essere normalizzati al formato HH:MM)
Mantenere coerenza con la dichiarazione di Cap.27.4 ("timestamp_emission e' il minuto chiuso CET di emissione").

**Finding #10 -- Cap.30.1 motivazione $W_{prod}=21$ con riferimento improprio a $\eta_{div}$.** Soluzione **B**: rimuovere la parentesi **"($\eta_{div}$ calcolato su $W_{prod}$ corrisponde a circa 21 osservazioni di classificazione sessione)"** dalla motivazione di $W_{prod}$ in Cap.30.1 (riga 249 v1). $\eta_{div}$ in Cap.25.4 PV e' una statistica per-fold, non rolling -- la citazione e' fuorviante. Mantenere il resto della motivazione ("$W_{prod} = 21$ sessioni di trading rolling ($\approx$ 1 mese calendario di FIB), coerente con la cadenza di ricalibrazione EGARCH proposta in Cap.27.5").

**Finding #11 -- Esempio numerico tie-break mancante.** Soluzione **A**: aggiungere **un esempio numerico singolo** dopo l'enumerazione dei 4 livelli e dopo il paragrafo della convenzione tie del Finding #8, in Cap.28.3. Esempio proposto (il Developer puo' rifinirlo): "**Esempio operativo di tie-break livello 1**: al tempo $t$ il bundle frozen genera due candidati simultanei $\mathcal{S}_1$ (LONG directional, $\hat{p}_{hit} = 0{,}72$) e $\mathcal{S}_2$ (SHORT directional, $\hat{p}_{hit} = 0{,}68$). Con $\epsilon_p = 10^{-6}$ vale $|0{,}72 - 0{,}68| = 0{,}04 > \epsilon_p$, quindi il livello 1 risolve il tie: il motore emette $\mathcal{S}_1$ e logga $\mathcal{S}_2$ con `dropped_due_to_tiebreak_loss`."

### Vincoli operativi di rework v2

- Il Developer **non puo' modificare** la struttura dei 4 capitoli (Cap.27/28/29/30) ne' aggiungere nuovi capitoli (eccezione: sotto-sezione interna a Cap.30 per separare $f_5^{live}$ dalle metriche di lifecycle, **e' ammessa**).
- Il Developer **non puo' introdurre patch retroattive a CAP-01..CAP-05** (out-of-scope ribadito).
- Tutti i finding sopra devono essere richiamati esplicitamente nel `REPORT_CAP_06.md` v2 sezione "Decisioni rilevanti prese durante lo sviluppo (rework v2)" con evidenza puntuale di risoluzione.
- L'AC del task v1 restano validi; il Developer deve produrre la **tabella verifica AC v2** nel REPORT v2 dichiarando lo stato di tutti i 38 AC + dei nuovi sotto-AC eventualmente nati dai finding (es. AC-30-3bis su $f_5^{live}$).
- Il commit del rework v2 deve essere `[DEV] CAP-06 v2 rework: 3 BUG REALI + 8 NEUTRO READY_FOR_REVIEW` o equivalente, pushato a origin/main.
