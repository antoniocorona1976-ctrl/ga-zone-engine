# ESITO_B3-CARD-UPDATE-01 — Installazione card SPEC-FUNZ-01-B3 `rev-B` + verifica seam

**Data**: 2026-06-16 · **Sede**: CLI (Claude Code, GOV-SURFACES-01) · **Esecutore**: Orchestratore CLI.
**Esito sintetico**: card `rev-B` installata su `tasks/ACTIVE_TASK.md` e pushata (`053ca98`); slot attivo **LIBERO**; marcatori B1/B2/CAP-02 **tutti PASS** (0 mismatch); **tutti i pin del §2 risolvono token-per-token**; seam `revoked` (F-1) risolto pulito a **:127** (Cap.7.2) + premessa `6.3` a **:77**; regola di precedenza (F-2) confermata a **:131**. Audit no-DAPI, nessuna probe. **Developer NON invocato** (out-of-scope §0). Nessun CAP modificato (freeze G-09).

---

## 1. Verifica stato repo (RM-2)

### 1.1 `git status --porcelain=v1` (estratto: nessun file-task pendente)
```
 M SINTESI_GOVERNANCE_GA_PER_AC.md      (estraneo al task, dirty preesistente)
?? Business Spec/Final/ACTIVE_TASK_B3_REVB.md   (sorgente rev-B)
?? Business Spec/Final/ISTRUZIONI_B3-CARD-UPDATE-01.md
?? tasks/ACTIVE_TASK_B3.md              (copia di comodo untracked)
... (resto = rumore untracked preesistente: build/, SINTESI_GOVERNANCE_PER_AC/, ecc.)
```
`tasks/ACTIVE_TASK.md`, `tasks/DEV_STATUS.md`, `tasks/STATO_CORRENTE.md` **non** comparivano dirty prima dell'installazione → nessun task pendente.

### 1.2 `git log --oneline -8` (al momento dell'avvio)
```
24ac6f9 [SPEC-FUNZ-01-B3] task card: State-machine & lifecycle (rev-A)
521a610 [STATO] SPEC-FUNZ-01-B2 ri-chiuso PASS 079552c -> b858a88
b858a88 [REVIEW] SPEC-FUNZ-01-B2 re-review (delta) — PASS
e12fc97 [SPEC-FUNZ-01-B2] micro-pass OM-1: §3.10->§8.1
e9ad71b [SPEC-FUNZ-01-B2] micro-pass: finding OM-1 instradato
123e37e [STATO] SPEC-FUNZ-01-B2 CHIUSO PASS 079552c
079552c [REVIEW] SPEC-FUNZ-01-B2 — PASS
ecce6a1 [SPEC-FUNZ-01-B2] Payload del segnale (B2)
```

### 1.2 (bis) Slot attivo
`tasks/DEV_STATUS.md` = **vuoto** (`[]`). Nessun `READY_FOR_REVIEW`/in corso → **SLOT LIBERO**.

### 1.3 Marcatori di chiusura attesi (`tasks/STATO_CORRENTE.md`)
| Atteso | Riga effettiva | Esito |
|---|---|---|
| B1 CHIUSO PASS `7195ffe` | `STATO_CORRENTE.md:7` `SPEC-FUNZ-01-B1: CHIUSO PASS 7195ffe` | **PASS** |
| B2 CHIUSO PASS `b858a88` | `STATO_CORRENTE.md:8` `SPEC-FUNZ-01-B2: CHIUSO PASS b858a88` | **PASS** |
| CAP-02 chiuso PASS `a1625df` (G-25 chiuso) | `STATO_CORRENTE.md:10` `CAP-02: CHIUSO PASS a1625df` | **PASS** |

**0 mismatch.**

---

## 2. Installazione card `rev-B` (punti 4–5)

- `cp "Business Spec/Final/ACTIVE_TASK_B3_REVB.md" → tasks/ACTIVE_TASK.md` eseguito.
- Banner presente: `tasks/ACTIVE_TASK.md:3` → `> **Revisione card rev-B** (post-review di supervisione): chiusi i finding F-1 ... F-2 ... F-3 ... F-5 ... F-6 ...`.
- Sigle finding chiusi tutte presenti: **F-1, F-2, F-3, F-5, F-6** (F-4 ritirato). Riscontro grep su `tasks/ACTIVE_TASK.md`.
- **CARD rev-B INSTALLATA: SÌ.**

---

## 3. Tabella pin §2 (punto 6) — verifica token-per-token su `CAP_02_parte_II.md` (Cap.6.1/6.3, 7.1–7.6, 11.1–11.5, preambolo)

Tutti i pin del §2 della card **risolvono**. Nessuna correzione necessaria.

| Pin (CAP_02_parte_II.md:) | Fatto | Risolve? |
|---|---|---|
| :5 | cap ≤2 giorni di trading dal raw touch (eredità CAP-01) | sì |
| :7 | Q-05 — 3 clausole (state machine 1+6, target_2 campo, submacchina) | sì |
| :63 | Δt_cromosoma dominio {1..1680}=2×840 min, decorrente dal raw touch | sì |
| :95 | state machine 1 non-terminale + 6 terminali (Q-05 Cl.1) | sì |
| :99 | nessun terminale ammette transizioni uscenti | sì |
| :101 | target_1_hit terminale di successo, chiude il contratto; target_2 non è transizione | sì |
| :105 | invalidated (pre-raw-touch) distinto da stopped; stop attraversato pre-touch | sì |
| :107 | missed_target riferito a target_1 (Q-03), non target_2 | sì |
| :109 | expired con due cause (pre/posttrigger_timeout) come campo causale | sì |
| :113 | NB-9: target_1_hit→revoked non esiste | sì |
| :124 | transizione active→invalidated (riga tabella 7.2) | sì |
| :125 | transizione active→missed_target | sì |
| :126 | transizione active→expired (a/b cause) | sì |
| :127 | **transizione active→revoked** (sostituzione, Cap.6.3) — *seam F-1* | sì |
| :129 | nessuna transizione esce dai terminali; target_1_hit non→target_2_hit/revoked/... | sì |
| :131 | **precedenza eventi** expiry>invalidazione>missed_target>raw touch>post-trigger (determinismo replay) — *F-2* | sì |
| :135 | definizione raw touch (barra 1-min, livello discreto entry_zone, no vincolo direzione) | sì |
| :137 | trigger_event; raw touch **sempre eseguibile**; nessun filtro post-emissione | sì |
| :139 | trigger_event non è stato; segnale resta active; motore non osserva il fill manuale | sì |
| :145 | NB-8(a) barra di emissione, valutazione da t_emission+1 | sì |
| :147 | NB-8(b) gap overnight non azzera il raw touch | sì |
| :149 | NB-8(c) gap opposto → invalidated / missed_target | sì |
| :155 | expiry = t_exec + Δt_cromosoma (min di trading) | sì |
| :157 | counter solo 8:00–22:00, arresto notte/weekend/festivi (esempio multi-giorno) | sì |
| :159 | scadenza → expired/posttrigger_timeout; dominio fuori {1..1680} = non valido | sì |
| :163 | T_touch_max ∈ {5..480}, counter sui minuti di trading | sì |
| :165 | scadenza senza raw touch → expired/pretrigger_timeout (campo, non stato) | sì |
| :167 | razionale anti-degenerazione executable_rate | sì |
| :171 | M-1 contratto osservazione; N_pivot non fissato in Parte II (→Parte V); algoritmo→Parte III | sì |
| :173 | osservazione barre 1-min da 8:00 CET; vincolo metodologico latenza pivot | sì |
| :175 | cadenza = barra 1-min chiusa, no tick intra-bar | sì |
| :349 | Q-05 Cl.3 separazione segnale vs position lifecycle | sì |
| :351 | lifecycle segnale (Cap.6-10) chiude in target_1_hit | sì |
| :362 | fill = raw touch; boundary = target_1_hit; gestione oltre = operatore | sì |
| :368 | OUT-OF-SCOPE (execution policy/scaling/trailing/sizing/take profit; punto 8) | sì |
| :370 | IN-SCOPE metriche per reporting fold-by-fold | sì |
| :372 | π_{t2\|t1} hit-rate condizionale target_2 dato target_1 | sì |
| :374 | f_{stop\|t1} frequenza stop post-target_1 | sì |
| :375 | distribuzione tempi di permanenza post-target_1 | sì |
| :381 | evento ingresso submacchina = target_1_hit | sì |
| :383 | stato iniziale tracking_active | sì |
| :385 | eventi submacchina (target_2_reached/stop_after_target_1/retracement_to_entry/position_close_event) | sì |
| :391 | terminale tracking_closed | sì |
| :393 | indipendenza: submacchina non modifica lo stato del segnale; log separati per signal_id | sì |
| :397 | space search del cromosoma NON esteso | sì |
| :399 | metriche submacchina come obiettivi di qualità informativa, non variabili decisionali | sì |
| :401 | razionale (punto 8; overfitting/DSR-PBO) | sì |

**Premessa supersessione 6.3** (seam): **:77** — "Emette un nuovo segnale … il segnale precedente … viene revocato e transita nello stato terminale `revoked`" (sostituzione-non-edit). Il vincolo `|𝒜(t)|≤1` (segnale unico attivo) è a **:81** ed è **materia B2** (non da ri-consolidare in B3, AC-G11).

---

## 4. Risoluzione dei due seam (punto 7)

### 4.1 Seam `revoked` (F-1) — transizione `active→revoked`
`grep -ni "revoked\|supersed\|signal_id"` + lettura Cap.7.1/7.2:
- Stato `revoked` definito a **:111** (§7.1).
- **Transizione `active→revoked` risolve PULITO a `:127`** (§7.2, riga tabella): `| active | revoked | Il motore emette un nuovo signal_id (sostituzione, Cap.6.3) |`.
- → Caso **7b**: placeholder `<riga-7.2-da-confermare>` **sostituito con `:127`** in `tasks/ACTIVE_TASK.md` (verifica meccanica del pin, non ripianificazione). **Nessun `[B-N PROVVISORIO]` necessario** (il Cap.7.2 ha riga di transizione propria; non rimanda interamente a 6.3).

### 4.2 Premessa `6.3` (punto 7d)
`<riga-6.3>` **sostituito con `:77`** (2 occorrenze: card §1 nota di confine + §2). `:77` è la riga che definisce la supersessione/sostituzione-non-edit.

### 4.3 Note di prosa ora stale (NON corrette qui — fuori scope "non ripianificazione"; per il giro-Planner separato)
- `tasks/ACTIVE_TASK.md:64`: la parentetica "(pin **non risolto a monte** …)" è ora **stale** (il pin è risolto a `:127`). Editoriale, non bloccante.
- `tasks/ACTIVE_TASK.md:214`: la nota di chiusura descrive ancora `<riga-7.2-da-confermare>`/`<riga-6.3>` come "puntatori da risolvere" — ora risolti. Editoriale, non bloccante.
- Raccomandazione: pulizia di queste due prose nel prossimo giro-Planner (non impattano contenuto/cecità/tracciabilità).

---

## 5. Regola di precedenza (F-2, punto 8)
**`:131` RISOLVE token-per-token**: "La precedenza degli eventi a parità di timestamp è: expiry > invalidazione > missed_target > raw touch > azione post-trigger. … essenziale per rendere deterministico il replay (Cap.10)." L'invariante di determinismo su cui poggia la categoria *valore-di-sistema* (F-2) esiste nel CAP.

---

## 6. Commit (punto 9)
`git add tasks/ACTIVE_TASK.md` → commit **`053ca98`** `[SPEC-FUNZ-01-B3] card rev-B: chiusi F-1/F-2/F-3/F-5/F-6; pin revoked/6.3 risolti in CLI` → push `origin/main` OK (`24ac6f9..053ca98`). Solo `tasks/ACTIVE_TASK.md` nel commit.

---

## 7. Applicazione RM-1 a me stesso

- **"Slot LIBERO"** → PROVE: `cat tasks/DEV_STATUS.md` = vuoto; `git status` non mostra task-file pendenti. ALT. ESCLUSA: READY_FOR_REVIEW nascosto — escluso (file vuoto, ispezione diretta). ALT. NON ESCLUSA: nessuna.
- **"B1/B2/CAP-02 ai commit attesi"** → PROVE: grep su `STATO_CORRENTE.md` righe 7/8/10 con SHA esatti. ALT. ESCLUSA: marcatore divergente — escluso per match testuale. ALT. NON ESCLUSA: nessuna.
- **"Tutti i pin §2 risolvono"** → PROVE: Read integrale di Cap.6.1(:55-70), 6.3(:75-87), 7.1-7.6(:91-175), 11.1-11.5(:345-409), preambolo(:1-9); confronto fatto↔riga per ogni pin (tabella §3). ALT. ESCLUSA: una riga citata non contiene il fatto — esclusa per ispezione diretta. ALT. NON ESCLUSA: scarto di ±1 riga su edizioni future del CAP (CAP frozen `a1625df`, quindi non si applica ora).
- **"Transizione active→revoked a :127"** → PROVE: riga 127 = `| active | revoked | Il motore emette un nuovo signal_id (sostituzione, Cap.6.3) |`. ALT. ESCLUSA: il Cap.7 rimanda interamente a 6.3 (avrebbe richiesto `[B-N PROVVISORIO]`) — esclusa: la riga di transizione propria esiste in 7.2. ALT. NON ESCLUSA: nessuna.
- **"Premessa 6.3 a :77"** → PROVE: riga 77 definisce emissione nuovo signal_id + revoca del precedente. ALT. ESCLUSA: che la supersessione viva altrove in 6.3 — :81 porta `|𝒜(t)|≤1` (constraint, B2), :77 porta il meccanismo (premessa corretta per il seam). ALT. NON ESCLUSA: si potrebbe citare anche :81 come premessa aggiuntiva del "segnale unico attivo" (non necessario per la transizione, ed è B2).
- **"Card rev-B installata"** → PROVE: banner a `:3`, commit `053ca98` con il solo `tasks/ACTIVE_TASK.md`. ALT. ESCLUSA: copia parziale — esclusa (cp completo, banner+sigle presenti). ALT. NON ESCLUSA: nessuna.

**Lista "Empirico-CLI da verificare": VUOTA** (audit documentale, no-DAPI; nessuna asserzione richiede DAPI/filesystem runtime).

---

## 8. Stato finale

`SLOT ATTIVO: LIBERO`
`CARD rev-B INSTALLATA: SÌ`

PRONTO PER DECISIONE SUPERVISORE SU PROMOZIONE B3
