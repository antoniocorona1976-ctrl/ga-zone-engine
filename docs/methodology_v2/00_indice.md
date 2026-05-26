# Indice — Motore genetico strutturale per segnali FIB (documento metodologico v2)

Documento specializzato per FIB N=1, derivato da ENGINE_ALGO_INTEGRATO_HARD_LOCKED con rimozione dei layer multi-indice (DCC/ADCC/BEKK, covarianza cross-index, N>=8) e dei layer di execution ordini. Lunghezza target ~55-65 pagine + appendici.

---

## Parte I — Ambito operativo e vincoli operatore (~7 pp) ✅ PASS Review v4 (con patch Iterazione 2 in commit fc7531b, Iterazione 3 in commit FIX-04)

- **Cap 1 — Obiettivo operativo** (~1.5 pp): definizione dello strumento (FIB su FTSE MIB, mercato IDEM), sessione operativa, target quantitativo (500 punti/giorno o 70% escursione intraday), vincolo "solo emissione, nessuna esecuzione".
- **Cap 2 — Profilo operatore e vincoli operativi** (~1.5 pp): operatore retail non professionale MiFID II, operativita' mobile, 1 contratto alla volta, commissioni 5 euro/op, separazione segnale/gestione posizione, rollover.
- **Cap 3 — Infrastruttura disponibile** (~1.5 pp): PC i5-7200U/8GB, ambiente Anaconda, broker Directa, storico Portara/CQG, canale Telegram. Lacune da colmare (API Directa, fornitura storico) rinviate alle Appendici C-D.
- **Cap 4 — Compute budget e strategia cloud** (~1.5 pp): valutazione adeguatezza PC per ogni fase, stima training GA non fattibile in locale, strategia AWS spot c5.4xlarge per il training, costi e frequenza di retraining.
- **Cap 5 — Definizione operativa del successo** (~1 pp): metrica primaria expected net return per segnale, metriche di lifecycle (executable/target-hit/invalidation), metriche di rischio (CVaR, drawdown), metriche anti-overfitting (DSR, PBO), filtro emissione minimo 80 punti.

## Parte II — Contratto del segnale FIB (~11-12 pp) ✅ PASS (Review v4 storica + Iterazione 4 e 5 mini-patch approvati da Review v3 CAP-04 commit `a1625df` del 2026-05-25: Cap.6.1 esteso con `target_2_type` e `stop_type`; Cap.6.1 e Cap.8.2 sincronizzati 80pt con Cap.5 PI; Cap.9.2 esteso a 9 voci pubblicate sul messaggio Telegram; dominio `stop_type` raffinato a `{structural, synthetic}` per D-v2-7)

- **Cap 6 — Schema del segnale e invarianti** (~2 pp): payload del segnale (direzione, banda discreta sul tick FIB, target_1 e target_2 strutturali — target_2 come informazione strutturale pubblicata, non variabile di lifecycle —, stop strutturale, timestamp_emission, expiry post-trigger, setup_class), invariante di payload immutabile, regola di sostituzione con segnale unico attivo.
- **Cap 7 — Stati del segnale e state machine** (~2 pp): 1 non-terminale (`active`) + 6 terminali (`target_1_hit`, `stopped`, `invalidated`, `missed_target`, `expired`, `revoked`); `trigger_event` come evento, raw touch sempre eseguibile; timer pre-trigger $T_{touch}^{max}$ e timer post-trigger $\Delta t_{cromosoma}$ con esempi numerici; edge case raw touch.
- **Cap 8 — Condizioni di emissione del segnale** (~2 pp): 3 condizioni pre-emissione (volatilità EGARCH, liquidità volume, distanza target_1 in sigma-units $\tau_{dist}^{\sigma}$), spread eliminata. Filtri post-emissione esclusi: una volta emesso, il raw touch è sempre eseguibile.
- **Cap 9 — Politica di pubblicazione su Telegram** (~2 pp): formato messaggio, latenza ammissibile, gestione anti-duplicato, nuovo messaggio per nuovo signal_id, notifica `trigger_event` separata.
- **Cap 10 — Replay e riproducibilità del lifecycle** (~2 pp): formato dei log (emissione, transizioni, chiusura), determinismo bit-exact dichiarato come vincolo formale.
- **Cap 11 — Position lifecycle e tracking out-of-scope dal motore** (~1-2 pp) [NUOVO, decisione Q-05]: submacchina distinta dal lifecycle del segnale, traccia eventi post-target_1 ($\pi_{t_2 \mid t_1}$, MFE, MAE, stop post-target_1) per reporting GA; OUT-OF-SCOPE execution policy, IN-SCOPE solo metriche di calibrazione; citazioni testuali baseline hard-locked Cap. 21.1 e 22.6.

## Parte III — Layer quantitativo single-instrument (~8 pp) ✅ PASS Review v4 (documento commit ee0b2ee, review v4 PASS)

- **Cap 12 — Definizioni di rendimento e scala temporale** (~1.5 pp): rendimenti log 1-min, aggregazione a barre superiori, gestione gap di sessione, regola deterministica di fill virtuale worst-case per il backtest (carryover N-6 CAP-02).
- **Cap 13 — Modello di volatilita' condizionata** (~2.5 pp): EGARCH(1,1) single-instrument con equazioni media e varianza, distribuzione Student-t/GED con selezione AIC/BIC in Parte V, calibrazione MLE su finestra rolling W=210.000 fold-per-fold (divergenza dichiarata dal baseline), conversione $\hat{\sigma}_{\text{pt}}(t) = \hat{\sigma}(t) \cdot p_t$, diagnostica residui (Ljung-Box, ARCH-LM), inizializzazione cross-session (Opzione A/B aperta), osservazione coda bassa N-5.
- **Cap 14 — Stato di regime intraday** (~2 pp): classificazione binaria calmo/turbolento deterministica su quantili rolling di $\bar{\sigma}_s$ (media di sessione, N_s=840), quantile $p=0{,}75$ su $N_{reg}=20$ sessioni, persistenza minima $T_{persist}=10$ barre, regime non ottimizzabile dal GA, impatto su condizionalita' soglie e fold walk-forward.
- **Cap 15 — Feature engineering causale** (~2 pp): vincolo causalita' $x_t \in \mathcal{F}_{t-1}$, catalogo 37 feature (prezzo, volume, volatilita', struttura), algoritmo pivot detection frattale 4 condizioni con $n_c=3$/$\delta_{pivot}=10$pt, EMA con reset cross-session e $T_{warmup,\text{EMA}}=74$, normalizzazione z-score MAD con $W_{norm}=1000$ e $T_{warmup,\text{norm}}=100$ per feature con reset.

## Parte IV — Geometria zone, target strutturali, survival (~12 pp) ✅ PASS Review v3 (review commit `a1625df` del 2026-05-25; documento commit `9852e12` + `687e042`; 15/15 AC v3 OK; 0 regressioni; 3 AC v2 promossi a OK; ciclo Review v1→v2→v3 con chiusura completa di 8 finding v1 + 9 finding v2 — 3 BUG REALI v2 chiusi, D-v2-7 stop_type `{structural, synthetic}` ratificata dall'Orchestratore, 5 NEUTRO opportunistici chiusi)

- **Cap 16 — Definizione delle zone di entry** (~2.5 pp): costruzione geometrica della zona long e short, ancoraggio a pivot strutturali, trattamento warm-up sessione, invalidazione strutturale pre-touch, condizione tempo residuo.
- **Cap 17 — Target strutturali** (~2 pp): derivazione di target_1 e target_2 dalla struttura dei pivot, vincolo minimo 80 punti per directional, condizione distanza sigma-units.
- **Cap 18 — Stop strutturali** (~2 pp): derivazione dello stop dalla struttura, vincolo $d_{stop} > b$, separazione dallo stop personale dell'operatore, condizionalita' al regime.
- **Cap 19 — Modello di survival per il target** (~2.5 pp): competing risks target_1_hit vs stopped, formulazione matematica del modello candidato, feature input dal catalogo CAP-03, calibrazione fold-per-fold, censoring, output $\hat{p}_{hit}$.
- **Cap 20 — Filtri di emissione basati sul survival** (~1.5 pp): soglia $\tau_{surv}$ parametro del cromosoma, integrazione AND con condizioni Cap.8, condizionalita' al regime, filtro implicito fine sessione.
- **Cap 21 — Caso trade range** (~1.5 pp): definizione range da pivot, eccezione al filtro 80pt ($A_{range} \geq 80$), geometria zone/target/stop nel range, classificazione directional vs trade_range.

## Parte V — Motore genetico e fitness operativa (~10 pp) 🟡 IN REVIEW v3 (riapertura 2026-05-26 dal supervisore via `DEV_STATUS=READY_FOR_REVIEW`; audit indipendente Review v3 in `reviews/REVIEW_CAP_05_v3_review.md` verdetto **CONDITIONAL** con 2 BUG REALI: NB-v3-1 NB-2 chiuso solo formalmente — censoring incoerente Cap.25.5/Cap.26.7 + aritmetica errata + Harrell violato sotto $K_{max}=6$ con caso pessimo strato 44; NB-v3-2 RP-1 chiuso solo formalmente — $T_{budget}=80$h motivato su calcolo Cap.23.6 ORMAI OBSOLETO 72h pre-fix M-4, calcolo aggiornato è 107h. Rework v3 in `tasks/ACTIVE_TASK.md`. Stato pre-riapertura — PASS Review v2 commit `50b6e7e` — invalidato a livello formale; il documento al commit `16590ae` resta baseline per il rework chirurgico v3.)

- **Cap 22 — Cromosoma e spazio dei parametri** (~2 pp): genoma del bundle (parametri zone, target, stop, soglie filtro, parametri survival), vincoli di ammissibilita'.
- **Cap 23 — Operatori GA** (~2 pp): selezione NSGA-II, crossover, mutazione, elitismo.
- **Cap 24 — Funzione di fitness multi-obiettivo** (~2 pp): obiettivi (expected net return, target hit rate, invalidation rate, drawdown), penalita' per emissione eccessiva o nulla.
- **Cap 25 — Walk-forward nested con purge ed embargo** (~2 pp): schema temporale dei fold, prevenzione del leakage, purge ed embargo tra in-sample e out-of-sample.
- **Cap 26 — Calibrazione dimensione popolazione, generazioni, criteri di stop** (~2 pp): popolazione 128, generazioni fino a 150, criteri di convergenza, gestione del seed.

## Parte VI — Emissione segnali e lifecycle senza execution (~6 pp) 🟡 IN REVIEW Review v2 (documento v1 commit `8875f1c` FAIL su 3 BUG REALI + 8 NEUTRO; rework v2 risolve tutti gli 11 finding approvati dal supervisore; 38 AC v1 + sub-AC v2 nuovi su $f_5^{live}$ e tie-break; ciclo Review v2 in corso)

- **Cap 27 — Pipeline di inference real-time** (~1.5 pp): ingest del feed Directa, calcolo feature, valutazione del bundle frozen, emissione del segnale.
- **Cap 28 — Politica anti-doppio-segnale** (~1.5 pp): gestione di segnali concorrenti sulla stessa direzione, no-refresh del segnale emesso.
- **Cap 29 — Gestione dell'operativita' su mobile** (~1.5 pp): formato del messaggio Telegram leggibile in mobilita', informazioni minime necessarie all'operatore.
- **Cap 30 — Monitoraggio del lifecycle in produzione** (~1.5 pp): metriche di lifecycle calcolate live, dashboard di sintesi, alert su deriva.

## Parte VII — Validazione OOS, frozen bundle, gate decisionali (~8 pp)

- **Cap 31 — Procedura di validazione OOS** (~1.5 pp): finestre OOS, scelta del bundle candidato, regole di selezione.
- **Cap 32 — Deflated Sharpe Ratio (DSR)** (~1.5 pp): definizione, stima, uso come gate primario di selezione.
- **Cap 33 — Probability of Backtest Overfitting (PBO) via CSCV** (~1.5 pp): definizione, stima, soglia di accettazione.
- **Cap 34 — Bootstrap stazionario** (~1.5 pp): parametri (B=2000, block length), uso per intervalli di confidenza su DSR e metriche di lifecycle.
- **Cap 35 — Frozen bundle e immutabilita'** (~1 pp): processo di freezing, hash di riferimento, regola di sostituzione.
- **Cap 36 — Gate decisionali per il go-live** (~1 pp): checklist DSR positivo, PBO sotto soglia, lifecycle stabile su regime calmo e turbolento.

## Appendici operative (~6 pp)

- **Appendice A — Specifiche PC e ambiente Python**: dettagli i5-7200U, Anaconda base, requirements, repository del codice.
- **Appendice B — Setup Claude Code e GitHub**: workflow dei 3 agenti, struttura repo, branch policy, formato commit.
- **Appendice C — API Directa**: qualificazione tra Darwin, DAPI e Visual Trader, requisiti di dato real-time del modello.
- **Appendice D — Storico Portara/CQG**: specifica del feed (FIB continuo 1-min, 5 anni minimo), valutazione costo e formato.
- **Appendice E — Telegram bot personale**: setup del bot, gestione chat ID, schema messaggio.
- **Appendice F — I 3 agenti Planner / Development / Review**: ruoli, ingressi, output, regole di handoff.
- **Appendice G — Glossario**: termini ricorrenti (zone, target strutturale, lifecycle, DSR, PBO, bundle frozen).
