# TASK ATTIVO: SPEC-FUNZ-01 — ricostruzione ex-novo (v2, modalità B)

**Assegnato da**: spec_planner (track Business-spec)
**Output atteso (lo scrive il Developer, NON il Planner)**: `docs/spec_funzionale/SPEC_FUNZ_01_v2.md` (file nuovo — il vecchio `SPEC_FUNZ_01.md` resta intatto, NON si tocca, NON si consulta)
**Report atteso (Developer)**: `reports/REPORT_SPEC_FUNZ_01_v2.md` con le 6 sezioni del formato supervisore (Cosa è stato prodotto / Ipotesi di partenza / Decisioni rilevanti / Misura prima/dopo / Domande aperte / Criterio di rollback) + tabella verifica AC.
**Stato**: IN ATTESA (pronto per spec_developer)
**Workflow**: Standard `spec_planner → spec_developer → spec_reviewer` (Developer v1 → Review v1 → eventuale classificazione finding al supervisore → fix → ... → PASS).
**Sede Reviewer**: **CLI** (GOV-SURFACES-01, METODO §Superfici). Audit documentale no-DAPI col divieto CLI (niente probe di zelo). Lista "Empirico-CLI da verificare" attesa **vuota** (il track non produce fatti empirici nuovi).
**Modalità di review**: **Review formale piena adattata al non-CAP** — il Reviewer applica i suoi giri ostili agli **AC di questo task card**, non agli AC dei CAP chiusi (i CAP sono frozen G-09 e fonte autoritativa, non oggetto di re-audit).

---

## Perché una RICOSTRUZIONE EX-NOVO (non una ri-validazione)

Questo task **ricostruisce da zero** SPEC-FUNZ-01. Il Developer scrive il documento **cieco** rispetto al vecchio.

- **Motivazione (AC)**: il vecchio `SPEC_FUNZ_01.md` è stato chiuso il **2026-06-03** (Re-Review v2 `a16a4c0`) sotto governance **pre-GOV-FIX**. Non ci si fida del **processo** con cui è stato prodotto, non necessariamente del **contenuto**. La ricostruzione produce un secondo testo indipendente sotto governance nuova; il confronto vecchio↔nuovo è materia del supervisore a valle, **non** del Developer.
- **Conseguenza vincolante sul Developer**: il vecchio `docs/spec_funzionale/SPEC_FUNZ_01.md` e il suo `reports/REPORT_SPEC_FUNZ_01.md` sono **NON consultabili** dal Developer durante la stesura. Il Developer deriva i requisiti **direttamente dai CAP chiusi PASS** elencati nella sezione "Capitoli-fonte" sotto, non da una copia del vecchio. Citare/parafrasare il vecchio è un BUG REALE di processo (il Reviewer lo segnala).
- **Cosa NON cambia**: lo **scope è invariato** rispetto al vecchio — Fase 1 della spec funzionale (requisiti R / NFR / CN sulla vista operatore/prodotto PHASE-1 FIB-only). **Niente ampliamento di scope.** Non è l'occasione per aggiungere requisiti PHASE-2, FASE-D o nuovi temi.

---

## Natura del track e perimetro non-CAP

SPEC-FUNZ-01 v2 **non è un capitolo metodologico** (non è CAP-XX né "Parte N" della metodologia v2). Non ridefinisce metodologia, non introduce nuovi parametri del GA, non modifica decisioni `D-*-N` chiuse, non riapre AC delle Review dei capitoli metodologici già PASS, non riapre il merito di alcun `Q-XX` chiuso.

È un **documento di requisiti funzionali / di prodotto / business**, in **vista operatore/prodotto**. Consolida la metodologia v2 (10 Parti, Cap.1-65, tutte PASS) in **requisiti funzionali (`R-N`)** + **non-funzionali/qualità (`NFR-N`)** + **vincoli normativi (`CN-N`)** + **matrice di tracciabilità requisito → capitolo metodologia v2**, e fa da **ponte fra il documento metodologico chiuso e la successiva FASE-D di implementazione**.

**Criterio di valore del track** (sostituisce la regola "orientamento al comportamento del GA", qui reinterpretata): ogni requisito di SPEC-FUNZ-01 v2 traccia **simultaneamente** a (a) un **valore operativo / di prodotto reale** per l'operatore retail FIB **E** (b) un **capitolo della metodologia v2** da cui deriva. Un requisito senza tracciabilità a metodologia O senza valore operativo dichiarato è un requisito sbagliato: il Reviewer lo segnala come BUG REALE.

---

## Obiettivo operativo della spec (vista prodotto)

Generare segnali long/short sul FIB (future mini FTSE MIB, IDEM, moltiplicatore 5 EUR/punto) per un operatore retail italiano che esegue **manualmente da cellulare**. Il sistema **NON esegue ordini**: pubblica segnali via Telegram, 1 contratto alla volta. Sessione operativa 08:00-22:00 CET. Commissioni 5 EUR/op. Broker Directa SIM DAPI. SPEC-FUNZ-01 v2 traduce questo obiettivo + le 10 Parti chiuse in requisiti verificabili e tracciati.

---

## Capitoli-fonte (perimetro di consolidamento)

Questo è il perimetro che rende il Developer capace di partire **cieco**: deriva i requisiti **solo** da questi capitoli (tutti chiusi PASS, frozen G-09), nei file `docs/methodology_v2/CAP_*.md` corrispondenti. Per ogni voce: cosa cercarvi. (Naming file confermato via Glob: `CAP_01_parte_I.md` … `CAP_10_parte_10.md`.)

| Parte (file) | Capitoli-fonte | Cosa il Developer cerca → tipo requisito |
|---|---|---|
| **Parte I** (`CAP_01_parte_I.md`) | Cap.1, 2, 3, 5 | Obiettivo operativo, vincolo "solo emissione" (→ R/CN), profilo operatore retail MiFID II + mobile + 1 contratto + commissioni 5€ (→ R/CN), infrastruttura/canale Telegram (→ R), definizione operativa del successo + filtro 80pt + metriche lifecycle/rischio/anti-overfitting (→ R/NFR). **Cap.4 (compute/cloud) → solo dipendenza infrastrutturale in Sez. dipendenze, NON requisito** (vedi Out-of-scope). |
| **Parte II** (`CAP_02_parte_II.md`) | Cap.6, 7, 8, 9, 11 | Schema/payload del segnale + invarianti immutabilità + segnale unico attivo + tick 5pt (→ R), state machine 1 non-terminale + 6 terminali + `trigger_event` (→ R/CN), condizioni di emissione (→ R), politica di pubblicazione Telegram + anti-duplicato + nuovo messaggio per nuovo `signal_id` (→ R/NFR latenza), position lifecycle out-of-scope dal motore — distinzione segnale/posizione (→ R). **Cap.10 (replay/determinismo) → dettaglio interno; citabile dove pertinente, non requisito a sé.** |
| **Parte III** (`CAP_03_parte_III.md`) | Cap.12-15 | **Nessun requisito diretto**: matematica interna (rendimenti, EGARCH, regime, feature/pivot) opaca al consumatore. Il Developer la dichiara esplicitamente non-tracciata nella sezione "capitoli non tracciati" con motivazione. |
| **Parte IV** (`CAP_04_parte_IV.md`) | Cap.16-21 | **Nessun requisito diretto** sulla derivazione (geometria zone, target/stop strutturali, survival, filtri, trade_range): è matematica interna; il prodotto pubblica il **risultato** (già coperto dal payload di Parte II). Il vincolo 80pt e il caso trade_range emergono come requisito **via Parte I/II**, non qui. Dichiarare non-tracciati con motivazione. |
| **Parte V** (`CAP_05_parte_V.md`) | Cap.22-26 | **Nessun requisito diretto**: motore GA interno (cromosoma, NSGA-II, fitness, walk-forward, popolazione) opaco al consumatore. I suoi **gate** emergono come NFR via Parte VII. Dichiarare non-tracciati con motivazione. |
| **Parte VI** (`CAP_06_parte_VI.md`) | Cap.28, 29 | Anti-doppio-segnale (→ R unico attivo), operatività mobile + formato messaggio Telegram mobile-readable + notifica trigger separata (→ R/NFR). **Cap.27 (inference) e Cap.30 (monitoraggio/dashboard) → interni/FASE-D; citabili per contrasto col gate bloccante, non requisito a sé.** |
| **Parte VII** (`CAP_07_parte_VII.md`) | Cap.31, 32, 33, 34, 36 | Latenza Telegram qualitativa (AC-GO-10, → NFR + M-2), DSR gate primario (→ NFR), PBO gate fragilità (→ NFR), bootstrap stazionario / lifecycle stabile cross-regime (→ NFR), **checklist go-live AC-GO-1..AC-GO-12** recepita come criteri di accettazione del prodotto. **Cap.35 (frozen bundle/hash) → meccanismo interno; citabile (AC-GO-12, M-16), non requisito a sé.** |
| **Parte 8** (`CAP_08_parte_8.md`) | Cap.42 (fasizzazione) | Confine PHASE-1 FIB-only vs PHASE-2 cross-index fuori scope (→ R fasizzazione). **Cap.37-44 (dati storici/back-adjustment/sanity) → materia di training; solo dipendenza infrastrutturale (Portara/CQG) in Sez. dipendenze, non requisito di prodotto.** |
| **Parte 9** (`CAP_09_parte_9.md`) | Cap.46, 47, 52, 53, 54, 56 | Canale DAPI esclusivo + porta 10002 trading mai aperta (→ CN/R dipendenza), catalogo simboli/rollover front-month + `CONTRACT_SWITCH` (→ R rollover, D-9-NB2), sessione 08:00-22:00 CET (→ R), gating qualitativo cash europei fuori dal GA (→ CN, Q-A-3/D-9-14), audit log + retention 90gg + permanente sui giorni di emissione (→ CN, D-9-15/Gap-4), marker normativi dei 6 terminali (→ CN, D-9-NB3), warm-up $L_{warmup}=30$gg (→ R, D-9-NB4, in Cap.51). **Cap.45, 50, 55 → premesse/recovery/punti aperti: dettagli interni, citabili dove pertinenti.** Minimizzazione PII/`chat_id`/account code (→ CN, Gap-1) da Cap.46. |
| **Parte 10** (`CAP_10_parte_10.md`) | Cap.59, 60, 61, 62, 65 | Backfill gap entro 100gg + fallback Portara oltre + re-warm-up (→ R), riconciliazione canonica giornaliera come **gate bloccante** distinto dal monitoraggio non-bloccante di Cap.30 (→ R, D-10-3/4), restart >100gg (→ R), tape archiviato runtime esteso 13 campi + manifest JSON + immutabilità append-only + "non fonte training" (→ R, D-10-8/9), invariante research=runtime esteso al ciclo di vita del tape (→ contesto). **Cap.57, 58, 63, 64 → premesse/tassonomia/coerenza inter-temporale/punti aperti: citabili dove pertinenti, non requisito a sé.** |

**Regola operativa per il Developer sul perimetro-fonte**: ogni requisito ha **almeno una** riga di tracciabilità verso uno o più capitoli di questa tabella, con riferimento puntuale `[DOC-INTERNO CAP_XX_parte_*.md:<riga>]`. La granularità (quanti requisiti per capitolo) è decisione del Developer purché atomica (N1) e tracciata; **non** è imposto un conteggio-target di requisiti (lo scope è "tutto e solo" il contenuto di prodotto dei capitoli-fonte sopra). Un capitolo della metodologia v2 che NON compare in matrice va elencato e **motivato** nella sezione "capitoli non tracciati" (Parte III, IV, V interamente; più i singoli capitoli interni indicati sopra).

---

## Dipendenze fragili (citazioni valide ma non pinnabili — freeze G-09)

`tasks/STATO_CORRENTE.md` riporta i marcatori di chiusura con SHA **`<sha-da-confermare>`** per:

- `CAP-01: CHIUSO PASS <sha-da-confermare>` → Parte I
- `CAP-02: CHIUSO PASS <sha-da-confermare>` → Parte II
- `CAP-03: CHIUSO PASS <sha-da-confermare>` → Parte III

**Dichiarazione di dipendenza vincolante**: i capitoli **Parte I, Parte II, Parte III** sono chiusi PASS ma il loro SHA-review non è ancora confermato/pinnabile. Poiché Parte I e Parte II sono **fonti pesanti** dei requisiti di prodotto (obiettivo operativo, vincolo "solo emissione", profilo operatore, payload del segnale, state machine, pubblicazione Telegram), molti requisiti R/NFR/CN dipenderanno da questi capitoli.

- Le citazioni `[DOC-INTERNO CAP_01_parte_I.md:…]` / `CAP_02_parte_II.md:…` / `CAP_03_parte_III.md:…` sono **valide** (i capitoli sono chiusi e congelati) ma **non ancora pinnabili a SHA**.
- Il Developer le **produce comunque** (sono la fonte legittima), citando file:riga, e segna la cautela: marca i requisiti la cui fonte primaria è uno di questi tre capitoli con il tag **`[B-N PROVVISORIO]`** soltanto se quella fonte è anche un **blocco aperto** (vedi AC sotto); la sola dipendenza dal capitolo a SHA-non-confermato si dichiara invece una volta in una nota di testa del documento ("citazioni verso CAP-01/02/03 valide, SHA non ancora pinnabile — freeze G-09"), senza appesantire ogni singolo requisito.
- **Nessuna ri-derivazione** di Parte I/II/III: sono frozen G-09. Il Developer le cita, non le riscrive né le corregge.

---

## Eredità obbligatoria (autoritativa — NON ri-verificare)

I dati seguenti sono **autoritativi** (input del Planner/Orchestratore, già verificati negli audit/CAP citati). Il Developer **non li ri-verifica**; li cita con la loro etichetta di livello-fonte.

1. **Stato metodologia**: 10 Parti, Cap.1-65, **tutte PASS** (vedi `docs/methodology_v2/00_indice.md`). `[DOC-INTERNO docs/methodology_v2/00_indice.md]`.
2. **Vincolo "solo emissione, nessuna esecuzione"**: strutturale non negoziabile. `[DOC-INTERNO CAP_01_parte_I.md]` (dichiarazione di intenti operatore).
3. **Sessione operativa**: negoziazione continua FIB **08:00-22:00 CET** (epoca E5), asta di apertura 07:45-08:00. `[DOC-INTERNO CAP_01_parte_I.md]`, `[DOC-INTERNO CAP_09_parte_9.md]` (Cap.52). Origine governance: **M-GOV-1** (`CARRYOVER.md`, decisione AC 13/06/2026 + `[WIKI-HINT Borsa Italiana, da verificare]`; upgrade a PROVA-EMPIRICA al primo probe V-1 — APERTO).
4. **Strumento**: FIB mini FTSE MIB, IDEM, moltiplicatore **5 EUR/punto**; operatore esegue su miniFIB (1 EUR/pt) mentre il motore calibra su FIB pieno. `[DOC-INTERNO CAP_01_parte_I.md]`, `[DOC-INTERNO CAP_09_parte_9.md]`.
5. **Tick discreto FIB = 5 pt**: prezzi e bande multipli di 5; $b_{min}=5$ è 1 tick. `[DOC-INTERNO CAP_02_parte_II.md]`. (Memoria progetto: FIB tick 5pt.)
6. **Filtro minimo 80 pt** (directional e $A_{range}$ trade_range): gate di emissione, non parametro libero del GA. `[DOC-INTERNO CAP_01_parte_I.md]` (Cap.5), `[DOC-INTERNO CAP_02_parte_II.md]` (Cap.8).
7. **Commissioni**: 5 EUR/op (≈2 pt FIB per ciclo apertura-chiusura) nel calcolo del rendimento netto. `[DOC-INTERNO CAP_01_parte_I.md]`.
8. **Sizing**: 1 contratto FIB alla volta; segnale unico attivo $|\mathcal{A}(t)|\le 1$. `[DOC-INTERNO CAP_01_parte_I.md]`, `[DOC-INTERNO CAP_02_parte_II.md]`.
9. **State machine del segnale**: 1 stato non-terminale (`active`) + 6 terminali (`target_1_hit`, `stopped`, `invalidated`, `missed_target`, `expired`, `revoked`); `trigger_event` è evento, non stato. `[DOC-INTERNO CAP_02_parte_II.md]` (Cap.7). Marker normativi `SIGNAL_*` a 6 terminali: `[DOC-INTERNO CAP_09_parte_9.md]` (D-9-NB3).
10. **Latenza Telegram**: NFR $L\le L_{max}$, $L_{max}=30$ s (valore di lavoro provvisorio). Verifica empirica **OPEN** → **M-2** (`CARRYOVER.md`), Appendice E / FASE-D. `[DOC-INTERNO CAP_02_parte_II.md]` (Cap.9.3), `[DOC-INTERNO CAP_07_parte_VII.md]` (AC-GO-10).
11. **Rollover / contract switch**: al boot del giorno di scadenza (terza venerdì) sottoscrizione diretta del next-month, marker `CONTRACT_SWITCH`. Codici mese Directa-IDEM verificati: `F`=giugno, `I`=settembre (NON-standard, RM-3, niente inferenza per analogia su Mar/Dic). `[DOC-INTERNO CAP_09_parte_9.md]` (D-9-NB2), M-4 (`STATO_CORRENTE.md`, `[PROVA-EMPIRICA 2026-06-01]`).
12. **Canale DAPI**: porte 10001 (realtime) / 10003 (storico); **porta 10002 (trading) mai aperta**; uso esclusivo del canale (D-6). `[DOC-INTERNO CAP_09_parte_9.md]`.
13. **Schemi DAPI** (per le sezioni dato): CANDLE reale `C;L;H;O;V` (`[CODICE-ESISTENTE scripts/export_directa_history_parametric.py:477-481]`); PRICE realtime (M-9) e BOOK_5 (M-10) come da `STATO_CORRENTE.md` — chiusi negli audit RM CAP-DATA-02/03. La **wiki Directa è dimostrata inesatta** sullo schema CANDLE (`O;H;L;C`): mai fonte unica, sempre `[WIKI-HINT, da verificare]`.
14. **Retention audit log**: JSON Lines append-only, retention minima 90 giorni rolling + permanente sui giorni di emissione. `[DOC-INTERNO CAP_09_parte_9.md]` (D-9-15/Gap-4).
15. **Warm-up**: $L_{warmup}=30$ giorni di trading IDEM congelato. `[DOC-INTERNO CAP_09_parte_9.md]` (D-9-NB4), `[DOC-INTERNO CAP_10_parte_10.md]` (Cap.61).
16. **Tape archiviato**: header runtime esteso **13 campi** distinto dal legacy **11 campi** (`[CODICE-ESISTENTE scripts/export_directa_history_parametric.py:605-617]`); limite DAPI intraday ~100gg (`[CODICE-ESISTENTE scripts/export_directa_history_parametric.py:61]` `DEFAULT_INTRADAY_MAX_DAYS=100`). `[DOC-INTERNO CAP_10_parte_10.md]`.
17. **PHASE-2 cross-index** (DAX/EuroStoxx50/ES/MES): **fuori scope**, fasizzazione già decisa. `[DOC-INTERNO CAP_08_parte_8.md]` (Cap.42), `[DOC-INTERNO CAP_09_parte_9.md]` (Cap.55), `[DOC-INTERNO CAP_10_parte_10.md]`.

**Censimento M-promemoria aperti** (`CARRYOVER.md`): l'unico M-promemoria **di capitolo OPEN** pertinente è **M-2** (latenza Telegram $L_{max}=30$s) — va **incardinato come NFR** nel documento, con la verifica empirica dichiarata OPEN (Appendice E / FASE-D), **non risolta** dalla spec. **M-GOV-1** (orario FIB) è APERTO nel namespace governance: la spec recepisce l'orario come requisito (R) citando M-GOV-1 e l'upgrade empirico pendente. Tutti gli altri M (M-4…M-16, M-9, M-10) sono CLOSED o note tecniche già incorporate: citabili come fonte, nessuno da incardinare. Nessun M perso.

> **Input dell'Orchestratore = autoritativo**: i dati 1-17 sopra e gli M citati sono autoritativi; il Developer NON li ri-verifica né ri-fetcha. "Autoritativo" non promuove il livello-fonte: nessuna conclusione strutturale può poggiare solo su un `[WIKI-HINT]`.

---

## Acceptance criteria (governance nuova)

### AC globali (G)

- **AC-G1 (atomicità N1)**: ogni requisito = **una** proposizione verificabile. Un requisito che impacchetta più concern va spezzato in più ID. Il Reviewer segnala come BUG REALE ogni requisito multi-concern.
- **AC-G2 (tracciabilità obbligatoria)**: ogni requisito traccia ad **almeno un** capitolo metodologia v2 con riferimento puntuale `[DOC-INTERNO CAP_XX_parte_*.md:<riga>]`. Requisito senza tracciabilità = BUG REALE.
- **AC-G3 (valore operativo obbligatorio)**: ogni requisito dichiara il proprio **valore operativo / di prodotto** per l'operatore retail FIB. Requisito senza valore operativo dichiarato = BUG REALE.
- **AC-G4 (floor citazioni 100% in review)**: il **100%** delle citazioni `[DOC-INTERNO …]` / `[CODICE-ESISTENTE …]` del documento è verificabile token-per-token contro la fonte. Il Reviewer le campiona/verifica; una citazione che non risolve = BUG REALE.
- **AC-G5 (divieto "verificato X" di prima istanza, RM-1)**: la spec **non introduce** nuove dichiarazioni "verificato X" su sistemi esterni. Ogni asserzione fattuale è un **richiamo etichettato** a un CAP chiuso (`[DOC-INTERNO …]`), a codice (`[CODICE-ESISTENTE …]`, **grafia canonica**), o a una prova già chiusa (`[PROVA-EMPIRICA <data>]`). Nessun blocco 4-righe `VERIFICA/PROVE/ALTERNATIVE` nuovo è dovuto (non si eseguono verifiche nuove); se ne comparisse uno, segnala incoerenza.
- **AC-G6 (etichette RM-3)**: ogni riferimento a documentazione esterna (MiFID II, wiki Directa, Telegram, Portara/CQG, CME/Eurex) è etichettato `[WIKI-HINT, da verificare]` e **mai** fonte unica di un'asserzione strutturale. La wiki Directa è citata solo con l'avvertenza esplicita di inaffidabilità sullo schema CANDLE.
- **AC-G7 (grafia etichette canonica)**: usare **`[CODICE-ESISTENTE …]`** (grafia canonica, METODO §RM-3). La grafia storica `[CODICE-EXISTENTE …]` è **vietata** nei nuovi documenti.
- **AC-G8 (marcatura `[B-N PROVVISORIO]`)**: ogni requisito la cui fonte primaria è un **blocco aperto** (M-2 latenza non verificata empiricamente; M-GOV-1 orario in attesa di upgrade PROVA-EMPIRICA; ogni dipendenza dichiarata aperta) porta il tag **`[B-N PROVVISORIO]`** con riga di spiegazione. Il blocco è aperto, il requisito resta dichiarato ma esplicitamente provvisorio.
- **AC-G9 (cecità rispetto al vecchio)**: il documento **non** cita, parafrasa o riusa `docs/spec_funzionale/SPEC_FUNZ_01.md` né il suo report. Nessun riferimento al vecchio testo. (Il Reviewer verifica l'assenza di tracce — es. ID requisito copiati 1:1 senza derivazione propria, frasi identiche — e segnala come BUG REALE di processo.)
- **AC-G10 (scope invariato, no ampliamento)**: il documento copre **Fase 1 = vista operatore/prodotto PHASE-1 FIB-only** e **nient'altro**. Niente requisiti PHASE-2, niente specifica di implementazione FASE-D, niente nuovi temi. Ampliamento di scope = BUG REALE.
- **AC-G11 (matrice di tracciabilità finale)**: il documento si chiude con una **sezione matrice di tracciabilità** requisito → capitolo metodologia v2 (una riga per requisito) + una **sezione "capitoli non tracciati"** che elenca e **motiva** ogni capitolo della metodologia v2 (in particolare Parti III, IV, V e i singoli capitoli interni indicati nella tabella capitoli-fonte) non mappato a un requisito.
- **AC-G12 (M-2 incardinato)**: M-2 è incardinato come **NFR** con la verifica empirica dichiarata OPEN (Appendice E / FASE-D) e tag `[B-N PROVVISORIO]`. M-GOV-1 (orario) recepito come R con citazione del pendente upgrade empirico.

### AC per sezione (atomicità del testo)

- **AC-S1**: ogni sezione del documento chiude con (a) una **lista out-of-scope** con destinazione esplicita per voce e (b) una **mini-tabella requisito→capitolo→tipo** dei requisiti introdotti nella sezione.
- **AC-S2**: gli schemi-dato di sistemi esterni citati (CANDLE/PRICE/BOOK_5, header CSV) riportano il **diff col decoder canonico** `scripts/export_directa_history_parametric.py` (RACC-METODO-2 / RM-2): la citazione di schema poggia sul decoder di produzione, non sul wiki.

---

## Out-of-scope esplicito (con destinazione)

| Voce fuori scope | Destinazione |
|---|---|
| Matematica del modello (rendimenti, EGARCH, regime, feature/pivot, geometria zone, derivazione target/stop, survival, fitness, GA, walk-forward) | **CAP chiusi** (Parti III/IV/V) — **NON ri-derivare**: citare il risultato dove esce in vista prodotto, dichiarare i capitoli interni come non tracciati e motivati |
| Implementazione (codice runtime, adapter, parser DAPI, microservizi, framework, CI/CD, stringhe esatte del bot, gestione `chat_id`, calibrazione fine $\theta_{reconcile}$) | **FASE-D** |
| Ampliamenti di scope (PHASE-2 cross-index DAX/EuroStoxx50/ES/MES; nuovi temi non presenti nelle 10 Parti) | **spec futura** (SPEC-FUNZ-02 o equivalente) — fuori scope qui |
| Vecchio `docs/spec_funzionale/SPEC_FUNZ_01.md` e suo report | **NON consultabile** dal Developer (ricostruzione cieca); confronto vecchio↔nuovo è materia del supervisore a valle |
| Verifica empirica di $L_{max}=30$s (M-2) e upgrade orario M-GOV-1 a PROVA-EMPIRICA | **Appendice E / FASE-D / probe V-1** — requisito dichiarato, non verificato qui |
| Parere legale formale, testo dei disclaimer MiFID II | consulente legale esterno (FASE-D/business) |
| Compute/TCO/instance AWS, contratti vendor | Cap.4 Parte I / FASE-D — citati come dipendenza, non ridiscussi |
| `00_indice.md` | **NON si tocca** (SPEC-FUNZ-01 non è una Parte della metodologia v2) |

---

## Done-when (domande operative a cui la spec v2 deve rispondere univocamente)

1. **Cosa pubblica** il prodotto e con quale **payload** (campi, domini, vincoli, invarianti)?
2. **A chi** è destinato (persona operatore retail MiFID II, mobile, 1 contratto) e **come** lo consuma?
3. **Quando** un segnale è eseguibile, e quali sono i **6 esiti terminali** dal punto di vista dell'operatore?
4. **Dove e come** il segnale è consegnato (Telegram, contenuti minimi, anti-duplicato, latenza-requisito) e quali requisiti di consegna valgono?
5. **Quali vincoli operativi e di sessione** (orario 08:00-22:00 CET, sizing 1 contratto, segnale unico, commissioni, rollover/`CONTRACT_SWITCH`) governano il prodotto?
6. **Con quali criteri di accettazione di prodotto** (KPI lifecycle, gate anti-overfitting DSR/PBO, checklist go-live AC-GO-1..12) si dichiara il prodotto pronto?
7. **Quali vincoli normativi/compliance** (solo emissione, separazione segnale/esecuzione, audit/retention, PII minima, gating qualitativo cash) si applicano?
8. **Quali dipendenze di dato e infrastruttura** (DAPI, Portara/CQG, cloud, Telegram, cash europei gating) e quali requisiti di dato (tape esteso, immutabilità, backfill 100gg, riconciliazione bloccante, warm-up)?
9. **Come è fasizzato** (PHASE-1 FIB-only in scope; PHASE-2 fuori) e **quali dipendenze restano aperte verso FASE-D**?
10. **Quale tracciabilità** lega ciascun requisito al/ai capitolo/i metodologia v2, e **quali capitoli non sono tracciati e perché**?

---

## Pipeline attesa (per l'Orchestratore)

1. **spec_developer** (via general-purpose che adotta `.claude/agents/spec_developer.md`): legge `tasks/METODO.md` + `.claude/BASE_COMUNE.md` + il proprio ruolo + questo task card, deriva i requisiti **dai capitoli-fonte** (cieco rispetto al vecchio), scrive `docs/spec_funzionale/SPEC_FUNZ_01_v2.md` + `reports/REPORT_SPEC_FUNZ_01_v2.md`, esegue la pre-consegna, scrive `READY_FOR_REVIEW` in `DEV_STATUS.md`, si ferma. Non committa il task card (lo committa l'Orchestratore).
2. **Orchestratore**: check post-Developer (6 controlli, condizione-3 indice = **N/A**; "commit copre i file attesi" = `SPEC_FUNZ_01_v2.md` + `REPORT_SPEC_FUNZ_01_v2.md` + `DEV_STATUS.md`).
3. **spec_reviewer** (via general-purpose, **sede CLI**): audit ostile doppio giro sugli AC di questo task card; verdetto PASS/CONDITIONAL/FAIL; lista "Empirico-CLI da verificare" attesa **vuota**.
4. Su CONDITIONAL/FAIL → punto di controllo supervisore. Su PASS → chiusura B (7 condizioni adattate; indice = N/A; marcatore `SPEC-FUNZ-01-v2: CHIUSO PASS <sha-review>` in `STATO_CORRENTE.md`, **distinto** dal marcatore storico `SPEC-FUNZ-01: CHIUSO PASS a16a4c0` del vecchio, che resta).

---

*Task card SPEC-FUNZ-01 v2 (ricostruzione ex-novo, modalità B) — scritto da spec_planner. Il Developer parte cieco dai capitoli-fonte; il vecchio `SPEC_FUNZ_01.md` resta intatto e non consultabile.*
