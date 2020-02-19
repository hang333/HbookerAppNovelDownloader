import zipfile
import re
import os
import codecs
import urllib.request

nl = '\r\n'


def str_mid(string: str, left: str, right: str, start=None, end=None):
    pos1 = string.find(left, start, end)
    if pos1 > -1:
        pos2 = string.find(right, pos1 + len(left), end)
        if pos2 > -1:
            return string[pos1 + len(left): pos2]
    return ''


def getallfiles(dirpath: str):
    result = list()
    for _name in os.listdir(dirpath):
        if os.path.isdir(dirpath + '/' + _name):
            result.extend(getallfiles(dirpath + '/' + _name))
        else:
            result.append(dirpath + '/' + _name)
    return result


class EpubFile:
    _filepath = ''
    _tempdir = ''
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

    def __init__(self, filepath: str, tempdir: str, book_id: str, book_title: str, book_author: str):
        self._filepath = filepath
        self._tempdir = tempdir.replace("?","？")
        if not os.path.isdir(tempdir):
            os.makedirs(tempdir)
        _template = zipfile.ZipFile(os.getcwd() + "/template/template.epub")
        self._content_opf = bytes(_template.read('OEBPS/content.opf')).decode()
        self._chapter_format_manifest = str_mid(self._content_opf, '${chapter_format_manifest}={{{', '}}}')
        self._image_format_manifest = str_mid(self._content_opf, '${image_format_manifest}={{{', '}}}')
        self._chapter_format_spine = str_mid(self._content_opf, '${chapter_format_spine}={{{', '}}}')
        self._toc_ncx = bytes(_template.read('OEBPS/toc.ncx')).decode()
        self._chapter_format_navMap = str_mid(self._toc_ncx, '${chapter_format_navMap}={{{', '}}}')
        self._chapter_format = bytes(_template.read('OEBPS/Text/${chapter_format}.xhtml')).decode()
        if os.path.isfile(filepath):
            try:
                with zipfile.ZipFile(self._filepath, 'r', zipfile.ZIP_DEFLATED) as _file:
                    try:
                        self._content_opf = bytes(_file.read('OEBPS/content.opf')).decode()
                        self._toc_ncx = bytes(_file.read('OEBPS/toc.ncx')).decode()
                        _file.extractall(self._tempdir)
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
                    _template.extract(_name, self._tempdir)
            self._content_opf = re.sub(r'\${.*?}={{{[\S\s]*?}}}[\r\n]*', '', self._content_opf)
            self._toc_ncx = re.sub(r'\${.*?}={{{[\S\s]*?}}}[\r\n]*', '', self._toc_ncx)
            self._content_opf_manifest = str_mid(self._content_opf, '<manifest>', '</manifest>')
            self._content_opf_spine = str_mid(self._content_opf, '<spine toc="ncx">', '</spine>')
            self._toc_ncx_navMap = str_mid(self._toc_ncx, '<navMap>', '</navMap>')
            self._content_opf = self._content_opf.replace('${book_id}', book_id)
            self._content_opf = self._content_opf.replace('${book_title}', book_title)
            self._content_opf = self._content_opf.replace('${book_author}', book_author)
            self._toc_ncx = self._toc_ncx.replace('${book_id}', book_id)
            self._toc_ncx = self._toc_ncx.replace('${book_title}', book_title)
            self._toc_ncx = self._toc_ncx.replace('${book_author}', book_author)
            with codecs.open(self._tempdir + '/OEBPS/content.opf', 'w', 'utf-8') as _file:
                _file.write(self._content_opf)
            with codecs.open(self._tempdir + '/OEBPS/toc.ncx', 'w', 'utf-8') as _file:
                _file.write(self._toc_ncx)
        _template.close()

    def _add_manifest_chapter(self, chapter_id: str):
        if self._content_opf_manifest.find('id="' + chapter_id + '.xhtml"') == -1:
            _before = self._content_opf_manifest
            self._content_opf_manifest += self._chapter_format_manifest.replace('${chapter_id}', chapter_id) + nl
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
                                              .replace('${media_type}', _media_type) + nl
            self._content_opf = self._content_opf.replace(
                '<manifest>' + _before + '</manifest>',
                '<manifest>' + self._content_opf_manifest + '</manifest>', 1)

    def _add_spine(self, chapter_id: str):
        if self._content_opf_spine.find('idref="' + chapter_id + '.xhtml"') == -1:
            _before = self._content_opf_spine
            self._content_opf_spine += self._chapter_format_spine.replace('${chapter_id}', chapter_id) + nl
            self._content_opf = self._content_opf.replace(
                '<spine toc="ncx">' + _before + '</spine>',
                '<spine toc="ncx">' + self._content_opf_spine + '</spine>', 1)

    def _add_navMap(self, chapter_index: str, chapter_id: str, chapter_title: str):
        if self._toc_ncx_navMap.find('id="' + chapter_id) == -1:
            _before = self._toc_ncx_navMap
            self._toc_ncx_navMap += self._chapter_format_navMap.replace('${chapter_id}', chapter_id) \
                                        .replace('${chapter_index}', chapter_index) \
                                        .replace('${chapter_title}', chapter_title) + nl
            self._toc_ncx = self._toc_ncx.replace(
                '<navMap>' + _before + '</navMap>',
                '<navMap>' + self._toc_ncx_navMap + '</navMap>', 1)

    def _save(self):
        with codecs.open(self._tempdir + '/OEBPS/content.opf', 'w', 'utf-8') as _file:
            _file.write(self._content_opf)
        with codecs.open(self._tempdir + '/OEBPS/toc.ncx', 'w', 'utf-8') as _file:
            _file.write(self._toc_ncx)

    def setcover(self, url: str):
        urllib.request.urlretrieve(url, self._tempdir + '/OEBPS/Images/cover.jpg')

    def addchapter(self, chapter_index: str, chapter_id: str, chapter_title: str, chapter_content: str):
        with codecs.open(self._tempdir + '/OEBPS/Text/' + chapter_id + '.xhtml', 'w', 'utf-8') as _file:
            _data = self._chapter_format.replace('${chapter_title}', chapter_title) \
                .replace('${chapter_content}', '<h3>' + chapter_title + '</h3>' + nl + chapter_content)
            for _img in re.findall(r'<img src="http.*?>', _data):
                _img = _img.replace('>', ' />')
                _src = str_mid(_img, '<img src="', '"')
                if _src.rfind('/') == -1:
                    continue
                _filename = _src[_src.rfind('/') + 1:]
                self.addimage(_filename, _src)
                _data = _data.replace(_src, '../Images/' + _filename)
            _file.write(_data)
        self._add_manifest_chapter(chapter_id)
        self._add_spine(chapter_id)
        self._add_navMap(chapter_index, chapter_id, chapter_title)

    def addimage(self, filename: str, url: str):
        try:
            urllib.request.urlretrieve(url, self._tempdir + '/OEBPS/Images/' + filename)
        except (KeyboardInterrupt, InterruptedError) as _e:
            raise _e
        except Exception as _e:
            print("[ERROR]", _e)
            print("下载插图时出现错误，已跳过")
            with open(self._tempdir + '/OEBPS/Images/' + filename, 'wb'):
                pass
        self._add_manifest_image(filename)

    def addimagechapter(self, chapter_index: str, chapter_id: str, chapter_title: str, image: bytes):
        self.addchapter(chapter_index, chapter_id, chapter_title,
                        '<img src="../Images/' + chapter_id + '.png" alt=\'' + chapter_title + '\' />')
        with open(self._tempdir + '/OEBPS/Images/' + chapter_id + '.png', 'wb') as _file:
            _file.write(image)
        self._add_manifest_image(chapter_id + '.png')

    def fixchapter(self, chapter_id: str, chapter_title: str, chapter_content: str):
        with codecs.open(self._tempdir + '/OEBPS/Text/' + chapter_id + '.xhtml', 'w', 'utf-8') as _file:
            _data = self._chapter_format.replace('${chapter_title}', chapter_title) \
                .replace('${chapter_content}', chapter_content)
            for _img in re.findall(r'<img src="http.*?>', _data):
                _img = _img.replace('>', ' />')
                _src = str_mid(_img, '<img src="', '"')
                if _src.rfind('/') == -1:
                    continue
                _filename = _src[_src.rfind('/') + 1:]
                _data = _data.replace(_src, '../Images/' + _filename)
            _file.write(_data)

    def fiximagechapter(self, chapter_id: str, chapter_title: str, image: bytes):
        self.fixchapter(chapter_id, chapter_title,
                        '<img src="../Images/' + chapter_id + '.png" alt=\'' + chapter_title + '\' />')
        with open(self._tempdir + '/OEBPS/Images/' + chapter_id + '.png', 'wb') as _file:
            _file.write(image)
        self._add_manifest_image(chapter_id + '.png')

    def export(self):
        self._save()
        with zipfile.ZipFile(self._filepath, 'w', zipfile.ZIP_DEFLATED) as _file:
            _result = getallfiles(self._tempdir)
            for _name in _result:
                _file.write(_name, _name.replace(self._tempdir + '/', ''))

    def export_txt(self):
        self._save()
        with codecs.open(self._filepath.replace('.epub', '.txt'), 'w', 'utf-8') as _file:
            for _name in sorted(os.listdir(self._tempdir + '/OEBPS/Text')):
                if _name.find('$') > -1 or _name == 'cover.xhtml':
                    continue
                with codecs.open(self._tempdir + '/OEBPS/Text/' + _name, 'r', 'utf-8') as _file_xhtml:
                    _data_chapter = re.sub(r'<h3>.*?</h3>', '', str(_file_xhtml.read()))
                for _a in re.findall(r'<a href=.*?>章节链接</a>', _data_chapter):
                    _data_chapter = _data_chapter.replace(_a, '章节链接:' + str_mid(_a, '<a href="', '"'))
                for _img in re.findall(r'<img src=.*?>', _data_chapter):
                    _data_chapter = _data_chapter.replace(_img, '图片:"' + str_mid(_img, "alt='", "'") + '",' +
                                                          '位置:"' + str_mid(_img, '<img src="', '"')
                                                          .replace('../', '') + '"')
                _data_chapter = re.sub(r'</?[\S\s]*?>', '', _data_chapter)
                _data_chapter = re.sub(r'[\r\n]+', nl * 2, _data_chapter)
                _file.write(_data_chapter + nl)
