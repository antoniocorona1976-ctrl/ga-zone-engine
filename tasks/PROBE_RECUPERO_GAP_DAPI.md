# PROBE RECUPERO GAP DAPI — risultati empirici

**Esecutore**: Claude Code CLI locale (PC supervisore), sessione 2026-05-29
**Origine**: continuazione del briefing `tasks/HANDOFF_PROBE_DAPI_20260528.md` (sessione web 2026-05-28)
**Scopo**: validare empiricamente (V-1) l'equivalenza realtime↔CANDLERANGE e (V-2) il cut-off temporale di CANDLERANGE, come prerequisito tecnico a CAP-DATA-03.

> **Stato documento**: V-1 **morning** + V-2 completi e verificati. V-1 **afternoon** (finestra 14:30–15:00) da eseguire e da aggiungere alla §2.4. Questo NON è un capitolo metodologico (no CAP-DATA-03).

---

## 0. SINTESI ESECUTIVA (per il revisore web — leggere prima)

1. **Equivalenza realtime↔CANDLERANGE: CONFERMATA** per il timeframe 1-min, una volta corretto un bug di decoder. Dopo il fix: **55/60 minuti identici**; i 5 residui sono tutti spiegati (primo minuto troncato dalla SUB + scarti di 1 tick al confine del minuto), nessuno è un errore sistematico.

2. **⚠️ SCOPERTA CRITICA — schema CANDLE invertito su Open/Close.** Lo schema reale dei campi CANDLE NON è `O;L;H;C` (come dichiarato nel "fatto #1" del handoff e nel decoder di `probe_dapi.py`), ma **`C;L;H;O`** (in nomenclatura Directa: `UFF;MIN;MAX;APE`). Questo **contraddice una verifica già fatta dalla sessione web**. → vedi **§3, che richiede risposta esplicita del revisore web**.

3. **Impatto dello swap sui dati archiviati: NULLO.** Il bug era nel solo `scripts/probe_dapi.py` (nuovo, sessione 28/05). Lo script di produzione `scripts/export_directa_history_parametric.py` — che ha generato tutti i ~380 dump live + 256 archeologici — decodificava **già correttamente** (`UFF→close`, `APE→open`). I dati storici NON sono corrotti.

4. **Cut-off CANDLERANGE: confermato ~100 giorni di calendario MA SOLO per l'intraday.** Sul daily (period 86400) non esiste muro a 100 giorni. → §4.

5. **Fix applicato e su `origin/main`**: commit `a12ae32` (decoder `C;L;H;O` + tolleranza float in v1-compare) e `1c91769` (correzione M-1 in `STATO_CORRENTE.md`).

---

## 1. Setup e condizioni di esecuzione

| Voce | Valore |
|---|---|
| Data | 2026-05-29 (venerdì, mercati IDEM/MIB aperti) |
| Gateway | DGo + Darwin 2.5.1, porte locali `127.0.0.1:10001` (realtime) e `10003` (storico) |
| Account | `B6086` (non in chiaro nei commit) |
| Vincolo D-6 | TradingView Directa CHIUSO durante tutte le catture |
| Tickers | FIB6F (future giugno), DITAS (FTSE MIB cash), MINI6F, CM.MESM6 |

**Nota operativa importante (per il revisore)**: un primo tentativo di V-2 è fallito (`banner=''`, 0 candele, `ConnectionReset 10054`) perché **DGo era stato chiuso**. DGo/Darwin DEVE essere in esecuzione: è il processo che espone i socket DAPI locali. Da non confondere con il vincolo D-6 (che riguarda *TradingView*, non DGo). Riaperto DGo, tutto ha funzionato.

---

## 2. V-1 — Equivalenza realtime vs CANDLERANGE

### 2.1 Metodo

1. **Cattura realtime** (`v1-capture`): `SUB FIB6F` + `SUB DITAS` sulla porta 10001, stream continuo per 30 min (09:00:00→09:30:00), su connessione persistente (SUB+stream+UNSUB, niente raffiche di socket).
2. **Fetch storico** (`v1-fetch`): `CANDLERANGE` 1-min (period 60) sulla porta 10003 per la stessa finestra, lo stesso giorno (T+0).
3. **Confronto** (`v1-compare`): i tick PRICE realtime vengono aggregati in barre 1-min (open=primo tick, close=ultimo tick, low=min, high=max) e confrontati minuto-per-minuto con la barra CANDLERANGE.

### 2.2 Cattura realtime — esito

Finestra piena 09:00:10 → 09:30:00 (la SUB ha agganciato il flusso a +10s dall'inizio finestra).

| Tipo evento | Conteggio |
|---|---|
| `PRICE` (tick prezzo) | **1425** (FIB6F 1245, DITAS 180) |
| `BOOK_5` | 2585 |
| `ANAG` | 6 |
| `unknown` (parser fallito) | **0** |

File: `probe_out/v1_morning_20260529.raw.log` (585 KB), `probe_out/v1_morning_20260529.decoded.csv` (683 KB).

### 2.3 Confronto morning — PRIMA e DOPO il fix di schema

| Versione decoder | matches | mismatches | natura dei mismatch |
|---|---|---|---|
| `O;L;H;C` (originale) | 4/60 | **56/60** | swap O/C **sistematico** su quasi ogni minuto |
| `C;L;H;O` (fix) — senza tolleranza | 26/60 | 34/60 | residui = rumore float DITAS + primo minuto |
| `C;L;H;O` (fix) + tolleranza 0.05 | **55/60** | **5/60** | vedi sotto |

I **4 match casuali** con il decoder originale erano esattamente i minuti FIB6F in cui Open==Close (09:01, 09:12, 09:17, 09:24): gli unici dove lo swap è invisibile. Questo da solo già indicava il problema.

**I 5 mismatch residui dopo il fix** (tutti spiegati, nessuno è un errore di schema):

| Minuto | Δ | Causa |
|---|---|---|
| FIB6F 09:00 | open −50, high −35 | primo minuto: SUB agganciata a +10s → persi i primi tick (open reale non catturato) |
| DITAS 09:00 | open/high −5 | idem (primo minuto troncato) |
| FIB6F 09:04 | open −10 | scarto al confine minuto: primo tick visto ≠ open ufficiale |
| FIB6F 09:06 | close +5 | scarto di 1 tick sul close (last tick borderline) |
| FIB6F 09:25 | open −5 | scarto di 1 tick sull'open |

La **tolleranza 0.05** introdotta in v1-compare assorbe il rumore di precisione float (realtime DITAS arriva arrotondato a 2 decimali `49968.32`, la CANDLE storica ha precisione piena `49968.32031`: Δ≈3e-4, non è una discrepanza reale). 0.05 << 1 tick (5pt FIB), quindi uno scostamento vero anche di 1 solo tick resta visibile.

### 2.4 Confronto afternoon — DA ESEGUIRE

`v1-capture --window afternoon` (14:30–15:00) + `v1-fetch` + `v1-compare`. Atteso lo stesso esito. Da completare e inserire qui.

### 2.5 T+1 — DA ESEGUIRE domani

`v1-fetch --date 2026-05-29` ripetuto il 30/05 per verificare se CANDLERANGE riscrive le barre già passate (aggiustamenti notturni). Confronto T+0 vs T+1.

---

## 3. ⚠️ SCHEMA CANDLE — punto che RICHIEDE RISPOSTA DEL REVISORE WEB

> **Il supervisore chiede esplicitamente una risposta del revisore (code web) su questo punto**, perché lo schema CANDLE era stato dichiarato "verificato" dalla sessione web del 28/05, e ora risulta invertito su Open/Close.

### 3.1 Cosa dichiarava il handoff (fatto #1)

> *"Lo schema CANDLE reale = `O;L;H;C;V`. Il wiki DAPI dichiara `O;H;L;C` ma è inesatto. Verificato empiricamente su FIB6F daily (O=48742, L=47925, H=48875, C=48160) e DITAS daily."*

### 3.2 Cosa risulta da V-1

Lo schema reale è **`C;L;H;O;V`** = `UFF;MIN;MAX;APE;V`. Cioè: posizione `p[4]` = **CLOSE** (non open), posizione `p[7]` = **OPEN** (non close). Le posizioni `p[5]`=LOW e `p[6]`=HIGH erano **già corrette** in entrambi gli schemi.

### 3.3 PROVA DIRETTA (non statistica) — FIB6F minuto 09:08, 39 tick reali

Il flusso realtime è ground truth assoluto (prezzi eseguiti, ordinati per timestamp host):

| Grandezza | Valore | Significato |
|---|---|---|
| PRIMO tick del minuto | **50090** | = OPEN per definizione |
| ULTIMO tick del minuto | **50130** | = CLOSE per definizione |
| CANDLE storica, campo `p[4]` | **50130** | == ultimo tick → **`p[4]` è il CLOSE** |
| CANDLE storica, campo `p[7]` | **50090** | == primo tick → **`p[7]` è l'OPEN** |

Uguaglianza **esatta** (non approssimata) su prezzi provenienti da due canali indipendenti (realtime SUB vs storico CANDLERANGE). Questo chiude la questione senza margine: il campo che il decoder chiamava "open" contiene il close, e viceversa.

### 3.4 Tre prove indipendenti, tutte concordi

1. **Prova diretta** (sopra): primo/ultimo tick realtime == p[7]/p[4]. Esatta.
2. **Test di continuità** su dati storici puri (indipendente dal realtime): in una serie 1-min continua, `close[N]≈open[N+1]`. Risultato su 3 strumenti:
   - FIB6F: ipotesi swap O/C → 27/29 transizioni coerenti (err medio 3.6pt); ipotesi decoder-originale → 3/29 (err medio 26pt).
   - DITAS: swap 22/29; originale 5/29.
   - MINI6F: swap 22/29; originale 3/29.
3. **Confronto post-fix** (§2.3): FIB6F passa da 30 mismatch a 0 mismatch reali (26/30 minuti esatti, gli altri spiegati).

### 3.5 PERCHÉ la verifica web del 28/05 è passata accanto al problema

Questo è il nodo da capire (e la domanda diretta al revisore). La verifica del 28/05 era su **candele daily**. Ma:

> **Su una candela daily, Open e Close NON sono distinguibili guardando solo i 4 valori OHLC.** Sai che L=min e H=max (verificabili dai numeri, e infatti L/H erano sempre corretti). Ma "quale dei due valori rimanenti è l'apertura e quale la chiusura?" NON è decidibile senza un riferimento esterno (il primo/ultimo prezzo di quel giorno), che la sessione web non aveva.

Quindi la verifica del 28/05 ha confermato **L e H** (posizioni 5,6) e ha **assunto** l'ordine di O e C (posizioni 4,7) dalla convenzione, senza poterlo testare. V-1 è il **primo** test con accesso al ground truth intra-minuto, ed è lì che lo swap è emerso.

### 3.6 Grado di certezza (onesto)

- **CERTO** (prova diretta + continuità + post-fix): il campo in posizione `p[4]` è il close, `p[7]` è l'open. Non dipende dal fidarsi di alcuna etichetta.
- **CONVENZIONE, non verificato indipendentemente**: che `p[4]` si chiami "UFF" (ufficiale) e `p[7]` "APE" (apertura) nella nomenclatura Directa. Questa nomenclatura viene da `export_directa_history_parametric.py` e concorda al 100% con la prova empirica, ma la prova empirica regge anche senza di essa.

### 3.7 DOMANDA AL REVISORE WEB

1. Confermi che la "verifica empirica su daily" del 28/05 NON poteva distinguere O da C (solo L/H), e quindi il fatto #1 era un'assunzione non testata sull'ordine O/C?
2. Esiste da qualche parte (wiki, doc, codice precedente) una fonte che giustifichi `O;L;H;C` come ordine reale, che potrei aver trascurato? Se sì, va riconciliata con la prova diretta §3.3.
3. Confermi che i dump prodotti da `export_directa_history_parametric.py` (schema `UFF;MIN;MAX;APE`) sono corretti e NON necessitano rigenerazione?

---

## 4. V-2 — Cut-off temporale CANDLERANGE

### 4.1 Metodo

`v2-cutoff`: per N giorni crescenti [50, 80, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 160], query `CANDLERANGE` da `now − N giorni` a `now`, su connessione persistente (gap 0.6s). Si registra il `first_ts` effettivamente ottenuto e il conteggio candele. Il **punto di rottura** è il valore N oltre cui `first_ts` non regredisce più (il server tronca la storia).

Eseguito su due timeframe: **period 60** (1-min, intraday) e **period 86400** (daily).

### 4.2 Risultato INTRADAY (period 60s) — limite netto ~100 giorni di calendario

File: `probe_out/v2_cutoff_period60_20260529_104927.csv`

| N giorni richiesti | first_ts ottenuto | candele | note |
|---|---|---|---|
| 50 | 2026-04-09 10:49 | 26.526 | |
| **80** | **2026-02-18 09:56** | **38.567** | ← punto di saturazione |
| 90 | 2026-02-18 09:56 | 38.567 | identico a 80 |
| 100 | 2026-02-18 09:56 | 38.567 | identico |
| … | … | … | … |
| 160 | 2026-02-18 09:56 | 38.567 | **identico**: non va MAI oltre il 18/02 |

**Identico e simultaneo su FIB6F, DITAS, CM.MESM6.** Da N=80 in su, `first_ts` e conteggio si congelano al **2026-02-18 ~09:56**. Oggi 29/05 − 18/02 ≈ **100 giorni di calendario** → il server limita lo storico intraday agli ultimi ~100 giorni. Conferma empirica dell'Appendice A.2 del handoff.

⚠️ Il floor è al minuto 09:56, non all'apertura: il server **tronca al punto esatto del limite scorrevole**, non al giorno intero. Il limite è quindi una finestra mobile in giorni di calendario, non un confine di sessione.

### 4.3 Risultato DAILY (period 86400s) — NESSUN muro a 100 giorni

File: `probe_out/v2_cutoff_period86400_20260529_105739.csv`

| N giorni richiesti | first_ts ottenuto | candele |
|---|---|---|
| 50 | 2025-12-22 | 106 |
| 100 | 2026-02-23 | ~69 |
| 160 | **2026-01-05** | ~104 |

Sul daily il `first_ts` **continua a regredire** col crescere di N (a 160gg arriva al 5 gennaio, e proseguirebbe). **Il limite ~100 giorni è specifico dell'intraday, NON del daily.** (I conteggi daily oscillano per via dei giorni non-trading inclusi nel range di calendario, ma il `first_ts` non satura.)

### 4.4 Conseguenza operativa per CAP-DATA-03

- **Intraday (1-min, 5M, 15M, 1H)**: recuperabile via CANDLERANGE **solo gli ultimi ~100 giorni di calendario**. Tutto ciò che è più vecchio deve provenire dall'archivio locale già scaricato (`exports/` + overlay). Questo è il "gap" che dà il nome al probe.
- **Daily/Weekly**: nessun cut-off pratico → la storia profonda (anni) si prende a livello daily. Coerente con l'esistenza del cumulativo `DITAS_20110404_20260402` (15 anni daily).

---

## 5. Punti aperti

| # | Punto | Stato |
|---|---|---|
| 1 | **Risposta del revisore web sullo schema O/C** (§3.7) | **ATTESA** |
| 2 | V-1 afternoon (14:30) + ri-compare | da eseguire 29/05 |
| 3 | V-1 T+1 (re-fetch 29/05 il giorno 30/05) | da eseguire 30/05 |
| 4 | Re-run inventory CME (settle 28/05) | da eseguire dopo le 14:30 |
| 5 | Decodifica mesi IDEM Mar/Dic (M-4) | non eseguita |
| 6 | Inventory CSV con path hardcoded all'overlay | nota architetturale, non bloccante |

---

## 6. File prodotti (in `probe_out/`, gitignored)

| File | Contenuto |
|---|---|
| `v1_morning_20260529.raw.log` / `.decoded.csv` | cattura realtime morning (1425 tick PRICE) |
| `v1_hist_20260529_fetched_20260529_093304.csv` | fetch storico con decoder ORIGINALE (schema errato — conservato come evidenza dello swap) |
| `v1_hist_20260529_fetched_20260529_094821.csv` | fetch storico con decoder CORRETTO |
| `v1_compare_20260529_100125.json` | confronto finale (55/60 match, tolleranza 0.05) |
| `v2_cutoff_period60_20260529_104927.csv` | cut-off intraday (limite ~100gg) |
| `v2_cutoff_period86400_20260529_105739.csv` | cut-off daily (nessun limite a 100gg) |
