# -*- encoding:utf-8 -*-

import logging
import pickle

import itchat
from itchat.content import PICTURE, ATTACHMENT, VIDEO, TEXT

logging.basicConfig(level=logging.ERROR)

MSGS = []


@itchat.msg_register([PICTURE, ATTACHMENT, VIDEO])
@itchat.msg_register([PICTURE, ATTACHMENT, VIDEO], isGroupChat=True)
def download_files(msg):
    MSGS.append(msg)
    msg.download(msg.fileName)
    return '%s received' % msg['Type']


@itchat.msg_register(TEXT)
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    MSGS.append(msg)
    with open('log.log', 'wb') as file:
        pickle.dump(MSGS, file)
    print('> ' + msg.text)


if __name__ == "__main__":
    itchat.auto_login(enableCmdQR=2)
    itchat.run()
