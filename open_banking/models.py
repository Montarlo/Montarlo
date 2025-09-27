"""Data models for the sample open banking application."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional


@dataclass(slots=True)
class Transaction:
    """Represents a single financial transaction."""

    id: str
    description: str
    amount: float
    currency: str
    booking_date: date
    category: Optional[str] = None


@dataclass(slots=True)
class Account:
    """Represents a bank account that can be retrieved via the API."""

    id: str
    name: str
    type: str
    currency: str
    balance: float
    provider: str
    transactions: List[Transaction] = field(default_factory=list)

    def available_balance(self) -> float:
        """Return the current balance including all booked transactions."""

        return self.balance + sum(t.amount for t in self.transactions)
