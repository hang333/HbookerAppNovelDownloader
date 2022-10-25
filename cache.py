from instance import *
import book


def save_cache(book_id: str, response: dict) -> None:
    if not os.path.exists('Localcache'):
        os.mkdir('Localcache')
    with open(f'Localcache/{book_id}.json', 'w', encoding='utf-8') as book_info_file:
        json.dump(response, book_info_file, ensure_ascii=False, indent=4)


def load_cache(book_id: str) -> dict:
    if os.path.exists(f'Localcache/{book_id}.json') and os.path.getsize(f'Localcache/{book_id}.json') > 0:
        with open(f'Localcache/{book_id}.json', 'r', encoding='utf-8') as book_info_file:
            return json.load(book_info_file)
    else:
        print(f'{book_id}.json not found.')


def test_cache_and_init_object(book_id: str) -> bool:
    Vars.current_book = load_cache(book_id)
    if not isinstance(Vars.current_book, dict):
        print("服务器无法获取书籍信息，已尝试从本地缓存中获取，但未找到。")
        return False
    Vars.current_book = book.Book(None, Vars.current_book)
    print("服务器无法获取书籍信息，从本地缓存中获取书籍信息成功。")
    return True
