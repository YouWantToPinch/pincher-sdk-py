# --------------------------------------------
#  HTTP data that can be sent to the REST API
# --------------------------------------------

# AUTH, USERS


from typing import NamedTuple
from enum import Enum


class UserCreateData(NamedTuple):
    username: str
    password: str


UserLoginData = UserCreateData
UserUpdateData = UserCreateData
UserDeleteData = UserCreateData


class BudgetCreateData(NamedTuple):
    name: str
    notes: str


class BudgetAccountType(Enum):
    ON_BUDGET = "ON_BUDGET"
    OFF_BUDGET = "OFF_BUDGET"


class BudgetAccountCreateData(NamedTuple):
    name: str
    notes: str
    account_type: BudgetAccountType


BudgetAccountUpdateData = BudgetAccountCreateData


class BudgetAccountDeleteData(NamedTuple):
    delete_hard: bool


# GROUPS


class BudgetGroupCreateData(NamedTuple):
    name: str
    notes: str


BudgetGroupUpdateData = BudgetGroupCreateData


# PAYEES


class BudgetPayeeCreateData(NamedTuple):
    name: str
    notes: str


BudgetPayeeUpdateData = BudgetAccountCreateData


class BudgetPayeeDeleteData(NamedTuple):
    new_payee_name: bool


# CATEGORIES


class BudgetCategoryCreateData(NamedTuple):
    name: str
    notes: str
    group_name: str


BudgetCategoryUpdateData = BudgetCategoryCreateData


class BudgetCategoryAssignData(NamedTuple):
    amount: int
    to_category: str
    from_category: str


# TRANSACTIONS


class BudgetTransactionCreateData(NamedTuple):
    account_name: str
    transfer_account_name: str
    transaction_date: str
    payee_name: str
    notes: str
    cleared: bool
    amounts: dict[str, int]


BudgetTransactionUpdateData = BudgetTransactionCreateData
