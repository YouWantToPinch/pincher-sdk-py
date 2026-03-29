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

default_base_url = "http://localhost:8080"

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


def endpoint_server_readiness() -> str:
    return URL_HEALTH_Z


def endpoint_login() -> str:
    return URL_USER_TOKEN_LOGIN


def endpoint_refresh() -> str:
    return URL_USER_TOKEN_REFRESH


def endpoint_revoke() -> str:
    return URL_USER_TOKEN_REVOKE


def endpoint_users() -> str:
    return URL_USERS


def endpoint_budgets() -> str:
    return URL_BUDGETS


def endpoint_budget(b_id: str) -> str:
    return interp_str_verbs(URL_BUDGET, b_id)


def endpoint_budget_capital(b_id: str) -> str:
    return interp_str_verbs(URL_BUDGET_CAPITAL, b_id)


def endpoint_budget_members(b_id: str) -> str:
    return interp_str_verbs(URL_BUDGET_MEMBERS, b_id)


def endpoint_budget_member(b_id: str, m_id: str) -> str:
    return interp_str_verbs(URL_BUDGET_MEMBER, b_id, m_id)


def endpoint_budget_groups(b_id: str) -> str:
    return interp_str_verbs(URL_BUDGET_GROUPS, b_id)


def endpoint_budget_group(b_id: str, g_id: str) -> str:
    return interp_str_verbs(URL_BUDGET_GROUP, b_id, g_id)


def endpoint_budget_categories(b_id: str) -> str:
    return interp_str_verbs(URL_BUDGET_CATEGORIES, b_id)


def endpoint_budget_category(b_id: str, c_id: str) -> str:
    return interp_str_verbs(URL_BUDGET_CATEGORY, b_id, c_id)


def endpoint_budget_payees(b_id: str) -> str:
    return interp_str_verbs(URL_BUDGET_PAYEES, b_id)


def endpoint_budget_payee(b_id: str, p_id: str) -> str:
    return interp_str_verbs(URL_BUDGET_PAYEE, b_id, p_id)


def endpoint_budget_accounts(b_id: str) -> str:
    return interp_str_verbs(URL_BUDGET_ACCOUNTS, b_id)


def endpoint_budget_account(b_id: str, a_id: str) -> str:
    return interp_str_verbs(URL_BUDGET_ACCOUNT, b_id, a_id)


def endpoint_budget_account_capital(b_id: str, a_id: str) -> str:
    return interp_str_verbs(URL_BUDGET_ACCOUNT_CAPITAL, b_id, a_id)


def endpoint_budget_transactions(b_id: str) -> str:
    return interp_str_verbs(URL_BUDGET_TRANSACTIONS, b_id)


def endpoint_budget_transaction(b_id: str, t_id: str) -> str:
    return interp_str_verbs(URL_BUDGET_TRANSACTION, b_id, t_id)


def endpoint_budget_transactions_details(b_id: str) -> str:
    return interp_str_verbs(URL_BUDGET_TRANSACTIONS_DETAILS, b_id)


def endpoint_budget_transaction_details(b_id: str, t_id: str) -> str:
    return interp_str_verbs(URL_BUDGET_TRANSACTION_DETAILS, b_id, t_id)


def endpoint_budget_transaction_splits(b_id: str, t_id: str) -> str:
    return interp_str_verbs(URL_BUDGET_TRANSACTION_SPLITS, b_id, t_id)


def endpoint_budget_month(b_id: str, m_id: str) -> str:
    return interp_str_verbs(URL_BUDGET_MONTH, b_id, m_id)


def endpoint_budget_month_categories(b_id: str, m_id: str) -> str:
    return interp_str_verbs(URL_BUDGET_MONTH_CATEGORIES, b_id, m_id)


def endpoint_budget_month_category(b_id: str, m_id, c_id: str) -> str:
    return interp_str_verbs(URL_BUDGET_MONTH_CATEGORY, b_id, m_id, c_id)
