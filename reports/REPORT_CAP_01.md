### REPORT SUPERVISORE — CAP-01
**Task**: Parte I del documento metodologico v2 — Ambito operativo e vincoli operatore
**Stato**: COMPLETATO — Review v4 verdetto PASS (dopo quattro cicli Planner → Development → Review, una rettifica supervisore sugli orari, e adozione Opzione A su Cap.4)

#### Cosa è stato prodotto
- `docs/methodology_v2/CAP_01_parte_I.md` — Parte I, 5 capitoli, versione v3 post-review-v2
- `reviews/REVIEW_CAP_01.md` — audit ostile (verdetto v2: CONDITIONAL; verdetto v3 atteso: PASS)
- `tasks/QUESTIONS.md` — Q-01..Q-04 tutte chiuse con decisione del supervisore

#### Ipotesi di partenza
La Parte I definisce i vincoli operativi e le metriche di successo che il GA ottimizza. Una definizione imprecisa di questi vincoli produce un GA che ottimizza il problema sbagliato (BUG REALI sul target operativo) o ottimizza cromosomi degeneri (parametri liberi senza dominio). I tre cicli di pipeline Planner → Development → Review hanno esposto progressivamente difetti che la prima stesura non aveva intercettato.

#### Decisioni rilevanti prese durante lo sviluppo

**Ciclo 1 (Development v1)**: scrittura iniziale dei 5 capitoli, con sessione 9:00-22:00 (post-CLAUDE.md aggiornata; successivamente rettificata a 8:00-22:00 dal supervisore), cross-index inserito, target 500pt/70%, struttura payload.

**Ciclo 2 (Review v1 → Development v2)**: la review ostile ha identificato 2 BUG REALI bloccanti (B-1 escursione intraday come max−min anziché movimento strutturale; B-2 trade range senza vincolo 80pt) e 4 non bloccanti. Supervisore ha approvato 6 fix:
- B-1: movimento strutturale = somma moduli swing dei pivot, con esempio numerico
- B-2: ≥80pt sul rettangolo trade range, pronome "di questa ampiezza" chiarito
- NB-3: target 1 + target 2 entrambi obbligatori; metriche lifecycle sdoppiate
- NB-4: banda ±40 come parametro libero del GA con tetto, non default
- NB-5: stima cloud corretta (13-27h, 4.5-9 USD)
- NB-2: soglia 500pt attribuita esplicitamente al supervisore (non bug)
Q-01 chiusa = perimetro 8:00-22:00 (rettifica supervisore).

**Ciclo 3 (Review v2 → Development v3)**: la review ostile sulla v2 ha rilevato 4 nuovi BUG REALI (3 generati dai fix v2, 1 pre-esistente non visto) + 3 osservazioni NEUTRO. Supervisore ha deciso di trattarle TUTTE in Parte I:
- N-1: il carico training era stimato su 520 min/sessione (regolare IDEM), inconsistente col perimetro 8:00-22:00. Ricalcolato su 840 min/sessione: 1.050.000 osservazioni, 15-29 giorni single-thread (21.000-41.500 min), 22-43 ore su 16 vCPU, 7-15 USD per run, 45-75 EUR di budget retraining. Rimossa la moltiplicazione misleading 128×150×4-8 min (NSGA-II riusa l'archivio dei non dominati; il numero di valutazioni effettive dipende dal tasso di rimpiazzo)
- N-2: banda ingresso ha ora dominio $b \in [b_{min}, 40]$ punti FIB; $b_{min}$ provvisorio = 5 punti (congelato in Parte V)
- N-3: vincolo geometrico esplicito $d_{stop} > b$ — cromosomi che lo violano sono dichiarati non validi
- N-4: missed target rate riferita esplicitamente al target 1
- N-5 (Q-02): movimento strutturale ancorato al primo minimo o primo massimo post-apertura, non al primo segnale → target esiste in ogni sessione
- N-6 (Q-03): nota provvisorietà sui parametri 128/150/B=2000 inserita in Cap.4
- N-7 (Q-04): cap multiday fissato a 2 giorni di trading; il GA ottimizza il timing di chiusura entro il tetto

#### Misura prima/dopo (ciclo 1 → ciclo 3 finale)
| Metrica | v1 | v3 finale | Delta |
|---------|----|-----------|-------|
| Definizione target operativo | max−min sessione (errato) | movimento strutturale dal primo min/max post-apertura | Definizione matematica corretta + edge case sessioni senza segnali risolto |
| Trade range | "ampiezza ben definita" | ≥ 80 punti FIB | Filtro emissione chiuso |
| Struttura target nel payload | "uno o più target" | target 1 + target 2 obbligatori | Payload deterministico per il GA |
| Banda ingresso | "±40 tipica" (ambigua) | $b \in [5, 40]$ punti, parametro libero GA | Dominio dichiarato, no cromosomi degeneri |
| Vincolo geometrico stop/banda | non dichiarato | $d_{stop} > b$ obbligatorio | Esclude segnali stoppati a fill |
| Osservazioni training | 650.000 (520 min/sessione) | 1.050.000 (840 min/sessione) | Coerente col perimetro 8:00-22:00 |
| Tempo training single-thread | 9-18 giorni | 15-29 giorni | +62% (atteso, scaling lineare dati ×1.615) |
| Costo cloud per run | 4.5-9 USD | 7-15 USD | +67% |
| Budget retraining | 25-40 EUR | 45-75 EUR | +80% |
| Cap validità segnale | "multiday" senza tetto | ≤ 2 giorni di trading | Tetto esplicito, GA vincolato |
| Missed target rate | "il target strutturale" (ambiguo) | target 1 (esplicito) | Metrica lifecycle deterministica |
| Parametri GA in Parte I | citati senza disclaimer | citati con nota provvisorietà | Coerenza con out-of-scope ACTIVE_TASK |

#### Promemoria per Parti successive (segnalati da Review v4, non rework di CAP-01)
- **M-1 (carryover da v2)**: identificazione real-time del primo pivot strutturale post-apertura — algoritmo da chiarire in Parte II
- **M-3 (Review v4) — RITIRATO**: il promemoria assumeva la presenza di una fase d'asta 8:00-9:00 con barre theoretical opening price. Chiarito dal supervisore che il FIB negozia in modo continuo 8:00-22:00 senza fase d'asta separata. Nessun trattamento speciale richiesto.
- **M-4 (Review v4)**: documentare il tasso di rimpiazzo NSGA-II atteso che giustifica la baseline 12.800-25.600 min — da formalizzare in Parte V

#### Domande aperte per il Planner
Nessuna. Q-01, Q-02, Q-03, Q-04 tutte chiuse dal supervisore.

#### Criterio di rollback
1. Se in fase di valutazione OOS della prima campagna il movimento strutturale calcolato secondo la nuova definizione produce un target di confronto sistematicamente irraggiungibile (es. nessun bundle frozen riesce a catturare il 70% in più del 10% delle sessioni di test), si torna alla calibrazione della soglia 70% con il supervisore.
2. Se in Parte V vengono congelati parametri NSGA-II diversi da 128/150/B=2000, Cap.4 di questa Parte I va aggiornato — l'aggiornamento è puntuale, non richiede riscrittura.
3. Se $b_{min} = 5$ punti produce in training un eccesso di cromosomi con banda al minimo che non superano l'executable rate, il valore va rivisto in Parte V con il supervisore.

---

## Iterazione 2 — Chiarificazione semantica retrospettiva (post-PASS Review v4)

**Origine**: chiarificazione esplicita del supervisore durante la lavorazione di CAP-02 Parte II, in risposta a due nodi metodologici emersi nel ciclo Development → Review v1 → Review v2 di CAP-02:
1. Il cap di validità di 2 giorni di trading decorre dall'esecuzione (raw touch), non dall'emissione del segnale.
2. Le "guardie di esecuzione al raw touch" sono state ristrutturate come "condizioni di emissione del segnale" (pre-emissione, non post). Una volta emesso, il raw touch è sempre eseguibile. La guardia di spread è stata eliminata in quanto non addestrabile sullo storico FIB 1-min Portara/CQG (lo spread richiederebbe storico di book non disponibile).

**Modifiche apportate a CAP-01**:

| Riga | Cosa cambia | Motivazione |
|------|-------------|-------------|
| 13 (Cap.1) | "Il limite massimo di estensione della validità del segnale è fissato a 2 giorni di trading dall'emissione" → "...del segnale eseguito è fissato a 2 giorni di trading decorrenti dall'esecuzione, intesa come il raw touch della entry zone". Aggiunta della menzione del timer pre-esecuzione (mix punti×tempo dipendente dal regime, formalizzato in Parte II Cap.7). | La validità di 2gg si applica al segnale eseguito (post-trigger), non al segnale in attesa di trigger. Il caso "segnale emesso e mai eseguito" è governato da un timer distinto pre-esecuzione. |
| 77 (Cap.5) | "executable rate, frazione di segnali emessi che raggiungono il raw touch... superando le guardie di esecuzione" → "...che raggiungono il raw touch... entro il timer di attesa pre-esecuzione (il raw touch è sempre eseguibile...; le condizioni di mercato... sono valutate dal motore prima dell'emissione, non dopo)". | Coerenza con la nuova architettura di Parte II v2: il raw touch è sempre eseguibile, le condizioni di emissione sono pre-emissione, non filtri post-trigger. |

**Perché non è una rottura del PASS Review v4**: il PASS riguardava la coerenza interna di CAP-01 sotto la lettura più ampia "validità del segnale" e "guardie di esecuzione" come concetto generico. La nuova lettura è un raffinamento semantico, non una contraddizione: nessun valore numerico, nessuna struttura argomentativa di CAP-01 viene invalidata; viene aggiunta precisione operativa che CAP-01 non aveva motivo di esplicitare prima della formalizzazione di Parte II. Il filtro 80pt, il vincolo $b \in [5, 40]$, il vincolo $d_{stop} > b$, le metriche DSR/PBO/CVaR, il compute budget, la sessione 8:00-22:00 CET — tutti restano invariati.

**Modalità di esecuzione**: la patch è eseguita direttamente da Development senza nuovo passaggio in Review, su autorizzazione esplicita del supervisore. La motivazione è che la modifica recepisce decisioni del supervisore già prese (cap 2gg post-trigger, raw touch sempre eseguibile, spread eliminata), non introduce contenuto interpretativo nuovo da auditare.

**Misura prima/dopo**:

| Metrica | Prima dell'Iterazione 2 | Dopo l'Iterazione 2 | Delta |
|---------|-------------------------|----------------------|-------|
| Decorrenza cap 2gg | dall'emissione (riga 13) | dall'esecuzione/raw touch | semantica corretta del cap di validità post-trigger |
| Trattamento segnale in attesa di raw touch | non distinto, assorbito nel cap 2gg | timer dedicato pre-esecuzione (mix punti×tempo, parametro libero del cromosoma) | nuova leva GA esplicitata, coerente con tema "se il segnale non si aggiorna è un problema" |
| Definizione executable_rate | basata sulle "guardie di esecuzione" | basata sul raw touch sempre eseguibile entro timer pre-esecuzione | coerenza con architettura Parte II v2 |
| Numero parametri liberi del cromosoma per filtri di mercato | 4 implicite (guardie) | 3 (volatilità EGARCH, liquidità volume, distanza target_1 in $\sigma$-units) — spread eliminata in quanto non addestrabile | riduzione spazio di ricerca, addestrabilità garantita |

**Criterio di rollback per l'Iterazione 2**:

4. Se in Parte V emerge che il timer pre-esecuzione produce in training un tasso di `pretrigger_timeout` superiore al 60% dei segnali emessi (segnali quasi sempre stantii prima del touch), va rivisto il dominio del parametro o la sua dipendenza dal regime, non l'architettura del cap 2gg post-trigger.
5. Se la patch di riga 77 (executable_rate) genera ambiguità nelle metriche OOS, va aggiornata di nuovo coordinandosi con il calcolo concreto delle metriche in Parte V. La patch attuale è coerente con la struttura del lifecycle dichiarata in Parte II v2.

---

## Iterazione 3 — Patch chirurgica post-PASS CAP-02 v3 (chiusura residui corpus-level)

**Origine**: Review v3 di CAP-02 (commit `e070fa9`) ha emesso PASS con due osservazioni NEUTRO (N-7, N-8) e un promemoria (M-4) riferiti a residui testuali in CAP-01 resi incoerenti dalla decisione Q-05 (Opzione D raffinata: separazione contratto del segnale vs position lifecycle, target_2_hit rimosso dagli stati del segnale, sostituzione delle "guardie di esecuzione" con "condizioni di emissione" pre-emissione). Patch applicata dal Planner come Iterazione 3, prima della partenza di CAP-03, per evitare incoerenza corpus-level.

**Modifiche apportate**:

| Riga (post-patch) | Cosa cambia | Finding chiuso |
|------|-------------|---------|
| 75 (Cap.5) | "modellati invece nelle **guardie di esecuzione** della Parte II" → "modellati invece nelle **condizioni di emissione** della Parte II (Cap.8)" | N-7 / M-4 |
| 77 (Cap.5) | "target 2 hit rate, definita analogamente sul target 2" → riformulata come metrica del position lifecycle (Cap.11 Parte II), non più della state machine del segnale; chiarimento esplicito post-Q-05 | N-8 |

**Perché non è una rottura del PASS Review v4 di CAP-01**: la formulazione originale di CAP-01 era coerente con l'architettura Parte II v1 (guardie post-trigger come filtri al raw touch + target_2_hit come stato terminale). Dopo Q-05 (Opzione D raffinata, decisione supervisore 2026-05-23) l'architettura Parte II è cambiata: la patch riallinea CAP-01 alla nuova architettura senza modificare alcun valore numerico, vincolo strutturale, o filosofia di Parte I. È una correzione di tracciabilità cross-parte, non una modifica di sostanza.

**Misura prima/dopo Iterazione 3**:

| Metrica corpus | Prima | Dopo | Delta |
|----------------|-------|------|-------|
| Coerenza terminologica CAP-01 ↔ CAP-02 v3 | 2 residui ("guardie di esecuzione", "target 2 hit rate") | 0 residui | corpus internamente coerente |
| Finding aperti post-PASS CAP-02 | 2 N + 1 M (su CAP-01) | 0 N + 0 M (chiusi) | rework CAP-01 chiuso |

**Finding chiusi**: N-7, N-8, M-4 (tutti di Review v3 CAP-02). Riferiti a CAP-01 e ora risolti.

**Criterio di rollback Iterazione 3**:
6. Se in Parte V (Cap.24 fitness) o nel position lifecycle (Cap.11 Parte II) emergerà che la metrica `target_2_hit_rate` come "metrica del position lifecycle" non è calcolabile coerentemente con il replay deterministico (Cap.10 Parte II), la formulazione di riga 77 va aggiornata di nuovo. La patch attuale è coerente con la decisione Q-05.
