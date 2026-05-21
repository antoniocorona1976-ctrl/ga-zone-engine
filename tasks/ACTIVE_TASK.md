# TASK ATTIVO: CAP-02 — Parte II del documento metodologico v2

**Assegnato da**: Planner
**Output atteso**: `docs/methodology_v2/CAP_02_parte_II.md`
**Stato**: IN ATTESA — eseguire dopo conferma supervisore

## Obiettivo

Scrivere la Parte II del documento metodologico v2: **Contratto del segnale FIB**. Questa parte risponde a: cosa è esattamente un segnale, in quali stati può trovarsi nel suo ciclo di vita, sotto quali condizioni può essere eseguito, come viene pubblicato all'operatore, e come viene loggato per essere riprodotto deterministicamente in backtest e in review.

Non contiene la matematica del modello (volatilità, survival, GA) → Parti III-V. Non contiene parametri numerici congelati → Parte V. Contiene il **contratto** che il motore deve onorare e che il GA ottimizza.

## Eredità obbligatoria da CAP-01

Tutte le decisioni del supervisore prese in CAP-01 (Q-01..Q-04 chiuse) entrano come vincoli rigidi in Parte II:

1. **Sessione operativa**: 8:00-22:00 CET, finestra unica e continua di negoziazione FIB. Il movimento strutturale e i target sono ancorati a questa finestra.
2. **Banda di ingresso**: parametro libero del cromosoma con dominio $b \in [b_{min}, 40]$ punti FIB; $b_{min} = 5$ provvisorio.
3. **Vincolo geometrico**: $d_{stop} > b$ obbligatorio; cromosomi che lo violano sono non validi.
4. **Target**: target 1 e target 2 entrambi obbligatori, ancorati a livelli strutturali.
5. **Cap validità**: ≤ 2 giorni di trading dall'emissione; il GA può ottimizzare il timing di chiusura entro questo tetto.
6. **Movimento strutturale**: definito dalla somma dei moduli degli swing tra pivot strutturali; ancoraggio al primo min/max identificato dopo l'apertura della sessione (dalle 8:00 in poi).
7. **Filtro emissione**: ≥ 80 punti FIB su target 1, o rettangolo trade range ≥ 80 punti.
8. **No execution**: il motore emette segnali, non ordini. Punto 1 dichiarazione di intenti.

Ogni capitolo deve citare l'eredità pertinente, non duplicare la motivazione.

## Capitoli da produrre (~10 pagine totali in italiano formale)

### Capitolo 6 — Schema del segnale e invarianti (~2 pp)
Definizione formale del payload del segnale come tupla strutturata:
- `signal_id`: identificatore univoco
- `timestamp_emission`: istante di emissione (precisione minuto)
- `direction`: long | short
- `entry_zone`: banda $[p_{ref} - b, p_{ref} + b]$ con $p_{ref}$ prezzo strutturale di riferimento e $b \in [b_{min}, 40]$
- `target_1`, `target_2`: prezzi strutturali (long: $> p_{ref}$; short: $< p_{ref}$)
- `stop_loss`: prezzo strutturale, $d_{stop} > b$
- `expiry`: istante di scadenza, $\leq$ emissione + 2 giorni di trading
- `setup_class`: directional | trade_range

Invariante **no-refresh**: un segnale emesso non viene modificato. Se le condizioni di mercato cambiano, il motore emette un nuovo segnale con nuovo `signal_id`, il segnale precedente prosegue il proprio lifecycle indipendentemente.

Distinzione tra invarianti del segnale (immutabili dopo emissione) e stato del segnale (variabile nel lifecycle).

### Capitolo 7 — Stati del segnale e state machine (~2 pp)
Stati ammessi:
- `emitted`: pubblicato, in attesa di raw touch sulla entry zone
- `executable`: raw touch avvenuto, guardie di esecuzione superate
- `executed`: fill operatore confermato (in simulazione: prima quotazione dentro la banda)
- `target_1_hit`: il prezzo raggiunge target 1 dopo il fill
- `target_2_hit`: il prezzo raggiunge target 2 dopo target 1
- `stopped`: il prezzo raggiunge lo stop loss dopo il fill
- `invalidated`: condizione di invalidazione strutturale prima del touch
- `missed_target`: target 1 raggiunto dal prezzo prima del touch della entry zone
- `expired`: scadenza raggiunta in qualsiasi stato non terminale

Transizioni ammesse e timer di scadenza (cap 2 giorni di trading da `timestamp_emission`).

Inclusione esplicita di **M-1** (carryover CAP-01): l'identificazione real-time del primo pivot strutturale post-apertura va trattata almeno a livello di interfaccia (cosa il motore osserva, quando, con che cadenza); l'algoritmo di pivot detection è rinviato a Parte III (Cap 14, feature engineering).

### Capitolo 8 — Guardie di esecuzione al raw touch (~2 pp)
Condizioni di filtro applicate al raw touch della entry zone prima di promuovere il segnale a `executable`:
- guardia di volatilità (range del minuto entro soglia)
- guardia di spread (bid-ask spread entro soglia, da Directa real-time)
- guardia di liquidità (volume del minuto sopra soglia)
- guardia di distanza dal target 1 (target ancora raggiungibile rispetto al prezzo corrente)

Le soglie sono parametri liberi del cromosoma del GA (rinvio a Parte V per congelamento). Le formule del modello di volatilità sono in Parte III.

**M-3 (Review v4) — RITIRATO**: il promemoria riguardava la presunta asta di apertura 8:00-9:00 con barre theoretical opening price. Il supervisore ha chiarito che il FIB negozia in modo continuo 8:00-22:00 senza fase d'asta. Nessuna neutralizzazione di fase iniziale è richiesta. Non integrare in CAP-02.

### Capitolo 9 — Politica di pubblicazione su Telegram (~2 pp)
Formato concreto del messaggio Telegram leggibile in mobilità (l'operatore opera da cellulare durante orario di lavoro):
- struttura del messaggio (campi obbligatori e ordine)
- latenza massima ammissibile dall'emissione interna alla ricezione sul cellulare
- politica anti-duplicato: un `signal_id` viene pubblicato una sola volta
- politica per nuovo segnale: emesso come messaggio separato con nuovo `signal_id`, NON come modifica/edit del messaggio precedente (coerente con l'invariante no-refresh)
- gestione errori di pubblicazione (timeout API Telegram, retry policy)

Lo schema esatto delle stringhe del messaggio è rinviato all'Appendice E; in Parte II si fissano il contratto informativo e i vincoli operativi.

### Capitolo 10 — Replay e riproducibilità del lifecycle (~2 pp)
Definizione del formato dei log che consente di ricostruire deterministicamente il lifecycle di ogni segnale a partire dallo storico delle barre 1-min:
- log di emissione (snapshot completo del payload + stato delle feature al momento dell'emissione)
- log delle transizioni di stato (ogni transizione registra: timestamp, stato precedente, stato nuovo, prezzo che ha innescato la transizione)
- log di chiusura (stato terminale + statistiche aggregate per il segnale)

Requisito di determinismo: dato lo stesso storico 1-min e lo stesso bundle frozen, il replay produce **esattamente** la stessa sequenza di stati e gli stessi timestamp. Niente non-determinismo introdotto dal motore.

## Acceptance criteria — tutti devono essere soddisfatti per PASS in Review

- [ ] I 5 capitoli (Cap 6-10) sono presenti, completi e nell'ordine corretto
- [ ] Tutte le 8 eredità di CAP-01 sono citate esplicitamente almeno una volta nei capitoli pertinenti
- [ ] Cap 6: il payload è specificato come tupla strutturata con tutti i campi e i loro vincoli (banda, $d_{stop} > b$, expiry $\leq$ 2 giorni trading, $\geq$ 80 punti target 1)
- [ ] Cap 6: l'invariante no-refresh è dichiarata e separata dallo stato variabile
- [ ] Cap 7: la state machine ha tutti gli stati elencati e le transizioni esplicite (anche graficamente o in tabella)
- [ ] Cap 7: il cap 2 giorni di trading è implementato come timer concreto, non come prosa generica
- [ ] Cap 7: M-1 è trattato almeno a livello di interfaccia (cosa osserva il motore, con che cadenza)
- [ ] Cap 8: tutte e 4 le guardie sono nominate; il rinvio a Parte V per le soglie è esplicito
- [ ] Cap 8: nessuna assunzione di fasi speciali nella sessione 8:00-22:00 (M-3 ritirato dal supervisore)
- [ ] Cap 9: la politica anti-duplicato e il "nuovo messaggio per nuovo signal_id" sono coerenti con l'invariante no-refresh
- [ ] Cap 10: il requisito di determinismo del replay è dichiarato come vincolo, non come desiderio
- [ ] Registro tecnico italiano formale (no linguaggio divulgativo)
- [ ] Formule e notazione in LaTeX inline e display dove serve
- [ ] Niente moltiplicazioni misleading o numeri inventati (lezione di Review v3 di CAP-01)

## Out-of-scope — Development NON include queste cose in CAP-02

- Formule EGARCH, modello survival, feature engineering causale → Parti III-IV
- Operatori GA, fitness multi-obiettivo, walk-forward → Parte V
- Algoritmo concreto di pivot detection → Parte III (Cap 14)
- Setup tecnico API Directa, Telegram, Portara → Appendici C-E
- Parametri numerici congelati delle guardie e dei timer → Parte V

## Done when

Il documento risponde senza ambiguità a queste domande:
1. Cosa contiene esattamente un segnale emesso dal motore?
2. Quali stati può attraversare e con quali transizioni?
3. Sotto quali condizioni un raw touch della entry zone si traduce in segnale eseguito?
4. Come arriva il segnale al cellulare dell'operatore e cosa succede se cambiano le condizioni?
5. Come si ricostruisce deterministicamente il lifecycle di un segnale a partire dallo storico?

## Pipeline attesa

Stesso schema di CAP-01: Development scrive v1 → Review v1 audit ostile con classificazione GA → Supervisore decide cosa mandare a Development → Development v2 → Review v2 → … fino a PASS.

Promemoria operativo per Development: la lezione di CAP-01 è che il primo giro produce sistematicamente buchi semantici (definizioni divergenti dalla fonte) e aritmetici (numeri che non quadrano). Non temere il PASS al primo giro: la pipeline esiste perché i bug ci sono.
