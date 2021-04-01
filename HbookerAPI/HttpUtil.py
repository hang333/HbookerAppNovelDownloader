import requests
import time
import sys

headers = {'User-Agent': 'Android'}
maxRetry = 20


def get(url, params=None, retry=maxRetry, **kwargs):
    # print("\t:get:" + str(url) + ' params:' + str(params) + ' kwargs' + str(kwargs))
    for count in range(retry):
        try:
            return str(requests.get(url, params=params, headers=headers, **kwargs).text)
        except (OSError, TimeoutError, IOError) as e:
            if retry != retry - 1:
                print("\nGet Error Retry: " + str(e) + '\n' + url)
                time.sleep(1 * count)
            else:
                print("\nGet Failed: " + str(e) + '\n' + url + "\nTerminating......")
                sys.exit(1)


def post(url, data=None, retry=maxRetry, **kwargs):
    # print("\t:get:" + str(url) + ' date:' + str(data) + ' kwargs:' + str(kwargs))
    for count in range(retry):
        try:
            return str(requests.post(url, data, headers=headers, **kwargs).text)
        except (OSError, TimeoutError, IOError) as e:
            if retry != retry - 1:
                print("\nGet Error Retry: " + str(e) + '\n' + url)
                time.sleep(1 * count)
            else:
                print("\nPost Failed: " + str(e) + '\n' + url + "\nTerminating......")
                sys.exit(1)
