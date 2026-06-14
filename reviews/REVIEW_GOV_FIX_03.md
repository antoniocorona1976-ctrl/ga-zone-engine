# REVIEW_GOV_FIX_03 — Review ostile del delta GOV-FIX-03

**Sede**: CLI locale (`C:\Users\AN\Documents\Projects\ga-zone-engine`).
**Oggetto**: `git diff 1cf3cb7..674e562`, escludendo `reviews/REVIEW_HA1_G12bis.md` e ogni `reviews/*`.
**Metodo**: due giri ostili. Guard testato via stdin JSON (protocollo PreToolUse reale). Nessuna correzione, nessun commit.

---

## VERDETTO: **PASS**

Le 4 patch sostanziali del delta (rm_guard.py, METODO P-23, METODO P-24, STATO_CORRENTE hash) corrispondono fedelmente a `ISTRUZIONI_GOV-FIX-03.md`, senza aggiunte né omissioni. Il lucchetto force-push funziona meccanicamente sui 5 casi-chiave, non ha rotto la logica esistente (RM-1/RM-4/quarantena/AGENTS_UNLOCK verificate ancora attive), la sintassi è valida. Gli hash G-25 sono giustificati dai commit citati e gli ambigui restano `<sha-da-confermare>`. Nessuna contraddizione bloccante fra documenti normativi. I finding sono tutti NEUTRO / osservazioni minori (nessun BUG REALE).

---

## File nel perimetro (esclusi i `reviews/*`)

| File | Δ | Patch attesa (ISTRUZIONI) |
|---|---|---|
| `scripts/claude_hooks/rm_guard.py` | +8 | Passo 1 (lucchetto force-push) |
| `tasks/METODO.md` | +4 | Passo 2 (P-23 + P-24) |
| `tasks/STATO_CORRENTE.md` | ±2 | Passo 4 (G-25 hash CAP-01/03) |
| ~~`reviews/REVIEW_HA1_G12bis.md`~~ | — | escluso da mandato |

Nessun file fuori perimetro modificato. `settings.json`, `.gitignore`, `docs/methodology_v2/CAP_*`, `00_indice.md` **non** toccati (verificato `git diff --name-only`). Coerente coi divieti (Passo regole 5/6, Divieti finali).

---

## Domanda (1) — Corrispondenza patch-per-patch alle ISTRUZIONI

**Passo 1 (rm_guard.py)** — MATCH. Aggiunte 2 costanti regex (righe 63-64: `GIT_PUSH`, `FORCE_FLAGS`) + 1 blocco guard (righe 223-228) nel ramo `tool in ("Bash","PowerShell")`. Usa lo **stesso meccanismo di blocco esistente** (`deny()` → exit 2, righe 67-69), come prescritto (Passo 1.2 vincolo "stesso exit code/canale"). Match `-f` su token isolato via `(?:^|\s)-f(?:\s|$)` (rispetta il vincolo "token isolato"). Override `[FORCE-PUSH-OK]` modellato su `[RM-HOOK-OVERRIDE]`. Nessuna modifica alla logica commit esistente. CONFORME.

**Passo 2 / P-23 (METODO force-push)** — MATCH ESATTO. Riga 236, testo verbatim rispetto all'AZIONE del Passo 2; collocata **PRIMA** di "Override d'emergenza" (riga 238), come da ancora. CONFORME.

**Passo 2 / P-24 (METODO bypass)** — MATCH ESATTO. Riga 232, testo verbatim; collocata **PRIMA** di "Limite dichiarato" (riga 234), come da ancora. CONFORME.

**Passo 4 / G-25 (STATO_CORRENTE)** — MATCH. Sostituiti solo i 2 placeholder CAP-01 e CAP-03; CAP-02 lasciato `<sha-da-confermare>`; tutti gli altri marcatori intatti. CONFORME.

Passo 3 (HA-1 review) e Passo 5 (G-26) non producono file nel perimetro di questa review (il file HA-1 è escluso per mandato; G-26 evidentemente non ha generato C4, coerente col commit log che non mostra `[SPEC-FUNZ-01]`). Nessuna omissione rispetto a ciò che il delta DEVE contenere.

---

## Domanda (2) — G-23 lucchetto: correttezza + non-regressione

**Sintassi**: `python -c "import ast; ast.parse(...)"` → `SYNTAX OK`.

**Test funzionale (stdin JSON, come PreToolUse)** — 5 casi-chiave:

| # | Comando (guard via stdin) | Atteso | Esito | OK |
|---|---|---|---|---|
| a | `git push origin main` | non bloccato | **exit 0** | ✓ |
| b1 | `git push --force origin main` | bloccato | **exit 2** | ✓ |
| b2 | `git push --force-with-lease origin main` | bloccato | **exit 2** | ✓ |
| b3 | `git push -f origin main` | bloccato | **exit 2** | ✓ |
| c | `git push --force-with-lease [FORCE-PUSH-OK] origin main` | non bloccato | **exit 0** | ✓ |

**Falsi positivi (tutti exit 0 = corretti):** `git commit -m fix-foo`; `git push origin feature-f`; `git push origin my-f-branch`; `git push --foo origin main`; `git commit -m "doc --force"` (force in messaggio, no push); `echo somepush -f` (non git); `git commit -f -m x` (no push); `git push origin --forceful` (—`\b` non aggancia). Nessun falso positivo sui casi richiesti dal mandato.

**Non-regressione logica esistente (tutti exit 2 = ancora attivi):**
- RM-1: commit che aggiunge "verificato" in `.md` non esente, senza blocco VERIFICA → **bloccato** (riprodotto con file staged reale).
- Quarantena B: `Read` su `OLD_NOT_USE_..._4_CANALI/` → **bloccato**; `cat` quarantena via Bash → **bloccato**.
- AGENTS_UNLOCK: `Write` su `.claude/agents/developer.md` senza flag → **bloccato**.
- Commit combinato `add;commit;push --force` → **bloccato** (il guard vede l'intero comando). PowerShell `push --force` → **bloccato**.

**Ordinamento force-push vs RM-HOOK-OVERRIDE (interazione)**: il check force-push (riga 223) è **prima** dell'early-exit `RM-HOOK-OVERRIDE` (riga 229). Conseguenza testata: `git push --force-with-lease [RM-HOOK-OVERRIDE] origin main` → **exit 2** (NON sbloccato). È **coerente col design** dichiarato (METODO G-23: l'unica eccezione al force-push è `[FORCE-PUSH-OK]`, non `[RM-HOOK-OVERRIDE]`). Nessun BUG: il tag generico non deve aprire la riscrittura history. Annotato come NEUTRO informativo (vedi tabella).

---

## Domanda (3) — Coerenza METODO G-23/G-24 ↔ comportamento reale guard/settings

- **G-23 (METODO riga 236)** dichiara: "`--force`, `--force-with-lease`, `-f` ... bloccati meccanicamente (exit 2); eccezione `[FORCE-PUSH-OK]`". → **Combacia** col guard testato (b1/b2/b3 exit 2; c exit 0). COERENTE.
- **G-24 (METODO riga 232)** dichiara: `settings.json` ha `"defaultMode": "bypassPermissions"`; bypass NON scavalca deny né hook. → `grep` su `.claude/settings.json` riga 14: `"defaultMode": "bypassPermissions"` **confermato**. Il claim "hook attivo a ogni tool" è coerente: il guard ha bloccato realmente le mie chiamate di test in questa stessa sessione (ambiente con bypassPermissions). COERENTE. La parte "non scavalca deny" non è ri-testabile in CLI senza alterare settings (vietato dal mandato): la lascio come asserzione documentale plausibile, non empiricamente ri-verificata qui (vedi RM-1 a me stesso).

---

## Domanda (4) — G-25: giustificazione degli hash

| CAP | Marcatore | Commit | Messaggio | Giudizio |
|---|---|---|---|---|
| 01 | `b76c32c` | `b76c32c` | `[CAP-01] Parte I completata: ... 4 cicli Review, PASS finale` | **Giustificato.** Unico commit che introduce `REVIEW_CAP_01.md` e cita "Parte I ... PASS finale". Nessun candidato concorrente. È un commit *bundle* (doc+report+review+PDF), non review-only, ma è l'unico portatore del PASS di CAP-01 → non ambiguo. |
| 02 | `<sha-da-confermare>` | — | — | **Correttamente lasciato.** PASS in `e070fa9 [REVIEW-02 v3] ... PASS`, ma esiste `1cb8219 [REVIEW-02] recupero file review v3 e v4 mai committati`: quale commit "chiude" CAP-02 è genuinamente ambiguo. Lasciarlo aperto è la scelta RM-1 onesta. |
| 03 | `1e3172d` | `1e3172d` | `[REVIEW-03 extra+v4] review EXTRA post-PASS + Review v4 PASS finale` | **Giustificato (con nota).** Commit review-only che cita CAP-03 + "PASS finale". Esiste un secondo commit con PASS (`9467a07 [REVIEW-03 v3] ... PASS`); la scelta del *finale* (`1e3172d`) è la corretta chiusura, e "PASS finale" disambigua. Difendibile. |

`git cat-file -t` conferma che `b76c32c` e `1e3172d` sono commit reali. **Nessun hash inventato.** Il commit `674e562` dichiara fedelmente "risoluzione hash CAP-01/03 ... CAP-02 resta da confermare". CONFORME al criterio di accettazione Passo 4.2 (onestà RM-1).

---

## Domanda (5) — Nuove contraddizioni fra documenti normativi

Nessuna contraddizione bloccante.

- METODO G-23 (eccezione = `[FORCE-PUSH-OK]`) e G-24 (override critici "coperti da regole nel guard, non da prompt") sono **mutuamente coerenti** e coerenti col guard (ordinamento force-check-prima-di-override).
- `.claude/CLAUDE.md` §Identità/precedenza già elenca `[RM-HOOK-OVERRIDE]` e `AGENTS_UNLOCK` come override AC-only; G-23 aggiunge `[FORCE-PUSH-OK]` con lo stesso trattamento → estensione coerente, non in conflitto.
- Osservazione minore (NEUTRO): `CLAUDE.md` non menziona ancora esplicitamente `[FORCE-PUSH-OK]` nella lista override §Identità (cita solo `[RM-HOOK-OVERRIDE]`, `AGENTS_UNLOCK`). Non è una contraddizione (METODO ha precedenza e lo norma), ma un allineamento futuro di CLAUDE.md ridurrebbe il rischio di residuo. Fuori dalle ancore di questa tranche.

---

## Tabella "Classificazione per il supervisore"

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|---|---|---|---|
| 1 | `[RM-HOOK-OVERRIDE]` non sblocca il force-push (force-check precede l'early-exit) | `rm_guard.py:223` vs `:229` | NEUTRO (è il design voluto: force-push richiede `[FORCE-PUSH-OK]`, non l'override generico) | No |
| 2 | Over-block conservativo: un compound `git push origin main ; ls -f` (push normale + `-f` non correlato altrove) viene bloccato | `rm_guard.py:223-228` | RISCHIO PEGGIORAMENTO (basso; raro; escape `[FORCE-PUSH-OK]` disponibile; nessun falso negativo introdotto) | No — decisione AC |
| 3 | CAP-03: due commit citano PASS (`9467a07` v3, `1e3172d` v4-finale); scelto il finale, difendibile ma non l'unico col token "PASS" | `STATO_CORRENTE.md:9` | NEUTRO (scelta corretta = PASS finale) | No |
| 4 | `CLAUDE.md` §Identità non cita ancora `[FORCE-PUSH-OK]` fra gli override AC-only | `.claude/CLAUDE.md` §Identità | NEUTRO (METODO ha precedenza; allineamento futuro) | No |
| 5 | Claim G-24 "bypass non scavalca deny" non ri-testato empiricamente in CLI (vietato toccare settings) | `METODO.md:232` | NEUTRO (asserzione documentale plausibile; hook-attivo confermato sì) | No |

Nessun **BUG REALE** → coerente con PASS (BASE_COMUNE §4: ≥1 BUG REALE impedirebbe il PASS).

---

## Applicazione RM-1 a me stesso

| Mia asserzione | Prova puntuale | Alternative escluse | Non escluse |
|---|---|---|---|
| "sintassi OK" | output `SYNTAX OK` da `ast.parse` | errori di parse | — |
| "force-push bloccato exit 2 (b1/b2/b3)" | esecuzione guard via stdin JSON, exit registrato | che l'exit 2 venisse da altro check (RM-1/quarantena): escluso, stderr cita "force-push vietato (G-23)" | — |
| "push normale non bloccato (a)" | exit 0 osservato | blocco silenzioso: escluso (exit 0 esplicito, stderr vuoto) | — |
| "`[FORCE-PUSH-OK]` lascia passare (c)" | exit 0 osservato | — | — |
| "RM-1/quarantena/AGENTS_UNLOCK ancora attivi" | 4 invocazioni guard, tutte exit 2 con stderr specifico per ciascun check | che fosse il force-check a bloccare: escluso (i comandi non contengono push+force; stderr cita il check corretto) | — |
| "hash b76c32c/1e3172d reali e giustificati" | `git cat-file -t` = commit; `git log -1 --format=%s`; `git log --all -- reviews/` per ambiguità | hash inventato: escluso; per CAP-01 candidato concorrente: escluso (unico portatore di REVIEW_CAP_01.md) | per CAP-03 esiste 2° commit con "PASS" (9467a07): scelta del finale è difendibile, ma "unicità assoluta" è verifica **parziale** — flaggato come NEUTRO #3 |
| "settings.json defaultMode=bypassPermissions" | `grep` riga 14 | — | — |
| "G-24: bypass non scavalca deny" | NON ri-testato (vietato modificare settings) | — | **NON ESCLUSA**: verifica documentale, non empirica. Dichiarata tale, non spacciata per verificata. |
| "nessun file fuori perimetro toccato" | `git diff --name-only 1cf3cb7..HEAD` | — | — |

**Limite di sede dichiarato**: la review è statica + esecuzione locale del guard (no DAPI coinvolto). Lista "Empirico-CLI da verificare": vuota (nessuna asserzione richiede DAPI live). L'unica asserzione non-empirica residua è il claim G-24 "non scavalca deny", lasciata esplicitamente come documentale.
