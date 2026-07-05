# ISTRUZIONI_M0-T1-REVIEW-01 — Audit ostile del task M0-T1

**Etichetta: NON AUDITATO** (card del Planner per il thread Review).

---

## REGOLA N.1 — REVIEW SEMPRE SU FILE

**Ogni uscita di questa esecuzione — completata, STOP, errore, blocco guard — termina scrivendo `Codice/Piano_di_lavoro/Review/REVIEW_M0-T1.md`** (intestazione con data/ora e verdetto). In chat solo 5 righe di riassunto. Se ti fermi, il motivo sta nel file.

## USO (protocollo file-bus)

Questo file è stato trascinato nella finestra CLI. Primo atto di filing: copialo tu in `Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_M0-T1-REVIEW-01.md`.

---

RUOLO: `prog_reviewer` (role file `.claude/agents/prog_reviewer.md`). Audit ostile: cerchi di rompere il lavoro, non di promuoverlo. RM-1/RM-2: ogni claim con path:riga o hash; per ogni conferma di prova empirica, alternative enumerate ed escluse.

VIETATO: correggere codice, ripianificare, toccare piano/DECISIONI/spec/CAP/ruoli, ridefinire scope. Solo findings. Se serve una decisione: la marchi PENDENTE-PLANNER, non la prendi. Nessun DAPI (D-6).

## 1. Perimetro dell'audit

- Catena commit del task: `55dc943` (decreti + STATO) → `adc30d1` (build) → `d701918` (appendice ESITO) → `101335e` (DEV_STATUS). Diff integrale della catena.
- File: `src/data_layer/`, `tests/data_layer/`, `Codice/Piano_di_lavoro/DECISIONI.md` (sole righe appese), `tasks/ACTIVE_TASK.md`, `tasks/STATO_CORRENTE.md`, `tasks/DEV_STATUS.md`, `Codice/Piano_di_lavoro/Esito/ESITO_M0-T1.md`.
- Contratto di riferimento: card `Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_M0-T1_v2.md` + `docs/spec_funzionale/SPEC_FUNZ_01.md` (CN-9.5/9.7/9.9, R-9.3, R-9.14 — letture per range, GC-4) + DEC-C/DEC-D.

## 2. Assi di audit (minimo obbligatorio; aggiungi ciò che trovi)

**A. Conformità alla card.** Ogni prescrizione §0-bis..§7 della v2 eseguita come scritta; elenca ogni deviazione (es.: ESITO committato in `d701918` invece che nel commit finale come da §6 — classificala).
**B. Riproducibilità done-when.** Riesegui tu `pytest` due volte: 8/8 verdi entrambe; T6 (byte-identico) confermato con i TUOI due run, hash riportati.
**C. RM-1 sulle prove empiriche.** (1) Discriminante settle-row `volume==0`: alternative enumerate ed escluse davvero, o asserite? (2) Ordine colonne O/C: cosa è PROVATO e cosa è ASSUNTO — quantifica (il PENDENTE "disambiguazione O/C statistica" è il bersaglio: barre non-flat che discriminano, quante, in che direzione).
**D. Timezone.** Conversione America/Chicago → CET via tz-database (DST-safe) o offset fisso? Prove sulle barre di confine sessione (01:00 CST = 08:00 CET); comportamento attraverso un cambio DST se il codice lo permette (anche solo per costruzione, dato che il sample è solo dicembre).
**E. Regole griglia.** R-9.3 forward-fill esatto (O=H=L=C=Close prec., V=0, tick_count=0); semantica `bar_synthetic` (R-9.14); header CN-9.5 ordine esatto; tipi CN-9.7 (uso di `0` vs `NULL` per `tick_count`: quale e perché, coerenza card/spec); `date`/`time` derivati da `timestamp` (CN-9.9).
**F. Giorno parziale.** 1167 = 840 + 327: ricostruisci quale regola il builder ha applicato al giorno non completo (finestra osservata? padding? troncamento?), verifica che T4 non lo copra, descrivi il comportamento effettivo con numeri. NON decidere la politica: finding + dati per il decreto del Planner.
**G. Decreti e stato.** Righe DEC-C/DEC-D appese verbatim (diff), nessuna riga preesistente riscritta; `STATO: v1.1 chiusa` presente; commit dedicato; `source=PORTARA`, `symbol=FIB`, `timeframe=60s` effettivamente asseriti nei test e presenti nell'output; citazione decoder legacy (`scripts/export_directa_history_parametric.py:797,802,885-887`) verificata a quelle righe.
**H. Tick-grid.** Ricalcola indipendentemente gli off-tick sull'intero sample: 30319 e 30389 confermati? Altri sfuggiti? Barre non alterate (no clamping) confermato sul codice e sull'output.
**I. Igiene.** Perimetro commit pulito (nessun file estraneo nella catena); nessun bypass del guard stile D-14 (`git add ; git commit` concatenati per eludere il hook — controlla la history dei comandi se ricostruibile, altrimenti dichiara non verificabile); lessico "verific*" nel testo nuovo.

## 3. Formato findings

`R-F1..R-Fn`, ciascuno: **[taxonomy: BUG REALE / MIGLIORA PERFORMANCE / NEUTRO / RISCHIO PEGGIORAMENTO] [severità: BLOCCANTE / alta / media / minore]** + problema / conseguenza / impatto se non risolto + citazioni path:riga o hash. Poi: sezione **NON VERIFICABILE** (esplicita, RM-1); elenco PENDENTE-PLANNER con i dati raccolti (senza decidere); **VERDETTO: PASS / CONDITIONAL / FAIL** sul task M0-T1 con motivazione in 3 righe.

## 4. Chiusura

1. Scrivi `Codice/Piano_di_lavoro/Review/REVIEW_M0-T1.md` (Regola n.1).
2. Append a `tasks/DEV_STATUS.md`: `REVIEW M0-T1: <verdetto> — <data>` (mai riscrivere righe esistenti).
3. Commit con add espliciti dei soli: `Review/REVIEW_M0-T1.md`, `Istruzioni/ISTRUZIONI_M0-T1-REVIEW-01.md`, `tasks/DEV_STATUS.md`. Staging estraneo → STOP + REVIEW file. Messaggio: `REVIEW M0-T1: <verdetto>`. Push. Nel testo nuovo evita "verific*" dove possibile; se `rm_guard` scatta: STOP + REVIEW file, chiedi override ad AC.
