# Review CAP-02 v4 — Parte II: Contratto del segnale FIB (verifica post-fix + audit ostile completo)

**Verdetto**: PASS

---

## Verifica chiusura finding v3

| ID finding v3 | Descrizione | Esito | Verifica |
|---------------|-------------|-------|----------|
| NB-3 (BUG REALE) | Formula display Cap.8.2: $\hat{\sigma}$ (log-return) anziché $\hat{\sigma}_{\text{pt}}$ (punti FIB) come argomento di $\tau_{vol}$ | **CHIUSO** | Formula display ora usa $\tau_{vol}(\hat{\sigma}_{\text{pt}}(t_{emission}))$; testo esplicativo, formula distanza sigma-units e riferimento a Parte III Cap.13 tutti coerenti. Nessun residuo della vecchia notazione in Cap.8. |
| NB-1 (MIGLIORA PERF) | Cross-reference Cap.7.6 pivot detection: "Cap.14" errato | **CHIUSO** | "L'algoritmo concreto di pivot detection è materia di Parte III (Cap.15)". Cap.15 contiene §15.3 con l'algoritmo. |
| NB-2 (MIGLIORA PERF) | Cross-reference Cap.7.1/7.2 invalidazione strutturale: "Parte IV (Cap.15)" errato | **CHIUSO** | Cap.7.1: "demandata a Parte IV" (nessun numero di capitolo). Cap.7.2 tabella: "(Parte IV)" (nessun numero di capitolo). |

Tutti e tre i finding v3 sono chiusi senza regressioni. I fix sono chirurgici e non introducono nuovi problemi nelle sezioni adiacenti.

---

## Problemi bloccanti (causano FAIL)

Nessuno.

---

## Problemi non bloccanti (causano CONDITIONAL)

Nessuno.

---

## Osservazioni minori (NEUTRO — non richiedono intervento di Development)

### O-1 — Cap.10.2: notazione $\hat{\sigma}$ residua nel log snapshot

**Posizione**: Cap.10.2, specifica del log di emissione (riga che descrive i valori loggati al momento dell'emissione).

**Citazione**: "$|\texttt{target\_1} - p_{ref}| / \hat{\sigma}$, con le soglie correnti $\tau_{vol}(\hat{\sigma}(t_{emission}))$"

**Fatto**: il fix NB-3 ha aggiornato correttamente Cap.8.2 (definizione autorevole). Cap.10.2 descrive i campi del log e usa ancora $\hat{\sigma}$ senza pedice. La definizione operativa è in Cap.8.2; Cap.10.2 è una specifica del log, non una definizione delle condizioni. Nessun impatto sul GA né sul ranking dei cromosomi.

**Classificazione**: NEUTRO

### O-2 — Cap.7.3: preview fill rule non allineata con worst-case di CAP-03 Cap.12.4

**Posizione**: Cap.7.3, descrizione del fill virtuale.

**Citazione**: "La regola di riferimento è il fill al primo livello discreto della zona toccato dalla barra 1-min"

**Fatto**: questa descrizione implica conoscenza intra-bar non derivabile da OHLC. La regola autorevole è in CAP-03 Cap.12.4 (worst-case conservativo: bordo superiore per long, bordo inferiore per short), ed è esplicitamente indicata nella stessa riga. Forward-reference approssimativo presente dall'origine, supersesso dalla delega a Parte III. Nessun impatto implementativo.

**Classificazione**: NEUTRO

---

## Secondo giro ostile — esito

Verificati senza problemi: state machine Q-05 (1+6 stati), tick FIB 5pt, $T_{touch}^{max}$ e $\Delta t_{cromosoma}$ coerenti, no-refresh payload, commissioni 1pt FIB equivalente, filtro 80pt entrambe le setup_class, condizioni di emissione post-fix tutte consistenti, cross-reference post-fix corretti, no look-ahead, separazione segnale/position lifecycle Cap.11.

Nessun problema reale aggiuntivo emerso.

---

## Classificazione per il supervisore

Non necessaria — verdetto PASS. Le due osservazioni minori (O-1, O-2) sono NEUTRO e non richiedono intervento.

---

*Audit eseguito su `docs/methodology_v2/CAP_02_parte_II.md` — 2026-05-24*
