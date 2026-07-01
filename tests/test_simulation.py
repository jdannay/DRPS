import unittest

from retirement.simulation import SimulationEngine


class FixedSpendingEngine:
    def __init__(self, spending_by_year):
        self.spending_by_year = spending_by_year

    def total_spending(self, year):
        return self.spending_by_year.get(year, 0)


class SimulationEngineTest(unittest.TestCase):
    def test_annual_loop_rolls_ending_portfolio_into_next_beginning(self):
        assumptions = {
            "simulation": {"start_year": 2026, "end_year": 2027},
            "portfolio": {
                "taxable": 1000,
                "traditional_ira": 0,
                "inherited_ira": 0,
                "roth_ira": 0,
            },
            "investment_returns": 0.10,
            "dividend_income": 50,
            "pension_income": 25,
            "advisor_fee_rate": 0.01,
        }
        spending_engine = FixedSpendingEngine({2026: 100, 2027: 100})

        rows = SimulationEngine(assumptions, spending_engine).run()

        self.assertAlmostEqual(rows[0].beginning_portfolio, 1000)
        self.assertAlmostEqual(rows[0].investment_returns, 100)
        self.assertAlmostEqual(rows[0].dividend_income, 50)
        self.assertAlmostEqual(rows[0].pension_income, 25)
        self.assertAlmostEqual(rows[0].spending, 100)
        self.assertAlmostEqual(rows[0].advisor_fee, 10.75)
        self.assertAlmostEqual(rows[0].ending_portfolio, 1064.25)
        self.assertAlmostEqual(rows[1].beginning_portfolio, rows[0].ending_portfolio)

    def test_annual_growth_uses_weighted_account_returns(self):
        assumptions = {
            "simulation": {"start_year": 2026, "end_year": 2026},
            "portfolio": {
                "taxable": 1000,
                "traditional_ira": 1000,
                "inherited_ira": 0,
                "roth_ira": 0,
            },
            "expected_returns": {
                "equities": 0.10,
                "fixed_income": 0.04,
                "alternatives": 0.06,
                "cash": 0.01,
            },
            "allocations": {
                "taxable": {"equities": 0.50, "fixed_income": 0.50},
                "traditional_ira": {"fixed_income": 1.00},
                "inherited_ira": {"cash": 1.00},
                "roth_ira": {"equities": 1.00},
            },
        }
        spending_engine = FixedSpendingEngine({2026: 0})

        row = SimulationEngine(assumptions, spending_engine).run()[0]

        self.assertAlmostEqual(row.investment_returns, 110)
        self.assertAlmostEqual(row.ending_portfolio, 2110)

    def test_inherited_ira_withdrawal_happens_before_spending(self):
        assumptions = {
            "simulation": {"start_year": 2026, "end_year": 2026},
            "portfolio": {
                "taxable": 0,
                "traditional_ira": 0,
                "inherited_ira": 500,
                "roth_ira": 0,
            },
            "inherited_ira_withdrawal": 200,
        }
        spending_engine = FixedSpendingEngine({2026: 150})

        row = SimulationEngine(assumptions, spending_engine).run()[0]

        self.assertEqual(row.inherited_ira_withdrawal, 200)
        self.assertEqual(row.spending, 150)
        self.assertEqual(row.ending_portfolio, 350)

    def test_missing_assumptions_default_to_zero(self):
        assumptions = {
            "simulation": {"start_year": 2026, "end_year": 2026},
            "portfolio": {
                "taxable": 100,
                "traditional_ira": 0,
                "inherited_ira": 0,
                "roth_ira": 0,
            },
        }
        spending_engine = FixedSpendingEngine({2026: 0})

        row = SimulationEngine(assumptions, spending_engine).run()[0]

        self.assertEqual(row.investment_returns, 0)
        self.assertEqual(row.dividend_income, 0)
        self.assertEqual(row.pension_income, 0)
        self.assertEqual(row.inherited_ira_withdrawal, 0)
        self.assertEqual(row.advisor_fee, 0)
        self.assertEqual(row.ending_portfolio, 100)
