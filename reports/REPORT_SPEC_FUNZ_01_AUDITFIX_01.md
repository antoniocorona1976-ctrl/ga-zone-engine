# REPORT — SPEC-FUNZ-01-AUDITFIX-01 (chiusura gap dell'audit indipendente, lato BLOCCHI)

> Track: Business-spec (SPEC-FUNZ). Sede: CLI. Tag commit: `[SPEC-FUNZ-01-AUDITFIX-01]`. HEAD task: `a3dd507`.
> Natura: remediation MIRATA di 6 difetti confermati dall'audit indipendente (`wf_589a4b92`), non ricostruzione. Tocco solo i 4 file-blocco indicati (B3, B5, B6, B8).

## Conferma letture obbligatorie (in testa, come da card §1)
1. `tasks/METODO.md` — letto integralmente (RM-1..RM-4, RACC-METODO-2, Freeze G-09, §Superfici GOV-SURFACES-01, §Enforcement guard). Prima azione assoluta.
2. `.claude/BASE_COMUNE.md` — letto (ciclo, check post-Developer §5, onestà claim->evidenza §8, registry §9).
3. `.claude/agents/spec_developer.md` — letto (atomicità N1, fonte di verità RM-1/2/3, gestione blocchi F6, pre-consegna).
4. `tasks/ACTIVE_TASK.md` — la card AUDITFIX-01, eseguita alla lettera: i 6 fix di §3, i vincoli di §4.

---

## Sezione 1 — Cosa è stato prodotto

Patch chirurgiche ai SOLI 4 file-blocco toccati dai 6 fix, ciascun requisito nuovo derivato dalla riga CAP riletta token-per-token a HEAD `a3dd507`:

| Fix | Blocco | Tipo | Azione | ID nuovo / ancora corretta |
|-----|--------|------|--------|----------------------------|
| F1 | B6 | gap MEDIUM | Regola di consumo a valle per-categoria-di-feature (5 categorie). 5 requisiti atomici N1. | B6-R-38 (volatilità), B6-R-39 (prezzo), B6-R-40 (volume), B6-R-41 (struttura), B6-R-42 (touch) |
| F2 | B3 | gap LOW | Subordinazione: profitto netto = metrica PRIMARIA; pi/MFE/MAE/f_stop subordinati. Criterio dichiarato, NON esito d'edge. | B3-R-48 |
| F3 | B5 | miscitation LOW | Aggiunta l'ancora del numero 1680 a :290; proposizione invariata. | ancora CAP_09:290 aggiunta a B5-CN-05 (no nuovo ID) |
| F4 | B6 | gap LOW | Vincolo encoding BOM/UTF-8 dell'header CSV runtime. Fonte CAP TROVATA (non in sospeso). | B6-CN-25 |
| F5 | B6 | gap LOW | Marker BACKFILL_VERIFIED_T3/BACKFILL_UNVERIFIED + routing al gate Cap.60. | B6-R-43 |
| F6 | B8 | gap LOW | Dipendenza FASE-D estensione immutabilità CANDLERANGE oltre T+3, dipendenza aperta / PENDING-empirico, mai risolta. | B8-R-13 |

File modificati: `docs/spec_funzionale/SPEC_FUNZ_01_B3.md`, `_B5.md`, `_B6.md`, `_B8.md` (+ questo REPORT + `tasks/DEV_STATUS.md`). Nessun altro file toccato.

### Dettaglio per fix (finding -> fonte CAP:riga riletta -> ID/ancora -> evidenza)

F1 (B6, MEDIUM): manca la regola di consumo per-categoria-di-feature (volatilità solo su barre reali; touch/livello mai su sintetiche). Fonte riletta CAP_09_parte_9.md:185-189 (blocco Coerenza con la regola d'uso a valle di Cap.40): r185 volatilità->bar_synthetic=False; r186 prezzo->griglia uniforme completa inclusi sintetici; r187 volume->bar_synthetic=False; r188 struttura->griglia uniforme completa; r189 touch entry zone->mai su barra bar_synthetic=True. N1: blocco con 5 concern eterogenei (regole opposte) -> 5 requisiti atomici. Evidenza: B6.md §6bis.1, B6-R-38..42; matrice §7.1.

F2 (B3, LOW): omessa la subordinazione (profitto netto = metrica primaria). Fonte riletta CAP_02_parte_II.md:411 (Cap.11.5). N1: nuovo B3-R-48 (non estensione di B3-R-47, concern diverso). Criterio NON esito d'edge: dichiarato nessun valore di profitto, esito d'edge PENDING-empirico esclusiva validator/FASE-D. Evidenza: B3.md §6.4, B3-R-48; matrice §8.1.

F3 (B5, LOW): B5-CN-05 ancora 1680 a :292/:302 ma il numero 1680 sta su :290. Fonte riletta CAP_09_parte_9.md:290 (dominio fino a 1680 minuti, scavalca le interruzioni notturne) = unica occorrenza di 1680. Azione: corretta SOLO l'ancora (aggiunta :290 in Tracciabilità e Valore di B5-CN-05; :292,302 restano). Proposizione invariata, nessun nuovo ID, B5 invariato (35). Evidenza: B5.md B5-CN-05; matrice §7.1.

F4 (B6, LOW): header CSV runtime, manca il vincolo encoding (BOM/UTF-8). Fonte CAP TROVATA via Grep: CAP_09_parte_9.md:117 (Cap.48: "Ogni file CSV prodotto dalla pipeline runtime ha header obbligatorio BOM UTF-8..."), + :145 + D-9-5 (:420). Concern distinto da B6-CN-05 (campi) -> nuovo B6-CN-25 (N1). F4 NON in sospeso. Evidenza: B6.md §6bis.2, B6-CN-25; matrice §7.1.

F5 (B6, LOW): omessi marker BACKFILL_VERIFIED_T3/UNVERIFIED e routing al gate Cap.60. Fonte riletta CAP_10_parte_10.md:90 (Cap.59 punto 4): "Marker di esito: BACKFILL_VERIFIED_T3 ...; altrimenti BACKFILL_UNVERIFIED con flag operativo che richiede il check di riconciliazione di Cap.60." Grafia: usata BACKFILL_UNVERIFIED (esatta del CAP), non l'abbreviazione UNVERIFIED della card. Marker inglesi -> non triggerano il guard. Nuovo B6-R-43 (N1). Evidenza: B6.md §6bis.3, B6-R-43; matrice §7.1.

F6 (B8, LOW): omessa dalla §2 la dipendenza FASE-D estensione immutabilità CANDLERANGE oltre T+3. Fonte riletta CAP_10_parte_10.md:234 (Cap.64): "Estensione immutabilita' barre CANDLERANGE oltre T+3 ... Una eventuale estensione richiede nuovo probe empirico (Q-XX al Planner, NON dentro Parte 10)." Nuovo B8-R-13 in §2, marcato dipendenza aperta / PENDING-empirico, mai risolto; aggiunto a lista PENDING §3 e matrice §4.1. Evidenza: B8.md §2 B8-R-13, §3, §4.1.

---

## Sezione 2 — Ipotesi di partenza

- I 6 finding dell'audit (`wf_589a4b92`) sono autoritativi (card §2): non li ri-litigo. Ho riletto la riga CAP reale a HEAD prima di ogni citazione (AC-G7), perché i pin erano puntatori dell'audit.
- I CAP chiusi PASS sono frozen (G-09): sola lettura, mai ri-derivati, mai modificati.
- Path CAP: arabo per parti 8/9/10, romano per II (`CAP_02_parte_II.md`) — confermato con Glob.
- Edge PENDING-empirico (cardine ereditato B7/B8): nessuna asserzione d'esito; F2 resta criterio dichiarato, F6 resta dipendenza aperta.

---

## Sezione 3 — Decisioni rilevanti

1. F1 -> 5 requisiti, non 1 (atomicità N1): le 5 categorie hanno regole opposte (volatilità/volume/touch escludono i sintetici; prezzo/struttura li includono); un unico requisito sfuggirebbe alla verifica singola.
2. F2 -> nuovo B3-R-48, non estensione di B3-R-47: due proposizioni distinte; N1 impone ID separati.
3. F3 -> solo l'ancora: proposizione cardine-fedele; aggiunta :290 senza toccare testo né ancore :292/:302. Nessun nuovo ID.
4. F4 -> fonte trovata, requisito creato: CAP_09:117 esiste ed è esplicita; F4 NON in sospeso; concern distinto da B6-CN-05.
5. F5 -> grafia canonica del CAP: usato BACKFILL_UNVERIFIED (grafia esatta r90).
6. Guard RM-1: riformulate le mie righe nuove che contenevano "verificat" (B6-R-43, B8-R-13 in più forme) con "attestata empiricamente in modo diretto" / "non un fatto dimostrato" / "non dimostrata" — NESSUN override (card §4). Controllo: il diff delle righe aggiunte filtrate sul pattern "verificat" è vuoto.
7. AC-G4: nessuna mia riga nuova introduce blocco VERIFICA/PROVE/... né "verificato X" di prima istanza; ogni asserzione è un richiamo a CAP chiuso PASS con [DOC-INTERNO CAP_*:riga].

---

## Sezione 4 — Misura prima/dopo (greenfield di consolidamento, adattata onestamente)

PRIMA: 6 difetti confermati nei blocchi — gap correttezza-feature (F1, product-relevant), criterio di successo non dichiarato (F2), miscitation del numero 1680 (F3), vincolo encoding mancante (F4), marker esito-verifica backfill assenti (F5), dipendenza FASE-D non enumerata (F6).

DOPO: 6 difetti chiusi, +8 requisiti atomici nuovi tracciati + 1 ancora corretta, conteggi aggiornati:

| Blocco | Prima | Dopo | Delta |
|--------|-------|------|-------|
| B3 | 62 (47 R + 12 CN + 3 NFR) | 63 (48 R + 12 CN + 3 NFR) | +1 R (B3-R-48) |
| B5 | 35 (20 R + 9 CN + 7 NFR) | 35 (invariato) | +0 (solo ancora corretta su B5-CN-05) |
| B6 | 65 (37 R + 24 CN + 4 NFR) | 72 (43 R + 25 CN + 4 NFR) | +6 R (B6-R-38..43) +1 CN (B6-CN-25) |
| B8 | 17 (12 R + 5 CN) | 18 (13 R + 5 CN) | +1 R (B8-R-13) |

Nessuna metrica GA inventata. Edge resta PENDING-empirico.

---

## Sezione 5 — Domande aperte / Criterio di rollback / Blocchi

Blocchi / Domande aperte: NESSUNO. Tutti e 6 i fix chiusi con fonte CAP risolvibile alla riga reale, incluso F4 (fonte CAP_09:117 trovata). Nessun requisito scritto a valle di un blocco aperto -> nessun marcatore [B-N PROVVISORIO] introdotto.

Criterio di rollback: i fix sono additivi (8 requisiti nuovi + 1 ancora) e isolati nei 4 file-blocco. Rollback = git revert del commit [SPEC-FUNZ-01-AUDITFIX-01]; ripristina lo stato pre-AUDITFIX (B3 62, B5 35, B6 65, B8 17) senza toccare CAP/v2/altri blocchi.

---

## Auto-check (richiesti dalla card §5)

- Edge-PENDING preservato: OK. F2 (B3-R-48) e F6 (B8-R-13) restano criterio/dipendenza, mai esito.
- Nessun "verificato X" di prima istanza (AC-G4): OK. Filtro sulle righe aggiunte del diff su pattern "verificat" -> nessuna riga aggiunta lo contiene. Ogni asserzione è richiamo [DOC-INTERNO CAP_*:riga].
- Nessun CAP toccato (freeze G-09): OK. git status docs/methodology_v2/ -> nessun CAP modificato. git diff --stat: solo i 4 file-blocco, nessun CAP_*, nessun SPEC_FUNZ_01.md (v2).
- v2 non toccata: OK. SPEC_FUNZ_01.md non nel diff del commit.
- Floor citazioni 100% / grafia canonica: OK. ogni requisito nuovo ha [DOC-INTERNO CAP_*:riga] risolvibile; grafia canonica; 0 conclusioni wiki-only.

## Tabella verifica AC (card §3-§4)

| AC-ID | OK/PARZIALE/MANCA | Evidenza file:riga |
|-------|-------------------|--------------------|
| F1 — regola consumo per-categoria, CAP_09:185-189 | OK | B6.md §6bis.1 B6-R-38..42; matrice §7.1; conteggio finale |
| F2 — profitto netto = metrica PRIMARIA, criterio non esito, CAP_02_parte_II:411 | OK | B3.md §6.4 B3-R-48; matrice §8.1 |
| F3 — ancora 1680 aggiunta a CAP_09:290, proposizione invariata | OK | B5.md B5-CN-05; matrice §7.1 |
| F4 — vincolo encoding BOM/UTF-8 header CSV, fonte CAP_09:117 | OK | B6.md §6bis.2 B6-CN-25; matrice §7.1 |
| F5 — marker BACKFILL_VERIFIED_T3/BACKFILL_UNVERIFIED + routing gate Cap.60, CAP_10:90 | OK | B6.md §6bis.3 B6-R-43; matrice §7.1 |
| F6 — dipendenza estensione immutabilità CANDLERANGE oltre T+3, PENDING mai risolta, CAP_10:234 | OK | B8.md §2 B8-R-13, §3 PENDING, §4.1 matrice |
| Solo i 4 file-blocco toccati, nessun CAP/v2/altri blocchi | OK | git diff --stat: B3/B5/B6/B8 only |
| Conteggi + matrici aggiornati per blocco toccato | OK | B3 §8.1; B5 §7.1; B6 §7.1 + conteggio; B8 §3 + §4.1 |
| Edge PENDING + no "verificato X" + grafia canonica + floor 100% | OK | auto-check sopra |

---

Documento REPORT AUDITFIX-01 prodotto dallo spec_developer del track Business-spec, sede CLI. CAP riletti token-per-token a HEAD a3dd507. Nessun blocco aperto. Pronto per Review formale piena (spec_reviewer in CLI).
