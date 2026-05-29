# METODO — regole metodologiche permanenti del progetto ga-zone-engine

**Scopo**: definire le regole di processo che si applicano a TUTTI gli agenti (Orchestrator, Planner, Developer, Reviewer) e a TUTTI gli output (CAP-XX, probe, script, handoff, decisioni di design). Sono regole **vincolanti**, non opzionali.

**Versionamento**: ogni regola ha un ID univoco `RM-N`. Non vengono cancellate, solo deprecate. Modifiche significative producono `RM-N v2`, e mantengono lo storico.

**Origine**: queste regole nascono da incidenti reali documentati nei commit di progetto. Ogni regola cita il caso che ha richiesto la sua introduzione.

---

## RM-1 — Verifica vs assunzione compatibile coi dati

### Enunciato

Quando un test lascia più di una conclusione compatibile con i dati osservati, l'output deve essere etichettato **"verifica parziale"** e deve nominare esplicitamente le ipotesi alternative ancora aperte. È **vietato** chiamare "verificato" un risultato che non escluda tutte le permutazioni alternative.

### Cosa significa in pratica

Per ogni asserzione del tipo `X = ...` ottenuta da un test:
- elencare le **alternative compatibili coi dati osservati** (anche solo enumerandole)
- per ciascuna, dichiarare se è stata esclusa dal test e con quale evidenza
- se restano alternative non escluse, l'asserzione si scrive `X ∈ {opzione_a, opzione_b}` o equivalentemente "verifica parziale, da disambiguare con test mirato Y"

### Formato obbligatorio

In ogni report, documento o commento di codice che dichiari "verificato":

```
VERIFICA: <asserzione>
PROVE: <quali dati osservati, quale test eseguito>
ALTERNATIVE COMPATIBILI ESCLUSE: <elenco esplicito>
ALTERNATIVE COMPATIBILI NON ESCLUSE: <elenco esplicito — se non vuoto, l'asserzione è "parziale">
```

### Caso reale che ha motivato la regola

Commit `7bb2955` (sessione web 28/05/2026): dichiarato "verificato schema CANDLE = `O;L;H;C`" da test su candela daily FIB6F. Il test mostrava {L=min, H=max} in posizioni 2,3 — ma non distingueva O da C in posizioni 1,4 (sui valori non-estremi). L'asserzione corretta era *"L,H verificati in pos 2,3; O e C indistinguibili sui daily, due alternative compatibili {O;L;H;C, C;L;H;O}"*. Lo schema reale (`C;L;H;O`) è stato scoperto solo con V-1 il giorno dopo, con prova diretta tick-by-tick. La sessione web aveva propagato l'errore in 2 file (handoff + probe_dapi.py) e nel codice che il CLI locale ha eseguito.

### Quando si applica

- Sempre. Su CAP-XX, su probe, su script, su scoperte tecniche, su decisioni di design.
- Non c'è esenzione "perché è una cosa piccola": l'errore di stanotte era esattamente di questo tipo.

---

## RM-2 — Grep nel repo prima di assumere un formato esterno

### Enunciato

Prima di assumere come è strutturato il payload di un sistema esterno (broker, API, protocollo, file format), eseguire una passata sistematica nel codebase per trovare tutti i parser/decoder/codec già esistenti per quel sistema, e leggere prima quelli (incluso i commenti). Il codice esistente che ha già funzionato in produzione è quasi sempre più affidabile della documentazione ufficiale del sistema esterno.

### Cosa significa in pratica

Prima di scrivere codice che decodifica un payload esterno:

1. `grep -rn "<NOME_PROTOCOLLO>\|parse_<X>\|decode_<X>\|UFF\|APE\|<KEYWORDS_DEL_DOMINIO>" --include='*.py' --include='*.md'`
2. Aprire i risultati, leggere i commenti, copiare le mapping
3. Se non c'è nulla in repo, allora consultare la documentazione esterna come fallback

Se trovi un decoder esistente, non assumere mai un formato divergente senza prima provare empiricamente che il decoder esistente è sbagliato.

### Formato obbligatorio

Nei commit message di nuovi parser/decoder per sistemi esterni, includere una sezione:

```
Decoder/parser esistenti già nel repo per <sistema>:
- <path:line>: <descrizione breve di cosa decodifica>
- <path:line>: ...
(oppure "Nessuno trovato dopo grep su <pattern>")
```

### Caso reale che ha motivato la regola

Stesso commit `7bb2955`. Riga 477 di `scripts/export_directa_history_parametric.py` contiene esattamente:

```python
# Documentazione Directa: UFF, MIN, MAX, APE => close, low, high, open.
close_v = Decimal(uff)
low_v   = Decimal(min_)
high_v  = Decimal(max_)
open_v  = Decimal(ape)
```

Cioè il decoder di produzione **dichiarava lo schema reale `C;L;H;O`** ed era già committato in `main` da settimane. La sessione web del 28/05 ha letto quel file (due volte, per altri scopi) **senza fare grep su `parse_directa_candle`/`UFF`/`APE`**. Bastava un grep di 5 secondi.

### Quando si applica

- Sempre, prima di scrivere o assumere il formato di:
  - protocolli DAPI (CANDLE, PRICE, ANAG, BOOK_5, ERR, ecc.)
  - payload Telegram (messaggi, update, callback)
  - formati di file (CSV, JSON manifest, ecc.)
  - qualunque schema di scambio dati con sistema esterno

---

## RM-3 — Documentazione ufficiale dei sistemi esterni non è fonte di verità

### Enunciato

Dopo che almeno una volta una documentazione ufficiale di un sistema esterno (es. wiki Directa) è stata dimostrata inesatta, da quel momento la documentazione è trattata come **suggestione iniziale**, mai come fonte di verità. La verità sta nei **dump reali misurati** + **commenti del codice di produzione che ha già processato quei dump**.

### Cosa significa in pratica

Ordine di priorità delle fonti per determinare un fatto su un sistema esterno:

1. **Prove empiriche dirette** (test live contro il sistema con ground truth indipendente). Es: V-1 che confronta tick realtime con campi della candela.
2. **Codice di produzione esistente nel repo** che ha già parsato/usato quel formato, con relativi commenti.
3. **Documenti operativi committati nel repo** (Appendici di indagine, dump testuali di probe).
4. **Documentazione ufficiale del sistema esterno** (wiki, PDF, API reference) — solo come *hint iniziale*, mai come ultima parola.

Una conclusione basata solo sul livello 4 senza supporto dai livelli 1–3 è **inammissibile**.

### Formato obbligatorio

Nei documenti e nei commenti di codice, ogni riferimento a documentazione esterna va etichettato con la sua qualità di fonte:

```
[WIKI-HINT, da verificare]    — riferimento a wiki/docs esterni, valore di hint
[CODICE-EXISTENTE r.NNN]      — citazione di decoder già in repo
[PROVA-EMPIRICA <data>]       — risultato di test diretto
```

### Caso reale che ha motivato la regola

Wiki Directa dichiara CANDLE `O;H;L;C`. Schema reale è `C;L;H;O`. Quindi il wiki è inaffidabile sullo schema candele. La sessione web del 28/05 ha trattato il wiki come "fonte da emendare il minimo possibile" → ha generato `O;L;H;C` come "permutazione minima del wiki sotto vincolo L=pos 2, H=pos 3" → schema sbagliato. Una volta che una fonte ti ha mentito su un campo, devi sospettare di tutto il resto: non emendare, ricominciare da prova diretta.

### Quando si applica

Sistemi esterni attualmente nel perimetro:

- **Wiki Directa DAPI** (`app1.directatrading.com/...`) — già dimostrato inesatto sullo schema CANDLE
- **Telegram Bot API docs** — non ancora testato, ma da trattare con la stessa cautela (livello 4 = hint, livello 1–3 = verità)
- **CME / Eurex documentation** — quando arriveremo a usarle direttamente
- **Portara / vendor dati storici** — idem

---

## RM-4 — Output tecnici determinanti vanno revisionati prima del commit

### Enunciato

Il workflow di review formale Planner→Developer→Reviewer copre i capitoli metodologici (CAP-XX). Ma ci sono altri output che, pur non essendo capitoli, hanno **impatto determinante** sul motore: probe empirici, script di parsing, handoff fra sessioni, decisioni tecniche citate come fatti. Questi output **non possono essere committati senza review esplicita**.

### Cosa significa in pratica

Output soggetti a RM-4 (lista non esaustiva):

- **Script di parsing/decoder** di payload di sistemi esterni (es. `probe_dapi.py`, futuri `telegram_consumer.py`, ecc.)
- **Documenti di handoff fra sessioni** che dichiarano "fatti verificati" (es. `tasks/HANDOFF_*.md`, `tasks/RIPRESA_*.md`)
- **Probe/spike empirici** i cui risultati saranno citati nei CAP successivi (es. `tasks/PROBE_*.md`, `tasks/INDAGINE_*.md`)
- **Scoperte tecniche dichiarate come "M-promemoria"** che entreranno in CARRYOVER

### Modalità di review per output non-CAP

Due opzioni accettabili:

**A. Self-review esplicita dell'autore prima del commit**

L'agente che produce l'output esegue un blocco di self-review ostile, formalizzato in fondo al documento o nel commit message, con:
- Lista delle asserzioni dichiarate "verificato"
- Per ognuna: check RM-1 (alternative escluse) + RM-2 (grep fatto) + RM-3 (fonte primaria)
- Lista delle assunzioni non testate ma usate come premesse
- Lista dei file/commenti del repo letti durante l'analisi (a riprova di RM-2)

**B. Review formale dal reviewer agent**

L'orchestratore invoca il reviewer in **modalità leggera** (probe-review): audit ostile focalizzato sui 4 punti seguenti:
1. RM-1: dichiarazioni di verifica hanno alternative escluse esplicite?
2. RM-2: grep nel repo eseguito? decoder esistenti citati?
3. RM-3: fonti esterne etichettate `[WIKI-HINT]`? conclusioni hanno supporto da livelli 1–3?
4. Onestà: claim asseriti hanno evidenza puntuale (file:linea o test:risultato)?

### Caso reale che ha motivato la regola

Sessione web 28/05: ha prodotto `scripts/probe_dapi.py` (588 righe nuove con decoder DAPI) + `tasks/HANDOFF_PROBE_DAPI_20260528.md` (207 righe con 6 "fatti verificati") + 2 PR. **Zero review.** Lo schema CANDLE sbagliato è entrato in `main` come fact-of-truth e ha contagiato la sessione CLI successiva. Se RM-4 fosse stata attiva, una self-review esplicita (opzione A) avrebbe forzato a scrivere "schema CANDLE: alternative compatibili coi soli daily = {O;L;H;C, C;L;H;O}, da disambiguare con test intraday" → il CLI avrebbe disegnato V-1 come **test di disambiguazione**, non come ri-conferma di un fatto già dato.

### Quando si applica

- Sempre, su qualunque output che soddisfi almeno UNA delle condizioni della lista sopra.
- Non c'è esenzione "perché è veloce", "perché è notte", "perché è solo un probe".

---

## Convenzioni di update di questo file

- Nuove regole RM-N nascono solo da **incidenti documentati**: un commit/file che cita il caso reale che ha richiesto la regola.
- Regole esistenti non si cancellano, si deprecano (es. `RM-1 v2 — sostituisce v1 (vedi commit X)`).
- Tutti gli agenti (Orchestrator, Planner, Developer, Reviewer) leggono questo file come parte del loro contesto operativo. La lettura è **prima** di qualunque altra azione, **dopo** la lettura del proprio prompt sistema.
- Update di questo file richiede commit dedicato `[METODO] descrizione`, mai mescolato ad altri cambiamenti.

## Riferimenti

- `tasks/CARRYOVER.md` — M-promemoria metodologici **del documento v2** (CAP-XX), namespace `M-N`
- `tasks/STATO_CORRENTE.md` — single source of truth dello stato del progetto, namespace M-note tecniche di sessione
- `.claude/CLAUDE.md` — orchestratore: si aspetta che tutti gli agenti rispettino RM-1..RM-4
- `.claude/agents/*.md` — i 3 sub-agenti hanno blocchi specifici di applicazione RM-1..RM-4
