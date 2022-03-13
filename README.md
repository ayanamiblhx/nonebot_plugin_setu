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

  注意: 确保能够访问相关服务后才能下载涩图(二者填其一，海外服务器可不填)

  PROXIES_HTTP = 'HTTP魔法地址(例如`http://127.0.0.1:7890`)，这与你使用的魔法有关'

  PROXIES_SOCKS = 'SOCKS5魔法地址(例如`socks5://127.0.0.1:10808`)，这与你使用的魔法有关'

  

- **在bot.py中添加：**
  `nonebot.load_plugin("nonebot_plugin_setu")`



### 正式使用

| 说明       | 命令                     | 举例          |
| :--------- | ------------------------ | ------------- |
| 下载图片   | 下载涩图+数量            | 下载涩图12345 |
| 发送图片   | 涩图、setu、无内鬼、色图 | setu          |
| 指定用户cd | @用户cd+时间（秒）       | @张三cd12345  |
| 指定群cd   | 群cd+时间（秒）          | 群cd12345     |

#### 注：

- 用户cd和群cd同时存在时，以用户cd为准
- 群cd默认3600s

## TODO

- [ ] 选择`在线/下载`发图
- [x] 指定群CD和用户CD
- [ ] 是否使用PROXY
- [ ] 指定TAG
- [ ] 数据可视化



# 更新日志

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
