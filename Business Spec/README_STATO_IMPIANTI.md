# STATO IMPIANTI — governance business-spec (LEGGERE PRIMA DI TOCCARE QUESTA CARTELLA)

> ⚠️ Questa cartella è materiale di lavoro UNTRACKED. NON è la governance in vigore.

## In vigore (impianto A — l'UNICO impianto)
`.claude/agents/spec_{planner,developer,reviewer}.md` + `.claude/CLAUDE.md` + `.claude/BASE_COMUNE.md`.
Tracciabilità requisito→capitolo, R/NFR/CN, RM-1..RM-4, reviewer bi-sede, N1+F6 (REV-A1, commit `d8cbca3`).
Ha prodotto SPEC-FUNZ-01 v1 PASS (`a16a4c0`).

## Impianto B (modello a 4 canali) — RESPINTO e ARCHIVIATO IN QUARANTENA
Respinto da AC con REV-A1 (razionale: `FINDING AUDIT_GOVERNANCE_4CANALI.md`, F1-F7).
I suoi file sono stati spostati l'11/06/2026 in `OLD_NOT_USE_NOT_READ_FILES_MODEL_4_CANALI/`:
**quella cartella non va letta, citata né richiamata da nessun documento futuro** (vedi il README al suo interno).
Unica eccezione tenuta fuori dalla quarantena: `SPEC_HARNESS_EMPIRICO.md` (vedi sotto).

## Contenuto vivo di questa cartella
- `FINDING AUDIT_GOVERNANCE_4CANALI.md` — l'audit ostile (F1-F7) che ha motivato il respingimento di B.
  È anche l'origine di N1 e F6 oggi in vigore nell'impianto A. Decision-record: si può citare.
- `SPEC_HARNESS_EMPIRICO.md` — spec di uno strumento di backtest a ipotesi singola (walk-forward,
  purge/embargo, assert anti-leakage). Nata in B ma utile in prospettiva FASE-D anche sotto A.
  Tenuta fuori dalla quarantena per decisione AC dell'11/06/2026.
- `Prompt1_CODE_CLI.md` / `Prompt2_CODE_CLI.md` — record dell'incidente di regressione (deposito errato
  sopra gli agenti in vigore + rollback scoped) ed esempi della prassi di handoff Web→CLI.
- `Final/ISTRUZIONI_REV-A1.md`, `Final/ESITO_REV-A1.md`, `Final/ISTRUZIONI_COMMIT_REV-A1.md`,
  `Final/ESITO_COMMIT_REV-A1.md` — storia dell'innesto N1+F6 sull'impianto A (commit `d8cbca3`).
- `task_card_SPEC-FUNZ-01_ex_novo.md` (+ variante `task_card_ REDO_...md/.txt`) — BOZZE di task card
  per l'eventuale REDO ex novo di SPEC-FUNZ-01 sotto impianto A. Diventano operative solo se il
  supervisore dà il GO e l'Orchestratore le promuove a `tasks/ACTIVE_TASK.md`.

## Regola permanente
La governance del track business-spec si evolve SOLO sull'impianto A. Nessun documento, task card,
review o memoria futuri deve richiamare i file in quarantena. Chi dovesse mai riconsiderare un
meccanismo di B riparta dal FINDING AUDIT (le idee), non dai file archiviati (i testi).
