import requests

headers = {'User-Agent': 'Android'}


def get(url, params=None, retry=3, **kwargs):
    while retry > 0:
        try:
            return str(requests.get(url, params=params, headers=headers, **kwargs).text)
        except ConnectionError:
            pass
        finally:
            retry -= 1
    return str(requests.get(url, params=params, headers=headers, **kwargs).text)


def post(url, data=None, retry=3, **kwargs):
    while retry > 0:
        try:
            return str(requests.post(url, data, headers=headers, **kwargs).text)
        except ConnectionError:
            pass
        finally:
            retry -= 1
    return str(requests.post(url, data, headers=headers, **kwargs).text)
