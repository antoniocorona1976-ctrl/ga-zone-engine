# Review CAP-10 v2 — Parte 10 Continuità tape, recupero gap, riconciliazione canonica, storicizzazione strutturata

**Sede**: CLI locale (Windows). **Modalità**: CAP-review PIENA, **iterazione v2** (re-review ostile sulla versione corretta dopo rework cosmetico). **Data**: 2026-06-01.
**Conferma lettura regole**: letti come prime azioni `tasks/METODO.md` (RM-1..RM-4) e `.claude/agents/reviewer.md` (ruolo, check, formato, regole di verdetto). Letta inoltre la review v1 `reviews/REVIEW_CAP_10_review.md` (PASS, 4 finding NEUTRO: NB-1 + OM-1/2/3) e la sezione "Iterazione 2 — risposta ai finding di Review" del `REPORT_CAP_10.md` (r.179+).

**Vincolo di sede rispettato**: NON ho ri-eseguito V-1/V-2/T+1 né lanciato DAPI (fatti empirici chiusi e autoritativi, fuori perimetro di una v2 cosmetica). Ho verificato le citazioni cross-CAP **leggendo i file committati** (sola lettura). La verifica critica della citazione `CAP_06_parte_VI.md:276` è stata fatta aprendo il file referente.

---

## Verdetto: **PASS**

I 4 finding NEUTRO della v1 sono **tutti chiusi correttamente**. Il fix NB-1 — che era la trappola (rischio di sostituire un errore di citazione con un altro) — è **accurato**: la citazione `CAP_06_parte_VI.md:276` è esatta verbatim e il meccanismo di Cap.30 è effettivamente non-bloccante. Il rework è chirurgico (CAP +7/-5 righe, confinato alle 4 aree), non introduce regressioni, non altera i 43 AC, non aggiunge asserzioni "verificato" in prosa libera né nuove citazioni cross-CAP non verificate (oltre `:276`, che è verificata). Il secondo giro ostile non ha prodotto nuovi finding bloccanti. Nessun problema bloccante → PASS.

---

## Iterazione 2 — esito dei 4 finding

### NB-1 — analogia "gate Brier $f_5^{live}$ Parte VI Cap.30" → **CHIUSO**

**Esito**: CHIUSO e accurato. Evidenza:

- **"Brier" sparito dal contesto normativo.** Grep `Brier` su `CAP_10_parte_10.md` e `00_indice.md` → **0 match**. Le uniche occorrenze di "Brier" sono in `REPORT_CAP_10.md` r.183-213, **tutte dentro il changelog "Iterazione 2"** che documenta il prima/dopo — ammesso esplicitamente dal task card. Conforme.
- **Le 4 occorrenze + 2 propagazioni riformulate** (verificato con `git diff 95f2219..3eba20f` + Read del file v2):
  - `CAP_10_parte_10.md:42` (Conversione signal-to-trade): "Direttamente analogo al gate Brier $f_5^{live}$…" → "gate operativo **bloccante** … A differenza del monitoraggio **non bloccante** di Parte VI Cap.30 (… non chiude il loop, `[DOC-INTERNO …CAP_06_parte_VI.md:276]` 'L'alert non chiude il loop di re-training'), il gate di Cap.60 **interviene sull'operatività**…". ✓
  - `CAP_10_parte_10.md:126` (Cap.60 step 6, ramo `RECONCILE_DIVERGENT_*`): "(gate operativo, analogo al gate Brier…)" → "(gate operativo bloccante, a differenza del monitoraggio non bloccante di Parte VI Cap.30 che emette alert ma non chiude il loop, `[DOC-INTERNO …CAP_06_parte_VI.md:276]`)". ✓
  - `CAP_10_parte_10.md:250` (Cap.65 D-10-3 motivazione): "analogo al gate Brier $f_5^{live}$…" → "gate **bloccante** sull'emissione $d+1$, a differenza del monitoraggio non bloccante di Parte VI Cap.30 (`CAP_06_parte_VI.md:276`)". ✓
  - **Propagazione indice** `00_indice.md:99`: "(analogo gate Brier $f_5^{live}$ Parte VI Cap.30)" → "(a differenza del monitoraggio non bloccante di Parte VI Cap.30)"; "effetto sulla sessione $d+1$" → "effetto **bloccante** sulla sessione $d+1$". ✓
  - **Propagazione report** `REPORT_CAP_10.md` (Ipotesi di partenza + tabella Misura prima/dopo + riga AC-60-2): "Brier" sostituito dal contrasto accurato con Cap.30. ✓

- **VERIFICA CRITICA — la citazione `:276` è accurata (NON ha introdotto un nuovo errore).** Ho aperto `CAP_06_parte_VI.md` e letto la riga 276 direttamente. Dice **verbatim**: *"**L'alert non chiude il loop di re-training**: la decisione di ritraining del GA in risposta a deriva persistente è materia di Parte VII Cap.36 (gate decisionali post-go-live), non di Cap.30."* La citazione nel capitolo è letterale ed esatta.
  - **Cap.30 è effettivamente non-bloccante** (letto integralmente `:260-304`): §30.2 "**Regola di alert**" (r.271, emette alert su deriva fuori IQR); r.276 "L'alert non chiude il loop"; §30.3 `f_5^{live}` r.280 è definita come **"stabilità cross-regime live"** con formula $|f_1^{calmo}-f_1^{turbolento}|/\max(\ldots)$ — **NON un Brier score**; §30.3bis r.297/r.303 le metriche di lifecycle "**non producono alert**" / "**senza soglie di alert**". L'intero Cap.30 è monitoraggio/dashboard/reporting: non blocca mai l'emissione. La nuova formulazione del capitolo ("a differenza del monitoraggio **non bloccante** di Parte VI Cap.30") è quindi **strutturalmente corretta su entrambi i punti** sollevati dalla v1 (non-Brier + non-gate). Il fix non sostituisce un errore con un altro.

### OM-1 — notazione "49/13 match" ambigua (Cap.59 RM-1) → **CHIUSO**

**Esito**: CHIUSO. `CAP_10_parte_10.md:104` (riga PROVE del blocco RM-1) ora: "(49 match / 13 mismatch su 62 minuti, finestra 14:55-15:25)". Notazione disambiguata. Cross-consistenza con Cap.60 r.122 ("5/60 e 13/62 mismatch"): allineata sui medesimi numeri canonici (49 match = 13 mismatch su 62). Il dato numerico è invariato.
- **Il resto del blocco RM-1 di Cap.59 è intatto.** Verificato col diff: l'unica riga modificata dentro il blocco è la riga PROVE (sola notazione); `VERIFICA`, `ALTERNATIVE COMPATIBILI ESCLUSE`, `ALTERNATIVE COMPATIBILI NON ESCLUSE` sono byte-identiche tra v1 e v2. Il formato 4-righe è preservato. Conforme alla restrizione del task ("non toccare il blocco RM-1 oltre la notazione").

### OM-2 — "tutti definiti in Cap.65" falso per 3 sotto-marker → **CHIUSO**

**Esito**: CHIUSO con l'opzione "ammorbidisci + nota". `CAP_10_parte_10.md:62` ora distingue: "i marker principali (Cap.59 `BACKFILL_FROM_CANDLERANGE`, Cap.61 `BOOTSTRAP_COMPLETE`, Cap.60 `RECONCILE_*`) sono **consolidati nella tabella decisioni di Cap.65**, mentre i sotto-marker operativi (`RUNTIME_GAP_BEYOND_100D` del cut-off Cap.59, `BACKFILL_VERIFIED_T3`/`BACKFILL_UNVERIFIED` di Cap.59 step 4, `RECONCILE_SCHEMA_FAIL` di Cap.60 step 3) sono **definiti in-body nei rispettivi capitoli**". L'affermazione è ora vera. Verifica incrociata: i 3 sotto-marker citati come "in-body" effettivamente compaiono in-body (`RUNTIME_GAP_BEYOND_100D` Cap.59 r.98; `BACKFILL_VERIFIED_T3`/`BACKFILL_UNVERIFIED` Cap.59 r.90; `RECONCILE_SCHEMA_FAIL` Cap.60 r.121) e NON sono righe della tabella Cap.65 (verificato leggendo Cap.65 r.246-257, che tabula solo D-10-1..D-10-10). La tabella Cap.65 NON è stata modificata (corretto: l'opzione scelta era ammorbidire il testo, non aggiungere righe).

### OM-3 — disallineamento nome-marker `RECONCILE_*` vs enum manifest → **CHIUSO**

**Esito**: CHIUSO con nota di corrispondenza esplicita. Aggiunto in `CAP_10_parte_10.md:192` (Cap.62, subito dopo la definizione dell'enum manifest) il paragrafo "**Corrispondenza marker audit log <-> enum manifest**": "il valore `reconcile_status = X` del manifest corrisponde 1:1 al marker `RECONCILE_X` dell'audit log (es. `reconcile_status = OK` <-> `RECONCILE_OK`; `DIVERGENT_FIB` <-> `RECONCILE_DIVERGENT_FIB`; `DIVERGENT_HIGHLOW` <-> `RECONCILE_DIVERGENT_HIGHLOW`; `DEGRADED` <-> `RECONCILE_DEGRADED`). Il manifest omette il prefisso `RECONCILE_` per concisione, ma l'insieme dei valori e la semantica sono identici." La mappatura 1:1 copre tutti e 4 i valori dell'enum manifest (`:188`) verso i marker di Cap.60 step 6 (`:126`-`:127`). Allineamento corretto e completo.

---

## Regressioni — verifica (CRITICO per una v2 cosmetica)

**Nessuna regressione.**

- **Diff chirurgico.** `git diff 95f2219..3eba20f -- CAP_10_parte_10.md` = **7 insertions / 5 deletions**, confinate esattamente alle 4 aree dei finding (r.42, r.62, r.104, r.126, r.250 + nuovo paragrafo dopo r.190). Nessuna modifica fuori dai 4 finding. (Il "+51/-10" del task card è l'aggregato CAP+REPORT+indice; il CAP-only è +7/-5, coerente.) La propagazione indice è 2 righe (header v1→v2 + riga Cap.60); la propagazione report è il changelog Iterazione 2.
- **43 AC reggono.** Le modifiche sono di sola accuratezza testuale. Campioni controllati:
  - **AC-60-2** (gate operativo): la sostanza è invariata — il gate di Cap.60 resta definito autonomamente (blocco $d+1$ su `RECONCILE_DIVERGENT_*`, congiunzione dei 3 check r.124, non-mutatività r.146). La modifica NB-1 tocca solo l'**analogia descrittiva** con Cap.30, non la definizione del gate. Anzi, la qualificazione "bloccante" rende il gate **più** preciso (prima il termine "gate operativo" era nudo; ora è "gate operativo bloccante"). Nessuna perdita.
  - **AC-59-4** (blocco RM-1 4-righe): formato 4-righe intatto, solo la notazione PROVE disambiguata (vedi OM-1). I 4 blocchi RM-1 del capitolo (Cap.59 cut-off r.79-82, Cap.59 equivalenza/immutabilità r.103-106, Cap.60 cash low/high r.135-139, Cap.61 daily r.168-171) sono tutti nel formato esatto `VERIFICA / PROVE / ALTERNATIVE COMPATIBILI ESCLUSE / ALTERNATIVE COMPATIBILI NON ESCLUSE`. Nessuno alterato oltre la notazione OM-1.
  - **Scope e decisioni D-10-*** invariati: la tabella Cap.65 (D-10-1..D-10-10) è modificata solo nella **motivazione** di D-10-3 (rimozione "Brier", aggiunta contrasto Cap.30); le 9 altre decisioni e tutti i criteri di rollback (r.259-267) sono byte-identici. Nessuna decisione aperta/chiusa/rinumerata.
- **Nessuna nuova asserzione "verificato" in prosa libera.** Grep sulle righe aggiunte (`+`) del diff per `verificat|confermat|dimostrat|provato|accertat|stabilito` → **0 match**. Il rework non ha introdotto claim di verifica fuori dai blocchi RM-1.
- **Nessuna nuova citazione cross-CAP non verificata.** L'unica citazione cross-CAP introdotta è `CAP_06_parte_VI.md:276` (3 istanze: r.42, r.126, r.250), verificata verbatim. Nessun'altra nuova ancora a file:riga aggiunta dal diff.

---

## Secondo giro ostile — nuovi problemi

**Nessun nuovo finding bloccante né non bloccante.**

Ho ripercorso il perimetro completo del capitolo v2 (non solo le 4 aree del fix) con la domanda "qualcosa di nuovo sfuggito al primo giro, a impatto reale su GA/ranking/fitness/conversione/correttezza/conformità RM?". Esito:
- I check strutturali della v1 (no residui multi-indice, no leakage temporale, no riapertura D-8-*/D-9-*, marker complementari, replay non-mutativo, formalizzazione 840-barre/E5) **reggono invariati** nella v2 (le 4 modifiche non li toccano).
- Le citazioni `[CODICE-ESISTENTE]` (decoder `export_..._parametric.py`, `probe_dapi.py`) e i numeri `[PROVA-EMPIRICA]` (V-1/V-2/T+1/W2) sono **invariati dal diff** → restano coperti dalla verifica indipendente già fatta in v1, non re-impattati.
- La qualificazione "bloccante"/"non bloccante" introdotta da NB-1 **migliora** la precisione del testo senza creare attriti con altre sezioni (Cap.60 r.146 "procedura non-mutativa", Cap.61 r.163 stato `RUNTIME_STALE_RESTART` bloccante per costruzione: tutto coerente con un gate che blocca l'emissione $d+1$).

---

## Citazioni problematiche dal testo

Nessuna. La citazione che in v1 era problematica ("gate Brier $f_5^{live}$") è stata rimossa e sostituita con un riferimento verificato (`CAP_06_parte_VI.md:276`, esatto).

---

## Classificazione per il supervisore

| # | Problema | Classificazione | Mandare a Development? |
|---|----------|-----------------|------------------------|
| — | *(nessun nuovo finding)* | — | — |

Nessun nuovo finding di alcuna classe (BUG REALE / MIGLIORA PERFORMANCE / NEUTRO / RISCHIO PEGGIORAMENTO). I 4 finding NEUTRO della v1 sono chiusi. Verdetto PASS.

---

## Applicazione RM-1 a me stesso (Reviewer)

- **"Citazione `CAP_06_parte_VI.md:276` esatta"**: ho aperto il file e letto la riga 276 direttamente (Read `CAP_06_parte_VI.md` offset 260, riga 276 nel range). PROVE: il testo della riga 276 è "L'alert non chiude il loop di re-training: …" — corrisponde verbatim alla stringa citata nel capitolo. ALTERNATIVE ESCLUSE: che il fix citasse una riga adiacente o sbagliata (controllato il numero di riga esatto nel cat -n); che `f_5^{live}` fosse davvero un Brier (letto §30.3 r.280: è stabilità cross-regime, formula esplicita, nessun Brier); che Cap.30 fosse in realtà bloccante (letto §30.2/§30.3/§30.3bis r.271-303: solo alert/dashboard/reporting, nessun blocco emissione). ALTERNATIVE NON ESCLUSE: non ho riletto integralmente Parte VII Cap.36 (dove la decisione di ritraining è rinviata) — ma è irrilevante al fix, che afferma solo che Cap.30 **non** chiude il loop, fatto verificato a r.276.
- **"Diff chirurgico +7/-5, confinato ai 4 finding"**: ho eseguito `git diff 95f2219 3eba20f -- CAP_10_parte_10.md` e ispezionato ogni hunk. PROVE: 4 hunk, ognuno su una delle aree dei finding (più il paragrafo OM-3). ALTERNATIVE ESCLUSE: modifiche fuori dai finding (nessun altro hunk nel diff); alterazione dei blocchi RM-1 oltre la notazione (le righe ESCLUSE/NON ESCLUSE non compaiono come modificate nel diff). NON ESCLUSE: non ho confrontato byte-per-byte le ~268 righe integrali fuori dal diff, ma git diff è autoritativo sulle differenze.
- **"43 AC reggono"**: ho confrontato la sostanza delle aree toccate con i criteri AC pertinenti (AC-60-2, AC-59-4), non ho ri-verificato ex-novo tutti i 43 AC (già fatti in v1 e non re-impattati da un diff +7/-5 di sola accuratezza). "Reggono" = le modifiche non toccano alcun elemento su cui un AC poggiava; il contenuto normativo è invariato.

---
PASS: nessun problema bloccante. I 4 finding NEUTRO della v1 sono chiusi correttamente; il fix NB-1 — la trappola — è accurato (citazione `CAP_06_parte_VI.md:276` verificata verbatim, Cap.30 confermato non-bloccante, `f_5^{live}` confermata non-Brier). Rework chirurgico (+7/-5 sul CAP), nessuna regressione sui 43 AC, nessuna nuova asserzione "verificato" in prosa libera, nessuna nuova citazione cross-CAP non verificata. Secondo giro ostile: nessun nuovo finding.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
