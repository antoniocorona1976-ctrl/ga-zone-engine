> ⚠️ **BOZZA — NON È IL TASK ATTIVO.** Proposta di task card per il REDO ex novo di SPEC-FUNZ-01.
> Diventa operativa solo quando il supervisore dà il GO e l'Orchestratore la promuove a `tasks/ACTIVE_TASK.md` (committandola), **oppure** la passa a `spec_planner` per l'affinamento. Finché vive con questo nome, la macchina a stati NON la legge (chiave di stato = solo `ACTIVE_TASK.md`).

# TASK ATTIVO: SPEC-FUNZ-01 (REDO ex novo) — Specifica funzionale del prodotto-segnale FIB (PHASE-1)

**Assegnato da**: Planner (track business-spec)
**Tipo**: **REDO ex novo che SOVRASCRIVE** `docs/spec_funzionale/SPEC_FUNZ_01.md`. La v1 PASS resta nella storia git e NON va cancellata né citata come fonte da copiare.
**Output atteso**: `docs/spec_funzionale/SPEC_FUNZ_01.md` (riscrittura integrale) + `reports/REPORT_SPEC_FUNZ_01.md` (riscrittura, 5 sezioni formato supervisore + tabella verifica AC).
**Stato**: IN ATTESA
**Workflow**: Standard `Planner → Developer → Reviewer`, con agenti `spec_*` **induriti N1+F6** (innesto `d8cbca3`, successivo alla chiusura v1).
**Sede Reviewer**: **WEB-statico** (documento + grep + Read dei CAP/decoder committati; nessun DAPI). Lista "Empirico-CLI da verificare" attesa **VUOTA**. CLI disponibile solo se una sezione richiedesse verifica empirica (non previsto).
**Modalità di review**: **CAP-review piena adattata al non-CAP, due giri ostili a tappeto** (NON re-review leggera: è un documento nuovo, non un micro-pass).

## Riferimenti alla v1 (storia git — input, non fonte da trascrivere)
- Task card v1: `7604445` · Developer v1: `e08409b` (531 righe doc) · Review v1 PASS: `d8a40a0` (0 BUG REALE, 3 NEUTRO) · Dev v2 micro-pass: `314dd1b` · Re-Review v2 PASS: `a16a4c0` · Chiusura: `1673160`.
- Esito v1: 10 sezioni, **36 requisiti** R/NFR/CN, matrice di tracciabilità 36 righe. PASS con 3 osservazioni NEUTRO di igiene-citazione (OM-1/2/3, vedi §"Correzioni note").

---

## Mandato del redo — le tre motivazioni (tutte attive)

**(M-A) Governance indurita — scope-method.**
- **N1 (atomicità)**: ogni requisito `R`/`NFR`/`CN` esprime **una sola proposizione verificabile**. Ogni requisito v1 che impacchetta più concern (soglia + condizione + conseguenza) va **spezzato** in più ID con tracciabilità propria. Conseguenza attesa: il conteggio requisiti del redo è **≥ 36** (i compositi si dividono).
- **F6 (blocchi in batch)**: il Developer mappa **l'intero task** e raccoglie **tutti** i blocchi in un unico batch nel REPORT (sezione "Blocchi / Domande aperte"), non si ferma al primo.

**(M-B) Ripensare lo scope nel merito.** Il Developer **NON trascrive** la v1: ri-consolida **da zero** i CAP chiusi PASS (Parti I–X, Cap.1–65) in vista prodotto. La struttura a 10 sezioni della v1 è **baseline di riferimento**, non un vincolo: perimetro, granularità, copertura e set di requisiti vanno **riconsiderati sul merito**, restando dentro la natura del track (consolidamento di metodologia chiusa in requisiti di prodotto; ponte verso FASE-D; nessuna riapertura dei CAP). Vincolo di **non-regressione di copertura** (AC-REDO-5): ogni requisito v1 dev'essere nel redo **carried / split / dropped-with-rationale**, mai perso in silenzio.

**(M-C) Re-run pulito di processo.** Ciclo completo fresco, nessuna scorciatoia. Il Reviewer riparte da **audit a tappeto** (asse #1 = fedeltà di tracciabilità), non da re-review leggera. La v1 non è autoritativa: autoritativi sono i **CAP chiusi**.

---

## Fedeltà di tracciabilità come GATE esplicito (chiude F1 dell'audit 4-canali)

Lezione di v1 (OM-1): diverse citazioni puntavano alla **riga di intestazione del capitolo o adiacente**, non alla riga esatta del costrutto. Nel redo questo è un **gate**, non una tolleranza:
- Ogni `[DOC-INTERNO CAP_XX:riga]` punta alla **riga ESATTA** che contiene il costrutto citato (verificata con Read token-per-token dal Developer prima di scriverla).
- Il Reviewer apre i CAP e verifica un **campione esteso**: citazione a riga di header/adiacente (che risolve al capitolo ma non alla riga) = **MIGLIORA-PROCESSO** (minimo); citazione che **non risolve** (capitolo sbagliato / costrutto assente) = **BUG REALE**.

---

## Correzioni note da incorporare (input autoritativo dalla Review v1 `a16a4c0` — già verificate dal Reviewer)

| ID v1 | Difetto v1 | Correzione obbligatoria nel redo |
|---|---|---|
| **OM-1** | 6 citazioni Sez.9/10 a riga di header/adiacente | Usare le righe **esatte** già identificate: `CAP_10:5` (invariante research=runtime esteso al tape), `CAP_10:76` (limite ~100gg, Cap.59), `CAP_10:161` (Step C fallback Portara, Cap.61), `CAP_10:236` (cross-index PHASE-2 fuori scope), `CAP_10:233` (riavvio Darwin mezzanotte), `CAP_07:576` (AC-GO-4 lifecycle cross-regime). Applicare lo standard riga-esatta **ovunque**. |
| **OM-2** | `R-17` "singolo segnale attivo **per direzione**": wording lasco | Enunciare il vincolo chiuso **globale** $\|\mathcal{A}(t)\|\le 1$ (Cap.6.3 / Cap.28 Parte VI, `[DOC-INTERNO CAP_02_parte_II.md:81]`, cfr. `:87` "elimina tutte le politiche multi-segnale concorrente") **senza** "per direzione". |
| **OM-3** | Ancora `fN` schema PRICE imprecisa | Ancorare la numerazione `f4/f6/f8/f9` a **`tasks/STATO_CORRENTE.md:76` (M-9)** come fonte puntuale, oltre al richiamo descrittivo `[DOC-INTERNO CAP_09_parte_9.md:94]`. |

---

## Eredità obbligatoria (da metodologia v2 chiusa, QUESTIONS chiuse, CARRYOVER)

Il **censimento integrale** dell'eredità (25 voci) del task card v1 (`7604445`) resta **valido e autoritativo** come input: il Planner del redo lo eredita per intero. Vincoli **hard** da non riaprire e da recepire (sintesi):

1. **Solo emissione, nessuna esecuzione ordini** (Cap.1 Parte I). · 2. **1 contratto FIB alla volta** (Cap.2 Parte I). · 3. **Tick FIB 5pt, moltiplicatore 5 EUR/pt**; prezzi/bande/target multipli di 5; $b_{min}=5$ = 1 tick (Cap.2 PI, Cap.6 PII). · 4. **Sessione 8:00–22:00 CET** continua (Q-01, Cap.52 P9). · 5. **Operatore retail non-professionale MiFID II**, esecuzione manuale mobile, Directa DAPI, Telegram, 5 EUR/op (Cap.2 PI, Cap.46 P9). · 6. **PHASE-1 = FIB-only**; PHASE-2 cross-index fuori scope (Cap.42 P8, Cap.55 P9).
7. **Q-04**: validità multiday segnale eseguito ≤ 2 giorni trading dal raw touch. · 8. **Q-05 (Opz. D raffinata)**: state machine = 1 non-terminale (`active`) + 6 terminali (`target_1_hit`/`stopped`/`invalidated`/`missed_target`/`expired`/`revoked`); `target_2` = informazione strutturale pubblicata, non variabile di lifecycle; position lifecycle post-target_1 = reporting-only (Cap.11 PII). · 9–13. **D-9-NB2/NB3/NB4, D-10-2/4/8** ecc.: rollover `CONTRACT_SWITCH` (terza venerdì del mese di scadenza), 6 marker normativi, $L_{warmup}=30$gg, idempotenza T+3, cash low/high via CANDLE `f8/f9`, immutabilità barre storicizzate.
14–17. **RM-1..RM-4** (vedi §"Vincoli di metodo"). · 18. **M-2 OPEN** (latenza Telegram $L_{max}=30$s): incardinato come **NFR del prodotto** (Sez. consegna); la **verifica empirica** del valore resta **dipendenza aperta Appendice E / FASE-D**, NON risolta dal redo. · 21–22. **RACC-METODO-2**: se la spec cita uno schema-dato esterno, il Reviewer verifica il **diff col decoder canonico**, non la sola completezza. · 23–25. **M-9 (PRICE `f4/f6/f8/f9`)**, **M-10 (BOOK_5 certificato)**, **M-1/M-3 (CANDLE `C;L;H;O;V` + codici errore)**: autoritativi.

**Decoder canonici già censiti** (citare con `[CODICE-ESISTENTE path:linea]`, riverificati con Read; **non** greppare per riscoprirli): `scripts/export_directa_history_parametric.py:467-481` (CANDLE `C;L;H;O`), `:605-617` (header CSV legacy **11 campi**), `:61` (`DEFAULT_INTRADAY_MAX_DAYS=100`), `:282-285`, `:605-617`; `scripts/probe_dapi.py:159/230/333`.

---

## Vincoli di metodo (RM-1 / RM-2 / RM-3)
- **RM-1**: il redo **NON introduce** dichiarazioni "verificato X" di prima istanza. Ogni asserzione fattuale è un **richiamo etichettato** a un CAP chiuso (`[DOC-INTERNO CAP_XX:riga]`, `[CODICE-ESISTENTE path:linea]`, `[PROVA-EMPIRICA data via CAP]`). Un "verificato X" senza richiamo = **BUG REALE**.
- **RM-2**: citazioni di codice puntuali e riverificate con Read prima di scriverle (token-per-token).
- **RM-3**: ogni riferimento a wiki Directa / docs Telegram / Portara / CME / MiFID-II è `[WIKI-HINT, da verificare]`; nessuna conclusione strutturale appoggiata solo a livello 4. Nota di testa con avvertenza esplicita di inaffidabilità della wiki Directa sullo schema CANDLE (eredità AUDIT-RM CAP-DATA-02).

---

## Sezioni da produrre — baseline v1 (da riconsiderare sul merito, M-B)

Struttura **di riferimento** (10 sezioni della v1), ognuna con mini-tabella di tracciabilità `Requisito ID | Capitolo metodologia v2 | Tipo` a fine sezione. Il Developer può **ristrutturare** con rationale documentato nel REPORT, fermo restando il floor di copertura (AC-REDO-5):

1. Scopo, visione, perimetro del prodotto. · 2. Attori, contesto, personas. · 3. Requisiti funzionali del segnale (payload ≥9 voci). · 4. Ciclo di vita del segnale (state machine 1+6 in vista operatore). · 5. Canale di pubblicazione e consegna (Telegram, NFR latenza, M-2). · 6. Requisiti operativi e di sessione. · 7. Requisiti di qualità e criteri di accettazione (KPI, DSR/PBO gate, checklist AC-GO). · 8. Vincoli normativi e compliance. · 9. Requisiti di dato e dipendenze infrastrutturali. · 10. Fasizzazione, roadmap, matrice di tracciabilità (≥ righe pari ai requisiti).

---

## Acceptance criteria

### Ereditati dalla v1 (restano vincolanti)
`AC-G1` (no "verificato X" nuovi) · `AC-G2` (fonti esterne `[WIKI-HINT]`) · `AC-G3` (citazioni codice puntuali ≤5) · `AC-G4` (ogni requisito tracciato a un capitolo) · `AC-G5` (matrice completa + capitoli non tracciati motivati) · `AC-G6` (no contraddizioni coi CAP chiusi) · `AC-G7` (valore operativo per requisito) · `AC-G8` (M-2 incardinato come dipendenza aperta) · `AC-G9` (out-of-scope sistematico) · `AC-G10` (12–16 pp) · `AC-G11` (italiano formale/conciso) · `AC-G12` (formato/commit) · `AC-G13` (Reviewer applica RM-1 a sé) · `AC-G14` (Reviewer non riapre i CAP) · `AC-G15` (RACC-METODO-2).

### Nuovi, specifici del redo
- **AC-REDO-1 (N1 atomicità)**: ogni `R`/`NFR`/`CN` = una proposizione verificabile; nessun composito sepolto nella prosa. Il Reviewer (asse 6) caccia i compositi → "da spezzare" = finding.
- **AC-REDO-2 (fedeltà riga-esatta)**: ogni `[DOC-INTERNO CAP:riga]` punta alla riga **esatta** del costrutto; campione esteso aperto dal Reviewer; header/adiacente = MIGLIORA-PROCESSO, non-risolvente = BUG REALE.
- **AC-REDO-3 (no trascrizione v1)**: il REPORT dichiara esplicitamente il ri-consolidamento dai CAP (non dalla v1) e documenta le differenze sostanziali vs v1 (requisiti aggiunti / spezzati / rimossi, con rationale).
- **AC-REDO-4 (OM v1 chiusi)**: OM-1, OM-2, OM-3 risolti come da §"Correzioni note".
- **AC-REDO-5 (non-regressione di copertura)**: tabella nel REPORT che mappa **ogni requisito v1 → stato nel redo** (carried / split-in {IDs} / dropped + rationale). Nessuna perdita silenziosa.

---

## Out-of-scope (Developer NON include) — invariato da v1 + redo
Riderivare matematica del modello (EGARCH/Cox/NSGA-II/DSR/PBO) · ridichiarare schemi DAPI · parametri congelati del cromosoma · implementazione FASE-D · PHASE-2 cross-index · consulenza legale / testo disclaimer · contratti vendor · tutorial operatore · analisi di mercato · roadmap con date · riapertura M-2 · **modifica `00_indice.md`** (eventuale rinvio = decisione Planner a chiusura PASS) · apertura `Q-XX` (solo per ambiguità reale non risolvibile) · audit retroattivo dei CAP chiusi · nuova probe empirica. **Per ogni voce: destinazione come da task card v1.**

## Done when
La spec PASS risponde univocamente alle 15 domande operative della v1 (prodotto / consumatore / payload / lifecycle / consegna+SLA / sessione / successo / compliance / dati / roadmap+tracciabilità / tracciabilità per requisito / valore per requisito / no-contraddizioni / M-2 / capitoli non tracciati), **e in più**: ogni requisito è atomico (N1), ogni citazione è a riga esatta (AC-REDO-2), la copertura non regredisce rispetto a v1 (AC-REDO-5).

## Pipeline attesa
```
Planner (questo task card)  →  Orchestratore committa il task card come ACTIVE_TASK.md
Developer v1 (Web): RISCRIVE docs/spec_funzionale/SPEC_FUNZ_01.md + reports/REPORT_SPEC_FUNZ_01.md; push origin/main; DEV_STATUS=READY_FOR_REVIEW
Orchestratore: check post-Developer (6 controlli; indice=N/A; commit copre SPEC+REPORT+DEV_STATUS)
Reviewer v1 (Web, statico, 2 giri ostili a tappeto)  →  PASS / CONDITIONAL / FAIL
  • CONDITIONAL/FAIL → punto di controllo supervisore (classificazione finding) → fix → re-review
  • PASS → chiusura 7 condizioni adattate (indice N/A); v1 PASS resta storica in git
```