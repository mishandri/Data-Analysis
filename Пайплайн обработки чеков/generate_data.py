from faker import Faker
import random as rnd
import pandas as pd
import numpy as np
import os
import logging  # Для логирования
from datetime import datetime, timedelta

dirname = os.path.dirname(__file__)
today = datetime.today()
fake = Faker('ru_RU')

# Настройка логера:
os.makedirs(os.path.join(dirname, "logs"), exist_ok=True) # Создаём папку logs, если её не существует
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO,
    encoding='utf-8',
    filename=f'{dirname}/logs/{today.strftime("%Y-%m-%d")}.log',
    filemode='a'
)
logging.info(f"Запуск скрипта {os.path.basename(__file__)} для генерации данных чеков...")

# Заголовки для чека
checks_title = ['doc_id',   # численно-буквенный идентификатор чека
                'doc_dt',   # дата и время покупки
                'item',     # название товара
                'category', # категория товара
                'amount',   # кол-во товара в чеке
                'price',    # цена одной позиции без учета скидки
                'discount'  # сумма скидки на эту позицию (может быть 0)
]

# Категории для товаров
categories = ["Овощи", "Фрукты", "Безалкогольные напитки", "Чипсы, орехи, сухарики", 
            "Алкогольные напитки", "Молочные продукты", "Кисломолочные продукты", 
            "Яйцо", "Сыры", "Хлеб, выпечка", "Бакалея, соусы", "Консервы", "Птица, мясо",
            "Рыба, морепродукты", "Колбасы, сосиски", "Чай, кофе, какао"]

# Функция генерации "уникального товара" на базе категории
def gen_product(category):
    if category == "Овощи":
        return f'{rnd.choice(["Свежий", "Фермерский"])} {rnd.choice(["картофель", "томат", "огурец", "лук", "баклажан", "кабачок"])} {rnd.choice(["650г.", "1кг.", "450г."])}'
    if category == "Фрукты":
        return f'{rnd.choice(["Яблоко", "Банан", "Груша", "Мандарин", "Апельсин", "Киви", "Виноград", "Клубника"])} ({fake.country()})'
    if category == "Безалкогольные напитки":
        return f'{rnd.choice(["Пиво безалкогольное", "Кола", "Лимонад", "Минеральная вода", "Питьевая вода"])} {fake.company()}'
    if category == "Алкогольные напитки":
        return f'{rnd.choice(["Пиво 4%", "Пиво 4.5%", "Пиво 4.2%", "Водка 40%", "Виски 38%"])} {fake.company()}'
    if category == "Чипсы, орехи, сухарики":
        return f'{rnd.choice(["Чипсы", "Орехи", "Сухарики", "Снеки", "Семечки"])} {rnd.choice(["40г.", "65г.", "120г.", "140г."])}'
    if category == "Молочные продукты":
        return f'Молоко {rnd.choice(["цельное", "пастеризованное", "ультрапастеризованное"])} {rnd.choice(["1%", "2.5%", "3.5%"])} {rnd.choice(["900г.", "850г.", "450г.", "400г."])}'
    if category == "Кисломолочные продукты":
        return f'{rnd.choice(["Кефир", "Йогурт", "Фругурт"])} {rnd.choice(["1%", "2.5%", "3.5%"])}  {rnd.choice(["120г.", "110г.", "450г.", "400г."])}'
    if category == "Яйцо":
        return f'Яйцо {rnd.choice(["С0", "С1", "С2"])}'
    if category == "Сыры":
        return f'Сыр {rnd.choice(["Российский", "Масдам", "Голландский", "Ламбер", "Тильзитер", "Пармезан"])} {rnd.choice(["40%", "45%", "50%"])} {rnd.choice(["150г.", "200г.", "250г."])}'
    if category == "Хлеб, выпечка":
        return f'{rnd.choice(["Батон", "Булка", "Буханка"])} {rnd.choice(["пшен.", "мультизерн.", "ржан.", "кукурузн."])} {rnd.choice(["150г.", "200г.", "250г.", "400г."])}'
    if category == "Бакалея, соусы":
        return f'{rnd.choice(["Майонез", "Кетчуп", "Соус"])} {rnd.choice(["220г.", "400г.", "780г."])}'
    if category == "Консервы":
        return f'{rnd.choice(["Горошек", "Кукуруза", "Фасоль красная", "Фасоль белая"])} {rnd.choice(["350г.", "400г."])}'
    if category == "Птица, мясо":
        return f'{rnd.choice(["Говядина", "Свинина", "Курица"])} {rnd.choice(["1кг.", "500г."])}'
    if category == "Рыба, морепродукты":
        return f'{rnd.choice(["Лосось", "Креветки", "Горбуша", "Крабовое мясо"])} {rnd.choice(["1кг.", "500г."])}'
    if category == "Колбасы, сосиски":
        return f'{rnd.choice(["Варен.", "Копчен.", "Сырокопч."])} {rnd.choice(["колбаса", "сосиски"])} {rnd.choice(["250г.", "300г.", "400г."])}'
    if category == "Чай, кофе, какао":
        return f'{rnd.choice(["Чай", "Кофе", "Какао"])} ({fake.country()}) {rnd.choice(["120г.", "150г.", "200г.", "400г."])}'
    
# Функция генерации цены по категории
def gen_price_product(category):
    if category == "Овощи":
        price_weights = [50, 50, 60, 60, 70, 70, 70]
    if category == "Фрукты":
        price_weights = [50, 50, 50, 60, 60, 70, 70]
    if category == "Безалкогольные напитки":
        price_weights = [70, 70, 90, 90, 100, 110]
    if category == "Алкогольные напитки":
        price_weights = [300, 300, 300, 500, 600, 800]
    if category == "Чипсы, орехи, сухарики":
        price_weights = [80, 80, 80, 40, 40, 30]
    if category == "Молочные продукты":
        price_weights = [60, 60, 60, 70, 80, 90]
    if category == "Кисломолочные продукты":
        price_weights = [90, 90, 90, 100, 110, 120]
    if category == "Яйцо":
        price_weights = [70, 70, 70, 70, 90, 110]
    if category == "Сыры":
        price_weights = [110, 110, 120, 120, 120, 150]
    if category == "Хлеб, выпечка":
        price_weights = [30, 30, 30, 40, 40, 50]
    if category == "Бакалея, соусы":
        price_weights = [100, 100, 100, 120, 120, 150]
    if category == "Консервы":
        price_weights = [80, 80, 100, 120, 120, 250]
    if category == "Птица, мясо":
        price_weights = [300, 300, 350, 400, 450, 500]
    if category == "Рыба, морепродукты":
        price_weights = [300, 350, 400, 400, 450, 500]
    if category == "Колбасы, сосиски":
        price_weights = [150, 150, 200, 200, 350, 400]
    if category == "Чай, кофе, какао":
        price_weights = [350, 350, 400, 400, 550, 550]
    price_tmp = [x - 0.01 for x in price_weights]      
    return rnd.choice(price_tmp)

# Функция генерации времени чека
def gen_time():   
    while True:
        t = fake.time(pattern='%H:%M:%S')
        hour = int(t.split(':')[0])
        if 9 <= hour < 21:  # Рабочее время магазина
            return t

# Функция генерации одного чека
def gen_check():
    check = pd.DataFrame(columns=checks_title)
    doc_id = fake.bothify(text='??####??#####?#?#?#?###??').upper()
    doc_dt = f'{today.strftime('%Y-%m-%d')} {gen_time()}'
    for i in range(rnd.randint(1, 10)): # в чеке будет от 1 до 10 позиций
        category = rnd.choice(categories)
        item = gen_product(category)
        amount_weights = [1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 4]  # 1 и 2 встречаются чаще
        amount = rnd.choice(amount_weights)
        price = round(gen_price_product(category), 2)
        discount = 0
        if rnd.random() < 0.2:  # 20% товаров со скидкой
            discount_percent = rnd.choice([5,10,15,20,30])
            discount = round(price * discount_percent / 100)
        check.loc[len(check)] = [doc_id, doc_dt, item, category, amount, price, discount]
    return check

n = 12 # Количество магазинов
k = 4 # Количество касс в каждом магазине
for shop in range(n):
    for cash in range(k):
        df = pd.DataFrame()
        for customer in range(5, 51): # от 5 до 50 покупателей в магазине за день
            df = pd.concat([df, gen_check()], ignore_index=True)
        # Сразу добавим номер магазина и номер чека для последующего удобства
        df['shop_num'] = shop + 1
        df['cash_num'] = cash + 1
        df = df.sort_values('doc_dt') # Отсортируем по времени
        filename = f"data/{shop + 1}-{cash + 1}.csv"
        pathfile = os.path.join(dirname, filename)
        df.to_csv(pathfile, index=False)
        logging.info(f'Файл "{filename}" создан.')

logging.info(f"Скрипт {os.path.basename(__file__)} успешно завершён. Файлы с чеками успешно созданы.")
