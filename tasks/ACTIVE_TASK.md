# TASK ATTIVO: CAP-02 — Parte II del documento metodologico v2 (rework v3)

**Assegnato da**: Planner (Orchestratore)
**Output atteso**: `docs/methodology_v2/CAP_02_parte_II.md` (versione v3)
**Stato**: IN CORSO — rework v3 dopo decisione supervisore Q-05 (Opzione D raffinata) e finding aperti di Review v2

## Obiettivo

Scrivere la Parte II del documento metodologico v2: **Contratto del segnale FIB**. Questa parte risponde a: cosa è esattamente un segnale, in quali stati può trovarsi nel suo ciclo di vita, sotto quali condizioni viene emesso dal motore, come viene pubblicato all'operatore, come viene loggato per essere riprodotto deterministicamente in backtest e in review, e come viene tracciato il position lifecycle post-target_1 fuori scope dal motore ma in scope per il reporting.

Non contiene la matematica del modello (volatilità EGARCH, survival, GA) → Parti III-V. Non contiene parametri numerici congelati → Parte V. Contiene il **contratto** che il motore deve onorare, che il GA ottimizza, e la **submacchina di tracking** che alimenta il reporting di calibrazione.

La versione v3 incorpora la decisione del supervisore Q-05 (Opzione D raffinata: contratto del segnale separato dal position lifecycle) e chiude tutti i finding aperti della Review v2.

## Eredità obbligatoria da CAP-01

Tutte le decisioni del supervisore prese in CAP-01 (Q-01..Q-04 chiuse) + raffinamenti dell'Iterazione 2 di CAP-01 entrano come vincoli rigidi:

1. **Sessione operativa**: 8:00-22:00 CET, finestra unica e continua di negoziazione FIB (Q-01).
2. **Banda di ingresso**: parametro libero del cromosoma con dominio discreto $b \in \{5, 10, 15, 20, 25, 30, 35, 40\}$ punti FIB (multipli di tick), $b_{min} = 5$ provvisorio.
3. **Vincolo geometrico**: $d_{stop} > b$ obbligatorio; cromosomi che lo violano sono non validi.
4. **Target**: target_1 e target_2 entrambi obbligatori, ancorati a livelli strutturali. **target_2 resta nel payload come informazione strutturale pubblicata** (decisione supervisore Q-05, Clausola 2).
5. **Cap validità post-esecuzione**: $\leq 2$ giorni di trading **decorrenti dal raw touch** (non dall'emissione) — patch CAP-01 Iterazione 2 (commit `fc7531b`). Il GA può ottimizzare il timing di chiusura entro questo tetto.
6. **Movimento strutturale**: definito dalla somma dei moduli degli swing tra pivot strutturali; ancoraggio al primo min/max identificato dopo l'apertura della sessione (Q-02).
7. **Filtro emissione**: $\geq 80$ punti FIB su target_1, o rettangolo trade_range $\geq 80$ punti.
8. **No execution**: il motore emette segnali, non ordini. Punto 1 dichiarazione di intenti.
9. **Tick size FIB = 5 punti**: tutti i prezzi sono multipli di 5; la banda di ingresso è insieme discreto di livelli; ogni formula e ogni esempio deve rispettare la discretizzazione.
10. **`executable_rate` ridefinita** (patch CAP-01 Iterazione 2): frazione di segnali emessi che raggiungono il raw touch entro il timer di attesa pre-esecuzione. Il raw touch è sempre eseguibile; le condizioni di mercato sono valutate prima dell'emissione, non come filtri post-trigger.

Eredità Q-05 (decisione supervisore 2026-05-23, B-3 Review v2):

11. **State machine del segnale**: 1 non-terminale (`active`) + **6 terminali** (`target_1_hit`, `stopped`, `invalidated`, `missed_target`, `expired`, `revoked`). `target_2_hit` RIMOSSO dagli stati del segnale.
12. **Separazione segnale vs position lifecycle**: il contratto del segnale è oggetto del motore (ottimizzato dal GA); il position lifecycle è oggetto del reporting (alimenta validazione GA fold-by-fold). I due lifecycle sono distinti per costruzione, in coerenza con baseline hard-locked Cap. 21.1 e 22.6.

Ogni capitolo deve citare l'eredità pertinente, non duplicare la motivazione.

## Capitoli da produrre (~11-12 pagine totali in italiano formale)

### Capitolo 6 — Schema del segnale e invarianti (~2 pp)
Definizione formale del payload del segnale come tupla strutturata, sul reticolo discreto del tick FIB:
- `signal_id`: identificatore univoco
- `timestamp_emission`: istante di emissione (precisione minuto)
- `direction`: long | short
- `entry_zone`: insieme discreto $\{p_{ref}-b, p_{ref}-b+5, \ldots, p_{ref}+b\}$ con $b \in \{5, ..., 40\}$
- `target_1`, `target_2`: prezzi strutturali multipli di 5 (long: $\texttt{target\_1} > p_{ref}$, $\texttt{target\_2} > \texttt{target\_1}$; short simmetrico)
- `stop_loss`: prezzo strutturale multiplo di 5, $d_{stop} > b$
- `setup_class`: directional | trade_range
- $\Delta t_{cromosoma}$ post-trigger: intero in minuti di trading nel dominio $\{1, \ldots, 1680\}$

**Nota esplicita obbligatoria** (decisione Q-05 Clausola 2): "target_2 è informazione strutturale pubblicata, non variabile di lifecycle del segnale; il suo eventuale raggiungimento è evento del position lifecycle, fuori scope dal motore (vedi Cap.11)".

Due regole strutturali del contratto:

**Payload immutabile** — una volta emesso, il `signal_id` non subisce modifiche al payload.

**Sostituzione e segnale unico attivo** — quando il motore valuta che le condizioni di mercato richiedono di rivedere il segnale, emette un nuovo `signal_id`; il segnale precedente viene revocato. A ogni istante $|\mathcal{A}(t)| \leq 1$, coerente col vincolo "1 contratto alla volta" (punto 7 dichiarazione) e con la revisione continua del segnale (punto 6).

### Capitolo 7 — Stati del segnale e state machine (~2 pp)

Stato unico non-terminale: `active`.

Stati terminali (6, decisione Q-05 Clausola 1):
- `target_1_hit`: dopo il raw touch della entry zone, il prezzo ha raggiunto target_1. Stato terminale di successo del segnale. **Il contratto del segnale si chiude qui**: il post-target_1 è oggetto del position lifecycle (Cap.11), non transizione di stato del segnale.
- `stopped`: dopo il raw touch, il prezzo ha raggiunto stop_loss prima di target_1.
- `invalidated`: prima del raw touch, condizione di invalidazione strutturale (Parte IV, Cap.15); fra cui esplicitamente $p(t) \leq \texttt{stop\_loss}$ per long, simmetrico per short.
- `missed_target`: prima del raw touch, il prezzo ha raggiunto target_1. Metrica riferita esplicitamente a target_1 (chiusura Q-03 di CAP-01).
- `expired`: scaduto il timer post-trigger (2gg trading dal raw touch) oppure scaduto il timer pre-trigger di attesa (se introdotto come stato terminale dedicato — vedi finding NB-7 da risolvere sotto).
- `revoked`: superseduto dall'emissione di un nuovo `signal_id`.

**Trigger di esecuzione come evento, non come stato.** Al raw touch della entry zone, il motore produce un evento `trigger_event` notificato all'operatore. Questo evento non è uno stato del segnale: il segnale resta `active` finché un evento successivo non lo porta in uno stato terminale. **Il raw touch è sempre eseguibile**: non esistono guardie o filtri post-emissione che blocchino il trigger. Le condizioni di mercato sono valutate prima dell'emissione (Cap.8), non al raw touch.

**Nota esplicita obbligatoria** (decisione Q-05 Clausola 1): "Il raggiungimento eventuale di target_2 dopo target_1 NON è una transizione di stato del segnale ma un evento del position lifecycle (Cap.11). Il segnale termina definitivamente in `target_1_hit`".

Timer post-trigger: 2 giorni di trading **dal raw touch** (eredità CAP-01 Iterazione 2). Granularità: intero in minuti di trading, dominio $\{1, \ldots, 1680\}$. Esempio numerico per emissione vicino alla chiusura di sessione: counter in minuti di trading che scavalca interruzioni notturne e weekend.

Inclusione di **M-1** (carryover CAP-01): identificazione real-time del primo pivot strutturale post-apertura va trattata a livello di interfaccia (cosa il motore osserva, con che cadenza). L'algoritmo di pivot detection è rinviato a Parte III (Cap 14). Il vincolo metodologico: la regola di pivot detection di Parte III non deve produrre primo candidato con latenza tale da rendere inattiva la finestra iniziale 8:00-22:00. Quantificazione di $N_{pivot}$ (massimo barre dall'apertura per il primo candidato) rinviata a Parte V con misura empirica sullo storico.

### Capitolo 8 — Condizioni di emissione del segnale (~2 pp)

Le tre condizioni di emissione applicate dal motore **prima** dell'emissione del segnale (no filtri post-trigger):

1. **Condizione di volatilità**: range della barra 1-min $r_{1m}(t_{emission}) \leq \tau_{vol}(\hat{\sigma}(t_{emission}))$, con $\tau_{vol}$ funzione di soglia parametrizzata dal cromosoma, alimentata dal modello EGARCH di Parte III.
2. **Condizione di liquidità**: volume del minuto $v_{1m}(t_{emission}) \geq \tau_{liq}$, con $\tau_{liq}$ parametro libero del cromosoma.
3. **Condizione di distanza strutturale dal target_1 in unità di volatilità** (decisione supervisore NB-10 Review v2, opzione β):

$$\frac{|\texttt{target\_1} - p_{ref}|}{\hat{\sigma}(t_{emission})} \geq \tau_{dist}^{\sigma}$$

con $\tau_{dist}^{\sigma}$ parametro libero del cromosoma (numero puro, sigma-units). Il filtro 80pt CAP-01 resta come vincolo assoluto a valle: per setup directional $|\texttt{target\_1} - p_{ref}| \geq 80$ pt; per setup trade_range $|\texttt{target\_1} - \texttt{stop\_loss}| \geq 80$ pt. Il GA può richiedere distanze maggiori in sigma-units se la volatilità è alta; il filtro 80pt non è allentabile dal cromosoma.

L'emissione avviene se e solo se le tre condizioni sono simultaneamente soddisfatte. Soglie congelate in Parte V. Modello di volatilità in Parte III. Le condizioni si applicano uniformemente in tutta la sessione 8:00-22:00 CET, senza fasi speciali (chiarimento supervisore M-3 di Review v4 di CAP-01: ritirata, FIB negozia in modo continuo).

**Spread bid-ask ELIMINATO come condizione**: lo storico Portara/CQG FIB 1-min non contiene book/spread; una condizione su spread non sarebbe addestrabile dal GA senza acquisti aggiuntivi di dati esplicitamente esclusi in CAP-01.

### Capitolo 9 — Politica di pubblicazione su Telegram (~2 pp)
Formato concreto del messaggio Telegram leggibile in mobilità:
- struttura del messaggio (campi obbligatori e ordine: signal_id, direction, setup_class, entry_zone, target_1, target_2, stop_loss, timestamp_emission)
- latenza massima ammissibile dall'emissione interna alla ricezione sul cellulare ($L_{max} = 30$ s provvisorio, congelato in Parte V)
- politica anti-duplicato: un `signal_id` viene pubblicato una sola volta
- politica per nuovo segnale: emesso come messaggio separato con nuovo `signal_id`, NON come modifica/edit del messaggio precedente (coerente con immutabilità Cap.6)
- notifica `trigger_event` al raw touch come messaggio separato (no edit), riferito al `signal_id`
- gestione errori di pubblicazione (timeout API Telegram, retry policy con $n_{retry}=3$ provvisorio)

Schema esatto delle stringhe del messaggio rinviato all'Appendice E.

### Capitolo 10 — Replay e riproducibilità del lifecycle (~2 pp)
Definizione del formato dei log per ricostruire deterministicamente il lifecycle:
- log di emissione (snapshot completo del payload + snapshot delle 3 condizioni di emissione + feature al momento dell'emissione + esito pubblicazione Telegram)
- log delle transizioni di stato della state machine del segnale (timestamp, stato precedente, stato nuovo, prezzo trigger, causa strutturata; il `trigger_event` registrato come evento associato non come transizione)
- log di chiusura del segnale (stato terminale + statistiche aggregate: rendimento lordo per segnali eseguiti, MAE, MFE post-trigger, durata totale e post-trigger in minuti di trading)

Requisito di determinismo formale: $\forall H, \forall B: \texttt{replay}(H, B) = \texttt{replay}(H, B)$ bit-exact. Seed di qualunque componente casuale è parte del bundle congelato.

### Capitolo 11 — Position lifecycle e tracking out-of-scope dal motore (~1-2 pp) **[NUOVO, decisione Q-05 Clausola 3]**

Definizione della submacchina di tracking del position lifecycle, **distinta dal lifecycle del segnale**, che gira in parallelo al replay del segnale e traccia gli eventi post-target_1 come oggetto di reporting per la validazione del GA.

**Vincoli architetturali obbligatori**:

- **OUT-OF-SCOPE dal motore**: execution policy, scaling-out automatico, trailing stop, dynamic sizing, qualsiasi decisione operativa post-target_1. La gestione della posizione oltre target_1 è dell'operatore manuale (punto 8 della dichiarazione di intenti).
- **IN-SCOPE per reporting e validazione**: la submacchina produce metriche che alimentano i report fold-by-fold del walk-forward in Parte V/Cap.23:
  - hit-rate condizionale di target_2 dato target_1 ($\pi_{t_2 \mid t_1}$)
  - distribuzioni di MFE (maximum favourable excursion) e MAE (maximum adverse excursion) post-target_1
  - eventi di stop dopo target_1 (retracement che riporta il prezzo a stop_loss)
  - distribuzione dei tempi di permanenza fra target_1 e evento terminale del position lifecycle
- **Indipendenza dal segnale**: la submacchina NON modifica lo stato del segnale; il segnale è terminato in `target_1_hit` prima ancora che la submacchina inizi a tracciare. Le metriche prodotte sono input al GA come obiettivi/vincoli di Parte V, non come variabili decisionali nel cromosoma.

**Citazioni testuali obbligatorie del baseline hard-locked**:
- Cap. 21.1 di `docs/reference/ENGINE_ALGO_INTEGRATO_HARD_LOCKED.pdf` (lifecycle della posizione vs lifecycle del contratto di segnale come sottosistemi distinti)
- Cap. 22.6 di `docs/reference/ENGINE_ALGO_INTEGRATO_HARD_LOCKED.pdf` (submacchina della posizione come boundary esplicito)

**Stati della submacchina position lifecycle** (proposta, da formalizzare in dettaglio):
- evento di ingresso: il segnale ha raggiunto `target_1_hit`
- stati interni di tracking (eventi registrati nel log della submacchina): `target_2_reached`, `stop_after_target_1`, `retracement_to_breakeven`, `position_close_event`
- stato terminale: chiusura della posizione (manuale dell'operatore in real-time; convenzione di simulazione in backtest)

**Impatto sul GA**: la submacchina alimenta metriche di calibrazione che entrano nella fitness multi-obiettivo del GA come obiettivi di qualità informativa del livello target_2 e di robustezza strutturale del setup. Lo space search del cromosoma NON viene esteso: nessuna policy decisionale post-target_1 entra nel cromosoma.

## Finding di Review v2 da risolvere (carryover obbligatorio)

Oltre alla decisione Q-05 (B-3), il rework v3 deve chiudere i seguenti finding ancora aperti dalla Review v2 di Parte II v2 (commit `c4d41bf`, file `reviews/CAP_02_review.md`):

- **NB-7 — Timer pre-trigger di attesa al raw touch**: il segnale può restare in `active` indefinitamente senza raw touch. Sotto decisione Q-05, dopo target_1_hit il segnale termina, ma il problema della fase di attesa pre-trigger resta. Soluzione approvata: timer dedicato $T_{touch}^{max}$ come parametro libero del cromosoma, espresso in minuti di trading, dominio $\{5, 6, \ldots, 480\}$ (cardinalità 476, floor 5 min, tetto 8h trading). Dipendenza funzionale dal regime e dalla distanza prezzo corrente ↔ $p_{ref}$ rinviata a Parte III/IV. Allo scadere del timer senza raw touch, il segnale transita in stato terminale `expired` (assorbimento nel terminale esistente, no nuovo stato — coerente con il vincolo 6 terminali della decisione Q-05). La distinzione fra "expired per timer pre-trigger" e "expired per timer post-trigger" viene registrata nel log delle transizioni come campo causale, non come stato dedicato.

- **NB-8 — Edge case raw touch su barra di emissione o gap di apertura**: la Parte II v3 deve trattare esplicitamente almeno tre casi: (a) la barra 1-min di emissione contiene già un prezzo che cade dentro l'`entry_zone` (raw touch immediato al momento dell'emissione?); (b) il prezzo apre con gap alla riapertura della sessione successiva con valore già dentro o oltre la zona; (c) il prezzo apre con gap che salta completamente la zona (es. long con zona $[40990, 41010]$ e apertura a 40970, sotto la zona). Per ciascun caso il documento deve specificare il comportamento della state machine (raw touch riconosciuto? convenzione del prezzo di trigger?).

- **NB-9 — Transizione `target_1_hit → revoked` mancante**: sotto decisione Q-05 (target_1_hit veramente terminale), questo finding si **chiude da solo**: nessuna transizione esce da target_1_hit, quindi non c'è bisogno di una transizione verso revoked. Il documento deve solo esplicitarlo per evitare ambiguità.

- **NB-10 — $\tau_{dist}$ in sigma-units (opzione β confermata)**: vedi Cap.8 sopra.

## Acceptance criteria — tutti devono essere soddisfatti per PASS in Review

- [ ] I 6 capitoli (Cap 6-10 + Cap 11) sono presenti, completi, nell'ordine corretto
- [ ] Tutte le 12 eredità (8 di CAP-01 + 4 raffinamenti Iterazione 2 e Q-05) sono citate esplicitamente almeno una volta nei capitoli pertinenti
- [ ] Cap 6: il payload è specificato come tupla con tutti i campi e i loro vincoli, incluso target_2 obbligatorio
- [ ] Cap 6: nota esplicita "target_2 è informazione strutturale pubblicata, non variabile di lifecycle del segnale; il suo eventuale raggiungimento è evento del position lifecycle"
- [ ] Cap 6: entry_zone definita come insieme discreto sul reticolo del tick FIB (multipli di 5), banda $b \in \{5, 10, 15, 20, 25, 30, 35, 40\}$
- [ ] Cap 6: payload immutabile e regola di sostituzione (revoca + nuovo signal_id, segnale unico attivo) dichiarate esplicitamente
- [ ] **Cap 7: state machine ha 1 solo stato non-terminale (`active`) e 6 stati terminali: `target_1_hit`, `stopped`, `invalidated`, `missed_target`, `expired`, `revoked`. target_2_hit RIMOSSO.**
- [ ] Cap 7: transizioni esplicite (tabella) con condizioni di trigger per ciascuna
- [ ] Cap 7: nota esplicita "il raggiungimento eventuale di target_2 dopo target_1 NON è una transizione di stato del segnale ma un evento del position lifecycle"
- [ ] Cap 7: `invalidated` esplicita il sotto-caso "stop_loss attraversato pre-touch" (B-1 Review v1)
- [ ] Cap 7: `trigger_event` dichiarato come evento, raw touch sempre eseguibile, nessun filtro post-emissione
- [ ] Cap 7: timer post-trigger 2gg trading decorrente dal raw touch, $\Delta t_{cromosoma}$ intero in minuti dominio $\{1, \ldots, 1680\}$, esempio caso emissione 21:55
- [ ] Cap 7: timer pre-trigger $T_{touch}^{max}$ con dominio $\{5, \ldots, 480\}$ minuti di trading, scadenza assorbita in `expired` con causa "pretrigger_timeout" nel log (NB-7)
- [ ] Cap 7: edge case raw touch trattati (barra di emissione, gap di apertura inside zone, gap oltre zona) (NB-8)
- [ ] Cap 7: M-1 trattato a livello di interfaccia con rinvio a Parte V per $N_{pivot}$
- [ ] Cap 8: 3 condizioni di emissione pre-emissione (volatilità, liquidità, distanza target_1 in sigma-units), spread eliminata con motivazione esplicita (no storico book)
- [ ] Cap 8: $\tau_{dist}^{\sigma}$ come sigma-units, filtro 80pt CAP-01 come vincolo assoluto a valle (NB-10)
- [ ] Cap 8: rinvio a Parte V per soglie congelate, a Parte III per modello volatilità
- [ ] Cap 8: nessuna assunzione di fasi speciali nella sessione 8:00-22:00 (M-3 ritirato)
- [ ] Cap 9: politica anti-duplicato e "nuovo messaggio per nuovo signal_id" coerenti con immutabilità Cap 6 (mai edit del messaggio precedente)
- [ ] Cap 9: notifica `trigger_event` come messaggio separato
- [ ] Cap 10: log di emissione include snapshot delle 3 condizioni di emissione (non più 4 guardie)
- [ ] Cap 10: log delle transizioni registra $t_{exec}$ del raw touch come riferimento del timer post-trigger
- [ ] Cap 10: requisito di determinismo bit-exact dichiarato come vincolo formale
- [ ] **Cap 11 (nuovo): definisce la submacchina position lifecycle come oggetto distinto dal lifecycle del segnale**
- [ ] **Cap 11: dichiarazione esplicita di OUT-OF-SCOPE dal motore (execution policy, scaling-out, trailing stop, dynamic sizing)**
- [ ] **Cap 11: dichiarazione esplicita di IN-SCOPE per reporting (metriche $\pi_{t_2 \mid t_1}$, MFE, MAE, eventi post-target_1)**
- [ ] **Cap 11: la submacchina NON modifica lo stato del segnale (separazione formale)**
- [ ] **Cap 11: citazioni testuali del baseline hard-locked Cap. 21.1 e 22.6 (`docs/reference/ENGINE_ALGO_INTEGRATO_HARD_LOCKED.pdf`)**
- [ ] **Cap 11: dichiarazione che lo space search del cromosoma del GA NON viene esteso (nessuna policy decisionale post-target_1 nel cromosoma)**
- [ ] Registro tecnico italiano formale (no linguaggio divulgativo)
- [ ] Formule e notazione in LaTeX inline e display dove serve
- [ ] Niente moltiplicazioni misleading o numeri inventati; valori provvisori dichiarati come tali con rinvio a Parte V
- [ ] Tick FIB = 5pt rispettato in ogni esempio numerico (prezzi e bande multipli di 5)
- [ ] Coerenza con CAP-01 v2 (post-patch Iterazione 2 commit `fc7531b`): cap 2gg dal raw touch, executable_rate ridefinita
- [ ] Il REPORT_CAP_02.md include una sezione "Iterazione 3 — risposta ai finding di Review v2 + decisione supervisore Q-05" con misura prima/dopo

## Out-of-scope — Development NON include queste cose in CAP-02

- Formule EGARCH, modello survival, feature engineering causale → Parti III-IV
- Operatori GA, fitness multi-obiettivo, walk-forward → Parte V (incluso $\pi_{t_2 \mid t_1}$ come funzione obiettivo nella fitness)
- Algoritmo concreto di pivot detection → Parte III (Cap 14); quantificazione $N_{pivot}$ → Parte V con misura empirica
- Setup tecnico API Directa, Telegram, Portara → Appendici C-E
- Parametri numerici congelati delle soglie e dei timer → Parte V
- **Execution policy della posizione post-target_1** (decisione Q-05 Clausola 3): scaling-out automatico, trailing stop, dynamic sizing, take profit anticipato, qualsiasi gestione attiva → la posizione post-target_1 è gestita manualmente dall'operatore (punto 8 dichiarazione di intenti). Il Cap 11 definisce solo il tracking per reporting, non la policy di gestione.
- Modello di first passage time per la dipendenza di $T_{touch}^{max}$ da regime e distanza → Parte III/IV
- Forma funzionale di $\tau_{vol}(\hat{\sigma})$ → Parte III, Cap.12

## Done when

Il documento risponde senza ambiguità a queste domande:
1. Cosa contiene esattamente un segnale emesso dal motore? (Cap 6)
2. Quali stati può attraversare il segnale e con quali transizioni? (Cap 7, 6 terminali)
3. Sotto quali condizioni il motore decide di emettere un segnale? (Cap 8, 3 condizioni pre-emissione)
4. Come arriva il segnale al cellulare dell'operatore? (Cap 9)
5. Come si ricostruisce deterministicamente il lifecycle del segnale? (Cap 10)
6. Come si traccia il position lifecycle post-target_1 senza che il motore lo gestisca? (Cap 11)
7. Perché target_2 è informazione strutturale del payload ma non variabile di lifecycle del segnale? (Cap 6 + Cap 11)

## Pipeline attesa

Development v3 → Review v3 audit ostile con classificazione GA → punto di controllo supervisore se CONDITIONAL/FAIL → fix → ... → PASS.

Promemoria operativo per Development: la decisione Q-05 implementa l'Opzione D raffinata del baseline hard-locked. Il Cap 11 è capitolo NUOVO che non esisteva in Parte II v1/v2; va scritto ex-novo con citazioni testuali del baseline Cap. 21.1 e 22.6. Non improvvisare: le citazioni vanno verificate sul PDF di riferimento.
