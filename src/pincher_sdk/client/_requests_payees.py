from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pincher_sdk import Client

from pincher_sdk.types import Payee, BudgetResourceKind
from pincher_sdk.cache import ResourceCacheEntry
from pincher_sdk.endpoints import endpoint_budget_payees, endpoint_budget_payee
from pincher_sdk.payloads import (
    BudgetPayeeCreateData,
    BudgetPayeeUpdateData,
    BudgetPayeeDeleteData,
)


async def budget_payee_create(self: "Client", b_id: str, data: BudgetPayeeCreateData):
    endpoint = endpoint_budget_payees(b_id)
    try:
        payee = await self._do_request("POST", endpoint, data._asdict(), self._token)
    except Exception as e:
        raise e
    self.cache.set(ResourceCacheEntry(payee, endpoint), b_id)


async def budget_payee(self: "Client", b_id: str, p_id: str) -> Payee:
    endpoint = endpoint_budget_payee(b_id, p_id)
    try:
        payee = await self._do_request("GET", endpoint, None, self._token)
    except Exception as e:
        raise e
    return payee


async def budget_payees(self: "Client", b_id: str, p_id: str) -> list[Payee]:
    endpoint = endpoint_budget_payees(b_id)
    try:
        payees = await self._do_request("GET", endpoint, None, self._token)
    except Exception as e:
        raise e
    return payees.data


async def budget_payee_update(
    self: "Client", b_id: str, p_id: str, data: BudgetPayeeUpdateData
):
    endpoint = endpoint_budget_payee(b_id, p_id)
    try:
        await self._do_request("PUT", endpoint, data._asdict(), self._token)
        self.budget_payee(b_id, p_id)  # type: ignore
    except Exception as e:
        raise e


async def budget_payee_delete(
    self: "Client",
    b_id: str,
    p_id: str,
    data: BudgetPayeeDeleteData,
):
    endpoint = endpoint_budget_payee(b_id, p_id)
    try:
        await self._do_request("DELETE", endpoint, data._asdict(), self._token)
        self.cache.delete(b_id, p_id, BudgetResourceKind.PAYEE)
    except Exception as e:
        raise e
