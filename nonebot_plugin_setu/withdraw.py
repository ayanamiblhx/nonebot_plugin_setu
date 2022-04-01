from datetime import datetime, timedelta

from nonebot import require
from nonebot.adapters.onebot.v11 import Bot
from nonebot.log import logger

scheduler = require("nonebot_plugin_apscheduler").scheduler


def add_withdraw_job(bot: Bot, message_id: int, withdraw_interval: int = 0):
    if withdraw_interval:
        logger.debug("撤回消息定时任务开启")
        scheduler.add_job(
            withdraw_msg,
            "date",
            args=[bot, message_id],
            run_date=datetime.now() + timedelta(seconds=withdraw_interval),
        )


async def withdraw_msg(bot: Bot, message_id: int):
    await bot.delete_msg(message_id=message_id)
