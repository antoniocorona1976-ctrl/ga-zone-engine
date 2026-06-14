# PROPOSTA — Suddivisione del lavoro business-spec (analisi, non esecuzione)

**Natura**: documento di **analisi e proposta**, non esecutivo. Prodotto dal ruolo `spec_planner` in modalità diagnosi. NON apre `ACTIVE_TASK.md`, NON scrive spec, NON invoca agenti. I capitoli `docs/methodology_v2/CAP_*` sono stati **solo letti** (freeze G-09 rispettato).

**Domanda di AC**: SPEC-FUNZ-01 v2 (chiusa PASS `ab7450f`) copre l'intero documento metodologico (10 Parti, Cap.1-65, 75 requisiti). Lo scope è troppo ampio per **organizzazione** (non per qualità)? Andava spezzato capitolo-per-blocco come la metodologia?

**Fonti di questa analisi** (lette, non re-derivate):
- `docs/methodology_v2/00_indice.md` (stato e contenuto delle 10 Parti).
- `docs/spec_funzionale/SPEC_FUNZ_01.md` (75 requisiti, matrice §11, capitoli-non-tracciati §12, blocchi §13).
- `tasks/STATO_CORRENTE.md`, `tasks/CARRYOVER.md` (marcatori di chiusura, M aperti).
- `git log` + `reviews/` (METODO di costruzione del doc metodologico — non merito dei CAP).

**Applicazione RM-1 a me stesso**: ogni claim "Parte X è core / di fase successiva" e "blocco Y regge una sessione" è ancorato a una citazione puntuale dell'indice o della matrice §11. Dove il repo non disambigua, la voce è marcata esplicitamente **[DECISIONE AC]** e NON presentata come fatto.

---

## 1. Verdetto Compito 1 — diagnosi scope

### Verdetto: **(C) MISTO / INCERTO con baricentro su (A)**

Il repo sostiene che SPEC-FUNZ-01 v2 **non ha gonfiato lo scope sul piano dei contenuti** (tutte le 10 Parti contribuiscono requisiti legittimi a un prodotto FIB-only di Fase 1 già definito), **ma ha gonfiato lo scope sul piano dell'organizzazione** (un solo documento-contenitore aggrega 75 requisiti eterogenei che tracciano a Parti con maturità e natura molto diverse). Il problema di AC è reale ma è di **impaginazione/granularità del lavoro**, non di perimetro dei requisiti. Da qui il "misto": la sostanza è (A) scope corretto, l'articolazione è (B) ri-articolabile.

### Evidenza Parte-per-Parte

Classifico ogni Parte come **core-Fase-1** (i suoi requisiti servono al prodotto-segnale FIB già operativo / al go-live di Fase 1) o **fase-successiva** (cross-index PHASE-2, estensioni). Fonte: indice + matrice §11 + §12 della spec.

| Parte | Capitoli | Requisiti che ne derivano (matrice §11) | Classe | Evidenza |
|---|---|---|---|---|
| **Parte I** (Ambito/vincoli) | Cap.1-5 | R-1.1..R-1.4, CN-1.1, R-2.1/2.2, CN-7.3, CN-5.1, NFR-8.1..8.5/8.9/8.10/8.11 (Cap.5) | **Core-Fase-1** | Definisce strumento, operatore, target, successo. `[SPEC §11:528-533, 558, 573, 580-590]`. Cap.4 (compute/cloud) è **dipendenza infrastrutturale, non requisito** `[SPEC §12:614]`. |
| **Parte II** (Contratto segnale) | Cap.6-11 | R-3.1..R-3.11, CN-3.1, R-4.1..R-4.4, CN-4.1, R-5.1..R-5.3, CN-5.1/5.2, R-6.1..R-6.7, NFR-6.2, CN-7.4, NFR-8.11, CN-9.4 | **Core-Fase-1 (nucleo)** | È il contratto del prodotto-segnale: payload, state machine, emissione, Telegram. ~30 requisiti `[SPEC §11:537-566, 574, 590, 599]`. Massima densità. |
| **Parte III** (Layer quant.) | Cap.12-15 | **0 requisiti diretti** (matematica interna) | **Core-Fase-1 (opaca)** | **Interamente non tracciata** `[SPEC §12:636]`: alimenta le condizioni di emissione (Sez.5) ma è opaca al consumatore. Necessaria al prodotto, non esposta come requisito. |
| **Parte IV** (Geometria/survival) | Cap.16-21 | **0 requisiti diretti** (derivazione interna) | **Core-Fase-1 (opaca)** | **Interamente non tracciata** `[SPEC §12:636]`: il prodotto pubblica entry_zone/target/stop, non la geometria che li produce. |
| **Parte V** (Motore GA) | Cap.22-26 | **0 requisiti diretti**; i *gate* emergono via Parte VII | **Core-Fase-1 (opaca)** | **Interamente non tracciata** `[SPEC §12:626, 636]`: il GA è il motore, opaco; i suoi esiti diventano NFR via Parte VII. |
| **Parte VI** (Emissione runtime) | Cap.27-30 | R-1.2, R-2.3, R-3.10, R-6.1/6.4/6.5/6.6, NFR-6.1 | **Core-Fase-1** | Pipeline inference, anti-doppio-segnale, layout Telegram mobile. `[SPEC §11:529, 535, 546, 560-567]`. Cap.27/30 citati ma non req. a sé `[SPEC §12:627-628]`. |
| **Parte VII** (Validazione OOS) | Cap.31-36 | NFR-6.2, NFR-8.1..8.8, R-10.2 | **Core-Fase-1 (go-live)** | Tutti i gate di accettazione del prodotto (DSR/PBO/$E[R_{net}]$/checklist 12 AC). `[SPEC §11:568, 580-587, 601]`. Claim sull'edge restano **PENDING-empirico** (validator FASE-D) `[SPEC §8:367]`. |
| **Parte 8** (Dati storici) | Cap.37-44 | **Solo Cap.42** → R-10.1, CN-10.1, CN-9.3 (Cap.44) | **MISTO: una voce fase-successiva** | Cap.37-44 sono **materia di training / dipendenza infrastrutturale** `[SPEC §12:631]`. L'unico capitolo tracciato come requisito di prodotto è **Cap.42 = fasizzazione PHASE-1/PHASE-2** (R-10.1/CN-10.1) — che è esattamente il **confine verso la fase successiva**. `[SPEC §11:600, 602]`. |
| **Parte 9** (Runtime DAPI) | Cap.45-56 | CN-2.1, CN-4.2, R-7.1/7.2, CN-7.1/7.2/7.5..7.9, CN-9.1, R-9.1/9.2 | **Core-Fase-1** | Pipeline runtime Directa, sessione, rollover, audit, compliance "solo emissione". `[SPEC §11:536, 554, 569-579, 591-593]`. Schema CANDLE/decoder = dato sensibile RM (vedi §3 rischi). |
| **Parte 10** (Continuità tape) | Cap.57-65 | R-9.3/9.4/9.5, CN-9.2/9.3 | **Core-Fase-1** | Backfill, riconciliazione bloccante, archivio. `[SPEC §11:594-598]`. Capitoli di cornice (57/58/63/64/65) non tracciati `[SPEC §12:634]`. |

### Lettura del verdetto

1. **Nessuna Parte è interamente "fase successiva"**. L'unico contenuto esplicitamente PHASE-2 (cross-index) è **dichiarato fuori scope** dalla spec stessa (R-10.1, CN-10.1, §10) e tracciato solo per marcarne il **confine**, non per specificarlo. Quindi sul piano dei contenuti la spec **non importa requisiti di fase successiva**: li nomina per escluderli. Questo sostiene **(A)**.
2. **Tre Parti su dieci (III, IV, V) producono ZERO requisiti** e sono dichiarate "interamente non tracciate" `[SPEC §12:636]`. Sono core ma **opache**: il loro contributo alla spec è una manciata di NFR-gate indiretti (via Parte VII) e nulla di diretto. Aggregarle nello stesso documento delle Parti ad alta densità (II, IX) è ciò che fa **percepire** l'ampiezza: 150 pagine di metodologia "attraversate" ma con resa-in-requisiti fortemente non uniforme. Questo è il nucleo di verità di **(B)**, ma è un problema di **organizzazione del lavoro di consolidamento**, non di scope dei requisiti.
3. **La densità è fortemente concentrata**: Parte II da sola genera ~30 dei 75 requisiti; Parti II+IX+X coprono la grande maggioranza dei requisiti R/CN operativi; Parti I+VII coprono quasi tutti gli NFR. Le Parti III/IV/V sono "passaggi obbligati ma muti".

**Conclusione Compito 1**: il repo **non sostiene (B) puro** (non ci sono requisiti di fase-2 mascherati da fase-1). Sostiene **(A) sul merito** con una **riserva organizzativa** (la singola spec mescola Parti dense, Parti opache e il confine PHASE-2): da qui **(C)**, con raccomandazione che il vero asse di un'eventuale ri-articolazione è la **densità/natura del consolidamento**, non il taglio Fase-1/Fase-2.

---

## 2. Implicazione su SPEC-FUNZ-01

**SPEC-FUNZ-01 v2 va LASCIATA com'è (chiusa PASS `ab7450f`). NON spezzarla retroattivamente.** Motivi, con evidenza:

- **Qualità non in discussione**: AC stesso pone la domanda "non per qualità (requisiti verificati, citazioni 100%) ma per organizzazione". Lo stato conferma: Review v2 PASS, micro-pass KPI, re-review PASS, 75 requisiti tracciati 1:1 (matrice 75 righe, 0 orfani, 0 mancanti) `[SPEC §11:604]`. Spezzare un documento PASS introduce churn e rischio regressione su un artefatto sano. Il freeze e la disciplina del progetto (MEMORY: "non chiudere/riaprire senza ragione normata") sconsigliano la riapertura di un PASS.
- **Coesione effettiva**: i 75 requisiti tracciano in larga parte a **Cap.5 (PI) e Parte II**, che sono il cuore unico del contratto-prodotto. Una scomposizione per-Parte spaccherebbe requisiti coesi (es. payload R-3.* e consegna Telegram R-6.* citano sia CAP_02 che CAP_06: `[SPEC §11:560-566]`) — esattamente il rischio "troppo stretto → frammenta requisiti coesi".
- **Il valore organizzativo si recupera in avanti, non indietro**: la lezione di AC è valida come **criterio per il lavoro futuro** (SPEC-FUNZ-02, …) e per un eventuale *re-indicizzamento* leggero di SPEC-FUNZ-01 (raggruppare le 13 sezioni esistenti in "macro-blocchi" tematici **dentro** il documento, senza spaccarlo). Questo è un micro-pass cosmetico opzionale, **[DECISIONE AC]**, non una ricostruzione.

**Sintesi**: lasciare; capitalizzare la lezione su ciò che viene dopo.

---

## 3. Proposta di suddivisione del lavoro business-spec (forward-looking)

La proposta vale **per come articolare il lavoro business-spec d'ora in avanti** (e come modello retrospettivo di "come si sarebbe potuto spezzare", a fini di apprendimento). Riarticola i 75 requisiti **già esistenti** in blocchi coerenti — **NON li riscrive** (sono PASS): se SPEC-FUNZ-01 fosse mai re-indicizzata o se si volesse un set di spec parallele sostitutive, questi sarebbero i tagli.

Asse di taglio scelto: **densità + natura del consumatore** (contratto / consegna / runtime-dato / gate-go-live / fasizzazione), NON il taglio per-Parte metodologica (che produrrebbe 3 blocchi vuoti). Motivazione della divergenza dal modello metodologico in §4.

### Blocco S-A — Contratto del segnale e consegna (nucleo prodotto)
- **Parti/capitoli coperti**: Parte I Cap.1-2 (ambito, operatore), Parte II Cap.6-9 (payload, state machine, emissione, Telegram), Parte VI Cap.28-29 (anti-doppio-segnale, layout mobile).
- **Requisiti attesi (ordine di grandezza)**: **~30-35** — i requisiti R-1.*, R-2.*, R-3.*, R-4.*, R-5.*, R-6.*, CN-1.1, CN-3.1, CN-4.*, CN-5.*, NFR-6.* della spec attuale. *(Ordine di grandezza dichiarato: conteggio derivato dalle Sez.1-6 della spec esistente, non re-inventato; la cifra esatta dipende dall'atomizzazione.)*
- **Perché stanno insieme**: è il contratto su cui l'operatore agisce — il "cosa pubblica e come lo consuma". È l'unico blocco che l'operatore legge davvero.
- **Fattibilità in una sessione**: **borderline**. È il blocco più denso (~30+ requisiti, ~6 sezioni). Una sessione regge con accuratezza piena solo se il Reviewer verifica il 100% delle citazioni verso CAP_01/CAP_02/CAP_06 — è molto. Rischio residui ↑ per ampiezza. Possibile split in S-A1 (payload+state machine, Parte II Cap.6-7) e S-A2 (emissione+consegna, Cap.8-9 + Parte VI) se si vuole margine. **[DECISIONE AC]** sul taglio fine.
- **Dipendenze/rischi**: cita **CAP-01 e CAP-02 a SHA-non-confermato** (`CAP-02: CHIUSO PASS <sha-da-confermare>` in STATO_CORRENTE:8) — **dipendenza fragile dichiarata**: i capitoli sono congelati e citabili, ma lo SHA-review di CAP-02 non è pinnabile finché non confermato (freeze G-09). Va dichiarato in nota di testa come fa la spec attuale `[SPEC §nota-di-testa:12]`, non bloccante.

### Blocco S-B — Runtime, dato e compliance
- **Parti/capitoli coperti**: Parte IX Cap.45-56 (pipeline DAPI, sessione, rollover, audit, gating cash, PII), Parte X Cap.57-65 (continuità tape, recupero gap, riconciliazione, archivio), più i ganci dato di Parte II Cap.10 (determinismo).
- **Requisiti attesi (ordine di grandezza)**: **~20-25** — R-7.*, R-9.*, CN-2.1, CN-4.2, CN-7.*, CN-9.* della spec attuale (Sez.7 e Sez.9). *(Ordine di grandezza; derivato dal conteggio Sez.7+9.)*
- **Perché stanno insieme**: è il versante infrastruttura-dato-compliance del prodotto: come arriva il dato, come si garantisce "solo emissione", audit, sessione, rollover. Consumatore = chi implementa/opera la pipeline (FASE-D), non l'operatore-segnale.
- **Fattibilità in una sessione**: **sì** (con cautela RM). ~20-25 requisiti su Parti IX/X ben delimitate.
- **Dipendenze/rischi**: **rischio RM-2/RM-3 elevato e documentato**. Questo blocco tocca lo schema DAPI (CANDLE `C;L;H;O;V`, BOOK_5, PRICE) e il decoder canonico. È esattamente il perimetro dove la metodologia ha avuto il **BUG REALE catastrofico** dello schema CANDLE invertito `O;H;L;C` (audit RM-RETRO CAP-DATA-02, indice:77; M-1 STATO_CORRENTE:83). La spec attuale lo cita correttamente (CN-9.1 con `[CODICE-ESISTENTE ...:477-481]` + `[PROVA-EMPIRICA M-1]`): qualsiasi ri-lavorazione DEVE mantenere il diff col decoder canonico (RACC-METODO-2, CARRYOVER:49), mai col wiki. **Dipendenza fragile**: B-2/M-GOV-1 (orario sessione, R-7.1 `[B-2 PROVVISORIO]`) APERTO fino al probe V-1 (CARRYOVER:37).

### Blocco S-C — Gate di go-live e fasizzazione
- **Parti/capitoli coperti**: Parte I Cap.5 (definizione di successo, metriche), Parte VII Cap.31-36 (validazione OOS, DSR, PBO, bootstrap, frozen bundle, gate), Parte 8 Cap.42 (fasizzazione PHASE-1/2), i rinvii FASE-D.
- **Requisiti attesi (ordine di grandezza)**: **~13-15** — NFR-8.*, R-10.*, CN-10.1, NFR-6.2 (latenza gate). *(Ordine di grandezza; derivato da Sez.8+10.)*
- **Perché stanno insieme**: è il "quando il prodotto è pronto" + "fin dove arriva la Fase 1". Tutti gli NFR di accettazione e il confine PHASE-2 stanno qui. È il blocco-ponte verso FASE-D e verso un'eventuale SPEC-FUNZ-02 cross-index.
- **Fattibilità in una sessione**: **sì** (la più sicura). ~13-15 requisiti, alta omogeneità (sono quasi tutti NFR-gate + confine).
- **Dipendenze/rischi**: tutte le claim sull'edge sono **PENDING-empirico** fino al validator (FASE-D) `[SPEC §8:367]`: il blocco recepisce criteri dichiarati, non risultati — coerente col fatto che il ruolo `validator` è in panchina. Nessun rischio RM-2/3 (no schemi esterni). B-1/M-2 (latenza Telegram) APERTO.

### Le Parti III, IV, V (matematica/motore opaco)
**Non generano un blocco-spec proprio**: producono 0 requisiti diretti (§12:636). Il loro contributo è già assorbito (gate via Parte VII → S-C; condizioni di emissione via Parte II → S-A). **Decisione di metodo**: non si scrive una spec di prodotto per il motore interno opaco. Confermato dalla spec attuale, che le elenca come "interamente non tracciate". Questo è il dato che **smonta l'analogia 1-Parte-1-sessione**: 3 delle 10 Parti non avrebbero MAI giustificato una sessione-spec.

### Dimensionamento d'insieme

| Blocco | Parti | Req. attesi (ordine di grandezza) | Fattibilità 1 sessione | Rischio dominante |
|---|---|---|---|---|
| S-A Contratto+consegna | I(1-2), II(6-9), VI(28-29) | ~30-35 | **borderline** (eventuale split A1/A2) | ampiezza → citazioni 100% pesanti |
| S-B Runtime+dato+compliance | IX, X, II(10) | ~20-25 | sì | **RM-2/RM-3 schema DAPI** + B-2 aperto |
| S-C Go-live+fasizzazione | I(5), VII, 8(42) | ~13-15 | sì (più sicura) | edge PENDING-empirico + B-1 aperto |
| (III/IV/V) | — | 0 | N/A | opache: nessuna spec |

Somma ordini di grandezza ≈ 63-75, coerente con i 75 requisiti attuali (le sovrapposizioni S-A/S-C su Cap.5 e su NFR-6.2 spiegano la forchetta). **Conferma**: 3 blocchi coprono lo stesso perimetro della singola SPEC-FUNZ-01 senza riscrivere nulla.

---

## 4. Confronto col documento metodologico — lezioni di METODO

Letto dalla history (`git log`, `reviews/`, indice) **per il metodo di costruzione, non per il merito** dei CAP (frozen).

### Come fu suddivisa la metodologia
10 Parti (Cap.1-65) + Appendici, una Parte ≈ una sessione Planner→Developer→Reviewer. Il taglio seguì la **struttura logica del motore** (ambito → contratto → quant → geometria → GA → emissione → validazione → dati → runtime → tape), non la densità di output.

### Lezioni estratte (con evidenza)

1. **Il primo giro di review quasi mai passa; il rework è la norma, non l'eccezione.** Conteggio file `reviews/`: CAP-05 ebbe 4 review (v1 CONDITIONAL→v2 PASS *invalidato da audit*→v3 CONDITIONAL→v4 PASS, indice:40), CAP-04 3 review (v1→v2→v3, BUG REALI ripetuti), CAP-06 v1 **FAIL**→v2 PASS (3 BUG REALI, commit `5b9bc8d`), CAP-09 v1 **FAIL**→v2 PASS (**7 BUG REALI**, commit `baeab2c`→`9bd35ba`). Solo CAP-10 passò sostanzialmente al primo colpo (v1 PASS→v2 cosmetica, indice:94). **Lezione**: dimensionare ogni blocco-spec assumendo ≥1 iterazione di rework piena; un blocco troppo largo moltiplica i finding del primo giro.

2. **I tagli più larghi/centrali generarono più rework.** Le Parti che concentravano molte decisioni interdipendenti (Parte V GA, Parte VII validazione, Parte IX runtime) ebbero i cicli più lunghi e i FAIL. Le Parti delimitate e di cornice (Parte X) ressero subito. **Lezione → dimensionamento**: il blocco **S-A** (contratto, ~30+ requisiti, analogo per densità a Parte II) è il candidato a rework; va trattato come borderline e valutato lo split.

3. **Gli schemi di sistemi esterni sono la fonte di errore più costosa.** L'unico BUG REALE "catastrofico" del progetto fu lo schema CANDLE invertito (`O;H;L;C` da wiki vs `C;L;H;O` reale del decoder), sfuggito a un intero ciclo Review v1→v2 perché gli AC verificavano *completezza* non *correttezza-vs-decoder* (indice:77, RACC-METODO-2). **Lezione → dimensionamento**: il blocco **S-B** (che tocca lo schema DAPI) richiede AC espliciti di diff col decoder canonico (RM-2) e va considerato a **rischio accuratezza alto** anche se piccolo per conteggio.

4. **La soglia che tenne l'accuratezza non è il numero di pagine ma il numero di citazioni da verificare al 100%.** Il Reviewer business-spec deve verificare ogni `[DOC-INTERNO CAP_XX:riga]`. SPEC-FUNZ-01 con 75 requisiti × ~1-2 citazioni = ~100-150 verifiche puntuali in una sola review: è il vero motivo del "troppo ampio" percepito. **Lezione → dimensionamento**: tarare i blocchi sul **numero di citazioni**, non di pagine. ~20-35 requisiti/blocco ≈ ~30-60 verifiche è una soglia di lavoro sostenibile in una review piena.

### Dove SEGUO il modello metodologico
- Ciclo Planner→Developer→Reviewer invariato (BASE_COMUNE §1), un blocco = una sessione = un PASS.
- Rework atteso ≥1 iterazione; doppio giro ostile del Reviewer.

### Dove me ne DISCOSTO (con motivazione)
- **Non replico "1 Parte metodologica = 1 sessione-spec".** Una spec di prodotto ≠ un capitolo metodologico: 3 Parti su 10 (III/IV/V) producono **zero requisiti** (§12:636) e non meritano una sessione-spec; viceversa la Parte II da sola vale ~30 requisiti e potrebbe valere 2 sessioni. **L'asse corretto per la business-spec è la densità-in-requisiti + la natura del consumatore, non la struttura del motore.** Questa è la divergenza chiave e la risposta diretta al dubbio di AC: la metodologia fu giustamente spezzata per Parte perché *ogni Parte è un blocco logico del motore*; la spec **no**, perché molti blocchi del motore sono muti per il prodotto.
- **Confine PHASE-2 come blocco-ponte (S-C), non disperso.** Nella metodologia la fasizzazione (Cap.42) vive dentro Parte 8 (dati). In una articolazione-spec conviene concentrare il confine PHASE-1/PHASE-2 + i gate go-live in un unico blocco-ponte verso FASE-D / SPEC-FUNZ-02.

---

## 5. Raccomandazione + punti per decisione AC

### Raccomandazione

1. **SPEC-FUNZ-01 v2 resta com'è** (PASS `ab7450f`). Nessuna ricostruzione, nessuno split retroattivo: la qualità è confermata e spezzare un PASS è churn a rischio regressione. Verdetto sostanziale = **(A) scope corretto**.
2. **La lezione organizzativa di AC è valida e va capitalizzata in avanti**: per il lavoro business-spec futuro, articolare per **densità + natura del consumatore** in ~3 blocchi (S-A contratto/consegna, S-B runtime/dato/compliance, S-C go-live/fasizzazione), **non** per Parte metodologica. Le Parti III/IV/V non generano spec.
3. **Se AC vuole un guadagno organizzativo su SPEC-FUNZ-01 senza riaprirla**: micro-pass cosmetico opzionale che raggruppa le 13 sezioni esistenti sotto 3 intestazioni macro-blocco (S-A/S-B/S-C), senza toccare requisiti né citazioni. **[DECISIONE AC]**.

### Punti che richiedono decisione AC (il repo non li disambigua)

- **[DECISIONE AC-1]** Verdetto operativo: accettare **(A) lasciare com'è** (raccomandato) — oppure procedere a una ri-articolazione in spec-blocco parallele sostitutive (sconsiglio: riapre un PASS).
- **[DECISIONE AC-2]** Se si articola in avanti: **taglio fine del blocco S-A** (monolitico ~30+ requisiti, *borderline* per una sessione, vs split S-A1 payload/state-machine + S-A2 emissione/consegna). Il repo non fissa una soglia numerica di requisiti/sessione: è una scelta di rischio.
- **[DECISIONE AC-3]** Soglia di lavoro "requisiti (o citazioni) per sessione-spec": propongo ~20-35 requisiti / ~30-60 citazioni come valore di lavoro (derivato dalla lezione 4), ma **non è un dato del repo** — va ratificato.
- **[DECISIONE AC-4]** Priorità del prossimo lavoro business-spec: i candidati in STATO_CORRENTE:24 (SPEC-FUNZ-02 PHASE-2 cross-index, FASE-D, Appendici operative) sono a discrezione del supervisore; questa analisi non la decide.
- **Dipendenze fragili da segnalare comunque** (non decisioni, avvisi): CAP-02 a `<sha-da-confermare>` (STATO_CORRENTE:8) tocca tutto il blocco S-A; B-1/M-2 (latenza) e B-2/M-GOV-1 (orario) APERTI toccano S-A/S-B/S-C; lo schema DAPI in S-B resta il punto a più alto rischio RM-2/RM-3 di tutto il perimetro.

---

*Documento di sola analisi. Nessuna spec scritta, nessun ACTIVE_TASK aperto, nessun CAP modificato (freeze G-09 rispettato). Prossimo passo = decisione AC.*
