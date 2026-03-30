from __future__ import annotations

from typing import Any, Dict, Optional

try:
    import requests
except ImportError as e:  # pragma: no cover
    requests = None
    _IMPORT_ERROR = e
else:
    _IMPORT_ERROR = None


class RequestsPostman:
    """A small requests-based postman compatible with jmcomic's needs.

    It is intentionally minimal: get/post, session cookies, headers, proxies,
    and a no-op with_redirect_catching() for API compatibility.
    """

    def __init__(self, **kwargs):
        if requests is None:  # pragma: no cover
            raise ImportError(
                'requests is required for RequestsPostman but is not installed'
            ) from _IMPORT_ERROR

        self._session = requests.Session()
        self._default_kwargs: Dict[str, Any] = {}
        self._redirect_catching = False
        self._meta_data: Dict[str, Any] = {}

        headers = kwargs.pop('headers', None)
        cookies = kwargs.pop('cookies', None)
        proxies = kwargs.pop('proxies', None)
        timeout = kwargs.pop('timeout', None)

        # requests ignores unknown kwargs, but we keep only the ones we use.
        kwargs.pop('impersonate', None)
        kwargs.pop('type', None)

        if headers:
            self._session.headers.update(headers)
        if cookies:
            self._session.cookies.update(cookies)
        if proxies:
            self._session.proxies.update(proxies)
        if timeout is not None:
            self._default_kwargs['timeout'] = timeout

        # Any remaining kwargs are treated as default request kwargs.
        self._default_kwargs.update(kwargs)

    def with_redirect_catching(self):
        self._redirect_catching = True
        return self

    def close(self):
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False

    def __getitem__(self, key):
        return self.get_meta_data(key)

    def __setitem__(self, key, value):
        if key == 'cookies':
            self._session.cookies.update(value)
        else:
            self.set_meta_data(key, value)

    def get_meta_data(self, key: str, default=None):
        if key == 'cookies':
            return self._session.cookies
        return self._meta_data.get(key, default)

    def set_meta_data(self, key: str, value):
        self._meta_data[key] = value

    def _request(self, method: str, url: str, **kwargs):
        request_kwargs = dict(self._default_kwargs)
        request_kwargs.update(kwargs)
        # requests follows redirects by default, which matches the existing use.
        return self._session.request(method=method, url=url, **request_kwargs)

    def get(self, url: str, **kwargs):
        return self._request('GET', url, **kwargs)

    def post(self, url: str, **kwargs):
        return self._request('POST', url, **kwargs)
