# ISTRUZIONI_B3-CARD-UPDATE-01 — Installazione card SPEC-FUNZ-01-B3 `rev-B` + verifica seam

> **Sede**: CLI (GOV-SURFACES-01, METODO §Superfici). **Esecutore**: Claude Code Orchestratore.
> **Natura**: aggiornamento della task card attiva + verifica di repo, **non** avvio del ciclo Developer.
> **Riga singola da incollare in CLI**: `Leggi ed esegui "Business Spec/Final/ISTRUZIONI_B3-CARD-UPDATE-01.md"`
>
> **Onestà claim→evidenza (BASE_COMUNE §8)**: ogni asserzione dell'esito porta evidenza puntuale (git/grep/Read, path:riga). Stato repo si **verifica, non si assume** (RM-2). Audit **no-DAPI**: nessuna probe runtime.

---

## 0. Out-of-scope (NON fare)

- **NON** invocare `spec_developer` né `spec_reviewer`: questo task **non** apre il ciclo di B3. La promozione di B3 la decide il **supervisore (AC)** dopo aver letto l'esito.
- **NON** modificare alcun CAP (freeze G-09): `docs/methodology_v2/CAP_02_parte_II.md` è in **sola lettura**.
- **NON** toccare i file chiusi: `SPEC_FUNZ_01_B1.md`, `SPEC_FUNZ_01_B2.md`, i relativi report, `00_indice.md`.
- **NON** scrivere alcuna spec (`SPEC_FUNZ_01_B3.md` non si crea qui).
- **NON** leggere/citare `SPEC_FUNZ_01.md`, `*_v1_storico*`, `PROPOSTA_SUDDIVISIONE_SPEC*.md` per scopi di contenuto: qui non c'è ricostruzione, solo installazione+verifica. (Il `grep` di censimento al punto 1 è ammesso: serve a contare file, non a leggerne il contenuto-requisiti.)

---

## 1. Verifica stato repo (RM-2, prima di toccare qualunque cosa)

Esegui e **riporta l'output testuale** nell'esito:

1. `git status --porcelain=v1` e `git log --oneline -8` — stato pulito/sporco e ultimi commit.
2. Conferma che lo **slot task attivo è libero**: leggi `tasks/STATO_CORRENTE.md` e `tasks/DEV_STATUS.md`; verifica che **non** ci sia un task in `READY_FOR_REVIEW`/in corso diverso da B3. Se uno slot risulta occupato, **fermati** e segnalalo: non installare.
3. Conferma i marcatori di chiusura attesi (grep su `tasks/STATO_CORRENTE.md`):
   - `B1` CHIUSO PASS, commit `7195ffe`;
   - `B2` CHIUSO PASS, commit `b858a88`;
   - `CAP-02` (`CAP_02_parte_II.md`) chiuso PASS SHA `a1625df`, G-25 chiuso.
   Riporta **PASS/MISMATCH** per ciascuno con la riga effettiva (`path:riga`). Un mismatch **non** blocca l'installazione della card, ma va segnalato come finding al supervisore.

## 2. Installazione card `rev-B`

4. Copia `Business Spec/Final/ACTIVE_TASK_B3_REVB.md` → `tasks/ACTIVE_TASK.md` (sovrascrivi la card B3 corrente con la revisione `rev-B`).
5. Verifica che `tasks/ACTIVE_TASK.md` contenga il banner `Revisione card rev-B` in testa e le sigle dei finding chiusi (`F-1`, `F-2`, `F-3`, `F-5`, `F-6`). Riporta esito.

## 3. Verifica dei pin e risoluzione dei due seam aperti (cuore del task)

Leggi `docs/methodology_v2/CAP_02_parte_II.md` (Cap.7 = 7.1–7.6 e Cap.11 = 11.1–11.5; più preambolo Parte II `:1-9`). **Verifica token-per-token** i pin del §2 della card e risolvi i seam:

6. **Pin §2 esistenti** (state machine, target_1_hit, expired, invalidated, missed_target, precedenza, raw touch, NB-8, timer post, timer pre, M-1, submacchina, GA): per ciascun numero di riga citato nel §2, conferma che la riga contenga il fatto. Produci una **tabella `pin | risolve? (sì/no) | riga effettiva se diversa`**. Non correggere la card per i pin che risolvono; per quelli che non risolvono, indica la **riga corretta** nell'esito (la card verrà patchata dal Planner in un giro separato, non da te).

7. **Seam `revoked` (F-1)** — risolvi la domanda lasciata aperta:
   a. Cerca nel **Cap.7.2** la riga della transizione `active → revoked` (segnale superseduto da nuovo `signal_id`). `grep -n -i "revoked\|supersed\|supersedu\|signal_id" docs/methodology_v2/CAP_02_parte_II.md`.
   b. **Se** la transizione `active→revoked` risolve in modo pulito su una riga del Cap.7.2 → riporta il numero di riga **e sostituisci** in `tasks/ACTIVE_TASK.md` il placeholder `<riga-7.2-da-confermare>` con la riga confermata (questa è verifica meccanica del pin, **non** ripianificazione). Riporta la sostituzione nell'esito.
   c. **Se** il Cap.7 rimanda interamente a Cap.6.3 per la condizione di `revoked` (nessuna riga di transizione propria in Cap.7.2) → **lascia il placeholder**, riportalo come esito, e segnala che il Developer dovrà marcare quel requisito `[B-N PROVVISORIO]` (come da nota di confine `revoked` §1 e §5 della card).
   d. Risolvi anche `<riga-6.3>` (la riga di Cap.6.3 che definisce "superseduto / segnale unico attivo / sostituzione-non-edit") e sostituiscila nel placeholder corrispondente in `tasks/ACTIVE_TASK.md`.

8. **Riga della regola di precedenza (F-2)**: conferma la riga del Cap.7.2 che enuncia `expiry > invalidazione > missed_target > raw touch > azione post-trigger` (il §2 la pinna a `:131`). Riporta risolve/non-risolve. Serve a validare che l'invariante di determinismo su cui poggia la categoria *valore-di-sistema* esista davvero nel CAP.

## 4. Commit e chiusura

9. Committa **solo** `tasks/ACTIVE_TASK.md` (l'Orchestratore committa la card, non il Planner): messaggio `[SPEC-FUNZ-01-B3] card rev-B: chiusi F-1/F-2/F-3/F-5/F-6; pin revoked/6.3 risolti in CLI`. Push su `origin/main`. Riporta lo SHA del commit.
10. Scrivi l'esito in `Business Spec/Final/ESITO_B3-CARD-UPDATE-01.md` con: output dei punti 1–3, tabella pin (punto 6), risoluzione seam `revoked`/`6.3` (punto 7), riga precedenza (punto 8), SHA commit (punto 9), e una riga finale **`SLOT ATTIVO: LIBERO/OCCUPATO`** e **`CARD rev-B INSTALLATA: SÌ/NO`**.
11. **Fermati.** Non invocare il Developer. Includi in coda la frase: `PRONTO PER DECISIONE SUPERVISORE SU PROMOZIONE B3`.

---

## 5. Applicazione RM-1 a te stesso (in coda all'esito)

Per ciascuna asserzione fattuale dell'esito (slot libero; B1/B2/CAP-02 ai commit attesi; pin che risolvono; riga `active→revoked`; card installata): **PROVE** (comando + output), **ALTERNATIVE ESCLUSE**, **ALTERNATIVE NON ESCLUSE**. Lista **"Empirico-CLI da verificare": attesa VUOTA** (audit documentale, no-DAPI).
