# AUDIT OSTILE — Governance del track business-spec (modello a 4 canali)

> **Oggetto**: il *metodo* con cui le business-spec del `ga-zone-engine` verranno scritte e validate (modello a 4 canali + agenti `spec_*` + check statici + harness + tracciabilità). NON il contenuto dei singoli requisiti (non ancora scritti).
> **Stato del processo auditato**: DRAFT, non depositato. Sequenza vincolante DRAFT → AUDIT → REVISIONE → DEPOSITO → loop.
> **Data**: 2026-06-05
> **File auditati**: `HANDOFF_4CANALI.md`, `META_REVIEW_PROMPT.md`, `spec_planner.md`, `spec_developer.md`, `spec_reviewer.md`, `TEMPLATE_SPEC_FUNZ.md`, `TRACCIABILITA.md`, `SPEC_CHECK_STATICI.md`, `SPEC_HARNESS_EMPIRICO.md`.

## Limite di questo audit (da non ignorare)
Eseguito **opus-su-opus, stessa famiglia di modello**. Vale come **pre-filtro**, NON sostituisce l'audit a **modello diverso** che `META_REVIEW_PROMPT.md` richiede per la decorrelazione vera. La correlazione dei punti ciechi tra auditor e progettista non è eliminata qui — è essa stessa il finding F2.

## Legenda natura / severità
- **Natura — progetto**: tocca la tesi stessa del design. Va chiuso prima del deposito.
- **Natura — sequenza/operatività**: legato all'assenza di infrastruttura (Stream D) o al throughput; si attenua o sparisce quando l'infra atterra.
- **Natura — costo-zero**: contraddizione da chiudere con una decisione, costo di fix quasi nullo.
- **Natura — costo/valore**: domanda di fondo, decisione di AC.

---

## F1 — La fedeltà alla metodologia frozen non ha canale
**Natura: progetto · Severità: alta**

Il lavoro centrale del track è tradurre `docs/methodology_v2/` (frozen) in requisiti. Ma i 4 canali coprono: fatto esterno *del mondo* (CH1, fonte in `data/reference/`), coerenza interna (CH2), claim falsificabile sui dati (CH3), intento di AC (CH4). La domanda "**questo requisito traduce fedelmente §X della metodologia?**" non cade in nessuno. La metodologia non è una fonte CH1 — l'esempio CH1 del template cita `borsa_italiana_FIB_contract.md`, un fatto di mondo, e `spec_planner` colloca le fonti CH1 in `data/reference/`. Non è coerenza interna, non è backtestabile, e marcarla CH4 sarebbe laundering (non è intento, è derivazione). La fedeltà finisce relegata all'annotazione "§Metodologia" in `TRACCIABILITA`, e nessuno la valida nel merito: il lint controlla che la riga *esista*, il Reviewer (asse 6) che una § sia citata o N/A. Nessuno verifica che §X dica davvero ciò che il requisito afferma di derivarne.

- **Rischio che emerge**: requisiti che deviano o travisano la metodologia passano tutti e quattro i canali più il lint, perché nessuno chiede "§X lo dice davvero?". L'autorità non-mente più forte e già disponibile — il documento congelato — è usata come post-it, non come gate.
- **Rischio del non intervenire**: il prodotto finale può essere coerente, verificato sui fatti di mondo e backtestato, e comunque infedele alla metodologia da cui doveva nascere. È esattamente il modo in cui la prima business-spec è uscita male, ora ripetuto sotto una veste più rigorosa.
- **Pro e contro**: un quinto canale (o estendere CH1 a "fonte = sezione di metodologia vendorizzata") costa, perché la metodologia è prosa, non valori — il match esatto stile CH1 non si applica pulito. Il contro del non farlo è che il pilastro dichiarato ("ancorare a non-mente") salta proprio sull'asse più importante del lavoro.

---

## F2 — Il giudizio portante (classificazione + anti-laundering) non è ancorato, ed è single-model
**Natura: progetto · Severità: alta**

La tesi del design regge solo se l'assegnazione al canale giusto è affidabile. Ma classificare è giudizio (lo fa il Planner — "assegni il canale"; e lo rifà il Developer — "Classificazione, secca"); la difesa contro la misclassificazione è giudizio del Reviewer (asse 3, "caccia attiva al declassamento", dichiarato "lavoro centrale"); e il lint dichiara esplicitamente di non vederla (`SPEC_CHECK_STATICI`, note di confine: non giudica se un requisito *fosse* da classificare CH1). Quindi la proprietà più load-bearing dell'intero sistema — instradare all'autorità giusta — non è ancorata a nessuna autorità non-mente: è giudizio Claude. E Planner, Developer, Reviewer sono tutti `model: opus`. Stesso modello, stessi punti ciechi. La direzione di laundering più conveniente è **CH3 (costoso: harness, dati, walk-forward) → CH4** (basta fondamento + rollback trigger + ratifica PENDING). Sotto pressione di consegna è la scorciatoia naturale; l'unico argine è che il Reviewer-opus se ne accorga dove il Developer-opus non se n'è accorto.

- **Rischio che emerge**: il sistema sposta la correlazione di un livello invece di risolverla. L'argomento che giustifica il gate umano (Dev e Review condividono blind spot → serve AC) si applica identico *dentro* il loop, dove AC non c'è su ogni requisito ma solo su CH4. Una claim empirica truccata da intento sfugge ai tre opus correlati e finisce a ratifica AC — dove AC ratifica l'intento, non scopre il backtest mancante.
- **Rischio del non intervenire**: il pregio centrale (rigore anti-fallibilità) è carta nel punto che conta. E questo stesso audit, opus-su-opus, ha lo stesso limite: pre-filtro, non la decorrelazione vera.
- **Pro e contro**: ancorare anche la classificazione costa — regole di routing più meccaniche che il lint possa controllare (riducendo lo spazio di giudizio), o un secondo modello sul solo anti-laundering, o estendere il gate AC a campione sulla classificazione, non solo su CH4. Tutte aggiungono attrito. Il contro del non farlo è che "decorrelazione" resta lo slogan con cui il design si autogiustifica e si autosmentisce.

---

## F3 — CH3 non è validabile finché non esiste Stream D; i capitoli raggiungono PASS pur restando empiricamente vuoti
**Natura: sequenza/operatività · Severità: media (si attenua con Stream D)**

`SPEC_CHECK_STATICI` dichiara un fallback manuale per CH1/CH2. `SPEC_HARNESS_EMPIRICO` non ha equivalente, e non potrebbe: non si "backtesta a mano" un walk-forward con purge/embargo su 5 anni di 1-min. `spec_developer` fissa CH3 a Esito=PENDING, "non passa a VALIDATO finché l'harness non conferma"; `spec_planner` fissa CH3 done-when = "harness conferma". Ma l'harness è infrastruttura Stream D non ancora implementata. Ogni requisito CH3 resta dunque BLOCCATO/PENDING senza percorso verso VALIDATO finché Stream C + D non esistono. E il Reviewer audita l'integrità del meccanismo, non la verità: un capitolo con tutti i CH3 a PENDING ben formati può legittimamente ottenere PASS.

- **Rischio che emerge**: il track può "completarsi" (tutti i capitoli PASS) mentre una quota grande dei claim sostanziali resta non validata a tempo indefinito. "Spec done" diventa fuorviante: PASS = ben formato, non = vero.
- **Rischio del non intervenire**: si accumula un magazzino di requisiti CH3 PASS-ma-PENDING; quando l'infra arriva, una parte verrà FALSIFICATA e tornerà al Planner come finding — si riapre in blocco, tardi, lavoro che si credeva chiuso.
- **Pro e contro**: chiudere il buco significa sequenziare lo skeleton harness prima dei capitoli con claim CH3, o restringere i primi `SPEC-FUNZ` a CH1/CH2/CH4, o introdurre uno stato esplicito "PASS-strutturale vs VALIDATO-empirico" così che "done" non menta. Tutte rallentano la sequenza. Il contro del non farlo è un falso senso di completamento che esplode quando l'harness gira.

---

## F4 — In modalità degradata i check "deterministici" CH1/CH2 non sono deterministici
**Natura: sequenza/operatività · Severità: media**

`spec_reviewer` asse 1 e il fallback di `SPEC_CHECK_STATICI`: finché lint e check-fonte non sono implementati, il Reviewer li esegue a mano. Ma CH2 include unicità ID su tutto il corpus, presenza unità su ogni soglia, contraddizioni decidibili tra coppie di soglie; CH1 include match valore-vs-fonte su tutta `data/reference/`. Fatti a mano da Claude, perdono la proprietà che li rende autorità non-mente — ripetibilità ed esaustività — e diventano "Claude legge con attenzione".

- **Rischio che emerge**: finché c'è Stream D, il gate "deterministico" è finzione: giudizio mascherato da meccanica, col rischio aggiuntivo di un falso "gate verde" che dà più fiducia del dovuto. Un ID duplicato o una contraddizione tra il REQ-003 del cap 2 e il REQ-011 del cap 5 sfugge alla lettura umana proprio perché la mole è quella che un linter gestisce e una persona no.
- **Rischio del non intervenire**: i primi capitoli vengono validati con un gate creduto automatico e invece manuale; errori che il lint avrebbe preso a colpo sicuro passano e si scoprono quando il lint vero gira (regressione retroattiva su spec già "chiuse").
- **Pro e contro**: anticipare il solo lint CH2 è codice semplice — non serve l'harness né i dati — ed elimina la finzione a costo basso. Il contro del non farlo è che CH1, CH2 e CH3 collassano tutti su giudizio finché Stream D non c'è: per la fase iniziale il modello a 4 canali è, di fatto, "Claude valuta tutto", lo stato che voleva superare.

---

## F5 — Ambiguità di ownership: Planner e Developer classificano entrambi il canale
**Natura: costo-zero · Severità: bassa per costo di fix, ma reale**

`spec_planner`: "Per ogni requisito previsto dal task, assegni il canale e scrivi l'acceptance"; per CH3 specifica "dataset, metrica, soglia, alternative". `spec_developer`: "Ogni requisito DEVE essere assegnato a esattamente UN canale… Classificazione, secca". Entrambi classificano. Ma il Developer "non ridefinisce il piano". Se il canale è piano (Planner-owned), il "Classificazione secca" del Developer è fuorviante e il suo anti-laundering perde senso (non può truccare ciò che è già assegnato). Se invece il canale segue la natura del requisito — nota solo quando l'enunciato esiste, e l'enunciato lo scrive il Developer — allora il Planner classifica requisiti il cui testo non esiste ancora, e pre-disegna il test CH3 (metrica/soglia/alternative) di un enunciato non scritto. Chicken-and-egg.

- **Rischio che emerge**: collisione di ruolo non risolta. Quando Planner e Developer divergono sul canale, il processo non dice chi vince né cosa succede: il Developer è vincolato a non ridefinire il piano ma anche istruito a classificare per natura. Stallo o override silenzioso.
- **Rischio del non intervenire**: in ogni capitolo resta un punto grigio su chi possiede la decisione più importante. Funziona finché Planner e Developer "indovinano" uguale; rompe al primo disaccordo, e lo risolverà AC a mano — di nuovo gate umano dove non previsto.
- **Pro e contro**: chiarire l'ownership è a costo quasi zero, ma è decisione di Planner. Il contro del non farlo è un confine di ruolo contraddittorio scritto nero su bianco in due dei file che dovrebbero essere la spina dorsale della disciplina.

---

## F6 — Il "gate umano minimo" non è minimo: AC è il collo di bottiglia, e un singolo blocco può congelare il progetto
**Natura: sequenza/operatività + throughput · Severità: media-alta operativa**

Il gate dichiarato è solo CH4. Sommando i file: AC ratifica *ogni* CH4 (template: ogni intento BLOCCATO finché RATIFICATO); AC decide *ogni* fonte CH1 mancante (`spec_planner`: fonte mancante = dipendenza bloccante / QUESTIONS); AC arbitra ogni deadlock a 3 iterazioni. Su blocco, `spec_developer` scrive il requisito BLOCCATO, lo elenca, emette "TASK BLOCCATO" e si ferma; `spec_planner` "sospendi il task fino alla risposta [AC]. Non sbloccare indovinando". E la regola: "un solo task attivo, globalmente — spec o codice, mai due", senza dire che un task sospeso liberi lo slot.

- **Rischio che emerge**: per un trader part-time, AC è il collo di bottiglia di fatto, non solo su CH4 ma su fonti CH1 e arbitrati. Peggio: se il Developer si ferma al *primo* blocco, i bloccanti si scoprono a goccia — capitolo con 5 fonti CH1 mancanti → fino a 5 cicli Dev→Planner→AC sequenziali invece di un batch. E se il task sospeso non libera lo slot globale, un solo CH4 in attesa congela spec *e* codice finché AC non risponde.
- **Rischio del non intervenire**: il throughput è governato dalla disponibilità di AC su decine di micro-decisioni; una singola assenza (ferie, un CH4 pendente) ferma tutto. "Umano solo dove irriducibile" diventa "umano ovunque, in serie".
- **Pro e contro**: mitigare costa scelte di Planner — far enumerare al Developer *tutti* i blocchi del capitolo prima di fermarsi (batch, non goccia); dichiarare che un task sospeso libera lo slot; raggruppare le ratifiche CH4 in sessioni batch. Aggiungono regole. Il contro del non farlo è una serializzazione + AC-bottleneck strutturali, non occasionali.

---

## F7 — Il costo del processo può superare il ritorno per un side-project a singolo trader
**Natura: costo/valore · Severità: decisione AC**

`META_REVIEW` punto 6 invita esplicitamente questo attacco. Il processo è pesante: 3 agenti induriti, tassonomia a 4 canali con blocco di validazione per canale, *due* strumenti d'infrastruttura da costruire (lint + harness), una matrice di tracciabilità, un audit esterno a modello diverso, un loop con cap di iterazione e arbitrato. Per una persona. E si sono già spese più sessioni sul *processo* prima di un solo requisito validato.

- **Rischio che emerge**: process-astronautics — la meta-attività (progettare e mantenere la governance) consuma l'energia che doveva andare nei requisiti e nel motore. Una governance elegante che non consegna mai una spec validata.
- **Rischio del non intervenire**: il rapporto coordinamento/output utile resta sfavorevole; ogni capitolo paga la tassa dei tre ruoli + audit anche quando 5 requisiti banali non la giustificano.
- **Pro e contro**: l'alternativa più semplice al ~90% del valore: tenere la parte che vale davvero — la tassonomia a 4 canali, che costringe a chiedere "come so che è vero?" per ogni requisito — e collassare il resto in fase di scrittura: AC come unico gate su batch di requisiti compilati nel template, harness costruito solo quando esiste un batch di claim CH3 che vale testare, niente audit-di-metodo a modello diverso come passo obbligatorio. Il contro di semplificare: il loop a tre ruoli compra cose reali — caccia al laundering, out-of-scope forzato, anti-scope-creep, un audit ostile che non sei tu a fare su te stesso. Buttarlo per intero riporta il rischio "scrivo prosa e mi convinco da solo" che ha fatto fallire il primo tentativo. La domanda onesta non è "tenere o buttare" ma "quale sottoinsieme del cerimoniale paga per sé in un progetto da una persona".

---

## Verdetto complessivo
**Adottabile con modifiche chirurgiche** — non così com'è, non da ripensare da zero. Il principio (instradare all'autorità non-mente, gate umano dove irriducibile) è giusto e la tassonomia a 4 canali è il pezzo che vale e che risolve il fallimento del primo tentativo.

- **Buchi di progetto (toccano la tesi del design, da chiudere prima del deposito)**: F1, F2.
- **Buchi di sequenza/operatività (condizionano "done" e throughput; si attenuano con Stream D)**: F3, F4, F6.
- **Contraddizione di ruolo a costo-zero**: F5.
- **Domanda costo/valore (decisione AC)**: F7.

I soli che, se ignorati, rifanno fallire la spec nello stesso modo di prima sono **F1 e F2**.
