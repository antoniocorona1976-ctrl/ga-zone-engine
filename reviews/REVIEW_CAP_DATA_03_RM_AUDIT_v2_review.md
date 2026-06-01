# AUDIT-RM CAP-DATA-03 — Re-Review v2 — esito del fix del finding NEUTRO #1

**Sede**: CLI locale (Windows). **Iterazione**: v2 (re-review focalizzata dopo fix chirurgico di 1 riga).
**Perimetro di questa v2**: il solo fix del finding #1 (NEUTRO) emesso dall'AUDIT-RM v1 (`reviews/REVIEW_CAP_DATA_03_RM_AUDIT_review.md`, commit `33d35b9`, verdetto **PASS**) + verifica di non-regressione sul perimetro A-D. NON ri-audita da zero il perimetro A-D (già PASS v1 `33d35b9`; Parte 10 già PASS v1 `ab80d96` + v2 `48171e4`).
**Conferma lettura regole**: lette come prime azioni `tasks/METODO.md` (RM-1 verifica vs assunzione + blocco 4-righe `:28-33`; RM-2 grep nel repo prima di assumere format esterno; RM-3 doc esterna non è fonte di verità + etichette livello; RM-4 output non-CAP) e `.claude/agents/reviewer.md` (ruolo ostile per default, 4 check probe-review, divieti di sede CLI, formato output, regole di verdetto).
**Vincolo di sede rispettato**: NON ho eseguito alcun probe DAPI né aperto socket. Empirico CHIUSO. Verifica via lettura dei file committati (Read) + grep + git diff. I numeri canonici (49 match / 13 mismatch su 62, 7 FIB6F, ≤6 tick, cash low 6/6 DITAS) sono usati come pietre di paragone autoritative (inputs #9..#11 del task card), NON ri-misurati.

---

## Verdetto: **PASS**

Finding NEUTRO #1 **CHIUSO** correttamente: "OHLCV coincidenti" rimosso (grep su `CAP_10_parte_10.md` → 0 occorrenze); la nuova dicitura "range high-low coincidente e nessuno swap O/C (…)" è **accurata** contro i fatti chiusi §2.4.5(A)/(B) e **non indebolisce** l'esclusione di path-inference/distorsione (anzi la rafforza, enumerando entrambe le classi di residuo). **Zero regressioni**: il diff `33d35b9..HEAD` su A è di **1 sola riga** (r.105), tutto il resto del blocco RM-1 e del capitolo è byte-identico; D non toccato. Nessun nuovo finding bloccante. Regola di decisione applicata: PASS se finding #1 chiuso bene e 0 regressioni / 0 nuovi bloccanti.

---

## Iterazione 2 — esito del finding NEUTRO #1: **CHIUSO**

### 1. "OHLCV coincidenti" rimosso

- **Evidenza**: `Grep "OHLCV coincident"` su `docs/methodology_v2/CAP_10_parte_10.md` → **0 match** (No matches found). La frase incriminata non esiste più nel capitolo.
- **Conferma incrociata via git diff** (`git diff 33d35b9 HEAD -- docs/methodology_v2/CAP_10_parte_10.md`): la riga `-` (rimossa) conteneva esattamente "…(morning + afternoon) **con OHLCV coincidenti**; swap O/C — …"; la riga `+` (aggiunta) la sostituisce. Sostituzione confermata.

### 2. La nuova dicitura a r.105 è accurata

Testo nuovo (verbatim `CAP_10_parte_10.md:105`):
> "ALTERNATIVE COMPATIBILI ESCLUSE: path-inference o distorsione di volatilita' nella ricostruzione CANDLERANGE — escluso dall'equivalenza su 2 finestre indipendenti (morning + afternoon) **con range high-low coincidente e nessuno swap O/C (i residui open/close di confine minuto, $\leq 6$ tick, e il low del cash rado sono enumerati nella riga PROVE e in ALTERNATIVE COMPATIBILI NON ESCLUSE, e non sono distorsioni di path-inference)**; swap O/C — escluso dal test discriminante local_O==hist_C che NON si verifica su nessuno dei 7 FIB6F (§2.4.5); …"

Verifica claim-per-claim contro i fatti chiusi (PROBE_RECUPERO_GAP_DAPI §2.4.5, autoritativo):

| Claim nella nuova frase | Fatto chiuso di riscontro | file:linea | Esito |
|---|---|---|---|
| "range high-low coincidente" (sui FIB6F) | "**`high` coincide su tutti i 7; `low` coincide su tutti i FIB6F.**" | `PROBE_RECUPERO_GAP_DAPI.md:134` (§2.4.5 B) | **ACCURATO** — high e low coincidono su tutti i 7 FIB6F → range H-L esatto |
| "nessuno swap O/C" | "NESSUNO swap O/C … se ci fosse inversione sarebbe `local_O == hist_C`, che NON accade su nessuno dei 7" | `PROBE_RECUPERO_GAP_DAPI.md:135` (§2.4.5 B) + §2.4.6 `:143` | **ACCURATO** — test discriminante mai verificato |
| "residui open/close di confine minuto, ≤6 tick" | "Scarto su **open (o close) al confine del minuto** di 1–6 tick (es. dO +5 / +30 …)" | `PROBE_RECUPERO_GAP_DAPI.md:134` (§2.4.5 B) | **ACCURATO** — max dO +30 = 6 tick (FIB tick 5pt); "≤6 tick" è il limite superiore corretto |
| "il low del cash rado" come residuo enumerato (non path-inference) | DITAS cash: "diverge **solo il `low`** … mentre **O / H / C coincidono esatti** … Non è schema: è incompletezza del feed cash sul low" | `PROBE_RECUPERO_GAP_DAPI.md:132` (§2.4.5 A) | **ACCURATO** — eccezione cash low correttamente isolata come feed-sparsity, non distorsione |
| "enumerati nella riga PROVE" | PROVE r.104: "49 match / 13 mismatch su 62 … mismatch tutti spiegati (primo minuto SUB-troncato + scarto 1 tick confine minuto + feed cash rado sul low)" | `CAP_10_parte_10.md:104` | **ACCURATO** — back-reference verificata |
| "enumerati … in ALTERNATIVE COMPATIBILI NON ESCLUSE" | NON ESCLUSE r.106 punto (1): "il low del cash rado e' un'eccezione documentata … (6/6 mismatch DITAS sul solo low, §2.4.5 lettera A)" | `CAP_10_parte_10.md:106` | **ACCURATO** — back-reference verificata |

**La nuova frase NON indebolisce l'esclusione di path-inference/distorsione.** La claim effettivamente esclusa (path-inference / distorsione di volatilità) resta esclusa, e ora con motivazione più forte: il **range H-L** (ciò che alimenta le feature di volatilità EGARCH) è esatto sui FIB6F, e le due sole classi di residuo (open/close di confine minuto + low cash rado) sono nominate esplicitamente come artefatti non-distorsivi. È un rafforzamento sostanziale rispetto al precedente "OHLCV coincidenti", che era assoluto e in tensione con i 13 mismatch dichiarati nella stessa riga PROVE.

**La nuova frase NON introduce affermazioni false.** Unica tensione residua possibile (esaminata in modo ostile): "range high-low coincidente" è una claim positiva, ma sul **cash DITAS** il low NON coincide (6/6 mismatch). La tensione è però **disinnescata nello stesso periodo**: "il low del cash rado" è enumerato come residuo immediatamente dopo, dentro la stessa parentesi, ed è etichettato come non-distorsione. La claim positiva è quindi qualificata in-clause e si riferisce sostanzialmente al FIB6F future (lo strumento che produce i segnali); nessun fatto falso sopravvive alla lettura completa della riga. Vedi §"Nuovi finding".

---

## Nessuna regressione — esito git diff `33d35b9..HEAD`

- **`git diff --numstat 33d35b9 HEAD -- docs/methodology_v2/CAP_10_parte_10.md`** → `1  1` (1 inserzione, 1 cancellazione). **Una sola riga modificata** (r.105). Confermato leggendo il diff testuale: VERIFICA (r.103), PROVE (r.104), le clausole "swap O/C" e "rewriting/adjustment" della stessa r.105, e NON ESCLUSE (r.106) sono **invariate** (non compaiono come righe `-`/`+` nel diff, eccetto la r.105 che è l'unica toccata e nella quale le clausole swap O/C e rewriting sono preservate verbatim).
- **D non toccato**: `git diff --stat 33d35b9 HEAD -- scripts/export_directa_history_parametric.py` → **vuoto**. Il decoder canonico (fonte di verità level-2) non è stato modificato (vincolo assoluto rispettato).
- **AC / decisioni / numeri invariati**: il diff su A non tocca alcun AC, alcuna decisione D-10-*, alcun numero. I numeri della riga PROVE (49/13/62, 7 FIB6F) sono byte-identici.
- **Altri file del range** (`git diff --stat 33d35b9 HEAD`): `REPORT_CAP_10.md` (+17/-0, **additivo puro** — solo la nuova sezione "Iterazione audit RM — fix finding NEUTRO #1", nessun contenuto preesistente alterato); `tasks/ACTIVE_TASK.md` (+16, sezione "Finding di Review da risolvere" aggiunta dall'Orchestratore); `tasks/DEV_STATUS.md` (+1, `READY_FOR_REVIEW`). Tutti coerenti col fix; nessun file fuori scope.
- **REPORT veritiero**: la sezione "Iterazione audit RM — fix finding NEUTRO #1" (`REPORT_CAP_10.md:217-230`) descrive correttamente prima→dopo (frammento "con OHLCV coincidenti" → "con range high-low coincidente e nessuno swap O/C (…)"), dichiara scope rigido (SOLO quel frammento), impatto nullo, Parte 10 resta PASS. Coerente con il diff reale.

**Conclusione**: il cambiamento è **solo** quella riga + la nota additiva nel REPORT. Zero regressioni sul perimetro A-D.

---

## Secondo giro — il fix ha introdotto nuove imprecisioni/incoerenze?

Esaminate due possibili imperfezioni introdotte dalla nuova formulazione; nessuna è bloccante.

- **(i) "range high-low coincidente" è troppo forte sul cash?** Sul DITAS cash il low NON coincide (6/6 mismatch). Ma la stessa parentesi enumera "il low del cash rado" come residuo non-distorsivo, qualificando la claim in-clause. La sostanza (range H-L esatto sul FIB6F future, che alimenta le feature di volatilità) è corretta; l'eccezione cash è disclosed nello stesso periodo e in NON ESCLUSE. **Classificazione: NEUTRO** (impatto GA nullo; nessun fatto falso sopravvive alla lettura completa; più accurato del testo v1). Coerente con la classificazione NEUTRO già data dall'audit v1 a questa stessa categoria di phrasing.
- **(ii) Ridondanza "nessuno swap O/C" + clausola "swap O/C — escluso dal test …".** La frase ora contiene "nessuno swap O/C" nella parte iniziale e, subito dopo, la clausola dedicata "swap O/C — escluso dal test discriminante local_O==hist_C …". È una **ridondanza** (back-reference), non una contraddizione: entrambe affermano lo stesso fatto, supportato da §2.4.5. Nessun impatto su correttezza/GA. **Classificazione: NEUTRO** (cosmesi; non riportabile come finding bloccante né da mandare a Development).
- **Riferimento a "PROVE e ALTERNATIVE COMPATIBILI NON ESCLUSE" corretto?** Sì: la riga PROVE (r.104) elenca i 13 mismatch e le loro cause; la riga NON ESCLUSE (r.106) punto (1) elenca il low del cash. Il back-reference è accurato (verificato sopra). Nessuna imprecisione.

Nessuna delle due imperfezioni raggiunge la soglia di BUG REALE / MIGLIORA PERFORMANCE / RISCHIO PEGGIORAMENTO. Sono entrambe NEUTRO e **non si mandano a Development** (cosmesi/back-reference; la sostanza è corretta e disclosed).

---

## Verdetto complessivo dell'AUDIT-RM perimetro A-D

Con il finding #1 chiuso e zero regressioni, l'audit del perimetro A-D **resta PASS**. La conformità RM-1/2/3 del perimetro A-D, già accertata in v1 (`33d35b9`), è preservata: il fix è una correzione di precisione di 1 riga che rende il blocco RM-1 di Cap.59 internamente ancora più riconciliato (la riga ESCLUSE ora è coerente con i 13 mismatch della riga PROVE). Nessun nuovo BUG REALE, nessun residuo aperto. La lista "Empirico-CLI da verificare" resta **VUOTA** (l'empirico è chiuso; il fix non introduce alcuna asserzione empirica nuova che ecceda il perimetro chiuso).

---

## Lista "Empirico-CLI da verificare"

**VUOTA**. Il fix è puramente testuale e si appoggia a fatti empirici già chiusi e autoritativi (§2.4.5 A/B, inputs #9..#11). Nessuna asserzione del fix richiede una prova DAPI live non già acquisita.

---

## Tabella classificazione per il supervisore

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|------------------------|
| — | Nessun nuovo finding bloccante. Il finding NEUTRO #1 è CHIUSO. Le 2 imperfezioni residue del secondo giro (claim "range high-low coincidente" qualificata in-clause sul cash; ridondanza "nessuno swap O/C") sono NEUTRO/cosmesi, internamente disclosed, impatto GA nullo. | `CAP_10_parte_10.md:105` | **NEUTRO** | NO — il fix chiude il finding; le imperfezioni residue sono cosmesi/back-reference, la sostanza è corretta e le eccezioni sono già disclosed nello stesso blocco |

Nessun finding **BUG REALE**, **MIGLIORA PERFORMANCE** o **RISCHIO PEGGIORAMENTO**. Verdetto PASS perché il finding #1 è chiuso bene e non c'è alcuna regressione né alcun nuovo bloccante.

---

## Applicazione RM-1 a me stesso (Reviewer)

- **VERIFICA**: "'OHLCV coincidenti' rimosso da CAP_10". **PROVE**: `Grep "OHLCV coincident"` su `CAP_10_parte_10.md` → 0 match; confermato dal lato `-` del `git diff 33d35b9 HEAD` sul file. **ALTERNATIVE COMPATIBILI ESCLUSE**: che la frase sia stata spostata altrove nel file — esclusa perché il grep su tutto il file dà 0 occorrenze; che il grep abbia mancato una variante di accento/spazio — mitigata dal pattern senza accenti/finali ("OHLCV coincident") che cattura sia "coincidenti" sia eventuali flessioni. **ALTERNATIVE COMPATIBILI NON ESCLUSE**: nessuna rilevante (0 match è risultato netto).

- **VERIFICA**: "la nuova dicitura r.105 è accurata contro §2.4.5". **PROVE**: lettura diretta (Read) di `PROBE_RECUPERO_GAP_DAPI.md:130-143` (§2.4.5 A/B + §2.4.6) e confronto claim-per-claim con la r.105 letta verbatim (tabella sopra). **ALTERNATIVE COMPATIBILI ESCLUSE**: che "range high-low coincidente" nasconda una distorsione di volatilità — esclusa perché §2.4.5(B):134 dichiara esplicitamente high coincide su tutti i 7 e low coincide su tutti i FIB6F (range esatto); che "nessuno swap O/C" sia non supportato — esclusa dal test `local_O==hist_C` mai verificato (§2.4.5 B:135). **ALTERNATIVE COMPATIBILI NON ESCLUSE**: che "range high-low coincidente", letto isolato dalla parentesi, sia in tensione col cash low DITAS — **non esclusa** ma disinnescata: la parentesi nomina il low del cash come residuo nello stesso periodo; l'ho classificata NEUTRO (non BUG) perché nessun fatto falso sopravvive alla lettura completa della riga e perché la categoria è la stessa già classificata NEUTRO in v1.

- **VERIFICA**: "zero regressioni / 1 sola riga cambiata su A / D non toccato". **PROVE**: `git diff --numstat 33d35b9 HEAD -- CAP_10` → `1 1`; `git diff --stat 33d35b9 HEAD -- scripts/export_directa_history_parametric.py` → vuoto; `git diff --stat 33d35b9 HEAD` → solo CAP_10 (1) + REPORT (+17/-0 additivo) + ACTIVE_TASK (+16) + DEV_STATUS (+1). **ALTERNATIVE COMPATIBILI ESCLUSE**: che il REPORT abbia alterato contenuto preesistente — esclusa dal numstat `17 0` (0 cancellazioni → solo aggiunte); che un altro blocco RM-1 sia stato toccato — esclusa dal numstat `1 1` su A (una sola riga). **ALTERNATIVE COMPATIBILI NON ESCLUSE**: non ho ri-letto integralmente A v2 in questa sessione (re-review focalizzata sul fix, come da natura del task); mitigato dal fatto che il diff prova meccanicamente che A è cambiato in 1 sola riga rispetto allo stato già auditato PASS in `33d35b9`.

- **VERIFICA**: "nessun nuovo finding bloccante dal secondo giro". **PROVE**: esaminate 2 imperfezioni (claim cash, ridondanza), entrambe NEUTRO/cosmesi con disclosure in-clause. **ALTERNATIVE COMPATIBILI ESCLUSE**: che la ridondanza "nessuno swap O/C" sia una contraddizione — esclusa perché le due occorrenze affermano lo stesso fatto (back-reference), supportato da §2.4.5. **ALTERNATIVE COMPATIBILI NON ESCLUSE**: che esistano imprecisioni in porzioni di A/B/C non rilette in questa v2 focalizzata — fuori perimetro di questa re-review (il perimetro A-D è già PASS in `33d35b9`; questa v2 audita il solo fix + non-regressione).

---
**PASS**: finding NEUTRO #1 CHIUSO ("OHLCV coincidenti" rimosso, grep 0 match); nuova dicitura r.105 accurata contro §2.4.5(A)/(B) (range H-L coincidente sui FIB6F, nessuno swap O/C, low cash enumerato come residuo non-distorsivo); esclusione di path-inference/distorsione preservata e rafforzata; zero regressioni (diff `33d35b9..HEAD` su A = 1 riga, D non toccato, REPORT additivo). 2 imperfezioni residue NEUTRO/cosmesi, internamente disclosed, non da mandare a Development. L'audit del perimetro A-D resta PASS.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
