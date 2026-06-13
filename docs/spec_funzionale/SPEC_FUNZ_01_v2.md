# SPEC-FUNZ-01 v2 — Specifica funzionale di prodotto (PHASE-1 FIB-only)

**Track**: Business-spec (non-CAP). **Versione**: v2 (ricostruzione ex-novo, modalità B — Developer cieco rispetto al vecchio `SPEC_FUNZ_01.md`).
**Scopo**: consolidare le 10 Parti chiuse PASS della metodologia v2 (`docs/methodology_v2/`, Cap.1-65) in **requisiti funzionali (`R-N`)**, **non-funzionali/qualità (`NFR-N`)** e **vincoli normativi/compliance (`CN-N`)** verificabili e tracciati, come ponte fra il documento metodologico chiuso e la successiva FASE-D di implementazione.
**Vista**: operatore/prodotto. Questo NON è un capitolo metodologico: non ridefinisce metodologia, non introduce parametri del GA, non riapre decisioni `D-*-N` né AC delle Review dei capitoli.

---

## Nota di testa — provenienza e cautele di fonte (RM-1/RM-3)

- **Fonte unica e autoritativa**: i capitoli metodologia v2 **chiusi PASS** (`docs/methodology_v2/CAP_*.md`), congelati G-09. Ogni asserzione fattuale di questa spec è un **richiamo etichettato** a un capitolo chiuso (`[DOC-INTERNO CAP_XX_parte_*.md:<riga>]`), a codice di produzione (`[CODICE-ESISTENTE path:linea]`, grafia canonica), o a una prova già chiusa (`[PROVA-EMPIRICA <data>]`). La spec **non introduce** nuove dichiarazioni "verificato X": nessun blocco `VERIFICA/PROVE/ALTERNATIVE` nuovo è dovuto (non si eseguono verifiche nuove).
- **Citazioni verso CAP-01/02/03**: valide (i capitoli sono chiusi e congelati) ma **SHA-review non ancora pinnabile** (freeze G-09, `<sha-da-confermare>` in `tasks/STATO_CORRENTE.md`). Questa dipendenza è dichiarata **una volta qui** e non ripetuta su ogni requisito. La sola dipendenza dal capitolo a SHA-non-confermato non genera `[B-N PROVVISORIO]`: il tag provvisorio è riservato ai requisiti la cui fonte primaria è un **blocco aperto** (vedi §Blocchi e §matrice).
- **Documentazione esterna** (MiFID II, wiki Directa, Telegram Bot API, Borsa Italiana, Portara/CQG, CME/Eurex): sempre `[WIKI-HINT, da verificare]`, mai fonte unica di un'asserzione strutturale. La **wiki Directa è dimostrata inesatta** sullo schema CANDLE (`O;H;L;C` dichiarato, `C;L;H;O` reale): citata solo con avvertenza esplicita.
- **Grafia etichette**: `[CODICE-ESISTENTE …]` (canonica). La grafia storica `[CODICE-EXISTENTE …]` è vietata in questo documento.
- **Blocchi aperti incardinati**: B-1 (latenza Telegram $L_{max}=30$s, M-2 OPEN) e B-2 (orario sessione FIB, M-GOV-1 in attesa di upgrade a PROVA-EMPIRICA). Vedi §"Blocchi / Domande aperte". I requisiti dipendenti portano il tag `[B-N PROVVISORIO]`.

---

## Sezione 1 — Obiettivo di prodotto e vincolo "solo emissione"

**Valore di prodotto della sezione**: definisce *cosa fa* il prodotto e il confine non negoziabile fra segnale (motore) ed esecuzione (operatore), da cui discende l'intera compliance del sistema.

- **R-1.1** — Il prodotto genera segnali long e short sul FIB (future mini FTSE MIB sull'indice FTSE MIB, mercato IDEM, moltiplicatore 5 EUR/punto indice).
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:9]`.
  - *Valore operativo*: definisce lo strumento e il prodotto-segnale che l'operatore retail riceverà.

- **R-1.2** — Il prodotto **non esegue ordini** in nessuna fase del proprio ciclo di vita: pubblica segnali strutturati su un canale di notifica; apertura, invio ordine, gestione e chiusura competono esclusivamente all'operatore umano che agisce manualmente.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:15]`, `[DOC-INTERNO CAP_06_parte_VI.md:15]` (modalità emissione-only della pipeline).
  - *Valore operativo*: separazione strutturale segnale/esecuzione — il pilastro della compliance retail (vedi CN-7.1).

- **CN-1.1** — Il vincolo "solo emissione, nessuna esecuzione" è **strutturale e non rivedibile**: discende dal punto 1 della dichiarazione di intenti dell'operatore ("genera solo segnali e non effettuerà mai trading direttamente").
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:15]`.
  - *Valore operativo*: rende esplicito che nessuna evoluzione del prodotto può introdurre order routing senza violare il contratto fondante.

- **R-1.3** — I segnali sono di natura intraday; la validità del segnale **eseguito** può estendersi a multiday entro un tetto massimo di **2 giorni di trading** decorrenti dal raw touch (esecuzione), non dall'emissione.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:13]`, `[DOC-INTERNO CAP_02_parte_II.md:63]` (dominio $\Delta t_{cromosoma} \in \{1,\ldots,1680\}$ = $2\times840$ minuti).
  - *Valore operativo*: l'operatore sa che una posizione aperta su un segnale non resta valida indefinitamente; il tetto è 2 sessioni di trading dall'ingresso.

- **R-1.4** — Il target operativo del prodotto è dichiarato in forma **asimmetrica alternativa**: 500 punti FIB di profitto netto giornaliero **OPPURE** il 70% del movimento strutturale intraday (somma dei moduli degli swing fra pivot strutturali, ancorata al primo min/max post-apertura).
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:11]`.
  - *Valore operativo*: definisce cosa significa "giornata di successo" in modo robusto al regime di volatilità del giorno.

**Out-of-scope della Sezione 1**:
| Voce | Destinazione |
|---|---|
| Matematica del movimento strutturale e pivot detection | Parti III/IV (CAP chiusi) — citate dove esce il risultato, non ri-derivate |
| Gestione attiva posizione (take/stop profit dopo il fill) | Operatore (CN-7.4); FASE-D per eventuale supporto |

**Mini-tabella requisiti della sezione**:
| ID | Capitolo-fonte | Tipo |
|---|---|---|
| R-1.1 | CAP_01 (Cap.1) | R |
| R-1.2 | CAP_01 (Cap.1) / CAP_06 (Cap.27) | R |
| CN-1.1 | CAP_01 (Cap.1) | CN |
| R-1.3 | CAP_01 (Cap.1) / CAP_02 (Cap.6) | R |
| R-1.4 | CAP_01 (Cap.1) | R |

---

## Sezione 2 — Destinatario e modalità di consumo

**Valore di prodotto della sezione**: definisce *a chi* è destinato il prodotto e *come* lo consuma — vincoli di profilo che governano formato, sizing e canale.

- **R-2.1** — Il destinatario è un operatore retail italiano (risk manager bancario), classificato **retail non professionale ai sensi MiFID II**, che opera da cellulare in modo discontinuo durante la giornata lavorativa.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:23]`. Riferimento normativo esterno `[WIKI-HINT MiFID II, da verificare]` (la classificazione retail è dato del profilo operatore, non asserzione strutturale della spec).
  - *Valore operativo*: il prodotto deve produrre segnali interpretabili e azionabili senza presenza continuativa allo schermo.

- **R-2.2** — Il dimensionamento della posizione è fissato a **1 contratto FIB alla volta**: il prodotto non calcola né propone gestione della size (incrementi/riduzioni).
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:25]` (punto 7 dichiarazione intenti).
  - *Valore operativo*: l'operatore esegue sempre un solo contratto; nessuna decisione di sizing è delegata al sistema.

- **CN-2.1** — L'operatore esegue manualmente su **miniFIB** (1 EUR/punto) mentre il motore calibra e fa inference sul **FIB pieno** (5 EUR/punto): la separazione fra strumento di calibrazione/inference e strumento di esecuzione è fattuale e voluta.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:25]`, `[DOC-INTERNO CAP_09_parte_9.md:75]` (FIB pieno front-month sottoscritto in runtime; operatore su miniFIB).
  - *Valore operativo*: l'operatore sa di leggere segnali calibrati su FIB pieno ed eseguirli su miniFIB.

- **R-2.3** — Il canale di pubblicazione dei segnali è un **bot Telegram personale** dell'operatore, già attivo, dichiarato come unica via di output verso l'operatore.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:47]`, `[DOC-INTERNO CAP_06_parte_VI.md:146]` (bot Telegram come unica via di output).
  - *Valore operativo*: l'operatore riceve i segnali sul proprio cellulare via Telegram, senza terminale dedicato.

**Out-of-scope della Sezione 2**:
| Voce | Destinazione |
|---|---|
| Testo dei disclaimer MiFID II / parere legale | Consulente legale esterno (FASE-D/business) |
| Setup bot, `chat_id`, stringhe esatte del messaggio | Appendice E / FASE-D |

**Mini-tabella requisiti della sezione**:
| ID | Capitolo-fonte | Tipo |
|---|---|---|
| R-2.1 | CAP_01 (Cap.2) | R |
| R-2.2 | CAP_01 (Cap.2) | R |
| CN-2.1 | CAP_01 (Cap.2) / CAP_09 (Cap.47) | CN |
| R-2.3 | CAP_01 (Cap.3) / CAP_06 (Cap.29) | R |

---

## Sezione 3 — Payload del segnale e invarianti

**Valore di prodotto della sezione**: definisce *cosa pubblica* il prodotto (campi, domini, vincoli, invarianti) — il contratto su cui l'operatore agisce.

- **R-3.1** — Il segnale è una tupla strutturata a **12 campi**: `signal_id`, `timestamp_emission`, `direction`, `entry_zone`, `target_1`, `target_2`, `target_2_type`, `stop_loss`, `stop_type`, `setup_class`, $\Delta t_{cromosoma}$, $T_{touch}^{max}$.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:19]`.
  - *Valore operativo*: definisce esattamente il contenuto informativo che il prodotto consegna.

- **R-3.2** — `direction` ha dominio $\{\text{long}, \text{short}\}$.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:27]`.
  - *Valore operativo*: l'operatore sa se comprare o vendere.

- **R-3.3** — `entry_zone` è una banda di prezzo discreta attorno al prezzo strutturale di riferimento $p_{ref}$, con semi-ampiezza $b$ multipla di 5 nel dominio $\{5,10,15,20,25,30,35,40\}$ punti FIB.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:33]`, `[DOC-INTERNO CAP_01_parte_I.md:27]` (dominio $b\in[b_{min},40]$, $b_{min}=5$).
  - *Valore operativo*: l'operatore conosce la banda entro cui entrare.

- **R-3.4** — `target_1` e `target_2` sono due prezzi strutturali obiettivo, **entrambi obbligatori e distinti**, multipli di 5, ancorati a livelli strutturali del prezzo (long: $\text{target\_1}>p_{ref}$, $\text{target\_2}>\text{target\_1}$; short simmetrico).
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:35]`.
  - *Valore operativo*: l'operatore ha due livelli obiettivo ordinati.

- **R-3.5** — `target_2` è **informazione strutturale pubblicata**, non variabile di lifecycle del segnale: il contratto del segnale si chiude al raggiungimento di `target_1` (decisione Q-05, Clausola 2).
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:37]`.
  - *Valore operativo*: chiarisce all'operatore che target_2 è un'informazione decisionale, non un secondo terminale del segnale.

- **R-3.6** — `target_2_type` e `stop_type` qualificano la natura del livello con dominio $\{\text{structural}, \text{synthetic}\}$: `structural` = derivato da pivot strutturale confermato; `synthetic` = calcolato come livello sintetico in fallback.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:39]` (target_2_type), `[DOC-INTERNO CAP_02_parte_II.md:51]` (stop_type).
  - *Valore operativo*: l'operatore distingue un livello confermato dalla struttura da uno derivato da una regola del modello.

- **R-3.7** — `stop_loss` è un prezzo strutturale di stop, multiplo di 5, soggetto al vincolo geometrico obbligatorio $d_{stop} > b$ (distanza stop dal $p_{ref}$ strettamente maggiore della semi-ampiezza della banda).
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:47]`, `[DOC-INTERNO CAP_01_parte_I.md:29]`.
  - *Valore operativo*: garantisce che un fill al bordo opposto della banda non coincida con lo stop nello stesso tick.

- **R-3.8** — `setup_class` ha dominio $\{\text{directional}, \text{trade\_range}\}$ e determina la regola di filtro di emissione applicata.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:53]`.
  - *Valore operativo*: l'operatore distingue un setup direzionale da uno su rettangolo di prezzo.

- **CN-3.1** — Tutti i prezzi del FIB si muovono per step discreti di **5 punti** (tick size): $p_{ref}$, `target_1`, `target_2`, `stop_loss`, i bordi della banda e $b$ sono multipli di 5; $b_{min}=5$ è esattamente 1 tick.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:9]`.
  - *Valore operativo*: nessun livello pubblicato sarà mai un valore non multiplo di 5; l'operatore può fidarsi della discretizzazione.

- **R-3.9** — Una volta emesso, il segnale identificato da `signal_id` è **immutabile**: nessuna operazione di refresh/edit lascia invariato il `signal_id` modificando un campo del payload.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:73]`.
  - *Valore operativo*: l'operatore opera su valori che non mutano a sua insaputa fra lettura e invio dell'ordine.

- **R-3.10** — Vale il vincolo di **segnale unico attivo**: $|\mathcal{A}(t)| \leq 1$ per ogni $t$ (a ogni istante è attivo al massimo un segnale).
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:81]`, `[DOC-INTERNO CAP_06_parte_VI.md:85]` (estensione operativa anti-doppio-segnale).
  - *Valore operativo*: l'operatore non riceve mai due segnali concorrenti da eseguire contemporaneamente (coerente con 1 contratto/volta).

- **R-3.11** — La revisione del segnale corrente si manifesta come **sostituzione**: emissione di un nuovo `signal_id` con tupla completa indipendente e revoca del precedente (transizione a `revoked`), mai modifica in-place.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:77]`.
  - *Valore operativo*: quando il contesto cambia, l'operatore riceve un nuovo segnale distinto, non un segnale mutato.

**Out-of-scope della Sezione 3**:
| Voce | Destinazione |
|---|---|
| Derivazione geometrica di $p_{ref}$, target, stop | Parte IV (CAP chiuso) — non ri-derivata |
| Formato esatto del log di emissione | Appendice B / FASE-D |

**Mini-tabella requisiti della sezione**:
| ID | Capitolo-fonte | Tipo |
|---|---|---|
| R-3.1..R-3.11 | CAP_02 (Cap.6-7) | R |
| CN-3.1 | CAP_02 (Cap.6) | CN |

---

## Sezione 4 — Esecuzione del segnale e 6 esiti terminali

**Valore di prodotto della sezione**: definisce *quando* un segnale è eseguibile e *quali sono gli esiti terminali* dal punto di vista dell'operatore.

- **R-4.1** — Il segnale ha **un solo stato non-terminale** (`active`) e **6 stati terminali**: `target_1_hit`, `stopped`, `invalidated`, `missed_target`, `expired`, `revoked` (decisione Q-05, Clausola 1).
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:95]`, `[DOC-INTERNO CAP_02_parte_II.md:99]`.
  - *Valore operativo*: l'operatore conosce l'insieme chiuso degli esiti possibili di ogni segnale.

- **CN-4.1** — La distinzione causale del terminale `expired` (`pretrigger_timeout` vs `posttrigger_timeout`) è registrata come **campo strutturato del log**, non come stato dedicato: i terminali restano esattamente 6.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:109]`.
  - *Valore operativo*: garantisce che il numero di esiti pubblicabili resti fisso a 6, con la causa di scadenza tracciata internamente.

- **R-4.2** — Il **raw touch** della entry zone è l'evento di esecuzione, sempre eseguibile: la prima barra 1-min il cui high-low contiene un livello discreto della zona produce il `trigger_event`, senza filtri post-emissione.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:135]`, `[DOC-INTERNO CAP_02_parte_II.md:137]`.
  - *Valore operativo*: una volta emesso il segnale, l'ingresso in zona è sempre azionabile dall'operatore.

- **R-4.3** — Il `trigger_event` è un **evento notificato, non uno stato**: il segnale resta `active` fino a un evento terminale; il motore non osserva il fill manuale dell'operatore sul broker.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:139]`.
  - *Valore operativo*: coerente con "solo emissione" — il sistema notifica l'eseguibilità, non traccia l'ordine reale.

- **R-4.4** — Il segnale dispone di **due timer distinti**: pre-trigger $T_{touch}^{max}\in\{5,\ldots,480\}$ minuti di trading (attesa al raw touch) e post-trigger $\Delta t_{cromosoma}\in\{1,\ldots,1680\}$ minuti di trading (validità dopo l'esecuzione); entrambi avanzano solo nei minuti di sessione, scavalcando notti/weekend/festivi.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:69]` ($T_{touch}^{max}$), `[DOC-INTERNO CAP_02_parte_II.md:163]` (avanzamento pre-trigger), `[DOC-INTERNO CAP_02_parte_II.md:157]` (avanzamento post-trigger).
  - *Valore operativo*: il segnale non resta in attesa indefinita né valido oltre il tetto; i timer rispettano il calendario di trading.

- **CN-4.2** — La chiusura di sessione alle 22:00 CET **non chiude automaticamente** un segnale `active`: la transizione è governata esclusivamente dai counter della state machine; lo stato è persistito e ripreso al boot del giorno successivo.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:292]`, `[DOC-INTERNO CAP_09_parte_9.md:302]`.
  - *Valore operativo*: un segnale aperto a fine sessione non viene perso né forzatamente chiuso; riprende coerentemente l'indomani.

**Out-of-scope della Sezione 4**:
| Voce | Destinazione |
|---|---|
| Condizioni di invalidazione strutturale (definizione completa) | Parte IV (CAP chiuso) |
| Regola deterministica di fill intrabar in backtest | Parte III (CAP chiuso) |

**Mini-tabella requisiti della sezione**:
| ID | Capitolo-fonte | Tipo |
|---|---|---|
| R-4.1..R-4.4 | CAP_02 (Cap.7) | R |
| CN-4.1 | CAP_02 (Cap.7) | CN |
| CN-4.2 | CAP_09 (Cap.52) | CN |

---

## Sezione 5 — Condizioni di emissione

**Valore di prodotto della sezione**: definisce *quando* il motore decide di emettere un segnale — la qualità a monte che protegge l'operatore da segnali in condizioni di mercato avverse.

- **R-5.1** — Il motore decide se emettere un segnale **prima** dell'emissione, sulla base di condizioni di mercato osservate; non esistono filtri post-emissione che blocchino il trigger.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:183]`.
  - *Valore operativo*: la selettività è a monte; dopo l'emissione l'operatore non subisce blocchi inattesi.

- **R-5.2** — L'emissione avviene **se e solo se** valgono simultaneamente tre condizioni (volatilità $E_{vol}$, liquidità $E_{liq}$, distanza strutturale in sigma-units $E_{dist}^{\sigma}$) **e** il filtro 80pt del `setup_class`.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:217]`.
  - *Valore operativo*: condizione AND esplicita che governa ogni emissione.

- **CN-5.1** — Il **filtro minimo di 80 punti FIB** è un vincolo di emissione assoluto (non parametro libero del GA): per setup `directional`, $|\text{target\_1}-p_{ref}|\geq 80$ pt; per setup `trade_range`, l'ampiezza del rettangolo $A_{range}\geq 80$ pt.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:83]` (Cap.5), `[DOC-INTERNO CAP_02_parte_II.md:61]` (Cap.8/setup_class).
  - *Valore operativo*: l'operatore non riceve mai segnali con target/range sotto la soglia minima di valore.

- **R-5.3** — Le condizioni di emissione sono calcolabili esclusivamente da grandezze derivabili dalle **barre 1-min** del feed (range, volume, volatilità condizionata): nessuna condizione richiede spread bid-ask o profondità del book, non disponibili nello storico di training.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:185]`, `[DOC-INTERNO CAP_02_parte_II.md:187]`.
  - *Valore operativo*: garantisce che la logica di emissione live sia omogenea a quella addestrabile sullo storico.

- **CN-5.2** — Le condizioni di emissione si applicano **uniformemente** nell'intera finestra 08:00-22:00 CET: nessuna fase speciale (apertura, asta, after-hours) né soglie differenziate per fascia oraria.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:227]`.
  - *Valore operativo*: comportamento uniforme di emissione lungo tutta la sessione.

**Out-of-scope della Sezione 5**:
| Voce | Destinazione |
|---|---|
| Forma esplicita di $\tau_{vol}$, $\tau_{liq}$, $\tau_{dist}^{\sigma}$ e modello EGARCH | Parte III (CAP chiuso) |
| Definizione operativa di $A_{range}$ | Parte IV Cap.21 (CAP chiuso) |

**Mini-tabella requisiti della sezione**:
| ID | Capitolo-fonte | Tipo |
|---|---|---|
| R-5.1, R-5.2, R-5.3 | CAP_02 (Cap.8) | R |
| CN-5.1 | CAP_01 (Cap.5) / CAP_02 (Cap.6,8) | CN |
| CN-5.2 | CAP_02 (Cap.8) | CN |

---

## Sezione 6 — Consegna su Telegram

**Valore di prodotto della sezione**: definisce *dove e come* il segnale è consegnato (contenuti minimi, anti-duplicato, latenza-requisito) e i requisiti di consegna.

- **R-6.1** — Il messaggio Telegram di emissione pubblica **9 voci** del payload in ordine: `signal_id`, `direction`, `setup_class`, `entry_zone`, `target_1`, `target_2`, `stop_loss`, `timestamp_emission`, più i qualificatori `target_2_type` e `stop_type`.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:241]` (contratto informativo), `[DOC-INTERNO CAP_06_parte_VI.md:148]` (9 voci, layout mobile).
  - *Valore operativo*: l'operatore riceve esattamente i campi decisionali, senza rumore.

- **R-6.2** — I campi $\Delta t_{cromosoma}$ e $T_{touch}^{max}$ **non figurano** nel messaggio: sono parametri tecnici del log interno, non rilevanti per la decisione operativa.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:253]`.
  - *Valore operativo*: il messaggio resta essenziale e leggibile su mobile.

- **R-6.3** — Il messaggio non contiene istruzioni di gestione attiva della posizione (incrementi, scaling out, take/stop profit anticipato).
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:253]`, `[DOC-INTERNO CAP_01_parte_I.md:25]` (punto 8 dichiarazione intenti).
  - *Valore operativo*: coerente con la delega della gestione posizione all'operatore (CN-7.4).

- **NFR-6.1** — Il messaggio è progettato **mobile-first**: testo self-contained (nessuna immagine/media/link), leggibile senza scroll orizzontale, con il contenuto critico (direzione, entry_zone, target_1, stop_loss) entro la prima schermata.
  - *Tracciabilità*: `[DOC-INTERNO CAP_06_parte_VI.md:152]`.
  - *Valore operativo*: l'operatore legge il segnale in pochi secondi sul cellulare in condizioni di attenzione limitata.

- **R-6.4** — Il prodotto pubblica **3 notifiche standard per segnale**: (i) emissione; (ii) `trigger_event` al raw touch; (iii) transizione a stato terminale. Tra una notifica e la successiva non sono inviati aggiornamenti di stato.
  - *Tracciabilità*: `[DOC-INTERNO CAP_06_parte_VI.md:220]`, `[DOC-INTERNO CAP_02_parte_II.md:271]` (notifica trigger separata).
  - *Valore operativo*: l'operatore riceve un flusso di notifiche prevedibile e non rumoroso.

- **R-6.5** — Ogni `signal_id` è pubblicato **una sola volta** (politica anti-duplicato): l'insieme dei `signal_id` pubblicati è persistito, così che un restart del motore non comporti ripubblicazione.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:265]`, `[DOC-INTERNO CAP_06_parte_VI.md:221]`.
  - *Valore operativo*: l'operatore non riceve segnali duplicati.

- **R-6.6** — Un nuovo segnale (sostituzione) è pubblicato come **messaggio Telegram separato** con `signal_id` distinto; nessun edit del messaggio precedente (coerente con l'invariante di payload immutabile).
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:269]`, `[DOC-INTERNO CAP_06_parte_VI.md:192]`.
  - *Valore operativo*: la cronologia Telegram resta una traccia storica immutabile; l'operatore distingue i segnali per `signal_id`.

- **NFR-6.2 [B-1 PROVVISORIO]** — La latenza di consegna $L$ (da `timestamp_emission` alla ricezione sul cellulare) deve rispettare $L \leq L_{max}$, con valore di lavoro provvisorio $L_{max}=30$ s. **La verifica empirica della latenza effettiva è OPEN (blocco B-1, M-2)**: il requisito è dichiarato ma non verificato qui.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:259]` (vincolo $L\leq L_{max}$), `[DOC-INTERNO CAP_07_parte_VII.md:23]` (AC-GO-10, vincolo qualitativo + M-2 OPEN).
  - *Valore operativo*: oltre la soglia il prezzo strutturale di riferimento può essersi spostato e il segnale perde valore informativo.
  - *Provvisorietà*: dipende da B-1 (M-2 latenza Telegram non verificata empiricamente — Appendice E / FASE-D).

- **R-6.7** — In caso di errore di pubblicazione (timeout, rete, indisponibilità) il motore applica una politica di **retry con backoff esponenziale** e, in caso di fallimento finale, registra l'errore e non aggiunge il `signal_id` all'insieme dei pubblicati (segnale registrato come non pubblicato).
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:275]`.
  - *Valore operativo*: i fallimenti di consegna sono tracciati e non rimangono impliciti.

**Out-of-scope della Sezione 6**:
| Voce | Destinazione |
|---|---|
| Stringhe esatte del bot, `chat_id`, API Telegram | Appendice E / FASE-D |
| Valore numerico congelato di $L_{max}$ | Appendice E (M-2 OPEN) |

**Mini-tabella requisiti della sezione**:
| ID | Capitolo-fonte | Tipo |
|---|---|---|
| R-6.1..R-6.7 | CAP_02 (Cap.9) / CAP_06 (Cap.29) | R |
| NFR-6.1 | CAP_06 (Cap.29) | NFR |
| NFR-6.2 [B-1] | CAP_02 (Cap.9) / CAP_07 (Cap.31) | NFR |

---

## Sezione 7 — Vincoli operativi, di sessione e compliance

**Valore di prodotto della sezione**: definisce i *vincoli operativi e normativi* che governano il prodotto (sessione, sizing, commissioni, rollover, compliance, audit, PII).

- **R-7.1 [B-2 PROVVISORIO]** — La sessione operativa del prodotto è la finestra continua **08:00-22:00 CET** (epoca E5): segnali emessi e processati in questa finestra; fuori sessione la pipeline è in stand-by.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:9]`, `[DOC-INTERNO CAP_09_parte_9.md:273]` (Cap.52, epoca E5). Origine governance dell'orario: **M-GOV-1** (decisione AC 13/06/2026 + `[WIKI-HINT Borsa Italiana, da verificare]`).
  - *Valore operativo*: l'operatore sa in quale finestra ricevere segnali.
  - *Provvisorietà*: dipende da B-2 (M-GOV-1 orario in attesa di upgrade a PROVA-EMPIRICA dal primo probe V-1).

- **CN-7.1** — Il prodotto pubblica segnali via Telegram e **non instrada ordini**: separazione segnale/esecuzione; l'esecuzione è manuale e dell'operatore.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:15]`, `[DOC-INTERNO CAP_09_parte_9.md:39]` (porta 10002 trading mai aperta).
  - *Valore operativo*: è la garanzia di compliance retail — il sistema è un segnalatore, non un esecutore.

- **CN-7.2** — Il canale dati runtime è **Directa DAPI** in uso esclusivo: porte 10001 (realtime) e 10003 (storico) in scope; **porta 10002 (trading) mai aperta** dalla pipeline.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:39]`, `[DOC-INTERNO CAP_09_parte_9.md:35]` (tabella porte).
  - *Valore operativo*: rinforza tecnicamente il vincolo "solo emissione" — l'esecuzione è architetturalmente esclusa.

- **CN-7.3** — Il calcolo del rendimento netto incorpora **commissioni di 5 EUR/operazione** (≈1 punto FIB equivalente per operazione, 2 punti per ciclo apertura-chiusura).
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:25]`, `[DOC-INTERNO CAP_01_parte_I.md:73]` (formula $E[R_{net}]=E[R_{gross}]-2c$).
  - *Valore operativo*: i target e le metriche del prodotto sono al netto del costo reale di transazione.

- **CN-7.4** — La gestione attiva della posizione dopo il fill (incrementi, scaling out, take/stop profit) è **interamente delegata all'operatore** e fuori dal contratto del segnale.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:25]` (punto 8), `[DOC-INTERNO CAP_02_parte_II.md:368]` (out-of-scope position lifecycle).
  - *Valore operativo*: il prodotto non interferisce con la gestione discrezionale post-ingresso dell'operatore.

- **R-7.2** — Al boot del giorno di scadenza (terza venerdì del mese) la pipeline sottoscrive direttamente il contratto **next-month**, saltando la finestra 08:00-09:00 del front in scadenza, con marker `CONTRACT_SWITCH` in audit.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:98]` (policy switch front-month, D-9-NB2), `[DOC-INTERNO CAP_09_parte_9.md:433]` (D-9-NB2 tabella).
  - *Valore operativo*: la continuità operativa del prodotto attraverso il rollover non genera segnali sul contratto morente.

- **CN-7.5** — I codici mese Directa-IDEM sono proprietari e **non inferibili per analogia** con lo standard CME: confermati empiricamente `F`=giugno e `I`=settembre (richiamo alle prove citate sotto); gli altri restano da derivare via ANAG.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:61]`, M-4 (`[PROVA-EMPIRICA M-4 2026-05-29]`) e probe ANAG `[PROVA-EMPIRICA 2026-05-27 Appendice B.2]`.
  - *Valore operativo*: protegge da errori di selezione del contratto front-month dovuti ad assunzioni sui codici mese.

- **CN-7.6** — Il prodotto mantiene un **audit log** JSON Lines append-only con **retention minima 90 giorni rolling** e **retention permanente sui giorni di emissione segnale** (giorni con `SIGNAL_EMITTED`/`SIGNAL_TRIGGERED` o un evento terminale).
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:364]`, `[DOC-INTERNO CAP_09_parte_9.md:365]` (D-9-15/Gap-4).
  - *Valore operativo*: garantisce ricostruibilità e tracciabilità compliance dei segnali emessi.

- **CN-7.7** — Gli eventi del lifecycle del segnale sono loggati con **granularità per stato**: `SIGNAL_EMITTED`, `SIGNAL_TRIGGERED` e i 6 terminali distinti (`SIGNAL_TARGET_1_HIT`, `SIGNAL_STOPPED`, `SIGNAL_INVALIDATED`, `SIGNAL_MISSED_TARGET`, `SIGNAL_EXPIRED`, `SIGNAL_REVOKED`).
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:353]`, `[DOC-INTERNO CAP_09_parte_9.md:434]` (D-9-NB3).
  - *Valore operativo*: marker normativi coerenti con i 6 terminali, sufficienti per metriche di lifecycle e audit.

- **CN-7.8** — L'account code Directa (`APIPortSettings.txt`) è **dato PII / sensibile** (non credenziale di autenticazione): escluso dal repo via `.gitignore`, mascherabile negli export pubblici dell'audit; minimizzazione PII per costruzione.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:43]` (Gap-1), `[DOC-INTERNO CAP_09_parte_9.md:358]` (account code PII in audit).
  - *Valore operativo*: protezione del dato personale che lega un'azione di mercato a una persona fisica.

- **CN-7.9** — Gli indici cash europei (DGER/DSTX50/DITAS/DFRA) entrano nella pipeline **esclusivamente** come logging operativo e **gating qualitativo POST-EMISSIONE** (annotazione del messaggio Telegram, mai soppressione del segnale): non entrano nel feature tensor del GA, nella state machine, nel cromosoma, nel walk-forward.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:308]` (Q-A-3), `[DOC-INTERNO CAP_09_parte_9.md:313]` (perimetro vincolante).
  - *Valore operativo*: l'operatore può ricevere una nota di contesto cash sul segnale, senza che il contesto cash alteri il segnale strutturale.

**Out-of-scope della Sezione 7**:
| Voce | Destinazione |
|---|---|
| Lookup completa codici mese IDEM oltre F/I | FASE-D (runtime-discovery via ANAG) |
| Calibrazione fine $\theta_{reconcile}$ | FASE-D / monitoring post-go-live |
| Gestione `chat_id`, file `gating_rules.yaml` | FASE-D |

**Mini-tabella requisiti della sezione**:
| ID | Capitolo-fonte | Tipo |
|---|---|---|
| R-7.1 [B-2] | CAP_01 (Cap.1) / CAP_09 (Cap.52) | R |
| R-7.2 | CAP_09 (Cap.47) | R |
| CN-7.1..CN-7.9 | CAP_01 (Cap.1,2,5) / CAP_02 (Cap.11) / CAP_09 (Cap.46,47,52,53,54) | CN |

---

## Sezione 8 — Criteri di accettazione di prodotto (go-live)

**Valore di prodotto della sezione**: definisce *con quali criteri* il prodotto è dichiarato pronto (KPI lifecycle, gate anti-overfitting, checklist go-live). Tutte le claim empiriche sull'edge restano **PENDING-empirico** fino al run del validator (FASE-D); questa spec le recepisce come criteri dichiarati, non come risultati.

- **NFR-8.1** — Il bundle è accettato per il go-live solo se sui dati OOS presenta **DSR (Deflated Sharpe Ratio) positivo e significativo** come gate primario (soglia di lavoro $\theta_{DSR}=0{,}95$, non congelata).
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:81]`, `[DOC-INTERNO CAP_07_parte_VII.md:202]` (Cap.32.4), `[DOC-INTERNO CAP_07_parte_VII.md:570]` (AC-GO-1).
  - *Valore operativo*: garantisce che la performance del prodotto non sia un artefatto del numero di prove condotte.

- **NFR-8.2** — Il bundle è accettato solo se **PBO (Probability of Backtest Overfitting) sotto soglia** come gate di fragilità (soglia di lavoro $\theta_{PBO}=0{,}50$, non congelata).
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:81]`, `[DOC-INTERNO CAP_07_parte_VII.md:572]` (AC-GO-2).
  - *Valore operativo*: garantisce che la scelta del bundle non dipenda fragilmente dalla partizione dei dati.

- **NFR-8.3** — Il bundle è accettato solo se **$E[R_{net}\mid executed]$ è positivo** dopo commissioni, con intervallo di confidenza bootstrap al 95% che esclude lo zero.
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:83]` (Cap.5), `[DOC-INTERNO CAP_07_parte_VII.md:574]` (AC-GO-3).
  - *Valore operativo*: il prodotto deve avere un rendimento netto atteso positivo, non solo lordo.

- **NFR-8.4** — Il bundle è accettato solo se i KPI di lifecycle (target hit rate, executable rate) sono **stabili e comparabili fra regime calmo e turbolento** (lifecycle stabile cross-regime, $|f_5^{global}|<\theta_{f_5}=0{,}30$ di lavoro).
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:85]`, `[DOC-INTERNO CAP_07_parte_VII.md:576]` (AC-GO-4).
  - *Valore operativo*: il prodotto si comporta in modo coerente a prescindere dal regime di volatilità del periodo.

- **NFR-8.5** — Il bundle è accettato solo se **CVaR al 95% e maximum drawdown intraday** sono entro limiti dichiarati ($\theta_{CVaR}=-100$ pt, $\theta_{MDD}=200$ pt di lavoro).
  - *Tracciabilità*: `[DOC-INTERNO CAP_01_parte_I.md:85]`, `[DOC-INTERNO CAP_07_parte_VII.md:580]` (AC-GO-6), `[DOC-INTERNO CAP_07_parte_VII.md:582]` (AC-GO-7).
  - *Valore operativo*: limita la perdita di coda e il drawdown intraday, compatibili col profilo retail a 1 contratto.

- **NFR-8.6** — La decisione di go-live è governata da una **checklist deterministica di 12 AC binari (AC-GO-1..AC-GO-12)**: GO solo se tutti e 12 sono OK; NO-GO con motivazione esplicita se anche uno solo è NOT OK.
  - *Tracciabilità*: `[DOC-INTERNO CAP_07_parte_VII.md:568]`, `[DOC-INTERNO CAP_07_parte_VII.md:601]`.
  - *Valore operativo*: criterio oggettivo e replicabile per dichiarare il prodotto pronto.

- **NFR-8.7** — Tra i 12 AC di go-live, il prodotto deve verificare che la **frequenza di emissione** sia nel range $[0{,}2; 5]$ segnali/sessione (AC-GO-8) e che il **target operativo asimmetrico** di Sez.1 sia raggiunto in oltre il 60% delle sessioni OOS (AC-GO-9, soglia di lavoro).
  - *Tracciabilità*: `[DOC-INTERNO CAP_07_parte_VII.md:584]` (AC-GO-8), `[DOC-INTERNO CAP_07_parte_VII.md:586]` (AC-GO-9).
  - *Valore operativo*: garantisce un volume di segnali utile e il raggiungimento del target di prodotto nella maggioranza delle sessioni.

- **NFR-8.8** — Tra i 12 AC di go-live rientrano verifiche infrastrutturali: pipeline di inference operativa con payload bit-exact e latenza qualitativa (AC-GO-10), dashboard di monitoraggio attiva (AC-GO-11), e **hash SHA-256 del bundle frozen valido** al caricamento (AC-GO-12).
  - *Tracciabilità*: `[DOC-INTERNO CAP_07_parte_VII.md:588]` (AC-GO-10), `[DOC-INTERNO CAP_07_parte_VII.md:594]` (AC-GO-11), `[DOC-INTERNO CAP_07_parte_VII.md:599]` (AC-GO-12).
  - *Valore operativo*: garantisce che, oltre alla statistica, l'infrastruttura del prodotto sia funzionante e integra prima del go-live.

**Out-of-scope della Sezione 8**:
| Voce | Destinazione |
|---|---|
| Calcolo empirico effettivo di DSR/PBO/$E[R_{net}]$ sull'edge | **PENDING-empirico** — validator (FASE-D) |
| Motore GA, NSGA-II, fitness, walk-forward (derivazione) | Parte V (CAP chiuso) — non ri-derivata |
| Valori congelati definitivi delle soglie $\theta_*$ | Parte V / post-go-live |

**Mini-tabella requisiti della sezione**:
| ID | Capitolo-fonte | Tipo |
|---|---|---|
| NFR-8.1..NFR-8.8 | CAP_01 (Cap.5) / CAP_07 (Cap.31,32,33,36) | NFR |

---

## Sezione 9 — Dipendenze di dato e infrastruttura; requisiti di dato

**Valore di prodotto della sezione**: definisce *quali dipendenze* di dato/infrastruttura il prodotto richiede e *quali requisiti di dato* garantiscono la qualità del feed che alimenta i segnali.

- **CN-9.1** — Lo schema CANDLE reale del payload Directa è **`C;L;H;O;V`** (`UFF;MIN;MAX;APE;V` = close;low;high;open;volume), **non** l'ordine `O;H;L;C` dichiarato dal wiki (dimostrato inesatto).
  - *Tracciabilità*: `[CODICE-ESISTENTE scripts/export_directa_history_parametric.py:477-481]`, `[PROVA-EMPIRICA M-1 2026-05-29]`; il wiki resta `[WIKI-HINT, da verificare]` e dimostrato inesatto.
  - *Valore operativo*: garantisce che le barre che alimentano i segnali siano decodificate correttamente (RACC-METODO-2: diff col decoder canonico, non col wiki).

- **R-9.1** — L'adapter DAPI produce, per ogni minuto della sessione, una barra 1-min normativa con schema **simmetrico al tape di training Portara** (OHLCV, `tick_count`, flag `bar_synthetic`), forward-fill su Close per i minuti senza trade: il bundle frozen non legge mai dati DAPI grezzi (invariante research = runtime).
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:17]`, `[DOC-INTERNO CAP_09_parte_9.md:191]` (Cap.49, adapter = normalizzazione di schema).
  - *Valore operativo*: i segnali live sono prodotti sulla stessa struttura dati del training, senza re-calibrazione.

- **R-9.2** — Il warm-up degli stati condizionali al boot di sessione usa un pull storico via `CANDLERANGE` (porta 10003) con lookback congelato **$L_{warmup}=30$ giorni di trading IDEM**, ampiamente entro il limite DAPI intraday di ~100 giorni.
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:254]` (D-9-NB4), `[CODICE-ESISTENTE scripts/export_directa_history_parametric.py:61]` (`DEFAULT_INTRADAY_MAX_DAYS=100`), `[DOC-INTERNO CAP_10_parte_10.md:80]` (limite ~100gg verificato).
  - *Valore operativo*: garantisce che il motore disponga di stato condizionato inizializzato prima di emettere segnali validi.

- **R-9.3** — Il recupero gap entro la finestra ~100 giorni avviene via `CANDLERANGE` con marker di provenienza `BACKFILL_FROM_CANDLERANGE`; oltre i 100 giorni (restart >100gg) la pipeline entra in stato `RUNTIME_STALE_RESTART` e richiede re-bootstrap a 3 step (archivio locale, CANDLERANGE daily, fallback Portara) con re-warm-up obbligatorio.
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:91]` (Cap.59 backfill), `[DOC-INTERNO CAP_10_parte_10.md:158]` (Cap.61 re-bootstrap 3 step), `[DOC-INTERNO CAP_09_parte_9.md:261]` (B-6 restart >100gg).
  - *Valore operativo*: il prodotto si riallinea automaticamente dopo gap brevi e in modo assistito dopo downtime prolungati, senza contaminare i segnali.

- **R-9.4** — A ogni end-of-day il prodotto esegue una **riconciliazione canonica giornaliera** come **gate operativo bloccante**: se la riconciliazione del giorno $d$ fallisce (`RECONCILE_DIVERGENT_*`/`RECONCILE_DEGRADED`), l'emissione di segnali del giorno $d+1$ è bloccata fino a intervento del supervisore.
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:126]` (Cap.60 stato finale + gate), `[DOC-INTERNO CAP_10_parte_10.md:42]` (gate bloccante distinto dal monitoraggio non-bloccante di Cap.30).
  - *Valore operativo*: protezione contro la deriva silenziosa del feed che altrimenti contaminerebbe i segnali emessi.

- **CN-9.2** — Per i ticker cash europei la riconciliazione del low/high giornaliero usa **esclusivamente la CANDLE ufficiale daily** (campi `f8`/`f9` = day_low/day_high), mai l'aggregato dei tick realtime (feed `PRICE` cash rado che perde i minimi intraday).
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:123]` (Cap.60 step 5), `[DOC-INTERNO CAP_10_parte_10.md:251]` (D-10-4), `[PROVA-EMPIRICA 2026-06-01]` (6/6 mismatch DITAS sul solo low).
  - *Valore operativo*: evita falsi divergenti di riconciliazione dovuti alla radezza del feed cash.

- **R-9.5** — Il tape DAPI runtime è archiviato in un **archivio canonico locale** con header CSV esteso a 13 campi, manifest JSON (incl. `reconcile_status`, `bar_counts_by_source`, `gap_log`) e **immutabilità append-only** (recupero gap retroattivo divergente apre una nuova versione, mai sovrascrittura).
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:185]` (Cap.62 formato), `[DOC-INTERNO CAP_10_parte_10.md:207]` (idempotenza/versioning append-only).
  - *Valore operativo*: permette ricostruzione post-hoc del replay deterministico e riconciliazione storica.

- **CN-9.3** — Il tape DAPI archiviato **non è fonte di training** del bundle: è destinato esclusivamente a riconciliazione, replay e bootstrap; l'apertura come fonte di training richiederebbe un nuovo task Planner.
  - *Tracciabilità*: `[DOC-INTERNO CAP_10_parte_10.md:209]` (D-10-9), `[DOC-INTERNO CAP_08_parte_8.md:217]` (esclusione fonti alternative di training — Cap.44).
  - *Valore operativo*: preserva la separazione fra serie di calibrazione (Portara ratio-adjusted) e tape runtime (DAPI unadjusted).

- **CN-9.4** — Il replay del motore è **deterministico bit-exact**: dato lo stesso storico e lo stesso bundle frozen, il replay produce la stessa sequenza di emissioni, `signal_id`, transizioni e timestamp; nessun generatore pseudo-casuale non seedato.
  - *Tracciabilità*: `[DOC-INTERNO CAP_02_parte_II.md:291]` (requisito di determinismo), `[DOC-INTERNO CAP_02_parte_II.md:295]`.
  - *Valore operativo*: rende le metriche di lifecycle verificabili e usabili come gate decisionale per il go-live.

**Dipendenze infrastrutturali (citate come dipendenza, non requisito di prodotto)**:
- **Compute/cloud**: training del GA su AWS spot (c5.4xlarge), inference e backtest leggero sul PC dell'operatore. `[DOC-INTERNO CAP_01_parte_I.md:63]` (Cap.4). *Citata come dipendenza infrastrutturale, non requisito.*
- **Storico training**: serie FIB continuo 1-min ≥5 anni da Portara/CQG. `[DOC-INTERNO CAP_01_parte_I.md:43]`, `[DOC-INTERNO CAP_08_parte_8.md:155]` (Cap.42). *Materia di training; dipendenza.*
- **Costo DAPI**: 20 EUR/mese, azzerato oltre 200 EUR/mese di commissioni. `[DOC-INTERNO CAP_01_parte_I.md:41]`, `[DOC-INTERNO CAP_09_parte_9.md:373]` (Gap-6). *Costo strutturale runtime; dipendenza.*

**Out-of-scope della Sezione 9**:
| Voce | Destinazione |
|---|---|
| Vendor cross-index pluriennale (PHASE-2) | spec futura / FASE-D |
| Implementazione adapter/parser DAPI, codice pipeline | FASE-D |
| Migrazione dump legacy 11→13 campi | FASE-D (una-tantum) |

**Mini-tabella requisiti della sezione**:
| ID | Capitolo-fonte | Tipo |
|---|---|---|
| R-9.1..R-9.5 | CAP_09 (Cap.49,51) / CAP_10 (Cap.59,60,61,62) | R |
| CN-9.1 | CAP_09 (Cap.49) / codice | CN |
| CN-9.2, CN-9.3, CN-9.4 | CAP_10 (Cap.60,62) / CAP_02 (Cap.10) / CAP_08 (Cap.44) | CN |

---

## Sezione 10 — Fasizzazione e confine PHASE-1 / PHASE-2

**Valore di prodotto della sezione**: definisce *come è fasizzato* il prodotto (PHASE-1 in scope, PHASE-2 fuori) e quali dipendenze restano aperte verso FASE-D.

- **R-10.1** — Il prodotto corrente è **PHASE-1 FIB-only**: single-instrument FIB, senza layer di covarianza cross-index. La fasizzazione è esplicita, non semplificazione silenziosa.
  - *Tracciabilità*: `[DOC-INTERNO CAP_08_parte_8.md:143]` (Cap.42), `[DOC-INTERNO CAP_08_parte_8.md:167]` (vincolo fasizzazione PHASE-1 vs PHASE-2).
  - *Valore operativo*: l'operatore opera solo sul FIB; nessun segnale cross-index è in scope nel prodotto corrente.

- **CN-10.1** — Gli strumenti cross-index PHASE-2 (DAX/EuroStoxx50/S&P mini futures) sono **dichiarazione normativa senza implementazione** nel doc v2 corrente: la loro attivazione è rinviata a un futuro ciclo di estensione, fuori scope qui.
  - *Tracciabilità*: `[DOC-INTERNO CAP_08_parte_8.md:143]`, `[DOC-INTERNO CAP_09_parte_9.md:338]` (cash europei ≠ cross-index PHASE-2), `[DOC-INTERNO CAP_10_parte_10.md:236]` (Parte 10 non si applica ai cross-index PHASE-2).
  - *Valore operativo*: il confine di prodotto è netto; eventuali estensioni cross-index sono un prodotto futuro distinto.

- **R-10.2** — Restano **dipendenze aperte verso FASE-D**: verifica empirica della latenza Telegram ($L_{max}$, B-1/M-2), upgrade empirico dell'orario di sessione (B-2/M-GOV-1), calibrazione fine di $\theta_{reconcile}$, e il run empirico del validator sull'edge (DSR/PBO/OOS, PENDING-empirico).
  - *Tracciabilità*: `[DOC-INTERNO CAP_09_parte_9.md:402]` (M-2 OPEN), `[DOC-INTERNO CAP_10_parte_10.md:232]` ($\theta_{reconcile}$ provvisorio), `[DOC-INTERNO CAP_07_parte_VII.md:639]` (10 parametri tuning carryover post-go-live).
  - *Valore operativo*: rende esplicito ciò che il prodotto dichiara ma non chiude, da risolvere prima/durante FASE-D.

**Out-of-scope della Sezione 10**:
| Voce | Destinazione |
|---|---|
| Requisiti PHASE-2 cross-index | spec futura (SPEC-FUNZ-02 o equivalente) |
| Specifica di implementazione FASE-D | FASE-D |

**Mini-tabella requisiti della sezione**:
| ID | Capitolo-fonte | Tipo |
|---|---|---|
| R-10.1, R-10.2 | CAP_08 (Cap.42) / CAP_07/09/10 | R |
| CN-10.1 | CAP_08 (Cap.42) / CAP_09 (Cap.53) / CAP_10 (Cap.64) | CN |

---

## Sezione 11 — Matrice di tracciabilità requisito → capitolo metodologia v2

Una riga per requisito. Tutte le citazioni puntuali `file:riga` sono nei requisiti delle Sezioni 1-10.

| Requisito | Tipo | Capitolo/i metodologia v2 (Parte) |
|---|---|---|
| R-1.1 | R | CAP_01 Cap.1 (PI) |
| R-1.2 | R | CAP_01 Cap.1 (PI) / CAP_06 Cap.27 (PVI) |
| R-1.3 | R | CAP_01 Cap.1 (PI) / CAP_02 Cap.6 (PII) |
| R-1.4 | R | CAP_01 Cap.1 (PI) |
| CN-1.1 | CN | CAP_01 Cap.1 (PI) |
| R-2.1 | R | CAP_01 Cap.2 (PI) |
| R-2.2 | R | CAP_01 Cap.2 (PI) |
| R-2.3 | R | CAP_01 Cap.3 (PI) / CAP_06 Cap.29 (PVI) |
| CN-2.1 | CN | CAP_01 Cap.2 (PI) / CAP_09 Cap.47 (P9) |
| R-3.1 | R | CAP_02 Cap.6 (PII) |
| R-3.2 | R | CAP_02 Cap.6 (PII) |
| R-3.3 | R | CAP_02 Cap.6 (PII) / CAP_01 Cap.2 (PI) |
| R-3.4 | R | CAP_02 Cap.6 (PII) |
| R-3.5 | R | CAP_02 Cap.6 (PII) |
| R-3.6 | R | CAP_02 Cap.6 (PII) |
| R-3.7 | R | CAP_02 Cap.6 (PII) / CAP_01 Cap.2 (PI) |
| R-3.8 | R | CAP_02 Cap.6 (PII) |
| R-3.9 | R | CAP_02 Cap.6 (PII) |
| R-3.10 | R | CAP_02 Cap.6 (PII) / CAP_06 Cap.28 (PVI) |
| R-3.11 | R | CAP_02 Cap.6 (PII) |
| CN-3.1 | CN | CAP_02 Cap.6 (PII) |
| R-4.1 | R | CAP_02 Cap.7 (PII) |
| R-4.2 | R | CAP_02 Cap.7 (PII) |
| R-4.3 | R | CAP_02 Cap.7 (PII) |
| R-4.4 | R | CAP_02 Cap.6-7 (PII) |
| CN-4.1 | CN | CAP_02 Cap.7 (PII) |
| CN-4.2 | CN | CAP_09 Cap.52 (P9) |
| R-5.1 | R | CAP_02 Cap.8 (PII) |
| R-5.2 | R | CAP_02 Cap.8 (PII) |
| R-5.3 | R | CAP_02 Cap.8 (PII) |
| CN-5.1 | CN | CAP_01 Cap.5 (PI) / CAP_02 Cap.6,8 (PII) |
| CN-5.2 | CN | CAP_02 Cap.8 (PII) |
| R-6.1 | R | CAP_02 Cap.9 (PII) / CAP_06 Cap.29 (PVI) |
| R-6.2 | R | CAP_02 Cap.9 (PII) |
| R-6.3 | R | CAP_02 Cap.9 (PII) / CAP_01 Cap.2 (PI) |
| R-6.4 | R | CAP_06 Cap.29 (PVI) / CAP_02 Cap.9 (PII) |
| R-6.5 | R | CAP_02 Cap.9 (PII) / CAP_06 Cap.29 (PVI) |
| R-6.6 | R | CAP_02 Cap.9 (PII) / CAP_06 Cap.29 (PVI) |
| R-6.7 | R | CAP_02 Cap.9 (PII) |
| NFR-6.1 | NFR | CAP_06 Cap.29 (PVI) |
| NFR-6.2 [B-1] | NFR | CAP_02 Cap.9 (PII) / CAP_07 Cap.31 (PVII) |
| R-7.1 [B-2] | R | CAP_01 Cap.1 (PI) / CAP_09 Cap.52 (P9) |
| R-7.2 | R | CAP_09 Cap.47 (P9) |
| CN-7.1 | CN | CAP_01 Cap.1 (PI) / CAP_09 Cap.46 (P9) |
| CN-7.2 | CN | CAP_09 Cap.46 (P9) |
| CN-7.3 | CN | CAP_01 Cap.2,5 (PI) |
| CN-7.4 | CN | CAP_01 Cap.2 (PI) / CAP_02 Cap.11 (PII) |
| CN-7.5 | CN | CAP_09 Cap.47 (P9) |
| CN-7.6 | CN | CAP_09 Cap.54 (P9) |
| CN-7.7 | CN | CAP_09 Cap.54 (P9) |
| CN-7.8 | CN | CAP_09 Cap.46,54 (P9) |
| CN-7.9 | CN | CAP_09 Cap.53 (P9) |
| NFR-8.1 | NFR | CAP_01 Cap.5 (PI) / CAP_07 Cap.32,36 (PVII) |
| NFR-8.2 | NFR | CAP_01 Cap.5 (PI) / CAP_07 Cap.33,36 (PVII) |
| NFR-8.3 | NFR | CAP_01 Cap.5 (PI) / CAP_07 Cap.36 (PVII) |
| NFR-8.4 | NFR | CAP_01 Cap.5 (PI) / CAP_07 Cap.31,36 (PVII) |
| NFR-8.5 | NFR | CAP_01 Cap.5 (PI) / CAP_07 Cap.36 (PVII) |
| NFR-8.6 | NFR | CAP_07 Cap.36 (PVII) |
| NFR-8.7 | NFR | CAP_07 Cap.36 (PVII) |
| NFR-8.8 | NFR | CAP_07 Cap.36 (PVII) / CAP_07 Cap.35 (PVII) |
| CN-9.1 | CN | CAP_09 Cap.49 (P9) / codice |
| R-9.1 | R | CAP_09 Cap.45,49 (P9) |
| R-9.2 | R | CAP_09 Cap.51 (P9) / codice / CAP_10 Cap.59 (P10) |
| R-9.3 | R | CAP_10 Cap.59,61 (P10) / CAP_09 Cap.51 (P9) |
| R-9.4 | R | CAP_10 Cap.60 (P10) |
| CN-9.2 | CN | CAP_10 Cap.60 (P10) |
| R-9.5 | R | CAP_10 Cap.62 (P10) |
| CN-9.3 | CN | CAP_10 Cap.62 (P10) / CAP_08 Cap.44 (P8) |
| CN-9.4 | CN | CAP_02 Cap.10 (PII) |
| R-10.1 | R | CAP_08 Cap.42 (P8) |
| R-10.2 | R | CAP_09 Cap.55 (P9) / CAP_10 Cap.64 (P10) / CAP_07 Cap.36 (PVII) |
| CN-10.1 | CN | CAP_08 Cap.42 (P8) / CAP_09 Cap.53 (P9) / CAP_10 Cap.64 (P10) |

**Conteggio**: 41 R + 10 NFR + 21 CN = **72 requisiti**. Tutti tracciati ad almeno un capitolo (matrice 72 righe, riconciliata 1:1 con i requisiti definiti nelle Sez.1-10: 0 mancanti, 0 orfani). Requisiti `[B-N PROVVISORIO]`: NFR-6.2 (B-1), R-7.1 (B-2).

---

## Sezione 12 — Capitoli non tracciati (con motivazione)

Capitoli della metodologia v2 **non** mappati a un requisito di prodotto, con motivazione. Sono matematica/motore interni, opachi al consumatore del segnale, oppure dettagli interni già coperti via altre Parti in vista prodotto.

| Capitolo (Parte) | Motivo del non-tracciamento |
|---|---|
| **Cap.4 (Parte I)** — compute budget / strategia cloud | Dipendenza infrastrutturale (AWS spot, TCO), non requisito di prodotto. Citato in Sez.9 come dipendenza. |
| **Cap.10 (Parte II)** — replay/determinismo (dettaglio) | Il *requisito* di determinismo bit-exact è tracciato (CN-9.4); il formato esatto dei tre log è dettaglio interno → Appendice B/FASE-D. |
| **Cap.12 (Parte III)** — definizioni rendimento/scala temporale | Matematica interna del modello, opaca al consumatore: il prodotto pubblica il risultato (payload), non la derivazione. |
| **Cap.13 (Parte III)** — modello di volatilità condizionata (EGARCH) | Matematica interna; alimenta condizioni di emissione (tracciate in Sez.5) ma la formula è opaca al consumatore. |
| **Cap.14 (Parte III)** — stato di regime intraday | Matematica interna; il regime calmo/turbolento entra negli NFR di stabilità cross-regime (Sez.8) ma la classificazione è interna. |
| **Cap.15 (Parte III)** — feature engineering causale | Catalogo 37 feature, matematica interna del motore, opaca al consumatore del segnale. |
| **Cap.16 (Parte IV)** — definizione zone di entry | Derivazione geometrica interna; il prodotto pubblica `entry_zone` (R-3.3), non la geometria che la produce. |
| **Cap.17 (Parte IV)** — target strutturali | Derivazione geometrica interna; il prodotto pubblica `target_1`/`target_2`/`target_2_type` (R-3.4/3.6), non la derivazione. |
| **Cap.18 (Parte IV)** — stop strutturali | Derivazione geometrica interna; il prodotto pubblica `stop_loss`/`stop_type` (R-3.7/3.6), non la derivazione. |
| **Cap.19 (Parte IV)** — modello di survival per il target | Matematica interna (Cox); alimenta filtri di emissione e tie-break, opaca al consumatore. |
| **Cap.20 (Parte IV)** — filtri di emissione basati sul survival | Filtro $E_{surv}$ interno; il prodotto espone l'esito (segnale emesso o no), non la matematica del survival. |
| **Cap.21 (Parte IV)** — caso trade_range | Derivazione interna di $A_{range}$; il prodotto espone `setup_class=trade_range` e il filtro 80pt (R-3.8/CN-5.1), non la derivazione. |
| **Cap.22-26 (Parte V)** — cromosoma, NSGA-II, fitness, walk-forward, calibrazione | Motore GA interno, opaco al consumatore. I suoi *gate* emergono come NFR via Parte VII (Sez.8); la meccanica del GA non è prodotto. |
| **Cap.27 (Parte VI)** — pipeline di inference real-time | Interna/FASE-D; citata per il vincolo emissione-only (R-1.2) e per AC-GO-10 (NFR-8.8), non requisito a sé. |
| **Cap.30 (Parte VI)** — monitoraggio/dashboard | Interna/FASE-D; citata per contrasto col gate bloccante di riconciliazione (R-9.4) e per AC-GO-11 (NFR-8.8), non requisito a sé. |
| **Cap.34 (Parte VII)** — bootstrap stazionario | Meccanismo statistico interno; alimenta l'IC bootstrap di NFR-8.3 ma la procedura è interna. |
| **Cap.35 (Parte VII)** — frozen bundle / hash | Meccanismo interno; citato (AC-GO-12, hash valido) in NFR-8.8, non requisito a sé. |
| **Cap.37-44 (Parte 8) salvo Cap.42** — dati storici/back-adjustment/sanity/esclusione fonti | Materia di training; dipendenza infrastrutturale (Portara/CQG) in Sez.9. Cap.44 citato in CN-9.3 (esclusione fonti training). Solo Cap.42 (fasizzazione) è tracciato (R-10.1/CN-10.1). |
| **Cap.45, 48, 50 (Parte 9)** — premessa, format dati canonico, gestione errori/recovery | Dettagli interni dell'adapter/recovery DAPI; il *requisito* di schema simmetrico è tracciato (R-9.1, CN-9.1), il dettaglio del format e dei codici errore è interno/FASE-D. |
| **Cap.55 (Parte 9)** — punti aperti fuori scope | Capitolo di rinvii; le sue voci aperte sono recepite in R-10.2, non requisito a sé. |
| **Cap.57, 58, 63, 64, 65 (Parte 10)** — premessa, tassonomia gap, coerenza inter-temporale, punti aperti, tabella decisioni | Premesse/tassonomia/coerenza/rinvii interni; i requisiti operativi (backfill, riconciliazione, archivio) sono tracciati in Sez.9 (R-9.3/9.4/9.5), questi capitoli di cornice no. |

**Parti interamente non tracciate**: **Parte III** (Cap.12-15), **Parte IV** (Cap.16-21), **Parte V** (Cap.22-26) — matematica/motore interni, opachi al consumatore del segnale, come da tabella sopra.

---

## Sezione 13 — Blocchi / Domande aperte

Due blocchi aperti incardinati. I requisiti dipendenti portano il tag `[B-N PROVVISORIO]`.

- **B-1 — Latenza Telegram $L_{max}$ non verificata empiricamente (M-2 OPEN)**.
  - *Requisito dipendente*: **NFR-6.2**.
  - *Motivo*: il valore $L_{max}=30$ s è valore di lavoro provvisorio; la verifica empirica della latenza effettiva del canale Telegram non è stata eseguita ed è carryover di Appendice E / FASE-D. `[DOC-INTERNO CAP_09_parte_9.md:402]`, `[DOC-INTERNO CAP_07_parte_VII.md:23]`.
  - *Cosa serve per sbloccarlo*: probe empirico sulla latenza del bot Telegram reale (Appendice E / FASE-D) → upgrade del requisito da provvisorio a verificato.

- **B-2 — Orario di sessione FIB in attesa di upgrade a PROVA-EMPIRICA (M-GOV-1)**.
  - *Requisito dipendente*: **R-7.1**.
  - *Motivo*: l'orario 08:00-22:00 CET è recepito da decisione AC 13/06/2026 + `[WIKI-HINT Borsa Italiana, da verificare]`; l'upgrade a `[PROVA-EMPIRICA]` dal primo probe V-1 sul tape DAPI è APERTO (M-GOV-1, namespace governance).
  - *Cosa serve per sbloccarlo*: primo probe V-1 che confermi empiricamente la finestra di negoziazione continua sul tape DAPI → upgrade del requisito da provvisorio a verificato.

**Nota**: nessun altro blocco. Tutti gli altri M citati nel task card (M-4, M-9, M-10, M-16, ecc.) sono CLOSED o note tecniche già incorporate come fonte; nessuno è incardinato come blocco aperto. La dipendenza da CAP-01/02/03 a SHA-non-pinnabile (freeze G-09) è dichiarata in nota di testa e **non** è un blocco aperto (i capitoli sono chiusi e congelati, citabili).
