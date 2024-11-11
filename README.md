## Description
This is code for simulating your net worth, given input of a list of assets, income, liabilities and expenses.

## How to use
Install the requirements
`pip install -r requirements.txt`

Create a `params.json` file to store the parameters for the assets, income, liabilities and expenses.
Here is an example:
```json
{
    "analysis_period_years": 20,
    "assets": [
        {
            "name": "Savings",
            "type": "cash",
            "id": 21,
            "initial_value": 100000
        },
        {
            "name": "House",
            "id": 0,
            "initial_value": 500000,
            "appreciation_rate": 0.03,
            "type": "property"
        },
        {
            "name": "Kitchen Remodel",
            "type": "renovation",
            "id": 2,
            "cost": 20000,
            "value_add_percentage": 0.75,
            "depreciation_rate": 0.05,
            "parent_asset_id": 0
        },
    ],
    "liabilities": [
      {
                  "name": "Mortgage",
                  "type": "mortgage",
                  "id": 8,
                  "interest_rate": 0.035,
                  "term_years": 30,
                  "principal": 500000,
                  "related_asset_id": 1
              },
      ],
    "incomes": [
        {
            "name": "Salary",
            "id": 9,
            "amount_per_period": 10000,
            "growth_rate": 0.03
        }
    ],
    "expenses": [
        {
            "name": "Groceries",
            "id": 11,
            "amount_per_period": 12000,
            "growth_rate": 0.03
        },
        {
            "name": "Energy",
            "id": 12,
            "amount_per_period": 5000,
            "growth_rate": 0.03
        },
        {
            "name": "Transportation",
            "id": 13,
            "amount_per_period": 2400,
            "growth_rate": 0.03
        },
        {
            "name": "Entertainment",
            "id": 14,
            "amount_per_period": 6000,
            "growth_rate": 0.03
        },
        {
            "name": "Insurance",
            "id": 15,
            "amount_per_period": 1000,
            "growth_rate": 0.03
        },
        {
            "name": "Miscellaneous",
            "id": 16,
            "amount_per_period": 1800,
            "growth_rate": 0.03
        }
    ]
}
```

Make sure you give each entry a unique ID. You do not need to include your mortgage (or any other liability) payments in the expenses. The amount of interest you are paying will automatically be calculated and added to your expenses.
If you have assets that are upgrades to an already existing asset, for example a kitchen renovation on your house, then enter the house's id in the 'parent_asset_id' field. If you dont, these will be considered as separate assets and the total value of your house will not take into account the upgrades.

To run the script type:
`python financial_analysis.py params.json`

