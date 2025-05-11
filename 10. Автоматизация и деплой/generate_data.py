from faker import Faker
import random as rnd
import pandas as pd
import numpy as np

fake = Faker('ru_RU')

checks_title = ['doc_id',   # численно-буквенный идентификатор чека
                'item',     # название товара
                'category', # категория товара (бытовая химия, текстиль, посуда и т.д.)
                'amount',   # кол-во товара в чеке
                'price',    # цена одной позиции без учета скидки
                'discount'  # сумма скидки на эту позицию (может быть 0)
]

# Категории
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
# Функция генерации одного чека
def gen_check():
    check = pd.DataFrame(columns=checks_title)
    doc_id = fake.bothify(text='??####??#####?#?#?#?###??').upper()
    for i in range(rnd.randint(1, 10)): # в чеке будет от 1 до 10 позиций
        category = rnd.choice(categories)
        item = gen_product(category)
        amount = rnd.randint(1,5)
        price = round(rnd.random()*1000, 2)
        discount = round(price * rnd.random()/10, 0)
        check.loc[len(check)] = [doc_id, item, category, amount, price, discount]
    return check

print(gen_check())

