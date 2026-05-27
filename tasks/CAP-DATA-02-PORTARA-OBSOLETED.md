# CAP-DATA-02 (Portara) — OBSOLETED

> **⚠️ Sostituito dal nuovo CAP-DATA-02 (DAPI runtime). Contenuto operativo assorbito o rinviato. Non procedere su questo file.**

L'identificatore `CAP-DATA-02` viene **riusato per il nuovo scope DAPI runtime** (Parte 9 del documento metodologico v2). Vedere `tasks/CAP-DATA-02.md` (task card normativo) e `tasks/ORCH_INSTRUCTIONS_CAP-DATA-02.md` (prompt-template per l'apertura della nuova sessione) per il flusso corrente.

---

## Scope storico abbandonato

Il vecchio `CAP-DATA-02` era citato nel task card di CAP-DATA-01 (`tasks/CAP-DATA-01.md` riga 8) come:

> "Task operativo gemello (fuori doc metodologico): **CAP-DATA-02 — Specifica della richiesta tecnica a Portara**"

Era pensato come task operativo gemello, esterno al documento metodologico v2, da pubblicare in `docs/operations/` (NON `docs/methodology_v2/`). Si occupava di:
- specifica della richiesta tecnica al vendor Portara (formato dati, campi richiesti, roll log, periodo storico)
- conferma del roll rule effettivo (3 giorni calendar vs trading, default N=3 di CAP-DATA-01 §3.3)
- protocollo di consegna dei dati storici back-adjusted Portara/CQG

## Motivazione dell'abbandono

In sessione di consulenza esterna del 2026-05-27 il supervisore ha riordinato la roadmap del progetto:
- **Parte 9 del doc v2** non è più Appendici A-G (rinviate a Parte 10 o oltre)
- **Parte 9 del doc v2** è ora `CAP-DATA-02 — Pipeline runtime FIB su Directa DAPI` (nuovo scope)
- L'identificatore `CAP-DATA-02` viene **riusato** per il nuovo scope DAPI runtime
- La specifica tecnica Portara originale del vecchio CAP-DATA-02 **non è più necessaria nell'orizzonte corrente del progetto**: la PHASE-B di acquisto storico Portara non è imminente (richiede prima la pipeline runtime DAPI funzionante); quando diventerà rilevante, sarà un nuovo task (CAP-DATA-03 o altro) NON ereditato da questo file

## Eredità documentale residua

Le citazioni storiche a `CAP-DATA-02` nel task card di CAP-DATA-01 (`tasks/CAP-DATA-01.md` righe 8, 53, 86, 162, 165, 185) restano **leggibili come storico**: si riferiscono al vecchio scope Portara e non al nuovo. Non vengono modificate per preservare l'audit trail della sessione CAP-DATA-01 (chiusa PASS Review v2 commit `6ba6186` del 2026-05-27).

I `data/sessions/README.md` e altri file pubblicati da CAP-DATA-01 che citano "CAP-DATA-02" come task gemello sono altresì lasciati invariati: leggono il vecchio scope.

Quando in futuro emergerà necessità della specifica tecnica Portara originale, il supervisore aprirà un nuovo task ID (es. `CAP-DATA-03` o equivalente) — NON sarà una continuazione di questo file.

## Non procedere su questo file

Nessun ulteriore lavoro va eseguito su `CAP-DATA-02-PORTARA-OBSOLETED.md`. Il file è conservato come **traccia storica del ri-scoping** del 2026-05-27.
