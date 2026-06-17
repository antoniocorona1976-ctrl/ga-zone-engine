# REPORT — SPEC-FUNZ-01-B5 (Runtime DAPI, sessione & compliance)

> **Conferma letture obbligatorie**: ho letto, in quest'ordine e prima di scrivere, `tasks/METODO.md` (RM-1..RM-4 + RACC-METODO-2), `.claude/BASE_COMUNE.md`, `.claude/agents/spec_developer.md`, `tasks/ACTIVE_TASK.md` (card B5).
> **Conferma cecità (§0.1)**: requisiti derivati dai SOLI capitoli del perimetro-fonte (`CAP_09_parte_9.md` Cap.45/46/47/50/52/53/54 + `CAP_01_parte_I.md` Cap.1). NON ho aperto né citato `SPEC_FUNZ_01.md` (v2), `*_v1_storico*`, i file di chunking come fonte-requisiti, né i documenti B1/B2/B3/B4. ID `B5-*` auto-assegnati da zero. Il confronto-copertura con la v2 è del Reviewer.

---

## 1. Cosa è stato prodotto

`docs/spec_funzionale/SPEC_FUNZ_01_B5.md` — blocco unico runtime/sessione/compliance, **35 requisiti atomici** (N1) ripartiti:
- `B5-R` (operativi): 20
- `B5-CN` (vincoli/invarianti): 9
- `B5-NFR` (non-funzionali, compliance/retention/sicurezza): 7

7 sezioni: (1) scopo+cecità; (2) canale DAPI; (3) catalogo & rollover; (4) sessione; (5) gating cash; (6) audit & compliance; (7) matrice di tracciabilità + nota di rinvio + PENDING-empirico + nota RM-3.

Ogni requisito porta tracciabilità `[DOC-INTERNO CAP_09_parte_9.md:<riga>]` (o `CAP_01_parte_I.md`) e un valore dichiarato (operativo o di sistema/replay).

## 2. Ipotesi di partenza

- I capitoli del perimetro sono **chiusi PASS e congelati** (freeze G-09): li ho letti selettivamente solo per ancorare le citazioni `capitolo:riga`, senza ri-verificarli né ri-derivare la matematica.
- La card è autoritativa su perimetro, note di confine e PENDING noti; i pin-riga depositati li ho **raffinati a paragrafo e riletti token-per-token** (AC-G7) prima di citarli.
- Modalità B (cieca): nessuna importazione da v2/B*/chunking.

## 3. Decisioni rilevanti

- **Premesse, non ri-derivazioni (AC-B5-1)**: i fatti delle giunte (Cap.27-28; 5€/B1; gating-su-messaggio/B4; lifecycle-state-machine/B3; epoca-E5/B8; schema-dato/B6) sono **citati come premessa** nella §7.2, mai consolidati in un requisito B5. In particolare ho **scartato** la tentazione di scrivere requisiti su EGARCH-recalibration, pipeline di emissione, contratto del messaggio, decoder/format: 0 requisiti B5 su Cap.27-28.
- **Cap.45 e Cap.50 trattati come contesto** (AC, nota di confine): non ho derivato requisiti propri di recovery/errori (Cap.50) né dalla premessa Cap.45. Cap.45 fornisce solo l'ancoraggio "canale = DAPI servizio locale" (rif. :27 usato per B5-R-01, che è materia di Cap.46, non di Cap.45).
- **Atomicità (N1)**: ho spezzato concern impacchettati. Esempi: il blocco audit-lifecycle è separato in B5-R-19 (granularità per-stato) e B5-R-20 (`timeout_cause` su MISSED_TARGET); il gating è separato in B5-R-16 (annotazione), B5-CN-07 (non-soppressione), B5-CN-08 (fuori-GA), B5-NFR-02 (config versionato), B5-R-17 (marker audit), B5-CN-09 (replay). La retention è separata in B5-NFR-05 (90gg rolling) e B5-NFR-06 (permanente su emissione).
- **Dualità miniFIB/FIB-pieno**: consolidata la sola parte miniFIB (1€, esecuzione operatore) in B5-R-10; il moltiplicatore 5€ del FIB pieno è premessa di B1 (§7.2), non ri-asserito.
- **PENDING-empirico marcati, non sovra-marcati (AC-B5-2)**: marcati i 3 noti (Mar/Dic; rollover reale V-3; calendario V-2). NON marcati i fatti già `[PROVA-EMPIRICA 2026-05-27]` (banner, porte) né il valore della finestra 08:00-22:00.
- **RM-3 sul wiki (AC-B5-3)**: nota dedicata §7.5; etichette `[WIKI-HINT, da verificare]` salvo dove esiste già PROVA-EMPIRICA.

## 4. Misura prima/dopo (greenfield di consolidamento)

Track documentale, nessuna metrica GA. La misura onesta è di **leggibilità da esterno**:
- **PRIMA**: il perimetro runtime/sessione/compliance vive disperso in 7 capitoli normativi della Parte 9 (Cap.46/47/52/53/54 + contesto 45/50), intervallato da derivazioni matematiche e note di replay; non leggibile come elenco di requisiti di prodotto tracciabili.
- **DOPO**: **35 requisiti** R/CN/NFR atomici, ciascuno con tracciabilità a riga-fonte e valore dichiarato, più una matrice e una nota di rinvio che separa esplicitamente cio che è consolidato qui da cio che è premessa di altri blocchi. Un lettore esterno risponde alle 7 domande del done-when (§5 della card) senza ambiguità.

## 5. Domande aperte

Nessun blocco bloccante incontrato (vedi §6 - Blocchi). I 3 PENDING-empirico (§7.4 del documento) non sono blocchi di derivazione: sono fatti correttamente marcati come non-ancora-verificati, attesi dai probe V-2/V-3 e dalla decodifica ANAG, già fuori scope per Cap.55. Restano in carico al validator/FASE-D, non al presente blocco.

## 6. Blocchi / Domande aperte

Nessun blocco aperto. Il task è stato mappato interamente derivando dai capitoli del perimetro; nessun requisito è stato scritto a valle di un blocco, quindi **nessun marcatore `[B-N PROVVISORIO]`** è presente nel documento.

## 7. Criterio di rollback

Il documento è un consolidamento additivo in `docs/spec_funzionale/` (nuovo file, nessuna modifica a CAP congelati). Rollback = rimozione del file `SPEC_FUNZ_01_B5.md` + report. Nessun impatto sul motore né su altri blocchi (le premesse sono citazioni, non dipendenze scritte).

---

## Applicazione RM-1 a me stesso

Non ho introdotto nuove dichiarazioni "verificato X" di mia produzione: ogni asserzione fattuale è un **richiamo** a un capitolo chiuso con provenienza `[DOC-INTERNO CAP_09_parte_9.md:<riga>]`. Verifiche puntuali su me stesso:

- **"Le righe citate dicono cio che asserisco"** - riletti token-per-token i paragrafi citati prima di scrivere ogni ID. Esempi controllati: porta 10002 mai aperta (`:39`), prefix-match banner (`:29`), "22:00 non chiude active" (`:292`, `:302`), 6 eventi terminali (`:353`, `:355`), retention 90gg/permanente (`:364`, `:365`), addebito 20EUR/200EUR (`:373`). ALTERNATIVE NON ESCLUSE: nessuna - sono citazioni dirette, non inferenze.
- **"35 requisiti, ripartizione 20/9/7"** - conteggio diretto sugli ID nel documento §7.1. ALTERNATIVE ESCLUSE: nessun ID duplicato (range R-01..R-20, CN-01..CN-09, NFR-01..NFR-07 contigui).
- **Stato empirico delle PROVA-EMPIRICA**: ho citato lo stato esatto presente nei CAP (banner/porte 2026-05-27; F/I 2026-05-27 e M-4 2026-05-29) senza promuovere a "verificato" cio che i CAP marcano come parziale (es. soglia "14 conn / ~30s" citata come verifica parziale smentita nel regime ~1Hz, B5-CN-03). ALTERNATIVE NON ESCLUSE: i codici mese Mar/Dic e il rollover reale restano PENDING (§7.4), non asseriti.
- **RM-2**: non ho introdotto decoder/parser; lo schema-dato è premessa di B6, non consolidato. Nessuna nuova citazione `[CODICE-ESISTENTE]` da me prodotta in questo blocco.
- **RM-3**: fonti wiki Directa etichettate `[WIKI-HINT, da verificare]` (§7.5); nessuna conclusione strutturale poggia su solo livello-4.

## Lista PENDING-empirico (riepilogo)

| # | Requisito | Pending | Origine |
|---|-----------|---------|---------|
| 1 | B5-R-07 | codici mese Mar/Dic Directa-IDEM (oltre F/I) | non listati, fuori scope Cap.55 - ANAG a mercato aperto |
| 2 | B5-R-08 / B5-R-09 | comportamento rollover/CONTRACT_SWITCH a scadenza reale | probe V-3 (terza venerdi reale) |
| 3 | B5-R-11 | convenzione calendario/giorni-di-trading della finestra | probe V-2 (calendario IDEM) |

NON pending (citati con stato empirico esatto, non sovra-marcati): valore finestra 08:00-22:00; banner gateway e porte 10001/10002/10003 (`[PROVA-EMPIRICA 2026-05-27]`); codici F/I (`[PROVA-EMPIRICA 2026-05-27 / M-4 2026-05-29]`).

---

## Tabella verifica Acceptance Criteria

| AC-ID | Stato | Evidenza (file:riga / sezione) |
|-------|-------|--------------------------------|
| AC-G1 (atomicità N1) | OK | un concern per requisito; concern impacchettati spezzati - es. SPEC_FUNZ_01_B5.md §6 (B5-R-19/B5-R-20), §5 (B5-R-16/CN-07/CN-08/NFR-02/R-17/CN-09), §6 (B5-NFR-05/NFR-06) |
| AC-G2 (tracciabilità a riga CAP_09/CAP_01) | OK | ogni requisito ha `[DOC-INTERNO ...:riga]`; matrice §7.1 |
| AC-G3 (valore operativo o di sistema/replay) | OK | campo *Valore* su ogni requisito; colonna "Valore" in §7.1 |
| AC-G4 (divieto "verificato X" RM-1) | OK | nessun "verificato" auto-prodotto; sez. "Applicazione RM-1 a me stesso" |
| AC-G5 (etichette RM-3 su fonti esterne / wiki) | OK | SPEC_FUNZ_01_B5.md §7.5; `[WIKI-HINT, da verificare]` salvo PROVA-EMPIRICA |
| AC-G6 (grafia canonica) | OK | `[CODICE-ESISTENTE]`/`[PROVA-EMPIRICA]`/`[DOC-INTERNO]` canonici; nessuna grafia deprecata |
| AC-G7 (floor citazioni 100% verificato in review - pin raffinati token-per-token) | OK | pin risolti a paragrafo via Read prima della citazione; righe ri-lette (Cap.46/47/52/53/54, Cap.1) |
| AC-G8 (cecità preservata) | OK | §1.3 + conferma in testa al report; nessuna traccia v2/B*/chunking |
| AC-G9 (scope "tutto e solo" il perimetro §1) | OK | §7.3 fuori-scope con destinazione; §7.2 premesse non consolidate |
| AC-G10 (matrice tracciabilità + nota di rinvio) | OK | SPEC_FUNZ_01_B5.md §7.1 + §7.2 |
| AC-G11 (invarianti come tali) | OK | invarianti marcati `B5-CN-*` con valore "di sistema/replay" |
| AC-B5-1 (premesse, non ri-derivazioni) | OK | §7.2 nota di rinvio; 0 requisiti B5 su Cap.27-28; report §3 |
| AC-B5-2 (PENDING-empirico marcati, non sovra-marcati) | OK | SPEC_FUNZ_01_B5.md §7.4 + nota B5-R-07; report "Lista PENDING-empirico" |
| AC-B5-3 (RM-3 sul wiki Directa) | OK | SPEC_FUNZ_01_B5.md §7.5 |
