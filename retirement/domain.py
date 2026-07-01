from dataclasses import dataclass

@dataclass
class Person:
    name: str
    birth_year: int

    def age(self, year:int)->int:
        return year - self.birth_year

@dataclass
class Portfolio:
    taxable: float
    traditional_ira: float
    inherited_ira: float
    roth_ira: float

    @property
    def total(self)->float:
        return (
            self.taxable +
            self.traditional_ira +
            self.inherited_ira +
            self.roth_ira
        )

@dataclass
class Household:
    primary: Person
    spouse: Person
    portfolio: Portfolio
