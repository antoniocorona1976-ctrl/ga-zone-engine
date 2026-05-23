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
