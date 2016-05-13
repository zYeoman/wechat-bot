#!/usr/bin/env python
# -*- coding=utf-8 -*-

# {
#     "name":"translate",
#     "description":"Translate all single english words.",
#     "regex":"\b^[a-zA-Z]+\b$",
#     "type": "response",
#     "author": "zyeoman",
#     "date": "2016-5-6"
# },

import requests


def get_iciba(msg):
    url = "http://dict-co.iciba.com/api/dictionary.php"
    query = {"key": "E0F0D336AF47D3797C68372A869BDBC5",
             "w": msg,
             "type": "json"}
    result = requests.get(url, params=query).json()
    return result


def get_response(msg, more=False):
    meanings = get_iciba(msg.lower().strip())
    content = meanings["symbols"][0]
    result = u"UK: /{}/; USA: /{}/\n".format(content.get("ph_en", ""),
                                             content.get("ph_am", ""))
    for meaning in content.get("parts", []):
        result += u"\n{}\n{}\n".format(meaning.get("part", ""),
                                       u" ".join(meaning.get("means")))
    return result


def test():
    msg = ['test', 'over-load', 'askldjf']
    for m in msg:
        print('test plugin translate:msg={}'.format(m))
        if get_response(m):
            print("OK!")

if __name__ == '__main__':
    import sys
    while True:
        msg = raw_input('>>>').decode(sys.stdin.encoding).encode('utf-8')
        if msg == 'exit()':
            break
        print(get_response(msg))
