# TASK ATTIVO: SPEC-FUNZ-01-AUDITFIX-01 — chiusura gap dell'audit indipendente (lato BLOCCHI)

> **Track**: Business-spec (SPEC-FUNZ). **Sede**: CLI (GOV-SURFACES-01). **Tag commit**: `[SPEC-FUNZ-01-AUDITFIX-01]`. Tutto su `main` (trunk).
>
> **Origine**: audit multi-agente **indipendente** (workflow `wf_589a4b92`, 34 agenti, **365/366 citazioni fedeli**) che ha riaperto i CAP-fonte a HEAD e verificato da zero v2 + serie B1..B8, ignorando le review esistenti. Esito: **8 blocchi SOUND**, v2 problemi minori, **12 difetti confermati** (0 high, 3 medium, 9 low). Questo task chiude i **6 difetti confermati che vivono NEI BLOCCHI** (B3/B5/B6/B8).
>
> **FUORI SCOPE — difetti SOLO-v2 (6)**: la submacchina di posizione Cap.11 (omessa in v2 ma **già presente in B3**), e le 4 miscitation di v2 (CN-2.1, R-3.7, NFR-8.3, R-10.2). **NON si patchano qui**: la v2 è il documento che i blocchi superano; il veicolo corretto è l'**assemblaggio** (rimpiazza v2 con i blocchi corretti). Patchare un doc destinato all'archiviazione è spreco. Decisione Orchestratore; AC può chiedere il patch standalone di v2 a parte.

---

## 0. Natura
Remediation **mirata** di difetti di audit, **non** ricostruzione. NON sei cieco: lavori CON i finding dell'audit (sotto, autoritativi) + i CAP-fonte. Tocchi **solo** i 4 file-blocco indicati. **Non** tocchi i CAP (freeze G-09, sola lettura), **non** tocchi `SPEC_FUNZ_01.md` (v2, fuori scope), **non** tocchi altri blocchi.

## 1. Letture obbligatorie PRIMA di scrivere (conferma in testa al REPORT)
1. `tasks/METODO.md` (RM-1..RM-4 + Freeze G-09 + §Superfici). **Prima azione.**
2. `.claude/BASE_COMUNE.md`.
3. `.claude/agents/spec_developer.md`.
4. Questo `tasks/ACTIVE_TASK.md`.

## 2. Input autoritativo dell'audit — NON re-litigare i finding, MA rileggi i CAP token-per-token (AC-G7)
I `CAP:riga` sotto sono puntatori dell'audit: **rileggi la riga reale a HEAD** prima di citarla; cita la riga reale. Path CAP: arabo per parti 8/9/10 (`CAP_09_parte_9.md`, `CAP_10_parte_10.md`), romano per I/II/VII (`CAP_02_parte_II.md`). Risolvi con Glob in `docs/methodology_v2/` se serve.

## 3. I 6 FIX (tutto e solo questo)

| # | Blocco | Tipo | Difetto (dall'audit) | Fonte CAP | Azione |
|---|---|---|---|---|---|
| **F1** | **B6** | **gap MEDIUM** | Manca la **regola di consumo per-categoria-di-feature**: volatilità calcolata **solo su barre reali**, feature di touch/livello **mai su barre sintetiche**. Product-relevant (correttezza feature in produzione). Assente in B6 (e v2). | `CAP_09_parte_9.md:185-189` (rileggi) | Deriva **nuovo/i requisito/i atomico/i** (N1) in coda allo schema B6 (prossimo `B6-R-NN` / `B6-CN-NN` disponibile), con citazione `[DOC-INTERNO CAP_09_parte_9.md:riga]` reale + valore operativo. |
| **F2** | **B3** | **gap LOW** | Omessa la subordinazione: **il profitto netto (al netto commissioni) è la metrica PRIMARIA di successo**; $\pi_{t_2\mid t_1}$/MFE/MAE/$f_{stop}$ sono strumenti di verifica/calibrazione, **non** la definizione di successo. È un **criterio dichiarato, NON un esito d'edge**. | `CAP_02_parte_II.md:411` (Cap.11.5) | Aggiungi un requisito atomico (o estendi `B3-R-47` sotto N1) che cattura la subordinazione, citando `:411`. **NON** asserire esiti d'edge. |
| **F3** | **B5** | **miscitation LOW** | `B5-CN-05`: "1680 min" ancorato a `:292/:302` (regola-cardine, corrette) ma il **numero 1680** sta su `:290`. Proposizione-cardine fedele. | `CAP_09_parte_9.md:290` (rileggi: unica occorrenza di 1680) | Correggi **solo l'ancora**: aggiungi/sposta la citazione del dettaglio numerico a `:290`. Proposizione invariata. |
| **F4** | **B6** | **gap LOW** | Header CSV runtime: manca il **vincolo di encoding (BOM/UTF-8)**. | Localizza la fonte nel CAP (CAP_09/CAP_10 schema-dato / continuità tape; cfr. M-8 cp1252→UTF-8 in STATO §5) | Aggiungi un requisito/CN atomico col vincolo encoding, citato alla riga CAP reale. **Se la fonte CAP non esiste, NON inventare**: segnala nel REPORT "fonte non trovata" e lascia F4 in sospeso. |
| **F5** | **B6** | **gap LOW** | Omessi i **marker `BACKFILL_VERIFIED_T3` / `UNVERIFIED`** e il **routing al gate Cap.60**. | `CAP_10_parte_10.md` Cap.60 (rileggi la regione) | Aggiungi requisito atomico per i marker + routing al gate, citato alla riga reale. |
| **F6** | **B8** | **gap LOW** | Omessa dalla §2 una **dipendenza FASE-D dichiarata**: "estensione immutabilità CANDLERANGE oltre T+3". | `CAP_10_parte_10.md:234` (rileggi) | Aggiungi la dipendenza all'enumerazione delle dipendenze aperte (nuovo `B8-R-NN` o estensione coerente dell'enumerazione §2), citata `:234`, marcata **dipendenza aperta / PENDING-empirico** (mai risolta). |

## 4. Vincoli (cardine)
- **Solo i 6 fix.** Nessun'altra proposizione, ID o citazione cambia. Nessun altro file oltre i 4 blocchi toccati.
- **Gap-closure (F1/F2/F4/F5/F6)**: nuovi ID atomici (N1) in coda allo schema del blocco; citazione `[DOC-INTERNO ...]` risolvibile alla riga reale + valore operativo dichiarato; **aggiorna conteggio + matrice di tracciabilità** del blocco toccato.
- **Miscitation (F3)**: correggi **solo** l'ancora di riga.
- **Floor citazioni 100%**; grafia canonica (vietata `[CODICE-EXISTENTE]`); **0 conclusioni wiki-only**.
- **Edge PENDING (cardine ereditato B7/B8)**: nessuna asserzione d'esito d'edge; F2 e F6 in particolare restano "criterio dichiarato" / "dipendenza aperta", mai esito.
- **AC-G4**: nessun "verificato X" di prima istanza nei file spec.
- **Guard**: `docs/spec_funzionale/` **non è esente** dal guard RM-1. Se un commit viene bloccato per `verificat*`, è un problema reale da **risolvere** (riformulare), **NON da override**.
- **CAP frozen (G-09)**: sola lettura. Pre-flight: nessun CAP nel diff del tuo commit.

## 5. Output e stop
- File-blocco modificati: **solo** `docs/spec_funzionale/SPEC_FUNZ_01_B3.md`, `_B5.md`, `_B6.md`, `_B8.md` (solo i toccati).
- `reports/REPORT_SPEC_FUNZ_01_AUDITFIX_01.md`: per ogni fix F1..F6 → finding, fonte CAP:riga **riletta**, ID nuovo / ancora corretta, evidenza `file:riga`; + **auto-check edge-PENDING preservato** + **auto-check nessun "verificato X" di prima istanza** + conferma "nessun CAP toccato, v2 non toccata".
- Commit `[SPEC-FUNZ-01-AUDITFIX-01]` (body: elenco F1..F6 + conteggi aggiornati per blocco), **push** su `origin/main`. Scrivi `READY_FOR_REVIEW` in `tasks/DEV_STATUS.md`, committa+pusha, poi **FERMATI**. Non invocare il Reviewer.

## 6. Separazione ruoli
- **Developer** (questo task, non-cieco): applica i 6 fix derivandoli dai CAP-fonte; non ridefinisce lo scope, non tocca v2/CAP/altri blocchi, non asserisce esiti d'edge.
- **Reviewer** (CLI, dopo): verifica che i 6 fix siano chiusi correttamente (citazioni nuove risolvono alla riga reale; gap-closure fedele al CAP; miscitation corretta), **0 regressioni** sui requisiti non toccati, edge-PENDING intatto, floor citazioni 100%. Verdetto PASS/CONDITIONAL/FAIL.

---
*Card AUDITFIX-01 scritta dall'Orchestratore (deposito finding autoritativi dell'audit `wf_589a4b92`, pattern punto-di-controllo). B8 resta CHIUSO PASS nello storico; i blocchi toccati verranno annotati come emendati-da-AUDITFIX alla chiusura. Difetti solo-v2 rinviati all'assemblaggio.*
