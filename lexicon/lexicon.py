LEXICON: dict[str, str] = {
    'ord_info': '''<b>Информация по заказу {DEPNO}/{ID_DOC}</b>\n
    <u>Готовность заказа</u>
    Контура: {ORDER_CONTOURS}
    М/с: {ORDER_MS}
    Подоконники: {ORDER_MS}

    <u>Информация о доставке</u>
    Маршрут: {ID_TRANS}
    Дата доставки: {TRANS_DATE}
    Водитель: {DRIVER}'''
}


'''ID_DOC,
DEPNO,
DOCNUM,
DOG_NO,
DOCDATE,
FINDATE,
ADRES_DEST,
DT_ENTRY,
DT_PRODUCT,
DT_DELIVERY,
IS_FACT,
SYMA,
ORDER_CONTOURS,
ORDER_MS,
ORDER_WINDOWSILLS,
ORDER_OTLIVS,
ID_TRANS,
TRANS_DATE,
DRIVER,
CAR'''