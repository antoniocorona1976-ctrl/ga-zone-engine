# Review CAP-04 v3 -- Parte IV

Verdetto: PASS

Commit oggetto: 9852e12 + 687e042 (push origin/main)
Data: 2026-05-25
Natura: Audit ostile finale rework v3 CAP-04 + mini-patch CAP-02 Iterazione 5

---

## Sintesi del verdetto

Il rework v3 chiude correttamente tutti i 9 finding di Review v2: 3 BUG REALI (NB-v2-1 Cap.9.2 esteso, NB-v2-3 razionale (a) rimosso, NB-v2-4 esempio multipli di 5), 1 MIGLIORA PERFORMANCE D-v2-7, 5 NEUTRO opportunistici. Flip-flop D-6 -> D-v2-5 -> D-v3-1 discusso in REPORT righe 281-283. I 15 AC v3 sono OK; 3 AC v2 PARZIALI promossi a OK (AC-v2-3, AC-v2-5, AC-I4-2). Nessuna regressione su 64 AC legacy. Tutti gli esempi numerici usano prezzi multipli di 5. Nessun look-ahead. Determinismo bit-exact preservato. D-v2-7 tecnicamente solida. Verdetto PASS.

---

## Stato dei finding di Review v2 -- verifica esplicita

| ID | Tipo | Stato | Verifica indipendente |
|----|------|-------|----------------------|
| NB-v2-1 | BUG REALE | CHIUSO | CAP_02_parte_II.md:241-251: Cap.9.2 con 9 voci. Voce 8 target_2_type, voce 9 stop_type dominio {structural, synthetic} + popolamento Cap.17.4/18.1 PIV. Riga 253 estesa. |
| NB-v2-3 | BUG REALE | CHIUSO | CAP_04_parte_IV.md:369: razionale (a) rimosso. Unico razionale: Delta_t_cromosoma frozen sul fold. Flip-flop discusso REPORT:281-283. |
| NB-v2-4 | BUG REALE | CHIUSO | CAP_04_parte_IV.md:497: prezzi 27.400, 27.450, 27.500, 27.495, 27.405 multipli di 5. Verifica passo per passo n_osc=2. |
| NB-v2-2/D-v2-7 | MIGLIORA PERF | CHIUSO | CAP_02:51,249 + CAP_04:231,260: dominio bivalente structural/synthetic. Nessun residuo personal. |
| O-v2-1 | NEUTRO | CHIUSO | CAP_04:30: indici di barra b_135, b_210, b_240 + nota notazione. |
| O-v2-2 | NEUTRO | CHIUSO | CAP_04:521: paragrafo target_2_type per trade_range. |
| O-v2-3 | NEUTRO | CHIUSO | CAP_04:428-432: argomento formale + Klein-Moeschberger 2003. |
| O-v2-4 | NEUTRO | CHIUSO | CAP_04:472-562: epsilon_osc ovunque. |
| O-v2-5 | NEUTRO | CHIUSO | CAP_04:478-481: commento cross-session. |

Conteggio finding v2 chiusi: 9/9 OK.

---

## Problemi bloccanti (FAIL)

Nessuno.

Verifica criteri FAIL:
- Look-ahead: nessuno introdotto (9 fix chirurgici).
- Determinismo bit-exact: preservato (esempio verificato passo per passo).
- Tick FIB 5pt: rispettato in tutti gli esempi.
- Contraddizione con CAP-01/02/03: nessuna.

---

## Problemi non bloccanti (CONDITIONAL)

Nessuno.

Verifica indipendente delle aree critiche:
1. NB-v2-1: Cap.6.1 vs Cap.9.2 vs Cap.17.4/Cap.18.1 ora coerenti.
2. D-v2-7: semantica synthetic identica fra stop e target_2.
3. NB-v2-3: razionale (b) strutturalmente difendibile.
4. NB-v2-4: verifica passo per passo presente.
5. O-v2-3: argomento matematicamente corretto.
6. O-v2-4: nessun residuo ambiguo.
7. O-v2-5: warm-up neutralizza edge case.

---

## Osservazioni minori

Nessuna osservazione minore con impatto reale.

Note informative (non finding):
- O-1 v1 NEUTRO non toccato (decisione supervisore): cross-ref Cap.15.2.1 PIII non riportato letteralmente in Cap.16.2.
- O-2 v1 NEUTRO non toccato (decisione supervisore): tie-break arrotondamento target_2 sintetico, caso misura-zero.

---

## Verifica sistematica AC v3 (15 voci)

| AC-ID | Criterio | Esito | Evidenza file:riga |
|-------|----------|-------|---------------------|
| AC-v3-1 | NB-v2-1 chiuso. Cap.9.2 con 9 voci. | OK | CAP_02_parte_II.md:241-251,253 |
| AC-v3-2 | NB-v2-3 chiuso. Flip-flop discusso. | OK | CAP_04:369; REPORT:281-283 |
| AC-v3-3 | NB-v2-4 chiuso. Multipli di 5. | OK | CAP_04:497 |
| AC-v3-4 | D-v2-7 chiuso. Dominio bivalente. | OK | CAP_02:51,249; CAP_04:231,260 |
| AC-v3-5 | O-v2-1 chiuso. Indici di barra. | OK | CAP_04:30 |
| AC-v3-6 | O-v2-2 chiuso. target_2_type Cap.21.4. | OK | CAP_04:521 |
| AC-v3-7 | O-v2-3 chiuso. Limite formale. | OK | CAP_04:428-432 |
| AC-v3-8 | O-v2-4 chiuso. epsilon_osc. | OK | CAP_04:464,472,478-486,495,497,562 |
| AC-v3-9 | O-v2-5 chiuso. Commento cross-session. | OK | CAP_04:478-481 |
| AC-v3-10 | Nessuna regressione. | OK | 3 AC v2 PARZIALI promossi. |
| AC-v3-11 | CARRYOVER.md aggiornato. | OK | Nessun nuovo M-promemoria. |
| AC-v3-12 | REPORT Iter.3. | OK | REPORT_CAP_04.md:277-371 |
| AC-v3-13 | REPORT_02 Iter.5. | OK | REPORT_CAP_02.md:341-393 |
| AC-v3-14 | 00_indice.md. | OK | 00_indice.md:15,31 |
| AC-v3-15 | Committati e pushati. | OK | 687e042, 9852e12 |

Conteggio finale AC v3: 15 OK / 0 PARZIALE / 0 MANCA su 15.

---

## Verifica non-regressione AC v1+v2+I4 (64 voci legacy)

| Bucket | v2 OK | v2 PARZIALE | v3 OK | v3 PARZIALE | Promozioni |
|--------|-------|-------------|-------|-------------|------------|
| AC v1 (44) | 43 | 1 (S-2 NEUTRO) | 43 | 1 (S-2 invariato) | Invariati. |
| AC v2 (12) | 10 | 2 (AC-v2-3, AC-v2-5) | 12 | 0 | AC-v2-3, AC-v2-5 promossi |
| AC I4 (8) | 7 | 1 (AC-I4-2) | 8 | 0 | AC-I4-2 promosso |
| Totale 64 | 60 | 4 | 63 | 1 | 3 promossi; 0 degradati |

Conclusione: 0 AC degradati. 3 AC promossi (AC-v2-3, AC-v2-5, AC-I4-2). PARZIALE residuo S-2 (NEUTRO O-1) per decisione supervisore.

---

## Secondo giro ostile finale

Domanda obbligatoria: sono sicuro di aver trovato tutti i problemi reali?

### 1. Causalita temporale -- nessun look-ahead
Tutti i 9 fix sono chirurgici. La causalita di p_hat_hit e gia garantita da Cap.19.5 (x_tilde in F_{t-1}).

### 2. Determinismo bit-exact
Esempio Cap.21.2 verificato passo per passo: bordo_corrente NONE -> LOW -> HIGH -> LOW produce n_osc=2. Deterministico.

### 3. Tick FIB 5pt -- TUTTI gli esempi verificati
- Cap.16.1: 27.300, 27.250, 27.700, 27.750 -- multipli di 5.
- Cap.16.3: 27.480..27.520 -- multipli di 5.
- Cap.17.2: 27.500, 27.540, 27.570, 27.600 -- multipli di 5.
- Cap.18.2: 27.500, 27.480, 27.520, 27.460, 27.490 -- multipli di 5.
- Cap.21.2 (post NB-v2-4): 27.400, 27.450, 27.500, 27.495, 27.405 -- multipli di 5.
- Cap.21.4: 27.400, 27.500, 27.385, 27.415, 27.360 -- multipli di 5.
TUTTI OK.

### 4. Coerenza Cap.6.1 / Cap.9.2 dopo NB-v2-1
Cap.6.1 tupla 12 campi. Cap.9.2 lista 9 voci (target_1+target_2 combinati nella voce 5; Delta_t_cromosoma e T_touch_max esclusi come tecnici interni dichiarati a riga 253). Coerente.

### 5. D-v2-7 dominio {structural, synthetic} -- tecnicamente solida
Semantica synthetic: stop da d_stop_sigma*sigma_pt, target_2 da k_t2*sigma_pt. Entrambi derivati da regola del modello con scala sigma_pt. Coerenza Cap.18.1 vs Cap.18.3 vs Cap.6.1 vs Cap.9.2 perfetta. Nessuna nuova ambiguita.

### 6. Razionale (b) D-v3-1 tiene da solo
Delta_t_cromosoma costante intra-fold ex ante dal fold in-sample precedente, T_j perp C | x_tilde plausibile per costruzione walk-forward. Difendibile.

### 7. Formalizzazione limite Cap.20.4 -- rigorosa
(i) h_1 >= 0, S_hat in [0,1] -- integrando non-negativo -- monotonicita non decrescente. (ii) Cap finito Delta_t_cromosoma -- integrabilita di h_1. -- integrale su misura zero = 0. Citazione Klein-Moeschberger (2003) cap. 2 appropriata.

### 8. Rinomina epsilon_osc -- tutte le occorrenze aggiornate
Epsilon senza pedice solo riga 464 (epsilon=b in condizione 2). Epsilon_osc righe 472, 482, 485, 486, 495, 497, 562. Nessun residuo ambiguo.

### 9. Pseudocodice cross-session -- corretto
Per t >= 100 (warm-up rispettato), finestra [t-60+1, t-1] dentro la sessione corrente. Commento corretto.

### Altre verifiche del secondo giro
Coerenza Cap.6.1 vs Cap.18.1 vs Cap.18.3 vs Cap.9.2 sul dominio stop_type perfetta. Cap.18.3 titolo Separazione stop strutturale vs stop personale mantiene la separazione. Stop personale operatore fuori scope dal contratto. Razionale (a) rimosso senza riferimenti orfani. Tabella riepilogo coerente con epsilon_osc.

Conclusione del secondo giro ostile: NESSUN nuovo problema reale rilevato.

---

## Citazioni problematiche dal testo

Nessuna citazione problematica rilevata.

---

## Classificazione per il supervisore

| # | Problema | Classificazione | Mandare a Development? |
|---|----------|-----------------|------------------------|
| -- | Nessun problema bloccante o non bloccante rilevato | -- | -- |

Tabella vuota: il rework v3 chiude correttamente tutti i 9 finding di Review v2 senza introdurre nuovi problemi. Nulla da inviare a Development.

---

## Riepilogo per chiusura

- Verdetto finale: PASS
- Conteggio: 0 bloccanti + 0 non bloccanti + 0 osservazioni minori con impatto
- Classificazione: 0 BUG REALI + 0 MIGLIORA PERFORMANCE + 0 NEUTRO nuovi + 0 RISCHIO PEGGIORAMENTO + 0 PROMEMORIA nuovi
- AC v3: 15 OK / 0 PARZIALE / 0 MANCA su 15
- Non-regressione AC v1+v2+I4: 63 OK su 64 voci legacy; 1 PARZIALE NEUTRO residuo (S-2 = O-1 non toccato per decisione supervisore); 0 MANCA; 0 degradati; 3 AC v2 promossi (AC-v2-3, AC-v2-5, AC-I4-2)
- File prodotto: C:/Users/AN/Documents/Projects/ga-zone-engine/reviews/REVIEW_CAP_04_v3_review.md
- Hash commit oggetto: 9852e12 + 687e042 (push origin/main verificato)

Note al supervisore sul flip-flop D-6/D-v2-5/D-v3-1: il REPORT_CAP_04 righe 281-283 discute esplicitamente il flip-flop. Posizione metodologica passata da censoring informativo (v1 D-6) a non informativo con razionale parzialmente sbagliato (v2 D-v2-5) a non informativo con razionale strutturale corretto (v3 D-v3-1). La verifica empirica formale resta in Parte V via Cox-Snell e Schoenfeld stratificato. Il supervisore puo obiettare al checkpoint successivo; in caso di obiezione il rollback e puntuale.

Motivazione del PASS: tutti e 9 i finding di Review v2 sono chiusi correttamente; nessun nuovo problema bloccante o non bloccante introdotto dai fix; tutti i 15 AC v3 OK con evidenza file:riga; nessuna regressione su AC legacy; 3 AC v2 PARZIALI promossi a OK; D-v2-7 tecnicamente solida; flip-flop discusso esplicitamente; tutti gli esempi numerici rispettano il tick FIB 5pt; determinismo bit-exact preservato; nessun look-ahead. Il CAP-04 e pronto per essere chiuso definitivamente come Parte IV del documento metodologico v2.

CAP-04 PRONTO PER CHIUSURA -- 7 condizioni di chiusura sessione: l Orchestratore della sessione corrente puo procedere con la checklist di chiusura (review PASS pubblicata, DEV_STATUS azzerato, documento+report pubblicati, indice aggiornato a CAP-04 PASS con data e hash, ACTIVE_TASK lasciato storico, CARRYOVER aggiornato con eventuali M-promemoria nuovi (atteso: nessuno), riepilogo+prompt-template al supervisore per nuova sessione CAP-05).
