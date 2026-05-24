READY_FOR_REVIEW

**Task**: CAP-04 v2 rework post-CONDITIONAL + CAP-02 patch4
**Iterazione**: v2 (CAP-04) + Iterazione 4 (CAP-02 mini-patch)
**Commit di consegna**: `6fdb05e` (sopra `7b9faa5 [CAP-04 v2 + CAP-02 patch4] rework post-CONDITIONAL`)
**Pre-consegna checklist**: 8/8 OK

Fix applicati (6 totali):
- NB-1 BUG REALE: criterio temporale unico per p_ref (Cap.16.1 di CAP-04)
- NB-2 BUG REALE: definizione algoritmica formale di oscillazione (Cap.21.2 di CAP-04)
- O-3 / M-12 PROMEMORIA: campi target_2_type e stop_type nel payload formale Cap.6.1 di CAP-02 + riferimenti in Cap.17.4 e Cap.18.1/18.3 di CAP-04
- O-4 / M-13 PROMEMORIA: x^(A_range) feature condizionale, catalogo CAP-03 invariato a 37 (Cap.21.5 di CAP-04)
- O-5 / M-7 PROMEMORIA: assunzione censoring non-informativo formalizzata + Cox-Snell e Schoenfeld stratificato nominati per Parte V (Cap.19.4 di CAP-04)
- O-6 PROMEMORIA: formulazione 80pt trade_range sincronizzata con Cap.5 PI (A_range >= 80 pt) in Cap.6.1 e Cap.8.2 di CAP-02

AC v2 CAP-04: 12 OK / 0 PARZIALE / 0 MANCA su 12 totali
AC I4 CAP-02: 8 OK / 0 PARZIALE / 0 MANCA su 8 totali

Decisioni di design D-v2-1...D-v2-6 ratificate dall'Orchestratore in assenza di Planner attivo, documentate nella sezione "Iterazione 2" di REPORT_CAP_04 con razionali strutturali e note al supervisore. Reviewer e supervisore possono obiettare nel checkpoint successivo.
