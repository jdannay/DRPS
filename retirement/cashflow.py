from .projection import ProjectionYear

class CashFlowEngine:
    def __init__(self, assumptions):
        self.assumptions=assumptions

    def run(self):
        hh=self.assumptions["household"]
        p=self.assumptions["portfolio"]
        rows=[]
        for year in range(2026,2061):
            rows.append(
                ProjectionYear(
                    year,
                    year-hh["primary"]["birth_year"],
                    year-hh["spouse"]["birth_year"],
                    p["taxable"],
                    p["traditional_ira"],
                    p["inherited_ira"],
                    p["roth_ira"]
                )
            )
        return rows
