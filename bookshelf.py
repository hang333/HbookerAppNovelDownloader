from book import *
import msg

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
        print(msg.m('shelf_index'), self.shelf_index, msg.m('shelf_name'), self.shelf_name)

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
            print('《', book.book_name, msg.m('show_list_author'), book.author_name, msg.m('show_list_book_index'), book.index, msg.m('show_list_book_id'), book.book_id)
            print(msg.m('show_list_uptime'), book.last_chapter_info['uptime'], msg.m('show_list_last_chap'), book.last_chapter_info['chapter_title'], '\n')
        print()

    def get_book(self, index):
        for book in self.BookList:
            if book.index == index:
                return book
        return None
