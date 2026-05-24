### REPORT SUPERVISORE — CAP-03
**Task**: Parte III del documento metodologico v2 — Layer quantitativo single-instrument
**Stato**: COMPLETATO — rework v4 dopo Review v1 CONDITIONAL + decisioni supervisore Q-06..Q-09

#### Cosa e stato prodotto
- `docs/methodology_v2/CAP_03_parte_III.md` v4 — Parte III, 4 capitoli (Cap.12-15). Modifiche chirurgiche rispetto alla v1: correzione NB-1/NB-2/NB-3/C-5.1 (BUG REALI) + NB-4/NB-5/NB-6/NB-7 (MIGLIORA PERFORMANCE approvati).
- `docs/methodology_v2/CAP_02_parte_II.md` — mini-patch Cap.8.2: cross-ref Cap.12 -> Cap.13, sigma_hat -> sigma_hat_pt nelle formule delle condizioni di emissione.
- `tasks/QUESTIONS.md` — M-5 e M-6 aggiunti come carryover per Parte V.
- `reports/REPORT_CAP_02.md` — sezione Iterazione 4 aggiunta (mini-patch Cap.8.2).

#### Ipotesi di partenza
La Parte III v1 aveva 3 BUG REALI strutturali: (1) look-ahead off-by-one nella pivot detection (NB-1) che produce ranking distorto dei cromosomi su feature di struttura; (2) formula E[|z|] GED errata (NB-2) che distorce sigma_hat se il GA seleziona GED; (3) unita di sigma_hat non riconciliate con Cap.8 Parte II (NB-3) che rende la condizione di emissione non implementabile univocamente. I 4 MIGLIORA PERFORMANCE approvati chiudono gradi di liberta impliciti che avrebbero prodotto implementazioni divergenti del motore.

#### Decisioni rilevanti prese durante lo sviluppo

D-1. NB-3: la conversione sigma_hat_pt = sigma_hat * p_t e introdotta in Cap.13.1 con nota disambiguante che chiarisce la notazione nei capitoli successivi. La formula non altera la ricorsione EGARCH (sigma_hat in log-return e invariato); e solo la sua proiezione in punti FIB per le condizioni di Cap.8.

D-2. NB-2: la formula corretta per GED include il fattore di scala c = [Gamma(1/kappa)/(2^{2/kappa} Gamma(3/kappa))]^{1/2}. I casi limite kappa=2 e kappa=1 sono verificati numericamente nel testo del documento.

D-3. Q-06/C-4.2: la cadenza di ricalibrazione e cambiata da "a ogni sessione" a "fold-per-fold del walk-forward". Questa e la scelta piu conservativa in termini di frequenza di stima MLE e la piu coerente metodologicamente con il walk-forward OOS.

D-4. Q-07/C-5.2: il reset EMA a 8:00 CET con T_warmup = 74 barre elimina il problema di cross-session senza richiedere modifiche architetturali. Le 74 barre unusable (74 minuti) sono compatibili con la sessione di 840 minuti: perdita < 9% delle barre utili per sessione.

D-5. Q-08: le 4 condizioni formali per pivot detection includono la condizione 4 (finestra nella sessione corrente), coerente con il reset EMA di C-5.2. Le due decisioni (C-5.2 e Q-08) si rinforzan a vicenda: nessun pivot puo attraversare il bordo di sessione.


#### Misura prima/dopo (v1 -> v4)

| Metrica | Prima (v1) | Dopo (v4) | Delta |
|---------|-----------|----------|-------|
| Look-ahead pivot detection | Pivot disponibile a t+n_c (off-by-one) | Pivot disponibile a t+n_c+1 (causalmente corretto) | -1 barra look-ahead sistematico |
| Formula E[abs(z)] GED, kappa=1 | 2.0 (errata) | 0.7071 (corretta) | Distorsione sigma_hat eliminata |
| Unita sigma_hat vs punti FIB | Rapporto non adimensionale in Cap.8 | sigma_hat_pt = sigma_hat * p_t; rapporto adimensionale | Ambiguita implementativa eliminata |
| Formula EMA | Somma da j=1 a infty con fattore lambda in piu | Somma da j=0 a n_t-1 (corretta) | Bug matematico chiuso |
| Dichiarazione divergenza rolling vs expanding | Assente | Esplicita con Pesaran-Timmermann (2007) | Tracciabilita metodologica con baseline |
| Cadenza ricalibrazione EGARCH | A ogni sessione (giornaliera) | Fold-per-fold del walk-forward | Coerenza con Cap.14.3 del baseline |
| Reset EMA cross-session | Assente (somma infinita cross-sessione) | Reset a 8:00 CET; T_warmup=74 barre unusable | Determinismo garantito; Engle-Sokalska (2012) |
| Condizioni pivot detection | 2 disequazioni (frattale senza retracement formale) | 4 condizioni esplicite con simmetria e condizione sessione | 0 gradi di liberta impliciti |
| Statistica sessione sigma_hat | Nessun valore provvisorio | sigma_bar_s = media su N_s=840 + mediana come benchmark | Default normativo chiuso; Corsi (2009) |

#### Verifica AC v4 (14 nuovi)

| AC | Criterio | Esito |
|----|----------|-------|
| AC-v4-1 | NB-1: "feature disponibile a t+n_c+1" nel testo | OK — Cap.15.3 |
| AC-v4-2 | NB-2: formula E[abs(z)] GED con fattore c; verifiche kappa=2 e kappa=1 | OK — Cap.13.2 |
| AC-v4-3 | NB-3: sigma_hat_pt in Cap.13.1; Cap.8.2 Parte II aggiornato | OK — Cap.13.1 + Cap.8.2 |
| AC-v4-4 | C-5.1: EMA con j da 0 a n_t-1 | OK — Cap.15.2.1 |
| AC-v4-5 | Q-06/C-4.1: divergenza + Pesaran-Timmermann (2007) inline | OK — Cap.13.3 |
| AC-v4-6 | Q-06/C-4.2: cadenza fold-per-fold | OK — Cap.13.3 |
| AC-v4-7 | Q-07/C-5.2: reset EMA; T_warmup=74; Engle-Sokalska (2012) inline | OK — Cap.15.2.1 |
| AC-v4-8 | Q-08: 4 condizioni; simmetria; condizione sessione | OK — Cap.15.3 |
| AC-v4-9 | Q-09: sigma_bar_s; mediana; Corsi (2009) inline | OK — Cap.14.2 |
| AC-v4-10 | M-5 e M-6 in REPORT_CAP_03 e QUESTIONS.md | OK — QUESTIONS.md (M-5, M-6 aggiunti) |
| AC-v4-11 | REPORT_CAP_03.md con sezione Iterazione 4 | OK — questo file |
| AC-v4-12 | REPORT_CAP_02.md con sezione Iterazione 4 | OK — REPORT_CAP_02.md |
| AC-v4-13 | 29 AC originali restano soddisfatti | OK — nessuna rimozione di contenuto |
| AC-v4-14 | Niente bibliografia aggiunta; citazioni inline nei capitoli | OK — Cap.13.3, Cap.14.2, Cap.15.2.1 |

#### Verifica AC originali (29) — sintesi post-v4

Tutti 29 AC originali confermati. Le modifiche v4 non hanno rimosso contenuto preesistente; hanno aggiunto o sostituito in modo chirurgico. I 3 AC condizionali al momento della Review v1 (AC #21 pivot detection, AC #26 determinismo EMA, AC #11 output sigma_hat) sono ora pienamente soddisfatti.

#### Domande aperte per il Planner
Nessuna. M-5 e M-6 sono carryover esplicitamente registrati in QUESTIONS.md per Parte V.

#### Criterio di rollback
1. Se sigma_hat_pt = sigma_hat * p_t produce instabilita in sessioni con prezzi FIB anomalmente bassi (verificabile sullo storico), sostituire p_t con p_bar (prezzo medio della finestra di calibrazione). Revisione puntuale su Cap.13.1.
2. Se il benchmark M-5 (Inoue-Rossi 2011) mostra che expanding domina rolling su tutte e tre le metriche OOS, la finestra rolling W=210.000 va scartata. Criterio di rollback automatico in QUESTIONS.md M-5.
3. Se la citazione Engle-Sokalska (2012) viene contestata come non pertinente (equity US vs futures su indice italiano), sostituire con Engle-Gallo (2006) per MEM con sessione netta. Revisione puntuale su Cap.15.2.1.

---

## Iterazione 4 — risposta ai finding di Review v1 + decisioni supervisore Q-06..Q-09

**Origine**: Review v1 CAP-03 (commit 916f3d4) CONDITIONAL. Supervisore 2026-05-24: tutti 4 MIGLIORA PERFORMANCE approvati; C-5.1 riclassificato BUG REALE.

### Risposta per finding

| Finding | Azione | Posizione |
|---------|--------|-----------|
| NB-1 | Testo: "pivot disponibile come feature a t+n_c+1, non t+n_c". Esempio numerico aggiornato con "t+4 = t+n_c+1". | Cap.15.3, paragrafo "Disponibilita temporale come feature" |
| NB-2 | Formula GED sostituita con versione corretta includente fattore c. Verifiche numeriche kappa=2 e kappa=1 nel testo. | Cap.13.2, bullet GED |
| NB-3 | Introdotta sigma_hat_pt = sigma_hat * p_t in Cap.13.1. Mini-patch Cap.8.2 Parte II: 3 occorrenze aggiornate (formula condizione volatilita, formula condizione distanza, riga finale Cap.8.3). | Cap.13.1 + Cap.8.2 Parte II |
| C-5.1 | Formula EMA corretta: somma da j=0 a n_t-1. Somma pesi (1-lambda^n_t) dichiarata esplicitamente. | Cap.15.2.1 |
| NB-4/Q-06/C-4.1 | Dichiarazione divergenza esplicita. Giustificazione: (i) T_roll=1500 = 1.8 gg insufficienti; (ii) Pesaran-Timmermann (2007) inline. | Cap.13.3, paragrafo divergenza |
| NB-4/Q-06/C-4.2 | Cadenza cambiata a "fold-per-fold del walk-forward". Coerenza con Cap.14.3 baseline dichiarata. | Cap.13.3, paragrafo cadenza |
| NB-5/Q-07/C-5.2 | Reset EMA a 8:00 CET. T_warmup >= ln(0.01)/ln(lambda) = 74 barre per lambda=0.94. Prime 74 barre unusable. Engle-Sokalska (2012) inline. | Cap.15.2.1, paragrafo reset |
| NB-6/Q-08 | 4 condizioni esplicite (2 frattale + retracement + sessione). Simmetrica per pivot low. n_c=3 confermato provvisorio. | Cap.15.3, paragrafo quattro condizioni |
| NB-7/Q-09/C-7.1+C-7.2 | Baseline: sigma_bar_s = (1/840) * sum sigma_s,t. Benchmark: med_t(sigma_s,t). Corsi (2009) inline. | Cap.14.2, paragrafo statistica sessione |

### Misura prima/dopo dell'Iterazione 4

| Metrica GA | v1 | v4 | Delta |
|------------|----|----|-------|
| Look-ahead feature pivot | 1 barra (sistematico) | 0 | -1 barra |
| Distorsione sigma_hat GED kappa=1 | ~283% rispetto al valore corretto | 0% | Eliminata |
| Ambiguita unita sigma vs punti FIB | Alta (implementazioni divergenti) | Nulla (conversione esplicita) | Ranking deterministico |
| Bug formula EMA | Presente (j da 1 non 0) | Assente | Fix matematico |
| Grado di liberta window selection | Implicito (rolling non dichiarato) | Esplicito con divergenza e M-5 | Tracciabilita completa |
| Contaminazione EMA cross-session | Presente (somma infinita) | Assente (reset + 74 barre unusable) | Determinismo garantito |
| Condizioni pivot detection | 2 implicite | 4 esplicite con simmetria | 0 gradi di liberta impliciti |
| Default statistica sessione regime | Assente | sigma_bar_s con N_s=840 | Default normativo chiuso |

---

## Iterazione 5 — chiusura B-1 + NB-1/NB-2 di Review v2

**Origine**: Review v2 CAP-03 (commit `6d959c6`) ha emesso verdetto CONDITIONAL con 1 BUG REALE + 2 MIGLIORA PERFORMANCE + 2 NEUTRO + 2 PROMEMORIA. Decisione supervisore 2026-05-24: B-1 obbligatorio + NB-1 v2 e NB-2 v2 approvati per Developer. NEUTRO (N-1, N-2) e PROMEMORIA (M-1, M-2) dichiarati carryover.

### Risposta per finding

**B-1 v2 — Regressione look-ahead nel fix EMA (Cap.15.2.1)**

La formula v4 $(1-\lambda)\sum_{j=0}^{n_t-1}\lambda^j r_{t-j}$ usava a $j=0$ il termine $r_t$, che richiede $p_t$ (close della barra corrente) — quindi $r_t \in \mathcal{F}_t$, non $\mathcal{F}_{t-1}$. Look-ahead sistematico di 1 barra.

Fix: sostituito $r_{t-j}$ con $r_{t-1-j}$. La formula diventa:
$$x_t^{(\text{ema},\lambda)} = (1-\lambda) \sum_{j=0}^{n_t - 1} \lambda^j \, r_{t-1-j}$$

Il termine piu recente usato e ora $r_{t-1}$ (a $j=0$), che e in $\mathcal{F}_{t-1}$: causale per costruzione. I pesi $(1-\lambda^{n_t})$ sono invariati. La frase esplicativa e stata aggiornata per affermare correttamente che $r_{t-1} \in \mathcal{F}_{t-1}$ e che $r_t \notin \mathcal{F}_{t-1}$.

Verifica coerenza warm-up $T_{warmup,\text{EMA}} = 74$ barre: la sostituzione non cambia la logica del warm-up. Con il reset cross-session, $n_t = 1$ alla prima barra della sessione ($t=1$) usa $r_0$ (gap overnight), ma tutte le prime 74 barre sono marcate `unusable` ed escluse dal training — il $T_{warmup} = 74$ rimane il valore corretto e invariato.

**NB-1 v2 — Denominatore feature distanza pivot in unita sbagliate (Cap.15.2.4)**

La formula v4 $(p_{t-1} - \hat{p}_{pivot}) / \hat{\sigma}_{t-1}$ aveva numeratore in punti FIB e denominatore in log-return (ordine $10^{-4}$): rapporto di ordine $10^5$, non adimensionale.

Fix: sostituito $\hat{\sigma}_{t-1}$ con $\hat{\sigma}_{\text{pt}, t-1} = \hat{\sigma}_{t-1} \cdot p_{t-1}$ (gia definita in Cap.13.1, introdotta in v4 con NB-3). La feature e ora pienamente in sigma-units FIB: numeratore in punti, denominatore in punti, rapporto adimensionale. Aggiunto nel testo il chiarimento esplicito della coerenza dimensionale.

**NB-2 v2 — Residuo formula condizione volatilita Cap.10.2 (CAP-02)**

La mini-patch v4 aveva aggiornato Cap.8.2 (formula display condizione volatilita, poi corretta anche da FIX-02 v3 commit `0f6087c`). Rimaneva in Cap.10.2 (log di emissione) il riferimento al simbolo non convertito: `$|\texttt{target\_1} - p_{ref}| / \hat{\sigma}$` e `$\tau_{vol}(\hat{\sigma}(t_{emission}))$`.

Fix: in Cap.10.2 CAP-02, sostituiti $\hat{\sigma}$ con $\hat{\sigma}_{\text{pt}}$ sia nel valore del rapporto di distanza sia nella soglia $\tau_{vol}(\hat{\sigma}_{pt})$. Il log ora usa coerentemente il simbolo in punti FIB in tutte le occorrenze rilevanti (Cap.8.2 e Cap.10.2).

### Modifiche applicate

| Finding | File | Posizione | Prima | Dopo |
|---------|------|-----------|-------|------|
| B-1 v2 | CAP_03_parte_III.md | Cap.15.2.1, formula EMA e testo | $r_{t-j}$ con $j=0$ (look-ahead) | $r_{t-1-j}$ con $j=0$; testo: "$r_{t-1} \in \mathcal{F}_{t-1}$, $r_t \notin \mathcal{F}_{t-1}$" |
| NB-1 v2 | CAP_03_parte_III.md | Cap.15.2.4, feature distanza pivot | $\hat{\sigma}_{t-1}$ (log-return) | $\hat{\sigma}_{\text{pt}, t-1}$ (punti FIB) |
| NB-2 v2 | CAP_02_parte_II.md | Cap.10.2, log di emissione | $\hat{\sigma}$ e $\hat{\sigma}(t_{emission})$ nel snapshot | $\hat{\sigma}_{\text{pt}}$ e $\hat{\sigma}_{\text{pt}}(t_{emission})$ nel snapshot |

### Carryover dichiarati

- **N-1 v2** (NEUTRO): ambiguita $Q_p$ calcolato su statistiche di sessione o di barra (Cap.14.2). Carryover Parte V.
- **N-2 v2** (NEUTRO): $\hat{\sigma}_{\text{pt}}$ definito con $p_t$ invece di $p_{t-1}$ — differenza numerica $< 0{,}02\%$ trascurabile. Carryover documentazione interna.
- **M-1 v2** (PROMEMORIA): pivot all'inizio e alla fine della sessione non confermabili per la condizione 4 di Q-08 (finestra $[t-n_c, t+n_c]$ in sessione). E design corretto — effetto atteso della condizione 4. Carryover Parte VI.
- **M-2 v2** (PROMEMORIA): cadenza ricalibrazione EGARCH in production non specificata (C-4.2 e per backtest/walk-forward). Carryover Parte V/VI.

### Misura prima/dopo (v4 -> v5)

| Metrica | Prima (v4) | Dopo (v5) | Delta |
|---------|-----------|----------|-------|
| Look-ahead EMA | 1 barra sistematico ($r_t$ a $j=0$) | 0 (formula usa $r_{t-1}$ come termine piu recente) | -1 barra look-ahead; causalita ripristinata |
| Warm-up $T_{warmup} = 74$ | Coerente | Coerente invariato | Nessuna variazione |
| Unita denominatore feature pivot | Log-return ($10^{-4}$), rapporto $\approx 10^5$ | Punti FIB, rapporto adimensionale (sigma-units) | Incoerenza dimensionale eliminata |
| Coerenza dimensionale log Cap.10.2 | $\hat{\sigma}$ (log-return) nel snapshot | $\hat{\sigma}_{\text{pt}}$ (punti FIB) nel snapshot | Coerenza con Cap.8.2 e Cap.13.1 |

### Verifica AC v5 (7 nuovi)

| AC | Criterio | Esito |
|----|----------|-------|
| AC-v5-1 | B-1 v2 chiuso: EMA usa $r_{t-1-j}$; testo afferma $r_{t-1} \in \mathcal{F}_{t-1}$ | OK — Cap.15.2.1 |
| AC-v5-2 | NB-1 v2 chiuso: Cap.15.2.4 usa $\hat{\sigma}_{\text{pt}, t-1}$ al denominatore | OK — Cap.15.2.4 |
| AC-v5-3 | NB-2 v2 chiuso: CAP-02 Cap.10.2 usa $\hat{\sigma}_{\text{pt}}$ nel snapshot log | OK — Cap.10.2 |
| AC-v5-4 | 14 AC v4 + 29 AC originali restano soddisfatti | OK — nessuna rimozione di contenuto, sostituzioni chirurgiche |
| AC-v5-5 | REPORT_CAP_03.md con sezione "Iterazione 5" | OK — questo file |
| AC-v5-6 | REPORT_CAP_02.md con sezione "Iterazione 5 (v5)" | OK — REPORT_CAP_02.md |
| AC-v5-7 | M-1 e M-2 v2 dichiarati carryover in questo report | OK — sezione "Carryover dichiarati" sopra |

### Verifica AC v4 (14) post-v5 — campione rappresentativo

| AC | Criterio | Esito post-v5 |
|----|----------|---------------|
| AC-v4-1 | NB-1: "feature disponibile a t+n_c+1" nel testo Cap.15.3 | OK — non toccato in v5 |
| AC-v4-4 | C-5.1: EMA con j da 0 a n_t-1 (formula corretta) | OK — struttura conservata, solo indice r cambiato |
| AC-v4-7 | Q-07/C-5.2: reset EMA; T_warmup=74; Engle-Sokalska (2012) | OK — T_warmup=74 confermato coerente con B-1 fix |
| AC-v4-3 | NB-3: sigma_hat_pt in Cap.13.1; Cap.8.2 Parte II aggiornato | OK — Cap.13.1 invariato; Cap.8.2 invariato in v5 (gia corretto) |

### Verifica AC originali (29) — sintesi post-v5

Tutti 29 AC originali confermati. Le 3 modifiche v5 sono chirurgiche su formula e simbolo, senza rimozione di contenuto strutturale. I capitoli Cap.12, Cap.13, Cap.14 sono invariati. Cap.15.2.1 e Cap.15.2.4 modificati per indice e denominatore rispettivamente, mantenendo la struttura e i vincoli di causalita e determinismo.

