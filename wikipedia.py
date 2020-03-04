from requests.exceptions import RequestException

import requests

_WIKI_URL = "https://en.wikipedia.org/wiki/"
_MAX_RETRIES = 3
_REQ_TIMEOUT = 30

_ERR_NOPAGE = "No page for term: {0}"


class PageFinder:
    def __init__(self, terms, session=None):
        self._iter = iter(terms)
        if session is None:
            self._method = requests.head
        else:
            self._method = session.head

    def __iter__(self):
        return self

    def __next__(self):
        term = next(self._iter)
        return term, self._page_url(term)

    def _page_url(self, term):
        response = _http_request(
            self._method, _WIKI_URL + term, timeout=_REQ_TIMEOUT
        )
        if response.status_code == requests.codes.not_found:
            raise ValueError(_ERR_NOPAGE.format(term))
        elif response.status_code != requests.codes.ok:
            response.raise_for_status()
        return response.url


def _http_request(method, url, **kwargs):
    for _ in range(0, _MAX_RETRIES):
        req_exc = None
        try:
            resp = method(url, **kwargs)
            break
        except RequestException as e:
            req_exc = e
    if req_exc:
        raise req_exc
    else:
        return resp
