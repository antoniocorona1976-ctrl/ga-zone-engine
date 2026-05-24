# Review CAP-04 -- Parte IV: Geometria zone, target strutturali, survival

**Verdetto**: CONDITIONAL

**Commit oggetto**: 64a31aa + a1de0a8 (Iterazione 1 + fix omissioni REPORT/ACTIVE_TASK)
**Data**: 2026-05-24
**Natura**: Audit ostile Iterazione 1
**Reviewer**: Review Agent

---

## Problemi bloccanti (causano FAIL)

Nessuno.

## Problemi non bloccanti (causano CONDITIONAL)

### NB-1 -- Contraddizione formula vs testo nella selezione di p_ref (Cap.16.1, righe 21-26)

**Impatto GA**: la contraddizione produce due algoritmi di selezione distinti, non equivalenti; due implementazioni conformi al testo produrrebbero p_ref diversi, zone diverse, target e stop diversi, ranking dei cromosomi divergente.

La formula a riga 21 definisce per segnale long: p_ref = max over p in P_low(t). Il testo adiacente lo traduce come il livello del pivot low piu recente confermato nella sessione. Ma max su prezzo e piu recente su timestamp sono criteri diversi quando nella sessione esistono piu pivot low a prezzi distinti. A riga 26 si conferma la regola temporale: si seleziona il piu recente (quello con il timestamp di conferma maggiore).

Esempio: sessione con due pivot low confermati -- uno a 27.300 (confermato alle 10:15) e uno a 27.250 (confermato alle 11:30). La formula max_p seleziona 27.300 (prezzo piu alto); la regola del timestamp seleziona 27.250 (confermato piu tardi). Il p_ref differisce di 50 punti, producendo zone, target e stop incompatibili. Problema analogo per lo short.

Il documento deve scegliere UNO dei due criteri e rendere formula e testo coerenti.

**Classificazione**: BUG REALE
---

### NB-2 -- Termine oscillazione non definito formalmente (Cap.21.2, riga 443)

**Impatto GA**: la classificazione trade_range vs directional dipende dalla condizione 3 (oscillazioni >= n_osc_min), ma oscillazione non ha definizione formale. Implementazioni diverse (crossing completo p_low->p_high, touch di un bordo, inversione locale entro il range) produrranno conteggi diversi e classificazioni divergenti. Questo viola il determinismo bit-exact (Cap.10 Parte II) e altera il comportamento del GA sulla sotto-popolazione di segnali trade_range.

Il documento deve fornire una definizione algoritmica univoca di oscillazione in termini di sequenza di prezzi OHLC delle barre 1-min.

**Classificazione**: BUG REALE

---

## Osservazioni minori

### O-1 -- Cross-reference esplicito a Cap.15.2.1 (T_warmup_EMA) assente in Cap.16.2 (riga 40)
Impatto GA: zero. Concetto presente e corretto, cross-ref esplicito manca.
**Classificazione**: NEUTRO

### O-2 -- Arrotondamento target_2 sintetico: regola di tie-break non specificata (Cap.17.4, riga 189)
Impatto GA: trascurabile (probabilita quasi nulla).
**Classificazione**: NEUTRO

### O-3 -- Flag target_2_type e stop_type: carryover legittimo (Cap.17.4/18.1)
Le flag non compaiono nel payload formale S di Cap.6.1 Parte II. Developer dichiara M-12. Impatto GA: nessuno.
**Classificazione**: PROMEMORIA (carryover M-12)

### O-4 -- Catalogo feature 37 vs 38 (Cap.21.5)
Feature x^(A_range) porta a 38 per trade_range. Developer dichiara M-13. Impatto GA: nessuno.
**Classificazione**: PROMEMORIA (carryover M-13)

### O-5 -- Censoring informativo dichiarato ma non risolto (Cap.19.4, riga 355)
Correttamente dichiarato e rinviato a Parte V. Impatto GA in Parte IV: nessuno.
**Classificazione**: PROMEMORIA (carryover M-7)

### O-6 -- Discrepanza trade_range 80pt tra Cap.5 PI e Cap.6.1 PII
Cap.5 Parte I dice A_range >= 80pt; Cap.6.1 Parte II dice |target_1 - stop_loss| >= 80pt. CAP-04 sceglie Cap.5. Discrepanza pre-esistente.
**Classificazione**: PROMEMORIA (pre-esistente)

---

## Secondo giro ostile

Domanda: Sono sicuro di aver trovato tutti i problemi reali?

1. **Causalita temporale**: verificata su tutti i capitoli. Nessun look-ahead trovato.
2. **Coerenza simboli con CAP-03**: sigma_pt usato correttamente. OK.
3. **Tick FIB = 5pt**: tutti gli esempi numerici verificati (Cap.16.3, 17.2, 18.2, 21.4). Tutti multipli di 5. OK.
4. **Determinismo bit-exact**: Cox MLE con seed nel bundle. Breslow deterministica. Unica ambiguita: oscillazione (NB-2).
5. **Coerenza Cap.8 PII (AND logico)**: Cap.20.2 estende correttamente con E_surv. OK.
6. **Coerenza Cap.11 PII (position lifecycle)**: Cap.18.3 dichiara MAE/MFE/f_stop alimentati. OK.
7. **Trade_range 4 condizioni**: nessun edge case che bypassa, salvo ambiguita oscillazione (NB-2).
8. **Survival Cox cause-specific**: non richiede indipendenza dei rischi. Fine-Gray benchmark. OK.
9. **Citazioni scientifiche**: Fine e Gray (1999) JASA, Grambsch e Therneau (1994) Biometrika. OK.
10. **Numerazione, cross-ref, indice**: Cap.16-21 presenti. Indice aggiornato. OK.
11. **Formula CIF**: p_hat_hit = integrale di h_1 * S. Matematicamente corretta.
12. **Vincolo 80pt trade_range**: discrepanza pre-esistente Cap.5 vs Cap.6.1 (O-6).

---

## Citazioni problematiche dal testo

### Citazione 1 (NB-1)
**Riga 21**: p_ref = max_{p in P_low(t)} p, ovvero il livello del pivot low piu recente confermato nella sessione.
**Problema**: max su prezzo != piu recente su timestamp. Due criteri distinti.
**Classificazione**: BUG REALE

### Citazione 2 (NB-1)
**Riga 26**: nel caso in cui piu pivot dello stesso tipo siano confermati nella sessione, si seleziona il piu recente (quello con il timestamp di conferma maggiore)
**Problema**: conferma criterio temporale, contraddicendo la formula max su prezzo della riga 21.
**Classificazione**: BUG REALE

### Citazione 3 (NB-2)
**Riga 443**: Il numero di oscillazioni del prezzo all interno del range [...] nelle ultime N_osc barre e maggiore o uguale a n_osc_min
**Problema**: oscillazioni non ha definizione algoritmica formale.
**Classificazione**: BUG REALE

---

## Verifica sistematica degli Acceptance Criteria

| AC-ID | Criterio | Esito | Evidenza |
|-------|----------|-------|----------|
| S-1 | 6 capitoli presenti e ordinati | OK | Cap.16-21 verificati |
| S-2 | 19 eredita citate | PARZIALE | 18/19. Eredita 19 (T_warmup_EMA): concetto OK, cross-ref manca (O-1 NEUTRO) |
| S-3 | Paragrafo finale parametri provvisori | OK | Tabella 12 parametri righe 497-512 |
| C16-1 | p_ref da pivot con algoritmo esplicito | PARZIALE | Contraddizione formula vs testo (NB-1 BUG REALE) |
| C16-2 | Trattamento warm-up (M-1 v2 CAP-03) | OK | Cap.16.2 |
| C16-3 | Banda b, cardinalita (2b/5)+1 | OK | Cap.16.3 |
| C16-4 | Condizione raw touch in OHLC | OK | Cap.16.4 |
| C16-5 | Invalidazione pre-touch, parametri provvisori | OK | Cap.16.5 |
| C16-6 | T_min_session provvisorio | OK | Cap.16.6 |
| C16-7 | Coerenza fill worst-case Cap.12.4 | OK | Cap.16.4 |
| C17-1 | Algoritmo selezione target_1 | OK | Cap.17.1 |
| C17-2 | Vincolo 80pt directional | OK | Cap.17.2 |
| C17-3 | Algoritmo selezione target_2 | OK | Cap.17.4 |
| C17-4 | Condizione sigma-units con cross-ref | OK | Cap.17.3 |
| C17-5 | target_1 e target_2 multipli di 5 | OK | Pivot + arrotondamento |
| C18-1 | Algoritmo derivazione stop_loss | OK | Cap.18.1 |
| C18-2 | Vincolo d_stop > b con cross-ref | OK | Cap.18.2 |
| C18-3 | Separazione stop strutturale vs personale | OK | Cap.18.3 |
| C18-4 | RR dichiarato, vincolo rinviato PV | OK | Cap.18.4 |
| C18-5 | Condizionalita regime | OK | Cap.18.5 |
| C19-1 | Variabile obiettivo formalizzata | OK | Cap.19.1 |
| C19-2 | Competing risks espliciti | OK | Cap.19.1-19.2 |
| C19-3 | Formulazione matematica modello primario | OK | Cap.19.2 |
| C19-4 | Feature input sottoinsieme normalizzate | OK | Cap.19.3 |
| C19-5 | Calibrazione fold-per-fold | OK | Cap.19.4 |
| C19-6 | Censoring a destra per expired | OK | Cap.19.4 |
| C19-7 | Output p_hat_hit formalizzato | OK | Cap.19.2 e 19.5 |
| C19-8 | Determinismo e causalita | OK | Cap.19.5 |
| C20-1 | tau_surv parametro cromosoma | OK | Cap.20.1 |
| C20-2 | AND logico con Cap.8 PII | OK | Cap.20.2 |
| C20-3 | Condizionalita tau_surv al regime | OK | Cap.20.3 |
| C20-4 | Filtro implicito fine sessione | OK | Cap.20.4 |
| C21-1 | Range da pivot strutturali | OK | Cap.21.1 |
| C21-2 | Eccezione filtro 80pt | OK | Cap.21.1 e 21.4 |
| C21-3 | Zone ai bordi, target opposto, stop fuori | OK | Cap.21.3 e 21.4 |
| C21-4 | Survival con feature ampiezza range | OK | Cap.21.5 |
| C21-5 | Regola classificazione dir vs trade_range | PARZIALE | 4 condizioni MA oscillazione non definita (NB-2) |
| T-1 | Tick FIB = 5pt rispettato | OK | Tutti gli esempi verificati |
| T-2 | Determinismo bit-exact | PARZIALE | Ambiguita oscillazione (NB-2) |
| T-3 | Causalita F_{t-1} | OK | Verificato |
| T-4 | Nessun parametro fissato | OK | Tabella riepilogo |
| T-5 | Registro tecnico formale | OK | Tutto il documento |
| T-6 | Citazioni scientifiche inline | OK | Fine-Gray, Grambsch-Therneau |
| T-7 | REPORT con misura prima/dopo | OK | REPORT_CAP_04.md |

**Conteggio AC baseline (35 originali)**: 31 OK, 4 PARZIALE (S-2, C16-1, C21-5, T-2), 0 MANCA
Di cui PARZIALE con impatto reale: 2 (C16-1 da NB-1, C21-5+T-2 da NB-2). PARZIALE senza impatto: 1 (S-2, NEUTRO).

---

## Classificazione per il supervisore

| # | Problema | Classificazione | Mandare a Development? |
|---|----------|-----------------|------------------------|
| NB-1 | Contraddizione formula max_p vs testo piu recente in selezione p_ref (Cap.16.1) | BUG REALE | SI -- algoritmo ambiguo, due implementazioni divergenti |
| NB-2 | Oscillazione non definita formalmente in trade_range (Cap.21.2) | BUG REALE | SI -- viola determinismo, impatta classificazione segnali |
| O-1 | Cross-ref Cap.15.2.1 assente in Cap.16.2 | NEUTRO | NO -- non cambia nulla |
| O-2 | Tie-break arrotondamento target_2 sintetico | NEUTRO | NO -- probabilita quasi nulla |
| O-3 | Flag target_2_type/stop_type vs payload (M-12) | PROMEMORIA | NO -- carryover per Planner |
| O-4 | Catalogo 37 vs 38 feature (M-13) | PROMEMORIA | NO -- carryover per Planner |
| O-5 | Censoring informativo (M-7) | PROMEMORIA | NO -- correttamente rinviato |
| O-6 | Discrepanza 80pt Cap.5 vs Cap.6.1 | PROMEMORIA | NO -- pre-esistente |

---

CONDITIONAL: 2 problemi non bloccanti BUG REALE (NB-1 e NB-2) che impediscono il PASS.
Nessun problema bloccante (no look-ahead, no violazione tick FIB, no contraddizione fondamentale).
La correzione e chirurgica per entrambi: scegliere un criterio per p_ref, definire oscillazione.