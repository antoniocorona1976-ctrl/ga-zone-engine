# REPORT RIDOTTO — Rework AUDIT-RM-RETRO CAP-DATA-02 (Iter.2)

**Task**: rework dei 9 finding approvati dal supervisore dopo verdetto **FAIL** della Review Web (`reviews/REVIEW_CAP_DATA_02_RM_RETRO_review.md`, commit `f6d2ac3`). Mandato operativo: `tasks/ACTIVE_TASK.md` sezione "Finding di Review approvati per rework — Iterazione 2" (tabella #1..#10; #9 NEUTRO escluso). Decisione supervisore 2026-05-30: tutti i 9 finding non-NEUTRO a Developer (4 BUG REALI + 5 MIGLIORA).
**Perimetro toccato**: SOLO **A** (`docs/methodology_v2/CAP_09_parte_9.md`) e **C** (`tasks/INDAGINE_DIRECTA_CROSS_INDEX.md`). **NON toccati**: **D** (`scripts/export_directa_history_parametric.py`, decoder canonico autoritativo), **B** (`reports/REPORT_CAP_09.md`, report storico immutabile), `docs/methodology_v2/00_indice.md` (Parte 9 resta PASS storico). Nessun file fuori perimetro.
**Stato**: COMPLETATO. Patch testuali statiche (nessuna esecuzione DAPI: le voci empiriche residue restano in lista Empirico-CLI della Review, sede CLI).

---

## 1. Cosa e' stato modificato

- **A = `docs/methodology_v2/CAP_09_parte_9.md`** (finding #1, #3, #4, #5, #6, #7, #10):
  - **Cap.49** (#1, catastrofico): tabella "canonica" mappatura CANDLE -> bundle frozen corretta sui 4 campi OHLC; aggiunto blocco RM-1 a 4 righe + etichette [CODICE-ESISTENTE]/[PROVA-EMPIRICA]/[CORREGGE WIKI] sulle righe bar_open/bar_high/bar_low/bar_close/volume.
  - **Cap.46** (#3): cooldown "~30s / 14a conn" riscritto come verifica parziale RM-1 (osservazione singola 27/05 in burst non disambiguato; refutato da M-5 nel regime ~1Hz); regola architetturale "1 connessione persistente per porta" mantenuta. (#10): banner Darwin r29 etichettato [PROVA-EMPIRICA 2026-05-27] + nota prefix-match/Empirico-CLI.
  - **Cap.47** (#7): schema BOOK_5 r93 annotato come verifica parziale (osservazione singola, alternative ordine BID/ASK + indice lots/price non escluse, anomalia bid>ask non disambiguata -> Empirico-CLI). (#10): mese IDEM r61 etichettato [PROVA-EMPIRICA 2026-05-27 / M-4 2026-05-29] (F=giu + I=set verificati, Mar/Dic parziale).
  - **Cap.49** (#7, riflesso): regola bar_synthetic (cella tabella + bullet sintesi) annotata con dipendenza dalle posizioni bid1_lots/ask1_lots non certificate.
  - **Cap.50** (#3): backoff r198 allineato (cooldown verifica parziale, rinvio a M-5). (#4): semantica codici 1004/1007 riscritta come verifica parziale (comando-trigger + "semantica da disambiguare"; nota che is_error_line di D non decodifica codici numerici -> no level-2). (#5): tabella codici estesa con 1017/1015 (NUOVO)/1003 (NUOVO) da [PROVA-EMPIRICA M-3 2026-05-29], con cautela RM-1; 1030 marcato "non riprodotto sul FIB". (#6): riavvio Darwin mezzanotte r207 etichettato [WIKI-HINT, da verificare] + "da osservare empiricamente" (Empirico-CLI).
  - **Cap.51** (#10): limite 100gg r249 etichettato [CODICE-ESISTENTE :61] + [PROVA-EMPIRICA 2026-05-27]; sintassi CANDLERANGE step 2 etichettata [CODICE-ESISTENTE :228-230].
- **C = `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md`** (finding #2, #10):
  - r28 (Q1) e r46 (Q2): schema wiki CANDLE O;H;L;C / Open;High;Low;Close etichettato [WIKI-HINT, dimostrato INESATTO su CANDLE: ordine reale C;L;H;O - vedi export_directa_history_parametric.py:477 e M-1 2026-05-29]. Testo wiki **conservato**, non cancellato.

**Regola di non-cancellazione rispettata**: in tutte le patch il testo originale non e' stato rimosso; e' stato etichettato/ri-caratterizzato ([CORREGGE WIKI] / "verifica parziale" / "refutato da M-5" / [WIKI-HINT]).

---

## 2. Mappatura finding -> patch (prima/dopo)

| # | Classificazione | File:linea | Prima | Dopo |
|---|-----------------|-----------|-------|------|
| 1 | BUG REALE (catastrofico) | A :158-162 (Cap.49) | bar_open<-campo 5 (O), bar_high<-campo 6 (H), bar_low<-campo 7 (L), bar_close<-campo 8 (C), volume<-campo 9 -> ordine wiki O;H;L;C | bar_open<-campo 8 (APE=open), bar_high<-campo 7 (MAX=high), bar_low<-campo 6 (MIN=low), bar_close<-campo 5 (UFF=close), volume<-campo 9 (qty) -> ordine reale C;L;H;O;V. + blocco RM-1 4-righe + etichette [CODICE-ESISTENTE :477-481] [PROVA-EMPIRICA M-1] [CORREGGE WIKI] |
| 2 | BUG REALE (RM-3) | C :28, :46 | schema wiki O;H;L;C dichiarato "documentato", non etichettato | stessa stringa wiki conservata + etichetta [WIKI-HINT, dimostrato INESATTO su CANDLE: ordine reale C;L;H;O - vedi ...:477 e M-1 2026-05-29] |
| 3 | BUG REALE (RM-1, refutato) | A :47, :51, :198 | "cooldown ~30s dopo 14a connessione" dichiarato come "regola operativa fissata" | verifica parziale RM-1: osservazione singola 27/05 in burst non disambiguato; M-5 (75 conn ~1Hz) non osserva cooldown -> 14/30s non costanti; soglia/durata burst >>1Hz non disambiguate. Regola "1 conn persistente per porta" mantenuta come scelta architetturale |
| 4 | BUG REALE (RM-1) | A :194, :195 | semantica 1004/1007 in tabella normativa come fatto | semantica come verifica parziale (comando-trigger osservato + "semantica esatta da disambiguare"); nota che is_error_line di D (:417-425) non decodifica codici numerici -> no supporto level-2; Empirico-CLI per i trigger esatti |
| 5 | MIGLIORA PERFORMANCE | A :192-196 (tabella) | tabella elenca solo 1004/1007/1030 | aggiunti 1017 (sintassi malformata), 1015 (data/parametro invalido, NUOVO), 1003 (comando storico su porta realtime, NUOVO) da [PROVA-EMPIRICA M-3 2026-05-29], con cautela RM-1; 1030 marcato "non riprodotto sul FIB B6086" |
| 6 | MIGLIORA PROCESSO | A :207 (Cap.50) | "manutenzione automatica giornaliera circa a mezzanotte (documentato dal wiki DAPI)" - wiki-only | [WIKI-HINT, da verificare] + "da osservare empiricamente" (Empirico-CLI: sessione cross-midnight); marcata come contingenza di recovery, non schema-dato |
| 7 | MIGLIORA PERFORMANCE | A :93, :164, :168 | schema BOOK_5 + regola bar_synthetic come fatto | annotato: schema da osservazione singola 27/05, alternative (ordine BID/ASK, indice lots/price) non escluse, anomalia bid>ask non disambiguata; regola bar_synthetic dipende da bid1_lots/ask1_lots non certificate -> Empirico-CLI |
| 8 | MIGLIORA PROCESSO | (annotazione qui, NON in B) | - | vedi sezione 3 sotto. reports/REPORT_CAP_09.md NON editato |
| 10 | MIGLIORA PROCESSO | A, C (globale) | etichette di livello fonte assenti (file pre-RM) | aggiunte [CODICE-ESISTENTE]/[PROVA-EMPIRICA]/[WIKI-HINT] dove la sostanza regge: W4 CANDLERANGE (Cap.51 step 2 + #1), W6 mesi F/I (A :61), W7 100gg (A :249/:61), W10 banner (A :29) |

**Escluso (NON patchato):** #9 NEUTRO (A :94, campi PRICE 5/6/7 marcati ? - gia' forma RM-1 onesta). Resta come-e'; disambiguazione in lista Empirico-CLI della Review.

**Coerenza A<->C (finding #1<->#2):** A Cap.49 e C r28/r46 ora riportano **lo stesso schema reale** C;L;H;O; A lo dichiara come mappatura corretta con etichetta [CORREGGE WIKI], C conserva la stringa wiki etichettandola come hint smentito che rimanda alla stessa fonte (export_directa_history_parametric.py:477 + M-1). Nessuna divergenza non etichettata residua sullo schema CANDLE fra A, C e il decoder canonico D.

---

## 3. Annotazione finding #8 (B = REPORT_CAP_09.md, NON editato)

Il finding #8 (MIGLIORA PROCESSO) osserva che B (reports/REPORT_CAP_09.md) dichiara "OK" sugli AC-3/AC-4 (B :39, :51, :52) avendo verificato la **completezza dei campi** della tabella Cap.49 ma **non la correttezza del mapping** contro il decoder canonico D: per questo l'errore catastrofico W1 (ordine OHLC invertito) e' sfuggito al ciclo Review v1->v2.

**Annotazione (vive qui, non in B):** la verifica AC-3/AC-4 di B avrebbe dovuto essere estesa a "mapping CANDLE verificato contro il decoder canonico di produzione D (export_directa_history_parametric.py:477-481)", non solo "tabella completa per TUTTI i campi". Per i futuri AC che dichiarano la correttezza di uno schema-dato di un sistema esterno, il criterio di verifica deve includere il confronto puntuale con il decoder di produzione esistente (RM-2), non la sola completezza strutturale.

**Vincolo rispettato:** reports/REPORT_CAP_09.md e' report storico immutabile del Developer di CAP-DATA-02. **NON e' stato editato.** L'annotazione resta in questo report ridotto di rework, come da mandato (ACTIVE_TASK.md finding #8 + Vincoli assoluti (ii)).

---

## 4. Verifica working tree

git status --short al momento del commit del rework mostra solo i file del perimetro:
- M docs/methodology_v2/CAP_09_parte_9.md (A)
- M tasks/INDAGINE_DIRECTA_CROSS_INDEX.md (C)
- (questo report reports/REPORT_AUDIT_RM_RETRO_CAP_DATA_02.md - nuovo file)

NON modificati e NON nel commit: D (scripts/export_directa_history_parametric.py), B (reports/REPORT_CAP_09.md), docs/methodology_v2/00_indice.md. File estranei al task tollerati ed esclusi dal commit: .claude/settings.json, .claude/scheduled_tasks.lock.

## 5. Verifica push

Patch A+C committate e pushate su origin/main; questo report committato e pushato; tasks/DEV_STATUS.md = READY_FOR_REVIEW committato e pushato. git status non mostra "Your branch is ahead of origin/main" dopo il push. Hash dei commit riportati nella consegna all'Orchestratore.

---

## Iterazione 2 - risposta ai finding di Review

Tutti e 9 i finding approvati sono stati chiusi con patch chirurgiche nei soli file del perimetro A/C. Nessun finding contestato.

- **#1 (BUG REALE catastrofico) - CHIUSO.** La mappatura OHLC di Cap.49 era invertita su tutti e 4 i campi (ordine wiki O;H;L;C). Corretta all'ordine reale del decoder canonico D (parts[:9] = ...,uff,min_,max_,ape,qty con UFF->close, MIN->low, MAX->high, APE->open): bar_open<-8(APE), bar_high<-7(MAX), bar_low<-6(MIN), bar_close<-5(UFF), volume<-9. E' l'unica asserzione del rework dichiarata **verifica piena** (level-2 D + level-1 M-1, alternative non escluse vuote); scritta col blocco RM-1 4-righe.
- **#2 (BUG REALE RM-3) - CHIUSO.** Radice della contaminazione di #1: C dichiarava lo schema wiki come "documentato". Etichettato [WIKI-HINT, dimostrato INESATTO] su r28 e r46, coerente con #1.
- **#3 (BUG REALE RM-1, refutato) - CHIUSO.** Cooldown 14/30s riscritto come verifica parziale refutata da M-5; regola architetturale mantenuta.
- **#4 (BUG REALE RM-1) - CHIUSO.** Semantica 1004/1007 riscritta come verifica parziale; nota assenza level-2 in is_error_line.
- **#5 (MIGLIORA PERFORMANCE) - CHIUSO.** Tabella codici estesa con 1017/1015/1003 da M-3.
- **#6 (MIGLIORA PROCESSO) - CHIUSO.** Riavvio mezzanotte etichettato [WIKI-HINT, da verificare].
- **#7 (MIGLIORA PERFORMANCE) - CHIUSO.** BOOK_5 e regola bar_synthetic annotati come verifica parziale (posizioni non certificate).
- **#8 (MIGLIORA PROCESSO) - CHIUSO** via annotazione in sezione 3 (B non editato).
- **#10 (MIGLIORA PROCESSO) - CHIUSO.** Etichette di livello fonte aggiunte dove la sostanza regge (W4/W6/W7/W10).

**Misura prima/dopo (qualitativa, salute dati per CAP-DATA-03):**

| Metrica | Prima | Dopo |
|---------|-------|------|
| Schema CANDLE in Cap.49 (mapping OHLC) | invertito su 4/4 campi (errore wiki) | corretto su 4/4, ancorato a D + M-1 |
| Divergenze schema CANDLE non etichettate A<->C<->D | 1 (catastrofica) | 0 |
| Asserzioni "verificato" refutate dall'empirico lasciate come fatto (cooldown) | 1 (W9) | 0 (riscritta verifica parziale) |
| Codici errore senza supporto level-2 dichiarati come fatto | 1004/1007 come fatto | verifica parziale + Empirico-CLI |
| Dominio codici errore vs M-3 | incompleto (manca 1017/1015/1003) | completo, con cautela RM-1 |
| Conclusioni wiki-only non etichettate | 2 (CANDLE, riavvio mezzanotte) | 0 (etichettate) |

**Criterio di rollback:** se la Re-Review Iter.3 rileva che (a) il mapping di Cap.49 non coincide ancora con D :477-481, oppure (b) una delle riscritte #3/#4 reintroduce una dichiarazione "verificato" senza alternative escluse, le patch corrispondenti vanno riviste. Il vincolo D immutabile e' la fonte di verita' del rollback per #1.

---

## Self-review RM-1..RM-3 (RM-4 opzione A)

Questo report e' output non-CAP determinante (handoff di rework, dichiara la chiusura di "fatti" - RM-4 criterio (b)). Self-review esplicita opzione A.

### Asserzioni "verificato" nel formato 4-righe

```
VERIFICA: lo schema CANDLE reale del payload Directa e' UFF;MIN;MAX;APE;V = close;low;high;open;volume; la mappatura corretta in Cap.49 e' bar_open<-campo 8 (APE), bar_high<-campo 7 (MAX), bar_low<-campo 6 (MIN), bar_close<-campo 5 (UFF), volume<-campo 9.
PROVE: [CODICE-ESISTENTE export_directa_history_parametric.py:471] (kind, symbol, ymd, hms, uff, min_, max_, ape, qty = parts[:9]) + [CODICE-ESISTENTE :477-481] (commento UFF, MIN, MAX, APE => close, low, high, open, con close_v=Decimal(uff)/low_v=Decimal(min_)/high_v=Decimal(max_)/open_v=Decimal(ape)/volume_v=int(Decimal(qty))); decoder che ha processato ~647 dump storici. + [PROVA-EMPIRICA M-1 2026-05-29 via STATO_CORRENTE.md sezione 5] (V-1 tick-by-tick ha distinto Open da Close sui tick realtime).
ALTERNATIVE COMPATIBILI ESCLUSE: ordine wiki O;H;L;C (escluso da V-1, che sui tick realtime ha distinto O da C; sui soli daily O/C erano indistinguibili, da cui l'errore originale); ordine parziale O;L;H;C dell'errore storico sezione 3.1 (escluso: D mappa MIN->low in pos 6 e MAX->high in pos 7, cioe' L/H sono in pos 6/7 non 7/6).
ALTERNATIVE COMPATIBILI NON ESCLUSE: nessuna. (Asserzione verificata piena: level-2 D + level-1 M-1 concordi, nessuna prova DAPI nuova richiesta.)
```

```
VERIFICA: la patch #1 corregge tutti e quattro i campi OHLC della tabella Cap.49 e non lascia divergenze schema CANDLE non etichettate fra A, C e D.
PROVE: lettura statica post-patch di A :167-171 (campi 8/7/6/5/9) confrontata con D :471,:477-481; lettura di C :28,:46 (stringa wiki conservata + etichetta che rimanda a :477 e M-1).
ALTERNATIVE COMPATIBILI ESCLUSE: "patch parziale (solo O/C, non H/L)" esclusa (verificate tutte e 4 le righe: bar_high<-7=MAX, bar_low<-6=MIN); "C ancora dichiara O;H;L;C come fatto" esclusa (C ora etichetta la stringa come hint smentito).
ALTERNATIVE COMPATIBILI NON ESCLUSE: nessuna sul mapping OHLC. (La correttezza del rendering Markdown della tabella non e' una verifica empirica.)
```

Le riscritte **#3 (cooldown)** e **#4 (codici 1004/1007)** sono state scritte in forma **"verifica parziale"** (ALTERNATIVE COMPATIBILI NON ESCLUSE non vuote: soglia/durata cooldown sotto burst >>1Hz; semantica esatta dei codici e trigger esatti) e rinviate a Empirico-CLI; non sono dichiarate "verificato" in questo report. La semantica empirica di M-3/M-5 e' assunta come [PROVA-EMPIRICA 2026-05-29 via STATO_CORRENTE.md sezione 5], non ri-verificata (dump probe_out/* locali non versionati, sede CLI).

### Grep RM-2 eseguito

Decoder/parser DAPI nel repo consultati per la correzione di #1 (e per ancorare #4/#5 alla mancanza di supporto level-2):

- **scripts/export_directa_history_parametric.py:471** - kind, symbol, ymd, hms, uff, min_, max_, ape, qty = parts[:9] (ordine posizionale del payload CANDLE).
- **scripts/export_directa_history_parametric.py:477-481** - commento "UFF, MIN, MAX, APE => close, low, high, open" + close_v=Decimal(uff) / low_v=Decimal(min_) / high_v=Decimal(max_) / open_v=Decimal(ape) / volume_v=int(Decimal(qty)). **Schema canonico C;L;H;O;V. Fonte di verita' di #1.**
- **scripts/export_directa_history_parametric.py:228-230** - emissione CANDLERANGE {symbol} {start} {end} {period_seconds} (period_s ultimo). Fonte level-2 per #10 W4.
- **scripts/export_directa_history_parametric.py:417-425** - is_error_line: string-match generico (ERR/Wrong/Not enough parameters/error/errore/not enabled/not valid), **NON decodifica codici numerici** -> nessun supporto level-2 per la semantica numerica dei codici 1004/1007/1017/1015/1003/1030 (base di #4).
- **scripts/export_directa_history_parametric.py:61** - DEFAULT_INTRADAY_MAX_DAYS = 100. Fonte level-2 per #10 W7.
- **scripts/probe_dapi.py (ramo CANDLE, post-fix a12ae32)** - concorde con D su C;L;H;O;V (citato come supporto, gia' auditato in CAP-DATA-01 PASS, non oggetto qui).

Nessun decoder DAPI aggiuntivo oltre i due noti (D canonico + probe_dapi). **Nessun codice di produzione dichiara O;H;L;C**: la divergenza di #1/#2 era solo testuale (ereditata dal wiki), non di codice. **D non e' stato modificato** (vincolo assoluto).

### Fonti RM-3 etichettate per livello

- Schema CANDLE reale C;L;H;O;V - [CODICE-ESISTENTE export_directa_history_parametric.py:477-481] (livello 2) + [PROVA-EMPIRICA M-1 2026-05-29] (livello 1).
- Codici errore 1004/1007/1017/1015/1003/1030 - [PROVA-EMPIRICA M-3 2026-05-29 dump probe_out/w4_errcodes_20260529.json via STATO_CORRENTE.md sezione 5] (livello 1, dump citato tramite M-promemoria, non ispezionato); semantica numerica priva di livello-2 in is_error_line.
- Cooldown refutato - [PROVA-EMPIRICA M-5 2026-05-29 dump probe_out/w6_cooldown_20260529.json via STATO_CORRENTE.md sezione 5] (livello 1).
- Mese F/I - [PROVA-EMPIRICA 2026-05-27 Appendice B.2] + [PROVA-EMPIRICA M-4 2026-05-29] (livello 1).
- Limite 100gg - [CODICE-ESISTENTE :61] (livello 2) + [PROVA-EMPIRICA 2026-05-27 Appendice A.2] (livello 1).
- Banner Darwin - [PROVA-EMPIRICA 2026-05-27 Appendice A] (livello 1).
- Schema wiki CANDLE O;H;L;C, riavvio Darwin mezzanotte - [WIKI-HINT, dimostrato/da verificare] (livello 4). **Nessuna conclusione del rework si appoggia solo a livello 4**: lo schema CANDLE e' ora ancorato a livelli 1-2; il riavvio mezzanotte e' etichettato come hint da osservare (non usato come fatto verificato).

### Assunzioni non testate usate come premesse

- Schema CANDLE C;L;H;O;V assunto per mandato del task (M-1 premessa, V-1 non riauditata - ACTIVE_TASK.md Note al Developer / eredita' #16).
- Risultati M-3/M-4/M-5 assunti come [PROVA-EMPIRICA 2026-05-29] acquisita; dump locali non ispezionati (sede CLI).
- Le voci empiriche residue (W2/W3 schema, W5 trigger esatti, W6 Mar/Dic, W8 mezzanotte, W9 burst, W10 release) restano in lista Empirico-CLI della Review: NON dichiarate verificate qui.

### File del repo letti durante il rework (a riprova di RM-2)

tasks/METODO.md, .claude/agents/developer.md, tasks/ACTIVE_TASK.md, reviews/REVIEW_CAP_DATA_02_RM_RETRO_review.md, tasks/STATO_CORRENTE.md sezione 5, reports/REPORT_AUDIT_RM_RETRO_CAP_DATA_01.md (modello), scripts/export_directa_history_parametric.py:465-499, docs/methodology_v2/CAP_09_parte_9.md (Cap.46-51), tasks/INDAGINE_DIRECTA_CROSS_INDEX.md (Q1/Q2).
