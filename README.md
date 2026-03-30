# Introduction

## Purpose

`pincher-sdk-py` (or, just known by its Python package name, `pincher_sdk`) is a library providing convenient access to the Pincher REST API endpoints from applications written in Python.

It is a Python port of [its Go counterpart](https://github.com/YouWantToPinch/pincher-sdk-go).

---

> [!NOTE]
> The `pincher_sdk` package is currently in an alpha pre-release state.

---

# Getting started

The package is available on the Python Package Index (PyPI).
You can add it to your own projects to build clients or other Pincher tools with the following command:

```bash
uv add pincher_sdk
```

You can import the package and define a new client instance with the following:

```Python

import asyncio
from pincher_sdk import Client, cache


async def main():
    client = Client(cache.Cache())
    ready = await client.get_server_ready()
    if ready:
        print("The Pincher API server is live!")
    else:
        print("Could not reach the Pincher API server.")


if __name__ == "__main__":
    asyncio.run(main())

```

The above setup produces a client instance with default settings. These are:

- An in-memory cache
  - Up to 100 budget cache entries, each with internal caches for each budget resource given this same capacity of 100 entries.
  - 5-minute TTL for each entry
- Auto-refresh enabled (the `/refresh` endpoint is hit once when an active access token is found to be expired, so as to generate a new one using the active refresh token)
- A default `base_url` that is: `http://localhost:8080`
- A request timeout value of 10 seconds

## License: BSD 3-Clause

pincher-sdk-py is licensed under the BSD 3-Clause License. What this means is that:

#### You are allowed to

- Modify the code, and distribute your own versions.
- Use this library in personal, open-source, or commercial projects.
- Include it in proprietary software, without making your project open-source.

#### You are not allowed to

- Remove or alter the license and copyright notice.
- Use the names "pincher-sdk-py" or its contributors for endorsements without permission.
