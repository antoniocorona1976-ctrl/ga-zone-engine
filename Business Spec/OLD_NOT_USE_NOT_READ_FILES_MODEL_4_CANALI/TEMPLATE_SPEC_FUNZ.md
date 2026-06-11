# TEMPLATE — SPEC_FUNZ_NN

> Struttura obbligatoria. Ogni requisito segue questo schema. `NN` = numero capitolo spec.
> Stato requisito: `BOZZA` | `VALIDATO` | `BLOCCATO`.

## Intestazione capitolo
- **ID capitolo**: SPEC-FUNZ-NN
- **Titolo**:
- **§Metodologia di riferimento**: (sezioni di `docs/methodology_v2/` da cui deriva)
- **Out-of-scope globale**: (cosa questo capitolo NON copre)

---

## Schema del singolo requisito

### REQ-FUNZ-NN-XXX — &lt;titolo breve&gt;
- **Enunciato**: &lt;cosa il sistema deve fare/garantire — una proposizione verificabile&gt;
- **Canale**: CH1 | CH2 | CH3 | CH4
- **Tracciabilità a monte**: §X.Y metodologia | N/A (decisione di prodotto)
- **Out-of-scope**: &lt;confine esplicito di questo requisito&gt;
- **Blocco di validazione**: (dipende dal canale, vedi sotto)
- **Stato**: BOZZA | VALIDATO | BLOCCATO

#### Blocco per CH1 — Fatto esterno
- **Fonte**: `data/reference/<file>` — &lt;riferimento puntuale: pagina/sezione&gt;
- **Check deterministico**: &lt;asserzione, es. `sessione == 09:00–22:00 CET`&gt;
- **Atteso**: &lt;valore atteso&gt;
- (VALIDATO solo a check verde.)

#### Blocco per CH2 — Coerenza interna
- Nessun blocco aggiuntivo. Il requisito deve possedere: ID, out-of-scope, unità di misura su ogni soglia, nessuna contraddizione con altri REQ. Verificato dal lint statico.

#### Blocco per CH3 — Claim testabile
- **Ipotesi falsificabile**: &lt;es. "80pt netti massimizzano la net expectancy per segnale vs {60,70,90,100}"&gt;
- **Dataset/Finestra**: &lt;es. Portara/CQG 1-min, 5 anni, walk-forward&gt;
- **Metrica**: &lt;es. net expectancy per segnale eseguito, al netto commissioni&gt;
- **Soglia di accettazione**: &lt;es. "80 domina le alternative, significatività test X"&gt;
- **Purge/Embargo**: &lt;parametri&gt;
- **Esito**: PENDING | CONFERMATA | FALSIFICATA
- (VALIDATO solo a esito CONFERMATA.)

#### Blocco per CH4 — Intento
- **Fondamento**: &lt;su cosa si basa la scelta — prodotto/rischio&gt;
- **Rollback trigger**: &lt;evento concreto e osservabile che dimostrerebbe la scelta sbagliata&gt;
- **Ratifica AC**: PENDING | RATIFICATO (data)
- (VALIDATO solo a ratifica AC.)

---

## Esempi compilati (uno per canale)

### REQ-FUNZ-01-003 — Orario di sessione [CH1]
- **Enunciato**: Il motore opera sulla sessione continua del FIB 09:00–22:00 CET.
- **Canale**: CH1
- **Tracciabilità**: §&lt;...&gt; metodologia
- **Out-of-scope**: gestione aste di apertura/chiusura; festività di calendario borsistico.
- **Fonte**: `data/reference/borsa_italiana_FIB_contract.md` — sezione orari di negoziazione.
- **Check**: `sessione_continua == 09:00–22:00 CET`
- **Atteso**: 09:00–22:00 CET
- **Stato**: BOZZA → VALIDATO a check verde.

### REQ-FUNZ-02-001 — Banda di entrata [CH2]
- **Enunciato**: La zona di entrata è espressa come banda di ±40 punti FIB attorno al livello strutturale.
- **Canale**: CH2
- **Out-of-scope**: logica di selezione del livello strutturale (altro requisito).
- **Stato**: BOZZA → VALIDATO a lint verde (deve portare unità "punti FIB", ID, out-of-scope).

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
- **Ratifica AC**: PENDING.
- **Stato**: BLOCCATO finché RATIFICATO.
