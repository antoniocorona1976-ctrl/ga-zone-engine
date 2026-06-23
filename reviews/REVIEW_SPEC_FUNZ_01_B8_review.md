# REVIEW — SPEC-FUNZ-01-B8 (Confine / chiusura della spec — blocco 8/8, ULTIMO)

> **Track**: Business-spec (SPEC-FUNZ). **Ruolo**: spec_reviewer. **Modalità**: CAP-review piena adattata al non-CAP (due giri ostili, BASE_COMUNE §6). **Oggetto**: deliverable commit `7bd927b` — `docs/spec_funzionale/SPEC_FUNZ_01_B8.md` (17 ID: 12 B8-R + 5 B8-CN, 0 NFR) + `reports/REPORT_SPEC_FUNZ_01_B8.md`.
>
> **Sede**: **CLI** (Claude Code CLI sul PC del supervisore, filesystem `C:\Users\AN\Documents\Projects\ga-zone-engine`). Audit documentale **no-DAPI** col **divieto CLI** (niente probe di zelo): i `[PROVA-EMPIRICA]` interni ai capitoli — es. FDAX 2026-05-27 — sono stati verificati **solo** come citazione fedele del capitolo frozen, **non** ri-eseguiti.
>
> **HEAD al momento della review**: `7bd927bd35fa24da38ec4bd46f18092712ae32e2`.

---

## VERDETTO: **PASS**

0 problemi bloccanti. 0 BUG REALE in tabella. 0 finding non-bloccanti che richiedano rework. 1 osservazione minore (NEUTRO, informativa, già coperta dalla card). Floor citazioni 100% verificato su **tutti e 17 gli ID** (non campione). Confronto-copertura Sez.10: 0 buchi, 0 sconfinamenti, 0 orfani. Chiusura **75/75** della serie B1..B8 verificata sulla mappa `c7ce4be`. Cardine confine (AC-B8-CONFINE/NOASSEMBLY/FRAMING/DEPS) integro. Lista "Empirico-CLI da verificare" **VUOTA** (come atteso).

---

## Conferma letture obbligatorie (eseguite PRIMA dell'audit)

1. `tasks/METODO.md` — RM-1..RM-4 + RACC-METODO-2 (r.212-214) + §Superfici GOV-SURFACES-01 (r.240-244) + Freeze G-09 (r.264-268). Prima azione assoluta.
2. `.claude/BASE_COMUNE.md` — §3 reviewer bi-sede (CLI per la spec), §4 classificazione finding + mapping verdetto↔BUG REALE, §6 doppio giro, §8 onestà claim→evidenza.
3. `.claude/agents/spec_reviewer.md` — ruolo (floor citazioni 100%, confronto-copertura, divieto CLI probe di zelo).
4. `tasks/ACTIVE_TASK.md` — card B8 (AC-G1..G11 + B8-CONFINE/NOASSEMBLY/FRAMING/DEPS, done-when §8, cardini).

Contesto autoritativo USATO per il confronto-copertura (riferimento Orchestratore/Reviewer, non riverificato come setup): `Business Spec/Final/ESITO_B8-01.md` (mappatura v2 Sez.10 = R-10.1/R-10.2/CN-10.1); `docs/spec_funzionale/PROPOSTA_SUDDIVISIONE_SPEC_v2.md` (mappa di chunking, autorità F-3 `c7ce4be`, riga B8 → Sez.10). L'incidente `3136a55` (override RM-1 sui file di setup, già risolto, autorizzato AC) è **fuori dal perimetro** di questa review.

---

## 1. Freeze G-09 — verifica indipendente (pre-condizione di tracciabilità)

`git diff <frozen> HEAD -- <file>` eseguito io stesso, **tutti e quattro vuoti**:

| CAP-fonte | SHA frozen | `diff` a HEAD `7bd927b` |
|---|---|---|
| `CAP_08_parte_8.md` (Cap.42 + premessa Cap.41) | `015c47a` | **VUOTO** ✓ |
| `CAP_09_parte_9.md` (Cap.55 + premessa Cap.53) | `28cfd2d` | **VUOTO** ✓ |
| `CAP_10_parte_10.md` (Cap.64) | `41447d3` | **VUOTO** ✓ |
| `CAP_07_parte_VII.md` (Cap.36.3, premessa) | `b27c1e3` | **VUOTO** ✓ |

Inoltre: i CAP-fonte sono **identici** tra `3136a55` (HEAD di derivazione dichiarato nel documento) e `7bd927b` (HEAD attuale) → `git diff 3136a55 HEAD -- <4 CAP>` **vuoto**. La rilettura token-per-token del Developer "a HEAD `3136a55`" resta valida a HEAD attuale. Nessuno slittamento pin (AC-G7 regge).

---

## 2. Floor citazioni 100% (AC-G8) — verificato su TUTTI i 17 ID (non campione)

Ho aperto con Read le regioni-fonte dei CAP frozen e risolto **ogni** citazione `capitolo:riga` di **ogni** requisito alla riga reale a HEAD. Esito: **17/17 ID con ≥1 citazione risolvibile, 100% delle citazioni risolve al costrutto affermato.**

| ID | Citazioni | Riga reale verificata | Risolve? |
|---|---|---|---|
| B8-R-01 | CAP_08:167, :143, :145 | :167 vincolo fasizzazione PHASE-1 single-instrument senza covarianza; :143 "esplicita e dichiarata, non semplificazione silenziosa"; :145 "rimozione layer multi-indice (DCC/ADCC/BEKK...)" | ✓ |
| B8-R-02 | CAP_08:143, :145 | :143 "dichiarazione normativa PHASE-2 senza implementazione ... rinviata"; :145 "layer covarianza cross-index non esiste nel doc v2 corrente" | ✓ |
| B8-CN-01 | CAP_08:147 (:149-:151) | :147-:151 strumenti previsti DAX(FDAX/Eurex)/EuroStoxx50(FESX/Eurex)/S&P mini(ES/CME) | ✓ |
| B8-CN-02 | CAP_08:176, :182 | :176-:180 estensioni dichiarate non implementate (DCC/ADCC/cDCC, Realized GARCH, S_xidx+5ª famiglia); :182 "nessuno entra nell'impegno corrente" | ✓ |
| B8-CN-03 | CAP_08:174, :169, :170, :171, :172 | :174 "non sostituisce la specifica ideale, la istanzia parziale con costi noti"; :169 σ_sys→σ_local; :170 feature tensor senza canali cross-index (catalogo 37); :171 S_xidx non calcolabile + 5ª famiglia esclusa; :172 no riga "Contagio cross-index" | ✓ |
| B8-CN-04 | CAP_09:338 | :338 "cash europei DGER/DSTX50/DITAS/DFRA non sono cross-index PHASE-2: canali di contesto live, logging+gating qualitativo" | ✓ |
| B8-CN-05 | CAP_10:236 | :236 "Convenzione cross-index PHASE-2 ... Parte 10 NON si applica ai cross-index PHASE-2 (fuori scope PHASE-1)" | ✓ |
| B8-R-03 | CAP_09:402; CAP_10:237 | :402 "M-2 OPEN ... resta OPEN come carryover ad Appendice E"; :237 "Telegram latenza L_max=30s (M-2 OPEN): Appendice E, fuori perimetro DAPI" | ✓ |
| B8-R-04 | CAP_10:131, :232 | :131 "θ_reconcile parametro provvisorio non congelato ... calibrazione rinviata a FASE-D / CAP-DATA-04 / monitoring"; :232 "calibrazione fine θ_reconcile ... carryover CAP-DATA-04 o monitoring post-go-live" | ✓ |
| B8-R-05 | CAP_07:637, :641 | :637 lista esatta 10 param "rimangono starting point ... nessun congelamento empirico in Parte VII"; :641 "monitoring post-go-live 3-6 mesi ... non è task di Parte VII" | ✓ |
| B8-R-06 | CAP_10:131 | :131 "12 parametri di tuning provvisori di Parte VII Cap.31 (θ_DSR, θ_PBO, ...)" trattati come provvisori non congelati | ✓ (vedi nota sotto) |
| B8-R-07 | CAP_09:389 | :389 "lookup completa codici mese ... congelati solo F=giugno, I=settembre; altri runtime-discovery via ANAG nel ciclo operativo (FASE-D)" | ✓ |
| B8-R-08 | CAP_09:387 | :387 "account B6086 non abilitato a FDAX standard, ERR;<sym>;1007 ... fuori scope D-1 ... se in PHASE-2 si decidesse..." | ✓ |
| B8-R-09 | CAP_09:391 | :391 "vendor cross-index pluriennale per training PHASE-2 ... decisione rinviata a futuri cicli di estensione (PHASE-2 attivazione)" | ✓ |
| B8-R-10 | CAP_09:404; CAP_10:238 | :404 "persistenza DAPI per training fuori scope ... vincolo Parte 8 invariato ... nuovo task Planner"; :238 idem versante tape | ✓ |
| B8-R-11 | CAP_10:230, :235 | :230 "migrazione formato legacy→esteso 391 dump, una-tantum FASE-D, 11→13 campi"; :235 "coabitazione legacy/esteso ... scelta architetturale FASE-D non vincolata" | ✓ |
| B8-R-12 | CAP_09:406; CAP_10:231 | :406 "implementazione codice pipeline ... FASE-D ... metodologia non codice"; :231 "pipeline backfill/riconciliazione/archiviazione FASE-D" | ✓ |

**Premesse (AC-B8-FRAMING) verificate per riga, non ri-derivate:** CAP_07:637/:641 (Cap.36.3, owned B7) → B8-R-05 cita come dipendenza aperta, gate non ri-derivato; CAP_09:338 (Cap.53, owned B5) → B8-CN-04 cita solo il confine, gating runtime non ri-derivato; CAP_08:133 (Cap.41, owned B5) → Sez.3/Sez.4.2 cita solo come dipendenza aperta M-GOV-1, regola di sessione non ri-consolidata. **Riga 133 reale** = "Riferimento alla sessione runtime corrente. L'epoca corrente E5 corrisponde alla sessione 08:00-22:00 CET..." → risolve.

**Nota su B8-R-06 (esaminato a fondo, non un finding):** l'unica citazione di fondazione è `CAP_10:131`, che testualmente parla di θ_reconcile e cita per analogia "i 12 parametri di tuning provvisori di Parte VII Cap.31 (θ_DSR, θ_PBO, ...)". La citazione **risolve al costrutto affermato dal requisito** ("i parametri di tuning provvisori es. θ_DSR, θ_PBO sono trattati come provvisori non congelati"). La seconda parte dell'asserzione (edge = materia validator, dipendenza aperta) NON è asserita come esito ma dichiarata "eredità del cardine B7" e marcata PENDING-empirico (§3) — coerente con card §6/§7 e con la dottrina "edge MAI asserito, esclusiva validator/FASE-D". Nessuna asserzione d'edge di prima istanza. **Conforme.**

---

## 3. Tabella per AC (G1..G11 + B8-CONFINE/NOASSEMBLY/FRAMING/DEPS)

| AC | Esito | Evidenza (file:riga) |
|---|---|---|
| **AC-G1** (N1 atomicità) | **OK** | ogni heading `### B8-*` esprime una proposizione; concern di confine separati in ID distinti (fasizzazione B8-R-01 / dichiarazione PHASE-2 B8-R-02 / strumenti B8-CN-01 / estensioni B8-CN-02 / costi B8-CN-03); dipendenze aperte una per ID (B8-R-03..R-12). B8-CN-03 enumera 4 costi sotto un'unica proposizione-confine ("costi noti della PHASE-1"): ammesso dalla card §3 AC-G1 (enumerazione dentro un unico requisito-confine). Non un buco N1. |
| **AC-G2** (tracciabilità a riga) | **OK** | ogni ID cita riga reale `[DOC-INTERNO CAP_0X_parte_*.md:NNN]`; matrice §4.1 (`SPEC_FUNZ_01_B8.md:195-211`) |
| **AC-G3** (valore operativo/di sistema) | **OK** | ogni ID ha bullet "Valore operativo/di sistema"; colonna valore in matrice §4.1 |
| **AC-G4** (no "verificato X" di 1ª istanza — RM-1) | **OK** | 0 blocchi `VERIFICA/PROVE/...`; grep "verificat" → tutte negazioni o citazioni del capitolo (r.99, 124, 133, 202), 0 asserzioni di prima istanza; dichiarato §0.5 |
| **AC-G5** (etichette RM-3) | **OK** | tutte `[DOC-INTERNO ...]`; PROVA-EMPIRICA FDAX riportata "come già dichiarata dal capitolo frozen" (B8-R-08 r.133 + §4.3) |
| **AC-G6** (grafia canonica) | **OK** | grep grafia deprecata (con "X") → **0 occorrenze** nel documento; etichette tutte canoniche |
| **AC-G7** (rilettura pin token-per-token) | **OK** | CAP-fonte invariati 3136a55→HEAD (diff vuoto); righe verificate indipendentemente a HEAD `7bd927b` corrispondono |
| **AC-G8** (floor citazioni 100%) | **OK** | 17/17 ID con citazione risolvibile (§2 sopra, verifica integrale non a campione) |
| **AC-G9** (cecità preservata) | **OK** | 0 ID-v2, 0 conteggio-target, 0 partizione nel documento; nessuna menzione di SPEC_FUNZ_01.md/chunking/B1..B7 come fonte; §0.3 |
| **AC-G10** (scope "tutto e solo") | **OK** | copre Cap.42+Cap.55+Cap.64; materia B1..B7 non ri-derivata (premesse §4.2 + out-of-scope) |
| **AC-G11** (matrice + nota di rinvio) | **OK** | §4.1 matrice 17 ID; §4.2 nota di rinvio premesse + out-of-scope; §4.3 nota RM-3 |
| **AC-B8-CONFINE** (cardine) | **OK** | ogni ID è dichiarazione di confine/fasizzazione/dipendenza-aperta; caccia verbi vietati ("supporta/erogati/implementati", "è calibrato/congelato/misurato/verificato") → 0 asserzioni di apertura/risoluzione (unica "supporta/erogati" è negazione r.60) |
| **AC-B8-NOASSEMBLY** (anti meta-processo) | **OK** | nessun heading `### B8-*` enuncia assemblaggio/indicizzazione/avvio-FASE-D; tali materie solo in §0.4 (NON-requisiti) e out-of-scope §4.2 |
| **AC-B8-FRAMING** (verifica fondazione) | **OK** | Cap.42/55/64 req-bearing; Cap.36.3/53/41 premesse citate per riga, non fonti primarie di alcun B8-* (§2 report classificazione + §4.2) |
| **AC-B8-DEPS** (stato esatto, non risolte) | **OK** | ogni dipendenza aperta con stato esatto ("aperta/provvisoria, non congelata, rinviata a FASE-D/monitoring/Appendice E/PHASE-2/nuovo task Planner") + destinazione; 0 dichiarate risolte; edge PENDING-empirico (B8-R-06) |

---

## 4. Confronto-copertura vs perimetro B8 (mappa `c7ce4be`, riga B8 → Sez.10)

Sez.10 = **R-10.1, R-10.2, CN-10.1** (3 req-v2; ESITO_B8-01 §3, mappa §139). Mappa `c7ce4be` = identica a HEAD (`git diff c7ce4be HEAD -- PROPOSTA_SUDDIVISIONE_SPEC_v2.md` vuoto).

| Req-v2 Sez.10 | Materia | Casa nei B8-* | Buco? | Sconfinamento? |
|---|---|---|---|---|
| **R-10.1** | fasizzazione PHASE-1/PHASE-2 (Cap.42) | B8-R-01, B8-R-02 | No | No |
| **CN-10.1** | cross-index PHASE-2 strumenti/estensioni/costi + cash europei + Parte 10 | B8-CN-01, B8-CN-02, B8-CN-03, B8-CN-04, B8-CN-05 | No | No |
| **R-10.2** | dipendenze aperte verso FASE-D (Cap.55/64 + premessa Cap.36.3) | B8-R-03 .. B8-R-12 | No | No |

- **0 buchi**: ogni req-v2 di Sez.10 ha casa nei B8-*.
- **0 sconfinamenti**: nessun B8-* ri-deriva materia di B1..B7. I punti di contatto (Cap.36.3 owned B7 in B8-R-05; Cap.53 owned B5 in B8-CN-04; Cap.41 owned B5 in Sez.3) sono **premesse citate per riga**, non requisiti duplicati. Doppia-tracciatura Cap.36.3 risolta (concern di confine ≠ concern di gate; ESITO_B8-01 §5).
- **0 orfani**: tutti i 17 ID tracciano a Cap.42/55/64/36.3 della Sez.10.
- Granularità 17 ID vs 3 req-v2: **ammessa** (atomica N1, non un buco).

---

## 5. Chiusura 75/75 della serie (verifica di partizione — specifico di B8 ultimo)

Partizione consolidata sulla mappa `c7ce4be` §139 (NON a memoria):

`B1=9 + B2=12 + B3=6 + B4=14 + B5=11 + B6=9 + B7=11 + B8=3 = **75**` ✓

Con B8 (Sez.10 = R-10.1/R-10.2/CN-10.1, 3 req-v2) la serie B1..B8 copre i 75 req-v2 della partizione 1-a-1 (0 gap, 0 orfani, mappa §116/§124/§139). **Chiusura 75/75 verificata. B8 è l'ultimo blocco: la serie chiude la copertura della spec.**

---

## 6. RM-1 / RM-3 / cecità (verifica trasversale)

- **RM-1 (AC-G4)**: 0 "verificato X" di prima istanza; ogni asserzione è richiamo etichettato a CAP frozen.
- **RM-3 (AC-G5/G6)**: 35 etichette `[DOC-INTERNO ...]` (livello 3); 0 conclusioni wiki-only; PROVA-EMPIRICA FDAX riportata come citazione del capitolo; grafia deprecata 0 occorrenze; paper esterni non usati come fonte di verità.
- **RACC-METODO-2**: N/A — B8 non cita alcuno schema di sistema esterno (perimetro interamente documentale di confine/fasizzazione; nessun decoder/parser in scope, card §0.1). Non c'è schema da diffare col decoder canonico.
- **Cecità preservata**: 0 ID-v2, 0 conteggio-target, 0 partizione importati; nessuna traccia di import da v2/chunking/B1..B7 nel documento.

---

## 7. Problemi bloccanti / non-bloccanti / osservazioni minori

**Bloccanti**: nessuno.

**Non-bloccanti (BUG REALE / da rework)**: nessuno.

**Osservazioni minori (NEUTRO, informative, nessuna azione richiesta):**

- **O-1 (NEUTRO).** B8-CN-03 enumera 4 costi distinti della PHASE-1 sotto un unico ID. È **una sola proposizione-confine** ("la PHASE-1 ha costi noti dichiarati come tali"), con i 4 costi come sua specificazione dalla stessa regione-fonte coesa (`:169-:172` sotto il cappello `:174`). La card §3 AC-G1 ammette esplicitamente l'enumerazione dentro un unico requisito-confine. Spezzarlo in 4 ID sarebbe granularità alternativa, non correzione di un difetto N1. **Nessuna azione.**

---

## 8. Tabella "Classificazione per il supervisore"

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|------------------------|
| 1 | B8-CN-03 enumera 4 costi sotto un ID (granularità, non difetto N1: ammesso da card §3 AC-G1) | `SPEC_FUNZ_01_B8.md:70-74` | NEUTRO | No |

**0 BUG REALE. 0 MIGLIORA PERFORMANCE. 0 RISCHIO PEGGIORAMENTO. 1 NEUTRO** (informativo, non va a Developer senza approvazione AC e comunque privo di impatto).

---

## 9. Applicazione RM-1 a me stesso (Reviewer)

Ogni mia affermazione di verifica ha sostegno operativo puntuale:

1. **"Freeze G-09 regge a HEAD"** — VERIFICA: `git diff <frozen> HEAD -- <file>` per i 4 CAP. PROVE: output vuoto per CAP_08 vs `015c47a`, CAP_09 vs `28cfd2d`, CAP_10 vs `41447d3`, CAP_07 vs `b27c1e3` (eseguito io, HEAD `7bd927b`). ALTERNATIVE ESCLUSE: file slittato (escluso: diff vuoto). NON ESCLUSE: nessuna.
2. **"Tutte le 17 citazioni risolvono alla riga reale"** — VERIFICA: Read delle regioni-fonte e confronto costrutto-per-costrutto. PROVE: CAP_08:138-187 (Cap.42 + Cap.41:107-137); CAP_09:380-414 (Cap.55) + :330-342 (Cap.53); CAP_10:224-241 (Cap.64) + :126-137 (θ_reconcile); CAP_07:630-645 (Cap.36.3). Tabella §2 con riga reale per ogni ID. ALTERNATIVE ESCLUSE: citazione che non risolve (escluso: 17/17 risolvono). NON ESCLUSE: nessuna.
3. **"Cardine confine integro (0 aperture/risoluzioni)"** — VERIFICA: caccia ostile ai verbi vietati via Grep. PROVE: "supporta/erogati/implementati" → unica occorrenza è negazione (r.60); "è calibrato/congelato/misurato" → 0; "verificat" → solo negazioni/citazioni (r.99/124/133/202); heading `### B8-*` → nessuno enuncia assemblaggio/indicizzazione/avvio-FASE-D. ALTERNATIVE ESCLUSE: asserzione di apertura/risoluzione sepolta nella prosa (escluso: lette tutte le 17 voci + grep). NON ESCLUSE: nessuna.
4. **"Confronto-copertura: 0 buchi/sconfinamenti/orfani + chiusura 75/75"** — VERIFICA: mappa `c7ce4be` (diff a HEAD vuoto) §139 + ESITO_B8-01 §3/§5/§6. PROVE: 9+12+6+14+11+9+11+3=75; R-10.1→B8-R-01/02, CN-10.1→B8-CN-01..05, R-10.2→B8-R-03..12. ALTERNATIVE ESCLUSE: req-v2 Sez.10 senza casa / B8-* che ri-deriva B1..B7 (escluso: tabella §4). NON ESCLUSE: nessuna.
5. **"M-2 e M-GOV-1 richiamati come aperti, non chiusi"** — VERIFICA: Read `tasks/CARRYOVER.md`. PROVE: M-2 OPEN (`CARRYOVER.md:21`), M-GOV-1 APERTO (`:37`); B8-R-03 + Sez.3 nota M-GOV-1 li richiamano come dipendenze aperte, report §"Censimento M aperti" coerente. ALTERNATIVE ESCLUSE: M chiuso da B8 (escluso: stato lasciato OPEN/APERTO). NON ESCLUSE: nessuna.

---

## 10. Lista "Empirico-CLI da verificare"

**VUOTA** (come atteso per un audit documentale no-DAPI in sede CLI). La spec consolida fatti già chiusi nei CAP frozen e non introduce fatti empirici nuovi; i `[PROVA-EMPIRICA]` interni ai capitoli (FDAX 2026-05-27) sono verificati solo come citazione fedele del capitolo, non ri-eseguiti (divieto CLI: niente probe di zelo). Nessun handoff alla sede empirica.

---

*Review SPEC-FUNZ-01-B8 — iterazione 1. Verdetto: **PASS**. Audit documentale CLI no-DAPI, due giri ostili. 0 bloccanti, 0 BUG REALE, 1 NEUTRO informativo. Floor citazioni 100% (17/17, integrale). Confronto-copertura Sez.10 pulito. Chiusura 75/75 verificata: la serie B1..B8 chiude la copertura della spec. Empirico-CLI vuoto. CAP frozen non toccati, spec non riscritta.*
