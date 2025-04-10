# Импортируем необходимые библиотеки
import requests # Для запроса данных их API
import logging  # Для логирования
import gspread  # Для работы с GoogleSheets
from oauth2client.service_account import ServiceAccountCredentials #Для авторизации на гугле
from datetime import datetime   # Для работы с датой и временем

#TODO Создать класс-синглтон для подключения к локальной БД
class ConnectDB:
    ...

#TODO Создать класс для запроса данных с удалённого сервера
class GetData:
    ...

#TODO Создать класс для логирования всех действий
class Logging:
    ...

#TODO Создать класс для отправки сообщений по электронной почте
class Email:
    ...

#TODO Создать класс для записи данных в Google Sheets
class GoogleSheet:
    ...