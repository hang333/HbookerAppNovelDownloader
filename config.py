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
            with open(self.file_path, 'r') as f:
                self.data = json.load(f) or {}
        except FileNotFoundError:
            try:
                if not os.path.isdir(self.dir_path):
                    os.makedirs(self.dir_path)
                with open(self.file_path, 'w'):
                    pass
            except Exception as e:
                print('[错误]', e)
                print('创建配置文件时出错')
        except Exception as e:
            print('[错误]', e)
            print('读取配置文件时出错')

    def save(self):
        try:
            if not os.path.isdir(self.dir_path):
                os.makedirs(self.dir_path)
            with open(self.file_path, 'w') as f:
                json.dump(self.data, f)
        except Exception as e:
            print('[错误]', e)
            print('保存配置文件时出错')
