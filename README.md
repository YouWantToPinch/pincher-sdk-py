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

You can import the package and define a new client instance in the following manner:

```Python
from pincher_sdk import Client

```

## License: BSD 3-Clause

pincher-sdk-py is licensed under the BSD 3-Clause License. What this means is that:

#### You are allowed to

- Modify the code, and distribute your own versions.
- Use this library in personal, open-source, or commercial projects.
- Include it in proprietary software, without making your project open-source.

#### You are not allowed to

- Remove or alter the license and copyright notice.
- Use the names "pincher-sdk-go" or its contributors for endorsements without permission.
