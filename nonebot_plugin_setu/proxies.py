from httpx_socks import AsyncProxyTransport
from nonebot.log import logger

from .create_file import Config

proxy_config = Config()

socks = proxy_config.proxies_socks
http = proxy_config.proxies_http
if socks != '':
    logger.info('已配置socks代理')
    proxy_socks = AsyncProxyTransport.from_url(socks)
    proxy_http = None
elif http != '':
    logger.info('已配置http代理')
    proxy_socks = None
    proxy_http = http
else:
    logger.info('未配置代理')
    proxy_socks = None
    proxy_http = None
