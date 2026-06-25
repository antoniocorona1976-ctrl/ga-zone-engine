# REPORT — SPEC-FUNZ-01-ASSEMBLY (assemblaggio loss-less serie B1..B8)

> Track: Business-spec (SPEC-FUNZ). Tag commit: [SPEC-FUNZ-01-ASSEMBLY]. Sede: CLI. Modalita: MERGE editoriale NON cieco.
> Output: docs/spec_funzionale/SPEC_FUNZ_01.md (assemblato, rimpiazza la v2) + docs/spec_funzionale/SPEC_FUNZ_01_v2_storico.md (v2 archiviata).

## Conferma letture obbligatorie

Confermo di aver letto, in quest'ordine, prima di scrivere: (1) tasks/METODO.md (RM-1..RM-4 + Freeze G-09 + Superfici GOV-SURFACES-01 + RACC-METODO-2 + Precedenza documenti); (2) .claude/BASE_COMUNE.md; (3) .claude/agents/spec_developer.md; (4) tasks/ACTIVE_TASK.md (integralmente). Per il merge NON cieco: tutti e 8 i blocchi SPEC_FUNZ_01_B1.md..SPEC_FUNZ_01_B8.md, la mappa PROPOSTA_SUDDIVISIONE_SPEC_v2.md, e la v2 corrente SPEC_FUNZ_01.md.

---

## 1. Cosa e stato prodotto

- Documento assemblato docs/spec_funzionale/SPEC_FUNZ_01.md (2084 righe): merge loss-less degli 8 blocchi B1..B8 in un unico documento di specifica funzionale autoritativo (PHASE-1 FIB-only), che rimpiazza la v2. Struttura: nota di testa (provenienza, cardine edge-PENDING, blocchi aperti incardinati) + 10 Sezioni di requisiti in ordine numerico 1->10 + 3 sezioni di servizio (Sez.11 matrice unica + tabella di mapping, Sez.12 capitoli non tracciati, Sez.13 blocchi/dipendenze aperte).
- v2 archiviata docs/spec_funzionale/SPEC_FUNZ_01_v2_storico.md (copia esatta della v2 corrente, 654 righe), creata PRIMA del rimpiazzo (analoga a _v1_storico).
- Conteggio finale assemblato: 375 requisiti (vedi par.4 e discrepanze). Mappatura 1-a-1, 0 dedup, 0 persi, 0 inventati.

Mappatura blocchi->sezioni: B1->Sez.1+2, B2->Sez.3, B3->Sez.4, B4->Sez.5(emissione)+Sez.6(consegna), B5->Sez.7, B7->Sez.8, B6->Sez.9, B8->Sez.10 (Sez.8/9 incrociate per ordine-blocco, disposte in ordine numerico).

---

## 2. Ipotesi/decisioni di merge

- Split B1->Sez.1+2: ambito/obiettivo/strumento/solo-emissione/economiche-FIB -> Sez.1; destinatario/operatore/sizing/canale/infra -> Sez.2. Split tematico fedele alla struttura v2, senza perdere ne duplicare requisiti B1.
- Split B4->Sez.5+6 (per concern): emissione (3 condizioni, filtro 80pt come regola, regola AND, non-emissione, assenza filtri post-emissione, no fasi orario) = B4-R-01..16 + B4-CN-01..05 -> Sez.5; consegna (contratto messaggio, ordine campi, latenza, anti-duplicato, notifiche, mobile-first, 3 notifiche standard) = il resto di B4 -> Sez.6. Confine fine rispettato: B4-R-16 (no fasi orario) e B4-CN-01/05 (assenza filtri post-emissione) -> Sez.5.
- Schema-ID sezione-based R-x.y/NFR-x.y/CN-x.y (x=Sezione). Numerazione progressiva per famiglia dentro la sezione, allineata 1-a-1 all'ordine del blocco-fonte (tabella di mapping Sez.11.2).
- Dedup premesse (AC-ASM-3): 0 collassamenti. Nessuna coppia di requisiti-blocco e stata fusa: le premesse condivise (state machine, moltiplicatore 5eur/pt, contratto messaggio, replay bit-exact CAP_02 Cap.10) sono un solo requisito nel blocco che le possiede e riferimenti interni negli altri (cross-ref risolti). Quindi N ID-assemblato = N requisiti-blocco = 375, senza riduzione.

---

## 3. Decisioni rilevanti

- Tabella di mapping (Sez.11.2): 375 righe ID-assemblato | ID-blocco | citazione CAP. La 3a colonna e popolata con la citazione [DOC-INTERNO CAP_XX:riga] / [CODICE-ESISTENTE path:linea] / [PROVA-EMPIRICA data] estratta dal corpo di ogni requisito-assemblato, per non lasciare ambiguita al Reviewer (AC-ASM-2/par.5).
- Matrice unica (Sez.11.1): la matrice puntuale per-requisito vive in-linea in ogni requisito (campo Tracciabilita/Fonte); la Sez.11.1 ne e la sintesi per Sezione, riconciliata 1-a-1 (0 mancanti, 0 orfani). Una sola matrice, non 8 giustapposte.
- Cross-reference inter-blocco risolti (AC-ASM-4): tutti i riferimenti "vedi X di B?", "premessa B?", "-> B?", le note di rinvio finali dei blocchi riscritti in riferimenti interni a Sezione/ID (es. "vedi Sez.4 / R-4.15"). 0 riferimenti penzolanti a "blocco B?".
- Blocchi VERIFICA/PROVE/ALTERNATIVE preservati verbatim (AC-G2/RM-1): B1-NFR-02->NFR-1.1 (tick 5pt); B6 schemi CANDLE/PRICE/BOOK_5->R-9.4/R-9.16/R-9.18 con i tre blocchi RM-1 e i tre diff-decoder copiati verbatim.
- SHA CAP nella nota di testa: riportati SOLO gli SHA effettivamente pinnati nei blocchi (b76c32c, a1625df, b27c1e3, e8d5424, 015c47a, 28cfd2d, 41447d3). CAP-06 (Sez.6) non e pinnato nel blocco B4-EXT: non ne ho inventato uno (RM-1).

---

## 4. Misura prima/dopo (greenfield di consolidamento)

PRIMA: i 375 requisiti di prodotto vivevano dispersi in 8 documenti-blocco separati (B1..B8), schema-ID locale, 8 matrici giustapposte, cross-reference fra documenti separati. Un esterno non poteva leggere la specifica completa in un solo posto ne tracciare un requisito al suo capitolo senza navigare 8 file.

DOPO: 375 requisiti R/NFR/CN consolidati in un unico documento con schema-ID sezione-based uniforme, una sola matrice di tracciabilita, una tabella di mapping che dimostra la copertura loss-less 1-a-1, cross-reference risolti in riferimenti interni.

Conteggi ricontati per blocco (Read su ogni file-blocco, grep ID distinti):

| Blocco | Card dichiara | Ricontato sul file | Composizione |
|---|---|---|---|
| B1 | 34 | 34 | 25 R + 5 CN + 4 NFR |
| B2 | 42 | 42 | 37 R + 5 CN |
| B3 | 63 | 63 | 48 R + 12 CN + 3 NFR |
| B4 | 61 | 61 | 40 R + 14 CN + 7 NFR |
| B5 | 35 | 36 (!) | 20 R + 9 CN + 7 NFR |
| B6 | 72 | 72 | 43 R + 25 CN + 4 NFR |
| B7 | 49 | 49 | 38 R + 7 CN + 4 NFR |
| B8 | 18 | 18 | 13 R + 5 CN |
| TOTALE | 374 | 375 (!) | |

Discrepanza di conteggio rilevata (B5): il file SPEC_FUNZ_01_B5.md contiene 36 requisiti (B5-R-01..20 = 20 R, B5-CN-01..09 = 9 CN, B5-NFR-01..07 = 7 NFR; 20+9+7 = 36), ma la sua riga di conteggio interno (SPEC_FUNZ_01_B5.md:281) e la task card dichiarano 35 (sommando erroneamente 20+9+7 come 35). Tutti i 36 requisiti B5 sono effettivamente presenti, atomici e tracciati nel file; l'errore e puramente aritmetico nel totale dichiarato. Come da istruzione (RM-1, F6): ho mappato tutti i 36 requisiti B5 in Sez.7 (R-7.1..20, CN-7.1..9, NFR-7.1..7 = 36) e il totale assemblato reale e 375, non 374. Il documento (Sez.11.1) e questo report riportano 375 con la discrepanza dichiarata. Non ho modificato il file-blocco B5 (fonte storica, fuori scope par.9 card).

Conteggio per Sezione dell'assemblato: Sez.1=20, Sez.2=14, Sez.3=42, Sez.4=63, Sez.5=21, Sez.6=40, Sez.7=36, Sez.8=49, Sez.9=72, Sez.10=18 -> 375. Coincide con la somma per blocco (34+42+63+61+36+72+49+18=375).

---

## 5. Domande aperte / criterio di rollback

Domande aperte (batch, F6):
1. Discrepanza B5 (374 vs 375): la card e il file B5 dichiarano 35 dove i requisiti effettivi sono 36. Non e un blocco all'esecuzione (ho mappato tutti i 36), ma il Reviewer/Planner deve decidere se (a) accettare 375 come totale corretto (mia scelta, conforme a RM-1) e/o (b) aprire un micro-fix sul file-blocco B5 per correggere l'aritmetica del suo conteggio interno. Nessun blocco operativo: il merge e completo e loss-less su 375.

Nessun altro blocco. Tutti i requisiti mappati; nessun requisito porta marcatore [B-N PROVVISORIO] per contaminazione da blocco non risolto (i tag [B-1/B-2 PROVVISORIO] presenti sono ereditati dai blocchi per M-2/M-GOV-1, non nuovi blocchi di questo task).

Criterio di rollback: se il Reviewer trova un requisito-blocco perso, una citazione rotta, un'asserzione d'edge introdotta o una reintroduzione di un difetto v2, il rollback e: ripristinare la v2 da SPEC_FUNZ_01_v2_storico.md (git checkout del file) e correggere chirurgicamente l'assemblato sui finding approvati. I file-blocco B1..B8 (intatti) restano la fonte autoritativa.

---

## Tabella verifica Acceptance Criteria

### AC-ASM-1..10 + AC-G1..4

| AC-ID | OK/PARZIALE/MANCA | Evidenza (file:riga / criterio) |
|---|---|---|
| AC-ASM-1 LOSS-LESS (0 persi, 0 inventati) | OK | Tabella mapping Sez.11.2 = 375 righe, copre B1..B8 1-a-1; conteggio per Sezione = somma per blocco = 375. SPEC_FUNZ_01.md:1622+ |
| AC-ASM-2 Citazioni preservate e risolvibili (floor 100%) | OK | Citazioni verbatim dai blocchi (gia 100% nei cicli-blocco + AUDITFIX-01); campione risolto (R-3.1->:19, R-9.33->:123, R-8.26->:574 AC-GO-3, CN-7.5->:290). Grafia deprecata CODICE-EXISTENTE = 0 |
| AC-ASM-3 Dedup premesse dichiarate | OK | 0 dedup; nota Sez.11.2 dichiara le premesse condivise come riferimenti interni. SPEC_FUNZ_01.md:1620 |
| AC-ASM-4 Cross-ref -> riferimenti interni; 0 penzolanti | OK | Tutti i riferimenti "vedi B?"/note di rinvio riscritti a Sezione/ID; out-of-scope per Sezione con destinazioni interne |
| AC-ASM-5 Matrice unica riconciliata 1-a-1 + tabella mapping | OK | Sez.11.1 matrice sintesi (0 mancanti/0 orfani) + matrice in-linea per requisito; Sez.11.2 tabella 375 righe |
| AC-ASM-6 Valore operativo per ogni requisito | OK | Ogni requisito ha campo Valore operativo/Valore di sistema (verbatim o sintesi fedele) |
| AC-ASM-7 Atomicita N1 (1-a-1, no fusione/spezzamento) | OK | Mappatura 1-a-1 Sez.11.2; nessuna fusione di concern, nessuno spezzamento inventivo |
| AC-ASM-8 No-reintroduzione 6 difetti SOLO-v2 | OK | Auto-check sotto |
| AC-ASM-9 Edge-PENDING intatto | OK | Auto-check sotto |
| AC-ASM-10 v2 archiviata + taggata | OK | SPEC_FUNZ_01_v2_storico.md creato; tag spec-funz-01-v2-storico apposto+pushato |
| AC-G1 Tracciabilita (valore + capitolo) | OK | Ogni requisito: valore operativo + citazione CAP; matrice Sez.11.1 |
| AC-G2 RM-1 no prima-istanza | OK | 0 nuove "verificato X"; blocchi VERIFICA/PROVE/ALTERNATIVE (NFR-1.1, R-9.4/9.16/9.18) preservati verbatim |
| AC-G3 RM-3 fonti esterne etichettate | OK | wiki/MiFID/Telegram/Borsa/Portara/CME tutti [WIKI-HINT]; grafia canonica [CODICE-ESISTENTE]; 0 conclusioni wiki-only |
| AC-G4 PENDING-empirico marcato | OK | Sez.13.3 lista PENDING; tag [B-1/B-2 PROVVISORIO] su NFR-6.3/6.4, NFR-8.3, R-10.3, R-7.11 |

### 13 Done-when (par.10 card)

| # | Done-when | OK/PARZIALE/MANCA | Evidenza |
|---|---|---|---|
| 1 | LOSS-LESS, tabella mapping copre i requisiti-blocco | OK | Sez.11.2 = 375 righe 1-a-1 (374 card + 1 da discrepanza B5 dichiarata) |
| 2 | Citazioni floor 100% verbatim e risolvibili | OK | campione risolto; verbatim dai blocchi |
| 3 | Dedup premesse consolidate + riferimenti interni | OK | 0 dedup; riferimenti interni risolti (Sez.11.2 nota) |
| 4 | Cross-reference 0 penzolanti | OK | tutti risolti a Sezione/ID |
| 5 | Matrice unica riconciliata 1-a-1 + tabella mapping | OK | Sez.11.1 + Sez.11.2 |
| 6 | Struttura 10 Sezioni ordine 1->10 + servizio | OK | Sez.1..10 numeriche + nota testa + Sez.11/12/13 |
| 7 | No-reintroduzione 6 difetti SOLO-v2 | OK | auto-check sotto |
| 8 | Edge-PENDING intatto, verbi vietati assenti | OK | auto-check sotto (i 2 grep-match sono enunciazioni del divieto, non asserzioni) |
| 9 | PENDING-empirico marcato | OK | Sez.13.3 + tag provvisori |
| 10 | RM-1 no prima-istanza | OK | 0 nuove "verificato X"; blocchi RM-1 preservati |
| 11 | v2 archiviata + taggata | OK | _v2_storico.md + tag spec-funz-01-v2-storico |
| 12 | Rimpiazzo pulito; CAP/00_indice/blocchi/METODO/SINTESI non toccati | OK | git diff CAP vuoto; blocchi intatti; METODO/SINTESI esclusi dal commit; 00_indice N/A |
| 13 | Valore operativo per ogni requisito | OK | campo Valore in ogni requisito |

---

## Auto-check no-reintroduzione dei 6 difetti SOLO-v2 (AC-ASM-8 / par.8 card)

Conferma esplicita che l'assemblato e costruito dai blocchi corretti, non dalla v2, e NON re-introduce i 6 difetti SOLO-v2:

1. Submacchina di posizione Cap.11 — presa da B3->Sez.4 (R-4.40..48, CN-4.7..12), dove arriva corretta (citazioni CAP_02_parte_II.md:349..411). La v2 aveva il gap submacchina; l'assemblato lo ha completo e corretto. NON re-introdotto.
2. Miscitation v2 CN-2.1 (dualita miniFIB/FIB-pieno) — presa da B5->Sez.7 / R-7.10, citazione corretta [DOC-INTERNO CAP_09_parte_9.md:75, :69] (+ R-1.16 per il 5eur/pt da CAP_01). NON re-introdotta.
3. Miscitation v2 R-3.7 (stop strutturale) — lo stop e preso da B2->Sez.3 / R-3.23..27, citazioni corrette CAP_02_parte_II.md:41, :51. NON re-introdotta.
4. Miscitation v2 NFR-8.3 (IC bootstrap / expected net return) — il gate e preso da B7->Sez.8 / R-8.26, citazione corretta [DOC-INTERNO CAP_07_parte_VII.md:574] (AC-GO-3, riga :574 = "AC-GO-3 — Expected net return positivo con IC bootstrap"). NON re-introdotta.
5. Miscitation v2 R-10.2 (punti aperti / edge) — il confine/dipendenze e preso da B8->Sez.10 (R-10.1..13, citazioni Cap.42/55/64 + dipendenze aperte). NON re-introdotta.
6. (Il gruppo "6 difetti" = gap submacchina Cap.11 + le 4 miscitation, secondo l'audit wf_589a4b92.) Poiche il merge e dai blocchi (non dalla v2), la non-reintroduzione e strutturale; questo e un check di conferma, non una correzione. Esito: 0 difetti SOLO-v2 re-introdotti.

---

## Auto-check edge-PENDING (AC-ASM-9)

- 0 asserzioni d'esito d'edge: grep su verbi vietati ("il bundle supera/passa il gate", "DSR e positivo/significativo", "l'edge esiste/e confermato") -> 2 match, entrambi enunciazioni del divieto (nota di testa riga 16, nota di confine Sez.8 riga 1029), nessuna asserzione d'esito. Verificato manualmente.
- Criteri/soglie come dichiarati/provvisori: tutte le soglie di Sez.8 riportate come "criterio dichiarato" / "valore di lavoro provvisorio non congelato"; valori effettivi sempre marcati "PENDING-empirico (validator / FASE-D)".
- Confine ruolo validator esplicito: nota di confine Sez.8 (riga 1029) + CN-8.6 + R-10.6 + Sez.13.3.
- Lista PENDING preservata (Sez.13.3): DSR/PBO/E[R_net]/CVaR/MDD/r_emit/rho_sessions effettivi, esito 12 criteri, GO/NO-GO, L_avg, F, L_max Telegram, theta_reconcile, 10 parametri tuning, codici mese Mar/Dic, FDAX, vendor cross-index, PRICE f5/f7, ticker 1030, riavvio Darwin. Esito: edge-PENDING intatto.

---

## Applicazione RM-1 a me stesso

Ogni asserzione fattuale di questo report ha sostegno operativo (citazione + esito), non e asserita nuda:

- "375 requisiti, loss-less 1-a-1" -> verificato ricontando con grep -oE gli ID distinti su ogni file-blocco (B1=34..B8=18, somma 375) e sull'assemblato (somma per Sezione = 375); tabella mapping = 375 righe, 0 ID-assemblato duplicati, copertura ID-blocco completa. Alternativa esclusa: "374" della card, falsificata dall'aritmetica reale di B5 (20+9+7=36, non 35).
- "CAP intatti" -> verificato: git diff --name-only -- docs/methodology_v2/ = vuoto.
- "blocchi B1..B8 intatti" -> verificato: git diff --name-only -- docs/spec_funzionale/SPEC_FUNZ_01_B*.md = vuoto.
- "METODO/SINTESI non toccati dal mio commit" -> verificato: stageato esplicitamente solo i 4 file del task.
- "citazioni risolvibili" -> verifica parziale dichiarata: campione di 8 citazioni risolto alla riga-CAP corretta (non l'intero set di 375 — le citazioni sono verbatim dai blocchi gia verificati 100% nei cicli-blocco + AUDITFIX-01 392a3f5; e un richiamo, non una nuova verifica di prima istanza). Alternativa non esclusa: una citazione potrebbe slittare se un CAP cambiasse, esclusa dal freeze G-09 (diff CAP vuoto).
- "0 difetti SOLO-v2 re-introdotti" -> verificato strutturalmente: il merge e dai blocchi, non dalla v2; miscitation corrette campionate (R-7.10->:75, R-8.26->:574) risolvono alla riga corretta.
- "edge-PENDING intatto" -> verificato: grep verbi vietati = 2 match, entrambi ispezionati e confermati come enunciazioni del divieto.

Nessuna nuova dichiarazione "verificato X" di prima istanza su sistemi esterni e introdotta: tutte le asserzioni di schema-dato (Sez.9) sono richiami ai blocchi B6 (verbatim, inclusi i 3 blocchi RM-1 e i 3 diff-decoder).
