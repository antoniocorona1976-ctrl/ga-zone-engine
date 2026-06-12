# SINTESI GOVERNANCE — ga-zone-engine (per AC)

**Data**: 2026-06-12 · **Natura**: documento riassuntivo di governance, non normativo. In caso di divergenza prevalgono le fonti.
**Fonti**: `.claude/CLAUDE.md` (Orchestratore + track) · `tasks/METODO.md` (RM-1..RM-4 + enforcement) · `.claude/BASE_COMUNE.md` (base comune ai track) · `.claude/agents/{planner,developer,reviewer,spec_planner,spec_developer,spec_reviewer}.md` (ruoli).

---

## 1. Vista d'insieme

Il progetto lavora su **due track**, con lo stesso ciclo a tre ruoli:

```
SUPERVISORE (AC) ──apre sessione / decide──▶ ORCHESTRATORE (sessione principale)
                                                │ invoca, controlla, committa stati
                              ┌─────────────────┼──────────────────┐
                              ▼                 ▼                  ▼
                           PLANNER  ──▶     DEVELOPER   ──▶     REVIEWER
                       (ACTIVE_TASK)   (documento+report)  (review PASS/COND/FAIL)
                              ▲                                    │
                              └──── finding approvati da AC ◀──────┘
```

| Track | Oggetto | Output | Ruoli | Discriminatore |
|---|---|---|---|---|
| **A — Metodologia v2** | capitoli `CAP-XX` (Parti I–X) | `docs/methodology_v2/CAP_XX_*.md` + `reports/REPORT_CAP_XX.md` | `planner`, `developer`, `reviewer` | intestazione `ACTIVE_TASK.md` = `CAP-XX`; stato Parte in `00_indice.md` |
| **B — Business-spec** | specifiche di prodotto `SPEC-FUNZ-NN` (ponte verso FASE-D) | `docs/spec_funzionale/SPEC_FUNZ_NN.md` + `reports/REPORT_SPEC_FUNZ_NN.md` | `spec_planner`, `spec_developer`, `spec_reviewer` | intestazione `ACTIVE_TASK.md` = `SPEC-FUNZ-NN`; `00_indice.md` NON si tocca |

**Principio cardine**: un task è completo solo quando il **Reviewer emette PASS** — mai quando "i file sono prodotti". Ogni capitolo/spec si sviluppa in **una sessione nuova e isolata**; tutto vive su `main` (trunk), push diretto approvato.

**Ordine di lettura obbligatorio per ogni agente a inizio sessione**: 1) `tasks/METODO.md` → 2) `.claude/BASE_COMUNE.md` → 3) il proprio ruolo → 4) `tasks/ACTIVE_TASK.md`.

**Modello**: tutti i 6 ruoli e la sessione principale sono pinnati a `claude-fable-5`.

---

## 2. Attori — schede sintetiche

### 2.1 Supervisore — AC (Antonio Corona)

| | |
|---|---|
| **Chi è** | L'utente umano. **Autorità finale del progetto.** |
| **Si attiva** | Sempre disponibile; interviene ai punti di decisione. Apre ogni nuova sessione. |
| **Input ←** | Dall'Orchestratore: tabella "Classificazione per il supervisore" (su CONDITIONAL/FAIL), riepilogo di chiusura + prompt-template, segnalazioni di violazione di processo, richieste di arbitraggio. |
| **Output →** | All'Orchestratore: decisioni sui finding non-bloccanti, arbitraggi, scelta del track/capitolo successivo, autorizzazioni override. |
| **Decide (in esclusiva)** | (1) finding MIGLIORA PERFORMANCE / RISCHIO PEGGIORAMENTO; (2) arbitraggi dopo 3 iterazioni Review↔Developer; (3) track/capitolo successivo a ogni chiusura; (4) modifiche alla governance (CLAUDE.md, BASE_COMUNE, METODO, ruoli); (5) ogni uso degli override del guard (`[RM-HOOK-OVERRIDE]`, `.claude/AGENTS_UNLOCK`); (6) applicazione di NEUTRO su PASS (micro-pass + re-review). |
| **Non fa** | Non serve la sua conferma per i push su `main` (prassi approvata) né per i passi già normati della macchina a stati. |

### 2.2 Orchestratore (sessione principale Claude Code, CLI o Web)

| | |
|---|---|
| **Chi è** | La sessione principale aperta da AC. Non è un subagente; il ruolo è definito solo da `.claude/CLAUDE.md`. Esiste anche una **routine remota** (trigger manuale claude.ai) che lancia un Orchestratore cloud sede Web, no DAPI, mai in auto-avvio. |
| **Si attiva** | All'apertura di sessione da parte di AC. Prima azione: leggere `METODO.md` + file di stato; agire sulla **prima condizione vera** della macchina a stati (§5). |
| **Input ←** | File di stato (`ACTIVE_TASK`, `DEV_STATUS`, `STATO_CORRENTE`, `CARRYOVER`, `00_indice`); verdetti del Reviewer; decisioni di AC; output dei subagenti. |
| **Output →** | Invocazioni dei subagenti (con prompt che ricorda letture obbligatorie, divieti di sede, dati autoritativi); commit del task card del Planner; azzeramento `DEV_STATUS`; tabella classificazione → AC; checklist di chiusura; aggiornamento `CARRYOVER`/`STATO_CORRENTE` in chiusura; riepilogo + prompt-template → AC. |
| **Fa** | Router del track attivo; check post-Developer (6 controlli); punto di controllo supervisore; gatekeeping RM-1/2/3 sui commit non-CAP; instradamento RM-4 (opzione A/B + sede); apertura `AUDIT-RECUPERO-<nome>` se trova output non-CAP senza review; verifica autoconsistenza delle 7 condizioni della sessione precedente (primo atto di ogni nuova sessione); recupero dati web per i subagenti (loro non hanno WebFetch/WebSearch) depositandoli in `ACTIVE_TASK.md` come **autoritativi**. |
| **Non fa mai** | Non scrive `docs/` (è Developer) · non fa audit (è Reviewer) · non definisce lo scope (è Planner) · non manda finding non-bloccanti a Developer senza AC · non salta il punto di controllo "perché sono cose minori" · non chiama Planner per il task successivo dopo PASS (lo fa la sessione nuova, su decisione di AC) · non chiude senza le 7 condizioni · non auto-fixa i gap di consegna del Developer · non lascia passare commit non-CAP determinanti senza opzione A o B · non agisce su un messaggio-titolo di AC (attende il prompt vero) · non aggira il guard via shell. |

### 2.3 Planner (Track A) / spec_planner (Track B)

| | Planner (A) | spec_planner (B) |
|---|---|---|
| **Si attiva** | Nuova sessione dopo PASS del capitolo precedente (con `00_indice.md` già a PASS), o assenza di task attivo. Invocato dall'Orchestratore. | Idem, quando AC ha deciso un task SPEC-FUNZ-NN. Si esegue via `general-purpose` che adotta `spec_planner.md`. |
| **Input ←** | `00_indice.md`, ultimo REPORT, ultima review, `QUESTIONS.md`, `CARRYOVER.md` (censimento M-promemoria obbligatorio: nessun M perso), decisioni AC (Q-XX chiuse). | Idem + capitoli metodologia v2 da consolidare; `STATO_CORRENTE.md`. |
| **Output →** | `tasks/ACTIVE_TASK.md` (scope, eredità obbligatorie, AC verificabili, out-of-scope con destinazione, done-when, pipeline). **Non lo committa**: lo committa l'Orchestratore (gatekeeping). A chiusura PASS aggiorna `00_indice.md`. | `tasks/ACTIVE_TASK.md` con intestazione `SPEC-FUNZ-NN`, "Sezioni" (non "Capitoli"), modalità review e sede dichiarate. **Non tocca `00_indice.md`**. |
| **Regola di valore** | Orientamento al comportamento del GA: ogni task deve avere impatto identificabile su ranking/fitness/conversione signal-to-trade. | **Reinterpretata**: ogni requisito traccia a (a) valore operativo/prodotto reale E (b) capitolo metodologia v2 di origine. |
| **Fa inoltre** | Secondo giro di completezza (checklist RM-1..RM-4) prima di pubblicare; gestione M-promemoria (censimento/assegnazione/rinvio/chiusura); registra le decisioni AC in `QUESTIONS.md`; arbitro tecnico nel loop (l'arbitraggio finale resta ad AC). | Idem + vincoli N1 (requisiti atomici) e F6 (blocchi in batch) imposti al Developer negli AC. |
| **Non fa** | Non scrive il documento · non fa audit · non corregge bug · non decide al posto di AC (apre Q-XX) · un solo task alla volta, niente piani a 6 mesi · niente conferme inutili ("vuoi che proceda?" vietato) · niente numeri inventati (parametri provvisori dichiarati o Q-XX). | Idem + non riapre CAP chiusi né decisioni D-*-N. |

### 2.4 Developer (Track A) / spec_developer (Track B)

| | Developer (A) | spec_developer (B) |
|---|---|---|
| **Si attiva** | `ACTIVE_TASK.md` definito e `DEV_STATUS.md` vuoto (v1), oppure rilancio con finding approvati da AC (iterazione N>1) o con gap di consegna. Invocato dall'Orchestratore. | Idem; via `general-purpose` che adotta `spec_developer.md`. |
| **Input ←** | `ACTIVE_TASK.md` (lo esegue alla lettera; i dati ivi depositati dall'Orchestratore sono autoritativi), finding approvati, `reviews/*`, `CARRYOVER.md` (sola lettura). | Idem + CAP chiusi in `docs/methodology_v2/` letti selettivamente per citazioni `capitolo:riga` accurate. |
| **Output →** | `docs/methodology_v2/CAP_XX_*.md` + `reports/REPORT_CAP_XX.md` (formato supervisore: 5 sezioni + tabella AC `OK/PARZIALE/MANCA` con evidenza `file:riga`); `00_indice.md` → IN REVIEW; commit `[CAP-XX]` pushati su `origin/main`; segnale `READY_FOR_REVIEW` (o `READY_FOR_PROBE_REVIEW <path>` per output non-CAP in opzione B) in `DEV_STATUS.md`; poi **si ferma**. | `docs/spec_funzionale/SPEC_FUNZ_NN.md` + `reports/REPORT_SPEC_FUNZ_NN.md`; commit `[SPEC-FUNZ-NN]`; sempre `READY_FOR_REVIEW` (track documento puro, niente probe). |
| **Obblighi chiave** | Pre-consegna checklist (13 controlli, inclusi RM-1 blocco 4-righe, RM-2 grep documentato, RM-3 etichette, RM-4 self-review); misura prima/dopo + criterio di rollback per ogni modifica; onestà AC (mentire peggiora la review); per output non-CAP la self-review opzione A è blindata dal suo stesso prompt. | Requisiti **atomici** (N1: una proposizione verificabile per ID); blocchi raccolti **in batch** nel REPORT (F6), non a goccia; zero nuovi "fatti dichiarati di prima istanza" — ogni asserzione è richiamo etichettato a CAP chiuso; misura prima/dopo adattata al greenfield (niente metriche GA inventate). |
| **Non fa mai** | Non ridefinisce il piano · non aggiunge sezioni non richieste · non emette verdetto sul proprio lavoro · non chiude il task da solo · non discute con Review nei commit (contestazioni nel REPORT) · non scrive READY_FOR_REVIEW senza checklist · non parte con un task nuovo prima del PASS del precedente · se un punto non è chiaro scrive in `QUESTIONS.md`, non improvvisa. | Idem + non modifica `00_indice.md`, `STATO_CORRENTE`, `CARRYOVER`, `QUESTIONS`, `ACTIVE_TASK` · non riapre/ri-deriva i CAP chiusi né il PDF originale · non produce script/probe collaterali. |

### 2.5 Reviewer (Track A) / spec_reviewer (Track B)

| | Reviewer (A) | spec_reviewer (B) |
|---|---|---|
| **Si attiva** | `DEV_STATUS.md = READY_FOR_REVIEW` **e** check post-Developer superato; oppure modalità **probe-review** su `READY_FOR_PROBE_REVIEW <path>` (output non-CAP, RM-4 opzione B). Invocato dall'Orchestratore con sede e divieti dichiarati nel prompt. | `DEV_STATUS = READY_FOR_REVIEW` su SPEC-FUNZ-NN; modalità **CAP-review piena adattata al non-CAP** (due giri, non probe ridotta); via `general-purpose` che adotta `spec_reviewer.md`. |
| **Input ←** | Documento + REPORT del Developer, `ACTIVE_TASK.md` (gli AC contro cui audita), repo committato (grep/Read), eventuale lista "Empirico-CLI da verificare" dalla sede opposta. | Idem + CAP chiusi (li apre con Read per la fedeltà di tracciabilità). |
| **Output →** | `reviews/REVIEW_CAP_XX_review.md` con verdetto **PASS / CONDITIONAL / FAIL** in apertura, problemi bloccanti/non bloccanti/osservazioni, citazioni problematiche, **tabella "Classificazione per il supervisore"** (BUG REALE / MIGLIORA PERFORMANCE / NEUTRO / RISCHIO PEGGIORAMENTO), sezione "Applicazione RM-1 a me stesso". In probe-review: `reviews/PROBE_REVIEW_<nome>_web.md` / `_cli.md` (formato snello, 4 check). Ogni iterazione **appende**, non sovrascrive. | `reviews/REVIEW_SPEC_FUNZ_NN_review.md`, stesso formato + header di sede + lista "Empirico-CLI da verificare" (attesa **vuota**). Commit `[REVIEW] SPEC-FUNZ-NN — verdetto: <...>`. |
| **Postura** | **Ostile per default**: il valore è trovare problemi reali. **Doppio giro obbligatorio** ("sono sicuro di aver trovato tutto?"). Pesa i finding sull'impatto GA (ranking, fitness, leakage, residui multi-indice, coerenza coi PDF di riferimento, completezza AC). | Ostile, doppio giro. Asse di impatto reinterpretato: (1) fedeltà di tracciabilità (apre i CAP citati e controlla che ogni citazione risolva — citazione che non risolve = BUG REALE); (2) contraddizioni con CAP chiusi (finding sempre sulla spec, mai sul CAP); (3) RM-1/2/3; (4) completezza vs AC; (5) valore operativo + onestà REPORT; (6) atomicità N1. |
| **Non fa mai** | Non riscrive il capitolo · non ridefinisce il piano · non riporta cosmesi senza impatto · non manda NEUTRO/RISCHIO a Developer senza AC · **Web**: non dichiara nulla "empiricamente provato" se richiede DAPI/filesystem locale (segnala "Empirico-CLI da verificare") · **CLI**: non esegue probe massivi di zelo (riproduce solo le asserzioni puntuali segnalate o dubbie). | Idem + non riapre i CAP chiusi PASS · non azzera `DEV_STATUS` (lo fa l'Orchestratore) · non modifica spec né CAP. |

### 2.6 Guard automatico — `rm_guard.py` (attore non umano, dal 2026-06-12)

| | |
|---|---|
| **Chi è** | Hook PreToolUse (`scripts/claude_hooks/rm_guard.py` + regole `permissions.deny` in `.claude/settings.json`). Attivo in sede CLI **e** Web, **anche sull'Orchestratore**. |
| **Si attiva** | Automaticamente, prima di ogni tool-call interessata (commit, lettura/scrittura su path protetti). |
| **Blocca** | (1) **RM-1 forma**: commit che aggiunge righe "verificat*" in `.md` senza il blocco `VERIFICA/PROVE/ALTERNATIVE` nel file (esenti: file di stato, `reviews/`, `reports/`, `docs/methodology_v2/`); (2) **RM-4 forma**: commit di nuovi `tasks/HANDOFF_*`, `PROBE_*`, `INDAGINE_*`, `RIPRESA_*` o script di parsing in `scripts/` senza blocco self-review né probe-review; (3) **quarantena impianto B**: lettura/scrittura in `Business Spec/OLD_NOT_USE_NOT_READ_FILES_MODEL_4_CANALI/`; (4) **protezione ruoli**: scrittura su `.claude/agents/` salvo flag `.claude/AGENTS_UNLOCK` (creato/rimosso solo su autorizzazione AC). |
| **Limite dichiarato** | Controlla la **presenza** dei blocchi, non la loro **verità**: guard verde ≠ contenuto corretto. La sostanza di RM-1..RM-4 resta in carico al gatekeeping dell'Orchestratore e alle review. RM-2 e RM-3 restano senza enforcement automatico (valgono per via procedurale). |
| **Override** | Tag `[RM-HOOK-OVERRIDE]` nel comando git — solo con autorizzazione esplicita di AC, motivato nel commit message. Un blocco non si aggira via shell. |

---

## 3. Regole metodologiche permanenti (RM-1..RM-4) — vincolano TUTTI

| Regola | Enunciato sintetico | Obbligo di forma |
|---|---|---|
| **RM-1** — verifica vs assunzione | Se un test lascia più conclusioni compatibili coi dati, l'esito è "**verifica parziale**" con le ipotesi alternative nominate. Vietato dichiarare chiuso ciò che non esclude tutte le permutazioni. | Blocco 4-righe esatto (sotto). Prosa libera = respinta come "non in formato" (BUG REALE). |
| **RM-2** — grep prima di assumere | Prima di assumere il formato di un payload esterno (DAPI, Telegram, vendor, file format): grep sistematico dei decoder/parser già nel repo e lettura dei loro commenti. Il codice di produzione batte la documentazione esterna. | Nel commit message dei nuovi parser: lista `path:linea` dei decoder esistenti, oppure "nessuno trovato dopo grep su `<pattern>`". |
| **RM-3** — doc esterna ≠ fonte di verità | Priorità fonti: 1) prove empiriche dirette > 2) codice di produzione nel repo > 3) documenti interni committati > 4) wiki/docs ufficiali (solo hint). Conclusioni solo-livello-4 inammissibili. La wiki Directa è dimostrata inesatta (schema CANDLE). | Etichette: `[PROVA-EMPIRICA <data>]` / `[CODICE-EXISTENTE r.NNN]` / `[DOC-INTERNO <path>]` / `[WIKI-HINT, da verificare]`. |
| **RM-4** — review per output non-CAP | Probe, script di parsing, handoff, indagini, M-promemoria destinati a CARRYOVER non si committano senza review esplicita: **opzione A** (self-review blindata dell'autore) o **opzione B** (probe-review del Reviewer). Lista tipi esaustiva; estensioni solo con commit dedicato `[METODO]`. | Vedi §6. Nessuna esenzione "perché è veloce / è notte / è solo un probe". |

Formato obbligatorio RM-1 (in ogni report/documento/commento che dichiari un esito di verifica):

```
VERIFICA: <asserzione>
PROVE: <quali dati osservati, quale test eseguito>
ALTERNATIVE COMPATIBILI ESCLUSE: <elenco esplicito>
ALTERNATIVE COMPATIBILI NON ESCLUSE: <elenco esplicito — se non vuoto, l'asserzione è "parziale">
```

Origine: incidente commit `7bb2955` (28/05/2026) — schema CANDLE dichiarato chiuso da soli daily, smentito da prova diretta (`C;L;H;O`), col decoder di produzione corretto già in repo e mai grepato.

---

## 4. Regole di processo trasversali (BASE_COMUNE)

- **Ciclo forzato**: Planner → Developer → check post-Developer (Orchestratore) → Reviewer → (CONDITIONAL/FAIL → punto di controllo AC | PASS → chiusura).
- **Reviewer bi-sede** (vincolo permanente, entrambi i track): **Web** = audit statico (repo via git, niente DAPI, niente file locali); **CLI locale** = verifica empirica (filesystem `C:\`, DAPI live con DGo+Darwin aperti). Handoff cross-sede via `reviews/PROBE_REVIEW_<nome>_web.md` / `_cli.md` + lista "Empirico-CLI da verificare". Divieti per sede vincolanti (Web non certifica l'empirico; CLI non fa probe di zelo).
- **Classificazione finding**: BUG REALE → sempre a Developer; NEUTRO → mai senza approvazione AC; MIGLIORA PERFORMANCE / RISCHIO PEGGIORAMENTO → decide AC. Su PASS con NEUTRO: micro-pass solo se AC approva, con re-review.
- **Check post-Developer (6 controlli)**: documento esiste · report con 5 sezioni + tabella AC · indice aggiornato (Track B: N/A) · working tree pulito sul task · commit pushato · commit copre i file attesi. Anche un solo gap → si rilancia Developer (mai fix d'ufficio dell'Orchestratore).
- **Doppio giro ostile** del Reviewer; le iterazioni di review si **appendono** al file.
- **Terminazione del loop**: disaccordo Review↔Developer dopo **3 iterazioni** sullo stesso punto → arbitraggio AC; nessuno chiude unilateralmente.
- **Onestà claim → evidenza**: tabella AC veritiera (`OK/PARZIALE/MANCA` + `file:riga`); il Reviewer applica RM-1 a sé stesso in sezione dedicata.
- **Registry subagenti**: `planner` (Track A) è subagent_type nativo (no Bash → il task card lo committa l'Orchestratore); `developer`/`reviewer` e i tre `spec_*` si eseguono via `general-purpose` che adotta il rispettivo `.md`. I subagenti **non hanno web**: i dati esterni li procura prima l'Orchestratore. Nel prompt di invocazione sempre: "leggi `tasks/METODO.md` e `.claude/BASE_COMUNE.md` prima di iniziare".

---

## 5. Macchina a stati dell'Orchestratore (sintesi)

| # | Condizione (prima vera vince) | Azione |
|---|---|---|
| 1 | Nessun task attivo, **oppure** task chiuso PASS e discriminatore di chiusura già aggiornato (Track A: `00_indice.md` a PASS) → siamo in **sessione nuova** | Invoca **Planner** per il task successivo (solo dopo decisione AC sul track) |
| 2 | Sta per essere committato **output non-CAP** che ricade in RM-4 (parsing esterno / "fatti dichiarati" per CAP successivi / asserzioni per CARRYOVER) | Instrada nel workflow RM-4 (§6) **prima** del commit |
| 3 | `DEV_STATUS` vuoto e `ACTIVE_TASK` non chiuso PASS | Invoca **Developer** |
| 4 | `DEV_STATUS = READY_FOR_REVIEW` e review mancante | **Check post-Developer**; se OK invoca **Reviewer**, altrimenti rilancia Developer sui gap |
| 5 | `DEV_STATUS = READY_FOR_PROBE_REVIEW <path>` e probe-review mancante | Determina sede (matrice §6), invoca **Reviewer in probe-review**; niente commit dell'output senza PASS |
| 6 | Ultima review = CONDITIONAL o FAIL | **Punto di controllo AC**: tabella → decisione → finding approvati in `ACTIVE_TASK` → azzera `DEV_STATUS` → Developer |
| 7 | Ultima review = PASS e chiusura non ancora eseguita (sessione N) | **Checklist di chiusura** (7 condizioni, §7), riepilogo ad AC, stop |

Discriminatore sessione N (che ha prodotto il PASS) vs N+1 (fresh): Track A = stato Parte in `00_indice.md`; Track B = `STATO_CORRENTE.md` + `ACTIVE_TASK.md`.

**Primi atti di ogni sessione nuova**: (1) autocheck delle 7 condizioni della sessione precedente — se una manca, segnalazione ad AC prima di procedere; (2) controllo retroattivo sugli output non-CAP committati: se manca sia self-review (A) sia probe-review (B), apertura task `AUDIT-RECUPERO-<nome>`.

---

## 6. Workflow output non-CAP (RM-4): opzione A vs B, e sede

**Criterio meccanico (nessuna discrezionalità)** — **B obbligatoria** se almeno uno:
(a) il commit introduce un **decoder/parser nuovo** di sistema esterno; (b) **modifica un fatto già dichiarato chiuso** in CAP precedenti o handoff committati; (c) il **diff aggregato del commit supera 200 righe**. **A ammessa** solo se nessuno di (a)/(b)/(c) è vero.

- **Opzione A — self-review dell'autore** (blindata dal prompt Developer): blocco `## Self-review RM-1..RM-3` in fondo al documento o nel commit message esteso, con asserzioni nel formato 4-righe, sotto-sezione `### Grep RM-2 eseguito`, fonti etichettate per livello. Senza blocco → niente commit.
- **Opzione B — probe-review del Reviewer**: l'autore scrive `READY_FOR_PROBE_REVIEW <path>` in `DEV_STATUS.md` e **non committa**; il Reviewer esegue audit ridotto sui 4 check (RM-1 / RM-2 / RM-3 / onestà claim→evidenza); commit solo con PASS.

**Matrice di sede della probe-review** (decisa dall'Orchestratore): documenti, CAP, audit statici → **Web**; risultati empirici, dump locali, riproduzioni DAPI → **CLI**; script di parsing/decoder e fatti chiusi da ri-provare → **entrambe** (pipeline 2 fasi Web→CLI).

---

## 7. Chiusura sessione PASS

| # | Track A (CAP-XX) | Track B (SPEC-FUNZ-NN) |
|---|---|---|
| 1 | Review PASS committata e pushata | idem |
| 2 | `DEV_STATUS.md` azzerato | idem |
| 3 | Documento + report su `origin/main` | idem |
| 4 | `00_indice.md` → Parte PASS con data+hash (**discriminatore N/N+1**) | **N/A** (indice non si tocca) |
| 5 | `ACTIVE_TASK.md` lasciato storico sul task chiuso | idem |
| 6 | `CARRYOVER.md` aggiornato con gli M emessi dalle review | idem (+ annotare M esistenti incardinati nella spec) |
| 7 | Riepilogo ad AC **+ prompt-template ready-to-paste** per la sessione successiva | Riepilogo ad AC; **nessun prompt-template automatico**: il track successivo lo decide AC |

Dopo il PASS l'Orchestratore **si ferma**: il Planner del task successivo gira in una **sessione nuova** aperta da AC.

---

## 8. File di stato — chi scrive cosa

| File | Scrive | Legge / azzera |
|---|---|---|
| `tasks/ACTIVE_TASK.md` | Planner / spec_planner (commit: **Orchestratore**); Orchestratore vi aggiunge i finding approvati | Tutti |
| `tasks/DEV_STATUS.md` | Developer (`READY_FOR_REVIEW` / `READY_FOR_PROBE_REVIEW <path>`) | Azzerato dall'**Orchestratore** a ogni ciclo |
| `tasks/CARRYOVER.md` | **Orchestratore** in chiusura (M-promemoria; namespace RACC-METODO separato) | Planner della sessione nuova (input obbligatorio) |
| `tasks/STATO_CORRENTE.md` | Single source of truth; sezioni con owner dedicati (vedi §7 del file stesso) | Tutti, prima azione di sessione |
| `tasks/QUESTIONS.md` | Planner (Q-XX); decisioni AC registrate come Q chiuse | Developer le eredita via task card |
| `docs/methodology_v2/00_indice.md` | Developer (→ IN REVIEW); Planner (→ PASS a chiusura). Track B: **intoccabile** | Orchestratore (discriminatore) |
| `reviews/REVIEW_*.md`, `reviews/PROBE_REVIEW_*_{web,cli}.md` | Reviewer (append per iterazione) | Orchestratore, AC, Developer |
| `reports/REPORT_*.md` | Developer (formato supervisore, 5 sezioni + tabella AC) | Reviewer, AC |

Disciplina: file di stato **single-writer**, mai push con working tree dirty su di essi; M-promemoria mai cancellati senza commit dedicato; dati sensibili (account, token) mai nei file di stato.

---

## 9. Promemoria operativi permanenti

- **Titolo-poi-prompt**: un messaggio breve di AC può essere solo il titolo dell'istruzione successiva — non si agisce sul titolo.
- **"Conclusa la parte X"** = PASS emesso + ruoli fermi + chiusura eseguita; non basta READY_FOR_REVIEW. Mai annotare l'indice a PASS in anticipo sulla re-review.
- **Cancellazioni**: prima di eliminare definitivamente, enumerare i file e far confermare ad AC la lista esatta.
- **Quarantena impianto B**: `Business Spec/OLD_NOT_USE_NOT_READ_FILES_MODEL_4_CANALI/` mai letta/citata (eccezione viva: `SPEC_HARNESS_EMPIRICO.md`); citabile solo il finding di audit. Impianto **A** è l'unico in vigore (REV-A1 `d8cbca3`).
- **DAPI**: DGo+Darwin devono essere aperti (gateway 10001/10003); TradingView Directa chiuso (conflitto datafeed).
- In assenza di AC, l'Orchestratore esegue **solo ciò che è già normato**; ai punti di decisione si ferma e attende — niente decisioni per analogia, niente override.
