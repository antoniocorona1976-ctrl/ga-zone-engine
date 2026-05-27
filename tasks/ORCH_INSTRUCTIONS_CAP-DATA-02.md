Sei l'Orchestratore del progetto ga-zone-engine, sessione NUOVA per CAP-DATA-02
(Parte 9 del documento metodologico v2: Pipeline runtime FIB su Directa DAPI).

=========================================================
STATO INIZIALE DEL REPO
=========================================================
- CAP-DATA-01 (Parte 8) chiuso PASS in sessione precedente. Indice metodologia
  aggiornato (Parte 8 = PASS). HEAD origin/main: 7b9bf68.
- Indagine informativa parallela cross-index Directa DAPI: conclusa (3 commit pushed,
  file tasks/INDAGINE_DIRECTA_CROSS_INDEX.md + due appendici empiriche). NON ha
  modificato la roadmap.
- ACTIVE_TASK.md ancora puntato a CAP-DATA-01 (da sovrascrivere come primo atto
  sostanziale dello STEP 3).
- DEV_STATUS.md vuoto.
- Indice 00_indice.md: Parti I-VIII tutte PASS. Parte 9 (CAP-DATA-02) NON ancora
  menzionata (verra' aggiunta a fine ciclo, decisione (d) ratificata da CAP-DATA-01).
- M-2 OPEN preservato (verifica empirica L_max Telegram, carryover Appendice E,
  Parte 10 o oltre — NON si chiude in CAP-DATA-02).
- M-16 CLOSED-CAP-07 invariato.

=========================================================
DECISIONI RATIFICATE — NON RIAPRIRE
=========================================================
Le decisioni del supervisore della sessione di indagine cross-index (2026-05-27) +
quelle ratificate dalla consulenza metodologica esterna sono GIA' CHIUSE.
NON discutere, NON proporre alternative, NON chiedere conferma.

Dalla sessione indagine (2026-05-27):
  (D-1) NIENTE attivazione market data Directa a pagamento (Eurex 7,50€ + CME 15$ /mese).
  (D-2) NIENTE apertura PHASE-2 cross-index intraday senza training storico pluriennale.
  (D-3) APRIRE CAP-DATA-02 con scope "Pipeline RUNTIME FIB su Directa DAPI".
  (D-4) Exports gia' scaricati = campione di VALIDAZIONE, non training.
  (D-5) Decisione Q-A sui cash europei va presa DENTRO CAP-DATA-02, NON rinviata.
  (D-6) Regola permanente: niente probe DAPI con DGo / TradingView Directa aperto.
  (D-7) Apertura sessione CAP-DATA-02 con Planner subagente (scope ridotto, vedi STEP 4).

Dalla consulenza metodologica esterna:
  (C-1) Naming β2 confermato: docs/methodology_v2/CAP_09_parte_9.md,
        reports/REPORT_CAP_09.md, identifier interno "Parte 9" arabo.
  (C-2) Push diretto a origin/main, no feature branch, no PR.
  (C-3) Aggiornamento 00_indice.md a FINE CICLO (coerente con (d) CAP-DATA-01).
  (C-4) Decisione Q-A ratificata = Q-A-3: cash europei usati SOLO come logging
        operativo e gating qualitativo per il supervisore umano, MAI come feature
        del GA, MAI nella state machine del segnale. Perimetro va scritto nel
        capitolo, non lasciato all'implementazione futura.
  (C-5) Scope IN del capitolo include: warm-up stati condizionali, tabella
        mappatura schema DAPI -> bundle frozen Portara, audit log retention.
  (C-6) Scope OUT esplicito del capitolo include: feature engineering,
        implementazione codice operativo, continuita'/storicizzazione/recupero
        gap (rinviati a CAP-DATA-03 / Parte 10).
  (C-7) Sei sezioni di GAP da chiudere obbligatoriamente nel capitolo:
        Gap-1 autenticazione canale (locale-only)
        Gap-2 policy timezone Darwin (CET/CEST, coerenza con CAP-DATA-01 §3.5)
        Gap-3 comportamento al riavvio Darwin di mezzanotte
        Gap-4 audit log retention policy
        Gap-5 test di regressione contro exports campione gia' archiviati
        Gap-6 comportamento se commissioni mensili scendono sotto 200 €

=========================================================
FILE DA LEGGERE — IN QUEST'ORDINE PRECISO
=========================================================
  1. .claude/CLAUDE.md
     (regole orchestrazione, macchina a stati, 7 condizioni di chiusura,
     check post-Developer)
  2. MEMORY.md
     (memorie persistenti, inclusa project-developer-subagent-no-web e regola
     "no DAPI probe con DGo aperto")
  3. tasks/CARRYOVER.md
     (M-promemoria attivi: M-2 OPEN, M-16 CLOSED-CAP-07)
  4. tasks/INDAGINE_DIRECTA_CROSS_INDEX.md
     (input autoritativo principale: catalogo simboli verificati, codici errore
     1004/1007/1030, limiti 100gg, rate-limit, conflitto DGo/TradingView,
     schemi risposta DAPI, costi)
  5. docs/methodology_v2/CAP_08_parte_8.md
     (Parte 8 chiusa PASS: ereditare convenzioni dati storici, gap semantics,
     timeline sessione FIB, regola bar_synthetic)
  6. docs/methodology_v2/00_indice.md
     (stato Parti I-VIII, titoli definitivi per riferimenti incrociati,
     ultimo capitolo Parte VIII per numerazione interna)

=========================================================
SEQUENZA OPERATIVA
=========================================================

──────────────────────────────────────────────────────────
STEP 1 — AUTOCHECK CHIUSURA CAP-DATA-01
──────────────────────────────────────────────────────────
Verifica che CAP-DATA-01 (Parte 8) sia formalmente chiuso PASS:
  - docs/methodology_v2/CAP_08_parte_8.md presente
  - reports/REPORT_CAP_08.md presente
  - 00_indice.md riporta Parte 8 = PASS Review
  - data/sessions/fib_session_calendar.csv presente con schema 6 campi
  - DEV_STATUS.md vuoto

REGOLA STOP:
  Se anche UNA condizione manca:
    1. STOP IMMEDIATO — non procedere a STEP 2
    2. NON modificare alcun file
    3. NON eseguire commit
    4. Stampa al supervisore quale condizione manca e attendi istruzioni

──────────────────────────────────────────────────────────
STEP 2 — NESSUN RECUPERO WEB (deroga rispetto a CAP-DATA-01)
──────────────────────────────────────────────────────────
A differenza di CAP-DATA-01, CAP-DATA-02 NON richiede recupero dati da fonti esterne.
Tutti gli input autoritativi sono GIA' nel repo (tasks/INDAGINE_DIRECTA_CROSS_INDEX.md
+ appendici empiriche probe del 2026-05-27).

NON eseguire WebFetch / WebSearch in questa sessione. I subagenti
project-developer-subagent-no-web e altri sub-agenti gia' non hanno web; anche
l'Orchestratore in questa sessione NON deve usare web. Tutto deriva da:
  - i file di INDAGINE gia' committati
  - il PDF hard-locked se necessario
  - la spec CAP-DATA-01 / Parte 8 gia' approvata

Se durante il ciclo un sub-agente segnalasse necessita' di un fatto esterno
NON presente nei file sopra: STOP, segnala al supervisore, NON inventare.

──────────────────────────────────────────────────────────
STEP 3 — APERTURA ACTIVE_TASK.md
──────────────────────────────────────────────────────────
Crea tasks/ACTIVE_TASK.md (sovrascrive CAP-DATA-01) con il seguente contenuto.

CONTENUTO ESATTO DA SCRIVERE (tra le linee ===):

===
# ACTIVE TASK — CAP-DATA-02 (Parte 9)

**Titolo:** Pipeline runtime FIB su Directa DAPI
**Status:** ACTIVE
**Posizione nel doc v2:** Parte 9, immediatamente prima di eventuali Parti
successive e dell'Appendice
**Predecessor:** Parte 8 (CAP-DATA-01) — PASS Review
**Owner deliverable:** Developer subagente
**Supervisore:** AC

## Goal
Formalizzare in metodologia v2 il canale Directa DAPI come provider RUNTIME
esclusivo del FIB, definendo simboli, format, gestione errori, sessione operativa,
vincoli di concorrenza e mappatura schema verso il bundle frozen di training
Portara, con risoluzione vincolante della Q-A sul gating cash europei.

## Scope IN
1. Formalizzazione canale DAPI come provider RUNTIME del FIB (Portara resta per
   training, eredita' da CAP-DATA-01).
2. Catalogo simboli Directa rilevanti per CAP-DATA-02:
   - IDEM FIB (FIB6F, FIB6I, MINI6F, MINI6I, MINI6C)
   - indici cash europei (DITAS, DGER, DSTX50, DFRA)
3. Architettura canale: gateway 127.0.0.1, porte 10001 (RT) e 10003 (storico),
   banner Darwin, file APIPortSettings.txt, socket persistente, rate-limit.
4. Format dati canonico (CSV BOM UTF-8 + manifest JSON, riferimento allo script
   esistente scripts/export_directa_history_parametric.py).
5. Codici errore DAPI (1004 / 1007 / 1030) e fallback aggregazione
   (AGG_FROM_60s, AGG_FROM_D).
6. Vincolo "uso esclusivo del canale" (conflitto con DGo/TradingView Directa).
7. Sessione operativa runtime FIB 08:00-22:00 CET, coerente con timeline
   epoche di CAP-DATA-01 §3.5.
8. Tabella di mappatura schema DAPI -> bundle frozen Portara (invariante
   research = runtime applicato all'adapter).
9. Warm-up degli stati condizionali (EGARCH/quantili) all'avvio sessione.
10. Audit log dei comandi inviati e risposte ricevute con policy di retention.
11. Decisione Q-A risolta nel capitolo (vedi sezione "Decisioni ratificate").

## Scope OUT (esplicito)
- Training storico cross-index intraday pluriennale (FUORI: rinviato a futuro)
- Attivazione market data Eurex/CME a pagamento (FUORI: D-1)
- Modifica spec hard-locked CAP-DATA-01 (FUORI)
- Apertura PHASE-2 cross-index (FUORI: futura)
- Trading / esecuzione ordini, porta 10002 (FUORI: il sistema non esegue)
- Implementazione codice operativo: il capitolo è metodologia, non codice (FUORI)
- Feature engineering / scelta delle feature: già coperto da Parti III/V (FUORI)
- Persistenza dei dati DAPI runtime per uso futuro come dataset di re-training
- Continuità del tape, recupero automatico gap entro 100gg CANDLERANGE,
  riconciliazione canonica giornaliera e storicizzazione strutturata: trattati
  nel capitolo successivo (CAP-DATA-03 / Parte 10), FUORI da CAP-DATA-02

## Decisioni ratificate (NON riaprire)

### Q-A — Cash europei come gating regime
**Ratificata Q-A-3:** i cash europei (DGER, DSTX50, DITAS, DFRA) entrano
ESCLUSIVAMENTE come:
- logging operativo
- gating qualitativo a basso costo per il supervisore umano (regole esplicite,
  auditable, configurabili fuori dal GA)
Perimetro vincolante da scrivere nel capitolo:
- NON entrano nel feature tensor che alimenta il GA
- NON entrano nella state machine del segnale (no condizioni "if DGER drop>X
  then blocca segnale")
- l'eventuale regola di gating qualitativo vive in config/gating_rules.yaml
  (o equivalente), versionata, modificabile senza re-training

### Altre decisioni vincolanti
- D-1: niente market data a pagamento
- D-6: uso esclusivo canale, no DGo/TradingView concorrente
- C-1: naming β2 (CAP_09_parte_9.md, REPORT_CAP_09.md, "Parte 9" arabo)
- C-2: push diretto origin/main
- C-3: aggiornamento 00_indice.md a fine ciclo

## Sei gap obbligatori da chiudere nel capitolo (C-7)
1. **Gap-1 Autenticazione canale**: dichiarare che la pipeline runtime gira
   sulla stessa macchina dell'account abilitato (Darwin locale, no remote access).
   APIPortSettings.txt nel filesystem utente è identificatore, non credenziale.
2. **Gap-2 Policy timezone**: dichiarare se i timestamp Darwin sono trattati
   come CET locale (con conversione CEST automatica) o come UTC convertito
   dal client. Coerente con timeline epoche CAP-DATA-01 §3.5.
3. **Gap-3 Riavvio Darwin mezzanotte**: specifica comportamento pipeline a
   restart (riconnessione automatica + marker RUNTIME_GAP nel log).
4. **Gap-4 Audit log retention**: tutti i comandi inviati + risposte ricevute
   loggati con timestamp UTC. Retention minima 90gg rolling per debug,
   retention permanente per giorni di emissione segnale (compliance interna).
5. **Gap-5 Test regressione exports**: dichiarare che la pipeline runtime
   eseguita oggi su simboli con storico ≤100gg deve produrre output identico
   a quello già archiviato in C:\directa_history_parametric_export_overlay\exports
   (a meno di righe nuove). Sanity check di non-regressione.
6. **Gap-6 Soglia commissioni**: comportamento se commissioni mensili
   scendono sotto 200 EUR (DAPI base diventa 20 EUR/mese). Pipeline
   tollera l'addebito automatico, alert al supervisore.

## Done criteria (verificabili)
1. File docs/methodology_v2/CAP_09_parte_9.md prodotto, 8-10 pp (stima),
   struttura coerente con la scaletta in calce (12 sezioni)
2. File reports/REPORT_CAP_09.md prodotto secondo template supervisore
3. Tutti gli input autoritativi della sezione INPUT verbatim nel capitolo
   (banner Darwin "Release 2.5.1", comandi CANDLERANGE/SUB/UNSUB, schemi
   CANDLE/ANAG/BOOK_5/PRICE, codici errore 1004/1007/1030, limite 100gg,
   rate-limit ~14 connessioni / cooldown 30s, conflitto DGo)
4. Tabella mappatura schema DAPI -> bundle frozen Portara completa per
   TUTTI i campi del bundle: bar_open, bar_high, bar_low, bar_close,
   volume, tick_count, bar_synthetic, eventuali altri presenti in CAP-DATA-01
5. Decisione Q-A chiusa nel testo con verdetto + motivazione + perimetro
   operativo (Q-A-3 ratificata, vedi sopra)
6. Tutti i 6 Gap (Gap-1..Gap-6) chiusi nel capitolo
7. Tabella decisioni del capitolo (ID, descrizione, motivazione 1 riga) presente
8. Sezione "Punti aperti fuori scope" con almeno: abilitazione FDAX standard,
   lookup completa codici mese IDEM (oltre I=settembre), vendor cross-index
   pluriennale, continuita'/storicizzazione (rinvio a CAP-DATA-03)
9. 00_indice.md aggiornato a fine ciclo (Parte 9 = PASS con hash review)
10. Nessuna modifica a Parti I-VIII del doc v2

## Scaletta deliverable Developer (12 sezioni)
Convenzione storica: il primo capitolo della Parte VIII era CapXX (verifica
ultimo capitolo Parte VIII in 00_indice.md). Parte 9 parte dal capitolo
successivo.

1. Premessa e collocazione (cosa formalizza, relazione con CAP-DATA-01,
   invariante research = runtime applicato all'adapter)
2. Architettura del canale DAPI (gateway, porte 10001/10003 NON 10002,
   banner, file APIPortSettings, vincolo uso esclusivo, pattern socket
   persistente, rate-limit)
3. Catalogo simboli FIB e cash europei (tabella IDEM FIB6x/MINI6x + cash
   DITAS/DGER/DSTX50/DFRA, schemi PRICE/BOOK_5/ANAG, codice mese IDEM
   noto I=settembre, meccanismo derivazione front-month da ANAG)
4. Format dati canonico runtime (CSV header BOM UTF-8, manifest JSON,
   source ∈ {DIRECTA, AGG_FROM_D, AGG_FROM_60s}, ruolo script
   export_directa_history_parametric.py come riferimento implementativo)
5. Mappatura schema DAPI -> bundle frozen Portara (tabella canonica;
   regola bar_synthetic=True anche in runtime quando un minuto non ha
   trade, coerente con CAP-DATA-01 §3.4 e Parte VII gap semantics)
6. Gestione errori, recovery, riavvio Darwin (decodifica 1004/1007/1030,
   backoff, comportamento al riavvio mezzanotte, fallback aggregazione,
   stato RUNTIME_DEGRADED se DGo entra in conflitto)
7. Warm-up degli stati condizionali all'avvio sessione (lookback DAPI
   ≤100gg sufficiente per warm-up tipico EGARCH; fallback Portara per
   restart dopo downtime >100gg)
8. Sessione operativa runtime FIB 08:00-22:00 CET (calendario, timezone,
   allineamento alla timeline epoche FIB di CAP-DATA-01 §3.5)
9. Decisione Q-A: gating cash europei (verdetto Q-A-3, motivazione,
   regola operativa, perimetro vincolante)
10. Audit log e retention (cosa logga, formato, retention minima)
11. Punti aperti fuori scope (FDAX standard, lookup mese IDEM, vendor
    cross-index pluriennale, rinvio CAP-DATA-03)
12. Tabella decisioni del capitolo

## Rollback criteria
- Decisione Q-A-3 reversibile in capitolo successivo se l'esperienza
  operativa mostra che il logging cash è inutile o dannoso
- Tabella ticker DAPI non reversibile (fattuale, verificato empiricamente
  2026-05-27)
- Adapter bar_synthetic non reversibile (invariante semantico ereditato
  da CAP-DATA-01 §3.4)
- Vincolo uso esclusivo canale (D-6) non reversibile
===

COMMIT (dopo scrittura ACTIVE_TASK):
  Messaggio: "[ORCH] CAP-DATA-02 apertura sessione: ACTIVE_TASK creato con
              scope da consulenza, Q-A-3 ratificata, 6 Gap obbligatori,
              CAP-DATA-03 rinviato"
  Push diretto a origin/main.

──────────────────────────────────────────────────────────
STEP 4 — CHIAMATA PLANNER SUBAGENTE
──────────────────────────────────────────────────────────
Modalita': Planner subagente con scope ridotto (decisione D-7).

RAZIONALE:
  Il task card ha gia' Goal/Scope/Done criteria/Rollback ratificati dalla
  consulenza (5 funzioni Planner su 9 gia' coperte). Saltare il Planner sarebbe
  pericoloso: il Developer si troverebbe senza piano formale su 4 funzioni che
  il task card NON copre. Chiamare il Planner senza istruzioni rischierebbe
  doppione.

PROMPT AL PLANNER SUBAGENTE (testo da passare via tool Agent):

  "Hai ACTIVE_TASK.md gia' definito (Goal, Scope IN/OUT, Decisioni ratificate
   Q-A-3 + D-1/D-6/C-1..C-7, 6 Gap obbligatori, Done criteria, Scaletta 12
   sezioni, Rollback criteria) ratificati dal supervisore e dalla consulenza
   metodologica esterna. NON ridefinirli, NON riformularli, NON discuterli.
   Tu AGGIUNGI le 4 cose mancanti nel formato Planner standard:

   (i) MAPPATURA EREDITA' I-VIII -> §X del capitolo
       Per ciascuna delle 12 sezioni della scaletta, elenca quale Parte e
       quale Capitolo specifico del doc v2 (Parti I-VIII) va citato come
       riferimento incrociato. Leggi 00_indice.md per trovare il titolo
       definitivo di ciascuna Parte/Capitolo.
       Esempi attesi (NON copiare letteralmente — verifica i Capitoli reali):
         §1 (research = runtime)              -> Parte I Cap.?, Parte II Cap.10
         §2 (architettura DAPI)               -> CAP-DATA-01 §3.5 (sessione FIB)
         §5 (mappatura schema -> bundle)      -> CAP-DATA-01 §3.4 (bar_synthetic),
                                                 Parte VII (gap semantics)
         §6 (gestione errori, riavvio Darwin) -> Parte VII (gap semantics)
         §7 (warm-up stati condizionali)      -> Parte III Cap.?-?? (EGARCH),
                                                 Parte V (covarianza condizionale)
         §8 (sessione operativa)              -> CAP-DATA-01 §3.5

   (ii) NUMERAZIONE CAPITOLI INTERNI DEL DOCUMENTO METODOLOGICO
        Verifica leggendo 00_indice.md qual è l'ULTIMO capitolo della Parte VIII
        (CAP-DATA-01). Parte 9 parte dal capitolo immediatamente successivo.
        Proponi numerazione Cap.YY..Cap.YY+N per le 12 sezioni della scaletta.
        Indica per ciascuna sezione una lunghezza attesa (in pagine A4) e una
        densità (alta/media/bassa). La consulenza stima il capitolo a 8-10 pp.

   (iii) CENSIMENTO M-PROMEMORIA PERTINENTI
         Leggi CARRYOVER.md. Identifica quali M-XX sono PERTINENTI a CAP-DATA-02.
         Verifica esplicita: M-2 (verifica empirica L_max Telegram) NON si chiude
         in Parte 9 (è materia di Appendice E o oltre). M-16 CLOSED-CAP-07 invariato.
         Output: tabella M-ID | origine | pertinenza CAP-DATA-02 (SI/NO + motivazione).

   (iv) EVENTUALI DECISIONI DI SCOPE RESIDUE
        Se trovi ambiguita' NON risolte dalle decisioni gia' ratificate
        (D-1..D-7, C-1..C-7, Q-A-3), apri Q-XX in tasks/QUESTIONS.md PRIMA di
        concludere. Le decisioni gia' ratificate NON sono ambiguita': sono
        decisioni chiuse — verificare prima questa lista.
        Probabile che non ce ne siano: il task card e la consulenza sono molto
        dettagliati. Ma verifica.

   Formato di output: aggiungi le 4 sezioni sopra in coda ad ACTIVE_TASK.md (NON
   sovrascrivere il task card). Le sezioni nuove vanno tutte sotto la sezione
   '## Rollback criteria'. Committa tu stesso le modifiche ad ACTIVE_TASK.md
   con messaggio '[PLANNER] CAP-DATA-02: mappatura eredita + numerazione capitoli +
   censimento M-promemoria' e push.

   Vincoli operativi:
   - NON modificare le sezioni esistenti del task card (Goal, Scope IN, Scope OUT,
     Decisioni ratificate, 6 Gap obbligatori, Done criteria, Scaletta, Rollback)
   - NON modificare alcun file in docs/methodology_v2/
   - NON scrivere docs/methodology_v2/CAP_09_parte_9.md — quello e' compito
     del Developer
   - NON aprire QUESTIONS senza prima verificare che la decisione non sia gia'
     nelle ratifiche
   - NON usare WebFetch / WebSearch (subagente no-web per design)"

──────────────────────────────────────────────────────────
STEP 5 — CHIAMATA DEVELOPER, CHECK POST-DEV, REVIEWER, CHIUSURA
──────────────────────────────────────────────────────────
Procedi come da .claude/CLAUDE.md:

  (5a) Azzera tasks/DEV_STATUS.md (commit + push se non gia' vuoto).

  (5b) Chiama subagente DEVELOPER per leggere ACTIVE_TASK.md (gia' arricchito
       dal Planner) e produrre:
         - docs/methodology_v2/CAP_09_parte_9.md (Parte 9 del doc, scaletta
           12 sezioni, 8-10 pp stimate)
         - reports/REPORT_CAP_09.md (report supervisore secondo format
           developer.md)
         - aggiornamento 00_indice.md (Parte 9 = "IN REVIEW")
         - commit + push + DEV_STATUS = READY_FOR_REVIEW

       PROMPT al Developer subagente (testo da passare via tool Agent):

         "Hai ACTIVE_TASK.md gia' arricchito dal Planner (Goal, Scope IN/OUT,
          Decisioni ratificate Q-A-3 + D-1/D-6/C-1..C-7, 6 Gap obbligatori,
          Done criteria, Scaletta 12 sezioni con numerazione capitoli e
          mappatura eredita' Parti I-VIII, Rollback criteria, censimento
          M-promemoria, pertinenze).
          NON ridiscutere il task card.

          Produci docs/methodology_v2/CAP_09_parte_9.md seguendo la scaletta
          12 sezioni e citando tutti gli input autoritativi di
          tasks/INDAGINE_DIRECTA_CROSS_INDEX.md (banner Darwin Release 2.5.1,
          comandi CANDLERANGE/SUB/UNSUB, schemi risposta CANDLE/ANAG/BOOK_5/
          PRICE, codici errore 1004/1007/1030, limite 100gg, rate-limit
          ~14 connessioni / cooldown 30s, conflitto DGo/TradingView).

          OBBLIGATORIO:
          - Chiudere tutti i 6 Gap (Gap-1..Gap-6) in modo esplicito
          - Decisione Q-A risolta con verdetto Q-A-3 + motivazione +
            PERIMETRO vincolante (vedi ACTIVE_TASK.md sezione
            'Decisioni ratificate -> Q-A')
          - Tabella mappatura schema DAPI -> bundle frozen Portara
            COMPLETA per tutti i campi del bundle
          - Aggiornare 00_indice.md aggiungendo Parte 9 = 'IN REVIEW'
          - Produrre reports/REPORT_CAP_09.md secondo template

          Vincoli operativi:
          - NON modificare alcuna Parte I-VIII del doc v2
          - NON usare WebFetch / WebSearch (subagente no-web per design)
          - NON inventare fatti esterni: tutti i fatti vengono da
            tasks/INDAGINE_DIRECTA_CROSS_INDEX.md o dal PDF hard-locked
            o dai capitoli Parti I-VIII del doc v2
          - NON sconfinare in CAP-DATA-03: continuita', storicizzazione,
            recupero gap, riconciliazione canonica giornaliera sono FUORI
            scope (rinvio esplicito nei punti aperti)
          - NON includere codice operativo (il capitolo è metodologia)
          - NON proporre attivazione market data a pagamento (D-1)
          - Lunghezza attesa: 8-10 pp A4
          - Commit messaggio: '[DEV] CAP-DATA-02 Parte 9 v1: scrittura
            iniziale capitolo + indice IN REVIEW'
          - Push diretto a origin/main
          - Settare DEV_STATUS = READY_FOR_REVIEW dopo commit"

  (5c) ESEGUI il check post-Developer (6 controlli di CLAUDE.md). Se anche
       uno fallisce, rilancia Developer con prompt mirato; NON chiamare
       Reviewer. I controlli minimi specifici a CAP-DATA-02:
         - CAP_09_parte_9.md presente, 8-12 pp
         - 12 sezioni scaletta tutte presenti
         - 6 Gap chiusi (Gap-1..Gap-6)
         - Q-A-3 verdetto + perimetro vincolante presente
         - Tabella mappatura schema DAPI -> bundle Portara presente,
           tutti i campi del bundle coperti
         - 00_indice.md Parte 9 = IN REVIEW
         - REPORT_CAP_09.md presente, template rispettato
         - Nessuna modifica a Parti I-VIII del doc v2

  (5d) Se 6/6 OK, chiama subagente REVIEWER.

       PROMPT al Reviewer subagente (testo da passare via tool Agent):

         "Audit ostile della Parte 9 (CAP-DATA-02) del doc metodologico v2.
          Leggi docs/methodology_v2/CAP_09_parte_9.md e reports/REPORT_CAP_09.md.

          Criteri di valutazione:

          PASS — devono valere TUTTI:
          1. Tutti gli input autoritativi presenti verbatim (banner Darwin
             Release 2.5.1, comandi CANDLERANGE/SUB/UNSUB, schemi risposta
             CANDLE/ANAG/BOOK_5/PRICE, codici errore 1004/1007/1030, limite
             100gg, rate-limit ~14 conn / cooldown 30s, conflitto DGo)
          2. Tabella mappatura schema DAPI -> bundle frozen Portara
             completa, copre TUTTI i campi del bundle, nessuna trasformazione
             non specificata
          3. Decisione Q-A chiusa con verdetto Q-A-3 + motivazione +
             PERIMETRO operativo vincolante (no feature GA, no state machine
             segnale, gating qualitativo in config separato)
          4. Vincolo 'uso esclusivo account / no DGo concorrente' (D-6)
             esplicitato come regola normativa, non solo nota
          5. Warm-up degli stati condizionali (sezione 7) specificato anche
             solo a livello di policy metodologica
          6. Coerenza con CAP-DATA-01 §3.4 (gap semantics, bar_synthetic)
             verificabile nella tabella mappatura
          7. Nessuna pretesa che PHASE-2 cross-index sia coperta da DAPI
          8. Tutti i 6 Gap obbligatori (Gap-1..Gap-6) chiusi
          9. Nessuno sconfinamento in CAP-DATA-03 (continuita',
             storicizzazione, recupero gap, riconciliazione)

          CONDITIONAL — trigger tipici:
          - Tabella mappatura schema presente ma con 1-2 campi non
            specificati o ambigui
          - Decisione Q-A presa ma con perimetro operativo vago
          - Warm-up trattato superficialmente
          - Catalogo simboli completo ma senza meccanismo derivazione
            front-month da ANAG
          - Uno o più dei 6 Gap chiusi in modo superficiale

          FAIL — trigger tipici:
          - Decisione Q-A rinviata o ambigua
          - Tabella mappatura schema assente
          - Affermazioni in contraddizione con CAP-DATA-01 (es. DAPI come
            fonte training)
          - Implementazione codice mescolata alla metodologia
          - Proposta di attivazione market data a pagamento (viola D-1)
          - Sconfinamento in CAP-DATA-03

          Produci reviews/REVIEW_CAP_09_review.md con:
          - verdetto PASS / CONDITIONAL / FAIL
          - tabella 'Classificazione per il supervisore' (BUG REALE /
            MIGLIORA PERF / NEUTRO / RISCHIO PEGGIORAMENTO) per ogni finding
          - lista finding numerati con citazione testo del capitolo

          Vincoli operativi:
          - NON usare WebFetch / WebSearch (subagente no-web per design)
          - NON proporre modifiche a CAP-DATA-01 o altre Parti
          - NON proporre apertura PHASE-2
          - Commit '[REVIEW] CAP-DATA-02 Parte 9 v1: verdetto <X>'
          - Push diretto a origin/main"

  (5e) Se Review emette CONDITIONAL o FAIL → punto di controllo supervisore
       (vedi CLAUDE.md 'Punto di controllo supervisore'), ritorno a Developer
       per rework su finding ammessi, ripeti (5c)-(5d).

  (5f) Se Review emette PASS:
       - Aggiorna 00_indice.md: Parte 9 = 'PASS Review vN' con hash review
         (decisione C-3: aggiornamento avviene QUI, non prima)
       - Aggiorna CARRYOVER.md SOLO se la Review ha emesso NUOVI M-promemoria
         per Parti successive. M-2 OPEN preservato invariato (non si chiude
         in Parte 9). M-16 CLOSED-CAP-07 invariato.
       - Azzera DEV_STATUS.md
       - Verifica le 7 condizioni di chiusura sessione (CLAUDE.md)
       - Produci nuovo file tasks/SESSION_HANDOFF_CAP-DATA-02_to_CAP-DATA-03.md
         con riepilogo + prompt-template per la sessione successiva
         (CAP-DATA-03 / Parte 10: storicizzazione strutturata, continuità del
         tape, recupero gap entro 100gg, riconciliazione canonica giornaliera —
         tema che il supervisore ha gia' anticipato e che andra' formalizzato
         con verifiche empiriche preliminari V-1/V-2/V-3 da pianificare).
       - Notifica al supervisore con riepilogo e ferma la sessione.

=========================================================
FINE ISTRUZIONI SESSIONE CAP-DATA-02
=========================================================
