from pathlib import Path
from .config import load_assumptions
from .logger import get_logger
from .portfolio import Portfolio
from .simulation import SimulationEngine
from . import __version__

class DRPSApplication:
    def __init__(self):
        self.log=get_logger()

    def run(self):
        a=load_assumptions(Path("data")/"assumptions.json")
        portfolio=Portfolio.from_mapping(a["portfolio"])
        projection=SimulationEngine(a).run()
        self.log.info(f"DRPS v{__version__}")
        self.log.info(f"Starting portfolio: ${portfolio.total:,.0f}")
        self.log.info("Year  Begin       Returns      Income       Spending     Fee        End")
        self.log.info("--------------------------------------------------------------------------")
        for r in projection[:5]:
            income = r.dividend_income + r.pension_income
            self.log.info(
                f"{r.year}  "
                f"${r.beginning_portfolio:>10,.0f}  "
                f"${r.investment_returns:>10,.0f}  "
                f"${income:>10,.0f}  "
                f"${r.spending:>10,.0f}  "
                f"${r.advisor_fee:>8,.0f}  "
                f"${r.ending_portfolio:>10,.0f}"
            )
