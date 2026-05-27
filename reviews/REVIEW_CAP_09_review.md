# Review CAP-DATA-02 - Pipeline runtime FIB su Directa DAPI (Parte 9)

**Verdetto**: FAIL

## Sintesi metodologica

Audit ostile dei 12 capitoli normativi Cap.45-56. Il capitolo presenta una struttura coerente, copre i 6 Gap, ratifica formalmente Q-A-3 e cita gli input autoritativi attesi, ma introduce contraddizioni dirette con invarianti gia congelate nelle Parti I-VIII e ambiguita operative che rompono il replay deterministico bit-exact (Parte II Cap.10).

---

## Problemi bloccanti (causano FAIL)

### B-1 - Chiusura automatica segnali alle 22:00 CET contraddice Parte II Cap.7

Cap.52 r254: alla chiusura 22:00 CET i segnali active vengono chiusi automaticamente. Ma Parte II Cap.7 r126 e Cap.6.5 dichiarano che il counter Delta_t_cromosoma ha dominio fino a 1680 minuti e scavalca le interruzioni notturne. Un segnale active alla chiusura 22:00 continua a vivere sulla sessione successiva. La transizione active->expired non e triggerata dall orologio di sessione ma dal counter cromosoma-specifico.

**Impatto GA**: chiusura prematura di segnali validi per due sessioni, alterando distribuzione di target_1_hit e missed_target. Metriche di lifecycle live (Parte VI Cap.30) divergerebbero dal backtest calibrato, falsificando monitoring post go-live e gate Parte VII Cap.36.

### B-2 - Format CSV runtime (Cap.48) non simmetrico al bundle frozen Cap.40

Cap.48 r100 dichiara simmetria con bundle Parte 8 Cap.40, ma i sample FIB6F_5M.csv hanno header: symbol, timeframe, timestamp, date, time, open, high, low, close, volume, source. Mancano tick_count e bar_synthetic obbligatori nel bundle (Cap.40 r94). I sample sono sparsi (solo barre con trade), non in griglia uniforme con bar_synthetic=True. Lo script export_directa_history_parametric.py non scrive bar_synthetic.

**Impatto GA**: senza bar_synthetic nel CSV, le feature di volatilita EGARCH (Parte III Cap.13) non sanno escludere forward-fill -> bias verso bassa volatilita -> regime calmo/turbolento (Parte III Cap.14) classificato male -> soglie tau_vol e tau_dist valutate su quantili sbagliati -> distorsione signal-to-trade.

### B-3 - Regola bar_synthetic (Cap.49) presuppone push PRICE su FIB futures, ma PRICE non esiste empiricamente per FIB

Cap.49 r146: bar_synthetic=True se nessun PRICE ricevuto entro il minuto in regime push tick. Verifica empirica 2026-05-27 (INDAGINE r360-376): SUB FIB6I restituisce solo ANAG e BOOK_5, mai PRICE. Il push PRICE empiricamente esiste solo per cash (DGER, DITAS). Applicando letteralmente la regola, tutte le barre del FIB diventano sintetiche -> EGARCH senza input -> sigma_hat non disponibile -> bundle non emette segnali.

**Impatto GA**: motore inerte in produzione; signal-to-trade=0.

### B-4 - Tabella Cap.47 attribuisce schema PRICE ai futures FIB senza evidenza empirica

Cap.47 r65-71 elenca PRICE, BOOK_5, ANAG come schema realtime per FIB6F/FIB6I/MINI6F/MINI6I/MINI6C. INDAGINE B.2-B.4 ha verificato PRICE solo per cash (DGER, DITAS); per FIB6I solo ANAG + BOOK_5. La tabella generalizza per simmetria un dato non verificato.

**Impatto GA**: in assenza di sorgente push su 10001 per FIB, l adapter dovrebbe ricostruire barre 1-min dal BOOK_5 (mid-price L1?) o pull periodico CANDLE su 10003. Nessuno dei due e normato. Replay bit-exact non garantibile.

### B-5 - Esempi di gating qualitativo Cap.53 sospendono pubblicazione, violando dichiarazione post-hoc

Cap.53 r273 esempio: se DGER scende oltre 2 percento intraday, sospendi invio segnali long su FIB. Questo non e post-hoc sull output del bundle; e condizione di pubblicazione condizionata da variabile cash. Effetti:

1. Funzionalmente identico a Q-A-2 (blocca segnale su drop DGER) dichiarato scartato.
2. Viola determinismo replay (Parte II Cap.10): due run con config/gating_rules.yaml diverso producono pubblicazioni diverse; la config NON e parte del bundle frozen.
3. Metriche lifecycle live (Parte VI Cap.30) inquinate da gate non nel cromosoma; monitoring post go-live perde valore probatorio.

**Impatto GA**: distorce signal-to-trade misurata in produzione. Se 10 percento segnali soppressi da gating cash, ranking cromosomi live diverge da calibrazione walk-forward -> drift selezione non controllato.

### B-6 - Warm-up fallback Portara per downtime oltre 100gg dipende da riconciliazione fuori scope

Cap.51 r221-225: per downtime oltre 100 giorni, warm-up via Portara + integrazione DAPI ultimi 100. Cap.48 r125: format runtime su serie unadjusted nativa. Cap.55 r349 dichiara fuori scope la riconciliazione canonica DAPI/Portara. Il bundle EGARCH calibrato su Portara ratio-adjusted; warm-up cross-source DAPI unadjusted + Portara ratio-adjusted produce sigma_hat su due back-adjustment diversi.

**Impatto GA**: stato condizionato post-warm-up deterministicamente errato su restart oltre 100gg. Soglie tau_vol su sigma_hat inquinato bloccano o sbloccano emissioni in modo non corrispondente al training. Dipendenza circolare con CAP-DATA-03.

### B-7 - Cap.49 introduce dominio tick_count divergente sui record warm-up storico

Cap.49 r145: tick_count impostato a volume come proxy o NaN su record warm-up; il flag bar_synthetic discrimina i due regimi. Falso: bar_synthetic ha dominio booleano (trade-presente vs assente), non discrimina realtime/storico. Distribuzioni di tick_count differiscono fra training e runtime. Il bundle frozen Parte 8 Cap.40 r94 persiste TickCount; coerenza schema completa richiesta da invariante research=runtime.

**Impatto GA**: se feature derivata da TickCount entra nel catalogo, distribuzione runtime diverge da training -> shift feature -> bundle invalido. NaN propagato e patologico.

---

## Problemi non bloccanti (causano CONDITIONAL)

### NB-1 - Procedura derivazione front-month FIB (Cap.47) dipende da lookup mese fuori scope

Cap.47 r94: SUB su ticker candidati FIB6F, FIB6I, FIB6L, seguendo lookup mese Directa-IDEM. Cap.55 r341: lookup completa NON verificata empiricamente, NON congelata nel doc v2 corrente. La procedura referenzia dati non disponibili.

**Impatto GA**: pipeline potrebbe sottoscrivere contratto sbagliato (non-front, volume basso) e calcolare feature su serie non rappresentativa. Probabilita bassa se FASE-D risolve empiricamente al primo run; impatto residuo se selezione front-month non tracciata in audit.

### NB-2 - Cap.47 cita Parte 8 Cap.39 in modo improprio per policy switch runtime

Cap.47 r94: applica filtro pre-expiry N=3 di Parte 8 Cap.39 al passaggio front-month al next-month. Parte 8 Cap.39 r69: filtro esclude barre dal training, non altera state machine, policy switch in produzione e demandata alle componenti runtime del progetto. Cap.47 sovrappone semantiche diverse: filtro training vs decisione di switch runtime.

**Impatto GA**: transizione fra contratti durante sessione 08:00-22:00 attiva implicherebbe interruzione EGARCH e ridiscontinuita prezzi (bundle calibrato su ratio-adjusted continua). Senza policy esplicita, lo switch puo rompere stato condizionato della sessione corrente.

### NB-3 - Cap.54 logga solo SIGNAL_EMITTED/TRIGGERED/CLOSED, Parte II Cap.7 ha 6 stati terminali distinti

Cap.54 r307: eventi SIGNAL_EMITTED, SIGNAL_TRIGGERED, SIGNAL_CLOSED. Parte II Cap.7: 6 stati terminali target_1_hit, stopped, invalidated, missed_target, expired (con causa pretrigger_timeout/posttrigger_timeout), revoked. Granularita impoverita: SIGNAL_CLOSED non distingue 6 transizioni. Replay bit-exact richiede eventi puntuali.

**Impatto GA**: metriche lifecycle (target_hit_rate, invalidation_rate, ecc.) richiedono distinzione transizioni. Log impoverito impedisce calcolo corretto dei tassi -> monitoring live degradato.

### NB-4 - L_warmup circa 30 giorni dichiarato valore di lavoro non congelato (Cap.51 r216)

Cap.51 r216: L_warmup circa 30 giorni, da congelare in FASE-D. Il parametro determina stato condizionato post-warm-up sigma_hat e quindi classificazione regime e soglie emissione. Non congelato = ambiguita output motore.

**Impatto GA**: cambiare L_warmup fra run produce stati condizionati diversi -> emissioni diverse a parita di bundle frozen. Replay bit-exact non garantito. Aritmetica: 30 giorni x 840 barre/sessione = 25200 barre, coprono W_norm=1000 e N_reg=20 con margine, ma verifica implicita e non formalizzata.

### NB-5 - CSV runtime Cap.48 incoerente con bar_synthetic, inferenza ambigua da volume=0

Sample FIB6F_5M.csv r4: FIB6F,5M,2026-01-19 08:00:00,...,0,DIRECTA con volume=0 e source=DIRECTA. Senza colonna bar_synthetic, adapter Cap.49 deve reinferire da volume; barra reale apertura 08:00 con volume=0 e possibile per FIB front-month a bassa liquidita iniziale. Inferenza bar_synthetic=(volume==0) produce falsi positivi sintetici su barre reali di apertura.

**Impatto GA**: barre reali apertura classificate sintetiche -> escluse da EGARCH -> sottostima volatilita apertura -> emissioni errate in apertura sessione.

### NB-6 - D-1 reinterpretato in Cap.54 oltre perimetro ratificato dal Planner

ACTIVE_TASK.md r67: D-1 niente market data a pagamento senza qualificazione. Cap.54 r327 reinterpreta: D-1 si applica solo a market data opzionali futures cross-index, non a DAPI Datafeed di base. Coerente operativamente (senza DAPI base no canale dati) ma non ratificata dal Planner come distinzione formale. Espone a rischio compliance interna.

**Impatto GA**: nessuno diretto; impatto su compliance/audit interno.

---

## Osservazioni minori

### O-1 - Banner manifest sample con doppi spazi rispetto a Cap.46

Cap.46 r29 banner: DARWIN_STATUS;CONN_OK;TRUE;Release 2.5.1 build 04/02/2025 (uno spazio). Sample FIB6F_manifest.json r12: Release con due spazi prima di 2.5.1. Se la pipeline loggasse verbatim il diff Gap-5 confronterebbe correttamente; se ripulisce, due implementazioni divergono. Sanity verifica.

### O-2 - DSTX50 e DFRA dichiarati atteso lowercase in Cap.47 senza verifica empirica

Cap.47 r77-82: DSTX50 e DFRA hanno nota (atteso lowercase) non verificato, mentre DGER e DITAS sono (lowercase nella risposta) verificato. Distinzione onesta ma non incide su comportamento GA (ticker solo per logging/gating, non training).

---

## Citazioni problematiche dal testo

- alla chiusura 22:00 CET i segnali attivi vengono chiusi automaticamente (Cap.52 r254) - problema: regola non esiste in Parte II Cap.7 - classificazione: BUG REALE

- Il format e simmetrico rispetto al bundle frozen Portara (Parte 8 Cap.40) (Cap.48 r100) - problema: CSV manca di tick_count e bar_synthetic, sparso non in griglia uniforme. Non simmetrico - classificazione: BUG REALE

- bar_synthetic=True se in regime push tick nessun PRICE ricevuto entro il minuto (Cap.49 r146) - problema: FIB futures non emette PRICE empiricamente, regola trasforma tutte le barre FIB in sintetiche - classificazione: BUG REALE

- Schema realtime PRICE BOOK_5 ANAG per FIB6F/FIB6I/MINI6F/MINI6I/MINI6C (Cap.47 r67-71) - problema: PRICE non verificato per FIB futures; INDAGINE B.2 mostra solo ANAG+BOOK_5 - classificazione: BUG REALE

- se DGER scende oltre 2 percento, sospendi invio segnali long FIB (Cap.53 r273) - problema: funzionalmente Q-A-2 scartato; viola replay deterministico se config cambia fra run - classificazione: BUG REALE

- Se gap downtime oltre 100 giorni: warm-up via Portara + DAPI ultimi 100 (Cap.51 r224) - problema: richiede riconciliazione DAPI/Portara fuori scope Cap.55; bundle EGARCH non coerente con due back-adjustment diversi - classificazione: BUG REALE

- tick_count impostato a volume come proxy o NaN, bar_synthetic discrimina due regimi (Cap.49 r145) - problema: bar_synthetic discrimina trade/no-trade, non realtime/storico; dominio tick_count diverge fra training e runtime - classificazione: BUG REALE

- valore di lavoro L_warmup ~30 giorni, da congelare in FASE-D (Cap.51 r216) - problema: parametro non congelato determina stato condizionato post-warm-up; replay bit-exact non garantito - classificazione: MIGLIORA PERFORMANCE

- filtro pre-expiry N=3 di Parte 8 Cap.39 al passaggio front-month al next-month (Cap.47 r94) - problema: Cap.39 filtro e di training, non runtime; policy switch in produzione demandata a Parte 9, va normata qui - classificazione: MIGLIORA PERFORMANCE

- sequenza SUB su ticker candidati FIB6F, FIB6I, FIB6L (Cap.47 r94) - problema: lookup mese fuori scope al Cap.55; procedura referenzia dati non disponibili - classificazione: MIGLIORA PERFORMANCE

- Tipologia evento HANDSHAKE SIGNAL_EMITTED SIGNAL_TRIGGERED SIGNAL_CLOSED (Cap.54 r307) - problema: granularita impoverita rispetto ai 6 stati terminali di Parte II Cap.7 - classificazione: MIGLIORA PERFORMANCE

- D-1 si applica solo a market data opzionali futures cross-index, non a DAPI Datafeed di base (Cap.54 r327) - problema: reinterpretazione di D-1 oltre il perimetro Planner - classificazione: NEUTRO

---

## Classificazione per il supervisore

| # | Problema | Classificazione | Mandare a Development? |
|---|----------|-----------------|------------------------|
| B-1 | Chiusura 22:00 CET contraddice Parte II Cap.7 | BUG REALE | SI |
| B-2 | Format CSV runtime Cap.48 manca tick_count e bar_synthetic | BUG REALE | SI |
| B-3 | Regola bar_synthetic Cap.49 assume PRICE su FIB ma FIB non emette PRICE | BUG REALE | SI |
| B-4 | Cap.47 attribuisce PRICE ai futures FIB senza evidenza | BUG REALE | SI |
| B-5 | Gating Cap.53 sospende emissione (Q-A-2 mascherato), viola replay deterministico | BUG REALE | SI |
| B-6 | Warm-up fallback Portara dipende da riconciliazione fuori scope | BUG REALE | SI |
| B-7 | Cap.49 introduce dominio tick_count divergente training/runtime | BUG REALE | SI |
| NB-1 | Derivazione front-month dipende da lookup mese fuori scope | MIGLIORA PERFORMANCE | in attesa decisione supervisore |
| NB-2 | Cap.47 cita Parte 8 Cap.39 in modo improprio per policy switch | MIGLIORA PERFORMANCE | in attesa decisione supervisore |
| NB-3 | Log Cap.54 con eventi SIGNAL aggregati vs 6 stati terminali | MIGLIORA PERFORMANCE | in attesa decisione supervisore |
| NB-4 | L_warmup ~30 giorni non congelato | MIGLIORA PERFORMANCE | in attesa decisione supervisore |
| NB-5 | Inferenza ambigua bar_synthetic da volume=0 nel CSV sparso | MIGLIORA PERFORMANCE | in attesa decisione supervisore |
| NB-6 | D-1 reinterpretato senza ratifica Planner | NEUTRO | NO |
| O-1 | Banner manifest doppi spazi vs Cap.46 | NEUTRO | NO |
| O-2 | DSTX50 e DFRA dichiarati atteso senza verifica empirica | NEUTRO | NO |

---

## Verifica criteri PASS (dal task card)

| # | Criterio PASS | Esito |
|---|----------|-------|
| 1 | Input autoritativi presenti verbatim | OK (banner, comandi, schemi, codici errore, 100gg, rate-limit, conflitto DGo tutti citati) |
| 2 | Tabella mappatura DAPI -> bundle frozen completa, no trasformazioni non specificate | FAIL (B-2, B-3, B-7) |
| 3 | Decisione Q-A chiusa con verdetto + motivazione + PERIMETRO vincolante | FAIL (B-5: gating sospende invio, identico a Q-A-2 scartato) |
| 4 | Vincolo D-6 esplicitato come regola normativa | OK (Cap.46 + Cap.50) |
| 5 | Warm-up stati condizionali specificato | PARZIALE (Cap.51 formalizzato ma L_warmup non congelato NB-4 e fallback Portara dipende da riconciliazione fuori scope B-6) |
| 6 | Coerenza con CAP-DATA-01 sez.3.4 (gap semantics, bar_synthetic) | FAIL (B-3 regola non applicabile al FIB; B-2 mappatura non verificabile) |
| 7 | Nessuna pretesa che PHASE-2 cross-index sia coperta da DAPI | OK |
| 8 | I 6 Gap chiusi | OK formalmente; Gap-3 intercala con B-6 |
| 9 | Nessuno sconfinamento in CAP-DATA-03 | OK formalmente; Cap.51 lo richiede di fatto (B-6) creando dipendenza circolare |

---

## Sintesi

Il capitolo presenta struttura ben strutturata e formalmente completa, ma introduce 7 BUG REALI che impattano direttamente il comportamento del GA in produzione: regole chiusura segnali in contraddizione con state machine (B-1), schema format CSV runtime non simmetrico al bundle frozen (B-2, B-3, B-4), gating qualitativo come gate di pubblicazione (B-5), warm-up fallback Portara dipende da riconciliazione fuori scope (B-6), dominio tick_count divergente (B-7). I primi 5 problemi distorcono in modo misurabile la conversione signal-to-trade live e il ranking dei cromosomi rispetto al ranking calibrato in walk-forward.

FAIL. Development deve correggere i BUG REALI ratificati dal supervisore prima che il Planner approvi.
