# Review CAP-05 v2 -- Parte V: Motore genetico, fitness operativa, walk-forward nested, calibrazione

**Verdetto**: PASS

**Commit oggetto**: 16590ae [DEV] CAP-05 v2 rework
**Data**: 2026-05-26
**Natura**: Audit ostile Iterazione 2 (rework post-CONDITIONAL Review v1)
**Reviewer**: Review Agent

---

## Sintesi del verdetto

PASS. I 5 fix chirurgici ratificati dal supervisore (3 BUG REALI NB-1/NB-2/NB-3 + RP-1 T_budget 60h -> 80h + RP-3 theta_CV starting point Parte VII) sono applicati come dichiarato, con coerenza inter-capitolo verificata e nessuna regressione strutturale sugli AC v1. Nessun nuovo BUG REALE emerge dal rework. La tensione residua F=8 vs T_budget=80h sotto i nuovi range M-4 (caso ottimo ~107 ore wall-clock) e dichiarata esplicitamente in Cap.23.6 e rinviata in modo trasparente a Parte VII Cap.34 (compute stress test); il valore 80h ratificato dal supervisore copre il caso ottimo della stima v1 originale (72h) come da decisione.

Si rileva 1 osservazione minore (potenziale residuo formale di NB-1 in Cap.26.1 riga 513) che NON costituisce regressione operativa e NON cambia il comportamento del GA. Tutti i 10 AC v2 sono soddisfatti.

---

## Tabella verifica chiusura finding v1 (5 voci ratificati)

| Finding v1 | Stato v2 | Evidenza testuale |
|-----------|----------|-------------------|
| **NB-1** -- Derivazione 12.800-25.600 min unita incoerenti | **CHIUSO** | Cap.23.6 righe 209-221: derivazione t_eval in [0,74; 1,47] min/cromosoma esplicita; verifica numerica 17.408 * [0,74; 1,47] = [12.882; 25.590] ~= [12.800; 25.600] min con dichiarazione val x min/val = min; rimossa 16.448 x 0,8 (grep su CAP_05_parte_V.md: nessun match per 16.448 come moltiplicatore di tempo, solo come valore di valutazioni nel caso ottimo r_cache=0,15 riga 209). |
| **NB-2** -- K_max=12 vs stratificazione Cap.25.5 | **CHIUSO** | Cap.25.5 riga 427 motivazione 3 aggiornata con K <= K_max = 6 per strato; Cap.26.5 riga 609 voce tabella K_max = 6 con motivazione Harrell 2015 rule N_eventi_strato/K >= 10 con N_eventi_strato >= 60 sotto split 50/50; Cap.26.7 riga 655 valore congelato K_max = 6 con calcolo analitico per strato e rapporto N_eventi_strato/K_max in [10; 32]. Nessun residuo testuale di K_max=12 come valore congelato. |
| **NB-3** -- MAE alla scadenza nomenclatura | **CHIUSO** | Cap.24.1 riga 245 contiene rendimento di chiusura virtuale forzata con nota esplicita che MAE e MFE restano definite secondo accezione standard (Cap.11 PII) e tracciate come metriche di lifecycle in Cap.24.3 riga 288. Grep su MAE alla scadenza: 0 match nel documento. |
| **RP-1** -- T_budget 60h vs caso ottimo 72h | **CHIUSO** (ratificato) | Cap.26.2 riga 523 dichiara T_budget = 80 ore con motivazione 11% margine sul caso ottimo v1 72 ore; Cap.26.5 riga 603 voce tabella aggiornata; Cap.23.6 riga 223 dichiara tensione residua sotto i nuovi range M-4 (caso ottimo F=8 ~ 107 ore wall-clock eccede T_budget=80h) e la rinvia a Parte VII Cap.34. Scelta 80h vs 75h motivata REPORT Decisioni rilevanti (margine robustezza > costo). |
| **RP-3** -- Soglia theta_CV = 0,5 senza fonte | **CHIUSO** (ratificato) | Cap.25.5 riga 429: theta_CV = 0,5 dichiarato come starting point per il primo run di calibrazione, in assenza di rule of thumb consolidata in letteratura per CV di coefficienti Cox; rinvio empirico a Parte VII; Cap.26.5 riga 622 con flag (starting point, riconsiderato Parte VII). Nessuna citazione di facciata aggiunta. |

---

## Tabella AC v2 (10 voci AC-v2-1..10)

| AC-ID | Esito | Nota Reviewer |
|-------|-------|---------------|
| AC-v2-1 | OK | Cap.23.6 righe 209-221: range derivato 17.408 * [0,74; 1,47] = [12.882; 25.590] ~= [12.800; 25.600] min. Verifica unita esplicita riga 221 val x min/val = min. Esempio numerico verificabile. |
| AC-v2-2 | OK | Scelta opzione (a) motivata nel REPORT su 4 punti (conservativita MLE, coerenza architettonica, robustezza audit, costo compute); Cap.25.5 riga 427 con K_max=6 per strato e calcolo N_eventi_strato/K_max in [10; 32]; Cap.26.7 riga 655 congelato 6; Cap.26.5 riga 609 tabella coerente. Nessuna contraddizione residua. |
| AC-v2-3 | OK | Cap.24.1 riga 245: rendimento di chiusura virtuale forzata con nota esplicita su accezione standard MAE/MFE; grep MAE alla scadenza -> 0 match. Cap.24.3 riga 288 traccia MFE/MAE post-target_1 con accezione corretta. |
| AC-v2-4 | OK | Cap.26.2 riga 523 T_budget=80h; Cap.26.5 riga 603 tabella; Cap.23.6 riga 223 dichiara tensione residua sotto i nuovi range M-4 con rinvio a Parte VII Cap.34. Scelta 80h motivata REPORT Decisioni rilevanti sezione RP-1 (4 motivazioni). |
| AC-v2-5 | OK | Cap.25.5 riga 429 dichiarazione esplicita starting point Parte VII + rinvio Cap.31; Cap.26.5 riga 622 flag corrispondente; REPORT Domande aperte e Criterio di rollback annotano natura provvisoria. Nessuna citazione di facciata. |
| AC-v2-6 | OK | Tabella no-regressione AC v1 in REPORT: 3 AC promossi PARZIALE -> OK (AC-23-5, AC-24-2, AC-26-8); 1 PARZIALE residuo (AC-2 carryover); 0 regressioni; 3 rafforzati. |
| AC-v2-7 | OK | REPORT include sezione ## Iterazione 2 con tabella sintesi, decisioni rilevanti (motivazione NB-2 e RP-1), verifica AC v2, no-regressione AC v1, criterio rollback v2. |
| AC-v2-8 | OK | CARRYOVER.md non modificato come da atteso. |
| AC-v2-9 | OK | 00_indice.md riga 40: Parte V IN REVIEW v2. |
| AC-v2-10 | OK | Check post-Developer Orchestratore: tutti 6 OK; commit 16590ae; DEV_STATUS = READY_FOR_REVIEW. |

**Sintesi AC v2**: 10/10 OK.

---

## Tabella no-regressione AC v1 (52 voci)

Verifica per perimetro completo dei 52 AC v1, raggruppata per sezione:

| Gruppo AC | v1 | v2 | Cambiamento |
|-----------|----|----|-------------|
| Struttura generale (AC-1..AC-5) | 4 OK + 1 PARZIALE (AC-2) | 4 OK + 1 PARZIALE | AC-2 resta PARZIALE come carryover documentazione interna (eredita 16 e 41), fuori scope v2 per decisione supervisore. Reviewer v1 dichiarato non bloccante. |
| Cap.22 Cromosoma (AC-22-1..7) | 7 OK | 7 OK | Cap.22 strutturalmente invariato. Vincolo sum_j s_j <= K_max preserva valenza formale; il valore K_max=6 e congelato in Cap.26.5/26.7. Nessuna regressione. |
| Cap.23 Operatori GA (AC-23-1..7) | 6 OK + 1 PARZIALE (AC-23-5) | 7 OK | **AC-23-5 promosso PARZIALE -> OK**: derivazione coerente unita (NB-1 chiuso). |
| Cap.24 Fitness (AC-24-1..10) | 9 OK + 1 PARZIALE (AC-24-2) | 10 OK | **AC-24-2 promosso PARZIALE -> OK**: rendimento di chiusura virtuale forzata sostituisce MAE alla scadenza (NB-3 chiuso). MAE/MFE coerenti accezione standard. |
| Cap.25 Walk-forward (AC-25-1..10) | 10 OK | 10 OK (AC-25-6 rafforzato) | AC-25-6 rafforzato per K_max=6 per strato; rollback CV>theta_CV=0,5 con flag starting point Parte VII (RP-3). Nessuna regressione. |
| Cap.26 Calibrazione (AC-26-1..9) | 8 OK + 1 PARZIALE (AC-26-8) | 9 OK (AC-26-2 rafforzato) | **AC-26-8 promosso PARZIALE -> OK**: K_max=6 congelato (NB-2 chiuso). **AC-26-2 rafforzato**: T_budget=80h (RP-1). |
| Vincoli trasversali (AC-T-1..9) | 9 OK | 9 OK | Tutti i vincoli preservati. Citazioni inline non alterate. |

**Sintesi no-regressione**: 47 AC v1 OK invariati; 3 promossi PARZIALE -> OK (AC-23-5, AC-24-2, AC-26-8); 3 rafforzati (AC-25-6, AC-26-2, AC-26-8); 1 resta PARZIALE come carryover (AC-2, fuori scope v2). **Nessuna regressione introdotta dal rework**.

---

## Finding NUOVI eventuali

Nessun nuovo BUG REALE, MIGLIORA PERFORMANCE, o RISCHIO PEGGIORAMENTO emerge dal rework v2. Si rileva 1 osservazione minore (NEUTRO) di natura formale:

### O-v2-1 -- Frase Cap.26.1 riga 513 con mescolanza ambigua valutazioni vs minuti

**Contesto**. La motivazione di G_max=150 in Cap.26.1 riga 513 scrive:

> Compute budget P * G_max valutazioni ~= 19.328 (Cap.23.6), dentro il range 12.800-25.600 min single-thread di M-4 sotto le ipotesi di r_cache del caso centrale.

La frase mescola formalmente unita: 19.328 e un numero di valutazioni (P * (1 + G_max) = 128 * 151 = 19.328 naive senza caching), il range [12.800; 25.600] e in minuti single-thread. La locuzione ~= 19.328 ... dentro il range 12.800-25.600 min suggerisce che 19.328 stia dentro un range di minuti, che e la stessa categoria di errore formale che il NB-1 originale aveva identificato a Cap.23.6.

**Impatto GA**: zero operativo. Il numero 19.328 e coerente come valutazioni naive (N_eval^naive definita in Cap.23.6 riga 200) e Cap.23.6 chiarisce immediatamente dopo che il prodotto val x min/val produce il range minuto. La frase di Cap.26.1 e una motivazione qualitativa per G_max=150 (compute budget sostenibile), non una derivazione formale. Il Reviewer v1 non aveva flaggato questa specifica frase perche il focus di NB-1 era Cap.23.6.

**Classificazione**: NEUTRO (residuo formale di NB-1; non impatta il comportamento del GA, non distorce il ranking, non viola la matematica; coerenza dimensionale ristabilita in Cap.23.6 in modo esplicito). NON e una regressione: era gia presente in v1 con la stessa formulazione, il Reviewer v1 non l aveva flaggata.

**Decisione Reviewer v2**: NON e un finding bloccante; e un osservazione minore. NON va a Developer di default.

---

## PROMEMORIA / M-promemoria nuovi

Nessun nuovo M-promemoria emerge dal rework v2. La tensione residua F=8 vs T_budget=80h sotto i nuovi range M-4 (~107 ore caso ottimo) e gia rinviata a Parte VII Cap.34 (compute stress test) come dichiarato in Cap.23.6 riga 223. Non costituisce nuovo M-promemoria.

---

## Classificazione per il supervisore

Verdetto PASS -- nessun finding da classificare per decisione supervisore.

Per completezza, l unica osservazione minore registrata:

| # | Problema | Classificazione | Default | Mandare a Development? |
|---|----------|-----------------|---------|------------------------|
| 1 | O-v2-1 -- Frase Cap.26.1 riga 513 con mescolanza ambigua valutazioni vs minuti | NEUTRO | NO -- ignorato | NO (residuo formale di NB-1; zero impatto operativo; era presente in v1 senza flag) |

---

## Verdetto finale

**PASS**

Il rework v2 di CAP-05 chiude tutti e 5 i finding ratificati dal supervisore (3 BUG REALI NB-1/NB-2/NB-3 + RP-1 ratificato T_budget=80h + RP-3 ratificato starting point Parte VII) con interventi chirurgici coerenti fra capitoli. Nessuna regressione strutturale sugli AC v1. I 10 AC v2 sono tutti OK. Tre AC v1 sono stati promossi da PARZIALE a OK (AC-23-5, AC-24-2, AC-26-8). Tre AC v1 sono stati rafforzati (AC-25-6, AC-26-2, AC-26-8). Un AC v1 resta PARZIALE come carryover documentazione interna (AC-2, fuori scope v2 per decisione supervisore).

La tensione residua F=8 vs T_budget=80h sotto i nuovi range M-4 (~107 ore caso ottimo wall-clock) e dichiarata trasparentemente in Cap.23.6 riga 223 e rinviata a Parte VII Cap.34 (compute stress test). Il valore T_budget=80h ratificato dal supervisore copre il caso ottimo della stima v1 originale (72h) come da decisione esplicita. Questo NON e un nuovo BUG: il documento riconosce onestamente la tensione e la rinvia al ciclo di Parte VII.

L unica osservazione minore (O-v2-1) sulla frase Cap.26.1 riga 513 e un residuo formale di NB-1 che il Reviewer v1 non aveva flaggato; zero impatto operativo sul GA; non bloccante. NON va a Developer.

Il bundle frozen che esce dalla Parte V con questo rework e tecnicamente solido: il GA puo essere implementato sulla base di Cap.22-26 senza ambiguita su cromosoma, operatori, fitness, penalita, walk-forward, protocolli di rollback, congelamento numerico. Il fronte di Pareto F_1 prodotto dal motore cosi specificato e interpretabile in Parte VII (Cap.31-36).

**Chiusura sessione CAP-05**: l Orchestratore puo procedere con le 7 condizioni di chiusura.
