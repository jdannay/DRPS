from dataclasses import dataclass


ACCOUNT_NAMES = ("taxable", "traditional_ira", "inherited_ira", "roth_ira")


@dataclass
class Portfolio:
    taxable: float
    traditional_ira: float
    inherited_ira: float
    roth_ira: float

    @classmethod
    def from_mapping(cls, balances):
        return cls(
            taxable=balances["taxable"],
            traditional_ira=balances["traditional_ira"],
            inherited_ira=balances["inherited_ira"],
            roth_ira=balances["roth_ira"],
        )

    @property
    def total(self):
        return (
            self.taxable
            + self.traditional_ira
            + self.inherited_ira
            + self.roth_ira
        )

    def apply_returns(self, rates):
        for account in ACCOUNT_NAMES:
            rate = self._rate_for_account(rates, account)
            setattr(self, account, getattr(self, account) * (1 + rate))
        return self

    def apply_advisor_fee(self, rate):
        if rate < 0:
            raise ValueError("advisor fee rate cannot be negative")
        fee = self.total * rate
        self.apply_returns(-rate)
        return fee

    def withdraw(self, amount, account_order=None):
        if amount < 0:
            raise ValueError("withdrawal amount cannot be negative")
        if amount > self.total:
            raise ValueError("withdrawal exceeds portfolio balance")

        order = account_order or ACCOUNT_NAMES
        available = 0
        for account in order:
            self._validate_account(account)
            available += getattr(self, account)
        if amount > available:
            raise ValueError("withdrawal account order cannot cover amount")

        remaining = amount
        withdrawals = {account: 0 for account in ACCOUNT_NAMES}
        for account in order:
            available = getattr(self, account)
            taken = min(available, remaining)
            setattr(self, account, available - taken)
            withdrawals[account] = taken
            remaining -= taken
            if remaining == 0:
                break
        if remaining > 0:
            raise ValueError("withdrawal account order cannot cover amount")
        return withdrawals

    def deposit(self, amount, account="taxable"):
        if amount < 0:
            raise ValueError("deposit amount cannot be negative")
        self._validate_account(account)
        setattr(self, account, getattr(self, account) + amount)
        return self

    def snapshot(self):
        return {
            "taxable": self.taxable,
            "traditional_ira": self.traditional_ira,
            "inherited_ira": self.inherited_ira,
            "roth_ira": self.roth_ira,
        }

    def _rate_for_account(self, rates, account):
        if isinstance(rates, dict):
            return rates.get(account, 0)
        return rates

    def _validate_account(self, account):
        if account not in ACCOUNT_NAMES:
            raise ValueError(f"unknown portfolio account: {account}")
