# Re-Review AUDIT-RM-RETRO CAP-DATA-02 (Parte 9) — Iterazione 3 — verifica chiusura 9 finding

**Sede**: WEB
**Natura**: Re-Review Iter.3 — verifica di chiusura dei 9 finding approvati dopo il rework Iter.2 del Developer (NON CAP-review piena; NON probe-review standard — è la re-review formale opzione B prevista da `tasks/ACTIVE_TASK.md` §RM-4 per le patch su A/C in Iterazione 2, criterio (b) di `CLAUDE.md`).
**Commit base auditato (HEAD post-rework)**: `dd36f97` (origin/main). Rework consegnato nei commit `9242135` (patch A+C), `6b9ea91` (report ridotto), `dd36f97` (DEV_STATUS = READY_FOR_REVIEW). Review v1 FAIL: `f6d2ac3`. Task card Planner: `f7d9b22`.
**Ruolo Reviewer assunto da agente general-purpose** (subagente nativo `reviewer` non disponibile nell'ambiente; ruolo adottato in pieno secondo `.claude/agents/reviewer.md`, incluse regole assolute, sezione "Probe-review (RM-4)" e divieti per sede `:163-164`).

**Perimetro auditato (mappatura A-D)**:
- A = `docs/methodology_v2/CAP_09_parte_9.md` (patchato dal rework)
- B = `reports/REPORT_CAP_09.md` (NON toccato — report storico immutabile; finding #8 vive nel report ridotto)
- C = `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md` (patchato dal rework)
- D = `scripts/export_directa_history_parametric.py` (decoder canonico, fonte CODICE-ESISTENTE level-2 — NON modificabile, NON modificato)

**Cross-reference fuori perimetro (citate, NON auditate)**:
- `reports/REPORT_AUDIT_RM_RETRO_CAP_DATA_02.md` — report ridotto del Developer (mappatura finding→patch + self-review RM-4 opzione A), letto come dichiarazione dell'autore ma verificato indipendentemente contro i file.
- `tasks/STATO_CORRENTE.md` §5 — M-1/M-3/M-4/M-5 come `[PROVA-EMPIRICA 2026-05-29]` acquisite tramite M-promemoria (forma versionata della prova), NON ispezionate direttamente (dump `probe_out/*` locali non versionati, sede CLI).

---

## VERDETTO: PASS (Sede: WEB)

**PASS sede WEB; lista Empirico-CLI non vuota (7 voci) → handoff CLI separato.**

**Motivazione sintetica.** Tutti e 9 i finding approvati dal supervisore (#1,#2,#3,#4,#5,#6,#7,#8,#10) sono **CHIUSI** con verifica indipendente file:linea. Il check critico W1 (schema CANDLE) è risolto correttamente: A Cap.49 `:167-171` ora mappa `bar_open←campo 8 (APE)`, `bar_high←campo 7 (MAX)`, `bar_low←campo 6 (MIN)`, `bar_close←campo 5 (UFF)`, `volume←campo 9 (qty)` — coerente bit-a-bit con il decoder canonico D `:471` + `:477-481`. Il blocco RM-1 a 4 righe (`:158-161`) è nel formato esatto `METODO.md:28-33`. Il **secondo giro ostile non ha trovato alcun residuo non etichettato** dello schema invertito `O;H;L;C` in A o C: gli unici riscontri sono interni ai blocchi correttivi (etichettati `[CORREGGE WIKI]` / `[WIKI-HINT, dimostrato INESATTO]`). Nessuna regressione introdotta dal rework. La regola di non-cancellazione è rispettata (testo originale etichettato, non rimosso) verificata sul diff `9242135`. Restano SOLO voci empiriche in lista CLI (7), che per il divieto `reviewer.md:163` non si chiudono in sede WEB e vanno in handoff alla sede CLI.

---

## Esito di chiusura per ciascuno dei 9 finding approvati

Legenda esito: **CHIUSO** = patch applicata come da mandato, nessuna nuova violazione RM-1, non-cancellazione rispettata. **NON CHIUSO** = patch assente/parziale. **REGRESSIONE** = la patch introduce un nuovo problema.

### Finding #1 — Schema CANDLE OHLC invertito (BUG REALE catastrofico) — **CHIUSO**

- **Mandato** (ACTIVE_TASK `:428`): correggere mappatura Cap.49 allo schema reale di D; `bar_open`←8(APE), `bar_high`←7(MAX), `bar_low`←6(MIN), `bar_close`←5(UFF); volume←9 invariato; etichette `[CODICE-ESISTENTE :477-481]`+`[PROVA-EMPIRICA M-1]`+`[CORREGGE WIKI]`.
- **Verifica indipendente (A post-patch)**: `docs/methodology_v2/CAP_09_parte_9.md`:
  - `:167`: `` | `bar_open` ($\mathrm{Open}_t$...) | numero (multiplo di 5pt) | `CANDLE` campo 8 (`APE` = open) `[CODICE-ESISTENTE export_directa_history_parametric.py:477-481]` `[PROVA-EMPIRICA M-1 2026-05-29]` `[CORREGGE WIKI]` | ... ``
  - `:168`: `` | `bar_high` ... | `CANDLE` campo 7 (`MAX` = high) `[CODICE-ESISTENTE ...:477-481]` `[CORREGGE WIKI]` | ``
  - `:169`: `` | `bar_low` ... | `CANDLE` campo 6 (`MIN` = low) `[CODICE-ESISTENTE ...:477-481]` `[CORREGGE WIKI]` | ``
  - `:170`: `` | `bar_close` ... | `CANDLE` campo 5 (`UFF` = close) `[CODICE-ESISTENTE ...:477-481]` `[PROVA-EMPIRICA M-1 2026-05-29]` `[CORREGGE WIKI]` | ``
  - `:171`: `` | `volume` ... | `CANDLE` campo 9 (`<V>` = qty) `[CODICE-ESISTENTE ...:471,482]` | ``
- **Verifica coerenza con D (canonico)** — confronto puntuale sulle 3 dimensioni richieste (AC-9, cosa intendo per "coerente"):
  - (a) **ordine dei 5 campi per posizione**: A `[5..9] = UFF;MIN;MAX;APE;V`; D `:471` `parts[4..8] = uff;min_;max_;ape;qty` → **COINCIDE**.
  - (b) **mapping posizione→OHLC**: pos5 A=close(UFF) / D `:478` `close_v=Decimal(uff)` → coincide; pos6 A=low(MIN) / D `:479` `low_v=Decimal(min_)` → coincide; pos7 A=high(MAX) / D `:480` `high_v=Decimal(max_)` → coincide; pos8 A=open(APE) / D `:481` `open_v=Decimal(ape)` → coincide; pos9 A=volume(qty) / D `:482` `volume_v=int(Decimal(qty))` → coincide. **Tutti e 5 coincidono.**
  - (c) **convenzione di indicizzazione**: A usa "campo 5..9" (1-indexed dal primo token `CANDLE`); D usa `parts[4..8]` (0-indexed) per gli stessi campi numerici. Campo 5 = `parts[4]` = primo numerico = UFF in entrambi. Le convenzioni di conteggio coincidono.
- **Blocco RM-1 4-righe** (`:158-161`): presente nel formato esatto `METODO.md:28-33`:
  - `:158` `VERIFICA:` enuncia il payload pos 5..9 = UFF;MIN;MAX;APE;V e il mapping bar_open←8/bar_high←7/bar_low←6/bar_close←5/volume←9.
  - `:159` `PROVE:` cita D `:471` + `:477-481` (testuale, `[CODICE-ESISTENTE]`) + M-1 (`[PROVA-EMPIRICA M-1 2026-05-29]`).
  - `:160` `ALTERNATIVE COMPATIBILI ESCLUSE:` enumera l'ordine wiki `O;H;L;C` (escluso da V-1) + `[CORREGGE WIKI: dimostrato inesatto]`.
  - `:161` `ALTERNATIVE COMPATIBILI NON ESCLUSE: nessuna.`
  - Le 4 etichette di riga (`VERIFICA / PROVE / ALTERNATIVE COMPATIBILI ESCLUSE / ALTERNATIVE COMPATIBILI NON ESCLUSE`) sono nell'ordine e nella forma di `METODO.md:28-33`. **Formato conforme.** Poiché "ALTERNATIVE NON ESCLUSE = nessuna", la dichiarazione "verificata piena" è legittima (base level-2 D + level-1 M-1).
- **Non-cancellazione**: il diff `9242135` (linee 118-122 vecchie → 123-127 nuove) mostra che le righe sono state **riscritte in loco** correggendo il mapping; il testo errato non sopravvive come fatto (per costruzione la riga corretta sostituisce la mappatura sbagliata). La memoria dell'errore è preservata nel blocco RM-1 `:160` (`ALTERNATIVE ESCLUSE: ordine wiki O;H;L;C`) e nella nota `:155-156` (`[CORREGGE WIKI]`). Questo è il trattamento corretto per un valore di codice errato (non si "conserva il valore sbagliato come hint": si conserva la **traccia dell'errore escluso**).
- **Nuove violazioni RM-1**: nessuna. La dichiarazione è in formato 4-righe; le etichette di fonte sono presenti su ogni riga della tabella.
- **Esito**: **CHIUSO.**

### Finding #2 — C dichiara schema wiki `O;H;L;C` come "documentato" (BUG REALE RM-3) — **CHIUSO**

- **Mandato** (ACTIVE_TASK `:429`): etichettare C `:28` e `:46` `[WIKI-HINT, dimostrato INESATTO su CANDLE: ordine reale C;L;H;O ...]`; NON cancellare il testo wiki.
- **Verifica indipendente (C post-patch)**: `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md`:
  - `:28`: la stringa wiki `CANDLE;<TICKER>;<yyyyMMdd>;<HH:mm:ss>;<O>;<H>;<L>;<C>;<V>` **conservata**, seguita da `` `[WIKI-HINT, dimostrato INESATTO su CANDLE: ordine reale C;L;H;O — vedi export_directa_history_parametric.py:477 e M-1 2026-05-29]` `` + chiarimento "le posizioni 5..8 del payload sono in realtà `UFF;MIN;MAX;APE` = `close;low;high;open` (testo wiki conservato, etichettato come hint smentito)".
  - `:46`: la stringa wiki `CANDLE;...;<Open>;<High>;<Low>;<Close>;<Volume>` **conservata**, seguita dalla stessa etichetta `[WIKI-HINT, dimostrato INESATTO ...]` + chiarimento.
- **Coerenza A↔C↔D sullo schema CANDLE**: A `:167-171` (mappatura reale `C;L;H;O;V`), C `:28`/`:46` (stringa wiki etichettata come hint smentito che rimanda a `:477` + M-1), D `:477-481` (canonico `C;L;H;O;V`). I tre concordano sull'ordine reale; C conserva la stringa wiki SOLO come hint dimostrato inesatto. **Nessuna divergenza non etichettata residua.**
- **Non-cancellazione**: rispettata (diff `9242135` linee 198→199 e 207→208: il `-`/`+` mostra che la riga è stata estesa con l'etichetta, la stringa wiki originale è interamente conservata nella riga `+`).
- **Esito**: **CHIUSO.**

### Finding #3 — Cooldown "~30s / 14ª connessione" come regola operativa, refutato da M-5 (BUG REALE RM-1 refutato) — **CHIUSO**

- **Mandato** (ACTIVE_TASK `:430`): riscrivere il cooldown come verifica parziale (osservazione singola 27/05 in burst non disambiguato; M-5 non osserva cooldown a ~1Hz; soglia/durata sotto burst >>1Hz non disambiguate); mantenere la regola architetturale "1 connessione persistente per porta".
- **Verifica indipendente (A post-patch)** — tre punti:
  - `:47` (Pattern socket persistente): *"Nello stesso probe, **in una singola osservazione del 2026-05-27 in regime di burst non disambiguato**, 14 connessioni TCP rapide ... `ConnectionRefusedError 10061` per circa 30 secondi. **Verifica parziale (RM-1): la cifra "14ª connessione / ~30 s" NON è una costante verificata.** Un ri-test empirico del 2026-05-29 (`[PROVA-EMPIRICA M-5 2026-05-29]`, 75 connessioni ... `onset_connection:null`) **non ha osservato alcun cooldown** nel regime ~1Hz ... soglia e durata sotto burst >>1Hz restano non disambiguate. La pipeline runtime adotta comunque il pattern **una singola connessione persistente per porta** ... questa è una **scelta architetturale prudente** indipendente dal cooldown ..."*.
  - `:51` (Rate-limit osservato): *"**Verifica parziale (RM-1):** nell'osservazione singola del 2026-05-27 (regime di burst non disambiguato) aperture TCP rapide oltre la 14ª ... cooldown di circa 30 s. Questa cifra **NON è una costante verificata**: il ri-test del 2026-05-29 ... **non ha osservato cooldown** nel regime ~1Hz; soglia e durata sotto burst >>1Hz restano non disambiguate ..."*.
  - `:212` (Backoff su perdita di connessione): *"... nell'osservazione singola del 2026-05-27, in regime di burst non disambiguato — vedi Cap.46: la soglia "14ª connessione" e la durata "~30 s" sono **verifica parziale**, non costanti, e nel regime ~1Hz nessun cooldown è stato osservato il 2026-05-29 `[PROVA-EMPIRICA M-5 2026-05-29]`) ..."*.
- **Regola architetturale mantenuta**: confermata in `:47` ("una singola connessione persistente per porta ... scelta architetturale prudente indipendente dal cooldown") e `:51`. Conserva la prudenza senza ancorarla alla cifra refutata. Corretto.
- **Nuove violazioni RM-1**: nessuna. La riscritta usa esplicitamente "Verifica parziale (RM-1)" e nomina l'evidenza che refuta (M-5) + le alternative non disambiguate (soglia/durata sotto burst >>1Hz). La forma "verifica parziale" è quella richiesta da RM-1 quando restano alternative non escluse.
- **Esito**: **CHIUSO.**

### Finding #4 — Semantica codici 1004/1007 in tabella normativa senza supporto (BUG REALE RM-1) — **CHIUSO**

- **Mandato** (ACTIVE_TASK `:431`): riscrivere 1004/1007 come "verifica parziale" con comando-trigger; marcare "semantica esatta da disambiguare"; nota che `is_error_line` di D non decodifica numerici → no level-2; Empirico-CLI per trigger esatti.
- **Verifica indipendente (A post-patch)**:
  - Premessa `:201` (nuovo paragrafo): *"**Verifica parziale (RM-1) sulla semantica numerica.** Il decoder di produzione `is_error_line` (`scripts/export_directa_history_parametric.py:417-425`) fa string-matching generico (...) e **NON decodifica i codici numerici**: non esiste quindi supporto di codice di produzione (level-2) per la *semantica* dei singoli codici. ... la **semantica esatta di ciascun codice resta da disambiguare** con comandi-trigger mirati a mercato aperto (Empirico-CLI)."*.
  - Intestazione colonna tabella `:203`: "Significato (verifica parziale — da disambiguare)".
  - `:205` (`1004`): *"... **Verifica parziale:** semantica derivata dal trigger; nessun supporto level-2 in `is_error_line`; semantica esatta da disambiguare (Empirico-CLI)."* + `[PROVA-EMPIRICA M-3 2026-05-29]`.
  - `:206` (`1007`): *"... **Verifica parziale:** semantica derivata dal trigger; nessun supporto level-2 in `is_error_line`; semantica esatta da disambiguare (Empirico-CLI)."* + `[PROVA-EMPIRICA M-3 2026-05-29]`.
- **Verifica RM-2 indipendente del Reviewer** su `is_error_line`: D `:417-425` (letto in CAP-DATA-01 e citato dal task `:367`) fa string-match generico, NON decodifica i numerici → la nota di A è corretta (no level-2 per la semantica numerica).
- **Coerenza intro**: il diff `9242135` (linea 143→144) mostra che l'intestazione del paragrafo è stata cambiata da "I codici **verificati** empiricamente il 2026-05-27 ... e il loro trattamento normativo" a "I codici sono stati **osservati** empiricamente ... e ri-auditati il 2026-05-29 `[PROVA-EMPIRICA M-3 2026-05-29]`". Igiene RM-1 corretta (da "verificati" a "osservati").
- **Nuove violazioni RM-1**: nessuna.
- **Esito**: **CHIUSO.**

### Finding #5 — Dominio codici errore incompleto vs M-3 (MIGLIORA PERFORMANCE) — **CHIUSO**

- **Mandato** (ACTIVE_TASK `:432`): estendere la tabella con `1017` (sintassi malformata), `1015` (data/parametro invalido, NUOVO), `1003` (comando storico su porta realtime, NUOVO) da M-3, con cautela RM-1.
- **Verifica indipendente (A post-patch)** — tabella codici `:203-210`:
  - `:207` (`1017`): aggiunto, *"Sintassi strutturale malformata. **Verifica parziale:** distinto empiricamente da 1015 ...; semantica esatta e confine con 1015 da disambiguare (Empirico-CLI)."* + `[PROVA-EMPIRICA M-3 2026-05-29]` (codice NON presente nella tabella originale).
  - `:208` (`1015`): aggiunto, *"Data/parametro invalido. **Verifica parziale:** NUOVO codice non presente nella tabella originale ...; confine con 1017 da disambiguare (Empirico-CLI)."* + `[PROVA-EMPIRICA M-3 2026-05-29]`.
  - `:209` (`1003`): aggiunto, *"Comando storico su porta realtime. **Verifica parziale:** NUOVO codice ...; da disambiguare (Empirico-CLI)."* + `[PROVA-EMPIRICA M-3 2026-05-29]`.
- **Confronto con M-3** (`tasks/STATO_CORRENTE.md` §5, `[PROVA-EMPIRICA 2026-05-29 via STATO_CORRENTE.md §5]`): M-3 elenca 1004/1007/1017/1015(nuovo)/1003(nuovo)/1030(non riprodotto). A `:205-210` ora copre tutti e 6 con la cautela richiesta. **Dominio completo rispetto a M-3.**
- **Bonus — finding #5 tocca anche 1030 (parte di W5)**: `:210` riscritto: *"... **Non riprodotto** sul perimetro account `B6086` (`[PROVA-EMPIRICA M-3 2026-05-29]`: l'IDEM è incluso nel servizio base, 1030 non osservato) → semantica derivata/attesa, non verificata sul FIB."* — coerente con M-3 (1030 non riprodotto) e già RM-1-conforme (non dichiara 1030 "verificato").
- **Nuove violazioni RM-1**: nessuna (ogni codice nuovo è marcato "Verifica parziale" + Empirico-CLI).
- **Esito**: **CHIUSO.**

### Finding #6 — Riavvio Darwin mezzanotte appoggiato a wiki-only (MIGLIORA PROCESSO) — **CHIUSO**

- **Mandato** (ACTIVE_TASK `:433`): etichettare `[WIKI-HINT, da verificare]`; marcare "da osservare empiricamente" (Empirico-CLI); non bloccante.
- **Verifica indipendente (A post-patch)**: `:221` (Gap-3): *"Il gateway Darwin esegue manutenzione automatica giornaliera circa a mezzanotte locale `[WIKI-HINT, da verificare]` (documentato dal wiki DAPI, **da osservare empiricamente** — Empirico-CLI: osservazione passiva di una sessione cross-midnight ...; nessuna corroborazione level-1/2 ad oggi, il wiki Directa è dimostrato inesatto sullo schema CANDLE e va trattato come hint anche qui), interrompendo le connessioni attive ... È una contingenza di recovery operativo, non uno schema-dato che alimenta il bundle."*.
- **RM-3**: etichetta `[WIKI-HINT, da verificare]` presente; la conclusione è esplicitamente marcata "nessuna corroborazione level-1/2 ad oggi" e "da osservare empiricamente" → non più una conclusione wiki-only presentata come fatto, ma un hint da verificare. Corretto.
- **Esito**: **CHIUSO.**

### Finding #7 — Schema BOOK_5 da osservazione singola + regola bar_synthetic su posizioni non certificate (MIGLIORA PERFORMANCE) — **CHIUSO**

- **Mandato** (ACTIVE_TASK `:434`): annotare che lo schema BOOK_5 deriva da osservazione singola 27/05, alternative non escluse (ordine BID/ASK, indice lots/price); la regola `bar_synthetic` dipende da `bid1_lots`/`ask1_lots` non certificate → Empirico-CLI. Punti `:93`, `:164`, `:168`.
- **Verifica indipendente (A post-patch)**:
  - `:93` (Cap.47, schema BOOK_5): *"**Verifica parziale (RM-1): lo schema BOOK_5 deriva da una singola osservazione del 2026-05-27** (un solo evento FIB6I) e non è corroborato dal decoder canonico (D non parsa BOOK_5). Alternative compatibili **non escluse**: ordine dei blocchi BID/ASK (potrebbe essere invertito — nel campione `bid1_price=49715.0` risulta maggiore di `ask1_price=49275.0`, anomalo ..., plausibilmente perché contratto a scadenza lontana ma non disambiguato), indice del triplo `lots`/`orders`/`price` per livello. La struttura va disambiguata con cattura di ≥N eventi `BOOK_5` su FIB front-month liquido (Empirico-CLI)."*.
  - `:173` (cella tabella `bar_synthetic`, Cap.49): *"**(Verifica parziale RM-1:** questa regola dipende dalle posizioni `bid1_lots`/`ask1_lots`/`bid1_price`/`ask1_price` nello schema `BOOK_5`, **non certificate** ...; se l'ordine dei livelli o l'indice del triplo fosse diverso, la regola si applicherebbe su campi sbagliati → Empirico-CLI.)"*.
  - `:177` (bullet sintesi `bar_synthetic`, Cap.49): *"(**Verifica parziale RM-1:** dipende dalle posizioni `bid1_lots`/`ask1_lots` dello schema `BOOK_5`, non certificate ... → Empirico-CLI.)"*.
  - Nota: il mandato citava `:164`/`:168` (numerazione pre-patch); l'inserimento del blocco RM-1 a `:155-162` ha spostato le righe target a `:173`/`:177`. La sostanza richiesta è applicata sulle righe corrette (cella tabella + bullet sintesi). Mappatura di riga corretta.
- **Verifica RM-2 indipendente**: D non parsa BOOK_5 (D `:467-496` parsa solo CANDLE) → l'affermazione "non corroborato dal decoder canonico" è corretta.
- **Nuove violazioni RM-1**: nessuna (le annotazioni sono in forma "Verifica parziale" con alternative non escluse nominate).
- **Esito**: **CHIUSO.**

### Finding #8 — B vouchera per tabella Cap.49 errata; AC-3/AC-4 verificano completezza non correttezza mapping (MIGLIORA PROCESSO) — **CHIUSO (via annotazione, B non editato)**

- **Mandato** (ACTIVE_TASK `:435`): annotare nel report ridotto che la verifica AC-3/AC-4 di B va estesa a "mapping CANDLE verificato contro il decoder canonico D"; il REPORT originale `reports/REPORT_CAP_09.md` resta storico immutabile.
- **Verifica indipendente**:
  - `reports/REPORT_AUDIT_RM_RETRO_CAP_DATA_02.md` §3 (`:45-51`): annotazione presente — *"la verifica AC-3/AC-4 di B avrebbe dovuto essere estesa a 'mapping CANDLE verificato contro il decoder canonico di produzione D (export_directa_history_parametric.py:477-481)', non solo 'tabella completa per TUTTI i campi'. Per i futuri AC che dichiarano la correttezza di uno schema-dato di un sistema esterno, il criterio di verifica deve includere il confronto puntuale con il decoder di produzione esistente (RM-2) ..."* + vincolo "reports/REPORT_CAP_09.md ... **NON è stato editato.**".
  - **B non editato**: confermato dal diff `9242135` (solo A e C nel commit; `REPORT_CAP_09.md` assente dal diff) e dal report ridotto §1 (`:4`) che dichiara B fra i NON toccati.
- **Esito**: **CHIUSO** (annotazione nel sede corretta; vincolo immutabilità B rispettato).

### Finding #10 — Etichette di livello fonte RM-3 assenti dove la sostanza regge (MIGLIORA PROCESSO) — **CHIUSO**

- **Mandato** (ACTIVE_TASK `:436`): aggiungere etichette `[CODICE-ESISTENTE]`/`[PROVA-EMPIRICA]`/`[WIKI-HINT]` dove la sostanza regge (W4/W6/W7/W10).
- **Verifica indipendente (A post-patch)**:
  - **W4 (CANDLERANGE)**: `:254` step 2 warm-up — *"`CANDLERANGE ... 60` (sintassi con `period_s` in ultima posizione `[CODICE-ESISTENTE export_directa_history_parametric.py:228-230]`)"*. Etichetta presente + verifica RM-2: D `:228-230` emette `CANDLERANGE {symbol} {start} {end} {period_seconds}` (period last) → corroborazione corretta.
  - **W6 (mese F/I)**: `:61` — `I=settembre` `[PROVA-EMPIRICA 2026-05-27 Appendice B.2]` + `F=giugno` `[PROVA-EMPIRICA M-4 2026-05-29]`; "Mar/Dic ancora da decodificare ... verifica parziale, Empirico-CLI". Etichette presenti; coerente con M-4.
  - **W7 (100gg)**: `:249` — *"limite **100 giorni intraday** del DAPI `[CODICE-ESISTENTE export_directa_history_parametric.py:61 (DEFAULT_INTRADAY_MAX_DAYS=100)]` `[PROVA-EMPIRICA 2026-05-27 Appendice A.2: query 150gg → first_timestamp ~100gg prima]`"*. Etichette presenti; verifica RM-2: D `:61` `DEFAULT_INTRADAY_MAX_DAYS = 100` (citato dal task `:368`) → corroborazione corretta.
  - **W10 (banner)**: `:29` — banner `[PROVA-EMPIRICA 2026-05-27 Appendice A]` + nota prefix-match + "variazione ... da osservare empiricamente (Empirico-CLI minore)". Etichetta presente.
  - **C**: l'etichettatura RM-3 di C è coperta da #2 (`:28`/`:46` etichettate `[WIKI-HINT ...]`).
- **Esito**: **CHIUSO.**

---

## Secondo giro ostile — caccia ai residui dello schema invertito

**Domanda esplicita**: "Sono sicuro che non ci sia un secondo punto con lo schema invertito `O;H;L;C` dichiarato come fatto e non etichettato, ALTROVE in A o C?"

**Grep eseguiti (sede WEB)** su A e C:

```
# Giro 1 — pattern larghi
grep -n "O;H;L;C|<O>;<H>|<O>;|;<O>;|Open.*High.*Low.*Close|Open;High;Low;Close|campo 5.*Open|campo 5.*<O>|campo 6.*High|campo 8.*Close|campo 8.*<C>"  CAP_09_parte_9.md
grep -n "O;H;L;C|<O>;<H>|<O>;|;<O>;|Open.*High.*Low.*Close|Open;High;Low;Close|campo 5.*Open|campo 5.*<O>|campo 8.*<C>"  INDAGINE_DIRECTA_CROSS_INDEX.md

# Giro 2 — pattern stretti sul mapping payload
grep -n "<O>;<H>;<L>;<C>|;<O>;|campo 5.*<O>|campo 6.*<H>|campo 7.*<L>|campo 8.*<C>|UFF;MIN;MAX;APE|APE.*MAX.*MIN.*UFF"  CAP_09_parte_9.md
grep -n "CANDLE;<TICKER>|CANDLE campo|campo 5|campo 8"  INDAGINE_DIRECTA_CROSS_INDEX.md

# Giro 3 — nuove asserzioni "verificato" potenzialmente regressive
grep -n "verificat[oi] empiricament|ha confermato|ha verificato|verificato che|confermato che"  CAP_09_parte_9.md
```

**Esito — residui dello schema invertito: NON TROVATI.** Tutte le occorrenze di `<O>;<H>;<L>;<C>` / `Open;High;Low;Close` in A e C sono **interne ai blocchi correttivi ed etichettate**:

| file:linea | Contesto | Etichettato? |
|---|---|---|
| A `:155-156` | nota "Mappatura schema CANDLE — corretta 2026-05-30 ... **non** l'ordine `<O>;<H>;<L>;<C>` dichiarato dal wiki ... dimostrato inesatto" | SÌ — testo correttivo, dichiara l'ordine wiki come errato |
| A `:160` | blocco RM-1 `ALTERNATIVE COMPATIBILI ESCLUSE: ordine wiki O;H;L;C — escluso da V-1 ... [CORREGGE WIKI: dimostrato inesatto]` | SÌ — alternativa esplicitamente esclusa |
| C `:28` | stringa wiki `...;<O>;<H>;<L>;<C>;<V>` + `[WIKI-HINT, dimostrato INESATTO su CANDLE: ordine reale C;L;H;O ...]` | SÌ |
| C `:46` | stringa wiki `...;<Open>;<High>;<Low>;<Close>;<Volume>` + `[WIKI-HINT, dimostrato INESATTO su CANDLE ...]` | SÌ |

**Controllo dei luoghi specifici richiesti dal mandato**:
- **Cap.45 (premessa/collocazione, A `:11-21`)**: nessuna tabella o esempio di payload CANDLE; cita "OHLCV" e "schema dati" in astratto (`:17`), nessun ordine posizionale di campi. Nessun residuo.
- **Cap.48 (format dati canonico, A `:111-147`)**: gli esempi CSV `:121-122` usano l'header **a colonne etichettate** `open,high,low,close,volume` (ordine di colonna del CSV di output, NON mapping posizionale del payload CANDLE). Questo è il formato di output simmetrico al bundle Portara (Parte 8 Cap.40), corretto e non in discussione. Il dominio `source` (`:131-138`) non tocca lo schema OHLC. Nessun residuo di mapping payload invertito.
- **Cap.27 PII**: Parte 9 cita "Parte VI Cap.27" come consumer della pipeline di inference (`:17`, `:191`, `:241`, `:267`) — nessuna tabella di schema CANDLE in questi riferimenti (Cap.27 vive in un'altra Parte, fuori perimetro). Nessun residuo.
- **Cap.49 (mappatura, A `:151-191`)**: l'unico schema CANDLE normativo; corretto (#1 CHIUSO). La cella `bar_synthetic` `:173`/`:177` usa `bid1_price`/`ask1_price` (BOOK_5, non CANDLE) per il mid — corretto, annotato come verifica parziale (#7).
- **Cap.50 (codici errore, A `:195-241`)**: nessuno schema CANDLE; tabella codici errore (#4/#5 CHIUSI).

**Altre asserzioni "verificato empiricamente" trovate dal Giro 3 — NON sono regressioni del rework** (pre-esistenti, già valutate OK in v1; nessuna re-dichiara il fatto invertito/refutato):
- A `:90` "tre schemi principali, verificati empiricamente il 2026-05-27" — riferito alla **struttura** osservata di ANAG/BOOK_5/PRICE (datata, level-1); il rework `:93` ha aggiunto il caveat "Verifica parziale (RM-1)" per BOOK_5 (#7). L'interpretazione dei campi medi resta in lista CLI (W2). Accettabile.
- A `:419` / `:440` (tabella decisioni D-9-4) e `:249` "`I=settembre` verificato empiricamente 2026-05-27" — level-1 (ANAG ISIN+descrizione), confermato da M-4; v1 review W6 = OK (RM-1 conforme). Non regressione.
- A `:53` "regola operativa ... verificata empiricamente: singola connessione persistente" — riferito alla regola dei 26 comandi sequenziali (osservata), NON alla cifra cooldown refutata. Accettabile.

**Conclusione secondo giro**: nessun residuo `O;H;L;C` non etichettato; nessuna regressione introdotta dal rework. Il rework è **completo** sul perimetro dei 9 finding.

---

## Check RM-2 — grep decoder esistenti (verifica indipendente del Reviewer)

**Grep eseguito (sede WEB)** + lettura diretta di D `:460-503`:

```
grep -n  su export_directa_history_parametric.py :460-504  (parse_directa_candle)
```

**Decoder/parser DAPI nel repo per schema CANDLE** (formato `METODO.md:64-71`):

| path:linea | Cosa decodifica | Schema dichiarato | Ruolo |
|---|---|---|---|
| `scripts/export_directa_history_parametric.py:467-496` (`parse_directa_candle`) | record `CANDLE` storico | `:471` `parts[4..8] = uff;min_;max_;ape;qty`; `:477-481` `UFF→close, MIN→low, MAX→high, APE→open` = **`C;L;H;O;V`** | **CANONICO level-2** (fonte di verità di codice, NON modificato) |
| `scripts/export_directa_history_parametric.py:228-230` | emissione `CANDLERANGE` | `CANDLERANGE {sym} {start} {end} {period_s}` (period LAST) | level-2 per #10 W4 (citato in A `:254`) |
| `scripts/export_directa_history_parametric.py:417-425` (`is_error_line`) | rilevamento errori | string-match generico, **NON decodifica codici numerici** | level-2 per #4/#5 (semantica numerica NON corroborata — citato in A `:201`) |
| `scripts/export_directa_history_parametric.py:61` | costante limite intraday | `DEFAULT_INTRADAY_MAX_DAYS = 100` | level-2 per #10 W7 (citato in A `:249`) |
| `scripts/probe_dapi.py` (ramo CANDLE, post-fix `a12ae32`) | record `CANDLE` realtime | concorde con D su `C;L;H;O;V` | level-2 di supporto (già auditato CAP-DATA-01 PASS, NON oggetto qui) |

**Conclusione RM-2**: confermo che **nessun codice di produzione dichiara `O;H;L;C`**. Il decoder canonico D NON è stato modificato dal rework (assente dal diff `9242135`; confermato dal report ridotto §1 e §"Grep RM-2"). La correzione di #1/#2 è **solo testuale** (allineamento di A e C al decoder canonico), come atteso. A `:167-171` ora coincide con D su tutte e 5 le dimensioni posizione→campo.

---

## Check RM-3 — fonti esterne (verifica post-patch)

| Riferimento | file:linea | Livello | Etichetta post-patch | Conclusione wiki-only residua? |
|---|---|---|---|---|
| wiki Directa (schema CANDLE) | A `:155-156`, `:160`; C `:28`, `:46` | 4 (dimostrato INESATTO) | SÌ — `[CORREGGE WIKI]` (A) / `[WIKI-HINT, dimostrato INESATTO]` (C) | NO — schema reale ora ancorato a D level-2 + M-1 level-1 |
| wiki Directa (riavvio mezzanotte) | A `:221` | 4 | SÌ — `[WIKI-HINT, da verificare]` + "da osservare empiricamente" | NO — marcato hint da verificare (non più fatto wiki-only) |
| wiki Directa (limite 100gg) | A `:249` | 4 | SÌ — `[CODICE-ESISTENTE :61]` + `[PROVA-EMPIRICA 2026-05-27 App. A.2]` | NO — corroborato level-1 + level-2 |
| CANDLERANGE period last | A `:254` | — | SÌ — `[CODICE-ESISTENTE :228-230]` | NO — corroborato level-2 |
| mese F/I | A `:61` | 1 | SÌ — `[PROVA-EMPIRICA 2026-05-27 App. B.2]` + `[PROVA-EMPIRICA M-4 2026-05-29]` | NO — level-1 |
| banner Darwin | A `:29` | 1 | SÌ — `[PROVA-EMPIRICA 2026-05-27 App. A]` | NO — level-1 (release trattata come variabile) |

**Esito RM-3**: le due conclusioni wiki-only critiche della v1 (schema CANDLE, riavvio mezzanotte) sono ora etichettate correttamente. Nessuna conclusione del perimetro patchato si appoggia a livello 4 senza supporto level 1-3 o senza etichetta di "hint da verificare".

---

## Check 4 — onestà mappatura claim→evidenza (post-patch)

| Asserzione | Evidenza puntuale post-patch | Esito |
|---|---|---|
| Schema CANDLE (A `:167-171`) | D `:471,:477-481` + M-1, nel blocco RM-1 `:158-161` | **OK** (verifica piena, alternative escluse = nessuna) |
| Cooldown (A `:47,:51,:212`) | M-5 (refuta a ~1Hz); osservazione 27/05 in burst non disambiguato | **OK** (verifica parziale dichiarata) |
| Codici 1004/1007 (A `:205,:206`) | trigger osservato + `[PROVA-EMPIRICA M-3]`; nota no-level-2 `is_error_line` | **OK** (verifica parziale dichiarata) |
| Codici 1017/1015/1003 (A `:207-209`) | `[PROVA-EMPIRICA M-3 2026-05-29]` | **OK** (verifica parziale dichiarata) |
| 1030 (A `:210`) | "non riprodotto sul FIB B6086" `[PROVA-EMPIRICA M-3]` | **OK** (non dichiarato verificato) |
| BOOK_5 (A `:93,:173,:177`) | osservazione singola 27/05; D non parsa BOOK_5 | **OK** (verifica parziale dichiarata) |
| mese F/I (A `:61`) | ANAG ISIN+descrizione `[PROVA-EMPIRICA]` + M-4 | **OK** (level-1) |
| banner (A `:29`) | probe 27/05 datato `[PROVA-EMPIRICA]` | **OK** (level-1) |

Nessuna asserzione "in aria" residua nel perimetro patchato.

---

## Empirico-CLI da verificare (lista NON vuota — handoff alla sede CLI)

In coerenza con il divieto `reviewer.md:163` (il Web reviewer NON dichiara "verificato empiricamente" niente che richieda DAPI live o filesystem locale), le seguenti asserzioni restano marcate per follow-up CLI. **Non sono finding di rework non chiusi**: sono asserzioni che richiedono prova DAPI diretta, già correttamente marcate "verifica parziale" + "Empirico-CLI" nei file patchati. **NB**: lo schema CANDLE (W1) e la sua radice in C (W13) NON sono in questa lista — sono risolti staticamente dal confronto con D (level-2) e M-1 (level-1), non richiedono ulteriore prova DAPI.

| W-N | Asserzione | File:linea (post-patch) | Test minimo proposto (CLI, DAPI live) |
|-----|-----------|------------------------|----------------------------------------|
| W2 | interpretazione campi medi `PRICE` 5/6/7 (`<volume_lot?>;<bid_qty?>;<ask_qty?>`) | A `:94`; C `:399` | catturare ≥N tick PRICE su DGER/DITAS e confrontare i campi 5/6/7 con book/volume noti per disambiguare il significato |
| W3 | schema BOOK_5 bit-a-bit (ordine BID/ASK, indice lots/orders/price, anomalia bid>ask del campione) | A `:93`, `:173`, `:177`; C `:375`/B.2 | SUB FIB front-month liquido, leggere ≥N eventi BOOK_5, verificare `bid1_price < ask1_price`, l'ordine dei 5 livelli BID/ASK e la posizione di lots/orders/price |
| W5 | semantica/trigger esatti codici 1004/1007 + confini 1017/1015/1003 | A `:205-209`; M-3 | inviare comandi-trigger (INFO/HELP su 10001; CANDLERANGE malformata su 10003 con ≥2 permutazioni; comando storico su 10001; SUB non sottoscritto) e registrare codice+dump:timestamp; disambiguare 1017 vs 1015 vs 1003 |
| W5/1030 | semantica 1030 su un ticker che richiede market data a pagamento | A `:210`; M-3 | (fuori perimetro FIB; cross-index PHASE-2) SUB di un ticker Eurex/CME non abilitato e registrare il codice |
| W6 | mese IDEM Mar/Dic + codice di `FIB6L` | A `:61`, `:96`; M-4 | SUB ticker trimestrale Mar/Dic + `FIB6L`, leggere ANAG (ISIN+descrizione) per decodificare i codici mese |
| W8 | riavvio Darwin mezzanotte (fenomeno) | A `:221` | osservazione passiva di una sessione cross-midnight: catturare disconnessione + re-handshake + timestamp |
| W9 | soglia/durata cooldown sotto burst >>1Hz | A `:47`, `:51`, `:212`; M-5 | ripetere il test M-5 con burst di apertura/chiusura socket a frequenza crescente (>>1Hz) per disambiguare se esiste una soglia e a quale frequenza/conteggio scatta |
| W10 | variazione banner per release Darwin diverse | A `:29` | catturare il banner su eventuali release Darwin diverse per confermare che solo il campo `Release ...` varia |

(8 voci. Tutte erano già nella lista CLI della v1 — nessuna è stata aggiunta dal rework; la 1030 è esplicitata come sotto-voce di W5. Per `reviewer.md:163` queste NON si chiudono in WEB: handoff alla sede CLI in sessione separata, secondo `tasks/ACTIVE_TASK.md` §"Iterazione 4".)

---

## Verdetto motivato

Il rework Iter.2 del Developer ha chiuso **tutti e 9 i finding approvati** (#1,#2,#3,#4,#5,#6,#7,#8,#10) con patch chirurgiche nei soli file del perimetro A e C, lasciando D (decoder canonico) e B (report storico) intatti. Ho verificato ciascun finding **indipendentemente** (citazione file:linea mia, non fidandomi del report del Developer), e ho ri-eseguito il confronto critico A↔D sullo schema CANDLE.

Il **cuore dell'audit (W1: schema CANDLE)** è risolto correttamente: A Cap.49 `:167-171` mappa ora `bar_open←campo 8 (APE=open)`, `bar_high←campo 7 (MAX=high)`, `bar_low←campo 6 (MIN=low)`, `bar_close←campo 5 (UFF=close)`, `volume←campo 9 (qty)`, coincidente su tutte e 5 le dimensioni posizione→campo con il decoder canonico D `:471` + `:477-481`. Il blocco RM-1 a 4 righe (`:158-161`) è nel formato esatto `METODO.md:28-33` con "ALTERNATIVE NON ESCLUSE: nessuna", che legittima la dichiarazione "verificata piena" (base level-2 D + level-1 M-1). La radice della contaminazione in C (`:28`/`:46`) è etichettata `[WIKI-HINT, dimostrato INESATTO]` con la stringa wiki conservata, non cancellata. I due pattern d'errore ereditati da CAP-DATA-01 — W9 cooldown (refutato da M-5) e W5 codici errore (senza level-2) — sono riscritti in forma "verifica parziale" corretta (#3, #4), con il dominio codici esteso e completo rispetto a M-3 (#5). Le etichette di livello fonte (#10) sono coerenti col livello reale della fonte.

Il **secondo giro ostile obbligatorio** ha cercato attivamente un secondo punto con lo schema invertito `O;H;L;C` dichiarato come fatto e non etichettato, in Cap.45/48/49/50, nelle tabelle CSV, nei riferimenti a Cap.27, e con grep larghi e stretti su A e C: **nessun residuo non etichettato trovato.** Le sole occorrenze sono interne ai blocchi correttivi ed esplicitamente marcate. Gli esempi CSV di Cap.48 (`:121-122`) usano l'ordine di colonna `open,high,low,close` come header di output etichettato (formato simmetrico al bundle Portara), che è cosa distinta dal mapping posizionale del payload CANDLE e non è in discussione. Le restanti asserzioni "verificato empiricamente" trovate nel file sono pre-esistenti, già valutate OK in v1, e nessuna re-dichiara il fatto invertito o il fatto refutato.

Non ho introdotto né rilevato **regressioni**. La regola di non-cancellazione è rispettata (verificata sul diff `9242135`). Il working tree è pulito sul perimetro A/B/C/D (gli unici file dirty pre-esistenti sono `.claude/settings.json` e `.claude/scheduled_tasks.lock`, estranei al perimetro). D non è stato toccato.

La **lista "Empirico-CLI da verificare" è non vuota (8 voci)**: per il divieto `reviewer.md:163` e per il criterio AC-13(d) del task card, queste asserzioni empiriche NON si chiudono in sede WEB. Lo scope WEB del rework è però **interamente chiuso**: i 9 finding sono saldati, nessun residuo schema invertito, nessuna regressione. Dichiaro quindi **PASS sede WEB; lista Empirico-CLI non vuota → handoff CLI separato** (sessione CLI di follow-up secondo `tasks/ACTIVE_TASK.md` §"Iterazione 4", che NON è parte del perimetro temporale di questa Re-Review).

**Riepilogo chiusura**: 9/9 finding CHIUSI (4 BUG REALI: #1 catastrofico, #2, #3, #4; 2 MIGLIORA PERFORMANCE: #5, #7; 3 MIGLIORA PROCESSO: #6, #8, #10). 0 NON CHIUSI. 0 REGRESSIONI. Residui schema invertito: 0. Lista Empirico-CLI: 8 voci (invariata rispetto a v1, handoff CLI).

---

## Applicazione RM a sé stesso (AC-9/10/11)

- **RM-1 (AC-9)**: la mia asserzione "A Cap.49 `:167-171` è coerente con D `:471,:477-481`" è verificata enumerando le 3 dimensioni cercate (ordine dei 5 campi per posizione; mapping posizione→OHLC per ciascuna pos 5/6/7/8/9; convenzione di indicizzazione di colonna) e dichiarando per ciascuna l'esito (Finding #1, blocco "Verifica coerenza con D"). Non ho dichiarato "coerente/chiuso" senza enumerare cosa ho confrontato. Per le asserzioni empiriche che richiedono DAPI (W2/W3/W5-trigger/W6-MarDic/W8/W9-burst/W10) NON ho dichiarato verificato/falsificato: le ho marcate Empirico-CLI in handoff alla sede CLI. Per W1/W13 dichiaro "chiuso staticamente" con base level-2 (D) + level-1 (M-1), entrambe acquisite senza accesso DAPI — legittimo in sede WEB.
- **RM-2 (AC-10)**: il grep su `export_directa_history_parametric.py` (parse_directa_candle `:460-504`) è stato eseguito direttamente e i decoder esistenti sono elencati con path:linea (Check RM-2). Ho verificato indipendentemente che NESSUN codice di produzione dichiara `O;H;L;C` e che D NON è stato modificato dal rework (assente dal diff `9242135`). Nessuna conclusione su "decoder esistenti" senza grep/lettura diretta.
- **RM-3 (AC-11)**: ogni finding cita file:linea testuale (post-patch) verificato di persona, non parafrasato dal report del Developer. I riferimenti a M-1/M-3/M-4/M-5 sono etichettati `[PROVA-EMPIRICA 2026-05-29 via STATO_CORRENTE.md §5]`; i riferimenti a D come `[CODICE-ESISTENTE r.NNN]`; il wiki come `[WIKI-HINT, dimostrato inesatto]`. I dump `probe_out/*` NON sono stati ispezionati (citati solo tramite M-3/M-5, forma versionata).
- **AC-12**: nessun file del perimetro A-D modificato da me; nessun file del repo modificato eccetto questo file di review. Working tree pulito su A/B/C/D. D (decoder canonico) NON toccato.

---
PASS: nessun problema bloccante (osservazioni minori ammesse) — **RAGGIUNTO sullo scope WEB**.
CONDITIONAL: solo problemi non bloccanti — non applicabile (nessun finding aperto).
FAIL: almeno un problema bloccante — non applicabile.

**VERDETTO: PASS sede WEB (9/9 finding chiusi, 0 regressioni, 0 residui schema invertito) + lista Empirico-CLI non vuota (8 voci) → handoff CLI separato.**
