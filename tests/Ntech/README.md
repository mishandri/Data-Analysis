# Анализ чекового массива с целью выявления ключевых показателей

Все вычисления в файле `analyse.ipynb`

Все необходимые библиотеки в файле `requirements.txt` 

## Выяснены какие торговые сети присутствуют в массиве чеков

В массиве чеков присутствуют 3 торговых сетей:

| Название сети | Количество магазинов |
| ------------------------- | --------------------------------------- |
| Metro c&c                 | 8                                       |
| Гиперглобус    | 7                                       |
| Окей                  | 20                                      |

## Построена интерактивная карта для отображения расположения магазинов

<img src="https://github.com/mishandri/Data-Analysis/blob/main/tests/Ntech/pics/map.gif" title="Интерактивная карта магазинов" />

## Проверены данные на выбросы (графики интерактивные)

### До обработки:

<img src="https://github.com/mishandri/Data-Analysis/blob/main/tests/Ntech/pics/box_before_1.png" title="Окей до обработки" />

<img src="https://github.com/mishandri/Data-Analysis/blob/main/tests/Ntech/pics/box_before_2.png" title="Гиперглобус до обработки" />

<img src="https://github.com/mishandri/Data-Analysis/blob/main/tests/Ntech/pics/box_before_3.png" title="Метро до обработки" />

### После обработки:

<img src="https://github.com/mishandri/Data-Analysis/blob/main/tests/Ntech/pics/box_after_1.png" title="Окей после обработки" />

<img src="https://github.com/mishandri/Data-Analysis/blob/main/tests/Ntech/pics/box_after_2.png" title="Гиперглобус после обработки" />

<img src="https://github.com/mishandri/Data-Analysis/blob/main/tests/Ntech/pics/box_after_3.png" title="Метро после обработки" />


## Выполнена общая оценка показателей в торговых сетях

### Построена интерактивная корреляционная матрица

<img src="https://github.com/mishandri/Data-Analysis/blob/main/tests/Ntech/pics/corr.png" title="Корреляционная матрица" />

### Проведён ABC-анализ для торговых сетей по трём параметрам:

- `CLEAN_SKU` по прибыли проданных позиций,
- `CLEAN_SKU` по количеству проданных позиций,
- `CATEGORY_NT` по количеству проданных позиций

### Проведён XYZ-анализ для торговых сетей по `CLEAN_SKU`

#### Результаты формируются в *.csv файлы с названиями `ABC-XYZ {Имя торговой сети}`

<img src="https://github.com/mishandri/Data-Analysis/blob/main/tests/Ntech/pics/ABC-XYZ.png" title="ABC-XYZ-анализ" />

### Проведено сравнение средних цен по категории товаров `CATEGORY_NT` во всех трёх сетях.

- В одной таблице взяты все значения (с пропусками) для наглядности отсутствующих категорий в торговых сетях
<img src="https://github.com/mishandri/Data-Analysis/blob/main/tests/Ntech/pics/mean_category1.png" title="С пропусками" />
- В другой таблице взяты только значения, встречающиеся во всех трёх торговых сетях
<img src="https://github.com/mishandri/Data-Analysis/blob/main/tests/Ntech/pics/mean_category2.png" title="Без пропусков" />

### Рассчитана средняя сумма чека:

- в каждой торговой сети
- по часам во всех торговых сетях (для сравнения) `*`
- по дням недели во всех торговых (сетях для сравнения) `*`
- по часам для каждого магазина торговой сети
- по дням недели для каждого магазина торговой сети

### Для средних чеков, обозначенных `*`, построены интерактивные графики

<img src="https://github.com/mishandri/Data-Analysis/blob/main/tests/Ntech/pics/mean_chek_hour.png" title="Средний чек по часам" />

<img src="https://github.com/mishandri/Data-Analysis/blob/main/tests/Ntech/pics/mean_chek_weekday.png" title="Средний чек по дням недели" />

### Проведён RFM-анализ по клиентам, у которых есть `customer_id`, то есть применена карта магазина

#### Результаты формируются в *.csv файлы с названиями `RFM {Имя торговой сети}`

<img src="https://github.com/mishandri/Data-Analysis/blob/main/tests/Ntech/pics/RFM.png" title="RFM-анализ" />

## Выводы:

- Применённые функции для проведения ABC, XYZ и RFM анализов можно, при необходимости, использовать для каждого отдельного магазина, сформировав отфильтрованный датафрейм.
- ABC-анализ говорит, что товары категории:

  - A - самые важные. Это 20% товаров, которые приносят 80% выручки. Они всегда должны быть на складе. Дефицит этих товаров приводит к проседанию по выручке
  - B - требуют контроля, так как это товары-кандидаты в категорию A. Они не приносят много выручки, но лучше, чтобы они были в наличии.
  - C - товары, которые не приносят значимой выручки, их можно реже закупать и не хранить на складах. Некоторые из них можно даже исключить из ассортимента.
- XYZ-анализ говорит, что товары категории:

  - X - товары со стабильным спросом, они всегда должны быть в наличии.
  - Y - товары со средним спросом, возможно, сезонные. Закупать в большом количестве смысла нет.
  - Z - товары с редким спросом. Необходимо проанализировать поставки, если с поставками проблем не было (то есть товара было достаточно), то от таких товаров можно либо отказаться, либо поставлять по предзаказу.
- RFM-анализ говорит, что покупатели категории:

  - R - сколько дней прошло с последней покупки клиента: 1 - давно, 3 - недавно
  - F - как клиент часто покупает: 1 - редко, 3 - часто
  - M - сколько прибыли приносит клиент: 1 - мало, 3 много
    
    Другими словами, следует присмотреться к клиентам 133 и 233, чтобы замотивировать их чаще ходить за покупками. Например, сделать персональные предложения.

    Клиентов 313 и 323 также можно замотивировать ходить чаще. Например, использовать рассылку уведомлений о временных акциях на товары.

    Кроме того, можно обратить внимание на клиентов 222, чтобы вывести их хотя бы в одну из групп 322, 232 или 223. Подойдут и персональные предложения, и уведомления об акциях.
