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

  SETU_CD = xxx（单位：秒）

  SETU_NUM = xxx （每次下载的图片张数，不大于100）

  

- **在bot.py中添加：**
  `nonebot.load_plugin("nonebot_plugin_setu")`



### 正式使用

#### 下载涩图

本插件采用的是下载和发送分离的方式，因此你必须先下载好涩图才能够发送，直接向机器人发送命令**下载涩图**即可，系统会自动下载好涩图存放在loliconImage里面（data的同级目录），一次默认下载量是80张

#### 发送涩图

向机器人发送命令**setu、涩图、色图、无内鬼**之一即可发送色图



# 更新日志

### 2022/3/5 [v1.0.1]

- 支持nonebot[v2.0.0-beta2]，请更新至最新版nonebot使用
- 更改图片的名字为对应pid
- 更改文件的配置方式，不再依赖.env文件



### 2022/1/26 [v1.0.0a1]

- 支持nonebot[v2.0.0-beta1]，beta1之前的请使用0.0.6版本
