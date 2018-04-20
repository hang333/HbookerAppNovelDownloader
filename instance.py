from config import *


class Vars:
    cfg = Config(os.getcwd() + '/../Hbooker/config.json', os.getcwd() + "/../Hbooker")
    current_bookshelf = None
    current_book = None
    help_info = ['下载的书籍文件、缓存和配置文件在../Hbooker/下',
                 'quit \t 退出脚本',
                 'login <用户名> <密码> \t 登录欢乐书客帐号',
                 'config load \t 重新加载配置文件',
                 'config save \t 保存配置文件',
                 'config set <配置项> [值] \t 设置配置项的值(空值表示删除)',
                 'help \t 用法与帮助',
                 'bookshelf \t 刷新并显示当前书架列表',
                 'bookshelf <书架编号> \t 切换书架',
                 'book \t 刷新并显示当前书架的书籍列表',
                 'book <书籍编号/书籍ID> \t 选择书籍',
                 'download \t 下载书籍(无-s和-e参数则下载全本)\n'
                 '\t参数列表\n'
                 '\t-a \t 下载当前书架所有书籍\n'
                 '\t-d <分卷编号> \t 下载指定分卷\n'
                 '\t-s <起始章节编号> \t 从指定章节开始下载\n'
                 '\t-e <终止章节编号> \t 下载到指定章节为止',
                 'update \t 更新已下载的所有书籍并复制到updates文件夹']


def get(prompt, default=None):
    while True:
        ret = input(prompt)
        if ret != '':
            return ret
        elif default is not None:
            return default
