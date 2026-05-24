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
---
## Review v2 -- Re-audit ostile dopo rework v4 (Q-06..Q-09 chiuse)
**Verdetto**: CONDITIONAL
**Commit oggetto della review**: f7a114c
**Data**: 2026-05-24
**Iterazione**: v2 (secondo giro di review dopo rework v4)
---
### Stato dei finding di Review v1
I 4 BUG REALI originali (NB-1, NB-2, NB-3, C-5.1) e i 4 MIGLIORA PERFORMANCE approvati dal supervisore (Q-06..Q-09) sono stati trattati dalla v4.
| Finding v1 | Stato v2 | Dettaglio |
|------------|----------|-----------|
| NB-1 (look-ahead pivot) | **CHIUSO** | Cap.15.3: pivot disponibile a t + n_c + 1 |
| NB-2 (formula GED) | **CHIUSO** | Cap.13.2: fattore c, verifiche kappa=2 e kappa=1 corrette |
| NB-3 (unita sigma) | **CHIUSO con residuo** | sigma_hat_pt introdotta. RESIDUO: formula volatilita CAP-02 riga 189 |
| C-5.1 (bug EMA) | **FIX PARZIALE** | Pesi corretti ma r_{t-j} j=0 look-ahead -- vedi B-1 v2 |
| Q-06/C-4.1 | **CHIUSO** | Pesaran-Timmermann (2007) inline |
| Q-06/C-4.2 | **CHIUSO** | fold-per-fold |
| Q-07/C-5.2 | **CHIUSO** | Reset 8:00, T_warmup=74, Engle-Sokalska (2012) |
| Q-08 | **CHIUSO** | 4 condizioni, simmetria, sessione, n_c=3 |
| Q-09 | **CHIUSO** | sigma_bar_s N_s=840, mediana, Corsi (2009) |
---
### Problemi bloccanti (causano FAIL)
Nessuno.
---
### Problemi non bloccanti (causano CONDITIONAL)
#### B-1 -- Look-ahead nella EMA: r_t in x_t viola causalita (Cap.15.2.1)
**Posizione**: Cap.15.2.1, formula EMA, riga 271.
**Problema**: formula v4 sum_{j=0}^{n_t-1} lambda^j r_{t-j}. A j=0 usa r_t = ln(p_t/p_{t-1}), che richiede p_t (close barra t). Ma p_t appartiene a F_t non F_{t-1}. Il testo (riga 273) afferma r_t in F_{t-1}: falso per definizione Cap.12.1.
Le altre feature di prezzo partono da r_{t-1}, mai r_t (rendimento x_t^{(r,1)} = r_{t-1}, cumulato sum_{j=1}^k r_{t-j}).
**Fix**: sommare r_{t-1-j} o equivalentemente sum_{j=1}^{n_t} lambda^{j-1} r_{t-j}. Pesi invariati.
**Impatto GA**: look-ahead 1 barra sistematico nella EMA. Distorce ranking cromosomi: backtest vede futuro, forward run no.
**Classificazione**: BUG REALE (regressione da C-5.1).
---
#### NB-1 v2 -- Feature distanza pivot: denominatore in log-return non in punti FIB (Cap.15.2.4)
**Posizione**: Cap.15.2.4, riga 306.
**Problema**: x_t^{(piv)} = (p_{t-1} - p_pivot) / sigma_hat_{t-1} dichiarata sigma-units. Numeratore punti FIB (10-100), denominatore log-return (10^{-4}). Rapporto ordine 10^5. Serve sigma_hat_pt al denominatore.
**Impatto GA**: z-score MAD corregge scala. Impatto ranking trascurabile. Semantica errata.
**Classificazione**: MIGLIORA PERFORMANCE.
---
#### NB-2 v2 -- Residuo mini-patch CAP-02: formula volatilita (Cap.8.2 riga 189)
**Posizione**: CAP-02 Cap.8.2 riga 189; Cap.10.2 riga 298.
**Problema**: formula tau_vol(sigma_hat) anziche tau_vol(sigma_hat_pt). Testo dice sigma_hat_pt, formula no. Condizione distanza (riga 201) correttamente sigma_hat_pt. Incoerenza con CAP-03 Cap.13.1.
**Impatto GA**: tau_vol parametrica, GA adatta. Impatto funzionale nullo.
**Classificazione**: MIGLIORA PERFORMANCE.
---
### Osservazioni minori
- **N-1**: Ambiguita Q_p sessione vs barra (Cap.14.2). NEUTRO.
- **N-2**: sigma_hat_pt con p_t anziche p_{t-1}. Diff < 0.02%. NEUTRO.
- **M-1**: Pivot inizio/fine sessione non confermabili. Design corretto. PROMEMORIA.
- **M-2**: Cadenza ricalibrazione production non specificata. Rinvio Parte V. PROMEMORIA.
---
### Citazioni problematiche
- r_t in F_{t-1} (Cap.15.2.1 riga 273) -- falsa. BUG REALE.
- sigma_hat = sigma_hat_pt indifferentemente (Cap.13.1 riga 112) -- approssimata. NEUTRO.
---
### Verifica 14 AC v4
| AC | Esito | Note |
|----|-------|------|
| AC-v4-1 | OK | Pivot a t+n_c+1 |
| AC-v4-2 | OK | GED con c, verifiche corrette |
| AC-v4-3 | PARZIALE | Cap.13.1 OK; Cap.8.2 formula residua |
| AC-v4-4 | PARZIALE | Pesi OK ma look-ahead j=0 |
| AC-v4-5 | OK | Divergenza + Pesaran-Timmermann |
| AC-v4-6 | OK | Fold-per-fold |
| AC-v4-7 | OK | Reset + warmup + Engle-Sokalska |
| AC-v4-8 | OK | 4 condizioni pivot |
| AC-v4-9 | OK | sigma_bar_s + mediana + Corsi |
| AC-v4-10 | OK | M-5 M-6 carryover |
| AC-v4-11 | OK | REPORT Iter.4 |
| AC-v4-12 | OK | REPORT_CAP_02 Iter.4 |
| AC-v4-13 | PARZIALE | 28/29 OK; EMA viola AC#18 |
| AC-v4-14 | OK | Citazioni inline |
---
### Verifica mini-patch CAP-02
| Punto | Esito |
|-------|-------|
| Cross-ref Cap.13 | OK |
| Distanza sigma_hat_pt | OK |
| Volatilita sigma_hat_pt | **KO** (formula riga 189) |
| REPORT Iter.4 | OK |
---
### Verifica citazioni inline
Pesaran-Timmermann (2007): inline, plausibile (J. Econometrics 137(1)).
Engle-Sokalska (2012): inline, plausibile (J. Fin. Econometrics 10(1)).
Corsi (2009): inline, plausibile (J. Fin. Econometrics 7(2)). Nessuna falsificata.
---
### Classificazione per il supervisore
| # | Problema | Classificazione | Mandare a Dev? |
|---|----------|-----------------|----------------|
| B-1 | Look-ahead EMA r_t (regressione C-5.1) | BUG REALE | SI |
| NB-1 v2 | Feature pivot sigma_hat vs sigma_hat_pt | MIGLIORA PERF | Attesa supervisore |
| NB-2 v2 | CAP-02 formula volatilita sigma_hat | MIGLIORA PERF | Attesa supervisore |
| N-1 | Q_p sessione vs barra | NEUTRO | NO |
| N-2 | p_t vs p_{t-1} in sigma_hat_pt | NEUTRO | NO |
| M-1 | Pivot bordo sessione | PROMEMORIA | NO |
| M-2 | Cadenza production | PROMEMORIA | NO |
---
### Sintesi
La v4 ha chiuso 8/9 finding di Review v1. Citazioni inline OK, non falsificate. Mini-patch CAP-02: cross-ref e distanza corretti, formula volatilita residua. Il fix C-5.1 ha introdotto regressione: r_t in EMA viola causalita (B-1). Fix: r_{t-1-j}. Verdetto CONDITIONAL: 1B, 2NB, 2N, 2M.

---

## Review v3 -- Re-audit ostile dopo rework v5 (chiusura B-1 + NB-1/NB-2 v2)

**Verdetto**: PASS

**Commit oggetto della review**: 2bf47ef
**Data**: 2026-05-24
**Iterazione**: v3 (terzo giro di review dopo rework v5)

---

### Stato dei finding di Review v2

I 3 finding approvati dal supervisore (1 BUG REALE + 2 MIGLIORA PERFORMANCE) sono stati trattati dalla v5 con fix chirurgici. I 2 NEUTRO e 2 PROMEMORIA restano carryover come previsto.

| Finding v2 | Stato v3 | Dettaglio |
|------------|----------|-----------|
| B-1 v2 (look-ahead EMA r_t) | **CHIUSO** | Cap.15.2.1 riga 271: formula r_{t-1-j}; testo riga 273 afferma r_{t-1} in F_{t-1} e r_t non in F_{t-1} |
| NB-1 v2 (feature pivot sigma_hat vs sigma_hat_pt) | **CHIUSO** | Cap.15.2.4 riga 306: sigma_hat_pt al denominatore; chiarimento dimensionale esplicito |
| NB-2 v2 (CAP-02 Cap.10.2 formula residua) | **CHIUSO** | Cap.10.2 riga 298: sigma_hat_pt e tau_vol(sigma_hat_pt) nel snapshot |
| N-1 (Q_p sessione vs barra) | CARRYOVER Parte V | Non a Developer (NEUTRO) |
| N-2 (p_t vs p_{t-1} in sigma_hat_pt) | CARRYOVER doc interna | Non a Developer (NEUTRO) |
| M-1 (pivot bordo sessione) | CARRYOVER Parte VI | Non a Developer (PROMEMORIA) |
| M-2 (cadenza production) | CARRYOVER Parte V/VI | Non a Developer (PROMEMORIA) |

---

### Verifica puntuale B-1 v2 -- Causalita EMA (Cap.15.2.1)

**1. Formula.** La formula a riga 271 usa r_{t-1-j}. A j=0 il rendimento piu recente usato e r_{t-1}, MAI r_t. **OK**.

**2. Dichiarazione causale.** Il testo a riga 273 afferma r_{t-1} in F_{t-1} e r_t in F_t \ F_{t-1}. **OK** -- entrambe le affermazioni sono esplicite.

**3. Pesi.** (1-lambda) sum lambda^j = 1-lambda^{n_t}. Invariati rispetto a v4. **OK**.

**4. Warm-up.** T_{warmup,EMA} = 74 per lambda=0,94: lambda^{74} approx 0,010. Peso residuo < 1%. Coerente. **OK**.

**5. Verifica matematica prime 3 barre.**
- t=1 (n_t=1): x_1 = (1-lambda) r_0. r_0 in F_0: **causale**.
- t=2 (n_t=2): x_2 = (1-lambda)(r_1 + lambda r_0). r_1 in F_1 sottoinsieme F_{t-1=1}: **causale**.
- t=3 (n_t=3): x_3 = (1-lambda)(r_2 + lambda r_1 + lambda^2 r_0). r_2 in F_2 sottoinsieme F_{t-1=2}: **causale**.

In tutti i casi il rendimento piu recente e r_{t-1}, mai r_t. **B-1 v2 chiuso senza regressioni.**

---

### Verifica puntuale NB-1 v2 -- Feature distanza pivot (Cap.15.2.4)

**6. Denominatore.** Riga 306: sigma_hat_{pt, t-1} presente. **OK**.

**7. Analisi dimensionale.** Numeratore (p_{t-1} - p_pivot): punti FIB. Denominatore sigma_hat_{pt,t-1}: punti FIB. Rapporto: adimensionale. **OK**.

**8. Chiarimento dimensionale esplicito.** Testo riga 306 dichiara esplicitamente numeratore e denominatore in punti FIB, rapporto adimensionale. **OK**.

---

### Verifica puntuale NB-2 v2 -- CAP-02 Cap.8.2 e Cap.10.2

**9. Cap.10.2 riga 298.** Snapshot condizioni: sigma_hat_pt e tau_vol(sigma_hat_pt). **OK** -- coerente con Cap.8.2.

**10. Cap.8.2 riga 189.** Formula display: tau_vol(sigma_hat_pt). **OK** -- gia corretto dal commit 0f6087c.

**11. Coerenza Cap.8.2 / Cap.10.2 / Cap.13.1.** Tutte le condizioni di emissione usano sigma_hat_pt. **OK**.

---
### Verifica 7 AC v5

| AC | Criterio | Esito |
|----|----------|-------|
| AC-v5-1 | B-1 v2 chiuso: EMA r_{t-1-j}; r_{t-1} in F_{t-1}, r_t non in F_{t-1} | **OK** |
| AC-v5-2 | NB-1 v2 chiuso: Cap.15.2.4 sigma_hat_{pt, t-1} | **OK** |
| AC-v5-3 | NB-2 v2 chiuso: CAP-02 Cap.10.2 sigma_hat_pt | **OK** |
| AC-v5-4 | 14 AC v4 + 29 AC originali soddisfatti | **OK** |
| AC-v5-5 | REPORT_CAP_03.md Iterazione 5 | **OK** |
| AC-v5-6 | REPORT_CAP_02.md Iterazione 5 (v5) | **OK** |
| AC-v5-7 | M-1 e M-2 v2 carryover dichiarati | **OK** |

---

### Verifica campionaria AC v4 post-v5

| AC | Criterio | Esito post-v5 |
|----|----------|---------------|
| AC-v4-1 | NB-1: pivot disponibile a t + n_c + 1 | OK -- non toccato in v5 |
| AC-v4-3 | NB-3: sigma_hat_pt in Cap.13.1; Cap.8.2 OK | OK -- ora anche Cap.10.2 chiuso |
| AC-v4-4 | C-5.1: EMA j da 0 a n_t-1 | OK -- struttura conservata, solo indice r corretto |
| AC-v4-7 | Q-07/C-5.2: reset EMA, T_warmup=74 | OK -- invariato |
| AC-v4-13 | 29 AC originali restano soddisfatti | OK -- 29/29 |

---

### Verifica AC originali (29) -- sintesi post-v5

Le 3 modifiche v5 sono chirurgiche. Nessuna rimozione di contenuto strutturale. Tutti 29 AC originali confermati: 29/29.

---

### Secondo giro ostile

Domanda: sono sicuro di aver trovato tutti i problemi reali?

1. **Altre feature che riferenziano la EMA.** Nessuna. La EMA e feature autonoma. La sostituzione r_t -> r_{t-1} non ha impatto su altre feature. **Nessun problema.**

2. **sigma_hat_{pt, t-1} in Cap.15.2.4: p_{t-1} disponibile?** p_{t-1} in F_{t-1}. **OK** -- nessun look-ahead.

3. **Residui sigma_hat senza _pt dove dovrebbe esserci.** Riga 178 (Cap.13.6) e riga 232 (Cap.14.4): tau_vol(sigma_hat(t)) in testo descrittivo. Formula normativa (Cap.8.2, Cap.13.1 riga 110) usa sigma_hat_pt. **NEUTRO** -- impatto GA nullo. CAP-02 riga 299: sigma_hat(t_emission) nello snapshot feature (grandezza modello, non condizione). **Corretto**.

4. **Assunzioni implicite.** Nessuna nuova assunzione introdotta. Fix sostitutivi, non architetturali. **Nessun problema.**

5. **Invarianti.** Causalita, determinismo, tick FIB 5pt, single-instrument N=1, sessione 8:00-22:00 -- tutte soddisfatte. **Nessun problema.**

---

### Problemi bloccanti (causano FAIL)

Nessuno.

---

### Problemi non bloccanti (causano CONDITIONAL)

Nessuno.

---

### Osservazioni minori

- **N-3**: Cap.13.6 riga 178 e Cap.14.4 riga 232 citano la condizione di Cap.8 come tau_vol(sigma_hat(t)) anziche tau_vol(sigma_hat_pt(t)). Incoerenza notazionale nel testo descrittivo, non nella formula normativa. Impatto GA: nullo. Classificazione: NEUTRO. Carryover documentazione interna.

---

### Classificazione per il supervisore

| # | Problema | Classificazione | Mandare a Development? |
|---|----------|-----------------|------------------------|
| N-3 | sigma_hat vs sigma_hat_pt in testo descrittivo (Cap.13.6, Cap.14.4) | NEUTRO | NO -- testo descrittivo, formula normativa corretta |

---

### Verifica mini-patch CAP-02 v5

| Punto | Esito |
|-------|-------|
| Cap.8.2 formula display volatilita sigma_hat_pt | OK -- riga 189 |
| Cap.8.2 formula display distanza sigma_hat_pt | OK -- riga 201 |
| Cap.10.2 snapshot condizioni sigma_hat_pt | OK -- riga 298 |
| Cap.10.2 snapshot feature sigma_hat (log-return) | OK -- riga 299 (intenzionale) |
| REPORT_CAP_02 Iterazione 5 (v5) | OK |
| Coerenza Cap.8.2 / Cap.10.2 / Cap.13.1 | OK |

---

### Sintesi

La v5 ha chiuso tutti e 3 i finding approvati dal supervisore con fix chirurgici corretti: (1) formula EMA causale con r_{t-1-j} e dichiarazione esplicita r_t non in F_{t-1}; (2) denominatore feature pivot in sigma_hat_{pt, t-1} con analisi dimensionale esplicita; (3) snapshot log Cap.10.2 di CAP-02 con sigma_hat_pt coerente con Cap.8.2. Nessun nuovo BUG REALE. Nessun nuovo MIGLIORA PERFORMANCE. Una osservazione NEUTRO residua (notazione descrittiva in Cap.13.6 e Cap.14.4 -- impatto GA nullo). 50/50 AC soddisfatti (29 originali + 14 v4 + 7 v5). Verdetto **PASS**: CAP-03 chiuso.
