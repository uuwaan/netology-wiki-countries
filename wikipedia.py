from requests.exceptions import RequestException

import requests

_WIKI_URL = "https://en.wikipedia.org/wiki/"
_MAX_RETRIES = 3
_REQ_TIMEOUT = 30

_ERR_NOPAGE = "No page for term: {0}"


class PageFinder:
    def __init__(self, terms):
        self._iter = iter(terms)
        self._session = requests.Session()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            term = next(self._iter)
            return term, self._page_url(term)
        except Exception:
            self._session.close()
            raise

    def _page_url(self, term):
        response = _http_request(
            self._session.head,
            _WIKI_URL + term,
            {"timeout": _REQ_TIMEOUT},
        )
        if response.status_code == requests.codes.not_found:
            raise ValueError(_ERR_NOPAGE.format(term))
        elif response.status_code != requests.codes.ok:
            response.raise_for_status()
        return response.url


def _http_request(method, url, args):
    for _ in range(0, _MAX_RETRIES):
        req_exc = None
        try:
            resp = method(url, **args)
            break
        except RequestException as e:
            req_exc = e
    if req_exc:
        raise req_exc
    else:
        return resp
