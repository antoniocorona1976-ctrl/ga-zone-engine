# REVIEW — SPEC-FUNZ-01 PROMOTE (Fase D)

**Perimetro**: il delta `git diff ab7450f..HEAD` (HEAD = `0165601`), cioè i due commit `cbd4e01` (storico esplicito v1) + `0165601` (promozione v2 → ufficiale). Mandato ristretto a 5 domande (vedi sotto). NON è una review piena del contenuto della spec (quello è già PASS a `ab7450f`).
**Sede**: CLI locale (working dir `C:\Users\AN\Documents\Projects\ga-zone-engine`). Audit no-DAPI, documentale + git. Lista "Empirico-CLI da verificare": **VUOTA** (nessuna asserzione richiede DAPI/runtime).
**Reviewer**: general-purpose ostile, due giri. Letti `tasks/METODO.md` (RM-1..RM-4), `.claude/BASE_COMUNE.md`, `Business Spec/Final/ISTRUZIONI_SPEC-FUNZ-01-PROMOTE.md`.
**Riferimento istruzioni**: la review committata sarà fatta dall'Orchestratore (`[REVIEW] SPEC-FUNZ-01 PROMOTE — verdetto: PASS`). Io non committo, non correggo.

---

## VERDETTO: **PASS**

Il rimpiazzo Fase D è fedele alle istruzioni, blob-identico ai sorgenti validati, reversibile (tag + copie tracciate), col marcatore meccanico aggiornato al nuovo sha e con history lineare a 2 commit senza alcun force-push/rewrite nel perimetro. 0 BUG REALE. 1 osservazione NEUTRO (residuo cosmetico ereditato dal blob già PASS, NON introdotto dalla promozione).

---

## Esito delle 5 domande

### (1) Fedeltà a `ISTRUZIONI_SPEC-FUNZ-01-PROMOTE.md` (Passi 1–5) — **CONFORME**

| Passo | Atteso | Riscontro | Esito |
|---|---|---|---|
| P1 — paracadute storico | commit SOLO delle 2 copie `_v1_storico` | `cbd4e01` aggiunge esattamente `docs/.../SPEC_FUNZ_01_v1_storico.md` + `reports/.../REPORT_SPEC_FUNZ_01_v1_storico.md` (A/A), nient'altro | OK |
| P2 — rimpiazzo | v2 → ufficiale; `_v2.md` non esiste più; ufficiale ha NFR-8.11 | in `0165601`: `SPEC_FUNZ_01.md` (M) + `SPEC_FUNZ_01_v2.md` (D); idem report. `_v2` assenti da `git ls-tree HEAD`. NFR-8.11 presente (r.411) | OK |
| P3 — marcatore + prosa + DEV_STATUS | marcatore → `ab7450f`; riga prosa "Aggiornamento 2026-06-14" in testa; DEV_STATUS azzerato | marcatore r.6 = `ab7450f`; riga prosa presente verbatim; `DEV_STATUS.md` = 0 byte | OK |
| P4 — CARRYOVER | nota di chiusura formato voci esistenti; riconciliare M aperti pertinenti | aggiunto `M-GOV-2` (CHIUSO); `M-2` re-ancorato a NFR-6.2 e `M-GOV-1` a R-7.1 (riconciliazione spec) | OK |
| P5 — commit & push | 1 commit con i 5 file attesi; push; no "ahead"; no `Business Spec/`, no `.gitignore` | `0165601` copre i 5 file (+ le 2 D dei `_v2`); nessun `Business Spec/`, nessun `.gitignore` toccato; nessun `[RM-HOOK-OVERRIDE]` | OK |

**Verifica blob-identità (la fedeltà è "il file ufficiale È il v2", non solo "ha NFR-8.11")**:
- `git diff ab7450f:...SPEC_FUNZ_01_v2.md  HEAD:...SPEC_FUNZ_01.md` → **vuoto** (identici).
- `git diff ab7450f:...REPORT_SPEC_FUNZ_01_v2.md  HEAD:...REPORT_SPEC_FUNZ_01.md` → **vuoto** (identici).
- `git diff a16a4c0:...SPEC_FUNZ_01.md  HEAD:...SPEC_FUNZ_01_v1_storico.md` → **vuoto** (la copia storica È la v1).

Nota meccanica (non un difetto): git registra la promozione come `M` su `SPEC_FUNZ_01.md` + `D` su `_v2.md`, non come `R` (rename). È atteso: `git mv -f` sovrascrive un path già tracciato, quindi il rename non emerge nel name-status. La sostanza ("ufficiale = v2") è dimostrata dall'identità blob sopra, non dal flag di rename.

### (2) L'ufficiale ORA È il v2 validato e NON il vecchio — **SÌ**
- NFR-8.11 presente: `SPEC_FUNZ_01.md:411` (+ righe matrice 427, 590).
- "non è consulenza" / "consulenza in materia": **0 occorrenze** (`git grep -in` sul file ufficiale a HEAD → nessun match). Coerente con decisione AC (CN-3 lasciata cadere).
- "75 requisiti": dichiarato a r.604 ("41 R + 13 NFR + 21 CN = **75 requisiti**"). Identità blob col v2 PASS confermata.
- L'ufficiale NON è più la v1: il contenuto v1 vive solo in `_v1_storico` e nel tag (vedi Q3).

### (3) Il vecchio è recuperabile — **SÌ**
- Tag `spec-funz-01-v1-storico` esiste e `git rev-list -n1` → `a16a4c0…` (combacia con `git rev-parse a16a4c0`).
- `git show spec-funz-01-v1-storico:docs/spec_funzionale/SPEC_FUNZ_01.md` restituisce il contenuto v1 (header "PHASE-1", "36 requisiti" della stagione v1).
- Copie `_v1_storico` tracciate: aggiunte in `cbd4e01` (dentro il delta), presenti in `git ls-tree HEAD`, identiche alla v1 (`a16a4c0`) per diff vuoto.

### (4) Marcatore meccanico = `ab7450f`, non più `a16a4c0` — **SÌ**
- `git grep "SPEC-FUNZ-01: CHIUSO PASS" HEAD -- tasks/STATO_CORRENTE.md` → **1 sola riga** (r.6): `` `SPEC-FUNZ-01: CHIUSO PASS ab7450f` ``.
- L'unica `a16a4c0` residua nel file è nella **prosa storica** (r.19, "Re-Review v2 PASS (a16a4c0)" della stagione v1) e nelle voci CARRYOVER che datano l'incardinamento storico — esplicitamente ammesse dal mandato. Non è il marcatore.

### (5) Nessun force-push / rewrite nel delta — **SÌ**
- `git merge-base --is-ancestor ab7450f HEAD` → vero (ab7450f è ancestor lineare di HEAD).
- `git rev-list --count ab7450f..HEAD` → **2**; catena parent lineare: `0165601`→`cbd4e01`→`ab7450f`.
- Reflog dei 2 commit del delta: `HEAD@{0}` e `HEAD@{1}` sono `commit:` semplici (nessun `(amend)`, `rebase`, `reset`, `--force`). Le voci `(amend)`/`reset` nel reflog sono a/prima di `1c59be9`, cioè **fuori** dal perimetro `ab7450f..HEAD` (appartengono al ciclo v2 precedente, già chiuso e PASS).

---

## Tabella "Classificazione per il supervisore"

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|------------------------|
| 1 | Il REPORT ufficiale promosso mantiene nell'header l'auto-riferimento al filename pre-promozione: "Output: `docs/spec_funzionale/SPEC_FUNZ_01_v2.md`" (il file ora è `SPEC_FUNZ_01.md`). Residuo cosmetico, **identico al blob v2 già PASS a `ab7450f`**, NON introdotto dalla promozione. | `reports/REPORT_SPEC_FUNZ_01.md:3` | NEUTRO | No (NEUTRO non va a Dev senza approvazione AC; se AC vuole, micro-pass cosmetico) |
| 2 | (informativa, non finding) Il documento ufficiale contiene 52 id `R-x.y` distinti a fronte dei "41 R" auto-dichiarati a r.604. La discrepanza preesiste nel blob v2 già PASS, è identica fra v2 e ufficiale, e ricade nel conteggio interno della spec, **fuori dal mandato di fedeltà della promozione**. | `SPEC_FUNZ_01.md:604` | NEUTRO | No (fuori perimetro Fase D; eventuale verifica appartiene a una re-review piena della spec, non a questa) |

Nessun **BUG REALE**. Coerente con verdetto PASS (BASE_COMUNE §4: ≥1 BUG REALE ⇒ niente PASS; qui zero).

---

## Applicazione RM-1 a me stesso

Per ogni mia asserzione "verificato", l'evidenza puntuale e le alternative escluse:

- **"ufficiale = v2"** — PROVE: `git diff ab7450f:…_v2.md HEAD:…SPEC_FUNZ_01.md` output vuoto (+ idem report). ALTERNATIVE ESCLUSE: "ha solo NFR-8.11 ma contenuto diverso" → esclusa dal diff vuoto byte-a-byte (non mi sono fermato al grep di NFR-8.11). NON ESCLUSE: nessuna.
- **"_v1_storico = v1 (a16a4c0)"** — PROVE: `git diff a16a4c0:…SPEC_FUNZ_01.md HEAD:…_v1_storico.md` vuoto. ALTERNATIVE ESCLUSE: copia da file ufficiale corrente già sovrascritto → esclusa perché diff è contro `a16a4c0`, non contro HEAD. NON ESCLUSE: nessuna.
- **"tag → a16a4c0"** — PROVE: `git rev-list -n1 spec-funz-01-v1-storico` = `a16a4c04…` = `git rev-parse a16a4c0`. Tag lightweight (punta al commit, non al blob); il requisito "punta ad a16a4c0" è sul commit ⇒ soddisfatto. NON ESCLUSE: nessuna.
- **"marcatore = ab7450f, unico"** — PROVE: `git grep` restituisce 1 riga (r.6). ALTERNATIVE ESCLUSE: residui `a16a4c0` come marcatore → esclusi distinguendo riga-marcatore (formato `` `SPEC-FUNZ-01: CHIUSO PASS <sha>` ``) da prosa (r.19) e CARRYOVER, come da mandato. NON ESCLUSE: nessuna.
- **"no force-push nel delta"** — PROVE: `--is-ancestor` vero + `rev-list --count`=2 + reflog HEAD@{0,1} = `commit:` puri. ALTERNATIVE ESCLUSE: amend/reset visti nel reflog → esclusi dal perimetro perché a/prima di `1c59be9` (< ab7450f), non dentro `ab7450f..HEAD`. NON ESCLUSE: un push `--force` che NON lascia traccia nel reflog locale (es. eseguito da altra macchina/sessione) non è osservabile da qui; il mandato chiede `git reflog`+`git log` locali, entrambi coerenti con history lineare → verifica completa rispetto al mandato, **parziale** in senso assoluto (limite dichiarato).
- **"NEUTRO #1 non introdotto dalla promozione"** — PROVE: il REPORT ufficiale è blob-identico al `REPORT_…_v2.md` di `ab7450f` (diff vuoto), quindi la stringa stale era già nel blob PASS. ALTERNATIVE ESCLUSE: "introdotto dal `git mv`" → escluso (mv non modifica il contenuto; diff identità lo conferma). NON ESCLUSE: nessuna.

**Limite di sede dichiarato**: audit interamente git/documentale; nessuna verifica empirica DAPI necessaria né eseguita (lista Empirico-CLI vuota, coerente col mandato Fase D no-DAPI).
