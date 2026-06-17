# REPORT — SPEC-FUNZ-01-B6 (Schema-dato DAPI & continuità tape)

> **Conferma letture obbligatorie**: letti in ordine PRIMA di scrivere: tasks/METODO.md (RM-1..RM-4 + RACC-METODO-2), .claude/BASE_COMUNE.md, .claude/agents/spec_developer.md, tasks/ACTIVE_TASK.md (card B6 rev. CARD-FIX-01). Eccezione RM-2: letti i decoder di produzione export_directa_history_parametric.py e probe_dapi.py e gli M-promemoria M-1/M-9/M-10/M-4/M-3 in tasks/STATO_CORRENTE.md per ancorare ogni claim di schema.

---

## 1. Cosa è stato prodotto

docs/spec_funzionale/SPEC_FUNZ_01_B6.md: specifica funzionale schema-dato DAPI & continuità tape, **61 requisiti atomici** (37 B6-R, 20 B6-CN, 4 B6-NFR), tutti tracciati a [DOC-INTERNO CAP_09_parte_9.md:riga] / [DOC-INTERNO CAP_10_parte_10.md:riga] / [DOC-INTERNO CAP_02_parte_II.md:riga] (premessa) o [CODICE-ESISTENTE path:line] o [PROVA-EMPIRICA data], con valore dichiarato. Sette sezioni: (1) scopo/cecità/convenzioni; (2) adapter & schema-dato (CANDLE/PRICE/BOOK_5/format); (3) replay deterministico; (4) warm-up & continuità; (5) riconciliazione canonica; (6) storicizzazione tape; (7) matrice + nota di rinvio + PENDING-empirico + nota RM-3.

## 2. Ipotesi di partenza

- Card B6 e fatti certificati (§2 card) autoritativi: schema CANDLE C;L;H;O;V, PRICE f8/f9/f6, BOOK_5 (290/290), mesi F/I, codici errore, L_warmup=30 congelato, 13 campi header — consolidati fedelmente, non ri-derivati né sovra-marcati.
- Capitoli del perimetro chiusi PASS (freeze G-09): citati selettivamente, non riaperti né ri-verificati.
- Cecità verso v2/B*: ID B6-* auto-assegnati da zero, nessun conteggio-target.

## 3. Decisioni rilevanti

- **Atomicità N1 su F5 (gap vs restart)**: recupero gap <=100gg (B6-R-24) e restart >100gg RUNTIME_STALE_RESTART (B6-R-27) sono requisiti distinti, non impacchettati: trigger, scala temporale e capitolo diversi.
- **F3 (f8/f9 cross-schema)**: separati per tipo-messaggio in B6-R-16 (PRICE realtime) e B6-R-17 (CANDLE daily), con B6-CN-04 a vietare la deduzione cross-namespace.
- **F4 (PRICE/BOOK_5 input adapter)**: consolidati ancorati al requisito-adapter (B6-CN-03), non come materia-canale.
- **F7 (Darwin-mezzanotte vs STALE)**: tenuti distinti in §7.2 — il primo premessa B5, il secondo in-scope B6.
- **Determinismo bit-exact**: consolidato come invariante che adapter preserva (B6-NFR-01..04), fondazione formale in premessa CAP_02 Cap.10 (:291,:293); non ri-derivato dal motore.
- **Cap.48 framing**: tradotto in vincoli di contenitore (B6-CN-05..09), non requisito standalone.
- **Diff col decoder canonico (RACC-METODO-2)**: CANDLE (concordanza piena dei 2 decoder), PRICE (decoder copre solo last, semantica f6/f8/f9 da PROVA-EMPIRICA), BOOK_5 (decoder documenta lo schema in commento ma non parsea le triple, posizioni da PROVA-EMPIRICA). Diff esplicitato in ogni caso.

## 4. Misura prima/dopo (greenfield di consolidamento)

PRIMA: materia schema-dato DAPI & continuità tape dispersa in 7 capitoli su 2 Parti (Cap.48/49/51 + Cap.59/60/61/62) più decoder e M-promemoria, non leggibile come elenco di requisiti da un esterno. DOPO: 61 requisiti R/CN/NFR atomici tracciati con valore dichiarato e matrice a 61 righe, schema-dato ancorato al decoder canonico con diff esplicito e permutazioni alternative escluse (RM-1), confini premessa/in-scope espliciti, PENDING-empirico separati dai certificati. Nessuna metrica GA inventata (track di prodotto).

## 5. Domande aperte / Blocchi

**Nessun blocco.** Tutta la materia del perimetro risolvibile dai capitoli + decoder + audit. Nessun requisito porta marcatore [B-N PROVVISORIO].

PENDING-empirico marcati nella spec (§7.3), NON asseriti: PE-1 codici mese Mar/Dic; PE-2 ticker 1030; PE-3 riavvio Darwin mezzanotte; PE-4 PRICE f5/f7; PE-5 base calendario-vs-trading-days finestre 30/100 (V-2). Pendenze ereditate, non blocchi di questo task.

## 6. Criterio di rollback

Consolidamento di capitoli chiusi PASS: rollback = revisione di un requisito a seguito di un finding di Review (citazione errata, atomicità violata, diff-decoder mancante, permutazione non esclusa, PENDING sovra/sotto-marcato). Patch chirurgica al solo requisito, ri-verifica con Read della citazione, nessun impatto sui capitoli-fonte (freeze G-09).

---

## Tabella verifica AC

| AC | Stato | Evidenza |
|----|-------|----------|
| AC-G1 (atomicità N1) | OK | Ogni B6-* una sola proposizione; F5 spezzato in B6-R-24/B6-R-27 |
| AC-G2 (tracciabilità a riga) | OK | Matrice §7.1, ogni riga con CAP_xx:riga o decoder path:line o PROVA-EMPIRICA |
| AC-G3 (valore dichiarato) | OK | Ogni requisito ha campo Valore |
| AC-G4 (no verificato-X prima istanza RM-1) | OK | Solo richiami a CAP chiusi/decoder/PROVA-EMPIRICA; blocchi VERIFICA/PROVE/ALTERNATIVE su CANDLE/PRICE/BOOK_5 |
| AC-G5 (etichette RM-3) | OK | §1.5 gerarchia; wiki = [WIKI-HINT, da verificare] §7.4 |
| AC-G6 (grafia canonica) | OK | Solo [CODICE-ESISTENTE]/[PROVA-EMPIRICA]/[DOC-INTERNO]/[WIKI-HINT]; nessun [CODICE-EXISTENTE] |
| AC-G7 (pin riverificati token-per-token) | OK | Tutti i pin decoder e CAP riletti con Read prima di citarli (vedi sezione Applicazione RM-1 a me stesso) |
| AC-G8 (cecità preservata) | OK | §1.4; 0 ID v2, 0 conteggi/partizioni v2 |
| AC-G9 (scope = capitoli §1) | OK | Solo Cap.48/49/51/59/60/61/62 + premessa Cap.10; confini §7.2 |
| AC-G10 (matrice + nota di rinvio) | OK | §7.1 matrice, §7.2 nota di rinvio |
| AC-G11 (invarianti come tali) | OK | Replay bit-exact = NFR (B6-NFR-01..04), non requisito funzionale |
| AC-B6-1 (RM-2 diff col decoder) | OK | Diff esplicito per CANDLE (B6-R-04), PRICE (B6-R-16), BOOK_5 (B6-R-18) |
| AC-B6-2 (RM-1 permutazioni escluse) | OK | Blocchi di esclusione: CANDLE (no O;H;L;C), PRICE f8/f9 (no bid/ask + no confusione CANDLE-daily), BOOK_5 (no triplo invertito) |
| AC-B6-3 (RM-3 gerarchia) | OK | §1.5 + §7.4; 0 conclusioni wiki-only |
| AC-B6-4 (PENDING marcato non asserito) | OK | §7.3 PE-1..5 marcati; certificati elencati separatamente non sovra-marcati |

## Applicazione RM-1 a me stesso

Ogni asserzione fattuale del documento è un richiamo a un capitolo chiuso PASS o a un decoder/prova; non ho introdotto dichiarazioni verificato-X di prima istanza.

**Grep / Read RM-2 eseguiti (decoder di produzione letti path:line)**:
- export_directa_history_parametric.py:467-489 (parse_directa_candle): riletto token-per-token. parts[:9] = kind, symbol, ymd, hms, uff, min_, max_, ape, qty (:471); close_v=Decimal(uff) (:478), low_v=Decimal(min_) (:479), high_v=Decimal(max_) (:480), open_v=Decimal(ape) (:481), volume_v=int(Decimal(qty)) (:482); commento UFF, MIN, MAX, APE => close, low, high, open (:477). -> fonda B6-R-04..09.
- export_directa_history_parametric.py:61 (DEFAULT_INTRADAY_MAX_DAYS = 100): riletto. -> fonda B6-CN-12.
- export_directa_history_parametric.py:228-230 (sintassi CANDLERANGE {symbol} {start} {end} {period_seconds}): riletto. -> fonda B6-R-22, B6-R-24.
- export_directa_history_parametric.py:282-285 (marker END CANDLES): letto (contesto, non requisito standalone).
- export_directa_history_parametric.py:417-425 (is_error_line, string-matching generico): letto -> conferma assenza supporto level-2 sulla semantica dei codici (rilevante per PE/§7.4, non asserito).
- export_directa_history_parametric.py:605-617 (header legacy 11 campi): riletto token-per-token -> fonda B6-CN-06.
- probe_dapi.py:247-273 (CANDLE: p[4]=UFF->close, p[5]=MIN->low, p[6]=MAX->high, p[7]=APE->open): riletto -> fonda B6-R-04 (concordanza col decoder canonico).
- probe_dapi.py:289-306 (PRICE: last=float(p[3]), fields_extra=p[4:], commento schema esatto dei campi extra non documentato): riletto -> fonda B6-R-16 + diff (decoder copre solo last).
- probe_dapi.py:307-317 (BOOK_5: commento schema [BID×5][ASK×5] triple, fields=p[3:] non parsate): riletto -> fonda B6-R-18 + diff (decoder non parsea le triple).

**Capitoli v2 riletti per i pin (token-per-token)**: CAP_09_parte_9.md:21,117,120,125,127,129,131-138,153,158,164-173,177-179,181,191,254,256,257,260-261; CAP_10_parte_10.md:68,79-83,88,90,91,98,119,121-127,131,136-139,146,157-164,168-170,174,184-188,194,196-203,207,209,233; CAP_02_parte_II.md:291,293.

**M-promemoria letti** (tasks/STATO_CORRENTE.md): M-1 (CANDLE C;L;H;O;V, :94), M-9 (PRICE f4/f6/f8/f9, :102), M-10 (BOOK_5 290/290, :103), M-4 (mesi F/I, :97), M-3 (codici errore, :96), riga :33 (audit RM-RETRO CAP-DATA-02 CHIUSO WEB+CLI, 0 SMENTITE).

**Audit empirici di riferimento**: reviews/REVIEW_CAP_DATA_02_RM_RETRO_CLI_review.md (esistenza verificata via Glob; citato come [rif.] per M-10 nei blocchi BOOK_5).

**Alternative escluse documentate inline** (RM-1): CANDLE O;H;L;C (falsificata V-1); PRICE f8/f9 bid/ask (falsificata BOOK_5 simultaneo) + confusione CANDLE-daily (namespace diverso); BOOK_5 triplo invertito (escluso da lots>=orders 290/290) + blocchi invertiti (escluso 29/29) + anomalia 27/05 (artefatto illiquido).

**Limite onesto**: la semantica dei campi PRICE f6/f8/f9 e le posizioni BOOK_5 NON hanno supporto level-2 strutturato (i decoder non parsano questi campi); poggiano su [PROVA-EMPIRICA 2026-06-01] (level-1). Dichiarato esplicitamente nei diff-decoder dei requisiti B6-R-16 e B6-R-18, non nascosto.

## Lista PENDING-empirico

PE-1 codici mese Mar/Dic; PE-2 ticker 1030 (PHASE-2 gated); PE-3 riavvio Darwin mezzanotte; PE-4 PRICE f5/f7; PE-5 base calendario-vs-trading-days finestre 30/100 (V-2). Tutti marcati nella spec §7.3, nessuno asserito come certo.
