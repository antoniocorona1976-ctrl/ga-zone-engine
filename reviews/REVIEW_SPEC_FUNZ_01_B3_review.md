# REVIEW — SPEC-FUNZ-01-B3 (State-machine & lifecycle del segnale, blocco 3/8)

## Header

- **Perimetro auditato**: `docs/spec_funzionale/SPEC_FUNZ_01_B3.md` (commit `89d28b4`, 61 requisiti: 47 B3-R, 11 B3-CN, 3 B3-NFR) + cross-check `reports/REPORT_SPEC_FUNZ_01_B3.md`.
- **Fonte autoritativa (sola lettura, NON auditata nei suoi AC — frozen G-09)**: `docs/methodology_v2/CAP_02_parte_II.md` (chiuso PASS `a1625df`), Cap.7 (7.1–7.6) e Cap.11 (11.1–11.5) + preambolo (:1-9) e Q-05 (:7).
- **Sede**: **CLI** (GOV-SURFACES-01, METODO §Superfici), su `C:\Users\AN\Documents\Projects\ga-zone-engine`. Audit documentale **no-DAPI**, divieto CLI rispettato (nessuna probe di zelo eseguita).
- **Modalità**: CAP-review piena adattata al non-CAP, **due giri ostili** (BASE_COMUNE §6) applicati agli **AC di B3** (card §3), NON agli AC del CAP frozen.
- **Letture obbligatorie eseguite**: (1) `tasks/METODO.md` (RM-1..RM-4 + RACC-METODO-2); (2) `.claude/BASE_COMUNE.md` (§3 sede, §4 classificazione, §6 doppio giro, §8 onestà); (3) `.claude/agents/spec_reviewer.md`; (4) `tasks/ACTIVE_TASK.md` (card rev-B1, AC-G1..AC-G11 §3). Per il confronto-copertura ho consultato la mappa di chunking autoritativa `docs/spec_funzionale/PROPOSTA_SUDDIVISIONE_SPEC_v2.md` (autorità di partizione F-3) e il perimetro lifecycle della v2 congelata `docs/spec_funzionale/SPEC_FUNZ_01.md` (PASS `ab7450f`).

---

## VERDETTO: **PASS**

0 problemi bloccanti, **0 BUG REALE** in tabella. Floor citazioni 100% verificato token-per-token: tutte le citazioni risolvono. Confronto-copertura: nessun requisito di prodotto del perimetro lifecycle (Cap.7) caduto. Cecità preservata: nessuna traccia di contaminazione dalla v2/B1/B2. Restano 3 osservazioni minori non bloccanti (1 MIGLIORA, 2 NEUTRO), nessuna delle quali impedisce il PASS.

---

## 1. Tabella verifica AC-G1..AC-G11

| AC | Esito | Evidenza (file:riga) |
|----|-------|----------------------|
| **AC-G1** Atomicità N1 | **OK** | `target_1_hit` spezzato: successo (B3-R-05:43), condizione d'ingresso (B3-R-06:46), chiusura contratto (B3-R-07:49), terminalità (B3-CN-02:86), NB-9 (B3-CN-03:89). Ogni terminale ha condizione separata (B3-R-08/09/11/13); ogni transizione un ID (B3-R-17..23:98-116); 3 edge case NB-8 separati (B3-R-29/30/31:159-165), come prescritto dalla card. Borderline su B3-CN-09 (vedi OM-1, non bloccante). |
| **AC-G2** Tracciabilità obbligatoria | **OK** | Ogni requisito porta ≥1 `[DOC-INTERNO CAP_02_parte_II.md:<riga>]`. Eccezione seam (F-1) rispettata: B3-R-23 (:116) traccia a Cap.7.2 `:127` per la transizione, con `:77` (Cap.6.3) come premessa **in più**, non in sostituzione. Verificato: CAP :127 = cella tabella 7.2 `active → revoked | Il motore emette un nuovo signal_id (sostituzione, Cap.6.3)`. |
| **AC-G3** Valore operativo obbligatorio | **OK** | Ogni requisito dichiara un *Valore operativo*; categoria F-2 *Valore di sistema/validazione* usata SOLO sui 4 invarianti di puro determinismo/replay: B3-R-14 (:73-74), B3-R-39 (:199-200), B3-CN-05 (:124-125), B3-CN-11 (:276-277). Gli invarianti con valore-operatore diretto (terminalità target_1_hit B3-R-07, raw touch sempre eseguibile B3-R-27, timer pre-trigger B3-R-38) mantengono correttamente il valore-operatore. Nessun valore-operatore contorto inventato per un invariante di replay (RM-1 rispettato). |
| **AC-G4** Divieto "verificato X" 1ª istanza (RM-1) | **OK** | Nessuna dichiarazione "verificato X" di prima istanza; ogni requisito è un richiamo etichettato a un fatto già chiuso nel CAP. Nessun blocco RM-1 4-righe presente né necessario. |
| **AC-G5** Etichette RM-3 fonti esterne | **OK** | Zero fonti esterne nel documento (grep: 0 occorrenze di `[WIKI-HINT]`/`[CODICE-ESISTENTE]`/`[PROVA-EMPIRICA]`). La finestra 8:00–22:00 CET e il cap 2 giorni compaiono come **calendario/dato dei CAP chiusi** (B3-R-34:182, B3-R-37:193), non come fonte esterna — coerente col carve-out F-5. |
| **AC-G6** Grafia canonica | **OK** | Solo `[DOC-INTERNO …]`. Grep: **0** occorrenze della grafia storica vietata `[CODICE-EXISTENTE]`. |
| **AC-G7** Floor citazioni 100% | **OK** | Tutte le citazioni verificate token-per-token (vedi §2). 0 citazioni che non risolvono. |
| **AC-G8** Cecità preservata | **OK** | Grep mirato (frasi peculiari della v2: "boot del giorno successivo", "persistito", "Valore di prodotto", "esiti terminali"; ID importati R-3./R-4./CN-4.): **0 occorrenze**. ID auto-assegnati da zero (B3-R/CN/NFR, schema dichiarato :11-19). Nessuna frase identica alla v2 non presente nel Cap.7/11. |
| **AC-G9** Scope "tutto e solo" | **OK** | Copre Cap.7.1–7.6 + Cap.11.1–11.5. Nessuna citazione esce dal perimetro (tutte in :7/:77/:95-:175/:349-:399; verificato che da :179 inizia Cap.8=B4). Note di confine esplicite verso B2 (:79, :172), B4 (:142, :355), Parte III (:155, :206), B5/Cap.10 (:356). Nessuno sconfinamento (vedi §4 per i 3 punti di confine fine). |
| **AC-G10** Matrice + nota di rinvio | **OK** | Matrice §8.1 (:285-347, una riga per requisito con ID/proposizione/citazione/valore) + nota di rinvio §8.2 (:349-359) che dichiara le materie adiacenti deliberatamente rinviate (B2/B4/B5/Parte III-IV/Parte V) con motivazione. |
| **AC-G11** Invarianti evidenziati | **OK** | Famiglia B3-CN dedicata agli invarianti: terminalità assoluta (CN-02), NB-9 (CN-03), chiusura transizioni (CN-04), precedenza/determinismo (CN-05), evento-vs-stato (CN-06/08), indipendenza submacchina (CN-09), space search non esteso (CN-10), $\|\mathcal{A}(t)\|\le1$ (CN-11). Sezione 7 (:267-277) li riepiloga. Confine $\|\mathcal{A}(t)\|\le1$ rispettato: richiamato per la conseguenza sul lifecycle (B3-CN-11), non ri-derivato come proprietà del payload (resta B2). |

---

## 2. Esito floor citazioni 100% (token-per-token)

Ho aperto con Read l'intero perimetro-fonte (CAP_02_parte_II.md righe 1-215 e 340-412) e verificato **ogni** citazione del documento e della matrice §8.1. Campione integrale dei punti critici:

- **:95** = "La state machine del segnale è costruita su un solo stato non-terminale e su sei stati terminali" → B3-R-01. **Risolve.**
- **:99** = "Nessun stato terminale ammette transizioni uscenti: il ciclo di vita … definitivamente chiuso" → B3-CN-02. **Risolve.**
- **:101** = `target_1_hit` semantica + "Il contratto del segnale si chiude definitivamente qui" → B3-R-05/06/07. **Risolve.**
- **:105 / :124** = invalidated pre-touch + "$p(t) \le \texttt{stop\_loss}$ con $t<t_{touch}$; simmetricamente per gli short" → B3-R-09/10, B3-CN-01. **Risolve** (la formula di B3-R-10 è verbatim dal CAP, non elaborazione del Developer).
- **:109** = expired + "campo causale … non come stato dedicato … 6 soli stati terminali" → B3-R-13/14. **Risolve.**
- **:111** = revoked superseduto + "La revoca avviene contestualmente" → B3-R-15/16. **Risolve.**
- **:113** = "$\|\mathcal{A}(t)\| \le 1$ si applica ai segnali attivi … un segnale terminato non è attivo" + NB-9 "`target_1_hit → revoked` non esiste" → B3-CN-03/11. **Risolve** (entrambe le proposizioni sono in :113).
- **:121-:127** = celle della tabella transizioni 7.2 (creazione→active con "scrittura del log di emissione"; i 6 rami `active→…`) → B3-R-17..23. **Risolvono tutte**; :127 = `active→revoked` come transizione (seam F-1 chiuso pulito).
- **:131** = "precedenza … expiry > invalidazione > missed_target > raw touch > azione post-trigger … deterministico il replay" → B3-CN-05. **Risolve.**
- **:135/:137/:139** = raw touch / trigger_event / evento-non-stato + fill manuale → B3-R-24..28, B3-CN-06. **Risolvono.**
- **:145/:147/:149** = edge case NB-8 a/b/c → B3-R-29/30/31. **Risolvono.**
- **:155/:157/:159** = timer post-trigger (expiry da $t_{exec}$, calendario di trading, counter 8:00–22:00 con arresto, scadenza→expired/posttrigger) → B3-R-32..35. **Risolvono.**
- **:163/:165/:167** = timer pre-trigger (decorrenza da emissione, counter, scadenza→expired/pretrigger, razionale executable_rate) → B3-R-36..39. **Risolvono.**
- **:171/:173/:175** = contratto osservazione pivot M-1 (barre da 8:00 CET, $N_{pivot}$ non fissato→Parte V, cadenza barra chiusa) → B3-NFR-01/02/03. **Risolvono.**
- **:349/:351/:352** = separazione segnale vs position lifecycle (Q-05 Cl.3, lista a 2 voci) → B3-CN-07. **Risolvono.**
- **:362** = "boundary … coincide con `target_1_hit` … responsabilità dell'operatore umano" → B3-R-40. **Risolve.**
- **:368/:370/:372/:373/:374/:375** = OUT-OF-SCOPE + 4 metriche IN-SCOPE → B3-R-41/42. **Risolvono** (5 righe metriche per le 4 metriche: :372=π, :373=MFE/MAE, :374=f_stop, :375=tempi permanenza).
- **:381/:383/:385-:389/:391/:393** = struttura submacchina (ingresso, tracking_active, 4 eventi, tracking_closed, indipendenza+log separati) → B3-R-43..46, B3-CN-09. **Risolvono.**
- **:397/:399** = space search non esteso + metriche in fitness come qualità informativa → B3-CN-10, B3-R-47. **Risolvono.**

**Esito: 100% delle citazioni risolve. Nessun finding di tracciabilità.** La dichiarazione del REPORT ("tutte le righe ri-verificate token-per-token") è confermata reale, non solo asserita.

---

## 3. Esito confronto-copertura (modalità B — perimetro lifecycle v2)

Partizione secondo la mappa autoritativa `PROPOSTA_SUDDIVISIONE_SPEC_v2.md` (F-3): **B3 = Sezione 4 della v2** (state-machine/lifecycle, famiglia R-4.*/CN-4.*), fonte CAP_02 Cap.7, con `CN-4.2 → CAP_09 Cap.52` (§4 della mappa, riga 105). Confronto del corpo B3 con la Sez.4 della v2 (`SPEC_FUNZ_01.md:162-201`) e con i requisiti v2 che tracciano a Cap.11 (CN-7.4, NFR-8.11).

| Requisito v2 (perimetro lifecycle) | Classificazione | Copertura in B3 |
|---|---|---|
| **R-4.1** (1 non-term + 6 terminali) | **coperto** | B3-R-01 (+ B3-R-02 target_2_hit rimosso) |
| **CN-4.1** (causa expired = campo, non stato) | **coperto** | B3-R-14 |
| **R-4.2** (raw touch evento sempre eseguibile, no filtri post-emissione) | **coperto** | B3-R-24/25/27 |
| **R-4.3** (trigger_event evento-non-stato; no fill manuale) | **coperto** | B3-CN-06, B3-R-28 |
| **R-4.4** (due timer pre/post, avanzano solo nei minuti di sessione) | **coperto** | B3-R-32..38 (anzi più granulare: B3 spezza decorrenza/counter/scadenza per timer) |
| **CN-4.2** (chiusura 22:00 non chiude active; stato persistito e ripreso al boot) | **fuori perimetro B3** | Traccia a `CAP_09 Cap.52` (P9), non a Cap.7. Mappa: lifecycle↔runtime → **B5**. NON è un gap di B3. |
| **CN-7.4** (→ CAP_02 Cap.11) | **fuori perimetro / nota** | La v2 colloca la traccia Cap.11 in Sez.7 (→B5) e Sez.8 (NFR-8.11, →B7). Vedi nota sotto. |
| **NFR-8.11** ($\pi_{t_2\mid t_1}$, → CAP_02 Cap.11) | **fuori perimetro B3** | Sez.8 della v2 → **B7** (gate). In B3 la metrica $\pi_{t_2\mid t_1}$ compare come IN-SCOPE reporting della submacchina (B3-R-42/47), tracciata a Cap.11, **non** come KPI-gate: nessuna sovrapposizione di concern. |

**Nessun requisito di prodotto del perimetro lifecycle (Sez.4 v2 = Cap.7) è caduto** nella ricostruzione cieca: i 6 requisiti Sez.4 mappabili a Cap.7 (R-4.1/4.2/4.3/4.4, CN-4.1) sono tutti coperti, con granularità superiore in B3 (atomicità N1 applicata).

**Asimmetria di perimetro segnalata (non un difetto di B3, è la fonte che diverge):** il perimetro-fonte di B3 fissato dalla card include **Cap.11 (position lifecycle/submacchina)** in modo esplicito e completo (B3-R-40..47, B3-CN-07..10). La v2, invece, **non ha una sezione dedicata al Cap.11**: lo tratta in modo sparso e parziale (solo $\pi_{t_2\mid t_1}$ via NFR-8.11→Sez.8, e un tocco CN-7.4→Sez.7). Quindi B3 è **più ricco** della v2 sul Cap.11. Questo è coerente con la modalità B (ricostruzione cieca dal CAP, che è la fonte autoritativa) e con la card (Cap.11 è dentro il perimetro B3): è materia "in più" rispetto alla v2, **legittima**, non scope creep — traccia tutta a Cap.11 dentro il perimetro dichiarato. Non genera finding.

**Requisiti v2 "in più" rispetto a B3**: nessuno nel perimetro Cap.7. CN-4.2 è fuori perimetro (B5). Nessuna divergenza dubbia da rinviare al supervisore: la mappa di chunking è netta su Sez.4→B3 e su CN-4.2→B5.

---

## 4. Esito 3 punti di confine fine (input Orchestratore)

- **B3-R-10** ($p(t)\le\texttt{stop\_loss}$ pre-touch come invalidated, :105/:124): la formula è **verbatim** dal CAP :105 ("per i segnali long, $p(t) \leq \texttt{stop\_loss}$ con $t < t_{touch}$") e :124 (cella tabella). **Non è elaborazione non ancorata del Developer.** B3-R-10 dichiara esplicitamente "Fra le condizioni … rientra" e rinvia la definizione piena a Parte IV (coerente con B3-R-09 e con il CAP che rinvia a Parte IV). **Resta dentro il CAP, non sconfina in Parte IV.** Nessun finding.
- **B3-R-17** ("scrittura del log di emissione" nella creazione→active, :121): la frase è **verbatim** dalla cella della transizione 7.2 (`Emissione del segnale, generazione del signal_id, scrittura del log di emissione`). Descrive la **transizione**, non il *formato* del log (B5). Nessun finding.
- **B3-CN-09** ("log separati referenziati dal signal_id", :393): il CAP :393 usa la separazione dei log come supporto dell'**indipendenza** della submacchina; B3-CN-09 la usa con la stessa funzione (proprietà di indipendenza), non come formato/persistenza (B5). Nessun finding di scope. (Solo osservazione di atomicità borderline → OM-1, non bloccante.)

---

## 5. Audit cecità (oggetto di audit)

- Ricerca attiva di ID importati dalla v2/B1/B2 (`R-3.`, `R-4.`, `CN-4.`): **0 occorrenze**.
- Ricerca di frasi peculiari della v2 non presenti nel Cap.7/11 ("boot del giorno successivo", "persistito", "Valore di prodotto della sezione", "esiti terminali"): **0 occorrenze**. In particolare B3 **non** importa il contenuto di CN-4.2 della v2 (persistenza/boot, che è materia P9/Cap.52, fuori dal Cap.7) — segno che il Developer ha derivato dal solo Cap.7 e non dalla v2.
- Schema ID auto-assegnato e dichiarato (:11-19), numerazione locale contigua (B3-R-01..47, B3-CN-01..11, B3-NFR-01..03), nessun buco né riuso.

**Cecità preservata. Nessun BUG REALE di processo.**

---

## 6. Problemi bloccanti

Nessuno.

## 7. Problemi non bloccanti / Osservazioni minori

- **OM-1 (MIGLIORA — atomicità borderline, non bloccante)**: **B3-CN-09** (:254) impacchetta due proposizioni: (a) "la submacchina non modifica mai lo stato del segnale" e (b) "i log della submacchina sono separati e referenziati dal `signal_id`". Sotto N1 stretto sarebbero due requisiti (indipendenza-di-stato vs separazione-dei-log). Non è un BUG REALE perché entrambe le proposizioni sono **esplicite** (nessuna sepolta nella prosa, nessuna sfugge alla verifica) e tracciano alla stessa riga :393 che le afferma insieme; (b) è strumentale a (a). Eventuale split a discrezione del supervisore. Stessa natura, ancora più lieve, in B3-R-14 (campo causale + nota "esito vissuto unico"): qui la seconda è chiaramente glossa del *Valore*, non una seconda proposizione tracciata.
- **OM-2 (NEUTRO)**: la matrice §8.1 per B3-R-42 elenca 5 puntatori (:370,:372,:373,:374,:375) per 4 metriche; :370 è la riga-intestazione "IN-SCOPE per reporting". Corretto e completo; nessuna azione.
- **OM-3 (NEUTRO)**: B3-R-46 cita "il primo evento terminante dichiarato in Parte V" — è un rinvio corretto (il CAP :391 rinvia a Parte V per l'evento terminante); non introduce numeri né anticipa Parte V. Coerente col carve-out F-5.

---

## 8. Tabella "Classificazione per il supervisore"

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|------------------------|
| 1 | B3-CN-09 impacchetta indipendenza-di-stato + separazione-log (N1 borderline; entrambe esplicite, stessa riga :393) | `SPEC_FUNZ_01_B3.md:254` | MIGLIORA PERFORMANCE | No (decisione supervisore; non bloccante) |
| 2 | Matrice B3-R-42: 5 puntatori per 4 metriche (:370 è intestazione IN-SCOPE) — completo e corretto | `SPEC_FUNZ_01_B3.md:328` | NEUTRO | No |
| 3 | B3-R-46 rinvia a "Parte V" per l'evento terminante della submacchina (rinvio corretto, nessun numero) | `SPEC_FUNZ_01_B3.md:251` | NEUTRO | No |

**0 BUG REALE** ⇒ verdetto **PASS** ammesso (BASE_COMUNE §4: ≥1 BUG REALE ⇒ non-PASS; qui nessuno). Le osservazioni minori sono ammesse in PASS.

---

## 9. Applicazione RM-1 a me stesso

- **"Floor citazioni 100% verificato"** — PROVE: Read integrale di `CAP_02_parte_II.md:1-215` e `:340-412`; confronto token-per-token di ciascuna citazione del corpo e della matrice §8.1 col testo del CAP (esiti puntuali in §2). ALTERNATIVE ESCLUSE: che una riga puntasse a contenuto diverso da quello asserito (escluso per ispezione diretta di ogni :riga citata). ALTERNATIVE NON ESCLUSE: nessuna riga del perimetro Cap.7/Cap.11 è rimasta non letta; le righe 216-339 (Cap.8-10) sono fuori perimetro e B3 non vi traccia (verificato che la prima citazione oltre :175 è :349, già Cap.11).
- **"Nessuna traccia di contaminazione (cecità preservata)"** — PROVE: grep mirato su ID v2 (`R-3.`,`R-4.`,`CN-4.`) e su 4 frasi-firma della v2 → 0 occorrenze. ALTERNATIVE NON ESCLUSE: una parafrasi semantica non letterale della v2 sfuggirebbe al grep; mitigato dal fatto che ogni requisito traccia a una riga del CAP che ne è la fonte diretta (la derivazione dal CAP è dimostrata dalla risoluzione 100% delle citazioni).
- **"Confronto-copertura: nessun requisito Sez.4 v2 caduto"** — PROVE: lettura di `SPEC_FUNZ_01.md:162-201` (Sez.4 completa) + matrice §11 (:549-554) + mappa di chunking `PROPOSTA_SUDDIVISIONE_SPEC_v2.md:84,105,120`; mappatura 1:1 dei 6 requisiti Sez.4→Cap.7 ai requisiti B3 (tabella §3). ALTERNATIVE ESCLUSE: che CN-4.2 fosse un gap di B3 (escluso: traccia a CAP_09 Cap.52→B5 per mappa). ALTERNATIVE NON ESCLUSE: nessuna nel perimetro Cap.7; la divergenza su Cap.11 è asimmetria di perimetro (B3 più ricco della v2), non un gap, e tutta tracciata dentro Cap.11.
- **"3 punti di confine fine non sconfinano"** — PROVE: confronto verbatim di B3-R-10/:105-:124, B3-R-17/:121, B3-CN-09/:393 col testo CAP. ALTERNATIVE NON ESCLUSE: nessuna.

---

## 10. Empirico-CLI da verificare

**VUOTA** (come atteso). La spec consolida fatti già chiusi nel CAP-02 frozen; nessuna asserzione di B3 richiede prova empirica contro DAPI o filesystem locale. Divieto CLI rispettato: nessuna probe eseguita.

---

*Review prodotta in sede CLI, audit documentale no-DAPI, due giri ostili sugli AC di B3. CAP-02 non riaudito (frozen G-09). Documento B3 e CAP non modificati. DEV_STATUS NON azzerato (lo fa l'Orchestratore alla chiusura).*
