from fastapi import FastAPI, Query, Body
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi.responses import RedirectResponse

from .dao.image_dao import ImageDao

setu_api = FastAPI(
    title="涩图Api",
    version="1.1.1",
    contact={
        "name": "nonebot_plugin_setu",
        "url": "https://github.com/ayanamiblhx/nonebot_plugin_setu"
    }
)


class SetuItem(BaseModel):
    pid: str = Field(None, max_length=20, description="pid", example="")
    uid: str = Field(None, max_length=20, description="uid", example="")
    num: Optional[int] = Field(1, ge=1, le=100, description="图片数量，默认为1，最大为100")
    proxy: bool = Field(False, description="是否使用代理，默认不使用")
    tags: Optional[List[str]] = Field(None, description="标签，最多3个", max_items=3, example=["碧蓝航线", "碧蓝幻想"])
    r18: bool = False


@setu_api.get("/v1", tags=["获取涩图"], description="GET请求")
async def get_img(pid: str = Query(None, max_length=20, description="pid"),
                  uid: str = Query(None, max_length=20, description="uid"),
                  num: Optional[int] = Query(1, ge=1, le=100, description="图片数量，默认为1，最大为100"),
                  tags: Optional[List[str]] = Query(None, max_items=3, description="标签，最多3个"),
                  proxy: bool = Query(False, description="是否使用代理地址，默认不使用"),
                  r18: bool = False):
    if pid is not None and pid != "":
        datas = ImageDao().get_images_by_pid(pid=pid)
    elif uid is not None and uid != "":
        datas = ImageDao().get_images_by_uid(uid=uid, num=num, r18=r18)
    elif tags is not None and tags.__len__() > 0:
        datas = ImageDao().get_images_by_tags(tags=tags, r18=r18, num=num)
    else:
        datas = ImageDao().get_random_images(num=num, r18=r18)
    if proxy:
        for data in datas['data']:
            data['urls']['regular'] = data["urls"]['regular'].replace('i.pixiv.cat', 'i.pixiv.re')
    else:
        for data in datas['data']:
            data["urls"]['regular'] = data["urls"]['regular'].replace('i.pixiv.cat', 'i.pximg.net')
    return datas


@setu_api.post("/v1", tags=["获取涩图"], description="POST请求")
async def post_img(setu_item: SetuItem = Body(...)):
    if setu_item.pid is not None and setu_item.pid != "":
        datas = ImageDao().get_images_by_pid(pid=setu_item.pid)
    elif setu_item.uid is not None and setu_item.uid != "":
        datas = ImageDao().get_images_by_uid(**setu_item.dict())
    elif setu_item.tags is not None and setu_item.tags.__len__() > 0:
        datas = ImageDao().get_images_by_tags(**setu_item.dict())
    else:
        datas = ImageDao().get_random_images(num=setu_item.num, r18=setu_item.r18)
    if setu_item.proxy:
        for data in datas['data']:
            data['urls']['regular'] = data["urls"]['regular'].replace('i.pixiv.cat', 'i.pixiv.re')
    else:
        for data in datas['data']:
            data["urls"]['regular'] = data["urls"]['regular'].replace('i.pixiv.cat', 'i.pximg.net')
    return datas
