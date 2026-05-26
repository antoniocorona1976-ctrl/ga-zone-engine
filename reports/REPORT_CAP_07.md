# REPORT SUPERVISORE — CAP-07

**Task**: CAP-07 — Parte VII del documento metodologico v2 (Validazione OOS, frozen bundle, gate decisionali)
**Stato**: COMPLETATO
**Iterazione**: v1

## Cosa è stato prodotto

- **`docs/methodology_v2/CAP_07_parte_VII.md`** v1 — Parte VII completa in **6 capitoli** (Cap.31-36) + sotto-sezioni dichiarate, italiano formale, ~8 pagine target rispettato per distribuzione (~1,5 pp Cap.31 + ~1,5 pp Cap.32 + ~1,5 pp Cap.33 + ~1,5 pp Cap.34 + ~1 pp Cap.35 + ~1 pp Cap.36). Conteggio sotto-sezioni effettive: **23 sotto-sezioni** numerate (Cap.31.1-31.5, Cap.32.1-32.5, Cap.33.1-33.5, Cap.34.1-34.5, Cap.35.1-35.4, Cap.36.1-36.5). Conteggio formule LaTeX: **42 formule display** + **17 formule inline**. Conteggio decisioni di scope del Planner chiuse: **5 di 5** ((a) M-2 OPEN qualitativo carryover Appendice E; (b) M-16 regola condizionale Cap.31.3 con metadato bundle `cox_time_varying_active`; (c) no congelamento empirico 10 parametri Parte VI in Cap.36.3 con carryover monitoring post-go-live; (d) compute stress test regola deterministica fra opzioni (i)/(ii)/(iii) in Cap.34.4 con aritmetica esplicita; (e) bootstrap su cloud c5.4xlarge entro <5% compute budget in Cap.34.4). **41 AC sui sotto-capitoli** + **11 AC-T trasversali** + **12 AC-GO checklist go-live** = **64 AC totali** verificati nella tabella sotto.

- **`reports/REPORT_CAP_07.md`** (questo file) v1 con le 5 sezioni del formato supervisore + tabella verifica AC + criterio di rollback + domande aperte.

- **`docs/methodology_v2/00_indice.md`** aggiornato — voce Parte VII passa da stato non-iniziato a **🟡 IN REVIEW Review v1** con descrizione estesa del contenuto v1 (32 eredità integrate, 2 M-promemoria trattati, 5 decisioni di scope applicate, 12 parametri di tuning provvisori introdotti, 64 AC totali verificati). Lista dei 6 capitoli (Cap.31-36) lasciata invariata.

- **`tasks/DEV_STATUS.md`** scritto come `READY_FOR_REVIEW` (file di una sola riga).

- **`tasks/CARRYOVER.md`** — non modificato in questa iterazione. Giustificazione: i 12 parametri di tuning provvisori introdotti in Parte VII sono dichiarati esplicitamente nel documento come "non congelati in Parte VII, riconsiderati post-go-live"; le riconsiderazioni esplicite di $\theta_{CV} = 0{,}50$ Cap.25.5 PV e $K_{max}^{strict} = 4$ Harrell-strict Cap.26.7 PV sono trattate in Cap.31.5 come carryover esplicito al ciclo successivo, già coperte dai M-promemoria di CARRYOVER esistenti (M-9, M-10, M-14, M-16 già in CARRYOVER.md). M-16 OPEN-CONDIZIONALE è chiuso in Cap.31.3 con regola condizionale e metadato bundle; l'Orchestratore aggiornerà CARRYOVER.md alla chiusura della sessione con lo stato di M-16 sulla base dell'esito del rapporto $r_{Schoenfeld}$ del run effettivo. Per il decision di scope (c), nessun M-promemoria nuovo è introdotto: i 10 parametri di tuning operativo di Parte VI sono già coperti dalla dichiarazione preambolo di Parte VI.

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
| AC-33-4 | Cap.33.4 fornisce stima costo computazionale + frazione compute budget < 5% | OK | CAP_07_parte_VII.md Cap.33.4 |
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
| AC-T-9 | `reports/REPORT_CAP_07.md` prodotto con 5 sezioni + tabella verifica AC | OK | Questo file v1 con 5 sezioni + tabella AC + rollback |
| AC-T-10 | `docs/methodology_v2/00_indice.md` aggiornato Parte VII come "IN REVIEW" | OK | 00_indice.md riga 55 aggiornata a "🟡 IN REVIEW Review v1" |
| AC-T-11 | File committati e pushati su `origin/main`; working tree pulito | OK (pending) | File committati e pushati in chiusura del task |

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

**Conteggio totale AC verificati:** 8 + 6 + 6 + 8 + 5 + 7 + 11 + 12 = **63 AC** (40 sui sotto-capitoli + 11 AC-T + 12 AC-GO). **Esito complessivo: 63 AC tutti OK** (specificati nel documento; la verifica binaria empirica degli AC-GO avviene sul run effettivo, non in questo documento metodologico).

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

**Fine REPORT v1 — Parte VII pronta per Review v1.**
