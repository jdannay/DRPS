from pathlib import Path
from .config import load_assumptions
from .logger import get_logger

class DRPSApplication:
    def __init__(self):
        self.logger = get_logger("DRPS")

    def run(self):
        self.logger.info("Dannay Retirement Planning System v0.3.0")
        config_path = Path("data") / "assumptions.json"
        assumptions = load_assumptions(config_path)

        household = assumptions["household"]
        portfolio = assumptions["portfolio"]

        self.logger.info(
            f'Loaded household: '
            f'{household["primary"]["name"]} & {household["spouse"]["name"]}'
        )
        self.logger.info(
            f'Total investable assets: '
            f'${sum(portfolio.values()):,.0f}'
        )
        self.logger.info("Initialization complete.")
