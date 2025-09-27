"""Facade for interacting with multiple open banking providers."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict
from typing import Dict, Iterable, List, Sequence

from .models import Account
from .providers import BankingProvider


class OpenBankingAPI:
    """Simple orchestrator that aggregates accounts from multiple providers."""

    def __init__(self) -> None:
        self._providers: Dict[str, BankingProvider] = {}

    def register_provider(self, provider: BankingProvider) -> None:
        """Register a provider by its name."""

        if provider.name in self._providers:
            raise ValueError(f"Provider '{provider.name}' already registered")
        self._providers[provider.name] = provider

    @property
    def providers(self) -> Sequence[str]:
        """Return the list of registered provider names."""

        return tuple(self._providers.keys())

    def accounts(self, provider: str | None = None) -> List[Account]:
        """Return accounts, optionally filtered by provider name."""

        providers: Iterable[BankingProvider]
        if provider:
            try:
                providers = (self._providers[provider],)
            except KeyError as exc:  # pragma: no cover - defensive branch
                raise KeyError(f"Unknown provider '{provider}'") from exc
        else:
            providers = self._providers.values()

        accounts: List[Account] = []
        for item in providers:
            accounts.extend(item.accounts())
        return accounts

    def aggregate_balances(self) -> Dict[str, float]:
        """Return the total balance per currency across all providers."""

        totals: Dict[str, float] = defaultdict(float)
        for account in self.accounts():
            totals[account.currency] += account.available_balance()
        return dict(totals)

    def to_dict(self) -> dict:
        """Return a serialisable representation of all accounts."""

        return {
            "providers": list(self.providers),
            "accounts": [self._account_to_dict(account) for account in self.accounts()],
            "balances": self.aggregate_balances(),
        }

    @staticmethod
    def _account_to_dict(account: Account) -> dict:
        serialisable = asdict(account)
        serialisable["available_balance"] = account.available_balance()
        serialisable["transactions"] = [
            {**tx, "booking_date": tx["booking_date"].isoformat()}
            for tx in serialisable["transactions"]
        ]
        return serialisable


__all__ = ["OpenBankingAPI"]
