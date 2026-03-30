from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pincher_sdk import Client

from pincher_sdk.types import User
from pincher_sdk.cache import ResourceCacheEntry
from pincher_sdk.endpoints import endpoint_login, endpoint_users
from pincher_sdk.payloads import (
    UserCreateData,
    UserUpdateData,
    UserDeleteData,
    UserLoginData,
)


async def user_create(self: "Client", data: UserCreateData):
    endpoint = endpoint_users()
    try:
        budget = await self._do_request("POST", endpoint, data._asdict(), self._token)
    except Exception as e:
        raise e
    self.cache.set(
        ResourceCacheEntry(budget, endpoint),
    )


async def user_login(self: "Client", data: UserLoginData) -> User:
    endpoint = endpoint_login()
    try:
        login = await self._do_request("POST", endpoint, data._asdict(), self._token)
        self._token = login.token
        self._refresh_token = login.refresh_token
    except Exception as e:
        raise e
    return User(login)


async def user_update(self: "Client", data: UserUpdateData):
    endpoint = endpoint_users()
    try:
        await self._do_request("PUT", endpoint, data._asdict(), self._token)
        self.budget_budget()  # type: ignore
    except Exception as e:
        raise e


async def user_delete(self: "Client", data: UserDeleteData):
    endpoint = endpoint_users()
    try:
        await self._do_request("DELETE", endpoint, data._asdict(), self._token)
    except Exception as e:
        raise e
