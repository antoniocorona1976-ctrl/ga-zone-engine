# HANDOFF — Adozione modello a 4 canali per business-spec (ga-zone-engine)

> Documento di coordinamento. Stato: **DRAFT prodotti, NON ancora depositati nel repo.**
> Ordine vincolante: **DRAFT → AUDIT → REVISIONE → DEPOSITO → loop spec.** Non depositare prima dell'audit.

## 1. Problema che risolve
Il primo tentativo di business-spec è fallito: gli agenti erano tarati sulla scrittura metodologica (prosa/contenuto), non sui requisiti (testabilità, tracciabilità, out-of-scope, contratti). Causa = taratura agenti + acceptance del task, **non** posizione del repo. Soluzione: **repo unico**, agenti `spec_*` induriti, e un modello a **4 canali** che instrada ogni requisito all'autorità più affidabile per stabilirne la correttezza.

## 2. Modello a 4 canali (sintesi per chi legge a freddo)
Ogni requisito → esattamente un canale:
- **CH1 fatto esterno** → check deterministico vs fonte vendorizzata (`data/reference/`). Autorità: l'artefatto.
- **CH2 coerenza interna** → lint statico. Autorità: regola meccanica.
- **CH3 claim testabile** → backtest sui dati. Autorità: il mercato.
- **CH4 intento** → gate AC, claim con rollback trigger. Autorità: AC, irriducibile.

CH1+CH2 automatici e deterministici; CH3 job sui dati; CH4 unico punto di gate umano.

## 3. Sequenza vincolante
1. **DRAFT** — fatto (questi file).
2. **AUDIT del metodo** — sessione **NUOVA** di Claude.ai (vedi `META_REVIEW_PROMPT.md`), con allegati i file vecchi + questi draft. Idealmente modello diverso. Verifica che il *metodo* regga **prima** di scolpirlo nel repo.
3. **REVISIONE** — incorpora i findings dell'audit nei draft.
4. **DEPOSITO** — Claude Code deposita i file revisionati (vedi §4). Commit tag `[SPEC-SETUP-4CH]`, push su `origin/main`.
5. **LOOP spec** — da qui il track gira: Planner apre il primo `SPEC-FUNZ-NN` in `tasks/ACTIVE_TASK.md`; Dev/Review nel loop hard-locked.

## 4. Inventario file e azione di deposito
| File draft (staging) | Path repo di destinazione | Azione |
|---|---|---|
| agents/spec_planner.md | `.claude/agents/spec_planner.md` | **SOSTITUISCE** esistente |
| agents/spec_developer.md | `.claude/agents/spec_developer.md` | **SOSTITUISCE** esistente |
| agents/spec_reviewer.md | `.claude/agents/spec_reviewer.md` | **SOSTITUISCE** esistente |
| docs_spec_funzionale/TEMPLATE_SPEC_FUNZ.md | `docs/spec_funzionale/TEMPLATE_SPEC_FUNZ.md` | **NUOVO** |
| docs_spec_funzionale/TRACCIABILITA.md | `docs/spec_funzionale/TRACCIABILITA.md` | **NUOVO** |
| specs_checks/SPEC_CHECK_STATICI.md | `specs/checks/SPEC_CHECK_STATICI.md` | **NUOVO** |
| specs_checks/SPEC_HARNESS_EMPIRICO.md | `specs/checks/SPEC_HARNESS_EMPIRICO.md` | **NUOVO** |
| META_REVIEW_PROMPT.md | (uso esterno; opzionale in `docs/spec_funzionale/`) | non-repo |
| HANDOFF_4CANALI.md | (questo; opzionale in `tasks/` o root) | riferimento |

I vecchi contenuti business-spec prodotti male vengono **riscritti** dal Developer nel loop (stessi path `docs/spec_funzionale/SPEC_FUNZ_NN.md`), **non** in questo deposito.

## 5. Da NON toccare (confine chirurgico)
- `docs/methodology_v2/` — **frozen**, sola lettura. È l'input dei CH1 "implementa §X".
- Prototipo/codice esistente — incapsulato via porta dati astratta, non sostituito.
- File di stato planner-owned (`STATO_CORRENTE.md`, `CARRYOVER.md`, `QUESTIONS.md`, `ACTIVE_TASK.md`) — non modificati da questo deposito.

## 6. Note di riconciliazione (VERIFICARE prima del deposito)
- I nuovi prompt assumono l'esistenza e il contenuto **corrente** di `tasks/METODO.md` (RM-1..RM-4) e `.claude/BASE_COMUNE.md`. Verifica che non li contraddicano (non li ho visti).
- **Cambio rispetto al modello iniziale**: niente file `ACTIVE_TASK_SPEC.md` separato. Si usa l'unico `tasks/ACTIVE_TASK.md` planner-owned → preserva "un solo task attivo" e rispetta il divieto (già presente nei prompt esistenti) per il Developer di scriverci.
- **Routing blocchi CH1/CH4**: il Developer NON scrive su `QUESTIONS.md` (planner-owned). Registra il blocco nel proprio REPORT + segnale "TASK BLOCCATO"; il Planner gestisce `QUESTIONS.md`. (Conseguenza diretta delle regole esistenti, non una nuova licenza.)
- Lint (CH2) e harness (CH3) sono **spec di infrastruttura** (Stream D), non ancora implementate. Finché non esistono, il Reviewer esegue i controlli **manualmente** (modalità degradata).

## 7. Decisioni aperte per AC
- Audit del metodo su **modello diverso** o stessa famiglia? (diverso = più decorrelato, più attrito.)
- Chi implementa lint/harness e quando: prima del primo `SPEC-FUNZ` o in parallelo con fallback manuale.
- `META_REVIEW_PROMPT.md` e questo handoff: versionati nel repo o tenuti fuori?

## 8. Scope del modello a 4 canali
Vale **solo** per l'attività di scrittura/definizione delle business-spec del modello GA. La metodologia ne è fuori (input frozen). Il codice (Stream B–E) eredita il *principio* — instrada all'autorità non-mente; gate umano solo dove il giudizio è irriducibile — ma **ri-tarato**: lì la correttezza è più verificabile (compila/tipi/test/walk-forward = DSR/PBO), quindi automazione maggiore e gate più stretto.
