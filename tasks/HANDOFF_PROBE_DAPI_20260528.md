# HANDOFF — Sessione probe DAPI 2026-05-28 → continuazione su Claude Code CLI locale

**Sessione di origine**: Claude Code on the web, 2026-05-28 sera/notte
**Continuazione**: Claude Code CLI locale sul PC del supervisore
**Scopo**: dare contesto completo per eseguire V-1 e V-2 oggi 2026-05-29 senza ribriefare

---

## 1. Cosa è successo stanotte (sintesi)

1. **Probe DAPI sanity** eseguito empiricamente dal supervisore con DGo+Darwin attivi: confermati ticker FIB6F vivo, indici cash europei (DITAS/DGER/DFRA/DSTX50) gratuiti, market data realtime FIB attivo su account `B6086`.
2. **Scoperti 6 fatti critici sul DAPI** (vedi §3 sotto) — di cui uno contraddice il wiki ufficiale.
3. **Commit + merge in `main`** di `scripts/probe_dapi.py` (runner CLI per V-1 e V-2) + 4 file consolidati dalla cartella locale overlay (PR #1 e #2).
4. **Pulizia cartella `C:\directa_history_parametric_export_overlay\`**: da 1409 MB → 346 MB (recuperati 1062 MB, 75%). Estratti 52 CSV unici da `.7z` poi cancellato. Materiale di valore preservato in `preserved_from_overlay/`.
5. **Inventory aggiornato**: rilanciato `update_inventory_indici_futures_daily.py`, scaricati ~380 dump giornalieri da 25/04 a 28/05/2026 su 16 ticker in `C:\Users\AN\Documents\Projects\ga-zone-engine\exports\directa_history\`.

---

## 2. Stato repository (`main` aggiornato)

| Path | Cosa è |
|---|---|
| `scripts/probe_dapi.py` (588 righe) | runner CLI: `sanity`, `v1-capture`, `v1-fetch`, `v1-compare`, `v2-cutoff` |
| `scripts/export_directa_history_parametric.py` | tool esistente per dump storico |
| `scripts/update_inventory_indici_futures_daily.py` | aggiornatore inventory (consolidato da overlay) |
| `scripts/directa_history_export_config.example.json` | template config (no account_code) |
| `scripts/README_export_directa_history_parametric.txt` | docs uso |
| `scripts/run_export_directa_history_parametric.cmd` | launcher Windows |
| `.gitignore` | esclude `exports/`, `probe_out/`, `scripts/directa_history_export_config.json` (config personale) |
| `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md` | indagine con Appendici A/B (probe storici) — leggere per contesto DAPI completo |

---

## 3. Scoperte DAPI critiche (M-promemoria per CAP-DATA-03)

### 3.1 Schema CANDLE reale = ~~`O;L;H;C;V`~~ → **`C;L;H;O;V`** (rettificato 2026-05-29)

⚠️ **RETTIFICA 2026-05-29 (sessione V-1)**: lo schema reale è **`C;L;H;O;V`** = `UFF;MIN;MAX;APE;V`, NON `O;L;H;C;V` come dichiarato qui sotto. La verifica del 28/05 era su daily, dove O e C non sono distinguibili dai 4 valori (solo L e H lo sono). V-1 ha provato con tick realtime FIB6F 09:08: primo tick=50090, ultimo=50130; nella candela storica `p[4]=50130 (close)`, `p[7]=50090 (open)`. La fonte corretta era già nel codice di produzione: `scripts/export_directa_history_parametric.py` r.477 con commento esplicito *"Documentazione Directa: UFF, MIN, MAX, APE => close, low, high, open"*. Dettagli e risposta del revisore in `tasks/PROBE_RECUPERO_GAP_DAPI.md` §3 e §7. Fix nel decoder `probe_dapi.py` in commit `a12ae32`.

**Testo originale del 28/05 (conservato per storia, ora superato):**

> ⚠️ Il wiki DAPI dichiara `O;H;L;C` ma è INESATTO. Verificato empiricamente su FIB6F daily (O=48742, L=47925, H=48875, C=48160) e DITAS daily — coerente in tutti i casi. `probe_dapi.py` decoder già usa questo schema corretto.

### 3.2 Sintassi `CANDLERANGE`

`CANDLERANGE <sym> <yyyyMMddHHmmss_start> <yyyyMMddHHmmss_end> <period_s>`

4 argomenti, **period_s come ULTIMO** (NON secondo).

**Etichetta fonte (RM-3, aggiunta post-RM 2026-05-29)**: l'ordine argomenti è corroborato da codice di produzione `[CODICE-ESISTENTE r.228-230 scripts/export_directa_history_parametric.py]`, che emette la stessa identica sintassi con `period_seconds` in ultima posizione. Non è asserzione isolata di sessione web (livello 2).

> **Nota (rettificato post-RM 2026-05-29)**: la clausola originale "Sintassi errata restituisce `ERR;;1017`" è stata disambiguata empiricamente — vedi §3.4: `1017` copre solo la sintassi STRUTTURALE malformata (ordine/numero argomenti), NON il parametro fuori range o la data invalida (che produce `1015`).

### 3.3 Terminatore stream history

`END CANDLES` — marker testuale di fine. `probe_dapi.py` lo usa già come marker per terminare la `read_until_any()`.

**Etichetta fonte (RM-3, aggiunta post-RM 2026-05-29)**: corroborato da `[CODICE-ESISTENTE r.245 scripts/export_directa_history_parametric.py]`, dove `END CANDLES` è usato come marker di fine stream nel tool di produzione che ha già processato ~380 dump (livello 2, non asserzione isolata).

### 3.4 Codici errore mappati

⚠️ **RIVEDUTO post-RM 2026-05-29 (BUG REALE #1, rework AUDIT-RM-RETRO)**: la tabella originale del 28/05 (conservata in fondo per storia, ora superata) dichiarava la semantica dei codici come "fatto" senza enumerare le alternative compatibili né citare un dump:timestamp. Audit RM-1 + prova empirica diretta hanno disambiguato `1017` e scoperto due codici nuovi (`1015`, `1003`). Blocco RM-1 sotto.

**VERIFICA**: semantica dei codici errore DAPI sulle porte storica (10003) e realtime (10001) come da tabella rivista sotto.

**PROVE**: `[PROVA-EMPIRICA 2026-05-29]` probe `w4_errcodes` (DGo aperta, mercato chiuso ~23:19 CET; dump locale completo `probe_out/w4_errcodes_20260529.json`, gitignored). Comandi-trigger inviati e righe `ERR;...` ricevute (campione incorporato inline per autoportanza su origin/main):

| Codice | Comando-trigger inviato | Riga `ERR;...` ricevuta (con timestamp dove restituito dal server) | Porta |
|---|---|---|---|
| `1017` | `CANDLERANGE FIB6F 60 20260519080000 20260519180000` (period come 2° arg) | `ERR;;1017` | 10003 |
| `1017` | `CANDLERANGE FIB6F` (argomenti insufficienti) | `ERR;;1017` | 10003 |
| `1015` | `CANDLERANGE FIB6F notadate notadate 60` (date non parsabili) | `ERR;1015;20260218000000;20260529231925` | 10003 |
| `1007` | `CANDLERANGE ZZZNOPE 20260519080000 20260519180000 60` (ticker inesistente) | `ERR;ZZZNOPE;1007` | 10003 |
| `1007` | `SUB ZZZNOPE` (ticker inesistente, realtime) | `ERR;ZZZNOPE;1007` | 10001 |
| `1004` | `HELP` | `ERR;HELP;1004` | 10003 e 10001 |
| `1004` | `INFO` | `ERR;INFO;1004` | 10001 |
| `1003` | `CANDLERANGE FIB6F 20260519080000 20260519180000 60` (comando storico su porta realtime) | `ERR;N/A;1003` | 10001 |
| `1030` | (market data realtime gated) | **NON riprodotto** — richiede ticker realtime gated a mercato aperto | 10001 |

Semantica rivista:
- `1017` = **sintassi STRUTTURALE malformata** (ordine/numero argomenti errato). **Ristretto**: NON copre il parametro fuori range né la data invalida.
- `1015` = **parametro/data invalida** (codice NUOVO, distinto da `1017`).
- `1007` = ticker non abilitato/inesistente (storico e realtime).
- `1004` = comando ignoto (entrambe le porte).
- `1003` = comando storico inviato su porta realtime (codice NUOVO).
- `1030` = market data realtime non sottoscritto — **verifica parziale, NON riprodotto**.

**ALTERNATIVE COMPATIBILI ESCLUSE**: l'ipotesi originale del 28/05 "`1017` = sintassi del comando malformata in senso ampio (inclusi parametro fuori range / data invalida)" è ESCLUSA dal trigger `notadate` che produce `1015`, non `1017`. L'ipotesi "`1017` = qualsiasi errore CANDLERANGE" è esclusa: ticker inesistente → `1007`, porta sbagliata → `1003`.

**ALTERNATIVE COMPATIBILI NON ESCLUSE**: `1030` non è stato riprodotto (mercato chiuso) → la sua semantica resta "verifica parziale" e va confermata CLI a mercato aperto con un ticker realtime gated. Non è escluso che esistano ulteriori codici (es. limiti di rate) non emersi dal set di trigger usato.

**Testo originale del 28/05 (conservato per storia, ora superato):**

> | Codice | Comando origine | Significato |
> |---|---|---|
> | `1004` | qualsiasi su porta 10001 | comando non valido/non supportato (es. HELP/INFO/STATUS) |
> | `1007` | CANDLERANGE su 10003 | ticker non abilitato per l'account (storico) |
> | `1017` | CANDLERANGE su 10003 | sintassi del comando malformata |
> | `1030` | SUB su porta 10001 | market data realtime non sottoscritto |
>
> _(superato: `1017` era dichiarato in senso troppo ampio; `1015` e `1003` non erano stati osservati; nessun dump:timestamp era citato.)_

### 3.5 Convenzione mese Directa-IDEM (parziale)

- `F` = **Giugno** `[PROVA-EMPIRICA: FIB6F = "FTSE MIB INDEX FUTURE GIU26", ISIN IT0024209022]`
- `I` = **Settembre** `[DOC-INTERNO Appendice B.2]` (da confermare CLI)
- ❓ **Mar e Dic da decodificare** — codici trimestrali, candidati probabili `C` e `L` (speculazione non verificata, Empirico-CLI)

**Nota RM (post-RM 2026-05-29)**: forma di verifica parziale corretta — `F` ancorato a evidenza puntuale (livello 1), `I` a fonte interna (livello 3), Mar/Dic dichiarati esplicitamente "da decodificare" (non come fatto). Etichette di fonte aggiunte in audit.

### 3.6 Pattern architetturale: socket persistente

⚠️ **RIVEDUTO post-RM 2026-05-29 (BUG REALE #2, rework AUDIT-RM-RETRO)**: le due costanti precise "~30s" e "14ª connessione" del 28/05 (conservate in fondo per storia, ora superate) erano dichiarate come fatti da una singola osservazione, senza enumerare le alternative (13/15/dipendenza dal timing). Audit RM-1 + prova empirica diretta le hanno REFUTATE come costanti nel regime testato. Blocco RM-1 sotto.

**VERIFICA**: aprire/chiudere socket a raffica su 10001/10003 innesca un cooldown del gateway dopo un numero fisso di connessioni (~14) per una durata fissa (~30s).

**PROVE**: `[PROVA-EMPIRICA 2026-05-29]` probe `w6_cooldown` (DGo aperta, mercato chiuso ~23:1x CET; dump locale completo `probe_out/w6_cooldown_20260529.json`, gitignored). Disegno: 3 cicli × 25 connessioni open/close su porta 10003 a cadenza ~1Hz (75 connessioni totali). Campione incorporato inline per autoportanza su origin/main:

| Ciclo | Connessioni OK | Onset cooldown | Recovery | Banner per connessione |
|---|---|---|---|---|
| 1 | 25 / 25 | `null` (nessuno) | `null` | `blen=142` ogni connessione |
| 2 | 25 / 25 | `null` (nessuno) | `null` | `blen=142` ogni connessione |
| 3 | 25 / 25 | `null` (nessuno) | `null` | `blen=142` ogni connessione |

(JSON: `onset_connection: null`, `n_ok_before_onset: 25` per tutti e 3 i cicli; tutte le 75 connessioni `ok:true`, `err:null`.)

**ALTERNATIVE COMPATIBILI ESCLUSE**: la soglia "14 connessioni come costante" è **REFUTATA** in questo regime — 25 connessioni consecutive senza alcun onset di cooldown, ripetuto su 3 cicli. Anche "~30s di durata cooldown" non è osservabile perché nessun cooldown si è manifestato.

**ALTERNATIVE COMPATIBILI NON ESCLUSE**: un rate-limit a frequenza più alta (burst >> 1Hz) o a mercato aperto NON è escluso da questo test (~1Hz, 75 connessioni totali). Sotto le condizioni testate nessun cooldown si manifesta; **soglia e durata restano NON confermate come costanti** e vanno ri-disambiguate CLI con burst ad alta frequenza a mercato aperto se mai serve dichiararle come fatto.

Per V-1 cattura realtime di 30 minuti rimane comunque consigliato **SUB + stream + UNSUB** sulla stessa connessione (best practice di prudenza, non più giustificata da una soglia "14" confermata). `probe_dapi.py` lo fa già.

**Testo originale del 28/05 (conservato per storia, ora superato):**

> Aperture/chiusure TCP rapide su 10001 o 10003 innescano **cooldown ~30s** dopo la 14ª connessione consecutiva (Appendice A.4). Per V-1 cattura realtime di 30 minuti: **SUB + stream + UNSUB** sulla stessa connessione. `probe_dapi.py` lo fa già.
>
> _(superato: "14ª connessione" e "~30s" erano due costanti precise da una singola osservazione; il probe del 29/05 non ha riprodotto alcun cooldown su 75 connessioni a ~1Hz.)_

---

## 4. Stato dati locali

### 4.1 `C:\Users\AN\Documents\Projects\ga-zone-engine\exports\directa_history\` — dati live aggiornati

- **391 sottocartelle** dopo run di `update_inventory_indici_futures_daily.py` del 28/05 sera
- 16 ticker × ~24 giorni di trading dal 25/04 al 28/05 = ~380 dump giornalieri freschi
- 5 timeframes per dump: 5M, 15M, 1H, D, W + `_ALL.csv` + `_manifest.json`
- ⚠️ **Mancano 6 dump CME del 28/05** (`CM.MESM6/U6`, `CM.MNQM6/U6`, `CM.MYMM6/U6`): daily settle CME non era ancora pubblicato dal DAPI a tarda sera. **Rilanciare `update_inventory_indici_futures_daily.py` oggi** li recupera.

### 4.2 `C:\directa_history_parametric_export_overlay\` — archeology pulita

- `exports/directa_history/`: 256 dump pre-25/04 storici (DITAS_20110404_20260402 = META-cumulativo 15 anni daily) + 3 pytest-cache vuote locked + 3 inventory CSV
- `exports/directa_history_ml2/`: progetto ML2 vivo (258 MB, NON toccare)
- `exports/directa_history_ml2_safety_backup/`: audit cleanup 29/03 (NON toccare)
- `exports/Dati directa.zip` (0.88 MB): snapshot DITAS+MINI6C
- `preserved_from_overlay/` (29 MB): `artifacts/` ricerca ML1, `DIRECTA_PDF_CORE_EXPORT_20260501_152220/` (probe SUB20), `artifacts_snapshot_20260414/` (52 CSV unici estratti dal `.7z`), codice ML1, docs flat
- ⚠️ **Residui irrilevanti**: `directa_history_parametric_export_overlay.zip` (10.9 KB locked da Windows), 3 pytest-cache locked. Riavvio PC li elimina.

### 4.3 Inventory meta-catalogo

`C:\directa_history_parametric_export_overlay\exports\directa_history\inventory_indici_futures_daily.csv` (path hardcoded nello script): aggiornato al 28/05 dopo run di stasera. Header: `snapshot_date,symbol,type,description,market,start_full_5m_to_w,start_daily_oldest,end_date,rows_5m,rows_15m,rows_1h,rows_d,rows_w,folder_path`.

---

## 5. Cosa fare oggi 2026-05-29 (in ordine)

### 5.0 Pre-flight (subito appena apri)

```powershell
cd C:\Users\AN\Documents\Projects\ga-zone-engine
git status                                              # working tree clean atteso
git pull                                                # già fatto se hai pullato ieri sera
python scripts\probe_dapi.py sanity                     # ~5s, verifica transport + ticker FIB6F vivo
python scripts\update_inventory_indici_futures_daily.py # recupera i 6 CME daily 28/05 mancanti + dump 29/05 dove disponibili
```

Vincoli operativi:
- **DGo + Darwin aperti** (porta 10003 storica, porta 10001 realtime)
- **TradingView Directa CHIUSO** (vincolo D-6)
- **Una sola istanza Darwin** attiva (no race su socket)
- Account `B6086` (privato — non scriverlo in chiaro nei commit)

### 5.1 V-1 cattura realtime — finestra morning

**Alle 09:00:00 CET** (lo script attende se lanci prima):
```powershell
python scripts\probe_dapi.py v1-capture --window morning --tickers FIB6F,DITAS
```

Durata: 30 minuti. Output:
- `probe_out/v1_morning_20260529.raw.log` — ogni linea ricevuta col timestamp host
- `probe_out/v1_morning_20260529.decoded.csv` — eventi parsati (kind, ticker, time, last, raw)

### 5.2 V-1 cattura realtime — finestra afternoon

**Alle 14:30:00 CET**:
```powershell
python scripts\probe_dapi.py v1-capture --window afternoon --tickers FIB6F,DITAS
```

### 5.3 V-1 fetch storico delle stesse finestre

Subito dopo la cattura (stesso giorno, per confronto T+0):
```powershell
python scripts\probe_dapi.py v1-fetch --date 2026-05-29 --tickers FIB6F,DITAS
```

Output: `probe_out/v1_hist_20260529_fetched_<timestamp>.csv` — barre 1-min storiche per le due finestre.

### 5.4 V-1 compare locale vs storico

```powershell
python scripts\probe_dapi.py v1-compare `
    --capture probe_out\v1_morning_20260529.decoded.csv `
    --hist    probe_out\v1_hist_20260529_fetched_<timestamp>.csv
```

Output: `probe_out/v1_compare_<timestamp>.json` con `summary` (matches/mismatches) e `diffs` (primi 200 mismatch).

**Domani 30/05**: rilanciare `v1-fetch --date 2026-05-29` per confronto T+1 (verifica aggiustamenti notturni CANDLERANGE su barre già passate).

### 5.5 V-2 cut-off temporale CANDLERANGE

Eseguibile in qualsiasi momento (no dipendenza temporale):
```powershell
python scripts\probe_dapi.py v2-cutoff --tickers FIB6F,DITAS,CM.MESM6 --period 60
python scripts\probe_dapi.py v2-cutoff --tickers FIB6F,DITAS,CM.MESM6 --period 86400
```

Range standard: `50, 80, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 160` giorni indietro.

Output: `probe_out/v2_cutoff_period<N>_<timestamp>.csv` con (ticker, days_requested, candles_received, first_ts, last_ts, err_code, end_marker).

**Cosa cerchiamo**: il punto di rottura — cioè il valore N oltre cui la query torna 0 candele o ERR. Coerente con Appendice A.2 (limite empirico ~100 giorni intraday DAPI).

---

## 6. Output finale atteso

Quando V-1 e V-2 sono completati con dati:
1. **Comporre `tasks/PROBE_RECUPERO_GAP_DAPI.md`** con tabelle risultati V-1 (equivalenza realtime/CANDLERANGE/T+1) e V-2 (cut-off giorni calendario vs trading)
2. Commit + push: `[PROBE] V-1 equivalenza + V-2 cut-off CANDLERANGE — risultati empirici 2026-05-29`
3. **NON aprire CAP-DATA-03**. Questo probe è prerequisito tecnico, non capitolo metodologico.

---

## 7. Punti aperti / promemoria

- Decodificare codici mese Directa-IDEM per **Mar** e **Dic** (sondare con SUB di un ticker trimestrale e leggere `ANAG.descrizione`)
- 6 CME daily 28/05 da recuperare al primo run di `update_inventory_*.py` di oggi
- `inventory_indici_futures_daily.csv` ha path hardcoded all'overlay — futuro fix architetturale (Claude CLI: questa è una nota per il futuro, non bloccante)
- Backup off-site di `preserved_from_overlay/` (29 MB) consigliato (artifacts ML1 + probe SUB20 — non riproducibili)
- DITAS aggiungere nei tickers V-1 se vuoi un controllo "cash index" stabile durante 9:00-9:30 (mercato MIB aperto, DITAS pubblica tick)

---

## 8. Cosa NON fare

- Non toccare `C:\directa_history_parametric_export_overlay\exports\directa_history_ml2\` (progetto ML2 vivo)
- Non cancellare `preserved_from_overlay/` (29 MB di archeology preservata stanotte)
- Non aprire DGo o TradingView Directa simultaneamente con il probe in corso (vincolo D-6)
- Non aprire/chiudere socket 10001/10003 a raffica (cooldown server)
- Non scrivere `account_code` (`B6086`) in file committati
- Non aprire CAP-DATA-03 prima di aver completato il probe e committato `PROBE_RECUPERO_GAP_DAPI.md`

---

## 9. File di riferimento da leggere se serve dettaglio

- `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md` (Appendici A/B con probe storici già fatti)
- `scripts/probe_dapi.py` (docstring iniziale + decoder)
- `scripts/update_inventory_indici_futures_daily.py` (lista hardcoded dei 16 simboli supportati)
- `.claude/CLAUDE.md` (istruzioni orchestratore del workflow metodologico — applicabili SOLO se il task fosse un CAP-XX, NON per questo probe)

---

**Fine handoff.** Buon V-1.
