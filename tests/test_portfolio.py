import unittest

from retirement.portfolio import Portfolio


class PortfolioTest(unittest.TestCase):
    def test_portfolio_tracks_total_balance(self):
        portfolio = Portfolio(100, 200, 300, 400)

        self.assertEqual(portfolio.total, 1000)

    def test_apply_returns_accepts_single_rate(self):
        portfolio = Portfolio(100, 200, 300, 400)

        portfolio.apply_returns(0.10)

        self.assertAlmostEqual(portfolio.taxable, 110)
        self.assertAlmostEqual(portfolio.traditional_ira, 220)
        self.assertAlmostEqual(portfolio.inherited_ira, 330)
        self.assertAlmostEqual(portfolio.roth_ira, 440)

    def test_apply_returns_accepts_account_rates(self):
        portfolio = Portfolio(100, 200, 300, 400)

        portfolio.apply_returns({"taxable": 0.10, "roth_ira": 0.25})

        self.assertAlmostEqual(portfolio.taxable, 110)
        self.assertAlmostEqual(portfolio.traditional_ira, 200)
        self.assertAlmostEqual(portfolio.inherited_ira, 300)
        self.assertAlmostEqual(portfolio.roth_ira, 500)

    def test_weighted_return_rates_use_account_allocations(self):
        portfolio = Portfolio(100, 200, 300, 400)
        expected_returns = {
            "equities": 0.10,
            "fixed_income": 0.04,
            "alternatives": 0.06,
            "cash": 0.01,
        }
        allocations = {
            "taxable": {"equities": 0.50, "fixed_income": 0.50},
            "traditional_ira": {"equities": 1.00},
            "inherited_ira": {"cash": 1.00},
            "roth_ira": {"alternatives": 1.00},
        }

        rates = portfolio.weighted_return_rates(expected_returns, allocations)

        self.assertAlmostEqual(rates["taxable"], 0.07)
        self.assertAlmostEqual(rates["traditional_ira"], 0.10)
        self.assertAlmostEqual(rates["inherited_ira"], 0.01)
        self.assertAlmostEqual(rates["roth_ira"], 0.06)

    def test_apply_advisor_fee_reduces_balances_and_returns_fee(self):
        portfolio = Portfolio(100, 200, 300, 400)

        fee = portfolio.apply_advisor_fee(0.01)

        self.assertAlmostEqual(fee, 10)
        self.assertAlmostEqual(portfolio.taxable, 99)
        self.assertAlmostEqual(portfolio.traditional_ira, 198)
        self.assertAlmostEqual(portfolio.inherited_ira, 297)
        self.assertAlmostEqual(portfolio.roth_ira, 396)

    def test_withdraw_uses_default_account_order(self):
        portfolio = Portfolio(100, 200, 300, 400)

        withdrawals = portfolio.withdraw(350)

        self.assertEqual(
            withdrawals,
            {
                "taxable": 100,
                "traditional_ira": 200,
                "inherited_ira": 50,
                "roth_ira": 0,
            },
        )
        self.assertEqual(
            portfolio.snapshot(),
            {
                "taxable": 0,
                "traditional_ira": 0,
                "inherited_ira": 250,
                "roth_ira": 400,
            },
        )

    def test_withdraw_can_use_custom_account_order(self):
        portfolio = Portfolio(100, 200, 300, 400)

        withdrawals = portfolio.withdraw(250, account_order=("roth_ira",))

        self.assertEqual(withdrawals["roth_ira"], 250)
        self.assertEqual(portfolio.roth_ira, 150)
        self.assertEqual(portfolio.total, 750)

    def test_withdraw_does_not_mutate_when_order_cannot_cover_amount(self):
        portfolio = Portfolio(100, 200, 300, 400)

        with self.assertRaises(ValueError):
            portfolio.withdraw(250, account_order=("taxable",))

        self.assertEqual(
            portfolio.snapshot(),
            {
                "taxable": 100,
                "traditional_ira": 200,
                "inherited_ira": 300,
                "roth_ira": 400,
            },
        )

    def test_deposit_adds_to_selected_account(self):
        portfolio = Portfolio(100, 200, 300, 400)

        portfolio.deposit(50, account="roth_ira")

        self.assertEqual(portfolio.roth_ira, 450)
        self.assertEqual(portfolio.total, 1050)

    def test_negative_deposit_is_rejected(self):
        portfolio = Portfolio(100, 200, 300, 400)

        with self.assertRaises(ValueError):
            portfolio.deposit(-1)

    def test_unknown_account_is_rejected(self):
        portfolio = Portfolio(100, 200, 300, 400)

        with self.assertRaises(ValueError):
            portfolio.deposit(50, account="brokerage")
