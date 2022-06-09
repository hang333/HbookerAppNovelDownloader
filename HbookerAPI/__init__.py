from HbookerAPI import HttpUtil, CryptoUtil, UrlConstants
import json

# 某些帳號要'device_token': 'ciweimao_'才能登入
common_params = {'account': None, 'login_token': None, 'app_version': '2.7.039'}
# common_params = {'account': None, 'login_token': None, 'app_version': '2.9.290', 'device_token': 'ciweimao_'}


def set_common_params(params):
    common_params.update(params)


def get(api_url, params=None, **kwargs):
    if params is None:
        params = common_params
    if params is not None:
        params.update(common_params)
    api_url = api_url.replace(UrlConstants.WEB_SITE, '')
    try:
        return json.loads(CryptoUtil.decrypt(HttpUtil.get(UrlConstants.WEB_SITE + api_url, params=params, **kwargs)))
    except Exception as error:
        print("post error:", error)


def post(api_url, data=None, **kwargs):
    if data is None:
        data = common_params
    if data is not None:
        data.update(common_params)
    api_url = api_url.replace(UrlConstants.WEB_SITE, '')
    try:
        return json.loads(CryptoUtil.decrypt(HttpUtil.post(UrlConstants.WEB_SITE + api_url, data=data, **kwargs)))
    except Exception as error:
        print("post error:", error)


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
    def get_updated_chapter_by_division_new(book_id: str):
        return get(UrlConstants.GET_DIVISION_LIST_NEW, {'book_id': book_id})

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
        return get(UrlConstants.GET_CHAPTER_COMMAND, data)

    @staticmethod
    def get_cpt_ifm(chapter_id, chapter_command):
        data = {'chapter_id': chapter_id, 'chapter_command': chapter_command}
        return get(UrlConstants.GET_CPT_IFM, data)


class CheckIn:
    @staticmethod
    def get_check_in_records():
        return get(UrlConstants.SIGN_RECORD, {})

    @staticmethod
    def do_check_in():
        return get(UrlConstants.SING_RECORD_TASK, {'task_type': 1})


class CheckAppVersion:
    @staticmethod
    def get_version():
        return get(UrlConstants.MY_SETTING_UPDATE)
