# TEMPLATE — SPEC_FUNZ_NN

> Struttura obbligatoria. Ogni requisito segue questo schema. `NN` = numero capitolo spec.
> Stato requisito: `BOZZA` | `VALIDATO` | `BLOCCATO`.
> Revisione [REV-4CH-audit]: incorpora N1 (proposizione singola), N2 (provenienza fonte CH1), N3 (classe rollback trigger CH4), F1 (citazione verbatim in tracciabilità). **Riconciliare con `tasks/METODO.md` e `.claude/BASE_COMUNE.md` prima del deposito.**

## Intestazione capitolo
- **ID capitolo**: SPEC-FUNZ-NN
- **Titolo**:
- **§Metodologia di riferimento**: (sezioni di `docs/methodology_v2/` da cui deriva)
- **Out-of-scope globale**: (cosa questo capitolo NON copre)

---

## Regola di atomicità (N1 — vincolo duro, verificato dal lint CH2)
Ogni REQ esprime **UNA sola proposizione verificabile**. Se un requisito naturale contiene più concern — es. una soglia numerica (CH3) **+** una scelta di prodotto (CH4) **+** una conseguenza di coerenza sullo state-machine (CH2) — si **spezza in più REQ-ID, uno per canale**. È vietato scegliere il canale dominante e seppellire gli altri concern nella prosa dell'enunciato: è laundering per occultamento, e né il lint né il Reviewer isolano un sotto-claim nascosto in una frase.

---

## Schema del singolo requisito

### REQ-FUNZ-NN-XXX — &lt;titolo breve&gt;
- **Enunciato**: &lt;UNA proposizione verificabile — un solo concern&gt;
- **Canale**: CH1 | CH2 | CH3 | CH4
- **Tracciabilità a monte**: §X.Y — «citazione verbatim breve della frase di metodologia da cui deriva» | N/A (decisione di prodotto)
- **Out-of-scope**: &lt;confine esplicito di questo requisito&gt;
- **Blocco di validazione**: (dipende dal canale, vedi sotto)
- **Stato**: BOZZA | VALIDATO | BLOCCATO

> **Tracciabilità (F1)**: quando il requisito deriva dalla metodologia, NON basta il numero di §. Riporta la **frase verbatim** della § da cui derivi l'enunciato. Il lint verifica che la citazione *esista*; il Reviewer (asse 6) verifica che la § citata *sostenga davvero* l'enunciato — la difesa contro la confabulazione di logica metodologica plausibile ma non presente nella fonte.

#### Blocco per CH1 — Fatto esterno
- **Fonte**: `data/reference/<file>` — &lt;riferimento puntuale: pagina/sezione&gt;
- **Check deterministico**: &lt;asserzione, es. `sessione == 09:00–22:00 CET`&gt;
- **Atteso**: &lt;valore atteso&gt;
- **Fonte verificata da AC**: PENDING | &lt;data&gt; — *la fonte vendorizzata rappresenta fedelmente il fatto di mondo*
- (VALIDATO solo a check verde **E** `Fonte verificata da AC` ≠ PENDING.)

> **Provenienza (N2)**: il check deterministico verifica che l'`Atteso` combaci con la **fonte vendorizzata** — è consistenza spec↔artefatto, NON verità. Che l'artefatto rappresenti fedelmente il mondo è un **atto di ratifica di AC**, non una trascrizione automatica: vendorizzare una fonte è un CH4 mascherato ("questo file rappresenta il mondo"). Esempio reale del rischio: l'orario di sessione FIB è 09:00–22:00 CET; se la fonte fosse trascritta col vecchio 09:00–17:40, il check passerebbe **verde** contro un artefatto sbagliato. Finché `Fonte verificata da AC` è PENDING, lo stato resta BLOCCATO.

#### Blocco per CH2 — Coerenza interna
- Nessun blocco aggiuntivo. Il requisito deve possedere: **proposizione singola** (N1), ID, out-of-scope, unità di misura su ogni soglia, nessuna contraddizione con altri REQ. Verificato dal lint statico.

#### Blocco per CH3 — Claim testabile
- **Ipotesi falsificabile**: &lt;es. "80pt netti massimizzano la net expectancy per segnale vs {60,70,90,100}"&gt;
- **Dataset/Finestra**: &lt;es. Portara/CQG 1-min, 5 anni, walk-forward&gt;
- **Metrica**: &lt;es. net expectancy per segnale eseguito, al netto commissioni&gt;
- **Soglia di accettazione**: &lt;es. "80 domina le alternative, significatività test X"&gt;
- **Purge/Embargo**: &lt;parametri&gt;
- **Esito**: PENDING | CONFERMATA | FALSIFICATA
- (VALIDATO solo a esito CONFERMATA dall'harness empirico.)

#### Blocco per CH4 — Intento
- **Fondamento**: &lt;su cosa si basa la scelta — prodotto/rischio&gt;
- **Rollback trigger**: &lt;evento concreto e osservabile che dimostrerebbe la scelta sbagliata&gt;
- **Classe rollback trigger**: pre-deployment osservabile | solo-live
- **Ratifica AC**: PENDING | RATIFICATO (data)
- (VALIDATO solo a ratifica AC.)

> **Classe del trigger (N3)**: un trigger **solo-live** (osservabile solo dopo il go-live, es. "P&L reale divergente in forward-run") rende il requisito **empiricamente inerte** fino al deployment: la ratifica AC lo porta a VALIDATO, ma nulla potrà smentirlo prima di rischiare capitale. Il Reviewer (asse 4) verifica se un trigger solo-live nasconde in realtà un **CH3 differito** (laundering inverso): se parte del claim è pre-testabile sui dati storici, va estratta come CH3.

---

## Esempi compilati (uno per canale)

### REQ-FUNZ-01-003 — Orario di sessione [CH1]
- **Enunciato**: Il motore opera sulla sessione continua del FIB 09:00–22:00 CET.
- **Canale**: CH1
- **Tracciabilità**: §&lt;...&gt; — «&lt;citazione verbatim della metodologia&gt;»
- **Out-of-scope**: gestione aste di apertura/chiusura; festività di calendario borsistico.
- **Fonte**: `data/reference/borsa_italiana_FIB_contract.md` — sezione orari di negoziazione.
- **Check**: `sessione_continua == 09:00–22:00 CET`
- **Atteso**: 09:00–22:00 CET
- **Fonte verificata da AC**: PENDING — *da confermare contro fonte primaria Euronext/Borsa Italiana (NON il vecchio 09:00–17:40).*
- **Stato**: BLOCCATO → VALIDATO a check verde E fonte verificata.

### REQ-FUNZ-02-001 — Banda di entrata [CH2]
- **Enunciato**: La zona di entrata è espressa come banda di ±40 punti FIB attorno al livello strutturale.
- **Canale**: CH2
- **Out-of-scope**: logica di selezione del livello strutturale (altro requisito).
- **Stato**: BOZZA → VALIDATO a lint verde (proposizione singola, unità "punti FIB", ID, out-of-scope).

### REQ-FUNZ-04-002 — Soglia di target netto [CH3]
- **Enunciato**: Un segnale è ammesso solo se il target netto atteso ≥ 80 punti FIB dopo commissioni.
- **Canale**: CH3
- **Ipotesi**: 80pt netti massimizzano la net expectancy per segnale eseguito rispetto a {60,70,90,100}, out-of-sample.
- **Dataset**: Portara/CQG 1-min, 5 anni, walk-forward, purge+embargo.
- **Metrica**: net expectancy per segnale eseguito (netto commissioni Directa).
- **Soglia**: 80 domina le alternative con significatività [test].
- **Esito**: PENDING.
- **Stato**: BLOCCATO finché Esito ≠ CONFERMATA.

### REQ-FUNZ-00-001 — Metrica di successo primaria [CH4]
- **Enunciato**: La metrica di successo primaria del sistema è il profitto netto in punti FIB per segnale eseguito; DSR/PBO sono strumenti di validazione, non definizione di successo.
- **Canale**: CH4
- **Fondamento**: decisione di prodotto/rischio di AC.
- **Rollback trigger**: se in forward-run i punti netti positivi non corrispondono all'obiettivo di business atteso (P&L reale divergente) → rivedere la metrica primaria.
- **Classe rollback trigger**: **solo-live** — osservabile solo in forward-run. Il Reviewer verifica che la parte pre-testabile (es. correlazione storica punti-netti ↔ metriche di edge) non vada estratta come CH3.
- **Ratifica AC**: PENDING.
- **Stato**: BLOCCATO finché RATIFICATO.
