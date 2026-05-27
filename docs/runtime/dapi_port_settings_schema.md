# Schema del file `APIPortSettings.txt` — Directa DAPI

> **Scopo**: documentare il formato del file di configurazione locale di Directa DAPI (`APIPortSettings.txt`) **senza esporre l'account code** del file reale. Questo schema è il riferimento normativo del runtime: il file reale **NON deve essere committato** nel repo perché contiene l'account code in chiaro.

---

## Localizzazione del file reale

Path tipico (Windows):
```
%USERPROFILE%\.directa\engine\APIPortSettings.txt
```

Path equivalente Unix-style usato nella documentazione interna:
```
~/.directa/engine/APIPortSettings.txt
```

Il file è prodotto dal gateway Darwin di Directa al primo avvio e aggiornato automaticamente quando il gateway viene riconfigurato. Non viene mai scritto direttamente dalla pipeline runtime: lo schema è in **sola lettura** per la pipeline.

---

## Formato della riga

Il file contiene **una singola riga** (terminata da newline) con quattro campi separati da `;`:

```
<account>;<rt>;<trd>;<hist>
```

### Esempio anonimizzato

```
<ACCOUNT>;10001;10002;10003
```

Il file **reale** ha al posto di `<ACCOUNT>` il codice account Directa in chiaro (es. `B6086` per l'account corrente nel probe del 2026-05-27 documentato in `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md`). **L'account code non va committato** per ragioni di sicurezza / privacy.

### Spiegazione dei campi

| Posizione | Nome canonico | Tipo | Significato |
|-----------|---------------|------|-------------|
| 1 | `account` | stringa alfanumerica | Codice account Directa del cliente (formato tipico `[A-Z]\d{4,}`, es. `B6086`). Identificatore dell'account abilitato al servizio DAPI sulla macchina locale. È un **identificatore**, NON una credenziale di autenticazione (vedi sezione "Modello di sicurezza" sotto). |
| 2 | `rt` | intero TCP port | Porta locale (`127.0.0.1`) per il **datafeed realtime** (push tick + book + anagrafica). Valore standard `10001`. |
| 3 | `trd` | intero TCP port | Porta locale per la **submission ordini di trading**. Valore standard `10002`. **Fuori scope** per la pipeline ga-zone-engine (vincolo "solo emissione segnale, nessuna esecuzione" del progetto). |
| 4 | `hist` | intero TCP port | Porta locale per le **richieste storico** (`CANDLE`, `CANDLERANGE`, `TBT`, `TBTRANGE`). Valore standard `10003`. |

### Valori di default Directa

Per tutti gli account standard Directa il triplo porte è invariato `10001/10002/10003`. Le porte sono configurabili nel pannello del gateway Darwin, ma la riconfigurazione non è prassi standard. La pipeline runtime ga-zone-engine **legge** i valori dal file e li usa per connettersi al gateway: non assume valori hard-coded.

---

## Modello di sicurezza

1. **Locale-only**: il gateway Darwin di Directa accetta connessioni esclusivamente su `127.0.0.1` (loopback). Non esiste configurazione remote.
2. **Account code = identificatore, non credenziale**: l'autenticazione al servizio DAPI è implicita nella sessione Darwin (l'utente è già loggato nel gateway). Il valore in `APIPortSettings.txt` serve al gateway per associare i comandi della pipeline alla sessione utente attiva. Non è una password e non garantisce accesso da remoto.
3. **Single-account per macchina**: la pipeline gira sulla **stessa macchina** dell'account abilitato. Non è supportata l'esecuzione in cloud / da remoto con un account locale: rompe il modello di sicurezza Directa.
4. **No commit dell'account code**: pur essendo un identificatore e non una credenziale, l'account code va trattato come dato sensibile / PII (lega un'azione di mercato a una persona fisica). Va escluso dal repo via `.gitignore` o convenzione operativa.

---

## Conflitto con DGo / TradingView Directa

Quando il gateway Darwin è già impegnato da una sessione DGo (piattaforma Directa) o da TradingView con plugin Directa, i socket locali a `127.0.0.1:10001/10003` sono in **conflitto** con eventuali connessioni della pipeline ga-zone-engine.

La pipeline runtime DEVE:
1. Rilevare il conflitto via `ConnectionRefusedError` o `ERR;<cmd>;<codice>` ripetuti immediatamente dopo connessione
2. Marcare lo stato come `RUNTIME_DEGRADED` nel log di audit
3. Notificare il supervisore (manualmente: fermare DGo / TradingView prima di lanciare la pipeline)
4. **NON** tentare workaround automatici (es. retry continuo, fallback su altre porte): si tratta di una decisione operativa dell'utente, non di un guasto transitorio

Questa regola è documentata in memoria persistente del progetto (`feedback_no_dapi_probe_con_dgo_aperto`).

---

## Relazione con il task card CAP-DATA-02

Il task card CAP-DATA-02 (`tasks/CAP-DATA-02.md`) cita questo schema come riferimento normativo per:
- la sezione architettura del canale DAPI (Cap.YY.2 del doc metodologico Parte 9)
- la gestione errori e recovery (Cap.YY.6)
- il modello di sicurezza locale-only (Gap-1 obbligatorio)

Il Developer della sessione CAP-DATA-02 leggerà questo file e citerà lo schema dei 4 campi (`account`, `rt`, `trd`, `hist`) nella sezione architettura del capitolo, **senza esporre il valore reale dell'`account` corrente**. L'esempio nel capitolo deve usare il placeholder `<ACCOUNT>` come in questo schema.

---

## Riferimenti

- `tasks/INDAGINE_DIRECTA_CROSS_INDEX.md` — probe empirico del 2026-05-27 con banner Darwin `DARWIN_STATUS;CONN_OK;TRUE;Release 2.5.1 build 04/02/2025` su account `B6086` (porte `10001/10002/10003`)
- `tasks/ORCH_INSTRUCTIONS_CAP-DATA-02.md` — istruzioni di apertura sessione CAP-DATA-02
- `tasks/CAP-DATA-02.md` — task card normativo CAP-DATA-02
- Wiki ufficiale Directa DAPI: `https://app1.directatrading.com/trading-api-directa/index.html`
