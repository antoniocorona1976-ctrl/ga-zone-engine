# TASK ATTIVO: SPEC-FUNZ-01-B5 — Runtime DAPI, sessione & compliance (ricostruzione cieca, modalità B, blocco 5/8)

> **Track**: Business-spec (SPEC-FUNZ). **Sede**: CLI (GOV-SURFACES-01). **Tag commit**: `[SPEC-FUNZ-01-B5]`. Tutto su `main`.
>
> **Perimetro consolidato (mappa `c7ce4be`)**: B5 è **blocco unico**, ~11 requisiti, due nature (canale DAPI + sessione/compliance). Fonte: **CAP_09 P9 Cap.45, 46, 47, 50, 52, 53, 54 + CAP_01 Cap.1**. La mappa di chunking è la **fonte autoritativa del perimetro**: riconciliarla **PRIMA** di scrivere/derivare (lezione B4-EXT).
>
> **Letture obbligatorie del Developer, in quest'ordine, PRIMA di scrivere**: `tasks/METODO.md` (RM-1..RM-4 + RACC-METODO-2), `.claude/BASE_COMUNE.md`, `.claude/agents/spec_developer.md`, questo `tasks/ACTIVE_TASK.md`. Conferma in testa al REPORT di averli letti.

---

## 0. Natura e cecità

**Natura**: ricostruzione cieca da zero del perimetro runtime/sessione/compliance (Sez.7 della v2). B1/B2/B3/B4 sono chiusi PASS; B6/B7/B8 non esistono ancora.

### 0.1 — Vincolo di cecità (modalità B)

Il Developer deriva i requisiti **DAI SOLI** capitoli del perimetro §1 (`CAP_09 Cap.45,46,47,50,52,53,54` + `CAP_01 Cap.1`), **cieco** rispetto a: `SPEC_FUNZ_01.md` (v2 congelata) e `*_v1_storico*`; i file di chunking (`PROPOSTA_SUDDIVISIONE_SPEC*.md`) **come fonte di contenuto-requisiti**; i documenti di B1/B2/B3/B4 (`SPEC_FUNZ_01_B*.md`). Gli ID sono auto-assegnati da zero (schema `B5-R-NN` / `B5-CN-NN` / `B5-NFR-NN`). Il confronto-copertura con la v2 è compito **esclusivo del Reviewer** (§6). **Eccezione**: i capitoli citati come **premessa** nelle note di confine (§1) si possono leggere **solo** per ancorare la citazione-premessa, non per ri-derivarne i requisiti.

---

## 1. Perimetro-fonte (cosa derivi) — SOLO questi capitoli

Fonte: `docs/methodology_v2/CAP_09_parte_9.md` (Cap.45,46,47,50,52,53,54) + `docs/methodology_v2/CAP_01_parte_I.md` (Cap.1, tocco). I pin-riga si **risolvono in CLI** prima della derivazione (l'Orchestratore li deposita, oppure il Developer li individua leggendo il capitolo): **nessun numero di riga è asserito a monte da chi ha scritto questa card.**

Materia da consolidare, per capitolo:
- **Cap.46 — Architettura canale DAPI**: gateway Darwin servizio locale, **loopback 127.0.0.1 esclusivo**, triplo-porte canonico (10001 datafeed realtime IN scope; **10002 ordini mai aperta**; 10003), banner di handshake con **prefix-match** (non match esatto), banner registrato in audit (Cap.54).
- **Cap.47 — Catalogo simboli & rollover**: sottoscrizione FIB front-month, convenzione ticker IDEM, **boot giorno scadenza / CONTRACT_SWITCH**, codici mese Directa-IDEM proprietari; **dualità miniFIB (1€/pt, esecuzione) / FIB-pieno (5€/pt, calibrazione)**.
- **Cap.50 — Errori, recovery, riavvio Darwin**: *capitolo di contesto runtime* (vedi nota di confine — verifica se fonda un requisito proprio).
- **Cap.52 — Sessione operativa 08:00-22:00 CET**: finestra operativa (epoca E5); fuori sessione la pipeline è in stand-by; **la chiusura 22:00 non chiude un segnale active**.
- **Cap.53 — Gating cash europei**: indici cash (DGER/DSTX50/…) entrano **solo** come logging operativo + **gating qualitativo post-emissione**, regole **fuori dal GA**, mai feature/cromosoma/state-machine; il gating **non sopprime** mai l'emissione.
- **Cap.54 — Audit log & retention**: log strutturato, immutabile, append-only; registra comandi/risposte DAPI, transizioni di stato, segnali emessi, decisioni di gating; eventi di lifecycle **per-stato**.
- **Cap.45 — Premessa/collocazione** e **CAP_01 Cap.1 — Obiettivo**: *capitoli di inquadramento* (vedi nota — verosimilmente nessun requisito proprio, contesto).

### Note di confine (premessa vs derivazione) — CARDINE di B5

B5 tocca molti altri blocchi. Regola generale: **consolida il fatto runtime/sessione/compliance; cita come premessa il fatto che vive altrove, NON ri-derivarlo.**

- **Cap.27-28 (pipeline inference, anti-doppio) → NON derivare.** Sono **elaborazione runtime** di requisiti **già specificati altrove**: emission-only (R-1.2, B1), |A|≤1 segnale unico (R-3.10, B2), latenza (NFR-6.2, B4), determinismo replay (CN-9.4, B6). Verificato (MAP-SPLIT-03): **0 requisiti-v2 propri**. Citabili come premessa; **nessun requisito B5 li consolida**. Se ti viene da scrivere un requisito su EGARCH-recalibration o sulla pipeline di emissione, **fermati**: è premessa o materia di altri blocchi.
- **Cap.45, Cap.50 → contesto, non assumere requisiti.** Cap.45 (premessa) e Cap.50 (errori/recovery) **non fondano requisiti di Sez.7** (verificato MAP-CONSOLIDATE-04). Derivane un requisito **solo** se trovi nel testo una proposizione che è genuinamente un requisito di prodotto; altrimenti trattali come contesto. **Non gonfiare** B5 con requisiti di recovery che non sono nel perimetro-requisiti.
- **Dualità miniFIB / FIB-pieno (Cap.47)**: consolida la **parte miniFIB (1€, esecuzione operatore)** da Cap.47; la parte **FIB-pieno (5€, calibrazione)** è già B1 — **cita B1 (moltiplicatore 5€) come premessa**, non ri-asserirla.
- **Gating (Cap.53)**: l'annotazione di gating si attacca al **messaggio Telegram** (contratto del messaggio = B4): **cita B4 come premessa/superficie**, non ri-derivare il contratto del messaggio.
- **Audit lifecycle (Cap.54)**: gli eventi di lifecycle loggati (SIGNAL_EMITTED, …, i 6 terminali) sono coerenti con la **state machine di Cap.7 (B3)**: **cita B3 come premessa**, non ri-derivare la macchina a stati. L'audit è inoltre **corredo del bundle frozen** (Parte VII Cap.35 = B7) e **input della dashboard Cap.30** (fuori-scope): citali come premessa/destinazione, non consolidarli.
- **Sessione (Cap.52)**: l'epoca E5 / calendario sessione vive in `fib_session_calendar.csv` di **Parte 8 Cap.41 (B8)**: **cita Cap.41 come premessa** per l'origine normativa della finestra, consolida la **regola operativa** (la pipeline opera 08:00-22:00; stand-by fuori; 22:00 non chiude active).
- **Schema-dato DAPI (CANDLE/PRICE/BOOK_5, formato canonico, decoder)**: il canale riceve questi messaggi, ma lo **schema/decoder è B6** (Cap.48/49/51): **cita B6 come premessa** per il dato ricevuto, **non** consolidare il decoder/format.

---

## 2. Acceptance Criteria

Si applicano **gli stessi `AC-G1..AC-G11` dei blocchi precedenti** (atomicità N1; tracciabilità obbligatoria a riga di `CAP_09`/`CAP_01`; valore operativo — o **valore di sistema/replay** per invarianti puri; divieto "verificato X" RM-1; etichette RM-3 su fonti esterne, qui in particolare il **wiki Directa**; grafia canonica; floor citazioni 100% verificato in review; **cecità preservata**; scope **"tutto e solo"** il perimetro §1; matrice di tracciabilità + nota di rinvio; invarianti come tali). In più:

- **AC-B5-1 — Premesse, non ri-derivazioni**: i fatti delle note di confine §1 (Cap.27-28, dualità 5€, gating-su-messaggio, lifecycle-state-machine, epoca E5, schema-dato) sono **citati come premessa**, **non** consolidati. Ri-derivare materia di B1/B2/B3/B4/B6/B7/B8 = finding (scope creep).
- **AC-B5-2 — PENDING-empirico marcato (RM-1)**: i requisiti la cui chiusura dipende da una verifica empirica DAPI **non ancora fatta** vanno marcati **PENDING-empirico** (come la latenza M-2 di B4), **non** asseriti come verificati. Noti a monte: **codici mese Mar/Dic** (non listati, Cap.55); **comportamento rollover/CONTRACT_SWITCH a scadenza reale** (probe V-3); **convenzione calendario/giorni-di-trading della finestra** (probe V-2). Il **valore** della finestra 08:00-22:00 e i fatti già coperti da PROVA-EMPIRICA 2026-05-27 (banner, porte) **non** sono pending: cita lo stato empirico esatto, non sovra-marcare.
- **AC-B5-3 — RM-3 sul wiki Directa**: porte/banner/convenzioni del wiki Directa sono `[WIKI-HINT, da verificare]` salvo dove c'è già PROVA-EMPIRICA (allora `[PROVA-EMPIRICA <data>]`); mai conclusione strutturale da solo wiki.

---

## 3. Sezioni da produrre

`docs/spec_funzionale/SPEC_FUNZ_01_B5.md`:
1. Intestazione/scopo/schema-ID + conferma cecità.
2. **Canale DAPI** (Cap.46): loopback, triplo-porte, no-order-routing, banner/handshake.
3. **Catalogo & rollover** (Cap.47): sottoscrizione front-month, CONTRACT_SWITCH, codici mese, dualità miniFIB.
4. **Sessione** (Cap.52): finestra 08:00-22:00, stand-by, 22:00-non-chiude-active.
5. **Gating cash** (Cap.53): logging + gating qualitativo post-emissione, fuori-GA.
6. **Audit & compliance** (Cap.54): log strutturato immutabile, eventi per-stato.
7. **Matrice di tracciabilità** + **nota di rinvio** (cosa è premessa/fuori-scope e dove vive: Cap.27-28→B1/B2/B4/B6; schema→B6; bundle→B7; dashboard Cap.30→fuori-scope; esecuzione/post-fill→B3).

REPORT (`reports/REPORT_SPEC_FUNZ_01_B5.md`): 6 sezioni formato supervisore + tabella AC + **"Applicazione RM-1 a me stesso"** + lista **PENDING-empirico**.

---

## 4. Out-of-scope (con destinazione)

| Materia | Destinazione |
|---|---|
| Pipeline inference, EGARCH-recalibration, anti-doppio operazionale (Cap.27-28) | **premessa**: R-1.2 (B1), R-3.10 (B2), NFR-6.2 (B4), CN-9.4 (B6) |
| Schema-dato DAPI / decoder / format canonico (Cap.48/49/51) | **B6** |
| Corredo bundle frozen / gate di go-live (Cap.35, Sez.8) | **B7** |
| Dashboard di monitoraggio lifecycle (Cap.30) | **fuori perimetro spec** (FASE-D) |
| State machine & stati terminali (Cap.7) | **B3** — premessa |
| Esecuzione/gestione attiva post-fill, commissioni | **B3 / B1** (CN-7.4→B3, CN-7.3→B1) — già coperti |
| Contratto messaggio Telegram (Cap.9.2) | **B4** — premessa per il gating |
| Calendario/epoca E5 (Cap.41) | **B8** — premessa per la sessione |

---

## 5. Done-when

Un lettore di `SPEC_FUNZ_01_B5.md` risponde senza ambiguità a:
1. Su quali porte/loopback opera il canale DAPI, e perché 10002 non si apre mai?
2. Come si sottoscrive il contratto e cosa succede al rollover (CONTRACT_SWITCH)? Su quale strumento esegue l'operatore (mini, 1€) vs su quale calibra il motore (pieno, 5€)?
3. Qual è la finestra operativa e perché la chiusura delle 22:00 non chiude un segnale active?
4. Come entrano i cash europei (logging + gating post-emissione) e perché il gating non sopprime l'emissione né tocca il GA?
5. Cosa registra l'audit log e con quale granularità per-stato?
6. Quali fatti sono premessa da altri blocchi (Cap.27-28, schema, lifecycle, epoca, messaggio) e cosa è rinviato?
7. Ogni requisito traccia a una riga di `CAP_09`/`CAP_01` (salvo premesse citate dai blocchi vicini) e porta un valore dichiarato? I PENDING-empirico sono marcati?

---

## 6. Modalità di review (materia del Reviewer — il Developer NON la usa per derivare)

- Audit formale CLI sugli AC (§2) + sui requisiti.
- **Confronto-copertura (modalità B)**: il Reviewer confronta i requisiti B5 con il **perimetro v2 di Sez.7** (i requisiti che la **mappa consolidata `c7ce4be` assegna a B5**: Sez.7 **escl. CN-7.3/CN-7.4**, **+ CN-2.1, + CN-4.2**), usando la **mappa come autorità di partizione (F-3)**. Verifica: copertura piena del perimetro B5; **nessuno sconfinamento** in B1/B2/B3/B4/B6/B7/B8 (le premesse devono essere citate, non consolidate); **PENDING-empirico** correttamente marcati e non asseriti.
- Cecità del Developer come oggetto di audit (tracce v2/B*/chunking importate = BUG REALE).
- Verdetto PASS / CONDITIONAL / FAIL. ≥1 BUG REALE ⇒ non-PASS.

---

## 7. Pipeline attesa (Orchestratore)

1. **Riconcilia il perimetro con la mappa `c7ce4be`** e risolvi i pin CAP_09/CAP_01 (leggi i capitoli; deposita i numeri di riga). **PRIMA** di lanciare il Developer.
2. **spec_developer** (CLI, cieco §0.1): scrive `SPEC_FUNZ_01_B5.md` + REPORT; `READY_FOR_REVIEW`; si ferma. *Recupero socket*: se l'agente si interrompe, completamento trasparente (provenienza nel REPORT), come per B4.
3. **Check post-Developer** + boundary-check sulle giunte §1 (Cap.27-28 non ri-derivati; schema→B6; lifecycle→B3; gating→B4; dualità 5€→B1; epoca→B8).
4. **spec_reviewer** (CLI): audit AC + copertura vs perimetro B5 (mappa F-3).
5. **PASS** → punto di controllo supervisore per la chiusura `SPEC-FUNZ-01-B5: CHIUSO PASS <sha>`. **CONDITIONAL/FAIL** → punto di controllo supervisore.

---

*Card scritta in fase di supervisione sul perimetro della mappa consolidata `c7ce4be`, NON committata dal Planner (lo fa l'Orchestratore). Nessuna spec scritta qui, nessun CAP modificato (freeze G-09). Nessun ID-requisito v2 né contenuto copiato da v2/B*/chunking: cecità del Developer preservata. I pin CAP_09/CAP_01 sono da risolvere in CLI, non fatti asseriti.*
