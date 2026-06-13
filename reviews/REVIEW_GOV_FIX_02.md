# REVIEW — GOV-FIX-02 (delta governance tranche 2)

## VERDETTO: **CONDITIONAL**

Le patch elencate in `ISTRUZIONI_GOV-FIX-02.md` sono state applicate **fedelmente, una a una, senza aggiunte né omissioni**, e **tutti** i grep di VERIFICA delle istruzioni (Passi 2–9) confermano gli esiti attesi. Il backfill dei marcatori è **onesto** (hash reali per CAP-04..10, `<sha-da-confermare>` per CAP-01/02/03, nessun hash inventato).

Tuttavia il **CHECK DEDICATO G-12 fallisce sul punto che era il suo scopo**: lo spostamento del discriminatore dall'indice al marcatore è stato eseguito **solo sulle 4 ancore citate** dall'istruzione (P-12a/b/c/d), lasciando in `.claude/CLAUDE.md` **sei punti residui** che continuano a dichiarare l'indice come discriminatore della macchina a stati del Track A. Due di questi sono contraddizioni dirette con le righe patchate; uno è una **regressione funzionale** (il trigger di apertura sessione N+1 interroga un indice che l'Orchestratore, dopo la patch, non scrive più alla chiusura). Il difetto è **nella copertura delle ancore dell'istruzione**, non in una deviazione dell'esecutore — ma il risultato è una macchina a stati Track A internamente incoerente, e questo è esattamente il rischio di regressione che il CHECK G-12 doveva intercettare.

Nessun BUG REALE è una deviazione dall'istruzione; il BUG REALE è un **gap di progettazione dell'istruzione G-12** che produce incoerenza normativa nel documento risultante. Per la regola di mapping di `BASE_COMUNE.md` §4 (≥1 BUG REALE ⇒ non-PASS), il verdetto è CONDITIONAL.

---

## Header

- **Perimetro**: `git diff 8734bd3..a2d408f -- tasks/METODO.md .claude/ tasks/STATO_CORRENTE.md`
- **SHA_PRE** = `8734bd3`, **HEAD** = `a2d408f`
- **Sede**: CLI (working dir `C:\Users\AN\Documents\Projects\ga-zone-engine`)
- **Commit del delta**: `b8a2f16` (METODO), `2174320` (CLAUDE), `f7f5c0a` (developer+planner), `5e33914` (BASE_COMUNE), `a2d408f` (STATO_CORRENTE)
- **Diff-stat**: 6 file, +50 / −18 righe, 16 hunk. Nessun file fuori perimetro toccato. `docs/methodology_v2/CAP_*` e `00_indice.md` **non toccati** (freeze rispettato). `Business Spec/` non committato.

---

## (1) Corrispondenza patch-per-patch all'istruzione

| Patch | Finding | Esito | Note |
|---|---|---|---|
| P-08 | G-08 canone grafia in METODO | **OK** | Sostituzione 1 riga → 2 righe (canonica + DEPRECATA). METODO:120-121. |
| P-08b | G-08 grafia CLAUDE.md | **OK** | 3 occorrenze corrette (r.22, r.170, r.207), non 2: la terza (r.207, deposito RM-3) introdotta da GOV-FIX-01 P-13. Correzione di tutte e tre = **corretto** (soddisfa la VERIFICA-zero del Passo 3 e l'intento "grafia canonica nei file vivi"). |
| P-08c | G-08 grafia developer.md | **OK** | 2 occorrenze (r.20, r.150) → ESISTENTE. |
| P-13a | CARRYOVER registro M unico | **OK** | METODO:272. |
| P-13b | RACC-METODO-2 promossa | **OK** | METODO:212, prima di "## Convenzioni di update". |
| P-20 | Sblocco ruoli 2 livelli | **OK** | METODO:256. Ramo procedura-a-due-passi **mantenuto** (parentesi quadre non sostituite): coerente con esito test G-20 "deny NON flag-aware" (vedi §nota P-20). |
| P-22 | Backfill marcatori di forma | **OK** | METODO:266, dopo P-20, prima di "## Riferimenti". |
| P-12a | Condizione-4 chiusura Track A | **OK (testo)** | CLAUDE:141. Vedi CHECK G-12 per la coerenza col resto. |
| P-12b | Riga tabella stati (PASS emesso) | **OK (testo)** | CLAUDE:73, ora cerca il marcatore. |
| P-12c | Riga "NON fa mai" | **OK (testo)** | CLAUDE:225, ora cita il marcatore. |
| P-12d | Backfill CAP in STATO_CORRENTE | **OK** | Intestazione "(Track A + B …)"; 10 righe CAP aggiunte; hash onesti. |
| P-14a | F6 batch developer | **OK** | developer.md:27, marcatore `[B-N PROVVISORIO]`. |
| P-14b | Terminazione loop → AC | **OK** | developer.md:229, "decide il supervisore (AC)". |
| P-6 / G-11 | Identità planner.md | **OK** | planner.md:10, rimosso "(Orchestrator)". |
| P-7 / G-15 | Frontmatter documentale | **OK** | BASE_COMUNE.md:102. |
| P-17 | "5 sezioni" → "6 sezioni" | **OK** | CLAUDE:80. |
| P-18 | `--author=ANAC` rimosso | **OK** | CLAUDE:84, ora `git log --stat -3`. |
| P-19 | Router con fallback | **OK** | CLAUDE:37, "fermati e chiedi al supervisore". |
| P-21 / G-21 | Validator in precedenza | **OK** | METODO:248. Blocco precedenza GOV-FIX-01 presente (no STOP). |

**Conclusione (1)**: tutte le patch presenti, nessuna patch fuori-lista, nessuna riga extra. L'esecuzione è **fedele all'istruzione**. (Le 3 colonne "OK (testo)" per P-12a/b/c segnalano che il *testo della singola ancora* è corretto ma genera incoerenza col resto — vedi G-12.)

### Nota P-08b — terza occorrenza
L'istruzione stimava 2 occorrenze in CLAUDE.md; ne esistevano 3 (la terza a r.207, deposito RM-3, da GOV-FIX-01 P-13). Tutte e tre corrette. **Giudizio: corretto**. Lasciarne una avrebbe lasciato grafia deprecata in un file vivo, contro l'intento G-08, e avrebbe sporcato la VERIFICA-zero. La correzione di tutte e tre è coerente con la regola "vietata in nuovi documenti / file vivi".

### Nota P-20 — esito test G-20
P-20 conserva il ramo "procedura a due passi" tra parentesi quadre (METODO:256-264). Coerente con la premessa del mandato (decisione AC Passo 1: "deny NON flag-aware"). **Non riverificabile in questa review** se il test empirico 1.1 sia stato eseguito (l'esito vive in `ESITO_GOV-FIX-02.md`, fuori perimetro del diff): segnalo come **[da leggere nell'esito]**, non come finding.

---

## (3) Grep di VERIFICA (comando + output)

```
$ grep -n "grafia canonica" tasks/METODO.md
120:[CODICE-ESISTENTE r.NNN]      — citazione di decoder già in repo (grafia canonica)
$ grep -n "registro M unico" tasks/METODO.md            → 272 (1)  OK
$ grep -n "RACC-METODO-2 (promossa" tasks/METODO.md     → 212 (1)  OK
$ grep -n "Sblocco dei file di ruolo" tasks/METODO.md   → 256 (1)  OK
$ grep -n "Backfill dei marcatori di forma" tasks/METODO.md → 266 (1)  OK
```
Passo 2: 1 ciascuno, tutti prima di "## Riferimenti" (r.270). **MATCH.**

```
$ grep -rn "CODICE-EXISTENTE" .claude/ tasks/METODO.md
tasks/METODO.md:121:[CODICE-EXISTENTE r.NNN]  — DEPRECATA: ... accettata SOLO in lettura ...
$ grep -rn "CODICE-EXISTENTE" docs/methodology_v2/ | wc -l
0
```
Passo 3: **solo** la riga DEPRECATA in METODO; ZERO in CLAUDE.md/developer.md; ZERO nei CAP frozen (il residuo atteso "EXISTENTE nei CAP" risulta **vuoto** — i CAP non contenevano la grafia deprecata, dato di fatto, non un problema). **MATCH.**

```
$ grep -n "CAP-XX: CHIUSO PASS\|nuovo discriminatore meccanico" .claude/CLAUDE.md  → 73,141,225 (≥1)  OK
$ grep -rn "00_indice.md.*discriminatore" .claude/CLAUDE.md                         → 141 (atteso 0!) ── vedi sotto
```
Passo 4: il primo grep MATCH; **il secondo grep restituisce 1 (r.141), non 0 come atteso dall'istruzione**. La riga 141 è la condizione-4 patchata, dove "00_indice.md" e "discriminatore" coabitano ma in negazione ("non è più il discriminatore"): è un **falso positivo** della VERIFICA, non una violazione su quella riga. **MA** lo stesso grep è troppo debole per stanare i residui reali (cattura solo "indice…discriminatore" sulla stessa riga; manca r.63 dove "discriminatore" precede "00_indice.md", e r.34/r.67/r.130/r.150/r.155). Vedi CHECK G-12.

```
$ grep -n "B-N PROVVISORIO" .claude/agents/developer.md            → 27 (1)  OK
$ grep -n "decide il supervisore (AC)" .claude/agents/developer.md → 229 (1) OK
$ grep -n "QUESTIONS.md. Non improvvisare" .claude/agents/developer.md → (0)  OK
```
Passo 5: 1 / 1 / 0. **MATCH.**

```
$ grep -n "PLANNER (Orchestrator)" .claude/agents/planner.md        → (0)  OK
$ grep -n "subagente, NON l'Orchestratore" .claude/agents/planner.md → 10 (1) OK
```
Passo 6: 0 / 1. **MATCH.**

```
$ grep -n "Frontmatter documentale" .claude/BASE_COMUNE.md → 102 (1)  OK
```
Passo 7: 1. **MATCH.**

```
$ grep -n "le 6 sezioni del formato supervisore" .claude/CLAUDE.md → 80 (1)  OK
$ grep -n "author=ANAC" .claude/CLAUDE.md                          → (0)    OK
$ grep -n "fermati e chiedi al supervisore" .claude/CLAUDE.md      → 37 (1)  OK
```
Passo 8: 1 / 0 / 1. **MATCH.**

```
$ grep -n "Il ruolo .validator." tasks/METODO.md → 248 (1)  OK
```
Passo 9: 1. **MATCH.**

**Conclusione (3)**: tutte le VERIFICA delle istruzioni passano. L'unico scostamento è il *valore atteso* del secondo grep del Passo 4 (atteso 0, reale 1, ma falso positivo); più grave è che quel grep **non è in grado di garantire ciò che dichiara di garantire** (vedi G-12).

---

## Esito CHECK G-12 (sezione dedicata)

Il CHECK G-12 è il cuore del mandato. Esito: **FALLITO su (a), (b)/(c) parzialmente, (d); PASS su (e).**

### (a) Ogni occorrenza di "discriminatore" punta al marcatore? ZERO ancora all'indice?

`grep -n "discriminatore" .claude/CLAUDE.md` → 5 occorrenze (r.34, r.45, r.63, r.141, r.225). Aggiungendo le menzioni di indice-come-spia senza la parola "discriminatore" letterale (r.67, r.130, r.150, r.155), il quadro è:

| Riga | Testo (sintesi) | Stato |
|---|---|---|
| 34 | "(**discriminatore `00_indice.md`**, 7 condizioni…)" descrive le sezioni Track A | **RESIDUO — indice = discriminatore** |
| 45 | Track B: discriminatore in STATO_CORRENTE/ACTIVE_TASK | OK (Track B, pre-esistente) |
| 63 | **"Il discriminatore tra sessione N e N+1 è lo stato di `00_indice.md`: se l'indice riporta già Parte X come PASS … siamo in N+1."** (definizione introduttiva della macchina) | **RESIDUO GRAVE — contraddice r.73/141/225** |
| 67 | 1ª riga tabella: trigger apertura N+1 = "`00_indice.md` riporta già Parte X come PASS" | **RESIDUO GRAVE — regressione funzionale (vedi sotto)** |
| 73 | (patchata) trigger chiusura N = marcatore in STATO_CORRENTE | OK (patch P-12b) |
| 130 | File di stato: "`00_indice.md` … **Discriminatore sessione N vs N+1** nella macchina a stati" | **RESIDUO — indice = discriminatore** |
| 141 | (patchata) condizione-4 = marcatore; indice = doc leggibile aggiornato dal Planner in N+1 | OK (patch P-12a) |
| 150 | prompt-template: "00_indice.md riporta Parte X come PASS" (stato iniziale N+1) | RESIDUO minore (coerente solo se Planner ha già scritto l'indice; non più garantito alla chiusura N) |
| 155 | autocheck N+1: "se una condizione è mancata (**in particolare la 4 sull'indice**)" | **RESIDUO — la condizione-4 ora è il marcatore, non l'indice** |
| 225 | (patchata) "NON fa mai: usa il marcatore … come discriminatore" | OK (patch P-12c) |

**Risposta (a): NO.** Restano almeno **6 punti** (r.34, r.63, r.67, r.130, r.150, r.155) che ancora trattano l'indice come spia/discriminatore della macchina Track A. L'istruzione ha coperto solo le 3 ancore "discriminatore" esplicite (P-12a/b/c) + il backfill; non ha coperto la definizione introduttiva (r.63), il trigger di apertura N+1 (r.67), la voce File-di-stato (r.130), il prompt-template (r.150) e l'autocheck (r.155).

### (b) Le 7 condizioni di chiusura Track A sono internamente coerenti? chi-scrive-cosa univoco?

**Parzialmente.** La condizione-4 (r.141) è ora coerente e univoca su *chi scrive cosa*: l'Orchestratore scrive il marcatore in STATO_CORRENTE; il Planner aggiorna l'indice in N+1; l'Orchestratore non scrive nei CAP/indice. **MA** l'autocheck delle 7 condizioni (r.155) dice ancora "in particolare la 4 sull'indice" — mentre la 4 ora è il marcatore. Incoerenza interna fra condizione-4 (marcatore) e il suo stesso autocheck (indice).

### (c) La riga tabella "PASS appena emesso" cerca il marcatore, non l'indice?

**SÌ** (r.73, patchata, cerca `CAP-XX: CHIUSO PASS` in STATO_CORRENTE). Questa metà è corretta. **Ma la metà gemella — la 1ª riga della stessa tabella (r.67), che rileva l'apertura N+1 — cerca ancora l'indice.** Le due righe della stessa macchina usano ora discriminatori diversi.

### (d) Contraddizione residua "Planner aggiorna l'indice in N+1" vs altre righe?

**SÌ, ed è la più grave (regressione funzionale).** Catena:
1. Chiusura sessione N (r.141 patchata): l'Orchestratore scrive il marcatore in STATO_CORRENTE e **NON tocca l'indice**.
2. Apertura sessione N+1, trigger per chiamare il Planner (r.67, NON patchata): richiede che **`00_indice.md` riporti già Parte X come PASS**.
3. Ma l'indice è aggiornato dal Planner **come primo atto di N+1** (r.141) — cioè *dopo* che il trigger lo avrebbe dovuto far partire.

⇒ All'avvio di N+1 l'indice **non** riporterà ancora "Parte X = PASS" (l'Orchestratore non lo scrive più in chiusura), quindi il trigger di r.67 è **FALSO** e nessuna riga della tabella fa partire il Planner per CAP-(X+1). La macchina Track A, dopo la patch additiva, ha **perso il proprio trigger di apertura del capitolo successivo**. Questa è la regressione che il CHECK G-12 doveva intercettare: **confermata**.

### (e) Backfill senza hash inventati?

**SÌ — PASS.** CAP-01/02/03 = `<sha-da-confermare>` (onesto: la mappa Parte→CAP per i primi capitoli è ambigua e Parte IV condivide `a1625df` con Parte II). CAP-04..10 confrontati con `00_indice.md` e con `git log`: **tutti reali e combacianti**:

| Marcatore | Backfill | Indice (Parte) | `git log -1` | Match |
|---|---|---|---|---|
| CAP-04 | a1625df | a1625df (Parte II) | [CAP-04 v3 Review] PASS | ✓ |
| CAP-05 | 72e00df | 72e00df (Parte V) | [REVIEWER] CAP-05 v4 PASS | ✓ |
| CAP-06 | d3f029d | d3f029d (Parte VI) | [REVIEWER] CAP-06 v2 PASS | ✓ |
| CAP-07 | b27c1e3 | b27c1e3 (Parte VII) | [REVIEWER] CAP-07 v2 PASS | ✓ |
| CAP-08 | 6ba6186 | 6ba6186 (Parte 8) | [REVIEWER] CAP-DATA-01 v2 PASS | ✓ |
| CAP-09 | 86425a7 | 86425a7 (Parte 9) | [REVIEW] CAP-DATA-02 v2 PASS | ✓ |
| CAP-10 | 48171e4 | 48171e4 (Parte 10) | [REVIEW] CAP-DATA-03 v2 PASS | ✓ |

---

## (2) Nuove contraddizioni fra documenti normativi

- **Intra-CLAUDE.md (Track A state machine)**: contraddizioni r.63/r.67/r.130/r.155 vs r.73/r.141/r.225 (vedi G-12). Questa è **la** contraddizione introdotta dalla tranche.
- **METODO ↔ CLAUDE**: nessuna nuova contraddizione. P-20 (METODO:256) e l'identità Orchestratore in CLAUDE coerenti; P-21 validator coerente con BASE_COMUNE §9 e con il divieto validator in CLAUDE.
- **BASE_COMUNE ↔ ruoli**: P-7/G-15 (BASE_COMUNE:102) e P-6/G-11 (planner.md:10) coerenti ("Planner non committa" = disciplina procedurale in entrambi).
- **METODO ↔ developer.md**: P-08 (METODO canone ESISTENTE) e P-08c (developer ESISTENTE) coerenti; F6 batch (developer:27) non confligge con BASE_COMUNE.
- **STATO_CORRENTE ↔ CLAUDE/Track B**: marcatori CAP additivi coerenti con la macchina Track B già descritta in CLAUDE (r.45/57).

Nessuna contraddizione cross-file nuova **oltre** quella intra-CLAUDE del Track A.

---

## Tabella "Classificazione per il supervisore"

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|---|---|---|---|
| 1 | Trigger apertura sessione N+1 interroga `00_indice.md` ("riporta già Parte X come PASS") ma l'Orchestratore non scrive più l'indice in chiusura (r.141) → la macchina Track A perde il trigger di apertura del capitolo successivo (regressione funzionale) | `.claude/CLAUDE.md:67` | **BUG REALE** | **Sì** (richiede decisione AC sull'ancora: il fix esce dalle ancore dell'istruzione, quindi serve mandato AC) |
| 2 | Definizione introduttiva della macchina a stati dichiara ancora "il discriminatore … è lo stato di `00_indice.md`" — contraddice condizione-4 (r.141), riga tabella (r.73) e "NON fa mai" (r.225) | `.claude/CLAUDE.md:63` | **BUG REALE** | **Sì** (stessa decisione AC) |
| 3 | Autocheck delle 7 condizioni cita "in particolare la 4 sull'indice" ma la condizione-4 ora è il marcatore in STATO_CORRENTE | `.claude/CLAUDE.md:155` | **BUG REALE** | **Sì** (stessa decisione AC) |
| 4 | Voce "File di stato": `00_indice.md` ancora etichettato "**Discriminatore sessione N vs N+1** nella macchina a stati" | `.claude/CLAUDE.md:130` | **BUG REALE** | **Sì** (stessa decisione AC) |
| 5 | Descrizione sezioni Track A: "(discriminatore `00_indice.md`, …)" | `.claude/CLAUDE.md:34` | RISCHIO PEGGIORAMENTO | In attesa decisione AC (cosmetico-descrittivo, ma alimenta la confusione) |
| 6 | Prompt-template N+1: "00_indice.md riporta Parte X come PASS" come stato iniziale — vero solo se il Planner ha già scritto l'indice; non più garantito alla chiusura N | `.claude/CLAUDE.md:150` | RISCHIO PEGGIORAMENTO | In attesa decisione AC |
| 7 | VERIFICA Passo 4 (`grep "00_indice.md.*discriminatore"`) dichiara atteso 0 ma è troppo debole per garantire l'assenza di residui (non cattura ordinamento inverso né righe senza "discriminatore" letterale) — falso senso di sicurezza dell'istruzione | (meta, `ISTRUZIONI_GOV-FIX-02.md:205-207`) | NEUTRO | No (osservazione di processo, non file di repo) |

**Nota di metodo per il supervisore**: i finding #1–#6 NON sono deviazioni dell'esecutore (che ha rispettato regola 2 "nessun fix creativo" e le ancore date). Sono un **gap di copertura delle ancore dell'istruzione G-12**. Il fix corretto è una **G-12-bis** che reindirizzi r.34/63/67/130/150/155 al marcatore (o ripristini l'indice come spia di apertura, scegliendo UN solo discriminatore per entrambe le metà della macchina). Poiché esce dalle ancore di GOV-FIX-02, richiede mandato AC, non auto-fix.

---

## Applicazione RM-1 a me stesso

| Mia asserzione | Prova / esito | Alternative escluse |
|---|---|---|
| "Tutte le patch P-08..P-21 applicate fedelmente" | Letto `ISTRUZIONI_GOV-FIX-02.md` integrale + diff `8734bd3..a2d408f` riga-per-riga + 18 grep VERIFICA eseguiti, tutti MATCH | Esclusa "patch mancante/extra": diff-stat = 6 file attesi, 16 hunk tutti mappati a un'istruzione; 0 hunk orfani |
| "r.67/63/130/155 contraddicono le righe patchate" | Read diretto di CLAUDE.md r.61-67, r.130, r.141, r.155, r.225 + grep "discriminatore" e "00_indice" | Esclusa "coerenza additiva intenzionale": l'istruzione G-12 dichiara esplicitamente "non è più lui a governare la macchina" → r.63/67/130 che lo chiamano discriminatore sono incoerenti col mandato, non additive |
| "Regressione funzionale del trigger N+1 (finding #1)" | Catena logica r.141 (Orch non scrive indice) → r.67 (trigger richiede indice) → r.141 (indice scritto dal Planner solo in N+1): trigger falso all'avvio N+1 | **Empirico-CLI: N/A** — è incoerenza testuale di un documento normativo, verificabile per sola lettura, nessun probe DAPI necessario. Non ho eseguito il GA né simulato la macchina: l'asserzione è una deduzione dal testo, etichettata come tale |
| "Backfill hash reali e combacianti CAP-04..10" | `git log -1 --oneline <h>` per i 7 hash (tutti risolti a commit Review PASS) + confronto 1:1 con `00_indice.md` | Esclusa "hash plausibile ma di altro commit": ogni hash risolve a un commit il cui messaggio è "[REVIEW(ER)] CAP-NN … PASS" della Parte corrispondente |
| "CAP-01/02/03 correttamente `<sha-da-confermare>`" | Indice: Parte I = `fc7531b`/FIX-04 (non review-hash pulito), Parte III = `ee0b2ee` (doc, non review), Parte IV = `a1625df` (condiviso con Parte II) → mappa Parte→CAP ambigua per i primi 3 | Esclusa "hash ricavabile con certezza": la corrispondenza CAP-01/02/03 ↔ review-PASS-hash non è univoca dall'indice; `<sha-da-confermare>` è la scelta onesta |
| "VERIFICA Passo 3 EXISTENTE-nei-CAP = vuoto (0)" | `grep -rn "CODICE-EXISTENTE" docs/methodology_v2/ \| wc -l` → 0 | Non un'omissione dell'esecutore: i CAP semplicemente non contenevano la grafia deprecata. Dato di fatto, non finding |

**Limiti dichiarati della mia review**: (1) non ho letto `ESITO_GOV-FIX-02.md` (fuori dal perimetro del diff): l'esito del test empirico G-20 (1.1) e il ripristino settings.json/AGENTS_UNLOCK (Passo 14) restano **[da leggere nell'esito]**, non verificati da me. (2) Non ho verificato che i commit siano su `origin/main` (mandato = audit del delta locale, non dello stato push). (3) La classificazione dei finding #1–#4 come BUG REALE riflette l'incoerenza normativa risultante; se il supervisore ritiene che la macchina Track A non verrà esercitata prima di una G-12-bis, può declassarli — ma il documento resta auto-contraddittorio finché non corretti.
