import sys
import Bitrix24
import Kaspi

funnel_stage = 'C125:1'


deal = Bitrix24.get_deal(funnel_stage)

canceled, completed = Kaspi.kaspi_info_for_order(deal)

if not canceled and not completed:
    sys.exit()


if canceled:
    Bitrix24.movement_deals_canceled(canceled)

if completed:
    Bitrix24.movement_deals_completed(completed)