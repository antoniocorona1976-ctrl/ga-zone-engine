# QUESTIONS — Development

## Q-01 — Conflitto orari sessione operativa (CAP-01) — CHIUSA

**Decisione del supervisore (2026-05-22, rettificata in pari data)**: il FIB negozia in modo continuo dalle 8:00 alle 22:00 CET. Non esistono fasi separate (asta, regolare, after-hours): la sessione è una finestra unica e continua. Il perimetro operativo del motore coincide con questa finestra 8:00-22:00 CET.

**Stato**: chiusa.

---

## Q-02 — Ancoraggio del movimento strutturale in sessioni senza emissione (CAP-01) — CHIUSA

**Contesto**: la definizione originaria faceva partire l'intervallo di calcolo del movimento strutturale "dal primo segnale post-apertura", lasciando indefinito il target in sessioni senza emissione.

**Decisione del supervisore (2026-05-22)**: l'intervallo parte dal primo minimo o primo massimo della giornata identificato post-apertura della sessione regolare, indipendentemente dall'attività di emissione del motore. Il target del 70% esiste in ogni sessione.

**Stato**: chiusa.

---

## Q-03 — Trattamento dei parametri NSGA-II (128, 150, B=2000) in Parte I (CAP-01) — CHIUSA

**Contesto**: ACTIVE_TASK.md mette out-of-scope di CAP-01 i parametri congelati del GA. Cap.4 li cita per dimensionare il compute budget.

**Decisione del supervisore (2026-05-22)**: i valori 128/150/B=2000 sono parametri di lavoro provvisori utilizzati esclusivamente per il dimensionamento del compute budget; valori definitivi congelati in Parte V con stima da aggiornare di conseguenza. Nota esplicita inserita in Cap.4.

**Stato**: chiusa.

---

## Q-04 — Cap massimo della validità multiday del segnale (CAP-01) — CHIUSA

**Contesto**: punto 3 della dichiarazione di intenti permette estensione multiday senza cap numerico. CLAUDE.md fissa il tetto a "fino a 2 giorni".

**Decisione del supervisore (2026-05-22)**: tetto fissato a 2 giorni di trading dall'emissione del segnale. Il GA può ottimizzare il timing di chiusura come parametro del cromosoma entro questo tetto, ma non oltrepassarlo. Cromosomi con orizzonte temporale > 2 giorni di trading sono dichiarati non validi.

**Nota retroattiva (2026-05-23, Iterazione 2 CAP-01)**: il supervisore ha precisato che il cap 2 giorni di trading decorre dal raw touch (esecuzione) e non dall'emissione. Patch applicata in CAP-01 riga 13 e in metrica `executable_rate` (commit `fc7531b`).

**Stato**: chiusa.

---

## Q-05 — Stati post-target_1 nella state machine del segnale (CAP-02, B-3 Review v2) — CHIUSA

**Contesto**: Review v2 di Parte II ha identificato un'inconsistenza in Cap 7 della state machine del segnale: `target_1_hit` e `target_2_hit` erano entrambi dichiarati terminali, lasciando indefinita la transizione fra i due e ignorando la dinamica post-target_1 (eventuale stop dopo target_1, retracement, revoca). Quattro opzioni strutturali sul tavolo: A (2 non-terminali), C (target_2 come evento), D (separazione segnale vs trade), E (stati composti).

**Decisione del supervisore (2026-05-23)**: **Opzione D raffinata** in tre clausole non separabili.

1. **State machine del segnale (Cap 7) ridotta a 1 non-terminale + 6 terminali**: `target_1_hit`, `stopped`, `invalidated`, `missed_target`, `expired`, `revoked`. `target_2_hit` RIMOSSO. Il contratto del segnale si chiude al raggiungimento del primo target strutturale.
2. **target_2 resta campo obbligatorio del payload (Cap 6)**: il motore pubblica due livelli strutturali come informazione decisionale per l'operatore, ma non gestisce execution oltre target_1. target_2 è "informazione strutturale pubblicata, non variabile di lifecycle del segnale".
3. **Position lifecycle come submacchina distinta (nuovo Cap 11)**: traccia eventi post-target_1 (raggiungimento target_2, stop post-target_1, MFE, MAE, retracement) come oggetto di reporting per la validazione del GA. OUT-OF-SCOPE dal motore: execution policy, scaling-out, trailing stop, dynamic sizing. IN-SCOPE per reporting: produce metriche per i report fold-by-fold del walk-forward. La submacchina NON modifica lo stato del segnale (terminato in `target_1_hit` prima ancora che la submacchina inizi a tracciare). Citare i riferimenti del baseline hard-locked: Cap. 21.1 (lifecycle posizione vs lifecycle contratto di segnale come sottosistemi distinti) e Cap. 22.6 (submacchina della posizione come boundary esplicito).

**Rationale (registrato dal supervisore)**:
- Opzione A viola l'invariante "1 solo stato non-terminale" di CAP-01.
- Opzione C scarta il livello strutturale ma non lo distingue dal payload, perdendo coerenza con l'eredità #4 di CAP-01.
- Opzione E (stati composti) esplode combinatoriamente.
- Opzione D raffinata separa il contratto del segnale (oggetto del motore, ottimizzato dal GA) dal lifecycle della posizione (oggetto del reporting). È l'unica scelta architetturalmente coerente con il baseline hard-locked.

**Impatto sul GA**:
- La fitness del GA continua a ottimizzare la qualità del segnale: probabilità condizionali di trigger, di hit di target_1, calibrazione del payload. Lo space search non viene esteso.
- target_2 entra nella fitness come metrica di qualità dell'informazione strutturale pubblicata (score strutturale del secondo livello), non come variabile decisionale di execution. Nessun ramo di policy nel cromosoma.
- La submacchina position lifecycle produce metriche di calibrazione ($\pi_{t_2 | t_1}$, MFE, MAE) che entrano nei report di Parte IV/V come obiettivi/vincoli del GA, senza introdurre execution decisions nel cromosoma.
- Rispetto alle altre opzioni: search space invariato, minor rischio di overfitting (DSR/PBO più robusti), maggiore parsimonia parametrica.

**Stato**: chiusa. Esecuzione in `ACTIVE_TASK.md` aggiornato per CAP-02 rework v3.

---

## Q-06 — Finestra di stima EGARCH: rolling vs expanding (CAP-03, NB-4 Review v1) — CHIUSA

**Contesto**: Review v1 di CAP-03 ha segnalato che la scelta di rolling $W = 210.000$ barre 1-min divergeva dal baseline hard-locked (expanding) senza dichiarazione esplicita. Il baseline è metodologico generale; la nostra applicazione è single-instrument intraday su FIB e ha requisiti specifici di adattamento ai regimi correnti.

**Decisione del supervisore (2026-05-24)**: **β-rigorosa, tre clausole**.

- **C-4.1**: Adottare rolling $W = 210.000$ in CAP-03 come baseline FIB, con dichiarazione esplicita di divergenza dal baseline hard-locked. La giustificazione testuale deve citare:
  - (i) inapplicabilità letterale di $T_{roll} = 1500$ del baseline perché calibrato per daily, non per 1-min: 1500 barre 1-min sono 1.8 giorni, insufficienti per stimare EGARCH(1,1) Student-$t$;
  - (ii) **Pesaran-Timmermann (2007)** "Selection of estimation window in the presence of breaks" come riferimento teorico che giustifica rolling in presenza di structural breaks parametrici.
- **C-4.2**: Cambiare cadenza di ricalibrazione da "all'apertura di ogni sessione" (giornaliera) a **"fold-per-fold del walk-forward"**, coerente con Cap. 14.3 del baseline.
- **C-4.3**: Aggiungere acceptance criterion per Parte V: benchmark comparativo rolling vs expanding vs EWMA su FIB con test **Inoue-Rossi (2011)**, e criterio di rollback automatico se rolling $W = 210.000$ non domina almeno una alternativa su metrica OOS congelata (log-likelihood OOS, Brier sulla calibrazione $\sigma^2$, MSE).

**M-promemoria per Parte V**: implementare il benchmark del punto C-4.3.

**Stato**: chiusa. Esecuzione in `ACTIVE_TASK.md` aggiornato per CAP-03 rework v4.

---

## Q-07 — EMA dei rendimenti: formula matematica + cross-session (CAP-03, NB-5 Review v1) — CHIUSA

**Contesto**: Review v1 di CAP-03 ha segnalato due problemi distinti sulla feature EMA dei rendimenti in Cap.15.2.1: (i) la formula $(1-\lambda)\sum_{j=1}^{\infty} \lambda^j r_{t-j}$ ha un fattore $\lambda$ in più rispetto alla forma standard EMA; (ii) la somma infinita attraversa il bordo di sessione senza trattamento esplicito del gap overnight.

**Decisione del supervisore (2026-05-24)**: **due fix separati**.

- **C-5.1** (riclassificato come **BUG REALE**, non più MIGLIORA PERFORMANCE): bug formula matematica. La formula corretta è
  $$x_t^{(\text{ema},\lambda)} = (1-\lambda) \sum_{j=0}^{n_t - 1} \lambda^j r_{t-j}$$
  con sommatoria che parte da $j=0$ (non $j=1$). La somma dei pesi durante warm-up è $(1-\lambda^{n_t})$, che non è 1 finché $n_t$ è finito.
- **C-5.2** (MIGLIORA PERFORMANCE): cross-session behavior. **Reset EMA all'apertura di ogni sessione 8:00 CET**. Le prime $T_{warmup,\text{EMA}}$ barre della sessione sono marcate come `unusable` ed escluse dal training del GA. Default operativo provvisorio:
  $$T_{warmup,\text{EMA}} \geq \frac{\ln(0{,}01)}{\ln(\lambda)}$$
  così che il peso di osservazioni pre-warmup sia $< 1\%$. Per $\lambda = 0{,}94$ questo dà $T_{warmup,\text{EMA}} \geq 74$ barre = 74 minuti. Congelato in Parte V.

**Citazione testuale obbligatoria** nel Cap.15.2.1 e nel rationale: **Engle-Sokalska (2012)** "Forecasting intraday volatility in the US equity market", *Journal of Financial Econometrics*, come riferimento metodologico per reset cross-session in equity con sessione netta.

**Stato**: chiusa. Esecuzione in `ACTIVE_TASK.md` aggiornato per CAP-03 rework v4.

---

## Q-08 — Soglia retracement nella pivot detection (CAP-03, NB-6 Review v1) — CHIUSA

**Contesto**: Review v1 di CAP-03 ha segnalato che in Cap.15.3 la soglia di retracement $\delta_{pivot}$ era formulata in modo ambiguo: non specificava su quale barra si valutasse il retracement né su quale grandezza di prezzo (high, low, close), e mancava una disequazione esplicita.

**Decisione del supervisore (2026-05-24)**: **formalizzazione esplicita opzione (a) con condizione di sessione**.

Pivot high a $t$ confermato a $t + n_c$ se e solo se valgono tutte e quattro le condizioni:

1. $\text{high}_t > \text{high}_{t-i}$ per ogni $i \in [1, n_c]$
2. $\text{high}_t > \text{high}_{t+j}$ per ogni $j \in [1, n_c]$
3. $\min(\text{low}_{t+1}, \ldots, \text{low}_{t+n_c}) \leq \text{high}_t - \delta_{pivot}$
4. La finestra temporale $[t - n_c, t + n_c]$ rientra interamente nella sessione operativa 8:00-22:00 corrente (coerenza con C-5.2: reset cross-session).

Simmetrica per pivot low.

**Verificare** che $n_c$ sia specificato in CAP-03 o in capitoli precedenti. Se non specificato, aggiungere il valore provvisorio in Cap. 15.3 con rinvio a Parte V. (Nota Orchestratore: in Parte III v1 il valore $n_c = 3$ era già dichiarato in Cap.15.3, da preservare nella v4 con conferma "provvisorio congelato in Parte V".)

**Stato**: chiusa. Esecuzione in `ACTIVE_TASK.md` aggiornato per CAP-03 rework v4.

---

## Q-09 — Statistica di sessione di $\hat{\sigma}$ per la classificazione di regime (CAP-03, NB-7 Review v1) — CHIUSA

**Contesto**: Review v1 di CAP-03 ha segnalato che in Cap.14.2 la scelta fra "ultima barra della sessione" o "media di un sottocampione di barre" come $\hat{\sigma}_{s,\bar{t}}$ per la classificazione del regime non aveva un valore provvisorio di default.

**Decisione del supervisore (2026-05-24)**: **media come default normativo + mediana come benchmark di robustezza**.

- **C-7.1**: Baseline operativo
  $$\bar{\sigma}_s = \frac{1}{N_s} \sum_{t \in s} \hat{\sigma}_{s,t} \quad \text{con } N_s = 840$$
- **C-7.2**: Benchmark di robustezza riportato nei report di sessione: $\text{med}_t(\hat{\sigma}_{s,t})$ (mediana delle stime sulla sessione).
- **C-7.3**: Acceptance criterion per Parte V: se in validation OOS la classificazione di regime cambia significativamente fra media e mediana (soglia da definire in Parte V), va investigato come segnale di sessioni con picchi anomali.

**Citazione testuale obbligatoria** nel Cap.14.2 e nel rationale: **Corsi (2009)** "A Simple Approximate Long-Memory Model of Realized Volatility", *Journal of Financial Econometrics*, come riferimento per uso di medie come statistica di aggregazione di sessione.

**M-promemoria per Parte V**: implementare la classificazione di regime in parallelo con media e mediana, e il test di stabilità del punto C-7.3.

**Stato**: chiusa. Esecuzione in `ACTIVE_TASK.md` aggiornato per CAP-03 rework v4.

---

## M-5 — Benchmark window EGARCH per Parte V (da Q-06 / C-4.3) — CARRYOVER

**Origine**: Q-06 / C-4.3 (decisione supervisore 2026-05-24, rework v4 CAP-03).

**Contenuto**: in Parte V, implementare il benchmark comparativo rolling vs expanding vs EWMA del modello EGARCH su dati FIB 1-min OOS, con test Inoue-Rossi (2011) "Out-of-sample forecast model evaluation and selection", *Review of Economic Studies*. Criterio di rollback automatico: se rolling $W = 210.000$ non domina almeno una alternativa su metrica OOS congelata (log-likelihood OOS, Brier sulla calibrazione $\sigma^2$, MSE), il parametro $W$ va ricalibrato o la finestra rolling scartata a favore della finestra dominante.

**Pertinenza**: Cap. di window selection del walk-forward in Parte V (probabilmente Cap.25 secondo l'indice attuale).

**Stato**: aperto, carryover per Parte V.

---

## M-6 — Classificazione regime media vs mediana per Parte V (da Q-09 / C-7.3) — CARRYOVER

**Origine**: Q-09 / C-7.3 (decisione supervisore 2026-05-24, rework v4 CAP-03).

**Contenuto**: in Parte V, implementare la classificazione di regime in parallelo con media e mediana di $\hat{\sigma}_t$ sulla sessione. Se la classificazione cambia significativamente fra media e mediana su una frazione rilevante di sessioni OOS (soglia da definire in Parte V), va investigato come segnale di sessioni con picchi anomali di volatilità; protocollo di gestione da specificare in Parte V (es. scartare le sessioni anomale dal training, flaggarle nel report).

**Pertinenza**: Cap. di gestione regimi nel walk-forward in Parte V (Cap.25 o Cap.26 secondo l'indice attuale).

**Stato**: aperto, carryover per Parte V.
