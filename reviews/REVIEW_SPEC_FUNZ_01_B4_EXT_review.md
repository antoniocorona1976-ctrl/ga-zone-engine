# REVIEW — SPEC-FUNZ-01-B4-EXT (Estensione consegna CAP_06 PVI Cap.29)

> **Perimetro**: SOLO l'estensione "consegna" appesa a `SPEC_FUNZ_01_B4.md` (sezione "# Estensione consegna — CAP_06 PVI (Cap.29)", righe :379–:487, commit `b954f17`): 11 nuovi requisiti (8 `B4-R-33..40` + 3 `B4-NFR-05..07`). La parte B4 base (CAP_02 Cap.8-9, PASS `c3be05e`) **non** è ri-auditata.
> **Sede**: CLI (GOV-SURFACES-01). Audit documentale no-DAPI, divieto CLI (nessuna probe). Lista "Empirico-CLI da verificare" attesa VUOTA.
> **Modalità**: CAP-review piena adattata al non-CAP, due giri ostili. Floor citazioni 100% sui 11 nuovi requisiti.
> **Letture confermate**: `tasks/METODO.md` (RM-1..RM-4 + RACC-METODO-2), `.claude/BASE_COMUNE.md`, `.claude/agents/spec_reviewer.md`, `tasks/ACTIVE_TASK.md` (card B4-EXT §0/§1/§2/§4).

---

## ITERAZIONE 1 — verdetto: **CONDITIONAL**

**Motivazione**: 1 BUG REALE di tracciabilità (B4-R-37: unica citazione `:190` punta all'header di sezione 29.3, non al paragrafo `:192` che contiene il costrutto affermato "no edit/no append/`signal_id`"). Per il mapping verdetto↔classificazione (BASE_COMUNE §4), ≥1 BUG REALE ⇒ non-PASS. Tutto il resto (AC-EXT-1/2/3, confine consegna/runtime, cecità, copertura piena consegna-vs-v2, no-duplicazione) è solido. Il difetto è circoscritto e a basso costo di fix (ri-puntare la citazione).

---

## 1. Esito AC-EXT-1/2/3 + AC-G pertinenti

| AC | Esito | Evidenza (file:riga) |
|---|---|---|
| **AC-EXT-1** Recupero esplicito NFR-6.1 + R-6.4 | **OK** | NFR-6.1 (mobile-first) → `B4-NFR-05/06/07` (SPEC :392–:407), recupero dichiarato in E.0 (:388) e titolo E.1 (:392). R-6.4 (3 notifiche) → `B4-R-33/34` (:411–:417) + le tre notifiche `B4-R-35/36/38` (:421/:428/:440), recupero dichiarato E.0 (:388) e titolo E.2 (:409). |
| **AC-EXT-2** Confine consegna/runtime | **OK** | Nessuno degli 11 requisiti tocca Cap.27 (pipeline/inference/EGARCH) né Cap.28 (anti-doppio/non-refresh/tie-break/logging/determinismo). Tutte le citazioni cadono in Cap.29 (:146/:148/:152/:154/:190/:192/:220/:223/:225/:230/:232) — verificato (vedi §2). Nota di rinvio E.7 (:474–:483) rinvia esplicitamente Cap.27 + Cap.28 intero a B5. Idempotenza di lettura di Cap.29.4 (`:218`/`:221`) riconosciuta già-B4 (Cap.9.4) e NON ri-consolidata (E.7 :483). Nessuno scope creep. |
| **AC-EXT-3** Continuità ID + no-duplicazione | **OK** | ID continui senza collisione: B4 base arriva a NFR-04 / R-32 / CN-14; estensione parte da NFR-05 / R-33, biunivoca con le 11 righe della matrice E.6 (:457–:468). 9 voci di Cap.9.2 NON ri-elencate (premessa esplicita in B4-NFR-06 :403 ed E.1 :394). Notifica `trigger_event` di Cap.9.5 NON duplicata (premessa "già-B4 §9 B4-R-28/CN-12" in B4-R-36 :431). State machine / stati terminali B3 NON ri-derivati (premessa in B4-R-38 :443 / B4-R-39 :448). |
| AC-G1 Atomicità (N1) | **OK** | Mobile-first scisso in 3 NFR distinti (principio :396 / cosmetico-non-contratto :400 / vincoli-scroll :405). 3 notifiche scisse in esistenza-insieme (B4-R-33 :411) + no-refresh (B4-R-34 :415) + una per momento (R-35/36/38) + contenuto terminale (R-39 stato :445, R-40 R_gross :450). Ogni requisito = 1 proposizione verificabile. |
| AC-G3 Valore | **OK** | Ogni requisito porta "*Valore operativo*" dichiarato (es. :398, :413, :452). Nessun invariante puro nell'estensione. |
| AC-G6 Grafia | **OK** | Etichette `[DOC-INTERNO CAP_06_parte_VI.md:<riga>]` in grafia canonica; nessuna grafia deprecata `[CODICE-EXISTENTE]`. |
| AC-G8 Cecità | **OK** | Vedi §5. Nessun ID v2/B1/B2/B3 importato; nessuna prosa v2 copiata; i riferimenti "NFR-6.1/R-6.4 della v2" sono nomi-bersaglio depositati nella card (autoritativa), non frutto di lettura della v2. |
| AC-G10 Matrice | **OK** | Matrice E.6 (:457–:468) 11 righe ID\|proposizione\|citazione\|valore + conteggi (:470 estensione = 8R+3NFR; :472 totale B4 = 61). Coerente con i requisiti. Nota di rinvio E.7 presente. |
| **AC-G7** Floor citazioni 100% | **PARZIALE** | Vedi §2: 1 citazione non risolve al costrutto (B4-R-37, BUG REALE) + 3 imprecisioni header→paragrafo (MIGLIORA PERFORMANCE). |

---

## 2. Floor citazioni 100% — ri-verifica token-per-token sui 11 nuovi requisiti

Convenzione del file CAP_06: ogni **paragrafo** è una riga numerata; gli header `### 29.x` sono righe a sé, separate dal paragrafo di contenuto da una riga vuota. Quindi citare un header (`:154`, `:190`, `:223`) ≠ citare il paragrafo di contenuto.

| Requisito | Citazioni nel doc | Riga del costrutto nel CAP | Esito |
|---|---|---|---|
| B4-NFR-05 | `:146` | :146 (29.1 — "il payload formale … viene **rappresentato** in un layout mobile-first ottimizzato per lettura su schermo cellulare in condizioni di attenzione limitata"; profilo "esegue manualmente da cellulare in modo discontinuo") | **RISOLVE** |
| B4-NFR-06 | `:146`, `:154` | "nessun campo nuovo / né omesso; payload formale (immutabile) vs rappresentazione mobile (cosmetica)" è a **:148** (+ ripreso :156/:172). `:146` supporta solo "rappresenta lo stesso payload"; `:154` è l'header 29.2 (vuoto di costrutto). | **PARZIALE** (nucleo "invarianza del contratto" risolve a :148, non a :146/:154) |
| B4-NFR-07 | `:152` | :152 ("**senza scroll orizzontale**", "contenuto critico … entro la prima schermata", larghezza schermi mobile) | **RISOLVE** (preciso) |
| B4-R-33 | `:220` | :220 ("il canale pubblica **esattamente 3 notifiche standard per segnale**: (i) emissione; (ii) trigger_event…; (iii) transizione a stato terminale") | **RISOLVE** |
| B4-R-34 | `:220` | :220 ("Tra una notifica e la successiva … no polling, no refresh") | **RISOLVE** |
| B4-R-35 | `:220`, `:154` | `:220` supporta "1ª = emissione (i)". "pubblica le 9 voci nel layout mobile-first" risolve a :156/:172; `:154` è header 29.2. | **PARZIALE** (nucleo coperto da :220; `:154` header non porta il costrutto) |
| B4-R-36 | `:220`, `:190` | `:220` supporta "2ª = trigger_event (ii)". "messaggio separato al raw touch" risolve a **:192**; `:190` è header 29.3. | **PARZIALE** (nucleo coperto da :220; `:190` header non porta il costrutto) |
| **B4-R-37** | **`:190`** (sola) | Costrutto "non modifica il messaggio di emissione (**no edit, no append**) … `signal_id` esplicito" è a **:192**. `:190` è l'header di sezione "### 29.3 Notifica trigger_event come messaggio separato": NON contiene il costrutto. **Nessuna** citazione concomitante a salvare. | **NON RISOLVE → BUG REALE** |
| B4-R-38 | `:220`, `:223`, `:225` | `:220` supporta "3ª = transizione terminale (iii)"; `:225` ("Alla transizione … da active a uno degli stati terminali … pubblica un messaggio di chiusura"). `:223` è header (ridondante ma innocuo, perché :225 copre). | **RISOLVE** (via :220 + :225) |
| B4-R-39 | `:230` | :230 ("**stato terminale finale**, uno dei 6 di Cap.7.1") | **RISOLVE** |
| B4-R-40 | `:232` | :232 ("**$R_{gross}$** … vuoto o `n/a` per i segnali non eseguiti") | **RISOLVE** |

**Sintesi floor**: 7/11 risolvono pienamente; 3 parziali (header→paragrafo, ma nucleo supportato da citazione concomitante); **1 non risolve** (B4-R-37, unica citazione = header).

---

## 3. Confronto-copertura — perimetro di consegna PIENO (CAP_02 Cap.8-9 + CAP_06 Cap.29) vs perimetro di consegna v2 (Sez.5+6), con mappa aggiornata come autorità di partizione

Autorità di partizione: `PROPOSTA_SUDDIVISIONE_SPEC_v2.md` riga :106 (B4 = Cap.8-9 + Cap.29) + nota :114 (scostamento Opzione 1 autorizzato AC, Cap.27-28 → B5). Coerente con la card.

Requisiti di consegna v2 (Sez.6 "Consegna su Telegram", matrice v2 :560–:568), classificati per fonte e copertura:

| Req. v2 | Fonte (matrice v2) | Copertura nel perimetro B4 pieno |
|---|---|---|
| R-6.1 (9 voci) | CAP_02 Cap.9 / CAP_06 Cap.29 | **già B4 base** (contratto 9 voci, Cap.9.2) |
| R-6.2 (Δt/T_touch non figurano) | CAP_02 Cap.9 | **già B4 base** |
| R-6.3 (no istruzioni gestione attiva) | CAP_02 Cap.9 / CAP_01 | **già B4 base** |
| **R-6.4 (3 notifiche standard)** | CAP_06 Cap.29 / CAP_02 Cap.9 | **RECUPERATO** (B4-R-33/34 + 35/36/38) ✓ |
| R-6.5 (anti-duplicato `signal_id`) | CAP_02 Cap.9 / CAP_06 Cap.29 | **già B4 base** (Cap.9.4); idempotenza di lettura Cap.29.4 riconosciuta già-B4 (E.7 :483), non gap |
| R-6.6 (messaggio separato, no-edit) | CAP_02 Cap.9 / CAP_06 Cap.29 | **già B4 base** (invariante no-edit); ribadito a livello consegna in B4-R-37 |
| R-6.7 (retry/backoff) | CAP_02 Cap.9 | **già B4 base** |
| **NFR-6.1 (mobile-first)** | CAP_06 Cap.29 | **RECUPERATO** (B4-NFR-05/06/07) ✓ |
| NFR-6.2 [B-1] (latenza L≤L_max) | CAP_02 Cap.9 / CAP_07 Cap.31 | **NON fondata su CAP_06 Cap.29** nella matrice v2 → fuori dal perimetro-fonte di questa estensione; resta tracciata via NFR-6.2 (B4 base / B-1 provvisorio). **Non è un gap.** |

**Esito copertura**: i **soli** requisiti di consegna v2 fondati su CAP_06 Cap.29 e non ancora coperti dal B4 base erano **R-6.4 e NFR-6.1** → **entrambi recuperati**. Nessun altro residuo di consegna v2 caduto. Nessuno scope creep runtime (Cap.27/Cap.28 esclusi e rinviati a B5).

**Nota sulla latenza (non-finding, segnalazione)**: Cap.29.1 `:150` contiene il "Vincolo di latenza Telegram (qualitativo)" con L_max=30 s provvisorio. L'estensione non lo recupera. È **corretto**: la matrice v2 fonda NFR-6.2 su CAP_02 Cap.9 + CAP_07 Cap.31 (non su CAP_06 Cap.29), e la card B4-EXT perimetra i bersagli a "solo NFR-6.1 + R-6.4". La latenza è già tracciata altrove (NFR-6.2, `[B-1 PROVVISORIO]`, mappa :181). Nessun marcatore `[B-1 PROVVISORIO]` è dovuto in questa estensione perché nessun suo requisito dipende dal blocco B-1.

---

## 4. Esito 3 punti di confine fine (boundary-check Orchestratore — non vincolanti sul verdetto)

| Punto | Esito | Evidenza |
|---|---|---|
| **B4-R-40** (R_gross veicola ≠ calcola ≠ logga) | **OK, no scope creep** | B4-R-40 (:450–:452) afferma che la notifica **veicola** R_gross alla consegna; non ri-definisce il calcolo (Cap.7.3 fill virtuale = B3) né il log di chiusura (Cap.10.4 = B5). La riga-fonte :232 attribuisce calcolo a Cap.7.3 e uso-log a Cap.10.4, ma il requisito si limita al "cosa veicola la notifica". |
| **B4-R-39** (stati terminali = premessa B3, non ri-derivati) | **OK** | B4-R-39 (:445–:448) cita "uno fra i sei stati terminali" con nota esplicita "l'**insieme** dei sei stati terminali è definito in B3 (Cap.7); qui si consolida solo che la notifica li **veicola**". Nessuna ri-derivazione della state machine. |
| **B4-R-35/36** (notifiche emissione/trigger non duplicano Cap.9.2/Cap.9.5) | **OK** | B4-R-35 (:424) cita la pubblicazione + contratto 9 voci come "già B4 §7", consolida solo il ruolo di 1ª notifica. B4-R-36 (:431) cita la pubblicazione `trigger_event` come "già-consolidata in B4 §9 B4-R-28/CN-12 (Cap.9.5)" e l'evento come premessa B3, consolida solo il ruolo di 2ª notifica. Nessuna duplicazione. |

---

## 5. Audit cecità (AC-G8)

- Grep di contaminazione sulla sezione di estensione (:379–:487) per pattern `R-6.|NFR-6.|R-5.|B1-|B2-|B3-|_v1_storico|SPEC_FUNZ_01.md|Sezione 6|valore di prodotto|risk manager bancario`: le **uniche** occorrenze sono `NFR-6.1`/`R-6.4` nelle note di recupero esplicito (E.0 :388, titoli E.1 :392 / E.2 :409) — **dovute** da AC-EXT-1 (marcare i bersagli recuperati). Nessuna prosa v2 copiata, nessun ID v2/B1/B2/B3 importato nei requisiti.
- I nomi-bersaglio "NFR-6.1 / R-6.4 della v2" provengono dalla **card B4-EXT** (autoritativa, §AC-EXT-1), non da lettura della v2: legittimo sotto cecità.
- ID auto-assegnati continui (NFR-05+/R-33+), nessuna collisione col B4 base.
- **Limite dichiarato** (RM-1 a me stesso): attesto l'assenza di tracce greppabili e di ID importati; un'eco lessicale di prosa che non matchi i pattern non è esclusa in assoluto — ma il confronto manuale della prosa dei requisiti con la v2 Sez.6 (:244–:285) non ha rilevato frasi ricalcate (la prosa dell'estensione è derivata dal lessico di Cap.29, es. "attenzione limitata", "self-contained", "no polling/refresh", che sono del CAP-fonte, non della v2).

**Esito cecità: OK.**

---

## 6. Problemi

### Bloccanti
Nessuno.

### Non-bloccanti
- **NB-1 (BUG REALE)** — `B4-R-37` (SPEC :433–:436): l'**unica** citazione `[DOC-INTERNO CAP_06_parte_VI.md:190]` punta all'**header** di sezione `### 29.3 Notifica trigger_event come messaggio separato`. Il costrutto affermato dal requisito — "non modifica il messaggio di emissione (no edit, no append)" e "`signal_id` esplicito" — è nel **paragrafo di contenuto a `:192`**, non a `:190`. La citazione non risolve al costrutto e non c'è citazione concomitante a sostenerlo. Fix: sostituire/aggiungere `:192`. (Il report Developer in AC-G7 dichiara `:190` come "risolve token-per-token" mappandolo a B4-R-36/37: la mappatura all'header è imprecisa per la convenzione paragrafo-riga del file.)

### Osservazioni minori
- **OM-1 (MIGLIORA PERFORMANCE)** — `B4-NFR-06` (:401) cita `:146`+`:154`, ma il nucleo "nessun campo nuovo/omesso; payload formale (immutabile) vs rappresentazione mobile (cosmetica)" risolve a **`:148`**. Consigliato aggiungere `:148`. Affermazione comunque parzialmente supportata da `:146` ("rappresentato in layout mobile-first").
- **OM-2 (MIGLIORA PERFORMANCE)** — `B4-R-35` (:422) cita `:154` (header 29.2); la parte "pubblica le 9 voci nel layout" risolve a `:156`/`:172`. Nucleo "1ª = emissione" coperto da `:220`. Consigliato puntare `:156` invece di / oltre `:154`.
- **OM-3 (MIGLIORA PERFORMANCE)** — `B4-R-36` (:429) cita `:190` (header) per "messaggio separato al raw touch" che risolve a `:192`. Nucleo "2ª = trigger_event" coperto da `:220`. Stesso fix di NB-1 (puntare `:192`).
- **OM-4 (NEUTRO)** — `B4-R-38` (:441) cita `:223` (header) in aggiunta a `:220`+`:225`: ridondante ma innocuo (il costrutto è già coperto da `:225`). Nessuna azione necessaria.

---

## 7. Tabella "Classificazione per il supervisore"

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|------------------------|
| 1 | B4-R-37: unica citazione `:190` = header 29.3, costrutto "no edit/no append/signal_id" è a `:192` → non risolve | SPEC_FUNZ_01_B4.md:433–:436 | **BUG REALE** | **Sì (obbligatorio)** |
| 2 | B4-NFR-06: `:146`/`:154` per "invarianza del contratto" che risolve a `:148` | SPEC_FUNZ_01_B4.md:401 | MIGLIORA PERFORMANCE | In attesa decisione AC |
| 3 | B4-R-35: `:154` (header) per "pubblica 9 voci nel layout" che risolve a `:156` | SPEC_FUNZ_01_B4.md:422 | MIGLIORA PERFORMANCE | In attesa decisione AC |
| 4 | B4-R-36: `:190` (header) per "messaggio separato al raw touch" che risolve a `:192` | SPEC_FUNZ_01_B4.md:429 | MIGLIORA PERFORMANCE | In attesa decisione AC |
| 5 | B4-R-38: `:223` (header) ridondante (costrutto già in `:225`) | SPEC_FUNZ_01_B4.md:441 | NEUTRO | No |

> Nota di efficienza per il supervisore: i finding 1, 3, 4 sono lo **stesso pattern** (citazione all'header di sottosezione invece che al paragrafo di contenuto immediatamente successivo). Se si manda il Developer per il BUG REALE (#1), conviene fargli sistemare in un colpo anche #2/#3/#4 (header→paragrafo) per chiudere il floor al 100% pulito. Sono micro-fix di puntatore, nessun cambio di contenuto/scope.

---

## 8. Applicazione RM-1 a me stesso

- **VERIFICA**: "B4-R-37 non risolve al costrutto". **PROVE**: Read diretta di `CAP_06_parte_VI.md` — `:190` = `### 29.3 Notifica trigger_event come messaggio separato` (header, confermato via `sed -n '190p'`); `:192` = paragrafo con "non modifica il messaggio di emissione (no edit, no append) … `signal_id` esplicito" (confermato via `sed -n '192p'`). La sola citazione di B4-R-37 (SPEC :434) è `:190`. **ALTERNATIVE ESCLUSE**: che B4-R-37 abbia una seconda citazione concomitante a salvare il costrutto — esclusa per lettura diretta delle righe :433–:436 (unica etichetta `[…:190]`). **ALTERNATIVE NON ESCLUSE**: nessuna.
- **VERIFICA**: "NFR-6.1 e R-6.4 sono gli unici requisiti di consegna v2 su CAP_06 Cap.29 non già coperti dal B4 base". **PROVE**: matrice v2 :560–:568 (fonti per req. R-6.*/NFR-6.*); R-6.1/6.5/6.6 hanno fonte CAP_02 Cap.9 (già B4 base); R-6.4 e NFR-6.1 hanno fonte CAP_06 Cap.29 ed erano i bersagli mancanti. **ALTERNATIVE ESCLUSE**: che NFR-6.2 (latenza) fosse un residuo CAP_06 caduto — esclusa: matrice v2 :568 la fonda su CAP_02 Cap.9 / CAP_07 Cap.31, non su CAP_06 Cap.29. **ALTERNATIVE NON ESCLUSE**: che esista un requisito di consegna v2 fuori Sez.6 con fonte CAP_06 Cap.29 — non rilevato nella matrice riconciliata v2 (75 righe, 0 orfani, :604).
- **VERIFICA**: "Cecità preservata". **PROVE**: grep di contaminazione sulla sola sezione :379–:487 → uniche occorrenze = note di recupero (dovute da AC-EXT-1); confronto manuale prosa vs v2 Sez.6 senza frasi ricalcate. **ALTERNATIVE NON ESCLUSE**: eco lessicale non greppabile — limite intrinseco dichiarato; mitigato dal fatto che il lessico dei requisiti è quello di Cap.29 (fonte legittima), non della v2.
- **VERIFICA**: "Nessuno scope creep runtime". **PROVE**: tutte le 11 citazioni cadono in Cap.29 (:146–:232); nessuna in Cap.27 (:1–:139) o Cap.28; E.7 rinvia Cap.27+Cap.28 a B5. **ALTERNATIVE ESCLUSE**: che un requisito citasse Cap.28 (es. determinismo/logging) — esclusa per ispezione delle 11 etichette. **ALTERNATIVE NON ESCLUSE**: nessuna.

---

## 9. Empirico-CLI da verificare

**VUOTA** — come atteso per il track Business-spec in sede CLI: l'estensione consolida materia documentale di un CAP frozen (Cap.29), non introduce fatti empirici nuovi né richiede accesso a DAPI o al filesystem locale. Nessuna asserzione rinviata a verifica empirica.

---

*Review iterazione 1 prodotta dallo spec_reviewer in sede CLI (audit documentale no-DAPI, divieto CLI rispettato — nessuna probe eseguita). Floor citazioni verificato token-per-token su tutte e 11 le citazioni-bersaglio contro `CAP_06_parte_VI.md` Cap.29 (frozen G-09, sola lettura — nessun CAP modificato). Parte B4 base (PASS `c3be05e`) non ri-auditata.*

---

## ITERAZIONE 2 (re-review di DELTA) — verdetto: **PASS**

> **Tipo**: re-review di **DELTA** sul solo rework iter.2. Commit del rework **`570d684`** (`[SPEC-FUNZ-01-B4-EXT] iter.2 — fix citazioni #1 BUG + #2/#3/#4 MIGLIORA: header->paragrafo`); HEAD READY_FOR_REVIEW `632a9f6`.
> **Delta certificato**: `git diff b954f17 570d684 -- docs/spec_funzionale/SPEC_FUNZ_01_B4.md` = numstat **`8 8`** (8 righe modificate, 8 sostituite, **0 aggiunte/eliminate nette**) = 4 citazioni nel corpo (B4-NFR-06, B4-R-35, B4-R-36, B4-R-37) + le 4 righe corrispondenti della matrice E.6. Nessun cambio di proposizione/testo.
> **Sede**: CLI (GOV-SURFACES-01). Audit documentale no-DAPI, divieto CLI rispettato (nessuna probe). CAP `CAP_06_parte_VI.md` aperto in **sola lettura** (frozen G-09), non modificato.
> **Letture confermate**: `tasks/METODO.md` (RM-1..RM-4 + RACC-METODO-2), `.claude/BASE_COMUNE.md` (§3/§4/§6/§8), `.claude/agents/spec_reviewer.md`, review iter.1 (finding #1..#5 §7), `tasks/ACTIVE_TASK.md` §8 (mandato dei 4 fix).

**Motivazione**: i 4 fix di citazione risolvono ora token-per-token al costrutto affermato; il BUG REALE #1 è chiuso; nessuna regressione; finding #5 (NEUTRO) lasciato invariato come da mandato. 0 BUG REALE in tabella ⇒ PASS (BASE_COMUNE §4).

### A. Le 4 citazioni corrette risolvono token-per-token (floor 100% pulito sull'estensione)

Verifica diretta sulle righe-paragrafo di `CAP_06_parte_VI.md` (Read, frozen):

| Fix | Requisito | Citazione iter.2 | Riga CAP — costrutto presente | Esito |
|---|---|---|---|---|
| **#1 (era BUG REALE)** | B4-R-37 | `:192` (sola) | `:192` = "il motore pubblica una **notifica `trigger_event` come messaggio Telegram separato** … ha `signal_id` esplicito … **non modifica il messaggio di emissione (no edit, no append)**" | **RISOLVE — BUG #1 CHIUSO** |
| #2 (era MIGLIORA) | B4-NFR-06 | `:146`, `:148` (rimosso `:154`) | `:148` = "**Nessun campo nuovo viene introdotto nel payload formale** … **payload formale (immutabile …) vs rappresentazione mobile (cosmetica …)**" | **RISOLVE** |
| #3 (era MIGLIORA) | B4-R-35 | `:220`, `:156` (era `:154`) | `:156` = "**Le 9 voci pubblicate** di Cap.9.2 … riordinate per **priorità di lettura mobile** … numero totale … **esattamente 9**" (+ `:220` "esattamente 3 notifiche standard", 1ª = emissione) | **RISOLVE** |
| #4 (era MIGLIORA) | B4-R-36 | `:220`, `:192` (era `:190`) | `:192` = "notifica `trigger_event` come **messaggio Telegram separato** … al verificarsi del **raw touch della `entry_zone`**" (+ `:220` 2ª = trigger_event) | **RISOLVE** |

Le 4 righe `:154` e `:190` precedentemente citate erano gli header `### 29.2` / `### 29.3` (confermato: `:154` = "### 29.2 Layout mobile-first del messaggio di emissione"; `:190` = "### 29.3 Notifica `trigger_event` come messaggio separato"), privi del costrutto. Ora rimpiazzate/integrate dai paragrafi di contenuto `:148`/`:156`/`:192`. **Floor citazioni AC-G7 = 100% pulito sull'estensione** (le 7 citazioni già RISOLVE in iter.1 sono immutate; i 3 PARZIALI e l'1 NON-RISOLVE sono ora tutti RISOLVE).

### B. Chiusura BUG #1 + 3 MIGLIORA

- **BUG REALE #1 (B4-R-37)**: chiuso. L'unica citazione non era più l'header `:190` ma il paragrafo `:192` che porta esattamente "no edit, no append" + "`signal_id` esplicito".
- **MIGLIORA #2/#3/#4**: chiusi (stesso pattern header→paragrafo), tutti risolti come da mandato §8.

### C. Finding #5 (NEUTRO, B4-R-38 `:223`) — lasciato invariato

Confermato: la riga di matrice di B4-R-38 resta `CAP_06_parte_VI.md:220, :223, :225`; il diff completo `b954f17..570d684` NON contiene alcuna modifica a B4-R-38 (né corpo né matrice). Non instradato, non toccato — corretto.

### D. 0 regressioni

- **Numstat SPEC = `8 8`**: 8 righe modificate, 0 aggiunte/eliminate nette. Le 8 sono esattamente le 4 del corpo (B4-NFR-06 :401, B4-R-35 :422, B4-R-36 :429, B4-R-37 :434) + le 4 della matrice E.6. Nessun altro requisito toccato.
- **Proposizioni/testo invariati**: ogni hunk del diff cambia solo il token di puntatore `[…:NNN]`; il testo del requisito e il *Valore operativo* sono identici.
- **Conteggio invariato**: parte base = 50 (riga :375); totale B4 = **61** (riga :472: 40 R + 14 CN + 7 NFR). Invariato.
- **50 requisiti B4 base intatti** (fuori dal diff) e gli altri 7 requisiti dell'estensione (B4-NFR-05/07, B4-R-33/34/38/39/40) intatti.

### E. Coerenza REPORT

`reports/REPORT_SPEC_FUNZ_01_B4.md`: tabella **AC-G7 aggiornata PARZIALE→OK** con annotazione iter.2 (le 4 citazioni spostate header→paragrafo, righe `:148`/`:156`/`:192` ri-verificate token-per-token); aggiunto §"Conferma letture (iter.2)" + punto 6 in §Decisioni con blocco RM-1 (VERIFICA/PROVE/ALTERNATIVE ESCLUSE/NON ESCLUSE) coerente con quanto verificato qui. Onesto e allineato al delta.

### F. Tabella "Classificazione per il supervisore" (re-review)

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|------------------------|
| — | Nessun residuo. I 4 finding instradati (iter.1 #1 BUG + #2/#3/#4 MIGLIORA) sono chiusi; #5 (NEUTRO) lasciato come deciso da AC. | — | — | — |

**0 BUG REALE, 0 bloccanti, 0 non-bloccanti. Tabella vuota.**

### G. Applicazione RM-1 a me stesso (re-review)

- **VERIFICA**: "Le 4 citazioni corrette risolvono token-per-token". **PROVE**: Read diretta di `CAP_06_parte_VI.md` righe :144-:159, :189-:194, :219-:220 (frozen, sola lettura): `:192` contiene "no edit, no append" + "`signal_id` esplicito" + "messaggio Telegram separato … raw touch"; `:148` contiene "Nessun campo nuovo … payload formale (immutabile) vs rappresentazione mobile (cosmetica)"; `:156` contiene "Le 9 voci pubblicate … riordinate per priorità di lettura mobile … esattamente 9"; `:220` "esattamente 3 notifiche standard … no polling, no refresh". **ALTERNATIVE ESCLUSE**: che una delle 4 conservasse ancora un puntatore-header — esclusa per ispezione del diff (`:154`/`:190` non più presenti nelle 4 righe corrette). **ALTERNATIVE NON ESCLUSE**: nessuna.
- **VERIFICA**: "0 regressioni, delta = solo 4 citazioni + 4 righe matrice". **PROVE**: `git diff b954f17 570d684 --numstat` su SPEC = `8 8`; ispezione hunk = solo token di puntatore cambiati, testo immutato. **ALTERNATIVE ESCLUSE**: cambio di proposizione/scope/conteggio — esclusa (conteggio 61 a :472 invariato; nessuna riga di requisito modificata oltre il puntatore). **ALTERNATIVE NON ESCLUSE**: nessuna.
- **VERIFICA**: "Finding #5 lasciato". **PROVE**: assenza di B4-R-38 dal diff + riga matrice `:220, :223, :225` immutata. **ALTERNATIVE NON ESCLUSE**: nessuna.

### H. Empirico-CLI da verificare

**VUOTA** — come atteso (track Business-spec, sede CLI). Il delta è puramente documentale (ri-puntamento di citazioni a un CAP frozen); nessun fatto empirico nuovo, nessun accesso DAPI/filesystem locale richiesto.

---

*Re-review iterazione 2 (delta) prodotta dallo spec_reviewer in sede CLI (audit documentale no-DAPI, divieto CLI rispettato). Delta circoscritto a `git diff b954f17 570d684`. Le 4 righe-bersaglio (:148/:156/:192) ri-verificate token-per-token contro `CAP_06_parte_VI.md` (frozen G-09, sola lettura — nessun CAP modificato). BUG #1 chiuso, floor citazioni 100% pulito sull'estensione, 0 regressioni, finding #5 lasciato. Verdetto: PASS.*
