# TRACCIABILITÀ — business-spec ga-zone-engine

> Mappa: requisito → §metodologia (a monte) → canale → modulo (a valle, futuro Stream B–E).
> Aggiornata dal Developer a ogni requisito prodotto. Verificata dal Reviewer.
> Una riga per requisito. "Modulo" resta vuoto finché il codice non esiste.
> Revisione [REV-4CH-audit]: aggiunta regola N5 (aggiornamento di stato cross-task dopo chiusura capitolo) e nota F1 (la § qui, la citazione verbatim nel SPEC_FUNZ).

| REQ-ID | Titolo breve | §Metodologia | Canale | Stato | Modulo (futuro) |
|---|---|---|---|---|---|
| REQ-FUNZ-00-001 | Metrica di successo primaria | §<...> | CH4 | BLOCCATO | — |
| REQ-FUNZ-01-003 | Orario di sessione | §<...> | CH1 | BLOCCATO | — |
| REQ-FUNZ-02-001 | Banda di entrata | — (prodotto) | CH2 | BOZZA | — |
| REQ-FUNZ-04-002 | Soglia di target netto | §<...> | CH3 | BLOCCATO | — |

## Regole
- Ogni REQ DEVE avere una riga. Un REQ senza riga = FAIL in review.
- `§Metodologia` = "—" solo se il requisito è una decisione di prodotto pura (e in tal caso, nel SPEC_FUNZ, Tracciabilità a monte = N/A).
- **(F1)** Questa tabella porta il **numero di §**. La **citazione verbatim** della frase di metodologia da cui il requisito deriva vive nel campo `Tracciabilità a monte` del `SPEC_FUNZ`. Il Reviewer (asse 6) verifica che la § citata sostenga l'enunciato; il lint verifica solo la presenza della riga e della citazione.
- `Stato` riflette il SPEC_FUNZ (BOZZA/VALIDATO/BLOCCATO) e deve restare coerente con esso.
- `Modulo` si compila in fase di codice: chiude il ponte spec↔implementazione (lo scopo per cui questa mappa esiste).

## (N5) Aggiornamento di stato dopo la chiusura del capitolo
Il ciclo di vita di un requisito **attraversa più task**: un CH3 nasce PENDING in `SPEC-FUNZ-NN`, ma viene CONFERMATA/FALSIFICATA dall'harness in un task **Stream-D successivo**, quando il capitolo NN è già PASS e chiuso. Aggiornare `Stato` qui e nel SPEC_FUNZ chiuso **non** è un'azione libera fuori da un task attivo (violerebbe "un solo task attivo / niente sviluppo fuori da current task").
- L'aggiornamento è eseguito via **micro-task pianificato dal Planner**: una **riapertura mirata del solo REQ** (non dell'intero capitolo), che il Planner apre quando l'harness produce un esito.
- Nessun agente modifica lo `Stato` di un requisito in un capitolo chiuso al di fuori di questo micro-task.
- Conseguenza accettata e dichiarata: un capitolo PASS con CH3 PENDING **non è "chiuso per sempre"** — è strutturalmente PASS, empiricamente in sospeso (distinzione PASS-strutturale vs VALIDATO-empirico).
