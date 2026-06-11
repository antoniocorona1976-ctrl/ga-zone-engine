# TRACCIABILITÀ — business-spec ga-zone-engine

> Mappa: requisito → §metodologia (a monte) → canale → modulo (a valle, futuro Stream B–E).
> Aggiornata dal Developer a ogni requisito prodotto. Verificata dal Reviewer.
> Una riga per requisito. "Modulo" resta vuoto finché il codice non esiste.

| REQ-ID | Titolo breve | §Metodologia | Canale | Stato | Modulo (futuro) |
|---|---|---|---|---|---|
| REQ-FUNZ-00-001 | Metrica di successo primaria | §<...> | CH4 | BLOCCATO | — |
| REQ-FUNZ-01-003 | Orario di sessione | §<...> | CH1 | BOZZA | — |
| REQ-FUNZ-02-001 | Banda di entrata | — (prodotto) | CH2 | BOZZA | — |
| REQ-FUNZ-04-002 | Soglia di target netto | §<...> | CH3 | BLOCCATO | — |

## Regole
- Ogni REQ DEVE avere una riga. Un REQ senza riga = FAIL in review.
- `§Metodologia` = "—" solo se il requisito è una decisione di prodotto pura (e in tal caso, nel SPEC_FUNZ, Tracciabilità a monte = N/A).
- `Stato` riflette il SPEC_FUNZ (BOZZA/VALIDATO/BLOCCATO) e deve restare coerente con esso.
- `Modulo` si compila in fase di codice: chiude il ponte spec↔implementazione (lo scopo per cui questa mappa esiste).
