# Review AUDIT-RM-RETRO CAP-DATA-02 (Parte 9) — perimetro A-D

**Sede**: WEB
**Natura**: audit retroattivo RM-1/2/3 + coerenza A/C ↔ D-canonico (NON CAP-review piena — Parte 9 è già PASS storico hash `86425a7`; NON probe-review standard — qui si audita simultaneamente 1 CAP storico + 1 report supervisore + 1 documento-indagine sorgente + 1 decoder canonico di riferimento)
**Commit base auditato**: `f7d9b22` (origin/main — task card Planner; A/B/C/D nello stato pubblicato su `origin/main`)
**Ruolo Reviewer assunto da agente general-purpose** (subagente nativo `reviewer` non disponibile nell'ambiente; ruolo adottato in pieno secondo `.claude/agents/reviewer.md`, incluse regole assolute, sezione "Probe-review (RM-4)" e divieti per sede `:163-164`).

**Perimetro auditato**:
- A = `docs/methodology_v2/CAP_09_parte_9.md`
- B = `reports/REPORT_CAP_09.md`
- C = `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md` (Appendici A/B)
- D = `scripts/export_directa_history_parametric.py` (decoder canonico, fonte CODICE-ESISTENTE level-2 — NON modificabile in questo task)

**Cross-reference fuori perimetro (citate, NON auditate)**:
- `scripts/probe_dapi.py` — decoder post-rettifica `a12ae32`, già auditato in CAP-DATA-01 PASS, citato come supporto level-2.
- `docs/runtime/dapi_port_settings_schema.md` — schema `APIPortSettings.txt`, citato come referente DOC-INTERNO level-3 di A Cap.46.
- M-1/M-3/M-4/M-5 di `tasks/STATO_CORRENTE.md` §5 — `[PROVA-EMPIRICA 2026-05-29]` acquisite tramite M-promemoria (forma versionata della prova), NON ispezionate direttamente (dump `probe_out/*` locali non versionati).

---

## VERDETTO: FAIL (Sede: WEB)

**Motivazione sintetica.** Il check critico W1 (schema CANDLE) è **FALLITO con BUG REALE catastrofico**: la tabella di mappatura canonica di A Cap.49 r158-162 dichiara l'ordine campi DAPI `O;H;L;C;V` (l'ordine del wiki Directa, **dimostrato inesatto** da M-1), mentre il decoder canonico di produzione D `:477-481` (e il decoder post-fix `probe_dapi.py:264-267`, e la prova empirica M-1) dichiarano `C;L;H;O;V`. **Tutti e quattro i campi OHLC sono mappati sulla posizione sbagliata** in A (O↔C scambiati E H↔L scambiati). È **esattamente l'errore originale §3.1** che ha motivato RM-1/2/3, sopravvissuto dentro il CAP-XX — e sopravvissuto persino al ciclo Review v1 FAIL → v2 PASS, che ha riscritto altre righe della stessa tabella Cap.49 (B-3 `bar_synthetic`, B-7 `tick_count`) senza correggere la mappatura OHLC. Questo è un finding di **valore già dimostrato sbagliato** (non solo metodologia difettosa): se applicato in produzione, l'adapter leggerebbe Open al posto di Close e High al posto di Low, contaminando l'inference del bundle frozen. Per AC-13(b) il PASS non è concedibile.

A questo si aggiungono: la contaminazione a monte in C (W13, lo schema wiki errato `O;H;L;C` è la fonte non etichettata da cui A ha attinto); il pattern ereditato W5 codici errore (semantica dichiarata senza enumerazione, ri-caratterizzata da M-3); il pattern ereditato W9 cooldown (refutato da M-5 nel regime ~1Hz). La **lista "Empirico-CLI da verificare" è NON vuota** → per AC-13(d) il PASS non è concedibile in sede WEB indipendentemente da W1.

---

## Esito per ogni asserzione dell'inventario W1..W11 (+ W12, W13 emerse)

### W1 — Schema CANDLE (mappatura DAPI → bundle frozen Portara) — **BUG REALE CATASTROFICO**

- **A.1 Localizzazione (A)**: `docs/methodology_v2/CAP_09_parte_9.md` Cap.49, tabella r155-164. Citazioni testuali esatte:
  - r158: `` | `bar_open` ($\mathrm{Open}_t$, prezzo in punti FIB) | numero (multiplo di 5pt) | `CANDLE` campo 5 (`<O>`) | Copia diretta. ... | ``
  - r159: `` | `bar_high` ($\mathrm{High}_t$) | numero | `CANDLE` campo 6 (`<H>`) | Copia diretta. ... | ``
  - r160: `` | `bar_low` ($\mathrm{Low}_t$) | numero | `CANDLE` campo 7 (`<L>`) | Copia diretta. ... | ``
  - r161: `` | `bar_close` ($\mathrm{Close}_t$) | numero | `CANDLE` campo 8 (`<C>`) | Copia diretta. ... | ``
  - r162: `` | `volume` ($\mathrm{Volume}_t$, contratti) | intero ≥ 0 | `CANDLE` campo 9 (`<V>`) | Copia diretta. ... | ``
  - **Lettura**: A dichiara che la posizione 5 del payload CANDLE contiene l'Open, la posizione 6 l'High, la posizione 7 il Low, la posizione 8 il Close → ordine campi `[5..8] = O;H;L;C`.

- **A.1 Localizzazione (D, canonico)**: `scripts/export_directa_history_parametric.py`:
  - r471: `kind, symbol, ymd, hms, uff, min_, max_, ape, qty = parts[:9]` → il payload CANDLE ha, nelle posizioni `[5..9]` (1-indexed dopo `CANDLE;sym;ymd;hms`), i campi `uff; min_; max_; ape; qty`.
  - r477: `# Documentazione Directa: UFF, MIN, MAX, APE => close, low, high, open.`
  - r478-482: `close_v = Decimal(uff)` / `low_v = Decimal(min_)` / `high_v = Decimal(max_)` / `open_v = Decimal(ape)` / `volume_v = int(Decimal(qty))`.
  - **Lettura**: posizione 5 = `uff` = **close**; posizione 6 = `min_` = **low**; posizione 7 = `max_` = **high**; posizione 8 = `ape` = **open**; posizione 9 = volume → ordine campi `[5..9] = C;L;H;O;V`.

- **A.3 Sostanza — confronto puntuale (cosa intendo per "divergenza", AC-9)**: ho confrontato le tre dimensioni richieste dal task:
  - (a) **ordine dei 5 campi numerici per posizione**: A `[5..9] = O;H;L;C;V`; D `[5..9] = C;L;H;O;V` → **DIVERGE**.
  - (b) **mapping campo→OHLC per posizione**: pos5 (A=Open / D=close) **DIVERGE**; pos6 (A=High / D=low) **DIVERGE**; pos7 (A=Low / D=high) **DIVERGE**; pos8 (A=Close / D=open) **DIVERGE**; pos9 (A=Volume / D=volume) coincide.
  - (c) **indice di colonna**: A usa "campo 5/6/7/8/9" (1-indexed, conta dal primo token `CANDLE`), D usa `parts[4..8]` (0-indexed) per gli stessi campi numerici; le convenzioni di conteggio coincidono (campo 5 = `parts[4]` = primo numerico = UFF). Nessuna ambiguità di indicizzazione spiega la divergenza: A e D contano i campi allo stesso modo, ma A vi associa l'OHLC sbagliato.
  - **Nota di rigore richiesta dal task** (distinguere "ordine campi DAPI `UFF;MIN;MAX;APE`" da "mapping campo→OHLC"): A **non** nomina mai UFF/MIN/MAX/APE; etichetta direttamente le posizioni con `<O>/<H>/<L>/<C>`. È quindi un'asserzione diretta sul **mapping posizione→OHLC**, non una mera elencazione di colonne. La divergenza è sostanziale e inequivocabile.
  - **Esito sostanza**: **BUG REALE**. A dichiara come "tabella canonica" (r153: *"La tabella sottostante e' canonica."*) uno schema che è l'esatto opposto del decoder di produzione su tutti e 4 i campi OHLC. Non è "verifica parziale": è una mappatura affermata come fatto e contraddetta da fonte level-1 (M-1) e level-2 (D).

- **A.2 Formato 4-righe**: assente (file pre-RM). Ma qui è irrilevante: la sostanza è errata, non solo il formato. La non-conformità di formato NON è il finding; il finding è il **valore sbagliato**.

- **A.5 Confronto empirico**: `[PROVA-EMPIRICA 2026-05-29 via STATO_CORRENTE.md §5 — M-1]`: *"schema CANDLE reale = UFF;MIN;MAX;APE;V = C;L;H;O;V, NON O;L;H;C. V-1 ha provato lo swap O/C"*. M-1 conferma `C;L;H;O`. A Cap.49 è quindi smentita dall'empirico più recente E dal codice canonico E dal decoder post-fix. Si noti che M-1/HANDOFF descrivono l'errore storico come `O;L;H;C` (L/H corretti, O/C scambiati); A Cap.49 è **ancora peggio**: ha anche L/H scambiati (`O;H;L;C`), cioè ha ereditato l'ordine grezzo del wiki (`<O>;<H>;<L>;<C>`, cfr. C `:28`, `:46`) senza nemmeno la correzione parziale L/H del probe daily.

- **A.4 Patch suggerita** (il Reviewer NON patcha; suggerimento testuale per il Developer di rework): in A Cap.49 r158-161 correggere la colonna "Origine DAPI runtime" così:
  - `bar_open` ← `CANDLE` campo 8 (`<APE>`) ;
  - `bar_high` ← `CANDLE` campo 7 (`<MAX>`) ;
  - `bar_low` ← `CANDLE` campo 6 (`<MIN>`) ;
  - `bar_close` ← `CANDLE` campo 5 (`<UFF>`) ;
  - `volume` ← `CANDLE` campo 9 (`<V>`) (invariato).
  - Aggiungere riga di etichettatura `[CODICE-ESISTENTE r.477-481 export_directa_history_parametric.py]` + `[PROVA-EMPIRICA 2026-05-29 V-1 / M-1]`, e una nota esplicita `[CORREGGE WIKI: il wiki Directa dichiara O;H;L;C ed è inesatto]`. Mantenere coerenza con C (vedi W13).

- **Esito W1**: **FAIL — BUG REALE catastrofico.** Questo è il finding che giustifica da solo il verdetto FAIL.

---

### W2 — Schema PRICE realtime (cash europei) — verifica parziale, no level-2, Empirico-CLI

- **A.1**: A Cap.47 r94: *"Schema **`PRICE`** ... `PRICE;<ticker>;<HH:mm:ss>;<last>;<volume_lot?>;<bid_qty?>;<ask_qty?>;<low_session>;<high_session>`. Esempi reali (cash, 2026-05-27): `PRICE;dGER;14:05:41;25251.9;0;0;0;25244.9;25400.9`; `PRICE;dITAS;14:05:43;49859.22;2;2318;2129;49859.22;50129.22`."*
- **C**: `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md:399`: *"Schema **`PRICE`**: ... (campi medi da chiarire)."* + B.4 r391-394 (gli stessi esempi reali con timestamp).
- **A.3 Sostanza**: i campi 5/6/7 sono marcati con punto interrogativo (`<volume_lot?>`, `<bid_qty?>`, `<ask_qty?>`) → questa è **forma RM-1 corretta**: A dichiara esplicitamente l'incertezza sull'interpretazione di quei campi (non li chiama "verificati"). C `:399` rinforza con *"campi medi da chiarire"*. **Nessun BUG.** Gli esempi reali hanno timestamp puntuale (`14:05:41`, `14:05:43`) → evidenza level-1 OK per la *struttura* osservata.
- **RM-2 (level-2)**: il decoder canonico D **non parsa PRICE** (D parsa solo CANDLE, r467-496). `probe_dapi.py:289-292` lo parsa ma raccoglie i campi senza interpretazione bit-a-bit di 5/6/7. Quindi nessuna corroborazione level-2 sull'interpretazione dei campi medi.
- **A.5**: nessun M-promemoria pertinente (M-3/M-4/M-5 non toccano PRICE; M-1 di V-1 morning conferma 1425 tick PRICE 0-unknown sul *parsing*, non sull'interpretazione dei campi medi).
- **Esito W2**: forma RM-1 corretta (incertezza dichiarata). Interpretazione campi 5/6/7 → **Empirico-CLI** (minore). Nessun BUG.

---

### W3 — Schema BOOK_5 (futures) — verifica parziale, esempio singolo, Empirico-CLI

- **A.1**: A Cap.47 r93: *"Schema **`BOOK_5`** ... `BOOK_5;<TICKER>;<HH:mm:ss>;<bid1_lots>;<bid1_ord>;<bid1_price>;<bid2..>;...<ask5..>` (5 livelli BID + 5 livelli ASK, ciascuno con triplo `lots / orders / price`)."* + esempio reale FIB6I `14:02:33`.
- **C**: `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md:375` (stessa struttura) + B.2 r366-368 (esempio reale grezzo).
- **A.3 Sostanza**: la struttura BID-poi-ASK e il triplo `lots/orders/price` sono dichiarati come fatto sulla base di **un solo evento** (FIB6I 2026-05-27 14:02:33). Alternative compatibili non enumerate: ordine BID/ASK potrebbe essere invertito; `lots` vs `orders` per livello potrebbe essere scambiato; l'indice del prezzo nel triplo. Su un solo campione con `bid1=49715` < `ask1=49275`... — anzi, **nota di attenzione**: nell'esempio r93/r366 `bid1_price=49715.0` risulta **maggiore** di `ask1_price=49275.0`, il che è anomalo per un book regolare (bid<ask); questo *potrebbe* essere coerente con BID/ASK invertiti nello schema, OPPURE con un book degenere a scadenza lontana (A r376 lo attribuisce a *"quasi-future a scadenza lontana"*). L'ambiguità NON è disambiguata. Questo è il pattern RM-1: struttura precisa da osservazione singola senza esclusione di alternative.
- **RM-2 (level-2)**: D non parsa BOOK_5 (nessuna corroborazione). `probe_dapi.py:307-310` lo parsa ma raccoglie i campi senza schema bit-a-bit certificato.
- **Esito W3**: **MIGLIORA PERFORMANCE / verifica parziale** — non è un BUG di valore dimostrato (è plausibile), ma la struttura BID/ASK e l'anomalia bid>ask non sono disambiguate. La regola `bar_synthetic` di A Cap.49 r164/r168 dipende da `bid1_lots ≥ 1 AND ask1_lots ≥ 1`: se l'ordine dei livelli o l'indice lots/price fosse diverso dal dichiarato, la regola si applicherebbe su campi sbagliati. → **Empirico-CLI** (ri-test BOOK_5 bit-a-bit su FIB front-month liquido). Marca come da arricchire, non BUG bloccante.

---

### W4 — Sintassi CANDLERANGE (period_s ultimo) — **OK level-2**

- **A.1**: A Cap.51 r240: *"`CANDLERANGE <FIB_front> <YYYYMMDD000000> <YYYYMMDD235959> 60`"* (period_s in ultima posizione). Coerente anche con A Cap.48 (uso implicito) e Cap.46 r47.
- **RM-2 (level-2)**: D `:228-230` emette `CANDLERANGE {symbol} {start} {end} {period_seconds}` — period LAST, **identico**. `probe_dapi.py:27, 335` conferma la stessa sintassi. Corroborazione level-2 piena.
- **A.3 Sostanza**: l'ordine argomenti ha supporto CODICE-ESISTENTE → **OK**. Enumerazione formale 4-righe assente (pre-RM).
- **Esito W4**: **OK / MIGLIORA PROCESSO** (opzionale: etichetta `[CODICE-ESISTENTE r.228-230]`). Nessun BUG. (Eredita pattern W2 di CAP-DATA-01 = OK level-2.)

---

### W5 — Codici errore DAPI 1004 / 1007 / 1030 (Cap.50) — **BUG REALE (sostanziale RM-1) + ri-caratterizzato da M-3**

- **A.1**: A Cap.50, tabella r192-196. Citazioni:
  - r194: `1004` → *"Comando non valido o non supportato dal protocollo realtime"* (emittenti: `INFO`, `HELP`, `VER`, `STATUS`, `GETAVAILABLESTATUS` su 10001; `UNSUB` di simbolo mai sottoscritto).
  - r195: `1007` → *"Strumento non abilitato per l'account, o ticker inesistente"* (`CANDLERANGE` su 10003).
  - r196: `1030` → *"Market data realtime non sottoscritto per quel ticker (distinto da 1007 ...)"*; + *"Per il FIB su account `B6086` non si osserva 1030 ... 1030 e' atteso esclusivamente sui futures cross-index Eurex/CME (FUORI scope ...)"*.
- **C**: `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md` A.3 r292-297 (1007/1004/1030/1004-UNSUB con *"Significato dedotto"*) + B.1 r358 (1004) + B.3 r378-386 (1030).
- **A.3 Sostanza**: la semantica dei codici è dichiarata come fatto. C la qualifica onestamente come *"Significato dedotto"* (r293) — forma RM-1 parzialmente corretta in C — ma A la trasferisce in tabella normativa senza enumerare le alternative compatibili né citare dump:timestamp puntuali per ciascun codice.
- **RM-2 (contro-prova level-2)**: D `:417-425` (`is_error_line`) fa string-matching generico (`ERR`, `Wrong `, `Not enough parameters`, `error`/`errore`/`not enabled`/`not valid`) e **NON decodifica i codici numerici** 1004/1007/1030. Quindi la semantica numerica **non ha alcun supporto in codice di produzione**: identica situazione di CAP-DATA-01 W4 (BUG REALE).
- **A.5 — confronto con M-3** `[PROVA-EMPIRICA 2026-05-29 dump probe_out/w4_errcodes_20260529.json via STATO_CORRENTE.md §5]`:
  - `1004` cmd ignoto → coerente con A r194. OK.
  - `1007` ticker inesistente/non abilitato → coerente con A r195. OK.
  - `1017` sintassi strutturale malformata → **NON citato in A Cap.50** (A elenca solo 1004/1007/1030). Gap.
  - `1015` data/parametro invalido → **NUOVO, NON in A**. Gap.
  - `1003` comando storico su porta realtime → **NUOVO, NON in A**. Gap.
  - `1030` realtime non sottoscritto → **NON RIPRODOTTO** (l'account FIB ha il dato). **Qui A è in forma RM-1 corretta**: A r196 dichiara esplicitamente *"Per il FIB su account `B6086` non si osserva 1030"* e marca il 1030 come atteso solo sui cross-index — cioè A **non** dichiara 1030 "verificato" sul perimetro account, riconosce che la sua semantica è derivata/attesa. Questo è coerente con M-3 (1030 non riprodotto, semantica plausibile non disambiguata).
- **Esito W5**: **BUG REALE (sostanziale RM-1)** per 1004/1007 (semantica in tabella normativa senza enumerazione alternative né dump:timestamp, senza supporto level-2 in D) — eredita il pattern W4 di CAP-DATA-01. **+ MIGLIORA PERFORMANCE** per l'arricchimento da M-3 (aggiungere 1017/1015/1003 ora noti empiricamente; il dominio dei codici trattati da A è incompleto rispetto alla realtà osservata). Il 1030 di A r196 è **già RM-1-conforme** (non va toccato sulla forma, eventualmente arricchito). Patch: riscrivere r194-195 come "verifica parziale" con comando-trigger e dump:timestamp, aggiungere 1017/1015/1003 con la stessa cautela. **Empirico-CLI** per disambiguare i trigger esatti.

---

### W6 — Mese IDEM F=Giu / I=Set (Mar/Dic da decodificare) — **OK (forma RM-1 corretta) + Empirico-CLI minore**

- **A.1**: A Cap.47 r61: *"La verifica empirica del 2026-05-27 ha confermato `FIB6I` = ... scadenza **settembre 2026** (ISIN `IT0024847870`, descrizione anagrafica `FTSE MIB INDEX FUTURE SET26`): il codice `I` corrisponde a **settembre** ... La lookup completa del codice mese Directa-IDEM (oltre `I=settembre`) e' punto aperto fuori scope (Cap.55)..."*. A Cap.55 r375 ribadisce: *"sono congelati solo i due codici verificati (`F = giugno`, `I = settembre`); gli altri restano lookup runtime-discovery."*
- **C**: `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md` B.2 r371-373 (ISIN + `SET26` + *"da decodificare"*) + B.6 r424 (*"constatato `I = Settembre`, `F` = ?"*).
- **A.3 Sostanza**: `I=settembre` è ancorato a evidenza puntuale citabile (ANAG ISIN+descrizione, timestamp `14:05:30`) → claim→evidenza valido level-1. La parzialità per gli altri mesi è **dichiarata esplicitamente** ("lookup completa fuori scope", "runtime-discovery") → forma RM-1 corretta.
- **A.5 — confronto con M-4** `[PROVA-EMPIRICA 2026-05-29 via STATO_CORRENTE.md §5]`: `F=Giugno` **confermato** (SUB FIB6F → ANAG ISIN IT0024209022 GIU26); `I=Settembre` già confermato. Mar/Dic ancora da decodificare. A è **coerente** con M-4. Nota: A r61/Cap.55 r375 dichiara `F=giugno` *"derivato dalla prassi dei sample export FIB6F"* — M-4 lo ha ora **direttamente confermato via ANAG** il 2026-05-29 (più forte della derivazione originale): possibile arricchimento, non correzione.
- **Attenzione W6.b — `FIB6L`**: A Cap.47 r96 cita *"una sequenza di SUB su ticker candidati (`FIB6F`, `FIB6I`, `FIB6L`, ...)"* e C B.2 r376 ipotizza *"per il front-month giugno occorrerebbe SUB su `FIB6L`/`FIB6M`"*. `FIB6L` è dichiarato come **candidato** (non come ANAG verificata), e A non lo afferma come fatto → accettabile. Ma è una posizione speculativa: il codice mese di `L` non è verificato. → **Empirico-CLI** (minore): SUB `FIB6L` per decodificarne il mese.
- **Esito W6**: forma RM-1 sostanzialmente corretta (la parzialità è dichiarata, l'evidenza puntuale c'è per F/I). Nessun BUG. Mar/Dic e `FIB6L` → **Empirico-CLI** minore. (Eredita pattern W5 di CAP-DATA-01 = OK.)

---

### W7 — Limite 100 giorni intraday — **OK level-2**

- **A.1**: A Cap.46 r53 (*"limite ... 100 giorni"* implicito nel rate-limit), A Cap.51 r235 (*"ampiamente entro il limite **100 giorni intraday** del DAPI verificato empiricamente sui sample"*), A Cap.55 r377 (*"Il limite 100 giorni intraday del DAPI e' strutturale a Directa"*).
- **RM-2 (level-2)**: D `:61` `DEFAULT_INTRADAY_MAX_DAYS = 100` — costante di produzione già in uso. `update_inventory_indici_futures_daily.py:12,124,144` la importa e usa. Corroborazione level-2.
- **A.5**: corroborato anche empiricamente in C A.2 r284-286 (query 150gg → first_timestamp ~100gg prima, *"Conferma empirica limite 100 giorni intraday"*) → level-1.
- **Esito W7**: **OK** (level-1 + level-2). MIGLIORA PROCESSO opzionale (etichetta `[CODICE-ESISTENTE r.61]`). Nessun BUG. (Eredita pattern W7 di CAP-DATA-01 = OK.)

---

### W8 — Riavvio Darwin mezzanotte (Cap.50) — verifica parziale, citazione wiki, Empirico-CLI

- **A.1**: A Cap.50 r207: *"Il gateway Darwin esegue manutenzione automatica giornaliera circa a mezzanotte locale (**documentato dal wiki DAPI**), interrompendo le connessioni attive..."*.
- **C**: `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md` Q4 r94 (*"Disconnessione automatica giornaliera ~mezzanotte (manutenzione server: Darwin va riavviato ogni 24h)"*) + r232 (wiki EN cita *"riavvio Darwin a mezzanotte"*).
- **A.3 / RM-3 Sostanza**: l'asserzione si appoggia **al solo wiki** (level-4), senza corroborazione level-1 (nessun dump di una sessione cross-midnight) né level-2 (il decoder non gestisce il riavvio). Il wiki è la fonte etichettata (parzialmente) ma il wiki è **dimostrato inesatto sullo schema CANDLE** (M-1, RM-3): per RM-3 ogni conclusione wiki-only è sospetta. Tuttavia il riavvio mezzanotte è un fatto operativo di routine, plausibile e non in conflitto con altre prove; A lo usa per costruire una procedura di recovery (Cap.50 r207-217), non come schema-dato critico.
- **Esito W8**: **MIGLIORA PROCESSO** (conclusione appoggiata a wiki-only; etichettare `[WIKI-HINT, da verificare]` e marcare il fenomeno come "da osservare empiricamente"). NON BUG REALE bloccante (non è uno schema-dato che contamina il bundle; è una contingenza operativa di recovery). → **Empirico-CLI** (osservazione passiva di una sessione cross-midnight; fenomeno notturno automatico, non forzabile).

---

### W9 — Cooldown ~30s / 14 connessioni (Cap.46, Cap.50) — **BUG REALE (sostanziale RM-1) + REFUTATO da M-5**

- **A.1**: A Cap.46:
  - r47: *"14 connessioni TCP rapide aperte/chiuse ravvicinate hanno provocato `ConnectionResetError 10054` sulla 14ª connessione e successivo `ConnectionRefusedError 10061` per circa 30 secondi (cooldown)."*
  - r51: *"Aperture TCP rapide oltre la 14ª nello stesso intorno temporale provocano cooldown circa 30 s."*
  - A Cap.50 r198: *"`ConnectionResetError 10054` sulla 14ª connessione TCP rapida ravvicinata; `ConnectionRefusedError 10061` durante il cooldown ~30 s"*.
- **C**: `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md` A.4 r306 (*"dopo la 14ª il server ha cominciato a chiudere ... rifiutare nuove connessioni per ~30 secondi"*) + B.6 r428 + A.7 r339 (*"cooldown ~30s dopo 14 aperture rapide ravvicinate"*).
- **A.3 Sostanza**: due numeri precisi ("14ª connessione", "~30 s") dichiarati come **regole operative** (A r49-51: *"Le evidenze empiriche del 2026-05-27 fissano due regole operative"*) da una **singola osservazione** del 2026-05-27, senza enumerare le alternative compatibili (soglia 12/13/15? dipendenza dal timing/regime di burst? durata esatta del cooldown?). Pattern identico a CANDLE e a CAP-DATA-01 W6 (BUG REALE sostanziale).
- **A.5 — confronto con M-5** `[PROVA-EMPIRICA 2026-05-29 dump probe_out/w6_cooldown_20260529.json via STATO_CORRENTE.md §5]`: *"la costante 'cooldown ~30s dopo 14ª connessione' è **REFUTATA nel regime testato** — 75 connessioni open/close a ~1Hz su 10003 senza alcun cooldown (3×25, `onset_connection:null`). Soglia/durata sotto burst >>1Hz NON disambiguate."* → **A dichiara oggi come "regola operativa fissata" un fenomeno che l'empirico più recente ha refutato nel regime ~1Hz.** L'asserzione non è più solo "non verificata": è **disallineata da prove disponibili**.
- **Esito W9**: **BUG REALE (sostanziale RM-1), aggiornato dall'empirico.** È il pattern canonico W6 di CAP-DATA-01 che si ripresenta in Parte 9, ora con refutazione empirica. Patch: riscrivere A Cap.46 r47-53 e Cap.50 r198 come *"osservazione singola del 2026-05-27 in regime di burst non disambiguato; in regime ~1Hz nessun cooldown osservato (M-5, 2026-05-29, 75 conn open/close su 10003); soglia e durata sotto burst >>1Hz non disambiguate"*. La regola operativa "una sola connessione persistente per porta" (A r47, r307 di C) **resta valida e prudente** indipendentemente dal cooldown — va mantenuta come scelta architetturale, ma il razionale "14/30s" va ri-caratterizzato. **Empirico-CLI** (ri-test burst >>1Hz per disambiguare la soglia).

---

### W10 — Banner Darwin `DARWIN_STATUS;CONN_OK;TRUE;Release 2.5.1 build 04/02/2025` — verifica parziale, Empirico-CLI minore

- **A.1**: A Cap.46 r27 + r29: *"Alla connessione il gateway risponde con il banner `DARWIN_STATUS;CONN_OK;TRUE;Release 2.5.1 build 04/02/2025`."*; A Cap.50 r212 (atteso `DARWIN_STATUS;CONN_OK;TRUE;Release ...`).
- **C**: `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md` A r249 (banner identico, probe 2026-05-27).
- **A.3 Sostanza**: singola osservazione del 2026-05-27, con data esplicita → **level-1 [PROVA-EMPIRICA] OK** sulla struttura osservata. A r29 lo tratta correttamente come stringa che *"contiene esplicitamente la release"* e A Cap.50 r212 usa il pattern `Release ...` (prefisso variabile) — coerente con l'idea che il numero di release cambi fra versioni Darwin. Nessuna asserzione "questa stringa è fissa per sempre".
- **Esito W10**: forma OK (osservazione datata, release trattata come variabile). Variazioni di banner per release diverse → **Empirico-CLI** minore. Nessun BUG.

---

### W11 — Decisione Q-A-3 cash gating (Cap.53) — **NON asserzione empirica (RM-1 non si applica) — perimetro vincolante coerente**

- **A.1**: A Cap.53 r294-328 (intero capitolo). Verdetto *"Q-A-3 (ratificato)"* (r294); perimetro vincolante r299-304 (4 NO: feature tensor, state machine, cromosoma, walk-forward).
- **Natura**: è una **SCELTA di design ratificata** (cfr. task card §"Out-of-scope" e W11). RM-1 NON si applica. Il Reviewer verifica solo la coerenza del perimetro vincolante.
- **Verifica coerenza perimetro**: i 4 NO sono scritti in modo netto (r301-304); il flusso post-emissione (r306-314) è coerente con "il gating non sopprime mai il segnale" (r297) e con il replay bit-exact (r314-315). Non ho trovato "porte aperte" testuali che permetterebbero al cash di entrare nel cromosoma o nella state machine. La coerenza con Parte 8 Cap.42 (cash ≠ cross-index PHASE-2, r324) e Cap.37 (esclusione MIB cash da training, r326) è esplicita.
- **Esito W11**: **NEUTRO** (coerente). Nessun finding. Non classificato come BUG metodologico (corretto per mandato).

---

### W12 (emerso, secondo giro) — A Cap.50 r196 + Cap.55 r373: codice 1030 / FDAX e "verifica empirica 2026-05-27"

- **A.1**: A Cap.55 r373: *"La verifica empirica 2026-05-27 ha confermato che l'account `B6086` **non e' abilitato** al ticker `FDAX` standard ... tutte le varianti del ticker hanno restituito `ERR;<sym>;1007`. Sono abilitati esclusivamente i ticker Mini-DAX `EU.FDXMM6` ... e Micro-DAX `EU.FDXSM6`..."*.
- **C**: `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md` A.1 r264-271 (tabella ticker probati: FDAX `❌ ERR;1007`, FDXM/FDXS/DJ50/ES `✅`) + B.3 r378-386 (1030 sui cross-index).
- **A.3 Sostanza**: l'asserzione "FDAX non abilitato → 1007" è ancorata a evidenza puntuale citabile (C A.1 r264, tabella con status per ticker). Claim→evidenza valido level-1 (DOC-INTERNO che riporta il probe). La distinzione 1007 (storico/abilitazione) vs 1030 (market data realtime) è coerente fra A r195-196, C A.3 r294-296 e C B.3 r386. **Coerente.**
- **Esito W12**: **OK / NEUTRO.** Le asserzioni FDAX/1007/1030-cross-index sono fuori dal perimetro FIB operativo (cross-index = PHASE-2 fuori scope) e hanno ancora empirica in C. Nessun BUG. (Si noti che riguardano cross-index, non il FIB: anche se da confermare CLI, non contaminano la pipeline FIB di CAP-DATA-03.)

---

### W13 (emerso, secondo giro — RADICE DELLA CONTAMINAZIONE W1) — C dichiara lo schema CANDLE wiki `O;H;L;C` come "documentato", non etichettato — **BUG REALE (RM-3) in C**

- **A.1 (C)**: `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md`:
  - r28 (Q1): *"Lo schema candle DAPI (`CANDLE;<TICKER>;<yyyyMMdd>;<HH:mm:ss>;<O>;<H>;<L>;<C>;<V>`) è documentato e identico tra strumenti italiani ed esteri."*
  - r46 (Q2): *"Candele: `CANDLE;<TICKER>;<yyyyMMdd>;<HH:mm:ss>;<Open>;<High>;<Low>;<Close>;<Volume>`. Niente settle né tick-count nel record candle."*
  - r34 (Q2 header): la fonte dei limiti/schema è esplicitamente il wiki `https://app1.directatrading.com/trading-api-directa/index.html`.
- **A.3 / RM-3 Sostanza**: C dichiara `O;H;L;C;V` come schema **"documentato"** (level-4 wiki) **senza etichetta** `[WIKI-HINT, da verificare]` e **senza corroborazione level-1/2**. Questo è esattamente lo schema che D `:477-481` e M-1 smentiscono. **C è la fonte da cui A Cap.49 ha ereditato l'ordine errato** (`<O>;<H>;<L>;<C>` di C r28 → `campo 5 (<O>)...campo 8 (<C>)` di A r158-161). La data di C (2026-05-27) è precedente alla scoperta dell'errore (V-1, 2026-05-29), quindi all'epoca l'errore era comprensibile; ma **oggi** C resta su `origin/main` con uno schema dimostrato inesatto, non etichettato, e ha già contaminato A.
- **Esito W13**: **BUG REALE (RM-3): conclusione di livello-4 (wiki) usata come fatto "documentato" senza supporto level-1/2 e ora dimostrata inesatta.** Patch: in C r28 e r46 etichettare `[WIKI-HINT, dimostrato INESATTO sullo schema CANDLE: l'ordine reale è UFF;MIN;MAX;APE = C;L;H;O;V, vedi export_directa_history_parametric.py:477 e M-1 2026-05-29]`. Il vecchio testo non si cancella ma si etichetta inequivocabilmente (come da Note al Developer del task card per C). Coerenza obbligatoria con la patch W1 di A.

---

## Check W2 (grep RM-2): comando + esito + tabella decoder/parser esistenti

**Grep eseguito** (sede WEB):
```
grep -rn "parse_directa\|parse_candle\|decode_candle\|UFF\|APE\|MIN\|MAX\|CANDLE;\|CANDLERANGE\|PRICE;\|BOOK_5;\|ANAG;\|END CANDLES\|ERR;\|DARWIN_STATUS\|DEFAULT_INTRADAY_MAX_DAYS\|is_error_line\|AGG_FROM" --include='*.py' --include='*.md' .
```
+ grep mirati su `*.py`: `UFF|APE|close_v|open_v|parse_directa_candle|is_error_line|DEFAULT_INTRADAY_MAX_DAYS|END_MARKER|def parse_line`; `def parse|def decode|\.split(";")|startswith("CANDLE|...`.

**Decoder/parser esistenti nel repo per DAPI** (formato `METODO.md:64-71`):

| path:linea | Cosa decodifica | Schema dichiarato | Ruolo |
|---|---|---|---|
| `scripts/export_directa_history_parametric.py:467-496` (`parse_directa_candle`) | record `CANDLE` storico | r471 `parts[4..8] = uff;min_;max_;ape;qty`; r477-481 `UFF→close, MIN→low, MAX→high, APE→open` = **`C;L;H;O;V`** | **CANONICO level-2** (fonte di verità di codice) |
| `scripts/export_directa_history_parametric.py:228-230` | emissione comando `CANDLERANGE` | `CANDLERANGE {sym} {start} {end} {period_s}` (period LAST) | level-2 per W4 |
| `scripts/export_directa_history_parametric.py:417-425` (`is_error_line`) | rilevamento errori | string-match `ERR`/`Wrong `/`Not enough parameters`/`error`/`errore`/`not enabled`/`not valid` — **NON decodifica codici numerici** | level-2 per W5 (semantica numerica NON corroborata) |
| `scripts/export_directa_history_parametric.py:282-285,437` | terminatore stream | `END CANDLES` | level-2 (terminatore) |
| `scripts/export_directa_history_parametric.py:61` | costante limite intraday | `DEFAULT_INTRADAY_MAX_DAYS = 100` | level-2 per W7 |
| `scripts/probe_dapi.py:230-272` (`parse_line`, ramo `CANDLE;`) | record `CANDLE` (post-fix `a12ae32`) | r249-250, r264-267 `p[4]=UFF=close ... p[7]=APE=open` = **`C;L;H;O;V`**; r14 docstring idem | level-2 di supporto (già auditato CAP-DATA-01 PASS, NON oggetto qui) |
| `scripts/probe_dapi.py:274-322` (`parse_line`, rami `ANAG;`/`PRICE;`/`BOOK_5;`) | ANAG / PRICE / BOOK_5 | raccolta campi senza schema bit-a-bit certificato per i campi medi | level-2 parziale (no corroborazione W2/W3 sui campi medi) |
| `scripts/update_inventory_indici_futures_daily.py:12,124,144` | consumer (importa `DEFAULT_INTRADAY_MAX_DAYS`) | nessun parsing CANDLE proprio | non rilevante per schema |

**Conclusione RM-2**: due decoder DAPI nel repo (canonico D + probe_dapi post-fix), **entrambi concordi** su `C;L;H;O;V`. Nessun decoder aggiuntivo mancato. La divergenza è **solo** in A Cap.49 (testo) e in C r28/r46 (testo wiki non etichettato) — **nessun codice di produzione dichiara `O;H;L;C`**. Questo isola il finding W1/W13 come errore testuale ereditato dal wiki, non come ambiguità di codice.

---

## Check W3 (RM-3): etichettatura fonti esterne

| Riferimento | file:linea | Livello | Etichetta presente? | Conclusione wiki-only? |
|---|---|---|---|---|
| wiki Directa (schema CANDLE) | A Cap.46 r27 (URL); C Q1 r28, Q2 r34, r46 | 4 (dimostrato INESATTO su CANDLE) | NO (pre-RM) | **SÌ in C r28/r46 → BUG REALE (W13)**; A Cap.49 NON cita il wiki ma ne eredita lo schema → BUG REALE (W1) |
| wiki Directa (riavvio mezzanotte) | A Cap.50 r207 (*"documentato dal wiki DAPI"*); C Q4 r94, r232 | 4 | parziale (A nomina il wiki) | **SÌ (wiki-only, no level-1/2) → MIGLIORA PROCESSO (W8)** |
| wiki Directa (limite 100gg) | A Cap.46 r53, Cap.51 r235; C Q2 r40, r43 | 4 | NO | **NO** — corroborato level-1 (C A.2 r284) + level-2 (D `:61`). OK (W7) |
| wiki Directa (max 100 simboli) | A Cap.46 r47; C Q4 r90 | 4 | NO | NO — ortogonale, non critico. Plausibile, non contraddetto. NEUTRO |
| pagine pubbliche Directa (sessione Eurex/CME, costi) | C Q1/Q3/Q5 (URL nei riferimenti r225-237) | 4 (pagine commerciali, non wiki API) | NO | parziale — cross-index PHASE-2 fuori scope; usato come hint, non critico per FIB. NEUTRO |
| `docs/runtime/dapi_port_settings_schema.md` | A Cap.46 r31, r41 | 3 (DOC-INTERNO) | NO (pre-RM) | NO — referente esiste e contiene lo schema 4-campi dichiarato (`:25-28`). OK |
| probe empirico 2026-05-27 (banner, ANAG, BOOK_5, PRICE, errori, rate-limit) | A multipli; C Appendici A/B | 3→1 (DOC-INTERNO che riporta prova empirica) | NO (pre-RM) | NO — è la fonte interna primaria; alcuni item single-shot (W2/W3/W9). |

**Esito RM-3**: due conclusioni wiki-only critiche: **W13/W1 (schema CANDLE)** = BUG REALE (dimostrata inesatta); **W8 (riavvio mezzanotte)** = MIGLIORA PROCESSO (plausibile, da etichettare + osservare). Le altre citazioni wiki sono o corroborate (100gg) o ortogonali/non-critiche. Etichette di livello assenti ovunque (pre-RM) → MIGLIORA PROCESSO globale dove la sostanza regge.

---

## Check W4 (coerenza interna A↔B↔C↔D)

- **A ↔ D (W5/W1 critico)**: A Cap.49 schema CANDLE **DIVERGE** da D `:477-481` (W1, BUG REALE). A Cap.51 r240 CANDLERANGE **coincide** con D `:228-230` (W4, OK). A Cap.46/55 limite 100gg **coincide** con D `:61` (W7, OK). A Cap.50 codici errore: D non li decodifica → nessuna corroborazione (W5).
- **A ↔ C**: A eredita da C lo schema CANDLE errato (C r28/r46 `O;H;L;C` → A Cap.49 `campo5(<O>)...campo8(<C>)`) → **contaminazione confermata (W13→W1)**. Per il resto A cita C come fonte (Cap.46 r27, Cap.47 r59/r92-94, Cap.50 r190, Cap.51 r235) e i referenti in C esistono e contengono il dichiarato (ANAG/BOOK_5/PRICE esempi in C B.2/B.4; errori in C A.3/B; cooldown in C A.4). **Citazioni A→C valide per esistenza referente e contenuto**, eccetto che il contenuto ereditato sullo schema CANDLE è esso stesso errato.
- **B (REPORT) ↔ A (mappatura claim→evidenza)**: vedi Check W6/Onestà sotto. **B vouchera per la tabella Cap.49 errata**: B `:39` (*"Coerenza adapter DAPI -> bundle frozen Portara ... normata in tabella canonica Cap.49"*) e B `:51` (AC-3 *"CANDLE schema (Cap.49 tabella)"* = OK) e B `:52` (AC-4 *"tabella mappatura ... completa per TUTTI i campi"* = OK) dichiarano "OK" su una tabella che è sbagliata sui 4 campi OHLC. Il "OK" di AC-4 è verificabile solo come **completezza dei campi** (tutti presenti), non come **correttezza del mapping** — il REPORT non ha verificato il mapping contro D. → finding su B (mappatura claim→evidenza incompleta).
- **C interna**: C r28 (Q1) e r46 (Q2) ripetono lo stesso schema wiki errato; coerenti fra loro, entrambi errati.

---

## Check W5 (script↔capitolo — il check che avrebbe intercettato l'errore O/C)

**Confronto mappatura CANDLE A vs C vs D vs probe_dapi**:
- A Cap.49 r158-161: pos5=Open, pos6=High, pos7=Low, pos8=Close → `O;H;L;C`.
- C r28/r46: `<O>;<H>;<L>;<C>` (wiki, non etichettato) → `O;H;L;C`.
- D `:477-481`: pos5=close, pos6=low, pos7=high, pos8=open → `C;L;H;O`.
- `probe_dapi.py:264-267`: pos5=close, pos6=low, pos7=high, pos8=open → `C;L;H;O`.

**A e C concordano fra loro (entrambi `O;H;L;C`) e DIVERGONO da entrambi i decoder di produzione (`C;L;H;O`).** Questo è precisamente il check W5 di CAP-DATA-01 (che lì passava perché lo script era stato rettificato): **qui FALLISCE**, perché il CAP-XX (A) e l'indagine sorgente (C) non sono stati allineati al decoder canonico. La divergenza è **non etichettata** in A e in C → **BUG REALE** (per AC-13(b) e per il criterio "divergenza non etichettata = BUG REALE" del task card §Check W5).

Gli altri item W5: CANDLERANGE (A↔D coincidono), terminatore END CANDLES (A non lo dichiara esplicitamente nel testo normativo ma D lo usa; non c'è divergenza), 100gg (coincidono), dominio `source ∈ {DIRECTA, AGG_FROM_60s, AGG_FROM_D}` (A Cap.48 r131-138 coerente con i marker di D / manifest sample, level-2/3 OK).

---

## Check W6 (onestà claim→evidenza)

| Asserzione | Evidenza puntuale? | Esito |
|---|---|---|
| W1 schema CANDLE (A Cap.49) | "tabella canonica" SENZA citare D né prova; **contraddetta da D r477 e M-1** | **BUG REALE** — asserzione "canonica" senza ancora corretta, ancorata implicitamente al wiki errato |
| W5 codici 1004/1007 (A Cap.50 r194-195) | nessun dump:timestamp per codice; no level-2 in D | **BUG REALE** (sostanziale RM-1) |
| W5 codice 1030 (A Cap.50 r196) | dichiarato esplicitamente "non osservato sul FIB B6086" | **OK** (RM-1-conforme: non lo chiama verificato) |
| W9 cooldown 14/30s (A Cap.46 r47-51) | unica ancora = probe singolo 2026-05-27 (C A.4); **refutato da M-5** | **BUG REALE** (sostanziale RM-1, refutato) |
| W6 mese F/I (A Cap.47 r61) | ISIN+descrizione ANAG, timestamp 14:05:30 (C B.2) | **OK** (level-1) |
| W10 banner (A Cap.46 r27) | probe 2026-05-27 datato (C A) | **OK** (level-1) |
| W2/W3 PRICE/BOOK_5 (A Cap.47 r93-94) | esempi reali singoli con timestamp | OK su struttura osservata; campi medi/ordine livelli **Empirico-CLI** |
| W12 FDAX/1007 (A Cap.55 r373) | tabella ticker C A.1 r264 | **OK** (level-1, cross-index fuori scope) |
| B AC-4 "tabella completa per TUTTI i campi" (B `:52`) | verifica solo completezza, NON correttezza mapping vs D | **mappatura claim→evidenza incompleta** (il REPORT non ha controllato il mapping contro il decoder) |

---

## Empirico-CLI da verificare (lista NON vuota — input per sessione CLI separata)

In coerenza con il divieto `reviewer.md:163` (il Web reviewer NON dichiara "verificato empiricamente" niente che richieda DAPI live o filesystem locale), le seguenti asserzioni sono marcate per follow-up CLI. **NB**: W1 e W13 NON sono in questa lista — sono già risolti staticamente dal confronto con il codice canonico D (level-2) e M-1 (level-1 acquisita): lo schema corretto è `C;L;H;O;V` e non richiede ulteriore prova DAPI (la prova è già stata fatta, V-1/M-1).

| W-N | Asserzione | File:linea | Test minimo proposto (CLI, DAPI live) |
|-----|-----------|-----------|----------------------------------------|
| W2 | interpretazione campi medi `PRICE` 5/6/7 (`<volume_lot?>;<bid_qty?>;<ask_qty?>`) | A Cap.47 r94; C r399 | catturare ≥N tick PRICE su DGER/DITAS e confrontare i campi 5/6/7 con il book/volume noti per disambiguare il significato |
| W3 | schema BOOK_5 bit-a-bit (ordine BID/ASK, indice lots/orders/price, anomalia bid>ask del campione) | A Cap.47 r93; C r375 / B.2 r366-368 | SUB FIB front-month liquido, leggere ≥N eventi BOOK_5, verificare che `bid1_price < ask1_price` e l'ordine dei 5 livelli BID/ASK e la posizione di lots/orders/price |
| W5 | semantica/trigger codici 1004/1007 + nuovi 1017/1015/1003 | A Cap.50 r194-195; M-3 | inviare comandi-trigger (INFO/HELP su 10001; CANDLERANGE malformata su 10003 con ≥2 permutazioni; comando storico su 10001; SUB non sottoscritto) e registrare codice+dump:timestamp; disambiguare 1017 vs 1015 vs 1003 |
| W6 | mese IDEM Mar/Dic + codice di `FIB6L` | A Cap.47 r96; A Cap.55 r375; M-4 | SUB ticker trimestrale Mar/Dic + `FIB6L`, leggere ANAG (ISIN+descrizione) per decodificare i codici mese |
| W8 | riavvio Darwin mezzanotte (fenomeno) | A Cap.50 r207 | osservazione passiva di una sessione cross-midnight: catturare disconnessione + re-handshake + timestamp |
| W9 | soglia/durata cooldown sotto burst >>1Hz | A Cap.46 r47-51; A Cap.50 r198; M-5 | ripetere il test M-5 con burst di apertura/chiusura socket a frequenza crescente (>>1Hz) per disambiguare se esiste una soglia e a quale frequenza/conteggio scatta |
| W10 | variazione banner per release Darwin diverse | A Cap.46 r27 | catturare il banner su eventuali release Darwin diverse per confermare che solo il campo `Release ...` varia |

(7 voci. La lista non vuota → per AC-13(d) il verdetto WEB non può essere PASS pieno indipendentemente da W1/W5/W9.)

---

## Tabella di classificazione per il supervisore

| # | Problema | File:linea | Classificazione | Patch suggerita (il Reviewer NON patcha) |
|---|----------|-----------|-----------------|-------------------------------------------|
| 1 | **Schema CANDLE invertito**: A Cap.49 dichiara mappatura campi `[5..8] = O;H;L;C` (ordine wiki), il decoder canonico D `:477-481` e M-1 dicono `C;L;H;O`. Tutti e 4 i campi OHLC sono mappati sulla posizione sbagliata. È l'errore originale §3.1 sopravvissuto nel CAP-XX. | A `docs/methodology_v2/CAP_09_parte_9.md:158-161` vs D `scripts/export_directa_history_parametric.py:477-481` | **BUG REALE (catastrofico)** | Correggere A r158-161: `bar_open`←campo 8 (APE), `bar_high`←campo 7 (MAX), `bar_low`←campo 6 (MIN), `bar_close`←campo 5 (UFF); aggiungere etichette `[CODICE-ESISTENTE r.477-481]` + `[PROVA-EMPIRICA M-1 2026-05-29]` + nota `[CORREGGE WIKI]`. |
| 2 | **C dichiara lo schema wiki `O;H;L;C` come "documentato"** non etichettato, dimostrato inesatto — è la fonte da cui A ha ereditato l'errore. | C `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md:28` e `:46` | **BUG REALE (RM-3)** | Etichettare r28/r46 `[WIKI-HINT, dimostrato INESATTO su CANDLE: ordine reale C;L;H;O, vedi export_directa_history_parametric.py:477 e M-1]`; non cancellare il testo, etichettarlo. Coerente con patch #1. |
| 3 | **Cooldown "~30s dopo 14ª connessione" dichiarato come regola operativa** da osservazione singola, **refutato da M-5** nel regime ~1Hz (75 conn senza cooldown). | A `:47`, `:51`; A `:198`; (C A.4 `:306`) | **BUG REALE (sostanziale RM-1, refutato)** | Riscrivere come "osservazione singola 2026-05-27 in burst non disambiguato; in regime ~1Hz nessun cooldown (M-5 2026-05-29); soglia/durata sotto burst >>1Hz non disambiguate". Mantenere la regola architetturale "1 connessione persistente per porta". |
| 4 | **Semantica codici errore 1004/1007 in tabella normativa** senza enumerazione alternative né dump:timestamp; `is_error_line` di D non decodifica numerici (no level-2). Pattern W4 ereditato da CAP-DATA-01. | A `:194`, `:195`; D `:417-425` | **BUG REALE (sostanziale RM-1)** | Riscrivere 1004/1007 come "verifica parziale" con comando-trigger e dump:timestamp. Empirico-CLI per i trigger esatti. |
| 5 | **Dominio codici errore incompleto vs M-3**: A elenca solo 1004/1007/1030; M-3 ha osservato anche 1017, 1015 (nuovo), 1003 (nuovo). | A `:192-196` (tabella); M-3 | **MIGLIORA PERFORMANCE** | Aggiungere 1017/1015/1003 alla tabella con la cautela RM-1 (comando-trigger, dump). Migliora il recovery deterministico in produzione. |
| 6 | **Riavvio Darwin mezzanotte appoggiato a wiki-only** (level-4), senza corroborazione level-1/2; il wiki è dimostrato inesatto su CANDLE. | A `:207` | **MIGLIORA PROCESSO** | Etichettare `[WIKI-HINT, da verificare]`; marcare il fenomeno come "da osservare empiricamente" (Empirico-CLI). Non bloccante (contingenza di recovery, non schema-dato). |
| 7 | **Schema BOOK_5 da osservazione singola** con anomalia bid>ask non disambiguata; la regola `bar_synthetic` (Cap.49 r164/r168) dipende da `bid1_lots`/`ask1_lots` la cui posizione non è certificata. | A `:93`; A `:164`, `:168`; C `:375`/`:366-368` | **MIGLIORA PERFORMANCE** | Annotare che lo schema BOOK_5 è da osservazione singola, alternative (ordine BID/ASK, indice lots/price) non escluse; Empirico-CLI. |
| 8 | **B (REPORT) vouchera per la tabella Cap.49 errata**: AC-3/AC-4 dichiarati "OK" verificando completezza dei campi ma NON la correttezza del mapping contro D. | B `:39`, `:51`, `:52` | **MIGLIORA PROCESSO** | Annotare nel rework che la verifica AC-4 va estesa a "mapping verificato contro decoder canonico D"; il REPORT originale resta storico (immutabile), l'annotazione vive nel report ridotto di rework. |
| 9 | **Schema PRICE campi medi 5/6/7** marcati `?` (forma RM-1 corretta), ma interpretazione non risolta. | A `:94`; C `:399` | **NEUTRO** (già onesto) → Empirico-CLI | Nessuna patch testuale obbligatoria; l'incertezza è già dichiarata. Disambiguare in CLI quando serve. |
| 10 | **Etichette di livello fonte RM-3 assenti** in tutto il perimetro (file pre-RM) dove la sostanza regge (W4/W6/W7/W10). | A, C (globale) | **MIGLIORA PROCESSO** | Aggiungere etichette `[CODICE-ESISTENTE]`/`[PROVA-EMPIRICA]`/`[WIKI-HINT]` in eventuale rework. Non bloccante. |

**Nota su NEUTRO/RISCHIO PEGGIORAMENTO**: nessun finding classificato RISCHIO PEGGIORAMENTO. Un finding NEUTRO (#9, già onesto). I **BUG REALI obbligatori** sono #1, #2, #3, #4 (di cui #1 catastrofico). I MIGLIORA (#5, #7 PERFORMANCE; #6, #8, #10 PROCESSO) sono a discrezione del supervisore.

---

## Verdetto motivato

Il **cuore dell'audit (W1: coerenza schema CANDLE A↔D) è FAIL**, ed è il caso peggiore previsto dal task card: A Cap.49 r158-161 dichiara come "tabella canonica" la mappatura `campo 5 = Open, campo 6 = High, campo 7 = Low, campo 8 = Close`, cioè l'ordine grezzo del wiki Directa `O;H;L;C`. Il decoder di produzione canonico D `:477-481` (`UFF→close, MIN→low, MAX→high, APE→open`), il decoder post-fix `probe_dapi.py:264-267`, e la prova empirica M-1 (`[PROVA-EMPIRICA 2026-05-29]`) concordano tutti su `C;L;H;O`. La divergenza è su **tutti e quattro i campi OHLC** (O↔C e H↔L scambiati): è il medesimo errore §3.1 che ha motivato l'introduzione di RM-1/2/3, sopravvissuto dentro il CAP-XX e — fatto aggravante — sopravvissuto al ciclo Review v1 FAIL→v2 PASS che ha riscritto altre righe della stessa tabella Cap.49 (B-3 `bar_synthetic`, B-7 `tick_count`, cfr. B `:85`, `:89`) senza mai toccare la mappatura OHLC. La radice della contaminazione è in C `:28`/`:46`, che dichiara lo schema wiki `O;H;L;C` come "documentato" senza etichetta e senza corroborazione level-1/2 (W13, BUG REALE RM-3). Questo non è "metodologia difettosa su un'asserzione che potrebbe rivelarsi vera": è un **valore già dimostrato sbagliato** che, se eseguito in produzione, farebbe leggere all'adapter Open al posto di Close e High al posto di Low, contaminando silenziosamente lo stato condizionato del bundle frozen (EGARCH, regime, feature di prezzo) — esattamente il rischio che CAP-DATA-03 erediterebbe a valle. Per AC-13(b) il verdetto è **FAIL**.

Indipendentemente da W1, il task chiedeva di verificare se i pattern d'errore canonici di CAP-DATA-01 si ripresentano: **sì per due** — W9 cooldown (A r47-51 dichiara "14 connessioni / ~30s" come regola operativa, **refutata da M-5** nel regime ~1Hz: BUG REALE sostanziale aggiornato dall'empirico) e W5 codici errore (A r194-195 dichiara semantica 1004/1007 senza enumerazione né dump:timestamp, senza supporto level-2 in `is_error_line`: BUG REALE sostanziale, con dominio per giunta incompleto rispetto a M-3 che ha osservato 1017/1015/1003). Diversi item risultano invece **OK**: W4 CANDLERANGE e W7 100gg sono corroborati level-2 da D; W6 mesi F/I, W10 banner, W12 FDAX hanno ancora empirica level-1; W11 Q-A-3 è una scelta di design coerente (RM-1 non applicabile); il 1030 di A r196 è già RM-1-conforme. La **lista "Empirico-CLI da verificare" è non vuota (7 voci)**: per AC-13(d) il PASS non sarebbe comunque concedibile in sede WEB. In coerenza col divieto `reviewer.md:163`, il Web reviewer NON dichiara verificato/falsificato nulla di W2/W3/W5(trigger)/W6(Mar-Dic)/W8/W9(burst)/W10: le marca Empirico-CLI. Fanno **eccezione W1 e W13**, che NON richiedono prova DAPI nuova: la prova è già acquisita (D level-2 + M-1 level-1) e lo schema corretto è `C;L;H;O;V` — il finding è chiuso staticamente, va solo applicata la patch testuale.

Riepilogo conteggio: **4 BUG REALI** (#1 catastrofico, #2, #3, #4), **2 MIGLIORA PERFORMANCE** (#5, #7), **3 MIGLIORA PROCESSO** (#6, #8, #10), **1 NEUTRO** (#9), **0 RISCHIO PEGGIORAMENTO**. Verdetto WEB: **FAIL**.

---

## Applicazione RM a sé stesso (AC-9/10/11)

- **RM-1 (AC-9)**: la mia asserzione "A Cap.49 DIVERGE da D sul mapping CANDLE" è verificata enumerando le 3 dimensioni cercate (ordine dei 5 campi per posizione; mapping posizione→OHLC per ciascuna pos 5/6/7/8/9; convenzione di indicizzazione di colonna) e dichiarando per ciascuna l'esito (vedi W1.A3) — non ho dichiarato "coerente/divergente" senza enumerare cosa ho confrontato. Ho distinto esplicitamente "ordine campi DAPI (UFF;MIN;MAX;APE)" da "mapping campo→OHLC" come richiesto, e ho verificato che A fa un'asserzione diretta sul mapping (etichetta le posizioni con `<O>/<H>/<L>/<C>`), non una mera elencazione di colonne. Per le asserzioni empiriche che richiedono DAPI (W2/W3/W5-trigger/W6-MarDic/W8/W9-burst/W10) NON ho dichiarato verificato/falsificato: le ho marcate Empirico-CLI. Per W1/W13 dichiaro "errato" con base level-1 (M-1) + level-2 (D), entrambe acquisite staticamente senza accesso DAPI — legittimo in sede WEB.
- **RM-2 (AC-10)**: il grep di Check W2 è stato eseguito direttamente (comando citato) e i decoder esistenti sono elencati con path:linea (tabella "Decoder/parser esistenti nel repo per DAPI"). Nessuna conclusione su "decoder esistenti" senza grep diretto. Ho verificato che NESSUN codice di produzione dichiara `O;H;L;C` (isolando il finding come testuale, non di codice).
- **RM-3 (AC-11)**: ogni finding cita file:linea testuale fra virgolette, nessuna parafrasi a memoria. I riferimenti a M-1/M-3/M-4/M-5 sono etichettati `[PROVA-EMPIRICA 2026-05-29 via STATO_CORRENTE.md §5]`; i riferimenti a D/probe_dapi come `[CODICE-ESISTENTE r.NNN]`; il wiki come `[WIKI-HINT, dimostrato inesatto]`. I dump `probe_out/*` NON sono stati ispezionati (citati solo tramite M-3/M-5, forma versionata).
- **AC-12**: nessun file del perimetro A-D modificato; nessun file del repo modificato eccetto questo file di review. Working tree pulito su A/B/C/D (gli unici file dirty pre-esistenti sono `.claude/settings.json` e `.claude/scheduled_tasks.lock`, estranei al perimetro). D (decoder canonico) NON toccato.

---
PASS: nessun problema bloccante (osservazioni minori ammesse) — NON raggiunto.
CONDITIONAL: solo problemi non bloccanti — NON applicabile (presenti BUG REALI).
**FAIL: almeno un problema bloccante (W1 catastrofico + W5/W9 + W13) — Development deve correggere prima della chiusura RM-retro. + lista Empirico-CLI non vuota (handoff sede CLI).**
