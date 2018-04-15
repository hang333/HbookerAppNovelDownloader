import requests

headers = {'User-Agent': 'Android'
           }


def get(url, params=None, **kwargs):
    return str(requests.get(url, params=params, headers=headers, **kwargs).text)


def post(url, data=None, **kwargs):
    return str(requests.post(url, data, headers=headers, **kwargs).text)
