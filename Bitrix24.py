import os
import time

import tg_bot
from fast_bitrix24 import Bitrix
from dotenv import load_dotenv


load_dotenv()

# Webhook in Bitrix24
webhook = os.getenv('BITRIX_WEBHOOK')
# Waits the required amount of time between
# requests to avoid exceeding Bitrix24 limits
b_time_delay = Bitrix(webhook, respect_velocity_policy=True)


def get_deal(funnel_stage_id):
    """
    Getting deals from the funnel by stage filter
    :return: deal list
    """
    retries = 2
    # Прогон когда через время если возникла ошибка
    for attempt in range(1, retries + 1):

        try:
            with b_time_delay.slow(max_concurrent_requests=5):
                return b_time_delay.get_all(
                    'crm.deal.list',
                    params={
                        'filter': {"STAGE_ID": funnel_stage_id},
                        "select": ["ID", "UF_CRM_IM_ORDER_NUMBER"],
                    }
                )
        except Exception as e:
            if attempt == retries:
                tg_bot.telegram_send_messages(
                    f'ERROR get_deal stage={funnel_stage_id}: {e}'
                )
                raise
            time.sleep(5 * attempt)
    return None


def movement_deals_canceled(canceled):
    """
    Transferring transactions to the cancelled orders stage
    :param canceled: list id deals for closed
    :return:
    """

    request = 0

    for deal_id in canceled:

        try:

            with (b_time_delay.slow(max_concurrent_requests=5)):
                b_time_delay.get_all('crm.deal.update',
                                     params={"ID": deal_id,
                                             "FIELDS": {
                                                 "STAGE_ID": "C125:UC_KTFH3T"}
                                             })
                request+=1
                if request % 50 == 0:
                    time.sleep(10)

        except Exception as e:
            tg_bot.telegram_send_messages(f'ERROR Kaspi_Examination_Order:'
                                           f' Ошибка в переносе сделок ОТМЕНЕННЫХ: {e}')
            raise


def movement_deals_completed(completed):
    """
    Moving deals to the successful orders stage

    :param completed: list id deals for closed
    :return:
    """

    request = 0

    for deal_id in completed:

        try:

            with (b_time_delay.slow(max_concurrent_requests=5)):
                b_time_delay.get_all('crm.deal.update',
                                     params={"ID": deal_id,
                                             "FIELDS": {
                                                 "STAGE_ID": "C125:UC_Y17SVX"}
                                             })
                request += 1
                if request % 50 == 0:
                    time.sleep(10)

        except Exception as e:
            tg_bot.telegram_send_messages(f'ERROR Kaspi_Examination_Order:'
                                           f' Ошибка в переносе сделок УСПЕШНЫХ: {e}')
            raise