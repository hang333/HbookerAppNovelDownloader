from datetime import datetime
from shutil import copyfile
from instance import *
import urllib.request
import zipfile
import codecs
import time
import msg
import os
import re

image_get_retry = 10
image_download_display_delay = 1
last_image_dl_start_time = None


def str_mid(string: str, left: str, right: str, start=None, end=None):
    pos1 = string.find(left, start, end)
    if pos1 > -1:
        pos2 = string.find(right, pos1 + len(left), end)
        if pos2 > -1:
            return string[pos1 + len(left): pos2]
    return ''


def get_all_files(dir_path: str):
    result = list()
    for _name in os.listdir(dir_path):
        if os.path.isdir(dir_path + '/' + _name):
            result.extend(get_all_files(dir_path + '/' + _name))
        else:
            result.append(dir_path + '/' + _name)
    return result


def text_to_html_element_escape(text: str):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def html_element_to_text_unescape(element: str):
    return element.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')


def backup_copy_add_suffix_if_exists_add_index(file_path: str, suffix: str):
    # fix_illegal_book_name_dir
    backup_dir = os.path.join(Vars.cfg.data['backup_dir'], re.sub('^(.+)\\.\\s*$', '\\1．',
                                                                  os.path.splitext(os.path.basename(file_path))[0]))
    file_basename = os.path.splitext(os.path.basename(file_path))[0] + ' ' + suffix
    file_ext = os.path.splitext(file_path)[1]
    if not os.path.isdir(backup_dir):
        os.makedirs(backup_dir)
    if os.path.exists(file_path):
        if os.path.exists(os.path.join(backup_dir, file_basename) + file_ext):
            index = 1
            while os.path.exists(os.path.join(backup_dir, file_basename) + ' ' + str(index) + file_ext):
                index += 1
            copyfile(file_path, os.path.join(backup_dir, file_basename) + ' ' + str(index) + file_ext)
        else:
            copyfile(file_path, os.path.join(backup_dir, file_basename) + file_ext)
    else:
        # 出現錯誤
        print("error: file dose not exists: " + file_path)


def download_progress_reporthook(count, block_size, total_size):
    # this prints the image downloading progress
    # this is to show that the script is working
    # the timer is "not thread" safe, but working as intended
    # the timer is reset every time when a new download is triggered
    # it will print the progress if it's taking too long
    global last_image_dl_start_time
    if count == 0:
        last_image_dl_start_time = time.time()
        return
    duration = time.time() - last_image_dl_start_time
    if duration < image_download_display_delay:
        return
    progress_size = int(count * block_size)
    percent = int(progress_size * 100 / total_size)
    print("\rDownloading Image... %d%%, %d KB" % (percent, progress_size / 1024), end='')


class EpubFile:
    _filepath = ''
    tempdir = ''
    _content_opf = ''
    _content_opf_manifest = ''
    _content_opf_spine = ''
    _chapter_format_manifest = ''
    _image_format_manifest = ''
    _chapter_format_spine = ''
    _toc_ncx = ''
    _toc_ncx_navMap = ''
    _chapter_format_navMap = ''
    _chapter_format = ''

    def __init__(self, filepath: str, tempdir: str, book_id: str, book_title: str, book_author: str, use_old_epub=True):
        self._filepath = filepath
        self.tempdir = tempdir
        if not os.path.isdir(tempdir):
            os.makedirs(tempdir)
        _template = zipfile.ZipFile(os.path.abspath(os.path.join(os.path.dirname(__file__), 'template.epub')))
        self.cover_template = bytes(_template.read('OEBPS/Text/cover.xhtml')).decode()
        self._content_opf = bytes(_template.read('OEBPS/content.opf')).decode()
        self._chapter_format_manifest = str_mid(self._content_opf, '${chapter_format_manifest}={{{', '}}}')
        self._image_format_manifest = str_mid(self._content_opf, '${image_format_manifest}={{{', '}}}')
        self._chapter_format_spine = str_mid(self._content_opf, '${chapter_format_spine}={{{', '}}}')
        self._toc_ncx = bytes(_template.read('OEBPS/toc.ncx')).decode()
        self._chapter_format_navMap = str_mid(self._toc_ncx, '${chapter_format_navMap}={{{', '}}}')
        self._chapter_format = bytes(_template.read('OEBPS/Text/${chapter_format}.xhtml')).decode()
        if os.path.isfile(filepath) and use_old_epub:
            try:
                with zipfile.ZipFile(self._filepath, 'r', zipfile.ZIP_DEFLATED) as _file:
                    try:
                        self._content_opf = bytes(_file.read('OEBPS/content.opf')).decode()
                        self._toc_ncx = bytes(_file.read('OEBPS/toc.ncx')).decode()
                        _file.extractall(self.tempdir)
                    except (KeyError, NameError, IOError):
                        self._content_opf = bytes(_template.read('OEBPS/content.opf')).decode()
                        self._toc_ncx = bytes(_template.read('OEBPS/toc.ncx')).decode()
                    finally:
                        self._content_opf_manifest = str_mid(self._content_opf, '<manifest>', '</manifest>')
                        self._content_opf_spine = str_mid(self._content_opf, '<spine toc="ncx">', '</spine>')
                        self._toc_ncx_navMap = str_mid(self._toc_ncx, '<navMap>', '</navMap>')
                        _init = False
            except zipfile.BadZipFile:
                _init = True
        else:
            _init = True
        if _init:
            for _name in _template.namelist():
                if _name.find('$') == -1:
                    if not os.path.exists(tempdir + '/' + _name):
                        _template.extract(_name, self.tempdir)
            self._content_opf = re.sub(r'\${.*?}={{{[\S\s]*?}}}[\r\n]*', '', self._content_opf)
            self._toc_ncx = re.sub(r'\${.*?}={{{[\S\s]*?}}}[\r\n]*', '', self._toc_ncx)
            self._content_opf_manifest = str_mid(self._content_opf, '<manifest>', '</manifest>')
            self._content_opf_spine = str_mid(self._content_opf, '<spine toc="ncx">', '</spine>')
            self._toc_ncx_navMap = str_mid(self._toc_ncx, '<navMap>', '</navMap>')
            self._content_opf = self._content_opf.replace('${book_id}', book_id)
            self._content_opf = self._content_opf.replace('${book_title}', text_to_html_element_escape(book_title))
            self._content_opf = self._content_opf.replace('${book_author}', text_to_html_element_escape(book_author))
            self._toc_ncx = self._toc_ncx.replace('${book_id}', book_id)
            self._toc_ncx = self._toc_ncx.replace('${book_title}', text_to_html_element_escape(book_title))
            self._toc_ncx = self._toc_ncx.replace('${book_author}', text_to_html_element_escape(book_author))
        _template.close()

    def _add_manifest_chapter(self, chapter_id: str):
        if self._content_opf_manifest.find('id="' + chapter_id + '.xhtml"') == -1:
            _before = self._content_opf_manifest
            self._content_opf_manifest += self._chapter_format_manifest.replace('${chapter_id}', chapter_id) + '\r\n'
            self._content_opf = self._content_opf.replace(
                '<manifest>' + _before + '</manifest>',
                '<manifest>' + self._content_opf_manifest + '</manifest>', 1)

    def _add_manifest_image(self, filename: str):
        if self._content_opf_manifest.find('id="' + filename + '"') == -1:
            _before = self._content_opf_manifest
            if filename.endswith('.png'):
                _media_type = 'image/png'
            else:
                _media_type = 'image/jpeg'
            self._content_opf_manifest += self._image_format_manifest.replace('${filename}', filename) \
                                              .replace('${media_type}', _media_type) + '\r\n'
            self._content_opf = self._content_opf.replace(
                '<manifest>' + _before + '</manifest>',
                '<manifest>' + self._content_opf_manifest + '</manifest>', 1)

    def _add_spine(self, chapter_id: str):
        # noinspection SpellCheckingInspection
        if self._content_opf_spine.find('idref="' + chapter_id + '.xhtml"') == -1:
            _before = self._content_opf_spine
            self._content_opf_spine += self._chapter_format_spine.replace('${chapter_id}', chapter_id) + '\r\n'
            self._content_opf = self._content_opf.replace(
                '<spine toc="ncx">' + _before + '</spine>',
                '<spine toc="ncx">' + self._content_opf_spine + '</spine>', 1)

    def add_nav_map(self, chapter_index: str, chapter_id: str, chapter_title: str):
        if self._toc_ncx_navMap.find('id="' + chapter_id) == -1:
            _before = self._toc_ncx_navMap
            self._toc_ncx_navMap += self._chapter_format_navMap.replace('${chapter_id}', chapter_id) \
                                        .replace('${chapter_index}', chapter_index) \
                                        .replace('${chapter_title}', chapter_title) + '\r\n'
            self._toc_ncx = self._toc_ncx.replace(
                '<navMap>' + _before + '</navMap>',
                '<navMap>' + self._toc_ncx_navMap + '</navMap>', 1)

    def _save(self):
        with codecs.open(self.tempdir + '/OEBPS/content.opf', 'w', 'utf-8') as _file:
            _file.write(self._content_opf)
        with codecs.open(self.tempdir + '/OEBPS/toc.ncx', 'w', 'utf-8') as _file:
            _file.write(self._toc_ncx)

    def set_cover(self, url: str):
        image_path = self.tempdir + '/OEBPS/Images/' + url[url.rfind('/') + 1:]
        if os.path.exists(image_path):
            if os.path.getsize(image_path) != 0:
                return
        for retry in range(image_get_retry):
            try:
                urllib.request.urlretrieve(url, image_path, download_progress_reporthook)
                copyfile(image_path, self.tempdir + '/OEBPS/Images/cover.jpg')
                return
            except OSError as e:
                if retry != image_get_retry - 1:
                    print(msg.m('cover_dl_rt') + str(retry + 1) + ' / ' + str(image_get_retry) + ', ' + str(e) + '\n' +
                          url)
                    time.sleep(0.5 * retry)
                else:
                    print(msg.m('cover_dl_f') + str(e) + '\n' + url)
                    with open(image_path, 'wb'):
                        pass

    def export(self):
        self._save()
        with zipfile.ZipFile(self._filepath, 'w', zipfile.ZIP_DEFLATED) as _file:
            _result = get_all_files(self.tempdir)
            counter = 0
            for _name in _result:
                _file.write(_name, _name.replace(self.tempdir + '/', ''))
                counter += 1
                print('\r' + str(counter) + ' / ' + str(len(_result)), end='')

    def add_image(self, filename: str, url: str):
        image_path = self.tempdir + '/OEBPS/Images/' + filename
        if os.path.exists(image_path):
            if os.path.getsize(image_path) != 0:
                return
        for retry in range(image_get_retry):
            try:
                urllib.request.urlretrieve(url, image_path, download_progress_reporthook)
                return
            except OSError as e:
                if retry != image_get_retry - 1:
                    print(msg.m('image_dl_rt') + str(retry + 1) + ' / ' + str(image_get_retry) + ', ' + str(e) + '\n' +
                          url)
                    time.sleep(0.5 * retry)
                else:
                    print(msg.m('image_dl_f') + str(e) + '\n' + url)
                    with open(image_path, 'wb'):
                        pass

    def add_chapter(self, chapter_id: str, division_name: str, chapter_title: str, chapter_content: str,
                    division_index, chapter_order):
        f_name = division_index.rjust(4, "0") + '-' + str(chapter_order).rjust(6, "0") + '-' + chapter_id
        _data = self._chapter_format.replace(
            '<title>${chapter_title}</title>', '<title>' + text_to_html_element_escape(division_name) + ' : ' +
                                               text_to_html_element_escape(chapter_title) + '</title>') \
            .replace('${chapter_content}', '<h3>' + text_to_html_element_escape(chapter_title) + '</h3>\r\n' +
                     chapter_content)
        # 改動插圖連結辨識方式，以適應另一種連結的結構
        for _img in re.findall(r'<img .*src="http.*?>', _data):
            _img = _img.replace('>', ' />')
            _src = str_mid(_img, 'src="', '"')
            if _src.rfind('/') == -1:
                continue
            filename = _src[_src.rfind('/') + 1:]
            self.add_image(filename, _src)
            _data = _data.replace(_src, '../Images/' + filename)
            _data = re.sub(
                f"(<img *src=[\"\']\\.\\./Images/{filename}[\"\'] *alt=[\"\'][^\"^\']+[\"\'] *)(?!( ))(?!(/>))[/>]?",
                "\\1/>", _data)
            _data = re.sub(
                f"(<img *alt=[\"\'][^\"^\']+[\"\'] *src=[\"\']\\.\\./Images/{filename}[\"\'] *)(?!( ))(?!(/>))[/>]?",
                "\\1/>", _data)
        with codecs.open(self.tempdir + '/OEBPS/Text/' + f_name + '.xhtml', 'w', 'utf-8') as _file:
            _file.write(_data)

    def download_book_write_chapter(self, division_chapter_list):
        order_count = 2
        with codecs.open(os.path.splitext(self._filepath)[0] + ".txt", 'w', 'utf-8') as _file:
            with codecs.open(self.tempdir + '/OEBPS/Text/cover.xhtml', 'r', 'utf-8') as _cover_xhtml:
                cover = str(_cover_xhtml.read())
                cover = str_mid(cover, '<h1>', '</body>')
                cover = cover.replace('</h1>', '').replace('<h2>', '').replace('</h2>', '').replace('<h3>', ''). \
                    replace('</h3>', '').replace('<p>', '').replace('</p>', '')
                cover = html_element_to_text_unescape(cover)
                _file.write(cover + '\r\n')
            for filename in sorted(os.listdir(self.tempdir + '/OEBPS/Text/')):
                if filename.find('$') > -1 or filename == 'cover.xhtml':
                    continue
                f_name = os.path.splitext(filename)[0]
                self._add_manifest_chapter(f_name)
                self._add_spine(f_name)
                with codecs.open(self.tempdir + '/OEBPS/Text/' + filename, 'r', 'utf-8') as _file_xhtml:
                    _data_chapter = re.sub(r'<h3>.*?</h3>', '', _file_xhtml.read())
                division_and_chapter_file = str_mid(_data_chapter, "<title>", "</title>")
                if division_and_chapter_file == '':
                    division_name = ''
                    chapter_title = ''
                    for division_list_name in division_chapter_list:
                        for chapter in division_chapter_list[division_list_name]:
                            if chapter['chapter_id'] == os.path.splitext(filename)[0].split("-")[2]:
                                division_name = division_list_name
                                chapter_title = chapter['chapter_title']
                                break
                        else:
                            continue
                        break
                    if division_name == '' and chapter_title == '':
                        division_and_chapter_file = text_to_html_element_escape(filename)
                    else:
                        division_and_chapter_file = text_to_html_element_escape(division_name + ' : ' + chapter_title)
                self.add_nav_map(str(order_count), f_name, division_and_chapter_file)
                for _a in re.findall(r'<a href=.*?>章节链接</a>', _data_chapter):
                    _data_chapter = _data_chapter.replace(_a, '章节链接:' + str_mid(_a, '<a href="', '"'))
                for _img in re.findall(r'<img src=.*?>', _data_chapter):
                    _data_chapter = _data_chapter.replace(_img, '图片:"' + str_mid(_img, "alt='", "'") + '",' + '位置:"'
                                                          + str_mid(_img, '<img src="', '"').replace('../', '') + '"')
                _data_chapter = re.sub(r'</?[\S\s]*?>', '', _data_chapter)
                _data_chapter = re.sub(r'[\r\n]+', '\r\n\r\n', _data_chapter)
                _data_chapter = html_element_to_text_unescape(_data_chapter)
                _file.write(_data_chapter)
                order_count += 1
            for filename in sorted(os.listdir(self.tempdir + '/OEBPS/Images/')):
                self._add_manifest_image(filename)
        self.export()
        self.make_backup()

    def make_backup(self):
        if Vars.cfg.data['do_backup']:
            date = str(datetime.now().date())
            backup_copy_add_suffix_if_exists_add_index(self._filepath, date)
            backup_copy_add_suffix_if_exists_add_index(os.path.splitext(self._filepath)[0] + '.txt', date)

    def make_cover_text(self, book_name: str, author_name: str, book_description: str, update_time: str, book_id: str):
        text = '<h1>' + text_to_html_element_escape(book_name) + '</h1>\r\n<h2>作者: ' + \
               text_to_html_element_escape(author_name) + '</h2>\r\n<h3>更新時間: ' + update_time + \
               '</h3>\r\n<h3>Book ID: ' + book_id + '</h3>\r\n<h3>簡介:</h3>\r\n<p>' + \
            re.sub('\r\n', '</p>\r\n<p>', text_to_html_element_escape(book_description) + '</p>')
        text = re.sub('</body>\r\n</html>', text + '\r\n</body>\r\n</html>', self.cover_template)
        with codecs.open(self.tempdir + '/OEBPS/Text/cover.xhtml', 'w', 'utf-8') as _file:
            _file.write(text)
