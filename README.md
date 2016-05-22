# wechat-bot
A simple wechat-bot based on  [ItChat](https://github.com/littlecodersh/ItChat)

## Basic
* `reload config`: reload `config.json` file
* `update update!`: run command `git pull`

## Config

```js
{
    "name":"r2",// name of the bot
    "plugins":[
        {
            "name":"translate",//name of plugin `./plugins/translate.py`
            "description":"Translate all single english words.",
            "regex":"^[a-zA-Z-]+$",//which msg to response to
            "type": "listener"//response all msg which matchs regex
        },
        {
            "name":"sayHello",
            "description":"say Hello!",
            "regex":"^(Hello|Hi)$",
            "type":"response",//response "r2 Hello" in group and "Hello" not in group
            "response":"Hello!"//response
        }
    ]
}
```

## Plugins
* Add `.py` script to `./plugins`. The script should have `get_response` and `test` functiongs.
* Edit `config.json`.

### Basic Plugins
* sayHello: response to Hello/Hi message, with 'Hello'.
* translate: translate all single English words.

### 已知的bug与期望的feature
* `Ctrl+C`无法关闭程序, 多线程问题
* 接收获得不了nickName
* 群消息和单个消息output两边
* Emoji 输出
* 新闻等消息排版输出: 参照weixinbot
* 另外的网页版登录或手机下线的Error发送: 参照weixinbot

### 未来
* 对指定nickName发送消息
* WebUI, 远程控制
