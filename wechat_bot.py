# -*- encoding:utf-8 -*-

import itchat
import json
import re
import os
import time
import threading
from pprint import pprint

# ToUserName = "filehelper" 文件传输助手


class response:

    def __init__(self, response):
        self.response = response

    def get_response(self, msg):
        return self.response

    def test(self):
        print(self.response + '  OK!')


class wechat_bot(itchat.client):
    """bot for wechat"""

    def __init__(self):
        itchat.client.__init__(self)
        self.config = self.load_config()
        self.own = None
        self.config_mutex = threading.Lock()

    def get_QR(self, uuid=None):
        BASE_URL = 'https://login.weixin.qq.com'
        if uuid is None:
            uuid = self.uuid
        url = '%s/qrcode/%s' % (BASE_URL, uuid)
        r = self.s.get(url, stream=True)
        QR_DIR = 'QR.jpg'
        with open(QR_DIR, 'wb') as f:
            f.write(r.content)
        try:
            os.startfile(QR_DIR)
        except:
            pass
        print('\n' + url)
        return True

    def load_config(self):
        with open('config.json') as f:
            content = json.load(f)
        for plugin in content['plugins']:
            if plugin.get('response'):
                plugin['module'] = response(plugin['response'])
            else:
                plugin['module'] = __import__('plugins.' + plugin['name'],
                                              fromlist=plugin['name'])
            plugin['regex'] = re.compile(plugin['regex'])
        pprint(content)
        return content

    def text_reply(self, msg, m='response', local=False):
        self.config_mutex.acquire()
        local_config = self.config.copy()
        self.config_mutex.release()
        for plugin in local_config['plugins']:
            if plugin.get('type', '') == m:
                regex = plugin['regex']
                r = regex.match(msg['Text'].strip())
                if r:
                    response = plugin['module'].get_response(r.string)
                    if local:
                        print(response)
                    else:
                        print({'Text': response,
                               'ToUserName': msg['FromUserName']})
                        self.send({'Text': response,
                                   'ToUserName': msg['FromUserName']})
        return True

    def send(self, send_msg):
        text = send_msg['Text']
        toUserName = send_msg['ToUserName']
        if text is None:
            return False
        if text[:5] == '@fil@':
            return self.send_file(text[5:], toUserName)
        elif text[:5] == '@img@':
            return self.send_image(text[5:], toUserName)
        elif text[:5] == '@msg@':
            return self.send_msg(text[5:], toUserName)
        else:
            return self.send_msg(text, toUserName)

    def reply(self, msg, local=False):
        if msg.get('Type') != 'Text' and not local:
            return False
        if not self.own and not local:
            self.own = msg['Text']
            return True
        if msg.get('Text') == 'reload config':
            self.config = self.load_config()
            return True
        if msg.get('Text') == 'update update!':
            threading.Thread(target=self.update, args=()).start()
            return True
        if msg.get('ToUserName') == 'filehelper' or \
                msg.get('FromUserName') == self.own:
            msg['FromUserName'] = 'filehelper'
        if '@@' in msg.get('FromUserName'):
            print('Group!  {}  {}'.format(msg['Text'], msg['FromUserName']))
            if msg.get('Text').startswith(self.config['name']):
                msg['Text'] = msg['Text'][len(self.config['name']):]
                self.text_reply(msg)
        else:
            self.text_reply(msg, local=local)
        self.text_reply(msg, 'listener', local=local)
        return True

    def update(self):
        os.system('git pull')
        os.system('git rebase origin/master')
        self.config_mutex.acquire()
        self.config = self.load_config()
        self.config_mutex.release()

    def run(self):
        print('Start auto replying')
        while 1:
            try:
                msg = self.storageClass.msgList.pop()
                self.reply(msg)
            except:
                pass
            time.sleep(0.3)

if __name__ == '__main__':
    bot = wechat_bot()
    bot.auto_login()
    bot.run()
