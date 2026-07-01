from dataclasses import dataclass

from .portfolio import Portfolio
from .spending import SpendingEngine


@dataclass
class SimulationYear:
    year:int
    beginning_portfolio:float
    investment_returns:float
    dividend_income:float
    pension_income:float
    inherited_ira_withdrawal:float
    spending:float
    advisor_fee:float
    ending_portfolio:float


class SimulationEngine:
    def __init__(self, assumptions, spending_engine=None):
        self.assumptions = assumptions
        self.spending_engine = spending_engine or SpendingEngine()

    def run(self):
        portfolio = Portfolio.from_mapping(self.assumptions["portfolio"])
        rows = []
        for year in range(self.start_year, self.end_year + 1):
            beginning_portfolio = portfolio.total
            before_returns = portfolio.total
            portfolio.apply_returns(self.investment_returns_for(year, portfolio))
            investment_returns = portfolio.total - before_returns

            dividend_income = self.dividend_income_for(year)
            portfolio.deposit(dividend_income)

            pension_income = self.pension_income_for(year)
            portfolio.deposit(pension_income)

            inherited_ira_withdrawal = self.inherited_ira_withdrawal_for(year, portfolio)
            if inherited_ira_withdrawal:
                portfolio.withdraw(
                    inherited_ira_withdrawal,
                    account_order=("inherited_ira",),
                )
                portfolio.deposit(inherited_ira_withdrawal)

            spending = min(self.spending_engine.total_spending(year), portfolio.total)
            if spending:
                portfolio.withdraw(spending)

            advisor_fee = portfolio.apply_advisor_fee(self.advisor_fee_rate_for(year))

            rows.append(
                SimulationYear(
                    year=year,
                    beginning_portfolio=beginning_portfolio,
                    investment_returns=investment_returns,
                    dividend_income=dividend_income,
                    pension_income=pension_income,
                    inherited_ira_withdrawal=inherited_ira_withdrawal,
                    spending=spending,
                    advisor_fee=advisor_fee,
                    ending_portfolio=portfolio.total,
                )
            )
        return rows

    @property
    def start_year(self):
        return self.assumptions.get("simulation", {}).get("start_year", 2026)

    @property
    def end_year(self):
        return self.assumptions.get("simulation", {}).get("end_year", 2060)

    def investment_returns_for(self, year, portfolio):
        expected_returns = self.expected_returns_for(year)
        allocations = self.account_allocations_for(year)
        if expected_returns and allocations:
            return portfolio.weighted_return_rates(expected_returns, allocations)
        return self.value_for_year("investment_returns", year, 0)

    def expected_returns_for(self, year):
        return self.year_config_for("expected_returns", year)

    def account_allocations_for(self, year):
        return self.year_config_for("allocations", year)

    def dividend_income_for(self, year):
        return self.value_for_year("dividend_income", year, 0)

    def pension_income_for(self, year):
        return self.value_for_year("pension_income", year, 0)

    def advisor_fee_rate_for(self, year):
        return self.value_for_year("advisor_fee_rate", year, 0)

    def inherited_ira_withdrawal_for(self, year, portfolio):
        requested = self.value_for_year("inherited_ira_withdrawal", year, 0)
        return min(requested, portfolio.inherited_ira)

    def value_for_year(self, key, year, default):
        value = self.assumptions.get(key, default)
        if isinstance(value, dict):
            return value.get(str(year), value.get(year, value.get("default", default)))
        return value

    def year_config_for(self, key, year):
        value = self.assumptions.get(key, {})
        if isinstance(value, dict) and any(
            year_key in value for year_key in (str(year), year, "default")
        ):
            return self.value_for_year(key, year, {})
        return value
