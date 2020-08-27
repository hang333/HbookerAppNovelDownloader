from HbookerAPI import HttpUtil, CryptoUtil, UrlConstants
import json

commonparams = {'account': None, 'login_token': None, 'app_version': '2.6.011'}


def setcommonparams(params):
    commonparams.update(params)


def get(apiurl, params=commonparams, **kwargs):
    if params is not None:
        params.update(commonparams)
    apiurl = apiurl.replace(UrlConstants.WEB_SITE, '')
    ret = json.loads(CryptoUtil.decrypt(HttpUtil.get(UrlConstants.WEB_SITE + apiurl, params=params, **kwargs)))
    # print('GET', apiurl)
    # print(params)
    # print(ret)
    return ret


def post(apiurl, data=commonparams, **kwargs):
    if data is not None:
        data.update(commonparams)
    apiurl = apiurl.replace(UrlConstants.WEB_SITE, '')
    ret = json.loads(CryptoUtil.decrypt(HttpUtil.post(UrlConstants.WEB_SITE + apiurl, data=data, **kwargs)))
    # print('POST', apiurl)
    # print(data)
    # print(ret)
    return ret


class SignUp:
    @staticmethod
    def login(login_name, passwd):
        data = {'login_name': login_name, 'passwd': passwd}
        return post(UrlConstants.MY_SIGN_LOGIN, data)


class BookShelf:
    @staticmethod
    def get_shelf_list():
        return post(UrlConstants.BOOKSHELF_GET_SHELF_LIST)

    @staticmethod
    def get_shelf_book_list(shelf_id, last_mod_time='0', direction='prev'):
        data = {'shelf_id': shelf_id, 'last_mod_time': last_mod_time, 'direction': direction}
        return post(UrlConstants.BOOKSHELF_GET_SHELF_BOOK_LIST, data)


class Book:
    @staticmethod
    def get_division_list(book_id):
        data = {'book_id': book_id}
        return get(UrlConstants.GET_DIVISION_LIST, data)

    @staticmethod
    def get_chapter_update(division_id, last_update_time='0'):
        data = {'division_id': division_id, 'last_update_time': last_update_time}
        return post(UrlConstants.GET_CHAPTER_UPDATE, data)

    @staticmethod
    def get_info_by_id(book_id):
        data = {'book_id': book_id, 'recommend': '', 'carousel_position': '', 'tab_type': '', 'module_id': ''}
        return post(UrlConstants.BOOK_GET_INFO_BY_ID, data)


class Chapter:
    @staticmethod
    def get_chapter_command(chapter_id):
        data = {'chapter_id': chapter_id}
        return get('chapter/get_chapter_command', data)

    @staticmethod
    def get_cpt_ifm(chapter_id, chapter_command):
        data = {'chapter_id': chapter_id, 'chapter_command': chapter_command}
        return get('chapter/get_cpt_ifm', data)
