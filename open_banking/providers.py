"""Provider implementations for the sample open banking application."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Iterable, List, Protocol

from .models import Account, Transaction


class BankingProvider(Protocol):
    """Protocol describing the behaviour of a banking data provider."""

    name: str

    def accounts(self) -> Iterable[Account]:
        """Return the accounts exposed by the provider."""


class JsonFileProvider:
    """Simple provider that loads account data from a JSON file."""

    def __init__(self, name: str, json_path: Path) -> None:
        self.name = name
        self._json_path = json_path
        self._accounts: List[Account] = []

    def accounts(self) -> Iterable[Account]:
        if not self._accounts:
            raw = json.loads(self._json_path.read_text(encoding="utf-8"))
            self._accounts = [self._parse_account(item) for item in raw["accounts"]]
        return list(self._accounts)

    def _parse_account(self, raw: dict) -> Account:
        transactions = [self._parse_transaction(t) for t in raw.get("transactions", [])]
        account = Account(
            id=raw["id"],
            name=raw["name"],
            type=raw.get("type", "unknown"),
            currency=raw.get("currency", "EUR"),
            balance=float(raw.get("balance", 0.0)),
            provider=self.name,
            transactions=transactions,
        )
        return account

    @staticmethod
    def _parse_transaction(raw: dict) -> Transaction:
        return Transaction(
            id=raw["id"],
            description=raw.get("description", ""),
            amount=float(raw.get("amount", 0.0)),
            currency=raw.get("currency", "EUR"),
            booking_date=date.fromisoformat(raw["booking_date"]),
            category=raw.get("category"),
        )

    def export(self) -> dict:
        """Return the provider data as a JSON serialisable dict."""

        return {
            "name": self.name,
            "accounts": [self._account_to_dict(account) for account in self.accounts()],
        }

    @staticmethod
    def _account_to_dict(account: Account) -> dict:
        serialisable = asdict(account)
        for transaction in serialisable["transactions"]:
            transaction["booking_date"] = transaction["booking_date"].isoformat()
        return serialisable


__all__ = ["BankingProvider", "JsonFileProvider"]
