# REVIEW HA1 — G-12-bis (commit `b350f04`) — audit ostile

**Verdetto: CONDITIONAL** — la G-12-bis ha bonificato **completamente** `.claude/CLAUDE.md` (6/6 residui reindirizzati al marcatore `CAP-XX: CHIUSO PASS` in `tasks/STATO_CORRENTE.md`, zero residui all'indice come discriminatore). **MA** un residuo identico sopravvive in `.claude/BASE_COMUNE.md:31`, file di **precedenza superiore** a CLAUDE.md: lo sweep è stato di nuovo confinato a un solo file — esattamente la lezione che GOV-FIX-02 doveva apprendere.

- **Sede**: CLI. **Oggetto**: commit `b350f04` + stato attuale `.claude/CLAUDE.md`, esteso a `.claude/BASE_COMUNE.md` e `.claude/agents/*.md`.
- **Metodo**: due giri ostili, grep `discrimin` + grep `00_indice|indice` su tutto `.claude/`, valutazione semantica per ogni hit (discriminatore/spia/trigger/condizione della macchina **vs** documento leggibile/check di consegna/N-A legittimi).

---

## 1. Verifica del commit `b350f04` (i 6 punti dichiarati)

`git show --stat b350f04`: `1 file changed, 6 insertions(+), 6 deletions(-)` — solo `.claude/CLAUDE.md`. I 6 reindirizzamenti dichiarati corrispondono 1:1 al diff:

| # | Riga | Prima (`00_indice` discriminatore) | Dopo (marcatore `CHIUSO PASS`) | Esito |
|---|------|------------------------------------|--------------------------------|-------|
| 1 | 34 | "discriminatore `00_indice.md`" | "discriminatore = marcatore `CAP-XX: CHIUSO PASS` in `STATO_CORRENTE.md`" | OK |
| 2 | 63 | "è lo stato di `00_indice.md`: se l'indice riporta già Parte X come PASS..." | "è il marcatore `CAP-XX: CHIUSO PASS`... L'indice... NON è il discriminatore" | OK |
| 3 | 67 (tabella) | "`00_indice.md` riporta già Parte X come PASS" | "`STATO_CORRENTE.md` riporta già `CAP-X: CHIUSO PASS`" | OK |
| 4 | 130 | "**Discriminatore sessione N vs N+1**" | "Documento leggibile... **NON è il discriminatore**" | OK |
| 5 | 150 (template) | "00_indice.md riporta Parte X come PASS" | "STATO_CORRENTE riporta il marcatore `CAP-X: CHIUSO PASS`" | OK |
| 6 | 155 | "in particolare la 4 sull'indice" | "la 4 — il marcatore `CAP-X: CHIUSO PASS` in `STATO_CORRENTE.md`" | OK |

(La riga di tabella 73 e la condizione-4 a riga 141 risultano già al marcatore: erano state convertite in passaggi precedenti, coerenti col commit.)

**Esito punto (1) del mandato**: in `CLAUDE.md`, `grep -ni "discrimin"` → 4 hit (34, 45, 63, 225), **tutti puntano al marcatore**, **ZERO all'indice**. PASS sul perimetro CLAUDE.md.

## 2. Residui SENZA la parola "discriminatore" in CLAUDE.md (punto 2 del mandato)

`grep -ni "00_indice|indice"` su CLAUDE.md → hit a 34, 45, 47, 49, 57, 63, 81, 82, 84, 130, 141, 150, 225. Valutazione per ciascuno:

- **45** (Track B): "il discriminatore... vivono in STATO_CORRENTE + ACTIVE_TASK, NON nell'indice" — corretto, Track B sempre stato così. **Legittimo.**
- **47, 49, 57** (Track B): "condizione-3 (indice) = N/A". **Legittimo** (indice non si tocca in SPEC-FUNZ).
- **81, 82, 84** (check post-Developer): indice "IN REVIEW" come **check di consegna mid-ciclo**, non discriminatore N/N+1. **Legittimo** (indice come documento che il Developer aggiorna a metà ciclo).
- **130, 141, 150, 225**: tutti esplicitano "NON è il discriminatore / documento leggibile / aggiornato dal Planner in N+1". **Coerenti.**

Nessun residuo nascosto in CLAUDE.md: l'indice non è mai più trattato come spia/trigger/condizione della macchina Track A. PASS sul punto (2).

## 3. Coerenza interna della catena chiusura-N / apertura-N+1 (punto 3 del mandato)

- **Chiusura N (chi scrive il marcatore)**: condizione-4, CLAUDE.md:141 — l'Orchestratore della sessione N scrive `CAP-XX: CHIUSO PASS <sha-review>` in `STATO_CORRENTE.md` (Orchestrator-owned, esente dal guard). L'indice NON è scritto in chiusura.
- **Apertura N+1 (chi legge il marcatore)**: macchina a stati CLAUDE.md:63 + riga-tabella 67 — l'Orchestratore di N+1 legge `STATO_CORRENTE.md` per `CAP-X: CHIUSO PASS`; autocheck condizione-4 a CLAUDE.md:155 sullo stesso marcatore. L'indice "Parte X = PASS" è aggiornato dal **Planner** come primo atto di N+1 (CLAUDE.md:141, 150; planner.md:146).
- **Nessun anello interroga l'indice come condizione**: la tabella della macchina (67, 73) e gli autocheck (155) leggono **solo** il marcatore. Catena chiusa e coerente **all'interno di CLAUDE.md**.

PASS sul punto (3) — *limitatamente a CLAUDE.md*. (Vedi §4: la coerenza si rompe a livello inter-documento.)

## 4. Estensione a BASE_COMUNE.md e ai ruoli (punto 4 del mandato) — RESIDUO TROVATO

`grep -ni "discrimin|00_indice|indice"` su tutto `.claude/`:

### Residuo R1 — `.claude/BASE_COMUNE.md:31`

> L'Orchestratore legge i file di stato [...] il **discriminatore di chiusura** [...] sono definiti dalla sezione del track attivo in `CLAUDE.md` (Metodologia: **`00_indice.md`** + 7 condizioni CAP; Business-spec: `STATO_CORRENTE.md`/`ACTIVE_TASK.md` + chiusura adattata, indice N/A).

Questo è **lo stesso residuo** bonificato in CLAUDE.md, sopravvissuto in BASE_COMUNE.md. Tre aggravanti:

1. **Precedenza.** Per `tasks/METODO.md:249` l'ordine è `METODO → BASE_COMUNE → CLAUDE → ruoli`. BASE_COMUNE **vince** su CLAUDE.md: un lettore che applica la regola di precedenza prende la versione **vecchia** (indice = discriminatore Metodologia) e scarta quella nuova di CLAUDE.md. Non è un commento stale innocuo: è la fonte di precedenza superiore che contraddice il fix.
2. **Contrasto esplicito col Track B.** La parentetica oppone "Metodologia: `00_indice.md`" a "Business-spec: `STATO_CORRENTE.md`", cioè codifica proprio la dicotomia che G-12-bis ha eliminato (ora **entrambi** i track usano il marcatore in `STATO_CORRENTE.md`).
3. **Lezione GOV-FIX-02 non applicata.** Ultimo commit su BASE_COMUNE = `5e33914` (GOV-FIX-02, G-15), **antecedente** a `b350f04`. Lo sweep G-12-bis non ha toccato BASE_COMUNE: lo stesso pattern di confinamento a un solo file che il mandato cita come lezione da non ripetere.

`grep -n "CHIUSO PASS|STATO_CORRENTE" BASE_COMUNE.md` → solo L31 e L87 (file di stato single-writer); **nessuna occorrenza del marcatore `CAP-XX: CHIUSO PASS`** in BASE_COMUNE: la voce L31 è l'unica descrizione del discriminatore e punta ancora all'indice.

### Ruoli `.claude/agents/*.md` — nessun residuo

- `planner.md:145-146`: indice = "stato vivente del documento", aggiornato dal Planner a chiusura PASS. **Coerente** col nuovo modello (doc leggibile, Planner-owned in N+1), non discriminatore della macchina.
- `developer.md:174,178,182`: indice "IN REVIEW" / file atteso nel commit = **check di consegna**, non discriminatore. **Legittimo.**
- `spec_planner.md`, `spec_developer.md`: "NON modificare 00_indice" / "indice = N/A". **Legittimo** (Track B).
- `reviewer.md:50`: "multi-indice (DCC/ADCC/BEKK)" — falso positivo lessicale (indice statistico, non l'indice metodologico). Nessun rilievo.
- `validator.md`, `spec_reviewer.md`: nessun hit.

I ruoli non re-introducono l'indice come discriminatore. **L'unico residuo è R1 in BASE_COMUNE.md:31.**

---

## Elenco puntuale dei residui

| ID | File:riga | Testo residuo | Natura |
|----|-----------|---------------|--------|
| R1 | `.claude/BASE_COMUNE.md:31` | "...la sezione del track attivo in `CLAUDE.md` (Metodologia: **`00_indice.md`** + 7 condizioni CAP; Business-spec: `STATO_CORRENTE.md`/`ACTIVE_TASK.md`...)" | Discriminatore di chiusura Track A ancora ancorato a `00_indice.md`, in file di **precedenza superiore** a CLAUDE.md; contraddice b350f04 |

---

## Classificazione per il supervisore

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|-----------------------|
| 1 | Discriminatore di chiusura Track A ancora `00_indice.md` (anziché marcatore `CAP-XX: CHIUSO PASS` in `STATO_CORRENTE.md`); file di precedenza > CLAUDE.md, quindi prevale sul fix b350f04 | `.claude/BASE_COMUNE.md:31` | **BUG REALE** | Sì (obbligatorio) — un BUG REALE in tabella impedisce il PASS (BASE_COMUNE §4 mapping verdetto↔classificazione) |

Fix suggerito (NON applicato — lo decide l'Orchestratore/supervisore): in L31 sostituire la parentetica con "(Metodologia: marcatore `CAP-XX: CHIUSO PASS` in `tasks/STATO_CORRENTE.md` + 7 condizioni CAP; Business-spec: marcatore `SPEC-FUNZ-NN: CHIUSO PASS` in `tasks/STATO_CORRENTE.md` + chiusura adattata, indice N/A)", o più semplicemente rimuovere la menzione di `00_indice.md` come discriminatore e rinviare alla sezione di track in CLAUDE.md. Nota guard: BASE_COMUNE non è esente dall'hook RM-1 di forma, ma il fix non aggiunge righe "verificat*" → nessun blocco atteso; resta protezione `deny` su `.claude/agents/**` (R1 non è in agents/).

---

## Applicazione RM-1 a me stesso

| Asserzione | Prova | Alternative escluse | Alternative NON escluse |
|------------|-------|---------------------|--------------------------|
| "b350f04 cambia 6 righe, solo CLAUDE.md" | `git show --stat b350f04` → "1 file changed, 6 insertions(+), 6 deletions(-)" + diff letto integralmente | Che il commit toccasse altri file (escluso da --stat) | — |
| "In CLAUDE.md ogni hit `discrimin` punta al marcatore, zero all'indice" | `grep -ni discrimin .claude/CLAUDE.md` → righe 34,45,63,225, lette tutte: ognuna nomina il marcatore o nega l'indice | — | — |
| "Gli altri hit `indice` in CLAUDE.md sono check di consegna / N-A / doc leggibile, non discriminatore" | Lette righe 47,49,57,81,82,84,130,141,150: contesto check post-Developer / Track B / "NON è il discriminatore" | — | — |
| "BASE_COMUNE.md:31 ancora ancora il discriminatore Track A a `00_indice.md`" | Riga letta integralmente (Read offset 29): "(Metodologia: `00_indice.md` + 7 condizioni CAP; Business-spec: `STATO_CORRENTE.md`...)" | Che fosse un riferimento a documento leggibile e non al discriminatore — **escluso**: la frase qualifica esplicitamente la parola "**discriminatore di chiusura**" | — |
| "BASE_COMUNE non contiene il marcatore `CHIUSO PASS`" | `grep -n "CHIUSO PASS\|STATO_CORRENTE"` → solo L31, L87; nessuna riga col marcatore | — | — |
| "BASE_COMUNE vince su CLAUDE per precedenza" | `tasks/METODO.md:249`: "`tasks/METODO.md` → `.claude/BASE_COMUNE.md` → `.claude/CLAUDE.md` → file di ruolo" | — | — |
| "Nessun residuo nei ruoli agents/*.md" | `grep -ni "discrimin\|00_indice\|indice" .claude/agents` + lettura contestuale planner.md:145-146, developer.md:174-182, spec_*: tutti check-consegna/N-A/stato-vivente | Che `reviewer.md:50` "multi-indice" fosse un residuo — escluso: è indice statistico (DCC/BEKK) | — |
| "L'ultimo commit su BASE_COMUNE precede b350f04" | `git log -1 --format=%h\ %ci` BASE_COMUNE → `5e33914 2026-06-14 00:22:45`; b350f04 = `00:36:47` stesso giorno, posteriore | — | — |

Nessuna asserzione di questa review richiede DAPI o filesystem non versionato: audit interamente statico-documentale, eseguibile in CLI senza probe. Lista "Empirico-CLI da verificare": **vuota**.

---

### Giri ostili
- **Giro 1**: verifica diff + grep `discrimin` + grep `indice` su CLAUDE.md → CLAUDE.md pulito.
- **Giro 2** ("sono sicuro di aver trovato tutto?"): estensione a BASE_COMUNE + ruoli con pattern allargati (`riporta già Parte`, `Parte X come PASS`, `stato.*00_indice`) → emerge R1 in BASE_COMUNE.md:31, unico residuo. Confermato che è l'**unica** occorrenza del discriminatore-indice sopravvissuta in tutto `.claude/`.
