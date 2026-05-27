# REPORT SUPERVISORE — CAP-07

**Task**: CAP-07 — Parte VII del documento metodologico v2 (Validazione OOS, frozen bundle, gate decisionali)
**Stato**: COMPLETATO (Iterazione v2 — rework post-Review v1 CONDITIONAL)
**Iterazione**: v2

## Cosa è stato prodotto

**Iterazione v2 (rework post-Review v1 CONDITIONAL)** — il documento v1 (commit `330359c`) e il REPORT v1 (commit `330359c`) sono entrambi solidi (Review v1: 32/32 eredità OK, 2/2 M-promemoria OK, 5/5 decisioni di scope OK, 63/64 AC OK + 1 PARZIALE AC-33-4). Il rework v2 chiude i 3 finding ratificati dal supervisore al checkpoint Orchestratore del 2026-05-27 (commit `a1e78b5`):

1. **Finding #1 BUG REALE** (contraddizione interna Cap.33.4 vs Cap.34.4 sulla frazione del compute budget assorbita dal PBO) — risolto in `CAP_07_parte_VII.md:320` con opzione (alpha): riformulazione del paragrafo "Frazione del compute budget" di Cap.33.4 con ammissione del range "$\sim 1\%$ per $S = 12$, $\sim 10\%$ per $S = 16$" coerente con la matematica esplicita interna di Cap.33.4 (5,5e7 / 6e9 ≈ 0,009; 7,7e8 / 8e9 ≈ 0,096) e con la dichiarazione di Cap.34.4 (post-processing complessivo ≤ ~15% per S=16). Nessun numero nuovo introdotto. AC-33-4 promosso da PARZIALE a OK.
2. **Finding #2 MIGLIORA PERFORMANCE** (errore unità "15 USD/h spot" c5.4xlarge — 2 occorrenze) — risolto con sostituzione puntuale "15 USD/h spot" → "0,15 USD/h spot" in `CAP_07_parte_VII.md:426` (Cap.34.4 opzione ii) e in `CAP_07_parte_VII.md:441` (Cap.34.4 Cloud). L'aritmetica successiva (0,15 USD/h · 80h = ~12 USD/run; differenziale c5.9xlarge ~24,4 USD < θ_cost=100) ora coerente con l'unità corretta.
3. **Finding #3 MIGLIORA PERFORMANCE** (errore bibliografico Notices AMS 61(5)) — risolto in `CAP_07_parte_VII.md:252` (Cap.33.1) con sostituzione del riferimento "Bailey-Borwein-Lopez de Prado-Zhu 2016 working paper preliminare in Notices of the American Mathematical Society 61(5)" con la citazione corretta: "Bailey, Borwein, Lopez de Prado, Zhu 2014 'Pseudo-Mathematics and Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance', Notices of the American Mathematical Society 61(5), 458-471". L'anno corretto è 2014 (non 2016), il paper è formale (non working paper) e il titolo è esplicitato come da specifica ACTIVE_TASK Finding #3.

**Finding #4 NEUTRO** (esempio Cap.33.5 PBO opaco) e **Finding #5 NEUTRO** (|f_5| ridondante in Cap.31.2 filtro 3 e AC-GO-4): **non modificati** come da decisione del supervisore.

**Bilancio modifiche di rework v2**: 3 Edit puntuali totali (1 in Cap.33.1, 1 in Cap.33.4, 2 in Cap.34.4 — due varianti `15 USD/h` → `0,15 USD/h`). Nessuna riscrittura strutturale, nessun nuovo capitolo, nessuna modifica ai 12 parametri di tuning provvisori, nessuna modifica alle 5 decisioni di scope, nessun nuovo M-promemoria. Replay deterministico bit-exact non impattato (le 3 modifiche sono testuali, non toccano formule o algoritmi). Tick FIB 5 pt preservato. Vincolo "solo emissione" preservato.

**File del rework v2:**

- **`docs/methodology_v2/CAP_07_parte_VII.md`** v2 — Parte VII completa in **6 capitoli** (Cap.31-36) + sotto-sezioni dichiarate, italiano formale, ~8 pagine target invariato vs v1. Conteggio sotto-sezioni effettive invariato: **23 sotto-sezioni** numerate (Cap.31.1-31.5, Cap.32.1-32.5, Cap.33.1-33.5, Cap.34.1-34.5, Cap.35.1-35.4, Cap.36.1-36.5). Conteggio formule LaTeX invariato: **42 formule display** + **17 formule inline**. Conteggio decisioni di scope del Planner chiuse invariato: **5 di 5**. Le 3 modifiche di rework v2 sono tutte chirurgiche, lunghezza target invariata.

- **`reports/REPORT_CAP_07.md`** (questo file) v2 con le 5 sezioni del formato supervisore aggiornate + tabella verifica AC v2 con **AC-33-4 promosso da PARZIALE a OK** + criterio di rollback invariato + sezione "Iterazione 2 — risposta ai finding di Review v1" sotto.

- **`docs/methodology_v2/00_indice.md`** aggiornato — voce Parte VII (riga 55) passa da "🟡 IN REVIEW Review v1 (commit pending)" a "🟡 IN REVIEW Review v2 (documento v2, rework v2 chiude 1 BUG REALE + 2 MIGLIORA PERFORMANCE ratificati dal supervisore via commit `a1e78b5`)". Riferimento alla v1 conservato come descrizione storica.

- **`tasks/DEV_STATUS.md`** scritto come `READY_FOR_REVIEW` (file di una sola riga).

- **`tasks/CARRYOVER.md`** — non modificato in questa iterazione v2. Giustificazione: i 3 finding chiusi dal rework v2 sono testuali (contraddizione interna, unità di misura, citazione bibliografica) e non introducono nuovi M-promemoria. M-2 OPEN e M-16 OPEN-CONDIZIONALE restano invariati come da decisione di scope (a) e (b).

## Ipotesi di partenza

L'ipotesi metodologica di partenza è che il fronte di Pareto $\mathcal{F}_1$ prodotto dal NSGA-II di Parte V è **necessario ma non sufficiente** per il go-live: il fronte contiene cromosomi non dominati sui 5 obiettivi della fitness di Parte V, ma non garantisce nessuna delle proprietà che il go-live richiede — significatività statistica al netto del bias di selezione (DSR), robustezza alla partizione del dato OOS (PBO), intervalli di confidenza sulle metriche di lifecycle (bootstrap), identità immutabile riproducibile (hash SHA-256), checklist deterministica di gate (12 AC binari). La Parte VII è il **layer di decisione finale** che converte $\mathcal{F}_1$ in **uno specifico bundle frozen** promosso a produzione.

L'**impatto sul GA** della Parte VII è di **filtraggio post-selezione**: il GA produce il fronte $\mathcal{F}_1$ in Parte V, la Parte VII applica gate che eliminano cromosomi non significativi (filtro 1 DSR), fragili (filtro 2 PBO), instabili cross-regime (filtro 3 $f_5$), instabili cross-fold (filtro 4 IQR), di scarsa qualità informativa per la submachine (filtro 5 $\pi_{t_2|t_1}$); il cromosoma sopravvissuto è scelto per massimizzazione di $f_1^{global}$ con tie-break esplicito. Il GA **non vede** i gate di Parte VII durante l'ottimizzazione (Cap.24.7 di Parte V: DSR/PBO non sono obiettivi diretti del NSGA-II, sono gate post-selezione), in coerenza con López de Prado 2018 cap. 12.

### Trentadue eredità citate (con destinazione effettiva nel documento)

**Da CAP-01 (Parte I):**

1. **Vincolo "solo emissione"** — Cap.31.1 (fonte canonica metriche = log replay, non fill broker) + preambolo Parte VII.
2. **Profilo operatore retail mobile** — Cap.36.1 AC-GO-7 ($\theta_{MDD} = 200$ pt FIB = 1.000 EUR/contratto compatibile con 1 contratto/volta) + Cap.36.5.
3. **Sessione operativa 8:00-22:00 CET** — Cap.31.1 (840 barre/sessione) + Cap.34.1 (coerenza finestra operativa con bootstrap senza overnight) + Cap.36.2 (verifica aggregata di sessione).
4. **Infrastruttura locale + cloud AWS c5.4xlarge per training** — Cap.34.4 (compute stress test, opzione (ii) migrazione c5.9xlarge/c5.18xlarge).
5. **Storico Portara/CQG FIB 1-min 5 anni** — Cap.31.1 (finestra OOS aggregata $W_{oos} \cdot F$ con conversione mesi calendario).
6. **Tick FIB = 5 punti** — Cap.36.5 (esempi numerici rispettano tick FIB 5 pt) + AC-T-5.
7. **Filtro emissione ≥80 pt** — Cap.35.1 elemento 1 ($A_{range,min} = 80$ pt) + Cap.31 vincolo per costruzione (Cap.22.7 PV vincolo 2).
8. **Commissioni 5 EUR/op** — Cap.32.2 (rendimenti $R_{net}$ al netto di $2 \cdot c = 2$ pt FIB round-trip).
9. **Definizione operativa del successo** — Cap.36.1 (checklist 12 AC come sintesi operativa della definizione di Cap.5 PI).
10. **Target operativo asimmetrico 500 pt/giorno OR 70% movimento strutturale** — Cap.36.2 (verifica aggregata con $T_{abs} \lor T_{rel}$, $\theta_{sessions} = 0{,}60$).
11. **Compute budget $T_{budget} = 80$h wall-clock** — Cap.34.4 (regola decisione fra opzioni (i)/(ii)/(iii) con aritmetica esplicita: $t_{eval, target}^{eff} \leq 0{,}496$ min/cromosoma).

**Da CAP-02 (Parte II):**

12. **Payload immutabile 12 campi** — Cap.35.1 elemento 4 (tupla $\mathcal{S}$ di Cap.6.1 PII come definizione strutturale invariante del bundle frozen).
13. **State machine 1 non-terminale + 6 terminali** — Cap.31.1 (transizioni stato nel log replay) + Cap.32.2 (segnali eseguiti = `target_1_hit`, `stopped`, `expired posttrigger_timeout`) + Cap.35.3 Regola 1 (gestione segnali `active`).
14. **Vincolo segnale unico attivo $|\mathcal{A}(t)| \leq 1$** — Cap.34.1 (bootstrap non genera segnali simultanei artificiali).
15. **Replay deterministico bit-exact** — Cap.31.1 (fonte canonica metriche) + Cap.31.2 (selezione lessicografica deterministica) + Cap.34.5 (seed bootstrap nel bundle) + Cap.35.1 elemento 5 (tutti i seed) + Cap.35.2 (hash SHA-256 per integrità).
16. **Submacchina position lifecycle post-target_1** — Cap.31.2 filtro 5 ($\pi_{t_2|t_1}$) + Cap.34.3 metriche 8-11.

**Da CAP-03 (Parte III):**

17. **EGARCH(1,1) con $D$ AIC/BIC e finestra rolling $W = 210.000$** — Cap.31.4 (chiusura M-5 window + $D$ + init) + Cap.35.1 elementi 1 e 3 (parametri EGARCH + coefficienti $(\mu, \omega, \alpha, \gamma, \beta, \nu)$).
18. **Classificazione regime calmo/turbolento** — Cap.31.2 filtro 3 ($f_5^{global}$ con separazione regime) + Cap.36.2 (reporting separato per regime) + Cap.35.1 elemento 3 (quantili $\bar{\sigma}_s$).
19. **Catalogo 37 feature + selezione $\mathbf{s} \in \{0,1\}^{37}$ con $K_{max} = 6$** — Cap.31.5 (riconsiderazione $K_{max}^{strict} = 4$ come carryover) + Cap.35.1 elementi 2 e 6.

**Da CAP-04 (Parte IV):**

20. **Geometria zone, target, stop strutturali/sintetici, Cox cause-specific, filtri Cap.20** — Cap.35.1 elementi 1 e 2 (tabella Cap.26.5 PV + geni geometrici).
21. **Modello Cox cause-specific stratificazione regime** — Cap.31.3 (chiusura tre decisioni $r_{FG}, r_{CV}, r_{Schoenfeld}$) + Cap.35.1 elemento 3 (coefficienti Cox $\boldsymbol{\beta}_{j,R}$ + baseline hazard) + Cap.35.1 elemento 6 (metadati).

**Da CAP-05 (Parte V):**

22. **Output NSGA-II = fronte di Pareto $\mathcal{F}_1$** — Cap.31.2 (input selezione bundle) + Cap.32.3 ($N_{trials} = |\mathcal{F}_1|$) + Cap.33.1-33.5 (CSCV opera su $\mathcal{F}_1$) + Cap.35.1 elemento 6.
23. **Aggregazione mediana cross-fold di Cap.24.6 PV** — Cap.31.2 (selezione finale $f_1^{global} = \text{median}_k f_1$) + Cap.34.4 opzione (iii) (robustezza al variare di $F$).
24. **Walk-forward nested $F = 8$ fold provvisori** — Cap.31.1 ($W_{oos} = 52.920$, $P_{purge} = 4.200$, $P_{emb} = 4.200$) + Cap.33.2 (blocchi CSCV con $S = 2F$).
25. **Tabella congelati Cap.26.5 PV** — Cap.35.1 elemento 1.
26. **No incorporazione DSR/PBO come obiettivi diretti** — Cap.32.1 + Cap.33.1 (gate post-selezione) + Cap.24.7 PV citato.
27. **Seed bundle frozen** — Cap.34.5 (seed bootstrap separato e indipendente) + Cap.35.1 elemento 5.
28. **Compute budget $T_{budget} = 80$h Cap.26.2 PV + bundle parziale F~6 atteso** — Cap.34.4 (compute stress test + aritmetica $t_{eval, target}^{eff} = 0{,}496$ + stima costi c5.9xlarge $\approx 36{,}4$ USD vs c5.4xlarge $\approx 12$ USD + differenziale $\approx 24{,}4$ USD < $\theta_{cost} = 100$ USD/run).
29. **Diagnostica survival fold-per-fold** — Cap.31.3 (flag fold-per-fold come input deterministico per rapporti).

**Da CAP-06 (Parte VI):**

30. **Pipeline di inference real-time + Cap.27.5 cadenza EGARCH + Cap.30 monitoraggio live** — Cap.36.1 AC-GO-10 (pipeline operativa) + Cap.36.1 AC-GO-11 (dashboard operativa).
31. **10 parametri di tuning operativo non congelati in Parte VI** — Cap.36.3 (decisione scope (c): rimangono starting point, carryover monitoring post-go-live).
32. **Bundle frozen come input invariante pipeline live** — Cap.35.1 (specifica formale prodotta da Parte VII) + Cap.35.3 (regola sostituzione senza interruzione).

### M-promemoria gestiti

- **M-2 OPEN** (verifica empirica latenza Telegram $L_{max} = 30$ s): trattato come da decisione di scope (a). Cap.31.1 cita qualitativamente l'obiettivo di latenza end-to-end. Cap.36.1 AC-GO-10 lo include come componente del gate go-live (verifica funzionale pipeline con vincolo qualitativo $L_{max}$). **Verifica numerica empirica** resta **carryover Appendice E** (M-2 OPEN invariato).

- **M-16 OPEN-CONDIZIONALE** (Cox time-varying coefficients): trattato come da decisione di scope (b). Cap.31.3 dichiara regola di chiusura condizionale:
  - (i) calcolo del rapporto $r_{Schoenfeld} = |\{k : p_{Schoenfeld, k} < 0{,}05\}| / F$;
  - (ii) se $r_{Schoenfeld} > 0{,}50$, **M-16 attivato**: estensione a Cox time-varying coefficients $\boldsymbol{\beta}_j(\tau)$ nel ciclo successivo (citazione Therneau-Grambsch 2000 cap. 6); bundle frozen registra `cox_time_varying_active = True`;
  - (iii) se $r_{Schoenfeld} \leq 0{,}50$, **M-16 CLOSED-CAP-07 senza attivazione**: bundle registra `cox_time_varying_active = False`;
  - (iv) decisione registrata nel bundle come metadato (Cap.35.1 elemento 6).

  M-16 è **chiuso in Cap.31.3 con regola condizionale + metadato bundle**.

### Cinque decisioni di scope del Planner riportate e applicate

**(a) M-2 OPEN.** Riportata verbatim: "Cap.31.1 cita qualitativamente l'obiettivo di latenza end-to-end nella procedura di validazione OOS. La verifica numerica empirica $L_{max}$ effettivo resta carryover Appendice E (M-2 OPEN invariato): Cap.31 non risolve numericamente $L_{max}$, ma dichiara che la sua verifica empirica è componente del gate di go-live (Cap.36 AC-GO-10)." **Applicata**: Cap.31.1 §3 cita $L_{max}$ qualitativamente con rinvio Appendice E; Cap.36.1 AC-GO-10 include la verifica funzionale pipeline con vincolo qualitativo $L_{max}$.

**(b) M-16 OPEN-CONDIZIONALE.** Riportata verbatim: "Cap.31.3 dichiara la regola di decisione (i) conta del rapporto $r_{Schoenfeld}$ di fold; (ii) se $r_{Schoenfeld} > 0{,}5$, dichiara l'estensione a Cox time-varying coefficients (Therneau-Grambsch 2000 cap. 6) nel ciclo successivo; (iii) se $r_{Schoenfeld} \leq 0{,}5$, M-16 CLOSED-CAP-07; (iv) la decisione è registrata nel bundle frozen come metadato: `cox_time_varying_active = True/False`." **Applicata**: Cap.31.3 (iii) con i 4 passi + Cap.35.1 elemento 6 con campo `cox_time_varying_active`.

**(c) Congelamento 10 parametri Parte VI.** Riportata verbatim: "Cap.36.3 NON congela i 10 parametri di tuning operativo di Cap.27-30 PVI. Motivazione esplicita: i 10 parametri sono dichiarati in Parte VI come 'non congelati in Parte VI, riconsiderati post-go-live'; il loro congelamento empirico richiede dati di produzione live che il backtest OOS Parte VII non possiede. Cap.36.3 dichiara che i default proposti rimangono starting point per il primo run di produzione, riconsiderati a 3-6 mesi di produzione live. Carryover esplicito al ciclo post-go-live: la riconsiderazione è attività di monitoring post-go-live, non di validazione OOS pre-go-live." **Applicata**: Cap.36.3 con motivazione esplicita + dichiarazione del carryover.

**(d) Robustezza al variare di F nel compute stress test.** Riportata verbatim: "Cap.34.4 conduce empiricamente il compute stress test e dichiara la regola di decisione deterministica fra: opzione (i) F=8 con riduzione $t_{eval}$ (aritmetica $t_{eval} < (80 \cdot 16) / (17.408 \cdot 8) \approx 0{,}919$ min/cromosoma); opzione (ii) F=8 con parallelizzazione >16 vCPU; opzione (iii) F~6 con varianza inflated. Regola di selezione: se (i) fattibile, scegliere (i); altrimenti se differenziale (ii) $\leq \theta_{cost} = 100$ USD/run, scegliere (ii); altrimenti (iii). Il Developer dichiara la regola, non simula l'esito." **Applicata**: Cap.34.4 con aritmetica esplicita $t_{eval, target}^{single} = 0{,}551$ → $t_{eval, target}^{eff} = 0{,}496$ con $\eta_{par} = 0{,}90$; confronto con range Cap.23.6 PV $[0{,}74; 1{,}47]$; aritmetica costi c5.9xlarge/c5.18xlarge. Nota: i numeri specifici della decisione di scope (es. $0{,}919$ min/cromosoma) sono stati ricalcolati con maggiore precisione nel documento finale per consistenza dimensionale (vincolo nominale + efficienza parallela); la regola di decisione rimane invariata.

**(e) Cloud per bootstrap stazionario.** Riportata verbatim: "Bootstrap stazionario $B = 2000$ NON è eseguibile in locale entro tempi ragionevoli. Cap.34.4 dichiara esplicitamente che il calcolo gira su c5.4xlarge come post-processing aggiuntivo del walk-forward, all'interno del compute budget $T_{budget} = 80$h. Il costo computazionale stimato del bootstrap su finestra OOS aggregata deve essere dichiarato come frazione del compute budget totale: $O(B \cdot n_{segnali})$ con $n_{segnali} \sim 1.500$-$3.000$. Per 13 metriche bootstrappate, $\sim 26.000 \cdot n_{segnali}$ operazioni totali $\sim 5 \cdot 10^7$-$10^8$ — trascurabile rispetto al training NSGA-II ($\sim 10^9$ per fold). La frazione di compute budget è dichiarata $< 5\%$." **Applicata**: Cap.34.4 con aritmetica esplicita $N_{bootstrap}^{ops} = 13 \cdot 2.000 \cdot n_{segnali} \in [3{,}9 \cdot 10^7; 7{,}8 \cdot 10^7]$ operazioni; frazione $\in [0{,}5\%; 1{,}3\%]$, ben sotto 5%.

## Decisioni rilevanti prese durante lo sviluppo

### Citazioni bibliografiche esplicite per i metodi statistici nuovi

- **DSR** — Bailey, D. H. e López de Prado, M. (2014) "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality", *Journal of Portfolio Management* 40(5), 94-107. Citato in Cap.32.1 + Cap.32.4.
- **PBO via CSCV** — Bailey, D. H., Borwein, J. M., López de Prado, M. e Zhu, Q. J. (2017) "The Probability of Backtest Overfitting", *Journal of Computational Finance* 20(4), 39-70. Citato in Cap.33.1 + Cap.33.2 (sez. 3) + Cap.33.3 (sez. 5).
- **Bootstrap stazionario** — Politis, D. N. e Romano, J. P. (1994) "The stationary bootstrap", *Journal of the American Statistical Association* 89(428), 1303-1313. Citato in Cap.34.1.
- **Block length adattiva** — Politis, D. N. e White, H. (2004) "Automatic block-length selection for the dependent bootstrap", *Econometric Reviews* 23(1), 53-70. Citato in Cap.34.2.
- **BCa bootstrap (alternativo)** — Efron, B. (1987) "Better bootstrap confidence intervals", *Journal of the American Statistical Association* 82(397), 171-185. Citato in Cap.34.3.
- **Cox time-varying coefficients** — Therneau, T. M. e Grambsch, P. M. (2000) "Modeling Survival Data: Extending the Cox Model", Springer, cap. 6. Citato in Cap.31.3 + Cap.35.3 Regola 3.
- **Test Schoenfeld** — Grambsch, P. M. e Therneau, T. M. (1994) "Proportional hazards tests and diagnostics based on weighted residuals", *Biometrika* 81(3), 515-526. Citato in Cap.31.3.
- **Quadro teorico generale gate post-selezione** — López de Prado, M. (2018) "Advances in Financial Machine Learning", Wiley, cap. 11-12. Citato in Cap.31.2, Cap.32.1, Cap.33.1, Cap.34.1.
- **JSON canonical form** — RFC 8785 (2020) "JSON Canonicalization Scheme (JCS)". Citato in Cap.35.2.
- **SHA-256** — FIPS PUB 180-4 (NIST 2015) "Secure Hash Standard (SHS)". Citato in Cap.35.2.

### Aritmetica del compute stress test di Cap.34.4

- **Vincolo $t_{eval}$ single-thread.** $T_{budget} = 80$ h = $4.800$ min wall-clock su 16 vCPU $\Rightarrow$ tempo single-thread disponibile = $76.800$ min. Numero valutazioni totali $F = 8$ fold = $17.408 \cdot 8 = 139.264$. Tempo medio = $76.800 / 139.264 \approx 0{,}551$ min/cromosoma single-thread.
- **Vincolo con efficienza parallela $\eta_{par} = 0{,}90$.** Vincolo reale = $0{,}551 \cdot 0{,}90 \approx 0{,}496$ min/cromosoma.
- **Confronto Cap.23.6 PV.** Range $[0{,}74; 1{,}47]$ min/cromosoma. Bound inferiore $0{,}74 > 0{,}496$: opzione (i) **non fattibile senza ottimizzazione**.
- **c5.9xlarge.** Tempo $= 107 \cdot 16/36 \approx 47{,}6$ h. Costo $= 47{,}6 \cdot 0{,}765 \approx 36{,}4$ USD/run. Differenziale vs c5.4xlarge $\approx 24{,}4$ USD $\ll \theta_{cost} = 100$ USD.
- **c5.18xlarge.** Tempo $\approx 23{,}8$ h. Costo $\approx 36{,}4$ USD. Differenziale $\approx 24{,}4$ USD.

L'aritmetica è regola di calcolo del vincolo, non esito empirico.

### Dettagli su block length adattiva (Politis-White 2004)

Calibrazione automatica obbligatoria; valore di lavoro $L_{avg} = 10$ è starting point. Bounds: tronca a $n/5$ se Politis-White stima troppo lungo; tronca a 1 se segnali pseudo-iid. Valore effettivo registrato come metadato `L_avg_bootstrap` nel bundle frozen.

### Scelta opzione (i)/(ii)/(iii) come regola deterministica, non scelta empirica

Il compute stress test di Cap.34.4 è una **procedura da seguire**, non un esito. Il Developer dichiara la regola + aritmetica + default. L'esito sarà disponibile in produzione/ciclo successivo. Il bundle frozen del run effettivo registrerà `F_effective` e `compute_instance`.

### Convenzione hash SHA-256

Cap.35.2 specifica due convenzioni: RFC 8785 JSON canonical form (default raccomandato) e tupla lessicograficamente ordinata con encoding binario IEEE 754 (alternativa). Scelta esatta demandata all'implementazione.

## Misura prima/dopo

Valore aggiunto della Parte VII rispetto alla situazione pre-Parte VII (output di Parte V = fronte $\mathcal{F}_1$).

| Metrica | Prima (senza Parte VII) | Dopo (con Parte VII v1) | Delta |
|---------|--------------------------|---------------------------|-------|
| Selezione cromosoma dal fronte | Ambigua ($|\mathcal{F}_1| \in [20, 60]$, nessuna regola) | Deterministica via 6 filtri lessicografici + tie-break (Cap.31.2) | +1 (decisione binaria GO/NO-GO possibile) |
| Prova statistica anti-overfitting | Assente | DSR (Cap.32) + PBO via CSCV (Cap.33) | +2 metodi statistici |
| Intervalli di confidenza | Solo $\text{IQR}_{norm}$ cross-fold | Bootstrap stazionario $B = 2.000$ + Politis-White + percentile/BCa | +13 metriche con IC 95% |
| Identità immutabile del bundle | Assente | Hash SHA-256 (Cap.35.2) + validazione integrità + 6 elementi (Cap.35.1) | +1 artefatto digitale immutabile |
| Regola di sostituzione del bundle | Assente | 4 regole esplicite (Cap.35.3) + gestione segnali `active` | +4 regole operative |
| Decisione binaria GO/NO-GO | Assente | Checklist 12 AC binari (Cap.36.1) + raccomandazione operativa | +1 checklist verificabile |
| Chiusura M-16 OPEN-CONDIZIONALE | OPEN-CONDIZIONALE | Chiusura condizionale Cap.31.3 con regola + metadato bundle | +1 M-promemoria chiuso |
| Chiusura 3 decisioni condizionali Parte V | Aperte | Chiusura in Cap.31.3 con regole di conteggio fold | +3 decisioni chiuse |
| Chiusura M-5 + $D$ + init EGARCH | Aperte | Chiusura in Cap.31.4 con regole di conteggio fold | +3 decisioni chiuse |
| Compute stress test (F=8 vs F~6) | Aperta | Regola deterministica fra opzioni (i)/(ii)/(iii) in Cap.34.4 | +1 regola operativa |
| Tracciabilità cross-bundle | Assente | `bundle_id` + `bundle_hash` + tabella `bundle_history` (Cap.35.4) | +1 tabella storica |
| Numero AC dichiarati | 0 | 41 sui sotto-capitoli + 11 AC-T + 12 AC-GO = **64 AC** | +64 AC verificabili |

**Sintesi:** senza Parte VII il fronte di Pareto $\mathcal{F}_1$ resterebbe ambiguo, mancherebbe la prova anti-overfitting (DSR/PBO), mancherebbero IC bootstrap, mancherebbe l'identità immutabile del bundle, mancherebbe la regola binaria di go-live. Con Parte VII il fronte si traduce in **uno specifico bundle frozen con hash SHA-256 + checklist binaria GO/NO-GO + 64 AC verificabili**.

## Verifica esplicita degli Acceptance Criteria

### AC Cap.31 (8 AC)

| AC-ID | Criterio | Esito | Evidenza |
|-------|----------|-------|----------|
| AC-31-1 | Cap.31.1 dichiara finestra OOS aggregata come $W_{oos} \cdot F$ con $W_{oos} = 52.920$ e $F \in \{6, 7, 8\}$ | OK | CAP_07_parte_VII.md Cap.31.1 §1 con formula $W_{oos,agg} = 52.920 \cdot F$ + valori 317.520/370.440/423.360 barre |
| AC-31-2 | Cap.31.1 dichiara log replay bit-exact come fonte canonica; nessuna metrica su fill broker; $L_{max}$ qualitativo con rinvio Appendice E | OK | CAP_07_parte_VII.md Cap.31.1 §3-4 |
| AC-31-3 | Cap.31.2 elenca 6 filtri lessicografici + criterio finale + tie-break 3 livelli; soglie provvisorie | OK | CAP_07_parte_VII.md Cap.31.2 |
| AC-31-4 | Cap.31.2 dichiara caso fallimento go-live + raccomandazioni | OK | CAP_07_parte_VII.md Cap.31.2 §finale "Caso di fallimento di go-live" |
| AC-31-5 | Cap.31.3 chiude 3 decisioni condizionali con $r_{FG}, r_{CV}, r_{Schoenfeld}$ e soglia 0,5; M-16 con regola + metadato `cox_time_varying_active` | OK | CAP_07_parte_VII.md Cap.31.3 (i)/(ii)/(iii) con i 4 sotto-passi M-16 |
| AC-31-6 | Cap.31.4 chiude M-5 + $D$ + init EGARCH con rapporti fold + soglia 0,5 | OK | CAP_07_parte_VII.md Cap.31.4 sezioni Window/Distribuzione/Inizializzazione |
| AC-31-7 | Cap.31.5 dichiara riconsiderazione $\theta_{CV} = 0{,}5$ + $K_{max}^{strict} = 4$ come carryover | OK | CAP_07_parte_VII.md Cap.31.5 |
| AC-31-8 | Nessun valore numerico congelato di Parte VII in Cap.31 | OK | CAP_07_parte_VII.md preambolo + Cap.31 (solo parametri di tuning provvisori) |

### AC Cap.32 (6 AC)

| AC-ID | Criterio | Esito | Evidenza |
|-------|----------|-------|----------|
| AC-32-1 | Cap.32.1 fornisce definizione formale DSR di Bailey-López de Prado 2014 con 5 componenti + citazione bibliografica | OK | CAP_07_parte_VII.md Cap.32.1 con formula DSR + $SR^*$ + citazione *Journal of Portfolio Management* 40(5), 94-107 |
| AC-32-2 | Cap.32.2 dichiara $\widehat{SR}$ per-segnale (no annualizzazione); conversione annualizzata reporting opzionale | OK | CAP_07_parte_VII.md Cap.32.2 |
| AC-32-3 | Cap.32.3 dichiara stima $\hat{\gamma}_3, \hat{\gamma}_4, N_{trials}, \text{Var}(\widehat{SR}_k)$ | OK | CAP_07_parte_VII.md Cap.32.3 con formule momenti centrali ordine 3 e 4 |
| AC-32-4 | Cap.32.4 dichiara soglia $\theta_{DSR} = 0{,}95$ provvisoria + comportamento ai bordi | OK | CAP_07_parte_VII.md Cap.32.4 |
| AC-32-5 | Cap.32.5 fornisce esempio numerico illustrativo con calcolo $SR^*$ e $DSR$ | OK | CAP_07_parte_VII.md Cap.32.5 con $SR^* = 0{,}1899$, $DSR \approx 0{,}042$ |
| AC-32-6 | Cap.32 cita esplicitamente Bailey-López de Prado 2014, López de Prado 2018 cap. 12, Cap.24.1/24.7 PV, Cap.31.1, Cap.5 PI | OK | CAP_07_parte_VII.md Cap.32.1 + Cap.32.5 §finale |

### AC Cap.33 (6 AC)

| AC-ID | Criterio | Esito | Evidenza |
|-------|----------|-------|----------|
| AC-33-1 | Cap.33.1 fornisce definizione formale CSCV di Bailey-Borwein-López de Prado-Zhu 2017 con 6 passi | OK | CAP_07_parte_VII.md Cap.33.1 con 6 passi + citazione *Journal of Computational Finance* 20(4), 39-70 |
| AC-33-2 | Cap.33.2 dichiara $S = 16$ (F=8) o $S = 12$ (F=6); allineamento ai fold; vincolo $S$ pari motivato | OK | CAP_07_parte_VII.md Cap.33.2 con regola $S = 2F$ |
| AC-33-3 | Cap.33.3 dichiara $\theta_{PBO} = 0{,}5$ gate minimo + citazione Bailey-Borwein-López de Prado-Zhu 2017 | OK | CAP_07_parte_VII.md Cap.33.3 |
| AC-33-4 | Cap.33.4 fornisce stima costo computazionale + frazione compute budget (riformulata in v2 come range "$\sim 1\%$ per $S = 12$, $\sim 10\%$ per $S = 16$", coerente con Cap.34.4 post-processing complessivo ≤ ~15%) | OK (era PARZIALE in v1, promosso a OK in v2 con rework Finding #1) | CAP_07_parte_VII.md:320 (paragrafo "Frazione del compute budget" Cap.33.4 riformulato) |
| AC-33-5 | Cap.33.5 fornisce esempio numerico illustrativo con calcolo $PBO$ | OK | CAP_07_parte_VII.md Cap.33.5 con $PBO \approx 0{,}3497$ |
| AC-33-6 | Cap.33 cita Bailey-Borwein-López de Prado-Zhu 2017, López de Prado 2018 cap. 11-12, Cap.23.1 PV, Cap.24.7 PV, Cap.31.1, Cap.5 PI | OK | CAP_07_parte_VII.md Cap.33.1 + Cap.33.5 §finale |

### AC Cap.34 (8 AC)

| AC-ID | Criterio | Esito | Evidenza |
|-------|----------|-------|----------|
| AC-34-1 | Cap.34.1 fornisce definizione formale bootstrap stazionario di Politis-Romano 1994 con block geometric + wrap modulo $n$ + $B = 2.000$ | OK | CAP_07_parte_VII.md Cap.34.1 con citazione *JASA* 89(428), 1303-1313 |
| AC-34-2 | Cap.34.2 dichiara $L_{avg}$ calibrata via Politis-White 2004; default $L_{avg} = 10$; range $[5, 20]$ | OK | CAP_07_parte_VII.md Cap.34.2 con citazione *Econometric Reviews* 23(1), 53-70 |
| AC-34-3 | Cap.34.3 elenca 13 metriche bootstrappate + percentile method default + BCa Efron 1987 alternativo | OK | CAP_07_parte_VII.md Cap.34.3 + citazione Efron 1987 *JASA* 82(397), 171-185 |
| AC-34-4 | Cap.34.4 compute stress test con regola decisione (i)/(ii)/(iii); aritmetica esplicita + $\theta_{cost} = 100$ USD/run | OK | CAP_07_parte_VII.md Cap.34.4 con $t_{eval, target}^{eff} = 0{,}496$ + differenziale c5.9xlarge $\approx 24{,}4$ USD |
| AC-34-5 | Cap.34.4 dichiara frazione compute budget bootstrap < 5% | OK | CAP_07_parte_VII.md Cap.34.4: $N_{bootstrap}^{ops} = 26.000 \cdot n_{segnali} \in [3{,}9 \cdot 10^7; 7{,}8 \cdot 10^7]$; frazione $\in [0{,}005; 0{,}013]$ |
| AC-34-6 | Cap.34.5 dichiara seed PRNG bootstrap come parte identità bundle | OK | CAP_07_parte_VII.md Cap.34.5 con `seed_bootstrap` nel bundle |
| AC-34-7 | Cap.34 cita Politis-Romano 1994, Politis-White 2004, Efron 1987, López de Prado 2018 cap. 12, Cap.4 PI, Cap.23.6 PV, Cap.24-26 PV | OK | CAP_07_parte_VII.md Cap.34 §finale |
| AC-34-8 | $B = 2.000$ ricampionamenti dichiarato esplicitamente | OK | CAP_07_parte_VII.md Cap.34.1 passo 4 + Cap.34.4 + Cap.34.5 §finale |

### AC Cap.35 (5 AC)

| AC-ID | Criterio | Esito | Evidenza |
|-------|----------|-------|----------|
| AC-35-1 | Cap.35.1 elenca 6 elementi bundle frozen; metadati `F_effective, r_FG, r_CV, r_Schoenfeld, cox_time_varying_active, egarch_window, egarch_distribution, egarch_init_option, N_trials, timestamp, code_version` | OK | CAP_07_parte_VII.md Cap.35.1 con elenco completo |
| AC-35-2 | Cap.35.2 dichiara hash SHA-256 in ordine canonico + `bundle_hash` + verifica integrità all'avvio con fallimento in caso di mismatch | OK | CAP_07_parte_VII.md Cap.35.2 con procedura 3 passi + validazione 5 passi + RFC 8785 + FIPS PUB 180-4 |
| AC-35-3 | Cap.35.3 elenca 4 regole sostituzione + gestione segnali `active` | OK | CAP_07_parte_VII.md Cap.35.3 Regole 1-4 |
| AC-35-4 | Cap.35.4 dichiara `bundle_id` progressivo + tabella `bundle_history` con metriche e motivazione | OK | CAP_07_parte_VII.md Cap.35.4 con tabella `bundle_history` |
| AC-35-5 | Cap.35 cita Cap.6.1 PII, Cap.10 PII, Cap.26.5 PV, Cap.26.8 PV, Cap.27.3 PVI, Cap.7 PII | OK | CAP_07_parte_VII.md Cap.35 §finale |

### AC Cap.36 (7 AC)

| AC-ID | Criterio | Esito | Evidenza |
|-------|----------|-------|----------|
| AC-36-1 | Cap.36.1 elenca checklist go-live in 12 AC binari (AC-GO-1..AC-GO-12) | OK | CAP_07_parte_VII.md Cap.36.1 con 12 AC numerati |
| AC-36-2 | Cap.36.1 dichiara decisione binaria GO/NO-GO + raccomandazione | OK | CAP_07_parte_VII.md Cap.36.1 §finale con 4 raccomandazioni operative |
| AC-36-3 | Cap.36.2 verifica aggregata sessione (500 pt OR 70% movimento) con $\theta_{sessions} = 0{,}60$ + reporting separato regime | OK | CAP_07_parte_VII.md Cap.36.2 con $T_{abs} \lor T_{rel}$, $\rho_{sessions}$ |
| AC-36-4 | Cap.36.3 decisione scope (c): 10 parametri rimangono starting point; carryover monitoring post-go-live | OK | CAP_07_parte_VII.md Cap.36.3 |
| AC-36-5 | Cap.36.4 regola anticipo ritraining su alert persistenti + citazione Cap.35.3.2 | OK | CAP_07_parte_VII.md Cap.36.4 con 4 trigger paralleli |
| AC-36-6 | Cap.36.5 report finale con tabelle checklist + metriche IC bootstrap + 3 decisioni condizionali + M-5+Cap.26.3-26.4 + bundle artifact + decisione GO/NO-GO | OK | CAP_07_parte_VII.md Cap.36.5 con i 6 punti (a)-(f) |
| AC-36-7 | Cap.36 cita Cap.5 PI, Cap.1 PI, Cap.24.1-24.2 PV, Cap.27 PVI, Cap.30 PVI, Cap.31-35 PVII | OK | CAP_07_parte_VII.md Cap.36 §finale |

### AC trasversali (AC-T, 11 AC)

| AC-ID | Criterio | Esito | Evidenza |
|-------|----------|-------|----------|
| AC-T-1 | Tutte le 32 eredità citate esplicitamente | OK | Vedi sezione "Trentadue eredità citate" sopra |
| AC-T-2 | I 2 M-promemoria trattati come da decisioni di scope | OK | Vedi sezione "M-promemoria gestiti" |
| AC-T-3 | Nessuna logica execution; verifica negativa lessicale | OK | CAP_07_parte_VII.md: "fill" solo in "fill virtuale" (Cap.32.2) o negativo "fill effettivi del broker" (Cap.31.1 §3) |
| AC-T-4 | Nessun re-training del GA in produzione attivato in Parte VII | OK | CAP_07_parte_VII.md preambolo + Cap.35.3 Regola 2 + Cap.36.4 |
| AC-T-5 | Esempi numerici rispettano tick FIB 5 pt; Cap.32.5 e Cap.33.5 dichiarati illustrativi | OK | CAP_07_parte_VII.md Cap.32.5 + Cap.33.5 (dichiarati illustrativi) + Cap.36.5 §finale ($-100, 200$ multipli di 5) |
| AC-T-6 | Parametri tuning provvisori con dominio + default + marcatura "non congelato in Parte VII" | OK | CAP_07_parte_VII.md preambolo (12 parametri) + Cap.31.2 + Cap.32.4 + Cap.33.3 + Cap.33.4 + Cap.34.2 + Cap.34.4 + Cap.36.1 |
| AC-T-7 | Lunghezza target ~8 pp totali | OK | CAP_07_parte_VII.md coerente con target (6 capitoli, 23 sotto-sezioni) |
| AC-T-8 | Italiano formale tecnico conciso; nessuna ridondanza vs Parti precedenti | OK | CAP_07_parte_VII.md: tutte le citazioni sono rinvii, no riscrittura |
| AC-T-9 | `reports/REPORT_CAP_07.md` prodotto con 5 sezioni + tabella verifica AC | OK | Questo file v2 con 5 sezioni aggiornate + tabella AC v2 + rollback + sezione "Iterazione 2" |
| AC-T-10 | `docs/methodology_v2/00_indice.md` aggiornato Parte VII come "IN REVIEW" | OK | 00_indice.md riga 55 aggiornata a "🟡 IN REVIEW Review v2 (rework v2 chiude 1 BUG REALE + 2 MIGLIORA PERFORMANCE)" |
| AC-T-11 | File committati e pushati su `origin/main`; working tree pulito | OK | File del rework v2 committati e pushati in chiusura del task |

### AC della checklist go-live (AC-GO, 12 AC)

Specifica nel documento (la verifica binaria empirica avviene sul run effettivo, non in questo documento metodologico):

| AC-GO ID | Criterio | Stato | Evidenza |
|----------|----------|-------|----------|
| AC-GO-1 | $DSR > \theta_{DSR} = 0{,}95$ | OK specificato | CAP_07_parte_VII.md Cap.36.1 AC-GO-1 |
| AC-GO-2 | $PBO < \theta_{PBO} = 0{,}50$ | OK specificato | CAP_07_parte_VII.md Cap.36.1 AC-GO-2 |
| AC-GO-3 | $E[R_{net}|executed] > 0$ con IC 95% bootstrap escluso lo zero | OK specificato | CAP_07_parte_VII.md Cap.36.1 AC-GO-3 |
| AC-GO-4 | $|f_5| < \theta_{f_5} = 0{,}30$ | OK specificato | CAP_07_parte_VII.md Cap.36.1 AC-GO-4 |
| AC-GO-5 | $\text{IQR}_{norm}(f_1) < \theta_{IQR} = 0{,}40$ | OK specificato | CAP_07_parte_VII.md Cap.36.1 AC-GO-5 |
| AC-GO-6 | $\text{CVaR}_{95\%} > \theta_{CVaR} = -100$ pt FIB | OK specificato | CAP_07_parte_VII.md Cap.36.1 AC-GO-6 |
| AC-GO-7 | $\text{MDD}_{intraday} < \theta_{MDD} = 200$ pt FIB | OK specificato | CAP_07_parte_VII.md Cap.36.1 AC-GO-7 |
| AC-GO-8 | $r_{emit} \in [E_{min} = 0{,}2; E_{max} = 5]$ segnali/sessione | OK specificato | CAP_07_parte_VII.md Cap.36.1 AC-GO-8 |
| AC-GO-9 | $\rho_{sessions} > \theta_{sessions} = 0{,}60$ | OK specificato | CAP_07_parte_VII.md Cap.36.1 AC-GO-9 + Cap.36.2 |
| AC-GO-10 | Pipeline Cap.27 PVI operativa: caricamento, processamento, payload bit-exact, Telegram, $L_{max}$ qualitativo | OK specificato | CAP_07_parte_VII.md Cap.36.1 AC-GO-10 |
| AC-GO-11 | Dashboard Cap.30 PVI operativa | OK specificato | CAP_07_parte_VII.md Cap.36.1 AC-GO-11 |
| AC-GO-12 | Hash bundle frozen valido all'avvio pipeline | OK specificato | CAP_07_parte_VII.md Cap.36.1 AC-GO-12 |

**Conteggio totale AC verificati v2:** 8 + 6 + 6 + 8 + 5 + 7 + 11 + 12 = **64 AC totali** (41 sui sotto-capitoli + 11 AC-T + 12 AC-GO). **Esito complessivo v2: 64/64 AC tutti OK** (AC-33-4 promosso da PARZIALE [v1] a OK [v2] con il rework Finding #1; tutti gli altri 63 AC OK già in v1, confermati OK in v2; la verifica binaria empirica degli AC-GO avviene sul run effettivo, non in questo documento metodologico).

## Domande aperte per il Planner

1. **Riconsiderazione di $\theta_{CV} = 0{,}50$ Cap.25.5 PV** (Cap.31.5 carryover): distribuzione empirica cross-fold di $CV(\hat{\boldsymbol{\beta}}_{j,R})$ del run corrente sarà input per Planner del ciclo successivo. Se concentrata in $[0{,}30; 0{,}70]$, definire nuovo $\theta_{CV}$ (es. percentile 75%).

2. **Riconsiderazione di $K_{max}^{strict} = 4$ Harrell-strict Cap.26.7 PV** (Cap.31.5 carryover): se rapporto $N_{eventi}^{strato}/K_{max} < 10$ in maggioranza fold del run corrente, Planner successivo attiva fallback nel ciclo successivo.

3. **Attivazione condizionale Cox time-varying coefficients M-16** (Cap.31.3): se run corrente produce $r_{Schoenfeld} > 0{,}50$, bundle registra `cox_time_varying_active = True` e ciclo successivo applica protocollo Parte V con specifica Cox estesa. Planner del ciclo successivo deve includere Cox time-varying in piano Parte V.

4. **Congelamento empirico 10 parametri tuning operativo Parte VI** (Cap.36.3 carryover monitoring post-go-live): a 3-6 mesi di produzione live, dati empirici sulla distribuzione alert e ricalibrazioni. Planner del ciclo successivo (o capitolo post-go-live) include revisione.

5. **Riconsiderazione soglie Cap.32-33-36 in caso di fallimento o borderline**: distribuzione empirica $DSR$ vicino $0{,}9$, $PBO$ vicino $0{,}5$, ecc. richiedono revisione delle soglie.

6. **Decisione operativa F=8 vs F~6** (Cap.34.4): regola deterministica dichiarata, esito empirico in produzione. Se `F_effective < 8`, Planner successivo include risultato compute stress test nel piano di Parte V.

7. **Convenzione serializzazione canonica per hash SHA-256** (Cap.35.2): RFC 8785 vs tupla lessicograficamente ordinata. Scelta esatta demandata all'implementazione; Planner del ciclo successivo o responsabile deployment fissa convenzione esatta.

## Criterio di rollback

Condizioni sotto cui Parte VII v1 andrebbe rivista in iterazione di rework v(N+1):

1. **Compute stress test mostra varianza inflated > 2× per F~6**: opzione (iii) Cap.34.4 non più accettabile. **Rollback**: ridimensionamento popolazione NSGA-II in Cap.26.1 PV (es. $P = 64$). Decisione Parte V ciclo successivo.

2. **$\theta_{DSR} = 0{,}95$ troppo stringente in produzione**: se 3 cicli consecutivi non passano AC-GO-1, abbassare a $\theta_{DSR} = 0{,}90$. **Rollback**: revisione Cap.32.4.

3. **Hash SHA-256 computazionalmente prohibitive per bundle > 100 MB**: valutare hash più leggero (BLAKE2, XXH64). **Rollback**: revisione Cap.35.2.

4. **Regola transizione segnali `active` Cap.35.3 Regola 1 produce inconsistenze**: revisione politica (es. tutti i segnali `active` revocati alla transizione). **Rollback**: revisione Cap.35.3 Regola 1.

5. **Compute stress test del run effettivo produce $F < 5$**: mediana cross-fold su 4 valori poco robusta. **Rollback**: revisione walk-forward in Cap.25.1 PV ($W_{in}, W_{oos}$ più corti). Decisione Parte V ciclo successivo.

6. **Review v1 trova BUG REALI strutturali sui 6 capitoli**: splitting di Parte VII in Parte VII.A (Cap.31-34 validazione statistica) + Parte VII.B (Cap.35-36 freezing + gate), con due cicli Review distinti. Decisione del supervisore al primo CONDITIONAL/FAIL.

---

## Iterazione 2 — risposta ai finding di Review v1

La Review v1 (commit `640ed61`) ha emesso verdetto **CONDITIONAL** con 5 finding classificati come 1 BUG REALE + 2 MIGLIORA PERFORMANCE + 2 NEUTRO. Il supervisore, al checkpoint Orchestratore del 2026-05-27 (commit `a1e78b5`), ha ratificato i 3 finding non-NEUTRO per Developer (1 BUG REALE Finding #1 obbligatorio + 2 MIGLIORA PERFORMANCE Finding #2 e #3 approvati). I 2 finding NEUTRO (Finding #4 esempio Cap.33.5 opaco; Finding #5 |f_5| ridondante) restano non risolti come da regola.

### Finding #1 — BUG REALE — Contraddizione interna Cap.33.4 vs Cap.34.4 sulla frazione PBO del compute budget

**Posizione v1**: `CAP_07_parte_VII.md:320` (Cap.33.4 paragrafo finale "Frazione del compute budget" dichiara "<5%") vs `CAP_07_parte_VII.md:435-439` (Cap.34.4 ammette "fino a ~10% per S=16").

**Diagnosi Review v1 (CB-1, riga 34-50 di REVIEW_CAP_07_review.md)**: il paragrafo finale di Cap.33.4 dichiara "Frazione del compute budget assorbita dal PBO è dunque inferiore al 5% del totale" ma la matematica esplicita del paragrafo precedente (Cap.33.4 stesso) dice: "Il PBO con S = 16 è ~7,7 · 10^8, ovvero ~10% del training F = 8". Cap.34.4 conferma il range fino al 10% per S=16. La dichiarazione "<5%" contraddice la matematica interna di Cap.33.4 e Cap.34.4 nel caso S=16. AC-33-4 violato alla lettera.

**Opzioni proposte dall'ACTIVE_TASK**:
- **(alpha)**: ammettere range "~1% per S=12, ~10% per S=16" coerente con i numeri esistenti (5,5e7, 7,7e8, 8e9, 6e9).
- **(beta)**: assumere caso nominale S=12 con frazione <5%.

**Scelta del Developer**: **opzione (alpha)**. Giustificazione: il documento è già strutturalmente impegnato a dichiarare entrambi i casi $S \in \{12, 14, 16\}$ in funzione di $F \in \{6, 7, 8\}$ (Cap.33.2 regola $S = 2F$, Cap.33.4 stima per $S = 16$ con $\sim 7{,}7 \cdot 10^8$ operazioni e per $S = 12$ con $\sim 5{,}5 \cdot 10^7$ operazioni, Cap.34.4 riferimento esplicito "$\sim 1\%$ per $S = 12$, fino a $\sim 10\%$ per $S = 16$"). L'opzione (beta) costringerebbe ad eliminare retroattivamente le menzioni di $S = 16$ in Cap.33.2 + Cap.33.4 + Cap.34.4 + metadati bundle di Cap.35.1 (ampliando il rework oltre il chirurgico). L'opzione (alpha) è la riformulazione minima testuale che rende il documento internamente coerente senza modifiche strutturali. Inoltre il bundle frozen registra `S` effettivo come metadato del run (Cap.35.1 elemento 6); la dichiarazione esplicita del range mantiene la regola operativa interpretabile.

**Edit applicato** (`CAP_07_parte_VII.md:320`): paragrafo "Frazione del compute budget" di Cap.33.4 riformulato come:

> "Frazione del compute budget assorbita dal PBO è dunque funzione di $S$: $\sim 1\%$ del totale per $S = 12$ (caso $F = 6$ atteso, $5{,}5 \cdot 10^7 / 6 \cdot 10^9 \approx 0{,}009$) e $\sim 10\%$ del totale per $S = 16$ (caso $F = 8$ ideale, $7{,}7 \cdot 10^8 / 8 \cdot 10^9 \approx 0{,}096$). Coerente con la dichiarazione globale di Cap.34.4 sotto sul compute budget aggregato di Parte VII (post-processing complessivo PBO + bootstrap $\leq \sim 15\%$ del compute budget nel caso peggiore $S = 16$). Il PBO non aggrava in modo critico il compute stress test e non è la causa del bundle parziale $F \approx 6$ atteso di Cap.26.2 di Parte V, che è dovuto al training NSGA-II stesso."

**Verifica numerica** (no nuovi numeri introdotti): $5{,}5 \cdot 10^7 / (6 \cdot 10^9) = 0{,}00917 \approx 0{,}009$ — OK. $7{,}7 \cdot 10^8 / (8 \cdot 10^9) = 0{,}0963 \approx 0{,}096$ — OK. Entrambe le frazioni derivano dai numeri già presenti in Cap.33.4 (5,5e7 e 7,7e8) e in Cap.34.4 (6e9 e 8e9 per training F=6 e F=8).

**Misura prima/dopo Finding #1**:

| Metrica | Prima (v1) | Dopo (v2) | Delta |
|---------|------------|-----------|-------|
| Contraddizione interna Cap.33.4 vs Cap.34.4 | PRESENTE (Cap.33.4: "<5%" vs Cap.34.4: "fino a ~10% per S=16") | ASSENTE (Cap.33.4 ora dichiara range coerente "~1% per S=12, ~10% per S=16", Cap.34.4 invariato) | -1 contraddizione |
| AC-33-4 esito | PARZIALE (dichiarazione "<5%" contraddetta dalla matematica del paragrafo precedente) | OK (dichiarazione coerente con la matematica del paragrafo precedente + con Cap.34.4) | +1 AC OK |
| Numero nuovo introdotto | 0 | 0 (uso solo numeri esistenti: 5,5e7, 6e9, 7,7e8, 8e9) | 0 |
| Impatto sul GA / fitness / ranking / signal-to-trade | 0 | 0 (correzione testuale, non tocca formule o algoritmi) | 0 |

**Promozione AC-33-4 da PARZIALE a OK** confermata nella tabella verifica AC sopra (sezione AC Cap.33).

### Finding #2 — MIGLIORA PERFORMANCE — Errore unità di misura "15 USD/h spot" c5.4xlarge (2 occorrenze)

**Posizione v1**: `CAP_07_parte_VII.md:426` (Cap.34.4 opzione ii) e `CAP_07_parte_VII.md:441` (Cap.34.4 Cloud).

**Diagnosi Review v1 (O-1, riga 56-70)**: due occorrenze di "15 USD/h spot" per c5.4xlarge. Aritmetica successiva ("15 USD/h * 80h = ~12 USD/run") incoerente (15 * 80 = 1.200, non 12). Per ottenere 12 USD/run, il prezzo deve essere **0,15 USD/h spot** (tipico spot pricing c5.4xlarge 2024-2025). Il differenziale di costo c5.9xlarge ~24,4 USD/run rispetto a c5.4xlarge ~12 USD/run usa implicitamente 0,15 USD/h. Fattore 100 di errore di unità.

**Edit applicato puntuale** (2 occorrenze):

1. `CAP_07_parte_VII.md:426` (Cap.34.4 opzione ii): sostituito "(15 USD/h spot $\cdot$ 80h $= \sim 12$ USD/run di base, con margine; ..." con "(0,15 USD/h spot $\cdot$ 80h $= \sim 12$ USD/run di base, con margine; ...". Aritmetica ora coerente: $0{,}15 \cdot 80 = 12$ USD/run base.

2. `CAP_07_parte_VII.md:441` (Cap.34.4 Cloud): sostituito "Il bootstrap gira su c5.4xlarge (16 vCPU, $\sim 15$ USD/h spot) **come post-processing aggiuntivo del walk-forward stesso**" con "Il bootstrap gira su c5.4xlarge (16 vCPU, $\sim 0{,}15$ USD/h spot) **come post-processing aggiuntivo del walk-forward stesso**". Coerente con la specifica spot c5.4xlarge tipica 2024-2025.

**Misura prima/dopo Finding #2**:

| Metrica | Prima (v1) | Dopo (v2) | Delta |
|---------|------------|-----------|-------|
| Errore unità prezzo c5.4xlarge | PRESENTE (2 occorrenze "15 USD/h" che producono 1.200 USD/run incoerente con 12 USD/run dichiarato) | ASSENTE (2 occorrenze "0,15 USD/h" coerenti con $0{,}15 \cdot 80 = 12$ USD/run) | -2 errori unità |
| Aritmetica costo opzione (ii) | Coerente solo se si reinterpreta "15 USD/h" come "0,15 USD/h" | Coerente esplicitamente: 0,15 · 80 = 12 USD/run, differenziale c5.9xlarge 24,4 USD < θ_cost = 100 USD | +1 aritmetica esplicitamente coerente |
| Impatto sul GA / fitness / ranking / signal-to-trade | 0 (errore autoreversibile) | 0 (correzione testuale di consegna) | 0 |

### Finding #3 — MIGLIORA PERFORMANCE — Errore bibliografico Notices AMS 61(5)

**Posizione v1**: `CAP_07_parte_VII.md:252` (Cap.33.1 paragrafo 1).

**Diagnosi Review v1 (O-2, riga 72-83)**: il riferimento alla pubblicazione su Notices of the American Mathematical Society 61(5) era citato come "Bailey-Borwein-Lopez de Prado-Zhu **2016** working paper preliminare". Verifica bibliografica: il volume 61 numero 5 di Notices of the AMS è del **maggio 2014** (non 2016), il paper è formale (non un working paper) e il titolo è "Pseudo-Mathematics and Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance", pp. 458-471.

**Edit applicato** (`CAP_07_parte_VII.md:252`): sostituito il riferimento errato con la citazione corretta:

> "(cfr. anche Bailey, Borwein, Lopez de Prado, Zhu 2014 'Pseudo-Mathematics and Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance', *Notices of the American Mathematical Society* 61(5), 458-471)"

**Misura prima/dopo Finding #3**:

| Metrica | Prima (v1) | Dopo (v2) | Delta |
|---------|------------|-----------|-------|
| Errore bibliografico (anno + tipo + titolo + pagine) | PRESENTE: "2016 working paper preliminare in Notices AMS 61(5)" (anno errato, tipo errato, titolo + pagine mancanti) | ASSENTE: "2014 'Pseudo-Mathematics and Financial Charlatanism: ...' Notices AMS 61(5), 458-471" (anno corretto, paper formale, titolo + pagine espliciti) | -1 errore bibliografico |
| Citazione bibliografica Bailey et al. Notices AMS | NOT OK | OK | +1 citazione corretta |
| Impatto sul GA / fitness / ranking / signal-to-trade | 0 (riferimento laterale, citazione JCF 2017 è quella primaria) | 0 (correzione bibliografica) | 0 |

### Finding #4 e #5 — NEUTRO (ignorati)

Non modificati come da decisione del supervisore. Per pulizia, **non rimossi** i `|f_5|` ridondanti in Cap.31.2 filtro 3 (`CAP_07_parte_VII.md:35`) e in Cap.36.1 AC-GO-4 (`CAP_07_parte_VII.md:576`): la rimozione opportunistica non è stata approvata; il Developer rispetta verbatim la decisione del supervisore. La forma con `|f_5|` resta matematicamente corretta (Cap.24.6 PV non garantisce esplicitamente la non-negatività di $f_5^{global}$ aggregato via mediana cross-fold, anche se per costruzione del numeratore $|f_{1,calmo} - f_{1,turbolento}|$ il rapporto è non-negativo); l'esempio Cap.33.5 PBO con il salto logico fra 8.500 e 4.500 resta come esempio illustrativo (dichiarato come tale nel testo).

### Sintesi rework v2

- **Modifiche totali**: 4 Edit puntuali (1 in Cap.33.1 per Finding #3, 1 in Cap.33.4 per Finding #1, 2 in Cap.34.4 per Finding #2 — due varianti "15 USD/h" → "0,15 USD/h"). Nessuna riscrittura strutturale.
- **AC promossi**: 1 (AC-33-4: PARZIALE → OK).
- **AC nuovi**: 0 (la Review v1 non ha introdotto nuovi AC-T trasversali).
- **AC totali post-v2**: 64/64 OK.
- **M-promemoria nuovi**: 0.
- **Carryover modificati**: 0 (CARRYOVER.md non modificato).
- **Parametri di tuning provvisori modificati**: 0 (12 parametri invariati).
- **Decisioni di scope modificate**: 0 (5/5 invariate).
- **Impatto sul GA / fitness / ranking / signal-to-trade**: 0 in tutti e 3 i finding (correzioni testuali, non toccano formule o algoritmi).
- **Replay deterministico bit-exact**: non impattato.
- **Tick FIB 5 pt**: preservato.
- **Vincolo "solo emissione"**: preservato.

### Criterio di rollback v2

Le 3 modifiche di rework v2 sono testuali e chirurgiche; il criterio di rollback sotto cui si tornerebbe al testo v1 è: **se la Review v2 trovasse che l'opzione (alpha) di Finding #1 introduce nuova incoerenza con altri sotto-capitoli non identificata in v1**, allora si tornerebbe al testo v1 e si applicherebbe l'opzione (beta) come fallback (assunzione caso nominale S=12 con frazione <5% e rimozione retroattiva delle menzioni di S=16 in Cap.33.2 + Cap.33.4 + Cap.34.4 + Cap.35.1). Per Finding #2 e #3 il rollback non è rilevante (la correzione bibliografica e l'unità di misura sono universalmente corrette per definizione esterna).

---

**Fine REPORT v2 — Parte VII pronta per Review v2.**
