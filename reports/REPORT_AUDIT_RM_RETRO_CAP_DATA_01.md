# REPORT RIDOTTO — Rework AUDIT-RM-RETRO CAP-DATA-01 (Iter.2)

**Task**: rework dei 7 finding approvati dalla Review v1 (reviews/REVIEW_CAP_DATA_01_RM_RETRO_review.md, commit 8e0e334, CONDITIONAL) — decisione supervisore 2026-05-29 (ACTIVE_TASK.md:380-408): tutti i 7 finding a Developer (2 BUG REALI + 5 MIGLIORA PROCESSO).
**Perimetro toccato**: SOLO C (scripts/probe_dapi.py) e D (tasks/HANDOFF_PROBE_DAPI_20260528.md). NON toccati A, B, né file fuori perimetro.
**Stato**: COMPLETATO. Empirico CLI ESEGUITO (DGo+Darwin aperti).

## 1. Cosa è stato modificato
- C: docstring (righe 7-113) riscritta con etichette RM-3, blocchi 4-righe RM-1 per W4/W6, etichette [CODICE-ESISTENTE] per W2/W3, annotazione W9, allineamento banner W8. Decoder parse_line (164-252) NON modificato (già corretto, schema C;L;H;O;V coerente col canonico :477).
- D: §3.2 etichetta [CODICE-ESISTENTE r.228-230]; §3.3 [CODICE-ESISTENTE r.245]; §3.4 blocco 4-righe RM-1 + tabella empirica, tabella originale conservata/etichettata "superata"; §3.5 etichette per livello; §3.6 blocco 4-righe RM-1 + tabella 3 cicli, testo originale conservato/etichettato "superato". Vecchio testo mai cancellato.

## 2. Mappatura finding → patch
| # | Finding | File:linea | Esito |
| 1 W4 | semantica codici errore | C :32-60; D §3.4 | Chiuso [PROVA-EMPIRICA 2026-05-29]: 1004/1007/1017 disambiguati; 1015+1003 nuovi; 1030 non riprodotto → parziale + Empirico-CLI |
| 2 W6 | cooldown 30s/14ª | C :74-87; D §3.6 | Chiuso [PROVA-EMPIRICA]: 75 conn ~1Hz, nessun cooldown → 14/30s refutate come costanti; parziale + Empirico-CLI |
| 3 W2/W3 | END CANDLES/CANDLERANGE | C :22-30; D §3.2-3.3 | Chiuso: [CODICE-ESISTENTE r.228-230/r.245] (grep verificato) |
| 4 W9 | ticker Eurex/CME | C :66-72 | Chiuso: solo IDEM testato; Eurex/CME [WIKI-HINT] → Empirico-CLI/Parte 9 |
| 5 W8 | banner docstring vs decoder | C :102-110 | Chiuso: docstring allineata a match prefisso DARWIN_STATUS; banner reale blen=142 |
| 6 RM-3 | etichette fonte | C, D | Chiuso |
| 7 RM-1 | formato 4-righe | C, D | Chiuso (#1/#2 + dove pertinente) |

Coerenza C↔D: schema CANDLE, codici errore e cooldown riportano le stesse conclusioni in C e D. Nessuna divergenza non etichettata.

## 3. Esito empirico CLI
ESEGUITO. DGo aperta (banner reale catturato, non banner=''+reset). Dump gitignored: probe_out/w4_errcodes_20260529.json, probe_out/w6_cooldown_20260529.json.
- W4: 1004=comando ignoto (2 porte); 1007=ticker inesistente (2 porte); 1017=sintassi strutturale; 1015=data invalida (NUOVO); 1003=comando storico su porta realtime (NUOVO); 1030 non riprodotto.
- W6: nessun cooldown su 75 connessioni ~1Hz; "14" refutata come costante.
- W8: banner reale ha campi extra oltre ;CONN_OK;TRUE; decoder prefisso-match corretto.
- W5 bonus: F=Giugno confermato live (SUB FIB6F → ANAG ISIN IT0024209022 GIU26).

Empirico-CLI residua: W4/1030 (ticker gated), W6 (burst alta-freq/mercato aperto), W5 (I=Set, Mar/Dic), W9 (Eurex/CME).

## 4. Verifica working tree
Solo C, D (+ report) nel commit; A/B/REPORT_CAP_08.md non modificati; .claude/settings.json e scheduled_tasks.lock esclusi; probe_out/ gitignored.

## 5. Verifica push
Commit e444c33 ([AUDIT-RETRO] patch C+D) + 34e233f (DEV_STATUS) su origin/main. Nessun "ahead of origin/main". Questo report committato in commit separato successivo.

## Self-review RM-1..RM-3 (RM-4 opzione A)

VERIFICA: semantica codici errore DAPI 1004/1007/1017/1015/1003.
PROVE: [PROVA-EMPIRICA 2026-05-29] probe w4_errcodes (DGo aperta), trigger+righe ERR registrate in probe_out/w4_errcodes_20260529.json (campione inlinato in D §3.4 e C).
ALTERNATIVE ESCLUSE: "1017 ampio" escluso (data invalida→1015); "1004 solo 10001" escluso (HELP→1004 su 10003); "1007 solo storico" escluso (SUB ZZZNOPE/10001→1007).
ALTERNATIVE NON ESCLUSE: semantica 1030 (non riprodotto); codici fuori dal set trigger. Dichiarati parziali.

VERIFICA: assenza cooldown nel regime testato (W6).
PROVE: [PROVA-EMPIRICA 2026-05-29] probe w6_cooldown, 3×25 conn open/close ~1Hz su 10003, tutte OK (onset_connection: null).
ALTERNATIVE ESCLUSE: "soglia hard 14" refutata (25 consecutive OK × 3 cicli).
ALTERNATIVE NON ESCLUSE: rate-limit burst >>1Hz o mercato aperto. Parziale → Empirico-CLI.

VERIFICA: decoder probe_dapi.py:188-204 coerente con canonico :477.
PROVE: lettura statica; mapping p[4]→close(UFF)/p[5]→low(MIN)/p[6]→high(MAX)/p[7]→open(APE)/p[8]→volume in entrambi.
ALTERNATIVE ESCLUSE: ordine 5 campi, mapping nome→OHLC, indice colonna — cercate ed escluse.
ALTERNATIVE NON ESCLUSE: nessuna (lettura statica). Decoder NON modificato nel rework.

Grep RM-2 eseguito (tool Grep su export_directa_history_parametric.py, pattern CANDLERANGE|END CANDLES|UFF|APE|is_error_line|DEFAULT_INTRADAY_MAX_DAYS):
- :477 commento UFF,MIN,MAX,APE => close,low,high,open (schema canonico)
- :229 CANDLERANGE {symbol} {start} {end} {period_seconds} (period ultimo) — etichetta r.228-230 (f-string ~228-230)
- :245/:282-285/:437 marker END CANDLES
- :417 is_error_line (string-match generico, NON decodifica codici numerici → la semantica numerica non ha supporto di produzione, andava disambiguata empiricamente)
- :61 DEFAULT_INTRADAY_MAX_DAYS=100 (corrobora W7, non toccato)
Nessun decoder DAPI aggiuntivo oltre i due noti.

Fonti RM-3: wiki Directa O;H;L;C [WIKI-HINT, smentito]; schema/codici/cooldown/banner [PROVA-EMPIRICA 2026-05-29]+[CODICE-ESISTENTE]; I=Settembre [DOC-INTERNO App. B.2]; Eurex/CME [WIKI-HINT, da verificare]. Nessuna conclusione si appoggia solo a livello 4.

Assunzioni non testate: schema CANDLE C;L;H;O;V assunto per mandato del task (M-1, [PROVA-EMPIRICA V-1]); dump prodotti contro DGo reale (banner reale catturato indipendentemente).
