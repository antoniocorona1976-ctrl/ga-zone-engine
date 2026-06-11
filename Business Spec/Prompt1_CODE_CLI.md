CONTESTO
Sei nel repo ga-zone-engine. Devi sostituire 6 file di governance del track business-spec
con le versioni revisionate [REV-4CH-audit] che si trovano nella cartella di staging
"Business Spec/Final/". Operazione = SOLO sostituzione file nel working tree.
NON committare, NON fare push, NON toccare altro.

STEP 1 — Verifica sorgente (fermati se qualcosa non torna)
Elenca il contenuto di "Business Spec/Final/". Conferma che ci siano ESATTAMENTE questi 6 file:
- spec_planner.md
- spec_developer.md
- spec_reviewer.md
- TEMPLATE_SPEC_FUNZ.md
- TRACCIABILITA.md
- SPEC_CHECK_STATICI.md
Se un nome è diverso (es. spazi al posto degli underscore) o manca un file: FERMATI e segnalamelo,
non indovinare la corrispondenza.
Se è presente anche ACTIVE_TASK_INFRA-LINT-CH2.md: LASCIALO DOV'È, non fa parte di questa operazione.

STEP 2 — Sostituzione (usa read+write con i tuoi tool, NON copy da shell:
il path sorgente contiene uno spazio ed evitiamo problemi di quoting)
Per ciascun file: leggi il sorgente e scrivi il contenuto IDENTICO alla destinazione,
sovrascrivendo se esiste, creando cartella e file se non esistono.

  "Business Spec/Final/spec_planner.md"        ->  .claude/agents/spec_planner.md
  "Business Spec/Final/spec_developer.md"       ->  .claude/agents/spec_developer.md
  "Business Spec/Final/spec_reviewer.md"        ->  .claude/agents/spec_reviewer.md
  "Business Spec/Final/TEMPLATE_SPEC_FUNZ.md"   ->  docs/spec_funzionale/TEMPLATE_SPEC_FUNZ.md
  "Business Spec/Final/TRACCIABILITA.md"        ->  docs/spec_funzionale/TRACCIABILITA.md
  "Business Spec/Final/SPEC_CHECK_STATICI.md"   ->  specs/checks/SPEC_CHECK_STATICI.md

STEP 3 — Verifica
Per ciascuna coppia conferma che destinazione e sorgente siano identici (diff vuoto).
Riporta eventuali differenze residue.

STEP 4 — NON committare
NON eseguire git add / git commit / git push. Lascia tutto nel working tree per la mia review in VS Code.
Esegui "git status" e "git --no-pager diff --stat" e riportami in una tabella:
quali file creati ex-novo (compaiono come untracked in status) e quali sovrascritti (compaiono nel diff).

VINCOLI
- Non modificare NESSUN file fuori dalle 6 destinazioni.
- Non installare né spostare l'ACTIVE_TASK.
- Niente commit, niente push.
- Se qualcosa è ambiguo, fermati e chiedi prima di agire.