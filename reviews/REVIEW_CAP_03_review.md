# Review CAP-03 -- Parte III: Layer quantitativo single-instrument

**Verdetto**: CONDITIONAL

**Commit oggetto della review**: 4a8d9a5
**Data**: 2026-05-24
**Iterazione**: v1 (primo giro di review)

---

## Problemi bloccanti (causano FAIL)

Nessun problema bloccante identificato.

---

## Problemi non bloccanti (causano CONDITIONAL)

### NB-1 -- Look-ahead off-by-one nella pivot detection (Cap.15.3)

**Posizione**: Cap.15.3, paragrafo Algoritmo frattale con conferma.

**Problema**: La condizione di conferma del pivot richiede high_{t+n_c} (o low_{t+n_c}). Questo dato e disponibile solo dopo la chiusura della barra t+n_c, ovvero in F_{t+n_c}, non in F_{t+n_c-1} come il testo afferma. Il pivot confermato a t diventa disponibile come feature al tempo t+n_c+1, non al tempo t+n_c.

**Impatto GA**: look-ahead di 1 barra nelle feature di struttura (distanza dal pivot, numero pivot). Con n_c=3, pivot disponibile alla barra t+3 anziche t+4. Impatto sistematico sul ranking dei cromosomi.

**Classificazione**: BUG REALE (look-ahead di 1 barra).

---

### NB-2 -- Formula E[|z|] per la GED errata (Cap.13.2)

**Posizione**: Cap.13.2, bullet point GED.

**Problema**: La formula E[|z|] = 2^{1/kappa} Gamma(2/kappa) / Gamma(1/kappa) e corretta solo per kappa = 2 (Normale). Per kappa=1 (Laplace) da 2.0 anziche 0.707. La formula corretta include un fattore di scala c = [Gamma(1/kappa) / (2^{2/kappa} Gamma(3/kappa))]^{1/2}.

**Impatto GA**: se il GA seleziona GED, il termine E[|z|] nell equazione EGARCH sarebbe sbagliato, distorcendo sigma_hat. Impatto attenuato dal default Student-t (formula corretta).

**Classificazione**: BUG REALE (formula matematica errata).

---

### NB-3 -- Unita di misura di sigma_hat non riconciliate con Cap.8 Parte II (Cap.13.1)

**Posizione**: Cap.13.1 e Cap.8.2 Parte II.

**Problema**: sigma_hat e in unita di log-return (ordine 10^-4). Il range r_{1m} e in punti FIB (ordine 10-100). La condizione |target_1 - p_ref| / sigma_hat produce rapporto non adimensionale. Nessuna conversione esplicita. Il riferimento Parte III Cap.12 in Cap.8 e errato (corretto: Cap.13).

**Impatto GA**: senza conversione esplicita, condizione di emissione non implementabile univocamente. Ranking diversi dei cromosomi in implementazioni diverse.

**Classificazione**: BUG REALE (ambiguita dimensionale).

---

### NB-4 -- Divergenza dalla baseline: rolling vs expanding window (Cap.13.3)

**Problema**: baseline hard-locked congela expanding come default. CAP-03 adotta rolling W=210.000 senza dichiarare la divergenza.

**Classificazione**: MIGLIORA PERFORMANCE.

---

### NB-5 -- Cross-session behavior EMA non specificato (Cap.15.2.1)

**Problema**: la somma infinita attraversa il confine di sessione senza trattamento esplicito. Formula usa sum lambda^j anziche sum lambda^{j-1} (fattore lambda). Impatto su determinismo nelle prime barre di sessione.

**Classificazione**: MIGLIORA PERFORMANCE.

---

### NB-6 -- Soglia retracement delta_pivot ambigua (Cap.15.3)

**Problema**: non specifica su quale barra si verifica il retracement ne quale grandezza di prezzo (high, low, close). Manca formalizzazione come disuguaglianza esplicita.

**Classificazione**: MIGLIORA PERFORMANCE.

---

### NB-7 -- Regime: nessun valore provvisorio per riassunto sessione (Cap.14.2)

**Problema**: scelta tra ultima barra e media e parametro del modello senza valore provvisorio.

**Classificazione**: MIGLIORA PERFORMANCE.

---

## Osservazioni minori

- **M-1**: p-value 0.05 vs baseline 0.01 (Cap.13.4). Divergenza conservativa.
- **M-2**: Fallback EGARCH -> GARCH(1,1) non citato. Rinviato a Parte V.
- **M-3**: Warm-up T_warm=750 del baseline non citato.
- **M-4**: Cross-reference Cap.8 Parte II dice Cap.12 anziche Cap.13.

---

## Classificazione per il supervisore

| # | Problema | Classificazione | Mandare a Development? |
|---|----------|-----------------|------------------------|
| NB-1 | Look-ahead off-by-one pivot detection | BUG REALE | SI |
| NB-2 | Formula E[|z|] GED errata | BUG REALE | SI |
| NB-3 | Unita sigma_hat non riconciliate | BUG REALE | SI |
| NB-4 | Rolling vs expanding non dichiarato | MIGLIORA PERFORMANCE | Attesa supervisore |
| NB-5 | EMA cross-session non specificato | MIGLIORA PERFORMANCE | Attesa supervisore |
| NB-6 | Retracement delta_pivot ambiguo | MIGLIORA PERFORMANCE | Attesa supervisore |
| NB-7 | Regime: nessun default sessione | MIGLIORA PERFORMANCE | Attesa supervisore |
| M-1 | p-value divergenza conservativa | NEUTRO | NO |
| M-2 | Fallback non citato | NEUTRO | NO |
| M-3 | Warm-up non citato | NEUTRO | NO |
| M-4 | Cross-ref Cap.8 | NEUTRO | NO |

---

## Verifica dei 29 Acceptance Criteria

26 su 29 AC soddisfatti. AC #21 (pivot detection) e #26 (determinismo EMA) sono CONDITIONAL per NB-1 e NB-5. AC #29 (REPORT_CAP_03.md) e N/A. Tutti gli altri AC passano.

## Verifica delle 11 Eredita

8 su 11 OK. Eredita 6, 7 (condizioni Cap.8 sigma_hat) e 9 (determinismo) sono CONDITIONAL per NB-3 e NB-5.

---

## Sintesi finale

La Parte III e sostanzialmente ben costruita. EGARCH(1,1), regime, catalogo feature e causalita sono formalizzati coerentemente con N=1. Tre BUG REALI richiedono correzione: (1) look-ahead off-by-one pivot detection; (2) formula E[|z|] GED errata per kappa != 2; (3) unita sigma_hat non riconciliate con Cap.8. Nessuno e strutturalmente devastante. Quattro MIGLIORA PERFORMANCE riguardano ambiguita implementative e una divergenza dal baseline. Verdetto CONDITIONAL: i 3 BUG REALI vanno a Development obbligatoriamente; i 4 MIGLIORA PERFORMANCE sono in attesa di decisione del supervisore.
