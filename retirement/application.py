from pathlib import Path
from retirement.config import load_assumptions
from retirement.logger import get_logger
from retirement.cashflow import CashFlowEngine

class DRPSApplication:
    def __init__(self):
        self.logger = get_logger("DRPS")

    def run(self):
        self.logger.info("Dannay Retirement Planning System v0.3.1")

        assumptions = load_assumptions(Path("data") / "assumptions.json")
        engine = CashFlowEngine(assumptions)
        projection = engine.run()

        first = projection[0]

        self.logger.info("")
        self.logger.info("Retirement Projection")
        self.logger.info("---------------------")
        self.logger.info(f"Year: {first.year}")
        self.logger.info(f"Your age: {first.your_age}")
        self.logger.info(f"Spouse age: {first.spouse_age}")
        self.logger.info(f"Portfolio: ${first.total_portfolio:,.0f}")
