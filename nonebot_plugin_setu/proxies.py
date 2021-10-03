from httpx_socks import AsyncProxyTransport
import nonebot
from nonebot.log import logger

global_config = nonebot.get_driver().config

socks = global_config.proxies_socks
http = global_config.proxies_http
if socks is not None:
    logger.info('已配置socks代理')
    proxy_socks = AsyncProxyTransport.from_url(socks)
    proxy_http = None
elif http is not None:
    logger.info('已配置http代理')
    proxy_socks = None
    proxy_http = http
else:
    logger.info('未配置代理')
    proxy_socks = None
    proxy_http = None
