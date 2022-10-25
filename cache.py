from instance import *
import book


def save_cache(file_name: str, response: dict) -> None:
    if not os.path.exists('Localcache'):
        os.mkdir('Localcache')
    with open(f'Localcache/{file_name}', 'w', encoding='utf-8') as book_info_file:
        json.dump(response, book_info_file, ensure_ascii=False, indent=4)


def load_cache(file_name: str) -> dict:
    if os.path.exists(f'Localcache/{file_name}') and os.path.getsize(f'Localcache/{file_name}') > 0:
        with open(f'Localcache/{file_name}', 'r', encoding='utf-8') as book_info_file:
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
