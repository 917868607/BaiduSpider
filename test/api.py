#-*-coding:utf-8-*-
KEY = 'i76wLHqy.26841.KpfgymhXfT6S'

# from __future__ import print_function, unicode_literals
# from __future__ import print_function,unicode_literals
import json
import requests


# SENTIMENT_URL = 'http://api.bosonnlp.com/sentiment/analysis'
# # 注意：在测试时请更换为您的API Token
# headers = {'X-Token': KEY}
#
# s = ['他是个傻逼', '美好的世界']
# s = '他妈的就是会吃'
# data = json.dumps(s)
# resp = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))
#
# print(resp.text)
#
import urllib.request
import ssl
AK = 'hfTqO6Hy0j6H24M6PiHQfUbQ'
SK = 'KXB6IFZbuXM9U0pKqy3zdzbgjgsOhhIY'
# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials' \
       '&client_id={}' \
       '&client_secret={}'.format(AK,SK)
request = urllib.request.Request(host)
request.add_header('Content-Type', 'application/json; charset=UTF-8')
response = urllib.request.urlopen(request)
content = response.read()
if (content):
    print(content)