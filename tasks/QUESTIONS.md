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

**Stato**: chiusa.
