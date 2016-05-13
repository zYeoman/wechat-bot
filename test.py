# -*- encoding=utf-8 -*-

import wechat_bot

wechat = wechat_bot.wechat_bot()
config = wechat.config


for plugin in config['plugins']:
    plugin['module'].test()

test = ['test', 'reload config', 'update update!']

for t in test:
    msg = {'Text': t}
    print('Text: {}'.format(t))
    wechat.reply(msg, local=True)
