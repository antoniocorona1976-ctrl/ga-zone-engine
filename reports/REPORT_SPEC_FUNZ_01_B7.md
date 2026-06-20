# REPORT — SPEC-FUNZ-01-B7 — Gate di go-live

> **Letture obbligatorie confermate (in ordine)**: (1) `tasks/METODO.md` (RM-1..RM-4 + RACC-METODO-2 + §Superfici + Freeze G-09) — letto; (2) `.claude/BASE_COMUNE.md` — letto; (3) `.claude/agents/spec_developer.md` (ruolo) — letto; (4) `tasks/ACTIVE_TASK.md` (card B7) — letto per intero. Inoltre letto `tasks/CARRYOVER.md` per censire M aperti pertinenti a B7.
>
> **Sede**: CLI. **Output**: `docs/spec_funzionale/SPEC_FUNZ_01_B7.md` + questo report. **Tag commit**: `[SPEC-FUNZ-01-B7]`.

---

## Pre-flight freeze G-09 (card §intestazione, F4) — esito

Eseguiti i due diff richiesti **prima** di fidarmi dei pin §1:

- `git diff b27c1e3 HEAD -- docs/methodology_v2/CAP_07_parte_VII.md` → **output VUOTO** (nessuna riga di diff). CAP_07 non slittato.
- `git diff e8d5424 HEAD -- docs/methodology_v2/CAP_01_parte_I.md` → **output VUOTO** (nessuna riga di diff). CAP_01 non slittato (SHA frozen corretto `e8d5424`, NON `b76c32c`, come da NB F4).

Conseguenza: i pin-riga §1 sono affidabili a HEAD. Ho comunque riletto token-per-token ogni riga citata (AC-G7) prima di scriverla; le citazioni nel documento puntano alla riga reale verificata a HEAD.

---

## 1. Cosa è stato prodotto

Un documento di specifica funzionale (`SPEC_FUNZ_01_B7.md`) che consolida il perimetro "Gate di go-live" (Cap.31-36 di Parte VII + Cap.5 di Parte I) in **49 requisiti di prodotto atomici** (N1), assegnati da zero con cecità rispetto a v2/chunking/B1-B6:

- **38 `B7-R-*`** (requisiti funzionali: criteri, procedure, definizioni, regole);
- **7 `B7-CN-*`** (vincoli/confini: immutabilità, integrità, confine di ruolo, separazione successo-segnale vs operatore, carryover);
- **4 `B7-NFR-*`** (non funzionali: replay bit-exact, latenza qualitativa, compute budget).

Struttura in 9 sezioni come da card §4: intestazione + cecità + nota di confine di ruolo edge-PENDING in evidenza (§1); definizione di successo Cap.5 (§2); procedura OOS Cap.31 (§3); DSR Cap.32 (§4); PBO/CSCV Cap.33 (§5); bootstrap Cap.34 come procedura di supporto (§6); frozen bundle Cap.35 (§7); gate decisionali Cap.36 con i 12 criteri come requisiti distinti (§8); matrice + rinvio + PENDING + RM-3 (§9).

Il documento applica il **cardine edge-PENDING** ovunque: ogni gate è "criterio dichiarato", ogni grandezza misurabile è marcata PENDING-empirico (validator/FASE-D), nota di confine di ruolo `validator` in evidenza in §1.4.

## 2. Ipotesi di partenza

- I pin §1, gli SHA frozen, il perimetro e gli AC depositati nella card dall'Orchestratore sono **autoritativi** (non riverificati come fonte), ma i pin sono stati **riletti token-per-token** prima di citarli (AC-G7), come imposto.
- Modalità B (cecità): nessuna lettura di `SPEC_FUNZ_01.md`, `*_v1_storico*`, `PROPOSTA_SUDDIVISIONE_SPEC*`, `SPEC_FUNZ_01_B1..B6`. (Glob della cartella eseguito solo per confermare l'esistenza della directory; nessuno di quei file aperto.)
- Nessuna eccezione RM-2 "leggi i decoder": perimetro B7 interamente interno (gate sul log di replay bit-exact), nessun decoder/parser esterno in scope.
- Cap.34 (bootstrap) e Cap.30 trattati secondo le note F3/framing della card: Cap.34 = procedura di supporto al gate AC-GO-3, nessun requisito standalone "su Cap.34"; Cap.30 = oggetto-citato, NON fonte di alcun `B7-*` (la fonte di B7-R-35 è Cap.36).

## 3. Decisioni rilevanti

1. **Atomicità dei 12 criteri di go-live (AC-B7-ATOMICITA-GO)**: i 12 criteri = 12 requisiti distinti (B7-R-25..B7-R-36). Per i compositi AC-GO-10 (pipeline) e AC-GO-11 (dashboard) le sotto-condizioni (4 e 3) sono enumerate **dentro** il singolo criterio come contenuto di verifica, NON spacchettate in requisiti separati (B7-R-34, B7-R-35). AC-GO-12 (hash all'avvio) consolidato come condizione singola già atomica (B7-R-36), non spacchettato.
2. **Disallineamento ordinamento `AC-GO-*` vs `B7-R-*`**: il capitolo enumera AC-GO-2 = PBO e AC-GO-3 = expected net return. Per non rompere l'assegnazione uno-a-uno e mantenere la riga reale, **B7-R-26 traccia ad AC-GO-3 (`:574`)** e **B7-R-27 ad AC-GO-2 (`:572`)**. Ho inserito una NB esplicita nel documento (§8, dopo B7-R-26) e la corrispondenza puntuale è nella matrice §9.1, per evitare che la review legga lo scostamento di numerazione come errore di citazione.
3. **Bootstrap come supporto (anti-gonfiamento)**: nessun requisito standalone "su Cap.34"; i tre requisiti B7-R-21/22/23 + B7-NFR-02 fissano procedura/replicazione/calibrazione/replay come corredo del gate B7-R-26, con nota framing esplicita in §6.
4. **Confine di ruolo edge-PENDING in tre punti**: nota in evidenza in §1.4, ribadita in B7-CN-06 (procedura GO/NO-GO, esito = validator) e nella lista PENDING §9.3. Decisione: marcare esplicitamente come PENDING ogni grandezza d'esito anche dentro i requisiti dei criteri (non solo nella sezione finale), per blindare il cardine.
5. **Stato delle soglie (AC-B7-SOGLIE)**: ogni soglia ($\theta_{DSR}, \theta_{PBO}, \theta_{f_5}, \theta_{IQR}, \theta_{t_2}, \theta_{CVaR}, \theta_{MDD}, \theta_{sessions}, L_{avg}, \epsilon_{f_1}$) consolidata con lo stato esatto "valore di lavoro provvisorio, non congelato in Parte VII, riconsiderato post-go-live"; mai "definitivo/validato".
6. **Confine successo-motore vs operatore (AC-B7-SUCCESSO)**: B7-CN-01 isola esplicitamente il successo del segnale dal risultato economico dell'operatore (esecuzione manuale/stop/rollover/feed fuori dal criterio), con doppia citazione `:69` e `:85`.

## 4. Misura prima/dopo (adattata al greenfield di consolidamento)

- **PRIMA**: i criteri di gate di go-live erano dispersi nei capitoli metodologici Cap.31-36 + Cap.5, in forma matematico-procedurale, non leggibili da un esterno come elenco di requisiti di prodotto tracciabili e verificabili singolarmente; il rischio di confondere "criterio dichiarato" con "esito misurato" (asserzione d'edge) non era arginato da una struttura a requisiti atomici.
- **DOPO**: 49 requisiti R/CN/NFR tracciati uno-a-uno a riga del capitolo, ciascuno con valore operativo dichiarato e stato esatto delle soglie; cardine edge-PENDING applicato come invariante (ogni grandezza d'esito marcata PENDING-empirico, confine `validator` esplicito). Nessuna metrica GA/edge inventata; nessun verdetto.

## 5. Domande aperte / Blocchi (F6 — batch unico)

**Nessun blocco.** Il task è stato interamente mappato dai capitoli del perimetro senza fonti mancanti, senza ambiguità che richiedessero decisione di Planner/AC, senza requisiti non risolvibili dai documenti. Nessun requisito porta il marcatore `[B-N PROVVISORIO]` (nessun blocco aperto a monte).

Osservazione non bloccante (non un blocco): il disallineamento di ordinamento AC-GO-2/3 vs B7-R-26/27 (Decisione 3.2) è gestito con NB esplicita + matrice; lo segnalo qui per trasparenza, non richiede sblocco.

Censimento M (CARRYOVER): l'unico M pertinente a B7 è **M-2 OPEN** (latenza Telegram $L_{max}=30$s, Appendice E), già premessa qualitativa della card; incardinato come **B7-NFR-03** con la sua misura empirica marcata PENDING-empirico (NON dichiarata verificata, RM-1). **Nessun M nuovo emesso da B7**; nessun M esistente chiuso/incardinato oltre il richiamo di M-2 come premessa.

## 6. Criterio di rollback

Il documento è additivo (nuovo file in `docs/spec_funzionale/`, nessuna modifica a CAP o indice). Rollback = `git revert` del commit `[SPEC-FUNZ-01-B7]` (rimuove `SPEC_FUNZ_01_B7.md` + questo report + `DEV_STATUS.md`); nessun effetto su capitoli metodologia (freeze G-09 rispettato, zero file CAP toccati), nessun effetto sugli altri blocchi.

---

## Tabella verifica AC

| AC-ID | Esito | Evidenza (file:riga) |
|-------|-------|----------------------|
| AC-G1 (N1 atomicità) | OK | 49 requisiti, una proposizione ciascuno; 12 criteri go-live = 12 ID distinti (`SPEC_FUNZ_01_B7.md` B7-R-25..36); DSR/PBO ID distinti (B7-R-09/10, B7-R-16/18) |
| AC-G2 (tracciabilità a riga) | OK | ogni requisito cita `[DOC-INTERNO ...:NNN]` riletto token-per-token; matrice §9.1 completa |
| AC-G3 (valore operativo/sistema) | OK | ogni requisito ha riga "**Valore**"; colonna "Valore" in matrice §9.1 |
| AC-G4 (no "verificato X" prima istanza) | OK | nessun blocco VERIFICA/PROVE; tutte le asserzioni sono richiami a CAP chiusi; §9.4 |
| AC-G5 (etichette RM-3) | OK | `[DOC-INTERNO ...]` su ogni claim; paper esterni `[WIKI-HINT, da verificare]` (B7-R-16/18/21, §9.4) |
| AC-G6 (grafia canonica) | OK | usate `[DOC-INTERNO]`/`[WIKI-HINT]`; nessuna occorrenza di `[CODICE-EXISTENTE]` (nessun codice citato in B7) |
| AC-G7 (rilettura pin token-per-token) | OK | tutti i Cap.31-36 + Cap.5 riletti via Read prima della citazione; diff freeze vuoti |
| AC-G8 (floor citazioni 100%) | OK | ogni `B7-*` ha ≥1 citazione risolvibile alla riga (matrice §9.1) |
| AC-G9 (cecità preservata) | OK | nessun ID-v2, nessun conteggio-target, nessuna partizione; ID da zero; §1.3 |
| AC-G10 (scope tutto-e-solo) | OK | coperti Cap.5 + Cap.31-36; nessuna materia di altri blocchi ri-derivata; out-of-scope §9.2 |
| AC-G11 (matrice + nota rinvio) | OK | §9.1 matrice, §9.2 nota rinvio/invarianti, §9.3 PENDING, §9.4 RM-3 |
| AC-B7-EDGE (edge PENDING, cardine) | OK | nota §1.4; ogni grandezza d'esito marcata PENDING; lista §9.3; auto-check sotto |
| AC-B7-VALIDATOR (confine di ruolo) | OK | §1.4 + B7-CN-06: B7 non emette GO/CONDITIONAL/NO-GO né valori d'edge, esclusiva `validator` |
| AC-B7-SOGLIE (stato soglie) | OK | tutte le soglie "valore di lavoro provvisorio, non congelato, riconsiderato post-go-live" (B7-R-17/20/23/30/31/33, §9.3 NON-pending) |
| AC-B7-SUCCESSO (motore vs operatore) | OK | B7-CN-01 (`CAP_01_parte_I.md:69, :85`) |
| AC-B7-ATOMICITA-GO (compositi) | OK | B7-R-34 (pipeline, 4 sotto-cond. dentro), B7-R-35 (dashboard, 3 sotto-cond. dentro), B7-R-36 (hash, singola) |

---

## Applicazione RM-1 a me stesso

Asserzioni fattuali che ho dichiarato e loro sostegno operativo:

- **"I due diff freeze sono vuoti"** — eseguiti realmente via Bash (`git diff b27c1e3 HEAD ...` e `git diff e8d5424 HEAD ...`); output catturato vuoto fra i marcatori. Alternativa esclusa: diff non vuoto → avrei dovuto rileggere e citare righe diverse; non si è verificata.
- **"I pin §1 reggono a HEAD"** — non assunto dalla card: ho aperto Cap.5 e Cap.31-36 con Read e confrontato il contenuto delle righe citate (es. `:71-75` formula $-2c$; `:568` "12 AC binari"; `:589-592` 4 sotto-cond. pipeline; `:595-597` 3 sotto-cond. dashboard; `:599` hash; `:602-605` raccomandazioni per classe). Le righe citate corrispondono al testo letto.
- **"Nessun M nuovo / solo M-2 pertinente"** — letto `tasks/CARRYOVER.md` per intero; M-2 è l'unico OPEN con destinazione Appendice E pertinente a B7 (latenza Telegram, in scope come AC-GO-10). Gli altri M sono CLOSED-CAP-* o relativi a schema-dato (B5/B6), fuori perimetro B7.
- **"49 requisiti, 38/7/4"** — conteggio rifatto sugli ID effettivamente scritti nel documento e contro-verificato con grep degli header `### B7-*`: **38 `B7-R-*` (B7-R-01..38), 7 `B7-CN-*` (B7-CN-01..07), 4 `B7-NFR-*` (B7-NFR-01..04) = 49 totali**. (Il conteggio precedente "38 — 28/7/3" era errato; corretto in iter.2 a valle del finding F1, qui e in §9.1 del documento.) Riportato come descrittivo, non come target.

Alternative non escluse / limiti onesti: la corrispondenza pin↔riga è stata verificata sul contenuto semantico delle righe lette; un eventuale errore di trascrizione di un singolo numero di riga resta possibile e va catturato dalla review (floor citazioni 100%, AC-G8). Non dichiaro "verificato" alcun esito d'edge: tutto ciò che è misurabile è PENDING-empirico.

## Lista PENDING-empirico (richiamo)

Vedi §9.3 del documento. In sintesi: valori effettivi di DSR/PBO/$E[R_{net}]$/IC/CVaR/MDD/$r_{emit}$/$\rho_{sessions}$/$L_{avg}$; esito dei 12 criteri e decisione GO/NO-GO; esito funzionale pipeline/dashboard/hash; latenza $L_{max}$ effettiva (M-2); $F$ effettivo. Tutti → validator / FASE-D, mai asseriti.

## Auto-check esplicito AC-B7-EDGE — conferma

**Confermo: ZERO asserzioni d'esito o d'edge nel documento.** Ho riletto il documento cercando i verbi vietati ("supera/passa il gate", "DSR è positivo/significativo", "l'edge esiste/è confermato", "GO" come affermazione di esito). Ogni occorrenza di tali concetti è formulata come *criterio dichiarato dal metodo* ("il metodo richiede", "il criterio dichiarato è", "al run del validator si misurerà") oppure marcata esplicitamente "(Esito = PENDING-empirico)". L'unica occorrenza testuale di "GO" è nella **procedura** GO/NO-GO (B7-CN-06) come nome della decisione che **il validator** emette, non come verdetto asserito da B7. Nessun valore numerico d'esito è dichiarato come misurato.

---

## Iterazione 2 — risposta ai finding di Review (CONDITIONAL `98780f9`)

Review iter.1 = **CONDITIONAL** (`reviews/REVIEW_SPEC_FUNZ_01_B7_review.md`): 2 BUG REALI (F1, F2) + 2 MIGLIORA PERFORMANCE (F3, F4). Decisione AC: instradati tutti e 4, accorpati in questo micro-pass di **sola accuratezza** (nessuna proposizione, ID-requisito o citazione-fonte cambiata). Patch chirurgiche limitate ai 4 finding.

**Conteggio reale ricontato da zero (F1)** — prima di scrivere il nuovo numero ho contato gli ID distinti dagli header `### B7-*` con grep, contigui e senza buchi:
- `B7-R-*` = **38** (B7-R-01 .. B7-R-38, contigui);
- `B7-CN-*` = **7** (B7-CN-01 .. B7-CN-07);
- `B7-NFR-*` = **4** (B7-NFR-01 .. B7-NFR-04);
- **Totale = 49**. Coincide col numero indipendente del Reviewer (49 = 38 R + 7 CN + 4 NFR). Il numero suggerito nella card NON è stato preso ciecamente: è stato verificato sugli ID reali e confermato.

| Finding | Classe | Correzione applicata | Prima → Dopo | Punti toccati |
|---|---|---|---|---|
| **F1** | BUG REALE | Conteggio requisiti corretto al valore reale verificato + auto-check RM-1 rifatto sul conteggio vero | "38 — 28 R / 7 CN / 3 NFR" → "**49 — 38 R / 7 CN / 4 NFR**" | doc `SPEC_FUNZ_01_B7.md` §9.1 (riga conteggio); REPORT §1 (totale + 3 sotto-conteggi), §"Misura prima/dopo" (DOPO), tabella AC-G1, §"Applicazione RM-1 a me stesso" (asserzione auto-smentita corretta) |
| **F2** | BUG REALE | ID nel paragrafo atomicità AC-GO allineati al corpo reale (shift -1) | "(B7-R-33 pipeline, B7-R-34 dashboard) … B7-R-35 (hash)" → "(**B7-R-34** pipeline, **B7-R-35** dashboard) … **B7-R-36** (hash)" | doc `SPEC_FUNZ_01_B7.md:232` |
| **F3** | MIGLIORA | Cross-reference corretto alla sezione esistente | "§10" → "**§9.3**" | doc `SPEC_FUNZ_01_B7.md` §1.4 (riga nota PENDING) |
| **F4** | MIGLIORA | Stato-soglie uniformato allo stato esatto completo inline | "valore di lavoro provvisorio" → "valore di lavoro provvisorio, **non congelato in Parte VII, riconsiderato post-go-live**" | doc `SPEC_FUNZ_01_B7.md` B7-R-30, B7-R-31, B7-R-33, B7-NFR-03 |

**Impatto**: tutti e 4 i fix sono di sola accuratezza descrittiva. Verificato (e confermato dalla review iter.1) che **nessuna proposizione di requisito, nessun ID-requisito e nessuna citazione-fonte (pin `path:line`) è cambiata**; il cardine edge-PENDING, la cecità, RM-1/RM-3 e il floor citazioni 100% restano inalterati. F2 corregge un refuso descrittivo, non l'applicazione del cardine AC-B7-ATOMICITA-GO (già corretta nel corpo). Freeze G-09 non toccato (nessuna modifica ai CAP; pre-flight: `git diff b27c1e3 HEAD -- CAP_07_parte_VII.md` e `git diff e8d5424 HEAD -- CAP_01_parte_I.md` entrambi vuoti).
