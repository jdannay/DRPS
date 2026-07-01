from dataclasses import dataclass

@dataclass
class SimulationYear:
    year:int
    beginning_portfolio:float
    income:float
    spending:float
    ending_portfolio:float

class SimulationEngine:
    def __init__(self, household):
        self.household = household

    def simulate_year(self, year:int):
        begin = self.household.portfolio.total
        income = 0.0
        spending = 0.0
        end = begin + income - spending
        return SimulationYear(
            year=year,
            beginning_portfolio=begin,
            income=income,
            spending=spending,
            ending_portfolio=end
        )
