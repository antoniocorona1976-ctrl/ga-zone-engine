# TASK ATTIVO: SPEC-FUNZ-01-B6 — Schema-dato DAPI & continuità tape (ricostruzione cieca, modalità B, blocco 6/8)

> **Track**: Business-spec (SPEC-FUNZ). **Sede**: CLI (GOV-SURFACES-01). **Tag commit**: `[SPEC-FUNZ-01-B6]`. Tutto su `main`.
>
> **⚠️ CAUTELA RM MASSIMA**: questo blocco consolida lo **schema-dato di un sistema esterno (Directa DAPI)** — il territorio che ha generato RM-1..RM-4 (incidente schema CANDLE `O;H;L;C` errato). La materia di schema è in larga parte **già certificata PROVA-EMPIRICA** (audit CAP-DATA-02, PASS contro DAPI live): il lavoro è **consolidamento fedele**, NON ri-derivazione. Ogni claim di schema porta una citazione `path:line` (decoder o CAP) o `[PROVA-EMPIRICA <data>]`; **mai** una conclusione strutturale dal solo wiki Directa.
>
> **Perimetro (per CAPITOLI — modalità B)**: deriva **tutti** i requisiti di prodotto dai capitoli **`CAP_09_parte_9.md` Cap.48, 49, 51 + `CAP_10_parte_10.md` Cap.59, 60, 61, 62** (più i decoder/audit per RM-2, §0.1). Assegna gli ID `B6-R-NN`/`B6-CN-NN`/`B6-NFR-NN` **da zero**, applicando l'atomicità N1. **Nessun conteggio-target è imposto.** NB path: i file CAP usano numero **arabo** (`CAP_09_parte_9.md`, `CAP_10_parte_10.md`).
>
> **Letture obbligatorie del Developer, in quest'ordine, PRIMA di scrivere**: `tasks/METODO.md` (RM-1..RM-4 + RACC-METODO-2), `.claude/BASE_COMUNE.md`, `.claude/agents/spec_developer.md`, questo `tasks/ACTIVE_TASK.md`. Conferma in testa al REPORT di averli letti.

---

## 0. Natura e cecità

**Natura**: ricostruzione cieca da zero del perimetro schema-dato DAPI & continuità tape. B1..B5 sono chiusi PASS; B7/B8 non esistono ancora.

### 0.1 — Vincolo di cecità (modalità B) + eccezione RM-2 obbligatoria

Il Developer deriva i requisiti **DAI SOLI** capitoli del perimetro §1, **cieco** rispetto a: `SPEC_FUNZ_01.md` (v2 congelata) e `*_v1_storico*`; i **file di chunking** (`PROPOSTA_SUDDIVISIONE_SPEC*.md`); i documenti B1..B5 (`SPEC_FUNZ_01_B*.md`). Il confronto-copertura con la v2 e la partizione dei requisiti sono compito **esclusivo del Reviewer/Orchestratore** (§6): il Developer **non li vede e non li deve cercare**. Gli ID `B6-*` sono auto-assegnati da zero.

**Eccezione RM-2 (OBBLIGATORIA, non rompe la cecità)**: il Developer **DEVE** leggere i **decoder di produzione** (`scripts/export_directa_history_parametric.py`, `scripts/probe_dapi.py`) e gli **audit empirici** (`reviews/PROBE_REVIEW_CAP_09_*_cli.md`, `reviews/REVIEW_CAP_09*_review.md`, M-promemoria in `tasks/STATO_CORRENTE.md`) per ancorare ogni claim di schema. Sono **codice di produzione + prove empiriche**, NON la spec v2/B*: leggerli è imposto da RM-2/RACC-METODO-2. **Citare uno schema esterno senza il diff col decoder canonico è verifica parziale, non verifica** (RACC-METODO-2).

---

## 1. Perimetro-fonte — materia da derivare, PER CAPITOLO

Fonte: `docs/methodology_v2/CAP_09_parte_9.md` (Cap.48,49,51) + `docs/methodology_v2/CAP_10_parte_10.md` (Cap.59,60,61,62). Pin = puntatori di lavoro verificati in CLI; il Developer li **rilegge token-per-token** (AC-G7) prima di citarli.

- **Cap.49 — Mappatura schema DAPI → bundle frozen** (`CAP_09_parte_9.md:151-191`): l'**adapter** che traduce il record DAPI in una **barra 1-min normativa simmetrica al tape di training** (stesso schema OHLCV + `tick_count` + `bar_synthetic`, stesse regole forward-fill). È il cuore del blocco. Materia:
  - schema **CANDLE** reale `UFF;MIN;MAX;APE;V` = **`C;L;H;O;V`** — mappatura campo-per-campo `:164-171` (bar_open←campo8 APE, bar_high←campo7 MAX, bar_low←campo6 MIN, bar_close←campo5 UFF, volume←campo9), col blocco RM-1 a 4 righe già nel CAP `:157-162`;
  - `tick_count` ← eventi **BOOK_5** in regime realtime (porta 10001), `NULL` in regime storico CANDLERANGE (porta 10003) `:172`;
  - `bar_synthetic` (booleano trade/no-trade): regola per FIB-realtime (BOOK_5), FIB-storico (CANDLERANGE), cash (PRICE) `:173, :177-179`;
  - **invariante replay bit-exact / research = runtime** applicato all'adapter `:21` (preambolo) — **fondazione formale premessa `CAP_02_parte_II.md` Cap.10** (NON ri-derivare il vincolo dal motore; consolidarlo come invariante che l'adapter preserva).
- **Cap.48 — Format dati canonico runtime** (`:111-149`): **capitolo di framing/contesto** (verificato CLI: non fonda un requisito-prodotto standalone). Definisce il **contenitore**: header CSV a **13 campi esatti** (`symbol, timeframe, timestamp, date, time, open, high, low, close, volume, tick_count, bar_synthetic, source`, `:117/:120`; il format **legacy** ha 11 campi, senza `tick_count`/`bar_synthetic`, `:129`) e il **manifest JSON** (`:141`). Tratta come format/contesto a supporto dell'adapter (Cap.49) e dell'archivio (Cap.62); **non** scrivere un requisito "su Cap.48" salvo trovi una proposizione di prodotto non coperta dall'adapter/archivio.
- **Cap.51 — Warm-up stati condizionali** (`:251-262`): al boot, pull storico `CANDLERANGE` con lookback **`L_warmup = 30` giorni di trading** (valore **congelato**, NB-4 Opzione A, `:259` — **non** "~30"); marker `WARMUP_COMPLETE`.
- **Cap.59 — Recupero gap ≤100gg** (`:74-110`): recupero gap entro la finestra **100 giorni** (intraday DAPI) via `CANDLERANGE`; idempotenza.
- **Cap.61 — Restart >100gg** (`:151-175`): downtime > 100gg → stato `RUNTIME_STALE_RESTART` + re-bootstrap (fallback archivio/daily/Portara) + re-warm-up obbligatorio.
  > **Nota N1 (atomicità)**: Cap.59 e Cap.61 descrivono **due comportamenti distinti** (recupero-gap entro-finestra **vs** restart-stale oltre-finestra), con trigger e capitoli diversi. Sono attesi **requisiti B6 distinti** (non impacchettarli in uno solo).
- **Cap.60 — Riconciliazione canonica giornaliera** (`:113-149`): **gate operativo end-of-day bloccante** (il fallimento di riconciliazione **blocca l'emissione del giorno d+1**); la riconciliazione di **low/high daily** usa **esclusivamente il CANDLE ufficiale daily** (campi `f8`/`f9`), **mai** l'aggregato realtime (`:122-124, :133-141`).
- **Cap.62 — Storicizzazione strutturata del tape** (`:178-210`): archivio canonico locale con header esteso, **manifest JSON**, **immutabilità append-only**; e il **vincolo negativo**: il tape archiviato **NON è fonte di training** del bundle (`:209`, premessa `CAP_08_parte_8.md` Cap.44).

---

## 2. Fatti schema-dato già certificati — consolidamento fedele (RM-3, NON ri-derivare)

Autoritativi (audit CAP-DATA-02): citali con l'etichetta esatta, non ri-derivarli, non sovra-marcarli.

- **CANDLE** = `UFF;MIN;MAX;APE;V` = **`C;L;H;O;V`** — `[CODICE-ESISTENTE export_directa_history_parametric.py:477-481]` (`# UFF, MIN, MAX, APE => close, low, high, open`) + `[CODICE-ESISTENTE probe_dapi.py:247-270]` + `[PROVA-EMPIRICA 2026-05-29 V-1]` (M-1). **RM-1**: permutazione wiki `O;H;L;C` **esclusa** (V-1 tick-by-tick distinse O da C; su daily erano indistinguibili → da cui l'errore originale). Diff col decoder canonico **obbligatorio** (RACC-METODO-2).
- **F3 — `f8`/`f9` per tipo-messaggio (RM-1, escludere confusione cross-schema)**: l'indice `f8`/`f9` compare in **due schemi DISTINTI**, da NON confondere:
  - **CANDLE daily** (riconciliazione, Cap.60): `f8`/`f9` = low/high ufficiali daily → usati per CN di riconciliazione. `[PROVA-EMPIRICA, CAP-DATA-02]`.
  - **PRICE realtime** (schema del canale): `f8`=day_low, `f9`=day_high, `f6`=volume cumulato — `[PROVA-EMPIRICA 2026-06-01 W2]` (M-9). **RM-1**: l'ipotesi web "`f8`/`f9` = best bid/ask" è **FALSIFICATA** dal BOOK_5 simultaneo (`tasks/STATO_CORRENTE.md:33`); `f5`/`f7` **non disambiguati** (verifica parziale → marcare).
  - **Esclusione esplicita (RM-1)**: la coincidenza dell'indice `f8`/`f9` fra CANDLE-daily e PRICE-realtime **non implica un namespace condiviso**: sono campi di due messaggi diversi. La card/spec li nomina **separati per tipo-messaggio**; non dedurre l'uno dall'altro.
- **BOOK_5**: `BOOK_5;<tk>;<HH:mm:ss>;` + 10 triple `(lots,orders,price)` = `[BID×5 best-first][ASK×5 best-first]`; `bid1_lots`=campo4, `bid1_orders`=campo5, `bid1_price`=campo6; `ask1_lots`=campo19, `ask1_price`=campo21 — `[PROVA-EMPIRICA 2026-06-01 W3]` (M-10) + `[CODICE-ESISTENTE probe_dapi.py:307-317]`. **RM-1**: `f1≥f2` su **290/290** esclude il triplo invertito; `bid1<ask1` su 29/29; l'anomalia 27/05 `bid1>ask1` è artefatto del campione (FIB6I illiquido), NON inversione schema.
- **Mesi Directa-IDEM**: `F`=giugno `[PROVA-EMPIRICA 2026-05-29 W5]`; `I`=settembre `[PROVA-EMPIRICA 2026-06-01 W6]` (M-4). Convenzione **NON-standard** (≠CME): **nessuna inferenza per analogia** (RM-3).
- **Codici errore** `1004`/`1007`/`1017`/`1015`/`1003` disambiguati `[PROVA-EMPIRICA 2026-05-29 W4 + 2026-06-01 W5a]` (M-3).

**F4 — PRICE e BOOK_5 sono INPUT dell'adapter** (decisione da repo, evidenza `CAP_09_parte_9.md:172-173, :177-179`): l'adapter (Cap.49) consuma **CANDLE** (OHLCV della barra), **BOOK_5** (`tick_count` realtime + regola `bar_synthetic` del FIB) e **PRICE** (regola `bar_synthetic` dei cash europei per il gating). Quindi gli schemi PRICE/BOOK_5 **si consolidano come input dell'adapter** (ancorati al requisito-adapter), **non** sono materia di canale (B5). Il **canale** (porte/handshake/sottoscrizione) resta B5-premessa (§5); B6 consolida lo **schema/decodifica** e il suo **uso nell'adapter**.

**Eredità M (registro CARRYOVER/STATO)**: **M-1** (CANDLE), **M-9** (PRICE), **M-10** (BOOK_5), **RACC-METODO-2** (diff col decoder canonico obbligatorio). Tutti pertinenti a B6.

---

## 3. Acceptance Criteria

**AC-G1..AC-G11** dei blocchi precedenti (atomicità N1; tracciabilità a riga `CAP_09`/`CAP_10`/decoder; valore operativo o di sistema/replay; divieto "verificato X" di prima istanza RM-1; etichette RM-3; grafia canonica `[CODICE-ESISTENTE]`/`[PROVA-EMPIRICA]`/`[DOC-INTERNO]`/`[WIKI-HINT]` — **vietata `[CODICE-EXISTENTE]`**; floor citazioni 100% in review; cecità preservata; scope "tutto e solo" i capitoli §1; matrice + nota di rinvio; invarianti come tali). In più, **specifici di B6 (cautela RM massima)**:

- **AC-B6-1 — RM-2 (diff col decoder canonico)**: ogni claim di schema-dato (CANDLE/PRICE/BOOK_5/ordine campi/header) cita il **decoder di produzione** `path:line` e, dove applicabile, il **diff** col decoder canonico. Citare lo schema senza il diff = finding (RACC-METODO-2).
- **AC-B6-2 — RM-1 permutazioni escluse**: ogni claim di **ordine campi** enumera ed **esclude esplicitamente** le permutazioni alternative. Obbligatorio per: CANDLE (escludere `O;H;L;C`), PRICE `f8`/`f9` (escludere bid/ask + escludere confusione con CANDLE-daily, F3), BOOK_5 (escludere triplo invertito).
- **AC-B6-3 — RM-3 gerarchia fonti**: `PROVA-EMPIRICA > CODICE-ESISTENTE > WIKI-HINT`. Wiki Directa = `[WIKI-HINT, da verificare]`; **0 conclusioni strutturali wiki-only**.
- **AC-B6-4 — PENDING-empirico marcato (non asserito)**: vedi §6. Distinguere certificato (CANDLE/PRICE/BOOK_5, mesi F/I, codici errore) da pending (Mar/Dic, 1030, Darwin-mezzanotte) e da verifica parziale (PRICE `f5`/`f7`; base calendario-vs-trading-days delle finestre).

---

## 4. Sezioni da produrre (`docs/spec_funzionale/SPEC_FUNZ_01_B6.md`)

1. Intestazione/scopo/schema-ID (`B6-*` da zero) + conferma cecità + nota cautela RM massima.
2. **Adapter & schema-dato** (Cap.49): adapter→barra 1-min simmetrica; schema CANDLE `C;L;H;O;V` (diff decoder + RM-1); PRICE e BOOK_5 come **input dell'adapter** (`tick_count`, `bar_synthetic`) con RM-1/RM-2; format/header come contesto (Cap.48, 13 campi).
3. **Replay deterministico** (invariante research=runtime, Cap.49 `:21` + premessa `CAP_02 Cap.10`): consolidare come invariante che l'adapter preserva, non ri-derivare dal motore.
4. **Warm-up & continuità** (Cap.51, Cap.59, Cap.61): warm-up `L_warmup=30` giorni di trading; recupero gap ≤100gg **e** (requisito distinto, N1) restart >100gg `RUNTIME_STALE_RESTART`.
5. **Riconciliazione canonica** (Cap.60): gate EOD bloccante; low/high daily da CANDLE ufficiale daily `f8`/`f9`.
6. **Storicizzazione tape** (Cap.62): archivio header esteso/manifest/append-only; tape **NON** fonte training (vincolo negativo, premessa `CAP_08 Cap.44`).
7. **Matrice di tracciabilità** + **nota di rinvio** (premesse/fuori-scope §5) + **lista PENDING-empirico** (§6) + nota RM-3.

REPORT (`reports/REPORT_SPEC_FUNZ_01_B6.md`): 6 sezioni formato supervisore + tabella AC (G1..G11 + B6-1..4) + "Applicazione RM-1 a me stesso" (con i grep RM-2 eseguiti e i decoder letti `path:line`) + lista PENDING-empirico.

---

## 5. Out-of-scope & premesse (con destinazione) — anti scope-creep

| Materia | Destinazione |
|---|---|
| **Canale DAPI**: porte/handshake/sottoscrizione/loopback (Cap.46/47) | **B5** — premessa (origine del dato); B6 consolida lo **schema/decodifica** e l'**uso nell'adapter**, NON il canale |
| Eventi audit (`CANDLE_RESPONSE`, `BOOK_RESPONSE`, …) (Cap.54) | **B5** — premessa; B6 tratta lo schema, l'audit è B5 |
| Riconciliazione tape↔runtime, versante runtime-tape | **Parte 10 / CAP-DATA-03** (chiuso PASS) — premessa |
| Preprocessor/back-adjustment Portara, ratio-adjusted, filtro pre-expiry (Cap.40/38/39) | **Parte 8** — premessa; B6 non ri-deriva il preprocessing di training |
| State machine / lifecycle del segnale | **B3** — premessa |
| Determinismo bit-exact (invariante formale) | **premessa `CAP_02 Cap.10`** (consolidato come invariante che l'adapter preserva, non ri-derivato) |
| `Cap.48` format canonico | **framing/contesto** (contenitore CSV 13 campi/manifest), non requisito standalone |
| Tape come fonte training | **fuori scope** (vincolo D-10-9; eredita Parte 8 Cap.44 + Parte 9 Cap.55) — consolidato come **vincolo negativo** |

### F7 — Due "restart" da NON confondere (riga esplicita)
- **Riavvio Darwin a mezzanotte** (Gap-3, `CAP_09 Cap.50`): manutenzione del gateway, **continuità infra-giornaliera** → **premessa B5** (recovery del canale). B6 lo cita come premessa, non lo consolida.
- **`RUNTIME_STALE_RESTART`** (`CAP_10 Cap.61`, >100gg): **staleness oltre la finestra** di recupero DAPI, richiede re-bootstrap → **in-scope B6** (continuità tape).
Sono concetti diversi (trigger, scala temporale, capitolo): tienili distinti, non conflarli.

---

## 6. PENDING-empirico (marcare, NON asserire — AC-B6-4)

- **Codici mese Mar/Dic** Directa-IDEM: contratti non listati al 2026-06-01 → `1007`; non decodificabili finché non quotati → **PENDING-empirico** (ANAG a mercato aperto, Cap.55/64).
- **Ticker 1030** (realtime non sottoscritto): IDEM nel servizio base, **non riprodotto** sul FIB → **verifica parziale / PHASE-2 gated**.
- **Riavvio Darwin a mezzanotte** (Gap-3): comportamento notturno → **PENDING-empirico** (premessa B5, vedi F7).
- **PRICE `f5`/`f7`** contatori cumulativi: **non disambiguati** → marcare, non asserire semantica.
- **Base calendario-vs-giorni-di-trading delle finestre 30/100** (V-2): la convenzione "30 giorni di trading" / "100 giorni" come si mappa sul calendario IDEM era **V-2 PENDING-empirico (eredità B5)** → marcare; **il valore `L_warmup=30` è congelato** (non pending), ma la sua **resa in giorni-di-calendario** è V-2.

NON pending (certificati, citare con stato esatto): CANDLE `C;L;H;O;V`; PRICE `f8`/`f9`/`f6`; BOOK_5 (290/290); mesi F/I; codici errore; `L_warmup=30` (valore congelato); 13 campi header.

---

## 7. Done-when (soglie di verdetto)

1. Ogni capitolo del perimetro §1 che fonda materia di prodotto è coperto da almeno un requisito `B6-*`; Cap.59 e Cap.61 producono **requisiti distinti** (N1, F5).
2. Ogni claim di schema porta `[CODICE-ESISTENTE path:line]` **o** `[PROVA-EMPIRICA <data>]`; **0 conclusioni wiki-only**.
3. **RM-1**: permutazioni alternative escluse (CANDLE `O;H;L;C`; PRICE `f8/f9` bid/ask **e** confusione con CANDLE-daily; BOOK_5 triplo invertito).
4. **RM-2**: decoder canonico citato `path:line`; diff schema↔decoder dichiarato.
5. PENDING-empirico (§6) marcati, non asseriti; verifiche parziali distinte dai certificati; `L_warmup=30` esatto (no `~`), 13 campi enumerati.
6. Confini §5 rispettati (canale→B5, audit→B5, preprocessor→Parte 8, lifecycle→B3, determinismo→premessa CAP_02 Cap.10, Cap.48 framing); F7 (Darwin vs STALE) distinto.
7. **Cecità**: la spec non contiene ID-requisito importati né conteggi/partizioni da v2/chunking; ID `B6-*` auto-assegnati.

---

## 8. Separazione ruoli

- **Planner** (questo task): definisce il perimetro **per capitoli** (no ID-v2, no conteggio, no partizione esposti al Developer), gli AC, i confini, i PENDING. **Non scrive la spec.** La mappatura Req-v2 ↔ capitolo vive **fuori da questa card** (ESITO Orchestratore/Reviewer).
- **Developer** (cieco, §0.1): deriva dai soli capitoli del perimetro + decoder/audit (RM-2); assegna `B6-*` da zero; **non ridefinisce il perimetro, non cerca la mappa v2**; scrive `SPEC_FUNZ_01_B6.md` + REPORT; `READY_FOR_REVIEW`; si ferma.
- **Reviewer** (CLI): audita gli AC + confronto-copertura vs perimetro B6 (mappa `c7ce4be`, F-3, che **il Reviewer** consulta — non il Developer); **floor citazioni 100%**; verifica RM-1/RM-2/RM-3 e i diff col decoder; **non ripianifica**. Verdetto PASS/CONDITIONAL/FAIL.

---

*Card B6 scritta dall'Orchestratore/Planner, **rev. CARD-FIX-01** (7 finding di audit chiusi: F1 cecità — rimossi ID-v2/conteggio/partizione, vista per soli capitoli; F2 invariante replay bit-exact/research=runtime = in-scope, fondazione premessa CAP_02 Cap.10, pin corretto `:21` non Cap.49; F3 `f8`/`f9` separati per tipo-messaggio + RM-1; F4 PRICE/BOOK_5 = input adapter, evidenza `:172-173/:177-179`; F5 gap≤100gg e restart>100gg = requisiti distinti; F6 `L_warmup=30` congelato + 13 campi enumerati, no `~`; F7 Darwin-mezzanotte vs RUNTIME_STALE_RESTART distinti). NON committata come `tasks/ACTIVE_TASK.md`: questo task produce la card-sorgente e si ferma. Nessuna spec scritta, nessun CAP modificato (freeze G-09). Path file CAP verificati reali: `CAP_09_parte_9.md`, `CAP_10_parte_10.md`. La vista-Developer è per soli capitoli: nessun ID-requisito v2, nessun conteggio, nessuna partizione esposti — cecità preservata.*
