# REVIEW GOV-FIX-01 — audit ostile del delta

## Header
- **Perimetro**: delta `git diff 60bcac0..HEAD` (HEAD = `57225e0`) limitato ai file `tasks/METODO.md`, `.claude/`, `scripts/claude_hooks/rm_guard.py`, `tasks/CARRYOVER.md`.
- **Sede**: CLI (working dir `C:\Users\AN\Documents\Projects\ga-zone-engine`). Audit documentale no-DAPI; nessun probe di zelo.
- **Riferimento normativo**: `Business Spec/Final/ISTRUZIONI_GOV-FIX-01.md` (patch P-01..P-17, Passi 1-9).
- **Mandato**: ristretto a 3 domande — (1) fedeltà alle istruzioni patch-per-patch; (2) nuove contraddizioni fra documenti normativi; (3) ri-esecuzione dei grep di VERIFICA.
- **Commit nel range**: `c2521df` (C1 METODO), `a286e74` (C2 guard), `3b04953` (C3 ruoli spec+developer), `a1d50ce` (C4 BASE_COMUNE+CLAUDE), `57225e0` (C5 CARRYOVER). Scoping per-commit conforme a Passo 10 (C1..C5): ogni commit tocca esattamente i file previsti, nessun file estraneo.

---

## VERDETTO: CONDITIONAL

Le 16 patch su 17 (P-01..P-16) sono applicate **fedelmente e verbatim** rispetto alle istruzioni; tutte le VERIFICA dei Passi 1-9 danno l'esito atteso; nessuna **nuova contraddizione sostanziale** fra i documenti normativi. **Un solo difetto bloccante**: **P-17** (M-GOV-1 in `tasks/CARRYOVER.md`) ha aggiunto la voce **non "nello stesso formato delle voci M esistenti"** come richiesto, ma **incollata sulla stessa riga di M-16** tramite `||`, producendo una riga di tabella Markdown malformata. La voce non risulta come riga propria del registro M-promemoria.

---

## Problemi per gravità

### BLOCCANTI

**B1 — P-17: M-GOV-1 incollata alla riga di M-16 (riga di tabella malformata).**
`tasks/CARRYOVER.md:36`. L'istruzione P-17 chiede di "aggiungere, **nello stesso formato** delle voci M esistenti, la voce" M-GOV-1. Tutte le voci esistenti sono righe autonome che iniziano con `| M-x | ...`. Invece M-GOV-1 è stata appesa in coda alla riga di M-16, separata solo da ` || `:
```
...coefficients.) || M-GOV-1 | GOV-FIX-01 (13/06/2026) | orario FIB... | CAP-DATA-01 / probe V-1 | APERTO |
```
Evidenza meccanica:
- La riga 36 contiene **12 pipe** (`awk` gsub) contro le **6** di una riga ben formata a 5 celle → sono due righe fuse.
- Nessuna riga del file inizia con `^| M-GOV-1` (grep exit 1).
- Al baseline `60bcac0` la riga di M-16 terminava pulita con `coefficients.) |` + newline; il commit `57225e0` ha **sostituito il newline** con ` || M-GOV-1 ...` (C5 = `1 insertion(+), 1 deletion(-)` sulla stessa riga, non un'aggiunta di riga nuova).

**Impatto**: in rendering Markdown M-GOV-1 non è una riga; il suo contenuto diventa celle extra della riga di M-16 (10 celle invece di 5). Il registro CARRYOVER è l'input autoritativo del Planner/Orchestratore della nuova sessione (`.claude/BASE_COMUNE.md` §7, `tasks/METODO.md` Riferimenti): una voce M mal registrata è un difetto di sostanza, non cosmetico. Un grep su `M-GOV-1` trova comunque il testo (per questo una verifica ingenua non lo intercetta), ma la voce non è correttamente incardinata nel registro. → **BUG REALE**, da rilavorare: M-GOV-1 va spostata su riga propria `| M-GOV-1 | ... | APERTO |` preceduta da newline, lasciando la riga di M-16 chiusa con `coefficients.) |`.

### NON BLOCCANTI

Nessuno.

### OSSERVAZIONI MINORI

**O1 — Heading "★ Sede — bi-sede CLI + Web" residuo in `spec_reviewer.md:18`.**
P-07 ha sostituito (come da istruzione, e SOLO) le due righe-corpo ANCORA 1/ANCORA 2, portandole a "Sede del track: CLI". Il **titolo di sezione** (riga 18) recita ancora "★ Sede — bi-sede CLI + Web (eredita BASE_COMUNE §3)", e le letture obbligatorie (riga 14) + la description frontmatter (riga 3) citano ancora "reviewer bi-sede CLI+Web". Non è una violazione delle istruzioni (P-07 era scopato alle sole due righe-corpo; il resto era fuori scope e correttamente non toccato), ma resta una **tensione titolo/corpo**: il corpo ora normates CLI come sede del ciclo, il titolo dice "bi-sede". Coerente con `BASE_COMUNE.md` §3 (che resta legittimamente "BI-SEDE" come capacità di piattaforma, con il blockquote P-04 che instrada il track B su CLI). Candidato a cleanup in tranche 2 (allineamento etichette/identità ruoli, cfr. G-11/G-08). → **NEUTRO**, non mandare a Development in questa tranche.

**O2 — `tasks/CARRYOVER.md` è esente dal guard RM-1 ma è un file di stato a singolo writer.**
Osservazione di contesto (non un difetto del delta): l'esenzione `RM1_EXEMPT_FILES` su `tasks/CARRYOVER.md` ha permesso al commit C5 di passare nonostante la riga malformata; il guard verifica la forma RM-1, non la well-formedness della tabella. Coerente con il "Limite dichiarato" già scritto in `METODO.md:227`. → **NEUTRO**.

---

## Domanda (1) — Fedeltà patch-per-patch

| Patch | File | Esito | Note |
|---|---|---|---|
| P-01 (C1) | `tasks/METODO.md` | OK | 3 blocchi (GOV-SURFACES-01 r.231, Precedenza r.237, Freeze r.243) inseriti verbatim, **prima** di `## Riferimenti` (r.249). |
| P-02 (C2) | `scripts/claude_hooks/rm_guard.py` | OK | `docs/spec_funzionale/` aggiunto a `RM1_EXEMPT_PREFIXES` (r.49) nello stesso formato (prefisso con slash finale). Nessun'altra modifica al file. |
| P-03 (C4) | `.claude/BASE_COMUNE.md` | OK | Riga matrice splittata in due righe (CAP-XX→Web; SPEC-FUNZ→CLI), verbatim. |
| P-04 (C4) | `.claude/BASE_COMUNE.md` | OK | Blockquote sede track B sostituito verbatim (r.56). |
| P-05 (C4) | `.claude/CLAUDE.md` | OK | Bullet "Sede Reviewer" sostituito verbatim (r.49 area). |
| P-06 (C3) | `.claude/agents/spec_planner.md` | OK | Segmento "Sede" sostituito verbatim; frase "Empirico-CLI attesa vuota" preservata (r.33). |
| P-07 (C3) | `.claude/agents/spec_reviewer.md` | OK | ANCORA 1 (r.19) e ANCORA 2 (r.20) sostituite verbatim. Titolo sezione non toccato (corretto: fuori scope) → vedi O1. |
| P-08 (C3) | `.claude/agents/spec_developer.md` | OK | Paragrafo "Marcatura della contaminazione" aggiunto dopo il paragrafo F6 (r.43), verbatim. |
| P-09 (C3) | `.claude/agents/spec_reviewer.md` | OK | Item 7 "(F6) Marcatura blocchi" aggiunto dopo item 6 (r.34), verbatim. |
| P-10a (C4) | `.claude/BASE_COMUNE.md` | OK | Riga "Mapping verdetto↔classificazione" aggiunta dopo "BUG REALI vanno sempre a Developer" (r.64), verbatim. Ancora intatta e unica. |
| P-10b (C4) | `.claude/BASE_COMUNE.md` | OK | Riga PASS/NEUTRO sostituita verbatim (r.67). |
| P-11 (C3) | `.claude/agents/spec_reviewer.md` | OK | Frammento verdetto PASS → "0 bloccanti **e 0 BUG REALE in tabella**" (r.38); resto della riga invariato. |
| P-12 (C3) | `.claude/agents/spec_reviewer.md` | OK | "campione esteso" → "100% delle citazioni dei requisiti (floor di default...)" (r.28), verbatim. |
| P-13 (C4) | `.claude/CLAUDE.md` | OK | Bullet "Etichetta RM-3 sui depositi" aggiunto **subito sotto** il bullet "Input dell'Orchestratore = autoritativo" (r.207), verbatim; il bullet-ancora non modificato. |
| P-14a (C4) | `.claude/CLAUDE.md` | OK | Frammento condizione (7) → marcatore `SPEC-FUNZ-NN: CHIUSO PASS <sha-review>` (r.49), verbatim. |
| P-14b (C4) | `.claude/CLAUDE.md` | OK | Tabellina "Macchina a stati Track B" aggiunta dopo il bullet Chiusura (r.51-59), verbatim. |
| P-15 (C4) | `.claude/CLAUDE.md` | OK | Riga orario FIB sostituita verbatim (r.28); Commissioni/Broker invariati. |
| P-16 (C3) | `.claude/agents/developer.md` | OK | Riga orario FIB sostituita verbatim (r.35), identica a P-15. |
| **P-17 (C5)** | **`tasks/CARRYOVER.md`** | **STOP/DIFETTO** | Voce M-GOV-1 presente nel testo ma **NON nel formato delle voci esistenti**: incollata alla riga di M-16 via `||` invece che su riga propria. Vedi B1. |

Conclusione (1): 16/17 fedeli e verbatim. P-17 non rispetta il vincolo "nello stesso formato delle voci M esistenti".

## Domanda (2) — Nuove contraddizioni fra documenti normativi

Esito: **nessuna nuova contraddizione sostanziale**. Verifiche puntuali:

- **Sede CLI track B** (rimozione del default Web-statico): coerente across `METODO.md` §Superfici (CLI = sede unica ciclo spec), `BASE_COMUNE.md` §3 blockquote (P-04) + matrice (P-03), `CLAUDE.md` bullet Sede Reviewer (P-05), `spec_planner.md` (P-06), `spec_reviewer.md` corpo (P-07). Tutte convergono su "CLI per il ciclo spec, Web solo per probe-review RM-4 instradata". `grep -rn "Web-statico" .claude/` → **0 occorrenze**. Residuo solo testuale/identitario nel titolo+frontmatter di `spec_reviewer.md` (O1), non normativo.
- **Mapping verdetto↔classificazione**: `BASE_COMUNE.md` §4 (≥1 BUG REALE ⇒ non-PASS, al più CONDITIONAL) ↔ `spec_reviewer.md` r.38 (PASS = 0 bloccanti **e** 0 BUG REALE). Coerenti. La triade PASS / CONDITIONAL (solo non-bloccanti) / FAIL (≥1 bloccante) resta internamente consistente con "BUG REALE = almeno un problema non bloccante".
- **Macchina a stati Track B (P-14b) ↔ 7 condizioni di chiusura (P-14a)**: la riga "Review PASS e STATO_CORRENTE senza marcatore CHIUSO PASS → chiusura B (7 condizioni), scrivi il marcatore" è coerente con la condizione (7) che prescrive la riga-marcatore `SPEC-FUNZ-NN: CHIUSO PASS <sha-review>`. `grep "CHIUSO PASS" .claude/CLAUDE.md` → 3 occorrenze (cond.7 + 2 righe tabella), ≥2 come atteso. Le 5 righe della tabella B non contraddicono le 7 condizioni; "indice = N/A" è ribadito (condizione-3 = N/A).
- **Precedenza normativa (P-01)**: l'ordine METODO → BASE_COMUNE → CLAUDE → ruoli con eccezione-identità è coerente con la clausola di precedenza già in `CLAUDE.md` §Identità; non introduce conflitto.

## Domanda (3) — Ri-esecuzione dei grep di VERIFICA (comando + output)

| Passo | Comando | Output | Esito atteso |
|---|---|---|---|
| 0.4 | `grep -n "methodology_v2" scripts/claude_hooks/rm_guard.py` | `49:RM1_EXEMPT_PREFIXES = (... "docs/methodology_v2/", "docs/spec_funzionale/")` | trovato ✔ |
| 1.4 | `grep -n "spec_funzionale" scripts/claude_hooks/rm_guard.py` | `49: ... "docs/spec_funzionale/")` (≥1 nella struttura esenzioni) | ≥1 ✔ |
| 2 | `grep -n "GOV-SURFACES-01" tasks/METODO.md` | `231:## Superfici di esecuzione (GOV-SURFACES-01)...` | 1, prima di Riferimenti (r.249) ✔ |
| 2 | `grep -n "Precedenza fra documenti normativi" tasks/METODO.md` | `237:## Precedenza fra documenti normativi...` | 1 ✔ |
| 2 | `grep -n "Freeze dei CAP chiusi PASS" tasks/METODO.md` | `243:## Freeze dei CAP chiusi PASS...` | 1 ✔ |
| 3 | `grep -rn "Web-statico" .claude/` | (vuoto, exit 1) | **0** ✔ |
| 4 | `grep -n "B-N PROVVISORIO" .claude/agents/spec_developer.md .claude/agents/spec_reviewer.md` | spec_developer r.43; spec_reviewer r.34 | ≥1 per file ✔ |
| 5 | `grep -n "non può emettere PASS" .claude/BASE_COMUNE.md` | `64: ... non può emettere PASS ...` | 1 ✔ |
| 5 | `grep -n "può applicarle" .claude/BASE_COMUNE.md` | (vuoto, exit 1) | **0** ✔ |
| 5 | `grep -n "0 BUG REALE in tabella" .claude/agents/spec_reviewer.md` | `38: ... 0 BUG REALE in tabella ...` | 1 ✔ |
| 6 | `grep -n "campione esteso" .claude/agents/spec_reviewer.md` | (vuoto, exit 1) | **0** ✔ |
| 6 | `grep -n "100% delle citazioni" .claude/agents/spec_reviewer.md` | `28: ... 100% delle citazioni dei requisiti ...` | 1 ✔ |
| 7 | `grep -n "Etichetta RM-3 sui depositi" .claude/CLAUDE.md` | `207: ... ` (riga subito dopo "Input dell'Orchestratore = autoritativo") | 1 ✔ |
| 8 | `grep -n "CHIUSO PASS" .claude/CLAUDE.md` | r.49 (cond.7), r.55, r.59 | ≥2 ✔ |
| 9 | `grep -n "M-GOV-1" tasks/CARRYOVER.md` | r.36 (ma **incollata alla riga M-16**, non riga propria — vedi B1) | trovata, ma formato errato ✖ |

**Inventario "9:00"** (`grep -rn "9:00\|9\.00" docs/ tasks/ .claude/ --include="*.md"`): 19 hit, tutti legittimi, **nessuno** è un orario di sessione FIB sbagliato:
- `docs/methodology_v2/CAP_02_parte_II.md:227` — cita la finestra continua 8:00-22:00 e il ritiro dell'osservazione M-3 su presunta asta 8:00-9:00 (contenuto **corretto**, conferma negoziazione continua).
- `CAP_08_parte_8.md:116-118,125` — orari storici epoche E2/E3/E4 (09:00-17:40/17:50/20:30): dati storici legittimi, non sessione attuale.
- `CAP_09_parte_9.md:98,433`, `SPEC_FUNZ_01.md:258`, `SESSION_HANDOFF_CAP-DATA-02_to_CAP-DATA-03.md:41` — chiusura negoziazione/settlement front-month alle 09:00 CET del giorno di scadenza + finestra rollover 08:00-09:00: orario di settlement, non sessione.
- `CAP_10_parte_10.md:104`, `tasks/PROBE_RECUPERO_GAP_DAPI.md`, `RIPRESA_20260529.md`, `HANDOFF_PROBE_DAPI_20260528.md`, `STATO_CORRENTE.md:35` — finestra probe V-1 09:00-09:30 e lancio capture morning: orario di probe, non sessione.
- `tasks/CAP-DATA-01.md:112`, `SESSION_HANDOFF_CAP-07_to_CAP-DATA-01.md:163,167,486` — epoche storiche/attuale 09:00-22:00 in tabelle epoche dati storici (da retro-audit, fuori scope del freeze).

Le occorrenze dentro `docs/methodology_v2/CAP_*` ricadono nel freeze (Passo 2) e vanno solo elencate (qui sopra), non modificate. **Nessun file modificato in questo passo** (conforme).

---

## Tabella "Classificazione per il supervisore"

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|-----------------------|
| 1 | M-GOV-1 incollata alla riga di M-16 via `||`: riga di tabella malformata, voce M non registrata come riga propria (violazione "stesso formato delle voci esistenti" di P-17). 12 pipe sulla riga, nessuna riga inizia con `\| M-GOV-1`. | `tasks/CARRYOVER.md:36` | BUG REALE | **Sì** (obbligatorio): spostare M-GOV-1 su riga propria, ripristinare il newline dopo `coefficients.) \|` di M-16. |
| 2 | Heading "★ Sede — bi-sede CLI + Web" + frontmatter/letture "reviewer bi-sede CLI+Web" residui, in tensione col corpo ora "Sede del track: CLI" (fuori scope P-07, non una violazione). | `.claude/agents/spec_reviewer.md:3,14,18` | NEUTRO | No (cleanup tranche 2, allineamento identità ruoli). |
| 3 | Esenzione guard RM-1 su `CARRYOVER.md` non intercetta la malformazione tabella (contesto; limite già dichiarato in METODO:227). | `scripts/claude_hooks/rm_guard.py:46-49` | NEUTRO | No. |

---

## Applicazione RM-1 a me stesso

Distinguo ciò che ho **verificato col grep/Read** da ciò che ho **assunto/dedotto**.

**VERIFICATO con comando/lettura diretta:**
- Tutti i 14 grep di VERIFICA dei Passi 0.4-9 sono stati **ri-eseguiti da me in CLI** e gli output trascritti sopra (sezione Domanda 3). Esiti = attesi tranne il caso M-GOV-1.
- B1 (riga malformata): **prova diretta multipla** — `awk` conta 12 pipe sulla riga 36 (vs 6 attese); `grep "^| M-GOV-1"` exit 1 (nessuna riga propria); `grep " || M-GOV-1"` match (gluing); `git show 60bcac0:tasks/CARRYOVER.md` mostra la riga M-16 chiusa con newline al baseline; `git show --stat 57225e0` = `1 insertion(+), 1 deletion(-)` (sostituzione di riga, non aggiunta). Catena di evidenza completa, non assunta.
- Fedeltà verbatim P-01..P-16: confrontato il testo di ogni patch nell'istruzione con l'output grep `-n` della riga risultante nel file. Le righe-corpo delle sostituzioni (P-04, P-05, P-06, P-07, P-10b, P-11, P-12, P-14a, P-15, P-16) e gli inserimenti (P-08, P-09, P-10a, P-13, P-14b) corrispondono carattere-per-carattere a quanto ho letto.
- Scoping per-commit: `git show --stat` su ognuno dei 5 commit — letto direttamente.

**ASSUNTO / non verificato empiricamente (dichiaro il limite):**
- Non ho aperto un renderer Markdown reale per osservare il rendering della tabella malformata; la conclusione "M-GOV-1 diventa celle extra di M-16" è **dedotta** dalla semantica delle tabelle GFM (il conteggio pipe è prova diretta, l'effetto di rendering è inferenza standard). L'inferenza non è in dubbio per GFM, ma la dichiaro come deduzione, non come osservazione di un renderer.
- **Alternative compatibili escluse** per B1: ho escluso "M-GOV-1 è una riga valida non rilevata dal mio pattern" (grep `^| M-GOV-1` exit 1 lo esclude) e "il baseline aveva già la fusione" (`git show 60bcac0` lo esclude: M-16 terminava pulita). **Alternative non escluse**: nessuna rilevante.
- Non ho verificato il contenuto di `Business Spec/Final/ESITO_GOV-FIX-01.md` (Passo 13) perché **fuori dal perimetro** dell'audit (delta sui 4 path citati); non mi pronuncio su Passi 0/10/11/12/13 se non per ciò che il delta committato rivela.
- Le occorrenze "9:00" dentro `docs/methodology_v2/CAP_*`: ho letto le righe via grep `-n` con contesto inline e giudicato la **semantica** (settlement/epoca/probe vs sessione) sul testo della riga; non ho aperto l'intero capitolo per ogni hit. Giudizio basato sul contesto di riga, sufficiente per l'inventario non-modificativo richiesto da Passo 9.

**Onestà del verdetto**: CONDITIONAL e non FAIL perché l'unico bloccante è circoscritto (1 riga, fix meccanico) e non inquina la sostanza normativa delle 16 patch corrette; non è PASS perché B1 è un BUG REALE in tabella (registro M autoritativo) e — per il mapping verdetto↔classificazione appena introdotto da questa stessa tranche (P-10a/P-11) — una review con ≥1 BUG REALE non può emettere PASS.
