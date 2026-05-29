# Re-Review AUDIT-RM-RETRO CAP-DATA-01 (Parte 8) — Iter.3 — perimetro C, D patchati

**Sede**: CLI (accesso al filesystem locale; dump `probe_out/*.json` ispezionabili).
**Natura**: Re-Review Iter.3 dei 7 finding approvati dal supervisore (NON CAP-review piena, NON nuovo audit del perimetro A-D). Verifica puntuale finding-per-finding della chiusura nel rework.
**Ruolo Reviewer** assunto da agente general-purpose (subagente nativo `reviewer` non disponibile; ruolo adottato in pieno secondo `.claude/agents/reviewer.md`, incluse regole assolute e divieti per sede `:163-164`).

**Commit auditati**:
- `e444c33` ([AUDIT-RETRO] patch C+D — chiusura 7 finding Review v1)
- `4bc870f` ([AUDIT-RETRO] report ridotto rework Iter.2)

**Perimetro della Re-Review** (solo C, D patchati + report; A/B intatti, A/B/opzione-A NON ri-auditati per mandato):
- C = `scripts/probe_dapi.py`
- D = `tasks/HANDOFF_PROBE_DAPI_20260528.md`
- Report = `reports/REPORT_AUDIT_RM_RETRO_CAP_DATA_01.md`

**Cross-reference fuori perimetro (citate, NON auditate)**:
- `scripts/export_directa_history_parametric.py` — decoder/comandi DAPI canonico `[CODICE-ESISTENTE]`
- Dump locali `probe_out/w4_errcodes_20260529.json`, `probe_out/w6_cooldown_20260529.json` — `[PROVA-EMPIRICA 2026-05-29]`, ispezionati in sede CLI come supporto evidenziale.

---

## VERDETTO: PASS (Sede: CLI)

Tutti e 7 i finding approvati sono **chiusi correttamente**. I 2 BUG REALI (#1 W4 codici errore, #2 W6 cooldown) sono riscritti nel formato 4-righe RM-1 sia in C sia in D, e le rispettive asserzioni `[PROVA-EMPIRICA 2026-05-29]` sono **corroborate dai dump locali** ispezionati in CLI. Le verifiche parziali residue (1030 non riprodotto; soglia/durata cooldown in burst non disambiguati) sono **oneste e marcate parziali**, non dichiarate risolte. I 5 MIGLIORA PROCESSO (#3-#7) sono chiusi con le etichette/annotazioni richieste, verificate contro il decoder canonico. C↔D coerenti; nessuna regressione nel decoder `parse_line`; vecchio testo in D inequivocabilmente etichettato "superato".

La lista "Empirico-CLI residua" è **non vuota** ma contiene solo voci genuinamente rinviate (ticker gated/mercato aperto, fonti interne, Eurex/CME canonicamente Parte 9), tutte già marcate come verifiche parziali in C/D: per mandato del task la loro presenza **NON blocca il PASS**.

---

## Tabella finding-per-finding

| # | Finding (W-N) | File:linea della patch | Chiuso? | Evidenza |
|---|---------------|------------------------|---------|----------|
| 1 | W4 codici errore 1004/1007/1017/1030 semantica | C `probe_dapi.py:32-60`; D `HANDOFF:60-101` | **CHIUSO** | Blocco 4-righe RM-1 presente in C `:33-44` (VERIFICA/PROVE/ALTERNATIVE ESCLUSE/ALTERNATIVE NON ESCLUSE) e in D `:64-90`. `[PROVA-EMPIRICA 2026-05-29]` corroborata da `probe_out/w4_errcodes_20260529.json`: 1004 (HELP/INFO 2 porte), 1007 (ZZZNOPE storico+realtime), 1017 (period 2° arg + few args), nuovi 1015 (data invalida) e 1003 (storico su realtime). 1030 marcato "NON riprodotto / verifica parziale" (C `:42-44,59-60`; D `:78,86,90`). |
| 2 | W6 cooldown ~30s / 14ª connessione | C `probe_dapi.py:74-87`; D `HANDOFF:111-137` | **CHIUSO** | Blocco 4-righe RM-1 presente in C `:77-87` e D `:115-129`. `[PROVA-EMPIRICA 2026-05-29]` corroborata da `probe_out/w6_cooldown_20260529.json`: 3 cicli × 25 conn ~1Hz su 10003 (75 tot), tutte `ok:true`, `onset_connection:null`. "14 come costante" REFUTATA; "~30s" e burst>>1Hz/mercato aperto marcati ALTERNATIVE NON ESCLUSE (parziale). |
| 3 | W2/W3 END CANDLES + ordine arg CANDLERANGE | C `probe_dapi.py:22-30`; D `HANDOFF:50,58` | **CHIUSO** | Etichetta `[CODICE-ESISTENTE r.245 ...]` per END CANDLES (C `:23`, D `:58`) e `[CODICE-ESISTENTE r.228-230 ...]` per CANDLERANGE period-ultimo (C `:29`, D `:50`). Righe canoniche verificate (vedi "Verifica citazioni canoniche" sotto): corrispondono. |
| 4 | W9 ticker Eurex/CME senza evidenza | C `probe_dapi.py:66-72` | **CHIUSO** | C `:67-68` annota "solo IDEM/FIB6F testato `[PROVA-EMPIRICA]`"; Eurex/CME `[WIKI-HINT, da verificare CLI]` (C `:69-70`); C `:71-72` "ordine MONTH/YEAR Eurex/CME da confermare via ANAG a mercato aperto e canonicizzare in Parte 9". |
| 5 | W8 banner docstring vs decoder | C `probe_dapi.py:102-110` | **CHIUSO** | Docstring `:102-110` allineata: dichiara che il decoder matcha SOLO il prefisso `DARWIN_STATUS`, etichetta la forma piena `;CONN_OK;TRUE` come `[WIKI-HINT, da verificare]`, cita banner reale `blen=142` `[PROVA-EMPIRICA]`. Decoder `parse_line:235` matcha `startswith("DARWIN_STATUS")` — coerente. blen=142 confermato nel dump w6. |
| 6 | RM-3 etichette fonte assenti | C, D (globale) | **CHIUSO** | Etichette `[PROVA-EMPIRICA]`/`[CODICE-ESISTENTE]`/`[WIKI-HINT]`/`[DOC-INTERNO]` introdotte nelle asserzioni toccate: legenda C `:9-12`; wiki smentito C `:15`, D `:42`; I=Set `[DOC-INTERNO App. B.2]` C `:63`, D `:106`. |
| 7 | RM-1 formato 4-righe assente | C, D (globale) | **CHIUSO** | Formato 4-righe applicato a #1 (W4) e #2 (W6) in C e D dove obbligatorio; W5 mantiene forma "verifica parziale" dichiarata (Mar/Dic "da decodificare"). |

**Sintesi**: 7/7 finding chiusi.

---

## Esito verifica dump empirici (sede CLI)

Entrambi i dump dichiarati nel report (`REPORT_AUDIT_RM_RETRO_CAP_DATA_01.md:24`) **esistono** in `probe_out/` e **corroborano** le asserzioni `[PROVA-EMPIRICA]`.

### `probe_out/w4_errcodes_20260529.json` (3158 byte, mtime 2026-05-29 23:19)

Contenuto vs asserzioni di D `:68-90` e C `:45-60`:
- `candlerange_period2nd` (period 2° arg) → `sample: ["ERR;;1017"]` ✓ corrobora 1017=sintassi strutturale.
- `candlerange_fewargs` → `ERR;;1017` ✓.
- `candlerange_baddate` (`notadate`) → `sample: ["ERR;1015;20260218000000;20260529231925"]` ✓ corrobora il codice NUOVO 1015=data invalida, distinto da 1017 (esclude l'alternativa "1017 ampio").
- `candlerange_badticker` (ZZZNOPE storico) → `ERR;ZZZNOPE;1007` ✓; `rt_sub_fake` (SUB ZZZNOPE realtime) → `ERR;ZZZNOPE;1007` ✓.
- `hist_helpcmd`/`rt_helpcmd`/`rt_info` → `ERR;HELP;1004` (2 porte) e `ERR;INFO;1004` ✓ corrobora 1004=comando ignoto su entrambe le porte.
- `rt_candlerange_on_rt` (storico su porta realtime) → `ERR;N/A;1003` ✓ corrobora il codice NUOVO 1003.
- 1030: **assente dal dump** — coerente con la dichiarazione "NON riprodotto, verifica parziale, Empirico-CLI a mercato aperto" (D `:78,86,90`; C `:42-44,59-60`). Onestà RM-1 confermata.

**Nota minore (NON finding bloccante)**: nel record `candlerange_baddate` il campo riassuntivo `err_codes` riporta `"20260218000000"` invece di `"1015"` — è un artefatto del parser che ha preso `p[2]` su una riga ERR a layout diverso (`ERR;1015;...` ha il codice in `p[1]`). Il campo `sample` raw è corretto e mostra `ERR;1015;...`, su cui poggiano le asserzioni di C/D. L'asserzione "1015=data invalida" resta corroborata dalla riga raw. Segnalo solo per trasparenza; non incide sul verdetto (i blocchi RM-1 citano la riga `ERR;...` ricevuta, non il campo riassuntivo `err_codes` del dump).

### `probe_out/w6_cooldown_20260529.json` (9516 byte, mtime 2026-05-29 23:22)

Contenuto vs asserzioni di D `:117-129` e C `:78-87`:
- 3 cicli, ciascuno `n_ok_before_onset: 25`, `onset_connection: null`, `recovery_seconds: null`.
- Ogni `seq` ha 25 elementi, tutti `ok:true`, `err:null`, `blen:142`, cadenza `t` ~1Hz (Δ≈1.0-1.02s) ✓.
- 75 connessioni totali senza alcun onset ✓ corrobora la REFUTAZIONE di "14 come costante".
- `blen:142` uniforme ✓ corrobora W8 (banner reale lunghezza 142, campi extra oltre `;CONN_OK;TRUE`).
- "~30s durata cooldown" non osservabile (nessun cooldown) → marcato NON ESCLUSO/parziale ✓.

**Conclusione dump**: esistono e corroborano. Nessuna asserzione `[PROVA-EMPIRICA]` contraddetta dai dump. Non ho rieseguito alcun probe contro DGo (divieto `reviewer.md:164` — nessuna asserzione puntuale è risultata dubbia dopo l'ispezione dei dump esistenti; rispetto del cooldown M-5).

---

## Verifica citazioni canoniche (RM-2 — grep eseguito da me, AC-10)

Grep eseguito direttamente (tool Grep, sede CLI):
```
pattern: parse_directa_candle|UFF|is_error_line|CANDLERANGE|END CANDLES   (path scripts/)
```
Esito — decoder/parser DAPI nel repo: **solo 2 file** — `scripts/probe_dapi.py` e `scripts/export_directa_history_parametric.py`. Nessun decoder aggiuntivo non noto (coerente col report `:61` "Nessun decoder DAPI aggiuntivo oltre i due noti").

Verifica puntuale delle righe citate dalle etichette `[CODICE-ESISTENTE]` del rework (lettura diretta del file canonico):
- **r.228-230** (`export_directa_history_parametric.py`): f-string `f"CANDLERANGE {symbol} {start_dt...} {end_dt...} {period_seconds}"` → period_seconds in **ultima** posizione. **Corrisponde** all'asserzione W2 (period ultimo) etichettata in C `:29` e D `:50`. ✓
- **r.245** (`export_directa_history_parametric.py`): stringa di warning contenente il marker testuale `END CANDLES` ("...nessun END CANDLES ricevuto..."). Il marker `END CANDLES` è genuinamente usato dal tool di produzione. **Corrisponde** sostanzialmente all'asserzione W3 etichettata in C `:23` e D `:58`. ✓ *(Sfumatura: r.245 è una stringa di warning che nomina il marker, non l'unico punto di definizione; il marker compare anche altrove nel file. Citazione sostanzialmente corretta, non fuorviante — non è finding.)*
- **r.477-481**: commento `# Documentazione Directa: UFF, MIN, MAX, APE => close, low, high, open.` + `close_v=Decimal(uff)`/`low_v=Decimal(min_)`/`high_v=Decimal(max_)`/`open_v=Decimal(ape)`. **Corrisponde** allo schema CANDLE `C;L;H;O;V` del decoder di C. ✓

---

## Coerenza inter-file e regressioni

### C ↔ D
- **Schema CANDLE**: C `:14`, decoder `:248-270` = `C;L;H;O;V`; D §3.1 `:36` = `C;L;H;O;V`. Coerenti. ✓
- **Codici errore**: C `:45-60` e D `:68-90` riportano la stessa tabella rivista (1004/1007/1017/1015/1003 + 1030 parziale). Coerenti. ✓
- **Cooldown**: C `:77-87` e D `:115-129` riportano la stessa conclusione (75 conn ~1Hz, nessun cooldown, 14 refutata). Coerenti. ✓
- Nessuna divergenza non etichettata fra C e D.

### Decoder `parse_line` (NON doveva essere toccato)
- Diff del commit `e444c33` su `probe_dapi.py`: i due hunk modificati sono entrambi nella **docstring** (range righe 4-113). Il corpo `parse_line` (`:230-318`) **non è nel diff** → nessuna regressione.
- Verifica positiva di coerenza col canonico: `parse_line:264-267` mappa `p[4]→close (UFF)`, `p[5]→low (MIN)`, `p[6]→high (MAX)`, `p[7]→open (APE)` = identico a `export_directa_history_parametric.py:478-481`. Coerente con `:477`. ✓ (Significato di "coerente" verificato enumerando ed escludendo le 3 divergenze possibili: ordine dei 5 campi, mapping nome→OHLC, indice di colonna — tutte coincidono.)

### Vecchio testo in D etichettato "superato"
- D §3.1 `:40` "**Testo originale del 28/05 (conservato per storia, ora superato):**" + schema barrato `~~O;L;H;C;V~~` (`:36`). ✓
- D §3.4 `:92` "**Testo originale del 28/05 (conservato per storia, ora superato):**" + tabella vecchia citata come "superato" `:101`. ✓
- D §3.6 `:133` "**Testo originale del 28/05 (conservato per storia, ora superato):**" + nota "superato" `:137`. ✓
- Grep `O;L;H;C|O;H;L;C` su C e D: tutte le occorrenze sono marcate "INESATTO"/"ERRATO"/"superato"/wiki-smentito (C `:15,16,251`; D `:36,42`). **Nessuna** ripropone lo schema vecchio come fatto valido. ✓

---

## Empirico-CLI residua (NON blocca il PASS)

Voci genuinamente rinviate, già marcate come verifiche parziali oneste in C/D:

| W-N | Asserzione residua | File:linea | Stato | Perché rinviata |
|-----|--------------------|-----------|-------|-----------------|
| W4 / 1030 | semantica 1030 (market data realtime non sottoscritto) | C `:59-60`; D `:78,86,90` | parziale dichiarata | richiede ticker realtime gated a mercato aperto |
| W6 (burst) | soglia/durata cooldown sotto burst >>1Hz o a mercato aperto | C `:84-87`; D `:129` | parziale dichiarata | il test ~1Hz/75conn non lo esclude |
| W5 | `I`=Settembre (conferma); Mar/Dic da decodificare | C `:63-64`; D `:106-107` | parziale dichiarata | SUB ticker trimestrale + ANAG a mercato aperto |
| W9 | ticker Eurex `EU.`/CME `CM.` ordine MONTH/YEAR | C `:69-72` | `[WIKI-HINT]` dichiarato | ANAG su Eurex/CME; canonicamente Parte 9 |

Tutte e 4 sono dichiarate "verifica parziale"/`[WIKI-HINT]`/"da confermare CLI" nei file: onestà RM-1 rispettata. Per mandato del task, la loro presenza non impedisce il PASS.

---

## Applicazione RM a me stesso (AC-9/10/11)

- **AC-9 (RM-1)**: la mia asserzione "decoder `parse_line:264-267` coerente con canonico `:478-481`" è verificata enumerando le 3 divergenze cercate ed escluse (ordine 5 campi, mapping nome→OHLC, indice colonna). La mia asserzione "i dump corroborano" è ancorata a ispezione diretta dei due file `probe_out/*.json` (sede CLI, accesso legittimo): non ho dichiarato "verificato empiricamente" nulla che richieda esecuzione contro DGo — mi sono limitato ai dump già prodotti. Le voci Empirico-CLI residue NON sono dichiarate da me né verificate né falsificate: le riporto come parziali.
- **AC-10 (RM-2)**: grep eseguito da me e citato sopra (pattern + esito: solo 2 decoder). Conclusione sui decoder esistenti basata su grep diretto + lettura delle righe canoniche r.228-230/r.245/r.477-481, non su assunzione.
- **AC-11 (RM-3)**: ogni riferimento ai file del perimetro è file:linea testuale, nessuna parafrasi "a memoria". Riferimenti al canonico citati con file:linea.
- **Working tree**: nessun file del perimetro (C/D) né A/B modificato da me; unico file scritto = questo review. `.claude/*` e `scheduled_tasks.lock` esclusi dal commit.

---

## Note di processo (NON finding)

1. Il record riassuntivo `err_codes` del dump w4 per `candlerange_baddate` è impreciso (riporta `20260218000000` invece di `1015`) per un artefatto di parsing del campo riassuntivo; la riga raw `sample` è corretta e le asserzioni C/D citano la riga raw. Non incide sul verdetto. Se in futuro il dump fosse citato direttamente come fonte machine-readable, valga la regola di leggere `sample` e non `err_codes`.
2. Le verifiche parziali residue (W4/1030, W6 burst, W5, W9) restano input per un'eventuale sessione CLI a mercato aperto, ma sono già correttamente recintate nei file e non costituiscono debito RM-1 aperto.

**Esito complessivo**: 7/7 finding chiusi, dump empirici esistenti e corroboranti, nessuna regressione, coerenza C↔D, vecchio testo etichettato superato. **VERDETTO: PASS.**
