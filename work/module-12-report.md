# Module 12 Completion Report

## Instruction File
- Filename: calculate-compound-interest.agent.md

````markdown
---
description: Calculate compound interest using the command-line compound interest script.
---

Use the `tools/compound_interest.py` script when asked to calculate a final balance or interest earned for a principal, annual interest rate, compounding frequency, and duration.

Run the script from the workspace root with four positional arguments, in this order:

```bash
python3 tools/compound_interest.py <principal> <annual_rate_percent> <compounds_per_year> <years>
```

- Pass the annual rate as a percentage, such as `7.34` for 7.34%.
- Pass the compounding frequency as a positive integer, such as `12` for monthly compounding.
- Pass the duration in years; for a duration given in years and months, convert it to years (for example, 8 years and 7 months is `8 + 7/12`).
- Preserve the user's stated principal, rate, frequency, and duration. Do not silently substitute assumptions.

For example, to calculate $15,847 at 7.34%, compounded monthly, for 8 years and 7 months:

```bash
python3 tools/compound_interest.py 15847 7.34 12 8.583333333333333
```

Present both values printed by the script: **Final amount** and **Interest earned**. Keep the two-decimal currency formatting, and make clear which figure is the ending balance and which is the interest portion.
````

## Script File
- Filename: compound_interest.py
- Language: Python

````python
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Calculate compound interest."
    )
    parser.add_argument("principal", type=float, help="Initial principal amount")
    parser.add_argument(
        "annual_rate",
        type=float,
        help="Annual interest rate as a percentage (for example, 7.34)",
    )
    parser.add_argument(
        "compounds_per_year",
        type=int,
        help="Number of compounding periods per year",
    )
    parser.add_argument("years", type=float, help="Total investment duration")
    args = parser.parse_args()

    if args.principal < 0:
        parser.error("principal must be non-negative")
    if args.annual_rate < 0:
        parser.error("annual_rate must be non-negative")
    if args.compounds_per_year <= 0:
        parser.error("compounds_per_year must be greater than zero")
    if args.years < 0:
        parser.error("years must be non-negative")

    periodic_rate = args.annual_rate / 100 / args.compounds_per_year
    final_amount = args.principal * (
        1 + periodic_rate
    ) ** (args.compounds_per_year * args.years)
    interest_earned = final_amount - args.principal

    print(f"Final amount: ${final_amount:,.2f}")
    print(f"Interest earned: ${interest_earned:,.2f}")


if __name__ == "__main__":
    main()
````

## Script Execution Output
```text
usage: compound_interest.py [-h]
                            principal annual_rate compounds_per_year years

Calculate compound interest.

positional arguments:
  principal           Initial principal amount
  annual_rate         Annual interest rate as a percentage (for example, 7.34)
  compounds_per_year  Number of compounding periods per year
  years               Total investment duration

optional arguments:
  -h, --help          show this help message and exit
```
