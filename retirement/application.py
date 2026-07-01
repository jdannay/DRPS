from pathlib import Path
from .config import load_assumptions
from .logger import get_logger
from .cashflow import CashFlowEngine
from .spending import SpendingEngine
from .events import EventEngine
from .portfolio import Portfolio
from . import __version__

class DRPSApplication:
    def __init__(self):
        self.log=get_logger()

    def run(self):
        a=load_assumptions(Path("data")/"assumptions.json")
        portfolio=Portfolio.from_mapping(a["portfolio"])
        proj=CashFlowEngine(a).run()
        spend=SpendingEngine()
        events=EventEngine()
        self.log.info(f"DRPS v{__version__}")
        self.log.info(f"Starting portfolio: ${portfolio.total:,.0f}")
        self.log.info("Year  Age  Spending     Portfolio    Inheritance")
        self.log.info("------------------------------------------------")
        for r in proj[:5]:
            self.log.info(
                f"{r.year}  {r.your_age:>3}  "
                f"${spend.total_spending(r.year):>10,.0f}  "
                f"${r.total_portfolio:>11,.0f}  "
                f"${events.inheritance(r.year):>10,.0f}"
            )
