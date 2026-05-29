# TASK ATTIVO: AUDIT-RM-RETRO CAP-DATA-02 — audit retroattivo RM-1/2/3 del perimetro A-D (Parte 9)

**Assegnato da**: Planner
**Output atteso primario**: `reviews/REVIEW_CAP_DATA_02_RM_RETRO_review.md` (verdetto PASS / CONDITIONAL / FAIL del Reviewer Web sul perimetro A-D di CAP-DATA-02)
**Output atteso secondario (solo se CONDITIONAL/FAIL approvato dal supervisore)**: fix mirati ai soli file del perimetro A-D approvati, prodotti dal Developer in iterazione di rework
**Stato**: IN ATTESA
**Workflow**: **Review-First** (il perimetro esiste già su `origin/main`; vanno auditate retroattivamente le regole RM-1/2/3 introdotte DOPO la produzione del capitolo)
**Sede del Reviewer**: **WEB** (perimetro = file versionati su repo + grep di codice committato; nessuna esecuzione contro DAPI in questo task)
**Natura del task**: NON è un capitolo metodologico CAP-XX nuovo. NON è una CAP-review piena nuova (Parte 9 è già PASS storico, hash review `86425a7` v2 del 2026-05-28). NON è una probe-review classica (qui si audita simultaneamente 1 CAP storico + decoder canonico di produzione + documento-indagine sorgente). È un **audit RM-1/2/3 retroattivo mirato** + coerenza A/C ↔ D-canonico sul perimetro A-D specifico di CAP-DATA-02.

---

## Obiettivo

Verificare, applicando retroattivamente le regole `RM-1 / RM-2 / RM-3` di `tasks/METODO.md`, che le asserzioni di tipo "verificato / confermato / fatto / stabilito" presenti nei file del perimetro A-D di CAP-DATA-02 (CAP_09_parte_9.md, REPORT_CAP_09.md, INDAGINE_DIRECTA_CROSS_INDEX.md, e — come riferimento canonico di codice — `scripts/export_directa_history_parametric.py`):

1. **rispettino il formato 4-righe** `VERIFICA / PROVE / ALTERNATIVE ESCLUSE / ALTERNATIVE NON ESCLUSE` di `METODO.md` §RM-1, OPPURE — quando il formato 4-righe non è esigibile in retroazione perché i file sono pre-RM — abbiano almeno **enumerazione esplicita delle alternative compatibili coi dati osservati** e dichiarazione dell'evidenza che le esclude;
2. **siano coerenti** con i decoder/comandi di produzione nel repo (`scripts/export_directa_history_parametric.py` come riferimento canonico per schema CANDLE, sintassi CANDLERANGE, terminatore stream, decoder errori), come richiesto da `METODO.md` §RM-2;
3. **non si appoggino come fonte autorevole** alla wiki Directa o ad altra documentazione esterna di livello 4 in violazione di `METODO.md` §RM-3 (ordine di priorità delle fonti `1>2>3>4`); il wiki Directa è già **dimostrato inesatto** sullo schema CANDLE e va trattato come hint smentito ovunque sia citato;
4. **siano coerenti** con i risultati empirici M-1..M-8 del follow-up CLI registrati in `tasks/STATO_CORRENTE.md` §5, che sono **livello-1 [PROVA-EMPIRICA 2026-05-29]** prodotti DOPO la chiusura di CAP-DATA-02 e che in alcuni casi **ri-caratterizzano o contraddicono** asserzioni che Parte 9 dichiara come fatti;
5. **non lascino divergenze script ↔ capitolo non etichettate** (Check W5 specifico): A (Cap.49 mappatura schema, Cap.47 schemi DAPI runtime, Cap.50 codici errore, Cap.48 dominio `source`) e C (INDAGINE_DIRECTA_CROSS_INDEX.md Appendici A/B) dichiarano gli stessi schemi che D (`export_directa_history_parametric.py` decoder canonico, sintassi comandi, marker stream, `is_error_line`) implementa? **Divergenza non etichettata = BUG REALE.**

L'audit ha **due finalità** simultanee:

- **Finalità retroattiva (gate metodologico)**: chiudere il debito di `RM-4` retroattivo su CAP-DATA-02 (CAP-XX prodotto prima dell'introduzione di RM-1..RM-4) — gli output non-CAP correlati (A:INDAGINE e D:script canonico) erano pre-RM-4 al momento della stesura del CAP. CAP-DATA-01 ha già chiuso il debito sul suo perimetro (PASS hash `a5f7bcb`); questo task chiude analogamente il debito su CAP-DATA-02, che è il capitolo **più esposto** all'errore originale O/C perché descrive direttamente lo schema CANDLE in Cap.49 (mappatura DAPI → Portara), gli schemi runtime ANAG/BOOK_5/PRICE in Cap.47, i codici errore in Cap.50, la sintassi CANDLERANGE in Cap.48/Cap.51 e i codici mese IDEM in Cap.47.
- **Finalità di salute dati corrente**: identificare se l'errore CANDLE già noto (schema reale `C;L;H;O`) e i risultati di follow-up CLI (M-3 codici errore ri-auditati, M-4 mese F=Giu confermato/Mar-Dic da decodificare, M-5 cooldown refutato nel regime testato) hanno lasciato in Parte 9 asserzioni che, oggi, vanno **ri-caratterizzate** come "verifica parziale" o "refutate" prima che CAP-DATA-03 (continuità tape, recupero gap, riconciliazione, storicizzazione) parta da fondamenta non RM-compliant. Parte 9 è la sede canonica di queste asserzioni DAPI: se restano dichiarate come "fatti" non disambiguati, contaminano CAP-DATA-03 esattamente come l'errore CANDLE aveva contaminato la sessione web 28/05.

Il task NON risponde a: validità complessiva di CAP-DATA-02 come capitolo metodologico (è già PASS hash `86425a7`, non si riapre); audit di CAP-DATA-01 (già auditato, PASS `a5f7bcb`); audit di CAP-DATA-03 (sessione futura); audit dei capitoli I-VIII; correttezza empirica di asserzioni che richiedono prova diretta contro DAPI live (sede CLI; il Web reviewer le marca "Empirico-CLI da verificare" e produce eventuale handoff alla sede CLI); riapertura della **decisione di design Q-A-3 cash gating** (è una **scelta**, non una verifica empirica: RM-1 NON si applica a decisioni di design).

Il task si fa adesso perché RM-1/2/3/4 sono state introdotte (commit `7bb2955`/`de2938d`/`916278a` del 2026-05-28) lo stesso giorno in cui Parte 9 v2 è stata pubblicata (hash `9bd35ba` per il documento, review PASS `86425a7`), ma il ciclo Review v1 FAIL → v2 PASS di Parte 9 è stato condotto **senza applicare retroattivamente RM-1/2/3** al setaccio sostanziale richiesto oggi. FONDAMENTA-01 ha chiuso il gate **ex-ante** per il futuro; CAP-DATA-01 ha chiuso il debito **ex-post** sul perimetro A-D di Parte 8 (PASS `a5f7bcb`); CAP-DATA-02 va chiuso analogamente prima che CAP-DATA-03 venga aperto. Inoltre i risultati empirici M-3 (codici errore ri-auditati con dump puntuale `probe_out/w4_errcodes_20260529.json`), M-4 (mesi IDEM verifica parziale) e M-5 (cooldown **refutato nel regime testato**, dump `probe_out/w6_cooldown_20260529.json`) sono divenuti disponibili come livello-1 dopo la chiusura della review di Parte 9: queste prove vanno ora confrontate puntualmente con il testo di CAP-DATA-02 per identificare asserzioni da ri-caratterizzare.

---

## Eredità obbligatoria

### Da `tasks/METODO.md` (testo vincolante, NON riaprire)

1. **RM-1** — formato 4-righe `VERIFICA / PROVE / ALTERNATIVE ESCLUSE / ALTERNATIVE NON ESCLUSE` (`METODO.md:28-33`). Asserzioni "verificato" senza enumerazione esplicita delle alternative compatibili coi dati osservati = BUG REALE. Asserzioni "verificato" in **prosa libera** anche con alternative enumerate = "non in formato" (BUG REALE secondo `reviewer.md`). Sui file del perimetro pre-RM, l'audit applica il criterio sostanziale (enumerazione + esclusione) e segnala separatamente la non-conformità al formato 4-righe come MIGLIORA PROCESSO se la sostanza è OK, BUG REALE se anche la sostanza manca.
2. **RM-2** — grep nel repo prima di assumere format esterno (`METODO.md:46-94`). Il Reviewer esegue **direttamente** `grep -rn` su pattern del dominio DAPI per verificare se decoder esistenti nel repo sono coerenti col perimetro o lo contraddicono. Decoder canonico già noto: `scripts/export_directa_history_parametric.py:477` (commento `# UFF, MIN, MAX, APE => close, low, high, open`).
3. **RM-3** — ordine di priorità fonti `1>2>3>4` (`METODO.md:97-136`). Etichette obbligatorie `[PROVA-EMPIRICA <data>]` / `[CODICE-EXISTENTE r.NNN]` / `[DOC-INTERNO]` / `[WIKI-HINT, da verificare]`. Conclusione "wiki-only" senza supporto dai livelli 1-3 = BUG REALE. Wiki Directa = **livello 4 dimostrato inesatto sullo schema CANDLE**: ogni conclusione di Parte 9 che si appoggia al wiki senza corroborazione level 1-3 è automaticamente sospetta.
4. **RM-4** — review obbligatoria per output non-CAP determinanti. CAP-DATA-02 è un CAP-XX e il suo ciclo Review v1→v2 è già stato fatto. Ma i suoi due input determinanti — INDAGINE_DIRECTA_CROSS_INDEX.md (documento sorgente non-CAP che dichiara "fatti DAPI") e export_directa_history_parametric.py (decoder di produzione canonico, fonte CODICE-ESISTENTE su cui CAP-DATA-02 si appoggia) — sono stati prodotti pre-RM e mai sottoposti a probe-review formale. Questo task chiude retroattivamente quel debito producendo l'audit mancante sull'asse A-D.

### Da `.claude/CLAUDE.md` (workflow di sessione)

5. Workflow Review-First per output esistenti: niente Developer in v1. L'Orchestratore della sessione corrente invoca direttamente il Reviewer in modalità adattata (audit RM-1/2/3 retroattivo del perimetro A-D, sede WEB). Il verdetto del Reviewer determina la presenza o assenza di una fase Developer di rework.
6. Modifiche ai file del perimetro NON sono autorizzate senza approvazione esplicita del supervisore al punto di controllo CONDITIONAL/FAIL. Il decoder canonico D è nel perimetro come **fonte CODICE-ESISTENTE** (riferimento di verità rispetto al quale A e C vanno confrontati), non come oggetto da modificare in Iterazione 1.
7. Push diretto a `origin/main` autorizzato (push policy MEMORY): il Reviewer pusha il file di review committato; l'eventuale Developer di rework pusha le patch dei file del perimetro approvate.
8. **Divieti per sede** (`.claude/agents/reviewer.md` riepilogato): il **Web reviewer NON dichiara "verificato empiricamente"** niente che richieda accesso a DAPI live o filesystem locale del supervisore; segnala come "Empirico-CLI da verificare" e lascia handoff alla sede CLI. Il **CLI reviewer NON fa probe massivi di zelo**; riproduce solo le asserzioni puntuali segnalate dal Web reviewer. Dump locali `probe_out/*` non versionati: l'audit Web li **cita come prove acquisite tramite M-3/M-4/M-5** (il M-promemoria è la forma versionata della prova), NON li ispeziona direttamente.

### Da `tasks/STATO_CORRENTE.md` §5 (M-promemoria attivi) — **INPUT CRITICO livello-1 [PROVA-EMPIRICA 2026-05-29]**

Sono risultati empirici del follow-up CLI di CAP-DATA-01, prodotti **dopo la chiusura PASS di CAP-DATA-02**. Sono livello-1 (prove dirette su DAPI live, dump puntuali) e contraddicono o ri-caratterizzano asserzioni che CAP-DATA-02 dichiara come fatti. Il Reviewer DEVE confrontare puntualmente le seguenti asserzioni di Parte 9 con questi M-promemoria:

9. **M-3** — codici errore ri-auditati [PROVA-EMPIRICA 2026-05-29, dump `probe_out/w4_errcodes_20260529.json`]: `1004` = comando ignoto (coerente con A `:194`), `1007` = ticker inesistente/non abilitato (coerente con A `:195`), `1017` = sintassi strutturale malformata (**non citato in A Cap.50** — A elenca solo 1004/1007/1030), **`1015` = data/parametro invalido NUOVO codice non in A**, **`1003` = comando storico su porta realtime NUOVO codice non in A**, **`1030` = realtime non sottoscritto NON RIPRODOTTO** (account FIB ha il dato, A `:196` dichiara semantica "atteso esclusivamente sui futures cross-index Eurex/CME" — verifica parziale: la semantica del 1030 dichiarata in A è **plausibile ma non riprodotta direttamente** sul perimetro account `B6086`). Implicazione su Parte 9 Cap.50: la tabella codici errore (A `:192-196`) va confrontata con M-3 → se A non cita 1017/1015/1003 ma li tratta come noti, o se dichiara 1030 verificato dove M-3 dice "non riprodotto", è verifica parziale o BUG REALE sostanziale.
10. **M-4** — mese IDEM ri-auditato [PROVA-EMPIRICA 2026-05-29]: `F`=Giugno **confermato** (SUB FIB6F → ANAG ISIN IT0024209022 GIU26); `I`=Settembre **già confermato** sul probe originale del 27/05 (ANAG FIB6I `IT0024847870 SET26`, ancora coerente con A `:61`); Mar/Dic **ancora da decodificare a mercato aperto** = verifica parziale. Implicazione su Parte 9 Cap.47 (codici mese FIB6F/FIB6I) e Cap.55 (lookup completa codici mese — già citata come "fuori scope, lookup runtime-discovery"): A `:61, 375` è già RM-1 conforme nel dichiarare la parzialità. Verificare che il testo dichiari esplicitamente "verifica parziale" per tutto ciò che non è F/I (Cap.47 r96 cita anche `FIB6L` come ticker candidato senza ANAG verificata — Empirico-CLI).
11. **M-5** — cooldown ri-auditato [PROVA-EMPIRICA 2026-05-29, dump `probe_out/w6_cooldown_20260529.json`]: la costante "cooldown ~30s dopo 14ª connessione" dichiarata in A `:47`, `:51`, `:198` è **REFUTATA nel regime testato** (75 connessioni open/close a ~1Hz su 10003 senza alcun cooldown, 3×25, `onset_connection:null`). Soglia/durata sotto burst >>1Hz non disambiguati. Implicazione su Parte 9 Cap.46 (rate-limit, "Pattern socket persistente, cooldown circa 30 s dopo la 14ª connessione TCP rapida") e Cap.50 (backoff esponenziale che ha come ancora empirica "ConnectionResetError 10054 sulla 14ª connessione TCP rapida"): la cifra "14 connessioni" e "~30s" è **smentita dall'empirico più recente nel regime ~1Hz**; Parte 9 oggi dichiara come fatto qualcosa che M-5 ha refutato. Va ri-caratterizzata come "osservazione sotto un regime burst non disambiguato; in regime ~1Hz nessun cooldown osservato". **Questo è il pattern canonico W6 che CAP-DATA-01 ha già identificato come BUG REALE sostanziale**: qui può ripresentarsi in Parte 9.

### Da `reviews/REVIEW_CAP_DATA_01_RM_RETRO_review.md` (pattern di errore ereditabili)

12. **Pattern W4 (codici errore)**: in CAP-DATA-01 era BUG REALE sostanziale RM-1 perché la tabella codici 1004/1007/1017/1030 era dichiarata "fatto" senza enumerare alternative né dump:timestamp e senza supporto in `is_error_line` del decoder canonico (che fa string-matching generico, NON decodifica numerici). Il Reviewer di questo task DEVE cercare lo stesso pattern in A Cap.50 (codici errore in tabella `:192-196`) e in C INDAGINE Cap.50 fonte: se la semantica è la stessa di CAP-DATA-01 senza miglior corroborazione level-1 (ora disponibile via M-3), è BUG REALE ereditato.
13. **Pattern W6 (cooldown)**: in CAP-DATA-01 era BUG REALE sostanziale RM-1 perché "14 connessioni" e "~30s" erano numeri precisi da singola osservazione senza alternative escluse. M-5 ha **refutato la dichiarazione** nel regime ~1Hz. Parte 9 lo dichiara come fatto in A Cap.46 `:47`, `:51`, `:198`: se non è marcato come "osservazione del 2026-05-27 in regime non disambiguato, refutata nel regime ~1Hz da prove empiriche 2026-05-29", è BUG REALE sostanziale ereditato + aggiornato dall'empirico recente.
14. **Pattern W2/W3/W7 (corroborazione level-2)**: in CAP-DATA-01 sintassi CANDLERANGE, terminatore END CANDLES, limite 100 giorni erano OK / MIGLIORA PROCESSO perché corroborati dal decoder canonico (`export_directa_history_parametric.py:228-230` per CANDLERANGE, `:245,282-285,437` per END CANDLES, `:61` `DEFAULT_INTRADAY_MAX_DAYS=100`). In Parte 9 questi stessi fatti vivono in Cap.48 (CANDLERANGE), implicitamente in Cap.51 (chunking ≤100gg via script), Cap.50 (fallback `AGG_FROM_60s` / `AGG_FROM_D` come dominio chiuso): se Parte 9 cita questi fatti senza etichettare la corroborazione `[CODICE-ESISTENTE r.NNN]` ma la sostanza regge level-2 → MIGLIORA PROCESSO, non BUG.
15. **Pattern schema CANDLE (`C;L;H;O`)**: in CAP-DATA-01 W1/W10 erano PASS sostanziale post-rettifica. In Parte 9 lo schema CANDLE è dichiarato nella tabella Cap.49 r158-162 con mapping `CANDLE campo 5 = <O>`, `campo 6 = <H>`, `campo 7 = <L>`, `campo 8 = <C>` — **ATTENZIONE**: questo è l'ordine `O;H;L;C` (il vecchio errore originale del wiki Directa). Verificare urgentemente con grep RM-2 sul decoder canonico `:477-481` quale ordine A dichiari: se A dichiara `O;H;L;C` mentre il decoder canonico (e M-1) dicono `C;L;H;O`, è **BUG REALE catastrofico** (lo stesso errore originale §3.1 di HANDOFF, sopravvissuto nel CAP-XX). Citazione obbligatoria nel report.

### Da `tasks/CARRYOVER.md` e `tasks/STATO_CORRENTE.md` §3 (carryover di sessione)

16. M-promemoria di sessione CAP-DATA-01 (M-1..M-8) sono **input vincolante** di questo task per i tre M-3/M-4/M-5 sopra. M-1 (schema CANDLE) è premessa, non da riauditare: il Reviewer assume come dato che lo schema reale è `C;L;H;O`, V-1 ha escluso `O;L;H;C`, fix nel decoder `probe_dapi.py` in `a12ae32` (vedi CAP-DATA-01 review PASS). M-6/M-7/M-8 non sono pertinenti al perimetro A-D di questo task.
17. **CARRYOVER.md** M-2 OPEN su latenza Telegram (Appendice E) non è pertinente al perimetro A-D di Parte 9 (CAP-DATA-02 tratta DAPI, non Telegram). Esplicitamente fuori scope qui.

---

## Perimetro — 4 file (A, B, C, D) con naming effettivo del repo

Il Reviewer audita **esclusivamente** questi 4 file, citando posizioni puntuali (file:linea). Nessun altro file del repo entra nel perimetro normativo (la lettura di altri file è ammessa solo come supporto evidenziale, es. grep su `scripts/` per validare RM-2, lettura di `tasks/METODO.md` per riferimento alle regole, lettura di `tasks/STATO_CORRENTE.md` §5 per gli M-3/M-4/M-5 come prove acquisite).

| ID | Path assoluto nel repo | Ruolo | Note di mappatura |
|----|------------------------|-------|-------------------|
| A | `docs/methodology_v2/CAP_09_parte_9.md` | CAP-DATA-02 = Parte 9 = "Pipeline runtime FIB su Directa DAPI" (Cap.45-56). Hash review PASS storica: `86425a7` (v2). | Naming canonico nel repo: `CAP_09_parte_9.md`. Identifier interno "Parte 9" (arabo). NON si audita come capitolo metodologico (già PASS); si audita SOLO per RM-1/2/3 retroattivo. Concentrazione di asserzioni RM-1 a rischio in: Cap.46 (banner, cooldown, rate-limit), Cap.47 (schemi ANAG/BOOK_5/PRICE, codici mese), Cap.48 (CANDLERANGE, dominio `source`), Cap.49 (mappatura schema CANDLE), Cap.50 (codici errore, riavvio mezzanotte), Cap.51 (limite 100gg, warm-up). |
| B | `reports/REPORT_CAP_09.md` | Report supervisore del Developer di CAP-DATA-02. Contiene "Decisioni rilevanti", "Misura prima/dopo", "Verifica esplicita degli Acceptance Criteria", iterazioni di rework v1→v2. | Il REPORT spesso dichiara "OK" come esito di AC: il Reviewer verifica che ogni "OK" non sia stato auto-dichiarato dal Developer senza prova RM-1 (claim → evidenza). Focus su AC che richiamano "verifica empirica" (es. AC su Cap.46 banner, Cap.47 ANAG, Cap.49 schema, Cap.50 codici errore). |
| C | `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md` | Documento-indagine: contiene le asserzioni "verificate" su DAPI da cui CAP-DATA-02 attinge — Appendici A/B esplicitamente citate da A Cap.46 r27, Cap.47 r59, Cap.50 r190, Cap.51 r235. È **input autoritativo** del capitolo, fonte degli "fatti DAPI" del 2026-05-27. | È fonte interna level-3 (DOC-INTERNO) di livello operativo, NON pre-RM con review formale. Il Reviewer audita le Appendici A/B (le sezioni `Q1`-`Q5` del documento INDAGINE sono state lette in apertura task) per RM-1 sostanziale: enumerazione alternative, distinzione fra hint wiki (Q2 `:34` cita wiki direttamente) vs prova empirica. Test canonico: la metodologia di verifica delle "scoperte" Q1-Q5 è la stessa che ha prodotto l'errore CANDLE? Se sì, almeno un finding "verifica parziale". |
| D | `scripts/export_directa_history_parametric.py` | Decoder/script DAPI di **produzione canonico**. È la fonte CODICE-ESISTENTE (level-2) rispetto alla quale A e C vanno confrontati. Riga `:477` schema CANDLE `# UFF, MIN, MAX, APE => close, low, high, open` = `C;L;H;O`. NB: D qui è la **fonte di verità di codice**, NON il file buggato (come era invece in CAP-DATA-01 dove C=probe_dapi.py era buggato). | Audit: D è oggetto di **lettura per estrarre le mapping canoniche** (schema CANDLE, sintassi CANDLERANGE, terminatore END CANDLES, decoder errori, limite 100gg) ed è oggetto di **confronto** rispetto al testo di A e C. Test centrale W5 di questo task: A (Cap.49 mappatura schema, Cap.48 dominio source, Cap.50 codici errore) e C (Appendici A/B su CANDLE) dichiarano gli stessi schemi che D implementa? Divergenza non etichettata = BUG REALE. Il Reviewer NON modifica D in Iterazione 1; il decoder canonico è autoritativo. |

**Cross-reference fuori perimetro ammesse**:
- `scripts/probe_dapi.py` decoder post-rettifica del 29/05 — citabile come `[CODICE-ESISTENTE]` di supporto (concorda con D sullo schema CANDLE post-fix `a12ae32`), NON auditabile in questo task (è già stato auditato in CAP-DATA-01 PASS);
- `tasks/HANDOFF_PROBE_DAPI_20260528.md` — già auditato in CAP-DATA-01 PASS, citabile come supporto per pattern d'errore identificato (Es. la rettifica §3.1 schema CANDLE) ma NON oggetto di questo audit;
- `tasks/STATO_CORRENTE.md` §5 — input critico (M-3, M-4, M-5) come `[PROVA-EMPIRICA 2026-05-29]` acquisita; NON oggetto di audit;
- `reviews/REVIEW_CAP_DATA_01_RM_RETRO_review.md` e `reviews/REVIEW_CAP_DATA_01_RM_RETRO_v2_review.md` — riferimento metodologico per il pattern di errore (W4/W6/W5 ereditabili), NON oggetto di audit;
- altri decoder/parser DAPI che emergano dal grep RM-2 (vedi sezione RM-2 in coda al task).

**Cross-reference esplicitamente FUORI scope**:
- canonizzazione delle asserzioni DAPI in CAP-DATA-03 (Parte 10): è la sessione futura che eredita le rettifiche di questo audit. Il Reviewer NON suggerisce rinvii a Parte 10 di asserzioni di Parte 9 (le asserzioni vivono canonicamente in Parte 9, non si spostano);
- decisione di design **Q-A-3 cash gating** (Cap.53): NON è asserzione empirica, è una **scelta di design** ratificata dal supervisore. RM-1 NON si applica a decisioni di design. Verifica solo che il perimetro vincolante (no feature tensor, no state machine, no cromosoma, no walk-forward) sia scritto in modo coerente, NON che la decisione sia "verificata".

---

## Lavoro atteso dal Reviewer (audit indipendente, sede WEB)

Il Reviewer produce **un singolo file** `reviews/REVIEW_CAP_DATA_02_RM_RETRO_review.md` con verdetto PASS / CONDITIONAL / FAIL e classificazione dei finding per il supervisore (BUG REALE / MIGLIORA PERFORMANCE / NEUTRO / RISCHIO PEGGIORAMENTO — categorie standard di `reviewer.md`; "PROCESSO" usato come sotto-etichetta di MIGLIORA quando il finding non incide sul GA ma sul gate metodologico).

**Header obbligatorio del file di review** (mappatura A-D esplicita):
```
# Review AUDIT-RM-RETRO CAP-DATA-02 (Parte 9) — perimetro A-D

**Sede**: WEB
**Natura**: audit retroattivo RM-1/2/3 + coerenza A/C ↔ D-canonico (NON CAP-review piena — Parte 9 è già PASS storico hash `86425a7`; NON probe-review standard — qui si audita simultaneamente 1 CAP storico + 1 report supervisore + 1 documento-indagine sorgente + 1 decoder canonico di riferimento)

**Perimetro auditato**:
- A = docs/methodology_v2/CAP_09_parte_9.md
- B = reports/REPORT_CAP_09.md
- C = tasks/INDAGINE_DIRECTA_CROSS_INDEX.md
- D = scripts/export_directa_history_parametric.py (decoder canonico, fonte CODICE-ESISTENTE)
```

### Inventario di partenza delle asserzioni a rischio (checklist iniziale, NON esaustiva)

Il Reviewer parte da questo elenco di asserzioni dichiarate o citate nel perimetro che sono potenzialmente sensibili a RM-1/2/3, e poi cerca anche asserzioni fuori da questo elenco trovate in modo indipendente nel secondo giro ostile. Numerazione W1..W11 mantenuta per simmetria con CAP-DATA-01 (i pattern d'errore si mappano direttamente).

| ID | Asserzione (paradigma) | File primario / capitolo Parte 9 | Test RM-N rilevante |
|----|------------------------|----------------------------------|---------------------|
| W1 | Schema CANDLE = `C;L;H;O` (mappatura DAPI → Portara) — Cap.49 tabella r155-164 dichiara `CANDLE campo 5 = <O>`, `campo 6 = <H>`, `campo 7 = <L>`, `campo 8 = <C>` | A Cap.49 r155-164; C (cita schema dal wiki Q2 r28 `<O>;<H>;<L>;<C>`); D `:477` (canonico `C;L;H;O`) | **RM-1 + RM-2 + W5 critico**. Verificare se A Cap.49 dichiara `O;H;L;C` (ordine wiki errato) o `C;L;H;O` (ordine canonico D). Se A dichiara `O;H;L;C` → BUG REALE catastrofico (lo schema sbagliato originale è sopravvissuto nel CAP-XX). Confrontare con D `:477-481` e con `probe_dapi.py:182-204` post-rettifica `a12ae32`. |
| W2 | Schema PRICE realtime (cash europei): `PRICE;<ticker>;<HH:mm:ss>;<last>;<volume_lot?>;<bid_qty?>;<ask_qty?>;<low_session>;<high_session>` — Cap.47 r94 | A Cap.47 r94; C INDAGINE Appendice B (campi 5/6/7 interpretati o ignoti?) | RM-1 (i campi 5/6/7 dichiarati con punto interrogativo `?` → forma RM-1 corretta o assenza di disambiguazione? Decoder di produzione D non parsa PRICE → assenza level-2). Empirico-CLI per riprodurre. |
| W3 | Schema BOOK_5 (futures): `BOOK_5;<TICKER>;<HH:mm:ss>;<bid1_lots>;<bid1_ord>;<bid1_price>;<bid2..>;<bid3..>;<bid4..>;<bid5..>;<ask1_lots>;<ask1_ord>;<ask1_price>;<ask2..>;...` (5 livelli BID + 5 livelli ASK) — Cap.47 r93 | A Cap.47 r93; C INDAGINE Appendice B | RM-1 (mai parsato bit-a-bit nel decoder canonico D — D `:467-496` parsa CANDLE, non BOOK_5; il `BOOK_5` esempio in A r93 viene da probe 27/05 di una sola candela. Alternative compatibili: ordine BID/ASK swapped, `lots` vs `orders` swapped, indice prezzo). Empirico-CLI. |
| W4 | Sintassi `CANDLERANGE <sym> <yyyyMMddHHmmss_start> <yyyyMMddHHmmss_end> <period_s>` con period_s ultimo — Cap.48 implicito, Cap.51 r240 esplicito | A Cap.51 r240; D `:228-230` (canonico emette CANDLERANGE con period_s last) | **RM-2 OK level-2** (decoder canonico corrobora). Verificare che A non dichiari ordine alternativo. MIGLIORA PROCESSO se enumerazione formale assente ma sostanza OK. |
| W5 | Codici errore DAPI 1004 / 1007 / 1030 con semantica dichiarata in tabella Cap.50 r192-196 | A Cap.50 r192-196; C INDAGINE Appendici A/B (errori 1004/1007/1017/1030 dichiarati); D `:417-425` `is_error_line` (string-match generico, NON decodifica numerici) | **RM-1 + confronto con M-3 critico**. M-3 ha ri-auditato empiricamente: 1004=cmd ignoto (coerente), 1007=ticker non abilitato (coerente), 1017 (sintassi malformata, **non in tabella A**), 1015 (NUOVO, non in A), 1003 (NUOVO, non in A), 1030 (NON RIPRODOTTO, A `:196` dichiara semantica derivata). Asserzioni di A senza disambiguazione + senza supporto in D = BUG REALE. Eredita pattern W4 di CAP-DATA-01. |
| W6 | Mese IDEM `F`=Giu, `I`=Set (Mar/Dic da decodificare) — Cap.47 r61, Cap.55 r375 | A Cap.47 r61 r96; A Cap.55 r375; C INDAGINE Appendice A | RM-1 (parziale dichiarata "lookup completa fuori scope" = forma RM-1 corretta). Confrontare con M-4 (F confermato, I confermato sul probe 27/05). Empirico-CLI per Mar/Dic + verifica che A dichiari esplicitamente "verifica parziale" per ticker candidati come `FIB6L` (r96). |
| W7 | Limite 100 giorni intraday DAPI — Cap.46 r53, Cap.51 r235-245, Cap.55 r377 | A Cap.46 r53; A Cap.51 r235-245; D `:61` `DEFAULT_INTRADAY_MAX_DAYS=100` | **RM-2 OK level-2**. Decoder canonico ha la costante. Eredita pattern W7 di CAP-DATA-01. MIGLIORA PROCESSO se etichetta `[CODICE-ESISTENTE r.61]` assente; nessun BUG. |
| W8 | Riavvio Darwin mezzanotte — Cap.50 r207, sequenza 7 step gap recovery | A Cap.50 r207-217 | RM-1 senza prova diretta empirica nel perimetro. Citazione "documentato dal wiki DAPI" (r207) → solo level 4. Empirico-CLI per riprodurre (ma è fenomeno notturno automatico, replicabile solo via osservazione passiva di una sessione cross-midnight). |
| W9 | Cooldown ~30s / 14 connessioni — Cap.46 r47, r51; Cap.50 r198 (backoff "ConnectionResetError 10054 sulla 14ª connessione TCP rapida; ConnectionRefusedError 10061 durante cooldown ~30s") | A Cap.46 r47-53; A Cap.50 r198; C INDAGINE Appendice A.4 (citato esplicitamente da A r47) | **RM-1 critico + confronto con M-5 CRITICO**. M-5 ha **REFUTATO** la dichiarazione nel regime ~1Hz (75 connessioni open/close senza cooldown). Parte 9 dichiara come fatto: BUG REALE sostanziale RM-1, **aggiornato dall'empirico** che oggi la smentisce. Eredita pattern W6 di CAP-DATA-01 + nuovo dato empirico. |
| W10 | Banner Darwin `DARWIN_STATUS;CONN_OK;TRUE;Release 2.5.1 build 04/02/2025` — Cap.46 r27, r29 | A Cap.46 r27 r29; C INDAGINE Appendice A (banner 27/05) | RM-1 (singola osservazione del 2026-05-27 — alternative? variazione di banner per versioni Darwin diverse? trattato come stringa fissa o pattern?). Etichettatura fonte RM-3: il banner cita esplicitamente la data della verifica `27/05` = level-1 [PROVA-EMPIRICA] OK; alternative su release-name variabili = Empirico-CLI minore. |
| W11 | Decisione Q-A-3 cash gating — Cap.53 | A Cap.53 (intero capitolo) | **NON asserzione empirica, è SCELTA di DESIGN. RM-1 NON si applica.** Il Reviewer verifica solo che il perimetro vincolante (no feature tensor, no state machine, no cromosoma, no walk-forward) sia scritto in modo coerente e ratificato dal supervisore (commit `bea513f` citato). NON classificare come BUG metodologico. Se il Reviewer trova ambiguità sul perimetro vincolante (es. una porta aperta nel testo che permetterebbe a cash di entrare nel cromosoma) → MIGLIORA PROCESSO (chiarimento testuale), non BUG. |

Il Reviewer è **libero di estendere** questo inventario nel secondo giro ostile (cfr. `reviewer.md`): asserzioni fuori lista che soddisfano un test RM-1/2/3 producono finding aggiuntivi W12+ con la stessa classificazione. Asserzioni aggiuntive plausibilmente a rischio (lista non esaustiva, hint per il Reviewer): dominio `source ∈ {DIRECTA, AGG_FROM_60s, AGG_FROM_D}` Cap.48 r131-138 (corroborabile da manifest D? oppure asserzione su sample committati?); schema ANAG Cap.47 r92 (campi `<ref_price>;<flag>;<flag>` con punti interrogativi sul significato); marker `RUNTIME_GAP_START`/`RUNTIME_GAP_END`/`CONTRACT_SWITCH`/`SIGNAL_TARGET_1_HIT` etc Cap.54 r339 (non sono asserzioni empiriche ma **convenzioni interne di logging**: RM-1 NON si applica direttamente; verificare solo coerenza interna con state machine Parte II Cap.7); `APIPortSettings.txt` schema 4 campi Cap.46 r41 (cita `docs/runtime/dapi_port_settings_schema.md` — verificare che il file esista e contenga lo schema dichiarato).

### Check A — RM-1 per ogni asserzione del perimetro

Per ogni asserzione presente nel perimetro A-D che dichiara o implica "verificato / confermato / fatto / stabilito / scoperto":

- **A.1 Localizzazione**: file:linea esatta, citazione testuale fra virgolette;
- **A.2 Formato 4-righe**: l'asserzione è in formato `VERIFICA/PROVE/ALTERNATIVE ESCLUSE/ALTERNATIVE NON ESCLUSE`? Se NO, classificare la non-conformità di formato (per file pre-RM è naturalmente assente: classificare come MIGLIORA PROCESSO se la sostanza è OK, BUG REALE se anche la sostanza manca — vedi A.3);
- **A.3 Sostanza** (criterio centrale): l'asserzione **enumera esplicitamente** le alternative compatibili coi dati osservati e **dichiara l'evidenza che le esclude**? Se NO, è BUG REALE (asserzione "verificato" senza esclusione di alternative — il pattern canonico CANDLE).
- **A.4 Verifica parziale opportuna**: se l'asserzione lascia alternative compatibili non escluse, andrebbe riscritta come "verifica parziale" o `X ∈ {opt_a, opt_b}`? Suggerire patch testuale concreta.
- **A.5 Confronto con prove empiriche M-3/M-4/M-5** (specifico CAP-DATA-02): se l'asserzione del perimetro è ri-caratterizzata o refutata dai risultati empirici di STATO_CORRENTE.md §5 (codici errore, mesi IDEM, cooldown), il Reviewer **CITA esplicitamente** l'M-promemoria pertinente e segna il finding come "aggiornato dall'empirico 2026-05-29 — la sostanza dell'asserzione era plausibile alla data di scrittura del CAP, oggi va ri-caratterizzata". Questa classe di finding può essere BUG REALE (se l'asserzione di Parte 9 è ora smentita: W9 cooldown) o MIGLIORA PERFORMANCE (se l'asserzione è plausibile ma andrebbe arricchita con i nuovi dati: W5 codici 1015/1003/1017 non in A, W6 mesi Mar/Dic ancora da decodificare).

### Check B — RM-2 grep nel repo e coerenza A/C ↔ D-canonico

Il Reviewer esegue **direttamente** in sede WEB il grep canonico:

```
grep -rn "parse_directa\|parse_candle\|decode_candle\|UFF\|APE\|MIN\|MAX\|CANDLE;\|CANDLERANGE\|PRICE;\|BOOK_5;\|ANAG;\|END CANDLES\|ERR;\|DARWIN_STATUS\|DEFAULT_INTRADAY_MAX_DAYS\|is_error_line\|AGG_FROM" --include='*.py' --include='*.md' .
```

(o varianti equivalenti). Esito atteso registrato nel report:
- elenco completo dei decoder/parser/comandi DAPI esistenti nel repo con path:linea (riferimento canonico atteso: `scripts/export_directa_history_parametric.py:467-496` per `parse_directa_candle`, `:477-481` per mapping CANDLE, `:228-230` per emissione CANDLERANGE, `:245,282-285,437` per `END CANDLES`, `:417-425` per `is_error_line`, `:61` per `DEFAULT_INTRADAY_MAX_DAYS`);
- verifica W5 critica: A (Cap.49 r155-164 mappatura schema, Cap.48 r131-138 dominio source, Cap.50 r192-196 codici errore, Cap.51 r240 sintassi CANDLERANGE) dichiara gli stessi schemi/sintassi/dominio che D implementa? **Divergenza nello schema CANDLE (W1) = BUG REALE catastrofico** (il pattern canonico originale).
- verifica che B (REPORT) non contenga asserzioni che riformulano lo schema CANDLE divergendo dal decoder canonico.
- verifica che C (INDAGINE) Q2 r28 cita lo schema wiki `<O>;<H>;<L>;<C>` come schema canonico — A NON deve aver ereditato questo schema errato. Se A lo eredita → BUG REALE.

Il Reviewer cita nel proprio report **il grep effettivamente eseguito** (comando + esito) per soddisfare `METODO.md:64-71` (formato obbligatorio "Decoder/parser esistenti nel repo per <sistema>").

### Check C — RM-3 etichettatura fonti

Per ogni riferimento del perimetro a documentazione esterna (wiki Directa, Telegram Bot API, Eurex docs, CME docs, Portara docs, ecc.) o a fonti interne:

- **C.1**: il riferimento è etichettato `[WIKI-HINT, da verificare]` / `[CODICE-EXISTENTE r.NNN]` / `[PROVA-EMPIRICA <data>]` / `[DOC-INTERNO]`?
- **C.2**: se NO (etichetta assente, pre-RM), il Reviewer **deduce il livello** della fonte e segnala l'omissione di etichetta come MIGLIORA PROCESSO (le etichette non esistevano quando il file è stato scritto).
- **C.3**: ESISTONO conclusioni "wiki-only" nel perimetro? A Cap.46 r27 cita esplicitamente `https://app1.directatrading.com/trading-api-directa/index.html`; A Cap.50 r207 dice "documentato dal wiki DAPI" per il riavvio mezzanotte; C INDAGINE Q2 r34 cita esplicitamente il wiki come fonte di profondità storica. Per ciascuna citazione del wiki: il fatto è corroborato da level 1-3 (empirico, codice, doc interno) oppure è wiki-only? Wiki-only senza supporto = BUG REALE per `METODO.md:112`.
- **C.4**: il wiki Directa è **dimostrato inesatto sullo schema CANDLE** (M-1, METODO.md §RM-3 riga 132). Ogni conclusione di Parte 9 che si appoggia al wiki senza corroborazione level 1-3 è automaticamente sospetta. Verificare specificamente: schema CANDLE in Cap.49 (W1 critico), profondità 100gg in Cap.46/51 (corroborata da D `:61` → OK), sessione Eurex/CME in Cap.55 / C INDAGINE Q5 (citata da C e da fonti pubbliche Directa pages, non da wiki API).

### Check D — coerenza inter-file del perimetro A-D

- **D.1**: A (CAP_09) cita C (INDAGINE) per fatti DAPI? Sì, multipli (Cap.46 r27, Cap.47 r59, Cap.50 r190, Cap.51 r235). Verificare per ciascuna citazione che il referente in C contenga davvero il fatto dichiarato. Se A dichiara "verificato in Appendice A" ma Appendice A non contiene la prova → claim → evidenza spezzato.
- **D.2**: B (REPORT) dichiara di aver "verificato AC X" — il Reviewer verifica che le evidenze citate (file:linea) puntino davvero al contenuto dichiarato. NON è audit del contenuto degli AC (è già PASS), ma audit della **mappatura claim → evidenza** (criterio 4 della probe-review).
- **D.3**: A e C divergono su qualunque fatto DAPI? In particolare lo schema CANDLE (W1): C Q2 r28 cita wiki `<O>;<H>;<L>;<C>`; A Cap.49 r158-161 dichiara mapping campi 5-8 → quale ordine? Coincidono o divergono? Se C cita lo schema wiki errato e A lo eredita, A è contaminata. Se C cita lo schema wiki errato ma A lo corregge esplicitamente (citando il decoder canonico D), C andrebbe rettificata o A va etichettata `[CORREGGE WIKI]`.
- **D.4**: D (decoder canonico) implementa schemi/sintassi/codici che A/C dichiarano: per ciascun item dell'inventario W1-W11 con potenziale corroborazione level-2, il Reviewer cita la riga di D che corrobora (o assenza di corroborazione, come per BOOK_5/PRICE che D non parsa).

### Check E — onestà claim→evidenza (criterio 4 della probe-review)

Per ogni "fatto N" / "scoperta N" del perimetro, il Reviewer richiede una **evidenza puntuale citabile**: file:linea di un dump empirico, timestamp di un test, commento di un decoder di produzione, sezione di un'Appendice interna. Asserzioni senza ancora a evidenza specifica = BUG REALE (asserzioni "in aria"). Per CAP-DATA-02, attenzione particolare a:

- E.1 Cap.47 r92-94 esempi `ANAG`/`BOOK_5`/`PRICE` reali del 27/05: hanno timestamp puntuale (`14:05:30`, `14:02:33`, `14:05:41`) → evidenza OK level-1. Ma sono **un solo evento ciascuno**: alternative su variazione del formato durante regimi diversi (orari, ticker, condizioni di mercato)? Marca Empirico-CLI minore.
- E.2 Cap.46 r47 "26 comandi CANDLERANGE sequenziali a 0,6 s di gap senza errori": singola osservazione. Alternative compatibili (gap minore, sequenza più lunga, comandi diversi)?
- E.3 Cap.46 r47 "14 connessioni TCP rapide → ConnectionResetError 10054 → cooldown ~30 secondi": **M-5 ha refutato questo nel regime ~1Hz**. Asserzione BUG REALE sostanziale.
- E.4 Cap.55 r375 lookup mese F=Giu / I=Set: forme RM-1 corrette (dichiarazione esplicita "lookup completa fuori scope, runtime-discovery") — OK.

### Asserzioni che richiedono prova empirica → handoff alla sede CLI

In coerenza con la matrice di sede di `METODO.md` §RM-4 e con il divieto `reviewer.md` (il Web reviewer NON dichiara "verificato empiricamente" niente che richieda accesso a DAPI live o filesystem locale), il Reviewer marca **come "Empirico-CLI da verificare"** ogni asserzione del perimetro la cui verifica RM-1 richiede:
- esecuzione di un comando contro DAPI live (es. ri-test schema BOOK_5/PRICE bit-a-bit di W2/W3; ri-test codici errore 1015/1003/1030 di W5 con comandi-trigger specifici; SUB di ticker trimestrale Mar/Dic per decodificare il codice mese di W6; banner Darwin su Release diverse di W10);
- ispezione di dump locali non versionati (`probe_out/`, `exports/directa_history/`, `C:\directa_history_parametric_export_overlay\`);
- riproduzione di test V-1/V-2 con parametri specifici;
- riproduzione del test M-5 con burst >>1Hz per disambiguare la soglia cooldown.

I dump `probe_out/w4_errcodes_20260529.json` e `probe_out/w6_cooldown_20260529.json` sono **locali non versionati**: il Web reviewer li cita come prove acquisite tramite M-3/M-5 (forma versionata), NON li ispeziona direttamente. Eventuali contro-verifiche dei dump appartengono alla sede CLI.

La lista "Empirico-CLI da verificare" alla fine dell'audit è l'eventuale input di una **sessione CLI separata** (vedi §"Pipeline attesa" sotto). In sede WEB il verdetto **non si chiude come PASS** se la lista CLI è non vuota (CONDITIONAL con motivazione, o PASS-condizionato-a-CLI).

---

## Acceptance criteria — tutti devono essere soddisfatti per PASS in Review

- [ ] **AC-1**: il file `reviews/REVIEW_CAP_DATA_02_RM_RETRO_review.md` esiste, è committato e pushato su `origin/main`, contiene l'header con mappatura A=CAP_09_parte_9.md / B=REPORT_CAP_09.md / C=INDAGINE_DIRECTA_CROSS_INDEX.md / D=export_directa_history_parametric.py, e contiene un verdetto esplicito PASS / CONDITIONAL / FAIL.
- [ ] **AC-2 (Check A — RM-1)**: ogni asserzione "verificato / confermato / fatto / scoperto" dei 4 file è elencata con file:linea + citazione testuale + esito A.1/A.2/A.3/A.4/**A.5 (confronto con M-3/M-4/M-5)**. L'inventario W1..W11 è coperto integralmente come baseline (cella popolata per ognuno: presente/assente nel file, esito RM-1, confronto con prove empiriche M-promemoria se pertinente). Asserzioni trovate fuori dall'inventario W1..W11 sono aggiunte come W12+.
- [ ] **AC-3 (Check B — RM-2)**: il grep canonico è eseguito direttamente dal Reviewer e il comando + esito sono citati nel report. Il confronto W5 critico A Cap.49 ↔ D `:477-481` è effettuato con citazione testuale di entrambe le posizioni (incluso ordine campi 5-8). La sezione "Decoder/parser esistenti nel repo per DAPI" è popolata secondo `METODO.md:64-71`.
- [ ] **AC-4 (Check C — RM-3)**: ogni riferimento al wiki Directa nel perimetro è elencato con file:linea, classificato per livello di fonte (4 con etichetta o dedotto), e valutato per conformità all'ordine di priorità `1>2>3>4`. Eventuali conclusioni "wiki-only" sono marcate BUG REALE.
- [ ] **AC-5 (Check D — coerenza inter-file)**: divergenze A↔C↔D (specialmente W1 schema CANDLE) sono identificate ed etichettate; mappatura claim→evidenza per B (REPORT) è verificata; citazioni di A verso C (Appendici A/B) sono validate per esistenza del referente E per correttezza del contenuto citato.
- [ ] **AC-6 (Check E — onestà)**: ogni "fatto verificato" del perimetro ha un'evidenza puntuale citabile (file:linea / test:risultato / dump:timestamp) o è marcata come "senza evidenza puntuale" (BUG REALE). Confronto specifico con M-3/M-4/M-5 documentato per W5/W6/W9.
- [ ] **AC-7 (lista Empirico-CLI)**: il Reviewer pubblica esplicitamente la sezione "Empirico-CLI da verificare" con elenco delle asserzioni che richiedono prova diretta contro DAPI o ispezione di dump locali. Se la lista è vuota → vincolo CLI sciolto. Se non vuota → la lista è completa con ID asserzione (W-N), motivazione del rinvio e test minimo proposto.
- [ ] **AC-8 — tabella di classificazione per il supervisore** con colonne `# | Problema | File:linea | Classificazione (BUG REALE / MIGLIORA PERFORMANCE / NEUTRO / RISCHIO PEGGIORAMENTO) | Modifica suggerita`. Niente proposte di modifica generiche: ogni riga indica file e sezione, con suggerimento di patch testuale concreta (o esplicita astensione: "il Reviewer non propone fix; richiede decisione del supervisore").
- [ ] **AC-9 (RM-1 applicato a sé stesso)**: nessuna asserzione "verificato X" nel REPORT del Reviewer senza enumerazione delle alternative considerate. Esempio: se il Reviewer dichiara "verificato che A Cap.49 r158-161 è coerente con D r477-481", deve enumerare cosa significa "coerente" e quali divergenze sono state cercate ed escluse (ordine 5 campi, mapping nome→OHLC, indice colonna).
- [ ] **AC-10 (RM-2 applicato a sé stesso)**: il grep di Check B è eseguito e citato; nessuna conclusione su "decoder esistenti" senza grep diretto.
- [ ] **AC-11 (RM-3 applicato a sé stesso)**: ogni riferimento del REPORT del Reviewer a documenti del perimetro è citato con file:linea, non parafrasato. Nessuna conclusione si appoggia a "ricordo del file" senza file:linea. Riferimenti a M-3/M-4/M-5 etichettati come `[PROVA-EMPIRICA 2026-05-29 via STATO_CORRENTE.md §5]`.
- [ ] **AC-12 (nessuna modifica al perimetro in Iterazione 1)**: il Reviewer NON modifica i 4 file del perimetro né alcun file del repo che non sia il proprio file di review. Working tree del Reviewer pulito su A/B/C/D al momento del commit della review.
- [ ] **AC-13 (verdetto motivato)**: il PASS si concede solo se:
  - (a) tutte le asserzioni del perimetro passano A.3 (sostanza RM-1: alternative enumerate ed escluse) — o sono già marcate come "verifica parziale" / rettificate;
  - (b) la coerenza W5 critica (schema CANDLE A Cap.49 ↔ D r.477-481) è verificata: nessuna divergenza non etichettata;
  - (c) nessuna conclusione del perimetro è "wiki-only" senza supporto level 1-3;
  - (d) la lista "Empirico-CLI da verificare" è vuota;
  - (e) nessuna divergenza non etichettata fra A e C su fatti DAPI;
  - (f) nessuna asserzione di Parte 9 è dichiarata "verificato" dove M-3/M-4/M-5 hanno ri-caratterizzato o refutato (W5 codici, W9 cooldown).
  
  Se uno qualunque di (a)..(f) fallisce → CONDITIONAL o FAIL secondo l'impatto. La lista CLI non vuota (d) trasforma automaticamente PASS in PASS-condizionato-a-CLI o CONDITIONAL con handoff alla sede CLI (decisione del Reviewer secondo entità delle asserzioni rinviate). **Il Web reviewer NON chiude in PASS asserzioni empiriche su cui ha solo evidenza di sessione web; lista CLI non vuota ⇒ non PASS pieno in WEB.**

---

## Out-of-scope — esplicito

Il Reviewer NON tratta in `REVIEW_CAP_DATA_02_RM_RETRO_review.md`:

- **Audit di contenuto di CAP-DATA-02 come capitolo metodologico** (decisioni di Cap.45-56, scelta sessione 08:00-22:00, decisioni Q-A/B-1..B-7/NB-1..NB-4, tabelle decisioni Cap.56): è già PASS hash `86425a7`. Il Reviewer audita solo le asserzioni RM-1/2/3 sensibili, non riapre acceptance criteria della review v2 storica.
- **Riapertura della decisione Q-A-3 cash gating (Cap.53)**: è una **SCELTA di design** ratificata. RM-1 NON si applica. Il Reviewer verifica solo la coerenza del perimetro vincolante, NON la decisione.
- **Audit di CAP-DATA-01 (Parte 8)**: già auditato (PASS `a5f7bcb`). Eventuali divergenze A-Parte 9 ↔ A-Parte 8 (es. sessione FIB 08:00-22:00 in Cap.41 e Cap.52) sono fuori scope. Le citazioni cross-CAP di Parte 9 verso Parte 8 (Cap.40, Cap.41, Cap.37, etc.) sono validate solo per esistenza del referente, non per correttezza del contenuto di Parte 8.
- **Audit di CAP-DATA-03 (Parte 10)**: sessione futura. Le asserzioni rinviate esplicitamente a CAP-DATA-03 da Cap.55 (continuità tape, recupero gap, riconciliazione canonica, storicizzazione strutturata) sono fuori scope qui (verifica solo che il rinvio sia esplicito e coerente).
- **Audit di FONDAMENTA-01** (prompt agenti + METODO.md): è già PASS. Le regole RM-1/2/3/4 sono input vincolante, non si riaprono.
- **Audit di altri capitoli I-VIII**: fuori scope. Nessuna citazione di Parti precedenti nel perimetro A-D di Parte 9 è oggetto di audit (sono già PASS).
- **Esecuzione di codice contro DAPI o di probe empirici**: sede CLI, fuori scope WEB. Asserzioni che richiedono prova empirica diretta vanno in lista "Empirico-CLI da verificare", non si chiudono in sede WEB.
- **Audit di dump locali** (`probe_out/`, `exports/directa_history/`, `C:\directa_history_parametric_export_overlay\`): sede CLI, fuori scope WEB. Le asserzioni su questi dump vanno in lista "Empirico-CLI da verificare". I dump `probe_out/w4_errcodes_20260529.json` e `probe_out/w6_cooldown_20260529.json` sono citati TRAMITE M-3/M-5 (forma versionata), NON ispezionati direttamente.
- **Modifica diretta dei file del perimetro o di qualunque altro file del repo (incluso `export_directa_history_parametric.py`)**: il Reviewer non patcha. Anche se identifica che A Cap.49 ha schema CANDLE errato, NON lo corregge; produce solo finding + suggerimento di patch testuale in AC-8. Le modifiche, se approvate dal supervisore al punto di controllo CONDITIONAL/FAIL, sono eseguite da un Developer in fase di rework. **Specialmente per D**: il decoder canonico è autoritativo (fonte CODICE-ESISTENTE level-2), il Reviewer NON propone mai patch a D in questa iterazione; eventuali bug del decoder vanno aperti come task separato fuori da questo audit.
- **Proposta di nuove regole RM-5..RM-N**: fuori scope. Il Reviewer può segnalare in "Osservazioni minori" che certe situazioni emergenti suggeriscono regole future, ma non le formalizza.
- **Revisione dei file di stato `STATO_CORRENTE.md`, `CARRYOVER.md`, `QUESTIONS.md`, `DEV_STATUS.md`**: fuori perimetro normativo. Possono essere letti come supporto evidenziale (M-3/M-4/M-5 per W5/W6/W9), non auditati come oggetti di output.

---

## Done when — domande operative a cui il report del Reviewer deve rispondere

1. Per ogni asserzione W1..W11 dell'inventario di partenza (+ W12+ eventuali emerse dal secondo giro), qual è l'esito RM-1? Citazione file:linea, alternative compatibili, esclusione esplicita o no?
2. Il capitolo Cap.49 di A (mappatura schema CANDLE DAPI → bundle frozen Portara) dichiara lo schema `C;L;H;O` (canonico D) o `O;H;L;C` (wiki errato)? Citazione testuale dei due punti A `:155-164` vs D `:477-481`. Coerenza o divergenza?
3. La tabella codici errore di A Cap.50 r192-196 (1004/1007/1030) è coerente con M-3? Quali codici M-3 ha aggiunto (1017, 1015, 1003) che A non cita? Il codice 1030 in A è dichiarato "atteso esclusivamente sui futures cross-index Eurex/CME" → questa è asserzione RM-1 conforme (riconosce che non è osservato sul perimetro account `B6086`) o asserzione di "verificato" non disambiguata?
4. La dichiarazione cooldown "~30s dopo 14ª connessione" in A Cap.46 r47-53 + Cap.50 r198 è coerente con M-5 [PROVA-EMPIRICA 2026-05-29 refutata nel regime ~1Hz]? Quale ri-caratterizzazione testuale serve?
5. Le citazioni di A verso C (Appendici A/B di INDAGINE_DIRECTA_CROSS_INDEX.md) sono valide (Appendici esistono e contengono il dichiarato)?
6. Le citazioni della wiki Directa nel perimetro (A Cap.46 r27, Cap.50 r207; C INDAGINE Q2 r34) sono trattate come hint o come fonte autorevole? Esistono conclusioni "wiki-only"?
7. La mappatura claim→evidenza di B (REPORT_CAP_09) regge: ogni "OK" degli AC è verificabile con file:linea?
8. Verdetto finale: il perimetro A-D di CAP-DATA-02, nello stato corrente di `origin/main`, soddisfa RM-1/2/3 retroattivamente e in coerenza con i nuovi dati empirici M-3/M-4/M-5? Se no, lista puntuale dei buchi + patch suggerita per ciascuno + classificazione BUG REALE / MIGLIORA / NEUTRO / RISCHIO PEGG. La lista "Empirico-CLI da verificare" è vuota o richiede una sessione CLI separata?

---

## Pipeline attesa

### Iterazione 1 — Review WEB

- L'Orchestratore della sessione corrente invoca **Reviewer** in sede **WEB**, con prompt che cita esplicitamente:
  - leggi `tasks/METODO.md` come prima azione;
  - leggi `tasks/ACTIVE_TASK.md` (questo file);
  - leggi `tasks/STATO_CORRENTE.md` §5 (M-3/M-4/M-5 come prove acquisite);
  - leggi `reviews/REVIEW_CAP_DATA_01_RM_RETRO_review.md` (riferimento metodologico — pattern di errore W4/W5/W6 ereditabili);
  - perimetro = 4 file A-D con i path effettivi riportati nel task;
  - sede = WEB (con divieti `reviewer.md`: NO "verificato empiricamente" su asserzioni che richiedono DAPI o dump locale; NO probe massivi di zelo);
  - esegui Check A/B/C/D/E come descritti;
  - applica RM-1/2/3 a te stesso (AC-9/10/11);
  - produci `reviews/REVIEW_CAP_DATA_02_RM_RETRO_review.md` con verdetto + tabella classificazione + sezione "Empirico-CLI da verificare" se non vuota;
  - committa e pusha su `origin/main`.
- Il Reviewer produce il file e termina (commit + push).

### Iterazione 2 — Punto di controllo supervisore (solo se CONDITIONAL/FAIL)

- L'Orchestratore esegue il **punto di controllo supervisore** (`CLAUDE.md` §"Punto di controllo supervisore"): presenta la tabella di classificazione AC-8, attende decisione del supervisore su quali finding "MIGLIORA PERFORMANCE" e "RISCHIO PEGGIORAMENTO" passare a Developer (i BUG REALI sono obbligatori).
- L'Orchestratore aggiorna `tasks/ACTIVE_TASK.md` aggiungendo sezione "## Finding di Review approvati per rework" con SOLO i finding approvati.
- Azzera `tasks/DEV_STATUS.md`.
- Invoca **Developer** con istruzione di patchare i SOLI file del perimetro A-D coinvolti dai finding approvati, secondo le patch suggerite in AC-8 modificate dalle decisioni del supervisore. Il Developer NON ridefinisce RM, NON riapre asserzioni non approvate, NON modifica file fuori dal perimetro A-D. **Specialmente: il Developer NON modifica D (decoder canonico) in questo task**; eventuali bug del decoder vanno aperti come task separato.
- Output del Developer: file del perimetro patchati su `origin/main` (A, B, C secondo necessità — D restando immutato come riferimento canonico) + report ridotto in `reports/REPORT_AUDIT_RM_RETRO_CAP_DATA_02.md` (formato ridotto: Cosa è stato modificato, Mappatura finding→patch, Verifica working tree, Verifica push). Nota: NON si tocca `reports/REPORT_CAP_09.md` esistente (che è il report originale del Developer di CAP-DATA-02, immutabile); le modifiche al file B come tale (se approvate) sono Edit chirurgici nel file stesso, separati dal report ridotto del rework.
- Developer scrive `READY_FOR_REVIEW` in `tasks/DEV_STATUS.md`.

### Iterazione 3 — Re-Review WEB (solo se Iter.2 eseguita)

- L'Orchestratore esegue check post-Developer (6 controlli adattati al fatto che NON c'è un nuovo CAP-XX: gli output attesi sono i file del perimetro patchati + il report ridotto + DEV_STATUS pulito).
- Invoca di nuovo **Reviewer** in sede **WEB** con istruzione: rieseguire i check sui file del perimetro patchati + verificare che i finding approvati siano effettivamente chiusi. Output: `reviews/REVIEW_CAP_DATA_02_RM_RETRO_v2_review.md` con verdetto PASS / CONDITIONAL / FAIL.
- Loop fino a PASS. Regola terminazione 3 iterazioni (`CLAUDE.md`): se Reviewer e Developer divergono su un finding dopo 3 giri, Planner arbitra.

### Iterazione 4 — Eventuale sessione CLI (solo se lista "Empirico-CLI da verificare" non vuota in nessuna iterazione WEB)

- Se la review WEB chiude PASS-condizionato-a-CLI o CONDITIONAL con handoff alla sede CLI, l'Orchestratore della sessione corrente:
  - prepara un **prompt-template ready-to-paste** per una sessione CLI separata, contenente la lista "Empirico-CLI da verificare" e i test minimi proposti;
  - NON esegue lui i test CLI (sessione WEB, non ha accesso al filesystem locale né a DAPI);
  - notifica il supervisore con il prompt-template e fermazione.
- La sessione CLI separata produce `reviews/PROBE_REVIEW_CAP_DATA_02_RM_RETRO_cli.md` con esiti empirici. L'Orchestratore della sessione CLI (separata da questa) raccoglie i due audit (WEB + CLI) e produce il verdetto finale consolidato. NB: questa fase è fuori dal perimetro temporale della sessione corrente.

### Chiusura sessione PASS — adattata (NON sono le 7 condizioni standard CAP-XX)

Quando la Review WEB chiude PASS e la lista "Empirico-CLI da verificare" è vuota (oppure è stata chiusa in una sessione CLI successiva):

1. Review PASS pubblicata su `origin/main` (`reviews/REVIEW_CAP_DATA_02_RM_RETRO_review.md` o `_v2_review.md`).
2. `DEV_STATUS.md` azzerato (se Iterazione 2/3 eseguita).
3. Eventuale `reports/REPORT_AUDIT_RM_RETRO_CAP_DATA_02.md` pubblicato (solo se rework eseguito).
4. `docs/methodology_v2/00_indice.md` **NON va aggiornato** (Parte 9 resta PASS storico inalterato; questo task NON è un CAP-XX). 
5. `tasks/ACTIVE_TASK.md` resta puntato a questo task (storico).
6. `tasks/CARRYOVER.md` aggiornato **solo se** la Review ha prodotto raccomandazioni di processo da registrare come `RACC-METODO-N` (namespace separato dai M-promemoria di capitolo).
7. `tasks/STATO_CORRENTE.md` aggiornato: in particolare i M-promemoria pertinenti (se le rispettive asserzioni W-N sono state riauditate o marcate "verifica parziale"), e una nota di sessione che indica "AUDIT-RM-RETRO CAP-DATA-02 chiuso PASS, debito retroattivo RM-4 su perimetro A-D saldato".
8. Notifica al supervisore con riepilogo (hash review PASS, conteggio finding, eventuali Empirico-CLI rinviati a sessione CLI separata) **senza** prompt-template per CAP-XX successivo: il supervisore decide quando aprire la sessione successiva (CAP-DATA-03 o altro).

---

## Pipeline sintetica

```
Reviewer(WEB) Iter.1
  ↓
verdetto PASS + lista CLI vuota       → chiusura sessione (8 punti adattati)
verdetto PASS + lista CLI non vuota   → prompt-template CLI al supervisore + chiusura sessione parziale (verdetto WEB OK, CLI rinviata)
verdetto CONDITIONAL/FAIL             → controllo supervisore → Developer Iter.2 → Reviewer Iter.3 → loop fino a PASS
```

---

## Note al Reviewer (vincoli operativi specifici di questo task)

- **Tono dell'audit retroattivo**: questo NON è un audit "ostile" su lavoro fresco appena consegnato; è un audit retroattivo su file pre-RM-1..RM-4 (Parte 9 pubblicata 28/05 lo stesso giorno dell'introduzione delle regole). Il Reviewer distingue chiaramente fra:
  - **non-conformità di formato** dovute alla pre-esistenza del file rispetto a RM (es. assenza del blocco 4-righe, assenza etichette di livello fonte): MIGLIORA PROCESSO se la sostanza regge;
  - **non-conformità sostanziale** (asserzioni dichiarate "verificato" senza enumerazione di alternative anche sostanzialmente): BUG REALE, indipendentemente dalla data del file;
  - **asserzioni ri-caratterizzate o refutate dall'empirico più recente M-3/M-4/M-5**: BUG REALE sostanziale (l'asserzione di Parte 9 è oggi disallineata da prove disponibili). Esempio canonico: W9 cooldown — Parte 9 dichiara "30s dopo 14a", M-5 ha refutato nel regime ~1Hz.
  Il Reviewer è ostile sulla **sostanza** e sulla **coerenza con prove empiriche disponibili oggi**, comprensivo sul **formato pre-RM**.
- **Quattro tipi di file misti nel perimetro**:
  - A è un CAP metodologico già PASS: focus RM-1 sostanziale su asserzioni "verificato" + RM-3 su citazioni esterne + confronto con M-3/M-4/M-5; nessuna riapertura di contenuti AC né di decisioni di design (Q-A-3).
  - B è un report supervisore: focus criterio 4 della probe-review (mappatura claim→evidenza) e RM-1 su eventuali asserzioni "verificato schema X".
  - C è un documento-indagine sorgente: focus RM-1 sostanziale su "fatti dichiarati Q1-Q5" + RM-3 su citazioni wiki; coerenza con A (è la fonte da cui A attinge).
  - D è un decoder di produzione **fonte di verità** (CODICE-ESISTENTE level-2): il Reviewer NON audita D come oggetto da modificare, lo legge come **riferimento** rispetto al quale verificare A e C. Il Reviewer NON propone patch a D in questa iterazione.
  Il Reviewer **non miscela** i criteri di giudizio: il fatto che A sia PASS non protegge le sue asserzioni "verificato" dalla setacciatura RM-1; il fatto che C sia un documento informale di indagine non gli consente di lasciare asserzioni "in aria"; il fatto che D sia decoder di produzione canonico non gli consente di assumere che A/C siano automaticamente coerenti con D (anzi, il Check W5 deve provarlo).
- **Niente cosmesi**: non riportare problemi di formattazione/stile che non cambiano il comportamento del sistema. Focus solo su finding che, se non chiusi, lasciano un cammino aperto al pattern d'errore canonico CANDLE o producono salute dati non-RM-compliant per CAP-DATA-03 a valle.
- **Citazioni testuali obbligatorie**: ogni finding cita il testo esatto dal file (file:linea + virgolette). Niente parafrasi. Il supervisore deve poter verificare con un click ogni finding.
- **Lo script in D non si modifica mai dal Reviewer**: anche se il Reviewer rileva ipotesi di patch per D (es. nuovi codici errore da decodificare), NON propone fix in questa iterazione. Apre solo finding informativi su D (se rilevanti per A/C). I bug del decoder vanno gestiti in task separato.
- **Coerenza con M-1 di STATO_CORRENTE.md**: il Reviewer può **assumere come dato** che lo schema CANDLE reale è `C;L;H;O` (V-1 ha provato lo swap O/C, commit `a12ae32` ha rettificato il decoder probe_dapi.py, decoder canonico D `:477` era già corretto da settimane) — NON deve riauditare la rettifica empirica del 29/05. Audita SOLO la propagazione formale della rettifica nei file del perimetro (in particolare W1 critico: A Cap.49 r158-161 dichiara `O;H;L;C` o `C;L;H;O`?).
- **Coerenza con M-3/M-4/M-5**: il Reviewer assume come dato i risultati di STATO_CORRENTE.md §5, citandoli come `[PROVA-EMPIRICA 2026-05-29 via STATO_CORRENTE.md §5]`. NON ispeziona i dump `probe_out/*` (locali non versionati, sede CLI).
- **RM-1 applicato a sé stesso (AC-9)**: esempio paradigmatico. Se il Reviewer dichiara "verificato che A Cap.49 schema CANDLE è coerente con D canonico", deve enumerare cosa significa "coerente": (a) ordine dei 5 campi numerici (5,6,7,8,9), (b) mapping nome→OHLC (UFF→close, MIN→low, MAX→high, APE→open, V→volume), (c) indice di colonna in CSV runtime. Se (a) o (b) o (c) non sono state verificate, scrive "verifica parziale" (la propria) e marca W1 come finding aperto.

---

## Note al Developer (solo se Iterazione 2 viene attivata)

- Patchare **solo** i finding approvati dal supervisore. Niente patch "mentre ci sono".
- Modifiche **solo** ai file del perimetro effettivamente coinvolti dai finding approvati. Niente edit a file fuori dal perimetro A-D senza approvazione esplicita.
- Mantenere la coerenza inter-file: una modifica ad A può richiedere riflesso in C (e viceversa); documentare nel report ridotto la mappatura.
- Nessuna modifica al contenuto sostanziale di A (Parte 9 è PASS storico): le eventuali patch su A sono ammesse SOLO per (i) etichettatura fonti RM-3 mancanti, (ii) ri-caratterizzazione di asserzioni "verificato" come "verifica parziale" alla luce di M-3/M-4/M-5, (iii) correzione di una citazione "verificato" che lascia alternative non escluse, (iv) correzione di un eventuale errore catastrofico W1 schema CANDLE se confermato dal Reviewer. Modifiche più sostanziali (es. ridefinizione di decisioni Q/B/NB) = richiedono nuovo task Planner.
- Per C (`tasks/INDAGINE_DIRECTA_CROSS_INDEX.md`): se i finding richiedono ri-caratterizzazione di "fatti" Q1-Q5 alla luce di M-3/M-4/M-5, applicare con etichetta `[REFUTATO 2026-05-29]` / `[VERIFICA PARZIALE]` + citazione M-promemoria. Il vecchio testo non si cancella ma si etichetta inequivocabilmente.
- Per D (`scripts/export_directa_history_parametric.py`): **NON modificare** in questo task. Il decoder canonico è autoritativo. Eventuali bug del decoder vanno aperti come task separato.
- Commit message format: `[AUDIT-RETRO] patch <file> — chiusura finding <#> (RM-N)`.
- Push diretto a `origin/main` (push policy MEMORY).
- Al termine: `READY_FOR_REVIEW` in `tasks/DEV_STATUS.md`.

---

## RM-2 — Decoder esistenti nel repo da leggere prima di assumere format (vincolo Planner secondo `tasks/METODO.md` §RM-2)

Per soddisfare il vincolo metodologico applicato al Planner, questo task elenca per il Reviewer i decoder DAPI già noti al momento della stesura del task card. Il Reviewer è comunque **tenuto a rifare il grep direttamente** (Check B) per individuare eventuali decoder mancanti da questa lista.

Decoder/parser/comandi DAPI noti al Planner nel repo:
- **`scripts/export_directa_history_parametric.py:467-496`** — `parse_directa_candle`, decoder di produzione canonico per schema CANDLE. Riga `:477` commento esplicito `# Documentazione Directa: UFF, MIN, MAX, APE => close, low, high, open.` con mapping `close_v=Decimal(uff)` (`:478`), `low_v=Decimal(min_)` (`:479`), `high_v=Decimal(max_)` (`:480`), `open_v=Decimal(ape)` (`:481`). Schema canonico `C;L;H;O`. **Fonte CODICE-ESISTENTE level-2 di riferimento per W1**.
- **`scripts/export_directa_history_parametric.py:228-230`** — emissione comando CANDLERANGE con sintassi `CANDLERANGE {symbol} {start} {end} {period_seconds}` (period LAST). Fonte level-2 per W4.
- **`scripts/export_directa_history_parametric.py:245,282-285,437`** — uso di `END CANDLES` come terminatore stream history. Fonte level-2 per terminatore.
- **`scripts/export_directa_history_parametric.py:417-425`** — `is_error_line`, decoder errori che fa string-matching generico `ERR`/`Wrong`/`error`, NON decodifica codici numerici. Fonte level-2 per W5 (semantica codici NON corroborata in D).
- **`scripts/export_directa_history_parametric.py:61`** — costante `DEFAULT_INTRADAY_MAX_DAYS=100`. Fonte level-2 per W7 (limite 100gg corroborato).
- **`scripts/probe_dapi.py:182-204`** — decoder `parse_line` ramo CANDLE post-rettifica `a12ae32`, coerente con D `:477-481` (citabile come supporto, NON oggetto di audit qui — già auditato in CAP-DATA-01 PASS).
- `scripts/update_inventory_indici_futures_daily.py` — consumer di dati storici DAPI (potrebbe contenere parsing minimo: il Reviewer estende il grep se necessario).

Se il grep RM-2 del Reviewer rivela decoder aggiuntivi non in questa lista, il finding è un'estensione naturale del Check B, non un'incompletezza del task card.

---

## RM-3 — Etichettatura fonti del task card

Riferimenti citati in questo task card e loro livello (`METODO.md` §RM-3):

- `tasks/METODO.md`, `.claude/CLAUDE.md`, `.claude/agents/reviewer.md`, `tasks/ACTIVE_TASK.md` precedente — `[DOC-INTERNO]` (livello 3, vincolante per processo);
- `scripts/export_directa_history_parametric.py:477` (schema CANDLE), `:228-230` (CANDLERANGE), `:245,282-285,437` (END CANDLES), `:417-425` (is_error_line), `:61` (max days) — `[CODICE-EXISTENTE r.NNN]` (livello 2);
- M-1 di `tasks/STATO_CORRENTE.md` §5 (schema CANDLE reale) — `[PROVA-EMPIRICA 2026-05-29 V-1 capture]` (livello 1);
- M-3 di `tasks/STATO_CORRENTE.md` §5 (codici errore ri-auditati) — `[PROVA-EMPIRICA 2026-05-29 dump probe_out/w4_errcodes_20260529.json via STATO_CORRENTE.md]` (livello 1, dump locale non versionato citato tramite M-promemoria);
- M-4 di `tasks/STATO_CORRENTE.md` §5 (mese F/I confermati) — `[PROVA-EMPIRICA 2026-05-27 + 2026-05-29 ANAG SUB]` (livello 1);
- M-5 di `tasks/STATO_CORRENTE.md` §5 (cooldown REFUTATO) — `[PROVA-EMPIRICA 2026-05-29 dump probe_out/w6_cooldown_20260529.json via STATO_CORRENTE.md]` (livello 1, dump locale non versionato citato tramite M-promemoria);
- `reviews/REVIEW_CAP_DATA_01_RM_RETRO_review.md` (pattern di errore W4/W5/W6) — `[DOC-INTERNO]` (livello 3, riferimento metodologico);
- commit `a12ae32` (fix CANDLE schema in probe_dapi.py), `7bb2955` (errore originale), `86425a7` (review CAP-DATA-02 v2 PASS), `9bd35ba` (CAP_09 v2), `a5f7bcb` (chiusura AUDIT-RM-RETRO CAP-DATA-01), `074fba4` (Re-Review CAP-DATA-01 v2 PASS) — `[DOC-INTERNO]` (eventi storici del repo);
- **wiki Directa DAPI** (`https://app1.directatrading.com/trading-api-directa/index.html`, citato da A Cap.46 r27 e da C INDAGINE Q2 r34) — `[WIKI-HINT, dimostrato inesatto su schema CANDLE]` (livello 4, non usato come fonte di verità da questo task; citato solo come oggetto di test RM-3 nel perimetro).

Nessuna conclusione di questo task card si appoggia esclusivamente a livello 4.

---

## RM-4 — Modalità di review per output non-CAP previsti dal task

Output non-CAP attesi da questo task:
- **`reviews/REVIEW_CAP_DATA_02_RM_RETRO_review.md`** (output del Reviewer Web Iter.1) — è esso stesso un audit, copre la propria RM-4 per costruzione. Nessuna self-review aggiuntiva richiesta.
- **Eventuali patch ai file A (CAP_09) o C (INDAGINE) in Iterazione 2** — se il Developer modifica `CAP_09_parte_9.md` o `INDAGINE_DIRECTA_CROSS_INDEX.md`, l'output rientra nuovamente in RM-4 criterio (b) di `CLAUDE.md` (modifica un fatto già dichiarato "verificato"). Modalità obbligatoria: opzione B (probe-review formale) eseguita dal Reviewer Iter.3, che già è prevista nella pipeline. Nessuna self-review opzione A è ammessa per le patch di Iter.2 su A.
- **`reports/REPORT_AUDIT_RM_RETRO_CAP_DATA_02.md`** (output del Developer in Iter.2, formato ridotto) — è documento di handoff, rientra in RM-4 criterio (b). Modalità: opzione A (self-review esplicita dell'autore in fondo al documento con blocco 4-righe RM-1 per ogni "verificato"). Auto-review del Developer obbligatoria prima del commit.

---

## Verifica esplicita dell'eredità (secondo giro del Planner — checklist obbligatoria)

- [x] **RM-1 applicata al task**: le citazioni di "fatti già verificati" dei task precedenti (M-1 schema CANDLE, hash storici PASS CAP-DATA-02 e CAP-DATA-01) sono accompagnate dall'evidenza di esclusione delle alternative (V-1 ha provato lo swap O/C, M-3/M-5 hanno ri-auditato/refutato empiricamente). Nessuna asserzione di task precedente è usata come dato senza supporto empirico citato.
- [x] **RM-2 applicata al task**: il task tocca parsing DAPI (è il cuore del Check B); i decoder/comandi esistenti nel repo sono citati esplicitamente (sezione "RM-2 — Decoder esistenti nel repo" sopra con path:linea precisi). Il Reviewer è comunque tenuto al grep diretto in Check B.
- [x] **RM-3 applicata al task**: ogni riferimento esterno nel task card è etichettato per livello (sezione "RM-3 — Etichettatura fonti" sopra). Nessuna conclusione è "wiki-only". Il wiki Directa è esplicitamente etichettato `[WIKI-HINT, dimostrato inesatto su schema CANDLE]`.
- [x] **RM-4 applicata al task**: output non-CAP previsti dal task sono elencati con modalità di review obbligatoria (sezione "RM-4 — Modalità di review" sopra).
- [x] **M-promemoria carryover**: M-1 di STATO_CORRENTE.md è premessa (schema CANDLE); M-3/M-4/M-5 sono integrati come eredità #9/#10/#11 critiche (input al Check A.5). M-2/M-6/M-7/M-8 non pertinenti. CARRYOVER.md M-2 latenza Telegram esplicitamente fuori scope.
- [x] **Pattern di errore ereditati da CAP-DATA-01**: W4/W5/W6 dell'audit CAP-DATA-01 mappati esplicitamente su W5/W6/W9 di CAP-DATA-02 (eredità #12/#13/#14/#15).
- [x] **Q-XX aperte**: nessuna ambiguità reale richiede apertura di Q-XX in QUESTIONS.md. Il perimetro è netto, le regole sono vincolanti, la modalità Review-First è in linea con il precedente AUDIT-RM-RETRO CAP-DATA-01 (PASS `a5f7bcb`).
- [x] **Impatto sul GA**: la salute dati DAPI runtime è il prerequisito per la pipeline di inference real-time (Parte VI Cap.27) che alimenta direttamente il GA con feature live. Schema CANDLE corretto in Cap.49 = bundle frozen può essere applicato senza re-calibrazione; codici errore corretti in Cap.50 = recovery deterministico in produzione (non emette segnali su stato di gateway compromesso); cooldown ri-caratterizzato in Cap.46 = backoff esponenziale ben dimensionato (non spreca tentativi né causa cascade di errori); mesi IDEM corretti in Cap.47 = front-month derivation corretta (signal-to-trade conversion accurata, no segnali su contratto scaduto). Un perimetro A-D RM-compliant è la condizione necessaria perché CAP-DATA-03 parta da fondamenta affidabili invece che da fatti "compatibili con i dati ma non verificati o oggi refutati". Impatto identificabile sul ranking dei cromosomi (via qualità dei dati live di feature), sulla fitness reale (via correttezza dei rendimenti su barre runtime), sulla conversione signal-to-trade (via correttezza del payload runtime DAPI + recovery operativo).
- [x] **Scope**: dentro = perimetro A-D + grep RM-2 + confronto con M-3/M-4/M-5 + lista Empirico-CLI; fuori = CAP-DATA-01 (già auditato), CAP-DATA-03 (futuro), capitoli I-VIII, Q-A-3 cash gating (scelta di design), modifiche a D (decoder canonico autoritativo), esecuzione DAPI. Esplicito.
- [x] **Acceptance criteria verificabili**: AC-1..AC-13 sono verificabili senza ambiguità (presenza di file, presenza di sezioni, esecuzione di grep, esiti puntuali per ogni W-N, confronto puntuale con M-promemoria).
- [x] **Done when**: 8 domande operative concrete, con W1 critico esplicito (schema CANDLE coerenza A↔D).
- [x] **Niente numeri inventati**: il task non introduce nuove soglie o parametri; eredita i criteri di classificazione di `reviewer.md` e i criteri RM di `METODO.md`.

---

**Fine del task card.**
