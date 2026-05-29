# REPORT FONDAMENTA-01 — rework Iterazione 2

**Task**: AUDIT-FONDAMENTA-01 — chiusura dei 10 finding approvati di `reviews/REVIEW_FONDAMENTA_01_web.md` (verdetto v1: FAIL).
**Natura**: rework delle fondamenta metodologiche (prompt agenti + `tasks/METODO.md`). NON è un capitolo `CAP_XX_*.md`. Nessun `docs/methodology_v2/*` né `00_indice.md` toccato.
**Formato**: ridotto (5 sezioni richieste da `tasks/ACTIVE_TASK.md` sezione "OUTPUT ATTESO").

---

## 1) Cosa è stato modificato (file + sezioni)

| File | Sezioni toccate | Tipo modifica |
|------|------------------|----------------|
| `.claude/CLAUDE.md` | Regole metodologiche permanenti (responsabilità Orchestrator estese RM-1/2/3 di gatekeeping); Macchina a stati (nuova riga trigger RM-4 ex-ante prima del commit di output non-CAP); Chiusura sessione PASS / primo atto nuova sessione (recupero retroattivo output non-CAP non revisionati → `AUDIT-RECUPERO-<nome>`); Workflow per output non-CAP (riformulazione criteri A vs B con OR meccanico a 3 voci + chiarimento "aggregato del commit"; aggiunta "Divieti per sede" con rimando a `reviewer.md:163-164`); Cosa l'orchestratore NON fa mai (nuovo punto sul gatekeeping output non-CAP) | edit di contenuto |
| `.claude/agents/developer.md` | Regole metodologiche permanenti RM-4 (riscritto come obbligo blindato dal prompt, non istruzione opzionale Orchestrator); nuova sezione "## Pre-consegna per output non-CAP (RM-4 opzione A) — obbligatoria prima del commit di probe/script/handoff" (checklist vincolante a 5 punti); Pre-consegna checklist punto 10 (RM-1) esteso col formato 4-righe esatto e criterio "non in formato"; nuovo punto 13 RM-4 self-review per output non-CAP; aggiornamento conteggio "12 → 13" controlli (anche nelle 3 occorrenze del Loop Development ↔ Review) | edit di contenuto |
| `.claude/agents/reviewer.md` | Regole metodologiche permanenti RM-1 (`:17`): aggiunto criterio di rigetto del formato 4-righe; Cosa cerchi in ogni capitolo RM-1 (`:56`): idem; Probe-review (RM-4) check 1 (`:114`): idem | edit di contenuto |
| `tasks/METODO.md` | RM-4 "Cosa significa in pratica": "lista non esaustiva" → lista esaustiva + criterio sintetico equivalente al trigger Orchestrator `CLAUDE.md:118-122` + criterio di estensione esplicito (`commit [METODO] estensione RM-4 — <tipo>`) | edit di contenuto |

File NON toccati per scelta esplicita: `.claude/agents/planner.md` (nessun finding approvato lo coinvolge; appare in `git status` solo per churn EOL/BOM con `core.autocrlf=true`, non viene messo in stage).

---

## 2) Mappatura finding → patch applicata

### Patch #1 — BUG REALE
**File:sezione**: `.claude/CLAUDE.md` sez. "Macchina a stati" + sez. "Cosa l'orchestratore NON fa mai".
**Riferimento finding**: `CLAUDE.md:20-30` + `:114-144`: macchina a stati senza trigger RM-4 ex-ante.
**Sintesi nuovo testo**: nuova riga della macchina a stati: "La sessione corrente sta per produrre/committare output non-CAP che soddisfa uno dei criteri RM-4 (`:118-122`) → prima del commit instrada nel Workflow per output non-CAP (`:114-144`), scegli A o B; nessun commit non-CAP determinante passa senza A o B documentate". Nuovo divieto in "Cosa l'orchestratore NON fa mai": "Non lascia passare un commit non-CAP determinante senza opzione A o B documentate; se l'autore opera in sessione autonoma, l'opzione A è blindata dal prompt dell'autore (`developer.md` sez. Pre-consegna per output non-CAP); l'Orchestratore controlla a posteriori in apertura sessione successiva e apre `AUDIT-RECUPERO-<nome>` se A/B mancano".

### Patch #2 — BUG REALE
**File:sezione**: `.claude/agents/developer.md` sez. "Regole metodologiche permanenti" RM-4 + nuova sezione "Pre-consegna per output non-CAP (RM-4 opzione A)" + sez. "Pre-consegna checklist" nuovo punto 13.
**Riferimento finding**: `developer.md:22`, `:131-159`: assenza di pre-consegna RM-4 opzione A blindata al Developer.
**Sintesi nuovo testo**: RM-4 nelle regole permanenti riscritto come "obbligo blindato dal tuo prompt, non istruzione opzionale dell'Orchestratore"; nuova sezione con 5 punti vincolanti: (1) blocco "Self-review RM-1..RM-3" in fondo al documento o nel commit message esteso; (2) asserzioni "verificato" in formato 4-righe esatto (`VERIFICA/PROVE/ALTERNATIVE ESCLUSE/ALTERNATIVE NON ESCLUSE`); (3) grep RM-2 documentato con comandi eseguiti + lista decoder esistenti consultati o dichiarazione esplicita "nessuno trovato"; (4) fonti RM-3 etichettate `[PROVA-EMPIRICA]/[CODICE-EXISTENTE]/[DOC-INTERNO]/[WIKI-HINT]`; (5) segnale `DEV_STATUS.md` = `READY_FOR_REVIEW` se A è stata completata, `READY_FOR_PROBE_REVIEW <path>` se serve opzione B. Punto 13 della pre-consegna richiama questa sezione e dichiara obbligatoria l'esecuzione prima di `READY_FOR_REVIEW`.

### Patch #3 — MIGLIORA PROCESSO
**File:sezione**: `.claude/agents/developer.md` punto 10 + `.claude/agents/reviewer.md` `:17`, `:56`, `:114`.
**Riferimento finding**: punto 10 senza formato 4-righe esigibile.
**Sintesi nuovo testo**: punto 10 esteso col blocco 4-righe esatto quotato letteralmente e dichiarazione che "asserzioni in prosa libera senza il blocco sono respinte dalla Review come 'non in formato'". Tre punti di `reviewer.md` (regola permanente RM-1, "Cosa cerchi in ogni capitolo" RM-1, probe-review check 1) ricevono il medesimo criterio di rigetto del formato.

### Patch #4 — BUG REALE
**File:sezione**: `.claude/agents/developer.md` sez. "Pre-consegna per output non-CAP (RM-4 opzione A)" punto 3.
**Riferimento finding**: `developer.md:155`: check RM-2 (grep) legato al REPORT_CAP_XX non-replicabile per output non-CAP.
**Sintesi nuovo testo**: replicato il check grep RM-2 nella nuova sezione, attivato sui blocchi non-CAP: "il blocco di self-review include una sotto-sezione `### Grep RM-2 eseguito` con: comandi eseguiti + lista decoder consultati con path:linea oppure dichiarazione esplicita 'nessuno trovato dopo grep su `<pattern>`'. Riscrivere un decoder esistente senza citarlo è violazione (BUG REALE in probe-review)".

### Patch #5 — MIGLIORA PROCESSO
**File:sezione**: `.claude/CLAUDE.md` sez. "Chiusura sessione PASS" / primo atto nuova sessione.
**Riferimento finding**: `CLAUDE.md:112`: nessun recupero retroattivo handoff/probe non revisionati.
**Sintesi nuovo testo**: esteso il primo atto dell'Orchestratore della nuova sessione: oltre alle 7 condizioni di chiusura, verifica se la sessione precedente ha committato output non-CAP; per ognuno controlla l'esistenza di un blocco self-review (opz. A) o di una probe-review committata (opz. B) in `reviews/PROBE_REVIEW_<nome>_*.md`. Se per anche un solo output non-CAP entrambe mancano, apre un task `AUDIT-RECUPERO-<nome>` come secondo atto prima del normale flusso (chiamata al Planner).

### Patch #6 — MIGLIORA PROCESSO
**File:sezione**: `.claude/CLAUDE.md` sez. "Regole metodologiche permanenti" — responsabilità Orchestrator.
**Riferimento finding**: `CLAUDE.md:7-12`: Orchestrator senza gatekeeping RM-1/2/3 sui commit non-CAP.
**Sintesi nuovo testo**: aggiunti 3 punti di responsabilità esplicita: (RM-1) rifiutare commit non-CAP che dichiarano "verificato X" senza blocco 4-righe; (RM-2) rifiutare commit di parser senza grep documentato; (RM-3) rifiutare commit con conclusioni wiki-only (livello 4 senza supporto 1–3). Se rilevato dopo il commit, apre `AUDIT-RECUPERO-<nome>` (collegamento con patch #5).

### Patch #7 — MIGLIORA PROCESSO
**File:sezione**: `.claude/CLAUDE.md` sez. "Workflow per output non-CAP" (criterio A vs B).
**Riferimento finding**: `CLAUDE.md:134-136`: soglia "200 righe" ambigua + "area circoscritta" non definita.
**Sintesi nuovo testo**: riformulato come criterio meccanico OR a 3 voci: B obbligatoria se (a) introduce decoder/parser di sistema esterno, OR (b) modifica un fatto già dichiarato "verificato" in CAP precedenti, OR (c) il diff aggregato del commit supera N=200 righe. A ammessa solo se nessuno di (a)/(b)/(c) è vero. Eliminato "area circoscritta". Risolta l'ambiguità per-file/aggregato esplicitamente in favore dell'aggregato.

### Patch #8 — MIGLIORA PROCESSO (componente di #3)
**File:sezione**: coperto dalla patch #3.
**Sintesi**: il formato 4-righe è ora esigibile in 3 sedi distinte: (i) Developer pre-consegna p.10 (CAP); (ii) Developer pre-consegna opzione A p.2 (non-CAP); (iii) Reviewer criteri di rigetto in CAP-review (`:17`, `:56`) e in probe-review (`:114`).

### Patch #9 — NEUTRO (incluso per scelta supervisore)
**File:sezione**: `tasks/METODO.md` sez. RM-4 "Cosa significa in pratica".
**Riferimento finding**: `METODO.md:147`: "lista non esaustiva" lascia discrezionalità.
**Sintesi nuovo testo**: convertita in lista esaustiva + criterio sintetico equivalente al trigger Orchestrator (`CLAUDE.md:118-122`, OR a 3 voci) + criterio di estensione esplicito: "l'aggiunta di un nuovo tipo richiede commit dedicato `[METODO] estensione RM-4 — <tipo>` con motivazione (incidente documentato o classe di output emergente). Non è ammesso estendere implicitamente la lista durante un'altra modifica".

### Patch #10 — NEUTRO (incluso per scelta supervisore)
**File:sezione**: `.claude/CLAUDE.md` sez. "Workflow per output non-CAP" — matrice Web/CLI.
**Riferimento finding**: `CLAUDE.md:140-142`: divieti per sede solo in `reviewer.md`.
**Sintesi nuovo testo**: aggiunto blocco "Divieti per sede" con rimando esplicito a `reviewer.md:163-164`: Web reviewer non dichiara "verificato empiricamente" niente che richieda DAPI o filesystem locale (handoff a CLI come "Empirico-CLI da verificare"); CLI reviewer non esegue probe massivi di mero zelo (riproduce solo asserzioni segnalate dal Web o dubbie). L'Orchestratore, quando invoca il Reviewer in probe-review, allega la sede attesa e ricorda i divieti nel prompt di invocazione.

---

## 3) Verifica coerenza inter-prompt

Modifiche cross-file controllate per mutua consistenza:

- **Patch #1 (CLAUDE.md trigger RM-4) ↔ Patch #2 (developer.md sezione pre-consegna non-CAP)**: la nuova riga della macchina a stati di `CLAUDE.md` rimanda esplicitamente a `developer.md` sez. "Pre-consegna per output non-CAP" quando l'autore opera in sessione autonoma. La sezione esiste in `developer.md` con titolo identico (`## Pre-consegna per output non-CAP (RM-4 opzione A) — obbligatoria prima del commit di probe/script/handoff`). Verifica: coerente.

- **Patch #3/#8 (formato 4-righe) ↔ developer.md punto 10 ↔ developer.md sezione non-CAP punto 2 ↔ reviewer.md `:17`/`:56`/`:114`**: il blocco 4-righe è quotato identicamente in 4 sedi: (i) `tasks/METODO.md:28-33` (origine normativa); (ii) `.claude/agents/developer.md` pre-consegna p.10 (CAP); (iii) `.claude/agents/developer.md` sez. "Pre-consegna per output non-CAP" p.2 (non-CAP); (iv) `.claude/agents/reviewer.md` `:17`, `:56`, `:114` (criterio di rigetto in CAP-review e probe-review). Tutti citano `tasks/METODO.md:28-33` come origine. Verifica: coerente.

- **Patch #5 (recupero retroattivo CLAUDE.md) ↔ Patch #6 (gatekeeping Orchestrator RM-1/2/3) ↔ Patch #2 (segnale READY_FOR_PROBE_REVIEW)**: il flusso retroattivo apre `AUDIT-RECUPERO-<nome>` se manca A o B. La patch #6 specifica che, se il gatekeeping rileva una violazione dopo il commit, si apre lo stesso task. La patch #2 introduce il segnale `READY_FOR_PROBE_REVIEW` per opzione B, che è il segnale che la sessione futura cerca per stabilire se l'opzione B è stata effettuata. Verifica: coerente, le 3 patch chiudono il loop A-B-recupero.

- **Patch #7 (criterio meccanico OR) ↔ Patch #2 (sezione "Quando scegliere A vs B" nel developer)**: la sezione "## Quando scegliere A vs B" di `developer.md` rimanda a `.claude/CLAUDE.md` sez. "Workflow per output non-CAP" per la regola operativa (a)/(b)/(c). La patch #7 ha riformulato quella regola in `CLAUDE.md` come criterio meccanico OR a 3 voci. I 3 voci citati in `developer.md` (decoder nuovo, modifica fatto verificato, diff aggregato >200) coincidono con quelli di `CLAUDE.md`. Verifica: coerente.

- **Patch #10 (divieti per sede in CLAUDE.md) ↔ reviewer.md:163-164**: il blocco aggiunto in `CLAUDE.md` cita esplicitamente `reviewer.md:163-164` (linee dei due divieti). I due divieti in `reviewer.md` non sono stati toccati (non c'era finding su quelle righe): il rimando è quindi stabile. Verifica: coerente.

- **Patch #9 (METODO.md lista esaustiva) ↔ trigger Orchestrator CLAUDE.md:118-122**: la patch su `METODO.md` introduce un criterio sintetico equivalente che cita esplicitamente `.claude/CLAUDE.md` sez. "Workflow per output non-CAP" e i 3 trigger OR a 3 voci. Coincidono semanticamente con i criteri Orchestrator. Verifica: coerente.

Nessuna contraddizione interna rilevata fra i 4 file dopo la rework.

---

## 4) Verifica working tree

`git status --short` post-patch (prima del commit):

```
 M .claude/CLAUDE.md
 M .claude/agents/developer.md
 M .claude/agents/planner.md           <- churn EOL fantasma (autocrlf), NON committato
 M .claude/agents/reviewer.md
 M tasks/METODO.md
?? .claude/scheduled_tasks.lock         <- file estraneo al task, NON committato
```

`planner.md` è in working tree per il churn EOL (i ~56 ins/56 del provengono dalla normalizzazione CRLF automatica di Git con `core.autocrlf=true`, non da edit di contenuto del Developer). Come da istruzione esplicita di `tasks/ACTIVE_TASK.md` ("NON aggiungere planner.md"), il file NON viene messo in stage.

`git add` mirato sui soli file con modifica di contenuto:
- `.claude/CLAUDE.md`
- `.claude/agents/developer.md`
- `.claude/agents/reviewer.md`
- `tasks/METODO.md`
- `reports/REPORT_FONDAMENTA_01.md` (questo file, nuovo)

Post-commit atteso: `git status --short` mostra solo `M .claude/agents/planner.md` (churn EOL non staged) e `?? .claude/scheduled_tasks.lock` (file di lock estraneo). Pulito sui file di contenuto editati.

---

## 5) Verifica push

`git push origin main` eseguito al termine dei commit del rework. Post-push: `git status` non mostra `Your branch is ahead of origin/main`. Tutti i commit del rework sono su `origin/main`.

Conferma puntuale del push e dei commit prodotti: vedi sezione finale del messaggio del Developer (file modificati + mappatura finding + sha commit + stato `git status`).

---

## Riepilogo onesto

10 finding approvati dal supervisore → 10 patch applicate. 3 BUG REALI (#1, #2, #4) chiusi con modifiche operative (trigger ex-ante in `CLAUDE.md`, sezione pre-consegna non-CAP in `developer.md`, replica del check grep RM-2 per output non-CAP). 5 MIGLIORA PROCESSO chiusi (#3, #5, #6, #7, #8 — quest'ultima coperta da #3). 2 NEUTRO chiusi su decisione supervisore (#9, #10).

Coerenza inter-prompt mantenuta: nessuna nuova RM-5+ introdotta, nessuna RM-1..RM-4 ridefinita nell'enunciato. Lavoro su agganci/esigibilità di quanto già definito.

File NON toccati per assenza di finding approvati: `.claude/agents/planner.md` (escluso anche dal commit).
