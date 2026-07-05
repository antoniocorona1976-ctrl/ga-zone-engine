# ISTRUZIONI_RATIFICA-PIANO-01 — Ratifica del piano fase codice + registro decreti

Uso: salva in `Codice/Piano_di_lavoro/Istruzioni/` e lancia:

Leggi ed esegui "Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_RATIFICA-PIANO-01.md"

---

RUOLO: esecutore della ratifica decisa da AC. Perimetro chiuso: SOLO i file elencati qui.
VIETATO: toccare CAP, `SPEC_FUNZ_01.md`, `tasks/METODO.md`, role file, `data/`, `Business Spec/`, qualsiasi file fuori perimetro. VIETATO `git add .` o `git add -A`: solo add espliciti per path. Ogni affermazione nell'ESITO con path:riga o hash (RM-2).

## 1. Sorgente

File sorgente: `Codice/Piano_di_lavoro/Esito/PIANO_FASE_CODICE_01.md` (la "finale", 30/06 23:09, derivata da v3).
Verifiche preliminari, se una fallisce STOP e riporta:
- il file esiste e la riga 1 è il titolo del piano;
- il file NON contiene già le stringhe `§0` o `RATIFICATO` (guardia di idempotenza).

## 2. Patch — header di stato + §0 decreti

Nel file sorgente, subito dopo la riga 1 (titolo), inserisci verbatim il blocco seguente:

```
---
**Stato: RATIFICATO da AC — 05/07/2026.** Versione ufficiale del piano di fase codice.
Provenienza: bozza finale del 30/06 (linea v3) + §0 decreti. Bozze storiche in `Esito/`.

## §0 — Decreti vincolanti del supervisore (AC)

I decreti seguenti sono decisioni vincolanti di AC e prevalgono su ogni punto
configgente della metodologia congelata (i CAP non si editano — G-09) **e del corpo
di questo piano**. Debiti di riconciliazione registrati in `DECISIONI.md`; la
riconciliazione documentale è a carico del track Metodologia e non blocca la fase codice.

**DEC-A — Semiampiezza `b` della zona di ingresso.**
`b` è un parametro libero del GA con dominio {5, 10, 15, 20} punti. L'ampiezza totale
massima della zona è quindi 40 punti (non 40 per lato). Supera la lettura "±40"
derivata per errore dall'esempio di intento "41100 41140".

**DEC-B — Floor di 80 punti.**
Il floor minimo di emissione di 80 punti netti (R-5.9; moltiplicatore 5 €/punto) si
valuta sui punti reali/unadjusted (serie concatenata ricostruita dal preprocessore),
perché la sua funzione è economica. La valutazione del segnale resta sulla serie
ratio, come da Invariante 7.

**Decisioni pregresse già incorporate nel corpo del piano** (registrate in DECISIONI.md):
DEC-01 primary input = 2 serie Portara consegnate (ratio-adjusted + Panama-additiva),
unadjusted derivata dal preprocessore — prevale su Cap.37/38, debito aperto;
DEC-02 archivio dati = root neutrale condivisa fuori dai repo (opzione b).
---
```

## 3. Verifica di coerenza del corpo — SOLA LETTURA, non editare

- `grep -n -i "80"` sul file patchato: riporta le righe in cui si dice su quale serie si valuta il floor 80pt.
- `grep -n -i -E "semiampiezza|per lato|±|zona"` : riporta ogni riga che fissa o vincola l'ampiezza della zona di ingresso.
- Non correggere nulla. Riporta i passaggi trovati nell'ESITO, marcando `CONFLITTO-§0` quelli in contrasto con DEC-A o DEC-B. Il §0 prevale comunque (clausola al punto 2); eventuali correzioni del corpo le decide il Planner dopo.

## 4. Promozione a piano ufficiale

Sposta il file patchato (è untracked, `mv` normale) in:
`Codice/Piano_di_lavoro/PIANO_FASE_CODICE_01.md`
Verifica: il vecchio path in `Esito/` non esiste più; il nuovo esiste.

## 5. DECISIONI.md

Crea `Codice/Piano_di_lavoro/DECISIONI.md` con questo contenuto verbatim:

```
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
```

## 6. Commit e push

`git add` espliciti, uno per path:
- `Codice/Piano_di_lavoro/PIANO_FASE_CODICE_01.md`
- `Codice/Piano_di_lavoro/DECISIONI.md`
- `Codice/Piano_di_lavoro/Esito/PIANO_FASE_CODICE_01_v2.md`
- `Codice/Piano_di_lavoro/Esito/PIANO_FASE_CODICE_01_v3.md`
- `Codice/Piano_di_lavoro/Istruzioni/PIANO_FASE_CODICE_01.md`
- `Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_RATIFICA-PIANO-01.md`

Prima del commit: `git status --short` — se in staging compare qualsiasi path non in elenco, STOP e riporta.

Commit: `RATIFICA: PIANO_FASE_CODICE_01 ufficiale + DECISIONI.md (DEC-01/02, DEC-A, DEC-B) — decreto AC`
Poi `git push`.

## 7. ESITO (in chat, nessun altro file scritto)

- hash e messaggio del commit (`git log -1 --oneline`), conferma push;
- conferma path ufficiale del piano + prime 30 righe del file committato;
- esito integrale dei grep del §3, con eventuali marcature `CONFLITTO-§0`;
- contenuto di `DECISIONI.md` come committato;
- `git status --short` finale del perimetro (deve essere pulito per i 6 path).
