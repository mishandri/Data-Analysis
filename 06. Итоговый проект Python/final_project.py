# Импортируем необходимые библиотеки
import requests # Для запроса данных их API
import logging  # Для логирования
import psycopg2 # Для работы с PostgreSQL
import gspread  # Для работы с GoogleSheets
from oauth2client.service_account import ServiceAccountCredentials #Для авторизации на гугле
from datetime import datetime   # Для работы с датой и временем
import ast # для чтения "кода"

# Переменные
api_url = "https://b2b.itresume.ru/api/statistics"
params={
    "client": "Skillfactory",
    "client_key": "M2MGWS",
    "start": "2023-04-01 12:46:47.860798",
    "end": "2023-04-01 12:49:47.860798"
}

psql_address = "localhost"
psql_port = 5432
psql_db = "postgres"
psql_user = "postgres"
psql_pass = 123

#TODO Создать класс-синглтон для подключения к локальной БД
class ConnectDB:
    ...

class APIClient:
    def __init__(self, url, params):
        self.url = url
        self.__params = params

    def fetch_data(self):
        """Загружает данные из API и возвращает их в структурированном виде."""
        try:
            response = requests.get(self.url, params=self.__params)
            self.status = response.status_code
            self.__json = response.json()
        except requests.exceptions.RequestException as err:
            raise ValueError(f"API request failed: {err}")
        res = []
        for el in self.__json:
            dict_res = {}
            dict_res['user_id'] = el['lti_user_id']
            d = ast.literal_eval((el['passback_params']))
            for key in ('oauth_consumer_key', 'lis_result_sourcedid', 'lis_outcome_service_url'):
                dict_res[key] = d[key] if key in d else ""
            dict_res['is_correct'] = el['is_correct']
            dict_res['attempt_type'] = el['attempt_type']
            dict_res['created_at'] = el['created_at']
            res.append(dict_res)
        return res

#TODO Создать класс для логирования всех действий
class Logging:
    ...
        # def status(self):
    #     status_code = r.status_code
    #     if status_code == 200:
    #         print("Запрос выполнен успешно!")
    #     elif status_code == 404:
    #         print("Ресурс не найден.")
    #     elif status_code == 403:
    #         print("Доступ запрещён!")
    #     elif status_code == 503:
    #         print("Сервер не доступен...")
    #     else:
    #         print("Произошла ошибка:", status_code)

#TODO Создать класс для отправки сообщений по электронной почте
class Email:
    ...

#TODO Создать класс для записи данных в Google Sheets
class GoogleSheet:
    ...


data = APIClient(api_url, params).fetch_data()
print(data)
