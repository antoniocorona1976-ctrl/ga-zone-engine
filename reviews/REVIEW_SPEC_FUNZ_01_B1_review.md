# REVIEW — SPEC-FUNZ-01-B1 (Ambito & operatore, ricostruzione cieca modalità B, blocco 1/8)

> **Perimetro**: audit ostile di `docs/spec_funzionale/SPEC_FUNZ_01_B1.md` (34 requisiti: 25 `B1-R`, 5 `B1-CN`, 4 `B1-NFR`) + cross-check di `reports/REPORT_SPEC_FUNZ_01_B1.md`. Capitolo-fonte (sola lettura, freeze G-09): `docs/methodology_v2/CAP_01_parte_I.md`, Cap.1-3.
> **Sede**: **CLI** (Claude Code CLI su `C:\`, GOV-SURFACES-01). Audit documentale **no-DAPI**; divieto CLI attivo (nessuna probe di zelo).
> **Modalità**: review formale piena adattata al non-CAP, **due giri ostili**, su **due fronti** (AC di B1 + confronto-copertura con la v2 congelata).
> **Letture confermate**: `tasks/METODO.md` (RM-1..RM-4 + RACC-METODO-2), `.claude/BASE_COMUNE.md` (§3/§4/§6/§8), `.claude/agents/spec_reviewer.md`, `tasks/ACTIVE_TASK.md` (AC-G1..AC-G11).

---

## VERDETTO (iterazione 1): **PASS**

0 problemi bloccanti. **0 BUG REALE** in tabella. Le citazioni risolvono al 100% token-per-token contro il CAP-fonte; la tracciabilità, l'atomicità, il valore operativo e lo scope sono rispettati; la cecità modalità B regge a tutti i test di traccia; il confronto-copertura con la v2 non rileva buchi (anzi, B1 è più completo della v2 sul perimetro Cap.1-3). Restano alcune **osservazioni minori** (NEUTRO) e **una divergenza informativa** rispetto alla v2 da portare all'attenzione del supervisore, nessuna delle quali blocca o degrada il documento.

---

## FRONTE 1 — Audit ostile sugli AC di B1

### 1.1 Tracciabilità / floor citazioni 100% (AC-G2, AC-G7) — verificato token-per-token

Ho aperto con Read `CAP_01_parte_I.md` (86 righe) e `tasks/QUESTIONS.md`, e riverificato OGNI riga citata. Esito: **15/15 righe CAP risolvono**, **2/2 Q risolvono**.

| Riga citata | Requisiti che la usano | Contenuto reale nel CAP | Esito |
|---|---|---|---|
| `:9` | R-01, R-02, R-03, R-04, R-22 | segnali long/short FIB, futures mini FTSE MIB, IDEM, codice MIB, moltiplicatore 5 EUR/pt, sessione 8-22 CET finestra unica e continua, "emessi e processati dalle 8:00 alle 22:00" | RISOLVE |
| `:11` | R-05, R-06, R-07, R-08, R-09 | target 500pt / 70% mov. strutturale, def. (somma moduli swing), ancoraggio primo min/max post-apertura, soglia minima asimmetrica | RISOLVE |
| `:13` | R-10, R-11, R-12 | natura intraday, estensione multiday ("incrementare il profitto o recuperare la perdita"), tetto 2 giorni dal raw touch | RISOLVE |
| `:15` | CN-01, CN-02, CN-03 | non esegue ordini (vincolo strutturale, non implementativo rivedibile), pubblica su canale di notifica, apertura/invio/gestione/chiusura all'operatore | RISOLVE |
| `:17` | R-13, R-14, R-15 | cross-index DAX/EuroStoxx50/S&P per 3 finalità: classificare regime, validare direzione, stimare rischio sistemico | RISOLVE |
| `:23` | CN-04, R-16, R-17, NFR-01 | retail non professionale MiFID II (dato immutabile), da cellulare in giornata lavorativa, discontinuo, segnali interpretabili/azionabili | RISOLVE |
| `:25` | R-18, CN-05, R-19, R-22 | 1 contratto FIB, moltiplicatore 5 EUR/pt, commissioni 5 EUR/op (apertura+chiusura), 5 EUR=1pt, ciclo=2pt | RISOLVE |
| `:27` | NFR-02 | esempio banda "+- 40pt ad es 41100 41140", b_min=5 | RISOLVE (l'esempio numerico c'è) |
| `:31` | R-20 | stop strutturale ≠ stop personale (−200pt dopo fill, non parametro del modello, non calibrato dal motore) | RISOLVE |
| `:33` | R-21 | rollover problematica operativa specifica FIB, segnali sul contratto attivo | RISOLVE |
| `:39` | NFR-03 | PC mobile, sviluppo/inference real-time/operato sull'hardware esistente | RISOLVE |
| `:41` | NFR-04 | broker Directa SIM, feed real-time deve provenire da Directa non da terzi | RISOLVE |
| `:43` | R-23 | storico FIB 1-min, profondità minima 5 anni | RISOLVE |
| `:45` | R-24 | dati storici e RT DAX/EuroStoxx50/S&P futures per cross-index | RISOLVE |
| `:47` | R-25 | bot Telegram personale, già attivo | RISOLVE |
| `QUESTIONS.md Q-02` | R-08 | ancoraggio primo min/max post-apertura, CHIUSA | RISOLVE |
| `QUESTIONS.md Q-04` | R-12 | tetto 2 giorni trading dal raw touch (nota retroattiva: "decorre dal raw touch, non dall'emissione"), CHIUSA | RISOLVE |

Nessuna citazione che non risolve. **AC-G2 OK, AC-G7 OK (floor 100% raggiunto).**

### 1.2 Atomicità N1 (AC-G1) — OK

- Concern impacchettati nel CAP correttamente spezzati: cross-index `:17` (3 finalità) → R-13/14/15; target `:11` → R-05/06/07/08/09; commissioni `:25` → CN-05 (importo) + R-19 (equivalenza in punti); solo-emissione `:15` → CN-01/02/03; profilo `:23` → CN-04 + R-16 + R-17 + NFR-01.
- **R-03 vs R-04 NON sono ridondanti**: il CAP `:9` esprime due proposizioni distinte ("la sessione di riferimento è 8-22 CET continua" e "i segnali sono emessi e processati dalle 8:00 alle 22:00"); lo split è corretto.
- Borderline esaminati e ritenuti accettabili (un solo concern verificabile, qualificatore non indipendente): CN-04 ("retail MiFID II" + "classificazione immutabile"), R-18 ("1 contratto" + "size out-of-scope"). Non li classifico come finding (vedi Osservazione O-1, NEUTRO).

### 1.3 Valore operativo (AC-G3) — OK

34/34 requisiti hanno il campo `**Valore operativo**` (conteggio meccanico: 34 header `### B1-`, 34 Proposizione, 34 Tracciabilità, 34 Valore operativo). Campionati R-01, R-07, R-09, CN-01, R-19, NFR-02, R-25: ognuno dichiara un valore reale per l'operatore retail FIB che esegue manualmente da cellulare, non boilerplate.

### 1.4 RM-1 / RM-3 / grafia canonica (AC-G4, AC-G5, AC-G6) — OK

- **AC-G4 (RM-1)**: nessuna dichiarazione "verificato X" di prima istanza. L'unico fatto non asserito esplicitamente dal CAP (tick 5pt) è marcato in B1-NFR-02 con il blocco RM-1 completo a 4 righe (`VERIFICA / PROVE / ALTERNATIVE ESCLUSE / ALTERNATIVE NON ESCLUSE`), con l'alternativa non esclusa esplicita ("tick reale diverso, conferma rinviata a B6/CAP-DATA"). Applicazione RM-1 corretta e onesta.
- **AC-G5 (RM-3)**: MiFID II, Borsa Italiana/IDEM, Directa, Telegram tutti etichettati `[WIKI-HINT, da verificare]` e mai fonte unica (ogni requisito regge sul CAP). Verificato sui requisiti R-02, R-03, CN-04, CN-05, NFR-04, R-25.
- **AC-G6 (grafia)**: grep su `CODICE-EXISTENTE` (grafia storica vietata) → **0 occorrenze** in B1. Grafia canonica `[DOC-INTERNO …]` / `[WIKI-HINT, da verificare]` usata ovunque.

### 1.5 Scope "tutto e solo" Cap.1-3 (AC-G9) — OK, nessun scope creep

- **Nessuno sconfinamento** in payload/state-machine/condizioni di emissione/schema-dato/gate/fasizzazione. Verificato: nessun requisito definisce i 12 campi del payload, gli stati terminali, il filtro 80pt (Cap.5), il compute budget (Cap.4) o lo schema CANDLE. Le firme caratteristiche dei blocchi successivi/della v2 (`12 campi`, `tupla strutturata`, `feature tensor`, `bit-exact`, `epoca E5`, `front-month`, `miniFIB`, `PENDING-empirico`) → **0 occorrenze** in B1.
- B1-R-13/14/15 (cross-index) e R-21 (rollover) e NFR-04/R-23/R-24 (dati/feed) restano dichiaratamente "a livello di ambito" senza definire meccanismo/policy/schema: confine rispettato.
- B1-NFR-02 (tick) resta a livello ambito (esempio banda Cap.2 `:27`) col dettaglio schema-dato rinviato a B6: NON è scope creep.
- Nessuna materia di Cap.1-3 omessa: la nota di rinvio §7.2 enumera 11 materie deliberatamente rinviate con destinazione, distinguendo omissione voluta da gap (AC-G10 OK).

### 1.6 AC-G10 (matrice) / AC-G11 (vincolo strutturale) — OK

- Matrice §7.1 a 34 righe (`ID | proposizione | citazione CAP | valore operativo`) + nota di rinvio §7.2. Le citazioni in matrice (`:9`, `:11`, ...) coincidono con quelle dei requisiti.
- B1-CN-01 rende "no esecuzione ordini" come vincolo **strutturale, non scelta implementativa rivedibile** (AC-G11 OK).

### 1.7 (F6) Marcatura blocchi — N/A corretto

Il REPORT §5 dichiara nessun blocco B-N aperto assegnato a B1 (coerente con la task card §2.1 e con CARRYOVER: M-2/B-1→B4, M-GOV-1/B-2→B5, M-1/M-9/M-10→B6, tutti fuori scope B1). Il tick 5pt è cautela RM-1 locale e autocontenuta, non un blocco che contamina altri requisiti → assenza di `[B-N PROVVISORIO]` è corretta (grep `PROVVISORIO` → 0). Nessun requisito dipende da un blocco aperto non marcato.

---

## FRONTE 2 — Confronto-copertura con la v2 congelata (`SPEC_FUNZ_01.md`, PASS `ab7450f`)

Ho aperto la v2 (compito esclusivo del Reviewer in modalità B) e confrontato il perimetro Cap.1-3 di B1 con le **Sezioni 1 e 2 della v2** (ambito/vincoli + destinatario/consumo), integrando i requisiti v2 a fonte CAP_01 che vivono in Sez.7 (CN-7.3 commissioni, R-7.1 sessione, CN-7.1/7.4).

### 2.1 Copertura: nessun buco

Ogni contenuto-di-prodotto di ambito/operatore presente nella v2 (perimetro Cap.1-3) ha un requisito corrispondente in B1:

| Contenuto-prodotto Cap.1-3 | v2 | B1 |
|---|---|---|
| Segnali long/short FIB; strumento FIB/FTSE MIB/IDEM; moltiplicatore 5 EUR/pt | R-1.1 | R-01, R-02, R-22 |
| Sessione 8-22 CET ambito; emissione entro sessione | R-1.x / R-7.1 | R-03, R-04 |
| Target 500pt / 70% + definizione + ancoraggio + soglia minima | R-1.4 | R-05/06/07/08/09 |
| Intraday + multiday + tetto 2gg | R-1.3 | R-10/11/12 |
| No esecuzione (strutturale); pubblica su canale; confine responsabilità | CN-1.1, R-1.2 | CN-01/02/03 |
| Retail MiFID II; cellulare/discontinuo; interpretabili/azionabili | R-2.1 | CN-04, R-16/17, NFR-01 |
| 1 contratto FIB | R-2.2 | R-18 |
| Commissioni 5 EUR/op; 5 EUR=1pt, ciclo=2pt | CN-7.3 | CN-05, R-19 |
| Rollover (ambito); feed Directa; canale Telegram; dati cross-index | R-7.2/CN-7.2/R-2.3/R-9.x | R-21, NFR-04, R-25, R-24 |

**Esito: 0 buchi di copertura.** Al contrario, **B1 copre più della v2 sul perimetro Cap.1-3** (tutti contenuti dei Cap.1-3 non consolidati nella Sez.1-2 della v2): cross-index (R-13/14/15), stop strutturale vs stop personale (R-20), infrastruttura PC locale (NFR-03), storico FIB per il training (R-23). Questo è un punto di qualità a favore di B1, non un finding.

### 2.2 Cecità: nessuna traccia di rottura

- ID v2 (`R-1.*`, `R-2.*`, `R-3.*`, `CN-1.1`, `CN-2.1`) in B1 → **0** (grep). ID B1 auto-assegnati da zero (schema §1).
- Firme testuali caratteristiche della v2 assenti dai Cap.1-3, cercate in B1 → **0** su tutte (`miniFIB`, `FIB pieno`, `front-month`, `epoca E5`, `feature tensor`, `bit-exact`, `self-contained`, `mobile-first`, `12 campi`, `tupla strutturata`, `PENDING-empirico`).
- **Controprova forte**: la qualifica "risk manager bancario" è nel CAP-fonte `:23` E nella v2 (R-2.1), ma **NON in B1** (grep `risk manager` → CAP 1, v2 1, B1 0). Se il Developer avesse copiato la v2 avrebbe verosimilmente importato quella qualifica; averla generalizzata a "operatore retail non professionale" senza riprenderla è indizio coerente di derivazione indipendente. **Cecità confermata: SÌ (nessuna traccia).**

### 2.3 Divergenze sostanziali (riportate al supervisore, non bug)

- **D-1 (tick 5pt)**: la v2 (CN-3.1) **asserisce** il tick 5pt citando `CAP_02_parte_II.md:9`; B1 (NFR-02) lo **marca come assunzione RM-1** perché il suo perimetro è il solo CAP_01 e `CAP_01:27` non asserisce esplicitamente "tick 5pt" (lo si desume dall'esempio banda). La divergenza è **corretta e voluta**: B1 è cieco rispetto a CAP_02 (out-of-scope) e non poteva citarne la riga; la cautela RM-1 è la scelta giusta dato lo scope. A valle (blocco B6/assemblaggio) il tick andrà consolidato citando `CAP_02:9` come fa la v2. Non è un bug di B1; è coerenza con il confine di blocco. Segnalata solo per consapevolezza dell'Orchestratore/supervisore in fase di assemblaggio.

---

## Problemi bloccanti
Nessuno.

## Problemi non-bloccanti
Nessuno (0 BUG REALE).

## Osservazioni minori (NEUTRO — non instradare a Developer salvo decisione supervisore)

- **O-1 (atomicità borderline)**: B1-CN-04 ("retail MiFID II" + "classificazione immutabile per il sistema") e B1-R-18 ("1 contratto" + "gestione size esclusa dal perimetro") impacchettano un'asserzione principale + un suo qualificatore derivante dalla stessa riga CAP. Ho valutato che restano una sola proposizione verificabile (il qualificatore non è un concern indipendente) → atomicità rispettata. Annoto come NEUTRO per trasparenza, non come "da spezzare".
- **O-2 (omissione lessicale innocua)**: B1-R-23 omette l'aggettivo "continuo" presente in CAP `:43` ("serie storica del FIB **continuo**"). A livello di ambito non altera il senso del requisito; il dettaglio (serie continua, stitching) è esplicitamente rinviato in §7.2. NEUTRO.

---

## Tabella "Classificazione per il supervisore"

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|----------------------|
| O-1 | Atomicità borderline CN-04 / R-18 (asserzione + qualificatore stessa riga CAP) | `SPEC_FUNZ_01_B1.md:134-137, :154-157` | NEUTRO | No (atomicità giudicata rispettata) |
| O-2 | R-23 omette "continuo" del CAP `:43` (innocuo a livello ambito) | `SPEC_FUNZ_01_B1.md:214-217` | NEUTRO | No |
| D-1 | Divergenza tick 5pt vs v2 CN-3.1 (B1 usa cautela RM-1, v2 asserisce da CAP_02): coerente con lo scope cieco di B1 | `SPEC_FUNZ_01_B1.md:188-198` | NEUTRO (informativa) | No — nota per l'assemblaggio post-B8 |

Nessun BUG REALE, nessun MIGLIORA PERFORMANCE, nessun RISCHIO PEGGIORAMENTO. Tutti i finding sono NEUTRO ⇒ non vanno a Developer senza approvazione del supervisore (e qui non c'è ragione di instradarli).

---

## Applicazione RM-1 a me stesso

- **"Citazioni risolvono al 100% token-per-token"** → PROVE: ho letto `CAP_01_parte_I.md` integralmente (86 righe, Read in questa sessione) e ho confrontato ogni riga citata col testo reale (tabella §1.1). ALTERNATIVA ESCLUSA: che una riga citata non contenga il fatto asserito — esclusa per ispezione diretta riga-per-riga. ALTERNATIVA NON ESCLUSA: nessuna.
- **"Q-02/Q-04 chiuse e pertinenti"** → PROVE: Read di `tasks/QUESTIONS.md`; Q-02 (riga 11-17, "CHIUSA", ancoraggio primo min/max), Q-04 (riga 31-39, "CHIUSA", tetto 2gg dal raw touch, nota retroattiva). ESCLUSA: Q inesistente/aperta — esclusa dal testo letto.
- **"Cecità confermata"** → questa è una conclusione su **assenza di prova di rottura**, non una prova di assenza assoluta. PROVE: grep su ID v2 (0), grep su 12 firme caratteristiche v2 (0), controprova "risk manager bancario" presente in CAP+v2 ma assente in B1 (indizio positivo). ALTERNATIVA NON ESCLUSA: che il Developer abbia parafrasato concetti v2 in modo non greppabile pur restando dentro i Cap.1-3 — non escludibile per via testuale, ma in tal caso il contenuto resterebbe comunque tracciato al CAP (fronte 1 OK) e non costituirebbe danno. Concludo "nessuna traccia rilevata", non "impossibile copiatura".
- **"Nessun buco di copertura vs v2"** → PROVE: Read Sez.1-2 v2 + requisiti v2 a fonte CAP_01 in Sez.7; mappatura §2.1 voce-per-voce. ESCLUSA: che un contenuto v2 di ambito non abbia corrispondente B1 — esclusa dalla mappatura completa.
- **"Conteggio 34 req con 3 campi ciascuno"** → PROVE: grep meccanico (34 header / 34 Proposizione / 34 Tracciabilità / 34 Valore operativo).

---

## Lista "Empirico-CLI da verificare"

**VUOTA** (come atteso). Il track non produce fatti empirici nuovi: B1 consolida fatti già chiusi nei Cap.1-3 di CAP_01 (frozen). L'unica materia che richiederebbe prova empirica (tick 5pt effettivo del FIB) è correttamente NON asserita da B1 (cautela RM-1) e rinviata a B6/CAP-DATA; non eseguo probe (divieto CLI). Nessun handoff alla sede CLI necessario.

---

*Review prodotta dallo spec_reviewer in sede CLI. CAP-01 non riaperto né modificato (freeze G-09 rispettato). Documento B1 non modificato (non è il Reviewer a riscriverlo). `SINTESI_GOVERNANCE_GA_PER_AC.md` lasciata dirty com'era. `DEV_STATUS.md` non azzerato (lo fa l'Orchestratore alla chiusura).*
