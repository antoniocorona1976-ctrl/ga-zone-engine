# ISTRUZIONI_M0-T1_v2 — Loader fixture ISP → griglia canonica 13-campi

**Etichetta: NON AUDITATO.** Sostituisce integralmente la v1 (STOP a §0.4 del 05/07: `source` non fissato — risolto qui con DEC-C/DEC-D).

---

## REGOLA N.1 — ESITO SEMPRE SU FILE

**Ogni uscita di questa esecuzione — COMPLETATO, STOP a precondizioni, errore, blocco guard — termina scrivendo `Codice/Piano_di_lavoro/Esito/ESITO_M0-T1.md`** (intestazione con data/ora e verdetto: COMPLETATO / STOP-§x / BLOCCO-GUARD). In chat solo 5 righe di riassunto. Nessuna eccezione: se ti fermi, il motivo dello stop sta NEL FILE.

## USO (protocollo file-bus)

Questo file è stato trascinato nella finestra CLI. Primo atto di filing: copialo tu in `Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_M0-T1_v2.md` (AC non salva file a mano).

---

RUOLO: `prog_developer` (role file `.claude/agents/prog_developer.md`). TDD: test PRIMA del codice. GC-4: letture di spec/piano per range, mai dump integrali. RM-1/RM-2 su ogni affermazione (path:riga; alternative escluse per le prove empiriche).

INQUADRAMENTO: il modulo M0 del piano resta uno; M0-T1 (fixture, questo task) / M0-T2 (tape pagato, futuro) è sequenziamento del Planner, non modifica del piano.

## 0. Precondizioni — su fallimento: STOP + ESITO (Regola n.1)

1. `git log --oneline -5`: presenti `774f9d3` (v1.1), `4b877db`, `bb8d625`, pushati, branch in pari.
2. `tasks/STATO_CORRENTE.md`: nessun altro task in slot.
3. Fixture presente: `data/samples/portara_isp/ISP2023Z.txt` (~52.499 byte).

## 0-bis. Registrazione decreti (ordine del Planner — eseguire verbatim)

1. In `Codice/Piano_di_lavoro/DECISIONI.md`, append alla tabella (mai riscrivere righe esistenti) queste due righe esatte:

```
| DEC-C | 05/07/2026 | Dataset di training M0 (griglia 13-campi: serie ratio, Panama, unadjusted e fixture ISP): campo `source` = `PORTARA` per tutte le barre, reali e sintetiche (la sinteticità è portata da `bar_synthetic`). Estensione del dominio alla famiglia training | CN-9.8 (dominio chiuso runtime: DIRECTA, AGG_FROM_60s, AGG_FROM_D) | APERTO — track Spec/Metodologia (clausola training-side) |
| DEC-D | 05/07/2026 | Dataset di training M0: `symbol` = `FIB` (identità di contratto nel sidecar/nome file, mai in `symbol`); `timeframe` = token della convenzione del decoder legacy, estratto da export_directa_history_parametric.py con citazione path:riga; in assenza di token univoco: `1min` | — | — |
```

2. Se `tasks/STATO_CORRENTE.md` non registra la chiusura v1.1: append riga `FASE-CODICE: v1.1 chiusa — commit 774f9d3.`
3. Commit dedicato (add espliciti dei soli file toccati): `DECISIONI: DEC-C (source=PORTARA) + DEC-D (symbol/timeframe M0); STATO: v1.1 chiusa` + push. Nel testo nuovo evita la famiglia "verific*"; se `rm_guard` scatta: STOP + ESITO, chiedi override ad AC.

## 1. Apertura slot

`tasks/ACTIVE_TASK.md`: intestazione `# TASK ATTIVO: M0-T1 — loader fixture ISP → griglia canonica 13-campi` + riferimento a questa card (commit incluso nel commit finale).

## 2. Layout (decisione Planner)

Codice: `src/data_layer/` (nuova). Test: `tests/data_layer/` (nuova). Python del repo; `pytest`; `pandas`/`numpy` ammessi. Altre dipendenze: STOP + ESITO e chiedi.

## 3. Perimetro M0-T1 (solo fixture)

1. **Accertamento empirico del formato sample** (PROVA-EMPIRICA, RM-1): mappatura delle 9 colonne; discriminante settle-row (atteso `volume = 0` — riprova o cita la prova agli atti, alternative escluse); controllo d'ordine colonne (flat bars / settle row); accertamento timezone (prima/ultima barra reale per giornata; il loader prende `tz` come parametro esplicito e normalizza a CET).
2. **Parser** sample → barre 1-min del contratto singolo, settle-row filtrate.
3. **Grid builder** → griglia canonica per sessione **08:00–22:00 CET** (R-9.3): 840 righe/giorno, passo 60s, `timestamp` SOB chiave (CN-9.9), `date`/`time` derivati.
4. **Forward-fill** minuti no-trade: `O=H=L=C=Close precedente`, `Volume=0`, `tick_count=0` (R-9.3), `bar_synthetic=True`; barra presente nel file → `bar_synthetic=False` (semantica storica R-9.14). `tick_count` da colonna sample se esiste, altrimenti `NULL` (CN-9.7).
5. **Output CSV**: header 13 campi esatti, quest'ordine (CN-9.5, `docs/spec_funzionale/SPEC_FUNZ_01.md:1335`): `symbol, timeframe, timestamp, date, time, open, high, low, close, volume, tick_count, bar_synthetic, source`. Tipi per CN-9.7. Valori: `source=PORTARA` (DEC-C), `symbol=FIB` e `timeframe` per DEC-D.
6. **Diagnostica tick-grid**: rileva off-tick (incluso il noto `30319`), li logga come finding — nessun clamping, nessun drop.

## 4. Done-when — tutti test `pytest` verdi sulla fixture

- **T1** Parser legge `ISP2023Z.txt` integralmente senza eccezioni; conteggi: righe raw, settle-row filtrate, barre valide.
- **T2** Zero settle-row nell'output; discriminante documentato con alternative escluse (RM-1).
- **T3** Header = 13 campi esatti e in ordine (CN-9.5); tipi CN-9.7; `date`/`time` coerenti con `timestamp` (CN-9.9); su tutte le righe `source=="PORTARA"`, `symbol=="FIB"`, `timeframe` == token DEC-D (citazione decoder nell'ESITO).
- **T4** Per ogni giornata completa: esattamente 840 timestamp, monotoni, passo 60s, 08:00–21:59 CET post-normalizzazione; zero buchi, zero duplicati.
- **T5** Minuti no-trade: regola forward-fill R-9.3 e `bar_synthetic=True`; minuti presenti nel sample: `bar_synthetic=False`.
- **T6** Determinismo: due run → output byte-identico (hash uguale).
- **T7** Diagnostica tick-grid rileva `30319`, lo riporta senza alterare la barra; ogni altro off-tick elencato o dichiarato assente.
- **T8** Test timezone: stampa prima/ultima barra reale per giornata e asserisce coerenza col `tz` dichiarato.

## 5. Out-of-scope — vietato

Tape pagato 12 colonne; 2 serie consegnate; derivazione unadjusted; cross-check ratio; sidecar roll (→ M0-T2). Feature/segnali (M3/M4). Directa/DAPI in ogni forma — nessun probe (D-6). Modifiche a CAP, spec, piano, METODO.md, role file. Modifiche a DECISIONI.md oltre il §0-bis. Archivio condiviso (M8a).

## 6. Commit finale e push

Add espliciti: `src/data_layer/`, `tests/data_layer/`, `tasks/ACTIVE_TASK.md`, `Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_M0-T1_v2.md`, `Codice/Piano_di_lavoro/Esito/ESITO_M0-T1.md`. Staging estraneo → STOP + ESITO.
Commit: `M0-T1: loader sample ISP -> griglia canonica 13-campi (fixture) - test verdi`
Poi `git push`. Guard: come §0-bis.3.

## 7. Contenuto dell'ESITO (`Esito/ESITO_M0-T1.md`)

Verdetto in testa; esito precondizioni e §0-bis (hash commit decreti); mappatura colonne + prove (RM-1); tz accertato; token `timeframe` con citazione decoder; output `pytest` integrale T1–T8; conteggi; finding tick-grid; hash commit finale + push; `git status --short` finale.
