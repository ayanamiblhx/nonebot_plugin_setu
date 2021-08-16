import os
import nonebot
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Message, Event
from nonebot.adapters.cqhttp.message import MessageSegment
import random
import glob
from .getPic import getUrl
from .limit import readJson,writeJson,check,deleteJson
from nonebot.log import logger
from pathlib import Path

setu = on_command('setu', aliases={'无内鬼', '涩图', '色图'})
downLoad = on_command('下载涩图')
super_user = nonebot.get_driver().config.superusers

if not os.path.exists('loliconImages'):
    os.mkdir('loliconImages')
if not os.path.exists('data'):
    os.mkdir('data')
if not os.path.exists('data/userscd.json'):
    with open('data/userscd.json','w') as file:
        file.write('{}')
        file.close()

@setu.handle()
async def _(bot: Bot, event: Event):
    imgPath = Path("loliconImages").resolve()
    jpg = str(random.randint(0, len(glob.glob('loliconImages/*.jpg')) - 1)) + '.jpg'
    no_timeout,remain = check(event.get_user_id())
    if no_timeout or event.get_user_id() in super_user:
        try:
            await setu.send(('今日涩图' + MessageSegment.image(f"file:///{imgPath.joinpath(jpg)}")),at_sender=True)
        except Exception as e:
            logger.error('机器人被风控了' + str(e))
            await setu.send(message=Message('机器人被风控了,本次涩图不计入cd'), at_sender=True)
            deleteJson(event.get_user_id(), readJson())
    else:
        hour = int(remain / 3600)
        minute = int((remain / 60) % 60)
        await setu.send(f'要等{hour}小时{minute}分钟才能再要涩图哦', at_sender=True)

@downLoad.handle()
async def _(bot: Bot, event: Event):
    if event.get_user_id() in super_user:
        try:
            await getUrl('80')
            await downLoad.send('下载涩图成功',at_sender=True)
        except Exception as e:
            logger.error('下载时出现异常' + str(e))
            await downLoad.send(str(e),at_sender=True)
    else:
        await downLoad.send('只有主人才有权限哦', at_sender=True)


