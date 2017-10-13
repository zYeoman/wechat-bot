# -*- encoding:utf-8 -*-

import os
import threading
import logging
import pickle

import requests
import owncloud
import itchat
from apscheduler.schedulers.blocking import BlockingScheduler
from itchat.content import PICTURE, ATTACHMENT, VIDEO, TEXT

logging.basicConfig(level=logging.ERROR)

MSGS = []
OC = owncloud.Client('https://cloud.mickir.me')
OC.login('zyeoman@163.com', 'zyw26266957')
try:
    OC.mkdir('wechat')
except owncloud.HTTPResponseError:
    pass


@itchat.msg_register([PICTURE, ATTACHMENT, VIDEO])
@itchat.msg_register([PICTURE, ATTACHMENT, VIDEO], isGroupChat=True)
def download_files(msg):
    MSGS.append(msg)
    msg.download(msg.fileName)
    OC.put_file('wechat/' + msg.fileName, msg.fileName)
    os.remove(msg.fileName)
    print('%s received' % msg['Type'])


@itchat.msg_register(TEXT)
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    MSGS.append(msg)
    with open('log.log', 'wb') as file:
        pickle.dump(MSGS, file)
    print('> ' + msg.text)


def report_weather():
    """Send Weather """
    weather = requests.get(
        "http://www.sojson.com/open/api/weather/json.shtml?city=北京").json()
    if weather.get('status', 0) == 200:
        try:
            weather_strs = weather['data']['forecast'][0]
            weather_str = '日期：{date}\n天气：{type}\n'\
                '气温：{low}-{high}\n'\
                '风向：{fengxiang} {fengli} \n'.format(**weather_strs)
        except KeyError:
            return
        itchat.send_msg(weather_str, 'filehelper')


def schedule():
    """定期执行任务"""
    # itchat.send_msg(msg='test', toUserName='filehelper')
    schedular = BlockingScheduler()
    schedular.add_job(report_weather, 'cron', hour=7, minute=30)
    schedular.start()


if __name__ == "__main__":
    itchat.auto_login(enableCmdQR=2)
    threading.Thread(target=itchat.run).start()
    threading.Thread(target=schedule).start()
