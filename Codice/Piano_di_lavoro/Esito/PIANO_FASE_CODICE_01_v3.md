# PIANO_FASE_CODICE_01 — Piano di lavoro della fase-codice (FASE-D) — **v3 riconciliato**

> **Stato:** BOZZA v3 per **ratifica AC**.
> **Audit:** ostile, eseguito dal Planner (Claude.ai) il 2026-06-30, **con verifica RM-2 delle citazioni contro `SPEC_FUNZ_01.md` e contro la metodologia v2** (`GA_metodologia_v2`). Questo header **sostituisce** l'auto-certificazione di v2 (che dichiarava un audit mai eseguito da questa superficie). Verdetto: v2 non ratificabile per mappatura-prezzo errata nell'invariante 7; v3 corregge.
> **Derivazione:** 375 requisiti `SPEC_FUNZ_01.md` (Sez.1–10) + confine Sez.12/13 + matematica motore nei CAP (metodologia v2). RM-2: ogni asserzione di stato-repo va verificata sul repo, il repo vince.
> **Cosa NON è:** non è una task-card, non l'implementazione, non fissa i dettagli per-modulo. Quelli scendono **dal** piano via `ISTRUZIONI_*.md` per-modulo, una alla volta, dopo la ratifica.

## Changelog v2 → v3 (mapping ai finding del MIO audit)

| Finding audit | Severità | Esito su v2 | Modifica in v3 |
|---|---|---|---|
| **AUDIT-1** — acquisizione Portara | BLOCCANTE | v2 diceva "compra 2 serie ma additivo ridondante/derivato". **Mezzo-sbagliato.** | **Si comprano DUE serie consegnate**: (a) Panama-additive (settle, default nativo Portara) + (b) ratio-adjusted/multiplicative (richiesta esplicita). La ratio è *ricostruibile* ma si compra anche consegnata = ground-truth per validare la ricostruzione del preprocessor. M0 carica 2, **deriva la 3ª** (unadjusted concatenata). Mail Arthur → **2 serie**. Cit.: metodologia v2 (tre-serie + ricostruzione preprocessing). |
| **AUDIT-2** — base prezzo dell'80pt | ALTO | v2 invariante 7b: 80pt/geometria su **unadjusted**. **Contraddice la metodologia.** | Invariante 7 **riscritto**: la valutazione del segnale (geometria + emissione incl. 80pt) è sulla **ratio** (metodologia: replay su ratio per la valutazione del segnale, Parte VII Cap.31.1 / Parte II Cap.10). L'unadjusted è **solo sanity** (Cap.43) + tape runtime (CN-9.16). Il dubbio di v2 (80 punti assoluti su scala ratio) → **domanda di metodologia non-bloccante** (§3 nota), non un invariante che il piano impone sopra il CAP. |
| **AUDIT-3** — claim sul repo | MEDIO | v2 cita "2340 file", "18 catture exports_sample", struttura R-9.35. | Restano **claim da verificare** a livello-modulo (RM-2), mai fatti. Marcati nel testo. |
| **AUDIT-4** — header auto-certificato | MEDIO | v2 dichiarava "audit completato (Planner/Claude.ai)" mai eseguito da questa superficie. | Header sostituito col verdetto di **questo** audit (sopra). |
| *(da v2, confermati validi)* | — | M8a/M8b split; fixture DIRECTA→M8a / ISP→M0; FIB-only scoped al motore; umiltà sample ISP. | **Mantenuti** — sono miglioramenti corretti e spec/metodologia-grounded. |

---

## 1. Inquadramento — chi governa cosa (cardine GC-2)

La spec è la **vista-prodotto/contratto**; la matematica del motore è nei **CAP** (Sez.12). Fonte-di-verità **doppia**, dichiarata per modulo:

- **Contratto (SPEC_FUNZ_01)**: schema-dato canonico, payload, state-machine, regola di emissione, consegna, runtime DAPI, gate di go-live, audit. Cit. `R-*/CN-*/NFR-*`.
- **Motore (CAP / metodologia v2)**: feature+pivot (Parte III), derivazione geometrica (Parte IV), GA/NSGA-II/walk-forward + soglie congelate (Parte V), matematica gate (Parte VII), **back-adjustment/roll/pre-expiry + le tre serie prezzo** (Parte 8). Cit. `CAP_* path:line` / capitolo.

> **Caso speciale — convenzioni di prezzo (AUDIT-1/2):** governato da CAP (Parte 8, tre serie) **e** dal contratto (CN-9.16: runtime=unadjusted; CN-5.2: 80pt floor assoluto). Materia di entrambe le fonti, dichiarata in M0 (§3, inv.7). La metodologia fissa: ratio per la **valutazione del segnale**, Panama per l'**audit monetario**, unadjusted per **sanity**.

Una card-modulo che fissa un comportamento del motore citando la spec (che non lo contiene) è bug di fonte. Una card del contratto che inventa una soglia congelata di Parte V è scope-creep. **Una card che inverte la mappatura-prezzo della metodologia (es. 80pt su unadjusted) è override del CAP — vietato.**

---

## 2. Architettura — DAG dei moduli

```
                 ┌──────────────────────────────────────────────────┐
   M0 Data ──────┤ schema canonico 13-campi (contratto condiviso)   │
   layer         │ + 2 serie CONSEGNATE (Panama-add. + ratio-mult.) │
   (2 tape)      │ + 1 DERIVATA (unadjusted concatenata)            │
                 └──────┬───────────────────┬───────────────┬───────┘
                        │                   │               │
                        ▼                   ▼               ▼
   M1 Payload ─▶ M2 State-machine   M3 Feature eng.   M8a Directa data-layer
   (puro)        & lifecycle        (RATIO: pivot/     (acquis. + archivio (b)
                 (fixture)           EGARCH/regime)     + riconcil. end-of-day)
                                          │             [dip. M0 — JOB post-22:00,
                                          ▼              NON gated su bundle]
                                   M4 Signal constr.          │
                                   + emissione                │
                                   (RATIO in eval; 80pt       │
                                    floor su serie eval)      │
                                          │                   │
                                          ▼                   │
                                   M5 GA core ─▶ M6 Frozen     │
                                   (NSGA-II,RATIO) bundle(SHA) │
                                          │         │         │
                                          ▼         ▼         │
                                   M7 Validator   M8b Runtime  │
                                   (PANAMA: audit  inference   │
                                    € → GO/NO-GO)  adapter ◀──┘
                                   (in panchina)  [dip.M0+M6+M8a]
                                                         │
                                                  ┌──────┴──────┐
                                                  ▼             ▼
                                              M9 Telegram   M10 Audit
                                              [dip.M2,M8b]   (trasversale)
```

### Tabella moduli

| ID | Modulo | Cosa costruisce (sintesi) | Fonte-di-verità | Dipende da | Costruibile **ora**? |
|---|---|---|---|---|---|
| **M0** | Data layer (training tape) | Loader **2 serie Portara consegnate** (Panama-additive + ratio-multiplicative), ciascuna con `unadjustedClose`+roll-cols → griglia 1-min canonica 13-campi. **Deriva** la 3ª serie (unadjusted concatenata). **Cross-check** ratio-consegnata vs ricostruzione-da-colonne (catch bug preprocessor). Filtro righe settle (vol 0 + diagnostico) + diagnostico tick-grid. Column-tolerant. | Schema: Sez.9 (CN-9.5..9). Serie/back-adjust: **CAP Parte 8** + metodologia v2 (tre-serie). Convenzione runtime: CN-9.16. Precond.: R-2.7, R-5.3 | — | **Sì, se** sample ISP presente (**da verificare**, §7) |
| **M1** | Payload & invarianti | Tupla `S`, domini, invarianti geometrici (`d_stop>b`, multipli 5, ordinamento target), immutabilità, segnale-unico-attivo | Sez.3 (R-3.1..37, CN-3.1..5) | — | **Sì** (fixture) |
| **M2** | State-machine & lifecycle | 1 stato non-terminale + 6 terminali, transizioni, precedenza eventi, raw touch, timer pre/post-trigger, submacchina posizione | Sez.4 (R-4.1..48, CN-4.1..12) | M1 | **Sì** (fixture) |
| **M3** | Feature engineering | Pivot, 37 feature causali, EGARCH, regime — **su serie ratio** (inv.7) | **CAP Parte III** (Cap.12–15). Consumo: Sez.9 (R-9.38..42) | M0 | No (dato reale) |
| **M4** | Signal construction + emissione | Derivazione `entry_zone`/`target_*`/`stop_loss` + tipi; regola emissione (3 cond. + **80pt floor**, AND), **valutata sulla serie di valutazione-segnale (ratio)** | Derivazione: **CAP Parte IV** (Cap.16–21). Emissione: Sez.5 (R-5.1..16, CN-5.1..3). 80pt: CN-5.2 + metodologia (riga valutazione-segnale=ratio) | M3, M1 | No |
| **M5** | GA core | Cromosoma, NSGA-II, fitness multi-obiettivo, walk-forward nested (purge/embargo) — **su ratio** | **CAP Parte V** (Cap.22–26) | M0–M4 | No (AWS) |
| **M6** | Frozen bundle | Artefatto immutabile 6 elementi, SHA-256, verifica-su-load fail-stop | Sez.8 (CN-8.3/.4/.5, R-8.24/.36) + Cap.35 | M5 | No |
| **M7** | Validator | Aggregazione OOS, DSR, PBO via CSCV, bootstrap; **audit monetario (E[R_net]/CVaR/MDD in €) su serie PANAMA** (5€/pt scala originale, Parte I Cap.2); 12 criteri → GO/NO-GO | Sez.8 (R-8.1..38, CN-8.1..7) + matematica **Parte VII** | M6 | No (**in panchina**) |
| **M8a** | **Directa data-layer** | Acquisizione DAPI (10003 storico post-chiusura + 10001 realtime, mai 10002), riconciliazione end-of-day (840 barre, schema 13-campi, R-9.31), **archivio (b)** append-only versionato (CN-9.22), logging cash. **Job post-22:00.** | Sez.7 (R-7.2/.14/.15) + Sez.9 (R-9.30/.31/.35/.36, CN-9.16/.22) | **M0 (schema)** | **Codice sì** (fixture DIRECTA); **run live** gated D-6 |
| **M8b** | **Runtime inference adapter** | Adapter DAPI→bundle (R-9.1, stesso schema), warm-up, gap-recovery runtime, gating qualitativo sul payload | Sez.7 (R-7.1..20, CN-7.1..9) + Sez.9 (R-9.1..43) + CAP Parte 9/10 | M0, **M6**, M8a | No (prereq. probe + bundle) |
| **M9** | Telegram delivery | Messaggio 9 campi mobile-first, 3 notifiche, retry/backoff, anti-duplicato persistito | Sez.6 (R-6.1..24, CN-6.1..9) + Appendice E | M2, **M8b** | No |
| **M10** | Audit & compliance | Log JSONL append-only immutabile, marker per-stato, retention 90gg rolling + permanente per segnali emessi | Sez.7.5 (NFR-7.3..7, R-7.18..20) | trasversale (M8a/M8b/M9) | No |

> **Dati Portara in acquisto:** **2 serie continue** settle-based, 1995→date, 1-min, stessa finestra, stesse colonne ciascuna (`unadjustedClose`/`spread`/`cumulativeSpread`/`contractName`/`tickcount` + roll-log): **(a) Panama-additive** (default nativo) + **(b) ratio-adjusted/multiplicative** (richiesta esplicita). M0 column-tolerant finché il tape pagato non è su disco e verificato. *(Claim "2340 file directa_history in-repo", "18 catture exports_sample", struttura esatta R-9.35 = AUDIT-3, da verificare a livello-modulo.)*

---

## 3. Invarianti trasversali (ogni modulo li preserva)

1. **research = runtime** (NFR-9.2): preprocessor di training (M0/M3) e adapter runtime (M8b) producono lo **stesso schema** 13-campi; stessa computazione feature su tape storico e griglia live. Lo schema 13-campi di M0 è **il contratto** su cui poggiano M3 e M8b.
2. **replay bit-exact** (NFR-9.1, NFR-8.1, CN-4.5): precedenza eventi deterministica; due replay sulla stessa finestra → stessa sequenza emissioni/`signal_id`/transizioni/timestamp.
3. **immutabilità del bundle** (CN-8.3/.4/.5): bundle hashato SHA-256, riverificato a ogni load; hash discordante → la pipeline **rifiuta di girare**.
4. **solo emissione, nessuna esecuzione** (CN-1.1, CN-7.1): porta ordini **10002 mai aperta**; il sistema pubblica segnali, l'operatore esegue a mano.
5. **edge = esclusiva del validator, PENDING** (Sez.8): **nessun modulo** asserisce GO/NO-GO né valori d'edge. Solo M7, in FASE-D. Verbi vietati ("supera il gate", "edge confermato", "GO") fuori da M7.
6. **PHASE-1 FIB-only — scope del MOTORE** (R-10.1, CN-10.1/.2): nessuna covarianza cross-index nel **feature tensor / cromosoma / walk-forward**. Lo scope "FIB-only" è del motore, **non dell'archivio**: M8a logga/archivia anche i cash europei (DGER/DSTX50/DITAS/DFRA) per il **solo gating qualitativo** (R-7.15, CN-7.8), fuori dal feature tensor. Archivio multi-strumento, motore single-instrument.
7. **Tre serie prezzo, consumatore esclusivo — mappatura della metodologia (AUDIT-1/2).** Il prezzo FIB esiste in tre rappresentazioni; nessun modulo le confonde. **M0 carica le due consegnate da Portara e deriva la terza.**
   - **(a) ratio-adjusted / multiplicative** (continua, scale-invariant; **consegnata** + ricostruibile/verificabile da `unadjustedClose`+`RollSpread`+roll-log) → **modelli a rendimenti log** (EGARCH, regime, feature, Cox) **E la valutazione del segnale** — geometria zona/target/stop e regola di emissione, **incluso il floor 80pt** — in training/backtest (metodologia: replay su ratio per la valutazione del segnale, Parte VII Cap.31.1 + Parte II Cap.10).
   - **(b) Panama-additive** (continua in punti assoluti; **consegnata nativa** da Portara, settle back-adjusted) → **audit monetario M7** (E[R_net]/CVaR/MDD in €, 5€/pt sulla scala originale, Parte I Cap.2) + sanity visivo + replay di controllo. **Non** entra nei modelli probabilistici (i suoi rendimenti log distorcono la varianza relativa).
   - **(c) unadjusted concatenata** (UnadjustedClose riga-per-riga + marker roll; **derivata** da M0) → **solo sanity check** (Cap.43, validazione finestra recente) **E** convenzione del **tape runtime** (CN-9.16: al runtime le barre arrivano unadjusted native del front-month).
   
   M0 done-when: cross-check ratio-consegnata vs ricostruzione (catch bug); 80pt **mai** valutato su Panama o su unadjusted in fase di valutazione-segnale (sarebbe override della metodologia).

   > **DOMANDA DI METODOLOGIA APERTA (dall'audit, NON-BLOCCANTE) — seam train/runtime sulle distanze assolute.** Le distanze assolute (zona ±40, target, stop, **floor 80pt**) sono valutate **su ratio in training** (inv.7a, metodologia) ma **su unadjusted al runtime** (CN-9.16). Per una soglia *assoluta* in punti, ratio e unadjusted differiscono per il fattore cumulato di roll: "80 punti" su ratio ≠ 80 punti reali per le barre storiche lontane dall'ancora. La metodologia ha scelto ratio per la valutazione-segnale; il piano la **rispetta** (non la inverte). **Se** questo seam sia materiale rispetto a research=runtime (NFR-9.2) è una **domanda per il track Metodologia / AC**, non risolta qui. **M4 done-when misura il seam** (80pt valutato in replay-training vs runtime sulla stessa barra) e lo **riporta** come diagnostico, senza deciderlo.

---

## 4. Sequenza di build (single-task, una card alla volta)

**Gate-dati (radice):** Fase B in poi gated sull'arrivo dei **2 tape Portara** (pagati + in jobs list, consegna ~24h). **Fase A costruibile ORA** — M0 sul sample ISP (**previa verifica presenza**), M1/M2 su fixture. Non si blocca lo sviluppo sul dataset completo.

- **Fase A — Nucleo-contratto (ora, senza tape pagato):**
  1. **M0** loader + schema + (sul sample) struttura serie/colonne. *(Sblocca tutto a valle; schema = contratto condiviso M3/M8b; inv.7 si fissa qui; il caricamento delle 2 serie reali + cross-check si chiude a consegna del tape.)*
  2. **M1** payload + invarianti. 3. **M2** state-machine + lifecycle + submacchina.
- **Track-dati parallelo (sblocca dopo M0, NON gated su bundle):**
  - **M8a** Directa data-layer. **Codice** costruibile dopo M0 (fixture DIRECTA già in repo). **Run live** = job post-22:00, gated D-6 (niente DGo/TradingView su B6086); accumula il forward (perituro dopo fine tape) e backfilla i ~100gg dalla 10003. *Da avviare appena scelta la root (b) e verificato D-6.*
- **Fase B — Motore (gated: 2 tape + M0 chiusa):** 4. **M3** (ratio). 5. **M4** (emissione/80pt su serie eval=ratio).
- **Fase C — Ottimizzazione (gated: pipeline replayabile su storico):** 6. **M5** GA core (AWS). 7. **M6** frozen bundle.
- **Fase D — Validazione (gated: bundle esistente):** 8. **M7** validator (audit € su Panama) → GO/NO-GO. *(In panchina finché M6 non produce un bundle.)*
- **Fase E — Forward-run (gated: bundle + DAPI + probe):** 9. **M8b** inference adapter. 10. **M9** Telegram. 11. **M10** audit (accanto a M8a/M8b).

L'ordine in Fase A fra M0 e M1/M2 non è forzato dalle dipendenze (M1/M2 fixture-testabili). Si parte da M0 perché è l'unblock corrente e fissa schema-contratto + inv.7.

---

## 5. Perimetro

**IN (build PHASE-1):** M0, M1, M2, M3, M4, M5, M6, M7, **M8a, M8b**, M9, M10 — FIB-only.

**OUT:**
- **XGBoost = progetto separato** (consumatore read-only dell'archivio (b)). Non governato da questo piano né dalla metodologia ga-zone-engine; nessun suo requisito entra qui. *(AUDIT-3: provenienza esterna, correttamente esclusa.)*
- Layer covarianza cross-index / DCC-ADCC-cDCC, `S_xidx`, 5ª famiglia target → **PHASE-2** (R-10.1, CN-10.1/.2, R-10.9). Dati cross-index futures pluriennali (FDAX/FESX/ES) → PHASE-2 (preventivo Arthur acquisito, **non comprato**).
- Soglie congelate di Parte V ($N_{pivot}$, $\tau_{vol}/\tau_{liq}/\tau_{dist}^\sigma$, timer, 80pt) → **consumate**, non ri-derivate.
- Verdetti/valori d'edge → **M7/validator/FASE-D**, PENDING-empirico.
- Dipendenze aperte Sez.13 ($L_{max}$, $\theta_{reconcile}$, param tuning, lookup codici mese oltre F/I, abilitazione FDAX, vendor cross-index) → FASE-D / monitoring. **Flag, non bloccanti.**
- Riavvio Darwin a mezzanotte, migrazione formato legacy→esteso → FASE-D.

**Archivio (b) — placement (claim repo da verificare, AUDIT-3):**
- Root **neutra condivisa, FUORI da entrambi i repo** (ga-zone-engine e XGBoost). Struttura R-9.35 invariata: `<root>/exports/directa_history/<TICKER>_<START>_<END>/`.
- **Scrittore unico** = M8a. Progetti consumatori **read-only**. Scrittura **append-only versionata** (CN-9.22: no-op se identico, nuova versione se divergente, mai sovrascrittura). Copie per-modello **derivate e rigenerabili**, mai a mano → zero drift.
- **Migrazione** dei file `directa_history` attualmente in-repo → root (b): una-tantum, parte di M8a *(conteggio "2340" da verificare)*.
- È **placement**, non modifica spec: struttura R-9.35 e muro feature/gating invariati.

---

## 6. Done-per-milestone & citazione (GC-1, GC-2, GC-3, GC-4)

- **Done-when (test-based, GC-1):** per ogni modulo la sua suite passa + comportamento = requisiti citati + **0 regressioni** sulla suite cumulativa (vincolante da M1 in poi; M0 primo task, porta la sua suite, nessuna baseline).
  - **M0 done-when**: le 2 serie consegnate caricate + la 3ª derivata, instradate ai consumatori (inv.7); **cross-check ratio-consegnata vs ricostruita** (diff ≤ tolleranza dichiarata, marker su scostamento); filtro righe settle (vol 0) + diagnostico fuori-calendario; diagnostico tick-grid (% O/H/L/C ÷5 per anno/contratto); column-tolerance verificata su sample ISP (9-col) e, a consegna, su tape Portara.
  - **M4 done-when**: 80pt valutato sulla **serie di valutazione-segnale (ratio)** (inv.7a); **diagnostico seam** train(ratio)/runtime(unadjusted) sull'80pt riportato (§3 nota), non deciso.
  - **M7 done-when**: audit monetario su serie **Panama** (inv.7b), 5€/pt scala originale.
  - **M8a done-when**: riconciliazione end-of-day (schema 13-campi + 840 timestamp + monotonia, R-9.31, marker `RECONCILE_SCHEMA_FAIL`); scrittura archivio append-only versionata (CN-9.22) su root (b).
- **Citazione (GC-2):** ogni modulo cita la fonte come da §1/tabella. Niente comportamento del motore giustificato dalla spec; niente convenzione-prezzo implicita; **niente inversione della mappatura metodologica**.
- **Fixture (GC-3):** **Fixture M0** = sample ISP/Portara ridotto. **Fixture M8a** = catture `source=DIRECTA` — NON input di M0. Mai tape-pagato né pull DAPI live nei test.
- **Lettura (GC-4):** spec/CAP letti per range mirato, mai dump integrale; ogni card cita le righe lette.
- **Review:** code-review CLI/RM-2 = gira i test + legge il diff, verdetto sul comportamento (mai verdetto d'edge — quello è M7).

---

## 7. Prerequisiti non-bloccanti il build core (da non perdere)

- **Probe DAPI** prima del forward-run live (Fase E), batch unico gated D-6: **V-2** (finestra 100gg cal vs trading), **V-3** (rollover/`CONTRACT_SWITCH` a scadenza reale), **SOB/EOB** (bar-stamp DAPI da riconciliare col tape Portara; se EOB, shift 1-min al seam). Mordono solo alla cucitura storico↔live.
- **Run live di M8a** (job post-22:00): gated D-6. Serve solo la root (b) decisa.
- **Domanda di metodologia — seam 80pt ratio/unadjusted** (§3 nota): da girare al track Metodologia / AC. Non blocca il build (il piano segue la metodologia); M4 la misura.
- **5 PENDING-empirico** da B6 (codici mese Mar/Dic; PRICE f5/f7; ticker 1030; riavvio mezzanotte) → runtime-discovery/FASE-D.
- **`rm_guard` fix** (A-1/D-14) → track Metodologia, separato.
- **Verifica sample ISP**: confermare presenza su disco (incl. `Downloads`) o ri-scaricare, prima che M0 parta.

---

## 8. Avvertenza di confine

Questo piano fissa **architettura, sequenza, perimetro, done-per-milestone, fonte-per-modulo, mappatura-prezzo (inv.7)**. Non disegna governance di processo non richiesta (gli organi crescono dagli incidenti — GOV-CODICE-01). Il dettaglio implementativo per-modulo (funzioni, file, schema test, formato colonne ritenute) scende **dal** piano via `ISTRUZIONI_*.md` per-modulo in `Codice/Programma/Istruzioni/`, una card alla volta, **dopo la ratifica**.
