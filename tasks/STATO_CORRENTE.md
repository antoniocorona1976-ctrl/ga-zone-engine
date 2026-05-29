# STATO CORRENTE — ga-zone-engine

> **Single source of truth** dello stato del progetto. Aggiornato all'inizio e alla fine di ogni sessione (web e CLI locale). **Prima azione** di ogni sessione Claude: leggere questo file.

**Ultimo aggiornamento**: 2026-05-29 02:15 CET — sessione **web** (Claude Code on the web)
**Prossima sessione attesa**: **CLI locale** alle 09:00 CET per V-1 morning capture

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
| 1 | **V-1 morning capture** | `scripts/probe_dapi.py v1-capture --window morning` | CLI locale | 09:00–09:30 CET 2026-05-29 |
| 2 | **V-1 afternoon capture** | idem `--window afternoon` | CLI locale | 14:30–15:00 CET 2026-05-29 |
| 3 | **Re-run inventory CME** | `update_inventory_indici_futures_daily.py` | CLI locale | dopo le 14:30 (settle USA propagato) |
| 4 | **V-1 fetch + compare** | `probe_dapi.py v1-fetch` poi `v1-compare` | CLI locale | dopo le 15:00 |
| 5 | **V-2 cut-off** | `probe_dapi.py v2-cutoff` con period 60 e 86400 | CLI locale | finestre morte (10:00–14:00, sera) |
| 6 | **Compilare PROBE_RECUPERO_GAP_DAPI.md** | redatto da CLI sulla base dei CSV di V-1/V-2 | CLI locale | fine giornata 2026-05-29 |
| 7 | **CAP-DATA-03** | data warehouse: cumulativi vs daily, limite 100gg, schema CANDLE corretto, gestione ticker scaduti | Web (Planner→Developer→Reviewer) | dopo che PROBE_*.md è su main |

---

## 4. Stato repo (`origin/main`)

| Campo | Valore |
|---|---|
| Ultimo commit | `6c84504` — `[PROBE] nota di ripresa 2026-05-29` |
| Branch primario | `main` |
| Branch attivi | nessuno (tutti i `claude/*` sono mergiati e fast-forwarded) |
| Working tree atteso | clean |

Commit recenti:
```
6c84504 [PROBE] nota di ripresa 2026-05-29: stato pre-V-1 + due note operative
2dc457b [PROBE] probe_dapi.py: forza UTF-8 su stdout/stderr per console Windows
9bf35fa [HANDOFF] briefing sessione probe DAPI 2026-05-28 per Claude CLI locale
1fa0109 Merge PR #1 — probe_dapi.py runner V-1/V-2
76efda2 Merge PR #2 — consolidate overlay scripts
```

---

## 5. M-promemoria attivi (memoria persistente fra sessioni)

| ID | Promemoria | Dove è già incorporato |
|---|---|---|
| M-1 | Schema CANDLE reale = `O;L;H;C;V` (wiki dichiara OHLC, inesatto) | `scripts/probe_dapi.py` decoder |
| M-2 | Sintassi `CANDLERANGE <sym> <yyyyMMddHHmmss_start> <yyyyMMddHHmmss_end> <period_s>` (4 arg, period ultimo) | `scripts/probe_dapi.py` |
| M-3 | Codici errore DAPI: `1004` cmd non valido, `1007` ticker non abilitato (storico), `1017` sintassi malformata, `1030` realtime non sottoscritto | docstring `probe_dapi.py` |
| M-4 | Convenzione mese Directa-IDEM: `F`=Giugno, `I`=Settembre. **Mar e Dic da decodificare oggi.** | TODO |
| M-5 | Socket persistente per porte 10001/10003: cooldown ~30s dopo 14 aperture rapide consecutive | `probe_dapi.py` |
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
- **Briefing probe corrente**: `tasks/HANDOFF_PROBE_DAPI_20260528.md`
- **Nota ripresa CLI**: `tasks/RIPRESA_20260529.md`
- **Carryover M-promemoria storici**: `tasks/CARRYOVER.md`
- **Indagine DAPI base**: `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md` (Appendici A/B)
- **Indice metodologico**: `docs/methodology_v2/00_indice.md`
