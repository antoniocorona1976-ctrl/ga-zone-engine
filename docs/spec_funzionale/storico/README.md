# storico/ — blocchi B1..B8 della ricostruzione cieca (SPEC-FUNZ-01)

Questi 8 file (`SPEC_FUNZ_01_B1.md` … `SPEC_FUNZ_01_B8.md`) sono i **blocchi-fonte** della ricostruzione cieca a 8 blocchi (modalità B) della specifica funzionale SPEC-FUNZ-01. Ogni blocco è stato scritto in una sessione separata, cieco rispetto agli altri e alla versione precedente, e chiuso PASS singolarmente.

**Sono materiale storico / di tracciabilità.** Il documento di specifica funzionale **unico e autoritativo** è `docs/spec_funzionale/SPEC_FUNZ_01.md`, ottenuto dall'**assemblaggio loss-less** di questi 8 blocchi (SPEC-FUNZ-01-ASSEMBLY, chiuso PASS `9b2a10f`, 2026-06-27). La tabella di mapping nella Sez.11 dell'assemblato collega ogni requisito finale (`R-x.y` / `CN-x.y` / `NFR-x.y`) al suo ID-blocco originario (`B?-…-NN`), per cui questi file restano la prova di provenienza.

| Blocco | Tema | Sezione nell'assemblato |
|---|---|---|
| B1 | Ambito & operatore | Sez.1 + Sez.2 |
| B2 | Payload del segnale | Sez.3 |
| B3 | State-machine & lifecycle | Sez.4 |
| B4 | Emissione & consegna Telegram | Sez.5 + Sez.6 |
| B5 | Runtime DAPI, sessione & compliance | Sez.7 |
| B6 | Schema-dato DAPI & continuità tape | Sez.9 |
| B7 | Gate di go-live | Sez.8 |
| B8 | Confine / fasizzazione PHASE-2 & dipendenze aperte | Sez.10 |

**Non modificare** questi file: sono congelati come storico (i marcatori PASS originali — B1 `7195ffe`, B2 `b858a88`, B3 `10ade01`, B4 `8500159`, B5 `5ec899c`, B6 `a5cfa80`, B7 `37d2166`, B8 `09cc7d9` — restano il riferimento; gli emendamenti AUDITFIX-01 `392a3f5` e i micro-pass dell'assemblaggio sono coperti dalle rispettive review). Per ogni esigenza usa il documento autoritativo assemblato.
