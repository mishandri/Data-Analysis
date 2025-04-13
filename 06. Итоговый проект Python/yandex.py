from webdav3.client import Client
from openpyxl import load_workbook, Workbook

import os

class YandexDisk:
    def __init__(self):
        #Сохраню пароль в отдельном файле, который не выгружается на гит
        with open('password_yandex', 'r') as f:
            self.__password_xlsx = f.read()

        self.options = {
            "webdav_hostname": "https://webdav.yandex.ru",
            "webdav_login": "kolcharma@yandex.ru",
            "webdav_password": self.__password_xlsx,
        }
        
    def report(self, filename):
        self.filename = filename
        file = os.path.abspath(__file__) # Получаем путь к файлу .py
        path = os.path.dirname(file)    # Берём только директорию
        # Выгружаем файл
        fullpath = f'{path}/{filename}'
        client = Client(self.options)
        if not client.check("python"):
            client.mkdir("python")
        client.upload(f'python/{self.filename}', fullpath)

report = YandexDisk().report('2025-04-12.log')