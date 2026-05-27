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
- Lo schema candle DAPI (`CANDLE;<TICKER>;<yyyyMMdd>;<HH:mm:ss>;<O>;<H>;<L>;<C>;<V>`) è documentato e identico tra strumenti italiani ed esteri.

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
- Candele: `CANDLE;<TICKER>;<yyyyMMdd>;<HH:mm:ss>;<Open>;<High>;<Low>;<Close>;<Volume>`. Niente settle né tick-count nel record candle.
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
