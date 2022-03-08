import glob
import os
import random
import re
from pathlib import Path

from nonebot.adapters.onebot.v11 import Bot, Message, Event, MessageSegment
from nonebot.log import logger
from nonebot.plugin import on_command, on_regex

from .create_file import Config
from .getPic import get_url
from .limit import read_json, write_json, check, delete_json

setu = on_command('setu', aliases={'无内鬼', '涩图', '色图'})
downLoad = on_regex(r"^下载涩图[1-9]\d*$")
Config.create()
super_user = Config().super_users


@setu.handle()
async def _(bot: Bot, event: Event):
    img_path = Path("loliconImages").resolve()
    images = os.listdir(img_path)
    file_name = images[random.randint(0, len(glob.glob('loliconImages/*.jpg'))) - 1]
    no_timeout, remain = check(event.get_user_id())
    if no_timeout or event.get_user_id() in super_user:
        try:
            await setu.send((MessageSegment.image(f"file:///{img_path.joinpath(file_name)}") +
                             f"PID: {file_name.replace('.jpg', '')}"), at_sender=True)
        except Exception as e:
            logger.error('机器人被风控了' + str(e))
            await setu.send(message=Message('机器人被风控了,本次涩图不计入cd'), at_sender=True)
            delete_json(event.get_user_id(), read_json(r'data/userscd.json'))
    else:
        hour = int(remain / 3600)
        minute = int((remain / 60) % 60)
        await setu.send(f'要等{hour}小时{minute}分钟才能再要涩图哦', at_sender=True)


@downLoad.handle()
async def _(bot: Bot, event: Event):
    num = int(re.search(r"\d+", event.get_plaintext()).group())
    if event.get_user_id() in super_user:
        try:
            await downLoad.send(f"开始下载...")
            await get_url(num)
            await downLoad.send(f"下载涩图成功,图库中涩图数量{len(glob.glob('loliconImages/*.jpg'))}", at_sender=True)
        except Exception as e:
            logger.error(f'下载时出现异常{e}')
            await downLoad.send(str(e), at_sender=True)
    else:
        await downLoad.send('只有主人才有权限哦', at_sender=True)
