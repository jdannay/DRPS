from retirement.projection import ProjectionYear

class CashFlowEngine:
    def __init__(self, assumptions):
        self.assumptions = assumptions

    def run(self):
        household = self.assumptions["household"]
        portfolio = self.assumptions["portfolio"]

        results = []

        for year in range(2026, 2061):
            results.append(
                ProjectionYear(
                    year=year,
                    your_age=year-household["primary"]["birth_year"],
                    spouse_age=year-household["spouse"]["birth_year"],
                    taxable=portfolio["taxable"],
                    traditional_ira=portfolio["traditional_ira"],
                    inherited_ira=portfolio["inherited_ira"],
                    roth_ira=portfolio["roth_ira"],
                )
            )

        return results
