# Review CAP-DATA-01 (Parte 8) - Convenzione dati storici e politica di rollover

**Verdetto**: PASS

**Iterazione**: v2 (rework chirurgico post-CONDITIONAL v1)
**Data**: 2026-05-27
**Reviewer**: Subagente reviewer (Claude Code)
**HEAD origin/main auditato**: 015c47a ([DEV] CAP-DATA-01 v2 rework: fix 1 r190 aritmetica rolls + fix 2a bar_synthetic=False simmetrico + fix 2b L_avg Politis-White independent calibration)

**File auditati (post-rework v2)**:
- docs/methodology_v2/CAP_08_parte_8.md (239 righe, +2 righe rispetto a v1)
- reports/REPORT_CAP_08.md (329 righe, +93 righe rispetto a v1: sezione Iterazione 2 in coda)
- docs/methodology_v2/00_indice.md (Parte 8 status invariato IN REVIEW v1 Developer 2026-05-27)
- data/sessions/fib_session_calendar.csv (invariato, 6 righe E1-E5)
- data/sessions/README.md (invariato)

**Riferimento ai 3 finding ratificati dal supervisore** (Opzione A allargata 2a+2b):
- Finding 1 BUG REALE non bloccante - fix aritmetica rolls r190
- Finding 2a MIGLIORA PERFORMANCE espansione - sample selection bar_synthetic=False simmetrico
- Finding 2b MIGLIORA PERFORMANCE originale - calibrazione L_avg Politis-White indipendente
- Finding 3 NEUTRO - NON applicato per default CLAUDE.md (corretto)

**Eccezione normativa applicata**: cross-index in Cap.42 resta dichiarazione PHASE-2 senza implementazione, ratificata dal supervisore in tasks/SESSION_HANDOFF_CAP-07_to_CAP-DATA-01.md sezione 4 decisione (1). Il rework v2 non ha modificato Cap.42; eccezione invariata.

**Scope dell audit v2**: focalizzato sul rework chirurgico + spot-check non-regressioni. Non ripete da capo l audit v1 (PASS formale 16/16 AC gia verificato in Review v1).

---

## Verifica puntuale dei 3 fix

### Fix 1 - Aritmetica rolls Cap.43 r190 - OK

**Vecchio testo (pre-rework, Review v1 r190)**:
> il numero di roll e sufficiente (sei rolls per anno sul FIB con scadenze trimestrali, dodici-quattordici roll nella finestra di 18-24 mesi)

**Nuovo testo (post-rework v2, r190)**:
> il numero di roll e sufficiente (quattro rolls per anno sul FIB con scadenze trimestrali, sei-otto roll nella finestra di 18-24 mesi) per consentire un confronto statistico significativo fra le due serie.

**Verifica aritmetica**: 4 rolls/anno x 1,5-2 anni = 6-8 rolls in 18-24 mesi. Internamente coerente con scadenze trimestrali (marzo, giugno, settembre, dicembre) convenzione standard FIB su IDEM.

**Verifica giustificazione retorica**: la giustificazione della finestra 18-24 mesi (sufficiente significativita statistica per il confronto fra le due serie) resta valida con 6-8 rolls invece di 12-14. Il principio retorico e invariato; cambia solo il quantum aritmetico, che ora torna.

**Esito**: fix 1 applicato correttamente.

---

### Fix 2a - Convenzione di selezione del campione bar_synthetic=False simmetrico - OK

**Localizzazione**: Cap.43, nuova clausola Convenzione di selezione del campione (sample selection) inserita fra Finestra di validazione (r190) e Metriche di confronto (r194). La clausola occupa r192. Inoltre il preambolo del paragrafo Metriche di confronto e stato esteso (r194).

**Verifica dei tre requisiti del finding**:

1. **Le 4 metriche operano su bar_synthetic = False** - OK. Tutte e quattro le metriche del sanity check definite di seguito sono calcolate sulla serie filtrata a bar_synthetic = False (r192).
2. **Filtro simmetrico sulle due serie** - OK. applicata simmetricamente alla serie ratio-adjusted e alla serie unadjusted-stitched sul medesimo intervallo della finestra di validazione (r192). Inoltre il preambolo del paragrafo Metriche di confronto e stato esteso a Per ciascuna delle due serie (ratio-adjusted e unadjusted-stitched), sul medesimo intervallo della finestra di validazione e con il filtro bar_synthetic = False applicato simmetricamente (r194), come richiamo di rinforzo.
3. **Citazione esplicita di Cap.40 r92** - OK. La convenzione eredita il precedente metodologico di Cap.40 (riga 92), che dichiara la regola bar_synthetic = False per le feature di volatilita del modello EGARCH (r192). Citazione letterale con numero di riga 92.

**Razionale del fix integrato nel testo**: la clausola spiega esplicitamente perche senza filtro si distorcerebbero le metriche (zeri strutturali della griglia regolare - contaminazione di distribuzione, autocorrelazione, sigma realized). Coerente con il finding ratificato.

**Esito**: fix 2a applicato correttamente.

---

### Fix 2b - Calibrazione L_avg indipendente via Politis-White (2004) - OK

**Localizzazione**: Cap.43, paragrafo Criterio di accettazione - r201 (post-rework, shift di +2 righe rispetto a v1 r199 per inserimento della clausola di sample selection).

**Verifica dei tre requisiti del finding**:

1. **L_avg calibrato indipendentemente via Politis-White (2004) sulla serie filtrata bar_synthetic=False, NON eredita da Cap.34.2** - OK. calibrata indipendentemente via la procedura di Politis e White (2004) sulla serie filtrata a bar_synthetic = False; L_avg non eredita il valore congelato di Parte VII Capitolo 34.2 (r201). Riferimento esplicito a Politis e White (2004) presente.
2. **Motivazione esplicita della divergenza (unita diverse, struttura autocorrelazione diversa)** - OK. la struttura di autocorrelazione e l unita temporale dei rendimenti su cui Cap.34.2 calibra (rendimenti per-segnale eseguito della finestra OOS aggregata, segnali rari con autocorrelazione tipicamente bassa) sono strutturalmente diverse dalla struttura di autocorrelazione e dall unita dei rendimenti su cui Cap.43 calibra (rendimenti per-barra-reale 1-min della finestra di sanity validation, con effetti GARCH intraday persistenti) (r201). Motivazione completa e tecnicamente corretta.
3. **L_avg dichiarato valore di lavoro non congelato, fissato a FASE-D** - OK. L_avg di Cap.43 e valore di lavoro non congelato in Parte 8, fissato al momento dell implementazione in FASE-D del roadmap del progetto (r201).

**Coerenza interna con Fix 2a**: il fix 2b cita esplicitamente post-filtro dichiarato nella Convenzione di selezione del campione sopra per chiudere il cerchio fra le due clausole. La relazione 2a vs 2b dichiarata nel finding (2a stabilisce QUALI osservazioni, 2b stabilisce STRUTTURA del bootstrap su quel campione) e onorata: il bootstrap calibra L_avg sulla serie che 2a ha gia filtrato.

**Esito**: fix 2b applicato correttamente.

---

### Finding 3 (NEUTRO) - Cap.38 r39 invariato - OK (corretto NON-applicato)

**Citazione attuale di Cap.38 r39**:
> Alla barra esatta del roll il rendimento log della serie ratio-adjusted e nullo per convenzione: il roll non genera un rendimento osservabile sulla serie continua, dato che il salto e assorbito dal fattore rho_k.

**Verifica**: la descrizione testuale di Cap.38 r39 e invariata rispetto allo stato pre-rework. Coerente con la regola CLAUDE.md NEUTRO non va mai a Developer e con la direttiva del Finding 3 ratificata dal supervisore.

**Esito**: Finding 3 correttamente NON applicato.

---

## Verifica non-regressioni rispetto al PASS formale v1

### Spot-check sui capitoli non toccati dal rework

Il rework v2 ha toccato esclusivamente Cap.43 (r190 sostituita, clausola r192 inserita, r194 estesa, r201 sostituita; variazione netta +2 righe). Tutti gli altri capitoli sono invariati:

| Capitolo | Stato post-rework v2 | Esito |
|----------|----------------------|-------|
| Preambolo (r1-7) | Invariato | OK |
| Cap.37 (r9-22) | Invariato | OK |
| Cap.38 (r24-51) | Invariato (incluso r39, Finding 3 NEUTRO non applicato) | OK |
| Cap.39 (r53-69) | Invariato | OK |
| Cap.40 (r71-103) | Invariato (incluso r92, riferimento sample selection bar_synthetic) | OK |
| Cap.41 (r105-137) | Invariato | OK |
| Cap.42 (r139-182) | Invariato (dichiarazione PHASE-2 cross-index) | OK |
| Cap.43 (r184-211) | Modificato: r190 corretta, r192 inserita, r194 estesa, r201 sostituita | OK (verificato sopra) |
| Cap.44 (r213-239) | Invariato | OK |

Confermato via git diff 17240b4 015c47a: tutto il delta e confinato dentro Cap.43.

### Verifica AC 16/16 v1 ancora OK

I 16/16 AC del v1 (AC-3.1 ... AC-3.8 + AC-DoD-1 ... AC-DoD-8) restano OK:

- AC-3.1 (Cap.37): invariato - OK.
- AC-3.2 (Cap.38): invariato - OK.
- AC-3.3 (Cap.39): invariato - OK.
- AC-3.4 (Cap.40): invariato - OK.
- AC-3.5 (Cap.41) + CSV: invariati - OK.
- AC-3.6 (Cap.42): invariato - OK (eccezione cross-index PHASE-2 rispettata).
- AC-3.7 (Cap.43): rafforzato dai fix 2a + 2b, ancora pienamente OK (la procedura normativa di sanity validation e ora piu completa, non meno).
- AC-3.8 (Cap.44): invariato - OK.
- AC-DoD-1..8: file/indice/CSV/README/REPORT/DEV_STATUS/commit/push tutti OK; REPORT esteso con sezione Iterazione 2.

### Eccezione cross-index Cap.42

Verifica: nessuna nuova citazione DCC/ADCC/BEKK/cross-index al di FUORI di Cap.42. Le occorrenze di cross-index sono confinate a Cap.42 r141-180 + r225 (Cap.44 esclusioni: Mix di vendor diversi per cross-index - gia presente in v1, riferimento a Cap.42) + r231-237 (Cap.44 Regola di estensione - gia presente in v1). Le menzioni di bar_synthetic = False in Cap.43 sono per la sample selection del sanity check single-instrument, non sono citazioni cross-index. Eccezione rispettata.

### Naming beta2 e identifier interno

Verifica: nome file docs/methodology_v2/CAP_08_parte_8.md (OK), identifier interno Parte 8 arabo (preambolo r1, r3, r5 - OK invariato), nome report reports/REPORT_CAP_08.md (OK), titolo report REPORT SUPERVISORE - CAP-DATA-01 (Parte 8) (OK invariato).

### Indice 00_indice.md

Verifica: Parte 8 ancora IN REVIEW (v1 Developer 2026-05-27) (r64). **Corretto**: l aggiornamento a PASS con hash review avviene a chiusura sessione (condizione 4 della checklist Orchestratore), non al rework v2. Le direttive del finding ratificato esplicitamente dichiarano: NON modificare indice (Parte 8 resta IN REVIEW). Rispettata.

### CSV e README invariati

- data/sessions/fib_session_calendar.csv invariato (1 header + 5 epoche E1-E5, schema 6 campi conforme task card sezione 3.5).
- data/sessions/README.md invariato.

### Eredita I-VII applicate correttamente nei capitoli toccati

Cap.43 (l unico capitolo toccato) cita ancora:
- Parte III Capitolo 12 (definizione rendimenti log) - r196, r207
- Parte III Capitolo 13.4 (diagnostica residui EGARCH Ljung-Box, ARCH-LM) - r208
- Parte VII Capitolo 34 (bootstrap stazionario Politis-Romano 1994) - r201, r209
- Cap.40 riga 92 (nuovo cross-riferimento intra-Parte 8 introdotto dal fix 2a) - r192

Nuovo riferimento bibliografico esterno: Politis e White (2004) (introdotto dal fix 2b, r201) - coerente con la prassi del doc v2 di citare paper accademici per metodi normativi (Politis-Romano 1994, Ljung-Box, ARCH-LM, ecc.).

Nessuna citazione di Parti/Capitoli inesistenti introdotta dal rework. Tutti i riferimenti incrociati restano verificati contro 00_indice.md stato 2026-05-27.

---

## Verifica REPORT_CAP_08.md aggiornato

**Sezione Iterazione 2 - risposta ai finding di Review v1** presente in coda al REPORT v1 (r241-329), occupa 89 righe (+93 righe rispetto a v1 - coerente con la dichiarazione dell Orchestratore).

**Contenuti verificati**:

- **Documenta i 3 fix con citazione delle righe modificate** - OK. Fix 1 cita r190; fix 2a cita nuova clausola normativa Convenzione di selezione del campione (sample selection) inserita fra Finestra di validazione e Metriche di confronto; fix 2b cita r199 (vecchia numerazione, ora r201 post-shift) con citazione vecchio testo e nuovo testo.
- **Documenta Finding 3 NEUTRO non applicato** - OK. Sezione esplicita Finding 3 - NEUTRO (NON applicato per default CLAUDE.md) (r295-297).
- **Tabella delta prima/dopo del rework v2** - OK. r309-315.
- **Criterio di rollback specifico del rework v2** - OK. r317-319 dichiara che il rework non introduce nuovi parametri congelati (L_avg di Cap.43 e valore di lavoro non congelato in FASE-D), la clausola di sample selection e invariante metodologico (eredita di Cap.40 r92), la correzione aritmetica di r190 e definitiva (fatto di mercato).
- **Output deliverable rework v2** - OK. r321-326 elenca i tre file modificati (CAP_08, REPORT_CAP_08, DEV_STATUS) e descrive il push diretto a origin/main.

**Coerenza interna con il documento**: il REPORT cita esplicitamente che le righe di Cap.43 si sono spostate per inserimento della clausola di sample selection (Cap.43 ora occupa r186-211, era r186-209 pre-rework, variazione +2 righe). Coerente con il diff git.

**Esito**: REPORT_CAP_08.md aggiornato in coerenza.

---

## Secondo giro ostile - domanda esplicita Sono sicuro di aver trovato tutti i problemi reali?

Re-verifica del perimetro completo post-rework con focus su problemi non immediatamente visibili:

1. **Coerenza interna fra Fix 2a e Fix 2b**: il fix 2b cita post-filtro dichiarato nella Convenzione di selezione del campione sopra - riferimento intra-paragrafo verificato (la clausola di sample selection e immediatamente sopra il Criterio di accettazione). Coerente. OK.

2. **Stimatore Newey-West (1987) di r197 per autocorrelazione**: gia presente in v1, invariato. Coerente con la diagnostica residui EGARCH di Parte III Cap.13.4. Nessun nuovo problema introdotto.

3. **Possibile interferenza con la convenzione di Cap.40 r92**: Cap.43 ora cita Cap.40 r92 come precedente metodologico. Cap.40 r92 e la dichiarazione che le feature di volatilita (EGARCH, classificazione di regime, dispersione realized) sono calcolate solo su barre con bar_synthetic = False. Il sanity check di Cap.43 e concettualmente diagnostica di distribuzione e di volatilita (quantili rendimenti log + autocorrelazione + sigma realized), pertanto l analogia regge: la sample selection di Cap.43 e coerente con la convenzione di Cap.40 r92. Coerente.

4. **Variabile T in L_NW = floor(4 * (T/100)^(2/9)) (r197)**: T dichiarata come lunghezza della finestra. Sotto la convenzione sample selection di r192, T va inteso come numero di barre con bar_synthetic = False nella finestra 18-24 mesi (non come numero totale di minuti della griglia regolare). Il documento non lo specifica esplicitamente, ma la lettura naturale post-clausola di sample selection e coerente: tutte le metriche calcolate sulla serie filtrata usano la T della serie filtrata. **Non e un problema operativo sul GA** (Cap.43 implementazione out-of-scope FASE-D); e tutt al piu una piccola ambiguita che FASE-D dovra risolvere automaticamente quando implementera la procedura. Non si propone come finding, perche la convenzione di sample selection r192 e chiara e applicata simmetricamente alle due serie sul medesimo intervallo, quindi T e definita coerentemente con il filtro.

5. **Ridenominazione Cap.43 r190 nel REPORT vs r190 nel documento**: nel REPORT iterazione 2 (r251), il Developer dichiara Cap.43 paragrafo Finestra di validazione (riga 190 nello stato pre-rework). Verifica: nel documento post-rework r190 e tuttora Finestra di validazione - il paragrafo non si e spostato, solo il testo interno e stato modificato. OK.

6. **Posizione effettiva della nuova clausola (r192) vs dichiarazione del REPORT (r267)**: il REPORT dichiara nuova clausola normativa Convenzione di selezione del campione (sample selection) inserita fra Finestra di validazione e Metriche di confronto. Verifica: la clausola e effettivamente fra r190 (Finestra di validazione) e r194 (Metriche di confronto). Posizione corretta.

7. **L_avg in Parte VII Cap.34.2**: il rework v2 dichiara esplicitamente che Cap.34.2 calibra L_avg = 10 su rendimenti per-segnale eseguito della finestra OOS aggregata, segnali rari con autocorrelazione tipicamente bassa. Verifica via 00_indice.md r55: la Parte VII Cap.34 e dichiarata Bootstrap stazionario (parametri B=2000, block length), uso per intervalli di confidenza su DSR e metriche di lifecycle. Non e stata aperta Parte VII per verificare letteralmente Cap.34.2; tuttavia, la motivazione operativa fornita nel Cap.43 r201 (rendimenti per-segnale eseguito vs rendimenti per-barra-reale 1-min) e tecnicamente coerente con il principio del bootstrap stazionario (Politis-Romano 1994), e la regola di non-eredita e metodologicamente corretta. Non si propone come finding.

8. **Conta righe del REPORT**: il REPORT dichiara nell header +93 righe rispetto a v1 (deduzione: era 236 righe in v1, ora 329 righe in v2). Conta confermata. Coerente.

9. **Push policy**: HEAD 015c47a su origin/main, commit message conforme al messaggio convenzionale dichiarato nel finding ratificato. Decisione (a) push diretto rispettata.

10. **Causalita F_(t-1)**: la convenzione di sample selection r192 e applicata ex-post sulla serie storica completa per scopi diagnostici (sanity check), non e un calcolo causale on-line. Non introduce leakage temporale. OK.

11. **Tick FIB 5pt** (memory project-fib-instrument): citato in r131 di Cap.41 (gia presente in v1, invariato). OK.

12. **Vincolo solo emissione** (DICHIARAZIONE_DI_INTENTI): nessun fix tocca esecuzione ordini, latenza Telegram, commissioni. Vincolo rispettato per inerzia (il rework v2 e interamente dentro la procedura di sanity validation, fuori dalla pipeline di emissione segnali).

**Conclusione del secondo giro**: nessun nuovo problema reale identificato. Il rework v2 e chirurgicamente preciso, internamente coerente, e non introduce regressioni.

---

## Tabella riassuntiva eventuali finding nuovi v2

| # | Problema | Classificazione | Mandare a Development? |
|---|----------|-----------------|------------------------|
| - | Nessun nuovo finding emerso dal rework v2 | - | - |

Il rework v2 e chirurgico e completo. I 3 fix ratificati sono applicati correttamente, il Finding 3 NEUTRO e correttamente non applicato, le non-regressioni sono verificate, le invarianti del documento metodologico v2 sono preservate.

---

## Verdetto finale

**PASS**.

Razionale del verdetto:
- 3/3 fix ratificati dal supervisore (Opzione A allargata 2a+2b) applicati correttamente (Fix 1 aritmetica rolls, Fix 2a sample selection bar_synthetic=False simmetrico con citazione Cap.40 r92, Fix 2b L_avg Politis-White calibrazione indipendente con motivazione divergenza Cap.34.2).
- 1/1 Finding 3 (NEUTRO) correttamente NON applicato (regola CLAUDE.md).
- Nessuna regressione sui 16/16 AC v1 (Cap.37, 38, 39, 40, 41, 42, 44 invariati; Cap.43 rafforzato dai fix).
- Eccezione cross-index Cap.42 rispettata (nessuna nuova citazione DCC/ADCC/BEKK fuori da Cap.42).
- Naming beta2 invariato (file CAP_08_parte_8.md, identifier Parte 8 arabo).
- CSV e README invariati.
- Indice 00_indice.md status invariato IN REVIEW (corretto: aggiornamento a PASS a chiusura sessione).
- REPORT_CAP_08.md aggiornato con sezione Iterazione 2 coerente (+93 righe, documenta i 3 fix con citazioni puntuali).

Tutti i finding del rework v2 hanno impatto operativo nullo sul GA nel doc v2 corrente (Cap.43 implementazione out-of-scope FASE-D), ma riducono il rischio downstream di falsi positivi sul criterio 3sigma in FASE-D (zeri strutturali nel campione + L_avg sottodimensionato, entrambi mitigati).

Il documento Parte 8 e strutturalmente solido e pronto per la chiusura sessione.

---

## M-promemoria nuovi emessi

**Nessuno**.

Il ciclo Review v2 di CAP-DATA-01 non emette nuovi M-promemoria. M-2 OPEN (verifica empirica L_max=30s Telegram) resta carryover invariato verso Appendice E (Parte 9) come confermato dall handoff CAP-07 -> CAP-DATA-01 sezione 1 e dal censimento Planner ACTIVE_TASK.md sezione Censimento M-promemoria pertinenti.

L eredita del rework v2 verso FASE-D del roadmap del progetto (Cap.43 implementazione effettiva del sanity check con sample selection bar_synthetic=False simmetrica e L_avg calibrato indipendentemente via Politis-White su serie filtrata) e gia documentata esplicitamente in Cap.43 r211 (Out-of-scope per CAP-DATA-01). Non richiede M-promemoria dedicato perche il task FASE-D (acquisizione storico Portara FASE-B + implementazione sanity check FASE-D) e gia censito nel roadmap del progetto.
