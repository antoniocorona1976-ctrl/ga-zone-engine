# ISTRUZIONI_M0-T1-REREVIEW-01 — Re-review delta del fix (chiusura #1 + DEC-E)

**Etichetta: NON AUDITATO.** Re-review sul SOLO delta del fix: non si riaudita M0-T1 per intero (già fatto, REVIEW_M0-T1 `225057d`).

---

## REGOLA N.1 — REVIEW SEMPRE SU FILE

**Ogni uscita — completata, STOP, errore, blocco guard — termina scrivendo `Codice/Piano_di_lavoro/Review/REVIEW_M0-T1-REREVIEW-01.md`** (data/ora + verdetto in testa). In chat solo 5 righe.

## USO (file-bus)

File trascinato nella finestra CLI. Primo atto: copialo tu in `Codice/Piano_di_lavoro/Istruzioni/ISTRUZIONI_M0-T1-REREVIEW-01.md`.

---

RUOLO: `prog_reviewer`. Audit ostile del delta. RM-1/RM-2 (path:riga, hash; alternative escluse dove confermi prove). VIETATO: correggere, ripianificare, riaprire assi già chiusi dalla prima review, toccare piano/DECISIONI/spec. Decisioni mancanti → PENDENTE-PLANNER, non le prendi.

## 1. Perimetro del delta

Catena fix: `01c53aa` (DEC-E in DECISIONI.md) → `c78c358` (fixture tracciata) → `e656315` (fix finale) → commit appendice ESITO (dichiarato `5ee357c`). Diff integrale della catena. Contratto: card `Istruzioni/ISTRUZIONI_M0-T1-FIX-01.md` + DEC-E + `Esito/ESITO_M0-T1-FIX-01.md`.

## 2. Assi di audit

**A. Finding #1 chiuso davvero.** `git ls-files` contiene la fixture; `git show --stat c78c358` = SOLO quel path; **rifai tu la prova GC-3** con un TUO worktree da HEAD (soli file tracciati, `pytest` integrale, 9/9) — non fidarti del transcript del developer; worktree rimosso a fine prova. Docstring: le 6 correzioni della tabella ESITO §2 confermate alle righe attuali; grep sui file del task per claim residui falsi ("committat*" e affini) → zero.
**B. DEC-E conforme al decreto.** Confronta implementazione vs testo DEC-E (DECISIONI.md, riga appesa in `01c53aa`, carattere-per-carattere vs card §0-bis): bordi esclusi con conteggio ED elenco; definizione di giorno completo (prima reale 08:00 E ultima 21:59, R-9.3) legittima rispetto alla spec; **gestione interinale delle parzialità INTERNE** (restano in griglia sull'intervallo osservato + report): classificala esplicitamente rispetto a DEC-E ("gestione decisa in M0-T2") — conforme/deviazione, con motivazione. T9 pinna la policy. Numeri riconciliati: 262/211 e 65/43 sui bordi; 745+95=840; 211+745+43=999.
**C. Asserzioni vecchio→nuovo.** Ogni riga della tabella ESITO §4 giustificata; nessun test indebolito di nascosto. In particolare T7: il re-pinning 30319→30389 non perde il finding — la diagnostica sulle barre raw rileva ancora i 3 finding noti (ricontrolla tu con run diretto); T6: riesegui ×2, hash TUO confrontato con `c1d9a8287c111f0b…`.
**D. Perimetro e igiene.** `git show --stat` dei 3 commit: soli path autorizzati dalla card (§0-bis/§1/§4); DEV_STATUS solo append; **finding #4 non toccato**: nella regione `isp_loader.py:211-216` solo commento cambiato, zero logica (diff); nessun bypass guard (add;commit concatenati — dichiara non-verificabile se non ricostruibile); lessico "verific*" nel testo nuovo.
**E. Regressioni.** Suite completa T1–T9 rieseguita ×2 da te nel repo principale: 9/9 entrambe; T4 e gli assi non toccati dal fix invariati.

## 3. Formato findings e verdetto

`RR-F1..n`: **[taxonomy][severità]** problema/conseguenza/impatto + citazioni. Sezione NON VERIFICABILE esplicita. **VERDETTO sul delta: PASS / CONDITIONAL / FAIL** + 3 righe di motivazione. Su PASS dichiara esplicitamente: "il ciclo M0-T1 è chiudibile" (la chiusura formale la ordina il Planner, non farla tu).

## 4. Chiusura

1. Scrivi `Codice/Piano_di_lavoro/Review/REVIEW_M0-T1-REREVIEW-01.md` (Regola n.1).
2. Append a `tasks/DEV_STATUS.md`: `RE-REVIEW M0-T1: <verdetto> — <data>` (mai riscrivere righe).
3. Commit con add espliciti dei soli: `Review/REVIEW_M0-T1-REREVIEW-01.md`, `Istruzioni/ISTRUZIONI_M0-T1-REREVIEW-01.md`, `tasks/DEV_STATUS.md`. Staging estraneo → STOP + REVIEW file. Messaggio: `RE-REVIEW M0-T1: <verdetto>`. Push. Evita "verific*" nel testo nuovo; se `rm_guard` scatta → STOP + REVIEW file, override solo su ok AC.
