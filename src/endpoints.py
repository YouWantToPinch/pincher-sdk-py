from src.formatting_verbs import interp_str_verbs

"""
	This file contains all the endpoints used in this library for the Pincher API.
	The naming scheme of the constants and methods has rules:

	Constants:
	 - Prefix with "URL"
	 - Follow a hierarchical structure that build on top of each other
	 - Use plural/singular forms to somewhat reflect the relationship between resources;
		- For example, "EndpointChannelAckMessage" relates to a single Channel and a single Message object

	deftions:
	 - Prefix with "Endpoint"
	 - Used to generate a URL for a specific resource
	 - Follow the same hierarchical structure as the constants
"""

# These base URLs are used by the Client's _do_request method

defaultBaseURL = "http://localhost:8080"

S_VERB = "/%s"

URL_HEALTH_Z = "/healthz"

URL_ADMIN = "/admin"
URL_ADMIN_USERS = URL_ADMIN + "/users"
URL_ADMIN_USERS_COUNT = URL_ADMIN_USERS + "/count"

URL_USER_TOKEN_LOGIN = "/login"
URL_USER_TOKEN_REFRESH = "/refresh"
URL_USER_TOKEN_REVOKE = "/revoke"

URL_USERS = "/users"

URL_BUDGETS = "/budgets"
URL_BUDGET = URL_BUDGETS + S_VERB
URL_BUDGET_CAPITAL = URL_BUDGET + "/capital"
URL_BUDGET_MEMBERS = URL_BUDGET + "/members"
URL_BUDGET_MEMBER = URL_BUDGET_MEMBERS + S_VERB
URL_BUDGET_GROUPS = URL_BUDGET + "/groups"
URL_BUDGET_GROUP = URL_BUDGET_GROUPS + S_VERB
URL_BUDGET_CATEGORIES = URL_BUDGET + "/categories"
URL_BUDGET_CATEGORY = URL_BUDGET_CATEGORIES + S_VERB
URL_BUDGET_PAYEES = URL_BUDGET + "/payees"
URL_BUDGET_PAYEE = URL_BUDGET_PAYEES + S_VERB
URL_BUDGET_ACCOUNTS = URL_BUDGET + "/accounts"
URL_BUDGET_ACCOUNT = URL_BUDGET_ACCOUNTS + S_VERB
URL_BUDGET_ACCOUNT_CAPITAL = URL_BUDGET_ACCOUNT + "/capital"
URL_BUDGET_TRANSACTIONS = URL_BUDGET + "/transactions"
URL_BUDGET_TRANSACTIONS_DETAILS = URL_BUDGET_TRANSACTIONS + "/details"
URL_BUDGET_TRANSACTION = URL_BUDGET_TRANSACTIONS + S_VERB
URL_BUDGET_TRANSACTION_DETAILS = URL_BUDGET_TRANSACTION + "/details"
URL_BUDGET_TRANSACTION_SPLITS = URL_BUDGET_TRANSACTION + "/splits"
URL_BUDGET_MONTHS = URL_BUDGET + "/months"
URL_BUDGET_MONTH = URL_BUDGET_MONTHS + S_VERB
URL_BUDGET_MONTH_CATEGORIES = URL_BUDGET_MONTH + "/categories"
URL_BUDGET_MONTH_CATEGORY = URL_BUDGET_MONTH_CATEGORIES + S_VERB


def EndpointServerReadiness() -> str:
    return URL_HEALTH_Z


def EndpointLogin() -> str:
    return URL_USER_TOKEN_LOGIN


def EndpointRefresh() -> str:
    return URL_USER_TOKEN_REFRESH


def EndpointRevoke() -> str:
    return URL_USER_TOKEN_REVOKE


def EndpointUsers() -> str:
    return URL_USERS


def EndpointBudgets() -> str:
    return URL_BUDGETS


def EndpointBudget(bID: str) -> str:
    return interp_str_verbs(URL_BUDGET, bID)


def EndpointBudgetCapital(bID: str) -> str:
    return interp_str_verbs(URL_BUDGET_CAPITAL, bID)


def EndpointBudgetMembers(bID: str) -> str:
    return interp_str_verbs(URL_BUDGET_MEMBERS, bID)


def EndpointBudgetMember(bID: str, mID: str) -> str:
    return interp_str_verbs(URL_BUDGET_MEMBER, bID, mID)


def EndpointBudgetGroups(bID: str) -> str:
    return interp_str_verbs(URL_BUDGET_GROUPS, bID)


def EndpointBudgetGroup(bID: str, gID: str) -> str:
    return interp_str_verbs(URL_BUDGET_GROUP, bID, gID)


def EndpointBudgetCategories(bID: str) -> str:
    return interp_str_verbs(URL_BUDGET_CATEGORIES, bID)


def EndpointBudgetCategory(bID: str, cID: str) -> str:
    return interp_str_verbs(URL_BUDGET_CATEGORY, bID, cID)


def EndpointBudgetPayees(bID: str) -> str:
    return interp_str_verbs(URL_BUDGET_PAYEES, bID)


def EndpointBudgetPayee(bID: str, pID: str) -> str:
    return interp_str_verbs(URL_BUDGET_PAYEE, bID, pID)


def EndpointBudgetAccounts(bID: str) -> str:
    return interp_str_verbs(URL_BUDGET_ACCOUNTS, bID)


def EndpointBudgetAccount(bID: str, aID: str) -> str:
    return interp_str_verbs(URL_BUDGET_ACCOUNT, bID, aID)


def EndpointBudgetAccountCapital(bID: str, aID: str) -> str:
    return interp_str_verbs(URL_BUDGET_ACCOUNT_CAPITAL, bID, aID)


def EndpointBudgetTransactions(bID: str) -> str:
    return interp_str_verbs(URL_BUDGET_TRANSACTIONS, bID)


def EndpointBudgetTransaction(bID: str, tID: str) -> str:
    return interp_str_verbs(URL_BUDGET_TRANSACTION, bID, tID)


def EndpointBudgetTransactionsDetails(bID: str) -> str:
    return interp_str_verbs(URL_BUDGET_TRANSACTIONS_DETAILS, bID)


def EndpointBudgetTransactionDetails(bID: str, tID: str) -> str:
    return interp_str_verbs(URL_BUDGET_TRANSACTION_DETAILS, bID, tID)


def EndpointBudgetTransactionSplits(bID: str, tID: str) -> str:
    return interp_str_verbs(URL_BUDGET_TRANSACTION_SPLITS, bID, tID)


def EndpointBudgetMonth(bID: str, mID: str) -> str:
    return interp_str_verbs(URL_BUDGET_MONTH, bID, mID)


def EndpointBudgetMonthCategories(bID: str, mID: str) -> str:
    return interp_str_verbs(URL_BUDGET_MONTH_CATEGORIES, bID, mID)


def EndpointBudgetMonthCategory(bID: str, mID, cID: str) -> str:
    return interp_str_verbs(URL_BUDGET_MONTH_CATEGORY, bID, mID, cID)
