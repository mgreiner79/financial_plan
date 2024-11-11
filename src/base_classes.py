import random


def generate_random_integer(length):
    if length <= 0:
        raise ValueError("Length must be a positive integer")

    # Calculate the minimum and maximum values for the given length
    min_value = 10 ** (length - 1)  # Smallest number with 'length' digits
    max_value = (10**length) - 1  # Largest number with 'length' digits

    # Generate a random integer between min_value and max_value
    return random.randint(min_value, max_value)


class FinancialModel:
    def __init__(self):
        self.period = None
        self.assets = None
        self.liabilities = None
        self.incomes = None
        self.expenses = None

    def set_period(self, period):
        self.period = period

    def load_data(self, data):

        period = data.get("analysis_period_years", 10)
        self.set_period(period)

        asset_data = data.get("assets", [])
        self.assets, _ = self.initialize_assets(asset_data, [], {})

        liability_data = data.get("liabilities", [])
        self.liabilities, _ = self.initialize_liabilities(liability_data)

        income_data = data.get("incomes", [])
        self.incomes = self.initialize_incomes(income_data)

        expense_data = data.get("expenses", [])
        self.expenses = self.initialize_expenses(expense_data)
        self.expenses = self.generate_interest_expenses_from_liabilities(
            self.liabilities, self.expenses
        )

    def initialize_assets(self, asset_data, assets=None, asset_map=None):
        if assets is None:
            assets = []
        if asset_map is None:
            asset_map = {}
        for data in asset_data:
            asset_id = data.get("id", None)
            asset_type = data.get("type", "generic")
            cost = data.get("cost", None)
            initial_value = data.get("initial_value", None)
            depreciation_rate = data.get("depreciation_rate", 0)
            appreciation_rate = data.get("appreciation_rate", 0)
            value_add_percentage = data.get("value_add_percentage", 1)
            asset = FinancialAsset(
                id=asset_id,
                name=data["name"],
                cost=cost,
                initial_value=initial_value,
                appreciation_rate=appreciation_rate,
                depreciation_rate=depreciation_rate,
                asset_type=asset_type,
                value_add_percentage=value_add_percentage,
            )
            assets.append(asset)
            asset_map[asset_id] = asset
        self.make_parent_child_connections(asset_data, asset_map)
        return assets, asset_map

    def make_parent_child_connections(self, asset_data, asset_map):
        for data in asset_data:
            asset_id = data.get("id", None)
            assert asset_id is not None
            asset = asset_map.get(asset_id, None)
            parent_asset_id = data.get("parent_asset_id", None)
            if parent_asset_id:
                if parent_asset_id in asset_map.keys():
                    parent_asset = asset_map[parent_asset_id]
                    parent_asset.add_child_asset(asset)
                else:
                    raise Exception(f"No asset with ID {parent_asset_id}")

    def initialize_liabilities(
        self, liability_data, liabilities=None, liability_map=None
    ):
        if liabilities is None:
            liabilities = []
        if liability_map is None:
            liability_map = {}
        for data in liability_data:
            liability_id = data.get("id", None)
            liability_type = data.get("type", "generic")
            principal = data["principal"]
            interest_rate = data["interest_rate"]
            term_years = data["term_years"]
            liability = FinancialLiability(
                id=liability_id,
                name=data["name"],
                principal=principal,
                interest_rate=interest_rate,
                term_years=term_years,
                liability_type=liability_type,
            )
            liabilities.append(liability)
            liability_map[liability_id] = liability
        return liabilities, liability_map

    def initialize_incomes(self, income_data, incomes=None):
        if incomes is None:
            incomes = []
        for data in income_data:
            income_id = data.get("id")
            income = Income(
                id=income_id,
                name=data["name"],
                amount_per_period=data["amount_per_period"],
                growth_rate=data.get("growth_rate", 0),
            )
            incomes.append(income)
        return incomes

    def initialize_expenses(self, expense_data, expenses=None):
        if expenses is None:
            expenses = []
        for data in expense_data:
            expense_id = data.get("id")
            expense = Expense(
                id=expense_id,
                name=data["name"],
                amount_per_period=data["amount_per_period"],
                growth_rate=data.get("growth_rate", 0),
            )
            expenses.append(expense)
        return expenses

    def generate_interest_expenses_from_liabilities(self, liabilities, expenses=None):
        if expenses is None:
            expenses = []
        for liability in liabilities:
            expense = Expense(
                id=generate_random_integer(10),
                name=f"{liability.name} Interest Payment",
                growth_rate=0,
                linked_liability=liability,
            )
            expenses.append(expense)
        return expenses

    def calculate_asset_value(self):
        value = 0
        for asset in self.assets:
            value += asset.value_at_period(self.period)
        return value

    def calculate_liability_value(self):
        return sum(
            liability.remaining_balance(self.period) for liability in self.liabilities
        )

    def calculate_income_value(self):
        return sum(income.total_over_periods(self.period) for income in self.incomes)

    def calculate_expense_value(self):
        return sum(expense.total_over_periods(self.period) for expense in self.expenses)

    def calculate_cash_flow(self):
        return self.calculate_income_value() - self.calculate_expense_value()

    def calculate_net_worth(self):
        return (
            self.calculate_cash_flow()
            + self.calculate_asset_value()
            - self.calculate_liability_value()
        )


class FinancialAsset:
    def __init__(
        self,
        id: int,
        name: str,
        appreciation_rate: float = 0,
        depreciation_rate: float = 0,
        asset_type: str = "generic",
        value_add_percentage=1,
        cost: float = None,
        initial_value: float = None,
    ):
        if asset_type == "cash":
            # For cash assets, set appreciation and depreciation rates to zero
            self.appreciation_rate = 0
            self.depreciation_rate = 0
            # Ensure initial_value is provided
            if initial_value is None:
                raise ValueError("Cash assets must have an initial_value")
            self.initial_value = initial_value
        else:
            if cost is None and initial_value is None:
                raise Exception(
                    "You must provide either agrument 'cost' or 'initial_value'"
                )
            if cost is not None and initial_value is not None:
                raise Exception(
                    "You can only provide one of agrument 'cost' or 'initial_value'"
                )
            if cost is not None:
                self.initial_value = cost * value_add_percentage
            else:
                self.initial_value = initial_value
        self.id = id  # Unique identifier
        self.name = name
        self.cost = cost
        self.appreciation_rate = appreciation_rate
        self.depreciation_rate = depreciation_rate
        self.type = asset_type
        self.child_assets = []
        self.parent_asset = None

    def add_child_asset(self, asset):
        self.child_assets += [asset]
        asset._set_parent_asset(self)

    def _set_parent_asset(self, asset):
        self.parent_asset = asset

    def value_at_period(self, periods, parent_id=None):
        """Calculate the value of the asset at a specific period."""
        net_rate = self.appreciation_rate - self.depreciation_rate
        value = self.initial_value * ((1 + net_rate) ** periods)

        for asset in self.child_assets:
            value += asset.value_at_period(periods, parent_id=self.id)
        # If it has a parent asset, but the parent id is not passed
        # as an argument, then retrun zero, so that it is not
        # counted outside of the context of the parent
        if self.parent_asset:
            if parent_id is None:
                return 0
            assert parent_id == self.parent_asset.id
            return value
        else:
            return value


class FinancialLiability:
    def __init__(
        self, id, name, principal, interest_rate, term_years, liability_type="generic"
    ):
        self.id = id  # Unique identifier
        self.name = name
        self.principal = principal
        self.interest_rate = interest_rate
        self.term_years = term_years
        self.type = liability_type

    def monthly_payment(self):
        """Calculate monthly payment using the loan amortization formula."""
        monthly_rate = self.interest_rate / 12
        total_payments = self.term_years * 12
        payment = (
            self.principal
            * monthly_rate
            * (1 + monthly_rate) ** total_payments
            / ((1 + monthly_rate) ** total_payments - 1)
        )
        return payment

    def remaining_balance(self, periods):
        """Calculate remaining balance after a certain number of periods (in years)."""
        monthly_rate = self.interest_rate / 12
        total_payments = self.term_years * 12
        payments_made = periods * 12
        balance = (
            self.principal
            * (
                (1 + monthly_rate) ** total_payments
                - (1 + monthly_rate) ** payments_made
            )
            / ((1 + monthly_rate) ** total_payments - 1)
        )
        return balance

    def amortization_schedule(self, periods):
        """Generate an amortization schedule for the liability over specified periods (years)."""
        monthly_rate = self.interest_rate / 12
        total_payments = int(self.term_years * 12)
        monthly_payment = self.monthly_payment()
        payments = min(int(periods * 12), total_payments)

        schedule = []
        remaining_balance = self.principal

        for _ in range(payments):
            interest_payment = remaining_balance * monthly_rate
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment
            schedule.append(
                {
                    "principal_payment": principal_payment,
                    "interest_payment": interest_payment,
                    "remaining_balance": remaining_balance,
                }
            )
            if remaining_balance <= 0:
                break
        return schedule

    def total_interest_paid(self, periods):
        """Calculate total interest paid over the specified periods (years)."""
        schedule = self.amortization_schedule(periods)
        total_interest = sum(payment["interest_payment"] for payment in schedule)
        return total_interest

    def total_principal_paid(self, periods):
        """Calculate total principal paid over the specified periods (years)."""
        schedule = self.amortization_schedule(periods)
        total_principal = sum(payment["principal_payment"] for payment in schedule)
        return total_principal


class Income:
    def __init__(
        self, id, name, amount_per_period, growth_rate=0, occurrence="recurring"
    ):
        self.id = id  # Unique identifier
        self.name = name
        self.amount_per_period = amount_per_period  # Amount per period (e.g., annual)
        self.growth_rate = growth_rate
        self.occurrence = occurrence

    def total_over_periods(self, periods):
        """Calculate total income over a number of periods considering growth."""
        total = 0
        if self.occurrence == "once":
            total = self.amount_per_period
        else:
            for period in range(periods):
                total += self.amount_per_period * ((1 + self.growth_rate) ** period)
        return total


class Expense:
    def __init__(
        self,
        id,
        name,
        amount_per_period=None,
        growth_rate=0,
        occurrence="recurring",
        occurs_in_period=0,
        linked_liability=None,
    ):
        self.id = id
        self.name = name
        self.amount_per_period = amount_per_period  # Amount per period (e.g., annual)
        self.growth_rate = growth_rate
        self.occurrence = occurrence
        self.occurs_in_period = occurs_in_period
        self.linked_liability = (
            linked_liability  # the linked liability (e.g., mortgage)
        )

    def link_liability(self, liability):
        self.link_liability = liability

    def total_over_periods(self, periods):
        """Calculate total expense over a number of periods considering growth."""
        total = 0
        if self.occurrence == "once":
            if 0 <= self.occurs_in_period < periods:
                total = self.amount_per_period * (
                    (1 + self.growth_rate) ** self.occurs_in_period
                )
        elif self.linked_liability:
            # Check if this expense is from a liability
            amortization_schedule = self.linked_liability.amortization_schedule(periods)
            for period in range(periods):
                if period < len(amortization_schedule):
                    # Check if the linked liability is still active
                    interest_payment = (
                        amortization_schedule[period]["interest_payment"] * 12
                    )  # Annualize
                    total += interest_payment
                else:
                    break
        else:
            for period in range(periods):
                total += self.amount_per_period * ((1 + self.growth_rate) ** period)
        return total
