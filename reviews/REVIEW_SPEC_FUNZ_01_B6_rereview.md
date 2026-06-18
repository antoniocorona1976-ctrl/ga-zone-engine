# RE-REVIEW (DELTA) — SPEC-FUNZ-01-B6 (Schema-dato DAPI & continuità tape)

> **Track**: Business-spec (SPEC-FUNZ). **Blocco**: 6/8 (ricostruzione cieca, modalità B).
> **Sede**: **CLI** (GOV-SURFACES-01) — audit documentale no-DAPI, divieto CLI attivo (nessuna probe di zelo).
> **Modalità**: re-review di **DELTA** sull'iterazione 2 — certifica SOLO che i 2 fix sono corretti e che non ci sono regressioni. NON è una CAP-review piena ripetuta (la sostanza è già certificata PASS-grade in iter.1).
> **Oggetti**: `docs/spec_funzionale/SPEC_FUNZ_01_B6.md` + `reports/REPORT_SPEC_FUNZ_01_B6.md` al commit di rework **`560ee08`**; delta vs commit auditato in iter.1 **`80409d9`**.
> **Letture confermate**: `tasks/METODO.md` (RM-1..RM-4 + RACC-METODO-2), `.claude/BASE_COMUNE.md`, `.claude/agents/spec_reviewer.md`, `reviews/REVIEW_SPEC_FUNZ_01_B6_review.md` (review iter.1), `tasks/ACTIVE_TASK.md` §9 (mandato dei 2 fix).
> **File precedente non sovrascritto**: la review iter.1 vive integra in `reviews/REVIEW_SPEC_FUNZ_01_B6_review.md`. Questo è il blocco di re-review (iter.2) come file separato (mandato Orchestratore).

---

## ITERAZIONE 2 (DELTA) — verdetto: **PASS**

**Sintesi**: i 2 fix instradati dal punto di controllo supervisore sono chiusi correttamente; il delta è **esattamente quello atteso** (2 righe modificate nel doc, 2 nel report + sezione "Iterazione 2"); **0 regressioni** (nessuna proposizione, ID-requisito o citazione-fonte alterata); finding #3 (B6-R-28/R-31) lasciato come da mandato. Il BUG REALE #1 di iter.1 (conteggio falso) è risolto e il nuovo conteggio è **verificato indipendentemente** in CLI. Tabella "Classificazione per il supervisore" della re-review: **vuota** (0 BUG REALE, 0 nuovi finding). Per il mapping verdetto↔classificazione (BASE_COMUNE §4: 0 BUG REALE ⇒ PASS ammesso) → **PASS**.

---

## Ambito del delta certificato

`git diff 80409d9 560ee08 --stat`:
- `docs/spec_funzionale/SPEC_FUNZ_01_B6.md` — **2 righe** (etichetta B6-CN-23 + footer conteggio).
- `reports/REPORT_SPEC_FUNZ_01_B6.md` — 2 righe modificate (§1, §4 conteggio) + sezione "Iterazione 2" appesa.
- `reviews/REVIEW_SPEC_FUNZ_01_B6_review.md` — file review iter.1 (committato col rework; non oggetto di delta-contenuto).
- `tasks/ACTIVE_TASK.md` — §9 "Finding di Review da risolvere" (mandato; scritto dall'Orchestratore).

Nessun altro file toccato. Il rework è chirurgico, coerente con la natura "sola accuratezza" dichiarata.

---

## Fix #1 (era BUG REALE) — conteggio: **CHIUSO**

**Verifica indipendente del conteggio reale** (grep meccanico su `560ee08`, sede CLI):
- ID `B6-R-*` unici (grassetto): **37**
- ID `B6-CN-*` unici (grassetto): **24** — enumerati `CN-01..CN-24`, **consecutivi, senza gap né duplicati**
- ID `B6-NFR-*` unici: **4**
- Righe matrice §7.1 (`^| B6-`): **65**

→ Totale reale = **65 (37 R + 24 CN + 4 NFR)**. **Coincide** col dichiarato dopo il fix.

**Occorrenze del claim corrette (tutte e sole)**:
| Posizione | Prima | Dopo | Esito |
|---|---|---|---|
| `SPEC_FUNZ_01_B6.md:413` (footer) | "61 requisiti: 37 R + 20 CN + 4 NFR" | "65 requisiti: 37 R + 24 CN + 4 NFR" | ✓ |
| `REPORT §1` (`:9`) | "61 requisiti atomici (37 B6-R, 20 B6-CN, 4 B6-NFR)" | "65 requisiti atomici (37 B6-R, 24 B6-CN, 4 B6-NFR)" | ✓ |
| `REPORT §4` (`:29`) | "61 requisiti … matrice a 61 righe" | "65 requisiti … matrice a 65 righe" | ✓ |

**Nessun conteggio-claim falso residuo**: grep `61`/`20 CN` su doc e report dà solo (a) numeri-di-riga di pin legittimi (`export_directa…py:61` = `DEFAULT_INTRADAY_MAX_DAYS`, righe matrice `:161`, `:163-164`, `:260-261`) e (b) la citazione storica prima→dopo nella sezione "Iterazione 2" del report (legittima: documenta il fix). La tabella AC del REPORT (AC-G1 atomicità riga 47, AC-G2 tracciabilità riga 48) **non cita più la numerosità sbagliata** — l'aggancio del BUG #1 alla tabella AC è risolto. Il claim fattuale è ora veritiero rispetto al proprio contenuto (BASE_COMUNE §8). **#1 CHIUSO.**

---

## Fix #2 (era NEUTRO) — etichetta orfana B6-CN-23: **CHIUSO**

- Matrice §7.1, riga `:373`: etichetta-fonte ora = **"Cap.62"** (rimossa "/58"). Grep `Cap.58|/58` sul doc → **nessuna occorrenza residua**.
- Pin `[DOC-INTERNO CAP_10_parte_10.md:68]` **invariato** (confermato dal diff: la riga cambia solo nell'ultima colonna).
- **Risoluzione del pin riverificata** (Read di `CAP_10_parte_10.md:66-70`): la riga 68 è il punto 3 "La provenienza è tracciata da `source`, non da `bar_synthetic`" — materia di Cap.62 (`source` esteso: `DIRECTA`/`BACKFILL_FROM_*`). Coincide token-per-token con la proposizione di B6-CN-23 (`:296`). L'etichetta-capitolo "Cap.62" è ora **corretta** e non più orfana. **#2 CHIUSO.**

---

## 0 regressioni — verificato

`git diff 80409d9 560ee08 -- docs/spec_funzionale/SPEC_FUNZ_01_B6.md` (sole righe `+/-`): **esattamente 2** righe modificate — la riga matrice B6-CN-23 (solo colonna-capitolo) e il footer (solo conteggio). `git diff … -- reports/…` (sole righe rimosse): **esattamente 2** — i conteggi §1 e §4; tutto il resto è **aggiunta** (sezione Iterazione 2).

Conseguenze certificate:
- **Proposizioni dei 65 requisiti**: identiche a iter.1 (0 testo-requisito toccato).
- **ID-requisito**: identici (37 R + 24 CN + 4 NFR, stessa numerazione).
- **Citazioni-fonte (pin)**: identiche; in particolare `B6-CN-23` mantiene `:68` (è cambiata solo l'etichetta descrittiva di colonna, non la citazione `path:line`).
- **Finding #3 (B6-R-28 / B6-R-31 borderline N1)**: **non toccato** — confermato dal mandato §9 ("non instradato, decisione AC") e dall'assenza di ogni modifica alle righe `:231/:253` nel diff.
- **Coerenza REPORT**: sezione "Iterazione 2 — risposta ai finding di Review (CONDITIONAL `fd48070`)" presente (`:92`), con Fix #1 / Fix #2 / Finding #3 documentati; tabella AC coerente col nuovo conteggio.

I capitoli-fonte (`docs/methodology_v2/`) restano frozen (G-09): nessuna modifica (solo Read di verifica su `:66-70`).

---

## Tabella "Classificazione per il supervisore" (re-review iter.2)

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|------------------------|
| — | Nessun nuovo finding. Fix #1 e #2 di iter.1 chiusi; 0 regressioni; finding #3 lasciato come da mandato. | — | — | — |

**Vuota** (0 BUG REALE, 0 nuovi finding). I 2 NEUTRO residui di iter.1 (#2 etichetta — ora **risolto**; #3 borderline N1 — lasciato per decisione AC) non generano instradamenti ulteriori.

---

## Applicazione RM-1 a me stesso

- **"conteggio reale 65 (37/24/4)"**: VERIFICA da grep meccanico indipendente sul commit `560ee08` (`\*\*B6-R-` = 37; `\*\*B6-CN-` = 24, enumerati 01..24 senza gap; `\*\*B6-NFR-` = 4; `^| B6-` = 65). PROVE: output grep citati sopra. ALTERNATIVE ESCLUSE: gap/duplicati negli ID CN (escluso — sequenza consecutiva 01..24). ALTERNATIVE NON ESCLUSE: nessuna. Non mi sono fidato del numero dichiarato: l'ho ricontato.
- **"delta = solo 2 righe per file, 0 regressioni"**: da `git diff 80409d9 560ee08` letto integralmente (non riassunto). PROVE: diff sottrattivo sul doc = 2 righe (etichetta + footer); sul report = 2 righe (conteggi §1/§4), resto in addizione. ALTERNATIVE NON ESCLUSE: nessuna — il diff è esaustivo per definizione.
- **"pin :68 risolve a Cap.62"**: da Read diretto di `CAP_10_parte_10.md:66-70`; la riga 68 enuncia "provenienza tracciata da `source`, non `bar_synthetic`" (Cap.62), che è la proposizione di B6-CN-23. Non da fiducia nella nuova etichetta.
- **"finding #3 non toccato"**: da assenza di diff sulle righe dei requisiti + mandato §9. Non da assunzione.
- **Limite dichiarato (onestà)**: questa è una re-review di **delta**, non una ri-esecuzione della CAP-review piena. Non ho ri-verificato token-per-token le ~65 citazioni DOC-INTERNO/decoder (lo ha fatto iter.1 con floor 100%): poiché il diff dimostra che **nessuna citazione è cambiata**, la certificazione di iter.1 sul corpo resta valida e non andava ri-eseguita. ALTERNATIVE NON ESCLUSE su questo: nessuna che il delta possa aver introdotto (il delta non tocca pin né proposizioni).

---

## Empirico-CLI da verificare

**VUOTA** (attesa). Il delta è di sola accuratezza testuale (conteggio + 1 etichetta-capitolo); non introduce né modifica fatti empirici. Audit documentale no-DAPI in sede CLI col divieto CLI rispettato (nessuna probe eseguita).
