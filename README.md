## Acadre docs

Add `/Frontend/Help/` to the base url.

## installation

Declare a dependency and it's source in `pyproject.toml` if it is not already there:

```toml
[project]
dependencies = [
    "acadrepy",
]

[tool.uv.sources]
acadrepy = { git = "https://github.com/BorholmsRegionsKommuneIT/acadrepy" }
```

then sync with `uv sync`

## usage

```python
from dotenv import load_dotenv
import os
from acadrepy import AcadreClient

load_dotenv()
base_url = os.getenv("ACADRE_BASE_URL")
username = os.getenv("ACADRE_USERNAME")
password = os.getenv("ACADRE_PASSWORD")
acadre_api = AcadreClient(base_url, username, password)

# Authenticate with the API
acadre_api.authenticate()

# Get documents by search term with pagination
try:
    documents = acadre_api.get_documents_by_searchterm_paged("your search term here, fx a cpr number", 0, 10)
    print(documents)
except Exception as e:
    print(e)
```