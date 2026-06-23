# ESITO_B8-01 — Costruzione card SPEC-FUNZ-01-B8 (Confine / chiusura, Sez.10)

**Esecutore**: Claude Code CLI, Orchestratore/Planner. **Data**: 2026-06-22.
**Verdetto**: ✅ `CARD-B8-DRAFT-PRONTA`.
**Output**: card-sorgente `Business Spec/Final/ACTIVE_TASK_B8.md` (NON installata in `tasks/ACTIVE_TASK.md`); questo ESITO.
**Stop**: `spec_developer` / `spec_reviewer` **NON** invocati. Install + ciclo = decisione AC.

---

## 1. Pre-flight (§1 ISTRUZIONI)

| Check | Esito |
|---|---|
| `git log --oneline -3` / HEAD | **`c1ee11d`** `[STATO] SPEC-FUNZ-01-B7 CHIUSO PASS 37d2166` (commit di stato sopra il review `37d2166`). Atteso `37d2166` (B7 CHIUSO PASS): **coerente** — `37d2166` è il review PASS, `c1ee11d` è il `[STATO]` di chiusura che lo segue. B7 CHIUSO PASS confermato. |
| Slot task libero | **OK** — `tasks/DEV_STATUS.md` **vuoto**; `tasks/STATO_CORRENTE.md` riporta `SPEC-FUNZ-01-B7: CHIUSO PASS 37d2166`, "SLOT LIBERO", `ACTIVE_TASK` storico su B7. |
| `ANTHROPIC_API_KEY` vuota | **OK** — `KEY=[]`. |

## 2. Nomi-file CAP reali + SHA frozen (§1 ISTRUZIONI)

| Capitolo (Sez.10) | File reale (verificato `git ls-files`) | Ruolo in B8 | SHA frozen pinnato | `git diff <frozen> HEAD` |
|---|---|---|---|---|
| Cap.42 | `docs/methodology_v2/CAP_08_parte_8.md` (arabo) | **fonte primaria** (fasizzazione PHASE-1/PHASE-2) | `015c47a` | **EMPTY** ✓ |
| Cap.55 | `docs/methodology_v2/CAP_09_parte_9.md` (arabo) | **fonte primaria** (dipendenze aperte P9) | `28cfd2d` | **EMPTY** ✓ |
| Cap.64 | `docs/methodology_v2/CAP_10_parte_10.md` (arabo) | **fonte primaria** (dipendenze aperte P10) | `41447d3` | **EMPTY** ✓ |
| Cap.36.3 | `docs/methodology_v2/CAP_07_parte_VII.md` (romano) | **premessa** (owned B7) | `b27c1e3` | **EMPTY** ✓ |
| Cap.53 | `docs/methodology_v2/CAP_09_parte_9.md` | **premessa** (owned B5) | `28cfd2d` | **EMPTY** ✓ |

**NB (analogo B7-F4) — SHA marcatore di chiusura ≠ SHA content-autoritativo per CAP_09/CAP_10**: i marcatori PASS in `STATO_CORRENTE` sono `CAP-09: ...86425a7` e `CAP-10: ...48171e4`, ma `git diff 86425a7 HEAD` e `git diff 48171e4 HEAD` sui rispettivi file sono **NON vuoti** (i file sono evoluti post-PASS via audit-RM CAP-DATA-02/03, giu 2026: CAP_09 ultimo tocco `28cfd2d` 2026-06-02; CAP_10 ultimo tocco `41447d3` 2026-06-01). Lo SHA frozen **autoritativo** pinnato nella card è l'ultimo commit che tocca il file (diff a HEAD vuoto). CAP_08 (`015c47a`) e CAP_07 (`b27c1e3`) hanno diff vuoto direttamente.

## 3. Riconciliazione perimetro con la mappa (§2 ISTRUZIONI — autorità F-3 = `c7ce4be`)

Mappa `PROPOSTA_SUDDIVISIONE_SPEC_v2.md` riga B8 (`:110`): **Sez.10**, CAP-fonte `CAP_08 Cap.42 P8 (+ P9/P10/PVII)`, **~3 req**, "Confine PHASE-2 & fasizzazione".

**Requisiti di Sez.10 (dalla v2 `SPEC_FUNZ_01.md` §10 + matrice §11)** — partizione consolidata, NON re-litigata:

| Req-v2 | Tipo | Capitolo-fonte (matrice §11) | Pin verificati (token-per-token in setup) | → fonte primaria / premessa B8 |
|---|---|---|---|---|
| **R-10.1** | R | CAP_08 Cap.42 (P8) | `CAP_08:143` (dichiarazione normativa PHASE-2 senza impl.), `CAP_08:167` (vincolo fasizzazione PHASE-1 vs PHASE-2) | **Cap.42** (primaria) |
| **R-10.2** | R | CAP_09 Cap.55 / CAP_10 Cap.64 / CAP_07 Cap.36 (PVII) | `CAP_09:402` (M-2 OPEN), `CAP_09:406` (impl. codice FASE-D), `CAP_10:131` (θ_reconcile provvisorio), `CAP_10:226`-region (punti aperti P10), `CAP_07:637` (10 param carryover) | **Cap.55 + Cap.64** (primaria); **Cap.36.3** (premessa, owned B7) |
| **CN-10.1** | CN | CAP_08 Cap.42 (P8) / CAP_09 Cap.53 (P9) / CAP_10 Cap.64 (P10) | `CAP_08:147` (strumenti cross-index), `CAP_08:176` (estensioni future), `CAP_09:338` (cash europei ≠ cross-index PHASE-2), `CAP_10:226`-region (cross-index PHASE-2 invariato) | **Cap.42 + Cap.64** (primaria); **Cap.53** (premessa, owned B5) |

**Conteggio reale Sez.10 confermato = 3 (R-10.1, R-10.2, CN-10.1)** — **coincide con l'atteso ~3** della mappa. ✓ Nessuna divergenza.

> Nota cecità: la tabella sopra (Req-v2 ↔ capitolo ↔ pin) è **riferimento Orchestratore/Reviewer**, NON esposta al Developer. La card-Developer è per soli capitoli, senza ID-v2/conteggio/partizione. Il Developer assegna `B8-*` da zero (N1, **nessun target**; plausibile 3-5 ID atomici a seconda di come spezza le dipendenze aperte sotto N1).

## 4. Verifica di fondazione / capitoli framing (§3 ISTRUZIONI)

| Capitolo | Classificazione B8 | Motivo |
|---|---|---|
| **Cap.42** (CAP_08) | **req-bearing** (primaria) | Fonda R-10.1 (fasizzazione PHASE-1 FIB-only, `:143/:145/:167`) + CN-10.1 (cross-index PHASE-2 = dichiarazione senza impl., `:143/:147/:176`). Esclusivo di B8 (nessun B1-B7 lo tocca). |
| **Cap.55** (CAP_09) | **req-bearing** (primaria) | Capitolo di rinvii, ma **fonda** R-10.2 (dipendenze aperte verso FASE-D: M-2 `:402`, impl. codice `:406`, FDAX/vendor/lookup `:387/:391`). Trattamento: consolidare **la dichiarazione di apertura/rinvio**, NON il merito. |
| **Cap.64** (CAP_10) | **req-bearing** (primaria) | Capitolo di rinvii, ma **fonda** R-10.2/CN-10.1 (θ_reconcile provvisorio `:131`, cross-index PHASE-2 invariato, M-2). Idem Cap.55. |
| **Cap.36.3** (CAP_07) | **framing/premessa** (owned B7) | 10 param carryover post-go-live `:637`: **già perimetro B7** (gate, chiuso PASS). In B8 = citazione di **una** dipendenza aperta, NON fonte primaria, NON ri-derivare il gate. |
| **Cap.53** (CAP_09) | **framing/premessa** (owned B5) | Gating cash europei: **già perimetro B5** (CN-7.9). In B8 si cita **solo** il confine `:338` (cash europei ≠ cross-index PHASE-2) per CN-10.1, NON il gating runtime. |
| **Cap.41** (CAP_08) | **framing/premessa** (owned B5) | Calendario/epoca E5: origine normativa della sessione, owned B5. Citabile solo se serve come dipendenza aperta (M-GOV-1), non ri-consolidata. |

**Nessuno script da diffare** (RM-2): `git ls-files scripts | grep` su termini di Sez.10 (cross-index, phase-2, reconcile, fasizzazione) → **gate/confine documentale**, nessun decoder/parser di sistema esterno in scope. (I `[PROVA-EMPIRICA]` interni ai capitoli — es. FDAX `:387` — si riportano come già dichiarati dal capitolo frozen, non si ri-verificano.)

**Trappole §3 gestite nella card**: AC-B8-NOASSEMBLY (assemblaggio serie B1..B8 + indicizzazione + avvio FASE-D = task/fasi separati, NON requisiti); AC-B8-FRAMING (Cap.36.3/53/41 = premesse, non gonfiare).

## 5. Cross-check copertura per-ID (§5 ISTRUZIONI — lezione CN-2.1)

| Req-v2 Sez.10 | Casa in B8? | Coperto altrove (B1-B7)? | Note |
|---|---|---|---|
| **R-10.1** | **sì** (Cap.42) | **No** — Cap.42 non è fonte di alcun B1-B7 | Esclusivo B8. ✓ |
| **CN-10.1** | **sì** (Cap.42 + Cap.64 + premessa Cap.53:338) | **No** — il confine cross-index PHASE-2 non è consolidato da B5 (B5 consolida il gating runtime di Cap.53, non il confine PHASE-2 `:338`) | Esclusivo B8. ✓ |
| **R-10.2** | **sì** (Cap.55 + Cap.64 + premessa Cap.36.3) | **Doppia-tracciatura nota su Cap.36.3** (vedi sotto) | Risolta dalla partizione v2: framing diverso. ✓ |

**Doppia-tracciatura Cap.36.3 (10 param carryover post-go-live) — risolta, non un buco:** il capitolo Cap.36 è perimetro **B7** (Sez.8, gate). B7 ha consolidato i 10 param come **proprietà del gate** ("rimangono starting point post-go-live, non task di Parte VII"). R-10.2 (Sez.10/B8) li recepisce come **una delle dipendenze aperte verso FASE-D** (framing di confine, non di gate). Concern distinti, sezioni distinte → la partizione v2 assegna R-10.2 a Sez.10/B8 senza overlap di *requisito*. Nella card B8 Cap.36.3 è **premessa** (cita la riga, NON ri-derivare il gate) proprio per evitare scope-creep su B7. ✓

**Nessun orfano** (ogni req Sez.10 ha casa in B8). **Nessun req-Sez.10 vive coperto altrove** (i punti di contatto Cap.36.3/Cap.53 sono premesse di confine, non requisiti duplicati).

## 6. Verifica chiusura 75/75 (§5 ISTRUZIONI)

Partizione consolidata (mappa `c7ce4be` §139, NON a memoria):

| Blocco | Sez. | # req-v2 |
|---|---|---|
| B1 | Sez.1+2 (escl. CN-2.1) +CN-7.3 | 9 |
| B2 | Sez.3 | 12 |
| B3 | Sez.4 (escl. CN-4.2) +CN-7.4 | 6 |
| B4 | Sez.5+6 | 14 |
| B5 | Sez.7 (+CN-4.2, +CN-2.1) | 11 |
| B6 | Sez.9 | 9 |
| B7 | Sez.8 | 11 |
| **B8** | **Sez.10** | **3** |
| **TOTALE** | | **75** ✓ |

9+12+6+14+11+9+11+3 = **75**. **Chiusura 75/75 verificata**: con B8 (R-10.1, R-10.2, CN-10.1) i 75 requisiti v2 risultano tutti coperti dalla serie B1-B8. **B8 è l'ultimo blocco.** ✓

## 7. PENDING (§7 card)

Tutti **ereditati**, dichiarati come dipendenze aperte (nessun PENDING nuovo introdotto da B8): L_max latenza Telegram (M-2 OPEN), upgrade empirico orario sessione (M-GOV-1), calibrazione θ_reconcile, congelamento 10 param tuning, run validator sull'edge (DSR/PBO/OOS). Edge resta PENDING-empirico (validator/FASE-D), cardine ereditato da B7.

## 8. Path della card + prossimi passi

- **Card**: `Business Spec/Final/ACTIVE_TASK_B8.md` (card-sorgente, NON installata).
- **Install + ciclo**: decisione AC. Su "vai": installare la card-Developer in `tasks/ACTIVE_TASK.md` (commit `[SPEC-FUNZ-01-B8]` del solo task card, Orchestratore) → `spec_developer` cieco → check post-Developer (6 controlli, indice N/A) + boundary-check → `spec_reviewer` CLI (confronto-copertura vs v2 Sez.10 sulla mappa `c7ce4be`; verifica chiusura 75/75) → chiusura B.
- **Post-B8**: assemblaggio della serie B1..B8 in un unico documento (task dedicato separato) + eventuale avvio FASE-D (validator).

---

## Verdetto finale

✅ **`CARD-B8-DRAFT-PRONTA`** — perimetro riconciliato con la mappa (Sez.10 = 3 req, coincide con atteso ~3); SHA frozen verificati (4 diff vuoti); capitoli framing/premessa identificati (Cap.36.3/53/41); cross-check per-ID PASS (doppia-tracciatura Cap.36.3 risolta); chiusura 75/75 verificata. Nessun blocco. **FERMO**: nessun agente invocato; attendo decisione AC su install + avvio ciclo.
