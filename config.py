FUNNEL_STAGE = {
    "new": "C125:NEW",#Новая
    "address_confirm": "C125:PREPARATION",#подтверждение адреса
    "selling_services": "C125:PREPAYMENT_INVOI",# продажа услуг
    "wait_cancelled": "C125:EXECUTING",#Ждем Отмену
    "awaiting_delivery": "C125:FINAL_INVOICE",#Ожидает доставку
    "kaspi_express": "C125:UC_E17ICW",#KASPI EXPRESS
    "kaspi_delivery": "C125:1",# Каспи доставка
}


STAGE_ORDER = [
    "kaspi_delivery",
    "address_confirm",
    "selling_services",
    "awaiting_delivery",
    "wait_cancelled",
    "kaspi_express",
]