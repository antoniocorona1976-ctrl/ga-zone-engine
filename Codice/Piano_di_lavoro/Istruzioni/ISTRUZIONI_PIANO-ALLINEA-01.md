# ISTRUZIONI_PIANO-ALLINEA-01 — Allineamento corpo del piano a §0 (chiusura CONFLITTO-§0)

Uso: salva in `Codice/Piano_di_lavoro/Istruzioni/` e lancia:

Leggi ed esegui "Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_PIANO-ALLINEA-01.md"

---

RUOLO: esecutore di correzioni puntuali decise dal Planner sull'ESITO RATIFICA-PIANO-01.
PERIMETRO: SOLO `Codice/Piano_di_lavoro/PIANO_FASE_CODICE_01.md` + questo file di istruzioni. Nessun altro file. VIETATO toccare `DECISIONI.md`, le bozze in `Esito/`, CAP, spec, METODO.md. VIETATO `git add .`/`-A`.

## 0. Precondizione — STOP se fallisce

`git log -1 --oneline` deve contenere il commit di ratifica (`RATIFICA: PIANO_FASE_CODICE_01`) già pushato. Se la ratifica non è committata: STOP, riporta, non fare nulla.

## 1. Regole di applicazione

- I numeri di riga sotto sono indicativi (numerario del file patchato alla ratifica): l'ancora vera è il testo citato. Individua il passaggio per testo; se l'ancora non si trova o è ambigua, NON applicare quell'intervento, marca `NON-APPLICATO` e prosegui con gli altri.
- Interventi chirurgici: tocca solo la clausola indicata, non riscrivere i paragrafi interi.
- Nel testo nuovo evita dove possibile le parole della famiglia "verific*" (usa "prova", "controllo", "valutato"). Se `rm_guard` scatta comunque al commit: STOP e chiedi ad AC l'override, come per la ratifica. Non auto-override.

## 2. Interventi (dalla tabella CONFLITTO-§0 dell'ESITO RATIFICA-PIANO-01)

1. **~:37 — CN-5.2.** Sostituire la sola clausola che attribuisce il floor alla valutazione-su-ratio con: floor 80pt valutato su punti reali/unadjusted (DEC-B); la valutazione del segnale (condizioni di emissione) resta su ratio.
2. **~:39 — divieto d'esempio.** La frase "una card che … es. 80pt su unadjusted … è override del CAP — vietato" diventa: una card che contraddice un decreto §0 è vietata; il caso 80pt-su-unadjusted è normato da DEC-B (prevale sul CAP, debito di riconciliazione in DECISIONI.md).
3. **~:60 — etichetta DAG.** "(RATIO in eval; 80pt floor su serie eval)" → "(RATIO in eval; 80pt floor su unadjusted — DEC-B)".
4. **~:87 — M4 regola emissione.** Le 3 condizioni restano valutate su ratio; il floor 80pt è valutato su unadjusted (DEC-B). La logica AND resta invariata.
5. **~:109 — inv.7a.** Escludere il floor dalla valutazione-su-ratio: valutazione segnale su ratio (condizioni di emissione); floor 80pt su unadjusted per DEC-B.
6. **~:113 — divieto diretto.** Invertire: il floor 80pt si valuta su unadjusted per decreto DEC-B (mai su Panama); il contrasto con la metodologia è sanato dal debito registrato in DECISIONI.md.
7. **~:115 — "(zona ±40, target, stop…)".** Sostituire "±40" con "semiampiezza b ∈ {5,10,15,20} — DEC-A". Nello stesso blocco: la domanda seam è risolta da DEC-B per il floor; resta aperta SOLO per zona/target/stop (gate M4→M5 invariato).
8. **~:128 — Fase B.** "M4 (emissione/80pt su serie eval=ratio)" → "M4 (emissione su ratio; floor 80pt su unadjusted — DEC-B)".
9. **~:161 — M4 done-when.** "80pt valutato su unadjusted (DEC-B); condizioni di emissione valutate su ratio (inv.7a)".
10. **~:175 — prerequisito seam.** Marcare risolto per il floor (DEC-B); la domanda al track Metodologia resta solo per zona/target/stop (gate M4→M5).

Non toccare: :18-19 e :13-15 (sono il §0 stesso), :144 (neutro), :109 prima tabella ampiezza (neutro).

## 3. Changelog

Nell'header del piano, subito dopo la riga "Provenienza: …", aggiungere:
`v1.1 — 05/07/2026: corpo allineato a §0 (chiusura CONFLITTO-§0 da ESITO RATIFICA-PIANO-01).`

## 4. Commit e push

`git add` espliciti:
- `Codice/Piano_di_lavoro/PIANO_FASE_CODICE_01.md`
- `Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_PIANO-ALLINEA-01.md`

`git status --short`: se in staging c'è altro, STOP.
Commit: `PIANO v1.1: allineamento corpo a §0 (DEC-A/DEC-B) — chiusura CONFLITTO-§0`
Poi `git push`.

## 5. ESITO (in chat)

- Per ciascuno dei 10 interventi: riga, testo PRIMA → testo DOPO verbatim, oppure `NON-APPLICATO` con motivo.
- Hash e messaggio commit, conferma push, `git status --short` finale (pulito sul perimetro).
- Conferma che DECISIONI.md e le bozze in `Esito/` non sono state toccate.
