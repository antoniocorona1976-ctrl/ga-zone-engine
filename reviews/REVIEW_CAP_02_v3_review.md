# Review CAP-02 v3 — Parte II: Contratto del segnale FIB (audit ostile stato corrente)

**Verdetto**: CONDITIONAL

Motivazione sintetica: il documento nella sua versione corrente (post Review v1/v2/v3 PASS, con mini-patch Cap.8.2 da NB-3 di CAP-03 applicata) è solido nella struttura della state machine, nella separazione segnale/position lifecycle, e nell'implementazione di Q-05. Tutti i finding delle review precedenti risultano chiusi. Emergono tre problemi non bloccanti: due cross-reference errati che puntano a capitoli sbagliati e una inconsistenza notazionale nella formula della condizione di volatilità che produce ambiguità dimensionale con impatto diretto sull'implementazione. Nessun bug bloccante sulla state machine o sulla logica del GA.

---

## Verifica di chiusura dei finding di Review v1/v2/v3

Tutti i finding B e NB delle review precedenti sono verificati chiusi nel testo corrente:

| ID | Esito | Verifica |
|----|-------|----------|
| B-1 (stop pre-touch) | CHIUSO | Cap.7.1: `invalidated` include esplicitamente superamento stop pre-touch |
| B-2 (missed_target contraddizione) | CHIUSO | Raw touch sempre eseguibile, nessun qualificatore "eseguibile" residuo |
| B-3 (target_1_hit non-terminale) | CHIUSO | Q-05: `target_2_hit` rimosso, `target_1_hit` rigorosamente terminale |
| B-4 (incoerenza CAP-01) | CHIUSO | CAP-01 patchata: "dall'esecuzione"; riga 75 patchata: "condizioni di emissione" |
| NB-7 (timer pre-trigger) | CHIUSO | Cap.6.1: $T_{touch}^{max} \in \{5,\ldots,480\}$ minuti di trading |
| NB-8 (edge case raw touch) | CHIUSO | Cap.7.3: tre sottocasi esplicitati |
| NB-9 (target_1_hit → revoked) | CHIUSO | Cap.7.1: nota esplicita |
| NB-10 (spazio nullo GA) | CHIUSO | Cap.8.2: sigma-units + 80pt come vincoli separati |
| N-7, N-8, M-4 v3 | CHIUSI | CAP-01 patchata (righe 75, 77) |

---

## Problemi bloccanti (causano FAIL)

Nessuno.

---

## Problemi non bloccanti (causano CONDITIONAL)

### NB-1 — Cross-reference errato: Cap.7.6 punta pivot detection a "Parte III (Cap.14)" anziché Cap.15

**Posizione**: Cap.7.6.

**Citazione**: "L'algoritmo concreto di pivot detection è materia di Parte III (Cap.14)".

**Fatto**: Cap.14 di Parte III è "Stato di regime intraday". L'algoritmo di pivot detection è in Cap.15.3 di Parte III ("Feature engineering causale", sottosezione "Algoritmo di pivot detection causale"). Il cross-reference è sbagliato.

**Impatto GA**: un implementatore che segua il riferimento cerca la pivot detection nel capitolo sbagliato. La regola di ancoraggio del primo pivot post-apertura (Q-02, target 70%) potrebbe essere implementata con la logica sbagliata. Rischio di errore di implementazione sulla regola di ancoraggio strutturale.

**Classificazione**: MIGLIORA PERFORMANCE (fix chirurgica: "Cap.14" → "Cap.15")

---

### NB-2 — Cross-reference errato: Cap.7.1 e Cap.7.2 puntano invalidazione strutturale a "Parte IV (Cap.15)"

**Posizione**: Cap.7.1 (definizione `invalidated`), Cap.7.2 (tabella transizioni, riga `active → invalidated`).

**Citazione**: "La definizione formale e completa delle condizioni di invalidazione strutturale è demandata a Parte IV (Cap.15)". Tabella: "condizione di invalidazione strutturale (Parte IV, Cap.15)".

**Fatto**: Cap.15 è in **Parte III** (feature engineering causale), non in Parte IV. Parte IV, secondo la struttura pianificata, conterrà Cap.16-18 (geometria delle zone) e Cap.19 (survival). Le condizioni di invalidazione strutturale saranno in un capitolo di Parte IV ancora da pianificare (verosimilmente Cap.16-18).

**Impatto GA**: la transizione `active → invalidated` pre-touch è critica per il ranking dei cromosomi (segnali invalidati prima del raw touch non vengono penalizzati come `stopped`). Un riferimento errato può portare a implementare una logica di invalidazione incoerente con la futura Parte IV.

**Fix proposta**: rimuovere il numero di capitolo e lasciare "Parte IV" senza specificare Cap.15, oppure rimandare a "Parte IV (Cap.16-18, da specificare)". In ogni caso eliminare l'erroneo "(Cap.15)".

**Classificazione**: MIGLIORA PERFORMANCE (fix chirurgica: rimozione del numero di capitolo errato)

---

### NB-3 — Inconsistenza notazionale nella formula della condizione di volatilità (Cap.8.2)

**Posizione**: Cap.8.2, formula display della condizione di emissione sulla volatilità.

**Citazione formula display**: $r_{1m}(t_{emission}) \leq \tau_{vol}(\hat{\sigma}(t_{emission}))$

**Citazione testo esplicativo** (subito dopo la formula): "dove $\hat{\sigma}_{\text{pt}}(t_{emission})$ è la stima di volatilità condizionata in punti FIB..."

**Fatto**: la formula display usa $\hat{\sigma}$ (volatilità in unità di log-return, ordine $10^{-4}$) come argomento di $\tau_{vol}$. Il testo immediatamente sotto definisce la variabile come $\hat{\sigma}_{pt}$ (volatilità convertita in punti FIB). Il lato sinistro $r_{1m}$ è in punti FIB. Per coerenza dimensionale, la formula deve usare $\hat{\sigma}_{pt}$ come argomento, non $\hat{\sigma}$.

La conversione $\hat{\sigma}_{pt}(t) = \hat{\sigma}(t) \cdot p_t$ è definita in Parte III Cap.13.1 (dopo NB-3 del CAP-03 v4). La formula display in Cap.8.2 deve riflettere questa conversione.

**Impatto GA**: se l'implementatore segue la formula display, passa $\hat{\sigma}$ (log-return) a $\tau_{vol}$; se segue il testo, passa $\hat{\sigma}_{pt}$ (punti FIB). La condizione di emissione produrrà soglie radicalmente diverse nei due casi, alterando quali segnali il motore emette e quindi il ranking dei cromosomi. Errore diretto sull'implementazione della condizione di emissione.

**Fix**: sostituire $\hat{\sigma}(t_{emission})$ con $\hat{\sigma}_{\text{pt}}(t_{emission})$ nella formula display.

**Classificazione**: BUG REALE (incoerenza dimensionale con impatto diretto sulla condizione di emissione)

---

## Osservazioni minori (NEUTRO)

### N-1 — CAP-01 riga 13: descrizione $T_{touch}^{max}$ non allineata con CAP-02

**Citazione CAP-01 riga 13**: "parametrizzato come mix di distanza in punti e tempo trascorso dipendente dal regime di volatilità corrente."

**Fatto**: in CAP-02, $T_{touch}^{max}$ è un semplice intero in minuti di trading nel dominio $\{5,\ldots,480\}$. Non è un "mix di distanza in punti e tempo trascorso". La descrizione in CAP-01 è una parafrasi imprecisa.

**Impatto GA**: nessuno. Il parametro è definito correttamente nel testo autorevole (CAP-02 Cap.6.1). Non entra in nessuna formula né logica di implementazione.

**Classificazione**: NEUTRO

### N-2 — Cap.10.1: "contesto cross-index" nel requisito di replay senza ancoraggio

**Citazione**: "a partire dallo storico delle barre 1-min del FIB e da quello dei feed ausiliari utilizzati dal motore (contesto cross-index, volumi)"

**Fatto**: il contesto cross-index (DAX, EuroStoxx50, S&P futures) è menzionato come input al replay ma non è formalmente dichiarato come input a nessuna decisione in Parte II. Il suo ruolo è in Parte III/IV.

**Impatto GA**: nessuno. Forward-reference legittimo; la specifica dei feed ausiliari sarà in Parte III.

**Classificazione**: NEUTRO

---

## Classificazione per il supervisore

| # | Problema | Classificazione | Default |
|---|----------|-----------------|---------|
| NB-3 | Formula display Cap.8.2: $\hat{\sigma}$ (log-return) anziché $\hat{\sigma}_{pt}$ (punti FIB) — incoerenza dimensionale nella condizione di emissione | BUG REALE | → Developer (obbligatorio) |
| NB-1 | Cross-ref Cap.7.6: pivot detection → "Cap.14" invece di "Cap.15" — fix 1 parola | MIGLIORA PERFORMANCE | → in attesa della tua decisione |
| NB-2 | Cross-ref Cap.7.1/7.2: invalidazione strutturale → "Parte IV (Cap.15)" errato — rimuovere "(Cap.15)" | MIGLIORA PERFORMANCE | → in attesa della tua decisione |
| N-1 | CAP-01 riga 13: descrizione $T_{touch}^{max}$ come "mix" non corrisponde al dominio intero di CAP-02 | NEUTRO | → ignorato |
| N-2 | Cap.10.1: "contesto cross-index" senza ancoraggio a capitolo specifico | NEUTRO | → ignorato |

**Conteggio**: BUG REALE = 1, MIGLIORA PERFORMANCE = 2, NEUTRO = 2.

---

*Audit eseguito su `docs/methodology_v2/CAP_02_parte_II.md` (stato corrente incluse modifiche non committate) — 2026-05-24*
