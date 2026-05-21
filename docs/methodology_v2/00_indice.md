# Indice — Motore genetico strutturale per segnali FIB (documento metodologico v2)

Documento specializzato per FIB N=1, derivato da ENGINE_ALGO_INTEGRATO_HARD_LOCKED con rimozione dei layer multi-indice (DCC/ADCC/BEKK, covarianza cross-index, N>=8) e dei layer di execution ordini. Lunghezza target ~55-65 pagine + appendici.

---

## Parte I — Ambito operativo e vincoli operatore (~7 pp)

- **Cap 1 — Obiettivo operativo** (~1.5 pp): definizione dello strumento (FIB su FTSE MIB, mercato IDEM), sessione operativa, target quantitativo (500 punti/giorno o 70% escursione intraday), vincolo "solo emissione, nessuna esecuzione".
- **Cap 2 — Profilo operatore e vincoli operativi** (~1.5 pp): operatore retail non professionale MiFID II, operativita' mobile, 1 contratto alla volta, commissioni 5 euro/op, separazione segnale/gestione posizione, rollover.
- **Cap 3 — Infrastruttura disponibile** (~1.5 pp): PC i5-7200U/8GB, ambiente Anaconda, broker Directa, storico Portara/CQG, canale Telegram. Lacune da colmare (API Directa, fornitura storico) rinviate alle Appendici C-D.
- **Cap 4 — Compute budget e strategia cloud** (~1.5 pp): valutazione adeguatezza PC per ogni fase, stima training GA non fattibile in locale, strategia AWS spot c5.4xlarge per il training, costi e frequenza di retraining.
- **Cap 5 — Definizione operativa del successo** (~1 pp): metrica primaria expected net return per segnale, metriche di lifecycle (executable/target-hit/invalidation), metriche di rischio (CVaR, drawdown), metriche anti-overfitting (DSR, PBO), filtro emissione minimo 80 punti.

## Parte II — Contratto del segnale FIB (~10 pp)

- **Cap 6 — Schema del segnale e invarianti** (~2 pp): payload del segnale (direzione, zona, target strutturale, stop strutturale, timestamp di emissione), invariante "no refresh" del segnale emesso.
- **Cap 7 — Stati del segnale e state machine** (~2 pp): emitted, executable, executed, target_hit, invalidated, missed_target, expired; transizioni ammesse e timer di scadenza.
- **Cap 8 — Guardie di esecuzione al touch** (~2 pp): condizioni di filtro al raw touch della entry zone (volatilita', spread, liquidita', distanza dal target).
- **Cap 9 — Politica di pubblicazione su Telegram** (~2 pp): formato messaggio, latenza ammissibile, gestione duplicati e correzioni.
- **Cap 10 — Replay e riproducibilita' del lifecycle** (~2 pp): formato dei log, ricostruzione deterministica del lifecycle a partire dallo storico tick/1-min.

## Parte III — Layer quantitativo single-instrument (~8 pp)

- **Cap 11 — Definizioni di rendimento e scala temporale** (~1.5 pp): rendimenti log 1-min, aggregazione a barre superiori, gestione gap di sessione.
- **Cap 12 — Modello di volatilita' condizionata** (~2.5 pp): EGARCH single-instrument, calibrazione, diagnostica residui standardizzati.
- **Cap 13 — Stato di regime intraday** (~2 pp): classificazione regime calmo/turbolento, soglie derivate da quantili rolling, persistenza minima.
- **Cap 14 — Feature engineering causale** (~2 pp): feature derivate da prezzo/volume/volatilita', vincolo di causalita' temporale (no look-ahead), normalizzazione robusta.

## Parte IV — Geometria zone, target strutturali, survival (~12 pp)

- **Cap 15 — Definizione delle zone di entry** (~2 pp): costruzione geometrica della zona long e short, parametri di larghezza e ancoraggio.
- **Cap 16 — Target strutturali** (~2 pp): derivazione del target dalla struttura del prezzo, vincolo minimo 80 punti (punto 4 dichiarazione).
- **Cap 17 — Stop strutturali** (~2 pp): derivazione dello stop dalla struttura, separazione dallo stop personale dell'operatore.
- **Cap 18 — Modello di survival per il target** (~2 pp): probabilita' condizionata di raggiungere il target prima dello stop strutturale e prima dello scadere della sessione.
- **Cap 19 — Filtri di emissione basati sul survival** (~2 pp): soglie su probabilita' di target hit, integrazione con regime corrente.
- **Cap 20 — Caso trade range** (~2 pp): gestione del setup a range con ampiezza definita, eccezione al filtro 80 punti.

## Parte V — Motore genetico e fitness operativa (~10 pp)

- **Cap 21 — Cromosoma e spazio dei parametri** (~2 pp): genoma del bundle (parametri zone, target, stop, soglie filtro, parametri survival), vincoli di ammissibilita'.
- **Cap 22 — Operatori GA** (~2 pp): selezione NSGA-II, crossover, mutazione, elitismo.
- **Cap 23 — Funzione di fitness multi-obiettivo** (~2 pp): obiettivi (expected net return, target hit rate, invalidation rate, drawdown), penalita' per emissione eccessiva o nulla.
- **Cap 24 — Walk-forward nested con purge ed embargo** (~2 pp): schema temporale dei fold, prevenzione del leakage, purge ed embargo tra in-sample e out-of-sample.
- **Cap 25 — Calibrazione dimensione popolazione, generazioni, criteri di stop** (~2 pp): popolazione 128, generazioni fino a 150, criteri di convergenza, gestione del seed.

## Parte VI — Emissione segnali e lifecycle senza execution (~6 pp)

- **Cap 26 — Pipeline di inference real-time** (~1.5 pp): ingest del feed Directa, calcolo feature, valutazione del bundle frozen, emissione del segnale.
- **Cap 27 — Politica anti-doppio-segnale** (~1.5 pp): gestione di segnali concorrenti sulla stessa direzione, no-refresh del segnale emesso.
- **Cap 28 — Gestione dell'operativita' su mobile** (~1.5 pp): formato del messaggio Telegram leggibile in mobilita', informazioni minime necessarie all'operatore.
- **Cap 29 — Monitoraggio del lifecycle in produzione** (~1.5 pp): metriche di lifecycle calcolate live, dashboard di sintesi, alert su deriva.

## Parte VII — Validazione OOS, frozen bundle, gate decisionali (~8 pp)

- **Cap 30 — Procedura di validazione OOS** (~1.5 pp): finestre OOS, scelta del bundle candidato, regole di selezione.
- **Cap 31 — Deflated Sharpe Ratio (DSR)** (~1.5 pp): definizione, stima, uso come gate primario di selezione.
- **Cap 32 — Probability of Backtest Overfitting (PBO) via CSCV** (~1.5 pp): definizione, stima, soglia di accettazione.
- **Cap 33 — Bootstrap stazionario** (~1.5 pp): parametri (B=2000, block length), uso per intervalli di confidenza su DSR e metriche di lifecycle.
- **Cap 34 — Frozen bundle e immutabilita'** (~1 pp): processo di freezing, hash di riferimento, regola di sostituzione.
- **Cap 35 — Gate decisionali per il go-live** (~1 pp): checklist DSR positivo, PBO sotto soglia, lifecycle stabile su regime calmo e turbolento.

## Appendici operative (~6 pp)

- **Appendice A — Specifiche PC e ambiente Python**: dettagli i5-7200U, Anaconda base, requirements, repository del codice.
- **Appendice B — Setup Claude Code e GitHub**: workflow dei 3 agenti, struttura repo, branch policy, formato commit.
- **Appendice C — API Directa**: qualificazione tra Darwin, DAPI e Visual Trader, requisiti di dato real-time del modello.
- **Appendice D — Storico Portara/CQG**: specifica del feed (FIB continuo 1-min, 5 anni minimo), valutazione costo e formato.
- **Appendice E — Telegram bot personale**: setup del bot, gestione chat ID, schema messaggio.
- **Appendice F — I 3 agenti Planner / Development / Review**: ruoli, ingressi, output, regole di handoff.
- **Appendice G — Glossario**: termini ricorrenti (zone, target strutturale, lifecycle, DSR, PBO, bundle frozen).
