# REVIEW — SPEC-FUNZ-01-B5 (Runtime DAPI, sessione & compliance)

> **Perimetro**: audit ostile pieno (CAP-review adattata al non-CAP, due giri) del blocco B5 della ricostruzione cieca a 8 blocchi (modalità B).
> **Oggetti**: `docs/spec_funzionale/SPEC_FUNZ_01_B5.md` (commit `4bb9225`, 35 requisiti: 20 B5-R, 9 B5-CN, 7 B5-NFR) + `reports/REPORT_SPEC_FUNZ_01_B5.md`.
> **Fonte floor citazioni**: `docs/methodology_v2/CAP_09_parte_9.md` (Cap.46,47,52,53,54; framing 45/50) + `docs/methodology_v2/CAP_01_parte_I.md` (Cap.1), frozen G-09.
> **Autorità di partizione**: `docs/spec_funzionale/PROPOSTA_SUDDIVISIONE_SPEC_v2.md` mappa consolidata `c7ce4be` (riga B5: 11 req-v2 = R-7.1, R-7.2, CN-7.1, CN-7.2, CN-7.5, CN-7.6, CN-7.7, CN-7.8, CN-7.9, CN-2.1, CN-4.2).
> **Sede**: **CLI** (GOV-SURFACES-01) — sessione Claude Code CLI su `C:\`. Audit documentale **no-DAPI**, divieto CLI attivo (nessuna probe di zelo). Lista "Empirico-CLI da verificare" attesa **vuota**.
> **Letture obbligatorie eseguite**: `tasks/METODO.md` (RM-1..RM-4 + RACC-METODO-2), `.claude/BASE_COMUNE.md`, `.claude/agents/spec_reviewer.md`, `tasks/ACTIVE_TASK.md` (card B5). Confermo.

---

## VERDETTO (iterazione 1): **PASS**

0 problemi bloccanti, **0 BUG REALE** in tabella. Floor citazioni 100% pulito (47/47 risolvono token-per-token al CAP frozen). Confronto-copertura: 11/11 req-v2 del perimetro B5 coperti, 0 sconfinamenti, 0 orfani. Cecità preservata. 1 osservazione non-bloccante classificata **MIGLIORA PERFORMANCE** (tracciabilità di processo su M-GOV-1) + 1 osservazione **NEUTRO** (editoriale). Nessuna delle due è BUG REALE → il verdetto resta PASS (BASE_COMUNE §4: il mapping verdetto↔classificazione vieta il PASS solo in presenza di ≥1 BUG REALE).

---

## 1. Tabella verifica Acceptance Criteria (audit indipendente, non sulla parola del REPORT)

| AC-ID | Esito | Evidenza (file:riga) |
|-------|-------|----------------------|
| AC-G1 (atomicità N1) | OK | Ogni requisito = 1 proposizione. Concern impacchettati spezzati genuinamente: gating in B5-R-16/CN-07/CN-08/NFR-02/R-17/CN-09 (§5); retention in B5-NFR-05/NFR-06 (§6); lifecycle-log in B5-R-19/R-20 (§6). Nessun over-split artificiale rilevato (vedi §4 punti di attenzione). |
| AC-G2 (tracciabilità a riga CAP_09/CAP_01) | OK | Ogni requisito porta `[DOC-INTERNO CAP_09_parte_9.md:<riga>]`; matrice §7.1 completa (35 righe). |
| AC-G3 (valore operativo / di sistema-replay) | OK | Campo *Valore* su ogni requisito + colonna §7.1. |
| AC-G4 (divieto "verificato X" RM-1) | OK | Nessun "verificato" auto-prodotto di prima istanza; B5-CN-03 cita la verifica parziale come tale (vedi §4). |
| AC-G5 (etichette RM-3 / wiki) | OK | §7.5: `[WIKI-HINT, da verificare]` salvo PROVA-EMPIRICA; nessuna conclusione strutturale da solo livello-4 (vedi AC-B5-3). |
| AC-G6 (grafia canonica) | OK | `[DOC-INTERNO]`/`[PROVA-EMPIRICA]`/`[WIKI-HINT, da verificare]` canonici; nessuna grafia deprecata `[CODICE-EXISTENTE]`. |
| AC-G7 (**floor citazioni 100%**) | OK | 47/47 citazioni risolvono al CAP frozen token-per-token — vedi §2. |
| AC-G8 (cecità preservata) | OK | §1.3 + testa REPORT. Grep su `CAP_01_parte_I`, ID v2 (`R-7.*`/`CN-*`), "chunking", "B1/B2/B3/B4": **0 tracce importate** nel corpo requisiti (i riferimenti `B1..B8` compaiono solo in §7.2 nota-di-rinvio come *premesse*, uso ammesso dalla card §1). |
| AC-G9 (scope "tutto e solo" perimetro §1) | OK | §7.3 fuori-scope con destinazione; §7.2 premesse non consolidate; nessun requisito su Cap.45/50/27-28 (§4). |
| AC-G10 (matrice + nota di rinvio) | OK | §7.1 matrice + §7.2 nota di rinvio + §7.3 fuori-scope + §7.4 PENDING + §7.5 RM-3. |
| AC-G11 (invarianti come tali) | OK | Invarianti marcati `B5-CN-*` con valore "di sistema/replay". |
| **AC-B5-1** (premesse, non ri-derivazioni) | OK | **0 requisiti B5 su Cap.27-28** (grep confermato); dualità 5€/B1, gating-su-messaggio/B4, lifecycle-SM/B3, epoca-E5/B8, schema-dato/B6 tutti **citati** in §7.2, **mai consolidati** in un requisito. Vedi §3. |
| **AC-B5-2** (PENDING-empirico marcato) | OK con osservazione | I 3 noti (Mar/Dic, rollover V-3, calendario V-2) marcati PENDING §7.4; PROVA-EMPIRICA 2026-05-27 (banner, porte, F/I) non sovra-marcate. **Osservazione MIGLIORA su M-GOV-1**, vedi §5 — non inficia l'AC (il valore finestra è correttamente non-pending per esplicita prescrizione della card §2). |
| **AC-B5-3** (RM-3 wiki Directa) | OK | §7.5: porte/banner/convenzioni wiki = `[WIKI-HINT, da verificare]` salvo PROVA-EMPIRICA; nessuna conclusione strutturale su solo wiki. |

---

## 2. Esito floor citazioni 100% (token-per-token contro CAP frozen)

Aperti con Read `CAP_09_parte_9.md` (righe 20-110, 265-380) e `CAP_01_parte_I.md` (intero). Ogni `[DOC-INTERNO ...:riga]` verificato contro il costrutto asserito. **47/47 risolvono.** Campione delle verifiche più delicate:

| Requisito | Pin | Costrutto nel CAP (verificato) | Esito |
|-----------|-----|-------------------------------|-------|
| B5-R-01 | :27 | "si connette al gateway esclusivamente in loopback su `127.0.0.1`, mai da rete esterna" | MATCH |
| B5-R-02 | :35 | tabella porta `10001` Datafeed realtime IN scope (PRICE/BOOK_5/ANAG) | MATCH |
| B5-R-03 | :37 | porta `10003` storico (CANDLERANGE/CANDLE/TBT/TBTRANGE), warm-up ≤100gg | MATCH |
| B5-CN-01 | :39 | "La porta `10002` non e' mai aperta dalla pipeline runtime" | MATCH |
| B5-R-04 | :29 | prefix-match su `DARWIN_STATUS;CONN_OK;TRUE;Release ...`, non match esatto; banner registrato in audit. PROVA-EMPIRICA 2026-05-27 alla :29 (`Appendice A`) | MATCH |
| B5-NFR-01 | :41,43 | `APIPortSettings.txt` sola lettura, dato PII, escluso dal repo via `.gitignore` | MATCH |
| B5-CN-02 | :45 | D-6: no workaround automatici, `RUNTIME_DEGRADED`, notifica Telegram, esce; rimedio del supervisore | MATCH |
| B5-CN-03 | :47,51 | una connessione persistente per porta; soglia "14 conn/~30s" = verifica parziale RM-1, smentita nel regime ~1Hz | MATCH (vedi §4) |
| B5-R-07 | :61 | `F`=giugno (PROVA-EMPIRICA M-4 2026-05-29), `I`=settembre (2026-05-27); Mar/Dic da derivare via ANAG | MATCH |
| B5-R-08 | :98,104 | switch al next-month al boot del giorno di scadenza, salta 08:00-09:00; "nessuna SUB del front in scadenza" (:104) | MATCH |
| B5-R-09 | :103 | marker `CONTRACT_SWITCH` payload `{from,to,scadenza_from,trigger:"boot_session_third_friday"}` | MATCH |
| B5-CN-04 | :107 | switch runtime (da `t` sul next) distinto dal filtro pre-expiry training N=3 (Cap.39) | MATCH |
| B5-CN-05 | :292,302 | "Un segnale in stato `active` alla chiusura 22:00 CET non viene chiuso automaticamente"; Δt fino a 1680 min scavalca la notte | MATCH |
| B5-CN-06 | :292 | stato `active` mantenuto in memoria persistente fuori sessione; ripreso al boot, transizione al primo boot utile se Δt scaduto fuori sessione | MATCH |
| B5-R-13 | :294,299 | apertura 08:00: banner+warm-up+SUB; marker `SESSION_OPEN` con timestamp UTC e data sessione | MATCH |
| B5-R-14 | :302 | `SESSION_CLOSE` + UNSUB cash + conservazione connessione storica | MATCH |
| B5-CN-07 | :311 | "Il gating non sopprime mai l'emissione: il segnale e' sempre emesso ... `SIGNAL_EMITTED`" | MATCH |
| B5-CN-08 | :315,316,317,318 | cash NON entra in feature tensor / state machine / cromosoma / walk-forward | MATCH (4 pin → 4 costrutti distinti) |
| B5-CN-09 | :328 | replay bit-exact preservato; solo `nota_gating` può variare; metriche lifecycle non inquinate | MATCH |
| B5-R-19 | :353,355 | 6 terminali distinti che sostituiscono `SIGNAL_CLOSED` (NB-3 Opzione A) | MATCH |
| B5-R-20 | :355 | `timeout_cause ∈ {pretrigger, posttrigger}` campo obbligatorio su SIGNAL_MISSED_TARGET | MATCH |
| B5-NFR-04 | :357,358 | banner loggato in HANDSHAKE; account code PII mascherabile negli export, in chiaro nel log locale | MATCH |
| B5-NFR-05/06 | :364,365 | retention 90gg rolling (:364) + permanente sui giorni di emissione (:365) | MATCH |
| B5-NFR-07 | :373,376,377 (+:375 per D-1) | tolleranza 20€/mese sotto 200€, notifica mensile Telegram, nessuna azione automatica; D-1 distinto (:375) | MATCH |

**Nota su CAP_01**: il documento **non cita mai** `CAP_01_parte_I.md:<riga>` come tracciabilità di un requisito. Cap.1 è richiamato **solo testualmente** come premessa ("vive in `CAP_01 Cap.1`/Cap.9", B5-CN-01; §7.2). Verificato che Cap.1 (`CAP_01_parte_I.md:15`) fonda effettivamente "Il sistema non esegue ordini autonomamente ... il motore pubblica segnali ... la decisione ... competono esclusivamente all'operatore" — premessa correttamente attribuita, non consolidata in B5. Coerente con la card (Cap.1 = inquadramento, verosimilmente 0 req propri).

---

## 3. Esito confronto-copertura (modalità B — perimetro B5 = 11 req-v2 della mappa `c7ce4be`)

Mappatura req-v2 (contenuti letti da `SPEC_FUNZ_01.md` §11 e definizioni Sez.7/2/4) → requisito/i B5:

| Req-v2 (perimetro B5) | Coperto da | Esito |
|-----------------------|------------|-------|
| **R-7.1** (finestra 08:00-22:00, stand-by) | B5-R-11, B5-R-12 | COPERTO |
| **R-7.2** (boot scadenza, next-month, CONTRACT_SWITCH) | B5-R-08, B5-R-09 (+ B5-R-06 derivazione front-month) | COPERTO |
| **CN-7.1** (non instrada ordini, separazione segnale/esecuzione) | B5-CN-01 (porta 10002) + B5-R-10 (esecuzione operatore) + §7.2 premessa B1/B2 | COPERTO |
| **CN-7.2** (DAPI porte 10001/10003 scope, 10002 mai aperta) | B5-R-02, B5-R-03, B5-CN-01 | COPERTO |
| **CN-7.5** (codici mese proprietari, F/I, altri via ANAG) | B5-R-07 | COPERTO |
| **CN-7.6** (audit JSONL append-only, retention 90gg + permanente) | B5-NFR-03, B5-NFR-05, B5-NFR-06 | COPERTO |
| **CN-7.7** (granularità per-stato, 6 terminali) | B5-R-19 (+ B5-R-18 contenuto loggato) | COPERTO |
| **CN-7.8** (account PII, gitignore, masking) | B5-NFR-01, B5-NFR-04 | COPERTO |
| **CN-7.9** (cash logging + gating post-emissione, fuori-GA) | B5-R-15, B5-R-16, B5-CN-07, B5-CN-08 (+ NFR-02, R-17, CN-09) | COPERTO |
| **CN-2.1** (dualità miniFIB 1€ / FIB-pieno 5€) | B5-R-10 | COPERTO |
| **CN-4.2** (22:00 non chiude active) | B5-CN-05 (+ B5-CN-06 persistenza notturna) | COPERTO |

**Copertura: 11/11. Buchi: 0.**

**Sconfinamenti / fuori-perimetro: 0.**
- **CN-7.3** (commissioni 5€/op di trade) e **CN-7.4** (gestione post-fill) — la mappa li assegna a B1/B3. **Non compaiono come requisiti B5.** Correttamente rinviati in §7.3 ("Esecuzione/gestione attiva post-fill, commissioni di trade (5€/op) → B3/B1 — già coperti"). Verificato che B5-NFR-07 tratta le **commissioni del servizio DAPI Datafeed (20€/mese, Cap.54 Gap-6)**, materia ortogonale e in-perimetro Sez.7, **non** le commissioni di trade 5€/op (CN-7.3). Distinzione netta, nessuna confusione.
- I requisiti B5 "extra" rispetto agli 11 (B5-R-04 banner, B5-CN-02 D-6, B5-CN-03 connessione persistente, B5-R-06 ANAG, B5-CN-04, B5-R-13/14 marker sessione, B5-NFR-02/R-17/CN-09 gating, B5-R-18/R-20 audit, B5-NFR-07 DAPI-fee) sono **espansioni granulari** di materia interna ai capitoli del perimetro (Cap.46/47/52/53/54), non requisiti di blocchi vicini. Tutti tracciano a righe in-perimetro. Nessuno traccia a Cap.45 (11-24), Cap.50 (195-270) o Cap.27-28.

---

## 4. Esito punti di attenzione (boundary-check Orchestratore)

| Punto | Esito |
|-------|-------|
| **Cap.45 (premessa) e Cap.50 (errori/recovery): nessun requisito proprio** | **OK.** Nessun pin di un requisito B5 cade in Cap.45 (righe 11-24) o Cap.50 (righe 195-270). B5-R-01 traccia a `:27` = Cap.46 (non Cap.45). B5-CN-02 (D-6) traccia a `:45` = Cap.46 (non Cap.50). §7.3 dichiara esplicitamente "Errori/recovery/riavvio Darwin (Cap.50) → contesto runtime, non fonda requisiti di Sez.7". Nessun gonfiaggio di recovery. |
| **Granularità 35 req per ~11 req-v2: over-split?** | **OK — split genuino.** I 35 nascono da espansione atomica N1 (un req-v2 multi-concern → più requisiti verificabili separatamente). Esempi controllati: CN-7.9 (gating) → 6 requisiti che colpiscono concern distinti (annotazione vs non-soppressione vs fuori-GA vs config vs marker-audit vs replay); CN-7.6 (audit) → NFR-03 (formato) + NFR-05 (90gg) + NFR-06 (permanente). Nessun requisito è una ri-frase cosmetica di un altro. |
| **B5-CN-03 (connessione persistente / soglia "14 conn/~30s")** | **OK.** B5-CN-03 cita la soglia come **"verifica parziale RM-1, smentita come costante nel regime ~1Hz"** `[CAP_09:47,51]`, e fonda il requisito sulla scelta architetturale (connessione persistente) **indipendente** dalla soglia. Riproduce fedelmente la cautela RM-1 del CAP (righe 47/51: "la cifra '14ª connessione/~30 s' NON è una costante verificata"). Non asserita come costante. |

---

## 5. Problemi non-bloccanti / osservazioni

### OSS-1 — [MIGLIORA PERFORMANCE] M-GOV-1/B-2 (sessione 08:00-22:00) non reso visibile come M aperto su B5-R-11

**Fatto.** `tasks/CARRYOVER.md:37` registra **M-GOV-1 come APERTO**: l'orario 08:00-22:00 CET è *fissato* (decisione AC 13/06/2026 + WIKI-HINT Borsa Italiana concordante), ma l'**upgrade del livello-fonte a `[PROVA-EMPIRICA]`** (primo/ultimo trade da tape DAPI) resta da fare al probe V-1. La v2 congelata marca il requisito corrispondente **`R-7.1 [B-2 PROVVISORIO]`** (`SPEC_FUNZ_01.md:304,359`). La mappa di chunking prescrive per B5 (riga 207 + `STATO_CORRENTE:33` "eredita M-GOV-1 OPEN"): *"recepire `[B-2 PROVVISORIO]`, non chiudere"*. Il requisito B5 corrispondente è **B5-R-11** (finestra 08:00-22:00), che **non porta alcun marcatore di provvisorietà** e traccia solo a `[CAP_09:273]`. §7.4 marca PENDING-empirico una cosa **diversa** (la convenzione calendario/festività via V-2), e §7.4 nota finale dichiara esplicitamente "Non sono pending: il valore della finestra 08:00-22:00".

**Perché NON è un BUG REALE** (e perché non blocca il PASS):
1. **La card §2 AC-B5-2 è autoritativa e prescrive l'esatto trattamento adottato**: *"Il valore della finestra 08:00-22:00 ... non sono pending: cita lo stato empirico esatto, non sovra-marcare"* (`ACTIVE_TASK.md:53`). Il Developer ha seguito la card alla lettera. Un Reviewer non può trasformare in BUG l'aderenza fedele a un AC esplicito della card.
2. **Il valore 08:00-22:00 non è incerto**: M-GOV-1 dice "orario FIB **fissato**"; ciò che è OPEN è solo l'*upgrade di livello-fonte* (da [decisione-AC + WIKI-HINT] a [PROVA-EMPIRICA]), non il numero. B5-R-11 traccia fedelmente al CAP frozen `:273` che asserisce la finestra come fatto normativo (epoca E5, in vigore dal 2020-02-17) senza etichetta di provvisorietà.
3. **Precedente B4 (chiuso PASS)**: l'analogo M-2/B-1 (latenza Telegram, OPEN) è stato recepito in B4 come **PENDING-empirico** (B4-NFR-04), **non** con marcatore `[B-1 PROVVISORIO]` (`STATO_CORRENTE:22`). B5 segue lo stesso pattern consolidato: `[B-N PROVVISORIO]` è convenzione interna della v2, i blocchi della ricostruzione cieca usano PENDING-empirico/citazione-di-stato.

**Perché vale comunque segnalarlo (MIGLIORA)**: a differenza di B4 (dove la latenza È marcata PENDING perché il valore stesso è da verificare), in B5 il documento **non rende visibile da nessuna parte** che M-GOV-1 è ancora OPEN su B5-R-11 — l'unico segnale di stato-fonte sull'orario è il pin nudo `[CAP_09:273]`. Il lettore non sa che l'upgrade a PROVA-EMPIRICA da tape DAPI è pendente. Una riga in §7.5 o una nota inline su B5-R-11 del tipo *"orario 08:00-22:00 = decisione-AC + WIKI-HINT concordante; upgrade a [PROVA-EMPIRICA] da tape DAPI pendente — M-GOV-1 OPEN, CARRYOVER"* chiuderebbe il gap di tracciabilità di processo senza contraddire la card (resta non-PENDING come *valore*, ma esplicita lo stato-fonte). **Decisione di instradamento al supervisore** (non va a Developer senza approvazione AC, BASE_COMUNE §4).

### OSS-2 — [NEUTRO] B5-NFR-07: doppio uso del termine "commissioni"

B5-NFR-07 usa "commissioni mensili < 200 EUR" (soglia di gratuità DAPI) nello stesso requisito che la §7.3 distingue dalle "commissioni di trade 5€/op" (CN-7.3 → B1). Il requisito è corretto e fedele al CAP (`:373`), ma il termine "commissioni" è sovraccarico nel documento (servizio-dato vs trade). Puramente editoriale, nessun impatto su correttezza o tracciabilità. NEUTRO (non va a Developer).

---

## 6. Esito audit cecità (AC-G8)

Cecità **preservata**. Grep nel corpo requisiti per: ID v2 (`R-7.*`, `CN-7.*`, `CN-2.1`, `CN-4.2` come *etichette-requisito*), stringhe "chunking" / "PROPOSTA_SUDDIVISIONE" / "v2 congelata come fonte" / "SPEC_FUNZ_01.md". Esito: i riferimenti ai blocchi `B1..B8` compaiono **esclusivamente** nella §7.2 "nota di rinvio" come **premesse citate** (uso esplicitamente ammesso dalla card §1 CARDINE e da AC-G9), mai come fonte-contenuto di un requisito. Nessun ID-requisito v2 né numerazione v2 importati. Gli ID `B5-*` sono auto-assegnati contigui (R-01..R-20, CN-01..CN-09, NFR-01..NFR-07). **Nessuna traccia v2/B*/chunking importata come contenuto = nessun BUG REALE di cecità.**

---

## 7. Tabella "Classificazione per il supervisore"

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|------------------------|
| 1 | M-GOV-1/B-2 (sessione 08:00-22:00 OPEN) non reso visibile come M aperto su B5-R-11: l'unico segnale di stato-fonte è il pin nudo `[CAP_09:273]`. Gap di tracciabilità di processo (valore correttamente non-pending, ma upgrade a PROVA-EMPIRICA da tape DAPI pendente non esplicitato). | `SPEC_FUNZ_01_B5.md:123-126` (B5-R-11) + §7.4/§7.5 | **MIGLIORA PERFORMANCE** | In attesa decisione AC (micro-pass se approvato). NON è BUG REALE: il trattamento segue l'AC-B5-2 esplicito della card e il precedente B4. |
| 2 | Termine "commissioni" sovraccarico (servizio-dato DAPI 20€ vs trade 5€/op) in B5-NFR-07. Editoriale. | `SPEC_FUNZ_01_B5.md:231-234` | **NEUTRO** | No (mai, salvo esplicita richiesta AC). |

**0 BUG REALE.** → verdetto **PASS** (BASE_COMUNE §4: il blocco al PASS scatta solo con ≥1 BUG REALE in tabella).

---

## 8. Applicazione RM-1 a me stesso

- **"47/47 citazioni risolvono token-per-token"** — PROVE: aperti con Read `CAP_09_parte_9.md` righe 20-110 e 265-380 (coprono tutti i pin citati :27..:107 e :273..:377) e `CAP_01_parte_I.md` intero; confronto diretto pin↔costrutto in tabella §2. ALTERNATIVE NON ESCLUSE: **nessuna** — ho letto le righe esatte, non inferito dal contesto. Limite dichiarato: ho letto i blocchi 20-110 e 265-380; le righe 110-265 (Cap.48-51) non sono citate da alcun requisito B5 (verificato che i pin di §7.1 sono tutti ≤107 o ≥273), quindi non rilevanti al floor.
- **"Copertura 11/11, 0 sconfinamenti"** — PROVE: contenuti dei 11 req-v2 letti da `SPEC_FUNZ_01.md` §11 (grep righe 304-345, 536-579) + mappa `c7ce4be` (riga 107/139); mappatura esplicita req-v2→B5 in §3. ALTERNATIVE ESCLUSE: CN-7.3/CN-7.4 verificati **assenti** dal corpo B5 via grep (`commission|gestione attiva|post-fill` → solo B5-NFR-07 [DAPI-fee, materia diversa] e §7.3 [rinvio]). 
- **"0 requisiti B5 su Cap.27-28 / Cap.45 / Cap.50"** — PROVE: grep `Cap.27|Cap.28|EGARCH|feature tensor` nel doc → riga 102 (valore/motivazione di B5-R-08, non requisito su EGARCH) e riga 173 (B5-CN-08, materia Cap.53 non Cap.27-28); nessun pin in 11-24 o 195-270. ALTERNATIVE NON ESCLUSE: nessuna.
- **"M-GOV-1 è APERTO ed è classificato MIGLIORA non BUG"** — PROVE: `CARRYOVER:37` (APERTO), `ACTIVE_TASK.md:53` (card prescrive valore-finestra non-pending), `STATO_CORRENTE:22` (precedente B4 = PENDING non `[B-1]`). La classificazione poggia sull'autorità della card + precedente chiuso PASS, non su mia preferenza. ALTERNATIVE CONSIDERATE: "BUG REALE per (F6) marcatore mancante" — **esclusa** perché (F6) richiede il marcatore per requisiti dipendenti da un blocco aperto *nel senso della card/REPORT*, e la card ha esplicitamente normato questo caso come non-PENDING; trasformarlo in BUG contraddirebbe un AC esplicito.

---

## 9. Lista "Empirico-CLI da verificare"

**VUOTA** (attesa). La spec consolida fatti già chiusi nei CAP frozen; non introduce fatti empirici nuovi. I 3 PENDING-empirico (Mar/Dic, rollover V-3, calendario V-2) e l'upgrade M-GOV-1 (V-1) sono **già marcati come non-verificati** dal documento/CARRYOVER e restano in carico al validator/FASE-D — **non** sono asserzioni da riprodurre in CLI da parte del Reviewer (divieto CLI: niente probe di zelo, no-DAPI).

---

*Review iterazione 1 — sede CLI. Verdetto PASS. 0 BUG REALE; 1 MIGLIORA PERFORMANCE (instradamento a decisione AC), 1 NEUTRO. Floor citazioni 100% pulito (47/47). Copertura 11/11 req-v2, 0 buchi, 0 sconfinamenti. Cecità preservata. DEV_STATUS non azzerato (lo fa l'Orchestratore alla chiusura). Nessuna modifica a CAP (frozen) né alla spec.*
