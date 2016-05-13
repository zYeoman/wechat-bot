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
