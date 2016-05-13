# -*- encoding=utf-8 -*-

import wechat_bot

wechat = wechat_bot.wechat_bot()
config = wechat.config


for plugin in config['plugins']:
    plugin['module'].test()

test = [u'呵呵', 'reload config']

for t in test:
    msg = {'Text': t}
    wechat.text_reply(msg, local=True)
