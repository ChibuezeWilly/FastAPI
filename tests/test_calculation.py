from app.calculation import add, BankAccount
import pytest

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

def test_add():
    print("testing to see if things work out")
    assert add(5, 5) == 10
    
def test_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0    

def test_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_deposit():
    bank_acc = BankAccount(balance=50)
    bank_acc.deposit(50)
    assert bank_acc.balance == 100
    
def test_withdraw():
    bank_acc = BankAccount(balance=50)
    bank_acc.withdraw(10)
    assert bank_acc.balance == 40
    
def test_collect_interest():
    bank_acc = BankAccount(balance=50)
    bank_acc.collect_interest()
    assert round(bank_acc.balance, 6) == 55
    
@pytest.mark.parametrize("deposit, withdraw, expected_balance", [
    (500, 100, 400),
    (400, 400, 0),
    (1000, 50, 950)
])

def test_bank_transactions(zero_bank_account, deposit, withdraw, expected_balance):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw),
    assert zero_bank_account.balance == expected_balance