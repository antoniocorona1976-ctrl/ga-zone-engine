# TASK ATTIVO: SPEC-FUNZ-01-B8 — Confine / chiusura della spec (ricostruzione cieca, modalità B, blocco 8/8 — ULTIMO)

> **Track**: Business-spec (SPEC-FUNZ). **Sede**: CLI (GOV-SURFACES-01, METODO §Superfici). **Tag commit**: `[SPEC-FUNZ-01-B8]`. Tutto su `main` (trunk; isolamento via cartella `docs/spec_funzionale/`, non via branch).
>
> **⚠️ VINCOLO CARDINE DI B8 — blocco di CONFINE/CHIUSURA, non materia-prodotto nuova.** B8 è l'**ultimo blocco** della serie. Consolida la **fasizzazione dichiarata** del prodotto (PHASE-1 FIB-only in scope; PHASE-2 cross-index fuori scope = dichiarazione normativa senza implementazione) e l'**enumerazione delle dipendenze aperte verso FASE-D**. **NON** apre materia nuova del motore, **NON** ri-deriva i blocchi precedenti, **NON** risolve le dipendenze aperte (le **dichiara** come aperte). Due trappole da gestire PRIMA di derivare:
>   1. **Rischio framing/0-req alto.** Molti capitoli toccati sono capitoli di "rinvii / punti aperti / confine" (Cap.55, Cap.64) o capitoli **già di proprietà** di altri blocchi (Cap.36.3 → B7; Cap.53 → B5). Applica la **verifica di fondazione** capitolo per capitolo: se un capitolo non porta una proposizione-prodotto di **confine/fasizzazione/dipendenza-aperta** non già coperta altrove, citalo come **premessa**, non scrivere un requisito su di esso.
>   2. **"Assemblaggio della serie B1..B8 in un unico documento" NON è un requisito di B8.** È un **task separato** (post-B8). Stessa cosa per **l'avvio FASE-D**: è la fase dopo, non un requisito B8. Se ti viene da scrivere un requisito "assembla i blocchi" / "indicizza B1..B7" / "avvia FASE-D", **fermati**: è meta-processo, non materia-prodotto.
>
> **SHA frozen pinnabili** (freeze G-09; **nessuna dipendenza fragile**; `git diff <frozen> HEAD -- <file>` verificato **vuoto** per tutti):
> - `CAP_08_parte_8.md` = `015c47a` (Cap.42, fonte primaria)
> - `CAP_09_parte_9.md` = `28cfd2d` (Cap.55 confine/punti aperti; Cap.53 premessa)
> - `CAP_10_parte_10.md` = `41447d3` (Cap.64 confine/punti aperti)
> - `CAP_07_parte_VII.md` = `b27c1e3` (Cap.36.3 carryover — **premessa, owned B7**)
> **NB (analogo B7-F4)**: per `CAP_09` e `CAP_10` lo SHA del marcatore di chiusura PASS (`86425a7` / `48171e4`) **non** è content-autoritativo a HEAD: i file sono evoluti post-PASS via audit-RM (CAP-DATA-02/03, giu 2026). Lo SHA frozen autoritativo è l'ultimo commit che tocca il file (`28cfd2d` / `41447d3`), `diff` a HEAD vuoto. Il Developer legge a HEAD (AC-G7).
>
> **Perimetro (per CAPITOLI — modalità B)**: deriva i requisiti di prodotto **dai capitoli di fonte primaria §1** (`CAP_08 Cap.42` + `CAP_09 Cap.55` + `CAP_10 Cap.64`); i capitoli §5 (Cap.36.3, Cap.53, Cap.41) sono **premesse** (cita per riga, NON ri-derivare). Assegna gli ID `B8-R-NN`/`B8-CN-NN`/`B8-NFR-NN` **da zero**, applicando l'atomicità N1. **Nessun conteggio-target è imposto.** NB path: numero **arabo** per Parte 8/9/10 (`CAP_08_parte_8.md`, `CAP_09_parte_9.md`, `CAP_10_parte_10.md`); **romano** per Parte VII (`CAP_07_parte_VII.md`).
>
> **Letture obbligatorie del Developer, in quest'ordine, PRIMA di scrivere**: `tasks/METODO.md` (RM-1..RM-4 + RACC-METODO-2 + §Superfici + Freeze G-09), `.claude/BASE_COMUNE.md`, `.claude/agents/spec_developer.md`, questo `tasks/ACTIVE_TASK.md`. Conferma in testa al REPORT di averli letti.
>
> **Pre-flight Developer — verifica freeze G-09 prima di fidarti dei pin §1**: esegui `git diff 015c47a HEAD -- docs/methodology_v2/CAP_08_parte_8.md`, `git diff 28cfd2d HEAD -- docs/methodology_v2/CAP_09_parte_9.md`, `git diff 41447d3 HEAD -- docs/methodology_v2/CAP_10_parte_10.md`, `git diff b27c1e3 HEAD -- docs/methodology_v2/CAP_07_parte_VII.md`; **tutti e quattro devono essere vuoti**. Se un diff **non** è vuoto, i pin-riga §1/§5 di quel file sono **slittati** → rileggi token-per-token (AC-G7) e cita la riga **reale** a HEAD. (Verificato in setup: a HEAD tutti e quattro i diff sono vuoti con questi SHA — vedi `Business Spec/Final/ESITO_B8-01.md`.)

---

## 0. Natura e cecità

**Natura**: ricostruzione cieca da zero del perimetro **Confine / chiusura della spec** — la traduzione in requisiti di prodotto della **fasizzazione PHASE-1/PHASE-2** e delle **dipendenze aperte verso FASE-D**, ultimo blocco della serie. B1..B7 sono chiusi PASS; B8 chiude la copertura della spec.

### 0.1 — Vincolo di cecità (modalità B)

Il Developer deriva i requisiti **DAI SOLI** capitoli del perimetro §1 (+ premesse §5 citate), **cieco** rispetto a:
- `docs/spec_funzionale/SPEC_FUNZ_01.md` (v2 congelata) e ogni `*_v1_storico*`;
- i **file di chunking** (`docs/spec_funzionale/PROPOSTA_SUDDIVISIONE_SPEC*.md`);
- i documenti dei blocchi precedenti (`docs/spec_funzionale/SPEC_FUNZ_01_B1.md` .. `SPEC_FUNZ_01_B7.md`).

Il confronto-copertura con la v2 e la partizione dei requisiti sono compito **esclusivo del Reviewer/Orchestratore** (§9): il Developer **non li vede e non li deve cercare**. Gli ID `B8-*` sono auto-assegnati da zero, con atomicità N1.

**NB — nessuna eccezione RM-2 "leggi i decoder" in B8.** Il perimetro di B8 è **interamente interno/documentale** (confine di fasizzazione + rinvii a FASE-D): **non c'è alcun decoder/parser di sistema esterno** in scope, quindi nessun rischio RM-2/RM-3 da schema esterno e nessuna lettura imposta di codice di decodifica. La sola fonte autoritativa è il testo dei capitoli §1 (e le premesse §5 per riga). I `[PROVA-EMPIRICA]` citati nei capitoli (es. abilitazione FDAX) si **riportano come fatti già dichiarati dal capitolo frozen**, non si ri-verificano (no probe di zelo).

---

## 1. Perimetro-fonte — materia da derivare, PER CAPITOLO (fonte primaria)

Fonte primaria: `docs/methodology_v2/CAP_08_parte_8.md` (Cap.42) + `docs/methodology_v2/CAP_09_parte_9.md` (Cap.55) + `docs/methodology_v2/CAP_10_parte_10.md` (Cap.64). I pin sotto sono **puntatori di lavoro** verificati in CLI dall'Orchestratore; il Developer li **rilegge token-per-token** (AC-G7) prima di citarli e cita la riga reale.

- **Cap.42 — Convenzione cross-index (PHASE-2)** (`CAP_08_parte_8.md:141`) — **fonte primaria, req-bearing.** Materia di confine/fasizzazione:
  - **fasizzazione PHASE-1 FIB-only esplicita** (single-instrument FIB, senza layer di covarianza cross-index): la fasizzazione è **dichiarata, non semplificazione silenziosa** `:143`; il doc v2 è esplicitamente single-instrument FIB, preambolo "rimozione dei layer multi-indice (DCC/ADCC/BEKK, covarianza cross-index, N≥8)" `:145`; **vincolo di fasizzazione PHASE-1 vs PHASE-2** `:167` (la convenzione cross-index è normativa **come dichiarazione**, attivazione operativa rinviata a PHASE-2; PHASE-1 istanzia la specifica solo sul FIB, con costi noti — σ_sys→σ_local, feature tensor senza canali cross-index, S_xidx non calcolabile);
  - **cross-index PHASE-2 = dichiarazione normativa SENZA implementazione** nel doc v2 corrente `:143`; strumenti previsti DAX (FDAX/Eurex), EuroStoxx 50 (FESX/Eurex), S&P 500 mini (ES/CME) `:147`; **estensioni future esplicite** (DCC/ADCC/cDCC, Realized GARCH, S_xidx + quinta famiglia catalogo target) dichiarate **non implementate** `:176`.
- **Cap.55 — Punti aperti fuori scope (Parte 9)** (`CAP_09_parte_9.md:383`) — **fonte del confine "dipendenze aperte verso FASE-D".** È un **capitolo di rinvii**: consolida la **dichiarazione di confine** (queste dipendenze sono aperte e rinviate), **NON** la loro risoluzione. Voci aperte dichiarate: abilitazione FDAX standard (rinviata a PHASE-2) `:387`; vendor cross-index pluriennale per training PHASE-2 `:391`; **M-2 OPEN latenza Telegram L_max=30s (carryover Appendice E)** `:402`; implementazione codice operativo pipeline = FASE-D `:406`; lookup completa codici mese IDEM (runtime-discovery/FASE-D), persistenza DAPI come training (nuovo task Planner) — tutte **rinvii motivati**, da consolidare come **dipendenze dichiarate aperte**, non come materia da chiudere.
- **Cap.64 — Punti aperti fuori scope (Parte 10)** (`CAP_10_parte_10.md:226`) — **fonte del confine "dipendenze aperte verso FASE-D" (versante tape/storicizzazione).** Capitolo di rinvii, stesso trattamento di Cap.55. Voci aperte dichiarate: **calibrazione fine di θ_reconcile** (parametro provvisorio non congelato, rinviato a FASE-D / CAP-DATA-04 / monitoring post-go-live — analogo a L_max=30s Telegram); migrazione formato legacy→esteso (una-tantum FASE-D); implementazione codice pipeline backfill/riconciliazione/archiviazione (FASE-D); **convenzione cross-index PHASE-2 invariata: Parte 10 NON si applica ai cross-index PHASE-2** (confine PHASE-1); Telegram L_max=30s (M-2 OPEN, Appendice E); apertura flusso DAPI come training (nuovo task Planner). Da consolidare come **dipendenze dichiarate aperte / confine**, non da risolvere.

> **NB sui capitoli di rinvii (Cap.55/Cap.64)**: sono di per sé "punti aperti fuori scope". Per B8 **fondano** il requisito di confine "dipendenze aperte verso FASE-D" (è la loro funzione-prodotto). Ma il Developer consolida **la dichiarazione che sono aperte e dove sono rinviate**, **non** ri-deriva il merito (non calibra θ_reconcile, non misura L_max, non decide il vendor): quello è PENDING/FASE-D (§7). Concern atomico N1: la fasizzazione PHASE-1, la dichiarazione cross-index PHASE-2, e l'enumerazione delle dipendenze aperte sono **concern distinti** → ID distinti (vedi AC-B8-* §3).

---

## 2. Fatti già fissati dai capitoli — consolidamento fedele (RM-3, NON ri-derivare)

Questi sono **dichiarazioni di confine/fasizzazione** fissate nei capitoli frozen: citarle con `[DOC-INTERNO CAP_08:riga]` / `[DOC-INTERNO CAP_09:riga]` / `[DOC-INTERNO CAP_10:riga]`, **non** ri-derivarle, **non** promuoverle a esito.

- **PHASE-1 = FIB-only, single-instrument** (`CAP_08:143, :145, :167`): fasizzazione esplicita dichiarata, non semplificazione silenziosa. Invariante di prodotto.
- **PHASE-2 cross-index = dichiarazione normativa senza implementazione** (`CAP_08:143, :147, :176`): DAX/EuroStoxx50/S&P mini + estensioni (DCC/ADCC, Realized GARCH, S_xidx) dichiarate non implementate. **Fuori scope del prodotto corrente** → destinazione spec futura (SPEC-FUNZ-02), §6.
- **Cash europei (DGER/DSTX50/DITAS/DFRA) NON sono "cross-index PHASE-2"** (`CAP_09:338`, premessa §5): canali di contesto live (logging + gating qualitativo, Cap.53), distinti dai futures cross-index. Confine fine da consolidare in CN su PHASE-2.
- **Dipendenze aperte verso FASE-D** (`CAP_09:402, :406`; `CAP_10:131/:226-region`; `CAP_07:637`, premessa §5): M-2 latenza Telegram OPEN, θ_reconcile provvisorio, 10 parametri tuning carryover post-go-live, run validator sull'edge (PENDING-empirico). Da consolidare come **insieme dichiarato di dipendenze aperte**, ciascuna col suo **stato "aperto/provvisorio, rinviato a FASE-D"**, MAI come risolta.

**Eredità M (registro CARRYOVER/STATO)**: B8 **non chiude** alcun M. Richiama **M-2** (latenza Telegram, OPEN) e **M-GOV-1** (orario sessione, upgrade empirico OPEN) come **dipendenze aperte dichiarate** verso FASE-D, **senza chiuderle** (restano OPEN/PENDING). Il Developer **censisce** in REPORT gli M aperti di `tasks/CARRYOVER.md` con destinazione (atteso: nessun M nuovo emesso da B8; M esistenti richiamati come dipendenze aperte, non incardinati salvo che la review li tocchi).

---

## 3. Acceptance Criteria

**AC-G1..AC-G11** ereditati dai blocchi precedenti, vincolanti:

- **AC-G1 (N1 — atomicità)**: ogni requisito è **una sola proposizione verificabile**. Un requisito che impacchetta più concern va spezzato in più ID `B8-*`. (Es.: "fasizzazione PHASE-1 FIB-only", "cross-index PHASE-2 = dichiarazione senza implementazione", "dipendenze aperte verso FASE-D" sono **concern distinti** → ID distinti. Le singole dipendenze aperte, se distinte e verificabili separatamente, possono essere requisiti distinti **oppure** enumerate dentro un unico requisito-confine: scelta del Developer sotto N1, vedi AC-B8-DEPS; nessun conteggio imposto.)
- **AC-G2 (tracciabilità a riga)**: ogni requisito cita la **riga reale** del capitolo-fonte (`[DOC-INTERNO CAP_08_parte_8.md:NNN]` / `CAP_09_parte_9.md:NNN` / `CAP_10_parte_10.md:NNN`; premesse `CAP_07_parte_VII.md:NNN`), riletta token-per-token (AC-G7).
- **AC-G3 (valore operativo / di sistema)**: ogni requisito dichiara il suo **valore per l'operatore retail FIB o per il sistema** (es.: "la fasizzazione PHASE-1 esplicita evita che l'operatore si aspetti segnali cross-index inesistenti"; "l'enumerazione delle dipendenze aperte rende esplicito ciò che il prodotto dichiara ma non chiude, da risolvere prima/durante FASE-D"). Un requisito senza valore dichiarato è sbagliato.
- **AC-G4 (divieto "verificato X" di prima istanza — RM-1)**: la spec **non introduce** nuove dichiarazioni "verificato X". Ogni asserzione fattuale è un **richiamo** a un capitolo frozen con provenienza. Nessun blocco `VERIFICA/PROVE/...` di prima istanza.
- **AC-G5 (etichette RM-3)**: ogni fonte etichettata `[DOC-INTERNO ...]` / `[CODICE-ESISTENTE ...]` / `[PROVA-EMPIRICA <data>]` / `[WIKI-HINT, da verificare]`. I `[PROVA-EMPIRICA]` interni ai capitoli (es. FDAX `:387`) si **riportano come già dichiarati dal capitolo**, non si ri-asseriscono di prima istanza.
- **AC-G6 (grafia canonica)**: usare `[CODICE-ESISTENTE]` / `[PROVA-EMPIRICA]` / `[DOC-INTERNO]` / `[WIKI-HINT]`. **Vietata** la grafia deprecata `[CODICE-EXISTENTE]` (METODO RM-3).
- **AC-G7 (rilettura pin token-per-token)**: i pin §1/§5 sono puntatori di lavoro; il Developer rilegge e cita la riga reale, non il pin assunto.
- **AC-G8 (floor citazioni 100%)**: in review, **ogni** requisito deve avere almeno una citazione valida risolvibile alla riga. Floor 100%.
- **AC-G9 (cecità preservata)**: nessun ID-requisito importato dalla v2, **nessun conteggio-target**, **nessuna partizione** da v2/chunking nel documento. ID `B8-*` da zero.
- **AC-G10 (scope "tutto e solo")**: la spec copre **tutto e solo** il confine/chiusura dei capitoli §1 (Cap.42 + Cap.55 + Cap.64). Materia di altri blocchi NON va ri-derivata (è finding): vedi out-of-scope §6.
- **AC-G11 (matrice + nota di rinvio)**: sezione finale con **matrice di tracciabilità** (ogni `B8-*` → capitolo:riga + valore operativo) e **nota di rinvio** per le premesse/out-of-scope §6; gli **invarianti**/confini consolidati come tali (non ri-derivati).

**Specifici di B8 (VINCOLO CARDINE — confine/chiusura):**

- **AC-B8-CONFINE (cardine, obbligatorio)**: ogni requisito è una **dichiarazione di confine/fasizzazione/dipendenza-aperta**, **mai** apertura di materia-prodotto nuova del motore né risoluzione di una dipendenza aperta. La PHASE-2 cross-index è consolidata come **"dichiarazione normativa senza implementazione"**; le dipendenze aperte come **"dichiarate aperte, rinviate a FASE-D"**. **Verbi vietati**: "il prodotto supporta i cross-index", "la latenza è verificata", "θ_reconcile è calibrato a …", "FASE-D fa …" come fosse fatto. **Verbi ammessi**: "il prodotto **dichiara** PHASE-1 FIB-only", "la PHASE-2 è **rinviata** a un futuro ciclo", "resta **dipendenza aperta** verso FASE-D".
- **AC-B8-NOASSEMBLY (anti meta-processo)**: la card e la spec **NON** contengono alcun requisito di **assemblaggio della serie B1..B8**, di **indicizzazione dei blocchi**, né di **avvio FASE-D**. Sono meta-processo/fasi successive, **non** materia-prodotto di Sez.10. Un requisito di questo tipo = finding (FAIL del concern).
- **AC-B8-FRAMING (verifica di fondazione)**: ogni capitolo toccato è classificato **req-bearing** (fonda una proposizione-confine non coperta altrove) **oppure** **framing/premessa** (rinvii puri o materia di altro blocco). Cap.42/Cap.55/Cap.64 sono req-bearing per il confine; **Cap.36.3 (B7), Cap.53 (B5), Cap.41 (B5)** sono **premesse** (§5): citarle per riga come riferimento di una dipendenza aperta / confine, **NON** ri-derivarle né scrivere un requisito "su di esse". Non gonfiare il perimetro.
- **AC-B8-DEPS (dipendenze aperte, stato esatto)**: ogni dipendenza aperta è consolidata col suo **stato esatto dichiarato** ("aperta / provvisoria, non congelata, rinviata a FASE-D / monitoring post-go-live / Appendice E"). È finding consolidarla come risolta o ometterne lo stato di apertura. L'edge (DSR/PBO/OOS) e i valori d'esito restano **PENDING-empirico (validator/FASE-D)** anche qui (eredità del cardine B7): B8 li **cita come dipendenza aperta**, non li asserisce.

---

## 4. Sezioni da produrre (`docs/spec_funzionale/SPEC_FUNZ_01_B8.md`)

1. **Intestazione/scopo/schema-ID** (`B8-*` da zero) + conferma cecità + **nota "blocco di chiusura"** in evidenza (rischio framing/0-req; assemblaggio della serie e avvio FASE-D = task/fasi separati, NON requisiti — AC-B8-NOASSEMBLY).
2. **Fasizzazione PHASE-1 / PHASE-2** (Cap.42): PHASE-1 FIB-only come fasizzazione esplicita dichiarata; PHASE-2 cross-index come **dichiarazione normativa senza implementazione** (strumenti + estensioni future) — come **confine di prodotto** (AC-B8-CONFINE). Confine cash-europei ≠ cross-index PHASE-2 (premessa Cap.53 §5).
3. **Dipendenze aperte verso FASE-D** (Cap.55 + Cap.64, premessa Cap.36.3): enumerazione delle dipendenze dichiarate aperte (M-2 latenza Telegram, θ_reconcile provvisorio, 10 parametri tuning carryover post-go-live, run validator sull'edge PENDING, lookup codici mese, vendor/abilitazioni PHASE-2), ciascuna col suo **stato esatto di apertura e destinazione** (AC-B8-DEPS) — **dichiarate**, non risolte.
4. **Matrice di tracciabilità** (`B8-*` → capitolo:riga + valore operativo/di sistema) + **nota di rinvio** (premesse §5/out-of-scope §6) + **lista PENDING-empirico** (§7) + nota RM-3 (gerarchia fonti).

**REPORT** (`reports/REPORT_SPEC_FUNZ_01_B8.md`): 5 sezioni formato supervisore (Cosa è stato prodotto; Ipotesi di partenza; Decisioni rilevanti; Domande aperte; Criterio di rollback) + **tabella AC** (G1..G11 + B8-CONFINE/NOASSEMBLY/FRAMING/DEPS con `OK/PARZIALE/MANCA` + evidenza `file:riga`) + sezione **"Applicazione RM-1 a me stesso"** + **lista PENDING-empirico** + **conferma esplicita che nessun requisito di assemblaggio/indicizzazione/avvio-FASE-D è stato scritto** (auto-check AC-B8-NOASSEMBLY) + **conferma che nessuna dipendenza aperta è stata dichiarata risolta** (auto-check AC-B8-DEPS). F6: tutti i blocchi/ambiguità raccolti in **un unico batch** nel REPORT, non un giro per blocco.

---

## 5. Premesse dichiarate (citare come premessa, NON ri-derivare)

| Materia | Destinazione / trattamento |
|---|---|
| **Carryover dei 10 parametri di tuning operativo post-go-live** (`CAP_07_parte_VII.md:637`, §36.3) | premessa **owned B7** — citare la riga come **una delle dipendenze aperte** verso il monitoring post-go-live; **NON** ri-derivare il gate (Cap.36 è perimetro B7, chiuso PASS) |
| **Cash europei = logging + gating qualitativo, NON cross-index PHASE-2** (`CAP_09_parte_9.md:338`, Cap.53) | premessa **owned B5** (CN-7.9 gating) — citare **solo** il confine "cash europei ≠ cross-index PHASE-2" a supporto del CN su PHASE-2; **NON** ri-derivare il gating runtime/`gating_rules.yaml` (perimetro B5) |
| **Calendario / epoca E5, sessione FIB 08:00-22:00** (`CAP_08_parte_8.md` Cap.41; `CAP_09` Cap.52) | premessa **owned B5** — origine normativa della finestra-sessione; B8 la cita solo se serve come dipendenza aperta (upgrade empirico M-GOV-1), **NON** ri-consolida la regola operativa di sessione |
| **Latenza L_max=30s Telegram (M-2 OPEN)** | premessa/dipendenza aperta (Appendice E); **misura empirica = PENDING-empirico**, NON asserita (eredità B4-NFR-03/B7) |
| **Materia di B1..B7** (ambito, payload, lifecycle, emissione/consegna, runtime/sessione/compliance, schema-dato, gate go-live) | premessa — già specificata nei blocchi rispettivi; **NON** ri-derivare (è finding) |

> **Nota di confine — perché Cap.36.3 e Cap.53 sono premesse e non perimetro.** Entrambi i capitoli sono **già di proprietà** di blocchi chiusi (Cap.36 → B7 gate; Cap.53 → B5 gating). In B8 compaiono **solo** come riferimento puntuale di una dipendenza aperta (Cap.36.3: 10 param post-go-live) o di un confine fine (Cap.53: cash europei ≠ cross-index PHASE-2). **Nessun requisito B8 va ancorato come fonte primaria a Cap.36 o Cap.53**: la fonte primaria del confine PHASE-1/PHASE-2 è **Cap.42**; delle dipendenze aperte, **Cap.55/Cap.64**.

---

## 6. Out-of-scope esplicito (con destinazione)

| Materia | Destinazione |
|---|---|
| **Implementazione PHASE-2 cross-index** (layer covarianza DCC/ADCC, S_xidx, quinta famiglia target, feature cross-index) | **spec futura (SPEC-FUNZ-02 o equivalente)** — B8 consolida solo il **confine dichiarato** (PHASE-2 = dichiarazione senza implementazione), non la materia |
| **Risoluzione delle dipendenze aperte** (misura L_max, calibrazione θ_reconcile, congelamento 10 param, run validator edge, lookup completa codici mese, abilitazione FDAX, scelta vendor cross-index) | **FASE-D / validator / monitoring post-go-live** — B8 le **dichiara aperte**, non le chiude (AC-B8-DEPS) |
| **Assemblaggio della serie B1..B8 in un unico documento** | **task separato post-B8** — NON requisito B8 (AC-B8-NOASSEMBLY) |
| **Indicizzazione/cross-reference dei blocchi B1..B7** | **task separato post-B8 / assemblaggio** — NON requisito B8 |
| **Avvio FASE-D / specifica di implementazione FASE-D** | **FASE-D** — fase successiva, NON requisito B8 |
| **Verdetti d'edge / valori effettivi** (DSR/PBO/E[R_net]/OOS) | **FASE-D / ruolo `validator`** — PENDING-empirico, MAI asserito (eredità cardine B7) |
| **Materia di B1..B7** (incl. gate Cap.36, gating Cap.53, sessione Cap.52, schema-dato) | **blocchi rispettivi (chiusi)** — premessa §5, non ri-derivare |

---

## 7. PENDING-empirico (marcare, NON asserire — AC-B8-CONFINE/DEPS)

B8 **dichiara** le dipendenze aperte; il loro **esito/valore** è PENDING-empirico. Il Developer le marca, non le asserisce (atteso: **pochi**, tutti ereditati; nessun PENDING nuovo introdotto da un blocco di confine):

- **Latenza L_max=30s Telegram effettiva** (M-2 OPEN) → PENDING-empirico (Appendice E / FASE-D). B8 consolida che è **dipendenza aperta dichiarata**.
- **Upgrade empirico orario di sessione** (M-GOV-1, da WIKI-HINT a PROVA-EMPIRICA via tape DAPI) → PENDING-empirico (FASE-D). Dipendenza aperta dichiarata.
- **Calibrazione fine θ_reconcile** (provvisorio, `CAP_10:131`) → PENDING-empirico (FASE-D / CAP-DATA-04 / monitoring). Dipendenza aperta dichiarata.
- **Congelamento empirico dei 10 parametri di tuning** (carryover post-go-live, `CAP_07:637`) → PENDING-empirico (monitoring post-go-live 3-6 mesi). Dipendenza aperta dichiarata.
- **Run del validator sull'edge** (DSR/PBO/OOS, valori d'edge) → PENDING-empirico (validator/FASE-D). B8 lo cita come dipendenza aperta, **non** asserisce alcun esito (eredità cardine B7).

**NON pending (dichiarazioni di confine, citare con stato esatto)**: la **fasizzazione PHASE-1 FIB-only** (criterio dichiarato); la **dichiarazione** PHASE-2 cross-index senza implementazione; il **confine** cash europei ≠ cross-index PHASE-2; l'**esistenza e destinazione** di ciascuna dipendenza aperta (la dichiarazione che è aperta è un fatto del capitolo, non un esito da misurare).

---

## 8. Done-when (soglie di verdetto)

1. Ogni capitolo del perimetro §1 (Cap.42, Cap.55, Cap.64) che fonda materia di confine è coperto da almeno un requisito `B8-*` atomico (N1); concern distinti → ID distinti (fasizzazione PHASE-1 ≠ dichiarazione PHASE-2 ≠ dipendenze aperte).
2. **Cardine confine (AC-B8-CONFINE)**: **zero** aperture di materia-prodotto nuova del motore o risoluzioni di dipendenze aperte; ogni requisito è dichiarazione di confine/fasizzazione/dipendenza-aperta. Una sola apertura/risoluzione indebita = **FAIL del blocco**.
3. **Anti meta-processo (AC-B8-NOASSEMBLY)**: **zero** requisiti di assemblaggio-serie / indicizzazione-blocchi / avvio-FASE-D nel documento.
4. **Verifica di fondazione (AC-B8-FRAMING)**: Cap.36.3, Cap.53, Cap.41 trattati come **premesse** (citati per riga, non fonti primarie di alcun `B8-*`); nessun capitolo gonfiato a requisito senza fondazione di confine propria.
5. **Stato dipendenze aperte (AC-B8-DEPS)**: ogni dipendenza aperta consolidata col suo stato esatto ("aperta/provvisoria, rinviata a FASE-D/monitoring/Appendice E"); nessuna dichiarata risolta; edge = PENDING-empirico.
6. Ogni claim porta `[DOC-INTERNO CAP_08_parte_8.md:riga]` / `CAP_09_parte_9.md:riga` / `CAP_10_parte_10.md:riga` (premesse `CAP_07_parte_VII.md:riga`); **floor citazioni 100%**; **0 conclusioni wiki-only**; grafia canonica `[CODICE-ESISTENTE]` (vietata `[CODICE-EXISTENTE]`).
7. Premesse §5 citate come tali, NON ri-derivate; confini consolidati come confini; out-of-scope §6 rispettato (in particolare: PHASE-2 → SPEC-FUNZ-02; risoluzioni → FASE-D; assemblaggio → task separato).
8. **Cecità**: nessun ID-requisito importato, nessun conteggio/partizione da v2/chunking; ID `B8-*` auto-assegnati da zero.
9. Matrice di tracciabilità completa + nota di rinvio + lista PENDING-empirico presenti nella sezione finale.

**Verdetto**: PASS / CONDITIONAL / FAIL (Reviewer CLI). Lista "Empirico-CLI da verificare" attesa **vuota** (audit documentale no-DAPI, divieto CLI: niente probe di zelo).

---

## 9. Separazione ruoli

- **Planner/Orchestratore** (questo task): definisce il perimetro **per capitoli** (fonte primaria Cap.42/55/64; premesse Cap.36.3/53/41; **no ID-v2, no conteggio, no partizione** esposti al Developer), gli AC (G1..G11 + B8-CONFINE/NOASSEMBLY/FRAMING/DEPS), le premesse, gli out-of-scope, i PENDING-empirico. **Non scrive la spec, non fa audit, non committa** questo task card al posto del Developer. La mappatura Req-v2 ↔ capitolo (Sez.10) vive **fuori da questa card** (`Business Spec/Final/ESITO_B8-01.md` / Reviewer), MAI esposta al Developer.
- **Developer** (cieco, §0.1): deriva dai **soli** capitoli del perimetro §1 (+ premesse §5 per riga); assegna `B8-*` da zero (N1); **non ridefinisce il perimetro, non cerca la mappa v2, non apre materia nuova del motore, non risolve dipendenze aperte, non scrive requisiti di assemblaggio/avvio-FASE-D** (AC-B8-CONFINE/NOASSEMBLY); rilegge i pin token-per-token; scrive `docs/spec_funzionale/SPEC_FUNZ_01_B8.md` + `reports/REPORT_SPEC_FUNZ_01_B8.md`; scrive `READY_FOR_REVIEW` in `tasks/DEV_STATUS.md`; si ferma.
- **Reviewer** (CLI, GOV-SURFACES-01): audita gli AC + **confronto-copertura vs perimetro B8** sulla mappa di chunking consolidata (`c7ce4be`, riga B8 → Sez.10), che **il Reviewer** consulta — **non il Developer**; **floor citazioni 100%**; verifica RM-1/RM-3 e — **in primo piano** — il **cardine confine** (nessuna apertura di materia nuova; nessun requisito di assemblaggio/avvio-FASE-D; dipendenze aperte dichiarate non risolte; verifica di fondazione su Cap.36.3/53/41 = premesse); **chiusura 75/75** della serie B1..B8 (verifica di partizione); **non ripianifica**. Audit documentale no-DAPI in CLI col divieto CLI (niente probe di zelo); lista "Empirico-CLI da verificare" attesa **vuota**. Verdetto PASS/CONDITIONAL/FAIL.

---

*Card B8 (card-sorgente `Business Spec/Final/ACTIVE_TASK_B8.md`, prodotta sotto `ISTRUZIONI_B8-01`). **NON installata**: `tasks/ACTIVE_TASK.md` resta storico su B7; l'install di questa card + l'avvio del ciclo Developer→Review sono **decisione AC**. Nessuna spec scritta, nessun CAP modificato (freeze G-09). Path file CAP verificati reali: `CAP_08_parte_8.md` / `CAP_09_parte_9.md` / `CAP_10_parte_10.md` (numero arabo, Parti 8/9/10), `CAP_07_parte_VII.md` (numero romano, Parte VII). SHA frozen pinnabili: CAP-08 `015c47a`, CAP-09 `28cfd2d`, CAP-10 `41447d3`, CAP-07 `b27c1e3` (diff a HEAD vuoti, verificati in setup). La vista-Developer è per soli capitoli: nessun ID-requisito v2, nessun conteggio-target, nessuna partizione esposti — cecità preservata. Vincolo cardine in evidenza: confine/chiusura, mai apertura di materia nuova; assemblaggio della serie e avvio FASE-D sono task/fasi separati, NON requisiti; ogni dipendenza aperta è dichiarata aperta, mai risolta.*
