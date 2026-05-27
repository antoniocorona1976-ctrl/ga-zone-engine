# Parte 9 — Pipeline runtime FIB su Directa DAPI

Documento metodologico v2 — Motore genetico strutturale per segnali FIB. La Parte 9 formalizza il canale Directa DAPI come provider runtime esclusivo del FIB, completando la convenzione dati del progetto: la Parte 8 (Cap.37-44) congela la convenzione storica per il training (FIB pieno back-adjusted Portara/CQG, ratio-adjusted ricostruito in preprocessing); la Parte 9 (Cap.45-56) congela la convenzione runtime per l'inference real-time (Directa DAPI sul gateway Darwin in locale). La Parte si colloca in coda alla Parte 8 e immediatamente prima delle eventuali Parti successive e dell'Appendice operativa. Eventuali deviazioni dalla convenzione runtime in fasi successive del progetto richiedono ritorno al Planner.

La Parte 9 eredita gli invarianti metodologici delle Parti I-VIII e li applica al canale runtime. In particolare l'invariante `research semantics = runtime semantics` (Parte I Cap.1; Parte 8 Cap.37) e' applicato all'adapter DAPI: il bundle frozen calibrato sul tape storico Portara opera in runtime sulla griglia 1-min normalizzata prodotta dall'adapter Directa, senza alcuna re-calibrazione e senza alcuna re-mappatura dello schema dati. La continuita' del tape, il recupero automatico di gap entro 100 giorni di CANDLERANGE, la riconciliazione canonica giornaliera e la storicizzazione strutturata dei flussi DAPI sono dichiarate **fuori scope** dalla Parte 9 e rinviate al capitolo successivo (CAP-DATA-03 / Parte 10).

La Parte 9 si compone di dodici capitoli normativi (Cap.45-56), ciascuno dedicato a una decisione di convenzione runtime con razionale documentato, regola operativa e criterio di rollback registrato nel report supervisore `reports/REPORT_CAP_09.md`.

---

## Capitolo 45 — Premessa e collocazione

La Parte 9 risponde a una domanda specifica: come opera in produzione il motore genetico strutturale congelato sul tape storico Portara, quando deve emettere segnali su barre live del FIB nella sessione 08:00-22:00 CET (Parte I Cap.1; Parte 8 Cap.41 epoca E5). La risposta normativa: il canale dati live e' Directa DAPI sul gateway Darwin in locale, e la pipeline runtime applica l'**adapter DAPI -> bundle frozen Portara** (Cap.49) sui tick e sulle barre ricevuti dal gateway, senza modificare lo schema dati congelato in Parte 8 Cap.40.

**Relazione con CAP-DATA-01 / Parte 8.** La Parte 8 ha congelato il tape ufficiale di training (FIB pieno back-adjusted Portara/CQG ratio-adjusted, Cap.37-38), il filtro pre-expiry e la politica di rollover ($N=3$ giorni di trading, Cap.39), la regola di preprocessing della griglia 1-min regolare con flag `bar_synthetic` (Cap.40), la timeline ufficiale delle sessioni FIB E1-E5 (Cap.41), la convenzione cross-index PHASE-2 dichiarata ma non implementata nel doc v2 corrente (Cap.42), la procedura di sanity validation (Cap.43) e l'esclusione esplicita di fonti alternative (Cap.44). La Parte 9 non rilegge ne' rimodifica nessuna di queste decisioni: le applica all'adapter che traduce in tempo reale i record DAPI nella griglia normativa congelata.

**Invariante research = runtime applicato all'adapter.** Il bundle frozen prodotto dal walk-forward nested di Parte V Cap.25 e' calibrato sul tape Portara ratio-adjusted (Parte 8 Cap.37). In runtime, il modello legge feature calcolate da una griglia 1-min con il medesimo schema operativo: OHLCV, TickCount, flag `bar_synthetic` (Parte 8 Cap.40). L'adapter DAPI deve quindi produrre, per ogni minuto della sessione 08:00-22:00 CET corrente (epoca E5 di Parte 8 Cap.41), una barra normativa con lo stesso schema, le stesse regole di forward-fill su Close per i minuti senza trade e lo stesso flag `bar_synthetic = True` quando la barra e' sintetica. La pipeline di inference real-time di Parte VI Cap.27 e' consumer dell'adapter, non del canale DAPI grezzo: lo schema visto dall'inference e' invariato rispetto al training.

**Cosa formalizza la Parte 9.** La Parte 9 formalizza, in ordine: l'architettura del canale DAPI (Cap.46), il catalogo dei simboli FIB e dei cash europei rilevanti per il runtime (Cap.47), il format dati canonico runtime adottato dalla pipeline e dallo script di riferimento (Cap.48), la mappatura schema DAPI -> bundle frozen Portara con la tabella di conversione campo per campo (Cap.49), la gestione errori e il recovery (Cap.50), il warm-up degli stati condizionali all'avvio sessione (Cap.51), la sessione operativa runtime FIB 08:00-22:00 CET (Cap.52), la decisione Q-A sul gating qualitativo dei cash europei (Cap.53), l'audit log e la retention (Cap.54), i punti aperti fuori scope (Cap.55) e la tabella decisioni del capitolo (Cap.56).

**Riproducibilita' e replay deterministico.** Il replay bit-exact dichiarato come vincolo formale in Parte II Cap.10 si applica al motore in produzione: due esecuzioni indipendenti della pipeline runtime sulla medesima finestra storica DAPI devono propagare in modo identico la distinzione fra barre reali e barre sintetiche, la decodifica dei codici errore, le transizioni della state machine. Il vincolo si riflette nel formato dei log di audit (Cap.54), nel determinismo del ricalcolo delle feature dopo eventuali gap (rinvio CAP-DATA-03) e nel comportamento dell'adapter al riavvio mezzanotte del gateway Darwin (Cap.50).

---

## Capitolo 46 — Architettura del canale DAPI

Il canale Directa DAPI opera come servizio locale sul gateway Darwin (Directa SIM). La pipeline runtime ga-zone-engine si connette al gateway esclusivamente in loopback su `127.0.0.1`, mai da rete esterna o da macchina diversa. L'architettura del canale e' fissata dai parametri pubblici documentati nel wiki ufficiale Directa (`https://app1.directatrading.com/trading-api-directa/index.html`) e dalle verifiche empiriche del 2026-05-27 (banner `DARWIN_STATUS;CONN_OK;TRUE;Release 2.5.1 build 04/02/2025`, account `B6086`), registrate in `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md`.

**Banner del gateway Darwin.** Alla connessione il gateway risponde con il banner `DARWIN_STATUS;CONN_OK;TRUE;Release 2.5.1 build 04/02/2025`. Il banner contiene esplicitamente la release del gateway. La pipeline runtime registra il banner in audit (Cap.54) ad ogni handshake.

**Triplo porte canonico.** Il gateway pubblica tre porte locali distinte, configurate nel file di sistema `APIPortSettings.txt` (vedi `docs/runtime/dapi_port_settings_schema.md`):

| Porta | Ruolo | Uso in ga-zone-engine |
|-------|-------|-----------------------|
| `10001` | Datafeed realtime (push tick, book, anagrafica) | **IN scope** runtime FIB (push `PRICE`, `BOOK_5`, `ANAG` per FIB e cash europei) |
| `10002` | Submission ordini di trading | **FUORI scope** — il sistema non esegue ordini, solo emissione segnale via Telegram (Parte I Cap.1; Parte II Cap.9) |
| `10003` | Richieste storico (`CANDLERANGE`, `CANDLE`, `TBT`, `TBTRANGE`) | **IN scope** runtime FIB (warm-up stati condizionali al boot, pull storico ≤100gg) |

La porta `10002` non e' mai aperta dalla pipeline runtime. Il vincolo "solo emissione, nessuna esecuzione" e' obbligato da Parte I Cap.1 e Parte II Cap.9: il motore pubblica segnali su Telegram, l'operatore retail esegue manualmente da cellulare. L'esclusione di `10002` e' clausola di chiusura architetturale.

**File `APIPortSettings.txt` come identificatore locale.** Il file e' prodotto dal gateway Darwin al primo avvio e contiene una singola riga con quattro campi separati da `;`: `<account>;<rt>;<trd>;<hist>` (esempio anonimizzato: `<ACCOUNT>;10001;10002;10003`). Lo schema completo dei campi e' documentato nel file normativo `docs/runtime/dapi_port_settings_schema.md`. Il campo `account` e' l'identificatore dell'account abilitato al servizio DAPI sulla macchina locale. **Non e' una credenziale di autenticazione**: e' un identificatore locale prodotto dal gateway dopo che l'utente si e' gia' loggato in Darwin. L'autenticazione e' implicita nella sessione Darwin attiva sulla stessa macchina.

**Gap-1 — Autenticazione canale.** La pipeline runtime gira sulla **stessa macchina fisica** dell'account abilitato. Il gateway Darwin accetta connessioni esclusivamente in loopback (`127.0.0.1`), non e' supportata esecuzione remota o cloud. Il file `APIPortSettings.txt` e' identificatore locale per associare i comandi della pipeline alla sessione Darwin attiva; non e' una credenziale segreta da nascondere come password ma e' comunque dato sensibile / PII (lega un'azione di mercato a una persona fisica) e va escluso dal repo via `.gitignore`. La pipeline non scrive il file: lo legge in sola lettura per ricavare le porte e l'account code da loggare in audit (Cap.54). Il modello di sicurezza e' **locale-only single-account per macchina**.

**Vincolo uso esclusivo del canale (D-6).** Quando il gateway Darwin e' gia' impegnato da una sessione DGo (la piattaforma di trading desktop di Directa) o da TradingView con plugin Directa, i socket locali `127.0.0.1:10001` e `127.0.0.1:10003` entrano in conflitto con eventuali connessioni della pipeline ga-zone-engine. Il conflitto si manifesta tipicamente come `ConnectionRefusedError` immediatamente dopo la connessione, o come stringhe `Bad Request` ripetute sul datafeed UDF della sessione DGo (memoria persistente `feedback_no_dapi_probe_con_dgo_aperto`). La pipeline runtime non tenta workaround automatici: rileva il conflitto, marca lo stato come `RUNTIME_DEGRADED` nel log di audit (Cap.50 e Cap.54), notifica il supervisore via Telegram ed esce. La decisione operativa (chiudere DGo / TradingView, riavviare la pipeline) e' del supervisore, non automatica. Il vincolo D-6 (uso esclusivo del canale DAPI da parte della pipeline) e' non reversibile per la durata della sessione runtime.

**Pattern socket persistente.** Il probe empirico 2026-05-27 ha verificato che 26 comandi `CANDLERANGE` sequenziali a 0,6 s di gap su **una sola** connessione persistente (porta 10003) sono stati elaborati senza errori, mentre 14 connessioni TCP rapide aperte/chiuse ravvicinate hanno provocato `ConnectionResetError 10054` sulla 14ª connessione e successivo `ConnectionRefusedError 10061` per circa 30 secondi (cooldown). La pipeline runtime adotta quindi il pattern **una singola connessione persistente per porta** (10001 e 10003), mai aperture/chiusure per comando. Il limite "100 simboli sottoscrivibili" sulla porta 10001 (wiki DAPI) e' ortogonale e ampiamente sotto soglia: la pipeline sottoscrive in totale 1 simbolo futures FIB front-month + al piu' 4 simboli cash europei (DGER, DSTX50, DITAS, DFRA per gating qualitativo Cap.53), per un totale di al piu' 5 sottoscrizioni simultanee.

**Rate-limit osservato.** Le evidenze empiriche del 2026-05-27 fissano due regole operative:
- Una singola connessione persistente accetta **almeno 26 comandi sequenziali a 0,6 s di gap** senza errori. La pipeline runtime non oltrepassa questo regime nella prassi operativa.
- Aperture TCP rapide oltre la 14ª nello stesso intorno temporale provocano cooldown circa 30 s. La pipeline deve quindi evitare riconnessioni a raffica: ogni perdita di connessione richiede backoff esponenziale prima della retry (Cap.50).

Il rate-limit pubblico DAPI sui comandi `CANDLE`/`CANDLERANGE` non e' documentato dal wiki ufficiale. La regola operativa di lavoro e' quella verificata empiricamente: singola connessione persistente, niente burst di connessioni.

---

## Capitolo 47 — Catalogo simboli FIB e cash europei

Il catalogo dei simboli rilevanti per il runtime FIB su Directa DAPI e' chiuso e fissato. La pipeline runtime sottoscrive il simbolo futures FIB front-month sulla porta 10001 (datafeed realtime) e opzionalmente i simboli cash europei come logging / gating qualitativo (Cap.53). Il catalogo deriva dalle verifiche empiriche del 2026-05-27 (`tasks/INDAGINE_DIRECTA_CROSS_INDEX.md` Appendice A e Appendice B).

**Convenzione ticker IDEM FIB.** I ticker dei contratti future sull'IDEM seguono il pattern proprietario Directa `<CODE><YEAR><MONTH>`, dove `<CODE>` indica il prodotto (FIB pieno o miniFIB), `<YEAR>` e' l'ultima cifra dell'anno e `<MONTH>` e' il codice mese Directa-IDEM (proprietario, non standard CME). La verifica empirica del 2026-05-27 ha confermato `FIB6I` = FTSE MIB Index Future scadenza **settembre 2026** (ISIN `IT0024847870`, descrizione anagrafica `FTSE MIB INDEX FUTURE SET26`): il codice `I` corrisponde a **settembre** nella convenzione Directa-IDEM (non a Sep come nello standard CME, dove `U=Sep`). La lookup completa del codice mese Directa-IDEM (oltre `I=settembre`) e' punto aperto fuori scope (Cap.55) e va derivata via ANAG dal gateway.

**Tabella simboli FIB ammessi nel runtime.**

| Ticker DAPI | Strumento | Mercato | Moltiplicatore | Schema realtime | Note |
|-------------|-----------|---------|----------------|-----------------|------|
| `FIB6F` | FTSE MIB Index Future giugno 2026 | IDEM | 5 EUR/pt | `PRICE`, `BOOK_5`, `ANAG` | Front-month di esempio Q2 2026 (sample export 2026-01-07/2026-04-02) |
| `FIB6I` | FTSE MIB Index Future settembre 2026 | IDEM | 5 EUR/pt | `PRICE`, `BOOK_5`, `ANAG` | Verifica empirica 2026-05-27 (ANAG con descrizione `FTSE MIB INDEX FUTURE SET26`) |
| `MINI6F` | miniFIB giugno 2026 | IDEM | 1 EUR/pt | `PRICE`, `BOOK_5`, `ANAG` | Strumento di esecuzione operativa dell'operatore retail (Parte I Cap.2) |
| `MINI6I` | miniFIB settembre 2026 | IDEM | 1 EUR/pt | `PRICE`, `BOOK_5`, `ANAG` | Atteso valido per simmetria con FIB6I |
| `MINI6C` | miniFIB (mese da derivare) | IDEM | 1 EUR/pt | `PRICE`, `BOOK_5`, `ANAG` | Citato come esempio nello script `export_directa_history_parametric.py`; mese da derivare via ANAG |

**Coerenza con la convenzione di training (Parte 8 Cap.37).** Il bundle frozen e' calibrato sul FIB pieno (back-adjusted Portara/CQG ratio-adjusted) per le ragioni dichiarate in Parte 8 Cap.37: maggior profondita' temporale e maggior volume rispetto al miniFIB. Il runtime, coerentemente con l'invariante research = runtime, sottoscrive il **FIB pieno front-month** sul DAPI (`FIB6F` o `FIB6I` a seconda del front-month corrente) per il calcolo delle feature e per la valutazione del bundle. L'operatore retail esegue manualmente su miniFIB (Parte I Cap.2): la separazione fra strumento di calibrazione / inference (FIB pieno) e strumento di esecuzione (miniFIB) e' coerente con la separazione segnale / gestione posizione di Parte I Cap.2 ed e' fattuale nella prassi operativa del progetto.

**Tabella indici cash europei (gating qualitativo, Cap.53).** I cash europei accessibili via DAPI sono soggetti a market data realtime **gratuito** incluso nel servizio DAPI base (verifica empirica 2026-05-27, Appendice B di `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md`): non richiedono abilitazioni Eurex / CME aggiuntive a pagamento (le abilitazioni Eurex 7,50 EUR/mese e CME 15 USD/mese sono necessarie esclusivamente per i futures cross-index FDXM / DJ50 / ES / MES, fuori scope CAP-DATA-02 — vedi Cap.55 punti aperti).

| Ticker DAPI (SUB) | Ticker risposta | Sottostante | Schema realtime | Mercato data |
|-------------------|-----------------|-------------|-----------------|--------------|
| `DGER` | `dGER` (lowercase nella risposta) | Indice DAX cash (Germania) | `PRICE` | gratuito DAPI |
| `DSTX50` | `dSTX50` (atteso lowercase) | Indice EuroStoxx 50 cash (Eurozona) | `PRICE` | gratuito DAPI |
| `DITAS` | `dITAS` (lowercase nella risposta) | Indice FTSE MIB cash (Italia) | `PRICE` | gratuito DAPI |
| `DFRA` | `dFRA` (atteso lowercase) | Indice CAC 40 cash (Francia) | `PRICE` | gratuito DAPI |

**Importante (rinforzo Q-A-3 Cap.53).** L'inclusione di `DITAS` nel catalogo cash europei e' a fini di **logging operativo e gating qualitativo configurabile** fuori dal motore. Non costituisce mai sostituzione della serie ufficiale di training: l'esclusione del MIB cash come fonte di calibrazione e' clausola hard-locked di Parte 8 Cap.37 (motivazione: differenze su orari, microstruttura, basis, gap di apertura rispetto al contratto futures di esecuzione), e di Parte 8 Cap.44 (esclusione esplicita). Il cash europeo entra **esclusivamente** nel layer di gating qualitativo definito al Cap.53 sotto, mai nel feature tensor del GA e mai nella state machine del segnale.

**Schemi di risposta DAPI per realtime.**

Il gateway Darwin pubblica su porta 10001 risposte streaming con tre schemi principali, verificati empiricamente il 2026-05-27 (`tasks/INDAGINE_DIRECTA_CROSS_INDEX.md` Appendice B):

- Schema **`ANAG`** (anagrafica strumento, restituita una volta al SUB del simbolo): `ANAG;<TICKER>;<HH:mm:ss>;<ISIN>;<descrizione>;<ref_price>;<flag>;<flag>`. Esempio reale: `ANAG;FIB6I;14:05:30;IT0024847870;FTSE MIB INDEX FUTURE SET26;50040.0;0.0;0`. Lettura: la descrizione contiene il mese di scadenza in chiaro (`SET26 = settembre 2026`), permettendo al runtime di derivare il front-month per matching con il codice mese Directa-IDEM.
- Schema **`BOOK_5`** (book a 5 livelli, push streaming dopo SUB): `BOOK_5;<TICKER>;<HH:mm:ss>;<bid1_lots>;<bid1_ord>;<bid1_price>;<bid2..>;<bid3..>;<bid4..>;<bid5..>;<ask1_lots>;<ask1_ord>;<ask1_price>;<ask2..>;<ask3..>;<ask4..>;<ask5..>` (5 livelli BID + 5 livelli ASK, ciascuno con triplo `lots / orders / price`). Esempio reale: `BOOK_5;FIB6I;14:02:33;1;1;49715.0;1;1;49275.0;0;0;0.0;0;0;0.0;0;0;0.0;1;1;50535.0;1;1;51115.0;0;0;0.0;0;0;0.0;0;0;0.0`.
- Schema **`PRICE`** (tick streaming per indici cash, push dopo SUB): `PRICE;<ticker>;<HH:mm:ss>;<last>;<volume_lot?>;<bid_qty?>;<ask_qty?>;<low_session>;<high_session>`. Esempi reali: `PRICE;dGER;14:05:41;25251.9;0;0;0;25244.9;25400.9`; `PRICE;dITAS;14:05:43;49859.22;2;2318;2129;49859.22;50129.22`. Per gli indici cash il ticker nella risposta e' in **lowercase** (`dGER`, `dITAS`), mentre la SUB usa il maiuscolo (`SUB DGER`).

**Derivazione del front-month FIB.** Il runtime deve determinare automaticamente il ticker front-month da sottoscrivere. La procedura normativa: al boot della sessione, la pipeline esegue una sequenza di SUB su ticker candidati (`FIB6F`, `FIB6I`, `FIB6L`, ... seguendo la lookup mese Directa-IDEM), parsea la risposta `ANAG` di ciascuno, estrae la data di scadenza dalla descrizione (es. `SET26` → settembre 2026), e seleziona il **primo contratto in scadenza non ancora oltrepassato**, applicando inoltre il filtro pre-expiry $N=3$ giorni di trading di Parte 8 Cap.39 al passaggio del front-month al next-month (3 giorni di trading prima della scadenza, la pipeline switcha al next contratto in coerenza con la roll rule del training). La lookup completa codici mese Directa-IDEM e' punto aperto fuori scope (Cap.55).

---

## Capitolo 48 — Format dati canonico runtime

Il format dati canonico runtime e' la **rappresentazione standard** dei dati DAPI prodotta dalla pipeline runtime e dallo script di riferimento implementativo `scripts/export_directa_history_parametric.py` (committato nel repo). Il format e' simmetrico rispetto al formato del bundle frozen Portara (Parte 8 Cap.40): consente la verifica diretta della compatibilita' di schema con il training.

**Struttura output per simbolo e finestra temporale.** Per ogni richiesta `(simbolo, finestra temporale)`, la pipeline produce un'unica cartella con sei artefatti: cinque file CSV (uno per timeframe normativo: `D`, `W`, `1H`, `15M`, `5M`) piu' un file CSV unificato `<simbolo>_ALL.csv` e un file `<simbolo>_manifest.json`. La nomenclatura segue il pattern `<simbolo>_<start>_<end>/<simbolo>_<timeframe>.csv` documentato dallo script. I sample committati in `data/runtime/exports_sample/` (FIB6F, MINI6F, DITAS, multi-month da 2025-12-23 a 2026-04-02) sono il riferimento empirico.

**Schema CSV BOM UTF-8.** Ogni file CSV ha header obbligatorio BOM UTF-8 con i campi `symbol, timeframe, timestamp, date, time, open, high, low, close, volume, source`. Esempio reale (FIB6F, 5M, manifest del 2026-04-03):

```
symbol,timeframe,timestamp,date,time,open,high,low,close,volume,source
FIB6F,5M,2026-01-07 10:35:00,2026-01-07,10:35:00,45170,45170,45170,45170,1,DIRECTA
```

I campi `open, high, low, close` sono prezzi in unita' indice (multipli di 5 punti, coerente con tick FIB di Parte 8 Cap.41); `volume` e' contratti scambiati nella barra; `source` indica l'origine del record. Il campo `timestamp` e' la chiave normativa di allineamento temporale; `date` e `time` sono campi derivati di comodita' per il consumer downstream.

**Dominio del campo `source`.** Il campo `source` di ogni record CSV ha dominio chiuso a tre valori:

| Valore `source` | Significato | Quando viene prodotto |
|-----------------|-------------|------------------------|
| `DIRECTA` | Record proveniente direttamente dal DAPI nel timeframe richiesto | Il gateway risponde con candele nel timeframe nativo (es. `CANDLERANGE FIB6F ... 300` per 5M) |
| `AGG_FROM_60s` | Record aggregato dai dati 1-min ricevuti dal DAPI (timeframes superiori non disponibili direttamente per il simbolo) | La candela richiesta a 5M/15M/1H non e' nativa: lo script pulla 1-min e aggrega |
| `AGG_FROM_D` | Record aggregato dai dati daily (timeframe `W` non disponibile direttamente) | Il gateway non risponde con candele weekly: lo script aggrega dal daily (warning `Nessun weekly diretto ricevuto: ricostruisco dal daily.`) |

Il dominio chiuso a tre valori e' osservato direttamente nei manifest dei sample committati (es. `FIB6F_manifest.json`: `D = DIRECTA_86400`, `W = AGG_FROM_D`, `1H = DIRECTA_3600`, `15M = DIRECTA_900`, `5M = DIRECTA_300`). Per il runtime FIB la pipeline lavora sulla griglia 1-min; per il warm-up degli stati condizionali (Cap.51) puo' usare timeframes superiori aggregati con marker `AGG_FROM_60s`.

**Manifest JSON.** Per ogni esecuzione la pipeline produce un manifest `<simbolo>_manifest.json` che documenta in modo strutturato: simbolo richiesto, finestra di date, parametri di connessione (host, porta storico, account code, percorso file `APIPortSettings.txt`, banner Darwin), config risolto, per ogni timeframe (modo `DIRECTA_<period_s>` / `AGG_FROM_60s` / `AGG_FROM_D`, righe ricevute, primo e ultimo timestamp, lista comandi inviati, warning), warning aggregati, lista file generati, lista comandi inviati, timestamp di generazione. Il manifest e' artefatto **auditabile** e immutabile per ogni esecuzione: e' parte del corredo di evidenza per il replay deterministico (Parte 8 Cap.43 — sanity validation che la pipeline runtime puo' riprodurre risultati committati).

**Coerenza con la convenzione di back-adjustment di Parte 8 Cap.38.** Il format runtime opera sulla serie **unadjusted nativa** del contratto front-month corrente sottoscritto sul DAPI: il gateway pubblica candele del contratto specifico (es. `FIB6F`), non di una serie ratio-adjusted continua. La continuita' del tape attraverso i roll, la riconciliazione fra contratti front-month successivi e l'eventuale persistenza strutturata per uso di re-training futuro sono **fuori scope** CAP-DATA-02 e rinviati a CAP-DATA-03 (Cap.55). Per il runtime, la pipeline opera sul contratto front-month corrente per ciascuna sessione e applica il filtro pre-expiry $N=3$ giorni di trading di Parte 8 Cap.39 al passaggio fra contratti.

**Ruolo dello script `export_directa_history_parametric.py`.** Lo script committato in `scripts/export_directa_history_parametric.py` e' il **riferimento implementativo** del format dati canonico runtime: definisce la struttura della cartella di output, il header CSV con BOM UTF-8, lo schema del manifest JSON, la gestione dei chunk da 100 giorni per il limite storico DAPI e la decodifica delle risposte `CANDLERANGE` del gateway. Non e' codice operativo della pipeline runtime di produzione (che gestira' anche il datafeed realtime su porta 10001, non solo lo storico); e' un riferimento concreto per la sezione 8 dei sample committati. La sua presenza nel repo serve da specifica esecutiva non ambigua del format.

**Gap-5 — Test regressione exports.** La pipeline runtime, eseguita oggi su simboli con storico ≤100 giorni, deve produrre **output identico** a quello gia' archiviato nei sample (`data/runtime/exports_sample/FIB6F_20260107_20260402`, `MINI6F_20251223_20260402`, `DITAS_20251223_20260402`), a meno di righe nuove aggiunte nelle giornate successive alla data di archivio del sample. La regola operativa: a ogni rilascio della pipeline runtime, ri-eseguire una `CANDLERANGE` sui tre simboli campione nella finestra esatta dei sample e verificare il diff byte-per-byte sui file CSV (al netto delle nuove righe in coda eventualmente prodotte dal gateway su dati aggiornati). Differenze su righe gia' archiviate sono regressione del format e bloccano il rilascio. Il test e' un sanity check di non-regressione del format dati canonico, applicato come gate operativo prima del go-live e ad ogni modifica successiva della pipeline.

---

## Capitolo 49 — Mappatura schema DAPI -> bundle frozen Portara

Il bundle frozen prodotto dal walk-forward nested di Parte V Cap.25 e' calibrato sullo schema operativo del preprocessor di Parte 8 Cap.40. La pipeline runtime DAPI deve quindi tradurre, per ogni minuto della griglia 1-min normativa della sessione corrente (epoca E5 di Parte 8 Cap.41), un record DAPI in un record con **esattamente** lo stesso schema operativo, in modo che il bundle frozen possa essere applicato senza alcuna re-calibrazione. La tabella sottostante e' canonica.

| Campo bundle frozen Portara | Tipo / unita' | Origine DAPI runtime | Regola di derivazione |
|-----------------------------|----------------|----------------------|------------------------|
| `timestamp` (chiave temporale, 1-min) | datetime CET con conversione automatica CEST | timestamp della candela `CANDLE` o, in regime push tick, fine del minuto corrente | Il timestamp e' allineato alla griglia 1-min uniforme della sessione 08:00-22:00 CET (epoca E5 Parte 8 Cap.41). Coerente con timezone di Cap.52 (Gap-2). |
| `bar_open` ($\mathrm{Open}_t$, prezzo in punti FIB) | numero (multiplo di 5pt) | `CANDLE` campo 5 (`<O>`) | Copia diretta. Per minuti senza trade: forward-fill da `bar_close` $_{t-1}$ (regola normativa Parte 8 Cap.40). |
| `bar_high` ($\mathrm{High}_t$) | numero | `CANDLE` campo 6 (`<H>`) | Copia diretta. Per minuti senza trade: forward-fill da `bar_close` $_{t-1}$. |
| `bar_low` ($\mathrm{Low}_t$) | numero | `CANDLE` campo 7 (`<L>`) | Copia diretta. Per minuti senza trade: forward-fill da `bar_close` $_{t-1}$. |
| `bar_close` ($\mathrm{Close}_t$) | numero | `CANDLE` campo 8 (`<C>`) | Copia diretta. Per minuti senza trade: forward-fill da `bar_close` $_{t-1}$. |
| `volume` ($\mathrm{Volume}_t$, contratti) | intero ≥ 0 | `CANDLE` campo 9 (`<V>`) | Copia diretta. Per minuti senza trade: $\mathrm{Volume}_t = 0$. |
| `tick_count` ($\mathrm{TickCount}_t$, count tick aggregati nella barra) | intero ≥ 0 | DAPI **non** espone `TickCount` nello schema `CANDLE` documentato (campi 1-9). Per il runtime DAPI: derivato indirettamente dal contatore di tick aggregati dalla pipeline durante il minuto corrente (se in regime push tick `PRICE`) | Quando la pipeline aggrega tick `PRICE` minuto per minuto, conta i tick non nulli osservati nel minuto. Quando la pipeline lavora su `CANDLE` storico DAPI (warm-up Cap.51), `tick_count` viene impostato a `volume` come proxy approssimativo o lasciato `NaN` e marcato come campo non auditabile sui record di warm-up. Il flag `bar_synthetic` discrimina i due regimi. |
| `bar_synthetic` (flag boolean) | bool | derivato da `volume` e da regola normativa Parte 8 Cap.40 | $\text{True}$ se il minuto $t$ della griglia uniforme non ha alcun trade (in regime push tick: nessun `PRICE` ricevuto entro il minuto; in regime CANDLE: la candela non e' presente nella risposta del gateway, ed e' interpolata per forward-fill). $\text{False}$ se il minuto ha almeno un trade reale. Regola identica a Parte 8 Cap.40. |

**Regola `bar_synthetic = True` in runtime.** La regola e' identica a quella congelata in Parte 8 Cap.40: per ogni minuto della griglia uniforme in cui il DAPI non riporta una barra (assenza di trade reale nel minuto, sia in regime storico CANDLE che in regime realtime push tick), la pipeline inserisce una barra sintetica con $\mathrm{Open}=\mathrm{High}=\mathrm{Low}=\mathrm{Close}=\mathrm{Close}_{t-1}$ (forward-fill su Close), $\mathrm{Volume}=0$, $\mathrm{TickCount}=0$ (o `NaN` su record di warm-up storico), `bar_synthetic = True`. Il flag e' propagato nel bundle frozen sui record runtime esattamente come nel training (Parte 8 Cap.40), preservando il vincolo di replay bit-exact (Parte II Cap.10).

**Coerenza con la regola d'uso a valle di Parte 8 Cap.40.** Le regole d'uso a valle congelate in Parte 8 Cap.40 si applicano simmetricamente al runtime:

- **Feature di volatilita'** (EGARCH di Parte III Cap.13, classificazione di regime di Parte III Cap.14, dispersione realized): calcolate **esclusivamente su barre con `bar_synthetic = False`**. Includere barre sintetiche (con rendimento log identicamente nullo) introdurrebbe bias verso bassa volatilita' e contaminerebbe lo stato condizionato. Identica a training.
- **Feature di prezzo** (livelli, distanze da zone Parte IV Cap.16, distanze da pivot strutturali Parte III Cap.15): usano la **griglia uniforme completa**, inclusi i minuti sintetici. Identica a training.
- **Feature di volume**: usano esclusivamente barre con `bar_synthetic = False` (le barre sintetiche hanno `volume = 0` per costruzione). Identica a training.
- **Feature di struttura** (pivot frattali Parte III Cap.15, EMA con reset cross-session $T_{warmup,\text{EMA}}=74$): usano la griglia uniforme completa per il time-indexing; pivot non spostati da barre sintetiche. Identica a training.
- **Touch della entry zone (raw touch Parte II Cap.7.3)**: mai dichiarato su una barra con `bar_synthetic = True`. La gap semantics di Parte II Cap.7.3 e' simmetrica fra training e runtime per via dell'invariante research = runtime.

**Implicazione operativa.** L'adapter DAPI -> bundle frozen non e' un layer di "traduzione semantica" del segnale: e' un layer di **normalizzazione di schema** che produce, in tempo reale, la stessa griglia 1-min con gli stessi campi e gli stessi flag del bundle frozen di training. Il bundle frozen non legge mai dati DAPI grezzi: legge sempre lo schema normalizzato. Eventuali patologie del canale DAPI (errori 1004/1007/1030, riavvio mezzanotte, conflitto DGo) sono assorbite dall'adapter e dal layer di recovery di Cap.50, non si propagano al bundle. Coerente con Parte VII Cap.31 (replay deterministico bit-exact, gap semantics implicita nel test su finestre OOS).

---

## Capitolo 50 — Gestione errori, recovery, riavvio Darwin

La pipeline runtime e' robusta a tre famiglie di errori: codici DAPI ricevuti come risposta a comandi (errori sintattici o di abilitazione), riavvio automatico giornaliero del gateway Darwin a mezzanotte (manutenzione server), conflitto con sessione DGo / TradingView Directa concorrente (vincolo D-6 di Cap.46). La gestione e' deterministica e non tenta workaround automatici fuori dalle regole congelate.

**Decodifica dei codici di errore DAPI osservati.** Il gateway Darwin restituisce errori nel formato `ERR;<TICKER_O_COMANDO>;<CODICE>`. I codici verificati empiricamente il 2026-05-27 (Appendice A e Appendice B di `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md`) e il loro trattamento normativo:

| Codice | Comando emittente / contesto | Significato | Azione pipeline runtime |
|--------|------------------------------|-------------|--------------------------|
| `1004` | `INFO`, `HELP`, `VER`, `STATUS`, `GETAVAILABLESTATUS` su porta 10001 (realtime); `UNSUB` con simbolo mai sottoscritto su 10001 | Comando non valido o non supportato dal protocollo realtime | Logga warning in audit (Cap.54). La pipeline runtime non usa comandi metadata del genere a regime; sull'`UNSUB` di simboli mai sottoscritti il warning e' ignorato. |
| `1007` | `CANDLERANGE` su porta 10003 (storico) | Strumento non abilitato per l'account, o ticker inesistente | Logga errore con marker `SYMBOL_NOT_ENABLED` in audit. La pipeline non tenta retry: il simbolo va corretto in configurazione. Se il simbolo e' il front-month FIB atteso, lo stato runtime si marca `RUNTIME_DEGRADED` (fallback a front-month corretto dopo controllo manuale del supervisore). |
| `1030` | `SUB <ticker>` su porta 10001 (realtime) | Market data realtime non sottoscritto per quel ticker (distinto da 1007: storico OK, realtime no) | Logga errore con marker `MARKET_DATA_NOT_SUBSCRIBED`. La pipeline non tenta retry: l'abilitazione market data e' decisione commerciale del supervisore. Per il FIB su account `B6086` non si osserva 1030 (l'IDEM e' incluso nel servizio base); 1030 e' atteso esclusivamente sui futures cross-index Eurex/CME (FUORI scope CAP-DATA-02 per D-1 niente market data a pagamento, Cap.55). |

**Backoff su perdita di connessione.** Le perdite di connessione TCP osservate empiricamente (`ConnectionResetError 10054` sulla 14ª connessione TCP rapida ravvicinata; `ConnectionRefusedError 10061` durante il cooldown ~30 s) richiedono backoff esponenziale prima della retry. Regola operativa: alla rilevazione di `ConnectionResetError` o `ConnectionRefusedError`, la pipeline attende un intervallo crescente (es. 5 s, 10 s, 20 s, 40 s, max 60 s) prima di tentare riconnessione; supera dopo 5 tentativi falliti consecutivi, marca lo stato `RUNTIME_DEGRADED` e notifica il supervisore. Nessun retry a raffica per evitare di amplificare il cooldown del gateway.

**Fallback aggregazione (sorgenti dati).** Quando il gateway non produce dati nel timeframe richiesto nativo, la pipeline applica le due regole di fallback canoniche del format dati (Cap.48):

- `AGG_FROM_60s`: timeframe superiore (5M, 15M, 1H) ricostruito aggregando candele 1-min ricevute dal DAPI. Marker `source = AGG_FROM_60s` nei record CSV. Usato dal warm-up degli stati condizionali (Cap.51) quando il gateway non risponde con candele native sui timeframe superiori.
- `AGG_FROM_D`: timeframe weekly ricostruito aggregando candele daily. Marker `source = AGG_FROM_D`. Warning automatico nel manifest (`Nessun weekly diretto ricevuto: ricostruisco dal daily.`). Osservato nei sample committati (`FIB6F_manifest.json`).

Nessun fallback automatico su fonti diverse da DAPI: l'esclusione di fonti alternative congelata in Parte 8 Cap.44 si applica anche in runtime. Se DAPI non e' raggiungibile, la pipeline non commuta su CFD broker, Yahoo, Investing o vendor alternativi.

**Gap-3 — Riavvio Darwin mezzanotte.** Il gateway Darwin esegue manutenzione automatica giornaliera circa a mezzanotte locale (documentato dal wiki DAPI), interrompendo le connessioni attive sulle porte 10001 e 10003. La regola operativa della pipeline runtime al riavvio:

1. Rilevazione della disconnessione via `ConnectionResetError` o assenza prolungata di tick su 10001.
2. Inserimento marker `RUNTIME_GAP_START` nel log di audit con timestamp UTC e motivazione `darwin_midnight_restart`.
3. Backoff esponenziale (vedi sopra) fino a riconnessione riuscita (tipicamente entro 1-5 minuti dopo mezzanotte).
4. Re-handshake con il gateway (banner Darwin atteso `DARWIN_STATUS;CONN_OK;TRUE;Release ...`).
5. Re-SUB su porta 10001 sui simboli FIB front-month e cash europei (Cap.47).
6. Re-pull warm-up storico su porta 10003 per copertura del gap fra la disconnessione e la riconnessione (Cap.51 — il warm-up coprira' anche le barre mancanti del riavvio).
7. Inserimento marker `RUNTIME_GAP_END` nel log di audit con timestamp UTC. Il gap rimane visibile nei log come intervallo strutturato auditabile, coerente con la gap semantics di Parte 8 Cap.40.

Il riavvio mezzanotte non viola il determinismo del replay (Parte II Cap.10; Parte VII Cap.31): le barre mancanti durante il gap sono ricostruite via warm-up post-riavvio o, se cadono in finestra di sessione attiva, marcate come `bar_synthetic = True` con forward-fill su Close.

**Stato `RUNTIME_DEGRADED` (D-6).** Quando la pipeline rileva conflitto con DGo / TradingView Directa concorrente (segnalato tipicamente da `ConnectionRefusedError` immediato post-handshake o da stringhe `Bad Request` sul datafeed UDF), l'azione e':

1. Logga errore in audit con marker `RUNTIME_DEGRADED_DGO_CONFLICT`.
2. Notifica il supervisore via Telegram (singolo messaggio con istruzione operativa: chiudere DGo / TradingView, riavviare la pipeline).
3. Esce dalla sessione runtime corrente. Nessun retry automatico, nessun fallback su porte alternative.

La decisione operativa (chiudere DGo / TradingView, ri-lanciare la pipeline manualmente) e' del supervisore: il vincolo D-6 di Cap.46 e' clausola operativa, non transitorio guasto.

**Coerenza con la pipeline di inference di Parte VI Cap.27.** La pipeline di inference real-time e' consumer dell'adapter DAPI (Cap.49): la valutazione del bundle frozen su ogni nuova barra completa avviene dopo che l'adapter ha prodotto il record normalizzato (con `bar_synthetic = False` o `True` secondo regola). Il recovery di Cap.50 e' interamente dentro il layer adapter: la pipeline di inference non vede mai stati intermedi di disconnessione, vede solo il flusso normalizzato di record. Il replay deterministico (Parte II Cap.10; Parte VII Cap.31) e' preservato.

---

## Capitolo 51 — Warm-up degli stati condizionali

Gli stati condizionali del motore — varianza condizionata $\hat{\sigma}(t)$ dell'EGARCH(1,1) (Parte III Cap.13), classificazione di regime intraday calmo/turbolento (Parte III Cap.14) con persistenza minima $T_{persist}=10$ barre e quantile $p=0{,}75$ su $N_{reg}=20$ sessioni, normalizzazione z-score MAD delle feature (Parte III Cap.15) con $W_{norm}=1000$ e $T_{warmup,\text{norm}}=100$, EMA con reset cross-session $T_{warmup,\text{EMA}}=74$ — richiedono un periodo di **warm-up** all'avvio sessione, durante il quale il modello non puo' emettere segnali validi. La pipeline runtime gestisce il warm-up via pull storico su porta 10003 al boot di ogni sessione operativa.

**Dimensione del lookback necessario.** Il warm-up tipico richiede un lookback di poche giornate di trading per re-inizializzare le quantita' condizionate (Parte III Cap.13 osservazione "coda bassa $N=5$" sulla finestra cross-session di EGARCH; Parte III Cap.14 $N_{reg}=20$ sessioni di rolling per il quantile di regime; Parte III Cap.15 $W_{norm}=1000$ barre di rolling per la normalizzazione z-score MAD). La somma di questi requisiti e' nell'ordine di 20-30 sessioni (~5-6 settimane di trading), ampiamente entro il limite **100 giorni intraday** del DAPI verificato empiricamente sui sample (Cap.46 rate-limit; Appendice A `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md`).

**Procedura di warm-up al boot di sessione.** Al primo boot della sessione operativa (08:00 CET, Cap.52), la pipeline runtime esegue:

1. Connessione su porta 10003 (storico).
2. `CANDLERANGE <FIB_front> <YYYYMMDD000000> <YYYYMMDD235959> 60` con finestra retrospettiva di $L_{warmup}$ giorni di trading (valore di lavoro $L_{warmup} \approx 30$ giorni, entro il limite 100gg DAPI, da congelare definitivamente in FASE-D del roadmap). Chunking automatico in finestre da ≤100 giorni se necessario, come implementato dallo script `export_directa_history_parametric.py`.
3. Decodifica delle candele 1-min ricevute, applicazione della regola normativa Parte 8 Cap.40 (forward-fill su Close per minuti mancanti, flag `bar_synthetic`).
4. Ricalcolo deterministico delle quantita' condizionate sul tape di warm-up: parametri EGARCH cross-session restano congelati dal bundle frozen (no re-calibrazione); la sola quantita' ricalcolata e' lo **stato condizionato corrente** $\hat{\sigma}(t_{warm-up})$ alla fine del periodo di warm-up. Analogamente per la classificazione di regime: il quantile $p=0{,}75$ del rolling $N_{reg}=20$ sessioni e' ricalcolato sulla finestra storica DAPI; la persistenza $T_{persist}=10$ barre e' applicata dall'inizio della sessione operativa runtime.
5. Inserimento marker `WARMUP_COMPLETE` nel log di audit con timestamp UTC alla fine del warm-up. Da quel momento la pipeline e' in regime steady-state e puo' emettere segnali validi.

**Limite 100 giorni e fallback Portara.** Il limite 100 giorni intraday del DAPI e' coperto dal warm-up tipico nell'80% dei casi (30 giorni di trading rappresentano ~6 settimane). Per casi di **restart dopo downtime > 100 giorni** (es. interruzione operativa prolungata della pipeline, manutenzione hardware, vacanza dell'operatore), il warm-up tramite DAPI non e' sufficiente: la pipeline deve cadere sul **tape storico Portara** (Parte 8 Cap.37, FIB ratio-adjusted Portara/CQG come fonte ufficiale di training) per coprire il gap >100gg. Il fallback Portara non e' un cambio di fonte training (il bundle frozen resta calibrato su Portara), e' un cambio di **fonte di pre-feed** del warm-up runtime. La logica:

- Se gap downtime ≤ 100 giorni: warm-up integrale via DAPI `CANDLERANGE` su porta 10003.
- Se gap downtime > 100 giorni: warm-up via Portara per la parte precedente i 100 giorni, integrazione DAPI per gli ultimi 100 giorni.
- Coerenza adapter: in entrambi i casi, l'output del warm-up e' la stessa griglia 1-min con schema bundle frozen Portara (Cap.49). L'origine concreta delle barre del warm-up non e' visibile alla pipeline di inference.

**Vincolo determinismo bit-exact.** Il warm-up e' parte del replay deterministico: due esecuzioni indipendenti della pipeline runtime sulla stessa data di restart, con la stessa configurazione $L_{warmup}$, devono produrre lo stesso stato condizionato post-warm-up. La regola e' coerente con Parte II Cap.10 (formato log e determinismo) e con Parte V Cap.25 (walk-forward fold-per-fold del rolling EGARCH $W=210.000$ barre, Q-06/C-4.1).

**Collocazione nel ciclo operativo.** Il warm-up e' chiamato come **primo step** della pipeline di inference real-time di Parte VI Cap.27: la pipeline di inference non parte mai con stato condizionato non inizializzato. L'output del warm-up alimenta lo stato iniziale dell'EGARCH (Parte III Cap.13, inizializzazione cross-session osservazione coda bassa $N=5$), della classificazione di regime (Parte III Cap.14), della normalizzazione z-score (Parte III Cap.15, $T_{warmup,\text{norm}}=100$), e dell'EMA con reset cross-session (Parte III Cap.15, $T_{warmup,\text{EMA}}=74$). Solo dopo `WARMUP_COMPLETE` la pipeline accetta nuove barre real-time dalla porta 10001 e puo' emettere segnali.

---

## Capitolo 52 — Sessione operativa runtime FIB 08:00-22:00 CET

La sessione operativa runtime del FIB e' la finestra **08:00-22:00 CET** (epoca corrente E5 di Parte 8 Cap.41, in vigore dal 2020-02-17). La pipeline runtime opera esclusivamente in questa finestra; fuori dalla sessione, la pipeline e' in stand-by (resta connessa al gateway per monitoraggio del riavvio mezzanotte di Cap.50, ma non emette segnali e non valuta il bundle).

**Coerenza con Parte 8 Cap.41 (timeline ufficiale).** La sessione 08:00-22:00 CET corrisponde all'epoca E5 dichiarata nel file normativo `data/sessions/fib_session_calendar.csv` (Parte 8 Cap.41, schema a 6 campi `epoch_id, start_date, end_date, session_open_local, session_close_local, timezone`). La pipeline runtime legge questo file per derivare `session_open_local = 08:00` e `session_close_local = 22:00` per ogni giorno di sessione $d$ (giorno di trading IDEM). Il calendario dei giorni di trading (esclude weekend e festivita' IDEM) e' derivato dal calendario CET con convenzioni IDEM ereditate dalla pratica documentata.

**Gap-2 — Policy timezone CET/CEST.** Il gateway Darwin pubblica timestamp in **ora locale CET** con conversione automatica a **CEST** quando l'ora legale e' in vigore (ultima domenica di marzo → ultima domenica di ottobre, calendario europeo standard). La pipeline runtime tratta i timestamp Darwin come **ora locale CET (con conversione automatica CEST)**, coerentemente con Parte 8 Cap.41 (note di interpretazione: "tutti i timestamp dichiarati `CET` includono la conversione automatica `CEST` quando in vigore"). La regola operativa interna alla pipeline:

- Timestamp ricevuti dal gateway: ora locale (CET o CEST a seconda della data). La pipeline non assume UTC dal gateway.
- Timestamp loggati in audit (Cap.54): UTC convertito dal client. La conversione e' deterministica (regola DST europea), riproducibile in replay.
- Timestamp persistiti nei CSV (formato `YYYY-MM-DD HH:MM:SS` del manifest e dei sample): ora locale CET / CEST, coerente con la timezone del file normativo Parte 8 Cap.41.

La doppia rappresentazione (ora locale CET nei CSV e nei manifest, UTC nel log di audit) e' necessaria perche': la griglia 1-min del bundle frozen e' allineata a ora locale della sessione FIB (per coerenza diretta con il preprocessor di Parte 8 Cap.40), ma l'audit deve essere riproducibile su scala globale (UTC) per esigenze di compliance e di debug fuori dalla timezone italiana.

**Allineamento epoche FIB.** La sessione runtime corrente e' esclusivamente E5 (08:00-22:00 CET, in vigore dal 2020-02-17). Le epoche storiche E1-E4 (Parte 8 Cap.41) sono rilevanti **esclusivamente per il training** (Parte 8 Cap.37-40): la pipeline runtime non opera mai su epoche storiche. La pipeline non legge il file `data/sessions/fib_session_calendar.csv` per derivare orari diversi da E5 in regime steady-state. Solo il warm-up storico (Cap.51), se richiede dati di sessioni precedenti, applica gli orari corretti dell'epoca corrispondente (per coerenza con la convenzione di griglia di Parte 8 Cap.40); la pipeline di inference (Parte VI Cap.27) lavora esclusivamente su E5.

**State machine del segnale e finestra di sessione.** La state machine del segnale (Parte II Cap.7) include due timer rilevanti per la finestra di sessione:

- Timer pre-trigger $T_{touch}^{max}$ (Parte II Cap.7): tempo massimo entro cui il raw touch della zona puo' essere dichiarato dopo l'emissione del segnale.
- Timer post-trigger $\Delta t_{cromosoma}$ (Parte II Cap.7): tempo massimo di permanenza in stato attivo dopo il trigger.

Entrambi i timer sono espressi in barre 1-min e operano entro la finestra di sessione 08:00-22:00 CET. Nessun timer puo' superare la fine della sessione: alla chiusura (22:00 CET) i segnali ancora attivi vengono chiusi automaticamente (transizione a `expired` o `missed_target` secondo regola di Parte II Cap.7). La pipeline runtime applica la chiusura alle 22:00 CET locali (con conversione automatica CEST quando in vigore), in coerenza con il preprocessor di Parte 8 Cap.41.

**Apertura della sessione.** Alla riapertura di sessione (08:00 CET di ogni giorno di trading), la pipeline esegue:

1. Verifica banner Darwin (handshake atteso `DARWIN_STATUS;CONN_OK;TRUE;Release ...`).
2. Warm-up degli stati condizionali (Cap.51).
3. SUB FIB front-month e cash europei opzionali (Cap.47).
4. Marker `SESSION_OPEN` in audit con timestamp UTC e data sessione.
5. Da quel momento, la pipeline e' in regime steady-state.

Alla chiusura della sessione (22:00 CET): marker `SESSION_CLOSE` in audit con timestamp UTC, chiusura dei segnali attivi residui, UNSUB delle sottoscrizioni realtime, conservazione della connessione storica per il monitoraggio del riavvio mezzanotte (Cap.50).

---

## Capitolo 53 — Decisione Q-A: gating cash europei

**Verdetto Q-A-3 (ratificato).** I cash europei accessibili gratuitamente via DAPI base — DGER (DAX cash), DSTX50 (EuroStoxx 50 cash), DITAS (FTSE MIB cash), DFRA (CAC 40 cash) — entrano nella pipeline runtime **esclusivamente** come:

- **Logging operativo**: i tick `PRICE` di ciascun cash europeo sono loggati in audit (Cap.54) come canale di contesto. Il logging e' osservazione passiva: non altera la fitness, non altera lo stato del bundle frozen.
- **Gating qualitativo a basso costo per il supervisore umano**: regole esplicite, auditable e configurabili **fuori dal GA**. Esempi di gating: "se DGER scende > 2% intraday rispetto all'apertura, sospendi temporaneamente l'invio dei segnali long su FIB"; "se DSTX50 e DITAS divergono > 1% in direzione opposta, alza l'attenzione del supervisore via Telegram". Le regole sono configurate in file YAML versionato fuori dal genoma del cromosoma.

**Perimetro vincolante (Q-A-3).** Il cash europeo:

- **NON entra nel feature tensor** che alimenta il GA. Il catalogo 37 feature di Parte III Cap.15 e' invariato: nessuna feature derivata da DGER, DSTX50, DITAS, DFRA. La struttura del bundle frozen (Parte VII Cap.35) e' invariata.
- **NON entra nella state machine del segnale**. La state machine di Parte II Cap.7 non ha condizioni condizionate su variabili cash europee. Nessuna regola del tipo "if DGER drop > X then blocca segnale" entra nello state graph: la state machine resta deterministica, single-instrument, calibrata sul FIB.
- **NON entra nel cromosoma** dello spazio dei parametri di Parte V Cap.22. Il genoma del bundle non ha parametri condizionati su cash europei. Nessun parametro `cash_eur_threshold` o simile entra nel cromosoma.
- **NON entra nel walk-forward nested** di Parte V Cap.25. Il training e' single-instrument FIB su tape Portara ratio-adjusted (Parte 8 Cap.37); cash europei non sono nemmeno presenti nel tape di training.

**Vita operativa del gating qualitativo.** L'eventuale regola di gating qualitativo vive in un file di configurazione versionato fuori dal genoma del bundle, tipicamente `config/gating_rules.yaml` (o equivalente). Il file e' modificabile senza re-training del bundle: cambiare una soglia di gating non richiede di ri-eseguire il walk-forward di Parte V Cap.25. La separazione e' netta: il bundle frozen resta calibrato, il gating qualitativo opera **post-hoc** sull'output del bundle (segnali pronti per pubblicazione su Telegram), come filtro umano-supervisionato configurabile.

**Razionale della decisione Q-A-3.** La tabella sintetica del razionale:

| Opzione | Effetto sul GA | Costo / rischio | Verdetto |
|---------|----------------|------------------|----------|
| Q-A-1 (cash entra come feature) | Riapre training cross-index, rompe vincolo PHASE-1 FIB-only (Parte 8 Cap.42) | Alto: training infattibile DAPI limite 100gg; richiede vendor cross-index extra; viola la fasizzazione | Scartata |
| Q-A-2 (cash entra come stato gating dentro la state machine) | Modifica la state machine (Parte II Cap.7), richiede re-validazione walk-forward di tutti i fold | Medio-alto: cambio strutturale del payload e della state machine; carico Review elevato | Scartata |
| **Q-A-3 (cash come logging + gating qualitativo configurable fuori dal GA)** | Nessun cambio al GA, al cromosoma, al bundle, alla state machine, al feature tensor | Basso: opera fuori dal motore, modificabile senza re-training | **Ratificata** |

**Coerenza con Parte VIII / Cap.42.** La convenzione cross-index PHASE-2 di Parte 8 Cap.42 dichiara che DAX, EuroStoxx 50 e S&P 500 (mini) entrerebbero come strumenti cross-index in PHASE-2 con propria serie back-adjusted da vendor unico (Portara/CQG). Cap.42 norma esplicitamente i **futures** cross-index, non i cash europei. I cash europei DGER, DSTX50, DITAS, DFRA non sono "cross-index PHASE-2": sono canali di contesto live, accessibili gratuitamente sul DAPI base, usabili solo come logging e gating qualitativo. Quando PHASE-2 sara' attivata in un futuro ciclo di estensione del documento, i futures cross-index (FDAX, FESX, ES) entreranno nel layer di covarianza condizionata, mentre i cash europei resteranno gating qualitativo coerente con Q-A-3 corrente.

**Coerenza con Parte 8 Cap.37 (esclusione MIB cash).** L'esclusione del **MIB cash** come fonte di **training** congelata in Parte 8 Cap.37 e Parte 8 Cap.44 non viene modificata. DITAS (FTSE MIB cash) **non e' fonte di training**: e' canale di contesto runtime per gating qualitativo. La calibrazione dei modelli EGARCH (Parte III Cap.13), classificazione di regime (Parte III Cap.14), survival (Parte IV Cap.19), feature engineering (Parte III Cap.15) resta esclusivamente su FIB pieno ratio-adjusted Portara/CQG. La regola "no cash come fonte di training" e' invariata.

**Rollback.** La decisione Q-A-3 e' reversibile in capitolo successivo (es. CAP-DATA-03 / Parte 10, oppure futuri cicli di estensione metodologica) se l'esperienza operativa mostra che il logging cash e' inutile (nessun evento osservato) o dannoso (false-positive eccessivi sul gating). Il rollback non richiederebbe re-training del bundle: basterebbe disattivare le sottoscrizioni cash europee dalla pipeline runtime e svuotare il file `config/gating_rules.yaml`.

---

## Capitolo 54 — Audit log e retention

L'audit log della pipeline runtime e' il **corredo di evidenza** del comportamento del motore in produzione. Ogni comando inviato al gateway DAPI, ogni risposta ricevuta, ogni transizione di stato della pipeline, ogni segnale emesso e ogni decisione di gating qualitativo (Cap.53) sono loggati in modo strutturato e immutabile. L'audit log e' parte del corredo del bundle frozen in produzione (Parte VII Cap.35) ed e' input della dashboard di monitoraggio del lifecycle (Parte VI Cap.30).

**Contenuto loggato.** Per ogni evento operativo, il log registra:

- Timestamp UTC (ISO 8601 con precisione al secondo).
- Tipologia evento: `HANDSHAKE`, `SUB`, `UNSUB`, `CANDLERANGE_REQUEST`, `CANDLE_RESPONSE`, `BOOK_RESPONSE`, `PRICE_RESPONSE`, `ANAG_RESPONSE`, `ERR`, `SESSION_OPEN`, `SESSION_CLOSE`, `WARMUP_COMPLETE`, `RUNTIME_GAP_START`, `RUNTIME_GAP_END`, `RUNTIME_DEGRADED`, `SIGNAL_EMITTED`, `SIGNAL_TRIGGERED`, `SIGNAL_CLOSED`, `GATING_RULE_APPLIED`, `GATING_RULE_REJECTED`.
- Payload strutturato (JSON o equivalente) con: comando inviato testuale (per eventi di tipo richiesta), risposta ricevuta testuale (per eventi di tipo risposta), ticker (per eventi su simbolo), codici errore (per ERR), motivazione (per RUNTIME_GAP_*, RUNTIME_DEGRADED), payload del segnale (per SIGNAL_*), regola di gating (per GATING_*).
- Banner Darwin loggato in `HANDSHAKE`: registrazione esplicita della release del gateway (es. `Release 2.5.1 build 04/02/2025`) per riproducibilita' del replay (Parte II Cap.10).
- Account code: loggato sul `HANDSHAKE` ma trattato come dato PII / sensibile (Cap.46, Gap-1): puo' essere mascherato negli export pubblici dell'audit; resta in chiaro nel log locale per replay deterministico.

**Formato del log.** Il log e' file append-only (mai sovrascritto), con una riga per evento. Formato consigliato: JSON Lines (una riga = un oggetto JSON serializzato), con campi obbligatori `timestamp_utc`, `event_type`, `payload`, e campi opzionali `ticker`, `session_id`, `error_code`. La scelta del JSON Lines garantisce: parseability automatizzata, append-friendly (nessun lock su intero file), determinismo del replay (ogni evento e' isolato).

**Gap-4 — Retention policy.** La retention dell'audit log e' a due livelli:

- **Retention minima 90 giorni rolling** per ogni log generato: l'intera vita di un log file (dalla creazione alla compattazione / archiviazione) deve garantire accessibilita' per **almeno 90 giorni** dalla data di creazione. Permette il debug a posteriori di anomalie rilevate fino a 3 mesi dopo l'evento, coerente con la finestra di backtest e di confronto OOS (Parte VII Cap.31).
- **Retention permanente sui giorni di emissione segnale** (compliance interna): tutti i log che contengono almeno un evento `SIGNAL_EMITTED` o un evento `SIGNAL_TRIGGERED` o un evento `SIGNAL_CLOSED` sono **conservati permanentemente** (mai cancellati, nemmeno dopo i 90 giorni rolling). Permettono replay deterministico (Parte II Cap.10; Parte VII Cap.31) di qualunque segnale emesso, in qualunque finestra storica, per audit interno o per ricostruzione post-hoc del comportamento del motore. La permanenza e' a costo di storage marginale (un log file giornaliero per un anno e' nell'ordine di pochi MB).

**Compattazione / archiviazione.** Dopo i primi 30 giorni di vita di un log file, la pipeline puo' applicare compressione (gzip o equivalente) per ridurre l'occupazione disco. La compressione non altera l'integrita' del log: il file compresso e' ancora replay-able tramite decompressione on-the-fly. Compressione e' opzionale, non normativa; e' decisione operativa di lavoro della FASE-D del roadmap.

**Coerenza con la dashboard di monitoraggio (Parte VI Cap.30).** L'audit log e' input della dashboard di monitoraggio del lifecycle in produzione (Parte VI Cap.30): metriche live di executable/target-hit/invalidation rate, alert su deriva (deflated Sharpe Ratio in regime live, drawdown intraday, persistenza giorni `n/a` su $f_5^{live}$, ecc.) leggono il log per popolare i pannelli di sintesi. Il flusso e' uni-direzionale: la dashboard e' consumer dell'audit log, mai writer.

**Coerenza con il bundle frozen (Parte VII Cap.35).** L'immutabilita' del bundle frozen di Parte VII Cap.35 si applica al bundle congelato dopo il walk-forward di Parte V Cap.25. L'audit log e' parte del **corredo di evidenza** del bundle in produzione: insieme al bundle, e' archiviato come prova storica del comportamento del motore. La regola di sostituzione del bundle (Parte VII Cap.35) impone che l'audit log del bundle precedente sia archiviato permanentemente prima del rilascio del nuovo bundle, per consentire confronto pre/post.

**Gap-6 — Soglia commissioni.** Il servizio DAPI Datafeed di Directa ha costo pubblico **20 EUR/mese**, con regola di gratuita': se nel mese precedente le commissioni di trading dell'account hanno superato **200 EUR**, il DAPI Datafeed del mese corrente e' gratuito (fonte: `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md` Q3 e https://www.directa.it/help-supporto/piattaforme/api). La regola operativa della pipeline runtime sotto commissioni mensili < 200 EUR:

- La pipeline **tollera** l'addebito automatico di 20 EUR/mese sul conto. Non interrompe il servizio. Il vincolo D-1 ("niente market data a pagamento") di Cap.55 si applica esclusivamente ai market data **opzionali** dei futures cross-index (Eurex 7,50 EUR/mese, CME 15 USD/mese), non al servizio DAPI Datafeed di base (che e' necessario al funzionamento del motore in produzione e non e' classificato come "market data a pagamento" nel senso del vincolo D-1).
- La pipeline notifica il supervisore via Telegram (singolo messaggio mensile, generato dal layer di monitoraggio Parte VI Cap.30) con avviso: "Commissioni mensili sotto soglia 200 EUR. DAPI Datafeed addebitato 20 EUR mese corrente."
- Nessuna azione automatica di riduzione del consumo dati. La decisione di sospendere il servizio o di intensificare l'operativita' per superare la soglia 200 EUR/mese e' del supervisore. Coerente con Parte I Cap.2 (operatore retail, 1 contratto alla volta, decisione operativa manuale).

L'addebito 20 EUR/mese e' costo strutturale del runtime; il vincolo D-1 (no market data Eurex / CME extra) e' invariato sui cross-index futures.

---

## Capitolo 55 — Punti aperti fuori scope

I seguenti punti sono **fuori scope** CAP-DATA-02 e sono rinviati a sviluppi successivi del documento metodologico v2. La loro elencazione esplicita serve a tracciare i limiti normativi della Parte 9 e a indirizzare il Planner della prossima sessione su quali decisioni vanno aperte.

**Abilitazione FDAX standard (DAX Future Eurex 25 EUR/pt).** La verifica empirica 2026-05-27 ha confermato che l'account `B6086` **non e' abilitato** al ticker `FDAX` standard (DAX Future, moltiplicatore 25 EUR/pt sul mercato Eurex): tutte le varianti del ticker hanno restituito `ERR;<sym>;1007`. Sono abilitati esclusivamente i ticker Mini-DAX `EU.FDXMM6` (5 EUR/pt) e Micro-DAX `EU.FDXSM6` (1 EUR/pt). L'abilitazione FDAX standard richiederebbe contatto con il supporto commerciale Directa (modulistica, eventuale market data dedicato). Il punto e' **fuori scope CAP-DATA-02 per D-1** (niente market data a pagamento sui cross-index futures): se in PHASE-2 si decidesse di attivare i futures cross-index, l'abilitazione FDAX standard sarebbe parte della valutazione, ma non e' decisa in CAP-DATA-02.

**Lookup completa codici mese Directa-IDEM.** La verifica empirica 2026-05-27 ha confermato `I = settembre 2026` (FIB6I = `FTSE MIB INDEX FUTURE SET26`). La lookup completa degli altri codici mese Directa-IDEM (`F`, `J`, `L`, `M`, `O`, ... attesi per copertura dei 12 mesi) non e' stata verificata empiricamente nel ciclo di indagine corrente. La lookup deve essere derivata via comando `ANAG` sul gateway per ciascun ticker candidato del front-month corrente e successivi. Implementazione concreta e' parte della pipeline di runtime in FASE-D del roadmap; nel doc v2 corrente, la lookup completa non e' congelata.

**Vendor cross-index pluriennale (training cross-index PHASE-2).** Il limite 100 giorni intraday del DAPI e' strutturale a Directa e si applica a tutti gli strumenti (FIB, FDXM, DJ50, ES, MES). Per il training cross-index PHASE-2 (Parte 8 Cap.42), un vendor pluriennale parallelo a Portara e' necessario: candidati documentati in `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md` Q2 sono Portara stesso (se copre Eurex/CME), FirstRateData, Kibot, IQFeed, Databento, Polygon. La decisione e' rinviata a futuri cicli di estensione del documento metodologico v2 (PHASE-2 attivazione). Coerente con Parte 8 Cap.42 (estensioni future esplicite) e Parte 8 Cap.44 (esclusione esplicita di fonti alternative senza nuovo task Planner).

**Continuita' tape, recupero gap, riconciliazione canonica giornaliera, storicizzazione strutturata — CAP-DATA-03 / Parte 10.** I temi seguenti sono **fuori scope** CAP-DATA-02 e sono rinviati a CAP-DATA-03 (Parte 10 futura):

- Continuita' del tape attraverso le sessioni e attraverso i roll del contratto front-month.
- Recupero automatico di gap entro la finestra 100 giorni di `CANDLERANGE` (gap brevi causati da riavvio mezzanotte di Cap.50 o da downtime <100gg sono coperti dal warm-up di Cap.51; gap intermedi che richiedono ri-pull strutturato vivono in CAP-DATA-03).
- Riconciliazione canonica giornaliera fra il tape DAPI runtime e il tape Portara storico (sanity check operativo che verifica la coerenza schema su finestre comuni; estensione runtime della procedura di sanity validation di Parte 8 Cap.43).
- Storicizzazione strutturata del flusso DAPI per uso futuro come dataset di re-training (DAPI come fonte di training non e' ammesso oggi per il vincolo dei 100 giorni; CAP-DATA-03 normera' se e come archiviare strutturalmente il flusso DAPI per ricostruzione di una serie pluriennale futura).

Il rinvio esplicito a CAP-DATA-03 e' coerente con Scope OUT del task card corrente (continuita', recupero gap, riconciliazione, storicizzazione FUORI da CAP-DATA-02).

**M-2 OPEN — verifica empirica latenza Telegram ($L_{max}=30$s).** Il M-promemoria M-2 (Review v1 CAP-02, verifica empirica $L_{max}=30$s su latenza Telegram bot personale) resta `OPEN` come carryover ad Appendice E del documento (Telegram bot personale). Non si chiude in Parte 9: CAP-DATA-02 tratta il canale dati Directa (DAPI), non il canale di pubblicazione Telegram. Rinvio motivato; nessuna azione richiesta da Parte 9.

**Persistenza dei dati DAPI runtime per uso futuro come dataset di re-training.** Esplicitamente fuori scope CAP-DATA-02. Il vincolo della Parte 8 (Cap.37, FIB Portara/CQG come unica fonte ufficiale di training) e' invariato. Eventuale persistenza strutturale del flusso DAPI (per ricostruzione di una serie pluriennale futura, in alternativa a Portara) richiederebbe nuovo task Planner con riesame delle convenzioni di back-adjustment (Cap.38), roll log e politica di rollover (Cap.39), filtro pre-expiry (Cap.39). Rinvio a CAP-DATA-03 o a futuri cicli di estensione.

**Implementazione codice operativo della pipeline runtime.** Il presente capitolo e' **metodologia**, non codice. La codifica concreta della pipeline runtime (parser DAPI per realtime e storico, adapter DAPI -> bundle frozen, layer di recovery, layer di audit, layer di gating qualitativo) vive in FASE-D del roadmap del progetto, dopo il congelamento del bundle in FASE-C (training cloud su AWS spot c5.4xlarge, Parte I Cap.4) e dopo l'acquisizione dei dati Portara in FASE-B (Parte 8 Cap.37). Il presente capitolo norma la convenzione operativa e l'adapter, non l'implementazione.

---

## Capitolo 56 — Tabella decisioni del capitolo

La tabella sottostante riassume le decisioni normative del capitolo CAP-DATA-02 / Parte 9 con ID univoco, descrizione sintetica e motivazione di una riga. Le decisioni sono ratificate a chiusura del ciclo di review della Parte 9 e diventano normative per la pipeline runtime.

| ID | Decisione | Motivazione |
|----|-----------|-------------|
| D-9-1 | Canale DAPI come provider runtime esclusivo del FIB (Cap.45-46) | Coerenza con invariante research = runtime (Parte I Cap.1; Parte 8 Cap.37); Directa SIM e' broker di esecuzione e gateway dati live unico per FIB su IDEM. |
| D-9-2 | Porte 10001 (realtime) e 10003 (storico) sono in scope; porta 10002 (trading) e' fuori scope (Cap.46) | Vincolo "solo emissione, nessuna esecuzione" obbligato da Parte I Cap.1 e Parte II Cap.9. |
| D-9-3 | Autenticazione canale: pipeline runtime su stessa macchina dell'account abilitato; `APIPortSettings.txt` come identificatore, non credenziale (Gap-1 chiuso in Cap.46) | Modello di sicurezza Directa locale-only single-account per macchina; account code e' PII ma non e' password. |
| D-9-4 | Catalogo simboli FIB front-month e cash europei chiuso, codice mese Directa-IDEM `I=settembre` verificato empiricamente, lookup completa rinviata (Cap.47) | Verifica empirica 2026-05-27 (ANAG FIB6I `IT0024847870` descrizione `SET26`); lookup completa fuori scope, derivata via ANAG in implementazione. |
| D-9-5 | Format dati canonico runtime CSV BOM UTF-8 + manifest JSON; dominio `source ∈ {DIRECTA, AGG_FROM_60s, AGG_FROM_D}` (Cap.48) | Allineamento con script `export_directa_history_parametric.py` committato e con sample committati in `data/runtime/exports_sample/`. |
| D-9-6 | Test regressione exports come gate operativo pre-rilascio pipeline (Gap-5 chiuso in Cap.48) | Sanity check di non-regressione: ri-eseguire CANDLERANGE su sample committati e verificare diff byte-per-byte. |
| D-9-7 | Mappatura schema DAPI -> bundle frozen Portara tabella canonica; `bar_synthetic` propagato in runtime esattamente come in training (Cap.49) | Vincolo "research = runtime applicato all'adapter": il bundle frozen non vede mai dati DAPI grezzi, vede solo schema normalizzato simmetrico al preprocessor di Parte 8 Cap.40. |
| D-9-8 | Decodifica errori DAPI 1004 / 1007 / 1030 normata (Cap.50) | Verifica empirica 2026-05-27; mapping a azioni pipeline deterministiche; nessun retry a raffica. |
| D-9-9 | Riavvio Darwin mezzanotte gestito con marker `RUNTIME_GAP_START` / `RUNTIME_GAP_END` e re-warm-up post-restart (Gap-3 chiuso in Cap.50) | Manutenzione automatica giornaliera del gateway; backoff esponenziale; replay deterministico preservato. |
| D-9-10 | Conflitto DGo / TradingView gestito con stato `RUNTIME_DEGRADED` e notifica supervisore via Telegram, no workaround automatici (D-6 in Cap.46 e Cap.50) | Memoria persistente `feedback_no_dapi_probe_con_dgo_aperto`; decisione operativa del supervisore. |
| D-9-11 | Warm-up stati condizionali via DAPI fino a 100 giorni, fallback Portara per downtime > 100 giorni (Cap.51) | Lookback tipico ≤ 30 giorni copre EGARCH cross-session $N=5$, regime $N_{reg}=20$ sessioni, $W_{norm}=1000$; oltre 100 giorni serve Portara come pre-feed. |
| D-9-12 | Sessione operativa runtime 08:00-22:00 CET coerente con epoca E5 di Parte 8 Cap.41 (Cap.52) | Sessione FIB corrente in vigore dal 2020-02-17; calendario CET/CEST automatico ereditato dal preprocessor di Parte 8 Cap.41. |
| D-9-13 | Policy timezone: ora locale CET/CEST nei CSV/manifest, UTC nei log di audit (Gap-2 chiuso in Cap.52) | Doppia rappresentazione necessaria: CSV simmetrici al bundle frozen training, audit log riproducibile globalmente. |
| D-9-14 | Decisione Q-A-3 ratificata: cash europei come logging + gating qualitativo configurable fuori dal GA (Cap.53) | Coerenza con Parte I Cap.5 (definizione di successo invariata), Parte III Cap.15 (feature tensor 37 invariato), Parte V Cap.22 (cromosoma invariato), Parte 8 Cap.42 (cash europei non sono cross-index PHASE-2). |
| D-9-15 | Audit log JSON Lines append-only, retention minima 90 giorni rolling + retention permanente sui giorni di emissione segnale (Gap-4 chiuso in Cap.54) | Coerenza con Parte II Cap.10 (formato log determinismo), Parte VI Cap.30 (dashboard monitoraggio consumer), Parte VII Cap.35 (audit log parte del corredo bundle frozen). |
| D-9-16 | Soglia commissioni < 200 EUR/mese: pipeline tollera addebito 20 EUR/mese DAPI base e notifica supervisore via Telegram (Gap-6 chiuso in Cap.54) | DAPI Datafeed base e' costo strutturale del runtime, distinto dai market data Eurex/CME a pagamento (D-1); decisione operativa di sospensione e' del supervisore. |
| D-9-17 | Punti aperti fuori scope: FDAX standard, lookup completa codici mese IDEM, vendor cross-index pluriennale, continuita' tape / recupero gap / riconciliazione canonica / storicizzazione strutturata rinviati a CAP-DATA-03 / Parte 10 (Cap.55) | Rinvio motivato; Scope OUT del task card corrente. |

**Criteri di rollback registrati.** I criteri di rollback delle decisioni della Parte 9, da consultare in `reports/REPORT_CAP_09.md`, sono:

- D-9-14 (Q-A-3) reversibile in capitolo successivo se l'esperienza operativa mostra che il logging cash e' inutile o dannoso (rollback non richiede re-training del bundle).
- D-9-4 (tabella ticker DAPI) non reversibile (fattuale, verificato empiricamente 2026-05-27).
- D-9-7 (adapter `bar_synthetic` in runtime) non reversibile (invariante semantico ereditato da Parte 8 Cap.40).
- D-9-10 (vincolo D-6 uso esclusivo canale) non reversibile per la durata della sessione runtime corrente; revisione richiederebbe nuovo task Planner.
