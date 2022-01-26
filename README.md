# nonebot_plugin_setu
基于nonebot2、loliconImage的涩图插件



## 使用方式

### 添加配置

```
在你的.env文件中添加如下配置：
SUPERUSERS=["主人的qq号"]
#注意: 确保能够访问相关服务后才能下载涩图(二者填其一，海外服务器可不填)
PROXIES_HTTP='HTTP魔法地址(例如http://127.0.0.1:7890)，这与你使用的魔法有关'
PROXIES_SOCKS='SOCKS5魔法地址(例如socks5://127.0.0.1:10808)，这与你使用的魔法有关'
#涩图CD
SETU_CD = xxx（单位：秒）

在bot.py中添加
nonebot.load_plugin("nonebot_plugin_setu")
```

### 正式使用

#### 下载涩图

本涩图插件采用的是下载和发图活动分离的方式，因此你必须先下载好涩图才能够发送涩图，命令也十分简单，直接向机器人发送命令

**下载涩图**即可，系统会自动下载好涩图存放在loliconImage里面（data的同级目录），一次默认下载量是80张，可以在init.py中进行更改

#### 发送涩图

向机器人发送命令**setu、涩图、色图、无内鬼**之一即可发送色图



# 更新

### 2021/1/26 [v1.0.0a1]

- 支持nonebot[v2.0.0-beta1]，beta1之前的请使用0.0.6版本
