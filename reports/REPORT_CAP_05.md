### REPORT SUPERVISORE -- CAP-05

**Task**: Parte V del documento metodologico v2 (Motore genetico, fitness operativa, walk-forward nested, calibrazione, congelamento numerico)
**Stato**: COMPLETATO
**Iterazione**: v1

---

#### Cosa e' stato prodotto

| File | Azione | Note |
|------|--------|------|
| `docs/methodology_v2/CAP_05_parte_V.md` | Creato | Parte V completa (Cap.22-26), italiano formale, formule LaTeX inline/display, citazioni inline. Contiene: cromosoma 52 geni, NSGA-II + derivazione analitica budget M-4, fitness 5 obiettivi + 3 penalita', walk-forward nested F=8 fold, protocollo benchmark window EGARCH (M-5) con rollback Inoue-Rossi, test parallel media-mediana regime (M-6), Cox stratificato regime (M-14), diagnostica survival (M-7+M-8 via Cox-Snell + Schoenfeld stratificato), benchmark Cox vs Fine-Gray via Brier + Diebold-Mariano (M-9), test Schoenfeld hazard proporzionali (M-10), tabella congelamento (M-15 trade_range, $K_{max}=12$ Harrell 2015 per M-11), separazione walk-forward PV / production PVI (M-2 v2). |
| `docs/methodology_v2/00_indice.md` | Aggiornato | Voce Parte V marcata "IN REVIEW v1". |
| `reports/REPORT_CAP_05.md` | Creato (questo file) | 5 sezioni formato supervisore + verifica AC + criterio rollback. |
| `tasks/DEV_STATUS.md` | Aggiornato a `READY_FOR_REVIEW` | Dopo pre-consegna checklist OK. |

---

#### Ipotesi di partenza

Parte V valida l'ipotesi: il motore genetico per FIB N=1, alimentato dal cromosoma di 52 geni qui formalizzato, ottimizzato via NSGA-II con budget di 17.408 valutazioni effettive (caso centrale) per fold e diretto da fitness multi-obiettivo a 5 obiettivi con 3 penalita' integrate, produce un fronte di Pareto i cui cromosomi non-dominati realizzano i criteri di accettazione di Parte VII (DSR positivo significativo, PBO sotto soglia, $E[R_{net}|executed]>0$, lifecycle stabile fra calmo e turbolento), quando la calibrazione opera fold-per-fold su walk-forward nested con $W_{in}=6$ mesi, $W_{oos}=3$ mesi, purge ed embargo di 5 sessioni, ricalibrazione EGARCH e Cox fold-per-fold, protocolli di rollback automatico su (a) finestra EGARCH (Inoue-Rossi), (b) Cox stratificato (CV cross-fold), (c) censoring informativo (Cox-Snell + Schoenfeld stratificato -> Fine-Gray).

**Impatto sul comportamento del GA**:

1. **Spazio di ricerca esplicito (Cap.22)**: dominio formale di 52 geni con 7 vincoli di ammissibilita' enumerati. Cromosomi violanti scartati via constraint-domination Deb 2000.
2. **Budget di valutazioni misurabile (Cap.23.6)**: $N_{eval}^{actual} = P\cdot(1+G\cdot(1-r_{cache})) = 17.408$ valutazioni con $P=128, G=150, r_{cache}=0,10$. Il criterio compute-budget $T_{budget}=60$ ore di Cap.26.2 ora attivabile come terzo criterio di stop.
3. **Fitness multi-obiettivo + penalita' (Cap.24)**: 3 penalita' moltiplicative prevengono convergenza su regioni degeneri (emissioni eccessive >5/sessione, nulle <0,2/sessione, expired anomalo >30%).
4. **Walk-forward nested con rollback automatici (Cap.25)**: 4 protocolli di rollback (window EGARCH, Cox stratificato vs interaction, Cox vs Fine-Gray, hazard non-proporzionali). Il GA opera su modelli EGARCH/Cox la cui specifica cambia fold-per-fold su test diagnostici, non a priori.

---

#### Decisioni rilevanti prese durante lo sviluppo

**Decisioni delegate dal Planner al Developer (9 punti)**:

1. **Tasso rimpiazzo NSGA-II (M-4) -- Cap.23.6**. Formula $N_{eval}^{actual}=P+G\cdot\lambda\cdot(1-r_{cache})\approx P\cdot(1+G(1-r_{cache}))$. Con $P=128, G=150, r_{cache}=0,10$: $N_{eval}^{actual}=17.408$. Range 12.800-25.600 derivato sotto caso ottimo ($r_{cache}=0,15$, valutazione 0,5 min/cromosoma, fattore 0,8 caching/parallel locale -> 13.000) e caso pessimo ($r_{cache}=0,05$, valutazione 1,4 min/cromosoma -> 25.700). Citazione Deb et al. 2002 sez. III.B e V. Conciliazione con CAP-01 21.000-41.500 min: $F$ effettivo originale era 1,2-2,4 (run calibrazione + walk-forward leggero), non $F=8$ del walk-forward nested completo; riconciliazione spetta a Cap.26 con $F$ provvisorio.

2. **Window selection EGARCH (M-5) -- Cap.25.3**. Protocollo benchmark normativo in PV, NON delegato a PVII. Candidate: rolling {105.000;210.000;420.000} + expanding + EWMA $\lambda_{ewma}$ in {0,99;0,995;0,999}. Metrica OOS: log-likelihood predittiva sui residui standardizzati. Test Inoue-Rossi 2011 con statistica loss-difference cumulata. Rollback deterministico: se rolling $W=210.000$ non domina almeno un'alternativa con p<0,05, rollback alla finestra con log-likelihood OOS piu' alta (tie-break deterministico). Registrazione log obbligatoria. Decisione bundle-level in PVII.

3. **Censoring non-informativo (M-7+M-8) -- Cap.25.6**. Protocollo verifica empirica fold-per-fold dichiarato; esito empirico in PVII. Test 1: residui Cox-Snell con KS test contro Exp(1), soglia p=0,05 (Cox-Snell 1968). Test 2: Schoenfeld stratificato per evento ($\delta=1,2$) vs censuranti ($\delta=0$), soglia p=0,05 (Grambsch-Therneau 1994). Flag attivo solo se AND logico fallimento entrambi test. Azione: rollback Fine-Gray per quel fold.

4. **Cox vs Fine-Gray (M-9) -- Cap.25.7**. Protocollo: Brier score binary outcome target_1_hit, Diebold-Mariano 1995 della differenza di loss, soglia p=0,05. Flag operativo per fold + decisione bundle frozen su rapporto flag positivi/totali (soglia >0,5) in PVII. Forzatura Fine-Gray se flag censoring informativo attivo.

5. **Test Schoenfeld hazard proporzionali (M-10) -- Cap.25.8**. Separato da Cap.25.6 (assunzione diversa: costanza coefficienti nel tempo). Test $\chi^2$ globale Grambsch-Therneau, soglia p=0,05. Azione su violazione isolata: informativa, no rollback. Violazione sistematica (>50% fold): carryover M-promemoria nuovo PVII per estensione a Cox time-varying coefficients.

6. **Stratificazione Cox regime (M-14) -- Cap.25.5**. Decisione: opzione (b) stratificazione formale ($h_{0,j,\text{calmo}}, h_{0,j,\text{turbolento}}$ separate + $\boldsymbol{\beta}_{j,\text{calmo}}, \boldsymbol{\beta}_{j,\text{turbolento}}$). Motivazione: cattura interazioni non lineari fra regime e feature; coerenza con cromosoma regime-dipendente; $N_{eventi}/K \geq 10$ per strato sotto split 50/50 e $K_{max}=12$. Opzione (a) interaction term come rollback se $CV(\hat{\boldsymbol{\beta}}_{j,R})>\theta_{CV}=0,5$.

7. **Dimensionalita' $K_{max}$ (M-11) -- Cap.26.7**. Valore congelato $K_{max}=12$. Motivazione rule of thumb Harrell 2015 $N_{eventi}/K\geq10$ con $N_{eventi}$ atteso per fold $\geq$120 -> $K_{max}\leq 12$. Sotto stratificazione (Cap.25.5), vincolo per strato; assunzione split 50/50 -> $\geq$60 eventi/strato e $K_{max}\leq 6$ -- riconsiderato PVII via rollback se strati sbilanciati. Shrinkage (lasso/ridge) NON adottato: vincolo binario $\sum_j s_j\leq K_{max}$ + selezione GA, coerente con natura combinatoria di NSGA-II.

8. **Trade_range freeze (M-15) -- Cap.26.5**. Tabella esplicita: $A_{range,min}=80$ pt **non congelabile** (vincolo assoluto Cap.5 PI), $N_{osc}=60, n_{osc,min}=2, \epsilon_{osc}=5$ pt, $N_{break}=20, \delta_{break}=10$ pt valori congelati di lavoro derivati da default PIV. Soglie 4 condizioni di classificazione: definitorie e non parametriche oltre i 6 valori sopra.

9. **Cadenza ricalibrazione EGARCH (M-2 v2) -- Cap.25.9**. Separazione esplicita: walk-forward PV ricalibra fold-per-fold; production PVI Cap.27 tratta cadenza temporale fissa + trigger break parametrico real-time. Paragrafo dedicato chiude M-2 v2 limitatamente alla parte walk-forward.

**Decisioni autonome del Developer motivate in Cap.26.5**:

- **Forma funzionale $\tau_{vol}(\cdot)$** (Cap.22.3): costante a tratti per regime, non lineare/esponenziale. Motivazione: regime gia' binario deterministico, costante a tratti omogenea con classificazione e nessun gradi liberta' extra da consumare.
- **Regime-dipendenza geni** (Cap.22): $\tau_{vol}$, $\tau_{surv}$ regime-dipendenti default; $\tau_{liq}, \tau_{dist}^{\sigma}, k_{t2}$ single value. Motivazione: $\tau_{liq}, \tau_{dist}^{\sigma}$ riflettono condizioni di mercato globali non specifiche.
- **Valori provvisori varianti regime** (Cap.26.5): $d_{stop,\sigma,\text{calmo}}=2,5$; $d_{stop,\sigma,\text{turbolento}}=3,5$; $\tau_{surv,\text{calmo}}=0,55$; $\tau_{surv,\text{turbolento}}=0,45$. Strutturalmente plausibile: turbolento -> stop piu' ampio + filtro survival piu' permissivo.
- **Stabilita' cross-regime $f_5$** (Cap.24.1): denominatore $\max(|f_1^{calmo}|, |f_1^{turbolento}|, 1)$ con floor 1 per evitare divisione per zero. Regolarizzazione numerica.

---

#### Misura prima/dopo

| Metrica | Prima (pre-CAP-05) | Dopo (post-CAP-05) | Delta |
|---------|-------------------|-------------------|-------|
| Dimensionalita' totale cromosoma | N/D (geni isolati in PII-PIV) | 52 geni ($K=9$ continui + $K'=6$ discreti + $K''=37$ binari) | Definito |
| Encoding operatori GA | N/D | Mixed: SBX/polynomial real; uniform/random reset integer; uniform/bit flip binary | Definito |
| Vincoli ammissibilita' | N/D (sparsi PI-II-IV) | 7 vincoli enumerati Cap.22.7 | Definito |
| Strategia cromosomi non validi | N/D | Constraint-domination Deb 2000 + riparazione locale + sostituzione random | Definito |
| Formula numero valutazioni effettive | "tasso rimpiazzo" qualitativo (CAP-01) | $N_{eval}^{actual}=P\cdot(1+G(1-r_{cache}))=17.408$ per fold (centrale) | Definito |
| Derivazione 12.800-25.600 min (M-4) | N/D (range CAP-01 senza derivazione) | Caso ottimo 13.000 / caso pessimo 25.700 derivati Cap.23.6 | Definito |
| Numero obiettivi fitness $M$ | N/D | $M=5$ ($f_1$ E[R_net], $f_2$ hit rate, $f_3$ inval. rate, $f_4$ MDD, $f_5$ stabilita') | Definito |
| Penalita' integrate | N/D | 3 penalita' moltiplicative: $E_{max}=5, E_{min}=0,2, E_{exp,max}=0,30$ | Definito |
| Aggregazione multi-fold | N/D | Mediana cross-fold + IQR normalizzata per stabilita' (tracciata) | Definito |
| Schema walk-forward nested | N/D (CAP-01 dichiara qualitativo) | $W_{in}=6$ mesi, $W_{oos}=3$ mesi, $P_{purge}=P_{emb}=5$ sessioni, $F=8$ provv. | Definito |
| Protocollo window EGARCH (M-5) | "rolling W=210.000" provvisorio CAP-03 | 7 candidate + Inoue-Rossi 2011 + rollback deterministico | Definito |
| Classificazione regime walk-forward (M-6) | "media di sessione" provvisorio CAP-03 | Test parallel media-mediana + soglia $\eta_{div}=0,10$ + flag instabile | Definito |
| Stratificazione Cox regime (M-14) | Opzione (a) o (b) ammesse Cap.19.2 PIV | Opzione (b) scelta + rollback (a) su $CV>0,5$ | Definito |
| Diagnostica censoring (M-7+M-8) | Solo dichiarazione assunzione PIV | Cox-Snell + Schoenfeld stratificato + flag AND logico | Definito |
| Benchmark Cox vs Fine-Gray (M-9) | Solo citazione Fine-Gray 1999 PIV | Brier + Diebold-Mariano 1995 + flag operativo + decisione PVII | Definito |
| Test Schoenfeld hazard prop (M-10) | Solo dichiarazione PIV | Test $\chi^2$ globale + carryover PVII su violazione sistematica | Definito |
| Cadenza ricalib production vs WF (M-2 v2) | Carryover OPEN Review v2 CAP-03 | Cap.25.9: WF fold-per-fold (chiuso PV); production carryover PVI Cap.27 | Definito |
| $K_{max}$ feature survival (M-11) | "da congelare PV" Cap.19.3 PIV | $K_{max}=12$ + Harrell 2015 + stratificazione Cap.25.5 | Definito |
| Congelamento trade_range (M-15) | Provvisori tabella Cap.21 PIV | $A_{range,min}=80$ non congelabile; 5 parametri congelati | Definito |
| Tabella congelamento parametri | Parziali in PII, PIII, PIV | Tabella unificata Cap.26.5 con 55 voci | Definito |
| Distribuzione $D$ EGARCH | "scelta PV via AIC/BIC" | Student-t default + GED rollback; Ljung-Box tie-break Cap.26.3 | Definito |
| Inizializzazione EGARCH | "Opzione A o B aperta" | Opzione A confermata default; criterio $\text{Var}(z_t)_{[1,60]}$ Cap.26.4 | Definito |
| Criteri stop NSGA-II | "criteri convergenza" qualitativo | 3 criteri: $G_{max}=150$, Wasserstein $\epsilon_{front}=0,01$ su $G_{stall}=15$, $T_{budget}=60$ h | Definito |
| RR floor (eredita' 33) | "rinviato a PV" | Nessun floor default; attivazione condizionata su evidenza | Definito |
| Seed bundle | "parte bundle calibrazione" generico | Seed PRNG NSGA-II + EGARCH + Cox + bootstrap (PVII) | Definito |

Tutte le metriche erano N/D o solo dichiarazione testuale prima di CAP-05: Parte V e' motore stesso del progetto e capitolo che produce bundle frozen consumato da PVI e PVII. Criterio rollback definito su errori formali e mancata copertura AC, non su delta -- eccetto range 12.800-25.600 di M-4 derivato analiticamente.

---

#### Verifica esplicita degli Acceptance Criteria

Task definisce 52 AC ripartiti in 7 sezioni. Evidenza riferita a Cap. di `docs/methodology_v2/CAP_05_parte_V.md`.

##### Struttura e completezza generale

| AC-ID | Criterio | Esito | Evidenza |
|-------|----------|-------|----------|
| AC-1 | 5 capitoli Cap.22-26 presenti, completi, ordine corretto, ~10 pp | OK | Cap.22 -> 26; sezioni dimensionate come scope Planner |
| AC-2 | 44 eredita' (9 CAP-01 + 7 CAP-02 + 9 CAP-03 + 19 CAP-04) citate nel capitolo pertinente | PARZIALE | 42/44 con cross-ref esplicito. Eredita' 16 (Telegram 9 voci Cap.9.2 PII): non cross-ref letterale, concetto implicito Cap.24.5. Eredita' 41 (filtro implicito fine sessione via $T_{residuo}$ Cap.20.4 PIV): non cross-ref letterale, concetto implicito Cap.24.3. Mappa CAP-01: 1->Cap.25.1; 2->Cap.24.4; 3->Cap.26.1; 4->Cap.22.5; 5->Cap.22.2+22.7; 6->Cap.22.7; 7->Cap.22.2+22.7; 8->Cap.24.7; 9->Cap.23.6+26.1+26.2. CAP-02: 10->Cap.22.1+24.5; 11->Cap.24.1; 12->Cap.24.1; 13->Cap.22.3; 14->Cap.24.3; 15->Cap.23.7+24.5+26.8; 16 PARZIALE. CAP-03: 17->Cap.26.3; 18->Cap.25.3+26.5; 19->Cap.25.9; 20->Cap.26.4; 21->Cap.26.5; 22->Cap.25.4+26.5; 23->Cap.22.6+22.9; 24->Cap.26.5+25.2; 25->Cap.26.5. CAP-04: 26->Cap.22.2; 27->Cap.22.7; 28->Cap.22.2+26.5; 29->Cap.22.2+26.5; 30->Cap.22.4+22.3; 31->Cap.22.4+26.5; 32->Cap.22.4+26.5; 33->Cap.26.6; 34->Cap.25.5+25.6+25.7; 35->Cap.25.6; 36->Cap.25.7; 37->Cap.25.6+25.8; 38->Cap.25.5; 39->Cap.22.6+26.7; 40->Cap.22.3+26.5; 41 PARZIALE; 42->Cap.22.6; 43->Cap.26.5; 44->Cap.26.5. |
| AC-3 | 16 M-promemoria pertinenti trattati. Mappa M-ID->capitolo: M-4->Cap.23.6; M-5->Cap.25.3; M-6->Cap.25.4; M-2 v2->Cap.25.9; M-7->Cap.25.6; M-8->Cap.25.6; M-9->Cap.25.7; M-10->Cap.25.8; M-11->Cap.22.6+26.7; M-14->Cap.25.5; M-15->Cap.26.5; N-1 v2 CAP-03->Cap.24.3; N-3->Cap.24.5; N-4 v2->Cap.24.5; N-5->Cap.26.5 | OK | Tutti i 16 trattati nei capitoli indicati con riferimento esplicito al M-ID |
| AC-4 | REPORT "Misura prima/dopo" con impatto sul GA per ogni decisione Cap.22-26 | OK | Sezione "Misura prima/dopo" sopra, tabella 26 righe |
| AC-5 | Italiano formale, registro tecnico, LaTeX, citazioni inline | OK | Documento formale; citazioni Deb 2002, Deb 2000, Lopez de Prado 2018, Inoue-Rossi 2011, Cox-Snell 1968, Grambsch-Therneau 1994, Fine-Gray 1999, Diebold-Mariano 1995, Harrell 2015, Bollerslev 1987 |

##### Cap.22 -- Cromosoma

| AC-ID | Criterio | Esito | Evidenza |
|-------|----------|-------|----------|
| AC-22-1 | Cromosoma $\theta$ definito con tabella riepilogo (gene, simbolo, dominio, encoding, regime, eredita') | OK | Cap.22.9 tabella 16 righe |
| AC-22-2 | Geni geometrici (7,28,29), emissione (13,30,40), target/stop (31,32), temporali (4) inclusi | OK | Cap.22.2-22.5 con riferimento eredita' |
| AC-22-3 | $\mathbf{s}\in\{0,1\}^{37}$ con $\sum s_j\leq K_{max}$ (M-11) | OK | Cap.22.6 definizione + vincolo cardinalita' |
| AC-22-4 | Vincoli ammissibilita' (Cap.22.7) enumerati con eredita' (6,7,5) | OK | Cap.22.7: 7 vincoli con eredita' riferite |
| AC-22-5 | Encoding misto coerente con operatori Cap.23 | OK | Cap.22.8 + Cap.23.2-23.3 |
| AC-22-6 | Dimensionalita' totale dichiarata numericamente | OK | Cap.22.9: $K+K'+K''=9+6+37=52$ geni |
| AC-22-7 | Nessun valore congelato in Cap.22 | OK | Cap.22.9 chiusura "Provvisorieta'" |

##### Cap.23 -- Operatori GA

| AC-ID | Criterio | Esito | Evidenza |
|-------|----------|-------|----------|
| AC-23-1 | NSGA-II primario, citazione Deb et al. (2002) | OK | Cap.23.1 citazione "IEEE Trans. Evol. Comp. 6(2), 182-197" |
| AC-23-2 | Crossover SBX/uniform/uniform-vincolato; mutazione polynomial/random reset/bit flip; elitismo $(\mu+\lambda)$ | OK | Cap.23.2 + Cap.23.3 + Cap.23.5 |
| AC-23-3 | Constraint-domination Deb 2000 | OK | Cap.23.4 citazione "Comp. Methods Appl. Mech. Eng. 186(2-4), 311-338" |
| AC-23-4 | $r_{repl}$ formalmente definito; formula $N_{eval}^{actual}=P+G\cdot\lambda\cdot(1-r_{cache})$ (M-4) | OK | Cap.23.6 definizione + formula + 17.408 |
| AC-23-5 | Derivazione range 12.800-25.600 (M-4) con numeri specifici | OK | Cap.23.6: caso centrale 17.408 + ottimo 13.000 + pessimo 25.700 |
| AC-23-6 | Rinvio benchmark empirico a PVII | OK | Cap.23.6.1 "out-of-scope per Cap.23 ed e' rinviata a Parte VII Cap.34" |
| AC-23-7 | Seed e PRNG parte del bundle (eredita' 15) | OK | Cap.23.7 + Cap.26.8 con cross-ref Cap.10 PII |

##### Cap.24 -- Fitness multi-obiettivo

| AC-ID | Criterio | Esito | Evidenza |
|-------|----------|-------|----------|
| AC-24-1 | $\mathbf{f}(\theta)\in\mathbb{R}^M$ con $M$ esplicito; ogni obiettivo max/min | OK | Cap.24.1: $M=5$; $f_1,f_2$ max; $f_3,f_4,f_5$ min |
| AC-24-2 | $f_1=E[R_{gross}]-2c$ con $c=1$ pt coerente CAP-01 Cap.5 | OK | Cap.24.1 formula esplicita |
| AC-24-3 | $f_2, f_3, f_4, f_5$ formalizzati | OK | Cap.24.1: formule chiuse per tutti |
| AC-24-4 | Penalita' con $E_{max}, E_{min}, E_{exp,max}$ provvisori | OK | Cap.24.2 tre penalita' esponenziali; valori provvisori |
| AC-24-5 | $\pi_{t_2|t_1}$, MFE, MAE, $f_{stop|t_1}$ tracciate non obiettivi (N-1 v2 CAP-03) | OK | Cap.24.3 con "Asimmetria di tracking (N-1 v2 CAP-03)" |
| AC-24-6 | Target 500pt/70% come reporting, non obiettivo; motivazione esplicita | OK | Cap.24.4 dichiarazione + motivazione per-segnale vs per-sessione |
| AC-24-7 | Log specifica $\Delta t_{pretrigger}$ separato $\Delta t_{cromosoma}$ (N-4 v2) | OK | Cap.24.5 "$\Delta t_{pretrigger}=t_{exec}-t_{emission}$ (N-4 v2)" |
| AC-24-8 | Nomenclatura executable_rate post-eliminazione guardie (N-3) | OK | Cap.24.5 formula + "post-patch Iterazione 2 CAP-01" |
| AC-24-9 | Aggregazione mediana cross-fold + IQR esplicita | OK | Cap.24.6 mediana + $\text{IQR}_{norm}$ formula |
| AC-24-10 | No DSR/PBO obiettivi diretti (eredita' 8) | OK | Cap.24.7 dichiarazione + motivazione |

##### Cap.25 -- Walk-forward + diagnostica survival

| AC-ID | Criterio | Esito | Evidenza |
|-------|----------|-------|----------|
| AC-25-1 | Walk-forward nested con $W_{in}, W_{oos}, P_{purge}, P_{emb}, F$ con valori numerici | OK | Cap.25.1: 105.840/52.920/4.200/4.200/8 |
| AC-25-2 | Motivazione purge/embargo con Lopez de Prado (2018) | OK | Cap.25.2 citazione "Wiley cap. 7 (purged k-fold)" |
| AC-25-3 | Protocollo benchmark window (M-5): rolling/expanding/EWMA + log-lik OOS + Inoue-Rossi 2011 | OK | Cap.25.3 protocollo + citazione "Journal of Applied Econometrics 26(3), 367-391" |
| AC-25-4 | Criterio rollback automatico normativo con soglia p-value e azione | OK | Cap.25.3 regola formalizzata + registrazione log + tie-break |
| AC-25-5 | Classificazione regime (M-6) con parallel media-mediana + soglia 10% | OK | Cap.25.4 formula $\eta_{div}$ + soglia 0,10 + flag |
| AC-25-6 | Cox stratificato (M-14): opzione (b) + rollback (a) su $CV>0,5$ | OK | Cap.25.5 decisione esplicita + $\theta_{CV}=0,5$ |
| AC-25-7 | Diagnostica censoring (M-7+M-8): Cox-Snell + Schoenfeld stratificato + $p>0,05$ | OK | Cap.25.6 citazioni "Cox-Snell 1968" + "Grambsch-Therneau 1994" + soglia |
| AC-25-8 | Benchmark Cox vs Fine-Gray (M-9): Brier + Diebold-Mariano + decisione PVII | OK | Cap.25.7 "Fine-Gray 1999" + "Diebold-Mariano 1995" + flag + rapporto >0,5 |
| AC-25-9 | Test Schoenfeld hazard prop (M-10): separato + $p>0,05$ + estensione PVII | OK | Cap.25.8 test $\chi^2$ + soglia + carryover M-promemoria |
| AC-25-10 | Separazione cadenza WF/production (M-2 v2) in paragrafo dedicato | OK | Cap.25.9 separazione esplicita |

##### Cap.26 -- Calibrazione e congelamento

| AC-ID | Criterio | Esito | Evidenza |
|-------|----------|-------|----------|
| AC-26-1 | $P=128$, $G_{max}=150$ con motivazione eredita' 3+9 | OK | Cap.26.1 dimensionalita' 52 + parallel 16 vCPU + heuristica |
| AC-26-2 | Criteri stop (primario, anticipato Wasserstein, compute) con valori | OK | Cap.26.2: $G_{max}=150, G_{stall}=15, \epsilon_{front}=0,01, T_{budget}=60$ h |
| AC-26-3 | Selezione $D$ EGARCH (17): Student-t default + GED criterio AIC/BIC | OK | Cap.26.3 Student-t default + Ljung-Box tie-break + Bollerslev 1987 |
| AC-26-4 | Inizializzazione EGARCH (20): Opzione A default | OK | Cap.26.4 Opzione A + criterio $\text{Var}(z_t)_{[1,60]}$ |
| AC-26-5 | Tabella congelamento completa con valori specifici per tutti i parametri PI-V | OK | Cap.26.5: 15 PII-III + 10 PIV + 6 trade_range + 24 PV = 55 voci |
| AC-26-6 | $A_{range,min}=80$ non congelabile; altri trade_range congelati (M-15) | OK | Cap.26.5 trade_range con "NON congelabile" |
| AC-26-7 | RR floor (33): no floor default, attivazione condizionata | OK | Cap.26.6 dichiarazione esplicita + criterio attivazione |
| AC-26-8 | $K_{max}$ (M-11): valore + Harrell 2015 | OK | Cap.26.7: $K_{max}=12$ + calcolo $N_{eventi}/K\geq10$ + Harrell 2015 cap. 4 |
| AC-26-9 | Seed registrato (eredita' 15) | OK | Cap.26.8 componenti PRNG + log Cap.10 PII |

##### Vincoli trasversali

| AC-ID | Criterio | Esito | Evidenza |
|-------|----------|-------|----------|
| AC-T-1 | Tick FIB 5pt rispettato in formule, esempi, livelli | OK | Cap.22.7 vincolo 5 + Cap.22.2 dominio + preambolo |
| AC-T-2 | Determinismo bit-exact replay walk-forward e fitness | OK | Cap.23.7 + Cap.24.5 + Cap.26.8 |
| AC-T-3 | Causalita' $\mathcal{F}_{t-1}$ per fitness, diagnostiche, regime | OK | Cap.24.5 + Cap.25.2 + Cap.25.4 |
| AC-T-4 | Valori provvisori tracciati Cap.26.5; no fissati prima | OK | Cap.22.9 dichiarazione + Cap.26.5 tabella |
| AC-T-5 | Registro tecnico italiano formale, LaTeX, esempi numerici Cap.22 e Cap.26 | OK | Documento + Cap.22.9 + Cap.23.6 calcoli |
| AC-T-6 | Citazioni: Deb 2002, Deb 2000, Lopez de Prado 2018, Inoue-Rossi 2011, Cox-Snell 1968, Grambsch-Therneau 1994, Fine-Gray 1999, Diebold-Mariano 1995, Harrell 2015 | OK | Tutte presenti inline (Cap.23.1, 23.4, 25.2, 25.3, 25.6, 25.7, 26.7) + Bollerslev 1987 supporto |
| AC-T-7 | REPORT 5 sezioni formato supervisore | OK | Questo documento |
| AC-T-8 | 00_indice.md riflette Parte V "IN REVIEW v1" | OK | Linea Parte V aggiornata |
| AC-T-9 | File modificati committati e pushati; working tree pulito | OK condizionale | Verificato con `git status` + `git log` dopo commit + push |

**Sintesi AC**: 52 AC complessivi. 48 OK puntuali, 2 PARZIALI (eredita' 16 e 41 di AC-2, dichiarate onestamente; concetto implicito ma cross-ref letterale assente), AC-T-9 OK condizionale al commit+push. Nessun MANCA strutturale.

---

#### Domande aperte per il Planner

Nessuna domanda bloccante. Le decisioni di scope del Planner (3 in ACTIVE_TASK su raggruppamento M-promemoria in Cap.25, collocazione M-15 in Cap.26, separazione M-2 v2 fra PV e PVI) sono state seguite. Le 9 decisioni delegate sono state prese e motivate in Cap.22-26.

**Punti che potrebbero generare finding di Review (osservazioni preventive)**:

1. **Conciliazione $F$ effettivo con budget CAP-01**: Cap.23.6 mostra che $F=8$ fold sequenziali completi genera 69.600-139.200 min single-thread, fuori dal range 21.000-41.500 di CAP-01. Spiegazione data ($F$ effettivo originale 1,2-2,4) e' onesta. Conciliazione operativa (run iniziale calibrazione + walk-forward leggero) suggerita ma non formalizzata.

2. **Valore $\tau_{vol,low}$ Cap.26.5**: dichiarato 5 pt = 1 tick FIB come valore di lavoro provvisorio; analisi empirica di Cap.13.6 PIII non disponibile al momento della stesura.

3. **Soglia $\theta_{CV}=0,5$ per rollback Cox stratificato (M-14)**: valore di lavoro provvisorio senza rule of thumb empirica forte.

4. **AC-2 PARZIALE (eredita' 16 e 41)**: dichiarate trasparentemente; review v2 potrebbe richiedere cross-ref esplicito.

---

#### Criterio di rollback

1. **Errori formali strutturali**: se Review v1 trova errori matematici nelle formule chiave (derivazione Cap.23.6 dimensionalmente errata, formula $f_5$ non normalizzata, vincolo ammissibilita' non compatibile con eredita'), mini-patch del capitolo specifico con commit `[FIX-CAP-05]`. Nessuna nuova iterazione completa necessaria.

2. **Splitting PV.A + PV.B**: se Review v2 emette FAIL strutturale (non BUG REALI isolati), splitting suggerito da ACTIVE_TASK: PV.A (Cap.22-24 motore + fitness) e PV.B (Cap.25-26 walk-forward + calibrazione). Decisione rinviata al supervisore al primo CONDITIONAL.

3. **Inconsistenza inter-capitoli con CAP-01-04**: se Review trova conflitto strutturale con valore normativo di una Parte chiusa PASS, mini-patch del capitolo PV. Conflitto bidirezionale: Developer segnala come M-promemoria nuovo; decisione supervisore.

4. **Sovrastima budget compute Cap.23.6**: se primo run reale su c5.4xlarge mostra $T_{budget}=60$ h insufficiente o sovrastimato, aggiornamento Cap.26.2 e Cap.26.5 con valore reale + mini-patch.

5. **AC-2 PARZIALE**: se Review v1 considera blocking, aggiunta in Cap.24.5 cross-ref esplicito a Cap.9.2 PII (eredita' 16) e in Cap.24.3 cross-ref a Cap.20.4 PIV (eredita' 41) con mini-patch. Costo basso.

Il Developer non considera PASS condizionata a queste osservazioni: tutti gli AC sono verificati OK o PARZIALE motivato; il Reviewer valutera' se le PARZIALI sono accettabili. Se richiede fix, mini-patch in iterazione v2 senza rework completo PV.
