from bookshelf import *
from instance import *
import HbookerAPI
import datetime
import msg
import sys
import re


def refresh_bookshelf_list():
    response = HbookerAPI.BookShelf.get_shelf_list()
    if response.get('code') == '100000':
        BookShelfList.clear()
        for shelf in response['data']['shelf_list']:
            BookShelfList.append(BookShelf(shelf))
    else:
        print(msg.m('error_response') + str(response))
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
        print(msg.m('input_correct_var'))
        return False
    response = HbookerAPI.SignUp.login(Vars.cfg.data['user_account'], Vars.cfg.data['user_password'])
    if response.get('code') == '100000':
        Vars.cfg.data['reader_name'] = response['data']['reader_info']['reader_name']
        Vars.cfg.data['user_code'] = response['data']['user_code']
        Vars.cfg.data['common_params'] = {'login_token': response['data']['login_token'],
                                          'account': response['data']['reader_info']['account']}
        Vars.cfg.save()
        HbookerAPI.set_common_params(Vars.cfg.data['common_params'])
        print(msg.m('login_success_user') + Vars.cfg.data['reader_name'])
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
            print(msg.m('input_correct_var'))
        else:
            print(msg.m('picked_shelf_s') + Vars.current_bookshelf.shelf_name + msg.m('picked_shelf_e'))
            Vars.current_bookshelf.get_book_list()
            Vars.current_bookshelf.show_book_list()
    else:
        refresh_bookshelf_list()


def shell_select_books(inputs):
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
                    print(msg.m('failed_get_book_info_index'), inputs[1])
                    return
        if Vars.current_book is None:
            response = HbookerAPI.Book.get_info_by_id(inputs[1])
            if response.get('code') == '100000':
                # print(response['data']['book_info'])
                Vars.current_book = Book(None, response['data']['book_info'])
            else:
                print(msg.m('failed_get_book_info_id'), inputs[1])
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
            print(msg.m('not_picked_shelf'))
        else:
            Vars.current_bookshelf.get_book_list()
            Vars.current_bookshelf.show_book_list()


def shell_download_book(inputs):
    if len(inputs) > 1:
        shell_select_books(inputs)
    if Vars.current_book is None:
        print(msg.m('not_picked_book'))
        return
    print(msg.m('start_book_dl'))
    Vars.current_book.download_book_multi_thread()


def shell_download_list(inputs):
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
        if re.match("^\\s*([0-9]{9}).*$", line):
            book_id = re.sub("^\\s*([0-9]{9}).*$\\n?", "\\1", line)
            print("Book ID: " + book_id + " ", end='')
            shell_download_book(['', book_id, ''])


def shell_download_shelf(inputs):
    if len(inputs) >= 2:
        shell_bookshelf(inputs)
    if Vars.current_bookshelf is not None:
        for book in Vars.current_bookshelf.BookList:
            shell_download_book(['', book.book_id])
    else:
        print(msg.m('not_picked_shelf'))


def check_in_today():
    if Vars.cfg.data.get('user_account') is None or Vars.cfg.data.get('user_account') == "" \
            or Vars.cfg.data.get('user_password') is None or Vars.cfg.data.get('user_password') == "":
        print(msg.m('not_login_pl_login'))
        return False
    check_in_records = HbookerAPI.CheckIn.get_check_in_records()
    if check_in_records.get('code') == '100000':
        if check_in_today_do(check_in_records):
            return True
        else:
            return False
    elif check_in_records.get('code') == '200001':
        # {'code': '200001', 'tip': '缺少登录必需参数'}
        print(msg.m('not_login_pl_login'))
        return False
    elif check_in_records.get('code') == '200100':
        # {'code': '200100', 'tip': '登录状态过期，请重新登录'}
        print(msg.m('check_in_token_failed'))
        if shell_login(['']):
            print(msg.m('check_in_re_login_retry_check_in'))
            check_in_records = HbookerAPI.CheckIn.get_check_in_records()
            if check_in_records.get('code') == '100000':
                if check_in_today_do(check_in_records):
                    return True
                else:
                    return False
            else:
                print(msg.m('check_in_error_1') + str(check_in_records) + '\n')
                return False
        else:
            print(msg.m('check_in_re_login_failed'))
            return False
    else:
        print(msg.m('check_in_error_2') + str(check_in_records) + '\n')
        return False


def check_in_today_do(check_in_records):
    # UTC+8
    server_time = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=8)
    print(str(server_time.date()) + " " + str(server_time.hour) + ":" + str(server_time.minute))
    today = str(server_time.date())
    for record in check_in_records['data']['sign_record_list']:
        if record['date'] == today:
            if record['is_signed'] == '0':
                check_in = HbookerAPI.CheckIn.do_check_in()
                if check_in.get('code') == '100000':
                    print(msg.m('check_in_success_got') + str(check_in['data']['bonus']['exp']) + msg.m('check_in_xp') +
                          str(check_in['data']['bonus']['hlb']) + msg.m('check_in_token') +
                          str(check_in['data']['bonus']['recommend']) + msg.m('check_in_recommend'))
                    return True
                elif check_in.get('code') == '340001':
                    print(msg.m('check_in_no_redo'))
                    return True
                else:
                    print(msg.m('check_in_failed') + str(check_in) + '\n')
                    return False
            else:
                print(msg.m('check_in_already'))
                return True
    # 日期異常，未找本日對應簽到記錄，不進行簽到嘗試
    print(msg.m('check_in_error_day_not_found') + str(check_in_records))
    return False


def agreed_read_readme():
    if Vars.cfg.data.get('agreed_to_readme') != 'yes':
        print(msg.m('read_readme'))
        print(msg.m('agree_terms'))

        confirm = get('>').strip()
        if confirm == 'yes':
            Vars.cfg.data['agreed_to_readme'] = 'yes'
            Vars.cfg.save()
        else:
            sys.exit()


def shell_switch_message_charter_set():
    if Vars.cfg.data['interface_traditional_chinese']:
        Vars.cfg.data['interface_traditional_chinese'] = False
        pass
    else:
        Vars.cfg.data['interface_traditional_chinese'] = True
    Vars.cfg.save()
    msg.set_message_lang(Vars.cfg.data['interface_traditional_chinese'])
    print(msg.m('lang'))


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
            print(msg.m('help_msg'))
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
        print(msg.m('help_msg'))
        print(msg.m('not_login_pl_login'))
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
            shell_select_books(inputs)
        elif inputs[0].startswith('ds') or inputs[0].startswith('downloads'):
            shell_download_shelf(inputs)
        elif inputs[0].startswith('d'):
            shell_download_book(inputs)
        elif inputs[0].startswith('u'):
            shell_download_list(inputs)
        elif inputs[0].startswith('t'):
            check_in_today()
        elif inputs[0].startswith('m'):
            shell_switch_message_charter_set()
        else:
            print(msg.m('help_msg'))
        if loop is False:
            break
        inputs = re.split('\\s+', get('>').strip())


if __name__ == "__main__":
    Vars.cfg.load()
    if type(Vars.cfg.data.get('interface_traditional_chinese')) is not bool:
        Vars.cfg.data['interface_traditional_chinese'] = False
        Vars.cfg.save()
        msg.set_message_lang()
    else:
        msg.set_message_lang(Vars.cfg.data['interface_traditional_chinese'])
    agreed_read_readme()
    if type(Vars.cfg.data.get('max_concurrent_downloads')) is not int:
        Vars.cfg.data['max_concurrent_downloads'] = 32
        Vars.cfg.save()
        max_concurrent_downloads = 32
    else:
        max_concurrent_downloads = Vars.cfg.data.get('max_concurrent_downloads')
    shell()
