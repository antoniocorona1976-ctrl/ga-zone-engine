# SPEC_FUNZ_01 — Blocco B4: Emissione & consegna del segnale

> **Track**: Business-spec (SPEC-FUNZ). **Blocco**: 4 di 8 (B1→B8). **Sede**: CLI.
> **Stato**: in costruzione (pre-review). **Tag commit**: `[SPEC-FUNZ-01-B4]`.

---

## 0. Intestazione e scopo del blocco

Questo documento è il **quarto blocco** della specifica funzionale `SPEC_FUNZ_01`, ricostruita ex-novo in 8 blocchi autonomi (B1→B8) che verranno ricomposti in un'unica spec consolidata da un task di assemblaggio dedicato **dopo B8** (assemblaggio fuori scope di B4).

**Tema di B4 — Emissione & consegna**: come e quando il motore **EMETTE** un segnale, e come quel segnale (e la notifica del suo trigger) viene **CONSEGNATO** all'operatore via Telegram. In dettaglio: la filosofia del contratto di emissione, le tre condizioni di mercato valutate prima dell'emissione, il filtro 80 pt come regola, la regola di emissione (AND logico) e le conseguenze della non-emissione, l'assenza di filtri post-emissione e di fasi speciali per orario, il contesto del canale Telegram, il contratto informativo del messaggio, la latenza di consegna, l'anti-duplicato, la regola del messaggio separato + notifica del trigger, e la gestione degli errori di pubblicazione.

### 0.1 — Fonte e pin

- **Fonte unica e autoritativa**: `docs/methodology_v2/CAP_02_parte_II.md` ("Parte II — Contratto del segnale FIB"), **Capitolo 8 (sez. 8.1–8.4)** e **Capitolo 9 (sez. 9.1–9.6)**; preambolo (`:1-9`) come contesto.
- **CAP-02 chiuso PASS, SHA pin `a1625df`** — capitolo congelato (freeze G-09), sola lettura.
- Ogni requisito traccia con grafia canonica `[DOC-INTERNO CAP_02_parte_II.md:<riga>]`.

### 0.2 — Schema ID requisito (auto-assegnato, NON importato)

- **`B4-R-NN`** — requisiti **funzionali / di prodotto** (le tre condizioni, il filtro 80pt come regola, la regola di emissione AND, le conseguenze della non-emissione, i campi pubblicati e l'ordine, la notifica del trigger, la politica di retry come comportamento).
- **`B4-CN-NN`** — requisiti **invarianti/strutturali / di compliance-contratto** (filtro 80pt non allentabile, emissione tutto-o-niente, anti-duplicato, no-edit/messaggio separato, assenza di filtri post-emissione, esclusione delle istruzioni di gestione attiva).
- **`B4-NFR-NN`** — requisiti **non-funzionali / di qualità-di-servizio** (latenza di consegna; formato di lettura mobile).

Gli ID sono assegnati da zero per questo blocco; nessuna numerazione importata da spec preesistenti o da altri blocchi. *(L'estensione consegna §E — CAP_06 Cap.29 — continua questi stessi schemi-ID senza rinumerare i 50 requisiti della parte CAP_02: prossimi liberi `B4-NFR-05`, `B4-R-33`.)*

### 0.3 — Carve-out numeri

- La **finestra di trading 8:00–22:00 CET** è citata come **calendario/semantica già fissata nei CAP chiusi** su cui le condizioni di emissione si applicano uniformemente (citata come dato, non introdotta da B4).
- Il **valore-soglia 80 pt del filtro** è citato come **valore già congelato** (CAP-01) **al solo fine di enunciare la regola** "$\geq 80$ pt, vincolo assoluto non allentabile": la **regola** è B4, il **valore** è materia Parte V.
- I **valori-soglia definitivi** ($L_{max}$, $n_{retry}$, $\Delta t_{retry}$ definitivi; $\tau_{vol}/\tau_{liq}/\tau_{dist}^\sigma$) sono **fuori B4** (Parte V). I **valori di lavoro provvisori** del CAP ($L_{max}=30$ s, $n_{retry}=3$, $\Delta t_{retry}=2$ s) sono citati dal CAP **marcati esplicitamente come provvisori / da congelare in Parte V**.

---

## 1. Filosofia del contratto di emissione (Cap.8.1)

**B4-R-01 — La decisione di emettere è presa prima dell'emissione.**
Il motore decide se emettere un segnale **prima** dell'emissione, sulla base di condizioni di mercato osservate al momento della valutazione `[DOC-INTERNO CAP_02_parte_II.md:183]`.
*Valore operativo*: l'operatore riceve solo segnali per cui il motore ha già verificato, sui dati di mercato, che le condizioni di emissione erano soddisfatte; non riceve segnali "condizionati" da rivalutare dopo.

**B4-CN-01 — Assenza di guardie/filtri post-emissione (invariante di contratto).**
Una volta emesso il segnale, il raw touch dell'entry zone è sempre eseguibile e produce il `trigger_event`; il contratto **non** prevede guardie o filtri post-emissione che blocchino il trigger `[DOC-INTERNO CAP_02_parte_II.md:183]`. (Il `trigger_event` come evento del lifecycle è premessa da Cap.7.3, qui non ri-derivata `[DOC-INTERNO CAP_02_parte_II.md:183]`.)
*Valore operativo*: l'operatore sa che, una volta ricevuto un segnale, nessun meccanismo nascosto del motore può invalidarne l'eseguibilità al raw touch; la decisione di entrare resta sua e basata su ciò che vede sul broker.

**B4-R-02 — Motivazione (a): coerenza con il punto 1 della dichiarazione di intenti.**
L'assenza di filtri post-emissione è coerente con il punto 1 della dichiarazione di intenti (il motore emette segnali, l'esecuzione è dell'operatore): un filtro post-emissione che bloccasse il trigger introdurrebbe una decisione di esecuzione mascherata da decisione di segnale `[DOC-INTERNO CAP_02_parte_II.md:185]`.
*Valore operativo*: garantisce all'operatore che il motore non si appropri della decisione di esecuzione, che resta interamente sua.

**B4-R-03 — Motivazione (b): le condizioni di emissione sono addestrabili sul GA e calcolabili sullo storico.**
Le condizioni di emissione devono essere calcolabili sulla serie storica del FIB disponibile per il training; lo storico Portara/CQG FIB 1-min copre OHLC e volume, omogenei con le grandezze del feed real-time `[DOC-INTERNO CAP_02_parte_II.md:185]` `[DOC-INTERNO CAP_02_parte_II.md:187]`.
*Valore operativo*: il segnale che l'operatore riceve è prodotto da una regola realmente ottimizzata e validata su dati storici, non da una regola che usa dati non disponibili in addestramento.

**B4-R-04 — Motivazione (c): la condizione di spread è eliminata.**
Lo spread bid-ask e la profondità del book non sono disponibili nello storico pianificato (richiederebbero acquisti di dati esplicitamente esclusi in CAP-01); pertanto la condizione di spread è **eliminata** dal contratto di emissione `[DOC-INTERNO CAP_02_parte_II.md:185]`.
*Valore operativo*: nessuna condizione di emissione dipende da dati che il motore non possiede in addestramento, così la regola è coerente fra training e produzione; lo spread istantaneo lo valuta l'operatore in tempo reale.

**B4-R-05 — Motivazione (d): l'operatore valuta le condizioni di esecuzione in tempo reale sul broker.**
Una volta ricevuto il payload, l'operatore valuta in tempo reale sul broker le condizioni di esecuzione visibili a lui (spread istantaneo, profondità del book, candela in corso) e decide se entrare manualmente `[DOC-INTERNO CAP_02_parte_II.md:185]`.
*Valore operativo*: il sistema delega all'operatore la sola valutazione che richiede dati real-time non modellabili, sfruttando il fatto che esegue manualmente.

---

## 2. Le tre condizioni di emissione (Cap.8.2)

### 2.1 Condizione di volatilità

**B4-R-06 — Condizione di volatilità.**
Il range della barra 1-min al momento della valutazione (massimo meno minimo della barra appena chiusa) deve essere $\leq \tau_{vol}\big(\hat\sigma_{\text{pt}}(t_{emission})\big)$, soglia derivata dal modello di volatilità condizionata `[DOC-INTERNO CAP_02_parte_II.md:191]` `[DOC-INTERNO CAP_02_parte_II.md:193]`.
*Valore operativo*: impedisce che l'operatore riceva un segnale costruito in una barra di volatilità anomala, in cui il prezzo strutturale di riferimento è instabile e il payload rischia di essere subito superseduto.
*(Rinvio: la forma esplicita di $\tau_{vol}$, le formule del modello EGARCH e la conversione $\hat\sigma_{\text{pt}}=\hat\sigma\cdot p_t$ sono Parte III, Cap.13 `[DOC-INTERNO CAP_02_parte_II.md:195]`; il valore della soglia è Parte V.)*

### 2.2 Condizione di liquidità

**B4-R-07 — Condizione di liquidità.**
Il volume della barra 1-min al momento della valutazione deve essere $\geq \tau_{liq}$ `[DOC-INTERNO CAP_02_parte_II.md:197]` `[DOC-INTERNO CAP_02_parte_II.md:199]`.
*Valore operativo*: evita che l'operatore riceva un segnale costruito su un prezzo strutturale di riferimento non rappresentativo, risultato di poche operazioni in un mercato anomalmente sottile.
*(Rinvio: la soglia $\tau_{liq}$ è parametro libero del cromosoma, congelata in Parte V `[DOC-INTERNO CAP_02_parte_II.md:201]`.)*

### 2.3 Condizione di distanza strutturale in sigma-units

**B4-R-08 — Condizione di distanza strutturale in sigma-units.**
La distanza fra prezzo strutturale di riferimento e target_1, espressa in sigma-units, deve essere $|\texttt{target\_1}-p_{ref}|/\hat\sigma_{\text{pt}}(t_{emission}) \geq \tau_{dist}^{\sigma}$, con $\tau_{dist}^{\sigma}$ numero puro `[DOC-INTERNO CAP_02_parte_II.md:203]` `[DOC-INTERNO CAP_02_parte_II.md:205]`.
*Valore operativo*: garantisce che la distanza minima fino al primo target sia tarata coerentemente con il regime di volatilità in corso, così che il segnale che l'operatore esegue abbia un'estensione attesa significativa rispetto al rumore del momento, e non solo in punti assoluti.
*(Rinvio: $\tau_{dist}^{\sigma}$ ha dominio strettamente positivo, è parametro libero del cromosoma, congelato in Parte V `[DOC-INTERNO CAP_02_parte_II.md:207]`; la conversione $\hat\sigma_{\text{pt}}$ è Parte III, Cap.13 `[DOC-INTERNO CAP_02_parte_II.md:205]`.)*

---

## 3. Il filtro 80 pt come regola di emissione (Cap.8.2–8.3)

**B4-R-09 — Filtro 80 pt come condizione di emissione (regola).**
L'emissione richiede che il filtro 80 pt del `setup_class` sia soddisfatto: per setup directional $|\texttt{target\_1}-p_{ref}| \geq 80$ pt; per setup trade_range $A_{range} \geq 80$ pt `[DOC-INTERNO CAP_02_parte_II.md:209]`.
*Valore operativo*: assicura che ogni segnale che l'operatore riceve abbia un'estensione minima in punti assoluti tale da rendere l'operazione economicamente sensata (a fronte di commissioni e tick), indipendentemente dal regime.
*(Carve-out: il valore numerico 80 è citato come dato già congelato in CAP-01 al solo fine di enunciare la regola; il suo congelamento è Parte V. La definizione operativa di $A_{range}$ è Parte IV — Cap.6.1/Cap.21.1 `[DOC-INTERNO CAP_02_parte_II.md:209]`.)*

**B4-CN-02 — Il filtro 80 pt è un vincolo assoluto non allentabile dal cromosoma (invariante).**
Il filtro 80 pt resta vincolo assoluto a valle, **non sostituito** dalla condizione in sigma-units; l'emissione richiede il soddisfacimento **simultaneo** di entrambi (sigma-units come leva ottimizzabile del GA, filtro 80pt come vincolo fisso); **in nessun caso** il cromosoma può allentare il floor di 80 pt `[DOC-INTERNO CAP_02_parte_II.md:209]`.
*Valore operativo*: garantisce all'operatore che la soglia minima di estensione del trade non possa mai essere abbassata dall'ottimizzazione, qualunque parametro il GA scelga — una protezione fissa del contratto, non rivedibile.

**B4-CN-03 — Distinzione architetturale leva-ottimizzabile vs floor-fisso (invariante).**
La separazione fra la condizione in sigma-units (parametro libero del cromosoma) e il filtro 80 pt (vincolo fisso del contratto) è architetturalmente equivalente a quella fra il floor fisso della banda $b_{min}=5$ e il parametro $b$ ottimizzato dal cromosoma nel dominio $\{5,\ldots,40\}$ `[DOC-INTERNO CAP_02_parte_II.md:211]`.
*Valore di sistema*: chiarisce in modo non ambiguo, per chi audita il contratto, quali grandezze il GA può muovere e quali sono floor fissi, prevenendo letture errate che tratterebbero il filtro 80 pt come parametro ottimizzabile.

---

## 4. Regola di emissione e conseguenze della non-emissione (Cap.8.3)

**B4-R-10 — Regola di emissione (AND logico).**
L'emissione del segnale avviene **se e solo se** al tempo $t_{emission}$ valgono simultaneamente le tre condizioni e il filtro 80 pt: $E_{vol}\land E_{liq}\land E_{dist}^{\sigma}\land E_{80pt}=\text{vero}$ `[DOC-INTERNO CAP_02_parte_II.md:215]` `[DOC-INTERNO CAP_02_parte_II.md:217]`.
*Valore operativo*: definisce in modo deterministico la sola condizione sotto cui l'operatore riceve un segnale, così che non esistano emissioni "borderline" a discrezione.

**B4-CN-04 — Emissione tutto-o-niente (invariante).**
Se almeno una delle quattro condizioni non è soddisfatta, il segnale candidato **non** viene emesso `[DOC-INTERNO CAP_02_parte_II.md:219]`.
*Valore operativo*: l'operatore non riceve mai un segnale che soddisfa solo parte delle condizioni di qualità; la barra è "tutto o niente".

**B4-R-11 — Non-emissione: nessun `signal_id` generato.**
In caso di non-emissione, nessun `signal_id` viene generato `[DOC-INTERNO CAP_02_parte_II.md:219]`.
*Valore di sistema*: garantisce che non esistano identificatori "fantasma" associati a segnali mai esistiti, premessa di un registro dei segnali pulito e auditabile.

**B4-R-12 — Non-emissione: nessuna pubblicazione Telegram.**
In caso di non-emissione, nessuna pubblicazione Telegram avviene `[DOC-INTERNO CAP_02_parte_II.md:219]`.
*Valore operativo*: l'operatore non riceve notifiche per segnali non emessi, evitando rumore sul canale e falsi inviti all'azione.

**B4-R-13 — Non-emissione: nessun log di emissione scritto.**
In caso di non-emissione, nessun log di emissione viene scritto `[DOC-INTERNO CAP_02_parte_II.md:219]`.
*Valore di sistema*: il log di emissione contiene solo segnali effettivamente emessi, premessa di un audit trail coerente con ciò che l'operatore ha ricevuto.

**B4-R-14 — Non-emissione: il motore continua a valutare alle barre successive.**
Se non emette, il motore continua a valutare le condizioni alle barre 1-min successive `[DOC-INTERNO CAP_02_parte_II.md:219]`.
*Valore operativo*: una barra non favorevole non chiude l'opportunità; l'operatore può ricevere il segnale appena le condizioni si verificano in una barra successiva.

*(Rinvio: le soglie $\tau_{vol}/\tau_{liq}/\tau_{dist}^{\sigma}$ sono parametri liberi del cromosoma congelati in Parte V; le formule del modello di volatilità sono Parte III, Cap.13 `[DOC-INTERNO CAP_02_parte_II.md:221]`.)*

---

## 5. Assenza di filtri post-emissione e di fasi speciali (Cap.8.4)

**B4-CN-05 — Raw touch sempre eseguibile, nessuna guardia ulteriore (invariante).**
Una volta emesso il segnale, il raw touch dell'entry zone è sempre eseguibile; non esistono nel contratto guardie o filtri ulteriori che blocchino il `trigger_event` `[DOC-INTERNO CAP_02_parte_II.md:225]`.
*Valore operativo*: l'operatore ha la certezza contrattuale che il segnale ricevuto sarà eseguibile al raw touch senza condizioni nascoste sopravvenute lato motore.

**B4-R-15 — Le condizioni patologiche al raw touch sono in carico all'operatore.**
Eventuali condizioni patologiche di mercato al momento del raw touch (spread istantaneo allargato, candela in corso violenta) sono valutate in autonomia dall'operatore prima dell'invio dell'ordine; non sono filtrate dal motore `[DOC-INTERNO CAP_02_parte_II.md:225]`.
*Valore operativo*: l'operatore sa esattamente cosa resta a suo carico (la lettura del mercato istantaneo al momento dell'ingresso), senza aspettarsi un filtro automatico che non esiste.

**B4-R-16 — Condizioni di emissione uniformi su tutta la finestra, nessuna fase speciale per orario.**
Le condizioni di emissione si applicano uniformemente lungo l'intera finestra 8:00–22:00 CET; non si introducono fasi speciali (apertura, regolare, after-hours, asta) né soglie differenziate per fascia oraria `[DOC-INTERNO CAP_02_parte_II.md:227]`.
*Valore operativo*: l'operatore riceve segnali con gli stessi criteri di qualità a qualunque ora della finestra; non deve interpretare diversamente un segnale del mattino da uno serale.
*(Carve-out: la finestra 8:00–22:00 CET è citata come calendario già fissato nei CAP chiusi. Il **requisito di sessione operativa** in sé, con la sua verifica empirica, è materia di un altro blocco — vedi §11 nota di rinvio.)*

---

## 6. Contesto del canale Telegram (Cap.9.1)

**B4-NFR-01 — Formato del messaggio progettato per la lettura mobile in attenzione limitata.**
Il canale è un bot Telegram personale dell'operatore (già attivo, CAP-01); l'operatore opera da cellulare in modo discontinuo durante l'orario di lavoro e legge il segnale prima di inviare manualmente l'ordine; il formato del messaggio deve essere progettato per la **lettura mobile in condizioni di attenzione limitata** `[DOC-INTERNO CAP_02_parte_II.md:235]`.
*Valore operativo*: permette all'operatore di cogliere il segnale a colpo d'occhio dal cellulare, in pause brevi e con attenzione parziale, riducendo il rischio di errori di lettura prima dell'invio manuale.

**B4-NFR-02 — Il canale deve garantire una latenza compatibile con l'urgenza operativa.**
Il canale deve garantire una latenza di consegna compatibile con l'urgenza operativa del segnale `[DOC-INTERNO CAP_02_parte_II.md:235]`.
*Valore operativo*: assicura che il segnale arrivi sul cellulare in tempo utile perché l'operatore possa ancora agire sul prezzo strutturale di riferimento. *(Il vincolo quantitativo è B4-NFR-03, §7.)*

*(Rinvio: il dettaglio tecnico del setup bot, della gestione `chat_id` e delle stringhe esatte del messaggio è Appendice E `[DOC-INTERNO CAP_02_parte_II.md:237]`.)*

---

## 7. Contratto informativo del messaggio (Cap.9.2)

Il messaggio Telegram di emissione contiene i seguenti campi del payload, **in ordine obbligatorio**, in forma leggibile da operatore mobile. *(I campi come dato/dominio/immutabilità sono consolidati in altro blocco — vedi §11; qui si fissa il contratto di presentazione: quali campi, in quale ordine, in quale forma, e cosa escludere.)*

**B4-CN-06 — Ordine obbligatorio dei campi del messaggio (invariante).**
I campi pubblicati seguono un **ordine obbligatorio** (1→9 sotto) `[DOC-INTERNO CAP_02_parte_II.md:241]`.
*Valore operativo*: un ordine fisso permette all'operatore di trovare ogni informazione sempre nella stessa posizione, accelerando la lettura mobile e riducendo gli errori.

**B4-R-17 — Campo pubblicato (pos. 1): `signal_id`.**
È pubblicato `signal_id`, l'identificatore del segnale, in chiaro come chiave operativa `[DOC-INTERNO CAP_02_parte_II.md:243]`.
*Valore operativo*: dà all'operatore una chiave univoca per riferirsi al segnale (e correlarlo alla successiva notifica di trigger).

**B4-R-18 — Campo pubblicato (pos. 2): `direction`.**
È pubblicata `direction` (long o short), evidenziata in modo immediato `[DOC-INTERNO CAP_02_parte_II.md:244]`.
*Valore operativo*: comunica all'operatore subito il verso dell'operazione, l'informazione più critica per non sbagliare lato.

**B4-R-19 — Campo pubblicato (pos. 3): `setup_class`.**
È pubblicato `setup_class` (directional o trade_range), per distinguere il senso del filtro 80 pt applicato `[DOC-INTERNO CAP_02_parte_II.md:245]`.
*Valore operativo*: l'operatore capisce di che tipo di setup si tratta e come è stata misurata l'estensione minima del trade.

**B4-R-20 — Campo pubblicato (pos. 4): `entry_zone` come intervallo $[p_{ref}-b, p_{ref}+b]$.**
È pubblicata `entry_zone`, banda di prezzo discreta, esplicitata come intervallo $[p_{ref}-b,\,p_{ref}+b]$ in punti FIB `[DOC-INTERNO CAP_02_parte_II.md:246]`.
*Valore operativo*: dà all'operatore la fascia di prezzo esatta entro cui il raw touch è valido, pronta da confrontare col book sul broker.

**B4-R-21 — Campo pubblicato (pos. 5): `target_1` e `target_2`, distinti e ordinati.**
Sono pubblicati `target_1` e `target_2`, i due target strutturali, distinti e ordinati `[DOC-INTERNO CAP_02_parte_II.md:247]`.
*Valore operativo*: l'operatore vede entrambi i livelli obiettivo, distinti e in ordine, per pianificare la gestione manuale della posizione.

**B4-R-22 — Campo pubblicato (pos. 6): `stop_loss`.**
È pubblicato `stop_loss`, il prezzo strutturale di stop `[DOC-INTERNO CAP_02_parte_II.md:248]`.
*Valore operativo*: comunica all'operatore il livello di uscita in perdita, essenziale per dimensionare il rischio prima di entrare.

**B4-R-23 — Campo pubblicato (pos. 7): `timestamp_emission` (data e ora CET).**
È pubblicato `timestamp_emission`, l'istante di emissione, riportato come data e ora CET `[DOC-INTERNO CAP_02_parte_II.md:249]`.
*Valore operativo*: permette all'operatore di valutare quanto è "fresco" il segnale prima di agire (coerente con il vincolo di latenza).

**B4-R-24 — Campo pubblicato (pos. 8): `target_2_type` (qualificatore structural/synthetic).**
È pubblicato `target_2_type`, qualificatore della natura del livello target_2, dominio $\{\text{structural},\text{synthetic}\}$ `[DOC-INTERNO CAP_02_parte_II.md:250]`.
*Valore operativo*: permette al consumer mobile di distinguere un target_2 derivato da una struttura confermata del prezzo da uno sintetico calcolato dal modello, informazione di contesto utile alla lettura.
*(Rinvio: l'algoritmo che popola il valore è Parte IV, Cap.17.4 `[DOC-INTERNO CAP_02_parte_II.md:250]`.)*

**B4-R-25 — Campo pubblicato (pos. 9): `stop_type` (qualificatore structural/synthetic).**
È pubblicato `stop_type`, qualificatore della natura del livello stop_loss, dominio $\{\text{structural},\text{synthetic}\}$ `[DOC-INTERNO CAP_02_parte_II.md:251]`.
*Valore operativo*: permette al consumer mobile di distinguere uno stop derivato da una struttura confermata da uno sintetico, informazione di contesto utile alla lettura.
*(Rinvio: l'algoritmo che popola il valore è Parte IV, Cap.18.1 `[DOC-INTERNO CAP_02_parte_II.md:251]`.)*

**B4-CN-07 — I qualificatori non hanno impatto sulla decisione di ingresso (invariante).**
La presenza di `target_2_type` e `stop_type` permette di valutare la natura strutturale dei livelli **senza alcun impatto** sulla decisione di ingresso, che resta vincolata al raw touch dell'`entry_zone` `[DOC-INTERNO CAP_02_parte_II.md:253]`.
*Valore operativo*: chiarisce all'operatore che i due qualificatori sono solo contesto informativo e non modificano la regola di ingresso, evitando interpretazioni che cambierebbero il comportamento atteso.

**B4-R-26 — Esclusione dal messaggio di $\Delta t_{cromosoma}$ e $T_{touch}^{max}$.**
I campi $\Delta t_{cromosoma}$ e $T_{touch}^{max}$ **non** figurano nel messaggio all'operatore: sono parametri tecnici rilevanti per il log interno ma non per la decisione operativa `[DOC-INTERNO CAP_02_parte_II.md:253]`.
*Valore operativo*: il messaggio resta sgombro di parametri che l'operatore non usa per decidere, sostenendo la leggibilità mobile.
*(Rinvio: questi parametri sono per il log interno — vedi §11.)*

**B4-CN-08 — Il messaggio non contiene istruzioni di gestione attiva della posizione (invariante).**
Il messaggio **non** contiene istruzioni di gestione attiva della posizione (incrementi, scaling out, take profit anticipato, stop profit), in coerenza con il punto 8 della dichiarazione di intenti che riserva queste decisioni all'operatore `[DOC-INTERNO CAP_02_parte_II.md:253]`.
*Valore operativo*: l'operatore mantiene piena titolarità della gestione della posizione; il messaggio non lo induce ad azioni di gestione che il contratto riserva a lui.

---

## 8. Latenza di consegna (Cap.9.3)

**B4-NFR-03 — Vincolo di latenza di consegna $L \leq L_{max}$.**
Definita la latenza di consegna $L$ come intervallo tra `timestamp_emission` e l'istante di ricezione del messaggio sul cellulare dell'operatore, vale il vincolo $L \leq L_{max}$ `[DOC-INTERNO CAP_02_parte_II.md:257]` `[DOC-INTERNO CAP_02_parte_II.md:259]`.
*Valore operativo*: garantisce che, quando l'operatore legge e agisce, il prezzo strutturale di riferimento non si sia spostato in modo non trascurabile rispetto al momento dell'emissione, così che il segnale conservi valore informativo.

**B4-NFR-04 — Valore di lavoro di $L_{max}$ provvisorio (30 s), verifica empirica OPEN / PENDING-empirico.**
Il valore di lavoro provvisorio di $L_{max}$ è 30 secondi (oltre questa soglia il segnale perde valore informativo); il valore congelato definitivo è materia di Parte V, e **la verifica empirica della latenza effettiva del canale Telegram è materia di Appendice E** `[DOC-INTERNO CAP_02_parte_II.md:261]`. Il valore 30 s è citato dal CAP **come provvisorio**; la latenza effettiva del canale è **PENDING-empirico** (non verificata in questo blocco).
*Valore di sistema*: fissa un riferimento di lavoro tracciabile per il vincolo $L\leq L_{max}$ tenendo esplicito che il numero non è definitivo e la sua verifica resta aperta, premessa di una validazione empirica futura senza falsi affidamenti.

---

## 9. Politica anti-duplicato e regola del messaggio separato (Cap.9.4–9.5)

**B4-CN-09 — Anti-duplicato: ogni `signal_id` pubblicato una sola volta (invariante).**
Il motore pubblica ciascun `signal_id` **una sola volta**: dato l'insieme $\mathcal{P}$ dei `signal_id` già pubblicati con successo, il motore pubblica il messaggio se e solo se `signal_id`$\notin\mathcal{P}$, e contestualmente aggiunge `signal_id` a $\mathcal{P}$ `[DOC-INTERNO CAP_02_parte_II.md:265]`.
*Valore operativo*: l'operatore non riceve due volte lo stesso segnale e non rischia di aprire per errore due posizioni sullo stesso segnale.

**B4-CN-10 — $\mathcal{P}$ persistito su disco a fini anti-ripubblicazione ai restart (invariante).**
L'insieme $\mathcal{P}$ è persistito su disco insieme al log di emissione, in modo che i restart del motore non comportino ripubblicazione di segnali già notificati `[DOC-INTERNO CAP_02_parte_II.md:265]`.
*Valore di sistema*: garantisce che l'anti-duplicato sopravviva ai restart del motore, premessa di un comportamento di pubblicazione riproducibile e auditabile. *(Il formato/schema del log di emissione è materia di altro blocco — vedi §11; qui si prende solo il fatto che $\mathcal{P}$ è persistito a fini anti-ripubblicazione.)*

**B4-R-27 — Nuovo segnale in sostituzione = messaggio separato con proprio `signal_id`.**
Quando il motore emette un nuovo segnale in sostituzione di un precedente, il messaggio Telegram corrispondente è pubblicato come **messaggio separato**, con il proprio `signal_id` distinto `[DOC-INTERNO CAP_02_parte_II.md:269]`.
*Valore operativo*: l'operatore vede ogni nuovo segnale come messaggio a sé, con la sua chiave, senza confondersi con il precedente.
*(Premessa: la regola di sostituzione e l'evento del lifecycle sono consolidati in altro blocco — vedi §11.)*

**B4-CN-11 — No-edit del messaggio precedente (invariante, coerente con l'immutabilità del payload).**
Non viene effettuata alcuna operazione di modifica o edit sul messaggio Telegram precedente; il messaggio del segnale revocato resta visibile come traccia storica ma non rappresenta più un segnale attivo. La scelta di emettere messaggi separati anziché editare è coerente con l'invariante di payload immutabile (Cap.6.2): editare equivarrebbe a modificare il payload pubblicato `[DOC-INTERNO CAP_02_parte_II.md:269]`.
*Valore operativo*: l'operatore ha la garanzia che un messaggio già ricevuto non cambi mai sotto i suoi occhi, così ciò che ha letto e su cui ha agito resta verità storica.
*(Premessa: l'immutabilità del payload — Cap.6.2 — e lo stato `revoked` nel log interno sono consolidati in altri blocchi — vedi §11; qui richiamati come premessa, non ri-derivati.)*

**B4-R-28 — Notifica del `trigger_event` come messaggio separato.**
Al verificarsi del `trigger_event` (raw touch dell'entry zone) il motore pubblica una **notifica separata** sul canale Telegram, che fa riferimento al `signal_id` del segnale corrente, all'istante $t_{exec}$ del raw touch e all'`expiry` calcolata `[DOC-INTERNO CAP_02_parte_II.md:271]`.
*Valore operativo*: avvisa l'operatore nel preciso momento in cui il prezzo è entrato in zona e il segnale è eseguibile, informazione tempestiva e azionabile.
*(Premessa: il `trigger_event` come evento del lifecycle è consolidato in altro blocco — vedi §11; qui si consolida la sua **pubblicazione**, non l'evento.)*

**B4-CN-12 — La notifica del trigger è funzionalmente distinta dal messaggio di emissione (invariante).**
La notifica del `trigger_event` è funzionalmente distinta dal messaggio di emissione: l'emissione comunica l'esistenza del segnale e i suoi parametri; la notifica del trigger comunica che il prezzo è entrato nella zona e che il segnale è eseguibile. In Parte II si fissa il vincolo che essa sia pubblicata come **messaggio separato e non come edit**, contestualmente al riconoscimento del raw touch `[DOC-INTERNO CAP_02_parte_II.md:271]`.
*Valore operativo*: l'operatore distingue nettamente "esiste un segnale con questi parametri" da "ora puoi eseguire", senza ambiguità sul significato dei due messaggi.
*(Rinvio: il dettaglio del contratto informativo della notifica del trigger è Appendice E `[DOC-INTERNO CAP_02_parte_II.md:271]`.)*

---

## 10. Gestione degli errori di pubblicazione (Cap.9.6)

**B4-R-29 — Politica di retry su errore API Telegram.**
In caso di errore nella chiamata all'API Telegram (timeout, errori di rete, indisponibilità temporanea), il motore applica una politica di retry `[DOC-INTERNO CAP_02_parte_II.md:275]`.
*Valore operativo*: un errore transitorio del canale non fa perdere il segnale all'operatore; il motore ritenta automaticamente.

**B4-R-30 — Numero massimo di tentativi $n_{retry}$ (valore di lavoro provvisorio 3).**
La politica prevede un numero massimo di tentativi $n_{retry}$, valore di lavoro provvisorio $n_{retry}=3$ `[DOC-INTERNO CAP_02_parte_II.md:277]`. Il valore 3 è citato dal CAP **come provvisorio**; il valore definitivo è Parte V.
*Valore di sistema*: limita il numero di ritentativi a un tetto definito e tracciabile, premessa di un comportamento di pubblicazione deterministico e auditabile.

**B4-R-31 — Backoff esponenziale fra i tentativi (base provvisoria 2 s, raddoppiata).**
Fra i tentativi si applica un backoff esponenziale, con base provvisoria $\Delta t_{retry}=2$ secondi raddoppiata a ogni tentativo `[DOC-INTERNO CAP_02_parte_II.md:278]`. Il valore 2 s è citato dal CAP **come provvisorio**; il valore definitivo è Parte V.
*Valore di sistema*: distanzia i ritentativi in modo crescente per non insistere su un canale temporaneamente indisponibile, premessa di una gestione robusta degli errori transitori.

**B4-R-32 — Esito al fallimento finale: errore registrato nel log, nessuna ulteriore pubblicazione.**
In caso di fallimento finale (tutti i tentativi esauriti), l'errore è registrato nel log di emissione e non avviene nessuna ulteriore pubblicazione `[DOC-INTERNO CAP_02_parte_II.md:279]`.
*Valore di sistema*: il fallimento di consegna lascia una traccia esplicita anziché restare implicito, premessa per diagnosticare i segnali non arrivati all'operatore. *(Il formato del log è materia di altro blocco — vedi §11; qui si prende la politica.)*

**B4-CN-13 — Al fallimento finale il `signal_id` non è aggiunto a $\mathcal{P}$ (invariante).**
In caso di fallimento finale, il `signal_id` **non** viene aggiunto a $\mathcal{P}$ e il segnale è registrato come **non pubblicato** `[DOC-INTERNO CAP_02_parte_II.md:279]`.
*Valore di sistema*: mantiene coerente l'invariante anti-duplicato (B4-CN-09): solo i segnali effettivamente consegnati entrano in $\mathcal{P}$, così un eventuale ritentativo futuro resta legittimo e lo stato riflette la realtà della consegna.

**B4-CN-14 — Il fallimento di pubblicazione è tracciato, non implicito (invariante).**
Il fallimento di pubblicazione è tracciato nel log e non rimane implicito `[DOC-INTERNO CAP_02_parte_II.md:281]`.
*Valore di sistema*: garantisce che ogni mancata consegna sia esplicitamente registrata, premessa di un audit trail completo e di un'eventuale azione correttiva.

*(Rinvio: i parametri $n_{retry}$, $\Delta t_{retry}$, $L_{max}$ sono congelati in Parte V; le specifiche di interazione con l'API Telegram sono Appendice E `[DOC-INTERNO CAP_02_parte_II.md:281]`.)*

---

## 11. Nota di rinvio (materia adiacente deliberatamente NON consolidata in B4)

Le seguenti materie, adiacenti a emissione/consegna, sono **deliberatamente rinviate** ad altri blocchi/Parti (non sono gap di B4):

| Materia adiacente | Destinazione | Perché fuori B4 |
|---|---|---|
| Schema-payload come **dato**: campi della tupla, domini, banda $b$, $d_{stop}>b$, qualificatori `{structural,synthetic}` **come dominio**, immutabilità del payload (Cap.6.2), segnale unico attivo come proprietà del payload | Altro blocco (Payload del segnale) | B4 usa i campi come **dato già fissato** e fissa il **contratto di presentazione**, non i domini/immutabilità |
| Stati e transizioni, **raw touch / `trigger_event` come evento del lifecycle**, timer come semantica di scadenza, regola di sostituzione (Cap.6.3/Cap.7) | Altro blocco (State-machine & lifecycle) | B4 consolida la **pubblicazione/notifica** del trigger, non l'evento del lifecycle |
| **Formato/schema** dei log (emissione/transizioni/chiusura), persistenza e determinismo del replay (Cap.10); stato `revoked` come voce di log | Altro blocco (runtime/log) | B4 prende da Cap.9.4/9.6 la **politica** (una-volta-sola, $\mathcal{P}$ persistito, esito al fallimento), non lo schema del log |
| **Sessione operativa come requisito** runtime (verifica empirica della finestra) | Altro blocco (runtime/sessione) | In B4 la finestra 8:00–22:00 CET compare solo come "nessuna fase speciale di emissione per orario" (Cap.8.4) |
| Formule del modello di volatilità EGARCH, conversione $\hat\sigma_{\text{pt}}=\hat\sigma\cdot p_t$, forma esplicita di $\tau_{vol}$, definizione operativa di $A_{range}$, algoritmo di popolamento `target_2_type`/`stop_type` | CAP chiusi, Parte III/IV | In B4 solo come rinvio (B4-R-06, B4-R-08, B4-R-09, B4-R-24, B4-R-25) |
| **Valori congelati**: $L_{max}$, $n_{retry}$, $\Delta t_{retry}$ definitivi, valori delle soglie $\tau_{vol}/\tau_{liq}/\tau_{dist}^{\sigma}$, valore 80 del filtro | Parte V | In B4 i valori di lavoro provvisori sono citati dal CAP **come provvisori**; i definitivi sono Parte V |
| Dettaglio tecnico del canale Telegram: setup bot, `chat_id`, stringhe esatte, **contratto informativo della notifica del trigger**, specifiche API Telegram | Appendice E (FASE-D) | In B4 solo come rinvio (B4-NFR-01, B4-CN-12, B4-R-29) |

Nessuna fonte esterna è usata come fonte unica in B4. La Telegram Bot API è livello-4 `[WIKI-HINT, da verificare]` e non fonda alcun requisito: ogni requisito di B4 regge sul Cap.8/9 di `CAP_02_parte_II.md` (le specifiche API Telegram sono comunque rinviate ad Appendice E).

---

## 12. Matrice di tracciabilità

| ID | Proposizione (sintesi) | Citazione CAP | Valore |
|---|---|---|---|
| B4-R-01 | Decisione di emettere presa prima dell'emissione | CAP_02_parte_II.md:183 | operativo |
| B4-CN-01 | Assenza di guardie/filtri post-emissione | CAP_02_parte_II.md:183 | operativo |
| B4-R-02 | Motivazione (a): coerenza punto 1 dichiarazione di intenti | CAP_02_parte_II.md:185 | operativo |
| B4-R-03 | Motivazione (b): condizioni addestrabili/calcolabili su storico | CAP_02_parte_II.md:185, :187 | operativo |
| B4-R-04 | Motivazione (c): condizione di spread eliminata | CAP_02_parte_II.md:185 | operativo |
| B4-R-05 | Motivazione (d): l'operatore valuta l'esecuzione real-time | CAP_02_parte_II.md:185 | operativo |
| B4-R-06 | Condizione di volatilità $r_{1m}\leq\tau_{vol}$ | CAP_02_parte_II.md:191, :193 | operativo |
| B4-R-07 | Condizione di liquidità $v_{1m}\geq\tau_{liq}$ | CAP_02_parte_II.md:197, :199 | operativo |
| B4-R-08 | Condizione di distanza sigma-units $\geq\tau_{dist}^{\sigma}$ | CAP_02_parte_II.md:203, :205 | operativo |
| B4-R-09 | Filtro 80 pt come condizione di emissione (regola) | CAP_02_parte_II.md:209 | operativo |
| B4-CN-02 | Filtro 80 pt vincolo assoluto non allentabile | CAP_02_parte_II.md:209 | operativo |
| B4-CN-03 | Distinzione leva-ottimizzabile vs floor-fisso | CAP_02_parte_II.md:211 | di sistema |
| B4-R-10 | Regola di emissione (AND logico) | CAP_02_parte_II.md:215, :217 | operativo |
| B4-CN-04 | Emissione tutto-o-niente | CAP_02_parte_II.md:219 | operativo |
| B4-R-11 | Non-emissione: nessun `signal_id` | CAP_02_parte_II.md:219 | di sistema |
| B4-R-12 | Non-emissione: nessuna pubblicazione | CAP_02_parte_II.md:219 | operativo |
| B4-R-13 | Non-emissione: nessun log | CAP_02_parte_II.md:219 | di sistema |
| B4-R-14 | Non-emissione: continua a valutare | CAP_02_parte_II.md:219 | operativo |
| B4-CN-05 | Raw touch sempre eseguibile, nessuna guardia ulteriore | CAP_02_parte_II.md:225 | operativo |
| B4-R-15 | Condizioni patologiche al raw touch in carico all'operatore | CAP_02_parte_II.md:225 | operativo |
| B4-R-16 | Condizioni uniformi su 8:00–22:00, no fasi speciali | CAP_02_parte_II.md:227 | operativo |
| B4-NFR-01 | Formato messaggio per lettura mobile | CAP_02_parte_II.md:235 | operativo |
| B4-NFR-02 | Canale a latenza compatibile con l'urgenza | CAP_02_parte_II.md:235 | operativo |
| B4-CN-06 | Ordine obbligatorio dei campi | CAP_02_parte_II.md:241 | operativo |
| B4-R-17 | Campo pos.1 `signal_id` | CAP_02_parte_II.md:243 | operativo |
| B4-R-18 | Campo pos.2 `direction` | CAP_02_parte_II.md:244 | operativo |
| B4-R-19 | Campo pos.3 `setup_class` | CAP_02_parte_II.md:245 | operativo |
| B4-R-20 | Campo pos.4 `entry_zone` come $[p_{ref}-b,p_{ref}+b]$ | CAP_02_parte_II.md:246 | operativo |
| B4-R-21 | Campo pos.5 `target_1`+`target_2` | CAP_02_parte_II.md:247 | operativo |
| B4-R-22 | Campo pos.6 `stop_loss` | CAP_02_parte_II.md:248 | operativo |
| B4-R-23 | Campo pos.7 `timestamp_emission` (CET) | CAP_02_parte_II.md:249 | operativo |
| B4-R-24 | Campo pos.8 `target_2_type` | CAP_02_parte_II.md:250 | operativo |
| B4-R-25 | Campo pos.9 `stop_type` | CAP_02_parte_II.md:251 | operativo |
| B4-CN-07 | Qualificatori senza impatto sull'ingresso | CAP_02_parte_II.md:253 | operativo |
| B4-R-26 | Esclusione di $\Delta t_{cromosoma}$/$T_{touch}^{max}$ dal messaggio | CAP_02_parte_II.md:253 | operativo |
| B4-CN-08 | No istruzioni di gestione attiva (punto 8) | CAP_02_parte_II.md:253 | operativo |
| B4-NFR-03 | Vincolo latenza $L\leq L_{max}$ | CAP_02_parte_II.md:257, :259 | operativo |
| B4-NFR-04 | $L_{max}=30$ s provvisorio, verifica empirica OPEN | CAP_02_parte_II.md:261 | di sistema |
| B4-CN-09 | Anti-duplicato: ogni `signal_id` una sola volta | CAP_02_parte_II.md:265 | operativo |
| B4-CN-10 | $\mathcal{P}$ persistito a fini anti-ripubblicazione | CAP_02_parte_II.md:265 | di sistema |
| B4-R-27 | Nuovo segnale = messaggio separato | CAP_02_parte_II.md:269 | operativo |
| B4-CN-11 | No-edit del messaggio precedente | CAP_02_parte_II.md:269 | operativo |
| B4-R-28 | Notifica del `trigger_event` come messaggio separato | CAP_02_parte_II.md:271 | operativo |
| B4-CN-12 | Notifica trigger distinta dall'emissione, separata/non-edit | CAP_02_parte_II.md:271 | operativo |
| B4-R-29 | Politica di retry su errore API Telegram | CAP_02_parte_II.md:275 | operativo |
| B4-R-30 | $n_{retry}$ (provvisorio 3) | CAP_02_parte_II.md:277 | di sistema |
| B4-R-31 | Backoff esponenziale (provvisorio 2 s, raddoppiato) | CAP_02_parte_II.md:278 | di sistema |
| B4-R-32 | Fallimento finale: errore nel log, nessuna ulteriore pubblicazione | CAP_02_parte_II.md:279 | di sistema |
| B4-CN-13 | Al fallimento `signal_id` non aggiunto a $\mathcal{P}$, segnale non pubblicato | CAP_02_parte_II.md:279 | di sistema |
| B4-CN-14 | Fallimento tracciato, non implicito | CAP_02_parte_II.md:281 | di sistema |

**Totale (parte CAP_02 Cap.8-9)**: 32 R + 14 CN + 4 NFR = **50 requisiti atomici**. *(Per il totale aggiornato comprensivo dell'estensione Cap.29 vedi §E.6.)*

---

# Estensione consegna — CAP_06 PVI (Cap.29)

> **Tag commit**: `[SPEC-FUNZ-01-B4-EXT]`. **Sede**: CLI. **Fonte unica**: `docs/methodology_v2/CAP_06_parte_VI.md`, **Cap.29 (§29.1–29.5)**.

## E.0 — Nota di provenienza ed estensione

Questa sezione è un'**estensione autorizzata** del blocco B4, **non** un nuovo blocco e **non** un rifacimento.

- **Autorizzazione**: decisione del supervisore AC, **Opzione 1** (recuperare la materia di **consegna** di CAP_06 Parte VI omessa dal perimetro-fonte originario di B4). La mappa di chunking assegnava a B4 anche CAP_06 PVI Cap.27-29; di quei tre capitoli **solo Cap.29 è consegna** (operatività mobile), mentre Cap.27 (pipeline di inference/EGARCH) e Cap.28 (anti-doppio operazionale, non-refresh, tie-break, logging candidati, determinismo del replay) sono **runtime** e sono **rinviati a B5** (vedi §E.5). La mappa è stata aggiornata in pari data per riflettere il taglio consegna/runtime: scostamento **autorizzato e tracciato**, non un drift.
- **Cosa recupera**: i due requisiti-bersaglio della consegna di CAP_06 — **mobile-first** (famiglia `B4-NFR`, recupera **NFR-6.1** della v2) e le **3 notifiche standard** (famiglia `B4-R`, recupera **R-6.4** della v2).
- **Invarianza della parte già PASS**: la parte di B4 su CAP_02 Cap.8-9 (i 50 requisiti delle §1–§12, **PASS `c3be05e`**) **non** si ri-deriva, **non** si riapre, **non** si rivede. Gli ID esistenti non sono rinumerati: questa estensione **continua** lo schema-ID di B4 (prossimi liberi: `B4-NFR-05`, `B4-R-33`).
- **Fonte e cecità**: i requisiti di questa estensione sono derivati **dal solo Cap.29** di `CAP_06_parte_VI.md`. Le voci del contratto a 9 campi (Cap.9.2) e la pubblicazione della notifica `trigger_event` (Cap.9.5) — già consolidate in B4 — sono **citate come premessa**, **non** ri-elencate. Gli stati terminali del lifecycle (Cap.7, materia di B3) sono **citati come premessa**, **non** ri-derivati.

## E.1 — Requisiti mobile-first (Cap.29.1–29.2) — recupera NFR-6.1

La consegna del segnale avviene sul **bot Telegram personale** dell'operatore, che esegue manualmente da cellulare in attenzione limitata. Cap.29 **rappresenta** il payload formale già fissato (le 9 voci del contratto di Cap.9.2 di Parte II, **già consolidate in B4 — §7, B4-CN-06/B4-R-17..R-25**, qui citate come premessa e **non** ri-elencate) in un **layout mobile-first**, senza introdurre campi nuovi.

**B4-NFR-05 — La consegna è progettata per essere leggibile e azionabile da cellulare in attenzione limitata (mobile-first).**
Il messaggio di consegna è progettato perché l'operatore lo legga e ci agisca da schermo di cellulare in condizioni di attenzione limitata e discontinua durante la giornata lavorativa; questo profilo operativo è il criterio di progettazione del messaggio Telegram in Cap.29 `[DOC-INTERNO CAP_06_parte_VI.md:146]`.
*Valore operativo*: chi opera da cellulare in pause brevi coglie il segnale a colpo d'occhio e può agire subito, riducendo il rischio di errore di lettura prima dell'invio manuale dell'ordine.

**B4-NFR-06 — Il layout mobile-first rappresenta lo stesso payload formale senza introdurre né omettere campi (estensione cosmetica, non del contratto).**
Il layout mobile-first **rappresenta** le 9 voci del payload formale di Cap.9.2 di Parte II (già B4) riordinandole per priorità di lettura: **nessun campo nuovo** è introdotto e nessuno è omesso; la distinzione dichiarata è *payload formale (immutabile) vs rappresentazione mobile (cosmetica)* `[DOC-INTERNO CAP_06_parte_VI.md:146]` `[DOC-INTERNO CAP_06_parte_VI.md:154]`.
*Valore operativo*: l'operatore vede sempre le stesse informazioni del contratto (niente in più che lo distragga, niente in meno che gli manchi), solo disposte per la lettura mobile; ciò che legge sul cellulare è esattamente ciò che il motore ha pubblicato e loggato.
*(Premessa citata, non ri-derivata: il contratto a 9 voci del messaggio è B4 — §7, B4-CN-06/B4-R-17..R-25 — e Cap.9.2 di Parte II resta il riferimento normativo del contenuto.)*

**B4-NFR-07 — Il contenuto critico è leggibile sul cellulare senza scroll orizzontale ed entro la prima schermata verticale.**
Il messaggio è interamente testuale e self-contained ed è progettato per schermi mobile di larghezza tipica, leggibile **senza scroll orizzontale** (linee corte) e con il contenuto critico (direzione, entry_zone, target_1, stop_loss) visibile **entro la prima schermata** (senza scroll verticale eccessivo) `[DOC-INTERNO CAP_06_parte_VI.md:152]`.
*Valore operativo*: l'operatore legge le informazioni che servono per decidere senza dover scorrere il messaggio, evitando di perdere un campo critico (es. il lato o lo stop) in fondo a un testo lungo.

## E.2 — Le 3 notifiche standard per segnale (Cap.29.4) — recupera R-6.4

**B4-R-33 — Il canale pubblica esattamente 3 notifiche standard per segnale.**
Per ogni segnale il canale Telegram pubblica **esattamente 3 notifiche standard**: (i) **emissione** (§E.3), (ii) **`trigger_event`** se avviene il raw touch (§E.4), (iii) **transizione a stato terminale** (§E.5) `[DOC-INTERNO CAP_06_parte_VI.md:220]`.
*Valore operativo*: l'operatore sa in anticipo quante e quali comunicazioni riceverà per ciascun segnale, così non resta in attesa di messaggi che non arriveranno né teme di averne persi.

**B4-R-34 — Tra una notifica e la successiva il canale non invia aggiornamenti di stato (no polling, no refresh).**
Tra una notifica standard e la successiva l'operatore **non** riceve aggiornamenti di stato del segnale: il motore monitora silenziosamente e l'operatore segue lo stato sul terminale Telegram in modo statico, senza polling né refresh `[DOC-INTERNO CAP_06_parte_VI.md:220]`.
*Valore operativo*: il canale resta sgombro tra un evento e l'altro; l'operatore non è bombardato da aggiornamenti continui e dedica attenzione solo ai tre momenti che contano.

## E.3 — Notifica 1: emissione (Cap.29.2)

**B4-R-35 — La 1ª notifica standard è il messaggio di emissione, pubblicato al momento dell'emissione del segnale.**
La prima delle 3 notifiche standard è il **messaggio di emissione**, che pubblica le 9 voci del payload nel layout mobile-first al momento dell'emissione del segnale `[DOC-INTERNO CAP_06_parte_VI.md:220]` `[DOC-INTERNO CAP_06_parte_VI.md:154]`.
*Valore operativo*: l'operatore è avvisato dell'esistenza del segnale e ne riceve i parametri appena il motore lo emette, in tempo per valutare l'ingresso.
*(Premessa citata, non duplicata: la pubblicazione del messaggio di emissione e il suo contratto informativo a 9 voci sono già B4 — §7; qui si consolida solo il suo ruolo di **prima delle 3 notifiche standard**.)*

## E.4 — Notifica 2: `trigger_event` (Cap.29.3)

**B4-R-36 — La 2ª notifica standard è la notifica `trigger_event`, pubblicata al raw touch dell'entry zone.**
La seconda delle 3 notifiche standard è la notifica **`trigger_event`**, pubblicata **se avviene** il raw touch della `entry_zone`, come messaggio Telegram separato dal messaggio di emissione `[DOC-INTERNO CAP_06_parte_VI.md:220]` `[DOC-INTERNO CAP_06_parte_VI.md:190]`.
*Valore operativo*: l'operatore è avvisato nel momento esatto in cui il prezzo è entrato in zona e il segnale è eseguibile, informazione tempestiva e azionabile.
*(Premessa citata, non duplicata: la **pubblicazione** della notifica `trigger_event` come messaggio separato è già consolidata in B4 — §9, B4-R-28/B4-CN-12, da Cap.9.5 di Parte II; il `trigger_event` come **evento** del lifecycle è materia di B3, citato come premessa e non ri-derivato. Qui si consolida solo il suo ruolo di **seconda delle 3 notifiche standard**.)*

**B4-R-37 — La notifica `trigger_event` non modifica il messaggio di emissione (è un messaggio separato, no edit/append).**
La notifica `trigger_event` è un messaggio distinto che **non** modifica il messaggio di emissione (no edit, no append) e riporta esplicitamente il `signal_id` del segnale originario `[DOC-INTERNO CAP_06_parte_VI.md:190]`.
*Valore operativo*: l'operatore distingue nettamente la comunicazione "esiste un segnale" da "ora puoi eseguire", e il messaggio già letto non gli cambia sotto gli occhi; il `signal_id` gli permette di correlare le due notifiche.
*(Coerente con l'invariante no-edit/immutabilità già in B4 — §9, B4-CN-11; qui ribadito a livello di consegna mobile sulla notifica `trigger_event`.)*

## E.5 — Notifica 3: transizione terminale (Cap.29.5)

**B4-R-38 — La 3ª notifica standard è il messaggio di chiusura, pubblicato alla transizione del segnale a uno stato terminale.**
La terza delle 3 notifiche standard è il **messaggio di chiusura**, pubblicato alla transizione del segnale dallo stato `active` a uno degli **stati terminali** del lifecycle, e informa l'operatore della conclusione del segnale e del risultato `[DOC-INTERNO CAP_06_parte_VI.md:220]` `[DOC-INTERNO CAP_06_parte_VI.md:223]` `[DOC-INTERNO CAP_06_parte_VI.md:225]`.
*Valore operativo*: l'operatore sa quando il segnale è concluso e con quale esito, così può chiudere mentalmente la posizione e non resta in attesa di un segnale già terminato.
*(Premessa citata, non ri-derivata: gli **stati terminali** e le transizioni del lifecycle sono materia di B3 (Cap.7); qui si consolida solo la **notifica** della transizione — che esiste, quando scatta, cosa veicola — non la state machine.)*

**B4-R-39 — La notifica di chiusura veicola lo stato terminale finale del segnale.**
La notifica di chiusura riporta lo **stato terminale finale** raggiunto dal segnale, uno fra i sei stati terminali del lifecycle `[DOC-INTERNO CAP_06_parte_VI.md:230]`.
*Valore operativo*: l'operatore conosce il motivo preciso della chiusura (target raggiunto, stop, scadenza, invalidazione, mancato target, revoca) e può registrarlo per la propria contabilità manuale.
*(Premessa citata, non ri-derivata: l'**insieme** dei sei stati terminali è definito in B3 (Cap.7); qui si consolida solo che la notifica li **veicola** alla consegna.)*

**B4-R-40 — La notifica di chiusura veicola il risultato $R_{gross}$ del segnale (vuoto/`n/a` per i segnali non eseguiti).**
La notifica di chiusura riporta il risultato **$R_{gross}$** in punti FIB (positivo, negativo o nullo) per i segnali eseguiti, e **vuoto o `n/a`** per i segnali non eseguiti `[DOC-INTERNO CAP_06_parte_VI.md:232]`.
*Valore operativo*: l'operatore legge a chiusura il risultato lordo del segnale in punti, utile per la propria contabilità, con la distinzione esplicita fra segnali eseguiti e segnali mai entrati.

## E.6 — Matrice di tracciabilità (estensione Cap.29)

| ID | Proposizione (sintesi) | Citazione CAP | Valore |
|---|---|---|---|
| B4-NFR-05 | Consegna leggibile/azionabile da cellulare in attenzione limitata (mobile-first) | CAP_06_parte_VI.md:146 | operativo |
| B4-NFR-06 | Layout mobile-first rappresenta lo stesso payload, senza nuovi/omessi campi | CAP_06_parte_VI.md:146, :154 | operativo |
| B4-NFR-07 | Contenuto critico senza scroll orizzontale ed entro la prima schermata | CAP_06_parte_VI.md:152 | operativo |
| B4-R-33 | Esattamente 3 notifiche standard per segnale | CAP_06_parte_VI.md:220 | operativo |
| B4-R-34 | Nessun aggiornamento di stato tra le notifiche (no polling/refresh) | CAP_06_parte_VI.md:220 | operativo |
| B4-R-35 | Notifica 1 = emissione, al momento dell'emissione | CAP_06_parte_VI.md:220, :154 | operativo |
| B4-R-36 | Notifica 2 = `trigger_event`, al raw touch, messaggio separato | CAP_06_parte_VI.md:220, :190 | operativo |
| B4-R-37 | Notifica `trigger_event` non modifica l'emissione (no edit/append), con `signal_id` | CAP_06_parte_VI.md:190 | operativo |
| B4-R-38 | Notifica 3 = chiusura, alla transizione a stato terminale | CAP_06_parte_VI.md:220, :223, :225 | operativo |
| B4-R-39 | Notifica di chiusura veicola lo stato terminale finale (1 di 6) | CAP_06_parte_VI.md:230 | operativo |
| B4-R-40 | Notifica di chiusura veicola $R_{gross}$ (vuoto/`n/a` se non eseguito) | CAP_06_parte_VI.md:232 | operativo |

**Estensione Cap.29**: 8 R + 0 CN + 3 NFR = **11 requisiti atomici**.

**Totale B4 (CAP_02 Cap.8-9 + CAP_06 Cap.29)**: 40 R + 14 CN + 7 NFR = **61 requisiti atomici**.

## E.7 — Nota di rinvio (materia di CAP_06 PVI deliberatamente rinviata a B5)

Le seguenti materie di CAP_06 Parte VI sono **runtime**, non consegna, e sono **deliberatamente rinviate a B5** (non sono gap di questa estensione):

| Materia di CAP_06 PVI | Destinazione | Perché fuori da questa estensione (consegna) |
|---|---|---|
| Pipeline di inference real-time, modello di volatilità EGARCH (Cap.27) | **B5** (runtime) | È la logica di produzione del segnale, non la sua consegna all'operatore |
| Politica anti-doppio-segnale operazionale, non-refresh, tie-break, logging dei candidati, determinismo del replay (Cap.28 intero, §28.1–28.4) | **B5** (runtime) | È comportamento del motore a runtime, non rappresentazione/consegna del messaggio |

**Distinzione consegna/runtime (cardine)**: questa estensione consolida **solo** la materia di **consegna** (Cap.29: come il segnale e le sue notifiche sono rappresentati e recapitati all'operatore mobile). La materia **runtime** (Cap.27 pipeline/inference; Cap.28 intero) è di B5. Nota di confine: la gestione duplicati/idempotenza di lettura di Cap.29.4 (idempotenza visiva via `signal_id`, anti-ripubblicazione ai restart) è già coperta in B4 — §9, B4-CN-09/B4-CN-10 — da Cap.9.4 di Parte II; di Cap.29.4 questa estensione recupera **solo** la regola delle 3 notifiche standard (B4-R-33/B4-R-34), non l'anti-duplicato già consolidato.

---

*Documento B4 della spec ricostruita a blocchi. Parte CAP_02 Cap.8-9 (§1–§12) costruita in cieco dai soli Cap.8 (8.1–8.4) e Cap.9 (9.1–9.6) di `CAP_02_parte_II.md` (pin `a1625df`), **PASS `c3be05e`**. Estensione consegna (§E) costruita in cieco dal solo Cap.29 di `CAP_06_parte_VI.md` (lettura del B4 esistente solo per continuità-ID e no-duplicazione). File autonomo, sarà ricomposto a fine serie (dopo B8).*
