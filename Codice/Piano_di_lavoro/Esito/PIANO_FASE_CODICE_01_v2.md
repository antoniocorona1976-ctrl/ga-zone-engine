# PIANO_FASE_CODICE_01 — Piano di lavoro della fase-codice (FASE-D) — **v2 riconciliato**

> **Stato:** BOZZA v2 per **ratifica AC**. Audit ostile completato (Planner / Claude.ai, 2026-06-30). Dopo ratifica AC → commit in `Codice/Piano_di_lavoro/` e diventa il **piano ufficiale unico**.
> **Derivazione:** dai 375 requisiti di `docs/spec_funzionale/SPEC_FUNZ_01.md` (Sez.1–10) + confine Sez.12/13 + matematica del motore nei CAP della metodologia v2. RM-2: ogni asserzione di stato-repo va verificata sul repo, il repo vince.
> **Cosa NON è:** non è una task-card, non è l'implementazione, non fissa i dettagli per-modulo. Quelli scendono **dal** piano via `ISTRUZIONI_*.md` per-modulo, uno alla volta, dopo la ratifica.

## Changelog v1 → v2 (mapping ai finding d'audit)

| Finding | Severità | Modifica in v2 |
|---|---|---|
| **B1** | BLOCCANTE | §3 nuovo invariante 7 — convenzione back-adjustment **per-consumatore** (ratio→feature, unadjusted/punti-reali→geometria 80pt, additivo→audit), cita CN-9.16/CN-5.2/riga 1486. M0 dichiara la convenzione e ritiene le tre rappresentazioni. |
| **B2** | BLOCCANTE | Header — rimosso il gate morto `GOV-CARDAUDIT-01` (chiuso oggi, commit 8417bfd); ratifica via audit-Planner corrente. |
| **A1** | ALTO | §2/§4 — **M8 splittato**: M8a (acquisizione/archivio/riconciliazione, dipende M0, è il job post-22:00) + M8b (adapter d'inferenza, Fase E, dipende M6). |
| **A2** | ALTO | §2/§3/§6 — M0 carica **entrambe** le serie; M7 consuma l'additiva per l'audit monetario (prescrizione metodologica Panama-additivo). Additiva = usata, non ridondante. |
| **M1** | MEDIO | §2/§4 — "M0 costruibile ora" condizionato a **verifica presenza sample ISP** (RM-2: non trovato in repo+Documents dall'inventario). |
| **M2** | MEDIO | §2/§5 — archivio (b): root neutra **fuori da entrambi i repo**, scrittore unico, append-only versionato (CN-9.22); migrazione dei 2340 file `directa_history` in-repo. |
| **M3** | MEDIO | §2/§6 — fixture su disco sono `source=DIRECTA` → fixture di **M8a**, non di M0; fixture M0 = sample ISP/Portara. |
| **L1** | BASSO | §3 invariante 6 — "FIB-only" scoped al **motore** (feature/GA), non all'archivio/gating (cash ammessi per gating). |
| **L2** | BASSO | §2 — DAG/tabella allineati: M8b dipende da M6 (build), il GO di M7 è gate di go-live, non dipendenza. |
| **L3** | BASSO | §5 OUT — **XGBoost = progetto separato** (consumatore dell'archivio (b), non governato qui). |

---

## 1. Inquadramento — chi governa cosa (cardine GC-2)

La spec è la **vista-prodotto/contratto**; la matematica del motore è nei **CAP** (Sez.12 lo dichiara esplicitamente). La fonte-di-verità è **doppia** e va dichiarata per ogni modulo:

- **Contratto (governato da SPEC_FUNZ_01)**: schema-dato canonico, payload, state-machine, regola di emissione, consegna, runtime DAPI, gate di go-live, audit. Si cita `R-*/CN-*/NFR-*`.
- **Motore (governato dai CAP, non in spec)**: feature engineering + pivot (Parte III, Cap.12–15), derivazione geometrica zone/target/stop (Parte IV, Cap.16–21), GA/NSGA-II/fitness/walk-forward + valori-soglia congelati (Parte V, Cap.22–26), matematica dei gate (Parte VII), **back-adjustment/roll/pre-expiry** (Parte 8, Cap.38/39/40). Si cita `CAP_* path:line` (RM-2).

> **Caso speciale — convenzione di prezzo (B1):** la *convenzione di back-adjustment* è governata dai CAP Parte 8 **e** dal contratto (CN-9.16 fissa runtime=unadjusted / training=ratio come hard-lock, riga 1486). È quindi materia di entrambe le fonti e va dichiarata esplicitamente in M0 (§3, invariante 7).

Una card-modulo che fissa un comportamento del motore citando la spec (che non lo contiene) è un bug di fonte. Una card del contratto che inventa un valore-soglia congelato di Parte V è scope-creep.

---

## 2. Architettura — DAG dei moduli

Spina di dipendenza (freccia = "dipende da"). Catena di **build**, distinta dal data-flow di runtime.

```
                 ┌──────────────────────────────────────────────────┐
   M0 Data ──────┤ schema canonico 13-campi (contratto condiviso)   │
   layer         │ + 3 rappresentazioni prezzo (ratio/unadj/addit.) │
   (tape)        └──────┬───────────────────┬───────────────┬───────┘
                        │                   │               │
                        ▼                   ▼               ▼
   M1 Payload ─▶ M2 State-machine   M3 Feature eng.   M8a Directa data-layer
   (puro)        & lifecycle        (ratio: pivot/     (acquis. + archivio (b)
                 (fixture)           EGARCH/regime)     + riconcil. end-of-day)
                                          │             [dip. M0 — JOB post-22:00,
                                          ▼              NON gated su bundle]
                                   M4 Signal constr.          │
                                   + emissione                │
                                   (unadj/punti: 80pt)        │
                                          │                   │
                                          ▼                   │
                                   M5 GA core ─▶ M6 Frozen     │
                                   (NSGA-II)      bundle (SHA) │
                                          │         │         │
                                          ▼         ▼         │
                                   M7 Validator   M8b Runtime  │
                                   (additivo:      inference   │
                                    audit € →       adapter ◀──┘
                                    GO/NO-GO)      [dip. M0+M6+M8a]
                                   (in panchina)         │
                                                  ┌──────┴──────┐
                                                  ▼             ▼
                                              M9 Telegram   M10 Audit
                                              (9 campi)     (append-only,
                                              [dip. M2,M8b]  trasversale)
```

### Tabella moduli

| ID | Modulo | Cosa costruisce (sintesi) | Fonte-di-verità | Dipende da | Costruibile **ora**? |
|---|---|---|---|---|---|
| **M0** | Data layer (training tape) | Loader **due serie Portara** (ratio + additivo), ciascuna con `unadjustedClose`+roll-cols → griglia 1-min canonica 13-campi (convenzione runtime=unadjusted) + **ritenzione** ratio/additivo/roll-log instradati ai consumatori (inv.7). Filtro righe settle (volume 0 + diagnostico) + diagnostico tick-grid. Column-tolerant. | Schema: Sez.9 (CN-9.5/.6/.7/.8/.9). Convenzione: **CN-9.16**, CN-5.2. Back-adjust/roll/pre-expiry: **CAP Parte 8** (Cap.38/39/40). Precond.: R-2.7, R-5.3 | — | **Sì, se** sample ISP presente (M1-audit: **da verificare**) |
| **M1** | Payload & invarianti | Tupla `S`, domini, invarianti geometrici (`d_stop>b`, multipli di 5, ordinamento target), immutabilità, segnale-unico-attivo | Sez.3 (R-3.1..37, CN-3.1..5) | — | **Sì** (fixture) |
| **M2** | State-machine & lifecycle | 1 stato non-terminale + 6 terminali, transizioni, precedenza eventi, raw touch, timer pre/post-trigger, submacchina posizione | Sez.4 (R-4.1..48, CN-4.1..12) | M1 | **Sì** (fixture) |
| **M3** | Feature engineering | Pivot detection, 37 feature causali, EGARCH, classificazione regime — **su serie ratio** (inv.7a) | **CAP Parte III** (Cap.12–15). Consumo: Sez.9 (R-9.38..42) | M0 | No (dato reale) |
| **M4** | Signal construction + emissione | Derivazione `entry_zone`/`target_*`/`stop_loss` + tipi; regola emissione (3 cond. + **filtro 80pt su punti reali**, AND) | Derivazione: **CAP Parte IV** (Cap.16–21). Emissione: Sez.5 (R-5.1..16, CN-5.1..5). Punti: inv.7b | M3, M1 | No |
| **M5** | GA core | Cromosoma, NSGA-II, fitness multi-obiettivo, walk-forward nested (purge/embargo) — **su ratio** | **CAP Parte V** (Cap.22–26) | M0–M4 | No (AWS) |
| **M6** | Frozen bundle | Artefatto immutabile 6 elementi, hash SHA-256, verifica-su-load fail-stop | Sez.8 (CN-8.3/.4/.5, R-8.24/.36) + Cap.35 | M5 | No |
| **M7** | Validator | Aggregazione OOS, DSR, PBO via CSCV, bootstrap; **audit monetario (E[R_net]/CVaR/MDD in €) su serie additiva** (inv.7c); 12 criteri → GO/NO-GO | Sez.8 (R-8.1..38, CN-8.1..7) + matematica **Parte VII** | M6 | No (**in panchina**) |
| **M8a** | **Directa data-layer** | Acquisizione DAPI (pull storico **10003** post-chiusura + cattura realtime **10001**, mai 10002), riconciliazione end-of-day (840 barre, schema 13-campi), **archivio (b)** append-only versionato, logging cash. **È il job post-22:00.** | Sez.7 (R-7.2/.14/.15) + Sez.9 (R-9.30/.31/.35/.36, CN-9.16/.22) | **M0 (schema)** | **Codice sì** (su fixture DIRECTA); **run live** gated D-6 |
| **M8b** | **Runtime inference adapter** | Adapter DAPI→bundle (R-9.1, stesso schema operativo), warm-up, gap-recovery runtime, gating qualitativo sul payload | Sez.7 (R-7.1..20, CN-7.1..9) + Sez.9 (R-9.1..43) + CAP Parte 9/10 | M0, **M6**, M8a | No (prereq. probe + bundle) |
| **M9** | Telegram delivery | Messaggio 9 campi mobile-first, 3 notifiche, retry/backoff, anti-duplicato persistito | Sez.6 (R-6.1..24, CN-6.1..9) + Appendice E | M2, **M8b** | No |
| **M10** | Audit & compliance | Log JSONL append-only immutabile, marker per-stato, retention 90gg rolling + permanente per segnali emessi | Sez.7.5 (NFR-7.3..7, R-7.18..20) | trasversale (M8a/M8b/M9) | No |

> **Dati Portara in acquisto (in consegna ~24h):** 2 serie continue (ratio + additivo), settle-based, 1995→date, 1-min, 12 colonne + `unadjustedClose`/`spread`/`cumulativeSpread`/`contractName`/`tickcount` + roll-log. M0 column-tolerant finché il tape pagato non è su disco e verificato.

---

## 3. Invarianti trasversali (ogni modulo li preserva)

1. **research = runtime** (NFR-9.2): preprocessor di training (M0/M3) e adapter runtime (M8b) producono lo **stesso schema** canonico 13-campi; stessa computazione feature su tape storico e griglia live. Lo schema 13-campi di M0 è **il contratto** su cui poggiano M3 e M8b.
2. **replay bit-exact** (NFR-9.1, NFR-8.1, CN-4.5): precedenza eventi deterministica; due replay sulla stessa finestra → stessa sequenza emissioni/`signal_id`/transizioni/timestamp.
3. **immutabilità del bundle** (CN-8.3/.4/.5): bundle hashato SHA-256, riverificato a ogni load; hash discordante → la pipeline **rifiuta di girare**.
4. **solo emissione, nessuna esecuzione** (CN-1.1, CN-7.1): porta ordini **10002 mai aperta**; il sistema pubblica segnali, l'operatore esegue a mano.
5. **edge = esclusiva del validator, PENDING** (Sez.8): **nessun modulo** asserisce GO/NO-GO né valori d'edge. Solo M7, in FASE-D. Verbi vietati ("supera il gate", "edge confermato", "GO") fuori da M7.
6. **PHASE-1 FIB-only — scope del MOTORE** (R-10.1, CN-10.1/.2): nessun layer di covarianza cross-index nel **feature tensor / cromosoma / walk-forward**. Lo scope "FIB-only" è del motore, **NON dell'archivio**: M8a logga e archivia anche i cash europei (DGER/DSTX50/DITAS/DFRA) per il **solo gating qualitativo** (R-7.15, CN-7.8), che resta fuori dal feature tensor. Archivio multi-strumento, motore single-instrument.
7. **Convenzione di back-adjustment per-consumatore — blinda CN-5.2 (B1).** Il prezzo FIB esiste in **tre rappresentazioni**, ciascuna con consumatore esclusivo; nessun modulo le confonde:
   - **(a) ratio-adjusted** (continua sui roll, scale-invariant) → **feature/GA** (M3, M5): volatilità, regime, rendimenti. Convenzione di training **hard-locked** (CN-9.16, riga 1486).
   - **(b) unadjusted / punti reali** (prezzo nativo del front-month, colonna `unadjustedClose`) → **geometria** (M4): zona ±40pt, target/stop in punti e in particolare il **filtro 80pt**. Convenzione runtime (CN-9.16). Il filtro 80pt (R-5.9/.10, **CN-5.2 — floor assoluto, mai allentabile dal cromosoma**) si valuta **esclusivamente su punti reali**: valutarlo su serie ratio violerebbe CN-5.2 **silenziosamente** (il numero "80" resterebbe, misurato col righello sbagliato).
   - **(c) additivo / Panama** (continua in punti assoluti) → **audit monetario** (M7): E[R_net], CVaR, MDD in euro, su serie continua (prescrizione metodologica Panama-additivo).
   
   M0 produce lo schema canonico 13-campi nella **convenzione runtime (unadjusted)** e **ritiene** accanto le rappresentazioni ratio e additiva + roll-log, instradandole ai rispettivi consumatori. *Una card che calcola l'80pt su prezzi ratio è un bug di correttezza, non di stile.*

---

## 4. Sequenza di build (single-task, una card alla volta)

**Gate-dati (radice):** Fase B in poi è gated sull'arrivo del **tape Portara** (acquisto: pagato + in jobs list, consegna ~24h). **Fase A è costruibile ORA** — M0 sul sample ISP (**previa verifica presenza**, M1-audit), M1/M2 su fixture. Non si blocca lo sviluppo sul dataset completo.

- **Fase A — Nucleo-contratto (ora, senza tape pagato):**
  1. **M0** loader + schema canonico + 3 rappresentazioni, validato sul sample ISP. *(Sblocca tutto a valle; lo schema è contratto condiviso M3/M8b; l'inv.7 si fissa qui.)*
  2. **M1** payload + invarianti. 3. **M2** state-machine + lifecycle + submacchina.
- **Track-dati parallelo (sblocca dopo M0, NON gated su bundle):**
  - **M8a** Directa data-layer. **Codice** costruibile dopo M0 (test su fixture DIRECTA già in repo). **Run live** = il **job post-22:00**, gated D-6 (niente DGo/TradingView su B6086). Il suo run accumula il **forward** (perituro dopo la fine del tape) e backfilla i ~100gg dalla 10003. *Da avviare appena scelta la root (b) e verificato D-6.*
- **Fase B — Motore (gated: tape + M0 chiusa):** 4. **M3** (ratio). 5. **M4** (emissione, 80pt su punti reali).
- **Fase C — Ottimizzazione (gated: pipeline replayabile su storico):** 6. **M5** GA core (AWS). 7. **M6** frozen bundle.
- **Fase D — Validazione (gated: bundle esistente):** 8. **M7** validator (audit € su additivo) → GO/NO-GO. *(In panchina finché M6 non produce un bundle.)*
- **Fase E — Forward-run (gated: bundle + DAPI + probe prerequisite):** 9. **M8b** inference adapter. 10. **M9** Telegram. 11. **M10** audit (accanto a M8a/M8b).

L'ordine in Fase A fra M0 e M1/M2 non è forzato dalle dipendenze (M1/M2 fixture-testabili). Si parte da M0 perché è l'unblock corrente e fissa lo schema-contratto + l'inv.7.

---

## 5. Perimetro

**IN (build PHASE-1):** M0, M1, M2, M3, M4, M5, M6, M7, **M8a, M8b**, M9, M10 — FIB-only.

**OUT:**
- **XGBoost = progetto separato** (consumatore read-only dell'archivio (b)). Non è governato da questo piano né dalla metodologia ga-zone-engine; nessun suo requisito entra qui. *(L3)*
- Layer covarianza cross-index / DCC-ADCC-cDCC, `S_xidx`, 5ª famiglia target → **PHASE-2** (R-10.1, CN-10.1/.2, R-10.9). Dati cross-index futures pluriennali (FDAX/FESX/ES) → PHASE-2 (preventivo Arthur acquisito, **non comprato**).
- Valori-soglia congelati di Parte V ($N_{pivot}$, $\tau_{vol}/\tau_{liq}/\tau_{dist}^\sigma$, timer, 80pt) → **consumati**, non ri-derivati.
- Verdetti/valori d'edge → **M7/validator/FASE-D**, PENDING-empirico.
- Dipendenze aperte Sez.13 (latenza $L_{max}$, $\theta_{reconcile}$, param tuning, lookup codici mese oltre F/I, abilitazione FDAX, vendor cross-index) → FASE-D / monitoring. **Flag, non bloccanti il build core.**
- Riavvio Darwin a mezzanotte, migrazione formato legacy→esteso dei dump → FASE-D.

**Archivio (b) — decisione di placement (M2):**
- Root **neutra condivisa, FUORI da entrambi i repo** (ga-zone-engine e XGBoost). Struttura R-9.35 invariata sotto: `<root>/exports/directa_history/<TICKER>_<START_YYYYMMDD>_<END_YYYYMMDD>/`.
- **Scrittore unico** = M8a (il job Directa). Entrambi i progetti **read-only**. Scrittura **append-only versionata** (CN-9.22: no-op se identico, nuova versione se divergente, mai sovrascrittura). Copie per-modello **derivate e rigenerabili** dall'archivio, mai a mano → zero drift.
- **Migrazione**: i 2340 file `directa_history` attualmente in-repo (cash, probe gap-recovery) → root (b). Operazione una-tantum, parte di M8a.
- È **placement**, non modifica spec: la struttura R-9.35 e il muro feature/gating restano.

---

## 6. Done-per-milestone & citazione (GC-1, GC-2, GC-3)

- **Done-when (test-based, GC-1):** per ogni modulo la sua suite passa + il comportamento combacia coi requisiti citati + **0 regressioni** sulla suite cumulativa (vincolante da M1 in poi; M0 è il primo task, porta la sua suite, nessuna baseline).
  - **M0 done-when** include: le tre rappresentazioni separate e instradate (inv.7); il filtro righe settle (volume 0) + diagnostico righe volume-0 fuori calendario roll; il diagnostico tick-grid (% O/H/L/C divisibili per 5 per anno/contratto); column-tolerance verificata su sample ISP (9-col) e, a consegna, sul tape Portara (12-col).
  - **M8a done-when** include: riconciliazione end-of-day che verifica schema 13-campi + 840 timestamp attesi + monotonia (R-9.31, marker `RECONCILE_SCHEMA_FAIL`); scrittura archivio append-only versionata (CN-9.22) sulla root (b).
  - **M7 done-when** include: audit monetario su serie **additiva** (inv.7c).
- **Citazione (GC-2):** ogni modulo cita la fonte come da §1/tabella — `R-*/CN-*/NFR-*` per il contratto, `CAP_* path:line` per il motore. Niente comportamento del motore giustificato dalla spec; niente convenzione di prezzo lasciata implicita (inv.7).
- **Fixture (GC-3):** test su fixture committate. **Fixture M0** = sample ISP/Portara ridotto. **Fixture M8a** = catture `source=DIRECTA` (le 18 di `data/runtime/exports_sample/` + probe) — NON sono input di M0. Mai tape-pagato né pull DAPI live nei test.
- **Review:** code-review CLI/RM-2 = gira i test + legge il diff, verdetto sul comportamento (mai verdetto d'edge — quello è M7).

---

## 7. Prerequisiti non-bloccanti il build core (da non perdere)

- **Probe DAPI** prima del forward-run live (Fase E, **non** prima del training), batch unico gated D-6: **V-2** (finestra 100gg calendario vs trading), **V-3** (rollover/`CONTRACT_SWITCH` a scadenza reale), **SOB/EOB** (convenzione bar-stamp DAPI da riconciliare col tape Portara — se DAPI risulta EOB, shift 1-min al seam). Mordono solo alla cucitura storico↔live.
- **Run live di M8a** (job post-22:00): anch'esso gated D-6. Costo zero rispetto al critical path; serve solo la root (b) decisa.
- **5 PENDING-empirico** da B6 (codici mese Mar/Dic; PRICE f5/f7; ticker 1030; riavvio mezzanotte) → runtime-discovery/FASE-D.
- **`rm_guard` fix** (A-1/D-14) → track Metodologia, separato da questo piano.
- **Verifica sample ISP** (M1-audit): confermare presenza su disco (incl. `Downloads`) o ri-scaricare, prima che M0 parta.

---

## 8. Avvertenza di confine

Questo piano fissa **architettura, sequenza, perimetro, done-per-milestone, fonte-per-modulo, convenzione di prezzo (inv.7)**. Non disegna a tavolino governance di processo non richiesta (gli organi-processo crescono dagli incidenti — GOV-CODICE-01). Il dettaglio implementativo di ciascun modulo (funzioni, file, schema test, formato esatto delle colonne ritenute) scende **dal** piano via `ISTRUZIONI_*.md` per-modulo in `Codice/Programma/Istruzioni/`, una card alla volta, dopo la ratifica di questo piano.
