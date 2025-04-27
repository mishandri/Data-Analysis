# Анализ чекового массива с целью выявления ключевых показателей

## Выснены какие торговые сети присутствуют в массиве чеков

В массиве чеков присутствуют 3 торговых сетей:

| Название сети | Количество магазинов |
| ------------------------- | --------------------------------------- |
| Metro c&c                 | 8                                       |
| Гиперглобус    | 7                                       |
| Окей                  | 20                                      |

## Построена интерактивная карта для отображения расположения магазинов

<img src="https://github.com/mishandri/Data-Analysis/blob/main/tests/Ntech/pics/map.gif" title="Интерактивная карта магазинов" />

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

### Для средних чеков, обозначенных `*` построены интерактивные графики

<img src="https://github.com/mishandri/Data-Analysis/blob/main/tests/Ntech/pics/mean_chek_hour.png" title="Средний чек по часам" />

<img src="https://github.com/mishandri/Data-Analysis/blob/main/tests/Ntech/pics/mean_chek_weekday.png" title="Средний чек по дням недели" />

### Проведён RFM-анализ по клиентам, у которых есть `customer_id`, то есть применена карта магазина

#### Результаты формируются в *.csv файлы с названиями `RFM {Имя торговой сети}`
<img src="https://github.com/mishandri/Data-Analysis/blob/main/tests/Ntech/pics/RFM.png" title="RFM-анализ" />
