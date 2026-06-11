# SPEC — Check statici (CH1 + CH2)

> Specifica di uno strumento deterministico, fail-fast, eseguito prima dell'audit ostile e (a regime) in CI/pre-deposito.
> Questo è un documento di **requisiti per l'infrastruttura**, NON l'implementazione. L'implementazione è un task di sviluppo (Stream D) che passa per il loop normale.
> **Fallback** finché non implementato: il Reviewer esegue questi controlli manualmente (modalità degradata).

## Scopo
Verificare in modo deterministico le proprietà che NON richiedono giudizio:
- **CH1 — fatto esterno**: ogni requisito CH1 ha un valore che combacia con la fonte vendorizzata.
- **CH2 — coerenza interna**: ogni requisito ha le proprietà formali richieste e non contraddice gli altri (controlli decidibili).

## Input
- `docs/spec_funzionale/SPEC_FUNZ_*.md`
- `docs/spec_funzionale/TRACCIABILITA.md`
- `data/reference/*` (fonti vendorizzate per CH1)

## Controlli CH1 (source-match)
- Ogni REQ taggato CH1 cita una `Fonte` esistente in `data/reference/`.
- Il `Check deterministico` è presente e ha un `Atteso`.
- Il valore in `Atteso` combacia con la fonte (match esatto o regola dichiarata). Mismatch → ERRORE.

## Controlli CH2 (coherence lint)
- **ID**: ogni REQ ha ID nel formato `REQ-FUNZ-NN-XXX`, univoco in tutto il corpus.
- **Out-of-scope**: presente e non vuoto.
- **Unità**: ogni soglia numerica porta un'unità esplicita (es. "punti FIB", "minuti", "giorni").
- **Tracciabilità**: ogni REQ ha riga corrispondente in `TRACCIABILITA.md`.
- **Canale**: ogni REQ ha esattamente un canale ∈ {CH1, CH2, CH3, CH4}.
- **Stato coerente**: CH3 in VALIDATO solo se Esito=CONFERMATA; CH4 VALIDATO solo se Ratifica=RATIFICATO; CH1 VALIDATO solo se check verde.
- **Contraddizioni decidibili**: coppie di soglie sullo stesso parametro con valori incompatibili (es. due "validità max" diverse) → ERRORE.

## Output
- Exit code 0 = tutto verde; ≠0 = almeno un ERRORE.
- Report `reports/CHECK_STATICI_SPEC_FUNZ_NN.txt`: per ogni errore → REQ-ID, controllo, evidenza `file:riga`.

## Note di confine (cosa il lint NON fa → è del Reviewer)
- NON giudica se un requisito *fosse* da classificare CH1 (laundering): solo che un CH1-taggato abbia il check.
- NON valuta contraddizioni semantiche non decidibili (assunzioni implicite divergenti).
