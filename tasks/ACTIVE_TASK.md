# TASK ATTIVO: SPEC-FUNZ-01-B4-EXT — Estensione "consegna" (CAP_06 PVI Cap.29: mobile-first + 3 notifiche standard)

> **Track**: Business-spec (SPEC-FUNZ). **Sede**: CLI (GOV-SURFACES-01). **Tag commit**: `[SPEC-FUNZ-01-B4-EXT]`. Tutto su `main`.
>
> **Natura**: **estensione** del blocco B4, **non** un nuovo blocco e **non** un rifacimento. La parte di B4 già chiusa (CAP_02 Cap.8-9, **PASS `c3be05e`**) **non** si ri-deriva, **non** si riapre, **non** si rivede. Qui si recupera **solo** la materia di **consegna** di CAP_06 che era stata omessa dal perimetro-fonte (errore di setup dell'Orchestratore, non del Planner né dei Developer).
>
> **Correzione di fonte (RM-2, verifica CLI 2026-06-16)**: le **3 notifiche standard** (R-6.4) sono fondate in **Cap.29.4 (`:220`)**, **non** in Cap.28.4 (`:123` = "Determinismo del replay e logging dei candidati" = **runtime**, che va a B5). Il mobile-first (NFR-6.1) è in Cap.29.1 (`:146`). Quindi la materia di **consegna** di CAP_06 è **tutta e solo in Cap.29**; **Cap.27 e Cap.28 interi** sono runtime → B5. Il taglio consegna/runtime e l'intento dell'Opzione 1 (recuperare NFR-6.1 + R-6.4) restano invariati; cambia solo il puntatore di fonte (Cap.29.4 anziché Cap.28.4) e il rinvio a B5 diventa "Cap.28 intero". Correzione confermata da AC.
>
> **Letture obbligatorie del Developer, in quest'ordine, PRIMA di scrivere**: `tasks/METODO.md` (RM-1..RM-4 + RACC-METODO-2), `.claude/BASE_COMUNE.md`, `.claude/agents/spec_developer.md`, questo `tasks/ACTIVE_TASK.md`. Conferma in testa al REPORT di averli letti.

---

## 0. Decisione di perimetro (autorizzata dal supervisore AC)

La mappa di chunking autoritativa (`PROPOSTA_SUDDIVISIONE_SPEC*.md`, riga ~106) assegnava a B4 **CAP_02 Cap.8-9 + CAP_06 PVI Cap.27-29 interi**. Cap.27-29 sono però di **due nature distinte**:

- **Consegna** (→ resta B4): **Cap.29 intero** (operatività mobile): layout mobile-first (§29.1 `:146`, §29.2 `:154`) e le **3 notifiche standard** — emissione (§29.2), `trigger_event` (§29.3 `:190`), transizione terminale (§29.5 `:223`) — dichiarate come insieme standard in **§29.4 (`:220`)**.
- **Runtime** (→ va a **B5**): **Cap.27** (pipeline di inference real-time, EGARCH) e **Cap.28 intero** (citazione vincolo §28.1, politica anti-doppio-segnale/non-refresh §28.2, tie-break §28.3, logging candidati e determinismo del replay §28.4).

**Decisione AC (Opzione 1)**: B4 recupera **solo** la materia di consegna (**Cap.29**); il runtime di **Cap.27 e Cap.28 (interi)** è **rinviato a B5**. È uno **scostamento voluto** dalla mappa (che univa 27-29 interi a B4): rispetta il contenuto (nessun requisito perso) divergendo sul contenitore. **La mappa viene aggiornata in pari data** (riga ~106 + riga ~107 B5) per riflettere il taglio consegna/runtime. Questo scostamento è quindi **autorizzato e tracciato**, non un drift.

### 0.1 — Vincolo di cecità (modalità B)

Il Developer costruisce i requisiti di questa estensione **DAL SOLO** `Cap.29` di **CAP_06 PVI** (perimetro §1), **cieco** rispetto a: `SPEC_FUNZ_01.md` (v2 congelata) e `*_v1_storico*`; i file di chunking (`PROPOSTA_SUDDIVISIONE_SPEC*.md`) **come fonte di contenuto-requisiti**; i documenti di B1/B2/B3 (`SPEC_FUNZ_01_B1/B2/B3.md`). **Eccezione necessaria, same-block**: il Developer **può** leggere il documento **B4 esistente** (`docs/spec_funzionale/SPEC_FUNZ_01_B4.md`) **solo** per (i) continuare lo schema-ID senza collisione e (ii) **non duplicare** il contratto a 9 voci del messaggio (Cap.9.2, già B4) e la notifica `trigger_event` già coperta su Cap.9.5: è lo stesso blocco, non una violazione di cecità. Il confronto-copertura con la v2 resta compito **esclusivo del Reviewer**.

---

## 1. Perimetro-fonte (cosa derivi) — SOLO questo

**Fonte**: `docs/methodology_v2/CAP_06_parte_VI.md`, **limitatamente a Cap.29 (Gestione dell'operatività su mobile, §29.1–29.5)**:

- **Mobile-first** (§29.1 `:146`, §29.2 `:154`): il requisito che la consegna sia leggibile/azionabile da cellulare in attenzione limitata; il layout mobile-first **rappresenta** il payload formale **estendendo senza duplicare** il contratto a 9 voci di Cap.9.2 (già B4). → famiglia **`B4-NFR`**, recupera **NFR-6.1**. Pin: `[DOC-INTERNO CAP_06_parte_VI.md:146]` (+ `:154` per il layout del messaggio di emissione).
- **Le 3 notifiche standard** (§29.4 `:220`): il canale pubblica **esattamente 3 notifiche standard per segnale** — (1) **emissione** (§29.2), (2) **`trigger_event`** / raw touch (§29.3 `:190`), (3) **transizione terminale** (§29.5 `:223`); tra una notifica e l'altra nessun aggiornamento di stato (no polling/refresh). → famiglia **`B4-R`**, recupera **R-6.4**. Pin: `[DOC-INTERNO CAP_06_parte_VI.md:220]` (notifiche specifiche: emissione `:154`, trigger `:190`, terminale `:223`).

I pin sono stati **risolti in CLI** (RM-2, verifica diretta su CAP_06) e depositati sopra. Il Developer li **ri-verifica token-per-token** prima di citarli (AC-G7); se una riga non risolve pulita, usa `[B-N PROVVISORIO]` e segnala.

**Regola di confine "consegna ≠ runtime" (cardine di questa estensione)**: derivi **SOLO** da **Cap.29**. Da **Cap.28 NON prendi nulla** (è interamente runtime: §28.1 citazione vincolo, §28.2 non-refresh, §28.3 tie-break, §28.4 determinismo/logging). Le 3 notifiche stanno in **Cap.29.4**, non in Cap.28.4. **NON** consolidare: la pipeline di inference / EGARCH (Cap.27); l'anti-doppio operazionale / tie-break / logging candidati / determinismo del replay (Cap.28 intero). Tutto questo è **B5** (runtime). Se sei tentato di tirarlo dentro, **fermati**: è scope creep verso B5.

### Note di confine
- **Notifica terminale ↔ stati terminali (B3)**: la 3ª notifica scatta alla transizione terminale del lifecycle. Gli **stati/transizioni terminali** sono materia di **B3** (Cap.7) — citali **come premessa**, **non** ri-derivare la state machine. Qui consolidi **la notifica** (che esiste, quando scatta, cosa veicola a livello di consegna), non lo stato.
- **No-duplicazione Cap.9.2**: il contratto informativo a 9 voci del messaggio è già B4 (Cap.9.2). Cap.29 lo **estende** col layout mobile-first: consolida l'**NFR mobile-first**, cita Cap.9.2 come premessa, **non** ri-elencare le 9 voci.
- **Notifica `trigger_event` ↔ pubblicazione già B4**: la 2ª notifica pubblica il `trigger_event`; la **pubblicazione** è già coperta dal B4 esistente (Cap.9.5). **Non** la duplicare: citala come già-consolidata e concentra la derivazione sulle 3 notifiche **come insieme standard** (R-6.4, Cap.29.4) e sulla notifica **terminale** (§29.5), non ancora coperta. L'**evento** `trigger_event` è B3 — premessa, non ri-derivare.

---

## 2. Acceptance Criteria

Si applicano **gli stessi `AC-G1..AC-G11` di B4** (atomicità N1; tracciabilità obbligatoria a riga di **CAP_06 Cap.29**; valore operativo — o **valore di sistema** per eventuali invarianti puri; divieto "verificato X" RM-1; etichette RM-3 su fonti esterne; grafia canonica; floor citazioni 100% verificato in review; **cecità preservata** estesa a B3; scope **"tutto e solo"** la materia di consegna §1; matrice di tracciabilità + nota di rinvio; invarianti come tali). In più:

- **AC-EXT-1 — Recupero esplicito**: i due requisiti-bersaglio della v2 sono recuperati e marcati: **NFR-6.1** (mobile-first) → un `B4-NFR-NN`; **R-6.4** (3 notifiche standard) → uno o più `B4-R-NN` (atomicità N1: l'esistenza dell'insieme + ciascuna delle 3 notifiche possono generare requisiti distinti — granularità decisa dal Developer applicando N1).
- **AC-EXT-2 — Confine consegna/runtime rispettato**: nessun requisito tocca pipeline/inference (Cap.27) né anti-doppio/tie-break/logging/determinismo (Cap.28 intero). Materia runtime inclusa = scope creep verso B5 (finding).
- **AC-EXT-3 — Continuità ID e no-duplicazione**: ID continuati dallo schema B4 esistente senza collisione; nessuna ri-derivazione di Cap.9.2 (9 voci), della notifica trigger Cap.9.5 (già B4) né della state machine B3 (premesse citate, non consolidate).

---

## 3. Sezioni da produrre

Il Developer **appende** a `docs/spec_funzionale/SPEC_FUNZ_01_B4.md` una sezione delimitata **"Estensione consegna — CAP_06 PVI (Cap.29)"** con:
1. **Nota di provenienza ed estensione**: dichiara che è un'estensione autorizzata (Opzione 1, supervisore AC), che recupera la materia di consegna di CAP_06 (Cap.29) omessa dal perimetro-fonte originario, che la parte CAP_02 Cap.8-9 (PASS `c3be05e`) resta invariata.
2. **Requisiti mobile-first** (`B4-NFR-NN`, da Cap.29.1/29.2): con valore operativo (operi da cellulare).
3. **Requisiti 3 notifiche standard** (`B4-R-NN`, da Cap.29.4 `:220`, con le specifiche §29.2/29.3/29.5): emissione / `trigger_event` / terminale; ciascuna con quando scatta e valore operativo; la terminale cita gli stati terminali B3 come premessa; la trigger cita la pubblicazione Cap.9.5 già-B4 come già-consolidata (non duplicare).
4. **Aggiornamento della matrice di tracciabilità** del documento B4 con le nuove righe.
5. **Nota di rinvio**: dichiara esplicitamente cosa di CAP_06 è **rinviato a B5** (Cap.27 pipeline/inference; Cap.28 intero: non-refresh/tie-break/logging/determinismo) e perché (runtime ≠ consegna).

REPORT atteso (`reports/REPORT_SPEC_FUNZ_01_B4.md`, **aggiornato** con sezione di estensione): 6 sezioni formato supervisore + tabella AC + **"Applicazione RM-1 a me stesso"**; dichiara la cecità (Cap.29; lettura del solo B4 esistente per ID/no-dup) e la provenienza.

---

## 4. Out-of-scope (con destinazione)

| Materia | Destinazione |
|---|---|
| Pipeline di inference real-time, EGARCH (Cap.27) | **B5** (runtime) |
| Politica anti-doppio-segnale operazionale, non-refresh, tie-break, logging candidati, determinismo del replay (Cap.28 intero, §28.1–28.4) | **B5** (runtime) |
| Contratto a 9 voci del messaggio (Cap.9.2), pubblicazione notifica `trigger_event` (Cap.9.5) e condizioni/regola di emissione (Cap.8) | **B4 già PASS `c3be05e`** — non ridefinire |
| State machine e stati terminali (Cap.7) | **B3** — premessa citabile, non ri-derivabile |
| Schema-payload, immutabilità (Cap.6) | **B2** |

---

## 5. Done-when

Un lettore, leggendo la sezione di estensione di `SPEC_FUNZ_01_B4.md`, risponde senza ambiguità a:
1. Qual è il requisito di consegna mobile-first e perché conta per chi opera da cellulare?
2. Quali sono le 3 notifiche standard, e in quale momento scatta ciascuna (emissione / trigger / terminale)?
3. In che senso la notifica terminale dipende dagli stati terminali del lifecycle (B3) senza ri-definirli?
4. Cosa di CAP_06 è stato deliberatamente rinviato a B5 e perché (Cap.27 + Cap.28 interi)?
5. Ogni requisito traccia a una riga di **CAP_06 Cap.29** — salvo premesse citate da Cap.9.2/Cap.9.5/Cap.7 — e porta un valore dichiarato?

---

## 6. Modalità di review

- Review formale CLI sugli AC dell'**estensione** (§2) + sui nuovi requisiti. La parte CAP_02 Cap.8-9 **non si ri-audita** (PASS `c3be05e` regge).
- **Confronto-copertura aggiornato (modalità B)**: il Reviewer ri-esegue la copertura ora sul **perimetro di consegna PIENO** (Cap.8-9 + Cap.29) contro il **perimetro di consegna corrispondente della v2** (Sez.5+6), usando la **mappa di chunking aggiornata** come autorità di partizione (F-3). Verifica: **NFR-6.1 e R-6.4 recuperati**; nessun residuo di consegna v2 caduto; nessuno scope creep runtime (Cap.27/Cap.28).
- Cecità del Developer come oggetto di audit (tracce v2/B1/B2/B3 importate = BUG REALE).
- Verdetto PASS / CONDITIONAL / FAIL. ≥1 BUG REALE ⇒ non-PASS.

---

## 7. Pipeline attesa (Orchestratore)

1. Pin CAP_06 risolti (Cap.29.1 `:146`/`:154`, Cap.29.4 `:220`, specifiche `:190`/`:223`) e depositati al §1.
2. **spec_developer** (CLI, cieco §0.1) appende la sezione di estensione + aggiorna matrice; aggiorna REPORT; scrive `READY_FOR_REVIEW`; si ferma. *Recupero socket*: se l'agente si interrompe, riprendi con un Developer di completamento trasparente (provenienza nel REPORT), come già fatto per B4 base.
3. **Check post-Developer** + boundary-check sul seam consegna/runtime (Cap.27/Cap.28 ↔ B5) e no-duplicazione (Cap.9.2/Cap.9.5/Cap.7).
4. **spec_reviewer** (CLI): audit AC estensione + copertura piena consegna vs v2 (mappa aggiornata).
5. **PASS** → marcatore `SPEC-FUNZ-01-B4: CHIUSO PASS <sha>` (B4 ora completo: CAP_02 Cap.8-9 + CAP_06 Cap.29 consegna). **CONDITIONAL/FAIL** → punto di controllo supervisore.

---

## 8. Finding di Review da risolvere — CONDITIONAL `f369276` (micro-fix citazioni, decisione AC)

Review B4-EXT iterazione 1 = **CONDITIONAL** (`reviews/REVIEW_SPEC_FUNZ_01_B4_EXT_review.md`). Punto di controllo supervisore eseguito: instradati il **BUG REALE #1** (obbligatorio) + i **3 MIGLIORA #2/#3/#4** (approvati da AC). Il **NEUTRO #5 NON va toccato**. Tutti sono lo **stesso pattern**: la citazione punta all'**header** di sottosezione invece che al **paragrafo di contenuto** immediatamente successivo (convenzione CAP_06: header e paragrafo sono righe distinte). **Micro-fix di solo puntatore-riga: NESSUN cambio di contenuto, proposizione o scope.** Verifica ogni nuova riga token-per-token sul CAP (AC-G7) prima di ri-citare.

| # | Requisito (file:riga) | Citazione attuale | Correzione | Costrutto da coprire |
|---|---|---|---|---|
| 1 (BUG REALE) | `B4-R-37` (`SPEC_FUNZ_01_B4.md:433–436`) | `:190` (header §29.3) | **→ `:192`** | "non modifica il messaggio di emissione (no edit, no append)"; "`signal_id` esplicito" |
| 2 (MIGLIORA) | `B4-NFR-06` (`:401`) | `:146`, `:154` | **aggiungi `:148`** (lascia `:146`; togli `:154` header) | "nessun campo nuovo/omesso; payload formale immutabile vs rappresentazione mobile cosmetica" |
| 3 (MIGLIORA) | `B4-R-35` (`:422`) | `:220`, `:154` | **`:154` → `:156`** (mantieni `:220`) | "pubblica le 9 voci nel layout mobile-first" |
| 4 (MIGLIORA) | `B4-R-36` (`:429`) | `:220`, `:190` | **`:190` → `:192`** (mantieni `:220`) | "messaggio separato al raw touch" |

**Mandato (tutto e solo questo)**: correggi le 4 citazioni come sopra in `docs/spec_funzionale/SPEC_FUNZ_01_B4.md` (sezione di estensione); aggiorna le righe corrispondenti della **matrice E.6** se vi compaiono i puntatori; aggiorna il **REPORT** (tabella AC-G7 → da PARZIALE a OK; nota nel §"Decisioni"/RM-1 sul micro-fix). **NON** toccare: gli altri requisiti, le proposizioni, il perimetro, il finding #5 (`B4-R-38` `:223` ridondante — si lascia), la parte CAP_02 Cap.8-9 (PASS `c3be05e`), il CAP (frozen). Conta come iterazione di rework v2 legata a finding di Review. Commit `[SPEC-FUNZ-01-B4-EXT]` (body: "iter.2 — fix citazioni #1 BUG + #2/#3/#4 MIGLIORA: header→paragrafo") + `READY_FOR_REVIEW`; poi fermati.

---

*Card di estensione scritta in fase di supervisione, **rev. RM-2** (correzione fonte Cap.28.4→Cap.29.4 confermata da AC), NON committata dal Planner (lo fa l'Orchestratore). Scostamento dalla mappa autorizzato dal supervisore (AC, Opzione 1) e tracciato; mappa aggiornata in pari data. Nessuna spec scritta qui, nessun CAP modificato (freeze G-09). I pin Cap.29 sono stati risolti in CLI (RM-2), non asseriti a monte.*
