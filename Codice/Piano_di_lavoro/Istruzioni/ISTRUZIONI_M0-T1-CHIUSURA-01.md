# ISTRUZIONI_M0-T1-CHIUSURA-01 — Chiusura formale del ciclo M0-T1

**Etichetta: NON AUDITATO.** Ordinata dal Planner su RE-REVIEW PASS (`7d44349`).

---

## REGOLA N.1 — ESITO SEMPRE SU FILE

**Ogni uscita — completata, STOP, errore, blocco guard — termina scrivendo `Codice/Piano_di_lavoro/Esito/ESITO_M0-T1-CHIUSURA-01.md`** (data/ora + verdetto in testa). In chat solo 5 righe.

## USO (file-bus)

File trascinato nella finestra CLI. Primo atto: copialo tu in `Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_M0-T1-CHIUSURA-01.md`.

---

RUOLO: esecutore di stato (nessun build, nessun ruolo Dev/Review): solo append di stato e commit. VIETATO toccare: codice, test, piano, DECISIONI.md, ACTIVE_TASK.md (resta storico per convenzione — il marker in STATO governa lo slot), qualsiasi file fuori dai quattro del §3.

## 0. Precondizioni — su fallimento STOP + ESITO

1. `git log --oneline -3`: `7d44349` (RE-REVIEW M0-T1: PASS) presente e pushato, branch in pari.
2. Ultima riga di `tasks/DEV_STATUS.md` = `RE-REVIEW M0-T1: PASS — 2026-07-05`.
3. `tasks/STATO_CORRENTE.md` NON contiene già un marker `M0-T1: CHIUSO` (guardia di idempotenza).

## 1. Marker di chiusura in STATO_CORRENTE (append, mai riscrivere)

Append a `tasks/STATO_CORRENTE.md` esattamente questo blocco:

```
M0-T1: CHIUSO PASS 7d44349 (catena: bb8d625 ratifica → 774f9d3 v1.1 → adc30d1 build → 225057d review CONDITIONAL → e656315 fix → 7d44349 re-review PASS). Slot: LIBERO.
Prossimo task: M0-T2 (loader tape Portara pagato, 12 colonne, 2 serie + derivazione unadjusted) — GATED su consegna tape.
Vincoli d'acceptance M0-T2, non negoziabili (ereditati dal ciclo M0-T1): (1) contatore/report barre fuori sessione — finding #4 review; (2) riconferma discriminante settle-row sul tape (volume==0, eventuale raffinamento flat+fuori-sequenza); (3) riconferma ordine O/C con roll-log/dati contratto vendor; (4) semantica tickCount da documentazione tape; (5) gestione parzialità nei giorni interni (DEC-E, rinviata); (6) policy sessioni corte da calendario di borsa.
```

## 2. DEV_STATUS (append, mai riscrivere)

Append a `tasks/DEV_STATUS.md`: `CHIUSURA M0-T1: slot libero — 2026-07-05`

## 3. Commit e push

Add espliciti dei soli: `tasks/STATO_CORRENTE.md`, `tasks/DEV_STATUS.md`, `Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_M0-T1-CHIUSURA-01.md`, `Codice/Piano_di_lavoro/Esito/ESITO_M0-T1-CHIUSURA-01.md`. Staging estraneo → STOP + ESITO.
Commit: `CHIUSURA M0-T1: PASS (7d44349) - slot libero, vincoli M0-T2 registrati`
Push. Nel testo nuovo evita la famiglia "verific*"; se `rm_guard` scatta → STOP + ESITO, override solo su ok esplicito di AC.

## 4. Contenuto ESITO

Verdetto; esito precondizioni; le righe appese a STATO_CORRENTE e DEV_STATUS così come scritte (con numero riga), conferma che nessuna riga preesistente è stata riscritta; hash commit + conferma push; `git status --short` finale sul perimetro.
