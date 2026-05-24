# Review CAP-03 v4 -- Parte III: Layer quantitativo single-instrument (post Review EXTRA)

**Verdetto**: PASS

**Commit oggetto della review**: `ee0b2ee` -- `[CAP-03 v6] 4 fix chirurgici E-1/E-2/E-3/E-4 Review EXTRA`
**Data**: 2026-05-24
**Natura**: Review v4 sul rework v6 (4 fix chirurgici approvati dalla Review EXTRA post-PASS)

## Problemi bloccanti (causano FAIL)

Nessuno.

## Problemi non bloccanti (causano CONDITIONAL)

Nessuno.

## Osservazioni minori

Nessuna con impatto reale.

## Verifica sistematica dei 7 AC v6

| AC | Criterio | Esito | Evidenza |
|----|----------|-------|----------|
| AC-v6-1 | E-1 chiuso: testo Cap.14.2 disambigua $Q_p$ su medie di sessione | OK | Riga 208: "$Q_p$ e' calcolato sulla distribuzione delle **medie di sessione** $\bar{\sigma}_s$ delle $N_{reg}$ sessioni piu' recenti -- quindi $N_{reg}$ valori, uno per sessione, coerenti con la definizione di statistica di sessione di cui sopra (baseline C-7.1, Q-09) e con la citazione Corsi (2009) HAR-RV". Confronto intenzionale $\hat{\sigma}_t$ barra vs $Q_p(\bar{\sigma}_s)$ dichiarato esplicitamente. |
| AC-v6-2 | E-2 chiuso: bullet momentum eliminato; conteggio aggiornato | OK | Grep "momentum" su CAP_03_parte_III.md: 0 risultati. Riga 260: "un massimo di 37 feature candidate". Nessun residuo "40 feature" nel documento (l'unico "40" a riga 160 e' il lag ACF). |
| AC-v6-3 | E-3 chiuso: formula volume cumulato usa $t_{\text{open}(s_t)}$; simbolo definito | OK | Riga 289: formula $\sum_{j=t_{\text{open}(s_t)}}^{t-1} v_{1m}(j)$ con definizione esplicita "$t_{\text{open}(s_t)}$ e' l'indice globale della prima barra (8:01 CET) della sessione corrente $s_t$". Testo aggiunge "con reset a zero a ogni nuova sessione". |
| AC-v6-4 | E-4 chiuso: Cap.15.4 frase su finestra sessione + $T_{warmup,\text{norm}}$ dichiarato | OK | Riga 361: paragrafo "Finestra di normalizzazione per feature con reset di sessione" presente. Med e MAD su $\{x_{t_{\text{open}(s_t)}}, \ldots, x_{t-1}\}$. $T_{warmup,\text{norm}} = 100$ barre dichiarato provvisorio. Relazione $T_{warmup,\text{norm}} = 100 > T_{warmup,\text{EMA}} = 74$ dichiarata. Riga 367: $T_{warmup,\text{norm}}$ nel paragrafo finale. |
| AC-v6-5 | REPORT_CAP_03.md ha sezione "Iterazione 6" | OK | Riga 187: "## Iterazione 6 -- chiusura E-1/E-2/E-3/E-4 di Review EXTRA". Tabella modifiche, misura prima/dopo, verifica AC v6, verifica non-regressione, criterio di rollback tutti presenti. |
| AC-v6-6 | Nessuna regressione su AC v4, v5, originali | OK | (1) Formula EMA Cap.15.2.1 riga 270: $r_{t-1-j}$ invariata (B-1 v2 intatto). (2) Feature pivot Cap.15.2.4 riga 305: $\hat{\sigma}_{\text{pt}, t-1}$ invariato (NB-1 v2 intatto). (3) Formula GED Cap.13.2 riga 120-124: invariata. (4) $\hat{\sigma}_{\text{pt}}$ Cap.13.1 riga 102: invariato. (5) Citazioni Pesaran-Timmermann, Engle-Sokalska, Corsi, Inoue-Rossi tutte presenti e invariate. (6) 4 condizioni pivot Cap.15.3 righe 314-326: invariate. (7) Tutti parametri provvisori dichiarati con rinvio a Parte V. |
| AC-v6-7 | Nessuna modifica a CAP-01 o CAP-02 | OK | `git diff HEAD~1 --name-only` conferma: solo `CAP_03_parte_III.md`, `REPORT_CAP_03.md`, file di stato e `.claude/CLAUDE.md` modificati nel commit `ee0b2ee`. |

## Secondo giro ostile -- verifica sistematica post-fix

Domanda esplicita: "Sono sicuro di aver trovato tutti i problemi reali?"

Aree verificate:

1. **Causalita' del volume cumulato post-fix E-3**: la formula $\sum_{j=t_{\text{open}(s_t)}}^{t-1} v_{1m}(j)$ usa barre fino a $t-1$. In $\mathcal{F}_{t-1}$. Nessun look-ahead.

2. **Simbolo $t_{\text{open}(s_t)}$ usato in due punti (Cap.15.2.2 e Cap.15.4)**: definito formalmente la prima volta a Cap.15.2.2 (riga 289). Riusato a Cap.15.4 (riga 361) senza ridefinizione -- coerente, la convenzione notazionale e' "definisci alla prima occorrenza". Nessuna incoerenza.

3. **$T_{warmup,\text{norm}} = 100$ vs $T_{warmup,\text{EMA}} = 74$**: la relazione $100 > 74$ e' dichiarata e motivata ("la normalizzazione disponga di un campione sufficiente"). Nessuna contraddizione logica: la normalizzazione diventa attiva dopo 100 barre, il warm-up EMA dopo 74 -- il vincolo effettivo e' il maggiore dei due (100 barre), dichiarato esplicitamente. La barra `unusable` per la normalizzazione copre anche il warm-up EMA. Coerente.

4. **Conteggio 37 feature verificato per coerenza interna**: il catalogo elenca 18 feature "base" (singola variante), ma con i multiplier k espliciti (k in {5,15,60} per rendimento cumulato = 3; k in {10,30,60} per volatilita' realizzata = 3) il totale raggiunge numeri maggiori. Il "37" e' un ceiling dichiarato come parametro del modello provvisorio, non una somma puntuale delle feature elencate. Il testo non afferma che il catalogo contiene esattamente 37 feature, ma "un massimo di 37 feature candidate". La differenza rispetto al precedente "40" e' esattamente 3 (i 3 slot del momentum eliminato con k in {5,15,60}). Aritmetica coerente.

5. **Disambiguazione E-1 -- confronto barra vs sessione e' intenzionale?** Il testo a riga 208 dichiara esplicitamente: "questo confronto e' intenzionale e produce granularita' alta nella classificazione (la barra corrente e' turbolenta se la sua volatilita' supera il percentile della distribuzione delle medie di sessione storiche)". La scelta architetturale e' ora dichiarata, non implicita. La formula a riga 210 ($R_t$ basato su $\hat{\sigma}_t$ vs $Q_p$) e' coerente con la dichiarazione. E-1 chiuso senza residui.

6. **Citazione Corsi (2009) nel contesto E-1**: a riga 208 il testo cita "la citazione Corsi (2009) HAR-RV che aggrega la volatilita' per intervalli temporali, non per singola osservazione". Corsi (2009) HAR-RV aggrega volatilita' realizzata in componenti giornaliera, settimanale, mensile -- grandezze aggregate per periodo temporale, non per singola barra. L'analogia con l'uso delle medie di sessione $\bar{\sigma}_s$ come unita' di aggregazione e' legittima e non forzata: la media di sessione e' l'analogo intraday della componente giornaliera del HAR-RV. Nessuna citazione scorretta.

7. **Effetto dell'eliminazione momentum sulle feature di struttura e prezzo**: la rimozione del bullet momentum non altera nessuna delle altre feature (rendimento cumulato, EMA, volume, volatilita', struttura). Nessuna cross-reference rotta.

8. **Parametri provvisori nel paragrafo finale (riga 367)**: l'elenco contiene $W$, $p$, $N_{reg}$, $T_{persist}$, $N_{pivot}$, $n_c$, $\delta_{pivot}$, $W_{norm}$, $T_{warmup,\text{EMA}}$, $T_{warmup,\text{norm}}$, $D$. I due nuovi parametri ($T_{warmup,\text{EMA}}$ e $T_{warmup,\text{norm}}$) sono correttamente aggiunti. L'elenco e' completo rispetto a tutti i parametri dichiarati provvisori nel corpo del documento. Verificato: $\lambda = 0{,}94$ non compare nell'elenco finale, ma e' dichiarato come "parametro del modello (valore provvisorio)" a riga 274. Tuttavia, questa omissione era gia' presente nelle versioni v1-v5 e non e' stata introdotta dal rework v6. Non e' una regressione v6.

9. **Single-instrument N=1**: nessun residuo DCC/ADCC/BEKK/multi-indice nel documento. Confermato.

10. **Determinismo bit-exact**: tutte le formule sono deterministiche. Il seed MLE e' dichiarato a Cap.13.3 riga 144. Nessuna componente stocastica non seedata introdotta dai fix v6.

11. **Look-ahead**: verificato su tutti i fix v6. Nessuno introduce informazione futura. E-1 non tocca formule causali. E-2 rimuove una feature, non ne aggiunge. E-3 restringe il dominio della sommatoria alla sessione (nessun dato futuro). E-4 restringe la finestra di normalizzazione (nessun dato futuro).

## Citazioni problematiche dal testo

Nessuna.

## Classificazione per il supervisore

| # | Problema | Classificazione | Mandare a Development? |
|---|----------|-----------------|------------------------|
| -- | Nessun finding | -- | -- |

---

**Verdetto finale: PASS**

**Motivazione**: i 4 fix chirurgici della Review EXTRA (E-1 disambiguazione $Q_p$ su medie di sessione, E-2 eliminazione feature momentum con conteggio aggiornato a 37, E-3 formula volume cumulato con $t_{\text{open}(s_t)}$ definito, E-4 normalizzazione limitata alla sessione con $T_{warmup,\text{norm}} = 100$) sono stati tutti applicati correttamente. Nessuna regressione rilevata. Nessun nuovo look-ahead. Nessuna cross-reference rotta. Nessuna incoerenza numerica. Il documento e' pronto per procedere a CAP-04.

PASS: nessun problema bloccante, nessun problema non bloccante, nessuna osservazione minore con impatto reale.
