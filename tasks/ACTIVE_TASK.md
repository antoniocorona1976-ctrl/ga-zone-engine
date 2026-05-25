# TASK ATTIVO: CAP-04 -- Parte IV del documento metodologico v2 (Geometria zone, target strutturali, survival)

**Assegnato da**: Planner
**Output atteso**: `docs/methodology_v2/CAP_04_parte_IV.md`
**Stato**: NUOVO

## Obiettivo

Scrivere la Parte IV del documento metodologico v2: **Geometria delle zone di entry, target strutturali, stop strutturali e modello di survival**. Questa parte risponde a: come si costruisce geometricamente la zona di entry attorno a un livello strutturale, come si derivano target_1, target_2 e stop_loss dalla struttura del prezzo, come si modella la probabilita' condizionata di raggiungere il target prima dello stop e prima dello scadere della sessione, come i filtri di emissione basati sul survival completano le condizioni di Cap.8 Parte II, e come il caso trade_range si distingue dal caso directional nella geometria e nel filtro.

La Parte IV non contiene il cromosoma, gli operatori GA, la fitness multi-obiettivo (Parte V), ne' il walk-forward, DSR, PBO (Parti V e VII). Non contiene la calibrazione definitiva dei parametri (Parte V). La Parte IV consuma come input i blocchi quantitativi di Parte III ($\hat{\sigma}_{\text{pt}}(t)$, regime calmo/turbolento, catalogo delle 37 feature causali, algoritmo pivot con $n_c=3$ e $\delta_{pivot}$) e il contratto del segnale di Parte II (payload, state machine, condizioni di emissione $\tau_{vol}$, $\tau_{dist}^{\sigma}$, fill virtuale worst-case, position lifecycle).

**Impatto sul GA**: la Parte IV e' il ponte tra i blocchi quantitativi (Parte III) e il cromosoma (Parte V). Definisce: (1) la costruzione geometrica che il cromosoma parametrizza (centro della zona, larghezza $b$, offsets target e stop); (2) il modello di survival che produce $\Pr(\text{target}_1 \text{ hit} \mid \text{entry}, \hat{\sigma}_{\text{pt}}, R_t)$, consumato dalla fitness e potenzialmente dalla condizione di emissione; (3) il filtro di emissione survival-based che puo' bloccare segnali con probabilita' di successo troppo bassa; (4) la gestione del caso trade_range con eccezione al filtro 80pt. Senza queste definizioni, il cromosoma non ha un dominio geometrico su cui operare e la fitness non ha una stima probabilistica del successo del segnale.

## Eredita' obbligatoria da CAP-01, CAP-02, CAP-03

### Da CAP-01 (Q-01..Q-04 chiuse)

1. **Sessione operativa 8:00-22:00 CET**, finestra unica e continua (Q-01). Il modello di survival opera entro questa finestra; il time-to-expiry e' funzione del tempo residuo di sessione.
2. **Movimento strutturale**: somma moduli swing fra pivot, ancorato al primo min/max post-apertura dalle 8:00 CET (Q-02). I pivot strutturali identificati dall'algoritmo di Cap.15.3 (CAP-03) sono gli input primari per la geometria delle zone.
3. **Parametri GA provvisori**: 128/150/B=2000, congelati in Parte V (Q-03). Il survival model puo' avere parametri propri, anch'essi provvisori.
4. **Cap 2 giorni di trading** dal raw touch (Q-04): il survival deve condizionare la stima alla durata residua ammissibile.
5. **Tick FIB = 5 punti**: tutti i livelli strutturali (entry, target, stop) sono multipli di 5.
6. **Filtro emissione >= 80 punti FIB** su target_1 per setup directional (Cap.5 Parte I).
7. **Banda $b \in \{5, 10, 15, 20, 25, 30, 35, 40\}$** punti FIB, $b_{min}=5$ provvisorio; $d_{stop} > b$ obbligatorio (Cap.6 Parte II).

### Da CAP-02 (Q-05 chiusa)

8. **Payload del segnale (Cap.6)**: tupla strutturata con $p_{ref}$, entry_zone, target_1, target_2, stop_loss, setup_class $\in \{\text{directional}, \text{trade\_range}\}$, $\Delta t_{cromosoma}$, $T_{touch}^{max}$. La Parte IV deve definire come il motore calcola $p_{ref}$, target_1, target_2, stop_loss a partire dalla geometria del prezzo.
9. **State machine (Cap.7)**: 1 non-terminale (active) + 6 terminali. target_1_hit chiude il contratto del segnale. Il survival modella $\Pr(\text{target\_1\_hit} \mid \cdot)$ e $\Pr(\text{stopped} \mid \cdot)$.
10. **Condizioni di emissione (Cap.8)**: $\tau_{vol}(\hat{\sigma}_{\text{pt}}(t_{emission}))$, $\tau_{dist}^{\sigma}$, volume. La Parte IV aggiunge una condizione survival-based che integra (non sostituisce) quelle di Cap.8.
11. **Fill virtuale worst-case (Cap.12.4 CAP-03)**: bordo superiore per long, bordo inferiore per short. Il survival deve condizionarsi al prezzo di fill worst-case, non al centro della zona.
12. **Position lifecycle (Cap.11)**: la submacchina post-target_1 traccia target_2, MFE, MAE. Il survival modella solo l'evento target_1_hit e stopped; il resto e' reporting post-contratto.
13. **Invalidazione strutturale (Cap.7.1-7.2)**: la transizione active -> invalidated pre-touch e' demandata a Parte IV. La Parte IV deve definire le condizioni geometriche sotto le quali un segnale attivo viene invalidato prima del raw touch.

### Da CAP-03

14. **$\hat{\sigma}_{\text{pt}}(t) = \hat{\sigma}(t) \cdot p_t$** (Cap.13.1): stima EGARCH in punti FIB, input primario per la geometria e per il survival.
15. **Classificazione regime $R_t \in \{\text{calmo}, \text{turbolento}\}$** (Cap.14): deterministica, non ottimizzabile dal GA, calcolata su quantili rolling di $\bar{\sigma}_s$. Il survival e i parametri geometrici possono essere condizionali al regime.
16. **Catalogo 37 feature causali** (Cap.15.2): le feature entrano nel survival come predittori. Vincolo $x_t \in \mathcal{F}_{t-1}$.
17. **Algoritmo pivot detection** (Cap.15.3): pivot confermato a $t$ disponibile come feature a $t + n_c + 1$, con $n_c = 3$ e $\delta_{pivot} = 10$pt provvisori. Condizione 4: finestra $[t-n_c, t+n_c]$ intera nella sessione.
18. **Normalizzazione MAD** (Cap.15.4): z-score con mediana e MAD su finestra rolling, sessione-limitata per feature con reset. $T_{warmup,\text{norm}} = 100$ barre unusable. Il survival consuma feature gia' normalizzate.
19. **$T_{warmup,\text{EMA}} = 74$ barre unusable** (Cap.15.2.1): le prime 100 barre di sessione (max tra $T_{warmup,\text{EMA}}$ e $T_{warmup,\text{norm}}$) sono `unusable` per il training. Il survival non puo' emettere stime valide prima di $T_{warmup,\text{norm}}$.

### M-promemoria censiti dalle Review precedenti

| M-ID | Origine | Contenuto | Pertinenza CAP-04 |
|------|---------|-----------|-------------------|
| M-2 | Review v1 CAP-02 | Verifica empirica latenza Telegram ($L_{max}=30$s) | NO -- carryover Appendice E |
| M-4 | Review v4 CAP-01 | Tasso di rimpiazzo NSGA-II che giustifica baseline 12.800-25.600 min | NO -- carryover Parte V (Cap.23) |
| M-5 | Q-06 / C-4.3 | Benchmark rolling vs expanding vs EWMA con Inoue-Rossi (2011); rollback automatico | NO -- carryover Parte V (Cap.25) |
| M-6 | Q-09 / C-7.3 | Classificazione regime media vs mediana; test di stabilita' | NO -- carryover Parte V (Cap.25 o Cap.26) |
| N-1 (v2) | Review v2 CAP-03 | Asimmetria tracking stopped vs target_*_hit (MFE post-stop) | NO -- carryover Parte V (Cap.24 fitness) |
| N-2 (v1) | Review v1 CAP-02 | Netto non registrato nel log di chiusura | NO -- carryover Parte VII |
| N-3 (v1) | Review v1 CAP-02 | `executable_rate` nomenclatura post-eliminazione guardie | NO -- carryover Parte V/VI |
| N-4 (v2) | Review v2 CAP-02 | Log chiusura: $\Delta t$ pre-trigger non esplicitato come campo | NO -- carryover Parte V |
| N-5 (v2) | Review v2 CAP-02 | Coda bassa volatilita': floor $\tau_{vol,low}$ | NO -- trattato in Cap.13.6 CAP-03; congelamento Parte V |
| M-1 (v2 CAP-03) | Review v2 CAP-03 | Pivot inizio/fine sessione non confermabili (condizione 4 Q-08) | **SI'** -- Cap.16. La geometria delle zone deve dichiarare come si comporta l'ancoraggio quando il pivot piu' recente e' della sessione precedente (prima barra = nessun pivot confermato ancora). |
| M-2 (v2 CAP-03) | Review v2 CAP-03 | Cadenza ricalibrazione EGARCH in production non specificata | NO -- carryover Parte V/VI |
| O-2 (v4 CAP-02) | Review v4 CAP-02 | Preview fill rule Cap.7.3 non allineata con worst-case Cap.12.4 | **SI'** (indiretto) -- la Parte IV formalizza la geometria completa e il survival usa il fill worst-case; nessun rinvio aggiuntivo necessario, basta coerenza. |

## Capitoli da produrre (~12 pagine totali in italiano formale)

### Capitolo 16 -- Definizione delle zone di entry (~2.5 pp)

Definire formalmente la costruzione geometrica della zona di entry long e short:
- **Ancoraggio strutturale**: il prezzo di riferimento $p_{ref}$ e' derivato dai pivot strutturali confermati (Cap.15.3 CAP-03). Specificare: quale pivot determina $p_{ref}$ (ultimo confermato, o combinazione), come si gestisce il caso in cui nessun pivot e' ancora confermato nella sessione corrente (warm-up + condizione 4 Q-08: M-1 v2 CAP-03), e come si gestisce il caso di pivot della sessione precedente.
- **Larghezza della banda**: $b \in \{5, 10, 15, 20, 25, 30, 35, 40\}$ punti FIB, parametro del cromosoma. La zona e' $[p_{ref} - b, p_{ref} + b]$ con tutti i livelli multipli di 5. Ribadire la cardinalita' $(2b/5)+1$ livelli discreti.
- **Direzione**: per segnale long, il raw touch avviene quando il prezzo scende nella zona (entry below $p_{ref}$); per short, quando il prezzo sale nella zona (entry above $p_{ref}$). Formalizzare la condizione di raw touch in termini di OHLC della barra 1-min.
- **Invalidazione strutturale pre-touch (carryover Cap.7.1-7.2 CAP-02)**: definire le condizioni geometriche che producono la transizione active -> invalidated prima del raw touch. Almeno: (a) il prezzo si allontana dalla zona oltre una soglia ($d_{inv}$ parametro del cromosoma); (b) formazione di un nuovo pivot strutturale che rende obsoleta la zona corrente. Dichiarare i parametri come provvisori, congelamento in Parte V.
- **Condizione di sessione**: il segnale non puo' essere emesso se il tempo residuo di sessione e' inferiore a una soglia minima $T_{min,session}$ (parametro del cromosoma, provvisorio). La zona non viene costruita a fine sessione.
- **Coerenza con fill virtuale worst-case (Cap.12.4 CAP-03)**: una volta che il raw touch avviene, il fill e' al bordo piu' sfavorevole. La geometria deve specificare quale bordo e' il peggiore per ciascuna direzione (gia' definito in Cap.12.4; qui si riconferma).

### Capitolo 17 -- Target strutturali (~2 pp)

Definire la derivazione dei livelli target dalla struttura del prezzo:
- **target_1**: livello strutturale primario, derivato dalla geometria dei pivot (prossimo pivot nella direzione del segnale, o livello di supporto/resistenza confermato). Specificare l'algoritmo di selezione del target fra i livelli candidati. Il target_1 e' multiplo di 5.
- **Vincolo minimo 80 punti FIB** per setup directional: $|\text{target\_1} - p_{ref}| \geq 80$ punti. Se nessun livello strutturale soddisfa il vincolo, il segnale non viene emesso.
- **target_2**: secondo livello strutturale, informazione pubblicata (non variabile di lifecycle). $|\text{target\_2}| > |\text{target\_1}|$ nella direzione del segnale. Specificare l'algoritmo di selezione. target_2 e' multiplo di 5.
- **Condizione di distanza in sigma-units (Cap.8 Parte II)**: $|\text{target\_1} - p_{ref}| / \hat{\sigma}_{\text{pt}}(t_{emission}) \geq \tau_{dist}^{\sigma}$. Mostrare che il filtro 80pt e la condizione sigma sono vincoli separati e indipendenti: il piu' restrittivo domina.
- **Determinismo**: dato lo storico OHLC e i pivot confermati, la selezione del target e' univocamente determinata.

### Capitolo 18 -- Stop strutturali (~2 pp)

Definire la derivazione dello stop dalla struttura del prezzo:
- **stop_loss**: livello strutturale nella direzione opposta al target, derivato dalla geometria dei pivot o da una regola basata su $\hat{\sigma}_{\text{pt}}(t)$. Specificare l'algoritmo. Lo stop e' multiplo di 5.
- **Vincolo geometrico $d_{stop} > b$** (eredita' Cap.6 Parte II): obbligatorio, cromosomi violanti non ammessi.
- **Separazione dallo stop personale dell'operatore**: lo stop strutturale e' parte del contratto del segnale; l'operatore puo' adottare uno stop personale piu' stretto, ma questa decisione e' fuori scope dal motore (Cap.11 Parte II, position lifecycle).
- **Relazione stop-target**: dichiarare il rapporto $d_{stop}/d_{target}$ come grandezza osservabile (risk-reward ratio strutturale). Non fissare un vincolo rigido sul ratio: e' parametro che il GA ottimizza implicitamente attraverso la fitness. Dichiarare che un eventuale vincolo floor/cap sul ratio e' materia di Parte V.
- **Stop e regime**: dichiarare se lo stop strutturale e' condizionale al regime calmo/turbolento. Se si': il cromosoma puo' specificare parametri di stop distinti per regime ($d_{stop,calmo}$, $d_{stop,turbolento}$), come per $\tau_{vol}$.

### Capitolo 19 -- Modello di survival per il target (~2.5 pp)

Definire il modello probabilistico che stima la probabilita' condizionata di raggiungere target_1 prima dello stop:
- **Variabile obiettivo**: tempo $\tau$ dal fill virtuale all'evento terminale (target_1_hit o stopped), osservato nello storico di backtest.
- **Evento concorrente**: il target e lo stop sono rischi concorrenti (competing risks). Il survival modella $\Pr(\text{target\_1\_hit prima di stopped} \mid \mathbf{x}_t, \hat{\sigma}_{\text{pt}}(t), R_t, T_{residuo})$, dove $\mathbf{x}_t$ e' il vettore delle feature causali normalizzate (Cap.15), $R_t$ e' il regime, $T_{residuo}$ e' il tempo residuo di sessione (o di validita' del segnale, max 2 gg trading).
- **Modello candidato**: specificare la classe di modello (Cox proportional hazards, modello parametrico Weibull/log-normal, o survival forest). Dichiarare la scelta come aperta con selezione in Parte V via criterio di validazione OOS. Fornire la formulazione matematica del modello candidato primario.
- **Feature input**: sottoinsieme delle 37 feature causali, selezionato dal cromosoma (Parte V) o per wrapper (Parte VII). La Parte IV definisce quali feature sono ammissibili come input al survival e come vengono consumate (normalizzate, gia' in z-score MAD).
- **Calibrazione**: specificare che il survival e' calibrato sui dati di backtest della finestra in-sample del walk-forward, separatamente per ciascun fold. Cadenza fold-per-fold (coerenza con Cap.13.3 CAP-03, C-4.2).
- **Condizione di censoring**: segnali che raggiungono expiry senza hit ne' stop sono censurati a destra.
- **Output**: $\hat{S}(t | \mathbf{x}) = \Pr(\tau > t | \mathbf{x})$ -- funzione di survival condizionata; e $\hat{p}_{hit} = \Pr(\text{target\_1\_hit prima di stopped} \mid \mathbf{x}, T_{residuo})$ -- probabilita' di successo del segnale.
- **Determinismo e causalita'**: il modello consuma solo feature in $\mathcal{F}_{t-1}$; la stima e' deterministica dato il modello calibrato e il vettore di feature.

### Capitolo 20 -- Filtri di emissione basati sul survival (~1.5 pp)

Definire i filtri di emissione che consumano l'output del survival:
- **Soglia minima di probabilita'**: il segnale viene emesso solo se $\hat{p}_{hit} \geq \tau_{surv}$, dove $\tau_{surv}$ e' parametro del cromosoma (provvisorio, congelamento Parte V).
- **Integrazione con le condizioni di Cap.8 (Parte II)**: la condizione survival-based si aggiunge (AND logico) alle condizioni di volatilita', distanza e volume. Il segnale deve soddisfare tutte le condizioni per essere emesso.
- **Condizionalita' al regime**: $\tau_{surv}$ puo' essere condizionale al regime ($\tau_{surv,calmo}$, $\tau_{surv,turbolento}$), come $\tau_{vol}$.
- **Interazione con la condizione di distanza sigma**: dichiarare se il survival gia' incorpora la distanza target-entry o se la condizione $\tau_{dist}^{\sigma}$ resta un filtro separato. (Presumibilmente filtri separati: il survival incorpora la distanza come feature, ma la condizione di Cap.8 resta un gate hard indipendente.)
- **Tempo residuo di sessione come filtro implicito**: il survival condiziona la stima a $T_{residuo}$; se $T_{residuo}$ e' troppo basso, $\hat{p}_{hit}$ cala naturalmente sotto $\tau_{surv}$, producendo un filtro di fine sessione senza soglia aggiuntiva. Dichiarare questo meccanismo esplicitamente.

### Capitolo 21 -- Caso trade_range (~1.5 pp)

Definire la geometria e i filtri per setup di tipo trade_range:
- **Definizione del range**: il trade_range e' un intervallo di prezzo $[p_{low}, p_{high}]$ derivato da due pivot strutturali (un pivot high e un pivot low confermati). L'ampiezza del range e' $A_{range} = p_{high} - p_{low}$, multiplo di 5.
- **Eccezione al filtro 80 punti**: per setup trade_range, il vincolo $|\text{target\_1} - p_{ref}| \geq 80$ e' sostituito dal vincolo $A_{range} \geq 80$ punti (Cap.5 Parte I). Se l'ampiezza del range e' $\geq 80$pt, il segnale e' ammesso anche se target_1 e' a meno di 80pt da $p_{ref}$.
- **Zone di entry nel range**: la zona di entry e' costruita ai bordi del range (bordo superiore per short, bordo inferiore per long).
- **Target e stop nel range**: target_1 e' il bordo opposto del range; stop e' fuori dal range nella direzione avversa.
- **Survival nel range**: il modello di survival opera allo stesso modo del caso directional, con la feature "ampiezza del range" come input aggiuntivo.
- **Classificazione setup_class**: dichiarare la regola algoritmica che classifica un setup come directional vs trade_range. La classificazione e' deterministica e dipende dalla geometria dei pivot della sessione.

## Acceptance criteria -- tutti devono essere soddisfatti per PASS in Review

### Struttura e completezza

- [ ] I 6 capitoli (Cap.16-21) sono presenti, completi, nell'ordine corretto
- [ ] Tutte le 19 eredita' (7 CAP-01 + 6 CAP-02 + 6 CAP-03) sono citate esplicitamente almeno una volta nei capitoli pertinenti
- [ ] Il paragrafo finale del documento elenca tutti i parametri provvisori introdotti in Parte IV con rinvio a Parte V per congelamento

### Cap.16 -- Zone di entry

- [ ] Prezzo di riferimento $p_{ref}$ derivato dai pivot strutturali con algoritmo esplicito
- [ ] Trattamento del warm-up (nessun pivot confermato nella sessione) dichiarato esplicitamente (M-1 v2 CAP-03)
- [ ] Banda $b \in \{5,...,40\}$ punti FIB come parametro del cromosoma, con cardinalita' $(2b/5)+1$
- [ ] Condizione di raw touch formalizzata in termini di OHLC della barra 1-min
- [ ] Condizioni di invalidazione strutturale pre-touch definite, con parametri dichiarati provvisori
- [ ] Condizione di tempo residuo minimo $T_{min,session}$ dichiarata con parametro provvisorio
- [ ] Coerenza esplicita con fill virtuale worst-case di Cap.12.4 CAP-03

### Cap.17 -- Target strutturali

- [ ] Algoritmo di selezione di target_1 dal catalogo dei pivot strutturali
- [ ] Vincolo $|\text{target\_1} - p_{ref}| \geq 80$pt per setup directional
- [ ] Algoritmo di selezione di target_2 con $|\text{target\_2}| > |\text{target\_1}|$
- [ ] Condizione sigma-units $\tau_{dist}^{\sigma}$ richiamata esplicitamente con cross-reference a Cap.8 Parte II
- [ ] target_1 e target_2 multipli di 5

### Cap.18 -- Stop strutturali

- [ ] Algoritmo di derivazione di stop_loss dalla struttura del prezzo
- [ ] Vincolo geometrico $d_{stop} > b$ obbligatorio con cross-reference a Cap.6 Parte II
- [ ] Separazione esplicita stop strutturale vs stop personale dell'operatore (Cap.11 Parte II)
- [ ] Risk-reward ratio $d_{stop}/d_{target}$ dichiarato come grandezza osservabile, eventuale vincolo rinviato a Parte V
- [ ] Condizionalita' al regime dichiarata (parametri di stop regime-dipendenti opzionali)

### Cap.19 -- Modello di survival

- [ ] Variabile obiettivo (tempo al primo evento terminale) formalizzata
- [ ] Competing risks (target_1_hit vs stopped) trattati esplicitamente
- [ ] Formulazione matematica del modello candidato primario (Cox, Weibull, o survival forest)
- [ ] Feature input: sottoinsieme delle 37 feature causali normalizzate, selezione rinviata a Parte V/VII
- [ ] Calibrazione fold-per-fold, coerente con Cap.13.3 CAP-03
- [ ] Censoring a destra per segnali expired senza hit ne' stop
- [ ] Output $\hat{p}_{hit}$ formalizzato come probabilita' condizionata
- [ ] Determinismo e causalita' ($\mathcal{F}_{t-1}$) dichiarati

### Cap.20 -- Filtri survival

- [ ] Soglia $\tau_{surv}$ come parametro del cromosoma, provvisorio
- [ ] Integrazione AND logico con condizioni Cap.8 Parte II
- [ ] Condizionalita' $\tau_{surv}$ al regime dichiarata
- [ ] Meccanismo di filtro implicito di fine sessione via $T_{residuo}$ descritto

### Cap.21 -- Caso trade_range

- [ ] Definizione del range $[p_{low}, p_{high}]$ da pivot strutturali
- [ ] Eccezione al filtro 80pt formalizzata: $A_{range} \geq 80$pt
- [ ] Zone di entry ai bordi del range, target al bordo opposto, stop fuori range
- [ ] Survival nel range: stessa architettura, feature aggiuntiva ampiezza range
- [ ] Regola algoritmica di classificazione directional vs trade_range

### Vincoli trasversali

- [ ] Tick FIB = 5pt rispettato in ogni formula, esempio numerico, livello strutturale
- [ ] Determinismo bit-exact: ogni algoritmo e regola e' deterministico (Cap.10 Parte II)
- [ ] Causalita': nessuna grandezza usata al tempo $t$ richiede dati dopo $t-1$ ($\mathcal{F}_{t-1}$)
- [ ] Nessun parametro fissato definitivamente: tutti i valori numerici sono provvisori con rinvio a Parte V
- [ ] Registro tecnico italiano formale, formule LaTeX inline e display
- [ ] Citazioni scientifiche pertinenti inline nei capitoli (non in bibliografia finale)
- [ ] Il REPORT_CAP_04.md include sezione "Misura prima/dopo" con impatto sul comportamento del GA

## Out-of-scope -- Development NON include queste cose in CAP-04

- **Cromosoma, operatori GA, fitness multi-obiettivo** -> Parte V (Cap.22-26). La Parte IV definisce i gradi di liberta' geometrici che il cromosoma parametrizza, non il cromosoma stesso.
- **Walk-forward, DSR, PBO** -> Parti V e VII. La Parte IV dichiara che il survival e' calibrato fold-per-fold, ma non definisce la procedura di walk-forward.
- **Selezione delle feature per il survival** (quale sottoinsieme delle 37) -> Parte V (cromosoma) o Parte VII (wrapper).
- **Congelamento definitivo dei parametri** ($\tau_{surv}$, $d_{inv}$, $T_{min,session}$, parametri survival) -> Parte V.
- **Pipeline di inference real-time** (Cap.27) -> Parte VI.
- **Tasso di rimpiazzo NSGA-II** (M-4) -> Parte V.
- **Benchmark window EGARCH** (M-5) -> Parte V.
- **Classificazione regime media vs mediana** (M-6) -> Parte V.
- **Verifica empirica latenza Telegram** (M-2) -> Appendice E.
- **Cadenza ricalibrazione EGARCH in production** (M-2 v2 CAP-03) -> Parte V/VI.
- **Pivot inconfermabili a inizio/fine sessione** (M-1 v2 CAP-03): il trattamento e' IN-SCOPE per Cap.16 (ancoraggio zona quando nessun pivot e' confermato nella sessione corrente); resta OUT-OF-SCOPE per Cap.15.3 che ha gia' chiuso la questione come design corretto.

## Done when

Il documento risponde senza ambiguita' a queste domande:

1. Come si determina il prezzo di riferimento $p_{ref}$ per la zona di entry a partire dai pivot confermati? (Cap.16)
2. Cosa succede nelle prime barre di sessione quando nessun pivot e' ancora confermato? (Cap.16)
3. Quali condizioni geometriche producono l'invalidazione del segnale prima del raw touch? (Cap.16)
4. Come si selezionano target_1 e target_2 fra i livelli strutturali candidati, e come interagiscono il filtro 80pt e la condizione sigma? (Cap.17)
5. Come si determina lo stop strutturale, e come si garantisce il vincolo $d_{stop} > b$? (Cap.18)
6. Qual e' la formulazione del modello di survival, e come stima la probabilita' di raggiungere target_1 prima dello stop? (Cap.19)
7. Come il filtro survival-based si integra con le condizioni di emissione di Cap.8 Parte II? (Cap.20)
8. In cosa il caso trade_range differisce geometricamente dal caso directional, e come si classifica un setup nell'una o nell'altra categoria? (Cap.21)

## Pipeline attesa

Development v1 -> Review v1 audit ostile con classificazione GA -> punto di controllo supervisore se CONDITIONAL/FAIL -> fix -> ... -> PASS

---

## Finding di Review v1 da risolvere (rework v2)

Review v1 di CAP-04 (commit `64a31aa` + `a1de0a8`) ha emesso verdetto **CONDITIONAL** con 2 BUG REALI + 2 NEUTRO + 4 PROMEMORIA. **Decisione supervisore 2026-05-24**: BUG REALI obbligatori (NB-1 + NB-2) + **tutti i PROMEMORIA approvati** (O-3, O-4, O-5, O-6). I 2 NEUTRO (O-1 cross-ref Cap.15.2.1; O-2 tie-break arrotondamento target_2 sintetico) restano carryover documentazione interna, NON vanno a Developer.

Le decisioni di design per chiudere i PROMEMORIA sono state prese dall'Orchestratore (in assenza di Planner attivo in questa sessione, scope CAP-04 esteso a chiusura PROMEMORIA invece di rinvio a Parte V). Il Reviewer le auditera' come decisioni di design dichiarate; il supervisore puo' obiettare nel checkpoint.

### BUG REALI obbligatori

#### **NB-1** -- Contraddizione formula vs testo in selezione p_ref (Cap.16.1 righe 21-26)

**Problema**: la formula a riga 21 dice $p_{ref} = \max_{p \in P_{low}(t)} p$ (criterio prezzo), il testo a riga 26 dice "si seleziona il piu' recente per timestamp di conferma" (criterio temporale). Due implementazioni divergenti producono $p_{ref}$ diversi.

**Fix v2 -- decisione di design**: scegliere il **criterio temporale (pivot piu' recente per timestamp di conferma)** come unico criterio. Motivazione: il pivot piu' recente e' il piu' "vicino" al momento decisionale e quindi piu' reattivo al regime corrente; il pivot estremo in prezzo puo' essere distante temporalmente e non riflettere la struttura attuale.

Modifiche concrete:
- Riga 21 Cap.16.1: sostituire formula con $p_{ref}(t) = \text{level}(\text{argmax}_{p \in P_{low}(t)} \tau_{conf}(p))$ dove $\tau_{conf}(p)$ e' il timestamp di conferma del pivot $p$ (coerente con disponibilita' a $t + n_c + 1$, Cap.15.3 di CAP-03).
- Riga 26: gia' corretta, lasciare invariata.
- Esempio numerico (se presente in Cap.16.3): aggiornare con due pivot a 27.300 (conferma 10:15) e 27.250 (conferma 11:30) -> $p_{ref} = 27.250$ (criterio temporale).
- Simmetrico per short.

#### **NB-2** -- Termine "oscillazione" non definito formalmente (Cap.21.2 riga 443)

**Problema**: la condizione 3 della classificazione trade_range richiede "oscillazioni $\geq n_{osc,min}$", ma "oscillazione" non ha definizione algoritmica. Viola il determinismo bit-exact.

**Fix v2 -- decisione di design**: definire "oscillazione" come **crossing completo del range** sulla sequenza delle barre OHLC.

Formulazione operativa da aggiungere a Cap.21.2 (dopo riga 443):

> Una *oscillazione* del prezzo nel range $[p_{low,range}, p_{high,range}]$ e' una sequenza di due tocchi consecutivi di bordi opposti: la barra $t_a$ tocca un bordo (cioe' $\text{close}(t_a) \in [p_{bordo} - \epsilon, p_{bordo} + \epsilon]$ con $\epsilon$ = tolleranza di prossimita') e una barra successiva $t_b > t_a$ tocca l'altro bordo. Le due barre $t_a$ e $t_b$ definiscono UNA oscillazione. Una sequenza di tocchi del medesimo bordo non incrementa il conteggio. $\epsilon$ e' parametro provvisorio del modello (valore di lavoro: $\epsilon = 5$ pt = 1 tick FIB), congelato in Parte V.
> Il conteggio $n_{osc}(t)$ a tempo $t$ considera tutte le oscillazioni completate nelle ultime $N_{osc}$ barre della sessione corrente. $N_{osc}$ e' parametro provvisorio (valore di lavoro provvisorio nell'ACTIVE_TASK), congelato in Parte V.

L'algoritmo e' deterministico, causale (usa solo close fino a $t-1$), e produce conteggio bit-exact identico fra implementazioni.

### PROMEMORIA approvati dal supervisore (chiusura in rework v2)

#### **O-3 / M-12** -- Flag target_2_type e stop_type nel payload formale

**Problema**: il Developer CAP-04 ha introdotto i flag `target_2_type` (synthetic/structural) e `stop_type` (structural/personal) ma non sono nel payload formale di Cap.6.1 di CAP-02. Domanda aperta: dove vanno?

**Fix v2 -- decisione di design**: i flag entrano nel **payload formale** di Cap.6.1 Parte II come campi obbligatori del messaggio segnale. Il consumer Telegram deve conoscerli per gestire correttamente il behavior (es. target_2 sintetico = chiusura forzata vs strutturale = trail; stop strutturale vs personale = priorita' diversa nella gestione).

Modifiche concrete:
1. **Mini-patch CAP-02 Cap.6.1**: aggiungere al payload $S$ due nuovi campi:
   - `target_2_type \in \{structural, synthetic\}`
   - `stop_type \in \{structural, personal\}`
   Aggiornare la definizione testuale di $S$ in Cap.6.1 e l'esempio di payload se presente.
2. **Aggiornare Cap.17.4 di CAP-04** (target_2): esplicitare che il campo `target_2_type` del payload viene popolato in base alla selezione fra strutturale e sintetico.
3. **Aggiornare Cap.18.1/18.3 di CAP-04** (stop): esplicitare che il campo `stop_type` del payload viene popolato in base alla derivazione strutturale o personale.
4. **CARRYOVER.md**: stato M-12 -> `CLOSED-CAP-04`.

#### **O-4 / M-13** -- Catalogo feature 37 vs 38 per trade_range

**Problema**: $x^{(A_{range})}$ aggiunta in Cap.21.5 di CAP-04 portava il catalogo a 38, in incoerenza con CAP-03 (catalogo 37).

**Fix v2 -- decisione di design**: il **catalogo globale resta 37 feature** (CAP-03 invariato). La feature $x^{(A_{range})}$ e' classificata come **feature condizionale** attiva solo nel regime trade_range, non aggiunta al catalogo principale.

Modifiche concrete:
1. **Cap.21.5 di CAP-04**: aggiungere all'inizio del paragrafo una dichiarazione esplicita: "Il modello survival per il regime trade_range usa un'estensione locale del catalogo causale con la feature condizionale $x^{(A_{range})} = A_{range} = p_{high,range} - p_{low,range}$, attiva solo quando lo stato di mercato e' classificato trade_range (Cap.14 di Parte III). Il catalogo globale del cromosoma per il regime directional resta a 37 feature (Cap.15 di CAP-03 invariato)."
2. **CARRYOVER.md**: stato M-13 -> `CLOSED-CAP-04`.
3. **Nessuna modifica a CAP-03** (catalogo invariato).

#### **O-5 / M-7** -- Censoring informativo nel Cox cause-specific (Cap.19.4)

**Problema**: il modello Cox cause-specific dichiara di assumere censoring non-informativo (i tempi di censoring sono indipendenti dai tempi di evento, condizionatamente alle covariate), ma l'assunzione non e' verificata in CAP-04.

**Fix v2 -- formalizzazione**: aggiungere a Cap.19.4 una **dichiarazione esplicita** dell'assunzione + **acceptance criterion** che rinvia formalmente la verifica empirica a Parte V.

Modifiche concrete:
1. **Cap.19.4 di CAP-04**: aggiungere dopo la riga 355 una frase: "Il modello assume che il censoring (eventi `expired` per timeout di sessione, vedi Cap.20.4) sia non-informativo rispetto ai tempi di evento, condizionatamente alle covariate $\tilde{\mathbf{x}}_t$. L'assunzione e' plausibile a priori perche' il timeout di sessione e' fissato dall'orario di chiusura (22:00 CET) e non dalla dinamica del prezzo. La verifica empirica formale (test di Cox-Snell sui residui di censoring, plot di Schoenfeld stratificato per evento vs censoring) e' rinviata a Parte V, Cap.X di calibrazione/diagnostica survival."
2. **CARRYOVER.md**: M-7 resta `OPEN` con destinazione Parte V (la verifica empirica resta Parte V; in CAP-04 solo dichiarazione formale).
3. **REPORT_CAP_04**: AC della formalizzazione aggiunto.

#### **O-6** -- Discrepanza 80pt fra Cap.5 PI e Cap.6.1 PII

**Problema**: Cap.5 PI dice "$A_{range} \geq 80$ pt" (ampiezza del range); Cap.6.1 PII dice "$|target_1 - stop_{loss}| \geq 80$ pt" (distanza target-stop). Formulazioni diverse. CAP-04 ha adottato Cap.5 PI come riferimento.

**Fix v2 -- mini-patch CAP-02**: la formulazione di Cap.5 PI ($A_{range} \geq 80$ pt) e' il riferimento normativo. Sincronizzare Cap.6.1 PII.

Modifiche concrete:
1. **Mini-patch CAP-02 Cap.6.1**: sostituire "$|target_1 - stop_{loss}| \geq 80$ pt" con "$A_{range} \geq 80$ pt" (oppure aggiungere chiarimento: "il vincolo dei 80 pt si applica all'ampiezza del range $A_{range}$, vedi Cap.5 di Parte I e Cap.21 di Parte IV per la definizione operativa di $A_{range}$").
2. **REPORT_CAP_02.md**: aggiungere sezione "## Iterazione 4 -- sincronizzazione 80pt Cap.6.1 con Cap.5 PI".
3. **CARRYOVER.md**: O-6 -> CHIUSO.

### Acceptance criteria aggiuntivi per la v2

- [ ] **AC-v2-1**: NB-1 chiuso. Cap.16.1 riga 21 ha formula con criterio temporale (argmax su timestamp di conferma). Riga 26 invariata. Esempio numerico aggiornato (se presente).
- [ ] **AC-v2-2**: NB-2 chiuso. Cap.21.2 contiene definizione algoritmica esplicita di "oscillazione" (crossing completo del range) con tolleranza $\epsilon = 5$ pt provvisoria. Algoritmo deterministico + causale.
- [ ] **AC-v2-3**: O-3 / M-12 chiuso. Payload $S$ Cap.6.1 di CAP-02 contiene i campi `target_2_type` e `stop_type`. Cap.17.4 e Cap.18.1/18.3 di CAP-04 fanno riferimento esplicito ai due campi del payload.
- [ ] **AC-v2-4**: O-4 / M-13 chiuso. Cap.21.5 di CAP-04 dichiara $x^{(A_{range})}$ come feature condizionale al regime trade_range. Catalogo globale di Cap.15 CAP-03 invariato a 37 feature.
- [ ] **AC-v2-5**: O-5 / M-7 formalizzato. Cap.19.4 contiene dichiarazione esplicita dell'assunzione di censoring non-informativo + rinvio formale a Parte V con metodi di verifica nominati (Cox-Snell, Schoenfeld stratificato).
- [ ] **AC-v2-6**: O-6 chiuso. Mini-patch CAP-02 Cap.6.1: formulazione 80pt allineata a Cap.5 PI (`A_{range} \geq 80` pt). REPORT_CAP_02 ha sezione "Iterazione 4".
- [ ] **AC-v2-7**: nessuna regressione su AC v1 originali (35 voci). Verifica esplicita nel REPORT con tabella prima/dopo dove rilevante.
- [ ] **AC-v2-8**: `tasks/CARRYOVER.md` aggiornato: M-12, M-13, O-6 -> `CLOSED-CAP-04`; M-7 resta `OPEN` Parte V; gli M-8...M-15 dichiarati dal Developer in v1 restano `OPEN`.
- [ ] **AC-v2-9**: REPORT_CAP_04.md include sezione "## Iterazione 2 -- risposta ai finding di Review v1 + decisioni PROMEMORIA" con: per ogni finding/PROMEMORIA, modifica applicata + misura prima/dopo + AC chiuso.
- [ ] **AC-v2-10**: REPORT_CAP_02.md include sezione "## Iterazione 4 -- mini-patch Cap.6.1 (flag payload + sincronizzazione 80pt)".
- [ ] **AC-v2-11**: 00_indice.md aggiornato per riflettere lo stato corrente di CAP-04 e CAP-02 (entrambi in revisione).
- [ ] **AC-v2-12**: tutti i file modificati sono committati e pushati. Working tree pulito sui file di task (escluso `.claude/*` locali e file di scheduling).

### Pipeline rework v2

Development v2 (2 fix BUG REALI + 4 chiusure PROMEMORIA + mini-patch CAP-02) -> Review v2 di CAP-04 -> atteso PASS (con possibili nuove osservazioni minori sui mini-patch CAP-02).

---

## Finding di Review v2 da risolvere (rework v3)

Review v2 di CAP-04 (commit `7b9faa5` + `6fdb05e` + `a92b515`) ha emesso verdetto **CONDITIONAL** con 3 BUG REALI + 1 MIGLIORA PERFORMANCE + 5 NEUTRO. **Decisione supervisore 2026-05-25**:
- 3 BUG REALI obbligatori (NB-v2-1 via (a) aggiunta a Cap.9.2; NB-v2-3 razionale (a); NB-v2-4 esempio numerico tick FIB)
- 1 MIGLIORA PERFORMANCE approvato (NB-v2-2 cambio dominio `stop_type`)
- 5 NEUTRO **inclusi** come fix opportunistici (O-v2-1...5) -- decisione supervisore: "includi anche NEUTRO"

I 2 BUG REALI di Review v1 (NB-1, NB-2) restano CHIUSI; nessuna regressione su AC v1 (43 OK + 1 PARZIALE NEUTRO su 44, 3 AC v1 ora promossi a OK).

Pipeline attesa rework v3: 9 fix chirurgici (<= 5 righe ciascuno) -> Review v3 -> PASS (alta confidenza).

### BUG REALI obbligatori

#### **NB-v2-1** -- Cap.6.1 / Cap.9.2 incoerenza payload-pubblicazione

**Problema**: Cap.6.1 (CAP-02 patch4) riga 39 e Cap.17.4 (CAP-04) riga 197 dichiarano "Il consumer Telegram dell'operatore (Cap.9.2) usa il valore" per `target_2_type`; Cap.6.1 riga 51 idem per `stop_type`. Tuttavia Cap.9.2 di CAP-02 enumera "in ordine obbligatorio" 7 voci: signal_id, direction, setup_class, entry_zone, target_1 e target_2, stop_loss, timestamp_emission. **I due nuovi campi non compaiono nella lista pubblicata.**

**Fix v3 -- decisione supervisore (a)**: aggiungere i due campi alla lista ordinata di Cap.9.2.

Modifiche concrete:
1. **Cap.9.2 di CAP-02**: estendere la lista ordinata a 9 voci:
   - 8. `target_2_type` (qualifica la natura del livello target_2 pubblicato)
   - 9. `stop_type` (qualifica la natura dello stop pubblicato)
   Aggiornare anche la specifica del formato del messaggio Telegram coerentemente.
2. **Cap.10.2 di CAP-02** (log emissione): verificare che la formulazione generica "tutti i campi di Cap.6.1" copra automaticamente i nuovi due campi; se elenco esplicito, aggiornare.
3. **REPORT_CAP_02.md**: aggiungere sezione "Iterazione 5 -- Cap.9.2 aggiornamento campi pubblicati (chiusura NB-v2-1)".

#### **NB-v2-3** -- Razionale (a) censoring non-informativo strutturalmente sbagliato

**Problema**: Cap.19.4 (CAP-04) riga 369, razionale (a) della dichiarazione di censoring non-informativo, dice "il timeout di sessione e' fissato dall'orario di chiusura (22:00 CET) e non dalla dinamica del prezzo". Ma il timer di censoring del modello survival NON e' 22:00 CET (orario assoluto), e' $\Delta t_{cromosoma}$ (cap di 2 giorni di trading dal raw touch, vedi Cap.20.4 e Parte II Cap.11). I due tempi sono distinti: 22:00 CET chiude la sessione operativa, $\Delta t_{cromosoma}$ chiude il segnale come `expired`. Razionale (a) confonde i due e va rimosso.

Inoltre, il flip-flop di design D-6 (v1) -> D-v2-5 (v2) non e' discusso nel REPORT_CAP_04. In v1 il Developer dichiarava "censoring potenzialmente informativo, rinviato Parte V" (D-6); in v2 ha dichiarato "non-informativo, formalizzato qui" (D-v2-5). Il razionale del cambiamento manca.

**Fix v3**: 
1. **Cap.19.4 di CAP-04 riga 369**: rimuovere la frase del razionale (a). Razionale (b) (sul fold OOS frozen) tiene da solo come motivazione strutturale.
2. **REPORT_CAP_04**: aggiungere alla sezione "Iterazione 3" una nota esplicita sul flip-flop D-6 -> D-v2-5 -> D-v3-1, con motivazione del cambiamento di assunzione (es. "dopo riflessione in iterazione 2, l'assunzione di non-informativita' condizionata alle covariate e' plausibile a priori; la verifica empirica formale resta Parte V").

#### **NB-v2-4** -- Esempio numerico Cap.21.2 viola tick FIB

**Problema**: Cap.21.2 riga 487 esempio dell'algoritmo di oscillazione usa prezzi 27.402, 27.498, 27.403. Tick FIB = 5pt -> tutti i prezzi devono essere multipli di 5. 27.402 non lo e' (27.400 o 27.405). Viola il vincolo non-negoziabile dichiarato in Cap.10 Parte II.

**Fix v3**: correggere l'esempio numerico Cap.21.2 riga 487 usando prezzi multipli di 5. Proposta operativa (allineata al suggerimento Reviewer):
- Range trade_range: $p_{low,range} = 27.400$, $p_{high,range} = 27.500$; $A_{range} = 100$ pt; $\epsilon = 5$ pt
- Barra t1: close = 27.495 ($\in [27.495, 27.505]$) -> tocco bordo alto
- Barra t2 (t2 > t1): close = 27.405 ($\in [27.395, 27.405]$) -> tocco bordo basso
- Oscillazione completata = 1 conteggio

Verificare che il pseudocodice di Cap.21.2 produca conteggio 1 sull'esempio corretto.

### MIGLIORA PERFORMANCE approvato dall'Orchestratore (decisione D-v2-7)

#### **NB-v2-2** -- Dominio `stop_type` asimmetrico

**Problema**: dominio `{structural, personal}` con valore costante `structural` dal motore (Cap.18.1 riga 231); `personal` "segnaposto formale del dominio mai prodotto dal motore" (Cap.18.3 riga 260). Campo non informativo verso operatore. Asimmetria con `target_2_type` dominio `{structural, synthetic}` che e' invece discriminante.

**Decisione di design D-v2-7** (Orchestratore): cambiare dominio di `stop_type` a `{structural, synthetic}` per simmetria con `target_2_type` e aumentare l'informativita' del payload pubblicato (Cap.9.2 aggiornato in NB-v2-1).

**Fix v3**:
1. **Cap.6.1 di CAP-02 riga 51**: cambiare "stop_type $\in \{structural, personal\}$" in "stop_type $\in \{structural, synthetic\}$".
2. **Cap.18.1 di CAP-04 riga 231**: cambiare "popolato come `structural` in tutti i casi (sia quando stop_loss deriva dal candidato pivot, sia quando deriva dal candidato sigma di fallback)" in "popolato come `structural` quando stop_loss deriva dal candidato pivot, come `synthetic` quando deriva dal candidato sigma di fallback con `d_stop_sigma`".
3. **Cap.18.3 di CAP-04 riga 260**: rimuovere o riformulare la frase su `personal` segnaposto. Sostituire con: "il valore `synthetic` e' prodotto quando lo stop strutturale richiede fallback sigma; il dominio non include valori prodotti dall'operatore (out-of-scope: il motore non gestisce stop manuali)".
4. **REPORT_CAP_04**: nella sezione "Iterazione 3" dichiarare D-v2-7 (decisione di design dell'Orchestratore, contestabile dal supervisore al checkpoint).

### Osservazioni minori NEUTRO incluse come fix opportunistici

#### **O-v2-1** -- Esempio Cap.16.1 usa orari invece di indici di barra

**Fix v3**: nell'esempio di Cap.16.1 sostituire "10:15" e "11:30" con indici di barra coerenti con la notazione algoritmica. Proposta: $b_{135}$ (10:15 = 135 minuti dall'apertura delle 8:00) e $b_{210}$ (11:30 = 210 minuti). Aggiungere mezza riga di nota: "indice di barra = minuti dall'apertura della sessione 8:00 CET; per esempio $b_{135}$ corrisponde alle 10:15".

#### **O-v2-2** -- `target_2_type` non richiamato esplicitamente in Cap.21.4 (trade_range)

**Fix v3**: in Cap.21.4 di CAP-04 (geometria trade_range) aggiungere richiamo esplicito a `target_2_type`. Proposta: nella sezione che descrive il target_2 del setup trade_range, aggiungere mezza riga "Il campo `target_2_type` del payload (Cap.6.1 PII) viene popolato come `structural` (target_2 = bordo opposto del range, sempre strutturale per definizione di trade_range)".

#### **O-v2-3** -- Cap.20.4 derivazione $\lim p_{hat,hit} = 0$ non rigorosa

**Fix v3**: in Cap.20.4 formalizzare la derivazione del limite. Proposta: aggiungere 2-3 righe con argomento basato su monotonicita' del survival $S(t)$ e finitezza del cap $\Delta t_{cromosoma}$. Citazione opzionale: "vedi Klein-Moeschberger (2003) cap. 2 per la convergenza monotona del survival function a 0 per $t \to \infty$ sotto rischio competitivo positivo".

#### **O-v2-4** -- Doppia notazione $\epsilon$ in Cap.21.2

**Fix v3**: rinominare uno dei due $\epsilon$ in Cap.21.2. Proposta:
- $\epsilon$ (condizione 2 della classificazione trade_range, distanza dai bordi) resta invariato
- $\epsilon$ dell'algoritmo oscillazione (definizione formale, riga ~470) rinominato in $\epsilon_{osc}$ con valore provvisorio 5 pt invariato

Aggiornare tutte le occorrenze nel testo, nel pseudocodice e nella tabella riepilogo parametri (se presente).

#### **O-v2-5** -- Pseudocodice oscillazione non gestisce esplicitamente cross-session

**Fix v3**: nel pseudocodice di Cap.21.2 (definizione algoritmo oscillazione) aggiungere all'inizio un commento esplicito sul cross-session:
```
# Il ciclo si limita alla sessione corrente; le barre della sessione precedente
# sono escluse dal conteggio. L'edge case cross-session e' neutralizzato dal
# warm-up T_warmup_norm = 100 barre (Cap.15.4 di Parte III) >= N_osc = 60 barre.
```

### Acceptance criteria aggiuntivi per la v3

- [ ] **AC-v3-1**: NB-v2-1 chiuso. Cap.9.2 di CAP-02 enumera 9 voci con `target_2_type` (8) e `stop_type` (9) come campi pubblicati del messaggio Telegram. Coerenza con Cap.6.1 e cross-ref di CAP-04 verificata.
- [ ] **AC-v3-2**: NB-v2-3 chiuso. Cap.19.4 riga 369 non contiene piu' il razionale (a) sbagliato. Razionale (b) e' presente e tiene da solo. REPORT_CAP_04 sezione "Iterazione 3" discute il flip-flop D-6 -> D-v2-5 -> D-v3-1.
- [ ] **AC-v3-3**: NB-v2-4 chiuso. Cap.21.2 riga 487 esempio numerico usa prezzi tutti multipli di 5 (proposta: 27.400, 27.500, 27.495, 27.405). Pseudocodice verificato sull'esempio corretto.
- [ ] **AC-v3-4**: NB-v2-2 chiuso (decisione D-v2-7). Dominio `stop_type` = `{structural, synthetic}` in Cap.6.1 di CAP-02. Cap.18.1 produce entrambi i valori (pivot/sigma). Cap.18.3 riformulato. Nessun residuo "personal" come dominio nel documento.
- [ ] **AC-v3-5**: O-v2-1 chiuso. Cap.16.1 esempio usa indici di barra ($b_{135}$, $b_{210}$ o equivalenti) con riga di nota sulla notazione.
- [ ] **AC-v3-6**: O-v2-2 chiuso. Cap.21.4 contiene richiamo esplicito a `target_2_type = structural` per trade_range.
- [ ] **AC-v3-7**: O-v2-3 chiuso. Cap.20.4 formalizza il limite $p_{hat,hit} \to 0$ con argomento di monotonicita' e finitezza del cap.
- [ ] **AC-v3-8**: O-v2-4 chiuso. Doppia notazione $\epsilon$ in Cap.21.2 risolta (uno dei due rinominato $\epsilon_{osc}$). Tutte le occorrenze aggiornate.
- [ ] **AC-v3-9**: O-v2-5 chiuso. Pseudocodice Cap.21.2 contiene commento esplicito sul cross-session.
- [ ] **AC-v3-10**: nessuna regressione sugli AC v2 (12 voci AC-v2-1...12) ne' sugli AC v1 (35 voci) ne' sugli AC I4 CAP-02 (8 voci). Verifica esplicita nel REPORT.
- [ ] **AC-v3-11**: CARRYOVER.md aggiornato se nuovi M-promemoria emergono (atteso: nessuno).
- [ ] **AC-v3-12**: REPORT_CAP_04.md include sezione "## Iterazione 3 -- risposta ai finding di Review v2 + decisione D-v2-7" con tabella sintesi finding + tabella AC v3 + nota flip-flop D-6/D-v2-5/D-v3-1.
- [ ] **AC-v3-13**: REPORT_CAP_02.md include sezione "## Iterazione 5 -- Cap.9.2 aggiornamento campi pubblicati (NB-v2-1)".
- [ ] **AC-v3-14**: 00_indice.md riflette CAP-04 IN REVIEW v3, CAP-02 IN REVIEW Iterazione 5.
- [ ] **AC-v3-15**: tutti i file modificati committati e pushati. Working tree pulito sui file di task.

### Pipeline rework v3

Development v3 (3 fix BUG REALI + 1 MIGLIORA PERFORMANCE D-v2-7 + 5 fix NEUTRO opportunistici + correzione REPORT) -> Review v3 di CAP-04 -> atteso PASS in 1 iterazione (correzioni chirurgiche tutte <= 5 righe, nessuna decisione di design aperta dopo D-v2-7).
