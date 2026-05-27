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

Versione finale ratificata dal supervisore al 2026-05-27 (opzione C su DEC-1: Planner subagente con scope chiarito; opzione C su DEC-3: schema CSV 6 campi normativi). Copia/incolla verbatim per aprire la sessione nuova.

```
Sei l'Orchestratore del progetto ga-zone-engine, sessione NUOVA per CAP-DATA-01 (Parte 8 del documento metodologico v2: Convenzione dati storici e politica di rollover).

=========================================================
STATO INIZIALE DEL REPO
=========================================================
- CAP-07 v2 (Parte VII) chiuso PASS Review v2 (review commit b27c1e3 del 2026-05-27; chiusura sessione commit d6a7ee0; condizione 7 adempiuta in commit 353316d via file tasks/SESSION_HANDOFF_CAP-07_to_CAP-DATA-01.md).
- Task CAP-DATA-01 in coda: file tasks/CAP-DATA-01.md committato in effbe5f.
- HEAD origin/main al momento dell'handoff: vedi ultimo commit [ORCH] su origin/main.
- ACTIVE_TASK.md ancora puntato storicamente a CAP-07 v2 rework (da sovrascrivere come primo atto sostanziale dello STEP 3).
- DEV_STATUS.md vuoto.
- Indice 00_indice.md riporta Parte VII = PASS Review v2; Parte 8 NON ancora menzionata (verra' aggiunta a fine ciclo CAP-DATA-01 in chiusura sessione, come da decisione (d) ratificata); Appendice (Parte 9 nel nuovo ordinamento) ancora senza numero di Parte.
- Documento metodologico v2 Parti I-VII formalmente COMPLETO.
- M-2 OPEN preservato (verifica empirica L_max Telegram → carryover Appendice E in Parte 9; NON si chiude in CAP-DATA-01).
- M-16 CLOSED-CAP-07 (regola operativa in Cap.31.3 + metadato cox_time_varying_active in Cap.35.1).

=========================================================
DECISIONI RATIFICATE — NON RIAPRIRE
=========================================================
Le 7 decisioni operative + disallineamenti del file handoff sono GIA' RATIFICATE dal supervisore.
NON discutere, NON proporre alternative, NON chiedere conferma.

  (a) Push diretto a origin/main (no feature branch, no PR — deroga task card §5)
  (b)+(c) Naming β2:
        - file doc:    docs/methodology_v2/CAP_08_parte_8.md
                       (NON parte_08_convenzione_dati_storici.md, NON CAP_08_parte_VIII.md)
        - file report: reports/REPORT_CAP_08.md
                       (NON REPORT_CAP_DATA_01.md)
        - identifier interno: "Parte 8" arabo (NON "Parte VIII" romano)
  (d) Aggiornamento indice 00_indice.md a FINE CICLO (non subito)
  (e.1) Orchestratore recupera date FIB via WebFetch da borsaitaliana.it
        (fallback e.2 = richiesta offline al supervisore — vedi STEP 2)
  (1) Cross-index DCC/ADCC/cDCC: dichiarazione normativa nel doc v2 SENZA implementazione
  (2) Realized GARCH: estensione futura, non in Parte 8
  (3) S_xidx + quinta famiglia catalogo target: estensione futura, non in Parte 8

=========================================================
FILE DA LEGGERE — IN QUESTO ORDINE PRECISO
=========================================================
  1. .claude/CLAUDE.md
     (regole orchestrazione, macchina a stati, 7 condizioni di chiusura, check post-Developer)
  2. MEMORY.md
     (memorie persistenti, inclusa project-developer-subagent-no-web)
  3. tasks/SESSION_HANDOFF_CAP-07_to_CAP-DATA-01.md
     (handoff completo: decisioni (a)-(e), disallineamenti (1)-(3), note tecniche T1/T2/T3)
  4. tasks/CARRYOVER.md
     (M-promemoria attivi)
  5. tasks/CAP-DATA-01.md
     (task card normativo Parte 8 — da copiare in ACTIVE_TASK.md come primo atto sostanziale)
  6. docs/methodology_v2/00_indice.md
     (stato Parti I-VII, titoli definitivi per riferimenti incrociati)

=========================================================
SEQUENZA OPERATIVA
=========================================================

──────────────────────────────────────────────────────────
STEP 1 — AUTOCHECK 7 CONDIZIONI CHIUSURA CAP-07 v2
──────────────────────────────────────────────────────────
Verifica le 7 condizioni di chiusura sessione CAP-07 v2 contro la tabella "stato finale"
del file handoff §1.

REGOLA STOP:
  Se anche UNA SOLA condizione risulta non adempiuta:
    1. STOP IMMEDIATO — non procedere a STEP 2
    2. NON modificare alcun file
    3. NON eseguire alcun commit
    4. Stampa in chat al supervisore:
       - quale condizione e' mancante
       - cosa serve per chiuderla
       - attendi istruzioni
  Se tutte e 7 OK: prosegui a STEP 2.

──────────────────────────────────────────────────────────
STEP 2 — RECUPERO DATE SESSIONE FIB (decisione e.1)
──────────────────────────────────────────────────────────
Cerca via WebSearch + WebFetch su borsaitaliana.it (e fonti correlate IDEM) il
calendario storico delle ore di negoziazione del segmento FIB / IDEM.

OBIETTIVO:
  Ricostruire tabella timeline delle epoche di sessione con schema NORMATIVO del
  task card §3.5 (6 campi):
    epoch_id | start_date | end_date | session_open_local | session_close_local | timezone
  Coprire l'intero periodo dal 1995 a oggi (2026).
  Epoche attese (approssimative, da VERIFICARE, NON assumere):
    E1 = 1995-XX-XX → 20XX-XX-XX  (sessione singola, ~09:00-17:25 CET)
    E2 = introduzione estensione pomeridiana
    E3 = introduzione sessione serale
    E4 = estensione orario apertura (~08:00)
    En = attuale 09:00-22:00 CET
  Numero esatto di epoche e date precise SONO L'OUTPUT del recupero.

REGOLE OUTPUT:
  - annotare URL fonte e data di consultazione (formato ISO YYYY-MM-DD) per ogni dato
    raccolto, in struttura separata (vedi sotto), non dentro il CSV normativo
  - se piu' fonti danno date diverse, riportare ENTRAMBE con annotazione
  - non inventare date: se una transizione non e' verificabile, marcare "DATA DA VERIFICARE"
    nelle note adiacenti, NON dentro il CSV normativo
  - tutti i timestamp in CET (la pipeline gestira' CEST automaticamente, coerente con
    task card §3.5)

DOVE METTERE LE NOTE/AMBIGUITA':
  Il CSV `data/sessions/fib_session_calendar.csv` ha schema NORMATIVO a 6 campi (task
  card §3.5) e va prodotto dal Developer. L'Orchestratore raccoglie i dati e li passa
  via ACTIVE_TASK.md (vedi STEP 3). Eventuali fonti, ambiguita', URL, date consultazione
  vanno in un file separato `data/sessions/README.md` (NON normativo, prodotto dal
  Developer come parte del deliverable §3.5). Per ora l'Orchestratore include URL e
  note dentro ACTIVE_TASK.md nella sezione "Dati di input recuperati" (vedi STEP 3).

REGOLA FALLBACK:
  Se WebFetch fallisce (rate limit, sito down, contenuto non parsabile, dati incompleti
  per qualunque epoca):
    1. NON procedere a STEP 3 con dati parziali o inventati
    2. Stampa in chat al supervisore richiesta strutturata:
       "Fallback e.2 attivato — serve fornitura offline della tabella sessioni FIB
        con schema normativo (epoch_id, start_date, end_date, session_open_local,
        session_close_local, timezone) + fonti separate (URL + data consultazione).
        Periodo coperto: 1995-2026. Dati mancanti specifici: [elenco epoche non
        ricostruite]."
    3. Attendi risposta supervisore prima di procedere

──────────────────────────────────────────────────────────
STEP 3 — APERTURA ACTIVE_TASK.md
──────────────────────────────────────────────────────────
Copia tasks/CAP-DATA-01.md → tasks/ACTIVE_TASK.md (sovrascrive storico CAP-07).

INTEGRAZIONI OBBLIGATORIE in ACTIVE_TASK.md, in QUEST'ORDINE dall'alto:

  1. Subito sotto il titolo principale, sezione delimitata da marker HTML:

     <!-- ORCH-NOTE: NON RIMUOVERE — eccezione strutturale autorizzata dal supervisore -->
     ## ⚠️ ATTENZIONE PER REVIEWER — eccezione alla regola residui multi-indice

     [testo verbatim dalla Nota tecnica T1 del file handoff §4]

     <!-- ORCH-NOTE: fine eccezione -->

     Questa sezione impedisce un falso FAIL del Reviewer su §3.6 cross-index.
     Decisione (1) ratificata dal supervisore al 2026-05-27.

  2. Subito dopo, sezione "## Dati di input recuperati dall'Orchestratore":
     - tabella date FIB dallo STEP 2 con schema normativo (6 campi del task card §3.5)
     - sotto-tabella separata con (epoch_id, fonte_url, data_consultazione_ISO, note_ambiguita)
       per tracciare la provenienza dei dati
     - nota: "Questa tabella e' input per §3.5 del task card. Il Developer la usa
       come riferimento per produrre data/sessions/fib_session_calendar.csv (CSV
       normativo a 6 campi) e data/sessions/README.md (note non normative)."

  3. Sezione "## Note tecniche T2/T3":
     - "T2: _build_order.yaml NON esiste in questo repo (verificato Glob 2026-05-27).
        Riferimenti del task card §5 a _build_order.yaml vanno letti come riferimenti
        a docs/methodology_v2/00_indice.md."
     - "T3: directory data/sessions/ NON esiste (verificato Glob 2026-05-27). Va
        creata dal Developer come parte di §3.5."

COMMIT (dopo le integrazioni sopra):
  Messaggio: "[ORCH] CAP-DATA-01 apertura sessione: ACTIVE_TASK aggiornato + date FIB integrate + eccezione cross-index per Reviewer + decisioni (a)-(e) ratificate"
  Push diretto a origin/main.

──────────────────────────────────────────────────────────
STEP 4 — CHIAMATA PLANNER SUBAGENTE (scope chiarito — opzione C)
──────────────────────────────────────────────────────────
Modalita': PLANNER SUBAGENTE CON SCOPE RIDOTTO (decisione DEC-1 = C ratificata dal
supervisore al 2026-05-27).

RAZIONALE:
  Il task card CAP-DATA-01 ha gia' scope/AC/out-of-scope/DoD/rollback ratificati dal
  supervisore (5 funzioni Planner su 9 gia' coperte). Saltare il Planner sarebbe
  pericoloso: il Developer si troverebbe senza piano formale su 4 funzioni che il
  task card NON copre. Chiamare il Planner senza istruzioni rischierebbe doppione.
  La soluzione C e' chiamare il Planner CON istruzioni esplicite di non ridefinire
  scope/AC e di concentrarsi solo sulle 4 funzioni mancanti.

PROMPT AL PLANNER SUBAGENTE (testo da passare via tool Agent):

  "Hai ACTIVE_TASK.md gia' definito (scope, AC §3.1-§3.8, out-of-scope §4, DoD §5,
   rollback §6 tutti ratificati dal supervisore). NON ridefinirli, NON riformularli,
   NON discuterli. Tu AGGIUNGI le 4 cose mancanti nel formato Planner standard:

   (i) MAPPATURA EREDITA' I-VII → §3.X
       Per ciascun §3.1-§3.8 elenca quale Parte e quale Capitolo specifico del doc v2
       (Parti I-VII) va citato come riferimento incrociato. Leggi 00_indice.md per
       trovare il titolo definitivo di ciascuna Parte/Capitolo.
       Esempio atteso (NON copiare letteralmente — verifica i Capitoli reali):
         §3.1 (research = runtime)           → Parte I Cap.1, Parte II Cap.10
         §3.3 (purge/embargo OOS)            → Parte V Cap.25.1
         §3.4 (gap semantics fill virtuale)  → Parte II Cap.7.3 + Cap.10.4
         §3.4 (EGARCH, regime, feature)      → Parte III Cap.13-15
         §3.6 (DCC/ADCC cross-index)         → NON ESISTE nel doc v2 — dichiarare
                                               ESPLICITAMENTE come dichiarazione
                                               normativa PHASE-2 senza implementazione
                                               (decisione (1) ratificata)

   (ii) LISTA CAPITOLI DEL DOCUMENTO METODOLOGICO
        Proponi la struttura del file docs/methodology_v2/CAP_08_parte_8.md:
          - quanti capitoli (es. Cap.37, Cap.38, ...)
          - quale §3.X del task card va in quale capitolo del documento
          - lunghezza attesa per ciascun capitolo (in pagine)
        Convenzione storica: il primo capitolo della Parte VII era Cap.31, quindi la
        Parte 8 probabilmente parte da Cap.37 (verifica leggendo l'ultimo capitolo
        di Parte VII in 00_indice.md).

   (iii) CENSIMENTO M-PROMEMORIA PERTINENTI
         Leggi CARRYOVER.md. Identifica quali M-XX sono PERTINENTI a CAP-DATA-01.
         Verifica esplicita: M-2 (verifica empirica L_max Telegram) va in Appendice E
         (Parte 9), NON in Parte 8 — confermalo. Verifica gli altri M-XX uno a uno.
         Output: tabella M-ID | origine | pertinenza CAP-DATA-01 (SI/NO + motivazione).

   (iv) EVENTUALI DECISIONI DI SCOPE RESIDUE
        Se trovi ambiguita' NON risolte dalle decisioni gia' ratificate (a)-(e) e
        (1)-(3), apri Q-XX in tasks/QUESTIONS.md PRIMA di concludere. Probabile che
        non ce ne siano: il task card e' molto dettagliato. Ma verifica.

   Formato di output: aggiungi le 4 sezioni sopra in coda ad ACTIVE_TASK.md (NON
   sovrascrivere il task card). Le sezioni nuove vanno tutte sotto la sezione '##
   Note tecniche T2/T3' aggiunta dall'Orchestratore. Committa tu stesso le modifiche
   ad ACTIVE_TASK.md con messaggio '[PLANNER] CAP-DATA-01: mappatura eredita +
   struttura capitoli + censimento M-promemoria' e push.

   Vincoli operativi:
   - NON modificare la sezione 'ATTENZIONE PER REVIEWER' (marker HTML) ne' la
     sezione 'Dati di input recuperati dall'Orchestratore' ne' la sezione 'Note
     tecniche T2/T3' — sono input dell'Orchestratore.
   - NON modificare il task card originale CAP-DATA-01.md.
   - NON scrivere docs/methodology_v2/CAP_08_parte_8.md — quello e' compito del Developer.
   - NON aprire QUESTIONS senza prima verificare che la decisione non sia gia' nelle
     ratifiche (a)-(e) o (1)-(3)."

──────────────────────────────────────────────────────────
STEP 5 — CHIAMATA DEVELOPER, CHECK POST-DEV, REVIEWER, CHIUSURA
──────────────────────────────────────────────────────────
Procedi come da .claude/CLAUDE.md:

  (5a) Azzera tasks/DEV_STATUS.md (commit + push se non gia' vuoto).
  (5b) Chiama subagente DEVELOPER per leggere ACTIVE_TASK.md (gia' arricchito dal
       Planner) e produrre:
         - docs/methodology_v2/CAP_08_parte_8.md (documento metodologico Parte 8)
         - reports/REPORT_CAP_08.md (report supervisore secondo format del developer.md)
         - data/sessions/fib_session_calendar.csv (CSV normativo 6 campi, dati dalla
           tabella in ACTIVE_TASK.md preparata dall'Orchestratore)
         - data/sessions/README.md (note non normative su fonti/ambiguita')
         - aggiornamento 00_indice.md (Parte 8 = "IN REVIEW")
         - commit + push + DEV_STATUS = READY_FOR_REVIEW
  (5c) ESEGUI il check post-Developer (6 controlli di CLAUDE.md). Se anche uno
       fallisce, rilancia Developer con prompt mirato; NON chiamare Reviewer.
  (5d) Se 6/6 OK, chiama subagente REVIEWER. Il Reviewer leggera' la sezione
       "ATTENZIONE PER REVIEWER" in testa ad ACTIVE_TASK.md e applichera' l'eccezione
       cross-index limitata a §3.6 e sezioni collegate.
  (5e) Se Review emette CONDITIONAL o FAIL → punto di controllo supervisore
       (vedi CLAUDE.md "Punto di controllo supervisore"), ritorno a Developer per
       rework, ripeti (5c)-(5d).
  (5f) Se Review emette PASS:
       - Aggiorna 00_indice.md: Parte 8 = "PASS Review vN" con hash review
         (decisione (d): aggiornamento avviene QUI, non prima)
       - Aggiorna CARRYOVER.md SOLO se la Review ha emesso NUOVI M-promemoria per
         Parti successive (Parte 9 Appendici). M-2 OPEN preservato invariato (non
         si chiude in Parte 8). M-16 CLOSED-CAP-07 invariato.
       - Azzera DEV_STATUS.md
       - Verifica le 7 condizioni di chiusura sessione (CLAUDE.md)
       - Produci nuovo file tasks/SESSION_HANDOFF_CAP-DATA-01_to_PARTE-9_APPENDICI.md
         con riepilogo + prompt-template per la sessione successiva (Parte 9
         Appendici A-G, che chiudera' anche M-2)
       - Notifica al supervisore con riepilogo e ferma la sessione

=========================================================
FINE ISTRUZIONI SESSIONE CAP-DATA-01
=========================================================
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

### Note tecniche critiche per la sessione successiva

Tre punti operativi emersi dalla verifica del repo che l'Orchestratore della sessione successiva DEVE conoscere prima di copiare CAP-DATA-01 in ACTIVE_TASK.md.

#### Nota tecnica T1 — Reviewer subagente e regola "residui multi-indice = bloccante"

Il subagente `reviewer` (file `.claude/agents/reviewer.md`, riga 38) dichiara come regola assoluta:

> "Specializzazione FIB N=1: ci sono residui di multi-indice (DCC, ADCC, BEKK, N>=8, covarianza cross-index)? Se si, e' un problema bloccante."

Questa regola e' stata scritta quando il doc v2 era esplicitamente single-instrument FIB. Il task CAP-DATA-01 §3.6 introduce **deliberatamente** DCC/ADCC/cDCC come dichiarazione normativa PHASE-2 (decisione (1) ratificata dal supervisore al 2026-05-27).

**Senza intervento, il Reviewer v1 di CAP-DATA-01 classifichera' §3.6 come BUG REALE bloccante** (regola attiva), producendo un falso FAIL.

**Mitigazione obbligatoria**: l'Orchestratore della sessione successiva, quando copia tasks/CAP-DATA-01.md in tasks/ACTIVE_TASK.md, aggiunge in cima al file (subito sotto il titolo) una sezione esplicita:

```
## ATTENZIONE PER REVIEWER — eccezione alla regola "residui multi-indice = bloccante"

Il subagente `reviewer` (.claude/agents/reviewer.md riga 38) dichiara bloccante
ogni residuo multi-indice (DCC/ADCC/BEKK/N>=8/covarianza cross-index).

**In questo task, §3.6 (Convenzione cross-index PHASE-2) introduce DELIBERATAMENTE
DCC/ADCC/cDCC come dichiarazione normativa.** La decisione e' ratificata dal
supervisore (AC) in conversazione del 2026-05-27, decisione (1): "dichiarazione
normativa senza implementazione nel doc v2". Vedi commit f497022 e file
tasks/SESSION_HANDOFF_CAP-07_to_CAP-DATA-01.md.

**Il Reviewer NON deve classificare come bloccanti** le citazioni cross-index in
§3.6 e nelle sue sezioni collegate (fasizzazione PHASE-1/PHASE-2, S_xidx, quinta
famiglia catalogo target, Realized GARCH come esempio futuro). Sono normative
dichiarate, non residui da rimuovere.

**La regola "residui multi-indice = bloccante" resta valida** per qualunque
citazione cross-index al di FUORI di §3.6 (es. se il Developer inserisse DCC in
§3.4 preprocessor griglia o in altre sezioni non legate alla fasizzazione PHASE-2).
```

Alternativa scartata: modificare reviewer.md per aggiungere l'eccezione. Sconsigliata perche' modifica un file degli agenti che e' stato stabile per tutto il ciclo CAP-01..CAP-07, e perche' l'eccezione e' specifica di CAP-DATA-01.

#### Nota tecnica T2 — File `_build_order.yaml` citato nel task card §5

Il task card §5 (Definition of Done) cita:

> "_build_order.yaml (o equivalente) aggiornato: Parte 8 aggiunta in coda al corpo principale..."

Il file `_build_order.yaml` **non esiste** nel repo (verificato con Glob al 2026-05-27 commit f497022). Il file "equivalente" che il progetto ha sempre usato e' `docs/methodology_v2/00_indice.md`. La condizione 4 della checklist di chiusura sessione gia' richiede l'aggiornamento di 00_indice.md.

**Implicazione**: l'Orchestratore della sessione successiva istruisce il Developer (via ACTIVE_TASK) di interpretare il riferimento "_build_order.yaml (o equivalente)" come `docs/methodology_v2/00_indice.md`. Non creare un nuovo file `_build_order.yaml`.

#### Nota tecnica T3 — Directory `data/sessions/` non esistente

Il task card §3.5 (Timeline ufficiale delle sessioni FIB) richiede produzione di:

> "data/sessions/fib_session_calendar.csv con schema (epoch_id, start_date, end_date, session_open_local, session_close_local, timezone)"

La directory `data/sessions/` **non esiste** nel repo (verificato con Glob al 2026-05-27 commit f497022). Il Developer dovra' crearla via `mkdir -p data/sessions` (o equivalente PowerShell `New-Item -ItemType Directory -Force data/sessions`) prima di scrivere il CSV.

**Implicazione**: l'Orchestratore della sessione successiva nota questo gap nel commit di apertura ACTIVE_TASK ma NON crea la directory preventivamente (e' compito del Developer).

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
