from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pincher_sdk import Client

from pincher_sdk.types import Group, BudgetResourceKind
from pincher_sdk.cache import ResourceCacheEntry
from pincher_sdk.endpoints import endpoint_budget_groups, endpoint_budget_group
from ._payloads import (
    BudgetGroupCreateData,
    BudgetGroupUpdateData,
)


async def budget_group_create(self: "Client", b_id: str, data: BudgetGroupCreateData):
    endpoint = endpoint_budget_groups(b_id)
    try:
        group = await self._do_request("POST", endpoint, data._asdict(), self._token)
    except Exception as e:
        raise e
    self.cache.set(ResourceCacheEntry(group, endpoint), b_id)


async def budget_group(self: "Client", b_id: str, g_id: str) -> Group:
    endpoint = endpoint_budget_group(b_id, g_id)
    try:
        group = await self._do_request("GET", endpoint, None, self._token)
    except Exception as e:
        raise e
    return group


async def budget_groups(self: "Client", b_id: str, g_id: str) -> list[Group]:
    endpoint = endpoint_budget_groups(b_id)
    try:
        groups = await self._do_request("GET", endpoint, None, self._token)
    except Exception as e:
        raise e
    return groups.data


async def budget_group_update(
    self: "Client", b_id: str, g_id: str, data: BudgetGroupUpdateData
):
    endpoint = endpoint_budget_group(b_id, g_id)
    try:
        await self._do_request("PUT", endpoint, data._asdict(), self._token)
        self.budget_group(b_id, g_id)  # type: ignore
    except Exception as e:
        raise e


async def budget_group_delete(
    self: "Client",
    b_id: str,
    g_id: str,
):
    endpoint = endpoint_budget_group(b_id, g_id)
    try:
        await self._do_request("DELETE", endpoint, None, self._token)
        self.cache.delete(b_id, g_id, BudgetResourceKind.GROUP)
    except Exception as e:
        raise e
