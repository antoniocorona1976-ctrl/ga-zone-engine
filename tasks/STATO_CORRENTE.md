# STATO CORRENTE — ga-zone-engine

> **Single source of truth** dello stato del progetto. Aggiornato all'inizio e alla fine di ogni sessione (web e CLI locale). **Prima azione** di ogni sessione Claude: leggere questo file.

**Ultimo aggiornamento**: 2026-05-30 — sessione **WEB** (AUDIT-RM-RETRO CAP-DATA-02 chiuso **PASS sede WEB**, Re-Review Iter.3 `20961f4`; trovato e corretto **1 BUG catastrofico**: schema CANDLE invertito `O;H;L;C` in Cap.49 → corretto a `C;L;H;O` coerente col decoder canonico, + 8 finding RM-1/2/3; debito retroattivo RM su perimetro A-D di Parte 9 saldato lato WEB; 8 voci Empirico-CLI in handoff)
**Prossima sessione attesa**: **CLI locale a mercato aperto** per le verifiche empiriche residue di **CAP-DATA-01 e CAP-DATA-02** (schema PRICE/BOOK_5 bit-a-bit, trigger esatti codici errore + 1030, mesi IDEM Mar/Dic + FIB6L, cooldown burst >>1Hz, banner per release Darwin, riavvio mezzanotte) — liste Empirico-CLI in `reviews/REVIEW_CAP_DATA_01_RM_RETRO_v2_review.md` e `reviews/REVIEW_CAP_DATA_02_RM_RETRO_v2_review.md`

---

## 1. Dove siamo nel progetto

**Fase**: pre-CAP-DATA-03. In corso il **probe DAPI V-1/V-2** (prerequisito empirico, non capitolo metodologico). CAP-DATA-02 chiuso PASS il 2026-05-27. Roadmap: PHASE-1 FIB-only.

**Bloccante per avanzare**: completare `tasks/PROBE_RECUPERO_GAP_DAPI.md` con i risultati di V-1 (equivalenza realtime vs CANDLERANGE) e V-2 (cut-off temporale).

---

## 2. Ultimo capitolo metodologico chiuso PASS

| Capitolo | Stato | Hash review |
|---|---|---|
| CAP-DATA-02 (Parte 9) | PASS | `86425a7` |

---

## 3. Task aperti in coda

| Priorità | Task | File di stato | Owner | Vincolo temporale |
|---|---|---|---|---|
| ~~1~~ | ~~**V-1 morning capture**~~ ✅ FATTO 09:00–09:30: 1425 tick PRICE (FIB6F 1245, DITAS 180), 0 unknown | `probe_out/v1_morning_20260529.*` | CLI locale | — |
| 2 | **V-1 afternoon capture** | idem `--window afternoon` | CLI locale | 14:30–15:00 CET 2026-05-29 |
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
| M-3 | ⚠️ **RIAUDITATO [PROVA-EMPIRICA 2026-05-29]** (AUDIT-RM-RETRO W4): `1004` cmd ignoto, `1007` ticker inesistente/non abilitato, `1017` sintassi strutturale malformata, `1015` data/parametro invalido (**NUOVO**, distinto da 1017), `1003` comando storico su porta realtime (**NUOVO**). `1030` realtime non sottoscritto **non riprodotto** (account FIB ha il dato) → verifica parziale. Dump: `probe_out/w4_errcodes_20260529.json` | docstring `probe_dapi.py` + `HANDOFF §3.4` |
| M-4 | Convenzione mese Directa-IDEM: `F`=Giugno **confermato [PROVA-EMPIRICA 2026-05-29]** (SUB FIB6F → ANAG ISIN IT0024209022 GIU26, AUDIT-RM-RETRO W5). `I`=Settembre + Mar/Dic **ancora da decodificare a mercato aperto** (verifica parziale). | TODO (W5 residuo Empirico-CLI) |
| M-5 | ⚠️ **RIAUDITATO [PROVA-EMPIRICA 2026-05-29]** (AUDIT-RM-RETRO W6): la costante "cooldown ~30s dopo 14ª connessione" è **refutata nel regime testato** — 75 connessioni open/close a ~1Hz su 10003 senza alcun cooldown (3×25, `onset_connection:null`). Soglia/durata sotto burst >>1Hz NON disambiguate (verifica parziale). Dump: `probe_out/w6_cooldown_20260529.json` | `probe_dapi.py` + `HANDOFF §3.6` |
| M-6 | Account `B6086` non committarlo in chiaro. `scripts/directa_history_export_config.json` (con il valore) è in `.gitignore`. Template safe = `.example.json` | `.gitignore` |
| M-7 | Settle CME daily arriva sul DAPI Directa nel pomeriggio CET (non di notte). Rilanciare `update_inventory_*` dopo le 14:30 | TODO 29/05 |
| M-8 | Bug encoding `cp1252` su console Windows italiana → patch UTF-8 reconfigure già committata in `2dc457b` | risolto |

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
