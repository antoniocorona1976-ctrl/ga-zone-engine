# REVIEW — SPEC-FUNZ-01-AUDITFIX-01 (remediation 6 difetti audit indipendente)

> **Track**: Business-spec (SPEC-FUNZ). **Sede**: CLI (Claude Code CLI su `C:\Users\AN\...\ga-zone-engine`, filesystem locale, no-DAPI). **Modalità**: CAP-review piena adattata, delta-mirata ai 6 fix + regressioni (diff +175/-4). **Oggetto**: commit `3a93d09` (base `a3dd507`). **Reviewer**: spec_reviewer.
>
> **Conferma letture obbligatorie** (in testa, come da ruolo): 1) `tasks/METODO.md` — RM-1..RM-4, RACC-METODO-2, Freeze G-09, §Superfici GOV-SURFACES-01, §Enforcement guard — letto integralmente come prima azione. 2) `.claude/BASE_COMUNE.md` — §3 bi-sede, §4 classificazione, §6 doppio giro, §8 onestà — letto. 3) `.claude/agents/spec_reviewer.md` — letto. 4) `tasks/ACTIVE_TASK.md` — card AUDITFIX-01 (i 6 fix §3, i vincoli §4) — letto. 5) `reports/REPORT_SPEC_FUNZ_01_AUDITFIX_01.md` — letto.

---

## ITERAZIONE v1 — VERDETTO: **PASS**

**0 problemi bloccanti. 0 BUG REALE. 0 finding non-bloccanti. 0 osservazioni minori sostanziali.**

I 6 fix sono chiusi correttamente e fedeli alla riga CAP reale a HEAD; 0 regressioni sui requisiti non toccati; edge-PENDING intatto; confini rispettati (nessun CAP, v2 non toccata, nessun blocco oltre B3/B5/B6/B8); conteggi e matrici coerenti; AC-G4 e grafia canonica OK. Floor citazioni 100% raggiunto (tutte le ancore-fonte aperte con Read e verificate token-per-token).

---

## Esito fix-per-fix (fedele/regge sì-no + evidenza CAP:riga riletta)

### F1 (B6, MEDIUM) — regola di consumo per-categoria-di-feature → B6-R-38..42 — **FEDELE: SÌ**
Fonte `CAP_09_parte_9.md:185-189` (Cap.49, sottotitolo "Coerenza con la regola d'uso a valle di Parte 8 Cap.40", header Cap.49 a r151). Corrispondenza categoria↔riga **esatta, nessun off-by-one** (verificata con `sed` riga-per-riga):
- `:185` volatilità (EGARCH/regime/dispersione) → solo `bar_synthetic=False` → **B6-R-38** ✓
- `:186` prezzo (livelli/distanze) → griglia uniforme completa, inclusi sintetici → **B6-R-39** ✓
- `:187` volume → solo `bar_synthetic=False` (sintetiche volume=0) → **B6-R-40** ✓
- `:188` struttura (pivot/EMA) → griglia completa, pivot non spostati → **B6-R-41** ✓
- `:189` touch entry zone (raw touch Cap.7.3) → mai su `bar_synthetic=True` → **B6-R-42** ✓

**Legittimità dello split N1 in 5 (richiesta esplicitamente): SÌ, legittimo, NON gonfiato.** Il CAP stesso enumera 5 bullet con regole **eterogenee e in due casi opposte** (volatilità/volume/touch escludono i sintetici; prezzo/struttura li includono). Un requisito unico maschererebbe l'opposizione e sottrarrebbe ciascuna regola alla verifica singola — esattamente il failure mode N1. Ogni B6-R-NN cita la sua riga puntuale e dichiara valore operativo proprio. Matrice §7.1 aggiornata con le 5 entry + Cap.49. **F1 chiuso bene.**

### F2 (B3, LOW) — subordinazione profitto netto = metrica primaria → B3-R-48 — **FEDELE: SÌ**
Fonte `CAP_02_parte_II.md:411` (Cap.11.5). La riga reale recita: *"La metrica primaria di successo del motore rimane il profitto netto al netto delle commissioni in punti FIB realizzato dai segnali eseguiti: π, MFE, MAE e f_stop sono strumenti di verifica e calibrazione, non la definizione di successo."* B3-R-48 trascrive fedelmente. **Criterio dichiarato, NON esito d'edge**: il requisito dichiara esplicitamente "nessun valore di profitto è asserito qui; l'esito d'edge resta PENDING-empirico, esclusiva del validator in FASE-D". Split da B3-R-47 corretto: R-47 = ruolo delle metriche nella fitness (qualità informativa); R-48 = subordinazione gerarchica al profitto netto — due proposizioni distinte. Matrice §8.1 aggiornata. **Edge PENDING preservato.**

### F3 (B5, LOW) — ancora 1680 spostata a CAP_09:290 → B5-CN-05 — **REGGE: SÌ**
`grep "1680"` su tutto CAP_09 → **unica occorrenza a `:290`**: *"dominio fino a 1680 minuti, scavalca le interruzioni notturne fra sessioni e puo' coprire fino a circa due giornate"*. Citazione fedele. La proposizione-cardine di B5-CN-05 è **invariata** (testo non toccato); le ancore preesistenti `:292`/`:302` sostengono effettivamente la regola "22:00 non chiude active" (`:292` "non viene chiuso automaticamente ... mai dalla chiusura di sessione"; `:302` "NESSUNA chiusura automatica dei segnali ancora active") e **restano**. Aggiunta la sola ancora del dettaglio numerico, **nessun nuovo ID**. Matrice §7.1 aggiornata con annotazione "numero 1680 / ~due giornate: CAP_09:290". Esattamente come prescritto dalla card (correggere SOLO l'ancora).

### F4 (B6, LOW) — vincolo encoding BOM/UTF-8 header CSV → B6-CN-25 — **`:117` REGGE: SÌ (NON ancora forzata)**
**Punto critico dell'audit.** `CAP_09_parte_9.md:117` (Cap.48 "Format dati canonico runtime") contiene **letteralmente**: *"**Schema CSV BOM UTF-8 (format runtime normativo, B-2).** Ogni file CSV prodotto dalla pipeline runtime ha header obbligatorio BOM UTF-8 con i campi ..."*. La citazione del Developer in B6-CN-25 ("Ogni file CSV prodotto dalla pipeline runtime ha header obbligatorio BOM UTF-8 ...") è una **trascrizione fedele e letterale**, non un'ancora forzata pur di chiudere. La seconda ancora `:145` è anch'essa confermata letteralmente ("definisce ... il header CSV con BOM UTF-8"). La glossa esplicativa aggiunta dal Developer ("UTF-8 con Byte Order Mark") è il significato standard di "BOM UTF-8", non un'asserzione nuova non supportata. Concern distinto da B6-CN-05 (enumerazione campi). Matrice §7.1 aggiornata, Cap.48. **F4 NON in sospeso: la fonte CAP esiste ed è esplicita. Chiuso correttamente.**

### F5 (B6, LOW) — marker BACKFILL_VERIFIED_T3/UNVERIFIED + routing gate Cap.60 → B6-R-43 — **FEDELE: SÌ**
Fonte `CAP_10_parte_10.md:90` (Cap.59 "Recupero gap entro la finestra 100gg", punto 4 "Validazione idempotenza", header Cap.59 a r74). Riga reale: *"Marker di esito: BACKFILL_VERIFIED_T3 se la finestra rientra nell'orizzonte empirico testato; altrimenti BACKFILL_UNVERIFIED con flag operativo che richiede il check di riconciliazione di Cap.60."* B6-R-43 trascrive fedelmente, usa la **grafia esatta** `BACKFILL_UNVERIFIED` (non l'abbreviazione `UNVERIFIED` della card). Cap.60 esiste (header a r113), routing valido. Matrice §7.1 aggiornata, Cap.59. **F5 chiuso bene.**

### F6 (B8, LOW) — dipendenza estensione immutabilità CANDLERANGE oltre T+3 → B8-R-13 — **FEDELE: SÌ, PENDING intatto**
Fonte `CAP_10_parte_10.md:234` (Cap.64 "Punti aperti fuori scope", header a r226). Riga reale: *"Estensione immutabilita' barre CANDLERANGE oltre T+3 / su finestre afternoon/usopen / strumenti non testati: limite empirico onesto ... da rifinire con probe addizionale in FASE-D ... assunto per estensione, sorvegliato dal gate di Cap.60 ... Una eventuale estensione richiede nuovo probe empirico (Q-XX al Planner, NON dentro Parte 10)."* B8-R-13 cattura tutto fedelmente. **Marcata in modo inequivocabile dipendenza aperta / PENDING-empirico, MAI risolta né asserita**: il testo dichiara "non è risolta da B8 e non è asserita come dimostrata oltre T+3 morning". Dettaglio "T+3 morning FIB6F/DITAS" confermato da CAP_10:90 ("entro l'orizzonte T+3 morning sui ticker FIB6F/DITAS testati"). Aggiunto a §2, a lista PENDING §3 e a matrice §4.1. **Edge PENDING preservato.**

---

## Esito regressioni — **0 REGRESSIONI**

Diff `--numstat`: B3 (+4/-0), B5 (+3/-3), B6 (+43/-1), B8 (+9/-0) + REPORT (+115) + DEV_STATUS (+1). Il diff è **puramente additivo** sui requisiti:
- **B5 (+3/-3)**: le 3 righe rimosse/riaggiunte sono **le sole righe `Tracciabilità`/`Valore`/matrice di B5-CN-05** modificate per inserire l'ancora `:290` (verificato leggendo il diff testuale: la proposizione del requisito è byte-identica). Nessun'altra proposizione alterata.
- **B6 (-1)**: la riga rimossa è il **footer** del documento (aggiornamento conteggio "65 → 72"), non un requisito.
- Nessuna proposizione preesistente alterata in nessuno dei 4 blocchi.
- Nessun ID duplicato (verificato `uniq -d` sulle definizioni bold; vuoto).
- Conteggi coerenti coi nuovi ID: B3 48R/12CN/3NFR=63; B5 20R/9CN/7NFR=35 (invariato); B6 43R/25CN/4NFR=72; B8 13R/5CN=18. Tutti combaciano con REPORT §4 e con i conteggi reali nel documento (`grep -oE | sort -u | wc -l`).

## Esito edge-PENDING / confini / RM — **OK**
- **Edge PENDING intatto**: nessuna riga aggiunta asserisce esito d'edge (`grep` su GO/NO-GO/DSR/PBO/edge confermato sulle righe `^+` → vuoto). F2 = criterio dichiarato; F6 = dipendenza aperta. Entrambi rinviano esplicitamente al validator/FASE-D.
- **AC-G4 / guard RM-1**: nessuna riga aggiunta nei file spec contiene "verificat" (`grep -i "verificat"` su righe `^+` dei file spec → vuoto). Riformulazioni del Developer ("attestata empiricamente in modo diretto" / "non un fatto dimostrato") coerenti, nessun override.
- **Grafia canonica**: nessun `[CODICE-EXISTENTE]` deprecato nelle righe aggiunte. Tutte le fonti `[DOC-INTERNO CAP_*:riga]`, livello-2/3, nessuna conclusione wiki-only.
- **Confini (freeze G-09)**: `git diff --name-only` → **nessun file in `docs/methodology_v2/`** nel commit; **v2 `SPEC_FUNZ_01.md` non toccata**; nessun blocco B1/B2/B4/B7 toccato. Solo i 4 file-blocco + REPORT + DEV_STATUS.
- Commit `3a93d09` su `origin/main`, branch allineato (guard verde, push OK).

## Onestà del REPORT — **VERIFICATA**
Tutti gli AC dichiarati OK nella tabella verifica AC del REPORT hanno evidenza reale nel file (campionato e riscontrato fix-per-fix sopra). La "Misura prima/dopo" (§4) coincide coi conteggi reali. La dichiarazione "Blocchi/Domande aperte: NESSUNO" è veritiera (tutte e 6 le fonti CAP risolvibili, incluso F4). Nessun `OK` gonfiato.

---

## Tabella "Classificazione per il supervisore"

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|-----------------------|
| — | Nessun finding | — | — | — |

Nessun BUG REALE, nessun MIGLIORA PERFORMANCE, nessun NEUTRO, nessun RISCHIO PEGGIORAMENTO.

---

## Applicazione RM-1 a me stesso

- "F1 fedele, 5 ancore senza off-by-one" — **PROVE**: Read di `CAP_09_parte_9.md:170-204` (contesto pieno) + `sed -n` riga-per-riga su 185/186/187/188/189; ogni categoria del requisito combaciata col testo letterale. **ALTERNATIVE ESCLUSE**: shift di una riga (escluso: r185=volatilità non r184; verificato con sed puntuale). **NON ESCLUSE**: nessuna.
- "F4 `:117` regge, non forzata" — **PROVE**: Read di `CAP_09_parte_9.md:108-152`; r117 contiene letteralmente "header obbligatorio BOM UTF-8"; r145 contiene "header CSV con BOM UTF-8". **ALTERNATIVE ESCLUSE**: ancora forzata su riga generica (esclusa: la riga è specificamente intitolata "Schema CSV BOM UTF-8"). **NON ESCLUSE**: nessuna.
- "F3 unica occorrenza 1680 a :290" — **PROVE**: `grep -n "1680"` su tutto CAP_09 → 1 sola riga (290). **ESCLUSE**: occorrenze multiple (escluse dal grep esaustivo). **NON ESCLUSE**: nessuna.
- "0 regressioni" — **PROVE**: `git diff --numstat` + lettura testuale del diff dei 4 blocchi; le uniche -N sono ancora B5-CN-05 + footer B6. **ESCLUSE**: alterazione silenziosa di proposizioni preesistenti (esclusa dalla lettura riga-per-riga del diff completo). **NON ESCLUSE**: nessuna (il diff è piccolo e interamente ispezionato).
- "nessun CAP toccato / v2 intatta" — **PROVE**: `git diff --name-only a3dd507 3a93d09` non contiene `methodology_v2/` né `SPEC_FUNZ_01.md`. **ESCLUSE**: modifiche fuori-diff (un commit non può modificare file fuori dal proprio diff). **NON ESCLUSE**: nessuna.
- "F2/F6 edge PENDING intatto" — **PROVE**: lettura del testo dei requisiti + `grep` esito-edge su righe aggiunte (vuoto) + le righe dichiarano esplicitamente PENDING-empirico/validator. **ESCLUSE**: asserzione d'edge mascherata in prosa (esclusa: testo letto integralmente). **NON ESCLUSE**: nessuna.

## Lista "Empirico-CLI da verificare"
**VUOTA** (attesa). Review documentale no-DAPI: la spec consolida fatti già chiusi nei CAP PASS; nessun fatto empirico nuovo introdotto dai 6 fix. Nessuna probe eseguita (divieto CLI di zelo rispettato).

---

*Review v1 prodotta dallo spec_reviewer in CLI. CAP-fonte riletti token-per-token a HEAD `3a93d09`. Doppio giro ostile eseguito: il secondo giro non ha prodotto ulteriori finding. Verdetto: **PASS**.*
