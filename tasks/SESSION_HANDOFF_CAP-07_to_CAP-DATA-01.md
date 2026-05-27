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
Sei l'Orchestratore del progetto ga-zone-engine, sessione NUOVA per CAP-DATA-01 (Parte 8 del documento metodologico v2: Convenzione dati storici e politica di rollover).

Stato iniziale:
- CAP-07 v2 (Parte VII) chiuso PASS Review v2 (review commit b27c1e3 del 2026-05-27; chiusura sessione commit d6a7ee0; condizione 7 adempiuta in commit 353316d via file tasks/SESSION_HANDOFF_CAP-07_to_CAP-DATA-01.md).
- Task CAP-DATA-01 in coda: file tasks/CAP-DATA-01.md committato in effbe5f.
- ACTIVE_TASK.md ancora puntato storicamente a CAP-07 v2 rework (da sovrascrivere come primo atto sostanziale).
- DEV_STATUS.md vuoto.
- Indice 00_indice.md riporta Parte VII = PASS Review v2; Parte 8 non ancora menzionata (verra' aggiunta a fine ciclo CAP-DATA-01 in chiusura sessione, come da decisione (d) ratificata); Appendice (Parte 9 nel nuovo ordinamento) ancora senza numero di Parte.
- Documento metodologico v2 Parti I-VII formalmente COMPLETO.
- M-2 OPEN preservato (verifica empirica L_max Telegram → carryover Appendice E in Parte 9).
- M-16 CLOSED-CAP-07 (regola operativa in Cap.31.3 + metadato cox_time_varying_active in Cap.35.1).

Convenzioni di naming RATIFICATE dal supervisore (decisione β2 del 2026-05-27):
- File doc: docs/methodology_v2/CAP_08_parte_8.md (NON parte_08_convenzione_dati_storici.md del task card §5; NON CAP_08_parte_VIII.md romano)
- File report: reports/REPORT_CAP_08.md (NON REPORT_CAP_DATA_01.md del task card §5)
- Identifier interno: "Parte 8" (arabo, NON "Parte VIII" romano)
- Branch: push diretto a origin/main, no feature branch, no PR (deroga task card §5)

Leggi:
- .claude/CLAUDE.md (regole orchestrazione, macchina a stati, 7 condizioni di chiusura, check post-Developer)
- MEMORY.md (memorie persistenti del progetto)
- tasks/CARRYOVER.md (M-promemoria attivi)
- tasks/CAP-DATA-01.md (task card normativo della Parte VIII, da copiare in ACTIVE_TASK.md come primo atto)
- tasks/SESSION_HANDOFF_CAP-07_to_CAP-DATA-01.md (questo file, per autocheck condizioni chiusura sessione precedente)
- docs/methodology_v2/00_indice.md (stato Parti I-VII)

Come primo atto:
1. Verifica autoconsistenza delle 7 condizioni di chiusura sessione CAP-07 v2 (autocheck su file e su commit d6a7ee0). Tutte e 7 devono risultare adempiute. Se anche una sola fosse mancata, segnala al supervisore prima di procedere.
2. Decisioni architetturali RATIFICATE dal supervisore in conversazione del 2026-05-27 (NON ridiscutere, applicare direttamente):
   (a) **Branch policy**: push diretto a `origin/main` (prassi storica + memory `project_push_policy`). Il task card §5 ("Commit firmato sul branch feature/parte-08-dati, PR aperta") e' DEROGATO. Non aprire branch separato, non aprire PR.
   (b)+(c) **Naming file e numerazione interna (combinata)**: il nome file e' `docs/methodology_v2/CAP_08_parte_8.md` (NON `parte_08_convenzione_dati_storici.md` del task card §5; NON `CAP_08_parte_VIII.md` con numero romano). Identifier interno: "Parte 8" (arabo). Soluzione β2 della discussione del 2026-05-27: tutto arabo internamente, mantiene il prefisso `CAP_XX_` storico del progetto. Pattern equivalente nel report: `reports/REPORT_CAP_08.md` (NON `REPORT_CAP_DATA_01.md` del task card §5).
   (d) **Aggiornamento indice**: NON aggiornare preventivamente. Aggiornamento di `00_indice.md` posticipato a fine ciclo CAP-DATA-01 (in chiusura sessione, condizione 4 della checklist). Dichiarazione di Parte 8 e Parte 9 (Appendici) avverra' al primo aggiornamento utile (chiusura sessione CAP-08 con PASS). Coerente con la prassi storica delle Parti precedenti.
   (e) **Verifica date sessione FIB da borsaitaliana.it**: il subagente `developer` NON ha tools WebFetch/WebSearch. **L'Orchestratore** della sessione successiva recupera personalmente le date via WebFetch/WebSearch dalla fonte ufficiale `borsaitaliana.it`, le verifica, e le inserisce come dato di input verificato dentro `tasks/ACTIVE_TASK.md` PRIMA di chiamare il Developer. Il Developer poi cita la fonte e usa i dati gia' pronti (opzione e.1 della discussione del 2026-05-27).
3. **Recupera date sessione FIB via WebFetch / WebSearch** dalla fonte ufficiale borsaitaliana.it (decisione (e.1) ratificata: l'Orchestratore lo fa direttamente perche' il subagente developer non ha questi tools). Cercare la pagina "ore di negoziazione" / "calendario di borsa" del segmento IDEM/FIB e ricostruire la timeline storica delle epoche di sessione (E1=1995, E2=introduzione serale, ..., En=09:00-22:00 attuale). Annotare URL e data consultazione. Se WebFetch fallisce o se le date non sono recuperabili da fonte ufficiale, segnala al supervisore PRIMA di procedere e chiedi fornitura offline (fallback e.2).
4. Copia tasks/CAP-DATA-01.md in tasks/ACTIVE_TASK.md (sovrascrivendo l'attuale storico CAP-07). **Integra in ACTIVE_TASK.md la tabella date FIB recuperata al punto 3**, citando fonte URL e data verifica. Committa "[ORCH] CAP-DATA-01 apertura sessione: ACTIVE_TASK aggiornato + date FIB integrate da fonte borsaitaliana.it + decisioni (a)-(e) ratificate". Push diretto a origin/main.
5. Chiama subagente planner per leggere ACTIVE_TASK.md e produrre il piano operativo dettagliato della Parte 8 (8 sotto-decisioni §3.1-§3.8 + DoD + rollback) — il task card e' gia' molto specifico, ma il Planner aggiunge struttura: lista capitoli/sotto-capitoli, eredita' obbligatorie da Parti I-VII, M-promemoria pertinenti, AC verificabili, decisioni di scope. Alternativa: se ritieni che il task card sia gia' equivalente a un output Planner (DoD e rollback gia' definiti, acceptance criteria gia' dettagliati), chiama direttamente developer — chiedi al supervisore se preferisce questa via diretta.
6. Procedi da li' come da CLAUDE.md (check post-Developer obbligatorio prima di chiamare Reviewer, ecc.).

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

### Disallineamenti task card vs doc v2 — chiariti dal supervisore al 2026-05-27

I 3 disallineamenti potenziali fra CAP-DATA-01 e doc v2 Parti I-VII sono stati tutti chiariti. Riassunto delle decisioni:

1. **Layer di covarianza cross-index (DCC/ADCC/cDCC)** — task card §3.6:
   - Stato: il doc v2 Parti I-VII e' esplicitamente single-instrument FIB (preambolo `00_indice.md` dichiara rimozione layer multi-indice).
   - **Decisione del supervisore**: **dichiarazione normativa SENZA implementazione nel doc v2**. CAP-DATA-01 §3.6 contiene la convenzione cross-index come specifica futura (PHASE-2) ma il doc v2 non sara' esteso con Parti aggiuntive per implementarla. La dichiarazione resta come obbligazione metodologica futura, non come specifica operativa.
   - Implicazione per il Developer della sessione successiva: scrivere §3.6 in modo dichiarativo e non implementativo. Non introdurre formule DCC/ADCC nel doc v2. Citare la fasizzazione PHASE-1/PHASE-2 esplicitamente.

2. **Realized GARCH measurement equation** — task card §3.4 (esempi feature volatilita'):
   - Stato: doc v2 Cap.13 PIII usa solo EGARCH(1,1).
   - **Decisione del supervisore**: **estensione futura**. Realized GARCH va citato con cautela come esempio futuro, non come parte dell'impegno corrente del doc v2.
   - Implicazione per il Developer: nella stesura di §3.4 limitare gli esempi di feature di volatilita' a EGARCH (gia' nel doc v2) e marcare Realized GARCH come "es. eventuale estensione futura non corrente nel doc v2", o ometterlo dagli esempi se crea ambiguita'.

3. **`S_xidx`, "quinta famiglia del catalogo target proiezioni cross-index coerenti"** — task card §3.6:
   - Stato: termini coerenti con `ENGINE_ALGO_INTEGRATO_HARD_LOCKED.pdf` (input §2) ma non presenti nel doc v2 corrente.
   - **Decisione del supervisore**: **estensione futura**, coerente con (1). I termini possono essere citati in §3.6 come oggetti futuri non implementati nel doc v2 corrente.
   - Implicazione per il Developer: trattare `S_xidx` e "quinta famiglia catalogo target" come terminologia di riferimento PHASE-2, sempre dichiarando esplicitamente la non-implementazione nel doc v2 corrente.

Le tre decisioni sono coerenti fra loro: tutto cio' che e' cross-index nel task card resta a livello di **dichiarazione normativa**, mai a livello di **implementazione** nel doc v2. La fasizzazione PHASE-1 / PHASE-2 di §3.6 e' lo strumento documentale per rendere esplicita questa scelta.

### Decisioni del supervisore — stato finale al 2026-05-27 (tutte chiuse)

| # | Decisione | Esito |
|---|-----------|-------|
| (a) | Branch policy | **RATIFICATA**: push diretto a `origin/main` (deroga task card §5) |
| (b)+(c) | Naming + numerazione | **RATIFICATA β2**: file `CAP_08_parte_8.md`; identifier "Parte 8" (arabo); report `REPORT_CAP_08.md` |
| (d) | Aggiornamento indice | **RATIFICATA**: a fine ciclo CAP-DATA-01 (in chiusura sessione) |
| (e) | Accesso web per date FIB | **RATIFICATA e.1**: Orchestratore recupera via WebFetch/WebSearch, inserisce in ACTIVE_TASK.md prima di chiamare Developer |
| (1) | Cross-index DCC/ADCC/cDCC | **RATIFICATA**: dichiarazione normativa SENZA implementazione nel doc v2 (solo §3.6 di CAP-DATA-01) |
| (2) | Realized GARCH | **RATIFICATA**: estensione futura — citare con cautela in task card, no impegno nel doc v2 |
| (3) | `S_xidx` + quinta famiglia catalogo target | **RATIFICATA**: estensione futura — coerente con (1), citazione normativa senza implementazione |

L'Orchestratore della sessione successiva NON deve riaprire queste decisioni. Le applica direttamente.

### Implicazione operativa cruciale per la sessione successiva

Per via della decisione (e.1), il **primo atto sostanziale** dell'Orchestratore della sessione successiva — DOPO l'autocheck delle 7 condizioni di chiusura CAP-07 — deve essere:

1. **Recupero date sessione FIB** via WebFetch su `borsaitaliana.it` (cercare la pagina sulle "ore di negoziazione" / "calendario di borsa" del segmento IDEM/FIB). Ricostruire la timeline storica delle epoche di sessione:
   - epoca E1: probabile 1995 → introduzione sessione serale (data esatta da verificare)
   - epoca E2: introduzione sessione after-hours (da verificare)
   - epoca successiva: estensione all'attuale 09:00-22:00 CET (data switch da verificare)
2. **Annotare le fonti** consultate, gli URL e la data di consultazione nel campo "Sintesi vincoli operativi" o equivalente di ACTIVE_TASK.md.
3. Se WebFetch fallisce o se le date non sono recuperabili da fonte ufficiale, segnalare al supervisore PRIMA di procedere e chiedere fornitura offline (fallback e.2).

Solo DOPO aver completato questi passi (date verificate o fallback ratificato), l'Orchestratore della sessione successiva copia CAP-DATA-01 in ACTIVE_TASK.md (con le date integrate) e chiama il Planner (o Developer diretto se concordato).

---

## 5. Fine del ciclo CAP-07. Sessione corrente CHIUSA.
