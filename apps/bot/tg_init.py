# from django.conf import settings
# from telegram.utils.request import Request
# from telegram.ext import messagequeue as mq
# from bot.utils.flood_limits import MQBot


# def telegram_bot():
#     # for test purposes limit global throughput to 3 messages per 3 seconds
#     q = mq.MessageQueue(all_burst_limit=3, all_time_limit_ms=3000)
#     # set connection pool size for bot
#     request = Request(con_pool_size=8)
#     bot = MQBot(
#         settings.BOT_TOKEN,
#         request=request,
#         mqueue=q
#     )
#     return bot


from django.conf import settings
from telegram import Bot


def telegram_bot():
    bot = Bot(settings.BOT_TOKEN)
    return bot