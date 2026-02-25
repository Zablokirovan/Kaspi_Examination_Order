import sys
import Bitrix24
import Kaspi
import argparse
import config
import tg_bot

funnel_stage = config.FUNNEL_STAGE


def main():
    """
    Calling stages by timing
    :return:
    """
    try:
        parser = argparse.ArgumentParser()
        # The tasks are specified in the config.py file.
        parser.add_argument("task", choices=list(funnel_stage.keys()))
        args = parser.parse_args()

        stage_id = funnel_stage[args.task]
        work_la_itl(stage_id)
    except Exception as e:
        tg_bot.telegram_send_messages("ERROR: Ошибка в parser "
                                      f"Kaspi_Examination_Order:{e}")



def work_la_itl(stage_id):
    """
    Calling a function with specific parameters
    :param stage_id:
    :return:
    """
    deal = Bitrix24.get_deal(stage_id)
    canceled, completed = Kaspi.kaspi_info_for_order(deal)

    if not canceled and not completed:
        sys.exit()

    if canceled:
        Bitrix24.movement_deals_canceled(canceled)

    if completed:
        Bitrix24.movement_deals_completed(completed)


if __name__ == "__main__":
    main()
