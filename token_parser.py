import xml.etree.cElementTree
import json


def token_from_novel_preferences_xml(file: str='com.kuangxiangciweimao.novel_preferences.xml'):
    # parse token and other user info from xml file used by com.kuangxiangciweimao.novel
    # the file can be found at
    # com.kuangxiangciweimao.novel\shared_prefs\com.kuangxiangciweimao.novel_preferences.xml
    logined_user = json.loads(xml.etree.cElementTree.parse(file).getroot().find('string[@name="LoginedUser"]').text)
    return {'reader_name': logined_user.get('readerInfo').get('reader_name'),
                 'user_code': logined_user.get('userCode'),
                 'account': logined_user.get('readerInfo').get('account'),
                 'login_token': logined_user.get('loginToken')}


def token_from_input(token: str = None, account: str = None):
    # used to input token and account manually
    data = {}
    if account is None:
        account = input('input account (例:书客123456789):')
    if token is None:
        token = input('input login_token (32 digit hex code):')
    return {'account': account, 'login_token': token}


if __name__ == '__main__':
    print(token_from_novel_preferences_xml())
    print(token_from_input())
