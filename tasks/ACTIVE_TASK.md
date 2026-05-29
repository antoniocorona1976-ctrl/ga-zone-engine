# TASK ATTIVO: AUDIT-FONDAMENTA-01 — Regole metodologiche RM-1..RM-4 e loro aggancio nei prompt agenti

**Assegnato da**: Planner
**Output atteso primario**: `reviews/REVIEW_FONDAMENTA_01_web.md` (verdetto PASS/CONDITIONAL/FAIL del Reviewer su 5 file di prompt + `METODO.md`)
**Output atteso secondario (solo se CONDITIONAL/FAIL approvato dal supervisore)**: modifiche mirate ai prompt agenti + `METODO.md`, prodotte dal Developer
**Stato**: IN ATTESA
**Workflow**: **Review-First** (le fondamenta esistono già su `origin/main`, vanno auditate, non sviluppate da zero)
**Natura del task**: NON è un capitolo metodologico CAP-XX. È un audit di processo. Non si scrive `docs/methodology_v2/CAP_XX_*.md` né `reports/REPORT_CAP_XX.md`.

---

## Obiettivo

Verificare **in modo indipendente** che le 4 regole metodologiche permanenti `RM-1`, `RM-2`, `RM-3`, `RM-4` definite in `tasks/METODO.md` (commit `7bb2955`/`de2938d`/`916278a` del 2026-05-28, sessione web) siano:

1. **agganciate** in ogni prompt agente che le deve applicare (Orchestrator in `CLAUDE.md`, Planner, Developer, Reviewer in `.claude/agents/*.md`), con un riferimento concreto e azionabile — non un generico "leggi `METODO.md`", ma istruzioni operative che producano comportamento osservabile;
2. **coerenti** fra loro (testo di `METODO.md` vs propagazioni nei prompt: nessuna contraddizione, nessuna omissione su clausole vincolanti);
3. **sufficienti** a impedire la ricomparsa dell'errore originale che le ha motivate, cioè il pattern: asserzione "verificato X" senza enumerazione di alternative compatibili escluse, propagata in output non-CAP (script di parsing + handoff fra sessioni) che non sono mai passati da un Reviewer formale e che diventano premessa autoritativa per sessioni successive.

Il capitolo NON risponde a: se i CAP-DATA-01/02/03 esistenti hanno errori discendenti dalla propagazione dello schema CANDLE errato (audit dei capitoli — fuori scope, sessioni separate); se nuove regole RM-5..RM-N vadano introdotte (proposte di nuove RM possono essere segnalate come "raccomandazioni" dal Reviewer, ma la decisione di aggiungerle è del supervisore in una sessione dedicata).

Il task si fa adesso perché le RM sono state introdotte e auto-valutate "sufficienti" dalla stessa sessione che ha causato l'incidente CANDLE: c'è un evidente conflitto di interesse epistemico. Prima di rilanciare il probe CAP-DATA-03 e le sessioni di rework che dipenderanno da queste regole, è necessario che un Reviewer **indipendente** verifichi che le fondamenta reggono. Se i prompt hanno buchi, ogni audit successivo eredita quei buchi.

---

## Eredità obbligatoria

### Da `tasks/METODO.md` (testo vincolante, NON riaprire)

1. **RM-1 — Verifica vs assunzione compatibile coi dati** (METODO.md §RM-1): asserzioni "verificato X" senza enumerazione esplicita delle alternative compatibili coi dati osservati sono **vietate**. Formato obbligatorio `VERIFICA / PROVE / ALTERNATIVE ESCLUSE / ALTERNATIVE NON ESCLUSE`.
2. **RM-2 — Grep nel repo prima di assumere un formato esterno** (METODO.md §RM-2): obbligo di passata `grep -rn` su keywords del dominio prima di scrivere parser/decoder; documentazione nei commit message dei decoder esistenti citati o dell'esplicita dichiarazione "nessuno trovato".
3. **RM-3 — Documentazione ufficiale dei sistemi esterni non è fonte di verità** (METODO.md §RM-3): ordine di priorità fonti `(1) prove empiriche dirette > (2) codice di produzione esistente > (3) documenti interni committati > (4) wiki/docs esterni`. Conclusione che si appoggia solo a livello 4 senza supporto dai livelli 1–3 è **inammissibile**. Etichette obbligatorie `[WIKI-HINT]`, `[CODICE-EXISTENTE r.NNN]`, `[PROVA-EMPIRICA <data>]`.
4. **RM-4 — Output tecnici determinanti vanno revisionati prima del commit** (METODO.md §RM-4): output non-CAP (script di parsing/decoder, handoff fra sessioni, probe/spike empirici, scoperte tecniche destinate a CARRYOVER) non possono essere committati senza review esplicita. Opzioni A (self-review esplicita dell'autore con blocco formalizzato) o B (probe-review formale del Reviewer, 4 check). Matrice di assegnazione Web vs CLI locale in `METODO.md §RM-4` sezione "Sede della review".

### Caso reale che ha motivato le regole (paradigma di test, NON riaprire)

Commit `7bb2955` sessione web 2026-05-28. La sessione ha:
- dichiarato "verificato schema CANDLE = `O;L;H;C`" da soli 4 valori daily (L,H verificati in pos 2,3; O,C indistinguibili sui valori non-estremi → due alternative compatibili `{O;L;H;C, C;L;H;O}` mai disambiguate); RM-1 violata;
- **non eseguito** `grep -rn "UFF\|APE\|parse_directa_candle"` nel repo, dove `scripts/export_directa_history_parametric.py:477` conteneva il decoder di produzione `# UFF, MIN, MAX, APE => close, low, high, open` (schema reale `C;L;H;O`); RM-2 violata;
- usato wiki Directa (`O;H;L;C`) come fonte autorevole emendabile invece che come hint da verificare; RM-3 violata;
- prodotto 588 righe di `scripts/probe_dapi.py` + 207 righe di `tasks/HANDOFF_PROBE_DAPI_20260528.md` con 6 "fatti verificati" e 2 PR, **senza alcuna review**; RM-4 violata.

Il pattern è quindi: **dichiarazione di verifica non rigorosa** → **omissione del grep di codice esistente** → **fonte esterna trattata come autorevole** → **propagazione in output non-CAP mai revisionato** → **errore entra in `origin/main` come fact-of-truth** e contagia la sessione successiva. Questo è il caso d'errore canonico che le RM devono intercettare e che il Reviewer userà come banco di prova nel check di sufficienza (vedi acceptance criterion AC-S).

### Da CLAUDE.md sessione corrente

5. Workflow Review-First: non c'è Developer in v1. L'Orchestratore invoca direttamente il Reviewer in modalità adattata (audit di prompt + metodologia, NON CAP-review piena, NON probe-review classica). Il verdetto del Reviewer determina la presenza o assenza di una fase Developer di rework.
6. Sede primaria del Reviewer: **WEB**. Tutto il perimetro è composto da file versionati nel repo (`tasks/METODO.md`, `.claude/CLAUDE.md`, `.claude/agents/*.md`) e da grep di codice committato. Nessun test contro DAPI è richiesto.
7. Push policy MEMORY: il Reviewer pubblica su `origin/main` il file di review committato. L'eventuale Developer di rework pusha su `origin/main` le modifiche ai prompt.
8. Modifiche ai prompt non sono autorizzate senza approvazione esplicita del supervisore al punto di controllo CONDITIONAL/FAIL.

---

## Perimetro — 5 file (le fondamenta del sistema)

Il Reviewer auditta **esclusivamente** questi 5 file, citando posizioni puntuali (file:linea). Nessun altro file del repo entra nel perimetro normativo (la sua lettura è ammessa solo come supporto evidenziale, es. grep su `scripts/` per validare RM-2).

| ID | Path assoluto | Ruolo |
|----|---------------|-------|
| P1 | `tasks/METODO.md` | Testo normativo delle 4 regole RM-1..RM-4 (origine). |
| P2 | `.claude/CLAUDE.md` | Prompt Orchestrator. |
| P3 | `.claude/agents/planner.md` | Prompt Planner. |
| P4 | `.claude/agents/developer.md` | Prompt Developer. |
| P5 | `.claude/agents/reviewer.md` | Prompt Reviewer. |

---

## Lavoro atteso dal Reviewer (audit indipendente)

Il Reviewer produce **un singolo file** `reviews/REVIEW_FONDAMENTA_01_web.md` con verdetto PASS / CONDITIONAL / FAIL e classificazione dei finding per il supervisore (BUG REALE / MIGLIORA PROCESSO / NEUTRO / RISCHIO PEGGIORAMENTO — sostituire "PERFORMANCE" con "PROCESSO" perché qui non c'è GA, c'è metodologia di processo).

Per ciascuna RM (RM-1, RM-2, RM-3, RM-4), il Reviewer esegue **3 check separati** e li scrive nel report con esito puntuale (file:linea per ogni aggancio trovato o assenza dichiarata).

### Check A — Aggancio (per ogni RM × ogni prompt P2/P3/P4/P5)

Per ognuna delle 4 RM, e per ognuno dei 4 prompt agente (Orchestrator, Planner, Developer, Reviewer), il Reviewer determina:

- **A.1 Presenza dell'aggancio**: il prompt cita esplicitamente la RM-N? Sì/No, con file:linea.
- **A.2 Azionabilità dell'aggancio**: la citazione è un'istruzione operativa concreta (es. "esegui `grep -rn ...` prima di scrivere parser") oppure un generico "leggi METODO.md" che non produce comportamento osservabile? Classificare come **AZIONABILE** / **GENERICO** / **ASSENTE**.
- **A.3 Pertinenza dell'aggancio per il ruolo**: la RM-N è effettivamente di competenza di quel ruolo? Es. RM-2 (grep nel repo prima di assumere format esterno) ha senso pieno per Developer e Reviewer, ha senso indiretto per Planner (deve segnalarlo nei task), può non avere senso operativo per Orchestrator (che non scrive parser). Il check verifica che l'aggancio esista dove necessario e che la sua assenza dove non necessario sia coerente (non un buco).

Output atteso: una **matrice 4 RM × 4 ruoli = 16 celle**, ognuna con esito A.1/A.2/A.3 e cita-linea. Le celle con AZIONABILE+pertinente sono OK; le celle GENERICO o ASSENTE dove la RM è pertinente sono finding (con classificazione).

### Check B — Coerenza fra `METODO.md` e i prompt

Il Reviewer verifica che la propagazione delle RM nei prompt **non contraddica** il testo di `METODO.md` e **non ometta clausole vincolanti**. In particolare:

- **B.1**: il formato obbligatorio `VERIFICA / PROVE / ALTERNATIVE ESCLUSE / ALTERNATIVE NON ESCLUSE` di RM-1 è ripreso operativamente in almeno uno dei prompt come obbligo di output (es. nella pre-consegna checklist Developer, nei check Reviewer)? Se nessun prompt lo rende esigibile, il formato resta enunciato in `METODO.md` ma non producibile/verificabile in pratica → finding.
- **B.2**: l'ordine di priorità delle fonti di RM-3 (livelli 1>2>3>4) è ripreso esplicitamente in almeno un prompt come criterio di rigetto di conclusioni "wiki-only"? Se nessun prompt formalizza l'inammissibilità del livello-4-solo, idem → finding.
- **B.3**: la matrice di assegnazione Web vs CLI di RM-4 è ripresa coerentemente in `CLAUDE.md` e in `reviewer.md`? Differenze rilevate → finding.
- **B.4**: le opzioni A (self-review) e B (probe-review) di RM-4 sono entrambe operative? Cioè: il prompt Developer prevede esplicitamente la self-review formalizzata opzione A per output non-CAP? Il prompt Reviewer prevede la probe-review opzione B con 4 check? L'Orchestrator sa quando scegliere A e quando B? Punti grigi → finding.

### Check C — Sufficienza (test di simulazione sull'errore canonico)

Il Reviewer **simula** il pattern d'errore canonico (descritto nell'eredità) contro il workflow definito dai prompt attuali, e traccia il percorso ipotetico per determinare se l'errore sarebbe **intercettato** e da quale checkpoint, oppure se ci sono **punti di fuga**.

Scenario di simulazione (vincolante, da eseguire **letteralmente** seguendo gli attuali prompt riga per riga):

> Una sessione web futura riceve dall'Orchestratore l'istruzione di produrre uno script di parsing di un nuovo payload DAPI mai osservato (es. PRICE_EXTENDED, ipotetico) e un handoff con "fatti verificati" da citare in un futuro CAP-DATA-04. La sessione legge `METODO.md`, esegue un test su un singolo dump giornaliero che mostra 4 valori dove 2 sono distinguibili (max e min) e 2 no, e dichiara "verificato schema PRICE_EXTENDED = `A;MIN;MAX;B`" basandosi sull'analogia col wiki Directa che dice `A;MAX;MIN;B`. Non esegue `grep -rn` nel repo. Commit + push + handoff scritto. Nessuna review esplicita richiesta perché "è un probe".

Il Reviewer traccia, citando file:linea dei prompt attuali:

- **C.1**: a quale punto del workflow l'Orchestrator avrebbe **dovuto** rilevare che si trattava di output RM-4 e richiedere opzione A o B? Quale linea di `CLAUDE.md` lo impone? Se è solo enunciato senza enforcement, è una fuga.
- **C.2**: nello scenario, se la sessione web salta la self-review opzione A (perché "è un probe veloce"), esiste un meccanismo nel prompt Orchestrator che **blocca** il commit/push prima che entri in `main`? Se no, è una fuga.
- **C.3**: se la sessione web esegue la self-review ma scrive "verificato `A;MIN;MAX;B`" senza enumerare l'alternativa `B;MIN;MAX;A`, esiste un check nel prompt dell'agente che produce l'output (es. checklist Developer punto 10 "RM-1 — dichiarazioni di verifica con alternative escluse") che intercetta? Sì/No, file:linea.
- **C.4**: se la sessione web non esegue il grep RM-2, c'è un punto del workflow attuale che lo rileva prima del commit? Sì/No, file:linea. (Nota: il check Developer punto 11 esiste — il Reviewer verifica se è esteso anche a output non-CAP o solo a CAP-XX.)
- **C.5**: se l'output entra comunque in `main` senza review, esiste un meccanismo di **recupero post-commit** (es. l'Orchestratore della sessione successiva è obbligato a rileggere `MEMORY.md` e a sospettare degli handoff non revisionati)? Sì/No, file:linea.

Per ogni punto C.1..C.5 con esito "no" o "fuga", il Reviewer produce un finding classificato.

---

## Acceptance criteria — tutti devono essere soddisfatti per PASS in Review

- [ ] **AC-1**: il file `reviews/REVIEW_FONDAMENTA_01_web.md` esiste, è committato e pushato su `origin/main`, e contiene un verdetto esplicito PASS / CONDITIONAL / FAIL.
- [ ] **AC-2**: contiene la **matrice 4 RM × 4 ruoli** del Check A, con ogni cella popolata (16 celle), e ogni cella ha citazione file:linea quando l'aggancio è presente, oppure dichiarazione esplicita "ASSENTE" quando manca.
- [ ] **AC-3**: contiene gli esiti dei 4 sotto-check di Check B (B.1, B.2, B.3, B.4), ciascuno con citazione testuale di `METODO.md` e dei prompt confrontati.
- [ ] **AC-4**: contiene la **traccia di simulazione** Check C con i 5 punti C.1..C.5 popolati, ognuno con file:linea del prompt che intercetta (o dichiarazione "fuga rilevata, nessun prompt intercetta").
- [ ] **AC-S — test di sufficienza**: il verdetto finale si basa esplicitamente sull'esito di Check C. Se anche un solo punto C.1..C.5 risulta "fuga", il verdetto NON può essere PASS senza una motivazione tecnica che spieghi perché quella fuga è accettabile.
- [ ] **AC-5**: tabella di classificazione per il supervisore con colonne `# | Problema | File:linea | Classificazione (BUG REALE / MIGLIORA PROCESSO / NEUTRO / RISCHIO PEGGIORAMENTO) | Modifica suggerita ai prompt`. Niente proposte di modifica generiche: ogni riga indica quale file e quale sezione, con suggerimento di patch testuale concreto.
- [ ] **AC-6**: il Reviewer ha applicato a sé stesso RM-1: nessuna asserzione "verificato X" nel suo report senza enumerazione delle alternative considerate e escluse (es. "verificato che RM-2 è agganciato in `developer.md` r.155" → enumerare le forme alternative di aggancio possibili e perché quella attuale è considerata azionabile, oppure dichiarare la verifica parziale).
- [ ] **AC-7**: il Reviewer ha applicato a sé stesso RM-2: ha eseguito grep nel repo (es. `grep -rn "RM-1\|RM-2\|RM-3\|RM-4" .claude/ tasks/`) per verificare di non aver mancato agganci presenti in posizioni diverse da quelle attese, e il grep eseguito è citato nel report.
- [ ] **AC-8**: il Reviewer ha applicato a sé stesso RM-3: ogni riferimento a documentazione (incluso `METODO.md`) è citato con file:linea, non parafrasato; nessuna conclusione si appoggia a "ricordo del prompt" senza file:linea.
- [ ] **AC-9**: nessuna modifica ai file P1..P5 è stata effettuata dal Reviewer (audit ostile, non riscrittura). Working tree del Reviewer pulito su tutti i 5 file del perimetro al momento del commit della review.

---

## Out-of-scope — esplicito

Il Reviewer NON tratta in `REVIEW_FONDAMENTA_01_web.md`:

- **Audit dei capitoli metodologici CAP-DATA-01/02/03 esistenti** (anche se compromessi dalla propagazione dello schema CANDLE errato). Sessioni separate, ognuna con propria `ACTIVE_TASK.md`. Rinvio: futura sessione "AUDIT-CAP-DATA-01-RIVERIFICA" (o nomi analoghi), una per capitolo.
- **Modifica diretta dei prompt agenti o di `METODO.md`**. Anche se identifica un buco evidente, il Reviewer **non** patcha. Produce solo finding + suggerimento di patch testuale nella tabella AC-5. Le modifiche, se approvate dal supervisore al punto di controllo CONDITIONAL/FAIL, sono eseguite da un Developer in fase di rework (vedi pipeline attesa).
- **Proposta di nuove RM-5, RM-6, ecc.** Il Reviewer può segnalare in "Osservazioni minori" che certe situazioni emergenti suggeriscono regole future, ma non le formalizza. La decisione di aggiungere una RM-N è del supervisore (vedi CLAUDE.md sezione "Regole metodologiche permanenti", responsabilità Orchestrator di proporle al supervisore).
- **Esecuzione di codice contro DAPI o di probe empirici**. Sede WEB, perimetro tutto su file committati. Nessuna prova empirica intraday/runtime è richiesta o ammessa nel report.
- **Revisione dei flussi di stato `tasks/STATO_CORRENTE.md`, `tasks/CARRYOVER.md`, `tasks/QUESTIONS.md`, `tasks/DEV_STATUS.md`** in quanto file di stato. Sono fuori dal perimetro normativo P1..P5. Possono essere letti come supporto evidenziale (es. per ricostruire il caso reale CANDLE), non auditati.
- **Modifiche alla matrice Web vs CLI di RM-4** in senso di "scelta della sede". La matrice è dichiarata vincolante in `METODO.md`. Il Reviewer verifica solo che sia ripresa coerentemente nei prompt (Check B.3); non la riapre.

---

## Done when — domande operative a cui il report del Reviewer deve rispondere

1. Per ogni RM-N (N=1..4) e per ogni ruolo (Orchestrator, Planner, Developer, Reviewer), qual è la **riga esatta** del prompt che aggancia operativamente quella regola? Se non esiste, il report lo dichiara letteralmente "ASSENTE in `<path>`".
2. La sessione web simulata nello scenario di Check C **viene fermata** prima del commit dello schema sbagliato? Se sì, da quale checkpoint (file:linea)? Se no, dove sono i punti di fuga?
3. Il workflow attuale **distingue** chiaramente i casi in cui Orchestrator deve esigere RM-4 opzione A vs opzione B vs nessuna review (cioè quando un output non rientra in RM-4)? Esistono criteri scritti? Sono operativi?
4. Quali clausole vincolanti di `METODO.md` (in particolare i blocchi "Formato obbligatorio" di RM-1 e RM-2 e l'ordine di priorità fonti di RM-3) **non hanno** una controparte operativa in nessuno dei 4 prompt agenti?
5. Verdetto finale: le RM-1..RM-4 nel loro stato attuale sono **sufficienti** a impedire la ricomparsa del pattern d'errore canonico? Se sì, motivazione puntuale ancorata a file:linea. Se no, lista dei buchi e patch suggerita per ciascuno.

---

## Pipeline attesa

**Iterazione 1**:
- Orchestratore della sessione corrente invoca **Reviewer** (sede WEB), con prompt che cita esplicitamente: leggi `tasks/METODO.md` e `tasks/ACTIVE_TASK.md`, perimetro = 5 file P1..P5, esegui Check A/B/C, applica RM-1/RM-2/RM-3 a te stesso (AC-6/AC-7/AC-8), produci `reviews/REVIEW_FONDAMENTA_01_web.md` con verdetto + tabella di classificazione, committa e pusha su `origin/main`.
- Reviewer produce il file e termina.

**Iterazione 2 (solo se CONDITIONAL/FAIL)**:
- Orchestratore esegue il **punto di controllo supervisore** (CLAUDE.md §"Punto di controllo supervisore"): presenta la tabella di classificazione AC-5, attende decisione del supervisore su quali finding "MIGLIORA PROCESSO" e "RISCHIO PEGGIORAMENTO" passare a Developer (i BUG REALI sono obbligatori).
- Orchestratore aggiorna `tasks/ACTIVE_TASK.md` aggiungendo sezione "## Finding di Review approvati per rework" con SOLO i finding approvati.
- Azzera `tasks/DEV_STATUS.md`.
- Invoca **Developer** con istruzione di patchare i prompt indicati (P1..P5 secondo necessità) **secondo le patch suggerite** in AC-5 modificate dalle decisioni del supervisore. Il Developer NON ridefinisce le RM; le esegue. Output del Developer: commit dei prompt patchati su `origin/main` + breve nota in `reports/REPORT_FONDAMENTA_01.md` (formato ridotto: solo "Cosa è stato modificato", "Mappatura finding → patch applicata", "Working tree verifica", "Push verifica").
- Developer scrive `READY_FOR_REVIEW` in `tasks/DEV_STATUS.md`.

**Iterazione 3 (Re-Review)**:
- Orchestratore esegue check post-Developer (6 controlli adattati: il "documento CAP" non è atteso; sono attesi i prompt patchati + il report ridotto + i file di stato puliti).
- Invoca di nuovo **Reviewer** (sede WEB) con istruzione: rieseguire Check A/B/C **sui prompt patchati** + verificare che i finding approvati siano effettivamente chiusi. Output: `reviews/REVIEW_FONDAMENTA_01_v2_web.md` con verdetto PASS / CONDITIONAL / FAIL.
- Loop fino a PASS. Regola terminazione 3 iterazioni (CLAUDE.md): se Reviewer e Developer divergono su un finding dopo 3 giri, Planner arbitra.

**Chiusura sessione PASS** (adattata, non sono le 7 condizioni standard CAP-XX):
1. Review PASS pubblicata su `origin/main`.
2. `DEV_STATUS.md` azzerato (se Iterazione 2/3 eseguita).
3. Eventuale `reports/REPORT_FONDAMENTA_01.md` pubblicato (solo se rework eseguito).
4. `00_indice.md` **NON va aggiornato** (non è un capitolo metodologico).
5. `tasks/ACTIVE_TASK.md` resta puntato a questo task (storico).
6. `tasks/CARRYOVER.md` aggiornato **solo se** la Review ha prodotto raccomandazioni di nuove RM-5..RM-N da valutare in futuro (in tal caso, registrare come "RACCOMANDAZIONE-METODO" con namespace separato dai M-promemoria di capitolo).
7. Notifica al supervisore con riepilogo (hash review PASS, conteggio finding, eventuali RACCOMANDAZIONI-METODO carryover) **senza** prompt-template per CAP-DATA-03: il supervisore deciderà autonomamente quando aprire la sessione successiva di rework capitoli o di nuovo capitolo.

---

## Note al Reviewer (vincoli operativi specifici di questo task)

- **Conflitto di interesse epistemico**: le RM e i prompt sono stati scritti dalla stessa sessione (web 28/05) che ha causato l'incidente CANDLE. Il Reviewer deve essere **particolarmente** sospettoso di clausole che potrebbero sembrare auto-assolutorie (es. "RM-4 si applica solo se l'output supera 200 righe" — il commit `7bb2955` aveva 795 righe nuove totali ma in 2 file da 588 e 207 separatamente; verificare se la soglia 200 è per-file o aggregata, e se questo crea un punto di fuga). RM-1 applicata al lavoro stesso del Reviewer = nessuna conclusione "verificato" senza enumerazione alternative.
- **Niente cosmesi**: come da prompt Reviewer (riga 64 di `.claude/agents/reviewer.md`), non riportare problemi di formattazione/stile che non cambiano il comportamento del sistema. Focus solo su finding che, se non chiusi, lasciano un cammino aperto al pattern d'errore canonico.
- **Citazioni testuali obbligatorie**: ogni finding cita il testo esatto del prompt incriminato (file:linea + virgolette), così che il punto di controllo supervisore possa verificare con un click. Niente parafrasi.
- **Test di simulazione (Check C) come ancora del verdetto**: il PASS non si concede sull'esistenza degli agganci, si concede sulla **dimostrata intercezione** del caso d'errore canonico nel workflow simulato. Se la simulazione mostra fughe, anche se gli agganci esistono, è almeno CONDITIONAL.

---

## Note al Developer (solo se Iterazione 2 viene attivata)

- Patchare **solo** i finding approvati dal supervisore. Niente patch "mentre ci sono".
- Mantenere la coerenza fra i prompt: una modifica a un punto di `CLAUDE.md` può richiedere riflesso in `developer.md` o `reviewer.md`; documentare nel report ridotto la mappatura.
- Nessuna modifica a `METODO.md` salvo che la patch approvata sia esplicitamente su quel file (es. correzione di un'incoerenza interna individuata in Check B).
- Commit message format: `[METODO-RM] patch RM-N — <breve descrizione>` per modifiche a `METODO.md`; `[AGENT-PROMPT] patch <ruolo> — <breve descrizione>` per modifiche ai prompt agenti.
- Push diretto a `origin/main` (push policy MEMORY).

---

## Pipeline sintetica

```
Reviewer(WEB) Iter.1
  ↓
verdetto PASS                                        → chiusura sessione (7 punti adattati)
verdetto CONDITIONAL/FAIL → controllo supervisore    → Developer Iter.2 → Reviewer Iter.3
                                                                       ↓
                                                                       PASS o nuovo loop
```

---

## Finding di Review approvati per rework (Iterazione 2)

**Verdetto Review v1**: FAIL (`reviews/REVIEW_FONDAMENTA_01_web.md`, commit `3ed0198`).
**Punto di controllo supervisore eseguito 2026-05-29.** Decisione del supervisore:
**TUTTI e 10 i finding approvati per il Developer** (3 BUG REALI + 5 MIGLIORA PROCESSO + 2 NEUTRO inclusi su scelta esplicita del supervisore).

Il Developer corregge **solo** i file di perimetro indicati, applicando le patch suggerite dal Reviewer (adattabili nella forma, non nella sostanza). NON ridefinisce le RM. NON introduce regole nuove (no RM-5+). Edita **solo contenuto** e fa `git add` dei **soli** file effettivamente modificati nel contenuto (NON aggiungere file con sola modifica EOL/BOM, es. `planner.md`, per non sporcare il commit — nota line-ending autocrlf attiva).

### BUG REALI (obbligatori)

| # | File:linea | Finding | Azione richiesta |
|---|-----------|---------|------------------|
| 1 | `CLAUDE.md:20-30` + `:114-144` | Nessun trigger nella macchina a stati Orchestrator che attivi RM-4 *ex-ante* prima del commit di output non-CAP fuori dal ciclo Planner→Developer→Reviewer. La sez. "Workflow non-CAP" descrive ma non è agganciata a una condizione. | Aggiungere una riga alla macchina a stati `CLAUDE.md:24-30`: "Se la sessione corrente sta per produrre/committare output non-CAP che soddisfa uno dei criteri `:118-122`, prima del commit esegui il workflow RM-4 (`:114-144`)". In "Cosa l'orchestratore NON fa mai" (`:152-162`) aggiungere: "Non lascia passare un commit non-CAP senza opzione A o B; se l'autore opera in sessione autonoma, l'autore applica opzione A blindata dal proprio prompt". |
| 2 | `developer.md:22`, `:131-159` | Il prompt Developer non ha pre-consegna RM-4 per output non-CAP. L'opzione A (self-review) è solo istruzione all'Orchestrator, non obbligo blindato dell'autore. | Aggiungere a `developer.md` una sezione "Pre-consegna per output non-CAP (RM-4 opzione A)" con checklist vincolante: (1) blocco "Self-review RM-1..RM-3" in fondo al documento o nel commit message esteso; (2) lista asserzioni "verificato" + alternative escluse nel formato 4-righe; (3) grep documentato; (4) fonti etichettate; (5) `READY_FOR_PROBE_REVIEW` in `DEV_STATUS.md` se opzione B richiesta. Aggiungere punto 13 alla pre-consegna. |
| 4 | `developer.md:155` | Check RM-2 (grep) vincolato al `REPORT_CAP_XX`; per output non-CAP non c'è dove documentarlo. | Nella nuova sezione "Pre-consegna RM-4 opzione A", replicare il check grep sui blocchi non-CAP: lista decoder consultati nel repo con path:linea o dichiarazione "nessuno trovato dopo grep su <pattern>", inclusa nel commit message o nel documento. |

### MIGLIORA PROCESSO (approvati dal supervisore — obbligatori)

| # | File:linea | Finding | Azione richiesta |
|---|-----------|---------|------------------|
| 3 | `developer.md:153`, `reviewer.md:17,56,114` | Check pre-consegna p.10 non impone il formato 4-righe `VERIFICA/PROVE/ALTERNATIVE ESCLUSE/ALTERNATIVE NON ESCLUSE` di `METODO.md:28-33`. Prosa libera passa come compliant. | Estendere `developer.md:153` (punto 10): "con formato esatto VERIFICA/PROVE/ALTERNATIVE ESCLUSE/ALTERNATIVE NON ESCLUSE (cfr. METODO.md:28-33). Asserzioni in prosa libera senza blocco formattato sono respinte come 'non in formato'". Estendere `reviewer.md:17` con il criterio di rigetto del formato. |
| 5 | `CLAUDE.md:112` | Nessun recupero retroattivo: la sessione successiva non rilegge handoff/probe non revisionati per riclassificarli RM-4. | Aggiungere al primo atto dell'Orchestratore della nuova sessione (`CLAUDE.md:112`): "Verifica anche se la sessione precedente ha committato output non-CAP. Per ognuno controlla che esista un blocco self-review (opz. A) o una probe-review committata (opz. B). Se manca, apri un task `AUDIT-RECUPERO-<nome>` come secondo atto prima del normale flusso." |
| 6 | `CLAUDE.md:7-12` | Orchestrator ha RM-1/2/3 solo come elenco enunciativo, senza gatekeeping sui commit non-CAP. | Aggiungere a `CLAUDE.md:9-12` la responsabilità: "Applicare RM-1 ai commit non-CAP: rifiutare commit che dichiarano 'verificato X' senza blocco 4-righe. RM-2: rifiutare commit di parser senza grep documentato. RM-3: rifiutare commit con conclusioni wiki-only." |
| 7 | `CLAUDE.md:135-136` | Soglia "200 righe" ambigua (per-file vs aggregata; ridondante per i decoder; valore non giustificato). Possibile fuga per handoff "piccoli". | Riscrivere `CLAUDE.md:134-136`: "B è obbligatoria se: (a) introduce un decoder/parser di sistema esterno, OR (b) modifica un fatto già dichiarato 'verificato' in CAP precedenti, OR (c) il diff **aggregato del commit** supera N righe (N=200 valore di lavoro). A è ammessa solo se nessuno di a/b/c è vero." Eliminare il criterio "area circoscritta" non definito. |
| 8 | `developer.md:153` + `reviewer.md` | Formato 4-righe non esigibile da nessun prompt (componente di #3). | Coperto dalla patch #3. |

### NEUTRO (inclusi su decisione esplicita del supervisore)

| # | File:linea | Finding | Azione richiesta |
|---|-----------|---------|------------------|
| 9 | `METODO.md:147` | "lista non esaustiva" lascia discrezionalità su output borderline. | Convertire `METODO.md:147` in lista esaustiva con un criterio di estensione esplicito (es. "ogni output che soddisfa i criteri RM-4 in `CLAUDE.md:118-122`; estensioni richiedono commit `[METODO]` dedicato"). |
| 10 | `CLAUDE.md:140-142` | `CLAUDE.md` non ripropone i divieti-per-sede del Reviewer (matrice solo in `reviewer.md`). | Aggiungere a `CLAUDE.md:140-142` un rimando esplicito ai divieti-per-sede di `reviewer.md:163-164` (Web non dichiara verificato-empirico; CLI non fa probe massivi di zelo). |

### Vincoli per la rework Iterazione 2

- Modifiche **solo** ai file di perimetro effettivamente coinvolti: `CLAUDE.md`, `developer.md`, `reviewer.md`, `METODO.md`. (`planner.md` NON è coinvolto da alcun finding approvato — non editarlo né committarlo.)
- Mantenere coerenza inter-prompt: una modifica a `CLAUDE.md` può richiedere riflesso in `developer.md`/`reviewer.md`; documentare la mappatura nel report.
- Nessuna riapertura delle RM-1..RM-4 nel loro enunciato; si aggancia/rende esigibile ciò che già esiste.
- Output Developer: prompt patchati su `origin/main` + `reports/REPORT_FONDAMENTA_01.md` (formato ridotto: Cosa è stato modificato, Mappatura finding→patch, Verifica working tree, Verifica push).
- Commit message: `[METODO-RM] patch RM-N — <descr>` per `METODO.md`; `[AGENT-PROMPT] patch <ruolo> — <descr>` per i prompt agenti.
- `git add` solo dei file con modifica di **contenuto** (autocrlf attiva → evitare di committare file con sola churn EOL/BOM).
- Al termine: pre-consegna checklist, poi `READY_FOR_REVIEW` in `tasks/DEV_STATUS.md`.

---

## Finding di Review v2 approvati per rework (Iterazione 4 — rework v3)

**Verdetto Review v2 (Re-Review Iter.3)**: CONDITIONAL (`reviews/REVIEW_FONDAMENTA_01_v2_web.md`, sede WEB).
**Punto di controllo supervisore eseguito 2026-05-29.** Decisione del supervisore:
**TUTTI e 3 i finding (N1, N2, N3) approvati per il Developer** (tutti MIGLIORA PROCESSO; nessun BUG REALE, nessun NEUTRO).

Sono regressioni inter-prompt introdotte dal rework Iter.2 stesso: due cross-reference di riga fuori sincrono + un gap di transizione nella tabella decisionale dell'Orchestratore. Il Developer corregge **solo** i rimandi/transizioni indicati; NON riapre i finding v1 (#1..#10, già chiusi), NON ridefinisce le RM, NON introduce regole nuove.

### MIGLIORA PROCESSO (approvati dal supervisore — obbligatori)

| # | File:linea | Finding | Azione richiesta |
|---|-----------|---------|------------------|
| N1 | `developer.md:152` | Rimando alla "matrice di sede Web/CLI" punta a `CLAUDE.md:140-142`, che contiene invece i criteri A/B (a/b/c). La matrice di sede è a `CLAUDE.md:149-153`. | In `developer.md:152` correggere il riferimento `CLAUDE.md:140-142` → `CLAUDE.md:149-153`. Preferibile sostituire il rimando numerico con un'àncora di sezione ("§Workflow per output non-CAP — matrice di sede") per immunizzare dal churn di riga. |
| N2 | `developer.md:133` + `CLAUDE.md:30` | Rimando ai "3 criteri OR" che qualificano un output non-CAP punta a `CLAUDE.md:118-122` (titolo + intro). I tre criteri OR sono ai bullet `CLAUDE.md:124-126`. Stesso off-by-range replicato in due punti. | Aggiornare entrambi i rimandi: `developer.md:133` e `CLAUDE.md:30` da `:118-122` → `:124-126`. Preferibile àncora di sezione ("§Workflow per output non-CAP — criteri OR"). |
| N3 | `CLAUDE.md:27-33` | La macchina a stati dell'Orchestratore non ha una riga che intercetti `READY_FOR_PROBE_REVIEW` (prodotto da `developer.md:133,152,164,201`); gestisce solo `READY_FOR_REVIEW` (`CLAUDE.md:32`). Lo stato opzione-B introdotto da Iter.2 non ha transizione deterministica. | Aggiungere alla tabella `CLAUDE.md:27-33` una riga che intercetti `tasks/DEV_STATUS.md` = `READY_FOR_PROBE_REVIEW <path>` (quando non esiste ancora `reviews/PROBE_REVIEW_<nome>_*.md`): "determina la sede (Web/CLI) secondo la matrice `:149-153`, ricorda i divieti per sede (`reviewer.md:163-164`), invoca il **reviewer** in modalità probe-review sul `<path>`". Allineare la sezione "Workflow per output non-CAP" citando `READY_FOR_PROBE_REVIEW` come trigger. |

### Vincoli per la rework Iterazione 4 (v3)

- Modifiche **solo** ai file effettivamente coinvolti: `CLAUDE.md`, `developer.md`. (`reviewer.md`, `METODO.md`, `planner.md` NON sono coinvolti da N1/N2/N3 — non editarli né committarli.)
- **Attenzione meta-ricorsiva**: questi finding SONO essi stessi rimandi di riga. Dopo aver applicato i fix, i numeri di riga di destinazione possono spostarsi. Verificare che i rimandi corretti puntino ancora al contenuto giusto **dopo** l'edit (rileggere le righe di destinazione a valle delle modifiche), oppure adottare i rimandi per àncora di sezione come suggerito dal Reviewer (più robusti).
- Nessuna riapertura delle RM-1..RM-4 nel loro enunciato; nessuna riapertura dei finding v1 #1..#10.
- Output Developer: prompt patchati su `origin/main` + aggiornamento di `reports/REPORT_FONDAMENTA_01.md` (aggiungere una sezione "Rework v3 — chiusura N1/N2/N3" col formato ridotto: Cosa è stato modificato, Mappatura finding→patch, Verifica rimandi post-edit, Verifica working tree, Verifica push).
- Commit message: `[AGENT-PROMPT] patch <ruolo> — chiusura N1/N2/N3 rework v3`.
- `git add` solo dei file con modifica di **contenuto** (autocrlf attiva → niente churn EOL/BOM, es. `planner.md`).
- Al termine: pre-consegna checklist, poi `READY_FOR_REVIEW` in `tasks/DEV_STATUS.md`.
