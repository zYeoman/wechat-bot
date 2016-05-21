# -*- encoding=utf-8 -*-

import wechat_bot

wechat = wechat_bot.wechat_bot(local=True)
config = wechat.config


for plugin in config['plugins']:
    plugin['module'].test()

test = ['test', 'reloadconfig', 'updateupdate!', u'测试.']

for t in test:
    msg = {'Text': t, 'FromUserName': '@dajflsdkfjs', 'Type': 'Text'}
    print(u'Text: {}'.format(t))
    wechat.reply(msg)
