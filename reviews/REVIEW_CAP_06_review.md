# Review CAP-06 -- Parte VI (Emissione segnali e lifecycle senza execution)

**Verdetto**: FAIL

**Hash documento auditato**: 8875f1c (commit [DEV] CAP-06 v1 Parte VI READY_FOR_REVIEW)
**File audit**: docs/methodology_v2/CAP_06_parte_VI.md + reports/REPORT_CAP_06.md
**Riferimento normativo**: tasks/ACTIVE_TASK.md (38 AC, 32 ereditá, 3 decisioni di scope)

---

## Sintesi esecutiva

L'audit ostile della Parte VI v1 produce verdetto **FAIL** per la presenza di due BUG REALI bloccanti, accompagnati da diversi errori di referencing e incoerenze minori. Il Developer ha consegnato un documento ampio, ben strutturato e con buona aderenza formale ai 4 capitoli richiesti; la quasi totalita degli AC e' soddisfatta. Tuttavia due problemi compromettono direttamente il comportamento del GA in produzione:

1. **L'ereditá 28 (f_5 stabilita cross-regime) e' completamente omessa in Cap.30**: il Developer ha tracciato live f_1, f_2, f_3, f_4 ma ha dimenticato f_5. L'ereditá 28 lo richiede esplicitamente in Cap.30.3 come metrica a piu bassa frequenza. La conseguenza pratica e' che un bundle ottimizzato per stabilita cross-regime in walk-forward potrebbe degradare la propria stabilita in produzione senza che il motore lo segnali, lasciando invisibile uno dei 5 assi di fitness su cui il NSGA-II ha selezionato il cromosoma.
2. **Cap.29.2 include Delta_t_cromosoma nel messaggio Telegram in violazione esplicita di Cap.9.2 PII** (PASS Review v4 + Iterazione 5 approvata): Cap.9.2 PII al paragrafo 253 dichiara esplicitamente che Delta_t_cromosoma e T_touch_max non figurano nel messaggio all'operatore. Cap.29.2 lo include come voce 7 dell'ordinamento mobile-first con esempio EXP: 60min post-trig, **mentre il paragrafo successivo dello stesso Cap.29.2 dichiara esattamente il contrario** (Delta_t_cromosoma e T_touch_max non figurano nel messaggio Telegram, il layout pubblica le 9 voci dichiarate in Cap.9.2; nient'altro). Il documento e' auto-contraddittorio in modo strutturale. La decisione di scope (c) del Planner (Cap.29 non duplica Cap.9.2 PII, estende il layout) e' violata.

Il punto 2 ha una circostanza attenuante: la decisione di scope (c) del Planner stesso elenca Delta_t_cromosoma e T_touch_max nelle posizioni 5-9 del layout mobile (linea 88 di ACTIVE_TASK.md), creando ambiguita rispetto all'AC-29-1. Il Developer ha seguito parzialmente il Planner (include Delta_t_cromosoma ma esclude T_touch_max) e ha aggiunto la dichiarazione contraddittoria del paragrafo 166. La responsabilita della contraddizione e' del Developer.

Gli altri finding sono problemi non bloccanti (errori di citazione, inconsistenze numeriche formali, ereditá non esplicitate ma implicite) elencati nelle sezioni successive.

---

## Tabella verifica AC v1 (38 AC)

| AC-ID | Esito | Evidenza/Problema |
|-------|-------|-------------------|
| AC-27-1 | OK | Cap.27.1 par. 1: modalita emissione-only + Cap.1 PI + pipeline in locale (i5-7200U/8GB, Cap.3 PI) |
| AC-27-2 | OK | Cap.27.1 lista 1-9: ingest DAPI -> barre -> feature 37 -> EGARCH -> regime -> pivot -> candidate -> AND filters -> Telegram |
| AC-27-3 | PARZIALE | Cap.27.4 dichiara bit-exact identico a Cap.6.1 PII, ma descrive la tupla come esteso a 11 campi ed elenca 12 (BUG REALE #3) |
| AC-27-4 | OK | Cap.27.3: cita Cap.25.1, Cap.26.5 PV; input invariante; seed loggato (Cap.26.8 PV) |
| AC-27-5 | OK | Cap.27.5: (i) T_recal_EGARCH non congelato; (ii) flag B(t) con Nyblom 1989 + Lee-Hansen 1994 + Engle-Sheppard 2001; (iii) theta_B non congelato; (iv) trigger anticipato; (v) separazione 27.5/30.4 |
| AC-27-6 | OK | Citazioni: Cap.6.1 PII, Cap.8 PII, Cap.10 PII, Cap.13 PIII, Cap.14 PIII, Cap.16 PIV, Cap.17-18 PIV, Cap.19-20 PIV, Cap.25-26 PV |
| AC-27-7 | PARZIALE | T_recal_EGARCH, theta_B, T_B_persist non congelati. **W_B = 3 sessioni introdotto in Cap.27.5 ma non figura nella lista del preambolo** (Osservazione #6) |
| AC-28-1 | OK | Cap.28.1: cita Cap.6.3 PII come vincolo normativo gia fissato, estende operativamente |
| AC-28-2 | OK | Cap.28.2: 4 bullet operativi (no Telegram, no marcatura, logging dropped_due_to_active_signal, slot occupato fino a transizione terminale) |
| AC-28-3 | OK con riserva | Cap.28.3: 4 livelli ordinati (p_hit max / directional / Delta_t min / lessicografico signal_id). Riserva: confine livello 1/2 su epsilon_p non esplicito (Osservazione #8) |
| AC-28-4 | OK | Cap.28.4: 5 campi log per ogni candidato; replay bit-exact |
| AC-28-5 | OK | epsilon_p dichiarato non congelato (Cap.28.3 livello 2, Cap.28.4 par. finale) |
| AC-29-1 | **KO** | Cap.29.1 cita Cap.9.2 PII a 9 voci ma Cap.29.2 elenca 9 voci che NON corrispondono a Cap.9.2 PII: include Delta_t_cromosoma, esclude signal_id dalla lista (BUG REALE #2) |
| AC-29-2 | **KO** | Cap.29.2 introduce Delta_t_cromosoma in violazione esplicita di Cap.9.2 PII (BUG REALE #2) |
| AC-29-3 | OK | Cap.29.2: lista 1-9 + esempio formattato; tutti i valori multipli di 5 |
| AC-29-4 | OK | Cap.29.3: signal_id, t_exec, prezzo trigger, Delta_t pre-trigger (Cap.24.5 PV N-4 v2), conferma stato active; esempio numerico presente |
| AC-29-5 | OK | Cap.29.5: signal_id, stato terminale, prezzo, R_gross; esempio numerico presente |
| AC-29-6 | OK | Cap.29.1: cita L_max qualitativo + rinvia ad Appendice E (M-2 OPEN); non risolve numericamente |
| AC-30-1 | PARZIALE | Cap.30.1: 4 metriche live + commissioning c=1 pt. **Citazione fonte errata**: Cap.5 PI invece di Cap.2 PI (Osservazione #5) |
| AC-30-2 | OK | Cap.30.2: IQR [Q1, Q3] cross-fold F=8 + T_drift_persist non congelato (default 5 giorni) |
| AC-30-3 | **KO** | Cap.30.3 traccia pi_t2_t1_live, MFE/MAE, f_stop_t1_live ma **NON menziona f_5 stabilita cross-regime**, che l'ereditá 28 richiede esplicitamente in Cap.30.3 (BUG REALE #1) |
| AC-30-4 | OK | Cap.30.4: calcolo live B(t) + alert theta_B + T_B_persist; cita Cap.27.5 |
| AC-30-5 | OK | Cap.30.5: r_emit_live + alert [E_min, E_max] + T_emit_persist; cita Cap.26.5 PV e Cap.24.2 PV |
| AC-30-6 | OK | Cap.30.6: dashboard lato motore (PC operatore), non sul cellulare; cellulare riceve solo Telegram (Cap.3 PI); no execution-side |
| AC-30-7 | OK | Cap.30.7: non calcola DSR/PBO live; rinvio Parte VII Cap.31-36 esplicito |
| AC-30-8 | OK | W_prod, T_drift_persist, T_B_persist, T_emit_persist non congelati; E_max=5, E_min=0,2, E_exp_max=0,30 ereditate da Cap.26.5 PV |
| AC-T-1 | **KO** | Ereditá 28 (f_5) non citata né calcolata. Ereditá 3 (sessione 8:00-22:00 CET) non esplicitamente citata come finestra operativa (Osservazione #4) |
| AC-T-2 | OK | M-2 v2 CAP-03 residuo trattato (Cap.27.5+Cap.30.4); M-2 OPEN rinvio Appendice E; M-16 OPEN-CONDIZIONALE non integrato |
| AC-T-3 | OK | Nessuna logica execution. fill solo come fill virtuale (citazione Cap.10.4 PII) |
| AC-T-4 | OK | Cap.27.3: non costituisce re-training del GA; Cap.30.2/30.5: alert non chiude loop |
| AC-T-5 | OK | Tutti gli esempi numerici sono multipli di 5 |
| AC-T-6 | PARZIALE | Lista 7 parametri al preambolo. **W_B omesso dalla lista** (Osservazione #6) |
| AC-T-7 | OK | 4 capitoli, ~340 righe non-blank, ~6 pp |
| AC-T-8 | OK | Italiano formale tecnico; nessuna ridondanza vs Parti precedenti |
| AC-T-9 | OK | REPORT_CAP_06.md ha 5 sezioni del formato supervisore + criterio di rollback |
| AC-T-10 | OK | 00_indice.md riporta Parte VI IN REVIEW v1 |
| AC-T-11 | OK | Commit 8875f1c pushato su origin/main |

**Totale AC**: 28 OK, 5 PARZIALE, 5 KO (AC-29-1, AC-29-2, AC-30-3, AC-T-1, AC-27-7/AC-T-6).


---

## Verifica ereditá obbligatoria (32 voci)

| # | Ereditá | Esito | Citazione |
|---|---------|-------|-----------|
| 1 | Solo emissione, no execution (Cap.1 PI) | OK | Cap.27.1 par. 1; Cap.30.6 par. finale |
| 2 | Operatore retail mobile (Cap.2 PI) | OK | Cap.28.2 sez. motivazione operativa; Cap.29.1 par. 1 |
| 3 | Sessione 8:00-22:00 CET (Cap.1 PI) | **KO** | Non citata esplicitamente come finestra operativa. "sessione di trading" usata genericamente in Cap.30; 8:00-22:00 NON dichiarata in Cap.27 né in Cap.30 (Osservazione #4) |
| 4 | Infrastruttura locale i5-7200U/8GB (Cap.3 PI) | OK | Cap.27.1 par. 1 |
| 5 | Broker Directa SIM DAPI (Cap.3 PI) | OK | Cap.27.1 par. 1 (Directa SIM DAPI porta 10001) + blocco 1 |
| 6 | Tick FIB 5 pt (Cap.5 PI) | OK | Cap.27.4 (multipli di 5), Cap.29 esempi |
| 7 | Filtro >=80 pt (Cap.5 PI) | OK | Cap.27.1 blocco 8 ("vincolo assoluto... gia incorporato nei vincoli del bundle frozen") |
| 8 | Commissioni 5 EUR/op (Cap.2 PI) | PARZIALE | Cap.30.1 cita "Cap.5 di Parte I" invece di Cap.2 PI (Osservazione #5). Valore c=1 pt corretto |
| 9 | Telegram unico canale (Cap.3 PI) | OK | Cap.29.1 par. 1; Cap.30.6 |
| 10 | Payload esteso (Cap.6.1 PII Iter.4) | PARZIALE | Cap.27.4 dichiara 11 campi ed elenca 12 (BUG REALE #3) |
| 11 | State machine 6 terminali (Cap.7 PII) | OK | Cap.27.1; Cap.29.5; Cap.30.3 |
| 12 | Vincolo segnale unico attivo (Cap.6.3 PII) | OK | Cap.28.1; Cap.28.3 |
| 13 | Condizioni emissione AND (Cap.8 PII + Cap.20 PIV) | OK | Cap.27.1 blocco 8; Cap.28.2; Cap.28.4 |
| 14 | Telegram 9 voci ordinate (Cap.9.2 PII Iter.5) | **KO** | Cap.29.1-29.2 introducono Delta_t_cromosoma in violazione di Cap.9.2 PII (BUG REALE #2) |
| 15 | Notifica trigger_event separata (Cap.9.5 PII) | OK | Cap.29.3 |
| 16 | Replay deterministico bit-exact (Cap.10 PII) | OK | Cap.27.4 par. finale; Cap.28.4 |
| 17 | Submacchina position lifecycle (Cap.11 PII) | OK | Cap.30.3 (cita Cap.11.2, Cap.11.3, Cap.11.4 PII) |
| 18 | EGARCH(1,1) D AIC/BIC W=210.000 (Cap.13 PIII) | OK | Cap.27.1 blocco 4 + Cap.27.5 (W rolling EGARCH non rivisto runtime) |
| 19 | Regime calmo/turbolento sigma_s, p, N_reg, T_persist (Cap.14 PIII) | OK | Cap.27.1 blocco 5 (parametri esplicitati) |
| 20 | Catalogo 37 feature causali (Cap.15.2 PIII) | OK | Cap.27.1 blocco 3 |
| 21 | Pivot detection (Cap.15.3 PIII) | OK | Cap.27.1 blocco 6 (n_c=3, delta_pivot=10 pt) |
| 22 | p_ref via timestamp pivot (Cap.16.1 PIV) | OK | Cap.27.4 |
| 23 | Target/stop strutturali e sintetici (Cap.17-18 PIV) | OK | Cap.27.4 (Cap.17.4 + Cap.18.1) |
| 24 | Cox cause-specific (Cap.19 PIV) | OK | Cap.27.1 blocco 7; Cap.28.3 livello 1 (Cap.19.5 PIV) |
| 25 | Filtri Cap.20 PIV | OK | Cap.27.1 blocco 8 |
| 26 | Bundle frozen output walk-forward (Cap.25-26 PV) | OK | Cap.27.3 par. 1 (F=8 fold, W_in=105.840, W_oos=52.920, purge=emb=4.200) |
| 27 | Tabella congelati Cap.26.5 PV | OK | Cap.27.3 par. 1 |
| 28 | Fitness M=5 obiettivi (Cap.24.1 PV) | **KO** | f_5 stabilita cross-regime **completamente omessa in Cap.30** (BUG REALE #1) |
| 29 | Metriche tracciate Cap.24.3 PV | OK | Cap.30.3 |
| 30 | Penalita E_max, E_min, E_exp_max (Cap.24.2 PV) | OK | Cap.30.5 sez. "Soglie ereditate" |
| 31 | Seed bundle frozen (Cap.26.8 PV) | OK | Cap.27.3 par. 3; Cap.28.4 |
| 32 | No DSR/PBO live (Cap.24.7 PV) | OK | Cap.30.7 |

**Totale ereditá**: 28 OK, 2 PARZIALE (#8, #10), 3 KO (#3, #14, #28).

---

## Verifica M-promemoria pertinenti

| M-ID | Trattamento richiesto | Esito |
|------|-----------------------|-------|
| M-2 v2 CAP-03 (residuo) | Cap.27.5 meccanismo + Cap.30.4 calcolo live + alert | OK -- chiusura completa (Nyblom 1989 + theta_B + T_B_persist + trigger anticipato) |
| M-2 OPEN | Cap.27.2 + Cap.29.1 citazione qualitativa L_max; rinvio Appendice E | OK -- rinvio esplicito |
| M-16 OPEN-CONDIZIONALE | Nessuna integrazione; Cox stratificato regime preservato in inference | OK -- Cap.27.1 blocco 7 + Cap.27.4 |

Nessun nuovo M-promemoria necessario per le Parti successive.

---

## Verifica decisioni di scope del Planner

| Decisione | Rispettata? |
|-----------|-------------|
| (a) M-2 v2 CAP-03 residuo: Cap.27.5 meccanismo / Cap.30.4 calcolo live + alert | OK |
| (b) Cap.28 estende Cap.6.3 PII operativamente, no modifica normativa | OK |
| (c) Cap.29 non duplica Cap.9.2 PII, estende layout -- nessun campo nuovo | **KO -- Cap.29.2 include Delta_t_cromosoma in violazione di Cap.9.2 PII** |

La decisione di scope (c) e' stata violata strutturalmente. Circostanza attenuante: il Planner stesso (linea 88 ACTIVE_TASK.md) elencava Delta_t_cromosoma e T_touch_max nelle "posizioni 5-9 del layout". Il Developer ha seguito parzialmente il Planner producendo un'auto-contraddizione interna (linea 162 vs linea 166 di Cap.29.2).

---

## Verifica vincoli trasversali

- **No execution layer**: OK -- "execution" solo per dichiarare assenza; "fill" solo come fill virtuale (citazione Cap.10.4 PII)
- **No DSR/PBO live**: OK -- Cap.30.7
- **No re-training GA**: OK -- Cap.27.3, Cap.30.2, Cap.30.5
- **Replay bit-exact**: OK -- Cap.27.4 + Cap.28.4 + Cap.30.1
- **Telegram canale unico**: OK -- Cap.29.1; Cap.30.6
- **Mobile-first**: OK formalmente (375-414 px, monospaziato, no scroll), **ma il messaggio include Delta_t_cromosoma che viola Cap.9.2 PII** (BUG REALE #2)


---

## Problemi bloccanti (causano FAIL)

### BUG REALE #1 -- f_5 stabilita cross-regime omessa in Cap.30

**Sezioni interessate**: Cap.30 (intero capitolo, in particolare Cap.30.3); ereditá 28 di ACTIVE_TASK.md.

**Descrizione**: la fitness multi-obiettivo del NSGA-II di Cap.24.1 di Parte V e' f(theta) = (f_1, f_2, f_3, f_4, f_5) con M=5 obiettivi. L'ereditá 28 di ACTIVE_TASK.md (linea 62) richiede esplicitamente:

> "Cap.30 calcola **live** le contropartite di f_1, f_2, f_3, f_4 su finestra rolling di produzione (Cap.30.2 definira' la finestra) e le confronta con la distribuzione cross-fold del walk-forward; f_5 richiede dati cross-regime aggregati e viene calcolato come metrica a piu' bassa frequenza (Cap.30.3)."

Il documento Cap.30 calcola correttamente f_1_live, f_2_live, f_3_live, f_4_live in Cap.30.1, ma **non menziona mai f_5**. Cap.30.3, che l'ereditá 28 destina esplicitamente a f_5, contiene invece le metriche di lifecycle aggiuntive (pi_t2_t1_live, MFE/MAE, f_stop_t1_live) -- che sono materia di ereditá 29 (Cap.24.3 PV), non di ereditá 28.

Il Developer ha confuso ereditá 28 (parte f_5) ed ereditá 29 (metriche tracciate), allocando l'intera Cap.30.3 alle metriche di lifecycle e omettendo f_5.

**Impatto sul GA**: il NSGA-II ha selezionato il cromosoma frozen tenendo conto di f_5 (stabilita cross-regime, formula esplicita in Cap.24.1 PV linea 262: f_5(theta) = |f_1_calmo(theta) - f_1_turbolento(theta)| / max(|f_1_calmo(theta)|, |f_1_turbolento(theta)|, 1)). Un cromosoma frozen puo' degradare la propria stabilita cross-regime in produzione (es. shock di mercato che modifica la distribuzione dei regimi calmo/turbolento) senza che il motore lo segnali -- un'asse essenziale di deriva del bundle rispetto alla calibrazione walk-forward resta invisibile. La conversione signal-to-trade non e' direttamente compromessa, ma il monitoring della deriva del cromosoma in produzione e' incompleto su uno dei 5 assi di selezione.

**Classificazione**: BUG REALE bloccante.

### BUG REALE #2 -- Cap.29.2 include Delta_t_cromosoma nel messaggio Telegram in violazione esplicita di Cap.9.2 PII

**Sezioni interessate**: Cap.29.1 e Cap.29.2; decisione di scope (c) del Planner; AC-29-1, AC-29-2; ereditá 14.

**Descrizione**: Cap.9.2 PII Iterazione 5 (PASS Review v4 + Iterazione 5 ratificata Review v3 CAP-04 commit a1625df del 2026-05-25) elenca le **9 voci pubblicate ordinate** del messaggio Telegram:
1. signal_id, 2. direction, 3. setup_class, 4. entry_zone, 5. target_1 e target_2, 6. stop_loss, 7. timestamp_emission, 8. target_2_type, 9. stop_type.

Cap.9.2 PII paragrafo 253 dichiara esplicitamente:
> "I campi Delta_t_cromosoma e T_touch_max non figurano nel messaggio all'operatore: sono parametri tecnici del modello rilevanti per il log interno (Cap.10) ma non per la decisione operativa dell'operatore."

Cap.29.2 di CAP-06 elenca un "ordinamento delle 9 voci di Cap.9.2 PII per priorita mobile" che **non corrisponde alle 9 voci di Cap.9.2 PII**:
1. direction, 2. entry_zone, 3. target_1, 4. stop_loss, 5. target_2 con target_2_type, 6. stop_type, **7. Delta_t_cromosoma**, 8. setup_class, 9. timestamp_emission.

signal_id e' messo come "footer compatto" e Delta_t_cromosoma e' introdotto come voce 7 (con esempio numerico EXP: 60min post-trig nell'esempio formattato di Cap.29.2 linea 177).

**Il documento si auto-contraddice nel paragrafo immediatamente successivo** (linea 166 di Cap.29.2):
> "Il campo T_touch_max (gene del cromosoma di Cap.6.1 di Parte II) **non figura nel messaggio Telegram** in coerenza con Cap.9.2 di Parte II (Delta_t_cromosoma e T_touch_max erano dichiarati come parametri tecnici del modello rilevanti per il log interno ma non per la decisione operativa dell'operatore); la sua presenza nel layout di Cap.29.2 sarebbe estensione del contratto di Cap.9.2 e non e' introdotta. Il layout pubblica le 9 voci dichiarate in Cap.9.2; nient'altro."

Quindi Cap.29.2 contemporaneamente:
- (a) lista numerata 1-9 al punto 7: include Delta_t_cromosoma con esempio EXP: 60min post-trig;
- (b) paragrafo successivo: "Delta_t_cromosoma non figurano nel messaggio Telegram... Il layout pubblica le 9 voci dichiarate in Cap.9.2; nient'altro."

Le due affermazioni sono mutuamente esclusive. Il documento non e' auto-coerente.

**Attenzione**: il Planner stesso (linea 88 ACTIVE_TASK.md decisione di scope (c)) ha elencato Delta_t_cromosoma e T_touch_max nelle "posizioni 5-9 del layout":
> "posizioni 5-9 i rimanenti campi (target_2 con tipo, Delta_t_cromosoma, T_touch_max, setup_class, timestamp_emission)"

Il Planner ha quindi creato l'ambiguita rispetto all'AC-29-1. Il Developer poteva risolverla sollevando M-promemoria al Planner, o dichiarando esplicitamente la deviazione dal Planner come decisione architetturale. Ha invece prodotto un documento auto-contraddittorio.

**Impatto sul GA**: il messaggio Telegram pubblicato non corrisponde piu al contratto di Cap.9.2 PII (vincolo PASS Review v4 + Iterazione 5). Un consumer mobile dovrebbe ricevere esattamente quelle 9 voci. Aggiungere Delta_t_cromosoma aggiunge informazione di gestione attiva (timer post-trigger) che Cap.9.2 PII paragrafo 253 dichiara esplicitamente fuori dal messaggio "non per la decisione operativa dell'operatore". L'impatto operativo e' duplice: (i) ereditá 14 violata; (ii) potenziale interferenza con la regola "il messaggio non contiene istruzioni di gestione attiva della posizione" di Cap.9.2 PII paragrafo 253. La conversione signal-to-trade non e' direttamente compromessa, ma il contratto del payload Telegram e' violato e l'invariante "payload formale (immutabile) vs rappresentazione mobile (cosmetica)" dichiarata in Cap.29.1 e' disattesa.

**Classificazione**: BUG REALE bloccante.

---

## Problemi non bloccanti

### BUG REALE #3 -- Cap.27.4 dichiara "11 campi" ma elenca 12

**Sezioni**: Cap.27.4 (linea 49).

**Descrizione**: Cap.27.4 dichiara:
> "Il payload del segnale prodotto dalla pipeline in inference live e' **bit-exact identico al payload formale di Cap.6.1 di Parte II** (Iterazione 4 con S esteso a 11 campi signal_id, timestamp_emission, direction, entry_zone, target_1, target_2, target_2_type, stop_loss, stop_type, setup_class, Delta_t_cromosoma, T_touch_max)."

Il documento dichiara "11 campi" ma elenca 12: signal_id (1), timestamp_emission (2), direction (3), entry_zone (4), target_1 (5), target_2 (6), target_2_type (7), stop_loss (8), stop_type (9), setup_class (10), Delta_t_cromosoma (11), T_touch_max (12).

Il payload di Cap.6.1 PII (linea 19) effettivamente ha 12 campi nella tupla S. Il task ACTIVE_TASK.md (ereditá 10, linea 35) dichiara erroneamente "11 campi" -- l'errore e' ereditato dal Planner, ma il Developer non l'ha corretto.

**Impatto sul GA**: nullo. Il payload effettivamente prodotto e' quello giusto. Errore di conteggio formale.

**Classificazione**: BUG REALE non bloccante.


---

## Osservazioni minori

### #4 -- Ereditá 3 (sessione 8:00-22:00 CET) non citata esplicitamente

**Sezioni**: Cap.27, Cap.30.

**Descrizione**: l'ereditá 3 di ACTIVE_TASK.md (linea 25) richiede:
> "Cap.27 dichiara la finestra di emissione del motore; Cap.30 dichiara la finestra di calcolo delle metriche live coerente con la finestra operativa."

Il documento usa "sessione di trading" e "giornata lavorativa" genericamente ma **non dichiara esplicitamente la finestra 8:00-22:00 CET** ne in Cap.27 ne in Cap.30. La citazione e' implicita (sessione FIB = 840 minuti di trading; W_B = 3 x 840 = 2.520 barre).

**Impatto sul GA**: limitato. In contesto FIB la "sessione di trading" e' inequivoca. Tuttavia il vincolo formale dell'ereditá 3 richiede esplicitazione.

**Classificazione**: NEUTRO (impatto formale).

### #5 -- Cap.30.1 attribuisce commissioning a "Cap.5 di Parte I" invece di Cap.2 PI

**Sezioni**: Cap.30.1 (linea 253).

**Descrizione**: Cap.30.1 dichiara:
> "La definizione di R_net include il commissioning c=1 pt FIB equivalente per operazione (ereditá Cap.5 di Parte I, conversione 5 EUR commissione / 5 EUR per punto FIB)"

L'ereditá 8 di ACTIVE_TASK.md (linea 30) specifica esplicitamente Cap.2 PI come fonte normativa delle commissioni. Cap.5 PI contiene il filtro 80 pt; Cap.2 PI contiene le commissioni 5 EUR/op. Errore di referencing.

**Impatto sul GA**: nullo. Il valore c=1 pt e' quello giusto.

**Classificazione**: NEUTRO.

### #6 -- W_B introdotto in Cap.27.5 ma omesso dalla lista del preambolo

**Sezioni**: Cap.27.5 (linea 71); preambolo Parte VI (linea 7).

**Descrizione**: il preambolo (linea 7) elenca i parametri di tuning operativo non congelati: T_recal_EGARCH, theta_B, T_B_persist, W_prod, T_drift_persist, T_emit_persist, epsilon_p (7 parametri). Cap.27.5 (linea 71) introduce un parametro tecnico aggiuntivo W_B = 3 sessioni (= 2.520 barre 1-min) "non congelato". W_B non figura nella lista del preambolo.

**Impatto sul GA**: nullo. E' un parametro tecnico aggiuntivo non strettamente di "tuning operativo".

**Classificazione**: NEUTRO (inconsistenza minore di completezza).

### #7 -- Cap.10.4 PII citato come fonte di "fill virtuale"

**Sezioni**: Cap.29.5 (linea 227).

**Descrizione**: Cap.29.5 cita "il prezzo di fill virtuale (Cap.10.4 di Parte II)". Cap.10.4 PII e' "Log di chiusura" (contiene la formula R_net derivata dal fill virtuale); la **definizione** di fill virtuale e' in Cap.7.3 PII (linea 141).

**Impatto sul GA**: nullo.

**Classificazione**: NEUTRO.

### #8 -- Tie-break livello 1 vs livello 2: confine epsilon_p non esplicito

**Sezioni**: Cap.28.3 (linee 112-113).

**Descrizione**: livello 1 dice "max" senza menzionare epsilon_p. Livello 2 dice "in caso di tie su p_hit, entro tolleranza numerica epsilon_p". L'interpretazione naturale e' "se |p_hit(S_1) - p_hit(S_2)| > epsilon_p vince il max; se entro epsilon_p, livello 2", ma il documento non lo dichiara esplicitamente.

**Impatto sul GA**: minore. Due implementazioni con convenzioni diverse potrebbero non riprodurre bit-exact lo stesso risultato in floating-point edge case.

**Classificazione**: NEUTRO (ambiguita lieve, replay bit-exact garantito solo con convenzione comune).

### #9 -- timestamp_emission esempi con secondi (Cap.6.1 PII dichiara "minuto chiuso")

**Sezioni**: Cap.29.2 esempio (linea 179), Cap.29.3 esempio (linea 202).

**Descrizione**: gli esempi mostrano "EMIT: 10:42:15 CET" e "TRIG: 11:18:00 CET". Cap.6.1 PII dichiara timestamp_emission "minuto chiuso". Formato HH:MM:SS inconsistente.

**Impatto sul GA**: nullo.

**Classificazione**: NEUTRO (cosmetic).

### #10 -- Cap.30.1 motivazione W_prod fa riferimento improprio a eta_div di Cap.25.4 PV

**Sezioni**: Cap.30.1 (linea 249).

**Descrizione**: Cap.30.1 motiva W_prod = 21 sessioni con "coerente con la persistenza del flag di regime di Cap.25.4 di Parte V (eta_div calcolato su W_prod corrisponde a circa 21 osservazioni di classificazione sessione)". eta_div in Cap.25.4 PV e' una statistica per-fold, non rolling su W_prod. Citazione fuorviante.

**Impatto sul GA**: nullo.

**Classificazione**: NEUTRO.

### #11 -- Esempio numerico tie-break mancante

**Sezioni**: Cap.28.3.

**Descrizione**: il prompt di Review chiede "esempi numerici concreti (es. esempio di tie-break)". Cap.28.3 ha la regola in 4 livelli ben dichiarata ma nessun esempio numerico concreto. L'AC-28-3 non chiede esempio numerico.

**Impatto sul GA**: nullo.

**Classificazione**: NEUTRO.

---

## Citazioni problematiche dal testo

- "(Iterazione 4 con S esteso a 11 campi signal_id, timestamp_emission, direction, entry_zone, target_1, target_2, target_2_type, stop_loss, stop_type, setup_class, Delta_t_cromosoma, T_touch_max)" (Cap.27.4 linea 49) -- problema: dichiara 11 campi ma ne elenca 12; il payload corretto ha 12 campi -- classificazione: **BUG REALE non bloccante** (formale).

- "Le 9 voci pubblicate di Cap.9.2 di Parte II sono riordinate per priorita di lettura mobile" (Cap.29.2 linea 152) **insieme a** "7. Delta_t_cromosoma in minuti di trading, abbreviato come EXP: <N>min post-trig" (Cap.29.2 linea 162) **insieme a** "Delta_t_cromosoma e T_touch_max erano dichiarati come parametri tecnici del modello rilevanti per il log interno ma non per la decisione operativa dell'operatore... Il layout pubblica le 9 voci dichiarate in Cap.9.2; nient'altro." (Cap.29.2 linea 166) -- problema: auto-contraddizione strutturale; include Delta_t_cromosoma in violazione esplicita di Cap.9.2 PII paragrafo 253; viola decisione di scope (c) del Planner -- classificazione: **BUG REALE bloccante**.

- "Tali metriche entrano nella dashboard di Cap.30.6 come tabelle/grafici di reporting, senza soglie di alert." (Cap.30.3 linea 281) -- problema: l'ereditá 28 richiede che f_5 sia tracciato in Cap.30.3 come metrica a piu bassa frequenza; il documento Cap.30.3 si limita a pi_t2_t1_live, MFE/MAE, f_stop_t1_live (ereditá 29) **omettendo f_5** -- classificazione: **BUG REALE bloccante**.

- "il commissioning c=1 pt FIB equivalente per operazione (ereditá Cap.5 di Parte I, conversione 5 EUR commissione / 5 EUR per punto FIB)" (Cap.30.1 linea 253) -- problema: la fonte normativa delle commissioni 5 EUR/op e' Cap.2 PI (ereditá 8 di ACTIVE_TASK.md), non Cap.5 PI -- classificazione: **NEUTRO** (errore di referencing, valore corretto).

- "1. p_hit piu alto sul candidato. Si seleziona il candidato S_c tale che p_hit(S_c) = max_c p_hit(S_c)..." (Cap.28.3 linea 112) -- problema: il confine fra livello 1 (max) e livello 2 (tie entro epsilon_p) non e' esplicitamente dichiarato come "se |p_hit(S_1)-p_hit(S_2)| > epsilon_p vince max; se <= epsilon_p va a livello 2" -- classificazione: **NEUTRO** (ambiguita lieve, replay bit-exact garantito se le implementazioni adottano la stessa convenzione).


---

## Classificazione finding per il supervisore

| # | Problema | Classificazione | Default Orchestratore |
|---|----------|-----------------|------------------------|
| 1 | f_5 stabilita cross-regime omessa in Cap.30 (ereditá 28 violata) | **BUG REALE** | SI -- Developer obbligatorio |
| 2 | Cap.29.2 include Delta_t_cromosoma in messaggio Telegram, in violazione di Cap.9.2 PII; auto-contraddizione interna | **BUG REALE** | SI -- Developer obbligatorio |
| 3 | Cap.27.4 dichiara "11 campi" ma ne elenca 12 (12 e' il valore corretto) | **BUG REALE** (formale, non operativo) | SI -- Developer obbligatorio (semplice correzione testo) |
| 4 | Ereditá 3 (sessione 8:00-22:00 CET) non citata esplicitamente in Cap.27 ne in Cap.30 | NEUTRO | In attesa decisione supervisore |
| 5 | Cap.30.1 cita "Cap.5 PI" come fonte commissioning invece di Cap.2 PI | NEUTRO | In attesa decisione supervisore |
| 6 | W_B introdotto in Cap.27.5 ma omesso dalla lista del preambolo | NEUTRO | In attesa decisione supervisore |
| 7 | Cap.10.4 PII citato come fonte di "fill virtuale" (definizione e' in Cap.7.3 PII) | NEUTRO | In attesa decisione supervisore |
| 8 | Tie-break livello 1 vs livello 2: confine epsilon_p non esplicito | NEUTRO | In attesa decisione supervisore |
| 9 | Esempi timestamp_emission con secondi (Cap.6.1 PII dichiara minuto chiuso) | NEUTRO | In attesa decisione supervisore |
| 10 | Cap.30.1 motivazione W_prod=21 con riferimento improprio a eta_div di Cap.25.4 PV | NEUTRO | In attesa decisione supervisore |
| 11 | Esempio numerico tie-break mancante (non in AC) | NEUTRO | In attesa decisione supervisore |

**Sintesi**:
- 3 BUG REALI (di cui 2 bloccanti, 1 formale non bloccante) -> Developer obbligatorio.
- 8 NEUTRO -> in attesa della decisione del supervisore.
- 0 MIGLIORA PERFORMANCE.
- 0 RISCHIO PEGGIORAMENTO.

---

## Nota su Planner-Developer responsibility

Il BUG REALE #2 ha una circostanza attenuante: il Planner stesso (ACTIVE_TASK.md linea 88, decisione di scope (c)) ha elencato Delta_t_cromosoma e T_touch_max nelle "posizioni 5-9 del layout mobile". Questa formulazione e' in tensione con l'AC-29-1 ("Cap.29 cita esplicitamente Cap.9.2 PII (formato 9 voci) come riferimento normativo del contenuto") e con Cap.9.2 PII paragrafo 253 (PASS Review v4 + Iterazione 5).

Il Developer ha **tre opzioni** in tensioni come questa: (a) seguire il Planner contraddicendo Cap.9.2 PII; (b) seguire Cap.9.2 PII contraddicendo il Planner; (c) sollevare M-promemoria al Planner chiedendo chiarimento.

Il Developer ha scelto un ibrido patologico: include Delta_t_cromosoma (segue Planner), esclude T_touch_max (segue Cap.9.2 PII), e nel paragrafo successivo dichiara "Delta_t_cromosoma non figura nel messaggio Telegram... Il layout pubblica le 9 voci dichiarate in Cap.9.2; nient'altro" (contraddicendo la lista numerata appena prima).

Il risultato e' un documento **auto-contraddittorio**. Il Developer doveva sollevare M-promemoria al Planner prima di pubblicare, oppure adottare una posizione coerente e dichiararla esplicitamente. Il rework v2 dovra chiarire questa tensione: o il Planner modifica la decisione di scope (c) (rimuovendo Delta_t_cromosoma e T_touch_max dalle posizioni 5-9 e mantenendo solo i 9 campi di Cap.9.2 PII), o il documento giustifica esplicitamente la deviazione e propone una mini-patch retroattiva a Cap.9.2 PII (vietata dall'Out-of-scope di ACTIVE_TASK.md linea 239: "Patch retroattive a CAP-01..CAP-05: nessuna modifica retroattiva alle Parti gia chiuse PASS").

Suggerimento al supervisore: la via naturale e' (i) chiedere al Planner di rivedere la decisione di scope (c) eliminando Delta_t_cromosoma e T_touch_max dalle voci pubblicate Telegram; (ii) il Developer riallinea Cap.29.2 alle 9 voci esatte di Cap.9.2 PII (con signal_id come prima voce, non come footer).

---

## M-promemoria nuovi (carryover Parti successive)

Nessuno. Tutti i M-promemoria pertinenti CAP-06 sono trattati come da task (M-2 v2 CAP-03 residuo chiuso in Cap.27.5 + Cap.30.4; M-2 OPEN rinvio Appendice E; M-16 OPEN-CONDIZIONALE rinvio Parte VII). I tre BUG REALI e gli 8 NEUTRO sono problemi di Parte VI v1 da risolvere nel rework v2, non M-promemoria per Parti successive.

---

## Verdetto finale

**FAIL**. Il documento ha due BUG REALI bloccanti che impattano direttamente la copertura del monitoring del bundle frozen in produzione (#1 omissione f_5) e la conformita del messaggio Telegram al contratto Cap.9.2 PII PASS Review v4 + Iterazione 5 (#2 inclusione Delta_t_cromosoma). Il BUG REALE #3 (11 vs 12 campi) e' una correzione testuale immediata.

Pipeline attesa: **FAIL -> rework v2 -> Review v2**. L'Orchestratore presentera al supervisore la tabella di classificazione e attendera la decisione sui finding NEUTRO prima di chiamare il Developer per il rework v2 (su almeno i 3 BUG REALI + eventuali NEUTRO approvati).

