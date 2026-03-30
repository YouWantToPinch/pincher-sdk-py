from client import Client
from .types import User


async def user_token_refresh(self: Client, with_user: bool = False) -> User | None:
    try:
        if self._refresh_token == "":
            # TODO: log "Client directed to get new access token, but Refresh Token is empty."
            raise Exception("refresh token is empty")
    except Exception as e:
        raise e

    query = "?with-user" if with_user else ""
    endpoint = "/refresh" + query

    try:
        data = await self._do_request("POST", endpoint, {}, self._refresh_token)
    except Exception as e:
        raise e

    self._token = data["access_token"]

    if with_user:
        return User(data)


async def user_token_revoke(self: Client):
    try:
        if self._refresh_token == "":
            # TODO: log "Client directed to get new access token, but Refresh Token is empty."
            raise Exception("refresh token is empty")
    except Exception as e:
        raise e

    endpoint = "/revoke"
    try:
        await self._do_request("POST", endpoint, {}, self._refresh_token)
    except Exception as e:
        raise e

    # Whether or not the server has trouble revoking,
    # we can at least forget it here in client as well.
    self._refresh_token = ""
