# Re-Review FONDAMENTA-01 v3 — Verifica di chiusura N1/N2/N3 post-rework Iter.4 (v3)

**Task**: AUDIT-FONDAMENTA-01 Iter.4 (rework v3) — `tasks/ACTIVE_TASK.md` sez. "Finding di Review v2 approvati per rework (Iterazione 4 — rework v3)".
**Perimetro modificato dal rework v3 (commit `f89b69f`)**:
- P2 `.claude/CLAUDE.md` — 6 righe di contenuto (macchina a stati: riga trigger output non-CAP riformulata + nuova riga `READY_FOR_PROBE_REVIEW`; §"Workflow per output non-CAP" opzione B: trigger + clausola commit).
- P4 `.claude/agents/developer.md` — 4 righe di contenuto (intro Pre-consegna non-CAP + punto 5: rimandi per àncora).
- (`reports/REPORT_FONDAMENTA_01.md` aggiornato con sez. "Rework v3" — non normativo.)

**Stato git**: `origin`/working tree — solo `?? .claude/scheduled_tasks.lock` (file di lock estraneo, untracked). Nessuna modifica pendente sui file di perimetro. `git status --short` pulito sui 5 file P1..P5.
**Sede**: WEB (audit statico; nessun accesso DAPI/filesystem live).
**Riferimento v2**: `reviews/REVIEW_FONDAMENTA_01_v2_web.md` (verdetto CONDITIONAL, finding N1/N2/N3).
**Conflitto di interesse epistemico**: il rework v3 è esso stesso meta-ricorsivo (i finding erano rimandi di riga; gli edit spostano le righe). Audit condotto con Read/Grep reali e confronto del diff `f89b69f`, non su asserzioni del Developer.

---

## Verdetto

**PASS** (Sede: WEB)

I 3 finding N1/N2/N3 sono **tutti chiusi**. Il rework ha adottato la strada raccomandata in v2 (àncore di sezione al posto di numeri di riga) per i rimandi incriminati, eliminando alla radice il rischio di churn che aveva generato N1/N2. La nuova riga della macchina a stati intercetta `READY_FOR_PROBE_REVIEW` (chiude N3) e la sezione discorsiva è allineata. **Nessuna nuova regressione inter-prompt** introdotta dal rework v3: il diff è chirurgico (6+4 righe di contenuto), tocca solo `CLAUDE.md` e `developer.md`, e tutti i rimandi residui (pre-esistenti, fuori scope) risolvono ancora al contenuto corretto. Nessun blocco "Empirico-CLI da verificare".

Essendo PASS, non si produce tabella di finding per il supervisore.

---

## Metodo di verifica (RM-1 — nessuna asserzione senza prova)

Audit statico WEB. Read diretto delle righe di destinazione + Grep sui marker. Confronto col diff del commit `f89b69f`. Grep eseguiti:

- `Grep "READY_FOR_PROBE_REVIEW"` su `.claude/` → `CLAUDE.md:33` (riga macchina a stati), `CLAUDE.md:136` (trigger opzione B); `developer.md:133,152,164,201`. **Ora presente in `CLAUDE.md` (2 hit), assente in v2.**
- `Grep "CLAUDE\.md:\d|developer\.md:\d|reviewer\.md:\d|METODO\.md:\d|planner\.md:\d|118-122|140-142|149-153|124-126|114-144"` su `.claude/` → nessun rimando numerico verso `CLAUDE.md` nei punti N1/N2; restano solo rimandi a `tasks/METODO.md:28-33` e `reviewer.md:17,56,114,163-164` (pre-esistenti, fuori scope — vedi §"Nessuna nuova regressione").
- `Grep "Workflow per output non-CAP|decide anche la sede del reviewer|L'output è uno script/decoder che parsa|matrice di sede|criteri OR"` su `.claude/` → tutti i target d'àncora presenti col testo verbatim.
- `git show --stat f89b69f` + `git log -1 --format -- <file>` per ogni file di perimetro (verifica file toccati / non toccati).

Letture di conferma: `developer.md:131-165`; `CLAUDE.md:27-36`, `:119-163`; `reviewer.md:17`, `:114`, `:163-164`.

---

## N1 — Rimando alla matrice di sede Web/CLI → CHIUSO

**Cosa chiedeva il finding**: `developer.md:152` (pre-consegna non-CAP, punto 5) rimandava a `CLAUDE.md:140-142` (= criteri A/B, a/b/c), non alla matrice di sede (che era a `CLAUDE.md:149-153`). Fix richiesto: puntare alla matrice, preferibilmente con àncora di sezione + frase-ancora "l'Orchestratore decide anche la sede del reviewer".

**Evidenza post-rework** (`.claude/agents/developer.md:152`, verbatim):
> "La sede (Web/CLI) del Reviewer è decisa dall'Orchestratore secondo la matrice `tasks/METODO.md` §RM-4 / `.claude/CLAUDE.md` §\"Workflow per output non-CAP\" — sotto-blocco \"matrice di sede\" (i 3 bullet Web / CLI locale / Entrambe che seguono \"l'Orchestratore decide anche la sede del reviewer\")."

**Risoluzione dell'àncora**: la frase-ancora citata esiste verbatim in `.claude/CLAUDE.md:151`:
> "**Quando sceglie B (review formale leggera), l'Orchestratore decide anche la sede del reviewer** (Web o CLI locale) secondo la matrice in `tasks/METODO.md` RM-4 (riepilogo):"

seguita dai 3 bullet **Web** / **CLI locale** / **Entrambe** a `CLAUDE.md:153-155`. La citazione "i 3 bullet Web / CLI locale / Entrambe" corrisponde esattamente al contenuto. Il rimando numerico errato `:140-142` è stato eliminato (confermato dal diff e dal grep 0-match).

**Univocità dell'àncora**: "l'Orchestratore decide anche la sede del reviewer" compare **una sola volta** in `CLAUDE.md` (`Grep "decide anche la sede del reviewer"` → 1 hit, riga 151). Il sotto-blocco "matrice di sede" è identificato univocamente dalla frase-ancora. Àncora risolvibile, non ambigua.

**Esito: CHIUSO.**

---

## N2 — Rimando ai 3 criteri OR (definizione output non-CAP) → CHIUSO

**Cosa chiedeva il finding**: due rimandi (in `developer.md:133` e nella riga macchina a stati `CLAUDE.md:30`) puntavano a `CLAUDE.md:118-122` (titolo + intro), non ai 3 bullet OR (allora a `:124-126`). Fix richiesto: puntare ai 3 bullet OR in entrambi i punti, preferibilmente con àncora di sezione.

**Evidenza post-rework — punto (a), Developer** (`.claude/agents/developer.md:133`, verbatim):
> "...(definizione: cfr. `tasks/METODO.md` §RM-4 e `.claude/CLAUDE.md` §\"Workflow per output non-CAP\" — i 3 criteri OR: parsing payload di sistemi esterni, dichiarazione \"fatti verificati\" da citare in CAP successivi, asserzioni destinate a CARRYOVER)."

**Evidenza post-rework — punto (b), Orchestratore** (`.claude/CLAUDE.md:30`, riga macchina a stati, verbatim):
> "La sessione corrente sta per produrre/committare **output non-CAP** che soddisfa uno dei 3 criteri OR di RM-4 (vedi §\"Workflow per output non-CAP\", i 3 bullet — parsing payload esterno, dichiarazione \"fatti verificati\" per CAP successivi, asserzioni destinate a CARRYOVER) | **Prima del commit** instrada il flusso nel §\"Workflow per output non-CAP\": ..."

Entrambi i rimandi numerici `:118-122` (e il `:114-144` nella stessa riga) sono stati sostituiti dall'àncora §"Workflow per output non-CAP" + "i 3 bullet OR".

**Risoluzione dell'àncora**: i 3 criteri OR sono i bullet a `.claude/CLAUDE.md:125-127`:
> - "L'output è uno script/decoder che parsa payload di un sistema esterno (DAPI, Telegram, vendor dati)"
> - "L'output è un documento che dichiara \"fatti verificati\" da citare in CAP successivi (es. handoff, probe report, indagini)"
> - "L'output produce M-promemoria o asserzioni che entreranno in CARRYOVER"

Sono esattamente i 3 criteri OR descritti inline nei due rimandi. L'header di sezione "## Workflow per output non-CAP (probe, script, handoff) — RM-4" esiste a `CLAUDE.md:119`.

**Univocità dell'àncora**: `Grep "Workflow per output non-CAP"` su `CLAUDE.md` → l'header `##` compare una sola volta (riga 119); le altre occorrenze sono rimandi *a* quella sezione (riga 30 ×2, riga 147, riga 152 in developer.md). Non esistono due sezioni con titolo ambiguo: l'àncora di sezione risolve univocamente. Il sotto-blocco "i 3 bullet OR" è identificato dalla frase introduttiva "L'Orchestratore valuta se un output non-CAP rientra in RM-4 quando uno qualunque di questi è vero:" (`CLAUDE.md:123`) seguita dai 3 bullet.

**Esito: CHIUSO** (entrambi i punti a/b).

---

## N3 — Macchina a stati intercetta `READY_FOR_PROBE_REVIEW` → CHIUSO

**Cosa chiedeva il finding**: la tabella della macchina a stati gestiva solo `READY_FOR_REVIEW`; nessuna riga intercettava `READY_FOR_PROBE_REVIEW <path>` (prodotto da `developer.md:133,152,164,201`). Fix richiesto: aggiungere una riga che intercetti il marker (determina sede + divieti + invoca reviewer in probe-review), e allineare la §"Workflow per output non-CAP" citando `READY_FOR_PROBE_REVIEW` come trigger.

**Evidenza post-rework — riga macchina a stati** (`.claude/CLAUDE.md:33`, verbatim):
> "| `tasks/DEV_STATUS.md` contiene `READY_FOR_PROBE_REVIEW <path>` e non esiste ancora `reviews/PROBE_REVIEW_<nome>_*.md` per quel `<path>` | Determina la **sede** (Web/CLI) secondo la matrice del §\"Workflow per output non-CAP\" (sotto-blocco \"matrice di sede\", i 3 bullet Web / CLI locale / Entrambe), ricorda esplicitamente nel prompt i **divieti per sede** (`reviewer.md` — Web non dichiara \"verificato empiricamente\", CLI non fa probe massivi di zelo) e invoca il subagente **reviewer** in **modalità probe-review** sul `<path>` indicato. Nessun commit dell'output non-CAP finché la probe-review non emette PASS |"

La riga è ben formata (2 colonne `|...|...|`), collocata dopo la riga `READY_FOR_REVIEW` (`:32`) e prima della riga `CONDITIONAL/FAIL` (`:34`). Condizione (`READY_FOR_PROBE_REVIEW <path>` + assenza di `PROBE_REVIEW_<nome>_*.md`) e azione (sede + divieti + invocazione probe-review + no-commit-fino-a-PASS) sono entrambe presenti.

**Evidenza post-rework — sezione discorsiva allineata** (`.claude/CLAUDE.md:136`, opzione B, verbatim):
> "- Trigger: il Developer (o l'autore dell'output non-CAP) scrive `READY_FOR_PROBE_REVIEW <path>` in `tasks/DEV_STATUS.md` e si ferma senza committare l'output. La macchina a stati (riga \"`READY_FOR_PROBE_REVIEW <path>`\") intercetta questo segnale e instrada qui."

e `CLAUDE.md:138`: "L'output passa (e può essere committato) solo se il verdetto è PASS".

**Coerenza riga-tabella ↔ sezione discorsiva**: la riga (`:33`) dice "instrada alla probe-review, no commit fino a PASS"; la sezione (`:136-138`) dice "il marker è il trigger che la macchina a stati intercetta e instrada qui, output committabile solo a PASS". I due punti si rimandano reciprocamente in modo coerente, chiudendo il loop di handoff opzione B (Developer scrive il marker → Orchestratore lo intercetta nella tabella → invoca probe-review → commit solo a PASS).

**Grep di conferma**: `Grep "READY_FOR_PROBE_REVIEW"` su `CLAUDE.md` → **2 hit** (`:33` tabella, `:136` sezione). In v2 erano **0**. Gap chiuso.

**Esito: CHIUSO** (riga tabella + sezione discorsiva, coerenti).

---

## Nessuna nuova regressione (rischio meta-ricorsivo) — VERIFICATO

Il rischio è che il rework v3, modificando i prompt per chiudere N1/N2/N3, introduca a sua volta nuovi rimandi fuori sincrono o incoerenze inter-prompt (esattamente ciò che fece l'Iter.2 generando N1/N2/N3).

### Grep rimandi numerici residui/nuovi nei file modificati

`Grep "CLAUDE\.md:\d|developer\.md:\d|reviewer\.md:\d|METODO\.md:\d|planner\.md:\d|118-122|140-142|149-153|124-126|114-144"` su `.claude/`. Esito per occorrenza:

| Rimando trovato | File:linea | Verso | Risolve correttamente? | Introdotto da v3? |
|---|---|---|---|---|
| `tasks/METODO.md:28-33` | `CLAUDE.md:13` | blocco 4-righe RM-1 in METODO.md | Sì — `METODO.md:28-33` è il blocco `VERIFICA/PROVE/ALTERNATIVE ESCLUSE/NON ESCLUSE` (verificato in bootstrap) | No (pre-esistente) |
| `reviewer.md:163-164` | `CLAUDE.md:157` | divieti per sede | Sì — `reviewer.md:163-164` sono i 2 divieti Web/CLI (verificato verbatim) | No (pre-esistente) |
| `tasks/METODO.md:28-33` | `developer.md:139` | blocco 4-righe | Sì | No (pre-esistente, Iter.2) |
| `reviewer.md:114` | `developer.md:146` | probe-review check 1 | Sì — `reviewer.md:114` è il check RM-1 con blocco 4-righe (verificato verbatim) | No (pre-esistente, Iter.2) |
| `tasks/METODO.md:28-33` | `developer.md:188` | blocco 4-righe | Sì | No (pre-esistente, Iter.2) |
| `reviewer.md:17,56,114` | `developer.md:195` | criteri rigetto formato | Sì — `reviewer.md:17` e `:114` verificati verbatim (entrambi blocco 4-righe / criterio rigetto) | No (pre-esistente, Iter.2) |

**Nessun rimando numerico verso `CLAUDE.md` sopravvive** nei due file editati per i punti N1/N2 (grep 0-match su `CLAUDE.md:\d`, `118-122`, `140-142`, `149-153`, `124-126`, `114-144`). I rimandi N1/N2 sono ora per àncora di sezione → immuni allo spostamento di riga causato dall'inserimento della nuova riga `READY_FOR_PROBE_REVIEW` nella tabella (N3). Questa è la causa-radice di N1/N2 eliminata strutturalmente, non solo corretta puntualmente.

I rimandi numerici residui (verso `METODO.md` e `reviewer.md`) sono tutti **pre-esistenti** (commit ≤ Iter.2), **fuori dallo scope** N1/N2/N3, e **risolvono ancora correttamente** dopo gli edit v3 — perché v3 non ha toccato `reviewer.md` né `METODO.md` (vedi sotto), quindi le loro numerazioni di riga sono stabili.

### Univocità delle àncore introdotte

- "Workflow per output non-CAP" come header `##`: 1 sola occorrenza (`CLAUDE.md:119`). Univoca.
- "l'Orchestratore decide anche la sede del reviewer": 1 sola occorrenza (`CLAUDE.md:151`). Univoca.
- "matrice di sede": usata come etichetta del sotto-blocco; risolta tramite la frase-ancora sopra. Nessun secondo blocco omonimo che la renda ambigua.

Nessuna àncora introdotta è ambigua o non risolvibile.

### File NON toccati dal rework v3 — verificato via git

`git show --stat f89b69f` → solo 3 file: `.claude/CLAUDE.md` (6 righe), `.claude/agents/developer.md` (4 righe), `reports/REPORT_FONDAMENTA_01.md` (non normativo). `git log -1 --format -- <file>` conferma l'ultimo commit per file:

| File | Ultimo commit | Pre-v3? |
|---|---|---|
| `.claude/agents/reviewer.md` | `4d9c68b` | Sì (Iter.2) — **non toccato da v3**, come atteso |
| `tasks/METODO.md` | `2558750` | Sì — **non toccato da v3**, come atteso |
| `.claude/agents/planner.md` | `de2938d` | Sì — **non toccato da v3**, come atteso (nessun churn EOL committato) |
| `.claude/CLAUDE.md` | `f89b69f` | v3 |
| `.claude/agents/developer.md` | `f89b69f` | v3 |

Atteso pienamente rispettato: `reviewer.md`, `METODO.md`, `planner.md` sono ai loro commit pre-v3.

### Coerenza inter-prompt complessiva

Il diff `f89b69f` è chirurgico: 2 righe riformulate in `developer.md` (intro + punto 5, solo i rimandi), 1 riga riformulata + 1 riga nuova nella tabella `CLAUDE.md`, 2 righe nella §"Workflow" opzione B. Nessun edit collaterale, nessuna riga di contenuto sostanziale alterata oltre a quanto richiesto dai 3 finding. Le catene di rimando reciproco (macchina a stati `:33` ↔ workflow opzione B `:136` ↔ developer punto 5 `:152`) sono internamente coerenti. Nessuna nuova contraddizione introdotta.

**Esito controllo "nessuna nuova regressione": NESSUNA REGRESSIONE INTRODOTTA.**

---

## Osservazione minore (non bloccante, fuori scope — NESSUNA AZIONE RICHIESTA)

Il rework v3 ha de-numerizzato i rimandi N1/N2/N3 verso `CLAUDE.md` (àncore di sezione). Restano però rimandi **numerici** pre-esistenti verso `reviewer.md` e `METODO.md` (es. `CLAUDE.md:157 → reviewer.md:163-164`; vari `→ METODO.md:28-33` e `→ reviewer.md:17,56,114`). Oggi risolvono tutti correttamente. Sono fuori dallo scope di questo task (N1/N2/N3 riguardavano esclusivamente i rimandi verso `CLAUDE.md`) e non sono una regressione v3. Si segnala solo come futura opportunità di robustezza (eventuale de-numerizzazione anche di questi, in una sessione dedicata, se il supervisore lo riterrà): non incide sul comportamento del sistema né riapre il pattern d'errore canonico. **Nessun finding, nessuna patch richiesta.**

---

## Empirico-CLI da verificare

Nessuno. Tutti i controlli (risoluzione àncore, univocità, assenza rimandi stale, file toccati/non-toccati, coerenza riga-tabella ↔ sezione) sono verificabili per via statica su file versionati + git log. Nessun accesso a DAPI o al filesystem locale del supervisore richiesto. La sede WEB è sufficiente a chiudere l'audit.

---

## Conclusione

**Verdetto: PASS.** N1, N2, N3 chiusi con evidenza verbatim. Strada delle àncore di sezione adottata come raccomandato → causa-radice del churn eliminata. Nessuna nuova regressione inter-prompt. Nessun blocco Empirico-CLI lasciato aperto. Il ciclo AUDIT-FONDAMENTA-01 può chiudersi (chiusura adattata, non 7 condizioni CAP-XX; `00_indice.md` non va toccato — task non-CAP).
