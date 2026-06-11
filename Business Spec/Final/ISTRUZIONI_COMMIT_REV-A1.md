# ISTRUZIONI per Claude Code — COMMIT REV-A1

> Deposito del lavoro REV-A1: commit dei **soli 3 file** `spec_*` (innesto N1 + F6 su impianto A), push su `origin/main`.
> Commit **per path espliciti**: NON usare `git add .` né `git add -A`. Il working tree contiene untracked da NON toccare (`build/`, `docs/methodology_v2/GA_metodologia_v2.pdf`, `Business Spec/`, `.claude/scheduled_tasks.lock`) e una modifica preesistente non nostra (`.claude/settings.json`).

## STEP 1 — Sanity check pre-commit
Esegui e verifica:
- `git status`
Conferma che i 3 file target risultino `modified`:
  - `.claude/agents/spec_developer.md`
  - `.claude/agents/spec_planner.md`
  - `.claude/agents/spec_reviewer.md`
Se uno dei 3 NON è modified, o se risultano modifiche inattese su altri file tracciati (oltre al noto `.claude/settings.json`): FERMATI, scrivi cosa hai trovato in `Business Spec/Final/ESITO_COMMIT_REV-A1.md`, non committare.

## STEP 2 — Stage SOLO i 3 file (per path)
```
git add .claude/agents/spec_developer.md .claude/agents/spec_planner.md .claude/agents/spec_reviewer.md
```
Poi `git status` e verifica che in "Changes to be committed" ci siano ESATTAMENTE quei 3 file e nient'altro. In particolare `.claude/settings.json` NON deve essere staged. Se lo fosse: `git restore --staged .claude/settings.json`.

## STEP 3 — Commit
```
git commit -m "[REV-A1] spec_*: innesto N1 (atomicita requisito) + F6 (blocchi in batch) su impianto A"
```

## STEP 4 — Push
```
git push origin main
```
Verifica che il push vada a buon fine e che `git status` riporti "up to date with 'origin/main'", niente "ahead".

## STEP 5 — Scrivi l'esito
Scrivi in `Business Spec/Final/ESITO_COMMIT_REV-A1.md`:
- Hash del commit creato (`git rev-parse --short HEAD`) e il messaggio.
- Output di `git show --stat HEAD` (deve elencare SOLO i 3 spec_*).
- Conferma push OK e working tree "up to date".
- Conferma esplicita: nessun file fuori dai 3 target è entrato nel commit (in particolare `.claude/settings.json`, `build/`, il PDF, `Business Spec/` NON sono nel commit).

## VINCOLI
- Stage e commit SOLO dei 3 `spec_*` per path espliciti. Mai `git add .` / `-A`.
- Non toccare `.claude/settings.json` né alcun untracked.
- Se qualcosa è ambiguo o un controllo fallisce: FERMATI, scrivi nell'esito, non forzare.
