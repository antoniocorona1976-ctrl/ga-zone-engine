# TASK ATTIVO: SPEC-FUNZ-01-B3 — State-machine & lifecycle del segnale (ricostruzione cieca, modalità B, blocco 3/8)

> **Track**: Business-spec (SPEC-FUNZ). **Sede**: CLI per tutto il ciclo (GOV-SURFACES-01, METODO §Superfici). **Tag commit**: `[SPEC-FUNZ-01-B3]`. Tutto su `main` (trunk); isolamento via cartella dedicata, non via branch.
>
> **Letture obbligatorie del Developer, in quest'ordine, PRIMA di scrivere**: `tasks/METODO.md` (RM-1..RM-4 + RACC-METODO-2), `.claude/BASE_COMUNE.md` (ciclo, sede CLI per la spec, onestà claim→evidenza), `.claude/agents/spec_developer.md` (il tuo ruolo), questo `tasks/ACTIVE_TASK.md`. **Conferma in testa al REPORT di averli letti** (formato richiamato anche al §5).

---

## 0. Natura del blocco e modalità di lavoro (LEGGERE PRIMA DI TUTTO)

Questo è il **terzo** di **8 blocchi** (B1→B8) in cui la business-spec del progetto viene **ricostruita ex-novo**, **uno alla volta**. Ogni blocco = un ciclo Planner→Developer→Reviewer = un PASS. Gli 8 documenti, a fine serie (dopo B8), verranno ricomposti in un'unica spec consolidata da un **task di assemblaggio dedicato**: l'assemblaggio è **FUORI SCOPE di B3** (non eseguirlo, non anticiparlo). B1 (Ambito & operatore, `7195ffe`) e B2 (Payload del segnale, `b858a88`) sono già **CHIUSI PASS**; B3 ne è la prosecuzione e **non ridefinisce** ciò che B1/B2 hanno già consolidato (ambito/operatore/strumento/vincolo solo-emissione/canale a livello di ambito = B1; schema-payload, campi, banda, target/stop **come schema-dato**, immutabilità, segnale unico attivo = B2): se un fatto di ambito o di payload ti serve come premessa, lo **citi dal CAP-fonte** (non da B1/B2, che non devi aprire — vedi §0.1).

### 0.1 — VINCOLO DI CECITÀ (cardine della modalità B — leggere con la massima attenzione)

Tu (Developer) costruisci i requisiti di B3 **DAI SOLI capitoli pertinenti del CAP-fonte** elencati al §1, **cieco** rispetto a qualsiasi specifica funzionale già esistente e rispetto ai blocchi B1/B2/B4..B8 già o non ancora prodotti. È **TASSATIVAMENTE VIETATO** aprire, leggere, consultare, citare o parafrasare:

1. `docs/spec_funzionale/SPEC_FUNZ_01.md` (la spec v2 congelata, PASS `ab7450f`) e qualsiasi file `*_v1_storico*`;
2. qualunque file di **pianificazione/chunking** del track business-spec (es. `PROPOSTA_SUDDIVISIONE_SPEC*.md`): contengono la mappa dei requisiti già esistenti — leggerli romperebbe la cecità;
3. i documenti già prodotti di **B1** (`docs/spec_funzionale/SPEC_FUNZ_01_B1.md`) e **B2** (`docs/spec_funzionale/SPEC_FUNZ_01_B2.md`) e qualsiasi altro `SPEC_FUNZ_01_B*.md`;
4. qualsiasi altro documento che enumeri requisiti `R-*`, `NFR-*`, `CN-*` (o `B1-*`, `B2-*`, ...) già definiti altrove.

Ti appoggi **esclusivamente** a: questa task card **+** il CAP-fonte del §1. Numeri gli ID requisito **da zero, autonomamente**, secondo lo schema del §4.2 — **non** riusare ID presi da una spec preesistente o da B1/B2.

Il **confronto-copertura** con la spec già esistente (v2 congelata, limitatamente al perimetro state-machine/lifecycle) è compito **esclusivo del Reviewer in fase di review** (modalità B già validata su B1 e B2). Non è compito tuo e non devi tentarlo.

> Perché: la cecità garantisce che i requisiti derivino dal contenuto metodologico chiuso e non da una parafrasi di lavoro precedente. Tracce di una spec preesistente nel tuo output (ID copiati, frasi identiche non presenti nel CAP-fonte) sono trattate dal Reviewer come **BUG REALE di processo**.

---

## 1. Perimetro-fonte (cosa derivi) — SOLO questo

**Fonte unica e autoritativa**: `docs/methodology_v2/CAP_02_parte_II.md` ("Parte II — Contratto del segnale FIB"), **limitatamente al Capitolo 7 (Stati del segnale e state machine, sezioni 7.1–7.6) e al Capitolo 11 (Position lifecycle e tracking out-of-scope dal motore, sezioni 11.1–11.5)**.

- **CAP-02 è chiuso PASS con SHA confermato `a1625df`** (`tasks/STATO_CORRENTE.md:10`; G-25 chiuso — l'SHA è pinnabile, **non** più `<sha-da-confermare>`; **nessuna dipendenza fragile**). Cita il file con provenienza `[DOC-INTERNO CAP_02_parte_II.md:<riga>]`. È un capitolo **congelato** (freeze G-09): **sola lettura**, non lo modifichi.
- Il preambolo della Parte II (`CAP_02_parte_II.md:1-9`) e le clausole Q-05 (`:7`) sono **leggibili come contesto** e citabili quando un fatto del lifecycle vi è ancorato (es. cap 2 giorni / decorrenza dal raw touch al `:5`; Q-05 Clausola 1 = state machine 1+6 stati al `:7`; Q-05 Clausola 3 = submacchina al `:7`), ma **non** sono materia di altri capitoli da consolidare qui.

Il **tema** del perimetro (descritto per contenuto, non per struttura di alcuna spec): **la semantica dinamica del ciclo di vita del segnale** — gli stati che il segnale attraversa, gli eventi che ne provocano le transizioni, la temporizzazione (timer pre/post-trigger come meccanica di scadenza), e la submacchina distinta che traccia la posizione oltre target_1. In dettaglio, e **solo** questo:

- **State machine del segnale: stati e semantica** (Cap.7.1): l'architettura a **1 stato non-terminale + 6 stati terminali** (Q-05 Clausola 1, target_2_hit rimosso). Lo stato `active` (segnale emesso, tupla pubblicata, in attesa di un evento). I sei stati terminali con la loro semantica e condizione d'ingresso: `target_1_hit` (successo, **chiusura definitiva del contratto** del segnale; target_2 NON è transizione di stato); `stopped` (stop raggiunto dopo raw touch, prima di target_1); `invalidated` (invalidazione strutturale **prima** del raw touch, incluso stop attraversato pre-touch; distinto da `stopped`); `missed_target` (target_1 raggiunto **prima** del raw touch; metrica riferita a target_1 non target_2, Q-03); `expired` (con le due cause `pretrigger_timeout`/`posttrigger_timeout` registrate come **campo causale**, non come stati distinti); `revoked` (segnale superseduto da nuovo `signal_id`, Cap.6.3). Proprietà invariante: **nessuno stato terminale ammette transizioni uscenti** (lifecycle definitivamente chiuso). Nota NB-9: la transizione `target_1_hit → revoked` **non esiste**.
- **Transizioni ammesse** (Cap.7.2): l'insieme delle transizioni $s \to s'$ (creazione→`active`; `active`→ciascuno dei 6 terminali con la rispettiva condizione). Proprietà: nessuna transizione esce dai terminali; in particolare `target_1_hit` non transita verso target_2_hit/revoked/altro. La **regola di precedenza degli eventi a parità di timestamp** (`expiry > invalidazione > missed_target > raw touch > azione post-trigger`) come vincolo necessario al determinismo del replay.
- **Raw touch come evento (non come stato)** (Cap.7.3): definizione del raw touch (prima barra 1-min chiusa il cui intervallo high-low contiene un livello discreto della `entry_zone`; nessun vincolo sulla direzione di provenienza); il `trigger_event` prodotto al raw touch; il **raw touch è sempre eseguibile** (nessuna guardia/filtro post-emissione); il `trigger_event` **non è uno stato** (il segnale resta `active`); il motore **non osserva il fill manuale** dell'operatore (non esegue ordini); trattamento del trigger come fill virtuale in backtest (riferito a Parte III per il dettaglio, **non** materia di B3). I **tre edge case del raw touch (NB-8)**: (a) barra di emissione con prezzo già in zona (valutazione da $t_{emission}+1$); (b) gap overnight dentro/oltre la zona (il gap **non** azzera il raw touch); (c) gap che salta la zona nella direzione opposta (verso lo stop → eventuale `invalidated`; verso target_1 → `missed_target`).
- **Semantica dei timer** (Cap.7.4 e 7.5): **timer post-esecuzione** $\Delta t_{cromosoma}$ — `expiry = t_exec + Δt_cromosoma` minuti di **trading**; il counter avanza **solo** nei minuti 8:00–22:00 CET dei giorni di trading, si arresta in notte/weekend/festivi (esempio multi-giorno citabile); allo scadere con segnale ancora `active` → `expired` con causa `posttrigger_timeout`. **Timer pre-trigger** $T_{touch}^{max}$ (NB-7) — decorre dalla `timestamp_emission`; counter sui soli minuti di trading; allo scadere senza raw touch → `expired` con causa `pretrigger_timeout`; razionale: eliminare la patologia "segnale `active` indefinitamente in attesa" che gonfierebbe l'`executable_rate`. **Confine**: in B3 entra la **semantica di temporizzazione** (decorrenza, scadenza, counter sui minuti di trading) dei due timer; i loro **domini discreti come campi del payload** sono già B2 e **non** si ri-consolidano (li citi come premessa dal CAP, non come requisito nuovo di B3).
- **Identificazione real-time del primo pivot strutturale post-apertura (M-1)** (Cap.7.6) come **contratto di osservazione real-time del motore** durante il lifecycle: il motore osserva le barre 1-min da 8:00 CET; il primo pivot strutturale post-apertura deve essere disponibile entro un tetto $N_{pivot}$ di barre (valore **non** fissato in Parte II → Parte V; **non** introdurre numeri); la cadenza di valutazione = barra 1-min chiusa (no tick intra-bar). **Confine**: l'**algoritmo** di pivot detection è Parte III (Cap.15) e **non** è B3; di Cap.7.6 prendi **solo** il contratto di osservazione/cadenza, non la regola di detection.
- **Position lifecycle come submacchina distinta** (Cap.11.1–11.5, Q-05 Clausola 3): la **separazione formale** segnale vs position lifecycle (il segnale si chiude in `target_1_hit`; la submacchina traccia oltre). Il perimetro **OUT-OF-SCOPE dal motore** (execution policy, scaling-out, trailing stop, dynamic sizing, take profit anticipato: tutto dell'operatore, punto 8 dichiarazione di intenti) e **IN-SCOPE per reporting/validazione** (le metriche). La **struttura della submacchina**: evento d'ingresso = `target_1_hit`; stato iniziale `tracking_active`; **eventi registrati** (`target_2_reached`, `stop_after_target_1`, `retracement_to_entry`, `position_close_event`) come **eventi della submacchina, non stati del segnale**; stato terminale `tracking_closed`; **target_2 come evento** (`target_2_reached`) e non come stato/transizione del segnale; **indipendenza assoluta**: la submacchina **non modifica** mai lo stato del segnale; log separati referenziati dal `signal_id`. L'**impatto sul GA**: lo space search del cromosoma **non** è esteso da policy post-target_1; le metriche della submacchina ($\pi_{t_2\mid t_1}$, MFE/MAE post-target_1, $f_{stop\mid t_1}$, tempi di permanenza) entrano nella fitness come **obiettivi di qualità informativa del payload**, non come variabili decisionali del cromosoma.

**Nota di confine sul `trigger_event`**: il `trigger_event` compare nel CAP in **due** luoghi distinti: come **evento del lifecycle** (Cap.7.3 — il raw touch produce l'evento, la state machine resta in `active`) → **questo è B3**; e come **notifica pubblicata su Telegram** (Cap.9.5 — messaggio separato, contratto informativo della notifica) → **questo è B4**. In B3 consolidi il raw touch/`trigger_event` come **evento del ciclo di vita** e la sua proprietà "sempre eseguibile / non-stato"; **non** consolidi la sua pubblicazione Telegram, il contratto informativo della notifica, la latenza o l'anti-duplicato (Cap.9 → B4). Evita lo scope creep verso B4.

**Nota di confine sui timer e su target_2/setup_class come campi**: $\Delta t_{cromosoma}$, $T_{touch}^{max}$, `target_2`, `stop_loss`, `setup_class`, `entry_zone`, banda $b$ sono **campi del payload** già consolidati in B2 (Cap.6). In B3 entra **solo** ciò che è **semantica dinamica**: i timer come **meccanica di scadenza/decorrenza**, target_2 come **evento** della submacchina, lo stop attraversato come **evento di invalidazione/stop**, la `entry_zone` come **insieme il cui contatto genera il raw touch**. **Non** ri-derivare i domini, i vincoli geometrici ($d_{stop}>b$), la cardinalità o l'immutabilità del payload: quella è B2. Se ti serve un campo come premessa di un evento, lo **citi dal Cap.6** come dato già fissato e ti concentri sull'**evento/transizione** che è materia di B3.

**Regola di confine "tutto e solo"**: lo scope di B3 è **tutto e solo** il contenuto di semantica-dinamica del Cap.7 (7.1–7.6) e del Cap.11 (11.1–11.5) sopra elencato, **niente di più, niente di meno**. Se incontri nel Cap.7/11 — o vieni tentato di tirare dentro da Cap.6/8/9/10 — materia che appartiene a un altro blocco (schema-payload come dato, condizioni/regola di emissione, contratto/latenza Telegram, formato dei log e determinismo bit-exact del replay), **non** la consolidi qui: la lasci al suo blocco (vedi §6 out-of-scope). In particolare: il **formato dei tre log** (emissione/transizioni/chiusura) e il **requisito di determinismo bit-exact del replay** (Cap.10) **non** sono B3 — pur registrando il lifecycle, sono materia di un blocco runtime/log (B5); di Cap.7 prendi la state machine **come tale**, non il formato del suo log.

---

## 2. Eredità autoritativa pertinente a B3 (NON ri-verificare — citala col livello-fonte)

I seguenti fatti sono **autoritativi**: "autoritativo" = **non ri-fetchare e non ri-derivare**, NON promozione di livello-fonte. Nessuna conclusione strutturale può poggiare su una fonte solo `[WIKI-HINT]`. (I numeri di riga indicati sono **puntatori di lavoro** dell'Orchestratore/Planner: il Developer li **verifica token-per-token** sul CAP-fonte prima di citarli — vedi AC-G7; se una riga non risolve esattamente, cita la riga corretta che contiene il fatto.)

- **State machine 1+6 stati (Q-05 Clausola 1)**: 1 stato non-terminale (`active`) + 6 terminali (`target_1_hit`, `stopped`, `invalidated`, `missed_target`, `expired`, `revoked`); `target_2_hit` **rimosso** — `[DOC-INTERNO CAP_02_parte_II.md:7, :95, :99]`.
- **`target_1_hit` è terminale di successo e chiude il contratto** (no transizioni uscenti; target_2 non è transizione; NB-9: niente `target_1_hit → revoked`) — `[DOC-INTERNO CAP_02_parte_II.md:101, :113, :129]`.
- **`expired` con due cause causali** (`pretrigger_timeout` / `posttrigger_timeout`) registrate come campo strutturato, non stati distinti — `[DOC-INTERNO CAP_02_parte_II.md:109, :126]`.
- **`invalidated` distinto da `stopped`** (invalidazione **prima** del raw touch, incluso stop attraversato pre-touch; definizione piena delle condizioni strutturali → Parte IV) — `[DOC-INTERNO CAP_02_parte_II.md:105, :124]`.
- **`missed_target` riferito a target_1** (non target_2; Q-03 di CAP-01) — `[DOC-INTERNO CAP_02_parte_II.md:107, :125]`.
- **Precedenza eventi a parità di timestamp** `expiry > invalidazione > missed_target > raw touch > azione post-trigger` (necessaria al determinismo del replay) — `[DOC-INTERNO CAP_02_parte_II.md:131]`.
- **Raw touch = evento, non stato; sempre eseguibile; segnale resta `active`; motore non osserva il fill manuale** — `[DOC-INTERNO CAP_02_parte_II.md:135, :137, :139]`.
- **Edge case raw touch NB-8** (a/b/c: barra di emissione $t_{emission}+1$; gap overnight non azzera; gap opposto → `invalidated`/`missed_target`) — `[DOC-INTERNO CAP_02_parte_II.md:145, :147, :149]`.
- **Timer post-trigger $\Delta t_{cromosoma}$**: `expiry = t_exec + Δt_cromosoma` minuti di trading; counter solo su 8:00–22:00 CET, arresto in notte/weekend/festivi; scadenza → `expired`/`posttrigger_timeout` — `[DOC-INTERNO CAP_02_parte_II.md:155, :157, :159]`.
- **Timer pre-trigger $T_{touch}^{max}$** (NB-7): decorre da `timestamp_emission`; counter sui minuti di trading; scadenza senza raw touch → `expired`/`pretrigger_timeout`; razionale anti-degenerazione `executable_rate` — `[DOC-INTERNO CAP_02_parte_II.md:163, :165, :167]`.
- **Contratto di osservazione pivot real-time (M-1)**: osservazione barre 1-min da 8:00 CET; tetto $N_{pivot}$ **non** fissato in Parte II (→ Parte V); cadenza = barra 1-min chiusa, no tick intra-bar; algoritmo detection → Parte III — `[DOC-INTERNO CAP_02_parte_II.md:171, :173, :175]`.
- **Separazione segnale vs position lifecycle (Q-05 Clausola 3)**: il segnale chiude in `target_1_hit`; la submacchina traccia oltre, fuori scope dal motore per le decisioni operative, in scope per reporting — `[DOC-INTERNO CAP_02_parte_II.md:7, :349, :351, :362]`.
- **Perimetro submacchina OUT/IN-scope**: OUT = execution policy/scaling-out/trailing/dynamic sizing/take profit (operatore, punto 8); IN = metriche $\pi_{t_2\mid t_1}$, MFE/MAE post-target_1, $f_{stop\mid t_1}$, tempi di permanenza — `[DOC-INTERNO CAP_02_parte_II.md:368, :370, :372, :374, :375]`.
- **Struttura submacchina**: ingresso = `target_1_hit`; stato iniziale `tracking_active`; eventi `target_2_reached`/`stop_after_target_1`/`retracement_to_entry`/`position_close_event` (eventi, **non** stati del segnale); terminale `tracking_closed`; **indipendenza** (non modifica lo stato del segnale); log separati per `signal_id` — `[DOC-INTERNO CAP_02_parte_II.md:381, :383, :385, :391, :393]`.
- **Impatto GA**: space search **non** esteso; metriche della submacchina come obiettivi di qualità informativa del payload, non variabili decisionali del cromosoma — `[DOC-INTERNO CAP_02_parte_II.md:397, :399, :401]`.
- **Cap 2 giorni / decorrenza dal raw touch** (ereditato CAP-01; $\Delta t_{cromosoma}$ dominio = $2\times840$ minuti) — `[DOC-INTERNO CAP_02_parte_II.md:5, :63]` (citabile come contesto del timer post-trigger; il **dominio come campo** è B2).
- **Q chiuse pertinenti** (decisioni del supervisore già prese, autoritative, NON riaprire): **Q-05** (Clausola 1 = state machine 1+6 stati con target_2_hit rimosso; Clausola 3 = submacchina distinta) — `[DOC-INTERNO CAP_02_parte_II.md:7]`; **Q-03** (cap 2 giorni dal raw touch; `missed_target` su target_1) e **Q-02** (ancoraggio al primo pivot post-apertura) — `[DOC-INTERNO CAP_02_parte_II.md:5]`. Di Q-05, in B3 si usano le **Clausole 1 e 3** (state machine + submacchina); la **Clausola 2** (target_2 campo del payload) è **B2** e non si ri-consolida qui (in B3 target_2 entra solo come **evento** `target_2_reached`).

### 2.1 — Censimento M-promemoria (CARRYOVER) per B3

Verificato il registro `tasks/CARRYOVER.md`: **nessun M-promemoria aperto è assegnato a B3**. La state-machine e il position lifecycle sono materia consolidata nei CAP chiusi (Cap.7/11 di CAP-02, chiuso PASS) e non portano M aperti propri. Assegnazioni motivate degli M pertinenti ad altri blocchi (per completezza, **NON da recepire in B3**):

- **M-2 / B-1** (verifica empirica latenza Telegram $L_{max}=30$s, OPEN) → blocco **B4** (consegna Telegram). Fuori scope B3.
- **M-GOV-1 / B-2** (orario sessione 08:00–22:00 CET, APERTO; upgrade empirico da tape DAPI) → blocco **B5** (runtime/sessione). Fuori scope B3. *Attenzione al confine*: in B3 la finestra 8:00–22:00 CET compare **solo** come calendario su cui i counter dei timer avanzano/si arrestano (semantica del timer, citata dal Cap.7.4/7.5); il **requisito di sessione operativa** in sé (con la sua verifica empirica) è B5, **non** B3 — non incardinare M-GOV-1 qui.
- **M-1 / M-9 / M-10** (schemi CANDLE/PRICE/BOOK_5) + **RACC-METODO-2** → blocco **B6** (schema-dato DAPI). Fuori scope B3.
- **M-1 (carryover CAP-03, "primo pivot post-apertura a livello di interfaccia in Parte II")** → **già CLOSED-CAP-04** (trattato in Cap.16 ancoraggio zona) e ripreso in Cap.7.6 come contratto di osservazione. In B3 il **contratto di osservazione real-time** (Cap.7.6) si recepisce **come dato di lifecycle già chiuso**, non come M da riaprire; l'algoritmo di detection resta Parte III (fuori B3).

Nessun M perso; nessun M da incardinare in B3. **Se** durante la review emergesse un M nuovo, lo registra l'Orchestratore in chiusura (non il Developer, non il Planner).

---

## 3. Acceptance Criteria — globali del blocco (il Reviewer audita QUESTI)

**AC-G1 — Atomicità (N1)**: ogni requisito è **una sola proposizione verificabile**. Un requisito che impacchetta più concern (es. "`target_1_hit` è terminale, di successo, chiude il contratto e non transita verso target_2") va **spezzato** in più ID atomici (terminalità; semantica di successo; chiusura del contratto; assenza di transizioni uscenti — separati). Ogni stato terminale con la propria condizione d'ingresso genera requisiti distinti; ogni transizione ammessa è un requisito a sé; ogni edge case del raw touch (a/b/c) è un requisito a sé. La granularità è decisa da te applicando N1; **nessun conteggio-target** è imposto.

**AC-G2 — Tracciabilità obbligatoria**: **ogni** requisito traccia ad almeno una riga del CAP-fonte con la grafia canonica `[DOC-INTERNO CAP_02_parte_II.md:<riga>]`. Un requisito senza tracciabilità è un requisito sbagliato.

**AC-G3 — Valore operativo obbligatorio**: **ogni** requisito dichiara esplicitamente il **valore per l'operatore retail FIB** (perché questo stato/transizione/evento/timer del lifecycle conta per chi riceve ed esegue manualmente il segnale da cellulare — es. "il timer pre-trigger evita che l'operatore resti in attesa indefinita di un raw touch che non arriva"; "la chiusura definitiva in `target_1_hit` dice all'operatore che il segnale non verrà più sostituito e la gestione oltre target_1 è sua"; "il raw touch sempre eseguibile garantisce che, una volta toccata la zona, non ci siano blocchi nascosti che invalidino l'ingresso"). Un requisito senza valore operativo dichiarato è un requisito sbagliato.

**AC-G4 — Divieto "verificato X" di prima istanza (RM-1)**: la spec **richiama** fatti già chiusi nel CAP; **non** introduce nuove dichiarazioni "verificato X" su sistemi esterni di prima istanza. Se un fatto non è asserito nel CAP-fonte, **non** lo asserisci come verificato: lo ometti, oppure lo marchi esplicitamente come assunzione non verificata con la formula RM-1 (`VERIFICA / PROVE / ALTERNATIVE ESCLUSE / ALTERNATIVE NON ESCLUSE`). Preferibile: restare entro ciò che il CAP afferma.

**AC-G5 — Etichette RM-3 su fonti esterne**: ogni riferimento a documentazione esterna (MiFID II, Telegram, Directa, Borsa Italiana/IDEM, calendario di trading) è etichettato `[WIKI-HINT, da verificare]` e **non è mai fonte unica** di un requisito: il requisito regge sul CAP-fonte; l'esterno è solo hint concordante. In B3 le fonti esterne dovrebbero essere marginali (la state machine è materia interna): se ne usi (es. calendario festivi del mercato per i counter dei timer), etichettale.

**AC-G6 — Grafia canonica delle citazioni**: usa `[DOC-INTERNO …]`, `[CODICE-ESISTENTE …]` (grafia canonica; **vietata** la grafia storica `[CODICE-EXISTENTE …]`), `[PROVA-EMPIRICA …]`, `[WIKI-HINT, da verificare]`.

**AC-G7 — Floor citazioni 100% (verifica in review)**: tutte le citazioni `[DOC-INTERNO CAP_02_parte_II.md:<riga>]` devono essere **verificabili token-per-token** contro il CAP-fonte. Il Reviewer le verifica al 100%; una citazione che non risolve è un finding. I numeri di riga del §2 sono puntatori di lavoro: **verificali tu** prima di citarli.

**AC-G8 — Cecità preservata (modalità B)**: l'output non contiene ID-requisito importati da una spec preesistente o da B1/B2, né frasi copiate da `SPEC_FUNZ_01.md` / `_v1_storico` / `SPEC_FUNZ_01_B*.md` / file di chunking. Tracce di questo tipo = **BUG REALE di processo** (Reviewer). I tuoi ID sono auto-assegnati (§4.2).

**AC-G9 — Scope invariato ("tutto e solo")**: i requisiti coprono **tutto e solo** il perimetro Cap.7 (7.1–7.6) + Cap.11 (11.1–11.5) del §1 (stati e semantica; transizioni e precedenza; raw touch come evento + edge case; semantica dei timer pre/post-trigger; contratto di osservazione pivot real-time; submacchina del position lifecycle con target_2 come evento + impatto GA). **Nessun** requisito sconfina in B2 (schema-payload come dato, domini, vincolo $d_{stop}>b$, cardinalità banda, immutabilità del payload, target_2 come campo), in B4 (condizioni/regola di emissione, filtro 80pt come regola, **pubblicazione Telegram del trigger_event**, contratto informativo del messaggio, latenza, anti-duplicato, retry), in B5/Cap.10 (**formato dei tre log**, determinismo bit-exact del replay, granularità/persistenza log), né in Parte III/IV (algoritmo di pivot detection, definizione delle condizioni strutturali di invalidazione, regola di fill virtuale). Materia di Cap.7/11 omessa = gap di copertura (finding); materia fuori perimetro inclusa = scope creep (finding).

**AC-G10 — Matrice di tracciabilità finale + nota di rinvio**: il documento si chiude con una **matrice** `ID requisito | proposizione | citazione CAP (CAP_02_parte_II.md:riga) | valore operativo`. Per il perimetro B3 (due capitoli, Cap.7 + Cap.11) **non** è richiesta una colonna "capitoli non tracciati" estesa all'intera metodologia; è invece richiesta una **nota** che dichiari esplicitamente cosa di adiacente al lifecycle è stato **deliberatamente rinviato** ad altri blocchi e perché (es. schema-payload come dato e immutabilità → B2; condizioni/regola di emissione e filtro 80pt come regola + pubblicazione Telegram del trigger → B4; formato dei log e determinismo del replay → B5/Cap.10; algoritmo di pivot detection e condizioni strutturali di invalidazione → Parte III/IV; tetto numerico $N_{pivot}$ e valori congelati → Parte V), così che il Reviewer possa distinguere un'omissione voluta da un gap.

**AC-G11 — Invarianti di lifecycle evidenziate come tali**: le proprietà **invarianti/strutturali** del ciclo di vita — **terminalità assoluta** degli stati terminali (nessuna transizione uscente; in particolare `target_1_hit` chiude il contratto, NB-9); **vincolo $|\mathcal{A}(t)|\le1$ riferito ai soli segnali attivi** (un segnale terminato non è attivo — citato come premessa da Cap.6.3/7.1, qui usato per disambiguare la sostituzione); **regola di precedenza degli eventi** come condizione del determinismo; **indipendenza della submacchina** (non modifica mai lo stato del segnale) — sono rese come requisiti **strutturali/invarianti** espliciti (non implementativi, non rivedibili), data la loro rilevanza contrattuale e di replay. La distinzione **evento vs stato** (raw touch/`trigger_event` e gli eventi della submacchina sono eventi, non stati) è resa esplicita come invariante di modellazione del lifecycle. *Nota di confine*: il **vincolo $|\mathcal{A}(t)|\le1$ come tale** è stato consolidato in B2 (proprietà del payload-oggetto); in B3 lo si richiama **solo** per la sua conseguenza sul lifecycle (la sostituzione `active→revoked` e l'inapplicabilità della revoca a un segnale terminato), non lo si ri-deriva.

---

## 4. Sezioni da produrre (nel documento `SPEC_FUNZ_01_B3.md`)

> Sono **sezioni**, non capitoli di metodologia. Struttura indicativa; l'importante è coprire il perimetro §1 rispettando gli AC §3.

### 4.1 — Contenuto
1. **Intestazione e scopo del blocco**: cosa copre B3 (state-machine & lifecycle del segnale), che è il blocco 3/8 di una spec ricostruita a blocchi, che il file è autonomo e sarà ricomposto a fine serie. Dichiara la pin del CAP-fonte: `CAP_02_parte_II.md` chiuso PASS `a1625df`. Dichiara lo schema ID (§4.2).
2. **Stati del segnale e semantica**: lo stato non-terminale `active` e i 6 stati terminali, ciascuno con semantica e condizione d'ingresso (un blocco di requisiti per stato), inclusa la causalità di `expired` (`pretrigger_timeout`/`posttrigger_timeout` come campo, non stati); la terminalità assoluta e NB-9.
3. **Transizioni ammesse e precedenza degli eventi**: l'insieme delle transizioni `active→terminale`; l'assenza di transizioni uscenti dai terminali; la regola di precedenza a parità di timestamp come condizione del determinismo.
4. **Raw touch come evento ed esecuzione**: definizione del raw touch; `trigger_event` come evento (non stato); raw touch sempre eseguibile; il motore non osserva il fill manuale; i tre edge case NB-8 (a/b/c) come requisiti distinti. (La **pubblicazione Telegram** del trigger è B4 — **non** trattarla.)
5. **Semantica dei timer (pre/post-trigger)**: $\Delta t_{cromosoma}$ post-trigger (decorrenza da $t_{exec}$, counter sui minuti di trading, arresto notte/weekend/festivi, scadenza→`expired`/`posttrigger_timeout`); $T_{touch}^{max}$ pre-trigger (decorrenza da `timestamp_emission`, scadenza→`expired`/`pretrigger_timeout`, razionale anti-degenerazione). (I **domini come campi** sono B2 — citarli come premessa, non ri-consolidarli.)
6. **Contratto di osservazione del primo pivot real-time (M-1)**: osservazione barre 1-min da 8:00 CET; cadenza = barra chiusa, no tick intra-bar; tetto $N_{pivot}$ non fissato in Parte II (→ Parte V); algoritmo detection → Parte III (non B3).
7. **Position lifecycle: submacchina distinta**: separazione segnale vs posizione; perimetro OUT/IN-scope; struttura della submacchina (ingresso `target_1_hit`, `tracking_active`, eventi `target_2_reached`/`stop_after_target_1`/`retracement_to_entry`/`position_close_event`, terminale `tracking_closed`); target_2 come **evento**; indipendenza assoluta dalla state machine del segnale; impatto GA (space search non esteso; metriche come obiettivi di qualità informativa del payload).
8. **Matrice di tracciabilità + nota di rinvio** (AC-G10).

### 4.2 — Schema ID requisito (auto-assegnato, NON importato)
Adotta uno schema **tuo**, coerente e atomico, ad esempio prefisso per famiglia + numerazione locale del blocco (es. `B3-R-01`, `B3-R-02` per requisiti funzionali/di lifecycle — stati, transizioni, eventi, timer; `B3-CN-01` per requisiti invarianti/strutturali — terminalità assoluta, precedenza degli eventi come condizione di determinismo, indipendenza della submacchina, invariante evento-vs-stato). **Non** riusare la numerazione di alcuna spec preesistente né di B1/B2. Dichiara lo schema all'inizio del documento.

---

## 5. REPORT atteso (`reports/REPORT_SPEC_FUNZ_01_B3.md`)

6 sezioni formato supervisore + tabella di verifica AC:
1. **Cosa è stato prodotto** (sintesi dei requisiti per sezione).
2. **Ipotesi di partenza** (incluso: ho lavorato in cieco dai soli Cap.7 e Cap.11 di `CAP_02_parte_II.md`; conferma delle letture obbligatorie del §0).
3. **Decisioni rilevanti** (scelte di atomicità N1; cosa ho deliberatamente rinviato ad altri blocchi e perché — in particolare la separazione lifecycle vs schema-payload/emissione/Telegram/log-replay; come ho gestito il doppio luogo del `trigger_event` evento-B3 vs notifica-B4; eventuali punti dove ho applicato la cautela RM-1 invece di asserire).
4. **Misura prima/dopo** (qui: copertura del perimetro Cap.7.1–7.6 e Cap.11.1–11.5; non c'è un "prima").
5. **Domande aperte** (eventuali ambiguità; se nessuna, dichiararlo).
6. **Criterio di rollback** (come si annullerebbe B3 senza impattare altri blocchi — è file autonomo).

+ **Tabella verifica AC**: `AC-G1..AC-G11 | OK/PARZIALE/MANCA | evidenza file:riga`. Onestà claim→evidenza (BASE_COMUNE §8): ogni OK ha evidenza puntuale. Includi la sezione **"Applicazione RM-1 a me stesso"** (BASE_COMUNE §8).

### Pre-consegna (checklist Developer)
- [ ] Letti METODO + BASE_COMUNE + spec_developer.md (confermato nel REPORT).
- [ ] Lavorato in **cieco** (non aperti SPEC_FUNZ_01.md / _v1_storico / SPEC_FUNZ_01_B*.md / file di chunking).
- [ ] Ogni requisito è atomico (N1), tracciato (`[DOC-INTERNO CAP_02_parte_II.md:<riga>]`), con valore operativo.
- [ ] Citazioni verificabili token-per-token; grafia canonica.
- [ ] Scope = tutto e solo Cap.7 (7.1–7.6) + Cap.11 (11.1–11.5); rinvii ad altri blocchi annotati nella nota di matrice; nessuno sconfinamento in B2 (schema-payload, domini, immutabilità), B4 (emissione, filtro 80pt come regola, pubblicazione Telegram del trigger, latenza), B5/Cap.10 (formato log, determinismo replay), Parte III/IV (algoritmo pivot, condizioni strutturali invalidazione, fill virtuale).
- [ ] `SPEC_FUNZ_01_B3.md` + `REPORT_SPEC_FUNZ_01_B3.md` scritti; commit `[SPEC-FUNZ-01-B3]` pushato su `origin/main`; `tasks/DEV_STATUS.md` = `READY_FOR_REVIEW`. Poi **fermati**.

---

## 6. Out-of-scope di B3 (con destinazione esplicita)

| Materia | Destinazione |
|---|---|
| Schema-payload come **dato**: campi della tupla $\mathcal{S}$, domini, banda $b$/cardinalità, target_1/2 come campi, `stop_loss`/$d_{stop}$/vincolo $d_{stop}>b$, qualificatori `{structural,synthetic}`, timer $\Delta t_{cromosoma}$/$T_{touch}^{max}$ **come campi**, immutabilità del payload (6.2), segnale unico attivo come proprietà-del-payload (6.3) — Cap.6 | **B2** (Payload del segnale, già CHIUSO PASS `b858a88`) — non ridefinire, non riaprire |
| Condizioni di emissione (volatilità, liquidità, distanza sigma-units), **regola di emissione** e **filtro 80pt come regola** (Cap.8); definizione operativa di $A_{range}$ (Parte IV) | **B4** (emissione & consegna) |
| **Pubblicazione Telegram** del `trigger_event` e dell'emissione, contratto informativo del messaggio/della notifica trigger, ordine dei campi pubblicati, latenza $L_{max}$ (M-2/B-1), anti-duplicato, retry, errori di pubblicazione (Cap.9) | **B4** (emissione & consegna) |
| **Formato** dei tre log (emissione/transizioni/chiusura), **determinismo bit-exact del replay**, granularità temporale/fonte del prezzo del log, persistenza e versionamento del log (Cap.10) | **B5** (runtime, sessione & compliance) — oppure CAP-10/lifecycle log come destinazione naturale |
| Runtime DAPI / **sessione operativa come requisito** / rollover / compliance operativa / **M-GOV-1** (la finestra 8:00–22:00 CET in B3 compare solo come calendario dei counter dei timer) | **B5** (runtime, sessione & compliance) |
| Schema-dato DAPI (CANDLE/PRICE/BOOK_5) / decoder / M-1·M-9·M-10 / RACC-METODO-2 | **B6** (schema-dato DAPI) |
| Gate di go-live: definizione quantitativa del successo, $E[R_{net}]$, DSR/PBO, metriche di lifecycle/rischio come gate decisionale (Cap.5 di CAP-01; Cap.35 di Parte VII) | **B7** (gate di go-live) |
| Confine PHASE-2 / fasizzazione / handoff a FASE-D | **B8** (confine PHASE-2) |
| **Algoritmo** di pivot detection (Cap.15 Parte III); **definizione delle condizioni strutturali** di invalidazione (Parte IV); **regola di fill virtuale** in backtest (Parte III); geometria delle zone, $p_{ref}$ derivato, volatilità condizionata $\hat\sigma_{pt}$ (Parti III/IV) | CAP chiusi, non tracciato in spec (in B3 solo come rinvio) |
| Tetto numerico $N_{pivot}$ e valori congelati dei timer/soglie | **Parte V** (congelamento numerico) — non introdurre numeri in B3 |
| Ambito / operatore / strumento / vincolo solo-emissione / canale a livello di ambito (Cap.1–3 di Parte I) | **B1** (già CHIUSO PASS `7195ffe`) — non ridefinire, non riaprire |
| Assemblaggio degli 8 documenti in un'unica spec consolidata | **task di assemblaggio dedicato dopo B8** |
| `docs/methodology_v2/00_indice.md` | **NON si tocca** (SPEC-FUNZ non è una Parte della metodologia v2) |

---

## 7. Done when (domande operative a cui B3 deve rispondere univocamente)

Al PASS, un lettore deve poter rispondere senza ambiguità, **solo leggendo `SPEC_FUNZ_01_B3.md`**, a:
1. Quali stati può attraversare un segnale nel suo ciclo di vita, e qual è la semantica e la condizione d'ingresso di ciascuno (1 stato `active` + 6 terminali)?
2. Quali transizioni sono ammesse, e perché nessuna transizione esce da uno stato terminale? Cosa significa che `target_1_hit` chiude definitivamente il contratto del segnale?
3. Che cos'è il raw touch, perché è un **evento** e non uno stato, ed è sempre eseguibile? Come si comporta il lifecycle nei tre edge case (prezzo già in zona all'emissione; gap overnight nella zona; gap che salta la zona)?
4. Come funzionano i due timer (pre-trigger $T_{touch}^{max}$ e post-trigger $\Delta t_{cromosoma}$): da quando decorrono, su quale calendario avanzano i counter, e in quale stato/causa fanno transitare il segnale alla scadenza?
5. Qual è la regola di precedenza degli eventi a parità di timestamp, e perché è necessaria?
6. Che cos'è il position lifecycle, perché è una submacchina distinta dal lifecycle del segnale, e perché non modifica mai lo stato del segnale?
7. Cosa è fuori scope dal motore dopo target_1 (gestione della posizione) e cosa è in scope per il reporting (metriche)? Perché lo space search del cromosoma del GA non viene esteso da policy post-target_1? In che senso target_2 è un **evento** della submacchina e non uno stato del segnale?
8. Ogni risposta è tracciabile a una riga di `CAP_02_parte_II.md` (Cap.7 o Cap.11) e porta un valore operativo dichiarato?

---

## 8. Modalità di review (per l'Orchestratore e il Reviewer)

- **Review formale piena adattata al non-CAP**, **sede CLI** (GOV-SURFACES-01). Il Reviewer applica i suoi **due giri ostili** agli **AC di B3** (§3), **non** agli AC dei CAP chiusi (CAP-02 è frozen, non si riaudita).
- Audit documentale **no-DAPI**; **divieto CLI** (niente probe di zelo). Lista **"Empirico-CLI da verificare" attesa VUOTA**.
- **Compito esclusivo del Reviewer — confronto-copertura (modalità B)**: il Reviewer (e **solo** lui, dopo aver auditato gli AC) confronta i requisiti di B3 con il **perimetro corrispondente di `docs/spec_funzionale/SPEC_FUNZ_01.md` (v2 congelata, PASS `ab7450f`)** limitatamente all'ambito **state-machine & lifecycle (Cap.7 e Cap.11 di Parte II)**, per verificare che **nessun requisito di prodotto del perimetro lifecycle sia caduto** nella ricostruzione cieca e per segnalare divergenze (in più / in meno) con classificazione. Questo è il punto in cui la cecità del Developer viene "chiusa". Attenzione al confine: requisiti della v2 che appartengono a schema-payload/emissione/Telegram/log **non** sono buchi di B3 (sono B2/B4/B5) — il Reviewer li classifica come "fuori perimetro B3", non come gap.
- **Cecità del Developer come oggetto di audit**: il Reviewer cerca attivamente tracce di rottura della cecità (ID importati da v2 o da B1/B2, frasi identiche alla v2 non presenti nel Cap.7/11); se trovate → **BUG REALE**.
- Verdetto **PASS / CONDITIONAL / FAIL** con tabella "Classificazione per il supervisore". ≥1 BUG REALE ⇒ non-PASS.

---

## 9. Pipeline attesa (per l'Orchestratore)

1. **spec_developer** (CLI, via general-purpose che adotta `spec_developer.md`) costruisce `docs/spec_funzionale/SPEC_FUNZ_01_B3.md` + `reports/REPORT_SPEC_FUNZ_01_B3.md` **in cieco** (vincolo §0.1), scrive `READY_FOR_REVIEW` in `tasks/DEV_STATUS.md`, si ferma. Non committa il task card (lo fa l'Orchestratore).
2. **Orchestratore**: **check post-Developer** (6 controlli, **condizione-3 indice = N/A**; "commit copre i file attesi" = `SPEC_FUNZ_01_B3.md` + `REPORT_SPEC_FUNZ_01_B3.md` + `DEV_STATUS.md`). Se OK → invoca il Reviewer; altrimenti rilancia il Developer con prompt mirato ai gap.
3. **spec_reviewer** (CLI, via general-purpose che adotta `spec_reviewer.md`): audit ostile sugli AC di B3 + confronto-copertura col perimetro lifecycle (Cap.7+Cap.11) della v2 congelata (§8); verdetto.
4. **CONDITIONAL/FAIL** → punto di controllo supervisore. **PASS** → chiusura B (7 condizioni adattate, indice = N/A); marcatore `SPEC-FUNZ-01-B3: CHIUSO PASS <sha-review>` in `tasks/STATO_CORRENTE.md`; poi il supervisore decide l'apertura di **B4**.

---

*Task card scritta dallo spec_planner. NON committata dal Planner (lo fa l'Orchestratore). Nessuna spec scritta, nessun CAP modificato (freeze G-09 rispettato). Questa card non contiene ID-requisito né contenuti copiati dalla v2 / da B1 / da B2 / dai file di chunking: cecità preservata.*
