# Review CAP-06 v2 -- Parte VI (Emissione segnali e lifecycle senza execution) -- rework post-FAIL v1

**Verdetto**: PASS

**Hash documento auditato**: `d082972` (commit [DEV] CAP-06 v2 rework documento) + `1bc37f3` (commit [DEV] CAP-06 v2 rework REPORT + indice + DEV_STATUS)
**File audit**: `docs/methodology_v2/CAP_06_parte_VI.md` (358 righe) + `reports/REPORT_CAP_06.md` (228 righe)
**Riferimento normativo**: `tasks/ACTIVE_TASK.md` sezione Finding di Review da risolvere (3 BUG REALI + 8 NEUTRO ratificati supervisore commit `bea513f`)
**Riferimento storico**: `reviews/REVIEW_CAP_06_review.md` (commit `5b9bc8d`, verdetto FAIL su v1 `8875f1c`)
**Data audit**: 2026-05-26
**Natura**: audit Review v2 del rework post-FAIL v1 (ciclo 2)

---

## Sintesi esecutiva

Audit ostile della Parte VI v2 produce verdetto PASS. Il rework v2 chiude sostanzialmente tutti e 3 i BUG REALI di Review v1 (#1 f_5_live omessa, #2 Delta_t_cromosoma in Cap.29.2, #3 11 campi vs 12) e tutti gli 8 NEUTRO ratificati dal supervisore via opzioni A/B. La nuova sotto-sezione Cap.30.3 dedicata a f_5_live e formalmente corretta (formula coerente con Cap.24.1 PV paragrafi 261-263; segmentazione regime via Cap.14 PIII applicata dal blocco 5 della pipeline Cap.27.1; frequenza piu bassa dichiarata; soglia N_reg_min_live e tolleranza alpha_f5 non congelate; soglia di alert riferita a f_5_global di Cap.24.6 PV paragrafo 330; impatto sul GA esplicitato sulla copertura dei 5 assi di selezione del fronte di Pareto). Cap.29.2 v2 e riallineato esattamente al contratto a 9 voci di Cap.9.2 PII Iterazione 5, con signal_id in posizione 1 per coerenza con il paragrafo 243 e con Delta_t_cromosoma + T_touch_max esclusi in coerenza con il paragrafo 253. Il preambolo lista 10 parametri di tuning operativo (estensione conseguente al Finding #1) e nessuna patch retroattiva a CAP-01..CAP-05 e introdotta. Nessun finding bloccante nuovo e emerso al secondo giro ostile.

Sono emersi 4 finding NEUTRO/cosmetici di impatto nullo o marginale sul ranking del GA e sulla conversione signal-to-trade: due residui di referencing non risolti dal rework v2 (motivazione W_prod ancora ancorata a Cap.25.4 PV in modo fuorviante; citazione Cap.11.2 PII per MFE/MAE post-target_1 errata -- Cap.11.2 PII e perimetro, le metriche sono in Cap.11.4-11.5 PII), una ambiguita tecnica nella regola di persistenza alert su f_5_live con giorni n/a, una imprecisione di notazione su distanza vs delta orientato negli esempi Telegram. Nessuno di questi finding impatta il comportamento del GA, il ranking dei cromosomi, la fitness reale o la conversione signal-to-trade -- tutti riferiscono al monitoring post-go-live o alla cosmesi del payload Telegram. Vengono riportati per completezza ma classificati NEUTRO; nessuno richiede rework. Il verdetto PASS conferma che la pipeline Parte VI e metodologicamente solida e operativa per CAP-07.

---

## Verifica chiusura BUG REALI di Review v1

| # | Finding v1 | Soluzione richiesta | Esito v2 | Evidenza puntuale (CAP_06_parte_VI.md) |
|---|------------|---------------------|----------|----------------------------------------|
| 1 | f_5 stabilita cross-regime omessa in Cap.30 (eredita 28 violata) | Nuova Cap.30.3 con f_5_live counterpart live di f_5(theta) di Cap.24.1 PV, segmentazione regime via Cap.14 PIII, frequenza piu bassa, soglia N_reg_min_live, alert su f_5_global * (1+alpha_f5), dashboard Cap.30.6 aggiornata | OK | Cap.30.3 righe 278-293: definizione formale con formula identica a Cap.24.1 PV par. 262; segmentazione R_t_emission_i via blocco 5 pipeline Cap.27.1; frequenza al massimo una volta per giornata di trading; N_reg_min_live=10 default non congelato; alpha_f5=0,25 default non congelato; soglia alert f_5_live(t) > f_5_global * (1+alpha_f5) con T_drift_persist persistenza; paragrafo Impatto sul GA riga 293 chiude esplicitamente la lacuna sui 5 assi di selezione del fronte di Pareto. Cap.30.6 riga 339 riporta riga dedicata; riga 343 alert esteso a Cap.30.3 |
| 2 | Cap.29.2 v1 include Delta_t_cromosoma in violazione Cap.9.2 PII par. 253; auto-contraddizione | Layout 9 voci esatte Cap.9.2 PII Iter.5, signal_id in posizione 1, paragrafo coerente esclusione Delta_t+T_touch_max, esempio senza EXP: | OK | Cap.29.2 righe 156-172: dichiarazione esattamente 9 voci con elenco normativo signal_id, direction, setup_class, entry_zone, target_1, target_2, stop_loss, timestamp_emission, target_2_type, stop_type (10 nomi raggruppati in 9 voci normative); paragrafo Convenzione di posizionamento del signal_id riga 158 cita paragrafo 243 PII; layout numerato 1-9 con signal_id voce 1, timestamp_emission voce 9; paragrafo riga 172 esclude Delta_t_cromosoma e T_touch_max citando paragrafo 253 PII; esempio righe 177-186 con 9 righe testuali senza EXP: ne WAIT:. Auto-contraddizione strutturale v1 rimossa |
| 3 | Cap.27.4 dichiara 11 campi ed elenca 12 | Sostituire 11 con 12 | OK | Cap.27.4 riga 49: Iterazione 4 con S esteso a 12 campi. Conteggio coerente (12 campi enumerati: signal_id, timestamp_emission, direction, entry_zone, target_1, target_2, target_2_type, stop_loss, stop_type, setup_class, Delta_t_cromosoma, T_touch_max) |

Risultato: tutti e 3 i BUG REALI di Review v1 chiusi sostanzialmente (non solo formalmente) -- verifica per testo eseguita riga per riga.

---

## Verifica chiusura NEUTRO di Review v1

| # | Finding v1 | Opzione approvata | Esito v2 | Evidenza puntuale |
|---|------------|-------------------|----------|-------------------|
| 4 | Sessione 8:00-22:00 CET non esplicitata (eredita 3) | A: aggiungere in Cap.27.1 + Cap.30.1 | OK | Cap.27.1 riga 15: finestra di sessione 8:00-22:00 CET di Cap.1 di Parte I (840 barre 1-min per sessione). Cap.30.1 riga 254: W_prod = 21 sessioni di trading rolling di 8:00-22:00 CET (~ 1 mese calendario di FIB, totale 17.640 barre 1-min) |
| 5 | Cap.5 PI -> Cap.2 PI per commissioning | A: sostituire riferimento | OK | Cap.30.1 riga 258: include il commissioning c = 1 pt FIB equivalente per operazione (eredita Cap.2 di Parte I, conversione 5 EUR commissione / 5 EUR per punto FIB) |
| 6 | W_B omesso dal preambolo | A: aggiungere W_B alla lista | OK (esteso a 10 parametri) | Preambolo riga 7: lista 10 parametri (T_recal_EGARCH, theta_B, T_B_persist, W_B, W_prod, T_drift_persist, T_emit_persist, epsilon_p, N_reg_min_live, alpha_f5). Estensione conseguente al Finding #1 documentata nel REPORT v2 |
| 7 | Cap.10.4 PII per fill virtuale (definizione in Cap.7.3 PII) | B: citazione doppia | OK | Cap.29.5 riga 232: (definizione Cap.7.3 di Parte II; uso nel log di chiusura Cap.10.4 di Parte II) |
| 8 | Tie-break livello 1/2 confine epsilon_p non esplicito | B: paragrafo dedicato | OK | Cap.28.3 riga 117: paragrafo Convenzione operativa di tie sul livello 1 con formula esplicita simmetrica |p_hit(S_c1) - p_hit(S_c2)| <= epsilon_p |
| 9 | Timestamp con secondi violano minuto chiuso Cap.6.1 PII | A: normalizzare HH:MM | OK | Cap.29.2 riga 185: EMIT: 10:42 CET. Cap.29.3 riga 207: TRIG: 11:18 CET @ 13.255. Cap.27.4 riga 58 chiarisce minuto chiuso CET |
| 10 | Motivazione W_prod=21 con eta_div improprio | B: rimuovere parentesi eta_div | OK (residuo documentale: vedi finding nuovo #1 sotto) | Cap.30.1 riga 254: parentesi su eta_div rimossa. Residuo: la motivazione mantiene persistenza del flag di regime di Cap.25.4 di Parte V -- il riferimento e ancora fuorviante perche Cap.25.4 PV definisce un flag binario per-fold senza concetto di persistenza temporale. Vedi finding ostile nuovo #1 (NEUTRO documentale) |
| 11 | Esempio numerico tie-break mancante | A: aggiungere esempio | OK | Cap.28.3 riga 119: esempio S_c1/S_c2 con p_hit = 0,620000 vs 0,6200003, risoluzione livello 2 (S_c2 directional > S_c1 trade_range), caso comparativo epsilon_p = 10^-9 |

Risultato: tutti gli 8 NEUTRO chiusi con le opzioni A/B approvate dal supervisore. Il Finding #10 ha un residuo documentale rilevato nel secondo giro ostile (vedi sotto).

---

## Verifica sub-AC nuovi v2

| Sub-AC | Criterio | Esito | Evidenza |
|--------|----------|-------|----------|
| AC-28-3bis | Convenzione operativa epsilon_p in Cap.28.3 esplicita per replay bit-exact | OK | Cap.28.3 riga 117: formula simmetrica e transitiva |
| AC-30-3bis-1 | Cap.30.3 definisce esplicitamente f_5_live(t) con segmentazione regime e frequenza piu bassa | OK | Cap.30.3 righe 278-289: definizione formale + frequenza end-of-session |
| AC-30-3bis-2 | Cap.30.3 dichiara N_reg_min_live e alpha_f5 come parametri di tuning operativo non congelati | OK | Cap.30.3 riga 289 (N_reg_min_live=10 default non congelato); riga 291 (alpha_f5=0,25 default non congelato); preambolo riga 7 entrambi presenti |

Risultato: i 3 sub-AC nuovi v2 sono soddisfatti.

---

## Verifica no-regressione AC v1

Audit a campione sui 38 AC v1 (verifica che il rework v2 non abbia introdotto regressioni). Campione mirato sugli AC piu sensibili:

| AC-ID | Esito v1 -> v2 | Note |
|-------|----------------|------|
| AC-27-1 | OK -> OK | Cap.27.1 riga 15 invariato sostanzialmente (vincolo emissione-only + PC i5-7200U + DAPI 10001), arricchito con esplicitazione finestra 8:00-22:00 CET |
| AC-27-2 | OK -> OK | Cap.27.1 righe 19-29: lista 9 blocchi invariata |
| AC-27-5 | OK -> OK | Cap.27.5 righe 63-77: tutti i 5 elementi della chiusura M-2 v2 CAP-03 invariati |
| AC-27-6 | OK -> OK | Tutte le citazioni a Cap.6.1 PII, Cap.8 PII, Cap.10 PII, Cap.13-14 PIII, Cap.16-20 PIV, Cap.25-26 PV preservate |
| AC-28-1 | OK -> OK | Cap.28.1 cita Cap.6.3 PII, estende operativamente |
| AC-28-2 | OK -> OK | Cap.28.2 no-refresh + 4 bullet operativi + motivazione operativa eredita 2 invariati |
| AC-28-3 | OK con riserva -> OK | Cap.28.3 4 livelli ordinati invariati + convenzione operativa epsilon_p esplicita (Finding #8) |
| AC-28-4 | OK -> OK | Cap.28.4 5 campi log + replay bit-exact + citazione Cap.10 PII invariati |
| AC-28-5 | OK -> OK | epsilon_p non congelato (Cap.28.3 + Cap.28.4) |
| AC-29-4 | OK -> OK | Cap.29.3 trigger_event separato + signal_id + Delta_t_pretrigger Cap.24.5 PV invariati; esempio normalizzato HH:MM |
| AC-29-5 | OK -> OK | Cap.29.5 transizione terminale + 6 stati Cap.7.1 PII + R_gross + esempio invariati |
| AC-29-6 | OK -> OK | Cap.29.1 cita L_max qualitativo + rinvio Appendice E (M-2 OPEN) |
| AC-30-2 | OK -> OK | Cap.30.2 IQR cross-fold + T_drift_persist non congelato (default 5 giorni) invariati |
| AC-30-4 | OK -> OK | Cap.30.4 calcolo live B(t) + alert + anticipo ricalibrazione invariati |
| AC-30-5 | OK -> OK | Cap.30.5 r_emit_live + soglie ereditate E_max=5, E_min=0,2 + T_emit_persist default 10 giorni invariati |
| AC-30-6 | OK -> OK (estesa) | Cap.30.6 dashboard lato motore + Telegram unico cellulare invariati; contenuto esteso con riga f_5_live + alert lista esteso |
| AC-30-7 | OK -> OK | Cap.30.7 no DSR/PBO live + rinvio Parte VII invariato |
| AC-T-3 | OK -> OK | Verifica negativa lessicale eseguita: nessuna occorrenza di order routing, fill (eccetto fill virtuale come definizione Cap.7.3 PII), slippage, broker execution in senso execution, posizione netta in senso execution. Cap.30.6 riga 345 esplicita Nessuna interazione execution-side |
| AC-T-4 | OK -> OK | Cap.27.3 riga 43 non costituisce re-training del GA; Cap.30.2 riga 276 + Cap.30.5 riga 330 Cap.30 emette alert; non chiude il loop |
| AC-T-5 | OK -> OK | Tutti gli esempi (Cap.29.2: 13.250, 13.260, 13.350, 13.200, 13.450, +95, -55; Cap.29.3: 13.255; Cap.29.5: 13.350, +95) sono multipli di 5 in notazione italiana (separatore migliaia . es. 13.255 = 13255 pt FIB / 5 = 2651) |
| AC-T-6 | PARZIALE -> OK | Preambolo riga 7 esteso a 10 parametri (W_B + N_reg_min_live + alpha_f5 aggiunti); tutti i parametri tuning operativo con dominio + default + non congelato |
| AC-T-11 | OK -> OK | Working tree pulito (verificato git status --short: solo .claude/scheduled_tasks.lock ignorato). Commit d082972 + 1bc37f3 pushati su origin/main |

Risultato no-regressione: nessuna regressione su AC v1. Cinque AC v1 PARZIALE/KO promossi a OK (AC-27-3, AC-27-7, AC-29-1, AC-29-2, AC-30-1, AC-30-3, AC-T-1, AC-T-6).

---

## Audit ostile - finding nuovi emersi dal rework v2

Secondo giro ostile sul perimetro completo.

### Finding ostile #1 - Cap.30.1 motivazione W_prod ancora fuorviante
Cap.30.1 riga 254. La motivazione mantiene persistenza del flag di regime di Cap.25.4 PV ma Cap.25.4 PV non parla di persistenza temporale.
Impatto GA: nullo. Classificazione: NEUTRO documentale.

### Finding ostile #2 - Cap.30.3bis cita Cap.11.2 PII per MFE/MAE
La citazione corretta sarebbe Cap.11.4 o Cap.11.5 PII.
Impatto GA: nullo. Classificazione: NEUTRO documentale.

### Finding ostile #3 - Cap.30.3 regola persistenza giorni n/a ambigua
Gestione dei giorni n/a per cardinalita insufficiente non specificata.
Impatto GA: nullo. Classificazione: NEUTRO.

### Finding ostile #4 - Cap.29.2 distanza vs delta orientato
Formula usa modulo ma esempio mostra +/- delta orientato.
Impatto GA: nullo. Classificazione: NEUTRO cosmetico.

---

### Finding ostile dettaglio aggiuntivo

Dettagli operativi sui 4 finding ostili gia elencati:

**Finding #1 dettaglio**: Cap.25.4 PV (test parallel media-mediana, paragrafi 401-414) definisce un flag binario per-fold attivato quando eta_div(k) > 0,10 (10 percento delle sessioni divergenti nel fold k). Non vi e alcun concetto di persistenza temporale ne di 21 sessioni in Cap.25.4 PV. Il flag e una statistica per-fold (sull intero fold OOS di 12 settimane), non una finestra rolling di 21 sessioni. Il documento v2 ha gia corretto la parentesi su eta_div (Finding #10 v1 risolto) ma il riferimento generico a Cap.25.4 PV come motivazione di W_prod=21 sessioni rimane fuorviante. W_prod resta non congelato; la motivazione e solo testuale del default proposto. Impatto: nullo.

**Finding #2 dettaglio**: Cap.30.3bis riga 300 dice: La submacchina position lifecycle di Cap.11.2 di Parte II traccia inoltre MFE/MAE post-target_1 (dal momento di target_1_hit alla chiusura della submacchina). Cap.11.2 PII e Perimetro della submacchina: OUT-OF-SCOPE e IN-SCOPE (paragrafi 364-376) - non tracciamento di MFE/MAE. Le metriche MFE/MAE post-target_1 sono enumerate in Cap.11.4 PII riga 399 e Cap.11.5 PII riga 408. La citazione corretta sarebbe Cap.11.4 PII o Cap.11.5 PII. Errore di referencing in sotto-sezione di reporting.

**Finding #3 dettaglio**: Cap.30.3 riga 291 regola alert su f_5_live richiede f_5_live(t) > f_5_global * (1 + alpha_f5) per piu di T_drift_persist giorni di trading consecutivi. Tuttavia la riga 289 dichiara che f_5_live puo essere n/a se N_reg_min_live non e soddisfatto in entrambi i regimi. La regola non chiarisce: un giorno n/a resetta il counter, lo sospende, o conta come non sopra soglia (reset)? Tre implementazioni diverse producono comportamenti di alert diversi a parita di feed, potenziale violazione del replay bit-exact di Cap.10 PII. Ambiguita per regola di monitoring (post-go-live), non per ranking GA.

**Finding #4 dettaglio**: Cap.29.2 dice target_1 - prezzo in punti FIB e distanza dal centro della banda |target_1 - p_ref| in pt, formato TGT1: prezzo (+/-distanza pt). La formula |.| e il modulo (sempre non negativo); l esempio mostra +95 (per LONG target_1 > p_ref) e -55 (per stop_loss < p_ref). +95 e -55 sono il delta orientato (target_1 - p_ref), non il modulo. Terminologia distanza impropria per valore con segno. Coerenza interna: formato esempio coerente con delta orientato; formula formale e modulo. Lieve imprecisione semantica nel layout mobile (cosmetica).

### Altri controlli ostili (nessun finding nuovo)

- Coerenza f_5 con frequenza Cap.30.2: f_5_live frequenza piu bassa (al massimo una volta per giornata) coerente con task. Alert su T_drift_persist giorni consecutivi (default 5) coerente con Cap.30.2.
- N_reg_min_live=10 motivazione qualitativa: la riga 289 dichiara popolazione minima per regime statisticamente significativa - sufficiente.
- alpha_f5=0,25 motivazione qualitativa: la riga 291 dichiara tolleranza relativa 25 percento rispetto al walk-forward - sufficiente.
- Convenzione signal_id posizione 1 paragrafo 243: citato esplicitamente Cap.29.2 riga 158. OK.
- Paragrafo 253 esclusione Delta_t+T_touch_max: citato esplicitamente Cap.29.2 riga 172. OK.
- Asimmetria dashboard Cap.30.6 (riga f_5_live vs tabella f_1-f_4): strutturalmente motivata e esplicitata riga 339. Coerente.
- CARRYOVER.md invariato: giustificazione preambolo generico copre i 3 parametri nuovi. Accettabile. Domanda aperta REPORT v2 punto 5 lascia al Planner Parte VII traccia per-parametro eventuale.
- No patch retroattive: verificato commit d082972 modifica solo CAP_06_parte_VI.md; commit 1bc37f3 modifica solo REPORT_CAP_06.md, 00_indice.md, DEV_STATUS.md. Nessuna patch retroattiva.
- AC-T-3 no execution: verifica negativa lessicale OK. Nessun order routing, slippage execution, broker execution senso execution, posizione netta senso execution. fill solo come fill virtuale Cap.7.3 PII.
- AC-T-4 no re-training: occorrenze re-training/ritraining solo per rinviare Parte VII Cap.36.
- Esempi numerici tutti multipli di 5 (notazione italiana, separatore migliaia .): verificati.
- Coerenza Cap.30.6 dashboard: contenuto include tabella f_1-f_4, riga f_5_live, tabella lifecycle, grafico B(t), grafico r_emit, lista alert. Esauriente.

---

## Verifica vincoli trasversali AC-T-1..AC-T-11

| AC-T | Esito v2 |
|------|----------|
| AC-T-1 (32 eredita citate) | OK - eredita 3 (sessione), 8 (commissioni Cap.2 PI), 10 (12 campi), 14 (9 voci esatte), 28 (f_5_live) tutte ora citate esplicitamente. Eredita 1-32 verificate a campione dalla tabella AC v2 del REPORT |
| AC-T-2 (M-promemoria) | OK - M-2 v2 CAP-03 residuo chiuso (Cap.27.5+Cap.30.4); M-2 OPEN rinviato Appendice E; M-16 OPEN-CONDIZIONALE rinviato Parte VII |
| AC-T-3 (no execution) | OK - verifica negativa lessicale eseguita |
| AC-T-4 (no re-training) | OK - Cap.27.3 + Cap.30.2 + Cap.30.5 esplicitano alert/no loop chiuso |
| AC-T-5 (esempi multipli di 5) | OK - tutti gli esempi numerici verificati |
| AC-T-6 (parametri tuning non congelati) | OK - preambolo lista 10 parametri; tutti con dominio + default + non congelato |
| AC-T-7 (lunghezza ~6 pp) | OK - 358 righe non-blank, ~6 pp |
| AC-T-8 (italiano formale) | OK - registro coerente con CAP-01..CAP-05 |
| AC-T-9 (REPORT 5 sezioni + rollback + finding-per-finding) | OK - REPORT v2 ha tutte e 5 le sezioni + tabella AC v2 + sezione Iterazione 2 - risposta ai finding di Review v1 |
| AC-T-10 (indice aggiornato) | OK - 00_indice.md riga 48: IN REVIEW Review v2 (documento v2 commit d082972...) |
| AC-T-11 (file committati pushati, working tree pulito) | OK - commit d082972 + 1bc37f3 su origin/main; git status --short mostra solo .claude/scheduled_tasks.lock (ignorato) |

---

## Classificazione finding nuovi per il supervisore

| # | Problema | Classificazione | Mandare a Development? |
|---|----------|-----------------|------------------------|
| 1 | Cap.30.1 riga 254 motivazione W_prod=21 cita ancora persistenza del flag di regime di Cap.25.4 di Parte V - Cap.25.4 PV non parla di persistenza temporale ma di flag binario per-fold; referencing residuo del Finding #10 v1 | NEUTRO | NO - non cambia nulla di misurabile sul GA, W_prod resta non congelato; eventuale correzione di referencing futura |
| 2 | Cap.30.3bis riga 300 cita Cap.11.2 PII traccia MFE/MAE post-target_1; Cap.11.2 PII e Perimetro, le metriche sono in Cap.11.4-11.5 PII | NEUTRO | NO - referencing impreciso, definizione delle metriche corretta nel testo |
| 3 | Cap.30.3 regola di alert T_drift_persist giorni consecutivi su f_5_live - gestione dei giorni n/a per cardinalita non specificata; ambiguita di replay bit-exact | NEUTRO | NO - ambiguita per regola di monitoring, non per ranking/fitness GA |
| 4 | Cap.29.2 distanza dal centro della banda usa modulo nella formula ma +/- delta negli esempi; lieve imprecisione semantica | NEUTRO | NO - cosmesi del payload Telegram, nessun impatto su GA |

Sintesi finding nuovi v2:
- 0 BUG REALI
- 0 MIGLIORA PERFORMANCE
- 4 NEUTRO (documentali/cosmetici, nessuno con impatto su comportamento del GA, ranking, fitness, conversione signal-to-trade)
- 0 RISCHIO PEGGIORAMENTO

Raccomandazione al supervisore: nessun finding nuovo richiede rework. I 4 finding NEUTRO sono catalogati per completezza ma non passano a Development (regola CLAUDE.md: NEUTRO non va mai a Developer senza esplicita approvazione del supervisore).

---

## M-promemoria nuovi (carryover Parti successive)

Nessuno nuovo emerso dalla Review v2. La decisione del Developer di lasciare tasks/CARRYOVER.md invariato e accettabile: i 3 parametri nuovi v2 (W_B, N_reg_min_live, alpha_f5) sono coperti dalla dichiarazione generica del preambolo di Parte VI (10 parametri di tuning operativo non congelati, riconsiderati post-go-live), e la sezione Domande aperte del REPORT v2 (punto 5) lascia al Planner di Parte VII la decisione se servono M-promemoria per-parametro per la calibrazione empirica post-go-live.

---

## Verdetto finale

PASS. Il rework v2 chiude sostanzialmente tutti i 3 BUG REALI di Review v1 (verificato per testo riga per riga) e tutti gli 8 NEUTRO con le opzioni A/B approvate dal supervisore. La nuova sotto-sezione Cap.30.3 dedicata a f_5_live e metodologicamente solida e chiude la lacuna sui 5 assi di selezione del fronte di Pareto del NSGA-II. Cap.29.2 v2 e riallineato esattamente al contratto a 9 voci di Cap.9.2 PII Iterazione 5, con signal_id in posizione 1 per coerenza con il paragrafo 243 e con Delta_t_cromosoma + T_touch_max esclusi in coerenza con il paragrafo 253. Il preambolo lista correttamente 10 parametri di tuning operativo (estensione conseguente al Finding #1 documentata nel REPORT v2). Nessuna patch retroattiva a CAP-01..CAP-05 e working tree pulito.

I 4 finding nuovi emersi dal secondo giro ostile sono tutti NEUTRO documentali/cosmetici, nessuno con impatto sul comportamento del GA, ranking dei cromosomi, fitness reale o conversione signal-to-trade. Nessuno richiede rework.

Pipeline successiva: Orchestratore esegue le 7 condizioni di chiusura sessione (CLAUDE.md):
1. Review PASS pubblicata (questo file) - DA COMMITTARE E PUSHARE
2. DEV_STATUS azzerato
3. Documento + report pubblicati su origin/main
4. Indice aggiornato Parte VI come PASS con data e hash review
5. ACTIVE_TASK lasciato storico
6. CARRYOVER aggiornato con M-promemoria carryover di CAP-06 (M-2 OPEN, M-16 OPEN-CONDIZIONALE; nessun nuovo M-promemoria emesso)
7. Riepilogo + prompt-template al supervisore per nuova sessione CAP-07

Atteso: sessione CAP-06 chiusa; sessione successiva apre CAP-07 (Parte VII Cap.31-34 validazione OOS + DSR + PBO + bootstrap stazionario).
