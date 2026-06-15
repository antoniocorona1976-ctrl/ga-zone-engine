# TASK ATTIVO: SPEC-FUNZ-01-B2 — Payload del segnale (ricostruzione cieca, modalità B, blocco 2/8)

## Finding di Review da risolvere (micro-pass, approvato dal supervisore 2026-06-15)

> Re-apertura del solo blocco B2 dopo Review PASS `079552c`, per correggere **1 finding NEUTRO** che il supervisore ha deciso di instradare. **Niente altro va toccato**: nessun nuovo requisito, nessuna ri-numerazione, nessun cambio di contenuto/tracciabilità/cecità. Solo la correzione editoriale sotto. Dopo il fix → re-review leggera → ri-chiusura sul nuovo SHA.

- **OM-1 (NEUTRO — cross-reference interno rotto)**: in `docs/spec_funzionale/SPEC_FUNZ_01_B2.md` due rinvii a B2-CN-01 puntano a **§3.10** (che è la sezione dei campi-timer $\Delta t_{cromosoma}/T_{touch}^{max}$), mentre **B2-CN-01 è definito sotto §8.1** (blocco invariante subito dopo la matrice di tracciabilità). Correggere `§3.10` → `§8.1` nei **due** punti:
  1. riga ~159: `*(Il vincolo geometrico $d_{stop}>b$ è reso come requisito invariante — vedi B2-CN-01 al §3.10.)*`
  2. riga ~298 (cella della matrice §8.1, riga `B2-CN-01`): `... (vedi §3.10) ...`
  - Nessun'altra modifica. Il contenuto di B2-CN-01, la sua tracciabilità (`:47, :49`) e tutto il resto restano invariati.

---

> **Track**: Business-spec (SPEC-FUNZ). **Sede**: CLI per tutto il ciclo (GOV-SURFACES-01, METODO §Superfici). **Tag commit**: `[SPEC-FUNZ-01-B2]`. Tutto su `main` (trunk); isolamento via cartella dedicata, non via branch.
>
> **Letture obbligatorie del Developer, in quest'ordine, PRIMA di scrivere**: `tasks/METODO.md` (RM-1..RM-4 + RACC-METODO-2), `.claude/BASE_COMUNE.md` (ciclo, sede CLI per la spec, onestà claim→evidenza), `.claude/agents/spec_developer.md` (il tuo ruolo), questo `tasks/ACTIVE_TASK.md`. **Conferma in testa al REPORT di averli letti** (formato richiamato anche al §5).

---

## 0. Natura del blocco e modalità di lavoro (LEGGERE PRIMA DI TUTTO)

Questo è il **secondo** di **8 blocchi** (B1→B8) in cui la business-spec del progetto viene **ricostruita ex-novo**, **uno alla volta**. Ogni blocco = un ciclo Planner→Developer→Reviewer = un PASS. Gli 8 documenti, a fine serie (dopo B8), verranno ricomposti in un'unica spec consolidata da un **task di assemblaggio dedicato**: l'assemblaggio è **FUORI SCOPE di B2** (non eseguirlo, non anticiparlo). B1 (Ambito & operatore) è già **CHIUSO PASS** (`7195ffe`); B2 ne è la prosecuzione e **non ridefinisce** ciò che B1 ha già consolidato (ambito, operatore, strumento, vincolo solo-emissione, canale a livello di ambito): se un fatto di ambito ti serve come premessa, lo **citi dal CAP-fonte** (non da B1, che non devi aprire — vedi §0.1).

### 0.1 — VINCOLO DI CECITÀ (cardine della modalità B — leggere con la massima attenzione)

Tu (Developer) costruisci i requisiti di B2 **DAI SOLI capitoli pertinenti del CAP-fonte** elencati al §1, **cieco** rispetto a qualsiasi specifica funzionale già esistente e rispetto ai blocchi B1/B3..B8 già o non ancora prodotti. È **TASSATIVAMENTE VIETATO** aprire, leggere, consultare, citare o parafrasare:

1. `docs/spec_funzionale/SPEC_FUNZ_01.md` (la spec v2 congelata, PASS `ab7450f`) e qualsiasi file `*_v1_storico*`;
2. qualunque file di **pianificazione/chunking** del track business-spec (es. `PROPOSTA_SUDDIVISIONE_SPEC*.md`): contengono la mappa dei requisiti già esistenti — leggerli romperebbe la cecità;
3. il documento già prodotto di **B1** (`docs/spec_funzionale/SPEC_FUNZ_01_B1.md`) e qualsiasi altro `SPEC_FUNZ_01_B*.md`;
4. qualsiasi altro documento che enumeri requisiti `R-*`, `NFR-*`, `CN-*` (o `B1-*`, `B3-*`, ...) già definiti altrove.

Ti appoggi **esclusivamente** a: questa task card **+** il CAP-fonte del §1. Numeri gli ID requisito **da zero, autonomamente**, secondo lo schema del §4.2 — **non** riusare ID presi da una spec preesistente o da B1.

Il **confronto-copertura** con la spec già esistente (v2 congelata, limitatamente al perimetro payload) è compito **esclusivo del Reviewer in fase di review** (modalità B già validata su B1). Non è compito tuo e non devi tentarlo.

> Perché: la cecità garantisce che i requisiti derivino dal contenuto metodologico chiuso e non da una parafrasi di lavoro precedente. Tracce di una spec preesistente nel tuo output (ID copiati, frasi identiche non presenti nel CAP-fonte) sono trattate dal Reviewer come **BUG REALE di processo**.

---

## 1. Perimetro-fonte (cosa derivi) — SOLO questo

**Fonte unica e autoritativa**: `docs/methodology_v2/CAP_02_parte_II.md` ("Parte II — Contratto del segnale FIB"), **limitatamente al Capitolo 6 (Schema del segnale e invarianti) nelle sue tre sezioni 6.1 / 6.2 / 6.3**.

- **CAP-02 è chiuso PASS con SHA confermato `a1625df`** (`tasks/STATO_CORRENTE.md:9`; disambiguazione storica risolta dall'Orchestratore con commit `633f39e` — l'SHA è ora pinnabile, **non** più `<sha-da-confermare>`). Cita il file con provenienza `[DOC-INTERNO CAP_02_parte_II.md:<riga>]`. È un capitolo **congelato** (freeze G-09): **sola lettura**, non lo modifichi.
- Il preambolo della Parte II (`CAP_02_parte_II.md:1-9`) e i suoi richiami autoritativi sono **leggibili come contesto** e citabili quando un campo del payload vi è definito (es. il tick 5pt al `:9`, il dominio di `b` al `:5`/`:9`), ma **non** sono materia di altri capitoli da consolidare qui.

Il **tema** del perimetro (descritto per contenuto, non per struttura di alcuna spec): **il payload formale del segnale come oggetto contrattuale immutabile**. In dettaglio, e **solo** questo:

- **Il segnale come tupla strutturata $\mathcal{S}$** (Cap.6.1): l'insieme ordinato dei campi che descrivono in modo completo l'ipotesi operativa pubblicata. Ogni campo del payload con il suo **dominio**, i suoi **vincoli** e il suo **significato di prodotto**: `signal_id` (chiave operativa univoca, non riusabile); `timestamp_emission` (istante al minuto chiuso, CET); `direction` (long/short); `entry_zone` (banda di prezzo discreta attorno a $p_{ref}$, con **semi-ampiezza $b$** e i suoi vincoli — vedi sotto); `target_1` e `target_2` (due prezzi strutturali di obiettivo, entrambi obbligatori e distinti, multipli di 5, con i vincoli d'ordine per long/short); `target_2_type` e `stop_type` (qualificatori `{structural, synthetic}` come **campi del payload**); `stop_loss` (prezzo strutturale di stop) con la distanza $d_{stop}$ e il **vincolo geometrico $d_{stop} > b$**; `setup_class` (`{directional, trade_range}`) come attributo del payload e il **filtro 80pt associato** *limitatamente alla sua qualificazione del campo* (vedi nota di confine sotto); $\Delta t_{cromosoma}$ e $T_{touch}^{max}$ come **campi/parametri del payload** con i loro domini discreti.
- **Banda di ingresso $b$** (Cap.6.1): dominio discreto $b \in \{5,10,15,20,25,30,35,40\}$ punti FIB; $b_{min}=5$ provvisorio = 1 tick; `entry_zone` come insieme discreto di livelli multipli di 5; cardinalità $(2b/5)+1$; $p_{ref}$ multiplo di 5 fissato all'emissione; il razionale del floor $b_{min}$ (evitare banda nulla).
- **Target 1 / Target 2 come schema-dato** (Cap.6.1): obbligatorietà e distinzione di entrambi; ancoraggio strutturale; vincoli d'ordine; la **nota Q-05 Clausola 2** secondo cui target_2 è informazione strutturale pubblicata, **non** variabile di lifecycle del segnale (questo è un attributo del *payload*; il fatto che il *contratto si chiuda a target_1* e l'eventuale raggiungimento di target_2 sia evento di lifecycle/submacchina è materia di B3 — qui si consolida solo "target_2 è un campo obbligatorio del payload, di natura informativa-strutturale").
- **Stop strutturale come schema-dato** (Cap.6.1): `stop_loss` come prezzo strutturale multiplo di 5; definizione di $d_{stop}=|p_{ref}-\texttt{stop\_loss}|$; vincolo obbligatorio $d_{stop}>b$ con il suo razionale (evitare fill al bordo opposto coincidente con lo stop); `stop_type` `{structural, synthetic}` come campo; il fatto che il dominio di `stop_type` **non** includa stop prodotti dall'operatore (il motore non gestisce stop manuali — confine già sancito, qui solo come vincolo di dominio del campo).
- **Invariante di payload immutabile** (Cap.6.2): una volta emesso, il payload identificato da `signal_id` non subisce alcuna modifica; la tupla $\mathcal{S}$ è congelata all'emissione; non esiste refresh/edit che lasci invariato il `signal_id` modificando un campo; il razionale di prodotto (l'operatore opera su valori che non mutano a sua insaputa fra lettura e invio ordine).
- **Segnale unico attivo + sostituzione come proprietà del payload-oggetto** (Cap.6.3): il vincolo $|\mathcal{A}(t)| \leq 1$ (al massimo un segnale attivo per istante) e la regola "il motore **non modifica** il segnale esistente ma emette un **nuovo** `signal_id` con una **nuova tupla $\mathcal{S}'$ completa e indipendente**, congelata" — consolidati **come invarianti del payload** (un payload non si edita: si sostituisce). **Confine**: la *meccanica delle transizioni di stato* della sostituzione (`active → revoked`, gli stati terminali, la state machine) è materia di **B3** e **non** va consolidata qui; di Cap.6.3 prendi **solo** ciò che è proprietà-del-payload (immutabilità → sostituzione, unicità del segnale attivo), non la state machine.

**Nota di confine sul filtro 80pt e su `setup_class`**: `setup_class` è un **campo del payload** (B2). Il **filtro di emissione 80pt** associato (`|target_1 − p_ref| ≥ 80` per directional; `A_range ≥ 80` per trade_range) è definito in Cap.6.1 *come qualificazione del campo* ma è **una condizione di emissione**, la cui trattazione piena è in Cap.8 → **B4**. In B2 puoi consolidare che `setup_class` ha dominio `{directional, trade_range}` e che **a ciascun valore è associato un filtro 80pt di emissione** (citando Cap.6.1), **senza** sviluppare la regola di emissione (Cap.8) né la definizione operativa di $A_{range}$ (Parte IV): quella è fuori B2. Evita lo scope creep verso B4.

**Regola di confine "tutto e solo"**: lo scope di B2 è **tutto e solo** il contenuto-payload del Cap.6 (6.1/6.2/6.3) sopra elencato, **niente di più, niente di meno**. Se incontri nel Cap.6 — o vieni tentato di tirare dentro da Cap.7/8/9/10/11 — materia che appartiene a un blocco successivo (state-machine e stati terminali, raw touch come evento, timer come *meccanica di transizione*, condizioni di emissione, contratto/latenza Telegram, log/replay, position lifecycle/submacchina), **non** la consolidi qui: la lasci al suo blocco (vedi §6 out-of-scope). I campi $\Delta t_{cromosoma}$ e $T_{touch}^{max}$ rientrano in B2 **come campi del payload con il loro dominio**; la **semantica dei timer** (decorrenza dal raw touch, scadenza → `expired`, counter sui minuti di trading) è materia di B3 e **non** è B2.

---

## 2. Eredità autoritativa pertinente a B2 (NON ri-verificare — citala col livello-fonte)

I seguenti fatti sono **autoritativi**: "autoritativo" = **non ri-fetchare e non ri-derivare**, NON promozione di livello-fonte. Nessuna conclusione strutturale può poggiare su una fonte solo `[WIKI-HINT]`. (I numeri di riga indicati sono **puntatori di lavoro** dell'Orchestratore/Planner: il Developer li **verifica token-per-token** sul CAP-fonte prima di citarli — vedi AC-G7; se una riga non risolve esattamente, cita la riga corretta che contiene il fatto.)

- **Tick size FIB = 5 punti**: prezzi, bande, target, stop sono multipli di 5; $b_{min}=5$ = 1 tick — `[DOC-INTERNO CAP_02_parte_II.md:9]` (e ripreso in 6.1 `:33`). È fatto strutturale dello strumento, già autoritativo (nota di progetto FIB; B1).
- **Dominio della semi-ampiezza** $b \in \{5,10,15,20,25,30,35,40\}$ con $b_{min}=5$ provvisorio (congelato in Parte V) — `[DOC-INTERNO CAP_02_parte_II.md:33]` (preambolo `:5`, `:9`).
- **Vincolo geometrico $d_{stop} > b$** (obbligatorio, ereditato da CAP-01; cromosomi che lo violano sono non validi) — `[DOC-INTERNO CAP_02_parte_II.md:47, :49]`.
- **target_1 e target_2 entrambi obbligatori, distinti, strutturali**, con vincoli d'ordine long/short; target_2 = informazione strutturale pubblicata (Q-05 Clausola 2) — `[DOC-INTERNO CAP_02_parte_II.md:35, :37]`.
- **Campi `target_2_type` / `stop_type`** dominio `{structural, synthetic}`, aggiunti nell'Iterazione 4/5 (chiusura O-3 / M-12, D-v2-7 / NB-v2-2) — `[DOC-INTERNO CAP_02_parte_II.md:39, :51]`.
- **Invariante di payload immutabile**: tupla congelata all'emissione, nessun edit a parità di `signal_id` — `[DOC-INTERNO CAP_02_parte_II.md:73]`.
- **Segnale unico attivo** $|\mathcal{A}(t)| \leq 1$; sostituzione = nuovo `signal_id` + nuova tupla, non edit (1 contratto alla volta, punto 7 dichiarazione di intenti) — `[DOC-INTERNO CAP_02_parte_II.md:81, :83]`.
- **Filtro 80pt per `setup_class`** (directional: `|target_1 − p_ref| ≥ 80`; trade_range: `A_range ≥ 80`) come qualificazione del campo `setup_class` — `[DOC-INTERNO CAP_02_parte_II.md:53, :55, :59]`. (Trattazione piena = B4; qui solo qualificazione del campo, vedi §1 nota di confine.)
- **Q chiuse pertinenti** (decisioni del supervisore già prese, autoritative, NON riaprire): **Q-05** (Opzione D raffinata: state machine 1+6 stati con target_2_hit rimosso; target_2 campo obbligatorio del payload come informazione strutturale; position lifecycle submacchina distinta) — `[DOC-INTERNO CAP_02_parte_II.md:7]`; **Q-02** (ancoraggio movimento strutturale al primo pivot post-apertura), **Q-03/cap 2 giorni** dal raw touch — `[DOC-INTERNO CAP_02_parte_II.md:5]`. Di Q-05, in B2 si usa **solo** la Clausola 2 (target_2 campo del payload); le Clausole 1 e 3 (state machine, submacchina) sono **B3** e non si consolidano qui.

### 2.1 — Censimento M-promemoria (CARRYOVER) per B2

Verificato il registro `tasks/CARRYOVER.md`: **nessun M-promemoria aperto è assegnato a B2**. Il payload del segnale è materia consolidata nei CAP chiusi e non porta M aperti propri. Assegnazioni motivate degli M pertinenti ad altri blocchi (per completezza, **NON da recepire in B2**):

- **M-2 / B-1** (verifica empirica latenza Telegram $L_{max}=30$s, OPEN) → blocco **B4** (consegna Telegram). Fuori scope B2.
- **M-GOV-1 / B-2** (orario sessione 08:00–22:00, APERTO; upgrade empirico da tape DAPI) → blocco **B5** (runtime/sessione). Fuori scope B2.
- **M-1 / M-9 / M-10** (schemi CANDLE/PRICE/BOOK_5) + **RACC-METODO-2** → blocco **B6** (schema-dato DAPI). Fuori scope B2.
- **M-12** (collocazione di `target_2_type` / `stop_type` nel payload) → **già CLOSED-CAP-04** (mini-patch CAP-02 Cap.6.1: i due campi sono nella tupla $\mathcal{S}$). In B2 i due campi si recepiscono **come dato di payload già chiuso**, non come M da riaprire.

Nessun M perso; nessun M da incardinare in B2. **Se** durante la review emergesse un M nuovo, lo registra l'Orchestratore in chiusura (non il Developer, non il Planner).

---

## 3. Acceptance Criteria — globali del blocco (il Reviewer audita QUESTI)

**AC-G1 — Atomicità (N1)**: ogni requisito è **una sola proposizione verificabile**. Un requisito che impacchetta più concern (es. "target_1 e target_2 sono obbligatori, distinti, multipli di 5 e ordinati") va **spezzato** in più ID atomici (obbligatorietà; distinzione; multiplo di 5; ordine long; ordine short — separati). Un campo del payload con più vincoli indipendenti genera più requisiti, non uno solo. La granularità è decisa da te applicando N1; **nessun conteggio-target** è imposto.

**AC-G2 — Tracciabilità obbligatoria**: **ogni** requisito traccia ad almeno una riga del CAP-fonte con la grafia canonica `[DOC-INTERNO CAP_02_parte_II.md:<riga>]`. Un requisito senza tracciabilità è un requisito sbagliato.

**AC-G3 — Valore operativo obbligatorio**: **ogni** requisito dichiara esplicitamente il **valore per l'operatore retail FIB** (perché questo campo/vincolo del payload conta per chi riceve ed esegue manualmente il segnale da cellulare — es. "l'immutabilità garantisce che i valori letti sul telefono siano quelli su cui si invia l'ordine"; "il vincolo $d_{stop}>b$ evita un segnale stoppato nello stesso tick del fill"). Un requisito senza valore operativo dichiarato è un requisito sbagliato.

**AC-G4 — Divieto "verificato X" di prima istanza (RM-1)**: la spec **richiama** fatti già chiusi nel CAP; **non** introduce nuove dichiarazioni "verificato X" su sistemi esterni di prima istanza. Se un fatto non è asserito nel CAP-fonte, **non** lo asserisci come verificato: lo ometti, oppure lo marchi esplicitamente come assunzione non verificata con la formula RM-1 (`VERIFICA / PROVE / ALTERNATIVE ESCLUSE / ALTERNATIVE NON ESCLUSE`). Preferibile: restare entro ciò che il CAP afferma.

**AC-G5 — Etichette RM-3 su fonti esterne**: ogni riferimento a documentazione esterna (MiFID II, Telegram, Directa, Borsa Italiana/IDEM) è etichettato `[WIKI-HINT, da verificare]` e **non è mai fonte unica** di un requisito: il requisito regge sul CAP-fonte; l'esterno è solo hint concordante. In B2 le fonti esterne dovrebbero essere marginali (il payload è materia interna): se ne usi, etichettale.

**AC-G6 — Grafia canonica delle citazioni**: usa `[DOC-INTERNO …]`, `[CODICE-ESISTENTE …]` (grafia canonica; **vietata** la grafia storica `[CODICE-EXISTENTE …]`), `[PROVA-EMPIRICA …]`, `[WIKI-HINT, da verificare]`.

**AC-G7 — Floor citazioni 100% (verifica in review)**: tutte le citazioni `[DOC-INTERNO CAP_02_parte_II.md:<riga>]` devono essere **verificabili token-per-token** contro il CAP-fonte. Il Reviewer le verifica al 100%; una citazione che non risolve è un finding. I numeri di riga del §2 sono puntatori di lavoro: **verificali tu** prima di citarli.

**AC-G8 — Cecità preservata (modalità B)**: l'output non contiene ID-requisito importati da una spec preesistente o da B1, né frasi copiate da `SPEC_FUNZ_01.md` / `_v1_storico` / `SPEC_FUNZ_01_B*.md` / file di chunking. Tracce di questo tipo = **BUG REALE di processo** (Reviewer). I tuoi ID sono auto-assegnati (§4.2).

**AC-G9 — Scope invariato ("tutto e solo")**: i requisiti coprono **tutto e solo** il perimetro Cap.6 (6.1/6.2/6.3) del §1 (campi del payload + invariante immutabilità + segnale unico attivo/sostituzione-come-proprietà-del-payload). **Nessun** requisito sconfina in B3 (state machine, stati terminali, raw touch come evento, semantica dei timer, transizioni di sostituzione), in B4 (condizioni di emissione, regola 80pt come regola di emissione, contratto Telegram, latenza, anti-duplicato, retry), in B5 (log/replay, runtime), né in Cap.10/11 (log di lifecycle, position lifecycle/submacchina). Materia di Cap.6 omessa = gap di copertura (finding); materia fuori perimetro inclusa = scope creep (finding).

**AC-G10 — Matrice di tracciabilità finale + nota di rinvio**: il documento si chiude con una **matrice** `ID requisito | proposizione | citazione CAP (CAP_02_parte_II.md:riga) | valore operativo`. Per il perimetro B2 (un solo capitolo, Cap.6) **non** è richiesta una colonna "capitoli non tracciati" estesa all'intera metodologia; è invece richiesta una **nota** che dichiari esplicitamente cosa del Cap.6 — o cosa adiacente al payload — è stato **deliberatamente rinviato** ad altri blocchi e perché (es. state machine e timer-semantica → B3; filtro 80pt come regola di emissione e contratto Telegram → B4; log/replay → B5/CAP-10; position lifecycle/target_2 come evento → B3/submacchina Cap.11), così che il Reviewer possa distinguere un'omissione voluta da un gap.

**AC-G11 — Invarianti del payload evidenziate come tali**: le proprietà **invarianti/strutturali** del payload — immutabilità post-emissione (6.2), segnale unico attivo $|\mathcal{A}(t)|\le1$ e sostituzione-non-edit (6.3), vincolo geometrico $d_{stop}>b$ (6.1) — sono rese come requisiti **strutturali/invarianti** espliciti (non implementativi, non rivedibili), data la loro rilevanza contrattuale e compliance/prodotto. La distinzione `{structural, synthetic}` di `target_2_type`/`stop_type` è resa come **dominio di campo del payload**, qualificando che `synthetic` ha natura informativa derivata da una regola del modello (non da struttura confermata).

---

## 4. Sezioni da produrre (nel documento `SPEC_FUNZ_01_B2.md`)

> Sono **sezioni**, non capitoli di metodologia. Struttura indicativa; l'importante è coprire il perimetro §1 rispettando gli AC §3.

### 4.1 — Contenuto
1. **Intestazione e scopo del blocco**: cosa copre B2 (payload del segnale), che è il blocco 2/8 di una spec ricostruita a blocchi, che il file è autonomo e sarà ricomposto a fine serie. Dichiara la pin del CAP-fonte: `CAP_02_parte_II.md` chiuso PASS `a1625df`. Dichiara lo schema ID (§4.2).
2. **Il segnale come oggetto-payload immutabile**: il segnale è una tupla strutturata $\mathcal{S}$, completa, congelata all'emissione; introduzione al contratto-payload (senza anticipare lifecycle/state-machine = B3).
3. **Campi del payload (schema-dato)**: un blocco di requisiti per ciascun campo con dominio + vincoli + valore operativo: `signal_id`, `timestamp_emission`, `direction`, `entry_zone` (con banda $b$ e suo dominio/cardinalità), `target_1`/`target_2` (obbligatorietà, distinzione, multiplo di 5, ordine, natura strutturale; target_2 informazione strutturale pubblicata — Q-05 Cl.2), `target_2_type`/`stop_type` (`{structural, synthetic}`), `stop_loss` ($d_{stop}$, vincolo $d_{stop}>b$), `setup_class` (`{directional, trade_range}` + filtro 80pt come qualificazione del campo, **non** come regola di emissione), $\Delta t_{cromosoma}$ e $T_{touch}^{max}$ (domini discreti, come **campi/parametri del payload**, **senza** semantica timer = B3).
4. **Banda di ingresso $b$**: dominio discreto, $b_{min}=5$=1 tick, `entry_zone` come insieme discreto di livelli multipli di 5, cardinalità, razionale del floor.
5. **Invariante di payload immutabile**: requisito/i strutturale/i (6.2) — nessun edit a parità di `signal_id`; razionale di prodotto.
6. **Segnale unico attivo e sostituzione come proprietà del payload**: $|\mathcal{A}(t)|\le1$; sostituzione = nuovo `signal_id` + nuova tupla, non edit (6.3) — **limitatamente** alla proprietà-del-payload (la state machine è B3).
7. **Matrice di tracciabilità + nota di rinvio** (AC-G10).

### 4.2 — Schema ID requisito (auto-assegnato, NON importato)
Adotta uno schema **tuo**, coerente e atomico, ad esempio prefisso per famiglia + numerazione locale del blocco (es. `B2-R-01`, `B2-R-02` per requisiti funzionali/di schema-payload; `B2-CN-01` per requisiti invarianti/compliance — es. immutabilità, segnale unico attivo, $d_{stop}>b$). **Non** riusare la numerazione di alcuna spec preesistente né di B1. Dichiara lo schema all'inizio del documento.

---

## 5. REPORT atteso (`reports/REPORT_SPEC_FUNZ_01_B2.md`)

6 sezioni formato supervisore + tabella di verifica AC:
1. **Cosa è stato prodotto** (sintesi dei requisiti per sezione).
2. **Ipotesi di partenza** (incluso: ho lavorato in cieco dal solo Cap.6 di `CAP_02_parte_II.md`; conferma delle letture obbligatorie del §0).
3. **Decisioni rilevanti** (scelte di atomicità N1; cosa ho deliberatamente rinviato ad altri blocchi e perché — in particolare la separazione payload vs state-machine/timer-semantica/emissione/Telegram; eventuali punti dove ho applicato la cautela RM-1 invece di asserire).
4. **Misura prima/dopo** (qui: copertura del perimetro Cap.6.1/6.2/6.3; non c'è un "prima").
5. **Domande aperte** (eventuali ambiguità; se nessuna, dichiararlo).
6. **Criterio di rollback** (come si annullerebbe B2 senza impattare altri blocchi — è file autonomo).

+ **Tabella verifica AC**: `AC-G1..AC-G11 | OK/PARZIALE/MANCA | evidenza file:riga`. Onestà claim→evidenza (BASE_COMUNE §8): ogni OK ha evidenza puntuale. Includi la sezione **"Applicazione RM-1 a me stesso"** (BASE_COMUNE §8).

### Pre-consegna (checklist Developer)
- [ ] Letti METODO + BASE_COMUNE + spec_developer.md (confermato nel REPORT).
- [ ] Lavorato in **cieco** (non aperti SPEC_FUNZ_01.md / _v1_storico / SPEC_FUNZ_01_B*.md / file di chunking).
- [ ] Ogni requisito è atomico (N1), tracciato (`[DOC-INTERNO CAP_02_parte_II.md:<riga>]`), con valore operativo.
- [ ] Citazioni verificabili token-per-token; grafia canonica.
- [ ] Scope = tutto e solo Cap.6 (6.1/6.2/6.3); rinvii ad altri blocchi annotati nella nota di matrice; nessuno sconfinamento in B3/B4/B5 (state-machine, timer-semantica, emissione, Telegram, log/replay, submacchina).
- [ ] `SPEC_FUNZ_01_B2.md` + `REPORT_SPEC_FUNZ_01_B2.md` scritti; commit `[SPEC-FUNZ-01-B2]` pushato su `origin/main`; `tasks/DEV_STATUS.md` = `READY_FOR_REVIEW`. Poi **fermati**.

---

## 6. Out-of-scope di B2 (con destinazione esplicita)

| Materia | Destinazione |
|---|---|
| State machine del segnale: stati (`active` + 6 terminali), transizioni, raw touch come **evento**, **semantica dei timer** ($\Delta t_{cromosoma}$/$T_{touch}^{max}$: decorrenza, scadenza→`expired`, counter minuti di trading), transizione di sostituzione `active→revoked` (Cap.7) | **B3** (state-machine & lifecycle) |
| Position lifecycle / submacchina post-target_1, target_2 come **evento** raggiunto, metriche $\pi_{t_2\mid t_1}$/MFE/MAE/$f_{stop\mid t_1}$ (Cap.11) | **B3** (lifecycle; submacchina) |
| Condizioni di emissione (volatilità, liquidità, distanza sigma-units), **regola di emissione** e **filtro 80pt come regola** (Cap.8); definizione operativa di $A_{range}$ (Parte IV) | **B4** (emissione & consegna) |
| Contratto informativo del messaggio Telegram, ordine dei campi pubblicati, latenza $L_{max}$ (M-2/B-1), anti-duplicato, retry, errori di pubblicazione (Cap.9) | **B4** (emissione & consegna) |
| Log di emissione/transizioni/chiusura, replay/determinismo bit-exact, granularità temporale, persistenza log (Cap.10) | **B5** (runtime, sessione & compliance) — oppure CAP-10/lifecycle log come destinazione naturale |
| Runtime DAPI / sessione operativa come requisito / rollover / compliance operativa / M-GOV-1 | **B5** (runtime, sessione & compliance) |
| Schema-dato DAPI (CANDLE/PRICE/BOOK_5) / decoder / M-1·M-9·M-10 / RACC-METODO-2 | **B6** (schema-dato DAPI) |
| Gate di go-live: definizione quantitativa del successo, $E[R_{net}]$, DSR/PBO, metriche di lifecycle/rischio (Cap.5 di CAP-01) | **B7** (gate di go-live) |
| Confine PHASE-2 / fasizzazione / handoff a FASE-D | **B8** (confine PHASE-2) |
| Matematica del modello: volatilità condizionata $\hat\sigma_{pt}$, geometria delle zone, $p_{ref}$ derivato (Parti III/IV) | CAP chiusi, non tracciato in spec |
| Ambito / operatore / strumento / vincolo solo-emissione / canale a livello di ambito (Cap.1–3 di Parte I) | **B1** (già CHIUSO PASS `7195ffe`) — non ridefinire, non riaprire |
| Assemblaggio degli 8 documenti in un'unica spec consolidata | **task di assemblaggio dedicato dopo B8** |
| `docs/methodology_v2/00_indice.md` | **NON si tocca** (SPEC-FUNZ non è una Parte della metodologia v2) |

---

## 7. Done when (domande operative a cui B2 deve rispondere univocamente)

Al PASS, un lettore deve poter rispondere senza ambiguità, **solo leggendo `SPEC_FUNZ_01_B2.md`**, a:
1. Da quali campi è composto il payload del segnale, e qual è il dominio e il vincolo di ciascun campo?
2. Che cos'è la banda di ingresso e qual è il dominio della sua semi-ampiezza $b$ (incluso $b_{min}$ e il significato in tick)?
3. Target_1 e target_2 sono entrambi obbligatori? Qual è la loro natura e il loro ordine per long e per short? Che cosa significa che target_2 è "informazione strutturale pubblicata"?
4. Che cosa qualificano `target_2_type` e `stop_type`, e quali valori possono assumere?
5. Qual è il vincolo che lega lo stop_loss alla banda ($d_{stop}>b$) e perché esiste?
6. Il payload può cambiare dopo l'emissione? (No — invariante di immutabilità; razionale.)
7. Quanti segnali possono essere attivi contemporaneamente, e come avviene una "revisione" del segnale a livello di payload (sostituzione vs edit)?
8. Ogni risposta è tracciabile a una riga di `CAP_02_parte_II.md` (Cap.6) e porta un valore operativo dichiarato?

---

## 8. Modalità di review (per l'Orchestratore e il Reviewer)

- **Review formale piena adattata al non-CAP**, **sede CLI** (GOV-SURFACES-01). Il Reviewer applica i suoi **due giri ostili** agli **AC di B2** (§3), **non** agli AC dei CAP chiusi (CAP-02 è frozen, non si riaudita).
- Audit documentale **no-DAPI**; **divieto CLI** (niente probe di zelo). Lista **"Empirico-CLI da verificare" attesa VUOTA**.
- **Compito esclusivo del Reviewer — confronto-copertura (modalità B)**: il Reviewer (e **solo** lui, dopo aver auditato gli AC) confronta i requisiti di B2 con il **perimetro corrispondente di `docs/spec_funzionale/SPEC_FUNZ_01.md` (v2 congelata, PASS `ab7450f`)** limitatamente all'ambito **payload (Cap.6 di Parte II)**, per verificare che **nessun requisito di prodotto del perimetro payload sia caduto** nella ricostruzione cieca e per segnalare divergenze (in più / in meno) con classificazione. Questo è il punto in cui la cecità del Developer viene "chiusa". Attenzione al confine: requisiti della v2 che appartengono a state-machine/emissione/Telegram **non** sono buchi di B2 (sono B3/B4) — il Reviewer li classifica come "fuori perimetro B2", non come gap.
- **Cecità del Developer come oggetto di audit**: il Reviewer cerca attivamente tracce di rottura della cecità (ID importati da v2 o da B1, frasi identiche alla v2 non presenti nel Cap.6); se trovate → **BUG REALE**.
- Verdetto **PASS / CONDITIONAL / FAIL** con tabella "Classificazione per il supervisore". ≥1 BUG REALE ⇒ non-PASS.

---

## 9. Pipeline attesa (per l'Orchestratore)

1. **spec_developer** (CLI, via general-purpose che adotta `spec_developer.md`) costruisce `docs/spec_funzionale/SPEC_FUNZ_01_B2.md` + `reports/REPORT_SPEC_FUNZ_01_B2.md` **in cieco** (vincolo §0.1), scrive `READY_FOR_REVIEW` in `tasks/DEV_STATUS.md`, si ferma. Non committa il task card (lo fa l'Orchestratore).
2. **Orchestratore**: **check post-Developer** (6 controlli, **condizione-3 indice = N/A**; "commit copre i file attesi" = `SPEC_FUNZ_01_B2.md` + `REPORT_SPEC_FUNZ_01_B2.md` + `DEV_STATUS.md`). Se OK → invoca il Reviewer; altrimenti rilancia il Developer con prompt mirato ai gap.
3. **spec_reviewer** (CLI, via general-purpose che adotta `spec_reviewer.md`): audit ostile sugli AC di B2 + confronto-copertura col perimetro payload (Cap.6) della v2 congelata (§8); verdetto.
4. **CONDITIONAL/FAIL** → punto di controllo supervisore. **PASS** → chiusura B (7 condizioni adattate, indice = N/A); marcatore `SPEC-FUNZ-01-B2: CHIUSO PASS <sha-review>` in `tasks/STATO_CORRENTE.md`; poi il supervisore decide l'apertura di **B3**.

---

*Task card scritta dallo spec_planner. NON committata dal Planner (lo fa l'Orchestratore). Nessuna spec scritta, nessun CAP modificato (freeze G-09 rispettato). Questa card non contiene ID-requisito né contenuti copiati dalla v2 / da B1 / dai file di chunking: cecità preservata.*
