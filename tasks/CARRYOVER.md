# CARRYOVER — M-promemoria fra capitoli del progetto ga-zone-engine

Questo file e' il **veicolo di handoff** tra sessioni di capitoli diversi. Ogni Review che emette PROMEMORIA / M-promemoria / NEUTRO con rinvio esplicito a una Parte successiva deve essere registrata qui dall'Orchestratore della sessione del capitolo chiuso, come parte della checklist di chiusura (vedi [[feedback-sessione-per-capitolo]] condizione 6).

L'Orchestratore della **nuova** sessione legge questo file come input obbligatorio prima di chiamare il Planner.

**Formato riga**: `| M-ID | origine | contenuto | destinazione | stato |`

- **M-ID**: identificatore univoco (M-1, M-2, ...). Crescente. Non riusato.
- **origine**: `Review vY CAP-XX` (es. `Review v1 CAP-02`).
- **contenuto**: descrizione sintetica del promemoria.
- **destinazione**: capitolo / parte / appendice dove il promemoria va affrontato (es. `Parte V Cap.24`, `Appendice E`).
- **stato**: `OPEN` (da affrontare) / `CLOSED` (gia' affrontato in un capitolo successivo, con riferimento al CAP che lo ha chiuso).

---

## M-promemoria attivi

| M-ID | Origine | Contenuto | Destinazione | Stato |
|------|---------|-----------|--------------|-------|
| M-2  | Review v1 CAP-02 | Verifica empirica latenza Telegram ($L_{max}=30$s) | Appendice E | OPEN |
| M-4  | Review v4 CAP-01 | Tasso di rimpiazzo NSGA-II che giustifica baseline 12.800-25.600 min | Parte V (Cap.23) | CLOSED-CAP-05 (Cap.23.6: formula $N_{eval}^{actual}=P(1+G(1-r_{cache}))=17.408$ con $r_{cache}$ provvisorio 0,15; range M-4 derivato come $17.408 \cdot t_{eval}$ con $t_{eval}\in[0,74;1,47]$ min/cromosoma, post-rework v2 dimensionalmente coerente) |
| M-5  | Review v1 CAP-03 (Q-06 / C-4.3) | Benchmark comparativo rolling vs expanding vs EWMA su FIB con test Inoue-Rossi (2011); criterio di rollback automatico | Parte V (Cap.25 window selection del walk-forward) | CLOSED-CAP-05 (Cap.25.3: 7 candidate windows + test Inoue-Rossi 2011 con $p=0,05$ + tie-break + rollback deterministico normativo) |
| M-6  | Review v1 CAP-03 (Q-09 / C-7.3) | Classificazione di regime in parallelo media e mediana; test di stabilita' con soglia da definire | Parte V (Cap.25-26 gestione regimi nel walk-forward) | CLOSED-CAP-05 (Cap.25.4: formula $\eta_{div}$ + soglia 0,10 + flag instabile) |
| M-1 v2 CAP-03 | Review v2 CAP-03 | Pivot all'inizio e alla fine della sessione non confermabili (conseguenza condizione 4 di Q-08) -- design corretto, va segnalato nel report | Parte VI | CLOSED-CAP-04 (trattato in Cap.16 ancoraggio zona) |
| M-2 v2 CAP-03 | Review v2 CAP-03 | Cadenza ricalibrazione EGARCH in production non specificata | Parte V/VI | CLOSED-CAP-06 completo (Cap.25.9 PV chiude parte V su walk-forward fold-per-fold; residuo Parte VI chiuso post-rework v2 di CAP-06: Cap.27.5 dichiara $T_{recal,\text{EGARCH}}$ come parametro di tuning operativo non congelato + flag di break parametrico $B(t)$ su residui standardizzati EGARCH con citazione bibliografica esplicita (Nyblom 1989 o Engle-Sheppard 2001) + soglia $\theta_B$ + meccanismo trigger anticipato; Cap.30.4 calcola live $B(t)$ con alert su $B(t)>\theta_B$ persistente per $T_{B,\text{persist}}$ barre; finestra recente $W_B$ aggiunta al preambolo come parametro non congelato) |
| M-7  | Review v1 CAP-04 (O-5) | Censoring informativo nel modello Cox cause-specific: verifica del'assunzione (indipendenza censoring/evento) | Parte V (calibrazione/diagnostica survival) | CLOSED-CAP-05 (Cap.25.6: protocollo Cox-Snell 1968 con KS test + Schoenfeld stratificato Grambsch-Therneau 1994 + flag AND logico; esito empirico in Parte VII) |
| M-8  | Developer CAP-04 | Verifica del censoring non-informativo nel survival | Parte V | CLOSED-CAP-05 (Cap.25.6: stesso protocollo di M-7; flag operativo per fold con rollback Fine-Gray in caso di fallimento test) |
| M-9  | Developer CAP-04 | Benchmark Cox cause-specific vs Fine-Gray sub-distribution | Parte V | CLOSED-CAP-05 (Cap.25.7: Brier score binary outcome target_1_hit + Diebold-Mariano 1995 + flag operativo + decisione bundle frozen su rapporto flag positivi/totali in Parte VII) |
| M-10 | Developer CAP-04 | Test Schoenfeld per assunzione hazard proporzionali | Parte V | CLOSED-CAP-05 (Cap.25.8: test $\chi^2$ globale Grambsch-Therneau con soglia $p=0,05$; violazione sistematica >50% fold produce M-promemoria nuovo Parte VII su Cox time-varying coefficients -- vedi M-16 condizionale sotto) |
| M-11 | Developer CAP-04 | Dimensionalita' massima del vettore di feature $\tilde{\mathbf{x}}$ nel survival | Parte V | CLOSED-CAP-05 (Cap.22.6 + Cap.26.7 post-rework v3: $K_{max}=6$ per strato congelato; Harrell 2015 rispettato sotto split 50/50 con $N_{eventi,strato} \geq 60$ nell'**accezione "segnali eseguiti"** allineata fra Cap.25.5 e Cap.26.7 dal rework v3 NB-v3-1; divergenza dichiarata dalla pratica Harrell-strict — sotto la quale $K_{max}^{strict}=4$ — esplicitamente motivata in Cap.26.7) |
| M-12 | Review v1 CAP-04 (O-3) + Developer | Flag `target_2_type` (synthetic/structural) e `stop_type` (structural/personal) — collocazione nel payload formale Cap.6.1 Parte II o solo nel log di emissione | Parte V (revisione payload) o mini-patch CAP-02 | CLOSED-CAP-04 (mini-patch CAP-02 Cap.6.1 Iterazione 4: campi `target_2_type` e `stop_type` aggiunti alla tupla $\mathcal{S}$; Cap.17.4, Cap.18.1, Cap.18.3 di CAP-04 aggiornati con riferimento esplicito ai due campi) |
| M-13 | Review v1 CAP-04 (O-4) + Developer | Catalogo feature: 37 baseline (CAP-03) vs 38 per trade_range con $x^{(A_{range})}$ aggiuntiva — decisione formale | Parte V (cromosoma) | CLOSED-CAP-04 (Cap.21.5 di CAP-04 Iterazione 2: $x^{(A_{range})}$ dichiarata feature condizionale attiva solo in regime trade_range; catalogo globale del cromosoma per regime directional resta a 37 feature, Cap.15.2 di CAP-03 invariato) |
| M-14 | Developer CAP-04 | Stratificazione del Cox per regime calmo/turbolento (interaction term o stratificazione formale) | Parte V | CLOSED-CAP-05 (Cap.25.5: stratificazione formale come default Parte V + rollback automatico a interaction term su $CV(\beta_{j,R})>\theta_{CV}=0,5$ -- $\theta_{CV}$ starting point per primo run, riconsiderato Parte VII) |
| M-15 | Developer CAP-04 | Parametri di classificazione `trade_range` ($A_{range,min}=80$, $N_{osc}$, $n_{osc,min}$, soglie 4 condizioni) congelamento numerico | Parte V | CLOSED-CAP-05 (Cap.26.5/26.6: $A_{range,min}=80$ pt dichiarato non congelabile -- vincolo assoluto Cap.5 PI; $N_{osc}=60$, $n_{osc,min}=2$, $\epsilon_{osc}=5$ pt, $N_{break}=20$, $\delta_{break}=10$ pt come valori congelati di lavoro derivati da default PIV) |
| M-16 condizionale | Review v1 CAP-05 (Cap.25.8 trigger) | Estensione a Cox time-varying coefficients se test Schoenfeld viola sistematicamente in >50% dei fold | Parte VII (calibrazione bundle frozen) | CLOSED-CAP-07 con condizione operativa (Cap.31.3 definisce la regola di decisione: se rapporto fold con `flag_schoenfeld_violation=True` > 0,5, attivazione Cox time-varying coefficients $\boldsymbol{\beta}_j(\tau)$ con riferimento Therneau-Grambsch 2000 nel ciclo successivo di training; altrimenti M-16 chiuso senza attivazione. Decisione registrata come metadato bundle frozen `cox_time_varying_active` $\in$ {True, False} in Cap.35.1 elemento 6. La regola metodologica e' definita in Parte VII; l'attivazione/disattivazione effettiva dipende dall'esito empirico del walk-forward nested di Parte V applicato al primo run. Il prossimo Planner del ciclo successivo di training riapplichera il monitoraggio Schoenfeld nel nuovo run e, se `cox_time_varying_active=True` nel bundle corrente, applichera Cox time-varying coefficients.) |

## RACCOMANDAZIONI-METODO (namespace separato dai M-promemoria di capitolo)

Registro delle raccomandazioni di processo emerse dalle Review di audit non-CAP (es. FONDAMENTA-XX). NON sono M-promemoria di capitolo. Non vincolano un CAP successivo: sono debito di manutenzione metodologica che il supervisore valuta quando opportuno.

**Formato riga**: `| RACC-ID | origine | contenuto | stato |`

| RACC-ID | Origine | Contenuto | Stato |
|---------|---------|-----------|-------|
| RACC-METODO-1 | Re-Review v3 FONDAMENTA-01 (`58cf81f`) | Permangono rimandi numerici **pre-esistenti** verso `.claude/agents/reviewer.md` e `tasks/METODO.md` (es. `→ METODO.md:28-33`, `→ reviewer.md:163-164`) che oggi risolvono correttamente ma sono soggetti allo stesso churn di riga che ha generato N1/N2/N3. Raccomandazione: de-numerizzare i rimandi residui convertendoli in àncore di sezione (come fatto nel rework v3 per `CLAUDE.md`/`developer.md`). Non bloccante, fuori scope FONDAMENTA-01. | OPEN |

---

## Carryover pre-esistenti (storici, non ancora migrati a questo file)

| Origine | Note |
|---------|------|
| Discrepanza 80pt Cap.5 Parte I vs Cap.6.1 Parte II | Review v1 CAP-04 (O-6): pre-esistente. **CHIUSO Iterazione 4 di CAP-02** (mini-patch Cap.6.1 sincronizza la formulazione del filtro trade_range con Cap.5 PI: `$A_{range} = p_{high,range} - p_{low,range} \geq 80$ pt`; allineamento anche in Cap.8.2). Cap.5 di Parte I resta riferimento normativo. |

---

**Convenzioni di update:**
- Quando una nuova Review emette PROMEMORIA / M-promemoria, l'Orchestratore della sessione corrente aggiunge righe alla tabella prima di considerare la sessione chiusa.
- Quando un capitolo successivo chiude un promemoria, lo stato passa a `CLOSED-CAP-YY` con riferimento al capitolo che lo ha chiuso. Mai eliminare la riga: lo storico serve.
- I PROMEMORIA NEUTRO senza impatto sul GA possono essere registrati come `CLOSED-NEUTRO` se il supervisore decide che non vanno mai affrontati.
