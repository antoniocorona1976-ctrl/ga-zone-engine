# BASE COMUNE — approccio e processo condivisi dagli agenti ga-zone-engine

**Scopo**: definire l'**approccio e la base comune** a TUTTI i track del progetto:

- **Track Metodologia v2** — capitoli `CAP-XX` in `docs/methodology_v2/` (ruoli: `planner.md`, `developer.md`, `reviewer.md`).
- **Track Business-spec** — specifiche funzionali/di prodotto `SPEC-FUNZ-NN` in `docs/spec_funzionale/` (ruoli: `spec_planner.md`, `spec_developer.md`, `spec_reviewer.md`).

Ciò che è **specifico** di un track vive nei ruoli di quel track e nella relativa sezione di `.claude/CLAUDE.md`. Ciò che è **comune** vive qui. Questo file **non sostituisce** `tasks/METODO.md` (RM-1..RM-4) né i ruoli: li **integra**.

**Ordine di lettura obbligatorio per ogni agente, a inizio sessione:**
1. `tasks/METODO.md` — RM-1..RM-4 (vincolanti, universali, validi su entrambi i track e su tutti gli output)
2. `.claude/BASE_COMUNE.md` — questo file (approccio comune)
3. il proprio ruolo: `.claude/agents/<ruolo>.md` (metodologia) **oppure** `.claude/agents/spec_<ruolo>.md` (business-spec)
4. `tasks/ACTIVE_TASK.md` — il task corrente

---

## 1. Il ciclo Planner → Developer → Reviewer

Identico per entrambi i track. Il completamento di un task **non** è "ho prodotto i file"; è **"Reviewer ha emesso PASS"** (e per la metodologia: il Planner ha approvato il passaggio al task successivo).

Sequenza forzata:
1. **Planner** definisce `tasks/ACTIVE_TASK.md` (scope, acceptance criteria, out-of-scope, eredità). Non scrive il documento, non fa audit.
2. **Developer** produce il documento + il REPORT supervisore; esegue la pre-consegna checklist; scrive `READY_FOR_REVIEW` in `tasks/DEV_STATUS.md`; si ferma.
3. **Orchestratore** esegue il **check post-Developer** (§5). Se OK invoca il Reviewer; altrimenti rilancia il Developer con prompt mirato ai gap.
4. **Reviewer** fa audit ostile (due giri, §6) e produce il file di review con verdetto **PASS / CONDITIONAL / FAIL**.
5. Su CONDITIONAL/FAIL → **punto di controllo supervisore** (§4). Su PASS → chiusura (le condizioni di chiusura sono definite dalla sezione di track in `CLAUDE.md`).

## 2. Macchina a stati dell'Orchestratore (pattern generico)

L'Orchestratore legge i file di stato nell'ordine e agisce **sulla prima condizione vera**. Il pattern è comune; il **discriminatore di chiusura**, i **path di output** e le **condizioni di chiusura** sono definiti dalla sezione del track attivo in `CLAUDE.md` (Metodologia: `00_indice.md` + 7 condizioni CAP; Business-spec: `STATO_CORRENTE.md`/`ACTIVE_TASK.md` + chiusura adattata, indice N/A). L'Orchestratore determina il **track attivo** dall'intestazione di `tasks/ACTIVE_TASK.md` (`# TASK ATTIVO: CAP-XX ...` → Metodologia; `# TASK ATTIVO: SPEC-FUNZ-NN ...` → Business-spec).

## 3. ★ Reviewer BI-SEDE — Claude Code CLI + Claude Code Web

Vincolo permanente del progetto, valido per **entrambi i track**: il Reviewer può girare in **due sedi con capacità asimmetriche**, e le si usa come pipeline complementare.

- **Web** (Claude Code on the web): container Linux nel cloud. Vede il repo via Git/MCP, **NON** il PC del supervisore, **NON** può lanciare contro DAPI, **NON** vede file locali non versionati (`probe_out/`, `C:\...`). È la sede dell'**audit statico** (documento + grep + Read del codice/CAP committati).
- **CLI locale** (Claude Code CLI sul PC del supervisore): vede `C:\` e il filesystem locale, lancia PowerShell/Python **contro DAPI live** se DGo+Darwin sono attivi. È la sede della **verifica empirica** (riproduzione di misurazioni, dump locali).

**Matrice di assegnazione (sintesi):**

| Tipo di output da auditare | Sede primaria |
|---|---|
| Documento (CAP-XX, SPEC-FUNZ, handoff, indagine, `probe_*.md`) | Web (audit statico) |
| Script di parsing/decoder di sistema esterno | Web (statico RM-1/2/3) **+** CLI (esecuzione su payload reale se Web segnala dubbio) |
| Risultato empirico (V-1, V-2, ...) / dump locali (`exports/`, `probe_out/`) | CLI |
| Asserzione "verificato X" che richiede prova diretta | Web identifica → CLI ri-testa |

**Divieti per sede (vincolanti):**
- Il **Web reviewer** NON dichiara "verificato empiricamente" nulla che richieda DAPI o il filesystem locale: lo segnala come **"Empirico-CLI da verificare"** e lascia handoff alla sede CLI.
- Il **CLI reviewer** NON esegue probe DAPI massivi di mero zelo: riproduce solo le asserzioni puntuali segnalate dal Web o trovate dubbie nel primo giro.

**Handoff cross-ambiente**: quando un audit richiede ENTRAMBE le sedi, il Web pubblica `reviews/PROBE_REVIEW_<nome>_web.md` + lista "Empirico-CLI da verificare"; l'Orchestratore (anche in sessione successiva) invoca il CLI con quella lista; il CLI pubblica `reviews/PROBE_REVIEW_<nome>_cli.md`; l'Orchestratore raccoglie i due audit e produce il verdetto finale.

> Per il track **Business-spec** la sede tipica è **Web-statico** (consolida fatti già chiusi, nessun fatto empirico nuovo → lista Empirico-CLI attesa **vuota**). La sede **CLI resta disponibile** se una sezione della spec dovesse richiedere una verifica empirica/locale. Una review documentale no-DAPI è eseguibile **anche in sessione CLI** (capability-equivalente): in tal caso il CLI applica comunque il proprio divieto (niente probe di zelo).

## 4. Classificazione dei finding + punto di controllo supervisore

Ogni Reviewer classifica i finding in **4 categorie**: `BUG REALE` / `MIGLIORA PERFORMANCE` / `NEUTRO` / `RISCHIO PEGGIORAMENTO`, in una tabella "Classificazione per il supervisore" (`# | Problema | file:riga | Classificazione | Mandare a Development?`).

Regole:
- I **BUG REALI** vanno sempre a Developer.
- **NEUTRO** e **RISCHIO PEGGIORAMENTO** **non** vanno a Developer senza **esplicita approvazione del supervisore**.
- Su **CONDITIONAL/FAIL** l'Orchestratore **non** chiama Developer in automatico: presenta la tabella al supervisore, attende la decisione, aggiunge i soli finding approvati in `ACTIVE_TASK.md` (sezione "Finding di Review da risolvere"), azzera `DEV_STATUS.md`, poi chiama Developer.
- Su **PASS** con osservazioni NEUTRO: l'Orchestratore può applicarle solo se il supervisore le approva (micro-pass + re-review).

## 5. Check post-Developer (6 controlli — generici)

Prima di chiamare il Reviewer, quando `DEV_STATUS.md = READY_FOR_REVIEW`, l'Orchestratore verifica **da sé** (non sulla parola del Developer):
1. **File documento** esiste e non è vuoto.
2. **File report** esiste con le 5 sezioni del formato supervisore + tabella verifica AC.
3. **Indice/stato aggiornato** secondo il track (Metodologia: `00_indice.md` IN REVIEW; **Business-spec: N/A** — `00_indice.md` non si tocca).
4. **Working tree pulito** sui file del task (noise `.claude/*`, `build/`, ecc. tollerato).
5. **Commit pushato** (niente "ahead of origin/main").
6. **Commit copre i file attesi** del track.

Se anche un solo controllo manca: NON chiamare Reviewer, NON correggere tu i file, rilancia Developer con prompt mirato ai gap.

## 6. Doppio giro ostile + terminazione del loop

Il Reviewer è **ostile per default** (il suo valore è trovare problemi reali, non validare). Dopo il primo giro **rifà** il giro ("sono sicuro di aver trovato tutto?"). Non riporta cosmesi senza impatto reale. Ogni iterazione di review **appende** un blocco al file di review, non sovrascrive il precedente. **Terminazione**: se Review e Development sono in disaccordo dopo **3 iterazioni** sullo stesso punto, decide il supervisore; nessuno chiude il loop unilateralmente.

## 7. Disciplina dei file di stato + push

- `tasks/ACTIVE_TASK.md` (Planner), `tasks/DEV_STATUS.md` (Developer; azzerato dall'Orchestratore a ogni ciclo), `tasks/CARRYOVER.md` (M-promemoria; scritto dall'Orchestratore in chiusura), `tasks/STATO_CORRENTE.md` (single source of truth) sono **single-writer per disciplina**: mai pushare con working tree dirty su questi file.
- **Push policy**: push **diretto su `origin/main`** (trunk) da parte di developer/reviewer/planner è prassi approvata; l'Orchestratore non chiede conferma per ogni push. Il progetto lavora **su `main`** (anche i track non-CAP: isolamento del contenuto via cartella dedicata, non via branch).
- **Il Planner non committa** il task card (per disciplina di gatekeeping): scrive `ACTIVE_TASK.md` e si ferma; **l'Orchestratore** rivede e committa il task card.

## 8. Onestà claim → evidenza

Vincolante per tutti. La tabella AC nel REPORT usa `OK / PARZIALE / MANCA` in modo veritiero, con evidenza puntuale (`file:riga`) per ogni `OK`. Il Reviewer applica **RM-1 a sé stesso** (ogni "verificato/MATCH/coerente/non trovato dopo grep" ha sostegno operativo: citazione + esito) in una sezione "Applicazione RM-1 a me stesso".

## 9. Registry subagenti (come invocare i ruoli)

- `developer` e `reviewer` **non** sono esposti come `subagent_type`: si eseguono via **`general-purpose` che adotta** il rispettivo `.md`.
- I tre ruoli **business-spec** (`spec_planner`, `spec_developer`, `spec_reviewer`) si eseguono **via `general-purpose` che adotta** `.claude/agents/spec_<ruolo>.md`.
- Il `planner` della **metodologia** è invocabile come `subagent_type: planner` (tools Read/Write/Glob, niente Bash → l'Orchestratore committa il task card).
- L'Orchestratore include sempre nel prompt di invocazione: "leggi `tasks/METODO.md` e `.claude/BASE_COMUNE.md` prima di iniziare", oltre al ruolo specifico.
