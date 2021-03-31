from config import *


class Vars:
    cfg = Config('HbookerAppNovelDownloader - Config.json', os.getcwd())
    current_bookshelf = None
    current_book = None
    help_info = \
        """HbookerAppNovelDownloader 刺蝟貓 / 歡樂書客 小說下載器
請閱讀README.md
指令(指令輸入字首即可):
h | help\t\t\t\t\t\t\t--- 顯示用法與幫助 (顯示此訊息)
q | quit\t\t\t\t\t\t\t--- 退出腳本
l | login <手機號/郵箱/用戶名> <密碼>\t\t\t\t--- 登錄歡樂書客帳號
t | task\t\t\t\t\t\t\t--- 執行每日簽到，領代幣 (正常來說，已經自動執行，不需再次執行)
s | bookshelf\t\t\t\t\t\t\t--- 刷新並顯示當前書架列表 (啟動時會自動刷新1次)
s <書架編號> | shelf <書架編號>\t\t\t\t\t--- 選擇與切換書架
b | book\t\t\t\t\t\t\t--- 刷新並顯示當前書架的書籍列表
b <書籍編號/書籍ID> | book <書籍編號/書籍ID>\t\t\t--- 選擇書籍
d | download\t\t\t\t\t\t\t--- 下載當前書籍(book時選擇的書籍)
d <書籍編號/書籍ID> | download <書籍編號/書籍ID>\t\t--- 下載指定ID書籍
ds <書架編號> | downloadshelf <書架編號> \t\t\t--- 下載整個書架
u | update\t\t\t\t\t\t\t--- 下載"list.txt"中的所有書籍
u <list_path.txt> | update <list_path.txt>\t\t\t--- 下載指定檔案"list_path.txt"中的所有書籍
"""


def get(prompt, default=None):
    while True:
        ret = input(prompt)
        if ret != '':
            return ret
        elif default is not None:
            return default
