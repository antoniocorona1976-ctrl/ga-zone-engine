# SPEC — Harness empirico (CH3)

> Specifica dello strumento che falsifica/conferma le claim CH3 contro i dati storici.
> Documento di **requisiti per l'infrastruttura**, NON l'implementazione. Implementazione = task di sviluppo (Stream D) nel loop normale.
> Esegue a **ipotesi singola**; gira dove vivono i dati (locale Portara/CQG), non è la ricerca GA (quella resta su AWS spot).

## Scopo
Dato un requisito CH3 con ipotesi falsificabile, eseguire il test definito e restituire CONFERMATA/FALSIFICATA con evidenza. Un requisito CH3 NON può passare a VALIDATO senza esito CONFERMATA da questo harness.

## Input (dal blocco CH3 del requisito)
- Ipotesi falsificabile.
- Dataset/finestra (default: Portara/CQG 1-min, back-adjusted continuo).
- Metrica.
- Soglia di accettazione + alternative da battere.
- Parametri purge/embargo.

## Procedura
1. Carica i dati nella finestra dichiarata.
2. Applica walk-forward con purge + embargo dichiarati (no leakage).
3. Calcola la metrica per la claim e per le alternative.
4. Applica il test di significatività dichiarato.
5. Verdetto: CONFERMATA se la claim batte le alternative alla soglia; altrimenti FALSIFICATA.

## Vincoli metodologici (invarianti — assert a runtime)
- Purge ed embargo non nulli e applicati (assert).
- Nessun dato post-finestra usato in-sample (assert no-leakage).
- Le alternative confrontate sono quelle dichiarate nel requisito, non scelte a posteriori.

## Output
- `reports/HARNESS_<REQ-ID>.md`: esito, metrica claim vs alternative, parametri, eventuali warning.
- Esito riportato nel blocco CH3 del requisito (PENDING → CONFERMATA/FALSIFICATA) dal Developer.

## Note di confine
- FALSIFICATA non significa "elimina il requisito": significa che l'enunciato (es. soglia 80) va rivisto. Torna al Planner come finding, non si auto-corregge.
- L'harness NON sceglie l'obiettivo (metrica) né le alternative: quelli sono input (decisione di task / CH4).
