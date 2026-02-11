import pandas as pd

def calculate_emi(principal, annual_rate, years):
    monthly_rate = annual_rate / (12 * 100)
    months = years * 12

    emi = (principal * monthly_rate * (1 + monthly_rate)**months) / \
          ((1 + monthly_rate)**months - 1)

    return emi


def generate_schedule(principal, annual_rate, years):
    emi = calculate_emi(principal, annual_rate, years)
    balance = principal
    monthly_rate = annual_rate / (12 * 100)
    months = years * 12

    schedule = []

    for month in range(1, months + 1):
        interest = balance * monthly_rate
        principal_paid = emi - interest
        balance -= principal_paid

        if balance < 0:
            balance = 0

        schedule.append([
            month,
            round(emi, 2),
            round(principal_paid, 2),
            round(interest, 2),
            round(balance, 2)
        ])

    columns = ["Month", "EMI", "Principal_Paid", "Interest_Paid", "Remaining_Balance"]
    df = pd.DataFrame(schedule, columns=columns)

    return df


# ------------------------------
# Multiple Loan Support
# ------------------------------

def main():
    print("🏦 Loan Repayment Calculator")

    num_loans = int(input("Enter number of loans: "))

    for i in range(num_loans):
        print(f"\nLoan {i+1}")

        try:
            principal = float(input("Enter Loan Amount: "))
            rate = float(input("Enter Annual Interest Rate (%): "))
            years = int(input("Enter Loan Tenure (years): "))

            if principal <= 0 or rate <= 0 or years <= 0:
                raise ValueError

        except ValueError:
            print("❌ Invalid input. Please enter positive numbers.")
            continue

        schedule_df = generate_schedule(principal, rate, years)

        print("\n📅 Repayment Schedule:")
        print(schedule_df)

        total_interest = schedule_df["Interest_Paid"].sum()
        total_payment = schedule_df["EMI"].sum()

        print("\n💰 Loan Summary:")
        print("Total Interest Paid:", round(total_interest, 2))
        print("Total Amount Paid:", round(total_payment, 2))


if __name__ == "__main__":
    main()
