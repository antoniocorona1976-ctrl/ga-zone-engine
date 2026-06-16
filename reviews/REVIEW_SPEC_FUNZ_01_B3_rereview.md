# RE-REVIEW (DELTA) — SPEC-FUNZ-01-B3 micro-pass OM-1

> File di re-review **di delta**. Si legge in coda alla review piena `reviews/REVIEW_SPEC_FUNZ_01_B3_review.md` (PASS originaria, `e94ef17`). Certifica SOLO il delta del micro-pass OM-1 (commit `a78c46a`) e l'assenza di regressioni.

## Header

- **Tipo**: re-review **di delta** (NON review piena ex-novo). B3 era gia PASS (review `e94ef17`, chiusura `389220c`). Qui certifico SOLO il delta del micro-pass OM-1 e l'assenza di regressioni.
- **Oggetto del delta**: commit `a78c46a` (`[SPEC-FUNZ-01-B3] micro-pass OM-1, split B3-CN-09->B3-CN-09+B3-CN-12`), parent `083fb1a`. Diff di sostanza circoscritto a `docs/spec_funzionale/SPEC_FUNZ_01_B3.md` (8 righe) + `reports/REPORT_SPEC_FUNZ_01_B3.md` (conteggio e AC).
- **Fonte autoritativa (sola lettura, frozen G-09)**: `CAP_02_parte_II.md:393` (chiuso PASS `a1625df`). NON modificata, NON riaudita nei suoi AC.
- **Sede**: **CLI** (GOV-SURFACES-01), su `C:\Users\AN\Documents\Projects\ga-zone-engine`. Audit documentale **no-DAPI**, divieto CLI rispettato (nessuna probe eseguita).
- **Letture obbligatorie eseguite**: (1) `tasks/METODO.md` (RM-1..RM-4 + RACC-METODO-2); (2) `.claude/BASE_COMUNE.md` (classificazione finding par.4, onesta claim->evidenza par.8); (3) `.claude/agents/spec_reviewer.md`; (4) `reviews/REVIEW_SPEC_FUNZ_01_B3_review.md` (la review PASS originaria, finding #1/OM-1 al par.7 e tabella par.8 riga 1); (5) `tasks/ACTIVE_TASK.md` par.10 (mandato del micro-pass).

---

## VERDETTO DELTA: **PASS**

OM-1 chiuso correttamente. Split atomico verificato. Citazione `:393` di B3-CN-12 risolve token-per-token. 0 regressioni: delta circoscritto allo split, nessuna rinumerazione a cascata, gli altri 61 requisiti intatti. Tabella "Classificazione per il supervisore" del delta: **VUOTA di BUG REALE** (i NEUTRO residui #2/#3 della review originaria non sono stati toccati e restano fuori mandato, come da decisione AC). **0 BUG REALE** => PASS.

---

## 1. OM-1 chiuso (N1, AC-G1)

Verificato sul documento (`SPEC_FUNZ_01_B3.md:254-258`):
- **B3-CN-09** (`:254`) ora porta **la sola proposizione (a)** *indipendenza-di-stato*: "La submacchina **non modifica mai lo stato del segnale**: il segnale e terminato in `target_1_hit` prima che la submacchina inizi a tracciare." La frase sui log (precedentemente impacchettata) e stata rimossa. Una sola proposizione verificabile. **Atomico.**
- **B3-CN-12** (`:257`, nuovo) porta **la sola proposizione (b)** *separazione-log*: "I **log della submacchina sono separati** dai log del lifecycle del segnale e referenziati dal `signal_id` del segnale che ha innescato il tracking." Una sola proposizione verificabile. **Atomico.**

Il finding OM-1 (review originaria par.7 e tabella par.8 riga 1: "B3-CN-09 impacchetta indipendenza-di-stato + separazione-log") e **risolto**: i due concern sono ora due ID distinti, ciascuno con una sola proposizione. **OM-1 CHIUSO.**

## 2. Tracciabilita token-per-token di `:393` per B3-CN-12 (AC-G2/AC-G7)

Read di `CAP_02_parte_II.md:393` (riga integrale): "**Indipendenza dalla state machine del segnale**: la submacchina **non modifica lo stato del segnale** in nessuna circostanza. Il segnale e terminato in `target_1_hit` prima ancora che la submacchina inizi a tracciare. I log della submacchina sono separati dai log del lifecycle del segnale (Cap.10) e sono scritti in un registro distinto, referenziato dal `signal_id` del segnale che ha innescato il tracking."

La riga `:393` **afferma entrambe le proposizioni**:
- proposizione (a) di B3-CN-09 = "la submacchina non modifica lo stato del segnale ... Il segnale e terminato in target_1_hit prima ..." -> **risolve**;
- proposizione (b) di B3-CN-12 = "I log della submacchina sono separati ... referenziato dal signal_id ..." -> **risolve token-per-token**.

Quindi **entrambi** B3-CN-09 e B3-CN-12 tracciano legittimamente a `:393` (la stessa riga afferma le due proposizioni insieme, come dichiarato dal mandato par.10 e dal REPORT). **Nessun finding di tracciabilita.**

## 3. Valore operativo (AC-G3)

B3-CN-12 (`:258`) dichiara *Valore operativo*: "garantisce all'operatore che la traccia di cio che accade alla posizione dopo `target_1_hit` e registrata distintamente dall'esito del segnale, cosi che reporting e track record restino leggibili e non si mescolino." Valore operativo coerente con la proposizione (separazione-log), categoria *operativo* (non *sistema/validazione*) — coerente con il mandato (valore operativo per entrambi, come l'originale B3-CN-09). **OK.**

## 4. Zero regressioni (delta circoscritto allo split)

- **Conteggio ID nel documento** (grep deduplicato): **47 R + 12 CN + 3 NFR = 62**. Coincide col REPORT aggiornato. **OK.**
- **Sequenza CN 01..12 senza buchi ne riuso**: verificato via grep (B3-CN-01..B3-CN-12 tutti presenti, una volta ciascuno). **OK.**
- **Nessuna rinumerazione a cascata**: il diff `083fb1a..a78c46a` tocca SOLO i blocchi B3-CN-09/B3-CN-12 (`:254-258`), il bullet "Indipendenza della submacchina" della Sezione 7 (`:277`) e la riga matrice par.8.1 (`:348`). Gli ID B3-CN-10/11 e tutti gli altri (R-01..47, NFR-01..03) **intatti**. B3-CN-12 inserito come prossimo ID libero (no churn sui riferimenti incrociati). **OK.**
- **Sezione 7 coerente**: bullet "Indipendenza della submacchina (...) -> B3-CN-09; separazione dei log della submacchina (referenziati dal signal_id) -> B3-CN-12." Rimando corretto a entrambi gli ID. **OK.**
- **Matrice par.8.1 coerente**: riga B3-CN-09 ridotta a "submacchina non modifica lo stato del segnale | :393 | operativo"; **aggiunta** riga B3-CN-12 "log della submacchina separati, referenziati dal signal_id | :393 | operativo". Una riga per requisito. **OK.**
- **REPORT conteggio = 62**: par.1 (61->62, 11->12 CN), par.4 Misura (DOPO: 62, lista Cap.11 include CN-12), tabella AC (AC-G1 e AC-G11 aggiornate), "Applicazione RM-1 a me stesso" (conteggio + blocco split a :393). **OK.**
- **Finding #2/#3 (NEUTRO) non toccati**: il diff non modifica B3-R-42 (matrice :370 intestazione) ne B3-R-46 (rinvio "Parte V"); restano come da review originaria. **OK** (fuori mandato, come prescritto).

## 5. Nessuno scope creep introdotto dal delta

B3-CN-12 resta materia Cap.11 (`:393`): la separazione-log e usata come **proprieta strutturale di indipendenza** della submacchina (i log distinti per signal_id sono il supporto del fatto che la submacchina non interferisce con lo stato del segnale). Il testo del requisito si ferma a "separati e referenziati dal signal_id" — **non** importa il **formato**, la **persistenza** o il **versionamento** del log (materia B5/Cap.10). Da notare: la riga `:393` stessa rimanda a "(Cap.10)" per i log del lifecycle, ma B3-CN-12 **non** ha tirato dentro Cap.10: ha citato solo `:393` per la proprieta di separazione strutturale. **Nessuno sconfinamento in B5.** Confine identico a quello gia validato per B3-CN-09 nella review originaria (par.4, terzo punto). **OK.**

## 6. Cecita (delta)

Il delta non introduce ID ne frasi importati da v2/B1/B2. B3-CN-12 e un ID auto-assegnato (prossimo libero nella sequenza locale B3-CN). Il testo deriva direttamente da `:393` del CAP (verificato token-per-token al par.2). Il REPORT dichiara "nessuna Read su SPEC_FUNZ_01.md / B1 / B2 / chunking / _v1_storico" per il micro-pass. **Cecita preservata.** (Per il micro-pass la cecita non era piu strettamente richiesta — il confronto-copertura era gia chiuso nella review originaria — ma resta buona prassi e non e stata violata.)

---

## 7. Problemi bloccanti (delta)

Nessuno.

## 8. Tabella "Classificazione per il supervisore" (delta)

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|------------------------|
| — | (nessun finding nuovo introdotto dal delta) | — | — | — |

**0 BUG REALE introdotti dal delta.** I NEUTRO residui #2 (matrice B3-R-42) e #3 (rinvio Parte V B3-R-46) della review originaria restano invariati e fuori mandato (decisione AC: micro-pass sul solo OM-1). Verdetto delta **PASS**.

## 9. Applicazione RM-1 a me stesso (delta)

- **":393 afferma entrambe le proposizioni (a) e (b)"** — PROVE: Read di `CAP_02_parte_II.md:393` integrale; la riga contiene letteralmente sia "la submacchina non modifica lo stato del segnale in nessuna circostanza. Il segnale e terminato in target_1_hit prima ancora ..." (a) sia "I log della submacchina sono separati ... referenziato dal signal_id ..." (b). ALTERNATIVE ESCLUSE: che (b) tracciasse a una riga diversa (esclusa: :393 contiene esplicitamente la frase sui log separati; nessun'altra riga del Cap.11 la duplica nel perimetro letto :385-403). ALTERNATIVE NON ESCLUSE: nessuna.
- **"Conteggio 62 (47 R + 12 CN + 3 NFR), nessuna rinumerazione a cascata"** — PROVE: grep deduplicato degli ID nel documento (47/12/3); sequenza CN 01..12 contigua; diff `083fb1a..a78c46a` ispezionato riga per riga (tocca solo :254-258, :277, :348 del documento). ALTERNATIVE ESCLUSE: che lo split avesse rinumerato altri ID (esclusa: B3-CN-10/11 e tutti gli R/NFR invariati nel diff). ALTERNATIVE NON ESCLUSE: nessuna.
- **"Nessuno scope creep in B5"** — PROVE: lettura del testo B3-CN-12 (`:257`): si ferma a "separati e referenziati dal signal_id" (proprieta strutturale), non cita formato/persistenza/Cap.10. ALTERNATIVE NON ESCLUSE: nessuna.
- **"OM-1 chiuso"** — PROVE: B3-CN-09 (`:254`) ridotto alla sola (a); B3-CN-12 (`:257`) porta la sola (b); confronto col finding originario (par.7 review, tabella par.8 riga 1). ALTERNATIVE NON ESCLUSE: nessuna.

---

## 10. Empirico-CLI da verificare (delta)

**VUOTA** (come atteso). Il delta consolida una proposizione gia chiusa nel CAP-02 frozen (`:393`); nessuna asserzione richiede prova empirica contro DAPI o filesystem locale. Divieto CLI rispettato: nessuna probe eseguita.

---

*Re-review di delta prodotta in sede CLI, audit documentale no-DAPI, focalizzata sul solo micro-pass OM-1 (commit a78c46a). CAP-02 non riaudito (frozen G-09). Documento B3 e CAP non modificati dalla review. DEV_STATUS NON azzerato (lo fa l'Orchestratore alla chiusura).*
