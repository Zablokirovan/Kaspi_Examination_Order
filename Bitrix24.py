import os

from fast_bitrix24 import Bitrix
from dotenv import load_dotenv

load_dotenv()

# Webhook in Bitrix24
webhook = os.getenv('BITRIX_WEBHOOK')
# Waits the required amount of time between
# requests to avoid exceeding Bitrix24 limits
b_time_delay = Bitrix(webhook, respect_velocity_policy=True)

def get_deal_wait_delivery():
    """

    :return:
    """
    try:
        with b_time_delay.slow(max_concurrent_requests=5):
            return b_time_delay.get_all('crm.deal.list',params={
                'filter': {
                    "STAGE_ID": 'C125:FINAL_INVOICE'
                },
                "select": [
                    "ID",
                    "UF_CRM_IM_ORDER_NUMBER"
                ],
            })
    except Exception as e:
        print(e)

print(get_deal_wait_delivery())