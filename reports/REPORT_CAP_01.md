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
- **M-3 (Review v4)**: trattamento delle barre 1-min durante l'asta 8:00-9:00 nel pre-processing del feed storico — rischio di pivot spurî da neutralizzare in Parte II/Appendice D
- **M-4 (Review v4)**: documentare il tasso di rimpiazzo NSGA-II atteso che giustifica la baseline 12.800-25.600 min — da formalizzare in Parte V

#### Domande aperte per il Planner
Nessuna. Q-01, Q-02, Q-03, Q-04 tutte chiuse dal supervisore.

#### Criterio di rollback
1. Se in fase di valutazione OOS della prima campagna il movimento strutturale calcolato secondo la nuova definizione produce un target di confronto sistematicamente irraggiungibile (es. nessun bundle frozen riesce a catturare il 70% in più del 10% delle sessioni di test), si torna alla calibrazione della soglia 70% con il supervisore.
2. Se in Parte V vengono congelati parametri NSGA-II diversi da 128/150/B=2000, Cap.4 di questa Parte I va aggiornato — l'aggiornamento è puntuale, non richiede riscrittura.
3. Se $b_{min} = 5$ punti produce in training un eccesso di cromosomi con banda al minimo che non superano l'executable rate, il valore va rivisto in Parte V con il supervisore.
