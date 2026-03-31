from datetime import datetime, timezone
import jwt
import httpx


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


type Queries = dict[str, str | list[str]] | None


def generate_query_string(url_queries: Queries) -> str:
    if not url_queries:
        return ""
    query_string = "?"
    first = True
    for k, v in url_queries:
        if not first:
            query_string += "&"
        else:
            first = False
        query_string += k + "="
        if isinstance(v, list[str]):
            query_string += ",".join(v)
        else:
            query_string += v
    return query_string
