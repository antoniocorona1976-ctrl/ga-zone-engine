# Probe-Review AUDIT-RM-RETRO CAP-DATA-02 (Parte 9) — fase EMPIRICA — Sede: CLI

**Sede**: CLI locale (workstation Windows del supervisore; DAPI live via DGo+Darwin su 127.0.0.1:10001 realtime e :10003 storico).
**Natura**: probe-review empirica (RM-4 opzione B, fase CLI) sulle 8 voci della lista "Empirico-CLI da verificare" pubblicata dal Web reviewer in `reviews/REVIEW_CAP_DATA_02_RM_RETRO_v2_review.md` §"Empirico-CLI da verificare". NON è CAP-review piena; NON ri-audita lo scope statico WEB (già PASS).
**Ruolo Reviewer** assunto da agente general-purpose (subagente nativo `reviewer` non disponibile nella CLI; ruolo adottato in pieno secondo `.claude/agents/reviewer.md`, incluse regole assolute, sezione "Probe-review (RM-4)" e divieti per sede CLI `:163-164`).

**Contesto operativo dato come autoritativo (NON ri-gateato)**: IDEM aperto (~11:10–11:20 CET, 2026-06-01); DGo+Darwin attivi su :10001/:10003; account `B6086` (non in chiaro, M-6); schema CANDLE `C;L;H;O` (M-1) già verificato e NON ri-testato (fuori lista).

**Strumento**: `scripts/probe_dapi.py` usato come libreria (`DapiConn`, `parse_line`, `run_candlerange`, costanti porte). NON modificato. Probe ad-hoc in `probe_out/` (gitignored): `cli_probe_errcodes.py`, `cli_probe_stream.py`, `cli_analyze.py`, `cli_w2_xcheck.py`, `cli_w2_vol.py`, `cli_w6_months.py`, `cli_w9_burst.py`, `cli_w9_burst2.py`, `cli_w10_banner.py`.

**Dump raw principali** (probe_out/, NON versionati):
- `w5_w10_20260601_111246.json` — W5a/W5b error codes + W10 banner
- `w2_w3_w6_20260601_111350.json` — stream FIB6F/DITAS/DGER (PRICE, BOOK_5, ANAG)
- `w2_vol_20260601_111546.json` — progressione temporale PRICE f5/f6/f7
- `w6_months_20260601_111616.json` — ANAG mesi IDEM
- `w9_burst_20260601_111818.json`, `w9_burst2_20260601_111842.json` — burst cooldown
- `w10_banner_20260601_111923.json` — banner ×6, due porte

---

## VERDETTO COMPLESSIVO: PASS EMPIRICO

7 voci verificabili confermate (W2 con una sotto-asserzione PARZIALE onesta; W3, W5a, W6-F/I, W9, W10 confermate); 2 voci PARZIALI per impossibilità oggettiva NON bloccanti (W5b/1030 non riproducibile sul FIB perché IDEM è nel servizio base; W8 riavvio mezzanotte non forzabile alle 11:18; W6 Mar/Dic non decodificabili perché i contratti non sono listati ora). **Nessuna asserzione SMENTITA = nessun BUG REALE bloccante.** Anzi, una hypothesis del Web reviewer su W2 (campi medi PRICE = `<bid_qty?>;<ask_qty?>`) è stata **falsificata e corretta** con prova diretta (sono day-low/day-high), e l'anomalia W3 (`bid1>ask1` del 27/05) è risultata **NON riprodotta** (artefatto del campione singolo a scadenza lontana, non difetto di schema).

---

## Esito per asserzione

### W2 — PRICE realtime (campi medi/estremi) — **CONFERMATA (con 1 sotto-campo PARZIALE)**

**Test (C1)**: SUB FIB6F (future), DITAS e DGER (cash) su :10001, cattura PRICE. Layout osservato: `PRICE;<ticker>;<HH:mm:ss>;<f4=last>;<f5>;<f6>;<f7>;<f8>;<f9>`.

Campioni (`dump w2_w3_w6_20260601_111350.json`):
- `PRICE;FIB6F;11:13:48;50160.0;1;2625;2446;49975.0;50240.0`
- `PRICE;dITAS;11:13:44;50097.75;1;1360;1223;49917.75;50177.75`
- `PRICE;dGER;...;25196.0;0;0;0;25075.0;25199.4`

**C2 — falsificazione bit-a-bit** (`dump w2_w3_w6` + `w2_vol_20260601_111546.json`, cross-check daily CANDLE in `cli_w2_xcheck.py`):

- **f8/f9 = day_low / day_high — CONFERMATO**, hypothesis "bid/ask" del Web reviewer FALSIFICATA. Confronto con il daily CANDLE odierno (CANDLERANGE 86400):
  - FIB6F: f8=49975.0 = daily L=49975.0 ✓; f9=50240.0 = daily H=50240.0 ✓
  - DITAS: f8=49917.75 = daily L ✓; f9=50177.75 = daily H ✓
  - DGER: f8=25075.0 = daily L ✓; f9=25199.4 ≈ daily H=25199.5 (rounding realtime)
  - **Esclusa** l'alternativa f8/f9 = best bid/ask: il BOOK_5 simultaneo dava best bid≈50155–50160 e best ask≈50165, ben dentro [f8,f9]=[49975,50240]. Quindi f8/f9 NON sono il book.
- **f6 = volume cumulato di giornata (lots) — CONFERMATO**: monotòno crescente nel tempo (FIB6F: 2625 → 2632 → 2633) e coincidente col campo V del daily CANDLE (V=2630 al fetch, in crescita). Esclusa l'alternativa "f6=qty ultimo trade" (sarebbe non-monotòno e piccolo).
- **f5, f7 — PARZIALE**: f5=1 costante (plausibile qty ultimo trade); f7 monotòno crescente (2446→2454→2455) con offset ~costante da f6. Coerenti con due contatori cumulativi distinti (es. f7 = n. contratti/trade vs f6 = volume), ma **un incremento +1 simultaneo su f6 e f7 non disambigua** se f7 sia "numero trade" o un secondo conteggio di volume. **ALTERNATIVE NON ESCLUSE**: f5∈{last_qty, n_book_levels}, f7∈{cum_trades, cum_volume_secondo_unità}. Per i cash (DGER) f5=f6=f7=0 (nessun trade sul cash index) → coerente con "contatori di trading", non con "book".

**C3 — casi non visti**: cash index untraded (DGER) → tutti i contatori a 0 ma f8/f9 = banda del giorno valorizzata → conferma che f8/f9 sono estremi di prezzo indipendenti dal trading, f5/f6/f7 sono contatori di trade.

VERIFICA: PRICE f8=day_low, f9=day_high, f6=volume cumulato; f5/f7 contatori cumulativi non disambiguati.
PROVE: [PROVA-EMPIRICA 2026-06-01] dump w2_w3_w6 + w2_vol; cross-check daily CANDLE (cli_w2_xcheck.py).
ALTERNATIVE COMPATIBILI ESCLUSE: f8/f9=best bid/ask (escluso da confronto BOOK_5 simultaneo); f6=qty-ultimo-trade (escluso da monotonia + match con CANDLE.V).
ALTERNATIVE COMPATIBILI NON ESCLUSE: semantica esatta di f5 (last_qty?) e f7 (n_trades? vs cum_volume_2); resta verifica parziale su questi due soli campi.

### W3 — BOOK_5 (FIB future) — **CONFERMATA** (anomalia 27/05 NON riprodotta)

**Test (C1)**: SUB FIB6F front-month (GIU26, liquido), 29 eventi BOOK_5 catturati (`dump w2_w3_w6`, analisi `cli_analyze.py`).

Layout: `BOOK_5;<ticker>;<HH:mm:ss>;` + **30 campi = 10 triple** = `(lots,orders,price)`. Blocco 1 = 5 livelli BID, blocco 2 = 5 livelli ASK.

**C2 — certificazione bit-a-bit** su 29 eventi / 290 triple:
- **Blocco 1 (triple 1–5) = BID**: prezzi sempre DISCENDENTI (best=bid1 in pos 1). Vero su 29/29 eventi.
- **Blocco 2 (triple 6–10) = ASK**: prezzi sempre ASCENDENTI (best=ask1 in pos 6). Vero su 29/29 eventi.
- **bid1_price < ask1_price su 29/29 eventi** (es. ts=11:13:50 bid1=50155.0 < ask1=50165.0; ts=11:13:51 bid1=50160.0 < ask1=50165.0). Spread 5–10pt (1–2 tick) coerente con front-month liquido.
- **Posizione del triplo `(lots, orders, price)` certificata**: su tutte le 290 triple f1≥f2 (290/290), coerente con f1=lots ≥ f2=orders (numero di proposte ≤ lotti totali); price è il 3° elemento. Esclusa l'alternativa `(orders, lots, price)` (richiederebbe orders≥lots, mai osservato) e `(price, ...)` (il 3° campo è sempre il multiplo-di-5 prezzo).
- Quindi `bid1_lots`=campo 4 (1ª tripla, pos f1), `bid1_orders`=campo 5, `bid1_price`=campo 6; `ask1_lots`=campo 19 (6ª tripla), `ask1_price`=campo 21. **Posizioni da cui dipende la regola `bar_synthetic` di Cap.49 CERTIFICATE.**

**Anomalia 27/05 (`bid1_price=49715 > ask1_price=49275`)**: **NON riprodotta**. Su 29 eventi del front-month liquido bid1<ask1 sempre. L'anomalia del campione singolo 27/05 (FIB6I, scadenza più lontana/illiquida) è un **artefatto del campione** (book rado/crossato su contratto poco scambiato), NON un'inversione dei blocchi BID/ASK nello schema. Lo schema è BID-poi-ASK con best-first in entrambi.

VERIFICA: BOOK_5 = `[BID×5 best-first][ASK×5 best-first]`, triple `(lots,orders,price)`; bid1_lots/ask1_lots/bid1_price nelle posizioni dette.
PROVE: [PROVA-EMPIRICA 2026-06-01] 29 eventi FIB6F, 290 triple; ordinamento prezzi e f1≥f2 su 100% (cli_analyze.py).
ALTERNATIVE COMPATIBILI ESCLUSE: ordine ASK-poi-BID (escluso: blocco1 sempre discendente=BID); triplo (orders,lots,price) (escluso: f1≥f2 290/290); "bid1>ask1 strutturale" (escluso: bid1<ask1 29/29).
ALTERNATIVE COMPATIBILI NON ESCLUSE: nessuna sulle posizioni interrogate (la sotto-distinzione lots vs orders entro la coppia f1/f2 è risolta da f1≥f2; l'etichetta semantica "orders" per f2 resta nominale ma non incide su bar_synthetic, che usa lots e price).

### W5a — codici errore — **CONFERMATA** (5/5 codici + confini disambiguati)

**Test (C1+C2)** — comandi-trigger, dump `w5_w10_20260601_111246.json`:
- **1004** (comando ignoto): `HELP`→`ERR;HELP;1004` e `INFO`→`ERR;INFO;1004`, su ENTRAMBE le porte (10001 e 10003). ✓
- **1007** (ticker inesistente): `CANDLERANGE ZZZNOPE ...` (10003)→`ERR;ZZZNOPE;1007`; `SUB ZZZNOPE` (10001)→`ERR;ZZZNOPE;1007`. ✓
- **1017** (sintassi malformata): `CANDLERANGE FIB6F` (pochi arg)→`ERR;;1017`; `CANDLERANGE FIB6F 60 ... ...` (period come 2° arg)→`ERR;;1017`. ✓
- **1015** (data invalida): `CANDLERANGE FIB6F notadate notadate 60`→`ERR;1015;20260221000000;20260601111314`. ✓ Codice **distinto** da 1017.
- **1003** (comando storico su porta realtime): `CANDLERANGE FIB6F ...` su **10001**→`ERR;N/A;1003`. ✓

**Confini disambiguati (C2)**: 1017 (struttura/arity sbagliata, ticker valido) ≠ 1015 (struttura ok ma valore data non parsabile) ≠ 1003 (comando valido ma su porta sbagliata) ≠ 1007 (ticker inesistente). Esclusa l'ipotesi "1017 copre anche data invalida" (data invalida → 1015, non 1017) e "qualsiasi errore comando → 1004" (1004 solo per verbo ignoto). Coerente con M-3 e con la tabella di CAP_09 `:205-209`.

VERIFICA: 1004=verbo ignoto, 1007=ticker inesistente, 1017=sintassi/arity, 1015=data invalida, 1003=storico-su-realtime.
PROVE: [PROVA-EMPIRICA 2026-06-01] dump w5_w10, ogni codice con trigger+riga ERR citata.
ALTERNATIVE COMPATIBILI ESCLUSE: 1017⊇data-invalida (escluso: 1015 distinto); 1004⊇qualsiasi-errore (escluso: codici distinti per ticker/sintassi).
ALTERNATIVE COMPATIBILI NON ESCLUSE: nessuna sui 5 codici testati.

### W5b — codice 1030 (realtime non sottoscritto) — **PARZIALE (non riproducibile sul FIB — NON bloccante)**

**Test**: `SUB FIB6F` su :10001 → restituisce ANAG + PRICE + BOOK_5 (subscription **riuscita**), nessun 1030 (dump `w5_w10`, record `1030_attempt_fib_rt`). Conferma M-3: l'IDEM/FIB è incluso nel servizio base dell'account B6086, quindi 1030 **non è riproducibile sul perimetro FIB** (servirebbe un ticker market-data gated, fuori perimetro, cross-index PHASE-2). Marcato **"non riprodotto / verifica parziale"** come previsto dal mandato — NON è uno SMENTITO bloccante (era già parziale in M-3).

VERIFICA: 1030 non osservabile sul FIB (IDEM nel servizio base).
PROVE: [PROVA-EMPIRICA 2026-06-01] SUB FIB6F → dati realtime, nessun 1030.
ALTERNATIVE NON ESCLUSE: semantica 1030 su ticker gated (Eurex/CME non abilitato) — fuori perimetro FIB, Empirico-CLI a mercato aperto in PHASE-2.

### W6 — mesi IDEM — **CONFERMATA per F/I; PARZIALE per Mar/Dic e FIB6L**

**Test (C1)** — SUB di FIB6{H,M,U,Z,I,F,L,G,J,C,X} + lettura ANAG (dump `w6_months_20260601_111616.json`):
- **FIB6F → `FTSE MIB INDEX FUTURE GIU26`** (ISIN IT0024209022) → **F = Giugno CONFERMATO** (level-1, ANAG ISIN+descr).
- **FIB6I → `FTSE MIB INDEX FUTURE SET26`** (ISIN IT0024847870) → **I = Settembre CONFERMATO** (level-1).
- Tutti gli altri (H, M, U, Z, L, G, J, C, X) → **`ERR;...;1007`** (ticker non listato/non abilitato ora).

**C2/C3 — disambiguazione**: al 2026-06-01 gli unici due futures FTSE MIB IDEM listati e subscrivibili sono **Giugno (F) e Settembre (I)** — le due scadenze trimestrali front. Le scadenze **Marzo e Dicembre NON sono listate ora** (1007), quindi le lettere-mese Mar/Dic **non sono decodificabili empiricamente in questa sessione** (impossibilità oggettiva: il contratto non esiste sul gateway). **FIB6L → 1007**: non è un ticker valido. NB metodologico (RM-3): la convenzione Directa è **non-standard** rispetto a CME/Eurex (F=Giugno, non Gennaio; I=Settembre) → le lettere Mar/Dic non si possono inferire per analogia, vanno lette via ANAG quando i contratti saranno listati.

VERIFICA: F=Giugno, I=Settembre (IDEM Directa); Mar/Dic non determinati.
PROVE: [PROVA-EMPIRICA 2026-06-01] ANAG FIB6F=GIU26, FIB6I=SET26; H/M/U/Z/L/...=1007.
ALTERNATIVE COMPATIBILI ESCLUSE: convenzione = CME-standard (esclusa: F≠Gennaio); FIB6L valido (escluso: 1007).
ALTERNATIVE COMPATIBILI NON ESCLUSE: lettere di Marzo e Dicembre (contratti non listati al 2026-06-01) → Empirico-CLI quando listati.

### W8 — riavvio Darwin mezzanotte — **PARZIALE (non forzabile alle 11:18 — NON bloccante)**

Osservazione PASSIVA cross-midnight, non riproducibile alle ~11:18 CET. Marcata **"da osservare in sessione notturna"** come da mandato. NON conta come SMENTITO. Nessun test eseguito (sarebbe zelo improprio forzare un riavvio — divieto `reviewer.md:164`).

VERIFICA: nessuna (rinviata a sessione notturna).
ALTERNATIVE NON ESCLUSE: esistenza/orario esatto del riavvio Darwin — Empirico-CLI cross-midnight.

### W9 — cooldown connessioni — **CONFERMATA la refutazione della costante "14/~30s"; soglia non osservata fino a ~900Hz**

**Test (C1+C2)** — burst open/close socket su :10003 a frequenza crescente (dump `w9_burst_20260601_111818.json` e `w9_burst2_20260601_111842.json`):
- Fase 1 (con drain banner, ~2Hz): 30+50+100 = 180 connessioni, **0 onset**.
- Fase 2 (connect+close immediato, alta frequenza): 50+100+200+500 = **850 connessioni, 0 onset**, frequenza misurata fino a **~907 Hz** (burst da 50 in 0.055s), e sostenuta ~90–200 Hz su burst da 100–500.

**C2 — falsificazione**: la "14ª connessione / cooldown ~30s" (dichiarata 27/05 in burst non disambiguato) è **REFUTATA come costante** ben oltre il regime ~1Hz di M-5 (75 conn): qui 850 connessioni consecutive fino a ~900 Hz senza alcun `ConnectionRefused`/`ConnectionReset`. Non esiste una soglia a 14 connessioni, né un cooldown ~30s, nel regime testato su :10003 a mercato aperto.

**C3 — confine non visto**: nessun onset osservato neppure ad alta frequenza → la *soglia/durata* di un eventuale cooldown a frequenze ancora più estreme, o su :10001 sotto carico, o lato server in condizioni diverse, resta non escludibile in assoluto — ma le **costanti specifiche "14" e "~30s" sono falsificate**.

VERIFICA: nessun cooldown su :10003 fino a 850 conn / ~907 Hz; "14ª conn / ~30s" refutata come costante.
PROVE: [PROVA-EMPIRICA 2026-06-01] dump w9_burst + w9_burst2, 0 onset su 850 conn.
ALTERNATIVE COMPATIBILI ESCLUSE: soglia "14 connessioni" (esclusa: 850 ok); cooldown "~30s" (escluso: nessun onset da recuperare).
ALTERNATIVE COMPATIBILI NON ESCLUSE: esistenza di un rate-limit a frequenze >>900 Hz o lato server in regimi non testati (non una costante dichiarata, resta ipotesi aperta minore).

### W10 — banner Darwin — **CONFERMATA**

**Test (C1+C2)** — banner ×6 su entrambe le porte (dump `w10_banner_20260601_111923.json`):
- Identico e stabile su 10001 e 10003, **len=142**, su 6/6 catture:
  `DARWIN_STATUS;CONN_OK;TRUE;Release  2.5.1 build 04/02/2025 11:00:00 more info at http://app1.directatrading.com/trading-api-directa/index.html`
- **Struttura a 4 campi** (split `;`): `DARWIN_STATUS` | `CONN_OK` | `TRUE` | `Release  2.5.1 build ... url`. La parte variabile è il **campo 4** (`Release ...`). I primi 3 campi sono costanti/di stato.
- Confronto col banner catturato dall'Orchestratore: **identico** (incluso il doppio spazio in `Release  2.5.1`). La forma "Release 2.5.1" (spazio singolo) citata in review è il rendering leggibile; il wire form ha doppio spazio.
- Il decoder `parse_line` matcha `startswith("DARWIN_STATUS")` → robusto a variazioni del campo 4 (coerente con la scelta documentata in CAP-DATA-01).

NB: nel run iniziale `sanity` il banner 10003 era apparso vuoto (`''`): è un **artefatto di timing** del drain (BANNER_TIMEOUT=2.0 occasionalmente in race); con timeout generoso il banner è sempre presente e pieno su entrambe le porte (6/6).

VERIFICA: banner stabile len=142, parte variabile = campo `Release ...`; identico su :10001/:10003.
PROVE: [PROVA-EMPIRICA 2026-06-01] dump w10_banner, 6 catture identiche.
ALTERNATIVE COMPATIBILI ESCLUSE: banner divergente tra porte (escluso: identico); banner assente su 10003 come fatto (escluso: artefatto di timeout, pieno con drain adeguato).
ALTERNATIVE COMPATIBILI NON ESCLUSE: variazione del campo `Release` su release Darwin diverse (non osservabile con una sola release installata) — Empirico-CLI minore.

---

## Riepilogo verdetti per voce

| Voce | Verdetto | Note |
|------|----------|------|
| W2 PRICE | **CONFERMATA** (f8/f9=day low/high, f6=cum volume) + PARZIALE su f5/f7 | hypothesis Web "bid/ask" FALSIFICATA |
| W3 BOOK_5 | **CONFERMATA** (BID×5 best-first / ASK×5 best-first; lots,ord,price) | anomalia 27/05 bid>ask NON riprodotta (artefatto) |
| W5a codici errore | **CONFERMATA** (1004/1007/1017/1015/1003, confini disambiguati) | — |
| W5b 1030 | **PARZIALE** (non riproducibile sul FIB, IDEM nel base) | NON bloccante |
| W6 mesi IDEM | **CONFERMATA F=Giu, I=Set**; PARZIALE Mar/Dic + FIB6L=1007 | contratti Mar/Dic non listati ora |
| W8 riavvio mezzanotte | **PARZIALE** (non forzabile alle 11:18) | NON bloccante, osservazione notturna |
| W9 cooldown | **CONFERMATA refutazione "14/~30s"** (850 conn / ~907Hz, 0 onset) | — |
| W10 banner | **CONFERMATA** (len=142, campo Release variabile) | — |

**0 asserzioni SMENTITE → 0 BUG REALI bloccanti.** PASS EMPIRICO.

---

## Applicazione RM a me stesso (AC-9/10/11)

- **RM-1 (AC-9)**: per ogni voce ho usato il formato VERIFICA/PROVE/ALTERNATIVE ESCLUSE/NON ESCLUSE. Dove restano alternative (W2 f5/f7; W5b; W6 Mar/Dic; W8; W9 frequenze estreme) ho scritto **PARZIALE**, non "verificato". Non ho dichiarato "verificato empiricamente" nulla oltre ciò che i dump mostrano puntualmente. Le permutazioni delle voci certificate (W3 ordine BID/ASK e triplo; W2 f8/f9; W9 costanti 14/30s) sono state **attivamente falsificate**, non solo ri-confermate (C2).
- **RM-2 (AC-10)**: ho riusato `scripts/probe_dapi.py` (`parse_line`, `DapiConn`, `run_candlerange`) come decoder esistente, senza riscriverlo né toccarlo; ho cross-controllato l'interpretazione dei campi CANDLE contro il suo `parse_line:247-273` e contro il decoder canonico (UFF/MIN/MAX/APE). Nessun nuovo decoder introdotto.
- **RM-3 (AC-11)**: ogni asserzione è ancorata a `dump:record` puntuale (file in probe_out + riga raw citata), non al wiki. Il banner W10 e la convenzione mesi W6 sono [PROVA-EMPIRICA 2026-06-01] level-1 (ANAG/banner diretti), non [WIKI-HINT]. Ho esplicitamente notato che la convenzione mesi Directa è non-standard (RM-3: non inferibile dalla doc esterna).
- **Divieto sede CLI (`reviewer.md:164`)**: ho riprodotto SOLO le 8 voci puntuali della lista Web, senza probe massivi di zelo. W8 non forzato (riavvio mezzanotte); W5b/1030 non insistito su ticker gated fuori perimetro; W9 con stop-on-onset (non ho martellato oltre il necessario a disambiguare, e non c'è stato onset).
- **File scritti**: unico file nel repo = questo review. Tutto il resto in `probe_out/` (gitignored). Nessun commit eseguito da me (committa l'Orchestratore). `scripts/probe_dapi.py` e `scripts/export_directa_history_parametric.py` NON toccati.

---

**VERDETTO: PASS EMPIRICO** — 8/8 voci processate: 5 CONFERMATE (W2, W3, W5a, W6-F/I, W9, W10), 0 SMENTITE; W5b/W8 PARZIALI per impossibilità oggettiva (NON bloccanti); W6-Mar/Dic e W2-f5/f7 PARZIALI dichiarate. La fase WEB (PASS) + questa fase CLI chiudono il debito empirico CAP-DATA-02 sul perimetro FIB. Residui Empirico-CLI rinviati (non bloccanti): W5b/1030 su ticker gated, W6 Mar/Dic quando listati, W8 cross-midnight, W2 f5/f7 fine-grained, W9 frequenze estreme.
