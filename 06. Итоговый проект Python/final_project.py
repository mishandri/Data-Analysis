# Импортируем необходимые библиотеки
import requests  # Для запроса данных их API
import logging  # Для логирования
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
import psycopg2  # Для работы с PostgreSQL
import gspread  # Для работы с GoogleSheets
# Для авторизации на гугле
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta   # Для работы с датой и временем
import ast  # для чтения "кода", чтобы быстро строку превратить в словарь
import os

# Считаем, что код запускается где-то ночью и записывает данные в БД за вчерашний день timedelta(days=1)
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
start = f'{yesterday} 00:00:00.000000'
end = f'{yesterday} 23:59:59.999999'

# Настройка логера:
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO,
    encoding='utf-8',
    filename=f"{Path(__file__).parent}/{yesterday}.log",
    filemode="a"
)
logging.info("Запуск программы...")
# Переменные
api_url = "https://b2b.itresume.ru/api/statistics"
params = {
    "client": "Skillfactory",
    "client_key": "M2MGWS",
    "start": start,
    "end": end
}

psql_address = "localhost"
psql_port = 5432
psql_db = "postgres"
psql_user = "postgres"
psql_pass = 123


class ConnectDB:
    __instance = None  # Явное объявление приватного атрибута класса

    @staticmethod
    def get_instance():
        if not ConnectDB.__instance:
            ConnectDB()
        return ConnectDB.__instance

    def __init__(self):
        """Устанавливает соединение с БД"""
        if ConnectDB.__instance:
            logging.warning(
                f"Попытка создать второй экземпляр класса {self.__class__.__name__}")
            raise Exception("Этот класс является Singleton")
        else:
            self.connection = psycopg2.connect(
                host=psql_address,
                port=psql_port,
                database=psql_db,
                user=psql_user,
                password=psql_pass
            )
            ConnectDB.__instance = self
            logging.info(
                f'Соединение с БД "{psql_db}:{psql_port}" установлено')

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close_instance(self):
        """Закрывает соединение с БД"""
        if ConnectDB.__instance:
            self.connection.close()
            logging.info(f'Соединение с БД "{psql_db}:{psql_port}" закрыто')


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
            logging.info('Данные из API получены')
        except requests.exceptions.HTTPError:
            logging.warning(f"HTTP Error: {self.status}")
            return self.status
        except requests.exceptions.RequestException:
            logging.warning(f"Request Error: {self.status}")
            return self.status
        res = []
        try:
            logging.info('Начата обработка данных')
            for el in self.__json:
                dict_res = {}
                dict_res['user_id'] = el['lti_user_id']
                if 'passback_params' in el:
                    if el['passback_params'] is not None:
                        d = ast.literal_eval((el['passback_params']))
                    else:
                        d = {}
                    for key in ('oauth_consumer_key', 'lis_result_sourcedid', 'lis_outcome_service_url'):
                        dict_res[key] = d[key] if key in d else ""
                else:
                    dict_res['oauth_consumer_key'] = ""
                    dict_res['lis_result_sourcedid'] = ""
                    dict_res['lis_outcome_service_url'] = ""
                dict_res['is_correct'] = el['is_correct']
                dict_res['attempt_type'] = el['attempt_type']
                dict_res['created_at'] = el['created_at']
                for k, v in dict_res.items():
                    if v == "":
                        logging.warning(
                            f'Обнаружено пустое значение в ключе {k}')
                res.append(dict_res)
            logging.info('Обработка данных закончена')
            return res
        except KeyError:
            logging.error('Ошибка ключа при формировании словаря')
            return []

# TODO Создать класс для отправки сообщений по электронной почте


class Email:
    ...

# TODO Создать класс для записи данных в Google Sheets


class GoogleSheet:
    ...


# Получаем данные из API
data = APIClient(api_url, params).fetch_data()

db_connection = ConnectDB.get_instance()  # Соединяемся с БД
try:
    cursor = db_connection.connection.cursor()  # Устанавливаем курсор
    query = """
    INSERT INTO users (
        user_id, 
        oauth_consumer_key, 
        lis_result_sourcedid, 
        lis_outcome_service_url, 
        is_correct, 
        attempt_type, 
        created_at
        ) 
        VALUES (
        %(user_id)s, 
        %(oauth_consumer_key)s, 
        %(lis_result_sourcedid)s,
        %(lis_outcome_service_url)s,
        %(is_correct)s,
        %(attempt_type)s,
        %(created_at)s
        )
    """
    cursor.executemany(query, data)  # Передаём список словарей для вставки многих строк
    db_connection.commit()  # "Подтверждаем" вставку
    logging.info(f'Данные успешно занесены в БД')
except Exception as e:
    logging.error(f"Неожиданная ошибка: {e}")
    if db_connection:
        # "Отменяем" вставку
        db_connection.rollback()
finally:
    if db_connection:
        # Отсоединяемся от БД
        db_connection.close_instance()


# yesterday = (datetime.now() - timedelta(days=732)).strftime("%Y-%m-%d")
logging.info("Работа программы успешно завершена")