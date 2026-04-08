# app/models/saving.py
from typing import Optional
from app.models.base import BankAccount, Amount
from app.exceptions import (
    InvalidAmountError,
    InsufficientFundsError,
    WithdrawLimitError,
)
from app.decorators import timer


class SavingAccount(BankAccount):
    def __init__(
        self,
        owner: str,
        initial_balance: Amount = 0,
        interest_rate: float = 0.05,
        withdraw_limit: int = 3,
    ) -> None:
        super().__init__(owner, initial_balance)
        self.interest_rate = interest_rate
        self._withdraw_limit = withdraw_limit
        self._withdraw_count = 0

    @timer
    def withdraw(self, amount: Amount, note: Optional[str] = None) -> Amount:
        if amount <= 0:
            raise InvalidAmountError(amount)
        if self._withdraw_count >= self._withdraw_limit:
            raise WithdrawLimitError(self._withdraw_count, self._withdraw_limit)
        if amount > self._balance:
            raise InsufficientFundsError(self._balance, amount)

        self._balance -= amount
        self._withdraw_count += 1
        self._transactions.append(
            __import__("app.models.base", fromlist=["Transaction"]).Transaction(
                amount, "rút", self._balance, note
            )
        )
        print(
            f"  Rút {amount:,.0f}đ. Số dư: {self._balance:,.0f}đ "
            f"(còn {self._withdraw_limit - self._withdraw_count} lần)"
        )
        return self._balance

    def add_interest(self) -> None:
        from app.models.base import Transaction

        interest = self._balance * self.interest_rate
        self._balance += interest
        self._transactions.append(Transaction(interest, "lãi suất", self._balance))
        print(
            f"  Lãi {self.interest_rate*100:.0f}%: "
            f"+{interest:,.0f}đ → {self._balance:,.0f}đ"
        )

    def reset_monthly(self) -> None:
        self._withdraw_count = 0
        print("  Reset lượt rút tháng mới.")
