# Flink SQL Gateway Client
A client library for accessing Flink SQL Gateway REST API
(mostly generated by [OpenAPI Generator](https://github.com/openapi-generators))

## Usage
First, create a client:

```python
from flink_gateway_api import Client

client = Client(base_url="http://localhost:8083")
```

If the endpoints you're going to hit require authentication, use `AuthenticatedClient` instead:

```python
from flink_gateway_api import AuthenticatedClient

client = AuthenticatedClient(base_url="http://localhost:80083", token="SuperSecretToken")
```

Now call your endpoint and use your models:

```python
import json
import time
from flink_gateway_api import Client
from flink_gateway_api.api.default import (
   open_session,
   close_session,
   execute_statement,
   fetch_results,
)
from flink_gateway_api.models import (
   OpenSessionRequestBody,
   ExecuteStatementResponseBody,
   RowFormat,
)

with Client('http://localhost:8083') as client:
   responses = open_session.sync(client=client, body=OpenSessionRequestBody.from_dict({
      "properties": {
         "idle-timeout": "10s"
      },
      "sessionName": "test_session"
   }))
   print(f"Open session response: {responses}")

   select_result = execute_statement.sync(responses.session_handle, client=client,
                                          body=ExecuteStatementResponseBody.from_dict({
                                             "statement": "SELECT 23 as age, 'Alice Liddel' as name;",
                                          }))

   print(f"Select result: {select_result}")
   time.sleep(1)
   fetch_return = fetch_results.sync(
      responses.session_handle,
      select_result.operation_handle,
      0,
      client=client,
      row_format=RowFormat.JSON,
   )
   print(f"Fetch return: {json.dumps(fetch_return.to_dict())}")

   close_session.sync(responses.session_handle, client=client)
   print(f"Session closed")
```

Or do the same thing with an async version:

```python
import json
import asyncio
from flink_gateway_api import Client
from flink_gateway_api.api.default import (
   open_session,
   close_session,
   execute_statement,
   fetch_results,
)
from flink_gateway_api.models import (
   OpenSessionRequestBody,
   ExecuteStatementResponseBody,
   RowFormat,
)

async with Client('http://localhost:8083') as client:
   responses = await open_session.asyncio(client=client, body=OpenSessionRequestBody.from_dict({
      "properties": {
         "idle-timeout": "10s"
      },
      "sessionName": "test_session"
   }))
   print(f"Open session response: {responses}")

   select_result = await execute_statement.asyncio(responses.session_handle, client=client,
                                                   body=ExecuteStatementResponseBody.from_dict({
                                                      "statement": "SELECT 23 as age, 'Alice Liddel' as name;",
                                                   }))

   print(f"Select result: {select_result}")
   await asyncio.sleep(1)  # Changed time.sleep to asyncio.sleep
   fetch_return = await fetch_results.asyncio(
      responses.session_handle,
      select_result.operation_handle,
      0,
      client=client,
      row_format=RowFormat.JSON,
   )
   print(f"Fetch return: {json.dumps(fetch_return.to_dict())}")

   await close_session.asyncio(responses.session_handle, client=client)
   print(f"Session closed")
```

By default, when you're calling an HTTPS API it will attempt to verify that SSL is working correctly. Using certificate verification is highly recommended most of the time, but sometimes you may need to authenticate to a server (especially an internal server) using a custom certificate bundle.

```python
client = AuthenticatedClient(
    base_url="https://internal_api.example.com", 
    token="SuperSecretToken",
    verify_ssl="/path/to/certificate_bundle.pem",
)
```

You can also disable certificate validation altogether, but beware that **this is a security risk**.

```python
client = AuthenticatedClient(
    base_url="https://internal_api.example.com", 
    token="SuperSecretToken", 
    verify_ssl=False
)
```

Things to know:
1. Every path/method combo becomes a Python module with four functions:
    1. `sync`: Blocking request that returns parsed data (if successful) or `None`
    1. `sync_detailed`: Blocking request that always returns a `Request`, optionally with `parsed` set if the request was successful.
    1. `asyncio`: Like `sync` but async instead of blocking
    1. `asyncio_detailed`: Like `sync_detailed` but async instead of blocking

1. All path/query params, and bodies become method arguments.
1. If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above)
1. Any endpoint which did not have a tag will be in `flink_gateway_api.api.default`

## Advanced customizations

There are more settings on the generated `Client` class which let you control more runtime behavior, check out the docstring on that class for more info. You can also customize the underlying `httpx.Client` or `httpx.AsyncClient` (depending on your use-case):

```python
from flink_gateway_api import Client

def log_request(request):
    print(f"Request event hook: {request.method} {request.url} - Waiting for response")

def log_response(response):
    request = response.request
    print(f"Response event hook: {request.method} {request.url} - Status {response.status_code}")

client = Client(
    base_url="http://localhost:80083",
    httpx_args={"event_hooks": {"request": [log_request], "response": [log_response]}},
)

# Or get the underlying httpx client to modify directly with client.get_httpx_client() or client.get_async_httpx_client()
```

You can even set the httpx client directly, but beware that this will override any existing settings (e.g., base_url):

```python
import httpx
from flink_gateway_api import Client

client = Client(
    base_url="http://localhost:80083",
)
# Note that base_url needs to be re-set, as would any shared cookies, headers, etc.
client.set_httpx_client(httpx.Client(base_url="http://localhost:80083"))
```