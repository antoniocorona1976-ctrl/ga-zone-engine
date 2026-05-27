# Handoff di sessione — chiusura CAP-DATA-01 (Parte 8) → apertura Parte 9 Appendici A-G

**Emesso da**: Orchestratore sessione corrente (post-PASS Review v2 CAP-DATA-01)
**Data**: 2026-05-27
**Destinatario**: Supervisore (AC) + Orchestratore della sessione successiva
**Scopo**: adempimento condizione 7 della checklist di chiusura sessione (riepilogo + prompt-template ready-to-paste)

---

## 1. Riepilogo formale ciclo CAP-DATA-01 (Parte 8)

### Stato finale

- **Verdetto**: PASS Review v2
- **HEAD origin/main**: aggiornato al commit di chiusura sessione (vedi log)
- **Documento metodologico v2 Parti I-VIII**: formalmente COMPLETO (Cap.1-44 tutti chiusi PASS Review)

### Hash chiave del ciclo CAP-DATA-01

| Fase | Commit | Descrizione |
|------|--------|-------------|
| Orchestratore apertura | `989304c` | ACTIVE_TASK aggiornato + tabella sessioni FIB recuperata via WebFetch (decisione (e.1)) + sezione "ATTENZIONE PER REVIEWER" (eccezione cross-index decisione (1)) + Note tecniche T2/T3 + decisioni (a)-(e) ratificate |
| Planner | `475cc70` | 4 sezioni Planner: mappatura eredità I-VII → §3.X, struttura capitoli Cap.37-44 (~10 pp), censimento M-promemoria (nessun M attivo pertinente), decisioni di scope residue (nessuna nuova Q-XX) |
| Developer v1 | `17240b4` | CAP-DATA-01 v1: documento Parte 8 (Cap.37-44, 237 righe) + REPORT v1 (237 righe, 6 sezioni format supervisore + 8 rollback) + CSV `data/sessions/fib_session_calendar.csv` (6 campi, 5 epoche E1-E5) + README + indice IN REVIEW + DEV_STATUS READY_FOR_REVIEW |
| Reviewer v1 | `89c5364` | CAP-DATA-01 v1 review: CONDITIONAL (16/16 AC formalmente OK; 3 finding non bloccanti: 1 BUG REALE non bloccante + 1 MIGLIORA PERFORMANCE + 1 NEUTRO; nessun bloccante; nessun nuovo M-promemoria) |
| Orchestratore checkpoint | `93dd93b` | Punto di controllo supervisore: 2 finding ratificati (#1 BUG REALE non bloccante obbligatorio + #2 MIGLIORA PERFORMANCE allargato a Opzione A 2a+2b — analisi tecnica esplicita su lacuna sample selection bar_synthetic in Cap.43); 1 finding ignorato per default (#3 NEUTRO); DEV_STATUS azzerato |
| Developer v2 | `015c47a` | CAP-DATA-01 v2 rework chirurgico: 3 Edit puntuali su `CAP_08_parte_8.md` (r190 aritmetica rolls + nuova clausola "Convenzione di selezione del campione" Cap.43 ~r192 + r201 L_avg calibrazione indipendente); REPORT_CAP_08.md +93 righe sezione "Iterazione 2 — risposta ai finding di Review v1"; nessuna riscrittura strutturale |
| Reviewer v2 | `6ba6186` | CAP-DATA-01 v2 review: PASS (3 fix tutti OK; 16/16 AC v1 ancora OK; nessuna regressione; 0 nuovi finding bloccanti; 0 nuovi M-promemoria; eccezione cross-index Cap.42 rispettata) |
| Orchestratore chiusura | _(questo commit)_ | Chiusura sessione: indice → PASS Review v2 con hash `6ba6186`; DEV_STATUS azzerato; handoff prodotto |

### Conteggio finding ciclo completo

| Categoria | v1 | v2 | Note |
|-----------|----|----|------|
| BUG REALE bloccante | 0 | 0 | — |
| BUG REALE non bloccante | 1 (#1 aritmetica rolls Cap.43 r190) | 0 | Chiuso via Edit chirurgico |
| MIGLIORA PERFORMANCE | 1 (#2 L_avg unit/calibration) → espanso dal supervisore a 2a+2b (bar_synthetic + L_avg) | 0 | Chiuso via Edit chirurgico (2 modifiche: nuova clausola Cap.43 r192 + sostituzione r201) |
| NEUTRO | 1 (#3 descrizione testuale Cap.38 r39) | 0 | Lasciato invariato per default CLAUDE.md ("NEUTRO non va mai a Developer") |
| **Totale ratificati supervisore** | **2** (#1 + #2 allargato) | **0** | — |

### M-promemoria — stato al chiudere CAP-DATA-01

- **M-2** (verifica empirica $L_{max}=30$s Telegram, Review v1 CAP-02): **OPEN** invariato → carryover ad **Appendice E (Parte 9 nel nuovo ordinamento)**. Cap.31.1 di Parte VII cita L_max qualitativamente; AC-GO-10 in Cap.36 lo include come AC pipeline funzionante. Verifica numerica empirica resta carryover, **deve chiudere in Appendice E della Parte 9** (sessione successiva).
- **M-16 condizionale** (Cox time-varying coefficients, Review v1 CAP-05 trigger Cap.25.8): **CLOSED-CAP-07** invariato. Regola operativa registrata in Cap.31.3 + metadato bundle `cox_time_varying_active` in Cap.35.1 elemento 6.
- **Nessun nuovo M-promemoria emesso** dal ciclo CAP-DATA-01 (né v1 né v2).

### Autocheck 7 condizioni di chiusura sessione

| # | Condizione | Stato | Evidenza |
|---|------------|-------|----------|
| 1 | Review PASS pubblicata e committata | ✅ | `6ba6186` su `origin/main` |
| 2 | DEV_STATUS azzerato e committato | ✅ | File vuoto a HEAD chiusura |
| 3 | Documento + report pubblicati | ✅ | `docs/methodology_v2/CAP_08_parte_8.md` v2 + `reports/REPORT_CAP_08.md` v2 (commit `015c47a`) |
| 4 | Indice aggiornato a PASS con hash review | ✅ | `00_indice.md:64` riporta `✅ PASS Review v2 (review commit 6ba6186 del 2026-05-27)` |
| 5 | ACTIVE_TASK lasciato storico su CAP-DATA-01 | ✅ | Resta puntato a CAP-DATA-01 v2 rework (sovrascrittura per nuova sessione) |
| 6 | CARRYOVER aggiornato | ✅ | Nessuna modifica necessaria (no nuovi M-promemoria, M-2 OPEN preservato, M-16 CLOSED-CAP-07 invariato) |
| 7 | **Riepilogo + prompt-template al supervisore** | ✅ | **Questo file (`tasks/SESSION_HANDOFF_CAP-DATA-01_to_PARTE-9_APPENDICI.md`)** |

**Tutte e 7 le condizioni soddisfatte. Sessione CAP-DATA-01 formalmente chiusa.**

---

## 2. Stato del documento metodologico v2 al chiudere CAP-DATA-01

- **Parti I-VIII** (Cap.1-44): tutte PASS Review, indice aggiornato.
- **Parte 9 = Appendici A-G** (era "Appendici operative" senza numero di Parte): **prossima sessione**. Contiene 7 appendici (struttura attuale in `00_indice.md` righe 75-82):
  - A: Specifiche PC e ambiente Python
  - B: Setup Claude Code e GitHub
  - C: API Directa
  - D: Storico Portara/CQG
  - E: **Telegram bot personale → qui chiude M-2 OPEN**
  - F: I 3 agenti Planner / Development / Review
  - G: Glossario

### Punto critico per la sessione successiva

La sessione Parte 9 chiude **M-2 OPEN** (verifica empirica $L_{max}=30$s Telegram). M-2 è in carryover da CAP-02 v1 attraverso 6 capitoli del doc v2 (CAP-02 → CAP-03 → CAP-04 → CAP-05 → CAP-06 → CAP-07 → CAP-DATA-01 → Parte 9). La chiusura empirica richiede setup operativo del Telegram bot (vedi Appendice E nel doc v2) + verifica numerica della latenza end-to-end emissione segnale → ricezione operatore mobile.

---

## 3. Prompt-template ready-to-paste per la sessione successiva (Parte 9 Appendici A-G)

Versione iniziale ratificata dall'Orchestratore sessione corrente al 2026-05-27. Copia/incolla verbatim per aprire la sessione nuova. **Decisioni di scope ancora aperte** che il supervisore deve ratificare al passo STEP iniziale della nuova sessione (vedi sotto).

```
Sei l'Orchestratore del progetto ga-zone-engine, sessione NUOVA per Parte 9 del documento metodologico v2 (Appendici operative A-G).

=========================================================
STATO INIZIALE DEL REPO
=========================================================
- CAP-DATA-01 (Parte 8) chiuso PASS Review v2 (review commit 6ba6186 del 2026-05-27; chiusura sessione commit <vedi log>; condizione 7 adempiuta in commit <vedi log> via file tasks/SESSION_HANDOFF_CAP-DATA-01_to_PARTE-9_APPENDICI.md).
- HEAD origin/main al momento dell'handoff: <vedi log>.
- ACTIVE_TASK.md ancora puntato storicamente a CAP-DATA-01 v2 rework (da sovrascrivere dopo che il supervisore ratifica le decisioni di scope aperte — vedi DEC-1, DEC-2 sotto).
- DEV_STATUS.md vuoto.
- Indice 00_indice.md riporta Parti I-VIII tutte PASS Review; Appendici A-G ancora senza numero di Parte definitivo nell'indice (riga 75 "## Appendici operative" da rinumerare a "## Parte 9 — Appendici operative" o equivalente, decisione di scope DEC-1).
- Documento metodologico v2 Parti I-VIII formalmente COMPLETO.
- M-2 OPEN (verifica empirica L_max=30s Telegram): DA CHIUDERE in Appendice E di questa sessione.
- M-16 CLOSED-CAP-07 (regola operativa Cap.31.3 + metadato bundle Cap.35.1) invariato.

=========================================================
DECISIONI DI SCOPE APERTE — DA RATIFICARE COME PRIMO ATTO
=========================================================
A differenza di CAP-DATA-01 (che ereditava 7 decisioni ratificate dall'Orchestratore della sessione precedente), per Parte 9 ci sono alcune decisioni di naming/struttura ancora da prendere. L'Orchestratore della nuova sessione DEVE chiedere al supervisore PRIMA di copiare task card in ACTIVE_TASK.md:

DEC-1: NUMERAZIONE PARTE 9
  L'indice 00_indice.md riga 75 ha attualmente intestazione "## Appendici operative (~6 pp)" senza prefisso "Parte 9 — ". Per coerenza con la decisione di CAP-07 / CAP-DATA-01 ("Appendici diventano Parte 9 nel nuovo ordinamento"), la sessione dovrebbe rinumerare l'indice in "## Parte 9 — Appendici operative (~6 pp)" o equivalente. Decidere il titolo definitivo della sezione.

DEC-2: STRUTTURA FILE METODOLOGICO
  Le 7 appendici (A-G) possono essere prodotte in:
    (i) Un singolo file `docs/methodology_v2/CAP_09_parte_9.md` con 7 sezioni interne (coerente con naming β2 di CAP-DATA-01)
    (ii) Sette file separati `docs/methodology_v2/APP_A.md`, ..., `docs/methodology_v2/APP_G.md` (coerente con la natura modulare delle appendici)
    (iii) Un file principale `docs/methodology_v2/CAP_09_parte_9.md` con 7 sotto-file di appoggio in `docs/methodology_v2/appendici/` per allegati lunghi
  Decidere quale opzione.

DEC-3: TASK ID
  Convenzione di task ID per la sessione. Possibilita':
    (i) CAP-09 (coerente con numerazione di Parte come CAP-01...CAP-07)
    (ii) CAP-APP-01 (esplicitando natura appendice)
    (iii) CAP-PARTE-9 (esplicitando posizione)
  Decidere quale convenzione.

DEC-4: CHIUSURA M-2 IN APPENDICE E
  M-2 OPEN (verifica empirica L_max=30s Telegram) deve chiudere in Appendice E. Decidere come la chiusura va documentata:
    (i) Solo sezione qualitativa in Appendice E + closure in CARRYOVER.md a fine sessione
    (ii) Sezione qualitativa in Appendice E + nuovo task gemello CAP-DATA-03 (specifica tecnica + protocollo di misura empirica) per attivita' di FASE-B
    (iii) Documentazione completa in Appendice E (setup bot + procedura di misura + accettazione del risultato empirico futuro come metadato del bundle frozen, simile a M-16 condizionale)
  Decidere quale.

DEC-5: SCOPE EFFETTIVO DELLE APPENDICI
  L'indice attuale prevede 7 appendici (A-G) per ~6 pp totali, cioe' ~0.85 pp per appendice. Verifica con il supervisore se questo target di lunghezza e ancora valido o se l'apertura della sessione richiede ampliamento (es. Appendice C su API Directa potrebbe richiedere piu' spazio data la complessita' MiFID II Darwin/DAPI/Visual Trader).

DEC-6: PUSH POLICY
  CAP-DATA-01 ha ereditato decisione (a) "push diretto a origin/main, no feature branch, no PR". Confermare che resta in vigore per Parte 9 (probabile SI, ma esplicitare).

L'Orchestratore della nuova sessione presenta DEC-1..DEC-6 al supervisore con una proposta default (mia raccomandazione qui sotto), poi attende ratifica. Dopo la ratifica, copia il task card in ACTIVE_TASK.md.

Raccomandazione iniziale dell'Orchestratore uscente:
- DEC-1: "Parte 9 — Appendici operative" (allineamento naming Parti precedenti)
- DEC-2: opzione (i) singolo file CAP_09_parte_9.md con 7 sezioni interne (coerente con β2; appendici sono brevi ~0.85 pp ciascuna, non richiedono file separati)
- DEC-3: CAP-09 (coerente con CAP-01...CAP-07)
- DEC-4: opzione (i) sezione qualitativa in Appendice E + closure in CARRYOVER.md a fine sessione (chiusura quanto piu' simile possibile al pattern CAP-04 → CAP-05 dove molti M-promemoria di CAP-04 sono stati chiusi senza task gemello)
- DEC-5: target ~6 pp confermato come minimo, ma flessibile (l'Appendice C su API Directa potrebbe richiedere fino a ~1.5 pp data la complessita' di MiFID II Darwin/DAPI/Visual Trader; il supervisore può ampliare)
- DEC-6: push diretto a origin/main confermato

=========================================================
FILE DA LEGGERE — IN QUESTO ORDINE PRECISO
=========================================================
  1. .claude/CLAUDE.md
     (regole orchestrazione, macchina a stati, 7 condizioni di chiusura, check post-Developer)
  2. MEMORY.md
     (memorie persistenti, inclusa project-developer-subagent-no-web)
  3. tasks/SESSION_HANDOFF_CAP-DATA-01_to_PARTE-9_APPENDICI.md
     (questo file — handoff completo, riepilogo CAP-DATA-01, decisioni di scope DEC-1..DEC-6)
  4. tasks/CARRYOVER.md
     (M-promemoria attivi — M-2 OPEN va chiuso in Appendice E)
  5. docs/methodology_v2/00_indice.md
     (stato Parti I-VIII + struttura appendici A-G attuale righe 75-82)

=========================================================
SEQUENZA OPERATIVA
=========================================================

──────────────────────────────────────────────────────────
STEP 1 — AUTOCHECK 7 CONDIZIONI CHIUSURA CAP-DATA-01
──────────────────────────────────────────────────────────
Verifica le 7 condizioni di chiusura sessione CAP-DATA-01 contro la tabella "stato finale" della sezione 1 di questo file handoff.

REGOLA STOP: se anche una condizione manca, segnala al supervisore prima di procedere a STEP 2.

──────────────────────────────────────────────────────────
STEP 2 — RATIFICA DEC-1..DEC-6 DAL SUPERVISORE
──────────────────────────────────────────────────────────
Presenta al supervisore la tabella DEC-1..DEC-6 sopra, con raccomandazione iniziale di default e proposte alternative. Attendi ratifica esplicita per ciascuna decisione.

DOPO la ratifica, scrivi i parametri ratificati in una sezione di header al task card e procedi a STEP 3.

──────────────────────────────────────────────────────────
STEP 3 — APERTURA TASK CARD + ACTIVE_TASK.md
──────────────────────────────────────────────────────────
Scrivi il task card per la sessione (es. tasks/CAP-09.md o equivalente secondo DEC-3 ratificato), poi copia in tasks/ACTIVE_TASK.md (sovrascrive storico CAP-DATA-01).

Il task card contiene:
- Naming + numerazione ratificati (DEC-1, DEC-2, DEC-3)
- Scope: 7 appendici A-G, eredita da Parti I-VIII
- Acceptance criteria per ciascuna appendice (es. A specifiche PC; B setup Claude Code + workflow agenti; ecc.)
- M-2 chiusura in Appendice E (DEC-4)
- Definition of Done coerente con CAP-DATA-01 (file + report + indice + CARRYOVER + commit + push)
- Out-of-scope (es. implementazione concreta API Directa = FASE-B; setup empirico Telegram bot = FASE-B se DEC-4 = i)
- Rollback criteria

──────────────────────────────────────────────────────────
STEP 4 — CHIAMATA PLANNER SUBAGENTE
──────────────────────────────────────────────────────────
Procedi come da .claude/CLAUDE.md: chiama subagente planner per la sessione Parte 9.

Note operative:
- Il Planner di Parte 9 ha eredita lieve (le appendici sono operative, non strettamente normative; eredita da Parti I-VIII soprattutto su terminologia, glossario, riferimenti a strumenti)
- Il Planner deve gestire la chiusura di M-2 OPEN secondo DEC-4 ratificato (es. quale livello di dettaglio empirico in Appendice E)
- Per Appendice C (API Directa) eventualmente serve recupero dati esterni (specifiche Directa Darwin/DAPI/Visual Trader). Verificare se il task richiede WebFetch dell'Orchestratore (memory `project-developer-subagent-no-web`)

──────────────────────────────────────────────────────────
STEP 5 — CHIAMATA DEVELOPER, CHECK POST-DEV, REVIEWER, CHIUSURA
──────────────────────────────────────────────────────────
Procedi come da .claude/CLAUDE.md (5a-5f). Standard.

In chiusura sessione Parte 9 (passo 5f):
- Aggiorna 00_indice.md: rinumerazione "Appendici operative" → "Parte 9 — Appendici operative" se DEC-1 = SI; aggiungi "✅ PASS Review v(N)" con hash review
- Aggiorna CARRYOVER.md: M-2 da OPEN → CLOSED-PARTE-9 (Appendice E) con riferimento al capitolo che lo ha chiuso
- M-16 CLOSED-CAP-07 invariato (resta storico)
- Produci nuovo file `tasks/SESSION_HANDOFF_PARTE-9_to_<next>.md` ... ma ATTENZIONE: Parte 9 dovrebbe essere l'ultima sessione del doc v2 corrente. Se il documento metodologico è formalmente concluso, il prossimo passo non è una nuova Parte ma il passaggio a FASE-B (acquisizione storico Portara/CQG e specifica CAP-DATA-02). Verifica con il supervisore quale handoff serve in chiusura Parte 9 (potrebbe essere "fine doc v2 + apertura FASE-B" invece di "apertura Parte 10").

=========================================================
FINE ISTRUZIONI SESSIONE PARTE 9
=========================================================
```

---

## 4. Note operative per l'Orchestratore della sessione successiva

### Decisione architetturale di consegna del documento

Parte 9 (Appendici A-G) è la **conclusione formale del documento metodologico v2 corrente**. Dopo Parte 9, il documento sarà "publication-ready" come Parti I-IX. Il prossimo passo del roadmap di progetto è il passaggio a **FASE-B (acquisizione storico Portara/CQG, specifica CAP-DATA-02 task operativo gemello)** + **FASE-D (implementazione preprocessor, walk-forward, training su AWS spot c5.4xlarge, sanity validation di Cap.43)**.

L'Orchestratore della sessione Parte 9, in chiusura, **non aprirà automaticamente una nuova sessione Parte 10** — non c'è una Parte 10 prevista. Verificherà con il supervisore quale handoff serve: fine doc v2 + apertura FASE-B (CAP-DATA-02), oppure altro.

### Eredità di lavoro per Appendice C (API Directa)

L'Appendice C (~0.85 pp nel target attuale di Parte 9) richiede dati specifici su:
- Qualificazione MiFID II del retail trader (vincoli Darwin / DAPI / Visual Trader)
- API endpoints e protocolli supportati da Directa
- Latenze tipiche di esecuzione retail
- Vincoli su strumenti derivati IDEM (FIB e miniFIB)

Questi dati non sono nel codebase e non sono stati raccolti dall'Orchestratore corrente. Se l'Orchestratore Parte 9 li ritiene rilevanti per la stesura dell'Appendice, dovrà recuperarli via WebFetch da `directa.it` o richiederli al supervisore (offline) prima di chiamare il Developer (memory `project-developer-subagent-no-web` e `project-orchestrator-input-is-authoritative`).

### Eredità di lavoro per Appendice E (chiusura M-2)

La chiusura empirica di M-2 ($L_{max}=30$s Telegram) richiede setup operativo del bot Telegram personale. Questo è **out-of-scope FASE-B** del roadmap (vedi Cap.31.1 AC-GO-10 di Parte VII).

Decisione DEC-4 sopra: l'Orchestratore Parte 9 propone al supervisore tre opzioni di chiusura M-2. Default raccomandato: opzione (i) sezione qualitativa in Appendice E + closure in CARRYOVER.md a fine sessione, coerente con il pattern di chiusura M-promemoria CAP-04 → CAP-05.

### Decisioni di scope ratificate in CAP-DATA-01 ancora applicabili a Parte 9

- **Push policy (a)**: push diretto a `origin/main`, no feature branch, no PR. Resta in vigore (DEC-6).
- **Eccezione cross-index Cap.42** (decisione (1)): rilevante SOLO per CAP-DATA-01 §3.6 / Cap.42. Per Parte 9 non si applica direttamente, ma se l'Appendice G (Glossario) dovesse includere termini cross-index (DCC/ADCC/cDCC), va rispettato il principio "dichiarazione normativa senza implementazione".
- **Realized GARCH (decisione (2))** e **`S_xidx` + quinta famiglia catalogo target (decisione (3))**: estensioni future, applicabili se citati nel Glossario.
- **Naming β2 (decisione (b)+(c))**: applicato come precedente. La decisione DEC-2 sopra estende il pattern a Parte 9.

### Decisioni nuove emerse da CAP-DATA-01 (non strettamente ratificabili, ma noted)

Nessuna decisione di carattere generale è emersa da CAP-DATA-01 che debba essere ratificata come ricetta permanente. Le 6 decisioni DEC-1..DEC-6 sono specifiche della sessione Parte 9.

---

## 5. Fine del ciclo CAP-DATA-01. Sessione corrente CHIUSA.

Tutte le 7 condizioni di chiusura adempiute. Documento metodologico v2 Parti I-VIII formalmente COMPLETE. Prossima sessione: Parte 9 Appendici A-G, con ratifica preliminare DEC-1..DEC-6 dal supervisore.
