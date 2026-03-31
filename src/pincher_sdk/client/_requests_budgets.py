from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pincher_sdk import Client

from pincher_sdk.types import Budget, MonthReport
from pincher_sdk.cache import ResourceCacheEntry
from pincher_sdk.endpoints import (
    endpoint_budget,
    endpoint_budgets,
    endpoint_budget_month,
)
from pincher_sdk.payloads import (
    BudgetCreateData,
    BudgetUpdateData,
)


async def budget_create(self: "Client", b_id: str, data: BudgetCreateData):
    endpoint = endpoint_budgets()
    try:
        budget = await self._do_request("POST", endpoint, data._asdict(), self._token)
    except Exception as e:
        raise e
    self.cache.set(ResourceCacheEntry(budget, endpoint), b_id)


async def budget(self: "Client", b_id: str) -> Budget:
    endpoint = endpoint_budget(b_id)
    try:
        budget = await self._do_request("GET", endpoint, None, self._token)
    except Exception as e:
        raise e
    return budget


async def budgets(self: "Client", b_id: str, **kwargs) -> list[Budget]:
    endpoint = endpoint_budgets(**kwargs)
    try:
        budgets = await self._do_request("GET", endpoint, None, self._token)
    except Exception as e:
        raise e
    return budgets.data


async def budget_report(self: "Client", b_id: str, m_id: str) -> MonthReport:
    endpoint = endpoint_budget_month(b_id, m_id)
    try:
        report = await self._do_request("GET", endpoint, None, self._token)
    except Exception as e:
        raise e
    return report


async def budget_update(self: "Client", b_id: str, data: BudgetUpdateData):
    endpoint = endpoint_budget(b_id)
    try:
        await self._do_request("PUT", endpoint, data._asdict(), self._token)
        self.budget(b_id)  # type: ignore
    except Exception as e:
        raise e


async def budget_delete(self: "Client", b_id: str):
    endpoint = endpoint_budget(b_id)
    try:
        await self._do_request("DELETE", endpoint, None, self._token)
        self.cache.delete(b_id)
    except Exception as e:
        raise e
