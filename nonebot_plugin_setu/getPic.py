from httpx import AsyncClient
import json
from nonebot.log import logger
from .proxies import proxy_http, proxy_socks


async def get_url(num: str):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    }
    req_url = f"https://api.lolicon.app/setu?num={num}"
    params = {
        "r18": 0,
        "size": 'regular',
    }
    async with AsyncClient() as client:
        res = await client.get(req_url, params=params, headers=head, timeout=10.0)
        try:
            res = json.loads(res.text)
            datas = res['data']
            await down_pic(datas)
        except Exception as e:
            logger.error(e)
            raise e


async def down_pic(datas):
    head = {
        'referer': 'https://www.pixiv.net/',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    async with AsyncClient(proxies=proxy_http, transport=proxy_socks) as client:
        for data in datas:
            url = data['url'].replace('i.pixiv.cat', 'i.pximg.net')
            pid = data['pid']
            response = await client.get(url=url, headers=head, timeout=10.0)
            img_path = f'loliconImages/{pid}.jpg'
            with open(img_path, 'wb') as f:
                try:
                    f.write(response.content)
                except TimeoutError:
                    pass
                except Exception as e:
                    raise e
