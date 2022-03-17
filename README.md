<div align=center>
	<img src="https://s4.ax1x.com/2022/03/05/bw2k9A.png" alt="bw2k9A.png" border="0"/>
</div>

# nonebot_plugin_setu

基于nonebot2、loliconApi的涩图插件



## 安装及更新

- 使用`nb plugin install nonebot_plugin_setu`或者`pip install nonebot_plugin_setu`来进行安装
- 使用`nb plugin update nonebot_plugin_setu`或者`pip install nonebot_plugin_setu -U`来进行更新



## 使用方式

首先运行一遍robot，然后在robot目录的data目录下修改setu_config.json配置文件，然后重启robot



### 添加配置

- **在你的setu_config.json文件中修改如下配置：**

  SUPERUSERS = ["主人的qq号"]，可添加多个

  PROXIES_HTTP = 'HTTP魔法地址(例如`http://127.0.0.1:7890`)，这与你使用的魔法有关'

  PROXIES_SOCKS = 'SOCKS5魔法地址(例如`socks5://127.0.0.1:10808`)，这与你使用的魔法有关'

  **注**：若没有魔法或者不会设置可不填

  

- **在bot.py中添加：**
  `nonebot.load_plugin("nonebot_plugin_setu")`



### 正式使用

| 命令                     | 举例          | 说明                                                         |
| ------------------------ | ------------- | :----------------------------------------------------------- |
| 下载涩图+数量            | 下载涩图12345 | 下载图片                                                     |
| 涩图、setu、无内鬼、色图 | setu          | 发送图片                                                     |
| @用户cd+时间（秒）       | @张三cd12345  | 指定用户cd                                                   |
| 群cd+时间（秒）          | 群cd12345     | 指定群cd                                                     |
| 开启/关闭在线发图        | 开启在线发图  | 在线发图开启之后，图片将不再从本地发送而是从网上下载后在线发送，不会占用服务器存储资源 |
| 开启/关闭魔法            | 关闭魔法      | 魔法关闭之后，图片的下载以及在线发送将不再通过魔法而是通过镜像来完成，如果没有魔法或者不会设置推荐关闭 |

#### 注：

- 用户cd和群cd同时存在时，以用户cd为准
- 群cd默认3600s

## TODO

- [x] 选择`在线/下载`发图
- [x] 指定群CD和用户CD
- [x] 是否使用PROXY
- [ ] 指定TAG
- [ ] 数据可视化



# 更新日志

### 2022/3/17[v1.0.9]

- 新增在线发图开关，图片可以在线发送而不占用服务器存储空间
- 新增魔法开关，没有魔法也能够正常使用

注：旧版本用户请删除setu_config.json然后重新配置一遍



### 2022/3/13[v1.0.5]

- 删除SETU_CD，修改cd配置，不再依赖userscd.json，转为依赖数据库文件
- 添加用户cd和群cd，可由管理员进行指定和更改
- 引入数据库存储图片信息，修改图片存储格式从jpg转为图片原本对应样式

注：旧版本用户请删除setu_config.json然后重新配置一遍



### 2022/3/9[v1.0.4]

- 更改异常捕获范围，修复无法捕获异常的bug



### 2022/3/8[v1.0.3]

- 删除配置：SETU_NUM，可下载指定数量的图片
- 新增下载图片进度条



### 2022/3/5 [v1.0.1]

- 支持nonebot[v2.0.0-beta2]，请更新至最新版nonebot使用
- 更改图片的名字为对应pid
- 更改文件的配置方式，不再依赖.env文件



### 2022/1/26 [v1.0.0a1]

- 支持nonebot[v2.0.0-beta1]，beta1之前的请使用0.0.6版本
