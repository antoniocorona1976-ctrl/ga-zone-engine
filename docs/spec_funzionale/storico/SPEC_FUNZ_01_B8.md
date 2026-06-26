# SPEC-FUNZ-01 — Blocco B8: Confine / chiusura della spec (fasizzazione PHASE-1/PHASE-2 e dipendenze aperte verso FASE-D)

> **Track**: Business-spec (SPEC-FUNZ). **Blocco**: B8 (8/8 — **ULTIMO** della ricostruzione cieca a 8 blocchi). **Sede**: CLI. **Tag commit**: `[SPEC-FUNZ-01-B8]`.
>
> **Natura del blocco — CONFINE / CHIUSURA, non materia-prodotto nuova.** Questo blocco consolida due cose e **solo** due cose: (a) la **fasizzazione dichiarata** del prodotto — PHASE-1 FIB-only in scope, PHASE-2 cross-index dichiarazione normativa senza implementazione; (b) l'**enumerazione delle dipendenze aperte verso FASE-D**, dichiarate aperte, **mai risolte**. B8 **non apre** materia nuova del motore, **non ri-deriva** i blocchi precedenti, **non risolve** alcuna dipendenza aperta.

---

## 0. Intestazione, scopo, schema-ID

### 0.1 Scopo

Tradurre in requisiti di prodotto il **confine** della specifica funzionale del motore di segnali FIB: cosa il prodotto **dichiara come in vigore ora** (PHASE-1 FIB-only), cosa **dichiara come previsto ma non implementato** (PHASE-2 cross-index), e quali **dipendenze restano aperte** e dove sono rinviate (FASE-D / monitoring post-go-live / Appendice E / ruolo `validator`). Il valore di prodotto del blocco è rendere **esplicito e tracciabile** il perimetro di ciò che il prodotto chiude e di ciò che lascia aperto, perché un esterno (o l'operatore retail FIB) non sia indotto ad aspettarsi funzioni che il prodotto non eroga in PHASE-1, e perché chi avvia FASE-D abbia l'elenco completo di ciò che va risolto prima/durante l'implementazione.

### 0.2 Schema-ID (assegnati da zero, atomicità N1)

- `B8-R-NN` — requisito funzionale/di confine di prodotto.
- `B8-CN-NN` — vincolo/confine normativo (constraint) di prodotto.
- `B8-NFR-NN` — requisito non funzionale (questo blocco non ne produce di propri: vedi §4 nota).

Ogni requisito esprime **una sola proposizione verificabile** (N1). Ogni requisito cita la **riga reale** del capitolo-fonte, riletta token-per-token a HEAD `3136a55`.

### 0.3 Conferma di cecità (modalità B)

I requisiti `B8-*` sono derivati **dai soli** capitoli del perimetro-fonte primario (`CAP_08_parte_8.md` Cap.42, `CAP_09_parte_9.md` Cap.55, `CAP_10_parte_10.md` Cap.64) più le premesse citate per riga (`CAP_07_parte_VII.md` Cap.36.3, `CAP_09_parte_9.md` Cap.53, `CAP_08_parte_8.md` Cap.41). Gli ID sono **auto-assegnati da zero**. Questo blocco è stato prodotto **cieco** rispetto a: `SPEC_FUNZ_01.md` (v2) e ogni `*_v1_storico*`; i file di chunking `PROPOSTA_SUDDIVISIONE_SPEC*.md`; i documenti dei blocchi precedenti `SPEC_FUNZ_01_B1.md` .. `SPEC_FUNZ_01_B7.md`. Nessun ID-requisito importato, nessun conteggio-target, nessuna partizione da v2/chunking.

### 0.4 Nota "blocco di chiusura" (in evidenza)

> **B8 è un blocco di confine. Tre cose che NON sono requisiti di B8 (anti meta-processo, AC-B8-NOASSEMBLY):**
> 1. **Assemblaggio della serie B1..B8 in un unico documento** — è un **task separato post-B8**, non materia-prodotto.
> 2. **Indicizzazione / cross-reference dei blocchi B1..B7** — task separato / parte dell'assemblaggio, non requisito B8.
> 3. **Avvio di FASE-D / specifica di implementazione FASE-D** — è la **fase successiva**, non un requisito B8.
>
> Ogni requisito di questo blocco è una **dichiarazione di confine / fasizzazione / dipendenza-aperta**: mai apertura di materia-prodotto nuova del motore, mai risoluzione di una dipendenza aperta (AC-B8-CONFINE). I `[PROVA-EMPIRICA]` interni ai capitoli (es. abilitazione FDAX) si **riportano come già dichiarati dal capitolo frozen**, non si ri-asseriscono.

### 0.5 Gerarchia delle fonti (RM-3)

L'ordine di priorità delle fonti è quello di `tasks/METODO.md` RM-3: (1) prove empiriche dirette, (2) codice di produzione esistente nel repo, (3) documenti operativi interni committati, (4) documentazione esterna (solo hint). Tutte le asserzioni di questo blocco sono **richiami** a capitoli metodologia v2 chiusi PASS (`[DOC-INTERNO ...]`), livello 3. Nessuna conclusione poggia su livello 4. Nessun blocco `VERIFICA/PROVE/...` di prima istanza è introdotto (AC-G4): B8 non verifica nulla ex novo, consolida confini già fissati nei capitoli frozen.

---

## 1. Fasizzazione PHASE-1 / PHASE-2 (Cap.42)

Questa sezione consolida la **fasizzazione del prodotto** come confine: cosa è in vigore in PHASE-1 e cosa è dichiarato-ma-non-implementato in PHASE-2. Fonte primaria: `CAP_08_parte_8.md` Cap.42.

### B8-R-01 — La PHASE-1 del prodotto è FIB-only, single-instrument

Il prodotto **dichiara** che la PHASE-1 (fase corrente in vigore) è **FIB-only, single-instrument**: la specifica del motore è istanziata esclusivamente sul FIB, senza il layer di covarianza cross-index `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:167]`. La fasizzazione PHASE-1 è **esplicita e dichiarata, non una semplificazione silenziosa** `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:143]`; il documento metodologico v2 è esplicitamente single-instrument FIB, con il preambolo che dichiara la "rimozione dei layer multi-indice (DCC/ADCC/BEKK, covarianza cross-index, N>=8)" `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:145]`.

- **Valore operativo**: l'operatore retail FIB sa che il prodotto in PHASE-1 produce segnali sul **solo FIB**; non deve aspettarsi segnali o copertura cross-index, che non esistono nella fase corrente. Rende esplicito il perimetro-strumento del prodotto erogato.

### B8-R-02 — La convenzione cross-index PHASE-2 è dichiarazione normativa senza implementazione

Il prodotto **dichiara** la convenzione cross-index per gli strumenti correlati al FIB come **dichiarazione normativa PHASE-2 senza implementazione** nel doc v2 corrente; la sua attivazione operativa è **rinviata a un futuro ciclo di estensione**, fuori scope dal corpo del documento corrente `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:143]`. Il layer di covarianza cross-index **non esiste** nel doc v2 corrente: nessun riferimento implementativo è fatto per quel layer `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:145]`.

- **Valore di sistema**: il confine è chiarito — la convenzione cross-index esiste come **norma scritta**, non come funzione erogata. Chi legge la spec non confonde "dichiarato" con "implementato".

### B8-CN-01 — Gli strumenti cross-index PHASE-2 sono previsti come dichiarazione, non erogati

Il prodotto **dichiara** che gli strumenti previsti per la PHASE-2 sono **DAX** (futures FDAX su Eurex), **EuroStoxx 50** (futures FESX su Eurex) e **S&P 500 mini** (futures ES su CME) `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:147]` (`:149-:151`). Questi strumenti entrano nella specifica **solo come previsione normativa di PHASE-2**: non sono erogati né implementati in PHASE-1 (vincolo di fasizzazione di B8-R-01/B8-R-02).

- **Valore di sistema**: enumera con precisione **quali** strumenti la PHASE-2 prevederebbe, senza promettere che il prodotto corrente li tratti. Confine esatto del catalogo-strumenti dichiarato.

### B8-CN-02 — Le estensioni metodologiche cross-index sono dichiarate esplicitamente non implementate

Il prodotto **dichiara** come **non implementate** nel doc v2 corrente tre classi di estensione cross-index: i **modelli di covarianza condizionata cross-index** (DCC, ADCC, cDCC); il **Realized GARCH**; lo **score `S_xidx` e la quinta famiglia del catalogo target ("proiezioni cross-index coerenti")** `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:176]` (`:178-:180`). Nessuno di questi tre elementi entra come parte dell'impegno corrente del documento metodologico v2 `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:182]`.

- **Valore di sistema**: fissa il **confine metodologico** della PHASE-1 — quali tecniche restano fuori dalla fase corrente — evitando che la loro citazione nel capitolo sia letta come impegno implementativo.

### B8-CN-03 — La fasizzazione PHASE-1 ha costi noti rispetto alla specifica ideale, dichiarati come tali

Il prodotto **dichiara** che la fasizzazione PHASE-1 **non sostituisce la specifica ideale, la istanzia in modo parziale con costi noti** `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:174]`. I costi dichiarati della PHASE-1 sono: la varianza sistemica cross-index $\sigma_{sys}$ è **ridotta a** $\sigma_{local}$ (varianza condizionata locale del FIB da EGARCH(1,1)), degradazione metodologica dichiarata `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:169]`; il feature tensor è **privo dei canali cross-index** della specifica ideale (catalogo 37 feature calibrato single-instrument FIB) `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:170]`; lo score $S_{xidx}$ **non è calcolabile** in PHASE-1 e la quinta famiglia del catalogo target è esclusa `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:171]`; il report per regime di volatilità è **privo della riga "Contagio cross-index"** `[DOC-INTERNO docs/methodology_v2/CAP_08_parte_8.md:172]`.

- **Valore di sistema**: rende esplicito **a quale prezzo metodologico** il prodotto eroga la PHASE-1, così che il costo non sia scoperto a posteriori e sia un input consapevole per la valutazione PHASE-2.

### B8-CN-04 — I cash europei sono canali di contesto live, NON cross-index PHASE-2 (confine fine)

Il prodotto **dichiara** il confine fine tra cash europei e cross-index PHASE-2: i cash europei **DGER, DSTX50, DITAS, DFRA non sono "cross-index PHASE-2"** — sono **canali di contesto live** (logging + gating qualitativo), accessibili gratuitamente sul DAPI base, distinti dai futures cross-index `[DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:338]` (premessa Cap.53, citata per riga). Quando PHASE-2 sarà attivata, i **futures** cross-index (FDAX, FESX, ES) entreranno nel layer di covarianza, mentre i cash europei resteranno gating qualitativo `[DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:338]`.

- **Valore di sistema**: previene la confusione fra due materie distinte (cash di contesto, già in PHASE-1 come gating qualitativo — perimetro B5; futures cross-index, in PHASE-2). Il requisito consolida **solo il confine**; il gating runtime/`gating_rules.yaml` è perimetro B5, non ri-derivato qui.

### B8-CN-05 — La materia tape/storicizzazione (Parte 10) non si applica ai cross-index PHASE-2

Il prodotto **dichiara** che la convenzione tape/storicizzazione runtime (Parte 10) **NON si applica ai cross-index PHASE-2**: la convenzione cross-index Parte 8 Cap.42 è **invariata**, e la Parte 10 resta dentro il confine PHASE-1 (fuori scope i cross-index) `[DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:236]`.

- **Valore di sistema**: chiude il confine PHASE-1 anche sul versante della pipeline tape/archiviazione, coerente con B8-R-01/B8-R-02: nessuna parte del prodotto corrente (incluso il ciclo di vita del tape) tratta i cross-index.

---

## 2. Dipendenze aperte verso FASE-D (Cap.55 + Cap.64, premessa Cap.36.3)

Questa sezione enumera le **dipendenze dichiarate aperte** dai capitoli di confine (Cap.55, Cap.64) e dalla premessa Cap.36.3, ciascuna col suo **stato esatto di apertura e destinazione**. Le dipendenze sono **dichiarate aperte, MAI risolte** (AC-B8-DEPS): B8 consolida l'esistenza, lo stato e la destinazione della dipendenza — fatti del capitolo — non il merito (non calibra, non misura, non sceglie). L'esito/valore di ciascuna è **PENDING-empirico** (§3).

### B8-R-03 — La latenza Telegram L_max=30s resta dipendenza aperta (M-2 OPEN)

Il prodotto **dichiara** la verifica empirica della latenza del canale Telegram ($L_{max}=30$s) come **dipendenza aperta** (M-promemoria M-2, `OPEN`), carryover ad **Appendice E** del documento; non si chiude nei capitoli di confine perché tratta il canale di pubblicazione Telegram, fuori perimetro DAPI `[DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:402]`. Lo stesso stato è ribadito sul versante tape: Telegram $L_{max}=30$s (M-2 OPEN), Appendice E, fuori perimetro DAPI `[DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:237]`.

- **Stato esatto**: **aperta**, rinviata ad **Appendice E** (sessione futura). La **misura empirica** del valore è PENDING-empirico (§3), mai asserita.
- **Valore di sistema**: rende esplicito che il vincolo di latenza del canale di consegna esiste come dichiarazione, ma il suo valore numerico non è ancora verificato — da chiudere prima/durante FASE-D.

### B8-R-04 — La calibrazione fine di θ_reconcile resta dipendenza aperta (parametro provvisorio non congelato)

Il prodotto **dichiara** la soglia $\theta_{reconcile}$ (numero massimo di minuti divergenti oltre tolleranza tollerati prima di `RECONCILE_DIVERGENT_FIB`) come **parametro provvisorio non congelato**, la cui calibrazione fine è **rinviata a FASE-D** su dati operativi reali (o a un futuro CAP-DATA-04 / monitoring post-go-live); nessun valore numerico è inventato `[DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:131]`. La voce è ribadita come fuori scope di Parte 10, con carryover a CAP-DATA-04 / monitoring post-go-live `[DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:232]`.

- **Stato esatto**: **provvisoria, non congelata**, rinviata a **FASE-D / CAP-DATA-04 / monitoring post-go-live**. La calibrazione è PENDING-empirico (§3); B8 non assegna alcun valore.
- **Valore di sistema**: rende esplicito che il gate di riconciliazione end-of-day dipende da un parametro non ancora fissato, da calibrare su dati reali — input per FASE-D.

### B8-R-05 — Il congelamento empirico dei 10 parametri di tuning resta dipendenza aperta (carryover post-go-live)

Il prodotto **dichiara** i 10 parametri di tuning operativo di Parte VI ($T_{recal,EGARCH}, \theta_B, T_{B,persist}, W_B, W_{prod}, T_{drift,persist}, T_{emit,persist}, \epsilon_p, N_{reg,\min}^{live}, \alpha_{f_5}$) come **starting point con i default proposti** per il primo run di produzione, **senza congelamento empirico** `[DOC-INTERNO docs/methodology_v2/CAP_07_parte_VII.md:637]` (premessa Cap.36.3, citata per riga). La riconsiderazione empirica è attività di **monitoring post-go-live a 3-6 mesi** di produzione live, dichiarata come carryover esplicito e **non** task corrente `[DOC-INTERNO docs/methodology_v2/CAP_07_parte_VII.md:641]`.

- **Stato esatto**: **aperta** (parametri non congelati empiricamente), rinviata al **monitoring post-go-live (3-6 mesi)**. Il congelamento è PENDING-empirico (§3).
- **Valore di sistema**: rende esplicito che i parametri operativi del prodotto sono default provvisori da raffinare in produzione, non valori finali — premessa B7-owned (Cap.36), qui citata solo come dipendenza aperta, non ri-derivata.

### B8-R-06 — Il run del validator sull'edge resta dipendenza aperta (PENDING-empirico, esclusiva validator/FASE-D)

Il prodotto **dichiara** che l'esito d'edge (es. DSR/PBO/OOS e valori d'esito) è materia del **ruolo `validator`** in FASE-D e resta **dipendenza aperta**: i parametri di tuning provvisori (es. $\theta_{DSR}, \theta_{PBO}$) sono trattati come provvisori non congelati `[DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:131]`, analogamente a $\theta_{reconcile}$ e $L_{max}$ Telegram. B8 **cita** l'edge come dipendenza aperta e **non asserisce alcun esito** (eredità del cardine B7).

- **Stato esatto**: **aperta**, PENDING-empirico, esclusiva del ruolo `validator` (FASE-D). Nessun valore d'edge è asserito (§3).
- **Valore di sistema**: rende esplicito che il prodotto **non dichiara** un edge misurato; l'esistenza/misura dell'edge è rinviata al validator, da risolvere in FASE-D prima del go-live.

### B8-R-07 — La lookup completa dei codici mese Directa-IDEM resta dipendenza aperta (runtime-discovery / FASE-D)

Il prodotto **dichiara** che la lookup completa dei codici mese Directa-IDEM è una **dipendenza aperta**: nel doc v2 corrente sono congelati solo i due codici verificati (`F = giugno`, `I = settembre`), mentre gli altri restano **lookup runtime-discovery**, da derivare via comando `ANAG` sul gateway per ciascun ticker candidato, con tabella arricchita progressivamente nel **ciclo operativo (FASE-D)** `[DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:389]`.

- **Stato esatto**: **aperta** (solo 2 codici congelati), rinviata a **runtime-discovery / FASE-D**. La decodifica dei codici mancanti è PENDING-empirico (§3).
- **Valore di sistema**: rende esplicito che il catalogo dei codici mese non è completo e va completato a mercato aperto — input operativo per FASE-D.

### B8-R-08 — L'abilitazione FDAX standard resta dipendenza aperta (PHASE-2, fuori scope corrente)

Il prodotto **dichiara** l'abilitazione FDAX standard (DAX Future Eurex, 25 EUR/pt) come **dipendenza aperta fuori scope** per il vincolo D-1 (niente market data a pagamento sui cross-index futures): la verifica empirica 2026-05-27 ha rilevato che l'account `B6086` **non è abilitato** al ticker `FDAX` standard (tutte le varianti hanno restituito `ERR;<sym>;1007`), mentre sono abilitati i ticker Mini-DAX e Micro-DAX; l'abilitazione FDAX standard sarebbe parte della valutazione solo **se in PHASE-2** si decidesse di attivare i futures cross-index `[DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:387]`.

- **Stato esatto**: **aperta**, rinviata alla valutazione **PHASE-2** (non decisa nel doc corrente). Il dato 2026-05-27 è riportato come **già dichiarato dal capitolo frozen** (PROVA-EMPIRICA del capitolo), non ri-verificato.
- **Valore di sistema**: rende esplicito che un eventuale futuro uso del DAX richiederebbe un'abilitazione che il prodotto corrente non possiede — confine commerciale di PHASE-2.

### B8-R-09 — La scelta del vendor cross-index pluriennale resta dipendenza aperta (training PHASE-2)

Il prodotto **dichiara** la scelta di un **vendor cross-index pluriennale** (necessario per il training cross-index PHASE-2, perché il limite 100 giorni intraday del DAPI è strutturale) come **dipendenza aperta**, con la decisione **rinviata a futuri cicli di estensione (attivazione PHASE-2)** `[DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:391]`.

- **Stato esatto**: **aperta**, rinviata all'**attivazione PHASE-2**. La scelta del vendor è PENDING (§3 — dipende dall'attivazione PHASE-2).
- **Valore di sistema**: rende esplicito che il training cross-index della PHASE-2 dipende da una fonte dati pluriennale ancora non scelta — confine dati di PHASE-2.

### B8-R-10 — L'apertura del flusso DAPI come fonte di training resta dipendenza aperta (nuovo task Planner)

Il prodotto **dichiara** l'apertura del flusso DAPI come fonte di training come **esplicitamente fuori scope / dipendenza aperta**: il vincolo Parte 8 (FIB Portara/CQG come unica fonte ufficiale di training) è invariato; una eventuale persistenza strutturale del flusso DAPI richiederebbe un **nuovo task Planner** con riesame delle convenzioni di back-adjustment, roll log e filtro pre-expiry `[DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:404]`. Lo stesso confine è ribadito sul versante tape: l'apertura del flusso DAPI come fonte di training è fuori scope e richiederebbe nuovo task Planner `[DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:238]`.

- **Stato esatto**: **aperta** (esplicitamente fuori scope corrente), rinviata a **nuovo task Planner**. Non risolta da B8.
- **Valore di sistema**: rende esplicito che il tape DAPI archiviato non è (oggi) fonte di training e che cambiarlo è una decisione strutturale futura — confine dati del prodotto.

### B8-R-11 — La migrazione del formato legacy→esteso dei dump resta dipendenza aperta (una-tantum FASE-D)

Il prodotto **dichiara** la migrazione del formato legacy→esteso dei 391 dump live esistenti come **operazione una-tantum di FASE-D, non normata in metodologia**: i dump legacy a 11 campi restano per il test di regressione, i dump nuovi adottano il format esteso a 13 campi `[DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:230]`. La coabitazione legacy/esteso dei sample è dichiarata senza vincolare la scelta architetturale FASE-D `[DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:235]`.

- **Stato esatto**: **aperta**, rinviata a **FASE-D** (operazione una-tantum, scelta architetturale non vincolata). Non risolta da B8.
- **Valore di sistema**: rende esplicito che la convivenza dei due formati di archivio è un debito di migrazione da chiudere in FASE-D — confine implementativo del ciclo di vita del tape.

### B8-R-12 — L'implementazione del codice operativo della pipeline resta dipendenza aperta (FASE-D)

Il prodotto **dichiara** che l'**implementazione del codice operativo** della pipeline runtime (parser DAPI realtime/storico, adapter DAPI→bundle frozen, layer di recovery, audit, gating qualitativo) vive in **FASE-D del roadmap**: i capitoli di confine sono **metodologia, non codice** `[DOC-INTERNO docs/methodology_v2/CAP_09_parte_9.md:406]`. Lo stesso vale per la pipeline di backfill, riconciliazione e archiviazione, rinviata a FASE-D `[DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:231]`.

- **Stato esatto**: **aperta**, rinviata a **FASE-D**. La codifica non è materia della spec corrente (metodologia/prodotto, non implementazione).
- **Valore di sistema**: rende esplicito il confine fra specifica (chiusa con la serie B1..B8) e implementazione (FASE-D), così che il go-live non sia confuso con la disponibilità di codice eseguibile.

### B8-R-13 — L'estensione dell'immutabilità CANDLERANGE oltre T+3 resta dipendenza aperta (probe addizionale FASE-D)

Il prodotto **dichiara** l'estensione del perimetro di immutabilità delle barre `CANDLERANGE` **oltre l'orizzonte T+3** (e oltre la finestra morning / su finestre afternoon e usopen / su strumenti non testati) come **dipendenza aperta**: il perimetro empirico onesto entro cui l'immutabilità è attestata empiricamente in modo diretto è T+3 morning sui ticker FIB6F/DITAS; oltre tale perimetro l'immutabilità è **assunta per estensione, sorvegliata dal gate di riconciliazione (Cap.60)**, e una eventuale estensione **richiede un nuovo probe empirico** (Q-XX al Planner, NON dentro Parte 10), da rifinire con probe addizionale in **FASE-D** se emerge necessità `[DOC-INTERNO docs/methodology_v2/CAP_10_parte_10.md:234]`.

- **Stato esatto**: **aperta**, PENDING-empirico, rinviata a **FASE-D** (probe addizionale) / sorvegliata dal gate Cap.60 nel frattempo. L'estensione del perimetro di immutabilità **non è risolta da B8** e **non è asserita** come dimostrata oltre T+3 morning.
- **Valore di sistema**: rende esplicito che la garanzia di idempotenza/immutabilità del backfill `CANDLERANGE` vale solo entro il perimetro empirico testato (T+3 morning, FIB6F/DITAS); fuori da quel perimetro è un'assunzione sorvegliata, non un fatto dimostrato — input per FASE-D prima di affidarvi backfill oltre quell'orizzonte.

---

## 3. Lista PENDING-empirico (marcate, NON asserite)

B8 **dichiara** le dipendenze aperte; il loro **esito/valore** è PENDING-empirico — marcato, non asserito (AC-B8-CONFINE/DEPS). Tutti ereditati; nessun PENDING nuovo introdotto da questo blocco di confine.

| PENDING | Requisito che lo dichiara | Destinazione | Stato |
|---|---|---|---|
| Latenza $L_{max}=30$s Telegram effettiva (M-2 OPEN) | B8-R-03 | Appendice E / FASE-D | dipendenza aperta dichiarata; valore non misurato |
| Upgrade empirico orario di sessione (M-GOV-1, da WIKI-HINT a PROVA-EMPIRICA via tape DAPI) | richiamato in B8 (premessa Cap.41 `:133`); upgrade empirico | probe V-1 (tape DAPI) / V-2 (calendario IDEM) / FASE-D | dipendenza aperta dichiarata; upgrade non eseguito |
| Calibrazione fine $\theta_{reconcile}$ (provvisorio) | B8-R-04 | FASE-D / CAP-DATA-04 / monitoring post-go-live | dipendenza aperta dichiarata; nessun valore assegnato |
| Congelamento empirico dei 10 parametri di tuning (carryover post-go-live) | B8-R-05 | monitoring post-go-live 3-6 mesi | dipendenza aperta dichiarata; default provvisori |
| Run del validator sull'edge (DSR/PBO/OOS, valori d'edge) | B8-R-06 | ruolo `validator` / FASE-D | dipendenza aperta dichiarata; nessun esito d'edge asserito |
| Decodifica codici mese Directa-IDEM mancanti (oltre `F`/`I`) | B8-R-07 | runtime-discovery (ANAG) / FASE-D | dipendenza aperta dichiarata; lookup incompleta |
| Abilitazione FDAX standard (account non abilitato 2026-05-27) | B8-R-08 | valutazione PHASE-2 | dipendenza aperta dichiarata; non decisa |
| Scelta vendor cross-index pluriennale (training PHASE-2) | B8-R-09 | attivazione PHASE-2 | dipendenza aperta dichiarata; non scelto |
| Estensione immutabilità barre `CANDLERANGE` oltre T+3 (e finestre afternoon/usopen / strumenti non testati) | B8-R-13 | probe addizionale FASE-D (Q-XX Planner) / gate Cap.60 nel frattempo | dipendenza aperta dichiarata; immutabilità oltre T+3 morning assunta per estensione, non dimostrata |

> **Nota M-GOV-1 (orario di sessione).** La finestra-sessione FIB 08:00-22:00 CET (epoca E5) è premessa B5-owned, origine normativa in `CAP_08_parte_8.md` Cap.41 `:133`. B8 la **cita solo** come dipendenza aperta (upgrade empirico M-GOV-1, da WIKI-HINT a PROVA-EMPIRICA), **non ri-consolida** la regola operativa di sessione (perimetro B5). La regola di sessione resta in vigore; ciò che è PENDING è l'**upgrade empirico** del valore.

> **NON pending (dichiarazioni di confine, citate con stato esatto, non da misurare):** la fasizzazione PHASE-1 FIB-only (B8-R-01); la dichiarazione PHASE-2 cross-index senza implementazione (B8-R-02, B8-CN-01, B8-CN-02); i costi noti della PHASE-1 (B8-CN-03); il confine cash europei ≠ cross-index PHASE-2 (B8-CN-04); il confine Parte 10 ≠ cross-index PHASE-2 (B8-CN-05); l'**esistenza e la destinazione** di ciascuna dipendenza aperta (la dichiarazione che è aperta è un fatto del capitolo, non un esito da misurare).

---

## 4. Matrice di tracciabilità + nota di rinvio

> **Nota su `B8-NFR-*`**: questo blocco di confine **non produce requisiti non funzionali propri**. La latenza Telegram (un NFR per natura) è qui richiamata **solo come dipendenza aperta dichiarata** (B8-R-03), non come NFR di prima istanza: la sua specifica NFR è già materia dei blocchi precedenti (premessa, non ri-derivata). Lo schema-ID `B8-NFR-NN` è riservato ma non istanziato in B8.

### 4.1 Matrice di tracciabilità

| ID | Proposizione (sintesi) | Capitolo:riga (fonte) | Valore operativo / di sistema |
|---|---|---|---|
| B8-R-01 | PHASE-1 = FIB-only single-instrument (dichiarata, non semplificazione silenziosa) | CAP_08_parte_8.md:167, :143, :145 | operatore: nessuna aspettativa cross-index in PHASE-1 |
| B8-R-02 | PHASE-2 cross-index = dichiarazione normativa senza implementazione | CAP_08_parte_8.md:143, :145 | sistema: "dichiarato" ≠ "implementato" |
| B8-CN-01 | Strumenti PHASE-2 (DAX/EuroStoxx50/S&P mini) previsti, non erogati | CAP_08_parte_8.md:147 | sistema: catalogo-strumenti dichiarato, confine esatto |
| B8-CN-02 | Estensioni (DCC/ADCC/cDCC, Realized GARCH, S_xidx + 5ª famiglia) dichiarate non implementate | CAP_08_parte_8.md:176, :182 | sistema: confine metodologico PHASE-1 |
| B8-CN-03 | Costi noti della fasizzazione PHASE-1 (σ_sys→σ_local, no canali cross-index, S_xidx non calcolabile, no riga contagio) | CAP_08_parte_8.md:174, :169, :170, :171, :172 | sistema: prezzo metodologico esplicito della PHASE-1 |
| B8-CN-04 | Cash europei = contesto live (logging+gating qualitativo), NON cross-index PHASE-2 | CAP_09_parte_9.md:338 | sistema: confine fine fra due materie distinte |
| B8-CN-05 | Parte 10 (tape/storicizzazione) NON si applica ai cross-index PHASE-2 | CAP_10_parte_10.md:236 | sistema: confine PHASE-1 esteso al ciclo di vita del tape |
| B8-R-03 | Latenza Telegram L_max=30s = dipendenza aperta (M-2 OPEN) | CAP_09_parte_9.md:402; CAP_10_parte_10.md:237 | sistema: vincolo di latenza dichiarato, valore non verificato |
| B8-R-04 | θ_reconcile = dipendenza aperta (provvisorio non congelato) | CAP_10_parte_10.md:131, :232 | sistema: gate riconciliazione dipende da parametro non fissato |
| B8-R-05 | 10 parametri tuning = dipendenza aperta (carryover post-go-live) | CAP_07_parte_VII.md:637, :641 | sistema: default provvisori da raffinare in produzione |
| B8-R-06 | Edge (DSR/PBO/OOS) = dipendenza aperta PENDING-empirico (validator/FASE-D) | CAP_10_parte_10.md:131 | sistema: nessun edge misurato dichiarato |
| B8-R-07 | Lookup completa codici mese IDEM = dipendenza aperta (runtime-discovery/FASE-D) | CAP_09_parte_9.md:389 | sistema: catalogo codici mese incompleto |
| B8-R-08 | Abilitazione FDAX standard = dipendenza aperta (PHASE-2) | CAP_09_parte_9.md:387 | sistema: confine commerciale PHASE-2 (account non abilitato) |
| B8-R-09 | Vendor cross-index pluriennale = dipendenza aperta (training PHASE-2) | CAP_09_parte_9.md:391 | sistema: confine dati training PHASE-2 |
| B8-R-10 | Flusso DAPI come fonte di training = dipendenza aperta (nuovo task Planner) | CAP_09_parte_9.md:404; CAP_10_parte_10.md:238 | sistema: confine dati del prodotto (tape ≠ training) |
| B8-R-11 | Migrazione formato legacy→esteso = dipendenza aperta (una-tantum FASE-D) | CAP_10_parte_10.md:230, :235 | sistema: debito di migrazione archivio |
| B8-R-12 | Implementazione codice pipeline = dipendenza aperta (FASE-D) | CAP_09_parte_9.md:406; CAP_10_parte_10.md:231 | sistema: confine specifica ↔ implementazione |
| B8-R-13 | Estensione immutabilità CANDLERANGE oltre T+3 = dipendenza aperta (probe addizionale FASE-D / gate Cap.60) | CAP_10_parte_10.md:234 | sistema: garanzia di idempotenza backfill solo entro T+3 morning testato |

### 4.2 Nota di rinvio (premesse §5 / out-of-scope §6)

**Premesse citate per riga, NON ri-derivate (verifica di fondazione, AC-B8-FRAMING):**

| Materia (premessa) | Capitolo:riga | Trattamento in B8 |
|---|---|---|
| Carryover dei 10 parametri di tuning post-go-live | CAP_07_parte_VII.md:637, :641 (Cap.36.3, **owned B7**) | citata come **dipendenza aperta** (B8-R-05); il gate di Cap.36 **non** è ri-derivato |
| Cash europei = logging+gating qualitativo, ≠ cross-index PHASE-2 | CAP_09_parte_9.md:338 (Cap.53, **owned B5**) | citata **solo** per il confine in B8-CN-04; il gating runtime/`gating_rules.yaml` **non** è ri-derivato |
| Calendario / epoca E5, sessione FIB 08:00-22:00 CET | CAP_08_parte_8.md:133 (Cap.41, **owned B5**) | citata **solo** come dipendenza aperta (upgrade empirico M-GOV-1, §3); la regola di sessione **non** è ri-consolidata |

> **Perché Cap.36.3, Cap.53, Cap.41 sono premesse e non perimetro.** Sono **già di proprietà** di blocchi chiusi (Cap.36 → B7; Cap.53/Cap.41 → B5). In B8 compaiono **solo** come riferimento puntuale di una dipendenza aperta (Cap.36.3: 10 param) o di un confine fine (Cap.53: cash ≠ cross-index; Cap.41: origine sessione). **Nessun requisito B8 è ancorato come fonte primaria a Cap.36/Cap.53/Cap.41**: la fonte primaria del confine PHASE-1/PHASE-2 è **Cap.42**; delle dipendenze aperte, **Cap.55/Cap.64**.

**Out-of-scope (con destinazione):**

| Materia | Destinazione |
|---|---|
| Implementazione PHASE-2 cross-index (layer covarianza, S_xidx, 5ª famiglia, feature cross-index) | spec futura (SPEC-FUNZ-02 o equivalente) — B8 consolida solo il confine dichiarato |
| Risoluzione delle dipendenze aperte (misura L_max, calibrazione θ_reconcile, congelamento 10 param, run validator edge, lookup codici mese, abilitazione FDAX, vendor cross-index) | FASE-D / validator / monitoring post-go-live — B8 le dichiara aperte (AC-B8-DEPS) |
| Assemblaggio della serie B1..B8 in un unico documento | task separato post-B8 — NON requisito B8 (AC-B8-NOASSEMBLY) |
| Indicizzazione / cross-reference dei blocchi B1..B7 | task separato post-B8 / assemblaggio — NON requisito B8 |
| Avvio FASE-D / specifica di implementazione FASE-D | FASE-D — fase successiva, NON requisito B8 |
| Verdetti d'edge / valori effettivi (DSR/PBO/E[R_net]/OOS) | FASE-D / ruolo `validator` — PENDING-empirico, MAI asserito |
| Materia di B1..B7 (gate Cap.36, gating Cap.53, sessione Cap.52, schema-dato) | blocchi rispettivi (chiusi) — premessa §5, non ri-derivare |

### 4.3 Nota RM-3 (gerarchia fonti)

Tutte le citazioni di questo blocco sono **richiami a capitoli metodologia v2 chiusi PASS** (`[DOC-INTERNO ...]`, livello 3 della gerarchia RM-3). Nessuna conclusione poggia su livello 4 (wiki/docs esterni); 0 conclusioni wiki-only. I `[PROVA-EMPIRICA]` interni ai capitoli (es. abilitazione FDAX 2026-05-27 in B8-R-08) sono **riportati come già dichiarati dal capitolo frozen**, non ri-asseriti di prima istanza (AC-G5). Grafia canonica `[CODICE-ESISTENTE]` / `[PROVA-EMPIRICA]` / `[DOC-INTERNO]` / `[WIKI-HINT]`; la grafia deprecata di `CODICE-ESISTENTE` (con "X" al posto di "S") non è usata (AC-G6, METODO RM-3).

---

*Documento B8 (8/8, ultimo della ricostruzione cieca). Derivato dai soli capitoli del perimetro-fonte primario (Cap.42 / Cap.55 / Cap.64) + premesse per riga (Cap.36.3 / Cap.53 / Cap.41), letti a HEAD `3136a55` (freeze G-09 verificato: diff a HEAD vuoti per CAP_08 `015c47a`, CAP_09 `28cfd2d`, CAP_10 `41447d3`, CAP_07 `b27c1e3`). Blocco di confine/chiusura: zero apertura di materia motore nuova, zero risoluzione di dipendenze aperte, zero requisiti di assemblaggio/indicizzazione/avvio-FASE-D. ID `B8-*` auto-assegnati da zero (cecità preservata).*
