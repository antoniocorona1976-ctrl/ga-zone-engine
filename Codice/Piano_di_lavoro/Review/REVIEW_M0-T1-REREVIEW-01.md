# REVIEW_M0-T1-REREVIEW-01 — re-review delta del fix (chiusura #1 + DEC-E)

**Data/ora**: 2026-07-05 23:55 CET
**VERDETTO SUL DELTA: PASS** — **il ciclo M0-T1 è chiudibile** (la chiusura formale la ordina il Planner).
**Reviewer**: `prog_reviewer` (card `Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_M0-T1-REREVIEW-01.md`, assi A–E)
**Perimetro**: SOLO delta del fix — catena `01c53aa` → `c78c358` → `e656315` → `5ee357c`; contratto `ISTRUZIONI_M0-T1-FIX-01.md` + DEC-E. Assi già chiusi da REVIEW_M0-T1 (`225057d`) non riaperti. Instradamento AC citato dal contesto autoritativo: #1 → Developer, #5 → DEC-E, #4 → M0-T2, #2/#3/#6 ignorati.

---

## Iterazione 1 — 2026-07-05

### A. Finding #1 chiuso davvero

- **Fixture tracciata**: `git ls-files data/samples/portara_isp/` → `data/samples/portara_isp/ISP2023Z.txt` (prima review: vuoto). `git show --stat c78c358` = **SOLO quel path**, 1000 inserzioni.
- **Prova GC-3 rifatta dal Reviewer** (non fidandomi del transcript del Developer): mio worktree da HEAD (`git worktree add <scratchpad>/wt_rereview_gc3 HEAD`, detached su `5ee357c`, soli file tracciati), `python -m pytest tests/data_layer/ -v` eseguito lì → **9/9 PASSED** (output raccolto; T1..T9 tutti verdi). Worktree rimosso a fine prova (`git worktree list` → solo il repo principale). La suite gira su soli file tracciati: GC-3 soddisfatta.
- **Docstring — 6 correzioni della tabella ESITO §2 confermate alle righe attuali**: `isp_loader.py:5-6` ("Fixture (GC-3): ... tracciata nel repo dal commit c78c358"); `isp_loader.py:39-46` (paragrafo DEC-E al posto della vecchia "decisione di modulo"); `isp_loader.py:246-248` (commento fuori-sessione riformulato + rinvio #4); `test_isp_loader.py:1,5-6` (T1..T9 + fixture tracciata); `test_isp_loader.py:25` ("sul sample tracciato in repo"); `__init__.py:3-4` (fixture tracciata da c78c358).
- **Claim residui falsi**: `grep -rni "committat" src/data_layer/ tests/data_layer/` → **zero occorrenze** (exit 1). Il claim in `tasks/ACTIVE_TASK.md` è diventato vero col commit `c78c358` (file correttamente non toccato, fuori add-list — nota ESITO §2 esatta).

### B. DEC-E conforme al decreto

- **Riga DEC-E**: confronto meccanico carattere-per-carattere card FIX-01 §0-bis ↔ `DECISIONI.md` = **IDENTICA**; diff di `01c53aa` = 1 sola riga aggiunta, zero righe preesistenti toccate.
- **Bordi esclusi CON conteggio ED elenco**: `report.excluded_edge_days` espone `PartialDay(date, rows_observed, real_bars, first_time, last_time)` (`isp_loader.py:128-136,269-278`) — mai scarto silenzioso; run diretto del Reviewer: `('2023-12-13', 262, 211, '17:38:00', '21:59:00')` e `('2023-12-15', 65, 43, '08:00:00', '09:04:00')`.
- **Definizione di giorno completo** (`isp_loader.py:262-265`): prima barra reale = 08:00 CET E ultima = 21:59 CET — legittima rispetto a R-9.3 (`SPEC_FUNZ_01.md:1224`, finestra 08:00–22:00 con ultimo SOB 21:59): sui bordi del dataset la troncatura è indistinguibile dall'assenza di scambi, ed è esattamente il caso che DEC-E decreta di escludere. Caveat non bloccante: un giorno interno con primo minuto 08:00 senza trade risulterebbe "parziale interno" pur essendo semanticamente no-trade — casistica dichiaratamente rinviata da DEC-E a M0-T2 (sessioni corte incluse).
- **Gestione interinale delle parzialità INTERNE** — classificazione richiesta dalla card: **CONFORME a DEC-E**. Il decreto prescrive solo "anomalia da riportare (gestione decisa in M0-T2)": il modulo riporta (`report.internal_partial_days`, `isp_loader.py:280-283`) e in via interinale tiene il giorno in griglia sull'intervallo osservato — scelta oltre la lettera ma non contraria (nessuna gestione è decretata; nessuno scarto silenzioso; interim dichiarato in docstring `isp_loader.py:43-46` e in ESITO §3). Riserva: il ramo non è esercitato dalla fixture (0 casi) — vedi RR-F2.
- **T9 pinna la policy** (`test_isp_loader.py:259-273`): 840 righe, tutte del 2023-12-14; esclusi `[("2023-12-13",262),("2023-12-15",65)]`; `real_bars == [211, 43]`; `internal_partial_days == ()`. Test non vacuo (valori letterali, non derivati dal modulo).
- **Numeri riconciliati** (ricalcolo indipendente del Reviewer, script che non importa `src/data_layer`): barre valide per giornata nativa = **211 / 745 / 43** (tot 999 ✓; il 15/12 ha 44 righe raw − 1 settle = 43 ✓); coperture 262 (17:38–21:59) e 65 (08:00–09:04) = le righe che quei giorni producevano nella vecchia griglia (1167 = 262+840+65, prima review) ✓; griglia nuova: 745 reali + 95 sintetiche = **840** ✓.

### C. Asserzioni vecchio→nuovo — nessun test indebolito di nascosto

Tabella ESITO §4 controllata riga per riga sul diff `adc30d1..e656315`:
- fixture pytest `grid`→`result/grid/report`: adattamento API, sostanza intatta.
- T2: usa la fixture condivisa invece di ricostruire la griglia; asserzione `volume==0 ⇔ bar_synthetic` invariata (`test_isp_loader.py:115`). Il docstring aggiorna "320" → "319 (più la settle stessa)" — vedi RR-F1.
- T5: `999→745` reali e `>0→==95` sintetiche — conseguenza diretta di DEC-E, e il nuovo `n_synth == 95` è PIÙ forte del vecchio `> 0`; il confronto puntuale barra-per-barra resta integrale.
- T6: stessa logica, hash cambiato per contenuto (840 righe). **Riprodotto ×2 dal Reviewer in processi separati**: sha256 = `c1d9a8287c111f0b17cf9e38e108d011480490ef01461682ef6e29973bcdb8db` identico nei due run e **identico all'hash dichiarato dal Developer**.
- T7: re-pinning griglia 30319→30389 giustificato (il giorno del 30319 è bordo escluso da DEC-E); **il finding NON è perso**: run diretto del Reviewer su `tick_grid_findings(parsed.bars)` → esattamente i 3 off-tick noti, 30319 incluso (la diagnostica opera sulle barre raw, invariata, `isp_loader.py:193-208`); T7 asserisce tuttora `30319 in values` + set esaustivo (`test_isp_loader.py:218-221`) + presenza del 13/12 nel report esclusi (`:229`). Anzi: il controllo su 30389 ora pinna anche `open` (`:226`), prima solo `high` — rafforzato.
- T8: prova tz sui bordi spostata dal frame al report, con assert NUOVI sulle coperture (17:38–21:59, 08:00–09:04, `test_isp_loader.py:253-256`) — rafforzato, non indebolito.
- T9 nuovo; T1/T3/T4 invariati (testo identico alla prima review).
- Trasparenza TDD del Developer (44→43 su run rosso, ESITO §4) coerente con la mia riconta (43 = 44 raw − settle).

### D. Perimetro e igiene

- `01c53aa` = solo `DECISIONI.md` (+1 riga); `c78c358` = sola fixture; `e656315` = 6 file, esattamente l'add-list §4 (348+/46−, come dichiarato); `5ee357c` = solo ESITO (appendice). Nessun file estraneo.
- `tasks/DEV_STATUS.md`: diff = 1 riga appesa (`FIX M0-T1: READY_FOR_RE-REVIEW — 2026-07-05`), nessuna riga preesistente riscritta.
- **Finding #4 NON toccato**: diff della regione fuori-sessione (`isp_loader.py:245-249`) = solo commento riformulato, la logica (`continue` senza contatore) è identica — conforme all'out-of-scope §3.
- Bypass guard: history dei comandi non ricostruibile (vedi NON VERIFICABILE); per costruzione del hook (scatta sul comando `git commit` stesso) la separazione add/commit — istruita dall'Orchestratore per il falso positivo basename — non costituisce elusione.
- Lessico: nessuna aggiunta "verific*" nei 4 commit fuori dal testo della card FIX-01 stessa (che cita la regola di lessico — artefatto del Planner copiato verbatim, ammesso).

### E. Regressioni

- Suite completa T1–T9 rieseguita ×2 dal Reviewer nel repo principale: **9/9 e 9/9**. T4 invariato e verde; T1/T3 invariati e verdi; gli assi della prima review non toccati dal fix (parser, tz, header, tipi, decreti C/D, determinismo) restano coperti dagli stessi test, tutti verdi.

---

### Findings

**RR-F1 — [NEUTRO] [severità: minore] Correzione 320→319 nel docstring di T2 tocca l'oggetto del finding #2 "ignorato".**
- *Problema*: la card FIX-01 §3 elenca #2/#3/#6 come out-of-scope ("ignorati per decisione AC"); il diff di `e656315` corregge comunque il conteggio delle barre flat nel docstring di T2 (`test_isp_loader.py:103`: "319 (più la settle stessa)", prima "320") — materia del finding #2.
- *Impatto*: zero sul comportamento; la correzione è fattualmente giusta (mia riconta prima review: 319 flat regolari + settle) e avviene in un file legittimamente in lavorazione. Deviazione dalla lettera dell'out-of-scope, migliorativa; l'ESITO però non la dichiara nella tabella §4 (la riga T2 dice "nessun cambio di sostanza" senza menzionare il ritocco al conteggio).

**RR-F2 — [NEUTRO] [severità: minore] Ramo "parzialità interne" non esercitato dalla fixture (dead branch sul sample).**
- *Problema*: `isp_loader.py:280-283` (anomalia interna → report + giorno tenuto sull'intervallo osservato) non è attraversato da alcun dato del sample (0 casi); T9 pinna solo il conteggio 0 (`test_isp_loader.py:273`). Il comportamento del ramo (incluso il forward-fill su un giorno interno monco) non ha copertura di test su dati.
- *Impatto*: nessuno oggi; in M0-T2, quando la gestione sarà decretata, servirà una fixture sintetica che eserciti il ramo. Coerente con DEC-E (gestione rinviata), quindi non richiesto ora.

**Deviazioni di processo (non bloccanti, pattern già classificati):**
- **D1-bis [NEUTRO]**: appendice ESITO in commit dedicato `5ee357c` — stesso pattern della deviazione D1 (REVIEW_M0-T1) già classificata NEUTRO: l'hash del commit finale non può vivere nel commit stesso; autodichiarata (ESITO §7).
- **D2-bis [NEUTRO]**: §0-bis (DEC-E) eseguito dall'Orchestratore (`01c53aa`) e non dal Developer — ordine del Planner, dichiarato nel contesto autoritativo; contenuto controllato carattere-per-carattere (asse B).

### NON VERIFICABILE (esplicito, RM-1)

1. **History dei comandi shell del Developer** (add/commit concatenati, asse D): non ricostruibile dal repo. Come nella prima review: la separazione add/commit è istruzione dell'Orchestratore per il falso positivo basename e il hook `rm_guard` scatta comunque sul comando `git commit` — nessuna elusione per costruzione; l'esecuzione effettiva resta non ricostruibile.
2. **Transcript della prova worktree del Developer** (ESITO §7): autodichiarazione non riprodotta alla lettera; SOSTITUITA dalla mia prova equivalente e indipendente (worktree mio da HEAD, 9/9) — il fatto sostanziale (GC-3 su soli file tracciati) è accertato in proprio.
3. **Comportamento del ramo parzialità-interne su dati reali**: non esercitabile sulla fixture (0 casi, RR-F2); resta accertato solo per lettura del codice.

### PENDENTE-PLANNER (dati raccolti, nessuna decisione presa)

1. **Gestione parzialità interne** (da DEC-E, M0-T2): con la decisione, prevedere una fixture sintetica che eserciti il ramo `internal_partial_days` (oggi dead branch, RR-F2); dati: interim attuale = giorno in griglia sull'intervallo osservato + report.
2. **Contatore/diagnostica barre fuori sessione** (finding #4, già vincolato a M0-T2 da AC): regione `isp_loader.py:245-249` intatta come prescritto.
3. **Sessioni corte da calendario di borsa** (DEC-E le rinvia esplicitamente a M0-T2, tape pluriennale + calendario).

### Tabella "Classificazione per il supervisore"

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|------------------------|
| RR-F1 | Ritocco 320→319 nel docstring T2 (oggetto del finding #2 "ignorato"), non dichiarato nella tabella vecchio→nuovo | `test_isp_loader.py:103`; ESITO FIX §4 riga T2 | NEUTRO | No |
| RR-F2 | Ramo parzialità-interne non esercitato dalla fixture (T9 pinna solo lo 0) | `isp_loader.py:280-283`; `test_isp_loader.py:273` | NEUTRO | No (fixture sintetica in M0-T2, col decreto di gestione) |

### Applicazione RM-1 a me stesso (BASE_COMUNE §8)

- "9/9 ×2": output pytest dei miei due run nel repo principale (asse E) + terzo run 9/9 nel MIO worktree (asse A).
- "GC-3 soddisfatta": prova diretta in worktree da HEAD con soli file tracciati; alternativa esclusa: dipendenza da file untracked del repo principale (il worktree non li contiene per costruzione; la fixture arriva da `c78c358`, in `git ls-files`).
- "Hash T6 identico al dichiarato": sha256 ricalcolato in due processi separati = `c1d9a828…bcdb8db`, confronto testuale col valore dell'ESITO §4.
- "211/745/43": riconta con script autonomo che non importa il modulo sotto audit; "262/65": differenza orari prima/ultima reale, coerente coi conteggi della prima review (1167 = 262+840+65).
- "DEC-E verbatim": confronto programmatico carattere-per-carattere + diff dal parent (1 sola riga `+`).
- "Finding 30319 non perso": run diretto di `tick_grid_findings` sulle barre raw → i 3 noti, nessun altro.
- Non escluso da me: i 3 punti in NON VERIFICABILE.

### VERDETTO SUL DELTA: PASS

Il finding #1 è chiuso con prova indipendente (fixture in `git ls-files`, 9/9 su MIO worktree da soli file tracciati, zero claim residui); DEC-E è registrato verbatim, implementato fedelmente (bordi esclusi e contati: 262/211 e 65/43; 745+95=840; 211+745+43=999) e pinnato da T9; nessun test indebolito di nascosto (T5/T7/T8 anzi rafforzati), hash T6 riprodotto, perimetro commit pulito, finding #4 intatto. Due soli rilievi NEUTRO minori (RR-F1, RR-F2), nessun BUG REALE: **il ciclo M0-T1 è chiudibile** — la chiusura formale la ordina il Planner.
