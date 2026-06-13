# REVIEW — SPEC-FUNZ-01 v2 (ricostruzione ex-novo, modalità B)

**Ruolo**: spec_reviewer (track Business-spec). **Sede**: **CLI** (GOV-SURFACES-01, METODO §Superfici) — audit documentale no-DAPI, divieto CLI attivo (niente probe di zelo).
**Perimetro**: `docs/spec_funzionale/SPEC_FUNZ_01_v2.md` + `reports/REPORT_SPEC_FUNZ_01_v2.md`. Capitoli-fonte `docs/methodology_v2/CAP_*.md` (frozen G-09, autoritativi, non riaperti). Vecchio `SPEC_FUNZ_01_v1_storico.md` aperto **solo** per la Parte 2 (diff di copertura), non toccato.
**Modalità**: Parte 1 = audit ostile standard (doppio giro, BASE_COMUNE §6) sugli AC del task card. Parte 2 = DIFF DI COPERTURA vecchio↔nuovo (gate anti-perdita).
**Iterazione**: v1.

---

## VERDETTO: **PASS**

0 problemi bloccanti. 0 BUG REALE in tabella. Floor citazioni 100% verificato (tutte le citazioni `[DOC-INTERNO]`/`[CODICE-ESISTENTE]` aperte con Read e risolte alla fonte: 0 misresolve, 0 not-found). Tracciabilità, valore operativo, atomicità N1, marcatura `[B-N PROVVISORIO]`, etichette RM-1/2/3 conformi. Solo osservazioni minori (non bloccanti, non BUG REALE). La DIFF DI COPERTURA non rileva perdite indebite: tutti i 36 requisiti del vecchio sono presenti nel nuovo o scartati con motivazione; 1 sotto-proposizione è marcata INTUIZIONE-DA-DECIDERE per il supervisore (non è una perdita bloccante: è materia di decisione AC).

---

## 1. Problemi bloccanti

Nessuno.

## 2. Problemi non bloccanti

Nessun BUG REALE. Nessun problema non bloccante che richieda fix obbligatorio. Vedi Osservazioni minori e DIFF DI COPERTURA per i punti rimessi alla decisione del supervisore.

## 3. Osservazioni minori (no fix obbligatorio)

- **OSS-1 (NEUTRO) — CN-9.1, citazione codice `:477-481` per schema a 5 campi `C;L;H;O;V`.** Il decoder canonico `scripts/export_directa_history_parametric.py` mappa `close=uff, low=min, high=max, open=ape` esattamente alle righe **477-481** (commento r.477 + 4 assegnazioni). Il **quinto campo `V` (volume)** è parsato alla riga **482** (`volume_v = int(Decimal(qty))`), appena fuori dal range citato `477-481`. La proposizione `C;L;H;O;V` è comunque corretta e coperta da `[PROVA-EMPIRICA M-1 2026-05-29]` (`tasks/STATO_CORRENTE.md:82` conferma `UFF;MIN;MAX;APE;V = C;L;H;O;V`). Imprecisione di 1 riga nel range, non misresolve. Eventuale rifinitura: citare `:477-482` per includere il volume. **Non bloccante.**
- **OSS-2 (NEUTRO) — etichetta `[PROVA-EMPIRICA M-1 2026-05-29]`.** La data 2026-05-29 corrisponde alla correzione M-1 in `tasks/STATO_CORRENTE.md:82` ("CORRETTO 2026-05-29"). Citazione coerente con la fonte autoritativa di stato. Nessuna azione.
- **OSS-3 (NEUTRO) — R-6.1 "9 voci" + 2 qualificatori.** R-6.1 elenca 7 voci numerate + "più i qualificatori `target_2_type` e `stop_type`" (9 totali). `CAP_02_parte_II.md:241-251` (Cap.9.2) elenca esattamente 9 punti, dove i punti 8 e 9 sono `target_2_type` e `stop_type`. Coerente. La formulazione "7+2" del v2 è meno limpida del "9 punti numerati" della fonte, ma sostanzialmente corretta. Nessuna azione.
- **OSS-4 (NEUTRO) — classificazione 80pt come CN (CN-5.1) vs NFR.** Il filtro 80pt è classificato CN-5.1 (vincolo di emissione assoluto) nel v2. Coerente con `CAP_01_parte_I.md:83` / `CAP_02_parte_II.md:61` ("vincolo di emissione, non parametro libero"). Il vecchio lo classificava NFR-5. La riclassificazione a CN è difendibile e meglio allineata alla fonte ("vincolo assoluto a valle"). Nessuna azione.

## 4. Citazioni problematiche

**Nessuna citazione non risolvente.** Floor 100% rispettato. Dettaglio della verifica:

- **CAP_01 / CAP_02**: tutte le citazioni del v2 aperte con Read e risolte direttamente dal reviewer (righe 9,11,13,15,23,25,27,29,73,83 di CAP_01; righe 9,19,27,33,35,37,39,47,51,53,61,63,69,73,77,81,95,99,109,135,137,139,157,163,183,185,187,217,227,241,253,259,265,269,271,275,291,295,368 di CAP_02). Tutte RESOLVE.
- **CAP_06 / CAP_07 / CAP_08 / CAP_09 / CAP_10**: 60 citazioni verificate riga-per-riga aprendo i file alle righe citate. **Tutte RESOLVE** (0 misresolve, 0 not-found). Le 3 righe a rischio di overflow (`CAP_07:639`, `CAP_09:402`, `CAP_10:232`) esistono e contengono il contenuto rivendicato (file rispettivamente 682/445/267 righe). Note di precisione (entro tolleranza ~3 righe, nessuna correzione dovuta): `CAP_07:639` ha l'header "10 parametri" a :637 ma il claim è nello stesso paragrafo; `CAP_09:35` risolve come riga della tabella porte (tabella :33-37, `10003` a :37).
- **`[CODICE-ESISTENTE]`**: `:61` (`DEFAULT_INTRADAY_MAX_DAYS=100`) RESOLVE esatto; `:477-481` (mapping CANDLE `C;L;H;O`) RESOLVE esatto (vedi OSS-1 per il 5° campo).

**Nota di merito (cecità rispettata, AC-G9)**: il v2 evita la trappola del vecchio sul tape esteso. R-9.5 traccia il formato "13 campi/manifest/append-only" a `CAP_10_parte_10.md:185,207` e **non** cita lo script `:605-617` (che contiene l'header **legacy 11 campi**, non il 13-campi). Il vecchio (`SPEC_FUNZ_01_v1_storico.md` R-20) citava `:605-617` come "13 campi" — citazione fuorviante, perché 605-617 è l'header a 11 campi. Il v2 non eredita questo difetto: nessuna traccia di copia dal vecchio.

## 5. Conformità RM-1 / RM-2 / RM-3 (asse 3 del ruolo)

- **RM-1**: nessuna dichiarazione "verificato X" di prima istanza. Ogni asserzione è richiamo etichettato a CAP chiuso / codice / prova chiusa. Grep su `verificato` nel documento: le sole 2 occorrenze (righe 628, 633) sono nella frase "upgrade del requisito da provvisorio a **verificato**" (descrizione di stato futuro di sblocco), non dichiarazioni di verifica eseguita. Nessun blocco `VERIFICA/PROVE/ALTERNATIVE` nuovo dovuto. **Conforme.**
- **RM-2 / RACC-METODO-2**: lo schema CANDLE (CN-9.1) poggia sul **decoder di produzione** (`:477-481`) + `[PROVA-EMPIRICA M-1]`, **non** sul wiki. Diff col decoder canonico esplicito (wiki `O;H;L;C` dichiarato inesatto vs reale `C;L;H;O`). **Conforme.**
- **RM-3**: grafia canonica `[CODICE-ESISTENTE …]` ovunque; grafia storica `[CODICE-EXISTENTE …]` **assente** (grep: 0 occorrenze fuori dalla nota di testa che la dichiara vietata). Fonti esterne (MiFID II, wiki Directa, Borsa Italiana) etichettate `[WIKI-HINT, da verificare]`, mai fonte unica strutturale; wiki Directa citata con avvertenza di inesattezza. **Conforme.**

## 6. Atomicità N1, marcatura F6, completezza AC

- **Atomicità (AC-G1)**: campionati i requisiti compositi a rischio (R-3.x, R-4.4, NFR-8.x, CN-7.x). R-4.4 impacchetta "due timer + avanzamento solo in sessione" ma è una singola proposizione verificabile sul **dominio dei due timer** con una clausola di calendario condivisa; accettabile come singolo requisito (la fonte CAP_02:69/157/163 li tratta congiuntamente). Nessun requisito multi-concern indebito che sfugga alla verifica singola. **Conforme.**
- **Tracciabilità + valore operativo (AC-G2/G3)**: ogni requisito ha ≥1 `[DOC-INTERNO …]` puntuale + riga *Valore operativo*. Verificato a campione su tutte le sezioni. **Conforme.**
- **Marcatura `[B-N PROVVISORIO]` (AC-G8/F6)**: i 2 blocchi aperti (B-1 latenza M-2; B-2 orario M-GOV-1) sono incardinati e i soli requisiti dipendenti (NFR-6.2, R-7.1) portano il tag inline con riga di spiegazione. Incrocio §13 ↔ corpo coerente. Nessuna dipendenza da blocco aperto non marcata. **Conforme.**
- **Matrice + capitoli non tracciati (AC-G11)**: §11 (72 righe, riconciliata 1:1) + §12 (Parti III/IV/V intere + capitoli interni, ciascuno motivato). **Conforme.**
- **Scope invariato (AC-G10)**: solo PHASE-1 FIB-only; PHASE-2 e FASE-D fuori scope per ogni sezione. **Conforme.**

---

## TABELLA — Classificazione per il supervisore

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|------------------------|
| 1 | CN-9.1: 5° campo `V` dello schema CANDLE è a `:482`, fuori dal range citato `:477-481` (mapping C/L/H/O esatto) | `SPEC_FUNZ_01_v2.md:420` | NEUTRO | No |
| 2 | R-6.1 formula "7 voci + 2 qualificatori" anziché "9 voci numerate" come la fonte Cap.9.2 | `SPEC_FUNZ_01_v2.md:248` | NEUTRO | No |
| 3 | Old CN-3 "non è consulenza in materia di investimenti" non restata come proposizione di prodotto nel v2 (vedi DIFF) | DIFF | INTUIZIONE-DA-DECIDERE | Decisione AC |
| 4 | KPI di lifecycle (invalidation rate, missed_target rate, $\pi_{t_2\mid t_1}$) non enumerati come KPI di accettazione nel v2 (presenti nel vecchio §7.1) | DIFF | INTUIZIONE-DA-DECIDERE | Decisione AC |

Nessun BUG REALE ⇒ verdetto PASS ammesso. I punti 3 e 4 sono **decisioni AC** (non BUG): riguardano *se* il prodotto v2 debba restare il merito di proposizioni del vecchio che **non sono pienamente ancorate a un CAP chiuso** (vedi DIFF). Non sono perdite di tracciabilità: sono scelte di perimetro su materia opinabile.

---

## DIFF DI COPERTURA vecchio↔nuovo (gate anti-perdita)

Vecchio: `docs/spec_funzionale/SPEC_FUNZ_01_v1_storico.md` — **36 requisiti** = R-1..R-24 (24 R) + NFR-1..NFR-5 (5) + CN-1..CN-7 (7). Aperto SOLO ora, dopo l'audit autonomo del nuovo. Per "presente" si intende: la stessa proposizione verificabile esiste nel nuovo, anche con ID/formulazione diversi.

### Tabella requisito-per-requisito

| Vecchio | Contenuto (vecchio) | Stato nel v2 | Requisito v2 corrispondente / motivazione |
|---|---|---|---|
| R-1 | Emissione segnali strutturati FIB | **PRESENTE** | R-1.1 |
| R-2 | Esecuzione delegata all'operatore | **PRESENTE** | R-1.2 |
| R-3 | Confine FIB-only PHASE-1 | **PRESENTE** | R-10.1 |
| R-4 | Esecuzione manuale mobile | **PRESENTE** | R-2.1 |
| R-5 | Canale Telegram obbligatorio | **PRESENTE** | R-2.3 |
| R-6 | Payload immutabile | **PRESENTE** | R-3.9 |
| R-7 | Segnale unico attivo $|\mathcal{A}(t)|\le1$ | **PRESENTE** | R-3.10 |
| R-8 | Filtro 80pt | **PRESENTE** | CN-5.1 (riclassificato CN, sostanza identica) |
| R-9 | Tick discreto 5pt | **PRESENTE** | CN-3.1 |
| R-10 | Notifica `trigger_event` separata | **PRESENTE** | R-4.3 + R-6.4 |
| R-11 | Distinzione segnale / position lifecycle | **PRESENTE** | R-3.5 + CN-7.4 |
| R-12 | Anti-duplicato persistito | **PRESENTE** | R-6.5 |
| R-13 | Nuovo messaggio per nuovo `signal_id` | **PRESENTE** | R-6.6 |
| R-14 | Notifica trigger separata dall'emissione | **PRESENTE** | R-6.4 |
| R-15 | Sessione 8-22 CET | **PRESENTE** | R-7.1 `[B-2]` |
| R-16 | Sizing fisso 1 contratto | **PRESENTE** | R-2.2 |
| R-17 | Singolo segnale attivo | **PRESENTE** | R-3.10 (stessa proposizione di R-7 vecchio) |
| R-18 | Commissioni 5 EUR/op | **PRESENTE** | CN-7.3 |
| R-19 | Rollover / contract switch | **PRESENTE** | R-7.2 |
| R-20 | Tape esteso 13 campi + manifest | **PRESENTE** | R-9.5 (e meglio tracciato: v2 non eredita la citazione fuorviante `:605-617`) |
| R-21 | Immutabilità tape append-only / non training | **PRESENTE** | R-9.5 + CN-9.3 |
| R-22 | Backfill 100gg + fallback Portara | **PRESENTE** | R-9.3 |
| R-23 | Riconciliazione gate bloccante | **PRESENTE** | R-9.4 |
| R-24 | Warm-up $L_{warmup}=30$gg | **PRESENTE** | R-9.2 |
| NFR-1 | Latenza $L_{max}=30$s (M-2 open) | **PRESENTE** | NFR-6.2 `[B-1]` |
| NFR-2 | DSR gate primario | **PRESENTE** | NFR-8.1 |
| NFR-3 | PBO gate fragilità | **PRESENTE** | NFR-8.2 |
| NFR-4 | Lifecycle stabile cross-regime | **PRESENTE** | NFR-8.4 |
| NFR-5 | 80pt pre-condizione emissione | **PRESENTE** | CN-5.1 (sostanza; riclassificato CN) |
| CN-1 | "Solo emissione" non negoziabile | **PRESENTE** | CN-1.1 |
| CN-2 | Marker normativi 6 terminali | **PRESENTE** | CN-7.7 |
| CN-3 | Segnale informativo, **non consulenza**, MiFID II | **PARZIALE** | MiFID-retail + solo-emissione presenti (R-2.1, CN-1.1); la sotto-proposizione "**non è consulenza in materia di investimenti**" NON è restata come proposizione di prodotto → vedi lista INTUIZIONE-DA-DECIDERE |
| CN-4 | Separazione segnale/esecuzione, porta 10002 mai aperta | **PRESENTE** | CN-7.1 + CN-7.2 |
| CN-5 | Audit log + retention 90gg/permanente | **PRESENTE** | CN-7.6 |
| CN-6 | Minimizzazione PII | **PRESENTE** | CN-7.8 |
| CN-7 | Gating qualitativo cash europei | **PRESENTE** | CN-7.9 (+ CN-9.2 per il low/high) |

**Elementi del vecchio non in forma di requisito numerato** (per completezza del gate anti-perdita):

| Elemento vecchio | Stato nel v2 | Categoria |
|---|---|---|
| §7.1 KPI di lifecycle enumerati (executable rate, target hit rate, **invalidation rate**, **missed target rate**, **$\pi_{t_2\mid t_1}$**, CVaR, MDD) | **PARZIALE** — il v2 nomina target hit/executable rate (NFR-8.4) e CVaR/MDD (NFR-8.5); **non enumera** invalidation rate, missed_target rate, $\pi_{t_2\mid t_1}$ come KPI di accettazione (i terminali `invalidated`/`missed_target` esistono come stati in R-4.1) | INTUIZIONE-DA-DECIDERE |
| §7.3 nota **M-16** (`cox_time_varying_active` metadato del bundle frozen) | **ASSENTE come requisito** — citato in §13 v2 come "CLOSED/già incorporato, non un blocco" | SCARTATO-CORRETTAMENTE (metadato interno del bundle, non vista prodotto) |
| §3.3 / §5.2 esempi numerici di payload e messaggio Telegram | **ASSENTE** — il v2 non riporta esempi numerici | SCARTATO-CORRETTAMENTE (illustrativo, non requisito verificabile; nessun CAP impone esempi) |
| §10.3 lista "dipendenze aperte FASE-D" (≥5 voci) | **PRESENTE in forma condensata** — R-10.2 elenca latenza/orario/$\theta_{reconcile}$/validator | PRESENTE |

### Lista — Requisiti del vecchio SCARTATI-CORRETTAMENTE

1. **§7.3 nota M-16 (`cox_time_varying_active`)** — metadato interno del bundle frozen (Cap.35.1 elemento 6 / Cap.31.3), deciso dal walk-forward del re-training. Non è vista operatore/prodotto: è meccanica interna del motore. La sua assenza come requisito di prodotto nel v2 è **corretta** (coerente con §12 v2 che dichiara Cap.35 non tracciato perché meccanismo interno). Non lo sostiene alcun CAP come requisito di **prodotto**.
2. **§3.3 / §5.2 esempi numerici** (payload `a3f7d9`, messaggio Telegram) — materiale illustrativo, non proposizione verificabile. Nessun CAP impone esempi nel documento di prodotto. Assenza corretta (semmai un arricchimento opzionale, non un requisito perso).

### Lista — Requisiti del vecchio INTUIZIONE-DA-DECIDERE (decisione AC)

1. **CN-3 (parziale): "il prodotto NON è consulenza in materia di investimenti".** Operativamente sensata come posizionamento di compliance, MA non tracciabile a un CAP chiuso: i CAP-fonte (Cap.1/2 Parte I) sostengono il profilo retail MiFID II e il vincolo "solo emissione" (entrambi **presenti** nel v2: R-2.1, CN-1.1), **non** la qualifica giuridica "non è consulenza". Quella era un'aggiunta di posizionamento legale/prodotto del vecchio, non derivata dai capitoli-fonte (nel v2 il tema disclaimer/consulenza è correttamente rinviato a "consulente legale esterno" in out-of-scope §2). **NON decido io**: AC decide se la spec di prodotto debba restare esplicitamente la proposizione "servizio informativo, non consulenza" (es. come CN aggiuntivo con etichetta `[WIKI-HINT MiFID II]` + ancoraggio interno), o lasciarla a FASE-D/consulente legale come fa il v2.
2. **KPI di lifecycle enumerati come criteri di accettazione (invalidation rate, missed_target rate, $\pi_{t_2\mid t_1}$).** Operativamente sensati e **tracciabili** a CAP chiusi (`CAP_01_parte_I.md:77` per i lifecycle rate; `CAP_02_parte_II.md:372` per $\pi_{t_2\mid t_1}$). Il v2 li copre solo parzialmente (target hit/executable rate in NFR-8.4; gli altri restano come stati terminali R-4.1, non come KPI di accettazione enumerati). Poiché sono **tracciabili alla fonte**, non sono "scarti corretti" automatici: la loro non-enumerazione come KPI di prodotto è una **scelta di perimetro** (il v2 enfatizza i gate go-live AC-GO-* anziché la batteria KPI completa). **NON decido io**: AC decide se il v2 debba enumerare la batteria KPI di lifecycle completa (come faceva il vecchio §7.1) o se la copertura via stati terminali + NFR-8.4/8.5 è sufficiente per la vista prodotto.

**Sintesi gate anti-perdita**: nessuna perdita indebita di requisito tracciabile. 34/36 requisiti numerati del vecchio PRESENTI in modo pieno; CN-3 PARZIALE (sostanza ancorata presente, sotto-proposizione non-ancorata rimessa ad AC); 2 elementi non-numerati SCARTATI-CORRETTAMENTE; 2 punti (CN-3 add-on, batteria KPI) INTUIZIONE-DA-DECIDERE. Nessuno di questi è bloccante per il PASS: sono decisioni di perimetro del supervisore, non bug.

---

## Applicazione RM-1 a me stesso

- **"Floor citazioni 100% verificato"**: VERIFICA parziale→completa. PROVE: CAP_01 e CAP_02 aperti integralmente e risolti dal reviewer in CLI; CAP_06/07/08/09/10 (60 citazioni) verificati riga-per-riga aprendo i file alle righe citate (delega di lettura a sub-agente con istruzione di riportare RESOLVE/MISRESOLVE/NOT-FOUND e contenuto effettivo). ALTERNATIVE ESCLUSE: misresolve non rilevati (ogni riga citata conteneva il contenuto rivendicato entro ~3 righe). ALTERNATIVE NON ESCLUSE: non ho riletto io personalmente ogni singola riga di CAP_06-10 (mi sono basato sul report citazione-per-citazione del sub-agente, che riporta il testo effettivo di ciascuna riga) — il rischio residuo è un errore di lettura del sub-agente, mitigato dal fatto che il report cita il testo testuale di ogni riga. Le citazioni CAP_01/CAP_02 (le più pesanti per i requisiti core) le ho risolte di persona.
- **"Grafia `[CODICE-EXISTENTE]` assente"**: VERIFICA piena. PROVE: Grep su `CODICE-EXISTENTE` nel documento → unica occorrenza è la riga 14 (nota di testa che la dichiara vietata). Nessun uso reale.
- **"Schema CANDLE poggia sul decoder, non sul wiki"**: VERIFICA piena. PROVE: Read di `export_directa_history_parametric.py:477-482` (mapping C/L/H/O + volume) e `STATO_CORRENTE.md:82` (M-1 `C;L;H;O;V` 2026-05-29). ALTERNATIVE ESCLUSE: il wiki `O;H;L;C` è citato solo come hint smentito.
- **"DIFF copertura: 36 requisiti vecchio, 34 pieni"**: VERIFICA piena. PROVE: lettura integrale di `SPEC_FUNZ_01_v1_storico.md` (matrice §10.4 = 36 righe) e mapping 1:1 al v2. ALTERNATIVE NON ESCLUSE: elementi del vecchio non in forma di requisito numerato (esempi, M-16, KPI table) li ho enumerati separatamente per non perderli, ma una proposizione minore sepolta nella prosa del vecchio potrebbe non essere stata catturata; ho campionato le sezioni 1-10 del vecchio, non parola-per-parola.

## Empirico-CLI da verificare

**(vuota)** — come atteso dal task card: la spec consolida fatti già chiusi (CAP frozen G-09) e non introduce fatti empirici nuovi. Nessuna asserzione richiede esecuzione contro DAPI o filesystem locale non versionato. Le uniche grandezze a sapore empirico (schema CANDLE, codici mese F/I, $L_{max}=30$s) sono richiami a prove già chiuse (`[PROVA-EMPIRICA]`) o blocchi dichiarati OPEN (`[B-N PROVVISORIO]`), non verifiche dovute in questa review.

---

*Review SPEC-FUNZ-01 v2 — spec_reviewer, sede CLI. Verdetto: PASS. Non ho corretto né riscritto il documento; non ho toccato il vecchio né i CAP. Commit a cura dell'Orchestratore.*
