# Calendario sessioni FIB — note non normative

Questo documento descrive il file `fib_session_calendar.csv` e raccoglie i metadati non normativi su fonti, ambiguita' e convenzioni di interpretazione delle epoche storiche delle sessioni di negoziazione del contratto FIB sul mercato IDEM.

Il file `fib_session_calendar.csv` e' **normativo**: la sua semantica e il suo contenuto sono congelati nel documento metodologico v2, Parte 8, Cap.41. Questo `README.md` e' invece **non normativo**: documenta provenienza, livello di confidenza dei dati e ambiguita' residue. La fonte autoritativa per il contenuto del CSV resta la tabella riportata nel doc v2 Parte 8 Cap.41 e in `tasks/ACTIVE_TASK.md` sezione "Dati di input recuperati dall'Orchestratore".

## Schema del CSV

Il file `fib_session_calendar.csv` ha 6 colonne:

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `epoch_id` | identificatore | Codice univoco dell'epoca (E1, E2, E3, E4, E5). Crescente nel tempo. |
| `start_date` | data ISO 8601 | Primo giorno di calendario in cui l'epoca e' in vigore. |
| `end_date` | data ISO 8601 | Ultimo giorno di calendario in cui l'epoca e' in vigore (giorno PRIMA della `start_date` dell'epoca successiva). Per l'epoca corrente E5, la `end_date` e' la data di consultazione (2026-05-27); il calendario va esteso quando emergeranno nuove epoche. |
| `session_open_local` | orario locale `HH:MM` | Orario di apertura della sessione di **negoziazione continua**, escludendo la fase di asta di apertura. |
| `session_close_local` | orario locale `HH:MM` | Orario di chiusura della sessione di negoziazione continua. |
| `timezone` | stringa | Fuso orario locale (sempre `CET`). La conversione automatica a `CEST` quando in vigore (ultima domenica di marzo → ultima domenica di ottobre) e' gestita dalla pipeline coerentemente con la semantica eventi/timestamp del doc v2. |

Il CSV ha 1 riga header + 5 righe dati (E1, E2, E3, E4, E5). Non contiene altre colonne, in conformita' al task card §3.5 del documento metodologico v2 Parte 8.

## Sotto-tabella fonti e ambiguita'

Per ciascuna epoca o per ciascun confine temporale, la tabella seguente riporta la fonte consultata, la data di consultazione ISO e le note di ambiguita' identificate. Le marcature **DATA DA VERIFICARE** segnalano gli elementi che richiedono conferma in CAP-DATA-02 (richiesta tecnica a Portara) o in PHASE-B (acquisizione storico Portara), tipicamente via roll log.

| epoca / confine | fonte_url | data_consultazione_ISO | note ambiguita' |
|-----------------|-----------|------------------------|-----------------|
| E1 (data inizio) | https://www.bankpedia.org/termine.php?c_id=20457 | 2026-05-27 | Lancio mercato IDEM 1994-11-28 confermato da bankpedia e Wikipedia IDEM; prima negoziazione FIB30 quel giorno. Sottostante: indice MIB30 (predecessore di FTSE MIB, transizione MIB30 → S&P/MIB → FTSE MIB avvenuta nel 2003-2004 e poi 2009; il contratto FIB e' continuativo nella serie Portara back-adjusted). |
| E1 (orari 09:15-17:30 CET) | https://www.borsaitaliana.it/borsaitaliana/ufficio-stampa/comunicati-stampa/2000/000613minifib.htm | 2026-05-27 | Orari **09:15-17:30 CET** confermati per il 2000 dal comunicato lancio miniFIB. **DATA DA VERIFICARE**: la fonte conferma gli orari nel 2000, NON il periodo intero 1994-2010. Possibili modifiche intermedie non documentate dalle fonti consultate. Si assume continuita' 1994-2010 in mancanza di evidenze contrarie. |
| E1 → E2 (data fine 2010-11-07) | https://www.thetradenews.com/borsa-italiana-derivatives-market-moves-to-sola-platform/ + Avviso Borsa n.15413 del 21/10/2010 | 2026-05-27 | Migrazione SOLA dichiarata per 2010-11-08 (Avviso n.15413: "IDEM - SOLA migration: postponement to 8th November 2010"). **DATA DA VERIFICARE**: l'associazione fra migrazione SOLA e cambio orari 09:15→09:00 / 17:30→17:40 e' un'inferenza non documentata esplicitamente nelle fonti consultate. Plausibile ma non confermata. |
| E2 (orari 09:00-17:40 CET) | https://www.borsaitaliana.it/borsaitaliana/ufficio-stampa/comunicati-stampa/2015/orarinegoziazione.htm | 2026-05-27 | Orari **09:00-17:40 CET** derivati per **inferenza inversa** dal comunicato Borsa Italiana del 2015 che cita "17:40 (IDEM - calcolato dalla differenza)" come orario precedente all'estensione a 17:50. L'orario di apertura 09:00 e' coerente con il modello IDEM noto e con il comunicato 2017 (`https://www.borsaitaliana.it/derivati/derivati/estensioneorarifibeminifib.en.htm`) che dichiara come orari pre-2017 "9 am to 5.50 pm CET". **DATA DA VERIFICARE**: la transizione 09:15→09:00 e 17:30→17:40 non e' documentata da un comunicato ufficiale diretto nei risultati delle ricerche. |
| E2 → E3 (estensione 17:40 → 17:50 il 2015-11-23) | https://www.borsaitaliana.it/borsaitaliana/ufficio-stampa/comunicati-stampa/2015/orarinegoziazione.htm | 2026-05-27 | Data **2015-11-23** confermata da comunicato Borsa Italiana ufficiale. Cita esplicitamente IDEM equity derivatives: "fase di negoziazione continua viene estesa fino alle 17.50" con "posticipamento di 10 minuti rispetto alla chiusura precedente" (17:40). |
| E3 → E4 (estensione 17:50 → 20:30 il 2017-07-03) | https://www.borsaitaliana.it/borsaitaliana/ufficio-stampa/comunicati-stampa/2017/idem.en.htm + https://www.borsaitaliana.it/derivati/derivati/estensioneorarifibeminifib.en.htm | 2026-05-27 | Data **2017-07-03** confermata da comunicato Borsa Italiana ufficiale: "As from today, IDEM ... has extended its trading hours" (data pubblicazione 2017-07-03). Orari: "continuous trading from 09:00 to 20:30" con sessione diurna 09:00-17:50 e serale 17:50-20:30, single continuous session (no pausa). Per la metodologia del doc v2, la sessione e' trattata come finestra continua singola: il marker 17:50 NON e' una pausa di mercato. |
| E4 → E5 (estensione 20:30 → 22:00 il 2020-02-17) | https://www.borsaitaliana.it/borsaitaliana/ufficio-stampa/comunicati-stampa/2020/estensioneorariidem.htm + https://www.borsaitaliana.it/derivati/nuovi-orari-di-negoziazione-fib-e-minifib.en.htm | 2026-05-27 | Data **2020-02-17** confermata da comunicato Borsa Italiana ufficiale: "a partire da oggi, 17 febbraio 2020". Orari: "Dalle 07:45 alle 8:00 la fase di asta di apertura (pre-asta, validazione, apertura) e dalle 8:00 fino alle 22:00 la negoziazione in continua". Per la metodologia (sessione = continuous trading), `session_open_local=08:00`. |

## Sintesi metadati ambiguita'

Le seguenti ambiguita' restano aperte al momento della consegna di CAP-DATA-01:

1. **Orari di E1** sono parzialmente derivati per inferenza: gli orari **09:15-17:30 CET** sono verificati solo per l'anno 2000 (lancio del miniFIB), non per l'intero periodo 1994-2010. Transizioni intermedie non documentate dalle fonti consultate sono possibili.
2. **Confine E1/E2 alla data 2010-11-08** e' inferito dalla migrazione SOLA (data documentata) ma il cambio orari da 09:15→09:00 e 17:30→17:40 associato a quella migrazione **non e' documentato esplicitamente** dai comunicati Borsa Italiana consultati.
3. **Orari di E2** (09:00-17:40 CET) sono derivati per **inferenza inversa** dal comunicato 2015 che cita 17:40 come orario precedente. L'apertura 09:00 e' coerente con il modello IDEM ma non e' documentata da un comunicato specifico per il periodo 2010-2015.
4. Le date **2015-11-23**, **2017-07-03**, **2020-02-17** sono **confermate** da comunicati Borsa Italiana ufficiali e non presentano ambiguita'.

## Procedura di riesame del calendario

Il calendario completo va riesaminato in due punti del roadmap del progetto:

- **CAP-DATA-02** (task gemello operativo, fuori scope dal doc v2): richiesta tecnica a Portara per riesame puntuale delle epoche storiche, con verifica delle date di switch via roll log Portara o conferma diretta dal vendor.
- **PHASE-B** (acquisizione storico Portara, FASE-B del roadmap): l'acquisto e la consegna dei dati Portara potrebbero contenere metadati addizionali sulle epoche storiche del FIB; le epoche del calendario `fib_session_calendar.csv` vanno riconciliate con i metadati Portara prima di considerare il calendario congelato per il training operativo.

Eventuali aggiornamenti al CSV richiedono un nuovo ciclo Planner per la conferma normativa nel doc v2 Parte 8 Cap.41.

## Riferimenti incrociati al doc v2

- `docs/methodology_v2/CAP_08_parte_8.md` Cap.41 — Timeline ufficiale delle sessioni FIB (definizione normativa, riferisce a questo CSV)
- `docs/methodology_v2/CAP_01_parte_I.md` Capitolo 1 — Obiettivo operativo (sessione 8:00-22:00 CET corrente, coerente con E5)
- `docs/methodology_v2/CAP_02_parte_II.md` Capitolo 7 — Stati del segnale e state machine (Q-01: sessione continua)
