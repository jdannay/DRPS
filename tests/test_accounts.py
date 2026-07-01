from retirement.accounts import InvestmentAccount
def test_withdraw():
    a=InvestmentAccount("Taxable",100)
    a.withdraw(40)
    assert a.balance==60
