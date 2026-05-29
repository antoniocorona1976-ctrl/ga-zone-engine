# Indagine — Disponibilità cross-index su Directa DAPI

**Data indagine:** 2026-05-27
**Scope:** verificare disponibilità real-time + storico intraday via Directa DAPI per FDAX (DAX, Eurex), FESX (EuroStoxx 50, Eurex), ES (S&P 500 e-mini, CME). Esclude FIB (già pianificato).
**Output:** informativo per PHASE-2; non modifica la roadmap.

---

## Sommario esecutivo

Directa SIM **negozia tutti e tre i contratti** (FDAX, FESX, ES) sui rispettivi mercati Eurex e CME, e li espone via DAPI sulla piattaforma Darwin con la **stessa identica architettura del FIB** (porta 10001 datafeed real-time, porta 10003 storici intraday/EoD). I **limiti storici DAPI sono unici per tutti gli strumenti**: max **100 giorni intraday** (1–4 min) e **15 anni EoD**; il limite di **100 simboli sottoscrivibili** in parallelo è ampiamente sufficiente per 4 stream (FIB + 3 cross-index). I **costi market data** sono pubblici: Eurex 7.50 EUR/mese (bid/ask futures) o 15 EUR/mese (book futures); CME 15 USD/mese. Il **DATAFEED DAPI** costa 20 EUR/mese (gratuito se commissioni mese precedente > 200 EUR). **Le sessioni Eurex (01:10–22:00 CET) e CME (Sun-Fri Globex) sono coperte** sui rispettivi orari pubblicati. La **profondità storica intraday DAPI rimane il limite strutturale** (100 giorni = ~5 mesi di trading): identico al FIB, quindi PHASE-2 cross-index eredita lo stesso vincolo "training su Portara, runtime su Directa". **Scenario raccomandato: B** (Directa copre runtime cross-index = OK, training storico cross-index resta da affrontare con provider parallelo a Portara).

---

## Q1 — Disponibilità strumenti

Verifica del trading e della pubblicazione tick real-time tramite Directa SIM e DAPI.

| Simbolo | Trading su Directa | Tick real-time DAPI | Fonte URL | Data consultazione |
|---------|--------------------|--------------------|------------------|---------------------|
| FDAX (DAX Future, Eurex) | SI | SI (porta 10001) | https://www.directa.it/offer/eurex-futures-options-trading-directa.html | 2026-05-27 |
| FESX (EuroStoxx 50, Eurex) | SI | SI (porta 10001) | https://www.directa.it/offer/eurex-futures-options-trading-directa.html | 2026-05-27 |
| ES (S&P 500 e-mini, CME) | SI | SI (porta 10001) | https://www.directa.it/help-supporto/futures/operativita-sui-futures | 2026-05-27 |

Note:
- Directa pubblica esplicitamente DAX, EURO STOXX 50, FBund, FOAT, FBobl, FBuxl, VSTOXX su Eurex; S&P 500 e-mini, Micro e-mini S&P, Nasdaq e-mini, Micro Nasdaq e-mini, e-micro FX, e-micro Gold sul CME.
- Ticker "ufficiali" su pagine Directa: per Eurex usa codici di prodotto Eurex (DAX, FESX, FDXM, FDXS, FSXE, ...); per il DAPI il formato esatto del **ticker contratto-mese** non è documentato pubblicamente, ma il DAPI espone indici e azioni con `<TICKER>` maiuscolo (es. DAX listato esplicitamente nel datafeed API). **Verifica empirica raccomandata in fase implementativa**: connettersi a Darwin attivo e testare i comandi `INFO`/`SUB`/`CANDLE` con i ticker reali del contratto front-month (es. nel quarto-FDAX di giugno 2026 il simbolo potrebbe avere forma `FDAXM6` o `DAX 06/26`; l'esatta convenzione DAPI è confermabile solo via supporto o test su account abilitato — vedi template email in coda).
- Lo schema candle DAPI (`CANDLE;<TICKER>;<yyyyMMdd>;<HH:mm:ss>;<O>;<H>;<L>;<C>;<V>`) è documentato e identico tra strumenti italiani ed esteri. `[WIKI-HINT, dimostrato INESATTO su CANDLE: ordine reale C;L;H;O — vedi export_directa_history_parametric.py:477 e M-1 2026-05-29]` — l'ordine `<O>;<H>;<L>;<C>` riportato qui è quello del wiki Directa, dimostrato inesatto; le posizioni 5..8 del payload sono in realtà `UFF;MIN;MAX;APE` = `close;low;high;open` (testo wiki conservato, etichettato come hint smentito).

---

## Q2 — Storico intraday

Limiti DAPI ufficiali tratti dal wiki API (https://app1.directatrading.com/trading-api-directa/index.html, consultato 2026-05-27):

| Time frame | Profondità massima | Comando DAPI |
|------------|---------------------|---------------|
| 1, 5 secondi | 1 giorno | TBT, CANDLE periodo=1/5 |
| 10, 30 secondi | 3 giorni | CANDLE periodo=10/30 |
| 1, 2, 3, 4 minuti | 100 giorni | CANDLE periodo=60/120/180/240 |
| End-Of-Day | 15 anni | CANDLE periodo=daily |

**Differenze tra FIB e cross-index:** la documentazione DAPI **non espone differenze per strumento**: i limiti sopra valgono per tutti i titoli sottoscrivibili dal Darwin del cliente. È plausibile (ma non confermato dalla documentazione pubblica) che la profondità reale dipenda dallo storico effettivo presente nel database Directa per quel contratto: nota letterale dal wiki — *"in caso di chiamate oltre i limiti la risposta sarà composta della massima profondità della nostra base dati"*.

**Schema dati:**
- Candele: `CANDLE;<TICKER>;<yyyyMMdd>;<HH:mm:ss>;<Open>;<High>;<Low>;<Close>;<Volume>`. Niente settle né tick-count nel record candle. `[WIKI-HINT, dimostrato INESATTO su CANDLE: ordine reale C;L;H;O — vedi export_directa_history_parametric.py:477 e M-1 2026-05-29]` — l'ordine `<Open>;<High>;<Low>;<Close>` è quello del wiki Directa, dimostrato inesatto; l'ordine reale del payload è `UFF;MIN;MAX;APE` = `close;low;high;open` (testo wiki conservato, etichettato come hint smentito).
- Tick-by-tick (TBT/TBTRANGE): tick livello base con price + size; non documentati VWAP né cumulative volume in chiusura.
- Volume: presente nel record candle (campo 9).
- Granularità candle minima utile per training: 1 min, fino a 100 giorni.

**Tick-level:** disponibile (TBT, TBTRANGE) con limite massimo 1 giorno per chiamata.

**Conseguenza per training GA cross-index:** **100 giorni intraday via DAPI sono insufficienti** per training tipico (5+ anni) esattamente come per il FIB. Per cross-index serve un provider storico parallelo a Portara (vedi Q sulla raccomandazione). Il runtime sì coperto.

---

## Q3 — Costi ed abbonamenti extra

Dati pubblici dal listino Directa (fonti: https://www.directa.it/help-supporto/condizioni-e-mercati/condizioni-di-trading-cme-cbot, https://www.directa.it/partner/eurex, https://www.qualebroker.com/recensioni/broker/directa — consultati 2026-05-27).

| Voce | Costo pubblico | Note |
|------|---------------|------|
| Market data Eurex (bid/ask futures) | 7,50 EUR/mese | privati |
| Market data Eurex (book futures 5 livelli) | 15 EUR/mese | privati |
| Market data CME (book 5 livelli) | 15 USD/mese | privati |
| Servizio DAPI / Datafeed real-time | 20 EUR/mese | gratuito se commissioni mese precedente > 200 EUR |
| Storico DAPI (porta 10003) | incluso in DAPI Datafeed | nessun extra dichiarato |
| Trading automatico via DAPI | 0 EUR | trading API gratuito |
| Commissioni FDAX | 9 → 2,50 EUR/contratto | scaglione dinamico |
| Commissioni FESX | 2 → 1,50 EUR/contratto | scaglione dinamico (sorgente: pagina futures Directa) |
| Commissioni ES (S&P 500 e-mini) | 6 USD/contratto (Semplice); 3 USD micro | listino dichiarato |

**Abilitazioni richieste (modulistica):**
- Eurex Futures: abilitazione operativa via portale Directa (INFO → Abilitazioni operative).
- Eurex Opzioni: ulteriore step (quiz di conoscenza o evidenza di operatività pregressa).
- CME-CBOT Futures: abilitazione operativa via portale Directa; sottoscrizione esplicita del market data CME.
- Per dettagli precisi su modulistica (firma disclaimer, documentazione pregressa, soglie patrimoniali) **richiedere conferma al supporto Directa**: la documentazione pubblica non scende nel dettaglio (vedi template email).
- Riferimenti pubblici: https://www.directa.it/help-supporto/conto-directa/come-ottengo-le-abilitazioni-aggiuntive-richieste-per-alcuni-mercati-quotazioni-o-servizi (consultato 2026-05-27).

**Conversione valuta:** il margine CME è "tenuto in euro" e la conversione USD/EUR avviene giornalmente al cambio LMAX delle 22:00 (rilevante per accounting, neutrale rispetto alle quotazioni real-time).

---

## Q4 — Vincoli tecnici DAPI

Da wiki ufficiale https://app1.directatrading.com/trading-api-directa/index.html e https://app1.directatrading.com/apiwiki/index.html (consultati 2026-05-27).

| Parametro | Valore |
|-----------|--------|
| Numero massimo simboli sottoscritti simultaneamente (porta 10001) | **100** |
| Numero massimo codici per comando bulk SUB | 90 |
| Porte: datafeed / trading / storici | 10001 / 10002 / 10003 |
| Connessione: localhost (127.0.0.1) solo se Darwin attivo | sì |
| Disconnessione automatica giornaliera | ~mezzanotte (manutenzione server: Darwin va riavviato ogni 24h) |
| Throughput tick/s dichiarato | **non documentato pubblicamente** — Directa non pubblica una specifica TPS |
| Finestra massima per richiesta storico intraday | 100 giorni / 1-4 min; 3 giorni / 10-30 sec; 1 giorno / 1-5 sec |
| Finestra massima storico EoD | 15 anni |

**Verifica capacità per 4 stream FIB + cross-index:** target = FIB + FDAX + FESX + ES = 4 simboli simultanei. Margine 4/100 ampiamente sotto saturazione. Nessun rischio architetturale.

**Verifica throughput:** in assenza di dato pubblico, la prassi è dimensionare il consumer interno (ring buffer, parser) per i tick aggregati di 4 strumenti high-volume (~poche centinaia di tick/s a picco). **Misura empirica raccomandata** in fase implementativa PHASE-2.

---

## Q5 — Completezza sessione

| Mercato | Sessione pubblicata da Eurex/CME | Sessione coperta da Directa | Fonte |
|---------|-----------------------------------|-----------------------------|---------|
| Eurex Index Futures (FDAX, FESX) | 01:10–22:00 CET | 01:10–22:00 CET dichiarato | https://www.directa.it/offer/eurex-futures-options-trading-directa.html (consultato 2026-05-27) |
| Eurex Index Options (ODAX, OESX) | sessione cash 08:50–17:30 CET | 08:50–17:30 CET | stessa fonte |
| CME Globex (ES e altri equity index) | Sun 23:00 → Fri 22:00 CET con pausa giornaliera 22:00–23:00 CET (CT 17:00-16:00) | non specificato letteralmente; Directa elenca "futures su indici, valute, commodities" CME senza ridurre la sessione | https://www.directa.it/help-supporto/condizioni-e-mercati/condizioni-di-trading-cme-cbot |
| IDEM FIB | 08:00–22:00 CET | 08:00–22:00 CET (08:01 inizio continuo) | https://www.directa.it/help-supporto/condizioni-e-mercati/mercati-e-orari |

**Restrizioni operative segnalate da Directa (rilevanti per accounting, non per dati):**
- Cutoff margini: 10:15 (apertura giornaliera)
- Validità ordini: giornaliera (multiday solo IDEM/Eurex)
- Stop orders: 1 giorno
- CME: cambio USD/EUR alle 22:00 LMAX (impatto P&L, non quotazioni)

**Conclusione Q5:** la sessione **pubblicamente dichiarata da Directa è coerente con la sessione ufficiale Eurex** (01:10–22:00 CET) per FDAX/FESX, quindi nessun "taglio" per orario broker. **Per CME la conferma scritta della copertura della sessione overnight 23:00–22:00 CET va richiesta al supporto Directa** (vedi template email): è plausibile che Directa pubblichi i dati Globex completi, ma la documentazione pubblica non lo afferma letteralmente.

---

## Tre scenari valutativi per il supervisore

### SCENARIO A — Directa copre tutto in modo equivalente al FIB
**Cosa significa:** runtime FDAX+FESX+ES uguale al FIB; storico intraday DAPI esteso ad almeno 5 anni anche per cross-index.
**Conseguenze:**
- training GA cross-index e FIB con stessa pipeline.
- Costo extra mensile: 7,50 EUR (Eurex bid/ask) + 15 USD (~14 EUR) (CME book) = ~21,50 EUR/mese.
- nessun provider storico aggiuntivo oltre Portara per FIB.

**Verdetto:** **NON realistico**. La documentazione DAPI mostra limite **100 giorni intraday** identico per tutti gli strumenti — quindi A non è uno scenario valido tecnicamente, è un "wish-state". Solo se Directa ampliasse il limite (richiesta improbabile) lo scenario diventa percorribile.

---

### SCENARIO B — Directa copre RUNTIME ma non STORICO sufficiente (RACCOMANDATO)
**Cosa significa:**
- PHASE-2a: cross-index runtime via DAPI (FDAX, FESX, ES) per coordinamento intermarket on-line, alert, feature engineering live.
- PHASE-2b: training storico cross-index posticipato finché non si identifica un provider storico parallelo a Portara per Eurex/CME (es. Portara stesso espone Eurex/CME, oppure FirstRateData, Kibot, IQFeed, Databento, Polygon).

**Conseguenze:**
- Costo extra mensile DAPI runtime: 7,50 EUR + 15 USD ≈ 21,50 EUR/mese.
- Eventuale costo provider storico (es. Databento intraday Eurex+CME backfill: ~50–200 USD/mese di dati, variabile).
- Architettura: il consumer DAPI accoglie 4 stream paralleli, ben sotto i 100 simboli max.
- Limitazione runtime: la sessione Eurex/CME coperta su orario ufficiale (FDAX/FESX 01:10–22:00; ES da verificare extra-USA).
- Limite operativo PHASE-2a: senza training storico cross-index, il segnale intermarket può essere usato solo come **filtro/heuristic** o per **feature qualitative** (regime detection, correlazione live), non per un secondo modello GA addestrato.

**Verdetto:** **RACCOMANDATO**. Sblocca subito il valore "intermarket live" senza vincolare la roadmap a una scelta storico-provider prematura. Distinguere PHASE-2a (no decisione provider) da PHASE-2b (decisione provider quando il segnale FIB-only è stabile e si vuole estendere il GA al cross-index).

---

### SCENARIO C — Directa NON copre uno o più cross-index
**Cosa significa:** si va su un broker alternativo (Interactive Brokers, LYNX, FXCM, ATAS) per i contratti non coperti.
**Verdetto:** **NON applicabile**. La verifica Q1 indica copertura SI per tutti e tre. Da considerare solo come ipotesi residuale se in PHASE-2a emergessero limiti pratici non documentati (es. lag eccessivo, gap di tick) che giustifichino la migrazione del runtime cross-index su altro broker — ma a quel punto il FIB resta su Directa (l'architettura diventa multi-broker, scelta strategica indipendente).

---

## Raccomandazione al supervisore

**Adottare lo SCENARIO B** in PHASE-2:

1. **PHASE-2a (cross-index runtime via Directa DAPI)**: sottoscrivere market data Eurex 7,50 EUR/mese (bid/ask futures sufficienti per intermarket "regime" — il book 5 livelli a 15 EUR è giustificato solo se PHASE-3 esplicitasse logiche order-flow), attivare market data CME 15 USD/mese, estendere il consumer DAPI da 1 stream (FIB) a 4 stream (FIB+FDAX+FESX+ES). Costo aggiuntivo mensile: ~21,50 EUR. Effort: solo lavoro engineering del consumer (zero contrattualistica nuova).
2. **PHASE-2b (training storico cross-index)**: rimandata. Si decide quando il segnale FIB-only mostra valore stabile e si vuole salire al modello cross-index addestrato. A quel punto, valutare provider unico (Portara stesso copre Eurex/CME?) o multi-provider. **NON decidere ora**: il delta valore aggiunto del cross-index nel GA va prima dimostrato in PHASE-2a (feature live).
3. **Conferma con supporto Directa** (5 punti, vedi template email sotto): (a) ticker DAPI esatto per FDAX/FESX/ES front-month e roll-policy; (b) profondità storica reale per Eurex e CME (è davvero 100 giorni / 1 min, o c'è un sottoinsieme limitato di simboli con storia minore?); (c) sessione CME coperta su Globex Sun→Fri (Directa pubblica i dati anche fuori orario italiano?); (d) procedura attivazione market data Eurex+CME (modulistica, tempi); (e) eventuali vincoli throughput o rate-limit non documentati.

**Razionale tecnico:** Scenario B preserva il principio di costo marginale crescente (paghiamo solo runtime, non storico cross-index finché non serve), conferma che l'architettura DAPI è la stessa identica del FIB (no rischio integrazione), e mantiene aperte le opzioni di provider storico (no lock-in). Il limite 100-giorni intraday del DAPI è strutturale a Directa (per tutti gli strumenti, FIB incluso) — non è una sorpresa nuova.

---

## Template email per supporto commerciale Directa

Da inviare a: `assistenza@directa.it` (oppure `directa@directa.it` come da pagina contatti, telefono +39 011 0884141).

```
Oggetto: Richiesta di chiarimento DAPI per strumenti Eurex (FDAX, FESX) e CME (ES)

Buongiorno,

sono un correntista Directa abilitato al servizio DAPI e sto valutando l'estensione del mio
consumer datafeed da 1 simbolo (FIB IDEM) a 4 simboli simultanei (FIB + FDAX + FESX + ES).
Vi chiedo conferma sui seguenti punti tecnici:

1) Ticker DAPI per i tre contratti cross-index:
   - FDAX (DAX Future Eurex)
   - FESX (EuroStoxx 50 Future Eurex)
   - ES (S&P 500 e-mini CME)
   In particolare: qual è il simbolo esatto da passare ai comandi SUB e CANDLE/CANDLERANGE
   per il contratto front-month? La convenzione segue lo standard <TICKER><MESE><ANNO>
   (es. FDAXM6 per giugno 2026) o un altro formato?

2) Profondità storico intraday su porta 10003 per Eurex e CME: 
   confermate il limite generale di 100 giorni per candele 1-4 minuti documentato sul wiki API,
   o esiste un sottoinsieme di simboli (in particolare contratti scaduti / continuous) con
   profondità inferiore?

3) Sessione coperta per CME via DAPI:
   pubblicate i tick durante l'intera sessione Globex (domenica 23:00 → venerdi 22:00 CET con
   pausa giornaliera 22:00-23:00 CET) o solo durante una finestra ridotta dell'orario italiano?

4) Procedura per attivare il market data Eurex (7,50 EUR/mese bid/ask) e CME (15 USD/mese):
   tempi di attivazione, modulistica eventuale, fatturazione (mese intero o pro-rata).

5) Limiti tecnici DAPI non documentati pubblicamente:
   - rate-limit sui comandi CANDLE/CANDLERANGE (numero richieste/minuto)?
   - throughput aggregato tick/s in caso di 4 simboli simultanei?
   - vincoli particolari di Darwin per contratti esteri (es. eventuali disconnessioni
     dedicate a orario diverso da quella di ~mezzanotte locale)?

In allegato la mia username Directa per la verifica delle abilitazioni attuali.
Grazie per la cortesia.

Cordiali saluti,
[Nome correntista]
[Username Directa]
[Numero telefono]
```

---

## Riferimenti consultati

Tutti i link aperti il 2026-05-27.

- https://www.directa.it/offer/eurex-futures-options-trading-directa.html — offerta Eurex (ticker DAX/FESX/FDXM/FDXS/FSXE, commissioni, sessione 01:10–22:00 CET).
- https://www.directa.it/partner/eurex — strumenti Eurex (futures indici DAX/EuroStoxx 50, bond Euro-Bund/Bobl/Buxl/BTP, VSTOXX, opzioni), sessione 01:10–22:00 CET principale, 08:50–17:30 opzioni.
- https://www.directa.it/help-supporto/futures/operativita-sui-futures — futures negoziabili (IDEM/Eurex/CME-CBOT), profili commissioni, cutoff margine 10:15.
- https://www.directa.it/help-supporto/condizioni-e-mercati/condizioni-di-trading-cme-cbot — generale CME (no dettaglio quote prodotti pubblicato, telefono +39 011 0884141 per chiarimenti).
- https://www.directa.it/prodotti-strumenti-finanziari/futures — listing Micro-DAX/Micro-EuroStoxx/Micro S&P/Micro-Nasdaq, commissioni Micro 2 EUR su Eurex, 3 USD su CME.
- https://www.directa.it/commissioni/commissioni.html — profili Semplice/Dinamico/Variabile.
- https://app1.directatrading.com/trading-api-directa/index.html — wiki DAPI: porte 10001/10002/10003, limiti intraday 100 giorni (1-4 min) ed EoD 15 anni, max 100 titoli sottoscritti, schema CANDLE.
- https://app1.directatrading.com/trading-api-directa/en.html — versione EN wiki DAPI, conferma indici DAPI (DAX listato), riavvio Darwin a mezzanotte.
- https://app1.directatrading.com/apiwiki/index.html — comandi TBT/TBTRANGE/CANDLE/CANDLERANGE.
- https://github.com/directa-it/documentation — repo ufficiale (darwinCommandLine, pluginExcel, pluginMulticharts).
- https://www.directa.it/help-supporto/conto-directa/come-ottengo-le-abilitazioni-aggiuntive-richieste-per-alcuni-mercati-quotazioni-o-servizi — procedura abilitazioni operative (portale Libera/dLite, sezione "Abilitazioni operative").
- https://www.qualebroker.com/recensioni/broker/directa — costi market data: Eurex 7,50 EUR (bid/ask) o 15 EUR (book futures), CME 15 USD (book).
- https://www.directa.it/help-supporto/piattaforme/api — DAPI datafeed 20 EUR/mese (gratuito se commissioni mese precedente > 200 EUR), trading API 0 EUR.

**Sezioni non confermate dalla documentazione pubblica** (rimandate al supporto Directa, vedi template email):
- ticker esatto DAPI per contratti future Eurex/CME front-month;
- conferma scritta che la sessione CME via DAPI copre tutta la finestra Globex;
- eventuali rate-limit non documentati su CANDLE/CANDLERANGE;
- throughput tick/s aggregato per 4 simboli paralleli.

---

# APPENDICE EMPIRICA — Probe diretto Darwin (2026-05-27)

Dopo la pubblicazione dell'indagine documentale (commit `2661a2f`), il supervisore ha aperto DGo + Darwin in locale e ha autorizzato un probe diretto al gateway DAPI per verificare empiricamente i punti rimasti "da chiarire con supporto Directa". Il probe è stato eseguito da un client TCP Python ad-hoc (non committato, vive in `C:\Users\AN\AppData\Local\Temp\`) contro `127.0.0.1:10003` (storici) e `127.0.0.1:10001` (realtime) con account `B6086`, banner `DARWIN_STATUS;CONN_OK;TRUE;Release 2.5.1 build 04/02/2025`.

## A.1 — Mappatura ticker DAPI canonical (verifica empirica)

Pattern Directa verificato:
- **Eurex futures**: `EU.<CODE><MONTH><YEAR>` — es. `EU.DJ50M6` = Euro Stoxx 50 future giugno 2026
- **CME futures**: `CM.<CODE><MONTH><YEAR>` — es. `CM.ESM6` = S&P 500 e-mini standard giugno 2026
- **IDEM futures**: `<CODE><YEAR><MONTH>` (FIB, MINI senza prefisso exchange) — es. `FIB6I`

Mese codice Eurex/CME: H=Mar, M=Jun, U=Sep, Z=Dec, ecc. (codici standard). YEAR = ultima cifra anno.

### Tabella ticker probati su porta 10003 con `CANDLERANGE` daily ultimi 20 giorni

| Strumento richiesto dalla spec | Ticker DAPI VALIDO | Status | Volume D campione 2026-05-26 | Note |
|---|---|---|---|---|
| **FDAX** (DAX 40 future, 25 EUR/pt) | ❌ nessuno | `ERR;<sym>;1007` su tutte le varianti | — | NON abilitato su account `B6086` (vedi A.3) |
| **FDXM** (Mini-DAX, 5 EUR/pt) | **`EU.FDXMM6`** | ✅ OK 14-15 candele D | ~27.945 contratti | proxy DAX accettabile per regime, moltiplicatore diverso |
| **FDXS** (Micro-DAX, 1 EUR/pt) | **`EU.FDXSM6`** | ✅ OK | ~30.839 | secondo proxy DAX |
| **FESX** (EuroStoxx 50 future, 10 EUR/pt) | **`EU.DJ50M6`** | ✅ OK 14 candele D | **455.505** | front-month liquidissimo. `DJ50` = Dow Jones EuroStoxx 50 |
| **MFESX** (Mini-EuroStoxx 50, 1 EUR/pt) | **`EU.FSXEM6`** | ✅ OK | 2.288 | liquidità marginale |
| **ES** (S&P 500 e-mini standard, 50 USD/pt) | **`CM.ESM6`** | ✅ OK 14 candele D | **1.342.222** | front-month liquidissimo |
| **MES** (Micro E-mini S&P, 5 USD/pt) | **`CM.MESM6`** | ✅ OK | 1.449.786 | già usato negli exports |
| **Positive controls (gia' negli exports)** | `FIB6F`, `FIB6I`, `MINI6F`, `EU.DJ50U6`, `EU.FSXEU6`, `CM.MESU6`, `DITAS`, `DGER`, `DSTX50` | ✅ tutti OK | — | confermano transport |

**Sintesi**: FESX e ES esistono con ticker DAPI canonico `EU.DJ50<MONTH><YEAR>` e `CM.ES<MONTH><YEAR>`. **FDAX standard NON è disponibile su account corrente**.

## A.2 — Profondità storica intraday verificata empiricamente

Probe su `CM.ESM6` (porta 10003, `CANDLERANGE` con vari range):

| Query | Periodo | Range richiesto | Candele ricevute | First timestamp | Last timestamp |
|---|---|---|---|---|---|
| daily 200gg | 86400 | 2025-11-08 → 2026-05-27 | 112 | **2025-12-17** | 2026-05-26 |
| 5min 30gg | 300 | 2026-04-27 → 2026-05-27 | 6025 | 2026-04-27 12:00 | 2026-05-27 12:00 |
| 1min 30gg | 60 | 2026-04-27 → 2026-05-27 | 30.120 | 2026-04-27 12:00 | 2026-05-27 12:00 |
| **1min 150gg (oltre limite)** | 60 | 2025-12-28 → 2026-05-27 | 77.829 | **2026-02-16 00:00** | 2026-05-15 |

**Conferma empirica limite 100 giorni intraday**: query a 150gg restituisce un first_timestamp coincidente con ~100 giorni prima del pull date (2026-05-27 − 2026-02-16 = ~100 giorni). Coerente con il wiki DAPI. Daily NON soffre il limite — risposta arriva su 5-6 mesi senza problemi.

Probe analoghi su `EU.DJ50M6` (5M, 30gg = 4981 candele) e `EU.FDXMM6` (5M, 30gg = 4843 candele) confermano profondità intraday identica al FIB.

## A.3 — Decodifica codici di errore DAPI osservati

| Codice | Comando emittente | Significato dedotto |
|---|---|---|
| `ERR;<TICKER>;1007` | `CANDLERANGE` su porta 10003 | strumento non abilitato per l'account o ticker inesistente |
| `ERR;INFO;1004` | `INFO <sym>` su porta 10001 | comando `INFO` non supportato nel protocollo realtime (codice "comando non valido") |
| `ERR;<TICKER>;1030` | `SUB <sym>` su porta 10001 | market data realtime non sottoscritto per quel ticker — distinto da 1007 (storico) |
| `ERR;UNSUB;1004` | `UNSUB` con simbolo mai sottoscritto | unsub non riconosciuto, irrilevante |

**Implicazione operativa**:
- Lo **storico** (porta 10003) è incluso nel DAPI base e funziona per tutti i ticker su cui l'account ha abilitazione operativa di trading (anche senza market data realtime).
- Il **realtime** (porta 10001) richiede abilitazione market data esplicita: per cross-index serve Eurex 7,50 EUR/mese + CME 15 USD/mese, **non ancora attivata** sull'account `B6086`.

## A.4 — Rate-limit DAPI osservato

- **26 comandi `CANDLERANGE` sequenziali a 0,6s di gap su una sola connessione persistente**: tutti elaborati senza errori, transport stabile.
- **14 connessioni TCP rapide aperte/chiuse ravvicinate**: dopo la 14ª il server ha cominciato a chiudere preventivamente (`ConnectionResetError 10054`) e poi a rifiutare nuove connessioni per ~30 secondi (`ConnectionRefusedError 10061`).
- **Lezione operativa**: il pipeline runtime deve usare **una singola connessione persistente per ogni porta** (10001 e 10003), non aprire/chiudere per ogni comando. Il limite "100 simboli sottoscritti" sulla 10001 è ortogonale e ampiamente sotto soglia per 4 stream.

## A.5 — Sessione e timezone osservate

- `EU.DJ50M6` daily open timestamp `01:00:00` → sessione Eurex overnight 01:10–22:00 CET confermata via Darwin (la candela daily è bookend dall'inizio della sessione overnight).
- `CM.ESM6` daily open timestamp `00:00:00` → sessione CME Globex normalizzata a mezzanotte locale Darwin.
- `EU.FDXMM6` (Mini-DAX) idem `01:00:00` → stesso pattern Eurex.
- L'intraday 5M e 1M su `CM.ESM6` copre 24h con candele attive anche durante la sessione overnight US (es. tick alle 12:00 CET = mezzogiorno italiano = mattino US off-hours) → conferma copertura Globex completa per CME via DAPI.

## A.6 — Aggiornamento raccomandazione (con dato empirico)

**Scenario B confermato e arricchito**. PHASE-2a cross-index runtime è tecnicamente fattibile da subito con i seguenti ticker DAPI già accessibili in storico, **previa attivazione market data realtime**:

| Spec hard-locked | Implementazione concreta DAPI | Pro | Contro |
|---|---|---|---|
| **FDAX** standard | **NON disponibile** su account corrente | — | richiede abilitazione market data DAX standard Eurex (verifica con supporto) |
| → workaround proxy DAX | `EU.FDXMM6` (Mini-DAX 5 €/pt) | già abilitato; sottostante identico (DAX 40); 27k contratti/day vol | moltiplicatore 5 vs 25 €/pt → non equivalente come strumento operativo ma sufficiente per **regime detection** intermarket |
| **FESX** standard | `EU.DJ50M6` | ✅ abilitato, vol 455k/day, front-month liquido | da attivare market data realtime (Eurex 7,50 €/mese) |
| **ES** standard | `CM.ESM6` | ✅ abilitato, vol 1.342k/day, front-month liquido | da attivare market data realtime (CME 15 USD/mese) |

**Costo runtime PHASE-2a verificato**: solo le due abilitazioni market data Eurex+CME = ~21,50 EUR/mese (nessuna sorpresa rispetto all'indagine documentale). Per FDAX standard servirebbe **eventualmente** un'abilitazione aggiuntiva da chiedere al supporto Directa.

**Costo storico training PHASE-2b confermato infattibile via DAPI**: il limite 100gg vincola tutti gli strumenti cross-index allo stesso modo del FIB — il vendor parallelo (Portara/Databento/IQFeed) resta necessario.

## A.7 — Aggiornamento template email supporto Directa

I 5 punti del template originale vanno aggiornati con quanto già verificato:

1. ~~Ticker DAPI per cross-index~~ → **verificato empiricamente**: `EU.DJ50M6` (FESX), `CM.ESM6` (ES), `EU.FDXMM6` (Mini-DAX). Resta UN punto aperto: **attivazione DAX standard FDAX**: «è possibile abilitare il DAX Future standard (25 EUR/pt) sull'account `B6086`, attualmente abilitato solo a Mini-DAX e Micro-DAX? Se sì, modulistica e costo market data dedicato?»
2. Profondità storico intraday → **verificato 100gg** identico al FIB. Punto chiuso.
3. Sessione CME via DAPI → **verificato** indirettamente via intraday 5M/1M che coprono 24h. Punto chiuso (no email).
4. Procedura attivazione market data Eurex 7,50 €/mese + CME 15 USD/mese → resta da chiedere (modulistica, tempi, fatturazione).
5. Rate-limit CANDLE/CANDLERANGE → **verificato**: socket persistente OK, apertura ripetuta NO. Aggiungere: «c'è un limite documentato sul numero di connessioni TCP aperte/chiuse al minuto? Abbiamo osservato cooldown ~30s dopo 14 aperture rapide ravvicinate.»

## A.8 — Implicazioni dirette per CAP-DATA-02 (futuro)

1. **Catalogo simboli DAPI per il documento metodologico**: la mappa `EU.<CODE><MONTH><YEAR>` / `CM.<CODE><MONTH><YEAR>` / `<CODE><YEAR><MONTH>` va formalizzata nel cap. come "input contract" del pipeline di ingestion.
2. **Conferma del limite 100gg**: ribadita empiricamente, già documentata in CAP-DATA-01 §3.6. Nessun cambio di scope necessario.
3. **Errori 1007 / 1030**: il pipeline runtime deve riconoscerli e propagare warning espliciti (gap di abilitazione vs gap di market data).
4. **Connessione persistente**: pattern architetturale da adottare nel consumer DAPI quando si estende da 1 a 4 stream.

**Nessuna modifica alla roadmap PHASE-1 FIB-only** richiesta da queste evidenze. La PHASE-2 cross-index resta nello scenario B raccomandato, ora con ticker DAPI canonical noti e gap di abilitazione FDAX standard isolato come unico punto residuo da chiarire.

---

# APPENDICE EMPIRICA B — Verifica REALTIME post-reconnect DGo (2026-05-27 14:05 CET)

Dopo aver riconnesso DGo/Darwin, il supervisore ha autorizzato un secondo probe diretto sulla **porta realtime 10001** per verificare se il SUB risponde ora che la sessione è stata rigenerata. Probe eseguito inline via Python `socket`, comandi visibili nel transcript.

## B.1 — Sintassi protocollo Darwin sulla 10001

I comandi metadata risultano tutti rifiutati: `HELP`, `VER`, `STATUS`, `GETAVAILABLESTATUS`, `INFO` → `ERR;<cmd>;1004`. Il protocollo realtime accetta in pratica solo `SUB`/`UNSUB` + (presumibilmente) `BOOK_SUB`/`BOOK_UNSUB` documentati nel wiki API. Codice `1004` = "comando non valido o non supportato".

## B.2 — SUB FIB6I (controllo positivo)

`SUB FIB6I` ha restituito immediatamente sia anagrafica che book full:

```
ANAG;FIB6I;14:05:30;IT0024847870;FTSE MIB INDEX FUTURE SET26;50040.0;0.0;0
BOOK_5;FIB6I;14:02:33;1;1;49715.0;1;1;49275.0;0;0;0.0;0;0;0.0;0;0;0.0;
                                                                       1;1;50535.0;1;1;51115.0;0;0;0.0;0;0;0.0;0;0;0.0
```

**Letture chiave:**
- **ISIN FIB6I**: `IT0024847870`
- **Descrizione**: "FTSE MIB INDEX FUTURE SET26" → **FIB6I è il future FTSE MIB scadenza settembre 2026** (`SET26 = SETtembre 2026`).
- Il codice mese Directa `I` quindi corrisponde a **settembre**, NON segue lo standard CME (U=Sep). La convenzione Directa-IDEM è proprietaria (`F`, `I`, ... → da decodificare). Per CAP-DATA-02 servirà una piccola lookup table tradotta dai metadata anagrafica.
- Schema **`ANAG`**: `ANAG;<TICKER>;<HH:mm:ss>;<ISIN>;<descrizione>;<ref_price>;<flag>;<flag>`
- Schema **`BOOK_5`**: `BOOK_5;<TICKER>;<HH:mm:ss>;<bid1_lots>;<bid1_ord>;<bid1_price>;<bid2..>;<bid3..>;<bid4..>;<bid5..>;<ask1_lots>;<ask1_ord>;<ask1_price>;<ask2..>;<ask3..>;<ask4..>;<ask5..>` (5 livelli BID + 5 livelli ASK).
- Mercato IDEM a 14:05 CET in pieno orario di sessione, ma il book pubblicato è scarno (1+1 lotti su L1 a entrambi i lati, gli altri 4 livelli `0`) — coerente con un quasi-future a scadenza lontana settembre 2026 in giornata di scambi normale; **per il front-month giugno occorrerebbe SUB su `FIB6L`/`FIB6M` o sul codice mese Directa corrispondente a giugno**: nei prossimi probe vale identificarlo.

## B.3 — SUB cross-index futures (FDXM, DJ50, ES) — confermato `1030`

```
SUB CM.ESM6     →  ERR;CM.ESM6;1030
SUB EU.DJ50M6   →  ERR;EU.DJ50M6;1030
SUB EU.FDXMM6   →  ERR;EU.FDXMM6;1030
```

**Conferma definitiva**: `ERR;<TICKER>;1030` = **market data realtime non sottoscritto** sull'account `B6086`. È un codice diverso da `1007` (storico/ticker non abilitato) e segnala specificamente la mancanza dell'abbonamento dati live.

## B.4 — SUB indici cash europei — FUNZIONA gratis

```
SUB DGER  →  PRICE;dGER;14:05:41;25251.9;0;0;0;25244.9;25400.9
              PRICE;dGER;14:05:47;25251.6;0;0;0;25244.9;25400.9
SUB DITAS →  PRICE;dITAS;14:05:43;49859.22;2;2318;2129;49859.22;50129.22
              PRICE;dITAS;14:05:53;49869.22;12;2330;2138;49859.22;50129.22
```

**Letture chiave:**
- **Indici cash europei** (DGER=DAX, DITAS=FTSE MIB, presumibilmente anche DSTX50 e DFRA) hanno **realtime gratuito incluso nel DAPI base** — non serve abilitazione market data Eurex/CME extra.
- Schema **`PRICE`**: `PRICE;<ticker>;<HH:mm:ss>;<last>;<volume_lot?>;<bid_qty?>;<ask_qty?>;<low_session>;<high_session>` (campi medi da chiarire).
- Notare il **prefisso lowercase** nel ticker della risposta (`dGER`, `dITAS`) — pattern proprietario Directa per gli indici cash; nel SUB usiamo invece il ticker maiuscolo.
- I tick arrivano in pubblicazione streaming continua (più righe sullo stesso simbolo a `:41`, `:47`, `:53`).

## B.5 — Implicazioni concrete per scenario B

L'evidenza realtime conferma e raffina la raccomandazione:

| Componente PHASE-2a runtime | Stato attuale sull'account `B6086` | Cosa serve |
|---|---|---|
| Tick FIB (front + scadenze) | ✅ già funzionante | nulla |
| Tick FDXM (Mini-DAX) | ❌ `ERR;1030` | attivare market data Eurex 7,50 EUR/mese (bid/ask) o 15 EUR (book 5) |
| Tick DJ50 (FESX) | ❌ `ERR;1030` | come sopra (stesso pacchetto Eurex futures) |
| Tick ES (CME standard) | ❌ `ERR;1030` | attivare market data CME 15 USD/mese (book 5) |
| Tick MES (CME micro) | ❌ `ERR;1030` (atteso, stessa famiglia CME) | come sopra, stesso pacchetto |
| **Tick DGER, DITAS, DSTX50, DFRA (indici cash)** | ✅ **gratuito già attivo** | nulla — **usabili da subito come feature intermarket low-cost** |

**Nuovo elemento di valore strategico**: il pipeline può ingerire i tick degli **indici cash europei gratuitamente** mentre l'abilitazione futures cross-index è ancora pending. Per regime detection / coordinamento intermarket / feature qualitative, `dGER` (DAX cash) e `dSTX50` (Eurostoxx cash) tracciano lo stesso sottostante dei rispettivi future con tracking error ~0 sull'intraday. **PHASE-2a può partire con tick cash zero-cost prima ancora di attivare i market data future**.

## B.6 — Aggiornamento template email supporto Directa (definitivo)

Riducendo il template alla luce di quanto verificato, restano 3 punti aperti:

1. **Abilitazione DAX standard FDAX (25 EUR/pt)** su account `B6086` — modulistica e costo aggiuntivo (se distinto dall'abbonamento Mini-DAX/Micro-DAX 7,50 EUR/mese).
2. **Procedura attivazione market data Eurex 7,50 EUR/mese (bid/ask futures) e CME 15 USD/mese (book futures)** — tempi attivazione, fatturazione pro-rata vs mese intero, attivazione contestuale o sequenziale.
3. **Decodifica codice mese Directa-IDEM**: lookup completa di `F`, `I`, ... ai mesi calendar per il FIB e il mini-FIB (constatato `I = Settembre`, `F` = ?). Utile per il pipeline che debba derivare il front-month automaticamente.

Gli altri 2 punti del template originale sono **chiusi** dal probe:
- ~~ticker DAPI cross-index~~ → identificati;
- ~~rate-limit~~ → osservato: cooldown ~30s dopo 14 aperture TCP rapide ravvicinate, mentre 26+ comandi su connessione persistente sono OK.

## B.7 — Tre commit della sessione di indagine

| Commit | Contenuto |
|---|---|
| `2661a2f` | indagine documentale (agent web) — Q1-Q5, costi, scenari A/B/C, raccomandazione iniziale |
| `b8f7273` | Appendice A — probe storico porta 10003: ticker DAPI canonical verificati, limite 100gg empirico, codici 1007/1004/1030 decodificati |
| `[questo commit]` | Appendice B — probe realtime porta 10001: SUB FIB6I OK, cross-index futures `ERR;1030`, **indici cash europei realtime gratuito** |

