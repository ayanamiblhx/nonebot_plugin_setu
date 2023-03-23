from httpx_socks import AsyncProxyTransport
from nonebot.log import logger

from .file_tools import Config

proxy_config = Config()

socks = proxy_config.get_file_args('PROXIES_SOCKS')
http = proxy_config.get_file_args('PROXIES_HTTP')
if socks != '':
    logger.info('已配置socks代理,http代理将被忽略')
    proxy_config.set_file_args('PROXIES_SWITCH', 1)
    proxy_socks = AsyncProxyTransport.from_url(socks)
    proxy_http = None
elif http != '':
    logger.info('已配置http代理,socks代理将被忽略')
    proxy_config.set_file_args('PROXIES_SWITCH', 1)
    proxy_socks = None
    proxy_http = http
else:
    logger.info('未配置代理')
    proxy_config.set_file_args('PROXIES_SWITCH', 0)
    proxy_socks = None
    proxy_http = None
