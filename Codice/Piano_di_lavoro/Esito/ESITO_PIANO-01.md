# ESITO_PIANO-01 — Inventario autoritativo dei requisiti di SPEC_FUNZ_01

> **Track:** Business-spec / track piano (non-CAP). **Task:** PIANO-01 (vedi `Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_PIANO-01.md`).
> **Natura:** sola lettura di `docs/spec_funzionale/SPEC_FUNZ_01.md` + scrittura di questo ESITO. **NON e il piano**: nessun modulo, architettura, DAG, sequenziamento o priorita.
> **Fonte unica (RM-2):** `docs/spec_funzionale/SPEC_FUNZ_01.md` a HEAD. SHA-ancora `9b2a10f` risolve (`git cat-file -t 9b2a10f` = `commit`). Ogni riga e citata con `riga:path` reale del **corpo** della spec.
> **Convenzione `riga:path`:** la riga citata e quella della **definizione del requisito nel corpo** (Sezioni 1-10), NON la riga della tabella di mapping (Sez.11) ne la citazione CAP in-linea.

---

## 1. Conteggio

**Totale requisiti in `SPEC_FUNZ_01.md` = 375.** Trovato **375** = atteso **375** → **nessuna discrepanza**.

Il formato ID nel corpo e **sezione-based** (`R-x.y` / `CN-x.y` / `NFR-x.y`, con `x` = Sezione 1..10). La famiglia `B*-*` citata nell'handoff originale e l'**ID-blocco originario** (colonna 2 della tabella di mapping di Sez.11); nel corpo dell'assemblato i requisiti portano l'ID sezione-based. I comandi sotto contano gli ID sezione-based, coerentemente col formato reale osservato (PRE-FLIGHT punto 5).

### Metodo 1 — definizioni nel corpo (Sez.1-10)

Comando:

```
grep -cnE "^[[:space:]]*-[[:space:]]+\*\*(R|NFR|CN)-[0-9]+\.[0-9]+\*\* " docs/spec_funzionale/SPEC_FUNZ_01.md
```

Output: `375`

Ripartizione per famiglia (stesso pattern, ancorato alla famiglia):

| Famiglia | Comando | Output |
|---|---|---|
| R   | `grep -cnE "^[[:space:]]*-[[:space:]]+\*\*R-[0-9]+\.[0-9]+\*\* " docs/spec_funzionale/SPEC_FUNZ_01.md`   | `264` |
| CN  | `grep -cnE "^[[:space:]]*-[[:space:]]+\*\*CN-[0-9]+\.[0-9]+\*\* " docs/spec_funzionale/SPEC_FUNZ_01.md`  | `82`  |
| NFR | `grep -cnE "^[[:space:]]*-[[:space:]]+\*\*NFR-[0-9]+\.[0-9]+\*\* " docs/spec_funzionale/SPEC_FUNZ_01.md` | `29`  |

Somma: 264 + 82 + 29 = **375**.

### Metodo 2 — tabella di mapping (Sez.11.2)

Conta le righe della tabella `| <ID-assemblato> | B?-...-NN | [citazione CAP] |`:

```
grep -cnE "^\|[[:space:]]*(R|CN|NFR)-[0-9]+\.[0-9]+[[:space:]]*\|" docs/spec_funzionale/SPEC_FUNZ_01.md
```

Output: `375`

### Riconciliazione dei due metodi

Join 1-a-1 fra le 375 definizioni del corpo e le 375 righe della tabella di mapping: **0 in mapping non in corpo, 0 in corpo non in mapping**. I due metodi indipendenti concordano su **375**.

> **Nota (autoritativa, dall'Orchestratore — ricontrollata sul file):** la ripartizione di famiglia trovata e **264 R / 82 CN / 29 NFR**. L'hint dell'handoff "262 R + 63 CN + ..." NON corrisponde al conteggio reale per-famiglia (totale invariato 375). Riportato come **osservazione**, non come discrepanza sul totale: il totale e 375 = 375 con entrambi i metodi. La spec stessa documenta un altro dettaglio di conteggio (375 vs 374, interamente in Sez.7/B5 = 36 req) alla riga `1614:docs/spec_funzionale/SPEC_FUNZ_01.md`; l'assemblato e loss-less su **375**.

### Ripartizione per blocco (colonna 2 della tabella di mapping, fonte autoritativa del blocco)

| Blocco | # req | Sezione assemblato |
|---|---|---|
| B1 | 34 | Sez.1 + Sez.2 |
| B2 | 42 | Sez.3 |
| B3 | 63 | Sez.4 |
| B4 | 61 | Sez.5 + Sez.6 |
| B5 | 36 | Sez.7 |
| B6 | 72 | Sez.9 |
| B7 | 49 | Sez.8 |
| B8 | 18 | Sez.10 |
| **TOTALE** | **375** | |

(Le sezioni 8 e 9 sono "incrociate": Sez.8 = B7, Sez.9 = B6, come da mappatura autoritativa.)

---

## 2. Indice strutturato (375 requisiti)

Una riga per ognuno dei **375** requisiti, raggruppato per blocco **B1..B8** (ordine di blocco crescente), in **ordine di documento** dentro ogni blocco. Formato:
`<req-id> | <blocco> (<id-blocco-originario>) | <riga:path> | <sintesi <=15 parole>`.
La sintesi e un'**etichetta** con parole mie: la fonte resta il `riga:path` (RM-2). `<riga:path>` punta alla **definizione nel corpo**.

### B1 — Ambito & operatore (Sez.1+Sez.2) — 34 requisiti

`R-1.1` | B1 (B1-R-01) | 28:docs/spec_funzionale/SPEC_FUNZ_01.md | Sistema genera segnali long/short sul FIB
`R-1.2` | B1 (B1-R-02) | 32:docs/spec_funzionale/SPEC_FUNZ_01.md | Strumento operativo: FIB futures mini FTSE MIB su IDEM
`R-1.3` | B1 (B1-R-03) | 36:docs/spec_funzionale/SPEC_FUNZ_01.md | Sessione di riferimento: finestra continua 8:00-22:00 CET
`R-1.4` | B1 (B1-R-04) | 41:docs/spec_funzionale/SPEC_FUNZ_01.md | Segnali emessi e processati solo dentro la finestra
`R-1.5` | B1 (B1-R-05) | 45:docs/spec_funzionale/SPEC_FUNZ_01.md | Target operativo prima formulazione: 500 punti netti giornalieri
`R-1.6` | B1 (B1-R-06) | 49:docs/spec_funzionale/SPEC_FUNZ_01.md | Target alternativo: 70% del movimento strutturale intraday
`R-1.7` | B1 (B1-R-07) | 53:docs/spec_funzionale/SPEC_FUNZ_01.md | Movimento strutturale = somma moduli swing fra pivot
`R-1.8` | B1 (B1-R-08) | 57:docs/spec_funzionale/SPEC_FUNZ_01.md | 70% applicato dal primo pivot post-apertura a chiusura
`R-1.9` | B1 (B1-R-09) | 61:docs/spec_funzionale/SPEC_FUNZ_01.md | 500 punti come soglia minima nelle sessioni mosse
`R-1.10` | B1 (B1-R-10) | 65:docs/spec_funzionale/SPEC_FUNZ_01.md | Segnali di natura intraday
`R-1.11` | B1 (B1-R-11) | 69:docs/spec_funzionale/SPEC_FUNZ_01.md | Validita segnale puo estendersi oltre sessione (multiday)
`R-1.12` | B1 (B1-R-12) | 73:docs/spec_funzionale/SPEC_FUNZ_01.md | Estensione validita non supera 2 giorni dall esecuzione
`R-1.13` | B1 (B1-R-13) | 77:docs/spec_funzionale/SPEC_FUNZ_01.md | Indici correlati per classificare il regime di mercato
`R-1.14` | B1 (B1-R-14) | 81:docs/spec_funzionale/SPEC_FUNZ_01.md | Indici correlati per validare la direzione del segnale
`R-1.15` | B1 (B1-R-15) | 85:docs/spec_funzionale/SPEC_FUNZ_01.md | Indici correlati per stimare il rischio sistemico
`R-1.16` | B1 (B1-R-22) | 91:docs/spec_funzionale/SPEC_FUNZ_01.md | Moltiplicatore FIB: 5 EUR per punto indice
`NFR-1.1` | B1 (B1-NFR-02) | 95:docs/spec_funzionale/SPEC_FUNZ_01.md | Prezzi su griglia a passo 5 punti
`CN-1.1` | B1 (B1-CN-01) | 108:docs/spec_funzionale/SPEC_FUNZ_01.md | Il sistema non esegue mai ordini autonomamente
`CN-1.2` | B1 (B1-CN-02) | 112:docs/spec_funzionale/SPEC_FUNZ_01.md | Output del sistema: pubblicazione del segnale strutturato
`CN-1.3` | B1 (B1-CN-03) | 116:docs/spec_funzionale/SPEC_FUNZ_01.md | Apertura, invio, gestione, chiusura competono solo all operatore
`CN-2.1` | B1 (B1-CN-04) | 137:docs/spec_funzionale/SPEC_FUNZ_01.md | Operatore classificato retail non professionale MiFID II
`R-2.1` | B1 (B1-R-16) | 141:docs/spec_funzionale/SPEC_FUNZ_01.md | Operatore interagisce col broker da cellulare
`R-2.2` | B1 (B1-R-17) | 145:docs/spec_funzionale/SPEC_FUNZ_01.md | Operatore opera in modo discontinuo, presenza non garantita
`NFR-2.1` | B1 (B1-NFR-01) | 149:docs/spec_funzionale/SPEC_FUNZ_01.md | Segnali interpretabili e azionabili senza presenza continua
`R-2.3` | B1 (B1-R-18) | 153:docs/spec_funzionale/SPEC_FUNZ_01.md | Size fissa: 1 contratto FIB alla volta
`CN-2.2` | B1 (B1-CN-05) | 157:docs/spec_funzionale/SPEC_FUNZ_01.md | Commissioni assunte: 5 EUR per operazione
`R-2.4` | B1 (B1-R-19) | 161:docs/spec_funzionale/SPEC_FUNZ_01.md | 5 EUR = 1 punto; ciclo completo grava 2 punti
`R-2.5` | B1 (B1-R-20) | 165:docs/spec_funzionale/SPEC_FUNZ_01.md | Stop strutturale distinto dallo stop personale dell operatore
`R-2.6` | B1 (B1-R-21) | 169:docs/spec_funzionale/SPEC_FUNZ_01.md | Rollover dello strumento riconosciuto come problematica operativa
`NFR-2.2` | B1 (B1-NFR-03) | 175:docs/spec_funzionale/SPEC_FUNZ_01.md | Infrastruttura locale: PC mobile dell operatore
`NFR-2.3` | B1 (B1-NFR-04) | 179:docs/spec_funzionale/SPEC_FUNZ_01.md | Broker e feed real-time: Directa SIM, non terzi
`R-2.7` | B1 (B1-R-23) | 183:docs/spec_funzionale/SPEC_FUNZ_01.md | Serve serie storica FIB 1-min, minimo cinque anni
`R-2.8` | B1 (B1-R-24) | 187:docs/spec_funzionale/SPEC_FUNZ_01.md | Servono dati storici/real-time DAX, EuroStoxx50, S&P futures
`R-2.9` | B1 (B1-R-25) | 191:docs/spec_funzionale/SPEC_FUNZ_01.md | Canale di pubblicazione: bot Telegram personale dell operatore

### B2 — Payload del segnale (Sez.3) — 42 requisiti

`R-3.1` | B2 (B2-R-01) | 213:docs/spec_funzionale/SPEC_FUNZ_01.md | Payload: tupla di esattamente dodici campi
`R-3.2` | B2 (B2-R-02) | 219:docs/spec_funzionale/SPEC_FUNZ_01.md | signal_id identificatore univoco assegnato all emissione, chiave primaria
`R-3.3` | B2 (B2-R-03) | 223:docs/spec_funzionale/SPEC_FUNZ_01.md | signal_id valore opaco non riutilizzabile
`R-3.4` | B2 (B2-R-04) | 227:docs/spec_funzionale/SPEC_FUNZ_01.md | Unicita signal_id su intero orizzonte operativo del motore
`R-3.5` | B2 (B2-R-05) | 233:docs/spec_funzionale/SPEC_FUNZ_01.md | timestamp_emission istante di emissione al minuto chiuso
`R-3.6` | B2 (B2-R-06) | 237:docs/spec_funzionale/SPEC_FUNZ_01.md | Riferimento orario di timestamp_emission e CET
`R-3.7` | B2 (B2-R-07) | 243:docs/spec_funzionale/SPEC_FUNZ_01.md | direction ha dominio long o short
`R-3.8` | B2 (B2-R-08) | 249:docs/spec_funzionale/SPEC_FUNZ_01.md | entry_zone banda discreta attorno al prezzo di riferimento
`R-3.9` | B2 (B2-R-09) | 253:docs/spec_funzionale/SPEC_FUNZ_01.md | Prezzo di riferimento multiplo di 5, fissato all emissione
`R-3.10` | B2 (B2-R-10) | 259:docs/spec_funzionale/SPEC_FUNZ_01.md | target_1 prezzo strutturale obiettivo, obbligatorio
`R-3.11` | B2 (B2-R-11) | 263:docs/spec_funzionale/SPEC_FUNZ_01.md | target_2 prezzo strutturale obiettivo, obbligatorio
`R-3.12` | B2 (B2-R-12) | 267:docs/spec_funzionale/SPEC_FUNZ_01.md | target_1 e target_2 sono valori distinti
`R-3.13` | B2 (B2-R-13) | 271:docs/spec_funzionale/SPEC_FUNZ_01.md | target_1 e multiplo di 5
`R-3.14` | B2 (B2-R-14) | 275:docs/spec_funzionale/SPEC_FUNZ_01.md | target_2 e multiplo di 5
`R-3.15` | B2 (B2-R-15) | 279:docs/spec_funzionale/SPEC_FUNZ_01.md | Long: target_1 maggiore del prezzo di riferimento
`R-3.16` | B2 (B2-R-16) | 283:docs/spec_funzionale/SPEC_FUNZ_01.md | Long: target_2 maggiore di target_1
`R-3.17` | B2 (B2-R-17) | 287:docs/spec_funzionale/SPEC_FUNZ_01.md | Short: target_1 minore del prezzo di riferimento
`R-3.18` | B2 (B2-R-18) | 291:docs/spec_funzionale/SPEC_FUNZ_01.md | Short: target_2 minore di target_1
`R-3.19` | B2 (B2-R-19) | 295:docs/spec_funzionale/SPEC_FUNZ_01.md | target_1 e target_2 ancorati a livelli strutturali
`R-3.20` | B2 (B2-R-20) | 299:docs/spec_funzionale/SPEC_FUNZ_01.md | target_2 informazione pubblicata, non variabile di lifecycle
`R-3.21` | B2 (B2-R-21) | 305:docs/spec_funzionale/SPEC_FUNZ_01.md | target_2_type campo con dominio structural o synthetic
`R-3.22` | B2 (B2-R-22) | 309:docs/spec_funzionale/SPEC_FUNZ_01.md | synthetic in target_2_type: livello derivato da regola
`R-3.23` | B2 (B2-R-23) | 315:docs/spec_funzionale/SPEC_FUNZ_01.md | stop_loss prezzo strutturale di stop, multiplo di 5
`R-3.24` | B2 (B2-R-24) | 319:docs/spec_funzionale/SPEC_FUNZ_01.md | Definita distanza stop = modulo p_ref meno stop_loss
`R-3.25` | B2 (B2-R-25) | 325:docs/spec_funzionale/SPEC_FUNZ_01.md | stop_type campo con dominio structural o synthetic
`R-3.26` | B2 (B2-R-26) | 329:docs/spec_funzionale/SPEC_FUNZ_01.md | synthetic in stop_type: livello derivato da regola
`R-3.27` | B2 (B2-R-27) | 333:docs/spec_funzionale/SPEC_FUNZ_01.md | stop_type non include stop manuali dell operatore
`R-3.28` | B2 (B2-R-28) | 339:docs/spec_funzionale/SPEC_FUNZ_01.md | setup_class campo con dominio directional o trade_range
`R-3.29` | B2 (B2-R-29) | 343:docs/spec_funzionale/SPEC_FUNZ_01.md | Ogni setup_class ha filtro di emissione 80 punti
`R-3.30` | B2 (B2-R-30) | 349:docs/spec_funzionale/SPEC_FUNZ_01.md | Delta_t_cromosoma parametro discreto 1..1680 minuti trading
`R-3.31` | B2 (B2-R-31) | 353:docs/spec_funzionale/SPEC_FUNZ_01.md | T_touch_max parametro discreto 5..480 minuti trading
`R-3.32` | B2 (B2-R-32) | 359:docs/spec_funzionale/SPEC_FUNZ_01.md | Semi-ampiezza banda b dominio discreto 5..40
`R-3.33` | B2 (B2-R-33) | 363:docs/spec_funzionale/SPEC_FUNZ_01.md | Semi-ampiezza b multipla di 5
`R-3.34` | B2 (B2-R-34) | 367:docs/spec_funzionale/SPEC_FUNZ_01.md | b minimo = 5 punti corrisponde a un tick
`R-3.35` | B2 (B2-R-35) | 371:docs/spec_funzionale/SPEC_FUNZ_01.md | entry_zone insieme discreto livelli da p_ref-b a p_ref+b
`R-3.36` | B2 (B2-R-36) | 375:docs/spec_funzionale/SPEC_FUNZ_01.md | Cardinalita della banda: (2b/5)+1 livelli
`R-3.37` | B2 (B2-R-37) | 379:docs/spec_funzionale/SPEC_FUNZ_01.md | Floor b minimo evita banda d ingresso nulla
`CN-3.1` | B2 (B2-CN-01) | 385:docs/spec_funzionale/SPEC_FUNZ_01.md | Vincolo geometrico obbligatorio: distanza stop maggiore di b
`CN-3.2` | B2 (B2-CN-02) | 389:docs/spec_funzionale/SPEC_FUNZ_01.md | Payload congelato all emissione, mai modificato
`CN-3.3` | B2 (B2-CN-03) | 393:docs/spec_funzionale/SPEC_FUNZ_01.md | Nessun refresh/edit che alteri payload mantenendo signal_id
`CN-3.4` | B2 (B2-CN-04) | 397:docs/spec_funzionale/SPEC_FUNZ_01.md | Vincolo segnale unico attivo: al massimo uno per istante
`CN-3.5` | B2 (B2-CN-05) | 401:docs/spec_funzionale/SPEC_FUNZ_01.md | Revisione = nuovo signal_id con nuova tupla, non edit

### B3 — State-machine & lifecycle (Sez.4) — 63 requisiti

`R-4.1` | B3 (B3-R-01) | 422:docs/spec_funzionale/SPEC_FUNZ_01.md | State machine: uno stato attivo, sei stati terminali
`R-4.2` | B3 (B3-R-02) | 425:docs/spec_funzionale/SPEC_FUNZ_01.md | target_2_hit non fa parte della state machine
`R-4.3` | B3 (B3-R-03) | 428:docs/spec_funzionale/SPEC_FUNZ_01.md | Segnale entra in active all emissione, attende evento terminale
`R-4.4` | B3 (B3-R-04) | 431:docs/spec_funzionale/SPEC_FUNZ_01.md | In active il motore osserva prezzo e calcola eventi
`R-4.5` | B3 (B3-R-05) | 434:docs/spec_funzionale/SPEC_FUNZ_01.md | target_1_hit stato terminale di successo del contratto
`R-4.6` | B3 (B3-R-06) | 437:docs/spec_funzionale/SPEC_FUNZ_01.md | target_1_hit: dopo raw touch, target_1 prima di stop/scadenza
`R-4.7` | B3 (B3-R-07) | 440:docs/spec_funzionale/SPEC_FUNZ_01.md | target_1_hit chiude definitivamente il contratto del segnale
`R-4.8` | B3 (B3-R-08) | 443:docs/spec_funzionale/SPEC_FUNZ_01.md | stopped: dopo raw touch, stop_loss prima di target_1
`R-4.9` | B3 (B3-R-09) | 446:docs/spec_funzionale/SPEC_FUNZ_01.md | invalidated: invalidazione strutturale prima del raw touch
`R-4.10` | B3 (B3-R-10) | 449:docs/spec_funzionale/SPEC_FUNZ_01.md | Invalidazione include stop attraversato pre-touch contrario all ipotesi
`CN-4.1` | B3 (B3-CN-01) | 452:docs/spec_funzionale/SPEC_FUNZ_01.md | invalidated distinto da stopped (che richiede raw touch)
`R-4.11` | B3 (B3-R-11) | 455:docs/spec_funzionale/SPEC_FUNZ_01.md | missed_target: target_1 raggiunto prima del raw touch
`R-4.12` | B3 (B3-R-12) | 458:docs/spec_funzionale/SPEC_FUNZ_01.md | Metrica missed_target ancorata a target_1, non target_2
`R-4.13` | B3 (B3-R-13) | 461:docs/spec_funzionale/SPEC_FUNZ_01.md | expired: stato terminale alla scadenza di un timer
`R-4.14` | B3 (B3-R-14) | 464:docs/spec_funzionale/SPEC_FUNZ_01.md | expired registra causa con campo, non con stati separati
`R-4.15` | B3 (B3-R-15) | 467:docs/spec_funzionale/SPEC_FUNZ_01.md | revoked: segnale superseduto da nuovo signal_id
`R-4.16` | B3 (B3-R-16) | 471:docs/spec_funzionale/SPEC_FUNZ_01.md | Revoca contestuale all emissione del nuovo segnale
`CN-4.2` | B3 (B3-CN-02) | 474:docs/spec_funzionale/SPEC_FUNZ_01.md | Nessuno stato terminale ammette transizioni uscenti
`CN-4.3` | B3 (B3-CN-03) | 477:docs/spec_funzionale/SPEC_FUNZ_01.md | Transizione target_1_hit verso revoked non esiste
`R-4.17` | B3 (B3-R-17) | 482:docs/spec_funzionale/SPEC_FUNZ_01.md | Creazione del segnale lo porta nello stato active
`R-4.18` | B3 (B3-R-18) | 485:docs/spec_funzionale/SPEC_FUNZ_01.md | Ammessa transizione active verso target_1_hit
`R-4.19` | B3 (B3-R-19) | 488:docs/spec_funzionale/SPEC_FUNZ_01.md | Ammessa transizione active verso stopped
`R-4.20` | B3 (B3-R-20) | 491:docs/spec_funzionale/SPEC_FUNZ_01.md | Ammessa transizione active verso invalidated
`R-4.21` | B3 (B3-R-21) | 494:docs/spec_funzionale/SPEC_FUNZ_01.md | Ammessa transizione active verso missed_target
`R-4.22` | B3 (B3-R-22) | 497:docs/spec_funzionale/SPEC_FUNZ_01.md | Ammessa transizione active verso expired, due cause
`R-4.23` | B3 (B3-R-23) | 500:docs/spec_funzionale/SPEC_FUNZ_01.md | Ammessa transizione active verso revoked alla sostituzione
`CN-4.4` | B3 (B3-CN-04) | 503:docs/spec_funzionale/SPEC_FUNZ_01.md | Nessuna uscita dai terminali; target_1_hit non transita
`CN-4.5` | B3 (B3-CN-05) | 506:docs/spec_funzionale/SPEC_FUNZ_01.md | Precedenza eventi a parita di timestamp definita
`R-4.24` | B3 (B3-R-24) | 511:docs/spec_funzionale/SPEC_FUNZ_01.md | raw touch: prima barra che tocca entry_zone discreta
`R-4.25` | B3 (B3-R-25) | 514:docs/spec_funzionale/SPEC_FUNZ_01.md | raw touch senza vincolo sulla direzione di provenienza
`R-4.26` | B3 (B3-R-26) | 517:docs/spec_funzionale/SPEC_FUNZ_01.md | Al raw touch il motore produce trigger_event
`R-4.27` | B3 (B3-R-27) | 520:docs/spec_funzionale/SPEC_FUNZ_01.md | raw touch sempre eseguibile, nessuna guardia post-emissione
`CN-4.6` | B3 (B3-CN-06) | 523:docs/spec_funzionale/SPEC_FUNZ_01.md | trigger_event non e uno stato; segnale resta active
`R-4.28` | B3 (B3-R-28) | 526:docs/spec_funzionale/SPEC_FUNZ_01.md | Motore non osserva il fill manuale dell operatore
`R-4.29` | B3 (B3-R-29) | 529:docs/spec_funzionale/SPEC_FUNZ_01.md | Edge prezzo gia in zona: raw touch da barra successiva
`R-4.30` | B3 (B3-R-30) | 532:docs/spec_funzionale/SPEC_FUNZ_01.md | Edge gap overnight dentro zona: non azzera raw touch
`R-4.31` | B3 (B3-R-31) | 535:docs/spec_funzionale/SPEC_FUNZ_01.md | Edge gap che salta la zona in direzione opposta
`R-4.32` | B3 (B3-R-32) | 542:docs/spec_funzionale/SPEC_FUNZ_01.md | Timer post-trigger decorre dal raw touch, expiry calcolata
`R-4.33` | B3 (B3-R-33) | 545:docs/spec_funzionale/SPEC_FUNZ_01.md | Timer post-trigger valutato sul calendario di trading
`R-4.34` | B3 (B3-R-34) | 548:docs/spec_funzionale/SPEC_FUNZ_01.md | Counter post-trigger avanza solo nei minuti di sessione
`R-4.35` | B3 (B3-R-35) | 551:docs/spec_funzionale/SPEC_FUNZ_01.md | Timer post-trigger: a expiry, segnale transita in expired
`R-4.36` | B3 (B3-R-36) | 554:docs/spec_funzionale/SPEC_FUNZ_01.md | Timer pre-trigger decorre dalla timestamp_emission
`R-4.37` | B3 (B3-R-37) | 557:docs/spec_funzionale/SPEC_FUNZ_01.md | Counter pre-trigger avanza solo nei minuti di sessione
`R-4.38` | B3 (B3-R-38) | 560:docs/spec_funzionale/SPEC_FUNZ_01.md | Scaduto pre-trigger senza touch: expired pretrigger_timeout
`R-4.39` | B3 (B3-R-39) | 563:docs/spec_funzionale/SPEC_FUNZ_01.md | Razionale timer pre-trigger: evitare attesa indefinita degenere
`NFR-4.1` | B3 (B3-NFR-01) | 570:docs/spec_funzionale/SPEC_FUNZ_01.md | Motore valuta pivot strutturali sulle barre 1-min chiuse
`NFR-4.2` | B3 (B3-NFR-02) | 573:docs/spec_funzionale/SPEC_FUNZ_01.md | Primo pivot post-apertura disponibile entro N_pivot barre
`NFR-4.3` | B3 (B3-NFR-03) | 576:docs/spec_funzionale/SPEC_FUNZ_01.md | Pivot detection su barra chiusa, non su tick intra-bar
`CN-4.7` | B3 (B3-CN-07) | 581:docs/spec_funzionale/SPEC_FUNZ_01.md | Lifecycle segnale chiuso in terminale; posizione e submacchina
`R-4.40` | B3 (B3-R-40) | 584:docs/spec_funzionale/SPEC_FUNZ_01.md | Boundary lifecycle coincide con target_1_hit
`R-4.41` | B3 (B3-R-41) | 587:docs/spec_funzionale/SPEC_FUNZ_01.md | Out-of-scope motore: execution policy, scaling, trailing, sizing
`R-4.42` | B3 (B3-R-42) | 590:docs/spec_funzionale/SPEC_FUNZ_01.md | In-scope reporting: metriche della submacchina post-target_1
`R-4.43` | B3 (B3-R-43) | 593:docs/spec_funzionale/SPEC_FUNZ_01.md | Evento d ingresso submacchina: raggiungimento di target_1_hit
`R-4.44` | B3 (B3-R-44) | 596:docs/spec_funzionale/SPEC_FUNZ_01.md | Stato iniziale submacchina: tracking_active
`R-4.45` | B3 (B3-R-45) | 599:docs/spec_funzionale/SPEC_FUNZ_01.md | Submacchina registra eventi, non stati del segnale
`CN-4.8` | B3 (B3-CN-08) | 602:docs/spec_funzionale/SPEC_FUNZ_01.md | target_2_reached e evento della submacchina, non stato
`R-4.46` | B3 (B3-R-46) | 605:docs/spec_funzionale/SPEC_FUNZ_01.md | Stato terminale submacchina: tracking_closed
`CN-4.9` | B3 (B3-CN-09) | 608:docs/spec_funzionale/SPEC_FUNZ_01.md | Submacchina non modifica mai lo stato del segnale
`CN-4.12` | B3 (B3-CN-12) | 611:docs/spec_funzionale/SPEC_FUNZ_01.md | Log della submacchina separati, referenziati dal signal_id
`CN-4.10` | B3 (B3-CN-10) | 614:docs/spec_funzionale/SPEC_FUNZ_01.md | Search space cromosoma non esteso da policy post-target_1
`R-4.47` | B3 (B3-R-47) | 617:docs/spec_funzionale/SPEC_FUNZ_01.md | Metriche submacchina entrano nella fitness multi-obiettivo GA
`R-4.48` | B3 (B3-R-48) | 620:docs/spec_funzionale/SPEC_FUNZ_01.md | Metrica primaria: profitto netto in punti FIB
`CN-4.11` | B3 (B3-CN-11) | 625:docs/spec_funzionale/SPEC_FUNZ_01.md | Vincolo unico attivo riguarda solo i segnali attivi

### B4 — Emissione & consegna Telegram (Sez.5+Sez.6) — 61 requisiti

`R-5.1` | B4 (B4-R-01) | 649:docs/spec_funzionale/SPEC_FUNZ_01.md | Motore decide se emettere prima dell emissione
`CN-5.1` | B4 (B4-CN-01) | 652:docs/spec_funzionale/SPEC_FUNZ_01.md | Dopo emissione il raw touch e sempre eseguibile
`R-5.2` | B4 (B4-R-02) | 655:docs/spec_funzionale/SPEC_FUNZ_01.md | Assenza filtri post-emissione coerente con dichiarazione d intenti
`R-5.3` | B4 (B4-R-03) | 658:docs/spec_funzionale/SPEC_FUNZ_01.md | Condizioni di emissione calcolabili sullo storico FIB
`R-5.4` | B4 (B4-R-04) | 661:docs/spec_funzionale/SPEC_FUNZ_01.md | Spread/book non in storico: condizione spread esclusa
`R-5.5` | B4 (B4-R-05) | 664:docs/spec_funzionale/SPEC_FUNZ_01.md | Operatore valuta in tempo reale le condizioni d esecuzione
`R-5.6` | B4 (B4-R-06) | 669:docs/spec_funzionale/SPEC_FUNZ_01.md | Condizione volatilita: range barra entro soglia
`R-5.7` | B4 (B4-R-07) | 672:docs/spec_funzionale/SPEC_FUNZ_01.md | Condizione liquidita: volume barra sopra soglia
`R-5.8` | B4 (B4-R-08) | 675:docs/spec_funzionale/SPEC_FUNZ_01.md | Condizione distanza: target_1/p_ref in sigma sopra soglia
`R-5.9` | B4 (B4-R-09) | 680:docs/spec_funzionale/SPEC_FUNZ_01.md | Emissione richiede filtro 80 punti del setup_class soddisfatto
`CN-5.2` | B4 (B4-CN-02) | 683:docs/spec_funzionale/SPEC_FUNZ_01.md | Filtro 80 punti vincolo assoluto, non sostituito da sigma
`CN-5.3` | B4 (B4-CN-03) | 686:docs/spec_funzionale/SPEC_FUNZ_01.md | Separazione sigma (cromosoma) e 80 punti (vincolo fisso)
`R-5.10` | B4 (B4-R-10) | 691:docs/spec_funzionale/SPEC_FUNZ_01.md | Emissione se e solo se tre condizioni piu filtro 80
`CN-5.4` | B4 (B4-CN-04) | 694:docs/spec_funzionale/SPEC_FUNZ_01.md | Se una condizione manca, candidato non viene emesso
`R-5.11` | B4 (B4-R-11) | 697:docs/spec_funzionale/SPEC_FUNZ_01.md | Non-emissione: nessun signal_id generato
`R-5.12` | B4 (B4-R-12) | 700:docs/spec_funzionale/SPEC_FUNZ_01.md | Non-emissione: nessuna pubblicazione Telegram
`R-5.13` | B4 (B4-R-13) | 703:docs/spec_funzionale/SPEC_FUNZ_01.md | Non-emissione: nessun log di emissione scritto
`R-5.14` | B4 (B4-R-14) | 706:docs/spec_funzionale/SPEC_FUNZ_01.md | Non-emissione: motore continua a valutare barre successive
`CN-5.5` | B4 (B4-CN-05) | 711:docs/spec_funzionale/SPEC_FUNZ_01.md | Dopo emissione nessuna guardia blocca il trigger_event
`R-5.15` | B4 (B4-R-15) | 714:docs/spec_funzionale/SPEC_FUNZ_01.md | Condizioni patologiche al raw touch valutate dall operatore
`R-5.16` | B4 (B4-R-16) | 717:docs/spec_funzionale/SPEC_FUNZ_01.md | Condizioni di emissione uniformi su tutta la finestra
`NFR-6.1` | B4 (B4-NFR-01) | 738:docs/spec_funzionale/SPEC_FUNZ_01.md | Canale: bot Telegram, lettura da cellulare discontinua
`NFR-6.2` | B4 (B4-NFR-02) | 741:docs/spec_funzionale/SPEC_FUNZ_01.md | Canale garantisce latenza compatibile con urgenza operativa
`CN-6.1` | B4 (B4-CN-06) | 746:docs/spec_funzionale/SPEC_FUNZ_01.md | Campi pubblicati seguono un ordine obbligatorio 1..9
`R-6.1` | B4 (B4-R-17) | 749:docs/spec_funzionale/SPEC_FUNZ_01.md | Pubblicato signal_id come chiave operativa (pos.1)
`R-6.2` | B4 (B4-R-18) | 752:docs/spec_funzionale/SPEC_FUNZ_01.md | Pubblicata direction evidenziata (pos.2)
`R-6.3` | B4 (B4-R-19) | 755:docs/spec_funzionale/SPEC_FUNZ_01.md | Pubblicato setup_class per il senso del filtro (pos.3)
`R-6.4` | B4 (B4-R-20) | 758:docs/spec_funzionale/SPEC_FUNZ_01.md | Pubblicata entry_zone come intervallo banda (pos.4)
`R-6.5` | B4 (B4-R-21) | 761:docs/spec_funzionale/SPEC_FUNZ_01.md | Pubblicati target_1 e target_2 distinti e ordinati (pos.5)
`R-6.6` | B4 (B4-R-22) | 764:docs/spec_funzionale/SPEC_FUNZ_01.md | Pubblicato stop_loss prezzo strutturale di stop (pos.6)
`R-6.7` | B4 (B4-R-23) | 767:docs/spec_funzionale/SPEC_FUNZ_01.md | Pubblicato timestamp_emission come data/ora CET (pos.7)
`R-6.8` | B4 (B4-R-24) | 770:docs/spec_funzionale/SPEC_FUNZ_01.md | Pubblicato target_2_type qualificatore del livello (pos.8)
`R-6.9` | B4 (B4-R-25) | 773:docs/spec_funzionale/SPEC_FUNZ_01.md | Pubblicato stop_type qualificatore del livello (pos.9)
`CN-6.2` | B4 (B4-CN-07) | 776:docs/spec_funzionale/SPEC_FUNZ_01.md | target_2_type e stop_type non impattano sull ingresso
`R-6.10` | B4 (B4-R-26) | 779:docs/spec_funzionale/SPEC_FUNZ_01.md | Delta_t e T_touch non nel messaggio, solo log
`CN-6.3` | B4 (B4-CN-08) | 782:docs/spec_funzionale/SPEC_FUNZ_01.md | Messaggio non contiene istruzioni di gestione attiva
`NFR-6.3` | B4 (B4-NFR-03) | 787:docs/spec_funzionale/SPEC_FUNZ_01.md | Latenza consegna entro soglia L_max definita
`NFR-6.4` | B4 (B4-NFR-04) | 790:docs/spec_funzionale/SPEC_FUNZ_01.md | Valore provvisorio L_max = 30 secondi
`CN-6.4` | B4 (B4-CN-09) | 795:docs/spec_funzionale/SPEC_FUNZ_01.md | Ogni signal_id pubblicato una sola volta (anti-duplicato)
`CN-6.5` | B4 (B4-CN-10) | 798:docs/spec_funzionale/SPEC_FUNZ_01.md | Insieme pubblicati persistito su disco contro ripubblicazioni
`R-6.11` | B4 (B4-R-27) | 801:docs/spec_funzionale/SPEC_FUNZ_01.md | Segnale sostitutivo pubblicato come messaggio separato distinto
`CN-6.6` | B4 (B4-CN-11) | 804:docs/spec_funzionale/SPEC_FUNZ_01.md | Nessun edit del messaggio Telegram precedente
`R-6.12` | B4 (B4-R-28) | 807:docs/spec_funzionale/SPEC_FUNZ_01.md | Al trigger_event pubblicata notifica separata col signal_id
`CN-6.7` | B4 (B4-CN-12) | 810:docs/spec_funzionale/SPEC_FUNZ_01.md | Notifica trigger_event distinta dal messaggio di emissione
`R-6.13` | B4 (B4-R-29) | 815:docs/spec_funzionale/SPEC_FUNZ_01.md | Errore API Telegram: il motore applica retry
`R-6.14` | B4 (B4-R-30) | 818:docs/spec_funzionale/SPEC_FUNZ_01.md | Numero massimo tentativi n_retry, provvisorio 3
`R-6.15` | B4 (B4-R-31) | 821:docs/spec_funzionale/SPEC_FUNZ_01.md | Backoff esponenziale fra i tentativi, base 2 secondi
`R-6.16` | B4 (B4-R-32) | 824:docs/spec_funzionale/SPEC_FUNZ_01.md | Fallimento finale registrato nel log, nessuna pubblicazione
`CN-6.8` | B4 (B4-CN-13) | 827:docs/spec_funzionale/SPEC_FUNZ_01.md | Fallimento finale: signal_id non aggiunto ai pubblicati
`CN-6.9` | B4 (B4-CN-14) | 830:docs/spec_funzionale/SPEC_FUNZ_01.md | Fallimento di pubblicazione tracciato nel log, non implicito
`NFR-6.5` | B4 (B4-NFR-05) | 837:docs/spec_funzionale/SPEC_FUNZ_01.md | Messaggio progettato per cellulare, attenzione limitata e discontinua
`NFR-6.6` | B4 (B4-NFR-06) | 840:docs/spec_funzionale/SPEC_FUNZ_01.md | Layout mobile-first riordina le 9 voci, nessun campo nuovo
`NFR-6.7` | B4 (B4-NFR-07) | 843:docs/spec_funzionale/SPEC_FUNZ_01.md | Messaggio testuale self-contained, leggibile senza scroll orizzontale
`R-6.17` | B4 (B4-R-33) | 848:docs/spec_funzionale/SPEC_FUNZ_01.md | Per segnale esattamente 3 notifiche standard
`R-6.18` | B4 (B4-R-35) | 851:docs/spec_funzionale/SPEC_FUNZ_01.md | Prima notifica: messaggio di emissione con le 9 voci
`R-6.19` | B4 (B4-R-36) | 854:docs/spec_funzionale/SPEC_FUNZ_01.md | Seconda notifica: trigger_event se avviene raw touch
`R-6.20` | B4 (B4-R-37) | 857:docs/spec_funzionale/SPEC_FUNZ_01.md | Notifica trigger_event distinta, non edita l emissione
`R-6.21` | B4 (B4-R-38) | 860:docs/spec_funzionale/SPEC_FUNZ_01.md | Terza notifica: messaggio di chiusura allo stato terminale
`R-6.22` | B4 (B4-R-39) | 863:docs/spec_funzionale/SPEC_FUNZ_01.md | Notifica chiusura riporta lo stato terminale finale
`R-6.23` | B4 (B4-R-40) | 866:docs/spec_funzionale/SPEC_FUNZ_01.md | Notifica chiusura riporta R_gross o n/a
`R-6.24` | B4 (B4-R-34) | 869:docs/spec_funzionale/SPEC_FUNZ_01.md | Fra notifiche standard nessun aggiornamento intermedio all operatore

### B5 — Runtime DAPI, sessione & compliance (Sez.7) — 36 requisiti

`R-7.1` | B5 (B5-R-01) | 892:docs/spec_funzionale/SPEC_FUNZ_01.md | Pipeline si connette al gateway solo in loopback
`R-7.2` | B5 (B5-R-02) | 895:docs/spec_funzionale/SPEC_FUNZ_01.md | Pipeline apre porta 10001 per datafeed realtime
`R-7.3` | B5 (B5-R-03) | 898:docs/spec_funzionale/SPEC_FUNZ_01.md | Pipeline apre porta 10003 per richieste storico
`CN-7.1` | B5 (B5-CN-01) | 901:docs/spec_funzionale/SPEC_FUNZ_01.md | Porta 10002 ordini mai aperta dalla pipeline runtime
`R-7.4` | B5 (B5-R-04) | 904:docs/spec_funzionale/SPEC_FUNZ_01.md | Riconoscimento gateway via banner con prefix-match
`NFR-7.1` | B5 (B5-NFR-01) | 907:docs/spec_funzionale/SPEC_FUNZ_01.md | APIPortSettings letto in sola lettura, dato sensibile
`CN-7.2` | B5 (B5-CN-02) | 910:docs/spec_funzionale/SPEC_FUNZ_01.md | In conflitto sul gateway la pipeline non tenta workaround
`CN-7.3` | B5 (B5-CN-03) | 913:docs/spec_funzionale/SPEC_FUNZ_01.md | Una sola connessione persistente per porta
`R-7.5` | B5 (B5-R-05) | 920:docs/spec_funzionale/SPEC_FUNZ_01.md | Pipeline sottoscrive il FIB pieno front-month su 10001
`R-7.6` | B5 (B5-R-06) | 923:docs/spec_funzionale/SPEC_FUNZ_01.md | Al boot deriva automaticamente il ticker front-month
`R-7.7` | B5 (B5-R-07) | 926:docs/spec_funzionale/SPEC_FUNZ_01.md | Codice mese Directa-IDEM: F=giugno, I=settembre
`R-7.8` | B5 (B5-R-08) | 930:docs/spec_funzionale/SPEC_FUNZ_01.md | Allo scadere del front-month sottoscrive direttamente next-month
`R-7.9` | B5 (B5-R-09) | 933:docs/spec_funzionale/SPEC_FUNZ_01.md | Al rollover registra in audit marker CONTRACT_SWITCH
`CN-7.4` | B5 (B5-CN-04) | 936:docs/spec_funzionale/SPEC_FUNZ_01.md | Switch runtime distinto dal filtro pre-expiry di training
`R-7.10` | B5 (B5-R-10) | 939:docs/spec_funzionale/SPEC_FUNZ_01.md | Runtime sul FIB pieno, operatore sul miniFIB
`R-7.11` | B5 (B5-R-11) | 944:docs/spec_funzionale/SPEC_FUNZ_01.md | Pipeline opera solo nella finestra 8:00-22:00 CET
`R-7.12` | B5 (B5-R-12) | 947:docs/spec_funzionale/SPEC_FUNZ_01.md | Fuori finestra la pipeline e in stand-by
`R-7.13` | B5 (B5-R-13) | 950:docs/spec_funzionale/SPEC_FUNZ_01.md | All apertura: banner, warm-up, sub, marker SESSION_OPEN
`R-7.14` | B5 (B5-R-14) | 953:docs/spec_funzionale/SPEC_FUNZ_01.md | Alla chiusura: marker SESSION_CLOSE, UNSUB cash, connessione mantenuta
`CN-7.5` | B5 (B5-CN-05) | 956:docs/spec_funzionale/SPEC_FUNZ_01.md | Segnale active alle 22:00 non chiuso automaticamente
`CN-7.6` | B5 (B5-CN-06) | 959:docs/spec_funzionale/SPEC_FUNZ_01.md | Fuori sessione stato active mantenuto in memoria persistente
`R-7.15` | B5 (B5-R-15) | 964:docs/spec_funzionale/SPEC_FUNZ_01.md | Cash europei DAPI come logging operativo, non feature
`R-7.16` | B5 (B5-R-16) | 967:docs/spec_funzionale/SPEC_FUNZ_01.md | Gating qualitativo dopo emissione, solo sul payload Telegram
`CN-7.7` | B5 (B5-CN-07) | 970:docs/spec_funzionale/SPEC_FUNZ_01.md | Gating qualitativo non sopprime mai l emissione
`CN-7.8` | B5 (B5-CN-08) | 973:docs/spec_funzionale/SPEC_FUNZ_01.md | Cash europeo fuori da feature, state machine, cromosoma, walk-forward
`NFR-7.2` | B5 (B5-NFR-02) | 976:docs/spec_funzionale/SPEC_FUNZ_01.md | Regole di gating in file di configurazione versionato
`R-7.17` | B5 (B5-R-17) | 979:docs/spec_funzionale/SPEC_FUNZ_01.md | Regola di gating attiva tracciata come GATING_RULE_APPLIED
`CN-7.9` | B5 (B5-CN-09) | 982:docs/spec_funzionale/SPEC_FUNZ_01.md | Stesso segnale emesso indipendentemente dalle regole di gating
`NFR-7.3` | B5 (B5-NFR-03) | 987:docs/spec_funzionale/SPEC_FUNZ_01.md | Audit log strutturato, immutabile, append-only
`R-7.18` | B5 (B5-R-18) | 990:docs/spec_funzionale/SPEC_FUNZ_01.md | Ogni evento operativo loggato con timestamp e tipologia
`R-7.19` | B5 (B5-R-19) | 993:docs/spec_funzionale/SPEC_FUNZ_01.md | Eventi lifecycle loggati distinti per stato terminale
`R-7.20` | B5 (B5-R-20) | 996:docs/spec_funzionale/SPEC_FUNZ_01.md | SIGNAL_MISSED_TARGET registra timeout_cause obbligatorio
`NFR-7.4` | B5 (B5-NFR-04) | 999:docs/spec_funzionale/SPEC_FUNZ_01.md | Banner e account code loggati su HANDSHAKE, mascherabili
`NFR-7.5` | B5 (B5-NFR-05) | 1002:docs/spec_funzionale/SPEC_FUNZ_01.md | Log accessibili almeno 90 giorni rolling
`NFR-7.6` | B5 (B5-NFR-06) | 1005:docs/spec_funzionale/SPEC_FUNZ_01.md | Log con eventi-segnale conservati permanentemente
`NFR-7.7` | B5 (B5-NFR-07) | 1008:docs/spec_funzionale/SPEC_FUNZ_01.md | Sotto soglia commissioni tollera addebito DAPI 20 EUR/mese

### B6 — Schema-dato DAPI & continuita tape (Sez.9) — 72 requisiti

`R-9.1` | B6 (B6-R-01) | 1218:docs/spec_funzionale/SPEC_FUNZ_01.md | Adapter DAPI verso bundle frozen, record per minuto
`R-9.2` | B6 (B6-R-02) | 1221:docs/spec_funzionale/SPEC_FUNZ_01.md | Adapter di normalizzazione di schema, non traduzione semantica
`R-9.3` | B6 (B6-R-03) | 1224:docs/spec_funzionale/SPEC_FUNZ_01.md | Adapter produce griglia 1-min uniforme della sessione
`R-9.4` | B6 (B6-R-04) | 1229:docs/spec_funzionale/SPEC_FUNZ_01.md | CANDLE Directa: ordine UFF;MIN;MAX;APE;V su C;L;H;O;V
`R-9.5` | B6 (B6-R-05) | 1242:docs/spec_funzionale/SPEC_FUNZ_01.md | bar_open copiato dal campo CANDLE APE
`R-9.6` | B6 (B6-R-06) | 1245:docs/spec_funzionale/SPEC_FUNZ_01.md | bar_high copiato dal campo CANDLE MAX
`R-9.7` | B6 (B6-R-07) | 1248:docs/spec_funzionale/SPEC_FUNZ_01.md | bar_low copiato dal campo CANDLE MIN
`R-9.8` | B6 (B6-R-08) | 1251:docs/spec_funzionale/SPEC_FUNZ_01.md | bar_close copiato dal campo CANDLE UFF
`R-9.9` | B6 (B6-R-09) | 1254:docs/spec_funzionale/SPEC_FUNZ_01.md | volume copiato dal campo CANDLE V
`R-9.10` | B6 (B6-R-10) | 1259:docs/spec_funzionale/SPEC_FUNZ_01.md | CANDLE non espone TickCount: schema a 9 campi
`R-9.11` | B6 (B6-R-11) | 1262:docs/spec_funzionale/SPEC_FUNZ_01.md | Realtime: tick_count = numero eventi BOOK_5 nel minuto
`R-9.12` | B6 (B6-R-12) | 1265:docs/spec_funzionale/SPEC_FUNZ_01.md | Storico CANDLERANGE: tick_count impostato a NULL
`CN-9.1` | B6 (B6-CN-01) | 1268:docs/spec_funzionale/SPEC_FUNZ_01.md | Discriminante regime: porta sorgente, non bar_synthetic
`CN-9.2` | B6 (B6-CN-02) | 1273:docs/spec_funzionale/SPEC_FUNZ_01.md | bar_synthetic booleano: trade vs no-trade, non regime
`R-9.13` | B6 (B6-R-13) | 1276:docs/spec_funzionale/SPEC_FUNZ_01.md | FIB realtime: bar_synthetic falso se almeno un BOOK_5
`R-9.14` | B6 (B6-R-14) | 1279:docs/spec_funzionale/SPEC_FUNZ_01.md | FIB storico: bar_synthetic falso se timestamp in CANDLERANGE
`R-9.15` | B6 (B6-R-15) | 1282:docs/spec_funzionale/SPEC_FUNZ_01.md | Cash realtime: bar_synthetic falso se almeno un PRICE
`CN-9.3` | B6 (B6-CN-03) | 1285:docs/spec_funzionale/SPEC_FUNZ_01.md | PRICE e BOOK_5 input dell adapter, non del canale
`R-9.16` | B6 (B6-R-16) | 1290:docs/spec_funzionale/SPEC_FUNZ_01.md | Schema PRICE realtime FIB: f4 last, f8/f9 estremi giornata
`R-9.17` | B6 (B6-R-17) | 1303:docs/spec_funzionale/SPEC_FUNZ_01.md | Riconciliazione: low/high daily da f8/f9 della CANDLE daily
`CN-9.4` | B6 (B6-CN-04) | 1306:docs/spec_funzionale/SPEC_FUNZ_01.md | f8/f9 in due schemi distinti (CANDLE daily, PRICE realtime)
`R-9.18` | B6 (B6-R-18) | 1311:docs/spec_funzionale/SPEC_FUNZ_01.md | Schema BOOK_5: 10 triple (5 BID poi 5 ASK)
`R-9.19` | B6 (B6-R-19) | 1316:docs/spec_funzionale/SPEC_FUNZ_01.md | BOOK_5: bid1 lots/orders/price ai campi 4/5/6
`R-9.20` | B6 (B6-R-20) | 1319:docs/spec_funzionale/SPEC_FUNZ_01.md | BOOK_5: ask1 lots campo 19, price campo 21
`R-9.21` | B6 (B6-R-21) | 1322:docs/spec_funzionale/SPEC_FUNZ_01.md | Mid level-1 = media di bid1_price e ask1_price
`CN-9.5` | B6 (B6-CN-05) | 1335:docs/spec_funzionale/SPEC_FUNZ_01.md | CSV runtime ha header esteso a 13 campi
`CN-9.6` | B6 (B6-CN-06) | 1338:docs/spec_funzionale/SPEC_FUNZ_01.md | Format esteso 13 campi distinto dal legacy 11 campi
`CN-9.7` | B6 (B6-CN-07) | 1341:docs/spec_funzionale/SPEC_FUNZ_01.md | tick_count intero o NULL; bar_synthetic booleano
`CN-9.8` | B6 (B6-CN-08) | 1344:docs/spec_funzionale/SPEC_FUNZ_01.md | source dominio chiuso: DIRECTA, AGG_FROM_60s, AGG_FROM_D
`CN-9.9` | B6 (B6-CN-09) | 1347:docs/spec_funzionale/SPEC_FUNZ_01.md | timestamp chiave normativa; date/time derivati di comodita
`NFR-9.1` | B6 (B6-NFR-01) | 1352:docs/spec_funzionale/SPEC_FUNZ_01.md | Replay del motore bit-exact a parita di input
`NFR-9.2` | B6 (B6-NFR-02) | 1355:docs/spec_funzionale/SPEC_FUNZ_01.md | Adapter preserva research semantics = runtime semantics
`NFR-9.3` | B6 (B6-NFR-03) | 1358:docs/spec_funzionale/SPEC_FUNZ_01.md | Replay propaga identica la distinzione reale/sintetica
`NFR-9.4` | B6 (B6-NFR-04) | 1361:docs/spec_funzionale/SPEC_FUNZ_01.md | bar_synthetic propagato come nel training, replay bit-exact
`R-9.22` | B6 (B6-R-22) | 1368:docs/spec_funzionale/SPEC_FUNZ_01.md | Al boot warm-up via CANDLERANGE, lookback 30 giorni
`CN-9.10` | B6 (B6-CN-10) | 1371:docs/spec_funzionale/SPEC_FUNZ_01.md | L_warmup = 30 giorni congelato nella metodologia
`R-9.23` | B6 (B6-R-23) | 1374:docs/spec_funzionale/SPEC_FUNZ_01.md | Fine warm-up: marker WARMUP_COMPLETE, poi steady-state
`CN-9.11` | B6 (B6-CN-11) | 1377:docs/spec_funzionale/SPEC_FUNZ_01.md | Warm-up ricalcola solo stato condizionato corrente
`R-9.24` | B6 (B6-R-24) | 1382:docs/spec_funzionale/SPEC_FUNZ_01.md | Gap entro 100 giorni recuperato via CANDLERANGE intraday
`CN-9.12` | B6 (B6-CN-12) | 1385:docs/spec_funzionale/SPEC_FUNZ_01.md | Finestra CANDLERANGE intraday limitata a circa 100 giorni
`R-9.25` | B6 (B6-R-25) | 1388:docs/spec_funzionale/SPEC_FUNZ_01.md | Barre da backfill con source BACKFILL_FROM_CANDLERANGE
`R-9.26` | B6 (B6-R-26) | 1391:docs/spec_funzionale/SPEC_FUNZ_01.md | Recupero gap idempotente: coincidenza no-op, divergenza versiona
`CN-9.13` | B6 (B6-CN-13) | 1394:docs/spec_funzionale/SPEC_FUNZ_01.md | Gap oltre 100gg: parte recuperata, complemento al fallback
`R-9.27` | B6 (B6-R-27) | 1399:docs/spec_funzionale/SPEC_FUNZ_01.md | Downtime oltre 100gg: RUNTIME_STALE_RESTART, no auto-restart
`R-9.28` | B6 (B6-R-28) | 1402:docs/spec_funzionale/SPEC_FUNZ_01.md | Re-bootstrap oltre 100gg: tre step in ordine
`CN-9.14` | B6 (B6-CN-14) | 1405:docs/spec_funzionale/SPEC_FUNZ_01.md | CANDLERANGE daily senza cut-off 100gg, cross-check retroattivo
`R-9.29` | B6 (B6-R-29) | 1408:docs/spec_funzionale/SPEC_FUNZ_01.md | Dopo re-bootstrap obbligatorio re-warm-up completo
`CN-9.15` | B6 (B6-CN-15) | 1411:docs/spec_funzionale/SPEC_FUNZ_01.md | Durante re-bootstrap il tape non alimenta inference live
`CN-9.16` | B6 (B6-CN-16) | 1414:docs/spec_funzionale/SPEC_FUNZ_01.md | Barre Portara convertite alla convenzione runtime unadjusted
`R-9.38` | B6 (B6-R-38) | 1421:docs/spec_funzionale/SPEC_FUNZ_01.md | Feature volatilita solo su barre reali
`R-9.39` | B6 (B6-R-39) | 1424:docs/spec_funzionale/SPEC_FUNZ_01.md | Feature prezzo sulla griglia uniforme inclusi minuti sintetici
`R-9.40` | B6 (B6-R-40) | 1427:docs/spec_funzionale/SPEC_FUNZ_01.md | Feature volume solo su barre reali
`R-9.41` | B6 (B6-R-41) | 1430:docs/spec_funzionale/SPEC_FUNZ_01.md | Feature struttura sulla griglia uniforme per time-indexing
`R-9.42` | B6 (B6-R-42) | 1433:docs/spec_funzionale/SPEC_FUNZ_01.md | raw touch mai dichiarato su barra sintetica
`R-9.30` | B6 (B6-R-30) | 1438:docs/spec_funzionale/SPEC_FUNZ_01.md | Fine sessione: riconciliazione canonica giornaliera come gate
`R-9.31` | B6 (B6-R-31) | 1441:docs/spec_funzionale/SPEC_FUNZ_01.md | Riconciliazione verifica integrita di schema del tape
`R-9.32` | B6 (B6-R-32) | 1444:docs/spec_funzionale/SPEC_FUNZ_01.md | Riconciliazione verifica coerenza CANDLE 1-min contro CANDLERANGE
`R-9.33` | B6 (B6-R-33) | 1447:docs/spec_funzionale/SPEC_FUNZ_01.md | Riconciliazione verifica low/high daily contro f8/f9
`CN-9.17` | B6 (B6-CN-17) | 1450:docs/spec_funzionale/SPEC_FUNZ_01.md | Cash europei: riconciliazione low/high solo da CANDLE daily
`R-9.34` | B6 (B6-R-34) | 1453:docs/spec_funzionale/SPEC_FUNZ_01.md | Verdetto riconciliazione = congiunzione dei tre check
`CN-9.18` | B6 (B6-CN-18) | 1456:docs/spec_funzionale/SPEC_FUNZ_01.md | RECONCILE_DIVERGENT blocca l emissione del giorno successivo
`CN-9.19` | B6 (B6-CN-19) | 1459:docs/spec_funzionale/SPEC_FUNZ_01.md | Riconciliazione non-mutativa sui prezzi, solo marker
`CN-9.20` | B6 (B6-CN-20) | 1462:docs/spec_funzionale/SPEC_FUNZ_01.md | Soglia theta_reconcile provvisoria non congelata, rinviata FASE-D
`R-9.35` | B6 (B6-R-35) | 1467:docs/spec_funzionale/SPEC_FUNZ_01.md | Tape confluisce in archivio canonico locale strutturato
`R-9.36` | B6 (B6-R-36) | 1470:docs/spec_funzionale/SPEC_FUNZ_01.md | CSV d archivio con header runtime esteso a 13 campi
`R-9.37` | B6 (B6-R-37) | 1473:docs/spec_funzionale/SPEC_FUNZ_01.md | Ogni archiviazione produce un manifest JSON
`CN-9.21` | B6 (B6-CN-21) | 1476:docs/spec_funzionale/SPEC_FUNZ_01.md | source d archivio estende Cap.48 con tre valori backfill
`CN-9.22` | B6 (B6-CN-22) | 1479:docs/spec_funzionale/SPEC_FUNZ_01.md | Scrittura archivio append-only, divergenza apre nuova versione
`CN-9.23` | B6 (B6-CN-23) | 1482:docs/spec_funzionale/SPEC_FUNZ_01.md | Provenienza nominale/backfill catturata da source, non bar_synthetic
`CN-9.24` | B6 (B6-CN-24) | 1485:docs/spec_funzionale/SPEC_FUNZ_01.md | Archivio del tape non e fonte di training del bundle
`CN-9.25` | B6 (B6-CN-25) | 1490:docs/spec_funzionale/SPEC_FUNZ_01.md | Ogni CSV runtime ha header con BOM UTF-8
`R-9.43` | B6 (B6-R-43) | 1493:docs/spec_funzionale/SPEC_FUNZ_01.md | Idempotenza backfill marcata VERIFIED_T3 entro orizzonte testato

### B7 — Gate di go-live (Sez.8) — 49 requisiti

`R-8.1` | B7 (B7-R-01) | 1033:docs/spec_funzionale/SPEC_FUNZ_01.md | Metrica primaria: expected net return per segnale eseguito
`R-8.2` | B7 (B7-R-02) | 1036:docs/spec_funzionale/SPEC_FUNZ_01.md | Relazione lineare net = gross meno due commissioni
`R-8.3` | B7 (B7-R-03) | 1039:docs/spec_funzionale/SPEC_FUNZ_01.md | Calcolo metriche di lifecycle sul replay OOS
`R-8.4` | B7 (B7-R-04) | 1042:docs/spec_funzionale/SPEC_FUNZ_01.md | Calcolo metriche di rischio (CVaR, max drawdown)
`R-8.5` | B7 (B7-R-05) | 1045:docs/spec_funzionale/SPEC_FUNZ_01.md | Selezione bundle subordinata a gate DSR e PBO
`R-8.6` | B7 (B7-R-06) | 1048:docs/spec_funzionale/SPEC_FUNZ_01.md | Motore accettato al go-live se DSR e PBO soddisfatti
`CN-8.1` | B7 (B7-CN-01) | 1051:docs/spec_funzionale/SPEC_FUNZ_01.md | Successo definito sul segnale, distinto dal risultato economico
`NFR-8.1` | B7 (B7-NFR-01) | 1056:docs/spec_funzionale/SPEC_FUNZ_01.md | Metriche di gate dalla fonte canonica: replay deterministico
`CN-8.2` | B7 (B7-CN-02) | 1059:docs/spec_funzionale/SPEC_FUNZ_01.md | Nessuna metrica calcolata su fill effettivi del broker
`R-8.7` | B7 (B7-R-07) | 1062:docs/spec_funzionale/SPEC_FUNZ_01.md | Finestra OOS aggregata: concatenazione dei fold completati
`R-8.8` | B7 (B7-R-08) | 1065:docs/spec_funzionale/SPEC_FUNZ_01.md | Selezione cromosoma vincente deterministica e lessicografica
`R-8.9` | B7 (B7-R-09) | 1068:docs/spec_funzionale/SPEC_FUNZ_01.md | Filtro 1: seleziona cromosomi con DSR sopra 0,95
`R-8.10` | B7 (B7-R-10) | 1071:docs/spec_funzionale/SPEC_FUNZ_01.md | Filtro 2: seleziona cromosomi con PBO sotto 0,50
`R-8.11` | B7 (B7-R-11) | 1074:docs/spec_funzionale/SPEC_FUNZ_01.md | Filtro 3: seleziona cromosomi con modulo f5 sotto 0,30
`R-8.12` | B7 (B7-R-12) | 1077:docs/spec_funzionale/SPEC_FUNZ_01.md | Filtro 4: seleziona cromosomi con IQR sotto 0,40
`R-8.13` | B7 (B7-R-13) | 1080:docs/spec_funzionale/SPEC_FUNZ_01.md | Filtro 5: seleziona cromosomi con pi t2|t1 sopra 0,30
`R-8.14` | B7 (B7-R-14) | 1083:docs/spec_funzionale/SPEC_FUNZ_01.md | Selezione finale: massimo f1 globale, tie-break definiti
`R-8.15` | B7 (B7-R-15) | 1086:docs/spec_funzionale/SPEC_FUNZ_01.md | Se nessun cromosoma sopravvive ai filtri, run fallito
`R-8.16` | B7 (B7-R-16) | 1091:docs/spec_funzionale/SPEC_FUNZ_01.md | DSR gate primario al netto di prove e momenti
`R-8.17` | B7 (B7-R-17) | 1094:docs/spec_funzionale/SPEC_FUNZ_01.md | Soglia DSR 0,95, valore provvisorio non congelato
`R-8.18` | B7 (B7-R-18) | 1099:docs/spec_funzionale/SPEC_FUNZ_01.md | PBO probabilita di overfit stimata via CSCV
`R-8.19` | B7 (B7-R-19) | 1102:docs/spec_funzionale/SPEC_FUNZ_01.md | Numero sotto-finestre S = 2F secondo regola deterministica
`R-8.20` | B7 (B7-R-20) | 1105:docs/spec_funzionale/SPEC_FUNZ_01.md | Soglia PBO sotto 0,50 gate minimo, provvisoria
`R-8.21` | B7 (B7-R-21) | 1112:docs/spec_funzionale/SPEC_FUNZ_01.md | Bootstrap stazionario a blocchi di lunghezza geometrica
`R-8.22` | B7 (B7-R-22) | 1115:docs/spec_funzionale/SPEC_FUNZ_01.md | B = 2.000 replicazioni bootstrap per gli IC
`R-8.23` | B7 (B7-R-23) | 1118:docs/spec_funzionale/SPEC_FUNZ_01.md | Calibrazione automatica L_avg via Politis-White
`NFR-8.2` | B7 (B7-NFR-02) | 1121:docs/spec_funzionale/SPEC_FUNZ_01.md | Seed PRNG bootstrap parte dell identita del bundle
`CN-8.3` | B7 (B7-CN-03) | 1126:docs/spec_funzionale/SPEC_FUNZ_01.md | Bundle frozen artefatto immutabile a sei elementi
`CN-8.4` | B7 (B7-CN-04) | 1129:docs/spec_funzionale/SPEC_FUNZ_01.md | Hash SHA-256 deterministico sui sei elementi del bundle
`CN-8.5` | B7 (B7-CN-05) | 1132:docs/spec_funzionale/SPEC_FUNZ_01.md | A ogni caricamento hash ricalcolato e confrontato
`R-8.24` | B7 (B7-R-24) | 1135:docs/spec_funzionale/SPEC_FUNZ_01.md | Sostituzione del bundle con quattro regole esplicite
`R-8.25` | B7 (B7-R-25) | 1142:docs/spec_funzionale/SPEC_FUNZ_01.md | Criterio go-live 1: DSR sopra 0,95
`R-8.26` | B7 (B7-R-26) | 1145:docs/spec_funzionale/SPEC_FUNZ_01.md | Criterio go-live 3: E[R_net] positivo con IC sopra zero
`R-8.27` | B7 (B7-R-27) | 1148:docs/spec_funzionale/SPEC_FUNZ_01.md | Criterio go-live 2: PBO sotto 0,50
`R-8.28` | B7 (B7-R-28) | 1151:docs/spec_funzionale/SPEC_FUNZ_01.md | Criterio go-live 4: modulo f5 sotto 0,30
`R-8.29` | B7 (B7-R-29) | 1154:docs/spec_funzionale/SPEC_FUNZ_01.md | Criterio go-live 5: IQR sotto 0,40
`R-8.30` | B7 (B7-R-30) | 1157:docs/spec_funzionale/SPEC_FUNZ_01.md | Criterio go-live 6: CVaR sopra soglia provvisoria
`R-8.31` | B7 (B7-R-31) | 1160:docs/spec_funzionale/SPEC_FUNZ_01.md | Criterio go-live 7: max drawdown sotto soglia provvisoria
`R-8.32` | B7 (B7-R-32) | 1163:docs/spec_funzionale/SPEC_FUNZ_01.md | Criterio go-live 8: tasso emissione nell intervallo
`R-8.33` | B7 (B7-R-33) | 1166:docs/spec_funzionale/SPEC_FUNZ_01.md | Criterio go-live 9: rho sessions sopra soglia provvisoria
`R-8.34` | B7 (B7-R-34) | 1169:docs/spec_funzionale/SPEC_FUNZ_01.md | Criterio go-live 10: verifica funzionale pipeline inference
`R-8.35` | B7 (B7-R-35) | 1172:docs/spec_funzionale/SPEC_FUNZ_01.md | Criterio go-live 11: dashboard di monitoring attiva
`R-8.36` | B7 (B7-R-36) | 1175:docs/spec_funzionale/SPEC_FUNZ_01.md | Criterio go-live 12: hash bundle valido all avvio
`CN-8.6` | B7 (B7-CN-06) | 1178:docs/spec_funzionale/SPEC_FUNZ_01.md | Procedura GO/NO-GO: GO solo se tutti i 12 OK
`R-8.37` | B7 (B7-R-37) | 1181:docs/spec_funzionale/SPEC_FUNZ_01.md | rho sessions calcolata anche separata per regime
`CN-8.7` | B7 (B7-CN-07) | 1184:docs/spec_funzionale/SPEC_FUNZ_01.md | Dieci parametri di tuning restano starting point provvisori
`R-8.38` | B7 (B7-R-38) | 1187:docs/spec_funzionale/SPEC_FUNZ_01.md | Alert persistenti su trigger paralleli innescano azione
`NFR-8.3` | B7 (B7-NFR-03) | 1190:docs/spec_funzionale/SPEC_FUNZ_01.md | Obiettivo qualitativo latenza end-to-end entro L_max
`NFR-8.4` | B7 (B7-NFR-04) | 1193:docs/spec_funzionale/SPEC_FUNZ_01.md | Post-processing PBO/bootstrap entro 15% del compute budget

### B8 — Confine / fasizzazione PHASE-2 & dipendenze aperte (Sez.10) — 18 requisiti

`R-10.1` | B8 (B8-R-01) | 1514:docs/spec_funzionale/SPEC_FUNZ_01.md | PHASE-1 dichiarata FIB-only, single-instrument
`R-10.2` | B8 (B8-R-02) | 1517:docs/spec_funzionale/SPEC_FUNZ_01.md | Convenzione cross-index dichiarata PHASE-2 senza implementazione
`CN-10.1` | B8 (B8-CN-01) | 1520:docs/spec_funzionale/SPEC_FUNZ_01.md | Strumenti PHASE-2 previsti: DAX, EuroStoxx50, S&P mini
`CN-10.2` | B8 (B8-CN-02) | 1523:docs/spec_funzionale/SPEC_FUNZ_01.md | Tre classi di estensione cross-index dichiarate non implementate
`CN-10.3` | B8 (B8-CN-03) | 1526:docs/spec_funzionale/SPEC_FUNZ_01.md | Fasizzazione istanzia parzialmente la specifica con costi noti
`CN-10.4` | B8 (B8-CN-04) | 1529:docs/spec_funzionale/SPEC_FUNZ_01.md | Cash europei sono contesto live, non cross-index PHASE-2
`CN-10.5` | B8 (B8-CN-05) | 1532:docs/spec_funzionale/SPEC_FUNZ_01.md | Convenzione tape runtime non si applica ai cross-index
`R-10.3` | B8 (B8-R-03) | 1539:docs/spec_funzionale/SPEC_FUNZ_01.md | Verifica empirica latenza Telegram dipendenza aperta (M-2)
`R-10.4` | B8 (B8-R-04) | 1543:docs/spec_funzionale/SPEC_FUNZ_01.md | Soglia theta_reconcile parametro provvisorio non congelato
`R-10.5` | B8 (B8-R-05) | 1547:docs/spec_funzionale/SPEC_FUNZ_01.md | Dieci parametri tuning Parte VI come default provvisori
`R-10.6` | B8 (B8-R-06) | 1551:docs/spec_funzionale/SPEC_FUNZ_01.md | Esito d edge materia del validator in FASE-D
`R-10.7` | B8 (B8-R-07) | 1555:docs/spec_funzionale/SPEC_FUNZ_01.md | Lookup completa codici mese Directa-IDEM dipendenza aperta
`R-10.8` | B8 (B8-R-08) | 1559:docs/spec_funzionale/SPEC_FUNZ_01.md | Abilitazione FDAX standard dipendenza aperta fuori scope
`R-10.9` | B8 (B8-R-09) | 1563:docs/spec_funzionale/SPEC_FUNZ_01.md | Scelta vendor cross-index pluriennale dipendenza aperta
`R-10.10` | B8 (B8-R-10) | 1567:docs/spec_funzionale/SPEC_FUNZ_01.md | Apertura flusso DAPI come training fuori scope
`R-10.11` | B8 (B8-R-11) | 1571:docs/spec_funzionale/SPEC_FUNZ_01.md | Migrazione legacy-esteso dei dump una-tantum di FASE-D
`R-10.12` | B8 (B8-R-12) | 1575:docs/spec_funzionale/SPEC_FUNZ_01.md | Implementazione del codice operativo fuori dalla metodologia
`R-10.13` | B8 (B8-R-13) | 1579:docs/spec_funzionale/SPEC_FUNZ_01.md | Estensione immutabilita CANDLERANGE oltre T+3 dipendenza aperta

**Verifica conteggio indice:** le righe dell'indice sono **375** (34+42+63+61+36+72+49+18 = 375). Coincide con il totale della Sezione 1. **Dichiarato: somma indice = 375.**

---

## 3. Dipendenze interne-spec (solo quelle esplicitamente dichiarate)

Scan eseguito con grep sull'intero corpo (Sez.1-10, righe < 1622, prima della tabella di mapping) cercando occorrenze del pattern `(R|CN|NFR)-\d+\.\d+` dentro il testo di ogni requisito, escludendo l'auto-riferimento dell'header. Trovate **100** menzioni cross-requisito; ognuna e stata letta in contesto per distinguere **dipendenza dichiarata** (condizione / precondizione / componente / coerenza / derivazione / instradamento scritti nel contenuto normativo) da **riferimento editoriale** (puntatori "vedi / e materia di Sez.X", note di confine "premessa citata non ri-derivata", righe-destinazione delle tabelle out-of-scope).

Comando di scan (riproducibile):

```
grep -nE "(R|CN|NFR)-[0-9]+\.[0-9]+" docs/spec_funzionale/SPEC_FUNZ_01.md | awk -F: '$1 < 1622'
```

**Dipendenze dichiarate trovate: 20** (di cui 17 a forza normativa diretta, 3 di framing dichiarato). Formato: `<req-A> -> dipende-da -> <req-B>  [riga:path della menzione]`.

### 3a. Dipendenze normative dirette (condizione / componente / coerenza / derivazione / instradamento)

- `R-1.13` -> dipende-da -> `R-2.8`  [189:docs/spec_funzionale/SPEC_FUNZ_01.md] (R-2.8 e "la precondizione-dato che abilita" R-1.13)
- `R-1.14` -> dipende-da -> `R-2.8`  [189:docs/spec_funzionale/SPEC_FUNZ_01.md] (idem)
- `R-1.15` -> dipende-da -> `R-2.8`  [189:docs/spec_funzionale/SPEC_FUNZ_01.md] (idem)
- `R-4.18` -> dipende-da -> `R-4.6`  [485:docs/spec_funzionale/SPEC_FUNZ_01.md] (transizione "con la condizione di R-4.6")
- `R-4.19` -> dipende-da -> `R-4.8`  [488:docs/spec_funzionale/SPEC_FUNZ_01.md] (transizione "con la condizione di R-4.8")
- `R-4.20` -> dipende-da -> `R-4.9`  [491:docs/spec_funzionale/SPEC_FUNZ_01.md] (transizione "con la condizione di R-4.9/R-4.10")
- `R-4.20` -> dipende-da -> `R-4.10` [491:docs/spec_funzionale/SPEC_FUNZ_01.md] (idem)
- `R-4.21` -> dipende-da -> `R-4.11` [494:docs/spec_funzionale/SPEC_FUNZ_01.md] (transizione "con la condizione di R-4.11")
- `CN-4.8` -> dipende-da -> `R-4.2`  [602:docs/spec_funzionale/SPEC_FUNZ_01.md] ("coerente con la rimozione di target_2_hit, R-4.2")
- `R-6.17` -> dipende-da -> `R-6.18` [848:docs/spec_funzionale/SPEC_FUNZ_01.md] (le 3 notifiche: (i) emissione = R-6.18)
- `R-6.17` -> dipende-da -> `R-6.19` [848:docs/spec_funzionale/SPEC_FUNZ_01.md] ((ii) trigger_event = R-6.19)
- `R-6.17` -> dipende-da -> `R-6.21` [848:docs/spec_funzionale/SPEC_FUNZ_01.md] ((iii) transizione terminale = R-6.21)
- `CN-6.8` -> dipende-da -> `CN-6.4` [828:docs/spec_funzionale/SPEC_FUNZ_01.md] ("mantiene coerente l'invariante anti-duplicato CN-6.4")
- `R-8.20` -> dipende-da -> `R-8.26` [1110:docs/spec_funzionale/SPEC_FUNZ_01.md] (nota framing in R-8.20: bootstrap "produce gli IC usati dal gate R-8.26")
- `NFR-8.3` -> dipende-da -> `R-8.34` [1190:docs/spec_funzionale/SPEC_FUNZ_01.md] (NFR-8.3 "componente di R-8.34")
- `R-9.25` -> dipende-da -> `R-9.14` [1388:docs/spec_funzionale/SPEC_FUNZ_01.md] ("bar_synthetic derivato dalla regola Cap.49, R-9.14")
- `CN-9.13` -> dipende-da -> `R-9.27` [1394:docs/spec_funzionale/SPEC_FUNZ_01.md] ("instradandolo al fallback di restart >100gg, R-9.27")

### 3b. Dipendenze di framing dichiarato (purpose-rispetto-al-gate scritto nel testo)

- `R-8.21` -> dipende-da -> `R-8.26` [1110:docs/spec_funzionale/SPEC_FUNZ_01.md] ("R-8.21/22/23 ne fissano procedura ... a corredo del gate" R-8.26)
- `R-8.22` -> dipende-da -> `R-8.26` [1110:docs/spec_funzionale/SPEC_FUNZ_01.md] (idem)
- `R-8.23` -> dipende-da -> `R-8.26` [1110:docs/spec_funzionale/SPEC_FUNZ_01.md] (idem)

### 3c. Riferimenti editoriali NON conteggiati come dipendenze (per trasparenza)

Le restanti ~80 menzioni cross-requisito sono **puntatori editoriali** e NON dipendenze normative dichiarate: rinvii "vedi Sez.X / e materia di Sez.X (R-y)", note di confine "premessa di Sez.X (R-y), citata non ri-derivata" (es. 39, 718, 921, 940, 957, 994, 1549), righe-destinazione delle tabelle out-of-scope (es. 202, 1014, 1016-1017, 1199, 1202-1204, 1502-1504), e cross-ref di tracciabilita/valore (es. 171, 189 nella parte "vedi", 301, 345, 351-355, 403, 469, 518, 521, 540, 626, 802, 835, 841, 855, 861-864, 902, 1140, 1169, 1175, 1199, 1277, 1299-1320, 1400, 1463, 1491, 1494, 1502-1533, 1580). Sono **citate ma non promosse** a dipendenza: il testo le presenta come premesse gia consolidate o rinvii di lettura, non come prerequisiti/ordinamenti che vincolano l'uno all'altro nel senso operativo. **Non dedotte** dipendenze non scritte (RM-1/RM-2).

> Sintesi: **20 dipendenze inter-req dichiarate** (17 normative + 3 framing). Non e vero che "nessuna dipendenza inter-req e dichiarata": ce ne sono, elencate sopra con riga.

---

## 4. Aree-tema (descrittive, NON architetturali)

I raggruppamenti funzionali **come sono nella spec**: nomi e perimetro dei blocchi B1..B8 dalle intestazioni di Sezione dell'assemblato e dalla tabella del README in `docs/spec_funzionale/storico/README.md` (righe 9-16). Nessun modulo software, nessun DAG, nessun sequenziamento/priorita.

| Blocco | Tema (README + intestazioni Sezione) | Sezioni assemblato | Perimetro / materia |
|---|---|---|---|
| **B1** | Ambito & operatore | Sez.1 + Sez.2 | Obiettivo di prodotto, ambito, vincolo "solo emissione"; destinatario retail, modalita di consumo, canale e infrastruttura. [22, 131:docs/spec_funzionale/SPEC_FUNZ_01.md] |
| **B2** | Payload del segnale | Sez.3 | I dodici campi della tupla del segnale, domini, vincoli geometrici e invarianti di immutabilita. [207:docs/spec_funzionale/SPEC_FUNZ_01.md] |
| **B3** | State-machine & lifecycle | Sez.4 | Stato attivo + sei terminali, transizioni, raw touch/trigger, timer pre/post, submacchina post-target_1. [416:docs/spec_funzionale/SPEC_FUNZ_01.md] |
| **B4** | Emissione & consegna Telegram | Sez.5 + Sez.6 | Regola di emissione (condizioni + filtro 80pt); contratto del messaggio Telegram, layout mobile-first, retry, 3 notifiche. [641, 730:docs/spec_funzionale/SPEC_FUNZ_01.md] |
| **B5** | Runtime DAPI, sessione & compliance | Sez.7 | Connessione gateway Darwin (porte/loopback), front-month/rollover, finestra di sessione, gating qualitativo, audit log. [884:docs/spec_funzionale/SPEC_FUNZ_01.md] |
| **B6** | Schema-dato DAPI & continuita tape | Sez.9 | Adapter DAPI->bundle, schemi CANDLE/PRICE/BOOK_5, tick_count/bar_synthetic, warm-up, recupero gap, riconciliazione, archivio. [1210:docs/spec_funzionale/SPEC_FUNZ_01.md] |
| **B7** | Gate di go-live | Sez.8 | Metrica primaria E[R_net], filtri DSR/PBO/f5/IQR/pi, 12 criteri di go-live, bundle frozen + hash. [1025:docs/spec_funzionale/SPEC_FUNZ_01.md] |
| **B8** | Confine / fasizzazione PHASE-1/PHASE-2 & dipendenze aperte | Sez.10 | Confine FIB-only PHASE-1 vs cross-index PHASE-2 dichiarato non implementato; dipendenze aperte verso FASE-D. [1508:docs/spec_funzionale/SPEC_FUNZ_01.md] |

> Le aree sono **descrittive** (cosa contiene ogni blocco nella spec), non una proposta di architettura: la pianificazione e demandata al Planner.

---

## In coda — conteggio trovato vs atteso, discrepanze, SHA

- **Conteggio trovato:** 375 requisiti (264 R + 82 CN + 29 NFR). **Atteso:** 375. **Discrepanza sul totale: NESSUNA.**
- **Righe nell'indice (Sez.2):** 375 (coincide col totale).
- **Dipendenze inter-req dichiarate:** 20 (17 normative + 3 framing).
- **Osservazione (non-discrepanza):** la ripartizione per-famiglia reale (264/82/29) differisce dall'hint "262 R + 63 CN" dell'handoff; il totale resta 375 con due metodi indipendenti. La spec documenta a riga 1614 la propria nota di conteggio interna (375 vs 374, risolta a 375).
- **SHA del commit:** <da inserire al commit dall'Orchestratore>
