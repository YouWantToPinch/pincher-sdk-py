from client.types import Account, BudgetResourceKind
from cache import ResourceCacheEntry
from client import Client
from endpoints import endpoint_budget_accounts, endpoint_budget_account
from client.payloads import (
    BudgetAccountCreateData,
    BudgetAccountUpdateData,
    BudgetAccountDeleteData,
)


async def budget_account_create(self: Client, b_id: str, data: BudgetAccountCreateData):
    endpoint = endpoint_budget_accounts(b_id)
    try:
        account = await self._do_request("POST", endpoint, data, self._token)
    except Exception as e:
        raise e
    self.cache.set(ResourceCacheEntry(account, endpoint), b_id)


async def budget_account(self: Client, b_id: str, a_id: str) -> Account:
    endpoint = endpoint_budget_account(b_id, a_id)
    try:
        account = await self._do_request("GET", endpoint, None, self._token)
    except Exception as e:
        raise e
    return account


async def budget_accounts(self: Client, b_id: str, a_id: str) -> list[Account]:
    endpoint = endpoint_budget_accounts(b_id)
    try:
        accounts = await self._do_request("GET", endpoint, None, self._token)
    except Exception as e:
        raise e
    return accounts


async def budget_account_update(
    self: Client, b_id: str, a_id: str, data: BudgetAccountUpdateData
):
    endpoint = endpoint_budget_account(b_id, a_id)
    try:
        await self._do_request("PUT", endpoint, data, self._token)
        self.budget_account(b_id, a_id)  # type: ignore
    except Exception as e:
        raise e


async def budget_account_restore(self: Client, b_id: str, a_id: str):
    endpoint = endpoint_budget_account(b_id, a_id)
    try:
        await self._do_request("PATCH", endpoint, None, self._token)
        self.budget_account(b_id, a_id)  # type: ignore
    except Exception as e:
        raise e


async def budget_account_delete(
    self: Client, b_id: str, a_id: str, data: BudgetAccountDeleteData
):
    endpoint = endpoint_budget_account(b_id, a_id)
    try:
        await self._do_request("DELETE", endpoint, data, self._token)
        if data.delete_hard:
            self.cache.delete(b_id, a_id, BudgetResourceKind.ACCOUNT)
        else:
            self.budget_account(b_id, a_id)  # type: ignore
    except Exception as e:
        raise e
