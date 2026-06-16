# PIANO DI CHUNK business-spec — 8 blocchi (FINALIZZATO)

> **FINALIZZATO: decisione AC = 8 blocchi (B1-B8). Soglia effettiva ~10-14 req/blocco. Questo documento è il piano di chunk operativo che governerà la sequenza di task business-spec.**

**Natura**: documento di **pianificazione operativa** (chunking), evoluto da analisi a piano definitivo. Prodotto dal ruolo `spec_planner` in modalità ANALISI E PROPOSTA — NO esecuzione. NON apre `ACTIVE_TASK.md`, NON scrive spec, NON invoca agenti, NON committa (il commit lo fa l'Orchestratore). I capitoli `docs/methodology_v2/CAP_*` sono **solo letti** (freeze G-09 rispettato).

**Letture obbligatorie fatte** (confermo): `tasks/METODO.md` (RM-1..RM-4 + RACC-METODO-2 + §Superfici GOV-SURFACES-01 + Freeze G-09), `.claude/BASE_COMUNE.md` (ciclo, sede CLI per la spec, classificazione finding, registry), `.claude/agents/spec_planner.md` (mio ruolo).

**Decisione di AC (autoritativa, presa con l'Orchestratore — NON ri-derivata, NON ridiscussa)**:
1. la business-spec **si spezza** in più blocchi (non un'unica spec sull'intero scope);
2. il numero di blocchi è **8** (B1-B8), ottenuto **partendo dal piano a 6 e applicando due soli split**: il contratto Parte II si divide in *payload* (B2) e *state-machine* (B3); il go-live si divide in *gate* (B7) e *confine PHASE-2* (B8). Le coppie coese restano unite — in particolare **emissione + consegna Telegram restano insieme** (B4).

**Fonti autoritative** (lette, non re-derivate):
- `docs/spec_funzionale/SPEC_FUNZ_01.md` §11 (matrice 75 req, righe 526-604), §12 (capitoli non tracciati, righe 608-636), §13 (blocchi aperti, righe 640-654). **Inventario autoritativo dei 75 requisiti**.
- `docs/spec_funzionale/PROPOSTA_SUDDIVISIONE_SPEC.md` (commit `fc72133`) — proposta storica a 3 blocchi.
- `tasks/STATO_CORRENTE.md` (marcatori di chiusura, M attivi), `tasks/CARRYOVER.md` (M aperti, RACC-METODO-2).

**Applicazione RM-1 a me stesso**: ogni claim "questo blocco regge una sessione" / "questa Parte è 0-req" / "questo blocco è il più carico" / "rischio X su blocco Y" è ancorato a una citazione puntuale (`§11`/`§12`/`PROPOSTA`/`STATO`/`CARRYOVER` con riga) + aritmetica esplicita, MAI asserito nudo. I conteggi di requisiti per blocco sono **ordini di grandezza (o.d.g.) derivati dalla matrice §11**; le sovrapposizioni sezionali (un requisito che traccia a due Parti) sono dichiarate. Dove il repo non disambigua, la voce è marcata **[DECISIONE AC]**. Nessuna dichiarazione "verificato X" di prima istanza: questo è planning interno, non introduce fatti su sistemi esterni.

---

## 1. Perché la proposta storica aveva 3 blocchi — diagnosi (come ci siamo arrivati)

La PROPOSTA storica (`PROPOSTA_SUDDIVISIONE_SPEC.md`) proponeva **3 blocchi**: S-A (contratto/consegna), S-B (runtime/dato/compliance), S-C (go-live/fasizzazione) `[PROPOSTA §3:68-98]`.

**Il difetto strutturale**: quei 3 blocchi sono un **raggruppamento per tipo di consumatore** — chi legge il segnale (S-A) / chi opera la pipeline-dato (S-B) / chi decide il go-live (S-C). Lo dichiara la PROPOSTA stessa: *"Asse di taglio scelto: densità + natura del consumatore (contratto / consegna / runtime-dato / gate-go-live / fasizzazione)"* `[PROPOSTA §3:66]`. È un asse **tematico**, scelto a priori; "3" è il numero di categorie-consumatore, **non** un numero derivato da una soglia di dimensionamento.

**La prova interna che 3 è sotto-dimensionato**: la PROPOSTA stessa ammette che il blocco **S-A è "borderline"** per una sessione e **candidato a split** in S-A1/S-A2:
- *"Fattibilità in una sessione: **borderline**. È il blocco più denso (~30+ requisiti, ~6 sezioni)... Possibile split in S-A1 (payload+state machine) e S-A2 (emissione+consegna)... **[DECISIONE AC]** sul taglio fine"* `[PROPOSTA §3 S-A:72]`.
- ribadito in §5: *"[DECISIONE AC-2] ... taglio fine del blocco S-A (monolitico ~30+ requisiti, *borderline* per una sessione, vs split...)"* `[PROPOSTA §5:143]`.

La PROPOSTA aveva già il criterio giusto in mano (la **lezione 4**, §2), ma **non lo applicò al conteggio**: si fermò a 3 categorie tematiche e poi notò *a posteriori* che una di esse non ci stava. La correzione: **partire dal criterio e lasciare che produca il numero**.

---

## 2. Il criterio applicato (meccanico) — come si è arrivati alla grana

### 2.1 La soglia di dimensionamento

Dalla **lezione 4** della PROPOSTA `[PROPOSTA §4:120]`: il vincolo che tiene l'accuratezza di una review business-spec **non è il numero di pagine, ma il numero di citazioni `[DOC-INTERNO CAP_XX:riga]` che il Reviewer deve verificare al 100%**. SPEC-FUNZ-01 con 75 req × ~1-2 citazioni = ~100-150 verifiche puntuali in una sola review: il motivo reale del "troppo ampio".

**Soglia operativa**: ~req per blocco, assumendo **≥1 giro di rework pieno** (lezione 1: il primo giro di review quasi mai passa `[PROPOSTA §4:114]`). Più stretta è la soglia, più blocchi, più margine al rework. La soglia è **[DECISIONE AC]**: il repo non fissa un numero, è una scelta di rischio. **Decisione AC = grana fine, ~10-14 req/blocco effettivi** (vedi §5: corrisponde alla fascia che produce 8 blocchi).

### 2.2 Vincolo strutturale autoritativo: III / IV / V = 0 requisiti

`[SPEC §12:636]` dichiara testualmente: *"Parti interamente non tracciate: **Parte III** (Cap.12-15), **Parte IV** (Cap.16-21), **Parte V** (Cap.22-26) — matematica/motore interni, opachi al consumatore del segnale"*. Confermato riga per riga in §12:616-626.

Conseguenza vincolante: **Parti III, IV, V NON generano blocchi-spec** (zero requisiti da consolidare). Il tetto del numero di blocchi NON è 10 (le Parti della metodologia) ma le **~7 Parti che generano requisiti**: I, II, VI, VII, 8(solo Cap.42), 9, 10.

### 2.3 Lezione di rischio: i tagli densi/centrali e gli schemi esterni vanno spezzati

`[PROPOSTA §4:116]`: *"I tagli più larghi/centrali generarono più rework... Parte V GA, Parte VII validazione, Parte IX runtime ebbero i cicli più lunghi e i FAIL"*. E `[PROPOSTA §4:118]`: lo schema esterno (Parte IX) è "la fonte di errore più costosa". → i blocchi che ereditano densità o schemi esterni vanno **spezzati**, non accorpati.

---

## 3. Re-derivazione dei blocchi (dalla matrice §11)

### 3.1 Distribuzione dei 75 requisiti per sezione-spec / Parte-fonte

Conteggio derivato contando le righe della matrice §11 (`SPEC_FUNZ_01.md:528-602`), raggruppate per famiglia-ID (= sezione della spec attuale). **Ordini di grandezza**: la somma sezionale dà 76 contro i 75 dichiarati `[SPEC §11:604]` perché ≥1 requisito traccia a due Parti (es. CN-9.4 → Cap.10 PII ma vive in Sez.9 `[SPEC §11:599]`); la forchetta è dichiarata, non nascosta.

| Sez. | Famiglia ID | Parte/i fonte (matrice §11) | # req (o.d.g.) | Citazioni attese (o.d.g., ~1-2/req) |
|---|---|---|---|---|
| 1 | R-1.*, CN-1.1 | CAP_01 PI (+ tocchi PVI, PII) | ~5 | ~6-9 |
| 2 | R-2.*, CN-2.1 | CAP_01 PI (+ PVI, P9) | ~4 | ~5-8 |
| 3 | R-3.*, CN-3.1 | **CAP_02 PII** (+ tocchi PI, PVI) | **~12** | ~13-20 |
| 4 | R-4.*, CN-4.* | CAP_02 PII (CN-4.2 → P9) | ~6 | ~7-10 |
| 5 | R-5.*, CN-5.* | CAP_02 PII (CN-5.1 → PI) | ~5 | ~6-9 |
| 6 | R-6.*, NFR-6.* | **CAP_02 PII + CAP_06 PVI** | **~9** | ~12-16 |
| 7 | R-7.*, CN-7.* | **CAP_09 P9** (+ PI, PII) | **~11** | ~13-18 |
| 8 | NFR-8.* | **CAP_07 PVII + CAP_01 Cap.5 PI** | **~11** | ~16-22 |
| 9 | R-9.*, CN-9.* | **CAP_09 P9 + CAP_10 P10** (+ PII) | **~10** | ~13-18 |
| 10 | R-10.*, CN-10.1 | CAP_08 Cap.42 P8 (+ P9/P10/PVII) | ~3 | ~6-9 |

**Concentrazione**: la "Parte II" come consumatore-contratto = somma di Sez.3+4+5+6 = ~12+6+5+9 = **~32 requisiti** — coincide col "~30 req" che la PROPOSTA attribuiva a Parte II `[PROPOSTA §1:30, §3:101]`. È il nucleo denso, e contiene il blocco S-A "borderline".

### 3.2 Dal piano a 6 al piano a 8 (i due split decisi da AC)

Il piano intermedio a **6 blocchi** (analisi precedente, conservata per tracciabilità del ragionamento) accorpava:
- contratto Parte II in **2** blocchi (payload+state-machine insieme; emissione+consegna insieme);
- go-live in **1** blocco (gate + confine PHASE-2 insieme).

**La decisione AC applica due soli split a questo piano a 6:**
- **Split 1 — il contratto Parte II "payload" e "state-machine" si separano.** Sez.3 (payload R-3.*, ~12 req) diventa un blocco autonomo (**B2**); Sez.4 (state-machine/lifecycle R-4.*, ~6 req) diventa un blocco autonomo (**B3**). Motivazione: Sez.3 da sola è ~12 req (vicino al tetto della grana fine) e payload vs lifecycle sono due concern verificabili separatamente.
- **Split 2 — il go-live "gate" e "confine PHASE-2" si separano.** Sez.8 (NFR-gate go-live, ~11 req) diventa un blocco autonomo (**B7**); Sez.10 (confine PHASE-2 + fasizzazione, ~3 req) diventa un blocco autonomo (**B8**). Motivazione: il gate eredita densità PVII (cicli lunghi/FAIL storici `[PROPOSTA §4:116]`) e mescola rischio PENDING-empirico col confine PHASE-2, che è invece materia di fasizzazione/handoff a FASE-D.

**Le coppie coese restano unite** (NON spaccate dalla grana 8):
- **emissione (Sez.5) + consegna Telegram (Sez.6) restano insieme** in **B4** (~14 req): è la coppia coesa più importante — la consegna ha senso solo come destinazione dell'emissione, e R-5.*/R-6.* citano insieme CAP_02+CAP_06 `[SPEC §11:560-566]`.
- ambito (Sez.1) + operatore (Sez.2) restano insieme in **B1** (~9 req).
- runtime+sessione+compliance (Sez.7) resta un blocco unico **B5** (~11 req).
- schema-dato + continuità tape (Sez.9) resta un blocco unico **B6** (~10 req).

Questo è il punto chiave del costo residuo della grana 8: **a differenza di un'ipotetica grana 10**, qui emissione+consegna NON sono spaccate e il contratto NON è frantumato in 4 (payload/lifecycle/emissione/consegna). Lo split tocca solo i due blocchi più densi/eterogenei del piano a 6.

---

## 4. Piano definitivo — 8 blocchi

Numero **derivato dal piano a 6 + due split decisi da AC** (§3.2). Nomi e sezioni come da decisione AC; requisiti/citazioni come o.d.g. dichiarati e ancorati a §11.

| # | Blocco | Sez.-spec | CAP-fonte (da §11) | Req o.d.g. | Citazioni o.d.g. (~1-2/req) | 1 sessione? |
|---|---|---|---|---|---|---|
| **B1** | **Ambito & operatore** | Sez.1+2 (escl. CN-2.1) | CAP_01 PI Cap.1-3 — **CN-2.1 → B5** (dualità miniFIB/FIB-pieno, nucleo su CAP_09 Cap.47; B1 copre la parte FIB-pieno Cap.2) | ~8 | ~11-17 | **sì** (margine ampio) |
| **B2** | **Payload del segnale** | Sez.3 | CAP_02 PII Cap.6 (+ tocchi PI/PVI) | ~12 | ~13-20 | **sì** (il più carico con B4, ma in soglia) |
| **B3** | **State-machine & lifecycle** | Sez.4 (escl. CN-4.2) | CAP_02 PII Cap.7+Cap.11 — **CN-4.2 → B5** (fonte CAP_09 Cap.52, sessione runtime; già escluso da B3 in review) | ~5 | ~7-10 | **sì** (margine ampio) |
| **B4** | **Emissione & consegna Telegram** | Sez.5+6 | CAP_02 PII Cap.8-9 + CAP_06 PVI **Cap.29** (mobile-first §29.1-2 + 3 notifiche standard §29.4) | ~14 | ~18-25 | **sì** (il più carico con B2, ma in soglia) |
| **B5a** | **Motore & emissione runtime** `[PROVVISORIO — conferma AC: 0 req-v2 propri]` | — (nessun req-v2 di Sez.7) | CAP_06 PVI Cap.27 (pipeline inference, emission-only, latenza, ricalibr. EGARCH) + Cap.28 (anti-doppio, non-refresh, tie-break, determinismo replay) | **0** | — | n/a |
| **B5b** | **Canale dati DAPI** | parte Sez.7 + CN-2.1 | CAP_09 P9 Cap.46 (architettura canale/porte) + Cap.47 (catalogo/rollover/codici mese) + Cap.50 (errori/recovery/Darwin) | **~4** (R-7.2, CN-7.2, CN-7.5, CN-2.1) `+CN-7.1†, +CN-7.8†` | ~6-9 | **sì** |
| **B5c** | **Sessione, gating & compliance** | parte Sez.7 + CN-4.2 | CAP_09 P9 Cap.45 (premessa) + Cap.52 (sessione 08:00-22:00) + Cap.53 (gating cash) + Cap.54 (audit/retention) + CAP_01 Cap.1 (tocco) | **~5** (R-7.1, CN-7.6, CN-7.7, CN-7.9, CN-4.2) `+CN-7.8†` | ~7-10 | **sì** |
| **B6** | **Schema-dato DAPI & continuità tape** | Sez.9 | CAP_09 P9 **Cap.48, 49, 51** + CAP_10 P10 Cap.59-62 (CN-9.4→CAP_02 Cap.10) | ~9 | ~13-18 | **sì (con cautela RM massima)** |
| **B7** | **Gate di go-live** | Sez.8 | CAP_07 PVII Cap.31-36 + CAP_01 Cap.5 PI | ~11 | ~16-22 | **sì** |
| **B8** | **Confine PHASE-2 & fasizzazione** | Sez.10 | CAP_08 Cap.42 P8 (+ P9/P10/PVII) | ~3 | ~6-9 | **sì** (margine ampio) |

**Somma o.d.g.**: ~9+12+6+14+11+10+11+3 = **~76**, coerente con i 75 req `[SPEC §11:604]` (la forchetta = sovrapposizioni sezionali, §3.1).

> **Aggiornamento 2026-06-16 (decisione AC, B4-EXT-01 — Opzione 1)**: la riga B4 originaria assegnava `CAP_06 PVI Cap.27-29 interi` a B4. Verifica CLI (RM-2) su `CAP_06_parte_VI.md`: la **consegna** vive in **Cap.29** (mobile-first §29.1 `:146` → NFR-6.1; 3 notifiche standard §29.4 `:220` → R-6.4), mentre **Cap.27** (pipeline/inference EGARCH) e **Cap.28 intero** (§28.1 vincolo, §28.2 non-refresh, §28.3 tie-break, §28.4 determinismo/logging) sono **runtime**. Nota: le 3 notifiche standard sono fondate in **Cap.29.4**, **non** in Cap.28.4 (che è determinismo/logging). Decisione AC (Opzione 1): **B4 = Cap.8-9 + Cap.29** (consegna); **Cap.27-28 → B5** (runtime). Scostamento da "27-29 interi a B4" **autorizzato dal supervisore** e tracciato: nessun requisito perso (taglio consegna/runtime), divergenza solo sul contenitore.

> **Riconciliazione 2026-06-16 (MAP-RECON-AUDIT-01, autorizzata da AC)**: chiusi gli overlap di capitolo del confine **B5/B6** (CAP_09 Parte IX). La riga B5 usava il range inglobante `Cap.45-54`, che includeva capitoli assegnati anche a B6 (`Cap.49,51`) → **overlap su Cap.49 e Cap.51**. Risoluzione **per concern + sezione-requisito-v2** (un capitolo = un blocco): **B6 (schema-dato, Sez.9)** = `Cap.48` (format canonico CSV, R-9.1), `Cap.49` (decoder/mappatura schema→bundle, CN-9.1/R-9.1), `Cap.51` (warm-up/gap, R-9.2/R-9.3 — Sez.9 "dipendenze di dato/infrastruttura"); **B5 (runtime/sessione/compliance, Sez.7)** = `Cap.45` (premessa), `Cap.46` (architettura canale/porte, CN-7.2), `Cap.50` (errori/recovery/Darwin), `Cap.52` (sessione 08:00-22:00, R-7.1), `Cap.54` (audit log/retention, CN-7.6/7/8). **CN-4.2** (Sez.4, "chiusura 22:00 non chiude segnale active", fonte CAP_09 Cap.52) **→ B5**, non B3: già escluso correttamente dalla review B3 (fuori perimetro Cap.7/11). **Partizione requisiti-v2: 1-a-1 completa, 0 gap, 0 orfani** (Sez.1+2→B1, Sez.3→B2, Sez.4 escl. CN-4.2→B3, Sez.5+6→B4, Sez.7+CN-4.2→B5, Sez.8→B7, Sez.9→B6, Sez.10→B8 = 75 req).

> **Finalizzazione 2026-06-16 (MAP-FINAL-AUDIT-02, decisa da AC)**: i due confini provvisori sono **confermati B5** (rimossi i `†`).
> - **Cap.47 → B5** (fonda R-7.2 boot scadenza/CONTRACT_SWITCH, CN-7.5 codici mese). Lo **schema BOOK_5/ANAG per simbolo** è **premessa citabile da B6** (decoder), non si consolida in B5 oltre la sottoscrizione/rollover. **Avvertenza**: i codici mese **Mar/Dic** sono empiricamente **APERTI** (Cap.55, verifica parziale) → il requisito B5 relativo sarà **PENDING-empirico**.
> - **Cap.53 → B5** (fonda CN-7.9, gating qualitativo post-emissione, fuori-GA, `config/gating_rules.yaml`). L'**annotazione di gating si attacca al messaggio Telegram** = **premessa verso B4** (contratto del messaggio), **non** uno split verso B6. Il logging dei tick PRICE resta in audit (Cap.54, già B5).
> - **Dualità sull'asse-requisito verificata (RM-2)**: né Cap.47 né Cap.53 fondano alcun requisito di **Sez.9** (grep `R-9.*`/`CN-9.*` × `Cap.47|Cap.53` = 0 occorrenze; la Sez.9 è fondata da Cap.48/49/51) → assegnazione B5 pulita, non duale sull'asse-requisito.
> - **Cap.30 (Parte VI, "Monitoraggio del lifecycle in produzione") → FUORI perimetro spec**: nessun requisito-prodotto v2 lo fonda come fonte primaria; la v2 lo colloca in §12 "capitoli non tracciati" (`SPEC_FUNZ_01.md:628`: "monitoraggio/dashboard — Interna/FASE-D; citata per contrasto col gate bloccante R-9.4 e per AC-GO-11/NFR-8.8, **non requisito a sé**"). Annotato qui perché non sparisca all'assemblaggio: **dettaglio di monitoraggio FASE-D, nessun blocco lo consolida**.
> **CN-2.1 → B5 (decisione AC, opzione A, 2026-06-16)**: la dualità **miniFIB (1€/punto, esecuzione) / FIB-pieno (5€/punto, calibrazione+inference)** ha il nucleo distintivo su **CAP_09 Cap.47** (catalogo simboli MINI6F/MINI6I), perimetro B5. B1 copre la sola parte FIB-pieno (CAP_01 Cap.2: moltiplicatore 5€/punto, 1 contratto). Riassegnato a **B5** (analogo a CN-4.2), non estensione di B1 → **B1 resta CLEAN sul perimetro Cap.1-3**. Trovato dall'audit per-ID MAP-FINAL-AUDIT-02 (la dualità non era nel perimetro-fonte di B1, quindi non rilevabile dal confronto-copertura della review B1).
> **Overlap residui: nessuno. Partizione req-v2: 1-a-1, 0 gap, 0 orfani (Sez.2 escl. CN-2.1→B1; CN-2.1→B5). Mappa finalizzata.**

> **Split B5 → B5a/B5b/B5c 2026-06-16 (MAP-SPLIT-B5-03, per natura — con riserve da ratificare)**: la riga B5 è stata spaccata in tre per natura (B5a motore/emissione runtime; B5b canale DAPI; B5c sessione/gating/compliance) dividendo i req di **Sez.7 (11) + CN-4.2 + CN-2.1** per capitolo-fonte (matrice §11 `SPEC_FUNZ_01.md:569-579`). **Assegnazioni certe**: B5b = R-7.2 (Cap.47), CN-7.2 (Cap.46), CN-7.5 (Cap.47), **CN-2.1** (Cap.47); B5c = R-7.1 (Cap.52), CN-7.6 (Cap.54), CN-7.7 (Cap.54), CN-7.9 (Cap.53), **CN-4.2** (Cap.52). **† DA CONFERMARE AC (capitolo-fonte ambiguo/fuori, F-3, non deciso d'arbitrio)**:
> - **B5a senza requisiti-prodotto v2 propri**: Cap.27/28 fondano R-1.2 (→B1), R-3.10 (→B2), NFR-6.2 (→B4), CN-9.4 (→B6), **tutti già coperti**. B5a è un contenitore di **runtime di produzione FASE-D senza requisiti-spec nuovi** (analogo a Cap.30 fuori-scope). **Decisione AC**: tenerlo come blocco-spec vuoto, marcarlo FUORI-SCOPE come Cap.30, o assorbire Cap.27/28 come "tocchi runtime" senza blocco dedicato.
> - **CN-7.1** (non instrada ordini, Cap.1/Cap.46): duale B5b (canale, porta 10002 mai aperta) / B5c (compliance separazione segnale-esecuzione).
> - **CN-7.8** (account code PII, Cap.46+Cap.54): duale B5b (Cap.46) / B5c (Cap.54 audit) — raccomando B5c.
> - **CN-7.3** (commissioni 5€, Cap.2,5 = B1/B7) e **CN-7.4** (gestione post-fill, Cap.2/Cap.11 = B1/B3): capitolo-fonte **fuori** dai tre sotto-blocchi B5; **verosimilmente già coperti** (CN-7.3 in B1-CN-05/B1-R-19; CN-7.4 in B3 out-of-scope post-target_1). **Decisione AC**: confermare che escono da B5 (già in B1/B3) o riportarli in un sotto-blocco B5.
> **Conteggio Sez.7 (11) preservato**: B5b 3 + B5c 4 + provvisori {CN-7.1, CN-7.8, CN-7.3, CN-7.4} 4 = 11. Partizione 1-a-1 **con riserva sui †** (sub-judice AC); nessun requisito perso o duplicato.

**Fattibilità in 1 sessione (grana 8)**: a questa grana **tutti i blocchi sono fattibili in 1 sessione**. I due più carichi sono **B2 (~12 req)** e **B4 (~14 req)**, entrambi **in soglia** (~10-14): sono i tetti del piano, ma non sforano la grana fine decisa da AC. Gli altri sei hanno margine.

### Dipendenze & rischi specifici per blocco

- **B1 — Ambito & operatore.** Nucleo-fondamenta: tutto ne dipende. Rischio basso. Ottimo primo blocco/pilota per tarare il ciclo a 8 blocchi.
- **B2 — Payload del segnale.** Cuore del contratto. **Dipendenza fragile: CAP-02 a `<sha-da-confermare>`** `[STATO_CORRENTE:8]` — citabile (freeze G-09) ma **SHA non pinnabile finché AC non conferma** → **nota di testa obbligatoria** nel doc di questo blocco. È il più carico insieme a B4 (~12 req).
- **B3 — State-machine & lifecycle.** Stesso CAP-02 di B2 (idem nota SHA). CN-4.2 traccia a CAP_09 Cap.52 (lifecycle ↔ runtime). Rischio basso-medio; coeso con B2 (vedi §6, accoppiamento da sorvegliare).
- **B4 — Emissione & consegna Telegram.** Cita CAP-02 (idem nota SHA) + CAP_06 PVI. **B-1/M-2 (latenza Telegram, OPEN)** `[CARRYOVER:21]` → recepire come provvisorio (`[B-1 PROVVISORIO]`, NFR-6.2 `[SPEC §13:644]`), **non chiuderlo**. È il più carico in assoluto (~14 req), in soglia. Rischio medio.
- **B5 — Runtime DAPI, sessione & compliance.** **B-2/M-GOV-1 (orario sessione, APERTO)** `[CARRYOVER:37]` → recepire provvisorio (`[B-2 PROVVISORIO]`, R-7.1 `[SPEC §13:649]`). Compliance "no esecuzione ordini" (CN-7.*). **NON contiene lo schema-dato** (isolato in B6). Rischio medio.
- **B6 — Schema-dato DAPI & continuità tape.** ⚠ **Rischio RM-2/RM-3 PIÙ ALTO dell'intero perimetro.** Tocca schema CANDLE `C;L;H;O;V`, BOOK_5, PRICE, decoder canonico. È il perimetro del BUG catastrofico storico (CANDLE invertito) `[CARRYOVER M-1/RACC-METODO-2:49]`, `[STATO M-1:83, M-9:91, M-10:92]`. **AC obbligatorio: diff puntuale col decoder canonico `export_directa_history_parametric.py` (RM-2)**, **mai col wiki (RM-3)**. Isolarlo è il vantaggio chiave del chunking: il Reviewer concentra il 100%-check su un blocco piccolo.
- **B7 — Gate di go-live.** Tutti gli NFR-gate (DSR/PBO/$E[R_{net}]$/checklist 12 AC). **Tutte le claim sull'edge restano PENDING-empirico fino al validator (FASE-D)** `[SPEC §10 R-10.2:504]` — recepisce *criteri dichiarati*, non risultati. Citazioni dense (NFR×PVII ~2/req). Nessun rischio RM-2/3 (no schemi esterni). Eredita la densità PVII (cicli lunghi/FAIL storici `[PROPOSTA §4:116]`).
- **B8 — Confine PHASE-2 & fasizzazione.** Ponte verso FASE-D e verso una futura SPEC-FUNZ cross-index. Piccolo (~3 req), margine ampio. Chiude naturalmente la serie. Nessun rischio RM-2/3.

---

## 5. Analisi di sensibilità (dove cade l'8)

Come cambia il numero di blocchi al variare della soglia. Il numero NON è un dato del repo: è funzione della soglia, **[DECISIONE AC]**.

| Soglia req/blocco | Logica | Blocchi | Note |
|---|---|---|---|
| **~30-35** (larga, = PROPOSTA storica) | accorpa per consumatore | **3** (S-A/S-B/S-C) | PROPOSTA storica; S-A borderline `[PROPOSTA §3:72]`. Respinta da AC ("troppo pochi"). |
| **~20** (media-alta) | spezza solo Parte II e IX+X | **~5** | B1 / Sez3+4 / Sez5+6 / Sez7 / Sez8+9+10 accorpati (sfora). |
| **~15-20** (media) | spezza Parte II in 2, isola schema-dato, separa go-live in 1 | **~6** | piano intermedio (§3.2): contratto in 2, go-live in 1. |
| **~10-14** (grana fine — **DECISIONE AC**) | piano a 6 **+ due split**: payload\|state-machine e gate\|confine | **8** ← | **il piano §4.** L'8 cade **fra ~20→5 e ~10-12→8-9**: corrisponde allo **split dei due blocchi più densi/eterogenei del piano a 6** (Parte-II-contratto e go-live), tenendo unite le coppie coese (emissione+consegna; ambito+operatore; runtime; schema-dato). |
| **~10-12** (stretta pura) | un blocco ≈ una famiglia-ID coesa | **~8-9** | spaccherebbe anche emissione\|consegna (Sez.5\|Sez.6) → rischio frammentazione di requisiti coesi (R-5.*/R-6.* citano insieme CAP_02+CAP_06 `[SPEC §11:560-566]`). **L'8 deciso da AC NON arriva qui**: ferma lo split a contratto e go-live, NON tocca emissione+consegna. |

**Lettura**: l'8 deciso da AC si colloca **appena dentro la grana fine**, ottenuto in modo controllato (due split mirati sul piano a 6) e **senza** scendere alla stretta pura che frammenterebbe la coppia emissione+consegna. È robusto al rework (margine su 6 blocchi su 8; i due tetti B2/B4 restano in soglia).

---

## 6. Nota sull'accoppiamento (costo residuo della grana 8)

Lo split del contratto Parte II crea **un unico punto di accoppiamento da sorvegliare**: **B2 (payload, Sez.3)** e **B3 (state-machine, Sez.4)** derivano **entrambi da CAP_02 PII** e sono concettualmente coesi (un payload esiste dentro un lifecycle).

**Conseguenza operativa, vincolante in review**: nel **confronto-copertura in fase di review** di B2 e di B3 (modalità B — confronto col perimetro corrispondente di SPEC-FUNZ-01 v2 congelata), il Reviewer **verifica esplicitamente che nessun requisito coeso payload/lifecycle sia caduto nel taglio fra i due blocchi**. È un rischio **gestito, non bloccante**.

Questo è l'unico costo strutturale introdotto dalla grana 8 rispetto al piano a 6. A differenza di un'ipotetica grana 10: qui **emissione+consegna NON sono spaccate** (restano in B4) e **il contratto NON è frantumato in 4** (solo payload\|lifecycle, non payload\|lifecycle\|emissione\|consegna). Lo split go-live (B7\|B8) non introduce accoppiamento analogo: gate (NFR/PVII) e confine PHASE-2 (fasizzazione/P8) sono materie distinte con consumatori diversi.

---

## 7. Ordine di esecuzione

**Metodo (cornice — richiamata, non oggetto di questo piano)**: ogni blocco = **un ciclo Planner→Developer→Reviewer = un PASS**, eseguito **uno alla volta** (BASE_COMUNE §1). Il Developer costruisce **in CIECO dai CAP-fonte**; **SPEC-FUNZ-01 v2 resta congelata** (PASS `ab7450f` `[STATO:6]`) e il **confronto di copertura** col perimetro corrispondente di SPEC-FUNZ-01 si fa **SOLO in fase di review** (modalità B, già validata per SPEC-FUNZ-01 v2 `[STATO:18]`). **Sede CLI** per tutto il ciclo (GOV-SURFACES-01).

**Ordine raccomandato**: **B1 → B2 → B3 → B4 → B5 → B6 → B7 → B8**
(fondamenta → contratto-payload → contratto-lifecycle → consegna → runtime → dato → go-live → confine).

1. **B1 — Ambito & operatore.** Fondamenta: strumento/operatore/target da cui tutti dipendono. Piccolo, basso rischio → blocco-pilota per tarare il ciclo a 8.
2. **B2 — Payload del segnale.** Cuore del contratto; precede la consegna (B4) e il dato (B6). Attenzione SHA CAP-02.
3. **B3 — State-machine & lifecycle.** Coeso con B2 (accoppiamento da sorvegliare in review, §6). Idem SHA CAP-02.
4. **B4 — Emissione & consegna Telegram.** Dipende dal contratto (B2/B3). Porta B-1/M-2 (provvisorio).
5. **B5 — Runtime DAPI, sessione & compliance.** Versante operativo. Porta B-2/M-GOV-1 (provvisorio).
6. **B6 — Schema-dato & continuità tape.** Affrontato a ciclo rodato (B1-B5 hanno già allenato il Reviewer al diff-vs-decoder). AC obbligatori RM-2/RM-3.
7. **B7 — Gate di go-live.** Ponte verso FASE-D; edge PENDING-empirico.
8. **B8 — Confine PHASE-2 & fasizzazione.** Ultimo: chiude la serie, fasizza l'handoff a FASE-D / futura SPEC-FUNZ cross-index.

L'ordine è **[DECISIONE AC]** (in particolare se anticipare B6 per smaltire prima il rischio RM più alto, vedi §8).

---

## 8. Censimento M ri-assegnato agli 8 blocchi (nessuno perso)

| M / promemoria | Stato | Origine | Destinazione | Modalità di recepimento |
|---|---|---|---|---|
| **M-2 / B-1** (latenza Telegram) | OPEN `[CARRYOVER:21]` | NFR-6.2 `[SPEC §13:644]` | **B4** | recepire `[B-1 PROVVISORIO]`, **non chiudere** |
| **M-GOV-1 / B-2** (orario sessione) | APERTO `[CARRYOVER:37]` | R-7.1 `[SPEC §13:649]` | **B5** | recepire `[B-2 PROVVISORIO]`, **non chiudere** |
| **M-1** (schema CANDLE) | nota tecnica-fonte `[STATO:83]` | decoder canonico | **B6** | fonte `[CODICE-ESISTENTE]`/`[PROVA-EMPIRICA]`, **mai** re-asserita di prima istanza |
| **M-9** (PRICE) | nota tecnica-fonte `[STATO:91]` | decoder canonico | **B6** | idem M-1 |
| **M-10** (BOOK_5) | nota tecnica-fonte `[STATO:92]` | decoder canonico | **B6** | idem M-1 |
| **RACC-METODO-2** (diff vs decoder canonico) | regola permanente `[CARRYOVER:49]` | METODO §RACC-METODO-2 | **B6** | **AC obbligatorio** del blocco |
| **M-4..M-16** (CAP-04/05/06/07) | CLOSED `[CARRYOVER:22-36]` | — | nessun blocco | eventuale fonte storica |
| **M-GOV-2** (slot SPEC-FUNZ-01) | CHIUSO | — | nessun blocco | — |

Nessun M aperto resta non assegnato. La doppia-tracciatura CN-9.4 (vive in Sez.9/B6 ma traccia a CAP_02 Cap.10) è registrata come punto [DECISIONE AC] di ownership (§9).

---

## 9. Punti [DECISIONE AC] residui

Questi **NON bloccano** la finalizzazione del piano a 8: si sciolgono all'apertura del singolo task.

- **[DECISIONE AC — ordine di esecuzione]**: sequenza **B1→B8** raccomandata (§7) **vs** anticipo di **B6** (schema-dato) per smaltire prima il rischio RM-2/RM-3 più alto. La raccomandazione è B6 penultimo (a ciclo rodato); l'anticipo è una scelta legittima di gestione-rischio.
- **[DECISIONE AC — ownership a doppia-tracciatura]**: requisiti che tracciano a due blocchi adiacenti. Caso esplicito: **CN-9.4** vive in Sez.9 (**B6**) ma traccia a CAP_02 Cap.10 (perimetro contratto/B2-B3) `[SPEC §11:599]`. Da decidere in quale blocco è "owned" (e nell'altro solo citato come riferimento), all'apertura del task del blocco interessato.
- **[DECISIONE AC — accoppiamento B2/B3]**: confermare la regola di review §6 (confronto-copertura incrociato payload/lifecycle) come AC esplicito del task di B2 e di B3, oppure lasciarlo come nota di sorveglianza al Reviewer.

### Dipendenze fragili da segnalare (avvisi, non decisioni)

- **CAP-02 a `<sha-da-confermare>`** `[STATO_CORRENTE:8]` → tocca **B2, B3, B4** (e B6 via CN-9.4): citabile (freeze G-09) ma SHA non pinnabile finché AC non conferma → **nota di testa** nei doc di quei blocchi.
- **B-1/M-2** (latenza Telegram) OPEN `[CARRYOVER:21]` → **B4** (`[B-1 PROVVISORIO]`).
- **B-2/M-GOV-1** (orario sessione) APERTO `[CARRYOVER:37]` → **B5** (`[B-2 PROVVISORIO]`).
- **Schema DAPI in B6** = punto a più alto rischio RM-2/RM-3 dell'intero perimetro `[CARRYOVER M-1/RACC-METODO-2:49]`, `[STATO M-1:83, M-9:91, M-10:92]`.
- **Edge in B7** = PENDING-empirico fino al validator (FASE-D) `[SPEC §10 R-10.2:504]`.

---

*Documento di pianificazione (chunking). Piano FINALIZZATO a 8 blocchi (decisione AC). Nessuna spec scritta, nessun ACTIVE_TASK aperto, nessun CAP modificato (freeze G-09 rispettato). Non committato (lo fa l'Orchestratore). Prossimo passo = apertura del task del primo blocco (B1) secondo l'ordine §7, salvo diversa [DECISIONE AC] sull'ordine.*
