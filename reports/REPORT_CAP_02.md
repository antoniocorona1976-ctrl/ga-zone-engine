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

---

## Iterazione 3 — Risposta ai finding di Review v2 + decisione supervisore Q-05

**Origine**: Review v2 ha emesso verdetto CONDITIONAL (B-3, B-4, NB-7, NB-8, NB-9, NB-10). La decisione del supervisore Q-05 (Opzione D raffinata, 2026-05-23) ha chiuso B-3 scegliendo la separazione segnale vs position lifecycle come soluzione architetturale, in luogo delle opzioni A/C/E valutate nel report di Review v2. B-4 era stato già chiuso dalla patch CAP-01 Iterazione 2 (commit `fc7531b`). I finding NB-7, NB-8, NB-9, NB-10 sono stati risolti chirurgicamente.

### Risposta per finding

| Finding | Azione applicata | Posizione in Parte II v3 |
|---------|-----------------|--------------------------|
| **B-3** (`target_1_hit` non-terminale formalmente) | Decisione Q-05 Clausola 1: `target_1_hit` reso veramente terminale, `target_2_hit` rimosso dalla state machine. La state machine ha 1 non-terminale + 6 terminali. | Cap.7.1 (stati), Cap.7.2 (tabella transizioni senza righe uscenti da `target_1_hit`), nota esplicita in Cap.7.1 e Cap.7.2. |
| **B-4** (incoerenza retroattiva CAP-01 vs Parte II v2) | Chiuso in commit `fc7531b` (patch CAP-01 Iterazione 2). La Parte II v3 è coerente con CAP-01 post-patch: cap 2gg dal raw touch, `executable_rate` ridefinita, nessun riferimento a "guardie di esecuzione". | Cap.6.1 ($\Delta t_{cromosoma}$ dal raw touch), Cap.8 (3 condizioni pre-emissione, no guardie). |
| **NB-7** (timer pre-trigger assente) | Introdotto $T_{touch}^{max} \in \{5, \ldots, 480\}$ minuti di trading come parametro libero del cromosoma. Scadenza assorbita nello stato terminale `expired` con causa `pretrigger_timeout` nel log (campo causale strutturato). | Cap.6.1 (campo $T_{touch}^{max}$ nel payload), Cap.7.1 (stato `expired` con due cause), Cap.7.2 (riga transizione `active → expired` con causa duplice), Cap.7.5 (sezione dedicata). |
| **NB-8** (edge case raw touch) | Trattati esplicitamente tre casi: (a) barra di emissione — raw touch valutato da $t_{emission}+1$; (b) gap overnight inside zone — raw touch sulla barra di apertura, fill al livello della zona più vicino all'open; (c) gap che allontana il prezzo dalla zona senza superarla — segnale resta `active`. | Cap.7.3 (sezione "Edge case del raw touch", tre sottoparagrafi etichettati (a), (b), (c)). |
| **NB-9** (transizione `target_1_hit → revoked` mancante) | Chiuso da solo per costruzione: con Q-05 `target_1_hit` è veramente terminale e non ammette transizioni uscenti verso alcuno stato. Esplicitato nel testo con nota dedicata. | Cap.7.1 (nota "chiusura NB-9"), Cap.7.2 (nessuna riga uscente da `target_1_hit`), Cap.6.3 (sostituzione applicata solo a segnali `active`). |
| **NB-10** ($\tau_{dist}$ con floor 80pt produce spazio nullo del GA) | Ridefinizione di $\tau_{dist}$ in sigma-units ($\tau_{dist}^{\sigma}$, numero puro). Il filtro 80pt resta come vincolo assoluto a valle, distinto dal parametro ottimizzabile. Nessun floor assoluto su $\tau_{dist}^{\sigma}$: il GA ha spazio pieno di ottimizzazione. | Cap.8.2 (terza condizione, formula in sigma-units), Cap.8.3 (congiunzione aggiornata con $E_{dist}^{\sigma}$ e $E_{80pt}$ separati). |
| **Q-05 Clausola 3** (Cap.11 nuovo) | Scritto ex-novo. Definisce la submacchina di position lifecycle come oggetto distinto. Citazioni testuali del baseline hard-locked: Cap. 21.1 e Cap. 22.6 di `ENGINE_ALGO_INTEGRATO_HARD_LOCKED.pdf`, verificate sul PDF. | Cap.11 (sezioni 11.1-11.5). |

### Decisioni rilevanti aggiuntive prese nell'Iterazione 3

**D-8. Payload esteso con $\Delta t_{cromosoma}$ e $T_{touch}^{max}$ come campi espliciti.** Il payload della tupla $\mathcal{S}$ in Cap.6.1 ora include esplicitamente entrambi i timer come campi del cromosoma. In v2, $\Delta t_{cromosoma}$ era implicito nel campo `expiry`; la v3 separa il parametro ottimizzabile ($\Delta t_{cromosoma}$) dal valore calcolato (`expiry`), che non è più nel payload (viene calcolato al momento del raw touch e comunicato nella notifica del `trigger_event`). Il campo `expiry` viene rimosso dalla tupla del payload e dal messaggio Telegram, dove non era pubblicabile in anticipo (decorre dal raw touch non ancora avvenuto): già la v2 aveva questo problema, ora esplicitato e risolto.

**D-9. Precisione sulla regola di sostituzione applicata solo ai segnali `active`.** Cap.6.3 precisa esplicitamente che la sostituzione si applica ai segnali in `active`; una volta transitato in qualunque stato terminale (incluso `target_1_hit`), il segnale non può essere revocato. Questo chiarisce la coerenza del vincolo $|\mathcal{A}(t)| \leq 1$: un segnale terminato non è "attivo" e non contribuisce al conteggio.

**D-10. Citazioni testuali del baseline verificate sul PDF.** Le citazioni di Cap. 21.1 e 22.6 del baseline `ENGINE_ALGO_INTEGRATO_HARD_LOCKED.pdf` sono state verificate per estratto diretto dal PDF usando `pdfplumber`. Il testo citato in Cap.11.1 è letterale e corrisponde esattamente al testo estratto (pagine 56 e 60 del PDF a 115 pagine totali). In particolare: (a) Cap. 21.1 pagina 56: "Il lifecycle della posizione oltre il fill è un sottosistema distinto e non va confuso con il lifecycle del contratto di segnale"; (b) Cap. 22.6 pagina 60: "La gestione fine dei partial fill viene trattata come submacchina della posizione e dunque come boundary del presente documento. [...] Il modo più semplice di rispettare il boundary è trattare il primo partial fill come passaggio del segnale in EXECUTED, spostando la gestione quantitativa della posizione in un sottosistema distinto."

**D-11. Adattamento delle citazioni al perimetro retail.** Le citazioni del baseline (Cap. 21.1, 22.6) fanno riferimento a un sistema con esecuzione automatica di ordini (fill, ORDER_WORKING, EXECUTED, partial fill). Nel presente motore il "fill" corrisponde al raw touch della entry zone (l'operatore esegue manualmente). L'adattamento è dichiarato esplicitamente in Cap.11.1: il boundary si applica con `target_1_hit` nel ruolo di `EXECUTED` del baseline. Questa riformulazione è fedele al principio metodologico ("sottosistemi distinti") e rispetta il perimetro retail ("no execution automatica").

### Misura prima/dopo dell'Iterazione 3

| Metrica del comportamento GA | v2 (post-Review v2) | v3 (Iterazione 3) | Delta |
|---|---|---|---|
| Stati terminali della state machine | 7 (`target_1_hit`, `target_2_hit`, `stopped`, `invalidated`, `missed_target`, `expired`, `revoked`) | 6 (`target_1_hit`, `stopped`, `invalidated`, `missed_target`, `expired`, `revoked`) — `target_2_hit` rimosso | -1 stato ambiguo; state machine formalmente consistente senza transizioni uscenti da terminali |
| Ambiguità formale `target_1_hit` | Terminale con transizione uscente verso `target_2_hit` (contraddizione formale, B-3) | Rigorosamente terminale, nessuna transizione uscente | Bug bloccante chiuso; ranking cromosomi non più influenzato da transizioni non specificate |
| Rischio strategia degenere "attesa indefinita" pre-trigger | Presente: segnale `active` senza timer pre-trigger | Eliminato: $T_{touch}^{max} \in \{5, \ldots, 480\}$ minuti di trading, scadenza in `expired` con causa `pretrigger_timeout` | +1 parametro del cromosoma; eliminazione del bias "emetti raramente, attendi sempre" |
| Spazio nullo del GA nella condizione di distanza | Intervallo $[0, 80]$ punti di $\tau_{dist}$ inattivo (mutazione GA senza variazione fitness) | Nessuno spazio nullo: $\tau_{dist}^{\sigma}$ in sigma-units, dominio pieno positivo, floor 80pt come vincolo separato | GA ha leva effettiva su tutta l'ottimizzazione della distanza; ridotto rischio di convergenza prematura |
| Edge case raw touch coperti dal contratto | 0 (barra emissione, gap overnight, gap beyond-zone non specificati) | 3 (tutti trattati con regola esplicita e deterministica) | Determinismo del replay garantito anche per i casi limite più frequenti in trading notturno/opening |
| Tracking post-target_1 | Assente nella Parte II; `target_2_hit` come stato del segnale | Submacchina distinta (Cap.11) con metriche $\pi_{t_2 \mid t_1}$, MFE, MAE, $f_{stop \mid t_1}$; OUT-OF-SCOPE dal motore | GA riceve feedback sulla qualità strutturale dei livelli target_2 senza espandere lo search space |
| Citazioni baseline hard-locked | Assenti (Cap.11 non esisteva) | Presenti e verificate: Cap. 21.1 e 22.6 del baseline | Tracciabilità formale con il documento di riferimento |
| Acceptance criteria soddisfatti | 14/14 con riserve su B-3, NB-7, NB-8, NB-9, NB-10 | 33/33 verificati puntualmente (vedi sezione "Acceptance criteria v3") | Tutti gli AC chiusi |

### Acceptance criteria v3 — verifica puntuale

| # | Criterio | Esito | Posizione |
|---|----------|-------|-----------|
| 1 | 6 capitoli (Cap 6-10 + Cap 11) presenti, completi, ordine corretto | OK | Sezioni `## Capitolo 6` … `## Capitolo 11` |
| 2 | 12 eredità (8 CAP-01 + 4 raffinamenti Iter.2/Q-05) citate esplicitamente | OK | Introduzione Parte II (tutte 10 eredità dell'ACTIVE_TASK citate); Cap.6.1 (banda discreta, $d_{stop}>b$, target 1+2, tick 5pt, $\Delta t_{cromosoma}$, $T_{touch}^{max}$, executable_rate); Cap.7.3 (raw touch sempre eseguibile); Cap.8.4 (sessione 8-22, no fasi speciali) |
| 3 | Cap 6: payload come tupla con tutti i campi e vincoli, target_2 obbligatorio | OK | Cap.6.1 (tupla con 10 campi inclusi $\Delta t_{cromosoma}$ e $T_{touch}^{max}$; target_2 obbligatorio con vincoli di ordinamento) |
| 4 | Cap 6: nota esplicita "target_2 informazione strutturale pubblicata, non variabile di lifecycle" | OK | Cap.6.1, campo `target_1` e `target_2`, nota esplicita con riferimento a Q-05 Clausola 2 e Cap.11 |
| 5 | Cap 6: entry_zone insieme discreto sul reticolo tick FIB (multipli di 5), $b \in \{5,…,40\}$ | OK | Cap.6.1, formula $\{p_{ref}-b, p_{ref}-b+5, \ldots, p_{ref}+b\}$, dominio $b \in \{5, 10, 15, 20, 25, 30, 35, 40\}$ |
| 6 | Cap 6: payload immutabile e regola sostituzione | OK | Cap.6.2 (immutabilità), Cap.6.3 (sostituzione, $|\mathcal{A}(t)| \leq 1$, applicata solo a `active`) |
| 7 | Cap 7: state machine 1 non-terminale + 6 terminali: `target_1_hit`, `stopped`, `invalidated`, `missed_target`, `expired`, `revoked`. `target_2_hit` RIMOSSO. | OK | Cap.7.1 (6 terminali elencati, `target_2_hit` assente), Cap.7.2 (tabella senza righe uscenti da terminali) |
| 8 | Cap 7: transizioni esplicite (tabella) con condizioni di trigger | OK | Cap.7.2 (tabella completa) |
| 9 | Cap 7: nota esplicita "target_2 dopo target_1 NON è transizione di stato del segnale ma evento del position lifecycle" | OK | Cap.7.1 (stato `target_1_hit`: "Il contratto del segnale si chiude definitivamente qui [...] Non è una transizione di stato del segnale ma un evento del position lifecycle (Cap.11)") |
| 10 | Cap 7: `invalidated` esplicita sotto-caso "stop_loss attraversato pre-touch" | OK | Cap.7.1 (definizione `invalidated`: "fra le condizioni esplicitamente incluse [...] il superamento del livello `stop_loss` [...] per i segnali long, $p(t) \leq \texttt{stop\_loss}$ con $t < t_{touch}$; simmetricamente per gli short") |
| 11 | Cap 7: `trigger_event` come evento, raw touch sempre eseguibile, nessun filtro post-emissione | OK | Cap.7.3 ("Il raw touch è sempre eseguibile: non esistono [...] guardie o filtri post-emissione che blocchino il trigger") |
| 12 | Cap 7: timer post-trigger 2gg trading dal raw touch, $\Delta t_{cromosoma} \in \{1,\ldots,1680\}$, esempio 21:55 | OK | Cap.7.4 (formula, dominio, esempio lunedì 21:55 → mercoledì 21:55) |
| 13 | Cap 7: timer pre-trigger $T_{touch}^{max} \in \{5,\ldots,480\}$, scadenza in `expired` con causa `pretrigger_timeout` | OK | Cap.7.5 (sezione dedicata), Cap.7.1 (stato `expired` con due cause), Cap.7.2 (transizione con causa duplice) |
| 14 | Cap 7: edge case raw touch trattati (barra emissione, gap inside zone, gap oltre zona) | OK | Cap.7.3 ("Edge case del raw touch", casi (a), (b), (c)) |
| 15 | Cap 7: M-1 trattato a livello di interfaccia con rinvio a Parte V per $N_{pivot}$ | OK | Cap.7.6 (contratto di osservazione, vincolo metodologico dichiarato, $N_{pivot}$ rinviato a Parte V) |
| 16 | Cap 8: 3 condizioni di emissione pre-emissione (volatilità, liquidità, distanza in sigma-units), spread eliminata con motivazione | OK | Cap.8.1 (motivazione filosofica, spread eliminata con ragione esplicita: no storico book in Portara/CQG), Cap.8.2 (3 condizioni) |
| 17 | Cap 8: $\tau_{dist}^{\sigma}$ in sigma-units, filtro 80pt come vincolo assoluto a valle | OK | Cap.8.2 (formula $|\texttt{target\_1} - p_{ref}| / \hat{\sigma} \geq \tau_{dist}^{\sigma}$), paragrafo successivo (filtro 80pt assoluto, non allentabile dal cromosoma) |
| 18 | Cap 8: rinvio a Parte V per soglie congelate, a Parte III per modello volatilità | OK | Cap.8.2 (EGARCH → Parte III, Cap.12; soglie → Parte V), Cap.8.3 |
| 19 | Cap 8: nessuna assunzione di fasi speciali nella sessione 8:00-22:00 | OK | Cap.8.4 (M-3 ritirato, FIB negozia in modo continuo) |
| 20 | Cap 9: politica anti-duplicato e "nuovo messaggio per nuovo signal_id" (mai edit) | OK | Cap.9.4 (anti-duplicato), Cap.9.5 (nuovo messaggio separato, motivazione immutabilità) |
| 21 | Cap 9: notifica `trigger_event` come messaggio separato | OK | Cap.9.5 (notifica come messaggio separato, con $t_{exec}$ e `expiry` calcolata) |
| 22 | Cap 10: log di emissione include snapshot delle 3 condizioni di emissione | OK | Cap.10.2 (3 condizioni + filtro 80pt, con valori e soglie) |
| 23 | Cap 10: log delle transizioni registra $t_{exec}$ del raw touch come riferimento timer post-trigger | OK | Cap.10.3 ("`trigger_event` [...] registrato nel log [...] in particolare l'istante $t_{exec}$ da cui decorre il timer post-trigger $\Delta t_{cromosoma}$") |
| 24 | Cap 10: requisito di determinismo bit-exact dichiarato come vincolo formale | OK | Cap.10.1 (formula $\forall H, \forall B: \texttt{replay}(H, B) = \texttt{replay}(H, B)$ bit-exact) |
| 25 | Cap 11: definisce submacchina position lifecycle come oggetto distinto dal lifecycle del segnale | OK | Cap.11.1 (separazione formale), Cap.11.3 (struttura della submacchina) |
| 26 | Cap 11: OUT-OF-SCOPE dal motore (execution policy, scaling-out, trailing stop, dynamic sizing) | OK | Cap.11.2 (sezione "OUT-OF-SCOPE dal motore" con lista esplicita e riferimento punto 8 dichiarazione) |
| 27 | Cap 11: IN-SCOPE per reporting (metriche $\pi_{t_2 \mid t_1}$, MFE, MAE, eventi post-target_1) | OK | Cap.11.2 (sezione "IN-SCOPE per reporting e validazione") |
| 28 | Cap 11: submacchina NON modifica stato del segnale | OK | Cap.11.3 ("la submacchina non modifica lo stato del segnale in nessuna circostanza") |
| 29 | Cap 11: citazioni testuali baseline Cap. 21.1 e 22.6 | OK | Cap.11.1 (citazioni letterali verificate sul PDF, con attribuzione esplicita alle sezioni e al file) |
| 30 | Cap 11: search space del cromosoma GA non esteso | OK | Cap.11.4 ("Lo space search del cromosoma del GA non viene esteso. Nessuna policy decisionale post-target_1 entra nel cromosoma") |
| 31 | Registro tecnico italiano formale | OK | Tutto il documento |
| 32 | Formule e notazione LaTeX inline e display | OK | Cap.6.1, Cap.7.2, Cap.7.4, Cap.8.2, Cap.8.3, Cap.10.1 |
| 33 | Tick FIB = 5pt rispettato in ogni esempio numerico | OK | Cap.6.1 (banda discreta multipli di 5), Cap.7.4 (esempio 21:55 in minuti), valori provvisori qualificati come tali |

### Criterio di rollback aggiornato per l'Iterazione 3

7. Se la state machine ridotta a 6 terminali (senza `target_2_hit`) si rivela insufficiente in Parte V perché il GA non riesce a calcolare `target_2_hit_rate` come metrica fold-by-fold senza uno stato dedicato nel segnale, si rivaluta l'opzione di registrare `target_2_reached` come campo del log di chiusura `target_1_hit` (campo booleano `target_2_reached_after_t1`). Questa revisione è puntuale su Cap.10.4 e non richiede nuovi stati nella state machine.
8. Se il dominio $\{5, \ldots, 480\}$ minuti di $T_{touch}^{max}$ si rivela subottimale (troppo stretto o troppo largo) sulla base delle distribuzioni empiriche dei tempi di primo tocco sullo storico FIB, il dominio va ricalibrato in Parte V. La revisione è puntuale su Cap.6.1 e Cap.7.5, senza impatto sull'architettura del contratto.
9. Se le citazioni del baseline (Cap. 21.1 e 22.6) vengono aggiornate in una versione successiva del documento `ENGINE_ALGO_INTEGRATO_HARD_LOCKED.pdf`, le citazioni di Cap.11.1 devono essere ricontrollate e aggiornate contestualmente. Il riferimento al file e alle sezioni è tracciato esplicitamente.

---

## Iterazione 4 — mini-patch Cap.8.2 cross-ref Cap.13

**Origine**: NB-3 di Review v1 CAP-03 ha identificato due errori in Cap.8.2 Parte II: (a) il riferimento "Parte III Cap.12" era errato (il modello EGARCH e in Cap.13, non Cap.12); (b) le formule delle condizioni di emissione usavano sigma_hat in unita di log-return anziche sigma_hat_pt in punti FIB, rendendo il rapporto non adimensionale.

### Modifiche applicate

| Posizione | Prima | Dopo |
|-----------|-------|------|
| Cap.8.2, formula condizione volatilita, testo esplicativo | "...sigma_hat(t_emission) e la stima di volatilita... (Parte III, Cap.12)..." | "...sigma_hat_pt(t_emission) e la stima di volatilita convertita in punti FIB secondo sigma_hat_pt = sigma_hat * p_t (Parte III, Cap.13)..." |
| Cap.8.2, formula condizione distanza, numeratore e denominatore | "|target_1 - p_ref| / sigma_hat(t_emission)" | "|target_1 - p_ref| / sigma_hat_pt(t_emission)" |
| Cap.8.2, formula condizione distanza, testo esplicativo | "...sigma_hat(t_emission) e la stima... (Parte III, Cap.12)..." | "...sigma_hat_pt(t_emission) e la stima convertita in punti FIB... (Parte III, Cap.13)..." |
| Cap.8.3, riga finale | "...formule del modello di volatilita che alimentano sigma_hat sono in Parte III, Cap.12" | "...formule del modello di volatilita che alimentano sigma_hat_pt e la conversione in punti FIB sono in Parte III, Cap.13" |

### Misura prima/dopo

| Metrica | Prima | Dopo | Delta |
|---------|-------|------|-------|
| Cross-ref corretto (Cap.12 vs Cap.13) | Errato (Cap.12) | Corretto (Cap.13) | Bug di riferimento chiuso |
| Rapporto in condizione distanza adimensionale | No (sigma in log-return vs target in punti) | Si (sigma_pt in punti FIB vs target in punti) | Implementabilita univoca garantita |

### Criterio di rollback
Non applicabile: la correzione e fattuale (il modello EGARCH e effettivamente in Cap.13, non Cap.12) e la conversione sigma_hat_pt e richiesta per la coerenza dimensionale. Non vi e ambiguita metodologica.

---

## Iterazione 5 — fix Review v3 (NB-3 formula $\hat{\sigma}_{pt}$, NB-1/NB-2 cross-reference)

**Origine**: Review v3 ha emesso verdetto CONDITIONAL con 3 finding approvati dal supervisore. I fix sono chirurgici: 1-2 simboli o parole per finding.

### Modifiche applicate

| Finding | Posizione | Prima | Dopo |
|---------|-----------|-------|------|
| **NB-3** (BUG: formula display condizione volatilità usa $\hat{\sigma}$ invece di $\hat{\sigma}_{\text{pt}}$) | Cap.8.2, formula display `$$r_{1m}(t_{emission}) \leq \tau_{vol}(\ldots)$$` | `\hat{\sigma}(t_{emission})` come argomento di $\tau_{vol}$ | `\hat{\sigma}_{\text{pt}}(t_{emission})` come argomento di $\tau_{vol}$ |
| **NB-1** (MIGLIORA PERF: cross-reference pivot detection errato "Cap.14" → "Cap.15") | Cap.7.6, frase di rinvio all'algoritmo di pivot detection | "materia di Parte III (Cap.14)" | "materia di Parte III (Cap.15)" |
| **NB-2** (MIGLIORA PERF: cross-reference invalidazione strutturale "Parte IV (Cap.15)") | Cap.7.1 definizione `invalidated` | "demandata a Parte IV (Cap.15)" | "demandata a Parte IV" |
| **NB-2** (MIGLIORA PERF: cross-reference invalidazione strutturale "Parte IV (Cap.15)") | Cap.7.2 tabella transizioni, riga `active → invalidated` | "(Parte IV, Cap.15)" | "(Parte IV)" |

### Misura prima/dopo

| Metrica | Prima | Dopo | Delta |
|---------|-------|------|-------|
| Coerenza dimensionale formula display condizione volatilità | Incoerente: $\hat{\sigma}$ (log-return, ordine $10^{-4}$) come argomento di $\tau_{vol}$ mentre $r_{1m}$ è in punti FIB | Coerente: $\hat{\sigma}_{\text{pt}}$ (volatilità in punti FIB) come argomento di $\tau_{vol}$ | Bug dimensionale chiuso; formula display allineata al testo esplicativo che già usava $\hat{\sigma}_{\text{pt}}$ |
| Correttezza cross-reference pivot detection | Errato: Cap.14 = "Stato di regime intraday" | Corretto: Cap.15 = "Feature engineering causale" (contiene §15.3 pivot detection) | Riferimento punta al capitolo corretto |
| Correttezza cross-reference invalidazione strutturale (Cap.7.1) | Errato: "Parte IV (Cap.15)" — Cap.15 è in Parte III | Corretto: "Parte IV" senza numero di capitolo (assegnato quando Parte IV sarà pianificata) | Eliminato riferimento a capitolo inesistente in Parte IV |
| Correttezza cross-reference invalidazione strutturale (Cap.7.2) | Errato: "(Parte IV, Cap.15)" | Corretto: "(Parte IV)" | Coerenza con la correzione applicata in Cap.7.1 |

### Criterio di rollback
Non applicabile: tutti e tre i fix sono correzioni fattuali di simboli e numeri di capitolo errati. Non vi è ambiguità metodologica. Se il numero di capitolo della sezione su invalidazione strutturale in Parte IV verrà assegnato, il riferimento in Cap.7.1 e Cap.7.2 dovrà essere aggiornato aggiungendo il numero corretto (aggiornamento puntuale, non rollback).

