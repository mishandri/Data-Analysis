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
columns = set(['doc_id', 'doc_dt', 'item', 'category', 'amount', 'price', 'discount', 'shop_num', 'cash_num'])

try:
    for f in csv_list:
        df = pd.read_csv(os.path.join(dirname, 'data', f))
        logging.info(f"Обработка файла {f}")
        if set(df.columns) == columns:  # Проверка колонок на соответствие
            for i, row in df.iterrows():
                query = f"INSERT INTO ticket VALUES ('{row['doc_id']}', CAST('{row['doc_dt']}' AS TIMESTAMP), '{row['item']}', '{row['category']}', '{row['amount']}', '{row['price']}', '{row['discount']}', '{row['shop_num']}', '{row['cash_num']}')"
                database.post(query)  
            # Удаляем загруженный csv-файл
            # try:
            #     os.remove(os.path.join(dirname, 'data', f))  
            #     logging.info(f"Файл {f} удалён")
            # except Exception as e:
            #     logging.error(e)
        logging.info(f"Файл {f} обработан")
        else:
            logging.warn(f"Названия колонок не соответствуют. Файл {f} был пропущен")
    logging.info("Работа программы завершена")
except Exception as err:
    logging.error(err)


# Отчёт на почту
def send_yandex_email(sender_email, sender_password, receiver_email: str, subject: str, body, attachment):
    try:
        # Настройки SMTP Яндекс
        smtp_server = config["email"]["SMTPSERVER"]
        smtp_port = 465
        
        # Создаем сообщение
        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.set_content(body)
        
        # Прикрепляем файл с логом
        with open(attachment, 'rb') as file:
            msg.add_attachment(file.read(), maintype='text', subtype='plain', filename=f'{today.strftime("%Y-%m-%d")}.log')
        
        # Отправляем письмо
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        logging.info("E-mail успешно отправлен!")
    
    except Exception as e:
        logging.error(f"Ошибка отправки E-mail: {e}")


# Настройка параметров для электронной почты
yandex_email = config["email"]["EMAIL"]
recipient = config["email"]["TO"]
app_password = config["email"]["PASSWORD"]

send_yandex_email(
    sender_email=yandex_email,
    sender_password=app_password,
    receiver_email=recipient,
    subject="Важное уведомление",
    body="""Здравствуйте!
Работа алгоритма закончена
С уважением,
Автоматизированная система""",
    attachment=f'{dirname}/logs/{today.strftime("%Y-%m-%d")}.log'
)
