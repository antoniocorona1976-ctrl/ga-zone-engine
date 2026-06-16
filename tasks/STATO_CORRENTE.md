# STATO CORRENTE — ga-zone-engine

> **Single source of truth** dello stato del progetto. Aggiornato all'inizio e alla fine di ogni sessione (web e CLI locale). **Prima azione** di ogni sessione Claude: leggere questo file.

**Marcatori di chiusura (Track A + B — macchina a stati `.claude/CLAUDE.md`)**:
`SPEC-FUNZ-01: CHIUSO PASS ab7450f`
`SPEC-FUNZ-01-B1: CHIUSO PASS 7195ffe`
`SPEC-FUNZ-01-B2: CHIUSO PASS b858a88`
`SPEC-FUNZ-01-B3: CHIUSO PASS e94ef17`
`CAP-01: CHIUSO PASS b76c32c`
`CAP-02: CHIUSO PASS a1625df`
`CAP-03: CHIUSO PASS 1e3172d`
`CAP-04: CHIUSO PASS a1625df`
`CAP-05: CHIUSO PASS 72e00df`
`CAP-06: CHIUSO PASS d3f029d`
`CAP-07: CHIUSO PASS b27c1e3`
`CAP-08: CHIUSO PASS 6ba6186`
`CAP-09: CHIUSO PASS 86425a7`
`CAP-10: CHIUSO PASS 48171e4`

**Aggiornamento 2026-06-16 (CLI, chiusura)**: **SPEC-FUNZ-01-B3 (State-machine & lifecycle del segnale) CHIUSO PASS** — terzo blocco della ricostruzione cieca a 8 blocchi (modalità B). Ciclo completo: mini giro `spec_planner` editoriale (card `rev-B1` `e5dc517`: pin `:127`/`:77` risolti nelle 2 prose stale, decisione AC opzione 2) → `spec_developer` cieco (`89d28b4`, **61 requisiti**: 47 B3-R + 11 B3-CN + 3 B3-NFR, da `CAP_02_parte_II.md` Cap.7 (7.1–7.6) + Cap.11 (11.1–11.5)) → **check post-Developer (6 controlli OK, indice N/A) + boundary-check anti-scope-creep dell'Orchestratore (decisione AC opzione 1+2)**: 3 punti di confine fine girati al Reviewer (B3-R-10 formula invalidazione, B3-R-17 log emissione, B3-CN-09 log submacchina) → **spec_reviewer CLI PASS (`e94ef17`)**: **0 BUG REALE**, floor citazioni 100% token-per-token risolto, **confronto-copertura vs v2 `ab7450f`** (partizione sulla mappa `PROPOSTA_SUDDIVISIONE_SPEC_v2.md`, F-3) = **0 buchi** (6 req. lifecycle Sez.4→Cap.7 tutti coperti, granularità superiore in B3; CN-4.2 persistenza/boot correttamente fuori perimetro→B5; B3 più ricco su Cap.11), cecità preservata (0 ID importati, 0 frasi-firma v2), lista Empirico-CLI VUOTA; i 3 punti di confine tutti senza finding (B3-R-10 verbatim dal CAP). **3 finding non bloccanti**: 1 MIGLIORA PERFORMANCE (B3-CN-09 N1-borderline) + 2 NEUTRO (matrice B3-R-42 puntatori; B3-R-46 rinvio Parte V). **Decisione AC: chiusura diretta** (i 3 finding cosmetici, non instradati). DEV_STATUS azzerato. `00_indice.md` non toccato (N/A). **Nessun M nuovo da B3, nessun M incardinato** (CARRYOVER §2.1: nessun M assegnato a B3). Prossimo: **B4 — Emissione & consegna** (fonte CAP-02 Cap.8 emissione + Cap.9 Telegram; eredita M-2/B-1 latenza Telegram), su decisione AC.
**Aggiornamento 2026-06-16 (CLI)**: **SPEC-FUNZ-01-B3 — card `rev-B` INSTALLATA e seam risolti in CLI**, in attesa di **decisione AC sulla promozione** (avvio Developer). La card B3 (rev-A `24ac6f9`) è stata sottoposta a review di supervisione su Claude.ai → istruzioni `Business Spec/Final/ISTRUZIONI_B3-CARD-UPDATE-01.md`. Eseguito: installata card **rev-B** (chiusi F-1 seam revoked/6.3+citazione+pin, F-2 categoria *valore-di-sistema* per l'invariante di precedenza/determinismo, F-3 autorità di partizione del Reviewer, F-5 carve-out numeri ammessi, F-6 famiglia `B3-NFR`+escape hatch `[B-N PROVVISORIO]`; F-4 ritirato); **tutti i 46 pin del §2 verificati token-per-token** sul CAP frozen; **seam `revoked` risolto pulito**: transizione `active→revoked` a `CAP_02_parte_II.md:127` (§7.2) + premessa supersessione 6.3 a `:77` (constraint $|\mathcal{A}|\le1$ a :81 = materia B2); **precedenza eventi (F-2) confermata a `:131`**. Commit card **`053ca98`** (solo `tasks/ACTIVE_TASK.md`). Esito completo in `Business Spec/Final/ESITO_B3-CARD-UPDATE-01.md`. **SLOT LIBERO**, Developer **NON** invocato (out-of-scope dell'istruzione). 2 note editoriali stale segnalate per giro-Planner (card `:64` parentetica "pin non risolto", `:214` nota di chiusura). **Nessun M nuovo.**
**Aggiornamento 2026-06-15 (CLI, 2ª sessione)**: **SPEC-FUNZ-01-B2 (Payload del segnale) CHIUSO PASS** — secondo blocco della ricostruzione cieca a 8 blocchi (modalità B). Pre-requisito risolto in apertura: **G-25 chiuso** — l'SHA di CAP-02 era `<sha-da-confermare>`, disambiguato a **`a1625df`** (criterio AC "ultima review del contenuto finale": `e070fa9` REVIEW-02 v3 → patch4 `7b9faa5` → patch5 `9852e12` → review PASS `a1625df`; `e070fa9` benediva una versione poi modificata 2 volte) e pinnato in STATO (`633f39e`). **B2**: ciclo `spec_planner` (task card `de9e005`; perimetro = **solo Cap.6 di `CAP_02_parte_II.md`**, sez. 6.1/6.2/6.3: schema-payload, banda $b$, target_1/2, stop strutturale $d_{stop}>b$, qualificatori, immutabilità, segnale unico attivo+sostituzione) → `spec_developer` cieco (`ecce6a1`, **42 requisiti**: 37 B2-R + 5 B2-CN) → **spec_reviewer CLI PASS (`079552c`)**: 0 BUG REALE, **1 NEUTRO** (OM-1 cross-ref interno rotto §3.10↔§8.1, editoriale, non instradato); confronto-copertura vs v2 (`ab7450f`, perimetro payload R-3.1..3.11+CN-3.1) = **0 buchi**; cecità confermata (0 ID v2, 0 firme-testo v2); floor citazioni 100% token-per-token su Cap.6 frozen; lista Empirico-CLI VUOTA. Campi timer (Δt_cromosoma/T_touch_max) e setup_class/filtro 80pt entrati **solo come campi del payload**, non come semantica (confine B3/B4 rispettato). **Micro-pass OM-1** (su decisione AC): corretto il cross-ref interno rotto §3.10→§8.1 per B2-CN-01 (Developer `e12fc97`, 2 righe) → **re-review CLI PASS `b858a88`** (0 regressioni, diff = solo le 2 righe); marcatore aggiornato da `079552c` a `b858a88`. **Nessun M nuovo da B2, nessun M incardinato** (M-GOV-1 `[B-2 PROVVISORIO]` in CARRYOVER = blocco interno v2→B5, non il chunk B2). DEV_STATUS azzerato. `00_indice.md` non toccato. Prossimo: **B3 — State-machine & lifecycle del segnale** (fonte CAP-02 Cap.7±Cap.11; SHA `a1625df` ora pinnabile, nessuna dipendenza fragile).
**Aggiornamento 2026-06-15 (CLI)**: **SPEC-FUNZ-01-B1 (Ambito & operatore) CHIUSO PASS** — primo blocco della **ricostruzione cieca a 8 blocchi** (modalità B) decisa da AC. Piano di chunk finalizzato a **8 blocchi B1→B8** (commit `d5d5fbf`, doc `docs/spec_funzionale/PROPOSTA_SUDDIVISIONE_SPEC_v2.md`; grana per-sezione, due split dal piano a 6: contratto→payload|state-machine, go-live→gate|confine). Modello output: 8 documenti separati che a fine serie si ricompongono in uno solo (assemblaggio = task dedicato post-B8). **B1**: ciclo `spec_planner` (task card `cb9e419`) → `spec_developer` cieco dai CAP (`35ca888`, 34 requisiti: 25 R + 5 CN + 4 NFR, da `CAP_01_parte_I.md` Cap.1-3) → **spec_reviewer CLI PASS (`7195ffe`)**: 0 BUG REALE, 3 NEUTRO; confronto-copertura vs v2 = 0 buchi (B1 più completo della v2 su Cap.1-3), cecità confermata (0 tracce v2), lista Empirico-CLI VUOTA. CAP-01 SHA confermato `b76c32c` (B1 senza dipendenza fragile). Nessun M nuovo da B1 (M-2→B4, M-GOV-1→B5, M-1/M-9/M-10+RACC-METODO-2→B6 restano assegnati). DEV_STATUS azzerato. `00_indice.md` non toccato. Prossimo: **B2 — Payload del segnale** (attenzione: cita CAP-02 a `<sha-da-confermare>`).
**Aggiornamento 2026-06-14 (CLI)**: **SPEC-FUNZ-01 RICOSTRUITA ex-novo (v2) e PROMOSSA**. Modalità B (Developer cieco): ricostruzione dai CAP-fonte, diff di copertura superato (36/36 requisiti vecchi coperti; CN-3 "non è consulenza" lasciata cadere su decisione AC; KPI lifecycle enumerati NFR-8.9/8.10/8.11). Review v2 PASS (2a6b944) → micro-pass KPI (1c59be9) → re-review PASS (ab7450f). 75 requisiti (41 R + 13 NFR + 21 CN). Vecchia v1 conservata: tag `spec-funz-01-v1-storico` (a16a4c0) + `_v1_storico` committate. Rimpiazzo Fase D eseguito.
**Ultimo aggiornamento**: 2026-06-03 — sessione **CLI locale**: **SPEC-FUNZ-01 (track NON-CAP, specifica funzionale di prodotto) CHIUSO PASS**. Ciclo completo Planner (`7604445`) → Developer v1 (`e08409b`) → Review v1 **PASS** (`d8a40a0`; 0 BUG REALE, 3 NEUTRO igiene-citazione) → micro-pass v2 sui 3 NEUTRO (`314dd1b`) → **Re-Review v2 PASS** (`a16a4c0`; 0 finding, 0 regressione, 6 numeri di riga OM-1 riverificati token-per-token). Prodotto: `docs/spec_funzionale/SPEC_FUNZ_01.md` (10 sezioni, **36 requisiti** R/NFR/CN, matrice di tracciabilità 36 righe) + `reports/REPORT_SPEC_FUNZ_01.md`. **M-2** (latenza Telegram $L_{max}=30$s) incardinato come **NFR-1**; la verifica empirica resta OPEN (Appendice E / FASE-D). `00_indice.md` **NON modificato** (SPEC-FUNZ-01 non è una Parte della metodologia v2). DEV_STATUS azzerato. Track su `main` (trunk).
**Aggiornamento 2026-06-02 (CLI)**: **AUDIT-RM CAP-DATA-03 (perimetro A-D) CHIUSO PASS**. Audit indipendente confermativo RM-1/2/3 su A=`CAP_10_parte_10.md` / B=`REPORT_CAP_10.md` / C=`PROBE_RECUPERO_GAP_DAPI.md` / D=`export_directa_history_parametric.py` (decoder canonico): v1 PASS `33d35b9` + re-review v2 PASS `aa19055`; tutte le citazioni `[CODICE-ESISTENTE]` verso D confermate token-per-token; lista Empirico-CLI VUOTA; **1 finding NEUTRO** (phrasing "OHLCV coincidenti" Cap.59 r.105) **fixato** (`41447d3`) e riconfermato (0 regressioni). Parte 10 resta PASS storico `48171e4`. DEV_STATUS azzerato.
**Aggiornamento precedente**: 2026-06-01 — sessione **CLI locale** (ciclo completo CAP-DATA-03 / Parte 10): **CAP-DATA-03 CHIUSO PASS** — Review v2 `48171e4` (ciclo: v1 PASS `ab80d96` → v2 cosmetica `3eba20f` → re-review v2 PASS; 43/43 AC confermati indipendentemente; 4 finding NEUTRO NB-1/OM-1/OM-2/OM-3 chiusi; 0 regressioni). Indice Parte 10 → PASS, DEV_STATUS azzerato, CARRYOVER aggiornato (nessun M-promemoria nuovo emesso da CAP-DATA-03; RACC-METODO-2 onorata). Parte 10 chiude i 4 temi rinviati da Parte 9 Cap.55 (continuità tape, recupero gap, riconciliazione canonica giornaliera, storicizzazione strutturata) ed estende l'invariante research = runtime al ciclo di vita del tape.
**Storico sessione precedente**: **CLI locale** (follow-up empirico AUDIT-RM-RETRO CAP-DATA-02): **PASS EMPIRICO** sulle 8 voci Empirico-CLI contro DAPI live (`reviews/REVIEW_CAP_DATA_02_RM_RETRO_CLI_review.md`), **0 SMENTITE / 0 BUG REALI**. **Audit RM-RETRO CAP-DATA-02 ora CHIUSO (WEB+CLI)**. Confermati: schema PRICE (`f8`/`f9`=day_low/day_high — hypothesis Web "bid/ask" FALSIFICATA; `f6`=volume cumulato), schema BOOK_5 (BID×5/ASK×5 best-first, triplo `lots,orders,price` certificato 290/290), codici errore 1004/1007/1017/1015/1003 (confini disambiguati), mesi `F`=Giugno/`I`=Settembre via ANAG, refutazione cooldown "14/~30s" estesa a 850 conn/~907Hz (0 onset), banner len=142. Parziali NON bloccanti: 1030 (IDEM nel servizio base), riavvio Darwin mezzanotte (notturno), mesi Mar/Dic (non listati al 2026-06-01).
**Aggiornamento 2026-06-01 (stessa sessione CLI)**: completati anche **V-1 afternoon (§2.4)** e **T+1 (§2.5)** in `tasks/PROBE_RECUPERO_GAP_DAPI.md`. Afternoon (cattura custom 14:55–15:25, dopo un blocco Darwin 14:30–14:50 risolto chiudendo TradingView): **equivalenza realtime↔CANDLERANGE CONFERMATA** (49/62 match, 13 residui spiegati = cash low sparsity + scarto confine minuto, nessuno swap O/C, schema C;L;H;O regge). T+1 (re-fetch 29/05 il 01/06 = T+3): **60/60 barre morning IDENTICHE → barre intraday immutabili** (no rewriting notturno). Self-review RM-4 opzione A in fondo al probe doc, gatekeeping Orchestratore PASS.
**Prossima sessione attesa** (trigger AC "**riprendiamo**"): **DECISIONE AC SUL PROSSIMO BLOCCO** dopo la chiusura PASS di B3. **Stato**: **SPEC-FUNZ-01-B3 CHIUSO PASS** (`e94ef17`); **SLOT LIBERO**, `DEV_STATUS` vuoto, `ACTIVE_TASK` storico su B3. Serie ricostruzione cieca: **B1** (`7195ffe`) + **B2** (`b858a88`) + **B3** (`e94ef17`) chiusi PASS → restano **B4→B8**. **Candidato naturale: B4 — Emissione & consegna** (fonte `CAP_02_parte_II.md` Cap.8 condizioni/regola di emissione + filtro 80pt come regola, Cap.9 pubblicazione Telegram/contratto notifica/latenza/anti-duplicato; **eredita M-2/B-1** = verifica empirica latenza Telegram $L_{max}=30$s, OPEN). **Azione attesa al "riprendiamo"**: su "vai" di AC, mini giro `spec_planner` per la card B4 (modalità B, cecità Developer da v2/_v1_storico/B*/chunking; sede CLI) → `spec_developer` cieco → check post-Developer (+ boundary-check Orchestratore) → `spec_reviewer` CLI (audit AC + confronto-copertura vs v2 `ab7450f` su perimetro emissione/consegna, partizione su mappa di chunking F-3) → chiusura B. _Storico:_ **B3 chiuso PASS 2026-06-16** (`e94ef17`, 61 req.); **B2** (`b858a88`); **B1** (`7195ffe`); **SPEC-FUNZ-01 v2** (`a16a4c0`). Altri candidati a fine serie (discrezione AC): **SPEC-FUNZ-02** (PHASE-2 cross-index), avvio **FASE-D**. _Contesto metodologico pregresso (CAP-DATA-03 / Parte 10, invariato):_ versante runtime-tape della convenzione dati chiuso PASS; Audit RM-RETRO CAP-DATA-01/02 CHIUSI (WEB+CLI); residui Empirico-CLI non bloccanti invariati (1030 ticker gated PHASE-2, mesi Mar/Dic, riavvio Darwin mezzanotte).

---

## 1. Dove siamo nel progetto

**Fase**: **CAP-DATA-03 / Parte 10 chiuso PASS** (2026-06-01, review `48171e4`). Si chiude il versante runtime-tape della convenzione dati (continuità, recupero gap, riconciliazione, storicizzazione). Prossimo capitolo deciso dal Planner della nuova sessione (Appendici operative o CAP-DATA-04). Roadmap: PHASE-1 FIB-only.

**Bloccante per avanzare**: ~~completare `tasks/PROBE_RECUPERO_GAP_DAPI.md` con i risultati di V-1 e V-2~~ ✅ **SBLOCCATO 2026-06-01**: V-1 (morning+afternoon, equivalenza confermata), V-2 (cut-off ~100gg intraday / nessun limite daily) e T+1 (immutabilità barre) tutti completi nel probe doc. Pronto per CAP-DATA-03.

---

## 2. Ultimo capitolo metodologico chiuso PASS

| Capitolo | Stato | Hash review |
|---|---|---|
| **CAP-DATA-03 (Parte 10)** | **PASS** | **`48171e4`** (Review v2; v1 `ab80d96`) |
| CAP-DATA-02 (Parte 9) | PASS | `86425a7` |

---

## 3. Task aperti in coda

| Priorità | Task | File di stato | Owner | Vincolo temporale |
|---|---|---|---|---|
| ~~1~~ | ~~**V-1 morning capture**~~ ✅ FATTO 09:00–09:30: 1425 tick PRICE (FIB6F 1245, DITAS 180), 0 unknown | `probe_out/v1_morning_20260529.*` | CLI locale | — |
| ~~2~~ | ~~**V-1 afternoon capture**~~ ✅ FATTO 2026-06-01 (cattura custom 14:55–15:25 dopo blocco Darwin 14:30–14:50; 2098 PRICE, 0 unknown): equivalenza confermata 49/62, 13 residui spiegati, schema C;L;H;O regge | `probe_out/v1_now_20260601_*` | — |
| 3 | **Re-run inventory CME** | `update_inventory_indici_futures_daily.py` | CLI locale | dopo le 14:30 (settle USA propagato) |
| ~~4~~ | ~~**V-1 fetch + compare**~~ ✅ FATTO (morning): equivalenza confermata, 55/60 match dopo fix schema; 5 residui = primo minuto troncato + scarti 1 tick. Ri-fare dopo afternoon. | `probe_out/v1_compare_*.json` | CLI locale | dopo le 15:00 (afternoon) |
| 5 | **V-2 cut-off** | `probe_dapi.py v2-cutoff` con period 60 e 86400 | CLI locale | finestre morte (10:00–14:00, sera) |
| 6 | **Compilare PROBE_RECUPERO_GAP_DAPI.md** | redatto da CLI sulla base dei CSV di V-1/V-2 | CLI locale | fine giornata 2026-05-29 |
| 7 | **CAP-DATA-03** | data warehouse: cumulativi vs daily, limite 100gg, schema CANDLE corretto, gestione ticker scaduti | Web (Planner→Developer→Reviewer) | dopo che PROBE_*.md è su main |

---

## 4. Stato repo (`origin/main`)

| Campo | Valore |
|---|---|
| Ultimo commit | `074fba4` — `[REVIEW] Re-Review AUDIT-RM-RETRO CAP-DATA-01 v2 — PASS` |
| Branch primario | `main` |
| Branch attivi | nessuno (tutti i `claude/*` sono mergiati e fast-forwarded) |
| Working tree atteso | clean |

Commit recenti:
```
074fba4 [REVIEW] Re-Review AUDIT-RM-RETRO CAP-DATA-01 v2 — PASS (sede CLI)
4bc870f [AUDIT-RETRO] report ridotto rework Iter.2 — mappatura 7 finding + self-review
34e233f [AUDIT-RETRO] DEV_STATUS READY_FOR_REVIEW — rework Iter.2 C+D consegnato
e444c33 [AUDIT-RETRO] patch C+D — chiusura 7 finding Review v1 (2 BUG REALI + 5 MIGLIORA PROCESSO)
8e0e334 [REVIEW] CAP-DATA-01 RM-RETRO web — CONDITIONAL
```

---

## 5. M-promemoria attivi (memoria persistente fra sessioni)

| ID | Promemoria | Dove è già incorporato |
|---|---|---|
| M-1 | ⚠️ **CORRETTO 2026-05-29**: schema CANDLE reale = `UFF;MIN;MAX;APE;V` = **`C;L;H;O;V`**, NON `O;L;H;C`. V-1 ha provato lo swap O/C: su daily O e C non erano distinguibili (solo L/H lo erano), per questo l'errore era passato. `export_directa_history_parametric.py` era già corretto → dump storici NON affetti. Fix nel decoder `probe_dapi.py` in `a12ae32`. | `scripts/probe_dapi.py` + `export_directa_history_parametric.py` |
| M-2 | Sintassi `CANDLERANGE <sym> <yyyyMMddHHmmss_start> <yyyyMMddHHmmss_end> <period_s>` (4 arg, period ultimo) | `scripts/probe_dapi.py` |
| M-3 | ⚠️ **RIAUDITATO [PROVA-EMPIRICA 2026-05-29]** (AUDIT-RM-RETRO W4): `1004` cmd ignoto, `1007` ticker inesistente/non abilitato, `1017` sintassi strutturale malformata, `1015` data/parametro invalido (**NUOVO**, distinto da 1017), `1003` comando storico su porta realtime (**NUOVO**). `1030` realtime non sottoscritto **non riprodotto** (account FIB ha il dato) → verifica parziale. Dump: `probe_out/w4_errcodes_20260529.json`. ✅ **RICONFERMATO CLI [PROVA-EMPIRICA 2026-06-01]** (CAP-DATA-02 W5a, mercato aperto): tutti e 5 i codici riprodotti, confini 1017/1015/1003/1007 disambiguati; 1030 ancora non riproducibile sul FIB (IDEM nel servizio base). Dump: `probe_out/w5_w10_20260601_111246.json` | docstring `probe_dapi.py` + `HANDOFF §3.4` |
| M-4 | Convenzione mese Directa-IDEM: `F`=Giugno **confermato [PROVA-EMPIRICA 2026-05-29]** (SUB FIB6F → ANAG ISIN IT0024209022 GIU26, AUDIT-RM-RETRO W5). ✅ **`I`=Settembre confermato [PROVA-EMPIRICA 2026-06-01]** (SUB FIB6I → ANAG ISIN IT0024847870 SET26, CAP-DATA-02 W6). Mar/Dic e `FIB6L` → `1007` (**contratti non listati al 2026-06-01**): non decodificabili finché non quotati. Convenzione Directa **NON-standard** (F≠Gennaio, RM-3) → niente inferenza per analogia. Residuo Empirico-CLI quando listati. Dump: `probe_out/w6_months_20260601_111616.json` | risolto F/I; Mar/Dic residuo |
| M-5 | ⚠️ **RIAUDITATO [PROVA-EMPIRICA 2026-05-29]** (AUDIT-RM-RETRO W6): la costante "cooldown ~30s dopo 14ª connessione" è **refutata nel regime testato** — 75 connessioni open/close a ~1Hz su 10003 senza alcun cooldown (3×25, `onset_connection:null`). ✅ **ESTESO CLI [PROVA-EMPIRICA 2026-06-01]** (CAP-DATA-02 W9): **850 connessioni** open/close fino a **~907 Hz** su 10003, **0 onset** → "14/~30s" refutata anche a burst >>1Hz. Rate-limit a frequenze ancora più estreme/lato server non escludibile in assoluto (ipotesi minore aperta, NON una costante dichiarata). Dump: `probe_out/w9_burst2_20260601_111842.json` | `probe_dapi.py` + `HANDOFF §3.6` |
| M-6 | Account `B6086` non committarlo in chiaro. `scripts/directa_history_export_config.json` (con il valore) è in `.gitignore`. Template safe = `.example.json` | `.gitignore` |
| M-7 | Settle CME daily arriva sul DAPI Directa nel pomeriggio CET (non di notte). Rilanciare `update_inventory_*` dopo le 14:30 | TODO 29/05 |
| M-8 | Bug encoding `cp1252` su console Windows italiana → patch UTF-8 reconfigure già committata in `2dc457b` | risolto |
| M-9 | **Schema PRICE realtime (DAPI)** [PROVA-EMPIRICA 2026-06-01 W2, CAP-DATA-02]: `PRICE;<tk>;<HH:mm:ss>;<f4=last>;<f5>;<f6=volume_cum>;<f7>;<f8=day_low>;<f9=day_high>`. `f8`/`f9`=estremi di giornata (cross-check daily CANDLE L/H — alternativa "best bid/ask" del Web reviewer **FALSIFICATA** da BOOK_5 simultaneo); `f6`=volume cumulato (monotòno, match CANDLE.V); `f5`/`f7` contatori cumulativi **non disambiguati** (verifica parziale). Cash untraded (DGER) → `f5=f6=f7=0`, `f8`/`f9` valorizzati. Dump: `probe_out/w2_w3_w6_20260601_111350.json` + `w2_vol_*` | nuovo, da incorporare in CAP-DATA-03 adapter |
| M-10 | **Schema BOOK_5 (DAPI) CERTIFICATO** [PROVA-EMPIRICA 2026-06-01 W3, CAP-DATA-02]: `BOOK_5;<tk>;<HH:mm:ss>;` + 10 triple `(lots,orders,price)` = `[BID×5 best-first][ASK×5 best-first]`. `bid1_lots`=campo4, `bid1_orders`=campo5, `bid1_price`=campo6; `ask1_lots`=campo19, `ask1_price`=campo21 (**posizioni di `bar_synthetic` Cap.49 certificate**). `f1≥f2` su 290/290 (lots≥orders) esclude triplo invertito; `bid1<ask1` su 29/29. Anomalia 27/05 `bid1>ask1` = **artefatto del campione** (FIB6I illiquido scadenza lontana), NON inversione schema. Dump: `probe_out/w2_w3_w6_20260601_111350.json` | nuovo, da incorporare in CAP-DATA-03 adapter |

---

## 6. Stato dati locali (NON versionati)

### `C:\Users\AN\Documents\Projects\ga-zone-engine\exports\directa_history\` — dati live
- 391 dump giornalieri (16 ticker × ~24 giorni dal 25/04 al 28/05/2026)
- ⚠️ **Mancano 6 CME del 28/05** (`CM.MESM6/U6`, `CM.MNQM6/U6`, `CM.MYMM6/U6`) — settle non propagato. Recuperare oggi pomeriggio.

### `C:\directa_history_parametric_export_overlay\` — archivio storico (346 MB, pulito da 1409 MB)
- `exports/directa_history/` — 256 dump storici pre-25/04. Include `DITAS_20110404_20260402` = **15 anni daily FTSE MIB cash**
- `exports/directa_history_ml2/` — progetto ML2 vivo (258 MB, **NON toccare**)
- `exports/directa_history_ml2_safety_backup/` — audit cleanup 29/03 (NON toccare)
- `preserved_from_overlay/` — 29 MB archeology ML1 + probe SUB20 + 52 CSV unici estratti da `.7z`
- ⚠️ Backup off-site di `preserved_from_overlay/` non ancora fatto

### Inventory CSV (path hardcoded all'overlay)
- `C:\directa_history_parametric_export_overlay\exports\directa_history\inventory_indici_futures_daily.csv` — aggiornato al 28/05 (CME 27/05)

---

## 7. Convenzioni di update di questo file

### Quando aggiornarlo

- **Inizio sessione**: dopo `git pull`, leggi questo file. È la prima fonte di verità su cosa è successo dall'ultima volta.
- **Fine sessione**: aggiorna le sezioni che hai toccato, cambia `Ultimo aggiornamento` e `Prossima sessione attesa`, committa.

### Regole di update

| Sezione | Chi può modificare | Quando |
|---|---|---|
| 1. Dove siamo | Web (Planner) | Cambio di fase/capitolo |
| 2. Ultimo PASS | Web (Orchestratore alla chiusura) | Chiusura sessione metodologica PASS |
| 3. Task aperti | Web o CLI | Ad ogni task completato (remuove riga) o nuovo (aggiunge) |
| 4. Stato repo | Chiunque | Dopo commit/push rilevante |
| 5. M-promemoria | Web (Planner/Reviewer) | Nuova scoperta che persiste fra sessioni. **Mai cancellare senza commit dedicato che spiega perché.** |
| 6. Stato dati locali | CLI locale (è l'unico che li vede) | Ad ogni run che cambia struttura locale |
| 7. Convenzioni | Web (per accordo con supervisore) | Raro |

### Sintassi commit message

`[STATO] <descrizione breve>` per il commit che aggiorna solo questo file.
Per commit che aggiornano più cose (es. PASS + STATO + indice): tag del commit principale + sezione "Aggiornato STATO_CORRENTE.md" nel body.

### Mai

- Pushare con working tree dirty su file di stato (`CARRYOVER.md`, `STATO_CORRENTE.md`, `ACTIVE_TASK.md`, `DEV_STATUS.md`) — sono single-writer per disciplina
- Cancellare M-promemoria senza spiegare in un commit dedicato
- Sovrascrivere "Prossima sessione attesa" se non sei tu il prossimo (chiedi al supervisore se ambiguo)
- Mettere dati sensibili (account_code, token, password) qui dentro

---

## 8. Riferimenti rapidi

- **Workflow orchestratore metodologico**: `.claude/CLAUDE.md`
- **Regole metodologiche permanenti (RM-1..RM-4)**: `tasks/METODO.md` ← **da leggere come prima azione di ogni sessione**
- **Briefing probe corrente**: `tasks/HANDOFF_PROBE_DAPI_20260528.md`
- **Nota ripresa CLI**: `tasks/RIPRESA_20260529.md`
- **Carryover M-promemoria storici (namespace CAP-XX)**: `tasks/CARRYOVER.md`
- **Indagine DAPI base**: `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md` (Appendici A/B)
- **Indice metodologico**: `docs/methodology_v2/00_indice.md`
