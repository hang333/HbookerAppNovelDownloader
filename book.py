from Epub import *
import HbookerAPI
import threading
import queue
import msg
import os


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
        self.get_chapter_catalog_mt_dl_lock = threading.Lock()
        self.concurrent_download_queue = queue.Queue()
        for item in range(Vars.cfg.data['max_concurrent_downloads']):
            self.concurrent_download_queue.put(item)
        self.process_finished_count = 0
        self.downloaded_count = 0
        # self.config = Config(Vars.cfg.data['cache_dir'] + 'book-' + self.fix_illegal_book_name() + '.json',
        #                      Vars.cfg.data['cache_dir'])
        # self.config.load()

    def get_division_list(self):
        print(msg.m('get_div'), end='')
        response = HbookerAPI.Book.get_division_list(self.book_id)
        if response.get('code') == '100000':
            self.division_list = response['data']['division_list']
        else:
            print(msg.m('failed_get_div') + str(response))

    def show_division_list(self):
        print('\r', end='')
        for division in self.division_list:
            print(msg.m('show_div_index') + division['division_index'].rjust(3, " ") + msg.m('show_div_total') +
                  str(len(self.division_chapter_list[division['division_name']])).rjust(4, " ") +
                  msg.m('show_div_name') + division['division_name'])

    def get_chapter_catalog_get_thread(self, division):
        response = HbookerAPI.Book.get_chapter_update(division['division_id'])
        if response.get('code') == '100000':
            self.get_chapter_catalog_mt_dl_lock.acquire()
            self.chapter_list.extend(response['data']['chapter_list'])
            self.division_chapter_list[division['division_name']] = response['data']['chapter_list']
            self.get_chapter_catalog_mt_dl_lock.release()
        else:
            print(msg.m('failed_get_chap') + division['division_name'] + ": " + str(response))

    def get_chapter_catalog(self):
        print('正在獲取書籍目錄...')
        self.chapter_list.clear()
        download_threads = []
        for division in self.division_list:
            get_thread = threading.Thread(target=self.get_chapter_catalog_get_thread, args=(division,))
            download_threads.append(get_thread)
            get_thread.start()
        for get_thread in download_threads:
            get_thread.join()
        self.chapter_list.sort(key=lambda x: int(x['chapter_index']))
        print("\r", end="")

    def show_latest_chapter(self):
        print(msg.m('show_last_chap_s_index'), self.chapter_list[-1]['chapter_index'], msg.m('show_last_chap_uptime'),
              self.last_chapter_info['uptime'], msg.m('show_last_chap_name'), self.chapter_list[-1]['chapter_title'])

    def fix_illegal_book_name(self):
        return self.book_name.replace('<', '＜').replace('>', '＞').replace(':', '：').replace('"', '“') \
            .replace('/', '╱').replace('|', '｜').replace('?', '？').replace('*', '＊')

    def show_chapter_list_order_division(self):
        for division in self.division_list:
            chapter_order = 1
            print(msg.m('show_chap_list_index'), division['division_index'], ',:', division['division_name'])
            for chapter_info in self.division_chapter_list[division['division_name']]:
                print(' ' + chapter_info['chapter_index'] + ', ' + division['division_index'] + "-" +
                      str(chapter_order) + "-" + str(chapter_info['chapter_id']) + ' ' + division['division_name'] +
                      '：' + chapter_info['chapter_title'])
                chapter_order += 1

    def download_book_multi_thread(self):
        self.file_path = Vars.cfg.data['output_dir'] + self.fix_illegal_book_name() + '/' + \
                         self.fix_illegal_book_name() + '.epub '
        self.epub = EpubFile(self.file_path, Vars.cfg.data['cache_dir'] + self.fix_illegal_book_name(), self.book_id,
                             self.book_name,
                             self.author_name, use_old_epub=False)
        self.epub.set_cover(self.cover)
        threads = []
        # for every chapter in order of division
        for division in self.division_list:
            chapter_order = 1
            # print('分卷編號:', division['division_index'], ', 分卷名:', division['division_name'])
            for chapter_info in self.division_chapter_list[division['division_name']]:
                # print("ch_info_index: ", chapter_info['chapter_index'], " ch_info_id", chapter_info['chapter_id'])
                if chapter_info['is_valid'] == '0':
                    # 處理屏蔽章節
                    self.process_finished_count += 1
                    f_name = division['division_index'].rjust(4, "0") + '-' + str(chapter_order).rjust(6, "0") + '-' + \
                        chapter_info['chapter_id']
                    if os.path.exists(self.epub.tempdir + '/OEBPS/Text/' + f_name + '.xhtml'):
                        if os.path.getsize(self.epub.tempdir + '/OEBPS/Text/' + f_name + '.xhtml') == 0:
                            # self.add_download_finished_count()
                            print('\r' + chapter_info['chapter_index'].rjust(5, "0") + ', ' + division[
                                'division_index'].rjust(4, "0") + "-" +
                                  str(chapter_order).rjust(6, "0") + "-" + str(chapter_info['chapter_id']) +
                                  msg.m('dl_chap_block_e') + division['division_name'] + '：' + chapter_info[
                                      'chapter_title'] +
                                  "\n" + str(self.downloaded_count) + ' / ' + str(
                                self.process_finished_count) + " / " + str(
                                len(self.chapter_list)), end=' ')
                        else:
                            print('\r' + chapter_info['chapter_index'].rjust(5, "0") + ', ' + division[
                                'division_index'].rjust(4, "0") + "-" +
                                  str(chapter_order).rjust(6, "0") + "-" + str(chapter_info['chapter_id']) +
                                  msg.m('dl_chap_block_c') + division['division_name'] + '：' + chapter_info[
                                      'chapter_title'] +
                                  "\n" + str(self.downloaded_count) + ' / ' + str(
                                self.process_finished_count) + " / " + str(
                                len(self.chapter_list)), end=' ')
                    else:
                        # 如無檔案 建立空檔
                        with codecs.open(self.epub.tempdir + '/OEBPS/Text/' + f_name + '.xhtml', 'w', 'utf-8') as _file:
                            pass
                        print('\r' + chapter_info['chapter_index'].rjust(5, "0") + ', ' + division[
                            'division_index'].rjust(4, "0") + "-" +
                              str(chapter_order).rjust(6, "0") + "-" + str(chapter_info['chapter_id']) +
                              msg.m('dl_chap_block_e') + division['division_name'] + '：' + chapter_info[
                                  'chapter_title'] +
                              "\n" + str(self.downloaded_count) + ' / ' + str(
                            self.process_finished_count) + " / " + str(
                            len(self.chapter_list)), end=' ')

                elif chapter_info['auth_access'] == '0':
                    # 跳過未購買章節
                    self.process_finished_count += 1
                    print(
                        '\r' + chapter_info['chapter_index'].rjust(5, "0") + ', ' +
                        division['division_index'].rjust(4, "0") + '-' + str(chapter_order).rjust(6, "0") + '-' +
                        chapter_info['chapter_id'] + msg.m('dl_chap_not_paid') + division['division_name'] + '：' +
                        chapter_info['chapter_title'] + "\n" + str(self.downloaded_count) + ' / ' +
                        str(self.process_finished_count) + " / " + str(len(self.chapter_list)), end=' ')
                else:
                    download_thread = threading.Thread(target=self.download_book_get_chapter,
                                                       args=(chapter_info['chapter_index'], chapter_info['chapter_id'],
                                                             division['division_index'], chapter_order,))
                    threads.append(download_thread)
                    download_thread.start()
                chapter_order += 1
        for thread in threads:
            thread.join()
        print(msg.m('dl_fin'), end='')

        if self.downloaded_count == 0:
            if os.path.exists(self.epub.tempdir + '/OEBPS/Text'):
                text_mod_time = os.path.getmtime(self.epub.tempdir + '/OEBPS/Text')
            else:
                text_mod_time = 0
            if os.path.exists(Vars.cfg.data['output_dir'] + self.fix_illegal_book_name() + '/' + self.fix_illegal_book_name() + '.epub'):
                epub_mod_time = os.path.getmtime(
                    Vars.cfg.data['output_dir'] + self.fix_illegal_book_name() + '/' + self.fix_illegal_book_name() + '.epub')
            else:
                epub_mod_time = 0
            if text_mod_time >= epub_mod_time:
                print(msg.m('expo_s'), end='')
                if not os.path.isdir(Vars.cfg.data['output_dir'] + self.fix_illegal_book_name()):
                    os.makedirs(Vars.cfg.data['output_dir'] + self.fix_illegal_book_name())
                self.epub.make_cover_text(self.book_info['book_name'], self.book_info['author_name'],
                                          self.book_info['description'], self.book_info['uptime'])
                self.epub.download_book_write_chapter(self.division_chapter_list)
                # self.config.data['book_info'] = self.book_info
                # self.config.data['division_chapter_list'] = self.division_chapter_list
                # self.config.save()
                print(msg.m('expo_e'))
            else:
                print(msg.m('expo_no'))
        else:
            print(msg.m('expo_s'), end='')
            if not os.path.isdir(Vars.cfg.data['output_dir']):
                os.makedirs(Vars.cfg.data['output_dir'])
            if not os.path.isdir(Vars.cfg.data['output_dir'] + self.fix_illegal_book_name()):
                os.makedirs(Vars.cfg.data['output_dir'] + self.fix_illegal_book_name())
            self.epub.make_cover_text(self.book_info['book_name'], self.book_info['author_name'],
                                      self.book_info['description'], self.book_info['uptime'])
            self.epub.download_book_write_chapter(self.division_chapter_list)
            # self.config.data['book_info'] = self.book_info
            # self.config.data['division_chapter_list'] = self.division_chapter_list
            # self.config.save()
            print(msg.m('expo_e'))
        self.process_finished_count = 0
        self.downloaded_count = 0

    def download_book_get_chapter(self, chapter_index, chapter_id, division_index, chapter_order):
        division_name = None
        for division in self.division_list:
            if division['division_index'] == division_index:
                division_name = division['division_name']
        chapter_title = None
        if division_name is not None:
            chapter_title = self.division_chapter_list[division_name][chapter_order - 1]['chapter_title']
        f_name = division_index.rjust(4, "0") + '-' + str(chapter_order).rjust(6, "0") + '-' + chapter_id
        if os.path.exists(self.epub.tempdir + '/OEBPS/Text/' + f_name + '.xhtml'):
            if os.path.getsize(self.epub.tempdir + '/OEBPS/Text/' + f_name + '.xhtml') == 0:
                # 章節檔案大小為0 重新下載
                print('\r' + chapter_index.rjust(5, "0") + ', ' + division_index.rjust(4, "0") + "-" +
                      str(chapter_order).rjust(6, "0") + "-" + str(chapter_id) +
                      msg.m('dl_0_chap_re_dl') + division_name + '：' + chapter_title +
                      "\n" + str(self.downloaded_count) + ' / ' + str(self.process_finished_count) + " / " + str(
                    len(self.chapter_list)), end=' ')
            else:
                # 章節已經下載過 跳過
                self.add_process_finished_count()
                print('\r' + str(self.downloaded_count) + ' / ' + str(self.process_finished_count) + " / " + str(
                    len(self.chapter_list)), end=' ')
                self.get_chapter_catalog_mt_dl_lock.release()
                return True

        q_item = self.concurrent_download_queue.get()
        response = HbookerAPI.Chapter.get_chapter_command(chapter_id)
        if response.get('code') == '100000':
            chapter_command = response['data']['command']
            response2 = HbookerAPI.Chapter.get_cpt_ifm(chapter_id, chapter_command)
            self.concurrent_download_queue.put(q_item)
            if response2.get('code') == '100000' and response2['data']['chapter_info'].get('chapter_title') is not None:
                if response2['data']['chapter_info']['auth_access'] == '1':
                    content = HbookerAPI.CryptoUtil.decrypt(response2['data']['chapter_info']['txt_content'],
                                                            chapter_command).decode('utf-8')
                    if content.find('\n') + 1 < len(content):
                        content = content[content.find('\n') + 1:]
                        if content[-1] == '\n':
                            content = content[:-1]
                        content = content.replace('\n', '</p>\r\n<p>')
                    else:
                        content = ''
                    # 下載成功
                    author_say = response2['data']['chapter_info']['author_say'].replace('\r', '')
                    author_say = author_say.replace('\n', '</p>\r\n<p>')
                    self.epub.add_chapter(chapter_id, division_name,
                                          response2['data']['chapter_info']['chapter_title'], '<p>' + content +
                                          '</p>\r\n<p>' + author_say + '</p>', division_index, chapter_order)
                    self.add_process_finished_count()
                    self.downloaded_count += 1
                    print('\r' + str(self.downloaded_count) + ' / ' + str(self.process_finished_count) + " / " + str(
                        len(self.chapter_list)), end=' ')
                    self.get_chapter_catalog_mt_dl_lock.release()
                    return True
                else:
                    # 異常狀況，態異常，已訂閱但無法下載。
                    self.add_process_finished_count()
                    print('\r' + chapter_index.rjust(5, "0") + ', ' + division_index.rjust(4, "0") + '-' +
                          str(chapter_order).rjust(6, "0") + '-' + chapter_id + msg.m('dl_error_paid_stat_conflict') +
                          division_name + '：' + chapter_title + "\n" +
                          str(self.downloaded_count) + ' / ' + str(self.process_finished_count) + " / " + str(
                        len(self.chapter_list)), end=' ')
                    self.get_chapter_catalog_mt_dl_lock.release()
                    return False
            else:
                # 章節下載異常，請再次嘗試下載
                with codecs.open(self.epub.tempdir + '/OEBPS/Text/' + f_name + '.xhtml', 'w', 'utf-8') as _file:
                    pass
                self.add_process_finished_count()
                print('\r' + chapter_index.rjust(5, "0") + ', ' + division_index.rjust(4, "0") + '-' +
                      str(chapter_order).rjust(6, "0") + '-' + chapter_id +
                      msg.m('dl_error_chap_get_failed_1') + division_name + '：' + chapter_title + "\n" +
                      str(self.downloaded_count) + ' / ' + str(self.process_finished_count) + " / " + str(
                    len(self.chapter_list)), end=' ')
                self.get_chapter_catalog_mt_dl_lock.release()
                return True
        else:
            self.concurrent_download_queue.put(q_item)
            self.add_process_finished_count()
            print('\r' + chapter_index.rjust(5, "0") + ', ' + division_index.rjust(4, "0") + '-' +
                  str(chapter_order).rjust(6, "0") + '-' + chapter_id + msg.m('dl_error_chap_get_failed_2') +
                  division_name + '：' + chapter_title + "\n" +
                  str(self.downloaded_count) + ' / ' + str(self.process_finished_count) + " / " + str(
                len(self.chapter_list)), end=' ')
            self.get_chapter_catalog_mt_dl_lock.release()
            return False

    def add_process_finished_count(self):
        self.get_chapter_catalog_mt_dl_lock.acquire()
        self.process_finished_count += 1
