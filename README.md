# Bank App

Hệ thống quản lý tài khoản ngân hàng — dự án luyện tập OOP Python.

## Tính năng

- Tài khoản cơ bản: nạp, rút, chuyển tiền
- Tài khoản tiết kiệm: giới hạn lần rút, cộng lãi suất
- Tài khoản thanh toán: phí giao dịch mỗi lần rút
- Lịch sử giao dịch chi tiết

## Cài đặt

```bash
git clone git@github.com:username/bank-app.git
cd bank-app
python -m venv venv
source venv/bin/activate
python main.py
```

## Cấu trúc project

```
bank_app/
├── app/
│   ├── models/
│   │   ├── base.py        # BankAccount
│   │   ├── saving.py      # SavingAccount
│   │   └── checking.py    # CheckingAccount
│   ├── exceptions.py
│   └── decorators.py
└── main.py
```
