from typing import Any
import httpx
import json
import jwt
from datetime import datetime, timezone


class Client(httpx.AsyncClient):
    def __init__(
        self,
        base_url: str,
        timeout: int,
        cache_interval: int,
        auto_refresh: bool = False,
    ) -> None:
        super().__init__(base_url=base_url)

        self.Cache = None
        self._base_url: str = ""
        self._parsed_base_url: httpx.URL | None = None
        self._token: str = ""
        self._refresh_token: str = ""
        self._auto_refresh: bool = auto_refresh

    # import methods from organized modules
    from ._requests_auth import user_token_refresh, user_token_revoke

    def base_url(self) -> str:
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
        data: Any,
        token: str = "",
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
                method, destination, data=data, headers=headers
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
                    self.user_token_refresh()
                    current_token = self._token
                    should_retry = False
                    continue
                except Exception as e:
                    raise e
            try:
                return self._handle_response(response)
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

        # Reject scheme-less URLs and any provided scheme
        if u.scheme != "" or u.netloc != "":
            if same_hostname(u, self._parsed_base_url):
                return str(u)
            raise Exception(f"refusing external URL host {u.netloc!r}")

        return str(self._parsed_base_url.join(destination))


# ------------
#   HELPERS
# ------------


def same_hostname(a: httpx.URL, b: httpx.URL) -> bool:
    # Host may include port; compare case-insensitively
    return a.netloc.lower() == b.netloc.lower()


def validate_base_url(
    new_url: str, enforce_https: bool = False, allow_local=True
) -> httpx.URL:
    new_url = new_url.strip().removesuffix("/")
    url = None
    try:
        url = httpx.URL(new_url)
    except httpx.InvalidURL as e:
        raise Exception(f"invalid base URL: {e}")

    if url.scheme != "https" and enforce_https:
        raise Exception("base URL must not have a path (trailing /)")

    if url.path == "":
        raise Exception("base URL must not have a path (trailing /)")

    if url.netloc == "":
        raise Exception("base URL must have a host")

    if not allow_local and url.host.count(".") < 1:
        raise Exception("base URL must have a domain and TLD")

    return url


def check_token_expired(token: str) -> bool:
    try:
        claims = jwt.decode(token, options={"verify_signature": False})
        exp = claims.get("exp")
        if not exp:
            return True

        exp_datetime = datetime.fromtimestamp(exp, tz=timezone.utc)
        return exp_datetime < datetime.now(timezone.utc)

    except Exception:
        # TODO: log "invalid claims"
        return True
