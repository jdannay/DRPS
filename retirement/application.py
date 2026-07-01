from pathlib import Path
from retirement.config import load_assumptions
from retirement.logger import get_logger
from retirement.cashflow import CashFlowEngine
from retirement.spending import SpendingEngine
from retirement.events import EventEngine

class DRPSApplication:
    def __init__(self):
        self.logger = get_logger("DRPS")

    def run(self):
        assumptions = load_assumptions(Path("data")/"assumptions.json")
        projection = CashFlowEngine(assumptions).run()
        spending = SpendingEngine()
        events = EventEngine()

        self.logger.info("Year  Age  Spending     Inheritance")
        self.logger.info("-----------------------------------")
        for row in projection[:5]:
            s = spending.spending_for_year(row.year)
            inh = events.inheritance_for_year(row.year)
            self.logger.info(
                f"{row.year}  {row.your_age:>3}  "
                f"${s.total:>10,.0f}   ${inh:>9,.0f}"
            )
