import nonebot
from httpx import AsyncClient
import aiohttp
import json
import aiofiles
import glob
from nonebot.log import logger

local_proxy = nonebot.get_driver().config.local_proxy

async def getUrl(num:str):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    }
    req_url = "https://api.lolicon.app/setu?num="+num
    params = {
        "r18": 0,
        "size1200": 'true',
    }
    async with aiohttp.ClientSession(headers=head) as session:
        async with session.get(url=req_url,params=params) as response:
            res = await response.read()
            try:
                res = json.loads(res.decode('utf-8'))
                datas = res['data']
                await downPic(datas)
            except Exception as e:
                logger.error(e)
                logger.error(res.txt)


async def downPic(datas):
    async with AsyncClient() as client:
        head = {
            'referer': 'https://www.pixiv.net/',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        }
        async with aiohttp.ClientSession(headers=head) as session:
            for data in datas:
                url = data['url'].replace('i.pixiv.cat','i.pximg.net')
                async with session.get(url=url,proxy=local_proxy,timeout=10) as response:
                    index = len(glob.glob('./loliconImages/*.jpg'))
                    img_path = 'loliconImages/' + str(index) + '.jpg'
                    async with aiofiles.open(img_path, 'wb') as f:
                        try:
                            await f.write(await response.read())
                        except TimeoutError:
                            pass