import unittest

from retirement.cashflow import CashFlowEngine


class CashFlowEngineTest(unittest.TestCase):
    def test_cashflow_uses_portfolio_balances_from_assumptions(self):
        assumptions = {
            "household": {
                "primary": {"birth_year": 1960},
                "spouse": {"birth_year": 1963},
            },
            "portfolio": {
                "taxable": 100,
                "traditional_ira": 200,
                "inherited_ira": 300,
                "roth_ira": 400,
            },
        }

        first_year = CashFlowEngine(assumptions).run()[0]

        self.assertEqual(first_year.taxable, 100)
        self.assertEqual(first_year.traditional_ira, 200)
        self.assertEqual(first_year.inherited_ira, 300)
        self.assertEqual(first_year.roth_ira, 400)
        self.assertEqual(first_year.total_portfolio, 1000)
