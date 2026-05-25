# Review CAP-05 -- Parte V: Motore genetico, fitness operativa, walk-forward nested, calibrazione

**Verdetto**: CONDITIONAL

**Commit oggetto**: 08e9216 [DEV] CAP-05 v1
**Data**: 2026-05-25
**Natura**: Audit ostile Iterazione 1
**Reviewer**: Review Agent

---

## Sintesi del verdetto

CONDITIONAL. Il documento e strutturalmente completo (5 capitoli Cap.22-26, ~10 pp, italiano formale, tutte le citazioni obbligatorie presenti), copre il cromosoma di 52 geni, gli operatori NSGA-II, la fitness multi-obiettivo a 5 obiettivi con 3 penalita, lo schema walk-forward nested con purge ed embargo, i protocolli di rollback automatico per i 4 M-promemoria survival (M-5, M-7+M-8, M-9, M-10) e la tabella di congelamento Cap.26.5.

Non si rilevano BUG REALI strutturali che invalidano l architettura del motore. Si rilevano 3 problemi non bloccanti che hanno impatto formale sull AC-23-5 (derivazione M-4 incoerente nelle unita), sull AC-26-8 (incoerenza K_max con stratificazione Cap.25.5) e su AC-24-2 (nomenclatura MAE alla scadenza incoerente con regola operativa di chiusura virtuale). Si rilevano 3 osservazioni di RISCHIO PEGGIORAMENTO che impattano potenzialmente il ranking del fronte di Pareto sotto budget compute insufficiente e sotto aggregazione metrica f_5 mista. Si rilevano 5 NEUTRO (conteggi, ambiguita formali non operative).

Nessun finding richiede splitting Parte V.A + Parte V.B. La proposta di rollback del Developer prevede mini-patch su Cap.23.6, Cap.26.7, Cap.24.1 senza rework completo: percorribile.

---

## Tabella AC (52 voci + AC-T-9 condizionale)

### Struttura e completezza generale

| AC-ID | Esito | Nota Reviewer |
|-------|-------|---------------|
| AC-1 | OK | 5 capitoli Cap.22-26 presenti, ordine corretto, ~10 pp. |
| AC-2 | PARZIALE | 42/44 eredita con cross-ref letterale. Eredita 16 (Telegram 9 voci Cap.9.2 PII) e 41 (filtro implicito fine sessione T_residuo Cap.20.4 PIV) con cross-ref implicito; non bloccante. |
| AC-3 | OK | 15 M-promemoria pertinenti coperti (REPORT dichiara 16 ma sono 15 pertinenti CAP-05; M-2 originale e carryover Appendice E). |
| AC-4 | OK | Sezione "Misura prima/dopo" con tabella 26 righe; impatto sul GA dichiarato. |
| AC-5 | OK | Italiano formale tecnico; LaTeX inline e display; citazioni inline. |

### Cap.22 -- Cromosoma

| AC-ID | Esito | Nota Reviewer |
|-------|-------|---------------|
| AC-22-1 | OK | Cap.22.9 tabella 16 righe gene/simbolo/dominio/encoding/regime/eredita. |
| AC-22-2 | OK | Geni geometrici (Cap.22.2), emissione (22.3), target/stop (22.4), temporali (22.5). |
| AC-22-3 | OK | s in {0,1}^37 con somma s_j <= K_max in Cap.22.6. |
| AC-22-4 | OK | 7 vincoli enumerati Cap.22.7 con eredita riferite. Cfr. O-2 sulla ambiguita del vincolo 2. |
| AC-22-5 | OK | Encoding misto coerente con operatori Cap.23.2-23.3. |
| AC-22-6 | OK | K + K' + K'' = 9 + 6 + 37 = 52 geni in Cap.22.9. |
| AC-22-7 | OK | Cap.22.9 chiusura "Provvisorieta" rinvia tutto a Cap.26.5. |

### Cap.23 -- Operatori GA

| AC-ID | Esito | Nota Reviewer |
|-------|-------|---------------|
| AC-23-1 | OK | NSGA-II + Deb et al. (2002) IEEE TEC 6(2). |
| AC-23-2 | OK | SBX/uniform/uniform-vincolato + polynomial/random reset/bit flip + (mu+lambda). |
| AC-23-3 | OK | Constraint-domination Deb (2000) citato Cap.23.4. |
| AC-23-4 | OK | r_repl definito; formula N_eval^actual in Cap.23.6. |
| AC-23-5 | PARZIALE | Derivazione 17.408 valutazioni OK; derivazione range 12.800-25.600 min single-thread incoerente nelle unita (cfr. NB-1). |
| AC-23-6 | OK | Cap.23.6.1 rinvia a Parte VII Cap.34. |
| AC-23-7 | OK | Seed Cap.23.7 + Cap.26.8 con cross-ref Cap.10 PII. |

### Cap.24 -- Fitness multi-obiettivo

| AC-ID | Esito | Nota Reviewer |
|-------|-------|---------------|
| AC-24-1 | OK | M=5 con direzione max/min per ogni obiettivo. |
| AC-24-2 | PARZIALE | Formula E[R_net|executed] = E[R_gross] - 2c OK; nomenclatura "MAE alla scadenza" per expired posttrigger_timeout incoerente con regola operativa "chiusura virtuale al prezzo della barra" (cfr. NB-3). |
| AC-24-3 | OK | f_2, f_3, f_4, f_5 formalizzati con formule chiuse. |
| AC-24-4 | OK | 3 penalita con E_max, E_min, E_exp,max provvisori. |
| AC-24-5 | OK | N-1 v2 CAP-03 trattato in Cap.24.3. |
| AC-24-6 | OK | Target 500pt/70% come reporting in Cap.24.4 con motivazione. |
| AC-24-7 | OK | Delta_t_pretrigger separato Delta_t_cromosoma in Cap.24.5. |
| AC-24-8 | OK | executable_rate ridefinita post-patch Iterazione 2 in Cap.24.5. |
| AC-24-9 | OK | Mediana cross-fold + IQR Cap.24.6. Cfr. RP-2 sull aggregazione f_5^global. |
| AC-24-10 | OK | Cap.24.7 esplicita. |

### Cap.25 -- Walk-forward + diagnostica survival

| AC-ID | Esito | Nota Reviewer |
|-------|-------|---------------|
| AC-25-1 | OK | W_in=105.840, W_oos=52.920, P_purge=P_emb=4.200, F=8 provvisorio. |
| AC-25-2 | OK | Lopez de Prado (2018) cap. 7 citato Cap.25.2. |
| AC-25-3 | OK | 7 candidate windows + Inoue-Rossi 2011 Cap.25.3. |
| AC-25-4 | OK | Rollback deterministico Cap.25.3 con soglia p=0.05 + tie-break. |
| AC-25-5 | OK | Cap.25.4 formula eta_div + soglia 0,10 + flag instabile. |
| AC-25-6 | OK | Cap.25.5 opzione (b) stratificazione + rollback CV>0,5. Cfr. NB-2 incoerenza K_max. |
| AC-25-7 | OK | Cox-Snell 1968 + Grambsch-Therneau 1994 in Cap.25.6 con AND logico. |
| AC-25-8 | OK | Brier + Diebold-Mariano 1995 Cap.25.7. |
| AC-25-9 | OK | Cap.25.8 separato; rinvio Parte VII su violazione sistematica. |
| AC-25-10 | OK | Separazione walk-forward / production esplicita Cap.25.9. |

### Cap.26 -- Calibrazione e congelamento

| AC-ID | Esito | Nota Reviewer |
|-------|-------|---------------|
| AC-26-1 | OK | P=128, G_max=150 Cap.26.1 con motivazione. |
| AC-26-2 | OK | 3 criteri stop Cap.26.2. Cfr. RP-1 sulla tensione T_budget=60h vs F=8. |
| AC-26-3 | OK | Student-t default + Ljung-Box tie-break Cap.26.3. |
| AC-26-4 | OK | Opzione A confermata Cap.26.4. |
| AC-26-5 | OK | Tabella 60 voci Cap.26.5 completa (REPORT dichiara 55 ma sono 60: errore conteggio non strutturale). |
| AC-26-6 | OK | A_range,min=80 NON congelabile esplicito. |
| AC-26-7 | OK | Cap.26.6 no floor default + attivazione condizionata. |
| AC-26-8 | PARZIALE | K_max=12 + Harrell 2015 OK su fold non stratificato; incoerente con decisione di stratificazione Cap.25.5 (cfr. NB-2). |
| AC-26-9 | OK | Seed Cap.26.8 componenti listati. |

### Vincoli trasversali

| AC-ID | Esito | Nota Reviewer |
|-------|-------|---------------|
| AC-T-1 | OK | Tick FIB 5pt rispettato. |
| AC-T-2 | OK | Determinismo bit-exact Cap.23.7 + Cap.26.8. |
| AC-T-3 | OK | Causalita F_{t-1} rispettata. |
| AC-T-4 | OK | Provvisorieta Cap.22.9 + tabella Cap.26.5. |
| AC-T-5 | OK | Registro tecnico italiano + LaTeX + esempi numerici Cap.22.9 e Cap.23.6. |
| AC-T-6 | OK | Citazioni Deb 2002, Deb 2000, Lopez de Prado 2018, Inoue-Rossi 2011, Cox-Snell 1968, Grambsch-Therneau 1994, Fine-Gray 1999, Diebold-Mariano 1995, Harrell 2015, Bollerslev 1987, Engle-Sokalska 2012, Klein-Moeschberger 2003 tutte presenti. |
| AC-T-7 | OK | REPORT 5 sezioni + criterio rollback. |
| AC-T-8 | OK | 00_indice.md riflette Parte V "IN REVIEW v1". |
| AC-T-9 | OK | Commit 08e9216 su origin/main. |

**Sintesi AC**: 52 voci totali. 47 OK puntuali, 4 PARZIALI (AC-2, AC-23-5, AC-24-2, AC-26-8) dichiarate trasparentemente, AC-T-9 confermato post-push. Nessun MANCA strutturale.


---

## Finding ordinati per gravita

### NB-1 -- Derivazione 12.800-25.600 min di M-4 incoerente nelle unita (Cap.23.6, righe 209-215)

**Impatto GA**: nessuno operativo immediato (il GA usa T_budget wall-clock di 60 ore in Cap.26.2, non i minuti single-thread M-4). Tuttavia, l AC-23-5 richiede derivazione analitica del range 12.800-25.600 min single-thread (M-4) che produce numeri specifici. La derivazione data nel documento e numericamente incoerente.

**Evidenza**. Cap.23.6 a riga 211 dichiara:

Caso ottimo (r_cache = 0,15, valutazione 0,5 min/cromosoma): N_eval^actual = 128 * (1 + 150 * 0,85) = 128 * 128,5 = 16.448; tempo single-thread 16.448 * 0,5 = 8.224 min per fold.

A riga 215, il documento scrive:

Il valore inferiore 12.800 e coerente con il caso ottimo per singolo run di calibrazione (16.448 * 0,8 ~= 13.000, dove il fattore 0,8 cattura un ulteriore margine ottimistico di caching e parallelizzazione locale entro un fold).

16.448 * 0,8 = 13.158 e in **unita di valutazioni** (riduzione del numero di valutazioni effettive per caching aggiuntivo), non in **minuti**. Il M-4 di CAP-01 e espresso in minuti single-thread (range 12.800-25.600 min). La derivazione confonde unita: applica un fattore alle valutazioni e poi etichetta il risultato come minuti.

Per ottenere 12.800 min single-thread con valutazione 0,5-1 min/cromosoma, servirebbero [12.800; 25.600] valutazioni a 1 min/cromosoma, oppure [25.600; 51.200] valutazioni a 0,5 min/cromosoma. Il caso ottimo dichiarato N_eval^actual = 16.448 a 0,5 min/cromosoma produce 8.224 min, non 12.800 min. Il caso pessimo N_eval^actual = 18.368 a 1 min/cromosoma produce 18.368 min, dentro al range 12.800-25.600 ma il caso ottimo manca dal range.

Il documento riconosce parzialmente questo bug a riga 215 attribuendo il valore 25.600 a valutazione fitness intorno a 1,4 min/cromosoma (18.368 * 1,4 ~= 25.700) - qui le unita sono coerenti (val * min/val = min), ma quel risultato implica che la valutazione fitness e 0,7-1,4 min/cromosoma (non 0,5-1 come dichiarato sopra).

**Fix richiesto**. Riallineare le unita in Cap.23.6 e dichiarare esplicitamente il range di valutazione fitness t_eval in [t_min, t_max] min/cromosoma coerente con il range M-4: con N_eval^actual = 17.408 centrale, t_eval in [12.800/17.408, 25.600/17.408] = [0,74; 1,47] min/cromosoma. Alternativamente, ridichiarare il range M-4 effettivo coerente con t_eval in [0,5; 1] min/cromosoma e N_eval^actual in [16.448; 18.368], che produce [8.224; 18.368] min single-thread per singolo run di calibrazione.

**Classificazione**: BUG REALE (errore di derivazione formale; non impatta il comportamento del GA ma viola l AC-23-5 e la coerenza inter-capitolo con CAP-01).
---

### NB-2 -- Incoerenza K_max=12 congelato vs decisione stratificazione formale di Cap.25.5 (Cap.26.7 righe 645-649, Cap.25.5 riga 421)

**Impatto GA**: la stima Cox cause-specific stratificata per regime con K=12 feature per strato e N_eventi atteso >= 60 per strato (caso pessimo del fold con split 50/50) non rispetta la rule of thumb di Harrell (2015) (N_eventi/K >= 10 richiede K <= 6 per strato). La stima MLE risulta sovra-parametrizzata, con coefficienti beta_{j,R} instabili cross-fold (variance inflation, overfitting). La stima p_hit e biased, e il filtro E_surv (Cap.20 PIV) usa una stima distorta. Il GA ottimizza su una fitness f_1-f_5 che dipende da p_hit distorto: il ranking del fronte di Pareto e alterato.

**Evidenza**. Cap.25.5 a riga 421 dichiara la stratificazione formale come decisione default di Parte V, con motivazione:

Costo in parametri contenuto: il raddoppio dei coefficienti beta_j (da K <= K_max = 12 a 2K <= 24) e gestibile sotto la rule of thumb di Harrell con N_eventi/K >= 10, purche N_eventi_calmo >= 10K e N_eventi_turbolento >= 10K separatamente. Per un fold con W_in ~= 105.840 barre ~= 126 sessioni e tasso di emissione 1-3 segnali/sessione, N_eventi atteso >= 120-380 segnali eseguiti per fold; ripartito 50/50 fra calmo e turbolento, ogni sottostrato ha >= 60-190 eventi, sufficienti per K <= 12.

Calcolo N_eventi/K nel caso pessimo N_eventi_strato = 60 e K = 12: rapporto = 5. Harrell 2015 cap. 4 prescrive >= 10, non >= 5. Il documento dichiara >= 60 sufficienti per K <= 12 senza giustificare il salto da 5 a 10.

Cap.26.7 a riga 647 riconosce esplicitamente la contraddizione:

Sotto stratificazione del Cox per regime (Cap.25.5), N_eventi/K >= 10 deve valere per ciascuno strato separatamente: N_eventi_calmo, N_eventi_turbolento >= 10 K_max. Assumendo split 50/50, ogni strato ha N_eventi >= 60, e il vincolo e K_max <= 6 per strato.

Pero immediatamente dopo (riga 649): Valore congelato di lavoro: K_max = 12. Il documento congela K_max = 12 pur riconoscendo che la decisione di Parte V (stratificazione) impone K_max <= 6.

Inoltre Cap.26.7 a riga 645 calcola N_eventi in [88; 264] applicando un rate non-censurato ~= 0,7; Cap.25.5 calcola N_eventi in [120; 380] senza il rate. Incoerenza minore di stima cross-capitoli (la differenza e il fattore 0,7 dei censuranti).

**Fix richiesto**. Una delle tre opzioni:

(a) Congelare K_max = 6 in Cap.26.5 e Cap.26.7, coerente con la decisione di Parte V (stratificazione). Aggiornare Cap.25.5 per dichiarare che con K <= 6 la stratificazione rispetta Harrell.

(b) Mantenere K_max = 12 ma cambiare la decisione di Parte V in Cap.25.5 da stratificazione formale default a interaction term default, coerente con N_eventi/K >= 10 su un singolo modello con K + 1 feature (regime indicatore). La stratificazione resta come opzione di rollback condizionata a N_eventi_strato >= 10 K_max.

(c) Mantenere entrambi i parametri (K_max = 12 + stratificazione default) ma dichiarare esplicitamente che la rule of thumb di Harrell e ammorbidita a N_eventi/K >= 5 con citazione di una fonte specifica che giustifichi il salto.

**Classificazione**: BUG REALE (la decisione di stratificazione di Parte V e il valore congelato di K_max in tabella sono mutualmente incompatibili sotto la rule of thumb dichiarata; la stima p_hit e biased e il GA e ranking-distorto).

---

### NB-3 -- Nomenclatura MAE alla scadenza incoerente con definizione operativa di chiusura virtuale (Cap.24.1, riga 239)

**Impatto GA**: la regola operativa di calcolo di R_gross per i segnali in stato terminale expired con causa posttrigger_timeout e univoca e coerente (rendimento dal prezzo di fill al prezzo di chiusura virtuale forzata alla barra in cui Delta_t_cromosoma e scaduto). Quindi il GA opera deterministicamente. Tuttavia, la nomenclatura MAE alla scadenza e scorretta: MAE (Maximum Adverse Excursion) e per definizione il massimo movimento avverso durante l intero segnale, non il rendimento al momento dell expiry. Un revisore o un implementatore che leggesse MAE alla scadenza potrebbe calcolare il rendimento al peggior punto del segnale anziche alla chiusura virtuale, producendo ranking distorto.

**Evidenza**. Cap.24.1 riga 239:

Per i segnali con stato terminale expired (causa posttrigger_timeout), il rendimento e la MAE alla scadenza (Cap.10.4 di Parte II): il segnale viene chiuso virtualmente al prezzo della barra in cui il timer ha esaurito Delta_t_cromosoma, e R_gross e il rendimento dal prezzo di fill (worst-case bordo, Cap.12.4 di Parte III) al prezzo di chiusura virtuale forzata.

Le due frasi sono incompatibili: MAE implica un ottimizzazione sul peggior istante del segnale; rendimento dal prezzo di fill al prezzo di chiusura virtuale forzata implica solo l ultimo istante. Sono due quantita diverse.

**Fix richiesto**. Sostituire MAE alla scadenza con rendimento di chiusura virtuale forzata o rendimento al timeout post-trigger o equivalente nomenclatura coerente con la regola operativa. Mantenere la regola operativa (e corretta).

**Classificazione**: BUG REALE (di nomenclatura, non di comportamento). La regola operativa e univoca; la nomenclatura confonde. Costo del fix: minimo (sostituzione di un etichetta).

---

### RP-1 -- Tensione F=8 congelato vs T_budget=60 ore congelato sotto caso ottimo (Cap.26.2 righe 517, Cap.26.5 riga 614)

**Impatto GA**: nel caso ottimo del calcolo di Cap.23.6, il run completo del walk-forward nested richiede 72 ore wall-clock (8 fold x 9 ore/fold). T_budget = 60 ore e inferiore. Se il GA viene fermato a T_budget, il bundle parziale ha solo 6,7 fold completi (Cap.26.2 lo dichiara esplicitamente). Tuttavia, i cromosomi del fronte di Pareto F_1 sono valutati su un sottoinsieme di fold, e l aggregazione multi-fold (Cap.24.6: mediana cross-fold) e meno robusta. La selezione del bundle frozen in Parte VII opera su metriche stimate con varianza maggiore.

**Evidenza**. Cap.23.6 riga 217 calcola wall-clock 69.600/16 ~= 4.350 min ~= 72 ore (caso ottimo) per F = 8 fold. Cap.26.2 riga 517 dichiara T_budget = 60 ore coerente con il caso ottimo del calcolo di Cap.23.6 (72 ore caso ottimo per 8 fold => 60 ore per 6,7 fold). Cap.26.5 riga 614 congela F = 8.

La contraddizione: F = 8 congelato vincola il numero di fold, ma T_budget = 60 ore non lo permette nel caso ottimo. Cap.23.6 riconosce la tensione: F e dichiarato provvisorio e il numero effettivo di fold sequenziali nel training potra essere ridotto a 2-3 con run di calibrazione iniziale separato.

**Fix richiesto** (non obbligatorio, decisione supervisore). Una delle opzioni:

(a) Aumentare T_budget a 75-80 ore per coprire il caso ottimo 8 fold.

(b) Ridurre F a 6 (congruente con 60 ore / 9 ore/fold = 6,67 fold).

(c) Mantenere entrambi i valori ma dichiarare esplicitamente nella tabella Cap.26.5 che F = 8 e target nominale; F effettivo dipende dal budget compute e puo essere ridotto a 6 sotto vincolo T_budget.

**Classificazione**: RISCHIO PEGGIORAMENTO (potenziale degrado della robustezza della selezione del bundle se il GA e fermato prematuramente; non BUG perche la tensione e dichiarata).

---

### RP-2 -- Aggregazione f_5^global concatena segnali OOS di fold con EGARCH/Cox diversi (Cap.24.6, righe 324-325)

**Impatto GA**: f_5^global e calcolata concatenando tutti i segnali OOS di tutti gli F fold. Ma in Cap.25.9 l EGARCH e il Cox sono ri-stimati fold-per-fold (parametri congelati per fold). I segnali OOS provengono quindi da fold con beta_{j,k} e sigma_{t,k} diversi. La concatenazione mescola popolazioni di segnali con modelli locali diversi, e la stima della stabilita cross-regime f_5^global puo essere distorta da effetti di pooling cross-fold.

**Evidenza**. Cap.24.6 riga 324-325:

f_5^global - la stabilita cross-regime - e calcolata diversamente: si concatenano tutti i segnali OOS di tutti gli F fold, si separano per regime e si calcola f_5 sull intera storia OOS unificata. Questo perche f_5 misura intrinsecamente la disparita fra due sottoinsiemi (calmo vs turbolento) e l aggregazione per fold separati produrrebbe due livelli di mediana cross-fold, non interpretabili.

La motivazione e solida (no double median), ma la concatenazione di segnali generati da modelli diversi cross-fold introduce eterogeneita non controllata. Un cromosoma puo sembrare stabile cross-regime sull intera storia ma instabile in ogni singolo fold (effetto Simpson).

**Fix possibile** (non obbligatorio). Sostituire il pooling cross-fold con la mediana cross-fold di f_{5,k} stimata fold-per-fold sui segnali del singolo fold OOS (accettando la critica two-level median); oppure stratificare per fold nel calcolo di f_5^global con un modello a effetti misti che separi varianza intra-fold da varianza cross-fold.

**Classificazione**: RISCHIO PEGGIORAMENTO (l aggregazione mista puo produrre stime f_5 distorte; alternativa esiste ma e piu costosa metodologicamente).

---

### RP-3 -- Soglia theta_CV = 0,5 per rollback Cox stratificato senza giustificazione empirica (Cap.25.5 riga 423, Cap.26.5 riga 616)

**Impatto GA**: theta_CV = 0,5 e il trigger di rollback dal Cox stratificato (default Cap.25.5) all interaction term (rollback). Se troppo permissivo, il rollback e raro e il Cox stratificato sotto-dimensionato resta in uso anche quando i coefficienti sono instabili. Se troppo restrittivo, il rollback e frequente e il Cox cambia forma fold-per-fold, producendo ranking instabile.

**Evidenza**. Cap.25.5 riga 423:

Se la stratificazione formale produce instabilita eccessiva nei coefficienti fold-per-fold (specificamente, CV(beta_{j,R}) - coefficiente di variazione cross-fold dei coefficienti - superiore a una soglia theta_CV = 0,5 valore di lavoro), il modello e soggetto a rollback all opzione (a) interaction term per quel fold, con registrazione nel log di calibrazione. La soglia theta_CV = 0,5 e dichiarata provvisoria e congelata in Cap.26.5.

Il valore 0,5 non ha rule of thumb associata. Il REPORT lo riconosce come Punto che potrebbe generare finding di Review.

**Fix possibile** (non obbligatorio). Citare una fonte (es. Pencina e D Agostino 2004 sul CV di stima dei coefficienti Cox come threshold di stabilita) o dichiarare esplicitamente che theta_CV = 0,5 e starting point per il primo run di calibrazione, riconsiderato in Parte VII sulla base degli esiti empirici cross-fold.

**Classificazione**: RISCHIO PEGGIORAMENTO leggero (rollback Cox dipende da una soglia arbitraria; tracciabile via log e modificabile).

---

## Osservazioni minori (NEUTRO)

### O-1 -- Errore di conteggio voci tabella Cap.26.5 nel REPORT (REPORT righe 87, 174)

Il REPORT dichiara tabella unificata Cap.26.5 con 55 voci (riga 87) e 15 PII-III + 10 PIV + 6 trade_range + 24 PV = 55 voci (riga 174). Conteggio effettivo della tabella nel documento: 15 + 10 + 6 + 29 = 60 voci (la sottosezione PV ha 29 voci, non 24).

Impatto GA: zero. La tabella e completa nel documento; il conteggio nel REPORT e errato.

**Classificazione**: NEUTRO

---

### O-2 -- Ambiguita del vincolo 2 di Cap.22.7 (filtro 80 pt) come ammissibilita del cromosoma vs ammissibilita del segnale derivato (Cap.22.7 riga 83, Cap.23.4 riga 173)

Il vincolo 2 di Cap.22.7 dichiara che cromosomi che producono target_1 con |target_1 - p_ref| < 80 pt sono non validi. Ma target_1 e derivato (Cap.22.4), non gene: per verificare il vincolo serve simulare il fold. Cap.23.4 richiede v_k(theta) calcolabile pre-fitness per constraint-domination, ma il vincolo 2 non e calcolabile pre-fitness senza simulazione. Il documento risolve implicitamente trattando il vincolo come filtro strutturale del segnale derivato (Cap.17 PIV), ma la nomenclatura non valido del cromosoma e ambigua.

Impatto GA: nessuno operativo (Cap.17 PIV filtra il segnale a livello strutturale; cromosomi che producono solo segnali < 80 pt vengono valutati con bassissimo E_rate e penalizzati via E_min). Tuttavia, il testo e formalmente ambiguo.

**Classificazione**: NEUTRO

---

### O-3 -- Formula v_k normalizzata ad esempio in Cap.23.4 ambigua (Cap.23.4 riga 173)

normalizzata ad esempio rispetto al massimo della violazione k-esima nella popolazione corrente. Il ad esempio lascia indeterminato il criterio operativo di normalizzazione, mentre Deb 2000 lo specifica esplicitamente. Impatto GA: due implementazioni diverse possono produrre ordinamenti diversi fra cromosomi non ammissibili; il fronte F_1 e invariante perche gli ammissibili dominano gli non ammissibili comunque, ma la pressione selettiva interna al pool non ammissibile cambia.

**Classificazione**: NEUTRO

---

### O-4 -- Eredita 16 e 41 con cross-ref implicito (REPORT righe 107, 210)

Eredita 16 (Telegram 9 voci Cap.9.2 PII): citata indirettamente in Cap.24.2 (rumore sul canale Telegram) e in Cap.24.5 (campi del payload). Non c e cross-ref letterale a Cap.9.2.

Eredita 41 (filtro implicito fine sessione T_residuo Cap.20.4 PIV): citata indirettamente nel meccanismo survival di Cap.20 ma non come filtro implicito fine sessione o T_residuo -> 0 implica p_hit -> 0 ne come stress test in Cap.24-25.

Impatto GA: zero, il meccanismo e preservato (Cap.20 PIV non modificato). Cross-ref letterale ridurrebbe la difficolta di lettura a futura manutenzione.

**Classificazione**: NEUTRO

---

### O-5 -- Floor numerico max(..., 1) in denominatore f_5 (Cap.24.1 riga 256)

Il denominatore max(|f_1_calmo|, |f_1_turbolento|, 1) assume 1 punto FIB come scala minima. Un cromosoma con f_1 in (0; 1) pt avra denominatore 1 (cap inferiore), e f_5 scala in modo non lineare con f_1. La scala del floor e plausibile (1 pt = 1/5 di 1 tick FIB equivalente) ma non motivata esplicitamente.

Impatto GA: il floor regolarizza numericamente f_5 ma puo distorcere il ranking sotto cromosomi marginali (f_1 vicino a 0). Cromosomi degeneri (E_min penalty) sono comunque scartati.

**Classificazione**: NEUTRO (scelta numerica difendibile; non BUG).

---

## Citazioni problematiche dal testo

- Il valore inferiore 12.800 e coerente con il caso ottimo per singolo run di calibrazione (16.448 * 0,8 ~= 13.000, dove il fattore 0,8 cattura un ulteriore margine ottimistico di caching e parallelizzazione locale entro un fold) - Cap.23.6 riga 215 - confusione di unita (valutazioni vs minuti); il fattore 0,8 applicato a valutazioni produce un numero di valutazioni, non i minuti - BUG REALE NB-1.

- Valore congelato di lavoro: K_max = 12. La motivazione include il fold a piena cardinalita N_eventi ~= 120. Se la stratificazione produce strati sbilanciati con N_eventi piccolo per uno degli strati (es. fold prevalentemente turbolento con pochi segnali in regime calmo), il vincolo e riconsiderato in Parte VII via rollback a interaction term (Cap.25.5) - Cap.26.7 riga 649 - K_max = 12 e congelato ma la decisione di Parte V (stratificazione) non rispetta Harrell con questo valore di K_max sotto split 50/50 - BUG REALE NB-2.

- Per i segnali con stato terminale expired (causa posttrigger_timeout), il rendimento e la MAE alla scadenza (Cap.10.4 di Parte II): il segnale viene chiuso virtualmente al prezzo della barra in cui il timer ha esaurito Delta_t_cromosoma, e R_gross e il rendimento dal prezzo di fill (worst-case bordo, Cap.12.4 di Parte III) al prezzo di chiusura virtuale forzata - Cap.24.1 riga 239 - MAE alla scadenza non e il rendimento di chiusura virtuale - BUG REALE NB-3 (nomenclatura).

- T_budget = 60 ore coerente con il caso ottimo del calcolo di Cap.23.6 (72 ore caso ottimo per 8 fold => 60 ore per 6,7 fold ~= run di calibrazione iniziale + 5-6 fold completi) - Cap.26.2 riga 517 - la tensione F = 8 congelato vs T_budget = 60 ore congelato e dichiarata ma non risolta - RISCHIO PEGGIORAMENTO RP-1.

- f_5^global - la stabilita cross-regime - e calcolata diversamente: si concatenano tutti i segnali OOS di tutti gli F fold, si separano per regime e si calcola f_5 sull intera storia OOS unificata - Cap.24.6 riga 324 - pooling cross-fold di segnali generati da modelli EGARCH/Cox diversi - RISCHIO PEGGIORAMENTO RP-2.

- Se la stratificazione formale produce instabilita eccessiva nei coefficienti fold-per-fold (specificamente, CV(beta_{j,R}) superiore a una soglia theta_CV = 0,5 valore di lavoro), il modello e soggetto a rollback all opzione (a) interaction term per quel fold - Cap.25.5 riga 423 - soglia arbitraria senza fonte - RISCHIO PEGGIORAMENTO RP-3.

---

## PROMEMORIA / M-promemoria nuovi

Nessun M-promemoria nuovo emerge da questa Review per Parte VI/VII. Tutti i finding sono riparabili in mini-patch CAP-05.

---

## Classificazione per il supervisore

| # | Problema | Classificazione | Default | Mandare a Development? |
|---|----------|-----------------|---------|------------------------|
| 1 | NB-1 -- Derivazione 12.800-25.600 min M-4 incoerente nelle unita (Cap.23.6) | BUG REALE | SI -- Developer (obbligatorio) | SI |
| 2 | NB-2 -- K_max=12 vs decisione stratificazione Cap.25.5 incompatibile sotto Harrell | BUG REALE | SI -- Developer (obbligatorio) | SI |
| 3 | NB-3 -- Nomenclatura MAE alla scadenza incoerente con regola operativa (Cap.24.1) | BUG REALE | SI -- Developer (obbligatorio) | SI |
| 4 | RP-1 -- Tensione F=8 vs T_budget=60 ore (Cap.26.2/26.5) | RISCHIO PEGGIORAMENTO | In attesa decisione supervisore | DECIDE SUPERVISORE |
| 5 | RP-2 -- Aggregazione f_5^global concatenazione cross-fold (Cap.24.6) | RISCHIO PEGGIORAMENTO | In attesa decisione supervisore | DECIDE SUPERVISORE |
| 6 | RP-3 -- Soglia theta_CV=0,5 senza fonte (Cap.25.5) | RISCHIO PEGGIORAMENTO | In attesa decisione supervisore | DECIDE SUPERVISORE |
| 7 | O-1 -- Errore conteggio voci tabella Cap.26.5 nel REPORT (55 vs 60) | NEUTRO | NO -- ignorato | NO |
| 8 | O-2 -- Ambiguita vincolo 2 Cap.22.7 (cromosoma vs segnale derivato) | NEUTRO | NO -- ignorato | NO |
| 9 | O-3 -- Normalizzata ad esempio in Cap.23.4 | NEUTRO | NO -- ignorato | NO |
| 10 | O-4 -- Eredita 16 e 41 cross-ref implicito | NEUTRO | NO -- ignorato | NO |
| 11 | O-5 -- Floor max(..., 1) in f_5 non motivato esplicitamente | NEUTRO | NO -- ignorato | NO |

**Riepilogo classificazione**:
- BUG REALI: 3 (NB-1, NB-2, NB-3) -- a Developer obbligatorio.
- RISCHIO PEGGIORAMENTO: 3 (RP-1, RP-2, RP-3) -- decide supervisore.
- NEUTRO: 5 (O-1 ... O-5) -- ignorati di default.
- MIGLIORA PERFORMANCE: 0.

---

## Verdetto finale

**CONDITIONAL**

Il documento Parte V e strutturalmente solido e operativamente funzionante: il GA puo essere implementato sulla base di Cap.22-26 senza ambiguita sull algoritmo, sul cromosoma, sulle penalita, sul walk-forward e sui protocolli di rollback. Tutti i 5 capitoli sono presenti, tutte le citazioni obbligatorie sono inline, le 5 sezioni del REPORT sono complete. Il fronte di Pareto F_1 prodotto dal motore cosi specificato e interpretabile in Parte VII.

I 3 BUG REALI sono riparabili in mini-patch senza rework completo della Parte V:

- NB-1 (Cap.23.6): riallineare le unita della derivazione M-4 - una riga di calcolo da correggere.
- NB-2 (Cap.25.5 + Cap.26.7): scegliere fra le opzioni (a) K_max = 6 congelato; (b) decisione di Parte V cambiata a interaction term; (c) ammorbidimento esplicito della rule of thumb con citazione. Costo: ~10 righe di testo.
- NB-3 (Cap.24.1): sostituire MAE alla scadenza con rendimento di chiusura virtuale forzata - una sostituzione di etichetta.

Nessuno dei 3 BUG REALI invalida l architettura. NB-1 non impatta il comportamento del GA (impatta solo l AC-23-5 e la coerenza inter-capitolo con CAP-01). NB-2 impatta il ranking del fronte di Pareto via stima Cox biased, ma il rollback automatico Cap.25.5 alla opzione (a) interaction term sotto CV > 0,5 mitiga il problema in pratica. NB-3 impatta solo la nomenclatura, non il calcolo di R_net.

I 3 RISCHIO PEGGIORAMENTO sono scelte di design che il supervisore puo approvare/respingere senza che il documento sia tecnicamente errato. RP-1 e una tensione esplicitamente dichiarata dal documento; RP-2 e una scelta motivata ma con costo metrico; RP-3 e una soglia provvisoria riconosciuta come tale.

Non si richiede splitting Parte V.A + Parte V.B (proposta di rollback del Developer). Iterazione v2 mirata sui 3 BUG REALI + eventuali RP-X approvati dal supervisore e il percorso atteso.
