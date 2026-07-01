from dataclasses import dataclass

@dataclass
class ProjectionYear:
    year: int
    your_age: int
    spouse_age: int

    taxable: float
    traditional_ira: float
    inherited_ira: float
    roth_ira: float

    income: float = 0.0
    expenses: float = 0.0
    taxes: float = 0.0

    @property
    def total_portfolio(self) -> float:
        return (
            self.taxable
            + self.traditional_ira
            + self.inherited_ira
            + self.roth_ira
        )
