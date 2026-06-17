# REVIEW — SPEC-FUNZ-01-B6 (Schema-dato DAPI & continuità tape)

> **Track**: Business-spec (SPEC-FUNZ). **Blocco**: 6/8 (ricostruzione cieca, modalità B).
> **Sede**: **CLI** (GOV-SURFACES-01) — audit documentale no-DAPI, divieto CLI attivo (nessuna probe di zelo).
> **Modalità**: CAP-review piena adattata al non-CAP, **due giri ostili** (BASE_COMUNE §6). **Cautela RM massima** (territorio incidente CANDLE).
> **Oggetti**: `docs/spec_funzionale/SPEC_FUNZ_01_B6.md` (commit `80409d9`) + `reports/REPORT_SPEC_FUNZ_01_B6.md`.
> **Letture confermate**: `tasks/METODO.md` (RM-1..RM-4 + RACC-METODO-2), `.claude/BASE_COMUNE.md`, `.claude/agents/spec_reviewer.md`, `tasks/ACTIVE_TASK.md` (card B6 rev. CARD-FIX-01).

---

## ITERAZIONE 1 — verdetto: **CONDITIONAL**

**Sintesi**: la sostanza dello schema-dato è solida e onesta — floor citazioni 100% (DOC-INTERNO + CODICE-ESISTENTE decoder) tutte risolte token-per-token; RM-1/RM-2/RM-3 rispettate; diff-decoder onesto (non spaccia per "da decoder" ciò che è solo PROVA-EMPIRICA); copertura piena dei 9 req-v2; cecità preservata; PENDING marcati e non asseriti. **Un solo finding bloccante non-PASS**: il **conteggio dei requisiti dichiarato è falso** — il documento e il REPORT dichiarano "61 (37 R + 20 CN + 4 NFR)", ma i B6-CN sono **24** e il totale reale è **65** (matrice a 65 righe). È un claim fattuale non veritiero sul proprio contenuto (BASE_COMUNE §8, onestà claim→evidenza) → 1 BUG REALE → CONDITIONAL.

---

## Problemi bloccanti (BUG REALE)

### BUG-1 — Conteggio dei requisiti dichiarato è errato (65 reali vs 61 dichiarati; 24 CN vs 20)

Il documento e il REPORT dichiarano ripetutamente **"61 requisiti (37 B6-R, 20 B6-CN, 4 B6-NFR)"**. L'evidenza nel file lo smentisce:

- ID `B6-R-*` definiti in grassetto: **37** ✓ (coerente)
- ID `B6-CN-*` definiti in grassetto: **24** (CN-01..CN-24, consecutivi, senza gap né duplicati — verificato `:89..:299`) — dichiarati **20** ✗
- ID `B6-NFR-*`: **4** ✓
- Righe della matrice di tracciabilità §7.1 (`^| B6-`): **65** ✗ rispetto al "61 righe" implicito.

Totale reale = **65 requisiti (37 + 24 + 4)**, non 61.

Occorrenze del claim falso:
- `SPEC_FUNZ_01_B6.md:413` (footer): "61 requisiti: 37 R + 20 CN + 4 NFR".
- `REPORT_SPEC_FUNZ_01_B6.md:8` (§1): "**61 requisiti atomici** (37 B6-R, 20 B6-CN, 4 B6-NFR)".
- `REPORT_SPEC_FUNZ_01_B6.md:29` (§4 Misura): "61 requisiti R/CN/NFR atomici … matrice a 61 righe".
- (Il prompt Orchestratore eredita lo stesso conteggio errato — propagazione, non causa.)

**Perché è BUG REALE e non cosmesi**: l'asse di impatto del track include l'**onestà del REPORT** (asse #5) e la **fedeltà** del documento (asse #1). Un conteggio è un claim fattuale verificabile: qui è falso e contraddetto dall'evidenza nel file stesso. La tabella AC del REPORT marca AC-G1 (atomicità) e AC-G2 (tracciabilità/matrice) come OK appoggiandosi a una numerosità sbagliata. Un lettore esterno che enumera i requisiti trova 65, non 61: la descrizione del documento diverge dal proprio corpo. Per il mapping verdetto↔classificazione (BASE_COMUNE §4), ≥1 BUG REALE ⇒ non-PASS.

**Ambito del fix (chirurgico, nessun impatto su CAP né proposizioni)**: correggere il conteggio a **65 (37 R + 24 CN + 4 NFR)** nel footer del documento (`:413`), in `REPORT §1`, `REPORT §4`, e nella tabella AC del REPORT ove citi la numerosità. Nessuna proposizione/ID/citazione cambia: i 65 requisiti sono tutti presenti, tracciati e atomici. È un errore di addizione/auto-descrizione, non un buco di contenuto.

---

## Problemi non-bloccanti

Nessuno.

---

## Osservazioni minori (NEUTRO / non instradare salvo decisione AC)

- **OM-1 — colonna "Capitolo v2" di B6-CN-23 = "Cap.62/58"** (`:373`). Il pin-fonte `[DOC-INTERNO CAP_10_parte_10.md:68]` risolve correttamente (riga 68 = regola di composizione "provenienza tracciata da source, non da bar_synthetic"), ma `:68` sta nel **preambolo compositivo** di CAP_10 (pre-Cap.59), non in un "Cap.58". L'etichetta di colonna "Cap.62/58" è imprecisa/orfana ("Cap.58" non è un capitolo della materia B6). Non è una citazione-fonte errata (la citazione `path:line` è giusta): è un'imprecisione nella colonna descrittiva della matrice. NEUTRO.
- **OM-2 — B6-R-28 e B6-R-31 borderline-compositi (N1)**: B6-R-28 impacchetta i 3 step ordinati del re-bootstrap (A/B/C); B6-R-31 elenca 5 controlli di integrità-schema in un enunciato. In entrambi i casi resta una **singola proposizione unitaria verificabile** (una procedura sequenziale interdipendente; il "primo check del gate" come unità), fedele alla struttura del CAP (`:158-161`, `:121`). Non sfugge a verifica singola → non "da spezzare" come BUG. Annotato come borderline, NEUTRO (eventuale split atomico solo su discrezione AC).

---

## Esito floor citazioni — 100% (target AC-G7)

**Tutte** le citazioni campionate (DOC-INTERNO + CODICE-ESISTENTE decoder) risolvono token-per-token contro i file reali. Aperti con Read: `CAP_09_parte_9.md`, `CAP_10_parte_10.md`, `CAP_02_parte_II.md`, `CAP_08_parte_8.md`, `export_directa_history_parametric.py`, `probe_dapi.py`.

**Decoder (RM-2), pin verificati**:
| Pin | Esito |
|---|---|
| `export_directa_history_parametric.py:61` `DEFAULT_INTRADAY_MAX_DAYS = 100` | ✓ verbatim |
| `:228-230` sintassi `CANDLERANGE {symbol} {start} {end} {period_seconds}` (period in ultima pos.) | ✓ verbatim |
| `:471` `kind, symbol, ymd, hms, uff, min_, max_, ape, qty = parts[:9]` | ✓ verbatim |
| `:477` commento `# Documentazione Directa: UFF, MIN, MAX, APE => close, low, high, open.` | ✓ verbatim |
| `:478-481` `close_v=Decimal(uff)/low_v=Decimal(min_)/high_v=Decimal(max_)/open_v=Decimal(ape)` | ✓ verbatim |
| `:482` `volume_v = int(Decimal(qty))` | ✓ (citato in B6-R-09) |
| `:605-617` header **legacy 11 campi** (`symbol..volume,source`, senza tick_count/bar_synthetic) | ✓ verbatim — enumerazione B6-CN-06 corretta |
| `probe_dapi.py:247-270` CANDLE `p[4]=UFF→close, p[5]=MIN→low, p[6]=MAX→high, p[7]=APE→open` | ✓ verbatim |
| `probe_dapi.py:289-306` PRICE `last=float(p[3])`, `fields_extra=p[4:]` + commento `:290-291` "schema esatto dei campi extra non documentato, varia tra cash e future" | ✓ verbatim |
| `probe_dapi.py:307-317` BOOK_5 commento `[BID×5][ASK×5]` triple, `fields=p[3:]` (non parsate) | ✓ verbatim |
| `probe_dapi.py:308-309` commento posizioni bid/ask | ✓ verbatim |

**DOC-INTERNO (CAP), pin verificati** (campione esteso, tutti risolti): CAP_09 `:21, :117, :120, :125, :127, :129, :131-138, :153, :158, :164-171, :172, :173, :177-179, :181, :191, :254, :256, :257, :260-261`; CAP_10 `:68, :79-83, :88, :90, :91, :98, :119, :121, :122, :123, :124-127, :126, :131, :136-139, :146, :157-158, :158-161, :161, :162, :163-164, :168-170, :174, :184, :185, :186-188, :194, :196-203, :207, :209, :233`; CAP_02 `:291, :293` (Cap.10 determinismo replay bit-exact); CAP_08 Cap.44 (`:215` "Esclusione esplicita di fonti alternative" — supporta il vincolo negativo tape-non-training). **Zero citazioni non risolte. Zero grafia deprecata `[CODICE-EXISTENTE]`.**

---

## Esito confronto-copertura (modalità B — mappa `c7ce4be`, F-3; mio compito esclusivo)

I **9 req-v2 di Sez.9** assegnati a B6 (10 con R-9.3 spezzato, F5):

| Req-v2 | Area | Coperto da | Esito |
|---|---|---|---|
| R-9.1 (adapter→barra simmetrica) Cap.49 | adapter | B6-R-01/02/03 | ✓ coperto |
| CN-9.1 (CANDLE C;L;H;O;V) Cap.49 | schema CANDLE | B6-R-04..09 | ✓ coperto |
| CN-9.4 (replay bit-exact) preambolo CAP_09 + CAP_02 Cap.10 | replay | B6-NFR-01..04 | ✓ coperto |
| R-9.2 (warm-up L_warmup=30) Cap.51 | warm-up | B6-R-22/23, CN-10/11 | ✓ coperto |
| R-9.3a (gap ≤100gg) Cap.59 | gap | B6-R-24..26, CN-12/13 | ✓ coperto (distinto) |
| R-9.3b (restart >100gg STALE) Cap.61 | restart | B6-R-27..29, CN-14..16 | ✓ coperto (distinto, F5 ✓) |
| R-9.4 (gate EOD bloccante) Cap.60 | riconciliazione | B6-R-30..34, CN-18 | ✓ coperto |
| CN-9.2 (low/high da CANDLE daily f8/f9) Cap.60 | low/high | B6-R-17, R-33, CN-17 | ✓ coperto |
| R-9.5 (tape archiviato) Cap.62 | archivio | B6-R-35..37, CN-21/22 | ✓ coperto |
| CN-9.3 (tape NON fonte training) Cap.62 + CAP_08 Cap.44 | vincolo negativo | B6-CN-24 | ✓ coperto |

**Copertura piena: 9/9 (10/10 con R-9.3a/b distinti). 0 buchi.**
**Sconfinamenti: 0.** Nessun requisito su canale Cap.46/47 (→B5 premessa, §7.2), audit Cap.54 (→B5), preprocessor Cap.40 (→Parte 8), lifecycle (→B3). Cap.48 trattato come **framing** → vincoli-contenitore B6-CN-05..09 (nessun requisito improprio). PRICE/BOOK_5 (B6-R-16..21) ancorati come **input dell'adapter** (F4), non materia-canale.
**Orfani (req B6 senza area v2): 0.**

---

## Esito audit cecità (AC-G8)

**Preservata.** Grep su `R-9.|CN-9.|R-7.|CN-7.|req-v2|partizione|chunking|SPEC_FUNZ_01.md|PROPOSTA_SUDD`: unica occorrenza = la frase di **dichiarazione di cecità** in §1.4 (`:25`). Nessun ID-requisito v2 importato, nessun conteggio/partizione v2 usato, nessuna firma-testo v2. ID `B6-*` auto-assegnati da zero.

---

## Esito RM-1 / RM-2 / RM-3 e onestà del diff-decoder

- **AC-B6-1 (RM-2 diff col decoder canonico)** — OK. Diff esplicito per i 3 schemi. **Onestà verificata**:
  - **CANDLE** (B6-R-04, `:53`): i due decoder concordano token-per-token → "nessun diff", schema = decoder. Corretto.
  - **PRICE** (B6-R-16, `:114`): dichiara esplicitamente che `probe_dapi.py:289-306` decodifica **solo `last=p[3]`** e tratta `p[4:]` come `fields_extra` non disambiguati → la semantica `f6/f8/f9` **NON ha supporto level-2**, è ancorata a `[PROVA-EMPIRICA 2026-06-01 W2]`. **Non spaccia per "da decoder" ciò che è solo empirico** — onesto.
  - **BOOK_5** (B6-R-18, `:135`): dichiara che il decoder documenta lo schema in commento ma **non parsea le triple** (`fields=p[3:]`) → posizioni certificate a level-1 da `[PROVA-EMPIRICA 2026-06-01 W3]` (290 triple). Onesto. Coerente col "Limite onesto" del REPORT (`:86`).
- **AC-B6-2 (RM-1 permutazioni escluse)** — OK. Blocchi VERIFICA/PROVE/ALTERNATIVE espliciti:
  - CANDLE (`:55-61`): `O;H;L;C` FALSIFICATA da V-1 (distinse O da C sui tick realtime). ✓
  - PRICE `f8/f9` (`:116-122`): (a) bid/ask FALSIFICATA dal BOOK_5 simultaneo; (b) confusione con CANDLE-daily f8/f9 esclusa (namespace per-tipo-messaggio, B6-CN-04). **Entrambe** le permutazioni richieste dalla card escluse. ✓
  - BOOK_5 (`:146-152`): triplo invertito escluso (lots≥orders 290/290), blocchi invertiti esclusi (29/29), anomalia 27/05 = artefatto FIB6I illiquido. ✓
- **AC-B6-3 (RM-3 gerarchia)** — OK. §1.5 + §7.4: gerarchia PROVA-EMPIRICA > CODICE-ESISTENTE > DOC-INTERNO > WIKI-HINT; **0 conclusioni wiki-only**; wiki Directa = `[WIKI-HINT, da verificare]`; mesi F/I convenzione NON-standard, nessuna inferenza per analogia CME. Grafia canonica (nessun `[CODICE-EXISTENTE]`).
- **AC-B6-4 (PENDING marcato, non asserito)** — OK. §7.3 PE-1..5 (Mar/Dic, 1030, Darwin-mezzanotte, PRICE f5/f7, base calendario V-2) marcati come pendenti, non asseriti; `L_warmup=30` correttamente classificato **congelato** (non pending), con la sola resa-in-calendario come V-2; certificati elencati separatamente, non sovra-marcati.

---

## Esito punti di attenzione (boundary-check Orchestratore; non vincolano il verdetto)

- **CAP_02_parte_II citato (6 volte nel corpo + matrice)** — tutte e sole **premesse** etichettate "premessa/fondazione formale", puntano a `:291`/`:293` (Cap.10 determinismo replay bit-exact). **Nessuna ri-derivazione di materia B2/B3** (payload/state-machine): B6-NFR-01 cita "signal_id/transizioni di stato" solo come oggetto della formula di determinismo verbatim dal CAP, non per consolidare il lifecycle. OK.
- **Granularità 65 req per 9 v2** — **atomicità genuina**, non over-split artificiale (un requisito per proposizione fattuale: campi CANDLE 5+, posizioni BOOK_5, regole bar_synthetic per regime, ecc.). Borderline OM-2 (B6-R-28/R-31), non bloccante.
- **F4/F5/F7** — tutti rispettati: PRICE/BOOK_5 ancorati al requisito-adapter (F4, B6-CN-03); gap≤100gg (B6-R-24) e restart>100gg (B6-R-27) distinti (F5); Darwin-mezzanotte (premessa B5, §7.2/PE-3) ≠ RUNTIME_STALE_RESTART (B6, in-scope) (F7).

---

## Tabella "Classificazione per il supervisore"

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|------------------------|
| 1 | Conteggio requisiti dichiarato falso: "61 (37R/20CN/4NFR)" vs reale **65 (37R/24CN/4NFR)**, matrice 65 righe | `SPEC_FUNZ_01_B6.md:413`; `REPORT:8,29` + tabella AC | **BUG REALE** | Sì (obbligatorio) |
| 2 | Colonna matrice B6-CN-23 = "Cap.62/58": etichetta orfana "Cap.58" (pin-fonte `:68` corretto) | `SPEC_FUNZ_01_B6.md:373` | NEUTRO | No (salvo decisione AC) |
| 3 | B6-R-28 / B6-R-31 borderline-compositi (N1) — restano proposizioni unitarie verificabili | `SPEC_FUNZ_01_B6.md:231,253` | NEUTRO | No (salvo decisione AC) |

I BUG REALI vanno sempre a Developer. NEUTRO non va a Developer senza approvazione del supervisore.

---

## Applicazione RM-1 a me stesso

- **"floor citazioni 100%"**: non è auto-compiacimento — ho aperto con Read ogni file-fonte e confrontato verbatim ogni pin elencato nel prompt + un campione esteso di DOC-INTERNO. Esito per pin riportato in tabella. ALTERNATIVE NON ESCLUSE: non ho riletto il 100% assoluto delle ~65 citazioni DOC-INTERNO una per una, ma il campione copre tutte le righe-chiave (schema CANDLE/PRICE/BOOK_5, warm-up, gap, restart, riconciliazione, archivio, replay) e tutti i pin decoder; nessuna delle verificate ha fallito.
- **"conteggio 65 vs 61"**: VERIFICA da grep meccanico (`^\*\*B6-CN-` = 24; `^\| B6-` = 65; enumerazione ID CN-01..CN-24 senza gap). PROVE: output grep citati. ALTERNATIVE ESCLUSE: duplicati/gap negli ID CN (escluso — i 24 ID sono distinti e consecutivi). ALTERNATIVE NON ESCLUSE: nessuna.
- **"copertura 9/9"**: la mappatura req-v2→capitolo è autoritativa dall'Orchestratore (mappa `c7ce4be`, F-3); io ho verificato la **risoluzione per contenuto** (ogni area v2 ha ≥1 requisito B6 con citazione che risolve), non ho riaperto la partizione. ALTERNATIVE NON ESCLUSE: nessuna sulle 9 aree elencate.
- **"diff-decoder onesto"**: ho aperto `probe_dapi.py:289-306` e `:307-317` e confermato che il decoder NON parsea f6/f8/f9 né le triple → la spec dichiara il limite, non lo nasconde. Asserzione sostenuta da Read diretto.
- **"cecità preservata"**: da grep negativo sui pattern v2 (unica occorrenza = dichiarazione di cecità). Non da fiducia nel REPORT.

---

## Empirico-CLI da verificare

**VUOTA** (attesa). La spec consolida fatti già chiusi PASS (CAP-DATA-02 RM-RETRO WEB+CLI, audit empirici certificati); non introduce fatti empirici nuovi. Audit documentale no-DAPI in sede CLI col divieto CLI rispettato (nessuna probe eseguita). I PENDING-empirico (PE-1..5) sono pendenze ereditate marcate, non verificate qui (fuori sede).
