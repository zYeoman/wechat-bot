# wechat-bot
A simple wechat-bot based on  [ItChat](https://github.com/littlecodersh/ItChat)

## Plugin

### 种类
* Listener: 接受所有信息并回应
    * 用例：保存接收到的文件、图片
* Responser: 接受群里提到自己的信息或私聊信息并回应
    * 用例：聊天机器人，翻译机器人
* Scheduler: 接受私聊信息，按时自动发送信息
    * 用例：天气预报，每日新闻

### 准则
* 智能：不做文字交互插件，文字聊天机器人是伪需求
* 速度
* 低调：不影响日常交流，不会干扰日常微信使用

### 协议
* 目前仅仅发送纯文本。
