# REPORT - SPEC-FUNZ-01-B1 (Ambito e operatore, ricostruzione cieca modalita B, blocco 1/8)

> Letture obbligatorie confermate, in quest ordine: tasks/METODO.md (RM-1..RM-4 + RACC-METODO-2), .claude/BASE_COMUNE.md, .claude/agents/spec_developer.md, tasks/ACTIVE_TASK.md. La task card e stata trattata come autoritativa.
> Output: docs/spec_funzionale/SPEC_FUNZ_01_B1.md + questo report.

---

## 1. Cosa e stato prodotto

Documento SPEC_FUNZ_01_B1.md con 34 requisiti atomici che consolidano il perimetro ambito e operatore dei Capitoli 1-3 di CAP_01_parte_I.md (chiuso PASS, SHA b76c32c, freeze G-09 - non modificato):

- Sezione 2 Ambito del prodotto-segnale (15 req., B1-R-01..15): oggetto (segnali long/short), strumento FIB/FTSE MIB/IDEM, sessione 8:00-22:00 CET come ambito, perimetro di emissione, target operativo nelle due formulazioni (500 punti / 70% movimento strutturale) con definizione e ancoraggio del movimento strutturale e soglia minima asimmetrica, natura intraday + estensione multiday + tetto 2 giorni, contesto cross-index per regime/direzione/rischio sistemico.
- Sezione 3 Vincolo strutturale solo emissione (3 req., B1-CN-01..03): no esecuzione ordini (strutturale), pubblicazione su canale di notifica, confine di responsabilita all operatore.
- Sezione 4 Profilo operatore e vincoli (10 req., B1-CN-04, B1-CN-05, B1-R-16..21, B1-NFR-01): retail MiFID II, mobile, discontinuo, interpretabilita segnali, 1 contratto, commissione 5 EUR/op, equivalenza punti, distinzione stop strutturale/personale, rollover di ambito.
- Sezione 5 Strumento FIB (2 req., B1-R-22, B1-NFR-02): moltiplicatore 5 EUR/pt; griglia 5pt con cautela RM-1 esplicita.
- Sezione 6 Canale e infrastruttura di ambito (5 req., B1-NFR-03/04, B1-R-23/24/25): PC mobile, feed da Directa, storico FIB, dati cross-index, canale Telegram (ambito).
- Sezione 7 matrice di tracciabilita completa (34 righe) + nota di rinvio (11 materie di Cap.1-3 deliberatamente rinviate ad altri blocchi).

Conteggio per famiglia: B1-R = 25, B1-CN = 5, B1-NFR = 4. Totale 34.

## 2. Ipotesi di partenza

- Ho lavorato in cieco (modalita B): derivati i requisiti dai soli Cap.1-3 di CAP_01_parte_I.md. Non ho aperto, letto, citato o parafrasato SPEC_FUNZ_01.md, alcun file _v1_storico, ne alcun file di pianificazione/chunking (PROPOSTA_SUDDIVISIONE_SPEC*). Gli ID sono auto-assegnati da zero secondo lo schema Sez.1, non importati.
- I fatti dell eredita autoritativa (Sez.2 task card) e le decisioni chiuse Q-01..Q-04 sono stati trattati come autoritativi: citati col loro livello-fonte, non ri-verificati ne ri-derivati.
- CAP-01 e frozen: l ho letto in sola lettura per le citazioni, senza modificarlo ne riauditarlo.

## 3. Decisioni rilevanti

- Atomicita N1 applicata spezzando concern impacchettati: il contesto cross-index (CAP :17, tre finalita) -> R-13/14/15; il target (CAP :11) -> R-05 (500 punti) e R-06 (70%) + R-07 (definizione) + R-08 (ancoraggio) + R-09 (soglia minima); le commissioni (CAP :25) -> CN-05 (importo) e R-19 (equivalenza in punti); il vincolo solo emissione (CAP :15) -> CN-01 (no esecuzione) + CN-02 (pubblica su canale) + CN-03 (confine responsabilita).
- Vincolo strutturale evidenziato (AC-G11): no esecuzione ordini reso come requisito compliance B1-CN-01 con la qualifica esplicita vincolo strutturale, non scelta implementativa rivedibile.
- Cautela RM-1 sul tick 5pt (B1-NFR-02): il CAP-fonte non asserisce tick 5pt; ho marcato la proposizione con il blocco RM-1 a 4 righe (alternativa non esclusa: tick reale diverso, conferma rinviata a B6/CAP-DATA), invece di asserirla come verificata.
- Rinvii deliberati (nota Sez.7.2): 11 materie presenti nei Cap.1-3 ma di pertinenza di altri blocchi (payload, dominio b/d_stop, timer/raw touch, dettaglio Telegram, policy rollover, runtime sessione, storico/cross-index/interfacce Directa di dettaglio, Cap.4 compute, Cap.5 gate) - annotate con destinazione per distinguere omissione voluta da gap.
- Etichette RM-3: MiFID II, Borsa Italiana/IDEM, Directa, Telegram marcati [WIKI-HINT, da verificare], mai fonte unica; ogni requisito regge sul CAP.

## 4. Misura prima/dopo

Greenfield di consolidamento, non modifica del motore. PRIMA: il contenuto di ambito/operatore era disperso nella prosa dei Cap.1-3 di CAP_01_parte_I.md, non leggibile come requisiti discreti da un lettore esterno. DOPO: 34 requisiti atomici tracciati riga-per-riga al CAP-fonte, ciascuno con valore operativo dichiarato, con matrice di tracciabilita e nota di rinvio. Copertura del perimetro Cap.1-3: tutte le proposizioni di prodotto dei tre capitoli risultano consolidate o esplicitamente rinviate (Sez.7.2). Nessuna metrica GA inventata.

## 5. Domande aperte

- Tick 5pt non asserito nel CAP (B1-NFR-02): l unica cautela RM-1 del blocco. Non e un blocco operativo per B1 (l ho marcata, non asserita); la conferma del tick e materia di B6/CAP-DATA. Nessun marcatore [B-N PROVVISORIO] e necessario perche non e un blocco che contamina altri requisiti: e una cautela locale e autocontenuta.
- Nessun altro blocco ne ambiguita irrisolvibile dai documenti. Il confronto-copertura con la v2 e compito esclusivo del Reviewer (modalita B): non l ho tentato.

## 6. Criterio di rollback

B1 e un file autonomo (SPEC_FUNZ_01_B1.md) non ancora ricomposto con altri blocchi (l assemblaggio e un task dedicato post-B8). Per annullare B1 basta rimuovere docs/spec_funzionale/SPEC_FUNZ_01_B1.md + reports/REPORT_SPEC_FUNZ_01_B1.md e azzerare DEV_STATUS.md: nessun altro file di prodotto dipende da B1, nessun CAP e stato toccato (freeze G-09 rispettato), 00_indice.md non e stato toccato. L impatto su B2..B8 e nullo perche sono blocchi separati non ancora prodotti.

---

## Tabella di verifica AC

| AC | Esito | Evidenza |
|---|---|---|
| AC-G1 - Atomicita (N1) | OK | ogni requisito e una proposizione singola; concern spezzati: cross-index Sez.2 B1-R-13/14/15, target B1-R-05..09, commissioni B1-CN-05 + B1-R-19, solo-emissione B1-CN-01/02/03 |
| AC-G2 - Tracciabilita obbligatoria | OK | ogni requisito ha [DOC-INTERNO CAP_01_parte_I.md:<riga>]; sintesi in matrice Sez.7.1 |
| AC-G3 - Valore operativo obbligatorio | OK | ogni requisito ha campo Valore operativo; vedi Sez.2-6 |
| AC-G4 - Divieto verificato X di prima istanza | OK | nessuna dichiarazione verificato X di prima istanza; tick 5pt marcato col blocco RM-1 a Sez.5 B1-NFR-02 |
| AC-G5 - Etichette RM-3 su fonti esterne | OK | MiFID II, IDEM/Borsa Italiana, Directa, Telegram tutti [WIKI-HINT, da verificare], mai fonte unica (B1-R-02/03, B1-CN-04/05, B1-NFR-04, B1-R-25) |
| AC-G6 - Grafia canonica citazioni | OK | usato [DOC-INTERNO ...] e [WIKI-HINT, da verificare]; nessuna grafia storica [CODICE-EXISTENTE] presente |
| AC-G7 - Floor citazioni 100% | OK | righe :9,:11,:13,:15,:17,:23,:25,:27,:31,:33,:39,:41,:43,:45,:47 riverificate token-per-token contro CAP_01_parte_I.md; Q-02/Q-04 verificate in tasks/QUESTIONS.md:11,31 |
| AC-G8 - Cecita preservata | OK | nessun ID importato (schema auto-assegnato B1-* da zero, Sez.1); nessuna apertura di v2/_v1_storico/chunking (vedi Sez.2 report) |
| AC-G9 - Scope invariato (tutto e solo) | OK | requisiti solo su Cap.1-3; Cap.4/5 e materie di altri blocchi rinviate in Sez.7.2; nessun req. sconfina |
| AC-G10 - Matrice di tracciabilita finale | OK | matrice 34 righe Sez.7.1 + nota di rinvio Sez.7.2 |
| AC-G11 - Vincolo strutturale evidenziato | OK | B1-CN-01 rende no esecuzione ordini come vincolo strutturale esplicito non rivedibile (Sez.3) |

## Applicazione RM-1 a me stesso

- Letto i 4 file obbligatori -> evidenza: contenuto integrale letto con Read in questa sessione (METODO, BASE_COMUNE, spec_developer, ACTIVE_TASK).
- Citazioni :<riga> verificabili token-per-token -> ho letto CAP_01_parte_I.md per intero (86 righe) in questa sessione; ogni riga citata corrisponde al testo letto. Alternativa esclusa: che una riga citata non contenga il fatto - esclusa per ispezione diretta.
- Q-02/Q-04 esistono e sono chiuse -> grep su tasks/QUESTIONS.md ha restituito Q-02 ... CHIUSA (riga 11) e Q-04 ... CHIUSA (riga 31). Alternativa esclusa: Q inesistente o aperta - esclusa dall output del grep.
- Cecita mantenuta -> non ho invocato Read/Grep su SPEC_FUNZ_01.md, file _v1_storico, o file di chunking. Il Reviewer la verifica cercando tracce (ID importati, frasi identiche); io dichiaro l assenza di accesso.
- Tick 5pt -> NON asserito come verificato; marcato come assunzione con alternativa non esclusa (tick reale diverso). Coerente con RM-1.
