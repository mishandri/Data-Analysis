import os
from datetime import datetime

import pandas as pd

result_path = f'07. Практический кейс Pandas/Результат/{datetime.now().strftime("%Y-%m-%d")}/'
if not os.path.exists(result_path):
    os.makedirs(result_path)

sbis_names = ["Дата",
            "Номер",
            "Сумма",
            "Статус",
            "Примечание",
            "Комментарий",
            "Контрагент",
            "ИНН/КПП",
            "Организация",
            "ИНН/КПП",
            "Тип документа",
            "Имя файла",
            "Дата",
            "Номер 1",
            "Сумма 1",
            "Сумма НДС",
            "Ответственный",
            "Подразделение",
            "Код",
            "Дата",
            "Время",
            "Тип пакета",
            "Идентификатор пакета",
            "Запущено в обработку",
            "Получено контрагентом",
            "Завершено",
            "Увеличение суммы",
            "НДC",
            "Уменьшение суммы",
            "НДС"
            ]

sbis_folder = r"07. Практический кейс Pandas/Входящие"
sbis_files = os.listdir(sbis_folder)

dfs = []
for file in sbis_files:
    if 'csv' not in file:
        continue
    df = pd.read_csv(sbis_folder + "/" + file, skiprows=1, sep = ";", encoding="1251", header=None)
    dfs.append(df)

sbis = pd.concat(dfs, ignore_index=True)
sbis.columns = sbis_names
sbis.columns = [c.replace(' ', '_') for c in sbis.columns]

apteka_folder = r"07. Практический кейс Pandas/Аптеки/csv/correct/"
apteka_files = os.listdir(apteka_folder)

for file in apteka_files:

    if 'csv' not in file:
        continue

    apteka = pd.read_csv(apteka_folder + file, sep = ";", encoding="windows-1251")
    apteka["Номер счет-фактуры"] = ""
    apteka["Сумма счет-фактуры"] = ""
    apteka["Дата счет-фактуры"] = ""
    apteka["Сравнение дат"] = ""

    docs = ["СчФктр", "УпдДоп", "УпдСчфДоп", "ЭДОНакл"]

    for i, row in apteka.iterrows():
        nakl = row["Номер накладной"]

        if 'ЕАПТЕКА' in row["Поставщик"]:
            nakl += "/15"

        records = sbis[sbis.Номер.values == nakl]
        records = records[records.Тип_документа.isin(docs)]

        if records.empty:
            continue

        invoice = records.iloc[0]["Номер"]
        summ = records.iloc[0]["Сумма"]
        date = records.iloc[0]["Дата"][1]
        date = datetime.strptime(date, "%d.%m.%y").strftime("%d.%m.%Y")

        apteka.at[i, "Номер счет-фактуры"] = invoice
        apteka.at[i, "Сумма счет-фактуры"] = summ
        apteka.at[i, "Дата счет-фактуры"] = date
        apteka.at[i, "Сравнение дат"] = "" if (date == apteka.at[i, 'Дата накладной']) else "Не совпадает!"


    apteka_columns = ['№ п/п', 'Штрих-код партии', 'Наименование товара', 'Поставщик',
        'Дата приходного документа', 'Номер приходного документа',
        'Дата накладной', 'Номер накладной', 'Номер счет-фактуры',
        'Сумма счет-фактуры', 'Кол-во',
        'Сумма в закупочных ценах без НДС', 'Ставка НДС поставщика',
        'Сумма НДС', 'Сумма в закупочных ценах с НДС', 'Дата счет-фактуры', 'Сравнение дат']

    apteka = apteka[apteka_columns]
    apteka.to_excel(f"{result_path}{file.split('.csv')[0]} - результат.xlsx", index=False)
    print(f'{file} Обработан!')
