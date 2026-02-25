import Bitrix24
import Kaspi

funnel_stage = 'C125:FINAL_INVOICE'


deal = Bitrix24.get_deal(funnel_stage)

canceled, completed = Kaspi.kaspi_info_for_order(deal)


