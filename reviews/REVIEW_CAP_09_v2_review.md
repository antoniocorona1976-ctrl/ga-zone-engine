# Review CAP-DATA-02 Parte 9 v2 - Pipeline runtime FIB su Directa DAPI

**Verdetto**: PASS

## Sintesi metodologica

Audit ostile della rework v2 del capitolo Parte 9 (Cap.45-56) post-Review v1 FAIL.
Il Developer ha eseguito le 11 correzioni ratificate dal supervisore in modo
chirurgico, senza riscritture strutturali, senza modifiche alle Parti I-VIII,
senza riapertura delle decisioni ratificate e senza sconfinamento in CAP-DATA-03.
La numerazione capitoli Cap.45-Cap.56 e la scaletta a 12 sezioni sono invariate;
tutti i criteri PASS non toccati in Review v1 (input autoritativi verbatim, D-6,
no PHASE-2 cross-index su DAPI, 6 Gap formali, no sconfinamento CAP-DATA-03)
restano OK senza regressioni.

I 7 BUG REALI (B-1..B-7) sono chiusi con la formulazione richiesta dal punto di
controllo supervisore. I 4 MIGLIORA PERFORMANCE Opzione A (NB-1..NB-4) sono
chiusi con le precisazioni richieste e la tabella decisioni Cap.56 e' estesa
con D-9-NB2, D-9-NB3, D-9-NB4 coerentemente.

Nessun nuovo BUG REALE e' emerso nel secondo giro ostile. Solo due osservazioni
minori, entrambe a impatto operativo trascurabile sul comportamento del GA.

---

## Tabella esplicita di chiusura dei 11 finding di v1

| Finding | Tipo | Chiusura | Citazione passaggio nuovo (sintesi) | Nota |
|---------|------|----------|-------------------------------------|------|
| B-1 | BUG REALE | OK | Cap.52 r278: un segnale in stato `active` alla chiusura 22:00 CET non viene chiuso automaticamente; il counter Delta_t_cromosoma e' governato dalla state machine di Parte II Cap.7 r126 scavalcando l'interruzione notturna. Cap.52 r288: alla chiusura 22:00 CET marker `SESSION_CLOSE` in audit, NESSUNA chiusura automatica dei segnali ancora `active`. | Citazione esplicita Parte II Cap.7 r126; persistenza stato segnale su disco per ripresa al boot del giorno successivo formalizzata. |
| B-2 | BUG REALE | OK | Cap.48 r117 estende header CSV runtime con `tick_count` e `bar_synthetic`. Cap.48 r127 norma griglia 1-min uniforme. Cap.48 r129 distingue sample legacy come input di validazione Gap-5 vs format runtime normativo. | Sample r121-122 mostra esplicitamente barra reale (`bar_synthetic=False`) e barra sintetica (`bar_synthetic=True, tick_count=0, volume=0`). |
| B-3 | BUG REALE | OK | Cap.49 r164 tabella riga `bar_synthetic` + Cap.49 r166-170 paragrafo che norma 3 regimi distinti (FIB realtime push `BOOK_5`, FIB storico `CANDLERANGE`, cash `PRICE`). | Per FIB realtime: criterio bid1_lots>=1 AND ask1_lots>=1; per FIB storico: presenza/assenza nella risposta `CANDLE`; eliminato il presupposto erroneo push PRICE su FIB. |
| B-4 | BUG REALE | OK | Cap.47 r66-71: tabella futures FIB con colonna "Schema realtime" che riporta solo `BOOK_5, ANAG` per FIB6F/FIB6I/MINI6F/MINI6I/MINI6C. Cap.47 r73: nuova "Nota normativa sulla differenza di schema futures vs cash". | Cash europei (DGER, DSTX50, DITAS, DFRA) mantengono `PRICE` nella tabella r79-84. Giustificazione della differenza esplicitata. |
| B-5 | BUG REALE | OK | Cap.53 r297: gating POST-EMISSIONE come annotazione del messaggio Telegram; il gating non sopprime mai l'emissione, il segnale e' sempre emesso dalla state machine, sempre tracciato in audit con marker `SIGNAL_EMITTED`. Cap.53 r314: replay deterministico bit-exact preservato. | Tabella razionale r318-322 aggiornata: Q-A-2 esplicitamente "scartata" perche' viola replay deterministico; Q-A-3 ratificata come post-emissione. |
| B-6 | BUG REALE | OK | Cap.51 r245-249: limite 100 giorni e stato `RUNTIME_STALE_RESTART`; la pipeline runtime non riparte automaticamente per downtime >100gg, richiede intervento supervisore; riconciliazione DAPI/Portara rinviata a CAP-DATA-03. La regola non introduce alcuna dipendenza circolare con CAP-DATA-03. | Fallback Portara automatico rimosso. Bundle EGARCH non viene mai eseguito su un warm-up cross-source mescolato. |
| B-7 | BUG REALE | OK | Cap.49 r163 tabella riga `tick_count`: realtime (porta 10001) = count eventi `BOOK_5`; storico (porta 10003) = `NULL` (marker assente, non NaN numerico). Cap.49 r164 + r172: `bar_synthetic` resta booleano (trade vs no-trade); discriminante realtime/storico spostato sulla porta sorgente del record. | Consumer downstream configurato per ignorare `NULL` o proxy `volume`. |
| NB-1 | MIGLIORA PERFORMANCE (Opzione A) | OK | Cap.47 r92: ANAG normativo su `FIB6F` con descrizione attesa FTSE MIB INDEX FUTURE GIU26 (GIU26 = giugno 2026); probe empirico `FIB6I` citato sul next-month. Cap.47 r93: BOOK_5 normativo su `FIB6F`. Cap.47 r96 + Cap.55 r375: lookup parziale F=giu/I=set dichiarata. | Esempi normativi correttamente spostati su FIB6F come front-month; FIB6I conservato come ancora empirica e next-month. |
| NB-2 | MIGLIORA PERFORMANCE (Opzione A) | OK | Cap.47 r98-107 nuovo paragrafo "Policy switch front-month durante runtime (NB-2 Opzione A)": switch al boot del giorno t (terza venerdi); pipeline sottoscrive direttamente next-month saltando finestra 08:00-09:00; marker `CONTRACT_SWITCH` in audit con payload esempio FIB6F->FIB6I 2026-06-19; distinzione esplicita rispetto al filtro pre-expiry N=3 di training di Parte 8 Cap.39. Cap.56 r419 nuova voce D-9-NB2 con rollback. | Esempio numerico corretto (sessione 2026-06-19 = terza venerdi giugno 2026). Distinzione training vs runtime esplicita. |
| NB-3 | MIGLIORA PERFORMANCE (Opzione A) | OK | Cap.54 r339: tipologia evento estesa a 6 eventi terminali distinti (`SIGNAL_TARGET_1_HIT, SIGNAL_STOPPED, SIGNAL_INVALIDATED, SIGNAL_MISSED_TARGET, SIGNAL_EXPIRED, SIGNAL_REVOKED`). Cap.54 r341: `SIGNAL_CLOSED` sostituito da sei eventi distinti; per `SIGNAL_MISSED_TARGET` campo obbligatorio `timeout_cause in pretrigger/posttrigger` nel payload JSON. Cap.54 r351: retention permanente estesa ai sei eventi terminali. Cap.56 r420 nuova voce D-9-NB3 con rollback. | Coerenza con state machine Parte II Cap.7 esplicita; dashboard live (Parte VI Cap.30) e replay bit-exact (Parte II Cap.10) tutelati. |
| NB-4 | MIGLIORA PERFORMANCE (Opzione A) | OK | Cap.51 r240: L_warmup = 30 giorni di trading IDEM, congelato in Parte 9 (NB-4 Opzione A). Motivazione aritmetica: N_reg=20 + 50% margine; 30*840 = 25.200 barre copre W_norm=1000, T_warmup_EMA=74, T_warmup_norm=100 con margine residuo ~8.400 barre. Cap.56 r421 nuova voce D-9-NB4 con rollback (non rifinibile dentro Parte 9). | Replay bit-exact ripristinato (Cap.51 r251). Margine aritmetico verificato: 25.200 - 16.800 = 8.400, coerente. |

Tutti gli 11 finding ratificati sono chiusi con esito OK e formulazione
coerente con il punto di controllo supervisore. Nessuna formulazione vaga,
ambigua o parziale rilevata.

---

## Verifica esplicita assenza di regressioni rispetto alla Review v1

I criteri PASS gia' OK in Review v1 sono stati verificati nuovamente sul testo
di v2. Nessuna regressione rilevata.

| # | Criterio PASS | Esito v1 | Esito v2 | Note |
|---|---------------|----------|----------|------|
| 1 | Input autoritativi presenti verbatim | OK | OK | Banner Release 2.5.1 (Cap.46), CANDLERANGE / SUB / UNSUB (passim), schemi `ANAG/BOOK_5/PRICE` (Cap.47), codici 1004/1007/1030 (Cap.50), limite 100gg (Cap.46/51/55), rate-limit (Cap.46), conflitto DGo (Cap.46/50): tutti citati invariatamente. |
| 4 | Vincolo D-6 esplicitato come regola normativa | OK | OK | Cap.46 r45 + Cap.50 r219-225 invariati nell'essenza; nessuna riapertura. |
| 7 | Nessuna pretesa che PHASE-2 cross-index sia coperta da DAPI | OK | OK | Cap.53 r324 + Cap.55 r377 dichiarano esplicitamente che PHASE-2 e' rinviata a futuri cicli; nessun cross-index futures (FDXM, ES, ecc.) entra nello scope CAP-DATA-02. |
| 8 | I 6 Gap chiusi | OK formalmente | OK | Gap-1 (Cap.46 r43), Gap-2 (Cap.52 r263), Gap-3 (Cap.50 r207), Gap-4 (Cap.54 r348), Gap-5 (Cap.48 r147), Gap-6 (Cap.54 r359) tutti presenti e formalmente chiusi. Gap-3 ora non intercala piu' con B-6 perche' B-6 e' chiuso. |
| 9 | Nessuno sconfinamento in CAP-DATA-03 | OK formalmente; in v1 Cap.51 lo richiedeva di fatto creando dipendenza circolare (B-6) | OK | B-6 chiuso: continuita' tape, recupero gap, riconciliazione canonica giornaliera, storicizzazione strutturata tutti rinviati esplicitamente a CAP-DATA-03 (Cap.51 r247-249, Cap.55 r379-386). Nessuna dipendenza circolare residua. |

Criteri PASS che in v1 erano FAIL e ora OK:

| # | Criterio PASS | Esito v1 | Esito v2 |
|---|---------------|----------|----------|
| 2 | Tabella mappatura DAPI -> bundle frozen completa, no trasformazioni non specificate | FAIL (B-2, B-3, B-7) | OK |
| 3 | Decisione Q-A chiusa con verdetto + motivazione + PERIMETRO vincolante | FAIL (B-5) | OK |
| 5 | Warm-up stati condizionali specificato | PARZIALE (NB-4 non congelato, B-6 dipendenza fuori scope) | OK (L_warmup=30 congelato; B-6 rinviato esplicitamente a CAP-DATA-03) |
| 6 | Coerenza con CAP-DATA-01 sez.3.4 (gap semantics, bar_synthetic) | FAIL (B-3, B-2) | OK |

---

## Vincoli di scope rispettati

| Vincolo | Esito | Note |
|---------|-------|------|
| Nessuna modifica alle Parti I-VIII del doc v2 | OK | `git diff baeab2c..9bd35ba --stat docs/methodology_v2/` mostra modifiche solo a `CAP_09_parte_9.md` e `00_indice.md` (sola riga "Parte 9 ... [IN REVIEW v2]"). Nessun file di Parti I-VIII toccato. |
| Numerazione capitoli Cap.45..Cap.56 invariata; scaletta 12 sezioni invariata | OK | Verificato via grep `^## Capitolo`: esattamente 12 capitoli Cap.45-56 nell'ordine originale. |
| Nessuna riapertura delle decisioni ratificate (Q-A-3, D-1, D-6, C-1..C-7) | OK | Q-A-3 confermata (Cap.53 r294); D-1 confermato (Cap.54 r361); D-6 confermato (Cap.46 r45 e Cap.50 r219); C-1/C-2/C-3 invariati. |
| Nessuno sconfinamento in CAP-DATA-03 | OK | Cap.51 r247-249, Cap.55 r379-386 e Cap.48 r129 dichiarano esplicitamente i temi rinviati a CAP-DATA-03 senza definirli normativamente in Parte 9. |
| Nessun codice operativo introdotto | OK | Cap.55 r392 ribadisce esplicitamente: "Il presente capitolo e' metodologia, non codice." |
| 00_indice.md aggiornato a "Parte 9 ... [IN REVIEW v2]" senza altre modifiche | OK | Verificato: riga 75 di `00_indice.md` riporta esattamente "Parte 9 - Pipeline runtime FIB su Directa DAPI (~9-12 pp) [IN REVIEW v2]". Le altre righe sono invariate rispetto a v1. |
| Nessuna proposta di attivazione market data a pagamento (viola D-1) | OK | Cap.54 r361 e Cap.55 r373 mantengono il vincolo D-1 sui market data Eurex/CME extra; DAPI base 20 EUR/mese qualificato come costo strutturale del runtime, non market data a pagamento ai sensi di D-1. Distinzione gia' presente in v1 e non riaperta. |

---

## Secondo giro ostile - verifica assenza di problemi nuovi

Riletto integralmente il capitolo cercando:
- assunzioni implicite non dichiarate
- invarianti violate silenziosamente
- parametri che sembrano definiti ma non lo sono
- comportamenti del GA che il testo implica ma non formalizza

Nessuno dei suddetti problemi e' emerso. In particolare:

1. **State machine post-22:00 CET (B-1).** La rework dichiara persistenza dello
   stato segnale su disco e ripresa al boot del giorno successivo. Coerente
   con Parte II Cap.7 r126 sul dominio del counter Delta_t_cromosoma fino a
   1680 minuti. Il replay bit-exact e' garantito perche' lo stato persistito
   e' ricaricato identicamente in ogni run.

2. **Forward-fill su mid BOOK_5 in regime realtime (B-3).** La regola
   O=H=L=C=(bid1_price_{t-1}+ask1_price_{t-1})/2 per le barre sintetiche FIB
   realtime usa il mid level-1 dell'ultima barra reale (non l'ultimo Close
   come nel training Portara). E' una scelta coerente con il fatto che il
   gateway non emette PRICE/last per i futures FIB. La rappresentazione
   O=H=L=C=mid e' simmetrica al forward-fill di Parte 8 Cap.40 (forward-fill
   su Close_{t-1}): nessuno introduce salti, entrambi mantengono volatilita'
   nulla sulla barra sintetica. Coerente con l'esclusione dalle feature di
   volatilita' di Cap.49 r176. **Non e' bug**.

3. **L_warmup=30 congelato (NB-4) coerente con riavvio mezzanotte Darwin
   (Gap-3).** Il riavvio mezzanotte e' gestito dal recovery di Cap.50 con
   RUNTIME_GAP_START/END e re-pull CANDLERANGE post-riconnessione. Il warm-up
   L_warmup=30 non riparte da zero ogni mezzanotte: e' una finestra storica
   lookback al boot del primo giorno di sessione dopo downtime > 1 giorno.
   Per il riavvio mezzanotte normale, il re-pull copre il gap di pochi minuti
   (Cap.50 punto 6). Coerente, nessuna contraddizione.

4. **Marker CONTRACT_SWITCH (NB-2) e dominio temporale Delta_t_cromosoma
   (B-1).** Uno scenario hostile potenziale e' "segnale FIB6F active alla
   chiusura 2026-06-18, terza venerdi 2026-06-19 mattina la pipeline switcha
   a FIB6I". Il counter Delta_t_cromosoma secondo B-1 deve scavalcare la
   notte. La rework non descrive esplicitamente cosa succede al segnale
   ereditato dal front in scadenza quando il ticker concreto cambia.
   Tuttavia: (i) il counter Delta_t_cromosoma opera sulla serie virtuale
   ratio-adjusted (esplicito in Cap.47 r105); (ii) Parte 8 Cap.38 e Cap.39
   vincolano il prezzo virtuale a propagare attraverso il roll. Quindi il
   segnale e' valutato sui prezzi della serie virtuale, non sul ticker
   concreto; la state machine non si rompe per il cambio di ticker. **Non
   e' bug**, ma l'interazione tra D-9-NB2 (boot switch) e B-1 (counter
   scavalca notte) potrebbe meritare un riferimento incrociato esplicito. Il
   finding NON sale a NB perche' (a) Cap.47 r105 gia' menziona "lo stato
   condizionato non e' interrotto dal cambio di ticker concreto, perche'
   opera sulla serie virtuale continua" e (b) impatta solo lo scenario
   specifico di scadenza con segnale gia' attivo, raro nella prassi
   (l'evento di scadenza dopo le 09:00 CET e' marginalmente esposto).

5. **Conservazione delle sottoscrizioni FIB fuori sessione (Cap.52 r288).**
   "UNSUB delle sottoscrizioni realtime sui simboli cash europei (le
   sottoscrizioni FIB possono restare per audit ma non sono valutate dal
   bundle fuori sessione)". L'asimmetria UNSUB cash / mantieni FIB e' una
   scelta operativa non motivata esplicitamente, ma non ha impatto sul GA
   perche' il bundle non e' valutato fuori sessione. **Non e' bug**.

6. **Tabella decisioni D-9 - D-9-11 e D-9-NB4 sovrapposti su L_warmup=30.**
   D-9-11 ora include "L_warmup=30 giorni di trading congelato" nella sua
   sintesi, ed esiste anche una D-9-NB4 separata dedicata esplicitamente a
   L_warmup=30. Le due voci non si contraddicono; D-9-NB4 e' piu' focalizzata
   e cita la nuova decisione del supervisore (Opzione A NB-4). La
   sovrapposizione testuale non ha impatto sul comportamento del GA. **Non
   e' bug**, classificato come osservazione minore (vedi sotto).

7. **Marker CONTRACT_SWITCH (NB-2) incluso nella tipologia evento Cap.54
   r339.** Verificato: il paragrafo Cap.54 r339 elenca esplicitamente
   CONTRACT_SWITCH nel dominio degli event_type loggati. Coerenza tra Cap.47
   r103 e Cap.54 r339 confermata. **Nessun problema**.

8. **B-2 sample CSV r121-122 confronto con tick FIB 5pt.** Il sample
   FIB6F,1M,2026-06-15 10:35:00 ha Open=45170, High=45175, Low=45165,
   Close=45170 - tutti multipli di 5pt, coerenti con tick FIB di Parte 8
   Cap.41 (esplicitato in Cap.48 r125). **Nessun problema**.

---

## Problemi bloccanti (causano FAIL)

Nessuno.

---

## Problemi non bloccanti (causano CONDITIONAL)

Nessuno.

---

## Osservazioni minori

### OM-v2-1 - Tabella decisioni D-9 sovrappone L_warmup=30 tra D-9-11 e D-9-NB4

In Cap.56 la voce D-9-11 nella colonna "Decisione" ora riporta "Warm-up stati
condizionali via DAPI con L_warmup=30 giorni di trading congelato; restart
dopo downtime > 100 giorni richiede intervento supervisore (stato
`RUNTIME_STALE_RESTART`)..." mentre D-9-NB4 isola la stessa decisione
("L_warmup = 30 giorni di trading IDEM congelato in Parte 9"). Le due voci
non si contraddicono ma sono ridondanti.

Classificazione: NEUTRO. Non impatta il comportamento del GA, non introduce
ambiguita' operativa. Il Developer ha mantenuto entrambe per chiarezza del
tracking dei finding NB. Lasciare cosi'.

### OM-v2-2 - Citazione "Cap.49 r146" residua nella Nota normativa di Cap.47

In Cap.47 r73 (Nota normativa sulla differenza di schema futures vs cash) il
testo cita "Cap.49 r146" come riga della regola di derivazione bar_synthetic
per il FIB futures. Nel testo di v2 la regola normativa e' espressa nella
tabella Cap.49 alla riga corrispondente al campo `bar_synthetic` (riga 164
sulla numerazione attuale del file) + paragrafo r166-170; non c'e' piu' una
"r146" canonica. Il riferimento "r146" e' un residuo lessicale della v1 che
non fa pero' alcun danno semantico perche' il lettore segue il capitolo
("Cap.49") e trova facilmente la regola.

Classificazione: NEUTRO. Cosmetico. Non e' un BUG REALE perche' non altera
ne' la regola operativa ne' la comprensione del GA. Da non mandare a
Development per default CLAUDE.md.

---

## Citazioni problematiche dal testo

Nessuna. Tutti i passaggi citati nelle "problemi bloccanti" della Review v1
sono stati riformulati correttamente nella v2.

---

## Classificazione per il supervisore

| # | Problema | Classificazione | Mandare a Development? |
|---|----------|-----------------|------------------------|
| OM-v2-1 | Sovrapposizione D-9-11 e D-9-NB4 su L_warmup=30 in tabella Cap.56 | NEUTRO | NO - ridondanza testuale che non altera il GA |
| OM-v2-2 | Citazione "Cap.49 r146" residua in Cap.47 r73 (Nota normativa) | NEUTRO | NO - riferimento incrociato impreciso ma non semanticamente fuorviante |

Nessun nuovo BUG REALE, MIGLIORA PERFORMANCE o RISCHIO PEGGIORAMENTO emerso
nel secondo giro ostile.

---

## Sintesi

La rework v2 chiude **tutti gli 11 finding ratificati** (7 BUG REALI B-1..B-7
+ 4 MIGLIORA PERFORMANCE Opzione A NB-1..NB-4) in modo chirurgico e fedele
alle istruzioni del punto di controllo supervisore. Nessuna formulazione vaga,
nessuna ambiguita' operativa, nessuna ricaduta sulla matematica del GA, sulla
state machine del segnale, sul cromosoma o sul replay deterministico bit-exact.

I criteri PASS che in v1 erano OK restano OK senza regressioni. I criteri PASS
che in v1 erano FAIL/PARZIALE ora sono OK. La tabella decisioni Cap.56 e' stata
correttamente estesa con D-9-NB2, D-9-NB3, D-9-NB4. La numerazione capitoli e
la scaletta sono invariate. Nessuno sconfinamento in CAP-DATA-03 (la dipendenza
circolare di B-6 e' eliminata: il caso > 100gg e' rinviato esplicitamente, non
normato).

Le due osservazioni minori (OM-v2-1, OM-v2-2) sono cosmetiche e non impattano
il comportamento del GA, il ranking dei cromosomi, la conversione
signal-to-trade o la correttezza matematica. Default CLAUDE.md: NEUTRO non
va a Development.

**Verdetto: PASS**. La Parte 9 e' pronta per la chiusura sessione PASS
(7 condizioni dell'Orchestratore) e per la propagazione di eventuali nuovi
M-promemoria al CARRYOVER per CAP-DATA-03 (continuita' tape, recupero gap,
riconciliazione canonica giornaliera, storicizzazione strutturata,
implementazione lookup completa codici mese Directa-IDEM, abilitazione FDAX
standard, vendor cross-index pluriennale PHASE-2).
