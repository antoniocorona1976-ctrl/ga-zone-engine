# ISTRUZIONI per Claude Code — REV-A1 (innesto N1 + F6 su impianto A)

> Decisione AC: si resta sull'impianto **A** (track business-spec: R/NFR/CN, RM-1/2/3, bi-sede). Si innestano SOLO due regole additive: **N1 (atomicità del requisito)** e **F6 (blocchi in batch)**. Tutto il resto dei file resta INVARIATO.
> Reversibilità verso B (modello a 4 canali), nero su bianco: tornare a B = riscrivere il solo TEMPLATE dei requisiti + ri-taggare i SPEC_FUNZ eventualmente prodotti (oggi: zero). L'impianto di processo (questi 3 file) NON va demolito in nessuno dei due casi. N1 e F6 sopravvivono identici anche in B.
> Operazione = cancellazione di 3 file untracked + 4 inserimenti di testo. NIENTE commit, NIENTE push.

---

## STEP 1 — Cancella i 3 file sbagliati (erano del modello B, non vanno nel repo A)
Sono untracked. Eliminali dal disco:
- `docs/spec_funzionale/TEMPLATE_SPEC_FUNZ.md`
- `docs/spec_funzionale/TRACCIABILITA.md`
- `specs/checks/SPEC_CHECK_STATICI.md`

Se la cartella `specs/checks/` resta vuota dopo, lasciala pure (non rimuovere altro).
NON toccare nessun altro file untracked o modificato (es. `.claude/settings.json`: non è mio, lascialo).

## STEP 2 — Modifica `.claude/agents/spec_developer.md` (2 inserimenti)
Usa Edit. Match dei testi-ancora come substring esatta; preserva il resto del file e gli a-capo CRLF. NON riscrivere il file intero.

**2a.** Trova la riga che termina con:
`Niente metriche GA inventate.`
Subito DOPO quella riga (nuova riga vuota + blocco), inserisci:

```
## Atomicità del requisito (N1)
Ogni requisito (R / NFR / CN) esprime **una sola proposizione verificabile**. Se un requisito naturale impacchetta più concern (es. una soglia + una condizione di compliance + una conseguenza di coerenza), **spezzalo in più requisiti, uno per concern**, ciascuno con ID e tracciabilità propri. NON impacchettare concern eterogenei in un unico enunciato: un sotto-requisito sepolto nella prosa non è tracciabile né verificabile singolarmente, e sfugge alla review.
```

**2b.** Trova la riga:
`## Chiusura (pre-consegna adattata)`
Subito PRIMA di quella riga (blocco + nuova riga vuota), inserisci:

```
## Gestione blocchi (F6 — in batch, non a goccia)
Se durante il task incontri un blocco (fonte/CAP mancante, ambiguità che richiede decisione di Planner/AC, requisito non risolvibile dai documenti): **NON fermarti al primo blocco**. Mappa l'**intero task** producendo tutto ciò che puoi, poi nel REPORT, sezione **"Blocchi / Domande aperte"**, elenca **tutti** i blocchi insieme — per ciascuno: ID requisito, motivo, cosa serve per sbloccarlo. Solo a task interamente mappato scrivi lo stato di blocco. Fermarsi a goccia genera cicli Developer→Orchestratore→supervisore in serie invece di un solo batch. (Non scrivi su `tasks/QUESTIONS.md`, planner-owned: il blocco vive nel tuo REPORT; l'Orchestratore/Planner lo gestisce.)
```

## STEP 3 — Modifica `.claude/agents/spec_planner.md` (1 inserimento)
Trova la riga:
`## Vincoli metodologici sul track (RM-1/RM-3)`
Subito PRIMA di quella riga (blocco + nuova riga vuota), inserisci:

```
## Atomicità e blocchi (N1, F6)
- **(N1)** Negli acceptance, richiedi requisiti **atomici**: un requisito = una proposizione verificabile. Un requisito che impacchetta più concern va spezzato in più ID. Vincola il Developer a questo.
- **(F6)** Il Developer raccoglie **tutti** i blocchi del task in un unico batch nel REPORT, non si ferma al primo. Quando interpelli supervisore/AC su blocchi o ambiguità, fallo **in un'unica sessione batch** per tutto il task, non un giro per blocco.
```

## STEP 4 — Modifica `.claude/agents/spec_reviewer.md` (1 inserimento)
Trova la riga che inizia con:
`5. **Valore operativo per requisito**`
Subito DOPO quella riga (intera, fino al punto finale), inserisci:

```
6. **(N1) Atomicità**: ogni requisito esprime una sola proposizione verificabile. Caccia ai requisiti compositi che impacchettano più concern in un enunciato (un sotto-requisito sepolto nella prosa sfugge alla verifica singola) → segnala come "da spezzare".
```

## STEP 5 — NON committare
NESSUN git add / commit / push. Lascia tutto nel working tree per la review in VS Code.

## STEP 6 — Scrivi l'esito in un file
Scrivi in `Business Spec/Final/ESITO_REV-A1.md`:
- I 3 file cancellati (confermati assenti dal disco).
- Per ciascuno dei 3 spec_*: quante righe aggiunte, e i nomi delle sezioni inserite (devono comparire: in developer "Atomicità del requisito (N1)" e "Gestione blocchi (F6 — in batch, non a goccia)"; in planner "Atomicità e blocchi (N1, F6)"; in reviewer il punto "6. **(N1) Atomicità**").
- Output di `git status` e di `git --no-pager diff --stat`.
- Conferma esplicita: nessun commit/push eseguito, nessun file fuori dai 4 target toccato.

## VINCOLI
- Tocchi SOLO: i 3 file da cancellare (STEP 1) e i 3 spec_* (STEP 2-4). Più il file esito (STEP 6).
- NON riscrivere i file interi: solo gli inserimenti indicati.
- Se un testo-ancora non si trova o compare più di una volta: FERMATI, scrivi cosa hai trovato in `ESITO_REV-A1.md`, non indovinare.
- Niente commit, niente push.
