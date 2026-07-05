# PIANO_FASE_CODICE_01 — Piano di lavoro della fase-codice (FASE-D)

> **Stato:** BOZZA per audit ostile. **Non ratificato.** Dopo audit (Claude.ai, GOV-CARDAUDIT-01) + ratifica AC → commit in `Codice/Piano_di_lavoro/` e diventa il **piano ufficiale unico**.
> **Derivazione:** dai 375 requisiti di `docs/spec_funzionale/SPEC_FUNZ_01.md` (Sez.1–10) + confine Sez.12/13. RM-2: ogni asserzione di stato-repo va verificata sul repo, il repo vince.
> **Cosa NON è:** non è una task-card, non è l'implementazione, non fissa i dettagli per-modulo. Quelli scendono **dal** piano via `ISTRUZIONI_*.md` per-modulo, uno alla volta.

---

## 1. Inquadramento — chi governa cosa (cardine GC-2)

La spec è la **vista-prodotto/contratto**; la matematica del motore è nei **CAP** (Sez.12 lo dichiara esplicitamente). La fonte-di-verità è quindi **doppia** e va dichiarata per ogni modulo:

- **Contratto (governato da SPEC_FUNZ_01)**: schema-dato canonico, payload, state-machine, regola di emissione, consegna, runtime DAPI, gate di go-live, audit. Si cita `R-*/CN-*/NFR-*`.
- **Motore (governato dai CAP, non in spec)**: feature engineering + pivot (Parte III, Cap.12–15), derivazione geometrica zone/target/stop (Parte IV, Cap.16–21), GA/NSGA-II/fitness/walk-forward + valori-soglia congelati (Parte V, Cap.22–26), matematica dei gate statistici (Parte VII). Si cita `CAP_*` `path:line` (RM-2).

Una card-modulo che fissa un comportamento del motore citando la spec (che non lo contiene) è un bug di fonte. Una card del contratto che inventa un valore-soglia congelato in Parte V è scope-creep.

---

## 2. Architettura — DAG dei moduli

Spina di dipendenza (freccia = "dipende da"). È la **catena di build**, distinta dal data-flow di runtime.

```
                 ┌─────────────────────────────────────────────┐
   M0 Data ──────┤ schema canonico 13-campi (contratto condiviso)│
   layer         └───────┬──────────────────────────┬───────────┘
   (tape)                │                            │
                         ▼                            ▼
   M1 Payload ─▶ M2 State-machine            M3 Feature eng. ─▶ M4 Signal
   (puro)        & lifecycle                 (pivot/EGARCH/      construction
                 (fixture)                    regime, da CAP)    + emissione
                                                   │                 │
                                                   └──────┬──────────┘
                                                          ▼
                                                   M5 GA core ─▶ M6 Frozen bundle
                                                   (NSGA-II,       (immutabile,
                                                    walk-fwd)       SHA-256)
                                                          │
                                                          ▼
                                                   M7 Validator  (in panchina:
                                                   (DSR/PBO/OOS    presuppone M6)
                                                    → GO/NO-GO)
                                                          │
                          ┌───────────────────────────────┼───────────────┐
                          ▼                                ▼               ▼
                   M8 Runtime DAPI               M9 Telegram        M10 Audit
                   adapter + recovery            delivery           (append-only,
                   + riconciliazione             (9 campi, 3 notif) trasversale)
```

### Tabella moduli

| ID | Modulo | Cosa costruisce (sintesi) | Fonte-di-verità | Dipende da | Costruibile **ora**? |
|---|---|---|---|---|---|
| **M0** | Data layer (training tape) | Loader Portara CSV → griglia 1-min canonica 13-campi (forward-fill, `bar_synthetic`=trade/no-trade, `tick_count`, `source`) | Schema: Sez.9 (CN-9.5/.6/.7/.8/.9). Back-adjust/roll/pre-expiry: **CAP Parte 8** (Cap.38/39/40). Precondizione: R-2.7, R-5.3 | — | **Sì** (sul sample ISP) |
| **M1** | Payload & invarianti | Tupla `S` 12 campi, domini, invarianti geometrici (`d_stop>b`, multipli di 5, ordinamento target), immutabilità, segnale-unico-attivo | Sez.3 (R-3.1..37, CN-3.1..5) | — | **Sì** (fixture) |
| **M2** | State-machine & lifecycle | 1 stato non-terminale + 6 terminali, transizioni, precedenza eventi, raw touch, timer pre/post-trigger, submacchina posizione | Sez.4 (R-4.1..48, CN-4.1..12) | M1 | **Sì** (fixture: sequenze barre sintetiche) |
| **M3** | Feature engineering | Pivot detection, catalogo 37 feature causali, EGARCH, classificazione regime; regole consumo per-categoria | **CAP Parte III** (Cap.12–15). Consumo: Sez.9 (R-9.38..42) | M0 | No (serve dato reale) |
| **M4** | Signal construction + emissione | Derivazione `entry_zone`/`target_1`/`target_2`/`stop_loss` + tipi; regola di emissione (3 condizioni + filtro 80pt, AND) | Derivazione: **CAP Parte IV** (Cap.16–21). Emissione: Sez.5 (R-5.1..16, CN-5.1..5) | M3, M1 | No |
| **M5** | GA core | Cromosoma, NSGA-II, fitness multi-obiettivo, walk-forward nested (purge/embargo) | **CAP Parte V** (Cap.22–26) | M0–M4 | No (AWS) |
| **M6** | Frozen bundle | Artefatto immutabile a 6 elementi, hash SHA-256, verifica-su-load fail-stop | Sez.8 (CN-8.3/.4/.5, R-8.24/.36) + Cap.35 | M5 | No |
| **M7** | Validator | Aggregazione OOS, DSR, PBO via CSCV, bootstrap stazionario, 12 criteri go-live → GO/NO-GO | Sez.8 (R-8.1..38, CN-8.1..7) + matematica **Parte VII** | M6 | No (**in panchina**) |
| **M8** | Runtime DAPI adapter + recovery | Connessione DAPI (porte 10001/10003, mai 10002), adapter DAPI→bundle, warm-up, gap-recovery, riconciliazione, archivio, gating cash | Sez.7 (R-7.1..20, CN-7.1..9) + Sez.9 (R-9.1..43, CN-9.1..25) + CAP Parte 9/10 | M0 (schema), M6 (bundle) | No (prereq. probe) |
| **M9** | Telegram delivery | Messaggio 9 campi mobile-first, 3 notifiche standard, retry/backoff, anti-duplicato persistito | Sez.6 (R-6.1..24, CN-6.1..9) + Appendice E (FASE-D) | M2 (eventi), M8 | No |
| **M10** | Audit & compliance | Log JSONL append-only immutabile, marker per-stato, retention 90gg rolling + permanente per segnali emessi | Sez.7.5 (NFR-7.3..7, R-7.18..20) | trasversale (M8/M9) | No |

---

## 3. Invarianti trasversali (ogni modulo li preserva)

1. **research = runtime** (NFR-9.2): il preprocessor di training (M0/M3) e l'adapter runtime (M8) producono lo **stesso** schema canonico; la **stessa** computazione delle feature gira identica su tape storico e griglia live. Lo schema 13-campi di M0 è **il contratto** su cui poggiano M3 e M8.
2. **replay bit-exact** (NFR-9.1, NFR-8.1, CN-4.5): precedenza eventi deterministica, nessun non-determinismo. Due replay sulla stessa finestra → stessa sequenza di emissioni/`signal_id`/transizioni/timestamp.
3. **immutabilità del bundle** (CN-8.3/.4/.5): il bundle è hashato (SHA-256), riverificato a ogni load; hash discordante → la pipeline **rifiuta di girare**.
4. **solo emissione, nessuna esecuzione** (CN-1.1, CN-7.1): porta ordini **10002 mai aperta**; il sistema pubblica segnali, l'operatore esegue a mano.
5. **edge = esclusiva del validator, PENDING** (cardine Sez.8): **nessun modulo** asserisce GO/NO-GO né valori d'edge (DSR/PBO/`E[R_net]`/CVaR/MDD effettivi). Solo M7 li emette, in FASE-D. Verbi vietati ("supera il gate", "edge confermato", "GO") fuori da M7.
6. **PHASE-1 FIB-only** (R-10.1, CN-10.1/.2): nessun layer di covarianza cross-index in questo build.

---

## 4. Sequenza di build (single-task, una card alla volta)

**Gate-dati (radice):** Fase B in poi è gated sull'arrivo del tape Portara (acquisto in corso). **Fase A è costruibile ORA** (M0 sul sample ISP gratuito; M1/M2 su fixture). Non si blocca lo sviluppo sul dataset completo.

- **Fase A — Nucleo-contratto (ora, senza tape):**
  1. **M0** loader + schema canonico, validato sul sample ISP. *(Sblocca tutto a valle; lo schema è contratto condiviso M3/M8.)*
  2. **M1** payload + invarianti. *(Oggetto referenziato da tutto il downstream.)*
  3. **M2** state-machine + lifecycle + submacchina.
- **Fase B — Motore (gated: tape + M0 chiusa):**
  4. **M3** feature engineering (pivot/EGARCH/regime). 5. **M4** signal construction + emissione.
- **Fase C — Ottimizzazione (gated: pipeline replayabile su storico):**
  6. **M5** GA core (AWS). 7. **M6** frozen bundle.
- **Fase D — Validazione (gated: bundle addestrato esistente):**
  8. **M7** validator → GO/NO-GO. *(In panchina finché M6 non produce un bundle.)*
- **Fase E — Forward-run (gated: bundle + DAPI + probe prerequisite):**
  9. **M8** runtime adapter + recovery. 10. **M9** Telegram. 11. **M10** audit (costruito accanto a M8).

L'ordine in Fase A fra M0 (dato) e M1/M2 (logica pura) **non è forzato dalle dipendenze** — M1/M2 sono fixture-testabili senza tape. Si parte da **M0** perché è l'unblock corrente e fissa lo schema-contratto; M1/M2 si interfogliano subito dopo.

---

## 5. Perimetro

**IN (build PHASE-1):** M0–M10, FIB-only.

**OUT:**
- Layer covarianza cross-index / DCC-ADCC-cDCC, `S_xidx`, 5ª famiglia target → **PHASE-2** (R-10.1, CN-10.1/.2, R-10.9). Dati cross-index futures pluriennali → PHASE-2.
- Valori-soglia congelati di Parte V ($N_{pivot}$, $\tau_{vol}/\tau_{liq}/\tau_{dist}^\sigma$, valori timer, 80pt) → **consumati** dai moduli, non ri-derivati.
- Verdetti/valori d'edge → **M7/validator/FASE-D**, PENDING-empirico.
- Dipendenze aperte Sez.13 (latenza $L_{max}$ Telegram, $\theta_{reconcile}$, 10 param tuning, lookup codici mese oltre F/I, abilitazione FDAX, vendor cross-index) → FASE-D / monitoring post-go-live. **Flag, non bloccanti il build core.**
- Riavvio Darwin a mezzanotte, migrazione formato legacy→esteso dei dump → FASE-D.

---

## 6. Done-per-milestone & citazione (GC-1, GC-2, GC-3)

- **Done-when (test-based, GC-1):** per ogni modulo, la sua suite passa + il comportamento combacia coi requisiti citati + **0 regressioni** sulla suite cumulativa (vincolante da M1 in poi; M0 è il primo task, porta la sua suite e non ha baseline).
- **Citazione (GC-2):** ogni modulo cita la propria fonte come da §1/tabella — `R-*/CN-*/NFR-*` per il contratto, `CAP_* path:line` per il motore. Niente comportamento del motore giustificato dalla spec.
- **Fixture (GC-3):** test su fixture committate (sample ISP ridotto, sequenze barre sintetiche). Mai tape-pagato né pull DAPI nei test.
- **Review:** code-review CLI/RM-2 = gira i test + legge il diff, verdetto sul comportamento (mai verdetto d'edge — quello è M7).

---

## 7. Prerequisiti non-bloccanti il build core (da non perdere)

- **Probe DAPI** prima del forward-run live (Fase E, **non** prima del training): **V-2** (finestra 100gg calendario vs trading), **V-3** (rollover/`CONTRACT_SWITCH` a scadenza reale), **SOB/EOB** (convenzione bar-stamp DAPI da riconciliare col tape Portara). Batch unico, gated D-6. Mordono solo alla cucitura storico↔live, non a monte.
- **5 PENDING-empirico** da B6 (codici mese Mar/Dic; PRICE f5/f7; ticker 1030; riavvio mezzanotte) → runtime-discovery/FASE-D.
- **`rm_guard` fix** (A-1/D-14) → track Metodologia, separato da questo piano.

---

## 8. Avvertenza di confine

Questo piano fissa **architettura, sequenza, perimetro, done-per-milestone, fonte-per-modulo**. Non disegna a tavolino governance di processo non richiesta (gli organi-processo crescono dagli incidenti — GOV-CODICE-01). Il dettaglio implementativo di ciascun modulo (funzioni, file, schema test) scende **dal** piano via `ISTRUZIONI_*.md` per-modulo in `Codice/Programma/Istruzioni/`, una card alla volta, dopo la ratifica di questo piano.
