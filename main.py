# main.py — chỉ import từ app, không biết cấu trúc bên trong
from app import SavingAccount, CheckingAccount
from app import InsufficientFundsError, WithdrawLimitError


def main() -> None:
    print("=== Tạo tài khoản ===")
    saving = SavingAccount("Nguyễn Minh", 2_000_000, interest_rate=0.06)
    checking = CheckingAccount("Trần Lan", 1_000_000, fee_per_withdraw=10_000)
    print(saving)
    print(checking)

    print("\n=== SavingAccount ===")
    saving.deposit(500_000, note="Lương")
    saving.withdraw(200_000, note="Mua sách")
    saving.withdraw(100_000)
    saving.withdraw(50_000)

    try:
        saving.withdraw(30_000)  # lần thứ 4 → lỗi
    except WithdrawLimitError as e:
        print(f"  Lỗi: {e}")

    saving.add_interest()
    saving.reset_monthly()

    print("\n=== CheckingAccount ===")
    checking.deposit(200_000)
    checking.withdraw(150_000, note="Thanh toán")

    try:
        checking.withdraw(999_000)
    except InsufficientFundsError as e:
        print(f"  Lỗi: {e}")
        print(f"  Thiếu: {e.amount - e.balance:,.0f}đ")

    print("\n=== Chuyển tiền ===")
    saving.transfer(checking, 300_000, note="Trả nợ")

    print("\n=== Lịch sử ===")
    saving.print_history()
    checking.print_history()


if __name__ == "__main__":
    main()
