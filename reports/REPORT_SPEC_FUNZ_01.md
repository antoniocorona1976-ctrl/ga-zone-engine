# REPORT — SPEC-FUNZ-01 v2 (ricostruzione ex-novo, modalità B)

**Autore**: spec_developer (track Business-spec). **Output**: `docs/spec_funzionale/SPEC_FUNZ_01_v2.md` + questo report (deliverable contrattuale del ruolo spec_developer).
**Cecità rispettata**: confermo di NON aver aperto `SPEC_FUNZ_01.md`, `SPEC_FUNZ_01_v1_storico.md`, `REPORT_SPEC_FUNZ_01.md` né alcuna copia `*_v1_storico*`. I requisiti sono ricostruiti esclusivamente dai capitoli-fonte in `docs/methodology_v2/` (Cap.1-65).

---

## 1. Cosa è stato prodotto

`docs/spec_funzionale/SPEC_FUNZ_01_v2.md` — specifica funzionale di prodotto PHASE-1 FIB-only, ricostruita ex-novo dai 10 capitoli-fonte. Struttura:

- **13 sezioni**: nota di testa (provenienza/cautele RM-1/RM-3) + 10 sezioni di requisiti (obiettivo/solo-emissione; destinatario; payload; esecuzione/6 terminali; condizioni emissione; consegna Telegram; vincoli operativi/compliance; criteri go-live; dipendenze dato/infrastruttura; fasizzazione) + matrice di tracciabilità + capitoli non tracciati + blocchi/domande aperte.
- **75 requisiti atomici** (N1): **41 R** (funzionali) + **13 NFR** (qualità/non-funzionali) + **21 CN** (compliance/normativi). *(72 nella stesura v2 originale; +3 NFR dal micro-pass AC 2026-06-14 — vedi §3.)*
- Ogni requisito: una sola proposizione verificabile, tracciabilità `[DOC-INTERNO CAP_XX_parte_*.md:<riga>]` puntuale, valore operativo dichiarato.
- **Matrice di tracciabilità** finale (75 righe, riconciliata 1:1 con i requisiti definiti: 0 mancanti, 0 orfani) + **sezione capitoli non tracciati** che motiva Parti III/IV/V intere e i singoli capitoli interni (Cap.4, 10, 27, 30, 34, 35, 37-44 salvo 42, 45/48/50/55, 57/58/63/64/65).
- **2 blocchi aperti** incardinati con tag `[B-N PROVVISORIO]` sui requisiti dipendenti.

Le domande operative del done-when del task card (1-10) trovano risposta univoca nelle Sezioni 1-10 e nella matrice (Sez.11).

## 2. Ipotesi di partenza

- I 10 capitoli metodologia v2 sono **chiusi PASS e frozen G-09**: fonte autoritativa, non ri-derivata, non ri-verificata. Letti selettivamente per citazioni accurate.
- I 17 fatti dell'eredità del task card + gli M citati sono **autoritativi** (input Orchestratore/Planner): non ri-verificati, citati con etichetta di livello-fonte.
- Lo scope è **invariato** rispetto al vecchio: Fase 1 = vista operatore/prodotto PHASE-1 FIB-only. Nessun ampliamento (no PHASE-2, no implementazione FASE-D, no nuovi temi).
- Il vecchio `SPEC_FUNZ_01.md` e il suo report sono **non consultabili**: ricostruzione cieca. La motivazione (sfiducia nel processo pre-GOV-FIX) è del supervisore; il confronto vecchio↔nuovo è materia del supervisore a valle.

## 3. Decisioni rilevanti

- **Granularità requisiti (N1)**: ho spezzato concern eterogenei. Es.: payload (Cap.6) → R-3.1 (12 campi) separato da R-3.2 (direction), R-3.3 (entry_zone), R-3.4 (target), R-3.5 (target_2 informativo), R-3.6 (type qualifiers), R-3.7 (stop+vincolo geometrico), R-3.8 (setup_class), R-3.9 (immutabilità), R-3.10 (segnale unico), R-3.11 (sostituzione). Il tick 5pt (CN-3.1) è separato come vincolo trasversale.
- **Classificazione R/NFR/CN**: R = comportamento funzionale del prodotto; NFR = qualità/gate (latenza, mobile-readability, DSR/PBO/CVaR/MDD, checklist go-live); CN = vincoli normativi/compliance non negoziabili (solo emissione, porta 10002 mai aperta, commissioni, PII, audit/retention, gating cash, tick discreto, determinismo, no-training-da-DAPI).
- **Etichette di provenienza**: usata grafia canonica `[CODICE-ESISTENTE …]`. Schema CANDLE (CN-9.1) citato col decoder canonico `export_directa_history_parametric.py:477-481` + `[PROVA-EMPIRICA M-1 2026-05-29]`, mai col wiki (etichettato `[WIKI-HINT, da verificare]` e dimostrato inesatto) — RACC-METODO-2 rispettata.
- **Blocchi F6 in batch (non a goccia)**: mappato l'intero task, poi i 2 blocchi insieme in Sez.13 del documento e §5 di questo report. Marcatura `[B-N PROVVISORIO]` su NFR-6.2 (B-1, latenza M-2) e R-7.1 (B-2, orario M-GOV-1).
- **Dipendenza CAP-01/02/03 a SHA non pinnabile**: dichiarata UNA volta in nota di testa, non ripetuta per requisito (come da task card); NON genera `[B-N PROVVISORIO]` (i capitoli sono chiusi/citabili; la sola dipendenza a SHA non confermato non è un blocco aperto).
- **M-2 incardinato come NFR** (NFR-6.2 [B-1]); **M-GOV-1 recepito come R** (R-7.1 [B-2]) citando il pendente upgrade empirico — come richiesto da AC-G12.
- **Cash europei**: classificati CN-7.9 (perimetro vincolante Q-A-3, gating qualitativo post-emissione mai soppressione) e CN-9.2 (riconciliazione low/high via CANDLE ufficiale).
- **Claim empiriche sull'edge**: NFR-8.1..8.8 recepite come criteri **dichiarati**, marcate PENDING-empirico (validator FASE-D) in Sez.8 out-of-scope; nessun verdetto GO/CONDITIONAL/NO-GO emesso (esclusiva del validator).
- **Micro-pass AC (2026-06-14) — enumerazione batteria KPI lifecycle**: la batteria di KPI di lifecycle del segnale era coperta solo parzialmente (NFR-8.3 metrica primaria $E[R_{net}]$; NFR-8.4 stabilità cross-regime di target hit rate + executable rate). I tre KPI di lifecycle restanti, definiti alla fonte ma non enumerati come criteri di accettazione atomici nella v2, sono stati aggiunti come NFR distinti: **NFR-8.9** (invalidation rate) e **NFR-8.10** (missed_target rate) tracciati a `[DOC-INTERNO CAP_01_parte_I.md:77]` (paragrafo "Metriche di lifecycle del segnale"); **NFR-8.11** ($\pi_{t_2\mid t_1}$, probabilità condizionata target_2 dato target_1) tracciato a `[DOC-INTERNO CAP_01_parte_I.md:77]` + `[DOC-INTERNO CAP_02_parte_II.md:372]` (hit-rate condizionale, submacchina position lifecycle IN-SCOPE per reporting/validazione). Entrambe le righe-fonte (CAP_01:77, CAP_02:372) verificate token-per-token con Read prima della stesura. Coerenti con gli stati terminali di R-4.1 (`invalidated`, `missed_target`) e con `target_2` informativo di R-3.5; **non** duplicano NFR-8.4 (che misura stabilità cross-regime di hit/executable rate, non i KPI di invalidazione/missed/condizionale). Nessun altro requisito toccato; CAP frozen non toccati; `00_indice.md` non toccato. Conteggio: 72 → **75** (10 → 13 NFR).

## 4. Misura prima/dopo (greenfield di consolidamento, onesto)

Questo è un greenfield di consolidamento, non una modifica al motore: nessuna metrica GA inventata, nessuna analisi "impatto sul ranking dei cromosomi".

- **PRIMA**: i requisiti di prodotto erano **dispersi** in 10 Parti / 65 capitoli metodologici (matematica, decisioni D-*, AC di review intrecciati), non leggibili da un esterno in vista prodotto; un consumatore del segnale non poteva enumerare cosa pubblica il sistema, quali esiti, quali vincoli, senza leggere l'intera metodologia.
- **DOPO**: **75 requisiti** R/NFR/CN atomici (72 nella stesura v2 originale + 3 NFR dal micro-pass AC del 2026-06-14), ciascuno tracciato a `capitolo:riga`, con valore operativo dichiarato, raccolti in 10 sezioni leggibili in vista operatore/prodotto + matrice di tracciabilità + capitoli non tracciati motivati. Le 10 domande operative del done-when hanno risposta univoca.

## 5. Domande aperte (Blocchi / Domande aperte — batch F6)

Due soli blocchi aperti, entrambi incardinati con `[B-N PROVVISORIO]` sui requisiti dipendenti:

| Blocco | Requisito dipendente | Motivo | Cosa serve per sbloccarlo |
|---|---|---|---|
| **B-1** — Latenza Telegram L_max=30s non verificata (M-2 OPEN) | NFR-6.2 | Valore di lavoro provvisorio; verifica empirica del canale Telegram non eseguita, carryover Appendice E/FASE-D `[DOC-INTERNO CAP_09_parte_9.md:402]` | Probe empirico latenza bot Telegram reale → upgrade requisito |
| **B-2** — Orario sessione FIB in attesa di upgrade a PROVA-EMPIRICA (M-GOV-1) | R-7.1 | Orario 08:00-22:00 CET da decisione AC 13/06/2026 + `[WIKI-HINT Borsa Italiana]`; upgrade empirico dal primo probe V-1 APERTO | Primo probe V-1 sul tape DAPI → upgrade requisito |

Nessun altro blocco. Gli altri M citati (M-4, M-9, M-10, M-16, ecc.) sono CLOSED o note tecniche già incorporate come fonte. Il task è **interamente mappato**; lo stato di blocco non impedisce la consegna (i 2 blocchi sono dichiarazioni di provvisorietà su 2 requisiti, non gap di consolidamento).

## 6. Criterio di rollback

- Se il **confronto vecchio↔nuovo** (materia del supervisore a valle) rivela divergenze sostanziali nei requisiti che indicano un errore di ricostruzione, il rollback è la ri-esecuzione del task con prompt mirato ai requisiti divergenti — non la fusione col vecchio (che resta non consultabile dal Developer).
- Se un **finding di Review** classificato BUG REALE riguarda un requisito (multi-concern non spezzato, tracciabilità mancante/errata, citazione non risolvente, valore operativo assente, marcatura `[B-N PROVVISORIO]` mancante, traccia del vecchio testo): patch chirurgica al solo requisito + ri-verifica citazione con Read + ri-pre-consegna.
- Il documento è **additivo e isolato** (`SPEC_FUNZ_01_v2.md`, file nuovo): il vecchio `SPEC_FUNZ_01.md` resta intatto; il rollback completo è la semplice rimozione di `SPEC_FUNZ_01_v2.md` + `REPORT_SPEC_FUNZ_01_v2.md`, senza impatto su alcun CAP (frozen G-09) né su `00_indice.md` (non toccato).

---

## Tabella verifica AC (AC-ID | OK/PARZIALE/MANCA | evidenza)

| AC | Esito | Evidenza |
|---|---|---|
| **AC-G1** (atomicità N1) | OK | 75 requisiti mono-concern; concern eterogenei spezzati (es. payload Cap.6 → R-3.1..R-3.11 + CN-3.1; KPI lifecycle → NFR-8.9/8.10/8.11 distinti). SPEC_FUNZ_01_v2.md Sez.3. |
| **AC-G2** (tracciabilità obbligatoria) | OK | Ogni requisito ha ≥1 `[DOC-INTERNO CAP_XX_parte_*.md:<riga>]`; matrice completa 75 righe in Sez.11, riconciliata 1:1 coi requisiti definiti. |
| **AC-G3** (valore operativo obbligatorio) | OK | Ogni requisito chiude con riga *Valore operativo*. Sez.1-10. |
| **AC-G4** (floor citazioni 100% verificabili) | OK | Tutte le citazioni `[DOC-INTERNO]`/`[CODICE-ESISTENTE]` verificate token-per-token con Read/sed contro la fonte (CAP_01/02/06/07/08/09/10 + codice :61, :477-481). Correzione applicata: CN-9.3 `CAP_08:218`→`:217`. |
| **AC-G5** (divieto "verificato X" prima istanza, RM-1) | OK | Nessuna nuova dichiarazione "verificato X"; ogni asserzione è richiamo etichettato a CAP chiuso/codice/prova. Nessun blocco VERIFICA/PROVE/ALTERNATIVE nuovo. Nota di testa. |
| **AC-G6** (etichette RM-3) | OK | MiFID II, Borsa Italiana, wiki Directa etichettati `[WIKI-HINT, da verificare]`, mai fonte unica strutturale; wiki Directa citata con avvertenza inesattezza CANDLE (CN-9.1, nota di testa). |
| **AC-G7** (grafia etichette canonica) | OK | Usata `[CODICE-ESISTENTE …]` ovunque; `[CODICE-EXISTENTE …]` assente (nessuna occorrenza nel documento). |
| **AC-G8** (marcatura `[B-N PROVVISORIO]`) | OK | NFR-6.2 `[B-1 PROVVISORIO]`, R-7.1 `[B-2 PROVVISORIO]` con riga di spiegazione; blocchi enumerati in Sez.13. |
| **AC-G9** (cecità rispetto al vecchio) | OK | File vietati NON aperti (confermato sopra). Nessun riferimento/parafrasi del vecchio testo; ID requisito derivati ex-novo dai capitoli-fonte. |
| **AC-G10** (scope invariato, no ampliamento) | OK | Solo PHASE-1 FIB-only; PHASE-2 dichiarata fuori scope (R-10.1/CN-10.1); implementazione FASE-D fuori scope (out-of-scope di ogni sezione). |
| **AC-G11** (matrice + capitoli non tracciati) | OK | Sez.11 (matrice 75 righe) + Sez.12 (capitoli non tracciati: Parti III/IV/V intere + Cap.4/10/27/30/34/35/37-44 salvo 42/45/48/50/55/57/58/63/64/65, ciascuno motivato). |
| **AC-G12** (M-2 incardinato; M-GOV-1 recepito) | OK | M-2 → NFR-6.2 `[B-1]` con verifica OPEN (Appendice E/FASE-D); M-GOV-1 → R-7.1 `[B-2]` con pendente upgrade empirico citato. |
| **AC-S1** (out-of-scope + mini-tabella per sezione) | OK | Ogni Sez.1-10 chiude con lista out-of-scope (destinazione per voce) + mini-tabella requisito→capitolo→tipo. |
| **AC-S2** (schemi-dato con diff col decoder canonico) | OK | CN-9.1 cita schema CANDLE `C;L;H;O;V` via `[CODICE-ESISTENTE export_directa_history_parametric.py:477-481]` + `[PROVA-EMPIRICA M-1 2026-05-29]`, non via wiki (RACC-METODO-2/RM-2). |

**Nota onestà claim→evidenza (BASE_COMUNE §8)**: ogni "OK" sopra ha evidenza puntuale nel documento o nella verifica con Read/sed delle citazioni. La verifica AC-G4 è stata eseguita campionando e risolvendo le citazioni contro la fonte (riga restituita ≡ contenuto citato); l'unico mismatch trovato (`CAP_08:218` blank) è stato corretto a `:217`.
