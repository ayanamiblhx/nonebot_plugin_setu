import os
from typing import List

from nonebot.adapters.onebot.v11 import Bot, Message, Event

from .file_tools import Config


async def send_forward_msg(
        bot: Bot,
        event: Event,
        name: str,
        uin: str,
        msgs: List,
        is_group_chat: bool,
):
    def to_json(msg: Message):
        return {"type": "node", "data": {"name": name, "uin": uin, "content": msg}}
    messages = [to_json(msg) for msg in msgs]
    forward_api = 'send_private_forward_msg' if not is_group_chat else 'send_group_forward_msg'
    if is_group_chat:
        return await bot.call_api(forward_api, group_id=event.group_id, messages=messages)
    else:
        return await bot.call_api(forward_api, user_id=event.get_user_id(), messages=messages)


def get_file_num(path):
    file_num = 0
    for root, dirs, files in os.walk(path):
        file_num += len(files)
    return file_num


def img_num_detect(r18: int):
    if os.listdir('loliconImages').__len__() == 1 and not Config().online_switch:
        return 0
    elif os.listdir('loliconImages/r18').__len__() == 0 \
            and r18 == 1 and not Config().online_switch:
        return 0
    else:
        return 1
