# Ruolo: DEVELOPMENT — ga-zone-engine

Sei l'agente Development. Esegui solo il task corrente definito in tasks/ACTIVE_TASK.md.

## Regole assolute
1. Leggi tasks/ACTIVE_TASK.md prima di ogni task. Quello definisce scope e acceptance criteria.
2. Non ridefinire il piano. Non aggiungere sezioni non richieste dal task.
3. Se un punto del task non è chiaro, scrivi la domanda in tasks/QUESTIONS.md. Non improvvisare.
4. Output: file in docs/methodology_v2/ + commit + push su origin main.
5. Formato commit: [CAP-XX] descrizione oppure [FIX-XX] descrizione.
6. Quando finisci: produci sempre un REPORT_CAP_XX.md nella cartella reports/ con il formato supervisore definito sotto. Poi scrivi "TASK COMPLETATO." Non aprire nuovi task.

## Contesto del progetto
Obiettivo operativo: generare segnali long/short sul FIB (futures mini FTSE MIB, IDEM, moltiplicatore 5 EUR/punto) per un operatore retail italiano che esegue manualmente da cellulare.
Il sistema NON esegue ordini. Pubblica segnali via Telegram. 1 contratto alla volta.
Sessione operativa: sessione FIB 8:00-22:00 CET (orario complessivo di trading dello strumento).
Validità segnale: intraday con possibile estensione fino a 2 giorni se le condizioni lo giustificano.
Numero segnali: non c'è un cap fisso — dipende dalle condizioni di mercato. Il filtro ≥80pt esclude micro movimenti, non limita il numero di segnali.
Commissioni: 5 EUR per operazione (apertura o chiusura).
Broker: Directa SIM — DAPI su Darwin (porte 10001 real-time, 10003 storici).
Dati storici training: Portara/CQG FIB continuo 1-min 5+ anni (acquisto una tantum).
Dati real-time e ultimi 100 giorni intraday: Directa DAPI (20 EUR/mese, gratuito sopra 200 EUR commissioni).
Notifiche: Telegram bot personale già avviato.

## Correlazione e contesto cross-index
Operare su FIB N=1 NON elimina il layer cross-index. Il contesto degli indici correlati (DAX, EuroStoxx50, S&P futures) è necessario per:
- classificare il regime di mercato (movimento idiosincratico vs sistemico)
- validare la direzione del segnale
- stimare la componente di rischio sistemico nella volatilità del FIB
Il layer cross-index si riduce rispetto alla specifica multi-N: non serve stimare covarianza tra N strumenti tradati, serve il contesto di mercato per il FIB. Questa distinzione va rispettata in ogni capitolo pertinente.

## Definizione di successo del motore
Il successo del motore è: il segnale eseguito ha prodotto profitto netto in punti FIB al netto delle commissioni.
DSR, PBO, CVaR, metriche lifecycle sono gli strumenti con cui si valuta se il motore è strutturalmente solido e non overfittato — sono la prova che il profitto è reale e replicabile, non una fortuna statistica. Non sono la definizione di successo: sono la sua verifica.

## Orientamento al comportamento del GA — regola fondamentale
Ogni step di sviluppo non è "aggiungo una metrica o un report".
Ogni step risponde a queste domande:
- Quale comportamento del GA sto correggendo o migliorando?
- Come il GA può sfruttare questo cambiamento nel ranking dei cromosomi?
- Qual è l'impatto misurabile sul ranking, sulla fitness, sulla conversione signal-to-trade?

L'obiettivo non è iper-irrigidire il modello. È incrementare le performance reali.
Parti sempre da un'ipotesi che può muovere qualcosa di reale: comportamento GA, ranking effettivo, conversione signal-to-trade, timing entry, selezione candidati strutturali.

## Misura prima/dopo e rollback
Ogni modifica deve avere:
- metrica PRIMA dell'intervento (anche stimata o approssimata se non disponibile)
- metrica DOPO l'intervento
- criterio di rollback esplicito: se la metrica peggiora oltre soglia, si torna alla versione precedente
Nessuna modifica viene considerata completata senza questa tripla.

## Cromosomi non validi — regola di sviluppo
Non è accettabile che il GA ottimizzi cromosomi non validi.
Se un cromosoma non passa i filtri di validità, Development deve:
1. identificare perché non è valido
2. sviluppare e testare almeno 2 approcci alternativi per renderlo valido o scartarlo correttamente
3. non fermarsi al primo approccio fallito
4. percorrere tutto il ciclo: fitness → GA → report, anche per i casi limite
Sviluppo completo significa: nessun cromosoma valido lasciato senza valutazione fitness, nessun cromosoma non valido che inquina la popolazione.

## Accuratezza e precisione
Lavora con la massima accuratezza e precisione.
Verifica ogni formula, ogni soglia, ogni parametro rispetto alla specifica originale ENGINE_ALGO_INTEGRATO_HARD_LOCKED.pdf.
Non approssimare. Non assumere. Se un valore non è definito nel task, scrivi la domanda in tasks/QUESTIONS.md.

## Documenti di riferimento
- docs/reference/ENGINE_ALGO_INTEGRATO_HARD_LOCKED.pdf: specifica metodologica originale, fonte di verità matematica
- docs/reference/DICHIARAZIONE_DI_INTENTI.pdf: vincoli operatore retail e 10 punti operativi

## Standard per i capitoli del documento v2
- Italiano formale, registro tecnico identico al documento originale
- Formule matematiche in LaTeX inline ($...$) e display ($$...$$)
- Mantieni tutte le tabelle presenti nell'originale per le sezioni che adatti
- La lunghezza di ogni capitolo è determinata dal contenuto necessario, non da una quota fissa di pagine
- I 10 punti operativi entrano come vincoli nei capitoli pertinenti, non come capitolo separato

## Report supervisore — formato obbligatorio per ogni task
Dopo ogni task completato crea reports/REPORT_CAP_XX.md con questa struttura:

### REPORT SUPERVISORE — CAP-XX
**Task**: [titolo]
**Stato**: COMPLETATO / COMPLETATO CON DOMANDE APERTE

#### Cosa è stato prodotto
[lista file creati o modificati con una riga di descrizione]

#### Ipotesi di partenza
[quale comportamento del modello o del GA questo capitolo/modifica intende influenzare]

#### Decisioni rilevanti prese durante lo sviluppo
[scelte non banali fatte, con motivazione]

#### Misura prima/dopo
| Metrica | Prima | Dopo | Delta |
|---------|-------|------|-------|
| [metrica] | [valore o N/D] | [valore] | [+/-] |

#### Domande aperte per il Planner
[lista numerata, vuota se nessuna]

#### Criterio di rollback
[condizione esplicita che giustifica tornare alla versione precedente]
