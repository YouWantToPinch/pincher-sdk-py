from pincher_sdk.endpoints import default_base_url
from ._helpers import (
    validate_base_url,
    check_token_expired,
    same_hostname,
)
from pincher_sdk.cache import Cache
from typing import Any
import httpx
import json


class Client(httpx.AsyncClient):
    def __init__(
        self,
        cache: Cache,
        base_url: str = default_base_url,
        auto_refresh: bool = True,
        timeout: int = 10,
    ) -> None:
        super().__init__(base_url=base_url)

        self.cache: Cache = cache
        self._base_url: str = ""
        self._parsed_base_url: httpx.URL | None = None
        self._token: str = ""
        self._refresh_token: str = ""
        self._auto_refresh: bool = auto_refresh
        self.timeout: float = timeout

        try:
            self.set_base_url(base_url)
        except Exception as e:
            raise e

    # import methods from organized modules
    from ._requests_accounts import (
        budget_account_create,
        budget_account,
        budget_accounts,
        budget_account_update,
        budget_account_restore,
        budget_account_delete,
    )
    from ._requests_auth import user_token_refresh, user_token_revoke
    from ._requests_budgets import (
        budget_create,
        budget,
        budgets,
        budget_update,
        budget_delete,
    )
    from ._requests_categories import (
        budget_category_create,
        budget_category,
        budget_categories,
        budget_category_update,
        budget_category_delete,
    )
    from ._requests_groups import (
        budget_group_create,
        budget_group,
        budget_groups,
        budget_group_update,
        budget_group_delete,
    )
    from ._requests_payees import (
        budget_payee_create,
        budget_payee,
        budget_payees,
        budget_payee_update,
        budget_payee_delete,
    )
    from ._requests_txns import (
        budget_transaction_create,
        budget_transaction,
        budget_transactions,
        budget_transaction_details,
        budget_transactions_details,
        budget_transaction_update,
        budget_transaction_delete,
    )
    from ._requests_users import (
        user_create,
        user_login,
        user_update,
        user_delete,
    )
    from ._requests_state import get_server_ready

    def get_base_url(self) -> str:
        if not self._base_url:
            return ""
        return self._base_url

    def set_base_url(self, new_url: str):
        try:
            url = validate_base_url(new_url)
        except Exception as e:
            raise Exception(f"could not set client base URL: {e}")

        self._base_url = str(url)
        self._parsed_base_url = url

        # TODO: log f"client base URL was set: {self._base_url}"
        return

    async def _do_request(
        self,
        method: str,
        destination: str,
        json_data: dict | None,
        token: str = "",
        handle_response: bool = True,
    ) -> Any:
        url = self._resolve_url("/api" + destination)
        if not url:
            return None

        dest_uses_access_token = (
            (u := str(url)) and "/refresh" not in u and "/revoke" not in u
        )
        should_retry = dest_uses_access_token and self._auto_refresh

        current_token = token

        while True:
            headers = {}
            if current_token:
                headers["Authorization"] = f"Bearer {current_token}"

            request = self.build_request(
                method,
                url,
                json=json_data,
                headers=headers,
                timeout=self.timeout,
            )

            response = await self._send_single_request(request)

            if not self._auto_refresh:
                break

            token_expired = check_token_expired(current_token)

            if (
                response.status_code != 401
                or current_token == ""
                or (not token_expired)
            ):
                break
            elif should_retry:
                try:
                    await self.user_token_refresh()
                    current_token = self._token
                    should_retry = False
                    continue
                except Exception as e:
                    raise e
            else:
                break
        if not handle_response:
            return response
        try:
            return self._handle_response(response)
        except RuntimeError as e:
            print(e)
            return None
        except Exception as e:
            raise e

    def _handle_response(self, response: httpx.Response) -> Any:
        status = response.status_code
        if status == 204:
            return None

        if status in (200, 201):
            try:
                return response.json()
            except json.JSONDecodeError as e:
                raise ValueError(f"could not decode response: {e}")

        error_msg = response.text[:1024]
        raise RuntimeError(f"bad status code {status}: {error_msg}")

    def _resolve_url(self, destination: str) -> str | None:
        if self._parsed_base_url is None:
            raise Exception(
                "refused to resovle destination url; client base url not set"
            )

        destination = destination.strip()
        if destination == "":
            raise Exception("destination empty")

        u = httpx.URL(destination)

        # Reject scheme-less URLs (//host/path) and any provided scheme
        if u.scheme != "" or u.host != "":
            if same_hostname(u, self._parsed_base_url):
                return str(u)
            raise Exception(f"refusing external URL host {u.host}")

        return str(self._parsed_base_url.join(destination))
