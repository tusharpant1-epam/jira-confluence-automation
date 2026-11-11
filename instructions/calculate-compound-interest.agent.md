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
