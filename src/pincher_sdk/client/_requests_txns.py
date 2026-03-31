from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pincher_sdk import Client

from pincher_sdk.types import Transaction, BudgetResourceKind
from pincher_sdk.cache import ResourceCacheEntry
from pincher_sdk.endpoints import (
    endpoint_budget_transactions,
    endpoint_budget_transaction,
    endpoint_budget_transaction_details,
    endpoint_budget_transactions_details,
)
from pincher_sdk.payloads import (
    BudgetTransactionCreateData,
    BudgetTransactionUpdateData,
)


async def budget_transaction_create(
    self: "Client", b_id: str, data: BudgetTransactionCreateData
):
    endpoint = endpoint_budget_transactions(b_id)
    try:
        transaction = await self._do_request(
            "POST", endpoint, data._asdict(), self._token
        )
        self.cache.set(ResourceCacheEntry(transaction, endpoint), b_id)
        # retrieve & cache the detailed version as well
        self.budget_transaction_details(b_id, str(transaction.id))  # type: ignore
    except Exception as e:
        raise e


async def budget_transaction(self: "Client", b_id: str, t_id: str) -> Transaction:
    endpoint = endpoint_budget_transaction(b_id, t_id)
    try:
        transaction = await self._do_request("GET", endpoint, None, self._token)
    except Exception as e:
        raise e
    return transaction


async def budget_transactions(
    self: "Client", b_id: str, t_id: str, **kwargs
) -> list[Transaction]:
    endpoint = endpoint_budget_transactions(b_id, **kwargs)
    try:
        transactions = await self._do_request("GET", endpoint, None, self._token)
    except Exception as e:
        raise e
    return transactions.data


async def budget_transaction_details(
    self: "Client", b_id: str, t_id: str
) -> Transaction:
    endpoint = endpoint_budget_transaction_details(b_id, t_id)
    try:
        transaction = await self._do_request("GET", endpoint, None, self._token)
    except Exception as e:
        raise e
    return transaction


async def budget_transactions_details(
    self: "Client", b_id: str, t_id: str, **kwargs
) -> list[Transaction]:
    endpoint = endpoint_budget_transactions_details(b_id, **kwargs)
    try:
        transactions = await self._do_request("GET", endpoint, None, self._token)
    except Exception as e:
        raise e
    return transactions.data


async def budget_transaction_update(
    self: "Client", b_id: str, t_id: str, data: BudgetTransactionUpdateData
):
    endpoint = endpoint_budget_transaction(b_id, t_id)
    try:
        await self._do_request("PUT", endpoint, data._asdict(), self._token)
        self.budget_transaction(b_id, t_id)  # type: ignore
        self.budget_transaction_details(b_id, t_id)  # type: ignore
    except Exception as e:
        raise e


async def budget_transaction_delete(
    self: "Client",
    b_id: str,
    t_id: str,
):
    endpoint = endpoint_budget_transaction(b_id, t_id)
    try:
        await self._do_request("DELETE", endpoint, None, self._token)
        self.cache.delete(b_id, t_id, BudgetResourceKind.TRANSACTION)
        self.cache.delete(b_id, t_id, BudgetResourceKind.TRANSACTION_DETAIL)
    except Exception as e:
        raise e
