from __future__ import annotations

api_version = "/api/v1"


def get_api_version(url_prefix: str | None = None):
    if url_prefix is None:
        return api_version

    return f'{api_version}{url_prefix}'
