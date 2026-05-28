PROGRAMMA PARAMETRICO DIRETTA - EXPORT SERIE STORICHE

Scopo
-----
Questa versione usa SEMPRE lo stesso programma Python, ma rende modificabili
prima dell'esecuzione i parametri principali da un file JSON dedicato.

File da usare
-------------
1) export_directa_history_parametric.py
2) directa_history_export_config.json
3) run_export_directa_history_parametric.cmd

Cosa devi modificare ogni volta
-------------------------------
Apri il file:

    scripts\directa_history_export_config.json

e modifica almeno queste 3 chiavi:

    "symbol": "MINI5L",
    "start": "2025-06-25",
    "end": "2025-12-19"

Esempi:
- per MINI6C:
    "symbol": "MINI6C"

- per range diverso:
    "start": "2025-09-23"
    "end": "2026-03-13"

Esecuzione
----------
Da root progetto:

    python scripts\export_directa_history_parametric.py

oppure:

    scripts\run_export_directa_history_parametric.cmd

Output
------
Se non imposti "output_dir", il programma scrive qui:

    exports\directa_history\<SYMBOL>_<YYYYMMDD>_<YYYYMMDD>\

Per esempio:

    exports\directa_history\MINI5L_20250625_20251219\

File generati
-------------
- <SYMBOL>_W.csv
- <SYMBOL>_D.csv
- <SYMBOL>_1H.csv
- <SYMBOL>_15M.csv
- <SYMBOL>_5M.csv
- <SYMBOL>_ALL.csv
- <SYMBOL>_manifest.json

Note utili
----------
- historical_port:
  lascia null per far leggere automaticamente la porta da APIPortSettings.txt

- account_code:
  lascia null se vuoi usare la prima utenza trovata, oppure imposta il codice conto

- delimiter:
  usa "," oppure ";" se vuoi una apertura più comoda in Excel IT

Override rapidi da riga comando
-------------------------------
Puoi anche lasciare invariato il JSON e lanciare così:

    python scripts\export_directa_history_parametric.py --symbol MINI6C --start 2025-09-23 --end 2026-03-13

Priorità parametri
------------------
1) argomenti CLI
2) file JSON
3) default integrati nel programma
