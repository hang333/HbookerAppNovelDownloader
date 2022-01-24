import requests
import time
import sys

headers = {'User-Agent': 'Android'}
maxRetry = 10


def get(url, params=None, retry=maxRetry, **kwargs):
    for count in range(retry):
        try:
            return str(requests.get(url, params=params, headers=headers, **kwargs).text)
        except (OSError, TimeoutError, IOError, requests.exceptions.Timeout) as e:
            if retry != retry - 1:
                print("\nGet Error Retry: " + str(e) + '\n' + url)
                time.sleep(1 * count)
            else:
                print("\nGet Failed: " + str(e) + '\n' + url + "\nTerminating......")
                sys.exit(1)
        except Exception as e:
            print(e)


def post(url, data=None, retry=maxRetry, **kwargs):
    for count in range(retry):
        try:
            return str(requests.post(url, data, headers=headers, **kwargs).text)
        except (OSError, TimeoutError, IOError, requests.exceptions.Timeout) as e:
            if retry != retry - 1:
                print("\nGet Error Retry: " + str(e) + '\n' + url)
                time.sleep(1 * count)
            else:
                print("\nPost Failed: " + str(e) + '\n' + url + "\nTerminating......")
                sys.exit(1)
        except Exception as e:
            print(e)
