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

---

## Iterazione 2 — risposta ai finding di Review v1 + decisioni PROMEMORIA

**Origine**: Review v1 di CAP-04 ha emesso verdetto **CONDITIONAL** (commit oggetto `64a31aa` + `a1de0a8`, file `reviews/REVIEW_CAP_04_review.md`). Decisione supervisore 2026-05-24: BUG REALI obbligatori (NB-1 + NB-2) + tutti i PROMEMORIA approvati (O-3, O-4, O-5, O-6). I due NEUTRO (O-1 cross-ref Cap.15.2.1; O-2 tie-break arrotondamento target_2 sintetico) restano carryover di documentazione interna e non sono affrontati in v2. Le decisioni di design per chiudere i PROMEMORIA sono state prese dall'Orchestratore in assenza di Planner attivo in questa sessione e sono dichiarate esplicitamente nei fix qui sotto.

### Sintesi finding → fix v2

| Finding | Classificazione | Azione applicata | File:posizione | AC chiuso |
|---------|-----------------|------------------|----------------|-----------|
| **NB-1** | BUG REALE | Cap.16.1 di CAP-04 riscritto: formula con **criterio temporale unico** $p_{ref}(t) = \mathrm{level}(\arg\max_{p \in \mathcal{P}_{low}(t)} \tau_{conf}(p))$ per long e simmetrico per short; rimossa contraddizione formula vs testo; aggiunto razionale del criterio temporale, determinismo della selezione (algoritmo frattale conferma 1 pivot/barra), esempio numerico con due pivot low | `docs/methodology_v2/CAP_04_parte_IV.md:19-30` | AC-v2-1 |
| **NB-2** | BUG REALE | Cap.21.2 di CAP-04 esteso con **definizione algoritmica formale di oscillazione**: crossing completo del range con tolleranza $\epsilon = 5$ pt provvisoria, algoritmo deterministico e causale (single-pass su close fino a $t-1$), produce conteggio bit-exact; aggiunto esempio numerico con range $[27.400, 27.500]$ e $n_{osc}=2$. Aggiunta riga $\epsilon$ alla tabella riepilogo parametri provvisori | `docs/methodology_v2/CAP_04_parte_IV.md:464-472` + riga `\epsilon` in tabella parametri provvisori finale | AC-v2-2 |
| **O-3 / M-12** | PROMEMORIA approvato | **Mini-patch CAP-02 Cap.6.1**: aggiunta dei campi `target_2_type` $\in \{\text{structural}, \text{synthetic}\}$ e `stop_type` $\in \{\text{structural}, \text{personal}\}$ alla tupla $\mathcal{S}$; descrizione testuale dei due campi con popolamento deterministico. Cross-reference esplicito in CAP-04 Cap.17.4 (target_2_type) e Cap.18.1/18.3 (stop_type sempre `structural` dal motore, `personal` segnaposto formale) | `docs/methodology_v2/CAP_02_parte_II.md:19,37,52`; `docs/methodology_v2/CAP_04_parte_IV.md:197,231,260` | AC-v2-3 |
| **O-4 / M-13** | PROMEMORIA approvato | Cap.21.5 di CAP-04 riscritto come **estensione locale del catalogo**: $x^{(A_{range})}$ dichiarata feature condizionale attiva solo quando il setup è classificato trade_range; catalogo globale del cromosoma resta 37 (CAP-03 invariato) | `docs/methodology_v2/CAP_04_parte_IV.md:524` (paragrafo "Estensione locale del catalogo") | AC-v2-4 |
| **O-5 / M-7** | PROMEMORIA approvato | Cap.19.4 di CAP-04 esteso con: (i) dichiarazione formale dell'assunzione di censoring non-informativo $T_j \perp\!\!\!\perp C \mid \tilde{\mathbf{x}}_t$ con razionale strutturale (timeout di sessione fissato dall'orario di chiusura, non dal prezzo); (ii) rinvio formale a Parte V con metodi nominati: **test sui residui di Cox-Snell** [Cox e Snell 1968] e **diagnostica di Schoenfeld stratificata per evento vs censoring** [Grambsch-Therneau 1994] | `docs/methodology_v2/CAP_04_parte_IV.md:363-377` | AC-v2-5 |
| **O-6** | PROMEMORIA approvato | **Mini-patch CAP-02 Cap.6.1**: formulazione del filtro 80pt trade_range sincronizzata con Cap.5 PI come `$A_{range} = p_{high,range} - p_{low,range} \geq 80$ pt` in luogo della precedente `|target_1 - stop_loss| ≥ 80 pt`. Allineamento anche in Cap.8.2 (riga 209) | `docs/methodology_v2/CAP_02_parte_II.md:59-61,209` | AC-v2-6 |

### Decisioni di design ratificate dall'Orchestratore in assenza di Planner

| D-ID v2 | Decisione | Motivazione strutturale |
|---------|-----------|------------------------|
| D-v2-1 | $p_{ref}$ = pivot più recente per timestamp di conferma (criterio temporale unico, no criterio prezzo) | Reattività al regime corrente: pivot più recente = informazione strutturale più aggiornata; criterio unico elimina contraddizione formula vs testo (NB-1). Determinismo bit-exact garantito perché l'algoritmo frattale conferma 1 pivot per volta (no parità di timestamp possibile). |
| D-v2-2 | $\epsilon = 5$ pt (= 1 tick FIB) come tolleranza di prossimità ai bordi del range per il conteggio oscillazioni | Coerenza con il tick discreto del FIB; $\epsilon$ minimo strutturale (1 tick) evita falsi positivi su micro-rimbalzi. Vincolo strutturale $\epsilon < A_{range}/2$ dichiarato ammissibile in tutti i casi compatibili con A_range >= 80 pt. Congelamento empirico in Parte V. |
| D-v2-3 | `target_2_type` e `stop_type` campi obbligatori del payload formale Cap.6.1 PII (non solo del log) | Trasparenza informativa verso il consumer Telegram dell'operatore; il valore `synthetic` di target_2 deve essere visibile in lettura mobile per qualificare la natura del livello. Dominio `{structural, personal}` di stop_type allineato alla separazione di Cap.18.3 PIV (mai `personal` dal motore, `structural` sempre — `personal` riservato a registri esterni). |
| D-v2-4 | $x^{(A_{range})}$ come feature condizionale del catalogo, non 38-esima feature | Preserva coerenza con CAP-03 (catalogo 37 invariato); impedisce introduzione di rumore strutturale nel survival directional (range non esiste in directional → $x^{(A_{range})}$ sarebbe `NaN` o convenzionalmente 0, entrambi inquinanti). |
| D-v2-5 | Censoring non-informativo formalizzato come assunzione + metodi di verifica empirica nominati (Cox-Snell, Schoenfeld stratificato) rinviati a Parte V | L'assunzione è plausibile a priori per ragioni strutturali (orario di chiusura della sessione fissa, $\Delta t_{cromosoma}$ frozen sul fold), ma deve essere verificata empiricamente. Il rinvio a Parte V con metodi nominati elimina ambiguità su come la verifica avverrà. |
| D-v2-6 | Formulazione normativa 80pt: $A_{range} \geq 80$ pt (Cap.5 PI = riferimento normativo) | Cap.5 PI è il riferimento normativo del filtro 80pt; Cap.6.1 PII e Cap.21.1 PIV vi si allineano. La precedente formulazione `|target_1 - stop_loss| ≥ 80 pt` non era allineata con Cap.5 PI e poteva produrre interpretazioni divergenti nei setup trade_range con stop_loss molto distante. |

### Misura prima/dopo Iterazione 2

| Metrica del comportamento GA | v1 (post-Review v1) | v2 (Iterazione 2) | Delta |
|---|---|---|---|
| Algoritmo selezione $p_{ref}$ — implementazioni conformi distinte | 2 (criterio prezzo o criterio temporale, contraddizione tra riga 21 e riga 26) | 1 (criterio temporale unico, $\arg\max \tau_{conf}$) | Eliminata divergenza fra implementazioni; ranking dei cromosomi diventa bit-exact riproducibile |
| Definizione algoritmica di "oscillazione" nel range trade_range | Ambigua: testo informale "oscillazioni >= n_osc_min" senza algoritmo | Formale: single-pass deterministico su close, con $\epsilon$ tolleranza esplicita, esempio numerico | Determinismo bit-exact ripristinato per classificazione trade_range; impatto su sotto-popolazione trade_range del GA |
| Campi del payload $\mathcal{S}$ | 10 (signal_id, timestamp, direction, entry_zone, target_1, target_2, stop_loss, setup_class, $\Delta t_{cromosoma}$, $T_{touch}^{max}$) | 12 (+`target_2_type`, +`stop_type`) | +2 campi obbligatori del contratto; consumer Telegram può qualificare natura strutturale dei livelli |
| Dimensionalità catalogo cromosoma (regime directional) | Ambigua: 37 (CAP-03) vs 38 (CAP-04 v1 implicito) | Univoca: 37 directional + 1 condizionale solo per trade_range | Coerenza CAP-03/CAP-04 ristabilita; survival directional non riceve feature trade_range-specifica come predittore inutile |
| Assunzione censoring nel modello Cox cause-specific | Dichiarata informativa, verifica solo accennata | Dichiarata non-informativa con razionale strutturale + metodi di verifica empirica nominati (Cox-Snell, Schoenfeld) rinviati a Parte V | Specifica del modello survival completa; Parte V sa esattamente quali test eseguire |
| Coerenza formulazione 80pt fra Cap.5 PI e Cap.6.1 PII | Discrepante: `|target_1-stop_loss|` (PII) vs `A_range` (PI) | Coerente: `A_range >= 80 pt` in entrambi (Cap.5 PI = riferimento normativo) | Riduzione di una fonte di interpretazione divergente fra Parti I-II-IV |
| Parametri provvisori dichiarati nella tabella riepilogo CAP-04 | 12 | 13 (+$\epsilon$ tolleranza oscillazione) | Trasparenza completa dei parametri congelati in Parte V |
| Cromosomi non validi che producono ranking distorto via $p_{ref}$ ambiguo | Presenti in v1 (contraddizione) | Eliminati: regole deterministiche univoche per $p_{ref}$ e per `oscillazione` | Conversione signal-to-trade del GA basata su ranking riproducibile |

### Verifica esplicita degli Acceptance Criteria v2 (tabella onesta con evidenza file:riga)

| AC-ID | Criterio | Esito | Evidenza |
|-------|----------|-------|----------|
| AC-v2-1 | NB-1 chiuso. Cap.16.1 con formula criterio temporale (argmax timestamp); riga 26 invariata; esempio numerico aggiornato | **OK** | `docs/methodology_v2/CAP_04_parte_IV.md:19` (notazione $\tau_{conf}(p)$ introdotta), `:21` (formula long con $\arg\max_{p \in \mathcal{P}_{low}(t)} \tau_{conf}(p)$), `:22` (formula short simmetrica), `:26-28` (razionale temporale + determinismo della selezione), `:30` (esempio numerico 27.300/27.250 con $p_{ref}=27.250$) |
| AC-v2-2 | NB-2 chiuso. Definizione algoritmica esplicita di oscillazione (crossing completo) con $\epsilon = 5$ pt provvisoria; algoritmo deterministico + causale | **OK** | `docs/methodology_v2/CAP_04_parte_IV.md:464` (paragrafo introduttivo "Definizione algoritmica di oscillazione (chiusura NB-2 v2)"), `:466` (definizione tolleranza $\epsilon$, valore di lavoro 5 pt = 1 tick), `:468` (formalizzazione algoritmica con pseudocodice single-pass, deterministico, causale su close fino a $t-1$), `:472` (esempio numerico range $[27.400, 27.500]$ con $n_{osc}=2$) |
| AC-v2-3 | O-3 / M-12 chiuso. Payload $\mathcal{S}$ Cap.6.1 di CAP-02 con campi `target_2_type` e `stop_type`. Cap.17.4 e Cap.18.1/18.3 di CAP-04 con riferimento esplicito | **OK** | `docs/methodology_v2/CAP_02_parte_II.md:19` (tupla $\mathcal{S}$ con 12 campi: aggiunti `target_2_type` dopo `target_2` e `stop_type` dopo `stop_loss`), `:37` (descrizione `target_2_type` con dominio + popolamento deterministico + uso consumer Telegram), `:52` (descrizione `stop_type` con dominio + valore sempre `structural` per segnali del motore + razionale `personal`); `docs/methodology_v2/CAP_04_parte_IV.md:197` (Cap.17.4 cita esplicitamente il campo `target_2_type` del payload formale come destinazione deterministica della classificazione structural/synthetic), `:231` (Cap.18.1 nuovo paragrafo "Flag `stop_type` nel payload formale"), `:260` (Cap.18.3 conferma "payload pubblicato dal motore reca sempre `stop_type = structural`") |
| AC-v2-4 | O-4 / M-13 chiuso. $x^{(A_{range})}$ dichiarata feature condizionale al regime trade_range; catalogo globale Cap.15 CAP-03 invariato a 37 | **OK** | `docs/methodology_v2/CAP_04_parte_IV.md:524` (paragrafo "Estensione locale del catalogo causale — feature condizionale (chiusura O-4 / M-13 v2)" in Cap.21.5: "Il modello survival per il regime trade_range usa un'estensione locale del catalogo causale con la feature condizionale $x^{(A_{range})}$ [...] Il catalogo globale del cromosoma per il regime directional resta a 37 feature (Cap.15.2 di CAP-03 invariato)") |
| AC-v2-5 | O-5 / M-7 formalizzato. Cap.19.4 con dichiarazione esplicita censoring non-informativo + rinvio Parte V con metodi nominati (Cox-Snell, Schoenfeld stratificato) | **OK** | `docs/methodology_v2/CAP_04_parte_IV.md:363` (paragrafo "Assunzione di censoring non-informativo (chiusura O-5 / M-7 v2)" + formula $T_j \perp\!\!\!\perp C \mid \tilde{\mathbf{x}}_t$ con $j \in \{1,2\}$), `:371` (razionale strutturale a priori: orario di chiusura fissa + $\Delta t_{cromosoma}$ frozen su fold), `:377` (paragrafo "Metodi di verifica empirica rinviati a Parte V": Cox-Snell 1968 + Schoenfeld stratificato per evento vs censoring Grambsch-Therneau 1994) |
| AC-v2-6 | O-6 chiuso. Mini-patch CAP-02 Cap.6.1: formulazione 80pt allineata a Cap.5 PI (`A_range >= 80 pt`). REPORT_CAP_02 ha sezione "Iterazione 4" | **OK** | `docs/methodology_v2/CAP_02_parte_II.md:59` (formula display Cap.6.1: $A_{range} = p_{high,range} - p_{low,range} \geq 80$ pt), `:61` (testo esplicativo: "La formulazione è quella normativa di Cap.5 di Parte I [...] in luogo della precedente formulazione `|target_1 − stop_loss| ≥ 80 pt`"), `:209` (Cap.8.2 paragrafo "Il filtro 80 punti CAP-01 resta come vincolo assoluto" sincronizzato a `A_range`); `reports/REPORT_CAP_02.md` (sezione "Iterazione 4 — mini-patch Cap.6.1: flag payload + sincronizzazione 80pt" aggiunta in append in questo commit) |
| AC-v2-7 | Nessuna regressione su AC v1 originali (35 voci). Tabella prima/dopo dove rilevante | **OK** | I 6 capitoli Cap.16-21 restano nella stessa struttura; modifiche additive (NB-1, NB-2, O-3, O-4, O-5) o estensive (tabella parametri +1 riga). Nessun AC originale rimosso o violato. Vedi tabella "Misura prima/dopo Iterazione 2" sopra. |
| AC-v2-8 | `tasks/CARRYOVER.md` aggiornato: M-12, M-13, O-6 → `CLOSED-CAP-04`; M-7 resta `OPEN` Parte V; M-8...M-15 invariati `OPEN` | **OK** | `tasks/CARRYOVER.md:32` (M-12 → CLOSED-CAP-04 con dettaglio mini-patch), `:33` (M-13 → CLOSED-CAP-04 con dettaglio feature condizionale), `:27` (M-7 invariato OPEN), `:41` (O-6 CHIUSO Iterazione 4 di CAP-02 nella tabella storica) |
| AC-v2-9 | REPORT_CAP_04.md include sezione "Iterazione 2" con: per ogni finding/PROMEMORIA, modifica applicata + misura prima/dopo + AC chiuso | **OK** | Questo documento, sezione corrente "Iterazione 2 — risposta ai finding di Review v1 + decisioni PROMEMORIA" (tabella sintesi finding → fix, tabella decisioni di design, tabella misura prima/dopo, tabella AC v2 con evidenza file:riga) |
| AC-v2-10 | REPORT_CAP_02.md include sezione "Iterazione 4 — mini-patch Cap.6.1 (flag payload + sincronizzazione 80pt)" | **OK** | `reports/REPORT_CAP_02.md` (sezione "Iterazione 4 — mini-patch Cap.6.1: flag payload + sincronizzazione 80pt" aggiunta in append in questo commit) |
| AC-v2-11 | 00_indice.md aggiornato per riflettere stato corrente CAP-04 e CAP-02 (entrambi in revisione) | **OK** | `docs/methodology_v2/00_indice.md:15` (CAP-02 — IN REVIEW Iterazione 4), `:31` (CAP-04 — IN REVIEW v2 con dettaglio fix BUG REALI + PROMEMORIA) |
| AC-v2-12 | Tutti i file modificati committati e pushati. Working tree pulito sui file di task | **OK** | Vedi `git log` e `git status` post-commit (sezione "Operazioni git" qui sotto) |

**Conteggio finale AC v2: 12 OK, 0 PARZIALE, 0 MANCA su 12 totali.**

### Operazioni git

- Modifiche raccolte in commit `[CAP-04 v2 + CAP-02 patch4]` (vedi git log)
- Push su `origin/main` con prassi approvata del progetto
- Working tree pulito sui file di task post-commit; nessun "ahead of origin/main"

### Note al supervisore

1. **Decisioni di design ratificate dall'Orchestratore**: D-v2-1...D-v2-6 sono dichiarazioni di design fatte in assenza di Planner attivo in questa sessione, in coerenza con il task ricevuto. Il Reviewer le auditerà come tali; il supervisore può obiettare nel checkpoint successivo.
2. **D-v2-3 — domino `personal` di `stop_type`**: la decisione di mantenere `personal` come segnaposto formale del dominio (mai prodotto dal motore) è motivata dalla simmetria con la separazione Cap.18.3 PIV. Alternativa scartata: dominio ristretto a `{structural, synthetic}` (cioè `synthetic` analoga di target_2_type) — scartata perché Cap.18.1 di CAP-04 produce sia stop pivot sia stop sigma come `structural` (entrambi del motore), e la distinzione pivot vs sigma va nel log diagnostica non nel payload. Se il supervisore preferisce il dominio `{structural, synthetic}` per analogia con target_2_type, è un fix puntuale di 1 riga in CAP-02 + 1 in CAP-04.
3. **D-v2-2 — valore $\epsilon = 5$ pt**: 1 tick FIB è il minimo strutturale possibile; valori più larghi (es. $\epsilon = 10$ pt) sono ammissibili ma richiedono giustificazione empirica (in regime di alta volatilità, $\epsilon = 5$ pt potrebbe sottostimare i tocchi). Il congelamento empirico in Parte V deve testare valori in $\{5, 10, 15\}$ pt sullo storico Portara/CQG.
4. **NEUTRO non affrontati**: O-1 (cross-ref Cap.15.2.1 mancante in Cap.16.2) e O-2 (tie-break arrotondamento target_2 sintetico) restano carryover NEUTRO come da decisione supervisore. Se il supervisore decide di farli passare a "MIGLIORA PERFORMANCE" in un'iterazione successiva, sono fix da 1 riga ciascuno.

### Criterio di rollback Iterazione 2

- **Rollback totale dell'Iterazione 2**: se Review v2 emette un nuovo BUG REALE sulla nuova formulazione di NB-1 o NB-2 (es. la definizione di oscillazione produce comportamenti non equivalenti tra implementazioni conformi a causa di edge case non coperti dall'algoritmo), si torna alla versione v1 + si applica un fix alternativo. Soglia: 1 BUG REALE su NB-1 o NB-2 in Review v2.
- **Rollback parziale dei PROMEMORIA**: se Review v2 contesta una delle decisioni di design D-v2-1...D-v2-6 (es. dominio di `stop_type`, valore di $\epsilon$), il fix è puntuale (1-3 righe) e non richiede rollback totale dell'iterazione.
- **Non rollback**: imprecisioni di notazione, cross-reference, formattazione — correzioni editoriali in iterazione successiva.