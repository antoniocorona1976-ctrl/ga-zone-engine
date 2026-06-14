# TASK ATTIVO: SPEC-FUNZ-01-B1 — Ambito & operatore (ricostruzione cieca, modalità B, blocco 1/8)

> **Track**: Business-spec (SPEC-FUNZ). **Sede**: CLI per tutto il ciclo (GOV-SURFACES-01, METODO §Superfici). **Tag commit**: `[SPEC-FUNZ-01-B1]`. Tutto su `main` (trunk); isolamento via cartella dedicata, non via branch.
>
> **Letture obbligatorie del Developer, in quest'ordine, PRIMA di scrivere**: `tasks/METODO.md` (RM-1..RM-4 + RACC-METODO-2), `.claude/BASE_COMUNE.md` (ciclo, sede CLI per la spec, onestà claim→evidenza), `.claude/agents/spec_developer.md` (il tuo ruolo), questo `tasks/ACTIVE_TASK.md`. Conferma in testa al REPORT di averli letti.

---

## 0. Natura del blocco e modalità di lavoro (LEGGERE PRIMA DI TUTTO)

Questo è il **primo** di **8 blocchi** (B1→B8) in cui la business-spec del progetto viene **ricostruita ex-novo**, **uno alla volta**. Ogni blocco = un ciclo Planner→Developer→Reviewer = un PASS. Gli 8 documenti, a fine serie (dopo B8), verranno ricomposti in un'unica spec consolidata da un **task di assemblaggio dedicato**: l'assemblaggio è **FUORI SCOPE di B1** (non eseguirlo, non anticiparlo).

### 0.1 — VINCOLO DI CECITÀ (cardine della modalità B — leggere con la massima attenzione)

Tu (Developer) costruisci i requisiti **DAI SOLI CAP-fonte** elencati al §1, **cieco** rispetto a qualsiasi specifica funzionale già esistente. È **TASSATIVAMENTE VIETATO** aprire, leggere, consultare, citare o parafrasare:

1. `docs/spec_funzionale/SPEC_FUNZ_01.md` (la spec v2 congelata) e qualsiasi file `*_v1_storico*`;
2. qualunque file di **pianificazione/chunking** del track business-spec (es. `PROPOSTA_SUDDIVISIONE_SPEC*.md`): contengono la mappa dei requisiti già esistenti — leggerli romperebbe la cecità;
3. qualsiasi altro documento che enumeri requisiti `R-*`, `NFR-*`, `CN-*` già definiti altrove.

Ti appoggi **esclusivamente** a: questa task card **+** i CAP-fonte del §1. Numeri gli ID requisito **da zero, autonomamente**, secondo lo schema del §4.2 — **non** riusare ID presi da una spec preesistente.

Il **confronto-copertura** con la spec già esistente è compito **esclusivo del Reviewer in fase di review** (modalità B già validata sul track). Non è compito tuo e non devi tentarlo.

> Perché: la cecità garantisce che i requisiti derivino dal contenuto metodologico chiuso e non da una parafrasi di lavoro precedente. Tracce di una spec preesistente nel tuo output (ID copiati, frasi identiche non presenti nei CAP-fonte) sono trattate dal Reviewer come **BUG REALE di processo**.

---

## 1. Perimetro-fonte (cosa derivi) — SOLO questo

**Fonte unica e autoritativa**: `docs/methodology_v2/CAP_01_parte_I.md`, **limitatamente ai Capitoli 1, 2 e 3**.

- **CAP-01 è chiuso PASS con SHA confermato `b76c32c`** (`tasks/STATO_CORRENTE.md:7`). A differenza di altri CAP, qui **non** c'è dipendenza fragile da `<sha-da-confermare>`: B1 è "pulito" sul fronte SHA. Cita il file con provenienza `[DOC-INTERNO CAP_01_parte_I.md:<riga>]`. È un capitolo **congelato** (freeze G-09): **sola lettura**, non lo modifichi.

I **temi** del perimetro (descritti per contenuto, non per struttura di alcuna spec):

- **Obiettivo operativo del prodotto-segnale (Cap.1)**: il sistema genera segnali long/short sul FIB; finestra/sessione operativa di riferimento 08:00–22:00 CET come ambito; natura intraday del segnale con possibile estensione multiday entro un tetto; doppia formulazione del target operativo dichiarato dall'operatore (profitto netto giornaliero in punti FIB **oppure** quota del movimento strutturale intraday); il ruolo del contesto indici correlati per la classificazione del regime (a livello di ambito).
- **Vincolo strutturale "solo emissione, nessuna esecuzione di ordini" (Cap.1)**: il sistema **non esegue ordini** in alcuna fase; pubblica segnali su un canale di notifica; apertura/invio/gestione/chiusura competono esclusivamente all'operatore umano. È un **vincolo strutturale**, non una scelta implementativa rivedibile.
- **Profilo dell'operatore e vincoli operativi (Cap.2)**: operatore retail non professionale ai sensi MiFID II; opera **da cellulare**, in modo discontinuo, durante la giornata lavorativa; **1 contratto FIB alla volta**; **commissioni 5 EUR/operazione** (apertura e chiusura); distinzione fra stop loss strutturale del segnale e stop personale dell'operatore (a livello di profilo/ambito); rollover riconosciuto come problematica operativa (a livello di ambito; il dettaglio della policy è di altre Parti — vedi out-of-scope).
- **Strumento FIB (Cap.1–2)**: futures mini su FTSE MIB, mercato IDEM di Borsa Italiana, **moltiplicatore 5 EUR/punto indice**, **tick discreto 5pt** (prezzi/bande multipli di 5).
- **Infrastruttura/canale a livello di ambito (Cap.3)**: hardware locale dichiarato; broker **Directa SIM** come fonte del feed real-time; **canale di pubblicazione = bot Telegram** dell'operatore (a livello di **ambito** — "i segnali sono pubblicati via Telegram"; il **dettaglio di consegna** — schema messaggio, chat ID, latenza — **NON** è B1, vedi out-of-scope); fonte storico per il training; necessità di dati cross-index.

**Regola di confine "tutto e solo"**: lo scope di B1 è **tutto e solo** il contenuto di prodotto dei Cap.1–3 sopra elencato, **niente di più, niente di meno**. Se incontri nei Cap.1–3 materia che appartiene a un blocco successivo (payload formale, state-machine, condizioni di emissione, schema-dato, gate di go-live, ecc.), **non** la consolidi qui: la lasci al suo blocco (vedi §6 out-of-scope). Cap.4 (compute budget/cloud) e Cap.5 (definizione quantitativa del successo / metriche / DSR-PBO) di CAP-01 **non** rientrano in B1 (vedi §6).

---

## 2. Eredità autoritativa pertinente a B1 (NON ri-verificare — citala col livello-fonte)

I seguenti fatti sono **autoritativi**: "autoritativo" = **non ri-fetchare e non ri-derivare**, NON promozione di livello-fonte. Nessuna conclusione strutturale può poggiare su una fonte solo `[WIKI-HINT]`.

- Vincolo "solo emissione, nessuna esecuzione di ordini" — `[DOC-INTERNO CAP_01_parte_I.md:15]`.
- Strumento FIB: moltiplicatore **5 EUR/punto** — `[DOC-INTERNO CAP_01_parte_I.md:9, :25]`; **tick discreto 5pt**, prezzi/bande multipli di 5 — nota di progetto FIB (cita la riga CAP dove la granularità a 5pt è desumibile, es. l'esempio banda `41100 41140` `[DOC-INTERNO CAP_01_parte_I.md:27]`; se nel CAP non è asserito esplicitamente "tick 5pt", **non** asserirlo come "verificato" — vedi RM-1 al §3).
- Profilo operatore: **retail non professionale MiFID II**, **mobile**, **1 contratto alla volta** — `[DOC-INTERNO CAP_01_parte_I.md:23, :25]`.
- **Commissioni 5 EUR/operazione** (= 1 punto FIB equivalente; ciclo completo = 2 punti) — `[DOC-INTERNO CAP_01_parte_I.md:25]`.
- **Sessione operativa 08:00–22:00 CET** (finestra unica e continua) — `[DOC-INTERNO CAP_01_parte_I.md:9]`. Riferimento esterno concordante: `[WIKI-HINT Borsa Italiana Trading Hours, da verificare]` — **mai fonte unica**, il fatto regge sul CAP.
- **Canale di pubblicazione = bot Telegram** (a livello di ambito) — `[DOC-INTERNO CAP_01_parte_I.md:47]`.
- **Q chiuse pertinenti** (decisioni del supervisore già prese, autoritative, NON riaprire): Q-01 (sessione 08:00–22:00 continua), Q-02 (ancoraggio del movimento strutturale al primo pivot post-apertura), Q-03 (128/150/B=2000 parametri provvisori di solo dimensionamento), Q-04 (cap validità multiday a 2 giorni di trading dal raw touch) — `[DOC-INTERNO tasks/QUESTIONS.md:Q-01..Q-04]`.

### 2.1 — Censimento M-promemoria (CARRYOVER) per B1

Verificato il registro `tasks/CARRYOVER.md`: **nessun M-promemoria aperto è assegnato a B1**. Assegnazioni motivate (per completezza, NON da recepire qui):
- **M-2 / B-1** (latenza Telegram, OPEN) → blocco **B4** (consegna Telegram). Fuori scope B1.
- **M-GOV-1 / B-2** (orario sessione, APERTO; upgrade empirico da tape DAPI) → blocco **B5** (runtime/sessione). Fuori scope B1, **ma** il fatto "sessione 08:00–22:00" è già un dato autoritativo di ambito (§2): in B1 lo si **cita come ambito dal CAP**, senza riaprire la verifica empirica (che resta a B5/CAP-DATA).
- **M-1 / M-9 / M-10** (schemi CANDLE/PRICE/BOOK_5) + **RACC-METODO-2** → blocco **B6** (schema-dato). Fuori scope B1.

Nessun M perso; nessun M da incardinare in B1.

---

## 3. Acceptance Criteria — globali del blocco (il Reviewer audita QUESTI)

**AC-G1 — Atomicità (N1)**: ogni requisito è **una sola proposizione verificabile**. Un requisito che impacchetta più concern (es. "il sistema opera su FIB e pubblica via Telegram e non esegue ordini") va **spezzato** in più ID atomici. La granularità è decisa da te applicando N1; **nessun conteggio-target** è imposto.

**AC-G2 — Tracciabilità obbligatoria**: **ogni** requisito traccia ad almeno una riga del CAP-fonte con la grafia canonica `[DOC-INTERNO CAP_01_parte_I.md:<riga>]`. Un requisito senza tracciabilità è un requisito sbagliato.

**AC-G3 — Valore operativo obbligatorio**: **ogni** requisito dichiara esplicitamente il **valore per l'operatore retail FIB** (perché questo requisito conta per chi riceve ed esegue manualmente il segnale da cellulare). Un requisito senza valore operativo dichiarato è un requisito sbagliato.

**AC-G4 — Divieto "verificato X" di prima istanza (RM-1)**: la spec **richiama** fatti già chiusi nei CAP; **non** introduce nuove dichiarazioni "verificato X" su sistemi esterni di prima istanza. Se un fatto non è asserito nel CAP-fonte, **non** lo asserisci come verificato: lo ometti, oppure lo marchi esplicitamente come assunzione non verificata con la formula RM-1 (`VERIFICA / PROVE / ALTERNATIVE ESCLUSE / ALTERNATIVE NON ESCLUSE`). Preferibile: restare entro ciò che il CAP afferma.

**AC-G5 — Etichette RM-3 su fonti esterne**: ogni riferimento a documentazione esterna (MiFID II, Borsa Italiana / orari, Telegram, Directa) è etichettato `[WIKI-HINT, da verificare]` e **non è mai fonte unica** di un requisito: il requisito regge sul CAP-fonte; l'esterno è solo hint concordante.

**AC-G6 — Grafia canonica delle citazioni**: usa `[DOC-INTERNO …]`, `[CODICE-ESISTENTE …]` (grafia canonica; **vietata** la grafia storica `[CODICE-EXISTENTE …]`), `[PROVA-EMPIRICA …]`, `[WIKI-HINT, da verificare]`.

**AC-G7 — Floor citazioni 100% (verifica in review)**: tutte le citazioni `[DOC-INTERNO CAP_01_parte_I.md:<riga>]` devono essere **verificabili token-per-token** contro il CAP-fonte. Il Reviewer le verifica al 100%; una citazione che non risolve è un finding.

**AC-G8 — Cecità preservata (modalità B)**: l'output non contiene ID-requisito importati da una spec preesistente, né frasi copiate da `SPEC_FUNZ_01.md`/`_v1_storico`/file di chunking. Tracce di questo tipo = **BUG REALE di processo** (Reviewer). I tuoi ID sono auto-assegnati (§4.2).

**AC-G9 — Scope invariato ("tutto e solo")**: i requisiti coprono **tutto e solo** il perimetro Cap.1–3 del §1 (ambito / operatore / strumento / vincolo solo-emissione / canale a livello ambito). Nessun requisito sconfina in B2..B8 o in Cap.4/Cap.5 (vedi §6). Materia di Cap.1–3 omessa = gap di copertura (finding); materia fuori perimetro inclusa = scope creep (finding).

**AC-G10 — Matrice di tracciabilità finale**: il documento si chiude con una **matrice** `ID requisito | proposizione | citazione CAP | valore operativo`. Per il perimetro B1 (un solo CAP, Cap.1–3) **non** è richiesta una colonna "capitoli non tracciati" estesa all'intera metodologia; è invece richiesta una **nota** che dichiari esplicitamente cosa dei Cap.1–3 è stato **deliberatamente rinviato** ad altri blocchi e perché (es. dettaglio Telegram → B4; rollover policy → altra Parte), così che il Reviewer possa distinguere un'omissione voluta da un gap.

**AC-G11 — Vincolo strutturale evidenziato**: il vincolo "solo emissione, nessuna esecuzione di ordini" è reso come requisito **strutturale** esplicito (non implementativo, non rivedibile), data la sua rilevanza compliance/prodotto.

---

## 4. Sezioni da produrre (nel documento `SPEC_FUNZ_01_B1.md`)

> Sono **sezioni**, non capitoli di metodologia. Struttura indicativa; l'importante è coprire il perimetro §1 rispettando gli AC §3.

### 4.1 — Contenuto
1. **Intestazione e scopo del blocco**: cosa copre B1 (ambito & operatore), che è il blocco 1/8 di una spec ricostruita a blocchi, che il file è autonomo e sarà ricomposto a fine serie. Dichiara la pin del CAP-fonte: `CAP_01_parte_I.md` chiuso PASS `b76c32c`.
2. **Ambito del prodotto-segnale**: obiettivo operativo, strumento FIB, sessione/finestra operativa come ambito, natura intraday/estensione multiday (a livello di ambito), target operativo dichiarato (doppia formulazione), contesto cross-index per il regime (a livello di ambito).
3. **Vincolo strutturale "solo emissione"**: requisito/i strutturale/i sul fatto che il sistema non esegue ordini e pubblica solo segnali; confine di responsabilità sistema vs operatore.
4. **Profilo operatore e vincoli operativi**: retail MiFID II, mobile/discontinuo, 1 contratto alla volta, commissioni 5 EUR/op, distinzione stop strutturale vs stop personale (a livello profilo), rollover come vincolo di ambito.
5. **Strumento FIB**: moltiplicatore 5 EUR/pt, tick 5pt (con la cautela RM-1 del §2/§3), IDEM/Borsa Italiana.
6. **Canale e infrastruttura a livello di ambito**: feed real-time da Directa; pubblicazione via bot Telegram come canale (ambito, **non** dettaglio consegna).
7. **Matrice di tracciabilità + nota di rinvio** (AC-G10).

### 4.2 — Schema ID requisito (auto-assegnato, NON importato)
Adotta uno schema **tuo**, coerente e atomico, ad esempio prefisso per famiglia + numerazione locale del blocco (es. `B1-R-01`, `B1-R-02` per requisiti funzionali/di ambito; `B1-CN-01` per requisiti compliance/normativi come MiFID II e "no esecuzione ordini"). **Non** riusare la numerazione di alcuna spec preesistente. Dichiara lo schema all'inizio del documento.

---

## 5. REPORT atteso (`reports/REPORT_SPEC_FUNZ_01_B1.md`)

6 sezioni formato supervisore + tabella di verifica AC:
1. **Cosa è stato prodotto** (sintesi dei requisiti per sezione).
2. **Ipotesi di partenza** (incluso: ho lavorato in cieco dai soli Cap.1–3; conferma delle letture obbligatorie).
3. **Decisioni rilevanti** (scelte di atomicità N1; cosa ho deliberatamente rinviato ad altri blocchi e perché; eventuali punti dove ho applicato la cautela RM-1 invece di asserire).
4. **Misura prima/dopo** (qui: copertura del perimetro Cap.1–3; non c'è un "prima").
5. **Domande aperte** (eventuali ambiguità; se nessuna, dichiararlo).
6. **Criterio di rollback** (come si annullerebbe B1 senza impattare altri blocchi — è file autonomo).

+ **Tabella verifica AC**: `AC-G1..AC-G11 | OK/PARZIALE/MANCA | evidenza file:riga`. Onestà claim→evidenza (BASE_COMUNE §8): ogni OK ha evidenza puntuale. Includi la sezione **"Applicazione RM-1 a me stesso"** (BASE_COMUNE §8).

### Pre-consegna (checklist Developer)
- [ ] Letti METODO + BASE_COMUNE + spec_developer.md (confermato nel REPORT).
- [ ] Lavorato in **cieco** (non aperti SPEC_FUNZ_01.md / _v1_storico / file di chunking).
- [ ] Ogni requisito è atomico (N1), tracciato (`[DOC-INTERNO CAP_01_parte_I.md:<riga>]`), con valore operativo.
- [ ] Citazioni verificabili token-per-token; grafia canonica.
- [ ] Scope = tutto e solo Cap.1–3; rinvii ad altri blocchi annotati nella nota di matrice.
- [ ] `SPEC_FUNZ_01_B1.md` + `REPORT_SPEC_FUNZ_01_B1.md` scritti; commit `[SPEC-FUNZ-01-B1]` pushato su `origin/main`; `tasks/DEV_STATUS.md` = `READY_FOR_REVIEW`. Poi **fermati**.

---

## 6. Out-of-scope di B1 (con destinazione esplicita)

| Materia | Destinazione |
|---|---|
| Payload formale del segnale (campi, banda $b$, target 1/2, stop strutturale come schema) | **B2** (payload) |
| State-machine / lifecycle del segnale (stati, transizioni, timer attesa/esecuzione) | **B3** (state-machine & lifecycle) |
| Condizioni di emissione + **dettaglio consegna Telegram** (schema messaggio, chat ID, latenza $L_{max}$, M-2/B-1) | **B4** (emissione & consegna) |
| Runtime DAPI / sessione operativa come requisito operativo / rollover policy / audit / compliance operativa / M-GOV-1 orario empirico | **B5** (runtime, sessione & compliance) |
| Schema-dato DAPI (CANDLE/PRICE/BOOK_5) / decoder / continuità tape / M-1·M-9·M-10 / RACC-METODO-2 | **B6** (schema-dato) |
| Gate di go-live: definizione quantitativa del successo, $E[R_{net}]$, DSR/PBO, filtro 80pt, metriche di lifecycle/rischio (**= Cap.5 di CAP-01**) | **B7** (gate di go-live) |
| Confine PHASE-2 / fasizzazione / handoff a FASE-D | **B8** (confine PHASE-2) |
| Compute budget e strategia cloud (**= Cap.4 di CAP-01**) | non tracciato in spec (dimensionamento infra) / eventuale Appendice operativa |
| Matematica interna del modello (Parti III/IV/V) | CAP chiusi, non tracciato in spec |
| Assemblaggio degli 8 documenti in un'unica spec consolidata | **task di assemblaggio dedicato dopo B8** |
| `docs/methodology_v2/00_indice.md` | **NON si tocca** (SPEC-FUNZ non è una Parte della metodologia v2) |

---

## 7. Done when (domande operative a cui B1 deve rispondere univocamente)

Al PASS, un lettore deve poter rispondere senza ambiguità, **solo leggendo `SPEC_FUNZ_01_B1.md`**, a:
1. Che cosa fa il prodotto (genera segnali long/short sul FIB) e su quale strumento/sessione opera?
2. Qual è il target operativo dichiarato e nelle sue due formulazioni?
3. Il sistema esegue ordini? (No — vincolo strutturale; confine di responsabilità sistema/operatore.)
4. Chi è l'operatore, con quali vincoli (retail MiFID II, mobile, 1 contratto, commissioni 5 EUR/op)?
5. Quali sono le caratteristiche economiche dello strumento FIB rilevanti per l'operatore (5 EUR/pt, tick 5pt)?
6. Su quale canale e da quale broker arrivano feed e segnali, a livello di ambito (Directa; Telegram)?
7. Ogni risposta è tracciabile a una riga di `CAP_01_parte_I.md` e porta un valore operativo dichiarato?

---

## 8. Modalità di review (per l'Orchestratore e il Reviewer)

- **Review formale piena adattata al non-CAP**, **sede CLI** (GOV-SURFACES-01). Il Reviewer applica i suoi **due giri ostili** agli **AC di B1** (§3), **non** agli AC dei CAP chiusi (CAP-01 è frozen, non si riaudita).
- Audit documentale **no-DAPI**; **divieto CLI** (niente probe di zelo). Lista **"Empirico-CLI da verificare" attesa VUOTA**.
- **Compito esclusivo del Reviewer — confronto-copertura (modalità B)**: il Reviewer (e **solo** lui, dopo aver auditato gli AC) confronta i requisiti di B1 con il **perimetro corrispondente di `docs/spec_funzionale/SPEC_FUNZ_01.md` (v2 congelata, PASS `ab7450f`)** limitatamente all'ambito Cap.1–3 (ambito & operatore), per verificare che **nessun requisito di prodotto del perimetro sia caduto** nella ricostruzione cieca e per segnalare divergenze (in più / in meno) con classificazione. Questo è il punto in cui la cecità del Developer viene "chiusa".
- **Cecità del Developer come oggetto di audit**: il Reviewer cerca attivamente tracce di rottura della cecità (ID importati, frasi identiche alla v2 non presenti nei Cap.1–3); se trovate → **BUG REALE**.
- Verdetto **PASS / CONDITIONAL / FAIL** con tabella "Classificazione per il supervisore". ≥1 BUG REALE ⇒ non-PASS.

---

## 9. Pipeline attesa (per l'Orchestratore)

1. **spec_developer** (CLI, via general-purpose che adotta `spec_developer.md`) costruisce `docs/spec_funzionale/SPEC_FUNZ_01_B1.md` + `reports/REPORT_SPEC_FUNZ_01_B1.md` **in cieco** (vincolo §0.1), scrive `READY_FOR_REVIEW` in `tasks/DEV_STATUS.md`, si ferma. Non committa il task card (lo fa l'Orchestratore).
2. **Orchestratore**: **check post-Developer** (6 controlli, **condizione-3 indice = N/A**; "commit copre i file attesi" = `SPEC_FUNZ_01_B1.md` + `REPORT_SPEC_FUNZ_01_B1.md` + `DEV_STATUS.md`). Se OK → invoca il Reviewer; altrimenti rilancia il Developer con prompt mirato ai gap.
3. **spec_reviewer** (CLI, via general-purpose che adotta `spec_reviewer.md`): audit ostile sugli AC di B1 + confronto-copertura col perimetro Cap.1–3 della v2 congelata (§8); verdetto.
4. **CONDITIONAL/FAIL** → punto di controllo supervisore. **PASS** → chiusura B (7 condizioni adattate, indice = N/A); marcatore `SPEC-FUNZ-01-B1: CHIUSO PASS <sha-review>` in `tasks/STATO_CORRENTE.md`; poi il supervisore decide l'apertura di **B2**.

---

*Task card scritta dallo spec_planner. NON committata dal Planner (lo fa l'Orchestratore). Nessuna spec scritta, nessun CAP modificato (freeze G-09 rispettato). Questa card non contiene ID-requisito né contenuti copiati dalla v2 / dai file di chunking: cecità preservata.*
