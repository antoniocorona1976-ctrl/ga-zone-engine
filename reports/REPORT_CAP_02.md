### REPORT SUPERVISORE — CAP-02
**Task**: Parte II del documento metodologico v2 — Contratto del segnale FIB
**Stato**: COMPLETATO Iterazione 2 — TASK PRONTO PER REVIEW v2

#### Cosa è stato prodotto
- `docs/methodology_v2/CAP_02_parte_II.md` — Parte II, 5 capitoli (Cap.6 schema e invarianti; Cap.7 state machine; Cap.8 guardie di esecuzione; Cap.9 politica Telegram; Cap.10 replay e riproducibilità). Italiano formale, LaTeX inline e display, ~10 pagine equivalenti.

#### Ipotesi di partenza
Il contratto del segnale è il punto in cui il GA passa da "ottimizzazione astratta di una funzione di fitness" a "decisione operativa che produce un payload immutabile sul cellulare dell'operatore". Una definizione imprecisa del contratto produce: (a) cromosomi che ottimizzano segnali non azionabili (es. payload con campi mancanti, o con stop loss strutturalmente incompatibile con la banda); (b) ranking distorto dei cromosomi per via di una state machine che ammette transizioni ambigue (es. confusione fra "executable", "executed", "active" che inquina la conversione signal-to-trade); (c) impossibilità di calcolare metriche di lifecycle deterministiche, e quindi di usarle come gate decisionali (Parte VII).

L'obiettivo del comportamento GA che CAP-02 vuole influenzare è triplice. (1) Forzare il GA a ottimizzare cromosomi che producono segnali completi (tutti i nove campi della tupla $\mathcal{S}$ definiti) e geometricamente validi ($d_{stop} > b$ e cap 2 giorni di trading). (2) Costringere il GA a confrontarsi con la regola di sostituzione: emettere un nuovo `signal_id` ha un costo (canale Telegram, log, lifecycle interrotto) e il cromosoma deve giustificarlo con miglioramento atteso. (3) Rendere le quattro guardie di esecuzione (volatilità, spread, liquidità, distanza target) parametri liberi del cromosoma e quindi leva diretta del GA sulla conversione signal-to-trade.

#### Decisioni rilevanti prese durante lo sviluppo

**D-1. Stato `active` unico non-terminale, niente `executable`/`executed`.** L'indice originale (00_indice.md riga 18) elencava stati "emitted, executable, executed, target_hit, invalidated, missed_target, expired". Il task ACTIVE_TASK ha chiesto invece 1 solo non-terminale (`active`) + 7 terminali (`target_1_hit`, `target_2_hit`, `stopped`, `invalidated`, `missed_target`, `expired`, `revoked`). Ho seguito il task. Motivazione strutturale (Cap.7.3): il motore non esegue ordini (vincolo punto 1 dichiarazione, ereditato da CAP-01) e non osserva il fill manuale dell'operatore sul broker Directa, quindi uno stato `executed` distinto da `active` richiederebbe una conferma di fill che non rientra nel perimetro del sistema. Il `trigger_event` è degradato a evento notificato, non stato.

**D-2. `target_2_hit` come transizione successiva ammessa da `target_1_hit`.** La state machine richiesta era "1 non-terminale + 7 terminali" ma `target_2_hit` succede sequenzialmente a `target_1_hit`. Ho risolto introducendo l'eccezione esplicita in Cap.7.2 (asterisco nella tabella): `target_1_hit` è terminale per il log di chiusura ma ammette la sola transizione `target_2_hit` per registrare il secondo target. Alternativa scartata: rendere `target_1_hit` non-terminale, che avrebbe contraddetto la specifica del task ("1 stato non-terminale").

**D-3. Timer expiry su barra 1-min e calendario di trading.** Ho specificato (Cap.7.4) che $\texttt{expiry} = \texttt{timestamp\_emission} + \Delta t_{cromosoma}$ con $\Delta t_{cromosoma} \in (0, 2]$ giorni di trading, valutato a ogni barra 1-min, sul calendario di trading (non solare) ovvero unione delle finestre 8:00-22:00 CET. Questa è una concretizzazione che il task chiedeva esplicitamente ("timer concreto, non prosa generica").

**D-4. Trattamento M-1 come contratto di osservazione, non algoritmo.** M-1 carryover da CAP-01 chiedeva di trattare l'identificazione real-time del primo pivot strutturale post-apertura. L'algoritmo concreto è materia di Parte III (Cap.14). Ho introdotto in Cap.7.5 un contratto di osservazione: cadenza barra 1-min, vincolo che la regola di pivot detection scelta in Parte III non introduca ritardo tale da rendere inattiva la finestra iniziale di sessione 8:00-22:00 (altrimenti l'ancoraggio del target 70% al primo pivot deciso in CAP-01 viene vanificato).

**D-5. Parametri provvisori delle guardie e della latenza dichiarati come tali, niente numeri inventati.** Le quattro soglie $\tau_{vol}, \tau_{spread}, \tau_{liq}, \tau_{dist}$ sono dichiarate parametri liberi del cromosoma e congelate in Parte V. La latenza massima Telegram $L_{max}$ ha un valore di lavoro provvisorio (30 secondi) esplicitamente dichiarato come tale e rinviato a Parte V/Appendice E. Stesso trattamento per $n_{retry} = 3$ e $\Delta t_{retry} = 2$ s in 9.6. Lezione esplicita di Review v3 di CAP-01: niente numeri congelati dentro la Parte II.

**D-6. Politica di pubblicazione coerente con invariante di immutabilità.** Cap.9.5: nuovo segnale = nuovo messaggio Telegram, mai edit del precedente. Motivazione strutturale: editare il messaggio del segnale precedente equivarrebbe a modificare il payload pubblicato, violando la regola di Cap.6.2.

**D-7. Determinismo del replay come vincolo formale.** Cap.10.1: dichiarato come $\forall H, \forall B: \texttt{replay}(H, B) = \texttt{replay}(H, B)$ bit-exact, con esplicitazione che generatori pseudo-casuali devono essere seedati e il seed è parte del bundle. Il task chiedeva esplicitamente "vincolo, non desiderio".

#### Misura prima/dopo

| Metrica del comportamento GA | Prima di CAP-02 (CAP-01 chiuso) | Dopo CAP-02 | Delta |
|---|---|---|---|
| Stati non-terminali della state machine | 3 (indice originale: emitted, executable, executed) | 1 (solo `active`) | -2 stati ambigui rispetto al perimetro "no execution" |
| Stati terminali della state machine | 4 (target_hit unico, invalidated, missed_target, expired) | 7 (target_1_hit, target_2_hit distinti; stopped esplicito; revoked introdotto) | +3 stati che producono metriche di lifecycle distinguibili per il GA |
| Vincoli di ammissibilità del cromosoma del segnale | 2 (banda $b \in [b_{min}, 40]$, $d_{stop} > b$) | 5 (banda, $d_{stop} > b$, target_1 e target_2 obbligatori e ordinati, $\Delta t_{cromosoma} \leq 2$ gg trading, filtro 80pt direzionale o trade_range) | +3 vincoli che filtrano cromosomi non emettibili prima del backtest, riducendo evaluation sprecate |
| Parametri liberi del cromosoma derivati dalle guardie | 0 (guardie non formalizzate in CAP-01) | 4 ($\tau_{vol}, \tau_{spread}, \tau_{liq}, \tau_{dist}$) | +4 leve dirette del GA sulla conversione raw-touch → trigger_event |
| Regola di sostituzione | implicita (CAP-01 menzionava "revisione continua") | esplicita: revoca + nuovo signal_id + segnale unico attivo $|\mathcal{A}(t)| \leq 1$ | +1 vincolo che riduce il dominio del GA dalle politiche multi-segnale concorrente a sequenze di segnali singoli sostituiti |
| Determinismo del replay | richiesto implicitamente da metriche OOS di CAP-01 | dichiarato come vincolo formale bit-exact con seed parte del bundle | +1 condizione necessaria per valore probatorio dei gate Parte VII |

#### Acceptance criteria — verifica puntuale

| # | Criterio | Esito | Posizione |
|---|----------|-------|-----------|
| 1 | I 5 capitoli (Cap 6-10) presenti, completi, ordine corretto | OK | Sezioni `## Capitolo 6` … `## Capitolo 10` |
| 2 | 8 eredità CAP-01 citate esplicitamente | OK | Sessione 8-22 (Cap.6 intro, Cap.7.4, Cap.8.4, Cap.10.5); banda (Cap.6.1); $d_{stop}>b$ (Cap.6.1); target 1+2 (Cap.6.1); $\leq$ 2gg trading (Cap.6.1, Cap.7.4); movimento strutturale primo pivot (Cap.7.5); filtro 80pt (Cap.6.1); no execution (Cap.7.3) |
| 3 | Cap 6: payload come tupla, tutti i campi, vincoli (banda, $d_{stop}>b$, expiry $\leq$ 2gg, $\geq$ 80pt target_1) | OK | Cap.6.1 |
| 4 | Cap 6: payload immutabile + regola sostituzione (revoca + nuovo signal_id, segnale unico attivo) | OK | Cap.6.2 e Cap.6.3 |
| 5 | Cap 7: 1 stato non-terminale + 7 terminali + transizioni esplicite + trigger_event come evento | OK | Cap.7.1 (stati), Cap.7.2 (tabella transizioni), Cap.7.3 (trigger_event come evento) |
| 6 | Cap 7: cap 2gg trading come timer concreto | OK | Cap.7.4 (formula + valutazione a ogni barra 1-min + calendario di trading) |
| 7 | Cap 7: M-1 a livello di interfaccia | OK | Cap.7.5 |
| 8 | Cap 8: 4 guardie nominate + rinvio Parte V soglie | OK | Cap.8.2 (volatilità, spread, liquidità, distanza target_1) + Cap.8.3 (rinvio Parte V) |
| 9 | Cap 8: nessuna assunzione fasi speciali (M-3 ritirato) | OK | Cap.8.4 esplicito |
| 10 | Cap 9: anti-duplicato + nuovo messaggio per nuovo signal_id coerente con sostituzione (no edit) | OK | Cap.9.4 (anti-duplicato), Cap.9.5 (no edit) |
| 11 | Cap 10: determinismo del replay come vincolo, non desiderio | OK | Cap.10.1 formula bit-exact |
| 12 | Registro tecnico italiano formale | OK | tutto il documento |
| 13 | LaTeX inline e display | OK | Cap.6.1 (entry_zone, $d_{stop}$, expiry, filtri), Cap.6.3 ($|\mathcal{A}(t)|\leq 1$), Cap.7.4 (expiry), Cap.8.2 (4 guardie), Cap.10.1 (replay bit-exact) |
| 14 | Niente moltiplicazioni misleading o numeri inventati | OK | i pochi valori numerici dichiarati ($L_{max}=30$s, $n_{retry}=3$, $\Delta t_{retry}=2$s) sono qualificati come "provvisorio congelato in Parte V" |

#### Domande aperte per il Planner
Nessuna. Tutti i punti del task sono stati indirizzati con materiale interno alla Parte II o con rinvii espliciti alle parti pertinenti del documento (Parti III, IV, V, VI, VII; Appendici B, C, D, E).

#### Criterio di rollback
1. Se la state machine a 1 non-terminale + 7 terminali si rivela inadeguata in Parte III/V perché il GA non riesce a separare la conversione signal-to-trade dal raggiungimento del target — ovvero se il `trigger_event` come evento (non stato) impedisce di costruire una metrica di lifecycle riferita agli "eseguiti virtuali" coerente con la metrica primaria $E[R_{net}\mid executed]$ di CAP-01 — si reintroduce uno stato `triggered` non-terminale fra `active` e gli stati terminali post-raw-touch. La revisione è puntuale su Cap.7 e Cap.10, non richiede riscrittura.
2. Se in Parte V le quattro guardie con parametri indipendenti producono una crescita combinatoria del genoma tale da rendere il GA non addestrabile sul compute budget di CAP-01 (45-75 EUR a retraining), si valuta di accorpare due o più guardie sotto un'unica soglia composita (es. guardia di "qualità della barra" che integra volatilità+volume).
3. Se la regola di sostituzione con segnale unico attivo $|\mathcal{A}(t)|\leq 1$ produce, in backtest OOS, un tasso di sostituzione superiore al 50% dei segnali emessi (cromosomi che sostituiscono troppo), il vincolo va integrato con una penalità nel fitness multi-obiettivo (Parte V, Cap.23). Questa è ottimizzazione del GA, non rollback strutturale del contratto.
4. Se la latenza $L_{max} = 30$ s provvisoria si rivela non realistica in Appendice E (verifica empirica del canale Telegram), il valore va aggiornato in Parte V. L'aggiornamento è puntuale su Cap.9.3, non richiede riscrittura della Parte II.

---

## Iterazione 2 — Risposta ai finding di Review v1 + rifondazione architettura Cap.8

**Origine**: Review v1 ha emesso verdetto CONDITIONAL (2 B + 6 NB + 3 N + 2 M). Durante la discussione con il supervisore per chiudere i finding sono emerse due decisioni strutturali che hanno richiesto una riscrittura integrale della Parte II, non un semplice patch:

1. **Chiarificazione semantica del cap 2 giorni di trading** (decisione del supervisore): il timer di validità di 2gg trading decorre dal raw touch (esecuzione), non dal `timestamp_emission`. La Parte II originale assumeva la decorrenza dall'emissione.
2. **Rifondazione del Cap.8** (decisione del supervisore in risposta a verifica metodologica): le "guardie di esecuzione al raw touch" come parametri liberi del cromosoma erano architettonicamente errate per tre ragioni: (a) la guardia di spread richiedeva storico di book non disponibile nei dati Portara/CQG pianificati in CAP-01; (b) i filtri post-emissione che bloccano il trigger contraddicono il principio "il motore emette segnali, l'esecuzione è dell'operatore" (punto 1 dichiarazione di intenti); (c) il raw touch deve essere sempre eseguibile, le condizioni di mercato vanno valutate prima dell'emissione, non dopo. Il Cap.8 è stato riscritto come "Condizioni di emissione del segnale" con tre condizioni pre-emissione (volatilità, liquidità, distanza dal target_1), eliminando la guardia di spread.

**Chiusura dei finding di Review v1**:

| Finding | Decisione applicata | Posizione in Parte II v2 |
|---------|---------------------|--------------------------|
| **B-1** (stop pre-touch non coperto) | C1: sotto-caso di `invalidated`, esplicitato nel testo. Decisione supervisore. | Cap.7.1 (definizione `invalidated` con condizione $p(t) \leq \texttt{stop\_loss}$ per long, simmetrica per short), Cap.7.2 (riga della tabella). 7 stati invariati. |
| **B-2** (contraddizione missed_target) | Cade da sola con la nuova architettura: "raw touch eseguibile" non esiste più come concetto distinto da "raw touch". Decisione supervisore: raw touch sempre eseguibile. | Cap.7.3, Cap.8.4. |
| **NB-1** (asimmetria missed_target_2) | (a) motivare nel testo richiamando Q-03 CAP-01. | Cap.7.1, definizione `missed_target`. |
| **NB-2** (granularità $\Delta t_{cromosoma}$) | (a) intero in minuti di trading, dominio $\{1, \ldots, 1680\}$. | Cap.7.4. |
| **NB-3** ($N_{pivot}$ vago) | (c) rinvio a Parte V con misura empirica sullo storico, vincolo metodologico dichiarato in Parte II. | Cap.7.5. |
| **NB-4** (caso emissione 21:55) | (a) counter in minuti di trading scavalcando interruzioni, con esempio numerico. | Cap.7.4. |
| **NB-5** (direzione raw touch) | Riformulazione corretta: il raw touch non impone direzione di provenienza; il prezzo entra nella zona da qualsiasi direzione. Tick discreto FIB=5pt esplicitato come fatto strutturale. | Cap.7.3, Cap.6 introduzione, Cap.6.1 (banda discreta multiplo di 5). |
| **NB-6** (citazione M-3 errata) | Sostituzione: "ha ritirato l'osservazione M-3" anziché "decisione del supervisore in chiusura M-3". | Cap.8.4. |
| **N-1, N-2, N-3** | Carryover legittimo, no rework su CAP-02. | Riferimenti rispettivamente a Parte V (fitness), Parte VII (gate), Parte V/VI (nomenclatura). |
| **M-1, M-2** | Carryover legittimo. | Riferimenti a Parte III/Cap.14 e Appendice E. |

**Decisioni strutturali aggiuntive dell'Iterazione 2**:

- **Tick FIB = 5 punti formalizzato come fatto strutturale dello strumento.** Il documento originale ignorava la discretizzazione e usava esempi con bordi di zona non multipli di 5. Iterazione 2 esplicita il tick nell'introduzione di Parte II e nel Cap.6.1, e modifica la definizione della banda di ingresso da intervallo continuo $[p_{ref}-b, p_{ref}+b]$ a insieme discreto $\{p_{ref}-b, p_{ref}-b+5, \ldots, p_{ref}+b\}$, con dominio di $b$ ridefinito come $\{5, 10, 15, 20, 25, 30, 35, 40\}$ (8 valori discreti, cardinalità 8 anziché continuo).
- **Cap.8 ricostruito come "Condizioni di emissione del segnale".** Tre condizioni pre-emissione (volatilità del minuto, liquidità del minuto, distanza strutturale $p_{ref}$ → target_1) con soglie come parametri liberi del cromosoma. Spread eliminata in quanto non addestrabile (no storico di book in Portara/CQG). Una sezione introduttiva 8.1 esplicita la filosofia: condizioni pre-emissione, raw touch sempre eseguibile, autonomia di esecuzione dell'operatore.
- **Notifica `trigger_event` aggiunta al protocollo Telegram di Cap.9.5.** Coerentemente con il raw touch come evento di esecuzione, il motore pubblica una notifica separata al `trigger_event`. Distinta dal messaggio di emissione.

**Misura prima/dopo dell'Iterazione 2**:

| Metrica del comportamento GA | v1 (post-Review v1) | v2 (Iterazione 2) | Delta |
|---|---|---|---|
| Parametri liberi del cromosoma per filtri di mercato | 4 (volatilità, spread, liquidità, distanza) | 3 (volatilità, liquidità, distanza) | -1 (spread eliminata) — riduzione dello spazio di ricerca, riduzione del rischio di overfitting su parametri non addestrabili |
| Architettura dei filtri | post-emissione al raw touch (guardie che bloccano il trigger) | pre-emissione (condizioni di valutazione dell'emissione); raw touch sempre eseguibile | cambio di paradigma — coerenza con punto 1 dichiarazione e con dati disponibili in storico FIB |
| Cardinalità del dominio di $b$ | implicita continua su $[5, 40]$ | esplicitamente discreta $\{5, 10, 15, 20, 25, 30, 35, 40\}$ — 8 valori | da continuo a 8 valori: GA mutation discreta sul reticolo del tick FIB |
| Cardinalità del dominio di $\Delta t_{cromosoma}$ | non specificata (NB-2 originale) | $\{1, \ldots, 1680\}$ minuti di trading | dominio dichiarato, GA può applicare mutazione discreta su intero |
| Stati terminali della state machine | 7 (con bug B-1 aperto: stop pre-touch non coperto) | 7 (B-1 chiuso come sotto-caso esplicito di `invalidated`) | bug chiuso senza aggiungere stati |
| Decorrenza del timer `expiry` | dall'emissione | dal raw touch (esecuzione) — chiarificazione supervisore | semantica corretta del cap 2gg trading |
| Notifica al raw touch | implicita | esplicita come messaggio Telegram separato | tracciabilità operatore: distinzione fra emissione e trigger |

**Punti aperti rinviati esplicitamente a decisione successiva**:

1. **Patch CAP-01 (riga 13)**: la chiarificazione semantica del cap 2gg richiede una mini-patch in CAP-01 per coerenza retroattiva. Non eseguita in questa iterazione: il supervisore deve decidere se applicarla con o senza passaggio in Review. Parte II v2 è autoconsistente.
2. **Tema separato `time_to_touch_max`**: durante la discussione è stato aperto il tema di un timer di attesa pre-trigger come "mix punti × tempo gestibile", per evitare segnali in attesa indefinita del raw touch. Non incluso in Parte II v2 per scelta del supervisore di chiudere prima i finding di Review v1. Rimane in tavola come tema di Parte II v3 se il supervisore lo riterrà necessario.
3. **Vincolo di coerenza distanze geometriche ↔ volatilità**: principio metodologico emerso nella discussione (le distanze entry-stop-target dovrebbero essere coerenti con la volatilità corrente). Non formalizzato in Parte II v2: la decisione su dove introdurlo (Parte II vincolo di alto livello, oppure Parte IV materia di geometria delle zone) spetta al supervisore.

**Criterio di rollback aggiornato per l'Iterazione 2**:

5. Se in Parte V emerge che la condizione di distanza dal target_1 come parametro libero del cromosoma di emissione è ridondante con il vincolo geometrico di Parte IV (target/stop strutturalmente coerenti con $\hat{\sigma}$), la condizione va eliminata da Cap.8 e demandata a Parte IV. La revisione è puntuale su Cap.8.2 (terza condizione) e su Cap.8.3 (rimozione del termine corrispondente dalla congiunzione logica), non richiede riscrittura della Parte II.
6. Se in misura empirica sullo storico FIB risulta che la condizione di liquidità con soglia $\tau_{liq}$ libera converge sistematicamente a valori prossimi a zero (il GA disattiva di fatto la condizione), la condizione va eliminata da Cap.8 e demandata a Parte V come scelta meta-cromosoma. Revisione puntuale.
