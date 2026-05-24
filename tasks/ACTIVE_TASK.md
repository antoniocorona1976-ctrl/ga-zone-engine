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
