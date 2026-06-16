# REPORT — SPEC-FUNZ-01-B4 (Emissione & consegna, blocco 4/8)

> Track: Business-spec (SPEC-FUNZ). Sede: CLI. Tag commit: [SPEC-FUNZ-01-B4] + estensione [SPEC-FUNZ-01-B4-EXT].
> Documento: docs/spec_funzionale/SPEC_FUNZ_01_B4.md — 61 requisiti (40 B4-R + 14 B4-CN + 7 B4-NFR): 50 della parte CAP_02 Cap.8-9 (PASS c3be05e) + 11 dell'estensione consegna CAP_06 Cap.29.
>
> NOTA DI STRUTTURA: le sezioni 1-6, la tabella AC-G1..G11 e l'Applicazione RM-1 a me stesso QUI SOTTO si riferiscono alla parte CAP_02 Cap.8-9 (B4 base, PASS c3be05e) e restano invariate come storico. La sezione di ESTENSIONE (consegna CAP_06 Cap.29) e in fondo al report, intestata "## Estensione consegna — SPEC-FUNZ-01-B4-EXT".

## Conferma letture obbligatorie

Confermo di aver letto, in questo ordine, prima di agire: (1) tasks/METODO.md (RM-1..RM-4 + RACC-METODO-2 + Enforcement); (2) .claude/BASE_COMUNE.md (ciclo, sede CLI per la spec, onesta claim->evidenza par.8); (3) .claude/agents/spec_developer.md (il mio ruolo); (4) tasks/ACTIVE_TASK.md (la card B4: perimetro par.1, eredita par.2, AC-G1..G11 par.3, sezioni par.4, report par.5, out-of-scope par.6, done-when par.7); (5) docs/methodology_v2/CAP_02_parte_II.md Cap.8 (8.1-8.4, righe :179-227) + Cap.9 (9.1-9.6, righe :231-281), per la verifica delle citazioni; (6) il documento da verificare/completare docs/spec_funzionale/SPEC_FUNZ_01_B4.md (379 righe, gia scritto).

## NOTA DI PROVENIENZA (RM-1, BASE_COMUNE par.8) — onesta tassativa

Questa passata NON ha derivato i requisiti di B4. Il documento SPEC_FUNZ_01_B4.md era gia scritto e completo su disco come file untracked: e stato prodotto da una passata Developer precedente, in cieco (modalita B), interrotta da un errore di rete PRIMA di produrre il REPORT, committare e scrivere READY_FOR_REVIEW.

Il compito di questa passata e stato verificare e completare il deliverable, NON riscriverlo. Concretamente, questa passata:
- ha verificato il documento esistente su quattro assi (cecita, completezza strutturale, citazioni campionate, scope) e ne attesta l-esito (sotto);
- non ha trovato errori evidenti (citazioni rotte, troncamenti, sconfinamenti netti): di conseguenza non ha toccato il documento (nessuna correzione, nessun rewrite);
- ha completato il deliverable producendo questo REPORT, committando documento+report e scrivendo READY_FOR_REVIEW.

Quanto segue e dunque l-attestazione della mia verifica, non un resoconto di una derivazione che avrei fatto io. Dove la verifica non e al 100% (es. citazioni campionate e non esaustive), lo dichiaro esplicitamente: il floor 100% sulle citazioni e compito del Reviewer (AC-G7).

---

## 1. Cosa e stato prodotto

Il documento SPEC_FUNZ_01_B4.md consolida emissione & consegna del segnale FIB dai soli Cap.8 (8.1-8.4) e Cap.9 (9.1-9.6) di CAP_02_parte_II.md. Struttura e copertura verificate:

- par.0: Intestazione e scopo + 0.1 fonte/pin (a1625df) + 0.2 schema ID auto-assegnato + 0.3 carve-out numeri.
- par.1 Filosofia del contratto di emissione (Cap.8.1): B4-R-01 (decisione prima dell-emissione), B4-CN-01 (assenza guardie post-emissione come invariante), B4-R-02..R-05 (motivazione triplice scomposta: coerenza punto 1 / addestrabilita su storico / eliminazione spread / valutazione real-time dell-operatore).
- par.2 Le tre condizioni (Cap.8.2): B4-R-06 (volatilita), B4-R-07 (liquidita), B4-R-08 (distanza sigma-units), ciascuna con senso operativo e rinvii a Parte III/V.
- par.3 Filtro 80 pt come regola (Cap.8.2-8.3): B4-R-09 (regola), B4-CN-02 (vincolo assoluto non allentabile), B4-CN-03 (distinzione architetturale leva-vs-floor, analogia b_min).
- par.4 Regola di emissione e non-emissione (Cap.8.3): B4-R-10 (AND logico), B4-CN-04 (tutto-o-niente), B4-R-11..R-14 (conseguenze della non-emissione scomposte: no signal_id / no pubblicazione / no log / continua a valutare).
- par.5 Assenza filtri post-emissione e fasi speciali (Cap.8.4): B4-CN-05 (raw touch sempre eseguibile), B4-R-15 (patologie al raw touch in carico all-operatore), B4-R-16 (uniformita su 8:00-22:00, no fasi speciali per orario).
- par.6 Contesto canale (Cap.9.1): B4-NFR-01 (formato per lettura mobile), B4-NFR-02 (canale a latenza compatibile).
- par.7 Contratto informativo del messaggio (Cap.9.2): B4-CN-06 (ordine obbligatorio), B4-R-17..R-25 (9 campi pubblicati, uno per posizione), B4-CN-07 (qualificatori senza impatto sull-ingresso), B4-R-26 (esclusione Delta-t_cromosoma/T_touch_max), B4-CN-08 (no istruzioni di gestione attiva, punto 8).
- par.8 Latenza (Cap.9.3): B4-NFR-03 (vincolo L<=L_max), B4-NFR-04 (valore di lavoro 30 s provvisorio, verifica empirica OPEN/PENDING-empirico).
- par.9 Anti-duplicato e messaggio separato (Cap.9.4-9.5): B4-CN-09 (una sola volta, P), B4-CN-10 (P persistito a fini anti-ripubblicazione), B4-R-27 (sostituzione = messaggio separato), B4-CN-11 (no-edit, coerente immutabilita Cap.6.2 come premessa), B4-R-28 (notifica trigger separata), B4-CN-12 (notifica distinta dall-emissione).
- par.10 Gestione errori (Cap.9.6): B4-R-29 (retry), B4-R-30 (n_retry=3 provvisorio), B4-R-31 (backoff 2 s provvisorio), B4-R-32 (fallimento finale: errore nel log, no ulteriore pubblicazione), B4-CN-13 (signal_id non aggiunto a P), B4-CN-14 (fallimento tracciato).
- par.11 Nota di rinvio (materia adiacente NON consolidata) + par.12 Matrice di tracciabilita (50 righe ID|proposizione|citazione|valore) + nota di chiusura.

Conteggio verificato: 50 ID unici (grep -oE B4-(R|CN|NFR)-[0-9]+ | sort -u -> 32 R + 14 CN + 4 NFR); le 50 definizioni di requisito corrispondono biunivocamente alle 50 righe della matrice.

## 2. Ipotesi di partenza

- La passata di derivazione precedente ha lavorato in cieco dai soli Cap.8 e Cap.9 di CAP_02_parte_II.md (modalita B, par.0.1 della card). Questa passata di verifica ha rispettato lo stesso vincolo di cecita: non ho aperto/letto/citato SPEC_FUNZ_01.md (v2), file _v1_storico, file di chunking, ne SPEC_FUNZ_01_B1/B2/B3.md o altri B*.md. Le mie uniche fonti di lavoro: la card B4 + il CAP-fonte Cap.8/9 + il documento B4 da verificare.
- CAP_02_parte_II.md e chiuso PASS, pin a1625df (card par.1; tasks/STATO_CORRENTE.md:13), congelato (freeze G-09): sola lettura, autoritativo, non ri-verificato come metodologia (solo come fonte delle citazioni puntuali).
- L-eredita autoritativa della card par.2 e i fatti chiusi sono presi come dati: non ri-derivati.
- Il confronto-copertura con la v2 congelata e fuori dal mio compito (e compito esclusivo del Reviewer, card par.8): non l-ho tentato.

## 3. Decisioni rilevanti

Trattandosi di una passata di verifica+completamento, le decisioni sono di natura attestativa. Le decisioni di contenuto sono della passata cieca precedente; le ho valutate e ne riporto l-esito:

1. Atomicita (N1): il documento spezza correttamente i concern impacchettati: la motivazione triplice di Cap.8.1 e scomposta in B4-R-02..R-05 (4 proposizioni); le conseguenze della non-emissione in B4-R-11..R-14 (4); i 9 campi del messaggio in 9 requisiti distinti; la politica di retry in B4-R-29/R-30/R-31/R-32 + B4-CN-13/CN-14. Non ho trovato requisiti che impacchettino piu concern verificabili separatamente.
2. Separazione regola-B4 vs valore-Parte-V: il documento enuncia la regola ">= 80 pt vincolo assoluto" (B4-R-09/CN-02) citando il valore 80 come dato gia congelato in CAP-01, e marca i valori di lavoro provvisori (L_max=30 s, n_retry=3, Delta-t_retry=2 s) come provvisori dal CAP (B4-NFR-04, B4-R-30, B4-R-31, par.0.3). Corretto rispetto al carve-out numeri (F-5).
3. Doppio luogo del trigger_event (nota di confine 1 della card): il documento tratta il trigger_event come evento del lifecycle solo come premessa citabile da Cap.7.3 (B4-CN-01, B4-R-28, B4-CN-12) e consolida la pubblicazione/notifica Telegram (B4-R-28/CN-12) tracciata a Cap.9.5 :271. Non ri-deriva l-evento. Corretto.
4. Finestra 8:00-22:00 come carve-out: compare solo in B4-R-16 come "nessuna fase speciale di emissione per orario" (Cap.8.4 :227), con carve-out esplicito che il requisito di sessione operativa (M-GOV-1) e altro blocco. Corretto rispetto alla nota di confine 4.
5. Latenza M-2 come PENDING-empirico: vedi sezione "Applicazione RM-1 a me stesso" e tabella AC-G4. Trattata come aperta, mai dichiarata verificata.
6. Cautela RM-1 invece di asserire: il documento non introduce alcuna nuova dichiarazione "verificato X" di prima istanza: ogni requisito e un richiamo a una riga del CAP-fonte. La Telegram Bot API e etichettata [WIKI-HINT, da verificare] (riga 316) e non fonda alcun requisito.

Correzioni minime fatte da questa passata: NESSUNA. La verifica non ha trovato errori evidenti (citazioni rotte, troncamenti, sconfinamenti). Coerentemente con il mandato ("se il documento e integro, non toccarlo; NON fare un rewrite"), il documento e stato lasciato invariato.

## 4. Misura prima/dopo

Greenfield di consolidamento a blocchi (non c-e un "prima" in senso di refactor di edge GA).
- PRIMA: il contenuto di emissione/consegna era disperso nei Cap.8 e Cap.9 di CAP_02_parte_II.md, in forma di prosa metodologica non leggibile come elenco di requisiti tracciabili da un esterno.
- DOPO: 50 requisiti atomici (32 R + 14 CN + 4 NFR), ciascuno tracciato a [DOC-INTERNO CAP_02_parte_II.md:<riga>] nel perimetro Cap.8/9, con valore (operativo/di sistema) dichiarato, piu matrice di tracciabilita e nota di rinvio.
- Copertura del perimetro: Cap.8.1 -> par.1; Cap.8.2 -> par.2-par.3; Cap.8.3 -> par.4; Cap.8.4 -> par.5; Cap.9.1 -> par.6; Cap.9.2 -> par.7; Cap.9.3 -> par.8; Cap.9.4-9.5 -> par.9; Cap.9.6 -> par.10. Tutte e 10 le sotto-sezioni del perimetro risultano coperte.

## 5. Domande aperte

Nessun blocco aperto in questa passata. Nessun requisito e marcato [B-N PROVVISORIO] (verificato: il documento non contiene marcatori di contaminazione, coerente con l-assenza di blocchi).

Una sola non-verifica dichiarata (non un blocco, ma per onesta): non ho ri-controllato il 100% delle citazioni del documento (50 requisiti, alcuni con doppia citazione). Ho verificato un campione che include tutti i punti critici richiesti (filtro 80pt :209, regola AND :215/:217, latenza :257-261, anti-duplicato :265, notifica trigger :271, errori :275-281) piu i 9 campi del messaggio (:243-251) e la riga aggregata :253. Tutti i campioni risolvono token-per-token. Il floor 100% resta compito del Reviewer (AC-G7).

## 6. Criterio di rollback

B4 e un file autonomo (docs/spec_funzionale/SPEC_FUNZ_01_B4.md) + il suo report. L-annullamento di B4 consiste nel git revert del commit [SPEC-FUNZ-01-B4] (o rimozione dei due file): non impatta B1/B2/B3 (file separati, gia chiusi PASS), non tocca i CAP (freeze G-09 rispettato: nessun CAP modificato), non tocca 00_indice.md (N/A per SPEC-FUNZ), non tocca i file di stato single-writer. Il task card resta come storico.

---

## Tabella verifica AC-G1..AC-G11

| AC | Esito | Evidenza (file:riga) |
|---|---|---|
| AC-G1 Atomicita (N1) | OK | Motivazione triplice scomposta SPEC_FUNZ_01_B4.md:46-60 (B4-R-02..R-05); conseguenze non-emissione :116-130 (B4-R-11..R-14); 9 campi distinti :175-211 (B4-R-17..R-25); retry scomposto :274-296 (B4-R-29..R-32, B4-CN-13/14). |
| AC-G2 Tracciabilita obbligatoria | OK | Ogni requisito porta [DOC-INTERNO CAP_02_parte_II.md:<riga>] nel perimetro Cap.8 (:179-227) o Cap.9 (:231-281). Matrice completa :322-373. Verificato a campione (vedi par.5 + RM-1 a me stesso). |
| AC-G3 Valore operativo obbligatorio | OK | Ogni requisito ha campo Valore operativo o, per invarianti di processo (F-2), Valore di sistema dichiarato: es. operativo :40,:70,:93; di sistema :102 (B4-CN-03), :118 (B4-R-11), :236 (B4-NFR-04), :280 (B4-R-30). |
| AC-G4 Divieto verificato-X / latenza PENDING-empirico | OK | Nessuna nuova dichiarazione verificato-X. Latenza M-2: SPEC_FUNZ_01_B4.md:234-236 (B4-NFR-04) valore di lavoro provvisorio, verifica empirica della latenza effettiva e materia di Appendice E, PENDING-empirico (non verificata in questo blocco). Mai "latenza verificata a 30 s". |
| AC-G5 Etichette RM-3 su fonti esterne | OK | Telegram Bot API etichettata [WIKI-HINT, da verificare] e non fonte unica :316. Nessun requisito regge solo su fonte esterna. |
| AC-G6 Grafia canonica citazioni | OK | Usata [DOC-INTERNO ...] e [WIKI-HINT, da verificare]; grafia storica [CODICE-EXISTENTE ...] assente (verificato con grep: nessuna occorrenza). |
| AC-G7 Floor citazioni 100% | PARZIALE (campione 100% OK; floor 100% = Reviewer) | Campione verificato token-per-token contro CAP-fonte: :183,:185,:187 (8.1); :191,:193,:197,:199,:203,:205 (8.2); :209,:211 (filtro 80pt); :215,:217,:219,:221 (8.3); :225,:227 (8.4); :235,:237 (9.1); :241,:243-:253 (9.2); :257,:259,:261 (9.3); :265 (9.4); :269,:271 (9.5); :275,:277,:278,:279,:281 (9.6). Tutti risolvono. Verifica esaustiva al 100% = compito del Reviewer per ruolo. |
| AC-G8 Cecita preservata | OK | grep R-3. / R-4. / CN-4. / B1- / B2- / B3- / _v1_storico / SPEC_FUNZ_01.md su SPEC_FUNZ_01_B4.md -> No matches. ID auto-assegnati B4-R/CN/NFR (:20-26). Nessuna firma della v2. |
| AC-G9 Scope tutto-e-solo | OK | Copertura completa Cap.8.1-8.4 + Cap.9.1-9.6 (par.1-par.10). Nessuno sconfinamento: campi come dato rinviati (:308), trigger_event come evento rinviato (:309), formato log rinviato (:310), sessione operativa rinviata (:311), formule/valori rinviati (:312-313), Appendice E (:314). Nota di rinvio par.11 :302-316. |
| AC-G10 Matrice + nota di rinvio | OK | Matrice :320-375 (colonne ID|proposizione|citazione|valore). Nota di rinvio (cosa deliberatamente rinviato e perche) :302-316. |
| AC-G11 Invarianti evidenziati come tali | OK | Filtro 80pt non allentabile :96 (B4-CN-02); tutto-o-niente :112 (B4-CN-04); anti-duplicato :242,:246 (B4-CN-09/10); no-edit/messaggio separato :255 (B4-CN-11); ordine obbligatorio :171 (B4-CN-06); assenza filtri post-emissione :42,:138 (B4-CN-01/05). Resi come B4-CN-* (famiglia invarianti). |

Legenda: AC-G7 e PARZIALE solo nel senso che la mia verifica delle citazioni e a campione (esauriente sui punti critici), non al 100%: la verifica esaustiva e per ruolo compito del Reviewer. Non e un gap del documento.

---

## Applicazione RM-1 a me stesso

Elenco delle affermazioni che faccio in questo report con sostegno operativo, e cio che resta non verificato da me:

- "Il documento e completo strutturalmente (50 requisiti)" - PROVE: grep -oE B4-(R|CN|NFR)-[0-9]+ | sort -u | uniq -c -> 32 B4-R, 14 B4-CN, 4 B4-NFR = 50; le 50 definizioni corrispondono alle 50 righe della matrice :322-373; nota di chiusura :375 dichiara lo stesso conteggio. ALTERNATIVE ESCLUSE: ID duplicati o buchi di numerazione (esclusi: sort -u da esattamente 50). ALTERNATIVE NON ESCLUSE: nessuna rilevante.
- "La cecita e preservata" - PROVE: grep su pattern di contaminazione (R-3./R-4./CN-4./B1-/B2-/B3-/_v1_storico/SPEC_FUNZ_01.md) -> No matches; ID auto-assegnati. ALTERNATIVE NON ESCLUSE: frasi identiche alla v2 che non corrispondano a uno dei pattern grep (es. una frase di prosa copiata) NON sono escluse dal mio grep - questa e precisamente la ricerca che il Reviewer fa nel confronto-copertura (card par.8). Io attesto l-assenza di tracce greppabili e di ID importati, non l-assenza assoluta di ogni eco lessicale: quest-ultima e verifica del Reviewer.
- "Le citazioni campionate risolvono token-per-token" - PROVE: lettura diretta di CAP_02_parte_II.md:179-283 e confronto puntuale con le citazioni dei requisiti critici (elencati in AC-G7). ALTERNATIVE NON ESCLUSE: le citazioni non campionate (sottoinsieme minore) non sono state ricontrollate da me al 100%; dichiarato apertamente. Floor 100% = Reviewer (AC-G7).
- "Nessuno sconfinamento di scope" - PROVE: lettura dell-intero documento; le materie adiacenti (payload come dato, lifecycle, log, sessione operativa, formule, valori congelati, dettaglio bot) sono esplicitamente rinviate nella nota par.11 e non consolidate nei requisiti. ALTERNATIVE NON ESCLUSE: una valutazione fine di confine (es. se un singolo requisito tocchi marginalmente B2/B3) resta giudizio che il Reviewer puo raffinare; non ho rilevato sconfinamenti netti.
- Latenza M-2 (PENDING-empirico) - VERIFICA: il documento tratta la latenza Telegram come non verificata. PROVE: B4-NFR-04 (:234-236) cita L_max=30 s come valore di lavoro provvisorio dal CAP (:261) e marca la verifica empirica del canale come OPEN / materia di Appendice E, con valore di sistema "tenendo esplicito che il numero non e definitivo e la sua verifica resta aperta". ALTERNATIVE ESCLUSE: una dichiarazione "latenza verificata a 30 s" - assente (verificato per lettura e coerente con AC-G4). ALTERNATIVE NON ESCLUSE: nessuna. Conferma: il trattamento PENDING-empirico della latenza M-2 e corretto e non dichiarato verificato.

---

*Report prodotto dallo spec_developer (passata di verifica+completamento). Il documento B4 e stato derivato in cieco da una passata Developer precedente interrotta da un errore di rete; questa passata ne ha verificato cecita/completezza/citazioni campionate/scope e ha completato il deliverable (report + commit). Nessuna correzione al documento (integro). Sede CLI, no-DAPI.*

---

# Estensione consegna — SPEC-FUNZ-01-B4-EXT

> Tag commit: [SPEC-FUNZ-01-B4-EXT]. Sede: CLI, no-DAPI. Fonte unica: docs/methodology_v2/CAP_06_parte_VI.md, Cap.29 (par.29.1-29.5).
> Estensione del blocco B4 che recupera la materia di CONSEGNA di CAP_06 PVI omessa dal perimetro-fonte originario. La parte CAP_02 Cap.8-9 (50 requisiti, PASS c3be05e) NON e toccata.

## Conferma letture obbligatorie (estensione)

Confermo di aver letto, in questo ordine, prima di scrivere l'estensione: (1) tasks/METODO.md (RM-1..RM-4 + RACC-METODO-2 + Enforcement); (2) .claude/BASE_COMUNE.md (ciclo, sede CLI, onesta claim->evidenza par.8); (3) .claude/agents/spec_developer.md (il mio ruolo); (4) tasks/ACTIVE_TASK.md (card B4-EXT: decisione di perimetro par.0, cecita par.0.1, perimetro-fonte par.1 SOLO Cap.29, AC par.2 con AC-EXT-1/2/3, sezioni par.3, out-of-scope par.4, done-when par.5); (5) FONTE: docs/methodology_v2/CAP_06_parte_VI.md Cap.29 (par.29.1-29.5, righe :142-244) per la verifica token-per-token delle citazioni; (6) ECCEZIONE same-block: docs/spec_funzionale/SPEC_FUNZ_01_B4.md (B4 esistente) SOLO per continuita-ID e no-duplicazione (par.0.1 della card).

## Provenienza e cecita (estensione) — onesta tassativa (RM-1, BASE_COMUNE par.8)

- Provenienza: estensione autorizzata dal supervisore AC (Opzione 1). Recupera la materia di CONSEGNA di CAP_06 PVI (Cap.29) omessa dal perimetro-fonte originario di B4 (errore di setup dell'Orchestratore, non del Planner ne dei Developer; card par.0/par.0 nota RM-2). NON e un nuovo blocco ne un rifacimento.
- Cecita: i requisiti dell'estensione sono derivati DAL SOLO Cap.29 di CAP_06_parte_VI.md. NON ho aperto/letto/citato SPEC_FUNZ_01.md (v2), file _v1_storico, file di chunking (PROPOSTA_SUDDIVISIONE_SPEC*.md) come fonte di requisiti, ne i documenti B1/B2/B3. Eccezione necessaria same-block: ho letto SPEC_FUNZ_01_B4.md (stesso blocco) SOLO per (i) continuare lo schema-ID senza collisione (prossimi liberi B4-NFR-05, B4-R-33) e (ii) non duplicare il contratto a 9 voci di Cap.9.2 e la pubblicazione della notifica trigger_event di Cap.9.5, gia consolidate in B4. Il confronto-copertura con la v2 resta compito esclusivo del Reviewer (card par.6).
- Invarianza parte PASS: NON ho toccato, riaperto ne rinumerato i 50 requisiti della parte CAP_02 (par.1-par.12 del documento). Ho solo: (a) appeso la sezione "# Estensione consegna — CAP_06 PVI (Cap.29)" dopo la matrice esistente; (b) aggiunto una nota in par.0.2 (continuita-ID) e una postilla al totale parziale di par.12.

## 1. Cosa e stato prodotto (estensione)

Appesa a SPEC_FUNZ_01_B4.md la sezione "# Estensione consegna — CAP_06 PVI (Cap.29)" con:
- E.0 Nota di provenienza ed estensione (Opzione 1 AC; cosa recupera: NFR-6.1 + R-6.4; invarianza parte PASS c3be05e; fonte e cecita Cap.29).
- E.1 Requisiti mobile-first (Cap.29.1-29.2): B4-NFR-05 (consegna leggibile/azionabile da cellulare in attenzione limitata), B4-NFR-06 (il layout rappresenta lo stesso payload senza nuovi/omessi campi — cosmetico, non del contratto; Cap.9.2 citato come premessa, 9 voci NON ri-elencate), B4-NFR-07 (contenuto critico senza scroll orizzontale ed entro la prima schermata).
- E.2 Le 3 notifiche standard (Cap.29.4): B4-R-33 (esattamente 3 notifiche standard per segnale), B4-R-34 (nessun aggiornamento di stato tra le notifiche, no polling/refresh).
- E.3 Notifica 1 emissione (Cap.29.2): B4-R-35 (1a notifica = emissione; pubblicazione gia B4, citata come premessa non duplicata).
- E.4 Notifica 2 trigger_event (Cap.29.3): B4-R-36 (2a notifica = trigger_event al raw touch, messaggio separato; pubblicazione gia B4 §9 B4-R-28/CN-12 citata come gia-consolidata; evento del lifecycle = B3, premessa), B4-R-37 (la notifica non modifica l'emissione, no edit/append, con signal_id).
- E.5 Notifica 3 transizione terminale (Cap.29.5): B4-R-38 (3a notifica = chiusura alla transizione a stato terminale; stati terminali = B3, premessa non ri-derivata), B4-R-39 (veicola lo stato terminale finale, 1 di 6), B4-R-40 (veicola R_gross, vuoto/n.a. se non eseguito).
- E.6 Matrice di tracciabilita estensione (11 righe) + conteggio: estensione 8 R + 3 NFR = 11; totale B4 = 40 R + 14 CN + 7 NFR = 61.
- E.7 Nota di rinvio: Cap.27 (pipeline/inference/EGARCH) e Cap.28 intero (anti-doppio operazionale, non-refresh, tie-break, logging candidati, determinismo del replay) rinviati a B5 (runtime != consegna), con nota di confine sull'anti-duplicato di Cap.29.4 gia coperto da Cap.9.4 in B4.

Conteggio verificato: 11 nuovi ID (B4-NFR-05/06/07; B4-R-33..R-40), continui dallo schema B4 senza collisione, biunivoci con le 11 righe della matrice E.6.

## 2. Ipotesi di partenza (estensione)

- Derivazione in cieco dal solo Cap.29 di CAP_06_parte_VI.md (modalita B, card par.0.1). CAP_06 e chiuso PASS (citato dalla card come fonte autoritativa) e congelato (freeze G-09): sola lettura, non ri-verificato come metodologia, usato solo come fonte delle citazioni puntuali.
- I pin depositati dall'Orchestratore nella card (par.1: :146/:154 mobile-first, :220 3 notifiche, :190 trigger, :223/:225 terminale) sono autoritativi (input dell'Orchestratore), ma li ho ri-verificati token-per-token come richiesto da AC-G7 (esito in tabella AC).
- Correzione di fonte della card (Cap.28.4 -> Cap.29.4 per R-6.4) presa come dato autoritativo confermato da AC: le 3 notifiche stanno in Cap.29.4 :220, NON in Cap.28.4. Da Cap.28 non ho preso nulla.
- Confronto-copertura con la v2 (NFR-6.1/R-6.4 effettivamente coperti, nessun residuo di consegna v2 caduto): fuori dal mio compito, compito esclusivo del Reviewer (card par.6).

## 3. Decisioni rilevanti (estensione)

1. Granularita N1 sul mobile-first: ho spezzato il concern "mobile-first" in 3 NFR distinti perche Cap.29 impacchetta 3 proposizioni verificabili separatamente: il principio di progettazione (B4-NFR-05, :146), la natura cosmetica-non-del-contratto della rappresentazione (B4-NFR-06, :146/:154), e i vincoli tecnici di leggibilita senza scroll (B4-NFR-07, :152). Ciascuna e verificabile da sola.
2. Granularita N1 sulle 3 notifiche: ho separato l'ESISTENZA dell'insieme (B4-R-33, esattamente 3) dalla regola di NON-AGGIORNAMENTO tra le notifiche (B4-R-34, no polling/refresh) perche sono due proposizioni distinte entrambe in :220. Poi una notifica per momento (B4-R-35/36/38). Per la terminale ho aggiunto due requisiti sul CONTENUTO veicolato alla consegna (B4-R-39 stato finale :230; B4-R-40 R_gross :232) perche sono concern di consegna distinti dall'esistenza della notifica.
3. No-duplicazione (AC-EXT-3): NON ho ri-elencato le 9 voci di Cap.9.2 (citate come premessa in B4-NFR-06 ed E.1); NON ho duplicato la pubblicazione della notifica trigger_event di Cap.9.5 (citata come gia-B4 in B4-R-36, rinviando a B4-R-28/CN-12); NON ho ri-derivato la state machine ne l'insieme degli stati terminali (citati come premessa B3 in B4-R-38/R-39). L'evento trigger_event come evento del lifecycle e B3, citato come premessa.
4. Confine consegna/runtime (AC-EXT-2): da Cap.28 NON ho preso nulla. Nessun requisito tocca pipeline/inference (Cap.27) ne anti-doppio operazionale/non-refresh/tie-break/logging/determinismo (Cap.28). La nota E.7 rinvia esplicitamente Cap.27 e Cap.28 intero a B5. La gestione idempotenza di lettura di Cap.29.4 (anti-ripubblicazione ai restart) e stata RICONOSCIUTA gia coperta da Cap.9.4 in B4 (B4-CN-09/10) e NON ri-consolidata: di Cap.29.4 ho preso solo le 3 notifiche standard.
5. Cautela RM-1: nessuna nuova dichiarazione "verificato X" di prima istanza; ogni requisito e un richiamo a una riga di Cap.29. Nessuna fonte esterna fonda requisiti (Telegram Bot API resta livello-4, gia [WIKI-HINT] nel B4 base; l'estensione non ne introduce di nuove).

## 4. Misura prima/dopo (estensione — greenfield di consolidamento)

- PRIMA: la materia di consegna di CAP_06 Cap.29 (mobile-first + 3 notifiche standard) era prosa metodologica nel CAP, non leggibile come requisiti tracciabili da un esterno; inoltre era stata OMESSA dal perimetro-fonte di B4 (i due requisiti-bersaglio NFR-6.1 e R-6.4 non risultavano recuperati). Tracciabilita della consegna CAP_06: 0 requisiti.
- DOPO: 11 requisiti atomici (8 R + 3 NFR) tracciati a [DOC-INTERNO CAP_06_parte_VI.md:<riga>] nel perimetro Cap.29, con valore operativo dichiarato, matrice E.6 e nota di rinvio E.7. NFR-6.1 recuperato (B4-NFR-05/06/07); R-6.4 recuperato (B4-R-33/34 + le tre notifiche B4-R-35/36/38).
- Totale B4 aggiornato: 50 -> 61 requisiti (40 R + 14 CN + 7 NFR). La parte CAP_02 (50) e invariata; +11 dalla consegna CAP_06.
- Copertura del perimetro Cap.29: 29.1 -> E.1 (B4-NFR-05/06/07); 29.2 -> E.1+E.3 (layout + notifica emissione); 29.3 -> E.4 (notifica trigger); 29.4 -> E.2 (3 notifiche standard; idempotenza riconosciuta gia-B4); 29.5 -> E.5 (notifica terminale). Tutte e 5 le sotto-sezioni di Cap.29 coperte o riconosciute gia-consolidate.

## 5. Domande aperte / Blocchi (estensione)

Nessun blocco aperto. I pin della card hanno risolto puliti alla ri-verifica token-per-token (vedi AC-G7/AC-EXT in tabella). Nessun requisito e marcato [B-N PROVVISORIO] (verificato: l'estensione non contiene marcatori di contaminazione, coerente con l'assenza di blocchi).

Nota di onesta: la verifica di copertura PIENA consegna-vs-v2 (che NFR-6.1 e R-6.4 siano effettivamente i soli requisiti di consegna v2 mancanti, e che nessun altro residuo di consegna v2 sia caduto) e per ruolo compito del Reviewer (card par.6), non mia: io attesto il recupero esplicito dei due bersagli nominati dalla card, non l'esaustivita rispetto alla v2 (che sono cieco di leggere).

## 6. Criterio di rollback (estensione)

L'estensione vive interamente nella sezione "# Estensione consegna — CAP_06 PVI (Cap.29)" appesa a SPEC_FUNZ_01_B4.md (piu una nota in par.0.2 e una postilla al totale di par.12) + questa sezione di report. L'annullamento consiste nel git revert del commit [SPEC-FUNZ-01-B4-EXT]: ripristina il documento ai 50 requisiti della parte CAP_02 (PASS c3be05e), non tocca i CAP (freeze G-09: nessun CAP modificato), non tocca 00_indice.md (N/A), non tocca i file di stato single-writer, non impatta B1/B2/B3 (file separati). La parte CAP_02 Cap.8-9 resta valida indipendentemente.

---

## Tabella verifica AC (estensione: AC-G + AC-EXT-1/2/3)

| AC | Esito | Evidenza (file:riga) |
|---|---|---|
| AC-G1 Atomicita (N1) | OK | Mobile-first scomposto in 3 NFR (SPEC_FUNZ_01_B4.md, sez. E.1: B4-NFR-05/06/07); 3 notifiche scomposte in esistenza-insieme (B4-R-33) + no-refresh (B4-R-34) + una per momento (B4-R-35/36/38) + contenuto terminale (B4-R-39/40, sez. E.2-E.5). Ogni requisito = 1 proposizione verificabile. |
| AC-G2 Tracciabilita obbligatoria | OK | Ogni requisito dell'estensione porta [DOC-INTERNO CAP_06_parte_VI.md:<riga>] nel perimetro Cap.29 (:146/:152/:154/:190/:220/:223/:225/:230/:232). Matrice E.6 (11 righe). Ri-verificato token-per-token (AC-G7 sotto). |
| AC-G3 Valore operativo obbligatorio | OK | Ogni requisito dell'estensione ha "Valore operativo" dichiarato (sez. E.1-E.5: es. B4-NFR-05, B4-R-33, B4-R-40). Nessun invariante puro in questa estensione (tutti operativi). |
| AC-G4 Divieto verificato-X | OK | Nessuna nuova dichiarazione "verificato X" di prima istanza nell'estensione: ogni requisito e un richiamo a una riga di Cap.29. Nessun claim empirico nuovo. |
| AC-G5 Etichette RM-3 fonti esterne | OK | L'estensione non introduce fonti esterne: ogni requisito regge su Cap.29 (livello DOC-INTERNO). Telegram Bot API resta livello-4 gia [WIKI-HINT] nel B4 base, non usata qui come fonte. |
| AC-G6 Grafia canonica | OK | Usata [DOC-INTERNO ...]; grafia storica [CODICE-EXISTENTE ...] assente nell'estensione. |
| AC-G7 Floor citazioni 100% (mia ri-verifica token-per-token) | OK (mio campione = tutte le 11) | Ri-verificate contro CAP_06_parte_VI.md: :146 (29.1 mobile-first "rappresentato in un layout mobile-first") -> B4-NFR-05/06; :152 (vincoli leggibilita "senza scroll orizzontale") -> B4-NFR-07; :154 (29.2 "Layout mobile-first del messaggio di emissione") -> B4-NFR-06/B4-R-35; :190 (29.3 "Notifica trigger_event come messaggio separato") -> B4-R-36/37; :220 ("esattamente 3 notifiche standard per segnale" + "no polling, no refresh") -> B4-R-33/34/35/36/38; :223 (29.5 "Notifica di transizione terminale") -> B4-R-38; :225 (transizione active->stati terminali) -> B4-R-38; :230 ("stato terminale finale, uno dei 6") -> B4-R-39; :232 ("R_gross ... vuoto o n/a per i segnali non eseguiti") -> B4-R-40. Tutte risolvono token-per-token. Floor esaustivo finale = Reviewer per ruolo. |
| AC-G8 Cecita preservata | OK | Estensione derivata dal solo Cap.29. Nessun ID importato (continui B4-NFR-05+/B4-R-33+). Premesse Cap.9.2/9.5/Cap.7 citate ESPLICITAMENTE come premessa, non ri-derivate. Letto B4 esistente solo per ID/no-dup (eccezione same-block). Tracce v2/B1/B2/B3 = nessuna importata. |
| AC-G9 Scope tutto-e-solo (Cap.29) | OK | Tutti gli 11 requisiti tracciano a Cap.29. Cap.27/Cap.28 esclusi e rinviati a B5 (sez. E.7). Vedi AC-EXT-2. |
| AC-G10 Matrice + nota di rinvio | OK | Matrice E.6 (ID|proposizione|citazione|valore, 11 righe + conteggi). Nota di rinvio E.7 (Cap.27 + Cap.28 intero -> B5, con motivazione runtime!=consegna). |
| AC-G11 Invarianti come tali | OK (N/A sostanziale) | L'estensione non introduce nuovi invarianti di contratto (famiglia CN): tutti i requisiti sono R o NFR di consegna. B4-R-37 (no-edit della notifica) e reso coerente con l'invariante no-edit gia in B4 (B4-CN-11), citato come premessa, non ri-creato come nuovo CN. |
| AC-EXT-1 Recupero esplicito NFR-6.1 + R-6.4 | OK | NFR-6.1 (mobile-first) -> B4-NFR-05/06/07 (sez. E.1, :146/:152/:154). R-6.4 (3 notifiche standard) -> B4-R-33/34 (sez. E.2, :220) + le tre notifiche B4-R-35/36/38 (E.3/E.4/E.5). Recupero dichiarato in E.0. |
| AC-EXT-2 Confine consegna/runtime | OK | Nessun requisito tocca Cap.27 (pipeline/inference) ne Cap.28 (anti-doppio operazionale/non-refresh/tie-break/logging/determinismo): rinviati a B5 in E.7. Da Cap.28 preso nulla. Idempotenza di lettura di Cap.29.4 riconosciuta gia-B4 (Cap.9.4), non ri-consolidata. |
| AC-EXT-3 Continuita ID e no-duplicazione | OK | ID continui senza collisione (B4-NFR-05/06/07; B4-R-33..R-40; verificato contro lo schema B4 esistente che arriva a NFR-04/R-32/CN-14). 9 voci di Cap.9.2 NON ri-elencate (premessa in B4-NFR-06). Notifica trigger Cap.9.5 NON duplicata (premessa gia-B4 in B4-R-36). State machine B3 NON ri-derivata (premessa in B4-R-38/39). |

## Applicazione RM-1 a me stesso (estensione)

- "L'estensione e completa strutturalmente (11 requisiti)" - PROVE: 11 nuove definizioni di requisito (B4-NFR-05/06/07, B4-R-33..R-40) biunivoche con le 11 righe della matrice E.6; conteggio E.6 dichiara 8 R + 3 NFR = 11 e totale 61. ALTERNATIVE ESCLUSE: collisione con ID B4 esistenti (esclusa: B4 base arriva a NFR-04/R-32, l'estensione parte da NFR-05/R-33). ALTERNATIVE NON ESCLUSE: nessuna rilevante.
- "Le citazioni dell'estensione risolvono token-per-token" - VERIFICA: tutte e 11 ricontrollate contro CAP_06_parte_VI.md:142-244 (lettura diretta). PROVE: elenco puntuale in AC-G7 sopra. ALTERNATIVE ESCLUSE: pin errato Cap.28.4 invece di Cap.29.4 (escluso: ho letto :220 in Cap.29.4 e contiene "esattamente 3 notifiche standard"; :123 NON e stato usato). ALTERNATIVE NON ESCLUSE: il floor esaustivo finale resta verifica del Reviewer per ruolo (ma il mio campione qui coincide con l'intero insieme degli 11).
- "La cecita e preservata (estensione)" - PROVE: derivazione dal solo Cap.29; premesse Cap.9.2/9.5/Cap.7 marcate esplicitamente come premessa; lettura del B4 esistente dichiarata e limitata a ID/no-dup (eccezione same-block della card). ALTERNATIVE NON ESCLUSE: eventuali echi lessicali dalla v2 che io non posso rilevare essendo cieco di leggerla - questa e precisamente la verifica del confronto-copertura che fa il Reviewer (card par.6). Io attesto l'assenza di ID importati e la derivazione da Cap.29, non l'assenza assoluta di ogni eco.
- "Nessuno sconfinamento runtime (Cap.27/Cap.28)" - PROVE: lettura dell'intero Cap.29 come perimetro; da Cap.28 (:123 e dintorni) non ho tratto requisiti; E.7 rinvia Cap.27 e Cap.28 intero a B5. ALTERNATIVE NON ESCLUSE: una valutazione fine di confine su un singolo requisito resta raffinabile dal Reviewer; non ho rilevato sconfinamenti netti.
- "No-duplicazione rispettata" - PROVE: le 9 voci di Cap.9.2 non sono ri-elencate (B4-NFR-06 le cita come premessa); la pubblicazione trigger_event di Cap.9.5 non e duplicata (B4-R-36 rinvia a B4-R-28/CN-12 gia-B4); la state machine non e ri-derivata (B4-R-38/39 citano B3 come premessa). ALTERNATIVE NON ESCLUSE: nessuna rilevante.

---

*Estensione consegna prodotta dallo spec_developer in cieco dal solo Cap.29 di CAP_06_parte_VI.md (lettura del B4 esistente solo per continuita-ID e no-duplicazione, eccezione same-block). Parte CAP_02 Cap.8-9 (PASS c3be05e) invariata. Sede CLI, no-DAPI.*
