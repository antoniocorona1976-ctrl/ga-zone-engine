# REVIEW — SPEC-FUNZ-01-B4 (Emissione & consegna, blocco 4/8)

> **Track**: Business-spec (SPEC-FUNZ). **Sede**: CLI (GOV-SURFACES-01) — audit documentale no-DAPI, divieto CLI (niente probe di zelo).
> **Modalità**: CAP-review piena adattata al non-CAP, due giri ostili sugli AC di B4 (§3 card).
> **Oggetti**: `docs/spec_funzionale/SPEC_FUNZ_01_B4.md` + `reports/REPORT_SPEC_FUNZ_01_B4.md`, commit `d7908f6`.
> **Fonte floor citazioni**: `docs/methodology_v2/CAP_02_parte_II.md` (chiuso PASS `a1625df`, frozen G-09) — Cap.8 `:179-227` + Cap.9 `:231-281`. CAP non auditato negli AC (sola lettura).
> **Letture obbligatorie confermate**: `tasks/METODO.md` (RM-1..RM-4 + RACC-METODO-2); `.claude/BASE_COMUNE.md` (§3 sede CLI, §4 classificazione, §6 doppio giro, §8 onestà); `.claude/agents/spec_reviewer.md`; `tasks/ACTIVE_TASK.md` (card B4 completa, AC-G1..AC-G11).

---

## ITERAZIONE 1 — VERDETTO: **PASS**

**0 problemi bloccanti. 0 BUG REALE in tabella.** Floor citazioni 100% risolto. Cecità preservata. Confronto-copertura: nessun requisito di prodotto del perimetro emissione/consegna tracciato a CAP_02 Cap.8-9 è caduto. Osservazioni minori (NEUTRO) ammesse e una **segnalazione al supervisore** (classificazione dubbia su un confine fonte card-vs-mappa, NON bug di B4).

La nota di processo (documento derivato in cieco da una passata Developer interrotta, completato da una seconda passata che ne ha solo verificato campione + scritto il REPORT) è stata trattata come **input, non certificazione**: ho rieseguito l'audit pieno e indipendente, in particolare il floor citazioni 100% e l'audit cecità interamente a mio carico.

---

## 1. Tabella verifica AC-G1..AC-G11

| AC | Esito | Evidenza (file:riga) |
|---|---|---|
| **AC-G1** Atomicità (N1) | OK | Motivazione triplice scomposta in 4 (`B4-R-02..R-05`, :46-60); conseguenze non-emissione in 4 (`B4-R-11..R-14`, :116-130); 9 campi = 9 requisiti (`B4-R-17..R-25`, :175-211); retry scomposto in 6 (`B4-R-29..R-32`, `B4-CN-13/14`, :274-296). Nessun requisito impacchetta concern verificabili separatamente in modo non separato. *(Osservazione minore su `B4-CN-11`, vedi #3 — non viola N1.)* |
| **AC-G2** Tracciabilità obbligatoria | OK | Ogni requisito porta `[DOC-INTERNO CAP_02_parte_II.md:<riga>]` nel perimetro Cap.8 (`:179-227`) o Cap.9 (`:231-281`). Tutte le 44 righe distinte citate (verifica grep) cadono nel perimetro. Matrice completa :322-373. |
| **AC-G3** Valore operativo obbligatorio | OK | Ogni requisito dichiara *Valore operativo* o, per invarianti di processo (eccezione F-2), *Valore di sistema* con categoria esplicita. Uso di *Valore di sistema* circoscritto e legittimo: `B4-CN-03` (:102), `B4-R-11` (:118), `B4-R-13` (:126), `B4-NFR-04` (:236), `B4-R-30/31/32` (:280/284/288), `B4-CN-10/13/14` (:248/292/296). I requisiti con valore-operatore diretto (3 condizioni, filtro 80pt, contratto informativo, latenza-vincolo `B4-NFR-03`, anti-duplicato `B4-CN-09`) lo dichiarano come operativo — nessuna scappatoia F-2 abusiva. |
| **AC-G4** Divieto "verificato X" / latenza M-2 PENDING-empirico | OK | Nessuna dichiarazione "verificato X" di prima istanza (grep `verificat*` = 2 occorrenze: :40 descrive il comportamento del motore, non un claim d'autore; :235 è il corretto trattamento RM-1 della latenza). **`B4-NFR-04` (:234-236)**: $L_{max}=30$ s citato dal CAP **come valore di lavoro provvisorio**; verifica empirica del canale marcata **OPEN / PENDING-empirico / Appendice E**; mai "latenza verificata a 30 s". Verifica specifica AC-G4 superata. |
| **AC-G5** Etichette RM-3 su fonti esterne | OK | Telegram Bot API etichettata `[WIKI-HINT, da verificare]` e dichiarata **non fonte unica** (:316: "non fonda alcun requisito… ogni requisito regge sul Cap.8/9"). Nessun riferimento esterno non etichettato (grep Borsa/MiFID/IDEM = 0). |
| **AC-G6** Grafia canonica | OK | Solo `[DOC-INTERNO …]` e `[WIKI-HINT, da verificare]`. Grafia storica vietata `[CODICE-EXISTENTE …]` assente (grep = 0). |
| **AC-G7** Floor citazioni **100%** | OK | **Verifica esaustiva token-per-token a mio carico** (non campione). Vedi §2. Tutte le citazioni risolvono. |
| **AC-G8** Cecità preservata | OK | Vedi §4. Nessun ID importato (grep ID non-B4 = 0); nessuna frase identica alla v2 non presente nel Cap.8/9 (la prosa di B4 deriva dalla prosa del CAP, non da `SPEC_FUNZ_01.md`). |
| **AC-G9** Scope "tutto e solo" | OK | Copertura completa Cap.8.1-8.4 + Cap.9.1-9.6 (§1-§10 doc). Nessuno sconfinamento netto in B2/B3/B5/Parte III-IV-V/Appendice E: tutte le materie adiacenti rinviate esplicitamente (nota §11, :302-316). Vedi §5 (4 punti di confine). |
| **AC-G10** Matrice + nota di rinvio | OK | Matrice :320-375 (colonne ID \| proposizione \| citazione CAP \| valore). Nota di rinvio :302-316 distingue omissione voluta da gap. |
| **AC-G11** Invarianti evidenziati | OK | Filtro 80pt non allentabile `B4-CN-02` (:96); tutto-o-niente `B4-CN-04` (:112); anti-duplicato `B4-CN-09/10` (:242/246); no-edit/messaggio separato `B4-CN-11` (:255); ordine obbligatorio `B4-CN-06` (:171); assenza filtri post-emissione `B4-CN-01/05` (:42/138). Resi come famiglia `B4-CN-*`. |

---

## 2. Esito floor citazioni 100% (token-per-token, a carico Reviewer)

Verifica esaustiva di **tutte** le 44 righe distinte citate contro il CAP-fonte (Read di `CAP_02_parte_II.md:179-283` + ispezione numerica righe `:243-253`). Esito: **tutte risolvono**.

Punti critici verificati puntualmente:
- **9 campi del messaggio** (`B4-R-17..R-25`): `:243`→`signal_id`, `:244`→`direction`, `:245`→`setup_class`, `:246`→`entry_zone` $[p_{ref}-b,p_{ref}+b]$, `:247`→`target_1`+`target_2`, `:248`→`stop_loss`, `:249`→`timestamp_emission` CET, `:250`→`target_2_type`, `:251`→`stop_type`. **Mappatura riga↔campo esatta** (rischio principale del blocco, dato che il CAP enumera i 9 campi su righe consecutive: nessun off-by-one).
- Filtro 80pt `:209` (`B4-R-09`, `B4-CN-02`: directional/trade_range, simultaneo, "in nessun caso il cromosoma può allentare"). Analogia $b_{min}=5$ `:211` (`B4-CN-03`).
- Regola AND `:215`/`:217` (`B4-R-10`); conseguenze non-emissione tutte su `:219` (`B4-CN-04`, `B4-R-11/12/13/14`: nessun signal_id / nessuna pubblicazione / nessun log / continua a valutare).
- Latenza `:257`/`:259`/`:261` (`B4-NFR-03/04`).
- Anti-duplicato `:265` (`B4-CN-09/10`); notifica trigger `:271` (`B4-R-28`, `B4-CN-12`); errori `:275/:277/:278/:279/:281` (`B4-R-29/30/31/32`, `B4-CN-13/14`).
- Premesse Cap.7.3 via `:183` (`B4-CN-01`) e immutabilità Cap.6.2 via `:269` (`B4-CN-11`): citate dal Cap-fonte come premessa, non ri-derivate.

Nessuna citazione fuori perimetro (tutte ∈ `:179-227` ∪ `:231-281`). Nessuna citazione che "non risolve".

---

## 3. Esito audit cecità (AC-G8) — oggetto di audit attivo

- **ID importati**: grep di pattern `R-[0-9]`, `CN-[0-9]`, `NFR-[0-9]`, `B1-`, `B2-`, `B3-` escludendo `B4-(R|CN|NFR)-` → **0 match**. Tutti gli ID sono auto-assegnati `B4-*` (schema dichiarato :20-26).
- **Frasi copiate dalla v2 non presenti nel Cap.8/9**: la prosa di B4 ricalca la prosa del **CAP-fonte** (es. "il raw touch della entry zone è sempre eseguibile", "in nessun caso il cromosoma può allentare il floor di 80 pt", l'enumerazione dei 9 campi) — ciò è atteso e legittimo (B4 deriva dal CAP). Confrontando con `SPEC_FUNZ_01.md` Sez.5/6: la v2 usa formulazioni proprie più aggregate (`R-5.1`, `R-6.1` "9 voci", ecc.) **diverse** dalla grana e dal fraseggio di B4. Nessuna firma lessicale della v2 (nessun `R-5.*`/`R-6.*`, nessun "9 voci", nessun "3 notifiche standard", nessun "mobile-first" che è invece termine-v2) compare in B4. **Cecità preservata.**

Esito: **nessuna traccia di rottura della cecità**. Nessun BUG REALE di processo.

---

## 4. Esito confronto-copertura (modalità B — compito esclusivo Reviewer)

Partizione autoritativa consultata: `docs/spec_funzionale/PROPOSTA_SUDDIVISIONE_SPEC_v2.md` (F-3). B4 = **emissione (Sez.5) + consegna Telegram (Sez.6)** della v2, fonti dichiarate dalla mappa: **CAP_02 PII Cap.8-9 + CAP_06 PVI Cap.27-29** (`:106`). Confronto requisito-per-requisito di `SPEC_FUNZ_01.md` Sez.5+6 (v2 congelata `ab7450f`) col perimetro emissione/consegna:

### Emissione (v2 Sez.5)
| v2 | Copertura in B4 | Esito |
|---|---|---|
| R-5.1 (decisione prima, no filtri post) | `B4-R-01` + `B4-CN-01` | **coperto** |
| R-5.2 (AND 3 condizioni + 80pt) | `B4-R-10` + `B4-R-06/07/08` + `B4-R-09` | **coperto** |
| CN-5.1 (filtro 80pt vincolo assoluto) | `B4-R-09` + `B4-CN-02` | **coperto** |
| R-5.3 (calcolabile da barre 1-min, no spread/book) | `B4-R-03` + `B4-R-04` | **coperto** |
| CN-5.2 (uniforme 08:00-22:00, no fasi speciali) | `B4-R-16` | **coperto** |

### Consegna (v2 Sez.6)
| v2 | Copertura in B4 | Esito |
|---|---|---|
| R-6.1 (9 voci in ordine) | `B4-CN-06` + `B4-R-17..25` | **coperto** (B4 più granulare) |
| R-6.2 (esclusione $\Delta t_{cromosoma}$/$T_{touch}^{max}$) | `B4-R-26` | **coperto** |
| R-6.3 (no gestione attiva, punto 8) | `B4-CN-08` | **coperto** |
| R-6.5 (anti-duplicato persistito) | `B4-CN-09` + `B4-CN-10` | **coperto** |
| R-6.6 (messaggio separato, no edit) | `B4-R-27` + `B4-CN-11` | **coperto** |
| NFR-6.2 [B-1] (latenza $L\le L_{max}$, 30s, OPEN) | `B4-NFR-03` + `B4-NFR-04` | **coperto** (PENDING-empirico) |
| R-6.7 (retry backoff, fallimento non pubblicato) | `B4-R-29/30/31/32` + `B4-CN-13/14` | **coperto** (B4 più granulare) |
| NFR-6.1 (mobile-first: self-contained, no scroll, prima schermata) | `B4-NFR-01` parziale (cattura "lettura mobile in attenzione limitata") | **fuori perimetro fonte B4** — il dettaglio mobile-first della v2 traccia a **CAP_06 Cap.29 (PVI)** (`SPEC_FUNZ_01.md:261`), fuori dalla fonte ristretta di B4 (solo CAP_02 Cap.8-9 per card §1) |
| R-6.4 (3 notifiche standard incl. transizione terminale) | parziale: B4 copre emissione + notifica trigger (`B4-R-28`); **non** la terza notifica (stato terminale) né "3 notifiche standard" | **fuori perimetro fonte B4** — la "notifica terminale" e l'enunciato "3 notifiche" tracciano in v2 a **CAP_06 Cap.29 (PVI)** (`:265`); nel CAP_02 Cap.9 (fonte B4) esistono solo emissione (9.2) e notifica trigger (9.5). Materia di lifecycle/consegna PVI, non Cap.8-9. |

**Requisiti B4 "in più" rispetto alla v2** (non scope creep): `B4-R-02` (motivazione punto 1), `B4-R-05` (operatore valuta esecuzione), `B4-CN-03` (analogia $b_{min}$), `B4-R-11/12/13/14` (conseguenze non-emissione scomposte), `B4-CN-04` (tutto-o-niente), `B4-CN-05` (raw touch sempre eseguibile), `B4-R-15` (patologie operatore), `B4-NFR-02` (latenza compatibile qualitativa), `B4-CN-07` (qualificatori senza impatto), `B4-CN-12` (notifica distinta). Tutti tracciati a righe del Cap.8/9 del CAP-fonte → grana N1 maggiore della v2 (più aggregata). **Legittimi.**

**Conclusione**: tutti i requisiti v2 del perimetro emissione/consegna **tracciati a CAP_02 Cap.8-9 sono coperti** in B4. Nessun gap di ricostruzione cieca. I due requisiti v2 non coperti (NFR-6.1 dettaglio mobile-first, R-6.4 terza notifica/"3 notifiche") tracciano a **CAP_06 PVI**, fuori dalla fonte ristretta a CAP_02 Cap.8-9 decisa dalla card §1 → **non gap di B4**, ma vedi #4 in tabella classificazione (segnalazione al supervisore: divergenza card-vs-mappa di chunking sulla fonte, F-3).

---

## 5. Esito dei 4 punti di confine (boundary-check)

1. **`trigger_event` (`B4-R-28`/`B4-CN-12`)** → cita `:271` (Cap.9.5). Consolida la **PUBBLICAZIONE/notifica Telegram**, non ri-deriva l'evento del lifecycle (premessa Cap.7.3 citata via `:183` in `B4-CN-01`, non consolidata). Confine B3/B4 rispettato. **OK, nessuno sconfinamento in B3.**
2. **Filtro 80pt (`B4-R-09`/`B4-CN-02`)** → la REGOLA è B4 (cite `:209`, Cap.8.2/8.3); il VALORE 80 è citato come dato già congelato (carve-out esplicito :94 "valore numerico 80 citato come dato già congelato in CAP-01… il suo congelamento è Parte V"). Confine regola/valore rispettato. **OK.**
3. **Anti-duplicato/errori (`B4-CN-10`/`B4-R-32`)** → prendono la POLITICA, non il FORMATO del log. `B4-CN-10` (:248): "il formato/schema del log di emissione è materia di altro blocco; qui solo il fatto che $\mathcal{P}$ è persistito". `B4-R-32` (:288): "Il formato del log è materia di altro blocco; qui si prende la politica". **OK, nessuno sconfinamento in B5/Cap.10.**
4. **Finestra 8:00-22:00 (`B4-R-16`)** → cita `:227` solo per "nessuna fase speciale di emissione per orario"; carve-out esplicito (:149) che il requisito di sessione operativa + M-GOV-1 è altro blocco. **OK, nessuno sconfinamento in B5.**

---

## 6. Problemi bloccanti
**Nessuno.**

## 7. Problemi non bloccanti (BUG REALE)
**Nessuno.**

## 8. Osservazioni minori (NEUTRO / segnalazione)

- **OM-1 (NEUTRO, atomicità)**: `B4-CN-11` (:255-258) raggruppa tre proposizioni — no-edit + "il messaggio revocato resta traccia storica non più attiva" + coerenza con l'immutabilità Cap.6.2. L'invariante centrale (no-edit) è uno solo; le altre due sono corollario/motivazione naturale. Difendibile sotto AC-G1 (granularità a discrezione del Developer, nessun conteggio imposto). **Non viola N1, non BUG.** Eventuale split solo se il supervisore lo desidera.
- **OM-2 (NEUTRO, marcatura)**: la v2 marcava la latenza come `NFR-6.2 [B-1 PROVVISORIO]`; la mappa di chunking (`:121`, `:179`, `:203`) raccomandava di recepirla in B4 come `[B-1 PROVVISORIO]`. B4 **non** usa il marcatore inline `[B-1 PROVVISORIO]`, ma tratta la latenza come **OPEN/PENDING-empirico** esplicito in `B4-NFR-04` (:234-236) e il REPORT non elenca blocchi aperti. Sostanzialmente equivalente; F6 (spec_reviewer §7) non scatta come BUG perché il REPORT non elenca B-N aperti da cui un requisito dipenda non marcato. **Non BUG.** Annotazione: all'assemblaggio finale conviene riconciliare la nomenclatura `[B-1 PROVVISORIO]` ↔ "PENDING-empirico".
- **#4 — SEGNALAZIONE AL SUPERVISORE (classificazione dubbia, F-3)**: la card B4 §1 ristringe la fonte al **solo CAP_02 Cap.8-9**, mentre la mappa di chunking autoritativa assegna a B4 anche **CAP_06 PVI Cap.27-29** (`PROPOSTA_SUDDIVISIONE_SPEC_v2.md:106`, `:121`). Conseguenza: due requisiti-prodotto della v2 del perimetro consegna (NFR-6.1 dettaglio mobile-first; R-6.4 "3 notifiche standard" incl. notifica terminale), tracciati in v2 a CAP_06 PVI, **non compaiono in B4**. **Non è un gap di B4** (B4 ha coperto fedelmente tutta la fonte che la card gli ha assegnato), ma è un divario di copertura prodotto reale rispetto alla v2/mappa. Per F-3, in caso di divergenza card-vs-mappa **prevale la mappa**: lo segnalo al supervisore come classificazione dubbia. **Rischio**: se nessun blocco successivo (B5 runtime/consegna, o il task di assemblaggio) recupera la materia CAP_06 PVI (mobile-first dettagliato, notifica di stato terminale, "3 notifiche standard"), all'assemblaggio finale due requisiti della v2 andrebbero persi. **Decisione al supervisore**: (a) confermare che la restrizione card→CAP_02 è voluta e che CAP_06 PVI sarà coperto altrove; oppure (b) un micro-pass B4 per incorporare la fonte CAP_06 PVI. **Non blocca il PASS di B4** (B4 è internamente corretto e completo sulla sua fonte).

---

## 9. Tabella "Classificazione per il supervisore"

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|------------------------|
| 1 | `B4-CN-11` raggruppa no-edit + traccia storica + coerenza immutabilità (atomicità borderline, invariante centrale unico) | `SPEC_FUNZ_01_B4.md:255-258` | NEUTRO | No (split opzionale, solo se AC lo vuole) |
| 2 | Latenza M-2 trattata come "PENDING-empirico" inline anziché col marcatore `[B-1 PROVVISORIO]` raccomandato dalla mappa di chunking | `SPEC_FUNZ_01_B4.md:234-236` | NEUTRO | No (equivalente sostanziale; riconciliare nomenclatura all'assemblaggio) |
| 3 | Requisiti B4 "in più" rispetto alla v2 (grana N1 maggiore) | vari | NEUTRO | No (legittimi, tutti tracciati al Cap.8/9) |
| 4 | Divergenza card-vs-mappa sulla fonte: card §1 ristringe a CAP_02 Cap.8-9; mappa assegna a B4 anche CAP_06 PVI Cap.27-29 → NFR-6.1 (mobile-first dettaglio) e R-6.4 (3 notifiche/notifica terminale) della v2 non in B4 | card `ACTIVE_TASK.md:32` vs `PROPOSTA_SUDDIVISIONE_SPEC_v2.md:106` | **classificazione dubbia → decisione supervisore** | No automatico (non è gap di B4; il supervisore decide se serve micro-pass o copertura altrove) |

Nessun BUG REALE. Le voci #1-#3 sono NEUTRO. La voce #4 è una segnalazione di confine (F-3) che richiede una decisione del supervisore ma **non condiziona il PASS di B4** (il blocco è corretto e completo rispetto alla fonte assegnatagli dalla sua card).

---

## 10. Applicazione RM-1 a me stesso

- **"Floor citazioni 100% risolto"** — VERIFICA: tutte le citazioni `[DOC-INTERNO CAP_02_parte_II.md:<riga>]` risolvono token-per-token. PROVE: Read di `CAP_02_parte_II.md:179-283` + ispezione numerica `awk` righe `:243-253` (mappatura 9 campi↔9 righe esatta) + grep delle 44 righe distinte citate (tutte ∈ `:179-227` ∪ `:231-281`). ALTERNATIVE ESCLUSE: off-by-one sull'enumerazione dei 9 campi (escluso: ogni riga corrisponde esattamente al campo affermato); citazione fuori perimetro (esclusa: grep delle righe). ALTERNATIVE NON ESCLUSE: nessuna.
- **"Cecità preservata"** — VERIFICA: nessun ID importato, nessuna firma lessicale v2. PROVE: grep ID non-B4 = 0; confronto diretto del fraseggio B4 vs `SPEC_FUNZ_01.md` Sez.5/6 (la prosa di B4 deriva dal CAP, non dalla v2; assenti i marcatori-v2 "9 voci"/"3 notifiche standard"/"mobile-first"). ALTERNATIVE NON ESCLUSE: un'eco lessicale isolata che non corrisponda né a un ID né a un termine-v2 distintivo — ricerca per quanto possibile esaustiva sui termini distintivi della v2; non rilevata.
- **"Confronto-copertura: nessun gap di ricostruzione cieca"** — VERIFICA: ogni requisito v2 di Sez.5/6 tracciato a CAP_02 Cap.8-9 ha copertura in B4. PROVE: mappatura requisito-per-requisito §4, contro le tracciabilità della v2 (`SPEC_FUNZ_01.md:238-240`, `:294-296`, `:555-568`) e la mappa di chunking (`PROPOSTA_SUDDIVISIONE_SPEC_v2.md`). ALTERNATIVE ESCLUSE: "B4 ha dimenticato un requisito del Cap.8-9" (escluso: tutti i 5 di Sez.5 e i 7+2 di Sez.6 mappati). ALTERNATIVE NON ESCLUSE: i due requisiti v2 tracciati a CAP_06 PVI (NFR-6.1, R-6.4) **non** sono coperti — ma per F-3 la loro fonte è fuori dal perimetro che la card assegna a B4 → segnalazione #4, non gap di B4.
- **"Nessuno sconfinamento di scope"** — VERIFICA: i 4 punti di confine reggono. PROVE: §5 (ogni confine con citazione+carve-out esplicito nel doc). ALTERNATIVE NON ESCLUSE: nessuna rilevata.
- **"Latenza M-2 PENDING-empirico, mai verificata"** — VERIFICA: `B4-NFR-04` tratta la latenza come aperta. PROVE: lettura :234-236 + grep `verificat*` (nessun "verificato a 30 s"). ALTERNATIVE ESCLUSE: dichiarazione "latenza verificata" (assente). ALTERNATIVE NON ESCLUSE: nessuna.

---

## 11. Lista "Empirico-CLI da verificare"

**VUOTA** (atteso). La spec consolida fatti già chiusi nel CAP frozen; non introduce fatti empirici nuovi. La latenza M-2 è PENDING-empirico per FASE-D (Appendice E) e NON è stata misurata da me (divieto CLI di zelo rispettato; audit documentale no-DAPI).

---

*Review ITERAZIONE 1 — spec_reviewer, sede CLI. Verdetto: PASS. Due giri ostili eseguiti. Nessun BUG REALE; 3 osservazioni NEUTRO + 1 segnalazione di confine (F-3) per decisione del supervisore. CAP-02 non modificato (freeze G-09 rispettato). Documento B4 non riscritto. DEV_STATUS non azzerato (lo fa l'Orchestratore alla chiusura).*
