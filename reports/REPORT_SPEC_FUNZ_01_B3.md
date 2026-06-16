# REPORT — SPEC-FUNZ-01-B3 (State-machine e lifecycle del segnale, blocco 3/8)

> Conferma letture obbligatorie (ordine prescritto, prima di scrivere): (1) tasks/METODO.md (RM-1..RM-4 + RACC-METODO-2) letto; (2) .claude/BASE_COMUNE.md (ciclo, sede CLI per la spec, onesta claim verso evidenza) letto; (3) .claude/agents/spec_developer.md (il mio ruolo) letto; (4) tasks/ACTIVE_TASK.md (task card rev-B1 di SPEC-FUNZ-01-B3) letto ed eseguito alla lettera. Fonte di contenuto: docs/methodology_v2/CAP_02_parte_II.md, limitatamente a Cap.7 (7.1-7.6) e Cap.11 (11.1-11.5) piu preambolo (:1-9) e Q-05 (:7).
>
> Conferma di lavoro in cieco: ho costruito i requisiti di B3 esclusivamente dai capitoli pertinenti del CAP-fonte e dalla task card. NON ho aperto, letto, citato o parafrasato SPEC_FUNZ_01.md (v2), alcun _v1_storico, alcun file di chunking (PROPOSTA_SUDDIVISIONE_SPEC), ne SPEC_FUNZ_01_B1.md/B2.md/altri B-N.md. Gli ID requisito sono auto-assegnati da zero (schema B3-R / B3-CN / B3-NFR). Non ho tentato il confronto-copertura con la v2 (compito esclusivo del Reviewer).

---

## 1. Cosa e stato prodotto

docs/spec_funzionale/SPEC_FUNZ_01_B3.md: 47 requisiti B3-R (lifecycle: stati, transizioni, eventi, timer, contratto submacchina), 12 requisiti B3-CN (invarianti/strutturali), 3 requisiti B3-NFR (contratto di osservazione del primo pivot). Totale 62 requisiti atomici, in 8 sezioni:

1. Stati e semantica: 1 non-terminale piu 6 terminali (B3-R-01/02); active (B3-R-03/04); 6 terminali con semantica e condizione di ingresso, un blocco per stato (B3-R-05..16, B3-CN-01); causalita di expired come campo (B3-R-14); terminalita assoluta e NB-9 (B3-CN-02/03).
2. Transizioni e precedenza: 7 transizioni creazione verso active e active verso i 6 terminali (B3-R-17..23); chiusura insieme (B3-CN-04); precedenza eventi a parita di timestamp (B3-CN-05).
3. Raw touch come evento: definizione (B3-R-24/25); trigger_event (B3-R-26); sempre eseguibile (B3-R-27); evento-non-stato (B3-CN-06); motore non osserva il fill (B3-R-28); tre edge case NB-8 a/b/c (B3-R-29/30/31).
4. Semantica dei timer: post-trigger decorrenza da t_exec, calendario di trading, counter 8:00-22:00 con arresto, scadenza verso expired/posttrigger_timeout (B3-R-32..35); pre-trigger decorrenza da timestamp_emission, counter di trading, scadenza verso expired/pretrigger_timeout, razionale (B3-R-36..39).
5. Contratto di osservazione pivot M-1: osservazione barre da 8:00 CET (B3-NFR-01); disponibilita entro N_pivot, valore verso Parte V (B3-NFR-02); cadenza barra chiusa, no tick intra-bar (B3-NFR-03).
6. Position lifecycle submacchina: separazione (B3-CN-07, B3-R-40); OUT/IN-scope (B3-R-41/42); struttura (B3-R-43..46); target_2 come evento (B3-CN-08); indipendenza-di-stato (B3-CN-09) e separazione-dei-log (B3-CN-12); impatto GA (B3-CN-10, B3-R-47).
7. Invarianti di modellazione: riepilogo piu B3-CN-11 (|A(t)|<=1 sui soli attivi).
8. Matrice di tracciabilita piu nota di rinvio (AC-G10).

reports/REPORT_SPEC_FUNZ_01_B3.md: questo file.

## 2. Ipotesi di partenza

- Lavorato in cieco dai soli Cap.7 (7.1-7.6) e Cap.11 (11.1-11.5) di CAP_02_parte_II.md, piu preambolo (:1-9) e Q-05 (:7).
- I fatti del par.2 della card e i pin-riga sono autoritativi (non ri-verificati come fatti); ho pero ri-verificato token-per-token i numeri di riga con Read prima di citarli (AC-G7). I puntatori del par.2 hanno risolto esatti; nessuna correzione di puntatore necessaria.
- CAP_02_parte_II.md chiuso PASS a1625df (tasks/STATO_CORRENTE.md:10); frozen (G-09): sola lettura, non modificato.

## 3. Decisioni rilevanti

- Atomicita N1: concern impacchettati spezzati. Es. target_1_hit reso da successo (B3-R-05), condizione di ingresso (B3-R-06), chiusura del contratto (B3-R-07), terminalita (B3-CN-02), NB-9 (B3-CN-03). Ogni stato terminale ha condizione di ingresso separata; ogni transizione e un requisito; ogni edge case NB-8 e un requisito.
- Famiglie ID: B3-R funzionale/lifecycle; B3-CN invarianti strutturali; B3-NFR contratto di osservazione pivot M-1 (interfaccia/QoS), come da card par.4.2.
- Categoria valore di sistema/validazione (F-2): applicata SOLO ai requisiti di puro determinismo/replay senza valore vissuto dall operatore: B3-CN-05 (precedenza), B3-R-14 (causa expired come campo per i 6 stati), B3-R-39 (razionale executable_rate), B3-CN-11 (|A(t)|<=1 come premessa). Per gli invarianti con valore-operatore diretto (terminalita target_1_hit, raw touch sempre eseguibile, timer pre-trigger) ho mantenuto il valore-operatore.
- Doppio luogo trigger_event (evento-B3 vs notifica-B4): consolidato come evento del lifecycle (B3-R-24..28, B3-CN-06) con nota di confine che rinvia a B4 pubblicazione Telegram/contratto notifica/latenza/anti-duplicato. Nessun requisito B3 tocca la pubblicazione.
- Seam revoked/Cap.6.3: la transizione active verso revoked traccia a Cap.7.2 (:127, verificato token-per-token; riga della tabella 7.2 con active / revoked / Il motore emette un nuovo signal_id sostituzione Cap.6.3). Il significato di superseduto e citato come premessa da Cap.6.3 (:77) IN PIU, non in sostituzione; NON ho ri-consolidato |A(t)|<=1 come proprieta del payload (resta B2; in B3 richiamato solo per la conseguenza sul lifecycle, B3-CN-11). Pin :127 risolto pulito: nessun [B-N PROVVISORIO].
- Carve-out numeri (F-5): finestra 8:00-22:00 CET e cap 2 giorni ammessi come calendario/semantica su cui i counter avanzano (B3-R-34/37, citati come dato). Esclusi i valori-soglia congelati: N_pivot non-numerico (B3-NFR-02 verso Parte V); valori dei domini dei timer non introdotti (domini come campi = B2).
- Rinvii deliberati: schema-payload/immutabilita/domini verso B2; emissione e filtro 80pt come regola verso B4; pubblicazione Telegram verso B4; formato log e determinismo replay verso B5/Cap.10; sessione operativa come requisito (M-GOV-1) verso B5; algoritmo pivot, condizioni strutturali di invalidazione, fill virtuale verso Parte III/IV; valori congelati verso Parte V. Annotati nella nota di rinvio par.8.2.
- Cautela RM-1: nessuna dichiarazione di prima istanza; ogni requisito e un richiamo a un fatto gia asserito nel CAP chiuso con [DOC-INTERNO ...]. Nessun blocco RM-1 a 4 righe necessario.
- Micro-pass OM-1 (finding #1, MIGLIORA PERFORMANCE, decisione AC): l originale B3-CN-09 impacchettava due proposizioni distinte (indipendenza-di-stato della submacchina + separazione-dei-log) sotto un solo ID, in violazione di N1 (AC-G1). Spezzato in due requisiti atomici, entrambi tracciati a :393 (la riga del CAP afferma entrambe insieme, ri-verificata token-per-token): B3-CN-09 (mantiene l ID) = sola indipendenza-di-stato; B3-CN-12 (prossimo ID libero, NESSUNA rinumerazione a cascata) = separazione-dei-log referenziati dal signal_id. Valore operativo per entrambi (come l originale). Aggiornati di conseguenza: Sezione 7 (bullet Indipendenza della submacchina, rimando a B3-CN-12) e matrice par.8.1 (riga B3-CN-09 ridotta alla sola (a); aggiunta riga B3-CN-12). Nessun altro requisito toccato; perimetro e altri finding invariati; CAP frozen (G-09) solo letto.

## 4. Misura prima/dopo

Greenfield di consolidamento (nessun prima lavorando in cieco). Copertura del perimetro-fonte:

- Cap.7.1 (stati e semantica): B3-R-01..16, B3-CN-01/02/03.
- Cap.7.2 (transizioni piu precedenza): B3-R-17..23, B3-CN-04/05.
- Cap.7.3 (raw touch piu NB-8): B3-R-24..31, B3-CN-06.
- Cap.7.4/7.5 (timer): B3-R-32..39.
- Cap.7.6 (pivot M-1): B3-NFR-01/02/03.
- Cap.11.1..11.5 (submacchina): B3-CN-07/08/09/12/10, B3-R-40..47, B3-CN-11.

DOPO: 62 requisiti tracciati (47 R piu 12 CN piu 3 NFR), ciascuno con citazione CAP_02_parte_II.md:riga e valore dichiarato.

## 5. Domande aperte / Blocchi

Nessun blocco aperto. Il seam noto (riga Cap.7.2 della transizione active verso revoked che avrebbe potuto rimandare a Cap.6.3) NON si e verificato: la riga :127 contiene la transizione come tale; AC-G2 soddisfatto senza sconfinare in Cap.6 e senza [B-N PROVVISORIO]. Nessun requisito a valle di un blocco; documento privo di marcatori di contaminazione. Tutti i puntatori-riga del par.2 hanno risolto esatti.

## 6. Criterio di rollback

B3 e un file autonomo (docs/spec_funzionale/SPEC_FUNZ_01_B3.md) piu report. Annullare B3 = rimuovere i due file (e la riga-marcatore di chiusura se gia scritta): nessun altro blocco li importa (assemblaggio = task dedicato post-B8), nessun CAP toccato (freeze G-09), 00_indice.md non modificato. Rollback senza impatto su B1/B2 ne blocchi futuri.

---

## Tabella di verifica AC (AC-G1..AC-G11)

| AC | Stato | Evidenza |
|----|-------|----------|
| AC-G1 Atomicita N1 | OK | target_1_hit verso B3-R-05/06/07 piu B3-CN-02/03; stati terminali con condizione separata (B3-R-08/09/10/11/13); transizioni una per ID (B3-R-17..23); edge case NB-8 separati (B3-R-29/30/31); contratto submacchina :393 spezzato in indipendenza-di-stato (B3-CN-09) + separazione-dei-log (B3-CN-12) — micro-pass OM-1. |
| AC-G2 Tracciabilita | OK | Ogni requisito porta [DOC-INTERNO CAP_02_parte_II.md:riga]; matrice par.8.1. Seam active verso revoked: B3-R-23 a :127 piu premessa :77 (in piu). |
| AC-G3 Valore operativo | OK | Ogni requisito dichiara Valore operativo (o di sistema/validazione per F-2). |
| AC-G4 Divieto prima istanza RM-1 | OK | Nessuna dichiarazione di prima istanza; richiami a fatti del CAP chiuso. |
| AC-G5 Etichette RM-3 | OK | Nessun requisito poggia su fonte esterna; calendario 8:00-22:00/cap 2 giorni citato come dato dei CAP chiusi (B3-R-34/37). |
| AC-G6 Grafia canonica | OK | Solo [DOC-INTERNO ...]; nessuna grafia storica. |
| AC-G7 Floor citazioni 100% | OK | Tutte le righe ri-verificate token-per-token con Read (:7,:77,:95,:97,:99,:101,:103,:105,:107,:109,:111,:113,:121-:127,:129,:131,:135,:137,:139,:141,:145,:147,:149,:155,:157,:159,:163,:165,:167,:171,:173,:175,:349,:351,:352,:362,:368,:370,:372,:373,:374,:375,:381,:383,:385-:389,:391,:393,:397,:399). |
| AC-G8 Cecita preservata | OK | Nessun ID importato (schema B3 da zero); nessuna frase copiata da v2/B1/B2/chunking (non aperti). |
| AC-G9 Scope tutto e solo | OK | Copre Cap.7.1-7.6 piu Cap.11.1-11.5; nessuno sconfinamento in B2/B4/B5/Parte III-IV (note di confine par.3.1, 3.2, 4, 5, 8.2). |
| AC-G10 Matrice piu nota di rinvio | OK | par.8.1 (matrice) piu par.8.2 (nota di rinvio). |
| AC-G11 Invarianti evidenziati | OK | B3-CN: terminalita (02), NB-9 (03), chiusura transizioni (04), precedenza (05), evento-vs-stato (06/08), indipendenza-di-stato submacchina (09), separazione-dei-log submacchina (12), space search non esteso (10), |A(t)|<=1 (11). Sezione 7 li riepiloga. |

---

## Applicazione RM-1 a me stesso

- Tutti i puntatori-riga del par.2 hanno risolto esatti — PROVE: Read di CAP_02_parte_II.md righe 1-10, 70-189, 340-409, confronto token-per-token. ALTERNATIVE ESCLUSE: che una riga puntasse a contenuto diverso (escluso per ispezione diretta). ALTERNATIVE NON ESCLUSE: nessuna; non ho riletto le righe 200-339, ma B3 non vi traccia.
- Seam :127 risolto pulito — PROVE: riga 127 = riga della tabella 7.2 con active / revoked / Il motore emette un nuovo signal_id (sostituzione, Cap.6.3). ALTERNATIVE NON ESCLUSE: nessuna.
- 62 requisiti, 47 R piu 12 CN piu 3 NFR — PROVE: conteggio diretto degli ID nel documento (R-01..R-47; CN-01..CN-12; NFR-01..NFR-03). Nota: CN-12 e l ID aggiunto dal micro-pass OM-1 (split di CN-09); la sequenza CN va 01..12 senza buchi.
- Split B3-CN-09 verso B3-CN-09 + B3-CN-12, entrambi a :393 — PROVE: Read di CAP_02_parte_II.md:393 (token-per-token) = la riga afferma sia la non-modifica dello stato del segnale ("la submacchina non modifica lo stato del segnale in nessuna circostanza. Il segnale e terminato in target_1_hit prima ancora...") sia la separazione dei log ("I log della submacchina sono separati ... referenziato dal signal_id"). Entrambe le proposizioni tracciano legittimamente a :393. ALTERNATIVE ESCLUSE: che (b) tracciasse a un altra riga (esclusa: :393 contiene esplicitamente la frase sui log separati). ALTERNATIVE NON ESCLUSE: nessuna.
- Lavoro in cieco — PROVE: nessuna Read su SPEC_FUNZ_01.md / B1 / B2 / chunking / _v1_storico; le uniche Read di contenuto sono su CAP_02_parte_II.md.
- Nessuna grafia storica nel documento — PROVE: nel documento solo [DOC-INTERNO ...].
