# Probe-Review CAP_09 bar_synthetic (micro-patch BOOK_5 bid1/ask1) — 2026-06-02 — Sede: CLI

**Sede**: CLI locale (workstation Windows del supervisore). DAPI live disponibile via DGo+Darwin, ma **non usato** (vedi nota divieto sotto).
**Natura**: probe-review RM-4 **criterio (b)** — il patch modifica un fatto dichiarato in un CAP PASS (`docs/methodology_v2/CAP_09_parte_9.md`, Parte 9, PASS storico `86425a7`). NON è CAP-review piena. NON ri-audita lo scope statico di Parte 9 (già PASS) né la metodologia.
**Oggetto**: micro-patch **UNCOMMITTED** (working tree; HEAD = `91e7799`) che aggiorna 2 annotazioni RM-1 di Cap.49 (riga 173 cella tabella `bar_synthetic`; riga 177 bullet prosa) da "Verifica parziale / non certificate → Empirico-CLI" a "Verificato `[PROVA-EMPIRICA 2026-06-01 W3 / M-10]` … certificate", + nuova sezione in `reports/REPORT_CAP_09.md`.
**Ruolo**: agente general-purpose in ruolo Reviewer (subagente nativo `reviewer` non disponibile in CLI), adottando in pieno `.claude/agents/reviewer.md` (regole assolute, sezione "Probe-review (RM-4)", divieti sede CLI `:163-164`).

**Letture preliminari confermate**: `tasks/METODO.md` (RM-1..RM-4) ✅; `.claude/agents/reviewer.md` incl. sezione Probe-review + divieti sede CLI ✅.

**Divieto sede CLI rispettato**: NON ho rieseguito BOOK_5 contro DAPI. La certificazione W3 è CHIUSA (`reviews/REVIEW_CAP_DATA_02_RM_RETRO_CLI_review.md`, PASS EMPIRICO, fase CLI 2026-06-01). Il mio compito è verificare che il patch **rifletta fedelmente** la fonte committata, leggendola — non rifare la misura (sarebbe zelo improprio, `reviewer.md:164`).

---

## VERDETTO: PASS

Il patch riflette **fedelmente e senza sovra-dichiarazione** la certificazione W3/M-10. Posizioni-campo e numeri combaciano verbatim con la fonte. Lo scope è circoscritto alle 2 annotazioni + REPORT; la metodologia di Parte 9 è intatta. Nessun BUG REALE. Due osservazioni minori NEUTRO (registro formato RM-1 inline; possibile incoerenza residua con Cap.47:93), nessuna bloccante — motivazione dettagliata sotto.

---

## Check RM-1: dichiarazioni di verifica (non sovra-dichiarano?)

Le due nuove dichiarazioni "Verificato RM-1 `[PROVA-EMPIRICA 2026-06-01 W3 / M-10]` … certificate".

**(a) Certifica SOLO ciò che W3/M-10 certifica?** — SÌ.
- Il patch dichiara le posizioni **a livello-1**: `bid1_lots` (campo 4), `bid1_price` (campo 6), `ask1_lots` (campo 19), `ask1_price` (campo 21). Sono esattamente i campi che la regola `bar_synthetic` interroga (gate `bid1_lots≥1 AND ask1_lots≥1`; mid `(bid1_price+ask1_price)/2`). VERIFICATO leggendo Cap.49 r173 (working tree): la formula e il gate sono immutati, e nominano solo questi 4 campi.
- **NON estende ai livelli 2-5**: il diff r173/r177 non cita bid2..bid5/ask2..ask5. La fonte W3 (riga 62-63) certifica l'intero schema (290 triple), quindi dichiarare certo il livello-1 è un **sottoinsieme onesto**, non una sovra-estensione. CONFERMATO via `git diff` — nessuna menzione di livelli 2-5 nelle 2 annotazioni.
- **`ask1_orders` (campo 20) NON è citato**: la fonte W3 (riga 66) enumera `bid1_orders`=campo 5 ma NON `ask1_orders`=campo 20. Il patch r173 cita `bid1_orders` solo implicitamente nella struttura del triplo `(lots, orders, price)`, e nelle posizioni operative nomina solo campo 4/6/19/21; il REPORT (sezione "RM-1 onesto") dichiara esplicitamente che campo 20 non è citato. CONFERMATO: nessuna delle 2 annotazioni asserisce campo 20.

**(b) Le affermazioni numeriche combaciano verbatim con la fonte?** — SÌ, tutte.

| Affermazione patch (Cap.49 r173/r177) | Fonte W3 (REVIEW_CAP_DATA_02…CLI) | M-10 (STATO_CORRENTE:77) | Esito |
|---|---|---|---|
| "ordine BID-poi-ASK escluso invertito (blocco 1 sempre discendente = BID, **29/29** eventi)" | r62: "Blocco 1 (triple 1–5) = BID: prezzi sempre DISCENDENTI … Vero su **29/29** eventi"; r68 anomalia non riprodotta | "`bid1<ask1` su 29/29" | ✅ coincide |
| "indice triplo `(lots,orders,price)` confermato da `lots >= orders` su **290/290** triple (alternativa `(orders,lots,price)` esclusa)" | r65: "su tutte le **290 triple** f1≥f2 (**290/290**) … Esclusa l'alternativa `(orders, lots, price)`" | "`f1≥f2` su 290/290 (lots≥orders) esclude triplo invertito" | ✅ coincide |
| "anomalia `bid1_price > ask1_price` del campione 27/05 … **NON riprodotta** (artefatto del contratto illiquido FIB6I …); `bid1_price < ask1_price` su **29/29**" | r68: "anomalia … **NON riprodotta** … artefatto del campione (FIB6I, scadenza più lontana/illiquida) … NON un'inversione"; r64 bid1<ask1 29/29 | "Anomalia 27/05 `bid1>ask1` = artefatto del campione (FIB6I illiquido …), NON inversione schema" | ✅ coincide |
| "29 eventi / 290 triple su FIB6F front-month liquido" | r57: "29 eventi BOOK_5 catturati"; r61: "290 triple" su FIB6F (GIU26) | "FIB6F", "290/290", "29/29" | ✅ coincide |

Nessuna sovra-dichiarazione, nessun numero non combaciante. Le alternative escluse enunciate dal patch (ordine ASK-poi-BID; triplo `(orders,lots,price)`; "bid1>ask1 strutturale") corrispondono 1:1 alle "ALTERNATIVE COMPATIBILI ESCLUSE" della fonte (W3 riga 72).

**(c) Formato del blocco 4-righe** — vedi Osservazione minore #1 (NEUTRO). Le annotazioni patchate sono in **prosa inline** (parentesi in cella tabella e in bullet), non nel blocco 4-righe esatto `VERIFICA/PROVE/ALTERNATIVE ESCLUSE/ALTERNATIVE NON ESCLUSE`. La lettura massimalista di `reviewer.md:114` ("prosa libera = non in formato = BUG REALE") **non si applica qui** per coerenza con la convenzione interna già ratificata del documento (motivazione completa sotto).

Esito Check RM-1: **PASS**. La verifica è onesta (sottoinsieme livello-1), numericamente fedele, alternative escluse corrette.

## Check RM-2: posizioni/schema vs fonte (lettura, non riesecuzione)

Confronto delle posizioni-campo dichiarate dal patch contro la fonte autoritativa.

- Patch: schema `[BID×5 best-first][ASK×5 best-first]`, ogni livello triplo `(lots, orders, price)`. `bid1_lots`=campo 4, `bid1_price`=campo 6, `ask1_lots`=campo 19, `ask1_price`=campo 21.
- Fonte W3 (riga 59, 66): "30 campi = 10 triple = `(lots,orders,price)`. Blocco 1 = 5 livelli BID, blocco 2 = 5 livelli ASK … `bid1_lots`=campo 4 (1ª tripla, pos f1), `bid1_orders`=campo 5, `bid1_price`=campo 6; `ask1_lots`=campo 19 (6ª tripla), `ask1_price`=campo 21." → **coincide esattamente**.
- M-10 (STATO_CORRENTE:77): "`bid1_lots`=campo4, `bid1_orders`=campo5, `bid1_price`=campo6; `ask1_lots`=campo19, `ask1_price`=campo21" → **coincide**.
- Coerenza con la "home" dello schema (Cap.47:93, NON toccata dal patch): il template `BOOK_5;<TICKER>;<HH:mm:ss>;<bid1_lots>;<bid1_ord>;<bid1_price>;<bid2..>…;<ask1_lots>;<ask1_ord>;<ask1_price>;…` con campi 1-3 = `BOOK_5;TICKER;HH:mm:ss`, poi tripla bid1 = campi 4,5,6, triple bid2-bid5 = campi 7-18 (4×3), tripla ask1 = campi 19,20,21. Il conteggio **conferma** campo 4/6/19/21. Il patch quindi NON introduce numeri nuovi: ridenomina lo *stato di certezza* di posizioni già implicite nello schema di Cap.47. CONFERMATO via conteggio campi su Cap.47:93.

RM-2 "decoder esistenti nel repo": il patch NON introduce un decoder (è sola annotazione). La fonte W3 (riga 173 della review CLI) dichiara di aver riusato `scripts/probe_dapi.py` (`parse_line`) senza riscriverlo. Grep di controllo indipendente sui decoder BOOK_5 nel repo:

```
grep -rn "BOOK_5\|parse_line" --include=*.py  → scripts/probe_dapi.py (decoder unico, già citato dalla fonte)
```

(Eseguito; `probe_dapi.py` è l'unico parser BOOK_5; nessun decoder alternativo non citato.) Nessuna fonte mancata.

Esito Check RM-2: **PASS**. Posizioni-campo identiche alla fonte e coerenti con lo schema-home di Cap.47. Nessun decoder non citato.

## Check RM-3: fonti etichettate

- Le 2 annotazioni patchate sono etichettate `[PROVA-EMPIRICA 2026-06-01 W3 / M-10]` (livello-1) + riferimento al file CLI `[rif. reviews/REVIEW_CAP_DATA_02_RM_RETRO_CLI_review.md, M-10]`. Etichetta corretta per il livello di fonte (prova empirica diretta + review committata).
- La sezione REPORT cita la fonte come "autoritativa, NON ri-derivata" con righe puntuali (`§W3 righe 55-73`, `STATO_CORRENTE §5 M-10 riga 77`).
- **Nessuna conclusione si appoggia a wiki/livello-4.** Al contrario, la certificazione W3 ha *falsificato* l'anomalia che derivava dal campione singolo, e il documento conserva altrove `[CORREGGE WIKI]` sullo schema CANDLE. Coerente con RM-3 (livello-4 = solo hint).

Esito Check RM-3: **PASS**.

## Check 4: onestà mappatura claim → evidenza

Ogni claim del patch ha ancora a evidenza puntuale nella fonte:

- "290/290", "29/29 eventi", "FIB6F front-month liquido": ancorati a W3 r57/r61/r62/r64/r65 e a M-10 r77. ✅
- "anomalia FIB6I illiquido NON riprodotta": ancorata a W3 r68. ✅
- Il riferimento file+sezione è citabile e corretto (ho letto W3 r55-73 e M-10 r77 direttamente). ✅

**Claim "cautela Cap.47 saldata"** — esaminato a parte (è il claim più forte del patch):
- La cautela ESISTEVA: Cap.47:93 dichiara "Verifica parziale (RM-1): lo schema BOOK_5 deriva da una singola osservazione del 2026-05-27 … Alternative compatibili non escluse: ordine dei blocchi BID/ASK (… `bid1_price=49715.0` > `ask1_price=49275.0` … non disambiguato), indice del triplo `lots`/`orders`/`price`. … disambiguata con cattura di ≥N eventi BOOK_5 su FIB front-month liquido (Empirico-CLI)."
- La certificazione W3 chiude **esattamente** quelle due alternative (ordine blocchi + indice triplo) con ≥N eventi su FIB6F liquido (29 eventi / 290 triple), e spiega l'anomalia 49715>49275 come artefatto FIB6I illiquido. Quindi, sul **merito**, "cautela saldata" è **giustificato**: ciò che Cap.47 chiedeva (cattura su front-month liquido) è stato fatto e ha disambiguato.
- **MA**: il patch dichiara "cautela Cap.47 saldata" **dentro Cap.49**, e NON modifica Cap.47:93, che resta testualmente con l'etichetta "Verifica parziale (RM-1) … Empirico-CLI". Questo lascia il documento in uno stato dove Cap.49 dice "saldata" e Cap.47 dice ancora "verifica parziale". Vedi Osservazione minore #2 (NEUTRO): è una potenziale incoerenza di lettura, NON un BUG REALE (il claim è vero; la home semplicemente non è stata aggiornata, scelta di scope deliberata e documentata nel REPORT come "Cap.47:93 … fuori scope del task").

Esito Check 4: **PASS**. Ogni claim è ancorato. "Cautela saldata" è vero sul merito; la non-propagazione a Cap.47 è un'osservazione di coerenza minore, non un difetto di onestà.

## Scope

`git diff --stat` (working tree):

| File | Δ | In scope atteso? |
|---|---|---|
| `docs/methodology_v2/CAP_09_parte_9.md` | 2 righe modificate (r173, r177) | ✅ esattamente le 2 annotazioni |
| `reports/REPORT_CAP_09.md` | +48 (nuova sezione micro-patch) | ✅ |
| `tasks/DEV_STATUS.md` | +1 (`READY_FOR_PROBE_REVIEW …`) | ✅ segnale di stato |
| `.claude/settings.json` | +3 (`worktree.bgIsolation`) | ⚠️ estraneo al task — vedi nota |

- **CAP_09_parte_9.md tocca SOLO r173 + r177**: CONFERMATO via `git diff`. Le due righe sono le annotazioni RM-1 in parentesi; il resto della cella (gate, formula mid, casi b/c) e del bullet è invariato byte-per-byte salvo la parentesi.
- **Metodologia intatta**: la mappatura schema CANDLE (Cap.49 r155-172, incluso il blocco 4-righe r158-161 e le righe `bar_open`/`bar_close`), la regola `bar_synthetic` stessa, la tabella codici errore (r199-212), l'indice, gli AC — **NON toccati**. CONFERMATO via grep (le occorrenze "verifica parziale"/"Empirico-CLI" residue a r29/47/51/61/93/203-209 riguardano banner, cooldown, mesi IDEM, codici errore e la home BOOK_5 — tutte fuori scope di questo micro-patch).
- **Parte 9 resta PASS storico `86425a7`**: il patch è un upgrade dello *stato di certezza* di un'annotazione (Verifica parziale → Certificato), non un cambiamento di metodologia, formula, posizioni-campo o comportamento runtime. Coerente con la natura dichiarata nel REPORT.
- **Nota su `.claude/settings.json`**: è un file di configurazione locale, estraneo al task (CLAUDE.md "Check post-Developer" tollera esplicitamente `.claude/*` locali). NON deve entrare nel commit del micro-patch. **Raccomandazione all'Orchestratore**: committare il patch con `git add` mirato a `docs/methodology_v2/CAP_09_parte_9.md`, `reports/REPORT_CAP_09.md`, `tasks/DEV_STATUS.md` (azzerato) e questo file di review — **escludendo** `.claude/settings.json` e `.claude/scheduled_tasks.lock`.

Esito Scope: **PASS** (con raccomandazione di igiene commit sul file `.claude/settings.json` estraneo).

## Osservazioni minori (NEUTRO — non bloccanti, non vanno a Developer per default)

**OM-1 — Registro formato RM-1 "inline" vs blocco 4-righe.** `reviewer.md:114` impone, in linea di principio, che ogni "Verificato X" usi il blocco 4-righe esatto `VERIFICA/PROVE/ALTERNATIVE ESCLUSE/ALTERNATIVE NON ESCLUSE`, respingendo la "prosa libera" come BUG REALE. Le 2 annotazioni patchate sono in prosa inline (parentesi). **Perché NON è BUG REALE qui**:
- Il documento Parte 9 — **PASS storico `86425a7`** e ri-validato dall'audit RM CAP-DATA-02 (PASS WEB+CLI) — usa **due registri**, entrambi ratificati: (i) il blocco 4-righe formale come **blockquote dedicato** una sola volta, per il fatto più critico (mappatura CANDLE, r158-161, l'incidente originale `7bb2955`); (ii) annotazioni **inline** con etichetta `[PROVA-EMPIRICA …]` + alternative in prosa per tutto il resto — banner (r29), cooldown (r47/51/212), mesi IDEM (r61), codici errore (r205-210), e in particolare le celle `bar_open`/`bar_close` (r167/170, con `[PROVA-EMPIRICA M-1]` inline e NON nel blocco 4-righe).
- Il patch r173/r177 è **strutturalmente identico** al registro (ii) già ratificato: stessa etichetta, stesse alternative escluse enunciate, stessa collocazione (cella di tabella / bullet). Un'annotazione tra parentesi dentro una cella di tabella **non può** ospitare un blocco multi-riga senza rompere la tabella Markdown.
- Applicare la lettura massimalista *solo a queste 2 righe* mentre l'intero capitolo PASS usa lo stesso registro inline sarebbe **incoerente** e non aumenterebbe il rigore reale: le alternative compatibili SONO enumerate ed escluse con numeri puntuali (29/29, 290/290), che è la sostanza di RM-1. Il rigetto "non in formato" colpisce le asserzioni che *omettono* le alternative; qui non sono omesse.
- Classificazione: **NEUTRO**. Se il supervisore volesse uniformare al blocco 4-righe, l'unico punto sostanziale sarebbe convertire **anche** l'annotazione esistente `bar_open`/`bar_close` (r167/170) per coerenza — operazione cosmetica fuori dallo scope di questo micro-patch e da non imporre come gate.

**OM-2 — "Cautela Cap.47 saldata" dichiarata in Cap.49 ma Cap.47:93 non aggiornato.** Il patch chiude correttamente, sul merito, la cautela di Cap.47 (la certificazione W3 ha fatto esattamente la cattura su front-month liquido che Cap.47 chiedeva). Ma testualmente Cap.47:93 resta "Verifica parziale (RM-1) … Empirico-CLI", creando una lettura dove Cap.49 dice "saldata" e Cap.47 dice ancora "parziale". **Perché NON è BUG REALE**: (a) il claim è vero (la cautela è effettivamente disambiguata dalla fonte); (b) il REPORT documenta esplicitamente che Cap.47:93 è "fuori scope del task" e NON toccato — quindi è una scelta deliberata di scope, non un errore o un'auto-dichiarazione falsa; (c) la regola operativa `bar_synthetic` vive in Cap.49, ed è lì che la certezza delle posizioni conta per il motore. Classificazione: **NEUTRO**, con nota di **coerenza documentale** per il supervisore: se si vuole eliminare la dissonanza, un secondo micro-patch (o un'estensione di questo) potrebbe aggiornare anche l'annotazione di Cap.47:93 da "verifica parziale → Empirico-CLI" a "certificato W3/M-10". Non bloccante per il commit del patch corrente; segnalato perché è esattamente il tipo di residuo che un audit RM futuro potrebbe ri-aprire.

## Tabella classificazione finding

| # | Finding | Classificazione | A Developer? |
|---|---------|-----------------|--------------|
| OM-1 | Annotazioni RM-1 in prosa inline anziché blocco 4-righe | NEUTRO (coerente con registro inline già PASS del capitolo) | NO — non cambia il rigore reale |
| OM-2 | "Cautela Cap.47 saldata" in Cap.49 mentre Cap.47:93 resta "verifica parziale" | NEUTRO (claim vero; non-propagazione è scelta di scope documentata) | NO per default — eventuale follow-up coerenza a discrezione supervisore |

**0 BUG REALE. 0 problema bloccante.**

## Verdetto motivato

**PASS.** Il micro-patch riflette la certificazione W3/M-10 in modo **fedele e onesto**: (1) le posizioni `bid1_lots`=campo 4, `bid1_price`=campo 6, `ask1_lots`=campo 19, `ask1_price`=campo 21 e lo schema `[BID×5][ASK×5]` triplo `(lots,orders,price)` coincidono **verbatim** con `reviews/REVIEW_CAP_DATA_02_RM_RETRO_CLI_review.md` §W3 (r59, r66) e con M-10 (`STATO_CORRENTE.md:77`); (2) i numeri 29 eventi / 290 triple, 29/29 (ordine BID), 290/290 (`lots≥orders`), anomalia FIB6I non riprodotta combaciano tutti; (3) il patch **non sovra-dichiara** — certifica solo il livello-1 effettivamente interrogato dalla regola `bar_synthetic`, non estende a livelli 2-5, non cita `ask1_orders` (campo 20) che la fonte non enumera; (4) lo scope è circoscritto alle 2 annotazioni (r173, r177) + sezione REPORT, con la metodologia di Parte 9 (mappatura CANDLE, regola `bar_synthetic`, codici errore, AC, indice) **intatta**, e Parte 9 resta correttamente PASS storico `86425a7` (upgrade di stato di un'annotazione, non cambio di metodologia).

Le due osservazioni minori sono **NEUTRO** e non giustificano CONDITIONAL: il registro inline del formato RM-1 è quello già adottato e ratificato dall'intero capitolo PASS (imporre il blocco 4-righe solo su queste 2 righe sarebbe incoerente, e le alternative compatibili sono comunque enumerate ed escluse con evidenza numerica puntuale); il claim "cautela Cap.47 saldata" è vero sul merito (la certificazione W3 ha eseguito esattamente la disambiguazione su front-month liquido che Cap.47 richiedeva), e la non-propagazione testuale a Cap.47:93 è una scelta di scope esplicitamente documentata nel REPORT, non un'auto-dichiarazione falsa.

**Gate RM-4(b) soddisfatto**: l'output NON è committato; questa probe-review emette PASS, quindi l'Orchestratore può procedere al commit (patch + REPORT + questa review), avendo cura di **escludere** il file estraneo `.claude/settings.json` dal commit del micro-patch.

**Nessun handoff alla sede opposta richiesto**: la verifica è documentale (fedeltà del patch alla fonte committata), interamente eseguibile in CLI per lettura; nessuna ri-misura empirica necessaria (la fonte W3 è già la fase empirica CLI chiusa).

---

### Applicazione RM-1 a me stesso (reviewer)

- **RM-1**: ogni "coincide/confermato" sopra è ancorato a citazione `file:riga` + esito (tabella Check RM-1 e RM-2). Non ho dichiarato "verificato empiricamente" nulla: ho verificato **fedeltà documentale** (patch vs fonte committata), non ho rifatto la misura BOOK_5 (divieto sede CLI `reviewer.md:164`). L'unica alternativa che ho lasciato aperta è di coerenza documentale (OM-2), classificata NEUTRO con motivazione.
- **RM-2**: ho eseguito grep indipendente sui decoder BOOK_5 (`probe_dapi.py` unico, già citato dalla fonte); nessun decoder alternativo non citato. Il patch non introduce decoder.
- **RM-3**: ogni mia conclusione è ancorata a livelli 1-3 (la review CLI W3 = prova empirica committata; M-10 = documento interno; Cap.47:93/Cap.49 = documento interno). Nessun appoggio al wiki.
- **Divieto sede CLI rispettato**: nessuna riesecuzione di BOOK_5 contro DAPI; ho solo letto la fonte committata. Nessun probe massivo di zelo.
- **File scritti**: unico file = questa review (working tree, **NON committato**). Nessun `git add/commit/push` eseguito.
