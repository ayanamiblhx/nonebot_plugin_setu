import asyncio
from nonebot.adapters.onebot.v11 import Bot
from nonebot.log import logger


async def add_withdraw_job(bot: Bot, message_id: int, withdraw_interval: int = 0):
    if withdraw_interval:
        tasks = []
        logger.info(f'添加撤回定时任务，撤回间隔：{withdraw_interval}秒')
        tasks.append(withdraw_msg(bot, message_id))
        await asyncio.sleep(withdraw_interval)
        asyncio.gather(*tasks).add_done_callback(lambda x: logger.info(f'撤回任务已完成，撤回消息id：{message_id}'))


async def withdraw_msg(bot: Bot, message_id: int):
    await bot.delete_msg(message_id=message_id)
