# TASK ATTIVO: CAP-DATA-03 — Parte 10 — Continuità tape, recupero gap, riconciliazione canonica, storicizzazione strutturata

**Assegnato da**: Planner
**Output atteso primario**: `docs/methodology_v2/CAP_10_parte_10.md` (capitolo metodologico nuovo, ~9-12 pp, capitoli Cap.57-Cap.65)
**Output atteso secondario**: `reports/REPORT_CAP_10.md` (report supervisore con le 5 sezioni standard: "Cosa è stato prodotto", "Ipotesi di partenza", "Decisioni rilevanti", "Misura prima/dopo", "Domande aperte", "Criterio di rollback") + aggiornamento `docs/methodology_v2/00_indice.md` (Parte 10 da "IN CORSO" a "IN REVIEW" a "PASS" attraverso il ciclo)
**Stato**: IN ATTESA
**Workflow**: **Planner → Developer → Reviewer pieno** (CAP-XX nuovo, NON Review-First)
**Sede del Reviewer proposta**: **WEB** (un CAP-XX completo è documento metodologico + grep di codice committato; nessuna esecuzione contro DAPI richiesta per la review della **metodologia**). NB sotto-asserzioni che richiedono prova DAPI live (non attese in questo CAP perché i prerequisiti empirici V-1/V-2/T+1 sono già chiusi nei dump committati come livello-1) vanno marcate "Empirico-CLI" dal Web Reviewer e lasciate come handoff alla sede CLI in una sessione separata. Questa sessione di Planner gira su CLI locale, ma la sede effettiva del Reviewer la decide l'Orchestratore a valle del Developer in base a quanto resterà come asserzione non risolvibile per documento + grep.

---

## Obiettivo

Parte 10 (= CAP-DATA-03) chiude il versante "ciclo di vita del tape" della convenzione dati del progetto, raccogliendo i 4 temi rinviati esplicitamente da Parte 9 Cap.55 ("Continuita' tape, recupero gap, riconciliazione canonica giornaliera, storicizzazione strutturata — CAP-DATA-03 / Parte 10"). Parte 9 ha formalizzato il **canale runtime DAPI** (architettura, schemi, mappatura `bar_synthetic`, errori, warm-up ≤30gg dentro la finestra 100gg, sessione 08:00-22:00 CET, audit log, retention); Parte 10 formalizza **cosa fa la pipeline quando il tape runtime ha discontinuità** (gap di sessione, restart, finestre fuori dai 100gg intraday), **come si verifica giornalmente** che il tape runtime sia coerente con la serie ufficiale di training (Parte 8), e **come si archivia strutturalmente** il flusso DAPI per coerenza inter-temporale e per ricostruzione futura.

Parte 10 risponde a quattro domande operative concrete, in ordine:
1. **Continuità tape**: dato un tape DAPI runtime con buchi (gap di sessione tra giorni, riavvio Darwin notturno, conflitto DGo, gap intra-sessione), come si compone una griglia 1-min coerente sul piano semantico con il preprocessor di Parte 8 Cap.40?
2. **Recupero gap**: per gap di durata ≤100gg di calendario, quale procedura `CANDLERANGE` su porta 10003 ricostruisce le barre mancanti, con quali marker di provenienza e quali criteri di idempotenza? Per gap >100gg, quale fallback all'archivio Portara, con quale criterio di coerenza con la serie ratio-adjusted di Parte 8 Cap.38?
3. **Riconciliazione canonica giornaliera**: ogni end-of-day, come si verifica che il tape DAPI runtime del giorno $d$ sia coerente con la fonte di training Portara, e come si gestisce la discrepanza nota del **low del cash rado** (DITAS feed PRICE ~6 tick/min perde i minimi intraday — vedi probe §2.4)?
4. **Storicizzazione strutturata**: come la tape runtime confluisce in un archivio canonico (formato, manifest, immutabilità, versioning, integrazione con `exports/` esistente) coerente con la convenzione storica di Parte 8 Cap.37-40 e con i 391 dump live + 256 archeologici già presenti in `exports/directa_history/`?

NON risponde a: ri-apertura schema CANDLE (chiuso `C;L;H;O` in AUDIT-RM-RETRO PASS); ri-apertura policy switch front-month (chiusa D-9-NB2 in Parte 9 Cap.47); ri-apertura warm-up ≤30gg/limite 100gg (chiusa D-9-NB4 in Parte 9 Cap.51 e Cap.55 perché il caso ≤100gg è coperto dal warm-up Cap.51 stesso, qui si tratta SOLO il caso >100gg con fallback Portara e il **gap intermedio nella finestra ≤100gg recuperabile via CANDLERANGE strutturato**); audit log e retention (chiusi D-9-15 in Parte 9 Cap.54 e Gap-4); audit ANAG/BOOK_5 codici mese (chiusi in AUDIT-RM-RETRO CAP-DATA-02 CLI); implementazione codice operativo (FASE-D del roadmap, dichiarato fuori scope da Parte 9 Cap.55 ultima riga); Telegram / latenza M-2 (dichiarato esplicitamente fuori perimetro: DAPI ≠ Telegram).

Parte 10 si fa adesso perché:
- Tutti i **prerequisiti empirici** sono completi e committati come livello-1 in `tasks/PROBE_RECUPERO_GAP_DAPI.md` (V-1 morning + afternoon equivalenza realtime↔CANDLERANGE su schema `C;L;H;O` 55/60+49/13 match, V-2 cut-off `~100gg intraday / nessun limite daily`, T+1=T+3 immutabilità barre 60/60 identiche su finestre morning) con self-review RM-4 opzione A approvata e gatekeeping Orchestratore PASS;
- Tutti i **prerequisiti normativi** sono congelati: Parte 8 (convenzione storica, ratio-adjusted, filtro pre-expiry, preprocessor griglia 1-min, sanity validation Cap.43), Parte 9 (canale runtime DAPI, mappatura schema, marker, warm-up, audit);
- Il **debito RM** retroattivo su Parte 8 e Parte 9 è chiuso (CAP-DATA-01 PASS, CAP-DATA-02 RM-RETRO PASS WEB+CLI), quindi le fondamenta su cui Parte 10 si appoggia sono RM-compliant e non vanno ri-auditate dentro questo CAP.

L'impatto sul GA è diretto e identificabile (orientamento al GA — regola fondamentale del Planner):
- **Ranking dei cromosomi e fitness**: il bundle frozen calibrato in Parte V opera in inference su una griglia 1-min runtime che, se ha gap non-conciliati o `bar_synthetic` non propagati simmetricamente, produce feature contaminate (volatilità EGARCH su barre fittizie, regime intraday mis-classificato per dati assenti, pivot strutturali instabili). Parte 10 garantisce che il **tape che alimenta l'inference live sia metricamente lo stesso del tape di training** (invariante research = runtime esteso al ciclo di vita del tape, non solo allo schema della barra come in Parte 9 Cap.49).
- **Conversione signal-to-trade**: la riconciliazione canonica giornaliera produce un **gate operativo** che, se fallisce, marca la sessione come degraded e blocca emissioni per il giorno successivo finché il supervisore non interviene — è una protezione contro la deriva silenziosa del feed che altrimenti contaminerebbe i segnali. Direttamente analogo al gate Parte VI Cap.30 sul Brier $f_5^{live}$.
- **Validità delle metriche live**: la storicizzazione strutturata del flusso DAPI permette di ricostruire post-hoc il replay deterministico bit-exact (Parte II Cap.10) anche dopo restart >100gg, evitando di marcare come "n/a" intervalli per i quali il dato è recuperabile dall'archivio locale.

---

## Eredità obbligatoria

### Da `tasks/METODO.md` — regole metodologiche permanenti (vincolanti per Developer e Reviewer di questo task)

1. **RM-1 — formato 4-righe**. Ogni asserzione del documento del tipo "verificato / confermato / fatto" deve essere accompagnata dal blocco `VERIFICA / PROVE / ALTERNATIVE COMPATIBILI ESCLUSE / ALTERNATIVE COMPATIBILI NON ESCLUSE` (`METODO.md:28-33`). Le asserzioni di Parte 10 che ricadono sotto RM-1 sono prevalentemente: (a) la composizione delle barre `bar_synthetic` cross-gap (semantica e simmetria training/runtime); (b) il limite ~100gg intraday di `CANDLERANGE` come finestra scorrevole (già provato in V-2); (c) l'immutabilità delle barre intraday CANDLERANGE entro T+3 morning (già provato in T+1); (d) il low rado del cash DITAS come limite del feed PRICE (già provato in V-1 afternoon). Per (b)/(c)/(d) le prove sono nei dump V-1/V-2/T+1: il Developer deve **citare** i dump per nome + il numero esatto dal probe (es. 60/60, 55/60, 49/62) + il **limite di validità onesto** dichiarato dal probe stesso (es. T+1 non oltre T+3, immutabilità solo su barre morning FIB6F/DITAS, non testato afternoon/usopen).
2. **RM-2 — grep nel repo prima di assumere format esterno** (`METODO.md:46-94`). Il Developer DEVE eseguire `grep -rn` su pattern del dominio prima di scrivere capitoli che toccano parsing/strutture esistenti, e citare i decoder esistenti con `[CODICE-ESISTENTE <path>:<linea>]`. Decoder noti rilevanti per Parte 10:
   - `scripts/export_directa_history_parametric.py:467-481` — `parse_directa_candle`, schema CANDLE canonico `C;L;H;O` (`UFF;MIN;MAX;APE`).
   - `scripts/export_directa_history_parametric.py:228-230` — sintassi `CANDLERANGE <sym> <yyyyMMddHHmmss_start> <yyyyMMddHHmmss_end> <period_s>` (period in ultima posizione).
   - `scripts/export_directa_history_parametric.py:245,282-285,437` — terminatore `END CANDLES` (RM-2 da CAP-DATA-01 W2/W3/W7).
   - `scripts/export_directa_history_parametric.py:61` — `DEFAULT_INTRADAY_MAX_DAYS=100` (limite costante codice).
   - `scripts/export_directa_history_parametric.py:119-122` — header CSV legacy (output `O;H;L;C;V` con label semantiche).
   - `scripts/probe_dapi.py:230` — `parse_line` post-rettifica `C;L;H;O` (`a12ae32`).
   - `scripts/probe_dapi.py:159,333` — `DapiConn` connessione persistente / `run_candlerange`.

   Pattern da grep aggiuntivi che il Developer DEVE eseguire prima della stesura: `grep -rn "manifest|bar_synthetic|RUNTIME_GAP|AGG_FROM_60s|AGG_FROM_D|forward.fill|reconcile|sanity"` su `scripts/`, `docs/`, `tasks/` per non re-inventare convenzioni esistenti. Risultato del grep va dichiarato nella sezione "Decoder/convenzioni esistenti nel repo letti prima della stesura" del REPORT_CAP_10.md.

3. **RM-3 — ordine priorità fonti `1>2>3>4`** (`METODO.md:97-136`). Etichette obbligatorie per ogni citazione. Il wiki Directa è **dimostrato inesatto** sullo schema CANDLE e va trattato come hint anche per i temi di Parte 10. Concretamente, sulle quattro classi di asserzioni di Parte 10:
   - **Limite ~100gg intraday CANDLERANGE**: `[PROVA-EMPIRICA 2026-05-29 V-2 dump probe_out/v2_cutoff_period60_20260529_104927.csv]` livello-1 + `[CODICE-EXISTENTE export_directa_history_parametric.py:61]` livello-2.
   - **Nessun limite intra-day sul daily CANDLERANGE**: `[PROVA-EMPIRICA 2026-05-29 V-2 dump probe_out/v2_cutoff_period86400_20260529_105739.csv]` livello-1.
   - **Immutabilità barre CANDLERANGE T+0/T+3 morning**: `[PROVA-EMPIRICA 2026-05-29+2026-06-01 T+1 dump probe_out/v1_hist_20260529_fetched_*_*.csv]` livello-1, **limite onesto T+3 morning only**.
   - **Riavvio Darwin mezzanotte**: già etichettato `[WIKI-HINT, da verificare]` in Parte 9 Cap.50 Gap-3 (Empirico-CLI residuo, sessione notturna non eseguita). Parte 10 EREDITA quel `WIKI-HINT` e NON lo solleva: si appoggia al marker `RUNTIME_GAP_*` già normato in Parte 9.
   - **Feed cash rado low**: `[PROVA-EMPIRICA 2026-06-01 V-1 afternoon §2.4.5 lettera A]` livello-1 (6/6 mismatch DITAS sul solo `low`).

4. **RM-4 — review esplicita per output non-CAP determinanti**. Parte 10 è un CAP-XX, quindi rientra nel workflow Planner→Developer→Reviewer standard. NON sono attesi output non-CAP collaterali (probe nuovi, decoder nuovi, handoff fra sessioni). Se il Developer dovesse scoprire la necessità di un probe empirico aggiuntivo (es. per disambiguare un caso di gestione gap), DEVE fermarsi e segnalare al Planner via Q-XX in QUESTIONS.md, **non** eseguirlo dentro questo task.

### Da AUDIT-RM-RETRO CAP-DATA-02 (chiusura WEB+CLI) — fatti livello-1/2 **AUTORITATIVI** per Parte 10 (NON ri-verificare, USA come HARD CONSTRAINT)

5. **Schema CANDLE canonico `C;L;H;O;V`** (= `UFF;MIN;MAX;APE;V`). Tutti i CSV di output usano convenzione `O;H;L;C;V` con header esplicito semantico (`bar_open` riceve `ape` = pos.8 del payload wire; `bar_close` riceve `uff` = pos.5 del payload wire). I dump storici sono integri: 391 dump live in `C:\Users\AN\Documents\Projects\ga-zone-engine\exports\directa_history\` + 256 archeologici in `C:\directa_history_parametric_export_overlay\` + 15 anni daily `DITAS_20110404_20260402` sono **tutti corretti, nessuna rigenerazione**. Parte 10 NON tocca lo schema, lo USA. (Fonte: `CAP_09_parte_9.md:155-191` Cap.49 tabella canonica post-AUDIT; `scripts/export_directa_history_parametric.py:477-481`; `tasks/PROBE_RECUPERO_GAP_DAPI.md` §3 + §7.)

6. **CANDLERANGE intraday — limite ~100gg di calendario, finestra scorrevole**, tronca al **minuto esatto** del limite (NON al giorno intero). Verificato V-2 period 60 su FIB6F+DITAS+CM.MESM6 (saturazione a `first_ts=2026-02-18 09:56`, identica e simultanea sui 3 ticker, costante da N=80 a N=160). Implicazione che Parte 10 deve assorbire: il **gap intra-sessione** ≤100gg è recuperabile via `CANDLERANGE` strutturato; il gap >100gg richiede fallback all'archivio locale (`exports/` + overlay) o, in subordine, all'archivio Portara. (Fonte: probe §4.2.)

7. **CANDLERANGE daily (period 86400) — nessun limite pratico** osservato fino a N=160gg (first_ts continua a regredire, a N=160 arriva al 2026-01-05). La storia profonda pluriennale è recuperabile a livello Daily, coerente con `DITAS_20110404_20260402` (15 anni daily). Implicazione che Parte 10 deve assorbire: la **riconciliazione canonica giornaliera** può attingere a daily DAPI per gap lunghi senza dipendenza da Portara, ma SOLO al livello daily (la ricostruzione intraday post-100gg resta fuori dal canale DAPI). (Fonte: probe §4.3.)

8. **Equivalenza realtime↔CANDLERANGE confermata su 2 finestre indipendenti** (morning 09:00-09:30, afternoon 14:55-15:25). Schema regge, nessuno swap O/C, mismatch tutti spiegati (primo minuto SUB-troncato + scarto 1 tick confine minuto + feed cash rado sul low). Implicazione che Parte 10 deve assorbire: il **recupero gap via CANDLERANGE** è metricamente equivalente al tape realtime (no path-inference, no distorsione di volatilità) → la ricostruzione di un gap con `CANDLERANGE` produce barre `bar_synthetic=False` indistinguibili da quelle che il realtime avrebbe prodotto, **a eccezione del low del cash rado**, vedi punto 10. (Fonte: probe §2.3 + §2.4.)

9. **Immutabilità barre intraday CANDLERANGE — verificata fino a T+3 morning** (re-fetch del 29/05 eseguito il 01/06, attraversando weekend, 60/60 barre OHLCV bit-identiche). Implicazione che Parte 10 deve assorbire: la **storicizzazione strutturata** può trattare le barre CANDLERANGE come **immutabili** entro l'orizzonte ≤T+3 morning per uso operativo (idempotenza del recupero gap, no riscrittura archivio per cambi notturni). **Limite onesto da dichiarare nel CAP**: non testato oltre T+3, non testato su finestre afternoon/usopen (erano future al fetch T+0), non testato su strumenti diversi da FIB6F/DITAS. Parte 10 deve normare il caso "T+3 morning" come **regola operativa con perimetro empirico esplicito**, non come "fatto universale". (Fonte: probe §2.5.)

10. **Feed cash realtime rado** (~6 tick/min su DITAS): il flusso PRICE perde i minimi intraday del cash; sulla CANDLE ufficiale daily il low è corretto. Implicazione che Parte 10 deve assorbire: la riconciliazione canonica giornaliera per i ticker cash europei (DGER/DSTX50/DITAS/DFRA — gating qualitativo Cap.53) DEVE usare la CANDLE ufficiale come fonte del low/high del giorno, NON l'aggregato dei tick realtime. (Fonte: probe §2.4.5 lettera A — 6/6 mismatch DITAS sul solo low.)

### Da Parte 9 (CAP-DATA-02) — marker, dominio source, fallback già normati (NON re-inventare, AGGANCIA)

11. **Marker già definiti in Parte 9 Cap.50/Cap.51/Cap.52/Cap.54** che Parte 10 USA come vocabolario normativo: `RUNTIME_GAP_START`/`RUNTIME_GAP_END` (gap intra-sessione/cross-midnight), `RUNTIME_DEGRADED` (conflitto DGo/TradingView), `RUNTIME_STALE_RESTART` (downtime >100gg), `CONTRACT_SWITCH` (rollover front-month), `WARMUP_COMPLETE` (fine warm-up boot), `SESSION_OPEN`/`SESSION_CLOSE` (apertura/chiusura sessione 08:00-22:00 CET). Parte 10 NON introduce marker concorrenti; introduce eventualmente marker **complementari** specifici alla riconciliazione e alla storicizzazione (es. `RECONCILE_OK`/`RECONCILE_DIVERGENT`, `ARCHIVE_WRITTEN`, `BACKFILL_FROM_CANDLERANGE`/`BACKFILL_FROM_ARCHIVE`/`BACKFILL_FROM_PORTARA`), con definizione esplicita e tabella decisioni in Cap.65.

12. **Dominio chiuso `source ∈ {DIRECTA, AGG_FROM_60s, AGG_FROM_D}`** (Parte 9 Cap.48 + D-9-5). Parte 10 può **estendere** il dominio con eventuali nuovi marker di provenienza per il recupero gap (es. `BACKFILL_CANDLERANGE`, `BACKFILL_ARCHIVE`, `BACKFILL_PORTARA`), ma DEVE giustificare ogni nuovo valore come decisione normativa esplicita in Cap.65 (tabella decisioni) e dichiarare se è sostituto, sub-categoria o complemento del dominio Cap.48.

13. **Warm-up congelato `L_warmup=30gg di trading IDEM`** (D-9-NB4 in Parte 9 Cap.51 e Cap.56). Parte 10 NON tocca il warm-up al boot (è il **caso nominale** ≤100gg coperto da Parte 9 Cap.51 procedura 1-5). Parte 10 tratta:
    - gap intra-sessione (es. perdita feed temporanea dentro la sessione 08:00-22:00 CET): recupero `CANDLERANGE` su porta 10003 della finestra mancante, immutabilità T+3 morning, marker `RUNTIME_GAP_END` + `BACKFILL_FROM_CANDLERANGE`;
    - gap cross-midnight (riavvio Darwin gestito da Parte 9 Cap.50 procedura 1-7): Parte 10 documenta la **riconciliazione end-of-day** che chiude il loop del riavvio (verifica che le barre della sessione $d$ riprese post-restart siano coerenti con quelle attese dalla finestra di sessione completa);
    - restart >100gg `RUNTIME_STALE_RESTART` (rinviato da Parte 9 Cap.51 r261): Parte 10 norma la **procedura di re-bootstrap** dopo downtime >100gg, con fallback strutturato all'archivio locale `exports/` + overlay o all'archivio Portara, e con vincolo di **coerenza ratio-adjusted** rispetto a Parte 8 Cap.38.

14. **Invariante research = runtime applicato all'adapter** (Parte 9 Cap.45/Cap.49 + Parte 8 Cap.37). Parte 10 ESTENDE l'invariante dal singolo bar all'**intero ciclo di vita del tape**: dopo recupero gap / riconciliazione / storicizzazione, le barre archiviate hanno gli **stessi metadati** del tape di training Portara (header CSV BOM UTF-8 con `tick_count` e `bar_synthetic`, dominio `source`, regola forward-fill, regola pivot-touch su `bar_synthetic`), così che il replay deterministico bit-exact (Parte II Cap.10 + Parte VII Cap.31) sia preservato anche dopo backfill.

15. **Tabella decisioni Parte 9 Cap.56** (17 decisioni D-9-1..D-9-17 + D-9-NB2/NB3/NB4): Parte 10 NON apre nessuna delle decisioni esistenti. Eventuali nuove decisioni di Parte 10 vivono nella tabella propria di Cap.65 (numerazione D-10-1..D-10-N), con criterio di rollback registrato.

### Da Parte 8 (CAP-08) — convenzione storica e sanity validation (vincolo strutturale)

16. **Serie ufficiale di training = FIB pieno back-adjusted Portara/CQG ratio-adjusted** (Parte 8 Cap.37 + Cap.38). Parte 10 conferma che il tape DAPI runtime archiviato **NON è fonte di training** (vincolo invariato D-9 ed eredità Parte 8 Cap.44). La storicizzazione strutturata di Parte 10 produce un archivio canonico per **riconciliazione e replay**, NON per re-training. L'apertura del flusso DAPI come fonte di training richiederebbe nuovo task Planner con riesame Cap.38 (back-adjustment ratio-adjusted ricostruzione da `UnadjustedClose+RollSpread`) e Cap.39 (filtro pre-expiry $N=3$). Parte 10 lo dichiara fuori scope esplicitamente (carryover Parte 9 Cap.55 invariato).

17. **Procedura di sanity validation Parte 8 Cap.43**: confronto ratio-adjusted vs unadjusted-stitched su ultimi 18-24 mesi, metriche (quantili rendimenti log 1/5/60-min, autocorrelazione rendimenti e rendimenti quadrati, $\sigma$ giornaliera realized), criterio $3\sigma$ bootstrap $B=2000$ con block length Politis-White (Parte VII Cap.34). Parte 10 NON ri-definisce questa procedura ma la USA come **template** per la riconciliazione canonica giornaliera: la riconciliazione end-of-day di Parte 10 è una **versione runtime, su scala giornaliera, del sanity check storico di Cap.43**. La differenza: Cap.43 è procedura **una-tantum** all'acquisizione dati Portara, Parte 10 è **gate operativo giornaliero** sul tape DAPI runtime; la struttura delle metriche è la stessa, la finestra è 1 giorno invece che 18-24 mesi, e la soglia di accettazione è da definire come parametro provvisorio di lavoro non congelato (vedi Done when domanda d3).

18. **Preprocessor griglia 1-min Parte 8 Cap.40 + flag `bar_synthetic`** (D-9-7 simmetria runtime/training). Parte 10 conferma che il forward-fill su Close per minuti senza trade + flag `bar_synthetic=True` con `Volume=0` `tick_count=0` e regola "nessun touch su barre sintetiche" (Parte 8 Cap.40 r92-96; Parte 9 Cap.49 r173-180) è **invariante operativo** per ogni barra ricostruita dal backfill di Parte 10. La storicizzazione produce barre con la stessa semantica: il consumer a valle (feature engineering Parte III Cap.15, EGARCH Parte III Cap.13) non distingue una barra ricostruita via backfill da una barra reale del tape (eccetto per il campo `source` che traccia la provenienza).

### Da `tasks/CARRYOVER.md` — M-promemoria attivi (censimento Planner, regola operativa)

Censimento completo dei M-promemoria aperti, con assegnazione esplicita a Parte 10 o rinvio motivato:

19. **M-2** (Review v1 CAP-02): "Verifica empirica latenza Telegram ($L_{max}=30$s)" → destinazione `Appendice E`. **FUORI SCOPE Parte 10**: tratta canale Telegram, NON canale DAPI. Parte 9 Cap.55 lo conferma esplicitamente come carryover ad Appendice E. **Rinvio motivato**: Parte 10 (DAPI tape lifecycle) e Appendice E (Telegram bot) sono perimetri disgiunti; M-2 sarà ripreso nella sessione di Appendice E quando il Planner aprirà quel capitolo, atteso in coda al consolidamento delle Appendici. Stato in CARRYOVER: `OPEN` invariato.

20. **M-2 v2 CAP-03** (Review v2 CAP-03): "Cadenza ricalibrazione EGARCH" → destinazione Parte V/VI. **Stato `CLOSED-CAP-06 completo`** (CARRYOVER riga 27): già chiuso in Cap.25.9 + Cap.27.5 + Cap.30.4. NON pertinente a Parte 10.

21. **M-1 v2 CAP-03** (Review v2 CAP-03): "Pivot all'inizio/fine sessione non confermabili" → destinazione Parte VI. **Stato `CLOSED-CAP-04`** (CARRYOVER riga 26). NON pertinente a Parte 10.

22. **M-4, M-5, M-6, M-7, M-8, M-9, M-10, M-11, M-12, M-13, M-14, M-15**: tutti `CLOSED-CAP-04/05/07`. NON pertinenti a Parte 10. (Verificato leggendo CARRYOVER.md righe 22-37.)

23. **M-16 condizionale** (Review v1 CAP-05): Cox time-varying coefficients in Parte VII. **Stato `CLOSED-CAP-07 con condizione operativa`** (Cap.31.3 + metadato bundle `cox_time_varying_active`). NON pertinente a Parte 10.

24. **Conclusione censimento M-promemoria** (regola operativa del Planner): **nessun M-promemoria aperto è pertinente al perimetro di Parte 10**. M-2 (Telegram) è esplicitamente fuori scope per natura del canale. Nessun M-promemoria attraversa la soglia "3 task senza integrazione" che richiederebbe sollevamento al supervisore.

25. **RACC-METODO-1** (Re-Review v3 FONDAMENTA-01): "de-numerizzare rimandi residui in `reviewer.md`/`METODO.md`" → raccomandazione di processo metodologico, NON di capitolo. **Stato `OPEN`**, fuori scope Parte 10. NON da integrare qui (è manutenzione del processo, non del documento metodologico v2).

26. **RACC-METODO-2** (Re-Review v2 CAP-DATA-02 RM-RETRO, finding #8): "AC su schemi-dato esterni devono includere diff col decoder canonico" → raccomandazione di processo. **Stato `OPEN`**. **Parziale impatto su Parte 10**: il Reviewer di Parte 10, se gli AC del capitolo dichiarano "schema X coerente con DAPI / con Portara", DOVREBBE confrontare con il decoder canonico prima di scrivere "OK". Il Planner NON include questo come requisito hard del task (è una raccomandazione di processo già da applicare per default dopo CAP-DATA-02 RM-RETRO), ma lo segnala al Reviewer nel prompt di invocazione futura.

### Da `tasks/STATO_CORRENTE.md` §5 — M-promemoria di sessione (non capitolo, **input critico per Developer di Parte 10**)

Sono note tecniche di sessione, livello-1 [PROVA-EMPIRICA]. Diversi sono **direttamente rilevanti** per il Developer di Parte 10 e devono essere citati esplicitamente come riferimenti `[PROVA-EMPIRICA <data>]`:

27. **M-1 (sessione)**: schema CANDLE `C;L;H;O;V`. Già assorbito in eredità #5. Citazione obbligatoria nel CAP-10 ogni volta che la mappatura schema è richiamata.

28. **M-2 (sessione)**: sintassi `CANDLERANGE <sym> <yyyyMMddHHmmss_start> <yyyyMMddHHmmss_end> <period_s>` (4 arg, period ultimo). Già normata in Parte 9 Cap.48 r144 e Cap.51 r254. Parte 10 la USA per il recupero gap; citazione `[CODICE-EXISTENTE export_directa_history_parametric.py:228-230]`.

29. **M-3 (sessione)**: codici errore 1004/1007/1017/1015/1003 ri-auditati [PROVA-EMPIRICA 2026-05-29 + ri-confermato 2026-06-01 CLI]. 1030 non riprodotto sul FIB (servizio base IDEM). Già normati in Parte 9 Cap.50. Parte 10 li USA come **codici di trigger del marker `RUNTIME_GAP_END` / `BACKFILL_*`** quando il backfill CANDLERANGE risponde con errore.

30. **M-4 (sessione)**: F=Giugno, I=Settembre confermati [PROVA-EMPIRICA]; Mar/Dic residuo Empirico-CLI. Già normato in Parte 9 Cap.47 r96 + Cap.55. NON pertinente al perimetro Parte 10 (rollover front-month è D-9-NB2 chiuso). Parte 10 lo cita solo se richiama esplicitamente il rollover come trigger di gap potenziale.

31. **M-5 (sessione)**: cooldown "14/~30s" refutato a ~907Hz/850 conn (0 onset). Già ri-caratterizzato in Parte 9 Cap.46 r47-53 e Cap.50 r218. NON pertinente al perimetro Parte 10 (recupero gap usa connessione persistente per backoff, non burst).

32. **M-9 (sessione)**: schema PRICE realtime [PROVA-EMPIRICA 2026-06-01 W2]: `f4=last`, `f6=volume_cum`, `f8=day_low`, `f9=day_high`; `f5`/`f7` parziali. Già normato in Parte 9 Cap.47 r91-94 post-AUDIT. Parte 10 lo USA nella **regola di derivazione del low/high del cash europeo per riconciliazione canonica**: per i cash europei la riconciliazione canonica giornaliera (es. low di giornata di DITAS) si appoggia su `f8`/`f9` della CANDLE ufficiale (level-2 verificato cross-check `[PROVA-EMPIRICA W2]`), NON sull'aggregato dei tick realtime (rado, vedi punto 10 di Eredità).

33. **M-10 (sessione)**: schema BOOK_5 certificato [PROVA-EMPIRICA 2026-06-01 W3]: `[BID×5 best-first][ASK×5 best-first]`, triplo `(lots,orders,price)`; `bid1_lots/ask1_lots/bid1_price` per `bar_synthetic` Cap.49 CERTIFICATE. Anomalia 27/05 spiegata come artefatto del campione. Parte 10 NON tocca BOOK_5 (il backfill è via CANDLERANGE, non via book replay). Riferimento citato solo come supporto per "schema runtime certificato post-AUDIT".

### Da `.claude/CLAUDE.md` — workflow di sessione (vincoli organizzativi)

34. **Workflow Planner→Developer→Reviewer pieno** (CAP-XX nuovo): Developer produce v1 di `CAP_10_parte_10.md` + `REPORT_CAP_10.md` + update `00_indice.md` (Parte 10 da assente a "IN CORSO" durante stesura, a "IN REVIEW" al `READY_FOR_REVIEW`). Orchestratore esegue check post-Developer (6 condizioni). Reviewer Web esegue review piena con classificazione finding per supervisore. Punto di controllo supervisore su CONDITIONAL/FAIL standard.

35. **Push policy** (MEMORY `push_policy`): push diretto a `origin/main` autorizzato per Developer/Reviewer.

36. **Sub-agente registry web** (MEMORY `subagent_registry_web`): in sessione web solo `planner` è esposto come `subagent_type`; Developer/Reviewer vanno via `general-purpose` adottando il proprio `.md`. Questa è una sessione **CLI locale** (autocheck Orchestratore), quindi la nota subagent web NON si applica direttamente alla sessione corrente; si applicherà quando l'Orchestratore della prossima sessione (Developer di CAP-DATA-03) eseguirà il task — ma se quella sessione sarà web (matrice METODO.md §RM-4 raccomanda Web per CAP-XX), allora la nota si applicherà.

37. **DGo aperto / TradingView chiuso per probe DAPI** (MEMORY `feedback_no_dapi_probe_con_dgo_aperto`): NON pertinente a Parte 10 (è documento metodologico, non probe). Citato solo per completezza dell'eredità organizzativa.

---

## Perimetro dei file (cosa il Developer produce e modifica)

Il Developer di Parte 10 produce/modifica **esclusivamente**:

| Path assoluto | Operazione | Note |
|---|---|---|
| `docs/methodology_v2/CAP_10_parte_10.md` | **CREATE** (file nuovo) | Capitolo metodologico Parte 10, ~9-12 pp totali, scaletta Cap.57-Cap.65 (vedi sezione successiva). Naming β2 ratificato: `CAP_10_parte_10.md`, identifier interno "Parte 10" (arabo), coerente con Parte 8/9. |
| `reports/REPORT_CAP_10.md` | **CREATE** (file nuovo) | Report supervisore con 5 sezioni standard: "Cosa è stato prodotto", "Ipotesi di partenza", "Decisioni rilevanti", "Misura prima/dopo", "Domande aperte" + "Criterio di rollback" + "Verifica esplicita degli AC". Include sezione "Decoder/convenzioni esistenti nel repo letti prima della stesura" (RM-2 grep documentato). |
| `docs/methodology_v2/00_indice.md` | **EDIT** | Aggiungere voce "Parte 10 — Continuità tape, recupero gap, riconciliazione canonica, storicizzazione strutturata (~9-12 pp)" con stato "IN CORSO" durante stesura, "IN REVIEW" al `READY_FOR_REVIEW`, "PASS Review v$N$ (review commit `<sha>` del <data>; documento commit `<sha>`)" alla chiusura PASS. Mantenere stile delle voci precedenti (Parte 8/9). |
| `tasks/DEV_STATUS.md` | **EDIT** | Scrivere `READY_FOR_REVIEW` al completamento v1; azzerato dall'Orchestratore a ogni nuovo ciclo. |

**Fuori perimetro (NON toccare in v1)**:
- `tasks/ACTIVE_TASK.md` (questo task card) — il Developer NON lo modifica; le eventuali "Finding di Review da risolvere" le aggiunge l'Orchestratore dopo il punto di controllo supervisore;
- `tasks/CARRYOVER.md` — il Developer aggiunge eventuali nuovi M-promemoria SOLO se la Review li solleva e il supervisore li ratifica (mai prima di PASS);
- `tasks/STATO_CORRENTE.md` — single-writer per disciplina; aggiornato in chiusura sessione dall'Orchestratore;
- `tasks/METODO.md` — NON si modifica nel ciclo CAP-XX; le RM si aggiungono solo per incidente con commit dedicato `[METODO]`;
- `scripts/*` — Parte 10 è metodologia, NON implementazione. Il decoder canonico `export_directa_history_parametric.py` è citato come `[CODICE-EXISTENTE]`, NON modificato;
- `docs/methodology_v2/CAP_08_parte_8.md`, `CAP_09_parte_9.md` — i capitoli precedenti sono PASS storici, NON si riapre nulla;
- `data/sessions/fib_session_calendar.csv`, `data/runtime/exports_sample/*` — file normativi/sample, NON toccati da Parte 10;
- `reviews/*` — il Developer NON produce review (lo fa il Reviewer);
- `probe_out/*` — dump empirici gitignored, NON modificati né riprodotti dal Developer (il task è di sola redazione documentale a partire dai dump già esistenti, identico schema del task PROBE §2.4-§2.5 vincolo rispettato).

---

## Scaletta capitoli proposta (~9-12 pp totali, Cap.57-Cap.65)

L'ultimo capitolo di Parte 9 è Cap.56 (tabella decisioni). Parte 10 parte da **Cap.57**.

### Cap.57 — Premessa e collocazione (~1 pp)
Cosa formalizza Parte 10, relazione con Parte 8 (convenzione storica) e Parte 9 (canale runtime), invariante research = runtime esteso al ciclo di vita del tape (non solo al singolo bar di Cap.49). Distinzione esplicita rispetto a quanto già normato (Parte 9 Cap.51 warm-up nominale, Cap.50 riavvio mezzanotte, Cap.54 audit log): Parte 10 si occupa del comportamento del tape **fuori dal flusso nominale**. Sintesi delle 4 domande operative (continuità, recupero, riconciliazione, storicizzazione). Riferimento esplicito a Parte 9 Cap.55 rinvio originale.

### Cap.58 — Continuità tape: definizione e tassonomia dei gap (~1-1.5 pp)
Definizione formale di "gap" sul tape runtime: intervallo $[t_{start}, t_{end}]$ contiguo di barre 1-min mancanti (o con `bar_synthetic=True` ma senza forward-fill semantico valido). Tassonomia normativa dei gap con riferimento ai marker Parte 9 già definiti:
- **Gap intra-sessione**: intervallo entro `[SESSION_OPEN, SESSION_CLOSE]` con `RUNTIME_GAP_START`/`RUNTIME_GAP_END` (cause: perdita feed transitoria, conflitto DGo brevemente risolto, hiccup TCP). Durata tipica minuti-ore.
- **Gap cross-midnight**: causato da riavvio Darwin (Parte 9 Cap.50 procedura 1-7). Durata tipica 1-5 minuti, sempre prima di `SESSION_OPEN` del giorno successivo (fuori sessione, basso impatto operativo).
- **Gap cross-session**: tape mancante per ≥1 sessione completa (es. server-side outage prolungato). Durata tipica 1-N giorni di trading, dentro la finestra 100gg.
- **Gap fuori finestra DAPI (>100gg)**: `RUNTIME_STALE_RESTART` (Parte 9 Cap.51 r261). Durata tipica >100gg di calendario. Richiede procedura speciale (Cap.61).

Sezione "Composizione semantica della griglia": ogni tipo di gap, una volta colmato dal backfill di Cap.59-Cap.61, deve produrre una sequenza di barre **identica per schema** a quella che il tape nominale avrebbe prodotto, con propagazione del `bar_synthetic` simmetrica al training (Parte 8 Cap.40, Parte 9 Cap.49 r173-180). Distinzione esplicita: una barra ricostruita via backfill con dato reale dal gateway è `bar_synthetic=False`, NON `True` (anche se cronologicamente "ricostruita post-hoc"); il flag `bar_synthetic` resta booleano "trade vs no-trade", mai "live vs ricostruito". La provenienza è tracciata dal campo `source` (Cap.62), non dal flag.

### Cap.59 — Recupero gap entro la finestra 100gg (~1.5 pp)
Procedura normativa per il recupero gap di durata ≤ ~100gg di calendario (entro il limite scorrevole `CANDLERANGE` intraday `[PROVA-EMPIRICA 2026-05-29 V-2 dump probe_out/v2_cutoff_period60_20260529_104927.csv]`). Algoritmo formale (numerato):

1. Identificazione del gap: rilevazione automatica via gap detector sulla griglia 1-min (timestamp mancanti tra `RUNTIME_GAP_START` e `RUNTIME_GAP_END`, oppure rilevati post-hoc nel ciclo di riconciliazione di Cap.60).
2. Richiesta `CANDLERANGE` su porta 10003 (storico, già normata Parte 9 Cap.48/Cap.51): sintassi `CANDLERANGE <ticker_front_month> <YYYYMMDDHHMMSS_start> <YYYYMMDDHHMMSS_end> 60` `[CODICE-EXISTENTE export_directa_history_parametric.py:228-230]`.
3. Decodifica risposta con schema canonico `C;L;H;O;V` `[CODICE-EXISTENTE export_directa_history_parametric.py:467-481]`.
4. Validazione idempotenza: confronto barre ricevute con barre già presenti nel tape (eventualmente già archiviate); regola di **idempotenza T+3 morning** `[PROVA-EMPIRICA T+1 dump probe_out/v1_hist_*]` — per finestre intraday entro T+3 morning sui ticker FIB6F/DITAS testati, le barre CANDLERANGE sono bit-identiche tra fetch successivi (60/60 verificato). Limite di validità onesto da dichiarare: oltre T+3 e per finestre afternoon/usopen e altri strumenti non testato, marker `BACKFILL_VERIFIED_T3` solo se la finestra rientra nell'orizzonte empirico; altrimenti `BACKFILL_UNVERIFIED` con flag operativo che richiede check di riconciliazione di Cap.60.
5. Inserimento barre ricostruite nella griglia 1-min con campo `source = BACKFILL_FROM_CANDLERANGE` (nuovo valore del dominio, vedi Cap.62), `bar_synthetic` derivato dalla regola Parte 9 Cap.49 (presenza/assenza minuto nella risposta CANDLE), `tick_count = NULL` (regime storico, Parte 9 Cap.49 r172).
6. Marker `RUNTIME_GAP_END` + `BACKFILL_FROM_CANDLERANGE` in audit log (Parte 9 Cap.54).

Vincoli operativi:
- **Connessione persistente** su porta 10003 (Parte 9 Cap.46): no burst di connessioni anche per backfill multipli (regola Parte 9 invariata).
- **Backoff esponenziale** su errori (Parte 9 Cap.50 procedura sui codici 1003/1004/1007/1015/1017): retry con 5/10/20/40/60s, dopo 5 fallimenti consecutivi marker `RUNTIME_DEGRADED` (Parte 9 Cap.50) e notifica supervisore.
- **Cut-off finestra**: se il gap risale a oltre ~100gg di calendario dalla data corrente, `CANDLERANGE` tronca al limite (V-2 verifica empirica: tronca al minuto esatto, NON al giorno). Caso `gap parzialmente oltre 100gg` (es. gap di 30 giorni che inizia 95 giorni fa, finisce 65 giorni fa, parzialmente recuperabile): la procedura recupera la parte recuperabile e marca il complemento `RUNTIME_GAP_BEYOND_100D` per fallback Cap.61.

### Cap.60 — Riconciliazione canonica giornaliera (~2 pp)
Procedura normativa di **gate operativo end-of-day** che verifica la coerenza del tape DAPI runtime del giorno $d$ con la convenzione di Parte 8 e con la disponibilità del gateway.

Algoritmo:
1. Trigger: chiusura sessione 22:00 CET, marker `SESSION_CLOSE` (Parte 9 Cap.52).
2. Costruzione del **tape giornaliero canonico atteso**: 840 barre 1-min sulla griglia uniforme della sessione (epoca E5, 08:00-22:00 CET, Parte 8 Cap.41), con composizione di:
   - barre realtime accumulate dal canale push porta 10001 durante la sessione, già processate da Parte 9 Cap.49 (`bar_synthetic` derivato da `BOOK_5` count);
   - eventuali barre ricostruite da Cap.59 per gap intra-sessione, con `source ∈ {BACKFILL_FROM_CANDLERANGE}`.
3. **Verifica integrità schema**: header CSV, dominio `source`, dominio `bar_synthetic`, presenza di tutti i 840 timestamp, monotonia temporale. Failure → marker `RECONCILE_SCHEMA_FAIL` + notifica supervisore.
4. **Verifica coerenza CANDLE ufficiale del giorno**: il tape composto del giorno $d$ è confrontato con una `CANDLERANGE` di controllo dello stesso giorno $d$ richiesta a end-of-day (es. 22:30 CET) sul **ticker front-month FIB**. Le due fonti devono produrre la **stessa serie 1-min** sui minuti non-sintetici, a meno di errori di confine minuto (≤1 tick = ≤5pt FIB, tolleranza già documentata `[PROVA-EMPIRICA 2026-05-29/06-01 §2.3+§2.4]` — 5/60 e 7/62 mismatch tutti confinati al primo/ultimo minuto o salto 1-tick). Divergenza > tolleranza su un numero di minuti > `θ_reconcile` (parametro provvisorio non congelato — vedi Done when domanda d3) → marker `RECONCILE_DIVERGENT_FIB` + notifica supervisore.
5. **Verifica low/high giornaliero**: per il **ticker FIB**, il low e high giornalieri del tape composto sono confrontati con i campi `day_low`/`day_high` (`f8`/`f9`) della CANDLE ufficiale daily (period 86400) del giorno $d$ `[PROVA-EMPIRICA M-9 W2 2026-06-01]`. Tolleranza ≤ 1 tick FIB (5pt). Per i **ticker cash europei** (DGER/DSTX50/DITAS/DFRA, gating qualitativo Cap.53), la riconciliazione del low/high USA **esclusivamente** la CANDLE ufficiale daily (`f8`/`f9`), NON l'aggregato dei tick realtime, perché il feed PRICE cash è rado (~6 tick/min) e perde i minimi intraday `[PROVA-EMPIRICA 2026-06-01 V-1 afternoon §2.4.5 lettera A — 6/6 mismatch DITAS sul solo low]`. Divergenza > 1 tick FIB → marker `RECONCILE_DIVERGENT_HIGHLOW`.
6. Stato finale del giorno:
   - **`RECONCILE_OK`**: tutti i check passano. Marker in audit, tape giornaliero promosso ad archivio (Cap.62).
   - **`RECONCILE_DIVERGENT_*`**: uno o più check falliti. Marker dettagliato in audit, notifica supervisore, **flag di sessione successiva** che impedisce l'emissione segnali del giorno $d+1$ finché il supervisore non interviene (gate operativo, analogo al gate Brier $f_5^{live}$ Parte VI Cap.30).
   - **`RECONCILE_DEGRADED`**: tape composto incompleto (es. session interrotta da `RUNTIME_DEGRADED` senza recovery), marker con dettaglio, archivio parziale del giorno con flag `partial=true` nel manifest (Cap.62).

Vincoli operativi:
- **Replay deterministico preservato** (Parte II Cap.10 + Parte VII Cap.31): la riconciliazione è procedura **non-mutativa** sulla griglia 1-min (NON modifica i prezzi delle barre composte); è solo un layer di verifica che emette marker.
- **Coerenza con sanity validation Parte 8 Cap.43**: la riconciliazione di Cap.60 USA lo **stesso schema** di metriche (quantili, autocorrelazione, $\sigma$ realized) ma su finestra **giornaliera**, NON 18-24 mesi. La soglia $\theta_{reconcile}$ è parametro provvisorio (vedi Done when).

### Cap.61 — Restart >100gg e fallback Portara (~1.5 pp)
Procedura normativa per il caso `RUNTIME_STALE_RESTART` (Parte 9 Cap.51 r261): downtime continuativo della pipeline >100gg, oltre la finestra `CANDLERANGE` intraday DAPI. Il warm-up Parte 9 Cap.51 non è sufficiente; il bundle EGARCH calibrato su Portara ratio-adjusted (Parte 8 Cap.38) non può essere eseguito su warm-up cross-source mescolato.

Procedura normativa:
1. Trigger: rilevazione di `RUNTIME_STALE_RESTART` (Parte 9 Cap.51 r261), payload `{downtime_days: N, reason: "gap_exceeds_DAPI_100d_window"}`.
2. **Intervento supervisore obbligatorio**: la pipeline NON riparte automaticamente (Parte 9 Cap.51 invariato). Procedura manuale assistita:
   - **Step A — Recupero archivio locale**: verifica esistenza dei dump per il periodo di gap in `C:\Users\AN\Documents\Projects\ga-zone-engine\exports\directa_history\` (391 dump live al 28/05/2026) e in `C:\directa_history_parametric_export_overlay\exports\directa_history\` (256 dump archeologici pre-25/04, incluso `DITAS_20110404_20260402` = 15 anni daily). Se l'archivio copre il periodo: backfill da archivio locale con `source = BACKFILL_FROM_ARCHIVE`.
   - **Step B — Recupero CANDLERANGE daily ≤ ora corrente**: per ulteriore copertura, `CANDLERANGE period 86400` (daily) entro il limite "nessun cut-off pratico" `[PROVA-EMPIRICA 2026-05-29 V-2 dump probe_out/v2_cutoff_period86400_20260529_105739.csv]`. Le barre daily NON sono surrogato delle barre 1-min ma servono per cross-check di riconciliazione giornaliera retroattiva.
   - **Step C — Fallback Portara**: se né archivio locale né CANDLERANGE daily coprono completamente il periodo di gap, fallback all'archivio Portara/CQG (Parte 8 Cap.37-38). Le barre Portara entrano con `source = BACKFILL_FROM_PORTARA` e sono **convertite alla convenzione runtime** (unadjusted nativa del contratto front-month corrente, NON ratio-adjusted: il ratio-adjusted è di training, non di runtime). Vincolo di coerenza esplicito: il bundle frozen EGARCH NON viene mai eseguito su un tape mescolato cross-source (DAPI + Portara intraday) **senza re-warm-up completo post-bootstrap**. Il re-bootstrap del warm-up (`L_warmup=30gg di trading IDEM` Parte 9 D-9-NB4) è **obbligatorio** dopo bootstrap >100gg e si esegue **solo dopo** che il periodo di gap è coperto. Marker `BOOTSTRAP_COMPLETE` analogo a `WARMUP_COMPLETE` di Parte 9 Cap.51.
3. **Vincolo di non mescolamento**: durante il re-bootstrap >100gg, il tape NON è ammesso come input dell'inference live (la pipeline resta in `RUNTIME_STALE_RESTART`). Solo dopo `BOOTSTRAP_COMPLETE` + `WARMUP_COMPLETE` la pipeline esce dallo stato degraded e può tornare a emettere segnali.
4. **Coerenza ratio-adjusted vs unadjusted**: documentazione esplicita che il tape archiviato dopo bootstrap >100gg è **unadjusted nativa del front-month corrente** (Parte 9 Cap.48 r140), NON ratio-adjusted (che è convenzione di training); l'invariante research = runtime non viene violato perché il bundle EGARCH è calibrato su tape ratio-adjusted ricostruito in preprocessing (Parte 8 Cap.38) e l'adapter runtime di Parte 9 Cap.49 produce una griglia 1-min con schema simmetrico, NON una serie ratio-adjusted.

### Cap.62 — Storicizzazione strutturata del tape DAPI (~1.5-2 pp)
Procedura normativa di archiviazione del tape DAPI runtime in archivio canonico locale.

Formato dell'archivio:
- **Struttura cartelle**: `exports/directa_history/<TICKER>_<START_YYYYMMDD>_<END_YYYYMMDD>/` (pattern già esistente nello script `[CODICE-EXISTENTE export_directa_history_parametric.py]`). Granularità: una cartella per ticker per finestra temporale chiusa.
- **File CSV**: una riga per timestamp 1-min, header `symbol, timeframe, timestamp, date, time, open, high, low, close, volume, tick_count, bar_synthetic, source` (format **runtime esteso** di Parte 9 Cap.48 r117-122 B-2, NON format legacy a 11 campi dei sample committati).
- **File manifest JSON**: per ogni esecuzione di archiviazione, manifest con i campi documentati Parte 9 Cap.48 r140 + estensione Parte 10:
  - `symbol`, `start_date`, `end_date`, `host`, `port_historic`, `account_code` (mascherabile), `banner_darwin`, `config_resolved`;
  - per ogni timeframe: `mode`, `rows_received`, `first_timestamp`, `last_timestamp`, `commands_sent`, `warnings`;
  - estensioni Parte 10: `reconcile_status ∈ {OK, DIVERGENT_FIB, DIVERGENT_HIGHLOW, DEGRADED}`, `bar_counts_by_source` (es. `{DIRECTA: 800, BACKFILL_FROM_CANDLERANGE: 30, AGG_FROM_60s: 10}`), `gap_log` (lista intervalli gap con start/end/source), `partial ∈ {true, false}`, `bootstrap_completed_at` (per archivi di re-bootstrap >100gg).

Dominio esteso del campo `source` (estende Parte 9 Cap.48 r131 D-9-5):
| Valore `source` | Significato | Quando viene prodotto |
|---|---|---|
| `DIRECTA` | Record proveniente dal DAPI nel timeframe richiesto, in realtime push o storico (eredità Parte 9). | Realtime su porta 10001 o storico su porta 10003 nominale. |
| `AGG_FROM_60s` | Record aggregato da dati 1-min DAPI per timeframes superiori (eredità Parte 9). | Timeframe 5M/15M/1H non nativo. |
| `AGG_FROM_D` | Record aggregato da daily (eredità Parte 9). | Weekly non disponibile. |
| `BACKFILL_FROM_CANDLERANGE` | Record ricostruito via `CANDLERANGE` per recupero gap (Cap.59). | Gap intra/cross-session ≤100gg. |
| `BACKFILL_FROM_ARCHIVE` | Record letto dall'archivio locale `exports/` per re-bootstrap >100gg (Cap.61 Step A). | Restart >100gg con copertura archivio. |
| `BACKFILL_FROM_PORTARA` | Record letto da Portara/CQG come fallback finale (Cap.61 Step C). | Restart >100gg senza copertura archivio, con intervento supervisore. |

Vincoli operativi:
- **Idempotenza dell'archivio**: la scrittura di un giorno $d$ già archiviato è un **no-op** se il tape del giorno è identico (eredità `[PROVA-EMPIRICA T+1]` immutabilità T+3 morning). Se il tape è divergente (es. recupero gap retroattivo che aggiunge barre): apertura nuova versione dell'archivio con `version=N+1` nel manifest, NON sovrascrittura. Versioning del manifest opzionale; convenzione di lavoro: append-only sui manifest, ultimo manifest valido è il "live".
- **Immutabilità barre archiviate** (`[PROVA-EMPIRICA T+1 60/60 barre identiche fino a T+3 morning]`, perimetro empirico esplicito): le barre archiviate del giorno $d$ entro T+3 morning sui ticker FIB6F/DITAS sono **immutabili**. Limite di validità onesto da dichiarare nel capitolo: oltre T+3, su finestre afternoon/usopen, e su strumenti non testati l'immutabilità è **assunta per estensione** (non verificata empiricamente), e la procedura di riconciliazione di Cap.60 funge da gate periodico per intercettare eventuali drift.
- **NON è fonte di training** (vincolo invariato D-9 + Parte 8 Cap.37 + Cap.44): l'archivio Parte 10 è per riconciliazione + replay + bootstrap futuro, NON per re-calibrazione del bundle. L'apertura del flusso DAPI come fonte di training richiederebbe nuovo task Planner (eredità ripresa da Parte 9 Cap.55 invariata).
- **Integrazione con archivi esistenti**: i 391 dump live in `C:\Users\AN\Documents\Projects\ga-zone-engine\exports\directa_history\` (formato legacy 11 campi) NON sono migrati al format esteso di Parte 10. La migrazione è **fuori scope** Parte 10 (è operazione una-tantum di FASE-D). I dump nuovi prodotti dalla pipeline runtime di FASE-D operativa adottano il format esteso. La coabitazione tra archivio legacy (per Gap-5 test regressione Parte 9 Cap.48) e archivio esteso (per riconciliazione Parte 10) è normata: due sotto-cartelle distinte `exports/legacy/` e `exports/runtime/` se necessario, scelta architetturale di FASE-D che Parte 10 normativamente non vincola.

### Cap.63 — Coerenza inter-temporale e ricostruzione ratio-adjusted (~0.5-1 pp)
Sezione di **chiusura coerenza** che lega il tape archiviato Parte 10 (unadjusted nativa) alla serie ufficiale di training ratio-adjusted (Parte 8 Cap.38). Riassunto normativo (NON re-inventare):
- L'archivio Parte 10 è una serie di file unadjusted per contratto (es. `FIB6F_*`, `FIB6I_*`, `MINI6F_*`).
- La ricostruzione ratio-adjusted (Parte 8 Cap.38) è procedura **deterministica** che prende in input la serie unadjusted concatenata via `roll_log` e produce la serie continua per training. Parte 10 NON ri-definisce la procedura, la **richiama** come riferimento e dichiara che il tape archiviato di Parte 10 è input legittimo per Parte 8 Cap.38 a condizione che (a) la coerenza con Portara/CQG sia verificata (riconciliazione canonica giornaliera Cap.60), (b) il filtro pre-expiry $N=3$ giorni di Parte 8 Cap.39 sia applicato in preprocessing prima dell'ingresso nel training set.
- L'apertura del flusso DAPI come fonte di training resta fuori scope (eredità Parte 8 Cap.44 + Parte 9 Cap.55 + #16 di Eredità di questo task), perché la finestra effettiva DAPI è limitata (100gg intraday) e non garantisce profondità storica.

### Cap.64 — Punti aperti fuori scope (~0.5 pp)
Lista esplicita di punti che Parte 10 NON normizza, con destinazione:
- **Migrazione formato legacy → esteso** dei 391 dump live esistenti: operazione una-tantum di FASE-D, NON normata in metodologia.
- **Implementazione codice operativo** della pipeline runtime di backfill, riconciliazione, archiviazione: FASE-D del roadmap (eredità Parte 9 Cap.55 ultima riga invariata).
- **Calibrazione fine della soglia $\theta_{reconcile}$** di Cap.60: parametro provvisorio non congelato, da rifinire in FASE-D su dati operativi reali; carryover a futuro CAP-DATA-04 o monitoring post-go-live (analogo trattamento di $L_{max}=30$s Telegram in Appendice E).
- **Riavvio Darwin mezzanotte** osservazione empirica diretta: residuo Empirico-CLI di Parte 9 Cap.50 Gap-3, sessione notturna non eseguita. Parte 10 si appoggia ai marker `RUNTIME_GAP_*` già normati senza richiedere prova diretta del riavvio.
- **Immutabilità barre CANDLERANGE oltre T+3 / su finestre afternoon/usopen / strumenti non testati**: limite empirico da rifinire con probe addizionale in FASE-D se emerge necessità; Parte 10 dichiara onestamente il perimetro empirico e tratta il caso oltre come "assunto per estensione, sorvegliato dal gate di Cap.60".
- **PHASE-2 cross-index** (DAX/EuroStoxx 50/ES/MES futures): convenzione Parte 8 Cap.42 invariata; Parte 10 NON si applica ai cross-index PHASE-2 (sono fuori scope PHASE-1).
- **Telegram latenza M-2**: Appendice E, fuori perimetro DAPI (eredità #19 invariata).

### Cap.65 — Tabella decisioni del capitolo (~0.5 pp)
Tabella `D-10-1..D-10-N` con motivazione 1 riga + criterio di rollback registrato in `REPORT_CAP_10.md`. Decisioni attese (provvisorie, il Developer le rifinisce):
- **D-10-1**: Tassonomia 4-tier dei gap (intra-sessione, cross-midnight, cross-session, fuori-100gg) come vocabolario canonico di Parte 10.
- **D-10-2**: Procedura `CANDLERANGE` per recupero gap ≤100gg con marker `BACKFILL_FROM_CANDLERANGE`, idempotenza T+3 morning con perimetro empirico esplicito.
- **D-10-3**: Riconciliazione canonica giornaliera come gate operativo end-of-day, con marker `RECONCILE_OK/DIVERGENT_*/DEGRADED` e gate sulla sessione successiva.
- **D-10-4**: Regola low/high giornaliero del cash europeo via CANDLE ufficiale (`f8`/`f9`), MAI via aggregato tick realtime (motivato dal feed cash rado).
- **D-10-5**: Procedura re-bootstrap >100gg con 3 step (archivio locale, CANDLERANGE daily, Portara) e marker `BOOTSTRAP_COMPLETE`.
- **D-10-6**: Dominio esteso `source` con 3 nuovi valori `BACKFILL_FROM_*`, complemento del dominio Parte 9 D-9-5.
- **D-10-7**: Format archiviazione runtime esteso (header CSV con `tick_count` e `bar_synthetic`) + manifest JSON esteso con `reconcile_status`, `bar_counts_by_source`, `gap_log`.
- **D-10-8**: Immutabilità archivio entro T+3 morning con perimetro empirico esplicito, versioning append-only per recovery retroattivi.
- **D-10-9**: Vincolo "tape DAPI archiviato NON è fonte di training" invariato da Parte 8 Cap.37/Cap.44 e Parte 9 Cap.55.
- **D-10-10**: $\theta_{reconcile}$ parametro provvisorio non congelato, rifinito in FASE-D.

Criterio di rollback registrato in `REPORT_CAP_10.md`:
- D-10-2 (T+3 morning) parzialmente reversibile se prove empiriche future allargano/restringono il perimetro; revisione richiede nuovo task Planner.
- D-10-3 (gate operativo riconciliazione) reversibile in capitolo successivo se sperimentazione operativa dimostra che il gate produce troppi falsi positivi; rollback non richiede re-training.
- D-10-5 (procedura 3-step re-bootstrap) non reversibile dentro Parte 10 (impatta lo stato condizionato post-bootstrap come D-9-NB4); revisione richiede nuovo task Planner.
- D-10-9 (vincolo training) ereditato non reversibile in Parte 10.

---

## Acceptance Criteria

Tutti i criteri devono essere soddisfatti per PASS in Review (verifica esplicita nel `REPORT_CAP_10.md` sezione "Verifica esplicita degli Acceptance Criteria"). Acceptance Criteria numerati per capitolo + acceptance trasversali.

### AC per capitolo

- [ ] **AC-57-1** Cap.57 cita esplicitamente il rinvio Parte 9 Cap.55 r393-398 e dichiara la copertura dei 4 temi (continuità, recupero, riconciliazione, storicizzazione).
- [ ] **AC-57-2** Cap.57 dichiara l'invariante research = runtime esteso al ciclo di vita del tape, con riferimento esplicito a Parte 9 Cap.45 e Parte 8 Cap.37.
- [ ] **AC-58-1** Cap.58 definisce formalmente "gap" come intervallo contiguo di barre 1-min mancanti su griglia uniforme.
- [ ] **AC-58-2** Cap.58 contiene tabella tassonomia 4-tier (intra-sessione, cross-midnight, cross-session, fuori-100gg) con riferimento esplicito ai marker Parte 9 (`RUNTIME_GAP_*`, `RUNTIME_STALE_RESTART`).
- [ ] **AC-58-3** Cap.58 dichiara esplicitamente "barra ricostruita via backfill con dato reale = `bar_synthetic=False`" e la provenienza è in `source`, NON in `bar_synthetic` (preserva l'invariante D-9-7 booleano trade/no-trade).
- [ ] **AC-59-1** Cap.59 contiene algoritmo formale numerato (almeno 6 step) per recupero gap ≤100gg.
- [ ] **AC-59-2** Cap.59 cita `[CODICE-EXISTENTE export_directa_history_parametric.py:228-230]` per la sintassi CANDLERANGE e `[CODICE-EXISTENTE :467-481]` per lo schema CANDLE canonico.
- [ ] **AC-59-3** Cap.59 cita `[PROVA-EMPIRICA 2026-05-29 V-2 dump probe_out/v2_cutoff_period60_*]` per il limite ~100gg e `[PROVA-EMPIRICA T+1 dump probe_out/v1_hist_*]` per immutabilità T+3 morning, con dichiarazione esplicita del perimetro empirico onesto (T+3, morning, FIB6F/DITAS).
- [ ] **AC-59-4** Cap.59 contiene blocco RM-1 4-righe per l'asserzione "recupero CANDLERANGE produce barre indistinguibili dal realtime entro la finestra ≤100gg", con alternative escluse (path-inference, distorsione volatilità) e alternative NON escluse (cash low rado — eccezione documentata + caso oltre T+3).
- [ ] **AC-59-5** Cap.59 normizza il caso parziale "gap che attraversa il limite 100gg" (recupero parte recuperabile + marker `RUNTIME_GAP_BEYOND_100D` per fallback Cap.61).
- [ ] **AC-60-1** Cap.60 contiene algoritmo formale numerato (almeno 6 step) per riconciliazione end-of-day.
- [ ] **AC-60-2** Cap.60 dichiara la riconciliazione come gate operativo (analogo Brier $f_5^{live}$ Parte VI Cap.30) e gli stati finali `RECONCILE_OK/DIVERGENT_*/DEGRADED` con effetto sulla sessione successiva.
- [ ] **AC-60-3** Cap.60 contiene regola esplicita "low/high giornaliero cash europeo via CANDLE ufficiale `f8`/`f9`, MAI via aggregato tick realtime" con citazione `[PROVA-EMPIRICA V-1 afternoon §2.4.5 lettera A]` e `[PROVA-EMPIRICA M-9 W2 2026-06-01]`.
- [ ] **AC-60-4** Cap.60 dichiara $\theta_{reconcile}$ come **parametro provvisorio non congelato** con riferimento alla Done when domanda d3.
- [ ] **AC-60-5** Cap.60 dichiara che la riconciliazione è **non-mutativa** sulla griglia (preserva replay deterministico Parte II Cap.10 + Parte VII Cap.31).
- [ ] **AC-61-1** Cap.61 contiene procedura 3-step (archivio locale, CANDLERANGE daily, Portara) per re-bootstrap >100gg.
- [ ] **AC-61-2** Cap.61 dichiara obbligatorietà intervento supervisore (NON automatica) coerente con Parte 9 Cap.51 r261 D-9-11.
- [ ] **AC-61-3** Cap.61 dichiara vincolo di non-mescolamento cross-source e obbligo re-warm-up `L_warmup=30gg` post-bootstrap (eredità D-9-NB4 invariata).
- [ ] **AC-61-4** Cap.61 dichiara la coerenza unadjusted nativa runtime vs ratio-adjusted training (Parte 8 Cap.38 invariato).
- [ ] **AC-62-1** Cap.62 contiene specifica formato CSV + manifest JSON dell'archivio runtime esteso, distinto dal format legacy (Parte 9 Cap.48 r129).
- [ ] **AC-62-2** Cap.62 contiene tabella estesa del dominio `source` con 3 nuovi valori `BACKFILL_FROM_*`, complemento (NON sostituto) di Parte 9 D-9-5.
- [ ] **AC-62-3** Cap.62 dichiara idempotenza e immutabilità con perimetro empirico onesto, e versioning append-only.
- [ ] **AC-62-4** Cap.62 dichiara vincolo invariato "archivio NON è fonte di training" (eredità Parte 8 Cap.37/Cap.44 + Parte 9 Cap.55).
- [ ] **AC-62-5** Cap.62 dichiara integrazione con archivi esistenti (`exports/legacy/` + `exports/runtime/` opzionale) senza vincolare scelta architetturale FASE-D.
- [ ] **AC-63-1** Cap.63 cita la procedura ratio-adjusted Parte 8 Cap.38 come riferimento, NON la ri-definisce.
- [ ] **AC-63-2** Cap.63 dichiara fuori scope l'apertura del flusso DAPI come fonte di training.
- [ ] **AC-64-1** Cap.64 contiene lista esplicita ≥6 punti aperti con destinazione (FASE-D, CAP-DATA-04, Appendice E, ecc.).
- [ ] **AC-65-1** Cap.65 contiene tabella decisioni `D-10-1..D-10-N` con motivazione 1 riga.
- [ ] **AC-65-2** Cap.65 dichiara criteri di rollback per ogni decisione, registrati in `REPORT_CAP_10.md`.

### AC trasversali (verificabili per documento intero)

- [ ] **AC-T-1 (RM-1)** Ogni asserzione "verificato/confermato/fatto" del documento ha il blocco 4-righe `VERIFICA / PROVE / ALTERNATIVE COMPATIBILI ESCLUSE / ALTERNATIVE COMPATIBILI NON ESCLUSE`. Asserzioni in prosa libera senza blocco = BUG REALE.
- [ ] **AC-T-2 (RM-2)** Ogni richiamo a struttura/format DAPI è etichettato `[CODICE-EXISTENTE <path>:<linea>]` con citazione puntuale; il REPORT include la sezione "Decoder/convenzioni esistenti nel repo letti prima della stesura" che documenta il grep eseguito (`grep -rn` con pattern e numero risultati).
- [ ] **AC-T-3 (RM-3)** Ogni prova empirica è etichettata `[PROVA-EMPIRICA <data>]` con dump puntuale citato; il wiki Directa è citato solo come `[WIKI-HINT, da verificare]` o non citato. Nessuna asserzione si appoggia solo a livello 4.
- [ ] **AC-T-4 (RM-4)** Il Developer NON produce probe nuovi né script nuovi né handoff dentro questo task; se ne emerge necessità, Q-XX in QUESTIONS.md e stop. Verifica nel diff del PR.
- [ ] **AC-T-5 (research = runtime)** Tutte le procedure di Cap.59-Cap.62 preservano l'invariante research = runtime esteso al ciclo di vita del tape: il bundle frozen continua a leggere lo stesso schema di griglia 1-min con stesso `bar_synthetic` semantico, stesso dominio `source` (esteso), stesso replay bit-exact.
- [ ] **AC-T-6 (coerenza CAP-08 / CAP-09)** Nessun riapertura di decisioni D-8-* o D-9-* esistenti. Eventuali estensioni vivono come nuove decisioni `D-10-*`.
- [ ] **AC-T-7 (orientamento GA — regola fondamentale)** Il documento dichiara esplicitamente in Cap.57 l'impatto sul ranking/fitness/conversione signal-to-trade (riferimento Cap.60 gate operativo + Cap.62 archivio per replay deterministico).
- [ ] **AC-T-8 (perimetro empirico onesto)** Tutte le asserzioni che si appoggiano ai dump V-1/V-2/T+1 dichiarano esplicitamente il perimetro empirico testato (T+3, morning, FIB6F/DITAS, finestra ~100gg, ecc.) e segnano come "assunto per estensione" / "non testato" / "sorvegliato dal gate Cap.60" tutto ciò che esce dal perimetro.
- [ ] **AC-T-9 (M-promemoria)** Nessun M-promemoria nuovo emesso dal Developer in v1. Eventuali M-promemoria emessi dalla Review vengono ratificati dal supervisore e registrati in CARRYOVER.md dall'Orchestratore al PASS.
- [ ] **AC-T-10 (naming β2)** File `CAP_10_parte_10.md` / `REPORT_CAP_10.md`, identifier interno "Parte 10" (arabo), coerente con Parte 8/Parte 9.
- [ ] **AC-T-11 (lunghezza)** Documento totale ~9-12 pp; ogni capitolo dimensionato come dichiarato in scaletta (~0.5 pp tolleranza per capitolo).
- [ ] **AC-T-12 (indice aggiornato)** `00_indice.md` aggiornato con voce Parte 10 e stato corrente.

### AC-GO (checklist go-live / replay deterministico)

- [ ] **AC-GO-1** Replay deterministico bit-exact (Parte II Cap.10 + Parte VII Cap.31) NON impattato: due esecuzioni indipendenti su stesso input (tape composito + gap_log) producono stessi marker, stesso `reconcile_status`, stesso archivio.
- [ ] **AC-GO-2** Backfill `CANDLERANGE` su stessa finestra produce barre bit-identiche (eredità immutabilità T+3 morning verificata).
- [ ] **AC-GO-3** Riconciliazione canonica giornaliera è procedura **non-mutativa** sulla griglia (verifica esplicita).
- [ ] **AC-GO-4** Marker di Parte 10 (`RECONCILE_*`, `BACKFILL_*`, `BOOTSTRAP_COMPLETE`) sono complementari a quelli Parte 9 (`RUNTIME_GAP_*`, `RUNTIME_DEGRADED`, `RUNTIME_STALE_RESTART`, `CONTRACT_SWITCH`, `WARMUP_COMPLETE`, `SESSION_OPEN/CLOSE`), nessuna sovrapposizione semantica.

---

## Out-of-scope esplicito

Development NON include queste cose in CAP-10:

1. **Schema CANDLE / mappatura DAPI runtime** — chiuso definitivamente in AUDIT-RM-RETRO CAP-DATA-02 (WEB+CLI PASS). Parte 10 USA lo schema, NON lo riapre. Dove va trattato: Parte 9 Cap.49 (PASS storico).
2. **Policy switch front-month / rollover** — chiusa D-9-NB2 in Parte 9 Cap.47/Cap.56. Dove va trattato: Parte 9 (PASS storico). Parte 10 cita il rollover SOLO come trigger potenziale di gap, NON ne ridiscute la policy.
3. **Warm-up nominale ≤30gg** — chiuso D-9-NB4 in Parte 9 Cap.51/Cap.56. Dove va trattato: Parte 9 (PASS storico). Parte 10 tratta SOLO il warm-up post-bootstrap >100gg (Cap.61), NON il warm-up nominale di sessione.
4. **Audit log e retention** — chiusi D-9-15 + Gap-4 in Parte 9 Cap.54. Dove va trattato: Parte 9 (PASS storico). Parte 10 USA i marker già definiti, NON re-definisce il formato JSON Lines né la retention 90gg/permanente.
5. **Decisione Q-A-3 cash gating** — chiusa D-9-14 in Parte 9 Cap.53. Dove va trattato: Parte 9 (PASS storico). Parte 10 tocca il cash europeo SOLO per la regola "low/high via CANDLE ufficiale, non via tick rado" (Cap.60), NON per riapertura del gating.
6. **Convenzione cross-index PHASE-2 (DAX, EuroStoxx 50, ES/MES futures)** — Parte 8 Cap.42 invariato, Parte 10 NON si applica.
7. **Telegram latenza $L_{max}=30$s (M-2 OPEN)** — dichiarato esplicitamente fuori perimetro DAPI. Dove va trattato: Appendice E nella sessione di consolidamento delle Appendici (eredità Parte 9 Cap.55 invariata).
8. **Implementazione codice operativo della pipeline runtime** (parser, adapter, layer recovery, layer backfill, layer archiviazione, layer riconciliazione) — FASE-D del roadmap (eredità Parte 9 Cap.55 r406 invariata). Parte 10 è metodologia, NON codice.
9. **Migrazione dei 391 dump live esistenti** dal format legacy al format esteso — operazione una-tantum di FASE-D. Dove va trattato: FASE-D operativa, NON metodologica.
10. **Calibrazione fine della soglia $\theta_{reconcile}$** — parametro provvisorio non congelato; rifinitura in FASE-D su dati operativi reali o in futuro CAP-DATA-04 / monitoring post-go-live.
11. **Riavvio Darwin mezzanotte osservazione empirica diretta** — residuo Empirico-CLI di Parte 9 Cap.50 Gap-3, sessione notturna non eseguita. Parte 10 si appoggia ai marker `RUNTIME_GAP_*` di Parte 9, NON ne richiede prova diretta.
12. **Apertura del flusso DAPI come fonte di training** — Parte 8 Cap.37/Cap.44 invariati; richiederebbe nuovo task Planner con riesame ratio-adjusted/filtro pre-expiry. Esplicitamente fuori scope (eredità Parte 9 Cap.55 r404 invariata).
13. **Migrazione formato sample legacy `data/runtime/exports_sample/*`** al format esteso — la coabitazione legacy ↔ esteso è dichiarata in Cap.62 senza vincolare scelta architetturale FASE-D.
14. **Estensione immutabilità barre oltre T+3 / su finestre afternoon/usopen / strumenti non testati** — perimetro empirico onesto dichiarato; estensione richiederebbe nuovo probe empirico (Q-XX al Planner, NON dentro Parte 10).
15. **Apertura riavvio Darwin diversa da mezzanotte** (es. manutenzione straordinaria) — fuori scope, la procedura `RUNTIME_GAP_*` Parte 9 copre per costruzione qualunque riavvio.

---

## Done when (domande operative cui il documento deve rispondere)

Il documento Parte 10 deve rispondere senza ambiguità a queste domande:

**Continuità tape**
- **d1**: data una griglia 1-min con barre mancanti tra $t_a$ e $t_b$ entro una sessione, qual è la procedura passo-passo per ricostruirla, con quale schema delle barre ricostruite (campi `source`, `bar_synthetic`, `tick_count`), e qual è la condizione di idempotenza?
- **d2**: una barra ricostruita via backfill con dato reale dal gateway è `bar_synthetic = True` o `False`? Come è tracciata la provenienza "ricostruita" se non nel flag `bar_synthetic`?

**Recupero gap**
- **d3**: qual è la soglia operativa `θ_reconcile` (in numero di minuti) oltre la quale la divergenza tape DAPI runtime vs CANDLERANGE ufficiale fa scattare il gate `RECONCILE_DIVERGENT_FIB`? È congelata in Parte 10 o è parametro provvisorio rifinito in FASE-D? *(Risposta attesa Developer: parametro provvisorio non congelato, rifinitura FASE-D / monitoring post-go-live.)*
- **d4**: se un gap di 30 giorni inizia 95 giorni fa e finisce 65 giorni fa, parzialmente recuperabile via CANDLERANGE entro 100gg, qual è la regola di composizione (recupero parziale + fallback Cap.61 per la parte fuori 100gg)?
- **d5**: in caso di errore DAPI codice 1003/1004/1007/1015/1017 durante il backfill CANDLERANGE, qual è la regola di backoff e qual è il marker emesso?

**Riconciliazione canonica giornaliera**
- **d6**: end-of-day, in che ordine vengono eseguiti i 3 check (integrità schema, coerenza CANDLE 1-min, coerenza low/high giornaliero), e qual è la regola di propagazione del verdetto finale?
- **d7**: cosa succede operativamente alla sessione $d+1$ se la riconciliazione di $d$ è `RECONCILE_DIVERGENT_*`? Il bundle frozen può emettere segnali, o è bloccato fino a intervento supervisore?
- **d8**: per il cash europeo DITAS, la regola di riconciliazione del low giornaliero USA quale fonte? La CANDLE ufficiale daily (`f8`/`f9`) o l'aggregato dei tick realtime?

**Storicizzazione strutturata**
- **d9**: il file CSV archiviato di un giorno $d$ ha header con quanti campi (11 legacy o 13 esteso)? Quali sono i 3 nuovi valori del dominio `source` introdotti da Parte 10?
- **d10**: quale è la struttura del manifest JSON esteso? Quali sono le estensioni Parte 10 (es. `reconcile_status`, `bar_counts_by_source`, `gap_log`)?
- **d11**: se un giorno $d$ è già archiviato e arriva un recupero gap retroattivo, l'archivio viene sovrascritto o ne viene creata una nuova versione?

**Restart >100gg**
- **d12**: dopo `RUNTIME_STALE_RESTART`, qual è la sequenza 3-step (archivio locale, CANDLERANGE daily, Portara) e il marker finale prima che la pipeline torni operativa?
- **d13**: il re-warm-up `L_warmup=30gg` post-bootstrap >100gg è obbligatorio o opzionale? Quali sono i prerequisiti per uscire dallo stato `RUNTIME_STALE_RESTART`?

**Coerenza training**
- **d14**: il tape DAPI archiviato di Parte 10 è fonte di training per il GA? *(Risposta attesa: NO, vincolo invariato Parte 8 Cap.37 + Cap.44 + Parte 9 Cap.55.)*

---

## Decisioni di scope prese dal Planner (motivazione 1 riga ciascuna)

1. **Sede Reviewer proposta = WEB** — CAP-XX completo è documento metodologico + grep di codice committato; i prerequisiti empirici sono dump già committati come livello-1, NON richiedono ri-esecuzione contro DAPI. Decisione finale dell'Orchestratore a valle del Developer in base agli AC residui.
2. **Scaletta 9 capitoli (Cap.57-Cap.65)** — copre i 4 temi rinviati con granularità sufficiente per AC verificabili, lunghezza ~9-12 pp coerente con Parte 8 (~10 pp) e Parte 9 (~9-12 pp).
3. **Marker complementari, NON sostitutivi, dei marker Parte 9** — `RECONCILE_*`/`BACKFILL_*`/`BOOTSTRAP_COMPLETE` vivono accanto a `RUNTIME_*`/`CONTRACT_SWITCH`/`WARMUP_*`/`SESSION_*` senza sovrapposizione, per preservare la chiusura Cap.56 di Parte 9.
4. **Dominio `source` esteso, NON sostituito** — i 3 nuovi valori `BACKFILL_FROM_*` complementano `{DIRECTA, AGG_FROM_60s, AGG_FROM_D}` di D-9-5, perché Cap.62 esplicitamente dichiara complemento, NON sostituzione. Coerente con principio "no riapertura decisioni precedenti".
5. **$\theta_{reconcile}$ parametro provvisorio** — non congelato dentro Parte 10, rifinitura in FASE-D operativa. Coerente con trattamento $L_{max}$ Telegram (Appendice E carryover) e $\theta_{DSR}/\theta_{PBO}/\ldots$ in Parte VII Cap.31 (12 parametri provvisori non congelati). NO numeri inventati dal Planner.
6. **Restart >100gg gestito con intervento supervisore obbligatorio** — eredità Parte 9 D-9-11 invariata, NON auto-recovery. Decisione conservativa: il caso è raro (downtime >5 mesi solari), il rischio di mescolamento cross-source è alto, l'intervento manuale è preferibile a procedura automatica complessa.
7. **Immutabilità barre con perimetro empirico esplicito (T+3, morning, FIB6F/DITAS)** — NON estesa per default a tutti i casi, dichiarata onestamente come "assunto per estensione, sorvegliato da gate Cap.60". Coerente con RM-1 (no asserzioni "verificate" oltre il perimetro testato).
8. **Cash europeo low/high via CANDLE ufficiale** — decisione forte motivata da `[PROVA-EMPIRICA V-1 afternoon 6/6 mismatch sul solo low]`, indipendente dalla decisione Q-A-3 di Parte 9 Cap.53 (gating qualitativo). NON apre il gating, normizza solo la fonte del low/high.
9. **Riconciliazione = procedura non-mutativa** — non modifica le barre, emette solo marker. Coerente con principio di replay deterministico bit-exact (Parte II Cap.10 + Parte VII Cap.31). Eventuale rewriting va in un capitolo successivo o in FASE-D.
10. **Carryover M-2 (Telegram) dichiarato esplicitamente fuori scope** — `OPEN` invariato in CARRYOVER.md, ripreso in sessione futura di Appendice E. Coerente con #19 Eredità del task.
11. **Migrazione dump legacy fuori scope** — è operazione una-tantum di FASE-D, non normazione metodologica.

---

## Pipeline attesa

```
Planner v1 (questo task card)
  ↓ Orchestratore committa task card
Developer v1 (CAP_10_parte_10.md + REPORT_CAP_10.md + 00_indice.md)
  ↓ READY_FOR_REVIEW
Orchestratore check post-Developer (6 condizioni)
  ↓ se PASS condizioni → Reviewer Web v1
Reviewer Web v1 (review piena RM-1/2/3 + AC + classificazione finding)
  ↓ verdetto PASS / CONDITIONAL / FAIL
  ↓ se CONDITIONAL/FAIL → punto di controllo supervisore con tabella classificazione
Eventuale rework Developer v2 (solo finding approvati)
  ↓ Reviewer Web v2 → ... → PASS
Chiusura sessione (7 condizioni Orchestratore) + notifica + prompt-template nuova sessione
```

Iterazioni attese: 1-2 cicli Review (in linea con i cicli Parte 8 v1→v2 e Parte 9 v1→v2). Se a 3 iterazioni il loop non chiude su un finding specifico, regola di terminazione `.claude/CLAUDE.md` § "Regola di terminazione del loop": segnalazione supervisore per arbitraggio.

---

## Note operative per il Developer (riepilogo dei vincoli RM-1..RM-4 applicabili in pre-consegna)

Il Developer di Parte 10:

- Prima di iniziare la stesura, esegue **grep RM-2** sui pattern dichiarati (#2 di Eredità) e documenta l'esito nella sezione "Decoder/convenzioni esistenti nel repo letti prima della stesura" del REPORT.
- Etichetta TUTTE le fonti con livello (`[PROVA-EMPIRICA <data>]` / `[CODICE-EXISTENTE <path>:<linea>]` / `[DOC-INTERNO]` / `[WIKI-HINT, da verificare]`). Wiki Directa = mai fonte autorevole.
- Per ogni asserzione "verificato/confermato/fatto" applica blocco 4-righe RM-1 (`METODO.md:28-33`).
- NON produce output non-CAP collaterali (probe, script, handoff). Se serve, Q-XX al Planner.
- Pre-consegna (autoverifica prima di `READY_FOR_REVIEW`):
  1. Tutti gli AC della sezione "Acceptance Criteria" sono verificabili sul documento prodotto?
  2. Tutte le citazioni file:linea sono accurate (controllo via Read sui path citati)?
  3. Tutti i blocchi RM-1 sono nel formato 4-righe esatto?
  4. Nessuna riapertura di decisioni D-8-* o D-9-*?
  5. Nessun M-promemoria nuovo emesso (al massimo segnalato come "potenziale per Review")?
  6. Naming β2 rispettato (`CAP_10_parte_10.md`, identifier "Parte 10" arabo)?
  7. `00_indice.md` aggiornato con voce Parte 10 e stato "IN REVIEW"?
  8. `REPORT_CAP_10.md` contiene le 5 sezioni standard + Verifica AC + Criterio rollback + sezione grep RM-2?

Se uno solo dei 8 punti non passa, NON scrivere `READY_FOR_REVIEW`: completa la revisione interna.
