from dataclasses import dataclass

@dataclass
class InvestmentAccount:
    name:str
    balance:float
    def deposit(self, amount:float):
        self.balance+=amount
    def withdraw(self, amount:float):
        if amount>self.balance:
            raise ValueError("Insufficient funds")
        self.balance-=amount
