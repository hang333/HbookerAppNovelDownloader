import HbookerAPI
from config import *
from Epub import *
import os
import shutil


class Book:
    index = None
    book_id = None
    book_name = None
    author_name = None
    cover = None
    book_info = None
    last_chapter_info = None
    division_list = None
    chapter_list = None
    division_chapter_list = None
    epub = None
    config = None
    file_path = None

    def __init__(self, index, book_info):
        self.index = index
        self.book_info = book_info
        self.book_id = book_info['book_id']
        self.book_name = book_info['book_name']
        self.author_name = book_info['author_name']
        self.cover = book_info['cover'].replace(' ', '')
        self.last_chapter_info = book_info['last_chapter_info']
        self.division_list = []
        self.chapter_list = []
        self.division_chapter_list = {}

    def get_division_list(self):
        print('[提示]', '正在获取书籍分卷...')
        response = HbookerAPI.Book.get_division_list(self.book_id)
        if response.get('code') == '100000':
            self.division_list = response['data']['division_list']

    def show_division_list(self):
        for division in self.division_list:
            print('分卷编号:', division['division_index'], ', 分卷名:', division['division_name'])

    def get_chapter_catalog(self):
        print('[提示]', '正在获取书籍目录...')
        self.chapter_list.clear()
        for division in self.division_list:
            response = HbookerAPI.Book.get_chapter_update(division['division_id'])
            if response.get('code') == '100000':
                self.chapter_list.extend(response['data']['chapter_list'])
                self.division_chapter_list[division['division_name']] = response['data']['chapter_list']
        self.chapter_list.sort(key=lambda x : int(x['chapter_index']))

    def show_chapter_latest(self):
        print('\t最新章节: \t章节编号:', self.chapter_list[-1]['chapter_index'], ', 章节标题:',
              self.chapter_list[-1]['chapter_title'])

    def download_chapter(self, chapter_index_start=None, chapter_index_end=None, copy_dir=None):
        if len(self.chapter_list) == 0:
            print('[提示]', '暂无书籍目录')
            return
        self.config = Config(os.getcwd() + '/../Hbooker/' + self.book_name + '/config.json',
                             os.getcwd() + '/../Hbooker/' + self.book_name)
        self.config.load()
        if self.config.data.get('downloaded_list') is None:
            self.config.data['downloaded_list'] = []
        if self.config.data.get('last_chapter_index') is None:
            self.config.data['last_chapter_index'] = 0
        chapter_index_start = int(chapter_index_start or int(self.config.data['last_chapter_index']) + 1)
        chapter_index_end = int(chapter_index_end or len(self.chapter_list))
        if chapter_index_start < 1:
            chapter_index_start = 1
        if chapter_index_end > len(self.chapter_list):
            chapter_index_end = len(self.chapter_list)
        if chapter_index_start > chapter_index_end:
            print('[提示][下载]', '《' + self.book_name + '》无需下载')
            return
        self.file_path = os.getcwd() + '/../Hbooker/' + self.book_name + '/' + self.book_name + '.epub'
        self.epub = EpubFile(self.file_path,
                             os.getcwd() + '/../Hbooker/cache/' + self.book_name, self.book_id, self.book_name,
                             self.author_name)
        print('[提示][下载]', '《' + self.book_name + '》', '文件名:', self.book_name + '.epub')
        self.epub.setcover(self.cover)
        print('[提示][下载]', '开始下载: 起始章节编号:', chapter_index_start, ', 终止章节编号:', chapter_index_end)
        for i in range(chapter_index_start, chapter_index_end + 1):
            if self.download_single(i) is False:
                print('[提示][下载]', '遇到未付费章节，跳过之后所有章节')
                break
        self.epub.export()
        self.epub.export_txt()
        print('[提示][下载]', '《' + self.book_name + '》下载已完成')
        try:
            if copy_dir is not None:
                copy_dir=copy_dir.replace("?","？")
                file_dir, file_name = os.path.split(self.file_path)
                if not os.path.isdir(copy_dir):
                    os.makedirs(copy_dir)
                shutil.copyfile(self.file_path, copy_dir + '/' + file_name)
                shutil.copyfile(self.file_path.replace('epub', 'txt'),
                                copy_dir + '/' + file_name.replace('epub', 'txt'))
        except Exception as e:
            print('[错误]', e)
            print('复制文件时出错')

    def download_division(self, division_index):
        division_name = None
        for division in self.division_list:
            if division['division_index'] == division_index:
                division_name = division['division_name']
                break
        if division_name is None:
            print('[提示]', '分卷编号不正确')
            return
        print('[提示]', '《' + self.book_name + '》', '下载分卷:', division_name)
        if len(self.division_chapter_list.get(division_name)) > 0:
            self.config = Config(os.getcwd() + '/../Hbooker/' + self.book_name + '/config-' + division_name + '.json',
                                 os.getcwd() + '/../Hbooker/' + self.book_name)
            self.config.load()
            if self.config.data.get('downloaded_list') is None:
                self.config.data['downloaded_list'] = []
            if self.config.data.get('last_chapter_index') is None:
                self.config.data['last_chapter_index'] = 0
            self.file_path = os.getcwd() + '/../Hbooker/' + self.book_name + '/' + self.book_name + '-' + division_name + '.epub'
            self.epub = EpubFile(
                self.file_path,
                os.getcwd() + '/../Hbooker/cache/' + self.book_name + '-' + division_name, self.book_id, self.book_name,
                self.author_name)
            print('[提示][下载]', '《' + self.book_name + '》', '文件名:', self.book_name + '-' + division_name + '.epub')
            self.epub.setcover(self.cover)
            for chapter_info in self.division_chapter_list[division_name]:
                if self.download_single_by_id(chapter_info['chapter_index'], chapter_info['chapter_id']) is False:
                    print('[提示][下载]', '遇到未付费章节，跳过之后所有章节')
                    break
            self.epub.export()
            self.epub.export_txt()
            print('[提示][下载]', '《' + self.book_name + '》' + division_name, '下载已完成')
        else:
            print('[提示]', '该分卷暂无章节')

    def download_single(self, i):
        i = int(i)
        if self.config.data['downloaded_list'].count(i) > 0:
            print('[提示][下载]', '编号:', i, ' 已下载，跳过')
            return True
        chapter_id = self.chapter_list[i - 1]['chapter_id']
        response = HbookerAPI.Chapter.get_chapter_command(chapter_id)
        if response.get('code') == '100000':
            chapter_command = response['data']['command']
            response2 = HbookerAPI.Chapter.get_cpt_ifm(chapter_id, chapter_command)
            if response2.get('code') == '100000' and response2['data']['chapter_info'].get('chapter_title') is not None:
                print('[提示][下载]', '编号:', i, ', chapter_id:', chapter_id, ', 标题:',
                      response2['data']['chapter_info']['chapter_title'])
                if response2['data']['chapter_info']['auth_access'] == '1':
                    content = HbookerAPI.CryptoUtil.decrypt(response2['data']['chapter_info']['txt_content'],
                                                            chapter_command).decode('utf-8')
                    if content.find('\n') + 1 < len(content):
                        if content[-1] == '\n':
                            content = content[:-2]
                        content = content.replace('\n', '</p>\r\n<p>')
                    author_say = response2['data']['chapter_info']['author_say'].replace('\r', '')
                    author_say = author_say.replace('\n', '</p>\r\n<p>')
                    self.epub.addchapter(str(i), chapter_id, response2['data']['chapter_info']['chapter_title'],
                                         '<p>' + content + '</p>\r\n<p>' + author_say + '</p>')
                    self.config.data['downloaded_list'].append(i)
                    self.config.data['last_chapter_index'] = max(i, self.config.data['last_chapter_index'])
                    self.config.save()
                    return True
                else:
                    print('[提示][下载]', '该章节未付费，无法下载')
                    return False
            else:
                self.config.data['downloaded_list'].append(i)
                self.config.data['last_chapter_index'] = max(i, self.config.data['last_chapter_index'])
                self.config.save()
                print('[提示][下载]', '编号:', i, ', chapter_id:', chapter_id, ', 该章节为空章节，标记为已下载')
                return True

    def download_single_by_id(self, chapter_index, chapter_id):
        chapter_index = int(chapter_index)
        response = HbookerAPI.Chapter.get_chapter_command(chapter_id)
        if response.get('code') == '100000':
            chapter_command = response['data']['command']
            response2 = HbookerAPI.Chapter.get_cpt_ifm(chapter_id, chapter_command)
            if response2.get('code') == '100000' and response2['data']['chapter_info'].get('chapter_title') is not None:
                print('[提示][下载]', '编号:', chapter_index, ', chapter_id:', chapter_id, ', 标题:',
                      response2['data']['chapter_info']['chapter_title'])
                if response2['data']['chapter_info']['auth_access'] == '1':
                    content = HbookerAPI.CryptoUtil.decrypt(response2['data']['chapter_info']['txt_content'],
                                                            chapter_command).decode('utf-8')
                    if content.find('\n') + 1 < len(content):
                        content = content[content.find('\n') + 1:]
                        if content[-1] == '\n':
                            content = content[:-2]
                        content = content.replace('\n', '</p>\r\n<p>')
                    else:
                        content = ''
                    author_say = response2['data']['chapter_info']['author_say'].replace('\r', '')
                    author_say = author_say.replace('\n', '</p>\r\n<p>')
                    self.epub.addchapter(str(chapter_index), chapter_id, response2['data']['chapter_info']['chapter_title'],
                                         '<p>' + content + '</p>\r\n<p>' + author_say + '</p>')
                    self.config.data['downloaded_list'].append(chapter_index)
                    self.config.data['last_chapter_index'] = max(chapter_index, self.config.data['last_chapter_index'])
                    self.config.save()
                    return True
                else:
                    print('[提示][下载]', '该章节未付费，无法下载')
                    return False
            else:
                self.config.data['downloaded_list'].append(chapter_index)
                self.config.data['last_chapter_index'] = max(chapter_index, self.config.data['last_chapter_index'])
                self.config.save()
                print('[提示][下载]', '编号:', chapter_index, 'chapter_id:', chapter_id, ', 该章节为空章节，标记为已下载')
                return True

