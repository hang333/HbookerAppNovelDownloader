import json
import os


class Config:
    file_path = None
    dir_path = None
    data = None

    def __init__(self, file_path, dir_path):
        self.file_path = file_path
        self.dir_path = dir_path
        self.data = {}

    def load(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f) or {}
        except FileNotFoundError:
            try:
                if not os.path.isdir(self.dir_path):
                    os.makedirs(self.dir_path)
                with open(self.file_path, 'w'):
                    pass
            except Exception as e:
                print('error: ', e)
                print('error: while creating config file: ' + self.file_path)
        except Exception as e:
            print('error: ', e)
            print('error: while reading config file: ' + self.file_path)

    def save(self):
        try:
            if not os.path.isdir(self.dir_path):
                os.makedirs(self.dir_path)
            with open(self.file_path, 'w') as f:
                json.dump(self.data, f)
        except Exception as e:
            print('error: ', e)
            print('error: while saving config file: ' + self.file_path)
