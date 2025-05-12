CREATE TABLE public.ticket (
	doc_id varchar NOT NULL,
	doc_dt timestamp NULL,
	item varchar NULL,
	category varchar NULL,
	amount float4 NULL,
	price float4 NULL,
	discount float4 NULL,
    shop_num int NULL,
    cash_num int NULL
);

-- Column comments

COMMENT ON COLUMN public.ticket.doc_id IS 'численно-буквенный идентификатор чека';
COMMENT ON COLUMN public.ticket.doc_dt IS 'дата и время покупки';
COMMENT ON COLUMN public.ticket.item IS 'название товара';
COMMENT ON COLUMN public.ticket.category IS 'категория товара';
COMMENT ON COLUMN public.ticket.amount IS 'кол-во товара в чеке';
COMMENT ON COLUMN public.ticket.price IS 'цена одной позиции без учета скидки';
COMMENT ON COLUMN public.ticket.discount IS 'сумма скидки на эту позицию (может быть 0)';
COMMENT ON COLUMN public.ticket.shop_num IS 'Номер магазина';
COMMENT ON COLUMN public.ticket.cash_num IS 'Номер кассы';
