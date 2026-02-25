import os
import time

import requests
import tg_bot
from dotenv import load_dotenv

load_dotenv()

KASPI_TOKEN = os.getenv("KASPI_TOKEN")

URL = "https://kaspi.kz/shop/api/v2/orders"


def kaspi_info_for_order(deals):
    """
    Function for receiving information from Kaspi
    :param deals: list id order in Kaspi
    :return: list id for moving in bitrix24
    """

    canceled_list_deal = []
    completed_list_deal = []

    session = requests.Session()

    session.headers.update({
        "X-Auth-Token": KASPI_TOKEN,
        "Accept": "application/vnd.api+json;charset=UTF-8",
        "User-Agent": "KaspiOrderSync/1.0"
    })

    request_counter = 0

    for deal in deals:

        order_code = deal.get("UF_CRM_IM_ORDER_NUMBER")
        if not order_code:
            continue

        params = {
            "filter[orders][code]": order_code
        }

        try:
            response = session.get(
                URL,
                params=params,
                timeout=(5, 30)
            )

            response.raise_for_status()

            data = response.json()

            if not data.get("data"):
                continue

            status = data["data"][0]["attributes"]["state"]

            if status == "CANCELLED":
                canceled_list_deal.append(deal["ID"])

            elif status == "COMPLETED":
                completed_list_deal.append(deal["ID"])

            # Увеличиваем счётчик ТОЛЬКО если запрос реально был
            request_counter += 1

            # Каждые 50 запросов — пауза 10 секунд
            if request_counter % 50 == 0:
                time.sleep(10)

        except requests.exceptions.RequestException as e:
            tg_bot.telegram_send_messages(
                f'ERROR Kaspi_Examination_Order: '
                f'KASPI ОШИБКА: {e} '
                f'Данные для проверки: {order_code}'
            )
            raise

    session.close()
    return canceled_list_deal, completed_list_deal
