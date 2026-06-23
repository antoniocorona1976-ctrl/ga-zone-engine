# REPORT — SPEC-FUNZ-01-B8 (Confine / chiusura della spec — blocco 8/8, ULTIMO)

> **Track**: Business-spec (SPEC-FUNZ). **Sede**: CLI. **Tag commit**: `[SPEC-FUNZ-01-B8]`. **Iterazione**: 1 (prima consegna).
>
> **Letture obbligatorie eseguite, in quest'ordine, PRIMA di scrivere** (conferma):
> 1. `tasks/METODO.md` — RM-1..RM-4 + RACC-METODO-2 + §Superfici di esecuzione + Freeze G-09 (G-09 righe 264-268; §Superfici GOV-SURFACES-01 righe 240-244).
> 2. `.claude/BASE_COMUNE.md` — ciclo comune, classificazione finding, disciplina file di stato, pre-consegna §5/§8.
> 3. `.claude/agents/spec_developer.md` — ruolo (incl. §Atomicità N1, §Gestione blocchi F6, §Pre-consegna).
> 4. `tasks/ACTIVE_TASK.md` — card B8 (fonte di verità per perimetro/AC/done-when).

---

## 1. Cosa è stato prodotto

- `docs/spec_funzionale/SPEC_FUNZ_01_B8.md` — blocco di confine/chiusura della spec funzionale del motore FIB. Contiene:
  - **Sez.1 Fasizzazione PHASE-1 / PHASE-2** (Cap.42): `B8-R-01` (PHASE-1 FIB-only), `B8-R-02` (PHASE-2 = dichiarazione senza implementazione), `B8-CN-01` (strumenti PHASE-2 previsti non erogati), `B8-CN-02` (estensioni metodologiche non implementate), `B8-CN-03` (costi noti della PHASE-1), `B8-CN-04` (cash europei NON cross-index PHASE-2), `B8-CN-05` (Parte 10 NON cross-index PHASE-2).
  - **Sez.2 Dipendenze aperte verso FASE-D** (Cap.55 + Cap.64, premessa Cap.36.3): `B8-R-03` (latenza Telegram M-2 OPEN), `B8-R-04` (theta_reconcile provvisorio), `B8-R-05` (10 parametri tuning post-go-live), `B8-R-06` (edge PENDING-empirico/validator), `B8-R-07` (lookup codici mese IDEM), `B8-R-08` (abilitazione FDAX standard), `B8-R-09` (vendor cross-index pluriennale), `B8-R-10` (flusso DAPI come training), `B8-R-11` (migrazione formato legacy-esteso), `B8-R-12` (implementazione codice pipeline).
  - **Sez.3 Lista PENDING-empirico** (tabella + note M-GOV-1 e "NON pending").
  - **Sez.4 Matrice di tracciabilità** (17 ID -> capitolo:riga + valore) + nota di rinvio (premesse / out-of-scope) + nota RM-3.
- `reports/REPORT_SPEC_FUNZ_01_B8.md` — questo report.

**Conteggio ID reale assegnato** (da zero, N1):

| Tipo | Conteggio | ID |
|---|---|---|
| `B8-R-*` | 12 | B8-R-01 .. B8-R-12 |
| `B8-CN-*` | 5 | B8-CN-01 .. B8-CN-05 |
| `B8-NFR-*` | 0 | nessuno (blocco di confine: la latenza Telegram, NFR per natura, è richiamata come dipendenza aperta B8-R-03, non come NFR di prima istanza) |
| **Totale** | **17** | — |

Conteggio plausibilmente contenuto, coerente con la natura di blocco di confine (nessun conteggio-target imposto dalla card; non gonfiato).

---

## 2. Ipotesi di partenza

- I quattro CAP sono **frozen G-09** e i diff a HEAD `3136a55` sono **vuoti** con gli SHA pinnati (`015c47a`/`28cfd2d`/`41447d3`/`b27c1e3`): verificato in pre-flight (sezione 4 sotto). I pin Sez.1/Sez.5 della card sono **puntatori di lavoro**; ho riletto ogni riga citata token-per-token a HEAD e cito la riga reale (AC-G7).
- B8 è **confine/chiusura**, non materia-prodotto nuova: ogni requisito è dichiarazione di confine/fasizzazione/dipendenza-aperta (AC-B8-CONFINE).
- Cap.42 / Cap.55 / Cap.64 sono **req-bearing** per il confine; Cap.36.3 / Cap.53 / Cap.41 sono **premesse** (citate per riga, non ri-derivate) — AC-B8-FRAMING.
- Le dipendenze aperte sono **dichiarate aperte, mai risolte**; l'edge e i valori d'esito sono **PENDING-empirico** (eredità cardine B7).
- Cecità modalità B: derivato dai soli capitoli del perimetro, cieco rispetto a v2/chunking/B1..B7.

**Classificazione dei capitoli (req-bearing vs premessa):**

| Capitolo | File:regione | Classificazione | Motivo |
|---|---|---|---|
| Cap.42 (Convenzione cross-index PHASE-2) | CAP_08_parte_8.md:141-182 | **req-bearing** | fonda il confine PHASE-1/PHASE-2 (B8-R-01/02, B8-CN-01/02/03) |
| Cap.55 (Punti aperti fuori scope, Parte 9) | CAP_09_parte_9.md:383-406 | **req-bearing** | fonda le dipendenze aperte versante DAPI (B8-R-03/07/08/09/10/12) |
| Cap.64 (Punti aperti fuori scope, Parte 10) | CAP_10_parte_10.md:226-238 | **req-bearing** | fonda le dipendenze aperte versante tape (B8-R-03/04/10/11/12, B8-CN-05) |
| Cap.36.3 (Carryover 10 parametri) | CAP_07_parte_VII.md:635-641 | **premessa (owned B7)** | citata solo come dipendenza aperta (B8-R-05); gate Cap.36 non ri-derivato |
| Cap.53 (Q-A-3 cash europei) | CAP_09_parte_9.md:330-342 | **premessa (owned B5)** | citata solo per confine cash NON cross-index (B8-CN-04); gating non ri-derivato |
| Cap.41 (Timeline sessioni FIB) | CAP_08_parte_8.md:107-137 | **premessa (owned B5)** | citata solo come dipendenza aperta M-GOV-1 (Sez.3); regola sessione non ri-consolidata |

---

## 3. Decisioni rilevanti

1. **Atomicità N1 sui concern di confine.** Ho separato la fasizzazione PHASE-1 (B8-R-01), la dichiarazione PHASE-2 senza implementazione (B8-R-02), gli strumenti previsti (B8-CN-01) e le estensioni non implementate (B8-CN-02) in ID distinti: sono concern verificabili separatamente. I "costi noti" della PHASE-1 (B8-CN-03) sono un concern di confine a sé (cosa il prodotto perde rispetto alla specifica ideale), distinto dal "cosa è in scope".
2. **Dipendenze aperte enumerate una per ID.** Ho scelto (sotto AC-B8-DEPS, opzione "requisiti distinti") di dare un ID a ciascuna dipendenza aperta verificabile separatamente (latenza, theta_reconcile, 10 param, edge, codici mese, FDAX, vendor, flusso-training, migrazione formato, codice pipeline). Motivo: ciascuna ha **stato esatto e destinazione distinti** ed è verificabile singolarmente in review; impacchettarle in un unico requisito-confine avrebbe sepolto sotto-requisiti nella prosa (violazione N1).
3. **R vs CN.** Ho usato `B8-CN-*` per i confini puramente vincolanti/normativi (strumenti previsti, estensioni non implementate, costi noti, cash NON cross-index, Parte 10 NON cross-index) e `B8-R-*` per le dichiarazioni di fasizzazione e per le dipendenze aperte (che il prodotto "dichiara aperte"). Distinzione coerente con lo schema-ID Sez.0.2.
4. **Nessun NFR di prima istanza.** La latenza Telegram è NFR per natura, ma in B8 è richiamata **solo** come dipendenza aperta (B8-R-03), non specificata come NFR: la sua specifica NFR è materia dei blocchi precedenti (premessa). Quindi `B8-NFR-*` riservato ma non istanziato. Questo evita di ri-derivare materia di altro blocco (AC-G10).
5. **M-GOV-1 trattato come dipendenza aperta, non come requisito-sessione.** La sessione 08:00-22:00 CET è premessa B5-owned; in B8 cito Cap.41 `:133` **solo** per l'upgrade empirico M-GOV-1 (PENDING-empirico), senza ri-consolidare la regola operativa (AC-B8-FRAMING).
6. **PROVA-EMPIRICA riportate come già dichiarate dal capitolo.** Il dato FDAX 2026-05-27 (account non abilitato, `ERR;1007`) in B8-R-08 è riportato come fatto del capitolo frozen, non ri-verificato (no probe di zelo; AC-G5, card Sez.0.1).

---

## 4. Misura prima/dopo (greenfield di consolidamento)

Adattata onestamente al greenfield (niente metriche GA inventate):

- **PRIMA**: il confine del prodotto (cosa è in PHASE-1, cosa è dichiarato-ma-non-implementato in PHASE-2, quali dipendenze restano aperte verso FASE-D) era **disperso** nei capitoli di rinvii (Cap.42 confine fasizzazione; Cap.55/Cap.64 punti aperti) — non leggibile come perimetro unico da un esterno, e non tracciabile requisito-per-requisito.
- **DOPO**: **17 requisiti di confine** (12 R + 5 CN) tracciati, ciascuno con citazione `capitolo:riga` reale a HEAD, valore operativo/di sistema dichiarato, e — per le dipendenze aperte — **stato esatto** ("aperta/provvisoria, rinviata a FASE-D/monitoring/Appendice E") e destinazione. Lista PENDING-empirico (8 voci) marcata, non asserita. Matrice di tracciabilità completa.

**Pre-flight freeze G-09 (verificato, pre-derivazione):** `git diff <frozen> HEAD -- <file>` **vuoto** per tutti e quattro:
- CAP_08_parte_8.md vs `015c47a` -> vuoto
- CAP_09_parte_9.md vs `28cfd2d` -> vuoto
- CAP_10_parte_10.md vs `41447d3` -> vuoto
- CAP_07_parte_VII.md vs `b27c1e3` -> vuoto

HEAD = `3136a557211d576d3be6dd6589a3c561465c551d`. I pin Sez.1/Sez.5 sono stati comunque riletti token-per-token e citati alla riga reale (AC-G7).

---

## 5. Domande aperte (Blocchi / Domande aperte — F6, batch unico)

**Nessun blocco bloccante.** Il task è stato mappato interamente dai soli capitoli del perimetro; tutti i requisiti sono risolvibili dai documenti frozen senza decisione di Planner/AC. Nessun marcatore `[B-N PROVVISORIO]` è stato apposto (nessun requisito è a valle di un blocco aperto).

**Osservazioni non bloccanti (per il Reviewer/AC, non sono blocchi):**

- **O-1 (informativa).** La scelta R-vs-CN per i requisiti di confine (es. B8-CN-04 vs un'eventuale forma B8-R) è una convenzione tassonomica; ho applicato il criterio "CN = vincolo/confine normativo puro; R = dichiarazione di fasizzazione o dipendenza-aperta". Se il Reviewer ritiene preferibile un'altra ripartizione tassonomica, è ridenominazione cosmetica senza impatto sulla copertura (NEUTRO atteso).
- **O-2 (informativa).** Le dipendenze aperte versante DAPI (Cap.55) e versante tape (Cap.64) hanno **doppia citazione** quando il confine è ribadito in entrambi i capitoli (es. flusso DAPI come training: `CAP_09:404` + `CAP_10:238`; latenza Telegram: `CAP_09:402` + `CAP_10:237`; codice pipeline: `CAP_09:406` + `CAP_10:231`). Ho mantenuto entrambe per fedeltà alla fonte; non è ridondanza ma doppia fondazione.

---

## Tabella di verifica AC

| AC-ID | Stato | Evidenza (file:riga) |
|---|---|---|
| AC-G1 (N1 atomicità) | OK | ogni ID una proposizione; concern distinti separati: `SPEC_FUNZ_01_B8.md` B8-R-01/02 + B8-CN-01/02/03 (fasizzazione vs dichiarazione vs strumenti vs estensioni vs costi); dipendenze aperte una per ID B8-R-03..R-12 |
| AC-G2 (tracciabilità a riga) | OK | ogni ID cita riga reale: es. B8-R-01 -> `CAP_08_parte_8.md:167,:143,:145`; B8-R-04 -> `CAP_10_parte_10.md:131,:232`; matrice Sez.4.1 |
| AC-G3 (valore operativo/di sistema) | OK | ogni ID ha bullet "Valore operativo/di sistema"; colonna valore in matrice Sez.4.1 |
| AC-G4 (no "verificato X" di prima istanza — RM-1) | OK | nessun blocco `VERIFICA/PROVE/...`; tutte richiami a CAP frozen; dichiarato `SPEC_FUNZ_01_B8.md` Sez.0.5 |
| AC-G5 (etichette RM-3) | OK | tutte `[DOC-INTERNO ...]`; PROVA-EMPIRICA FDAX riportata come già dichiarata dal capitolo (B8-R-08 + Sez.4.3) |
| AC-G6 (grafia canonica) | OK | `[DOC-INTERNO]`/`[CODICE-ESISTENTE]`/`[PROVA-EMPIRICA]`/`[WIKI-HINT]`; nessuna `[CODICE-EXISTENTE]` (grep -> 0, vedi RM-1 a me stesso #5); Sez.4.3 |
| AC-G7 (rilettura pin token-per-token) | OK | tutte le righe pinnate rilette a HEAD `3136a55`; cito riga reale (report Sez.4 pre-flight) |
| AC-G8 (floor citazioni 100%) | OK | tutti e 17 gli ID hanno >=1 citazione `[DOC-INTERNO ...]` risolvibile alla riga; matrice Sez.4.1 |
| AC-G9 (cecità preservata) | OK | nessun ID importato, nessun conteggio-target, nessuna partizione da v2/chunking; `SPEC_FUNZ_01_B8.md` Sez.0.3 |
| AC-G10 (scope "tutto e solo") | OK | copre tutto e solo il confine di Cap.42+Cap.55+Cap.64; materia B1..B7 non ri-derivata (premesse Sez.4.2 + out-of-scope) |
| AC-G11 (matrice + nota di rinvio) | OK | `SPEC_FUNZ_01_B8.md` Sez.4.1 (matrice) + Sez.4.2 (nota di rinvio premesse/out-of-scope) |
| AC-B8-CONFINE (cardine) | OK | ogni ID è dichiarazione di confine/fasizzazione/dipendenza-aperta; verbi ammessi ("dichiara"/"rinviata"/"resta dipendenza aperta"); 0 aperture/risoluzioni; auto-check sotto |
| AC-B8-NOASSEMBLY (anti meta-processo) | OK | 0 requisiti di assemblaggio/indicizzazione/avvio-FASE-D; nota in evidenza `SPEC_FUNZ_01_B8.md` Sez.0.4; out-of-scope Sez.4.2; auto-check sotto |
| AC-B8-FRAMING (verifica di fondazione) | OK | Cap.42/55/64 req-bearing; Cap.36.3/53/41 premesse (citate per riga, non fonti primarie); Sez.2 classificazione + Sez.4.2 |
| AC-B8-DEPS (stato esatto, non risolte) | OK | ogni dipendenza aperta col suo stato esatto e destinazione; edge PENDING-empirico; `SPEC_FUNZ_01_B8.md` Sez.2 + Sez.3; auto-check sotto |

---

## Applicazione RM-1 a me stesso

Ogni mia affermazione di verifica ha sostegno operativo puntuale:

1. **"Freeze G-09 regge a HEAD"** — VERIFICA: `git diff <frozen> HEAD -- <file>` per tutti e quattro i CAP. PROVE: output vuoto per CAP_08 vs `015c47a`, CAP_09 vs `28cfd2d`, CAP_10 vs `41447d3`, CAP_07 vs `b27c1e3` (eseguito in pre-flight; HEAD `3136a55`). ALTERNATIVE ESCLUSE: file slittato post-pin (escluso: diff vuoto). ALTERNATIVE NON ESCLUSE: nessuna.
2. **"Le righe citate corrispondono alla riga reale a HEAD"** — VERIFICA: rilettura token-per-token via Read di ogni regione pinnata. PROVE: Cap.42 `CAP_08_parte_8.md:141-182` (Read offset 130, lim 70); Cap.55 `CAP_09_parte_9.md:383-406` (Read offset 375); Cap.64 `CAP_10_parte_10.md:226-238` + theta_reconcile `:131` (Read offset 218 e 120); premesse Cap.36.3 `:635-641` (Read offset 628), Cap.53 `:338` (Read offset 330), Cap.41 `:133` (Read offset 130 + Grep `^## Capitolo 41` -> `:107`). ALTERNATIVE ESCLUSE: pin assunto diverso da riga reale (escluso: ogni riga riletta). NON ESCLUSE: nessuna.
3. **"Ogni dipendenza aperta è dichiarata aperta, non risolta"** — VERIFICA: rilettura del testo-fonte per ogni B8-R-03..R-12 e controllo che il capitolo usi verbi di rinvio. PROVE: es. `CAP_10_parte_10.md:131` "parametro provvisorio non congelato ... rinviata a FASE-D"; `CAP_09_parte_9.md:402` "resta `OPEN` come carryover ad Appendice E"; `CAP_07_parte_VII.md:641` "non è task di Parte VII". ALTERNATIVE ESCLUSE: capitolo che chiude la dipendenza (escluso: tutte le voci sono in capitoli "Punti aperti fuori scope" o premesse di carryover). NON ESCLUSE: nessuna.
4. **"L'edge non è asserito (PENDING-empirico)"** — VERIFICA: il documento cita l'edge solo come dipendenza aperta. PROVE: `SPEC_FUNZ_01_B8.md` B8-R-06 ("non asserisce alcun esito") + Sez.3 ("nessun esito d'edge asserito"); fondazione `CAP_10_parte_10.md:131` (soglie provvisorie). ALTERNATIVE ESCLUSE: asserzione d'esito d'edge (escluso: nessun valore/verdetto d'edge scritto). NON ESCLUSE: nessuna.
5. **"Grafia canonica, nessuna grafia deprecata di CODICE-ESISTENTE come etichetta-fonte"** — VERIFICA: grep sul documento prodotto sulla stringa deprecata (con "X"). PROVE: il primo grep ha trovato **1 occorrenza** — una meta-menzione nella nota RM-3 (Sez.4.3) che citava il nome della grafia deprecata per dichiarare che NON è usata; **riformulata** (descritta a parole, senza scrivere la stringa) -> grep post-fix = **0 occorrenze**. Nessun uso della grafia deprecata come etichetta di citazione (le etichette-fonte sono tutte `[DOC-INTERNO ...]`). ALTERNATIVE ESCLUSE: uso reale della grafia deprecata come etichetta (escluso: l'unica occorrenza era meta-menzione, ora rimossa). NON ESCLUSE: nessuna.
6. **"Nessun M nuovo, nessun M chiuso da B8"** — VERIFICA: lettura `tasks/CARRYOVER.md`. PROVE: M-2 OPEN (`CARRYOVER.md:21`), M-GOV-1 APERTO (`CARRYOVER.md:37`); B8 li richiama come dipendenze aperte (B8-R-03, Sez.3 nota M-GOV-1) senza chiuderli, e non emette M nuovi. ALTERNATIVE ESCLUSE: incardinamento che chiude un M (escluso: stato lasciato OPEN/APERTO). NON ESCLUSE: la review può decidere di incardinare/annotare un M (allora l'Orchestratore aggiorna CARRYOVER in chiusura).

---

## Censimento M aperti (registro CARRYOVER/STATO)

B8 **non chiude** alcun M e **non emette** M nuovi (atteso dalla card Sez.2). M aperti richiamati come dipendenze aperte dichiarate:

| M-ID | Stato | Destinazione | Trattamento in B8 |
|---|---|---|---|
| M-2 (latenza Telegram L_max=30s) | OPEN | Appendice E / FASE-D | richiamato come dipendenza aperta (B8-R-03); misura empirica PENDING, mai asserita |
| M-GOV-1 (orario sessione, upgrade empirico) | APERTO | probe V-1/V-2 / FASE-D | richiamato come dipendenza aperta (Sez.3 nota M-GOV-1); upgrade PENDING, mai asserito |

---

## Lista PENDING-empirico (riepilogo report)

8 voci, tutte ereditate, nessuna nuova (vedi `SPEC_FUNZ_01_B8.md` Sez.3 per la tabella completa con destinazioni): latenza Telegram L_max=30s; upgrade empirico orario sessione (M-GOV-1); theta_reconcile; congelamento 10 parametri; run validator sull'edge; codici mese IDEM mancanti; abilitazione FDAX standard; vendor cross-index pluriennale. Tutte marcate come dipendenze aperte dichiarate, **non asserite**.

---

## Auto-check finali (espliciti, AC-B8-NOASSEMBLY + AC-B8-DEPS)

**(i) AC-B8-NOASSEMBLY — nessun requisito di assemblaggio/indicizzazione/avvio-FASE-D scritto.**
Verificato per ispezione di tutti e 17 gli ID: nessuno enuncia "assembla la serie B1..B8", "indicizza i blocchi", "cross-reference B1..B7", né "avvia FASE-D / specifica l'implementazione FASE-D". Queste materie compaiono **solo** nella nota in evidenza Sez.0.4 (come NON-requisiti) e nella tabella out-of-scope Sez.4.2 (con destinazione "task separato post-B8" / "FASE-D"). Auto-check: **PASS**.

**(ii) AC-B8-DEPS — nessuna dipendenza aperta dichiarata risolta.**
Verificato per ispezione di B8-R-03..R-12 e Sez.3: ogni dipendenza porta verbi di apertura/rinvio ("resta dipendenza aperta", "provvisoria, non congelata", "rinviata a FASE-D / Appendice E / monitoring / nuovo task Planner / PHASE-2") e uno stato esatto + destinazione; nessuna è dichiarata risolta/chiusa/calibrata/misurata. L'edge è citato come dipendenza aperta (B8-R-06), nessun esito asserito. Auto-check: **PASS**.

**Grep di forma sul documento prodotto** (eseguito in CLI):
- grafia deprecata di `CODICE-ESISTENTE` (con "X") -> **0 occorrenze** post-fix (la singola occorrenza iniziale era una meta-menzione nella nota RM-3, riformulata; vedi RM-1 a me stesso #5).
- conteggio ID: `B8-R-` = 12, `B8-CN-` = 5, `B8-NFR-` heading = 0 (verificato con `grep -oE`).
- `[DOC-INTERNO` (etichette-fonte) -> 19 occorrenze (floor citazioni 100% su 17 ID; alcuni ID hanno doppia citazione, vedi O-2).
- verbi vietati di apertura/risoluzione ("il prodotto supporta i cross-index", "la latenza è verificata", "theta_reconcile è calibrato a") -> **0 occorrenze** come asserzioni di prodotto (la stringa "verificata" compare solo in citazione del capitolo, es. PROVA-EMPIRICA FDAX, non come asserzione di prima istanza).

---

## Criterio di rollback

Il blocco è documentale e additivo (nuovo file `SPEC_FUNZ_01_B8.md` + report). Rollback = rimozione dei due file / revert del commit `[SPEC-FUNZ-01-B8]`, senza impatto su CAP frozen (non toccati), su `00_indice.md` (N/A, non toccato), o su altri blocchi (cecità: non letti, non modificati). Nessun M chiuso da revertire. Se la review riclassifica un confine o richiede ri-ID, è patch chirurgica sul solo `SPEC_FUNZ_01_B8.md` + sezione "Iterazione N" nel report.
