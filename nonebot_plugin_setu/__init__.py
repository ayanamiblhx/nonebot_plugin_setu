import json
import os
import random
import re
from datetime import datetime
from pathlib import Path

from nonebot.adapters.onebot.v11 import Bot, Message, Event, MessageSegment
from nonebot.log import logger
from nonebot.plugin import on_regex
from nonebot import get_driver

from .create_file import Config
from .dao.group_dao import GroupDao
from .dao.image_dao import ImageDao
from .dao.user_dao import UserDao
from .getPic import get_url, down_pic
from .setu_api import setu_api
from .withdraw import add_withdraw_job

setu = on_regex("^涩图$|^setu$|^无内鬼$|^色图$|^涩图tag.+$")
downLoad = on_regex(r"^下载涩图[1-9]\d*$|^下载色图[1-9]\d*$")
user_cd = on_regex(r"^\[CQ:at,qq=[1-9][0-9]{4,10}\] cd\d+$")
group_cd = on_regex(r"^群cd0$|^群cd[1-9]\d*$")
online_switch = on_regex(r"^开启在线发图$|^关闭在线发图$")
proxy_switch = on_regex(r"^开启魔法$|^关闭魔法$")
api = on_regex(r"^涩图api$|^设置api地址.+$")
withdraw_interval = on_regex(r"^撤回间隔0$|^撤回间隔[1-9]\d*$")
r18_switch = on_regex(r"^开启涩涩$|^关闭涩涩$|^开启私聊涩涩$|^关闭私聊涩涩$")

super_user = Config().super_users
driver = get_driver()
driver.server_app.mount('/setu', setu_api, name='setu_plugin')


@setu.handle()
async def _(bot: Bot, event: Event):
    r18 = UserDao().get_r18_private_chat() \
        if not hasattr(event, 'group_id') else GroupDao().get_group_r18(event.group_id)
    img_path = Path(f"loliconImages{'/r18' if r18 else ''}").resolve()
    images = os.listdir(img_path)
    if r18 == 0:
        images.remove('r18')
    file_name = images[random.randint(0, len(os.listdir(img_path))) - 1]
    pid = re.sub(r'\D+', '', file_name)
    remain_time = 0 if event.get_user_id() in Config().super_users else UserDao().get_user_remain_time(
        event.get_user_id(), event.group_id)
    if remain_time == 0:
        try:
            msg = event.get_plaintext()
            tag_flag = 0
            if bool(re.search(r"^涩图tag.+$", msg)):
                tag_flag = 1
                tags = re.sub(r'^涩图tag', '', msg).split('和')
                if len(tags) > 3:
                    UserDao().delete_user_cd(event.get_user_id())
                    await setu.send('涩图tag最多只能有三个哦', at_sender=True)
                    return
                else:
                    file_name = await get_url(num=1, tags=tags, online_switch=Config().online_switch, r18=r18)
                    if Config().online_switch == 0:
                        pid = re.sub(r'\D+', '', file_name)
                    if file_name == "":
                        UserDao().delete_user_cd(event.get_user_id())
                        await setu.send('没有找到相关涩图，请更换tag', at_sender=True)
                        return
            interval = 0 if not hasattr(event, 'group_id') else GroupDao().get_group_interval(event.group_id)
            if Config().online_switch == 1:
                img = file_name if tag_flag == 1 else await get_url(num=1, online_switch=1, tags="", r18=r18)
                msg_info = await setu.send(MessageSegment.image(img['base64']) +
                                           f"https://www.pixiv.net/artworks/{img['pid']}", at_sender=True)
                add_withdraw_job(bot, **msg_info, withdraw_interval=interval)
                return
            msg_info = await setu.send(MessageSegment.image(f"file:///{img_path.joinpath(file_name)}") +
                                       f"https://www.pixiv.net/artworks/{pid}", at_sender=True)
            add_withdraw_job(bot, **msg_info, withdraw_interval=interval)
        except Exception as e:
            logger.error(f'机器人被风控了{e}')
            UserDao().delete_user_cd(event.get_user_id())
            await setu.finish(message=Message('机器人被风控了,本次涩图不计入cd'), at_sender=True)
    else:
        hour = int(remain_time / 3600)
        minute = int((remain_time / 60) % 60)
        await setu.finish(f'要等{hour}小时{minute}分钟才能再要涩图哦', at_sender=True)


@downLoad.handle()
async def _(bot: Bot, event: Event):
    num = int(re.search(r"\d+", event.get_plaintext()).group())
    if event.get_user_id() in super_user:
        try:
            r18 = 1 if event.get_plaintext().find('色图') != -1 else 0
            await downLoad.send(f"开始下载...")
            await get_url(num=num, online_switch=0, tags="", r18=r18)
            await downLoad.send(f"下载涩图成功,图库中涩图数量{get_file_num('loliconImages')}", at_sender=True)
        except Exception as e:
            logger.error(f'下载时出现异常{e}')
            await downLoad.send(str(e), at_sender=True)
    else:
        await downLoad.send('只有主人才有权限哦', at_sender=True)


def get_file_num(path):
    file_num = 0
    for root, dirs, files in os.walk(path):
        file_num += len(files)
    return file_num


@user_cd.handle()
async def _(bot: Bot, event: Event):
    msg = event.get_message()
    user_id = event.get_user_id()
    if user_id in super_user:
        user_id = msg[0].get('data')['qq']
        cd = int(event.get_plaintext().replace(' cd', ''))
        user = UserDao().get_user(user_id)
        if user is None:
            UserDao().add_user_cd(user_id, UserDao.datetime_to_seconds(datetime.now()), cd)
        else:
            UserDao().update_user_cd(user_id, '', cd)
        await user_cd.send(f'设置用户{user_id}的cd成功,cd时间为{cd}s', at_sender=True)
    else:
        await user_cd.send('只有主人才有权限哦', at_sender=True)


@group_cd.handle()
async def _(bot: Bot, event: Event):
    user_id = event.get_user_id()
    if user_id in super_user:
        cd = int(event.get_plaintext().replace('群cd', ''))
        if not hasattr(event, 'group_id'):
            await group_cd.send('请在群里使用', at_sender=True)
        group_id = GroupDao().get_group_cd(event.group_id)
        if group_id is None:
            GroupDao().set_group_cd(event.group_id, cd)
        else:
            GroupDao().update_group_cd(event.group_id, cd)

        await group_cd.send(f'设置群{event.group_id}的cd成功,cd时间为{cd}s', at_sender=True)
    else:
        await group_cd.send('只有主人才有权限哦', at_sender=True)


@online_switch.handle()
async def _(bot: Bot, event: Event):
    msg = event.get_plaintext()
    switch = 1 if msg == "开启在线发图" else 0
    if event.get_user_id() in super_user:
        with open('data/setu_config.json', 'r') as file:
            configs = json.load(file)
            configs['ONLINE_SWITCH'] = switch
            with open('data/setu_config.json', 'w') as f:
                json.dump(configs, f)
                await online_switch.send(f'{msg}成功')
    else:
        await online_switch.send('只有主人才有权限哦', at_sender=True)


@proxy_switch.handle()
async def _(bot: Bot, event: Event):
    msg = event.get_plaintext()
    switch = 1 if msg == "开启魔法" else 0
    if event.get_user_id() in super_user:
        with open('data/setu_config.json', 'r') as file:
            configs = json.load(file)
            configs['PROXIES_SWITCH'] = switch
            with open('data/setu_config.json', 'w') as f:
                json.dump(configs, f)
                await proxy_switch.send(f'{msg}成功')
    else:
        await proxy_switch.send('只有主人才有权限哦', at_sender=True)


@withdraw_interval.handle()
async def _(bot: Bot, event: Event):
    msg = event.get_plaintext()
    interval = int(msg.replace('撤回间隔', ''))
    if event.get_user_id() in super_user:
        if interval > 120:
            await withdraw_interval.send('间隔不能超过120s', at_sender=True)
        else:
            if not hasattr(event, 'group_id'):
                await withdraw_interval.finish("请在群里使用此功能")
            group_id = event.group_id
            GroupDao().set_or_update_group_interval(group_id=group_id, interval=interval)
            await withdraw_interval.send(f'设置群{group_id}撤回间隔{interval}s成功')
    else:
        await withdraw_interval.send('只有主人才有权限哦', at_sender=True)


@api.handle()
async def _(bot: Bot, event: Event):
    msg = event.get_plaintext()
    if msg == '涩图api':
        if ImageDao().get_api() is None:
            await api.send(f'请设置api地址(格式：http://服务器公网ip或域名:机器人端口)')
        else:
            await api.send(
                f'涩图api已开启,请访问\n{ImageDao().get_api()}/setu/docs\n{ImageDao().get_api()}/setu/redoc\n查看api文档')
    else:
        if event.get_user_id() in super_user:
            address = re.sub('^设置api地址', '', msg)
            ImageDao().set_or_update_api(address)
            await api.send(f"设置api地址{address}成功")
        else:
            await api.send("只有主人才有权限哦", at_sender=True)


@r18_switch.handle()
async def _(bot: Bot, event: Event):
    msg = event.get_plaintext()
    if event.get_user_id() in super_user:
        if msg == "开启涩涩" or msg == "关闭涩涩":
            if not hasattr(event, 'group_id'):
                await r18_switch.finish('私聊请使用开启/关闭私聊涩涩')
            GroupDao().set_or_update_group_r18(event.group_id, 1 if msg == "开启涩涩" else 0)
            await r18_switch.finish(f"群{event.group_id}{msg}成功")
        else:
            UserDao().set_or_update_r18(1 if msg == "开启私聊涩涩" else 0)
            await r18_switch.finish(f"{msg}成功")
    else:
        await r18_switch.finish('只有主人才有权限哦', at_sender=True)
