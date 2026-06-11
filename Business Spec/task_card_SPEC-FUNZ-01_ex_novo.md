> ⚠️ **BOZZA — NON È IL TASK ATTIVO.** Proposta di task card per la scrittura *ex novo* di SPEC-FUNZ-01.
> Diventa operativa solo quando il supervisore dà il GO e l'Orchestratore la promuove a `tasks/ACTIVE_TASK.md` (committandola), **oppure** la passa a `spec_planner` per l'affinamento. Finché vive con questo nome, la macchina a stati NON la legge (chiave di stato = solo `ACTIVE_TASK.md`).

# TASK CARD (BOZZA): SPEC-FUNZ-01 (ex novo) — Specifica funzionale del prodotto-segnale FIB (PHASE-1)

**Assegnato da**: Planner (track business-spec)
**Tipo**: **SCRITTURA EX NOVO DA ZERO che SOVRASCRIVE** `docs/spec_funzionale/SPEC_FUNZ_01.md`. Consolidamento di **GA_Metodologia_v2** in requisiti di prodotto. La spec precedente resta nella **storia git**, **non** va cancellata, **non** è fonte né baseline.
**Output atteso**: `docs/spec_funzionale/SPEC_FUNZ_01.md` (scrittura integrale ex novo) + `reports/REPORT_SPEC_FUNZ_01.md` (5 sezioni formato supervisore — definite sotto — + tabella verifica AC).
**Stato**: IN ATTESA (bozza)
**Workflow**: Standard `Planner → Developer → Reviewer`, con agenti `spec_*` **induriti N1+F6**.
**Sede Reviewer**: **WEB-statico** (documento + grep + Read di GA_Metodologia_v2 e dei decoder committati; **nessun DAPI**). Lista "Empirico-CLI da verificare" attesa **VUOTA**.
**Modalità di review**: audit ostile **a tappeto**, **due passate complete entro la singola Review prima del verdetto** (requisito di accuratezza della Review, **distinto** dal loop CONDITIONAL/FAIL → fix → re-review). NON re-review leggera.

---

## Fonte di verità (autoritativa)

**Fonte unica = `GA_Metodologia_v2`.** I requisiti si consolidano da lì e si citano **per capitolo/parte del documento** (es. "Cap. 6.3 / Parte VI").
**NON è fonte**: la spec v1, né alcuna sua riga. Non è autoritativa, non è baseline, non si trascrive, non si cita.
**Niente schema `[DOC-INTERNO file:riga]`** (abbandonato): i richiami puntano a GA_Metodologia_v2 per capitolo. Il codice del repo (decoder) **non è una fonte concorrente**: compare solo come superficie di PROVE/esclusione dentro RM-1/RM-2 (vedi Vincoli di metodo). Su un dubbio reale non risolvibile dal documento → **BLOCCO al Planner**, non citazione inventata.

---

## Mandato — perché ex novo (deciso, non in discussione)

Governance e indicazioni di task sono cambiate. La spec si **riscrive da zero da GA_Metodologia_v2**, non si emenda la v1. Tre vincoli di metodo del redo, tutti attivi:

- **N1 (atomicità)**: ogni requisito `R`/`NFR`/`CN` esprime **una sola proposizione verificabile**. Nessun composito (soglia + condizione + conseguenza) sepolto nella prosa: va spezzato in più ID con tracciabilità propria.
- **F6 (blocchi in batch)**: il Developer mappa **l'intero task** e raccoglie **tutti** i blocchi in un unico batch nel REPORT, non si ferma al primo.
- **Fedeltà a GA_Metodologia_v2 come asse #1 della Review** (vedi GATE sotto).

---

## Perimetro definito dal Planner (il Developer esegue, NON ridefinisce)

> Confine di ruolo: *Planner decide · Development non ridefinisce · Review non ripianifica*.

- **Perimetro**, **copertura-target** e **natura del track** sono **fissati qui dal Planner**. Il Developer li **consolida** in requisiti; non li ridefinisce.
- **Latitudine del Developer** = **solo** la *granularità di decomposizione* (N1) e l'*organizzazione interna* delle sezioni, documentata con rationale nel REPORT. **NON** il perimetro.
- Se il Developer trova: (a) un capitolo in-scope non rappresentabile, (b) una lacuna/contraddizione di perimetro, (c) un requisito che pare fuori da GA_Metodologia_v2 → **niente ri-scoping silenzioso**: apre un **BLOCCO** (batch F6) per il Planner.
- Il **Reviewer** audita **fedeltà a GA_Metodologia_v2** e **atomicità**; **non** valuta le scelte di perimetro (sono del Planner).

**Perimetro in-scope**: consolidamento in vista **prodotto-segnale** dei capitoli di GA_Metodologia_v2 pertinenti, ponte verso FASE-D, dentro PHASE-1 (FIB-only). Mappa di perimetro = le **10 sezioni** sotto.

---

## Copertura come GATE

Floor di copertura **ancorato a GA_Metodologia_v2**:

- Ogni **capitolo in-scope** dev'essere rappresentato nella spec da **≥1 requisito**, **oppure** marcato **esplicitamente out-of-scope con rationale** nel REPORT. **Mai omesso in silenzio.**
- Tabella nel REPORT: `Capitolo GA_Metodologia_v2 → {requisito/i ID}` oppure `{out-of-scope + rationale}`.
- **Nessun conteggio-target di requisiti**: il numero è quello che l'atomizzazione N1 dei capitoli in-scope produce.

---

## Fedeltà di tracciabilità come GATE esplicito

- Ogni richiamo punta al **capitolo/parte ESATTO** di GA_Metodologia_v2 che contiene il costrutto citato (verificato con **Read** dal Developer **prima** di scriverlo).
- Il Reviewer apre GA_Metodologia_v2 e verifica **TUTTI** i richiami — **verifica esaustiva**, fattibile in review statica, **non a campione**:
  - richiamo a un capitolo che **non risolve** (capitolo sbagliato / costrutto assente) = **BUG REALE**;
  - richiamo impreciso (risolve al capitolo ma non al costrutto puntuale) = **MIGLIORA-PROCESSO**.
- È l'**asse #1** della Review.

---

## Vincoli di metodo: RM-1 / RM-2 / RM-3 / RM-4 (governance, da `tasks/METODO.md`)

Le RM sono **regole di governance** definite in `tasks/METODO.md` — **non** in GA_Metodologia_v2 (che le *usa* soltanto). Sono vincolanti per Developer e Reviewer del redo. **Testo canonico = METODO.md.** Tutte e quattro nascono dall'incidente CANDLE (schema dato per "verificato" da 4 valori daily senza escludere le permutazioni, su fonte wiki errata, in uno script non-CAP mai revisionato); ciascuna tappa uno di quei buchi.

- **RM-1 — enumera ed escludi le alternative.** Ogni asserzione "verificato / confermato / stabilito X" enumera **esplicitamente** le alternative compatibili coi dati ed esclude ciascuna con evidenza puntuale. Enumerazione mancante = **BUG REALE anche se l'asserzione è vera**. Forma: blocco `VERIFICA: / PROVE: / ALTERNATIVE COMPATIBILI ESCLUSE: / ALTERNATIVE COMPATIBILI NON ESCLUSE:`. Aggancio: Developer in pre-consegna **e** Reviewer in audit.
- **RM-2 — cita il codice esistente + coerenza script↔documento.** Ogni claim su schemi-dato/codice cita i decoder già nel repo (`[CODICE-ESISTENTE path:linea]`) ed è coerente con ciò che il codice fa; verifica meccanica via grep, anche per output non-CAP; formato a 4 righe esigibile. Decoder che diverge dal documento (o non citato) = **BUG REALE**. Niente grep esplorativo per riscoprire i decoder già censiti.
- **RM-3 — fonti etichettate per livello; mai conclusioni wiki-only.** Ogni riferimento esterno è `[PROVA-EMPIRICA]` › `[CODICE-ESISTENTE]` › `[WIKI-HINT, da verificare]`. Conclusione strutturale appoggiata solo al livello 4 (wiki Directa / Telegram / Portara / CME / MiFID-II) senza supporto da un livello più forte = **BUG REALE**. Nota di testa: wiki Directa inaffidabile sullo schema CANDLE.
- **RM-4 — review anche dei non-CAP; instradamento Orchestratore.** Ogni output passa dal Reviewer, non solo i CAP: anche script/probe/handoff. L'Orchestratore li instrada **ex-ante** + **recupero retroattivo**, contro lista output esaustiva + criterio di estensione. Divisione Web/CLI per la probe-review (la sede Web non chiude le asserzioni empiriche; vanno in CLI). *In questo task: SPEC-FUNZ-01 è esso stesso un output non-CAP → passa dal Reviewer (Web-statico); lista Empirico-CLI attesa VUOTA.*

**Incrocio doc-vs-codice (RM-1 + RM-2)**: dove la spec asserisce uno schema-dato, il Reviewer confronta GA_Metodologia_v2 col **decoder canonico** per cogliere divergenze (non solo completezza). Decoder canonici (citare con `[CODICE-ESISTENTE path:linea]`, riverificati con Read; **non** greppare per riscoprirli):
`scripts/export_directa_history_parametric.py:471` (unpack `uff,min_,max_,ape` → close/low/high/open), `:477-481` (mappatura), `:605-617` (header CSV legacy **11 campi**), `:61` (`DEFAULT_INTRADAY_MAX_DAYS=100`); `scripts/probe_dapi.py:159/230/333`.

---

## Vincoli hard ereditati dalla metodologia (recepire, NON riaprire)

Tutti ancorati a GA_Metodologia_v2:

1. **Solo emissione, nessuna esecuzione ordini** (Cap.1 PI).
2. **1 contratto FIB alla volta** (Cap.2 PI).
3. **Tick FIB 5pt, moltiplicatore 5 EUR/pt**; prezzi/bande/target multipli di 5; b_min = 5 = 1 tick (Cap.2 PI, Cap.6 PII).
4. **Sessione 8:00–22:00 CET** continua (Q-01, Cap.52 P9).
5. **Operatore retail non-professionale MiFID II**, esecuzione manuale mobile, Directa DAPI, Telegram, 5 EUR/op (Cap.2 PI, Cap.46 P9).
6. **PHASE-1 = FIB-only**; PHASE-2 cross-index fuori scope (Cap.42 P8, Cap.55 P9).
7. **Vincolo segnale-attivo GLOBALE**: ‖A(t)‖ ≤ 1 — **NON** "per direzione" (Cap.6.3 / Cap.28 Parte VI).
8. **Q-04**: validità multiday del segnale eseguito ≤ 2 giorni trading dal raw touch.
9. **Q-05 (Opz. D)**: state machine = 1 non-terminale (`active`) + 6 terminali (`target_1_hit`/`stopped`/`invalidated`/`missed_target`/`expired`/`revoked`); `target_2` = informazione strutturale **pubblicata**, non variabile di lifecycle; position lifecycle post-`target_1` = **reporting-only** (Cap.11 PII).
10. **Rollover/storicizzazione** (P9/P10): `CONTRACT_SWITCH` (terza venerdì del mese di scadenza), 6 marker normativi, L_warmup=30gg, idempotenza T+3, cash low/high via CANDLE `f8/f9`, immutabilità barre storicizzate.
11. **M-2 OPEN** (latenza Telegram L_max=30s): incardinato come **NFR del prodotto**; la **verifica empirica** del valore resta **dipendenza aperta Appendice E / FASE-D**, **NON** risolta dal redo.
12. **Numerazione campi PRICE `f4/f6/f8/f9`** (M-9): ancorata a `[CODICE-ESISTENTE probe_dapi.py:…]` + capitolo dati di GA_Metodologia_v2.
13. **M-1/M-3** (CANDLE `C;L;H;O;V` + codici errore), **M-10** (BOOK_5 certificato): autoritativi.

---

## Sezioni da produrre

Perimetro **fissato dal Planner** (10 sezioni). Il Developer può **riorganizzare l'interno** con rationale nel REPORT — **fermo il floor di copertura** e il confine di ruolo. Ogni sezione chiude con mini-tabella `Requisito ID | Capitolo GA_Metodologia_v2 | Tipo (R/NFR/CN)`:

1. Scopo, visione, perimetro del prodotto.
2. Attori, contesto, personas.
3. Requisiti funzionali del segnale (payload ≥9 voci).
4. Ciclo di vita del segnale (state machine 1+6 in vista operatore).
5. Canale di pubblicazione e consegna (Telegram, NFR latenza, M-2).
6. Requisiti operativi e di sessione.
7. Requisiti di qualità e criteri di accettazione (KPI, DSR/PBO gate, checklist AC-GO).
8. Vincoli normativi e compliance.
9. Requisiti di dato e dipendenze infrastrutturali.
10. Fasizzazione, roadmap (senza date), matrice di tracciabilità (≥ righe pari ai requisiti).

---

## Acceptance criteria

### Generali (vincolanti)
`AC-G1` (RM-1: ogni "verificato X" enumera ed esclude le alternative; enumerazione mancante = BUG REALE anche se vera) · `AC-G2` (RM-3: fonti esterne etichettate per livello `[PROVA-EMPIRICA]`/`[CODICE-ESISTENTE]`/`[WIKI-HINT]`; nessuna conclusione wiki-only) · `AC-G3` (RM-2: claim su schemi/codice citano i decoder esistenti `[CODICE-ESISTENTE path:linea]`, coerenti col codice, grep-checkable; niente grep esplorativo sui decoder già censiti) · `AC-G4` (ogni requisito tracciato a un capitolo di GA_Metodologia_v2) · `AC-G5` (matrice completa + capitoli non tracciati motivati) · `AC-G6` (no contraddizioni con GA_Metodologia_v2) · `AC-G7` (valore operativo per requisito) · `AC-G8` (M-2 incardinato come dipendenza aperta) · `AC-G9` (out-of-scope sistematico) · `AC-G10` (concisione prioritaria; nessun cap rigido di pagine — l'atomizzazione N1 può portare oltre ~16pp ed è accettabile se annotato) · `AC-G11` (italiano formale/conciso) · `AC-G12` (formato/commit) · `AC-G13` (Reviewer applica RM-1 a sé) · `AC-G14` (Reviewer non riapre GA_Metodologia_v2 nel merito metodologico) · `AC-G15` (RACC-METODO-2: se la spec cita uno schema-dato esterno, il Reviewer verifica il **diff col decoder canonico**, non la sola completezza).

### Specifici dell'ex novo
- **AC-X1 (N1 atomicità)**: ogni `R`/`NFR`/`CN` = una proposizione verificabile; nessun composito nella prosa. Il Reviewer caccia i compositi → "da spezzare" = finding.
- **AC-X2 (fedeltà esaustiva)**: ogni richiamo punta al capitolo/parte esatto di GA_Metodologia_v2; il Reviewer verifica **TUTTI** i richiami; non-risolvente = BUG REALE, impreciso = MIGLIORA-PROCESSO.
- **AC-X3 (consolidamento dal documento)**: il REPORT dichiara che la spec è consolidata **da GA_Metodologia_v2** (non dalla v1) e include la **tabella di copertura capitolo→requisiti**.
- **AC-X4 (confine di ruolo)**: **nessuna decisione di perimetro** presa dal Developer; ogni questione di perimetro è un **BLOCCO** per il Planner (batch F6).

---

## Out-of-scope (il Developer NON include)

Riderivare matematica del modello (EGARCH/Cox/NSGA-II/DSR/PBO) · ridichiarare schemi DAPI · parametri congelati del cromosoma · implementazione FASE-D · PHASE-2 cross-index · consulenza legale / testo disclaimer · contratti vendor · tutorial operatore · analisi di mercato · roadmap con date · riapertura M-2 · **modifica `00_indice.md`** (eventuale rinvio = decisione Planner a chiusura PASS) · apertura `Q-XX` (solo per ambiguità reale non risolvibile da GA_Metodologia_v2) · **lettura della v1 come fonte/baseline** · **ri-scoping del perimetro** (è del Planner).

---

## Done when

La spec PASS:
- **copre ogni capitolo in-scope** (rappresentato o out-of-scope-con-rationale);
- risponde univocamente alle domande operative di prodotto (prodotto / consumatore / payload / lifecycle / consegna+SLA / sessione / successo / compliance / dati / roadmap+tracciabilità / tracciabilità per requisito / valore per requisito / no-contraddizioni / M-2 / capitoli non tracciati);
- **ogni requisito è atomico (N1)**;
- **ogni richiamo a GA_Metodologia_v2 è al capitolo esatto** (AC-X2, verifica **esaustiva** del Reviewer);
- **nessuna decisione di perimetro è stata presa fuori dal Planner** (AC-X4).

---

## REPORT — 5 sezioni (formato supervisore)

1. **Sintesi esecutiva** — cosa è stato consolidato, da quali capitoli, esito complessivo.
2. **Tabella di copertura capitolo→requisiti** — ogni capitolo in-scope rappresentato (con ID requisiti) o out-of-scope con rationale.
3. **Decisioni di granularità e organizzazione** — latitudine N1 esercitata, ristrutturazioni interne, con rationale.
4. **Blocchi / Domande aperte** — batch F6 unico (vuoto se nessuno).
5. **Tabella verifica AC** — `AC-G1..G15` + `AC-X1..X4`: stato per ciascuno.

---

## Precondizioni di promozione (chiudere PRIMA che l'Orchestratore committi come `ACTIVE_TASK.md`)

- Lo **slot task-attivo globale è LIBERO** (nessun task sospeso che tiene lo slot → rischio freeze).

---

## Pipeline attesa

```
Planner (questa task card)  →  Orchestratore committa la task card come ACTIVE_TASK.md
Developer — giro 1 del redo (Web): SCRIVE EX NOVO docs/spec_funzionale/SPEC_FUNZ_01.md
            + reports/REPORT_SPEC_FUNZ_01.md; push origin/main; DEV_STATUS=READY_FOR_REVIEW
Orchestratore: check post-Developer (commit copre SPEC+REPORT+DEV_STATUS; indice = N/A)
Reviewer — giro 1 del redo (Web, statico, DUE passate ostili a tappeto entro la singola Review)
            →  PASS / CONDITIONAL / FAIL
  • CONDITIONAL/FAIL → punto di controllo supervisore (classificazione finding) → fix → re-review
  • PASS → chiusura standard del track (indice N/A); la v1 resta storica in git, non citata
```
