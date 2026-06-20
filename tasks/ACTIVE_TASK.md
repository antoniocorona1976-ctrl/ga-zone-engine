# TASK ATTIVO: SPEC-FUNZ-01-B7 — Gate di go-live (ricostruzione cieca, modalità B, blocco 7/8)

> **Track**: Business-spec (SPEC-FUNZ). **Sede**: CLI (GOV-SURFACES-01, METODO §Superfici). **Tag commit**: `[SPEC-FUNZ-01-B7]`. Tutto su `main` (trunk; isolamento via cartella `docs/spec_funzionale/`, non via branch).
>
> **⚠️ VINCOLO CARDINE DI B7 — criteri DICHIARATI, MAI verdetti.** Questo blocco consolida i **CRITERI DI GATE DICHIARATI DAL METODO** per il go-live (le *definizioni* di DSR, PBO/CSCV, bootstrap stazionario, $E[R_{net}]$, CVaR, MDD, la checklist dei 12 AC-GO, le soglie dichiarate, la procedura OOS, l'immutabilità del frozen bundle). **NON** consolida risultati numerici, **NON** dichiara se l'edge esiste, **NON** emette verdetti GO/NO-GO. Ogni claim sull'effettiva esistenza/misura dell'edge (DSR, PBO, out-of-sample, $E[R_{net}]$ effettivi) è **PENDING-empirico (validator / FASE-D)**, mai "verificato". I verdetti **GO/CONDITIONAL/NO-GO** su DSR/PBO/out-of-sample sono **esclusiva del ruolo `validator`** (`.claude/agents/validator.md`, in panchina fino a FASE-D), MAI di Planner/Developer/Reviewer. Questo è il rischio principale del blocco: il Developer NON deve scivolare in asserzioni di esito.
>
> **SHA frozen pinnabili** (freeze G-09; **nessuna dipendenza fragile**): `CAP_07_parte_VII.md` = `b27c1e3`; `CAP_01_parte_I.md` = `e8d5424`. Citabili come SHA di riferimento dei capitoli-fonte congelati.
> **NB (CARD-FIX-01, F4) — SHA frozen di CAP_01 corretto `b76c32c`→`e8d5424`**: `b76c32c` era lo SHA del PASS finale di CAP-01 ma il file è stato successivamente corretto da `[FIX-01]` `01d689a` + `[FIX-03]` `fc7531b` + `[FIX-04]` `e8d5424` (22-23 mag 2026, **pre-B7**, correzioni proprie di Parte I: sessione finestra unica, cap 2gg dal raw touch, `executable_rate`/`target_2_hit_rate` riformulate). Lo SHA frozen autoritativo corrente è quindi `e8d5424` (≡ HEAD per CAP_01, verificato CARD-FIX-01). I **pin-riga §1 Cap.5** (`:67/:71-75/:77/:79/:81/:85`) sono stati riverificati a HEAD e **reggono** (edit FIX bilanciati, nessuno slittamento di riga); il contenuto di Cap.5 è quello corrente (FIX-01/03/04), che il Developer legge a HEAD (AC-G7).
>
> **Perimetro (per CAPITOLI — modalità B)**: deriva **tutti** i requisiti di prodotto dai capitoli **`CAP_07_parte_VII.md` Cap.31, 32, 33, 34, 35, 36 + `CAP_01_parte_I.md` Cap.5**. Assegna gli ID `B7-R-NN`/`B7-CN-NN`/`B7-NFR-NN` **da zero**, applicando l'atomicità N1. **Nessun conteggio-target è imposto.** NB path: numero **romano** per Parte VII (`CAP_07_parte_VII.md`); `CAP_01_parte_I.md` per Parte I.
>
> **Letture obbligatorie del Developer, in quest'ordine, PRIMA di scrivere**: `tasks/METODO.md` (RM-1..RM-4 + RACC-METODO-2 + §Superfici + Freeze G-09), `.claude/BASE_COMUNE.md`, `.claude/agents/spec_developer.md`, questo `tasks/ACTIVE_TASK.md`. Conferma in testa al REPORT di averli letti.
>
> **Pre-flight Developer — verifica freeze G-09 prima di fidarti dei pin §1 (CARD-FIX-01, F4)**: esegui `git diff b27c1e3 HEAD -- docs/methodology_v2/CAP_07_parte_VII.md` e `git diff e8d5424 HEAD -- docs/methodology_v2/CAP_01_parte_I.md`; **entrambi devono essere vuoti**. Se un diff **non** è vuoto, i pin-riga §1 di quel file sono **slittati** → rileggi token-per-token (AC-G7) e cita la riga **reale** a HEAD, non il pin assunto. (Verificato in CARD-FIX-01: a HEAD entrambi i diff sono vuoti con questi SHA — vedi `Business Spec/Final/ESITO_B7-CARD-FIX-01.md`.)

---

## 0. Natura e cecità

**Natura**: ricostruzione cieca da zero del perimetro **Gate di go-live** — la traduzione in requisiti di prodotto dei criteri di validazione OOS, dei gate statistici (DSR, PBO), del bootstrap, del congelamento del bundle e della checklist decisionale di go-live, in vista operatore/prodotto come ponte verso FASE-D. B1..B6 sono chiusi PASS; B8 non esiste ancora.

### 0.1 — Vincolo di cecità (modalità B)

Il Developer deriva i requisiti **DAI SOLI** capitoli del perimetro §1, **cieco** rispetto a:
- `docs/spec_funzionale/SPEC_FUNZ_01.md` (v2 congelata) e ogni `*_v1_storico*`;
- i **file di chunking** (`docs/spec_funzionale/PROPOSTA_SUDDIVISIONE_SPEC*.md`);
- i documenti dei blocchi precedenti (`docs/spec_funzionale/SPEC_FUNZ_01_B1.md` .. `SPEC_FUNZ_01_B6.md`).

Il confronto-copertura con la v2 e la partizione dei requisiti sono compito **esclusivo del Reviewer/Orchestratore** (§8): il Developer **non li vede e non li deve cercare**. Gli ID `B7-*` sono auto-assegnati da zero, con atomicità N1.

**NB — nessuna eccezione RM-2 "leggi i decoder" in B7.** A differenza di B6 (schema-dato DAPI), il perimetro di B7 è **interamente interno** (validazione/gate metodologico calcolato sul **log di replay deterministico bit-exact**, `CAP_07_parte_VII.md:21`): **non c'è alcun decoder/parser di sistema esterno** in scope, quindi nessun rischio RM-2/RM-3 da schema esterno e nessuna lettura imposta di codice di decodifica. La sola fonte autoritativa è il testo dei capitoli del perimetro §1.

---

## 1. Perimetro-fonte — materia da derivare, PER CAPITOLO

Fonte: `docs/methodology_v2/CAP_07_parte_VII.md` (Cap.31, 32, 33, 34, 35, 36) + `docs/methodology_v2/CAP_01_parte_I.md` (Cap.5). I pin sotto sono **puntatori di lavoro** verificati in CLI dall'Orchestratore; il Developer li **rilegge token-per-token** (AC-G7) prima di citarli e cita la riga reale.

- **Cap.5 — Definizione operativa del successo** (`CAP_01_parte_I.md:67`): il **criterio dichiarato di accettazione del bundle** in vista operatore. Materia: metrica primaria $E[R_{net} \mid executed] = E[R_{gross}] - 2c$ (con $c = 1$ pt FIB equivalente/operazione, derivato da 5 EUR su moltiplicatore 5 EUR/pt) `:71-75`; metriche di lifecycle (emission/executable/target-hit/target2-hit/invalidation/missed-target) `:77`; metriche di rischio (CVaR 95%, MDD intraday, MAE/MFE) `:79`; metriche anti-overfitting (DSR, PBO via CSCV) `:81`; e la **dichiarazione di successo per go-live** `:85` (DSR positivo significativo; PBO sotto soglia; $E[R_{net}]>0$; target/executable rate stabili calmo vs turbolento; CVaR 95% e MDD entro limiti dichiarati). **Vincolo da consolidare come tale**: il successo del motore è definito in termini **quantitativi e verificabili del segnale**, **distinto** dal risultato economico aggregato dell'operatore (`:69, :85` — l'esecuzione manuale, lo stop personale, il rollover, la qualità feed NON rientrano nel criterio di successo del motore).
- **Cap.31 — Procedura di validazione OOS** (`CAP_07_parte_VII.md:11`): la **procedura dichiarata** che trasforma il fronte di Pareto $\mathcal{F}_1$ in bundle candidato. Materia:
  - **fonte canonica unica** di tutte le metriche di Parte VII = **log di replay deterministico bit-exact** di Cap.10 di Parte II, sulla finestra OOS aggregata `:21`; **nessuna metrica è calcolata su fill effettivi del broker** (vincolo "solo emissione", `:21`) — da consolidare come **invariante** (premessa `CAP_02_parte_II.md` Cap.10, NON ri-derivare);
  - **finestra OOS aggregata** = concatenazione dei $W_{oos}$ degli $F$ fold del walk-forward nested, con esclusione di purge/embargo `:15-19` (anti-leakage);
  - **selezione lessicografica deterministica** del cromosoma vincente $\theta^*$ via **sei filtri ordinati + criterio finale** `:29-39` (Filtro 1 DSR $>\theta_{DSR}=0{,}95$; Filtro 2 PBO $<\theta_{PBO}=0{,}50$; Filtro 3 lifecycle cross-regime $|f_5|<\theta_{f_5}=0{,}30$; Filtro 4 IQR$_{norm}(f_1)<\theta_{IQR}=0{,}40$; Filtro 5 $\pi_{t_2|t_1}>\theta_{t_2}=0{,}30$; Filtro 6 + tie-break) — **deterministica perché coerente col replay bit-exact**;
  - **parametri di tuning $\theta_{DSR},\theta_{PBO},\theta_{f_5},\theta_{IQR},\theta_{t_2},\epsilon_{f_1}$ dichiarati NON congelati in Parte VII, riconsiderati post-go-live** `:131` (soglie = **valori di lavoro provvisori**, NON valori definitivi: da consolidare con questo stato esatto, vedi AC-B7-3).
- **Cap.32 — Deflated Sharpe Ratio (DSR)** (`CAP_07_parte_VII.md:135`): la **definizione dichiarata** del gate primario di significatività. Materia: formula canonica Bailey-López de Prado 2014 (CDF normale di $(\widehat{SR}-SR^*)\sqrt{n-1}$ su correzione skew/curtosi) `:143`; correzione per $N_{trials}$ prove, lunghezza campione $n$, non-normalità `:139`; soglia $\theta_{DSR}=0{,}95$ **valore di lavoro provvisorio non congelato** `:244`. È il **criterio**, NON un valore misurato.
- **Cap.33 — PBO via CSCV** (`CAP_07_parte_VII.md:248`): la **definizione dichiarata** del gate di fragilità. Materia: PBO = probabilità che il cromosoma vincente in-sample sia overfit (OOS sotto la mediana del fronte) `:252`; procedura **CSCV in sei passi** `:254-` (partizione in $S$ sotto-finestre, $S$ pari, regola $S=2F$ deterministica, $S\in\{12,14,16\}$); soglia $\theta_{PBO}=0{,}50$ **valore di lavoro provvisorio non congelato** `:344`. Criterio, NON misura.
- **Cap.34 — Bootstrap stazionario** (`CAP_07_parte_VII.md:348`) — ⚠️ **CAPITOLO FRAMING / SUPPORT (0-req standalone atteso)**: il bootstrap è il **meccanismo statistico interno** che produce gli $IC_{95\%}$ a supporto del gate **AC-GO-3** (Cap.36, $E[R_{net}]>0$ con IC che esclude lo zero). Come Cap.48 in B6 / Cap.27-28 in B5, è **materia di supporto, non fonda un requisito-prodotto standalone**: consolidalo come **procedura dichiarata a corredo** del gate sull'$E[R_{net}]$, **non** come requisito B7 autonomo. **Se NON trovi una proposizione di prodotto non già coperta dal gate AC-GO-3, non scrivere un requisito "su Cap.34"** (anti-gonfiamento del perimetro). Materia di contesto: bootstrap stazionario Politis-Romano 1994 a **blocchi geometrici** ($p=1/L_{avg}$) `:352-356`; **$B = 2.000$ replicazioni** (eredità Cap.4 di Parte I compute budget) `:449`; $L_{avg}=10$ default Politis-White e $\theta_{cost}=100$ USD/run **valori di lavoro provvisori non congelati** `:449`. Procedura, NON esito.
- **Cap.35 — Frozen bundle e immutabilità** (`CAP_07_parte_VII.md:453`): la **specifica dichiarata** dell'artefatto immutabile e della sua regola di sostituzione. Materia: bundle frozen = artefatto digitale immutabile composto da **sei elementi** (parametri congelati Parte V; geni del cromosoma vincente $\theta^*$; modelli stimati; …) `:457-`; **hash SHA-256 di riferimento immutabile** (integrità al caricamento); **regola di sostituzione del bundle** `:560` (Regola 1/Regola 2, riferimenti Cap.30/Cap.31). Da consolidare come **vincolo di immutabilità/integrità** in vista FASE-D.
- **Cap.36 — Gate decisionali per il go-live** (`CAP_07_parte_VII.md:564`): la **checklist deterministica dichiarata** di go-live. Materia:
  - **12 AC-GO binari** (OK/NOT OK), ordinati e replicabili `:568-599`: AC-GO-1 DSR$>\theta_{DSR}$; AC-GO-2 PBO$<\theta_{PBO}$; AC-GO-3 $E[R_{net}]>0$ con $IC_{95\%}$ bootstrap escluso lo zero; AC-GO-4 $|f_5|<\theta_{f_5}$; AC-GO-5 IQR$_{norm}(f_1)<\theta_{IQR}$; AC-GO-6 CVaR$_{95\%}>\theta_{CVaR}=-100$ pt FIB; AC-GO-7 MDD$_{intraday}<\theta_{MDD}=200$ pt FIB; AC-GO-8 $r_{emit}\in[0{,}2;5]$ segnali/sessione; AC-GO-9 $\rho_{sessions}>\theta_{sessions}=0{,}60$ (target operativo asimmetrico Cap.1: 500 pt FIB/giorno **OR** 70% movimento strutturale intraday); AC-GO-10 pipeline Cap.27 operativa (carica bundle, payload bit-exact, Telegram di test, latenza qualitativa $L_{max}=30$ s); AC-GO-11 dashboard Cap.30 operativa; AC-GO-12 hash bundle frozen valido all'avvio;
  - **decisione binaria GO / NO-GO** `:601-605`: GO se **tutti i 12 AC** OK; NO-GO se **anche un solo** AC è NOT OK, con motivazione + raccomandazione per classe di AC fallito;
  - **verifica aggregata di sessione** (formula di $\rho_{sessions}$, $T_{abs}\lor T_{rel}$, reporting separato calmo/turbolento) `:609-633`;
  - **carryover post-go-live** dei 10 parametri di tuning operativo di Parte VI `:637-641` (rimangono starting point; congelamento empirico richiede dati di produzione live → **non task di Parte VII**);
  - **regola di anticipo del ritraining su trigger di deriva** `:643-` (eredità Cap.30 alert + Cap.35.3 Regola 2; ritraining anticipato se alert persistenti).
  - Le **soglie** $\theta_{CVaR}=-100$, $\theta_{MDD}=200$, $\theta_{sessions}=0{,}60$ sono **valori di lavoro provvisori** dichiarati: consolidare con questo stato esatto.

---

## 2. Fatti già fissati dai capitoli — consolidamento fedele (RM-3, NON ri-derivare)

Questi sono **criteri/definizioni dichiarati** nei capitoli frozen: citarli con `[DOC-INTERNO CAP_07:riga]` / `[DOC-INTERNO CAP_01:riga]`, **non** ri-derivarli, **non** promuoverli a esito misurato.

- **Fonte canonica = log di replay deterministico bit-exact** (`CAP_07_parte_VII.md:7, :21`); nessuna metrica su fill broker (vincolo "solo emissione"). Invariante, premessa `CAP_02_parte_II.md` Cap.10 (NON ri-derivare il determinismo dal motore).
- **Soglie come valori di lavoro provvisori NON congelati in Parte VII** (`:7, :131, :244, :344, :449, :637`): $\theta_{DSR}=0{,}95$, $\theta_{PBO}=0{,}50$, $\theta_{f_5}=0{,}30$, $\theta_{IQR}=0{,}40$, $\theta_{t_2}=0{,}30$, $\theta_{CVaR}=-100$ pt FIB, $\theta_{MDD}=200$ pt FIB, $\theta_{sessions}=0{,}60$, $L_{avg}=10$, $\theta_{cost}=100$ USD/run. **Stato esatto da consolidare**: "valore di lavoro provvisorio, riconsiderato post-go-live", **mai** "valore definitivo/validato".
- **$B = 2.000$ replicazioni bootstrap** (`:449`) — eredità Cap.4 di Parte I (compute budget cloud).
- **Regola $S = 2F$ deterministica**, $S\in\{12,14,16\}$, $S$ pari (`:344, :256`).
- **12 AC-GO binari** e **decisione GO/NO-GO deterministica** (`:568-605`): consolidare come **checklist di criteri dichiarati**; la decisione è una **procedura**, il suo **esito** è validator/FASE-D.
- **Target operativo asimmetrico Cap.1**: 500 pt FIB profitto netto/giorno **OR** 70% movimento strutturale intraday (`:586, :609-625`), eredità Cap.1 di Parte I.

**Eredità M (registro CARRYOVER/STATO)**: nessun M-promemoria di schema-dato è pertinente a B7 (perimetro interno). Resta pertinente la disciplina generale: **claim sull'edge = PENDING-empirico (validator)**. Il Developer **censisce** in REPORT eventuali M aperti di `tasks/CARRYOVER.md` con destinazione (atteso: nessun M nuovo emesso da B7; M esistenti non incardinati salvo che la review li tocchi).

---

## 3. Acceptance Criteria

**AC-G1..AC-G11** ereditati dai blocchi precedenti, vincolanti:

- **AC-G1 (N1 — atomicità)**: ogni requisito è **una sola proposizione verificabile**. Un requisito che impacchetta più concern va spezzato in più ID `B7-*`. (Es.: i 12 AC-GO sono **criteri distinti** → attesi requisiti distinti, non un unico requisito-checklist; DSR e PBO sono gate diversi → ID diversi; recupero/selezione/congelamento/decisione sono concern diversi.)
- **AC-G2 (tracciabilità a riga)**: ogni requisito cita la **riga reale** del capitolo-fonte (`[DOC-INTERNO CAP_07_parte_VII.md:NNN]` / `[DOC-INTERNO CAP_01_parte_I.md:NNN]`), riletta token-per-token (AC-G7).
- **AC-G3 (valore operativo / di sistema)**: ogni requisito dichiara il suo **valore per l'operatore retail FIB o per il sistema** (es.: "il gate DSR protegge l'operatore dal pubblicare un bundle overfit"; "l'immutabilità del bundle garantisce replay/audit"). Un requisito senza valore dichiarato è un requisito sbagliato.
- **AC-G4 (divieto "verificato X" di prima istanza — RM-1)**: la spec **non introduce** nuove dichiarazioni "verificato X". Ogni asserzione fattuale è un **richiamo** a un capitolo frozen con provenienza. Nessun blocco `VERIFICA/PROVE/...` di prima istanza.
- **AC-G5 (etichette RM-3)**: ogni fonte etichettata `[DOC-INTERNO ...]` / `[CODICE-ESISTENTE ...]` / `[PROVA-EMPIRICA <data>]` / `[WIKI-HINT, da verificare]`. Wiki/paper esterni (Bailey-López de Prado, Politis-Romano, ecc.) citati come riferimento bibliografico **del capitolo**, non come fonte di verità di prima istanza.
- **AC-G6 (grafia canonica)**: usare `[CODICE-ESISTENTE]` / `[PROVA-EMPIRICA]` / `[DOC-INTERNO]` / `[WIKI-HINT]`. **Vietata** la grafia deprecata `[CODICE-EXISTENTE]` (METODO RM-3).
- **AC-G7 (rilettura pin token-per-token)**: i pin §1 sono puntatori di lavoro; il Developer rilegge e cita la riga reale, non il pin assunto.
- **AC-G8 (floor citazioni 100%)**: in review, **ogni** requisito deve avere almeno una citazione valida risolvibile alla riga. Floor 100%.
- **AC-G9 (cecità preservata)**: nessun ID-requisito importato dalla v2, **nessun conteggio-target**, **nessuna partizione** da v2/chunking nel documento. ID `B7-*` da zero.
- **AC-G10 (scope "tutto e solo")**: la spec copre **tutto e solo** i capitoli del perimetro §1 (Cap.31-36 + Cap.5). Materia di altri blocchi NON va ri-derivata (è finding): vedi out-of-scope §6.
- **AC-G11 (matrice + nota di rinvio)**: sezione finale con **matrice di tracciabilità** (ogni `B7-*` → capitolo:riga + valore operativo) e **nota di rinvio** per le premesse/out-of-scope §6; gli **invarianti** consolidati come tali (non ri-derivati).

**Specifici di B7 (VINCOLO CARDINE — edge PENDING):**

- **AC-B7-EDGE (cardine, obbligatorio)**: ogni criterio di gate è formulato come **criterio DICHIARATO dal metodo** (definizione/soglia/procedura), **mai** come esito misurato. **Ogni claim sull'effettiva esistenza o misura dell'edge** (valore di DSR/PBO/$E[R_{net}]$/CVaR/MDD effettivo, esito out-of-sample, decisione GO/NO-GO) è marcata **PENDING-empirico (validator / FASE-D)** e **mai asserita "verificata"**. Verbi vietati su grandezze d'esito: "il bundle supera/passa il gate", "DSR è positivo/significativo", "l'edge esiste/è confermato", "GO". Verbi ammessi: "il metodo **richiede** DSR$>\theta_{DSR}$", "il criterio **dichiarato** è …", "**al run del validator** si misurerà …".
- **AC-B7-VALIDATOR (confine di ruolo)**: la spec **esplicita** che B7 (e l'intero track SPEC-FUNZ) **NON emette** verdetti GO/CONDITIONAL/NO-GO né valori d'edge: sono **esclusiva del ruolo `validator`** (`.claude/agents/validator.md`), in panchina fino a FASE-D. Una nota di confine di ruolo è obbligatoria nel documento (intestazione o sezione gate decisionali).
- **AC-B7-SOGLIE (stato delle soglie)**: ogni soglia ($\theta_{DSR},\theta_{PBO},\theta_{f_5},\theta_{IQR},\theta_{t_2},\theta_{CVaR},\theta_{MDD},\theta_{sessions},L_{avg},\theta_{cost}$) è consolidata col suo **stato esatto dichiarato**: "**valore di lavoro provvisorio, non congelato in Parte VII, riconsiderato post-go-live**". È finding consolidarle come valori definitivi/validati o ometterne la provvisorietà.
- **AC-B7-SUCCESSO (confine motore vs operatore)**: il requisito sulla definizione di successo (Cap.5) consolida esplicitamente che il successo è **del segnale del motore**, **distinto** dal risultato economico aggregato dell'operatore (esecuzione manuale/stop personale/rollover/qualità feed **fuori** dal criterio di successo). È finding confondere i due piani.
- **AC-B7-ATOMICITA-GO (atomicità degli AC-GO compositi — F5/B6-analogo)**: i 12 AC-GO restano **12 criteri/requisiti distinti** (N1, un ID `B7-*` ciascuno). In più, per gli AC-GO **compositi** al loro interno — **AC-GO-10** (pipeline operativa, multi-condizione: (a) carica bundle frozen + hash valido `CAP_07_parte_VII.md:589`, (b) payload bit-exact 12 campi `:590`, (c) Telegram di test mobile-first `:591`, (d) latenza $L_{max}=30$ s `:592`) e **AC-GO-11** (dashboard, multi-condizione: (a) tracciamento metriche live `:595`, (b) alert configurati e testati `:596`, (c) reporting opzionale lifecycle `:597`) — la verifica multi-condizione è **enumerata DENTRO il singolo criterio**, **NON** spacchettata in requisiti separati: il criterio è **un'unica proposizione OK/NOT-OK**, le sotto-condizioni ne sono il contenuto di verifica (coerente con Cap.36, che presenta i 12 AC-GO come **criteri binari**, `:568`). **NB (RM-2, verificato sul repo)**: **AC-GO-12** (hash bundle frozen valido all'avvio, `:599`) è una **condizione singola** (già atomica), **non** un AC-GO composito; non spacchettarlo. Per AC-GO-10/11 vale lo stesso buco di B6-F5 (R-9.3): un Developer cieco non deve né scrivere un requisito non-atomico né spacchettare arbitrariamente — un criterio, N sotto-condizioni di verifica al suo interno.

---

## 4. Sezioni da produrre (`docs/spec_funzionale/SPEC_FUNZ_01_B7.md`)

1. **Intestazione/scopo/schema-ID** (`B7-*` da zero) + conferma cecità + **nota di confine di ruolo edge-PENDING / validator** (AC-B7-EDGE, AC-B7-VALIDATOR) in evidenza.
2. **Definizione operativa del successo** (Cap.5): metrica primaria $E[R_{net}]$, metriche di lifecycle/rischio/anti-overfitting, dichiarazione di successo per go-live come **criterio dichiarato**; confine motore vs operatore (AC-B7-SUCCESSO).
3. **Procedura di validazione OOS** (Cap.31): fonte canonica = log di replay bit-exact (invariante, premessa CAP_02 Cap.10); finestra OOS aggregata (purge/embargo/anti-leakage); selezione lessicografica deterministica del bundle candidato (sei filtri ordinati) — come **procedura dichiarata**.
4. **Gate statistico primario — DSR** (Cap.32): definizione/formula/correzioni; soglia $\theta_{DSR}=0{,}95$ provvisoria; valore d'esito = PENDING-empirico.
5. **Gate di fragilità — PBO via CSCV** (Cap.33): definizione; procedura CSCV 6 passi; $S=2F$; soglia $\theta_{PBO}=0{,}50$ provvisoria; esito = PENDING-empirico.
6. **Intervalli di confidenza — bootstrap stazionario** (Cap.34): procedura Politis-Romano a blocchi geometrici; $B=2.000$; $L_{avg}=10$ provvisorio; uso per $IC_{95\%}$ (es. AC-GO-3); esito = PENDING-empirico.
7. **Frozen bundle & immutabilità** (Cap.35): artefatto immutabile (sei elementi), hash SHA-256 di integrità al caricamento, regola di sostituzione del bundle — come **vincolo di immutabilità/integrità** verso FASE-D.
8. **Gate decisionali di go-live** (Cap.36): i **12 AC-GO** come **criteri dichiarati distinti** (N1, un ID `B7-*` ciascuno). Per gli AC-GO **compositi** (AC-GO-10 pipeline 4 sotto-cond. `:589-592`; AC-GO-11 dashboard 3 sotto-cond. `:595-597`) le sotto-condizioni sono **enumerate DENTRO il singolo criterio** come contenuto di verifica, **non** spacchettate in requisiti separati (AC-B7-ATOMICITA-GO); **AC-GO-12** è una condizione singola già atomica (`:599`). La **procedura** di decisione GO/NO-GO deterministica (esito = validator/FASE-D, AC-B7-VALIDATOR); verifica aggregata di sessione ($\rho_{sessions}$, target asimmetrico Cap.1); carryover post-go-live dei 10 parametri Parte VI; regola di anticipo del ritraining su trigger di deriva.
9. **Matrice di tracciabilità** (`B7-*` → capitolo:riga + valore operativo/di sistema) + **nota di rinvio** (premesse/out-of-scope §6) + **lista PENDING-empirico** (§7-card) + nota RM-3 (gerarchia fonti).

**REPORT** (`reports/REPORT_SPEC_FUNZ_01_B7.md`): 5 sezioni formato supervisore (Cosa è stato prodotto; Ipotesi di partenza; Decisioni rilevanti; Domande aperte; Criterio di rollback) + **tabella AC** (G1..G11 + B7-EDGE/VALIDATOR/SOGLIE/SUCCESSO con `OK/PARZIALE/MANCA` + evidenza `file:riga`) + sezione **"Applicazione RM-1 a me stesso"** + **lista PENDING-empirico** + **conferma esplicita che nessun verdetto d'edge è stato asserito** (auto-check AC-B7-EDGE). F6: tutti i blocchi/ambiguità raccolti in **un unico batch** nel REPORT, non un giro per blocco.

---

## 5. Premesse dichiarate (citare come premessa, NON ri-derivare)

| Materia | Destinazione / trattamento |
|---|---|
| **Determinismo bit-exact / replay** (fonte canonica delle metriche) | premessa **`CAP_02_parte_II.md` Cap.10** — consolidato come **invariante** che la procedura OOS preserva, NON ri-derivato dal motore |
| **Fronte di Pareto $\mathcal{F}_1$, NSGA-II, cromosoma, $f_1$-$f_5$, $\text{IQR}_{norm}$** | premessa **Parte V (Cap.22-26)** — B7 consuma $\mathcal{F}_1$ e le metriche come **input** della procedura OOS, non ne ri-deriva la generazione |
| **Walk-forward nested, purge/embargo, $W_{in}/W_{oos}/F$** | premessa **Parte V (Cap.25)** — B7 cita la finestra OOS aggregata, non ri-deriva il walk-forward |
| **Modello EGARCH / classificazione regime calmo-turbolento** | premessa **Parte III (Cap.14)** — usata per il reporting separato di sessione, non ri-derivata |
| **Pipeline di inference (Cap.27), layout Telegram (Cap.29), dashboard+alert (Cap.30)** | premessa **Parte VI** — B7 le cita come oggetto di verifica AC-GO-10/11 e della regola di anticipo ritraining, non ne ri-deriva la specifica |
| **Submachine post-target_1 ($\pi_{t_2|t_1}$, MFE/MAE)** | premessa **Parte II (Cap.11)** — usata in Filtro 5 e nelle metriche di rischio, non ri-derivata |
| **Target operativo asimmetrico (500 pt / 70% strutturale), pivot detection** | premessa **Cap.1 di Parte I + Parte III (Cap.15)** — B7 cita la soglia di AC-GO-9, non ri-deriva l'algoritmo pivot |
| **Latenza $L_{max}=30$ s del canale Telegram (M-2 OPEN)** | premessa qualitativa (AC-GO-10); **misura empirica = carryover Appendice E / PENDING-empirico**, NON asserita |

> **Nota di confine — Cap.30 compare due volte di proposito (CARD-FIX-01, F3)**: (i) **oggetto-citato** di AC-GO-11 (premessa §5 sopra — la dashboard di Cap.30 è *ciò che il gate verifica*: "operativa e configurata"); (ii) **esercizio-in-produzione** della dashboard (out-of-scope §6 → FASE-D — il monitoring live in esercizio). Non è una contraddizione. **Cap.30 NON è fonte di alcun `B7-*`**: non è nel perimetro §1 (Cap.31-36 + Cap.5); la **fonte** del requisito su AC-GO-11 è **Cap.36** (`CAP_07_parte_VII.md:594-597`), che cita Cap.30 come oggetto. Nessun requisito B7 va ancorato a Cap.30.

---

## 6. Out-of-scope esplicito (con destinazione)

| Materia | Destinazione |
|---|---|
| **Risultati numerici / verdetti GO-NO-GO / valori d'edge effettivi** (DSR/PBO/$E[R_{net}]$ misurati, esito OOS) | **FASE-D / ruolo `validator`** — PENDING-empirico, MAI asserito in B7 (cardine AC-B7-EDGE) |
| **Monitoraggio di produzione / dashboard live / alert in esercizio** (esecuzione effettiva di Cap.30 in produzione) | **FASE-D** — B7 consolida solo il **criterio** AC-GO-11 (dashboard "operativa e configurata"), non l'esercizio |
| **Implementazione** (codice della pipeline, dell'harness di validazione, del calcolo DSR/PBO/bootstrap) | **FASE-D** — B7 è specifica di requisiti, non implementazione |
| **Matematica interna del modello** (derivazione formule DSR/PBO/bootstrap, NSGA-II, EGARCH, Cox, geometria zone) | **CAP chiusi (Parti III/IV/V)** — opachi; B7 li cita come premessa, non li ri-deriva |
| **Congelamento empirico delle soglie/parametri** ($\theta_*$ definitivi, 10 parametri Parte VI) | **post-go-live / FASE-D** — B7 consolida lo stato "provvisorio, riconsiderato post-go-live" (AC-B7-SOGLIE), non li congela |
| **Schema-dato / canale DAPI / continuità tape** | **B5/B6** (chiusi) — fuori perimetro B7 |
| **Esecuzione ordini / compliance esecuzione** | **B5 / compliance** — B7 eredita il vincolo "solo emissione" come premessa, non lo ri-norma |
| **Fasizzazione / cross-index PHASE-2 / chiusura della spec** | **B8** (spec futura) — B7 non chiude la spec né indicizza i blocchi |

---

## 7. PENDING-empirico (marcare, NON asserire — AC-B7-EDGE)

Tutte le claim sull'edge/esito sono **PENDING-empirico (validator / FASE-D)**; il Developer le marca, non le asserisce:

- **Valore di DSR effettivo** del bundle candidato → PENDING-empirico (validator). B7 consolida solo $\theta_{DSR}=0{,}95$ come **criterio**.
- **Valore di PBO effettivo** → PENDING-empirico (validator). B7 consolida $\theta_{PBO}=0{,}50$ come criterio.
- **$E[R_{net}\mid executed]$ effettivo e $IC_{95\%}$ bootstrap** (AC-GO-3) → PENDING-empirico (validator).
- **CVaR$_{95\%}$, MDD$_{intraday}$, $r_{emit}$, $\rho_{sessions}$ effettivi** (AC-GO-6/7/8/9) → PENDING-empirico (validator).
- **Esito dei 12 AC-GO e decisione GO/NO-GO** → PENDING-empirico (validator); B7 consolida la **checklist e la procedura**, non l'esito.
- **Esito funzionale di AC-GO-10/11/12** (pipeline/dashboard/hash operativi) → PENDING-empirico (FASE-D, verifica funzionale al go-live).
- **Latenza $L_{max}=30$ s effettiva** del canale Telegram → PENDING-empirico (carryover Appendice E, M-2 OPEN).
- **$F$ effettivo** (fold completati: $\{6,7,8\}$ atteso) → dipende dal run di training → PENDING-empirico; B7 consolida la procedura parametrica in $F$, non un $F$ specifico.

**NON pending (criteri/definizioni dichiarati, citare con stato esatto)**: le **definizioni** di DSR/PBO/bootstrap; la **procedura** OOS e i 6 filtri; la **regola** $S=2F$; **$B=2.000$**; i **12 AC-GO** come criteri; le **soglie** come valori di lavoro provvisori (stato esatto); la **specifica di immutabilità** del frozen bundle; la **definizione operativa del successo** (Cap.5).

---

## 8. Done-when (soglie di verdetto)

1. Ogni capitolo del perimetro §1 (Cap.31, 32, 33, 34, 35, 36, Cap.5) che fonda materia di prodotto è coperto da almeno un requisito `B7-*` atomico (N1); concern distinti → ID distinti (DSR≠PBO; recupero/selezione/congelamento/decisione separati; i 12 AC-GO non impacchettati in un unico requisito).
2. **Cardine edge-PENDING (AC-B7-EDGE)**: **zero** asserzioni d'esito o d'edge nel documento; ogni grandezza misurabile è marcata PENDING-empirico (validator/FASE-D); ogni gate è "criterio dichiarato". Una sola asserzione d'esito = **FAIL del blocco**.
3. **Confine di ruolo (AC-B7-VALIDATOR)**: nota esplicita che B7 non emette GO/CONDITIONAL/NO-GO né valori d'edge (esclusiva `validator`).
4. **Stato soglie (AC-B7-SOGLIE)**: ogni soglia consolidata come "valore di lavoro provvisorio, non congelato in Parte VII, riconsiderato post-go-live".
5. **Confine successo (AC-B7-SUCCESSO)**: successo del segnale del motore distinto dal risultato economico dell'operatore.
6. Ogni claim porta `[DOC-INTERNO CAP_07_parte_VII.md:riga]` o `[DOC-INTERNO CAP_01_parte_I.md:riga]`; **floor citazioni 100%**; **0 conclusioni wiki-only** (paper esterni = riferimento bibliografico del capitolo, non fonte di prima istanza); grafia canonica `[CODICE-ESISTENTE]` (vietata `[CODICE-EXISTENTE]`).
7. Premesse §5 citate come tali, NON ri-derivate; invarianti (replay bit-exact) consolidati come invarianti; out-of-scope §6 rispettato.
8. **Cecità**: nessun ID-requisito importato, nessun conteggio/partizione da v2/chunking; ID `B7-*` auto-assegnati da zero.
9. Matrice di tracciabilità completa + nota di rinvio + lista PENDING-empirico presenti nella sezione finale.

**Verdetto**: PASS / CONDITIONAL / FAIL (Reviewer CLI). Lista "Empirico-CLI da verificare" attesa **vuota** (audit documentale no-DAPI, divieto CLI: niente probe di zelo).

---

## 9. Separazione ruoli

- **Planner** (questo task): definisce il perimetro **per capitoli** (Cap.31-36 + Cap.5; **no ID-v2, no conteggio, no partizione** esposti al Developer), gli AC (G1..G11 + B7-EDGE/VALIDATOR/SOGLIE/SUCCESSO), le premesse, gli out-of-scope, i PENDING-empirico. **Non scrive la spec, non fa audit, non committa** questo task card (lo committa l'Orchestratore). La mappatura Req-v2 ↔ capitolo (Sez.8, famiglia `NFR-8.*`) vive **fuori da questa card** (ESITO Orchestratore / Reviewer), MAI esposta al Developer.
- **Developer** (cieco, §0.1): deriva dai **soli** capitoli del perimetro §1; assegna `B7-*` da zero (N1); **non ridefinisce il perimetro, non cerca la mappa v2, non asserisce alcun esito d'edge** (AC-B7-EDGE); rilegge i pin token-per-token; scrive `docs/spec_funzionale/SPEC_FUNZ_01_B7.md` + `reports/REPORT_SPEC_FUNZ_01_B7.md`; scrive `READY_FOR_REVIEW` in `tasks/DEV_STATUS.md`; si ferma.
- **Reviewer** (CLI, GOV-SURFACES-01): audita gli AC + **confronto-copertura vs perimetro B7** sulla mappa di chunking consolidata (`c7ce4be`, riga B7 → Sez.8 `NFR-8.*`), che **il Reviewer** consulta — **non il Developer**; **floor citazioni 100%**; verifica RM-1/RM-3 e — **in primo piano** — il **cardine edge-PENDING** (nessuna asserzione d'esito; ogni gate = criterio dichiarato; confine di ruolo validator esplicitato); **non ripianifica**. Audit documentale no-DAPI in CLI col divieto CLI (niente probe di zelo); lista "Empirico-CLI da verificare" attesa **vuota**. Verdetto PASS/CONDITIONAL/FAIL.

---

*Card B7 (card-sorgente `Business Spec/Final/ACTIVE_TASK_B7.md`, prodotta sotto `ISTRUZIONI_B7-01`). **NON installata**: `tasks/ACTIVE_TASK.md` resta storico su B6; l'install di questa card + l'avvio del ciclo Developer→Review sono **decisione AC**. Nessuna spec scritta, nessun CAP modificato (freeze G-09). Path file CAP verificati reali: `CAP_07_parte_VII.md` (Parte VII, numero romano), `CAP_01_parte_I.md` (Parte I). SHA frozen pinnabili: CAP-07 `b27c1e3`, CAP-01 `e8d5424` (corretto da `b76c32c` in CARD-FIX-01/F4: CAP_01 evoluto post-PASS via FIX-01/03/04, vedi intestazione). La vista-Developer è per soli capitoli: nessun ID-requisito v2, nessun conteggio-target, nessuna partizione esposti — cecità preservata. Vincolo cardine in evidenza: criteri DICHIARATI, mai verdetti; ogni claim d'edge è PENDING-empirico (validator/FASE-D).*
