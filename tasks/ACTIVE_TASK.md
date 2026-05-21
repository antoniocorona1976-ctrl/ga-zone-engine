# TASK ATTIVO: CAP-01 — Parte I del documento metodologico v2

**Assegnato da**: Planner
**Output atteso**: docs\methodology_v2\CAP_01_parte_I.md
**Stato**: IN ATTESA — eseguire solo dopo che i 2 PDF di riferimento sono in docs\reference\

## Obiettivo
Scrivere la Parte I del documento metodologico v2 "Motore genetico strutturale per segnali FIB".
Questa parte risponde a: chi usa il sistema, su cosa, con quali strumenti, con quali aspettative quantitative.
Non contiene formule del modello. Non contiene setup tecnico. Solo ambito, vincoli e definizione del successo.

## Capitoli da produrre (6-8 pagine totali in italiano formale)

### Capitolo 1 — Obiettivo operativo
Il sistema genera segnali long/short sul FIB (futures mini su FTSE MIB, mercato IDEM, codice MIB).
Sessione operativa primaria: 9:00-17:40 CET (sessione regolare IDEM).
Target operativo: 500 punti al giorno oppure 70% dell'escursione intraday del FIB misurata
dall'apertura della sessione fino alla chiusura, prendendo come riferimento il range massimo osservato
nel giorno dal primo segnale post-apertura. Il sistema non esegue ordini autonomamente.
Pubblica segnali strutturati; l'operatore decide e agisce manualmente.
Specificare esplicitamente: il sistema genera SOLO segnali (punto 1 dichiarazione di intenti).

### Capitolo 2 — Profilo operatore e vincoli operativi
Operatore: risk manager bancario italiano, operatore retail non professionale ai sensi MiFID II.
Opera da cellulare durante la giornata lavorativa. Non puo' monitorare il terminale in modo continuo.
Dimensionamento: 1 contratto FIB alla volta (1 contratto FIB = 5 euro per punto indice).
Commissioni: 5 euro per operazione di apertura o chiusura (punto 10 dichiarazione).
Gestione size, incrementi di posizione, take profit e stop profit: scelte esclusivamente dell'operatore,
non codificate nel segnale (punti 7 e 8 dichiarazione). Il segnale pubblica direzione, zona ingresso,
target strutturale e stop strutturale; non pubblica gestione della posizione.
SL personale dell'operatore: -200 punti di emergenza immediato dopo il fill (prassi operatore,
non parametro del sistema). Rollover: gestione da definire in funzione dello spread futures/cash
nelle ultime sessioni prima della scadenza (punto 9 dichiarazione).

### Capitolo 3 — Infrastruttura disponibile
PC: Intel Core i5-7200U 2.5GHz (mobile, dual-core/4-thread), 8GB RAM DDR4, Intel HD Graphics 620,
238GB SSD, Windows 10. Ambiente Python: Anaconda (base).
Broker: Directa SIM (accesso da mobile). Interfaccia operativa da qualificare tra Darwin, DAPI e
Visual Trader — verifica della disponibilita' dei dati real-time utili al modello rinviata all'Appendice C.
Dati storici: FIB continuo 1-minuto, minimo 5 anni, da Portara/CQG — specifiche richiesta e valutazione
costo rinviate all'Appendice D. Questa e' la lacuna da colmare prima dell'avvio del progetto.
Feed real-time in forward-run: Directa (da qualificare quale API).
Canale notifiche segnali: Telegram bot personale (dettagli setup in Appendice E).

### Capitolo 4 — Compute budget e strategia cloud
Valutazione PC per ciascuna fase del progetto:

Fase sviluppo e test unitari: adeguato. I5-7200U regge scrittura codice, test su finestre brevi,
debug della state machine, inference real-time del bundle frozen.

Fase backtest singolo cromosoma su 5 anni FIB 1-min (~650.000 osservazioni):
stima 2-8 minuti per cromosoma a seconda del layer attivo. Lento ma fattibile.

Fase training completo GA: NSGA-II popolazione 128, generazioni fino a 150, walk-forward nested
con purge/embargo, bootstrap stazionario B=2000 per DSR/PBO. Stima: 128 cromosomi x 150 generazioni
x 4-8 minuti/cromosoma = 12.800-25.600 minuti su single-thread, ovvero 9-18 giorni di calcolo continuo.
Verdict: non fattibile sul PC di casa.

Fase forward-run (inference live): adeguato. Il bundle frozen e' leggero, l'inference di un segnale
richiede secondi.

Strategia cloud: AWS spot instance c5.4xlarge (16 vCPU, 32GB RAM, ~0.34 USD/ora spot).
Stima training completo GA su cloud: 8-16 ore, costo 3-6 USD. Con overhead e prove: budget 20-30 euro
per run completo. Frequenza di retraining prevista: trimestrale o semestrale.
Il PC e' l'ambiente primario di sviluppo; il cloud e' usato esclusivamente per il training del GA.

### Capitolo 5 — Definizione operativa del successo
Traduzione quantitativa del target operativo. Le variabili sono definite qui; i valori soglia
emergono dalla prima campagna di validazione OOS.

Metrica primaria di segnale: expected net return per segnale eseguito, espresso in punti FIB
al netto delle commissioni (1 punto FIB = 5 euro; 5 euro commissione = 1 punto equivalente per operazione).
Formula: E[R_net | executed] = E[R_gross | executed] - 2 punti equivalenti commissioni (apertura + chiusura).

Metriche di lifecycle (da calcolare sul replay OOS della state machine):
- Emission count: numero segnali pubblicati per sessione
- Executable rate: frazione segnali che raggiungono il raw touch con guardie superate
- Target hit rate: frazione segnali eseguiti che raggiungono il target strutturale
- Invalidation rate: frazione segnali invalidati prima del touch
- Missed target rate: target raggiunto prima della entry zone

Metriche di rischio: CVaR al 95%, max drawdown intraday, MAE/MFE aggregati.

Metriche anti-overfitting: DSR (Deflated Sharpe Ratio) come filtro primario di selezione del bundle;
PBO via CSCV come misura di fragilita' della selezione.

Filtro di emissione minimo (punto 4 dichiarazione): il sistema non pubblica segnali con target
strutturale inferiore a 80 punti FIB, salvo il caso di trade range con ampiezza definita.

Il successo del motore non e' "ha guadagnato X euro". E': il bundle frozen supera i gate OOS,
il DSR e' positivo, il PBO e' sotto soglia, le metriche lifecycle sono stabili tra regime calmo
e regime turbolento. Il profitto operativo dell'operatore dipende dall'esecuzione, non solo dal segnale.

## Acceptance criteria — tutti devono essere soddisfatti per PASS in Review
- [ ] I 5 capitoli sono presenti, completi e nell'ordine corretto
- [ ] Capitolo 1: il target 500pt/70% e' definito senza ambiguita' (su quale escursione, da quando)
- [ ] Capitolo 2: i punti 1, 7, 8, 9, 10 della dichiarazione di intenti sono citati esplicitamente
- [ ] Capitolo 3: il PC e' specificato con i dati tecnici reali (non generici)
- [ ] Capitolo 4: la stima del training GA include numeri (non solo "e' lento")
- [ ] Capitolo 5: nessuna formula vaga; tutto e' variabile numerica o soglia da calibrare
- [ ] Registro tecnico identico al documento originale (niente linguaggio divulgativo o colloquiale)
- [ ] Lunghezza: 6-8 pagine (stima ~1500-2000 parole)

## Out-of-scope — Development NON include queste cose in CAP-01
- Formule matematiche del modello (EGARCH, survival, GA): vengono nelle Parti II-V
- Setup tecnico di Claude Code o GitHub: Appendice B
- Specifiche API Directa o Portara: Appendici C e D
- Telegram bot setup: Appendice E
- Definizione operativa dei 3 agenti Planner/Development/Review: Appendice F
- Parametri numerici congelati del GA (popolazione, generazioni, ecc.): Parte V

## Done when
Il capitolo risponde senza ambiguita' a questa domanda:
"Cosa fa questo sistema, chi lo usa, su quale strumento, con quale infrastruttura, e come misuriamo se funziona?"
