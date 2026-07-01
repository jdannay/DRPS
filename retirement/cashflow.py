from .projection import ProjectionYear
from .portfolio import Portfolio

class CashFlowEngine:
    def __init__(self, assumptions):
        self.assumptions=assumptions

    def run(self):
        hh=self.assumptions["household"]
        portfolio=Portfolio.from_mapping(self.assumptions["portfolio"])
        rows=[]
        for year in range(2026,2061):
            balances=portfolio.snapshot()
            rows.append(
                ProjectionYear(
                    year,
                    year-hh["primary"]["birth_year"],
                    year-hh["spouse"]["birth_year"],
                    balances["taxable"],
                    balances["traditional_ira"],
                    balances["inherited_ira"],
                    balances["roth_ira"]
                )
            )
        return rows
