# Review CAP-05 v3 -- Parte V: Motore genetico, fitness operativa, walk-forward nested, calibrazione

**Verdetto**: CONDITIONAL

**Commit oggetto**: `16590ae` [DEV] CAP-05 v2 rework
**Data audit**: 2026-05-26
**Natura**: Audit ostile v3 indipendente (riapertura ciclo dal supervisore via `DEV_STATUS=READY_FOR_REVIEW`; ipotesi Review v2 PASS da verificare)
**Reviewer**: Review Agent (audit indipendente non vincolato dalla Review v2)

---

## Sintesi del verdetto

CONDITIONAL. Tre dei cinque fix v2 ratificati dal supervisore sono chiusi correttamente (NB-1, NB-3, RP-3). Due fix sono chiusi solo apparentemente:

- **NB-2 (K_max=6 per strato)** e' chiuso testualmente ma poggia su un calcolo aritmetico errato in Cap.26.7 (riga 652) e un'incoerenza di stima censoring fra Cap.25.5 e Cap.26.7 che il Reviewer v2 ha mancato. Sotto la stima corretta con censoring 0,7 di Cap.26.7, il caso pessimo strato e' $N_{eventi,strato} \approx 44$ (non 60), e con $K_{max}=6$ il rapporto $N/K = 7,3 < 10$ viola Harrell. Il fix v2 non chiude il vincolo di stabilita' MLE che NB-2 originale doveva garantire.

- **RP-1 (T_budget=80h)** e' chiuso testualmente ma poggia su una motivazione formalmente contraddittoria: Cap.26.2 riga 523 e Cap.26.5 riga 603 motivano $T_{budget}=80$h come "coerente con il caso ottimo del calcolo di Cap.23.6 (72 ore caso ottimo per 8 fold sequenziali)", mentre lo stesso Cap.23.6 riga 223 dichiara esplicitamente che i 72h sono "la stima Cap.23.6 ORIGINALE, ottenuta con la derivazione $r_{cache}$/min-per-fold dell'iterazione v1 PRIMA del riallineamento M-4". Il calcolo coerente con la versione attuale (post-fix v2) di Cap.23.6 e' 107h caso ottimo / 213h caso pessimo. Cap.23.6 lo riconosce ma Cap.26.2/26.5 motivano $T_{budget}$ sul calcolo v1 ormai obsoleto.

Inoltre l'O-v2-1 che il Reviewer v2 ha classificato NEUTRO e' la stessa categoria di errore di NB-1 originale: in v2 il fix NB-1 ha riparato Cap.23.6 ma ha lasciato la stessa confusione di unita' (valutazioni vs minuti) in Cap.26.1 riga 513.

I problemi sopra hanno impatto sul ranking del fronte di Pareto (BUG-1: stima Cox sovra-parametrizzata nel caso pessimo $\to$ $\hat{p}_{hit}$ biased $\to$ filtro $E_{surv}$ distorto $\to$ ranking alterato) e sulla robustezza dell'aggregazione cross-fold (BUG-2: budget compute incoerente $\to$ run interrotto a $\sim 56\%$ dei fold nel caso ottimo $\to$ mediana cross-fold con varianza inflated). Non sono problemi cosmetici.

---

## Tabella verifica chiusura finding v1 + v2 (6 voci)

| Finding v1/v2 | Stato v2 atteso | Stato verifica v3 | Evidenza |
|--------------|-----------------|------------------|----------|
| **NB-1** -- Derivazione 12.800-25.600 min unita' incoerenti | CHIUSO | **CHIUSO** | Cap.23.6 righe 209-221: derivazione $t_{eval} \in [0,74; 1,47]$ min/cromosoma esplicita, verifica numerica val * min/val = min coerente. Formula errata "16.448 * 0,8" rimossa. Confermo chiusura. |
| **NB-2** -- K_max=12 vs stratificazione Cap.25.5 | CHIUSO (opzione a, K_max=6) | **PARZIALE / REGRESSIONE LATENTE** | Cap.26.7 riga 651 dichiara $N_{eventi} \in [88; 264]$ applicando censoring 0,7; riga 652 dichiara strato $\in [60; 190]$ caso pessimo 60 -- INCOERENTE con la stima censurata della riga sopra (88/2 = 44, non 60). Il caso pessimo strato corretto e' 44, sotto cui $K_{max}=6$ produce $N/K = 7,3 < 10$ -- VIOLA HARRELL. Inoltre Cap.25.5 riga 427 mantiene il calcolo SENZA censoring (120/380 -> 60/190); incoerenza Cap.25.5 ↔ Cap.26.7 persiste post-fix v2. Formula aritmetica Cap.26.7 riga 652 "$[60/2; 264/2] \cdot 2 = [60; 190]$" e' anche aritmeticamente errata: $[30; 132] \cdot 2 = [60; 264]$, non $[60; 190]$. |
| **NB-3** -- Nomenclatura "MAE alla scadenza" | CHIUSO | **CHIUSO** | Cap.24.1 riga 245 contiene "rendimento di chiusura virtuale forzata"; nota esplicita che MAE/MFE restano accezione standard. Grep su "MAE" mostra solo 2 match (riga 245 nota esplicativa + riga 288 metriche lifecycle). Confermo chiusura. |
| **RP-1** -- T_budget vs caso ottimo F=8 | CHIUSO (T_budget=80h ratificato) | **APERTO / REGRESSIONE** | $T_{budget}=80$h e' applicato in Cap.26.2 e Cap.26.5 -- ma motivato come "coerente con caso ottimo Cap.23.6 (72h)". Cap.23.6 riga 223 dichiara esplicitamente che 72h e' il calcolo v1 PRE-fix; il calcolo POST-fix (con il riallineamento M-4 applicato in NB-1) e' 107h caso ottimo per F=8. Cap.26.2 motiva $T_{budget}=80$h su un calcolo obsoleto. Cap.23.6 stesso riconosce che $T_{budget}=80$h **NON** copre il caso ottimo 107h del calcolo attuale e rinvia il problema a Parte VII Cap.34. Il fix v2 NON ha risolto la tensione che RP-1 doveva risolvere; ha solo nascosto la tensione dietro una motivazione che cita la stima v1 ormai obsoleta. |
| **RP-3** -- Soglia $\theta_{CV}=0,5$ senza fonte | CHIUSO (starting point Parte VII) | **CHIUSO** | Cap.25.5 riga 429 dichiara $\theta_{CV}=0,5$ come "starting point per il primo run di calibrazione, in assenza di rule of thumb consolidata"; Cap.26.5 riga 622 con flag "(starting point, riconsiderato Parte VII)". Nessuna citazione di facciata. Confermo chiusura onesta. |
| **O-v2-1** -- Cap.26.1 riga 513 ambiguita' valutazioni vs minuti | NEUTRO (non a Developer) | **APERTO ma NEUTRO** | Riga 513: "Compute budget P * G_max valutazioni $\approx$ 19.328 (Cap.23.6), **dentro il range 12.800-25.600 min single-thread di M-4**". La frase e' la stessa categoria di errore formale di NB-1 originale (19.328 e' in valutazioni, range e' in minuti). Reviewer v2 l'ha lasciata come NEUTRO. Confermo NEUTRO: non impatta il GA, ma e' formalmente brutto e segnala che il rework non e' stato esaustivo sui residui di NB-1. |

---

## Tabella AC v1 + AC v2 (62 voci) -- revisione indipendente

| Gruppo | Esito v3 Reviewer indipendente |
|--------|-------------------------------|
| **AC-1..AC-5** (5 voci struttura generale) | 4 OK + 1 PARZIALE (AC-2 carryover) -- invariato vs v2. |
| **AC-22-1..7** (7 voci cromosoma) | 7 OK -- invariato. Nota: Cap.22.6 vincolo "$\sum_j s_j \leq K_{max}$" dove $K_{max}=6$ e' ora il **cap totale del cromosoma** (37 bit con max 6 attivi), non "per strato"; la dicitura "(per strato sotto stratificazione Cap.25.5)" in Cap.26.5 riga 609 e' misleading ma operativamente coerente. |
| **AC-23-1..7** (7 voci operatori GA) | 6 OK + AC-23-5 OK (promosso da PARZIALE). Confermo promozione: derivazione M-4 ora dimensionalmente coerente. |
| **AC-24-1..10** (10 voci fitness) | 10 OK. AC-24-2 promosso da PARZIALE a OK. Confermo. |
| **AC-25-1..10** (10 voci walk-forward) | 9 OK + 1 PARZIALE -- **AC-25-6 RICLASSIFICATO PARZIALE**: Cap.25.5 riga 427 mantiene la motivazione 3 con stima $N_{eventi} \in [120; 380]$ SENZA censoring, mentre Cap.26.7 applica censoring 0,7. L'incoerenza di stima e' la stessa che Reviewer v1 aveva segnalato in NB-2 come "minore" ma che il fix v2 ha solo spostato (ora la contraddizione e' tra Cap.25.5 senza censoring e Cap.26.7 con censoring). Sotto la stima corretta con censoring, $K_{max}=6$ non garantisce Harrell nel caso pessimo. Riviste mancate dal Reviewer v2. |
| **AC-26-1..9** (9 voci calibrazione) | 7 OK + AC-26-8 RICLASSIFICATO PARZIALE (NB-2 incompletamente chiuso, vedi sopra). AC-26-2 **RICLASSIFICATO PARZIALE**: $T_{budget}=80$h applicato ma motivato su calcolo obsoleto (72h v1); il calcolo aggiornato (107h ottimo / 213h pessimo) e' in Cap.23.6 riga 223 e contraddice la motivazione di Cap.26.2 riga 523. |
| **AC-T-1..9** (9 voci trasversali) | 9 OK -- invariati. |
| **AC-v2-1..10** (10 voci v2) | 8 OK + 2 RICLASSIFICATI: AC-v2-2 **PARZIALE** (NB-2 chiusura incompleta, vedi sopra); AC-v2-4 **PARZIALE** (RP-1 chiusura formale ma motivazione contraddittoria). |

**Sintesi AC v3 indipendente**: 62 AC totali. **54 OK + 5 PARZIALI + 0 MANCA**. Reviewer v2 contava 60 OK + 1 PARZIALE (AC-2) + 1 NEUTRO non flaggato. **4 nuovi PARZIALI emergono dall'audit v3** (AC-25-6, AC-26-2, AC-26-8, AC-v2-2, AC-v2-4 -- di cui AC-26-8/AC-v2-2 contano insieme come una sola questione NB-2, e AC-26-2/AC-v2-4 contano insieme come una sola questione RP-1).

---

## Finding NUOVI emersi dall'audit v3 indipendente

### NB-v3-1 -- Chiusura incompleta di NB-2: calcolo censoring incoerente fra Cap.25.5 e Cap.26.7, Harrell violato nel caso pessimo strato (Cap.25.5 riga 427, Cap.26.7 righe 651-653)

**Impatto GA**: la motivazione del fix v2 NB-2 (scelta opzione (a), $K_{max}=6$ per strato) si basa su $N_{eventi,strato} \geq 60$ nel caso pessimo. Ma:

1. **Cap.26.7 riga 651** dichiara correttamente $N_{eventi} \in [88; 264]$ applicando il **rate non-censurato ≈ 0,7** (i censuranti sono i segnali `expired` con `posttrigger_timeout`, che NON producono eventi target_1_hit/stopped e devono essere esclusi dal conteggio Harrell).

2. **Cap.26.7 riga 652** dichiara "$N_{eventi,strato} \in [60/2; 264/2] \cdot 2 = [60; 190]$, caso pessimo 60". Doppio bug:
   - **Aritmetico**: $[60/2; 264/2] = [30; 132]$, $\cdot 2 = [60; 264]$, non $[60; 190]$.
   - **Semantico**: il range strato corretto dal range fold $[88; 264]$ con split 50/50 e' $[44; 132]$, non $[60; 190]$. Il caso pessimo strato CON censoring e' $88/2 = 44$, non 60.

3. **Cap.25.5 riga 427** dichiara $N_{eventi} \in [120; 380]$, strato $[60; 190]$, caso pessimo 60 -- usando una stima **senza** censoring (1-3 segnali eseguiti/sessione × 126 sessioni = 126-378 segnali eseguiti). Questa stima conta gli ESEGUITI, non gli EVENTI Harrell.

4. **Conseguenza Harrell**: con $K_{max}=6$ feature per strato e $N_{eventi,strato}^{pessimo} = 44$ (stima corretta con censoring), rapporto $44/6 = 7,3 < 10$ -- **Harrell violato nel caso pessimo**. La stima MLE Cox stratificata risulta sovra-parametrizzata nel caso pessimo (fold turbolenti con poche emissioni); $\hat{p}_{hit}$ biased; filtro $E_{surv}$ Cap.20.1 PIV distorto; ranking del fronte di Pareto alterato -- esattamente la cascata di effetti che NB-2 originale doveva eliminare.

5. **Cosa il fix v2 avrebbe dovuto fare**: o (a) sanare l'incoerenza Cap.25.5/Cap.26.7 applicando uniformemente il censoring 0,7 e dichiarando $K_{max} \leq 4$ (con $44/4 = 11 \geq 10$), oppure (b) motivare esplicitamente perche' il rate non-censurato non si applica al conteggio Harrell (es. ridefinire $N_{eventi}$ come segnali eseguiti, divergendo dalla definizione standard).

**Evidenza testuale**:

- Cap.25.5 riga 427: "tasso di emissione 1-3 segnali/sessione, $N_{eventi}$ atteso $\in [120; 380]$ segnali eseguiti per fold... ogni sottostrato ha $N_{eventi} \in [60; 190]$. Con $K_{max} = 6$ per strato, il rapporto $N_{eventi}/K_{max} \in [10; 32]$ rispetta la soglia $\geq 10$ di Harrell **in tutti i fold compreso il caso pessimo $N_{eventi,strato} = 60$**".
- Cap.26.7 riga 651: "$N_{eventi}$ atteso per fold (... rate non-censurato $\approx 0,7$): $N_{eventi} \in [88; 264]$".
- Cap.26.7 riga 652: "Assumendo split 50/50, ogni strato ha $N_{eventi} \in [60/2; 264/2] \cdot 2 = [60; 190]$ (il caso pessimo e' $N_{eventi,\text{strato}} \approx 60$)".

**Fix richiesto**:
- (a) Allineare Cap.25.5 e Cap.26.7 sulla definizione di $N_{eventi}$. Se il censoring 0,7 si applica, il caso pessimo strato e' 44 e $K_{max} \leq 4$ e' il valore Harrell-compliant; rivedere il fix v2 NB-2 con $K_{max}=4$. Se invece $N_{eventi}$ e' "segnali eseguiti" (no censoring), Cap.26.7 va corretto e il caso pessimo 60 diventa difendibile sotto $K_{max}=6$.
- (b) Sanare l'aritmetica errata "$[60/2; 264/2] \cdot 2 = [60; 190]$" -> la formula corretta dipende dalla decisione (a).
- (c) Correggere la dichiarazione "valore centrale $\approx 120$" di Cap.26.7 riga 651: il valore centrale di $[88; 264]$ e' 176; 120 e' il punto centrale del range $[88; 264]$ assumendo distribuzione lineare scalata su 126 sessioni × 2 segnali medi × 0,7 censoring = 176... la cifra 120 e' semplicemente sbagliata.

**Classificazione**: **BUG REALE**. Errore aritmetico + errore di applicazione del censoring + incoerenza inter-capitolo. Il fix v2 NB-2 era basato su un calcolo che non sostiene la decisione di Parte V (stratificazione + $K_{max}=6$). Impatto operativo sul ranking del Pareto attraverso la cascata $\hat{p}_{hit}$ biased $\to$ $E_{surv}$ distorto $\to$ fitness $f_1$-$f_5$ con valori distorti su fold pessimi $\to$ ranking alterato.

---

### NB-v3-2 -- Chiusura solo formale di RP-1: motivazione di T_budget=80h cita un calcolo Cap.23.6 ORMAI OBSOLETO (Cap.26.2 riga 523, Cap.26.5 riga 603, contraddizione con Cap.23.6 riga 223)

**Impatto GA**: il criterio compute-budget di Cap.26.2 e' il terzo criterio di stop del NSGA-II. Se $T_{budget}$ e' motivato su un calcolo obsoleto e non copre il caso ottimo del calcolo aggiornato, il run reale si interrompe prima del completamento del walk-forward nested $F=8$. Conseguenza: bundle parziale con fronte di Pareto $\mathcal{F}_1$ valutato su una frazione dei fold (107h / 80h * 8 = 5,98 fold completati nel caso ottimo); l'aggregazione cross-fold mediana di Cap.24.6 opera su un campione ridotto con varianza inflated; la selezione del bundle frozen in Parte VII (gate DSR/PBO) e' basata su metriche stimate con incertezza maggiore.

**Evidenza testuale**:

- **Cap.26.2 riga 523**: "$T_{budget} = 80$ ore e' coerente con il caso ottimo del calcolo di Cap.23.6 (72 ore caso ottimo per 8 fold sequenziali); il margine di 8 ore (~11%) copre la varianza wall-clock attesa di c5.4xlarge spot... permettendo al GA di completare $F = 8$ fold sequenziali del walk-forward nested nel caso ottimo senza rientro in stop forzato".

- **Cap.26.5 riga 603**: "$T_{budget}$ -- budget compute wall-clock | 80 | Cap.26.2 PV | Coerente Cap.4 PI / Cap.23.6 PV; **copre caso ottimo $F = 8$ fold sequenziali (~72 ore)** con margine ~11%".

- **Cap.23.6 riga 223** (versione POST-fix v2 NB-1): "Estendendo a $F$ fold del walk-forward nested completo (Cap.25.1, $F = 8$ provvisorio), il totale e' $F \cdot 12.800\text{-}25.600 = 102.400\text{-}204.800$ min single-thread. Su c5.4xlarge con 16 vCPU... il tempo wall-clock e' $102.400/16 = 6.400$ min $\approx 107$ ore (caso ottimo) e $204.800/16 = 12.800$ min $\approx 213$ ore (caso pessimo)... **con l'aggiornamento $T_{budget} = 80$ ore wall-clock (Cap.26.2, in chiusura RP-1 Review v1), il caso ottimo del walk-forward nested $F = 8$ (circa 107 ore wall-clock con $t_{eval}$ inferiore 0,74 min/cromosoma) eccede il budget**... Il valore $T_{budget} = 80$ ore copre il **caso ottimo della stima Cap.23.6 ORIGINALE** (~72 ore wall-clock, ottenuta con la derivazione $r_{cache}$/min-per-fold dell'iterazione v1 PRIMA del riallineamento M-4) e il run di calibrazione iniziale (singolo fold di lavoro) con margine".

**Cosa significa concretamente**: Cap.23.6 stesso dichiara che il calcolo "72h caso ottimo F=8" su cui Cap.26.2 e Cap.26.5 motivano $T_{budget}=80$h **NON esiste piu'**. Il calcolo coerente con la versione attuale e' 107h ottimo / 213h pessimo. Cap.26.2 cita un numero obsoleto come motivazione del valore aggiornato -- e' una **contraddizione interna del documento**, mascherata dal fatto che Cap.23.6 riconosce esplicitamente la tensione.

Il Reviewer v2 ha visto questa tensione (lo dichiara esplicitamente in REVIEW v2 riga 27 e 113) e l'ha accettata come "rinviata trasparentemente a Parte VII Cap.34". Ma il problema NON e' la trasparenza del rinvio: il problema e' che la **motivazione testuale di Cap.26.2 cita un calcolo che il documento stesso dichiara obsoleto**. Il lettore di Cap.26.2/Cap.26.5 isolatamente legge "80h coerente con 72h ottimo" e non vede mai che il vero ottimo e' 107h. La motivazione e' formalmente disonesta -- non perche' il Developer abbia mentito, ma perche' ha modificato Cap.23.6 senza riallineare Cap.26.2 e Cap.26.5 al nuovo calcolo.

**Fix richiesto**:
- Cap.26.2 riga 523 e Cap.26.5 riga 603 devono citare il calcolo POST-fix v2 (107h ottimo, non 72h). Esempio: "$T_{budget}=80$h NON copre il caso ottimo aggiornato F=8 (107h post-riallineamento M-4); copre il run di calibrazione iniziale (singolo fold) con margine ~11%; per F=8 completo serve riduzione di F oppure parallelizzazione > 16 vCPU (rinvio Cap.23.6, decisione Parte VII Cap.34)".
- L'alternativa coerente e' alzare $T_{budget}$ a un valore che copre 107h con margine (es. 120h) o ridurre F al numero massimo compatibile con 80h (5-6 fold nel caso ottimo).

**Classificazione**: **BUG REALE** (di motivazione testuale). La sostanza decisionale del supervisore ($T_{budget}=80$h ratificato) resta valida; ma la motivazione di Cap.26.2 e Cap.26.5 e' incoerente con Cap.23.6 nello stesso documento. Impatto sul GA: il run reale si interrompe a ~56% dei fold nel caso ottimo (80h vs 107h) producendo bundle parziale.

---

### O-v3-1 -- Cap.26.7 riga 651 "valore centrale ≈ 120" non corrisponde al range [88; 264] dichiarato (Cap.26.7 riga 651)

**Impatto GA**: zero. E' una incoerenza numerica residua: $N_{eventi}$ atteso e' dichiarato $\in [88; 264]$ con "valore centrale ≈ 120" -- ma il centro del range e' 176, non 120. La cifra 120 sembra derivata da una stima diversa (es. 126 sessioni × 1 segnale/sessione × 0,95 ≈ 120, senza censoring, oppure 1 segnale/sessione mediano × 0,7 × 126 ≈ 88). Comunque non coerente con il range dichiarato nella stessa riga.

**Classificazione**: NEUTRO. Errore formale che non impatta il comportamento del GA.

---

### O-v3-2 -- Cap.26.5 riga 609 descrizione "per strato sotto stratificazione" e' misleading (Cap.26.5 riga 609)

**Impatto GA**: zero operativo. La voce in tabella "$K_{max}$ -- cardinalita' feature attive survival (per strato sotto stratificazione Cap.25.5)" suggerisce che $K_{max}$ sia un parametro per strato, ma il cromosoma ha UN UNICO vettore $\mathbf{s}$ di 37 bit con $\sum_j s_j \leq K_{max}$ (Cap.22.6 e Cap.22.7 vincolo 4). Le stesse 6 feature attive sono usate per entrambi gli strati; solo i coefficienti $\beta$ sono diversi. La dicitura "per strato" e' interpretabile correttamente sotto Harrell (ogni strato stima 6 coefficienti dalle stesse 6 feature), ma confusa per il lettore che cerca lo spazio di selezione del cromosoma.

**Classificazione**: NEUTRO. Chiarimento testuale richiederebbe ~1 riga.

---

## Citazioni problematiche dal testo

- **Cap.26.7 riga 652** -- "Assumendo split 50/50, ogni strato ha $N_{eventi} \in [60/2; 264/2] \cdot 2 = [60; 190]$ (il caso pessimo e' $N_{eventi,\text{strato}} \approx 60$)" -- **BUG REALE** NB-v3-1: aritmetica errata ($[30; 132] \cdot 2 = [60; 264]$, non $[60; 190]$) + il range corretto a partire da Cap.26.7 riga 651 ($[88; 264]$) split 50/50 e' $[44; 132]$, non $[60; 190]$. Caso pessimo strato corretto e' 44, $K_{max}=6$ non garantisce Harrell.

- **Cap.25.5 riga 427** -- "tasso di emissione 1-3 segnali/sessione, $N_{eventi}$ atteso $\in [120; 380]$ segnali eseguiti per fold... ogni sottostrato ha $N_{eventi} \in [60; 190]$. Con $K_{max} = 6$ per strato, il rapporto $N_{eventi}/K_{max} \in [10; 32]$ rispetta la soglia $\geq 10$ di Harrell in tutti i fold compreso il caso pessimo $N_{eventi,strato} = 60$" -- **BUG REALE** NB-v3-1: la motivazione del fix v2 NB-2 si basa su una stima di $N_{eventi}$ inconsistente con la definizione Harrell (gli eseguiti non sono eventi se sono censurati `expired`).

- **Cap.26.2 riga 523** -- "$T_{budget} = 80$ ore e' coerente con il caso ottimo del calcolo di Cap.23.6 (72 ore caso ottimo per 8 fold sequenziali); il margine di 8 ore (~11%) copre la varianza wall-clock... permettendo al GA di completare $F = 8$ fold sequenziali del walk-forward nested nel caso ottimo senza rientro in stop forzato" -- **BUG REALE** NB-v3-2: cita "72h caso ottimo F=8" che Cap.23.6 riga 223 dichiara essere "la stima Cap.23.6 ORIGINALE, pre-riallineamento M-4"; il calcolo coerente e' 107h. La motivazione testuale e' contraddittoria con Cap.23.6 nello stesso documento.

- **Cap.26.5 riga 603** -- "$T_{budget}$ -- budget compute wall-clock | 80 | Cap.26.2 PV | Coerente Cap.4 PI / Cap.23.6 PV; copre caso ottimo $F = 8$ fold sequenziali (~72 ore) con margine ~11%" -- stessa contraddizione di Cap.26.2 (parte di NB-v3-2).

- **Cap.26.1 riga 513** -- "Compute budget P × G_max valutazioni ≈ 19.328 (Cap.23.6), dentro il range 12.800-25.600 min single-thread di M-4" -- **NEUTRO** O-v2-1 confermato: residuo formale identico a NB-1 originale (19.328 valutazioni ≠ minuti). Reviewer v2 l'ha classificato NEUTRO; confermo.

- **Cap.26.7 riga 651** -- "$N_{eventi}$ atteso per fold... $N_{eventi} \in [88; 264]$, valore centrale $\approx 120$" -- **NEUTRO** O-v3-1: il centro di $[88; 264]$ e' 176, non 120.

---

## Verifica chiusure CARRYOVER

| M-ID | Origine | Chiusura dichiarata in CAP-05 | Verifica v3 indipendente |
|------|---------|-------------------------------|--------------------------|
| **M-4** | Review v4 CAP-01 | CLOSED-CAP-05 (Cap.23.6: $t_{eval} \in [0,74; 1,47]$ min/cromosoma post-rework v2) | **OK** -- chiusura coerente con NB-1 chiuso. |
| **M-5** | Review v1 CAP-03 | CLOSED-CAP-05 (Cap.25.3: 7 candidate windows + Inoue-Rossi + rollback) | **OK** -- protocollo deterministico ben formalizzato. |
| **M-6** | Review v1 CAP-03 | CLOSED-CAP-05 (Cap.25.4: $\eta_{div}$ + soglia 0,10) | **OK**. |
| **M-2 v2** | Review v2 CAP-03 | CLOSED-CAP-05 PARZIALE (Cap.25.9: walk-forward chiuso; production carryover CAP-06) | **OK** -- separazione PV/PVI esplicita. |
| **M-7** | Review v1 CAP-04 | CLOSED-CAP-05 (Cap.25.6: Cox-Snell + Schoenfeld stratificato + AND logico) | **OK**. |
| **M-8** | Developer CAP-04 | CLOSED-CAP-05 (Cap.25.6) | **OK** -- stesso protocollo di M-7. |
| **M-9** | Developer CAP-04 | CLOSED-CAP-05 (Cap.25.7: Brier + Diebold-Mariano) | **OK**. |
| **M-10** | Developer CAP-04 | CLOSED-CAP-05 (Cap.25.8: test χ² globale; carryover M-16) | **OK**. |
| **M-11** | Developer CAP-04 | CLOSED-CAP-05 ($K_{max}=6$ per strato congelato; Harrell rispettato sotto split 50/50 con $N_{eventi,strato} \geq 60$) | **CONTESTATO** -- vedi NB-v3-1. La chiusura dichiara "$N_{eventi,strato} \geq 60$" ma sotto censoring 0,7 di Cap.26.7 il caso pessimo e' 44. La chiusura di M-11 e' incompleta sotto le definizioni del documento. |
| **M-14** | Developer CAP-04 | CLOSED-CAP-05 (Cap.25.5: stratificazione + rollback CV>0,5 starting point) | **OK** condizionale a M-11 -- la coerenza fra opzione (b) stratificazione e $K_{max}$ dipende dalla risoluzione di NB-v3-1. |
| **M-15** | Developer CAP-04 | CLOSED-CAP-05 (Cap.26.5/26.6: $A_{range,min}=80$ non congelabile + 5 parametri) | **OK**. |
| **M-16 condizionale** | Review v1 CAP-05 (Cap.25.8 trigger) | OPEN-CONDIZIONALE (attivo solo se Schoenfeld viola sistematicamente >50% fold) | **OK** -- formulazione corretta come condizionale. |

**Sintesi CARRYOVER v3**: 11 M-promemoria dichiarati CLOSED-CAP-05; **M-11 contestato** sulla base di NB-v3-1 (chiusura formale ma non sostanziale). M-16 condizionale ben formulato.

---

## Classificazione per il supervisore

| # | Problema | Classificazione | Default | Mandare a Development? |
|---|----------|-----------------|---------|------------------------|
| 1 | **NB-v3-1** -- Calcolo censoring incoerente Cap.25.5/Cap.26.7; aritmetica errata; Harrell violato nel caso pessimo strato sotto $K_{max}=6$ | **BUG REALE** | SI -- Developer (obbligatorio) | SI |
| 2 | **NB-v3-2** -- $T_{budget}=80$h motivato su calcolo Cap.23.6 ORMAI OBSOLETO; Cap.26.2/Cap.26.5 contraddicono Cap.23.6 nello stesso documento | **BUG REALE** | SI -- Developer (obbligatorio) | SI |
| 3 | **O-v3-1** -- Cap.26.7 riga 651 "valore centrale ≈ 120" non corrisponde al range $[88; 264]$ | NEUTRO | NO -- ignorato | NO (zero impatto GA) |
| 4 | **O-v3-2** -- Cap.26.5 riga 609 dicitura "per strato sotto stratificazione" misleading vs Cap.22.7 vincolo 4 | NEUTRO | NO -- ignorato | NO (chiarimento testuale) |
| 5 | **O-v2-1 confermato** -- Cap.26.1 riga 513 ambiguita' valutazioni vs minuti (residuo formale NB-1) | NEUTRO | NO -- ignorato | NO (Reviewer v2 lo aveva gia' flaggato come NEUTRO) |

**Riepilogo classificazione v3**:
- **BUG REALI**: 2 (NB-v3-1, NB-v3-2) -- a Developer obbligatorio.
- **NEUTRO**: 3 (O-v3-1, O-v3-2, O-v2-1) -- ignorati di default.
- **MIGLIORA PERFORMANCE**: 0.
- **RISCHIO PEGGIORAMENTO**: 0.

---

## Verdetto finale

**CONDITIONAL**

Il Reviewer v2 ha dato PASS troppo morbido su due chiusure (NB-2 e RP-1) che apparentemente erano risolte ma poggiano su calcoli/motivazioni incoerenti che il fix v2 ha solo spostato, non sanato. Il supervisore ha riaperto la review correttamente: c'erano cose da trovare.

**NB-v3-1 (chiusura incompleta NB-2)** e' il problema piu' grave per la performance del GA. La stima $\hat{p}_{hit}$ Cox cause-specific entra direttamente nel filtro $E_{surv}$ (Cap.20.1 PIV) che gate-keepa l'emissione del segnale. Se la stima e' biased perche' la stratificazione opera su strati troppo piccoli per Harrell, il filtro emette o sopprime segnali su una probabilita' predittiva distorta, e il GA ottimizza il cromosoma su una fitness derivata da segnali filtrati in modo biased. Il ranking del fronte di Pareto risulta alterato in maniera difficile da quantificare a priori -- l'intero scopo del fix NB-2 era proprio prevenire questa cascata.

**NB-v3-2 (chiusura formale RP-1)** e' meno grave operativamente (il valore numerico $T_{budget}=80$h e' ratificato dal supervisore e resta valido come decisione), ma e' un BUG di **integrita' testuale**: Cap.26.2 e Cap.26.5 motivano il valore citando un calcolo che lo stesso Cap.23.6 dichiara obsoleto. La conseguenza operativa e' che il run reale si interrompe a ~56% del walk-forward nel caso ottimo (80h vs 107h aggiornati), producendo bundle parziale con aggregazione cross-fold di varianza inflated; il documento non lo dice nei punti dove il lettore lo cerca (Cap.26.2 e Cap.26.5) ma lo confessa solo in Cap.23.6 riga 223.

I 3 NEUTRO (O-v3-1, O-v3-2, O-v2-1) sono residui formali senza impatto sul GA; non vanno a Developer di default.

**Raccomandazione al supervisore**:

1. **Mandare NB-v3-1 a Developer**: l'opzione concreta e' scegliere fra (a) ridurre $K_{max}$ a 4 sotto la stima censurata di Cap.26.7 (sicuro Harrell-compliant), oppure (b) sanare Cap.26.7 ridefinendo $N_{eventi}$ coerentemente con Cap.25.5 (no censoring nel conteggio) -- quale delle due richiede decisione del supervisore o del Developer motivata nel REPORT.

2. **Mandare NB-v3-2 a Developer**: l'opzione e' (a) riallineare la motivazione di Cap.26.2 e Cap.26.5 al calcolo POST-fix v2 (107h non 72h), dichiarando trasparentemente che 80h NON copre F=8 ottimo; oppure (b) alzare $T_{budget}$ al valore che copre 107h+margine (es. 120h); oppure (c) ridurre F al numero massimo compatibile con 80h.

3. **Lasciare i 3 NEUTRO**: senza impatto operativo. Reviewer v2 e v1 li avevano gia' valutati o non visti.

Se supervisore approva entrambi i BUG REALI, e' atteso un rework v3 chirurgico (~15-25 righe modificate complessive in Cap.25.5, Cap.26.2, Cap.26.5, Cap.26.7). Non si richiede splitting ne' rework completo della Parte V.
