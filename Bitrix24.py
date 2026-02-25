import os

from fast_bitrix24 import Bitrix
from dotenv import load_dotenv

load_dotenv()

# Webhook in Bitrix24
webhook = os.getenv('BITRIX_WEBHOOK')
# Waits the required amount of time between
# requests to avoid exceeding Bitrix24 limits
b_time_delay = Bitrix(webhook, respect_velocity_policy=True)

#TODO НУЖНО НАПИСАТЬ ЛОГИКУ ОБРАБОТОК ОШИБОК В ТЕЛЕГРАМ
#TODO ПОДПИСАТЬ КАЖДУЮ ФУНКЦИЮ
def get_deal(funnel_stage_id):
    """

    :return:
    """
    try:
        with b_time_delay.slow(max_concurrent_requests=5):
            return b_time_delay.get_all('crm.deal.list',params={
                'filter': {
                    "STAGE_ID": funnel_stage_id
                },
                "select": [
                    "ID",
                    "UF_CRM_IM_ORDER_NUMBER"
                ],
            })
    except Exception as e:
        print(e)
