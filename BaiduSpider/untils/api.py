#-*-coding:utf-8-*-
"""情感分析"""
import requests
import json
import time
import re
import json
from BaiduSpider.settings import AK,SK
import urllib.request
from BaiduSpider.untils.until import RedisCheck
# from __future__ import print_function,unicode_literals




class GetToken(object):

    def __init__(self):
        self.url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={AK}&client_secret={SK}'.format(AK=AK,SK=SK)

        self.header = {'Content-Type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'}

    def getAccess(self):
        request = urllib.request.Request(self.url)
        request.add_header('Content-Type', 'application/json; charset=UTF-8')
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')
        content = json.loads(content)
        if content:
            token = content['access_token']
            time = content['expires_in']
            red = RedisCheck().redis_connect(db=3)
            red.set('token',token,ex=(time-100))

    def returnToken(self):
        red = RedisCheck().redis_connect(db=3)
        res = red.get('token')
        if res:
            res = res.decode('utf-8')
        else:
            self.getAccess()
            res = self.returnToken()
        return res




TOKEN = GetToken().returnToken()

class Emotion(object):
    def __init__(self):
        self.url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token={}'
        self.header = {'Content-Type':'application/json','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'}


    @classmethod
    def post(cls,text,title=None):
        """0 中性 1 正面 2 负面"""
        _res = 0
        body = {
            'text':text
        }
        if not ''.join(re.findall(re.compile('[\u4e00-\u9fa5]'), text)):
            return _res
        else:
            text = ''.join(re.findall(re.compile('[\u4e00-\u9fa5]'), text))
        try:
            resp = requests.post(cls().url.format(TOKEN),json=body,headers=cls().header,verify=False)
        except Exception as e:
            resp = requests.post(cls().url.format(TOKEN), json=body, headers=cls().header, verify=False)
        res = json.loads(resp.text)
        if res.get('items',None):
            positive_prob,negative_prob =res['items'][0]['positive_prob'],res['items'][0]['negative_prob']
            if title:
                if float(-0.3) < float(positive_prob) - float(negative_prob) < float(0.3):
                    print('中性')
                    return _res
                if float(positive_prob) - float(negative_prob) > float(0.3):
                    print('正面')
                    _res = 1
                    return _res
                else:
                    _res = -1
                    print('负面')
                    return _res
            else:
                return positive_prob,negative_prob
        else:
            time.sleep(0.5)
            print('情感测试失败,重新来过')
            if title:
                _res = cls().post(text)
                return _res
            else:
                positive_prob, negative_prob = cls().post(text)
                return positive_prob,negative_prob




if __name__ == '__main__':
    str = "很垃圾"
    # str = str.replace('，','')
    # print(str)
    # print(type(str))
    # str = Untiles().check_china(str)[:1000]
    # print(len(list(str)))
    # res = Emotion.post(str)
    # res = Emotion.post(str,title='hah')
    # print('jaj')
    print(GetToken().returnToken())