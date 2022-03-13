import os
import random
import re
from datetime import datetime
from pathlib import Path

from nonebot.adapters.onebot.v11 import Bot, Message, Event, MessageSegment
from nonebot.log import logger
from nonebot.plugin import on_command, on_regex

from .create_file import Config
from .dao.image_dao import ImageDao
from .dao.usercd_dao import UserCdDao
from .dao.groupcd_dao import GroupCdDao
from .getPic import get_url

setu = on_command('setu', aliases={'无内鬼', '涩图', '色图'})
downLoad = on_regex(r"^下载涩图[1-9]\d*$")
user_cd = on_regex(r"^\[CQ:at,qq=[1-9][0-9]{4,10}\] cd\d+$")
group_cd = on_regex(r"^群cd0$|^群cd[1-9]\d*$")

Config.create_file()
Config.create_table()
super_user = Config().super_users


@setu.handle()
async def _(bot: Bot, event: Event):
    img_path = Path("loliconImages").resolve()
    images = os.listdir(img_path)
    file_name = images[random.randint(0, len(os.listdir('loliconImages'))) - 1]
    file_name = re.sub(r'\D+', '', file_name)
    img_info = ImageDao().get_images(file_name)
    ext = img_info['ext']
    remain_time = 0 if event.get_user_id() in Config().super_users else UserCdDao().get_user_remain_time(
        event.get_user_id(), event.group_id)
    if remain_time == 0:
        try:
            await setu.send((MessageSegment.image(f"file:///{img_path.joinpath(file_name)}.{ext}") +
                             f"https://www.pixiv.net/artworks/{file_name}"), at_sender=True)
        except Exception as e:
            logger.error(f'机器人被风控了{e}')
            await setu.send(message=Message('机器人被风控了,本次涩图不计入cd'), at_sender=True)
            UserCdDao().delete_user_cd(event.get_user_id())
    else:
        hour = int(remain_time / 3600)
        minute = int((remain_time / 60) % 60)
        await setu.send(f'要等{hour}小时{minute}分钟才能再要涩图哦', at_sender=True)


@downLoad.handle()
async def _(bot: Bot, event: Event):
    num = int(re.search(r"\d+", event.get_plaintext()).group())
    if event.get_user_id() in super_user:
        try:
            await downLoad.send(f"开始下载...")
            await get_url(num)
            await downLoad.send(f"下载涩图成功,图库中涩图数量{len(os.listdir('loliconImages'))}", at_sender=True)
        except Exception as e:
            logger.error(f'下载时出现异常{e}')
            await downLoad.send(str(e), at_sender=True)
    else:
        await downLoad.send('只有主人才有权限哦', at_sender=True)


@user_cd.handle()
async def _(bot: Bot, event: Event):
    msg = event.get_message()
    user_id = event.get_user_id()
    if user_id in super_user:
        user_id = msg[0].get('data')['qq']
        cd = int(event.get_plaintext().replace(' cd', ''))
        user = UserCdDao().get_user(user_id)
        if user is None:
            UserCdDao().add_user_cd(user_id, UserCdDao.datetime_to_seconds(datetime.now()), cd)
        else:
            UserCdDao().update_user_cd(user_id, '', cd)
        await user_cd.send(f'设置用户{user_id}的cd成功,cd时间为{cd}s', at_sender=True)
    else:
        await user_cd.send('只有主人才有权限哦', at_sender=True)


@group_cd.handle()
async def _(bot: Bot, event: Event):
    user_id = event.get_user_id()
    if user_id in super_user:
        cd = int(event.get_plaintext().replace('群cd', ''))
        group_id = GroupCdDao().get_group_cd(event.group_id)
        if group_id is None:
            GroupCdDao().set_group_cd(event.group_id, cd)
        else:
            GroupCdDao().update_group_cd(event.group_id, cd)
        await group_cd.send(f'设置群{event.group_id}的cd成功,cd时间为{cd}s', at_sender=True)
    else:
        await group_cd.send('只有主人才有权限哦', at_sender=True)
