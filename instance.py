from config import *


class Vars:
    cfg = Config('HbookerAppNovelDownloader - Config.json', os.getcwd())
    current_bookshelf = None
    current_book = None


def get(prompt, default=None):
    while True:
        ret = input(prompt)
        if ret != '':
            return ret
        elif default is not None:
            return default
