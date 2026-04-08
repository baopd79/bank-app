# app/models/base.py
from datetime import datetime
from typing import Optional
from app.exceptions import InsufficientFundsError, InvalidAmountError, BankError
from app.decorators import timer

Amount = float


class Transaction:
    def __init__(
        self,
        amount: Amount,
        transaction_type: str,
        balance_after: Amount,
        note: Optional[str] = None,
    ) -> None:
        self.amount = amount
        self.type = transaction_type
        self.balance_after = balance_after
        self.note = note
        self.created_at = datetime.now().strftime("%H:%M:%S %d/%m/%Y")

    def __repr__(self) -> str:
        dau = "+" if self.type in ("nạp", "nhận") else "-"
        note_str = f"  [{self.note}]" if self.note else ""
        return (
            f"  {self.type.upper():<12}"
            f"{dau}{self.amount:>10,.0f}đ  →  "
            f"số dư: {self.balance_after:,.0f}đ"
            f"{note_str}"
        )


class BankAccount:
    def __init__(self, owner: str, initial_balance: Amount = 0) -> None:
        if initial_balance < 0:
            raise InvalidAmountError(initial_balance)
        self.owner = owner
        self._balance: Amount = initial_balance
        self._transactions: list[Transaction] = []

    @property
    def balance(self) -> Amount:
        return self._balance

    @timer
    def deposit(self, amount: Amount, note: Optional[str] = None) -> Amount:
        if amount <= 0:
            raise InvalidAmountError(amount)
        self._balance += amount
        self._transactions.append(Transaction(amount, "nạp", self._balance, note))
        print(f"  Nạp {amount:,.0f}đ. Số dư: {self._balance:,.0f}đ")
        return self._balance

    @timer
    def withdraw(self, amount: Amount, note: Optional[str] = None) -> Amount:
        if amount <= 0:
            raise InvalidAmountError(amount)
        if amount > self._balance:
            raise InsufficientFundsError(self._balance, amount)
        self._balance -= amount
        self._transactions.append(Transaction(amount, "rút", self._balance, note))
        print(f"  Rút {amount:,.0f}đ. Số dư: {self._balance:,.0f}đ")
        return self._balance

    def transfer(
        self, other: "BankAccount", amount: Amount, note: Optional[str] = None
    ) -> None:
        if self is other:
            raise BankError("Không thể chuyển cho chính mình")
        if amount <= 0:
            raise InvalidAmountError(amount)
        if amount > self._balance:
            raise InsufficientFundsError(self._balance, amount)

        self._balance -= amount
        self._transactions.append(
            Transaction(amount, "chuyển đi", self._balance, note or f"→ {other.owner}")
        )
        other._balance += amount
        other._transactions.append(
            Transaction(amount, "nhận", other._balance, note or f"← {self.owner}")
        )
        print(
            f"  Chuyển {amount:,.0f}đ → '{other.owner}'. "
            f"Số dư còn: {self._balance:,.0f}đ"
        )

    def print_history(self) -> None:
        if not self._transactions:
            print("  Chưa có giao dịch.")
            return
        print(f"\n  --- {self.owner} ---")
        for t in self._transactions:
            print(t)
        print(f"  Số dư: {self._balance:,.0f}đ\n")

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"chủ='{self.owner}', "
            f"số dư={self._balance:,.0f}đ)"
        )
