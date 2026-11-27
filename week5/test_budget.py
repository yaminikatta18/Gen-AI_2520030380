
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from budget import FeatureBudget


class TestFeatureBudget(unittest.TestCase):

    def setUp(self):
        self.budget = FeatureBudget(
            requests_per_day=2000,
            avg_input_tokens=1200,
            avg_output_tokens=300,
            peak_requests_per_minute=30,
            input_price_per_million=0.30,
            output_price_per_million=1.20,
            rpm_limit=60,
            tpm_limit=100000,
            monthly_budget_usd=50,
            daily_budget_usd=2,
            safety_margin_percent=20
        )

    def test_cost_estimation(self):
        result = self.budget.calculate()

        self.assertAlmostEqual(result["daily_cost"], 1.44)
        self.assertAlmostEqual(result["monthly_cost"], 43.20)

    def test_capacity_passes(self):
        result = self.budget.calculate()

        self.assertTrue(result["rpm_pass"])
        self.assertTrue(result["tpm_pass"])

    def test_rpm_limit_fails(self):
        self.budget.peak_requests_per_minute = 100
        result = self.budget.calculate()

        self.assertFalse(result["rpm_pass"])

    def test_monthly_budget_fails(self):
        self.budget.monthly_budget_usd = 10
        result = self.budget.calculate()

        self.assertFalse(result["monthly_budget_pass"])


if __name__ == "__main__":
    unittest.main()
