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
