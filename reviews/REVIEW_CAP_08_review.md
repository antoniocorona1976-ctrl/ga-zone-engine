# Review CAP-DATA-01 (Parte 8) - Convenzione dati storici e politica di rollover

**Verdetto**: CONDITIONAL

**Iterazione**: v1 (prima review del ciclo)
**Data**: 2026-05-27
**Reviewer**: Subagente reviewer (Claude Code)
**HEAD origin/main auditato**: 17240b4 ([DEV] CAP-DATA-01 v1)

**File auditati**:
- docs/methodology_v2/CAP_08_parte_8.md (237 righe)
- reports/REPORT_CAP_08.md (237 righe)
- data/sessions/fib_session_calendar.csv (1 header + 5 dati = 6 righe)
- data/sessions/README.md (58 righe)
- docs/methodology_v2/00_indice.md (riga 64-73 - Parte 8 in coda)

**Eccezione normativa applicata**: cross-index in Cap.42 NON e classificato come BUG REALE bloccante, ratificata dal supervisore in tasks/SESSION_HANDOFF_CAP-07_to_CAP-DATA-01.md sezione 4 decisione (1). Il Reviewer ha verificato che il Cap.42 e scritto in modo strettamente dichiarativo (no formule DCC implementate, fasizzazione PHASE-1/PHASE-2 esplicita, Realized GARCH + S_xidx + quinta famiglia catalogo target citati come estensioni future esplicite - righe 176-182). Nessuna citazione cross-index al di FUORI di Cap.42 e stata trovata nel doc Parte 8.

---

## Riepilogo verifica Acceptance Criteria 3.1-3.8

| AC | Criterio | Esito | Evidenza |
|----|----------|-------|----------|
| AC-3.1 | Scelta serie ufficiale FIB pieno back-adjusted Portara/CQG; razionale equivalenza FIB/miniFIB; esclusione MIB cash ancorata a research = runtime | OK | CAP_08_parte_8.md:11-22 (Cap.37) - esclusione MIB cash motivata via 4 differenze (orari, microstruttura, basis, gap apertura) con ancoraggio Parte I Cap.1 |
| AC-3.2 | Tre serie derivabili (ratio-adjusted, Panama-additive, unadjusted concatenata); formule esplicite; ricostruzione preprocessing | OK con osservazione | CAP_08_parte_8.md:25-51 (Cap.38) - formula ratio-adjusted ben definita, tre uses normativi distinti. Vedi N-1 sotto |
| AC-3.3 | Filtro pre-expiry N=3; algoritmo formale; training/outer valid ma NON outer test | OK | CAP_08_parte_8.md:55-69 (Cap.39) - algoritmo esplicito; esclusione fold OOS finale Parte VII Cap.31.1 motivata via Lopez de Prado 2018 Cap.7 |
| AC-3.4 | Preprocessor griglia 1-min; forward-fill OHLC=Close_(t-1), Volume=0, TickCount=0, flag bar_synthetic; uso differenziato; nessun touch su bar_synthetic; flag persistito nel bundle frozen | OK | CAP_08_parte_8.md:73-103 (Cap.40) - formula completa, regola di uso per 4 famiglie feature (prezzo, volume, volatilita, struttura) coerente con Parte III Cap.15.2 |
| AC-3.5 | Timeline ufficiale sessioni FIB E1-E5; tabella; CSV 6 campi; CET con conversione automatica CEST | OK | CAP_08_parte_8.md:107-137 (Cap.41) + data/sessions/fib_session_calendar.csv:1-6 + data/sessions/README.md - dati esattamente coerenti con ACTIVE_TASK.md (5 epoche E1-E5, date 1994-11-28 a 2026-05-27, orari per epoca, timezone CET) |
| AC-3.6 | Convenzione cross-index PHASE-2; timestamp intersezione; fasizzazione PHASE-1 con costi noti; DICHIARAZIONE NORMATIVA SENZA implementazione | OK | CAP_08_parte_8.md:141-182 (Cap.42) - dichiarazione PHASE-2 esplicita (r143-145); 4 cost PHASE-1 elencati. Realized GARCH + DCC/ADCC/cDCC + S_xidx + quinta famiglia catalogo target tutti citati come estensioni future esplicite (r176-182). Eccezione normativa supervisore (decisione (1)) rispettata. NESSUN BUG REALE bloccante |
| AC-3.7 | Sanity validation: finestra 18-24 mesi; ratio-adjusted vs unadjusted-stitched; metriche; 3 sigma bootstrap; out-of-scope implementazione | OK con riserva | CAP_08_parte_8.md:186-209 (Cap.43) - procedura completa. Vedi B-1 e M-1 sotto |
| AC-3.8 | Esclusione fonti alternative: MIB cash, vendor non-Portara/CQG, mix vendor cross-index, CFD broker, dati intraday liberi | OK | CAP_08_parte_8.md:213-237 (Cap.44) - 5 esclusioni esplicite con razionale per ciascuna |

## Riepilogo verifica Definition of Done sezione 5

| AC-DoD | Criterio | Esito | Evidenza |
|--------|----------|-------|----------|
| AC-DoD-1 | File CAP_08_parte_8.md creato e completo (naming beta2) | OK | 237 righe, naming beta2 corretto, 8 capitoli Cap.37-44 in mappatura 1:1 con AC |
| AC-DoD-2 | File fib_session_calendar.csv creato con tabella sessioni dalla sezione Dati di input recuperati dall Orchestratore | OK | 6 righe (1 header + 5 dati), schema 6 campi conforme task card 3.5, dati identici a ACTIVE_TASK.md |
| AC-DoD-3 | File data/sessions/README.md creato con note non normative su fonti, URL, ambiguita | OK | 58 righe, marcature DATA DA VERIFICARE per E1/E2 preservate. CSV pulito (direttiva S1 rispettata) |
| AC-DoD-4 | 00_indice.md aggiornato: Parte 8 in coda; stato IN REVIEW; nessuna rinumerazione | OK | Riga 64 Parte 8 IN REVIEW (v1 Developer 2026-05-27); inserita DOPO Parte VII (r55) e PRIMA di Appendici operative (r75); Parti I-VII invariate |
| AC-DoD-5 | Riferimenti incrociati a Parti I-VII verificati e citati con il numero di Parte definitivo | OK | Mappatura Planner applicata verbatim: Cap.37 a Parte I Cap.1,2,5; Cap.38 a Parte III Cap.12,13, Parte IV Cap.19, Parte VII Cap.31.1; Cap.39 a Parte V Cap.25.1, Parte VII Cap.31.1; Cap.40 a Parte II Cap.7,10, Parte III Cap.12,13,14,15, Parte VII Cap.35; Cap.41 a Parte I Cap.1, Parte II Cap.7; Cap.42 a preambolo 00_indice.md, Parte III Cap.13,15.2; Cap.43 a Parte III Cap.12,13.4, Parte VII Cap.34; Cap.44 a Parte I Cap.1,3. Tutti verificati contro 00_indice.md stato 2026-05-27 |
| AC-DoD-6 | REPORT_CAP_08.md generato secondo template supervisore (5+ sezioni) con rollback criteria per ciascuna decisione | OK | 237 righe. Sezioni: Cosa e stato prodotto, Ipotesi di partenza, Decisioni rilevanti (D1-D8), Misura prima/dopo, Verifica esplicita AC (16/16 OK), Domande aperte (0), Criterio di rollback per ciascuna delle 8 decisioni 3.1-3.8, Riepilogo Orchestratore |
| AC-DoD-7 | DEV_STATUS.md aggiornato a READY_FOR_REVIEW | OK | File contiene READY_FOR_REVIEW |
| AC-DoD-8 | Commit + push diretto a origin/main (decisione (a) ratificata) | OK | HEAD 17240b4 su origin/main |

**Risultato AC**: 16/16 OK formalmente. Tre rilievi non strutturali registrati sotto.

---

## Verifica eredita I-VII applicata correttamente

La mappatura Planner ACTIVE_TASK.md sezione Mappatura eredita I-VII a 3.X e stata applicata letteralmente dal Developer. Verifica puntuale dei capitoli citati:

| Cap. doc Parte 8 | Riferimenti Planner | Verifica esecuzione | Esito |
|------------------|---------------------|---------------------|-------|
| Cap.37 | Parte I Cap.1, 2, 5 | Cita Parte I Cap.1 (research=runtime r19), Cap.2 (moltiplicatore 5 EUR/punto vs 1 EUR/punto miniFIB r15), Cap.5 (definizione operativa successo r21) | OK |
| Cap.38 | Parte III Cap.12, 13; Parte IV Cap.19; Parte VII Cap.31.1 | Cita Parte III Cap.12 (rendimenti log), Cap.13 (calibrazione MLE EGARCH W=210.000 r45), Parte IV Cap.19 (survival Cox consumer indiretto r45), Parte VII Cap.31.1 (fonte canonica metriche replay bit-exact r51) | OK |
| Cap.39 | Parte V Cap.25.1; Parte VII Cap.31.1 | Cita Parte V Cap.25.1 (schema walk-forward W_in, P_purge, W_oos, P_emb r67) e Parte VII Cap.31.1 (esclusione fold OOS finale r67), con eredita Lopez de Prado 2018 Cap.7 | OK |
| Cap.40 | Parte II Cap.7.3, Cap.10; Parte III Cap.12.4, 13, 14.2, 15.2; Parte VII Cap.35 | Cita Parte II Cap.7.3 (raw touch r96), Cap.10 (replay bit-exact r94); Parte III Cap.12.4 (carryover N-6 CAP-02 fill virtuale r86), Cap.13.3 (calibrazione MLE EGARCH r90), Cap.14.2 (media di sessione r90), Cap.15.2 (catalogo 37 feature r98), Cap.15.3 (pivot frattali r103); Parte VII Cap.35 (bundle frozen r94) | OK |
| Cap.41 | Parte I Cap.1; Parte II Cap.7 (Q-01) | Cita Parte I Cap.1 (sessione 8:00-22:00 CET r131, r133), Parte II Cap.7 (Q-01 chiusa sessione continua r125, r129) | OK |
| Cap.42 | preambolo 00_indice.md; Parte III Cap.13, 15.2 | Cita preambolo 00_indice.md (r145 rimozione dei layer multi-indice), Parte III Cap.13 (sigma_local proxy di sigma_sys r170), Cap.15.2 (catalogo 37 feature privo canali cross-index r170) | OK |
| Cap.43 | Parte III Cap.12, 13.4; Parte VII Cap.34 | Cita Parte III Cap.12 (definizione rendimenti log 1/5/60-min r194, r205), Cap.13.4 (diagnostica residui EGARCH Ljung-Box, ARCH-LM r206); Parte VII Cap.34 (bootstrap stazionario Politis-Romano 1994, B=2.000 r199, r207). Vedi M-1 sotto su precisione di eredita L_avg | OK con osservazione |
| Cap.44 | Parte I Cap.1, 3 | Cita Parte I Cap.1 (research = runtime per esclusione MIB cash r219), Cap.3 (Portara/CQG come fonte ufficiale r221) | OK |

**Risultato eredita**: tutti i riferimenti incrociati Planner sono stati applicati letteralmente. Nessuna citazione di Parti/Capitoli inesistenti. Nessun riferimento mancante.

---

## Problemi bloccanti (causano FAIL)

**Nessuno**.

Il Reviewer ha verificato:
- Nessuna citazione cross-index al di FUORI di Cap.42 (Cap.40 preprocessor griglia 1-min e altre sezioni non legate a fasizzazione PHASE-2 sono pulite - confermato via Grep su DCC, ADCC, BEKK, cross-index).
- Nessuna violazione di invarianti del documento metodologico v2 (research=runtime, gap semantics, walk-forward purge/embargo, replay bit-exact tutti rispettati).
- Nessun leakage temporale (causalita F_(t-1) esplicitamente dichiarata in Cap.40 r92).
- Specializzazione FIB N=1 preservata (Cap.42 dichiarazione PHASE-2 senza implementazione, eccezione supervisore applicata).
- Naming beta2 corretto su tutti i file e identifier interno.
- Indice 00_indice.md aggiornato senza rinumerazione di Parti I-VII.

## Problemi non bloccanti (causano CONDITIONAL)

### B-1 (BUG REALE non bloccante) - Incoerenza aritmetica sei rolls per anno in Cap.43

**Citazione esatta** (CAP_08_parte_8.md:190):

> il numero di roll e sufficiente (sei rolls per anno sul FIB con scadenze trimestrali, dodici-quattordici roll nella finestra di 18-24 mesi) per consentire un confronto statistico significativo fra le due serie.

**Problema**: con scadenze trimestrali (marzo/giugno/settembre/dicembre - convenzione standard FIB su IDEM) il numero di rolls per anno e 4, non 6. Per coerenza con dodici-quattordici roll nella finestra di 18-24 mesi servirebbero ~7-8 rolls/anno (cioe scadenze bimestrali, che il FIB non ha) o scadenze mensili (12 rolls/anno -> 18-24 rolls in 18-24 mesi).

L affermazione e internamente incoerente: o 4 rolls/anno (trimestrali) -> 6-8 rolls in 18-24 mesi; oppure 12 rolls/anno (mensili) -> 18-24 rolls in 18-24 mesi. Il valore sei rolls/anno + dodici-quattordici roll in 18-24 mesi non torna sotto nessuna convenzione realistica.

**Impatto GA**: nullo nel doc v2 corrente. Cap.43 dichiara esplicitamente l implementazione out-of-scope (FASE-D del roadmap) (r209). Il numero esatto di rolls e usato solo come giustificazione retorica della scelta della finestra 18-24 mesi (sufficiente significativita statistica), che resta valida anche con 6-8 rolls invece di 12-14. Non altera ranking dei cromosomi, fitness, conversione signal-to-trade.

**Classificazione**: BUG REALE non bloccante (incoerenza aritmetica formale in documento normativo, impatto operativo nullo).

## Osservazioni minori

### M-1 (MIGLIORA PERFORMANCE) - Eredita L_avg Cap.43 da Cap.34.2 imprecisa

**Citazione esatta** (CAP_08_parte_8.md:199):

> L intervallo di confidenza bootstrap e calcolato con bootstrap stazionario (Politis e Romano 1994) con B = 2.000 replicazioni, in coerenza con il protocollo bootstrap normativo del doc v2 (Parte VII, Capitolo 34). La block length media L_avg del bootstrap stazionario e quella calibrata su dati FIB in Parte VII Capitolo 34.2; in mancanza di calibrazione operativa, il sanity check utilizza L_avg pari al valore di default congelato in Parte VII (vedi Capitolo 34.2 per il valore corrente).

**Problema**: Parte VII Cap.34.2 calibra L_avg via Politis-White (2004) sui rendimenti dei segnali eseguiti della finestra OOS aggregata (ordine di grandezza L_avg in [5, 20] segnali, valore di lavoro L_avg = 10 segnali). La block length e in unita di segnali, non di minuti. Il Cap.43 invece bootstrappa metriche su rendimenti 1-min della serie ratio-adjusted vs unadjusted-stitched (autocorrelazione lag 1, 5, 30 di rendimenti 1-min; sigma giornaliera realized; quantili di rendimenti log 1/5/60-min). Per un bootstrap di rendimenti 1-min, L_avg dovrebbe essere calibrata via Politis-White sui rendimenti 1-min stessi (verosimilmente L_avg molto piu grande, in unita di minuti, di ordine 10-60+ minuti dato che l autocorrelazione dei rendimenti 1-min sul FIB ha tipicamente struttura intraday).

L affermazione il sanity check utilizza L_avg pari al valore di default congelato in Parte VII e metodologicamente impropria: il default L_avg=10 di Parte VII e calibrato su unita diverse (segnali eseguiti) e non e direttamente applicabile al bootstrap di Cap.43.

**Impatto GA**: nullo nel doc v2 corrente. Cap.43 dichiara l implementazione out-of-scope (FASE-D del roadmap) (r209), quindi nessun bootstrap viene effettivamente eseguito con quel valore nel doc v2. Tuttavia, la regola metodologica come scritta produrrebbe risultati errati se applicata letteralmente in FASE-D.

**Classificazione**: MIGLIORA PERFORMANCE (chiarezza metodologica). Il Developer dovrebbe specificare che L_avg per il bootstrap di Cap.43 va calibrato indipendentemente via Politis-White sui rendimenti 1-min (non eredita diretta dal default L_avg=10 di Cap.34.2), oppure dichiarare il parametro come valore di lavoro non congelato senza eredita specifica.

### N-1 (NEUTRO) - Descrizione testuale rendimento nullo alla barra del roll in Cap.38 r39

**Citazione esatta** (CAP_08_parte_8.md:39):

> Alla barra esatta del roll il rendimento log della serie ratio-adjusted e nullo per convenzione: il roll non genera un rendimento osservabile sulla serie continua, dato che il salto e assorbito dal fattore rho_k.

**Problema**: la formula matematica della riga 37 (P_t = P_t_unadj per prodotto su k:r_k<t di rho_k) e corretta e produce, alla barra successiva al roll, un rendimento log(P_(t+1)/P_t) che e il rendimento naturale del next-month sulla barra immediatamente successiva al roll (non zero, ma il rendimento naturale di mercato). L affermazione il rendimento log e nullo per convenzione e una semplificazione imprecisa rispetto alla formula matematica:
- A t = r_k il fattore rho_k NON e ancora moltiplicato (perche la formula richiede r_k < t), quindi P_(r_k) = P_(r_k)_unadj per prodotto su j<k di rho_j - dove P_(r_k)_unadj e il prezzo curr-month.
- A t = r_k + 1 il fattore rho_k entra nel prodotto, e P_(r_k+1) = P_(r_k+1,next)_unadj per prodotto su j<=k di rho_j.
- Il rendimento log(P_(r_k+1)/P_(r_k)) si riduce, sotto l ipotesi P_(r_k)_unadj = P_(r_k)_curr, a log(P_(r_k+1,next)_unadj/P_(r_k)_next) - rendimento naturale del next-month, NON nullo.

Inoltre l espressione alla barra esatta del roll e ambigua (a t = r_k o t = r_k+1?).

**Impatto GA**: nullo. La formula matematica del Cap.38 e quella che entra nel preprocessor (i modelli probabilistici a valle vedono solo P_t e r_t = log(P_t/P_(t-1))). La descrizione testuale e commento esplicativo, non vincolo operativo. Non altera comportamento GA.

**Classificazione**: NEUTRO (chiarezza descrittiva, impatto nullo).

---

## Verifica perimetro completo - secondo giro ostile

Il Reviewer ha eseguito un secondo giro ostile mirato a problemi non immediatamente visibili. Risultati:

1. **Causalita F_(t-1)**: esplicitamente dichiarata in Cap.40 r92 sia per feature di prezzo (sulla griglia uniforme completa) sia per feature di volatilita (con esclusione barre sintetiche). Nessun leakage temporale. OK.
2. **Touch su barre sintetiche**: Cap.40 r96 nega esplicitamente la possibilita di touch su bar_synthetic=True. Ragionamento edge case zona contiene gia Close_(t-1) verificato come logicamente corretto (touch sarebbe gia stato dichiarato sulla barra reale precedente). OK.
3. **Coerenza CSV vs ACTIVE_TASK vs Cap.41**: confronto riga per riga delle 5 epoche E1-E5 - tutte le date, orari, timezone identici fra i tre artefatti. OK.
4. **Naming beta2**: file CAP_08_parte_8.md (OK), REPORT_CAP_08.md (OK), identifier Parte 8 arabo (r1, r3, r5 - OK).
5. **M-promemoria**: nessun M attivo pertinente integrato nel doc Parte 8 (confermato dal censimento Planner). M-2 OPEN preservato per Appendice E (verifica empirica L_max=30s Telegram, non chiuso in Parte 8). OK.
6. **Indice**: Parte 8 inserita riga 64 dopo Parte VII (r55) e prima di Appendici (r75). Nessuna rinumerazione I-VII. Stato IN REVIEW (v1 Developer 2026-05-27). OK.
7. **REPORT formato 5+ sezioni**: tutte le sezioni richieste presenti (Cosa e stato prodotto, Ipotesi di partenza, Decisioni rilevanti, Misura prima/dopo, Verifica AC, Domande aperte, Criterio di rollback, Riepilogo Orchestratore). Rollback per ciascuna delle 8 decisioni 3.1-3.8 esplicito. OK.
8. **Cross-index Cap.42 strettamente dichiarativo**: nessuna formula DCC/ADCC/cDCC implementata; fasizzazione PHASE-1/PHASE-2 esplicita (r167-174); Realized GARCH + S_xidx + DCC/ADCC/cDCC + quinta famiglia catalogo target tutti citati come estensioni future esplicite non implementate nel doc v2 corrente (r176-182). Eccezione normativa supervisore applicata. OK.
9. **Tick FIB 5pt**: citato r131. Coerente con memory project_fib_instrument. OK.

---

## Citazioni problematiche dal testo

- il numero di roll e sufficiente (sei rolls per anno sul FIB con scadenze trimestrali, dodici-quattordici roll nella finestra di 18-24 mesi) (CAP_08_parte_8.md:190) - problema: incoerenza aritmetica interna (4 rolls/anno con scadenze trimestrali, non 6; per 12-14 roll in 18-24 mesi servirebbero ~8 rolls/anno) - classificazione: **BUG REALE non bloccante**
- il sanity check utilizza L_avg pari al valore di default congelato in Parte VII (vedi Capitolo 34.2 per il valore corrente) (CAP_08_parte_8.md:199) - problema: L_avg=10 di Cap.34.2 e calibrato su rendimenti per-segnale eseguito; il bootstrap di Cap.43 opera su rendimenti 1-min, unita diverse, necessita ricalibrazione Politis-White sui rendimenti 1-min - classificazione: **MIGLIORA PERFORMANCE**
- Alla barra esatta del roll il rendimento log della serie ratio-adjusted e nullo per convenzione (CAP_08_parte_8.md:39) - problema: descrizione testuale imprecisa rispetto alla formula matematica (rendimento alla barra successiva al roll e il rendimento naturale del next-month, non zero); ambiguita su barra esatta del roll (a r_k o r_k+1?). La formula matematica e corretta. - classificazione: **NEUTRO**

---

## Classificazione per il supervisore

| # | Problema | File:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|------------------------|
| 1 | Incoerenza aritmetica sei rolls/anno con scadenze trimestrali + dodici-quattordici roll in 18-24 mesi | CAP_08_parte_8.md:190 | BUG REALE non bloccante | DECISIONE SUPERVISORE - impatto GA nullo (procedura out-of-scope FASE-D), incoerenza formale in doc normativo |
| 2 | L_avg Cap.43 dichiarata valore di default congelato in Parte VII ma Cap.34.2 calibra su rendimenti per-segnale eseguito (unita diverse) | CAP_08_parte_8.md:199 | MIGLIORA PERFORMANCE | DECISIONE SUPERVISORE - impatto GA nullo nel doc v2 (procedura out-of-scope FASE-D), ma regola metodologica scorretta se applicata letteralmente in FASE-D |
| 3 | Descrizione testuale rendimento nullo alla barra del roll imprecisa rispetto alla formula matematica corretta della riga 37 | CAP_08_parte_8.md:39 | NEUTRO | NO - formula matematica corretta, descrizione testuale e commento esplicativo, impatto GA nullo |

---

## M-promemoria nuovi emessi

**Nessuno**.

Il ciclo Review v1 di CAP-DATA-01 non emette nuovi M-promemoria. M-2 OPEN (verifica empirica L_max=30s Telegram) resta carryover invariato verso Appendice E (Parte 9) come confermato dall handoff CAP-07 -> CAP-DATA-01 sezione 1 e dal censimento Planner ACTIVE_TASK.md sezione Censimento M-promemoria pertinenti.

---

**Verdetto finale**: **CONDITIONAL**

**Razionale del verdetto**:
- Nessun BUG REALE bloccante (16/16 AC OK; eredita I-VII applicate correttamente; eccezione cross-index Cap.42 rispettata; invarianti del doc v2 preservati).
- 1 BUG REALE non bloccante (incoerenza aritmetica Cap.43 r190, impatto GA nullo).
- 1 MIGLIORA PERFORMANCE (eredita L_avg Cap.43 imprecisa, impatto GA nullo).
- 1 NEUTRO (descrizione testuale Cap.38 r39, impatto GA nullo).

Tutti i finding hanno impatto operativo nullo sul GA, sul ranking dei cromosomi, sulla fitness e sulla conversione signal-to-trade. Il documento Parte 8 e strutturalmente solido. Il punto di controllo supervisore (CLAUDE.md) determinera se i finding B-1 e M-1 vanno mandati a Developer per rework v2 o se restano accettati per la chiusura del ciclo. Il finding N-1 NEUTRO non va a Developer per default.
