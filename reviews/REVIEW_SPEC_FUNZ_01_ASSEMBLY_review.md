# REVIEW — SPEC-FUNZ-01-ASSEMBLY (audit di merge loss-less serie B1..B8)

> **Perimetro**: audit ostile del merge loss-less degli 8 blocchi B1..B8 in `docs/spec_funzionale/SPEC_FUNZ_01.md` (assemblato, commit `8d7ff60`). Cross-check di `reports/REPORT_SPEC_FUNZ_01_ASSEMBLY.md`. NON ri-audito il merito dei requisiti (chiusi nei cicli-blocco + AUDITFIX-01 `392a3f5`); audito **fedeltà del merge**: nulla perso, nulla inventato, nulla alterato, nessun difetto v2 reintrodotto, edge-PENDING intatto, v2 archiviata+taggata.
> **Sede**: **CLI** (GOV-SURFACES-01, METODO §Superfici) su `C:\Users\AN\Documents\Projects\ga-zone-engine`. Audit documentale **no-DAPI**, divieto CLI attivo (nessun probe di zelo). Lista "Empirico-CLI da verificare" attesa VUOTA.
> **Modalità**: CAP-review piena adattata al non-CAP, doppio giro ostile (BASE_COMUNE §6).
> **Letture obbligatorie completate**: (1) `tasks/METODO.md` RM-1..RM-4 + Freeze G-09 + §Superfici + RACC-METODO-2 + Precedenza; (2) `.claude/BASE_COMUNE.md` §3/§4/§6/§8; (3) `.claude/agents/spec_reviewer.md`; (4) `tasks/ACTIVE_TASK.md` (AC-ASM-1..10, AC-G1..4, §8 6 difetti v2, §10 13 done-when).

---

## VERDETTO (iterazione 1): **PASS**

0 problemi bloccanti, **0 BUG REALE in tabella**. Il merge è loss-less e fedele: 375 requisiti-blocco coperti 1-a-1 (0 persi, 0 inventati, 0 dedup), citazioni preservate e risolvibili (floor 100% rispettato sul campione esteso + verifica strutturale completa), 6 difetti SOLO-v2 NON reintrodotti, edge-PENDING intatto, v2 archiviata come copia esatta + taggata, freeze G-09 rispettato. Due osservazioni non-bloccanti (un refuso di conteggio nella nota di testa; un riferimento secondario di citazione ridotto), nessuna delle quali intacca la tracciabilità.

**Conteggio B5 verificato indipendentemente**: B5 = **36** (20 R + 9 CN + 7 NFR), NON 35. Confermo la rettifica del Developer: la card e il file-blocco B5 (`:281`) sommavano erroneamente 35; gli ID effettivi univoci sono 36, senza gap (`B5-R-01..20`, `B5-CN-01..09`, `B5-NFR-01..07`).
**Totale verificato indipendentemente**: 34 + 42 + 63 + 61 + **36** + 72 + 49 + 18 = **375**. Confermo 375, non 374.

---

## ESITO PUNTUALE DEGLI 8 PUNTI CARDINE

### 1. LOSS-LESS / conteggio (AC-ASM-1, done-when 1) — **OK**
Riconteggio indipendente (`grep -oE "B?-(R|CN|NFR)-[0-9]+" | sort -u | wc -l` su ogni file-blocco):
| Blocco | R | CN | NFR | TOT |
|---|---|---|---|---|
| B1 | 25 | 5 | 4 | 34 |
| B2 | 37 | 5 | 0 | 42 |
| B3 | 48 | 12 | 3 | 63 |
| B4 | 40 | 14 | 7 | 61 |
| **B5** | **20** | **9** | **7** | **36** |
| B6 | 43 | 25 | 4 | 72 |
| B7 | 38 | 7 | 4 | 49 |
| B8 | 13 | 5 | 0 | 18 |
| **TOTALE** | | | | **375** |

Copertura della tabella di mapping (Sez.11.2) verificata programmaticamente:
- 375 ID-blocco reali (univoci) nei file-blocco; 375 ID-blocco mappati nell'assemblato.
- **Persi** (reali NON in mappa): **0**. **Inventati** (in mappa NON reali): **0**.
- 375 ID-assemblato univoci, **0 collisioni**, 1-a-1 con i 375 ID-blocco.
- 0 dedup dichiarate (e 0 effettive): N(ID-assemblato) = N(ID-blocco) = 375. La nota di dedup (Sez.11.2 r.1620) è coerente con la verifica.

### 2. Citazioni (AC-ASM-2, done-when 2, floor 100%) — **OK**
- **Risolvibilità**: estratte tutte le 938 occorrenze numero-riga delle citazioni `[DOC-INTERNO CAP_*.md:riga]` dell'assemblato → **0 fuori range** (ogni riga ≤ totale righe del CAP), **0 CAP citati inesistenti**.
- **Identità col blocco-fonte (verbatim)**: confronto programmatico citazione-in-linea corpo-assemblato vs blocco-fonte per tutti i 375 requisiti. I 9 apparenti scostamenti iniziali si sono rivelati artefatti del matching (numeri di Parte/Cap. catturati come righe; citazioni di premessa di altre righe). Ispezione manuale di campione largo (R-3.7, R-3.23, R-3.25, R-4.15, R-6.24, R-7.10, R-8.34, CN-7.5, CN-9.25, NFR-1.1, R-9.4): tutte preservano la citazione **primaria** identica al blocco-fonte.
- **Verifica materia (apertura Read dei CAP frozen)**: R-3.23→CAP_02:41 (`stop_loss`), R-3.25→CAP_02:51 (`stop_type`), R-8.26→CAP_07:574 (AC-GO-3 E[R_net] IC bootstrap), R-7.10→CAP_09:75/:69 (dualità FIB pieno/miniFIB), CN-7.5→CAP_09:292/:302/:290 (1680min), R-9.4→CODICE export_directa…:477-481 (close/low/high/open), R-1.13/NFR-1.1→CAP_01:27 (banda 41100/41140), CN-2.1→CAP_01:23 (operatore retail MiFID II). **Tutte risolvono alla materia asserita.**

### 3. No-reintroduzione 6 difetti SOLO-v2 (AC-ASM-8, done-when 7) — **OK**
Verificato che le materie ex-difetto arrivano dalle citazioni **corrette dei blocchi**, non dalle errate v2:
- Submacchina Cap.11 → da B3→Sez.4 (R-4.40..48, CN-4.7..12), citazioni CAP_02:349..411 (presenti e risolvibili).
- CN-2.1 dualità miniFIB → da B5→Sez.7/R-7.10, CAP_09:75/:69 (corretta).
- R-3.7 v2 stop strutturale → nell'assemblato lo stop è R-3.23/R-3.25 (CAP_02:41/:51, corrette). Nota: lo schema-ID è cambiato dalla v2 (in v2 R-3.7 era `stop_loss`; nell'assemblato R-3.7 è `direction`); la materia stop ha la citazione corretta. Nessuna riflusso v2.
- NFR-8.3 v2 IC bootstrap → da B7→Sez.8/R-8.26, CAP_07:574 (AC-GO-3, corretta).
- R-10.2 v2 punti aperti/edge → da B8→Sez.10, CAP_08:143 (confine PHASE-2, corretta).
Confronto con `_v2_storico.md`: l'errore v2 non è rifluito; il merge è strutturalmente dai blocchi.

### 4. Edge-PENDING intatto (AC-ASM-9, done-when 8) — **OK**
- Verbi vietati di B7 §1.4 ("il bundle supera/passa il gate", "DSR è positivo/significativo", "l'edge esiste/è confermato", "GO" come esito): **0 come asserzioni**. Le 2 occorrenze sono **enunciazioni del divieto** (nota di testa r.16; nota di confine Sez.8 r.1029). Nessuna asserzione d'esito d'edge (DSR/PBO/OOS/E[R_net]/GO-NO-GO).
- Confine ruolo `validator` esplicito (r.1029 + CN-8.6 + R-10.6 + Sez.13.3).
- Soglie riportate come "criterio dichiarato"/"valore di lavoro provvisorio".

### 5. Dedup premesse + cross-ref (AC-ASM-3/4, done-when 3/4) — **OK**
- 0 dedup (premesse condivise risolte come riferimenti interni, non fusioni); coerente con la copertura 375.
- **0 cross-ref operativi penzolanti**: `grep` di "vedi B?", "§ di B?", "B? §/Cap" → 0. Le occorrenze `\bB[1-8]\b` nel corpo sono note di provenienza nei titoli di Sezione e nelle tabelle di rinvio fuse ("Sez.9 (da B6)", "Sez.7 (da B5)") = riferimenti storici legittimi, non cross-ref operativi.

### 6. Struttura + matrice unica (done-when 5/6) — **OK**
- 10 Sezioni in ordine numerico 1→10 (verificato header `##`): Sez.1/2←B1, Sez.3←B2, Sez.4←B3, Sez.5/6←B4, Sez.7←B5, **Sez.8←B7**, **Sez.9←B6** (incrociate come da mappa §4), Sez.10←B8.
- Matrice unica (Sez.11.1 sintesi + matrice in-linea per requisito) riconciliata 1-a-1 col corpo: 375 ID nel corpo = 375 in mappa, **0 orfani di mappa, 0 orfani di corpo**.
- Sezioni di servizio presenti: nota di testa, Sez.12 capitoli non tracciati (coerente coi blocchi, con correzione esplicita delle 3 righe v2 — Cap.29/34/35), Sez.13 blocchi/dipendenze aperte.

### 7. v2 archiviata + taggata (AC-ASM-10, done-when 11/12) — **OK**
- `SPEC_FUNZ_01_v2_storico.md` (654 righe) == v2 pre-merge (`git show 8d7ff60^:…SPEC_FUNZ_01.md`): **diff vuoto, copia esatta**.
- Tag `spec-funz-01-v2-storico` esiste e punta a `8d7ff60` (commit assembly). 
- **Freeze G-09**: `git diff 8d7ff60^ 8d7ff60 --` → CAP toccati = **0**, blocchi B1..B8 toccati = **0**, METODO/SINTESI toccati = **0**. `00_indice.md` non toccato (N/A). Commit copre solo i 4 file attesi (assemblato, v2_storico, REPORT, DEV_STATUS), su `origin/main`.

### 8. RM-1 no prima-istanza (AC-G2, done-when 10) — **OK**
- Nessuna nuova dichiarazione "verificato X" di prima istanza: ogni asserzione è un richiamo etichettato.
- 4 blocchi `VERIFICA/PROVE/ALTERNATIVE` = 1 (B1-NFR-02→NFR-1.1) + 3 (B6 CANDLE/PRICE/BOOK_5→Sez.9), coincide coi conteggi-fonte (B1=1, B6=3). Diff verbatim verificato su CANDLE e BOOK_5: **identici** ai blocchi-fonte. Grafia deprecata `[CODICE-EXISTENTE]` = 0.
- Marcatura F6 `[B-N PROVVISORIO]` inline su tutti e soli i 5 requisiti dipendenti dichiarati in Sez.13: NFR-6.3, NFR-6.4, NFR-8.3, R-10.3 (B-1), R-7.11 (B-2). Coerenza Sez.13↔corpo perfetta.

---

## Problemi bloccanti
Nessuno.

## Problemi non-bloccanti
Nessuno con impatto sulla tracciabilità o sul merito.

## Osservazioni minori (non-bloccanti)

**OSS-1 — Refuso di conteggio nella nota di testa (r.11): "374" anziché "375".**
La nota di testa (`SPEC_FUNZ_01.md:11`) recita *"I **374 requisiti-blocco** entrano nell'assemblato"*, mentre l'intero resto del documento è coerente su 375 (8 occorrenze: mappa 375 righe, matrice Sez.11.1 r.1612, conteggi per Sezione, nota correttiva Sez.11.1 r.1614 *"375, non 374"*) e il REPORT pure. È l'**unica** occorrenza-refuso del conteggio-requisiti rimasta non aggiornata dopo la correzione. NON intacca la tracciabilità (la mappa è loss-less su 375, verificato): nessun requisito perso/inventato/miscitato. È una incoerenza editoriale interna in un documento il cui valore è la fedeltà del numero, perciò vale la pena allinearla.

**OSS-2 — CN-9.25 (B6-CN-25): riferimento secondario `:145` non riportato in mappa.**
La matrice del file-blocco B6 (`SPEC_FUNZ_01_B6.md:415`) cita `[DOC-INTERNO CAP_09_parte_9.md:117,145]`; l'assemblato (corpo r.1490 e mappa r.1976) cita `CAP_09:117`. La riga 117 è la materia centrale (schema CSV header BOM UTF-8) e risolve correttamente; la 145 è un riferimento secondario (ruolo dello script `export_…`, premessa di contesto). La citazione **primaria** è preservata e risolve; la materia è tracciata. Riduzione di un riferimento di contesto, non della citazione load-bearing — non perdita di tracciabilità.

> Nota su REPORT r.85: il campione "CN-7.5→:290" citato è una delle tre righe (`:292,:302,:290`) del requisito; non è un errore del documento (il corpo r.956 e il blocco-fonte r.263 le riportano tutte e tre correttamente), solo una citazione abbreviata nel report.

---

## Tabella "Classificazione per il supervisore"

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|------------------------|
| 1 | Nota di testa dice "374 requisiti-blocco"; tutto il resto del doc + REPORT dicono 375 (incoerenza editoriale interna; tracciabilità intatta, loss-less su 375 verificato) | `docs/spec_funzionale/SPEC_FUNZ_01.md:11` | MIGLIORA PERFORMANCE | No (default; decide AC — coerenza documentale del documento autoritativo) |
| 2 | CN-9.25 mappa cita `CAP_09:117`, matrice-blocco B6 citava `:117,145`; `:145` è riferimento secondario, primaria preservata e risolvibile | `docs/spec_funzionale/SPEC_FUNZ_01.md:1976` (vs `SPEC_FUNZ_01_B6.md:415`) | NEUTRO | No |

Nessun BUG REALE. Verdetto coerente col mapping BASE_COMUNE §4 (0 BUG REALE ⇒ PASS ammesso; osservazioni minori ammesse in PASS).

---

## Onestà del REPORT (cross-check)
La tabella AC del REPORT (AC-ASM-1..10 + AC-G1..4 + 13 done-when tutti OK) è veritiera: ogni OK campionato ha evidenza reale nel documento. La discrepanza B5 (35→36) è dichiarata trasparentemente (§4 r.55-61, §5 r.70) e risolta in favore di RM-1 (verità di documento). L'"Applicazione RM-1 a sé stesso" (r.143-153) dichiara correttamente la verifica parziale sulle citazioni (campione, non intero set, perché richiamo non prima-istanza). Criterio di rollback presente. Nessuna autodichiarazione falsa rilevata.

---

## Lista "Empirico-CLI da verificare"
**VUOTA** (attesa). Il merge è documentale; nessuna asserzione empirica di prima istanza introdotta (gli schemi CANDLE/PRICE/BOOK_5 sono richiami `[PROVA-EMPIRICA]`/`[CODICE-ESISTENTE]` preservati verbatim dai blocchi già chiusi). Divieto CLI rispettato: nessun probe DAPI eseguito.

---

## Applicazione RM-1 a me stesso

- **"B5 = 36, totale 375"** → VERIFICATO. PROVE: `grep -oE "B5-(R|CN|NFR)-[0-9]+" SPEC_FUNZ_01_B5.md | sort -u | wc -l` per famiglia (R=20, CN=9, NFR=7), nessun gap negli ID; somma su tutti i blocchi = 375. ALTERNATIVE ESCLUSE: "35/374" della card/`B5:281`, falsificata dall'enumerazione reale (20+9+7=36). ALTERNATIVE NON ESCLUSE: nessuna.
- **"0 persi, 0 inventati, 1-a-1"** → VERIFICATO. PROVE: `comm -23`/`comm -13` tra set ID-reali e set ID-mappati = entrambi vuoti; 375 ID-assemblato univoci senza collisioni; riconciliazione corpo↔mappa con 0 orfani in entrambe le direzioni. ALTERNATIVE NON ESCLUSE: nessuna.
- **"938 citazioni numero-riga risolvibili"** → VERIFICATO. PROVE: confronto programmatico ogni numero-riga ≤ `wc -l` del CAP citato (0 fuori range). VERIFICA PARZIALE sulla *materia*: campione largo (~13 requisiti) aperto con Read sui CAP frozen, materia confermata; il resto è richiamo verbatim a blocchi già verificati 100% (cicli-blocco + AUDITFIX-01 `392a3f5`) sotto freeze G-09. ALTERNATIVE NON ESCLUSE: slittamento di una citazione se un CAP cambiasse — esclusa dal freeze G-09 (`git diff` CAP vuoto).
- **"citazioni verbatim dai blocchi"** → VERIFICATO sul campione + diff verbatim dei blocchi VERIFICA CANDLE/BOOK_5 (diff vuoto). I 9 apparenti mismatch del primo passaggio automatico → ispezionati manualmente, tutti artefatti del regex (numeri Parte/Cap o citazioni-premessa di righe vicine), 0 mismatch reali sulla citazione primaria.
- **"6 difetti v2 non reintrodotti"** → VERIFICATO. PROVE: Read delle 4 righe-CAP ex-miscitation (CAP_09:75, CAP_02:41/51, CAP_07:574, CAP_08:143) + confronto con `_v2_storico.md`. ALTERNATIVE ESCLUSE: riflusso v2 — escluso (merge strutturalmente dai blocchi; schema-ID dell'assemblato diverso dalla v2). 
- **"verbi vietati 0 come asserzioni"** → VERIFICATO. PROVE: `grep -niE` dei pattern → 2 match, entrambi ispezionati = enunciazioni del divieto.
- **"freeze G-09 + tag + v2 copia esatta"** → VERIFICATO. PROVE: `git diff --name-only 8d7ff60^ 8d7ff60` su CAP/blocchi/METODO = 0 file; `git rev-list -n1 spec-funz-01-v2-storico` = `8d7ff60`; `diff` v2_storico vs `8d7ff60^:…SPEC_FUNZ_01.md` = vuoto. ALTERNATIVE NON ESCLUSE: nessuna.

---

# RE-REVIEW DI DELTA (iterazione 2) — micro-pass OSS-1

> **Trigger**: micro-pass approvato (solo OSS-1, classificato MIGLIORA PERFORMANCE nella review PASS `4eaa7df`). Fix applicato dal Developer, commit `217f522`. OSS-2 (NEUTRO) NON instradato.
> **Natura**: re-review **di DELTA** — audito SOLO la differenza tra l'assemblato già PASS (`8d7ff60`) e lo stato post-fix (`217f522`); non ri-audito da capo il merge (già PASS in iterazione 1). Sede CLI, no-DAPI, divieto CLI.
> **Disclosure di processo (per trasparenza)**: l'edit di contenuto è dello spec_developer; il commit `217f522` è stato finalizzato dall'Orchestratore dopo uno stallo watchdog del subagente — passo meccanico (commit + DEV_STATUS), non scrittura di contenuto. **Confermato sul diff**: il commit message di `217f522` lo documenta esplicitamente e il diff effettivo è coerente (1 sola riga di contenuto + DEV_STATUS, nessuna scrittura sostanziale fuori dal fix approvato).

## VERDETTO DELTA: **PASS**

Il fix è esattamente circoscritto a OSS-1, 0 regressioni, 0 effetti collaterali. La review precedente (PASS `4eaa7df`) resta valida; questo delta la conferma e chiude l'unica osservazione MIGLIORA PERFORMANCE approvata.

## Esito dei 4 punti

### 1. Diff circoscritto — **OK**
`git diff 8d7ff60 217f522 -- docs/spec_funzionale/SPEC_FUNZ_01.md` mostra **una sola riga** modificata (nota di testa, r.11):
- `374`→`375`, con aggiunta della clausola esplicativa *"il conteggio 375 — non 374 — è dovuto a B5 che ha 36 requisiti effettivi, non 35, vedi nota §11.1"*.
- Nessun requisito, ID, citazione, matrice o tabella di mapping toccati. Il commit `217f522` tocca solo 2 file: l'assemblato (1 riga, `2 +-`) e `tasks/DEV_STATUS.md`. REPORT, v2_storico, CAP, blocchi B1..B8, METODO/SINTESI: **0** modifiche.

### 2. 0 regressioni — **OK**
- Loss-less ancora **375/375** su `217f522`: 375 ID-blocco mappati univoci, 375 ID-assemblato univoci (riconteggio su `git show 217f522:…`).
- **Sez.11 (matrice + tabella di mapping) IDENTICA**: `diff` della sezione tra `8d7ff60` e `217f522` = **vuoto**. Citazioni intatte, mapping intatto.
- Edge-PENDING intatto: la riga modificata non tocca verbi/asserzioni d'edge (è la frase sul conteggio nella nota di testa).

### 3. Coerenza conteggio — **OK**
- Dopo il fix la nota di testa (r.11) recita `375 requisiti-blocco`, allineata al 375 del resto del documento (Sez.11.1 r.1612, nota correttiva r.1614, conteggi per Sezione, mapping).
- Occorrenze residue di "374" nell'assemblato — tutte **legittime e correttamente conservate**:
  - r.11: solo dentro la nuova clausola esplicativa "375 — non 374 — … B5=36";
  - r.590 / r.602: `:374` = numeri di riga CAP citati (non conteggi);
  - r.1614: nota esplicativa "375 vs 374" (deve restare).
- REPORT non toccato (`git diff` REPORT vuoto): i suoi "374" restano come riferimento storico alla card — corretto, non un errore.

### 4. OSS-2 non instradato — **OK**
CN-9.25 (`SPEC_FUNZ_01.md:1976`) **invariato**: `| CN-9.25 | B6-CN-25 | [DOC-INTERNO CAP_09_parte_9.md:117] |` identico tra `8d7ff60` e `217f522`. Il NEUTRO non approvato non è stato toccato per errore.

## Classificazione per il supervisore (delta)
Nessun nuovo finding. 0 BUG REALE, 0 non-bloccanti, 0 osservazioni. OSS-1 della iterazione 1 è **risolto**; OSS-2 resta aperto-non-instradato (decisione AC, invariata).

## Lista "Empirico-CLI da verificare"
**VUOTA** (delta editoriale, nessuna materia empirica).

## Applicazione RM-1 a me stesso (delta)
- **"diff = sola riga nota di testa 374→375"** → VERIFICATO. PROVE: `git diff 8d7ff60 217f522 -- …SPEC_FUNZ_01.md` = 1 hunk, 1 riga `-`/`+`; `git show --stat 217f522` = 2 file (assemblato 1 riga + DEV_STATUS). ALTERNATIVE ESCLUSE: modifiche nascoste a requisiti/mapping — escluse dal `diff` Sez.11 vuoto. ALTERNATIVE NON ESCLUSE: nessuna.
- **"loss-less 375/375 invariato"** → VERIFICATO. PROVE: riconteggio ID su `217f522` = 375/375; `diff` Sez.11 = vuoto.
- **"OSS-2 intatto"** → VERIFICATO. PROVE: `grep` CN-9.25 su entrambi i commit = riga identica.
- **"commit meccanico Orchestratore, non contenuto"** → VERIFICATO sul diff. PROVE: il diff di contenuto è la sola riga del fix dello spec_developer; il commit message `217f522` documenta la finalizzazione meccanica post-watchdog. ALTERNATIVE NON ESCLUSE: nessuna (nessuna scrittura sostanziale dell'Orchestratore nel diff).

---

# RE-REVIEW DI DELTA (iterazione 3) — micro-pass 2 (OSS-2 + aritmetica B5)

> **Trigger**: secondo micro-pass post-PASS. Due fix instradati: OSS-2 (CN-9.25 mapping `:117`→`:117,145` — che io avevo classificato NEUTRO in iterazione 1) + correzione aritmetica del file-blocco B5 (`:281` "35"→"36", coerente col conteggio B5=36 che io stesso avevo verificato indipendentemente). Commit `74d75c8` (instradamento `2bf0a8c`).
> **Natura**: re-review **di DELTA** sullo stato chiuso precedente (`ee1ea13` re-review / `217f522` assemblato); audito SOLO la differenza `217f522`→`74d75c8`. Sede CLI, no-DAPI, divieto CLI.
> **Nota di processo osservata (trasparenza)**: la catena git mostra che dopo la mia re-review PASS `ee1ea13` era stato scritto un marcatore di chiusura `4dff43e` ("CHIUSO PASS ee1ea13"), poi lo slot è stato riaperto per questo secondo micro-pass instradato (decisione AC riferita dal coordinatore — trattata come contesto da verificare sul repo, non come autorità). Questo non è un difetto del fix qui auditato; lo registro come fatto di processo. Il commit `74d75c8` è autore ANAC, non riscrive history (5ec899c intatto).

## VERDETTO DELTA: **PASS**

Entrambi i fix sono esattamente circoscritti, fedeli (ripristino di tracciabilità, non alterazione), 0 regressioni. OSS-2 (NEUTRO) e la discrepanza aritmetica B5 sono ora chiusi. La review precedente (PASS) resta valida.

## Esito dei 4 punti

### 1. Diff circoscritto — **OK**
`git show 74d75c8 --stat` = **3 file, 3 righe** (3 insertions, 3 deletions):
- `SPEC_FUNZ_01.md:1976` (Sez.11 tabella mapping, riga CN-9.25): `[DOC-INTERNO CAP_09_parte_9.md:117]` → `[DOC-INTERNO CAP_09_parte_9.md:117,145]` (unica riga dell'assemblato modificata, verificato con `git diff` filtrato).
- `SPEC_FUNZ_01_B5.md:281`: "Conteggio: **35 requisiti**" → "**36 requisiti**"; la parentetica `(B5-R: 20, B5-CN: 9, B5-NFR: 7)` **invariata**.
- `tasks/DEV_STATUS.md` (segnale di stato).
Nessun altro requisito, ID, citazione, matrice o tabella toccati.

### 2. OSS-2 corretto e fedele — **OK**
- (a) **`:145` risolve a riga reale coerente**: `CAP_09_parte_9.md` ha 445 righe; r.145 = *"Ruolo dello script `export_directa_history_parametric.py`… definisce… il header CSV con BOM UTF-8"* — coerente con la materia BOM UTF-8 / header CSV di CN-9.25 (assieme a r.117 = "Schema CSV BOM UTF-8").
- (b) **Allineamento (ripristino di fedeltà, non alterazione)**: la tabella di mapping ora coincide sia col **corpo CN-9.25** (`SPEC_FUNZ_01.md:1491`, che già citava `:117` **e** `:145` — verificato **identico** tra `217f522` e `74d75c8`, NON toccato), sia con la **matrice-fonte B6** (`SPEC_FUNZ_01_B6.md:415` = `:117,145`, NON toccata; B6 = 0 modifiche nel commit). Prima del fix la mappa ometteva `:145` rispetto a corpo e fonte; il fix la riallinea. Confermo: ripristino di fedeltà. Era esattamente OSS-2 della review iniziale.

### 3. B5 = 36 corretto — **OK**
- Riconteggio ID univoci B5 su `74d75c8`: R=20, CN=9, NFR=7 → **20+9+7 = 36**. Identico a `217f522` (pre-fix): il **set di ID B5 è invariato** (`diff` dei set = vuoto) — nessun requisito aggiunto/tolto, è **solo la somma dichiarata** corretta da 35 a 36.
- Il marcatore PASS originale di B5 `5ec899c` resta **storico e intatto** (il commit non riscrive history). L'emendamento del file-blocco post-PASS è coperto da questa re-review (analogo al precedente AUDITFIX-01). 

### 4. 0 regressioni — **OK**
- Loss-less assemblato ancora **375/375** (375 ID-blocco mappati univoci, 375 ID-assemblato univoci su `74d75c8`).
- **Freeze G-09**: 0 CAP toccati dal commit.
- Nessun altro file-blocco toccato oltre B5 (atteso); v2_storico e REPORT non toccati.
- Edge-PENDING intatto: la riga modificata è in Sez.11 (encoding CSV), nessuna materia/verbo d'edge; 0 asserzioni edge introdotte nel diff.

## Classificazione per il supervisore (delta)
Nessun nuovo finding. 0 BUG REALE, 0 non-bloccanti, 0 osservazioni. **Tutte le osservazioni della review iniziale sono ora chiuse**: OSS-1 risolto (iterazione 2), OSS-2 risolto (questa iterazione). La discrepanza aritmetica B5 del file-blocco è chiusa.

## Lista "Empirico-CLI da verificare"
**VUOTA** (delta editoriale/tracciabilità, nessuna materia empirica).

## Applicazione RM-1 a me stesso (delta)
- **"diff = 3 righe (CN-9.25 mapping + B5 35→36 + DEV_STATUS)"** → VERIFICATO. PROVE: `git show 74d75c8 --stat` = 3 file/3+3 righe; `git diff 217f522 74d75c8 -- SPEC_FUNZ_01.md` filtrato = sola riga CN-9.25. ALTERNATIVE ESCLUSE: modifiche nascoste — escluse (loss-less 375/375 invariato, corpo CN-9.25 identico). ALTERNATIVE NON ESCLUSE: nessuna.
- **"`:145` risolve e allinea, non altera"** → VERIFICATO. PROVE: `sed -n 145p CAP_09_parte_9.md` = riga BOM/script reale; corpo r.1491 e B6 r.415 invariati e già `:117,145`. ALTERNATIVE ESCLUSE: `:145` inventato/fuori range — escluso (445 righe, r.145 esiste e coerente).
- **"B5=36, set ID invariato"** → VERIFICATO. PROVE: `grep -oE 'B5-...' | sort -u | wc -l` = 36 pre e post; `diff` dei set = vuoto. ALTERNATIVE NON ESCLUSE: nessuna.
- **"0 regressioni, freeze G-09"** → VERIFICATO. PROVE: 375/375 su `74d75c8`; 0 CAP/v2_storico/REPORT/altri-blocchi toccati dal commit. ALTERNATIVE NON ESCLUSE: nessuna.
