CONTESTO
La precedente sostituzione integrale dei tre agent file spec_* è stata una REGRESSIONE:
ha cancellato impianto preesistente (bi-sede, RM-1/2/3, eredità CAP, ecc.).
Vanno RIPRISTINATI allo stato dell'ultimo commit (HEAD), recuperando gli originali nel working tree.
Operazione = SOLO ripristino di 3 file + localizzazione di 2 file. NIENTE commit, NIENTE push, NIENTE git clean.

STEP 1 — Ripristino scoped (ESATTAMENTE questi 3 path, nessun altro)
Esegui:
  git checkout -- .claude/agents/spec_planner.md .claude/agents/spec_developer.md .claude/agents/spec_reviewer.md

NON usare: git checkout . (senza path), git reset, git clean, git restore su altri path.
Se uno dei 3 file non risultasse tracciato/committato (quindi non ripristinabile): FERMATI e segnalamelo.

STEP 2 — Verifica ripristino
Esegui e riportami l'output:
  git --no-pager diff -- .claude/agents/spec_planner.md .claude/agents/spec_developer.md .claude/agents/spec_reviewer.md
  git status
Atteso: i 3 spec_* NON compaiono più come modificati (diff vuoto, tornati a HEAD).

STEP 3 — Conferma che il resto è intatto (NON toccare)
Conferma che siano ancora presenti come untracked (??) e NON modificati:
  docs/spec_funzionale/TEMPLATE_SPEC_FUNZ.md
  docs/spec_funzionale/TRACCIABILITA.md
  specs/checks/SPEC_CHECK_STATICI.md
Conferma che .claude/settings.json sia ancora com'era (NON toccato da te).

STEP 4 — Localizza i 2 file di riconciliazione (sola lettura, non modificare)
Verifica che esistano e riportami path esatto + numero righe di:
  tasks/METODO.md
  .claude/BASE_COMUNE.md
Se uno dei due ha nome o path diverso da quello atteso: FERMATI e dimmi dove sono davvero.

VINCOLI
- Niente commit, niente push, niente git clean, niente git reset.
- Tocchi SOLO i 3 path dello STEP 1 (ripristino). Tutto il resto è sola lettura.
- Se qualcosa è ambiguo, fermati e chiedi prima di agire.