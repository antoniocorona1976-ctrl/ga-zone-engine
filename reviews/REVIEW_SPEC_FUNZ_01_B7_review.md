# REVIEW — SPEC-FUNZ-01-B7 — Gate di go-live

> **Perimetro auditato**: `docs/spec_funzionale/SPEC_FUNZ_01_B7.md` + `reports/REPORT_SPEC_FUNZ_01_B7.md` (Developer cieco, commit `14c7c57`).
> **Sede**: **CLI** (GOV-SURFACES-01, METODO §Superfici) — audit documentale **no-DAPI**, divieto CLI attivo (niente probe di zelo).
> **Modalità**: CAP-review piena adattata al non-CAP, due giri ostili (BASE_COMUNE §6).
> **Capitoli-fonte aperti con Read (freeze G-09, ≡ HEAD)**: `CAP_07_parte_VII.md` (`b27c1e3`) Cap.31-36; `CAP_01_parte_I.md` (`e8d5424`) Cap.5; più `CAP_02_parte_II.md` Cap.10 come premessa-invariante citata.
> **Mappa di chunking consultata (compito esclusivo del Reviewer)**: `PROPOSTA_SUDDIVISIONE_SPEC_v2.md` (`c7ce4be`) riga B7 → Sez.8 `NFR-8.*`; `SPEC_FUNZ_01.md` (`c7ce4be`) NFR-8.1..NFR-8.11.

---

## ITERAZIONE 1 — VERDETTO: **CONDITIONAL**

**Sintesi**: la spec è metodologicamente solida sul nucleo del blocco. **Floor citazioni 100% = PASS** (tutte le ~49 citazioni risolvono token-per-token alla riga reale dei CAP frozen). **Confronto-copertura = 0 buchi, 0 sconfinamenti, 0 orfani**. **Cardine edge-PENDING = rispettato** (zero asserzioni d'esito/edge; 30 marcature PENDING-empirico; confine di ruolo `validator` esplicito). Tuttavia ci sono **2 BUG REALI** che impediscono il PASS:

1. il **conteggio dei requisiti è falso** (49 reali vs 38 dichiarati; 38 `B7-R` reali vs 28 dichiarati; 4 `B7-NFR` reali vs 3 dichiarati) — lezione B6, conteggio dichiarato falso = BUG REALE, qui aggravato perché auto-asserito come "verificato" nella sezione RM-1 del report;
2. un **riferimento interno errato** nel punto che descrive proprio l'atomicità degli AC-GO compositi (doc §8:232).

Più 2 osservazioni non-bloccanti (cross-reference a §10 inesistente; grafia stato-soglie non uniforme inline). Nessun finding FAIL/bloccante.

---

## Problemi BLOCCANTI (FAIL)

Nessuno.

---

## Problemi NON-BLOCCANTI (BUG REALI — vietano il PASS, vanno a Developer)

### F1 — [BUG REALE] Conteggio dei requisiti dichiarato falso (49 reali vs 38)
**Dove**: doc `SPEC_FUNZ_01_B7.md:384` (riga sotto la matrice §9.1); report `REPORT_SPEC_FUNZ_01_B7.md:22, :24-26, :51, :71, :97`.

**Conteggio reale (verificato con grep degli header `### B7-*` e contro-verificato con le righe della matrice §9.1):**
- `B7-R-*` = **38** (B7-R-01 .. B7-R-38)
- `B7-CN-*` = **7** (B7-CN-01 .. B7-CN-07)
- `B7-NFR-*` = **4** (B7-NFR-01 .. B7-NFR-04)
- **Totale = 49 requisiti**

**Dichiarato** (doc §9.1:384 e report): "38 requisiti totali — **28** `B7-R`, 7 `B7-CN`, **3** `B7-NFR`". Tutti e tre i sotto-conteggi e il totale sono falsi. La **matrice §9.1 elenca correttamente 49 righe** (38 R + 7 CN + 4 NFR): il conteggio sotto la matrice contraddice la matrice stessa.

**Aggravante (onestà del report, BASE_COMUNE §8)**: la sezione "Applicazione RM-1 a me stesso" del report (`:97`) dichiara «"38 requisiti, 28/7/3" — conteggio fatto sugli ID effettivamente scritti nel documento (**B7-R-01..38** con i tre namespace)». L'asserzione è auto-smentita: "B7-R-01..38" sono **38 requisiti B7-R da soli**, non 28; il totale con CN e NFR è 49. Un claim dichiarato "verificato sugli ID reali" che riporta un dato falso viola l'onestà claim→evidenza.

**Impatto sull'asse di tracciabilità**: è esattamente il pattern della lezione B6 (conteggio dichiarato falso). Non rompe le citazioni a riga, ma è un fatto interno falso ripetuto in 6 punti fra doc e report.

**Correzione suggerita**: correggere il conteggio in **49 requisiti totali — 38 `B7-R`, 7 `B7-CN`, 4 `B7-NFR`** in tutte le occorrenze (doc §9.1:384; report `:22, :24-26, :51, :71, :97`) e rifare l'auto-check RM-1 sul conteggio reale.

### F2 — [BUG REALE] Riferimento interno errato agli ID nel paragrafo sull'atomicità degli AC-GO (§8:232)
**Dove**: doc `SPEC_FUNZ_01_B7.md:232`.

Il testo afferma: *"Per i criteri compositi al loro interno (**B7-R-33 pipeline, B7-R-34 dashboard**) le sotto-condizioni sono enumerate dentro il singolo criterio ...; **B7-R-35 (hash all'avvio)** è condizione singola già atomica."*

Gli ID sono **shiftati di -1** rispetto al corpo reale del documento:
- B7-R-33 = "Criterio go-live 9: **target operativo asimmetrico**" (NON pipeline)
- B7-R-34 = "Criterio go-live 10: **pipeline** (composito, 4 sotto-cond.)"
- B7-R-35 = "Criterio go-live 11: **dashboard** (composito, 3 sotto-cond.)"
- B7-R-36 = "Criterio go-live 12: **hash all'avvio** (singola)"

Quindi la frase corretta è "(B7-R-34 pipeline, B7-R-35 dashboard) ...; B7-R-36 (hash all'avvio)". Il REPORT (decisione 3.1, `:41`) usa **gli ID corretti** (B7-R-34/35/36): è la riga 232 del **documento** ad essere sbagliata.

**Impatto**: è un'asserzione interna fattualmente falsa proprio nel punto che illustra l'applicazione del cardine AC-B7-ATOMICITA-GO. Disorienta il lettore sull'esatto requisito composito. Non tocca le citazioni a riga né il cardine edge. Basso impatto, ma è un fatto interno errato → BUG REALE.

**Correzione suggerita**: in §8:232 sostituire "(B7-R-33 pipeline, B7-R-34 dashboard) ...; B7-R-35 (hash all'avvio)" con "(B7-R-34 pipeline, B7-R-35 dashboard) ...; B7-R-36 (hash all'avvio)".

---

## Osservazioni minori (non-bloccanti, NON BUG REALE)

### F3 — [MIGLIORA PERFORMANCE] Cross-reference a una sezione inesistente (§10)
**Dove**: doc `:29`. La nota di confine §1.4 rinvia alla "**§10**" per "la lista completa delle grandezze PENDING-empirico", ma il documento ha **9 sezioni** e la lista PENDING è in **§9.3**. Riferimento rotto. Impatto basso (la lista esiste e si trova facilmente). **Correzione**: cambiare "§10" → "§9.3".

### F4 — [MIGLIORA PERFORMANCE] Grafia dello stato-soglie non uniforme inline (AC-B7-SOGLIE)
**Dove**: doc `:262` (B7-R-30 CVaR), `:267` (B7-R-31 MDD), `:277` (B7-R-33 ρ_sessions), `:317` (B7-NFR-03 L_max).

L'AC-B7-SOGLIE chiede lo **stato esatto** "valore di lavoro provvisorio, **non congelato in Parte VII, riconsiderato post-go-live**". Per B7-R-17 (DSR), B7-R-20 (PBO), B7-R-23 (L_avg) la grafia inline è completa. Per CVaR/MDD/ρ_sessions/L_max la clausola è **troncata** a "valore di lavoro provvisorio" (manca "non congelato in Parte VII, riconsiderato post-go-live").

**Perché NON è BUG REALE**: la provvisorietà NON è omessa per nessuna soglia (tutte dicono almeno "provvisorio") e nessuna è dichiarata "definitiva/validata"; lo **stato esatto completo è consolidato collettivamente** in §9.3:414 («le soglie come **valori di lavoro provvisori non congelati, riconsiderati post-go-live**»), che copre tutte le soglie. Il vincolo sostanziale dell'AC è soddisfatto a livello documento; il difetto è di sola **uniformità formale inline**. **Correzione suggerita** (consigliata): estendere la clausola completa inline a B7-R-30/31/33 e B7-NFR-03.

---

## Esiti dei controlli cardine

### Floor citazioni 100% (AC-G8) — **PASS**
Aperti con Read tutti i capitoli-fonte e verificate token-per-token tutte le citazioni (campione = totale delle citazioni "calde" + tutte le citazioni dei 49 requisiti via matrice §9.1). Esiti puntuali:
- **Cap.5** (`CAP_01_parte_I.md`): B7-R-01 `:71`, B7-R-02 `:73-75`, B7-R-03 `:77`, B7-R-04 `:79`, B7-R-05 `:81`, B7-R-06 `:85`, B7-CN-01 `:69,:85` → tutte risolvono al testo reale.
- **Cap.31**: B7-NFR-01 `:21,:7`, B7-CN-02 `:21`, B7-R-07 `:15-19`, B7-R-08 `:29`, B7-R-09..13 `:31/:33/:35/:37/:39`, B7-R-14 `:41,:43-46`, B7-R-15 `:50`, B7-NFR-03 `:23` → tutte risolvono.
- **Cap.32**: B7-R-16 `:139,:143`, B7-R-17 `:202,:204,:244` → risolvono.
- **Cap.33**: B7-R-18 `:252,:254`, B7-R-19 `:294-298,:322`, B7-R-20 `:304,:308,:344` → risolvono.
- **Cap.34**: B7-R-21 `:352,:354-356,:358`, B7-R-22 `:359,:379-381,:449`, B7-R-23 `:369,:371,:373,:449`, B7-NFR-02 `:445,:447`, B7-NFR-04 `:439,:441` → risolvono.
- **Cap.35**: B7-CN-03 `:457,:459,:461-466,:483-500`, B7-CN-04 `:506,:509-510`, B7-CN-05 `:512-517`, B7-R-24 `:523,:525,:533` → risolvono.
- **Cap.36** (i 12 AC-GO): B7-R-25→`:570`, B7-R-26→`:574` (AC-GO-3), B7-R-27→`:572` (AC-GO-2), B7-R-28→`:576`, B7-R-29→`:578`, B7-R-30→`:580`, B7-R-31→`:582`, B7-R-32→`:584`, B7-R-33→`:586,:609-625,:629-631`, B7-R-34→`:588,:589-592`, B7-R-35→`:594,:595-597`, B7-R-36→`:599`, B7-CN-06→`:601,:602-605`, B7-R-37→`:633`, B7-CN-07→`:637,:641`, B7-R-38→`:645,:647-654,:656` → **tutte risolvono token-per-token**.
- **Sotto-condizioni calde di AC-GO-10** (`:589-592`, 4 sotto-cond.) e **AC-GO-11** (`:595-597`, 3 sotto-cond.) verificate una-a-una contro il CAP: contenuto fedele.
- **Disallineamento numerazione AC-GO-2/3 vs B7-R-26/27**: gestito correttamente. AC-GO-3 (`:574`) = expected net return → B7-R-26; AC-GO-2 (`:572`) = PBO → B7-R-27. La NB esplicita (doc `:244`) e la matrice §9.1 rendono la mappa corretta. **Non è un errore di citazione.**

Nota: F1 e F2 NON intaccano il floor citazioni: sono fatti **interni** (conteggio; riferimento ID), non citazioni ai CAP.

### Confronto-copertura vs perimetro B7 (Sez.8 `NFR-8.*`) — **0 buchi, 0 sconfinamenti, 0 orfani**
Req-v2 di Sez.8 = NFR-8.1 .. NFR-8.11 (**11 req-v2**, coerente con la mappa `c7ce4be`). Copertura verificata:
- NFR-8.1 (DSR) → B7-R-09/16/17/25 ✓
- NFR-8.2 (PBO) → B7-R-10/18/19/20/27 ✓
- NFR-8.3 (E[R_net]>0 + IC bootstrap) → B7-R-01/02/26 ✓
- NFR-8.4 (lifecycle cross-regime |f5|) → B7-R-03/11/28 ✓
- NFR-8.5 (CVaR + MDD) → B7-R-04/30/31 ✓
- NFR-8.6 (checklist 12 AC + GO/NO-GO) → B7-CN-06 + B7-R-25..36 ✓
- NFR-8.7 (r_emit + target asimmetrico) → B7-R-32/33 ✓
- NFR-8.8 (pipeline/dashboard/hash) → B7-R-34/35/36 ✓
- NFR-8.9 (invalidation rate) → B7-R-03 (enumera invalidation rate) ✓
- NFR-8.10 (missed_target rate) → B7-R-03 (enumera missed-target rate) ✓
- NFR-8.11 (π_{t2|t1}) → B7-R-03 (target_2 hit rate) + B7-R-13 (Filtro 5 π_{t2|t1}) ✓

**0 buchi**: ogni NFR-8.* coperto. **0 sconfinamenti**: le sole fonti di prima istanza citate `[DOC-INTERNO]` sono CAP_07 (Cap.31-36) e CAP_01 Cap.5 (grep: 121 occ. CAP_07, 17 occ. CAP_01); CAP_02 Cap.10 compare 2 volte solo come **premessa-invariante** (determinismo bit-exact), non come fonte di requisito; **Cap.30 NON è fonte di alcun `B7-*`** (grep "Fonte … Cap.30" = vuoto), coerente con la nota CARD-FIX-01/F3 e con la mappa (`c7ce4be:122`: Cap.30 fuori perimetro spec). Nessuna materia B5/B6 (schema-dato/canale), B3 (lifecycle state-machine), né determinismo ri-derivato. **0 orfani**: ogni `B7-*` traccia a una riga reale del perimetro.

### Cardine EDGE-PENDING (AC-B7-EDGE) — **rispettato (nessun FAIL del blocco)**
Ricerca attiva delle asserzioni d'esito/edge vietate:
- I verbi vietati ("supera/passa il gate", "DSR è positivo/significativo", "l'edge esiste/confermato", "GO" come verdetto) compaiono **solo** nella nota §1.4 che li **elenca come vietati** (riga 31), mai usati come affermazione.
- Tutte le occorrenze di "GO" sono "go-live" (nome del processo) o "GO/NO-GO" come **nome della decisione che il validator emette** — mai un verdetto asserito da B7.
- **Nessun valore numerico d'esito importato**: gli esempi illustrativi di Cap.32.5 (DSR≈0,042) e Cap.33.5 (PBO≈0,35) NON sono stati portati nella spec (grep dei valori = vuoto).
- B7-R-06 (`:65`) riproduce la **dichiarazione di successo del metodo** (Cap.5:85) col verbo "presenta", ma è esplicitamente chiuso come "criterio di accettazione dichiarato, il cui esito è PENDING-empirico": è il punto più vicino al limite, ma rientra nei verbi ammessi dalla card ("il criterio dichiarato è …") ed è neutralizzato dalla marcatura PENDING. Accettabile.
- 30 marcature "PENDING-empirico"; lista PENDING §9.3 completa (9 voci) + sezione NON-pending corretta.

### AC-B7-VALIDATOR — **presente ed esplicito**
Nota di confine di ruolo in §1.4 (`:25-31`: «B7 NON emette verdetti GO/CONDITIONAL/NO-GO né valori d'edge … esclusiva del ruolo `validator`») + ribadita in B7-CN-06 (`:296-299`). ✓

### AC-B7-SUCCESSO — **rispettato**
B7-CN-01 (`:69-72`) isola il successo del segnale dal risultato economico dell'operatore (esecuzione manuale/stop personale/rollover/qualità feed fuori dal criterio), con doppia citazione `:69, :85`. ✓

### AC-B7-ATOMICITA-GO — **rispettato nel corpo** (vedi F2 per il refuso descrittivo)
12 criteri = 12 ID distinti (B7-R-25 .. B7-R-36). AC-GO-10 (pipeline, 4 sotto-cond. dentro un unico criterio, B7-R-34), AC-GO-11 (dashboard, 3 sotto-cond. dentro, B7-R-35), AC-GO-12 (hash, condizione singola già atomica, B7-R-36): né impacchettati né spacchettati. Il refuso F2 riguarda solo il paragrafo che *descrive* l'applicazione, non l'applicazione stessa.

### RM-1 / RM-3 — conforme (salvo l'aggravante di F1)
Nessun blocco `VERIFICA/PROVE/...` di prima istanza nel documento. Etichette canoniche corrette: `[DOC-INTERNO]`, `[WIKI-HINT, da verificare]`; **nessuna** grafia deprecata `[CODICE-EXISTENTE]` (grep = vuoto). Paper esterni (Bailey-López de Prado 2014; Bailey-Borwein-LdP-Zhu 2017; Politis-Romano 1994; Politis-White 2004; Efron 1987) citati come **riferimento bibliografico del capitolo** `[WIKI-HINT]`, non come fonte di prima istanza (§9.4 + B7-R-16/18/21). 0 conclusioni wiki-only. L'unica frizione RM-1 è l'aggravante di F1 (claim di conteggio "verificato" ma falso).

### RACC-METODO-2 (schema esterno vs decoder canonico) — N/A
Perimetro B7 interamente interno (gate sul log di replay bit-exact); nessuno schema/decoder di sistema esterno in scope (confermato dalla card §0.1). Nessun diff con decoder canonico dovuto.

### F6 (marcatura blocchi) — coerente
Il report dichiara "nessun blocco aperto, nessun `[B-N PROVVISORIO]`"; grep dei marcatori `[B-N PROVVISORIO]` nel doc = vuoto. Nessun requisito dipende da un blocco aperto non marcato. Coerente.

### Cecità preservata (AC-G9) — rispettata
Nessun ID-requisito v2 importato nel documento; nessun conteggio-**target** imposto (il conteggio descrittivo, ancorché errato — F1, è auto-prodotto, non importato); nessuna partizione da v2/chunking nel corpo. ✓

---

## Tabella "Classificazione per il supervisore"

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|-----------------------|
| F1 | Conteggio requisiti dichiarato falso: 49 reali (38 R + 7 CN + 4 NFR) vs "38 — 28/7/3" dichiarati; auto-asserito "verificato" nella sezione RM-1 del report | doc `:384`; report `:22,:24-26,:51,:71,:97` | **BUG REALE** | **Sì (obbligatorio)** |
| F2 | Riferimento interno errato agli ID nel paragrafo sull'atomicità AC-GO: "(B7-R-33 pipeline, B7-R-34 dashboard)…B7-R-35 (hash)" invece di B7-R-34/35/36 | doc `:232` | **BUG REALE** | **Sì (obbligatorio)** |
| F3 | Cross-reference a sezione inesistente: §1.4 rinvia alla "§10" ma la lista PENDING è in §9.3 (doc ha 9 sezioni) | doc `:29` | MIGLIORA PERFORMANCE | In attesa decisione supervisore |
| F4 | Grafia stato-soglie non uniforme inline su B7-R-30/31/33 + B7-NFR-03 (clausola "non congelato…riconsiderato post-go-live" troncata; stato esatto completo presente in §9.3) | doc `:262,:267,:277,:317` | MIGLIORA PERFORMANCE | In attesa decisione supervisore |

> I BUG REALI (F1, F2) vanno sempre a Developer. F3, F4 (MIGLIORA PERFORMANCE): decisione del supervisore. Si raccomanda di accorpare F3 e F4 nel medesimo micro-pass di F1/F2 (costo marginale nullo, migliorano la coerenza del documento).

---

## Applicazione RM-1 a me stesso

- **"Floor citazioni 100% = PASS"** — non assunto: ho aperto con Read `CAP_01_parte_I.md` (offset 60-95) e `CAP_07_parte_VII.md` (righe 1-55, 135-249, 248-347, 348-461, 462-561, 562-661) e confrontato ogni riga citata col costrutto affermato. Alternativa esclusa: una citazione che non risolve → l'avrei marcata finding; nessuna trovata. Limite onesto: ho verificato il contenuto semantico delle righe citate; un singolo refuso di numero-riga residuo è teoricamente possibile ma non riscontrato sul campione (= totale dei requisiti via matrice).
- **"49 requisiti reali, non 38"** — verificato due volte con strumenti indipendenti: (a) grep degli header `### B7-*` con conteggio per namespace (38/7/4); (b) conteggio delle righe `| B7-*` della matrice §9.1 (identico, 38/7/4). I due metodi concordano. Alternativa esclusa: che il documento avesse più ID degli header (assente nella matrice) o viceversa → i due conteggi coincidono, quindi 49 è il numero reale.
- **"0 buchi/sconfinamenti/orfani"** — non assunto: estratti NFR-8.1..NFR-8.11 da `SPEC_FUNZ_01.md@c7ce4be` e mappati uno-a-uno ai B7-*; estratte le fonti citate dal doc via grep (solo CAP_07/CAP_01 come prima istanza; CAP_02 Cap.10 = premessa; Cap.30 = nessuna fonte). Alternativa non esclusa con certezza: la copertura di NFR-8.9/8.10/8.11 poggia su B7-R-03 ("metriche di lifecycle" che *enumera* invalidation/missed-target/target_2 hit rate) + B7-R-13 — è copertura per enumerazione dentro un requisito atomico, coerente con la natura batch dei KPI di lifecycle alla fonte (Cap.5:77). La giudico copertura valida; se il supervisore ritenesse che NFR-8.9/10/11 richiedano ID dedicati sarebbe una scelta di granularità, non un buco di copertura (la materia c'è).
- **"Cardine edge-PENDING rispettato"** — verificato con grep dei verbi vietati (solo nella nota che li elenca) + grep dei valori numerici d'esito illustrativi dei CAP (assenti nella spec) + conteggio marcature PENDING (30). Alternativa esclusa: un'asserzione d'esito mascherata → ispezionato B7-R-06 (il caso-limite), risulta chiuso come criterio dichiarato + PENDING.
- **Confine di sede**: audit interamente documentale in CLI; **nessuna** probe DAPI eseguita (divieto CLI di zelo rispettato).

---

## Lista "Empirico-CLI da verificare"

**VUOTA** (attesa). L'audit è documentale no-DAPI; la spec consolida criteri/definizioni già chiusi nei CAP frozen e non introduce fatti empirici nuovi. Tutte le grandezze d'esito sono correttamente marcate PENDING-empirico (validator/FASE-D) dal Developer e non vanno verificate in questa sede.

---

## Riepilogo conteggi (verificato vs dichiarato)

| Voce | Dichiarato (doc+report) | Reale (verificato) | Esito |
|---|---|---|---|
| Totale requisiti | 38 | **49** | ✗ falso (F1) |
| `B7-R-*` | 28 | **38** | ✗ falso (F1) |
| `B7-CN-*` | 7 | 7 | ✓ |
| `B7-NFR-*` | 3 | **4** | ✗ falso (F1) |
| Citazioni risolvibili (floor) | 100% | 100% | ✓ PASS |
| Buchi copertura Sez.8 | 0 | 0 | ✓ |
| Sconfinamenti | 0 | 0 | ✓ |
| Orfani | 0 | 0 | ✓ |
| Asserzioni d'esito/edge | 0 | 0 | ✓ cardine rispettato |

**VERDETTO ITERAZIONE 1: CONDITIONAL** — 2 BUG REALI (F1, F2), 0 bloccanti, 2 osservazioni MIGLIORA PERFORMANCE (F3, F4). Floor citazioni, copertura e cardine edge-PENDING tutti superati.

---

# RE-REVIEW DELTA — ITERAZIONE 2 — VERDETTO: **PASS**

> **Oggetto**: delta del rework iter.2, commit `46cab7e` (risposta alla CONDITIONAL iter.1 `98780f9`).
> **Sede**: **CLI** (GOV-SURFACES-01) — audit documentale **no-DAPI**, divieto CLI attivo (nessuna probe di zelo).
> **Modalità**: re-review del DELTA (non review piena da zero). Verifica mirata dei 4 fix (F1-F4) + ricerca attiva di regressioni sul diff `46cab7e`.
> **Metodo**: ricontati indipendenti (grep header `### B7-*` + righe matrice §9.1), Read puntuale delle righe toccate, ispezione integrale del diff (`git show 46cab7e`). Capitoli-fonte NON riaperti (frozen G-09): il delta dichiara e mostra di non toccarli.

## Sintesi
Tutti e 4 i finding della iter.1 sono **risolti correttamente**. Il delta e' **chirurgico e circoscritto** ai 4 fix (7 righe nel documento + correzioni di conteggio/RM-1 nel report + nuova sezione narrativa iter.2). **0 regressioni**: nessuna proposizione di requisito, nessun ID-requisito, nessuna citazione-fonte (pin `path:line`) e' cambiata; il cardine edge-PENDING resta intatto (nessuna asserzione d'esito introdotta); il floor citazioni 100% resta valido sui requisiti toccati (i pin non sono stati alterati). I 2 BUG REALI che vietavano il PASS in iter.1 sono eliminati => **0 BUG REALE in tabella** => PASS (BASE_COMUNE §4).

## Esito dei 4 fix

### F1 (BUG REALE) — Conteggio requisiti — **RISOLTO**
Riconteggio indipendente sul documento a HEAD:
- `### B7-R-*` = **38** (B7-R-01..38, contigui, nessun buco) — grep header.
- `### B7-CN-*` = **7** (B7-CN-01..07).
- `### B7-NFR-*` = **4** (B7-NFR-01..04).
- Righe matrice §9.1 (`| B7-`) = **49**. **Totale = 49 = 38 R + 7 CN + 4 NFR.** I due metodi (header vs matrice) concordano.

Il dichiarato e' ora **49 (38 R + 7 CN + 4 NFR) in tutte le occorrenze sostanziali**:
- doc §9.1 `:384` -> "49 requisiti totali — 38 `B7-R-*`, 7 `B7-CN-*`, 4 `B7-NFR-*`" OK
- report §1 `:22` (totale 49), `:24` (38 R), `:25` (7 CN), `:26` (4 NFR) OK
- report Misura/DOPO `:51` (49) OK
- report tabella AC-G1 `:71` (49) OK
- report "Applicazione RM-1 a me stesso" `:97`: l'asserzione auto-smentita e' **corretta** — ora "49 requisiti, 38/7/4 … 38 `B7-R-*` (B7-R-01..38)", coerente con gli ID reali (non piu' "28"). L'aggravante RM-1 (claim "verificato" su dato falso) e' rimossa.
- I due residui "28/7/3" rimasti (report `:97` e `:123`) sono **riferimenti storici espliciti** ("il conteggio precedente era errato" / colonna Prima->Dopo della tabella iter.2): narrativi e veri, non asserzioni di conteggio corrente. Corretto lasciarli.

### F2 (BUG REALE) — ID atomicita' AC-GO (doc `:232`) — **RISOLTO**
doc `:232` ora: "(B7-R-34 pipeline, B7-R-35 dashboard) … B7-R-36 (hash all'avvio)". Confronto col corpo reale:
- B7-R-34 `:281` = "Criterio go-live 10: **pipeline** (composito)" OK
- B7-R-35 `:286` = "Criterio go-live 11: **dashboard** (composito)" OK
- B7-R-36 `:291` = "Criterio go-live 12: **hash** bundle frozen all'avvio (singola)" OK
Gli ID corrispondono token-per-token al corpo. Lo shift -1 e' eliminato.

### F3 (MIGLIORA) — Cross-ref (doc `:29`) — **RISOLTO**
doc `:29` ora rinvia a **§9.3**. §9.3 esiste (`:400` "Lista PENDING-empirico (marcata, MAI asserita)"). **Nessun residuo "§10"** nel documento (grep vuoto). Il documento ha 9 sezioni; il rinvio rotto e' corretto.

### F4 (MIGLIORA) — Stato-soglie inline — **RISOLTO**
La clausola completa "valore di lavoro provvisorio, **non congelato in Parte VII, riconsiderato post-go-live**" e' ora presente inline sui 4 requisiti target:
- B7-R-30 (CVaR) `:262` OK · B7-R-31 (MDD) `:267` OK · B7-R-33 (rho_sessions) `:277` OK · B7-NFR-03 (L_max) `:317` OK.
Le 3 occorrenze "troncate" residue (righe `:146/:167/:190`) sono i **titoli-header** di B7-R-17/20/23 che recano l'etichetta breve "(valore di lavoro provvisorio)"; il **corpo** di quei requisiti (`:147`, `:168`) porta gia' la clausola completa. Nessun corpo troncato residuo. Uniformita' raggiunta.

## 0 regressioni — verifica sul diff `46cab7e`
- **Diff documento = 7 righe modificate**, tutte e sole i 4 fix (1×F1 conteggio §9.1, 1×F2 ID, 1×F3 §10->§9.3, 4×F4 soglie). Nessun'altra riga del documento toccata.
- **Pin `path:line` invariati**: 0 occorrenze di `[DOC-INTERNO ...]` nelle righe +/- del diff doc. Tutte le citazioni-fonte sono righe non toccate => il floor citazioni 100% (PASS in iter.1) regge per costruzione sui requisiti toccati.
- **Proposizioni di requisito invariate**: nei 4 fix F4 i valori numerici delle soglie (-100 pt, 200 pt, 0,60, 30 s), gli operatori di confronto e la struttura restano identici; si aggiunge solo la coda della clausola di provvisorieta'. F2 cambia solo 3 ID in una frase **descrittiva** (paragrafo introduttivo §8), non dentro un requisito. F1 tocca una riga di conteggio descrittivo. F3 tocca la nota di confine.
- **Cardine edge-PENDING intatto**: tutte le righe modificate conservano "(Esito = PENDING-empirico)"/"PENDING-empirico"; la riga F3 e' proprio la nota "B7 NON emette verdetti GO/CONDITIONAL/NO-GO" e il suo contenuto di divieto e' invariato. **Nessuna asserzione d'esito/edge introdotta** dal delta.
- **ID-requisito invariati**: nessun header `### B7-*` aggiunto/rimosso/rinominato (il riconteggio coincide con quello atteso 38/7/4 = 49).
- **Diff report**: correzioni di conteggio F1 + correzione dell'asserzione RM-1 (resa veritiera) + nuova sezione narrativa "Iterazione 2 — risposta ai finding". Nessuna nuova asserzione di verifica empirica; nessun blocco `VERIFICA/PROVE` di prima istanza introdotto.
- **Freeze G-09**: il delta non tocca alcun file in `docs/methodology_v2/` (diff su 3 file: doc spec, report, DEV_STATUS). I capitoli-fonte restano congelati.

## Applicazione RM-1 a me stesso (delta)
- **"49 = 38 R + 7 CN + 4 NFR"** — non assunto: ricontato due volte con strumenti indipendenti a HEAD — (a) grep degli header `### B7-R-/CN-/NFR-` (38/7/4); (b) conteggio righe `| B7-` della matrice §9.1 (49). I due concordano. Alternativa esclusa: header senza riga in matrice (o viceversa) -> i conteggi coinciderebbero solo se la corrispondenza e' 1:1, ed e' cosi'.
- **"0 regressioni"** — non assunto: ispezionato l'intero diff `46cab7e` riga per riga (`git show`), enumerato ogni `+`/`-`; confermato che le sole modifiche sostanziali sono i 4 fix. Limite onesto: ho verificato il diff di QUESTO commit; un'eventuale regressione introdotta in un commit precedente alla iter.1 sarebbe stata gia' coperta dalla review iter.1 (PASS-grade su tutto tranne F1-F4).
- **"pin invariati"** — grep `DOC-INTERNO` sulle righe +/- del diff doc = 0; quindi nessuna citazione-fonte modificata.
- **"cardine edge-PENDING intatto"** — verificato che ogni riga modificata che riguarda una grandezza d'esito conserva il marcatore PENDING; la riga F3 conserva il divieto di verdetti.
- **Confine di sede**: audit interamente documentale in CLI; nessuna probe DAPI (divieto CLI di zelo rispettato).

## Tabella "Classificazione per il supervisore" (delta iter.2)

| # | Problema | file:riga | Classificazione | Mandare a Development? |
|---|----------|-----------|-----------------|-----------------------|
| — | Nessun finding nuovo. F1, F2 (BUG REALE iter.1) risolti; F3, F4 (MIGLIORA iter.1) risolti. | — | — | No |

**0 BUG REALE in tabella, 0 bloccanti.**

## Lista "Empirico-CLI da verificare"
**VUOTA** (attesa). Il delta e' di sola accuratezza documentale; non introduce fatti empirici.

---

**VERDETTO RE-REVIEW DELTA ITER.2: PASS.** I 4 fix (F1, F2, F3, F4) sono risolti correttamente e verificati indipendentemente; conteggio reale = **49 (38 R + 7 CN + 4 NFR)** in tutte le occorrenze sostanziali; **0 regressioni** (nessuna proposizione/ID/pin cambiata, cardine edge-PENDING intatto, floor citazioni 100% preservato). Combinato con la iter.1 (floor citazioni, copertura Sez.8, cardine edge-PENDING tutti PASS-grade), il blocco SPEC-FUNZ-01-B7 e' **PASS pieno**.
