# ACTIVE TASK — CAP-DATA-02 (Parte 9)

**Titolo:** Pipeline runtime FIB su Directa DAPI
**Status:** ACTIVE
**Posizione nel doc v2:** Parte 9, immediatamente prima di eventuali Parti
successive e dell'Appendice
**Predecessor:** Parte 8 (CAP-DATA-01) — PASS Review
**Owner deliverable:** Developer subagente
**Supervisore:** AC

## Goal
Formalizzare in metodologia v2 il canale Directa DAPI come provider RUNTIME
esclusivo del FIB, definendo simboli, format, gestione errori, sessione operativa,
vincoli di concorrenza e mappatura schema verso il bundle frozen di training
Portara, con risoluzione vincolante della Q-A sul gating cash europei.

## Scope IN
1. Formalizzazione canale DAPI come provider RUNTIME del FIB (Portara resta per
   training, eredita' da CAP-DATA-01).
2. Catalogo simboli Directa rilevanti per CAP-DATA-02:
   - IDEM FIB (FIB6F, FIB6I, MINI6F, MINI6I, MINI6C)
   - indici cash europei (DITAS, DGER, DSTX50, DFRA)
3. Architettura canale: gateway 127.0.0.1, porte 10001 (RT) e 10003 (storico),
   banner Darwin, file APIPortSettings.txt, socket persistente, rate-limit.
4. Format dati canonico (CSV BOM UTF-8 + manifest JSON, riferimento allo script
   esistente scripts/export_directa_history_parametric.py).
5. Codici errore DAPI (1004 / 1007 / 1030) e fallback aggregazione
   (AGG_FROM_60s, AGG_FROM_D).
6. Vincolo "uso esclusivo del canale" (conflitto con DGo/TradingView Directa).
7. Sessione operativa runtime FIB 08:00-22:00 CET, coerente con timeline
   epoche di CAP-DATA-01 §3.5.
8. Tabella di mappatura schema DAPI -> bundle frozen Portara (invariante
   research = runtime applicato all'adapter).
9. Warm-up degli stati condizionali (EGARCH/quantili) all'avvio sessione.
10. Audit log dei comandi inviati e risposte ricevute con policy di retention.
11. Decisione Q-A risolta nel capitolo (vedi sezione "Decisioni ratificate").

## Scope OUT (esplicito)
- Training storico cross-index intraday pluriennale (FUORI: rinviato a futuro)
- Attivazione market data Eurex/CME a pagamento (FUORI: D-1)
- Modifica spec hard-locked CAP-DATA-01 (FUORI)
- Apertura PHASE-2 cross-index (FUORI: futura)
- Trading / esecuzione ordini, porta 10002 (FUORI: il sistema non esegue)
- Implementazione codice operativo: il capitolo è metodologia, non codice (FUORI)
- Feature engineering / scelta delle feature: già coperto da Parti III/V (FUORI)
- Persistenza dei dati DAPI runtime per uso futuro come dataset di re-training
- Continuità del tape, recupero automatico gap entro 100gg CANDLERANGE,
  riconciliazione canonica giornaliera e storicizzazione strutturata: trattati
  nel capitolo successivo (CAP-DATA-03 / Parte 10), FUORI da CAP-DATA-02

## Decisioni ratificate (NON riaprire)

### Q-A — Cash europei come gating regime
**Ratificata Q-A-3:** i cash europei (DGER, DSTX50, DITAS, DFRA) entrano
ESCLUSIVAMENTE come:
- logging operativo
- gating qualitativo a basso costo per il supervisore umano (regole esplicite,
  auditable, configurabili fuori dal GA)
Perimetro vincolante da scrivere nel capitolo:
- NON entrano nel feature tensor che alimenta il GA
- NON entrano nella state machine del segnale (no condizioni "if DGER drop>X
  then blocca segnale")
- l'eventuale regola di gating qualitativo vive in config/gating_rules.yaml
  (o equivalente), versionata, modificabile senza re-training

### Altre decisioni vincolanti
- D-1: niente market data a pagamento
- D-6: uso esclusivo canale, no DGo/TradingView concorrente
- C-1: naming β2 (CAP_09_parte_9.md, REPORT_CAP_09.md, "Parte 9" arabo)
- C-2: push diretto origin/main
- C-3: aggiornamento 00_indice.md a fine ciclo

## Sei gap obbligatori da chiudere nel capitolo (C-7)
1. **Gap-1 Autenticazione canale**: dichiarare che la pipeline runtime gira
   sulla stessa macchina dell'account abilitato (Darwin locale, no remote access).
   APIPortSettings.txt nel filesystem utente è identificatore, non credenziale.
2. **Gap-2 Policy timezone**: dichiarare se i timestamp Darwin sono trattati
   come CET locale (con conversione CEST automatica) o come UTC convertito
   dal client. Coerente con timeline epoche CAP-DATA-01 §3.5.
3. **Gap-3 Riavvio Darwin mezzanotte**: specifica comportamento pipeline a
   restart (riconnessione automatica + marker RUNTIME_GAP nel log).
4. **Gap-4 Audit log retention**: tutti i comandi inviati + risposte ricevute
   loggati con timestamp UTC. Retention minima 90gg rolling per debug,
   retention permanente per giorni di emissione segnale (compliance interna).
5. **Gap-5 Test regressione exports**: dichiarare che la pipeline runtime
   eseguita oggi su simboli con storico ≤100gg deve produrre output identico
   a quello già archiviato in C:\directa_history_parametric_export_overlay\exports
   (a meno di righe nuove). Sanity check di non-regressione.
6. **Gap-6 Soglia commissioni**: comportamento se commissioni mensili
   scendono sotto 200 EUR (DAPI base diventa 20 EUR/mese). Pipeline
   tollera l'addebito automatico, alert al supervisore.

## Done criteria (verificabili)
1. File docs/methodology_v2/CAP_09_parte_9.md prodotto, 8-10 pp (stima),
   struttura coerente con la scaletta in calce (12 sezioni)
2. File reports/REPORT_CAP_09.md prodotto secondo template supervisore
3. Tutti gli input autoritativi della sezione INPUT verbatim nel capitolo
   (banner Darwin "Release 2.5.1", comandi CANDLERANGE/SUB/UNSUB, schemi
   CANDLE/ANAG/BOOK_5/PRICE, codici errore 1004/1007/1030, limite 100gg,
   rate-limit ~14 connessioni / cooldown 30s, conflitto DGo)
4. Tabella mappatura schema DAPI -> bundle frozen Portara completa per
   TUTTI i campi del bundle: bar_open, bar_high, bar_low, bar_close,
   volume, tick_count, bar_synthetic, eventuali altri presenti in CAP-DATA-01
5. Decisione Q-A chiusa nel testo con verdetto + motivazione + perimetro
   operativo (Q-A-3 ratificata, vedi sopra)
6. Tutti i 6 Gap (Gap-1..Gap-6) chiusi nel capitolo
7. Tabella decisioni del capitolo (ID, descrizione, motivazione 1 riga) presente
8. Sezione "Punti aperti fuori scope" con almeno: abilitazione FDAX standard,
   lookup completa codici mese IDEM (oltre I=settembre), vendor cross-index
   pluriennale, continuita'/storicizzazione (rinvio a CAP-DATA-03)
9. 00_indice.md aggiornato a fine ciclo (Parte 9 = PASS con hash review)
10. Nessuna modifica a Parti I-VIII del doc v2

## Scaletta deliverable Developer (12 sezioni)
Convenzione storica: il primo capitolo della Parte VIII era CapXX (verifica
ultimo capitolo Parte VIII in 00_indice.md). Parte 9 parte dal capitolo
successivo.

1. Premessa e collocazione (cosa formalizza, relazione con CAP-DATA-01,
   invariante research = runtime applicato all'adapter)
2. Architettura del canale DAPI (gateway, porte 10001/10003 NON 10002,
   banner, file APIPortSettings, vincolo uso esclusivo, pattern socket
   persistente, rate-limit)
3. Catalogo simboli FIB e cash europei (tabella IDEM FIB6x/MINI6x + cash
   DITAS/DGER/DSTX50/DFRA, schemi PRICE/BOOK_5/ANAG, codice mese IDEM
   noto I=settembre, meccanismo derivazione front-month da ANAG)
4. Format dati canonico runtime (CSV header BOM UTF-8, manifest JSON,
   source ∈ {DIRECTA, AGG_FROM_D, AGG_FROM_60s}, ruolo script
   export_directa_history_parametric.py come riferimento implementativo)
5. Mappatura schema DAPI -> bundle frozen Portara (tabella canonica;
   regola bar_synthetic=True anche in runtime quando un minuto non ha
   trade, coerente con CAP-DATA-01 §3.4 e Parte VII gap semantics)
6. Gestione errori, recovery, riavvio Darwin (decodifica 1004/1007/1030,
   backoff, comportamento al riavvio mezzanotte, fallback aggregazione,
   stato RUNTIME_DEGRADED se DGo entra in conflitto)
7. Warm-up degli stati condizionali all'avvio sessione (lookback DAPI
   ≤100gg sufficiente per warm-up tipico EGARCH; fallback Portara per
   restart dopo downtime >100gg)
8. Sessione operativa runtime FIB 08:00-22:00 CET (calendario, timezone,
   allineamento alla timeline epoche FIB di CAP-DATA-01 §3.5)
9. Decisione Q-A: gating cash europei (verdetto Q-A-3, motivazione,
   regola operativa, perimetro vincolante)
10. Audit log e retention (cosa logga, formato, retention minima)
11. Punti aperti fuori scope (FDAX standard, lookup mese IDEM, vendor
    cross-index pluriennale, rinvio CAP-DATA-03)
12. Tabella decisioni del capitolo

## Rollback criteria
- Decisione Q-A-3 reversibile in capitolo successivo se l'esperienza
  operativa mostra che il logging cash è inutile o dannoso
- Tabella ticker DAPI non reversibile (fattuale, verificato empiricamente
  2026-05-27)
- Adapter bar_synthetic non reversibile (invariante semantico ereditato
  da CAP-DATA-01 §3.4)
- Vincolo uso esclusivo canale (D-6) non reversibile

---

## (i) Mappatura eredita' Parti I-VIII -> sezioni della scaletta

Riferimenti incrociati obbligatori per il Developer. Ogni sezione della
scaletta deve citare ESATTAMENTE i capitoli sotto elencati come ancore
nell'eredita' del documento metodologico v2. Verifica eseguita su
`docs/methodology_v2/00_indice.md` (Parti I-VIII complete, tutte PASS).
Per "Parte 8 / CAP-DATA-01" si intendono i Cap.37-44 secondo l'indice
corrente; per "Parte VIII §3.x" del task card originale si intende il
contenuto interno dei singoli capitoli della Parte 8.

| Sez. | Tema sezione | Eredita' obbligatorie (Parte / Cap. / sub-rif.) |
|------|--------------|--------------------------------------------------|
| §1 | Premessa, collocazione, invariante research = runtime | Parte I Cap.1 (definizione strumento + sessione operativa) · Parte I Cap.3 (infrastruttura disponibile: Directa, Portara/CQG, Telegram) · Parte II Cap.10 (replay e riproducibilita' del lifecycle, determinismo bit-exact) · Parte 8 Cap.37 (FIB pieno back-adjusted Portara/CQG come fonte ufficiale training; razionale `research = runtime`) · Parte 8 Cap.44 (esclusione esplicita di fonti alternative, vincolo invariante) |
| §2 | Architettura canale DAPI (gateway, porte 10001/10003, banner, APIPortSettings, uso esclusivo, socket persistente, rate-limit) | Parte I Cap.3 (broker Directa, canale Telegram, lacune API rinviate ad Appendice C) · Appendice C (API Directa: qualificazione Darwin / DAPI / Visual Trader — citazione di riferimento del task in cui Appendice C sara' completata in coda al doc v2) |
| §3 | Catalogo simboli FIB e cash europei (IDEM FIB6x/MINI6x + cash DITAS/DGER/DSTX50/DFRA, schemi PRICE/BOOK_5/ANAG) | Parte I Cap.1 (strumento FIB su mercato IDEM, sessione 08:00-22:00 CET) · Parte I Cap.2 (operativita' 1 contratto, separazione MINI/standard) · Parte 8 Cap.37 (esclusione MIB cash dalla serie ufficiale di training, da NON confondere con DITAS runtime gating) · Parte 8 Cap.42 (convenzione cross-index PHASE-2 come perimetro normativo per cash europei) |
| §4 | Format dati canonico runtime (CSV BOM UTF-8, manifest JSON, source ∈ {DIRECTA, AGG_FROM_D, AGG_FROM_60s}) | Parte 8 Cap.38 (convenzione back-adjustment ufficiale: ratio-adjusted + Panama-additive + unadjusted; format normativo del training) · Parte 8 Cap.40 (preprocessor griglia 1-min regolare, flag `bar_synthetic` persistito nel bundle frozen) · Parte 8 Cap.43 (procedura di sanity validation: metriche di confronto su finestre 18-24 mesi) |
| §5 | Mappatura schema DAPI -> bundle frozen Portara (tabella canonica + regola `bar_synthetic=True` in runtime quando il minuto non ha trade) | Parte 8 Cap.40 (definizione operativa `bar_synthetic`, forward-fill su Close, volume=0, uso differenziato a valle: volatilita' su barre reali, prezzo su griglia completa) · Parte 8 Cap.43 (sanity validation come strumento di verifica della coerenza schema) · Parte VII Cap.31 (procedura di validazione OOS — gap semantics implicita nel test su finestre OOS, citazione testuale dell'invariante `bar_synthetic`) |
| §6 | Gestione errori, recovery, riavvio Darwin (decodifica 1004/1007/1030, backoff, fallback aggregazione, stato RUNTIME_DEGRADED) | Parte 8 Cap.40 (semantica gap di sessione e barre sintetiche; comportamento del preprocessor a valle di dati mancanti) · Parte VII Cap.31 (replay deterministico bit-exact: il riavvio Darwin non deve violare il determinismo) · Parte II Cap.10 (formato log e determinismo per il replay) · Parte VI Cap.27 (pipeline di inference real-time: collocazione del recovery dentro il ciclo operativo) |
| §7 | Warm-up stati condizionali all'avvio sessione (lookback DAPI ≤100gg per EGARCH; fallback Portara per restart dopo downtime >100gg) | Parte III Cap.13 (EGARCH(1,1) single-instrument: equazioni media e varianza, inizializzazione cross-session — osservazione coda bassa N-5) · Parte III Cap.14 (stato di regime intraday, persistenza minima $T_{persist}=10$ barre, quantile $p=0{,}75$ su $N_{reg}=20$ sessioni) · Parte III Cap.15 (EMA reset cross-session, $T_{warmup,\text{EMA}}=74$ barre; normalizzazione z-score MAD con $W_{norm}=1000$ e $T_{warmup,\text{norm}}=100$) · Parte V Cap.25 (walk-forward fold-per-fold del rolling EGARCH $W=210.000$ barre, decisione Q-06/C-4.1) · Parte VI Cap.27 (pipeline di inference real-time: punto di chiamata del warm-up all'avvio sessione) |
| §8 | Sessione operativa runtime FIB 08:00-22:00 CET (calendario, timezone, allineamento epoche) | Parte I Cap.1 (sessione operativa 08:00-22:00 CET, Q-01 chiusa) · Parte II Cap.7 (state machine del segnale: timer pre-trigger $T_{touch}^{max}$ e post-trigger $\Delta t_{cromosoma}$ entro la finestra di sessione) · Parte 8 Cap.41 (timeline ufficiale delle sessioni FIB E1-E5 1994-2026, file `data/sessions/fib_session_calendar.csv` a 6 campi, conversione CET/CEST normativa) |
| §9 | Decisione Q-A: gating cash europei (verdetto Q-A-3, motivazione, regola operativa, perimetro vincolante) | Parte I Cap.5 (definizione operativa del successo, metrica primaria expected net return — il gating qualitativo NON ne modifica la fitness GA) · Parte III Cap.15 (catalogo 37 feature: il cash europeo NON entra nel feature tensor) · Parte V Cap.22 (cromosoma e spazio dei parametri: il gating qualitativo vive in `config/gating_rules.yaml` fuori dal genoma del bundle) · Parte 8 Cap.42 (convenzione cross-index PHASE-2: DITAS/DGER/DSTX50/DFRA NON sono cross-index PHASE-2, sono cash logging/gating qualitativo) |
| §10 | Audit log e retention (cosa logga, formato, retention minima 90gg / permanente sui giorni di emissione) | Parte II Cap.10 (formato dei log di emissione, transizioni, chiusura; determinismo bit-exact dichiarato come vincolo formale) · Parte VI Cap.30 (monitoraggio del lifecycle in produzione, metriche live, alert su deriva: il log DAPI alimenta la dashboard di Cap.30) · Parte VII Cap.35 (frozen bundle e immutabilita': l'audit log e' parte del corredo di evidenza del bundle in produzione) |
| §11 | Punti aperti fuori scope (FDAX standard, lookup codici mese IDEM, vendor cross-index pluriennale, rinvio CAP-DATA-03) | Parte 8 Cap.42 (convenzione cross-index PHASE-2 — vendor DAX/ESTX50/ES Portara/CQG come perimetro futuro) · Parte 8 Cap.44 (esclusione esplicita di fonti alternative — qualunque vendor diverso da Portara/CQG senza nuovo task Planner) · CAP-DATA-03 / Parte 10 futura (continuita' tape, recupero gap, riconciliazione canonica giornaliera, storicizzazione strutturata) |
| §12 | Tabella decisioni del capitolo (ID, descrizione, motivazione 1 riga) | nessuna eredita' diretta: e' la sintesi normativa interna al capitolo, allineata in stile alla tabella decisioni di Parte 8 Cap.37-44 e di Parte VII Cap.36 (gate decisionali) |

Note operative:
- Il Developer e' tenuto a citare i capitoli esattamente con la notazione
  in tabella (es. "Parte 8 Cap.40" o "Parte III Cap.13"). Il documento NON
  duplica contenuti gia' normati: rinvia con riferimento puntuale.
- Per "Appendice C" si intende il segnaposto presente nell'indice ufficiale
  della Parte Appendici operative; quando il task corrente formalizza il
  canale DAPI, l'Appendice C verra' aggiornata in una fase successiva di
  consolidamento delle Appendici (NON in CAP-DATA-02).

---

## (ii) Numerazione capitoli interni del documento metodologico v2

L'ultimo capitolo della Parte 8 (CAP-DATA-01) e' il **Cap.44** ("Esclusione
esplicita di fonti alternative"). La Parte 9 (CAP-DATA-02) parte quindi
dal **Cap.45** e copre 12 capitoli consecutivi fino al **Cap.56** incluso.

Stima dimensionale complessiva del capitolo: **8-10 pagine A4** (consulenza
metodologica esterna ratificata).

| Cap. | Sezione scaletta | Lunghezza attesa | Densita' |
|------|-------------------|--------------------|----------|
| Cap.45 | §1 Premessa e collocazione (research = runtime, relazione con CAP-DATA-01) | ~0,5 pp | bassa |
| Cap.46 | §2 Architettura canale DAPI (gateway, porte, banner, APIPortSettings, uso esclusivo, socket persistente, rate-limit) | ~1 pp | alta |
| Cap.47 | §3 Catalogo simboli FIB e cash europei (tabella IDEM + cash + schemi PRICE/BOOK_5/ANAG, codice mese I=settembre) | ~1 pp | alta |
| Cap.48 | §4 Format dati canonico runtime (CSV BOM UTF-8 + manifest JSON, source ∈ {DIRECTA, AGG_FROM_D, AGG_FROM_60s}) | ~0,75 pp | media |
| Cap.49 | §5 Mappatura schema DAPI -> bundle frozen Portara (tabella canonica + bar_synthetic in runtime) | ~1 pp | alta |
| Cap.50 | §6 Gestione errori, recovery, riavvio Darwin (codici 1004/1007/1030, backoff, fallback aggregazione, RUNTIME_DEGRADED) | ~1 pp | alta |
| Cap.51 | §7 Warm-up stati condizionali (EGARCH/quantili, lookback ≤100gg, fallback Portara) | ~0,75 pp | media |
| Cap.52 | §8 Sessione operativa runtime FIB 08:00-22:00 CET (calendario, timezone, allineamento epoche) | ~0,5 pp | media |
| Cap.53 | §9 Decisione Q-A: gating cash europei (verdetto Q-A-3, perimetro vincolante) | ~0,75 pp | alta |
| Cap.54 | §10 Audit log e retention (formato, retention 90gg rolling / permanente giorni emissione) | ~0,5 pp | media |
| Cap.55 | §11 Punti aperti fuori scope (FDAX standard, lookup IDEM, vendor cross-index, rinvio CAP-DATA-03) | ~0,5 pp | bassa |
| Cap.56 | §12 Tabella decisioni del capitolo (ID, descrizione, motivazione 1 riga) | ~0,75 pp | alta |

Totale stimato: **~9 pp A4** (entro il range 8-10 pp della consulenza).

Vincoli operativi:
- La numerazione Cap.45-Cap.56 e' VINCOLANTE per il Developer.
- Il Developer e' tenuto ad aggiornare `00_indice.md` aggiungendo la
  sezione "Parte 9 — Pipeline runtime FIB su Directa DAPI (~8-10 pp)"
  con la lista dei 12 capitoli sopra (Cap.45..Cap.56), ognuno con il
  titolo coerente con la scaletta e l'indicazione "in review" durante
  il ciclo Developer→Reviewer e "PASS" con data e hash review a chiusura.

---

## (iii) Censimento M-promemoria pertinenti a CAP-DATA-02

Lettura `tasks/CARRYOVER.md` aggiornata al 2026-05-27. Tabella di
censimento e verdetto di pertinenza per CAP-DATA-02 (Parte 9 / Cap.45-56).

| M-ID | Origine | Pertinenza CAP-DATA-02 | Motivazione |
|------|---------|------------------------|-------------|
| M-2 | Review v1 CAP-02 | **NO** | Verifica empirica $L_{max}=30$s su latenza Telegram. Materia di **Appendice E** (Telegram bot personale). Non si chiude in Parte 9, resta OPEN come carryover ad Appendice E nel ciclo di consolidamento delle Appendici. CAP-DATA-02 NON tratta il canale Telegram, tratta il canale dati Directa. Rinvio motivato. |
| M-4 | Review v4 CAP-01 | NO | Tasso di rimpiazzo NSGA-II e baseline 12.800-25.600 minuti. Gia' **CLOSED-CAP-05** (Cap.23.6 Parte V). Nessuna azione richiesta. |
| M-5 | Review v1 CAP-03 (Q-06/C-4.3) | NO | Benchmark rolling vs expanding vs EWMA + Inoue-Rossi 2011. Gia' **CLOSED-CAP-05** (Cap.25.3 Parte V). Nessuna azione richiesta. |
| M-6 | Review v1 CAP-03 (Q-09/C-7.3) | NO | Classificazione regime media vs mediana + test stabilita'. Gia' **CLOSED-CAP-05** (Cap.25.4 Parte V). Nessuna azione richiesta. |
| M-1 v2 CAP-03 | Review v2 CAP-03 | NO | Pivot inizio/fine sessione non confermabili. Gia' **CLOSED-CAP-04** (Cap.16). Nessuna azione richiesta. |
| M-2 v2 CAP-03 | Review v2 CAP-03 | NO | Cadenza ricalibrazione EGARCH in production. Gia' **CLOSED-CAP-06 completo** (Cap.27.5 + Cap.30.4 Parte VI). Nessuna azione richiesta. |
| M-7 | Review v1 CAP-04 (O-5) | NO | Censoring informativo Cox cause-specific. Gia' **CLOSED-CAP-05** (Cap.25.6 Parte V). Nessuna azione richiesta. |
| M-8 | Developer CAP-04 | NO | Verifica censoring non-informativo nel survival. Gia' **CLOSED-CAP-05** (Cap.25.6 Parte V). Nessuna azione richiesta. |
| M-9 | Developer CAP-04 | NO | Benchmark Cox cause-specific vs Fine-Gray. Gia' **CLOSED-CAP-05** (Cap.25.7 Parte V). Nessuna azione richiesta. |
| M-10 | Developer CAP-04 | NO | Test Schoenfeld per assunzione hazard proporzionali. Gia' **CLOSED-CAP-05** (Cap.25.8 Parte V), con derivazione di M-16 condizionale chiuso in Parte VII. Nessuna azione richiesta. |
| M-11 | Developer CAP-04 | NO | Dimensionalita' massima feature survival ($K_{max}$). Gia' **CLOSED-CAP-05** post-rework v3 (Cap.22.6 + Cap.26.7 Parte V). Nessuna azione richiesta. |
| M-12 | Review v1 CAP-04 (O-3) + Dev | NO | Flag `target_2_type` / `stop_type` nel payload Cap.6.1. Gia' **CLOSED-CAP-04** (mini-patch CAP-02 Iterazione 4). Nessuna azione richiesta. |
| M-13 | Review v1 CAP-04 (O-4) + Dev | NO | Catalogo feature 37 vs 38 per trade_range ($x^{(A_{range})}$). Gia' **CLOSED-CAP-04** (Cap.21.5 CAP-04 Iterazione 2). Nessuna azione richiesta. |
| M-14 | Developer CAP-04 | NO | Stratificazione Cox per regime calmo/turbolento. Gia' **CLOSED-CAP-05** (Cap.25.5 Parte V). Nessuna azione richiesta. |
| M-15 | Developer CAP-04 | NO | Parametri `trade_range` congelamento numerico ($A_{range,min}$, $N_{osc}$, ...). Gia' **CLOSED-CAP-05** (Cap.26.5/26.6 Parte V). Nessuna azione richiesta. |
| M-16 condizionale | Review v1 CAP-05 (Cap.25.8 trigger) | NO | Cox time-varying coefficients se test Schoenfeld viola sistematicamente in >50% dei fold. Gia' **CLOSED-CAP-07 con condizione operativa** (Cap.31.3 Parte VII + metadato bundle `cox_time_varying_active` in Cap.35.1). L'attivazione dipende dall'esito empirico del walk-forward nel ciclo successivo di training, NON e' materia di CAP-DATA-02. **INVARIATO** rispetto a quanto richiesto dal Planner. Nessuna azione richiesta. |

**Sintesi:** **nessun M-promemoria del CARRYOVER e' pertinente a
CAP-DATA-02**. La Parte 9 e' un capitolo a perimetro nuovo (provider
runtime DAPI) che non eredita M-promemoria aperti dalla pipeline
metodologica delle Parti I-VIII. M-2 resta OPEN come carryover ad
Appendice E (Telegram), non si chiude in Parte 9. M-16 resta
CLOSED-CAP-07 invariato come da vincolo del Planner.

**Carryover post-CAP-DATA-02:** non si prevedono nuovi M-promemoria
intrinseci al capitolo a livello di Planner. La Review v1 potra'
emetterne; se cosi' fosse, l'Orchestratore dovra' registrarli nel
CARRYOVER al passaggio PASS, in particolare per la futura CAP-DATA-03
/ Parte 10 (continuita' tape, recupero gap, riconciliazione canonica
giornaliera, storicizzazione strutturata).

---

## (iv) Decisioni di scope residue

Verifica esplicita di completezza del task card rispetto alle decisioni
ratificate (D-1, D-6, C-1, C-2, C-3, C-7 sui 6 Gap, Q-A-3 sul gating
cash europei). Lista delle decisioni gia' chiuse:

- D-1: niente market data a pagamento — vincolo chiuso.
- D-6: uso esclusivo canale DAPI, no DGo/TradingView concorrente — chiuso.
- C-1: naming β2 (CAP_09_parte_9.md, REPORT_CAP_09.md, "Parte 9" arabo) — chiuso.
- C-2: push diretto origin/main — chiuso.
- C-3: aggiornamento 00_indice.md a fine ciclo — chiuso.
- C-7: 6 Gap obbligatori (Gap-1..Gap-6) — chiusi nella sezione "Sei gap obbligatori".
- Q-A-3: cash europei come logging + gating qualitativo, fuori dal feature
  tensor e fuori dal cromosoma — chiusa.

**Verifica ambiguita' residue:** nessuna. Tutte le scelte di scope IN/OUT,
i 12 capitoli della scaletta, i 6 Gap, i 10 Done criteria, le decisioni
ratificate e i 4 Rollback criteria coprono il perimetro del task senza
lasciare zone grigie:

- la mappatura schema DAPI -> bundle frozen Portara (Done criterion #4) e'
  obbligata dall'invariante `bar_synthetic` di Parte 8 Cap.40;
- la regola "research = runtime" applicata all'adapter (Scope IN #8) e'
  obbligata da Parte 8 Cap.37;
- il gating cash europei (Q-A-3) e' obbligato da `config/gating_rules.yaml`
  fuori dal GA e fuori dal cromosoma di Parte V Cap.22;
- il vincolo "no esecuzione ordini" (Scope OUT, porta 10002) e' obbligato
  da Parte I Cap.1 ("solo emissione, nessuna esecuzione").

**Conclusione:** nessuna **Q-XX** nuova da aprire in `tasks/QUESTIONS.md`.
Il task card e' eseguibile dal Developer senza ipotesi proprie. La pipeline
parte: Developer v1 → Review v1 → eventuale punto di controllo supervisore
sulla classificazione GA → fix → ... → PASS.

---

## Finding di Review da risolvere (rework v2)

Verdetto Review v1: **FAIL** (commit `baeab2c`, file `reviews/REVIEW_CAP_09_review.md`).
Punto di controllo supervisore eseguito 2026-05-28. Decisioni del supervisore:

- 7 BUG REALI (B-1..B-7): da risolvere **obbligatoriamente**.
- 4 MIGLIORA PERFORMANCE (NB-1..NB-4): tutti decisi Opzione A → da risolvere.
- 1 MIGLIORA PERFORMANCE (NB-5): coperto per propagazione da B-2 (aggiunta colonna `bar_synthetic` al format CSV) → si chiude automaticamente quando B-2 è chiuso.
- 1 MIGLIORA PERFORMANCE (NB-6) + 2 NEUTRO (O-1, O-2): NON vanno a Developer.

### BUG REALI (obbligatori)

| ID | Capitolo/Riga | Descrizione finding | Azione richiesta al Developer v2 |
|----|---------------|---------------------|-----------------------------------|
| B-1 | Cap.52 r254 | Chiusura automatica segnali a 22:00 CET contraddice Parte II Cap.7 (counter $\Delta t_{cromosoma}$ scavalca interruzioni notturne fino a 1680 min) | Rimuovere la regola di chiusura automatica a 22:00. Il segnale `active` alla chiusura sessione resta `active` (la state machine di Parte II Cap.7 governa). La pipeline in stand-by fuori sessione mantiene lo stato segnale; al boot del giorno successivo riprende dallo stato salvato. Citare esplicitamente Parte II Cap.7 r126. |
| B-2 | Cap.48 r100, sample CSV | Format CSV runtime non simmetrico al bundle frozen Cap.40: mancano `tick_count` e `bar_synthetic`; sample sparsi non in griglia uniforme | Estendere header CSV runtime con colonne `tick_count` e `bar_synthetic` (booleano). Dichiarare che la pipeline runtime produce griglia 1-min **uniforme** sulla sessione 08:00-22:00 CET con barre sintetiche `bar_synthetic=True` per i minuti senza trade (coerenza con Parte 8 Cap.40). Sample non uniformi (export storici esistenti) sono **input campione di validazione** del Gap-5, non template normativo del format runtime: distinguere esplicitamente i due ruoli. |
| B-3 | Cap.49 r146 | Regola `bar_synthetic=True ⟺ no PRICE nel minuto` non applicabile a FIB futures (INDAGINE B.2 verifica solo `ANAG+BOOK_5` per FIB; PRICE empiricamente solo per cash) | Riformulare la regola di derivazione `bar_synthetic` per il FIB futures basandosi sul flusso effettivo. Opzione raccomandata: in regime realtime sul FIB, la barra 1-min è "reale" se almeno un evento `BOOK_5` con `bid1_lots ≥ 1` AND `ask1_lots ≥ 1` è stato osservato nel minuto; altrimenti `bar_synthetic=True` con forward-fill del mid del BOOK_5 dell'ultima barra reale. In regime storico (CANDLERANGE su porta 10003), `bar_synthetic=True` per i minuti che non compaiono nella risposta. Distinguere esplicitamente i due regimi. |
| B-4 | Cap.47 r65-71 | Tabella catalogo attribuisce schema `PRICE` ai futures FIB6F/FIB6I/MINI6F/MINI6I/MINI6C senza evidenza empirica | Correggere la tabella Cap.47: per i futures FIB rimuovere `PRICE` dalla colonna "Schemi" lasciando solo `BOOK_5, ANAG` (verificato empiricamente su FIB6I 2026-05-27 e atteso per simmetria su FIB6F). Per i cash europei (DGER, DITAS, DSTX50, DFRA) lasciare `PRICE`. Aggiungere nota che giustifica la differenza: per i futures IDEM il gateway pubblica il book come tick stream, per i cash europei il last price come tick stream. |
| B-5 | Cap.53 r273 | Esempio gating "se DGER scende >2% sospendi invio segnali long FIB" è funzionalmente Q-A-2 (scartato); viola determinismo replay (config esterna al bundle frozen) e inquina metriche lifecycle live | Riformulare l'esempio di gating Cap.53 in modo coerente con Q-A-3: il gating cash europei è **POST-EMISSIONE** dal motore. Il segnale viene emesso dal bundle e arriva a una **coda di pubblicazione**. Il gating qualitativo (config `gating_rules.yaml`) interviene solo sulla **pubblicazione Telegram al supervisore** (es. flag visivo, nota di rischio nel messaggio), MAI sopprimendo l'emissione. Il segnale resta emesso nel log audit (per replay deterministico). Esempio corretto: "se DGER scende >2% intraday, il messaggio Telegram per i segnali long FIB include una nota di avvertimento `[GATING-cash-europei: DGER -2.3% intraday]`; il segnale viene comunque inviato e tracciato regolarmente nello state machine". Replay bit-exact preservato: lo stesso segnale è sempre emesso, solo il payload Telegram cambia condizionalmente. |
| B-6 | Cap.51 r221-225 | Warm-up fallback Portara per downtime >100gg dipende da riconciliazione DAPI/Portara che Cap.55 dichiara fuori scope (CAP-DATA-03); EGARCH su due back-adjustment diversi | Rimuovere il fallback Portara per downtime >100gg dalla normativa Parte 9. Sostituire con: "Per restart dopo downtime >100 giorni, la pipeline runtime **non riparte automaticamente**; entra in stato `RUNTIME_STALE_RESTART` e richiede intervento supervisore. La riconciliazione DAPI/Portara e la procedura di re-bootstrap dopo gap >100gg sono **fuori scope CAP-DATA-02**, rinviate a CAP-DATA-03 / Parte 10 (Cap.55). Probabilità: bassa (richiede downtime continuativo >5 mesi solari)." Eliminare la dipendenza circolare. |
| B-7 | Cap.49 r145 | Dominio `tick_count` divergente training/runtime: regola attuale (`tick_count = volume proxy / NaN` discriminato da `bar_synthetic`) confonde dominio booleano `bar_synthetic` (trade/no-trade) con discriminante realtime/storico | Riformulare la mappatura `tick_count` in Cap.49 distinguendo correttamente i due assi: (a) **realtime** (porta 10001): `tick_count` = numero di eventi `BOOK_5` ricevuti nel minuto (proxy puntuale dell'attività di book); (b) **storico** (porta 10003 `CANDLERANGE`): `tick_count` non è esposto dallo schema `CANDLE` → impostato a `NULL` (non `NaN` che è marker numerico). Il campo `bar_synthetic` resta booleano (trade vs no-trade), come in Parte 8 Cap.40, e NON discrimina realtime/storico. Coerenza con bundle frozen Portara: il training conserva `tick_count` reale; in runtime su porta 10001 `tick_count` è derivato; in warm-up storico su porta 10003 `tick_count = NULL` con il consumer a valle (es. feature engineering Parte III Cap.15) configurato per ignorare `NULL` o usare proxy `volume`. |

### MIGLIORA PERFORMANCE decisi dal supervisore (obbligatori in rework v2)

| ID | Capitolo/Riga | Opzione decisa | Azione richiesta al Developer v2 |
|----|---------------|----------------|-----------------------------------|
| NB-1 | Cap.47 r90/r91/r94, Cap.55 r341 | A — esempi normativi su FIB6F + lookup parziale F=giu/I=set + procedura ANAG runtime-discovery | Sostituire negli esempi schemi r90 (ANAG) e r91 (BOOK_5) i riferimenti `FIB6I` con `FIB6F` come ticker normativo del front-month corrente. Lo schema ANAG per FIB6F è normato per simmetria con il probe empirico su FIB6I (2026-05-27): formato `ANAG;FIB6F;HH:MM:SS;<ISIN>;FTSE MIB INDEX FUTURE GIU26;<ref_price>;0;0` con descrizione attesa `GIU26 → giugno 2026`. In Cap.47 r94 sostituire l'esempio `SET26 → settembre 2026` con `GIU26 → giugno 2026` come esempio del front-month corrente; lasciare `SET26` solo come esempio del **next-month** nello switch (vedi NB-2). In Cap.55 r341 espandere la dichiarazione: la lookup parziale **già nota** è `F=giugno, I=settembre` (derivata da prassi dei sample export FIB6F + probe 2026-05-27 su FIB6I); la lookup completa per gli altri codici mese va derivata via ANAG runtime, con tabella codici mese arricchita progressivamente nel ciclo operativo. |
| NB-2 | Cap.47 r94, paragrafo dedicato | A — switch fuori-sessione FIB6F→FIB6I con precisazione "chiusura contratto 09:00 giorno scadenza" | Aggiungere in Cap.47 un paragrafo dedicato "Policy switch front-month durante runtime" che norma: in IDEM il contratto FIB scade la **terza venerdì del mese alle 09:00 CET** (negoziazione di chiusura mattutina, settlement su asta di apertura del FTSE MIB cash). Lo switch operativo della pipeline avviene **al boot della sessione del giorno t** (giorno di scadenza, terza venerdì): la pipeline alle 08:00 CET sottoscrive direttamente il **next-month** saltando completamente la finestra 08:00-09:00 del front in scadenza. Marker `CONTRACT_SWITCH` nel log audit al boot, con payload `{from: "FIB6F", to: "FIB6I", scadenza_from: "2026-06-19"}` (esempio per il ciclo giugno→settembre 2026). EGARCH stato condizionato preservato (la calibrazione è su ratio-adjusted virtuale di Parte 8 Cap.38, non interrotta dal cambio di ticker concreto). Distinguere esplicitamente: il filtro pre-expiry $N=3$ di Parte 8 Cap.39 è di **training** (esclude le 3 giornate t-3, t-2, t-1 dal training set); il runtime invece opera fino al giorno t-1 incluso su front e dal giorno t in poi su next. Aggiornare la tabella decisioni D-9 con la nuova decisione D-9-NB2 e relativo rollback. |
| NB-3 | Cap.54 r307, tabella D-9 | A — 6 eventi terminali distinti | Sostituire l'evento `SIGNAL_CLOSED` aggregato in Cap.54 r307 con i 6 eventi terminali distinti coerenti con Parte II Cap.7: `SIGNAL_TARGET_1_HIT`, `SIGNAL_STOPPED`, `SIGNAL_INVALIDATED`, `SIGNAL_MISSED_TARGET`, `SIGNAL_EXPIRED`, `SIGNAL_REVOKED`. Mantenere `SIGNAL_EMITTED` e `SIGNAL_TRIGGERED` come pre-terminali. Per `SIGNAL_MISSED_TARGET` la sotto-distinzione `pretrigger_timeout` vs `posttrigger_timeout` resta nel payload JSON con campo obbligatorio `timeout_cause ∈ {pretrigger, posttrigger}`. Dashboard live (Parte VI Cap.30) e replay bit-exact (Parte II Cap.10) ora robusti. Aggiornare la tabella decisioni D-9 con la nuova decisione D-9-NB3 e relativo rollback. |
| NB-4 | Cap.51 r216, tabella D-9 | A — congelare $L_{warmup}=30$ giorni con motivazione aritmetica | Sostituire in Cap.51 r216 la dichiarazione "$L_{warmup} \approx 30$ giorni, da congelare in FASE-D" con "$L_{warmup} = 30$ giorni di trading IDEM, **congelato in Parte 9**. Motivazione aritmetica: il requisito minimo del warm-up è $N_{reg}=20$ sessioni (Parte III Cap.14) = 20 giorni di trading; il valore 30 garantisce ~50% di margine. Implementazione: 30 × 840 barre/sessione = 25.200 barre, copre $W_{norm}=1000$ (Parte III Cap.15), $T_{warmup,\text{EMA}}=74$ (Parte III Cap.15), $T_{warmup,\text{norm}}=100$ (Parte III Cap.15) e $N_{reg} \cdot 840 = 16.800$ con margine ~8.400 barre. Rifinibile solo via nuovo task Planner." Replay bit-exact ripristinato. Aggiornare la tabella decisioni D-9 con la nuova decisione D-9-NB4 e relativo rollback ($L_{warmup}$ non reversibile dentro Parte 9; revisione richiede nuovo task Planner). |

### Finding NON da risolvere (registrati per completezza)

- **NB-5** (CSV runtime senza colonna `bar_synthetic`): si chiude per propagazione da B-2.
- **NB-6** (reinterpretazione D-1 esclude DAPI Datafeed base): NEUTRO, ignorato per default CLAUDE.md.
- **O-1** (banner manifest con doppi spazi): NEUTRO cosmetico, ignorato.
- **O-2** (DSTX50/DFRA dichiarati atteso lowercase senza verifica): NEUTRO, ignorato.

### Vincoli per la rework v2

- Nessuna modifica alle Parti I-VIII del doc v2 (incluso `CAP_08_parte_8.md`).
- Nessuna riapertura delle decisioni ratificate (Q-A-3, D-1, D-6, C-1..C-7).
- Mantenere la numerazione capitoli Cap.45..Cap.56 e la scaletta 12 sezioni del Planner.
- Aggiornare `00_indice.md` aggiungendo "v2" al marker "IN REVIEW" (es. "Parte 9 — Pipeline runtime FIB su Directa DAPI (~8-10 pp) [IN REVIEW v2]") senza modificare le righe delle Parti I-VIII.
- Aggiornare `reports/REPORT_CAP_09.md` con sezione "Rework v2 — finding chiusi" che mappa ciascun finding a (capitolo/riga modificata, citazione testo nuovo, riferimento incrociato).
- Commit messaggio: `[DEV] CAP-DATA-02 Parte 9 v2: rework post-Review v1 (7 BUG REALI + 4 NB chiusi)`.
- Push diretto a origin/main.
- Settare `tasks/DEV_STATUS.md = READY_FOR_REVIEW` dopo commit.
