principal = 15_847
annual_rate = 0.0734
months = 8 * 12 + 7

monthly_rate = annual_rate / 12
final_amount = principal * (1 + monthly_rate) ** months
total_interest = final_amount - principal

print(f"Final amount: ${final_amount:,.2f}")
print(f"Total interest: ${total_interest:,.2f}")
