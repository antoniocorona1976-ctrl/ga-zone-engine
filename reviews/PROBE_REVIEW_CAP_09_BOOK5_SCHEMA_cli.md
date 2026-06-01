# Probe-Review CAP_09 schema BOOK_5 (micro-patch #2 Cap.47:93) — 2026-06-02 — Sede: CLI

**Verdetto**: PASS

Lettura confermata: `tasks/METODO.md` (RM-1..RM-4) + `.claude/agents/reviewer.md` (sezione "Probe-review (RM-4)" + divieti sede CLI). Audit ostile, focalizzato sui 4 check RM-4. Non ho riscritto il patch. Non ho ri-eseguito BOOK_5 contro DAPI (W3 e' CHIUSA — divieto CLI `reviewer.md:164`): ho verificato la **fedelta' documentale** della citazione leggendo la fonte committata.

Oggetto: seconda micro-patch UNCOMMITTED a `docs/methodology_v2/CAP_09_parte_9.md` **riga 93** (Cap.47, schema `BOOK_5`) — la caveat "Verifica parziale (RM-1) … Empirico-CLI" sostituita con "Verificato (RM-1) `[PROVA-EMPIRICA 2026-06-01 W3 / M-10]` … certificato". HEAD `1ff556c`. RM-4 criterio (b): modifica un fatto in un CAP PASS storico (`86425a7`). Chiude OM-2 della probe-review di patch #1.

---

## Check RM-1: dichiarazioni di verifica (no sovra-dichiarazione)

Asserzione "Verificato/certificato" introdotta nel patch e confronto verbatim con la fonte (`reviews/REVIEW_CAP_DATA_02_RM_RETRO_CLI_review.md` §W3 r.55-73 + `tasks/STATO_CORRENTE.md` §5 M-10 r.77):

| Claim del patch (r.93) | Fonte | Esito |
|---|---|---|
| "29 eventi / 290 triple su FIB6F front-month liquido" | W3 r.57 "29 eventi BOOK_5 catturati" + r.61 "290 triple"; M-10 r.77 "290/290" | **COINCIDE** |
| "ordine dei blocchi BID-poi-ASK confermato (blocco 1 sempre discendente = BID su 29/29, NON invertito)" | W3 r.62 "Blocco 1 (triple 1-5) = BID: prezzi sempre DISCENDENTI … Vero su 29/29 eventi" + r.68 "BID-poi-ASK con best-first" | **COINCIDE** |
| "indice del triplo `(lots, orders, price)` confermato da `lots >= orders` su 290/290 triple (esclusa `(orders, lots, price)`)" | W3 r.65 "su tutte le 290 triple f1≥f2 (290/290) … Esclusa l'alternativa `(orders, lots, price)`"; M-10 r.77 "`f1≥f2` su 290/290 (lots≥orders) esclude triplo invertito" | **COINCIDE** |
| "`bid1_price < ask1_price` su 29/29 eventi" | W3 r.64 "bid1_price < ask1_price su 29/29 eventi"; M-10 r.77 "`bid1<ask1` su 29/29" | **COINCIDE** |
| "anomalia `bid1_price=49715.0 > ask1_price=49275.0` del campione singolo 27/05 … NON riprodotta … artefatto del contratto illiquido FIB6I a scadenza lontana, non un'inversione di schema" | W3 r.68 "Anomalia 27/05 … NON riprodotta … artefatto del campione (book rado/crossato su contratto poco scambiato), NON un'inversione dei blocchi"; M-10 r.77 "Anomalia 27/05 `bid1>ask1` = artefatto del campione (FIB6I illiquido scadenza lontana), NON inversione schema" | **COINCIDE** |

**Nota "D non parsa BOOK_5 → certificazione level-1, non level-2" — MANTENUTA e onesta**: il patch chiude con "Il decoder canonico D continua a non parsare `BOOK_5`: la certificazione e' empirica diretta a livello-1 via probe CLI `[PROVA-EMPIRICA 2026-06-01]`, non level-2 da codice di produzione." Verifica indipendente sul decoder (`scripts/probe_dapi.py:307-317`): il ramo `BOOK_5;` esegue **solo** `line.split(";")` e restituisce `"fields": p[3:]` grezzi (kind="book5"), **senza** interpretare ordine BID/ASK ne' indice del triplo. Confermato: il decoder di produzione NON corrobora lo schema — la prova e' empirica diretta, non da codice. La caveat e' percio' **onesta** nel non spacciare per level-2 cio' che e' level-1. Non sovra-estende: non dichiara nulla sui livelli 2-5 oltre l'ordinamento prezzi gia' osservato, ne' sulla semantica nominale di "orders" (che W3 r.73 lascia "nominale ma non incidente su bar_synthetic").

**Sovra-claim**: nessuno. Ogni elemento certificato dal patch e' un sottoinsieme esatto di cio' che W3/M-10 certifica. Non trovo asserzioni che eccedano la fonte.

**Formato 4-righe (RM-1 strict `METODO.md:28-33`)**: la nuova dichiarazione e' in **prosa inline** ("Verificato (RM-1) `[PROVA-EMPIRICA …]`: …"), non nel blocco 4-righe `VERIFICA / PROVE / ALTERNATIVE ESCLUSE / ALTERNATIVE NON ESCLUSE`. Pur contenendo nel testo gli elementi del blocco (le alternative escluse sono enumerate: ordine blocchi, indice triplo, anomalia 27/05). Classificazione: **NEUTRO**, NON BUG REALE — motivazione di precedente vincolante sotto (la caveat ORIGINALE sostituita era anch'essa "Verifica parziale (RM-1): …" in prosa inline, gia' PASS in `86425a7`; tutte le annotazioni di verifica di Parte 9 — es. `bar_open`/`bar_close` r.167/170, e le annotazioni Cap.49 r.173/177 di patch #1 gia' landed PASS — usano lo stesso registro inline; la probe-review di patch #1 ha classificato lo stesso punto OM-1 NEUTRO, `PROBE_REVIEW_CAP_09_BAR_SYNTHETIC_cli.md:118`). Imporre il blocco 4-righe qui sarebbe un cambio di registro dell'intero capitolo PASS, fuori dallo scope di un micro-patch di sola annotazione, e contraddirebbe il precedente landed. Coerentemente con `reviewer.md` (no blocco per cosmesi/registro quando il rigore reale e' presente e ancorato), non e' bloccante.

**Esito Check RM-1: PASS.** Numeri e asserzioni combaciano verbatim con W3/M-10. Nessun sovra-claim. Nota level-1/level-2 mantenuta e verificata indipendente. Registro inline = NEUTRO (precedente vincolante), non BUG REALE.

## Check RM-2: schema vs fonte + grep decoder esistenti

**Definizione schema INVARIATA**: la stringa `BOOK_5;<TICKER>;<HH:mm:ss>;<bid1_lots>;<bid1_ord>;<bid1_price>;<bid2..>;…;<ask5..>` (5 BID + 5 ASK, triplo `lots/orders/price`) sul rigo 93 e' **identica** prima e dopo (confronto `git diff` r.93: la sostituzione tocca SOLO la frase di caveat finale, dopo l'esempio). **Esempio INVARIATO**: `BOOK_5;FIB6I;14:02:33;1;1;49715.0;1;1;49275.0;0;0;0.0;…;1;1;50535.0;1;1;51115.0;0;0;0.0;…` e' byte-identico prima/dopo. Cambia **solo** la caveat.

**Schema `[BID×5][ASK×5]` triplo `(lots,orders,price)` + risoluzioni vs W3**: ordine blocchi (BID-poi-ASK, best-first), indice triplo (`lots,orders,price` con `lots≥orders`) e posizioni-campo coincidono con W3 r.59-66 e M-10 r.77. Le posizioni puntuali (`bid1_lots`=c4, `bid1_price`=c6, `ask1_lots`=c19, `ask1_price`=c21) non sono ripetute nel patch #2 (che resta a livello "ordine blocchi + indice triplo"), ma sono coerenti con W3 r.66 e con patch #1 (Cap.49) gia' landed — nessuna divergenza.

**Grep decoder BOOK_5 nel repo** (verifica indipendente, `--glob *.py`): unico match in `scripts/probe_dapi.py` (`:307-317`), gia' l'atteso e gia' citato dalla fonte W3 (r.173 della review CLI dichiara riuso di `probe_dapi.py` senza riscrittura). Nessun decoder BOOK_5 alternativo non citato. Il patch #2 **non introduce** alcun decoder (e' sola annotazione testuale), quindi RM-2 "decoder esistenti" si applica solo come controllo di non-omissione: nessuna fonte mancata.

**Esito Check RM-2: PASS.** Definizione schema ed esempio del probe invariati (solo caveat cambiata). Schema/risoluzioni coincidono con W3. `probe_dapi.py` unico parser BOOK_5, gia' coperto, nessun decoder occulto.

## Check RM-3: fonti etichettate

- Etichetta `[PROVA-EMPIRICA 2026-06-01 W3 / M-10]` presente sull'asserzione principale (livello 1). ✅
- Riferimento file citabile `[rif. reviews/REVIEW_CAP_DATA_02_RM_RETRO_CLI_review.md, M-10]` presente. ✅ (Ho letto W3 r.55-73 e M-10 r.77 direttamente: i riferimenti sono corretti.)
- Seconda etichetta `[PROVA-EMPIRICA 2026-06-01]` sulla frase level-1/level-2. ✅
- Nessuna conclusione appoggiata a wiki / livello-4. La certificazione e' ancorata a prova empirica (livello 1) + documento interno (M-10, livello 3). Coerente con RM-3 (anzi, il patch e' espressamente cauto nel declassare a level-1 cio' che non e' supportato dal codice di produzione level-2).

**Esito Check RM-3: PASS.**

## Check 4: onesta' mappatura claim → evidenza

Ogni claim del patch e' ancorato a evidenza puntuale citabile (tabella Check RM-1: ogni riga → `file:riga` della fonte). Nessuna asserzione orfana.

**Claim "esattamente la disambiguazione che questa caveat richiedeva"** (il claim piu' forte del patch #2) — esaminato a parte:
- La caveat ORIGINALE (r.93 pre-patch, riportata integralmente nel REPORT "PRIMA") chiedeva testualmente: "La struttura va disambiguata con cattura di **≥N eventi `BOOK_5` su FIB front-month liquido (Empirico-CLI)**" e lasciava aperte due alternative: (1) ordine blocchi BID/ASK (con l'anomalia `bid1>ask1` come indizio di possibile inversione), (2) indice del triplo `lots/orders/price`.
- W3 ha fatto **esattamente** questo: 29 eventi su **FIB6F front-month liquido** (la caveat chiedeva "front-month liquido" — W3 r.57 "FIB6F front-month (GIU26, liquido)"), e ha chiuso **entrambe** le alternative (ordine blocchi via 29/29 discendente=BID; indice triplo via `lots≥orders` 290/290) + spiegato l'anomalia 27/05 come artefatto FIB6I illiquido.
- Quindi "esattamente la disambiguazione richiesta" e' **giustificato sul merito**: il predicato della caveat (≥N eventi su front-month liquido) e' soddisfatto alla lettera, e le due alternative nominate sono entrambe risolte. Non e' un claim retorico: e' una corrispondenza puntuale requisito→evidenza.

**Esito Check 4: PASS.** Ogni claim ancorato. Il claim forte "disambiguazione esatta" e' verificabile e vero.

## Scope

`git diff --stat` (working tree, HEAD `1ff556c`):
- `docs/methodology_v2/CAP_09_parte_9.md` — **1 riga** (r.93). Confermato leggendo il blocco r.90-94: r.92 (ANAG) e r.94 (PRICE) **INVARIATI**; definizione schema ed esempio del probe su r.93 **INVARIATI** (solo la caveat finale del bullet cambia). ✅
- `reports/REPORT_CAP_09.md` — `+43` righe: nuova sezione "Micro-patch post-PASS #2" (motivazione, fonte, prima→dopo, file:riga, note di stato, rollback). Coerente, nessuna sovra-dichiarazione. ✅
- `tasks/DEV_STATUS.md` — `+1`: `READY_FOR_PROBE_REVIEW docs/methodology_v2/CAP_09_parte_9.md`. ✅ (trigger corretto del workflow RM-4 opzione B)
- `.claude/settings.json` — `+5/-2` (chiave `worktree.bgIsolation`): **ESTRANEO al task**, tollerato (`reviewer.md` / `CLAUDE.md` check post-Developer punto 4 — file `.claude/*` locali tollerati). **NON deve entrare** nel commit del micro-patch (l'Orchestratore lo escluda, come gia' fatto per patch #1).

Non toccati (verificato): Cap.49 r.173/177 (gia' patchate da patch #1 in `1ff556c`), tabella codici errore Cap.50, indice `00_indice.md`, AC. **Parte 9 resta PASS storico `86425a7`**: la modifica e' un upgrade di stato di un'annotazione descrittiva (Verifica parziale → Certificato), schema/esempio/metodologia/regola `bar_synthetic`/posizioni-campo invariati, nessun impatto su comportamento runtime ne' su mappatura dati. Il PASS storico regge.

**Esito Scope: OK.** Solo caveat r.93 + REPORT + DEV_STATUS (trigger). `.claude/settings.json` estraneo e da escludere dal commit, non parte del task.

## Coerenza patch #1 ↔ patch #2 (chiusura OM-2)

- Patch #1 (commit `1ff556c`, Cap.49 r.173+177) ha aggiornato a CERTIFICATE le annotazioni `bar_synthetic` e ha dichiarato due volte "la cautela 'verifica parziale → Empirico-CLI' di Cap.47 e' **saldata**".
- La probe-review di patch #1 (`reviews/PROBE_REVIEW_CAP_09_BAR_SYNTHETIC_cli.md:119`) ha rilevato **OM-2** (NEUTRO): «"Cautela Cap.47 saldata" in Cap.49 mentre Cap.47:93 resta "verifica parziale"» → incoerenza documentale residua, follow-up a discrezione supervisore. Il commit message di `1ff556c` la cita esplicitamente: "OM-2 NEUTRO: Cap.47:93 mantiene ancora 'verifica parziale -> Empirico-CLI' (fuori scope 'unica modifica = Cap.49') -> coerenza documentale per eventuale follow-up."
- Patch #2 aggiorna **esattamente** Cap.47:93 (la sorgente che Cap.49 dichiarava saldata) allo stesso stato di certezza, con la stessa fonte W3/M-10 e gli stessi numeri.
- **Esito: COERENTI. OM-2 CHIUSO.** Dopo patch #2, Cap.47:93 (home dello schema) e Cap.49 r.173/177 (annotazioni che vi rimandano) sono allineate: la cautela dichiarata "saldata" in Cap.49 e' ora effettivamente saldata nella sua sorgente. Nessuna contraddizione tra le due patch (stessa fonte, stesso livello di certezza, stessa spiegazione dell'anomalia 27/05). Le posizioni-campo di patch #1 (c4/c6/c19/c21) sono un raffinamento di patch #2 (ordine blocchi + indice triplo): sottoinsieme coerente, non divergente.

## Punti aperti per la sede opposta

Nessuno. L'audit e' di **fedelta' documentale** (patch vs fonte committata), interamente eseguibile in sede CLI senza riesecuzione DAPI. La misura empirica sottostante (W3) e' gia' CHIUSA e committata; non richiede ulteriore follow-up Web. Nessun "Statico-Web da verificare".

## Tabella classificazione finding

| # | Finding | Classificazione | Mandare a Development? |
|---|---------|-----------------|------------------------|
| OM-1 | Dichiarazione di verifica r.93 in prosa inline anziche' blocco 4-righe `VERIFICA/PROVE/ALTERNATIVE ESCLUSE/NON ESCLUSE` | NEUTRO (coerente con registro inline dell'intero capitolo gia' PASS `86425a7`; precedente vincolante OM-1 di patch #1 stesso esito; la caveat sostituita era anch'essa inline) | NO — non cambia il rigore reale; convertire imporrebbe cambio di registro all'intero capitolo PASS, fuori scope micro-patch |

**0 BUG REALE. 0 problema bloccante.**

## Verdetto motivato

**PASS.** Il patch #2 riflette **fedelmente e senza sovra-dichiarazione** la certificazione W3/M-10: tutti e cinque i numeri/asserzioni chiave (29 eventi / 290 triple; BID-poi-ASK 29/29; `lots≥orders` 290/290; `bid1<ask1` 29/29; anomalia 27/05 = artefatto FIB6I illiquido NON riprodotta) combaciano **verbatim** con la fonte committata. La definizione dello schema `BOOK_5;<TICKER>;…` e l'esempio del probe `BOOK_5;FIB6I;14:02:33;…` restano **invariati**: cambia solo la caveat finale del bullet r.93. La nota "D non parsa BOOK_5 → certificazione level-1, non level-2" e' **mantenuta e verificata indipendente** (`probe_dapi.py:307-317` fa solo split, non interpreta lo schema): il patch e' onesto nel non spacciare per level-2 una prova level-1. Lo scope e' chirurgico (r.93 + REPORT + DEV_STATUS-trigger); `.claude/settings.json` e' estraneo e da escludere dal commit. **OM-2 della probe-review di patch #1 e' chiuso**: Cap.47:93 e Cap.49 sono ora coerenti, senza contraddizione tra le due patch. L'unico finding (OM-1, registro inline vs blocco 4-righe) e' NEUTRO per precedente vincolante landed e per coerenza col registro dell'intero capitolo PASS — non bloccante. Parte 9 resta PASS storico `86425a7` (upgrade di stato di annotazione descrittiva, metodologia intatta).

Gate RM-4(b) soddisfatto: l'output NON e' committato; questa probe-review emette PASS → l'Orchestratore puo' procedere al commit (patch + REPORT + DEV_STATUS + questa review), **escludendo** `.claude/settings.json`.

---

### Applicazione RM-1 a me stesso (reviewer)

- **RM-1**: ogni "COINCIDE/confermato" della tabella Check RM-1 e' ancorato a `file:riga` della fonte (W3 r.55-73, M-10 r.77) + esito. Non ho dichiarato "verificato empiricamente" alcunche': ho verificato **fedelta' documentale** (patch vs fonte committata), NON ho rifatto la misura BOOK_5 (divieto sede CLI `reviewer.md:164` — W3 e' CHIUSA). L'unica osservazione lasciata aperta (OM-1, registro) e' classificata NEUTRO con motivazione di precedente. ALTERNATIVE NON ESCLUSE sul mio giudizio: nessuna — la fedelta' e' una corrispondenza testuale binaria, qui verificata riga-per-riga.
- **RM-2**: grep indipendente sui decoder BOOK_5 eseguito (`--glob *.py` → `probe_dapi.py` unico, gia' citato dalla fonte; ispezionato `:307-317`). Nessun decoder alternativo non citato. Il patch non introduce decoder.
- **RM-3**: ogni mia conclusione e' ancorata a livelli 1-3 (W3 = prova empirica committata; M-10 = documento interno; Cap.47:93 / Cap.49 / probe-review #1 = documenti interni). Nessun appoggio al wiki/livello-4.
- **Divieto sede CLI rispettato**: nessuna riesecuzione di BOOK_5 contro DAPI; solo lettura della fonte committata. Nessun probe massivo di zelo.
- **File scritti**: unico file = questa review (working tree, **NON committato**). Nessun `git add/commit/push` eseguito.
