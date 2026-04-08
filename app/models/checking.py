# app/models/checking.py
from typing import Optional
from app.models.base import BankAccount, Transaction, Amount
from app.exceptions import InvalidAmountError, InsufficientFundsError
from app.decorators import timer


class CheckingAccount(BankAccount):
    def __init__(
        self, owner: str, initial_balance: Amount = 0, fee_per_withdraw: Amount = 5_000
    ) -> None:
        super().__init__(owner, initial_balance)
        self.fee_per_withdraw = fee_per_withdraw

    @timer
    def withdraw(self, amount: Amount, note: Optional[str] = None) -> Amount:
        if amount <= 0:
            raise InvalidAmountError(amount)
        total = amount + self.fee_per_withdraw
        if total > self._balance:
            raise InsufficientFundsError(self._balance, total)

        self._balance -= total
        self._transactions.append(
            Transaction(
                amount, "rút", self._balance, f"phí {self.fee_per_withdraw:,.0f}đ"
            )
        )
        print(
            f"  Rút {amount:,.0f}đ "
            f"+ phí {self.fee_per_withdraw:,.0f}đ. "
            f"Số dư: {self._balance:,.0f}đ"
        )
        return self._balance
