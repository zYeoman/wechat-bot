# -*- encoding:utf-8 -*-

import itchat
import json
import re
import os
import time
import threading
from pprint import pprint

import logging

_DebugLevel = logging.ERROR
logging.basicConfig(level=logging.ERROR)

# ToUserName = "filehelper" 文件传输助手


class response:

    def __init__(self, response):
        self.response = response

    def get_response(self, msg):
        return self.response

    def test(self):
        print(self.response + '  OK!')


class wechat_bot(itchat.Core):
    """bot for wechat"""

    def __init__(self, local=False):
        itchat.Core.__init__(self)
        self._config = self.load_config()
        self.user = None
        self.config_mutex = threading.Lock()
        self.local = local

    @property
    def config(self):
        self.config_mutex.acquire()
        local_config = self._config.copy()
        self.config_mutex.release()
        return local_config

    def load_config(self):
        with open('config.json') as f:
            content = json.load(f)
        for plugin in content['plugins']:
            if plugin.get('response'):
                plugin['module'] = response(plugin['response'])
            else:
                plugin['module'] = __import__('plugins.' + plugin['name'],
                                              fromlist=plugin['name'])
            if plugin.get('regex'):
                plugin['regex'] = re.compile(plugin['regex'])
        pprint(content)
        return content

    def reload_config(self):
        self.config_mutex.acquire()
        self._config = self.load_config()
        self.config_mutex.release()

    def update(self):
        os.system('git pull --rebase')
        self.reload_config()

    def text_reply(self, msg, m='response'):
        local_config = self.config
        for plugin in local_config['plugins']:
            if plugin.get('type', '') == m:
                regex = plugin['regex']
                r = regex.match(msg['Text'].strip())
                if r:
                    local_msg = msg.copy()
                    local_msg['Text'] = r.string
                    response = plugin['module'].get_response(local_msg,
                                                             self.send
                                                             )
                    self.send({'Text': response,
                               'ToUserName': msg['FromUserName']})
        return True

    def file_reply(self, msg):
        local_config = self.config
        if not os.path.isdir('files'):
            os.mkdir('files')
        filepath = u'{}{}{}'.format('files', os.sep, msg['FileName'])
        msg['Text'](filepath)
        msg['Text'] = filepath
        for plugin in local_config['plugins']:
            if plugin.get('type') == 'file':
                response = plugin['module'].get_response(msg, self.send)
                if response:
                    self.send({'Text': response,
                               'ToUserName': msg['FromUserName']})

    def send(self, send_msg):
        text = send_msg['Text']
        toUserName = send_msg['ToUserName']
        nickName = self.search_friends(userName=toUserName)
        if nickName is not None:
            nickName = nickName['NickName']
        print(u"Send to {1}: {0}".format(
            text, nickName if nickName else toUserName))
        if self.local:
            return True
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

    def reply(self, msg):
        if msg.get('Type') == 'Init':
            if not self.user:
                self.user = self.storageClass.userName
                return True
            else:
                return False
        if msg.get('ToUserName') == 'filehelper' or \
                msg.get('FromUserName') == self.user:
            msg['FromUserName'] = 'filehelper'
        nickName = self.search_friends(userName=msg['FromUserName'])
        if nickName is not None:
            nickName = nickName['NickName']
        if msg.get('Type') == 'Text':
            print(u'Receive from {1}:{0}'.format(
                msg.get('Text'),
                nickName if nickName else msg.get('FromUserName')))
            if msg.get('Text') == 'reload config':
                self.reload_config()
                return True
            if msg.get('Text') == 'update update!':
                threading.Thread(target=self.update, args=()).start()
                return True
            if '@@' in msg.get('FromUserName'):
                print(u'Group!  {1} : {0}'.format(
                    msg['Text'],
                    nickName if nickName else msg.get('FromUserName')))
                if msg.get('Text').startswith(self.config['name']):
                    msg['Text'] = msg['Text'][len(self.config['name']):]
                    self.text_reply(msg)
            else:
                self.text_reply(msg)
            self.text_reply(msg, 'listener')
        elif msg.get('Type') == 'Attachment':
            threading.Thread(target=self.file_reply, args=(msg,)).start()
        return True

    def run(self):
        print('Start auto replying')
        while 1:
            if self.storageClass.msgList:
                msg = self.storageClass.msgList.get()
                self.reply(msg)
            else:
                time.sleep(0.3)

    def cli_input(self):
        while 1:
            try:
                msg = input('input:')
            except EOFError:
                exit()
            send_msg = {'Text': msg, 'ToUserName': 'filehelper'}
            self.send(send_msg)

if __name__ == '__main__':
    bot = wechat_bot()
    bot.auto_login(enableCmdQR=2)
    threading.Thread(target=bot.run).start()
    threading.Thread(target=bot.cli_input).start()
