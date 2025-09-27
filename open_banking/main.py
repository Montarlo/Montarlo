"""Command line interface for the sample open banking application."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

from .api import OpenBankingAPI
from .providers import JsonFileProvider


def configure_api(data_paths: List[Path]) -> OpenBankingAPI:
    api = OpenBankingAPI()
    for path in data_paths:
        provider_name = path.stem.replace("_", " ").title()
        api.register_provider(JsonFileProvider(provider_name, path))
    return api


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sample Open Banking CLI")
    parser.add_argument(
        "data",
        nargs="+",
        type=Path,
        help="Path(s) to provider JSON definitions",
    )
    parser.add_argument(
        "--provider",
        help="Filter results for a specific provider name",
    )
    parser.add_argument(
        "--format",
        choices=("table", "json"),
        default="table",
        help="Output format",
    )
    return parser


def format_table(api: OpenBankingAPI, provider: str | None) -> str:
    accounts = api.accounts(provider)
    if not accounts:
        return "No accounts found."

    headers = ("Provider", "Account", "Type", "Currency", "Balance", "Available")
    table = [headers]
    for account in accounts:
        table.append(
            (
                account.provider,
                account.name,
                account.type,
                account.currency,
                f"{account.balance:,.2f}",
                f"{account.available_balance():,.2f}",
            )
        )

    col_widths = [max(len(str(row[idx])) for row in table) for idx in range(len(headers))]
    lines = []
    for row in table:
        lines.append(
            " | ".join(str(value).ljust(col_widths[idx]) for idx, value in enumerate(row))
        )
    return "\n".join(lines)


def format_json(api: OpenBankingAPI, provider: str | None) -> str:
    data = api.to_dict()
    if provider:
        data["accounts"] = [account for account in data["accounts"] if account["provider"] == provider]
    return json.dumps(data, indent=2)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    data_paths = [path.expanduser().resolve() for path in args.data]
    missing_files = [str(path) for path in data_paths if not path.exists()]
    if missing_files:
        raise SystemExit(f"Missing provider files: {', '.join(missing_files)}")

    api = configure_api(data_paths)
    if args.format == "table":
        print(format_table(api, args.provider))
    else:
        print(format_json(api, args.provider))


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
