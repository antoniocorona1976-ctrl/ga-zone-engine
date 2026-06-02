# Review SPEC-FUNZ-01 — Specifica funzionale del prodotto-segnale FIB (PHASE-1)

**Verdetto**: PASS

**Perimetro**: `docs/spec_funzionale/SPEC_FUNZ_01.md` (Developer v1, commit `e08409b`). Cross-check onestà claim→evidenza: `reports/REPORT_SPEC_FUNZ_01.md`.
**Sede**: WEB — audit statico (documento + grep + Read dei CAP/decoder committati). Nessuna esecuzione DAPI. Lista "Empirico-CLI da verificare": **VUOTA** (atteso — la spec consolida fatti già chiusi, non introduce fatti empirici nuovi).
**Modalità**: CAP-review piena adattata al non-CAP. Due giri ostili.
**Asse di impatto** (reinterpretazione "orientamento al GA" per documento di prodotto): (1) fedeltà di tracciabilità, (2) assenza di contraddizioni con CAP chiusi, (3) conformità RM-1/2/3, (4) completezza vs AC, (5) valore operativo per requisito.

---

## Sintesi

La spec è **tracciabilmente solida**. Ho aperto i CAP referenti e verificato un campione esteso (>50 citazioni `[DOC-INTERNO]` su CAP_01/02/06/07/08/09/10 + le 3 citazioni `[CODICE-ESISTENTE]` token-per-token + gli ID decisione D-9-2/15/NB2/NB3/NB4, D-10-3/4/5/8/9/10 contro le tabelle Cap.56/Cap.65 + M-9/M-10 contro STATO_CORRENTE). **Ogni citazione campionata risolve** al capitolo/decisione corretto e l'asserzione referente è effettivamente presente. Nessuna contraddizione con un fatto/decisione chiuso (AC-G6). Nessuna dichiarazione "verificato X" di prima istanza (AC-G1). Fonti esterne etichettate (AC-G2). 36 requisiti, tutti tracciati e con valore operativo dichiarato (AC-G4/G7). Matrice a 36 righe (AC-G5). Lunghezza 6443 parole ≈ 13-14 pp (AC-G10). Il REPORT è onesto: gli AC dichiarati OK hanno evidenza reale.

**0 problemi bloccanti. 0 BUG REALE. Le osservazioni sotto sono tutte NEUTRO** (imprecisioni di citazione di tipo "puntatore a riga di intestazione capitolo anziché alla riga esatta dell'asserzione", e una formulazione lasca disambiguata in-linea). Non cambiano la correttezza della spec né la sua tracciabilità sostanziale, e non vanno a Development per default.

---

## Problemi bloccanti (causano FAIL)

Nessuno.

---

## Problemi non bloccanti (causano CONDITIONAL)

Nessuno.

---

## Osservazioni minori (NEUTRO — non bloccanti, non a Development per default)

### OM-1 — Cluster di imprecisioni di citazione in Sez. 9/10 (puntatore a riga di intestazione/adiacente)

Diverse citazioni inline puntano alla **riga di intestazione del capitolo** o a una riga **adiacente** invece che alla riga esatta che contiene l'asserzione. In tutti i casi la citazione **risolve al capitolo corretto** e il costrutto asserito **è realmente presente** in quel capitolo (verificato con Read), quindi non è una citazione "che non risolve" (non è BUG REALE per il criterio di priorità #1). Dettaglio:

| Citazione nella spec | Riga citata (contenuto reale) | Riga esatta dell'asserzione |
|---|---|---|
| `[DOC-INTERNO CAP_10_parte_10.md:11]` (Sez.9.2 research=runtime esteso al tape) | r11 = header "Capitolo 57 — Premessa" | r5 (invariante esteso al ciclo di vita del tape) |
| `[DOC-INTERNO CAP_10_parte_10.md:74]` (R-22, Cap.59) | r74 = header "Capitolo 59" | r76 (limite ~100gg stabilito empiricamente) |
| `[DOC-INTERNO CAP_10_parte_10.md:151]` (R-22, Cap.61) | r151 = header "Capitolo 61" | r151+ (fallback Portara nel corpo del cap) |
| `[DOC-INTERNO CAP_10_parte_10.md:226]` (Sez.10.1 PHASE-2 fuori scope) | r226 = header "Capitolo 64" | r236 (Convenzione cross-index PHASE-2 fuori scope PHASE-1) |
| `[DOC-INTERNO CAP_10_parte_10.md:234]` (Sez.10.3 voce 4 "riavvio Darwin mezzanotte") | r234 = estensione immutabilità barre | r233 (Riavvio Darwin mezzanotte, residuo Empirico-CLI) |
| `[DOC-INTERNO CAP_07_parte_VII.md:574]` (NFR-4, tag "AC-GO-4") | r574 = AC-GO-3 (expected net return) | r576 (AC-GO-4 lifecycle cross-regime) |

Nota: il **tag testuale** è sempre corretto (es. "(AC-GO-4)", "(Cap.59)", "(Cap.61)") e l'asserzione esiste nello stesso capitolo/checklist a poche righe di distanza. L'impatto è nullo sulla tracciabilità sostanziale (un lettore che apre il capitolo trova il costrutto); è solo una perdita di precisione "riga-esatta" rispetto allo standard di citazione puntuale tenuto altrove nella spec (Sez. 1-8, dove le citazioni a riga esatta sono accurate). **Classificazione: NEUTRO.** Se il supervisore desidera la massima igiene di citazione, un fix chirurgico (sostituire i 6 numeri di riga con quelli esatti) è opzionale; non è richiesto per la correttezza.

### OM-2 — R-17 (Sez. 6) "Singolo segnale attivo **per direzione**" — formulazione lasca disambiguata in-linea

R-17 titola "Singolo segnale attivo **per direzione**", ma il vincolo chiuso (Cap.6.3 / Cap.28 Parte VI, `[DOC-INTERNO CAP_02_parte_II.md:81]`) è $|\mathcal{A}(t)|\le 1$ **globale** (un solo segnale attivo in assoluto, non uno per direzione; cfr. CAP_02:87 "elimina tutte le politiche multi-segnale concorrente"). La locuzione "per direzione", presa isolata, potrebbe suggerire $|\mathcal{A}|\le 2$ (un long + uno short). **Tuttavia** R-17 enuncia immediatamente in-linea la forma corretta "$|\mathcal{A}(t)|\le 1$: nessuna politica multi-segnale concorrente", che è il vincolo vincolante e coincide col CAP. R-7 (Sez. 3.2) lo enuncia correttamente senza "per direzione". Poiché la formula governa ed è quella giusta, non c'è contraddizione sostanziale con il CAP (AC-G6 regge): l'asserzione operativa pubblicata è corretta. **Classificazione: NEUTRO** (wording opportunisticamente ripulibile cancellando "per direzione" dal titolo di R-17; non BUG REALE perché il constraint è dichiarato giusto accanto).

### OM-3 — Provenienza dell'indicizzazione `f4/f6/f8/f9` dello schema PRICE (Sez. 9.2)

Sez. 9.2 cita lo schema PRICE come "`f4=last`/`f6=volume_cum`/`f8=day_low`/`f9=day_high`, M-9 `[DOC-INTERNO CAP_09_parte_9.md:94]`". L'**indicizzazione `fN` esatta** proviene da **M-9 in `tasks/STATO_CORRENTE.md:76`** (`PRICE;<tk>;<HH:mm:ss>;<f4=last>;<f5>;<f6=volume_cum>;<f7>;<f8=day_low>;<f9=day_high>`), riprodotta dalla spec **token-per-token** (corretta). La riga citata `CAP_09_parte_9.md:94` riporta lo stesso schema in forma **descrittiva** (`...;<last>;<volume_lot?>;<bid_qty?>;<ask_qty?>;<low_session>;<high_session>`), coerente con M-9 (last dopo time; low/high in coda). Quindi la citazione non è errata (l'ancora DOC-INTERNO è il capitolo che descrive lo schema; il valore è corretto), ma l'ancora più puntuale per la numerazione `fN` sarebbe `STATO_CORRENTE.md:76`. **Classificazione: NEUTRO** (fatto corretto e tracciabile; ancora aggiuntiva opzionale).

---

## Citazioni problematiche dal testo

Nessuna citazione **errata** (cioè che non risolve, capitolo sbagliato, o costrutto assente). Le uniche imprecisioni sono di tipo "puntatore a riga di header/adiacente" elencate in OM-1, tutte risolventi al capitolo corretto con costrutto presente. Non si configura alcuna citazione `[CODICE-ESISTENTE]` o `[DOC-INTERNO]` falsa.

---

## Verifiche positive principali (a sostegno del PASS)

### Fedeltà di tracciabilità (PRIORITÀ #1) — campione esteso, tutto risolve

**Citazioni di codice `[CODICE-ESISTENTE]` (RM-2 / AC-G3 / RACC-METODO-2) — riverificate token-per-token con Read:**
- `scripts/export_directa_history_parametric.py:467-481` → `parse_directa_candle`: r471 `kind, symbol, ymd, hms, uff, min_, max_, ape, qty = parts[:9]`; r477 commento `# UFF, MIN, MAX, APE => close, low, high, open`; r478-481 `close_v=Decimal(uff)`/`low_v=Decimal(min_)`/`high_v=Decimal(max_)`/`open_v=Decimal(ape)`. **Schema CANDLE `C;L;H;O` confermato (MATCH).**
- `scripts/export_directa_history_parametric.py:605-617` → header CSV legacy: `symbol, timeframe, timestamp, date, time, open, high, low, close, volume, source` = **11 campi** senza `tick_count`/`bar_synthetic`. **MATCH** (la spec R-20 e la self-review (b) lo dichiarano "11 campi": corretto).
- `scripts/export_directa_history_parametric.py:61` → `DEFAULT_INTRADAY_MAX_DAYS = 100`. **MATCH.**
- Grep di controllo (RACC-METODO-2): i decoder nel repo sono solo `export_directa_history_parametric.py` (citato, canonico) e `probe_dapi.py` (non necessario alla spec: nessuna asserzione della spec dipende da esso; gli schemi citati provengono tutti dal decoder canonico). **Nessun decoder mancante.** ≤5 citazioni codice (3 distinte): AC-G3 OK.

**Campione `[DOC-INTERNO]` aperto e verificato (estratto):**
- "solo emissione" CN-1/R-1/R-2 → `CAP_01_parte_I.md:15` (MATCH); 80pt R-8 → `CAP_01_parte_I.md:83` + `CAP_02_parte_II.md:55` (MATCH); tick 5pt R-9 → `CAP_02_parte_II.md:9` (MATCH); $E[R_{net}]$ → `CAP_01_parte_I.md:73` (MATCH formula esatta).
- Tabella payload (Sez.3.1): i 10 campi mappano esattamente alle righe `CAP_02_parte_II.md:23/25/27/29/35/37/39/41/51/53`; target_2 "informazione strutturale pubblicata, non variabile di lifecycle (Q-05 Clausola 2)" → `:37` (MATCH esatto). Distinzione 9 voci pubblicate / 10 campi consumer-facing / 12 campi tupla formale: coerente con `:241`/`:253`/`:19` e con CAP_07:21 ("12 campi della tupla"). **Nessuna ambiguità introdotta.**
- State machine 1+6 (Sez.4): `CAP_02_parte_II.md:95` "un solo stato non-terminale e sei stati terminali (Q-05, Clausola 1)" (MATCH esatto); i 6 terminali → `:101`-`:111` (tutti MATCH); trigger_event evento-non-stato → `:139` (MATCH).
- 6 marker normativi CN-2 → `CAP_09_parte_9.md:353` + D-9-NB3 (r434): elenco `SIGNAL_TARGET_1_HIT/STOPPED/INVALIDATED/MISSED_TARGET/EXPIRED/REVOKED` (MATCH esatto).
- Rollover R-19 (D-9-NB2): `CAP_09_parte_9.md:98`/`:103` + D-9-NB2 (r433): switch al boot del giorno di scadenza, salto finestra 08:00-09:00, marker `CONTRACT_SWITCH {from:FIB6F,to:FIB6I,scadenza_from:2026-06-19}`, F=giugno/I=settembre (r61). Esempio FIB6F→FIB6I al 2026-06-19 (terza venerdì giugno 2026): **MATCH**.
- $L_{warmup}=30$gg R-24 (D-9-NB4): `CAP_09_parte_9.md:435` + D-10-5 `CAP_10_parte_10.md:252` (MATCH).
- Riconciliazione bloccante R-23 (D-10-3/4): `CAP_10_parte_10.md:250`/`:251` "gate **bloccante** sull'emissione $d+1$, a differenza del monitoraggio non bloccante di Parte VI Cap.30"; low/high cash via CANDLE ufficiale `f8`/`f9` (D-10-4). **MATCH esatto**, inclusa la contrapposizione con Cap.30 non-bloccante. (Confermato indipendentemente anche dall'indice r101.)
- Gate go-live (Sez.7): AC-GO-1 DSR $>\theta_{DSR}=0{,}95$ → `CAP_07_parte_VII.md:570` (MATCH); AC-GO-2 PBO $<\theta_{PBO}=0{,}50$ → `:572` (MATCH); $\theta_{MDD}=200$pt → AC-GO-7 `:582` (MATCH, valore provvisorio); target 500pt/g OR 70% → AC-GO-9 `:586` (MATCH); checklist 12 AC → `:566`-`:601`; NFR-1 latenza + M-2 Appendice E + AC-GO-10 → `:23`/`:592` (MATCH esatto).
- PHASE-2 fuori scope R-3 → `CAP_08_parte_8.md:167` (MATCH); Portara unica fonte training → `CAP_08_parte_8.md:13` (MATCH).
- Retention CN-5 (Gap-4/D-9-15) → `CAP_09_parte_9.md:362` + D-9-15 (r430): 90gg rolling + permanente sui giorni di emissione (MATCH); PII account code CN-6 → `:358` (MATCH esatto); porta 10002 mai aperta CN-4 (D-9-2) → `:39` + D-9-2 (r417) (MATCH); gating cash Q-A-3 CN-7 → `:308` + D-9-14 (MATCH).

### AC-G6 — nessuna contraddizione con CAP chiusi
Verificati per scrupolo i 9 punti rischiosi (vincolo solo emissione, state machine 1+6, target_2 informazione, 80pt minimo, tick 5pt, sessione 8-22 CET, M-2 ancora OPEN, $L_{warmup}=30$gg, riconciliazione bloccante vs Cap.30). **Tutti coerenti col CAP referente.** Dove la spec tocca notazioni del corpus chiuso (es. f8/f9 su CANDLE in D-10-4) **riproduce fedelmente la decisione chiusa**: in coerenza con AC-G14 non riapro il CAP; non c'è difetto della spec.

### AC-G1/G2 (RM-1/RM-3)
Grep `verificat|confermat|dimostrat|stabilit|provato|accertato` sulla spec: zero asserzioni "verificato X" di prima istanza. Le occorrenze sono (i) meta-negazioni ("NON introduce verificato X"), (ii) un richiamo etichettato ("rinvio empirico confermato in `[DOC-INTERNO CAP_07:23]`"), (iii) "Codici mese verificati F/I `[DOC-INTERNO CAP_09:61]`" — richiamo a fatto chiuso `[PROVA-EMPIRICA]` con etichetta DOC-INTERNO. Fonti esterne (MiFID II, wiki Directa, Portara/CQG, CME/Eurex) etichettate `[WIKI-HINT, da verificare]`; nota di testa con avvertenza esplicita di inaffidabilità wiki Directa su schema CANDLE (eredità AUDIT-RM CAP-DATA-02). **AC-G1/G2 OK.**

### Completezza vs AC e onestà REPORT
AC di sezione 1-10 + AC-G1..G12 soddisfatti con evidenza reale nel file (non solo dichiarata): tabella payload ≥9 voci (10), diagramma 1+6, due esempi Telegram, NFR L_max 30s + M-2 dichiarata aperta (AC-G8), KPI ≥6 (8), checklist ≤12 (12), tabella dipendenze ≥6 (6), matrice ≥30 righe (36), capitoli non tracciati motivati (Sez.10.5). REPORT: campionati AC-G3/G6/G10 e i flag N/A (AC-G13/14/15 correttamente marcati lato Reviewer). **Onesto: nessun "OK" privo di evidenza.**

---

## Classificazione per il supervisore

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|------------------------|
| OM-1 | Citazioni Sez.9/10 a riga di header capitolo/adiacente invece che riga esatta (6 occorrenze; tag corretto, capitolo corretto, costrutto presente) | `SPEC_FUNZ_01.md` Sez.9.2/9.3/10.1/10.3 (rif. CAP_10:11/74/151/226/234; CAP_07:574) | NEUTRO | NO — non cambia tracciabilità sostanziale; fix chirurgico opzionale |
| OM-2 | R-17 "singolo segnale attivo **per direzione**": wording lasco, ma vincolo corretto $\|\mathcal{A}(t)\|\le 1$ enunciato in-linea | `SPEC_FUNZ_01.md:256` | NEUTRO | NO — il constraint corretto governa; pulibile cancellando "per direzione" |
| OM-3 | Ancora di provenienza `fN` schema PRICE: spec cita CAP_09:94 (descrittivo); numerazione `fN` da STATO_CORRENTE M-9:76 (riprodotta corretta) | `SPEC_FUNZ_01.md:384` | NEUTRO | NO — fatto corretto e tracciabile; ancora aggiuntiva opzionale |

**Default applicato**: i NEUTRO non vanno a Development. Nessun BUG REALE, nessun MIGLIORA PERFORMANCE, nessun RISCHIO PEGGIORAMENTO rilevato. Verdetto **PASS**: la spec può essere chiusa. Se il supervisore vuole massimizzare l'igiene di citazione, OM-1/OM-2/OM-3 sono ritocchi chirurgici opzionali (non obbligatori per la correttezza).

---

## Empirico-CLI da verificare

**VUOTA** (come atteso dal task card). La spec consolida fatti già chiusi nei CAP (Parti I-X tutte PASS) e negli audit RM CAP-DATA-01/02/03; non introduce alcuna asserzione empirica nuova che ecceda i fatti chiusi e richieda riproduzione contro DAPI. Nessun handoff alla sede CLI necessario.

---

## Applicazione RM-1 a me stesso (AC-G13)

Dichiaro il sostegno operativo di ogni mia affermazione di verifica:

- **"Le 3 citazioni `[CODICE-ESISTENTE]` risolvono (MATCH)"**. PROVE: Read di `scripts/export_directa_history_parametric.py` r55-69 (`:61`), r460-489 (`:467-481`, incluso commento r477 e assegnazioni `close_v=Decimal(uff)` ecc.), r600-622 (`:605-617`, header 11 campi). ALTERNATIVE ESCLUSE: schema diverso da `C;L;H;O` (escluso da r471+r477-481 leggibili direttamente); header con `tick_count`/`bar_synthetic` (escluso: assenti nella lista r605-617). ALTERNATIVE NON ESCLUSE: nessuna sui tre punti citati.
- **">50 citazioni `[DOC-INTERNO]` risolvono al capitolo corretto con costrutto presente"**. PROVE: Read integrale o mirato di CAP_01 (r1-86), CAP_02 (r1-412), CAP_06 (r142-220), CAP_07 (r20-27, r562-602), CAP_08 (r11-14, r165-168), CAP_09 (r33-147, r270-308, r350-446), CAP_10 (r1-20, r72-76, r149-153, r182-191, r224-259); tabelle decisioni Cap.56 (r414-446) e Cap.65 (r246-258); STATO_CORRENTE M-9/M-10 (r76-77); indice (campionato r7-114). ALTERNATIVE ESCLUSE per i punti rischiosi: contraddizione su state machine (esclusa da CAP_02:95+:101-111), su target_2 lifecycle (esclusa da CAP_02:37), su riconciliazione bloccante (esclusa da CAP_10:250 + indice r101), su 6 marker (esclusa da CAP_09:353 + D-9-NB3). ALTERNATIVE NON ESCLUSE: non ho aperto la totalità delle ~70 citazioni (ho campionato per copertura su tutti i CAP citati e sulla totalità dei punti rischiosi del task card); il campione non aperto è omogeneo a quello aperto (stesso autore, stesso pattern di etichettatura) e nessuna anomalia è emersa nel campione esteso → rischio residuo basso, non zero.
- **"Lista Empirico-CLI VUOTA è corretta"**. PROVE: grep `verificat|confermat|...` sulla spec (nessuna asserzione empirica nuova di prima istanza); la spec etichetta ogni fatto empirico come richiamo `[DOC-INTERNO]`/`[PROVA-EMPIRICA via CAP]`. ALTERNATIVE ESCLUSE: presenza di un "verificato X" nuovo che richieda DAPI (escluso dal grep). ALTERNATIVE NON ESCLUSE: nessuna.
- **"Lunghezza entro AC-G10"**. PROVE: `wc -w` = 6443 parole; stima 13-14 pp a ~470 parole/pagina. ALTERNATIVE ESCLUSE: deviazione ≥40% (esclusa: 6443 è dentro 12-16 pp). ALTERNATIVE NON ESCLUSE: la conversione parole→pagine è una stima (il criterio "pagine" non è rigorosamente definito in righe/pagina); resta comunque entro banda con margine.

Non ho riaperto alcun CAP chiuso (AC-G14): dove la spec riproduce una decisione chiusa (es. f8/f9 su CANDLE in D-10-4), l'ho trattata come autoritativa e ho verificato solo la **fedeltà di riproduzione** della spec, non il merito del CAP.

---

*Fine review SPEC-FUNZ-01. Verdetto: PASS. 0 bloccanti, 0 BUG REALE, 3 osservazioni NEUTRO (ritocchi opzionali). Sede WEB, statico, no DAPI. Empirico-CLI: vuoto.*

---
---

# Re-Review v2 SPEC-FUNZ-01 — verdetto: PASS

**Tipo**: re-review LEGGERA focalizzata (modello "re-review v2 cosmetica" di CAP-DATA-03). **NON** ripete l'audit a tappeto di v1 (gia' PASS, `d8a40a0`): verifica solo (a) che i 3 fix NEUTRO approvati risolvano correttamente e (b) zero regressione.
**Sede**: WEB (audit statico — documento + grep + Read dei CAP committati; nessuna esecuzione DAPI).
**Oggetto**: commit Developer v2 `314dd1b` — diff = **6 righe** su `docs/spec_funzionale/SPEC_FUNZ_01.md` (6 ins / 6 del), confinato alle 3 zone OM (R-17 Sez.6; NFR-4 Sez.7.2; Sez.9.2; R-22 Sez.9.3; Sez.10.1; Sez.10.3 voce 4).
**Input autoritativo**: i 3 OM approvati sono in `tasks/ACTIVE_TASK.md` ("Finding di Review da risolvere", r406-418) e in `reports/REPORT_SPEC_FUNZ_01.md` ("Iterazione 2", r125-175). Mapping di review v1: blocco "Osservazioni minori" OM-1/2/3 (sopra in questo file).

## A — OM-1: i 6 nuovi numeri di riga risolvono alla riga ESATTA col costrutto citato?

Aperti con Read `CAP_10_parte_10.md` e `CAP_07_parte_VII.md`. Ognuno confermato token-per-token: la riga di destinazione contiene **davvero** il costrutto che la spec cita in quel punto.

| # | Citazione (spec) | Nuovo target | Costrutto reale alla riga (Read) | Esito |
|---|---|---|---|---|
| 1 | invariante research=runtime esteso al ciclo di vita del tape (Sez.9.2) | `CAP_10:5` | r5 = "l'invariante `research semantics = runtime semantics` ... e' esteso ... all'**intero ciclo di vita del tape**" | MATCH |
| 2 | limite ~100gg, Cap.59 (R-22) | `CAP_10:76` | r76 = "Questo capitolo norma il recupero gap di durata $\leq \sim 100$gg ... Il limite e' stabilito empiricamente" | MATCH |
| 3 | Step C fallback Portara, Cap.61 (R-22) | `CAP_10:161` | r161 = "**Step C — Fallback Portara.** Se ne' archivio locale ne' `CANDLERANGE` daily coprono ... fallback all'archivio Portara/CQG" | MATCH |
| 4 | cross-index PHASE-2 fuori scope (Sez.10.1) | `CAP_10:236` | r236 = "**Convenzione cross-index PHASE-2** ... Parte 10 NON si applica ai cross-index PHASE-2 (fuori scope PHASE-1)" | MATCH |
| 5 | riavvio Darwin mezzanotte (Sez.10.3 voce 4) | `CAP_10:233` | r233 = "**Riavvio Darwin mezzanotte** — osservazione empirica diretta: residuo Empirico-CLI di Parte 9 Cap.50 Gap-3" | MATCH |
| 6 | AC-GO-4 lifecycle cross-regime (NFR-4) | `CAP_07:576` | r576 = "**AC-GO-4 — Lifecycle stabile cross-regime.** $\|f_5^{global}(\theta^*)\| < \theta_{f_5} = 0{,}30$" | MATCH |

Nota anti-falso-positivo: per #2 r74 = header "## Capitolo 59" (riga vecchia, ora abbandonata); per #6 r574 = AC-GO-3 (expected net return, riga vecchia). I nuovi target (r76, r576) puntano al corpo del costrutto, non all'header/adiacente. **OM-1: tutti e 6 risolvono alla riga esatta. 0 citazioni introdotte dal fix che non risolvano.**

## B — OM-2: R-17 senza "per direzione" + constraint globale preservato

- Diff R-17 (spec r256): titolo "**R-17 — Singolo segnale attivo per direzione.**" → "**R-17 — Singolo segnale attivo.**". Unico token cambiato; il resto della riga e' byte-identico.
- Vincolo in-linea `$|\mathcal{A}(t)|\le 1$: nessuna politica multi-segnale concorrente` **mantenuto** (non perso).
- Coerenza con CAP_02 (Read r79-87): r81 = "$$|\mathcal{A}(t)| \leq 1\ \text{per ogni}\ t$$" — vincolo **globale** (al massimo un segnale a ogni istante), r87 "elimina dal dominio del GA tutte le politiche multi-segnale concorrente". La locuzione "per direzione" rimossa dal titolo poteva suggerire $|\mathcal{A}|\le 2$; la sua rimozione **avvicina** il titolo alla semantica del CAP, non la altera.
- Allineamento a R-7 (spec r112, Read): "**R-7 — Segnale unico attivo.** ... $|\mathcal{A}(t)|\le 1$" — gia' senza "per direzione". Ora R-17 ↔ R-7 coerenti.
- Riferimento autoritativo `CAP_02_parte_II.md:81` **invariato**. **OM-2: constraint non perso, coerente con CAP_02:81/:87. OK.**

## C — OM-3: ancora STATO_CORRENTE:76 aggiunta + richiamo CAP_09:94 mantenuto

- Diff Sez.9.2 (spec r384): `M-9 [DOC-INTERNO CAP_09_parte_9.md:94]` → `M-9 [DOC-INTERNO tasks/STATO_CORRENTE.md:76], descritto anche in [DOC-INTERNO CAP_09_parte_9.md:94]`.
- Verifica STATO_CORRENTE:76 (Read r76): r76 = riga **M-9** = "**Schema PRICE realtime (DAPI)** [PROVA-EMPIRICA 2026-06-01 W2, CAP-DATA-02]: `PRICE;<tk>;<HH:mm:ss>;<f4=last>;<f5>;<f6=volume_cum>;<f7>;<f8=day_low>;<f9=day_high>`". E' davvero la riga sorgente della numerazione `f4/f6/f8/f9` riprodotta dalla spec, token-per-token, ed e' etichettata `[PROVA-EMPIRICA]` (provenienza corretta della numerazione `fN`).
- Il richiamo descrittivo `CAP_09_parte_9.md:94` e' **mantenuto** (come richiesto dal finding). **OM-3: ancora puntuale alla riga M-9 corretta + richiamo CAP_09 mantenuto. OK.**

## D — Zero regressione

1. **Diff confinato alle 3 zone OM**: `git show 314dd1b --numstat` su `SPEC_FUNZ_01.md` = `6  6` (6 ins / 6 del). Ispezione riga-per-riga dei `-`/`+`: ogni coppia differisce SOLO per il token oggetto del fix (numero di riga, titolo R-17, ancora STATO_CORRENTE). Nessun'altra citazione, requisito, formula o sezione alterata.
2. **Vecchi numeri = 0 occorrenze residue**: grep sulla spec di `CAP_10:11`, `:74`, `:151`, `:226`, `:234`, `CAP_07:574` → **No matches found** (nessuna citazione stale lasciata). I 6 nuovi numeri + `STATO_CORRENTE:76` tutti presenti (NFR-4 r301, Sez.9.2 r384, R-22 r390, Sez.10.1 r417, Sez.10.3 r428).
3. **Citazioni gia' corrette in v1 invariate**: `CAP_10:230` (r427 + self-review r520), `CAP_10:255` / `:256` (R-21 r389), `CAP_09:94` (r384, richiamo descrittivo conservato) — tutte presenti e immutate. `CAP_10:230` (DEFAULT_INTRADAY_MAX_DAYS) **correttamente** non toccato (non era in lista OM-1).
4. **Nessun nuovo "verificato X"**: il diff non introduce asserzioni empiriche di prima istanza; tutte le righe modificate restano richiami `[DOC-INTERNO]`/`[CODICE-ESISTENTE]` etichettati. Nessuna nuova contraddizione coi CAP (le 6 righe ora puntano a righe che, lette, confermano l'asserzione della spec).

**D: 0 regressione.**

## Osservazioni fuori-perimetro v2

Nessuna. Non ho ispezionato (per mandato di re-review focalizzata) le zone non toccate dal diff v2: sono gia' PASS in v1 e AC-G14 vieta di riaprire i CAP chiusi. Nessun problema sostanziale notato di sfuggita durante la verifica dei 4 punti.

## Applicazione RM-1 a me stesso (re-review v2)

- **"I 6 nuovi target risolvono alla riga esatta col costrutto"**. PROVE: Read `CAP_10_parte_10.md` r1-12 / r72-81 / r157-164 / r230-238 e `CAP_07_parte_VII.md` r572-578; ogni riga citata contiene il costrutto (tabella sez. A). ALTERNATIVE ESCLUSE: target che cade su header/adiacente (escluso: r5/r76/r161/r236/r233/r576 sono corpo del costrutto, verificato leggendo la riga; gli header r74/adiacente r574 sono i target *vecchi* abbandonati). ALTERNATIVE NON ESCLUSE: nessuna — ho letto direttamente le righe di destinazione, non dedotto.
- **"OM-2 non perde il constraint ed e' coerente con CAP_02:81"**. PROVE: diff mostra inline `$|\mathcal{A}(t)|\le 1$` mantenuto; Read CAP_02 r79-87 (r81 vincolo globale, r87 elimina multi-segnale); Read spec r112 (R-7 gia' senza "per direzione"). ALTERNATIVE ESCLUSE: constraint $|\mathcal{A}|\le 2$ (escluso da CAP_02:81 "≤ 1 per ogni t"). ALTERNATIVE NON ESCLUSE: nessuna.
- **"OM-3 ancora la riga M-9 sorgente della numerazione fN"**. PROVE: Read STATO_CORRENTE r73-77 (r76 = M-9 con `f4=last/.../f9=day_high`). ALTERNATIVE ESCLUSE: riga diversa da M-9 (esclusa: r76 e' M-9, r75=M-7, r77=M-10). ALTERNATIVE NON ESCLUSE: nessuna.
- **"Zero regressione: diff confinato + 0 vecchi numeri + correttezza v1 invariata"**. PROVE: `git show 314dd1b --numstat`=`6 6`; diff `-`/`+` riga-per-riga (solo token-fix); grep vecchi numeri = "No matches found"; grep `CAP_10:230/:255/:256/CAP_09:94` = tutte presenti. ALTERNATIVE ESCLUSE: modifica nascosta fuori dalle 3 zone (esclusa: numstat=6 righe + ispezione integrale dei `-`/`+`); citazione stale residua (esclusa dal grep). ALTERNATIVE NON ESCLUSE: nessuna — il diff e' piccolo e interamente ispezionato.

Non ho riaperto alcun CAP chiuso (AC-G14): ho usato i CAP come autoritativi e verificato solo la **fedelta' della citazione** della spec verso la riga di destinazione, non il merito del CAP.

## Verdetto motivato

**PASS.** I 3 fix NEUTRO approvati risolvono correttamente: OM-1 (6/6 numeri di riga puntano ora alla riga esatta col costrutto, verificato token-per-token), OM-2 (R-17 allineato a R-7, constraint globale $|\mathcal{A}(t)|\le 1$ preservato e coerente con CAP_02:81/:87), OM-3 (ancora `STATO_CORRENTE:76`=M-9 aggiunta come provenienza della numerazione `fN`, richiamo CAP_09:94 mantenuto). Zero regressione: diff di 6 righe interamente confinato alle 3 zone OM, 0 occorrenze residue dei vecchi numeri, citazioni gia' corrette in v1 invariate, nessun nuovo "verificato X". Nessun finding. Nessun handoff CLI richiesto (audit statico sufficiente; il track non produce fatti empirici).

---

*Fine re-review v2 SPEC-FUNZ-01. Verdetto: PASS. 0 finding. A/B/C/D tutti OK. Sede WEB, statico, no DAPI.*
