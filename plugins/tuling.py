#!/usr/bin/env python
# -*- coding=utf-8 -*-

# {
#     "name":"tuling",
#     "description":"Tuling bot",
#     "type":"response",
#     "regex":"^.*\.$"
# }

import requests
import json


def get_tuling(msg, local='北京市', userid='abcd1234'):
    url = "http://www.tuling123.com/openapi/api"
    query = {"key": "1c38197ddf406d97ac4958a7a47f541b",
             "info": msg,
             "loc": local,
             "userid": userid}
    result = requests.post(url, data=json.dumps(query)).json()
    return result


def get_response(msg, send=None, more='abcd'):
    response = get_tuling(msg.lower().strip(), more[2:7])
    content = response["text"]
    return content


def test():
    msg = [u'天气', u'你好', 'askldjf']
    for m in msg:
        print(u'test plugin tuling:msg={}'.format(m))
        if get_response(m):
            print("OK!")

if __name__ == '__main__':
    import sys
    while True:
        msg = raw_input('>>>').decode(sys.stdin.encoding).encode('utf-8')
        if msg == 'exit()':
            break
        print(get_response(msg))
