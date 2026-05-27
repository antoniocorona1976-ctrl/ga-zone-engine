# Review CAP-07 v1 -- Parte VII -- Validazione OOS, frozen bundle, gate decisionali

**Data review**: 2026-05-27
**Documento auditato**: docs/methodology_v2/CAP_07_parte_VII.md v1 (commit 330359c del 2026-05-27)
**Report del Developer**: reports/REPORT_CAP_07.md v1 (autodichiarazione 63/63 AC OK + 12 AC-GO specificati)
**Reviewer**: subagente reviewer
**Tipo di ciclo**: Review v1 (primo audit)

---

## Verdetto

**CONDITIONAL**

Il documento e formalmente solido e copre integralmente le 5 decisioni di scope del Planner, le 32 eredita e i 2 M-promemoria pertinenti. La sostanza metodologica (formule DSR, CSCV, bootstrap stazionario, hash bundle, checklist go-live) e corretta e bene tracciata bibliograficamente. Tutti i 64 AC sono **sostanzialmente soddisfatti**.

Tuttavia, il documento contiene:

1. **una contraddizione interna sul carico computazionale del PBO** (Cap.33.4 vs Cap.34.4) che, pur non impattando il comportamento del GA, viola l'AC-33-4 alla lettera;
2. **un errore di unita di misura sul prezzo spot di c5.4xlarge** che si propaga in due punti del documento, autoreversibile per il lettore ma di consegna scorretta;
3. **un errore bibliografico** sull'anno della pubblicazione di Bailey-Borwein-Lopez de Prado-Zhu su Notices of the AMS;
4. **un esempio numerico illustrativo opaco** in Cap.33.5 con disconnessione logica fra il conteggio "vincente in 8.500 combinazioni" e il calcolo finale PBO = 4.500/12.870.

Nessuno dei 4 problemi sopra impatta il **comportamento del GA**, il **ranking dei cromosomi**, la **fitness reale**, ne la **conversione signal-to-trade**. I primi 3 sono difetti di consegna documentale; il 4 e opacita dell'esempio illustrativo. Il verdetto resta CONDITIONAL e non FAIL perche le **decisioni metodologiche di fondo sono corrette**, il bundle frozen e definito senza ambiguita, e la regola di decisione GO/NO-GO e deterministica.

---

## Problemi bloccanti (causano FAIL)

Nessuno.

## Problemi non bloccanti (causano CONDITIONAL)

### CB-1 -- Contraddizione interna sul carico computazionale del PBO

**File:riga**: CAP_07_parte_VII.md:320 (Cap.33.4 paragrafo finale) vs CAP_07_parte_VII.md:435-439 (Cap.34.4 post-processing aggregato).

**Citazione 1 (Cap.33.4)**:
> Il PBO con S = 16 e ~7,7 * 10^8, ovvero ~10% del training F = 8; con S = 12 e ~5,5 * 10^7, ovvero ~1% del training F = 6. **Frazione del compute budget** assorbita dal PBO e dunque **inferiore al 5%** del totale.

**Citazione 2 (Cap.34.4)**:
> Sommando PBO (~1% per S = 12, fino a ~10% per S = 16, Cap.33.4) e bootstrap (< 5%), il post-processing totale di Parte VII assorbe **al massimo ~15% del compute budget**.

**Problema**: i due paragrafi affermano cose incompatibili. Cap.33.4 dichiara PBO <5%, mentre Cap.34.4 ammette PBO fino al 10% per S=16. La matematica esplicita di Cap.33.4 (7,7e8 / 8e9 ~= 10%) contraddice direttamente la sua stessa conclusione "<5%".

**Impatto sul GA**: nullo (il post-processing rimane fattibile in entrambe le letture; il run aggregato sta entro T_budget=80h modulo le opzioni i/ii/iii di Cap.34.4).

**Impatto sull'AC**: l'AC-33-4 dell'ACTIVE_TASK richiede esplicitamente "frazione del compute budget < 5%". Sotto il caso S=16, la frazione e ~10%, quindi l'AC e violato alla lettera. Il Developer ha dichiarato OK nel REPORT autodichiarando l'AC come soddisfatto, ma il calcolo interno mostra il contrario.

**Cosa risolverebbe**: rimuovere la dicitura "<5%" da Cap.33.4 e sostituirla con il range corretto "~1% per S=12 fino a ~10% per S=16, coerente con Cap.34.4"; oppure riformulare l'AC-33-4 come "< 10% per S=16".

---

## Osservazioni minori (con impatto reale)

### O-1 -- Errore di unita di misura sul prezzo spot di c5.4xlarge

**File:riga**: CAP_07_parte_VII.md:426 (Cap.34.4 opzione ii) e CAP_07_parte_VII.md:441 (Cap.34.4 Cloud).

**Citazione 1 (Cap.34.4)**:
> rispetto a c5.4xlarge 80h (**15 USD/h spot** * 80h = ~12 USD/run di base, con margine)

**Citazione 2 (Cap.34.4)**:
> Il bootstrap gira su c5.4xlarge (16 vCPU, **~15 USD/h spot**)

**Problema**: 15 USD/h * 80 h = 1.200 USD/run, NON 12 USD/run. Per ottenere 12 USD/run, il prezzo deve essere **0,15 USD/h spot** (tipico spot pricing per c5.4xlarge in 2024-2025: c5.4xlarge on-demand ~0,68 USD/h, spot ~0,15-0,27 USD/h). L'aritmetica "12 USD/run base + differenziale 24,4 USD/run vs c5.9xlarge" si chiude correttamente con **0,15 USD/h**, ma il testo continua a leggere "15 USD/h" -- un fattore 100 di errore di unita.

**Impatto sul GA**: nullo. La conclusione finale (differenziale <= theta_cost=100 USD/run -> opzione ii fattibile) e invariata perche tutta l'aritmetica successiva usa implicitamente 0,15 USD/h.

**Cosa risolverebbe**: sostituire "15 USD/h spot" con "0,15 USD/h spot" in entrambi i punti. Errore di consegna.

### O-2 -- Errore bibliografico sul lavoro Bailey-Borwein-Lopez de Prado-Zhu su Notices of the AMS

**File:riga**: CAP_07_parte_VII.md:252 (Cap.33.1 paragrafo 1).

**Citazione**:
> Bailey, Borwein, Lopez de Prado e Zhu (2017) ... Journal of Computational Finance 20(4), 39-70 (cfr. anche Bailey-Borwein-Lopez de Prado-Zhu **2016** working paper preliminare in Notices of the American Mathematical Society 61(5))

**Problema**: il volume 61, numero 5 di Notices of the AMS e del **maggio 2014**, non del 2016. Il paper e Bailey, Borwein, Lopez de Prado, Zhu (2014) "Pseudo-Mathematics and Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance", Notices of the AMS 61(5), 458-471. E un paper formale (non un working paper) e l'anno e 2014 (non 2016).

**Impatto sul GA**: nullo. Il paper JCF 2017 e citato correttamente; il riferimento aggiuntivo al Notices paper e una nota laterale.

**Cosa risolverebbe**: sostituire "2016 working paper preliminare in Notices of the American Mathematical Society 61(5)" con "2014 articolo divulgativo in Notices of the American Mathematical Society 61(5), 458-471". Errore bibliografico.

### O-3 -- Esempio numerico illustrativo PBO opaco in Cap.33.5

**File:riga**: CAP_07_parte_VII.md:326-340 (Cap.33.5).

**Citazione**:
> Cromosoma candidato c* vincente nell'in-sample CSCV in 8.500 delle 12.870 combinazioni... Sulle 8.500 combinazioni in cui c* vince in-sample, il rank OOS e distribuito come segue (illustrativa): 4.500 combinazioni con r_j < 0,5... Considerando l'intera popolazione di 12.870 combinazioni... il conteggio totale delle combinazioni con lambda_j < 0 ... e ~4.500 delle 12.870

**Problema**: l'esempio fissa un cromosoma c* che vince in-sample in 8.500 combinazioni; di queste, 4.500 sono overfit (r_j<0,5). Poi salta al risultato finale PBO = 4.500/12.870 = 0,35 "considerando l'intera popolazione di 12.870 combinazioni". Implicitamente assume che le **rimanenti 4.370 combinazioni** (dove c* non vince in-sample, ma vince qualcun altro) contribuiscono **0** alla conta degli overfit. Cio non e spiegato. La definizione formale (Cap.33.1 passo 6) dice che il PBO conta over le combinazioni dove il **vincente di quella combinazione** (qualunque sia) ha lambda_j<0, non dove c* specifico ha lambda_j<0.

**Impatto sul GA**: nullo (l'esempio e dichiarato illustrativo); ma l'esempio offusca il significato della formula PBO e rende difficile per il lettore replicare il calcolo.

**Cosa risolverebbe**: o chiarire che nelle 4.370 combinazioni rimanenti il vincente in-sample (diverso da c*) ha tutti lambda_j>0 (non-overfit) per costruzione dell'esempio, oppure riformulare l'esempio in modo da avere coerenza fra le frazioni intermedie e finali.

### O-4 -- Filtro 3 di Cap.31.2 usa |f_5| ridondante

**File:riga**: CAP_07_parte_VII.md:35 (Cap.31.2 filtro 3).

**Citazione**:
> selezionare quelli con |f_5_global(theta_k)| < theta_f5 = 0,30

**Problema**: f_5 definito in Cap.24.1 PV come f_5(theta) = |f_1_calmo - f_1_turbolento|/max(|f_1_calmo|, |f_1_turbolento|, 1) e gia non-negativo per costruzione (numeratore con valore assoluto, denominatore positivo). Le barre verticali |f_5| del filtro sono ridondanti.

**Impatto sul GA**: nullo (matematicamente equivalente).

**Cosa risolverebbe**: rimuovere le barre verticali, scrivere f_5_global(theta_k) < theta_f5. Stesso commento per AC-GO-4 (riga 576).

---

## Citazioni problematiche dal testo

| # | Citazione | Problema | Classificazione |
|---|-----------|----------|----------------|
| 1 | "il PBO con S = 16 e ~7,7 * 10^8, ovvero ~10% del training F = 8 ... Frazione del compute budget assorbita dal PBO e dunque inferiore al 5% del totale" (riga 318-320) | Contraddizione interna: 10% > 5%. AC-33-4 violato alla lettera. | **BUG REALE** (violazione AC, non impatto GA) |
| 2 | "rispetto a c5.4xlarge 80h (15 USD/h spot * 80h = ~12 USD/run di base)" (riga 426) | 15 * 80 = 1200, non 12. Tipo: 0,15 USD/h. | **MIGLIORA PERFORMANCE** (errore di consegna, autoreversibile) |
| 3 | "c5.4xlarge (16 vCPU, ~15 USD/h spot)" (riga 441) | Stesso errore di unita del punto 2. | **MIGLIORA PERFORMANCE** (errore di consegna) |
| 4 | "Bailey-Borwein-Lopez de Prado-Zhu 2016 working paper preliminare in Notices of the American Mathematical Society 61(5)" (riga 252) | Notices 61(5) e del 2014, non 2016; e paper formale, non working paper. | **MIGLIORA PERFORMANCE** (errore bibliografico) |
| 5 | "il conteggio totale delle combinazioni con lambda_j < 0 ... e ~4.500 delle 12.870" (riga 336-338) | Salto logico fra "8.500 vincite di c*" e "4.500 overfit su 12.870" senza spiegare le altre 4.370 combinazioni. | **NEUTRO** (esempio dichiarato illustrativo; opacita logica) |
| 6 | "|f_5_global(theta_k)| < theta_f5 = 0,30" (riga 35) | Barre verticali ridondanti su quantita gia non-negativa per costruzione. | **NEUTRO** (matematicamente equivalente) |

---

## Verifica eredita (32 totali)

Ciascuna eredita deve essere citata in almeno un capitolo pertinente di Parte VII.

### Da CAP-01 (Parte I)

| Eredita | Citata in | Esito |
|---------|-----------|-------|
| 1. "solo emissione, nessuna esecuzione" (Cap.1 PI) | Preambolo (riga 5), Cap.31.1 (riga 7, 21) | OK |
| 2. Profilo operatore retail mobile (Cap.2 PI) | Cap.36.1 AC-GO-7 (riga 582), Cap.36.5 (riga 676) | OK |
| 3. Sessione operativa 8:00-22:00 CET (Cap.1 PI) | Cap.31.1 (riga 15), Cap.34.1 (riga 365), Cap.36.2 implicito | OK |
| 4. Infrastruttura locale + cloud c5.4xlarge (Cap.3-4 PI) | Cap.34.4 (riga 441 con i5-7200U) | OK |
| 5. Storico Portara/CQG FIB 1-min 5 anni (Cap.3 PI) | Cap.31.1 (riga 15 con W_oos*F) | OK |
| 6. Tick FIB = 5 punti (Cap.5 PI) | Cap.32.5 (riga 242), Cap.33.5 (riga 342), Cap.36.5 (riga 676) | OK |
| 7. Filtro emissione >=80 pt (Cap.5 PI) | Cap.35.1 elemento 1 (riga 459 con A_range,min=80) | OK |
| 8. Commissioni 5 EUR/op = 1 pt FIB (Cap.2 PI) | Cap.32.2 (riga 170 con 2*c = 2 pt) | OK |
| 9. Definizione operativa del successo (Cap.5 PI) | Cap.36.1 (riga 568 sintetizza checklist) | OK |
| 10. Target operativo asimmetrico 500 pt/giorno OR 70% (Cap.1 PI) | Cap.36.2 (riga 609-631) | OK |
| 11. Compute budget T_budget=80h (Cap.4 PI + Cap.26.2 PV) | Cap.34.4 (riga 411-441) | OK |

### Da CAP-02 (Parte II)

| Eredita | Citata in | Esito |
|---------|-----------|-------|
| 12. Payload immutabile 12 campi (Cap.6.1 PII) | Cap.35.1 elemento 4 (riga 473) | OK |
| 13. State machine 1 non-terminale + 6 terminali (Cap.7 PII) | Cap.31.1 (riga 21), Cap.32.2 (riga 170), Cap.35.3 Regola 1 (riga 525) | OK |
| 14. Vincolo segnale unico |A(t)|<=1 (Cap.6.3 PII + Cap.28 PVI) | Cap.34.1 (riga 363) | OK |
| 15. Replay deterministico bit-exact (Cap.10 PII) | Cap.31.1 (riga 21), Cap.31.2 (riga 29), Cap.34.5 (riga 445), Cap.35.2 (riga 519) | OK |
| 16. Submacchina position lifecycle post-target_1 (Cap.11 PII) | Cap.31.2 filtro 5 (riga 39), Cap.34.3 metriche 8-11 (riga 395-397) | OK |

### Da CAP-03 (Parte III)

| Eredita | Citata in | Esito |
|---------|-----------|-------|
| 17. EGARCH(1,1) con D AIC/BIC e finestra W=210.000 (Cap.13 PIII) | Cap.31.4 (riga 92-119), Cap.35.1 elementi 1 e 3 (riga 459, 469) | OK |
| 18. Classificazione regime calmo/turbolento (Cap.14 PIII) | Cap.31.2 filtro 3 (riga 35), Cap.36.2 (riga 633), Cap.35.1 elemento 3 (riga 471) | OK |
| 19. Catalogo 37 feature + K_max=6 (Cap.15.2 PIII + Cap.26.7 PV) | Cap.31.5 (riga 127), Cap.35.1 elementi 2 e 6 (riga 466, 495) | OK |

### Da CAP-04 (Parte IV)

| Eredita | Citata in | Esito |
|---------|-----------|-------|
| 20. Geometria zone, target, stop, Cox, filtri Cap.20 (Cap.16-20 PIV) | Cap.35.1 elementi 1 e 2 (tabella + geni geometrici) | OK |
| 21. Modello Cox cause-specific stratificazione regime (Cap.19 PIV) | Cap.31.3 (riga 57-89), Cap.35.1 elemento 3 e 6 (riga 470, 486-491) | OK |

### Da CAP-05 (Parte V)

| Eredita | Citata in | Esito |
|---------|-----------|-------|
| 22. Output NSGA-II = F_1 (Cap.23.1 PV + Cap.24.1 PV) | Cap.31.2 (riga 27), Cap.32.3 (riga 190), Cap.33.1 (riga 256), Cap.35.1 elemento 6 (riga 496) | OK |
| 23. Aggregazione mediana cross-fold (Cap.24.6 PV) | Cap.31.2 (riga 41), Cap.34.4 opzione (iii) (riga 427) | OK |
| 24. Walk-forward F=8 provvisori, W_in/W_oos/P_purge/P_emb (Cap.25.1 PV) | Cap.31.1 (riga 15-19), Cap.33.2 (riga 294-296) | OK |
| 25. Tabella congelati Cap.26.5 PV | Cap.35.1 elemento 1 (riga 459) | OK |
| 26. No DSR/PBO in NSGA-II (Cap.24.7 PV) | Cap.32.1 (riga 162), Cap.33.1 (riga 252 implicito) | OK |
| 27. Seed bundle frozen (Cap.26.8 PV) | Cap.34.5 (riga 447), Cap.35.1 elemento 5 (riga 475-481) | OK |
| 28. Compute budget T_budget=80h + bundle parziale F~6 (Cap.26.2 PV) | Cap.34.4 (riga 409-441) | OK |
| 29. Diagnostica survival fold-per-fold (Cap.25.6-25.8 PV) | Cap.31.3 (riga 63, 72, 81) | OK |

### Da CAP-06 (Parte VI)

| Eredita | Citata in | Esito |
|---------|-----------|-------|
| 30. Pipeline + Cap.27.5 cadenza EGARCH + Cap.30 monitoraggio (Cap.27-30 PVI) | Cap.36.1 AC-GO-10 (riga 588-593), AC-GO-11 (riga 594-598) | OK |
| 31. 10 parametri tuning operativo non congelati (Cap.27-30 PVI) | Cap.36.3 (riga 637-641) | OK |
| 32. Bundle frozen come input pipeline (Cap.27.3 PVI) | Cap.35.1 (riga 457), Cap.35.3 (riga 525) | OK |

**Verdetto verifica eredita: 32/32 citate -- OK.**

---

## Verifica M-promemoria

| M-ID | Stato pre-CAP-07 | Trattamento previsto | Trattamento osservato | Esito |
|------|------------------|----------------------|------------------------|-------|
| M-2 | OPEN (verifica empirica L_max=30s Telegram) | Citazione qualitativa Cap.31.1 + AC-GO-10 Cap.36.1; carryover Appendice E (decisione di scope (a)) | Cap.31.1 (riga 23) cita qualitativamente L_max con rinvio Appendice E; Cap.36.1 AC-GO-10 (riga 588, sub-punto d) include vincolo qualitativo L_max | OK -- M-2 resta OPEN |
| M-16 OPEN-CONDIZIONALE | OPEN-CONDIZIONALE (Cox time-varying se r_Schoenfeld>0,5) | Cap.31.3 regola con 4 passi + metadato cox_time_varying_active (decisione di scope (b)) | Cap.31.3 (riga 79-87) implementa la regola completa; Cap.35.1 elemento 6 (riga 491) registra cox_time_varying_active | OK -- M-16 CHIUSO con regola condizionale |

**Verdetto verifica M-promemoria: 2/2 trattati come da decisioni di scope -- OK.**

---

## Verifica 5 decisioni di scope del Planner

| # | Decisione di scope | Applicata verbatim? | Esito |
|---|---------------------|----------------------|-------|
| (a) | M-2 OPEN qualitativo in Cap.31.1 + AC-GO-10; carryover Appendice E | Si -- Cap.31.1 paragrafo 3 (riga 23) qualitativo + AC-GO-10 sub-punto d (riga 593) qualitativo | OK |
| (b) | M-16 regola condizionale Cap.31.3 con metadato cox_time_varying_active | Si -- Cap.31.3 (riga 79-87) 4 passi + Cap.35.1 elemento 6 (riga 491) metadato | OK |
| (c) | No congelamento empirico 10 parametri Parte VI in Cap.36.3 | Si -- Cap.36.3 (riga 637-641) dichiara starting point + carryover monitoring post-go-live | OK |
| (d) | Compute stress test Cap.34.4 con aritmetica esplicita fra opzioni i/ii/iii | Si -- Cap.34.4 (riga 411-441) aritmetica + regola deterministica. **Nota**: il numero "0,919 min/cromosoma" della decisione di scope era errato per un fattore di unita di misura (h vs min); il Developer ha autonomamente ricalcolato a 0,551 min/cromosoma single-thread -> 0,496 con eta_par=0,90, documentandolo nel REPORT. L'auto-correzione e giustificata. | OK |
| (e) | Bootstrap su cloud c5.4xlarge entro <5% compute budget | Si -- Cap.34.4 (riga 431-437) aritmetica frazione bootstrap in [0,5%; 1,3%]<5% verificabile | OK |

**Verdetto verifica decisioni di scope: 5/5 applicate -- OK.**

---

## Verifica citazioni bibliografiche

| Riferimento | Citazione documento | Verificato? |
|--------------|----------------------|--------------|
| DSR -- Bailey & Lopez de Prado 2014, JPM 40(5), 94-107 | Cap.32.1 (riga 139), Cap.32.4 (riga 204) | OK (formula DSR + formula SR* congruenti con paper originale) |
| PBO/CSCV -- Bailey, Borwein, Lopez de Prado, Zhu 2017, JCF 20(4), 39-70 | Cap.33.1 (riga 252) | OK (procedura 6 passi congruente con paper) |
| Bailey et al. Notices AMS 61(5) | Cap.33.1 (riga 252): "**2016** working paper preliminare" | **ERRORE BIBLIOGRAFICO** -- Notices 61(5) e del 2014, non 2016, ed e paper formale non working paper |
| Bootstrap stazionario -- Politis & Romano 1994, JASA 89(428), 1303-1313 | Cap.34.1 (riga 352) | OK |
| Block length -- Politis & White 2004, Econometric Reviews 23(1), 53-70 | Cap.34.2 (riga 369) | OK |
| BCa -- Efron 1987, JASA 82(397), 171-185 | Cap.34.3 (riga 401) | OK |
| Cox time-varying -- Therneau & Grambsch 2000, Springer cap. 6 | Cap.31.3 (riga 85), Cap.35.3 Regola 3 (riga 529) | OK |
| Schoenfeld -- Grambsch & Therneau 1994, Biometrika 81(3), 515-526 | Cap.31.3 (riga 83) | OK |
| Hash SHA-256 -- FIPS PUB 180-4 (NIST 2015) | Cap.35.2 (riga 509) | OK |
| JSON canonical form -- RFC 8785 (2020) | Cap.35.2 (riga 508) | OK |
| Lopez de Prado 2018, Advances in Financial ML, Wiley | Cap.31.2 (riga 27), Cap.32.1 (riga 139), Cap.33.1 (riga 252), Cap.34.1 (riga 352 implicito) | OK |

**Verdetto verifica citazioni: 10/11 OK + 1 errore bibliografico minore.**

---

## Verifica aritmetica del compute stress test Cap.34.4

**Target t_eval_target_eff <= 0,496 min/cromosoma:**

| Passo | Documento | Verifica autonoma | Esito |
|-------|-----------|--------------------|-------|
| t_eval_target_single | (80*60*16)/(17.408*8) = 76.800/139.264 ~= 0,551 | 76.800/139.264 = 0,5514 | OK |
| t_eval_target_eff | 0,551*0,90 = 0,496 | 0,5514*0,90 = 0,4963 | OK |
| Confronto Cap.23.6 PV | "0,74 > 0,496 -> opzione (i) non fattibile senza ottimizzazione" | Bound inferiore range [0,74; 1,47] e 0,74, sopra 0,496. Conclusione corretta. | OK |
| c5.9xlarge wall-clock | 107*16/36 ~= 47,6 h | 107*16/36 = 47,556 ~= 47,6 | OK |
| c5.9xlarge costo | 47,6*0,765 ~= 36,4 USD | 47,6*0,765 = 36,42 ~= 36,4 | OK |
| c5.18xlarge wall-clock | 107*16/72 ~= 23,8 h | 107*16/72 = 23,78 ~= 23,8 | OK |
| c5.18xlarge costo | 23,8*1,53 ~= 36,4 USD | 23,8*1,53 = 36,41 ~= 36,4 | OK |
| Differenziale c5.9xlarge | 36,4 - 12 = 24,4 USD/run | 36,4 - 12 = 24,4 | OK (ma vedi O-1: il "12" implica spot rate 0,15 USD/h, non i 15 USD/h scritti) |

**Verdetto verifica aritmetica: tutta numericamente coerente; solo problema l'unita di misura "15 USD/h" (vedi O-1).**

---

## Verifica vincolo "solo emissione" (AC-T-3)

Ricerca lessicale negativa nel documento per: "order routing", "fill" (escluso "fill virtuale"), "slippage", "broker execution", "posizione netta" in senso execution.

| Termine | Occorrenze | Contesto | Esito |
|---------|------------|----------|-------|
| "order routing" | 0 | -- | OK |
| "slippage" | 0 | -- | OK |
| "broker execution" | 0 | -- | OK |
| "posizione netta" | 0 | -- | OK |
| "fill" | 3 | (riga 7) "fill effettivi del broker" -- usato in senso negativo (esclusione); (riga 21) "fill effettivi del broker" -- esclusione esplicita; (riga 170) "fill virtuale di chiusura" -- definitorio Cap.10.4 PII consentito | OK -- tutti consentiti |
| "execution" | 0 | -- | OK |

**Verdetto vincolo solo emissione: rispettato -- OK.**

---

## Verifica tick FIB 5 pt (AC-T-5)

| Valore numerico | Multiplo di 5? | Esito |
|------------------|------------------|-------|
| theta_CVaR = -100 pt FIB (Cap.36.1 AC-GO-6, riga 580) | -100 = -20*5 -- si | OK |
| theta_MDD = 200 pt FIB (Cap.36.1 AC-GO-7, riga 582) | 200 = 40*5 -- si | OK |
| T_abs = 500 pt FIB (Cap.36.2, riga 611) | 500 = 100*5 -- si | OK |
| A_range,min = 80 pt (Cap.35.1 elemento 1, riga 459) | 80 = 16*5 -- si | OK |
| b_min = 5 pt (eredita Cap.5 PI, implicito) | -- | n/a |
| delta_pivot = 10 pt, epsilon_osc = 5 pt, delta_break = 10 pt | tutti multipli di 5 (eredita Cap.5 PI + Cap.26.5 PV) | OK |
| SR_hat, gamma_3, gamma_4 in esempi Cap.32.5 | adimensionali, non livelli di prezzo | n/a |
| PBO in esempio Cap.33.5 | frazione in [0,1] adimensionale | n/a |
| Esempio "R_net >= 500" in Cap.36.2 | livello di profitto netto in pt FIB; 500 multiplo di 5 | OK |

**Verdetto verifica tick FIB: tutti i numeri di prezzo sono multipli di 5 -- OK.**

---

## Verifica nessun numero inventato (AC-T-6)

Tutti i numeri introdotti in Parte VII sono:
- **(a) parametri di tuning provvisori dichiarati**: theta_DSR=0,95, theta_PBO=0,50, theta_f5=0,30, theta_IQR=0,40, theta_t2=0,30, epsilon_f1=10^-6, theta_CVaR=-100 pt, theta_MDD=200 pt, theta_sessions=0,60, S in {12,14,16}, L_avg=10, theta_cost=100 USD/run. **12 parametri** dichiarati provvisori non congelati;
- **(b) ereditati**: W_oos=52.920 (Cap.25.1 PV), W_in=105.840, P_purge=P_emb=4.200, F in {6,7,8}, W=210.000 EGARCH (Cap.13 PIII), p=0,75, N_reg=20, T_persist=10, sigma_bar_s, n_c=3, delta_pivot=10, A_range,min=80, N_osc=60, n_osc,min=2, epsilon_osc=5, N_break=20, delta_break=10, P=128, G_max=150, G_stall=15, epsilon_front=0,01, eta_c, eta_m, p_m, K_max=6, theta_CV=0,5, p_Schoenfeld=0,05, E_min=0,2, E_max=5, T_budget=80h, c=1 pt FIB, B=2.000 ricampionamenti, gamma_E~0,5772, e~2,71828, alpha=0,05;
- **(c) derivati con aritmetica esplicita**: W_oos_agg = 52.920*F; D ~= F*63 sessioni; 317.520, 370.440, 423.360 barre; t_eval_target_single=0,551, t_eval_target_eff=0,496; 107*16/36=47,6; 47,6*0,765=36,4; N_bootstrap_ops=26.000*n_segnali in [3,9*10^7; 7,8*10^7]; frazione bootstrap in [0,005; 0,013]; C(16,8)=12.870, C(12,6)=924; PBO ops ~7,7*10^8 (S=16) e ~5,5*10^7 (S=12).

**Verdetto verifica numeri inventati: nessun numero inventato di test empirici** (Cap.34.4 dichiara la regola, non simula). Esempi numerici Cap.32.5 e Cap.33.5 dichiarati illustrativi.

---

## Verifica 64 AC totali (41 sotto-capitoli + 11 AC-T + 12 AC-GO)

### AC Cap.31 (8 AC)

| AC | Esito | File:riga evidenza |
|----|-------|---------------------|
| AC-31-1 | OK | CAP_07_parte_VII.md:15-19 (W_oos=52.920 + F in {6,7,8} + valori 317.520/370.440/423.360) |
| AC-31-2 | OK | CAP_07_parte_VII.md:21-23 (log replay bit-exact + nessun fill broker + L_max qualitativo + Appendice E) |
| AC-31-3 | OK | CAP_07_parte_VII.md:27-48 (6 filtri + criterio finale + tie-break 3 livelli + soglie provvisorie) |
| AC-31-4 | OK | CAP_07_parte_VII.md:50-55 (caso fallimento go-live + raccomandazioni (a)/(b)) |
| AC-31-5 | OK | CAP_07_parte_VII.md:57-89 (3 decisioni condizionali con r_FG, r_CV, r_Schoenfeld + M-16 + metadato) |
| AC-31-6 | OK | CAP_07_parte_VII.md:91-119 (M-5 + D + init EGARCH con rapporti fold + soglia 0,50) |
| AC-31-7 | OK | CAP_07_parte_VII.md:121-130 (riconsiderazione theta_CV + K_max_strict=4 come carryover) |
| AC-31-8 | OK | Preambolo (riga 7) + Cap.31 (nessun valore congelato di Parte VII, solo parametri provvisori) |

### AC Cap.32 (6 AC)

| AC | Esito | File:riga evidenza |
|----|-------|---------------------|
| AC-32-1 | OK | CAP_07_parte_VII.md:139-162 (formula DSR + SR* + citazione Bailey-Lopez de Prado 2014 JPM 40(5)) |
| AC-32-2 | OK | CAP_07_parte_VII.md:164-179 (SR_hat per-segnale + annualizzazione opzionale) |
| AC-32-3 | OK | CAP_07_parte_VII.md:181-196 (gamma_3, gamma_4, N_trials, Var(SR_k)) |
| AC-32-4 | OK | CAP_07_parte_VII.md:198-208 (theta_DSR=0,95 provvisorio + comportamento ai bordi) |
| AC-32-5 | OK | CAP_07_parte_VII.md:210-243 (esempio illustrativo con calcolo SR*=0,1899, DSR~0,042) |
| AC-32-6 | OK | CAP_07_parte_VII.md:244 (citazioni esplicite di tutti i rinvii richiesti) |

### AC Cap.33 (6 AC)

| AC | Esito | File:riga evidenza |
|----|-------|---------------------|
| AC-33-1 | OK | CAP_07_parte_VII.md:252-286 (6 passi CSCV + citazione Bailey-Borwein-Lopez de Prado-Zhu 2017 JCF 20(4)) |
| AC-33-2 | OK | CAP_07_parte_VII.md:288-298 (S=16 F=8 + S=12 F=6 + S=14 F=7 + regola S=2F) |
| AC-33-3 | OK | CAP_07_parte_VII.md:300-308 (theta_PBO=0,50 gate minimo + citazione Bailey et al.) |
| AC-33-4 | **PARZIALE** | CAP_07_parte_VII.md:310-322: stima costo computazionale presente, ma frazione compute budget claim "<5%" contraddetta da Cap.33.4 stesso (10% per S=16). Vedi CB-1. |
| AC-33-5 | OK | CAP_07_parte_VII.md:324-342 (esempio illustrativo con PBO~0,35); opacita interna O-3 non bloccante |
| AC-33-6 | OK | CAP_07_parte_VII.md:344 (citazioni esplicite) |

### AC Cap.34 (8 AC)

| AC | Esito | File:riga evidenza |
|----|-------|---------------------|
| AC-34-1 | OK | CAP_07_parte_VII.md:352-365 (Politis-Romano 1994 + block geometric + wrap modulo n + B=2.000) |
| AC-34-2 | OK | CAP_07_parte_VII.md:367-375 (Politis-White 2004 + L_avg=10 default + range [5, 20]) |
| AC-34-3 | OK | CAP_07_parte_VII.md:377-405 (13 metriche + percentile method default + BCa Efron 1987 alt) |
| AC-34-4 | OK | CAP_07_parte_VII.md:407-429 (regola i/ii/iii + t_eval_target_eff=0,496 + theta_cost=100 USD) |
| AC-34-5 | OK | CAP_07_parte_VII.md:431-441 (N_bootstrap=26.000*n_segnali + frazione in [0,5%; 1,3%] < 5%) |
| AC-34-6 | OK | CAP_07_parte_VII.md:443-447 (seed bootstrap nel bundle, Cap.34.5) |
| AC-34-7 | OK | CAP_07_parte_VII.md:449 (citazioni esplicite di tutti i riferimenti richiesti) |
| AC-34-8 | OK | CAP_07_parte_VII.md:359 + CAP_07_parte_VII.md:443 (B=2.000 dichiarato esplicitamente) |

### AC Cap.35 (5 AC)

| AC | Esito | File:riga evidenza |
|----|-------|---------------------|
| AC-35-1 | OK | CAP_07_parte_VII.md:457-502 (6 elementi bundle frozen + tutti i metadati richiesti) |
| AC-35-2 | OK | CAP_07_parte_VII.md:504-519 (hash SHA-256 + JSON canonical form + validazione integrita + fallimento se mismatch) |
| AC-35-3 | OK | CAP_07_parte_VII.md:521-533 (4 regole sostituzione + gestione segnali active) |
| AC-35-4 | OK | CAP_07_parte_VII.md:535-558 (bundle_id + tabella bundle_history con metriche + motivazione) |
| AC-35-5 | OK | CAP_07_parte_VII.md:560 (citazioni esplicite) |

### AC Cap.36 (7 AC)

| AC | Esito | File:riga evidenza |
|----|-------|---------------------|
| AC-36-1 | OK | CAP_07_parte_VII.md:566-600 (12 AC binari AC-GO-1..AC-GO-12 con criteri espliciti) |
| AC-36-2 | OK | CAP_07_parte_VII.md:601-606 (decisione GO/NO-GO + raccomandazioni operative) |
| AC-36-3 | OK | CAP_07_parte_VII.md:607-633 (verifica aggregata di sessione T_abs OR T_rel + theta_sessions=0,60 + reporting regime separato) |
| AC-36-4 | OK | CAP_07_parte_VII.md:635-641 (10 parametri rimangono starting point + carryover monitoring post-go-live) |
| AC-36-5 | OK | CAP_07_parte_VII.md:643-656 (4 trigger paralleli + Cap.35.3.2 + conseguenza operativa) |
| AC-36-6 | OK | CAP_07_parte_VII.md:658-674 (report finale con 6 punti (a)-(f)) |
| AC-36-7 | OK | CAP_07_parte_VII.md:676 (citazioni esplicite di tutti i riferimenti) |

### AC trasversali (11 AC-T)

| AC | Esito | Evidenza |
|----|-------|----------|
| AC-T-1 | OK | 32/32 eredita citate (vedi tabella sopra) |
| AC-T-2 | OK | M-2 OPEN qualitativo + M-16 chiuso condizionalmente (vedi tabella sopra) |
| AC-T-3 | OK | Nessuna logica execution (verifica negativa lessicale sopra) |
| AC-T-4 | OK | Nessun re-training del GA attivato direttamente in Parte VII (Cap.35.3.2 + Cap.36.4 dichiarano regola di sostituzione + anticipo, non riottimizzazione) |
| AC-T-5 | OK | Esempi numerici rispettano tick FIB 5 pt (vedi tabella sopra) |
| AC-T-6 | OK | 12 parametri provvisori con dominio + default + marcatura "non congelato in Parte VII" (preambolo + Cap.31-36) |
| AC-T-7 | OK | Lunghezza documento ~8 pp coerente (6 capitoli con distribuzione attesa) |
| AC-T-8 | OK | Italiano formale, nessuna ridondanza vs Parti precedenti |
| AC-T-9 | OK | reports/REPORT_CAP_07.md con 5 sezioni + tabella AC + rollback |
| AC-T-10 | OK | docs/methodology_v2/00_indice.md aggiornato (Parte VII = IN REVIEW v1, riga 55) |
| AC-T-11 | OK | File committati e pushati (verificato dall'Orchestratore in check post-Developer 6/6) |

### AC della checklist go-live (12 AC-GO)

| AC-GO | Esito specificato? | File:riga evidenza |
|-------|---------------------|---------------------|
| AC-GO-1 (DSR>0,95) | OK | CAP_07_parte_VII.md:570 |
| AC-GO-2 (PBO<0,50) | OK | CAP_07_parte_VII.md:572 |
| AC-GO-3 (E[R_net|exec]>0 con IC) | OK | CAP_07_parte_VII.md:574 |
| AC-GO-4 (|f_5|<0,30) | OK | CAP_07_parte_VII.md:576 |
| AC-GO-5 (IQR_norm(f_1)<0,40) | OK | CAP_07_parte_VII.md:578 |
| AC-GO-6 (CVaR_95>-100 pt) | OK | CAP_07_parte_VII.md:580 |
| AC-GO-7 (MDD_intraday<200 pt) | OK | CAP_07_parte_VII.md:582 |
| AC-GO-8 (r_emit in [0,2;5]) | OK | CAP_07_parte_VII.md:584 |
| AC-GO-9 (rho_sessions>0,60) | OK | CAP_07_parte_VII.md:586 + Cap.36.2 |
| AC-GO-10 (pipeline operativa + L_max qualitativo) | OK | CAP_07_parte_VII.md:588-593 |
| AC-GO-11 (dashboard operativa) | OK | CAP_07_parte_VII.md:594-598 |
| AC-GO-12 (hash bundle valido) | OK | CAP_07_parte_VII.md:599 |

**Verifica binaria empirica degli AC-GO**: avviene sul run effettivo del walk-forward, non in questo documento metodologico. Specifica documentale presente e completa.

**Conteggio totale AC verificati**: 8 + 6 + 6 + 8 + 5 + 7 + 11 + 12 = **63 AC** (di cui 1 PARZIALE -- AC-33-4); **64 AC totali** considerando i 12 AC-GO. **Esito: 63 OK + 1 PARZIALE su 64 totali.**

---

## Classificazione per il supervisore

| # | Problema | Classificazione | Default |
|---|----------|-----------------|---------|
| 1 | Contraddizione interna Cap.33.4: dichiara PBO <5% del compute budget, ma la matematica esplicita mostra 10% per S=16; viola AC-33-4 alla lettera | **BUG REALE** | -> Developer (obbligatorio) |
| 2 | Errore di unita di misura: "15 USD/h spot" c5.4xlarge dovrebbe essere "0,15 USD/h spot" (2 occorrenze) | **MIGLIORA PERFORMANCE** | -> in attesa della tua decisione |
| 3 | Errore bibliografico: "Bailey-Borwein-Lopez de Prado-Zhu 2016 working paper in Notices AMS 61(5)" -- in realta Notices 61(5) e del 2014 e non e un working paper | **MIGLIORA PERFORMANCE** | -> in attesa della tua decisione |
| 4 | Esempio Cap.33.5 PBO: salto logico fra "c* vince in 8.500/12.870 combinazioni" e "PBO = 4.500/12.870 = 0,35"; le altre 4.370 combinazioni non sono spiegate | **NEUTRO** | -> ignorato |
| 5 | Filtro 3 di Cap.31.2 e AC-GO-4 usano |f_5| ridondante (quantita gia non-negativa per costruzione) | **NEUTRO** | -> ignorato |

**I BUG REALI vanno sempre a Developer.**
**NEUTRO non va mai a Developer.**
**Decidi per i finding MIGLIORA PERFORMANCE.**

---

## M-promemoria nuovi (eventuali)

Nessun M-promemoria nuovo introdotto dalla Review v1. Tutti i promemoria pertinenti CAP-07 (M-2 OPEN, M-16 OPEN-CONDIZIONALE) sono trattati come da decisioni di scope.

I carryover esistenti che restano attivi:

- **M-2 OPEN**: invariato (verifica empirica L_max=30s in Appendice E -- non risolta in Parte VII per decisione di scope (a)).
- **M-16 OPEN-CONDIZIONALE**: chiuso condizionalmente in Cap.31.3 -- l'esito (attivazione/non-attivazione) dipende dal run empirico; il bundle frozen registra cox_time_varying_active. Per la chiusura del cycle, lo stato di M-16 diventa **CLOSED-CAP-07 con condizione** (il prossimo Planner del ciclo successivo riapplichera il monitoraggio Schoenfeld nel nuovo run; se cox_time_varying_active=True nel bundle corrente, applichera Cox time-varying coefficients).

I carryover esplicitati in Cap.31.5 (riconsiderazione theta_CV + K_max_strict) sono direzioni metodologiche per il ciclo successivo, non promemoria attivi.

Il carryover esplicitato in Cap.36.3 (10 parametri di tuning operativo Parte VI a 3-6 mesi post-go-live) e attivita di monitoring post-go-live, non promemoria attivo Parte VII.

---

## Sintesi finale

**Verdetto: CONDITIONAL.**

**Conteggio finding**:
- 0 BUG REALI bloccanti (FAIL)
- 1 BUG REALE non bloccante (contraddizione interna Cap.33.4 vs Cap.34.4 sulla frazione PBO del compute budget; viola AC-33-4 alla lettera ma non impatta GA)
- 2 MIGLIORA PERFORMANCE (errore unita c5.4xlarge spot + errore bibliografico Notices AMS)
- 2 NEUTRO (esempio Cap.33.5 opaco + |f_5| ridondante)

**Eredita verificate**: 32/32 OK.
**M-promemoria verificati**: 2/2 OK.
**Decisioni di scope verificate**: 5/5 OK.
**Citazioni bibliografiche**: 10/11 OK + 1 errore minore (Notices AMS year).
**Aritmetica compute stress test**: tutta numericamente coerente.
**Vincolo solo emissione**: rispettato.
**Tick FIB 5 pt**: rispettato.
**Numeri inventati**: nessuno.
**AC totali**: 63 OK + 1 PARZIALE (AC-33-4) / 64 totali.

**Raccomandazione operativa**: il documento e sostanzialmente solido. L'unico finding **BUG REALE** (la contraddizione Cap.33.4) e una correzione testuale minima (riformulare il paragrafo "Frazione del compute budget" di Cap.33.4 finale per ammettere il range 1%-10% a seconda di S). I 2 finding **MIGLIORA PERFORMANCE** sono errori di consegna documentale che non impattano il GA. I 2 **NEUTRO** sono cosmetici.

Il Developer dovrebbe iterare per chiudere il BUG REALE; la decisione sui MIGLIORA PERFORMANCE spetta al supervisore.
