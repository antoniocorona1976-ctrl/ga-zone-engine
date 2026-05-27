# Handoff di sessione — chiusura CAP-DATA-01 (Parte 8) → apertura CAP-DATA-02 (Parte 9, DAPI runtime)

**Emesso da**: Orchestratore sessione corrente (post-PASS Review v2 CAP-DATA-01, post-riallineamento ri-scoping CAP-DATA-02)
**Data**: 2026-05-27
**Destinatario**: Supervisore (AC) + Orchestratore della sessione successiva
**Scopo**: adempimento condizione 7 della checklist di chiusura sessione (riepilogo + prompt-template ready-to-paste), versione **corretta dopo il ri-scoping** del 2026-05-27 (vedi §2)

> **Nota**: questo file **sostituisce** `tasks/SESSION_HANDOFF_CAP-DATA-01_to_PARTE-9_APPENDICI_SUPERSEDED.md`, che era stato emesso prima della decisione di consulenza esterna del 2026-05-27 in cui il supervisore ha ridefinito Parte 9 da "Appendici A-G" a "CAP-DATA-02 DAPI runtime".

---

## §1. Stato finale CAP-DATA-01 (Parte 8)

### Verdetto

- **PASS Review v2**
- HEAD origin/main al chiudere CAP-DATA-01 (prima del riallineamento): `7b9bf68` [ORCH] CAP-DATA-01 v2 PASS Review v2 + chiusura sessione
- **Documento metodologico v2 Parti I-VIII formalmente COMPLETE** (Cap.1-44 tutti PASS Review)

### Hash chiave del ciclo CAP-DATA-01

| Fase | Commit | Descrizione |
|------|--------|-------------|
| Orchestratore apertura | `989304c` | ACTIVE_TASK + tabella sessioni FIB recuperata via WebFetch + eccezione cross-index Cap.42 + decisioni (a)-(e) ratificate |
| Planner | `475cc70` | Mappatura eredità I-VII → §3.X + struttura Cap.37-44 + censimento M-promemoria |
| Developer v1 | `17240b4` | Parte 8 v1 (237 righe) + REPORT v1 + CSV sessioni FIB (5 epoche E1-E5) + README + indice IN REVIEW |
| Reviewer v1 | `89c5364` | CONDITIONAL (16/16 AC OK; 3 finding non bloccanti: 1 BUG REALE non bloccante + 1 MIGLIORA PERFORMANCE + 1 NEUTRO) |
| Orchestratore checkpoint | `93dd93b` | Punto di controllo supervisore: 2 finding ratificati (Opzione A allargata 2a+2b sul finding #2) |
| Developer v2 | `015c47a` | Rework chirurgico 3 Edit puntuali (r190 aritmetica + Cap.43 bar_synthetic + r201 L_avg Politis-White) |
| Reviewer v2 | `6ba6186` | PASS (3 fix OK, no regressioni, 0 nuovi M-promemoria) |
| Orchestratore chiusura | `7b9bf68` | Indice Parte 8 → PASS Review v2 + DEV_STATUS azzerato + handoff (poi SUPERSEDED dal riallineamento) |

### Carryover M-promemoria al chiudere CAP-DATA-01

- **M-2 OPEN** (verifica empirica $L_{max}=30$s Telegram, Review v1 CAP-02): preservato invariato. Destinazione Appendice E nella struttura Appendici (vedi §2 per la riassegnazione di posizione: ora Parte 10 o oltre, non più Parte 9).
- **M-16 CLOSED-CAP-07**: invariato (regola operativa Cap.31.3 + metadato bundle Cap.35.1).
- **Nessun nuovo M-promemoria emesso** dal ciclo CAP-DATA-01.

---

## §2. Riordino ratificato dalla consulenza esterna del 2026-05-27

In sessione di consulenza esterna (post-PASS Review v2 CAP-DATA-01), il supervisore ha riordinato la roadmap del documento metodologico v2 corrente:

- **Parte 9** non è più "Appendici operative A-G" come da handoff originale (`SESSION_HANDOFF_CAP-DATA-01_to_PARTE-9_APPENDICI.md`, ora _SUPERSEDED).
- **Parte 9** è ora **`CAP-DATA-02 — Pipeline runtime FIB su Directa DAPI`** (nuovo scope: formalizzazione canale DAPI come provider RUNTIME esclusivo del FIB, definizione simboli, format, gestione errori, sessione operativa, vincoli di concorrenza, mappatura schema → bundle frozen Portara, risoluzione Q-A cash europei).
- **L'identificatore `CAP-DATA-02` viene riusato**: il vecchio scope di CAP-DATA-02 (specifica richiesta tecnica a Portara) è **abbandonato definitivamente**. Documento traccia: `tasks/CAP-DATA-02-PORTARA-OBSOLETED.md` (creato in questa sessione di riallineamento).
- **Le Appendici A-G** sono **rinviate a Parte 10 o oltre** (numerazione esatta da decidere al momento dell'apertura della loro sessione).

### Decisioni ratificate dalla consulenza esterna (vedi `tasks/ORCH_INSTRUCTIONS_CAP-DATA-02.md` per il dettaglio normativo)

**Dalla sessione di indagine cross-index del 2026-05-27** (3 commit `2661a2f` + `b8f7273` + `4d71207`):
- **(D-1)** NIENTE attivazione market data Directa a pagamento (Eurex 7,50€ + CME 15$ /mese).
- **(D-2)** NIENTE apertura PHASE-2 cross-index intraday senza training storico pluriennale.
- **(D-3)** APRIRE CAP-DATA-02 con scope "Pipeline RUNTIME FIB su Directa DAPI".
- **(D-4)** Exports già scaricati = campione di VALIDAZIONE, non training.
- **(D-5)** Decisione Q-A sui cash europei va presa DENTRO CAP-DATA-02, NON rinviata.
- **(D-6)** Regola permanente: niente probe DAPI con DGo / TradingView Directa aperto.
- **(D-7)** Apertura sessione CAP-DATA-02 con Planner subagente (scope ridotto).

**Dalla consulenza metodologica esterna**:
- **(C-1)** Naming β2 confermato: `docs/methodology_v2/CAP_09_parte_9.md`, `reports/REPORT_CAP_09.md`, identifier interno "Parte 9" arabo.
- **(C-2)** Push diretto a `origin/main`, no feature branch, no PR.
- **(C-3)** Aggiornamento `00_indice.md` a FINE CICLO.
- **(C-4)** Q-A ratificata = **Q-A-3**: cash europei usati SOLO come logging operativo e gating qualitativo per il supervisore umano, MAI come feature del GA, MAI nella state machine del segnale.
- **(C-5)** Scope IN del capitolo include: warm-up stati condizionali, tabella mappatura schema DAPI → bundle frozen Portara, audit log retention.
- **(C-6)** Scope OUT esplicito: feature engineering, implementazione codice operativo, continuità/storicizzazione/recupero gap (rinviati a CAP-DATA-03 / Parte 10).
- **(C-7)** Sei sezioni di GAP da chiudere obbligatoriamente nel capitolo: Gap-1 autenticazione canale, Gap-2 policy timezone, Gap-3 riavvio Darwin mezzanotte, Gap-4 audit log retention, Gap-5 test di regressione exports, Gap-6 comportamento soglia commissioni.

---

## §3. Prompt-template di apertura sessione

Il prompt-template completo per l'Orchestratore della nuova sessione CAP-DATA-02 **NON è incluso in questo handoff**. È stato prodotto separatamente dal supervisore e committato come file standalone:

> **`tasks/ORCH_INSTRUCTIONS_CAP-DATA-02.md`** (commit `fa037e7` su `origin/main` del 2026-05-27)

Il file contiene la sequenza operativa completa (STEP 1 autocheck CAP-DATA-01, STEP 2 nessun recupero web — deroga rispetto a CAP-DATA-01, STEP 3 apertura ACTIVE_TASK con task card normativo nel blocco `===`, STEP 4 chiamata Planner subagente con scope ridotto + prompt verbatim, STEP 5 Developer + check post-Dev + Reviewer + chiusura con prompt verbatim per ciascun subagente).

### Istruzione per il futuro Orchestratore

> **Apri una nuova sessione Claude Code. Incolla integralmente il contenuto di `tasks/ORCH_INSTRUCTIONS_CAP-DATA-02.md` come prompt iniziale.**

Il task card della sessione si trova in `tasks/CAP-DATA-02.md` (creato in questa sessione di riallineamento, STEP-R4). L'Orchestratore della nuova sessione lo copia in `tasks/ACTIVE_TASK.md` come primo atto sostanziale dello STEP 3.

---

## §4. Input ancora attesi dal supervisore PRIMA della nuova sessione

Per soddisfare il Done criterion #3 del task card CAP-DATA-02 ("Tutti gli input autoritativi della sezione INPUT verbatim nel capitolo") e il Gap-5 (test di regressione contro exports campione già archiviati), oltre al materiale già nel repo, il supervisore deve committare i seguenti file PRIMA dell'apertura della nuova sessione:

1. **`scripts/export_directa_history_parametric.py`**
   - Script Python di riferimento implementativo per il format dati canonico runtime (CSV BOM UTF-8 + manifest JSON, source ∈ {DIRECTA, AGG_FROM_D, AGG_FROM_60s}).
   - Atteso da AC #3 del task card e dalla scaletta §4 (Format dati canonico runtime).
   - **Azione richiesta al supervisore**: copia manuale da `C:\directa_history_parametric_export_overlay\` al repo path `scripts/export_directa_history_parametric.py`, poi `git add` + `git commit` + `git push origin main`.

2. **`data/runtime/exports_sample/`** (directory con 2-3 file CSV campione)
   - Esempi di export storico già archiviati, riferimento per il sanity check di non-regressione di Gap-5.
   - Atteso da AC #3 del task card e dal Gap-5 obbligatorio (test di regressione: la pipeline runtime eseguita oggi su simboli con storico ≤100gg deve produrre output identico a quello già archiviato).
   - **Azione richiesta al supervisore**: copia 2-3 file CSV esempio dal PC al repo path `data/runtime/exports_sample/`, poi `git add` + `git commit` + `git push origin main`.

3. **`docs/runtime/dapi_port_settings_schema.md`** — **già creato in questa sessione di riallineamento (STEP-R3)**. NON più atteso dal supervisore. File presente nel repo a partire dal commit di riallineamento.

---

## §5. Pre-flight checklist per il supervisore (prima di lanciare la nuova sessione)

Eseguire **in ordine** prima di aprire la sessione Claude Code per CAP-DATA-02:

- [ ] **`git pull`** — sincronizza il riallineamento del 2026-05-27 (questo handoff, task card CAP-DATA-02, PORTARA-OBSOLETED, schema port settings, vecchio handoff rinominato _SUPERSEDED)
- [ ] **verifica esistenza dei 5 file** (`ls -la` o equivalente):
  - `tasks/CAP-DATA-02.md` (task card normativo creato in STEP-R4)
  - `tasks/SESSION_HANDOFF_CAP-DATA-01_to_CAP-DATA-02.md` (questo file)
  - `tasks/ORCH_INSTRUCTIONS_CAP-DATA-02.md` (prompt-template, già committato dal supervisore in `fa037e7`)
  - `tasks/CAP-DATA-02-PORTARA-OBSOLETED.md` (trace storico ri-scoping, creato in STEP-R2)
  - `docs/runtime/dapi_port_settings_schema.md` (schema APIPortSettings, creato in STEP-R3)
- [ ] **copia `scripts/export_directa_history_parametric.py`** dal PC al repo + `git add` + `git commit` + `git push` (input addizionale §4 punto 1)
- [ ] **copia `data/runtime/exports_sample/`** con 2-3 file campione dal PC al repo + `git add` + `git commit` + `git push` (input addizionale §4 punto 2)
- [ ] **chiudi DGo / TradingView Directa** prima della sessione (decisione D-6 ratificata: "niente probe DAPI con DGo / TradingView Directa aperto")
- [ ] **apri nuova sessione Claude Code** (sessione fresca, principio "una sessione per capitolo" come da memory `feedback_sessione_per_capitolo`)
- [ ] **incolla integralmente `tasks/ORCH_INSTRUCTIONS_CAP-DATA-02.md`** come prompt iniziale della nuova sessione

Quando l'Orchestratore della nuova sessione partirà, eseguirà come primo atto (STEP 1 del prompt) la verifica autoconsistenza delle 7 condizioni di chiusura CAP-DATA-01 (già verificate in questa sessione corrente, ma il check è ridondante per safety) + verifica esistenza dei 3 input addizionali (`script Python`, `exports_sample/`, `dapi_port_settings_schema.md`). Se anche uno mancasse, la nuova sessione si fermerà e segnalerà al supervisore prima di procedere.

---

## §6. Fine sessione corrente

Tutte le 7 condizioni di chiusura CAP-DATA-01 adempiute. Riallineamento CAP-DATA-02 (ri-scoping vecchio Portara → nuovo DAPI runtime) completo. Documento metodologico v2 Parti I-VIII formalmente COMPLETE.

Prossima sessione: **CAP-DATA-02 / Parte 9** — Pipeline runtime FIB su Directa DAPI. Apertura a discrezione del supervisore dopo aver completato la pre-flight checklist §5.
