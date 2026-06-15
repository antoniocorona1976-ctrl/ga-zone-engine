# REVIEW — SPEC-FUNZ-01-B2 — Payload del segnale

> **Perimetro auditato**: `docs/spec_funzionale/SPEC_FUNZ_01_B2.md` (commit `ecce6a1`) + cross-check `reports/REPORT_SPEC_FUNZ_01_B2.md`.
> **Sede**: CLI (GOV-SURFACES-01, METODO §Superfici) — audit documentale **no-DAPI**, divieto CLI attivo (nessuna probe di zelo).
> **Modalità**: CAP-review piena adattata al non-CAP, **due giri ostili** (BASE_COMUNE §6). Due fronti: (1) audit AC di B2 §3 card; (2) confronto-copertura modalità B vs v2 congelata `ab7450f`.
> **CAP-fonte**: `docs/methodology_v2/CAP_02_parte_II.md` (CAP-02 PASS `a1625df`, freeze G-09) — aperto in **sola lettura**, NON riaudito, NON modificato. Auditata solo la risoluzione delle citazioni di B2.
> **Letture obbligatorie confermate**: `tasks/METODO.md` (RM-1..RM-4 + RACC-METODO-2); `.claude/BASE_COMUNE.md` (§3/§4/§6/§8); `.claude/agents/spec_reviewer.md`; `tasks/ACTIVE_TASK.md` (card B2, AC-G1..AC-G11, §8 modalità review).

---

## VERDETTO: **PASS**

0 problemi bloccanti, **0 BUG REALE in tabella**. 1 osservazione minore (NEUTRO: riferimento interno rotto). Confronto-copertura vs v2: **0 buchi** nel perimetro payload. Audit cecità: **0 tracce** di rottura. Lista "Empirico-CLI da verificare": **vuota** (atteso).

Mapping verdetto↔classificazione (BASE_COMUNE §4): nessun BUG REALE ⇒ PASS ammesso; il singolo finding è NEUTRO (osservazione minore), che non declassa a CONDITIONAL.

---

## FRONTE 1 — Audit ostile sugli AC di B2

### AC-G7 / Tracciabilità — Floor citazioni 100% (PRIORITÀ #1)

Verificata **token-per-token** ogni citazione `[DOC-INTERNO CAP_02_parte_II.md:<riga>]` di B2 contro il Cap.6 del CAP-fonte (righe 13-89, lette integralmente; alcune righe borderline ri-estratte con `awk`/`Grep`). **Tutte risolvono.** Campione dei controlli decisivi:

| Citazione B2 | Requisito | Riga CAP — contenuto verificato | Esito |
|---|---|---|---|
| :17, :19 | B2-R-01 (tupla 12 campi) | :17 "tupla strutturata, immutabile…"; :19 tupla con i 12 campi esatti | RISOLVE |
| :23 | B2-R-02/03/04 (signal_id univoco/opaco/orizzonte) | :23 "identificatore univoco… valore opaco non riutilizzabile… unicità… intero orizzonte operativo" | RISOLVE |
| :25 | B2-R-05/06 (minuto chiuso, CET) | :25 "istante… al minuto chiuso. Il riferimento orario è CET" | RISOLVE |
| :27 | B2-R-07 (direction long/short) | :27 dominio $\{long,short\}$ | RISOLVE |
| :29, :31 | B2-R-08/35 (entry_zone insieme discreto) | :29-:31 definizione formale dell'insieme attorno a $p_{ref}$ | RISOLVE |
| :33 | B2-R-09/32/36/37 (p_ref mult.5; dominio b; cardinalità; floor) | :33 dominio $b\in\{5..40\}$, $b_{min}=5$, cardinalità $(2b/5)+1$, floor per evitare banda nulla | RISOLVE |
| :35 | B2-R-10..19 (target obblig./distinti/mult.5/ordine/strutturali) | :35 "entrambi obbligatori e distinti, multipli di 5… long $t_1>p_{ref}$, $t_2>t_1$; short simmetrico… ancorati a livelli strutturali" | RISOLVE |
| :37 (:7) | B2-R-20 (target_2 info strutturale, Q-05 Cl.2) | :37 "target_2 è informazione strutturale pubblicata, non variabile di lifecycle… contratto si chiude a target_1"; :7 Clausola 2 | RISOLVE |
| :39 | B2-R-21/22 (target_2_type {structural,synthetic}) | :39 dominio + synthetic = livello calcolato vs structural confermato | RISOLVE |
| :41 | B2-R-23 (stop_loss strutturale mult.5) | :41 "prezzo strutturale di stop, multiplo di 5" | RISOLVE |
| :43 | B2-R-24 ($d_{stop}=|p_{ref}-stop|$) | :43 definizione di $d_{stop}$ | RISOLVE |
| :47, :49 | B2-CN-01 (vincolo $d_{stop}>b$) | :47 "$d_{stop}>b$"; :49 razionale fill bordo opposto = stop stesso tick | RISOLVE |
| :51 | B2-R-25/26/27 (stop_type; dominio esclude stop operatore) | :51 dominio {structural,synthetic} + "non include valori prodotti dall'operatore: il motore non gestisce stop manuali" | RISOLVE |
| :53, :55, :59 | B2-R-28/29 (setup_class + filtro 80pt come qualificazione) | :53 dominio + "regola di filtro"; :55 $|t_1-p_{ref}|\ge80$; :59 $A_{range}\ge80$ | RISOLVE |
| :63 | B2-R-30 ($\Delta t_{cromosoma}\in\{1,..,1680\}$) | :63 dominio $\{1,..,1680\}$ minuti di trading | RISOLVE |
| :69 | B2-R-31 ($T_{touch}^{max}\in\{5,..,480\}$) | :69 dominio $\{5,..,480\}$ minuti di trading | RISOLVE |
| :73 | B2-CN-02/03 (immutabilità; no edit a parità signal_id) | :73 "non subisce alcuna modifica… congelata… non esiste refresh/edit che lasci invariato signal_id" | RISOLVE |
| :77, :83 | B2-CN-05 (sostituzione = nuovo id + nuova tupla) | :77 "non modifica… emette nuovo signal_id… tupla $\mathcal{S}'$ completa indipendente"; :83 punto 7+6 dich. intenti | RISOLVE |
| :79, :81 | B2-CN-04 (segnale unico attivo $|\mathcal{A}(t)|\le1$) | :79 "$\mathcal{A}(t)$ insieme segnali attivi"; :81 "$|\mathcal{A}(t)|\le1$ per ogni $t$" | RISOLVE |
| :9, :5 | B2-R-33/34/32 (tick 5pt; b mult.5; preambolo b) | :9 "tick size 5 punti… $b_{min}=5$ = 1 tick… cardinalità 8 $\{5..40\}$"; :5 banda eredità CAP-01 | RISOLVE |

**Floor 100% raggiunto.** Nessuna citazione che non risolve. 0 finding di tracciabilità.

### AC-G1 — Atomicità (N1): OK
Ogni requisito = una sola proposizione verificabile. I campi multi-vincolo sono correttamente spezzati: `target_1`/`target_2` → 11 requisiti atomici (obbligatorietà ×2, distinzione, mult.5 ×2, ordine long ×2, ordine short ×2, ancoraggio, natura Q-05); `signal_id` → 3; banda b → 6. Nessun requisito composito sfuggito alla verifica singola.

### AC-G2 / AC-G3 — Tracciabilità + valore operativo per ogni requisito: OK
Tutti i 42 requisiti portano sia `[DOC-INTERNO CAP_02_parte_II.md:<riga>]` sia una riga *Valore operativo* riferita all'operatore retail FIB. La matrice §8.1 ribadisce entrambe le colonne.

### AC-G4 — Divieto "verificato X" di prima istanza (RM-1): OK
La §7 dichiara esplicitamente l'assenza di "verificato X" di prima istanza. Verificato: il documento non contiene blocchi `VERIFICA/PROVE/ALTERNATIVE` mancanti, perché ogni proposizione è un richiamo a un fatto già chiuso nel Cap.6 frozen. Nessuna asserzione empirica nuova su sistemi esterni.

### AC-G5 — Etichette RM-3 fonti esterne: OK (vacuamente)
Nessun `[WIKI-HINT]` né riferimento a MiFID/Telegram/Directa/IDEM nel corpo B2 (il payload è materia interna del contratto). Nessuna fonte esterna usata come fonte unica. RACC-METODO-2 non applicabile (B2 non cita schemi di sistemi esterni / decoder).

### AC-G6 — Grafia canonica: OK
Usata solo `[DOC-INTERNO …]`. Nessuna occorrenza della grafia storica vietata `[CODICE-EXISTENTE …]`.

### AC-G8 — Cecità preservata (modalità B): OK — vedi "Audit cecità" sotto.

### AC-G9 — Scope "tutto e solo" Cap.6: OK
- **Tutto**: coperti i 12 campi (6.1), l'immutabilità (6.2), il segnale unico attivo + sostituzione-come-proprietà (6.3), la banda b con dominio/cardinalità/floor, il filtro 80pt come qualificazione del campo. Nessuna materia di Cap.6 omessa.
- **Solo (no scope creep)**: verificato che i campi a rischio restano **campi/qualificazione del payload**, NON semantica/regola:
  - `setup_class`/filtro 80pt (B2-R-28/29): consolidata solo l'**associazione** del filtro al campo; la regola di emissione è esplicitamente rinviata (nota inline r.183 + §8.2). Nessuno sviluppo della regola Cap.8 → B4. Conforme.
  - $\Delta t_{cromosoma}$/$T_{touch}^{max}$ (B2-R-30/31): consolidati come **campi-parametro con dominio**; la semantica timer (decorrenza, scadenza→`expired`, counter minuti trading) è rinviata (note inline + §8.2). Nessuno sconfinamento in B3. Conforme.
  - target_2 (B2-R-20): consolidato come **campo informativo-strutturale**; il raggiungimento *come evento* del position lifecycle è rinviato. Conforme.
  - sostituzione (B2-CN-05): consolidata come **proprietà-del-payload** (nuovo id + nuova tupla, non edit); la meccanica delle transizioni (`active→revoked`, state machine) è rinviata. Conforme — da notare che la v2 R-3.11 includeva "(transizione a `revoked`)", elemento di state-machine che B2 **correttamente NON** importa (rispetto del confine B3).

### AC-G10 — Matrice di tracciabilità + nota di rinvio: OK
Matrice §8.1 con 42 righe (ID | proposizione | citazione | valore operativo). Nota di rinvio §8.2 enumera le materie deliberatamente rinviate (state-machine/timer-semantica → Cap.7; lifecycle/target_2-evento → Cap.11; emissione/filtro-regola/$A_{range}$ → Cap.8/Parte IV; Telegram → Cap.9; log/replay → Cap.10; matematica → Parti III/IV) con il "perché". Distinzione omissione-voluta vs gap risolta.

### AC-G11 — Invarianti come tali: OK
Immutabilità (B2-CN-02/03), segnale unico attivo (B2-CN-04), sostituzione-non-edit (B2-CN-05), $d_{stop}>b$ (B2-CN-01) sono resi come `B2-CN` *(invariante strutturale)*. La distinzione `{structural, synthetic}` è resa come **dominio di campo** (B2-R-21/22/25/26), con `synthetic` qualificato come "natura informativa derivata da una regola del modello". Conforme alla card.

---

## FRONTE 2 — Confronto-copertura con la v2 congelata (`SPEC_FUNZ_01.md`, PASS `ab7450f`)

Perimetro payload corrispondente nella v2 = **Sezione 3 "Payload del segnale e invarianti"** (R-3.1..R-3.11 + CN-3.1, righe 96-158). Confronto requisito-per-requisito:

| Requisito v2 (perimetro payload) | Coperto in B2? | Mappatura |
|---|---|---|
| R-3.1 tupla 12 campi | SÌ | B2-R-01 |
| R-3.2 direction {long,short} | SÌ | B2-R-07 |
| R-3.3 entry_zone + b mult.5 {5..40} | SÌ | B2-R-08, B2-R-32, B2-R-33 |
| R-3.4 target obblig./distinti/mult.5/ordine/strutturali | SÌ (più granulare) | B2-R-10..19 |
| R-3.5 target_2 info strutturale (Q-05 Cl.2) | SÌ | B2-R-20 |
| R-3.6 target_2_type/stop_type {structural,synthetic} | SÌ | B2-R-21/22/25/26 |
| R-3.7 stop_loss strutturale + $d_{stop}>b$ | SÌ | B2-R-23/24 + B2-CN-01 |
| R-3.8 setup_class {directional,trade_range} | SÌ | B2-R-28 |
| CN-3.1 tick 5pt (p_ref/target/stop/b mult.5; $b_{min}$=1 tick) | SÌ (distribuito) | B2-R-09/13/14/23/33/34 |
| R-3.9 immutabilità signal_id | SÌ | B2-CN-02/03 |
| R-3.10 segnale unico attivo $|\mathcal{A}(t)|\le1$ | SÌ | B2-CN-04 |
| R-3.11 sostituzione (nuovo id + revoca precedente) | SÌ (parte payload) | B2-CN-05 |

**Esito: 0 requisiti di prodotto del perimetro payload caduti.** Nessun buco.

**Divergenze "in più" di B2 (copertura superiore, non gap):** B2 espande dove la v2 era sintetica — `signal_id` opacità/non-riuso/orizzonte (B2-R-02..04), `timestamp_emission` minuto-chiuso/CET (B2-R-05/06), filtro 80pt come qualificazione esplicita del campo (B2-R-29), $\Delta t_{cromosoma}$/$T_{touch}^{max}$ come campi-parametro con dominio (B2-R-30/31), cardinalità banda $(2b/5)+1$ e floor (B2-R-36/37). Tutte tracciate al Cap.6: è maggiore granularità N1, non scope creep.

**Confine rispettato (NON contati come gap di B2):** i requisiti v2 che appartengono a state-machine/emissione/Telegram/go-live (Sezioni 4-8: R-4.*, R-5.*, R-6.*, NFR-8.*, CN-4/5/7.*) sono fuori perimetro payload → B3/B4/B5/B7. Nota: il frammento "(transizione a `revoked`)" interno a R-3.11 v2 è materia state-machine: la sua assenza in B2 è **corretta** (confine B3), non un buco.

---

## Audit cecità (modalità B) — cerca attivamente tracce di rottura

- **ID importati dalla v2**: `Grep` su `R-3.|CN-3.|R-4.|NFR-|Sezione 3` nel documento B2 → **No matches**. Gli ID sono tutti `B2-R-NN`/`B2-CN-NN` auto-assegnati da zero.
- **Frasi identiche alla v2 non presenti nel Cap.6**: la frase-firma della v2 R-3.1 ("tupla strutturata a **12 campi**") non compare in B2 (`Grep` → no match); B2 usa formulazione propria derivata da :17/:19 ("tupla strutturata $\mathcal{S}$ composta esattamente dai dodici campi").
- **ID v2 nelle citazioni / firme testuali v2**: nessuna.
- **Commit message** (`ecce6a1`) dichiara esplicitamente "Lavorato in cieco: nessuna spec preesistente / B1 / file di chunking aperti. ID auto-assegnati".

**Esito: 0 tracce di rottura della cecità.** Nessun BUG REALE di processo.

---

## Problemi bloccanti
Nessuno.

## Problemi non-bloccanti
Nessuno (nessun BUG REALE, nessun MIGLIORA PERFORMANCE / RISCHIO PEGGIORAMENTO sostanziale).

## Osservazioni minori

**OM-1 (NEUTRO) — Riferimento incrociato interno rotto a "§3.10".** Le note alle righe 159 e 298 rinviano per B2-CN-01 al **§3.10**, ma il §3.10 (righe 185-193) contiene i campi-timer $\Delta t_{cromosoma}$/$T_{touch}^{max}$, **non** B2-CN-01. Il requisito B2-CN-01 è in realtà definito nella nota sotto la matrice §8.1 (righe 304-308). Il puntatore interno non collima con la collocazione fisica del requisito.
- *Impatto*: nullo su tracciabilità al CAP (B2-CN-01 è tracciato correttamente a `:47,:49`, verificati), atomicità, valore operativo, cecità, scope. È un difetto di navigabilità editoriale: chi segue il link "§3.10" non trova lì il requisito. Il requisito **esiste** ed è ben formato.
- *Classificazione*: NEUTRO. Non declassa il verdetto. Eventuale correzione (puntare a "§8.1" o spostare B2-CN-01 in una sotto-sezione del corpo §3) resta a discrezione del supervisore via micro-pass, non obbligatoria.

---

## Onestà del REPORT (campionamento claim→evidenza, BASE_COMUNE §8)
La tabella verifica AC del REPORT dichiara tutti gli AC `OK`. Campionati e riscontrati reali: AC-G7 (pin verificati token-per-token — riscontrato indipendentemente sopra), AC-G1 (atomicità target — riscontrata B2-R-10..20), AC-G8 (cecità — riscontrata via Grep), AC-G9 (scope — riscontrato confine timer/filtro/sostituzione). Il conteggio "42 requisiti (37 R + 5 CN)" è esatto (B2-R-01..37 + B2-CN-01..05). Nessun `OK` privo di evidenza puntuale reale. La sezione "Applicazione RM-1 a me stesso" del REPORT è presente e coerente.

---

## Applicazione RM-1 a me stesso (Reviewer)

- **"Tutte le citazioni di B2 risolvono token-per-token"** — PROVE: lette righe 1-302 del CAP-fonte (Cap.6 = righe 13-89 integrali), più ri-estrazione mirata via `awk`/`Grep` di :17-19, :37, :77, :79-83. Confrontato ogni numero di riga citato col contenuto effettivo (tabella FRONTE 1). ALTERNATIVE ESCLUSE: citazione che punta a riga sbagliata — esclusa, tutte verificate. ALTERNATIVE NON ESCLUSE: nessuna entro il perimetro Cap.6. Le righe >302 (Cap.7-11) sono fuori perimetro B2 e non citate da B2 (confermato: nessuna citazione B2 supera :83).
- **"0 buchi nel confronto-copertura vs v2"** — PROVE: letta la Sezione 3 v2 integralmente (righe 96-158) e mappato ogni R-3.*/CN-3.1 a un requisito B2 (tabella FRONTE 2). ALTERNATIVE ESCLUSE: requisito payload v2 non mappato — escluso, 12/12 mappati. ALTERNATIVE NON ESCLUSE: la v2 oltre la Sezione 3 (righe 159+) contiene payload? Verificato per lettura: le Sezioni 4-8 sono state-machine/emissione/Telegram/go-live (fuori perimetro payload); il perimetro payload v2 è circoscritto alla Sezione 3. Nessun requisito-payload disperso altrove individuato.
- **"0 tracce di rottura cecità"** — PROVE: `Grep` su pattern ID v2 e su frase-firma "12 campi" → no match; commit message dichiara cieco. ALTERNATIVE ESCLUSE: parafrasi identica alla v2 non greppata — mitigata dal confronto manuale FRONTE 2 (le formulazioni B2 derivano dal CAP, non dalla v2). ALTERNATIVE NON ESCLUSE: una parafrasi semantica non-letterale non è meccanicamente escludibile al 100%, ma l'aderenza testuale al Cap.6 è positiva e nessun costrutto v2-specifico assente dal CAP è comparso.
- **"Commit pulito, pushato, 3 file attesi"** — PROVE: `git show --stat ecce6a1` (SPEC_FUNZ_01_B2.md + REPORT + DEV_STATUS); `git status -sb` = `main...origin/main` senza "ahead". ALTERNATIVE NON ESCLUSE: nessuna.

Nessuna mia asserzione richiede accesso DAPI o filesystem locale non versionato.

---

## Empirico-CLI da verificare
**VUOTA** (atteso). B2 consolida fatti già chiusi in CAP-02 frozen; nessuna asserzione empirica nuova introdotta. Divieto CLI rispettato: nessuna probe eseguita.

---

## Tabella "Classificazione per il supervisore"

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|------------------------|
| 1 | Riferimento incrociato interno rotto: le note rinviano a "§3.10" per B2-CN-01, ma il requisito è definito sotto la matrice §8.1 (r.306); §3.10 contiene i timer. Difetto di navigabilità, zero impatto su tracciabilità/atomicità/scope/cecità. | `SPEC_FUNZ_01_B2.md:159`, `:298` (→ target reale `:306`) | NEUTRO | No (a discrezione AC; eventuale micro-pass non obbligatorio) |

**Regola applicata**: 0 BUG REALE ⇒ verdetto PASS. Il finding NEUTRO non va a Development senza esplicita approvazione del supervisore (BASE_COMUNE §4).

---

*Review prodotta dallo spec_reviewer (CLI), due giri ostili. CAP-02 frozen non riaudito né modificato. Nessun file estraneo committato: solo questo file di review.*
