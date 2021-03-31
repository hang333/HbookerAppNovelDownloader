from book import *

BookShelfList = []


def get_bookshelf_by_index(shelf_index):
    for shelf in BookShelfList:
        if shelf.shelf_index == shelf_index:
            return shelf
    return None


class BookShelf:
    shelf_id = None
    reader_id = None
    shelf_name = None
    shelf_index = None
    book_limit = None
    BookList = None

    def __init__(self, data):
        self.shelf_id = data['shelf_id']
        self.reader_id = data['reader_id']
        self.shelf_name = data['shelf_name']
        self.shelf_index = data['shelf_index']
        self.book_limit = data['book_limit']
        self.BookList = []

    def show_info(self):
        print('書架编號:', self.shelf_index, ', 書架名:', self.shelf_name)

    def get_book_list(self):
        response = HbookerAPI.BookShelf.get_shelf_book_list(self.shelf_id)
        if response.get('code') == '100000':
            self.BookList.clear()
            i = 1
            for data in response['data']['book_list']:
                self.BookList.append(Book(str(i), data['book_info']))
                i += 1

    def show_book_list(self):
        for book in self.BookList:
            print('《', book.book_name, '》作者:', book.author_name, '\n書籍编號:', book.index, ', 書籍ID:', book.book_id)
            print('更新時間:', book.last_chapter_info['uptime'], '\n最新章節:', book.last_chapter_info['chapter_title'], '\n')
        print()

    def get_book(self, index):
        for book in self.BookList:
            if book.index == index:
                return book
        return None
