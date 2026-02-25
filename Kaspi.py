import os
import requests
from dotenv import load_dotenv

load_dotenv()

KASPI_TOKEN = os.getenv("KASPI_TOKEN")

URL = f"https://kaspi.kz/shop/api/v2/orders"


def kaspi_info_for_order(deals):
    canceled_list_deal = []
    completed_list_deal = []

    Session = requests.session()

    Session.headers.update({
        "X-Auth-Token": KASPI_TOKEN,
        "Accept": "application/vnd.api+json;charset=UTF-8",
        "User-Agent": "KaspiOrderSync/1.0"
    })

    for deal in deals:
        order_code = deal.get("UF_CRM_IM_ORDER_NUMBER")
        if not order_code:
            continue

        parms = {
            "filter[orders][code]":order_code
        }

        try:
            response = Session.get(
                URL,
                params=parms,
                timeout=(5, 30)
            )
            print(response)
            response.raise_for_status()

            data = response.json()
            print(data)

            if not data.get("data"):
                continue

            status = data["data"][0]["attributes"]["state"]

            if status == "CANCELLED":
                canceled_list_deal.append(deal["ID"])

            elif status == "COMPLETED":
                completed_list_deal.append(deal["ID"])

        except requests.exceptions.RequestException as e:
            print(f"Kaspi error for deal {deal.get('ID')}: {e}")

    return canceled_list_deal, completed_list_deal