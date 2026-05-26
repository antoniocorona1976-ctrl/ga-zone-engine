# TASK ATTIVO: CAP-05 rework v3 -- chiusura sostanziale di NB-2 e RP-1 (Parte V)

**Assegnato da**: Orchestratore (checkpoint supervisore post-Review v3 CONDITIONAL)
**Output atteso**: revisione chirurgica di `docs/methodology_v2/CAP_05_parte_V.md` + sezione Iterazione 3 in `reports/REPORT_CAP_05.md`
**Stato**: NUOVO -- rework v3
**Baseline**: commit `16590ae` (CAP-05 v2)

## Contesto

La Review v2 di CAP-05 (commit `50b6e7e` del 2026-05-26) aveva emesso verdetto PASS e l'Orchestratore aveva chiuso la sessione (commit `fe86d70`). Il supervisore ha riaperto manualmente il ciclo modificando `tasks/DEV_STATUS.md = READY_FOR_REVIEW`. L'audit indipendente Review v3 (`reviews/REVIEW_CAP_05_v3_review.md`, verdetto **CONDITIONAL**) ha rivelato che due dei cinque fix v2 ratificati dal supervisore in v1 sono chiusi **solo testualmente** e non sostanzialmente:

- **NB-2 (K_max=6 per strato)** poggia su aritmetica errata in Cap.26.7 riga 652 + incoerenza di stima censoring fra Cap.25.5 (no censoring) e Cap.26.7 (con 0,7). Sotto la stima corretta con censoring, il caso pessimo strato e' $N_{eventi,strato} \approx 44$ (non 60); con $K_{max}=6$ rapporto $44/6 = 7,3 < 10$ -- viola Harrell. Stima MLE Cox stratificata sovra-parametrizzata; $\hat{p}_{hit}$ biased; filtro $E_{surv}$ Cap.20.1 PIV distorto; ranking Pareto alterato.

- **RP-1 (T_budget=80h)** e' applicato in Cap.26.2 e Cap.26.5 ma motivato citando "72h ottimo F=8" che Cap.23.6 riga 223 dichiara essere il calcolo PRE-fix v2 NB-1 (ormai obsoleto). Il calcolo POST-fix v2 e' 107h caso ottimo / 213h caso pessimo. Cap.26.2/Cap.26.5 motivano $T_{budget}=80$h su un numero che il documento stesso dichiara obsoleto -- contraddizione interna. Conseguenza operativa: run interrotto a ~56% dei fold nel caso ottimo (80h vs 107h) -> bundle parziale -> aggregazione cross-fold con varianza inflated.

Decisione supervisore (2026-05-26): **entrambi i 2 BUG REALI a Developer per rework v3**. Le opzioni concrete di fix (a/b/c) restano nel perimetro del Developer e vanno motivate nel REPORT (come per i BUG REALI di Review v1). I 3 NEUTRO (O-v3-1, O-v3-2, O-v2-1 confermato) **non** vanno a Developer.

## Finding di Review v3 da risolvere (rework v3)

### NB-v3-1 -- NB-2 chiuso solo formalmente: censoring incoerente Cap.25.5/Cap.26.7, Harrell violato sotto K_max=6 (caso pessimo strato 44)

**Cosa va sistemato**:
1. **Allineare la definizione di $N_{eventi}$** fra Cap.25.5 riga 427 e Cap.26.7 riga 651. Le due opzioni (Developer sceglie e motiva nel REPORT):
   - **Opzione (a)**: applicare uniformemente il censoring 0,7 (definizione Harrell standard: $N_{eventi}$ = eventi target_1_hit + stopped osservati, no `expired posttrigger_timeout`). Sotto questa definizione, caso pessimo strato = 44, e per rispettare Harrell ($N/K \geq 10$) deve essere $K_{max} \leq 4$. Aggiornare Cap.26.5 riga 609 e Cap.26.7 riga 649 con $K_{max} = 4$ (anziche' 6).
   - **Opzione (b)**: ridefinire $N_{eventi}$ come "segnali eseguiti" (no censoring nel conteggio Harrell). In quel caso Cap.26.7 va corretto: range fold $[120; 380]$ (allineato a Cap.25.5), strato $[60; 190]$ caso pessimo 60, $K_{max}=6$ resta Harrell-compliant. Aggiungere a Cap.26.7 nota esplicita che la definizione di $N_{eventi}$ in questo documento divergente dalla pratica Harrell standard.

2. **Correggere l'aritmetica errata** di Cap.26.7 riga 652: "$[60/2; 264/2] \cdot 2 = [60; 190]$" e' aritmeticamente sbagliato ($[30; 132] \cdot 2 = [60; 264]$). Il valore corretto del range strato dipende dall'opzione (a/b) scelta sopra. Allineare la formula.

3. **Sanare le ricadute trasversali**: con $K_{max}$ aggiornato (4 in opzione a; 6 in opzione b), verificare che:
   - Cap.22.6 vincolo $\sum_j s_j \leq K_{max}$ riferisca il nuovo valore.
   - Cap.22.7 vincolo 4 sia allineato.
   - Cap.26.5 riga 609 dichiari $K_{max}$ coerente.
   - CARRYOVER.md riga M-11 (CLOSED-CAP-05) sia aggiornata se la chiusura cambia ($K_{max}=4$ in opzione a vs $K_{max}=6$ in opzione b).

**Impatto atteso**: opzione (a) restringe lo spazio di selezione feature del cromosoma ($\binom{37}{4} \approx 66k$ vs $\binom{37}{6} \approx 2,3M$ combinazioni) -- conservativo per stabilita' MLE; opzione (b) mantiene lo spazio ampio ma richiede una motivazione esplicita della divergenza dalla pratica Harrell standard.

### NB-v3-2 -- RP-1 chiuso solo formalmente: T_budget=80h motivato su calcolo Cap.23.6 obsoleto (Cap.26.2 riga 523, Cap.26.5 riga 603)

**Cosa va sistemato**:

Cap.26.2 riga 523 e Cap.26.5 riga 603 motivano $T_{budget}=80$h citando "il caso ottimo del calcolo di Cap.23.6 (72 ore caso ottimo per 8 fold sequenziali)". Cap.23.6 riga 223 (post-fix v2 NB-1) dichiara esplicitamente che 72h e' "la stima Cap.23.6 ORIGINALE, pre-riallineamento M-4"; il calcolo coerente con $t_{eval} \in [0,74; 1,47]$ min/cromosoma e' 107h ottimo / 213h pessimo. La motivazione testuale di Cap.26.2/Cap.26.5 e' contraddittoria con Cap.23.6 nello stesso documento.

Tre opzioni (Developer sceglie e motiva nel REPORT):
- **Opzione (a)**: **riallineare la motivazione testuale** di Cap.26.2 riga 523 e Cap.26.5 riga 603 al calcolo POST-fix v2 (107h ottimo, non 72h). Dichiarare onestamente che $T_{budget}=80$h **NON** copre il caso ottimo $F=8$; copre il run di calibrazione iniziale (singolo fold con margine ~11% sopra 72h del calcolo originale, o equivalente sotto la nuova stima). Per $F=8$ completo serve riduzione di F oppure parallelizzazione > 16 vCPU (rinvio Parte VII Cap.34 esplicitato). Conseguenza: bundle parziale dichiarato a priori, aggregazione cross-fold con varianza inflated documentata in Cap.30 PVI (carryover).
- **Opzione (b)**: **alzare $T_{budget}$** al valore che copre 107h con margine ~10-15% (es. $T_{budget}=120$h). Aggiornare Cap.26.2 e Cap.26.5. Costo: piu' ore AWS spot, ma copre il caso ottimo del WF nested.
- **Opzione (c)**: **ridurre $F$** al numero massimo compatibile con 80h (es. $F=6$ ottimo: $80/107 \cdot 8 \approx 6$). Aggiornare Cap.25.1 ($F=8 \to 6$), Cap.26.5 riga relativa, e ricalcolare le stime di $N_{eventi,strato}$ in Cap.25.5/Cap.26.7 (l'opzione c interagisce con NB-v3-1: con $F=6$ ogni fold ha $W_{in}$ piu' lungo e $N_{eventi}$ atteso piu' alto, potenzialmente rilassando il vincolo Harrell).

Le tre opzioni hanno conseguenze diverse sui parametri di Parte V; il Developer sceglie e motiva nel REPORT.

## Vincoli operativi di rework v3

- **Scope esclusivo**: rework v3 e' chirurgico. Modifiche attese: Cap.25.5 (riga 427), Cap.26.2 (riga 523), Cap.26.5 (riga 603 + 609 se Kmax cambia), Cap.26.7 (righe 651-652-649); eventualmente Cap.22.6 e Cap.22.7 vincolo 4 se Kmax cambia da 6 a 4; eventualmente Cap.25.1 se F cambia da 8. Totale stimato: ~15-25 righe modificate. NON si chiede rework completo di Parte V; NON si chiede rivisitazione di Cap.22 (cromosoma), Cap.23 (operatori), Cap.24 (fitness), Cap.25.1-25.4, Cap.25.6-25.10, Cap.26.1-26.4, Cap.26.6-26.9.

- **REPORT_CAP_05.md** deve avere una nuova sezione "## Iterazione 3 -- risposta ai finding di Review v3 (rework v3)" con:
  - tabella sintesi finding NB-v3-1 + NB-v3-2;
  - opzione scelta (a/b/c per ciascun finding) + motivazione;
  - misura prima/dopo per ogni capitolo modificato;
  - verifica esplicita di assenza di regressioni sugli AC v1 (52 voci), AC v2 (10 voci), AC trasversali (9 voci);
  - dichiarazione che i 3 NEUTRO (O-v3-1, O-v3-2, O-v2-1) sono lasciati inalterati come da decisione supervisore.

- **Indice `00_indice.md`** riga 40 va aggiornata da "PASS Review v2" a "IN REVIEW v3" durante la consegna (il Developer aggiorna l'indice nel commit di v3, come da prassi).

- **CARRYOVER.md** va aggiornata se la chiusura di M-11 cambia (es. $K_{max}=4$ in opzione a richiede aggiornamento riga M-11).

- **Out-of-scope rework v3**: NB-1, NB-3, RP-2, RP-3, 5 NEUTRO v1, 5 NEUTRO v2 -- tutti gia' risolti o esplicitamente non a Developer. CAP-06 v2 rework -- sospeso in `tasks/ACTIVE_TASK_CAP06_SUSPENDED.md`, ripreso dopo PASS CAP-05 v3.

- **Vincoli trasversali invariati**: tick FIB 5pt; causalita' $\mathcal{F}_{t-1}$; determinismo bit-exact (Cap.10 PII); italiano formale; LaTeX inline/display; nessun parametro fissato definitivamente fuori da Cap.26.5; citazioni inline.

## Acceptance criteria del rework v3

- [ ] **AC-v3-1**: NB-v3-1 chiuso. Cap.25.5 riga 427 e Cap.26.7 righe 651-653 allineate sulla stessa definizione di $N_{eventi}$ (opzione a oppure b). Aritmetica Cap.26.7 corretta. $K_{max}$ in Cap.26.5 coerente con opzione scelta ($K_{max}=4$ in opzione a; $K_{max}=6$ in opzione b con motivazione esplicita).
- [ ] **AC-v3-2**: NB-v3-2 chiuso. Cap.26.2 riga 523 e Cap.26.5 riga 603 NON citano piu' "72h caso ottimo" come motivazione di $T_{budget}$; cita il calcolo POST-fix v2 (107h) coerentemente con Cap.23.6 riga 223. La scelta operativa fra (a) riallineare la motivazione / (b) alzare $T_{budget}$ / (c) ridurre F e' dichiarata e motivata nel REPORT.
- [ ] **AC-v3-3**: O-v3-1, O-v3-2, O-v2-1 confermato come NEUTRO non flaggati a Developer. Nessuna modifica al doc su queste 3 voci. Il REPORT lo dichiara esplicitamente.
- [ ] **AC-v3-4**: nessuna regressione sugli AC v1 (52 voci) ne' sugli AC v2 (10 voci) ne' sugli AC trasversali (9 voci). Verifica esplicita in tabella nel REPORT.
- [ ] **AC-v3-5**: nessuna modifica strutturale (no nuovi capitoli, no rimozione capitoli, no rinomina). Modifiche limitate al perimetro Cap.22.6/22.7 (se Kmax cambia), Cap.25.1 (se F cambia), Cap.25.5, Cap.26.2, Cap.26.5, Cap.26.7. Totale stimato <= 25 righe modificate.
- [ ] **AC-v3-6**: REPORT_CAP_05.md include sezione "## Iterazione 3" con tutti gli elementi richiesti.
- [ ] **AC-v3-7**: 00_indice.md riporta Parte V "IN REVIEW v3" durante la consegna.
- [ ] **AC-v3-8**: CARRYOVER.md aggiornata se la chiusura di M-11 cambia (riferimento $K_{max}$).
- [ ] **AC-v3-9**: tutti i file modificati committati e pushati su `origin/main`. Working tree pulito sul task. `DEV_STATUS.md = READY_FOR_REVIEW` come segnale di consegna.
- [ ] **AC-v3-10**: il commit del rework v3 e' `[DEV] CAP-05 v3 rework: NB-v3-1 + NB-v3-2 READY_FOR_REVIEW` o equivalente, pushato su origin/main.

## Pipeline rework v3

Development v3 (rework chirurgico ~15-25 righe + sezione REPORT Iterazione 3) -> Review v4 di CAP-05 -> atteso PASS in 1 iterazione (correzioni puntuali, no decisioni di design pendenti dopo la scelta opzione a/b/c). Se Review v4 emerge nuovi BUG REALI, checkpoint supervisore standard.

## File di riferimento

- Documento da modificare: `docs/methodology_v2/CAP_05_parte_V.md` (commit `16590ae`, 664 righe, 89.5 KB).
- Report da estendere: `reports/REPORT_CAP_05.md` (esistente, aggiungere sezione Iterazione 3).
- Indice: `docs/methodology_v2/00_indice.md` riga 40.
- CARRYOVER: `tasks/CARRYOVER.md` (riga M-11 se necessario).
- Review v3 di riferimento: `reviews/REVIEW_CAP_05_v3_review.md`.
- Review v2 PASS (storico): `reviews/REVIEW_CAP_05_v2_review.md`.
- Review v1 CONDITIONAL (storico): `reviews/REVIEW_CAP_05_review.md`.
- Task CAP-06 sospeso: `tasks/ACTIVE_TASK_CAP06_SUSPENDED.md` (ripresa dopo PASS CAP-05 v3).
