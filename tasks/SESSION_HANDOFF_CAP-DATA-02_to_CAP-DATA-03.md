# SESSION HANDOFF — CAP-DATA-02 → CAP-DATA-03

**Data chiusura sessione CAP-DATA-02:** 2026-05-28
**Stato:** Parte 9 chiusa **PASS Review v2** (review commit `86425a7`, documento commit `9bd35ba`)
**Prossima sessione:** CAP-DATA-03 / Parte 10 — Continuità tape, recupero gap, riconciliazione canonica, storicizzazione strutturata
**Supervisore:** AC

---

## 1. Riepilogo della sessione chiusa

### Ciclo Developer → Review

| Iterazione | Developer | Review | Verdetto |
|------------|-----------|--------|----------|
| v1 | commit `c4cd38f` (2026-05-27) | commit `baeab2c` (2026-05-28) | **FAIL** — 7 BUG REALI (B-1..B-7) + 5 MIGLIORA PERFORMANCE (NB-1..NB-5) + 3 NEUTRO (NB-6, O-1, O-2) |
| v2 | commit `9bd35ba` (2026-05-28) | commit `86425a7` (2026-05-28) | **PASS** — 11/11 finding chiusi OK; 2 osservazioni minori NEUTRO (OM-v2-1, OM-v2-2) lasciate inalterate |

### Punto di controllo supervisore (2026-05-28)

Esecuzione standard: tabella di classificazione presentata al supervisore con 15 finding totali (7 BUG REALI obbligatori + 5 MIGLIORA PERFORMANCE in attesa decisione + 3 NEUTRO ignorati). Decisioni del supervisore:

- 7 BUG REALI (B-1..B-7): obbligatori → Developer
- 4 MIGLIORA PERFORMANCE (NB-1, NB-2, NB-3, NB-4): tutti decisi **Opzione A** → Developer
- 1 MIGLIORA PERFORMANCE (NB-5): coperto per propagazione da B-2 (aggiunta colonna `bar_synthetic` al CSV runtime)
- 1 MIGLIORA PERFORMANCE (NB-6) + 2 NEUTRO (O-1, O-2): ignorati per default CLAUDE.md

Nota di sessione: durante la prima formulazione del punto di controllo NB-1 il supervisore ha rilevato un errore espositivo dell'Orchestratore (riferimento a FIB6I come ticker normativo del front-month invece di FIB6F al 2026-05-28); l'analisi è stata rifatta su FIB6F (FTSE MIB Index Future giugno 2026, scadenza 2026-06-19) e l'Opzione A è stata ratificata.

### Deliverable prodotti

- `docs/methodology_v2/CAP_09_parte_9.md` (431 righe, 12 capitoli Cap.45-Cap.56)
- `reports/REPORT_CAP_09.md` (146 righe, Iterazione 1 + Iterazione 2 rework)
- `reviews/REVIEW_CAP_09_review.md` (Review v1 FAIL)
- `reviews/REVIEW_CAP_09_v2_review.md` (Review v2 PASS)
- `tasks/ACTIVE_TASK.md` arricchito con sezione "Finding di Review da risolvere (rework v2)"
- `docs/methodology_v2/00_indice.md` aggiornato a "Parte 9 ... ✅ PASS Review v2"

### Decisioni ratificate del capitolo (riferimento Cap.56 tabella D-9)

- **D-9-NB2**: policy switch front-month al boot del giorno $t$ (terza venerdì del mese di scadenza), pipeline alle 08:00 CET sottoscrive direttamente next-month saltando finestra 08:00-09:00 del front in scadenza; marker `CONTRACT_SWITCH` in audit
- **D-9-NB3**: 6 eventi terminali distinti nel log audit (`SIGNAL_TARGET_1_HIT`, `SIGNAL_STOPPED`, `SIGNAL_INVALIDATED`, `SIGNAL_MISSED_TARGET`, `SIGNAL_EXPIRED`, `SIGNAL_REVOKED`); sotto-distinzione `pretrigger`/`posttrigger` nel payload JSON di `SIGNAL_MISSED_TARGET`
- **D-9-NB4**: $L_{warmup}=30$ giorni di trading IDEM congelato in Parte 9 con motivazione aritmetica ($N_{reg}=20$ + ~50% margine = 25.200 barre); non rifinibile dentro Parte 9, revisione richiede nuovo task Planner
- **Q-A-3 (B-5 raffinata)**: cash europei come logging operativo + gating qualitativo **POST-EMISSIONE** come annotazione del messaggio Telegram; il gating **non sopprime mai** l'emissione; replay bit-exact preservato
- **B-6**: rimosso fallback Portara automatico per downtime >100gg; sostituito con stato `RUNTIME_STALE_RESTART` + intervento supervisore; riconciliazione DAPI/Portara rinviata a CAP-DATA-03

---

## 2. Carryover M-promemoria al ciclo successivo

Lettura `tasks/CARRYOVER.md` aggiornata al 2026-05-28 post-chiusura sessione CAP-DATA-02.

| M-ID | Origine | Stato | Destinazione | Note |
|------|---------|-------|--------------|------|
| M-2 | Review v1 CAP-02 | **OPEN** | Appendice E (Telegram bot personale) | Verifica empirica latenza Telegram $L_{max}=30$s. **NON pertinente a CAP-DATA-03** (materia di Appendice E nel ciclo di consolidamento delle Appendici, fuori dal corpo Parti). Preservato invariato. |
| M-4..M-15, M-1v2 CAP-03, M-2v2 CAP-03 | varie Review CAP-01..CAP-04 | tutti CLOSED-CAP-04..CAP-06 | — | Tutti chiusi in cicli precedenti. Nessuna azione richiesta. |
| M-16 condizionale | Review v1 CAP-05 (Cap.25.8 trigger) | **CLOSED-CAP-07** con condizione operativa | Parte VII Cap.31.3 (gia' implementato) | Cox time-varying coefficients attivabili se test Schoenfeld viola sistematicamente >50% fold nel ciclo successivo di training. Metadato `cox_time_varying_active` nel bundle frozen Cap.35.1. NON pertinente a CAP-DATA-03. |

**Nessun nuovo M-promemoria** emesso dal ciclo Review v1 FAIL → v2 PASS di CAP-DATA-02. Le 2 osservazioni minori (OM-v2-1, OM-v2-2) di Review v2 sono cosmetiche, classificate NEUTRO senza azione richiesta.

---

## 3. Scope previsto per CAP-DATA-03 / Parte 10

I temi rinviati esplicitamente da CAP-DATA-02 (Cap.55 della Parte 9) costituiscono lo scope di partenza di CAP-DATA-03:

1. **Continuità del tape** attraverso i roll di front-month durante runtime. Cap.49 di Parte 9 norma lo schema barra-per-barra, ma la **sequenza temporale** di barre attraverso il `CONTRACT_SWITCH` di D-9-NB2 (es. sessioni FIB6F del 2026-06-18 seguite dalle sessioni FIB6I del 2026-06-19 e successive) richiede una formalizzazione di Parte 10: come la pipeline runtime e il bundle frozen ricevono il flusso continuo del tape virtuale ratio-adjusted di Parte 8 Cap.38 anche durante e dopo lo switch.
2. **Recupero automatico di gap** entro la finestra 100 giorni di `CANDLERANGE` per gap intermedi (riavvio mezzanotte di Cap.50 e downtime <100gg sono coperti dal warm-up di Cap.51; gap più estesi nella stessa finestra richiedono ri-pull strutturato non normato in Parte 9).
3. **Riconciliazione canonica giornaliera** fra il tape DAPI ingerito intra-sessione e il tape Portara di training (es. confronto EOD su volume aggregato, ultimo prezzo, eventuali discrepanze causate dal back-adjustment ratio-adjusted di Parte 8 Cap.38 applicato al tape Portara vs il tape DAPI unadjusted nativo).
4. **Storicizzazione strutturata** del tape DAPI runtime per eventuale uso come dataset di re-training futuro (oggi vietato da Parte 9 Cap.48 Scope OUT, da riconsiderare in Parte 10 con regole esplicite di conservazione, etichettatura e accesso).
5. **Riconciliazione DAPI/Portara per downtime >100gg** (collegato a B-6 di Parte 9: stato `RUNTIME_STALE_RESTART` rimanda esplicitamente a Parte 10 per la procedura di re-bootstrap quando il warm-up via `CANDLERANGE` non basta).
6. **Lookup completa codici mese Directa-IDEM** (oltre F=giugno, I=settembre già noti): da derivare via ANAG runtime nel ciclo operativo, normata in Parte 10 come tabella congelata progressiva.
7. **Abilitazione FDAX standard** sull'account `B6086` (Mini-DAX `EU.FDXMM6` e Micro-DAX `EU.FDXSM6` già abilitati per storico, FDAX standard non abilitato — vedi INDAGINE A.3): rinvio operativo, non blocca CAP-DATA-03.
8. **Vendor cross-index pluriennale** per PHASE-2 (decisione fuori scope CAP-DATA-02, anticipata in Cap.42 di Parte 8 come deroga normativa).

Suggerimento operativo per il Planner di CAP-DATA-03: valutare se aprire **verifiche empiriche preliminari V-1/V-2/V-3** prima di iniziare la stesura del capitolo (ad esempio: V-1 confronto byte-per-byte tape DAPI vs Portara su finestra recente sovrapposta; V-2 simulazione del `CONTRACT_SWITCH` nel walk-forward storico; V-3 test di reconcile EOD su finestra di sanity di Parte 8 Cap.43). La consulenza metodologica esterna o il supervisore decideranno se queste verifiche vanno fatte prima o durante il ciclo CAP-DATA-03.

---

## 4. Prompt-template ready-to-paste per la nuova sessione

```
Sei l'Orchestratore del progetto ga-zone-engine, sessione NUOVA per CAP-DATA-03
(Parte 10 del documento metodologico v2: continuita' tape, recupero gap,
riconciliazione canonica giornaliera, storicizzazione strutturata).

Stato iniziale del repo (autocheck obbligatorio come primo atto):
- CAP-DATA-02 (Parte 9) chiuso PASS Review v2 (review `86425a7`, doc `9bd35ba`).
- 00_indice.md riporta Parte 9 come PASS Review v2.
- DEV_STATUS.md vuoto.
- ACTIVE_TASK.md ancora puntato a CAP-DATA-02 (da sovrascrivere come primo atto
  sostanziale dopo l'autocheck e la chiamata Planner).
- M-2 OPEN preservato (verifica empirica L_max Telegram, carryover Appendice E).
- M-16 CLOSED-CAP-07 invariato.

File da leggere nell'ordine:
  1. .claude/CLAUDE.md
  2. MEMORY.md
  3. tasks/CARRYOVER.md (nessun nuovo M-promemoria da CAP-DATA-02)
  4. tasks/SESSION_HANDOFF_CAP-DATA-02_to_CAP-DATA-03.md (questo file)
  5. docs/methodology_v2/CAP_09_parte_9.md (Parte 9 PASS, eredita' obbligatorie,
     specialmente Cap.49 mappatura schema, Cap.51 warm-up, Cap.52 sessione,
     Cap.55 punti aperti rinviati)
  6. docs/methodology_v2/CAP_08_parte_8.md (Parte 8 PASS, eredita' di back-adjustment
     e politica di rollover)
  7. docs/methodology_v2/00_indice.md

Come primo atto, esegui autocheck delle 7 condizioni di chiusura della sessione
precedente (CAP-DATA-02) su file. Se anche una sola e' mancata, segnala al
supervisore prima di procedere. Poi chiama il subagente `planner` per CAP-DATA-03,
ereditando come scope di partenza i temi rinviati da Cap.55 di Parte 9 (8 punti
aperti listati nel SESSION_HANDOFF sezione 3) e valutando se aprire prima
verifiche empiriche preliminari V-1/V-2/V-3 (vedi suggerimento operativo nel
SESSION_HANDOFF).

Vincoli operativi ereditati:
- D-1: niente market data a pagamento.
- D-6: uso esclusivo canale DAPI, no DGo/TradingView concorrente durante probe
  DAPI (probe non sono materia di CAP-DATA-03 metodologico, ma se servisse
  ulteriore verifica empirica, regola D-6 va rispettata).
- C-2: push diretto a origin/main, no feature branch.
- C-3: aggiornamento 00_indice.md a fine ciclo (Parte 10 = PASS con hash review).
- Naming β2 atteso: `docs/methodology_v2/CAP_10_parte_10.md` (file documento),
  `reports/REPORT_CAP_10.md` (report supervisore), identifier interno "Parte 10"
  arabo (consulenza CAP-DATA-02 C-1 estesa per simmetria a Parte 10).
- Q-A-3 ratificata in Parte 9 NON va riaperta: cash europei restano gating
  qualitativo post-emissione fuori dal GA.
- Subagenti developer/planner/reviewer no-web: input autoritativi vanno
  preparati dall'Orchestratore in ACTIVE_TASK.md se serve recupero web.
```

---

## 5. Verifica autoconsistenza chiusura sessione CAP-DATA-02 (7 condizioni)

Per memoria, l'Orchestratore della sessione successiva eseguirà autocheck su queste 7 condizioni dello stato pubblicato su `origin/main` alla chiusura sessione corrente:

1. **Review PASS pubblicata**: `reviews/REVIEW_CAP_09_v2_review.md` commit `86425a7` su `origin/main` ✓
2. **DEV_STATUS azzerato**: `tasks/DEV_STATUS.md` vuoto (verifica con `wc -c`) ✓ (azzerato dall'Orchestratore in chiusura sessione)
3. **Documento + report pubblicati**: `docs/methodology_v2/CAP_09_parte_9.md` (431 righe) e `reports/REPORT_CAP_09.md` (146 righe) su `origin/main` ✓
4. **Indice aggiornato**: `docs/methodology_v2/00_indice.md` riga 75 riporta "Parte 9 ... ✅ PASS Review v2" con data 2026-05-28 e hash review `86425a7` ✓ (aggiornato dall'Orchestratore in chiusura sessione, decisione C-3)
5. **ACTIVE_TASK lasciato storico**: `tasks/ACTIVE_TASK.md` resta puntato a CAP-DATA-02 (Parte 9); sarà sovrascritto dall'Orchestratore della nuova sessione come primo atto sostanziale dopo il Planner ✓
6. **CARRYOVER aggiornato**: `tasks/CARRYOVER.md` invariato (nessun nuovo M-promemoria emesso da v1 o v2); M-2 OPEN e M-16 CLOSED-CAP-07 preservati ✓
7. **SESSION_HANDOFF + prompt-template + notifica supervisore**: questo file (`tasks/SESSION_HANDOFF_CAP-DATA-02_to_CAP-DATA-03.md`) committato e pushato; riepilogo + prompt-template notificati al supervisore in chiusura sessione ✓ (azione dell'Orchestratore in chiusura)
