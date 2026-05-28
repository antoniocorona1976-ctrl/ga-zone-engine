#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

from export_directa_history_parametric import (
    DEFAULT_HOST,
    DEFAULT_INTRADAY_MAX_DAYS,
    DEFAULT_PORT_SETTINGS,
    DEFAULT_TIMEOUT_SECONDS,
    DATE_ONLY_FMT,
    DirectaHistoricalClient,
    build_fetch_plan,
    discover_historical_port,
    end_of_day,
    fetch_direct,
    make_default_output_dir,
    start_of_day,
)

SYMBOLS = [
    "DITAS",
    "DGER",
    "DFRA",
    "DSTX50",
    "MINI6F",
    "FIB6F",
    "MINI6I",
    "FIB6I",
    "EU.DJ50U6",
    "EU.FSXEU6",
    "CM.MESM6",
    "CM.MESU6",
    "CM.MNQM6",
    "CM.MNQU6",
    "CM.MYMM6",
    "CM.MYMU6",
]

INVENTORY_COLUMNS = [
    "snapshot_date",
    "symbol",
    "type",
    "description",
    "market",
    "start_full_5m_to_w",
    "start_daily_oldest",
    "end_date",
    "rows_5m",
    "rows_15m",
    "rows_1h",
    "rows_d",
    "rows_w",
    "folder_path",
]

INVENTORY_PATH = Path(r"C:\directa_history_parametric_export_overlay\exports\directa_history\inventory_indici_futures_daily.csv")
SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[1]
EXPORTS_ROOT = PROJECT_ROOT / "exports" / "directa_history"


@dataclass
class SymbolState:
    symbol: str
    row_template: dict[str, str]
    latest_end_date: date


def load_inventory() -> tuple[list[dict[str, str]], dict[str, SymbolState], set[tuple[str, str]]]:
    rows: list[dict[str, str]] = []
    latest_by_symbol: dict[str, SymbolState] = {}
    existing_pairs: set[tuple[str, str]] = set()

    with INVENTORY_PATH.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != INVENTORY_COLUMNS:
            raise SystemExit(
                f"Header inventario inatteso in {INVENTORY_PATH}: {reader.fieldnames!r}"
            )
        for row in reader:
            rows.append(row)
            symbol = row["symbol"]
            end_date_str = row["end_date"]
            existing_pairs.add((symbol, end_date_str))
            if symbol not in SYMBOLS:
                continue
            end_date_value = date.fromisoformat(end_date_str)
            state = latest_by_symbol.get(symbol)
            if state is None or end_date_value > state.latest_end_date:
                latest_by_symbol[symbol] = SymbolState(
                    symbol=symbol,
                    row_template=dict(row),
                    latest_end_date=end_date_value,
                )

    missing = [symbol for symbol in SYMBOLS if symbol not in latest_by_symbol]
    if missing:
        raise SystemExit(f"Simboli senza cursore iniziale nel CSV: {', '.join(missing)}")

    return rows, latest_by_symbol, existing_pairs


def fetch_available_daily_dates(
    client: DirectaHistoricalClient,
    *,
    symbol: str,
    start_date: date,
    end_date: date,
) -> list[date]:
    if start_date > end_date:
        return []
    daily, _warnings, _commands = fetch_direct(
        client,
        symbol=symbol,
        timeframe="D",
        period_seconds=86400,
        start_dt=start_of_day(start_date),
        end_dt=end_of_day(end_date),
        intraday_max_days=DEFAULT_INTRADAY_MAX_DAYS,
    )
    return sorted({candle.ts.date() for candle in daily if start_date <= candle.ts.date() <= end_date})


def export_single_day(
    client: DirectaHistoricalClient,
    *,
    symbol: str,
    target_date: date,
) -> tuple[Path, dict[str, int]]:
    output_dir = make_default_output_dir(SCRIPT_PATH, symbol=symbol, start_d=target_date, end_d=target_date)
    output_dir.mkdir(parents=True, exist_ok=True)

    commands_before = len(client.command_log)
    results, _warnings = build_fetch_plan(
        client,
        symbol=symbol,
        start_dt=start_of_day(target_date),
        end_dt=end_of_day(target_date),
        intraday_max_days=DEFAULT_INTRADAY_MAX_DAYS,
    )

    ordered_timeframes = ["W", "D", "1H", "15M", "5M"]
    merged: list[dict[str, str | int]] = []
    for timeframe in ordered_timeframes:
        fetch_result = results[timeframe]
        csv_path = output_dir / f"{symbol}_{timeframe}.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "symbol",
                    "timeframe",
                    "timestamp",
                    "date",
                    "time",
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume",
                    "source",
                ],
            )
            writer.writeheader()
            for candle in fetch_result.candles:
                row = candle.csv_row()
                writer.writerow(row)
                merged.append(row)

    merged.sort(key=lambda item: (str(item["timestamp"]), str(item["timeframe"])))
    merged_path = output_dir / f"{symbol}_ALL.csv"
    with merged_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "symbol",
                "timeframe",
                "timestamp",
                "date",
                "time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "source",
            ],
        )
        writer.writeheader()
        writer.writerows(merged)

    manifest_payload = {
        "symbol": symbol,
        "requested_range": {
            "start": target_date.strftime(DATE_ONLY_FMT),
            "end": target_date.strftime(DATE_ONLY_FMT),
        },
        "connection": {
            "host": client.host,
            "historical_port": client.port,
            "account_code": None,
            "port_settings_path": str(DEFAULT_PORT_SETTINGS),
            "banner": client.banner,
        },
        "timeframes": {name: result.summary() for name, result in results.items()},
        "warnings": [],
        "generated_files": [],
        "commands_sent": client.command_log[commands_before:],
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    manifest_path = output_dir / f"{symbol}_manifest.json"
    manifest_path.write_text(json.dumps(manifest_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    counts = {
        "rows_5m": len(results["5M"].candles),
        "rows_15m": len(results["15M"].candles),
        "rows_1h": len(results["1H"].candles),
        "rows_d": len(results["D"].candles),
        "rows_w": len(results["W"].candles),
    }
    return output_dir, counts


def build_inventory_row(
    *,
    template: dict[str, str],
    symbol: str,
    target_date: date,
    folder_path: Path,
    counts: dict[str, int],
) -> dict[str, str]:
    date_str = target_date.strftime(DATE_ONLY_FMT)
    row = {
        "snapshot_date": date_str,
        "symbol": symbol,
        "type": template["type"],
        "description": template["description"],
        "market": template["market"],
        "start_full_5m_to_w": date_str,
        "start_daily_oldest": date_str,
        "end_date": date_str,
        "rows_5m": str(counts["rows_5m"]),
        "rows_15m": str(counts["rows_15m"]),
        "rows_1h": str(counts["rows_1h"]),
        "rows_d": str(counts["rows_d"]),
        "rows_w": str(counts["rows_w"]),
        "folder_path": str(folder_path),
    }
    return row


def append_inventory_rows(rows_to_append: list[dict[str, str]]) -> None:
    if not rows_to_append:
        return
    with INVENTORY_PATH.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=INVENTORY_COLUMNS, quoting=csv.QUOTE_ALL)
        for row in rows_to_append:
            writer.writerow(row)


def main() -> int:
    _inventory_rows, state_by_symbol, existing_pairs = load_inventory()

    historical_port, _account_code, _warnings = discover_historical_port(DEFAULT_PORT_SETTINGS, account_code=None)
    today = date.today()
    pending: list[tuple[date, str, dict[str, str], Path, dict[str, int]]] = []

    with DirectaHistoricalClient(
        host=DEFAULT_HOST,
        port=historical_port,
        timeout_seconds=DEFAULT_TIMEOUT_SECONDS,
        verbose=False,
    ) as client:
        for symbol in SYMBOLS:
            state = state_by_symbol[symbol]
            start_date = state.latest_end_date + timedelta(days=1)
            available_dates = fetch_available_daily_dates(
                client,
                symbol=symbol,
                start_date=start_date,
                end_date=today,
            )
            for target_date in available_dates:
                date_str = target_date.strftime(DATE_ONLY_FMT)
                if (symbol, date_str) in existing_pairs:
                    continue
                folder_path, counts = export_single_day(client, symbol=symbol, target_date=target_date)
                pending.append((target_date, symbol, state.row_template, folder_path, counts))
                existing_pairs.add((symbol, date_str))

    pending.sort(key=lambda item: (item[0], item[1]))
    rows_to_append = [
        build_inventory_row(
            template=template,
            symbol=symbol,
            target_date=target_date,
            folder_path=folder_path,
            counts=counts,
        )
        for target_date, symbol, template, folder_path, counts in pending
    ]
    append_inventory_rows(rows_to_append)

    print(f"APPENDED_ROWS={len(rows_to_append)}")
    for row in rows_to_append:
        print(f"{row['symbol']}\t{row['end_date']}\t{row['folder_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
