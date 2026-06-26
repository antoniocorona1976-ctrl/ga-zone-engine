# TASK ATTIVO: SPEC-FUNZ-01-ASSEMBLY — Assemblaggio loss-less della serie B1..B8 in un unico documento di specifica funzionale autoritativo

> **Track**: Business-spec (SPEC-FUNZ). **Sede**: CLI (GOV-SURFACES-01, METODO §Superfici). **Tag commit**: `[SPEC-FUNZ-01-ASSEMBLY]`. **Modalità**: MERGE editoriale **NON cieco** (Planner e Developer leggono tutti i blocchi e la mappa).
>
> **Natura**: questo NON è un capitolo metodologico, NON è una ricostruzione cieca, NON è l'avvio di FASE-D. È il **merge fedele e loss-less** degli 8 blocchi B1..B8 (già scritti e già passati in review) in un unico documento. Il valore del task è la **fedeltà** (0 requisiti persi, 0 inventati), non la produzione di materia nuova.

---

## 0. Conferma letture obbligatorie (Planner)

Confermo di aver letto, in quest'ordine, prima di scrivere questa card:
1. `tasks/METODO.md` — RM-1..RM-4 + Freeze G-09 + §Superfici GOV-SURFACES-01 + RACC-METODO-2 + Precedenza documenti.
2. `.claude/BASE_COMUNE.md` — ciclo Planner→Developer→Reviewer, sede CLI per la spec, classificazione finding, check post-Developer (condizione-3 indice = N/A), registry.
3. `.claude/agents/spec_planner.md` — il mio ruolo.
4. `tasks/STATO_CORRENTE.md` — serie B1..B8 chiusa PASS + AUDITFIX-01 CHIUSO PASS `392a3f5`; conteggi blocchi aggiornati (B3=63, B5=35, B6=72, B8=18).
5. `tasks/CARRYOVER.md` — M-promemoria + eredità AUDITFIX-01 (debito v2 → assemblaggio).
6. `docs/spec_funzionale/PROPOSTA_SUDDIVISIONE_SPEC_v2.md` — mappa di chunking, partizione 75 req-v2 1-a-1.
7. Tutti e 8 i blocchi `SPEC_FUNZ_01_B1.md` .. `SPEC_FUNZ_01_B8.md` (letti per intero / per le parti load-bearing: intestazioni, schemi-ID, requisiti, matrici, note di rinvio, conteggi).
8. La v2 da archiviare `docs/spec_funzionale/SPEC_FUNZ_01.md` (struttura a 10 Sezioni + matrice §11 + Sez.12 capitoli non tracciati + Sez.13 blocchi aperti).

---

## 1. Scopo e domande operative a cui l'assemblato deve rispondere univocamente

Produrre **un unico documento di specifica funzionale** `docs/spec_funzionale/SPEC_FUNZ_01.md` che **rimpiazza** la v2 corrente, ottenuto dal merge loss-less degli 8 blocchi B1..B8 (post-AUDITFIX-01). L'assemblato deve rispondere univocamente a:

- *Quali sono TUTTI i requisiti di prodotto del motore di segnali FIB (PHASE-1 FIB-only)?* — e ognuno deve essere rintracciabile 1-a-1 al suo ID-blocco originario e alla sua riga-CAP.
- *Dove vive ciascun requisito nelle 10 Sezioni di prodotto?* (struttura ereditata dalla v2, vedi §4).
- *Qual è la matrice di tracciabilità unica requisito→capitolo metodologia v2 dell'intero prodotto?*
- *Quali materie restano fuori scope e con quale destinazione (FASE-D / validator / PHASE-2 / CAP chiusi)?*
- *Quali dipendenze/blocchi restano aperti (PENDING-empirico) e dove sono rinviati?*

**Reinterpretazione del criterio di valore (track business-spec)**: ogni requisito dell'assemblato traccia simultaneamente a (a) un **valore operativo/di prodotto** per l'operatore retail FIB (già presente in ogni requisito-blocco, da preservare verbatim o in sintesi fedele) E (b) un **capitolo della metodologia v2** di origine (già presente nella citazione `[DOC-INTERNO CAP_XX:riga]` di ogni requisito-blocco, da preservare e mantenere risolvibile). Un requisito senza tracciabilità o senza valore operativo è un difetto di assemblaggio.

---

## 2. Perimetro: gli 8 blocchi + la mappa di chunking

**Perimetro-fonte dell'assemblaggio = gli 8 documenti-blocco** (questi sono la fonte autoritativa del merge, NON i CAP — i CAP restano congelati, freeze G-09):

| Blocco | File | Conteggio attuale (post-AUDITFIX-01) — riferimento di completezza |
|---|---|---|
| B1 — Ambito & operatore | `docs/spec_funzionale/SPEC_FUNZ_01_B1.md` | **34** (25 R + 5 CN + 4 NFR) — matrice §7.1, conteggio `:272` |
| B2 — Payload del segnale | `docs/spec_funzionale/SPEC_FUNZ_01_B2.md` | **42** (37 R + 5 CN, 0 NFR) — matrice §8.1 |
| B3 — State-machine & lifecycle | `docs/spec_funzionale/SPEC_FUNZ_01_B3.md` | **63** (48 R + 12 CN + 3 NFR) — include `B3-R-48` (AUDITFIX F2, Cap.11.5) |
| B4 — Emissione & consegna Telegram | `docs/spec_funzionale/SPEC_FUNZ_01_B4.md` | **61** (40 R + 14 CN + 7 NFR) — `:472` — include estensione B4-EXT Cap.29 |
| B5 — Runtime DAPI, sessione & compliance | `docs/spec_funzionale/SPEC_FUNZ_01_B5.md` | **35** (20 R + 9 CN + 7 NFR) — `:281` — include ancora corretta B5-CN-05→`CAP_09_parte_9.md:290` (AUDITFIX F3) |
| B6 — Schema-dato DAPI & continuità tape | `docs/spec_funzionale/SPEC_FUNZ_01_B6.md` | **72** (43 R + 25 CN + 4 NFR) — `:455` — include `B6-R-38..43` + `B6-CN-25` (AUDITFIX F1 Cap.49 + F4 encoding + F5 backfill marker) |
| B7 — Gate di go-live | `docs/spec_funzionale/SPEC_FUNZ_01_B7.md` | **49** (38 R + 7 CN + 4 NFR) — conteggio `:384` |
| B8 — Confine / fasizzazione PHASE-2 | `docs/spec_funzionale/SPEC_FUNZ_01_B8.md` | **18** (13 R + 5 CN, 0 NFR) — include `B8-R-13` (AUDITFIX F6, dip. CANDLERANGE T+3) |

**Totale atteso dell'assemblato = 34 + 42 + 63 + 61 + 35 + 72 + 49 + 18 = 374 requisiti-blocco** (riferimento di completezza per il Reviewer). Conteggi **verificati dal Planner leggendo i file**: sono riferimento autoritativo, ma il Developer deve **ricontarli sui file** (l'aritmetica finale dell'assemblato è verità di documento, non di card), non assumerli ciecamente.

> **Nota AUDITFIX-01 (autoritativa, non riverificare)**: i 6 difetti che vivevano nei blocchi sono già stati chiusi nei file-blocco e coperti dalla review `392a3f5`. I marcatori PASS originali dei blocchi (B3 `10ade01`, B5 `5ec899c`, B6 `a5cfa80`, B8 `09cc7d9`) restano storici; lo stato corrente dei file è quello post-AUDITFIX. L'assemblato parte **dallo stato corrente dei file-blocco**, già emendato.

> **Riconciliazione mappa-Orchestratore ↔ file di chunking (`PROPOSTA_SUDDIVISIONE_SPEC_v2.md`)**: la mappatura blocchi→sezioni di §4 (B1→Sez.1+2, B2→Sez.3, B3→Sez.4, B4→Sez.5+6, B5→Sez.7, B6→Sez.9, B7→Sez.8, B8→Sez.10) **coincide** con il file di chunking (tabella §4 di `PROPOSTA_SUDDIVISIONE_SPEC_v2.md:101-110`: B6=Sez.9, B7=Sez.8, gli altri 1-a-1). **Nessuna discrepanza rilevata.** Punto di attenzione per Developer/Reviewer: l'**ordine numerico delle Sezioni** (1→10) NON coincide con l'ordine dei blocchi (B6 popola Sez.9, B7 popola Sez.8 — le Sezioni 8 e 9 sono "incrociate" rispetto all'ordine B7/B8). Il Developer dispone le Sezioni in **ordine numerico 1→10** (struttura v2), non in ordine di blocco.

---

## 3. Parametri di output e archiviazione (AUTORITATIVI — preparati dall'Orchestratore, NON riverificare)

Input autoritativo (CLAUDE.md §"Input dell'Orchestratore = autoritativo"); il Developer li rispetta alla lettera, non li ridiscute:

1. **Rimpiazzo**: l'assemblato **RIMPIAZZA** `docs/spec_funzionale/SPEC_FUNZ_01.md` (la v2 corrente). L'output del Developer è scritto su quel path.
2. **Archiviazione della v2**: PRIMA del rimpiazzo, la v2 corrente va **archiviata** come copia/rename in `docs/spec_funzionale/SPEC_FUNZ_01_v2_storico.md` (esattamente come v1→v2 con `_v1_storico`).
3. **Tag git** sulla v2 storica: `spec-funz-01-v2-storico` (esattamente come `spec-funz-01-v1-storico` per la v1; vedi CARRYOVER M-GOV-2 e STATO 2026-06-14).
4. **Report**: `reports/REPORT_SPEC_FUNZ_01_ASSEMBLY.md` (5 sezioni formato supervisore + tabella AC, vedi §12.B).
5. **Tag commit**: `[SPEC-FUNZ-01-ASSEMBLY]`. Tutto su `main` (trunk), sede CLI.
6. **`docs/methodology_v2/00_indice.md` NON si tocca** (SPEC-FUNZ non è una Parte; condizione-3 del check post-Developer = N/A).

---

## 4. Struttura: le 10 Sezioni della v2, popolate dai blocchi (mappatura AUTORITATIVA)

L'assemblato adotta la **struttura a 10 Sezioni di prodotto della v2** (Sez.1..Sez.10), in **ordine numerico 1→10**, popolate dai blocchi secondo la mappatura seguente (preparata dall'Orchestratore, autoritativa):

| Blocco | Sezione/i di destinazione | Tema |
|---|---|---|
| B1 | **Sez.1 + Sez.2** | Obiettivo di prodotto / vincolo "solo emissione" (Sez.1) + Destinatario e modalità di consumo (Sez.2) |
| B2 | **Sez.3** | Payload del segnale |
| B3 | **Sez.4** | State-machine & lifecycle del segnale |
| B4 | **Sez.5 + Sez.6** | Condizioni/regola di emissione (Sez.5) + Consegna Telegram (Sez.6) |
| B5 | **Sez.7** | Runtime DAPI, sessione & compliance |
| B7 | **Sez.8** | Gate di go-live |
| B6 | **Sez.9** | Schema-dato DAPI & continuità tape |
| B8 | **Sez.10** | Confine / fasizzazione PHASE-2 & dipendenze aperte verso FASE-D |

Oltre alle 10 Sezioni di requisiti, l'assemblato conserva le **sezioni di servizio della v2**:
- **Nota di testa** (provenienza e cautele di fonte RM-1/RM-3) — aggiornata per riflettere lo stato post-blocchi (SHA CAP pinnabili: i blocchi pinnano CAP-01 `b76c32c`, CAP-02 `a1625df`, CAP-07 `b27c1e3`, CAP-01 Cap.5 via `e8d5424`, CAP-09 `28cfd2d`, CAP-10 `41447d3`, CAP-08 `015c47a`, CAP-06 `d3f029d`; il Developer riporta gli SHA effettivi presenti nei blocchi-fonte, **senza inventarne** — RM-1).
- **Sezione matrice di tracciabilità UNICA** (= Sez.11 v2): una riga per ogni requisito dell'assemblato, con ID-assemblato, citazione `[DOC-INTERNO CAP:riga]`, capitolo/Parte. + **tabella di mapping ID-assemblato ↔ ID-blocco** (vedi §5).
- **Sezione capitoli non tracciati** (= Sez.12 v2): conserva la motivazione per ogni capitolo metodologia v2 NON tracciato a un requisito (Parti III/IV/V interne, ecc.). Il Developer la **ricostruisce dalla v2** (materia di servizio, non un requisito-blocco) verificando che le motivazioni restino coerenti coi blocchi.
- **Sezione blocchi/dipendenze aperte** (= Sez.13 v2): B-1 (latenza Telegram, M-2 OPEN), B-2 (orario sessione, M-GOV-1 APERTO), + le dipendenze aperte enumerate da B8 (vedi §6.2).

> **Nota di confine (split B4→Sez.5/Sez.6)**: B4 è internamente diviso in parte CAP_02 Cap.8-9 (emissione + consegna base) + estensione B4-EXT Cap.29 (consegna mobile-first + 3 notifiche). Nell'assemblato: la materia di **emissione** (3 condizioni, filtro 80pt come regola, regola AND, non-emissione, assenza filtri post-emissione) → **Sez.5**; la materia di **consegna Telegram** (contratto messaggio, ordine campi, latenza, anti-duplicato, notifica trigger, errori, mobile-first, 3 notifiche standard) → **Sez.6**. Lo split B4→Sez.5/Sez.6 è **per concern**, senza perdere né duplicare alcun requisito B4. Confine fine: B4-R-16 "nessuna fase speciale per orario" e B4-CN-01/05 (assenza filtri post-emissione) appartengono all'emissione → Sez.5.

---

## 5. Schema-ID dell'assemblato + tabella di mapping (decisione del Planner)

**Schema-ID scelto: sezione-based `R-x.y` / `NFR-x.y` / `CN-x.y`** (come la v2), dove `x` è il numero di Sezione (1..10) e `y` è progressivo dentro la sezione per famiglia. Esempi: `R-3.1` (primo requisito funzionale della Sez.3 = payload); `CN-7.2`; `NFR-8.5`.

**Vincoli sullo schema-ID (acceptance per il Developer)**:
- (a) **Nessun requisito-blocco perso**: ognuno dei 374 requisiti-blocco `B?-R/CN/NFR-NN` mappa a **esattamente un** ID-assemblato.
- (b) **Ogni ID-assemblato è tracciabile** sia al suo ID-blocco di origine (`B?-…-NN`) sia alla sua riga-CAP originaria (`[DOC-INTERNO CAP_XX:riga]`).
- (c) **Atomicità preservata (N1)**: un requisito-blocco atomico resta un ID-assemblato atomico. L'assemblaggio **non fonde** due requisiti-blocco distinti in un solo ID-assemblato (perdita di atomicità/tracciabilità) e **non spezza** un requisito-blocco atomico in due (invenzione). Mappatura **1-a-1** requisito-blocco ↔ requisito-assemblato. *(Unica eccezione ammessa: due requisiti-blocco di blocchi diversi che sono **letteralmente lo stesso fatto** perché premessa condivisa duplicata — vedi §7 AC-ASM-3 — vanno collassati in un solo ID-assemblato con doppia tracciabilità; NON è perdita, è dedup, e va dichiarata esplicitamente nella tabella di mapping con motivazione.)*

**Tabella di mapping OBBLIGATORIA** (sezione dedicata dell'assemblato o appendice): per ogni ID-assemblato, la riga `ID-assemblato | ID-blocco originario (B?-…-NN) | citazione CAP | (se dedup) altri ID-blocco collassati + motivazione`. È ciò che rende il merge **verificabile come loss-less** dal Reviewer: deve coprire tutti i 374 requisiti-blocco (eventualmente meno ID-assemblato se dedup premesse, con la riga di dedup che enumera gli ID-blocco assorbiti).

---

## 6. Eredità obbligatoria (vincoli hard autoritativi + censimento M)

### 6.1 Vincoli hard dai CAP chiusi e dalle decisioni AC (autoritativi, NON ri-verificare)

- **Freeze G-09**: i CAP `docs/methodology_v2/CAP_*` chiusi PASS sono congelati. L'assemblaggio è un merge dei **blocchi**, non dei CAP: **non tocca alcun CAP**. Le citazioni `[DOC-INTERNO CAP:riga]` ereditate dai blocchi sono richiami in sola lettura, già verificate token-per-token nei rispettivi cicli-blocco (floor citazioni 100% in ogni review-blocco) e nell'AUDITFIX-01 (`392a3f5`).
- **Cardine EDGE-PENDING** (eredità B7/B8, vincolante): **nessuna asserzione d'esito d'edge** (DSR/PBO/OOS/`E[R_net]`/GO-NO-GO). L'assemblato riporta criteri/soglie come **dichiarati/provvisori**, mai come esiti. I verbi vietati di B7 §1.4 ("il bundle supera/passa", "DSR è significativo/positivo", "l'edge esiste/è confermato", "GO") restano vietati nell'assemblato. L'esito d'edge è esclusiva del ruolo `validator`/FASE-D.
- **PENDING-empirico**: ogni grandezza marcata PENDING nei blocchi resta marcata PENDING (latenza Telegram effettiva, codici mese Mar/Dic, calendario IDEM finestra, θ_reconcile, 10 param tuning, run validator, ticker 1030, riavvio Darwin mezzanotte, PRICE f5/f7, ecc.). Marcare, mai asserire verificate (RM-1).
- **Subsunzione dei 6 difetti SOLO-v2 (NON re-introdurli)** — vedi §8.

### 6.2 Censimento M-promemoria aperti (CARRYOVER) — assegnazione all'assemblato

| M / promemoria | Stato | Trattamento nell'assemblato |
|---|---|---|
| **M-2** (latenza Telegram `L_max=30s`) | OPEN | **Incardinato** come NFR di latenza (Sez.6, da B4-NFR-03/04) + dipendenza aperta (Sez.10, da B8-R-03) + premessa gate (Sez.8, da B7-NFR-03). **NON chiuso**: resta OPEN/PENDING-empirico. Riportato `[B-1 PROVVISORIO]` / dichiarato provvisorio, mai verificato. |
| **M-GOV-1** (orario sessione 08:00-22:00 CET) | APERTO | **Incardinato** come regola operativa (Sez.7, da B5-R-11) + dipendenza aperta upgrade empirico (Sez.10, da B8 nota M-GOV-1). **NON chiuso**: verifica empirica resta OPEN (probe V-1/V-2). Riportato `[B-2 PROVVISORIO]` / dichiarato provvisorio. |
| **M-1 / M-9 / M-10** (schemi CANDLE/PRICE/BOOK_5) | nota tecnica-fonte | Già consolidati in B6 come requisiti di schema-dato con diff-decoder + permutazioni escluse (RM-1/RM-2/RACC-METODO-2). Nell'assemblato entrano **via B6→Sez.9 verbatim**, citati `[CODICE-ESISTENTE]`/`[PROVA-EMPIRICA]`, **mai ri-asseriti di prima istanza**. |
| **RACC-METODO-2** (diff vs decoder canonico) | regola permanente | Già onorata in B6 (i blocchi di diff-decoder sono nel B6-fonte). L'assemblato li **preserva verbatim**; non si introduce nuovo diff. |
| **M-4..M-16** (CAP-04/05/06/07) | CLOSED | nessun blocco; eventuale fonte storica, non incardinati. |
| **M-GOV-2** (slot SPEC-FUNZ-01) | CHIUSO | non pertinente al merge. |
| **Debito v2 (6 difetti SOLO-v2)** | da chiudere all'assemblaggio | **Subsunto** dall'assemblaggio (§8): la submacchina Cap.11 arriva corretta da B3; le 4 miscitation v2 spariscono perché la v2 è rimpiazzata. Done-when §10 verifica la non-reintroduzione. |

**Nessun M aperto resta non assegnato.** L'assemblaggio **non chiude** M-2 né M-GOV-1 (restano OPEN/APERTO): li **incardina** nello stesso stato in cui vivono nei blocchi.

---

## 7. Vincoli cardine di assemblaggio (LOSS-LESS) — acceptance specifici

### AC-ASM-1 — Fedeltà LOSS-LESS (cardine)
Ogni requisito di ogni blocco entra nell'assemblato: **0 requisiti persi, 0 inventati**. Il Developer produce la tabella di mapping (§5) che dimostra la copertura 1-a-1 dei 374 requisiti-blocco. Il Reviewer verifica il conteggio per blocco e la copertura della tabella di mapping.

### AC-ASM-2 — Citazioni `[DOC-INTERNO CAP:riga]` preservate e risolvibili
Ogni citazione di ogni requisito-blocco è **preservata verbatim** nell'assemblato e resta risolvibile (la riga-CAP citata esiste nel CAP frozen). Floor citazioni **100%** in review (come nei cicli-blocco). Nessuna citazione persa, alterata o de-numerizzata nel merge.

### AC-ASM-3 — Premesse condivise deduplicate (senza perdere tracciabilità)
Più blocchi citano la stessa premessa (es. "state machine & 6 stati terminali" è materia B3 e premessa in B4/B5/B6; "moltiplicatore 5€/pt" è materia B1 e premessa B5; "contratto messaggio Telegram" è materia B4 e premessa B5; "replay bit-exact CAP_02 Cap.10" è premessa in B5/B6/B7). Nell'assemblato la premessa-fatto è consolidata **una sola volta** (nella Sezione che la *possiede* come materia), e gli altri punti la **citano come riferimento interno** (AC-ASM-4), senza perdere la tracciabilità al CAP. La dedup va **dichiarata** nella tabella di mapping (§5). Una premessa-citazione che NON sia lo stesso requisito atomico NON va collassata: solo i fatti letteralmente identici si deduplicano.

### AC-ASM-4 — Cross-reference inter-blocco risolti in riferimenti interni
Ogni cross-reference inter-blocco presente nei blocchi (es. "vedi §7 di B5", "premessa B3 Cap.7", "materia di B4", "→ B6", le note di rinvio §-finali di ogni blocco) è **risolto in un riferimento interno** allo schema-ID/sezione dell'assemblato (es. "vedi Sez.4", "vedi `R-4.x`"). Nessun riferimento penzolante a un "blocco B?" che nel documento unico non esiste più come documento separato. Le note di rinvio dei blocchi vanno **fuse** in note di rinvio coerenti dell'assemblato (per Sezione o in una nota di rinvio unica), senza perdere le destinazioni out-of-scope.

### AC-ASM-5 — Matrice di tracciabilità UNICA
Una sola matrice requisito→capitolo per tutto il documento (non 8 matrici giustapposte). Una riga per ogni requisito-assemblato, con citazione puntuale e capitolo/Parte. Riconciliata 1-a-1 con i requisiti definiti nelle Sezioni 1-10 (0 mancanti, 0 orfani). + tabella di mapping ID-assemblato↔ID-blocco (§5).

### AC-ASM-6 — Valore operativo preservato per ogni requisito
Ogni requisito-assemblato conserva il proprio **valore operativo/di prodotto** (verbatim dal blocco o in sintesi fedele non riduttiva). Un requisito senza valore operativo dichiarato è un difetto.

### AC-ASM-7 — Atomicità preservata (N1)
Mappatura 1-a-1 requisito-blocco ↔ requisito-assemblato (salvo dedup premesse §AC-ASM-3, dichiarata). Nessuna fusione di concern distinti, nessuno spezzamento inventivo.

### AC-ASM-8 — No-reintroduzione dei 6 difetti SOLO-v2 (vedi §8)
### AC-ASM-9 — Edge-PENDING intatto (vedi §6.1)
### AC-ASM-10 — v2 archiviata + taggata (vedi §3)

### AC-G (globali, ereditati dal track, applicabili)
- **AC-G1 — Tracciabilità**: ogni requisito traccia a (a) valore operativo E (b) capitolo metodologia v2. *(verificabile sulla matrice unica + valore operativo per requisito.)*
- **AC-G2 — RM-1 no prima-istanza**: l'assemblato **non introduce** nuove dichiarazioni "verificato X" di prima istanza. Ogni asserzione fattuale è un **richiamo** a un CAP chiuso / codice / prova già chiusa, con provenienza etichettata. I blocchi `VERIFICA/PROVE/ALTERNATIVE` esistenti (B1-NFR-02; B6 schemi CANDLE/PRICE/BOOK_5) sono **preservati verbatim** dai blocchi, non riscritti né estesi.
- **AC-G3 — RM-3 fonti esterne**: ogni riferimento a wiki/docs esterni (MiFID II, wiki Directa, Telegram Bot API, Borsa Italiana, Portara/CQG, CME/Eurex) resta `[WIKI-HINT, da verificare]`, mai fonte unica di un'asserzione strutturale. Grafia canonica `[CODICE-ESISTENTE]` obbligatoria (grafia storica deprecata vietata).
- **AC-G4 — PENDING-empirico marcato**: ogni PENDING resta marcato, mai asserito verificato.

---

## 8. Subsunzione dei 6 difetti SOLO-v2 (NON re-introdurre — AC-ASM-8)

I 6 difetti che vivono **solo nella v2** (e che la v2-archiviata conserverà come storico, NON patchata) sono **subsunti** dall'assemblaggio perché l'assemblato è costruito **dai blocchi corretti**, non dalla v2:

1. **Submacchina di posizione Cap.11** — già presente **corretta in B3** (B3-R-40..48, B3-CN-07..12). L'assemblato la prende da B3→Sez.4, dove arriva corretta.
2. **Miscitation v2 CN-2.1** (dualità miniFIB/FIB-pieno) — sparisce: l'assemblato prende la dualità da **B5-R-10** (Sez.7), citazione corretta `[DOC-INTERNO CAP_09_parte_9.md:75,:69]`.
3. **Miscitation v2 R-3.7** (stop strutturale) — sparisce: l'assemblato prende lo stop da **B2** (Sez.3), citazioni corrette `CAP_02_parte_II.md:41,:51`.
4. **Miscitation v2 NFR-8.3** (IC bootstrap / expected net return) — sparisce: l'assemblato prende il gate da **B7** (Sez.8), citazione corretta `CAP_07_parte_VII.md:574`.
5. **Miscitation v2 R-10.2** (punti aperti / edge) — sparisce: l'assemblato prende il confine/dipendenze da **B8** (Sez.10), citazioni corrette Cap.55/64 + dipendenze aperte.

*(I 6 difetti SOLO-v2 di STATO/CARRYOVER = il gap submacchina Cap.11 + le 4 miscitation, conteggiati come gruppo di 6 secondo l'audit `wf_589a4b92`.)*

**Acceptance (done-when §10.7)**: il Developer dichiara e il Reviewer verifica che l'assemblato **NON re-introduca** nessuno dei 6 difetti — in particolare che le citazioni delle materie corrispondenti siano quelle **corrette dei blocchi**, non quelle errate della v2. Poiché il merge è dai blocchi (non dalla v2), la non-reintroduzione è strutturale; il check è una **conferma esplicita**, non una correzione.

---

## 9. Out-of-scope (con destinazione per ogni voce)

| Voce fuori scope | Destinazione |
|---|---|
| Modifica di qualunque CAP `docs/methodology_v2/CAP_*` | **CAP chiusi / freeze G-09** — l'assemblaggio è merge dei blocchi, non tocca i CAP |
| Modifica dei file-blocco B1..B8 | **restano storici** — sono la fonte del merge, non si riaprono; eventuali refusi NON si patchano qui |
| Modifica di `docs/methodology_v2/00_indice.md` | **N/A** (SPEC-FUNZ non è una Parte; §3.6) |
| Modifica di `tasks/METODO.md`, `SINTESI_GOVERNANCE_GA_PER_AC.md` (file pre-esistenti dirty nel working tree) | **fuori task** — non toccarli; sono modifiche di altri contesti, l'assemblaggio non li include nel suo commit |
| Patch dei 6 difetti SOLO-v2 nella v2-archiviata | **non si fa** — la v2 va all'archivio così com'è (patchare un doc destinato all'archivio = spreco); i difetti sono subsunti (§8) |
| Avvio FASE-D / implementazione codice / specifica di implementazione | **FASE-D** — l'assemblato chiude la spec, non avvia l'implementazione (eredità B8) |
| Verdetti d'edge / valori effettivi DSR/PBO/E[R_net]/OOS/GO-NO-GO | **FASE-D / ruolo `validator`** — PENDING-empirico, MAI asserito (cardine B7/B8) |
| Implementazione PHASE-2 cross-index (layer covarianza, S_xidx, feature cross-index) | **spec futura (SPEC-FUNZ-02 o equivalente)** — l'assemblato consolida solo il confine dichiarato (da B8→Sez.10) |
| Risoluzione delle dipendenze aperte (misura L_max, calibrazione θ_reconcile, congelamento 10 param, lookup codici mese, abilitazione FDAX, vendor cross-index) | **FASE-D / validator / monitoring post-go-live** — l'assemblato le dichiara aperte (da B8→Sez.10) |
| Apertura di materia-prodotto nuova non presente nei blocchi | **vietata** — l'assemblaggio è loss-less, non additivo: 0 requisiti inventati |
| Matematica interna del modello (geometria prezzo, EGARCH, pivot, NSGA-II, Cox) | **CAP chiusi / Parti III-IV-V** — già fuori scope nei blocchi; l'assemblato conserva la Sez. "capitoli non tracciati" con le motivazioni |

---

## 10. Done-when (soglie di verdetto verificabili dal Reviewer)

L'assemblaggio è completo quando **TUTTE** queste condizioni sono verificabili dal Reviewer (CLI, audit documentale no-DAPI):

1. **LOSS-LESS**: la tabella di mapping copre i **374** requisiti-blocco (B1=34, B2=42, B3=63, B4=61, B5=35, B6=72, B7=49, B8=18); ogni requisito-blocco mappa a esattamente un ID-assemblato (salvo dedup premesse dichiarate). 0 persi, 0 inventati. *(Il Reviewer ricontrolla i conteggi per blocco sui file-blocco e la copertura sulla tabella di mapping.)*
2. **Citazioni**: floor **100%** — ogni citazione `[DOC-INTERNO CAP:riga]` dell'assemblato è preservata verbatim dai blocchi e risolvibile sul CAP frozen.
3. **Dedup premesse**: ogni premessa condivisa è consolidata una sola volta, con riferimenti interni risolti; ogni dedup è dichiarata nella tabella di mapping con motivazione (AC-ASM-3).
4. **Cross-reference**: 0 riferimenti penzolanti a "blocco B?"; tutti risolti in riferimenti interni a sezione/ID dell'assemblato (AC-ASM-4).
5. **Matrice unica**: una sola matrice requisito→capitolo, riconciliata 1-a-1 con le Sezioni 1-10 (0 mancanti, 0 orfani) + tabella di mapping ID-assemblato↔ID-blocco completa.
6. **Struttura 10 Sezioni**: l'assemblato ha le 10 Sezioni di prodotto in ordine numerico 1→10, popolate secondo la mappatura §4 (B1→Sez.1+2, B2→Sez.3, B3→Sez.4, B4→Sez.5+6, B5→Sez.7, B7→Sez.8, B6→Sez.9, B8→Sez.10) + sezioni di servizio (nota di testa, capitoli non tracciati, blocchi/dipendenze aperte).
7. **No-reintroduzione 6 difetti SOLO-v2**: conferma esplicita (Developer) + verifica (Reviewer) che submacchina Cap.11 e le 4 miscitation (CN-2.1, R-3.7, NFR-8.3, R-10.2) arrivino dalle citazioni **corrette dei blocchi**, non da quelle errate della v2 (AC-ASM-8 / §8).
8. **Edge-PENDING intatto**: 0 asserzioni d'esito d'edge; criteri/soglie come dichiarati/provvisori; verbi vietati di B7 §1.4 assenti; confine ruolo `validator` esplicito (AC-ASM-9).
9. **PENDING-empirico**: tutti i PENDING dei blocchi restano marcati, mai asseriti (AC-G4).
10. **RM-1 no prima-istanza**: 0 nuove dichiarazioni "verificato X" di prima istanza; i blocchi `VERIFICA/PROVE/ALTERNATIVE` esistenti preservati verbatim (AC-G2).
11. **v2 archiviata + taggata**: `SPEC_FUNZ_01_v2_storico.md` presente su `origin/main` + tag git `spec-funz-01-v2-storico` apposto (AC-ASM-10 / §3).
12. **Rimpiazzo pulito**: `docs/spec_funzionale/SPEC_FUNZ_01.md` contiene l'assemblato; `00_indice.md` non toccato; CAP non toccati (freeze G-09: diff CAP vuoti); file-blocco B1..B8 non modificati; `METODO.md`/`SINTESI_GOVERNANCE_GA_PER_AC.md` non toccati dal commit del task.
13. **Valore operativo**: ogni requisito-assemblato ha valore operativo dichiarato (AC-ASM-6 / AC-G1).

---

## 11. Modalità di review e separazione ruoli

- **Modalità**: **Review formale piena adattata al non-CAP** — il Reviewer applica i suoi giri ostili agli **AC di questo task** (LOSS-LESS, dedup, cross-ref, matrice unica, no-reintroduzione, edge-PENDING, v2 archiviata+taggata), **non** agli AC dei CAP chiusi (congelati e già verificati). Doppio giro ostile (BASE_COMUNE §6).
- **Sede**: **CLI** (GOV-SURFACES-01, METODO §Superfici). Audit documentale no-DAPI col **divieto CLI** (niente probe di zelo). Lista **"Empirico-CLI da verificare" attesa VUOTA** (merge documentale: nessuna prova empirica nuova).
- **Classificazione finding** in 4 categorie (BUG REALE / MIGLIORA PERFORMANCE / NEUTRO / RISCHIO PEGGIORAMENTO) + tabella per il supervisore (BASE_COMUNE §4). Un requisito-blocco perso, una citazione rotta, un'asserzione d'edge introdotta o una reintroduzione di difetto v2 = **BUG REALE**.
- **Separazione ruoli**: il **Planner** (questa card) NON scrive l'assemblato e NON fa audit; NON committa la card (lo fa l'Orchestratore). Il **Developer** scrive `SPEC_FUNZ_01.md` (assemblato) + `REPORT_SPEC_FUNZ_01_ASSEMBLY.md`, archivia la v2 + appone il tag, esegue gli auto-check, scrive `READY_FOR_REVIEW`. Il **Reviewer** (CLI) audita contro gli AC di §7/§10.

---

## 12. Sezioni da produrre (per il Developer)

Il Developer produce, nell'**unica sessione batch** (F6: tutti i blocchi/ambiguità in un solo batch nel REPORT, non un giro per blocco; N1: requisiti atomici):

### A. Documento assemblato `docs/spec_funzionale/SPEC_FUNZ_01.md`
1. **Nota di testa** — provenienza e cautele di fonte (RM-1/RM-3), aggiornata allo stato post-blocchi (SHA CAP pinnabili dove i blocchi li pinnano), cardine edge-PENDING, blocchi aperti B-1/B-2 incardinati.
2. **Sez.1** (da B1, ambito/obiettivo/solo-emissione) + **Sez.2** (da B1, destinatario/operatore/sizing/canale).
3. **Sez.3** (da B2, payload).
4. **Sez.4** (da B3, state-machine & lifecycle, inclusa submacchina Cap.11 corretta).
5. **Sez.5** (da B4, emissione: 3 condizioni, filtro 80pt regola, regola AND, non-emissione, assenza filtri post-emissione) + **Sez.6** (da B4, consegna Telegram: contratto messaggio, latenza, anti-duplicato, notifiche, mobile-first, 3 notifiche standard).
6. **Sez.7** (da B5, runtime DAPI, sessione, gating, audit/compliance).
7. **Sez.8** (da B7, gate di go-live — criteri dichiarati, edge-PENDING).
8. **Sez.9** (da B6, schema-dato DAPI, replay, warm-up/continuità, riconciliazione, storicizzazione — schemi CANDLE/PRICE/BOOK_5 con diff-decoder e permutazioni escluse preservati verbatim).
9. **Sez.10** (da B8, confine PHASE-1/PHASE-2 + dipendenze aperte verso FASE-D).
10. **Sezione matrice di tracciabilità UNICA** (requisito→capitolo) + **tabella di mapping ID-assemblato↔ID-blocco** (§5).
11. **Sezione capitoli non tracciati** (motivazioni, ricostruita dalla v2 e verificata coerente coi blocchi).
12. **Sezione blocchi/dipendenze aperte** (B-1, B-2, + dipendenze aperte da B8).

### B. Report `reports/REPORT_SPEC_FUNZ_01_ASSEMBLY.md`
- **5 sezioni formato supervisore**: (1) Cosa è stato prodotto; (2) Ipotesi/decisioni di merge (split B1→Sez.1+2, B4→Sez.5+6; dedup premesse operate); (3) Decisioni rilevanti (schema-ID, dedup, cross-ref risolti); (4) Misura prima/dopo (conteggi per blocco → conteggio assemblato: 374 → N, con N=374 meno eventuali dedup dichiarate); (5) Domande aperte / criterio di rollback.
- **Tabella AC** (`OK / PARZIALE / MANCA` con evidenza `file:riga`) su AC-ASM-1..10 + AC-G1..4 + i 13 done-when.
- **Lista mapping** (la tabella di mapping completa, o riferimento alla sezione del documento che la contiene).
- **Auto-check no-reintroduzione** dei 6 difetti SOLO-v2 (esito esplicito).
- **Auto-check edge-PENDING** (0 asserzioni d'esito, lista PENDING preservata).
- **Applicazione RM-1 a sé stesso** (BASE_COMUNE §8).

### C. Archiviazione v2 + tag (§3)
- Copia/rename `SPEC_FUNZ_01.md` (v2 corrente) → `SPEC_FUNZ_01_v2_storico.md` **prima** del rimpiazzo.
- Tag git `spec-funz-01-v2-storico` sul commit (o sullo stato) che fissa la v2 storica.
- `tasks/DEV_STATUS.md` = `READY_FOR_REVIEW` a fine consegna.

---

*Card scritta dallo spec_planner del track Business-spec. Merge editoriale NON cieco (Planner e Developer leggono blocchi + mappa). Nessun CAP toccato (freeze G-09). Nessun file-blocco toccato. Card NON committata dal Planner (lo fa l'Orchestratore). Riconciliazione mappa-Orchestratore ↔ file di chunking: **nessuna discrepanza** (vedi §2 + report al supervisore).*

---

## 13. Finding di Review da risolvere (micro-pass post-PASS — decisione AC 2026-06-26)

Review `4eaa7df` = **PASS** (0 BUG REALE). AC ha approvato **un solo** micro-pass sul finding non bloccante OSS-1; OSS-2 (NEUTRO) **non instradato**.

- **OSS-1 (MIGLIORA PERFORMANCE) — `docs/spec_funzionale/SPEC_FUNZ_01.md:11` (nota di testa)**: la nota di testa riporta il conteggio totale come **"374"**, mentre il totale reale e verificato indipendentemente (Developer + Reviewer, B5=36 non 35) è **375**. Correggere il numero nella nota di testa da `374` a `375` (e ogni altra occorrenza residua di "374" come conteggio-totale nell'assemblato, se presente), allineandolo al 375 già coerente nel resto del documento (Sez.11, matrice, mapping). **Fix di sola accuratezza editoriale**: nessuna modifica ai requisiti, agli ID, alle citazioni, alla matrice o al mapping. Loss-less invariato (375). Edge-PENDING invariato.

Vincolo: micro-pass minimale, diff circoscritto alla/e riga/e del conteggio. Poi re-review di delta del Reviewer (CLI).

## 14. Secondo micro-pass post-PASS (decisione AC 2026-06-27) — OSS-2 + aritmetica B5

Dopo la chiusura ASSEMBLY (`ee1ea13`), AC ha approvato **due** ulteriori fix editoriali (entrambi accuratezza, nessun requisito cambia):

- **OSS-2 (era NEUTRO) — `docs/spec_funzionale/SPEC_FUNZ_01.md:1976` (tabella di mapping, riga `CN-9.25`)**: la colonna citazione elenca solo `[DOC-INTERNO CAP_09_parte_9.md:117]`, mentre la fonte B6 (`SPEC_FUNZ_01_B6.md:415`, matrice) e il **corpo stesso** di CN-9.25 nell'assemblato (`:1491`) citano **entrambi** `:117` **e** `:145`. È una **regressione del merge nella sola tabella di mapping**. Fix: ripristinare la riga 1976 a `[DOC-INTERNO CAP_09_parte_9.md:117,145]` (allineamento verbatim alla fonte B6). **Nessuna modifica a B6** (B6 è corretto); nessuna modifica al corpo (già corretto).

- **Aritmetica B5 — `docs/spec_funzionale/SPEC_FUNZ_01_B5.md:281`**: la riga di conteggio interno dice "**35 requisiti** (`B5-R`: 20, `B5-CN`: 9, `B5-NFR`: 7)"; 20+9+7 = **36**. Fix: `35`→`36` (la parentetica è già corretta). Se altre occorrenze di "35" come conteggio-totale-B5 esistono nel file B5 (es. intestazione/matrice), allinearle a 36. **Solo accuratezza aritmetica**: nessun requisito aggiunto/tolto (i 36 erano già tutti presenti ed elencati). Il marcatore PASS originale di B5 (`5ec899c`) resta storico; l'emendamento è coperto dalla re-review di questo micro-pass (precedente AUDITFIX-01).

Vincoli: due edit puntuali, diff minimale. NON toccare altro nell'assemblato né in B5; NON toccare i CAP (freeze G-09), gli altri blocchi, METODO/SINTESI. Loss-less assemblato invariato (375). Edge-PENDING invariato. Poi re-review di delta del Reviewer (CLI).
