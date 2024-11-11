import json
import sys
import os

os.chdir(os.getcwd())
from base_classes import FinancialModel
from utils import load_data_from_json


def perform_financial_analysis(data):
    """Perform financial analysis based on the loaded data."""
    analysis_period_years = data.get("analysis_period_years", 10)
    periods = analysis_period_years

    model = FinancialModel()
    model.set_period(periods)
    model.load_data(data)

    # Calculate total assets value at the end of the analysis period
    total_assets_value = model.calculate_asset_value()

    # Calculate total liabilities remaining at the end of the analysis period
    total_liabilities_value = model.calculate_liability_value()

    # Calculate total incomes over the analysis period
    total_incomes = model.calculate_income_value()

    # Calculate total expenses over the analysis period
    total_expenses = model.calculate_expense_value()

    # Calculate net cash flow
    net_cash_flow = model.calculate_cash_flow()

    # Calculate net worth
    net_worth = model.calculate_net_worth()

    # Output the results
    print("Financial Analysis Results:")
    print(f"Total Assets Value: ${total_assets_value:,.2f}")
    print(f"Total Liabilities Value: ${total_liabilities_value:,.2f}")
    print(f"Net Cash Flow over {analysis_period_years} years: ${net_cash_flow:,.2f}")
    print(f"Net Worth: ${net_worth:,.2f}")

    return {
        "total_assets_value": total_assets_value,
        "total_liabilities_value": total_liabilities_value,
        "net_cash_flow": net_cash_flow,
        "net_worth": net_worth,
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python financial_analysis.py data.json")
        sys.exit(1)
    data_file = sys.argv[1]
    data = load_data_from_json(data_file)
    perform_financial_analysis(data)


if __name__ == "__main__":
    main()
