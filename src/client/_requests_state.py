from client import Client
from endpoints import endpoint_server_readiness


async def get_server_ready(self: Client) -> bool:
    endpoint = endpoint_server_readiness()
    try:
        response = await self.get(endpoint)
        return 200 <= response.status_code < 300
    except Exception as e:
        raise e
