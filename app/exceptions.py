# app/exceptions.py
from typing import Optional


class BankError(Exception):
    """Lỗi gốc của hệ thống ngân hàng"""

    pass


class InsufficientFundsError(BankError):
    def __init__(self, balance: float, amount: float) -> None:
        self.balance = balance
        self.amount = amount
        super().__init__(f"Số dư không đủ. có: {balance:,.0f}đ, cần: {amount:,.0f}đ")


class InvalidAmountError(BankError):
    def __init__(self, amount: float) -> None:
        self.amount = amount
        super().__init__(f"Số tiền không hợp lệ: {amount}")


class WithdrawLimitError(BankError):
    def __init__(self, used: int, limit: int) -> None:
        self.used = used
        self.limit = limit
        super().__init__(f"Đã rút {used}/{limit} lần trong tháng — hết lượt")
