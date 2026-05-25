# Review CAP-04 v2 -- Parte IV: rework post-CONDITIONAL + mini-patch CAP-02 Iterazione 4

**Verdetto**: CONDITIONAL

**Commit oggetto**: `7b9faa5` + `6fdb05e` + `a92b515` (push su origin/main)
**Data**: 2026-05-25
**Natura**: Audit ostile rework v2 CAP-04 (post-Review v1 CONDITIONAL) + mini-patch CAP-02 Iterazione 4 (chiusura O-3 / O-6 sul payload e sul filtro 80pt)
**Reviewer**: Review Agent
**Decisioni di design auditate**: D-v2-1 ... D-v2-6 ratificate dall Orchestratore in assenza di Planner attivo

---

## Sintesi del verdetto

Il rework v2 chiude correttamente i 2 BUG REALI di Review v1 (NB-1 criterio temporale unico per `p_ref`; NB-2 definizione algoritmica formale di oscillazione con $\epsilon$ esplicito). Tre dei quattro PROMEMORIA approvati (O-4 catalogo 37 invariato; O-6 sincronizzazione 80pt Cap.6.1 PII vs Cap.5 PI) sono chiusi correttamente. Tuttavia il mini-patch CAP-02 introduce **1 incoerenza interna di documento fra Cap.6.1 e Cap.9.2** (i nuovi campi `target_2_type` e `stop_type` sono dichiarati nel payload e nominati come consumati dal canale Telegram, ma Cap.9.2 non li ha aggiunti alla lista ordinata dei campi del messaggio) e la decisione D-v2-5 sul censoring non-informativo contiene **1 razionale strutturalmente sbagliato** (Cap.19.4 riga 369 punto (a) confonde il timeout di sessione 22:00 CET con il timer di censoring effettivo $\Delta t_{cromosoma}$). Esiste inoltre **1 asimmetria di design** sul dominio di `stop_type` che riduce il valore informativo del campo verso loperatore, gia notata dal Developer stesso nel REPORT come "fix puntuale di 1 riga". Audit ha inoltre rilevato **1 esempio numerico in Cap.21.2 che viola il tick FIB 5 pt** dichiarato non-negoziabile. Nessun look-ahead introdotto; nessuna violazione del determinismo bit-exact algoritmico; nessuna regressione sui 35 AC v1 originali; nessuna contraddizione fondamentale con CAP-01/02/03 escluse quelle generate da NB-v2-1. Il verdetto e **CONDITIONAL**.

---

## Stato dei finding di Review v1

| ID | Tipo | Stato in v2 | Verifica indipendente |
|----|------|-------------|----------------------|
| NB-1 | BUG REALE | CHIUSO | Cap.16.1 righe 19-30: formula con argmax su tau_conf; testo coerente; razionale temporale esplicito; determinismo della selezione (riga 28). Verifica: il pivot a t1 e confermato a t1+nc, due pivot a t1!=t2 hanno tau_conf distinti. argmax ben definito senza tie-break. Causalita: tau_conf(p) in F_{t-1} per ogni pivot disponibile alla barra t. OK. |
| NB-2 | BUG REALE | CHIUSO con riserva | Cap.21.2 righe 464-487: definizione formale di "oscillazione completata", pseudocodice single-pass, esempio numerico. Tre riserve riscontrate in audit: (a) doppia notazione epsilon nello stesso Cap.21.2 - vedi O-v2-4; (b) gestione cross-session non esplicitata ma neutralizzata dal warm-up T_warmup_norm=100 >= N_osc=60; (c) vincolo epsilon < A_range/2 dichiarato "ammissibilita implicita" ma non enforced sul cromosoma (rinviato a Parte V). Chiusura sostanziale ma con osservazioni. |
| O-1 | NEUTRO | NON TOCCATO (corretto carryover) | Cap.16.2 riga 44 cita T_warmup_norm = 100 ma non cita "Cap.15.2.1 di Parte III" per T_warmup_EMA=74. Non-toccato come da decisione supervisore. |
| O-2 | NEUTRO | NON TOCCATO (corretto carryover) | Cap.17.4 riga 193 "arrotondato al multiplo di 5 piu vicino" - tie-break (es. valore esatto +/-2.5 dal multiplo) non esplicitato. Non-toccato come da decisione supervisore. |
| O-3 / M-12 | PROMEMORIA | CHIUSO con incoerenza interna | Mini-patch CAP-02 Cap.6.1 righe 19, 37-39, 51: nuovi campi nella tupla S; cross-ref a Cap.17.4 CAP-04 (riga 197) e Cap.18.1/18.3 (righe 231, 260). MA: Cap.6.1 riga 39 e Cap.17.4 riga 197 di CAP-04 dichiarano "Il consumer Telegram dell operatore (Cap.9.2) usa il valore" - e Cap.9.2 (riga 241-249) NON include i due nuovi campi nella lista di 7 voci. Vedi NB-v2-1. |
| O-4 / M-13 | PROMEMORIA | CHIUSO | Cap.21.5 riga 524: x^(A_range) feature condizionale al regime trade_range; catalogo globale 37 invariato. Coerente con D-v2-4. CARRYOVER.md riga 33 aggiornata a CLOSED-CAP-04. OK. |
| O-5 / M-7 | PROMEMORIA | CHIUSO con razionale parzialmente sbagliato | Cap.19.4 righe 363-371: formula T_j perp C | x_t, razionale strutturale, rinvio Parte V con Cox-Snell (1968) e Schoenfeld stratificato (Grambsch-Therneau 1994). MA: razionale (a) di riga 369 confonde 22:00 CET con Delta_t_cromosoma. Vedi NB-v2-3. Razionale (b) tiene; metodi corretti. |
| O-6 | PROMEMORIA | CHIUSO | Mini-patch CAP-02 Cap.6.1 riga 59-61: formula A_range >= 80 pt sostituita; Cap.8.2 riga 209 sincronizzato. REPORT_CAP_02 sezione "Iterazione 4" presente. CARRYOVER.md riga 41 marcato CHIUSO. OK. |

---

## Problemi bloccanti (causano FAIL)

**Nessuno.**

Verifica sui criteri di FAIL:
- **Look-ahead introdotto**: nessuno. NB-1 usa tau_conf(p) in F_{t-1}; NB-2 algoritmo causale su close(s) per s <= t-1.
- **Violazione determinismo bit-exact**: nessuna. NB-1 argmax univoco per costruzione; NB-2 single-pass con else-if disambiguante.
- **Violazione tick FIB**: a livello algoritmico, nessuna. A livello documentale (esempio numerico Cap.21.2), si - vedi NB-v2-4 non-bloccante.
- **Contraddizione fondamentale con CAP-01/02/03**: nessuna. Le 6 decisioni D-v2-1...D-v2-6 sono tecnicamente sostenibili.

Nessuna delle condizioni di FAIL si verifica.

---

## Problemi non bloccanti (causano CONDITIONAL)

### NB-v2-1 -- Incoerenza Cap.6.1 vs Cap.9.2 di CAP-02: target_2_type e stop_type dichiarati consumati dal canale Telegram ma non inclusi nella lista ordinata del messaggio pubblicato

**Localizzazione**: docs/methodology_v2/CAP_02_parte_II.md riga 39 (Cap.6.1 dichiarazione target_2_type) e riga 51 (Cap.6.1 dichiarazione stop_type); docs/methodology_v2/CAP_04_parte_IV.md riga 197 (Cap.17.4); confronto con docs/methodology_v2/CAP_02_parte_II.md righe 241-249 (Cap.9.2 lista ordinata dei campi pubblicati sul messaggio Telegram).

**Sintomo del problema**. Cap.6.1 riga 39 dichiara per target_2_type: "Il consumer Telegram dell’operatore (Cap.9.2) usa il valore per qualificare la natura del livello pubblicato: un livello synthetic ha natura informativa derivata da una regola del modello, non da una struttura confermata del prezzo." E Cap.17.4 riga 197 di CAP-04 ripete: "Il consumer Telegram dell’operatore (Cap.9.2 di Parte II) usa questo campo per qualificare la natura del livello pubblicato." Tuttavia Cap.9.2 di CAP-02 (righe 241-249) enumera "in ordine obbligatorio, i seguenti campi del payload" e la lista contiene solo 7 voci: signal_id, direction, setup_class, entry_zone, target_1 e target_2, stop_loss, timestamp_emission. **Ne target_2_type ne stop_type compaiono nella lista**. Analoga incoerenza per stop_type (Cap.6.1 riga 51 lo dichiara nel payload formale).

**Impatto GA**. Diretto: nullo. Il GA non legge Telegram. Indiretto sul contratto del segnale e sulla validazione operativa: se il consumer Telegram non vede il campo target_2_type, il claim del Cap.6.1 che "il consumer usa il valore per qualificare" e falso testualmente; l’operatore non puo qualificare la natura del target_2. La conversione signal-to-trade non e alterata (l’operatore agisce sul prezzo); ma il giudizio dell’operatore sul "tenere la posizione fino a target_2 vs uscire a target_1" e privato dell’informazione che il mini-patch dichiarava di fornire. Cioe il fix O-3/M-12 e formalmente nel payload ma non e visibile al consumer per cui era motivato. Problema reale di coerenza interna del contratto, non sul comportamento del GA.

**Classificazione**: BUG REALE di coerenza testuale (interno a CAP-02 fra Cap.6.1 e Cap.9.2 e con cross-ref errato da CAP-04). Non bloccante.

**Fix proposto al supervisore (decisione richiesta)**: aggiungere a Cap.9.2 due voci alla lista ordinata (8. target_2_type; 9. stop_type) oppure, in alternativa, decidere esplicitamente che i due campi NON sono pubblicati sul messaggio Telegram ma sono campi del payload diagnostico interno - e in tal caso correggere Cap.6.1 riga 39 (CAP-02) e Cap.17.4 riga 197 (CAP-04) rimuovendo il claim "Il consumer Telegram (Cap.9.2) usa il valore".

---

### NB-v2-2 -- Asimmetria di design stop_type rispetto a target_2_type: dominio {structural, personal} con valore costante structural per il motore

**Localizzazione**: docs/methodology_v2/CAP_02_parte_II.md riga 51 (Cap.6.1); docs/methodology_v2/CAP_04_parte_IV.md riga 231 (Cap.18.1); riga 260 (Cap.18.3); reports/REPORT_CAP_04.md riga 265 (nota al supervisore punto 2).

**Sintomo del problema**. Il dominio dichiarato di stop_type e {structural, personal}. Per i segnali emessi dal motore, il valore e SEMPRE structural (Cap.18.1 riga 231: "il valore del campo stop_type e popolato come structural in tutti i casi (sia quando stop_loss deriva dal candidato pivot, sia quando deriva dal candidato sigma di fallback)"); il valore personal e "segnaposto formale del dominio mai prodotto dal motore" (Cap.18.3 riga 260).

Per contro, target_2_type ha dominio {structural, synthetic} e il motore popola entrambi i valori a seconda dell’algoritmo di selezione di Cap.17.4 (pivot disponibile vs fallback sigma con k_t2). Cap.18.1 distingue lo stesso identico schema (pivot vs sigma fallback con d_stop_sigma) ma collassa entrambi i casi su structural, demandando la distinzione al log di emissione (Cap.10.2) come campo strutturato di diagnostica.

**Impatto GA**. Diretto: nullo. Indiretto sul contratto e sull’informativita verso l’operatore: il campo stop_type nel payload non porta informazione discriminante a chi consuma il payload pubblicato; il consumer Telegram (ammesso che venga aggiunto, vedi NB-v2-1) vedrebbe sempre structural e non saprebbe se lo stop e pivot strutturale forte o sigma sintetico debole. Asimmetria semantica fra target_2_type (informativo, discriminante) e stop_type (costante per il motore) e una scelta di design dichiarata in D-v2-3 ma non motivata strutturalmente. Il Developer stesso nel REPORT_CAP_04 nota al supervisore punto 2 propone esplicitamente l’alternativa {structural, synthetic} come "fix puntuale di 1 riga in CAP-02 + 1 in CAP-04".

**Classificazione**: MIGLIORA PERFORMANCE (decisione di design del supervisore). L’allineamento del dominio a {structural, synthetic} aumenta l’informativita del payload verso l’operatore e fornisce simmetria con target_2_type. Decisione del supervisore richiesta.

---

### NB-v2-3 -- Razionale (a) di censoring non-informativo strutturalmente sbagliato in Cap.19.4 + flip-flop di design D-6 v1 vs D-v2-5 v2 non discusso

**Localizzazione**: docs/methodology_v2/CAP_04_parte_IV.md righe 361, 369; reports/REPORT_CAP_04.md riga 133 (v1 D-6) vs righe 210, 221 (v2 D-v2-5).

**Sintomo del problema**. Cap.19.4 riga 361 dichiara: "I segnali che raggiungono l’expired con causa posttrigger_timeout (Cap.7.1 di Parte II) senza aver raggiunto ne target_1 ne stop_loss sono **censurati a destra a tau_i = Delta_t_cromosoma** minuti di trading." Il timer effettivo di censoring del survival e **Delta_t_cromosoma** (parametro del cromosoma, dominio {1,...,1680} min trading, fino a 2 giorni di trading dal raw touch).

Cap.19.4 riga 369 dichiara come razionale strutturale dell’assunzione di censoring non-informativo: "(a) **il timeout di sessione che genera il censoring e fissato dall’orario di chiusura (22:00 CET, Cap.7.4 di Parte II)** e non dipende dalla dinamica del prezzo ne dalle decisioni dell’operatore". **Questa frase e strutturalmente sbagliata**: il censoring non e generato dall’orario di chiusura 22:00 CET - e generato da Delta_t_cromosoma. Il timeout di sessione 22:00 CET si applica a T_residuo in Cap.16.6 (condizione di emissione) e in Cap.20.4 (filtro implicito via T_residuo), non al censoring del survival. Cap.19.4 riga 361 lo dichiara esplicitamente. La frase (a) confonde due meccanismi temporali distinti.

Il razionale (b) di riga 369 ("il timer post-trigger Delta_t_cromosoma [...] frozen sul fold in-sample e applicato uniformemente a tutti i segnali del fold OOS - la sua scelta non e correlata con le realizzazioni intra-fold dei tempi di evento T_j") tiene **condizionatamente al fold OOS** con cromosoma frozen: Delta_t_cromosoma e una costante intra-fold, quindi T_j perp C | x_t e plausibile a posteriori. Razionale (b) e valido; razionale (a) NON e un argomento corretto per l’assunzione di non-informativita del censoring.

Nota aggiuntiva sul flip-flop di design: REPORT v1 D-6 (riga 133) aveva dichiarato esplicitamente: "Censoring informativo dichiarato esplicitamente (Cap.19.4) - Il timer Delta_t_cromosoma e un parametro del cromosoma, non un evento casuale: il censoring **non e non-informativo per costruzione**." In v2 il Developer/Orchestratore ha invertito la posizione e dichiarato il censoring **non-informativo**. L’inversione non e discussa esplicitamente nel REPORT v2: la D-v2-5 dichiara la nuova posizione come se fosse coerente con v1, senza segnalare il flip-flop. Il supervisore deve sapere che la posizione metodologica sul censoring e cambiata.

**Impatto GA**. Diretto: indiretto. La specifica del modello survival rinvia la verifica empirica a Parte V (Cox-Snell, Schoenfeld stratificato) indipendentemente dal razionale a priori (a)/(b). Il razionale sbagliato non altera il comportamento del survival in Parte IV: il modello assume non-informativita e la verifica empirica decidera. Tuttavia: (i) un razionale sbagliato e una falla di documentazione metodologica; (ii) se (a) fosse l’unico supporto, la motivazione sarebbe nulla; (b) regge da solo, quindi l’assunzione non e invalidata, ma e motivata male.

**Classificazione**: BUG REALE di razionale (di documentazione metodologica), non BUG REALE algoritmico.

**Fix proposto**: rimuovere la frase (a) di riga 369 ("il timeout di sessione che genera il censoring e fissato dall’orario di chiusura (22:00 CET, Cap.7.4 di Parte II) e non dipende dalla dinamica del prezzo ne dalle decisioni dell’operatore") e mantenere solo (b). Aggiungere nota nel REPORT v2 che D-v2-5 inverte la posizione di D-6 v1 (flip-flop di design da segnalare al supervisore).

---

### NB-v2-4 -- Esempio numerico Cap.21.2 riga 487 viola il tick FIB 5 pt

**Localizzazione**: docs/methodology_v2/CAP_04_parte_IV.md riga 487 (esempio numerico dell’algoritmo NB-2).

**Sintomo del problema**. L’esempio numerico introdotto per illustrare il pseudocodice di conteggio oscillazioni usa close: 27.402 (tocco LOW), 27.450 (NONE), 27.498 (tocco HIGH), 27.495 (HIGH stesso bordo), 27.403 (tocco LOW), 27.450 (NONE). Il FIB ha tick fisso 5 pt; le close ammissibili sono multipli di 5 (27.400, 27.405, 27.410, ...). Verifica puntuale:
- 27.402 / 5 = 5480.4 (NO)
- 27.498 / 5 = 5499.6 (NO)
- 27.495 / 5 = 5499.0 (SI)
- 27.403 / 5 = 5480.6 (NO)
- 27.450 / 5 = 5490.0 (SI)

Quindi 3 dei 5 valori distinti (27.402, 27.498, 27.403) **non sono prezzi ammissibili sul FIB**.

Il documento dichiara piu volte (CAP-04 introduzione riga 9, Cap.16.1 riga 24, Cap.6.1 PII) che i prezzi FIB sono multipli di 5: **vincolo non-negoziabile**. L’esempio didattico viola il vincolo.

**Impatto GA**. Diretto: zero (esempio illustrativo; l’algoritmo opera su qualunque close ammissibile FIB e l’algoritmo non discrimina). Impatto su coerenza documentazione: presente. Per audit ostile, e un BUG REALE di documentazione perche viola un vincolo dichiarato non-negoziabile.

**Classificazione**: BUG REALE (documentazione).

**Fix proposto**: sostituire i prezzi non ammissibili con multipli di 5 prossimi. Esempio: barra t-50 close 27.400 (tocco LOW con epsilon=5), barra t-45 close 27.450 (NONE), barra t-40 close 27.500 (tocco HIGH, crossing 1, n_osc=1), barra t-30 close 27.495 (tocco HIGH stesso bordo, no incremento), barra t-20 close 27.405 (tocco LOW, crossing 2, n_osc=2), barra t-10 close 27.450 (NONE). Tutti multipli di 5; logica del conteggio invariata.

---

## Osservazioni minori

### O-v2-1 -- Esempio numerico Cap.16.1 usa orari (10:15, 11:30) invece di indici di barra

**Localizzazione**: docs/methodology_v2/CAP_04_parte_IV.md riga 30.

L’esempio dice "pivot a 27.300 con tau_conf = 10:15 e pivot a 27.250 con tau_conf = 11:30". Ma tau_conf(p) e definito a riga 19 come "la barra t_p + n_c alla cui chiusura il pivot rilevato a t_p e stato confermato": e un indice di barra, non un orario. La corrispondenza orario-barra di 1 minuto e biunivoca, quindi non c’e ambiguita formale. Convenzione consolidata anche in Cap.7.4 di CAP-02 (esempio 21:55), Cap.16.6 di CAP-04. **Impatto GA: nullo**. Non e un problema.

### O-v2-2 -- target_2_type non richiamato esplicitamente in Cap.21.4 (target_2 nel trade_range)

**Localizzazione**: docs/methodology_v2/CAP_04_parte_IV.md riga 511.

Cap.21.4 applica l’algoritmo di selezione di Cap.17.4 al trade_range. Quindi la dicotomia structural/synthetic e il campo target_2_type restano operativi. Cap.21 non lo richiama esplicitamente ma e implicito. **Impatto GA: nullo**. Non bloccante.

### O-v2-3 -- Cap.20.4 limite formale derivazione plausibile ma non rigorosa

**Localizzazione**: docs/methodology_v2/CAP_04_parte_IV.md riga 426.

Il documento afferma lim_{T_res->0} p_hat_hit = 0 per "incidenza cumulativa su intervallo di durata zero". L’equazione di hazard a riga 313 ha T_residuo come covariata con coefficiente gamma_j; per T_residuo -> 0 con gamma_j finito, il termine exp(gamma_j * T_residuo) -> 1 - effetto sulla hazard finito e integrale a limite di integrazione zero da zero. **Impatto GA: nullo** (risultato corretto). Non bloccante.

### O-v2-4 -- Doppia notazione epsilon in Cap.21.2 con due significati distinti

**Localizzazione**: docs/methodology_v2/CAP_04_parte_IV.md riga 458 (condizione 2 classificazione: "dove epsilon = b") vs riga 466 (algoritmo NB-2: "Sia epsilon una tolleranza di prossimita ai bordi, parametro provvisorio del modello con valore di lavoro epsilon = 5 pt") e tabella riga 552.

Nello stesso Cap.21.2, la lettera epsilon e usata due volte con significati distinti: (a) condizione 2 della classificazione, epsilon = b (semi-ampiezza zona, parametro cromosoma in {5,...,40} pt); (b) algoritmo NB-2 di conteggio oscillazioni, epsilon = 5 pt (parametro provvisorio del modello). Distanti 8 righe nel testo. Impatto GA: nullo a runtime. Possibile confusione per l’implementatore. Fix proposto: rinominare uno dei due (ad es. epsilon_b in condizione 2 e epsilon_osc nell’algoritmo). Non bloccante.

### O-v2-5 -- Pseudocodice oscillazione non gestisce esplicitamente cross-session

**Localizzazione**: docs/methodology_v2/CAP_04_parte_IV.md righe 468-483.

Il pseudocodice itera s in [t - N_osc + 1, t-1] senza filtrare cross-session. Per t a inizio sessione, la finestra potrebbe attraversare 22:00->8:00. Tuttavia il warm-up di Cap.16.2 (sospensione emissione finche T_warmup_norm = 100 >= N_osc = 60) garantisce che alla prima barra ammissibile la finestra [t-60, t-1] e interamente dentro la sessione corrente. **Edge case neutralizzato dal warmup esistente**, ma non esplicitato nel pseudocodice. Impatto GA: nullo. Suggerimento di documentazione: aggiungere riga "tutti gli s appartengono alla sessione corrente per costruzione, grazie a T_warmup_norm >= N_osc" al pseudocodice.

---

## Citazioni problematiche dal testo

### Citazione 1 (NB-v2-1)
**File**: docs/methodology_v2/CAP_02_parte_II.md riga 39 (Cap.6.1).
**Testo**: "Il consumer Telegram dell’operatore (Cap.9.2) usa il valore per qualificare la natura del livello pubblicato".
**Problema**: Cap.9.2 (righe 241-249 dello stesso documento) elenca i 7 campi del messaggio Telegram e **non include** target_2_type. La frase e falsa testualmente.
**Classificazione**: BUG REALE (coerenza interna).

### Citazione 2 (NB-v2-1)
**File**: docs/methodology_v2/CAP_04_parte_IV.md riga 197 (Cap.17.4).
**Testo**: "Il consumer Telegram dell’operatore (Cap.9.2 di Parte II) usa questo campo per qualificare la natura del livello pubblicato".
**Problema**: stessa incoerenza della Citazione 1, replicata in CAP-04 con riferimento esplicito a Cap.9.2 di Parte II.
**Classificazione**: BUG REALE (coerenza interna fra Parte II e Parte IV).

### Citazione 3 (NB-v2-2)
**File**: docs/methodology_v2/CAP_04_parte_IV.md riga 231 (Cap.18.1).
**Testo**: "Per i segnali emessi dal motore, il valore del campo stop_type e popolato come structural in tutti i casi [...] Il valore personal non viene mai assegnato dal motore al campo del payload pubblicato".
**Problema**: il dominio {structural, personal} e di fatto degenerato a singolo valore structural per qualsiasi payload prodotto dal motore. Il campo non porta informazione utile a chi consuma il payload. Asimmetria con target_2_type che invece discrimina effettivamente.
**Classificazione**: MIGLIORA PERFORMANCE (decisione di design del supervisore).

### Citazione 4 (NB-v2-3)
**File**: docs/methodology_v2/CAP_04_parte_IV.md riga 369 (Cap.19.4).
**Testo**: "(a) il timeout di sessione che genera il censoring e fissato dall’orario di chiusura (22:00 CET, Cap.7.4 di Parte II) e non dipende dalla dinamica del prezzo ne dalle decisioni dell’operatore".
**Problema**: stessa Cap.19.4 riga 361 (8 righe sopra) dichiara che il censoring avviene a tau_i = Delta_t_cromosoma - **non** al timeout di sessione 22:00 CET. La frase (a) attribuisce al censoring un meccanismo strutturale diverso da quello effettivo.
**Classificazione**: BUG REALE (razionale metodologico sbagliato, ma argomento (b) tiene da solo).

### Citazione 5 (NB-v2-3, flip-flop di design)
**File**: reports/REPORT_CAP_04.md riga 133 (v1 D-6) vs righe 210, 221 (v2 D-v2-5).
**Testo v1**: "Censoring informativo dichiarato esplicitamente (Cap.19.4) - Il timer Delta_t_cromosoma e un parametro del cromosoma, non un evento casuale: il censoring non e non-informativo per costruzione."
**Testo v2**: "(O-5 / M-7 PROMEMORIA approvato) Cap.19.4 di CAP-04 esteso con: (i) dichiarazione formale dell’assunzione di censoring non-informativo T_j perp C | x_t".
**Problema**: inversione completa della posizione metodologica fra v1 e v2 non discussa esplicitamente come tale. Il supervisore deve essere informato del flip-flop e validarlo.
**Classificazione**: PROMEMORIA (necessita di nota esplicita al supervisore nel REPORT).

### Citazione 6 (O-v2-4)
**File**: docs/methodology_v2/CAP_04_parte_IV.md riga 458 (Cap.21.2 condizione 2) e riga 466 (definizione di oscillazione).
**Testo riga 458**: "dove epsilon = b (la semi-ampiezza della zona) e il margine di prossimita".
**Testo riga 466**: "Sia epsilon una tolleranza di prossimita ai bordi, parametro provvisorio del modello con valore di lavoro epsilon = 5 pt = 1 tick FIB".
**Problema**: stesso simbolo, due grandezze distinte, nello stesso paragrafo distanti 8 righe.
**Classificazione**: NEUTRO (chiarezza, non comportamento).

### Citazione 7 (NB-v2-4)
**File**: docs/methodology_v2/CAP_04_parte_IV.md riga 487 (esempio Cap.21.2).
**Testo**: "barra t-50 close 27.402 (tocco LOW), barra t-45 close 27.450 (NONE, nel mezzo), barra t-40 close 27.498 (tocco HIGH, crossing 1 completato, n_osc = 1), barra t-30 close 27.495 (HIGH, stesso bordo, no incremento), barra t-20 close 27.403 (tocco LOW, crossing 2 completato, n_osc = 2), barra t-10 close 27.450 (NONE)".
**Problema**: i prezzi 27.402, 27.498, 27.403 **non sono multipli di 5** e quindi non sono close ammissibili sul FIB (tick FIB = 5 pt). Il documento dichiara piu volte che i prezzi FIB sono multipli di 5 (vincolo non-negoziabile).
**Classificazione**: BUG REALE (documentazione).

---

## Verifica sistematica AC v2 (12 voci AC-v2-1 ... AC-v2-12)

| AC-ID | Criterio | Esito | Evidenza riga/file |
|-------|----------|-------|--------------------|
| AC-v2-1 | NB-1 chiuso. Cap.16.1 con formula criterio temporale (argmax timestamp); riga 26 invariata; esempio numerico aggiornato | **OK** | CAP_04_parte_IV.md:19-30. Verifica indipendente determinismo: t1 + nc != t2 + nc iff t1 != t2. argmax univoco. |
| AC-v2-2 | NB-2 chiuso. Definizione algoritmica esplicita di oscillazione (crossing completo) con epsilon = 5 pt provvisoria; algoritmo deterministico + causale | **OK con riserva** | CAP_04_parte_IV.md:464-487. Riserve: O-v2-4 doppio epsilon (NEUTRO); O-v2-5 cross-session non esplicitato ma neutralizzato dal warm-up; **NB-v2-4 esempio numerico viola tick FIB**. Algoritmicamente OK, documentazione con bug. |
| AC-v2-3 | O-3 / M-12 chiuso. Payload S Cap.6.1 di CAP-02 con campi target_2_type e stop_type. Cap.17.4 e Cap.18.1/18.3 di CAP-04 con riferimento esplicito | **PARZIALE** | CAP_02_parte_II.md:19, 37, 39, 51; CAP_04_parte_IV.md:197, 231, 260. Riserva: **Cap.9.2 di CAP-02 NON include i nuovi campi** nella lista pubblicata sul Telegram benche Cap.6.1 e Cap.17.4 dichiarino il consumo. **NB-v2-1**. |
| AC-v2-4 | O-4 / M-13 chiuso. x^(A_range) feature condizionale al regime trade_range; catalogo CAP-03 invariato a 37 | **OK** | CAP_04_parte_IV.md:524. CAP-03 invariato (verificato non toccato dal commit 7b9faa5). |
| AC-v2-5 | O-5 / M-7 formalizzato. Cap.19.4 con dichiarazione esplicita censoring non-informativo + rinvio Parte V con metodi nominati (Cox-Snell, Schoenfeld stratificato) | **PARZIALE** | CAP_04_parte_IV.md:363-371. Riserva: **razionale (a) di riga 369 strutturalmente sbagliato** (confonde 22:00 CET con Delta_t_cromosoma). **NB-v2-3**. Argomento (b) tiene; metodi corretti. |
| AC-v2-6 | O-6 chiuso. Mini-patch CAP-02 Cap.6.1: formulazione 80pt allineata a Cap.5 PI (A_range >= 80 pt). REPORT_CAP_02 ha sezione "Iterazione 4" | **OK** | CAP_02_parte_II.md:59-61, 209; REPORT_CAP_02.md:281-337. |
| AC-v2-7 | Nessuna regressione su AC v1 originali (35 voci). Tabella prima/dopo dove rilevante | **OK** | Verifica sotto: 43/44 OK; 0 degradati; 3 PARZIALE v1 chiusi (C16-1 da NB-1; C21-5 e T-2 da NB-2). |
| AC-v2-8 | tasks/CARRYOVER.md aggiornato: M-12, M-13, O-6 -> CLOSED-CAP-04; M-7 resta OPEN Parte V; M-8...M-15 invariati OPEN | **OK** | CARRYOVER.md:27, 32, 33, 34-35, 41. |
| AC-v2-9 | REPORT_CAP_04.md include sezione "Iterazione 2" con: per ogni finding/PROMEMORIA, modifica applicata + misura prima/dopo + AC chiuso | **OK** | REPORT_CAP_04.md:198-273. |
| AC-v2-10 | REPORT_CAP_02.md include sezione "Iterazione 4 - mini-patch Cap.6.1 (flag payload + sincronizzazione 80pt)" | **OK** | REPORT_CAP_02.md:281-337. |
| AC-v2-11 | 00_indice.md aggiornato per riflettere stato corrente CAP-04 e CAP-02 (entrambi in revisione) | **OK** | 00_indice.md:15, 31. |
| AC-v2-12 | Tutti i file modificati committati e pushati. Working tree pulito sui file di task | **OK** | git log: a92b515 sopra 6fdb05e e 7b9faa5. Push su origin/main. |

**Conteggio AC v2: 10 OK, 2 PARZIALE (AC-v2-3 per NB-v2-1; AC-v2-5 per NB-v2-3), 0 MANCA su 12 totali.**

---

## Verifica sistematica AC I4 CAP-02 (8 voci AC-I4-1 ... AC-I4-8)

| AC-ID | Criterio | Esito | Evidenza riga/file |
|-------|----------|-------|--------------------|
| AC-I4-1 | Tupla S di Cap.6.1 estesa con target_2_type e stop_type come campi obbligatori | **OK** | CAP_02_parte_II.md:19 (tupla a 12 campi). |
| AC-I4-2 | Descrizione formale target_2_type con dominio + popolamento deterministico + uso consumer Telegram | **PARZIALE** | CAP_02_parte_II.md:37-39. Riserva: claim su consumer Telegram (Cap.9.2) non riflesso in Cap.9.2 stesso. **NB-v2-1**. |
| AC-I4-3 | Descrizione formale stop_type con dominio + valore sempre structural da motore + razionale personal | **OK formale, MIGLIORA PERF di design** | CAP_02_parte_II.md:51. Formalmente l’AC e soddisfatto; il design e discusso in NB-v2-2. |
| AC-I4-4 | Filtro 80pt trade_range in Cap.6.1 sincronizzato a A_range >= 80 pt (Cap.5 PI normativo) | **OK** | CAP_02_parte_II.md:59-61. |
| AC-I4-5 | Filtro 80pt trade_range in Cap.8.2 sincronizzato | **OK** | CAP_02_parte_II.md:209. |
| AC-I4-6 | Coerenza con CAP-04: cross-ref espliciti in Cap.17.4 e Cap.18.1/18.3 | **OK** | CAP_04_parte_IV.md:197, 231, 260. |
| AC-I4-7 | CARRYOVER aggiornato: M-12 -> CLOSED-CAP-04, O-6 -> CHIUSO Iter.4 CAP-02 | **OK** | CARRYOVER.md:32, 41. |
| AC-I4-8 | Indice aggiornato per riflettere stato CAP-02 IN REVIEW Iterazione 4 | **OK** | 00_indice.md:15. |

**Conteggio AC I4: 7 OK, 1 PARZIALE (AC-I4-2 per NB-v2-1), 0 MANCA su 8 totali.**

---

## Verifica non-regressione AC v1 (44 voci originali)

Confronto stato v1 vs v2 (conteggio AC del REPORT_CAP_04 = 41 voci della tabella; review v1 considerava 35 effettivi al netto delle voci ridondanti; adottato 44 = struttura completa del REPORT inclusi sub-AC).

| Bucket | v1 OK | v1 PARZIALE | v1 MANCA | v2 OK | v2 PARZIALE | v2 MANCA | Note |
|--------|-------|-------------|----------|-------|-------------|----------|------|
| Strutturali (S-1..S-3) | 2 | 1 (S-2) | 0 | 2 | 1 (S-2 NEUTRO non-toccato) | 0 | Invariati. S-2 NEUTRO mantiene PARZIALE come da decisione supervisore (O-1). |
| Cap.16 (C16-1..C16-7) | 6 | 1 (C16-1) | 0 | **7** | 0 | 0 | **C16-1 chiuso da NB-1 fix (criterio temporale unico)**. |
| Cap.17 (C17-1..C17-5) | 5 | 0 | 0 | 5 | 0 | 0 | Invariati. |
| Cap.18 (C18-1..C18-5) | 5 | 0 | 0 | 5 | 0 | 0 | Invariati. |
| Cap.19 (C19-1..C19-8) | 8 | 0 | 0 | 8 | 0 | 0 | Invariati. |
| Cap.20 (C20-1..C20-4) | 4 | 0 | 0 | 4 | 0 | 0 | Invariati. |
| Cap.21 (C21-1..C21-5) | 4 | 1 (C21-5) | 0 | **5** | 0 | 0 | **C21-5 chiuso da NB-2 fix (definizione algoritmica oscillazione)**. |
| Trasversali (T-1..T-7) | 6 | 1 (T-2) | 0 | **7** | 0 | 0 | **T-2 chiuso da NB-2 fix (determinismo bit-exact ripristinato)**. |
| **Totale** | **40** | **4** | **0** | **43** | **1** | **0** | Progressione +3 (NB-1 chiude C16-1; NB-2 chiude C21-5 e T-2). Nessuna regressione. |

**Conclusione non-regressione**: **0 AC v1 degradati o rotti**; 3 AC v1 che erano PARZIALE in v1 sono ora OK in v2; l’unico PARZIALE residuo (S-2) e NEUTRO e per decisione supervisore non e stato toccato in v2.

---

## Secondo giro ostile

**Domanda: sono sicuro di aver trovato tutti i problemi reali?**

Riesame sistematico:

1. **Causalita temporale di tutti i nuovi formalismi**:
   - tau_conf(p) = t_p + n_c, disponibile per la valutazione alla barra t > t_p + n_c -> tau_conf(p) in F_{t-1} per ogni pivot disponibile. OK.
   - Pseudocodice oscillazione: itera su close(s) per s in [t - N_osc + 1, t-1]. Esplicitamente esclude close(t). OK.
   - Censoring: tau_i osservato a posteriori sui segnali OOS (replay deterministico). Non look-ahead.
   - target_2_type, stop_type: popolati al momento dell’emissione sulla base di pivot in P(t_emission). OK.

2. **Determinismo bit-exact**:
   - NB-1: argmax univoco (provato strutturalmente in riga 28). OK.
   - NB-2: single-pass su sequenza chiusa con else-if disambiguante (riga 475-476). OK anche per intervalli LOW/HIGH potenzialmente sovrapposti.
   - Tie-break su due barre stesso close-tocco lo stesso secondo: non possibile perche barre 1-min hanno timestamp interi distinti.
   - Bordo inclusivo/esclusivo: intervalli chiusi [p_low-eps, p_low+eps]. Determinismo OK.

3. **Coerenza simboli con CAP-03 e capitoli precedenti**:
   - sigma_hat_pt usato consistentemente in Cap.17.3, 17.4, 18.1, 18.5, 19, 21.5. OK.
   - tau_conf nuovo simbolo introdotto in Cap.16.1 riga 19. Distinto da tau_vol, tau_liq, tau_dist^sigma, tau_surv. OK.
   - epsilon: **collisione locale Cap.21.2** (O-v2-4 NEUTRO).
   - delta_pivot vs delta_break: distinti. OK (delta_break = delta_pivot = 10 pt provvisori).

4. **Tick FIB = 5 pt rispettato negli esempi**:
   - Cap.16.1 esempio: 27.300, 27.250, 27.700, 27.750 - tutti multipli di 50. OK.
   - Cap.17.2 esempio: 27.540, 27.570, 27.600 - tutti multipli di 5. OK.
   - Cap.18.2 esempio: 27.500, 27.460, 27.490 - tutti multipli di 5. OK.
   - Cap.21.4 esempio: 27.400, 27.385, 27.415, 27.500, 27.360 - tutti multipli di 5. OK.
   - **Cap.21.2 esempio: 27.402, 27.498, 27.403 - VIOLAZIONE TICK FIB**. NB-v2-4.

5. **Compatibilita nuova tupla S con i consumer dichiarati**:
   - Telegram bot (Cap.9.2): NON aggiornato -> NB-v2-1.
   - Log emissione (Cap.10.2): "l’intero payload del segnale S (tutti i campi di Cap.6.1)" -> formulazione generica che cattura automaticamente i nuovi campi. OK.
   - Motore di esecuzione manuale: l’operatore agisce sul prezzo, non sui flag. OK.

6. **Coerenza Cap.6.1 PII vs CAP-04 sul filtro 80pt**:
   - Cap.6.1 (CAP-02 patch 4): A_range = p_high,range - p_low,range >= 80 pt.
   - Cap.5 PI: A_range >= 80 pt (riferimento normativo).
   - Cap.21.1 PIV: A_range = p_high - p_low >= 80 pt.
   - Allineamento corretto.

7. **Coerenza Cap.21 vs Cap.6.1 PII su setup_class**:
   - Cap.6.1 PII riga 53: dominio setup_class in {directional, trade_range}.
   - Cap.21.2 PIV: classificazione deterministica con 4 condizioni.
   - Allineamento corretto.

8. **Decisione D-v2-4 catalogo 37**:
   - Cap.19.3 PIV: feature input "sottoinsieme delle 37 feature causali normalizzate".
   - Cap.21.5 PIV: x^(A_range) feature condizionale solo per trade_range; catalogo directional resta 37.
   - **Comportamento quando regime cambia da directional a trade_range a meta sessione?** Il segnale e classificato setup_class al momento dell’emissione (Cap.21.2): "La classificazione e deterministica dato lo storico OHLC e i parametri del modello." Una volta classificato, il setup_class e nel payload immutabile (Cap.6.2 PII). Quindi un segnale e directional o trade_range per la sua intera vita; il survival applicato e quello corrispondente alla classe del segnale. No cross-contamination del survival fra le due classi. OK.

9. **Decisione D-v2-5 censoring**:
   - Razionale (a) sbagliato (NB-v2-3).
   - Razionale (b) tiene condizionatamente al fold OOS frozen.
   - Verifica empirica rinviata correttamente a Parte V con Cox-Snell e Schoenfeld stratificato.
   - **Citazioni**: Cox e Snell (1968) JRSS B 30(2) 248-275 e Grambsch e Therneau (1994) Biometrika 81(3) 515-526. **Citazioni corrette al contesto**: Cox-Snell residuals sono definiti in Cox e Snell (1968), Schoenfeld test pesato e formalizzato in Grambsch-Therneau (1994). OK.

10. **Coerenza Cap.16.2 warm-up + Cap.21.2 condizione di sessione**: T_warmup_norm = 100 >= N_osc = 60. OK, warmup neutralizza l’edge case cross-session.

11. **Inversione D-6 v1 -> D-v2-5 v2 sul censoring**: il REPORT v2 non discute il flip-flop esplicitamente. Coperto in NB-v2-3.

12. **Causa pretrigger_timeout esclusa dal campione survival** (Cap.19.4 riga 361): OK, coerente con il modello post-fill.

---

## Classificazione per il supervisore

| # | Problema | Classificazione | Mandare a Development? |
|---|----------|-----------------|------------------------|
| NB-v2-1 | Cap.6.1/Cap.17.4 dichiarano "Consumer Telegram (Cap.9.2) usa il valore" ma Cap.9.2 non include i nuovi campi nella lista pubblicata | BUG REALE (coerenza interna documento) | **SI** - fix in alternativa: (a) aggiungere target_2_type e stop_type a Cap.9.2 oppure (b) rimuovere claim da Cap.6.1/Cap.17.4. Decisione del supervisore richiesta sulla via. |
| NB-v2-2 | stop_type dominio {structural, personal} con valore costante structural dal motore: asimmetria con target_2_type, campo non informativo verso operatore | MIGLIORA PERFORMANCE | Decisione del supervisore richiesta. Developer stesso propone dominio {structural, synthetic} per simmetria (REPORT nota 2). Se approvato, fix di 1 riga in CAP-02 + 1 riga in CAP-04. |
| NB-v2-3 | Razionale (a) di censoring non-informativo strutturalmente sbagliato (Cap.19.4 riga 369: confonde 22:00 CET con Delta_t_cromosoma); flip-flop di design D-6 v1 -> D-v2-5 v2 non discusso esplicitamente | BUG REALE (razionale metodologico) | **SI** - rimozione frase (a) di riga 369; aggiunta nota al supervisore sul flip-flop nel REPORT. Razionale (b) tiene da solo, ma (a) e sbagliato e va corretto. |
| NB-v2-4 | Esempio numerico Cap.21.2 riga 487 usa prezzi che non sono multipli di 5 (viola tick FIB 5 pt dichiarato non-negoziabile) | BUG REALE (documentazione) | **SI** - correzione esempio: usare 27.400, 27.450, 27.500, 27.495, 27.405 (multipli di 5). Fix banale ma rilevante per coerenza. |
| O-v2-1 | Esempio Cap.16.1 usa orari (10:15) invece di indici di barra per tau_conf | NEUTRO | NO - convenzione consolidata nel documento. |
| O-v2-2 | target_2_type non richiamato esplicitamente in Cap.21.4 | NEUTRO | NO - implicito dall’algoritmo di Cap.17.4. |
| O-v2-3 | Cap.20.4 limite lim p_hat_hit = 0 derivazione plausibile ma non formalmente rigorosa | NEUTRO | NO - risultato corretto. |
| O-v2-4 | Doppia notazione epsilon in Cap.21.2 con due significati distinti (condizione 2 vs algoritmo oscillazione) | NEUTRO | NO - leggibilita, non comportamento. |
| O-v2-5 | Pseudocodice oscillazione non gestisce esplicitamente cross-session (neutralizzato dal warm-up) | NEUTRO | NO - edge case neutralizzato. |

---

## Riepilogo per chiusura

- **Verdetto finale**: CONDITIONAL
- **Conteggio**: 0 bloccanti + 4 non bloccanti (NB-v2-1, NB-v2-2, NB-v2-3, NB-v2-4) + 5 osservazioni minori
- **Conteggio classificazione**: 3 BUG REALI (NB-v2-1, NB-v2-3, NB-v2-4) + 1 MIGLIORA PERFORMANCE (NB-v2-2) + 5 NEUTRO (O-v2-1...O-v2-5) + 0 RISCHIO PEGGIORAMENTO + 0 PROMEMORIA nuovi
- **AC v2**: 10 OK / 2 PARZIALE / 0 MANCA su 12 (PARZIALE: AC-v2-3 per NB-v2-1; AC-v2-5 per NB-v2-3)
- **AC I4 CAP-02**: 7 OK / 1 PARZIALE / 0 MANCA su 8 (PARZIALE: AC-I4-2 per NB-v2-1)
- **AC v1 (non-regressione)**: 43 OK / 1 PARZIALE / 0 MANCA su 44; **0 AC v1 degradati**; **3 AC v1 che erano PARZIALE in v1 sono OK in v2** (C16-1, C21-5, T-2)
- **File prodotto**: C:/Users/AN/Documents/Projects/ga-zone-engine/reviews/REVIEW_CAP_04_v2_review.md
- **Hash commit oggetto della review**: 7b9faa5 + 6fdb05e + a92b515

**Motivazione del CONDITIONAL anziche PASS**: I 2 BUG REALI di Review v1 (NB-1, NB-2) sono chiusi correttamente. 3 dei 4 PROMEMORIA sono chiusi senza problemi residui (O-4, O-6). Tuttavia:
1. La chiusura di O-3 introduce un’incoerenza interna fra Cap.6.1 (dichiara consumer Telegram) e Cap.9.2 (non aggiornato) -> NB-v2-1.
2. La chiusura di O-5 ha un razionale strutturalmente sbagliato in (a) di Cap.19.4 riga 369 -> NB-v2-3.
3. L’esempio numerico Cap.21.2 viola il tick FIB -> NB-v2-4.
4. La decisione D-v2-3 sul dominio di stop_type produce campo costante = non informativo (asimmetria con target_2_type) -> NB-v2-2.

Nessuno di questi e bloccante per il GA (la matematica del survival, l’algoritmo della oscillazione, la selezione del p_ref, il filtro 80pt e la geometria delle zone funzionano correttamente). Ma sono problemi reali di coerenza interna che il PASS non puo tollerare. La correzione e chirurgica per tutti e quattro (<= 5 righe per ogni fix).
