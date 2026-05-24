### REPORT SUPERVISORE — CAP-04
**Task**: Parte IV del documento metodologico v2 (Geometria zone, target strutturali, survival)
**Stato**: COMPLETATO
**Iterazione**: v1
**Commit documento**: `64a31aa [CAP-04 v1] Parte IV ...`
**Commit presente**: `[CAP-04 v1 fix] REPORT_CAP_04 + commit ACTIVE_TASK CAP-04 (omissioni Iterazione 1)`

---

#### Cosa è stato prodotto

| File | Stato | Righe | Note |
|------|-------|-------|------|
| `docs/methodology_v2/CAP_04_parte_IV.md` | Creato (commit 64a31aa) | 517 | Parte IV completa: Cap.16–21 |
| `docs/methodology_v2/00_indice.md` | Aggiornato (commit 64a31aa) | — | Voce Parte IV aggiunta |
| `reports/REPORT_CAP_04.md` | Creato (questo commit) | — | Omesso in commit 64a31aa |
| `tasks/ACTIVE_TASK.md` | Committato (questo commit) | 223 | Omesso in commit 64a31aa |

---

#### Ipotesi di partenza

Senza la Parte IV, il GA ottimizza un cromosoma che parametrizza gradi di libertà senza dominio formale:
non sa dove costruire la zona (nessun algoritmo di ancoraggio a pivot), non sa come selezionare
target e stop dalla struttura del prezzo, non ha una stima probabilistica del successo del segnale.
La Parte IV fornisce al GA il dominio geometrico su cui operare (b, d_inv, d_obsolete, T_min_session,
k_t2, d_stop_sigma, tau_surv) e il meccanismo di scoring probabilistico (p_hat_hit) che la fitness
di Parte V consuma per distinguere segnali strutturalmente solidi da segnali casuali.

**Impatto sul comportamento del GA:**

- **Prima di CAP-04**: il GA non aveva un dominio geometrico formale. I parametri relativi a entry,
  target e stop erano impliciti o non definiti. La fitness non aveva p_hat_hit come input.
- **Dopo CAP-04**: il GA ha 9 parametri geometrici/probabilistici esplicitamente definiti nel dominio
  (b, d_inv, d_obsolete, T_min_session, k_t2, d_stop_sigma o le varianti regime, tau_surv o le varianti
  regime). Il modello di survival produce p_hat_hit come filtro di emissione e potenziale componente
  della fitness. I cromosomi non validi (d_stop <= b) sono identificati e scartati prima di entrare
  nella popolazione.

---

#### Misura prima/dopo

| Metrica | Prima (pre-CAP-04) | Dopo (post-CAP-04) | Delta |
|---------|-------------------|-------------------|-------|
| Dominio di b (semi-ampiezza zona) | N/D (non formalizzato) | {5,10,15,20,25,30,35,40} pt FIB | Definito |
| Algoritmo p_ref da pivot | N/D | p_ref = max(P_low) per long, min(P_high) per short | Definito |
| Gestione warm-up strutturale | N/D | Sospensione emissione se P_low=∅ o P_high=∅ | Definito |
| Selezione target_1 | N/D | min(T+_80) per long (primo pivot >= 80pt da p_ref) | Definito |
| Selezione target_2 | N/D | min(T+_2) o fallback sintetico con k_t2 | Definito |
| Algoritmo stop strutturale | N/D | max(S-_low) con fallback sigma * d_stop_sigma | Definito |
| Cromosomi non validi per d_stop<=b | Non rilevabili (no dominio) | Identificati e scartati (Cap.18.2) | Definito |
| Modello survival (stima p_hat_hit) | N/D | Cox cause-specific hazard, Fine-Gray come benchmark | Definito |
| Filtro emissione survival-based | N/D | E_surv = I[p_hat_hit >= tau_surv], AND con Cap.8 | Definito |
| Classificazione trade_range | N/D | 4 condizioni deterministiche (A_range, prezzo, osc, breakout) | Definito |
| Feature aggiuntiva trade_range | N/D | x^(A_range) = A_range / sigma_pt | Definito |

*Tutte le metriche erano N/D prima di CAP-04: la Parte IV è un capitolo fondativo, non un miglioramento*
*di qualcosa di esistente. Il criterio di rollback è pertanto definito su errori formali, non su delta.*

---

#### Verifica esplicita degli Acceptance Criteria

| AC-ID | Criterio | Esito | Evidenza (Cap. o formula) |
|-------|----------|-------|--------------------------|
| S-1 | I 6 capitoli (Cap.16–21) presenti, completi, nell’ordine corretto | OK | Struttura lineare Cap.16–21 nel documento |
| S-2 | Tutte le 19 eredità citate esplicitamente (7 CAP-01 + 6 CAP-02 + 6 CAP-03) | PARZIALE | 18/19 con cross-ref esplicito. Eredità n.19 (T_warmup_EMA=74 barre, Cap.15.2.1 CAP-03): trattata sostanzialmente in Cap.16.2 (il vincolo più stringente tra T_warmup_EMA e T_warmup_norm), ma il cross-ref ‘Cap.15.2.1 di Parte III’ non appare letteralmente nel testo. Il concetto è presente e corretto; il link bibliografico esplicito manca. |
| S-3 | Paragrafo finale con lista parametri provvisori e rinvio Parte V | OK | Tabella 12 righe ‘Riepilogo parametri provvisori della Parte IV’ (righe 497–512) |
| C16-1 | p_ref derivato da pivot con algoritmo esplicito | OK | Cap.16.1: p_ref = max(P_low) per long, min(P_high) per short; criteri di selezione deterministici |
| C16-2 | Trattamento warm-up (nessun pivot confermato nella sessione) dichiarato esplicitamente (M-1 v2 CAP-03) | OK | Cap.16.2: regola di sospensione se P_low=∅ o P_high=∅; nessun fallback a sessione precedente |
| C16-3 | Banda b in {5,...,40} pt FIB come parametro del cromosoma, con cardinalità (2b/5)+1 | OK | Cap.16.3: formula entry_zone, cardinalità (2b/5)+1, 2 esempi numerici con tick 5pt |
| C16-4 | Condizione di raw touch formalizzata in termini di OHLC barra 1-min | OK | Cap.16.4: low_t <= p_ref+b e high_t >= p_ref-b; valutata da t_emission+1 |
| C16-5 | Condizioni di invalidazione strutturale pre-touch definite, parametri dichiarati provvisori | OK | Cap.16.5: I1 (stop pre-touch), I2 (d_inv, parametro cromosoma), I3 (d_obsolete, parametro cromosoma) |
| C16-6 | Condizione T_min_session dichiarata con parametro provvisorio | OK | Cap.16.6: T_residuo >= T_min_session, floor 15 min provvisorio, parametro cromosoma |
| C16-7 | Coerenza esplicita con fill virtuale worst-case Cap.12.4 CAP-03 | OK | Cap.16.4: fill al bordo superiore per long, inferiore per short; cross-ref Cap.12.4 |
| C17-1 | Algoritmo di selezione target_1 dal catalogo pivot strutturali | OK | Cap.17.1: target_1 = min(T+_80) per long, max(T-_80) per short; caso insieme vuoto trattato |
| C17-2 | Vincolo |target_1 - p_ref| >= 80pt per setup directional | OK | Cap.17.2: insiemi T+_80 e T-_80 definiti formalmente; esempio numerico (tick 5pt) |
| C17-3 | Algoritmo selezione target_2 con |target_2| > |target_1| | OK | Cap.17.4: min(T+_2) per long; fallback sintetico target_1 + k_t2 * sigma_pt (arrotondato a multiplo 5) |
| C17-4 | Condizione sigma-units tau_dist^sigma richiamata con cross-ref Cap.8 Parte II | OK | Cap.17.3: formula esplicita con cross-ref Cap.8.2 Parte II |
| C17-5 | target_1 e target_2 multipli di 5 | OK | Garantito da pivot (prezzi OHLC FIB, tick 5pt); livello sintetico arrotondato al multiplo di 5 |
| C18-1 | Algoritmo di derivazione stop_loss dalla struttura del prezzo | OK | Cap.18.1: max(S-_low) per long, min(S+_high) per short; fallback sigma con d_stop_sigma |
| C18-2 | Vincolo d_stop > b obbligatorio con cross-ref Cap.6 Parte II | OK | Cap.18.2: verifica post-selezione, ricerca pivot più distante se violato; cross-ref Cap.2 PI + Cap.6.1 PII |
| C18-3 | Separazione esplicita stop strutturale vs stop personale operatore (Cap.11 Parte II) | OK | Cap.18.3: dichiarazione esplicita; cross-ref Cap.11 PII e punto 2 dichiarazione di intenti |
| C18-4 | RR = d_stop/d_target dichiarato come grandezza osservabile, vincolo rinviato Parte V | OK | Cap.18.4: formula RR, dichiarazione ‘eventuale floor esplicito materia di Parte V’ |
| C18-5 | Condizionalità al regime dichiarata (parametri stop regime-dipendenti opzionali) | OK | Cap.18.5: d_stop_sigma condizionale a R_t (calmo/turbolento), parametri cromosoma opzionali |
| C19-1 | Variabile obiettivo (tempo al primo evento terminale) formalizzata | OK | Cap.19.1: tau = durata dal fill all’evento terminale (target_1_hit, stopped, expired) |
| C19-2 | Competing risks (target_1_hit vs stopped) trattati esplicitamente | OK | Cap.19.1 e Cap.19.2: competing risks dichiarati; cause-specific hazard per j=1,2 |
| C19-3 | Formulazione matematica modello candidato primario (Cox, Weibull, o survival forest) | OK | Cap.19.2: h_j(tau|x,T_res) = h_0j(tau) * exp(beta_j^T x + gamma_j * T_res); Fine-Gray citato |
| C19-4 | Feature input: sottoinsieme 37 feature causali normalizzate, selezione rinviata Parte V/VII | OK | Cap.19.3: x tilde in F_{t-1}, normalizzate MAD, selezione rinviata; dimensionalità massima congelata PV |
| C19-5 | Calibrazione fold-per-fold, coerente con Cap.13.3 CAP-03 | OK | Cap.19.4: fold-per-fold; cross-ref Cap.13.3 Parte III; stima Breslow; seed per determinismo |
| C19-6 | Censoring a destra per segnali expired senza hit né stop | OK | Cap.19.4: segnali expired censurati a tau_i = Delta_t_cromosoma; nota su informativeness |
| C19-7 | Output p_hat_hit formalizzato come probabilità condizionata | OK | Cap.19.2: p_hat_hit = integrale CIF; Cap.19.5: output operativo 1 e 2 |
| C19-8 | Determinismo e causalità (F_{t-1}) dichiarati | OK | Cap.19.5: x tilde in F_{t-1}; modello frozen; due esecuzioni indipendenti = stesso p_hat_hit |
| C20-1 | Soglia tau_surv come parametro del cromosoma, provvisorio | OK | Cap.20.1: tau_surv in (0.1, 0.9), valore provvisorio 0.5, parametro cromosoma |
| C20-2 | Integrazione AND logico con condizioni Cap.8 Parte II | OK | Cap.20.2: E_vol AND E_liq AND E_dist^sigma AND E_80pt AND E_surv = vera |
| C20-3 | Condizionalità tau_surv al regime dichiarata | OK | Cap.20.3: tau_surv condizionale a R_t (calmo/turbolento), parametri cromosoma opzionali |
| C20-4 | Meccanismo di filtro implicito fine sessione via T_residuo descritto | OK | Cap.20.4: lim_{T_res -> 0} p_hat_hit = 0; filtro adattivo vs gate hard T_min_session |
| C21-1 | Definizione del range [p_low, p_high] da pivot strutturali | OK | Cap.21.1: A_range = p_high - p_low, multiplo di 5; requisito A_range >= 80pt |
| C21-2 | Eccezione al filtro 80pt formalizzata: A_range >= 80pt | OK | Cap.21.1 e Cap.21.4: A_range >= 80pt sostituisce |target_1 - p_ref| >= 80pt |
| C21-3 | Zone di entry ai bordi del range, target al bordo opposto, stop fuori range | OK | Cap.21.3: p_ref = p_low (long) o p_high (short); Cap.21.4: target_1 = p_high (long) o p_low (short) |
| C21-4 | Survival nel range: stessa architettura, feature aggiuntiva ampiezza range | OK | Cap.21.5: x^(A_range) = A_range / sigma_pt aggiunta al vettore x tilde |
| C21-5 | Regola algoritmica classificazione directional vs trade_range | OK | Cap.21.2: 4 condizioni deterministiche (A_range>=80pt, prezzo nel range, n_osc_min, no breakout recente) |
| T-1 | Tick FIB = 5pt rispettato in ogni formula, esempio numerico, livello strutturale | OK | Cap.16.3 (2 esempi), Cap.17.2 (esempio), Cap.18.2 (esempio), Cap.21.4 (esempio); tutti livelli multipli di 5 |
| T-2 | Determinismo bit-exact: ogni algoritmo e regola è deterministico (Cap.10 Parte II) | OK | Cap.16.1, 16.5, 17.1, 17.4, 18.1, 19.5: dichiarazioni esplicite di determinismo con cross-ref Cap.10 PII |
| T-3 | Causalità: nessuna grandezza usata al tempo t richiede dati dopo t-1 | OK | Cap.16.1, 19.3, 19.5: x tilde in F_{t-1}; pivot disponibili da t+n_c+1 |
| T-4 | Nessun parametro fissato definitivamente: tutti provvisori con rinvio Parte V | OK | Tabella riepilogo 12 parametri; dichiarazione iniziale della Parte IV |
| T-5 | Registro tecnico italiano formale, formule LaTeX inline e display | OK | Tutto il documento usa registro formale; formule in LaTeX $...$ e $$...$$ |
| T-6 | Citazioni scientifiche pertinenti inline nei capitoli | OK | Cap.19.2: Fine e Gray (1999) JASA; Cap.19.4: Grambsch e Therneau (1994) Biometrika |
| T-7 | REPORT_CAP_04.md include sezione ‘Misura prima/dopo’ con impatto sul GA | OK | Questo documento, sezione ‘Misura prima/dopo’ (11 righe tabella) |

**Conteggio finale AC: 40 OK, 1 PARZIALE (S-2), 0 MANCA su 41 totali.**

**Nota S-2 (PARZIALE)**: L’eredità n.19 (T_warmup_EMA = 74 barre, Cap.15.2.1 di Parte III) è trattata
sostanzialmente in Cap.16.2: il testo dichiara che il vincolo più stringente tra warm-up strutturale
e warm-up normalizzazione determina la prima barra ammissibile per l’emissione, richiamando
T_warmup_norm = 100 barre (il più stringente dei due). Il concetto di T_warmup_EMA = 74 barre come
fonte dell’eredità è presente nella lista delle eredità del task (n.19) e il suo effetto è catturato
correttamente, ma il cross-ref esplicito ‘Cap.15.2.1 di Parte III’ non appare nel testo del Cap.16.2.
Si tratta di un’omissione di link bibliografico, non di un errore concettuale.

---

#### Decisioni rilevanti prese durante lo sviluppo

| D-ID | Decisione | Motivazione |
|------|-----------|-------------|
| D-1 | p_ref = pivot più recente (max P_low per long, min P_high per short), senza fallback a sessione precedente | Motivazione strutturale: pivot sessione corrente = informazione più aggiornata; no fallback coerente con condizione 4 dell’algoritmo frattale (finestra nella sessione). Richiesto da M-1 v2 CAP-03. |
| D-2 | Cox cause-specific hazard come modello primario, Fine-Gray come benchmark | Interpretabilità dei coefficienti beta_j (log-hazard ratio causa-specifica) preferibile per supervisore; Fine-Gray più diretto per stima CIF ma meno interpretabile. Benchmark rinviato a Parte V. |
| D-3 | 4 condizioni deterministiche per classificazione trade_range (A_range, prezzo nel range, n_osc_min, no breakout) | Robustezza: la sola condizione di ampiezza sarebbe insufficiente a classificare un range ‘attivo’. Le 4 condizioni riducono falsi positivi (pivot lontani nel tempo che non identificano un range corrente). |
| D-4 | Flag target_2_type in {structural, synthetic} e stop_type in {structural, synthetic} nel payload | Trasparenza operativa: l’operatore riceve informazione sulla natura del livello. Rilevante per la validazione delle metriche di lifecycle in Parte VII. |
| D-5 | Filtro implicito di fine sessione via T_residuo (Cap.20.4) senza soglia oraria esplicita | Adattività: il filtro dipende dalla struttura del segnale (distanza target/stop) e dal contesto (regime, volatilità), non da un orario fisso. Complementare al gate hard T_min_session di Cap.16.6. |
| D-6 | Censoring informativo dichiarato esplicitamente (Cap.19.4) | Il timer Delta_t_cromosoma è un parametro del cromosoma, non un evento casuale: il censoring non è non-informativo per costruzione. La nota richiede verifica in Parte V (test di dipendenza tra Delta_t e feature). |
| D-7 | x^(A_range) = A_range / sigma_pt come feature aggiuntiva del survival per trade_range | Normalizzazione coerente con il catalogo (feature già in sigma-units). Porta il catalogo a 38 feature per il caso trade_range (37 + 1 feature specifica), ma non modifica formalmente il catalogo di Parte III che rimane a 37. |

---

#### M-promemoria: carryover verso Parte V, VI, VII

I seguenti M-ID erano già presenti nel task e rimangono invariati come carryover:

| M-ID | Origine | Destinazione | Nota |
|------|---------|-------------|------|
| M-2 | Review v1 CAP-02 | Appendice E | Latenza Telegram L_max=30s |
| M-4 | Review v4 CAP-01 | Parte V (Cap.23) | Tasso rimpiazzo NSGA-II |
| M-5 | Q-06 / C-4.3 | Parte V (Cap.25) | Benchmark rolling vs EWMA |
| M-6 | Q-09 / C-7.3 | Parte V (Cap.25/26) | Classificazione regime media vs mediana |
| N-1 (v2) | Review v2 CAP-03 | Parte V (Cap.24) | Asimmetria stopped vs target_hit |
| N-2 (v1) | Review v1 CAP-02 | Parte VII | Netto non registrato nel log di chiusura |
| N-3 (v1) | Review v1 CAP-02 | Parte V/VI | executable_rate nomenclatura |
| N-4 (v2) | Review v2 CAP-02 | Parte V | Delta_t pre-trigger non esplicitato come campo |
| N-5 (v2) | Review v2 CAP-02 | Parte V | Floor tau_vol_low (congelamento) |
| M-2 (v2 CAP-03) | Review v2 CAP-03 | Parte V/VI | Cadenza ricalibrazione EGARCH in production |

Nuovi M-ID generati da CAP-04 (carryover verso Review e Parte V/VI/VII):

| M-ID | Generato da | Contenuto | Destinazione |
|------|------------|-----------|-------------|
| M-7 | Cap.19.4 nota censoring | Verifica assunzione non-informativeness del censoring: test di dipendenza tra Delta_t_cromosoma e feature di survival in Parte V | Parte V (Cap.25/26) |
| M-8 | Cap.19.2 benchmark | Confronto empirico Cox cause-specific vs Fine-Gray come test di robustezza su dati Portara/CQG | Parte V (Cap.25) |
| M-9 | Cap.19.4 diagnostica | Test di Schoenfeld fold-per-fold: se PH assumption sistematicamente violata, estendere a hazard non proporzionali | Parte V (Cap.25) |
| M-10 | Cap.19.3 dimensionalità | Dimensionalità massima del vettore x_tilde del survival: parametro da congelare in Parte V per evitare overfitting del survival sul cromosoma | Parte V (Cap.23/25) |
| M-11 | Cap.19.2 regime | Scelta tra stratificazione per regime (modelli separati) e singolo modello con indicatore regime come feature: benchmark in Parte V | Parte V (Cap.25) |
| M-12 | D-4 questo report | target_2_type e stop_type: decidere se entrano nel payload formale (Cap.6.1 CAP-02) o solo nel log di emissione | Parte II (Q aperta) o Parte V |
| M-13 | D-7 questo report | x^(A_range) = A_range/sigma_pt: il catalogo di Parte III resta a 37 feature; per trade_range il survival usa 38. Verificare se il catalogo va formalmente esteso a 38 o se la feature rimane implicita nella variante trade_range | Parte III (Q aperta) o Parte V |

---

#### Domande aperte per il Planner

1. **M-12 — target_2_type e stop_type nel payload formale**: La Parte IV introduce le flag
   `target_2_type in {structural, synthetic}` e `stop_type in {structural, synthetic}` come campi
   informativi del log di emissione. Il payload formale $\mathcal{S}$ di Cap.6.1 di Parte II non le
   include esplicitamente. Va aggiornato il payload in Parte II (richiederebbe un fix di CAP-02)
   o si accettano come campi del log non-formali fino a Parte V/VII?

2. **M-13 — catalogo feature: 37 o 38?**: Il catalogo di Cap.15.2 di Parte III conta 37 feature
   causali. La feature $x^{(A_{range})} = A_{range}/\hat{\sigma}_{\text{pt}}$ introdotta in Cap.21.5
   di Parte IV è una feature aggiuntiva specifica del caso trade_range. Il catalogo formale va
   esteso a 38 feature con nota ‘opzionale per trade_range’, oppure rimane a 37 con la feature
   come appendice implicita della variante?

---

#### Criterio di rollback

- **Rollback totale** (tornare a versione pre-CAP-04 e riscrivere): >= 3 AC con esito MANCA,
  oppure errore matematico nelle formule del survival (h_j, S_hat, p_hat_hit) con impatto sulla
  stima di probabilità del segnale.
- **Rollback parziale** (correzione chirurgica del capitolo interessato): 1 AC con esito MANCA
  con impatto sul comportamento del GA (es. vincolo d_stop > b non verificato, algoritmo p_ref
  non deterministico).
- **Non rollback** (correzione editoriale): AC PARZIALE su cross-reference bibliografico (come S-2),
  imprecisioni di notazione senza impatto algoritmico, testo non formale senza impatto su formule.