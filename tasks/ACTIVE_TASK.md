# TASK ATTIVO: AUDIT-RM-RETRO CAP-DATA-01 — audit retroattivo RM-1/2/3 del perimetro A-D

**Assegnato da**: Planner
**Output atteso primario**: `reviews/REVIEW_CAP_DATA_01_RM_RETRO_review.md` (verdetto PASS / CONDITIONAL / FAIL del Reviewer Web sul perimetro A-D)
**Output atteso secondario (solo se CONDITIONAL/FAIL approvato dal supervisore)**: fix mirati ai soli file del perimetro A-D approvati, prodotti dal Developer in una iterazione di rework
**Stato**: IN ATTESA
**Workflow**: **Review-First** (il perimetro esiste già su `origin/main`; vanno auditate retroattivamente le regole RM-1/2/3 che sono state introdotte DOPO la sua produzione)
**Sede del Reviewer**: **WEB** (perimetro = file versionati su repo + grep di codice committato; nessuna esecuzione contro DAPI in questo task)
**Natura del task**: NON è un capitolo metodologico CAP-XX. NON è una CAP-review piena nuova (Parte 8 è già PASS storico, hash review `015c47a` v2). NON è una probe-review classica (qui auditiamo simultaneamente un CAP storico + 3 output non-CAP correlati). È un **audit RM-1/2/3 retroattivo mirato** + coerenza script↔testo sul perimetro A-D.

---

## Obiettivo

Verificare, applicando retroattivamente le regole `RM-1 / RM-2 / RM-3` di `tasks/METODO.md`, che le asserzioni di tipo "verificato / confermato / stabilito / fatto N" presenti nei 4 file del perimetro A-D (CAP_08_parte_8.md, REPORT_CAP_08.md, scripts/probe_dapi.py, tasks/HANDOFF_PROBE_DAPI_20260528.md):

1. **rispettino il formato 4-righe** `VERIFICA / PROVE / ALTERNATIVE ESCLUSE / ALTERNATIVE NON ESCLUSE` di `METODO.md` §RM-1, OPPURE — quando il formato 4-righe non è esigibile in retroazione perché i file sono pre-RM — abbiano almeno **enumerazione esplicita delle alternative compatibili coi dati osservati** e dichiarazione dell'evidenza che le esclude;
2. **siano coerenti** con i decoder esistenti di produzione nel repo (`scripts/export_directa_history_parametric.py:477` come riferimento canonico per lo schema CANDLE, ma anche altri eventuali decoder/parser DAPI presenti), come richiesto da `METODO.md` §RM-2;
3. **non si appoggino come fonte autorevole** alla wiki Directa o ad altra documentazione esterna di livello 4, in violazione di `METODO.md` §RM-3 (ordine di priorità delle fonti `1>2>3>4`);
4. **siano coerenti tra di loro** all'interno del perimetro (in particolare: lo script `probe_dapi.py` afferma lo stesso schema dichiarato nei capitoli/handoff? L'HANDOFF 28/05 dichiara fatti che lo script poi rinnega? Il CAP_08 cita prove empiriche che esistono davvero al livello corretto?).

L'audit ha **due finalità** simultanee:

- **Finalità retroattiva (gate metodologico)**: chiudere il debito di `RM-4` retroattivo sui 3 output non-CAP (B, C, D) committati prima dell'introduzione di RM-4, secondo la logica dei task `AUDIT-RECUPERO-<nome>` di `.claude/CLAUDE.md` §"Chiusura sessione PASS" / §"L'Orchestratore della NUOVA sessione" (verifica blocco self-review opzione A o probe-review opzione B; se entrambe mancano per uno qualunque, apertura task di recupero — è il caso che qui consolidiamo in un unico task A-D).
- **Finalità di salute dati corrente**: identificare se l'errore CANDLE già noto (schema reale `C;L;H;O;V`) ha lasciato **residui** in altre asserzioni del perimetro che NON sono ancora state rettificate. Esempio canonico: le 5 "scoperte critiche" oltre 3.1 dell'HANDOFF 28/05 (sintassi CANDLERANGE, terminatore `END CANDLES`, codici errore 1004/1007/1017/1030, convenzione mese F/I, cooldown 30s/14 connessioni) sono dichiarate con metodologia di verifica omogenea a quella che ha prodotto l'errore CANDLE: vanno passate al setaccio RM-1.

Il task NON risponde a: validità complessiva di CAP-DATA-01 come capitolo metodologico (è già PASS hash `015c47a`, non si riapre); audit di CAP-DATA-02 (Parte 9) o CAP-DATA-03 (sessioni separate); audit dei capitoli I-VII; correttezza empirica di asserzioni che richiedono prova diretta contro DAPI live (sede CLI; il Web reviewer le marca "Empirico-CLI da verificare" e produce eventuale handoff alla sede CLI).

Il task si fa adesso perché RM-1/2/3/4 sono state introdotte (commit `7bb2955`/`de2938d`/`916278a` del 2026-05-28) DOPO la produzione del perimetro A-D (Parte 8 chiusa PASS il 2026-05-27 con hash `015c47a`; HANDOFF 28/05 e probe_dapi.py committati in zona pre-RM senza alcun reviewer formale, come riconosciuto da `METODO.md` §RM-4 "Caso reale che ha motivato la regola"). FONDAMENTA-01 ha chiuso il gate **ex-ante** per il futuro; questo task chiude il debito **ex-post** sul perimetro A-D. Prima che PROBE_RECUPERO_GAP_DAPI.md venga compilato e che CAP-DATA-03 venga aperto, è necessario sapere quali asserzioni del perimetro corrente reggono al setaccio RM-1/2/3 e quali sono ancora "compatibili con i dati ma non verificate".

---

## Eredità obbligatoria

### Da `tasks/METODO.md` (testo vincolante, NON riaprire)

1. **RM-1** — formato 4-righe `VERIFICA / PROVE / ALTERNATIVE ESCLUSE / ALTERNATIVE NON ESCLUSE` (`METODO.md:28-33`). Asserzioni "verificato" senza enumerazione esplicita delle alternative compatibili coi dati osservati = BUG REALE. Asserzioni "verificato" in **prosa libera** anche con alternative enumerate = "non in formato" (BUG REALE secondo `reviewer.md:17, 56, 114`). Sui file del perimetro pre-RM, l'audit applica il criterio sostanziale (enumerazione + esclusione) e segnala separatamente la non-conformità al formato 4-righe come MIGLIORA PROCESSO se la sostanza è OK, BUG REALE se anche la sostanza manca.
2. **RM-2** — grep nel repo prima di assumere format esterno (`METODO.md:46-94`). Il Reviewer esegue **direttamente** `grep -rn` su pattern del dominio DAPI per verificare se decoder esistenti nel repo sono coerenti col perimetro o lo contraddicono. Decoder canonico già noto: `scripts/export_directa_history_parametric.py:477` (commento `# UFF, MIN, MAX, APE => close, low, high, open`).
3. **RM-3** — ordine di priorità fonti `1>2>3>4` (`METODO.md:97-136`). Etichette obbligatorie `[PROVA-EMPIRICA <data>]` / `[CODICE-EXISTENTE r.NNN]` / `[DOC-INTERNO]` / `[WIKI-HINT, da verificare]`. Conclusione "wiki-only" senza supporto dai livelli 1-3 = BUG REALE.
4. **RM-4** — review obbligatoria per output non-CAP determinanti. Sui file C (script di parsing/decoder DAPI) e D (handoff con "fatti verificati") l'opzione B (probe-review formale) era obbligatoria secondo il criterio (a) di `CLAUDE.md` §"Workflow per output non-CAP" — entrambi rientrano in (a) "introduce un decoder/parser di sistema esterno". Sono stati committati invece senza alcuna review (riconosciuto in `METODO.md:200-202`). Questo task chiude retroattivamente quel debito producendo l'audit mancante.

### Da `.claude/CLAUDE.md` (workflow di sessione)

5. Workflow Review-First per output esistenti: niente Developer in v1. L'Orchestratore della sessione corrente invoca direttamente il Reviewer in modalità adattata (audit RM-1/2/3 retroattivo del perimetro A-D, sede WEB). Il verdetto del Reviewer determina la presenza o assenza di una fase Developer di rework.
6. Modifiche ai file del perimetro NON sono autorizzate senza approvazione esplicita del supervisore al punto di controllo CONDITIONAL/FAIL. Lo script `probe_dapi.py` è nel perimetro come **oggetto auditato**, non come oggetto da modificare in Iterazione 1.
7. Push diretto a `origin/main` autorizzato (push policy MEMORY): il Reviewer pusha il file di review committato; l'eventuale Developer di rework pusha le patch dei file del perimetro approvate.

### Da `tasks/CARRYOVER.md` (M-promemoria carryover di capitolo) e `tasks/STATO_CORRENTE.md` (M-promemoria di sessione)

8. **M-1 di STATO_CORRENTE.md** (riga 64): "schema CANDLE reale = `UFF;MIN;MAX;APE;V` = `C;L;H;O;V`, NON `O;L;H;C`. V-1 ha provato lo swap O/C su daily O e C non erano distinguibili (solo L/H lo erano), per questo l'errore era passato. `export_directa_history_parametric.py` era già corretto → dump storici NON affetti. Fix nel decoder `probe_dapi.py` in `a12ae32`." Questa rettifica copre `probe_dapi.py` (file C) e parzialmente l'HANDOFF 28/05 §3.1 (file D, dove è stata appiccicata una "RETTIFICA 2026-05-29" in cima alla §3.1, ma il vecchio testo errato è preservato come "storia"). Il Reviewer verifica che la rettifica sia stata applicata in **tutti** i punti del perimetro che la richiedevano (non solo §3.1 dell'handoff), e — punto chiave — che le **altre 5 scoperte** dell'handoff (§3.2-§3.6) siano state passate al setaccio RM-1 con la stessa metodologia che ha smascherato l'errore §3.1, o restino sospette.
9. **M-2..M-8 di STATO_CORRENTE.md** (righe 65-71): sintassi CANDLERANGE, codici errore, convenzione mese, cooldown 30s/14 connessioni, account `B6086`, settle CME pomeridiano, bug encoding `cp1252`. Sono potenziali asserzioni RM-1 da auditare nei file del perimetro (in particolare C e D li dichiarano come "fatti scoperti").
10. **CARRYOVER.md** (M-2 OPEN su latenza Telegram per Appendice E, e tutti gli altri M-promemoria CAP-XX) NON è pertinente a questo task (l'audit è A-D, non Parte 9 né capitoli precedenti). Nessun M-promemoria di capitolo viene chiuso da questo task. RACC-METODO-1 (`CARRYOVER.md:46`) NON è pertinente al perimetro A-D.

### Caso reale che ha motivato l'audit (paradigma di test, NON riaprire)

11. Commit `7bb2955` sessione web 2026-05-28 ha prodotto C (588 righe) + D (207 righe) + 6 "fatti verificati" senza alcun reviewer. L'errore §3.1 (schema CANDLE) è stato scoperto solo il giorno dopo dalla sessione CLI con V-1 (commit `a12ae32`). Il pattern: dichiarazione "verificato" su test che non distingue tutte le permutazioni compatibili → omissione del grep di codice esistente → wiki Directa trattato come fonte autorevole emendabile → output non-CAP mai revisionato → errore in `main` come fact-of-truth. Il Reviewer **usa questo pattern come banco di prova**: per ogni asserzione del perimetro, simula il test "esiste un'altra permutazione compatibile coi dati osservati che la sessione ha dichiarato esclusa senza prova?".

---

## Perimetro — 4 file (A, B, C, D) con naming effettivo del repo

Il Reviewer auditta **esclusivamente** questi 4 file, citando posizioni puntuali (file:linea). Nessun altro file del repo entra nel perimetro normativo (la lettura di altri file è ammessa solo come supporto evidenziale, es. grep su `scripts/` per validare RM-2, lettura di `tasks/METODO.md` per riferimento alle regole, lettura di `tasks/STATO_CORRENTE.md` e `tasks/CARRYOVER.md` come supporto al censimento M-promemoria).

| ID | Path assoluto nel repo | Ruolo | Note di mappatura |
|----|------------------------|-------|-------------------|
| A | `docs/methodology_v2/CAP_08_parte_8.md` | CAP-DATA-01 = Parte 8 = "Convenzione dati storici e politica di rollover". Hash review PASS storica: `015c47a` (v2). | Naming canonico nel repo: `CAP_08_parte_8.md`. Identifier interno "Parte 8" (arabo). NON si auditta come capitolo metodologico (già PASS); si auditta SOLO per RM-1/2/3 retroattivo. |
| B | `reports/REPORT_CAP_08.md` | Report supervisore del Developer di CAP-DATA-01. Contiene "Decisioni rilevanti", "Verifica esplicita degli Acceptance Criteria", e in coda la "Iterazione 2 — risposta ai finding di Review v1". | Il REPORT spesso dichiara "OK" come esito di AC: il Reviewer verifica che ogni "OK" non sia stato auto-dichiarato dal Developer senza prova RM-1 (è essenzialmente un'autodichiarazione, che però NON è asserzione su sistema esterno: i finding rilevanti qui sono se cita "verificato schema CANDLE" o simili). |
| C | `scripts/probe_dapi.py` | Script di parsing/decoder DAPI. Output non-CAP critico (commit originale `7bb2955`; fix schema CANDLE in `a12ae32`). | È il file dove l'errore CANDLE è nato. Audit di coerenza interna (docstring vs decoder), coerenza esterna (decoder vs `export_directa_history_parametric.py`), e RM-1 sulle asserzioni nei commenti (es. righe 7-29 docstring, righe 182-187 nel parser CANDLE). |
| D | `tasks/HANDOFF_PROBE_DAPI_20260528.md` | Handoff fra sessioni con 6 "fatti verificati" (§3.1-§3.6). §3.1 è stata rettificata 29/05 in cima, ma il vecchio testo errato è preservato sotto. §3.2-§3.6 NON sono mai state riauditate dopo l'incidente CANDLE. | Test canonico RM-1: la metodologia di verifica delle altre 5 scoperte è la stessa che ha prodotto l'errore §3.1? Se sì, almeno un finding "verifica parziale". |

**Cross-reference fuori perimetro ammesse**:
- `scripts/export_directa_history_parametric.py:477` come decoder canonico CODICE-ESISTENTE (citabile, non auditabile in questo task);
- `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md` Appendici A/B (citato da C e D come fonte interna delle scoperte; il Reviewer può aprirlo per **verificare** se le Appendici A/B contengono prove empiriche che supportano le asserzioni di D §3.2-§3.6 a livello-3, oppure se anche le Appendici sono livello-4-only — questa cross-reference è essenziale per il giudizio RM-3 su §3.2-§3.6);
- `tasks/PROBE_RECUPERO_GAP_DAPI.md` se esiste già una versione committata (questo task del Reviewer NON la auditta, la cita solo come supporto evidenziale per la rettifica §3.1);
- altri file decoder/parser che emergano dal grep RM-2.

**Cross-reference esplicitamente FUORI scope**:
- canonicizzazione delle asserzioni DAPI in Parte 9 (CAP-DATA-02): le citazioni RM-1 "schema CANDLE / CANDLERANGE / codici errore / mesi IDEM F/I/Mar/Dic" appartengono canonicamente alla Parte 9, che resta PASS e NON si auditta in questo task. Se il Reviewer trova in C/D un'asserzione che dovrebbe canonicamente vivere in Parte 9 e non in A, lo segnala come MIGLIORA PROCESSO (suggerimento di rinvio canonico) ma NON come BUG REALE.

---

## Lavoro atteso dal Reviewer (audit indipendente, sede WEB)

Il Reviewer produce **un singolo file** `reviews/REVIEW_CAP_DATA_01_RM_RETRO_review.md` con verdetto PASS / CONDITIONAL / FAIL e classificazione dei finding per il supervisore (BUG REALE / MIGLIORA PERFORMANCE / NEUTRO / RISCHIO PEGGIORAMENTO — categorie standard di `reviewer.md`; "PROCESSO" usato come sotto-etichetta di MIGLIORA quando il finding non incide sul GA ma sul gate metodologico).

**Header obbligatorio del file di review** (mappatura A-D esplicita):
```
# Review AUDIT-RM-RETRO CAP-DATA-01 (Parte 8) — perimetro A-D

**Sede**: WEB
**Natura**: audit retroattivo RM-1/2/3 (NON CAP-review piena, NON probe-review standard)

**Perimetro auditato**:
- A = docs/methodology_v2/CAP_08_parte_8.md
- B = reports/REPORT_CAP_08.md
- C = scripts/probe_dapi.py
- D = tasks/HANDOFF_PROBE_DAPI_20260528.md
```

### Inventario di partenza delle asserzioni a rischio (checklist iniziale, NON esaustiva)

Il Reviewer parte da questo elenco di asserzioni dichiarate o citate nel perimetro che sono potenzialmente sensibili a RM-1/2/3, e poi cerca anche asserzioni fuori da questo elenco trovate in modo indipendente nel primo e secondo giro.

| ID | Asserzione (paradigma) | File primario | Test RM-N rilevante |
|----|------------------------|---------------|---------------------|
| W1 | "Schema CANDLE = `C;L;H;O;V`" e varianti rettificate (`UFF;MIN;MAX;APE;V`) | C (righe 7-13, 182-204), D (§3.1) | RM-1 (alternative `{O;L;H;C, C;L;H;O, O;H;L;C, ...}` enumerate ed escluse?), RM-2 (citato `export_directa_history_parametric.py:477`?), RM-3 (wiki Directa etichettato `[WIKI-HINT]`?) |
| W2 | "Sintassi `CANDLERANGE <sym> <yyyyMMddHHmmss_start> <yyyyMMddHHmmss_end> <period_s>` con period_s ULTIMO" | C (righe 15-16, 269), D (§3.2) | RM-1 (test che ha escluso permutazioni alternative dell'ordine argomenti documentato?), RM-3 (livello fonte) |
| W3 | "Terminatore stream history = `END CANDLES`" | C (riga 14, 75), D (§3.3) | RM-1 (alternative compatibili: maiuscolo/minuscolo, trailing newline, presenza di altri marker simultanei?), RM-3 |
| W4 | Codici errore DAPI 1004 / 1007 / 1017 / 1030 con semantica dichiarata | C (righe 17-21), D (§3.4) | RM-1 (test che ha escluso semantica alternativa? quali comandi hanno prodotto ciascun codice?), RM-3 |
| W5 | Convenzione mese Directa-IDEM `F`=Giugno, `I`=Settembre (e `?`=Mar/Dic da decodificare) | C (riga 22), D (§3.5) | RM-1 (parziale dichiarata = OK; il "da decodificare" è correttamente "non verificato"?), RM-3 |
| W6 | "Pattern socket persistente, cooldown ~30s dopo 14a connessione consecutiva" | C (righe 27-29), D (§3.6) | RM-1 (qual è il test che ha dato 14? misurazioni? alternative compatibili — 12, 13, 15?), RM-3 |
| W7 | "Limite empirico ~100 giorni intraday DAPI" come "cosa cerchiamo" V-2 | D (§5.5 riga 168) | RM-1 (citato come ipotesi, non come fatto verificato — verificare che D non lo dichiari come fatto) |
| W8 | "Banner `DARWIN_STATUS;CONN_OK;TRUE` atteso" | C (riga 46) | RM-1, RM-3 |
| W9 | Convenzione ticker IDEM `<CODE><YEAR><MONTH>` (es. FIB6F) vs Eurex `EU.<CODE><MONTH><YEAR>` vs CME `CM.<CODE><MONTH><YEAR>` | C (righe 23-26) | RM-1 (test che ha distinto le 3 convenzioni? alternative compatibili escluse?), RM-3 |
| W10 | Coerenza script-corretto (C) vs handoff-stale (D) sullo schema CANDLE | C (correct `C;L;H;O;V`) vs D §3.1 (rettifica 29/05 in cima + vecchio testo `O;L;H;C` preservato sotto come "storia") | RM-1 di coerenza inter-file; verificare se il "preservato per storia" è chiaramente etichettato come errato (non come fatto) |

Il Reviewer è **libero di estendere** questo inventario nel secondo giro ostile (cfr. `reviewer.md:60-65`): asserzioni fuori lista che soddisfano un test RM-1/2/3 producono finding aggiuntivi con la stessa classificazione.

### Check A — RM-1 per ogni asserzione del perimetro

Per ogni asserzione presente nel perimetro A-D che dichiara o implica "verificato / confermato / stabilito / fatto N / scoperto N":

- **A.1 Localizzazione**: file:linea esatta, citazione testuale fra virgolette;
- **A.2 Formato 4-righe**: l'asserzione è in formato `VERIFICA/PROVE/ALTERNATIVE ESCLUSE/ALTERNATIVE NON ESCLUSE`? Se NO, classificare la non-conformità di formato (per file pre-RM è naturalmente assente: classificare come MIGLIORA PROCESSO se la sostanza è OK, BUG REALE se anche la sostanza manca — vedi A.3);
- **A.3 Sostanza** (criterio centrale): l'asserzione **enumera esplicitamente** le alternative compatibili coi dati osservati e **dichiara l'evidenza che le esclude**? Se NO, è BUG REALE (asserzione "verificato" senza esclusione di alternative — il pattern canonico CANDLE).
- **A.4 Verifica parziale opportuna**: se l'asserzione lascia alternative compatibili non escluse, andrebbe riscritta come "verifica parziale" o `X ∈ {opt_a, opt_b}`? Suggerire patch testuale concreta.

Per W10 (coerenza inter-file): il Reviewer verifica che il vecchio testo errato dell'HANDOFF §3.1 sia inequivocabilmente etichettato come "superato" (non come "storia preservata", che è ambiguo se un lettore distratto può confonderlo con un fatto valido).

### Check B — RM-2 grep nel repo e coerenza script↔testo

Il Reviewer esegue **direttamente** in sede WEB il grep canonico:

```
grep -rn "parse_directa\|parse_candle\|decode_candle\|UFF\|APE\|CANDLERANGE\|CANDLE;\|PRICE;\|BOOK_5;\|ANAG;\|END CANDLES" --include='*.py' --include='*.md' .
```

(o varianti equivalenti). Esito atteso registrato nel report:
- elenco dei decoder/parser DAPI esistenti nel repo con path:linea (riferimento canonico atteso: `scripts/export_directa_history_parametric.py:477`);
- verifica che il decoder in C (`scripts/probe_dapi.py:164-252`, sezione `parse_line`) sia **coerente** col decoder canonico (riga 477 di `export_directa_history_parametric.py`): stesso schema, stesse mapping `UFF→close, APE→open, MIN→low, MAX→high`. **Divergenza nello schema = BUG REALE** (qualunque divergenza, anche se il decoder canonico fosse esso stesso sbagliato — in tal caso il rilievo è "incoerenza inter-decoder nel repo, richiede consolidamento");
- verifica che B (REPORT) non contenga asserzioni che riformulano lo schema CANDLE divergendo dal decoder canonico.

Il Reviewer cita nel proprio report **il grep effettivamente eseguito** (comando + esito) per soddisfare `METODO.md:64-71` (formato obbligatorio "Decoder/parser esistenti nel repo per <sistema>").

### Check C — RM-3 etichettatura fonti

Per ogni riferimento del perimetro a documentazione esterna (wiki Directa, Telegram Bot API, Eurex docs, CME docs, Portara docs, ecc.) o a fonti interne:

- **C.1**: il riferimento è etichettato `[WIKI-HINT, da verificare]` / `[CODICE-EXISTENTE r.NNN]` / `[PROVA-EMPIRICA <data>]` / `[DOC-INTERNO]`?
- **C.2**: se NO (etichetta assente, pre-RM), il Reviewer **deduce il livello** della fonte e segnala l'omissione di etichetta come MIGLIORA PROCESSO (le etichette non esistevano quando il file è stato scritto).
- **C.3**: ESISTONO conclusioni "wiki-only" nel perimetro (es. "il wiki dice X, quindi X")? Se sì, BUG REALE (`METODO.md:112` "una conclusione basata solo sul livello 4 senza supporto dai livelli 1-3 è inammissibile").
- **C.4**: ESISTONO citazioni del wiki Directa nel perimetro? Verificare specificamente che sia trattato come hint da verificare, non come fonte autorevole emendabile (il pattern §3.1 originale).

### Check D — coerenza inter-file del perimetro A-D

- **D.1**: A (CAP_08) cita fatti DAPI come "verificato in CAP-DATA-02" o simile? In caso, verificare che la citazione cross-CAP sia coerente con lo stato attuale (CAP-DATA-02 contiene davvero la prova RM-1?). NB: il Reviewer NON auditta CAP-DATA-02; verifica solo che le citazioni di A verso Parte 9 puntino a sezioni esistenti e plausibilmente RM-1-compliant.
- **D.2**: B (REPORT) dichiara di aver "verificato AC X" — il Reviewer verifica che le evidenze citate (file:linea) puntino davvero al contenuto dichiarato. NON è audit del contenuto degli AC (è già PASS), ma audit della **mappatura claim → evidenza** (criterio 4 della probe-review, `reviewer.md:120`).
- **D.3**: C e D divergono su qualunque fatto DAPI (schema, sintassi, codici, mesi, cooldown)? La divergenza è esplicitamente etichettata in entrambi come "rettificata 29/05" o resta ambigua?
- **D.4**: D dichiara "fatti verificati" mai più rettificati dopo l'incidente CANDLE — in particolare §3.2-§3.6. Il Reviewer applica a ciascuna lo stesso filtro RM-1 di §3.1: la verifica ha enumerato le alternative compatibili?

### Check E — onestà claim→evidenza (criterio 4 della probe-review, `reviewer.md:120`)

Per ogni "fatto N" / "scoperta N" dell'HANDOFF e dei commenti in C, il Reviewer richiede una **evidenza puntuale citabile**: file:linea di un dump empirico, timestamp di un test, commento di un decoder di produzione, sezione di un'Appendice interna. Asserzioni senza ancora a evidenza specifica = BUG REALE (asserzioni "in aria").

### Asserzioni che richiedono prova empirica → handoff alla sede CLI

In coerenza con la matrice di sede di `METODO.md` §RM-4 e con il divieto `reviewer.md:163` (il Web reviewer NON dichiara "verificato empiricamente" niente che richieda accesso a DAPI live o filesystem locale), il Reviewer marca **come "Empirico-CLI da verificare"** ogni asserzione del perimetro la cui verifica RM-1 richiede:
- esecuzione di un comando contro DAPI (es. ri-test del cooldown 14 connessioni di W6; ri-test della sintassi `CANDLERANGE` con permutazioni alternative degli argomenti di W2; ri-test dei codici errore di W4 con comandi ad hoc; SUB di un ticker trimestrale per decodificare `?`=Mar/Dic di W5);
- ispezione di dump locali non versionati (`probe_out/`, `exports/directa_history/`, `C:\directa_history_parametric_export_overlay\`);
- riproduzione di un test V-1/V-2 con parametri specifici.

La lista "Empirico-CLI da verificare" alla fine dell'audit è l'eventuale input di una **sessione CLI separata** (vedi §"Pipeline attesa" sotto). In sede WEB il verdetto **non si chiude come PASS** se la lista CLI è non vuota (CONDITIONAL con motivazione, o PASS-condizionato-a-CLI).

---

## Acceptance criteria — tutti devono essere soddisfatti per PASS in Review

- [ ] **AC-1**: il file `reviews/REVIEW_CAP_DATA_01_RM_RETRO_review.md` esiste, è committato e pushato su `origin/main`, contiene l'header con mappatura A=CAP_08_parte_8.md / B=REPORT_CAP_08.md / C=scripts/probe_dapi.py / D=tasks/HANDOFF_PROBE_DAPI_20260528.md, e contiene un verdetto esplicito PASS / CONDITIONAL / FAIL.
- [ ] **AC-2 (Check A — RM-1)**: ogni asserzione "verificato / confermato / stabilito / fatto N / scoperto N" dei 4 file è elencata con file:linea + citazione testuale + esito A.1/A.2/A.3/A.4. L'inventario W1..W10 è coperto integralmente come baseline (cella popolata per ognuno: presente/assente nel file, esito RM-1). Asserzioni trovate fuori dall'inventario W1..W10 sono aggiunte come W11+.
- [ ] **AC-3 (Check B — RM-2)**: il grep canonico è eseguito direttamente dal Reviewer e il comando + esito sono citati nel report. Il decoder di `probe_dapi.py:164-252` è confrontato con `export_directa_history_parametric.py:477`: coerente / divergente con esito puntuale. La sezione "Decoder/parser esistenti nel repo per DAPI" è popolata secondo `METODO.md:64-71`.
- [ ] **AC-4 (Check C — RM-3)**: ogni riferimento a wiki Directa nel perimetro è elencato con file:linea, classificato per livello di fonte (4 con etichetta o dedotto), e valutato per conformità all'ordine di priorità `1>2>3>4`. Eventuali conclusioni "wiki-only" sono marcate BUG REALE.
- [ ] **AC-5 (Check D — coerenza inter-file)**: divergenze C↔D (specialmente W10 schema CANDLE) sono identificate ed etichettate; mappatura claim→evidenza per B (REPORT) è verificata; citazioni cross-CAP di A verso Parte 9 sono validate per esistenza del referente (non per correttezza del contenuto di Parte 9).
- [ ] **AC-6 (Check E — onestà)**: ogni "fatto verificato" di D (§3.1-§3.6) e ogni asserzione dichiarata nei commenti docstring di C (righe 7-29) ha un'evidenza puntuale citabile (file:linea / test:risultato / dump:timestamp) o è marcata come "senza evidenza puntuale" (BUG REALE).
- [ ] **AC-7 (lista Empirico-CLI)**: il Reviewer pubblica esplicitamente la sezione "Empirico-CLI da verificare" con elenco delle asserzioni che richiedono prova diretta contro DAPI o ispezione di dump locali. Se la lista è vuota → vincolo CLI sciolto. Se non vuota → la lista è completa con ID asserzione (W-N), motivazione del rinvio e test minimo proposto.
- [ ] **AC-8 — tabella di classificazione per il supervisore** con colonne `# | Problema | File:linea | Classificazione (BUG REALE / MIGLIORA PERFORMANCE / NEUTRO / RISCHIO PEGGIORAMENTO) | Modifica suggerita`. Niente proposte di modifica generiche: ogni riga indica file e sezione, con suggerimento di patch testuale concreta (o esplicita astensione: "il Reviewer non propone fix; richiede decisione del supervisore").
- [ ] **AC-9 (RM-1 applicato a sé stesso)**: nessuna asserzione "verificato X" nel REPORT del Reviewer senza enumerazione delle alternative considerate. Esempio: se il Reviewer dichiara "verificato che il decoder di probe_dapi.py r182-204 è coerente con export_directa_history_parametric.py r477", deve enumerare cosa significa "coerente" e quali divergenze sono state cercate ed escluse.
- [ ] **AC-10 (RM-2 applicato a sé stesso)**: il grep di Check B è eseguito e citato; nessuna conclusione su "decoder esistenti" senza grep diretto.
- [ ] **AC-11 (RM-3 applicato a sé stesso)**: ogni riferimento del REPORT del Reviewer a documenti del perimetro è citato con file:linea, non parafrasato. Nessuna conclusione si appoggia a "ricordo del file" senza file:linea.
- [ ] **AC-12 (nessuna modifica al perimetro in Iterazione 1)**: il Reviewer NON modifica i 4 file del perimetro né alcun file del repo che non sia il proprio file di review. Working tree del Reviewer pulito su A/B/C/D al momento del commit della review.
- [ ] **AC-13 (verdetto motivato)**: il PASS si concede solo se:
  - (a) tutte le asserzioni del perimetro passano A.3 (sostanza RM-1: alternative enumerate ed escluse) — o sono già marcate come "verifica parziale" / rettificate;
  - (b) lo script C è coerente con il decoder canonico (W10 OK);
  - (c) nessuna conclusione del perimetro è "wiki-only";
  - (d) la lista "Empirico-CLI da verificare" è vuota;
  - (e) nessuna divergenza non etichettata fra C e D.
  
  Se uno qualunque di (a)..(e) fallisce → CONDITIONAL o FAIL secondo l'impatto. La lista CLI non vuota (e) trasforma automaticamente PASS in PASS-condizionato-a-CLI o CONDITIONAL con handoff alla sede CLI (decisione del Reviewer secondo entità delle asserzioni rinviate).

---

## Out-of-scope — esplicito

Il Reviewer NON tratta in `REVIEW_CAP_DATA_01_RM_RETRO_review.md`:

- **Audit di contenuto di CAP-DATA-01 come capitolo metodologico** (decisioni di Cap.37-44, formule, mappatura I-VII): è già PASS hash `015c47a`. Il Reviewer auditta solo le asserzioni RM-1/2/3 sensibili, non riapre acceptance criteria della review v2 storica.
- **Audit di CAP-DATA-02 (Parte 9 = canonicizzazione DAPI)** e **CAP-DATA-03**: sessioni separate. Le asserzioni schema CANDLE / CANDLERANGE / codici errore / mesi IDEM vivono canonicamente in Parte 9, che resta PASS e fuori scope. Le citazioni cross-CAP di A verso Parte 9 sono validate solo per esistenza del referente (cfr. D.1), non per correttezza del contenuto.
- **Audit di FONDAMENTA-01** (prompt agenti + METODO.md): è già PASS Re-Review v3 commit `58cf81f`. Le regole RM-1/2/3/4 sono input vincolante, non si riaprono.
- **Audit di altri capitoli I-VII**: fuori scope. Nessuna citazione di Parti precedenti nel perimetro A-D è oggetto di audit (sono già PASS).
- **Esecuzione di codice contro DAPI o di probe empirici**: sede CLI, fuori scope WEB. Asserzioni che richiedono prova empirica diretta vanno in lista "Empirico-CLI da verificare", non si chiudono in sede WEB.
- **Audit di dump locali** (`probe_out/`, `exports/directa_history/`, `C:\directa_history_parametric_export_overlay\`): sede CLI, fuori scope WEB. Le asserzioni su questi dump vanno in lista "Empirico-CLI da verificare".
- **Modifica diretta dei file del perimetro o di qualunque altro file del repo (incluso `probe_dapi.py`)**: il Reviewer non patcha. Anche se identifica che lo script ha un decoder ancora sbagliato, NON lo corregge; produce solo finding + suggerimento di patch testuale in AC-8. Le modifiche, se approvate dal supervisore al punto di controllo CONDITIONAL/FAIL, sono eseguite da un Developer in fase di rework (vedi pipeline attesa).
- **Proposta di nuove regole RM-5..RM-N**: fuori scope. Il Reviewer può segnalare in "Osservazioni minori" che certe situazioni emergenti suggeriscono regole future, ma non le formalizza. La decisione spetta al supervisore in una sessione dedicata.
- **Revisione dei file di stato `STATO_CORRENTE.md`, `CARRYOVER.md`, `QUESTIONS.md`, `DEV_STATUS.md`**: fuori perimetro normativo. Possono essere letti come supporto evidenziale (es. M-1 per il fatto W1), non auditati come oggetti di output.
- **Riapertura della rettifica §3.1 di D**: la rettifica esiste (commit `a12ae32` + nota in cima a §3.1 dell'HANDOFF). Il Reviewer verifica che la rettifica sia chiara, NON la riapre. Verifica però che la stessa rettifica sia stata propagata a TUTTE le posizioni del perimetro che ne avevano bisogno (in C, in A se citato, in B se citato).

---

## Done when — domande operative a cui il report del Reviewer deve rispondere

1. Per ogni asserzione W1..W10 dell'inventario di partenza (+ W11+ eventuali emerse dal secondo giro), qual è l'esito RM-1? Citazione file:linea, alternative compatibili, esclusione esplicita o no?
2. Lo script `scripts/probe_dapi.py` è coerente con `scripts/export_directa_history_parametric.py:477` sullo schema CANDLE? Citazione testuale dei due punti.
3. L'HANDOFF 28/05 §3.2-§3.6 ("scoperte critiche" diverse da §3.1 schema CANDLE) è stato rivisto con la metodologia RM-1 dopo l'incidente §3.1? Se no, quali §3.k restano "compatibili con i dati ma non verificate"?
4. Le citazioni della wiki Directa nel perimetro sono trattate come hint o come fonte autorevole? Esistono conclusioni "wiki-only"?
5. La mappatura claim→evidenza di B (REPORT) regge: ogni "OK" degli AC è verificabile con file:linea?
6. Verdetto finale: il perimetro A-D, nello stato corrente di `origin/main`, soddisfa RM-1/2/3 retroattivamente? Se no, lista puntuale dei buchi + patch suggerita per ciascuno + classificazione BUG REALE / MIGLIORA / NEUTRO / RISCHIO PEGG. La lista "Empirico-CLI da verificare" è vuota o richiede una sessione CLI separata?

---

## Pipeline attesa

### Iterazione 1 — Review WEB

- L'Orchestratore della sessione corrente invoca **Reviewer** in sede **WEB**, con prompt che cita esplicitamente:
  - leggi `tasks/METODO.md` come prima azione;
  - leggi `tasks/ACTIVE_TASK.md` (questo file);
  - perimetro = 4 file A-D con i path effettivi riportati nel task;
  - sede = WEB (con divieti `reviewer.md:163-164`: NO "verificato empiricamente" su asserzioni che richiedono DAPI o dump locale);
  - esegui Check A/B/C/D/E come descritti;
  - applica RM-1/2/3 a te stesso (AC-9/10/11);
  - produci `reviews/REVIEW_CAP_DATA_01_RM_RETRO_review.md` con verdetto + tabella classificazione + sezione "Empirico-CLI da verificare" se non vuota;
  - committa e pusha su `origin/main`.
- Il Reviewer produce il file e termina (commit + push).

### Iterazione 2 — Punto di controllo supervisore (solo se CONDITIONAL/FAIL)

- L'Orchestratore esegue il **punto di controllo supervisore** (`CLAUDE.md` §"Punto di controllo supervisore"): presenta la tabella di classificazione AC-8, attende decisione del supervisore su quali finding "MIGLIORA PERFORMANCE" e "RISCHIO PEGGIORAMENTO" passare a Developer (i BUG REALI sono obbligatori).
- L'Orchestratore aggiorna `tasks/ACTIVE_TASK.md` aggiungendo sezione "## Finding di Review approvati per rework" con SOLO i finding approvati.
- Azzera `tasks/DEV_STATUS.md`.
- Invoca **Developer** con istruzione di patchare i SOLI file del perimetro A-D coinvolti dai finding approvati, secondo le patch suggerite in AC-8 modificate dalle decisioni del supervisore. Il Developer NON ridefinisce RM, NON riapre asserzioni non approvate, NON modifica file fuori dal perimetro A-D.
- Output del Developer: file del perimetro patchati su `origin/main` + report ridotto in `reports/REPORT_AUDIT_RM_RETRO_CAP_DATA_01.md` (formato ridotto: Cosa è stato modificato, Mappatura finding→patch, Verifica working tree, Verifica push). Nota: NON si tocca `reports/REPORT_CAP_08.md` esistente (che è il report originale del Developer di CAP-DATA-01, immutabile); le modifiche al file B come tale (se approvate) sono Edit chirurgici nel file stesso, separati dal report ridotto del rework.
- Developer scrive `READY_FOR_REVIEW` in `tasks/DEV_STATUS.md`.

### Iterazione 3 — Re-Review WEB (solo se Iter.2 eseguita)

- L'Orchestratore esegue check post-Developer (6 controlli adattati al fatto che NON c'è un nuovo CAP-XX: gli output attesi sono i file del perimetro patchati + il report ridotto + DEV_STATUS pulito).
- Invoca di nuovo **Reviewer** in sede **WEB** con istruzione: rieseguire i check sui file del perimetro patchati + verificare che i finding approvati siano effettivamente chiusi. Output: `reviews/REVIEW_CAP_DATA_01_RM_RETRO_v2_review.md` con verdetto PASS / CONDITIONAL / FAIL.
- Loop fino a PASS. Regola terminazione 3 iterazioni (`CLAUDE.md`): se Reviewer e Developer divergono su un finding dopo 3 giri, Planner arbitra.

### Iterazione 4 — Eventuale sessione CLI (solo se lista "Empirico-CLI da verificare" non vuota in nessuna iterazione WEB)

- Se la review WEB chiude PASS-condizionato-a-CLI o CONDITIONAL con handoff alla sede CLI, l'Orchestratore della sessione corrente:
  - prepara un **prompt-template ready-to-paste** per una sessione CLI separata, contenente la lista "Empirico-CLI da verificare" e i test minimi proposti;
  - NON esegue lui i test CLI (sessione WEB, non ha accesso al filesystem locale né a DAPI);
  - notifica il supervisore con il prompt-template e fermazione.
- La sessione CLI separata produce `reviews/PROBE_REVIEW_CAP_DATA_01_RM_RETRO_cli.md` con esiti empirici. L'Orchestratore della sessione CLI (separata da questa) raccoglie i due audit (WEB + CLI) e produce il verdetto finale consolidato. NB: questa fase è fuori dal perimetro temporale della sessione corrente.

### Chiusura sessione PASS — adattata (NON sono le 7 condizioni standard CAP-XX)

Quando la Review WEB chiude PASS e la lista "Empirico-CLI da verificare" è vuota (oppure è stata chiusa in una sessione CLI successiva):

1. Review PASS pubblicata su `origin/main` (`reviews/REVIEW_CAP_DATA_01_RM_RETRO_review.md` o `_v2_review.md`).
2. `DEV_STATUS.md` azzerato (se Iterazione 2/3 eseguita).
3. Eventuale `reports/REPORT_AUDIT_RM_RETRO_CAP_DATA_01.md` pubblicato (solo se rework eseguito).
4. `docs/methodology_v2/00_indice.md` **NON va aggiornato** (Parte 8 resta PASS storico inalterato; questo task NON è un CAP-XX). 
5. `tasks/ACTIVE_TASK.md` resta puntato a questo task (storico).
6. `tasks/CARRYOVER.md` aggiornato **solo se** la Review ha prodotto raccomandazioni di processo da registrare come `RACC-METODO-N` (namespace separato dai M-promemoria di capitolo).
7. `tasks/STATO_CORRENTE.md` aggiornato: in particolare i M-promemoria M-2..M-6 (se le rispettive asserzioni W2..W6 sono state riauditate o marcate "verifica parziale"), e una nota di sessione che indica "AUDIT-RM-RETRO CAP-DATA-01 chiuso PASS, debito retroattivo RM-4 su perimetro A-D saldato".
8. Notifica al supervisore con riepilogo (hash review PASS, conteggio finding, eventuali Empirico-CLI rinviati a sessione CLI separata) **senza** prompt-template per CAP-XX successivo: il supervisore decide quando aprire la sessione successiva (PROBE_RECUPERO_GAP_DAPI.md, CAP-DATA-03, o altro).

---

## Pipeline sintetica

```
Reviewer(WEB) Iter.1
  ↓
verdetto PASS + lista CLI vuota       → chiusura sessione (7 punti adattati)
verdetto PASS + lista CLI non vuota   → prompt-template CLI al supervisore + chiusura sessione parziale (verdetto WEB OK, CLI rinviata)
verdetto CONDITIONAL/FAIL             → controllo supervisore → Developer Iter.2 → Reviewer Iter.3 → loop fino a PASS
```

---

## Note al Reviewer (vincoli operativi specifici di questo task)

- **Tono dell'audit retroattivo**: questo NON è un audit "ostile" su lavoro fresco appena consegnato; è un audit retroattivo su file pre-RM. Il Reviewer distingue chiaramente fra:
  - **non-conformità di formato** dovute alla pre-esistenza del file rispetto a RM (es. assenza del blocco 4-righe in C/D che sono pre-28/05 sera): MIGLIORA PROCESSO se la sostanza regge;
  - **non-conformità sostanziale** (asserzioni dichiarate "verificato" senza enumerazione di alternative anche sostanzialmente): BUG REALE, indipendentemente dalla data del file.
  Il Reviewer è ostile sulla **sostanza**, comprensivo sul **formato pre-RM**.
- **Tre tipi di file misti nel perimetro**:
  - A è un CAP metodologico già PASS: focus RM-1 su asserzioni "verificato" e RM-3 su citazioni esterne; nessuna riapertura di contenuti AC.
  - B è un report supervisore: focus criterio 4 della probe-review (mappatura claim→evidenza) e RM-1 su eventuali asserzioni "verificato schema X".
  - C è uno script: focus RM-1 sui commenti docstring + coerenza decoder + RM-2 con `export_directa_history_parametric.py:477`.
  - D è un handoff: il caso più pieno di asserzioni RM-1 da auditare; setaccio integrale §3.1-§3.6 + il §5.5 ("limite empirico ~100 giorni intraday DAPI" come "cosa cerchiamo") + §3.6 architettura socket.
  Il Reviewer **non miscela** i criteri di giudizio: il fatto che A sia PASS non protegge le sue asserzioni "verificato" dalla setacciatura RM-1; il fatto che D sia un handoff informale non gli consente di lasciare asserzioni "in aria".
- **Niente cosmesi**: come da `reviewer.md:64`, non riportare problemi di formattazione/stile che non cambiano il comportamento del sistema. Focus solo su finding che, se non chiusi, lasciano un cammino aperto al pattern d'errore canonico CANDLE o producono salute dati non-RM-compliant per CAP-DATA-03 a valle.
- **Citazioni testuali obbligatorie**: ogni finding cita il testo esatto dal file (file:linea + virgolette). Niente parafrasi. Il supervisore deve poter verificare con un click ogni finding.
- **Lo script in C non si corregge mai dal Reviewer**: anche se il Reviewer rileva che `parse_line` (`probe_dapi.py:164-252`) ha ancora un decoder errato, NON lo corregge. Produce finding + patch suggerita testuale.
- **Coerenza con M-1 di STATO_CORRENTE.md**: il Reviewer può **assumere come dato** che lo schema CANDLE reale è `C;L;H;O;V` (commit `a12ae32` ha rettificato lo script) — NON deve riauditare la rettifica empirica del 29/05. Auditta SOLO la propagazione formale della rettifica nei file del perimetro (in particolare W10: D §3.1 chiaramente etichetta il vecchio testo come errato? altri punti del perimetro citano ancora lo schema vecchio in altro contesto?).
- **RM-1 applicato a sé stesso (AC-9)**: esempio paradigmatico. Se il Reviewer dichiara "verificato che §3.2 sintassi CANDLERANGE rispetta RM-1", deve enumerare cosa significa "rispetta": (a) §3.2 enumera permutazioni alternative degli argomenti? (b) ha test che ha escluso ognuna? Se (a) o (b) sono NO, il Reviewer scrive "verifica parziale" (la propria) e marca W2 come finding aperto.

---

## Note al Developer (solo se Iterazione 2 viene attivata)

- Patchare **solo** i finding approvati dal supervisore. Niente patch "mentre ci sono".
- Modifiche **solo** ai file del perimetro effettivamente coinvolti dai finding approvati. Niente edit a file fuori dal perimetro A-D senza approvazione esplicita.
- Mantenere la coerenza inter-file: una modifica a C può richiedere riflesso in D (e viceversa); documentare nel report ridotto la mappatura.
- Nessuna modifica al contenuto sostanziale di A (Parte 8 è PASS storico): le eventuali patch su A sono ammesse SOLO per (i) etichettatura fonti RM-3 mancanti, (ii) chiarimenti di citazione cross-CAP che il Reviewer ha marcato come ambigue, (iii) correzione di una citazione "verificato" che lascia alternative non escluse (in tal caso, riscrittura come "verifica parziale" senza alterare la decisione tecnica). Modifiche più sostanziali = richiedono nuovo task Planner.
- Per C (`scripts/probe_dapi.py`): se i finding richiedono fix al decoder (es. coerenza con `export_directa_history_parametric.py:477` non ancora perfetta), il Developer applica il fix. Se richiedono fix ai commenti docstring per RM-1 (enumerazione alternative), riscrive i commenti nel formato 4-righe per gli "scoperti" attualmente in prosa libera.
- Per D (HANDOFF): le rettifiche RM-1 vanno applicate aggiungendo a §3.k il blocco 4-righe `VERIFICA/PROVE/ALTERNATIVE ESCLUSE/ALTERNATIVE NON ESCLUSE` per ogni asserzione approvata; il vecchio testo non si cancella ma si etichetta inequivocabilmente come "rettificato post-RM" o "verifica parziale".
- Commit message format: `[AUDIT-RETRO] patch <file> — chiusura finding <#> (RM-N)`.
- Push diretto a `origin/main` (push policy MEMORY).
- Al termine: `READY_FOR_REVIEW` in `tasks/DEV_STATUS.md`.

---

## RM-2 — Decoder esistenti nel repo da leggere prima di assumere format (vincolo Planner secondo `tasks/METODO.md` §RM-2)

Per soddisfare il vincolo metodologico applicato al Planner (regola "decoder esistenti nel repo da leggere prima di assumere format" — applicabile quando il task tocca parsing di sistemi esterni), questo task elenca per il Reviewer i decoder DAPI già noti al momento della stesura del task card. Il Reviewer è comunque **tenuto a rifare il grep direttamente** (Check B) per individuare eventuali decoder mancanti da questa lista.

Decoder/parser DAPI noti al Planner nel repo:
- **`scripts/export_directa_history_parametric.py:477`** — decoder di produzione canonico per schema CANDLE, con commento esplicito `# Documentazione Directa: UFF, MIN, MAX, APE => close, low, high, open.` (commit pre-incidente CANDLE; lo schema reale `C;L;H;O` era già qui, è la fonte CODICE-ESISTENTE che `7bb2955` aveva ignorato);
- **`scripts/probe_dapi.py:164-252`** — decoder di `parse_line` introdotto nel commit `7bb2955` con schema CANDLE inizialmente errato e rettificato in commit `a12ae32` (oggetto auditato in C);
- `scripts/update_inventory_indici_futures_daily.py` — citato dall'handoff come consumer di dati storici (può contenere parsing minimo: il Reviewer estende il grep se necessario).

Se il grep RM-2 del Reviewer rivela decoder aggiuntivi non in questa lista, il finding è un'estensione naturale del Check B, non un'incompletezza del task card (i decoder elencati qui sono **hint**, non esaustivi per costruzione).

---

## RM-3 — Etichettatura fonti del task card

Riferimenti citati in questo task card e loro livello (`METODO.md` §RM-3):

- `tasks/METODO.md`, `.claude/CLAUDE.md`, `.claude/agents/reviewer.md` — `[DOC-INTERNO]` (livello 3, vincolante per processo);
- `scripts/export_directa_history_parametric.py:477` — `[CODICE-ESISTENTE r.477]` (livello 2);
- M-1 di `tasks/STATO_CORRENTE.md` (riga 64) sullo schema CANDLE reale — `[PROVA-EMPIRICA 2026-05-29]` (livello 1, V-1 capture con tick realtime FIB6F 09:08);
- commit `a12ae32`, `7bb2955`, `015c47a`, `58cf81f`, `de2938d`, `916278a` — `[DOC-INTERNO]` (eventi storici del repo);
- **wiki Directa DAPI** (`O;H;L;C` schema dichiarato) — `[WIKI-HINT, dimostrato inesatto]` (livello 4, non usato come fonte di verità da questo task; citato solo come oggetto di test RM-3 nel perimetro).

Nessuna conclusione di questo task card si appoggia esclusivamente a livello 4.

---

## RM-4 — Modalità di review per output non-CAP previsti dal task

Output non-CAP attesi da questo task:
- **`reviews/REVIEW_CAP_DATA_01_RM_RETRO_review.md`** (output del Reviewer Web Iter.1) — è esso stesso un audit, copre la propria RM-4 per costruzione. Nessuna self-review aggiuntiva richiesta.
- **Eventuali patch ai file C (script) o D (handoff) in Iterazione 2** — se il Developer modifica `probe_dapi.py` o `HANDOFF_PROBE_DAPI_20260528.md`, l'output rientra nuovamente in RM-4 criterio (a) o (b) di `CLAUDE.md`. Modalità obbligatoria: opzione B (probe-review formale) eseguita dal Reviewer Iter.3, che già è prevista nella pipeline. Nessuna self-review opzione A è ammessa per le patch di Iter.2.
- **`reports/REPORT_AUDIT_RM_RETRO_CAP_DATA_01.md`** (output del Developer in Iter.2, formato ridotto) — è documento di handoff, rientra in RM-4 criterio (b). Modalità: opzione A (self-review esplicita dell'autore in fondo al documento con blocco 4-righe RM-1 per ogni "verificato"). Auto-review del Developer obbligatoria prima del commit.

---

## Verifica esplicita dell'eredità (secondo giro del Planner — checklist obbligatoria)

- [x] **RM-1 applicata al task**: le citazioni di "fatti già verificati" dei task precedenti (M-1, hash storici PASS) sono accompagnate dall'evidenza di esclusione delle alternative (V-1 ha provato lo swap O/C, ergo `C;L;H;O` esclude `O;L;H;C` — questa esclusione è la prova che giustifica usare M-1 come dato). Nessuna asserzione di task precedente è usata come dato senza supporto empirico citato.
- [x] **RM-2 applicata al task**: il task tocca parsing DAPI (è il cuore del Check B); i decoder esistenti nel repo sono citati esplicitamente (sezione "RM-2 — Decoder esistenti nel repo" sopra). Il Reviewer è comunque tenuto al grep diretto in Check B.
- [x] **RM-3 applicata al task**: ogni riferimento esterno nel task card è etichettato per livello (sezione "RM-3 — Etichettatura fonti" sopra). Nessuna conclusione è "wiki-only".
- [x] **RM-4 applicata al task**: output non-CAP previsti dal task sono elencati con modalità di review obbligatoria (sezione "RM-4 — Modalità di review" sopra).
- [x] **M-promemoria carryover**: M-1 di STATO_CORRENTE.md è integrato come eredità #8; M-2..M-8 di STATO_CORRENTE.md come #9. M-promemoria di `CARRYOVER.md` (M-2 latenza Telegram per Appendice E, ecc.) NON pertinenti al perimetro A-D, esplicitamente esclusi (eredità #10).
- [x] **Q-XX aperte**: nessuna ambiguità reale richiede apertura di Q-XX in QUESTIONS.md. Il perimetro è netto, le regole sono vincolanti, la modalità Review-First è in linea con i casi di audit retroattivo già consolidati (FONDAMENTA-01). Le decisioni discrezionali del Reviewer (es. se una violazione è BUG REALE o MIGLIORA PROCESSO) sono parte naturale del suo lavoro, non ambiguità da escalare.
- [x] **Impatto sul GA**: la salute dati DAPI è il prerequisito per la training pipeline. Lo schema CANDLE corretto impatta la calibrazione EGARCH; codici errore, sintassi CANDLERANGE, mesi IDEM, cooldown 30s impattano la pipeline di ingest che alimenta il GA. Un perimetro A-D RM-compliant è la condizione necessaria perché PROBE_RECUPERO_GAP_DAPI.md e CAP-DATA-03 partano da fondamenta affidabili invece che da fatti "compatibili con i dati ma non verificati". Impatto identificabile sul ranking dei cromosomi (via qualità della serie storica), sulla fitness (via correttezza dei rendimenti log), sulla conversione signal-to-trade (via correttezza del payload runtime DAPI). Il task NON è metrica/report sterile.
- [x] **Scope**: dentro = perimetro A-D + grep RM-2 + lista Empirico-CLI; fuori = Parte 9, capitoli I-VII, modifiche al perimetro, esecuzione DAPI. Esplicito.
- [x] **Acceptance criteria verificabili**: AC-1..AC-13 sono verificabili senza ambiguità (presenza di file, presenza di sezioni, esecuzione di grep, esiti puntuali per ogni W-N).
- [x] **Done when**: 6 domande operative concrete.
- [x] **Niente numeri inventati**: il task non introduce nuove soglie o parametri; eredita i criteri di classificazione di `reviewer.md` e i criteri RM di `METODO.md`.

---

## Finding di Review approvati per rework (Iter.2 — decisione supervisore 2026-05-29)

**Verdetto Review v1**: CONDITIONAL (`reviews/REVIEW_CAP_DATA_01_RM_RETRO_review.md`, commit `8e0e334`).
**Punto di controllo supervisore eseguito 2026-05-29 ~23:10 CET.** Decisione: **tutti i 7 finding a Developer** (2 BUG REALI obbligatori + 5 MIGLIORA PROCESSO tutti approvati). Nessun finding NEUTRO/RISCHIO PEGGIORAMENTO nella review.

### BUG REALI (obbligatori) — chiusura con evidenza empirica preferita all'auto-downgrade

| # | W-N | File:linea | Finding | Azione Developer v2 |
|---|-----|-----------|---------|---------------------|
| 1 | W4 | `scripts/probe_dapi.py:17-21`; `HANDOFF_PROBE_DAPI_20260528.md:54-61` | Semantica codici errore `1004/1007/1017/1030` dichiarata "fatto" senza enumerazione alternative né dump:timestamp; nessun supporto nel decoder di produzione (`is_error_line` non decodifica numerici) | Riscrivere come blocco 4-righe RM-1. **Se l'empirico CLI è disponibile** (DGo aperta), chiudere con `[PROVA-EMPIRICA 2026-05-29]`: per ogni codice il comando-trigger osservato + ≥2 permutazioni errate per disambiguare l'ampiezza di 1017. **Altrimenti** "verifica parziale" + Empirico-CLI. |
| 2 | W6 | `scripts/probe_dapi.py:27-29`; `HANDOFF_PROBE_DAPI_20260528.md:69-71` | Cooldown "~30s dopo 14ª connessione" — due costanti precise da singola osservazione, alternative 13/15/timing non escluse | Riscrivere come blocco 4-righe RM-1. **Se empirico disponibile**: loop open/close su 10003 contando le connessioni, ≥3 ripetizioni per stabilire se la soglia è 14 esatta o varia + durata cooldown misurata. **Altrimenti** "verifica parziale: cooldown ~30s in prossimità della ~14ª, soglia non disambiguata" + Empirico-CLI. |

### MIGLIORA PROCESSO approvati dal supervisore (tutti a Developer)

| # | File:linea | Finding | Azione Developer v2 |
|---|-----------|---------|---------------------|
| 3 | `scripts/probe_dapi.py:14-16`; `HANDOFF:44-52` | `END CANDLES` + ordine arg CANDLERANGE corretti e corroborati da codice di produzione, ma enumerazione formale assente | Aggiungere etichetta `[CODICE-ESISTENTE r.228-230 / r.245]` ai due fatti. |
| 4 | `scripts/probe_dapi.py:23-26` | Convenzione ticker Eurex/CME senza evidenza nel perimetro; appartiene canonicamente a Parte 9 | Annotare in C che IDEM è l'unico testato; Eurex/CME da confermare CLI e canonicizzare in Parte 9. Se empirico ANAG disponibile su un ticker Eurex/CME, allegare evidenza. |
| 5 | `scripts/probe_dapi.py:44` vs `:169` | Banner: docstring dichiara stringa piena `DARWIN_STATUS;CONN_OK;TRUE`, decoder matcha solo prefisso `DARWIN_STATUS` | Allineare docstring al comportamento del decoder (o viceversa) dopo cattura banner reale. Banner catturabile anche a mercato chiuso → chiudere con evidenza. |
| 6 | C, D (globale) | Etichette di fonte RM-3 (`[WIKI-HINT]`/`[CODICE-ESISTENTE]`/`[PROVA-EMPIRICA]`) assenti (file pre-RM); la sostanza RM-3 regge | Aggiungere le etichette nelle asserzioni toccate dal rework. |
| 7 | C, D (globale) | Formato 4-righe RM-1 assente nelle asserzioni di C/D (file pre-RM) | Riformattare in 4-righe le asserzioni toccate (#1, #2 obbligatori; le altre dove pertinente). |

### Nota operativa sull'esecuzione (constraint di sessione 2026-05-29 ~23:12 CET)

- **Subagenti `developer`/`reviewer` non disponibili** in questo ambiente: il rework è eseguito da un agente `general-purpose` in **ruolo Developer** (stesso pattern già usato per il Reviewer di questo audit, cfr. review `:6`). La re-review Iter.3 sarà ugualmente in ruolo Reviewer general-purpose.
- **Mercato chiuso** (sessione FIB 08:00–22:00, ora 23:12): il dato realtime tick NON è disponibile. **MA** W4 (codici errore via comandi-trigger) e W6 (cooldown = comportamento gateway) NON dipendono dal dato di mercato → disambiguabili ora con DGo aperta. Anche W8 (banner) e parte di W5/W4 (ANAG/codici) sono catturabili a mercato chiuso. Solo la cattura tick realtime resta rinviata a sessione di mercato aperto.
- **Ordine empirico** (rispetto del cooldown M-5): prima W4 (poche connessioni), W6 (cooldown) per ultimo.

**Commit message rework**: `[AUDIT-RETRO] patch C+D — chiusura 7 finding Review v1 (2 BUG REALI + 5 MIGLIORA PROCESSO)`.

---

**Fine del task card.**
