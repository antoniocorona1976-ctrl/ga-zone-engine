# Review AUDIT-RM-RETRO CAP-DATA-01 (Parte 8) — perimetro A-D

**Sede**: WEB
**Natura**: audit retroattivo RM-1/2/3 + coerenza script↔testo (NON CAP-review piena — Parte 8 è già PASS storico hash `015c47a`; NON probe-review standard — qui si auditano simultaneamente 1 CAP storico + 3 output non-CAP correlati)
**Commit base auditato**: `f728311` (origin/main)
**Ruolo Reviewer assunto da agente general-purpose** (subagente nativo `reviewer` non disponibile nell'ambiente; ruolo adottato in pieno secondo `.claude/agents/reviewer.md`, incluse regole assolute, sezione "Probe-review (RM-4)" e divieti per sede `:163-164`).

**Perimetro auditato**:
- A = `docs/methodology_v2/CAP_08_parte_8.md`
- B = `reports/REPORT_CAP_08.md`
- C = `scripts/probe_dapi.py`
- D = `tasks/HANDOFF_PROBE_DAPI_20260528.md`

**Cross-reference fuori perimetro (citate, NON auditate)**:
- `scripts/export_directa_history_parametric.py` — decoder/comandi DAPI di produzione canonico `[CODICE-ESISTENTE]`
- Parte 9 / CAP-DATA-02 — sede canonica delle asserzioni DAPI (schema CANDLE, CANDLERANGE, codici errore, mesi IDEM): FUORI SCOPE, citata solo come destinazione di rinvio.

---

## VERDETTO: CONDITIONAL (Sede: WEB)

Motivazione sintetica: la coerenza script↔testo sullo schema CANDLE (W10) è **OK** — l'errore canonico è stato propagato correttamente nella rettifica. Tuttavia **5 asserzioni DAPI** (codici errore W4, sintassi CANDLERANGE W2, terminatore W3, cooldown 14-connessioni W6, convenzione mese W5) sono dichiarate come "fatti" in C e D **senza enumerazione delle alternative compatibili coi dati osservati** (violazione sostanziale RM-1, lo stesso pattern che ha prodotto l'errore CANDLE §3.1). Nessuna di queste è un BUG di valore già dimostrato (alcune sono anzi corroborate da codice di produzione, vedi Check W2), ma tutte condividono la **metodologia di verifica difettosa** che il task chiede esplicitamente di setacciare. La lista "Empirico-CLI da verificare" è **NON vuota** → per AC-13(d) il PASS non è concedibile in sede WEB.

---

## Check W1 — RM-1 statico (asserzioni "verificato/confermato/fatto N")

Esito per ogni asserzione dell'inventario W1..W10 + asserzioni emerse (W11).

### W1 — Schema CANDLE = `C;L;H;O;V`
- **C** `scripts/probe_dapi.py:7-13` (docstring), `:182-204` (decoder `parse_line`).
- **D** `tasks/HANDOFF_PROBE_DAPI_20260528.md:36-42` (§3.1, con rettifica 2026-05-29 in testa).
- **A.3 Sostanza**: **OK (post-rettifica)**. Il commento `probe_dapi.py:182-187` enumera esplicitamente l'alternativa storica errata (`O;L;H;C`), spiega *perché* il test daily non la escludeva ("su candele daily O e C non sono distinguibili dai soli valori"), e cita la prova di esclusione V-1 realtime (`p[4]=close, p[7]=open`). Questa è esattamente l'enumerazione+esclusione che RM-1 richiede. La sostanza regge.
- **A.2 Formato 4-righe**: assente (file pre-RM) → MIGLIORA PROCESSO, non BUG.
- **RM-2**: il commento `probe_dapi.py:187` cita `export_directa_history_parametric.py` come fonte coerente. Confermato (vedi Check W2). OK.
- **RM-3**: il wiki Directa è etichettato come INESATTO in C `:9` e in D `:42` (testo storico). Trattato come hint smentito, non come fonte di verità. OK.
- **Esito W1**: PASS sostanziale. La rettifica è ben fatta. Resta da verificare in CLI lo schema su tick reali (è già `[PROVA-EMPIRICA 2026-05-29]` per M-1 — non ri-auditata, assunta come dato per mandato del task §309).

### W2 — Sintassi `CANDLERANGE <sym> <start> <end> <period_s>` (period_s ULTIMO)
- **C** `scripts/probe_dapi.py:15-16` (docstring), `:269` (`run_candlerange`).
- **D** `tasks/HANDOFF_PROBE_DAPI_20260528.md:44-48` (§3.2): *"4 argomenti, **period_s come ULTIMO** (NON secondo). Sintassi errata restituisce `ERR;;1017`."*
- **A.3 Sostanza**: l'asserzione sull'**ordine argomenti** è **corroborata da CODICE-ESISTENTE** (vedi Check W2 / RM-2): `export_directa_history_parametric.py:228-230` emette la stessa identica sintassi con period LAST. Quindi l'ordine NON è wiki-only né empirico-isolato: ha supporto di livello-2. **OK su ordine argomenti.**
- **MA**: la clausola *"Sintassi errata restituisce `ERR;;1017`"* è un'asserzione causale empirica (quale permutazione errata produce 1017? quali altre permutazioni sono state provate ed escluse?) senza enumerazione → vedi W4 (codici errore).
- **Esito W2**: ordine argomenti OK (level-2). Mappatura errore→1017: rinviata a CLI (W4).

### W3 — Terminatore stream history = `END CANDLES`
- **C** `:14`, `:75` (`END_MARKER = b"END CANDLES"`). **D** `:50-52` (§3.3).
- **A.3 Sostanza**: **corroborato da CODICE-ESISTENTE**: `export_directa_history_parametric.py:245,282-285,437` usa `END CANDLES` come marker di fine identico. Level-2. **OK.**
- Alternative compatibili non discusse (case-sensitivity, trailing marker simultanei), ma la coincidenza con decoder di produzione che ha già processato ~380 dump rende il rischio basso. Marcato MIGLIORA PROCESSO (enumerazione formale), non BUG.

### W4 — Codici errore DAPI 1004 / 1007 / 1017 / 1030 con semantica
- **C** `scripts/probe_dapi.py:17-21` (docstring). **D** `tasks/HANDOFF_PROBE_DAPI_20260528.md:54-61` (§3.4, tabella).
- **A.3 Sostanza**: **VIOLAZIONE RM-1**. Ciascuna riga dichiara `codice → significato` come fatto, **senza** dichiarare: (i) quale comando esatto ha prodotto ciascun codice (timestamp/dump), (ii) quali semantiche alternative sono state escluse. Esempio `:20` *"1017 = sintassi del comando malformata"* — ma 1017 potrebbe codificare un sottoinsieme più ampio (parametro fuori range? ticker+sintassi insieme?). Non enumerato.
- **RM-2 (contro-prova)**: il decoder di produzione `export_directa_history_parametric.py:417-425` (`is_error_line`) **NON decodifica codici numerici** — fa string-matching su `ERR`/`Wrong`/`error`. Quindi la semantica numerica 1004/1007/1017/1030 **non ha alcun supporto in codice di produzione**: è asserzione empirica isolata di sessione web 28/05. Esattamente la classe di asserzione che il task chiede di setacciare.
- **Esito W4**: **BUG REALE (sostanziale RM-1)** — semantica codici errore dichiarata "fatto" senza enumerazione alternative né evidenza puntuale (dump:timestamp). Va riscritta come "verifica parziale" e marcata Empirico-CLI.

### W5 — Convenzione mese Directa-IDEM `F`=Giu, `I`=Set (Mar/Dic da decodificare)
- **C** `:22`. **D** `:63-67` (§3.5).
- **A.3 Sostanza**: **parzialmente OK**. `F`=Giugno è ancorato a evidenza puntuale citabile (D `:65`: ISIN IT0024209022 + descrizione "GIU26") — questo è un claim→evidenza valido. `I`=Settembre cita "Appendice B.2" (D `:66`) — rinvio a fonte interna `[DOC-INTERNO]`, accettabile come level-3 ma non verificato in questo perimetro. **Mar/Dic** sono correttamente dichiarati *"da decodificare"* (D `:67`) — questa è la forma RM-1 corretta (verifica parziale dichiarata). Buona pratica.
- **MA**: D `:67` aggiunge *"candidati probabili `C` e `L`"* — speculazione, non fatto. Etichettata come "candidati probabili" → accettabile (non dichiarata verificata).
- **Esito W5**: forma RM-1 sostanzialmente corretta (la parzialità è dichiarata). `I`=Settembre da confermare CLI (Empirico-CLI, basso). Nessun BUG.

### W6 — Cooldown ~30s dopo 14ª connessione consecutiva
- **C** `scripts/probe_dapi.py:27-29` (docstring). **D** `tasks/HANDOFF_PROBE_DAPI_20260528.md:69-71` (§3.6).
- **A.3 Sostanza**: **VIOLAZIONE RM-1**. Due numeri precisi ("~30s", "14ª connessione") dichiarati come fatti, con unica ancora *"(osservato in App. A.4)"* / *"(Appendice A.4)"*. Non enumerate le alternative compatibili (cooldown dopo 12/13/15 connessioni? la soglia 14 è hard o è il punto in cui *quel* test specifico ha visto il cooldown?). Un singolo run che vede cooldown alla 14ª non esclude che la soglia reale sia 13 o che dipenda dal timing. Pattern identico a CANDLE: numero preciso da un test che non disambigua.
- **Esito W6**: **BUG REALE (sostanziale RM-1)** — "14" e "30s" dichiarati come costanti senza enumerazione/esclusione. Riscrivere come "verifica parziale: cooldown osservato ~30s in prossimità della ~14ª connessione in App. A.4; soglia esatta non disambiguata". Empirico-CLI.

### W7 — Limite empirico ~100 giorni intraday DAPI
- **D** `tasks/HANDOFF_PROBE_DAPI_20260528.md:168` (§5.5): *"Cosa cerchiamo: il punto di rottura... Coerente con Appendice A.2 (limite empirico ~100 giorni intraday DAPI)."*
- **A.3 Sostanza**: **OK**. È dichiarato come *"cosa cerchiamo"* — ipotesi da testare (V-2), NON fatto verificato. Forma RM-1 corretta.
- **RM-2 (corroborazione)**: il codice di produzione **conferma** l'ordine di grandezza: `export_directa_history_parametric.py:61` `DEFAULT_INTRADAY_MAX_DAYS = 100`. Quindi il ~100gg ha supporto level-2 come *parametro operativo già in uso*. C `:78` (`CUTOFF_DAYS`) lo sonda con range 50..160 — coerente con un'ipotesi da disambiguare. Nessun BUG.

### W8 — Banner `DARWIN_STATUS;CONN_OK;TRUE` atteso
- **C** `scripts/probe_dapi.py:44` (docstring), `:169` (`parse_line` matcha prefisso `DARWIN_STATUS`).
- **A.3 Sostanza**: asserzione su formato banner sistema esterno, senza enumerazione né evidenza puntuale citata nel perimetro. Tuttavia: il decoder `:169` matcha solo il **prefisso** `DARWIN_STATUS` (non l'intera stringa `;CONN_OK;TRUE`), quindi l'asserzione "atteso `DARWIN_STATUS;CONN_OK;TRUE`" è più stringente di ciò che il codice usa. Discrepanza minore docstring↔codice. Empirico-CLI (richiede banner reale). Classificato MIGLIORA PROCESSO.

### W9 — Convenzione ticker IDEM/Eurex/CME
- **C** `scripts/probe_dapi.py:23-26` (docstring): `IDEM: <CODE><YEAR><MONTH>` es. FIB6F; `Eurex: EU.<CODE><MONTH><YEAR>`; `CME: CM.<CODE><MONTH><YEAR>`.
- **A.3 Sostanza**: **VIOLAZIONE RM-1 (minore)**. Tre convenzioni distinte dichiarate come fatti. L'ordine YEAR/MONTH differisce fra IDEM (`6F`=anno-mese) ed Eurex/CME (`M6`=mese-anno): è un'affermazione precisa che richiede test che distingua le 3. Solo FIB6F ha evidenza (W5). Eurex/CME non hanno evidenza nel perimetro. Da notare: la convenzione ticker appartiene **canonicamente a Parte 9** (cross-reference) → per `ACTIVE_TASK.md:78` va segnalata MIGLIORA PROCESSO (rinvio canonico), non BUG. Empirico-CLI per Eurex/CME.

### W10 — Coerenza script-corretto (C) vs handoff-stale (D) su schema CANDLE
- **C** dichiara `C;L;H;O;V` corretto (`:8`, `:182-204`). **D** §3.1 ha rettifica in testa (`:36-38`) + testo errato preservato sotto (`:40-42`).
- **A.3 / coerenza inter-file**: **OK**. Il testo errato di D `:40-42` è inequivocabilmente etichettato: D `:40` *"**Testo originale del 28/05 (conservato per storia, ora superato):**"* e la rettifica D `:36` usa `~~O;L;H;C;V~~` (strikethrough) + "⚠️ RETTIFICA". Un lettore non può confondere il vecchio testo per un fatto valido. La condizione critica del task (W10) è **soddisfatta**.
- **Nota**: la rettifica D `:36` scrive lo schema come `O;L;H;C;V` nel testo barrato originale, ma il titolo §3.1 e la docstring di C usano `C;L;H;O;V`. Coerenti fra loro (entrambi indicano UFF=close in pos 1, APE=open in pos 4). Nessuna divergenza residua di valore.
- **Esito W10**: PASS. Propagazione della rettifica corretta in C e D. **Punto chiave dell'audit: superato.**

### W11 (emerso nel secondo giro) — Schema PRICE / BOOK_5 / ANAG mai disambiguati bit-a-bit
- **C** `scripts/probe_dapi.py:208-251` (decoder `anag`, `price`, `book5`).
- **A.3 Sostanza**: i decoder `price` (`:223-240`) e `book5` (`:241-251`) **ammettono onestamente** di non conoscere lo schema esatto: `:224-225` *"schema esatto dei campi extra non documentato, varia tra cash e future"*; `book5` raccoglie `fields: p[3:]` senza interpretazione bit-a-bit. Questa è onestà RM-1 corretta (non dichiara verificato ciò che non lo è). **Nessun BUG**. Ma sono asserzioni di posizione campi (`PRICE` last in `p[3]`, `:227-230`) che restano Empirico-CLI se mai citate come fatto in Parte 9 (fuori scope qui). Segnalo solo come MIGLIORA PROCESSO/Empirico-CLI.

---

## Check W2 — RM-2 grep nel repo e coerenza script↔decoder canonico

**Grep eseguito** (sede WEB, via strumento Grep su `--include=*.py`):
```
pattern: parse_|decode_|UFF|APE|CANDLE|BOOK_5|PRICE   (glob *.py)
```
**Esito — decoder/parser DAPI esistenti nel repo per CANDLE**:
- `scripts/export_directa_history_parametric.py:467-496` (`parse_directa_candle`) — **decoder canonico di produzione**. Riga `:477` commento esplicito `# Documentazione Directa: UFF, MIN, MAX, APE => close, low, high, open.` con mapping `close_v=Decimal(uff)` (`:478`), `low_v=Decimal(min_)` (`:479`), `high_v=Decimal(max_)` (`:480`), `open_v=Decimal(ape)` (`:481`). Cioè ordine campi `p[4..8] = UFF;MIN;MAX;APE;qty` = `close;low;high;open;volume`.
- `scripts/probe_dapi.py:188-204` (`parse_line`, ramo `CANDLE;`) — `close=float(p[4])` (UFF), `low=float(p[5])` (MIN), `high=float(p[6])` (MAX), `open=float(p[7])` (APE), `volume=p[8]`.

**Confronto puntuale (cosa significa "coerente" — AC-9)**: ho cercato divergenze su (a) ordine dei 5 campi numerici, (b) mapping nome→OHLC, (c) indice di colonna. Tutte e 3 coincidono: entrambi mappano pos `[4]→close`, `[5]→low`, `[6]→high`, `[7]→open`, `[8]→volume`. **Nessuna divergenza trovata.** I due decoder sono coerenti sullo schema CANDLE. (W10 confermato anche via codice, non solo via testo.)

**Altri comandi DAPI corroborati dal canonico**:
- CANDLERANGE: `export_directa_history_parametric.py:228-230` emette `CANDLERANGE {symbol} {start} {end} {period_seconds}` — period LAST, identico a C `:269` e a D §3.2. Corrobora W2 (ordine argomenti) a level-2.
- `END CANDLES`: `export_directa_history_parametric.py:245,282-285,437` — corrobora W3 a level-2.
- Codici errore numerici (1004/1007/1017/1030): `export_directa_history_parametric.py:417-425` (`is_error_line`) **NON** li decodifica (string-match generico). → W4 **non** ha supporto level-2: resta asserzione empirica isolata (conferma il finding BUG REALE su W4).

**Decoder non citati dal perimetro**: nessun decoder DAPI aggiuntivo oltre i due sopra è emerso dal grep. `scripts/update_inventory_indici_futures_daily.py` (citato da D `:206`) non è apparso nel grep dei pattern decoder → non contiene parsing CANDLE rilevante. RM-2 soddisfatto.

---

## Check W3 — RM-3 etichettatura fonti

- **C `:9`** *"il wiki DAPI dichiara O;H;L;C ed è INESATTO"* — wiki trattato come hint smentito. Conforme RM-3 (non usato come fonte di verità). Etichetta esplicita assente (pre-RM) → MIGLIORA PROCESSO.
- **D `:42`** (testo storico) *"Il wiki DAPI dichiara `O;H;L;C` ma è INESATTO. Verificato empiricamente su FIB6F daily..."* — **qui è la radice dell'incidente**: il vecchio testo dichiarava "Verificato empiricamente" su un test daily che non disambiguava O/C. La rettifica `:36-38` lo corregge e ora cita correttamente `[CODICE-ESISTENTE r.477]` + `[PROVA-EMPIRICA V-1]`. La rettifica è RM-3 conforme.
- **Conclusioni "wiki-only" nel perimetro**: **nessuna trovata**. Lo schema CANDLE finale poggia su codice di produzione (level-2) + V-1 (level-1), non sul wiki. Gli altri fatti (W4/W6) poggiano su "App. A.x" interne (level-3) o osservazione empirica (level-1 da disambiguare), non sul wiki. **Nessun BUG RM-3.**
- **A (CAP_08)**: nessuna citazione del wiki Directa. A non tocca lo schema DAPI runtime (parla di Portara/CQG, serie storiche, sessioni). Le fonti esterne di A (Borsa Italiana, Portara) sono in `data/sessions/README.md` (fuori perimetro). Nessuna conclusione wiki-only in A.

---

## Check W4 — coerenza interna del perimetro

- **A vs B**: B (`reports/REPORT_CAP_08.md`) è il report di A. Mappatura AC→evidenza (B `:127-144`): ogni "OK" punta a righe di A. Verifica a campione: AC-3.4 → A `:73-105` (Cap.40) ✓; AC-3.5 → A `:107-139` (Cap.41) + CSV ✓; AC-3.2 → A `:25-53` (Cap.38) ✓. Le righe citate esistono e contengono il dichiarato. **Mappatura claim→evidenza di B regge** (criterio 4 probe-review). Nota: B `:231` dichiara "16/16 AC OK" ma la tabella elenca AC-3.1..3.8 (8) + AC-DoD-1..8 (8) = 16 — coerente.
- **A non contiene asserzioni "verificato schema CANDLE/DAPI"**: A è puramente metodologico-Portara. Nessun residuo DAPI da setacciare in A. (Buono: l'errore CANDLE non ha contaminato A.)
- **C vs D**: coerenti su CANDLE (W10), CANDLERANGE (W2), END CANDLES (W3), codici errore (W4 — entrambi dichiarano la stessa tabella non-RM-1), mesi (W5), cooldown (W6). Le divergenze sono solo nella rettifica esplicita §3.1 di D (etichettata). **Nessuna divergenza non etichettata.**
- **D.1 — citazioni cross-CAP di A verso Parte 9**: A NON cita Parte 9 per fatti DAPI (A cita "CAP-DATA-02" per ambiguità Portara/roll-rule: A `:57` Cap.39 e A `:137` Cap.41). Questi rinvii sono a referenti plausibili (Parte 9 esiste come destinazione). Validati per esistenza del referente, non per contenuto. OK.

---

## Check W5 — coerenza script↔capitolo↔handoff (il check che avrebbe preso l'errore)

**Confronto decoder CANDLE di C vs §3.1 di D vs decoder canonico**:
- C `scripts/probe_dapi.py:188-204`: `p[4]→close, p[5]→low, p[6]→high, p[7]→open` = `C;L;H;O;V`.
- D §3.1 rettifica `:36-38`: schema reale `C;L;H;O;V`, vecchio `O;L;H;C;V` barrato.
- Canonico `export_directa_history_parametric.py:477-481`: `UFF→close, MIN→low, MAX→high, APE→open` = `C;L;H;O`.
- **Tutti e tre concordano.** Lo script C è **ora corretto e coerente** con il canonico e con la rettifica di D. La divergenza storica (script `O;L;H;C` → ora `C;L;H;O`) è chiusa dal commit `a12ae32` (citato in C `:13` e D `:38`).

**Conclusione W5**: lo script NON afferma più uno schema divergente dal testo/handoff. Il check che avrebbe intercettato l'errore originale (script vs handoff) oggi **passa**: nessuna divergenza residua codice↔testo sullo schema CANDLE. L'unico residuo è metodologico (W4/W6: fatti dichiarati senza disambiguazione), non di valore di schema.

---

## Check W6 — onestà claim→evidenza + lista Empirico-CLI

Asserzioni senza evidenza puntuale citabile (file:linea/dump:timestamp/test:risultato):
- **W4** codici errore: nessun dump:timestamp citato. → senza evidenza puntuale = BUG REALE.
- **W6** cooldown 14/30s: unica ancora "App. A.4" (non un dump puntuale con conteggio connessioni). → evidenza debole, BUG REALE sostanziale.
- **W8** banner: nessuna evidenza citata; discrepanza docstring (stringa piena) vs codice (solo prefisso). → MIGLIORA PROCESSO + Empirico-CLI.
- **W9** Eurex/CME ticker: nessuna evidenza per i non-IDEM. → MIGLIORA PROCESSO (canonicamente Parte 9) + Empirico-CLI.

Asserzioni CON evidenza adeguata: W1 (V-1 + codice r.477), W5 `F`=Giu (ISIN+descr), W7 (param di produzione + dichiarata ipotesi).

### Empirico-CLI da verificare (lista NON vuota — input per sessione CLI separata)

| W-N | Asserzione | File:linea | Test minimo proposto (CLI, DAPI live) |
|-----|-----------|-----------|----------------------------------------|
| W4 | semantica codici 1004/1007/1017/1030 | C `:17-21`; D `:54-61` | inviare i comandi-trigger dichiarati (HELP su 10001; CANDLERANGE malformata su 10003; SUB non sottoscritto su 10001) e registrare codice+dump:timestamp per ognuno; provare ≥2 permutazioni errate per disambiguare se 1017 copre solo "sintassi" o anche "parametro fuori range" |
| W6 | cooldown ~30s / 14ª connessione | C `:27-29`; D `:69-71` | aprire/chiudere socket 10003 in loop contando le connessioni fino al cooldown; ripetere ≥3 volte per stabilire se la soglia è 14 esatta o varia (13/15); misurare la durata del cooldown |
| W5 | `I`=Settembre; Mar/Dic | C `:22`; D `:63-67` | SUB ticker trimestrale Set + Mar/Dic, leggere `ANAG.descrizione`+ISIN per confermare `I` e decodificare Mar/Dic |
| W8 | banner `DARWIN_STATUS;CONN_OK;TRUE` | C `:44`, `:169` | catturare il banner reale alla connessione 10001/10003 e confrontare con la stringa attesa; allineare docstring↔codice |
| W9 | ticker Eurex `EU.` / CME `CM.` | C `:23-26` | SUB di un ticker Eurex e uno CME, leggere ANAG per confermare ordine MONTH/YEAR (nota: canonicamente Parte 9) |

(W1/W10 NON sono in lista: già `[PROVA-EMPIRICA 2026-05-29]` per M-1, assunti come dato per mandato del task §309.)

---

## Tabella di classificazione per il supervisore

| # | Problema | File:linea | Classificazione | Patch/azione suggerita |
|---|----------|-----------|-----------------|------------------------|
| 1 | Semantica codici errore 1004/1007/1017/1030 dichiarata "fatto" senza enumerazione alternative né dump:timestamp; nessun supporto in codice di produzione (`is_error_line` non decodifica numerici) | C `scripts/probe_dapi.py:17-21`; D `:54-61` | **BUG REALE** (sostanziale RM-1) | Riscrivere come "verifica parziale": per ogni codice indicare il comando-trigger osservato e marcare "semantica esatta da disambiguare". Aggiungere blocco 4-righe in D §3.4. Test in CLI (riga W4). Il Reviewer NON patcha. |
| 2 | Cooldown "~30s dopo 14ª connessione" — due costanti precise da singola osservazione, alternative (13/15, dipendenza timing) non escluse | C `:27-29`; D `:69-71` | **BUG REALE** (sostanziale RM-1) | Riscrivere D §3.6 come "verifica parziale: cooldown ~30s osservato in prossimità della ~14ª connessione (App. A.4); soglia esatta non disambiguata". Test CLI (riga W6). |
| 3 | Terminatore `END CANDLES`, ordine arg CANDLERANGE: corretti e corroborati da codice di produzione (level-2), ma enumerazione alternative formale assente (pre-RM) | C `:14-16`; D `:44-52` | **MIGLIORA PROCESSO** (NON BUG: hanno supporto level-2) | Opzionale: aggiungere etichetta `[CODICE-ESISTENTE r.228-230 / r.245]` ai due fatti. Nessun rischio di valore. |
| 4 | Convenzione ticker Eurex/CME senza evidenza nel perimetro; appartiene canonicamente a Parte 9 | C `:23-26` | **MIGLIORA PROCESSO** (rinvio canonico) | Annotare in C che IDEM è l'unico testato; Eurex/CME da confermare CLI e canonicizzare in Parte 9. |
| 5 | Banner: docstring dichiara stringa piena `DARWIN_STATUS;CONN_OK;TRUE`, decoder matcha solo prefisso `DARWIN_STATUS` | C `:44` vs `:169` | **MIGLIORA PROCESSO** | Allineare docstring al comportamento del decoder o viceversa dopo cattura banner reale (CLI). |
| 6 | Etichette di fonte RM-3 (`[WIKI-HINT]`/`[CODICE-ESISTENTE]`/`[PROVA-EMPIRICA]`) assenti nel perimetro (file pre-RM) | C, D (globale) | **MIGLIORA PROCESSO** | Le etichette non esistevano alla scrittura; la sostanza RM-3 regge. Aggiungere etichette in eventuale rework. |
| 7 | Formato 4-righe RM-1 assente in tutte le asserzioni di C/D (file pre-RM) | C, D (globale) | **MIGLIORA PROCESSO** (solo dove la sostanza regge: W1/W3/W5/W7) | Riformattare in 4-righe solo le asserzioni approvate per rework (#1, #2 obbligatori). |

**Nota su NEUTRO/RISCHIO PEGGIORAMENTO**: nessun finding classificato NEUTRO o RISCHIO PEGGIORAMENTO. I 2 BUG REALI (#1, #2) sono obbligatori per chiusura RM-1 sostanziale; i 5 MIGLIORA PROCESSO sono a discrezione del supervisore.

---

## Verdetto motivato

Il **cuore dell'audit (W5/W10: coerenza script↔testo sullo schema CANDLE) è PASS**: l'errore canonico `O;L;H;C` → `C;L;H;O;V` è stato rettificato in modo esemplare. Il decoder di `probe_dapi.py:188-204` è ora coerente bit-per-bit con il decoder di produzione `export_directa_history_parametric.py:477-481`; il vecchio testo errato in D §3.1 è inequivocabilmente barrato e datato; nessuna divergenza di valore residua. Il check W5 — quello che avrebbe intercettato l'errore originale se fosse esistito a fine maggio — oggi **passa**. Inoltre l'audit ha trovato che A (CAP_08) non è stato contaminato dall'errore DAPI (è puramente Portara/serie storiche) e che B (REPORT) ha una mappatura claim→evidenza solida. Nessuna conclusione "wiki-only" nel perimetro.

Tuttavia il task chiede esplicitamente di setacciare se le **altre scoperte** di D (§3.2-§3.6) condividono la metodologia difettosa che ha prodotto l'errore §3.1. La risposta è **sì per due di esse**: W4 (codici errore) e W6 (cooldown 14/30s) sono dichiarate come fatti precisi senza enumerare/escludere le alternative compatibili coi dati osservati e senza ancora a evidenza puntuale — lo stesso pattern di `O;L;H;C`. Non è dimostrato che siano *sbagliate* (W2/W3/W7 risultano anzi corroborate da codice di produzione, smentendo l'ipotesi che tutto §3 sia inaffidabile), ma sono **non verificate** nel senso RM-1, e alimenterebbero PROBE_RECUPERO_GAP_DAPI.md / CAP-DATA-03 come "fatti" prematuri. Per questo, e poiché la **lista "Empirico-CLI da verificare" è non vuota** (5 asserzioni che richiedono DAPI live), per AC-13(a)/(d) il verdetto è **CONDITIONAL**, non PASS: i 2 BUG REALI vanno riscritti come verifica parziale (sede WEB, Developer di rework) e le 5 voci empiriche handoffate a una sessione CLI separata per disambiguazione contro DAPI live. In coerenza col divieto `reviewer.md:163`, il Reviewer WEB NON dichiara verificato/falsificato nulla di W4/W5/W6/W8/W9: le marca Empirico-CLI.

---

### Applicazione RM a sé stesso (AC-9/10/11)

- **RM-1 (AC-9)**: la mia asserzione "il decoder di C `:188-204` è coerente con il canonico `:477-481`" è verificata enumerando le 3 divergenze cercate ed escluse (ordine dei 5 campi, mapping nome→OHLC, indice colonna) — vedi Check W2. Non ho dichiarato "verificato" nulla che richieda DAPI live (W4/W5/W6/W8/W9 → marcate Empirico-CLI, NON chiuse). L'asserzione W10-PASS è basata su lettura statica di file versionati (non richiede DAPI), quindi legittima in sede WEB.
- **RM-2 (AC-10)**: grep eseguito e citato (Check W2, comando + esito + path:linea). Conclusione sui decoder esistenti basata su grep diretto, non su assunzione.
- **RM-3 (AC-11)**: ogni finding cita file:linea testuale, nessuna parafrasi "a memoria". Riferimenti al canonico citati con `file:linea` (`:477-481`, `:228-230`, `:417-425`, `:61`).
- **AC-12**: nessun file del perimetro A-D modificato; unico file scritto = questo review. Working tree pulito su A/B/C/D.
