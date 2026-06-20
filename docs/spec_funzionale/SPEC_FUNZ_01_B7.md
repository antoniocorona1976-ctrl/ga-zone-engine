# SPEC-FUNZ-01-B7 — Gate di go-live

> **Track**: Business-spec (SPEC-FUNZ), blocco 7/8. **Sede**: CLI. **Fonte autoritativa**: capitoli metodologia v2 chiusi PASS — `docs/methodology_v2/CAP_07_parte_VII.md` (Cap.31-36, SHA frozen di riferimento `b27c1e3`) + `docs/methodology_v2/CAP_01_parte_I.md` (Cap.5, SHA frozen di riferimento `e8d5424`). Pre-flight freeze G-09 eseguito: entrambi i diff `b27c1e3 HEAD` e `e8d5424 HEAD` **vuoti** → pin-riga §1 non slittati, citazioni rilette token-per-token a HEAD.

---

## 1. Intestazione, scopo, schema-ID, cecità, confine di ruolo

### 1.1 Scopo del blocco

Questo blocco consolida in **requisiti di prodotto** i **criteri di gate dichiarati dal metodo** per il go-live del motore di segnali FIB: la definizione operativa del successo del segnale (Cap.5), la procedura di validazione OOS che trasforma il fronte di Pareto in bundle candidato (Cap.31), il gate statistico primario DSR (Cap.32), il gate di fragilità PBO via CSCV (Cap.33), il bootstrap stazionario per gli intervalli di confidenza (Cap.34), la specifica di immutabilità del frozen bundle (Cap.35) e la checklist decisionale dei 12 criteri di go-live (Cap.36). È il ponte fra la metodologia v2 (validazione finale) e FASE-D (esecuzione del validator).

### 1.2 Schema-ID

Gli identificatori sono assegnati **da zero** in questo blocco, con atomicità N1 (una sola proposizione verificabile per requisito):

- **`B7-R-NN`** — requisito funzionale/di prodotto (criterio, procedura, definizione, regola).
- **`B7-CN-NN`** — vincolo/condizione di compliance o di confine (immutabilità, integrità, confine di ruolo, separazione dei piani).
- **`B7-NFR-NN`** — requisito non funzionale (qualità: latenza qualitativa, determinismo/replay, compute budget, formato).

### 1.3 Conferma di cecità

I requisiti `B7-*` sono derivati **dai soli** capitoli del perimetro (Cap.31-36 + Cap.5), senza alcun riferimento alla spec v2, ai file di chunking, ai blocchi B1-B6, né a conteggi-target o partizioni esterni. Gli ID sono auto-assegnati. Il confronto-copertura e la partizione sono compito del Reviewer/Orchestratore, non di questo documento.

### 1.4 ⚠️ NOTA DI CONFINE DI RUOLO — edge PENDING-empirico / validator (cardine del blocco)

**Questo documento consolida CRITERI DICHIARATI, MAI verdetti né valori d'edge.** Ogni gate è formulato come *criterio/definizione/soglia/procedura dichiarata dal metodo*. Ogni grandezza misurabile — il valore effettivo di DSR, PBO, $E[R_{net}]$, CVaR, MDD, $r_{emit}$, $\rho_{sessions}$; l'esito dei 12 criteri di go-live; la decisione GO/NO-GO — è **PENDING-empirico (validator / FASE-D)** e **mai** asserita come "verificata", "superata", "confermata".

**B7 (e l'intero track SPEC-FUNZ) NON emette verdetti GO / CONDITIONAL / NO-GO né valori d'edge.** L'emissione di tali verdetti su DSR/PBO/out-of-sample è **esclusiva del ruolo `validator`** (`.claude/agents/validator.md`), in panchina fino a FASE-D. La spec consolida la *checklist e la procedura*; l'*esito* è del validator. La lista completa delle grandezze PENDING-empirico è nella §9.3.

Verbi vietati in questo documento su grandezze d'esito: "il bundle supera/passa il gate", "DSR è positivo/significativo", "l'edge esiste/è confermato", "GO". Verbi ammessi: "il metodo richiede DSR$>\theta_{DSR}$", "il criterio dichiarato è …", "al run del validator si misurerà …".

---

## 2. Definizione operativa del successo (Cap.5 di Parte I)

**Valore operativo trasversale di questa sezione**: definire *che cosa* il sistema deve raggiungere perché il segnale sia accettabile per l'operatore retail FIB, in termini quantitativi e verificabili sul segnale, distinti dal risultato economico personale dell'operatore.

### B7-R-01 — Metrica primaria di segnale: expected net return per segnale eseguito
Il criterio dichiarato definisce come **metrica primaria** l'expected net return per segnale eseguito $E[R_{net}\mid executed]$, valore atteso del rendimento netto in punti FIB di un segnale che ha completato il proprio ciclo di vita fino all'esecuzione e alla chiusura.
**Valore**: dà all'operatore una misura unica e confrontabile della redditività attesa del segnale al netto dei costi.
**Fonte**: `[DOC-INTERNO CAP_01_parte_I.md:71]`.

### B7-R-02 — Conversione lordo→netto della metrica primaria
Il criterio dichiarato fissa la relazione lineare $E[R_{net}\mid executed] = E[R_{gross}\mid executed] - 2\cdot c$, con $c = 1$ punto FIB equivalente per operazione (conversione delle commissioni di 5 EUR sul moltiplicatore 5 EUR/punto) e fattore 2 per la doppia operazione apertura+chiusura.
**Valore**: rende esplicito che il successo è misurato dopo commissioni, coerente con l'operatività reale (5 EUR/op).
**Fonte**: `[DOC-INTERNO CAP_01_parte_I.md:73-75]`.

### B7-R-03 — Metriche di lifecycle del segnale
Il criterio dichiarato richiede il calcolo, sul replay OOS della state machine, delle metriche di lifecycle: emission count, executable rate, target_1 hit rate, target_2 hit rate ($\pi_{t_2\mid t_1}$), invalidation rate, missed-target rate.
**Valore**: descrive il comportamento del segnale lungo tutto il suo ciclo, non solo l'esito finale, dando all'operatore visibilità su quanti segnali sono eseguibili e quanti convertono.
**Fonte**: `[DOC-INTERNO CAP_01_parte_I.md:77]`.

### B7-R-04 — Metriche di rischio del segnale
Il criterio dichiarato richiede il calcolo, sullo stesso replay, delle metriche di rischio: CVaR al 95% del rendimento per segnale eseguito, maximum drawdown intraday dell'equity sintetica di sessione, MAE e MFE aggregati condizionati allo stato di lifecycle terminale.
**Valore**: quantifica il rischio di coda e di drawdown a cui l'operatore retail (1 contratto/volta) è esposto.
**Fonte**: `[DOC-INTERNO CAP_01_parte_I.md:79]`.

### B7-R-05 — Metriche anti-overfitting
Il criterio dichiarato subordina la selezione del bundle frozen a gate basati su DSR (filtro primario + significatività al netto del numero di prove) e su PBO via CSCV (fragilità della scelta rispetto a partizioni alternative dei dati).
**Valore**: protegge l'operatore dal pubblicare un bundle che funziona solo "sulla carta" per effetto del numero di tentativi (overfitting).
**Fonte**: `[DOC-INTERNO CAP_01_parte_I.md:81]`.

### B7-R-06 — Dichiarazione di successo per il go-live (criterio dichiarato)
Il criterio dichiarato definisce il motore **accettato per il go-live** se, sui dati OOS della prima campagna, il bundle candidato presenta: DSR positivo e significativo; PBO sotto la soglia calibrata in Parte VII; $E[R_{net}\mid executed]$ positivo dopo commissioni; target hit rate ed executable rate stabili e comparabili fra regime calmo e turbolento; CVaR al 95% e MDD intraday entro limiti dichiarati. Questo è il **criterio di accettazione dichiarato**, il cui *esito* è PENDING-empirico (validator / FASE-D).
**Valore**: stabilisce, prima di qualunque misura, la condizione complessiva sotto cui un bundle può essere pubblicato come segnale operativo.
**Fonte**: `[DOC-INTERNO CAP_01_parte_I.md:85]`.

### B7-CN-01 — Confine successo-del-segnale vs risultato-dell'operatore
Il successo del motore è definito **in termini quantitativi e verificabili del segnale**, ed è **distinto** dal risultato economico aggregato dell'operatività dell'utilizzatore. Le componenti governate dall'operatore e non dal motore — esecuzione manuale, disciplina sullo stop personale, gestione del rollover, qualità del feed Directa — **non rientrano** nel criterio di successo del motore.
**Valore**: evita di attribuire al segnale colpe/meriti dell'esecuzione manuale; tutela la valutazione corretta del motore e le aspettative dell'operatore.
**Fonte**: `[DOC-INTERNO CAP_01_parte_I.md:69]`, `[DOC-INTERNO CAP_01_parte_I.md:85]`.

---

## 3. Procedura di validazione OOS (Cap.31 di Parte VII)

**Valore operativo trasversale**: definire la procedura *deterministica* con cui si passa dal fronte di Pareto a un singolo bundle candidato, in modo riproducibile e auditabile.

### B7-NFR-01 — Fonte canonica unica: log di replay deterministico bit-exact (invariante)
Tutte le metriche di gate sono calcolate dalla **fonte canonica unica** = log di replay deterministico bit-exact (invariante ereditato come premessa da `CAP_02_parte_II.md` Cap.10, non ri-derivato qui), generato durante la valutazione della fitness multi-obiettivo, sulla finestra OOS aggregata.
**Valore**: garantisce che la validazione sia riproducibile al bit e auditabile, requisito di fiducia per l'operatore e per FASE-D.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:21]`, `[DOC-INTERNO CAP_07_parte_VII.md:7]`.

### B7-CN-02 — Vincolo "solo emissione": nessuna metrica su fill effettivi del broker
Il criterio dichiarato impone che **nessuna metrica di Parte VII sia calcolata su fill effettivi del broker**: la verifica di go-live opera interamente sui log di replay, in coerenza col vincolo "solo emissione" (eredità invariante Cap.1 di Parte I).
**Valore**: il motore non esegue ordini; valutarlo sui propri segnali (non sui fill) è coerente col perimetro "segnali, non esecuzione" e protegge da contaminazioni dell'esecuzione manuale.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:21]`.

### B7-R-07 — Finestra OOS aggregata con esclusione purge/embargo (anti-leakage)
Il criterio dichiarato definisce la **finestra OOS aggregata** come concatenazione temporale dei $W_{oos}$ degli $F$ fold del walk-forward nested effettivamente completati, **con esclusione** dei blocchi di purge ($P_{purge}=4.200$ barre) ed embargo ($P_{emb}=4.200$ barre) fra in-sample e out-of-sample di ciascun fold, in prevenzione del leakage.
**Valore**: assicura che la valutazione del segnale avvenga su dati realmente fuori campione, evitando di sovrastimare la bontà del segnale per leakage.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:15-19]`.

### B7-R-08 — Selezione deterministica e lessicografica del bundle candidato
Il criterio dichiarato impone che la selezione del cromosoma vincente $\theta^*$ (bundle candidato) dal fronte di Pareto $\mathcal{F}_1$ sia **deterministica e lessicografica**, applicando in sequenza sei filtri ordinati più un criterio finale di massimizzazione con tie-break esplicito, coerente col replay bit-exact.
**Valore**: un'unica selezione riproducibile elimina arbitrarietà; lo stesso input produce sempre lo stesso bundle, requisito di audit.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:29]`.

### B7-R-09 — Filtro 1: gate primario DSR
Il criterio dichiarato (Filtro 1) seleziona i cromosomi con $DSR(\theta^{(k)}) > \theta_{DSR} = 0{,}95$, eliminando i cromosomi statisticamente non distinguibili dal benchmark deflazionato. (Esito su singolo cromosoma = PENDING-empirico.)
**Valore**: come primo setaccio, scarta segnali la cui performance può essere frutto del numero di prove.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:31]`.

### B7-R-10 — Filtro 2: gate di fragilità PBO
Il criterio dichiarato (Filtro 2) seleziona, fra i sopravvissuti al Filtro 1, i cromosomi con $PBO(\theta^{(k)}) < \theta_{PBO} = 0{,}50$, eliminando quelli la cui scelta dipende fragilmente dalla partizione del dato OOS. (Esito = PENDING-empirico.)
**Valore**: scarta segnali la cui bontà è un artefatto di quale fetta di dati è stata usata.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:33]`.

### B7-R-11 — Filtro 3: lifecycle stabile cross-regime
Il criterio dichiarato (Filtro 3) seleziona, fra i sopravvissuti al Filtro 2, i cromosomi con $|f_5^{global}(\theta^{(k)})| < \theta_{f_5} = 0{,}30$ (stabilità cross-regime sulla finestra OOS aggregata), eliminando i cromosomi sbilanciati verso un solo regime.
**Valore**: privilegia segnali che funzionano sia in mercato calmo sia turbolento, riducendo il rischio per l'operatore al cambio di regime.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:35]`.

### B7-R-12 — Filtro 4: IQR cross-fold normalizzata su $f_1$
Il criterio dichiarato (Filtro 4) seleziona, fra i sopravvissuti al Filtro 3, i cromosomi con $\text{IQR}_{norm}(f_1)(\theta^{(k)}) < \theta_{IQR} = 0{,}40$, eliminando i cromosomi con metrica $f_1$ instabile fra fold.
**Valore**: privilegia segnali la cui redditività attesa è stabile nel tempo, non concentrata in pochi periodi fortunati.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:37]`.

### B7-R-13 — Filtro 5: probabilità di proseguimento $\pi_{t_2\mid t_1}$ minima
Il criterio dichiarato (Filtro 5) seleziona, fra i sopravvissuti al Filtro 4, i cromosomi con $\pi_{t_2\mid t_1}^{aggregated}(\theta^{(k)}) > \theta_{t_2} = 0{,}30$, eliminando i cromosomi che producono molti `target_1_hit` di scarsa qualità informativa per la submachine.
**Valore**: privilegia segnali il cui primo target tende a proseguire verso il secondo, informazione utile alla gestione manuale della posizione.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:39]`.

### B7-R-14 — Selezione finale per massimizzazione di $f_1^{global}$ con tie-break
Il criterio dichiarato seleziona, fra i sopravvissuti ai filtri 1-5, il cromosoma $\theta^*$ con $f_1^{global}$ (mediana cross-fold) massimo; in caso di parità entro tolleranza $\epsilon_{f_1}=10^{-6}$ pt FIB applica un tie-break lessicografico crescente in tre livelli: minimo $\text{IQR}_{norm}(f_1)$, minimo $|f_5^{global}|$, hash deterministico del cromosoma.
**Valore**: chiude la selezione su un unico bundle in modo deterministico anche a parità, garantendo riproducibilità totale.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:41]`, `[DOC-INTERNO CAP_07_parte_VII.md:43-46]`.

### B7-R-15 — Caso di fallimento di go-live a livello di selezione
Il criterio dichiarato stabilisce che, se nessun cromosoma del fronte $\mathcal{F}_1$ sopravvive ai filtri 1-5, il run è dichiarato **fallito di go-live** e si produce un report di fallimento con motivazione esplicita (quale filtro ha eliminato l'ultimo candidato e su quale soglia). La decisione di ricalibrazione è rinviata alla sessione operativa post-fallimento. (L'occorrenza effettiva = PENDING-empirico.)
**Valore**: garantisce che, in assenza di un bundle valido, il sistema **non pubblichi** segnali, proteggendo l'operatore; e che il fallimento sia tracciato per la correzione successiva.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:50]`.

---

## 4. Gate statistico primario — DSR (Cap.32 di Parte VII)

**Valore operativo trasversale**: definire il gate che misura se la performance del segnale è genuina al netto del numero di prove condotte.

### B7-R-16 — Definizione del Deflated Sharpe Ratio (DSR)
Il criterio dichiarato definisce il DSR come gate primario di significatività della performance al netto di: (i) numero $N_{trials}$ di prove (bias di selezione), (ii) lunghezza finita $n$ del campione, (iii) non-normalità (skewness $\hat\gamma_3$, curtosi $\hat\gamma_4$). La formula adottata è la formulazione canonica Bailey-López de Prado 2014 (CDF normale di $(\widehat{SR}-SR^*)\sqrt{n-1}$ corretta per skew/curtosi), con $N_{trials}=|\mathcal{F}_1|$.
**Valore**: traduce in un singolo numero la domanda "questo segnale è migliore del caso, dato che ho provato molti cromosomi?", proteggendo l'operatore dall'illusione statistica.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:139]`, `[DOC-INTERNO CAP_07_parte_VII.md:143]`. Riferimento bibliografico del capitolo: Bailey-López de Prado 2014 `[WIKI-HINT, da verificare]` (citato dal capitolo, non fonte di prima istanza).

### B7-R-17 — Soglia di accettazione del DSR (valore di lavoro provvisorio)
Il criterio dichiarato fissa la soglia $\theta_{DSR}=0{,}95$ (test a un solo lato al 5% contro $H_0: SR\le SR^*$), **valore di lavoro provvisorio non congelato in Parte VII, riconsiderato post-go-live**. Il valore *effettivo* di $DSR(\theta^*)$ è PENDING-empirico (validator).
**Valore**: stabilisce in anticipo l'asticella di significatività; dichiararla provvisoria evita che venga trattata come legge definitiva prima dei dati di produzione.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:202]`, `[DOC-INTERNO CAP_07_parte_VII.md:204]`, `[DOC-INTERNO CAP_07_parte_VII.md:244]`.

---

## 5. Gate di fragilità — PBO via CSCV (Cap.33 di Parte VII)

**Valore operativo trasversale**: definire il gate che misura quanto la scelta del bundle dipenda fragilmente dalla partizione dei dati (overfitting).

### B7-R-18 — Definizione del PBO via CSCV
Il criterio dichiarato definisce il PBO come probabilità che il cromosoma vincente in-sample sia overfit (OOS sotto la mediana del fronte), stimato via **Combinatorially Symmetric Cross-Validation** in **sei passi** (partizione in $S$ sotto-finestre contigue, enumerazione $\binom{S}{S/2}$, rank Sharpe in-sample, rank OOS del vincente, logit-rank, frazione di combinazioni con logit-rank negativa).
**Valore**: misura se la bontà del segnale resiste a partizioni alternative dei dati, proteggendo l'operatore da segnali fragili.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:252]`, `[DOC-INTERNO CAP_07_parte_VII.md:254]`. Riferimento bibliografico del capitolo: Bailey-Borwein-López de Prado-Zhu 2017 `[WIKI-HINT, da verificare]`.

### B7-R-19 — Regola deterministica $S = 2F$ per il numero di sotto-finestre CSCV
Il criterio dichiarato fissa il numero di sotto-finestre $S$ secondo la regola deterministica $S = 2F$ (2 blocchi per fold), con $S$ pari e $S \in \{12,14,16\}$ ($S=12$ per $F=6$, $S=14$ per $F=7$, $S=16$ per $F=8$), preservando la struttura temporale di ciascun fold.
**Valore**: lega il numero di partizioni alla struttura reale dei dati in modo riproducibile, evitando rotture artificiali della dipendenza temporale.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:294-298]`, `[DOC-INTERNO CAP_07_parte_VII.md:322]`.

### B7-R-20 — Soglia di accettazione del PBO (valore di lavoro provvisorio)
Il criterio dichiarato fissa la soglia $PBO(\theta^*) < \theta_{PBO}=0{,}50$ (gate minimo), **valore di lavoro provvisorio non congelato in Parte VII, riconsiderato post-go-live** (possibile innalzamento a $0{,}40$ post-go-live). Il valore *effettivo* di $PBO(\theta^*)$ è PENDING-empirico (validator).
**Valore**: stabilisce in anticipo la soglia di fragilità tollerata; la provvisorietà evita di trattarla come definitiva prima dei dati.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:304]`, `[DOC-INTERNO CAP_07_parte_VII.md:308]`, `[DOC-INTERNO CAP_07_parte_VII.md:344]`.

---

## 6. Intervalli di confidenza — bootstrap stazionario (Cap.34 di Parte VII)

**Valore operativo trasversale**: definire come si producono gli intervalli di confidenza sulle metriche aggregate, a supporto del gate sull'$E[R_{net}]$.

> **Nota framing (Cap.34 = procedura di supporto).** Il bootstrap stazionario è il *meccanismo statistico interno* che produce gli $IC_{95\%}$ usati dal gate **B7-R-26** (AC-GO-3, $E[R_{net}]>0$ con IC che esclude lo zero). Non fonda un requisito-prodotto standalone ulteriore: è consolidato qui come **procedura dichiarata a corredo** del gate sull'$E[R_{net}]$ (anti-gonfiamento del perimetro). I requisiti B7-R-21/22/23 ne fissano la procedura, la replicazione e l'uso; non si scrive un requisito "su Cap.34" privo di proposizione di prodotto non già coperta da B7-R-26.

### B7-R-21 — Procedura del bootstrap stazionario a blocchi geometrici
Il criterio dichiarato definisce il bootstrap stazionario (Politis-Romano 1994) come ricampionamento a **blocchi di lunghezza aleatoria geometrica** ($p=1/L_{avg}$) sui rendimenti $R_{net}$ dei segnali eseguiti, con wrap modulo $n$ che garantisce la stazionarietà del processo bootstrappato.
**Valore**: produce intervalli di confidenza che rispettano la dipendenza temporale dei rendimenti del segnale, dando all'operatore una stima onesta dell'incertezza.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:352]`, `[DOC-INTERNO CAP_07_parte_VII.md:354-356]`, `[DOC-INTERNO CAP_07_parte_VII.md:358]`. Riferimento bibliografico del capitolo: Politis-Romano 1994 `[WIKI-HINT, da verificare]`.

### B7-R-22 — Numero di replicazioni bootstrap $B = 2.000$
Il criterio dichiarato fissa $B = 2.000$ replicazioni bootstrap (eredità Cap.4 di Parte I, compute budget cloud), producendo la distribuzione empirica da cui si ricavano gli $IC_{95\%}$ via percentile method (default; BCa alternativa per metriche skewed).
**Valore**: fissa un numero di repliche sufficiente a stabilizzare gli intervalli, dentro il budget di calcolo del progetto.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:359]`, `[DOC-INTERNO CAP_07_parte_VII.md:379-381]`, `[DOC-INTERNO CAP_07_parte_VII.md:449]`.

### B7-R-23 — Calibrazione automatica della block length $L_{avg}$ (valore di lavoro provvisorio)
Il criterio dichiarato impone la calibrazione automatica di $L_{avg}$ via Politis-White 2004 su ogni run; il valore $L_{avg}=10$ segnali è **default di lavoro provvisorio non congelato in Parte VII**, solo starting point (con troncamenti ai bordi $L_{avg}\in[1, n/5]$). Il valore *effettivo* calibrato è PENDING-empirico.
**Valore**: adatta la lunghezza dei blocchi all'autocorrelazione reale dei segnali, senza fissare a priori un valore arbitrario.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:369]`, `[DOC-INTERNO CAP_07_parte_VII.md:371]`, `[DOC-INTERNO CAP_07_parte_VII.md:373]`, `[DOC-INTERNO CAP_07_parte_VII.md:449]`.

### B7-NFR-02 — Replay bit-exact del bootstrap via seed PRNG dedicato
Il criterio dichiarato impone che il seed PRNG del bootstrap sia parte dell'identità del bundle frozen e separato dagli altri seed; due esecuzioni con stesso seed, stessi log e stesso $L_{avg}$ producono **identici intervalli di confidenza al bit**, in coerenza col vincolo di replay bit-exact.
**Valore**: rende gli intervalli di confidenza riproducibili e auditabili, requisito di fiducia per FASE-D.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:445]`, `[DOC-INTERNO CAP_07_parte_VII.md:447]`.

---

## 7. Frozen bundle e immutabilità (Cap.35 di Parte VII)

**Valore operativo trasversale**: definire l'artefatto immutabile pubblicato in produzione e le regole che ne governano integrità e sostituzione.

### B7-CN-03 — Composizione del bundle frozen come artefatto immutabile (sei elementi)
Il criterio dichiarato definisce il **bundle frozen** come artefatto digitale **immutabile** composto da sei elementi: (1) parametri congelati di Parte V; (2) geni del cromosoma vincente $\theta^*$; (3) modelli stimati (EGARCH, Cox/Fine-Gray, quantili regime); (4) definizione formale della tupla payload $\mathcal{S}$; (5) seed PRNG; (6) metadati di tracciabilità.
**Valore**: ciò che va in produzione è un oggetto unico, completo e congelato; nulla cambia "in silenzio" dopo la pubblicazione del segnale.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:457]`, `[DOC-INTERNO CAP_07_parte_VII.md:459]`, `[DOC-INTERNO CAP_07_parte_VII.md:461-466]`, `[DOC-INTERNO CAP_07_parte_VII.md:483-500]`.

### B7-CN-04 — Hash SHA-256 di riferimento immutabile del bundle
Il criterio dichiarato impone il calcolo deterministico di un **hash crittografico SHA-256** sull'intero contenuto dei sei elementi (serializzazione canonica), registrato nel bundle come campo `bundle_hash`.
**Valore**: dà un'impronta univoca al bundle, base per integrità e tracciabilità di ogni segnale emesso.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:506]`, `[DOC-INTERNO CAP_07_parte_VII.md:509-510]`.

### B7-CN-05 — Validazione di integrità all'avvio: la pipeline si rifiuta di girare su hash non corrispondente
Il criterio dichiarato impone che, a ogni caricamento del bundle in pipeline, l'hash sia ricalcolato e confrontato col `bundle_hash` registrato; se i due hash **non coincidono al bit**, il caricamento **fallisce e la pipeline si rifiuta di girare**, con log esplicito dell'errore di integrità.
**Valore**: protegge l'operatore da un bundle corrotto o alterato — meglio nessun segnale che un segnale prodotto da un bundle compromesso.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:512-517]`.

### B7-R-24 — Regola di sostituzione del bundle frozen (quattro regole + gestione segnali attivi)
Il criterio dichiarato governa la sostituzione del bundle con quattro regole esplicite — (1) pianificata trimestrale/semestrale, (2) anticipata su trigger di deriva, (3) anticipata su Cox time-varying attivato, (4) anticipata su fallimento di go-live — con regola comune: i segnali in stato `active` alla transizione **continuano la propria state machine con il bundle precedente** fino a uno stato terminale; solo le nuove emissioni usano il nuovo bundle. La motivazione è registrata in `replacement_reason`.
**Valore**: garantisce continuità del servizio all'operatore (un segnale in corso non cambia regole a metà) e tracciabilità del motivo di ogni sostituzione.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:523]`, `[DOC-INTERNO CAP_07_parte_VII.md:525]`, `[DOC-INTERNO CAP_07_parte_VII.md:533]`.

---

## 8. Gate decisionali di go-live (Cap.36 di Parte VII)

**Valore operativo trasversale**: definire la checklist binaria, deterministica e replicabile che autorizza (o nega) la pubblicazione del bundle come segnale operativo. **Ogni criterio è un gate *dichiarato*; l'esito di ciascuno e la decisione complessiva sono PENDING-empirico (validator / FASE-D).**

I 12 criteri di go-live (`CAP_07_parte_VII.md:568`) sono consolidati come **12 requisiti distinti** (atomicità N1: un criterio binario OK/NOT-OK ciascuno). Per i criteri compositi al loro interno (B7-R-34 pipeline, B7-R-35 dashboard) le sotto-condizioni sono **enumerate dentro il singolo criterio** come contenuto di verifica, non spacchettate in requisiti separati; B7-R-36 (hash all'avvio) è condizione singola già atomica.

### B7-R-25 — Criterio di go-live 1: gate primario DSR
Criterio dichiarato OK/NOT-OK: $DSR(\theta^*) > \theta_{DSR}=0{,}95$. (Esito = PENDING-empirico.)
**Valore**: ribadisce come gate esplicito di go-live la significatività statistica della performance.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:570]`.

### B7-R-26 — Criterio di go-live 2: expected net return positivo con IC bootstrap escluso lo zero
Criterio dichiarato OK/NOT-OK: $E[R_{net}\mid executed](\theta^*) = f_1^{global}(\theta^*) > 0$ **con $IC_{95\%}$ bootstrap $[a,b]$ tale che $a>0$**. (Esito e IC effettivi = PENDING-empirico.)
**Valore**: richiede che la redditività attesa netta sia non solo positiva ma statisticamente distinta da zero, alzando la garanzia per l'operatore.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:574]`.

> NB ordinamento: il capitolo enumera AC-GO-2 = gate PBO e AC-GO-3 = expected net return. Per atomicità i requisiti sono assegnati uno-a-uno ai criteri del capitolo; **B7-R-26 traccia ad AC-GO-3 (`:574`)** e **B7-R-27 traccia ad AC-GO-2 (`:572`)**. La numerazione `B7-R-*` non riproduce l'ordine `AC-GO-*`: la corrispondenza puntuale è nella matrice §9.

### B7-R-27 — Criterio di go-live 3: gate di fragilità PBO
Criterio dichiarato OK/NOT-OK: $PBO(\theta^*) < \theta_{PBO}=0{,}50$. (Esito = PENDING-empirico.)
**Valore**: ribadisce come gate esplicito di go-live la non-fragilità della scelta del bundle.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:572]`.

### B7-R-28 — Criterio di go-live 4: lifecycle stabile cross-regime
Criterio dichiarato OK/NOT-OK: $|f_5^{global}(\theta^*)| < \theta_{f_5}=0{,}30$ (riverifica esplicita del Filtro 3 come gate di go-live). (Esito = PENDING-empirico.)
**Valore**: conferma in fase di go-live che il segnale è bilanciato fra regimi calmo/turbolento.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:576]`.

### B7-R-29 — Criterio di go-live 5: stabilità cross-fold
Criterio dichiarato OK/NOT-OK: $\text{IQR}_{norm}(f_1)(\theta^*) < \theta_{IQR}=0{,}40$ (riverifica esplicita del Filtro 4). (Esito = PENDING-empirico.)
**Valore**: conferma in fase di go-live che la redditività attesa è stabile nel tempo.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:578]`.

### B7-R-30 — Criterio di go-live 6: CVaR entro limite (soglia provvisoria)
Criterio dichiarato OK/NOT-OK: $\text{CVaR}_{95\%}(\theta^*) > \theta_{CVaR}=-100$ pt FIB, **valore di lavoro provvisorio, non congelato in Parte VII, riconsiderato post-go-live**. (Esito = PENDING-empirico.)
**Valore**: limita la perdita media nei segnali peggiori (worst-5%) a 100 pt, coerente con stop strutturali tipici di FIB intraday e col profilo retail 1 contratto/volta.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:580]`.

### B7-R-31 — Criterio di go-live 7: MDD intraday entro limite (soglia provvisoria)
Criterio dichiarato OK/NOT-OK: $\text{MDD}_{intraday}(\theta^*) < \theta_{MDD}=200$ pt FIB, **valore di lavoro provvisorio, non congelato in Parte VII, riconsiderato post-go-live** ($200\cdot 5 = 1.000$ EUR per contratto). (Esito = PENDING-empirico.)
**Valore**: limita il drawdown intraday massimo a un livello compatibile col profilo retail mobile (1 contratto/volta).
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:582]`.

### B7-R-32 — Criterio di go-live 8: frequenza di emissione entro range
Criterio dichiarato OK/NOT-OK: $r_{emit}(\theta^*) \in [E_{min}=0{,}2; E_{max}=5]$ segnali/sessione (riverifica esplicita sul fold OOS aggregato). (Esito = PENDING-empirico.)
**Valore**: garantisce che il motore non sia né silente né iperattivo, coerente con un operatore che esegue manualmente da cellulare.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:584]`.

### B7-R-33 — Criterio di go-live 9: target operativo asimmetrico raggiunto
Criterio dichiarato OK/NOT-OK: $\rho_{sessions} > \theta_{sessions}=0{,}60$ (**valore di lavoro provvisorio, non congelato in Parte VII, riconsiderato post-go-live**), dove $\rho_{sessions}$ è la frazione di sessioni del fold OOS aggregato che raggiungono il **target operativo asimmetrico di Cap.1 di Parte I** — 500 pt FIB profitto netto/giorno (soglia assoluta $T_{abs}$) **OR** 70% del movimento strutturale intraday (soglia relativa $T_{rel}$), condizione OR $T(d)=T_{abs}(d)\lor T_{rel}(d)$. (Esito e $\rho_{sessions}$ effettivo = PENDING-empirico.)
**Valore**: lega il go-live all'obiettivo operativo concreto dichiarato per il prodotto, tarato sul singolo giorno di trading.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:586]`, `[DOC-INTERNO CAP_07_parte_VII.md:609-625]`, `[DOC-INTERNO CAP_07_parte_VII.md:629-631]`.

### B7-R-34 — Criterio di go-live 10: pipeline di inference operativa (criterio composito)
Criterio dichiarato OK/NOT-OK **unico** sulla verifica funzionale della pipeline di inference real-time, il cui contenuto di verifica enumera quattro sotto-condizioni: (a) carica correttamente il bundle frozen con hash SHA-256 valido al caricamento; (b) processa un feed di test e produce un payload bit-exact identico alla specifica della tupla a 12 campi; (c) pubblica messaggi Telegram di test conformi al layout mobile-first; (d) la latenza end-to-end rispetta il vincolo qualitativo $L_{max}=30$ s (la verifica numerica empirica di $L_{max}$ resta carryover, vedi B7-NFR-03). Le quattro sotto-condizioni sono il contenuto di verifica di un **unico** criterio binario, non requisiti separati. (Esito funzionale = PENDING-empirico, FASE-D.)
**Valore**: garantisce che il segnale arrivi davvero all'operatore via Telegram, correttamente formattato e in tempi accettabili, prima di dichiarare il go-live.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:588]`, `[DOC-INTERNO CAP_07_parte_VII.md:589-592]`.

### B7-R-35 — Criterio di go-live 11: dashboard di monitoring operativa (criterio composito)
Criterio dichiarato OK/NOT-OK **unico** sulla verifica che la dashboard di monitoring live è configurata e attiva, il cui contenuto di verifica enumera tre sotto-condizioni: (a) tracciamento di tutte le metriche live ($f_1^{live}..f_5^{live}$, $B(t)$, $r_{emit}^{live}$); (b) tutti gli alert configurati e testati (deriva fitness, deriva $f_5^{live}$, break parametrico EGARCH, frequenza emissione fuori range); (c) reporting opzionale lifecycle aggiuntivo. Le tre sotto-condizioni sono il contenuto di verifica di un **unico** criterio binario. (Esito funzionale = PENDING-empirico, FASE-D.)
**Valore**: garantisce che, una volta live, il comportamento del segnale sia monitorato e gli scostamenti generino alert, proteggendo l'operatore da derive non rilevate.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:594]`, `[DOC-INTERNO CAP_07_parte_VII.md:595-597]`.

### B7-R-36 — Criterio di go-live 12: hash bundle frozen valido all'avvio (condizione singola)
Criterio dichiarato OK/NOT-OK **singolo** (già atomico): il bundle frozen del run corrente ha hash SHA-256 valido all'avvio della pipeline, ovvero il caricamento iniziale non produce errore di integrità (riverifica del meccanismo di B7-CN-04/B7-CN-05 nel primo caricamento operativo). (Esito = PENDING-empirico, FASE-D.)
**Valore**: ultimo controllo prima del go-live che il bundle pubblicato è integro al primo avvio operativo.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:599]`.

### B7-CN-06 — Procedura di decisione GO/NO-GO deterministica (esito = validator/FASE-D)
Il criterio dichiarato definisce la **procedura** di decisione binaria: GO se **tutti i 12 criteri** sono OK; NO-GO se **anche un solo** criterio è NOT-OK, con motivazione esplicita su quale criterio è fallito + raccomandazione operativa per classe (gate statistici → re-applicazione Parte V o ritocco soglie; metriche operative → revisione cromosoma; infrastruttura → correzione tecnica senza re-training). **B7 consolida la procedura; l'esito GO/NO-GO è esclusiva del ruolo `validator`** (PENDING-empirico, FASE-D), mai asserito qui.
**Valore**: rende la decisione di pubblicazione totalmente deterministica e tracciabile, senza discrezionalità; e separa nettamente "chi definisce la regola" (metodo/spec) da "chi emette il verdetto" (validator).
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:601]`, `[DOC-INTERNO CAP_07_parte_VII.md:602-605]`.

### B7-R-37 — Reporting separato per regime calmo/turbolento (metrica, non gate)
Il criterio dichiarato impone che $\rho_{sessions}$ sia calcolata anche separatamente per sessioni calmo e turbolento, producendo $\rho_{sessions}^{calmo}$ e $\rho_{sessions}^{turbolento}$; la differenza $|\rho^{calmo}-\rho^{turbolento}|$ è **metrica di reporting, non gate binario**. (Valori effettivi = PENDING-empirico.)
**Valore**: dà visibilità su quanto il rendimento operativo dipenda dal regime di mercato, informazione utile per l'operatore senza vincolare il go-live.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:633]`.

### B7-CN-07 — Carryover post-go-live dei 10 parametri di tuning operativo di Parte VI
Il criterio dichiarato stabilisce che i 10 parametri di tuning operativo di Parte VI **rimangono starting point con i default proposti di Parte VI** per il primo run di produzione; il loro congelamento empirico richiede dati di produzione live (distribuzione degli alert, frequenza break EGARCH, $r_{emit}^{live}$ effettiva) ed è attività di monitoring post-go-live a 3-6 mesi, **non task di Parte VII**.
**Valore**: chiarisce che alcuni parametri si tarano solo con la produzione reale, evitando false certezze prima del go-live.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:637]`, `[DOC-INTERNO CAP_07_parte_VII.md:641]`.

### B7-R-38 — Regola di anticipo del ritraining su trigger di deriva
Il criterio dichiarato definisce che, se gli alert di Parte VI scattano in modo persistente su almeno uno di quattro trigger paralleli (deriva fitness; deriva $f_5^{live}$; break parametrico EGARCH; frequenza emissione fuori range), il ciclo di ritraining è **anticipato** rispetto alla cadenza pianificata, via Regola 2 di sostituzione del bundle; il bundle non si riottimizza in produzione ma si sostituisce con un nuovo bundle frozen.
**Valore**: garantisce che il segnale resti aggiornato quando il mercato cambia, senza alterare in produzione un bundle congelato (coerenza con immutabilità).
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:645]`, `[DOC-INTERNO CAP_07_parte_VII.md:647-654]`, `[DOC-INTERNO CAP_07_parte_VII.md:656]`.

### B7-NFR-03 — Latenza qualitativa del canale Telegram $L_{max}=30$ s (provvisoria; misura empirica PENDING)
Il criterio dichiarato pone come obiettivo qualitativo della catena ingest-feature-inference-Telegram una latenza end-to-end entro $L_{max}=30$ s (**valore di lavoro provvisorio, non congelato in Parte VII, riconsiderato post-go-live**), componente di B7-R-34. La **verifica numerica empirica** di $L_{max}$ effettivo su bot reale resta carryover di Appendice E (M-2 OPEN) → **PENDING-empirico**, mai asserita verificata qui.
**Valore**: fissa un'aspettativa di tempestività del segnale per l'operatore mobile, distinguendo l'obiettivo dichiarato dalla sua misura (rinviata).
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:23]`, `[DOC-INTERNO CAP_07_parte_VII.md:592]`. M-promemoria: M-2 OPEN (CARRYOVER, Appendice E).

### B7-NFR-04 — Compute budget del post-processing di Parte VII
Il criterio dichiarato stabilisce che il post-processing di Parte VII (PBO + bootstrap) assorbe **al massimo ~15% del compute budget** (PBO ~1% per $S=12$, fino a ~10% per $S=16$; bootstrap <5%), e che il bootstrap $B=2.000$ gira su istanza cloud (non in locale) come post-processing del walk-forward, entro $T_{budget}=80$h wall-clock.
**Valore**: garantisce che i gate statistici non facciano esplodere costo/tempo del ciclo di validazione, mantenendo sostenibile il retraining trimestrale/semestrale.
**Fonte**: `[DOC-INTERNO CAP_07_parte_VII.md:439]`, `[DOC-INTERNO CAP_07_parte_VII.md:441]`.

---

## 9. Matrice di tracciabilità, nota di rinvio, lista PENDING-empirico, nota RM-3

### 9.1 Matrice di tracciabilità (`B7-*` → capitolo:riga + valore)

| ID | Materia | Fonte (capitolo:riga) | Mappa al criterio del metodo | Valore (operatore/sistema) |
|----|---------|------------------------|------------------------------|-----------------------------|
| B7-R-01 | Metrica primaria $E[R_{net}\mid executed]$ | CAP_01_parte_I.md:71 | Cap.5 metrica primaria | redditività attesa netta confrontabile |
| B7-R-02 | Conversione lordo→netto ($-2c$, $c=1$ pt) | CAP_01_parte_I.md:73-75 | Cap.5 commissioni | successo misurato dopo commissioni |
| B7-R-03 | Metriche di lifecycle | CAP_01_parte_I.md:77 | Cap.5 lifecycle | visibilità sul ciclo del segnale |
| B7-R-04 | Metriche di rischio (CVaR/MDD/MAE/MFE) | CAP_01_parte_I.md:79 | Cap.5 rischio | rischio di coda e drawdown |
| B7-R-05 | Metriche anti-overfitting (DSR/PBO) | CAP_01_parte_I.md:81 | Cap.5 anti-overfit | protezione da overfitting |
| B7-R-06 | Dichiarazione di successo per go-live | CAP_01_parte_I.md:85 | Cap.5 dichiarazione | condizione complessiva di pubblicazione |
| B7-CN-01 | Confine successo-segnale vs operatore | CAP_01_parte_I.md:69, :85 | Cap.5 confine | valutazione corretta del motore |
| B7-NFR-01 | Fonte canonica = replay bit-exact | CAP_07_parte_VII.md:21, :7 | Cap.31.1 | riproducibilità/audit |
| B7-CN-02 | Vincolo "solo emissione" | CAP_07_parte_VII.md:21 | Cap.31.1 | coerenza perimetro segnali |
| B7-R-07 | Finestra OOS aggregata + purge/embargo | CAP_07_parte_VII.md:15-19 | Cap.31.1 | anti-leakage |
| B7-R-08 | Selezione deterministica lessicografica | CAP_07_parte_VII.md:29 | Cap.31.2 | bundle riproducibile |
| B7-R-09 | Filtro 1 DSR | CAP_07_parte_VII.md:31 | Cap.31.2 F1 | scarto segnali non significativi |
| B7-R-10 | Filtro 2 PBO | CAP_07_parte_VII.md:33 | Cap.31.2 F2 | scarto segnali fragili |
| B7-R-11 | Filtro 3 $|f_5|$ cross-regime | CAP_07_parte_VII.md:35 | Cap.31.2 F3 | bilanciamento fra regimi |
| B7-R-12 | Filtro 4 $\text{IQR}_{norm}(f_1)$ | CAP_07_parte_VII.md:37 | Cap.31.2 F4 | stabilità nel tempo |
| B7-R-13 | Filtro 5 $\pi_{t_2\mid t_1}$ | CAP_07_parte_VII.md:39 | Cap.31.2 F5 | qualità del target |
| B7-R-14 | Selezione finale + tie-break | CAP_07_parte_VII.md:41, :43-46 | Cap.31.2 | determinismo a parità |
| B7-R-15 | Fallimento go-live a selezione | CAP_07_parte_VII.md:50 | Cap.31.2 | nessun segnale se nessun bundle valido |
| B7-R-16 | Definizione DSR | CAP_07_parte_VII.md:139, :143 | Cap.32.1 | significatività al netto delle prove |
| B7-R-17 | Soglia $\theta_{DSR}=0,95$ provvisoria | CAP_07_parte_VII.md:202, :204, :244 | Cap.32.4 | asticella di significatività |
| B7-R-18 | Definizione PBO/CSCV 6 passi | CAP_07_parte_VII.md:252, :254 | Cap.33.1 | misura fragilità |
| B7-R-19 | Regola $S=2F$ | CAP_07_parte_VII.md:294-298, :322 | Cap.33.2 | partizioni riproducibili |
| B7-R-20 | Soglia $\theta_{PBO}=0,50$ provvisoria | CAP_07_parte_VII.md:304, :308, :344 | Cap.33.3 | soglia di fragilità tollerata |
| B7-R-21 | Procedura bootstrap stazionario | CAP_07_parte_VII.md:352, :354-356, :358 | Cap.34.1 | IC che rispettano dipendenza temporale |
| B7-R-22 | $B=2.000$ replicazioni + percentile | CAP_07_parte_VII.md:359, :379-381, :449 | Cap.34.3 | IC stabili nel budget |
| B7-R-23 | Calibrazione $L_{avg}$ Politis-White, $L_{avg}=10$ provv. | CAP_07_parte_VII.md:369, :371, :373, :449 | Cap.34.2 | block length adattiva |
| B7-NFR-02 | Replay bit-exact bootstrap (seed dedicato) | CAP_07_parte_VII.md:445, :447 | Cap.34.5 | IC riproducibili al bit |
| B7-CN-03 | Bundle frozen immutabile (6 elementi) | CAP_07_parte_VII.md:457, :459, :461-466, :483-500 | Cap.35.1 | artefatto congelato unico |
| B7-CN-04 | Hash SHA-256 di riferimento | CAP_07_parte_VII.md:506, :509-510 | Cap.35.2 | impronta univoca/integrità |
| B7-CN-05 | Validazione integrità all'avvio | CAP_07_parte_VII.md:512-517 | Cap.35.2 | rifiuto bundle corrotto |
| B7-R-24 | Regola di sostituzione bundle (4 regole) | CAP_07_parte_VII.md:523, :525, :533 | Cap.35.3 | continuità servizio + tracciabilità |
| B7-R-25 | Go-live 1: DSR | CAP_07_parte_VII.md:570 | Cap.36.1 AC-GO-1 | significatività esplicita al go-live |
| B7-R-26 | Go-live 3: $E[R_{net}]>0$ con IC bootstrap | CAP_07_parte_VII.md:574 | Cap.36.1 AC-GO-3 | redditività netta distinta da zero |
| B7-R-27 | Go-live 2: PBO | CAP_07_parte_VII.md:572 | Cap.36.1 AC-GO-2 | non-fragilità esplicita al go-live |
| B7-R-28 | Go-live 4: $|f_5|$ cross-regime | CAP_07_parte_VII.md:576 | Cap.36.1 AC-GO-4 | bilanciamento fra regimi |
| B7-R-29 | Go-live 5: $\text{IQR}_{norm}(f_1)$ | CAP_07_parte_VII.md:578 | Cap.36.1 AC-GO-5 | stabilità nel tempo |
| B7-R-30 | Go-live 6: CVaR $>\theta_{CVaR}=-100$ pt provv. | CAP_07_parte_VII.md:580 | Cap.36.1 AC-GO-6 | limite perdita di coda |
| B7-R-31 | Go-live 7: MDD $<\theta_{MDD}=200$ pt provv. | CAP_07_parte_VII.md:582 | Cap.36.1 AC-GO-7 | limite drawdown intraday |
| B7-R-32 | Go-live 8: $r_{emit}\in[0,2;5]$ | CAP_07_parte_VII.md:584 | Cap.36.1 AC-GO-8 | frequenza adatta a esecuzione manuale |
| B7-R-33 | Go-live 9: $\rho_{sessions}>0,60$ provv. (target asimm.) | CAP_07_parte_VII.md:586, :609-625, :629-631 | Cap.36.1 AC-GO-9 + 36.2 | obiettivo operativo concreto |
| B7-R-34 | Go-live 10: pipeline (4 sotto-cond.) | CAP_07_parte_VII.md:588, :589-592 | Cap.36.1 AC-GO-10 | segnale recapitato all'operatore |
| B7-R-35 | Go-live 11: dashboard (3 sotto-cond.) | CAP_07_parte_VII.md:594, :595-597 | Cap.36.1 AC-GO-11 | monitoraggio post-go-live |
| B7-R-36 | Go-live 12: hash valido all'avvio | CAP_07_parte_VII.md:599 | Cap.36.1 AC-GO-12 | integrità al primo avvio |
| B7-CN-06 | Procedura GO/NO-GO deterministica | CAP_07_parte_VII.md:601, :602-605 | Cap.36.1 | decisione tracciabile + confine validator |
| B7-R-37 | Reporting calmo/turbolento (non gate) | CAP_07_parte_VII.md:633 | Cap.36.2 | visibilità dipendenza dal regime |
| B7-CN-07 | Carryover 10 parametri Parte VI | CAP_07_parte_VII.md:637, :641 | Cap.36.3 | tuning solo con produzione reale |
| B7-R-38 | Anticipo ritraining su deriva | CAP_07_parte_VII.md:645, :647-654, :656 | Cap.36.4 | segnale aggiornato al cambio mercato |
| B7-NFR-03 | Latenza $L_{max}=30$ s qualitativa | CAP_07_parte_VII.md:23, :592 | Cap.31.1/36.1 | tempestività del segnale (mobile) |
| B7-NFR-04 | Compute budget post-processing ≤~15% | CAP_07_parte_VII.md:439, :441 | Cap.33.4/34.4 | sostenibilità del retraining |

**Conteggio**: 49 requisiti totali — 38 `B7-R-*`, 7 `B7-CN-*`, 4 `B7-NFR-*`. (Nessun conteggio-target imposto; conteggio puramente descrittivo del prodotto.)

### 9.2 Nota di rinvio — premesse e out-of-scope

Le seguenti materie sono **premesse citate**, non ri-derivate in questo documento (vedi card §5):

- **Determinismo/replay bit-exact** — invariante premessa `CAP_02_parte_II.md` Cap.10; consolidato come invariante che la procedura OOS preserva (B7-NFR-01, B7-NFR-02), non ri-derivato.
- **Fronte di Pareto $\mathcal{F}_1$, NSGA-II, $f_1$-$f_5$, $\text{IQR}_{norm}$** — premessa Parte V (Cap.22-26); B7 consuma $\mathcal{F}_1$ e le metriche come input.
- **Walk-forward nested, purge/embargo, $W_{in}/W_{oos}/F$** — premessa Parte V (Cap.25); B7 cita la finestra OOS aggregata, non ri-deriva il walk-forward.
- **Modello EGARCH / regime calmo-turbolento** — premessa Parte III (Cap.14); usato per il reporting separato di sessione.
- **Pipeline di inference (Cap.27), layout Telegram (Cap.29), dashboard+alert (Cap.30)** — premessa Parte VI; oggetto di verifica di B7-R-34/B7-R-35 e della regola di anticipo ritraining, non ri-specificati. **Cap.30 è oggetto-citato, NON fonte di alcun `B7-*`**: la fonte di B7-R-35 è Cap.36 (`CAP_07_parte_VII.md:594-597`).
- **Submachine post-target_1 ($\pi_{t_2\mid t_1}$, MFE/MAE)** — premessa Parte II (Cap.11); usata in B7-R-13 e nelle metriche di rischio.
- **Target operativo asimmetrico (500 pt / 70% strutturale), pivot detection** — premessa Cap.1 di Parte I + Parte III (Cap.15); B7 cita la soglia di B7-R-33, non ri-deriva l'algoritmo pivot.

Out-of-scope (vedi card §6): risultati numerici/verdetti GO-NO-GO/valori d'edge effettivi → FASE-D/validator; monitoraggio di produzione in esercizio → FASE-D; implementazione/codice → FASE-D; matematica interna delle formule → CAP chiusi; congelamento empirico delle soglie → post-go-live/FASE-D; schema-dato/DAPI → B5/B6; esecuzione ordini → B5/compliance; fasizzazione/chiusura della spec → B8.

### 9.3 Lista PENDING-empirico (marcata, MAI asserita)

Tutte le grandezze d'esito/edge seguenti sono **PENDING-empirico (validator / FASE-D)**:

1. Valore di $DSR(\theta^*)$ effettivo → validator. (B7 consolida solo $\theta_{DSR}=0{,}95$ come criterio.)
2. Valore di $PBO(\theta^*)$ effettivo → validator. (Criterio: $\theta_{PBO}=0{,}50$.)
3. $E[R_{net}\mid executed]$ effettivo e $IC_{95\%}$ bootstrap (B7-R-26) → validator.
4. $\text{CVaR}_{95\%}$, $\text{MDD}_{intraday}$, $r_{emit}$, $\rho_{sessions}$ effettivi (B7-R-30/31/32/33) → validator.
5. Esito dei 12 criteri di go-live e decisione GO/NO-GO (B7-R-25..36, B7-CN-06) → validator. (B7 consolida checklist e procedura.)
6. Esito funzionale di B7-R-34/35/36 (pipeline/dashboard/hash operativi al go-live) → FASE-D.
7. Latenza $L_{max}=30$ s effettiva del canale Telegram (B7-NFR-03) → carryover Appendice E, M-2 OPEN.
8. $F$ effettivo (fold completati, $\{6,7,8\}$ atteso) → dipende dal run di training; B7 consolida la procedura parametrica in $F$ ($S=2F$), non un $F$ specifico.
9. Valore effettivo di $L_{avg}$ calibrato via Politis-White (B7-R-23) → validator.

**NON pending** (criteri/definizioni dichiarati, consolidati col loro stato esatto): definizioni di DSR/PBO/bootstrap; procedura OOS e 6 filtri; regola $S=2F$; $B=2.000$; i 12 criteri di go-live come criteri binari; le soglie come **valori di lavoro provvisori non congelati, riconsiderati post-go-live**; specifica di immutabilità del frozen bundle; definizione operativa del successo (Cap.5).

### 9.4 Nota RM-3 — gerarchia delle fonti

Tutte le asserzioni fattuali di questo documento sono **richiami** a capitoli metodologia v2 chiusi PASS, etichettati `[DOC-INTERNO CAP_07_parte_VII.md:NNN]` / `[DOC-INTERNO CAP_01_parte_I.md:NNN]`. I paper esterni citati (Bailey-López de Prado 2014; Bailey-Borwein-López de Prado-Zhu 2017; Politis-Romano 1994; Politis-White 2004; Efron 1987) sono **riferimenti bibliografici dei capitoli**, non fonti di prima istanza di questo documento; sono etichettati `[WIKI-HINT, da verificare]` dove citati. Nessuna conclusione strutturale poggia su una fonte di solo livello 4. Nessuna nuova dichiarazione "verificato X" è introdotta (RM-1): le grandezze misurabili sono marcate PENDING-empirico, non verificate.
