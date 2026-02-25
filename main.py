import time
import os

import Bitrix24
import Kaspi
import config
import tg_bot


SLEEP_BETWEEN_STAGES_SEC = int(os.getenv("SLEEP_BETWEEN_STAGES_SEC", "5"))
SLEEP_BETWEEN_CYCLES_SEC = int(os.getenv("SLEEP_BETWEEN_CYCLES_SEC", str(20 * 60)))

def main():
    """
    Calling stages by timing
    :return:
    """

    while True:
        for stage in config.STAGE_ORDER:
            stage_id = config.FUNNEL_STAGE[stage]

            try:
                work_la_itl(stage_id)

            except Exception as e:
                tg_bot.telegram_send_messages(f"ERROR in stage {stage_id}: {e}")

            # Пауза между полными циклами
            time.sleep(SLEEP_BETWEEN_STAGES_SEC)

        time.sleep(SLEEP_BETWEEN_CYCLES_SEC)



def work_la_itl(stage_id):
    """
    Calling a function with specific parameters
    :param stage_id:
    :return:
    """
    deal = Bitrix24.get_deal(stage_id)
    canceled, completed = Kaspi.kaspi_info_for_order(deal)

    if not canceled and not completed:
        return

    if canceled:
        Bitrix24.movement_deals_canceled(canceled)

    if completed:
        Bitrix24.movement_deals_completed(completed)


if __name__ == "__main__":
    main()
