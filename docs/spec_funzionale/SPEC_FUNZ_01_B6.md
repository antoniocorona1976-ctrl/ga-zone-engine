# SPEC-FUNZ-01-B6 — Schema-dato DAPI & continuità tape

> **Track**: Business-spec (SPEC-FUNZ). **Blocco**: 6/8 della ricostruzione cieca (modalità B). **Tag commit**: `[SPEC-FUNZ-01-B6]`.
>
> **Cautela RM massima**: questo documento consolida lo **schema-dato di un sistema esterno (Directa DAPI)**, il territorio che ha generato RM-1..RM-4 (incidente schema CANDLE `O;H;L;C` errato). La materia di schema è in larga parte **già certificata PROVA-EMPIRICA** (audit CAP-DATA-02, PASS contro DAPI live) e/o ancorata al **decoder di produzione**: il lavoro qui è **consolidamento fedele**, non ri-derivazione. Ogni claim di schema porta una citazione `path:line` (decoder o CAP chiuso) o `[PROVA-EMPIRICA <data>]`; **nessuna conclusione strutturale poggia sul solo wiki Directa** (RM-3).

---

## 1. Scopo, ambito e convenzioni

### 1.1 Scopo

Questo documento è la specifica funzionale dello **schema-dato DAPI** (decodifica dei record del gateway Directa Darwin) e della **continuità del tape** runtime: come la pipeline traduce i record DAPI in barre normative simmetriche al training, come preserva il replay deterministico, come gestisce warm-up, gap, riconciliazione e storicizzazione. Consolida i capitoli metodologici v2 già chiusi PASS in requisiti atomici tracciabili e leggibili da un esterno.

### 1.2 Fonte

Derivato da: `docs/methodology_v2/CAP_09_parte_9.md` (Cap.48, 49, 51) e `docs/methodology_v2/CAP_10_parte_10.md` (Cap.59, 60, 61, 62), più i **decoder di produzione** (`scripts/export_directa_history_parametric.py`, `scripts/probe_dapi.py`) e gli **audit empirici** (CAP-DATA-02 RM-RETRO, M-promemoria M-1/M-9/M-10/M-4/M-3) citati a norma di RM-2/RACC-METODO-2. La fondazione formale del replay bit-exact è in premessa da `docs/methodology_v2/CAP_02_parte_II.md` Cap.10.

### 1.3 Convenzione degli ID e atomicità (N1)

Gli ID `B6-R-NN` (requisito funzionale), `B6-CN-NN` (vincolo/condizione), `B6-NFR-NN` (requisito non funzionale di sistema/replay) sono **auto-assegnati da zero** per questo blocco. Ogni requisito esprime **una sola proposizione verificabile**.

### 1.4 Conferma di cecità

Questo documento è stato derivato **dai soli** capitoli del perimetro §1.2 + decoder/audit (eccezione RM-2). Non sono stati letti né citati: `SPEC_FUNZ_01.md` (v2), file `*_v1_storico*`, file di chunking (`PROPOSTA_SUDDIVISIONE_SPEC*.md`), documenti B1..B5 (`SPEC_FUNZ_01_B*.md`). Nessun ID-requisito v2 è importato; nessun conteggio o partizione v2 è usato.

### 1.5 Convenzione delle etichette di fonte (RM-3)

Gerarchia: `[PROVA-EMPIRICA <data>]` (livello 1) > `[CODICE-ESISTENTE path:line]` (livello 2) > `[DOC-INTERNO <path:riga>]` (capitolo v2 chiuso PASS, livello 3) > `[WIKI-HINT, da verificare]` (livello 4, solo hint, mai conclusione strutturale). Grafia canonica: `[CODICE-ESISTENTE]` (vietata la grafia storica deprecata).

---

## 2. Adapter & schema-dato (Cap.49, Cap.48)

L'adapter DAPI → bundle frozen è il cuore del blocco: traduce i record DAPI in barre 1-min normative simmetriche al tape di training, senza re-calibrazione e senza re-mappatura dello schema.

### 2.1 L'adapter come layer di normalizzazione di schema

**B6-R-01** — La pipeline runtime deve applicare un **adapter DAPI → bundle frozen** che traduce, per ogni minuto della griglia 1-min della sessione corrente, un record DAPI in un record con **esattamente lo stesso schema operativo** del preprocessor di training, in modo che il bundle frozen sia applicato senza re-calibrazione.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:153]`. *Valore*: garantisce che il modello in produzione legga la stessa struttura-dato su cui è stato calibrato (continuità research↔runtime).

**B6-R-02** — L'adapter deve essere un layer di **normalizzazione di schema**, non un layer di traduzione semantica del segnale: produce in tempo reale la stessa griglia 1-min con gli stessi campi e gli stessi flag del bundle frozen di training; il bundle frozen non legge mai dati DAPI grezzi.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:191]`. *Valore*: confina la complessità del canale esterno nell'adapter, isolando il motore da formati e patologie DAPI.

**B6-R-03** — L'adapter deve produrre per la sessione 08:00-22:00 CET una griglia 1-min **uniforme**, con una riga per ogni minuto della finestra di sessione, applicando le stesse regole di forward-fill del training (per i minuti senza trade: Open = High = Low = Close = Close del minuto precedente, Volume = 0, `tick_count = 0`).
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:127]`. *Valore*: la griglia uniforme è la struttura attesa dal feature engineering downstream.

### 2.2 Schema CANDLE — ordine campi certificato (RM-1 + RM-2)

**B6-R-04** — Il payload `CANDLE` del gateway Directa ha l'ordine campi `UFF;MIN;MAX;APE;V`, mappato su `close;low;high;open;volume` (schema canonico `C;L;H;O;V`).
*Tracciabilità*: `[CODICE-ESISTENTE export_directa_history_parametric.py:477-481]` (decoder canonico di produzione: commento `# Documentazione Directa: UFF, MIN, MAX, APE => close, low, high, open.`, con `close_v = Decimal(uff)`, `low_v = Decimal(min_)`, `high_v = Decimal(max_)`, `open_v = Decimal(ape)`) + `[CODICE-ESISTENTE probe_dapi.py:247-270]` (`"close": float(p[4]) # UFF`, `"low": float(p[5]) # MIN`, `"high": float(p[6]) # MAX`, `"open": float(p[7]) # APE`) + `[PROVA-EMPIRICA 2026-05-29 V-1]` (M-1, tick-by-tick) + `[DOC-INTERNO CAP_09_parte_9.md:158]`. *Valore*: lo schema corretto dei prezzi è il prerequisito di ogni feature di prezzo; un ordine sbagliato (incidente CANDLE) corrompe tutto il motore.

> **Diff col decoder canonico (RACC-METODO-2)**: i due decoder di produzione concordano token-per-token. `parse_directa_candle` (`export_directa_history_parametric.py:471`) splitta `parts[:9] = kind, symbol, ymd, hms, uff, min_, max_, ape, qty` e mappa `close←uff, low←min_, high←max_, open←ape` (`:477-481`); il decoder runtime `probe_dapi.py:247-270` mappa `p[4]=UFF→close, p[5]=MIN→low, p[6]=MAX→high, p[7]=APE→open`. **Nessun diff**: lo schema in questa spec è identico a entrambi i decoder canonici.

> **Esclusione delle permutazioni alternative (RM-1)**
> ```
> VERIFICA: il payload CANDLE Directa ha nelle posizioni campo UFF;MIN;MAX;APE;V mappate su close;low;high;open;volume.
> PROVE: decoder canonico export_directa_history_parametric.py:471 (split parts[:9]) e :477-481 (UFF→close, MIN→low, MAX→high, APE→open), che ha già processato ~647 dump storici [CODICE-ESISTENTE]; decoder runtime probe_dapi.py:247-270 concorde; V-1 tick-by-tick del 2026-05-29 [PROVA-EMPIRICA 2026-05-29 M-1].
> ALTERNATIVE COMPATIBILI ESCLUSE: ordine wiki Directa O;H;L;C — FALSIFICATO da V-1, che sui tick realtime ha distinto Open da Close (sui soli daily O e C erano indistinguibili, da cui l'errore originale dell'incidente CANDLE). Il wiki Directa è [WIKI-HINT, da verificare], dimostrato inesatto sullo schema CANDLE.
> ALTERNATIVE COMPATIBILI NON ESCLUSE: nessuna.
> ```

**B6-R-05** — `bar_open` (Open della barra) deve essere copiato dal campo `CANDLE` `APE` (open).
*Tracciabilità*: `[CODICE-ESISTENTE export_directa_history_parametric.py:481]` (`open_v = Decimal(ape)`) + `[DOC-INTERNO CAP_09_parte_9.md:167]`. *Valore*: campo prezzo della barra normativa.

**B6-R-06** — `bar_high` (High della barra) deve essere copiato dal campo `CANDLE` `MAX` (high).
*Tracciabilità*: `[CODICE-ESISTENTE export_directa_history_parametric.py:480]` (`high_v = Decimal(max_)`) + `[DOC-INTERNO CAP_09_parte_9.md:168]`. *Valore*: campo prezzo della barra normativa.

**B6-R-07** — `bar_low` (Low della barra) deve essere copiato dal campo `CANDLE` `MIN` (low).
*Tracciabilità*: `[CODICE-ESISTENTE export_directa_history_parametric.py:479]` (`low_v = Decimal(min_)`) + `[DOC-INTERNO CAP_09_parte_9.md:169]`. *Valore*: campo prezzo della barra normativa.

**B6-R-08** — `bar_close` (Close della barra) deve essere copiato dal campo `CANDLE` `UFF` (close = prezzo ufficiale).
*Tracciabilità*: `[CODICE-ESISTENTE export_directa_history_parametric.py:478]` (`close_v = Decimal(uff)`) + `[PROVA-EMPIRICA 2026-05-29 V-1]` (M-1) + `[DOC-INTERNO CAP_09_parte_9.md:170]`. *Valore*: campo prezzo della barra normativa; Close è la base del forward-fill.

**B6-R-09** — `volume` (contratti scambiati nella barra) deve essere copiato dal campo `CANDLE` `V` (qty).
*Tracciabilità*: `[CODICE-ESISTENTE export_directa_history_parametric.py:471,482]` (`qty` da `parts[:9]`, `volume_v = int(Decimal(qty))`) + `[DOC-INTERNO CAP_09_parte_9.md:171]`. *Valore*: input per le feature di volume.

### 2.3 `tick_count` — input dell'adapter da BOOK_5 (F4)

**B6-R-10** — Il campo DAPI `CANDLE` **non espone** un `TickCount`: lo schema `CANDLE` ha 9 campi (posizioni 1-9), nessuno dei quali è il count tick.
*Tracciabilità*: `[CODICE-ESISTENTE export_directa_history_parametric.py:471]` (`parts[:9]` = `kind, symbol, ymd, hms, uff, min_, max_, ape, qty`, nessun campo tick_count) + `[DOC-INTERNO CAP_09_parte_9.md:172]`. *Valore*: chiarisce che `tick_count` è un campo **derivato** dall'adapter, non un campo nativo DAPI.

**B6-R-11** — In **regime realtime** (porta 10001), l'adapter deve derivare `tick_count` del minuto `t` come **numero di eventi `BOOK_5`** osservati nel minuto `t` sul ticker FIB front-month.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:172]`. *Valore*: proxy puntuale dell'attività di book (microstruttura), simmetrico al `tick_count` reale del training.

**B6-R-12** — In **regime storico** (porta 10003, risposta `CANDLERANGE`), l'adapter deve impostare `tick_count = NULL` (marker assente, non `NaN` numerico), perché lo schema `CANDLE` del gateway non espone tick count.
*Tracciabilità*: `[CODICE-ESISTENTE export_directa_history_parametric.py:471]` (nessun tick count nel payload) + `[DOC-INTERNO CAP_09_parte_9.md:172]`. *Valore*: separa onestamente il dato derivabile (realtime) dal dato non disponibile (storico), evitando valori inventati.

**B6-CN-01** — Il discriminante fra regime realtime e regime storico per `tick_count` deve essere la **porta sorgente** del record (10001 vs 10003), **non** il flag `bar_synthetic`.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:172]`. *Valore*: tiene separati due assi ortogonali (provenienza del dato vs presenza-di-trade), evitando confusione semantica.

### 2.4 `bar_synthetic` — input dell'adapter da BOOK_5/PRICE (F4)

**B6-CN-02** — Il flag `bar_synthetic` deve essere **booleano** e distinguere **esclusivamente trade vs no-trade**, mai realtime vs storico.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:173]`. *Valore*: invariante di dominio del flag, condizione perché il bundle frozen tratti barre live e storiche allo stesso modo.

**B6-R-13** — Per il FIB futures in **regime realtime** (porta 10001, push `BOOK_5`), la barra 1-min `t` deve essere marcata reale (`bar_synthetic = False`) se nel minuto è stato osservato almeno un evento `BOOK_5` con `bid1_lots >= 1` AND `ask1_lots >= 1`; altrimenti `bar_synthetic = True` con forward-fill del mid level-1 dell'ultima barra reale (`Open = High = Low = Close = (bid1_price + ask1_price) / 2`).
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:173,177]` + posizioni `BOOK_5` certificate (vedi B6-R-19..21). *Valore*: regola di sinteticità del FIB realtime, che governa quali barre alimentano le feature di volatilità.

**B6-R-14** — Per il FIB futures in **regime storico** (porta 10003, `CANDLERANGE`), la barra 1-min `t` deve essere marcata reale (`bar_synthetic = False`) se il timestamp `t` compare nella risposta `CANDLE` del gateway; altrimenti `bar_synthetic = True` con forward-fill su Close (`Open = High = Low = Close = Close del minuto precedente`).
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:173,178]`. *Valore*: regola di sinteticità del FIB in warm-up/backfill, simmetrica al training.

**B6-R-15** — Per i cash europei in **regime realtime** (porta 10001, push `PRICE`), la barra 1-min `t` deve essere marcata reale (`bar_synthetic = False`) se nel minuto è stato osservato almeno un evento `PRICE`; altrimenti `bar_synthetic = True` con forward-fill su `last`.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:173,179]`. *Valore*: regola di sinteticità del cash, usata solo dal layer di gating qualitativo, mai dal feature tensor del GA.

**B6-CN-03** — PRICE e BOOK_5 sono **input dell'adapter** (Cap.49), non materia del canale: l'adapter consuma `CANDLE` (OHLCV), `BOOK_5` (`tick_count` realtime + regola `bar_synthetic` del FIB) e `PRICE` (regola `bar_synthetic` del cash per il gating).
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:172-173,177-179]`. *Valore*: posiziona correttamente lo schema PRICE/BOOK_5 come schema-dato consumato dall'adapter; il canale (porte/handshake/sottoscrizione) è premessa B5 (§7).

### 2.5 Schema PRICE realtime — campi certificati e separazione per tipo-messaggio (F3, RM-1)

**B6-R-16** — Lo schema `PRICE` realtime del FIB cash ha `f4 = last`, `f6 = volume cumulato`, `f8 = day_low`, `f9 = day_high` (estremi di giornata).
*Tracciabilità*: `[PROVA-EMPIRICA 2026-06-01 W2]` (M-9) + `[DOC-INTERNO CAP_10_parte_10.md:123]` (`f8=day_low, f9=day_high`) + `[CODICE-ESISTENTE probe_dapi.py:289-306]` (decoder runtime: `last = float(p[3])`, campi extra `p[4:]` non disambiguati nel decoder). *Valore*: i campi `f8`/`f9` sono la fonte normativa del low/high giornaliero per la riconciliazione cash (§5).

> **Diff col decoder canonico (RACC-METODO-2)**: il decoder di produzione `probe_dapi.py:289-306` decodifica **solo** `last = p[3]` e tratta i campi successivi come `fields_extra = p[4:]` (commento `:290-291`: "schema esatto dei campi extra non documentato, varia tra cash e future"). Quindi la semantica di `f6`/`f8`/`f9` **non ha supporto di codice di produzione (level-2)**: è ancorata a `[PROVA-EMPIRICA 2026-06-01 W2]` (level-1) e al CAP chiuso. Il diff col decoder è esplicito: il decoder copre `last`, la semantica dei campi-estremo è certificata empiricamente, non da codice.

> **Esclusione delle permutazioni alternative su `f8`/`f9` (RM-1)**
> ```
> VERIFICA: nello schema PRICE realtime, f8=day_low e f9=day_high (estremi di giornata).
> PROVE: [PROVA-EMPIRICA 2026-06-01 W2 M-9], cross-check daily CANDLE L/H; cash untraded (DGER) → f5=f6=f7=0 con f8/f9 valorizzati.
> ALTERNATIVE COMPATIBILI ESCLUSE: (a) f8/f9 = best bid/ask — FALSIFICATA dal BOOK_5 simultaneo (M-9, STATO_CORRENTE: l'ipotesi Web "bid/ask" è smentita dal book a 5 livelli osservato nello stesso istante); (b) confusione con la coppia f8/f9 della CANDLE-daily — esclusa: f8/f9 della CANDLE daily (riconciliazione, vedi B6-R-17) e f8/f9 del PRICE realtime sono campi di DUE messaggi diversi (namespace per-tipo-messaggio), la coincidenza dell'indice NON implica namespace condiviso.
> ALTERNATIVE COMPATIBILI NON ESCLUSE: f5/f7 (contatori cumulativi) restano NON disambiguati (verifica parziale, §6 PENDING).
> ```

**B6-R-17** — Per la riconciliazione (Cap.60), il low/high ufficiale daily del FIB è preso dai campi `f8`/`f9` della **CANDLE ufficiale daily** (period 86400); questi `f8`/`f9` appartengono allo schema `CANDLE daily`, distinto dallo schema `PRICE realtime` di B6-R-16.
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:123]` + `[PROVA-EMPIRICA 2026-06-01 W2]` (M-9). *Valore*: ancora la fonte normativa del low/high per il gate di riconciliazione (§5), tenendola separata dal PRICE realtime.

**B6-CN-04** — I campi `f8`/`f9` compaiono in **due schemi distinti** (CANDLE daily per la riconciliazione; PRICE realtime per il canale): la spec li nomina **separati per tipo-messaggio** e non deduce l'uno dall'altro.
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:123]` + `[PROVA-EMPIRICA 2026-06-01 W2]` (M-9, F3). *Valore*: evita una confusione cross-schema che sarebbe un errore di tipo-incidente-CANDLE su namespace condiviso.

### 2.6 Schema BOOK_5 — posizioni certificate (RM-1, RM-2)

**B6-R-18** — Lo schema `BOOK_5` è `BOOK_5;<ticker>;<HH:mm:ss>;` seguito da **10 triple `(lots, orders, price)`** = `[BID×5 best-first][ASK×5 best-first]` (5 livelli BID poi 5 livelli ASK, ciascuno triplo).
*Tracciabilità*: `[PROVA-EMPIRICA 2026-06-01 W3]` (M-10) + `[CODICE-ESISTENTE probe_dapi.py:307-317]` (decoder runtime: `BOOK_5;<ticker>;<HH:mm:ss>; bid1_lots;bid1_ord;bid1_price; ... (x5) ask1_lots;ask1_ord;ask1_price; ... (x5)`, con `fields = p[3:]`) + `[DOC-INTERNO CAP_09_parte_9.md:93]`. *Valore*: lo schema del book è la fonte di `tick_count` e della regola `bar_synthetic` del FIB realtime.

> **Diff col decoder canonico (RACC-METODO-2)**: il decoder runtime `probe_dapi.py:307-317` documenta lo schema nel commento (`:308-309`) ma **non parsea le triple** (`fields = p[3:]`, lista grezza). Quindi le posizioni dei singoli campi **non hanno supporto level-2 strutturato**: sono certificate a livello-1 da `[PROVA-EMPIRICA 2026-06-01 W3 / M-10]` (29 eventi / 290 triple su FIB6F front-month liquido). Il diff col decoder è esplicito: il decoder conferma il commento di schema, la certificazione delle posizioni è empirica diretta.

**B6-R-19** — Nello schema `BOOK_5`, `bid1_lots` è il campo 4, `bid1_orders` il campo 5, `bid1_price` il campo 6.
*Tracciabilità*: `[PROVA-EMPIRICA 2026-06-01 W3]` (M-10) + `[CODICE-ESISTENTE probe_dapi.py:308]`. *Valore*: posizioni del primo livello BID, usate dalla regola `bar_synthetic` (B6-R-13).

**B6-R-20** — Nello schema `BOOK_5`, `ask1_lots` è il campo 19 e `ask1_price` il campo 21.
*Tracciabilità*: `[PROVA-EMPIRICA 2026-06-01 W3]` (M-10) + `[CODICE-ESISTENTE probe_dapi.py:309]` (i 5 livelli BID occupano i campi 4-18, i livelli ASK iniziano dal campo 19). *Valore*: posizioni del primo livello ASK, usate dalla regola `bar_synthetic` (B6-R-13).

**B6-R-21** — Il mid level-1 usato nel forward-fill della barra FIB realtime sintetica è `(bid1_price + ask1_price) / 2` con `bid1_price` = campo 6 e `ask1_price` = campo 21.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:173]` + `[PROVA-EMPIRICA 2026-06-01 W3]` (M-10). *Valore*: definisce il prezzo del forward-fill realtime in modo univoco sui campi certificati.

> **Esclusione delle permutazioni alternative su BOOK_5 (RM-1)**
> ```
> VERIFICA: lo schema BOOK_5 è [BID×5 best-first][ASK×5 best-first], ogni livello triplo (lots, orders, price); bid1_lots=campo4, bid1_price=campo6, ask1_lots=campo19, ask1_price=campo21.
> PROVE: [PROVA-EMPIRICA 2026-06-01 W3 M-10], 29 eventi / 290 triple su FIB6F front-month liquido [rif. reviews/REVIEW_CAP_DATA_02_RM_RETRO_CLI_review.md].
> ALTERNATIVE COMPATIBILI ESCLUSE: (a) triplo invertito (orders, lots, price) — esclusa da lots >= orders su 290/290 triple; (b) ordine dei blocchi ASK-poi-BID — escluso (blocco 1 sempre discendente = BID su 29/29 eventi); (c) inversione di schema suggerita dall'anomalia bid1>ask1 del campione 27/05 — esclusa: NON riprodotta sul front-month liquido (bid1_price < ask1_price su 29/29), era artefatto del contratto illiquido FIB6I a scadenza lontana, non inversione di schema.
> ALTERNATIVE COMPATIBILI NON ESCLUSE: nessuna sulle posizioni qui asserite.
> ```

### 2.7 Format/header come contesto (Cap.48 — framing, non requisito standalone)

**B6-CN-05** — Ogni file CSV prodotto dalla pipeline runtime ha header esteso a **13 campi esatti**: `symbol, timeframe, timestamp, date, time, open, high, low, close, volume, tick_count, bar_synthetic, source`.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:117,120]`. *Valore*: contenitore canonico del format runtime; i 13 campi sono enumerati esattamente (no abbreviazioni).

**B6-CN-06** — Il format runtime esteso (13 campi, con `tick_count`/`bar_synthetic`) è distinto dal format **legacy** a 11 campi (`symbol, timeframe, timestamp, date, time, open, high, low, close, volume, source`, senza `tick_count` e `bar_synthetic`).
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:129]` + `[CODICE-ESISTENTE export_directa_history_parametric.py:605-617]` (header legacy del decoder: i 11 campi senza tick_count/bar_synthetic). *Valore*: i due format coabitano; la distinzione evita di rompere la riproducibilità dei sample legacy.

**B6-CN-07** — La colonna `tick_count` del CSV è intero ≥ 0 oppure `NULL`; la colonna `bar_synthetic` è booleano `True`/`False`.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:117]`. *Valore*: vincolo di dominio dei due campi che rendono il CSV simmetrico al bundle frozen.

**B6-CN-08** — Il campo `source` di ogni record CSV runtime (Cap.48) ha dominio chiuso a tre valori: `DIRECTA`, `AGG_FROM_60s`, `AGG_FROM_D`.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:131-138]`. *Valore*: traccia la provenienza del record; è il dominio-base esteso poi dalla storicizzazione (§6).

**B6-CN-09** — Il campo `timestamp` è la chiave normativa di allineamento temporale della griglia 1-min; `date` e `time` sono campi derivati di comodità.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:125]`. *Valore*: definisce la chiave di join/allineamento downstream.

---

## 3. Replay deterministico (invariante research = runtime)

### 3.1 Fondazione formale (premessa CAP_02 Cap.10)

**B6-NFR-01** — Il replay del motore deve essere **bit-exact**: a parità di storico delle barre 1-min, di feed ausiliari e di bundle frozen, due esecuzioni indipendenti producono esattamente la stessa sequenza di emissioni, `signal_id`, transizioni di stato e timestamp di transizione.
*Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:291,293]` (premessa, fondazione formale). *Valore*: condizione necessaria perché le metriche di lifecycle abbiano valore probatorio. **Nota di rinvio**: la fondazione formale del replay bit-exact è materia di `CAP_02 Cap.10` (premessa); qui è **consolidata come invariante che l'adapter preserva**, non ri-derivata dal motore.

### 3.2 Applicazione runtime dell'invariante all'adapter

**B6-NFR-02** — L'adapter DAPI deve preservare l'invariante `research semantics = runtime semantics`: la griglia 1-min prodotta in runtime ha lo stesso schema operativo del tape di training, senza re-calibrazione e senza re-mappatura dello schema.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:21]` (preambolo: replay bit-exact applicato al motore in produzione) + premessa `[DOC-INTERNO CAP_02_parte_II.md:291]`. *Valore*: estende l'invariante formale al layer di ingest, garantendo che il bundle non distingua training da runtime.

**B6-NFR-03** — Il replay runtime deve propagare in modo identico la distinzione fra barre reali e barre sintetiche (`bar_synthetic`) tra due esecuzioni indipendenti sulla medesima finestra storica DAPI.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:21]`. *Valore*: la riproducibilità del flag `bar_synthetic` è precondizione del determinismo delle feature di volatilità.

**B6-NFR-04** — Il flag `bar_synthetic` deve essere propagato nei record runtime del bundle frozen esattamente come nel training, preservando il vincolo di replay bit-exact.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:181]` + premessa `[DOC-INTERNO CAP_02_parte_II.md:293]`. *Valore*: chiude il cerchio fra regola di sinteticità (§2.4) e invariante di replay (§3.1).

---

## 4. Warm-up & continuità (Cap.51, Cap.59, Cap.61)

### 4.1 Warm-up degli stati condizionali (Cap.51)

**B6-R-22** — Al boot di ogni sessione operativa, la pipeline deve eseguire un **warm-up** degli stati condizionali via pull storico `CANDLERANGE` su porta 10003, con lookback `L_warmup = 30` **giorni di trading IDEM** (valore congelato in Parte 9, NB-4 Opzione A).
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:254]` + sintassi comando `[CODICE-ESISTENTE export_directa_history_parametric.py:228-230]` (`CANDLERANGE <symbol> <start> <end> <period_seconds>`). *Valore*: re-inizializza EGARCH, classificazione di regime e normalizzazione prima che il motore emetta segnali. Il valore `L_warmup = 30` è **esatto** (non "~30").

**B6-CN-10** — Il valore `L_warmup = 30` giorni di trading è **congelato** dentro la metodologia: ogni revisione richiede un nuovo task Planner (rollback non reversibile dentro la Parte).
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:254]`. *Valore*: vincolo di immutabilità del parametro di warm-up.

**B6-R-23** — Al completamento del warm-up, la pipeline deve inserire il marker `WARMUP_COMPLETE` nel log di audit; solo da quel momento entra in regime steady-state e può emettere segnali validi.
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:257]`. *Valore*: gate che impedisce emissioni con stato condizionato non inizializzato.

**B6-CN-11** — Il warm-up deve ricalcolare solo lo **stato condizionato corrente** (es. la varianza condizionata corrente, il quantile di regime sulla finestra storica), mantenendo **congelati** i parametri EGARCH cross-session del bundle frozen (nessuna re-calibrazione).
*Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:256]`. *Valore*: distingue ri-inizializzazione di stato da re-calibrazione, preservando il bundle frozen.

### 4.2 Recupero gap entro la finestra 100gg (Cap.59)

**B6-R-24** — Per gap di durata ≤ ~100 giorni di calendario, la pipeline deve recuperare le barre mancanti via richiesta `CANDLERANGE` su porta 10003 (sintassi: `CANDLERANGE <ticker_front_month> <YYYYMMDDHHMMSS_start> <YYYYMMDDHHMMSS_end> 60`, period in ultima posizione).
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:88]` + `[CODICE-ESISTENTE export_directa_history_parametric.py:228-230]`. *Valore*: ripristina la continuità del tape entro la finestra coperta dal DAPI intraday.

**B6-CN-12** — La finestra di recupero `CANDLERANGE` intraday (period 60) è limitata a ~100 giorni di calendario (finestra scorrevole che tronca al minuto esatto del limite).
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:79-83]` (`[PROVA-EMPIRICA 2026-05-29 V-2]`: saturazione del first_ts a partire da N=80) + `[CODICE-ESISTENTE export_directa_history_parametric.py:61]` (`DEFAULT_INTRADAY_MAX_DAYS = 100`). *Valore*: definisce il confine fra recupero-gap (≤100gg) e restart-stale (>100gg).

**B6-R-25** — Le barre ricostruite dal backfill `CANDLERANGE` devono essere inserite nella griglia 1-min con `source = BACKFILL_FROM_CANDLERANGE`, `bar_synthetic` derivato dalla regola Cap.49 (B6-R-14) e `tick_count = NULL` (regime storico).
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:91]`. *Valore*: traccia la provenienza del backfill mantenendo lo schema invariato.

**B6-R-26** — Il recupero gap deve essere **idempotente**: una barra ricostruita che coincide con una già archiviata è un no-op; una divergenza apre una nuova versione dell'archivio (Cap.62), non sovrascrive.
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:90]`. *Valore*: protegge l'integrità dell'archivio dai backfill ripetuti.

**B6-CN-13** — Se un gap attraversa il limite ~100gg, la pipeline deve recuperare la parte entro finestra e marcare il complemento fuori finestra con `RUNTIME_GAP_BEYOND_100D`, instradandolo al fallback di restart >100gg (B6-R-27).
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:98]`. *Valore*: gestione esplicita del caso-limite parziale, senza perdita silenziosa di copertura.

### 4.3 Restart >100gg (Cap.61) — requisito distinto (N1, F5)

**B6-R-27** — Per downtime continuativo > 100 giorni (oltre la finestra `CANDLERANGE` intraday), la pipeline deve entrare nello stato `RUNTIME_STALE_RESTART` e **non ripartire automaticamente** (intervento del supervisore obbligatorio).
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:157-158]` + `[DOC-INTERNO CAP_09_parte_9.md:260-261]`. *Valore*: protegge il motore dall'esecuzione su un warm-up cross-source non sufficiente. **Requisito distinto** da B6-R-24 (recupero-gap entro finestra): trigger, scala temporale e capitolo diversi (N1, F5).

**B6-R-28** — Nel re-bootstrap >100gg, la copertura del periodo di gap deve seguire una procedura a tre step in ordine: (A) recupero da archivio locale `exports/` con `source = BACKFILL_FROM_ARCHIVE`; (B) recupero `CANDLERANGE` daily (period 86400) per cross-check di riconciliazione; (C) fallback all'archivio Portara/CQG con `source = BACKFILL_FROM_PORTARA`.
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:158-161]`. *Valore*: scala dei fallback dal dato più locale al dato di training, massimizzando la copertura.

**B6-CN-14** — La `CANDLERANGE` daily (period 86400) non ha il cut-off ~100gg dell'intraday: il first_ts regredisce col crescere di N, permettendo cross-check di riconciliazione retroattiva su profondità pluriennale.
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:168-170]` (`[PROVA-EMPIRICA 2026-05-29 V-2]`: first_ts daily non satura fino a N=160). *Valore*: distingue il daily (cross-check profondo) dall'intraday (limitato a 100gg); il daily NON è surrogato delle barre 1-min.

**B6-R-29** — Dopo il re-bootstrap >100gg è **obbligatorio** un re-warm-up completo (`L_warmup = 30` giorni di trading), eseguito solo dopo che il periodo di gap è coperto (step A/B/C completati); al completamento, marker `BOOTSTRAP_COMPLETE`.
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:162]`. *Valore*: garantisce che il bundle EGARCH non venga mai eseguito su un tape mescolato cross-source senza re-warm-up.

**B6-CN-15** — Durante il re-bootstrap >100gg, il tape non è ammesso come input dell'inference live (la pipeline resta in `RUNTIME_STALE_RESTART`); solo dopo `BOOTSTRAP_COMPLETE` + `WARMUP_COMPLETE` la pipeline può tornare a emettere segnali.
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:163-164]`. *Valore*: vincolo di non-mescolamento che impedisce emissioni durante il bootstrap.

**B6-CN-16** — Le barre Portara dello step C entrano convertite alla convenzione **runtime** (unadjusted nativa del front-month corrente), NON ratio-adjusted (che è convenzione di training).
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:161,174]`. *Valore*: preserva la coerenza di back-adjustment fra tape archiviato e convenzione runtime, senza violare l'invariante.

---

## 5. Riconciliazione canonica giornaliera (Cap.60)

**B6-R-30** — A fine sessione (chiusura 22:00 CET, marker `SESSION_CLOSE`), la pipeline deve eseguire la **riconciliazione canonica giornaliera** come gate operativo end-of-day sul tape del giorno `d`.
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:119]`. *Valore*: verifica end-of-day che protegge contro la deriva silenziosa del feed.

**B6-R-31** — La riconciliazione deve verificare l'integrità di schema: header CSV esteso (13 campi), dominio `source` esteso, dominio `bar_synthetic` booleano, presenza di tutti gli 840 timestamp 1-min attesi, monotonia temporale stretta; il fallimento produce il marker `RECONCILE_SCHEMA_FAIL` + notifica supervisore.
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:121]`. *Valore*: primo check del gate, blocca tape strutturalmente malformati.

**B6-R-32** — La riconciliazione deve verificare la coerenza CANDLE 1-min: il tape composto del giorno `d` è confrontato con una `CANDLERANGE` di controllo dello stesso giorno; divergenza oltre tolleranza (≤1 tick = ≤5pt FIB) su più di `θ_reconcile` minuti produce il marker `RECONCILE_DIVERGENT_FIB` + notifica supervisore.
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:122]`. *Valore*: secondo check del gate, intercetta divergenze diffuse sui minuti.

**B6-R-33** — La riconciliazione deve verificare il low/high giornaliero del FIB confrontandolo con i campi `day_low`/`day_high` (`f8`/`f9`) della CANDLE ufficiale daily (period 86400), tolleranza ≤1 tick FIB (5pt); divergenza oltre tolleranza produce `RECONCILE_DIVERGENT_HIGHLOW`.
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:123]` + `[PROVA-EMPIRICA 2026-06-01 W2]` (M-9). *Valore*: terzo check del gate, verifica gli estremi di giornata.

**B6-CN-17** — Per i ticker cash europei, la riconciliazione del low/high deve usare **esclusivamente** la CANDLE ufficiale daily (`f8`/`f9`), **mai** l'aggregato dei tick realtime, perché il feed `PRICE` cash è rado e perde i minimi intraday.
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:123,136-139]` (`[PROVA-EMPIRICA 2026-06-01 V-1 afternoon §2.4.5]`: 6/6 mismatch DITAS sul solo low). *Valore*: evita falsi `RECONCILE_DIVERGENT_HIGHLOW` dovuti alla radezza del feed cash.

**B6-R-34** — Il verdetto della riconciliazione deve essere la **congiunzione** dei tre check (integrità schema, coerenza CANDLE 1-min, coerenza low/high): `RECONCILE_OK` se tutti passano; `RECONCILE_DIVERGENT_*` se uno o più check di coerenza falliscono; `RECONCILE_DEGRADED` se il tape è incompleto.
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:124-127]`. *Valore*: regola di propagazione fail-stop del gate.

**B6-CN-18** — In caso di `RECONCILE_DIVERGENT_*`, la pipeline deve impostare un flag che **blocca l'emissione di segnali del giorno `d+1`** finché il supervisore non interviene (gate operativo bloccante).
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:126]`. *Valore*: protezione operativa contro l'emissione di segnali su un feed la cui coerenza è in dubbio.

**B6-CN-19** — La riconciliazione deve essere **non-mutativa** sui prezzi delle barre composte (layer di sola verifica che emette marker), preservando il replay deterministico.
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:146]` + premessa `[DOC-INTERNO CAP_02_parte_II.md:291]`. *Valore*: garantisce che il gate non introduca non-determinismo modificando il tape.

**B6-CN-20** — La soglia `θ_reconcile` è un **parametro provvisorio non congelato**, la cui calibrazione fine è rinviata a FASE-D; nessun valore numerico è fissato qui.
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:131]`. *Valore*: dichiara onestamente che la soglia è ancora da calibrare, senza inventare numeri.

---

## 6. Storicizzazione strutturata del tape (Cap.62)

**B6-R-35** — Il tape DAPI runtime deve confluire in un **archivio canonico locale** con struttura cartelle `exports/directa_history/<TICKER>_<START_YYYYMMDD>_<END_YYYYMMDD>/` (una cartella per ticker per finestra temporale chiusa).
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:184]` + `[CODICE-ESISTENTE export_directa_history_parametric.py]` (pattern di cartella del decoder di riferimento). *Valore*: organizzazione persistente del tape per riconciliazione, replay e bootstrap futuro.

**B6-R-36** — I file CSV dell'archivio devono usare l'header **runtime esteso a 13 campi** (`symbol, timeframe, timestamp, date, time, open, high, low, close, volume, tick_count, bar_synthetic, source`), NON il format legacy a 11 campi.
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:185]`. *Valore*: simmetria con il bundle frozen Portara; coerenza con il format runtime (§2.7).

**B6-R-37** — Ogni esecuzione di archiviazione deve produrre un **manifest JSON** con i campi ereditati Cap.48 (`symbol`, `start_date`, `end_date`, `host`, `port_historic`, `account_code` mascherabile, `banner_darwin`, `config_resolved`; per timeframe: `mode`, `rows_received`, `first_timestamp`, `last_timestamp`, `commands_sent`, `warnings`) più le estensioni Parte 10 (`reconcile_status`, `bar_counts_by_source`, `gap_log`, `partial`, `bootstrap_completed_at`).
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:186-188]`. *Valore*: corredo auditabile per il replay deterministico e la tracciabilità della provenienza.

**B6-CN-21** — Il dominio `source` dell'archivio estende quello di Cap.48 con tre nuovi valori (`BACKFILL_FROM_CANDLERANGE`, `BACKFILL_FROM_ARCHIVE`, `BACKFILL_FROM_PORTARA`), come **complemento** (non sostituzione) dei tre valori Cap.48 (`DIRECTA`, `AGG_FROM_60s`, `AGG_FROM_D`).
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:194,196-203]`. *Valore*: traccia la provenienza delle barre ricostruite senza rompere il dominio-base.

**B6-CN-22** — La scrittura dell'archivio deve essere **append-only**: la scrittura di un giorno `d` già archiviato è un no-op se identico; se divergente, apre una nuova versione (`version = N+1` nel manifest), mai sovrascrittura.
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:207]`. *Valore*: immutabilità dell'archivio, condizione per il replay retroattivo.

**B6-CN-23** — La provenienza "barra del flusso nominale vs barra ricostruita via backfill" deve essere catturata interamente dal campo `source`, non dal flag `bar_synthetic`: il bundle frozen ignora `source` nel calcolo delle feature (legge solo OHLCV + `tick_count` + `bar_synthetic`).
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:68]`. *Valore*: preserva l'invariante research=runtime — il motore non distingue una barra live da una ricostruita.

**B6-CN-24** — L'archivio del tape DAPI **NON è fonte di training** del bundle: serve esclusivamente per riconciliazione, replay e bootstrap futuro; l'apertura del flusso DAPI come fonte di training richiederebbe un nuovo task Planner con riesame di Cap.38/Cap.39.
*Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:209]` + premessa `[DOC-INTERNO CAP_08_parte_8.md Cap.44]`. *Valore*: vincolo negativo hard-locked; tiene separato lo strumento di calibrazione (Portara ratio-adjusted) dal tape runtime archiviato.

---

## 7. Matrice di tracciabilità, nota di rinvio, PENDING-empirico, nota RM-3

### 7.1 Matrice di tracciabilità

| ID | Proposizione (sintesi) | Fonte primaria | Capitolo v2 |
|----|------------------------|----------------|-------------|
| B6-R-01 | Adapter DAPI → schema bundle frozen | `[DOC-INTERNO CAP_09_parte_9.md:153]` | Cap.49 |
| B6-R-02 | Adapter = normalizzazione schema, non traduzione | `[DOC-INTERNO CAP_09_parte_9.md:191]` | Cap.49 |
| B6-R-03 | Griglia 1-min uniforme + forward-fill | `[DOC-INTERNO CAP_09_parte_9.md:127]` | Cap.48/49 |
| B6-R-04 | Schema CANDLE `C;L;H;O;V` | `[CODICE-ESISTENTE export_directa_history_parametric.py:477-481]` + `[CODICE-ESISTENTE probe_dapi.py:247-270]` + `[PROVA-EMPIRICA 2026-05-29 V-1]` | Cap.49 |
| B6-R-05 | bar_open ← APE | `[CODICE-ESISTENTE export_directa_history_parametric.py:481]` | Cap.49 |
| B6-R-06 | bar_high ← MAX | `[CODICE-ESISTENTE export_directa_history_parametric.py:480]` | Cap.49 |
| B6-R-07 | bar_low ← MIN | `[CODICE-ESISTENTE export_directa_history_parametric.py:479]` | Cap.49 |
| B6-R-08 | bar_close ← UFF | `[CODICE-ESISTENTE export_directa_history_parametric.py:478]` + `[PROVA-EMPIRICA 2026-05-29 V-1]` | Cap.49 |
| B6-R-09 | volume ← V | `[CODICE-ESISTENTE export_directa_history_parametric.py:471,482]` | Cap.49 |
| B6-R-10 | CANDLE non espone TickCount | `[CODICE-ESISTENTE export_directa_history_parametric.py:471]` | Cap.49 |
| B6-R-11 | tick_count realtime ← #eventi BOOK_5 | `[DOC-INTERNO CAP_09_parte_9.md:172]` | Cap.49 |
| B6-R-12 | tick_count storico = NULL | `[CODICE-ESISTENTE export_directa_history_parametric.py:471]` | Cap.49 |
| B6-CN-01 | discriminante regime = porta sorgente | `[DOC-INTERNO CAP_09_parte_9.md:172]` | Cap.49 |
| B6-CN-02 | bar_synthetic booleano trade/no-trade | `[DOC-INTERNO CAP_09_parte_9.md:173]` | Cap.49 |
| B6-R-13 | regola bar_synthetic FIB realtime (BOOK_5) | `[DOC-INTERNO CAP_09_parte_9.md:173,177]` | Cap.49 |
| B6-R-14 | regola bar_synthetic FIB storico (CANDLERANGE) | `[DOC-INTERNO CAP_09_parte_9.md:173,178]` | Cap.49 |
| B6-R-15 | regola bar_synthetic cash (PRICE) | `[DOC-INTERNO CAP_09_parte_9.md:173,179]` | Cap.49 |
| B6-CN-03 | PRICE/BOOK_5 = input adapter (F4) | `[DOC-INTERNO CAP_09_parte_9.md:172-173,177-179]` | Cap.49 |
| B6-R-16 | schema PRICE: f4/f6/f8/f9 | `[PROVA-EMPIRICA 2026-06-01 W2]` + `[DOC-INTERNO CAP_10_parte_10.md:123]` + `[CODICE-ESISTENTE probe_dapi.py:289-306]` | Cap.60 |
| B6-R-17 | low/high daily ← CANDLE daily f8/f9 | `[DOC-INTERNO CAP_10_parte_10.md:123]` + `[PROVA-EMPIRICA 2026-06-01 W2]` | Cap.60 |
| B6-CN-04 | f8/f9 separati per tipo-messaggio (F3) | `[DOC-INTERNO CAP_10_parte_10.md:123]` + `[PROVA-EMPIRICA 2026-06-01 W2]` | Cap.60 |
| B6-R-18 | schema BOOK_5 [BID×5][ASK×5] triple | `[PROVA-EMPIRICA 2026-06-01 W3]` + `[CODICE-ESISTENTE probe_dapi.py:307-317]` | Cap.49 |
| B6-R-19 | bid1_lots=4, bid1_orders=5, bid1_price=6 | `[PROVA-EMPIRICA 2026-06-01 W3]` + `[CODICE-ESISTENTE probe_dapi.py:308]` | Cap.49 |
| B6-R-20 | ask1_lots=19, ask1_price=21 | `[PROVA-EMPIRICA 2026-06-01 W3]` + `[CODICE-ESISTENTE probe_dapi.py:309]` | Cap.49 |
| B6-R-21 | mid level-1 = (bid1_price+ask1_price)/2 | `[DOC-INTERNO CAP_09_parte_9.md:173]` + `[PROVA-EMPIRICA 2026-06-01 W3]` | Cap.49 |
| B6-CN-05 | header CSV 13 campi esatti | `[DOC-INTERNO CAP_09_parte_9.md:117,120]` | Cap.48 |
| B6-CN-06 | format esteso ≠ legacy 11 campi | `[DOC-INTERNO CAP_09_parte_9.md:129]` + `[CODICE-ESISTENTE export_directa_history_parametric.py:605-617]` | Cap.48 |
| B6-CN-07 | dominio tick_count/bar_synthetic | `[DOC-INTERNO CAP_09_parte_9.md:117]` | Cap.48 |
| B6-CN-08 | dominio source base (3 valori) | `[DOC-INTERNO CAP_09_parte_9.md:131-138]` | Cap.48 |
| B6-CN-09 | timestamp = chiave allineamento | `[DOC-INTERNO CAP_09_parte_9.md:125]` | Cap.48 |
| B6-NFR-01 | replay bit-exact (fondazione) | `[DOC-INTERNO CAP_02_parte_II.md:291,293]` | Cap.10 (premessa) |
| B6-NFR-02 | adapter preserva research=runtime | `[DOC-INTERNO CAP_09_parte_9.md:21]` + `[DOC-INTERNO CAP_02_parte_II.md:291]` | Cap.49 / Cap.10 |
| B6-NFR-03 | replay propaga bar_synthetic identico | `[DOC-INTERNO CAP_09_parte_9.md:21]` | Cap.49 |
| B6-NFR-04 | bar_synthetic propagato come training | `[DOC-INTERNO CAP_09_parte_9.md:181]` + `[DOC-INTERNO CAP_02_parte_II.md:293]` | Cap.49 / Cap.10 |
| B6-R-22 | warm-up L_warmup=30gg trading | `[DOC-INTERNO CAP_09_parte_9.md:254]` + `[CODICE-ESISTENTE export_directa_history_parametric.py:228-230]` | Cap.51 |
| B6-CN-10 | L_warmup=30 congelato | `[DOC-INTERNO CAP_09_parte_9.md:254]` | Cap.51 |
| B6-R-23 | marker WARMUP_COMPLETE | `[DOC-INTERNO CAP_09_parte_9.md:257]` | Cap.51 |
| B6-CN-11 | warm-up ricalcola stato, non parametri | `[DOC-INTERNO CAP_09_parte_9.md:256]` | Cap.51 |
| B6-R-24 | recupero gap ≤100gg via CANDLERANGE | `[DOC-INTERNO CAP_10_parte_10.md:88]` + `[CODICE-ESISTENTE export_directa_history_parametric.py:228-230]` | Cap.59 |
| B6-CN-12 | finestra intraday ~100gg | `[DOC-INTERNO CAP_10_parte_10.md:79-83]` + `[CODICE-ESISTENTE export_directa_history_parametric.py:61]` | Cap.59 |
| B6-R-25 | barre backfill: source/bar_synthetic/tick_count | `[DOC-INTERNO CAP_10_parte_10.md:91]` | Cap.59 |
| B6-R-26 | recupero gap idempotente | `[DOC-INTERNO CAP_10_parte_10.md:90]` | Cap.59 |
| B6-CN-13 | gap che attraversa 100gg → BEYOND_100D | `[DOC-INTERNO CAP_10_parte_10.md:98]` | Cap.59 |
| B6-R-27 | restart >100gg = RUNTIME_STALE_RESTART | `[DOC-INTERNO CAP_10_parte_10.md:157-158]` + `[DOC-INTERNO CAP_09_parte_9.md:260-261]` | Cap.61 |
| B6-R-28 | re-bootstrap 3 step (archivio/daily/Portara) | `[DOC-INTERNO CAP_10_parte_10.md:158-161]` | Cap.61 |
| B6-CN-14 | CANDLERANGE daily senza cut-off 100gg | `[DOC-INTERNO CAP_10_parte_10.md:168-170]` | Cap.61 |
| B6-R-29 | re-warm-up obbligatorio + BOOTSTRAP_COMPLETE | `[DOC-INTERNO CAP_10_parte_10.md:162]` | Cap.61 |
| B6-CN-15 | non-mescolamento durante re-bootstrap | `[DOC-INTERNO CAP_10_parte_10.md:163-164]` | Cap.61 |
| B6-CN-16 | Portara step C = unadjusted nativa | `[DOC-INTERNO CAP_10_parte_10.md:161,174]` | Cap.61 |
| B6-R-30 | gate riconciliazione EOD | `[DOC-INTERNO CAP_10_parte_10.md:119]` | Cap.60 |
| B6-R-31 | check integrità schema | `[DOC-INTERNO CAP_10_parte_10.md:121]` | Cap.60 |
| B6-R-32 | check coerenza CANDLE 1-min | `[DOC-INTERNO CAP_10_parte_10.md:122]` | Cap.60 |
| B6-R-33 | check low/high via f8/f9 daily | `[DOC-INTERNO CAP_10_parte_10.md:123]` + `[PROVA-EMPIRICA 2026-06-01 W2]` | Cap.60 |
| B6-CN-17 | cash low/high SOLO da CANDLE daily | `[DOC-INTERNO CAP_10_parte_10.md:123,136-139]` | Cap.60 |
| B6-R-34 | verdetto = congiunzione 3 check | `[DOC-INTERNO CAP_10_parte_10.md:124-127]` | Cap.60 |
| B6-CN-18 | gate bloccante su emissione d+1 | `[DOC-INTERNO CAP_10_parte_10.md:126]` | Cap.60 |
| B6-CN-19 | riconciliazione non-mutativa | `[DOC-INTERNO CAP_10_parte_10.md:146]` + `[DOC-INTERNO CAP_02_parte_II.md:291]` | Cap.60 / Cap.10 |
| B6-CN-20 | θ_reconcile provvisorio non congelato | `[DOC-INTERNO CAP_10_parte_10.md:131]` | Cap.60 |
| B6-R-35 | archivio canonico locale (struttura) | `[DOC-INTERNO CAP_10_parte_10.md:184]` + `[CODICE-ESISTENTE export_directa_history_parametric.py]` | Cap.62 |
| B6-R-36 | CSV archivio header esteso 13 campi | `[DOC-INTERNO CAP_10_parte_10.md:185]` | Cap.62 |
| B6-R-37 | manifest JSON esteso | `[DOC-INTERNO CAP_10_parte_10.md:186-188]` | Cap.62 |
| B6-CN-21 | source esteso (+3 BACKFILL_*) complemento | `[DOC-INTERNO CAP_10_parte_10.md:194,196-203]` | Cap.62 |
| B6-CN-22 | archivio append-only / versioning | `[DOC-INTERNO CAP_10_parte_10.md:207]` | Cap.62 |
| B6-CN-23 | provenienza da source, non bar_synthetic | `[DOC-INTERNO CAP_10_parte_10.md:68]` | Cap.62/58 |
| B6-CN-24 | tape NON fonte training (vincolo negativo) | `[DOC-INTERNO CAP_10_parte_10.md:209]` + premessa `CAP_08 Cap.44` | Cap.62 |

### 7.2 Nota di rinvio (premesse / fuori-scope)

| Materia | Destinazione |
|---|---|
| Canale DAPI: porte/handshake/sottoscrizione/loopback (Cap.46/47) | **B5** — premessa (origine del dato). B6 consolida lo schema/decodifica e l'uso nell'adapter, non il canale. |
| Eventi audit (`CANDLE_RESPONSE`, `BOOK_RESPONSE`, …) (Cap.54) | **B5** — premessa. B6 tratta lo schema, non gli eventi-audit. |
| Riconciliazione tape↔runtime, versante runtime-tape | **Parte 10 / CAP-DATA-03** (chiuso PASS) — premessa. |
| Preprocessor / back-adjustment Portara, ratio-adjusted, filtro pre-expiry (Cap.40/38/39) | **Parte 8** — premessa. B6 non ri-deriva il preprocessing di training. |
| State machine / lifecycle del segnale | **B3** — premessa. |
| Determinismo bit-exact (invariante formale) | **premessa `CAP_02 Cap.10`** — consolidato come invariante che l'adapter preserva (B6-NFR-01..04), non ri-derivato dal motore. |
| `Cap.48` format canonico | **framing/contesto** (contenitore CSV 13 campi/manifest) — consolidato come vincoli di contenitore (B6-CN-05..09), non requisito standalone slegato dall'adapter/archivio. |
| Tape come fonte training | **fuori scope** (vincolo D-10-9; eredita Parte 8 Cap.44 + Parte 9 Cap.55) — consolidato come vincolo negativo B6-CN-24. |

**F7 — due "restart" distinti**:
- **Riavvio Darwin a mezzanotte** (Cap.50, Gap-3): manutenzione del gateway, continuità infra-giornaliera → **premessa B5** (recovery del canale). B6 lo cita come premessa, non lo consolida.
- **`RUNTIME_STALE_RESTART`** (Cap.61, >100gg): staleness oltre la finestra di recupero DAPI, richiede re-bootstrap → **in-scope B6** (B6-R-27..29, CN-14..16).

Sono concetti diversi (trigger, scala temporale, capitolo): tenuti distinti, non conflati.

### 7.3 Lista PENDING-empirico (marcare, NON asserire — AC-B6-4)

I seguenti elementi NON sono asseriti come certi in questo documento; sono marcati come pendenti perché non disambiguati dalle prove disponibili:

- **PE-1 — Codici mese Directa-IDEM Mar/Dic**: contratti non listati al 2026-06-01 (→ `1007`); non decodificabili finché non quotati. PENDING-empirico (ANAG a mercato aperto, Cap.55/64). *(Solo `F`=giugno e `I`=settembre sono certificati, vedi nota RM-3.)*
- **PE-2 — Ticker 1030** (realtime non sottoscritto): IDEM nel servizio base, non riprodotto sul FIB → verifica parziale / PHASE-2 gated.
- **PE-3 — Riavvio Darwin a mezzanotte**: comportamento notturno → PENDING-empirico (premessa B5, vedi F7; residuo Empirico-CLI di Cap.50 Gap-3, `[DOC-INTERNO CAP_10_parte_10.md:233]`).
- **PE-4 — PRICE `f5`/`f7`** (contatori cumulativi): non disambiguati → marcati, non si asserisce semantica.
- **PE-5 — Base calendario-vs-giorni-di-trading delle finestre 30/100** (V-2): la resa in giorni-di-calendario della convenzione "30 giorni di trading" / "100 giorni" era V-2 PENDING-empirico (eredità B5) → marcata. **Il valore `L_warmup = 30` è congelato (non pending)**; è pendente solo la sua mappatura sul calendario IDEM.

**NON pending** (certificati, citati con stato esatto, da non sovra-marcare): schema CANDLE `C;L;H;O;V`; PRICE `f8`/`f9`/`f6`; BOOK_5 (290/290 triple, 29/29 eventi); mesi `F`=giugno / `I`=settembre; codici errore `1004`/`1007`/`1017`/`1015`/`1003`; `L_warmup = 30` (valore congelato); 13 campi header.

### 7.4 Nota RM-3 (gerarchia delle fonti)

Tutti i claim strutturali di questo documento poggiano su `[PROVA-EMPIRICA]` (livello 1), `[CODICE-ESISTENTE]` (livello 2) o `[DOC-INTERNO]` capitolo v2 chiuso PASS (livello 3). **Nessuna conclusione strutturale poggia sul solo wiki Directa** (livello 4): il wiki Directa è dimostrato inesatto sullo schema CANDLE (ordine `O;H;L;C` falsificato) ed è trattato come `[WIKI-HINT, da verificare]` ovunque, mai come ultima parola. I codici mese Directa-IDEM seguono una convenzione **NON-standard** (`F`=giugno ≠ standard CME): nessuna inferenza per analogia con CME.

---

*Documento B6 prodotto dallo spec_developer del track Business-spec, cieco rispetto a SPEC_FUNZ_01 v2/v1 e ai documenti B1..B5, con eccezione RM-2 sui decoder di produzione e sugli audit empirici. ID `B6-*` auto-assegnati da zero, nessun conteggio-target. 61 requisiti: 37 R + 20 CN + 4 NFR.*
