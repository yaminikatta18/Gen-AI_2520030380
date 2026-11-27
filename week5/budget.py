
import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from the week5 folder
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


@dataclass
class FeatureBudget:
    requests_per_day: int
    avg_input_tokens: int
    avg_output_tokens: int
    peak_requests_per_minute: int
    input_price_per_million: float
    output_price_per_million: float
    rpm_limit: int
    tpm_limit: int
    monthly_budget_usd: float
    daily_budget_usd: float
    safety_margin_percent: float

    @classmethod
    def from_env(cls):
        return cls(
            requests_per_day=int(os.getenv("REQUESTS_PER_DAY", 2000)),
            avg_input_tokens=int(os.getenv("AVG_INPUT_TOKENS", 1200)),
            avg_output_tokens=int(os.getenv("AVG_OUTPUT_TOKENS", 300)),
            peak_requests_per_minute=int(
                os.getenv("PEAK_REQUESTS_PER_MINUTE", 30)
            ),
            input_price_per_million=float(
                os.getenv("INPUT_PRICE_PER_MILLION", 0.30)
            ),
            output_price_per_million=float(
                os.getenv("OUTPUT_PRICE_PER_MILLION", 1.20)
            ),
            rpm_limit=int(os.getenv("RPM_LIMIT", 60)),
            tpm_limit=int(os.getenv("TPM_LIMIT", 100000)),
            monthly_budget_usd=float(
                os.getenv("MONTHLY_BUDGET_USD", 50)
            ),
            daily_budget_usd=float(os.getenv("DAILY_BUDGET_USD", 2)),
            safety_margin_percent=float(
                os.getenv("SAFETY_MARGIN_PERCENT", 20)
            )
        )

    def calculate(self):
        if min(
            self.requests_per_day,
            self.avg_input_tokens,
            self.avg_output_tokens,
            self.peak_requests_per_minute,
            self.input_price_per_million,
            self.output_price_per_million,
            self.rpm_limit,
            self.tpm_limit,
            self.monthly_budget_usd,
            self.daily_budget_usd,
            self.safety_margin_percent
        ) < 0:
            raise ValueError("Configuration values cannot be negative.")

        if self.rpm_limit == 0 or self.tpm_limit == 0:
            raise ValueError("Rate limits must be greater than zero.")

        margin = 1 + self.safety_margin_percent / 100

        daily_input_tokens = (
            self.requests_per_day * self.avg_input_tokens
        )
        daily_output_tokens = (
            self.requests_per_day * self.avg_output_tokens
        )
        daily_total_tokens = daily_input_tokens + daily_output_tokens

        daily_input_cost = (
            daily_input_tokens / 1_000_000
        ) * self.input_price_per_million

        daily_output_cost = (
            daily_output_tokens / 1_000_000
        ) * self.output_price_per_million

        daily_cost = daily_input_cost + daily_output_cost
        monthly_cost = daily_cost * 30

        adjusted_rpm = self.peak_requests_per_minute * margin
        adjusted_tpm = (
            self.peak_requests_per_minute
            * (self.avg_input_tokens + self.avg_output_tokens)
            * margin
        )

        return {
            "daily_input_tokens": daily_input_tokens,
            "daily_output_tokens": daily_output_tokens,
            "daily_total_tokens": daily_total_tokens,
            "daily_cost": daily_cost,
            "monthly_cost": monthly_cost,
            "adjusted_rpm": adjusted_rpm,
            "adjusted_tpm": adjusted_tpm,
            "daily_budget_pass": daily_cost <= self.daily_budget_usd,
            "monthly_budget_pass": monthly_cost <= self.monthly_budget_usd,
            "rpm_pass": adjusted_rpm <= self.rpm_limit,
            "tpm_pass": adjusted_tpm <= self.tpm_limit,
        }


def main():
    budget = FeatureBudget.from_env()
    result = budget.calculate()

    print("\n===== TOKEN ECONOMICS BUDGET REPORT =====")
    print(f"Daily Input Tokens : {result['daily_input_tokens']:,}")
    print(f"Daily Output Tokens: {result['daily_output_tokens']:,}")
    print(f"Daily Total Tokens : {result['daily_total_tokens']:,}")
    print(f"Estimated Daily Cost  : ${result['daily_cost']:.2f}")
    print(f"Estimated Monthly Cost: ${result['monthly_cost']:.2f}")
    print(f"Adjusted RPM: {result['adjusted_rpm']:.0f}")
    print(f"Adjusted TPM: {result['adjusted_tpm']:,.0f}")

    print("\n===== BUDGET AND RATE LIMIT CHECKS =====")
    checks = {
        "Daily Budget": result["daily_budget_pass"],
        "Monthly Budget": result["monthly_budget_pass"],
        "RPM Limit": result["rpm_pass"],
        "TPM Limit": result["tpm_pass"],
    }

    for name, passed in checks.items():
        print(f"{name}: {'PASS' if passed else 'FAIL'}")

    if all(checks.values()):
        print("\nRECOMMENDATION: GO - All checks passed.")
    else:
        print("\nRECOMMENDATION: NO-GO - Review failed checks.")


if __name__ == "__main__":
    main()
