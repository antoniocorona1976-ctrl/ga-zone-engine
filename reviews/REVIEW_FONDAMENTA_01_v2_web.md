# Re-Review FONDAMENTA-01 v2 — Audit indipendente RM-1..RM-4 post-rework Iter.2

**Task**: AUDIT-FONDAMENTA-01 Iter.3 (tasks/ACTIVE_TASK.md rev. corrente, sezione "Finding di Review approvati per rework").
**Perimetro auditato (P1..P5)**:
- P1 tasks/METODO.md (commit 2558750)
- P2 .claude/CLAUDE.md (commit f6de106)
- P3 .claude/agents/planner.md (intatto — fuori scope per scelta del task)
- P4 .claude/agents/developer.md (commit 4d9c68b)
- P5 .claude/agents/reviewer.md (commit 4d9c68b)

**Stato git**: origin/main allineato a dbce3fa; working tree pulito sui 5 file (solo .claude/agents/planner.md con churn EOL non staged, e .claude/scheduled_tasks.lock fuori scope).
**Sede**: WEB.
**Conflitto di interesse epistemico**: dichiarato in v1. La re-review è eseguita dallo stesso ruolo Reviewer ma su nuovo contenuto, con grep di verifica.
**Riferimento v1**: reviews/REVIEW_FONDAMENTA_01_web.md (commit 3ed0198), verdetto FAIL.

---

## Verdetto

**CONDITIONAL** (Sede: WEB)

Motivazione sintetica:

- I **3 BUG REALI** (#1, #2, #4) e le **5 MIGLIORA PROCESSO** (#3, #5, #6, #7, #8) sono **chiusi sostanzialmente**: i 5 punti C.1..C.5 di v1 (4 fughe + 1 fuga parziale) sono **tutti intercettati** dai nuovi prompt. Il pattern d errore canonico (PRICE_EXTENDED / scenario 28/05) non passa più senza opzione A o B.
- Tuttavia il rework ha introdotto **2 regressioni inter-prompt** (cross-reference) e **1 nuovo gap di processo** (orchestrator non gestisce READY_FOR_PROBE_REVIEW nella macchina a stati). I nuovi finding sono di tipo **MIGLIORA PROCESSO**, non BUG REALE: la sostanza dei prompt blinda comunque il pattern via il prompt-prompt dell autore (developer.md sezione Pre-consegna non-CAP), ma i rimandi di riga sono fuori sincrono e generano confusione operativa.

Non ci sono problemi bloccanti aggiuntivi che vanifichino il rework: per AC-S di v1, le fughe del Check B sono chiuse, il PASS sarebbe ammissibile sulla sufficienza, ma le regressioni inter-prompt impediscono un PASS "pulito". Verdetto: **CONDITIONAL** (decisione supervisore su #N1..#N3).

---

## Metodo di verifica dei finding (RM-1 — nessuna asserzione senza prova)

Tutti e tre i finding sono stati verificati con `Read` diretto delle righe citate e `Grep` sui marker, in sede WEB (audit statico, nessun accesso a DAPI/filesystem live). I rimandi di riga sono confrontati col contenuto reale del file di destinazione al commit corrente (`origin/main` allineato a `dbce3fa`). Grep eseguiti:

- `grep -rn "READY_FOR_PROBE"` su tutto il repo → occorrenze in `.claude/agents/developer.md:133,152,164,201`; nessuna in `.claude/CLAUDE.md`.
- `grep -n "reviewer\.md:\d|developer\.md:\d|CLAUDE\.md:\d|METODO\.md:\d|planner\.md:\d"` su `.claude/` → enumerazione dei cross-reference inter-prompt.

Letture di conferma: `developer.md:131-164` e `:188-203`; `CLAUDE.md:114-126`, `:138-157`, `:27-33`.

---

## Finding #N1 — Rimando di riga fuori sincrono: matrice di sede Web/CLI (MIGLIORA PROCESSO)

**Descrizione**: il prompt Developer, nel punto in cui spiega che la sede (Web/CLI) della probe-review è decisa dall'Orchestratore "secondo la matrice", rimanda a un intervallo di righe di `.claude/CLAUDE.md` che NON contiene la matrice di sede, bensì i criteri meccanici (a)/(b)/(c) di scelta dell'opzione B.

**Evidenza (path:linea reali)**:
- Rimando errato: `.claude/agents/developer.md:152` — "La sede (Web/CLI) del Reviewer è decisa dall'Orchestratore secondo la matrice `tasks/METODO.md` §RM-4 / `.claude/CLAUDE.md:140-142`."
- Contenuto reale a destinazione `.claude/CLAUDE.md:140-142` — è il blocco "**B (probe-review formale del Reviewer) è obbligatoria se almeno uno è vero**: (a) decoder/parser di sistema esterno; (b) modifica un fatto già verificato; (c) diff aggregato > N righe". Sono i **criteri di scelta A/B**, non la matrice di sede.
- Destinazione corretta: la matrice di sede Web / CLI locale / Entrambe è a `.claude/CLAUDE.md:149-153` (apertura: "**Quando sceglie B (review formale leggera), l'Orchestratore decide anche la sede del reviewer** ... secondo la matrice ...", poi i 3 bullet Web/CLI/Entrambe).

**Impatto**: chi segue il rimando dal prompt Developer per capire come viene scelta la sede atterra sul criterio A/B (decoder/diff>200) e non trova la regola Web/CLI/Entrambe. Confusione operativa, nessun output sbagliato del GA: il prompt Developer comunque rinvia correttamente anche a `tasks/METODO.md §RM-4`, dove la matrice esiste. Non è un BUG REALE perché non altera la blindatura del pattern d'errore canonico né il comportamento del motore; degrada solo la navigabilità inter-prompt.

**Classificazione**: MIGLIORA PROCESSO.

**Fix consigliato (puntuale)**: in `.claude/agents/developer.md:152` sostituire il riferimento `.claude/CLAUDE.md:140-142` con `.claude/CLAUDE.md:149-153` (matrice di sede). In alternativa, sostituire il rimando numerico con un rimando per àncora di sezione (es. "§Workflow per output non-CAP — matrice di sede") per renderlo resistente al churn di riga.

---

## Finding #N2 — Rimando di riga fuori sincrono: criteri OR di definizione output non-CAP (MIGLIORA PROCESSO)

**Descrizione**: il prompt Developer rimanda alla definizione operativa dei tre criteri OR che qualificano un output come "non-CAP determinante" (parsing payload esterno / dichiarazione "fatti verificati" / asserzioni destinate a CARRYOVER) puntando a `.claude/CLAUDE.md:118-122`, che è però l'intestazione della sezione più la frase introduttiva, non l'enumerazione dei tre criteri. Lo stesso rimando errato è replicato nella tabella della macchina a stati dell'Orchestratore.

**Evidenza (path:linea reali)**:
- Rimando errato (Developer): `.claude/agents/developer.md:133` — "(definizione: cfr. `tasks/METODO.md` §RM-4 e `.claude/CLAUDE.md:118-122` — parsing payload di sistemi esterni, dichiarazione "fatti verificati" da citare in CAP successivi, asserzioni destinate a CARRYOVER)".
- Rimando errato (Orchestratore, replicato): `.claude/CLAUDE.md:30` (riga della macchina a stati) — "...output non-CAP che soddisfa uno dei criteri RM-4 (`:118-122` — parsing payload esterno, ...)".
- Contenuto reale a destinazione `.claude/CLAUDE.md:118-122` — riga 118 è il titolo "## Workflow per output non-CAP (probe, script, handoff) — RM-4"; 120 è la frase di apertura; 122 è "L'Orchestratore valuta se un output non-CAP rientra in RM-4 quando uno qualunque di questi è vero:". I tre criteri NON sono in questo intervallo.
- Destinazione corretta: i tre criteri OR sono i bullet a `.claude/CLAUDE.md:124-126` ("L'output è uno script/decoder che parsa payload..."; "L'output è un documento che dichiara fatti verificati..."; "L'output produce M-promemoria o asserzioni che entreranno in CARRYOVER").

**Impatto**: chi apre `CLAUDE.md:118-122` per leggere i tre criteri trova solo titolo + introduzione e deve cercare oltre. Il testo del rimando elenca comunque i tre criteri inline, quindi il contenuto non si perde; resta un disallineamento di àncora. Doppio punto di manutenzione (developer.md + tabella macchina a stati) con lo stesso off-by-range. Non BUG REALE: non incide su selezione/ranking/fitness del GA.

**Classificazione**: MIGLIORA PROCESSO.

**Fix consigliato (puntuale)**: aggiornare entrambi i rimandi a `.claude/CLAUDE.md:124-126` (i tre bullet OR). In `.claude/CLAUDE.md:30` correggere `:118-122` → `:124-126`; in `.claude/agents/developer.md:133` idem. Preferibile sostituire con rimando per àncora di sezione ("§Workflow per output non-CAP — criteri OR") per immunizzare dal churn di riga futuro.

---

## Finding #N3 — Macchina a stati Orchestratore non gestisce `READY_FOR_PROBE_REVIEW` (MIGLIORA PROCESSO)

**Descrizione**: il rework Iter.2 ha introdotto nel prompt Developer un nuovo stato di uscita `READY_FOR_PROBE_REVIEW <path>` da scrivere in `tasks/DEV_STATUS.md` quando il commit ricade in opzione B (probe-review formale, criterio (a)/(b)/(c)). Ma la tabella della macchina a stati dell'Orchestratore in `.claude/CLAUDE.md` non ha alcuna riga che intercetti questo marker: l'unico stato di `DEV_STATUS.md` gestito è `READY_FOR_REVIEW`. Quando il Developer emette `READY_FOR_PROBE_REVIEW`, l'Orchestratore non ha una transizione definita e cade nella riga generica di default (Developer) o resta senza azione deterministica.

**Evidenza (path:linea reali)**:
- Marker prodotto/atteso dal Developer: `.claude/agents/developer.md:133` ("...scrivi `READY_FOR_PROBE_REVIEW <path>` in `tasks/DEV_STATUS.md` e fermati senza committare"), ribadito a `:152`, `:164` ("il segnale corretto è `READY_FOR_PROBE_REVIEW`, non `READY_FOR_REVIEW`") e `:201`.
- Tabella macchina a stati Orchestratore: `.claude/CLAUDE.md:27-33`. La riga `.claude/CLAUDE.md:32` intercetta esclusivamente "`tasks/DEV_STATUS.md` contiene `READY_FOR_REVIEW`". Nessuna riga della tabella (27-33) cita `READY_FOR_PROBE_REVIEW`.
- Grep di conferma: `grep -rn "READY_FOR_PROBE"` → 4 hit in `developer.md`, **0 hit in `.claude/CLAUDE.md`**.

**Impatto**: gap di processo nel ciclo non-CAP opzione B. Se il Developer instrada correttamente verso probe-review (come imposto dai criteri (a)/(b)/(c)), l'Orchestratore non ha una regola che dica "leggi il path, invoca il reviewer in modalità probe-review nella sede X". Rischio: lo stato `READY_FOR_PROBE_REVIEW` viene trattato come `READY_FOR_REVIEW` (chiamata CAP-review piena anziché probe-review leggera) oppure ignorato. Non è BUG REALE sul motore/GA, ma è una rottura della catena di handoff RM-4 introdotta proprio dal rework: il workflow opzione B è descritto nelle sezioni discorsive di CLAUDE.md ma non è agganciato alla tabella decisionale che l'Orchestratore consulta "sulla prima condizione vera".

**Classificazione**: MIGLIORA PROCESSO.

**Fix consigliato (puntuale)**: aggiungere alla tabella della macchina a stati (`.claude/CLAUDE.md:27-33`), prima o dopo la riga `READY_FOR_REVIEW`, una riga del tipo:

> | `tasks/DEV_STATUS.md` contiene `READY_FOR_PROBE_REVIEW <path>` e non esiste ancora `reviews/PROBE_REVIEW_<nome>_*.md` | Determina la sede (Web/CLI) secondo la matrice `:149-153`, ricorda i divieti per sede (`reviewer.md:163-164`) e invoca il **reviewer** in modalità probe-review sul `<path>` indicato |

In coerenza, allineare la sezione "Workflow per output non-CAP" affinché lo stato `READY_FOR_PROBE_REVIEW` sia citato esplicitamente come trigger della probe-review.

---

## Empirico-CLI da verificare

Nessuno. I tre finding sono interamente verificabili per via statica (lettura di file versionati e grep su marker testuali); non richiedono accesso a DAPI né al filesystem locale del supervisore. La sede WEB è sufficiente per chiudere l'audit di questi finding.

---

## Classificazione per il supervisore

| # | Problema | Classificazione | Default |
|---|----------|-----------------|---------|
| N1 | `developer.md:152` rimanda a `CLAUDE.md:140-142` (criteri A/B) per la matrice di sede, che è invece a `CLAUDE.md:149-153` | MIGLIORA PROCESSO | → in attesa della tua decisione |
| N2 | `developer.md:133` e `CLAUDE.md:30` rimandano a `CLAUDE.md:118-122` (titolo+intro) per i 3 criteri OR, che sono a `CLAUDE.md:124-126` | MIGLIORA PROCESSO | → in attesa della tua decisione |
| N3 | La macchina a stati Orchestratore (`CLAUDE.md:27-33`) non ha una riga che intercetti `READY_FOR_PROBE_REVIEW` (prodotto da `developer.md:133,152,164,201`) | MIGLIORA PROCESSO | → in attesa della tua decisione |

Nessun finding è BUG REALE: nessuno altera comportamento del GA, ranking dei cromosomi, fitness o conversione signal-to-trade. Sono tre regressioni di processo introdotte dal rework Iter.2 (due cross-reference fuori sincrono + un gap di transizione nella tabella decisionale). Decisione su tutti e tre in attesa del supervisore.
