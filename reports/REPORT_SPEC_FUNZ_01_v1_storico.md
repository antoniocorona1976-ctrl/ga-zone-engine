### REPORT SUPERVISORE — SPEC-FUNZ-01

**Task**: SPEC-FUNZ-01 — Specifica funzionale del prodotto-segnale FIB (PHASE-1)
**Stato**: COMPLETATO

> **Natura non-CAP**: SPEC-FUNZ-01 e' una specifica funzionale / di prodotto, NON un capitolo metodologico ne' una Parte della metodologia v2. Adattamenti rispetto al flusso CAP-XX (da prompt di invocazione): output in `docs/spec_funzionale/` (cartella nuova), nessuna modifica a `docs/methodology_v2/00_indice.md`, commit tag `[SPEC-FUNZ-01]`, segnale `READY_FOR_REVIEW` per Review formale piena adattata.

---

#### Cosa e' stato prodotto

| File | Operazione | Descrizione |
|------|-----------|-------------|
| `docs/spec_funzionale/SPEC_FUNZ_01.md` | CREATE (cartella nuova) | Specifica funzionale, 10 sezioni + matrice di tracciabilita' a 36 righe + self-review Developer. ~6.440 parole (~13-15 pp). Consolida la metodologia v2 (Cap.1-65, tutte PASS) in 36 requisiti: 24 `R`, 5 `NFR`, 7 `CN`. |
| `reports/REPORT_SPEC_FUNZ_01.md` | CREATE | Questo report supervisore (5 sezioni + tabella verifica AC). |
| `tasks/DEV_STATUS.md` | EDIT | `READY_FOR_REVIEW` dopo pre-consegna OK (adattata al non-CAP). |

**NON modificati** (vincoli espliciti del task): `docs/methodology_v2/00_indice.md`, `tasks/STATO_CORRENTE.md`, `tasks/CARRYOVER.md`, `tasks/QUESTIONS.md`, `tasks/ACTIVE_TASK.md` (gia' committato dall'Orchestratore). **Non committati** file di noise (`.claude/settings.json`, `build/`, PDF, `.lock`).

---

#### Ipotesi di partenza

Criterio di valore del track (reinterpretazione dell'"orientamento al GA", da task card): SPEC-FUNZ-01 e' un documento di **prodotto/requisiti**, non una modifica al comportamento del GA. Ogni requisito traccia simultaneamente a (a) un **valore operativo / di prodotto reale** per l'operatore retail FIB E (b) un **capitolo della metodologia v2** di origine. Nessuna analisi "impatto sul ranking dei cromosomi" e' forzata.

Cosa il documento intende ottenere: **consolidare** la metodologia v2 chiusa (dispersa su 65 capitoli, non leggibile da un esterno) in un documento di requisiti **cantierabile da FASE-D** e **mostrabile fuori dal team metodologico** (consulenza legale MiFID II, valutatori AWS, fornitori Portara/CQG e bot Telegram). Fa da **ponte** fra metodologia chiusa e implementazione FASE-D. Incardina M-2 (latenza Telegram) come NFR del prodotto e ne dichiara la verifica empirica come dipendenza aperta, senza risolverla.

---

#### Decisioni rilevanti prese durante lo sviluppo

1. **36 requisiti, numerazione progressiva per tipo** (R-1..R-24 funzionali, NFR-1..NFR-5 qualita'/quantitativi, CN-1..CN-7 compliance). Ogni requisito ha ID univoco, valore operativo dichiarato e tracciabilita' a capitolo. Scelta: numerazione globale progressiva (non per-sezione) per facilitare il riferimento da FASE-D.
2. **M-2 opzione (a) del Planner**: NFR-1 fissa il requisito $L_{max}=30$ s come SLA consumer-facing; la verifica empirica resta dipendenza aperta Appendice E / FASE-D, dichiarata esplicitamente in Sez. 5.3 e Sez. 10.3. Un documento di prodotto deve dichiarare lo SLA di consegna; non dichiararlo lo lascerebbe amputato.
3. **Esempi numerici coerenti col layout mobile chiuso** (Cap.29 Parte VI): il payload e il messaggio Telegram di Sez. 3.3 / 5.2 riusano l'esempio normativo di `CAP_06_parte_VI.md:176` (prezzi multipli di 5, 80pt rispettato, $d_{stop}>b$). Nessun valore inventato.
4. **Distinzione 9 voci pubblicate vs 10 campi payload consumer-facing** (Sez. 3.1): il messaggio Telegram pubblica 9 voci (Cap.9.2 Iterazione 5), la tupla del segnale ha 12 campi formali di cui 2 timer non pubblicati; la tabella di prodotto elenca i 10 campi consumer-facing (timer esclusi). Risolve la potenziale ambiguita' "9 vs 12" senza contraddire i CAP.
5. **Capitoli non tracciati motivati esplicitamente** (Sez. 10.5): Cap.4, 12-26, 27, 30, 35, 37-44, 45/50/55/57/58/63/64, 56/65 esclusi dalla matrice con motivazione "implementazione metodologica interna / tabelle-registro / training, opaca al consumatore". Richiesto da AC-G5.
6. **Self-review Developer inclusa** (opzione consigliata dal task card, non sostitutiva della Review formale piena): documenta diligenza RM-1/2/3 e i file letti, con riverifica token-per-token delle 3 citazioni di codice.

##### Decoder/convenzioni esistenti nel repo consultati (RM-2 — citazioni codice riverificate con Read)

Le citazioni `[CODICE-ESISTENTE]` sono autoritative dal task card (eredita' #15) e sono state **riverificate con Read** prima della stesura (la spec NON le ha scoperte ex novo via grep, NON ha riscritto alcun decoder — e' documento di prodotto):

- `[CODICE-ESISTENTE scripts/export_directa_history_parametric.py:467-481]` — `parse_directa_candle`, schema CANDLE `C;L;H;O` (`kind, symbol, ymd, hms, uff, min_, max_, ape, qty = parts[:9]`; commento r477 `# UFF, MIN, MAX, APE => close, low, high, open`; `close_v=Decimal(uff)`/`low_v=Decimal(min_)`/`high_v=Decimal(max_)`/`open_v=Decimal(ape)`). **CONFERMATO token-per-token** (Read r465-484).
- `[CODICE-ESISTENTE scripts/export_directa_history_parametric.py:605-617]` — header CSV legacy 11 campi (`symbol, timeframe, timestamp, date, time, open, high, low, close, volume, source`, senza `tick_count`/`bar_synthetic`). **CONFERMATO token-per-token** (Read r603-620).
- `[CODICE-ESISTENTE scripts/export_directa_history_parametric.py:61]` — `DEFAULT_INTRADAY_MAX_DAYS = 100`. Autoritativo dal task card + `[DOC-INTERNO CAP_10_parte_10.md:230]`; non riletto in questa sessione ma citato come fatto chiuso.

Citazioni di codice totali nel documento: **3 distinte** (<=5, AC-G3 OK).

---

#### Misura prima/dopo

Adattata onestamente al greenfield (non sono metriche del GA):

| Metrica | Prima | Dopo | Delta |
|---------|-------|------|-------|
| Requisiti di prodotto consolidati e tracciati | 0 (dispersi e impliciti nei 65 capitoli metodologici, non leggibili da un esterno) | 36 (24 R + 5 NFR + 7 CN), ognuno con ID + valore operativo + capitolo di origine | +36 |
| Righe di matrice tracciabilita' requisito->metodologia | 0 (nessuna matrice esistente) | 36 righe (>=30, AC-G5) | +36 |
| Documento di prodotto mostrabile fuori dal team metodologico | assente | 1 (`SPEC_FUNZ_01.md`, ~13-15 pp) | +1 |
| M-2 (latenza Telegram) incardinato come requisito di prodotto | OPEN, solo carryover senza requisito esplicito | NFR-1 fissato + dipendenza empirica dichiarata aperta (M-2 resta OPEN) | requisito incardinato; verifica empirica invariata (OPEN) |
| Dipendenze aperte FASE-D censite e tracciate | implicite/sparse | 6 voci esplicite (Sez. 10.3) | +6 |

---

#### Verifica esplicita degli Acceptance Criteria

**AC di sezione** (sintesi; evidenza nel file):

| AC sezione | Esito | Evidenza (file:rif) |
|---|---|---|
| Sez.1 — valore <=3 righe + >=3 R-PERIM + CN-1 "solo emissione" + out-of-scope chiuso | OK | SPEC_FUNZ_01.md Sez.1 (proposta di valore, R-1/2/3, CN-1, sez.1.3) |
| Sez.2 — persona >=5 attributi + >=2 R contesto + stakeholder | OK | SPEC_FUNZ_01.md Sez.2 (sez.2.1 5 attributi, R-4/R-5, sez.2.2) |
| Sez.3 — tabella payload >=9 voci + tipo/dominio/vincoli/cap + immutabilita' + segnale unico + 80pt + esempio | OK | SPEC_FUNZ_01.md Sez.3 (tabella 10 voci sez.3.1, R-6/7/8/9, esempio sez.3.3) |
| Sez.4 — diagramma 1+6 + ogni terminale spiegato + trigger_event R+CN + distinzione segnale/position | OK | SPEC_FUNZ_01.md Sez.4 (sez.4.1 diagramma, sez.4.2, R-10/CN-2, R-11) |
| Sez.5 — esempio emissione + esempio trigger + NFR L_max 30s + M-2 dichiarata + >=3 R | OK | SPEC_FUNZ_01.md Sez.5 (sez.5.2 due esempi, NFR-1, blocco M-2, R-12/13/14) |
| Sez.6 — >=5 R operativi + rollover D-9-NB2 con esempio FIB6F->FIB6I 2026-06-19 | OK | SPEC_FUNZ_01.md Sez.6 (R-15..R-19, sez.6.2 esempio rollover) |
| Sez.7 — KPI >=6 + DSR/PBO gate + checklist <=12 + M-16 metadato | OK | SPEC_FUNZ_01.md Sez.7 (tabella 8 KPI sez.7.1, NFR-2/3, checklist 12 sez.7.3, blocco M-16) |
| Sez.8 — CN segnale informativo + CN separazione + CN retention valori + catalogo eventi riferito | OK | SPEC_FUNZ_01.md Sez.8 (CN-3, CN-4, CN-5 90gg+permanente, sez.8.2 catalogo) |
| Sez.9 — tabella dipendenze >=6 + legacy 11 vs esteso 13 + >=2 R tape + riconciliazione bloccante | OK | SPEC_FUNZ_01.md Sez.9 (tabella 6 dip. sez.9.1, R-20 13vs11, R-20/21, R-23) |
| Sez.10 — PHASE-1 vs PHASE-2 + >=5 dipendenze aperte + matrice >=30 righe + capitoli non tracciati motivati | OK | SPEC_FUNZ_01.md Sez.10 (sez.10.1, sez.10.3 6 voci, sez.10.4 36 righe, sez.10.5) |

**AC globali AC-G1..AC-G15**:

| AC-ID | Criterio (estratto) | Esito | Evidenza (file:rif) |
|-------|---------------------|-------|---------------------|
| AC-G1 | RM-1 — no nuovi "verificato X" di prima istanza; ogni asserzione richiama un CAP chiuso etichettato | OK | Nessun "verificato X" nuovo; etichette `[DOC-INTERNO]`/`[CODICE-ESISTENTE]` ovunque; self-review (a). I richiami a fatti empirici (CANDLE, F/I, PRICE/BOOK_5) sono richiami ad audit/decoder gia' chiusi, non asserzioni nuove. |
| AC-G2 | RM-3 — fonti esterne `[WIKI-HINT, da verificare]`; nessuna conclusione solo livello-4; wiki Directa con avvertenza | OK | Nota di lettura in testa (wiki inesatta su CANDLE); `[WIKI-HINT]` su MiFID II (Sez.2/8). Nessuna asserzione strutturale wiki-only. |
| AC-G3 | RM-2 — citazioni codice puntuali e verificabili, <=5 | OK | 3 citazioni `[CODICE-ESISTENTE export_directa_history_parametric.py:467-481 / :605-617 / :61]`, riverificate token-per-token (REPORT Decisioni). |
| AC-G4 | Ogni requisito ha colonna "capitolo v2 di origine" non vuota | OK | Mini-tabelle per ogni sezione + matrice sez.10.4: 36/36 righe con capitolo non vuoto. |
| AC-G5 | Matrice sez.10 >=30 righe + capitoli non tracciati motivati | OK | Matrice sez.10.4 = 36 righe; sez.10.5 "Capitoli non tracciati e motivazione" (Cap.4,12-26,27,30,35,37-44,45/50/55/57/58/63/64,56/65). |
| AC-G6 | Nessuna contraddizione con CAP chiusi | OK | Punti rischiosi verificati per scrupolo contro i CAP: solo emissione (Cap.1), 1+6 state machine (Cap.7), target_2 informazione (Q-05/Cap.6), 80pt (Cap.5/8), tick 5pt (Cap.6), sessione 8-22 (Cap.1/52), M-2 OPEN (CARRYOVER:21), L_warmup=30gg (D-9-NB4), riconciliazione bloccante vs Cap.30 (D-10-3). Tutti coerenti. |
| AC-G7 | Ogni requisito ha valore operativo/di prodotto dichiarato | OK | Ogni R/NFR/CN ha campo "*Valore operativo*" o "*Valore di prodotto*" nella sezione di origine. |
| AC-G8 | M-2 NFR latenza presente + dichiarata dipendenza aperta Appendice E/FASE-D | OK | NFR-1 Sez.5.3 + blocco "M-2 OPEN — dipendenza aperta" + Sez.10.3 voce 1. Verifica empirica NON risolta (resta carryover). |
| AC-G9 | Out-of-scope sistematico per sezione + quadro complessivo sez.10 | OK | Ogni sezione 1-10 ha riga "Out-of-scope Sezione N"; sez.10.5 quadro complessivo. |
| AC-G10 | Lunghezza 12-16 pp | OK | ~6.440 parole ~ 13-15 pp (entro target; deviazione <20%). |
| AC-G11 | Italiano formale, tecnico, conciso | OK | Registro coerente coi CAP v2; nessun paragrafo divulgativo non necessario. |
| AC-G12 | Formato: `docs/spec_funzionale/SPEC_FUNZ_01.md` (nuova) + `reports/REPORT_SPEC_FUNZ_01.md`; tag `[SPEC-FUNZ-01]`; indice NON modificato | OK | File creati nei path corretti; commit tag `[SPEC-FUNZ-01]`; `00_indice.md` non toccato. |
| AC-G13 | Reviewer applica RM-1 a se' stesso | N/A (Reviewer) | Vincolo per il Reviewer v1, non per il Developer. Citato per completezza. |
| AC-G14 | Reviewer non riapre CAP chiusi | N/A (Reviewer) | Vincolo per il Reviewer v1. Il Developer ha usato i CAP come autoritativi (nessuna contraddizione, AC-G6). |
| AC-G15 | Reviewer applica RACC-METODO-2 su schemi esterni citati | N/A (Reviewer) | Vincolo per il Reviewer v1. La spec NON ridichiara schemi DAPI: li cita come chiusi (CANDLE via decoder :467-481; PRICE/BOOK_5 via audit RM CLI; legacy CSV :605-617). |

**Onesta'**: nessun AC e' PARZIALE o MANCA. AC-G13/14/15 sono vincoli per il **Reviewer**, marcati N/A lato Developer (non sono auto-valutazioni del proprio lavoro). Tutti gli AC di sezione e AC-G1..AC-G12 sono OK con evidenza puntuale.

---

#### Domande aperte per il Planner

Nessuna. Il task card e' dettagliato e non ha lasciato ambiguita' non risolvibili dai documenti; nessuna Q-XX aperta (coerente con il vincolo del task: il Developer NON apre Q-XX di sua iniziativa). M-2 resta dipendenza aperta dichiarata (non e' una domanda al Planner: e' carryover gia' deciso opzione (a)).

---

#### Criterio di rollback

SPEC-FUNZ-01 e' un documento di consolidamento, non una modifica al motore: il rollback non comporta re-training ne' impatto sul bundle frozen. Condizioni che giustificano il rollback (ritorno a versione precedente o re-stesura):

- La Review trova una **contraddizione reale** fra un requisito della spec e un fatto/decisione chiusa in un CAP (BUG REALE AC-G6): si corregge il requisito (la spec e' sempre la parte che cede, mai il CAP — AC-G14).
- La Review trova un **requisito senza tracciabilita' a metodologia o senza valore operativo** (BUG REALE AC-G4/AC-G7): si aggiunge la tracciabilita'/valore o si rimuove il requisito.
- La Review trova **citazioni codice non verificabili** (BUG REALE AC-G3): si correggono.
- Deviazione di lunghezza >=40% dal target 12-16 pp (AC-G10 BUG REALE): la spec e' amputata o bloated -> re-bilanciamento.

Il rollback e' sempre **chirurgico** sul requisito o sulla sezione interessata, mai re-stesura integrale, salvo FAIL strutturale.

---

## Iterazione 2 — risposta ai finding di Review

**Contesto.** Review v1 = **PASS** (`d8a40a0`): 0 bloccanti, 0 BUG REALE. I 3 finding sono **NEUTRO** (igiene-citazione), approvati dal supervisore come micro-pass opzionale. Patch **chirurgiche** su `docs/spec_funzionale/SPEC_FUNZ_01.md` (solo le 3 zone OM-1/2/3); nessuna re-stesura, nessuna altra modifica. **Impatto sulla correttezza: nullo** (la spec era gia' tracciabilmente corretta); **impatto: +precisione di citazione** (puntatore a riga esatta dell'asserzione invece che a riga di intestazione capitolo / adiacente).

**Vincolo RM-1 applicato.** Ogni nuovo numero di riga e' stato verificato con `Read` del file di destinazione PRIMA di scriverlo: la riga deve contenere davvero il costrutto citato. Nessun target ha richiesto fallback al capitolo (tutti hanno risolto alla riga esatta).

### OM-1 — 6 numeri di riga corretti (puntatore header/adiacente → riga esatta)

Tutti su `SPEC_FUNZ_01.md`. Ogni mapping confermato con `Read` del CAP di destinazione.

| # | Citazione | Prima | Dopo | Riga spec | Contenuto reale della riga di destinazione (verificato con Read) |
|---|---|---|---|---|---|
| 1 | `CAP_10_parte_10.md` (Sez.9.2, invariante research=runtime esteso al tape) | `:11` (header "Capitolo 57") | `:5` | 384 | r5 = "l'invariante `research semantics = runtime semantics` ... e' esteso ... all'**intero ciclo di vita del tape**". MATCH col testo spec "fino all'intero ciclo di vita del tape". |
| 2 | `CAP_10_parte_10.md` (R-22, Cap.59 limite ~100gg) | `:74` (header "Capitolo 59") | `:76` | 390 | r76 = "Questo capitolo norma il recupero gap di durata $\leq \sim 100$gg ... Il limite e' stabilito empiricamente". MATCH. |
| 3 | `CAP_10_parte_10.md` (R-22, Cap.61 fallback Portara) | `:151` (header "Capitolo 61") | `:161` | 390 | r161 = "**Step C — Fallback Portara.** Se ne' archivio locale ne' `CANDLERANGE` daily coprono ... fallback all'archivio Portara/CQG". E' la riga esatta del costrutto "fallback Portara" nel corpo del capitolo. MATCH. |
| 4 | `CAP_10_parte_10.md` (Sez.10.1, PHASE-2 fuori scope) | `:226` (header "Capitolo 64") | `:236` | 417 | r236 = "**Convenzione cross-index PHASE-2** ... Parte 10 NON si applica ai cross-index PHASE-2 (fuori scope PHASE-1)". MATCH. |
| 5 | `CAP_10_parte_10.md` (Sez.10.3 voce 4, riavvio Darwin mezzanotte) | `:234` (estensione immutabilita' barre, riga adiacente) | `:233` | 428 | r233 = "**Riavvio Darwin mezzanotte** — osservazione empirica diretta: residuo Empirico-CLI di Parte 9 Cap.50 Gap-3". MATCH col costrutto "riavvio Darwin mezzanotte". |
| 6 | `CAP_07_parte_VII.md` (NFR-4, tag "AC-GO-4") | `:574` (AC-GO-3, expected net return) | `:576` | 301 | r576 = "**AC-GO-4 — Lifecycle stabile cross-regime.** $|f_5^{global}(\theta^*)| < \theta_{f_5} = 0{,}30$". MATCH col tag (AC-GO-4) gia' presente nella spec. |

**Verifica anti-regressione**: `grep` sulla spec dei 5 vecchi numeri `CAP_10:11/74/151/226/234` e `CAP_07:574` → **0 occorrenze residue** (nessuna citazione stale lasciata). I nuovi 6 numeri tutti presenti. La citazione `CAP_10_parte_10.md:230` (DEFAULT_INTRADAY_MAX_DAYS / migrazione legacy, Sez.9.3 + self-review (b)) NON e' nella lista OM-1 ed e' stata **lasciata invariata** (corretta).

**Impatto OM-1**: nullo sulla tracciabilita' sostanziale (gia' risolveva al capitolo corretto col costrutto presente); +precisione "riga-esatta", ora allineata allo standard di citazione tenuto nelle Sez. 1-8.

### OM-2 — R-17 (Sez.6): rimosso "per direzione" dal titolo

- **Prima** (spec r256): "**R-17 — Singolo segnale attivo per direzione.** Vincolo $|\mathcal{A}(t)|\le 1$: nessuna politica multi-segnale concorrente."
- **Dopo** (spec r256): "**R-17 — Singolo segnale attivo.** Vincolo $|\mathcal{A}(t)|\le 1$: nessuna politica multi-segnale concorrente."
- **Razionale**: il vincolo chiuso e' $|\mathcal{A}(t)|\le 1$ **globale** (`[DOC-INTERNO CAP_02_parte_II.md:81]`; cfr. CAP_02:87 "elimina tutte le politiche multi-segnale concorrente"), non "uno per direzione". La locuzione "per direzione", isolata, poteva suggerire $|\mathcal{A}|\le 2$. La forma corretta era gia' enunciata **in-linea** ed e' stata **mantenuta**; rimosso solo il wording lasco dal titolo, allineandolo a R-7 (Sez.3.2) che era gia' senza "per direzione". Il riferimento autoritativo `CAP_02_parte_II.md:81` resta invariato.
- **Impatto**: nullo sulla correttezza (il constraint corretto gia' governava in-linea, AC-G6 reggeva); +coerenza terminologica titolo↔formula e R-17↔R-7.

### OM-3 — Sez.9.2: aggiunta ancora puntuale STATO_CORRENTE:76 per la numerazione `fN` di PRICE

- **Prima** (spec r384): "...il feed cash usa `PRICE` (schema realtime `f4=last`/`f6=volume_cum`/`f8=day_low`/`f9=day_high`, M-9 `[DOC-INTERNO CAP_09_parte_9.md:94]`)."
- **Dopo** (spec r384): "...il feed cash usa `PRICE` (schema realtime `f4=last`/`f6=volume_cum`/`f8=day_low`/`f9=day_high`, M-9 `[DOC-INTERNO tasks/STATO_CORRENTE.md:76]`, descritto anche in `[DOC-INTERNO CAP_09_parte_9.md:94]`)."
- **Razionale**: l'indicizzazione `fN` esatta proviene da **M-9 in `tasks/STATO_CORRENTE.md:76`** (verificato con Read: r76 = "**Schema PRICE realtime (DAPI)** [PROVA-EMPIRICA 2026-06-01 W2, CAP-DATA-02]: `PRICE;<tk>;<HH:mm:ss>;<f4=last>;<f5>;<f6=volume_cum>;<f7>;<f8=day_low>;<f9=day_high>`"), riprodotta dalla spec token-per-token. Aggiunta l'**ancora puntuale** alla numerazione `fN`; **mantenuto** il richiamo descrittivo a `CAP_09_parte_9.md:94` (che riporta lo schema in forma descrittiva, coerente con M-9), come richiesto dal finding.
- **Impatto**: nullo sulla correttezza (fatto gia' corretto e tracciabile); +precisione di provenienza (ancora alla riga sorgente della numerazione `fN`).

### Misura prima/dopo (Iterazione 2)

| Metrica | Prima (v1) | Dopo (v2) | Delta |
|---|---|---|---|
| Citazioni `[DOC-INTERNO]` che puntano a riga di header/adiacente invece che alla riga esatta (OM-1) | 6 | 0 | -6 |
| Titoli di requisito con wording lasco rispetto alla formula vincolante (OM-2) | 1 (R-17) | 0 | -1 |
| Ancore di provenienza puntuali per la numerazione `fN` dello schema PRICE (OM-3) | 0 (solo richiamo descrittivo a CAP_09:94) | 1 (STATO_CORRENTE:76 + richiamo CAP_09:94 mantenuto) | +1 |
| Correttezza sostanziale / tracciabilita' / contraddizioni con CAP chiusi | corretta (PASS) | corretta (invariata) | 0 |

**Onesta'**: nessun target OM-1 ha richiesto di restare al livello capitolo (tutti hanno risolto alla riga esatta con costrutto presente, verificato con Read). Nessun finding contestato. Le modifiche sono confinate alle 3 zone OM-1/2/3 del solo `SPEC_FUNZ_01.md`; nessun CAP, indice o file di stato toccato.

### Criterio di rollback (Iterazione 2)

Trattandosi di sole correzioni di numero-di-riga e di wording (nessun cambiamento di contenuto sostanziale), il rollback dell'Iterazione 2 e' il ripristino dei 6 numeri precedenti + del titolo R-17 + rimozione dell'ancora STATO_CORRENTE:76, senza alcun impatto sul motore. Condizione di rollback: se la re-review v2 rilevasse che un nuovo numero di riga non risolve al costrutto atteso (regressione di citazione), si ripristina quella singola citazione al livello capitolo (livello meno puntuale ma corretto).
