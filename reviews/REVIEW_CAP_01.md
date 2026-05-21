# Review CAP-01 v4 — Parte I: Ambito operativo e vincoli operatore (quarto giro ostile)

**Verdetto**: PASS

Motivazione sintetica: la correzione del perimetro sessione da 9:00-22:00 a 8:00-22:00 CET è applicata in modo coerente in tutto il documento. L'Opzione A approvata dal supervisore per il Cap.4 (eliminazione della moltiplicazione popolazione × generazioni × tempo per cromosoma come stima esatta e adozione di una "stima empirica totale" giustificata dal riuso dell'archivio NSGA-II dei non dominati) è effettivamente implementata: il prodotto misleading 128 × 150 × t_chromo è scomparso, sostituito da una baseline empirica esplicita (12.800-25.600 min sulla sessione regolare di 520 min) riscalata linearmente al fattore 840/520 ≈ 1,62. Tutta l'aritmetica derivata è verificata internamente coerente. Tutti i fix precedenti accumulati (B-1, B-2, NB-2..NB-5, N-1..N-7) restano applicati. Nessun nuovo problema bloccante introdotto dalle correzioni.

---

## Stato cumulativo di tutti i fix

### Fix v1 → v2 (B-1, B-2, NB-2..NB-5)

| Fix | Tema | Stato v4 | Posizione |
|-----|------|----------|-----------|
| B-1 | Definizione movimento strutturale (somma moduli swing, non range max-min) | OK | Riga 11, esempio numerico 100/150/100/150/100/150 → 50 vs 250 pt mantenuto |
| B-2 | Distinzione $E[R_{net}\|executed]$ da $E[R_{net}\|emitted]$, formula con $2c$ | OK | Righe 71-75 |
| NB-2 | Definizione FIB come MIB IDEM moltiplicatore 5 EUR/pt | OK | Riga 9 |
| NB-3 | 1 contratto FIB con motivazione punto 7 dichiarazione | OK | Riga 25 |
| NB-4 | Punti dichiarazione 1, 7, 8, 9, 10 citati esplicitamente | OK | Cap.1 e Cap.2 |
| NB-5 | DSR e PBO con riferimenti Bailey/Lopez de Prado e CSCV | OK | Riga 81 |

### Fix v2 → v3 (N-1..N-7)

| Fix | Tema | Stato v4 | Note |
|-----|------|----------|------|
| N-1 | Cap.4 ricalcolato sul perimetro corretto della sessione | OK | Ora su 8:00-22:00 (840 min), non più 9:00-22:00 (780 min). Aritmetica interna coerente con Opzione A. |
| N-2 | Cap.2 banda con dominio $b \in [b_{min}, 40]$, $b_{min}=5$ provvisorio | OK | Riga 27 invariata |
| N-3 | Cap.2 vincolo geometrico $d_{stop} > b$ | OK | Riga 29 invariata |
| N-4 | Cap.5 missed target rate riferita esplicitamente a target 1 | OK | Riga 77 invariata |
| N-5 | Cap.1 movimento strutturale ancorato a primo min/max post-apertura | OK | Riga 11. Ancoraggio ora esplicitamente "dopo l'asta di apertura, dalle 9:00 CET in poi". |
| N-6 | Cap.4 nota provvisorietà 128/150/B=2000 | OK | Riga 59 invariata |
| N-7 | Cap.1 cap 2 giorni di trading + GA ottimizza timing entro tetto | OK | Riga 13 invariata |

### Fix v3 → v4

| Fix v4 | Tema | Stato | Verifica |
|--------|------|-------|----------|
| Correzione 8-22 | Sessione FIB da 9:00-22:00 a 8:00-22:00 CET con dettaglio fasi | OK | Riga 9: "asta 8:00-9:00 + regolare 9:00-17:40 + after-hours 17:40-22:00". Coerente in Cap.1 (righe 9, 11) e Cap.4 (righe 57, 59). Nessun residuo "9:00-22:00" nel documento (verifica grep negativa). |
| Opzione A Cap.4 | Eliminata moltiplicazione misleading 128 × 150 × tempo. Stima empirica scalata linearmente con menzione riuso archivio NSGA-II. | OK | Riga 59: "NSGA-II riutilizza l'archivio dei cromosomi non dominati fra generazioni, per cui il numero di valutazioni effettive di backtest in un run completo non coincide con il prodotto popolazione × generazioni ma dipende dal tasso di rimpiazzo della popolazione." Stima totale presentata come "stima empirica totale ricondotta alla baseline... riscalata linearmente al fattore 840/520 ≈ 1,62". |

Esito complessivo: 14 fix presenti, 0 regressioni, 0 nuovi bloccanti.

---

## Verifica aritmetica interna Cap.4 (v4)

| Calcolo | Atteso | Pubblicato | Esito |
|---------|--------|------------|-------|
| Minuti per sessione 8:00-22:00 | 14h × 60 = 840 | 840 | OK |
| Osservazioni 5y: 250 × 840 × 5 | 1.050.000 | 1.050.000 | OK |
| Fattore scaling 840/520 | 1,6154 ≈ 1,62 | 1,62 | OK |
| Tempo per cromosoma scalato: 2 × 1,62 — 8 × 1,62 | 3,24 — 12,96 | 3-13 min | OK |
| Baseline scalata: 12.800 × 1,62 — 25.600 × 1,62 | 20.736 — 41.472 | 21.000 — 41.500 | OK (arrotondamento dichiarato) |
| Giorni single-thread: 21.000/1.440 — 41.500/1.440 | 14,58 — 28,82 | 15 — 29 giorni | OK |
| Ore cloud 16 vCPU: 21.000/16 — 41.500/16 | 1.312,5 min = 21,87h ; 2.593,75 min = 43,23h | ≈ 22 — 43 ore | OK |
| Costo USD: 22 × 0,34 — 43 × 0,34 | 7,48 — 14,62 | 7-15 USD | OK |
| Budget retraining EUR (overhead ~5-6x) | — | 45-75 EUR | OK (range plausibile) |

Tutti i passaggi numerici sono internamente coerenti. Nessuna sottostima o sovrastima di fattore residua.

---

## Verifica residui 8:00-22:00 vs 9:00-22:00

Grep su "9:00-22:00" → 0 match. Grep su "8:00" → match solo in righe coerenti (9, 23 dichiarazione operatore — invariata, 43 nessuno).

Verifiche di coerenza:
- Riga 9: definizione perimetro 8:00-22:00 con tre fasi (asta, regolare, after-hours).
- Riga 11: ancoraggio del primo pivot strutturale "post-apertura, dopo l'asta di apertura, dalle 9:00 CET in poi". Distinzione corretta tra "post-apertura" (sessione regolare) e perimetro complessivo. Non c'è leakage: l'esclusione dell'asta dal calcolo del primo pivot è esplicita.
- Riga 57: 840 min per sessione esplicito, 1.050.000 osservazioni derivate correttamente.
- Riga 59: scaling 840/520 ≈ 1,62 esplicito.

---

## Problemi bloccanti

Nessuno.

---

## Problemi non bloccanti

Nessuno con impatto sul comportamento del GA, sul ranking dei cromosomi o sulla conversione signal-to-trade in Parte I.

---

## Osservazioni minori (impatto reale, non cosmesi)

- **M-1 (carryover v3)** — il primo pivot strutturale post-apertura serve come ancora per il target 70%. La regola di identificazione del pivot non è descritta in Cap.1 (correttamente, è materia di Parte II). Resta il follow-up girato a Parte II in v3: verificare che la regola di identificazione non richieda conferma su N barre future, altrimenti l'ancora del target è disponibile solo con ritardo. Non bloccante in Parte I.

- **M-3 (nuova in v4)** — la finestra di 840 min/sessione include i 60 minuti dell'asta di apertura 8:00-9:00 come barre 1-min regolari ai fini del conteggio osservazioni del backtest. Le dinamiche dell'asta (price discovery discontinuo, assenza di order book continuo) sono diverse dalla negoziazione continua. Se i dati Portara/CQG forniscono barre 1-min sull'asta come bar regolari, il calcolo è formalmente corretto ma il GA può ricevere segnali pivot strutturali deboli o spurî sui 60 min di asta. È un rischio di disegno della state machine del segnale, non un bug di Parte I. Da girare a Parte II/Appendice D come vincolo di pre-processing del feed storico (potenzialmente: escludere o trattare separatamente le barre 8:00-9:00 dal calcolo dei pivot strutturali). Non bloccante in Parte I.

- **M-4 (nuova in v4)** — la baseline empirica "12.800-25.600 minuti single-thread sulla finestra ridotta di sola sessione regolare" è citata senza derivazione esplicita. L'Opzione A approvata dal supervisore rende legittimo presentarla come stima empirica decoupled dal prodotto 128 × 150 × t_chromo, ma il documento non chiarisce quale rapporto di rimpiazzo dell'archivio NSGA-II giustifica il numero. Per coerenza con la regola di "misura prima/dopo" del CLAUDE.md, in Parti successive andrebbe documentato il tasso di rimpiazzo atteso che genera quella baseline (≈17-33% delle valutazioni teoriche massime). Non bloccante in Parte I: la stima è esplicitamente provvisoria e va aggiornata in Parte V.

---

## Citazioni rilevanti dal testo (per tracciabilità, nessun bug)

| # | Citazione | Note |
|---|-----------|------|
| 1 | "sessione complessiva di trading del FIB nell'orario 8:00-22:00 CET... asta di apertura (8:00-9:00)... regolare IDEM (9:00-17:40)... after-hours (17:40-22:00)" (riga 9) | Correzione 8-22 applicata con tre fasi esplicite. OK. |
| 2 | "primo minimo o primo massimo della giornata identificato post-apertura (dopo l'asta di apertura, dalle 9:00 CET in poi)" (riga 11) | Distinzione corretta tra perimetro complessivo e finestra di identificazione del primo pivot. OK. |
| 3 | "1.050.000 osservazioni utili (250 giorni di trading per anno, 840 minuti per sessione)" (riga 57) | 250 × 840 × 5 = 1.050.000. OK. |
| 4 | "NSGA-II riutilizza l'archivio dei cromosomi non dominati fra generazioni... non coincide con il prodotto popolazione × generazioni" (riga 59) | Opzione A applicata correttamente. La moltiplicazione misleading è scomparsa. OK. |
| 5 | "ricondotta alla baseline di 12.800-25.600 minuti single-thread sulla finestra ridotta di sola sessione regolare e riscalata linearmente al fattore 840/520 ≈ 1,62, è dell'ordine di 21.000-41.500 minuti single-thread" (riga 59) | Aritmetica coerente: 12.800 × 1,62 ≈ 20.736; 25.600 × 1,62 ≈ 41.472. Arrotondamento esplicito ai numeri tondi 21.000/41.500. OK. |

---

## Classificazione per il supervisore

Nessun problema da mandare a Development. Tabella vuota.

| # | Problema | Classificazione | Mandare a Development? |
|---|----------|-----------------|------------------------|
| — | — | — | — |

Le osservazioni M-1, M-3, M-4 sono follow-up da girare a Parte II / Parte V / Appendice D al momento opportuno; non sono rework di CAP-01.

---

## Sintesi finale per il supervisore (< 200 parole)

**Verdetto v4**: PASS.

Quarto giro ostile completato. La correzione del perimetro sessione 8:00-22:00 CET è applicata in modo coerente: zero residui di 9:00-22:00 nel documento. L'Opzione A per il Cap.4 è effettivamente implementata: la moltiplicazione misleading 128 × 150 × tempo è scomparsa, sostituita da una stima empirica scalata linearmente con menzione esplicita del riuso dell'archivio NSGA-II dei non dominati. Tutta l'aritmetica interna del Cap.4 è verificata coerente (840 min/sessione, 1.050.000 osservazioni, 21.000-41.500 min single-thread, 15-29 giorni, 22-43 ore cloud, 7-15 USD/run, 45-75 EUR budget retraining). Tutti i fix accumulati nei tre cicli precedenti (B-1, B-2, NB-2..NB-5, N-1..N-7) restano applicati senza regressioni. Tre osservazioni minori (M-1 carryover, M-3 trattamento barre d'asta nel pre-processing, M-4 documentazione tasso rimpiazzo NSGA-II) restano come follow-up per Parti II/V/Appendice D, non rework di CAP-01.

**Raccomandazione**: PASS definitivo. CAP-01 può essere chiuso. Procedere con il task successivo.
