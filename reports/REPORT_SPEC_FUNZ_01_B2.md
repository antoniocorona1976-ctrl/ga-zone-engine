# REPORT — SPEC-FUNZ-01-B2 — Payload del segnale

> **Conferma letture obbligatorie** (in quest'ordine, prima di scrivere): ho letto `tasks/METODO.md` (RM-1..RM-4 + RACC-METODO-2), `.claude/BASE_COMUNE.md` (ciclo, sede CLI, onestà claim→evidenza §8), `.claude/agents/spec_developer.md` (il mio ruolo), `tasks/ACTIVE_TASK.md` (task card B2, autoritativa).
>
> **Conferma cecità**: ho lavorato **in cieco** dal solo Cap.6 (6.1/6.2/6.3) di `docs/methodology_v2/CAP_02_parte_II.md`. **Non** ho aperto, letto, consultato o citato `SPEC_FUNZ_01.md`, alcun `*_v1_storico*`, `SPEC_FUNZ_01_B1.md` o altri `SPEC_FUNZ_01_B*.md`, né alcun file di chunking/pianificazione (`PROPOSTA_SUDDIVISIONE_SPEC*.md`). Gli ID requisito sono auto-assegnati da zero (schema `B2-R-NN` / `B2-CN-NN`).

---

## 1. Cosa è stato prodotto

`docs/spec_funzionale/SPEC_FUNZ_01_B2.md`: la specifica funzionale del **payload del segnale** come oggetto contrattuale immutabile, blocco 2/8 della spec ricostruita a blocchi. **42 requisiti** atomici, così ripartiti:

- **37 requisiti `B2-R-NN`** (schema-payload): struttura della tupla (B2-R-01); campi e loro domini/vincoli — `signal_id` (B2-R-02..04), `timestamp_emission` (B2-R-05..06), `direction` (B2-R-07), `entry_zone` (B2-R-08..09, B2-R-35), `target_1`/`target_2` (B2-R-10..20), `target_2_type` (B2-R-21..22), `stop_loss`/d_stop (B2-R-23..24), `stop_type` (B2-R-25..27), `setup_class`+filtro 80pt come qualificazione (B2-R-28..29), Δt_cromosoma/T_touch_max come campi-parametro (B2-R-30..31); banda b (B2-R-32..34, B2-R-36..37).
- **5 requisiti `B2-CN-NN`** (invarianti/compliance): vincolo geometrico d_stop>b (B2-CN-01); immutabilità post-emissione (B2-CN-02..03); segnale unico attivo (B2-CN-04); sostituzione-non-edit (B2-CN-05).

Sezioni del documento: 1 intestazione/scopo/schema-ID; 2 segnale come oggetto-payload immutabile; 3 campi del payload; 4 banda di ingresso b; 5 invariante immutabilità; 6 segnale unico attivo e sostituzione; 7 nota RM-1; 8 matrice di tracciabilità + nota di rinvio.

`reports/REPORT_SPEC_FUNZ_01_B2.md`: questo report.

## 2. Ipotesi di partenza

- Ho lavorato **in cieco** dal solo Cap.6 di `CAP_02_parte_II.md` (vedi conferma in testa). Mi sono appoggiato esclusivamente alla task card + al CAP-fonte.
- CAP-02 è autoritativo e frozen (PASS `a1625df`): non l'ho riaperto per ri-verificarne la matematica né l'ho modificato (sola lettura). Ho verificato **token-per-token** ogni numero di riga citato leggendo il Cap.6 (righe 13-89 del file).
- I pin-riga del §2 della card sono puntatori di lavoro: li ho confermati sul CAP. Tutti hanno risolto esattamente; nessuna correzione di riga è stata necessaria.

## 3. Decisioni rilevanti

- **Atomicità N1**: ho spezzato i campi multi-vincolo in più requisiti. Esempi: `target_1`/`target_2` hanno generato 11 requisiti distinti (obbligatorietà ×2, distinzione, multiplo-di-5 ×2, ordine long ×2, ordine short ×2, ancoraggio strutturale, natura informativa Q-05 Cl.2) invece di un unico enunciato; `signal_id` 3 requisiti (univocità, opacità/non-riuso, scope orizzonte); banda b 6 requisiti.
- **Classificazione R vs CN**: ho reso come `B2-CN` (invarianti strutturali) le proprietà a rilevanza contrattuale — immutabilità, segnale unico attivo, sostituzione-non-edit, d_stop>b — coerentemente con AC-G11. I campi-schema e i loro domini sono `B2-R`.
- **Confine payload vs lifecycle/emissione (rinvii deliberati)**: ho consolidato `target_2` **come campo del payload** (informazione strutturale, Q-05 Cl.2) e ho **rinviato** il suo raggiungimento *come evento*; ho consolidato Δt_cromosoma/T_touch_max **come campi/parametri** e ho **rinviato la semantica dei timer**; ho consolidato `setup_class` e l'**associazione** del filtro 80pt al campo, **rinviando la regola di emissione**; ho consolidato la sostituzione **come proprietà del payload** (nuovo id + nuova tupla, non edit) **rinviando la meccanica delle transizioni di stato**. Tutti i rinvii sono esplicitati nella nota §8.2 e marcati inline nel documento con frasi in corsivo.
- **Cautela RM-1**: non ho introdotto alcuna dichiarazione "verificato X" di prima istanza (sezione 7 del documento). Ogni requisito è un richiamo a un fatto già chiuso nel Cap.6.

## 4. Misura prima/dopo

Greenfield di consolidamento del perimetro payload (Cap.6.1/6.2/6.3):

- **PRIMA**: il contratto del payload era disperso nella prosa del Cap.6 della metodologia, non leggibile come elenco di requisiti tracciati da un lettore esterno.
- **DOPO**: **42 requisiti** atomici, ciascuno tracciato a riga del Cap.6 e con valore operativo dichiarato, più matrice di tracciabilità e nota di rinvio. Copertura del perimetro: 6.1 (tutti i 12 campi + banda + filtro-qualificazione), 6.2 (immutabilità), 6.3 (segnale unico + sostituzione-come-proprietà). Nessun "prima" quantitativo (greenfield).

## 5. Domande aperte

Nessuna. Il perimetro Cap.6 (6.1/6.2/6.3) è interamente risolvibile dai soli contenuti del CAP-fonte; non ho incontrato blocchi (fonte mancante, ambiguità che richieda decisione di Planner/AC, requisito non derivabile). Nessun marcatore `[B-N PROVVISORIO]` è quindi presente nel documento.

## 6. Criterio di rollback

B2 è un file autonomo (`SPEC_FUNZ_01_B2.md`). Per annullarlo basta rimuovere il file e il relativo report e azzerare `DEV_STATUS.md`: nessun altro blocco vi dipende (B1 è chiuso e non è stato toccato; B3..B8 non esistono ancora). Nessun CAP è stato modificato (freeze G-09 rispettato). L'assemblaggio finale è un task separato post-B8, quindi il rollback di B2 non impatta documenti consolidati.

---

## Tabella verifica AC

| AC | Stato | Evidenza (`SPEC_FUNZ_01_B2.md`) |
|----|-------|----------------------------------|
| AC-G1 (atomicità N1) | OK | ogni requisito = 1 proposizione; target spezzati in B2-R-10..20; signal_id in B2-R-02..04; banda in B2-R-32..37 |
| AC-G2 (tracciabilità obbligatoria) | OK | ogni requisito porta `[DOC-INTERNO CAP_02_parte_II.md:<riga>]`; matrice §8.1 colonna citazione |
| AC-G3 (valore operativo obbligatorio) | OK | ogni requisito ha riga *Valore operativo*; matrice §8.1 colonna dedicata |
| AC-G4 (divieto "verificato X" RM-1) | OK | §7 dichiara l'assenza di "verificato X" di prima istanza; nessun blocco RM-1 necessario |
| AC-G5 (etichette RM-3 fonti esterne) | OK | nessuna fonte esterna usata (§7); vacuamente soddisfatto |
| AC-G6 (grafia canonica) | OK | usata solo `[DOC-INTERNO ...]`; nessuna grafia storica `[CODICE-EXISTENTE ...]` |
| AC-G7 (floor citazioni 100%) | OK | pin verificati token-per-token sul Cap.6 (righe 13-89): :17,:19,:23,:25,:27,:29,:31,:33,:35,:37,:39,:41,:43,:47,:49,:51,:53,:55,:59,:63,:69,:73,:77,:79,:81,:83,:7,:9,:5 |
| AC-G8 (cecità preservata) | OK | ID auto-assegnati da zero; nessuna apertura di spec preesistenti/B1/chunking (conferma in testa) |
| AC-G9 (scope "tutto e solo") | OK | coperto tutto Cap.6.1/6.2/6.3; nessuno sconfinamento in B3/B4/B5 (rinvii in §8.2 e inline) |
| AC-G10 (matrice + nota di rinvio) | OK | matrice §8.1 (ID/proposizione/citazione/valore); nota di rinvio §8.2 |
| AC-G11 (invarianti come tali) | OK | immutabilità/unico-attivo/d_stop>b resi come `B2-CN`; {structural,synthetic} reso come dominio di campo (B2-R-21,22,25,26) |

## Applicazione RM-1 a me stesso

Asserzioni fattuali che ho scritto e relativa evidenza:

- **"Ho verificato token-per-token i pin del §2"** — PROVE: ho letto le righe 1-302 del file (che includono integralmente il Cap.6, righe 13-89) e confrontato ogni numero di riga citato col contenuto effettivo. ALTERNATIVE ESCLUSE: pin che non risolvono — escluso, tutti risolvono. ALTERNATIVE NON ESCLUSE: nessuna entro il perimetro Cap.6; le righe oltre la 302 (Cap.7-11) sono fuori perimetro e non citate.
- **"Ho lavorato in cieco"** — PROVE: non ho invocato Read/Glob/Grep su alcun file di spec preesistente, B1, o chunking; le sole letture sono METODO, BASE_COMUNE, spec_developer.md, ACTIVE_TASK.md, CAP_02_parte_II.md. ALTERNATIVE ESCLUSE: traccia di apertura involontaria — esclusa. ALTERNATIVE NON ESCLUSE: nessuna.
- **"Nessuna fonte esterna usata"** — PROVE: il documento non contiene `[WIKI-HINT]` né riferimenti a MiFID/Telegram/Directa/IDEM; il payload è materia interna. ALTERNATIVE ESCLUSE: riferimento esterno implicito non etichettato — escluso.
- **"42 requisiti"** — PROVE: conteggio diretto B2-R-01..37 (37) + B2-CN-01..05 (5) = 42. ALTERNATIVE NON ESCLUSE: nessuna.

Nessuna mia asserzione richiede accesso DAPI o filesystem locale (audit no-DAPI). Lista "Empirico-CLI da verificare": **vuota**.
