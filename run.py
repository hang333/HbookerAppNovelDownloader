from instance import *
from bookshelf import *
import sys
import re
import datetime
import HbookerAPI


def refresh_bookshelf_list():
    response = HbookerAPI.BookShelf.get_shelf_list()
    if response.get('code') == '100000':
        BookShelfList.clear()
        for shelf in response['data']['shelf_list']:
            BookShelfList.append(BookShelf(shelf))
    else:
        print("Error: " + str(response))
    for shelf in BookShelfList:
        shelf.show_info()
    if len(BookShelfList) == 1:
        shell_bookshelf(['', '1'])


def shell_login(inputs):
    if len(inputs) == 1 and Vars.cfg.data.get('user_account') is not None and \
            Vars.cfg.data.get('user_password') is not None:
        pass
    elif len(inputs) >= 3:
        Vars.cfg.data['user_account'] = inputs[1]
        Vars.cfg.data['user_password'] = inputs[2]
    else:
        print('請輸入正確的參數')
        return False

    response = HbookerAPI.SignUp.login(Vars.cfg.data['user_account'], Vars.cfg.data['user_password'])
    if response.get('code') == '100000':
        Vars.cfg.data['reader_name'] = response['data']['reader_info']['reader_name']
        Vars.cfg.data['user_code'] = response['data']['user_code']
        Vars.cfg.data['common_params'] = {'login_token': response['data']['login_token'],
                                          'account': response['data']['reader_info']['account']}
        Vars.cfg.save()
        HbookerAPI.set_common_params(Vars.cfg.data['common_params'])
        print('登錄成功, 用戶暱稱為: ', Vars.cfg.data['reader_name'])
        return True
    else:
        # print("response logon: " + str(response))
        print(response.get('tip'))
        return False


def shell_bookshelf(inputs):
    if len(inputs) >= 2:
        if not BookShelfList:
            refresh_bookshelf_list()
        Vars.current_bookshelf = get_bookshelf_by_index(inputs[1])
        if Vars.current_bookshelf is None:
            print('請輸入正確的參數')
        else:
            print('選擇書架: "' + Vars.current_bookshelf.shelf_name + '"')
            Vars.current_bookshelf.get_book_list()
            Vars.current_bookshelf.show_book_list()
    else:
        refresh_bookshelf_list()


def shell_books(inputs):
    if len(inputs) >= 2:
        Vars.current_book = None
        if Vars.current_bookshelf is not None:
            Vars.current_book = Vars.current_bookshelf.get_book(inputs[1])
            if Vars.current_book is not None:
                response = HbookerAPI.Book.get_info_by_id(Vars.current_book.book_id)
                if response.get('code') == '100000':
                    Vars.current_book = Book(None, response['data']['book_info'],
                                             max_concurrent_downloads=max_concurrent_downloads)
                else:
                    print('獲取書籍信息失敗, shelf_index:', inputs[1])
                    return
        if Vars.current_book is None:
            response = HbookerAPI.Book.get_info_by_id(inputs[1])
            if response.get('code') == '100000':
                # print(response['data']['book_info'])
                Vars.current_book = Book(None, response['data']['book_info'])
            else:
                print('獲取書籍信息失敗, book_id:', inputs[1])
                return

        print('《' + Vars.current_book.book_name + '》')
        Vars.current_book.get_division_list()
        Vars.current_book.get_chapter_catalog()
        if len(inputs) < 3:
            Vars.current_book.show_division_list()
            Vars.current_book.show_latest_chapter_()
    else:
        if Vars.current_book is not None:
            Vars.current_book.show_chapter_list_order_division()
        elif Vars.current_bookshelf is None:
            print('未選擇書架')
        else:
            Vars.current_bookshelf.get_book_list()
            Vars.current_bookshelf.show_book_list()


def shell_mtd(inputs):
    if len(inputs) > 1:
        shell_books(inputs)
    if Vars.current_book is None:
        print('未選擇書籍')
        return
    print('開始下載書籍...\n')
    Vars.current_book.download_book_multithreading()


def shell_mtd_list(inputs):
    if len(inputs) >= 2:
        list_file = inputs[1]
    else:
        list_file = 'list.txt'
    try:
        list_file_input = open(list_file, 'r', encoding='utf-8')
    except OSError:
        print(OSError)
        return
    list_lines = list_file_input.readlines()
    for line in list_lines:
        if re.match("^\\s*([0-9]+).*$", line):
            book_id = re.sub("^\\s*([0-9]{9}).*$\\n?", "\\1", line)
            print("Book ID: " + book_id + " ", end='')
            shell_mtd(['', book_id, ''])


def shell_download_shelf(inputs):
    if len(inputs) >= 2:
        shell_bookshelf(inputs)
    if Vars.current_bookshelf is not None:
        for book in Vars.current_bookshelf.BookList:
            shell_mtd(['', book.book_id])
    else:
        print('未選擇書架')


def check_in_today():

    if Vars.cfg.data.get('user_account') is None or Vars.cfg.data.get('user_account') == "" \
            or Vars.cfg.data.get('user_password') is None or Vars.cfg.data.get('user_password') == "":
        print("未登入，請先登入")
        return False

    today = str((datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=8)).date())
    check_in_records = HbookerAPI.CheckIn.get_check_in_records()
    if check_in_records.get('code') == '100000':
        for record in check_in_records['data']['sign_record_list']:
            if record['date'] == today:
                if record['is_signed'] == '0':
                    check_in = HbookerAPI.CheckIn.do_check_in()
                    if check_in.get('code') == '100000':
                        print('簽到成功, 獲得: ' + str(check_in['data']['bonus']['exp']) + ' 經驗, ' +
                              str(check_in['data']['bonus']['hlb']) + ' 代幣, ' +
                              str(check_in['data']['bonus']['recommend']) + ' 推薦票\n')
                        return True
                    elif check_in.get('code') == '340001':
                        print("任務已完成，請勿重複簽到\n")
                        return True
                    else:
                        print("簽到失敗:\n" + str(check_in) + '\n')
                        return False
                else:
                    print("已簽到\n")
                    return True
    elif check_in_records.get('code') == '200001':
        # {'code': '200001', 'tip': '缺少登录必需参数'}
        print("未登入，請先登入\n")
        return False
    elif check_in_records.get('code') == '200100':
        # {'code': '200100', 'tip': '登录状态过期，请重新登录'}
        print("登入過期或失效，自動嘗試重新登入")
        if shell_login(['']):
            print("成功重新登入，再次執行簽到")
            check_in_records = HbookerAPI.CheckIn.get_check_in_records()
            if check_in_records.get('code') == '100000':
                for record in check_in_records['data']['sign_record_list']:
                    if record['date'] == today:
                        if record['is_signed'] == '0':
                            check_in = HbookerAPI.CheckIn.do_check_in()
                            if check_in.get('code') == '100000':
                                print('簽到成功, 獲得: ' + str(check_in['data']['bonus']['exp']) + ' 經驗, ' +
                                      str(check_in['data']['bonus']['hlb']) + ' 代幣, ' +
                                      str(check_in['data']['bonus']['recommend']) + ' 推薦票\n')
                                return True
                            elif check_in.get('code') == '340001':
                                print("任務已完成，請勿重複簽到\n")
                                return True
                            else:
                                print("簽到失敗:\n" + str(check_in) + '\n')
                                return False
                        else:
                            print("已簽到\n")
                            return True
            else:
                print("簽到失敗，特殊原因，請手動處理:\n" + str(check_in_records) + '\n')
                return False
        else:
            print("重新登入失敗，請手動處理\n")
            return False
    else:
        print("簽到失敗，特殊原因，請手動處理:\n" + str(check_in_records) + '\n')
        return False


def agreed_read_readme():
    if Vars.cfg.data.get('agreed_to_readme') is None:
        print(
            "!!使用前請仔細閱讀README.md!!  !!使用前請仔細閱讀README.md!!\n\n!!使用前請仔細閱讀README.md!!  "
            "!使用前請仔細閱讀README.md!!\n\n!!使用前請仔細閱讀README.md!!  !!使用前請仔細閱讀README.md!!\n\n")
        print("是否以仔細閱讀且同意README.md中敘述事物\n如果兩者回答皆為\"是\"，請輸入英文 \"yes\" 後按Enter建，如果不同意請關閉此程式\n")

        confirm = get('>').strip()
        if confirm == 'yes':
            Vars.cfg.data['agreed_to_readme'] = 'yes'
            Vars.cfg.save()
        else:
            sys.exit()


def shell():
    if Vars.cfg.data.get('user_code') is not None:
        HbookerAPI.set_common_params(Vars.cfg.data['common_params'])

        if len(sys.argv) > 1:
            if str(sys.argv[1]).startswith('t'):
                if check_in_today():
                    sys.exit()
                else:
                    loop = True
                    inputs = []
            else:
                check_in_today()
                loop = False
                inputs = sys.argv[1:]
        else:
            check_in_today()
            loop = True
            print(Vars.help_info)
            refresh_bookshelf_list()
            inputs = re.split('\\s+', get('>').strip())
    else:
        loop = True
        save = False
        if Vars.cfg.data.get('user_account') is None or Vars.cfg.data.get('user_account') is not str:
            Vars.cfg.data['user_account'] = ""
            save = True
        if Vars.cfg.data.get('user_password') is None or Vars.cfg.data.get('user_password') is not str:
            Vars.cfg.data['user_password'] = ""
            save = True
        if save:
            Vars.cfg.save()

        print(Vars.help_info)
        print("未登入，請先登入")
        if len(sys.argv) > 1:
            inputs = sys.argv[1:]
        else:
            inputs = re.split('\\s+', get('>').strip())

    while True:
        if inputs[0].startswith('q'):
            sys.exit()
        elif inputs[0].startswith('l'):
            shell_login(inputs)
            check_in_today()
        elif inputs[0].startswith('s'):
            shell_bookshelf(inputs)
        elif inputs[0].startswith('b'):
            shell_books(inputs)
        elif inputs[0].startswith('ds') or inputs[0].startswith('downloads'):
            shell_download_shelf(inputs)
        elif inputs[0].startswith('d'):
            shell_mtd(inputs)
        elif inputs[0].startswith('u'):
            shell_mtd_list(inputs)
        elif inputs[0].startswith('t'):
            check_in_today()
        else:
            print(Vars.help_info)

        if loop is False:
            break
        inputs = re.split('\\s+', get('>').strip())


if __name__ == "__main__":
    Vars.cfg.load()

    agreed_read_readme()

    if type(Vars.cfg.data.get('max_concurrent_downloads')) is not int:
        Vars.cfg.data['max_concurrent_downloads'] = 32
        Vars.cfg.save()
        max_concurrent_downloads = 32
    else:
        max_concurrent_downloads = Vars.cfg.data.get('max_concurrent_downloads')

    shell()
