# Handoff di sessione — chiusura CAP-07 v2 (Parte VII) → apertura CAP-DATA-01 (Parte 8)

**Emesso da**: Orchestratore sessione corrente (post-PASS Review v2 CAP-07)
**Data**: 2026-05-27
**Destinatario**: Supervisore (AC) + Orchestratore della sessione successiva
**Scopo**: adempimento condizione 7 della checklist di chiusura sessione (riepilogo + prompt-template ready-to-paste)

---

## 1. Riepilogo formale ciclo CAP-07 (Parte VII)

### Stato finale

- **Verdetto**: PASS Review v2
- **HEAD origin/main**: `d6a7ee0` (chiusura sessione CAP-07 v2)
- **Documento metodologico v2 Parti I-VII**: formalmente COMPLETO (Cap.1-36 tutti chiusi PASS Review)

### Hash chiave del ciclo CAP-07

| Fase | Commit | Descrizione |
|------|--------|-------------|
| Planner | `e19cd71` | CAP-07 task definito: Parte VII validazione OOS + DSR + PBO + Bootstrap + Frozen bundle + Gate go-live |
| Developer v1 | `330359c` | CAP-07 v1: Parte VII (Cap.31-36) + REPORT v1 + indice + DEV_STATUS READY_FOR_REVIEW |
| Reviewer v1 | `640ed61` | CAP-07 v1 review: CONDITIONAL (1 BUG REALE + 2 MIGLIORA PERFORMANCE + 2 NEUTRO) |
| Orchestratore | `a1e78b5` | Checkpoint supervisore: 3 finding ratificati (1 BUG REALE + 2 MIGLIORA PERFORMANCE) + 2 NEUTRO ignorati per scelta del supervisore + DEV_STATUS azzerato |
| Developer v2 | `9d46bd5` | CAP-07 v2 rework: 1 BUG REALE + 2 MIGLIORA PERF risolti via 4 Edit puntuali (r252, r320, r426, r441); AC-33-4 PARZIALE → OK; nessuna riscrittura strutturale |
| Reviewer v2 | `b27c1e3` | CAP-07 v2 review: PASS (64/64 AC OK; 32/32 eredità integre; 0 nuovi finding bloccanti; 0 nuovi M-promemoria) |
| Orchestratore chiusura | `d6a7ee0` | Chiusura sessione: indice → PASS Review v2; CARRYOVER M-16 → CLOSED-CAP-07; DEV_STATUS azzerato |

### Conteggio finding ciclo completo

| Categoria | v1 | v2 | Note |
|-----------|----|----|------|
| BUG REALE bloccante | 0 | 0 | — |
| BUG REALE non bloccante | 1 (CB-1 contraddizione Cap.33.4 vs Cap.34.4) | 0 | Chiuso |
| MIGLIORA PERFORMANCE | 2 (O-1 unità 15 USD/h × 2 occorrenze; O-2 errore bibliografico Notices AMS 2014) | 0 | Chiusi |
| NEUTRO | 2 (esempio PBO Cap.33.5 opaco; \|f_5\| ridondante) | 0 | Lasciati per scelta del supervisore |
| **Totale ratificati supervisore** | **3** (1 BUG + 2 MIGLIORA) | **0** | — |

### M-promemoria — stato al chiudere CAP-07

- **M-2** (verifica empirica $L_{max}=30$s Telegram, Review v1 CAP-02): **OPEN** invariato → carryover ad Appendice E (Parte 9 nel nuovo ordinamento). Cap.31.1 cita L_max qualitativamente; AC-GO-10 in Cap.36 lo include come AC pipeline funzionante. Verifica numerica empirica resta carryover.
- **M-16 condizionale** (Cox time-varying coefficients, Review v1 CAP-05 Cap.25.8 trigger): **CLOSED-CAP-07** con regola operativa. Cap.31.3 definisce condizione di attivazione (rapporto fold con `flag_schoenfeld_violation=True` > 0,5 → estensione a $\boldsymbol{\beta}_j(\tau)$ Therneau-Grambsch 2000 nel ciclo successivo di training); metadato bundle `cox_time_varying_active ∈ {True, False}` registrato in Cap.35.1 elemento 6.
- **Nessun nuovo M-promemoria emesso** dal ciclo CAP-07 (né v1 né v2).

### Autocheck 7 condizioni di chiusura sessione

| # | Condizione | Stato | Evidenza |
|---|------------|-------|----------|
| 1 | Review PASS pubblicata e committata | ✅ | `b27c1e3` su `origin/main` |
| 2 | DEV_STATUS azzerato e committato | ✅ | File vuoto su HEAD `d6a7ee0` |
| 3 | Documento + report pubblicati | ✅ | `docs/methodology_v2/CAP_07_parte_VII.md` v2 + `reports/REPORT_CAP_07.md` v2 (commit `9d46bd5`) |
| 4 | Indice aggiornato a PASS con hash review | ✅ | `00_indice.md:55` riporta `✅ PASS Review v2 (review commit b27c1e3 del 2026-05-27)` |
| 5 | ACTIVE_TASK lasciato storico su CAP-07 | ✅ | Resta puntato a CAP-07 v2 rework (sovrascrittura per nuova sessione) |
| 6 | CARRYOVER aggiornato | ✅ | M-16 condizionale → `CLOSED-CAP-07` con regola operativa; M-2 OPEN preservato |
| 7 | **Riepilogo + prompt-template al supervisore** | ✅ | **Questo file (`tasks/SESSION_HANDOFF_CAP-07_to_CAP-DATA-01.md`)** |

**Tutte e 7 le condizioni soddisfatte. Sessione CAP-07 v2 formalmente chiusa.**

---

## 2. Stato del documento metodologico v2 al chiudere CAP-07

- **Parti I-VII** (Cap.1-36): tutte PASS Review, indice aggiornato.
- **Parte VIII** (nuova, CAP-DATA-01): TASK in coda, vedi `tasks/CAP-DATA-01.md`. **Aggiunta non prevista** al momento della scrittura delle Parti I-VII; non richiede rinumerazione delle Parti precedenti.
- **Parte IX = Appendice** (era "Appendici operative" senza numero di Parte): NON ancora scritta. Conterrà A-G (PC + Anaconda, Claude Code + GitHub, API Directa, Storico Portara/CQG, Telegram bot personale → qui chiude M-2 OPEN, I 3 agenti, Glossario).

### Decisione architetturale di consegna del documento

CAP-DATA-01 (Parte VIII) **precede** la stesura delle Appendici (Parte IX). Razionale: la convenzione dati storici è normativa e ne ha bisogno qualsiasi implementazione successiva; l'Appendice D (Storico Portara/CQG) è la sua controparte operativa esterna, ma la specifica normativa va prima.

---

## 3. Prompt-template ready-to-paste per la sessione successiva (CAP-DATA-01)

Il supervisore può copiare e incollare il blocco qui sotto per aprire la sessione nuova. Le sezioni in `{{...}}` vanno valorizzate dal supervisore al momento dell'apertura.

```
Sei l'Orchestratore del progetto ga-zone-engine, sessione NUOVA per CAP-DATA-01 (Parte VIII del documento metodologico v2: Convenzione dati storici e politica di rollover).

Stato iniziale:
- CAP-07 v2 (Parte VII) chiuso PASS Review v2 (review commit b27c1e3 del 2026-05-27; chiusura sessione commit d6a7ee0). HEAD origin/main = d6a7ee0 al momento della chiusura.
- Task CAP-DATA-01 in coda: file tasks/CAP-DATA-01.md committato in effbe5f.
- ACTIVE_TASK.md ancora puntato storicamente a CAP-07 v2 rework (da sovrascrivere).
- DEV_STATUS.md vuoto.
- Indice 00_indice.md riporta Parte VII = PASS Review v2; Parte VIII non ancora menzionata; Appendice (Parte IX) ancora senza numero di Parte.
- Documento metodologico v2 Parti I-VII formalmente COMPLETO.
- M-2 OPEN preservato (verifica empirica L_max Telegram → carryover Appendice E in Parte IX).
- M-16 CLOSED-CAP-07 (regola operativa in Cap.31.3 + metadato cox_time_varying_active in Cap.35.1).

Leggi:
- .claude/CLAUDE.md (regole orchestrazione, macchina a stati, 7 condizioni di chiusura, check post-Developer)
- MEMORY.md (memorie persistenti del progetto)
- tasks/CARRYOVER.md (M-promemoria attivi)
- tasks/CAP-DATA-01.md (task card normativo della Parte VIII, da copiare in ACTIVE_TASK.md come primo atto)
- tasks/SESSION_HANDOFF_CAP-07_to_CAP-DATA-01.md (questo file, per autocheck condizioni chiusura sessione precedente)
- docs/methodology_v2/00_indice.md (stato Parti I-VII)

Come primo atto:
1. Verifica autoconsistenza delle 7 condizioni di chiusura sessione CAP-07 v2 (autocheck su file e su commit d6a7ee0). Tutte e 7 devono risultare adempiute. Se anche una sola fosse mancata, segnala al supervisore prima di procedere.
2. Decisioni architetturali da prendere PRIMA di copiare CAP-DATA-01 in ACTIVE_TASK.md (chiedi al supervisore se non sono autoevidenti dal task card):
   (a) **RATIFICATA dal supervisore in conversazione del 2026-05-27**: push diretto a `origin/main` (prassi storica del progetto, memory `project_push_policy`). Il task card §5 ("Commit firmato sul branch feature/parte-08-dati, PR aperta") viene DEROGATO su questo punto. Non aprire branch separato, non aprire PR. Il riferimento "Commit firmato" e' rispettato dal commit standard del Developer (no GPG signing aggiuntivo, prassi storica del repo).
   (b) Naming file output: il task card §5 dichiara "docs/methodology_v2/parte_08_convenzione_dati_storici.md" come file di output, mentre la convenzione storica del progetto e' "CAP_XX_parte_NN.md". Conferma se il task card e' normativo sul naming (parte_08_*.md) oppure se mantieni la convenzione storica (CAP_08_*.md o similare). **Pendente**.
   (c) Numero di Parte usato negli identificatori interni: le Parti precedenti usano "Parte I, II, ..., VII" (numeri romani); il task card usa "Parte 8" (numero arabo). Decidi se omogeneizzare a "Parte VIII" per coerenza o se rispettare la dicitura del task card. **Pendente**.
   (d) Conferma supervisore sulla nuova posizione "Appendici = Parte IX": il task card dichiara Successor = Parte 9 (Appendice). Verifica se l'indice deve essere aggiornato preventivamente o se aggiornamento posticipato a fine ciclo CAP-DATA-01. **Pendente**.
   (e) Il task card §3.5 richiede produzione del file data/sessions/fib_session_calendar.csv con date verificate da borsaitaliana.it (fonte web). Conferma con il supervisore: il Developer puo' accedere al web per la verifica delle date (richiede tool web), oppure il supervisore fornisce le date verificate offline? **Pendente**.
3. Una volta chiarite le decisioni 2.(a)-(e), copia tasks/CAP-DATA-01.md in tasks/ACTIVE_TASK.md (sovrascrivendo l'attuale storico CAP-07). Committa "[ORCH] CAP-DATA-01 apertura sessione: ACTIVE_TASK aggiornato + ratifica decisioni branch/naming/Appendice". Push.
4. Chiama subagente planner per leggere ACTIVE_TASK.md e produrre il piano operativo dettagliato della Parte VIII (8 sotto-decisioni §3.1-§3.8 + DoD + rollback) — il task card e' gia' molto specifico, ma il Planner aggiunge struttura: lista capitoli/sotto-capitoli, eredita' obbligatorie da Parti I-VII, M-promemoria pertinenti, AC verificabili, decisioni di scope. Alternativa: se ritieni che il task card sia gia' equivalente a un output Planner (DoD e rollback gia' definiti, acceptance criteria gia' dettagliati), chiama direttamente developer — chiedi al supervisore se preferisce questa via diretta.
5. Procedi da li' come da CLAUDE.md (check post-Developer obbligatorio prima di chiamare Reviewer, ecc.).

Eredita' diretta da CAP-07 (Parte VII) e Parti precedenti pertinenti a CAP-DATA-01:
- Invariante "research semantics = runtime semantics" (Cap.1 PI + Cap.10 PII replay bit-exact): CAP-DATA-01 §3.1 lo cita esplicitamente per escludere MIB cash come fonte training.
- Gap semantics e fill virtuale (Cap.7.3 PII, Cap.10.4 PII): CAP-DATA-01 §3.4 lo cita per escludere touch su bar_synthetic=True.
- Protocollo OOS, purge ed embargo (Cap.25.1 PV, Cap.25.3 PV M-5): CAP-DATA-01 §3.3 lo cita per non applicare il filtro pre-expiry a outer test.
- Layer di covarianza cross-index (NON presente nel doc v2 - solo single-instrument FIB): CAP-DATA-01 §3.6 lo cita ma dichiara fasizzazione PHASE-1/PHASE-2 con costi della PHASE-1 elencati. Attenzione: questo e' un'estensione esplicita dello scope rispetto al doc v2 finora scritto. Da verificare con il supervisore.
- Window EGARCH W=210.000, regime calmo/turbolento, catalogo 37 feature (Cap.13-15 PIII): CAP-DATA-01 §3.4 li cita per definire quali feature sono calcolabili su barre non sintetiche.
- Tabella congelati Cap.26.5 PV, bundle frozen Cap.35.1 PVII: CAP-DATA-01 §3.4 dichiara che il flag bar_synthetic entra nel feature schema persistito nel bundle frozen.
```

---

## 4. Note operative per l'Orchestratore della sessione successiva

### Disallineamenti potenziali fra task card CAP-DATA-01 e doc metodologico v2 esistente

Durante la lettura del task card, l'Orchestratore della sessione nuova noterà che CAP-DATA-01 fa riferimento a concetti che **non sono presenti** nel doc v2 Parti I-VII finora scritto:

1. **"Layer di covarianza cross-index" (DCC/ADCC/cDCC)**: il doc v2 attuale è esplicitamente single-instrument FIB (il preambolo dell'indice dichiara `con rimozione dei layer multi-indice (DCC/ADCC/BEKK, covarianza cross-index, N>=8)`). CAP-DATA-01 §3.6 introduce DCC/ADCC/cDCC per la PHASE-2. Questa è un'**estensione dello scope rispetto al doc v2 originario**, non un'eredità del doc v2 corrente. Va segnalata al supervisore: si tratta di una decisione strategica di estendere il doc v2 a includere materiale che era stato esplicitamente escluso, o di trattare la convenzione cross-index come puramente normativa senza implementazione in Parti successive del doc v2?

2. **"Realized GARCH measurement equation"**: il doc v2 attuale (Cap.13 PIII) usa EGARCH(1,1), non Realized GARCH. CAP-DATA-01 §3.4 cita "EGARCH, Realized GARCH measurement equation" come esempi di feature di volatilità. Da chiarire se Realized GARCH va aggiunto in una Parte successiva o se è solo esempio illustrativo nel task card.

3. **"S_xidx dello score strutturale" e "quinta famiglia del catalogo target proiezioni cross-index coerenti"**: questi termini sono coerenti con il documento `ENGINE_ALGO_INTEGRATO_HARD_LOCKED.pdf` (input richiesto al §2 del task card) ma NON sono presenti nel doc v2 Parti I-VII corrente. CAP-DATA-01 §3.6 li cita come "non calcolabili in PHASE-1". Verificare con il supervisore: sono concetti che entreranno in Parti successive del doc v2 (estensione) o sono retaggi del documento HARD_LOCKED che non sopravvivono nel doc v2 (errore nel task card)?

### Decisioni del supervisore — stato al 2026-05-27

| # | Decisione | Stato | Esito |
|---|-----------|-------|-------|
| (a) | Branch policy (feature branch + PR vs push diretto a main) | **RATIFICATA** | Push diretto a `origin/main`, prassi storica preservata. Task card §5 derogato su questo punto. |
| (b) | Naming file output (`parte_08_*.md` vs `CAP_08_*.md`) | Pendente | — |
| (c) | Numerazione interna (Parte 8 vs Parte VIII) | Pendente | — |
| (d) | Aggiornamento preventivo indice (Parte VIII + Parte IX Appendici) | Pendente | — |
| (e) | Accesso web Developer per date borsaitaliana.it | Pendente | — |

L'Orchestratore della sessione successiva deve chiudere le decisioni (b)-(e) con il supervisore prima di chiamare il Planner/Developer.

---

## 5. Fine del ciclo CAP-07. Sessione corrente CHIUSA.
