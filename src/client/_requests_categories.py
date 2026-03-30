from client.types import Category, BudgetResourceKind
from cache import ResourceCacheEntry
from client import Client
from endpoints import endpoint_budget_categories, endpoint_budget_category
from client.payloads import (
    BudgetCategoryCreateData,
    BudgetCategoryUpdateData,
)


async def budget_category_create(
    self: Client, b_id: str, data: BudgetCategoryCreateData
):
    endpoint = endpoint_budget_categories(b_id)
    try:
        category = await self._do_request("POST", endpoint, data._asdict(), self._token)
    except Exception as e:
        raise e
    self.cache.set(ResourceCacheEntry(category, endpoint), b_id)


async def budget_category(self: Client, b_id: str, c_id: str) -> Category:
    endpoint = endpoint_budget_category(b_id, c_id)
    try:
        category = await self._do_request("GET", endpoint, None, self._token)
    except Exception as e:
        raise e
    return category


async def budget_categories(self: Client, b_id: str, c_id: str) -> list[Category]:
    endpoint = endpoint_budget_categories(b_id)
    try:
        categories = await self._do_request("GET", endpoint, None, self._token)
    except Exception as e:
        raise e
    return categories.data


async def budget_category_update(
    self: Client, b_id: str, c_id: str, data: BudgetCategoryUpdateData
):
    endpoint = endpoint_budget_category(b_id, c_id)
    try:
        await self._do_request("PUT", endpoint, data._asdict(), self._token)
        self.budget_category(b_id, c_id)  # type: ignore
    except Exception as e:
        raise e


async def budget_category_delete(
    self: Client,
    b_id: str,
    c_id: str,
):
    endpoint = endpoint_budget_category(b_id, c_id)
    try:
        await self._do_request("DELETE", endpoint, None, self._token)
        self.cache.delete(b_id, c_id, BudgetResourceKind.CATEGORY)
    except Exception as e:
        raise e
