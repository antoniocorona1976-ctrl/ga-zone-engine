# Review CAP-05 v4 -- Parte V: Motore genetico, fitness operativa, walk-forward nested, calibrazione

**Verdetto**: PASS

**Commit oggetto**: `dcdcaee` [DEV] CAP-05 v3 rework: NB-v3-1 (opt b K_max=6 segnali eseguiti) + NB-v3-2 (opt a T_budget=80h riallineata) READY_FOR_REVIEW
**Data audit**: 2026-05-26
**Natura**: Audit ostile v4 della chiusura sostanziale dei 2 BUG REALI v3 (NB-v3-1 + NB-v3-2)
**Reviewer**: Review Agent (audit indipendente)

---

## Sintesi del verdetto

**PASS**. I 2 BUG REALI di Review v3 (NB-v3-1 e NB-v3-2) sono **chiusi sostanzialmente** con rework chirurgico (~20 righe diff effettive). Nessuna regressione su AC v1 + v2 + T (71 AC pregressi). 5 AC riclassificati PARZIALE in Review v3 (AC-25-6, AC-26-2, AC-26-8, AC-v2-2, AC-v2-4) sono effettivamente promossi nuovamente a OK.

I 3 NEUTRO (O-v3-1, O-v3-2, O-v2-1) sono confermati come lasciati inalterati per decisione supervisore. O-v3-1 e di fatto risolto come *conseguenza* del nuovo range (la riga ora dichiara valore centrale 250).

Sono emerse 2 **osservazioni minori** che il documento contiene come residui formali del rework v3:
1. Incoerenza testuale tra Cap.23.6 riga 223 ("riduzione di $F$ a 2-3") e Cap.26.2/26.5 ("riduzione di $F$ a ~6") -- entrambe valide ma con rationale diverse.
2. Il "fallback Harrell-strict $K_{max}^{strict}=4$" e dichiarato testualmente come "ammesso se Parte VII Cap.31 mostra instabilita", ma NON ha trigger operativo esplicito in Parte V.

Entrambi non sono BUG REALI: il primo e residuo formale (Cap.23.6 non era nel perimetro chirurgico del rework v3), il secondo e una scelta architetturale (la Review v3 menzionava il fallback come carryover testuale).

---

## Tabella verifica AC v3 (10 voci AC-v3-1..AC-v3-10)

| AC-ID | Criterio | Esito | Evidenza |
|-------|----------|-------|----------|
| **AC-v3-1** | NB-v3-1 chiuso. Cap.25.5 e Cap.26.7 allineate sulla definizione di $N_{eventi}$, aritmetica corretta, $K_{max}$ coerente | **OK** | Cap.25.5 riga 427 (modificata) dichiara accezione "segnali eseguiti" entranti nella partial likelihood; nuovo paragrafo riga 429 ("Nota sulla definizione operativa di $N_{eventi}$ rework v3") con divergenza Harrell-strict esplicitata ($N^{strict} \in [84; 266]$ fold, $\in [42; 133]$ strato, $K_{max}^{strict} \leq 4$, $42/4 = 10{,}5$). Cap.26.7 righe 651-655 (riscritte) con range fold $[120; 380]$ allineato a Cap.25.5, aritmetica $120/2 = 60$ corretta, range strato $[60; 190]$. Cap.26.7 nuovo paragrafo riga 657 con stesso calcolo. Cap.26.5 riga 611 motivazione tabella aggiornata. **Verifiche numeriche**: $84/2 = 42$, $42/4 = 10{,}5$, $inom{37}{6}/inom{37}{4} = 35{,}2$: tutti coerenti |
| **AC-v3-2** | NB-v3-2 chiuso. Cap.26.2 + Cap.26.5 non citano 72h come motivazione; cita 107h POST-fix v2 | **OK** | Cap.26.2 riga 525 (riscritta) cita esplicitamente "calcolo aggiornato di Cap.23.6 -- 107h caso ottimo / 213h caso pessimo"; dichiara "$80 < 107$h ovvero $\sim 6$ fold completati"; copertura ridotta a (i) run calibrazione iniziale + (ii) stima Cap.23.6 originale ~72h pre-M-4 come *valore storico*. Cap.26.5 riga 605 motivazione tabella aggiornata. Calcoli: $107 \cdot 6/8 = 80{,}25$, $80/107 \cdot 8 = 5{,}98$: coerenti |
| **AC-v3-3** | O-v3-1, O-v3-2, O-v2-1 lasciati inalterati | **OK** | (a) O-v3-1: "valore centrale 120" e sostituita con "valore centrale 250" come conseguenza del nuovo range; non intervento diretto. (b) O-v3-2: Cap.26.5 riga 611 mantiene la dicitura. (c) O-v2-1: Cap.26.1 riga 515 inalterato. REPORT Iterazione 3 dichiara onestamente |
| **AC-v3-4** | Nessuna regressione su 71 AC pregressi | **OK** | 5 AC riclassificati PARZIALE in Review v3 promossi nuovamente a OK. AC-2 carryover resta PARZIALE come pre-v3 (non bloccante) |
| **AC-v3-5** | Nessuna modifica strutturale. ~25 righe modificate stimate | **OK** | Diff git: 20 righe effettive. Modifiche limitate a Cap.25.5, Cap.26.2, Cap.26.5, Cap.26.7. Cap.22.6, Cap.22.7 vincolo 4, Cap.25.1 invariati come dichiarato |
| **AC-v3-6** | REPORT include sezione "## Iterazione 3" | **OK** | `reports/REPORT_CAP_05.md` sezione dalla riga 330 con tabella sintesi + opzioni a/b/c motivate + misura prima/dopo + tabella no-regressione + dichiarazione 3 NEUTRO |
| **AC-v3-7** | 00_indice.md riporta Parte V "IN REVIEW v3" | **OK** | Riga 40 dell'indice: "IN REVIEW v3" dal commit ORCH `279b6ba` |
| **AC-v3-8** | CARRYOVER.md M-11 aggiornata | **OK** | Riga 31 di CARRYOVER.md: M-11 ora dichiara accezione "segnali eseguiti" + divergenza Harrell-strict + cross-ref Cap.26.7 |
| **AC-v3-9** | File committati e pushati. Working tree pulito | **OK** | HEAD = `dcdcaee` su origin/main; git status mostra solo `.claude/scheduled_tasks.lock` (tollerato) |
| **AC-v3-10** | Commit con messaggio specificato | **OK** | Commit `dcdcaee` -- messaggio conforme al task |

**Sintesi AC v3**: 10/10 OK.

---

## Verifica chiusura sostanziale di NB-v3-1

### Coerenza Cap.25.5 e Cap.26.7

Verifica bit-exact:

| Aspetto | Cap.25.5 riga 427+429 | Cap.26.7 riga 649+653+657 | Coerenza |
|---------|------------------------|----------------------------|----------|
| Definizione $N_{eventi}$ | "osservazioni eseguite entranti nella partial likelihood ... target_1_hit + stopped + expired posttrigger_timeout censurate" | "cardinalita delle osservazioni eseguite (target_1_hit, stopped, e expired posttrigger_timeout censurate)" | **coerente** |
| Range fold | $\in [120; 380]$ | $\in [120; 380]$ (valore centrale 250) | **coerente** |
| Range strato | $\in [60; 190]$ | $\in [60; 190]$ (derivato da $120/2 = 60$) | **coerente** |
| Caso pessimo strato | 60 | 60 | **coerente** |
| $K_{max}$ | 6 | 6 | **coerente** |
| Rapporto N/K | $\in [10; 32]$ | $\in [10; 32]$ | **coerente** |
| Divergenza Harrell-strict | Si ($N^{strict} \in [84; 266]$/fold, pessimo strato 42, $K^{strict} \leq 4$) | Si (stessi numeri) | **coerente** |

**Aritmetica verificata**:
- $84/2 = 42$ (caso pessimo strato Harrell-strict) -- corretto.
- $42/4 = 10{,}5 \geq 10$ (Harrell-strict K=4 marginale) -- corretto.
- $120/2 = 60$ (caso pessimo strato accezione documento) -- corretto. **L'aritmetica errata baseline "$[60/2; 264/2] \cdot 2 = [60; 190]$" non e piu presente**.
- $inom{37}{6} = 2.324.784$ e $inom{37}{4} = 66.045$: ratio = 35,2 -- corretto.

### Onesta della divergenza Harrell-strict

Il documento dichiara la divergenza in modo trasparente in **entrambi** i capitoli (Cap.25.5 riga 429 + Cap.26.7 riga 657), riportando il calcolo Harrell-strict completo come fallback conservativo. La motivazione (informativita osservazioni censurate via partial likelihood) e statisticamente discutibile -- la pratica Harrell-strict considera solo eventi non-censurati perche il power di stima dei $eta_j$ e dominato dagli eventi -- ma il documento la dichiara come *scelta operativa*, non come *risultato matematico*. La motivazione integrativa "redundanza informativa del catalogo" e ammissibile come argomento euristico.

Non si rileva manipolazione testuale: la divergenza e esplicita e supportata da numeri.

### Fallback $K_{max}^{strict}=4$ -- operativamente attivabile?

Il documento dichiara il fallback in Cap.26.7 riga 659: "Una eventuale riconsiderazione verso la pratica Harrell-strict ($K_{max} = 4$) e ammessa come fallback se Parte VII (Cap.31) mostra che la stima MLE e instabile."

**Manca trigger operativo esplicito** per attivare $K_{max}=4$. Il rollback operativo dichiarato in Parte V e solo $	heta_{CV} > 0{,}5$ verso **opzione (a) interaction term** (NON verso $K_{max}=4$). Quindi il fallback Harrell-strict e dichiarato come *opzione architettonica testuale* da riconsiderare in Parte VII Cap.31, non come *trigger operativo* in Parte V.

Classifico questa come **osservazione minore** (non bloccante): la Review v3 chiedeva di esplicitare il fallback, e il documento lo esplicita come opzione di Parte VII. Una soglia operativa e oggetto naturale di Parte VII (decisione empirica), non di Parte V.

---

## Verifica chiusura sostanziale di NB-v3-2

### Riallineamento motivazione $T_{budget}=80$h

Verifica bit-exact:

| Aspetto | Cap.23.6 riga 223 | Cap.26.2 riga 525 | Cap.26.5 riga 605 | Coerenza |
|---------|-------------------|---------------------|---------------------|----------|
| Calcolo aggiornato POST-fix v2 | "107 ore ottimo / 213 ore pessimo" | "107 ore wall-clock ottimo / 213 ore pessimo" | "NON copre caso ottimo F=8 (~107 ore)" | **coerente** |
| Dichiarazione "80h NON copre F=8" | "il caso ottimo eccede il budget" | "$T_{budget} = 80$ ore non copre il caso ottimo $F = 8$ aggiornato" | "NON copre caso ottimo F=8 aggiornato post-M-4" | **coerente** |
| Riferimento 72h originale (pre-M-4) | "stima Cap.23.6 ORIGINALE (~72 ore, pre-riallineamento M-4)" | "stima Cap.23.6 ORIGINALE (~72 ore wall-clock pre-riallineamento M-4), valore storico per tracciabilita" | "stima Cap.23.6 originale (~72 ore pre-M-4)" | **coerente** -- 72h e citato come *valore storico*, non come motivazione corrente |
| Rinvio Parte VII Cap.34 | Si | Si | Si | **coerente** |

**La motivazione "72h ottimo F=8" del v2 NON e piu presente come motivazione del valore corrente.** E invece citata come *valore storico per tracciabilita*. La contraddizione interna del v2 e risolta.

### Calcoli verificati

- $107 \cdot 6/8 = 80{,}25$ -- F=6 compatibile con 80h budget. Corretto.
- $80/107 = 0{,}748$, quindi $0{,}748 \cdot 8 = 5{,}98$ fold completati nel caso ottimo. Documento dichiara "~6 fold completati". Coerente.
- $80 - 107/8 = 80 - 13{,}4 = 66{,}6$h. Aritmeticamente corretto (sotto caso ottimo).

**Osservazione minore**: la frase "66,6 ore wall-clock disponibili dopo il fold di calibrazione" usa il caso *ottimo* del fold di calibrazione (13.4h). Il caso pessimo del singolo fold e $25.600/16 = 26{,}67$h, quindi margine residuo reale sotto pessimo = $80 - 26{,}67 = 53{,}3$h, non 66.6h. Non e errore aritmetico ma e ambiguita testuale.

### Coerenza con Cap.24.6 (aggregazione cross-fold)

Cap.26.2 riga 525 dichiara: "bundle parziale a fold ~6 nel caso ottimo, con aggregazione cross-fold di Cap.24.6 operante su mediana di ~6 valori (varianza inflated rispetto a F=8 pieno); robustezza preservata dalla scelta della mediana cross-fold di Cap.24.6 (robusta a fold mancanti)".

Cap.24.6 (riga 326) formalizza la mediana su $k \in \{1, \ldots, F\}$ con $F=8$ provvisorio; quando il run e interrotto a F effettivo 6, l'interfaccia tra Cap.26.2 e Cap.24.6 e ora *testuale* (Cap.26.2 dichiara F effettivo $pprox 6$). Cap.24.6 non e stato toccato dal rework v3 e non formalizza esplicitamente cosa significhi F quando il run e interrotto. **Non e BUG REALE** -- Cap.26.2 esplicita il trade-off e rinvia a Parte VII Cap.34. Ma e una **osservazione minore**.

### Carryover esplicito a Parte VII Cap.34

Cap.26.2 riga 525 + Cap.26.5 riga 605 + Cap.23.6 riga 223 rinviano tutti a Parte VII Cap.34 (compute stress test). Coerente fra i tre punti.

**Discrepanza testuale rilevata**: Cap.23.6 dice "F a 2-3", Cap.26.2/26.5 dicono "F a ~6". Le rationali differiscono (F=2-3 = F effettivo CAP-01 storico; F=6 = F massimo compatibile con 80h). Cap.23.6 riga 223 non e stata aggiornata nel rework v3 (out-of-scope). Impatto operativo nullo: la decisione e a Parte VII Cap.34 empiricamente.

---

## Verifica no-regressione sugli AC v1 + v2 + T

| AC-ID | Esito v2 | Esito v3 | Esito v4 | Verifica |
|-------|----------|----------|----------|----------|
| AC-1, AC-3, AC-4, AC-5 | OK x4 | OK x4 | **OK x4** | Struttura Cap.22-26 invariata |
| AC-2 | PARZIALE | PARZIALE | **PARZIALE** | Eredita 16/41 cross-ref letterale, non in scope rework v3 |
| AC-22-1..AC-22-7 | OK x7 | OK x7 | **OK x7** | Cap.22 non modificato |
| AC-23-1..AC-23-7 | OK x7 | OK x7 | **OK x7** | Cap.23 non modificato |
| AC-24-1..AC-24-10 | OK x10 | OK x10 | **OK x10** | Cap.24 non modificato |
| AC-25-1..AC-25-5, AC-25-7..AC-25-10 | OK x9 | OK x9 | **OK x9** | Cap.25.1-25.4, 25.6-25.10 non modificati |
| **AC-25-6** | OK | PARZIALE | **OK promosso nuovamente** | Cap.25.5 riga 427+429 allineata a Cap.26.7 |
| AC-26-1, AC-26-3, AC-26-4, AC-26-6, AC-26-7, AC-26-9 | OK x6 | OK x6 | **OK x6** | Cap.26.1, 26.3, 26.4, 26.6, 26.8 non modificati |
| **AC-26-2** | OK | PARZIALE | **OK promosso nuovamente** | Cap.26.2 riga 525 riscritta con 107h POST-fix v2 |
| AC-26-5 | OK | OK | **OK** | Cap.26.5 tabella aggiornata (righe 605 + 611) |
| **AC-26-8** | OK | PARZIALE | **OK promosso nuovamente** | Cap.26.7 riscritto: aritmetica corretta + divergenza Harrell-strict |
| AC-T-1..AC-T-9 | OK x9 | OK x9 | **OK x9** | Vincoli trasversali preservati |
| AC-v2-1 | OK | OK | **OK** | NB-1 chiuso, non toccato dal rework v3 |
| **AC-v2-2** | OK | PARZIALE | **OK promosso nuovamente** | NB-2 chiuso sostanzialmente in v3 via opzione (b) |
| AC-v2-3 | OK | OK | **OK** | NB-3 chiuso, non toccato dal rework v3 |
| **AC-v2-4** | OK | PARZIALE | **OK promosso nuovamente** | RP-1 chiuso sostanzialmente in v3 via opzione (a) |
| AC-v2-5..AC-v2-10 | OK x6 | OK x6 | **OK x6** | Non toccati dal rework v3 |

**Sintesi no-regressione v4**: 81 AC totali. 80 OK + 1 PARZIALE (AC-2 carryover, non bloccante). 5 AC riclassificati PARZIALE in v3 effettivamente promossi nuovamente a OK. Nessuna nuova regressione.

---

## Verifica chiusure CARRYOVER

| M-ID | Stato pre-v3 | Stato post-v3 | Verifica v4 |
|------|--------------|---------------|-------------|
| M-4 | CLOSED-CAP-05 | invariato | **OK** |
| M-5..M-10 | CLOSED-CAP-05 | invariati | **OK** |
| **M-11** | CLOSED-CAP-05 (K_max=6) | aggiornato: accezione "segnali eseguiti" + divergenza Harrell-strict in Cap.26.7 | **OK** |
| M-14 | CLOSED-CAP-05 | invariato | **OK** (coerenza con M-11 ripristinata) |
| M-15 | CLOSED-CAP-05 | invariato | **OK** |
| M-2 v2 | CLOSED-CAP-05 parziale | invariato | **OK** |
| M-16 condizionale | OPEN-CONDIZIONALE | invariato | **OK** |

**Sintesi CARRYOVER v4**: nessun nuovo M-promemoria. M-11 aggiornata correttamente.

---

## Audit ostile -- finding nuovi emersi dal rework v3

### O-v4-1 -- Cap.23.6 riga 223 raccomanda "F a 2-3" vs Cap.26.2/26.5 "F a ~6"

**Evidenza**: Cap.23.6 riga 223: "riduzione di $F$ a **2-3** (run di calibrazione + walk-forward leggero)" vs Cap.26.2 riga 525 (rework v3): "riduzione di $F$ a $\sim 6$ (compatibile con 80 h: $107 \cdot 6/8 pprox 80$ ore)".

**Analisi**: rationali diverse (F=2-3 = F effettivo CAP-01 storico; F=6 = F massimo per 80h). Cap.23.6 out-of-scope rework v3.

**Impatto GA**: zero. Decisione F operativa a Parte VII Cap.34.

**Classificazione**: **NEUTRO**.

### O-v4-2 -- Cap.26.7 fallback K^strict=4 senza trigger operativo Parte V

**Evidenza**: Cap.26.7 riga 659: fallback dichiarato come opzione Parte VII Cap.31, senza soglia operativa Parte V.

**Analisi**: la Review v3 chiedeva esplicitare il fallback; il documento lo esplicita come opzione di Parte VII. Soglia operativa naturale di Parte VII.

**Impatto GA**: nullo. Rollback opzione (a) interaction term gia operativo via theta_CV > 0.5.

**Classificazione**: **NEUTRO**.

### O-v4-3 -- Cap.26.2 "margine residuo 66.6h" usa caso ottimo

**Evidenza**: "$80 - (107/8) pprox 66{,}6$ ore disponibili dopo il fold di calibrazione". 107/8 = 13.4h e per-fold ottimo. Caso pessimo per-fold = 26.67h; margine residuo reale 53.3h.

**Analisi**: ambiguita testuale; la frase "anche con $t_{eval}$ pessimo" e onesta ma il numero 66.6h e margine ottimo.

**Impatto GA**: nullo.

**Classificazione**: **NEUTRO**.

### O-v4-4 -- Cap.24.6 non formalizza F effettivo < F dichiarato

**Evidenza**: Cap.24.6 riga 326 formalizza mediana su $k \in \{1, \ldots, F\}$ con $F=8$. Cap.26.2 riga 525 dichiara F effettivo $pprox 6$. Cap.24.6 non modificato.

**Analisi**: interfaccia testuale tra Cap.26.2 e Cap.24.6; mediana di 6 valori ben definita; trade-off accettato e dichiarato; carryover Parte VII Cap.34.

**Impatto GA**: marginale.

**Classificazione**: **NEUTRO**.

---

## Classificazione per il supervisore

| # | Problema | Classificazione | Default | Mandare a Development? |
|---|----------|-----------------|---------|------------------------|
| 1 | **O-v4-1** -- Cap.23.6 vs Cap.26.2/26.5 raccomandano F diverso | NEUTRO | NO | NO (zero impatto GA) |
| 2 | **O-v4-2** -- Cap.26.7 fallback K^strict=4 senza trigger Parte V | NEUTRO | NO | NO (separazione Parte V/Parte VII appropriata) |
| 3 | **O-v4-3** -- Cap.26.2 "margine 66.6h" usa caso ottimo | NEUTRO | NO | NO (ambiguita testuale, no impatto GA) |
| 4 | **O-v4-4** -- Cap.24.6 non formalizza F effettivo < F | NEUTRO | NO | NO (mediana robusta; trade-off dichiarato) |

**Riepilogo classificazione v4**:
- **BUG REALI**: 0.
- **NEUTRO**: 4.
- **MIGLIORA PERFORMANCE**: 0.
- **RISCHIO PEGGIORAMENTO**: 0.

---

## M-promemoria nuovi

**Nessun nuovo M-promemoria** emerge dal rework v3.

Carryover esistente preservato:
- M-2 v2 (production refresh EGARCH Cap.27, carryover Parte VI in corso CAP-06 v2).
- M-16 condizionale (Cox time-varying coefficients).
- Bundle parziale F~6 con varianza inflated cross-fold (carryover operativo dichiarato a Parte VII Cap.34, non M-promemoria formale).

---

## Verdetto finale

**PASS**

I 2 BUG REALI di Review v3 (NB-v3-1 e NB-v3-2) sono **chiusi sostanzialmente**, non solo formalmente:

1. **NB-v3-1 chiuso**: Cap.25.5 e Cap.26.7 allineate sulla definizione di N_eventi come "segnali eseguiti"; aritmetica corretta in Cap.26.7 (rimossa formula errata baseline); divergenza Harrell-strict (K^strict=4) dichiarata esplicitamente in entrambi i capitoli; fallback Harrell-strict ammesso come opzione di Parte VII. K_max=6 ratificato dal supervisore preservato.

2. **NB-v3-2 chiuso**: Cap.26.2 + Cap.26.5 motivazioni riallineate al calcolo POST-fix v2 (107h ottimo F=8). Dichiarazione onesta che 80h NON copre F=8 ottimo. Conseguenza bundle parziale ~6 fold dichiarata. Rinvio Parte VII Cap.34 esplicito. T_budget=80h ratificato dal supervisore preservato.

5 AC riclassificati PARZIALE in Review v3 sono effettivamente promossi nuovamente a OK. 71 AC pregressi preservati senza regressione.

3 NEUTRO confermati come lasciati inalterati.

4 osservazioni minori emerse (O-v4-1, O-v4-2, O-v4-3, O-v4-4) tutte classificate NEUTRO: nessuna altera il comportamento del GA.

**Atteso PASS in 1 iterazione** soddisfatto. CAP-05 v3 chiuso.

**Pipeline successiva**: Orchestratore chiude la sessione CAP-05 (7 condizioni di chiusura sessione) ed eventualmente apre nuova sessione per la ripresa di CAP-06 v2 (sospeso in `tasks/ACTIVE_TASK_CAP06_SUSPENDED.md`).
