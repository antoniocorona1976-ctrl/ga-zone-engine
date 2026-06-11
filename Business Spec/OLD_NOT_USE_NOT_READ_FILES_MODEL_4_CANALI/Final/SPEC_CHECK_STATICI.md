# SPEC — Check statici (CH1 + CH2)

> Specifica di uno strumento deterministico, fail-fast, eseguito prima dell'audit ostile e (a regime) in CI/pre-deposito.
> Questo è un documento di **requisiti per l'infrastruttura**, NON l'implementazione. L'implementazione è un task di sviluppo (Stream D) che passa per il loop normale.
> **Fallback** finché non implementato: il Reviewer esegue questi controlli manualmente (**modalità degradata, non deterministica** — vedi nota in coda).
> Revisione [REV-4CH-audit]: aggiunti controlli per N1 (proposizione singola), N2 (presenza provenienza CH1 + coerenza stato), N3 (presenza classe trigger CH4), F1 (presenza citazione verbatim).
> **Raccomandazione di sequenza**: costruire **questo lint CH2 per primo** (è codice, non richiede dati né harness). Chiude la finzione della modalità degradata (F4), scarica le proprietà CH2 dall'attenzione dell'agente (mitiga il carico cognitivo, M1), e dà al Reviewer un gate deterministico vero.

## Scopo
Verificare in modo deterministico le proprietà che NON richiedono giudizio:
- **CH1 — fatto esterno**: ogni requisito CH1 ha un valore che combacia con la fonte vendorizzata, e porta il campo di provenienza.
- **CH2 — coerenza interna**: ogni requisito ha le proprietà formali richieste e non contraddice gli altri (controlli decidibili).

## Input
- `docs/spec_funzionale/SPEC_FUNZ_*.md`
- `docs/spec_funzionale/TRACCIABILITA.md`
- `data/reference/*` (fonti vendorizzate per CH1)

## Controlli CH1 (source-match + provenienza)
- Ogni REQ taggato CH1 cita una `Fonte` esistente in `data/reference/`.
- Il `Check deterministico` è presente e ha un `Atteso`.
- Il valore in `Atteso` combacia con la fonte (match esatto o regola dichiarata). Mismatch → ERRORE.
- **(N2)** Il campo `Fonte verificata da AC` è presente. Se = PENDING → lo stato del REQ DEVE essere BLOCCATO (non VALIDATO). Stato VALIDATO con provenienza PENDING → ERRORE.

## Controlli CH2 (coherence lint)
- **Proposizione singola (N1)**: l'enunciato esprime un solo concern verificabile. Euristica decidibile: segnala enunciati che congiungono concern eterogenei (es. una soglia numerica legata a una scelta d'intento, o due soglie su parametri diversi nello stesso enunciato). I casi genuinamente ambigui si **escalano al Reviewer** (il lint segnala il sospetto, non chiude il giudizio).
- **ID**: ogni REQ ha ID nel formato `REQ-FUNZ-NN-XXX`, univoco in tutto il corpus.
- **Out-of-scope**: presente e non vuoto.
- **Unità**: ogni soglia numerica porta un'unità esplicita (es. "punti FIB", "minuti", "giorni").
- **Tracciabilità**: ogni REQ ha riga corrispondente in `TRACCIABILITA.md`. **(F1)** Se `§Metodologia` ≠ N/A, il campo citazione verbatim nel SPEC_FUNZ è presente e non vuoto (il lint verifica la *presenza* della citazione; la *fedeltà* è del Reviewer, asse 6).
- **Canale**: ogni REQ ha esattamente un canale ∈ {CH1, CH2, CH3, CH4}.
- **(N3)** Ogni REQ CH4 porta il campo `Classe rollback trigger` ∈ {pre-deployment, solo-live}, presente e non vuoto.
- **Stato coerente**: CH3 in VALIDATO solo se Esito=CONFERMATA; CH4 VALIDATO solo se Ratifica=RATIFICATO; CH1 VALIDATO solo se check verde **E** `Fonte verificata da AC` ≠ PENDING.
- **Contraddizioni decidibili**: coppie di soglie sullo stesso parametro con valori incompatibili (es. due "validità max" diverse) → ERRORE.

## Output
- Exit code 0 = tutto verde; ≠0 = almeno un ERRORE.
- Report `reports/CHECK_STATICI_SPEC_FUNZ_NN.txt`: per ogni errore → REQ-ID, controllo, evidenza `file:riga`.

## Note di confine (cosa il lint NON fa → è del Reviewer)
- NON giudica se un requisito *fosse* da classificare CH1 (laundering): solo che un CH1-taggato abbia il check e la provenienza.
- NON valuta contraddizioni semantiche non decidibili (assunzioni implicite divergenti).
- **(F1)** NON giudica se la citazione verbatim *sostiene davvero* l'enunciato → Reviewer asse 6; verifica solo che esista.
- **(N1)** NON decide i casi di atomicità genuinamente ambigui: li segnala al Reviewer.
- **(N2)** NON verifica che la fonte vendorizzata sia fedele al mondo: quello è ratifica AC, non meccanica.

## Nota sulla modalità degradata (F4)
Finché il lint non è implementato, il Reviewer esegue questi controlli a mano. Un "verde manuale" NON è deterministico né esaustivo (unicità ID su tutto il corpus, contraddizioni tra capitoli distanti, sfuggono alla lettura umana proprio dove un linter è infallibile). Il Reviewer tratta un verde-manuale come **confidenza inferiore** a un verde-lint e lo dichiara nella review. È il motivo per cui il lint CH2 va costruito per primo.
