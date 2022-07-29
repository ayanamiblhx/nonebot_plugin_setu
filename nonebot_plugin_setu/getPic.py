import base64
import json
from io import BytesIO

from httpx import AsyncClient, ConnectTimeout
from nonebot.log import logger
from tqdm import tqdm

from .create_file import Config
from .dao.image_dao import ImageDao
from .proxies import proxy_http, proxy_socks


async def get_url(num: int, online_switch: int, tags: list, r18: int = 0):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.36",
    }
    params = {
        "r18": r18,
        "size": 'regular',
        "tag": tags,
    }
    async with AsyncClient(proxies=None) as client:
        times = int(num / 20) + 1
        remain = num % 20
        datas = []
        try:
            for i in range(times):
                num = 20 if i != times - 1 else remain
                print(num)
                if num == 0:
                    break
                req_url = f"https://api.lolicon.app/setu/v2?num={num}"
                res = await client.get(req_url, params=params, headers=head, timeout=10.0)
                res = json.loads(res.text)
                data = res['data']
                if not data:
                    return ""
                datas.extend(data)
            ImageDao().add_images(datas)
            img = await down_pic(datas, online_switch, r18)
            return img
        except Exception as e:
            logger.error(e)
            raise e


async def down_pic(datas, online_switch: int, r18: int = 0):
    head = {
        'referer': 'https://www.pixiv.net/',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.36"
    }
    http = proxy_http if Config().proxies_switch else None
    socks = proxy_socks if Config().proxies_switch else None
    async with AsyncClient(proxies=http, transport=socks) as client:
        pbar = tqdm(datas, desc='Downloading', colour='green')
        tag_img = ""
        for data in datas:
            proxy_url = data['urls']['regular'].replace('i.pixiv.cat', 'i.pximg.net')
            url = data['urls']['regular'].replace('i.pixiv.cat', 'i.pixiv.re')
            url = proxy_url if Config().proxies_switch else url
            pid = data['pid']
            ext = data['ext']
            tag_img = str(pid) + "." + ext
            try:
                response = await client.get(url=url, headers=head, timeout=10.0)
                pbar.update(1)
                if online_switch == 1:
                    img_info = {'pid': pid,
                                'base64': f"base64://{base64.b64encode(BytesIO(response.content).getvalue()).decode()}"}
                    return img_info
                img_path = f"loliconImages/{'r18/' if r18 else ''}{pid}.{ext}"
                with open(img_path, 'wb') as f:
                    f.write(response.content)
            except ConnectTimeout:
                pass
            except Exception as e:
                raise e
        pbar.close()
        return tag_img
