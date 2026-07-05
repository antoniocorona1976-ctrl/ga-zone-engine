# ISTRUZIONI_M0-T1-FIX-01 — Chiusura findings review (#1 + DEC-E)

**Etichetta: NON AUDITATO.** Instradamento deciso da AC su REVIEW_M0-T1 (225057d): #1 → Developer; #4 → M0-T2; #2/#3/#6 ignorati; #5 chiuso qui con DEC-E.

---

## REGOLA N.1 — ESITO SEMPRE SU FILE

**Ogni uscita — completata, STOP, errore, blocco guard — termina scrivendo `Codice/Piano_di_lavoro/Esito/ESITO_M0-T1-FIX-01.md`** (data/ora + verdetto in testa). In chat solo 5 righe.

## USO (file-bus)

File trascinato nella finestra CLI. Primo atto: copialo tu in `Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_M0-T1-FIX-01.md`.

---

RUOLO: `prog_developer`. TDD. RM-1/RM-2. Il task attivo resta M0-T1 (ciclo di fix, nessun nuovo slot).

## 0. Precondizioni — su fallimento STOP + ESITO

1. `git log --oneline -3` contiene `225057d` (REVIEW M0-T1), pushato, branch in pari.
2. `tasks/DEV_STATUS.md` ultimo stato = review CONDITIONAL su M0-T1.

## 0-bis. Registrazione DEC-E (ordine del Planner — verbatim)

Append a `Codice/Piano_di_lavoro/DECISIONI.md` (mai riscrivere righe esistenti):

```
| DEC-E | 05/07/2026 | Griglia canonica di training M0: i giorni a copertura parziale ai BORDI del dataset (primo/ultimo giorno osservato, incompleti rispetto alla sessione 08:00–22:00) sono ESCLUSI, con conteggio ed elenco espliciti nel report del loader — mai scarto silenzioso. Parzialità nei giorni INTERNI = anomalia da riportare (gestione decisa in M0-T2). Sessioni corte da calendario di borsa: policy rinviata a M0-T2 (tape pluriennale + calendario) | — | — |
```

Commit dedicato (add esplicito del solo file): `DECISIONI: DEC-E (giorni di bordo esclusi e contati)` + push. Lessico: evita "verific*"; se `rm_guard` scatta → STOP + ESITO, override solo su ok AC.

## 1. Fix #1 — fixture committata + prova GC-3

1. `git add data/samples/portara_isp/ISP2023Z.txt` (SOLO questo path, niente cartelle intere) + commit `M0-T1-FIX: fixture ISP tracciata (GC-3)` + push.
2. Correggi le docstring che dichiarano il falso ("committata" quando non lo era): il testo deve descrivere lo stato reale (path della fixture, tracciata nel repo da questo commit).
3. **Prova GC-3 (acceptance):** crea un worktree pulito da HEAD (`git worktree add`), esegui lì l'intera suite `pytest` usando SOLO file tracciati: 8/8 verdi. Riporta comando, path del worktree, output integrale. Rimuovi il worktree a fine prova.

## 2. Implementazione DEC-E + test T9 (chiude finding #5)

1. Grid builder: escludi i giorni di bordo a copertura parziale; il report del loader espone `excluded_edge_days` con data e conteggio righe osservate per ciascuno (attesi sul sample: 2 giorni, 262 e 65), e segnala eventuali parzialità interne (attese: 0).
2. **T9**: test che pinna DEC-E — output della fixture = solo giornate complete (esattamente 840 righe, tutte del 14/12/2023); report con 2 giorni di bordo esclusi (262, 65); zero parzialità interne.
3. Aggiorna le asserzioni numeriche dei test esistenti alla nuova policy (griglia 840; sintetiche ricontate) documentando in ESITO ogni valore vecchio→nuovo con motivo. T1–T8 devono restare verdi nella nuova forma; T6 (determinismo, doppio run byte-identico) rieseguito.

## 3. Out-of-scope — vietato

Finding #4 (contatore barre fuori sessione → M0-T2, già vincolato); #2/#3/#6 (ignorati per decisione AC); tape pagato; qualsiasi file oltre: `data/samples/portara_isp/ISP2023Z.txt`, `src/data_layer/`, `tests/data_layer/`, DECISIONI.md (§0-bis), DEV_STATUS.md, card ed ESITO propri.

## 4. Commit finale e push

Add espliciti: `src/data_layer/`, `tests/data_layer/`, `Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_M0-T1-FIX-01.md`, `Codice/Piano_di_lavoro/Esito/ESITO_M0-T1-FIX-01.md`, `tasks/DEV_STATUS.md` (append: `FIX M0-T1: READY_FOR_RE-REVIEW — <data>`). Staging estraneo → STOP + ESITO.
Commit: `M0-T1-FIX-01: GC-3 fixture + DEC-E giorni di bordo + T9 - suite verde su worktree pulito`
Push.

## 5. Contenuto ESITO

Verdetto; hash dei 3 commit (DEC-E, fixture, fix finale) + push; prova GC-3 integrale (worktree); diff docstring; report DEC-E (giorni esclusi, conteggi); tabella asserzioni vecchio→nuovo; output pytest ×2; `git status --short` finale.
