"""
Задача от внутреннего заказчика: ежедневная выгрузка продаж приходит одним файлом,
его надо превратить в три витрины для отчётности.
"""
from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

BASE_DIR = Path(__file__).parent
SOURCE = BASE_DIR / "sales_data.csv"
OUT_DIR = BASE_DIR / "output"

DATE_FMT = "%Y-%m-%d"
PERIOD = "month"


@dataclass(frozen=True)
class Sale:
    """Строка исходной выгрузки. frozen=True потому что после чтения запись не меняется."""

    id: str
    date: datetime
    amount: Decimal
    product: str

    @property
    def period(self) -> str:
        return self.date.strftime("%Y-%m")


def read_sales(path: Path) -> list[Sale]:
    sales: list[Sale] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sales.append(
                Sale(
                    id=row["id"],
                    date=datetime.strptime(row["date"], DATE_FMT),
                    amount=Decimal(row["amount"]),
                    product=row["product"],
                )
            )
    return sales


def filter_by_date(
    sales: list[Sale], start: datetime, end: datetime
) -> list[Sale]:
    """Период включительно с обеих сторон. Даты приходят в одном формате,
    приводить к datetime достаточно."""
    return [s for s in sales if start <= s.date <= end]


def filter_by_amount(sales: list[Sale], low: Decimal, high: Decimal) -> list[Sale]:
    return [s for s in sales if low <= s.amount <= high]


def round_money(value: Decimal) -> Decimal:
    """ROUND_HALF_UP, а не банковский ROUND_HALF_EVEN: в отчётности
    привычнее 0.5 вверх, иначе суммы разных строк будут расходиться
    с суммой итогов."""
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def aggregate(sales: list[Sale], key) -> dict:
    """Сумма и количество по произвольному ключу."""
    result = defaultdict(lambda: {"revenue": Decimal(0), "qty": 0})
    for s in sales:
        bucket = result[key(s)]
        bucket["revenue"] += s.amount
        bucket["qty"] += 1
    return result


def write_csv(path: Path, header: list[str], rows: list[list]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def build(sales: list[Sale], start: datetime, end: datetime,
          low: Decimal, high: Decimal) -> dict:
    """Пайплайн целиком: фильтр по дате, фильтр по сумме, агрегаты, выгрузка."""
    by_date = filter_by_date(sales, start, end)
    by_amount = filter_by_amount(by_date, low, high)

    total = sum((s.amount for s in by_amount), Decimal(0))
    months = aggregate(by_amount, lambda s: s.period)
    products = aggregate(by_amount, lambda s: s.product)

    write_csv(
        OUT_DIR / "sales_filtered.csv",
        ["id", "date", "amount", "product"],
        [[s.id, s.date.strftime(DATE_FMT), s.amount, s.product] for s in by_amount],
    )
    write_csv(
        OUT_DIR / "by_month.csv",
        ["period", "qty", "revenue"],
        [[k, v["qty"], round_money(v["revenue"])]
         for k, v in sorted(months.items())],
    )
    write_csv(
        OUT_DIR / "by_product.csv",
        ["product", "qty", "revenue"],
        [[k, v["qty"], round_money(v["revenue"])]
         for k, v in sorted(products.items())],
    )

    return {
        "total": round_money(total),
        "count": len(by_amount),
        "avg": round_money(total / len(by_amount)) if by_amount else Decimal(0),
        "months": months,
        "products": products,
        "in_date": len(by_date),
        "source": len(sales),
    }


if __name__ == "__main__":
    sales = read_sales(SOURCE)
    stats = build(
        sales,
        start=datetime(2023, 1, 1),
        end=datetime(2023, 6, 30),
        low=Decimal("100"),
        high=Decimal("1000"),
    )
    print(f"Прочитано строк: {stats['source']}")
    print(f"После фильтра по датам: {stats['in_date']}")
    print(f"После фильтра по сумме: {stats['count']}")
    print(f"Сумма: {stats['total']}")
    print(f"Средний чек: {stats['avg']}")
    print()
    print("По месяцам:")
    for k, v in sorted(stats["months"].items()):
        print(f"  {k}  чеков {v['qty']:>4}  сумма {round_money(v['revenue'])}")
    print()
    print("По товарам:")
    for k, v in sorted(stats["products"].items(), key=lambda x: -x[1]["revenue"]):
        print(f"  {k:<12} чеков {v['qty']:>4}  сумма {round_money(v['revenue'])}")
