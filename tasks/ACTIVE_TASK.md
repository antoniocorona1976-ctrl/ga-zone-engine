# TASK ATTIVO: AUDIT-RM CAP-DATA-03 — audit indipendente RM-1/2/3 perimetro A-D (Parte 10)

**Assegnato da**: Planner
**Output atteso**: `reviews/REVIEW_CAP_DATA_03_RM_AUDIT_review.md`
**Stato**: IN ATTESA
**Workflow**: **Review-First** (il perimetro A-D esiste già su `origin/main` e Parte 10 è già **PASS** — review v1 `ab80d96` + v2 `48171e4`. Il Developer NON entra in v1: entra **solo** se il supervisore approva finding `BUG REALE` / `MIGLIORA PERFORMANCE` / `RISCHIO PEGGIORAMENTO` derivanti dall'audit; in tal caso l'Orchestratore riapre il loop con prompt mirato. Niente bozze Developer prima della Review.)
**Sede Reviewer**: **CLI locale** (sessione corrente — il supervisore non ha richiesto sede WEB; l'audit è documento + grep + lettura del codice committato, **nessuna esecuzione DAPI**).

**Natura del task** (dichiarata esplicitamente come premessa metodologica):

CAP-DATA-03 è **post-RM**: è nato RM-compliant ed è già stato revisionato su RM-1/2/3 nelle review v1/v2 (entrambe in sede CLI, locale). Questo task **non è un recupero di debito retroattivo** come gli `AUDIT-RM-RETRO` di CAP-DATA-01/02 (che erano pre-RM e dovevano saldare retroattivamente i 3 vincoli su un capitolo storico non auditato in chiave RM). Questo task è un **audit indipendente confermativo** (seconda opinione / simmetria con il trattamento ricevuto da CAP-DATA-01/02 / verifica che la conformità RM regga a un secondo sguardo ostile esteso al **perimetro A-D**, non al solo capitolo): tre file accessori del CAP (B report, C probe-sorgente empirico, D decoder canonico) non sono stati formalmente auditati come perimetro a sé nelle review v1/v2 (queste hanno auditato il CAP A e verificato citazioni puntuali, non gli oggetti B/C/D come oggetti di prima classe). Il naming evita deliberatamente "RETRO" perché sarebbe fuorviante: qui non c'è debito retroattivo da saldare, c'è una conformità da **riconfermare con sguardo esteso**.

NON è una CAP-review piena nuova (Parte 10 è già PASS e questo task NON la riapre); NON è una probe-review standard (qui si audita simultaneamente: 1 CAP appena chiuso A + 1 report supervisore B + 1 documento-indagine sorgente C + 1 decoder canonico di riferimento D); è un **audit RM mirato a 4 sorgenti contemporaneamente**, con priorità "non re-derivare l'empirico, verificare l'uso che ne fa il perimetro A-D".

---

## Obiettivo

L'audit verifica, su tutto il **perimetro A-D** di CAP-DATA-03, che:

1. **RM-1 — formato e sostanza**. Tutte le asserzioni "verificato / confermato / fatto / dimostrato / stabilito" del perimetro:
   - rispettino il formato 4-righe `VERIFICA / PROVE / ALTERNATIVE COMPATIBILI ESCLUSE / ALTERNATIVE COMPATIBILI NON ESCLUSE` (`tasks/METODO.md:28-33`);
   - abbiano sostanza coerente con le prove citate (cioè le "alternative escluse" siano effettivamente escluse dai dati osservati, e le "non escluse" siano davvero compatibili);
   - dichiarino il **perimetro empirico onesto** quando l'asserzione si appoggia a prove parziali (T+3 morning, FIB6F/DITAS, ~100gg) — NON dichiarino "verificato universalmente" cio' che e' verificato solo entro un perimetro.
2. **RM-2 — grep + citazioni file:linea verso D-canonico**. Ogni richiamo a strutture/format/protocollo DAPI nel perimetro abbia citazione `[CODICE-ESISTENTE <path>:<linea>]` puntuale **VERIFICATA leggendo D** (sola lettura): la riga citata contiene davvero il costrutto che A/B/C affermano. Coerenza A/C ↔ D-canonico: gli schemi (CANDLE `C;L;H;O;V`, sintassi `CANDLERANGE`, costante `DEFAULT_INTRADAY_MAX_DAYS=100`, header CSV legacy 11-campi, terminatore `END CANDLES`) citati in A e/o C combaciano con D nelle righe esatte; **eventuali divergenze di citazione o di numero di campi devono essere segnalate**. Onorando `RACC-METODO-2` (Re-Review v2 CAP-DATA-02): per ogni AC del CAP che dichiara "schema X coerente con DAPI", verificare con diff puntuale rispetto a D, NON solo completezza strutturale.
3. **RM-3 — etichettatura fonti per livello**. Ogni prova nel perimetro e' etichettata con il suo livello (1 `[PROVA-EMPIRICA <data>]`, 2 `[CODICE-ESISTENTE r.NNN]`, 3 `[DOC-INTERNO <path>]`, 4 `[WIKI-HINT, da verificare]`); nessuna conclusione di livello 1/2/3 si appoggia **solo** a livello 4 (wiki Directa, dimostrato inesatto); riferimenti residui a wiki o convenzioni esterne sono espliciti come hint.
4. **Coerenza inter-file (perimetro come un tutto)**. Le citazioni di A verso C e D sono fedeli (numero di match, posizione del cut-off, schema PRICE `f4/f6/f8/f9`, cash low/high, immutabilita' T+3, perimetro empirico onesto FIB6F/DITAS morning); le citazioni cross-CAP (`CAP_06_parte_VI.md:276`, `CAP_08_parte_8.md` Cap.37/Cap.38/Cap.40/Cap.41/Cap.43/Cap.44, `CAP_09_parte_9.md` Cap.45/Cap.46/Cap.47/Cap.48/Cap.49/Cap.50/Cap.51/Cap.52/Cap.54/Cap.55) puntano a contenuti effettivamente esistenti nei file referenti.
5. **Onesta' claim → evidenza in B (REPORT_CAP_10.md)**. Ogni AC dichiarato OK dal REPORT (43/43) ha evidenza puntuale verificabile nel CAP A; ogni "OK" non si appoggia a un riferimento generico ("Cap.59 ✓") ma alla riga/blocco esatto del CAP che soddisfa l'AC. La tabella AC del REPORT non contiene "OK" privi di evidenza puntuale.

**Cosa l'audit NON fa**:

- **Non riapre AC della Review v2**: i 43/43 AC del task card di sviluppo CAP-DATA-03 sono gia' stati verificati indipendentemente in v1 (`ab80d96`) e ri-confermati in v2 (`48171e4`); l'audit RM non li riesamina nel merito (e' verifica trasversale di conformita' RM al perimetro esteso, non re-verifica del merito metodologico del capitolo).
- **Non re-deriva l'empirico**. Le fondamenta empiriche sono **CHIUSE** ed elencate come inputs autoritativi sotto. L'audit ne controlla l'**uso** dentro A/B/C, non le ri-misura contro DAPI.
- **Non riapre decisioni** `D-10-1..D-10-10`. L'audit verifica che siano dichiarate correttamente con RM-1 dove l'oggetto della decisione e' una verifica empirica (es. D-10-2 idempotenza T+3 morning, D-10-4 cash low/high); non ne mette in discussione il merito normativo.
- **Non patcha D** (`scripts/export_directa_history_parametric.py`): D e' **fonte di verita' level-2** e NON si modifica in questo task. Eventuali divergenze A/C ↔ D si segnalano come finding e si correggono in A o C, mai in D.
- **Non re-fa la review v1/v2** di CAP-DATA-03: NB-1 (Brier $f_5^{live}$), OM-1/2/3 sono gia' **chiusi** in v2; l'audit verifica per scrupolo che le correzioni reggano e non siano regredite, ma non li riapre se intatti.
- **Non audita il micro-patch Cap.49 di Parte 9** (sotto-task separato fuori dal perimetro A-D di Parte 10).
- **Non audita il cross-index PHASE-2** (DAX/EuroStoxx 50/ES/MES futures): Parte 10 dichiara fuori scope (Cap.64) e PHASE-2 e' perimetro autonomo.
- **Non esegue DAPI** ne' apre socket: vincolo di sede CLI = lettura del codice committato + grep + Read dei dump citati come esistenti su `probe_out/` (sola verifica di esistenza, NON di contenuto rispetto a DAPI live).
- **Non solleva probe massivi di mero zelo** (divieto di sede CLI in `reviewer.md`): le asserzioni empiriche del perimetro sono CHIUSE; eventuali residui empirici si segnalano come "Empirico-CLI da verificare" — **lista attesa VUOTA**, perche' l'empirico e' chiuso (V-1 morning+afternoon, V-2 cut-off, T+1=T+3 immutabilita', schema PRICE `f4/f6/f8/f9`).

L'audit rende possibile, in caso di esito PASS, una **conferma di simmetria** col trattamento ricevuto da CAP-DATA-01/02 e una **verifica indipendente** che l'apparato RM (formato e sostanza) sia diventato pratica stabile del progetto sul perimetro esteso, non solo sul singolo CAP. In caso di esito CONDITIONAL/FAIL, indirizza fix mirati (correzioni puntuali ad A/B/C, mai D) attraverso il punto di controllo supervisore con classificazione dei finding.

---

## Eredita' obbligatoria

### Da `tasks/METODO.md` — RM-1..RM-4 (vincolanti per il Reviewer di questo task — RM-1 si applica anche al Reviewer)

1. **RM-1 — formato e sostanza** (`METODO.md:11-43`). Il Reviewer applica la regola a se' stesso: ogni sua dichiarazione "CONFERMATO ESATTO", "MATCH", "coerente", "verificato esatto", "non trovato dopo grep" deve essere accompagnata, nel corpo dell'audit, da: (a) prova testuale puntuale (token cercato + esito + file:linea); (b) enumerazione esplicita delle alternative compatibili (es. "alternativa: riga diversa nel file, esclusa controllando le 5 righe adiacenti"; "alternativa: il documento usa convenzione X non Y, esclusa cercando il pattern `X|Y` su tutto il file"). NON sono ammesse asserzioni "verificato" del Reviewer senza il blocco 4-righe o suo equivalente operativo (es. "tabella con `Citazione | Contenuto atteso | Esito verifica`" e' ammessa come forma compatta del blocco RM-1 se ogni riga contiene esattamente i 4 elementi).

2. **RM-2 — grep documentato** (`METODO.md:46-94`). Il Reviewer DEVE eseguire `grep`/`Grep` sui pattern del dominio prima di concludere e citare comando + esito nell'audit. Pattern obbligatori (lista minima — il Reviewer estende):
   - **Schema CANDLE**: `parse_directa_candle|UFF|MIN|MAX|APE|C;L;H;O|O;L;H;C|O;H;L;C` su `scripts/` + `docs/methodology_v2/CAP_10_*.md` + `tasks/PROBE_RECUPERO_GAP_DAPI.md`. Esito atteso: nessuna occorrenza di `O;L;H;C` o `O;H;L;C` come "schema canonico" nel perimetro (sono il wiki + l'errore §3.1 storico); se occorrono, devono essere in contesti di rifiuto/correzione esplicita (es. §3.2 PROBE, §7.2 risposta web).
   - **CANDLERANGE sintassi**: `CANDLERANGE.*period|period_s|period_seconds|<period_s>|86400|period 60` su `scripts/` + perimetro. Verifica posizione `period` (ultimo arg) coerente in A/C/D.
   - **Cut-off 100gg**: `DEFAULT_INTRADAY_MAX_DAYS|100.*gg|~100|100 giorni|2026-02-18` su perimetro. Verifica che il valore numerico (~100gg/saturazione `2026-02-18 09:56`/38.567 candele) sia coerente fra A Cap.59 cut-off, REPORT B, e PROBE C §4.2.
   - **Schema CSV legacy vs runtime**: `fieldnames|tick_count|bar_synthetic|symbol,timeframe,timestamp` su `scripts/export_directa_history_parametric.py` (header legacy 11 campi `:605-617`) e su `docs/methodology_v2/CAP_09_parte_9.md` (header runtime esteso 13 campi `:117-122` — riferimento di Parte 9). Verifica che A Cap.62 e Cap.64 distinguano correttamente i due, e che la correzione `:605-617` vs `:119-122` (introdotta dal Developer post-task-card) sia accurata e cross-consistente fra A e B.
   - **Marker normativi**: `RUNTIME_GAP|BACKFILL_FROM|RECONCILE_|BOOTSTRAP_COMPLETE|WARMUP_COMPLETE|SESSION_OPEN|SESSION_CLOSE|RUNTIME_STALE_RESTART|CONTRACT_SWITCH|RUNTIME_DEGRADED` su perimetro + `CAP_09_parte_9.md`. Verifica che ogni marker citato da A esista realmente in Parte 9 nel capitolo dichiarato (es. `RUNTIME_GAP_*` Cap.50, `WARMUP_COMPLETE` Cap.51, `SESSION_*` Cap.52, `RUNTIME_STALE_RESTART` Cap.51 D-9-11).
   - **`bar_synthetic` semantica**: `bar_synthetic` su perimetro + `CAP_08_parte_8.md` + `CAP_09_parte_9.md`. Verifica regola "booleano trade/no-trade, MAI live/ricostruito" (Cap.58 regola 2/3) coerente con D-9-7.
   - **Cash low/high**: `f8|f9|day_low|day_high|cash.*low|6/6 mismatch|low rado` su perimetro + STATO M-9. Verifica regola D-10-4 (cash via CANDLE ufficiale `f8`/`f9`, MAI tick realtime) e prova [PROVA-EMPIRICA 2026-06-01 V-1 afternoon §2.4.5 lettera A] in C.
   - **Immutabilita' T+3 morning**: `T\+1|T\+3|60/60|60 / 60|immutabil|rewriting|bit-identic|bit-exact` su perimetro. Verifica perimetro empirico onesto (morning, FIB6F/DITAS, T+3, ~100gg) sistematico in A blocchi RM-1 e in REPORT B.
   - **Citazioni cross-CAP** (per coerenza inter-file): `CAP_06_parte_VI.md:276|CAP_08_parte_8.md Cap.|CAP_09_parte_9.md Cap.|CAP_02_parte_II.md Cap.10` su perimetro. Verifica con Read che i referenti esistano e contengano cio' che A afferma.

   Il Reviewer documenta nell'audit la lista comandi eseguiti con esito sintetico (file/righe principali).

3. **RM-3 — fonti etichettate** (`METODO.md:97-136`). Il Reviewer verifica che:
   - ogni `[PROVA-EMPIRICA <data>]` citata in A/B abbia il dump corrispondente esistente in `probe_out/*` (verifica esistenza con `Glob probe_out/*`, NON ri-apertura del contenuto contro DAPI);
   - le 4 prove cardine (V-1 morning §2.3, V-1 afternoon §2.4, V-2 cut-off §4.2/§4.3, T+1 §2.5, schema PRICE W2 M-9) siano citate in A esattamente con i numeri canonici delle fonti (55/60 morning, 49 match / 13 mismatch su 62 afternoon, saturazione `2026-02-18 09:56` da N=80, daily senza cut-off fino N=160, 60/60 T+3 morning, cash 6/6 mismatch sul solo low DITAS, `f8`/`f9` = day_low/day_high) — eventuali numeri divergenti sono finding;
   - il wiki Directa compaia **solo** come `[WIKI-HINT, da verificare]` (atteso: Cap.64 punto 4, riavvio Darwin mezzanotte) e con dichiarazione esplicita di inaffidabilita' (RM-3 caso reale);
   - nessuna conclusione del perimetro si appoggi **solo** a livello 4: il fact-check e' "ogni asserzione strutturale ha almeno una fonte livello 1/2/3".

4. **RM-4 — output non-CAP** (`METODO.md:139-208`). Il Reviewer NON deve produrre probe nuovi ne' script nuovi: l'audit e' documento + lettura + grep. Se l'audit rivela un'asserzione del perimetro che richiede prova empirica nuova (es. immutabilita' oltre T+3, afternoon/usopen, strumento ≠ FIB6F/DITAS), questa entra nella sezione **"Empirico-CLI da verificare"** dell'audit come handoff (NON viene eseguita dentro questo task). Lista attesa **VUOTA** perche' l'empirico e' chiuso; se non vuota, il Reviewer indica esplicitamente il motivo (asserzione che eccede il perimetro empirico chiuso).

### Inputs AUTORITATIVI — fatti CHIUSI, NON ri-verificare, l'audit ne controlla l'USO

Sono livello-1 / livello-2 gia' acquisiti, citati come hard constraint da CAP-DATA-03 e gia' autoritativi dopo AUDIT-RM-RETRO CAP-DATA-01 + CAP-DATA-02 WEB+CLI chiusi PASS. Il Reviewer di questo task NON li ri-deriva. Li USA come pietre di paragone: A e/o C che li citano devono citarli **fedelmente**; eventuali divergenze sono finding.

5. **Schema CANDLE canonico `C;L;H;O;V`** = `UFF;MIN;MAX;APE;V`. Fonte level-1: V-1 morning §3.3 (PROBE_RECUPERO_GAP_DAPI). Fonte level-2: D `:467-481` (commento r.477 + assegnazioni r.478-481). Wiki Directa (`O;H;L;C`) dimostrato inesatto (RM-3 caso reale).

6. **CANDLERANGE intraday — limite ~100gg di calendario, finestra scorrevole** che tronca **al minuto** del limite (NON al giorno). Fonte level-1: V-2 dump `probe_out/v2_cutoff_period60_20260529_104927.csv` (saturazione `first_ts=2026-02-18 09:56`, 38.567 candele identica su FIB6F+DITAS+CM.MESM6 da N=80 a N=160). Fonte level-2: D `:61` `DEFAULT_INTRADAY_MAX_DAYS=100`.

7. **CANDLERANGE daily (period 86400) — nessun limite pratico a 100gg**. Fonte level-1: V-2 dump `probe_out/v2_cutoff_period86400_20260529_105739.csv` (first_ts regredisce fino al 2026-01-05 a N=160).

8. **Sintassi CANDLERANGE**: `CANDLERANGE <sym> <YYYYMMDDHHMMSS_start> <YYYYMMDDHHMMSS_end> <period_s>` (4 arg, period LAST). Fonte level-2: D `:228-230`.

9. **Equivalenza realtime ↔ CANDLERANGE confermata su due finestre indipendenti**: morning 09:00-09:30 (55/60 match tol 0.05, V-1 morning §2.3) + afternoon 14:55-15:25 (49 match / 13 mismatch su 62, V-1 afternoon §2.4); nessuno swap O/C su nessuno dei 7 FIB6F afternoon (test discriminante `local_O ≠ hist_C`); schema `C;L;H;O` regge.

10. **Immutabilita' barre intraday CANDLERANGE verificata fino a T+3 morning** sui ticker FIB6F/DITAS (T+1 §2.5: re-fetch 29/05 eseguito il 01/06 = T+3 attraverso weekend, 60/60 barre OHLCV bit-identiche). **Perimetro empirico onesto esplicito**: T+3, morning, FIB6F/DITAS, finestra ~100gg. Oltre = "assunto per estensione, sorvegliato dal gate Cap.60".

11. **Feed cash realtime rado** (~6 tick/min su DITAS): il flusso PRICE perde i minimi intraday del cash; la CANDLE ufficiale daily ha il low corretto. Fonte level-1: V-1 afternoon §2.4.5 lettera A (6/6 mismatch DITAS sul solo low).

12. **Schema PRICE realtime (M-9 W2 [PROVA-EMPIRICA 2026-06-01])**: `f4=last`, `f6=volume_cum`, `f8=day_low`, `f9=day_high`; `f5`/`f7` parziali. L'ipotesi Web "bid/ask" e' **FALSIFICATA** da W2.

13. **Codici errore DAPI** (M-3): 1004 cmd ignoto, 1007 ticker inesistente/non abilitato, 1017 sintassi malformata, 1015 data/parametro invalido, 1003 comando storico su porta realtime. 1030 realtime non sottoscritto **non riprodotto** sul FIB (servizio base IDEM). Confini disambiguati [PROVA-EMPIRICA 2026-05-29 + 2026-06-01 CLI].

14. **Cooldown "14/~30s" REFUTATO** (M-5): 850 connessioni open/close fino a ~907Hz su 10003, 0 onset. Rate-limit a regimi estremi lato server non escludibile in assoluto (ipotesi minore aperta, non costante dichiarata).

15. **BOOK_5 CERTIFICATO** (M-10 W3): `[BID×5 best-first][ASK×5 best-first]`, triplo `(lots, orders, price)`. Posizioni di `bar_synthetic` Cap.49 certificate (`bid1_lots`=campo4, `bid1_orders`=campo5, `bid1_price`=campo6; `ask1_lots`=campo19, `ask1_price`=campo21). NON pertinente al perimetro Parte 10 (backfill via CANDLERANGE, non via book replay); citato come supporto level-2 alla coerenza schema runtime certificato post-AUDIT CAP-DATA-02.

### Da `tasks/CARRYOVER.md` — raccomandazioni di processo pertinenti

16. **RACC-METODO-2** (Re-Review v2 CAP-DATA-02 RM-RETRO, finding #8, **OPEN**): *"Quando una Review/AC dichiara 'OK' sulla correttezza di uno schema-dato di un sistema esterno (DAPI, Telegram, vendor), la verifica deve includere il confronto puntuale col decoder di produzione esistente (RM-2), non la sola completezza strutturale dei campi."* Il Reviewer di questo audit la applica come **vincolo operativo**: ogni AC di B che dichiara "schema X OK" deve essere verificato non solo dalla completezza dei campi citati ma dal **diff puntuale** col decoder canonico D. CARRYOVER nota esplicitamente che RACC-METODO-2 e' gia' stata "onorata in CAP-DATA-03 (Review v1+v2)" su CANDLE/CSV legacy; questo audit **riconferma indipendentemente** che la onoranza sia effettiva e completa.

17. **RACC-METODO-1** (Re-Review v3 FONDAMENTA-01, **OPEN**): de-numerizzare rimandi residui `METODO.md:NN` / `reviewer.md:NN`. **NON pertinente al perimetro A-D** di questo audit (e' manutenzione del processo, non del documento metodologico v2). Citato per completezza del censimento; non si applica.

### Da `tasks/STATO_CORRENTE.md` §5 — M-promemoria di sessione (input critico)

Il Reviewer USA i M-promemoria di sessione come "fonte autoritativa versionata" dei fatti empirici, in alternativa all'apertura diretta dei dump in `probe_out/*` (non versionati). Sono livello-1 acquisiti.

18. **M-1**: schema CANDLE `C;L;H;O;V` — autoritativo per W1 dell'audit.
19. **M-2**: sintassi `CANDLERANGE <sym> <start> <end> <period_s>` (period ultimo) — autoritativo per W2/W4.
20. **M-3**: codici errore 1004/1007/1017/1015/1003 ri-confermati 2026-06-01 — autoritativo per il check di completezza/coerenza dei codici se A li cita; A Cap.59 r.97 li cita.
21. **M-5**: cooldown "14/~30s" refutato a 907Hz/850conn — autoritativo se A cita rate-limit.
22. **M-9**: schema PRICE `f4/f6/f8/f9`; ipotesi Web "bid/ask" falsificata — autoritativo per W7/W8 del cash low/high (regola D-10-4).
23. **M-10**: BOOK_5 certificato — supporto level-2.

### Da `.claude/CLAUDE.md` — workflow e divieti di sede CLI

24. **Workflow Review-First su perimetro esistente**: nessuna v1 Developer prima della Review. Macchina a stati Orchestratore: se la Review emette PASS, il task chiude come `AUDIT-RM CAP-DATA-03` confermativo, senza riaprire Parte 10. Se emette CONDITIONAL/FAIL, l'Orchestratore esegue il **punto di controllo supervisore** standard (tabella di classificazione `BUG REALE / MIGLIORA PERFORMANCE / NEUTRO / RISCHIO PEGGIORAMENTO`), il supervisore decide cosa va a Developer, e il Developer riceve un prompt di rework MIRATO ai soli finding approvati.

25. **Divieti di sede CLI** (`.claude/agents/reviewer.md`, ribaditi in CLAUDE.md §"Workflow per output non-CAP"): il CLI reviewer (a) NON esegue probe DAPI massivi di mero zelo; (b) verifica le citazioni `[CODICE-ESISTENTE]` leggendo i sorgenti committati con Read (sola lettura); (c) le fondamenta empiriche sono CHIUSE e NON si ri-eseguono in questo task; (d) tutto cio' che richiederebbe prova diretta DAPI live va come "Empirico-CLI da verificare" in handoff a sessione futura, NON eseguito qui. (Per coerenza con la sede WEB: il WEB reviewer NON dichiara "verificato empiricamente" niente che richieda DAPI/filesystem locale — qui non rilevante perche' siamo CLI; ma il vincolo simmetrico CLI sopra e' il vincolo attivo.)

26. **Subagent registry CLI**: in sessione CLI locale `reviewer` e' invocabile direttamente come `subagent_type`. L'Orchestratore della CLI invoca il Reviewer e lascia push diretto su `origin/main` (Push policy MEMORY).

---

## Perimetro dei file dell'audit

| ID | Path (assoluto rispetto a project root) | Ruolo | Audit |
|----|------------------------------------------|-------|-------|
| **A** | `docs/methodology_v2/CAP_10_parte_10.md` | Capitolo CAP-DATA-03 (Cap.57-Cap.65, ~10-11 pp). Oggetto primario dell'audit RM-1/2/3. | RM-1 + RM-2 + RM-3 + coerenza interna (no auto-contraddizioni, no leakage, no residui multi-indice). |
| **B** | `reports/REPORT_CAP_10.md` | Report supervisore Developer (5 sezioni + verifica AC + Iterazione 2 risposta finding). | Onesta' claim → evidenza (i 43/43 AC dichiarati OK hanno evidenza puntuale verificabile in A?); coerenza B ↔ A (B non afferma di A cose che A non dice); RM-2 sezione "Decoder/convenzioni esistenti" e' veritiera (i decoder citati esistono e contengono cio' che il REPORT afferma — `:467-481`, `:228-230`, `:61`, `:282-285`, `:605-617`, `:159`, `:230`, `:333`). |
| **C** | `tasks/PROBE_RECUPERO_GAP_DAPI.md` | Documento-sorgente empirico (prerequisito) da cui A attinge V-1/V-2/T+1. Ha **self-review RM-4 opzione A** (§"Self-review RM-4" in fondo, r.384-433). | Le citazioni di A verso C sono fedeli? Il perimetro empirico onesto (T+3 morning FIB6F/DITAS ~100gg) e' riportato correttamente da A? Il blocco self-review RM-4 di C copre realmente le sue asserzioni? Numeri canonici (49/13 afternoon, 60/60 T+3 morning, saturazione `2026-02-18 09:56` da N=80) coincidono con quelli usati da A? |
| **D** | `scripts/export_directa_history_parametric.py` | Decoder canonico di produzione (fonte CODICE-ESISTENTE level-2). Riferimento di verita' per RM-2. **NON modificabile in questo task.** | Verifica delle citazioni di A e C verso D, **leggendo D direttamente** alle righe citate: schema CANDLE `C;L;H;O;V` (`:467-481` + commento r.477), sintassi CANDLERANGE period-last (`:228-230`), `DEFAULT_INTRADAY_MAX_DAYS=100` (`:61`), terminatore `END CANDLES` (`:282-285`, `:245`, `:255`), header CSV legacy 11-campi (`:605-617`, distinto da Cap.62 esteso 13-campi di Parte 9 `:117-122`). |

**Cross-reference fuori perimetro (citate dall'audit, NON auditate come perimetro a se')**:

- `scripts/probe_dapi.py` — decoder DAPI post-rettifica `a12ae32` (CAP-DATA-01 PASS). Citato come supporto level-2 (`:230` `parse_line`, `:159` `DapiConn`, `:333` `run_candlerange`). Verificabile con Read se necessario per disambiguazione.
- `docs/methodology_v2/CAP_08_parte_8.md` — Cap.37/Cap.38/Cap.40/Cap.41/Cap.43/Cap.44. Citato come referente DOC-INTERNO; il Reviewer verifica con Read le righe citate quando A le richiama puntualmente.
- `docs/methodology_v2/CAP_09_parte_9.md` — Cap.45/Cap.46/Cap.47/Cap.48/Cap.49/Cap.50/Cap.51/Cap.52/Cap.54/Cap.55/Cap.56. Verifica con Read i marker citati (`RUNTIME_GAP_*`, `WARMUP_*`, `SESSION_*`, `RUNTIME_STALE_RESTART` = D-9-11, dominio `source` D-9-5, `L_warmup=30gg` D-9-NB4, header CSV runtime esteso 13 campi Cap.48).
- `docs/methodology_v2/CAP_06_parte_VI.md:276` — riga critica della Iterazione 2 NB-1 (test che il fix v2 non ha sostituito un errore con un altro). Verifica con Read riga 276 ("L'alert non chiude il loop di re-training").
- `docs/methodology_v2/CAP_02_parte_II.md:23,131` — replay deterministico bit-exact (Cap.10).
- `tasks/STATO_CORRENTE.md` §5 M-1/M-3/M-9/M-10 — versione M-promemoria delle prove empiriche, autoritativa.
- `tasks/CARRYOVER.md` riga RACC-METODO-2 — vincolo operativo per AC su schemi esterni.

---

## Inventario W — asserzioni a rischio nel perimetro A-D (lista iniziale, il Reviewer estende nel secondo giro)

Il Reviewer parte da questa lista, la **estende** durante l'audit (e' normale e atteso scoprire asserzioni W aggiuntive durante la lettura; al modello degli AUDIT-RM-RETRO 01/02 sono emerse asserzioni Wn+1, Wn+2 in corsa). Ogni voce dell'inventario va auditata con il framework dei Check A-E della sezione successiva.

| ID | Asserzione del perimetro | File:linea (citazione iniziale) | Test RM rilevante |
|----|---------------------------|----------------------------------|-------------------|
| **W1** | Schema CANDLE canonico `C;L;H;O;V` = `UFF;MIN;MAX;APE;V` come fonte di verita' del backfill | A Cap.59 step 3 r.89 `[CODICE-ESISTENTE :467-481]`; A Cap.65 D-10-* dipendenza implicita; B sez. "Decoder esistenti" + AC-59-2; C §3.2-§3.6 + §7.2 + Self-review §"Grep RM-2"; **D `:467-481` canonico** | RM-2 puntuale + coerenza A/C ↔ D (verificare riga-per-riga r.471 split + r.477 commento + r.478-481 assegnazioni); RM-1 implicito (asserzione e' "CONFERMATO" perche' `[CODICE-ESISTENTE]` level-2 e [PROVA-EMPIRICA] V-1) — nessun blocco 4-righe richiesto se l'asserzione e' una citazione level-2 verificata, ma l'audit verifica che il documento NON dichiari "schema CANDLE verificato" senza il riferimento level-2 |
| **W2** | Cut-off intraday CANDLERANGE ~100gg di calendario, finestra scorrevole, tronca al minuto (saturazione `2026-02-18 09:56` da N=80, 38.567 candele) | A Cap.59 r.79-82 (blocco RM-1 cut-off) `[PROVA-EMPIRICA V-2 dump probe_out/v2_cutoff_period60_*]`; B AC-59-3; C §4.2 tabella N=50..160; **D `:61` `DEFAULT_INTRADAY_MAX_DAYS=100`** | RM-1 formato 4-righe + sostanza (alternative escluse: "limite al giorno intero" escluso dal minuto-preciso, "limite specifico di period 60" escluso dalla simultaneita' 3 ticker); RM-2 D `:61`; RM-3 [PROVA-EMPIRICA] livello-1 + [CODICE-ESISTENTE] livello-2 |
| **W3** | CANDLERANGE daily (period 86400) — nessun limite pratico fino N=160 (first_ts regredisce al 2026-01-05) | A Cap.61 r.168-171 (blocco RM-1 daily) `[PROVA-EMPIRICA V-2 dump probe_out/v2_cutoff_period86400_*]`; B AC-61-1; C §4.3 | RM-1 formato 4-righe + sostanza ("alternative escluse: limite a 100gg anche sul daily"); RM-3 livello-1; coerenza con W2 (intraday vs daily distinti) |
| **W4** | Sintassi CANDLERANGE `CANDLERANGE <sym> <YYYYMMDDHHMMSS_start> <YYYYMMDDHHMMSS_end> <period_s>` (period LAST, 4 arg) | A Cap.59 step 2 r.88 `[CODICE-ESISTENTE :228-230]`; B sez. "Decoder esistenti" + AC-59-2; C §2.2/§2.4.3/§4.1; **D `:228-230`** | RM-2 puntuale (verificare token-per-token `f"CANDLERANGE {symbol} {start} {end} {period_seconds}"` a `:228-230`) |
| **W5** | Equivalenza realtime ↔ CANDLERANGE confermata su 2 finestre indipendenti (morning 55/60 + afternoon 49 match/13 mismatch su 62), schema regge, nessuno swap O/C su nessuno dei 7 FIB6F afternoon (test discriminante `local_O ≠ hist_C`) | A Cap.59 r.103-106 (blocco RM-1 equivalenza/immutabilita'); B AC-59-4 + AC-GO-2; C §2.3 + §2.4.4 + §2.4.5 + §3.3-§3.4 | RM-1 formato 4-righe + sostanza (alternative escluse: path-inference/distorsione vol/swap O/C; non escluse: low cash rado, oltre T+3 non testato, afternoon/usopen non testato, strumenti ≠ FIB6F/DITAS non testato); numeri canonici coincidenti tra A e C |
| **W6** | Immutabilita' barre intraday CANDLERANGE entro T+3 morning (60/60 OHLCV bit-identiche), perimetro empirico onesto (morning, FIB6F/DITAS, T+3, ~100gg) | A Cap.59 r.103-106 + Cap.62 vincolo idempotenza/immutabilita' r.207-208; B AC-GO-2 + Decisione D-10-2/D-10-8; C §2.5 | RM-1 perimetro onesto sistematicamente dichiarato ("ALTERNATIVE NON ESCLUSE: oltre T+3 non testato, afternoon/usopen non testato, strumenti ≠ FIB6F/DITAS non testato"); D-10-2/D-10-8 motivazione coerente |
| **W7** | Cash low/high via CANDLE ufficiale `f8`/`f9`, MAI tick realtime (6/6 mismatch DITAS sul solo low; densita' ~6 tick/min) | A Cap.60 r.123 step 5 + Cap.60 r.135-139 (blocco RM-1 cash); B AC-60-3 + D-10-4; C §2.4.5 lettera A; STATO M-9 W2 | RM-1 formato 4-righe + sostanza (alternative escluse: low realtime corretto sul cash, swap di schema; NON escluse: densita' ~6 tick/min stima, DGER/DSTX50/DFRA assunti per estensione, FIB futures non si applica); RM-3 [PROVA-EMPIRICA] livello-1 + cross-check con M-9 W2 (ipotesi Web "bid/ask" falsificata) |
| **W8** | Schema PRICE realtime `f4=last, f6=volume_cum, f8=day_low, f9=day_high`; `f5`/`f7` parziali (cross-check daily CANDLE; hypothesis Web "bid/ask" falsificata da BOOK_5 simultaneo) | A Cap.60 step 5 r.123 `[PROVA-EMPIRICA W2 M-9]`; STATO M-9 | RM-1 sostanza (verifica parziale dichiarata per `f5`/`f7`); citazione "ipotesi Web falsificata" coerente con M-9 |
| **W9** | Schema CSV runtime esteso 13 campi (`symbol, timeframe, timestamp, date, time, open, high, low, close, volume, tick_count, bar_synthetic, source`) — Cap.62 r.185 + dominio `source` esteso a 6 valori (3 ereditati Parte 9 + 3 nuovi `BACKFILL_FROM_*`) | A Cap.62 r.185 + tabella domino source r.196-204 (6 righe); B AC-62-1/AC-62-2 + D-10-6/D-10-7; **A Cap.62/Cap.64 referenzia legacy D `:605-617` 11-campi vs runtime esteso 13-campi di Parte 9 Cap.48 r.117-122** | RM-2: distinzione legacy-11 (`:605-617` D) vs runtime-esteso-13 (Cap.48 Parte 9 r.117-122) DEVE essere accurata; RM-1: domain `source` esteso come complemento (non sostituto) coerente con D-9-5 invariato |
| **W10** | Codici errore DAPI (1004/1007/1017/1015/1003) come trigger del backoff e marker `RUNTIME_DEGRADED` (Cap.59 r.97) — semantica esatta dei singoli codici dichiarata "verifica parziale ereditata da Parte 9 Cap.50" | A Cap.59 "Vincoli operativi" r.96-97 `[PROVA-EMPIRICA 2026-05-29 + 2026-06-01 CLI]`; STATO M-3 | RM-1 sostanza: A dichiara "verifica parziale ereditata"? Coerente con M-3 (5 codici ri-confermati 01/06; 1030 non riprodotto); e' onesto NON re-claim semantica completa |
| **W11** | Marker normativi Parte 10 complementari (no sovrapposizione con Parte 9): `RUNTIME_GAP_BEYOND_100D` (Cap.59 cut-off), `BACKFILL_VERIFIED_T3`/`BACKFILL_UNVERIFIED` (Cap.59 step 4), `RECONCILE_SCHEMA_FAIL` (Cap.60 step 3), `BACKFILL_FROM_CANDLERANGE` (Cap.59 step 5), `BACKFILL_FROM_ARCHIVE`/`BACKFILL_FROM_PORTARA` (Cap.61), `BOOTSTRAP_COMPLETE` (Cap.61), `RECONCILE_OK/DIVERGENT_FIB/DIVERGENT_HIGHLOW/DEGRADED` (Cap.60 step 6) | A Cap.58 r.62 (dopo OM-2 fix v2) + Cap.59 + Cap.60 + Cap.61 + Cap.65 tabella D-10-*; B sez. Misura prima/dopo "Marker complementari" + AC-GO-4; cross-reference con Parte 9 Cap.50/51/52/54 | Coerenza cross-CAP: Parte 9 marker citati esistono e dicono quello che A afferma (Read `CAP_09_parte_9.md` Cap.50 r.224,229,233; Cap.51 r.257,259-263; Cap.52 r.299; Cap.54 catalogo); marker Parte 10 sono complementari (zero sovrapposizione semantica); fix OM-2 v2 (i sotto-marker in-body sono dichiarati esplicitamente in-body, NON tutti in Cap.65) regge |
| **W12** | Citazione cross-CAP critica `CAP_06_parte_VI.md:276` (post-fix NB-1 v2 — gate Cap.60 bloccante a differenza del monitoraggio non-bloccante di Cap.30) | A Cap.57 r.42 + Cap.60 r.126 + Cap.65 D-10-3 r.250; B "Iterazione 2 — NB-1" + Misura prima/dopo + AC-60-2 | RM-2 + coerenza inter-file (la riga 276 di CAP_06 contiene verbatim "L'alert non chiude il loop di re-training"); il fix v2 non ha sostituito un errore con un altro; nessuna citazione nuova non verificata altrove |
| **W13** | Invariante research = runtime esteso al ciclo di vita del tape (non solo singolo bar); `bar_synthetic` resta booleano trade/no-trade per barre ricostruite; provenienza in `source`; non-mutativita' riconciliazione | A Cap.57 + Cap.58 regola 2/3 + Cap.60 r.146 "non-mutativa"; B AC-T-5 + AC-GO-1/AC-GO-3 + D-10-3 | Coerenza con D-9-7 (Parte 9 Cap.49 r.181); replay deterministico Parte II Cap.10 preservato; nessuna asimmetria live/storico introdotta |
| **W14** | Onesta' claim → evidenza degli AC del REPORT B (43/43 OK): ogni "OK" ha file:linea verificabile in A | B tabella verifica AC (27 per-cap + 12 AC-T + 4 AC-GO) | Audit randomizzato + esaustivo sui sotto-insiemi a rischio (AC-59-2/3/4/5, AC-60-2/3/5, AC-61-2/3/4, AC-62-1/2/4, AC-T-1/2/3/4, AC-GO-1/2/3/4); RACC-METODO-2 (vincolo operativo); ogni AC su schema esterno DEVE avere il diff col decoder canonico gia' onorato (CARRYOVER stato OPEN — e' gia' onorata in CAP-DATA-03 v1/v2 sul CAP, l'audit RICONFERMA su perimetro esteso B) |
| **W15** | Self-review RM-4 di C (r.384-433): copre realmente le asserzioni (a) afternoon + (b) immutabilita' T+3 morning; grep RM-2 documentato; etichette RM-3; assunzioni non testate dichiarate; lista file letti | C §"Self-review RM-4" + commit `687c744` | RM-4 opzione A applicata: blocco 4-righe asserzione (a) + asserzione (b) presente; grep RM-2 eseguito su pattern del dominio; etichette RM-3 livello 1/2/4 corrette; assunzioni non testate (es. finestra 14:55-15:25 rappresentativa di "afternoon") esplicite |

Il Reviewer estende l'inventario nel secondo giro ostile. Asserzioni emerse vanno numerate W16, W17, ... e auditate con lo stesso framework.

---

## I Check A-E del Reviewer

Ispirato direttamente al framework AUDIT-RM-RETRO CAP-DATA-01/02 (v1+v2+CLI) adattato al perimetro A-D di CAP-DATA-03.

### Check A — RM-1 (formato 4-righe + sostanza) per ogni asserzione W

Per ogni Wi dell'inventario:
- **A.1 Localizzazione**: cita la riga esatta del file dove l'asserzione compare (`<file>:<linea>` con citazione testuale del costrutto).
- **A.2 Formato**: l'asserzione ha il blocco 4-righe `VERIFICA / PROVE / ALTERNATIVE COMPATIBILI ESCLUSE / ALTERNATIVE COMPATIBILI NON ESCLUSE` quando si presenta come "verificato / confermato / fatto / dimostrato / stabilito"? Se l'asserzione e' una citazione level-2 (`[CODICE-ESISTENTE]`) verificata, il blocco 4-righe **non e' obbligatorio** ma la verifica del referente si'. Se manca dove dovrebbe esserci: **BUG REALE (formale RM-1)**.
- **A.3 Sostanza**: le ALTERNATIVE COMPATIBILI ESCLUSE sono **effettivamente escluse** dai dati osservati? Le NON ESCLUSE sono **davvero compatibili**? Eventuali ipotesi non escluse spacciate per escluse: **BUG REALE (sostanziale RM-1)**.
- **A.4 Patch suggerita** (testuale; il Reviewer NON patcha A/B/C): cosa il Developer dovrebbe correggere se finding e' approvato dal supervisore (riformulazione del blocco RM-1, aggiunta etichetta, citazione mancante, ecc.).
- **A.5 Confronto empirico** con inputs autoritativi #5..#15: l'asserzione contraddice o ridichiara correttamente la fonte autoritativa? Eventuali contraddizioni: **BUG REALE catastrofico** (analogamente a W1 di CAP-DATA-02 RM-RETRO). Eventuali asserzioni che dichiarano "verificato universalmente" cio' che gli inputs limitano a un perimetro empirico (T+3 morning FIB6F/DITAS): **BUG REALE (sostanziale RM-1)**.

### Check B — RM-2 (grep + citazioni di codice verso D-canonico)

- **B.1 Grep** dei pattern del dominio (lista in eredita' #2) eseguito **dal Reviewer stesso** e citato nell'audit (comando + esito sintetico file:riga).
- **B.2 Verifica file:linea**: per ogni citazione `[CODICE-ESISTENTE <path>:<linea>]` nel perimetro, leggere il file alla riga citata e verificare token-per-token che il costrutto dichiarato esista. **Tabella obbligatoria** stile review v1 CAP-10 (vedi `REVIEW_CAP_10_review.md:70-80`):

  | Citazione nel perimetro | File:linea | Contenuto atteso | Esito verifica |
  |---|---|---|---|

- **B.3 Coerenza A/C ↔ D canonico**: per ogni schema/format DAPI dichiarato in A o C, confrontare con D **leggendo D**. Schemi a rischio: CANDLE `C;L;H;O;V` (D `:467-481`), sintassi CANDLERANGE period-last (D `:228-230`), `DEFAULT_INTRADAY_MAX_DAYS=100` (D `:61`), terminatore `END CANDLES` (D `:282-285`, `:245`, `:255`), header CSV legacy 11-campi (D `:605-617`). Eventuali divergenze: **BUG REALE** (analogamente a W1 CAP-DATA-02).
- **B.4 RACC-METODO-2**: per ogni AC di B che dichiara "schema X OK" con riferimento a un sistema esterno, **diff puntuale col decoder canonico D e' onorato**? (verifica che B non si sia limitato alla completezza strutturale dei campi citati).
- **B.5 Decoder pre-esistenti non citati**: c'e' un decoder/parser/codec gia' nel repo per il dominio DAPI che il perimetro avrebbe dovuto citare ma non cita? (lookup con grep sui pattern di dominio + lettura risultati). Se si': **MIGLIORA PROCESSO** (RM-2 incompleto).

### Check C — RM-3 (etichettatura fonti per livello)

- **C.1 Etichette presenti**: ogni evidenza nel perimetro ha la sua etichetta `[PROVA-EMPIRICA <data>]` / `[CODICE-ESISTENTE r.NNN]` / `[DOC-INTERNO <path>]` / `[WIKI-HINT, da verificare]`? Etichette assenti dove servono: **MIGLIORA PROCESSO**.
- **C.2 Livello adeguato**: conclusioni del perimetro che si appoggiano **solo** a livello 4 (wiki) senza supporto da livelli 1/2/3: **BUG REALE (RM-3)**. Wiki Directa atteso solo come `[WIKI-HINT, da verificare]` con dichiarazione esplicita di inaffidabilita'.
- **C.3 Numeri canonici**: i numeri empirici citati in A (55/60, 49/13, saturazione `2026-02-18 09:56`, N=80→160, 60/60 T+3 morning, 6/6 DITAS sul solo low, 38.567 candele, 14h×60min=840 barre) coincidono coi numeri in C e/o STATO M-1/M-3/M-9? Eventuali discrepanze: **BUG REALE** (numero falso, da correggere).
- **C.4 Dump esistenti**: per ogni `[PROVA-EMPIRICA <data>]` citata da A o B, il dump corrispondente esiste in `probe_out/*` (verifica con Glob, sola esistenza, NON apertura/ricomputo).
- **C.5 Perimetro empirico onesto**: A dichiara sistematicamente il perimetro empirico nei blocchi RM-1 ("ALTERNATIVE NON ESCLUSE: oltre T+3 / afternoon-usopen / strumenti ≠ FIB6F-DITAS")? Eventuali "verificato universalmente" senza qualificatore di perimetro: **BUG REALE (sostanziale RM-1)**.

### Check D — Coerenza inter-file (A ↔ B ↔ C ↔ D + cross-CAP)

- **D.1 Citazioni di A verso C** (es. "[PROVA-EMPIRICA V-1 afternoon §2.4.5 lettera A — 6/6 mismatch DITAS sul solo low]"): C effettivamente contiene §2.4.5 lettera A con 6/6 mismatch DITAS sul solo low? Verifica con Read.
- **D.2 Citazioni di A verso D**: i ranges `:467-481`, `:228-230`, `:61`, `:282-285`, `:605-617` ESISTONO e contengono i costrutti dichiarati (vedi Check B.2).
- **D.3 Citazioni cross-CAP** di A verso `CAP_06_parte_VI.md:276`, `CAP_08_*`, `CAP_09_*`, `CAP_02_*`: i referenti esistono e contengono cio' che A afferma. Verifica con Read i 5-10 referenti piu' critici (Cap.30 r.276 verbatim, marker `RUNTIME_GAP_*` Cap.50, dominio `source` D-9-5 Cap.48, `L_warmup=30gg` D-9-NB4 Cap.51, replay deterministico Cap.10).
- **D.4 Coerenza B ↔ A**: ogni AC dichiarato OK dal REPORT con evidenza "Cap.X step Y" punta a una riga di A che effettivamente lo soddisfa.
- **D.5 Coerenza C ↔ A**: la self-review RM-4 di C copre realmente le asserzioni (a) afternoon (49/13 + nessuno swap O/C) e (b) immutabilita' T+3 morning (60/60 morning T+0 vs T+3); i numeri di C coincidono con quelli di A.
- **D.6 Coerenza interna A**: nessuna auto-contraddizione (es. tassonomia 4-tier coerente fra Cap.58 e Cap.65; marker Parte 10 ↔ enum manifest 1:1 fra Cap.60 step 6 e Cap.62 r.192 dopo fix OM-3 v2).

### Check E — Onesta' claim → evidenza (specifico per B, applicato per scrupolo anche ad A)

- **E.1 AC del REPORT (B) — 43/43 OK ribaditi v2**: campionamento sistematico (audit a tappeto sugli AC a rischio + audit randomizzato sugli altri). Per ogni AC controllato: `OK` → evidence in A → contenuto in A copre l'AC? Eventuali AC "OK" senza evidenza in A (vuoto, generico, o errato): **BUG REALE (onesta' claim → evidenza)**.
- **E.2 Iterazione 2 REPORT**: le correzioni NB-1, OM-1, OM-2, OM-3 dichiarate chiuse hanno regredito? (Verifica grep `Brier` su A (atteso 0 match — vedi REVIEW_CAP_10_v2_review.md r.22) e cross-check di OM-2 → distinzione marker principali vs in-body in Cap.58 r.62).
- **E.3 Domande aperte REPORT**: il Developer dichiara "Nessuna"; verifica che non ci siano effettivamente Q-XX aperte in `tasks/QUESTIONS.md` pertinenti al perimetro.
- **E.4 Criterio di rollback REPORT**: per ogni decisione D-10-1..D-10-10 il rollback e' registrato in REPORT (vedi sezione "Criterio di rollback") con motivazione coerente con Cap.65 r.259-267.

---

## Acceptance criteria — tutti verificabili, devono essere soddisfatti per PASS

L'audit emette PASS solo se TUTTI i seguenti sono soddisfatti. CONDITIONAL/FAIL se anche uno non lo e' e il finding e' BUG REALE / MIGLIORA PERFORMANCE / RISCHIO PEGGIORAMENTO.

- [ ] **AC-1 (RM-1 perimetro A)**: ogni asserzione del CAP A del tipo "verificato / confermato / fatto / dimostrato / stabilito" ha il blocco 4-righe RM-1 con formato esatto E sostanza non smentita dagli inputs autoritativi #5..#15. Atteso: 4 blocchi RM-1 in A (Cap.59 cut-off r.79-82, Cap.59 equivalenza/immutabilita' r.103-106, Cap.60 cash r.135-139, Cap.61 daily r.168-171), tutti `compliant`. Eventuali asserzioni "verificato" in prosa libera fuori dai 4 blocchi: identificate e classificate.

- [ ] **AC-2 (RM-2 grep + citazioni D)**: il Reviewer ha eseguito grep dei pattern del dominio e citato comando + esito; ogni citazione `[CODICE-ESISTENTE]` del perimetro (A + B + C nella self-review §"Grep RM-2") e' verificata token-per-token leggendo D alle righe esatte; le 6 citazioni cardine in B (`:467-481`, `:228-230`, `:61`, `:282-285`, `:605-617`, `:230` probe_dapi, `:159/:333` probe_dapi) sono confermate o segnalate. Tabella `Citazione | File:linea | Contenuto atteso | Esito` obbligatoria. RACC-METODO-2 onorata (diff col decoder canonico per ogni AC su schema esterno).

- [ ] **AC-3 (RM-3 fonti etichettate)**: ogni evidenza nel perimetro e' etichettata col livello corretto; nessuna conclusione si appoggia solo a livello 4 (wiki); wiki Directa compare solo come `[WIKI-HINT, da verificare]` con dichiarazione esplicita di inaffidabilita' (atteso: A Cap.64 punto 4 riavvio Darwin). Numeri canonici cross-file coincidenti.

- [ ] **AC-4 (coerenza inter-file)**: citazioni di A verso C/D/cross-CAP fedeli ai referenti (verifica con Read); auto-coerenza di A (nessuna contraddizione interna fra Cap.58 e Cap.65, fra Cap.60 step 6 e Cap.62 r.192 dopo OM-3); coerenza B ↔ A (43/43 AC ribaditi v2 OK con evidenza puntuale verificata) e C ↔ A (numeri canonici, self-review RM-4 di C copre afternoon + T+3).

- [ ] **AC-5 (onesta' claim → evidenza B)**: campione di almeno 15 AC su 43 verificato direttamente leggendo A; nessun AC dichiarato OK senza evidenza puntuale nel CAP A.

- [ ] **AC-6 (correzioni Iterazione 2 reggono)**: NB-1 (Brier sparito 0 match grep su A); OM-1 (notazione 49 match/13 mismatch su 62 a Cap.59 r.104); OM-2 (Cap.58 r.62 distingue marker principali vs in-body); OM-3 (Cap.62 r.192 corrispondenza marker↔enum manifest 1:1). Nessuna regressione, fix accurati e non sostituiti con altri errori (es. la citazione `CAP_06_parte_VI.md:276` e' verbatim corretta).

- [ ] **AC-7 (Self-review RM-4 in C)**: blocco self-review §"Self-review RM-4 (opzione A)" di C (r.384-433) copre realmente le asserzioni (a) equivalenza afternoon + (b) immutabilita' T+3; ha formato 4-righe RM-1 per ogni asserzione; grep RM-2 eseguito su `parse_directa_candle|parse_line|run_candlerange|UFF|APE|DapiConn`; etichette RM-3 corrette; assunzioni non testate (es. "finestra 14:55-15:25 rappresentativa di afternoon" come "assunto, non dimostrato") dichiarate esplicite.

- [ ] **AC-8 (RM-1 applicato al Reviewer)**: ogni "CONFERMATO ESATTO" / "MATCH" / "verificato esatto" / "non trovato dopo grep" del Reviewer ha sostegno operativo (citazione + esito); sezione finale "Applicazione RM-1 a me stesso" e' presente come nelle review v1/v2 CAP-10 (`REVIEW_CAP_10_review.md:149-153`).

- [ ] **AC-9 (Lista "Empirico-CLI da verificare" esplicita)**: attesa **VUOTA** (l'empirico e' chiuso). Se non vuota: il Reviewer indica esplicitamente quale asserzione del perimetro eccede il perimetro empirico chiuso e perche' richiederebbe DAPI live in sessione futura (NON eseguita qui).

- [ ] **AC-10 (Tabella classificazione per il supervisore)**: per ogni finding del Reviewer, riga in tabella con `# | Problema | file:riga | Classificazione | Mandare a Development?`; classificazione fra `BUG REALE` / `MIGLIORA PERFORMANCE` / `NEUTRO` / `RISCHIO PEGGIORAMENTO` (i 4 valori standard); se nessun finding: dichiarazione esplicita "Nessun finding — perimetro A-D RM-compliant".

- [ ] **AC-11 (Verdetto motivato PASS / CONDITIONAL / FAIL)**: verdetto in apertura con motivazione sintetica (≤3 righe); regola di decisione applicata: PASS se 0 BUG REALE e 0 MIGLIORA PERFORMANCE/RISCHIO PEGGIORAMENTO bloccanti; CONDITIONAL se finding non bloccanti ma da decidere col supervisore; FAIL solo se BUG REALE bloccante.

- [ ] **AC-12 (Naming + path output)**: file di review pubblicato a `reviews/REVIEW_CAP_DATA_03_RM_AUDIT_review.md` (NON "RETRO" — il task e' confermativo, non retroattivo). Commit dell'audit con tag `[REVIEW] CAP-DATA-03 RM-AUDIT — verdetto: <PASS|CONDITIONAL|FAIL>`.

- [ ] **AC-13 (audit indipendente, non copia-incolla di v1/v2)**: il Reviewer NON riproduce verbatim sezioni della review v1/v2; usa v1/v2 come **input di consapevolezza** (sa cosa e' gia' stato controllato — 4 finding NEUTRO chiusi) e si concentra su (a) verificare che i fix v2 reggano (E.2), (b) audit RM trasversale **esteso al perimetro A-D** che v1/v2 hanno toccato meno (B come perimetro a se', C come perimetro a se' incluso il self-review, D come fonte di verita' leggibile). Indipendenza dichiarata esplicitamente nel verdetto.

---

## Out-of-scope esplicito

NON entrano in questo audit. Per ciascuno: motivazione e destinazione.

- **Ri-derivare l'empirico (V-1 morning/afternoon, V-2 cut-off, T+1=T+3 immutabilita', W1-W11 codici/mesi/cooldown/BOOK_5)**. **Destinazione**: chiusi in CAP-DATA-01 PASS + CAP-DATA-02 AUDIT-RM-RETRO PASS WEB+CLI + PROBE_RECUPERO_GAP_DAPI committato. Il Reviewer USA i M-1/M-3/M-5/M-9/M-10 + i numeri canonici di PROBE come inputs autoritativi, non li ri-misura.
- **Micro-patch Cap.49 di Parte 9** (eventuale tocco di tabella Cap.49 emerso in audit CAP-DATA-02). **Destinazione**: sotto-task separato del supervisore, NON parte del perimetro A-D di Parte 10 di questo audit. Se il Reviewer rileva incidentalmente che la mappatura Cap.49 si e' propagata in citazioni del perimetro A-D, segnala come finding "MIGLIORA PROCESSO — coerenza inter-CAP" SENZA proporre patch a CAP-DATA-02.
- **Riapertura metodologia / 43 AC del task card di sviluppo CAP-DATA-03**. **Destinazione**: gia' verificati indipendentemente in v1/v2 (entrambe sede CLI). Questo audit verifica **trasversalmente la conformita' RM** al perimetro A-D, non re-valuta il merito metodologico del capitolo.
- **Riapertura decisioni D-10-1..D-10-10**. **Destinazione**: chiuse in Cap.65 con criteri di rollback in REPORT B. L'audit verifica che siano dichiarate correttamente con RM-1 dove l'oggetto e' una verifica empirica (D-10-2 idempotenza T+3 morning, D-10-4 cash low/high via CANDLE ufficiale), non ne mette in discussione il merito normativo.
- **Cross-index PHASE-2** (DAX, EuroStoxx 50, ES, MES futures). **Destinazione**: Parte 10 Cap.64 dichiara fuori scope; PHASE-2 e' perimetro autonomo (task Planner separato in futuro).
- **Esecuzione DAPI**. **Destinazione**: vincolo di sede CLI — niente probe massivi di mero zelo; lista "Empirico-CLI da verificare" attesa VUOTA (l'empirico e' chiuso); se non vuota, handoff a sessione CLI futura.
- **Modifica dei file del perimetro A/B/C/D in v1**. **Destinazione**: il Reviewer NON patcha (regola assoluta di Reviewer). Eventuali fix approvati dal supervisore dopo il punto di controllo → Developer in rework con prompt mirato; D non si modifica MAI.
- **Apertura di Q-XX nuove in `tasks/QUESTIONS.md`**. **Destinazione**: l'audit NON apre nuove Q-XX (e' un audit confermativo); eventuali ambiguita' reali emerse durante l'audit vanno classificate come finding nella tabella supervisore, non come Q-XX (a meno che siano ambiguita' non risolvibili dai documenti del progetto — nel qual caso il Reviewer si ferma e il Planner apre Q-XX).
- **Cross-CAP integrale Parte 8/9/VI/II**. **Destinazione**: l'audit verifica le citazioni che A fa verso questi CAP (Check D.3), NON re-audita Parte 8/9/VI/II integralmente.
- **Migrazione formato legacy → esteso dei 391 dump live**. **Destinazione**: A Cap.64 dichiara fuori scope (operazione una-tantum FASE-D).
- **Implementazione codice operativo pipeline runtime backfill/riconciliazione/archiviazione**. **Destinazione**: A Cap.64 + REPORT dichiarano fuori scope (FASE-D del roadmap).

---

## Done when — domande operative a cui l'audit risponde

L'audit chiude con un report che risponde univocamente a queste domande:

1. **RM-1 formato**: tutti i 4 blocchi RM-1 di A (Cap.59 r.79-82, r.103-106; Cap.60 r.135-139; Cap.61 r.168-171) hanno formato esatto `VERIFICA/PROVE/ALTERNATIVE COMPATIBILI ESCLUSE/ALTERNATIVE COMPATIBILI NON ESCLUSE`? Esistono altre asserzioni "verificato/confermato/fatto" in A fuori dai 4 blocchi (in prosa libera) e sono in forma RM-1-compliant o no?
2. **RM-1 sostanza**: in ognuno dei 4 blocchi RM-1, le ALTERNATIVE COMPATIBILI ESCLUSE sono effettivamente escluse dai dati osservati (e quali dati lo escludono, file:dump:timestamp)? Le NON ESCLUSE sono davvero compatibili? Il perimetro empirico onesto (T+3, morning, FIB6F/DITAS, ~100gg) e' dichiarato sistematicamente o ci sono "verificato universalmente" non qualificati?
3. **RM-2 grep**: il Reviewer ha eseguito i grep dei pattern del dominio (lista in eredita' #2)? Comando + esito sintetico per ognuno? Decoder pre-esistenti non citati dal perimetro che avrebbero dovuto essere?
4. **RM-2 D-canonico**: ogni citazione `[CODICE-ESISTENTE D:NNN]` nel perimetro corrisponde alla riga esatta di D? Lo schema CANDLE `C;L;H;O;V` di D `:467-481` e' citato fedelmente in A/B/C? La sintassi CANDLERANGE period-last `:228-230` e' citata fedelmente? `DEFAULT_INTRADAY_MAX_DAYS=100` `:61` e' citato fedelmente? Header CSV legacy 11-campi `:605-617` e' distinto correttamente da runtime esteso 13-campi di Parte 9 Cap.48?
5. **RM-2 RACC-METODO-2**: ogni AC del REPORT che dichiara "schema X OK" ha il diff puntuale col decoder canonico gia' onorato?
6. **RM-3 etichettatura**: ogni `[PROVA-EMPIRICA <data>]` / `[CODICE-ESISTENTE r.NNN]` / `[DOC-INTERNO <path>]` / `[WIKI-HINT, da verificare]` e' presente dove serve? Nessuna conclusione si appoggia solo a livello 4? Wiki Directa compare solo come hint?
7. **RM-3 numeri canonici**: i numeri empirici di A (55/60, 49/13, saturazione `2026-02-18 09:56`, N=80→160, 60/60 T+3 morning, 6/6 DITAS sul solo low, 14h×60min=840 barre) coincidono con quelli di C e STATO M-1/M-3/M-9? Eventuali divergenze identificate?
8. **Coerenza inter-file**: citazioni A → C, A → D, A → cross-CAP (`CAP_06:276`, `CAP_08_*`, `CAP_09_*`, `CAP_02_*`) verificate con Read? Coerenza interna di A (Cap.58 ↔ Cap.65 marker, Cap.60 step 6 ↔ Cap.62 manifest dopo OM-3) preservata?
9. **Onesta' claim → evidenza B**: i 43/43 AC dichiarati OK in REPORT hanno evidenza puntuale in A? Campionamento di almeno 15 AC controllato direttamente. Nessuna evidenza vuota/generica/errata?
10. **Iterazione 2 v2 regge**: NB-1 (Brier sparito), OM-1 (notazione 49/13), OM-2 (Cap.58 r.62), OM-3 (Cap.62 r.192) confermati; nessuna regressione; nessun fix che sostituisce un errore con un altro?
11. **Self-review C**: il blocco RM-4 di C (r.384-433) copre realmente afternoon + T+3 con formato 4-righe per ogni asserzione?
12. **Lista Empirico-CLI**: vuota (atteso), oppure motivata se non vuota?
13. **Classificazione per il supervisore**: tabella di finding con classificazione finale; oppure dichiarazione "Nessun finding"?
14. **Verdetto**: PASS / CONDITIONAL / FAIL con motivazione e regola di decisione applicata?
15. **Indipendenza dichiarata**: il Reviewer dichiara esplicitamente di NON aver copia-incollato v1/v2, e indica come ha esteso l'audit al perimetro A-D rispetto al solo CAP A delle review precedenti?

---

## Pipeline attesa

**Modalita' Review-First su perimetro esistente**:

```
Planner (questo task card)
  ↓ Orchestratore committa task card
Reviewer v1 (CLI, audit indipendente sul perimetro A-D)
  ↓ verdetto PASS / CONDITIONAL / FAIL
  ↓ se PASS → chiusura task (audit confermativo)
  ↓ se CONDITIONAL/FAIL → punto di controllo supervisore con tabella classificazione finding
Eventuale rework Developer (solo finding approvati; D NON si tocca; A/B/C eventualmente)
  ↓ Reviewer v2 → ... → PASS
Chiusura sessione + notifica
```

L'Orchestratore di sessione:
- Letto il task card, invoca direttamente il **Reviewer** (subagent `reviewer` se disponibile nativamente in CLI, oppure general-purpose adottando `.claude/agents/reviewer.md`).
- Allega al prompt del Reviewer: il path di questo `ACTIVE_TASK.md` + la dichiarazione di **sede CLI** + i **divieti per sede CLI** (no probe massivi di zelo, no DAPI; verifica via Read del codice committato; lista "Empirico-CLI" attesa VUOTA).
- A esito Reviewer: se PASS, chiude la sessione lasciando il task card storico; se CONDITIONAL/FAIL applica il punto di controllo standard CLAUDE.md §"Punto di controllo supervisore obbligatorio dopo CONDITIONAL/FAIL".

**Vincoli per il Reviewer della v1**:

- NON ri-esegue probe DAPI (fondamenta empiriche CHIUSE — inputs autoritativi #5..#15).
- NON modifica A/B/C/D (vincolo assoluto Reviewer).
- USA i numeri canonici degli inputs autoritativi come pietre di paragone, NON ri-misura contro DAPI.
- Applica RM-1 a se' stesso: ogni "CONFERMATO ESATTO" ha sostegno operativo nell'audit (citazione + esito).
- Verifica via Read le righe citate di D (`scripts/export_directa_history_parametric.py`) e dei cross-CAP critici (`CAP_06_parte_VI.md:276`, marker Parte 9 Cap.50/51/52/54).
- Estende l'inventario W se durante la lettura emergono asserzioni W16, W17, ... non previste.
- Produce il file `reviews/REVIEW_CAP_DATA_03_RM_AUDIT_review.md` con la struttura standard degli AUDIT-RM (header con perimetro A-D, inventario W, Check A-E per ogni Wi, lista "Empirico-CLI", tabella classificazione supervisore, AC, applicazione RM-1 a se').
- Push diretto su `origin/main` con tag commit `[REVIEW] CAP-DATA-03 RM-AUDIT — verdetto: <PASS|CONDITIONAL|FAIL>`.

**In caso di rework Developer (se supervisore approva finding)**:

- L'Orchestratore aggiorna questo `ACTIVE_TASK.md` con sezione "Finding di Review da risolvere" (solo finding approvati).
- Developer riceve prompt mirato; modifica A e/o B e/o C; **NON modifica D**; aggiorna `00_indice.md` se necessario (es. Parte 10 status); aggiorna REPORT B con sezione "Iterazione N — risposta ai finding di Review" con prima→dopo + misura prima/dopo + impatto GA.
- Reviewer v2 verifica chiusura finding + nessuna regressione (analogamente alla v2 CAP-10 sede CLI gia' fatta).

---

## Self-review del Planner (RM-1 applicata al task card stesso)

In coerenza con `tasks/METODO.md` RM-1 e con l'eredita' che il Planner pone come premesse, qui dichiaro esplicitamente:

- **VERIFICATO (level-2)** che le 6 citazioni cardine di D usate come pietre di paragone (`:467-481`, `:228-230`, `:61`, `:282-285`, `:605-617`, `:245/:255`) corrispondono al contenuto di `scripts/export_directa_history_parametric.py` letto in questa sessione (Read righe 1-90, 100-300, 460-622). Specificamente: r.471 contiene `kind, symbol, ymd, hms, uff, min_, max_, ape, qty = parts[:9]`; r.477 contiene il commento `# Documentazione Directa: UFF, MIN, MAX, APE => close, low, high, open.`; r.478-482 contengono le assegnazioni `close_v/low_v/high_v/open_v/volume_v`; r.228-230 contiene `f"CANDLERANGE {symbol} {start_dt.strftime(DIRECTA_TS_FMT)} {end_dt.strftime(DIRECTA_TS_FMT)} {period_seconds}"` (period last); r.61 contiene `DEFAULT_INTRADAY_MAX_DAYS = 100`; r.605-617 contiene `fieldnames=[...]` 11 campi `symbol, timeframe, timestamp, date, time, open, high, low, close, volume, source` (NO `tick_count` e NO `bar_synthetic`); r.245 e r.255 contengono le regole "accetto buffer raccolto" su timeout/socket-close dopo dati. **ALTERNATIVE COMPATIBILI ESCLUSE**: nessun decoder candle alternativo in D (D contiene `parse_directa_candle` unico a `:467-481`); nessuna definizione dell'header CSV alternativa in D (l'header e' solo a `:605-617`). **NON ESCLUSE**: non ho letto integralmente le ~620 righe di D; possono esserci righe non lette con costrutti rilevanti per asserzioni W non ancora identificate — e' normale e atteso che il Reviewer durante l'audit estenda l'inventario W.

- **VERIFICATO (level-2 via Read parziale)** che la review v2 CAP-10 (`reviews/REVIEW_CAP_10_v2_review.md` r.1-80) conferma fix NB-1 (Brier 0 match), OM-1 (49/13 → "49 match / 13 mismatch su 62 minuti"), OM-2 (Cap.58 r.62 distinzione marker principali vs in-body), OM-3 (Cap.62 r.192 mappatura 1:1 manifest↔marker). La review v2 PASS e' fonte autoritativa per AC-6 del task card. **NON ESCLUSE**: non ho riletto integralmente A v2 in questa sessione di Planner (CAP_10_parte_10.md letto r.1-219 + r.220-268, quasi integrale ma il Reviewer rilegge per scrupolo); il Reviewer durante l'audit DEVE rileggere A e ri-verificare per scrupolo (E.2).

- **VERIFICATO (per costruzione del task card)** che CARRYOVER.md riga RACC-METODO-2 nota "onorata in CAP-DATA-03 v1+v2" e' una dichiarazione **del Planner CAP-DATA-03 dopo-PASS**, non un fatto auto-verificato; il Reviewer di questo audit la **riconferma** o la segnala come incompleta (B.4 RACC-METODO-2 onorata in modo COMPLETO sui 43 AC?).

- **AMBIGUITA' POTENZIALI** che ho risolto come Planner (NON Q-XX, perche' non sono ambiguita' non risolvibili dai documenti):
  - Naming output Reviewer: `REVIEW_CAP_DATA_03_RM_AUDIT_review.md` (NON `RETRO`, perche' Parte 10 e' post-RM e l'audit e' confermativo, non un recupero di debito).
  - Workflow Review-First (non c'e' Developer in v1 — Parte 10 e' gia' PASS, c'e' solo audit RM trasversale).
  - Sede CLI (non richiesta WEB dal supervisore; audit e' documento + lettura + grep, niente DAPI).
  - Lista Empirico-CLI attesa VUOTA (l'empirico e' chiuso ed e' hard constraint).

- **NON dichiarato come "verificato" dal Planner**:
  - Non ho letto integralmente B (REPORT_CAP_10.md tutto letto in 214 righe — verifica completa attesa al Reviewer per E.1).
  - Non ho letto C integralmente in questa sessione di Planner (PROBE r.1-433 letto integralmente, ma il Reviewer rilegge per cross-check con A).
  - I 43/43 AC ribaditi v2 sono presi come **autoritativi dalla review v2 PASS gia' fatta**: il Reviewer di questo audit NON li ri-valuta nel merito, ma campionamento sostantivo dell'onesta' claim → evidenza in B (E.1) e' obbligatorio.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
