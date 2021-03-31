from HbookerAPI import HttpUtil, CryptoUtil, UrlConstants
import json

common_params = {'account': None, 'login_token': None, 'app_version': '2.7.039'}


def set_common_params(params):
    common_params.update(params)


def get(api_url, params=None, **kwargs):
    if params is None:
        params = common_params
    if params is not None:
        params.update(common_params)
    api_url = api_url.replace(UrlConstants.WEB_SITE, '')
    ret = json.loads(CryptoUtil.decrypt(HttpUtil.get(UrlConstants.WEB_SITE + api_url, params=params, **kwargs)))
    # print('GET', api_url)
    # print(params)
    # print(ret)
    return ret


def post(api_url, data=None, **kwargs):
    if data is None:
        data = common_params
    if data is not None:
        data.update(common_params)
    api_url = api_url.replace(UrlConstants.WEB_SITE, '')
    ret = json.loads(CryptoUtil.decrypt(HttpUtil.post(UrlConstants.WEB_SITE + api_url, data=data, **kwargs)))
    # print('POST', api_url)
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


class CheckIn:

    @staticmethod
    def get_check_in_records():
        response = get(UrlConstants.SIGN_RECORD, {})
        return response

    @staticmethod
    def do_check_in():
        response = get(UrlConstants.SING_RECORD_TASK, {'task_type': 1})
        return response
