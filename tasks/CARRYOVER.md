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
| M-2  | Review v1 CAP-02 | Verifica empirica latenza Telegram ($L_{max}=30$s) | Appendice E | OPEN — requisito incardinato come **NFR-6.2** `[B-1 PROVVISORIO]` in SPEC-FUNZ-01 v2 (`ab7450f`, 2026-06-14; era NFR-1 nella v1 `a16a4c0`); **ri-incardinato nel blocco B4 (ricostruzione cieca) come `B4-NFR-03/04`** (vincolo $L\le L_{max}$ + valore 30s **provvisorio dal CAP**, Cap.9.3) alla chiusura B4 PASS `8500159` (2026-06-16); **richiamato anche in B7 come `B7-NFR-03`** (latenza qualitativa $L_{max}=30$s del canale Telegram dentro il criterio AC-GO-10, premessa di gate, Cap.36) alla chiusura B7 PASS `37d2166` (2026-06-21); la verifica empirica del valore resta **OPEN** a Appendice E / FASE-D (PENDING-empirico, mai dichiarata verificata — RM-1/AC-G4); **richiamato anche in B8 come dipendenza aperta `B8-R-03`** alla chiusura B8 PASS `09cc7d9` (2026-06-23, blocco di confine), non chiuso. **NON chiuso.** |
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
| M-GOV-1 | GOV-FIX-01 (13/06/2026) | orario FIB fissato a 08:00–22:00 CET (continua) + asta 07:45–08:00 con etichetta decisione-AC + WIKI-HINT Borsa Italiana; upgrade a PROVA-EMPIRICA (primo/ultimo trade da tape DAPI) al primo probe CAP-DATA (V-1). | CAP-DATA-01 / probe V-1 | APERTO — requisito incardinato come **R-7.1** `[B-2 PROVVISORIO]` in SPEC-FUNZ-01 v2 (`ab7450f`, 2026-06-14); **ri-incardinato nel blocco B5 (ricostruzione cieca) come `B5-R-11`** (finestra 08:00-22:00 CET) alla chiusura B5 PASS `5ec899c` (2026-06-17); la verifica empirica (primo/ultimo trade da tape DAPI + convenzione calendario/giorni-di-trading) resta **OPEN**: probe V-1 (tape DAPI) / V-2 (calendario IDEM); **richiamato anche in B8 come dipendenza aperta** alla chiusura B8 PASS `09cc7d9` (2026-06-23). **NON chiuso** (PENDING-empirico, RM-1) |
| M-GOV-2 | SPEC-FUNZ-01-PROMOTE (14/06/2026) | SPEC-FUNZ-01 ricostruita ex-novo (v2, Developer cieco) e promossa; v1 archiviata (tag `spec-funz-01-v1-storico` + `_v1_storico` committate). 2 decisioni AC dal diff di copertura: CN-3 "non è consulenza" scartata; KPI lifecycle enumerati (NFR-8.9/8.10/8.11). | — (chiusura slot SPEC-FUNZ-01) | CHIUSO |

### Eredità chiusura SPEC-FUNZ-01-B6 (Schema-dato DAPI & continuità tape) — `a5cfa80`, 2026-06-18

Alla chiusura PASS di B6 (territorio incidente CANDLE, cautela RM massima):

- **Schemi-dato DAPI consolidati in B6**: **M-1 (CANDLE `C;L;H;O;V`) / M-9 (PRICE `f8`/`f9`/`f6`) / M-10 (BOOK_5 `[BID×5][ASK×5]`, 290/290)** — registro tecnico in `STATO_CORRENTE §5` — sono stati **consolidati nella spec come requisiti B6 di schema-dato** (`SPEC_FUNZ_01_B6.md`), ciascuno col **diff col decoder canonico** (`export_directa_history_parametric.py` / `probe_dapi.py`) e permutazioni alternative escluse (RM-1). Restano riferimento **PROVA-EMPIRICA** (audit CAP-DATA-02), **non riaperti**. **RACC-METODO-2 onorata** (vedi sotto).
- **5 PENDING-empirico instradati a probe (task empirico separato / FASE-D — NON bloccanti per la spec, NON asseribili come verificati)**:
  1. **Codici mese Mar/Dic** Directa-IDEM (oltre `F`=giu/`I`=set certificati) — decodifica via ANAG a mercato aperto quando i contratti sono listati (cfr. M-4 STATO §5, Cap.55).
  2. **Ticker `1030`** realtime non sottoscritto — IDEM nel servizio base, PHASE-2 gated (cfr. M-3 STATO §5).
  3. **Riavvio Darwin a mezzanotte** (Gap-3) — comportamento notturno, continuità del tape.
  4. **PRICE `f5`/`f7`** contatori cumulativi — non disambiguati (verifica parziale).
  5. **Base calendario-vs-giorni-di-trading** delle finestre warm-up 30gg / recupero 100gg — convenzione IDEM (**probe V-2**). Nota: il valore `L_warmup=30` è **congelato**; è la resa in giorni-di-calendario che è pending.
- **Finding #3 NEUTRO** (B6-R-28/R-31 borderline N1): non instradato (decisione AC), restano proposizioni unitarie verificabili.

### Eredità chiusura SPEC-FUNZ-01-B7 (Gate di go-live) — `37d2166`, 2026-06-21

Alla chiusura PASS di B7 (settimo blocco della ricostruzione cieca a 8 blocchi; ponte verso FASE-D; **cardine edge-PENDING**):

- **Nessun M nuovo emesso da B7.** L'unico M pertinente è **M-2** (latenza Telegram), già OPEN: richiamato in B7 come **B7-NFR-03** dentro il criterio AC-GO-10 (premessa qualitativa di gate), misura empirica resta **PENDING-empirico** (mai asserita — RM-1). Vedi riga M-2 sopra. **M-16 condizionale** (Cox time-varying) è materia metodologica già **CLOSED-CAP-07** (Cap.31.3), non riaperto da B7.
- **Cardine edge-PENDING** (vincolo cardine di B7): B7 consolida i **criteri di gate dichiarati** (DSR/PBO/bootstrap/$E[R_{net}]$/CVaR/MDD/12 AC-GO/frozen bundle/decisione GO-NO-GO) come **definizioni/soglie/procedure**, **MAI** come esiti. **Tutte le claim sull'esistenza/misura dell'edge restano PENDING-empirico**, esclusiva del ruolo **`validator`** (in panchina fino a FASE-D). Verificato dal Reviewer: 0 asserzioni d'esito, 30 marcature PENDING, confine di ruolo `validator` esplicito.
- **Soglie tutte provvisorie**: $\theta_{DSR}=0{,}95$, $\theta_{PBO}=0{,}50$, $\theta_{f_5}=0{,}30$, $\theta_{IQR}=0{,}40$, $\theta_{t_2}=0{,}30$, $\theta_{CVaR}=-100$ pt, $\theta_{MDD}=200$ pt, $\theta_{sessions}=0{,}60$, $L_{avg}=10$, $\theta_{cost}=100$ USD/run, $B=2.000$ — consolidate come "valore di lavoro provvisorio, non congelato in Parte VII, riconsiderato post-go-live" (PENDING / FASE-D, NON definitive).

### Eredità chiusura SPEC-FUNZ-01-B8 (Confine / chiusura della spec) — `09cc7d9`, 2026-06-23

Alla chiusura PASS di B8 (**ottavo e ULTIMO blocco**; chiude la copertura della spec a 75/75 req-v2):

- **Nessun M nuovo emesso da B8.** Blocco di confine/chiusura: **M-2** (latenza Telegram, OPEN) e **M-GOV-1** (orario sessione, APERTO) sono **richiamati come dipendenze aperte dichiarate** verso FASE-D (B8-R-03 / nota M-GOV-1 in Sez.3), **NON chiusi** (restano OPEN/APERTO, PENDING-empirico, mai asseriti — RM-1). Nessun M esistente incardinato o chiuso da B8.
- **Cardine confine ereditato da B7**: l'edge (DSR/PBO/OOS/valori d'esito) resta **PENDING-empirico (validator/FASE-D)**; B8 lo cita come dipendenza aperta (B8-R-06), **mai asserito**. Verificato dal Reviewer (`09cc7d9`): 0 aperture di materia nuova, 0 risoluzioni di dipendenze, 0 requisiti di assemblaggio/indicizzazione/avvio-FASE-D.
- **SERIE B1..B8 COMPLETA — 75/75 req-v2 coperti** (B1=9, B2=12, B3=6, B4=14, B5=11, B6=9, B7=11, B8=3). Le **10 dipendenze aperte** enumerate da B8 (latenza Telegram, θ_reconcile, 10 param tuning post-go-live, run validator sull'edge, lookup codici mese IDEM, abilitazione FDAX standard, vendor cross-index pluriennale, flusso DAPI come training, migrazione formato legacy→esteso, implementazione codice pipeline) costituiscono il **debito dichiarato verso FASE-D / post-go-live**, tutte **OPEN/PENDING** — dichiarate, mai risolte.
- **Nota di processo**: card-sorgente + ESITO B8 committati in `3136a55` con `[RM-HOOK-OVERRIDE]` **autorizzato da AC** (override out-of-band rispetto alla sessione CLI; flaggato dall'Orchestratore e ratificato — disciplina: ogni override va sempre flaggato ad AC, mai assunto come fabbricazione).

## RACCOMANDAZIONI-METODO (namespace separato dai M-promemoria di capitolo)

Registro delle raccomandazioni di processo emerse dalle Review di audit non-CAP (es. FONDAMENTA-XX). NON sono M-promemoria di capitolo. Non vincolano un CAP successivo: sono debito di manutenzione metodologica che il supervisore valuta quando opportuno.

**Formato riga**: `| RACC-ID | origine | contenuto | stato |`

| RACC-ID | Origine | Contenuto | Stato |
|---------|---------|-----------|-------|
| RACC-METODO-1 | Re-Review v3 FONDAMENTA-01 (`58cf81f`) | Permangono rimandi numerici **pre-esistenti** verso `.claude/agents/reviewer.md` e `tasks/METODO.md` (es. `→ METODO.md:28-33`, `→ reviewer.md:163-164`) che oggi risolvono correttamente ma sono soggetti allo stesso churn di riga che ha generato N1/N2/N3. Raccomandazione: de-numerizzare i rimandi residui convertendoli in àncore di sezione (come fatto nel rework v3 per `CLAUDE.md`/`developer.md`). Non bloccante, fuori scope FONDAMENTA-01. | OPEN |
| RACC-METODO-2 | Re-Review v2 CAP-DATA-02 RM-RETRO (`20961f4`), finding #8 | Quando una Review/AC dichiara "OK" sulla correttezza di uno **schema-dato di un sistema esterno** (DAPI, Telegram, vendor), la verifica deve includere il **confronto puntuale col decoder di produzione esistente** (RM-2), non la sola completezza strutturale dei campi. Lo schema CANDLE invertito `O;H;L;C` di Cap.49 (CAP-DATA-02) era **completo su tutti i campi** ma con mapping OHLC sbagliato, ed è sfuggito al ciclo Review v1→v2 (AC verificavano completezza, non correttezza-vs-decoder). Raccomandazione: i criteri di accettazione per schemi esterni richiedano esplicitamente il diff col decoder canonico. Non bloccante, fuori scope CAP-DATA-02. | OPEN — onorata in CAP-DATA-03 (Review v1 `ab80d96` + v2 `48171e4`, sede CLI): il Reviewer ha verificato le citazioni di schema del capitolo contro il decoder canonico `export_directa_history_parametric.py:467-481`/`:605-617` (RM-2), incluso il diff legacy-11-campi vs esteso-13-campi e la correzione `:605-617` vs `:119-122`. Resta raccomandazione di processo *standing*. **Ulteriormente onorata in SPEC-FUNZ-01-B6 (chiusura PASS `a5cfa80`, 2026-06-18)**: la card B6 ha imposto come AC il diff col decoder canonico per ogni claim di schema (CANDLE/PRICE/BOOK_5); il Reviewer ha verificato l'onestà del diff (PRICE/BOOK_5 ancorati a PROVA-EMPIRICA dove i decoder non parsano i campi, non spacciati come "da decoder"). |

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
