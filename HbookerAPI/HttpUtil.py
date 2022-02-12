import requests
import time
import sys

headers = {'User-Agent': 'Android'}
maxRetry = 10
requests_timeout = 10


def get(url, params=None, retry=maxRetry, **kwargs):
    for count in range(retry):
        try:
            return str(requests.get(url, params=params, headers=headers, **kwargs, timeout=requests_timeout).text)
        except requests.exceptions.RequestException as e:
            print("\nGet Error Retry: " + str(e) + '\n' + url)
            time.sleep(1 * count)
        except Exception as e:
            print(repr(e))
            break
    print("\nGet Failed, Terminating......")
    sys.exit(1)


def post(url, data=None, retry=maxRetry, **kwargs):
    for count in range(retry):
        try:
            return str(requests.post(url, data, headers=headers, **kwargs, timeout=requests_timeout).text)
        except requests.exceptions.RequestException as e:
            print("\nGet Error Retry: " + str(e) + '\n' + url)
            time.sleep(1 * count)
        except Exception as e:
            print(repr(e))
            break
    print("\nPost Failed, Terminating......")
    sys.exit(1)
