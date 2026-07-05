# REVIEW_M0-T1 — audit ostile del task M0-T1 (loader fixture ISP → griglia canonica 13-campi)

**Data/ora**: 2026-07-05 23:12 CET
**VERDETTO: CONDITIONAL**
**Reviewer**: `prog_reviewer` (card `Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_M0-T1-REVIEW-01.md`, assi A–I eseguiti)
**Perimetro**: catena `55dc943` → `adc30d1` → `d701918` → `101335e`; contratto = `ISTRUZIONI_M0-T1_v2.md` + SPEC_FUNZ_01 (range citati) + DEC-C/DEC-D. Sede CLI, nessun accesso DAPI/rete (D-6): tutte le prove su fixture locale e repo.

---

## Iterazione 1 — 2026-07-05

### Riassunto esecuzioni del Reviewer (asse B — riproducibilità)

- **pytest, run 1**: `python -m pytest tests/data_layer/ -v` → **8/8 PASSED** (T1..T8).
- **pytest, run 2**: idem → **8/8 PASSED**.
- **T6 riprodotto indipendentemente** (due processi Python separati, fuori da pytest): CSV → sha256 identico sui due run: `1267cb3a4e4e2df3d0f5951764f0496f70adcf5d96c3ae8b79494e61d859e99c` (1167 righe dati + header). Byte-identico confermato con i MIEI run e hash.

### Esiti per asse (sintesi con citazioni)

**A. Conformità alla card v2** — §0 precondizioni: commit `774f9d3`/`4b877db`/`bb8d625` presenti in history (riscontro `git log`), fixture presente (52.499 byte, `ls`). §1 `tasks/ACTIVE_TASK.md` intestato `# TASK ATTIVO: M0-T1 ...` con riferimento card (diff `adc30d1`). §2 layout rispettato (`src/data_layer/`, `tests/data_layer/`, pandas/numpy, nessuna dipendenza extra). §3 perimetro rispettato. §4 done-when: 8/8 due volte (sopra). §5 out-of-scope: nessun socket/DAPI nel diff, CAP/spec/piano/METODO/ruoli intatti (file-list dei 4 commit). §6 add-list del commit finale: esattamente i 7 file attesi (`git show --stat adc30d1`). Deviazioni: D1/D2/D3 sotto (tutte NEUTRO) + **R-F1** (fixture non committata: la card §6 non la includeva, ma GC-3 la esige — vedi finding).

**B. Riproducibilità** — sopra: 8/8 ×2, T6 byte-identico con hash del Reviewer.

**C. RM-1 sulle prove empiriche** —
- *Settle-row `volume==0`*: alternative escluse DAVVERO, non asserite. Ricalcolo indipendente sull'intero sample: 1 sola riga con col9==0 (riga 1000, `ISP2023Z,20231215,1038,30434,30434,30434,30434,1,0`); contro-conteggi delle alternative: col8==0 → 146 righe regolari (tutte flat, col9>0); flat regolari → 319; off-tick su barre negoziate → 3 valori. I numeri dell'ESITO (§4) reggono, salvo il "(320 righe regolari)": sono 319 regolari + la settle (anch'essa flat) — imprecisione minore (R-F2).
- *Ordine O/C*: PROVATO a vincolo rigido solo {H=max, L=min} → 2 permutazioni superstiti (OHLC, CHLO), riprodotto sulle 24 permutazioni. L'esclusione di CHLO è **statistica, non rigida** — e l'ESITO lo dichiara onestamente ("NON ESCLUSE: ... l'esclusione è statistica"). Quantificazione del Reviewer: 574 barre non-flat (O≠C) su 999; sulle 996 coppie consecutive intra-day (settle esclusa): media |O_t−C_(t−1)| = **3.61** per OHLC vs **10.07** per CHLO (fattore 2.79); per-coppia: **572** coppie favoriscono OHLC, **112** CHLO, 312 pari. Direzione concorde e robusta. Però: i numeri dell'ESITO (997 coppie, 3.72 vs 10.17) si riproducono **solo includendo la settle-row nel calcolo** (1000 righe − 3 giornate = 997 coppie; riprodotto esattamente: 3.72/10.17) — la metrica del blocco PROVE include il dato che il Developer stesso classifica non-barra (R-F2). Conclusione invariata in entrambe le varianti.

**D. Timezone** — conversione via `zoneinfo.ZoneInfo` (tz-database), NON offset fisso: `isp_loader.py:181-184,205-206`. Prove dirette del Reviewer su `_to_cet`: `20231214 0100` → `08:00` (+7h, CST→CET, la barra di confine richiesta dalla card); `20230714 0100` → `08:00` (+7h, CDT→CEST); finestre di disallineamento USA/EU: `20230315 0100` → `07:00` (+6h: USA già in DST dal 12/03, EU ancora no) e `20231101 0100` → `07:00` (+6h: EU uscita dal DST il 29/10, USA ancora dentro fino al 05/11) — gli offset variano correttamente col calendario DST delle due zone (+7h a regime, +6h nelle due finestre): DST-safe per costruzione, incompatibile con qualunque offset fisso. Il target CET è `Europe/Rome` (gestisce CEST), `isp_loader.py:86`.

**E. Regole griglia** — R-9.3 (`SPEC_FUNZ_01.md:1224`): forward-fill esatto `O=H=L=C=Close prec., Volume=0, tick_count=0` a `isp_loader.py:239-245`, testato riga-per-riga in T5 (`test_isp_loader.py:146-158`). R-9.14 (`:1279`): `bar_synthetic=False` se barra nel dato, `True` altrimenti — rispettata (T5, incluso il confronto puntuale OHLCV+tick per ogni barra reale via mappatura tz inversa, `test_isp_loader.py:160-176` — test non vacuo). CN-9.5 (`:1335`): header 13 campi esatto, doppio pin in T3 (contro la costante E contro la lista letterale, `test_isp_loader.py:100-105`) + prima riga CSV controllata dal Reviewer. CN-9.7 (`:1341`): `tick_count` int64 ≥0 (la colonna esiste nel sample → niente NULL, come da card §3.4); per i minuti sintetici `0` e non NULL — coerente card/spec perché R-9.3 prescrive letteralmente `tick_count = 0` per i minuti no-trade (`:1224`); `bar_synthetic` booleano True/False nel CSV. CN-9.9 (`:1347`): `date`/`time` derivati da `timestamp`, asserito in T3 (`test_isp_loader.py:113`).

**F. Giorno parziale** — ricostruito: il builder applica griglia per giornata = `[max(08:00 CET, prima barra reale), min(21:59 CET, ultima barra reale)]` (`isp_loader.py:222-226`; poiché le barre sono pre-filtrate alla sessione, di fatto = [prima reale, ultima reale]). Numeri del Reviewer (ricalcolo indipendente): 2023-12-13 → 262 righe (17:38–21:59), 2023-12-14 → 840 (08:00–21:59), 2023-12-15 → 65 (08:00–09:04); totale 1167 = 262+840+65 = 999 reali + 168 sintetiche. **T4 NON lo copre** (filtra `COMPLETE_DAY="2023-12-14"`, `test_isp_loader.py:123`); nessun test asserisce 1167/262/65. Politica = decisione di modulo del Developer, documentata (ESITO §7, docstring `isp_loader.py:37-43`), rinviata a M0-T2 → PENDENTE-PLANNER (dati sotto), R-F5.

**G. Decreti e stato** — righe DEC-C/DEC-D: confronto meccanico carattere-per-carattere card §0-bis ↔ `DECISIONI.md` = **IDENTICHE** entrambe; diff di `55dc943` = 2 sole righe aggiunte, zero righe preesistenti toccate (unified diff dal parent). Riga `FASE-CODICE: v1.1 chiusa — commit 774f9d3.` appesa verbatim in `STATO_CORRENTE.md`. Commit dedicato ✓. `source=PORTARA`, `symbol=FIB`, `timeframe=60s` asseriti su TUTTE le righe in T3 (`test_isp_loader.py:115-117`) e presenti nell'output CSV (riscontro diretto sulla prima riga dati). Citazione decoder: `scripts/export_directa_history_parametric.py:797` = `base_tf = f"{fallback_period_seconds}s"` ✓; `:802` = `timeframe=base_tf` ✓; `:885-887` = tre chiamate con `fallback_period_seconds=60` ✓; "1M" compare solo in prosa di docstring (`:25`), mai come valore record — token `60s` univoco, DEC-D soddisfatto; concordanza `AGG_FROM_{base_tf}` (`:817,827`) con CN-9.8 (`SPEC_FUNZ_01.md:1344`) ✓.

**H. Tick-grid** — ricalcolo indipendente del Reviewer sull'intero sample (script autonomo, senza usare `src/data_layer`): off-tick sulle barre valide = **esattamente 3**: `20231213 1038 high 30319`, `20231214 1039 open 30389`, `20231214 1039 high 30389`. Confermati 30319 e 30389; **nessun altro sfuggito**. Settle-row off-tick sui 4 campi (30434), correttamente fuori dai finding delle barre valide. No clamping: `tick_grid_findings` è pura lettura (`isp_loader.py:163-178`); sull'output la barra 30389 è in griglia intatta (riscontro diretto: `2023-12-14 17:39:00, open=30389, high=30389`) e T7 pinna 30319 + set esaustivo + conteggio barre reali invariato.

**I. Igiene** — perimetro commit pulito: `55dc943` 2 file, `adc30d1` 7 file (i soli della card §6), `d701918` 1 file, `101335e` 1 file — nessun estraneo. Lessico: "VERIFICA" compare solo come intestazione dei blocchi canonici RM-1 dell'ESITO e come rimando a quei blocchi nel docstring di T2 — ammesso; nessuna aggiunta della famiglia vietata fuori dai blocchi (grep sulle righe `+` dei 4 commit). Bypass guard: vedi NON VERIFICABILE.

---

### Findings

**R-F1 — [BUG REALE] [severità: alta] Fixture NON committata: GC-3 violata, suite non portabile, claim "committata" falso.**
- *Problema*: `data/samples/portara_isp/ISP2023Z.txt` è **untracked**: `git ls-files` non la elenca, `git log --all -- data/samples/portara_isp/` è vuoto (nessun commit l'ha mai contenuta), non è in `.gitignore` (`git check-ignore` esce 1), compare in `git status --porcelain -uall` come `??`. GC-3 (`tasks/METODO.md:305-309`) esige "fixture COMMITTATE (es. sample ISP ridotto)" e "La suite deve passare su qualunque clone senza dati esterni": su un clone pulito T1 fallisce con FileNotFoundError e l'intera baseline GC-1 è rotta.
- *Aggravante di onestà*: i docstring dichiarano il contrario — `src/data_layer/isp_loader.py:4` "(committata, GC-3)", `tests/data_layer/test_isp_loader.py:4` "Fixture committata (GC-3)", `:20-21` "sul sample committato"; anche `tasks/ACTIVE_TASK.md` ("fixture committata (GC-3)"). Claim non rispondente allo stato del repo.
- *Concausa (attenuante)*: la card v2 §0.3 chiede solo fixture "presente" e l'add-list §6 NON include `data/samples/` — con la regola §6 "staging estraneo → STOP", il Developer non poteva committarla senza deviare dalla card. Conflitto card ↔ GC-3: per precedenza documenti (METODO > card) prevale GC-3. Anche l'ESITO §11 registra le voci untracked come "noise di progetto ... non committate" senza accorgersi che una di esse è la fixture del task.
- *Conseguenza se non risolto*: ogni task-codice successivo eredita una baseline che gira solo su questa macchina; il vincolo GC-1 "intera suite verde" diventa non-attestabile su clone; i claim nei docstring restano falsi agli atti.
- *Rimedio (per il rilancio al Developer, senza ripianificare)*: commit della fixture (e correzione a quel punto veritiera dei docstring); l'estensione dell'add-list della card è formalità del Planner → voce PENDENTE-PLANNER 2.

**R-F2 — [NEUTRO] [severità: minore] Metrica O/C dell'ESITO calcolata con la settle-row inclusa; due conteggi imprecisi.**
- *Problema*: ESITO §3 dichiara "media |O_t − C_(t−1)| = 3.72 vs 10.17 su 997 coppie consecutive [intra-giornata]". I numeri si riproducono **solo** includendo la settle-row (1000 righe − 3 giornate = 997 coppie; riprodotto esatto: 3.72/10.17). Sulle sole barre valide (999, come la narrativa del filtro settle suggerirebbe): 996 coppie, 3.61/10.07. Analogamente "(320 righe regolari)" flat in §4: le regolari sono 319, la 320ª è la settle stessa.
- *Conseguenza/impatto*: nessun impatto sul codice né sulla conclusione (fattore 2.7–2.8x e direzione identici in ogni variante; riscontro indipendente del Reviewer). Difetto di precisione del blocco PROVE: chi rifà il calcolo "sulle barre" ottiene numeri diversi da quelli scritti.

**R-F3 — [NEUTRO] [severità: minore] Fonte DOC-INTERNO citata nei blocchi RM-1 è essa stessa untracked.**
- *Problema*: `Codice/PROMPT_RECUPERO_SAMPLE_ISP.md`, citato come `[DOC-INTERNO]` in ESITO §3/§5 (tz Chicago, penultima colonna = tickCount), è `??` in `git status` — la catena di evidenza poggia su un file non versionato, perdibile.
- *Impatto*: audit trail fragile; stessa radice di R-F1 (materiale del sample mai committato). Da sanare insieme (decisione di perimetro al Planner).

**R-F4 — [RISCHIO PEGGIORAMENTO] [severità: minore] Scarto silenzioso delle barre fuori sessione.**
- *Problema*: `isp_loader.py:211-214` — barra fuori 08:00–22:00 CET → `continue` senza contatore né diagnostica.
- *Stato sul sample*: zero occorrenze, e T5 lo pinna indirettamente (`len(reali)==len(parsed.bars)`, `test_isp_loader.py:162`): oggi nessun fallimento silenzioso.
- *Impatto prospettico*: su tape pieno M0-T2 (print d'asta 07:45–08:00, sedute anomale) barre reali sparirebbero dalla griglia senza traccia. Suggerito (non obbligatorio in M0-T1) un contatore/lista scarti nella diagnostica.

**R-F5 — [NEUTRO] [severità: minore] Politica giornate troncate: comportamento non pinnato da alcun test.**
- *Problema*: nessuna assert copre 1167/262/65 né la regola `[prima reale, ultima reale]` (T4 copre solo la giornata completa, per design della card). Una regressione sulla politica dei giorni parziali non farebbe fallire la suite.
- *Attenuante*: la politica è dichiaratamente provvisoria in attesa di decreto (ESITO §7 "Da riesaminare in M0-T2"); pinnarla ora congelerebbe una decisione non presa. Dati al Planner in PENDENTE-PLANNER 1.

**R-F6 — [NEUTRO] [severità: minore] `assert` come guardia runtime.**
- `isp_loader.py:241` usa `assert prev_close is not None` come invariante: sotto `python -O` sparisce. L'invariante è garantito per costruzione (griglia parte da barra reale), quindi oggi nessun percorso lo attiva; igiene, non bug.

**Deviazioni dalla card (asse A) — classificate, nessuna bloccante:**
- **D1 [NEUTRO]**: appendice ESITO committata a parte (`d701918`) invece che tutto nel commit finale (§6): la card §7 chiede l'hash del commit finale DENTRO l'ESITO — impossibilità logica nel medesimo commit; soluzione dichiarata in ESITO §11-12. Deviazione forzata dalla card stessa.
- **D2 [NEUTRO]**: §0-bis eseguito dall'Orchestratore (`55dc943`), non dal Developer come scritto in card — ordine del Planner, dichiarato nel contesto autoritativo; contenuto controllato verbatim (asse G), esito conforme.
- **D3 [NEUTRO]**: commit `101335e` (DEV_STATUS → READY_FOR_REVIEW) non previsto dalla card ma richiesto dal ciclo di BASE_COMUNE §1; DEV_STATUS era vuoto, nessuna riga preesistente riscritta.

### NON VERIFICABILE (esplicito, RM-1)

1. **History dei comandi shell del Developer** (asse I, bypass guard stile D-14): non ricostruibile dal repo (nessun log dei comandi committato). Dichiarato dall'Orchestratore nel prompt: la separazione `git add` / `git commit` in due chiamate è stata **istruita dall'Orchestratore** per un falso positivo noto del guard sui basename nei comandi combinati; il hook `rm_guard` scatta comunque sul comando `git commit` stesso, dunque la separazione non aggira il controllo RM-1 **per costruzione del hook**. Giudizio d'igiene: prassi accettabile finché il hook resta agganciato a `git commit`; l'esecuzione effettiva resta non ricostruibile.
2. **Semantica fine di `tickCount`** (n. trade vs n. variazioni di prezzo): non discriminabile dal sample — dichiarato apertamente dall'ESITO stesso (§3, ALTERNATIVE NON ESCLUSE); nessun impatto su M0-T1 (colonna propagata as-is).
3. **Esclusione rigida di (C,H,L,O)**: impossibile sul solo sample (nessun dato tick-by-tick); l'esclusione resta statistica (robusta: 2.7–2.8x, 572 vs 112 coppie). L'ESITO la etichetta correttamente come non esclusa a vincolo rigido; riconferma su tape M0-T2.

### PENDENTE-PLANNER (dati raccolti, nessuna decisione presa)

1. **Politica giornate parziali**: regola applicata dal builder = `[max(08:00 CET, prima barra reale), min(21:59 CET, ultima barra reale)]` per giornata. Numeri: 1167 righe totali = 262 (13/12, 17:38–21:59) + 840 (14/12, completa) + 65 (15/12, 08:00–09:04); 999 reali + 168 sintetiche. Alternative sul tavolo (da decretare per M0-T2): (a) griglia sempre 840 righe con NULL/righe assenti pre-prima-barra; (b) regola attuale; (c) scarto delle giornate incomplete. Dopo il decreto, pinnare la politica con test dedicato (chiude R-F5).
2. **Fixture nel repo**: GC-3 impone la fixture committata; la card §6 non la includeva nell'add-list. Serve l'istruzione operativa (estensione add-list o commit dedicato) per `data/samples/portara_isp/ISP2023Z.txt` ed eventualmente `Codice/PROMPT_RECUPERO_SAMPLE_ISP.md` (fonte DOC-INTERNO citata, R-F3). Il fix di R-F1 dipende da questa via operativa, l'obbligo GC-3 no.
3. **Riconferme su tape M0-T2** (già annotate dall'ESITO, riportate qui per il registro): discriminante settle `volume==0` da riconfermare (possibili no-trade row legittime a volume 0); disambiguazione O/C definitiva con roll-log/contract data del vendor.

### Tabella "Classificazione per il supervisore"

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|------------------------|
| 1 | Fixture ISP non committata (GC-3 violata, suite non portabile) + claim "committata" falso nei docstring | `git status -uall`: `?? data/samples/portara_isp/ISP2023Z.txt`; `isp_loader.py:4`; `test_isp_loader.py:4,20-21` | BUG REALE | Sì (obbligatorio) — con istruzione operativa del Planner (PENDENTE-PLANNER 2) |
| 2 | Metrica O/C dell'ESITO calcolata con settle-row inclusa (997/3.72/10.17); "(320 righe regolari)" = 319+settle | `ESITO_M0-T1.md:36-42,78` | NEUTRO | No (salvo decisione supervisore) |
| 3 | Fonte DOC-INTERNO dei blocchi RM-1 non versionata | `ESITO_M0-T1.md:50,101`; `?? Codice/PROMPT_RECUPERO_SAMPLE_ISP.md` | NEUTRO | No (accorpabile al fix #1 se il supervisore approva) |
| 4 | Scarto silenzioso barre fuori sessione (nessun contatore) | `isp_loader.py:211-214` | RISCHIO PEGGIORAMENTO | Decisione supervisore (proposta: rinvio a M0-T2) |
| 5 | Politica giorni parziali non pinnata da test (in attesa di decreto) | `isp_loader.py:222-226`; T4 `test_isp_loader.py:123` | NEUTRO | No (dopo decreto Planner) |
| 6 | `assert` come guardia runtime (sparisce con `-O`) | `isp_loader.py:241` | NEUTRO | No |

### Applicazione RM-1 a me stesso (BASE_COMUNE §8)

- "8/8 due volte": output pytest dei miei due run (asse B). — "T6 byte-identico": sha256 `1267cb3a…` uguale su due processi separati, hash riportato.
- "Fixture untracked": tre prove indipendenti (`git ls-files` vuoto sul path; `git log --all --` vuoto; `git status --porcelain -uall` = `??`). Alternative escluse: copia committata altrove (`git ls-files | grep -i isp` → solo i 2 sorgenti); path ignorato da gitignore (`git check-ignore` exit 1).
- "997 coppie = settle inclusa": riprodotto esattamente 997/3.72/10.17 col calcolo settle-inclusa; alternative provate ed escluse: intra-day su barre valide (996/3.61/10.07), tutte le coppie (998/3.77/10.25).
- "Off-tick = 3": ricalcolo con script autonomo che non importa `src/data_layer` (indipendenza dal codice sotto audit).
- "DST-safe": 4 conversioni dirette su `_to_cet` in finestre con offset diversi (+7 dic, +7 lug, +6 metà marzo, +8 non applicabile/finestra autunno — gli offset seguono il tz-database, nessun offset fisso possibile che li spieghi tutti).
- Non escluso da me: tutto quanto elencato in NON VERIFICABILE.

### VERDETTO: CONDITIONAL

Il comportamento del codice corrisponde ai requisiti citati (R-9.3/R-9.14/CN-9.5/9.7/9.9, DEC-C/D): 8/8 test non vacui, riprodotti due volte, T6 byte-identico con hash del Reviewer, decreti verbatim, off-tick e tz riscontrati in modo indipendente. Ma la fixture su cui l'intera suite poggia NON è committata (GC-3 violata, baseline GC-1 non portabile) e i docstring dichiarano il contrario: un BUG REALE in tabella esclude il PASS (BASE_COMUNE §4). Fix circoscritto: commit della fixture + rettifica docstring, su istruzione operativa del Planner (PENDENTE-PLANNER 2).
