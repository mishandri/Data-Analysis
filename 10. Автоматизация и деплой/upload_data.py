import random as rnd
import pandas as pd
import numpy as np
import configparser
import os
from datetime import datetime
import logging  # Для логирования
import smtplib  # Для отправки по SMTP
from email.message import EmailMessage  # Для создания e-mail

from pgdb import PGDatabase

dirname = os.path.dirname(__file__)
today = datetime.today()

# Настройка кофиг-файла
config = configparser.ConfigParser()
config.read(os.path.join(dirname, "config.ini"))
PSQL = config['sql']

os.makedirs(os.path.join(dirname, "logs"), exist_ok=True) # Создаём папку logs, если её не существует
# Настройка логера:
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO,
    encoding='utf-8',
    filename=f'{dirname}/logs/{today.strftime("%Y-%m-%d")}.log',
    filemode='a'
)
logging.info(f"Запуск скрипта {os.path.basename(__file__)} для выгрузки данных в БД...")

# Подключаемся к БД
try:
    database = PGDatabase(
        host=PSQL["HOST"],
        database=PSQL["DATABASE"],
        user=PSQL["USER"],
        password=PSQL["PASSWORD"]
    )
except Exception as err:
    logging.error(err)

# Список всех файлов csv в директории
csv_list = [f for f in os.listdir(os.path.join(dirname, 'data')) if f.endswith(".csv")]

try:
    for f in csv_list:
        df = pd.read_csv(os.path.join(dirname, 'data', f))
        logging.info(f"Обработка файла {f}")
        for i, row in df.iterrows():
            query = f"INSERT INTO ticket VALUES ('{row['doc_id']}', CAST('{row['doc_dt']}' AS TIMESTAMP), '{row['item']}', '{row['category']}', '{row['amount']}', '{row['price']}', '{row['discount']}', '{row['shop_num']}', '{row['cash_num']}')"
            database.post(query)    
except Exception as err:
    logging.error(err)

