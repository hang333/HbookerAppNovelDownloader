import json
import os


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
