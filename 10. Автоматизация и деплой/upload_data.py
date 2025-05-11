import random as rnd
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import logging  # Для логирования
import smtplib  # Для отправки по SMTP
from email.message import EmailMessage  # Для создания e-mail

dirname = os.path.dirname(__file__)
today = datetime.today()

# Настройка логера:
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO,
    encoding='utf-8',
    filename=f"{dirname}/logs/{today.strftime("%Y-%m-%d")}.log",
    filemode="a"
)
logging.info(f"Запуск скрипта {os.path.basename(__file__)} для выгрузки данных в БД...")

