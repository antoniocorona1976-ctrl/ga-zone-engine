# DECISIONI.md — Registro dei decreti vincolanti (fase codice)

Regola: i decreti di AC prevalgono sui punti configgenti dei CAP congelati (G-09: i
CAP non si editano) e sul corpo del piano. La riconciliazione documentale è lavoro
del track Metodologia e non blocca la fase codice. Aggiornamento solo tramite
Planner: un decreto per riga, mai riscrivere righe esistenti.

| ID | Data | Decreto | Prevale su | Debito riconciliazione |
|---|---|---|---|---|
| DEC-01 | 30/06/2026 | Primary input = 2 serie Portara consegnate (ratio-adjusted/multiplicativa + Panama-additiva, entrambe settle-based); la serie unadjusted concatenata è derivata dal preprocessore da unadjustedClose/RollSpread/cumulativeSpread/roll-log | Cap.37/38 metodologia (ricostruzione ratio nel preprocessore) | APERTO — track Metodologia |
| DEC-02 | 30/06/2026 | Archivio dati: root neutrale condivisa fuori da entrambi i repo (opzione b); writer unico = job Directa M8a; consumer read-only; scritture append-only versionate; copie derivate per-modello rigenerabili | — | — |
| DEC-A | 02/07/2026 | Semiampiezza zona `b` = parametro libero del GA, dominio {5,10,15,20} (ampiezza totale max 40 punti, non 40 per lato) | Lettura "±40" della metodologia | APERTO — track Metodologia |
| DEC-B | 02/07/2026 | Floor 80 punti netti valutato su punti reali/unadjusted (funzione economica; R-5.9; 5 €/punto); valutazione del segnale su serie ratio (Invariante 7) | Estensione al floor della prescrizione valutazione-su-ratio | APERTO — track Metodologia |

Nota: gli ID DEC-01/DEC-02 sono assegnati ora ai decreti pregressi ai soli fini di registro.
