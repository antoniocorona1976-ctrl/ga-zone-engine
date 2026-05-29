# Review FONDAMENTA-01 — Audit indipendente RM-1..RM-4 e loro agganci nei prompt agenti

**Task**: AUDIT-FONDAMENTA-01 (`tasks/ACTIVE_TASK.md` commit `320f4fa`)
**Perimetro auditato (P1..P5)**:
- P1 `tasks/METODO.md` (commit `de2938d` + `916278a`)
- P2 `.claude/CLAUDE.md`
- P3 `.claude/agents/planner.md`
- P4 `.claude/agents/developer.md`
- P5 `.claude/agents/reviewer.md`
- **Stato git**: `origin/main` allineato a `320f4fa`; working tree pulito sul perimetro (solo `.claude/scheduled_tasks.lock` non versionato, fuori scope).
- **Sede**: WEB (container Linux cloud, nessuna esecuzione contro DAPI possibile né necessaria).
- **Conflitto di interesse epistemico dichiarato**: P1..P5 sono stati scritti dalla stessa sessione web 28/05 che ha causato l'incidente CANDLE (`tasks/ACTIVE_TASK.md:181-182`). Audit condotto con sospetto sistematico verso clausole auto-assolutorie.

---

## Verdetto

**FAIL**

Motivazione sintetica ancorata a Check B/C (dettaglio in §Check B e §Check C):

1. **C.1 (fuga reale)**: nessuna riga di `.claude/CLAUDE.md` impone all'Orchestratore di rilevare *ex-ante* (prima del commit dell'autore) che un output rientra in RM-4. La sezione "Workflow per output non-CAP" (`CLAUDE.md:114-144`) descrive cosa fare *se* l'output rientra, ma non c'è alcun trigger nella "Macchina a stati" (`CLAUDE.md:20-30`) che faccia entrare un agente in quel ramo. L'Orchestratore istanzia Developer solo via `ACTIVE_TASK.md` (workflow CAP-XX); per output prodotti **da una sessione web come quella 28/05** (probe + handoff fuori dal ciclo Planner->Developer->Reviewer), nessun gate esiste.
2. **C.2 (fuga reale)**: nessun meccanismo di blocco pre-commit/pre-push esiste nei prompt. `developer.md:30,159` consente al Developer di committare/pushare prima di scrivere `READY_FOR_REVIEW`; la pre-consegna checklist (`developer.md:131-159`) gira *dopo* il push (punto 6: "Push verificato"). Per output non-CAP, non c'è proprio una checklist analoga: l'opzione A di RM-4 è descritta solo in `CLAUDE.md:126-128` come istruzione all'Orchestratore, non come obbligo dell'agente autore.
3. **C.4 (fuga reale)**: il check RM-2 (punto 11 della pre-consegna Developer, `developer.md:155`) è **vincolato al ciclo CAP-XX**. La pre-consegna parte solo se l'agente sta seguendo il workflow Planner->Developer->Reviewer (`developer.md:25,30`: "Leggi tasks/ACTIVE_TASK.md prima di ogni task" + "Output: file in docs/methodology_v2/"). Un agente in sessione web che produce uno script di parsing fuori dal ciclo CAP non passa mai da `developer.md:155`.
4. **C.5 (fuga reale)**: nessun meccanismo di recupero post-commit per output non-CAP. L'Orchestratore della sessione successiva non ha un check obbligatorio di sospetto verso handoff/probe non revisionati prodotti dalla sessione precedente. Il file `MEMORY.md` non è citato in `CLAUDE.md` come fonte obbligatoria.

Tutti e 4 i punti di fuga sono **esattamente quelli che hanno permesso l'incidente CANDLE del 28/05**. AC-S del task (`tasks/ACTIVE_TASK.md:119`) impone che se anche un solo punto C.1..C.5 risulta "fuga", il verdetto NON può essere PASS. 4 fughe documentate -> **FAIL**.

---

## AC-7 — grep eseguito (auto-applicazione RM-2)

Eseguiti:
- `grep -rn "RM-1|RM-2|RM-3|RM-4" .claude/` -> 31 occorrenze in `.claude/CLAUDE.md`, `.claude/agents/planner.md`, `.claude/agents/developer.md`, `.claude/agents/reviewer.md`
- `grep -rn "RM-1|RM-2|RM-3|RM-4" tasks/` -> occorrenze in `tasks/METODO.md`, `tasks/ACTIVE_TASK.md`, `tasks/STATO_CORRENTE.md`

Output integrale citato in sezione "Grep RM-* su perimetro" più sotto. Nessuna occorrenza non attesa rilevata fuori perimetro (in particolare nessuna in `reports/`, `reviews/` di capitoli, `MEMORY.md`).


---

## Check A — Matrice 4 RM x 4 ruoli (aggancio: presenza / azionabilità / pertinenza)

Legenda:
- **AZIONABILE**: l'aggancio nel prompt è un'istruzione operativa concreta che produce comportamento osservabile (es. checklist con punto numerato, sezione vincolante con formato output).
- **GENERICO**: l'aggancio cita la regola ma non produce comportamento osservabile (es. "leggi METODO.md", "applica RM-N", senza specificare cosa fare).
- **ASSENTE**: nessun aggancio nel prompt.

### Matrice 16 celle

**RM-1 / Orchestrator**: **GENERICO** — `CLAUDE.md:7` cita RM-1 nell'elenco; nessuna istruzione operativa successiva per Orchestrator. Pertinenza: BASSA (Orchestrator non produce dichiarazioni di verifica direttamente, ma dovrebbe gatekeepare i commit con dichiarazioni "verificato"). Buco: vedi §Check B.1.

**RM-1 / Planner**: **AZIONABILE** — `planner.md:17` (operatività: apre Q-XX se trova "verificato" non disambiguato in eredità) + `planner.md:138` (checklist secondo giro). Pertinente.

**RM-1 / Developer**: **AZIONABILE** — `developer.md:16` (definizione operativa con esempio CANDLE) + `developer.md:153` (pre-consegna punto 10, checklist vincolante prima di READY_FOR_REVIEW). Pertinente. **Limite**: l'aggancio gira solo nel ciclo CAP-XX (cfr. C.3).

**RM-1 / Reviewer**: **AZIONABILE** — `reviewer.md:17` (definizione check ostile + classificazione BUG REALE) + `reviewer.md:56` (cosa cerca) + `reviewer.md:114` (probe-review check 1). Pertinente.

**RM-2 / Orchestrator**: **GENERICO** — `CLAUDE.md:7` nell'elenco; nessuna istruzione operativa per Orchestrator. Pertinenza: BASSA-MEDIA (Orchestrator non scrive parser, ma dovrebbe verificare che il grep sia documentato prima di lasciare passare un commit non-CAP — assente).

**RM-2 / Planner**: **AZIONABILE (parziale)** — `planner.md:18` (istruzione: includere nel task una sezione "Decoder esistenti nel repo") + `planner.md:139` (checklist). Pertinente come pre-condizione del task.

**RM-2 / Developer**: **AZIONABILE** — `developer.md:18` (comando `grep -rn` esplicito + obbligo REPORT sezione "Decisioni rilevanti") + `developer.md:155` (pre-consegna punto 11). Pertinente. **Limite C.4**: vincolato al ciclo CAP-XX, vedi §Check C.4.

**RM-2 / Reviewer**: **AZIONABILE** — `reviewer.md:19` (Reviewer esegue grep autonomamente, classificazione BUG REALE) + `reviewer.md:57` (replica) + `reviewer.md:116` (probe-review check 2). Pertinente.

**RM-3 / Orchestrator**: **GENERICO** — `CLAUDE.md:7` nell'elenco; nessuna istruzione operativa. Pertinenza: BASSA.

**RM-3 / Planner**: **AZIONABILE** — `planner.md:19` (etichetta `[WIKI-HINT]` obbligatoria nei task) + `planner.md:140` (checklist). Pertinente.

**RM-3 / Developer**: **AZIONABILE** — `developer.md:20` (etichette obbligatorie `[PROVA-EMPIRICA]`, `[CODICE-EXISTENTE]`, `[WIKI-HINT]`) + `developer.md:157` (pre-consegna punto 12). Pertinente. **Limite**: l'inammissibilità del livello-4-solo è nel testo (`developer.md:20`) ma la pre-consegna punto 12 non esplicita il criterio di rigetto. Vedi §Check B.2.

**RM-3 / Reviewer**: **AZIONABILE** — `reviewer.md:21` (BUG REALE se conclusione wiki-only) + `reviewer.md:58` + `reviewer.md:118` (probe-review check 3). Pertinente.

**RM-4 / Orchestrator**: **AZIONABILE (con buchi)** — `CLAUDE.md:11` (Orchestrator applica RM-4 ai commit non-CAP) + `CLAUDE.md:114-144` (sezione dedicata: trigger, opzioni A/B, soglia 200 righe, matrice Web/CLI). Pertinente come ruolo principale. **Buchi gravi**: (a) trigger della sezione assente dalla "Macchina a stati" `CLAUDE.md:20-30`; (b) opzione A descritta come "L'autore aggiunge..." senza enforcement (`CLAUDE.md:127`); (c) soglia 200 righe ambigua (vedi §Check E.3). Vedi §Check C.1/C.2.

**RM-4 / Planner**: **AZIONABILE (parziale)** — `planner.md:20` (specifica nel task se A o B) + `planner.md:141` (checklist). Pertinente come obbligo di pianificazione. **Limite**: vincola solo i task pianificati dal Planner; per output che nascono fuori da un task (sessione web che produce probe ad hoc come 28/05) non c'è copertura.

**RM-4 / Developer**: **GENERICO** — `developer.md:22` rinvia a METODO.md senza istruzione operativa concreta ("esegui self-review esplicita o richiedi review formale leggera dell'Orchestrator. Vedi METODO.md per il formato"). Nessuna checklist analoga ai punti 10-12 per output non-CAP. **Pertinente e BUCO**: il Developer è l'agente che potrebbe produrre output non-CAP, ma il suo prompt non ha un punto di pre-consegna RM-4. Vedi §Check C.2.

**RM-4 / Reviewer**: **AZIONABILE** — `reviewer.md:23` rinvia alla sezione `reviewer.md:80-173` "Probe-review (RM-4)" con matrice sede, 4 check, formato output. Pertinente. **Limite**: il Reviewer entra in probe-review solo se invocato dall'Orchestratore, e il trigger di invocazione è il buco di C.1.

**Conteggio celle**:
- AZIONABILE pertinente: 11 (Planner x4, Developer x3 [RM-1/2/3], Reviewer x4)
- AZIONABILE con buchi: 1 (Orchestrator RM-4)
- GENERICO dove la RM è pertinente: 4 (Orchestrator RM-1/2/3, Developer RM-4)
- ASSENTE: 0

**Finding di Check A**:
- **F-A1**: Orchestrator ha RM-1/RM-2/RM-3 solo come elenco enunciativo (`CLAUDE.md:7`), senza istruzioni operative di gatekeeping sui commit non-CAP che contengono dichiarazioni "verificato", riscritture di parser, o citazioni di fonti esterne. **Classificazione**: MIGLIORA PROCESSO.
- **F-A2**: Developer ha RM-4 solo in forma GENERICA (`developer.md:22`). La pre-consegna checklist `developer.md:131-159` ha punti 10/11/12 per RM-1/2/3 ma nessun punto 13 per RM-4 "se ho prodotto output non-CAP, ho eseguito self-review opzione A?". **Classificazione**: BUG REALE (è esattamente il vuoto che ha permesso `probe_dapi.py` + handoff 28/05 a passare senza review).


---

## Check B — Coerenza fra `METODO.md` e i prompt

### B.1 — Formato RM-1 `VERIFICA / PROVE / ALTERNATIVE ESCLUSE / ALTERNATIVE NON ESCLUSE`

`tasks/METODO.md:28-33` dichiara il formato obbligatorio:

```
VERIFICA: <asserzione>
PROVE: <quali dati osservati, quale test eseguito>
ALTERNATIVE COMPATIBILI ESCLUSE: <elenco esplicito>
ALTERNATIVE COMPATIBILI NON ESCLUSE: <elenco esplicito>
```

Verifica nei prompt:
- `planner.md:138`: cita "evidenza di esclusione delle alternative compatibili" — NON impone il formato 4-righe.
- `developer.md:153` (pre-consegna punto 10): "c'è enumerazione esplicita delle alternative compatibili coi dati osservati e dell'evidenza che le esclude" — NON impone il formato.
- `reviewer.md:17,56,114`: parla di "enumerazione" — NON cita il formato 4-righe come criterio.

**Finding F-B1**: il formato 4-righe obbligatorio di `METODO.md:28-33` non è esigibile da nessuno dei 4 prompt. Nessun agente è obbligato a *produrre* o *verificare* il formato esatto. Resta un'enunciazione che il Developer può tradurre in qualunque forma testuale, e il Reviewer può accettare qualunque forma testuale come compliant. Buco di esigibilità.
**Impatto**: medio. L'enumerazione delle alternative è il core di RM-1 ed è agganciata. Ma senza un formato fisso, il pattern dell'errore 28/05 (asserzione "verificato X" nel testo libero del REPORT, senza una struttura riconoscibile come "blocco VERIFICA") può ripetersi e non essere intercettato a colpo d'occhio.
**Classificazione**: MIGLIORA PROCESSO.

### B.2 — Ordine di priorità fonti di RM-3 e rigetto del livello-4-solo

`tasks/METODO.md:104-112` definisce l'ordine `(1) empirico > (2) codice produzione > (3) docs interni > (4) wiki/docs esterni` e dichiara "Una conclusione basata solo sul livello 4 senza supporto dai livelli 1-3 è **inammissibile**".

Verifica nei prompt:
- `planner.md:19`: solo etichetta `[WIKI-HINT]`, non parla di inammissibilità.
- `developer.md:20`: testo *cita* "Una conclusione che si appoggia solo a wiki/docs ufficiale senza supporto dai livelli 1-3 è inammissibile" — OK.
- `developer.md:157` (pre-consegna punto 12): "Nessuna conclusione poggia solo su livello 4 (wiki/docs esterni) senza supporto dai livelli 1-3" — OK, esigibile in pre-consegna.
- `reviewer.md:21`: "Una conclusione che si appoggia solo a wiki/docs esterni senza supporto dai livelli 1-3 è BUG REALE" — OK.
- `reviewer.md:118` (probe-review): "le conclusioni si appoggiano a fonti di livello 1-3, non solo al livello 4" — OK.

**Esito B.2**: criterio di rigetto presente in Developer (pre-consegna 12) e in Reviewer (sia CAP-review sia probe-review). Non presente in Planner, ma Planner non produce conclusioni tecniche, definisce solo task: la sua etichettatura `[WIKI-HINT]` nel task è sufficiente come segnale a Developer. **Nessun finding B.2 di gravità (B.2 OK).**

### B.3 — Matrice Web/CLI di RM-4 ripresa coerentemente in `CLAUDE.md` e `reviewer.md`

`tasks/METODO.md:183-190` definisce la matrice. Confronto:

`CLAUDE.md:140-142`:
- Web per: CAP-XX, documenti (handoff, indagine, probe_*.md), audit statico di script (RM-1/2/3 + grep)
- CLI per: risultati empirici (V-1, V-2), riproduzione di test contro DAPI, audit di dump locali
- Entrambe per: script di parsing/decoder, asserzioni "verificato X" da CAP precedenti

`reviewer.md:102-108` (tabella sede):
- Documento (handoff, indagine, probe_*.md) -> Web primario
- Script di parsing/decoder -> Web audit statico + CLI solo se richiesto
- Risultato empirico (V-1, V-2) -> CLI primario
- Asserzione "verificato X" -> Web identifica + CLI ri-testa
- Audit di dump locali -> CLI primario

**Esito B.3**: coerente. Nessuna contraddizione di sostanza. **Nessun finding B.3.**

### B.4 — Opzioni A (self-review) e B (probe-review) entrambe operative

- Opzione A — self-review dell'autore. Definita in `METODO.md:158-164` e in `CLAUDE.md:126-128`. **Esigibilità nel prompt dell'autore (Developer)**: ASSENTE. Il prompt Developer `developer.md:22` cita RM-4 in modo GENERICO ("esegui self-review esplicita o richiedi review formale leggera dell'Orchestrator. Vedi METODO.md per il formato"). Nessuna sezione "Self-review opzione A" nel prompt Developer. Nessun punto della pre-consegna checklist (`developer.md:131-159`) la richiede per output non-CAP. **L'Orchestratore può dire all'autore "fai opzione A" tramite invocazione, ma se l'autore opera in sessione web fuori dal ciclo CAP, non c'è Orchestratore che lo intercetta** (vedi C.1/C.2).
- Opzione B — probe-review formale. Definita in `METODO.md:166-172` e operativa in `reviewer.md:80-173` con 4 check, matrice sede, formato output. OK.

**Esito B.4**: opzione B operativa, opzione A operativa solo come istruzione dell'Orchestratore, non come obbligo dell'autore. Asimmetria pericolosa.

**Finding F-B4**: il prompt Developer non ha una sezione "Self-review esplicita per output non-CAP (RM-4 opzione A)" con formato e checklist vincolanti. Risulta che l'opzione A, dichiarata "preferita per output veloci" in `CLAUDE.md:126`, non è producibile in modo verificabile da Developer senza un'invocazione esplicita dell'Orchestratore che gliela richieda. Per una sessione web che produce un probe ad hoc (come 28/05), né opzione A né opzione B sono attivate.
**Classificazione**: BUG REALE — è esattamente il vuoto operativo che le RM dovrebbero chiudere.

### B.5 — Quando Orchestratore sceglie A vs B vs nessuna review

`CLAUDE.md:134-136`:
> "L'Orchestratore decide A o B in base a complessità e rischio:
> - A se l'output è < 200 righe e tocca un'area circoscritta
> - B se l'output supera 200 righe O introduce un decoder/parser nuovo O modifica un fatto già dichiarato 'verificato' in passato"

Verifica testuale citata. Vedi anche §Check E.3 (clausola "200 righe" — ambiguità per-file vs aggregato).

**Esito B.5**: criterio definito ma con ambiguità (vedi E.3). Nessuna definizione di "area circoscritta". Nessun criterio per "nessuna review" (cioè: quando un output NON rientra in RM-4). Il trigger `CLAUDE.md:118-122` è una lista a 3 voci OR — qualunque output che parsa payload esterno O dichiara fatti verificati O produce M-promemoria -> RM-4. Bene; ma se Orchestratore non gira (output prodotto in sessione web autonoma), tutto questo non si applica. -> Rinvio a §C.1.


---

## Check C — Sufficienza: simulazione dell'errore canonico (banco di prova)

Scenario applicato letteralmente (da `tasks/ACTIVE_TASK.md:99`): sessione web produce `parse_price_extended.py` (decoder ipotetico, 250 righe) + `tasks/HANDOFF_PRICE_EXTENDED.md` (180 righe con "fatti verificati") basandosi su wiki Directa e test su 1 dump giornaliero a 4 valori. Dichiara `verificato schema = A;MIN;MAX;B` senza enumerare `B;MIN;MAX;A`. Salta `grep -rn "UFF|APE|price_extended"`. Commit + push. Nessuna review.

### C.1 — Trigger Orchestratore: rileva che è output RM-4 e richiede A o B?

**Verifica letterale dei prompt**:
- `CLAUDE.md:20-30` "Macchina a stati" definisce 5 condizioni-azione: (i) Planner se ACTIVE_TASK assente o CAP-X chiuso; (ii) Developer se DEV_STATUS vuoto e ACTIVE_TASK pending; (iii) Reviewer se DEV_STATUS=READY_FOR_REVIEW; (iv) controllo supervisore se review CONDITIONAL/FAIL; (v) chiusura sessione se review PASS + indice non aggiornato. **Nessuna delle 5 condizioni include "se l'agente sta per produrre output non-CAP"**. La sezione "Workflow per output non-CAP" (`CLAUDE.md:114-144`) descrive *cosa fare* ma non è agganciata a nessun trigger nella macchina a stati.
- `CLAUDE.md:118` "L'Orchestratore valuta se un output non-CAP rientra in RM-4 quando..." — verbo "valuta" senza definizione di quando esegue la valutazione. Se l'agente che produce l'output è la stessa sessione che agisce come "orchestratore implicito" (caso 28/05), non c'è un secondo agente che esegue la valutazione *ex-ante*.

**Esito C.1**: **FUGA**. Nessuna linea di `.claude/CLAUDE.md` instrada l'Orchestratore a verificare RM-4 prima del commit di un agente che non è entrato nel ciclo Planner->Developer->Reviewer. La sezione `CLAUDE.md:114-144` è un *manuale di riferimento*, non una *macchina a stati* eseguibile.

### C.2 — Meccanismo di blocco pre-commit/pre-push se l'autore salta self-review opzione A

**Verifica**:
- `developer.md:30`: "Output: file in docs/methodology_v2/ + commit + push su origin main." — il commit/push è parte del workflow Developer **prima** della pre-consegna checklist. La pre-consegna (`developer.md:131-159`) gira *dopo*: il punto 6 verifica che il push sia avvenuto, non che debba avvenire dopo la checklist.
- `developer.md:159`: "Solo dopo che tutti e 12 i controlli sono OK, scrivi READY_FOR_REVIEW e fermati." Il segnale di completamento è dopo il push, non il push.
- Per output non-CAP: nessun analogo. Nessuna istruzione "non committare un probe/script/handoff senza prima aver eseguito blocco opzione A".
- `CLAUDE.md:128`: "Se la self-review è assente, NON committare; rilanciare l'agente con prompt mirato" — istruzione all'**Orchestratore**, ma vedi C.1 (Orchestratore non gira su output autonomo della sessione web).

**Esito C.2**: **FUGA**. Nessun meccanismo di blocco pre-commit/pre-push esiste per output non-CAP nei prompt degli agenti. Il blocco è scritto solo in `CLAUDE.md:128` come azione che presuppone un Orchestratore che giri *prima* del commit dell'autore. Nello scenario 28/05 e nello scenario ipotetico PRICE_EXTENDED, l'autore commit+pusha autonomamente.

### C.3 — Check Developer RM-1 (punto 10) intercetta "verificato A;MIN;MAX;B" senza enumerare B;MIN;MAX;A?

**Verifica**:
- `developer.md:153` (punto 10): "per ogni 'Verificato X' nel documento o nel REPORT, c'è enumerazione esplicita delle alternative compatibili coi dati osservati e dell'evidenza che le esclude. Se anche un solo 'Verificato X' è privo di questa enumerazione, va riscritto come 'Verifica parziale' oppure va completato con un test che disambigua."
- **Limite**: il check vive nella "Pre-consegna checklist" che si applica al ciclo CAP-XX (`developer.md:25,30` punti 1-2). Non c'è un analogo per output non-CAP. Se l'autore in sessione web sta producendo `parse_price_extended.py` come *attività spontanea fuori task*, non sta seguendo `developer.md:25` ("Leggi tasks/ACTIVE_TASK.md prima di ogni task"). La pre-consegna non si attiva.
- **Anche se la pre-consegna si attivasse**, il punto 10 non specifica il formato 4-righe (cfr. B.1): l'autore potrebbe scrivere "Schema verificato dai daily, possibili altre permutazioni non testate" e dichiarare il punto 10 OK. È più stretto del prompt 28/05 ma non blinda.

**Esito C.3**: **FUGA PARZIALE**. Il check punto 10 sta nel posto giusto (Developer pre-consegna) ed è azionabile se attivo, ma è attivo solo nel ciclo CAP-XX, mancando per output non-CAP — che è esattamente lo scenario incriminato dal task. Inoltre la mancanza del formato 4-righe (B.1) lascia margine interpretativo.

### C.4 — Check RM-2 grep eseguito prima del commit per output non-CAP?

**Verifica**:
- `developer.md:155` (punto 11): "se il task ha prodotto codice/spec di parsing di sistemi esterni, il REPORT contiene nella sezione 'Decisioni rilevanti' la lista dei decoder/parser già presenti nel repo che sono stati consultati (con path:linea) o l'esplicita dichiarazione che nessuno è stato trovato dopo grep su pattern specifico."
- Il REPORT è `reports/REPORT_CAP_XX.md` (formato CAP-XX). Per output non-CAP non esiste un REPORT analogo previsto. Quindi il check punto 11, formalmente, non si applica al caso del probe ad hoc.
- `reviewer.md:116` (probe-review check 2): "Esegui grep diretto. Se trovi qualcosa che il Developer non ha citato, è BUG REALE." Azionabile *se* il Reviewer è invocato. Ma l'invocazione dipende da C.1 (Orchestratore che gira). Punto di fuga.

**Esito C.4**: **FUGA**. Il check grep esiste in due posti (`developer.md:155` per ciclo CAP-XX, `reviewer.md:116` per probe-review se invocato) ma nessuno dei due si attiva nel caso 28/05 / scenario ipotetico PRICE_EXTENDED, dove l'autore opera autonomamente fuori da task pianificato.

### C.5 — Recupero post-commit: la sessione successiva sospetta degli handoff non revisionati?

**Verifica**:
- `CLAUDE.md:112` "L'Orchestratore della NUOVA sessione, come primo atto, verifica autoconsistenza delle 7 condizioni della sessione precedente" — verifica chiusura sessione CAP, non sospetto verso handoff non revisionati.
- `CLAUDE.md:46-48` (check post-Developer) verifica gap di consegna del Developer del ciclo corrente, non di sessioni precedenti.
- Nessuna citazione di `MEMORY.md` in `CLAUDE.md`. Nessun obbligo di rileggere handoff committati senza review per riclassificarli come "RM-4 fallita".
- `reviewer.md`: nessuna modalità "audit retroattivo di handoff non revisionati".

**Esito C.5**: **FUGA**. Nessun meccanismo di recupero post-commit. Una volta che un output non-CAP è in `main` come fatto autoritativo, la sessione successiva lo eredita come premessa (è esattamente quello che è successo: il CLI del 29/05 ha letto `tasks/HANDOFF_PROBE_DAPI_20260528.md` come fatti verificati senza riauditarli).

### Sintesi Check C

| Punto | Esito | Punto di fuga |
|---|---|---|
| C.1 | FUGA | Macchina a stati `CLAUDE.md:20-30` non triggera RM-4 ex-ante |
| C.2 | FUGA | Nessun blocco pre-commit/pre-push per output non-CAP nei prompt degli agenti autori |
| C.3 | FUGA PARZIALE | Check punto 10 azionabile solo nel ciclo CAP-XX + manca formato 4-righe (B.1) |
| C.4 | FUGA | Check grep si attiva solo via ciclo CAP-XX o via Reviewer invocato (dipende da C.1) |
| C.5 | FUGA | Nessun meccanismo retroattivo per handoff non revisionati |

**4 fughe + 1 fuga parziale** su 5 punti. AC-S del task richiede che almeno un PASS si conceda solo se Check C dimostra l'intercezione: qui non si dimostra. -> **FAIL**.


---

## Check D — Stato divisione Web/CLI in `reviewer.md`

**Verifica letterale**:
- `reviewer.md:84-99`: sezione "Sede dell'audit — Web vs CLI locale". Distinzione esplicita Web (`reviewer.md:88-92`) vs CLI (`reviewer.md:94-98`). Definita per capacità: cosa puoi/non puoi fare.
- `reviewer.md:102-108`: tabella di assegnazione.
- `reviewer.md:122-126`: check aggiuntivi specifici per sede ("Se sei Web reviewer" / "Se sei CLI reviewer"). Web esplicita "non può rieseguire il test contro DAPI" e "lascia un punto aperto 'Empirico-CLI da verificare'".
- `reviewer.md:163-164`: cosa Web NON dichiara ("verificato empiricamente niente che richieda accesso a DAPI o filesystem locale"); cosa CLI NON fa (probe massivi solo per zelo).
- `reviewer.md:167-173`: handoff cross-ambiente Web -> CLI -> Web tramite file `reviews/PROBE_REVIEW_<nome>_web.md` e `_cli.md`.

**Esito D**: la distinzione c'è ed è esplicita; un Reviewer che legge il prompt sa in quale sede è e cosa può/non può fare. La regola di handoff (Web non chiude asserzioni empiriche, CLI le conferma) è scritta esplicitamente in `reviewer.md:124` ("Lascia un punto aperto 'Empirico-CLI da verificare' nel verdetto").

**Nessun finding D** di gravità sostanziale.

Osservazione minore (non finding): la sezione D è scritta solo in `reviewer.md`. `CLAUDE.md:140-142` riprende solo la matrice di assegnazione, non i divieti per sede. Non bloccante: il Reviewer è l'agente che opera sotto sede, l'Orchestratore solo lo invoca.

---

## Check E — Onestà delle regole stesse: clausole vaghe/discrezionali in `METODO.md`

### E.1 — `METODO.md:42` "Non c'è esenzione 'perché è una cosa piccola'"

**Esito**: chiaro, vincolante. Non vago.

### E.2 — `METODO.md:60` "Se trovi un decoder esistente, non assumere mai un formato divergente senza prima provare empiricamente che il decoder esistente è sbagliato"

**Esito**: chiaro. "Provare empiricamente" è il livello 1 di RM-3 — meccanico.

### E.3 — `CLAUDE.md:134-136` soglia "200 righe" (ambiguità per-file vs aggregato — **flag esplicito del task**)

`CLAUDE.md:135`: "A se l'output è < 200 righe e tocca un'area circoscritta".
`CLAUDE.md:136`: "B se l'output supera 200 righe O introduce un decoder/parser nuovo O modifica un fatto già dichiarato 'verificato' in passato".

**Verifica**: il commit incriminato `7bb2955` aveva 588 righe in `scripts/probe_dapi.py` + 207 in `tasks/HANDOFF_PROBE_DAPI_20260528.md` = 795 righe aggregate. Per-file, entrambi superano 200. Non c'è quindi punto di fuga per il commit 28/05 *retrospettivamente* (l'opzione B sarebbe stata richiesta in entrambi i casi).

**MA**: la formulazione "l'output" è singolare ambigua. Se un autore distribuisce un cambiamento in 3 file da 199 righe ciascuno, ognuno < 200 -> si potrebbe interpretare come opzione A. Inoltre, la clausola B in OR contiene già "introduce un decoder/parser nuovo": qualunque parser triggera B, indipendentemente dalla soglia. Quindi la soglia 200 è ridondante per il caso decoder ma resta ambigua per documenti (handoff/probe report) che non sono decoder.

**Inoltre**: il criterio della soglia stessa è discrezionale (perché 200 e non 100 o 500?). Senza giustificazione, è una soglia arbitraria che dà l'illusione di meccanicità.

**Finding F-E3**: la clausola `CLAUDE.md:135` "< 200 righe" non specifica se per-file o aggregata; e in OR con `CLAUDE.md:136` ("decoder/parser nuovo" o "modifica fatto verificato"), il primo criterio della soglia è quasi mai determinante (i decoder triggerano B per il secondo OR). Per documenti (handoff puro, senza decoder), la soglia 200 può creare ambiguità. **Classificazione**: MIGLIORA PROCESSO (impatto basso retroattivamente sul caso 28/05; impatto medio prospettivamente come potenziale punto di fuga per handoff "piccoli" che dichiarano fatti verificati).

### E.4 — `METODO.md:147-152` "Output soggetti a RM-4 (lista non esaustiva)"

`tasks/METODO.md:147` recita "lista non esaustiva". L'enumerazione include: script di parsing/decoder, documenti di handoff, probe/spike empirici, scoperte tecniche dichiarate come M-promemoria. Una "lista non esaustiva" lascia discrezionalità all'Orchestratore di non includere un output borderline.

**Esito E.4**: discrezionalità limitata. La lista include i 4 tipi reali del caso 28/05. Ma "non esaustiva" è una clausola da osservare: per evitare punti di fuga futuri, sarebbe da convertire in "esaustiva, con criterio di estensione esplicito". **Classificazione**: MIGLIORA PROCESSO, non bloccante.

### E.5 — `CLAUDE.md:118-122` trigger "uno qualunque di questi è vero"

Lista OR a 3 voci: parsa payload esterno OR dichiara fatti verificati OR produce M-promemoria CARRYOVER.

**Esito**: meccanica nei criteri. Ma vedi C.1 — il vero buco non è nel criterio, è nell'inesistenza del trigger sulla macchina a stati.

### E.6 — `CLAUDE.md:131` "Invocare il reviewer in modalità 'probe-review'"

Operativa. Cita la sezione di `reviewer.md`. OK.

---

## Grep RM-* su perimetro (citazione esplicita per AC-7)

Output `grep -rn "RM-1\|RM-2\|RM-3\|RM-4" .claude/`:
- 9+ righe in `.claude/CLAUDE.md` (linee 7, 11, 114, 116, 118, 124, 127, 131, 138, 140)
- 9 righe in `.claude/agents/planner.md` (linee 15, 17, 18, 19, 20, 138, 139, 140, 141)
- 8 righe in `.claude/agents/developer.md` (linee 14, 16, 18, 20, 22, 153, 155, 157)
- 19+ righe in `.claude/agents/reviewer.md` (linee 15, 17, 19, 21, 23, 56, 57, 58, 80, 105, 107, 114, 116, 118, 124, 137, 140, 143, 162)

Output `grep -rn "RM-1\|RM-2\|RM-3\|RM-4" tasks/`:
- `tasks/METODO.md` linee 11, 46, 97, 139, 147, 162, 164, 169, 170, 171, 187, 194, 198, 210, 218, 219
- `tasks/ACTIVE_TASK.md` linee 1, 14, 30..33, 38..41, 56, 60, 72, 80, 88..91, 103..106, 121..123, 137, 145, 146, 147, 154, 182
- `tasks/STATO_CORRENTE.md` linee 5, 129

Nessun aggancio "fuori posto" trovato (es. occorrenze nascoste in `reports/` o `MEMORY.md` che il Reviewer avrebbe potuto saltare). **AC-7 soddisfatto**: il grep è stato eseguito e citato.


---

## Classificazione per il supervisore (AC-5)

| # | Problema | File:linea | Classificazione | Patch suggerita concreta |
|---|----------|------------|-----------------|--------------------------|
| 1 | **C.1+C.2 combinati**: nessun trigger nella "Macchina a stati" Orchestratore che attivi il workflow RM-4 *ex-ante* prima del commit di un agente che sta producendo output non-CAP (probe, script, handoff) fuori dal ciclo Planner->Developer->Reviewer. La sezione "Workflow per output non-CAP" (`CLAUDE.md:114-144`) descrive cosa fare ma non è agganciata a una condizione della macchina a stati. | `.claude/CLAUDE.md:20-30` e `:114-144` | **BUG REALE** | Aggiungere riga alla "Macchina a stati" `CLAUDE.md:24-30`: "Se la sessione corrente sta per produrre/committare output non-CAP che soddisfa uno dei criteri `CLAUDE.md:118-122`, prima del commit esegui il workflow RM-4 (`CLAUDE.md:114-144`)". In `CLAUDE.md:152-162` "Cosa l'orchestratore NON fa mai" aggiungere "Non lascia passare un commit non-CAP senza opzione A o B; se l'autore opera in sessione web autonoma, l'autore stesso applica opzione A in modo blindato dal proprio prompt". |
| 2 | **B.4 / F-A2**: il prompt Developer non ha una checklist analoga ai punti 10/11/12 per output non-CAP soggetti a RM-4. L'opzione A "self-review esplicita" è descritta solo in `CLAUDE.md:126-128` come istruzione all'Orchestratore, non come obbligo blindato dell'autore. | `.claude/agents/developer.md:22` e `:131-159` | **BUG REALE** | Aggiungere a `developer.md` una nuova sezione "Pre-consegna per output non-CAP (RM-4 opzione A)" con checklist analoga: (1) blocco "Self-review RM-1..RM-3" in fondo al documento o nel commit message esteso; (2) lista asserzioni "verificato" + alternative escluse con formato 4-righe; (3) grep eseguito documentato; (4) fonti etichettate; (5) `READY_FOR_PROBE_REVIEW` in `DEV_STATUS.md` se opzione B richiesta. Aggiungere punto 13 alla pre-consegna `developer.md:131-159`. |
| 3 | **C.3 + B.1**: il check pre-consegna punto 10 (`developer.md:153`) non impone il formato 4-righe `VERIFICA / PROVE / ALTERNATIVE ESCLUSE / ALTERNATIVE NON ESCLUSE` di `METODO.md:28-33`. Senza formato fisso, una self-review può scrivere "alternative considerate" in prosa e dichiararsi compliant senza essere blindata. | `.claude/agents/developer.md:153` (e .agg. `reviewer.md:17,56,114`) | **MIGLIORA PROCESSO** | Estendere `developer.md:153` (punto 10): "con formato esatto VERIFICA/PROVE/ALTERNATIVE ESCLUSE/ALTERNATIVE NON ESCLUSE (cfr. METODO.md:28-33). Asserzioni in prosa libera senza blocco formattato sono respinte come 'non in formato'". Estendere `reviewer.md:17` con il criterio di rigetto del formato. |
| 4 | **C.4**: il check RM-2 (grep) è vincolato al REPORT_CAP_XX.md (`developer.md:155`). Per output non-CAP non c'è dove l'autore documenta il grep. | `.claude/agents/developer.md:155` | **BUG REALE** (sotto-componente del #2) | Nella nuova sezione "Pre-consegna RM-4 opzione A" del Developer, replicare il check punto 11 sui REPORT/blocchi non-CAP: lista decoder consultati nel repo con path:linea o dichiarazione "nessuno trovato dopo grep su <pattern>", inclusa nel commit message o nel documento stesso. |
| 5 | **C.5**: nessun meccanismo retroattivo per handoff non revisionati. L'Orchestratore della sessione successiva non rilegge documenti committati nelle sessioni precedenti per riclassificarli RM-4 e segnalarne l'assenza di self-review. | `.claude/CLAUDE.md:112` | **MIGLIORA PROCESSO** | Aggiungere al primo atto dell'Orchestratore della nuova sessione (`CLAUDE.md:112`): "Verifica anche se la sessione precedente ha committato output non-CAP. Per ognuno, controlla che esista un blocco self-review (opzione A) o una probe-review committata (opzione B). Se manca, apri un task `AUDIT-RECUPERO-<nome>` come secondo atto prima di procedere col normale flusso." |
| 6 | **F-A1**: Orchestrator ha RM-1/RM-2/RM-3 solo come elenco enunciativo (`CLAUDE.md:7`). Buchi di gatekeeping su commit non-CAP. | `.claude/CLAUDE.md:7-12` | **MIGLIORA PROCESSO** | Aggiungere a `CLAUDE.md:9-12` la lista di responsabilità: "Applicare RM-1 ai commit non-CAP: rifiutare PR/commit che dichiarano 'verificato X' senza blocco 4-righe. Applicare RM-2: rifiutare commit di parser senza grep documentato. Applicare RM-3: rifiutare commit con conclusioni wiki-only." (Dipende da #1.) |
| 7 | **E.3**: soglia "200 righe" ambigua (per-file vs aggregata, decoder ridondante per OR successivo, niente giustificazione del valore). Possibile punto di fuga per documenti puri (handoff senza decoder). | `.claude/CLAUDE.md:135-136` | **MIGLIORA PROCESSO** | Riscrivere `CLAUDE.md:134-136`: "B è obbligatoria se: (a) introduce un decoder/parser di sistema esterno, OR (b) modifica un fatto già dichiarato 'verificato' in CAP precedenti, OR (c) il diff aggregato del commit supera N righe (con N=200 come valore di lavoro). A è ammessa solo se nessuno di a/b/c è vero." Eliminare il criterio "area circoscritta" non definito. |
| 8 | **B.1**: formato 4-righe `VERIFICA / PROVE / ALTERNATIVE ESCLUSE / ALTERNATIVE NON ESCLUSE` di `METODO.md:28-33` non è esigibile da nessun prompt. | `.claude/agents/developer.md:153` + `reviewer.md:17,56,114` | **MIGLIORA PROCESSO** (componente di #3) | Vedi patch #3. |
| 9 | **E.4**: `METODO.md:147` "lista non esaustiva" lascia discrezionalità sull'inclusione di output borderline. | `tasks/METODO.md:147` | **NEUTRO** | Borderline: la lista copre i 4 tipi del caso 28/05. Decisione supervisore se vale la pena patchare. |
| 10 | Osservazione: `CLAUDE.md` non ripropone i divieti per sede del Reviewer (matrice presente solo in `reviewer.md`). | `.claude/CLAUDE.md:140-142` | **NEUTRO** | Non bloccante. |

**Conteggio finding**:
- BUG REALE: **3** (#1, #2, #4)
- MIGLIORA PROCESSO: **5** (#3, #5, #6, #7, #8)
- NEUTRO: **2** (#9, #10)
- RISCHIO PEGGIORAMENTO: 0


---

## Auto-applicazione RM-1 (AC-6)

Asserzioni "verificato" usate nel report e loro disambiguazione:

- **"Verificato che RM-2 è agganciato in `developer.md:18`"** — alternative considerate: (a) aggancio AZIONABILE come affermato (con comando `grep -rn` esplicito + obbligo REPORT); (b) aggancio GENERICO che mi è apparso AZIONABILE solo a una lettura superficiale; (c) aggancio assente che ho confuso con un'altra riga. Esclusione: ho letto `developer.md:18` testualmente sopra ("prima di scrivere parser/decoder per qualunque sistema esterno [...] esegui `grep -rn '<KEYWORDS_DEL_DOMINIO>' --include='*.py' --include='*.md'` nel repo"). Il comando concreto + l'obbligo di documentare nel REPORT sezione "Decisioni rilevanti" sono comportamenti osservabili. Alternative (b) e (c) **escluse** dal testo letterale citato. Verifica completa.

- **"Verificato che la 'Macchina a stati' `CLAUDE.md:20-30` non contiene trigger RM-4"** — alternative considerate: (a) il trigger c'è ma è formulato in modo non immediato; (b) il trigger è altrove in `CLAUDE.md` ma collegato logicamente alla macchina a stati. Esclusione: lettura testuale delle 5 condizioni in `CLAUDE.md:24-30` — nessuna menziona output non-CAP. Lettura della sezione `CLAUDE.md:114-144` — non è agganciata via "vai a §Workflow non-CAP se..." da nessuna riga della macchina a stati. Grep `non-CAP|probe|handoff|script` su `CLAUDE.md` (eseguito) -> nessuna occorrenza dentro `CLAUDE.md:20-30`. Verifica completa.

- **"Verificato che nessuna pre-consegna RM-4 esiste per Developer su output non-CAP"** — alternative considerate: (a) c'è una sezione che non ho letto; (b) il punto 9 `developer.md:151` ("Iterazione N>1") copre implicitamente anche output non-CAP. Esclusione: lettura completa di `developer.md:131-159` (12 punti). Nessun punto cita output non-CAP esplicitamente. Il punto 9 è formulato per "Iterazione di rework" su finding di Review, non per produzione iniziale di output non-CAP. **Verifica parziale**: ammetto che potrebbe esistere una *interpretazione* della pre-consegna che la estende anche a output non-CAP, ma il testo letterale non la rende esigibile. Mantengo il finding come BUG REALE perché il *testo* dei prompt è ciò che definisce il comportamento osservabile degli agenti.

- **"Verificato che D (divisione Web/CLI) è esplicita e azionabile"** — alternative considerate: (a) c'è azionabile ma la regola di handoff "Web non chiude empirico" è solo enunciata, non blindata; (b) un Reviewer potrebbe ancora dichiarare "verificato empiricamente" in sede Web. Esclusione: lettura di `reviewer.md:163` ("Web reviewer: non dichiari 'verificato empiricamente' niente che richieda accesso a DAPI o filesystem locale — segnali come 'Empirico-CLI da verificare'"). Riga divieto esplicita. Verifica completa.

- **"Verificato che la soglia 200 righe è ambigua"** — alternative considerate: (a) "l'output" è inequivocabilmente per-file in italiano tecnico; (b) il criterio in OR rende la soglia di fatto irrilevante. Esclusione (a): "l'output" è singolare ambigua nel contesto di un commit che tocca N file. Esclusione (b) parziale: il secondo OR "decoder/parser nuovo" assorbe la soglia per il caso decoder, ma non per handoff puro. Verifica con caveat (vedi F-E3): la soglia è ambigua per il sottoscenario "handoff senza decoder nuovo".

---

## Auto-applicazione RM-3 (AC-8)

Ogni riferimento ai prompt in questo report è citato con `file:linea`, non parafrasato. Citazioni testuali rilevanti racchiuse fra virgolette quando direttamente quotate. Nessuna conclusione si appoggia a "ricordo del prompt" senza file:linea verificabile dal supervisore.

---

## Osservazioni minori (non finding)

- Il prompt Developer `developer.md:170` cita "pre-consegna checklist (9 controlli)" mentre `developer.md:131-159` ne elenca **12** (i punti 10/11/12 di RM-1/2/3 sono stati aggiunti dopo). Il numero "9" è obsoleto in più punti (`:170, :179, :199`). **Non impatta il comportamento del GA o l'intercezione dell'errore canonico**. Nessuna azione richiesta dal supervisore.
- `CLAUDE.md` non cita `MEMORY.md` come fonte obbligatoria all'apertura sessione, anche se MEMORY contiene la nota "Stop dopo PASS" che riguarda l'Orchestratore. Non è un finding di RM-4 ma vale per il rigore della catena di stato.
- Non propongo nuove RM-5+: AC esplicito del task (out-of-scope `ACTIVE_TASK.md:134`). Le mie patch suggerite sono tutte chiusure di buchi dentro RM-1..RM-4 esistenti.

---

## Riassunto del verdetto motivato (ancorato a file:linea)

Il PASS non si concede sull'esistenza degli agganci. AC-S richiede l'intercezione dimostrata dell'errore canonico tramite il workflow simulato. La simulazione mostra:

1. C.1 fuga: macchina a stati `CLAUDE.md:20-30` non triggera RM-4 ex-ante.
2. C.2 fuga: nessun blocco pre-commit/pre-push nei prompt degli agenti autori per output non-CAP.
3. C.3 fuga parziale: check `developer.md:153` esigibile solo in ciclo CAP-XX + manca formato fisso 4-righe.
4. C.4 fuga: check grep `developer.md:155` vincolato a REPORT_CAP_XX, non esiste analogo per output non-CAP.
5. C.5 fuga: nessun meccanismo retroattivo per handoff non revisionati.

Lo scenario PRICE_EXTENDED (C.1..C.5 del task card) **non viene fermato** dal workflow attuale: l'autore può commitare il decoder + handoff con schema sbagliato esattamente come 28/05. Le RM-1..RM-4 sono **definite** correttamente in `METODO.md`, ma **non sono integralmente agganciate** all'attore (Developer/Orchestrator) nel punto operativo in cui l'errore può essere bloccato.

**Verdetto finale: FAIL.**

I 3 BUG REALI (#1, #2, #4) devono essere chiusi. Le 5 patch MIGLIORA PROCESSO sono raccomandate ma decisione supervisore. Le 2 NEUTRO non vanno a Developer salvo decisione esplicita.

---
