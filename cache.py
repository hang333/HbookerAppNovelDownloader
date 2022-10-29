from instance import *
import book


def save_cache(file_name: str, response: dict) -> None:
    if not os.path.exists(Vars.cfg.data['local_cache_dir']):
        os.mkdir(Vars.cfg.data['local_cache_dir'])
    if Vars.cfg.data.get('backups_local_cache'):
        with open(f"{Vars.cfg.data['local_cache_dir']}/{file_name}", 'w', encoding='utf-8') as book_info_file:
            json.dump(response, book_info_file, ensure_ascii=False, indent=4)
    else:
        print("未开启本地缓存备份，已跳过本地缓存备份步骤, 请在配置文件中开启本地缓存备份。")


def load_cache(file_name: str) -> dict:
    local_cache_dir = f"{Vars.cfg.data['local_cache_dir']}/{file_name}"
    if os.path.exists(local_cache_dir) and \
            os.path.getsize(local_cache_dir) > 0:
        with open(local_cache_dir, 'r', encoding='utf-8') as book_info_file:
            return json.load(book_info_file)
    else:
        print(f'{file_name} not found.')


def test_division_list(book_id: str):
    division_list = load_cache(f"{book_id}_chapter_list.json")
    if not isinstance(division_list, dict):
        print("服务器无法获取目录信息，从本地缓存中获取目录信息成功。")
        return division_list
    print("服务器无法获取目录信息，已尝试从本地缓存中获取，但未找到。")


def test_cache_and_init_object(book_id: str) -> bool:
    Vars.current_book = load_cache(f"{book_id}.json")
    if not isinstance(Vars.current_book, dict):
        print("服务器无法获取书籍信息，已尝试从本地缓存中获取，但未找到。")
        return False
    Vars.current_book = book.Book(None, Vars.current_book)
    print("服务器无法获取书籍信息，从本地缓存中获取书籍信息成功。")
    return True
