from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.refresh_materialized_table_request_body import RefreshMaterializedTableRequestBody
from ...models.refresh_materialized_table_response_body import RefreshMaterializedTableResponseBody
from ...types import Response


def _get_kwargs(
    session_handle: str,
    identifier: str,
    *,
    body: RefreshMaterializedTableRequestBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/sessions/{session_handle}/materialized-tables/{identifier}/refresh",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[RefreshMaterializedTableResponseBody]:
    if response.status_code == 200:
        response_200 = RefreshMaterializedTableResponseBody.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[RefreshMaterializedTableResponseBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    session_handle: str,
    identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: RefreshMaterializedTableRequestBody,
) -> Response[RefreshMaterializedTableResponseBody]:
    """Refresh materialized table

    Args:
        session_handle (str):
        identifier (str):
        body (RefreshMaterializedTableRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RefreshMaterializedTableResponseBody]
    """

    kwargs = _get_kwargs(
        session_handle=session_handle,
        identifier=identifier,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    session_handle: str,
    identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: RefreshMaterializedTableRequestBody,
) -> Optional[RefreshMaterializedTableResponseBody]:
    """Refresh materialized table

    Args:
        session_handle (str):
        identifier (str):
        body (RefreshMaterializedTableRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RefreshMaterializedTableResponseBody
    """

    return sync_detailed(
        session_handle=session_handle,
        identifier=identifier,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    session_handle: str,
    identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: RefreshMaterializedTableRequestBody,
) -> Response[RefreshMaterializedTableResponseBody]:
    """Refresh materialized table

    Args:
        session_handle (str):
        identifier (str):
        body (RefreshMaterializedTableRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RefreshMaterializedTableResponseBody]
    """

    kwargs = _get_kwargs(
        session_handle=session_handle,
        identifier=identifier,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    session_handle: str,
    identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: RefreshMaterializedTableRequestBody,
) -> Optional[RefreshMaterializedTableResponseBody]:
    """Refresh materialized table

    Args:
        session_handle (str):
        identifier (str):
        body (RefreshMaterializedTableRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RefreshMaterializedTableResponseBody
    """

    return (
        await asyncio_detailed(
            session_handle=session_handle,
            identifier=identifier,
            client=client,
            body=body,
        )
    ).parsed
