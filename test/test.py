#-*-coding:utf-8-*-

from urllib import parse
import requests
from fake_useragent import UserAgent
import re
import redis
import datetime
import time
import os
from lxml import etree
from BaiduSpider.untils.until import *
from multiprocessing import Pool

def eat(name):
    print('子进程号{}'.format(os.getpid()))
    print(name)
def now_to_timestamp(digits = 10):
    time_stamp = time.time()
    digits = 10 ** (digits -10)
    time_stamp = int(round(time_stamp*digits))
    return time_stamp

if __name__ == '__main__':

    # times = now_to_timestamp(13)
    # print(times)
    # print('主进程id{}'.format(os.getpid()))
    # p = Pool()
    # for i in range(5):
    #     p.apply_async(eat,args=('hah',))
    #     time.sleep(.5)
    # p.close()
    # p.join()
    # print('结束id')


    # str = 'window._common_counter_code_="channel=10932";window._common_counter_uuid_="__uuid=521526&";window._common_counter_from_="";!(function(){vardomain="5.pconline.com.cn/newcount",reffer=document.referrer,tagName="img";if(!window.PCGPARAM||(window.PCGPARAM&&PCGPARAM.browserType!="main")){if(!!document.cookie.match(/(^|;)referrerUrl=[^;]+/)){reffer=document.cookie.match(/(^|;)referrerUrl=([^;]+)/)[2];document.cookie="referrerUrl=;expires="+newDate(newDate().getTime()-10000).toGMTString()+";path=/;domain="+domain}tagName="script"}varelem=(document.body.insertBefore(document.createElement(tagName),document.body.firstChild));elem.style.display="none";elem.src=location.protocol+"//count"+domain+"/count.php?"+(window._common_counter_uuid_?window._common_counter_uuid_:"")+_common_counter_code_+"&screen="+screen.width+"*"+screen.height+"&refer="+encodeURIComponent(reffer)+"&anticache="+newDate().getTime()+"&url="+encodeURIComponent(location.href)+"&from="+(window._common_counter_from_?window._common_counter_from_:"")+"&iframeCode="+(self===top?0:(top===parent?1:2))})();太平洋电脑网if(!window.preloadShow4)document.write('');if(!window._addIvyID)document.write('');functionivyLoadReal(closespan){varad=null,adpos=document.getElementsByTagName("u");for(vari=0;i<adpos.length;i++)if(adpos[i].className=="adpos"){ad=adpos[i];break;}if(ad==null)return;if(!closespan){document.write("");showIvyViaJs(ad.id);return;}document.write("");varreal=document.getElementById("adpos_"+ad.id);for(vari=0;i<real.childNodes.length;i++){varnode=real.childNodes[i];if(node.tagName=="SCRIPT"&&/closespan/.test(node.className))continue;ad.parentNode.insertBefore(node,ad);i--}ad.parentNode.removeChild(ad);real.parentNode.removeChild(real);}showIvyViaJs("pc.cpdq.zdym.b20796.s20820.stl1.")showIvyViaJs("pc.cpdq.zdym.b20796.s20820.stl1xf.")showIvyViaJs("pc.cpdq.zdym.b20796.s20820.stl1xf2.")showIvyViaJs("pc.cpdq.zdym.b20796.s20820.p45451.zu.tl.")showIvyViaJs("pc.cpdq.zdym.b20796.s20820.zu.tl.")showIvyViaJs("pc.cpdq.zdym.b20796.s20820.stl1xf3.")showIvyViaJs("pc.cpdq.zdym.b20796.s20820.stl1xf4.")分类：手机通讯安卓手机苹果手机4G手机八核手机双卡手机>>笔记本超极本触控本便携本平板笔记本实用本游戏本>>平板电脑苹果平板安卓平板微软平板双系统通讯平板整机硬件CPU主板显卡内存硬盘显示器键鼠>>数码外设耳机蓝牙耳机移动电源U盘移动硬盘电子书>>数字家电液晶电视电视盒子空调冰箱空气净化器>>网络设备无线路由无线上网卡随身wifi路由器交换机>>办公·企业投影机打印机一体机扫描仪服务器>>更多分类当前位置：首页>产品报价>鼠标大全>达尔优鼠标大全>牧马人鼠标牧马人鼠标别名：达尔优牧马人游戏鼠标;全称：达尔优牧马人游戏鼠标(TM133)牧马人鼠标全称是达尔优牧马人游戏鼠标，有线链接，工作方式是光电，最高分辨率是4000dpi，鼠标接口是USB。[展开]概览参数报价点评图片评测导购竞品对比showIvyViaJs("pc.cpdq.zdym.b20796.s20820.p45451.xfwz.")showIvyViaJs("pc.cpdq.zdym.b20796.s20820.xfwz.")showIvyViaJs("pc.cpdq.zdym.xhxfwz.")'
    # res = re.findall(re.compile('[\u4e00-\u9fa5]'),str)
    # print(''.join(res))
# useragent = UserAgent()
#
# str = '%E8%87%AA%E7%94%B1%E5%85%89'
#
# print(parse.unquote(str))
#
#
# print(parse.unquote('%C2%A0'))
# #
# # url = 'https://baike.baidu.com/item/JEEP%E8%87%AA%E7%94%B1%E5%85%89/3040035?fromtitle=%E8%87%AA%E7%94%B1%E5%85%89&fromid=2511991&fr=aladdin'
# url = 'https://www.baidu.com'
# # response = requests.get(url,allow_redirects=False)
# # print(response.text)
# # response = etree.HTML(response.text)
# #相关搜索
# # link = response.xpath('//div[@id="rs"]/table/tr[1]/th[1]/a/@href')
# # print(link)
#
# #
# # if response.status_code == 302:
# #     print(response.text)
# # else:
# #     print(response.text)
# #     url = re.search(re.compile("URL=(.*?)>"),response.text).group(1).replace("'",'').replace('"','')
# #     print(url)
# #     with open('1.html','r',encoding='utf-8') as f:
# #         f.write(response.text)
# import random
# print('***********')
# # time = datetime.datetime.now().strftime("%Y%m%d")
# # time = 'meg' + time
# # print(time)
#
# r = redis.Redis(host='127.0.0.1',port=6379,db=0)
# proxies = r.lrange('proxies',0,r.llen('proxies'))
# # r.ltrim('proxies',1, -1)
# print(proxies)
# res = r.lindex(('219.141.153.35:80').encode(),r.llen('proxies'))
# proxies = r.lrange('key',0,r.llen('proxies'))
# print(proxies)
# # print(type(proxies))
# # res = random.choice(proxies)
# # res = bytes.decode(res)
# # res = str(res).replace("b'",'').replace("'",'')
# import hashlib
# url = 'https://www.baidu.com'
# h1 = hashlib.md5()
# h1.update(url.encode())
# print('MD5加密前为 ：' + url)
# print('MD5加密后为 ：' + h1.hexdigest())
# r.lpush('url',{'key':h1.hexdigest(),'type':0,'time':datetime.datetime.now().strftime('%Y%m%d')})
#
# # r.setex('url',{'key':h1.hexdigest(),'type':0,'time':datetime.datetime.now().strftime('%Y%m%d')},50)
# # res = r.lrange('url',0,r.llen('url'))
# # time.sleep(11)
# time = datetime.timedelta(days=1)
# print(time)
# r.expire('url',time)
# res = r.lrange('url',0,r.llen('url'))
# _res = [eval(bytes.decode(x)) for x in res]
# # # _res = []
# # # for x in res:
# # #     x = eval(bytes.decode(x))
# # #     _res.append(x)
# print(_res)
# print(type(_res))
#
#
# # key时间 [{'title':标题,'index':第几名,'page':第几页,'type':类型}]
    r = redis.Redis(host='127.0.0.1',port=6379,db=4)
    res = r.lrange('pull20180810百度移动',0,r.llen('pull20180810百度移动'))
    res = sendstr(res)
    value = []
    for x in res:
        for val in x['大切诺基'].values():
            print(val)
            value.append(val)
    print(value)
#
print(list([val for x in res for val in x['大切诺基'].values()]))
# print('insert into '
#       'haha'
#       'erhah'
#       'sanha')
# respose = requests.get('https://baidu.com')
# print(respose)
#
# import pymysql
#
# connect = pymysql.Connection(host='127.0.0.1', user='root', password="123456",
#                  database='seo')
# cursor = connect.cursor()
# sql = 'select url from urls'
# res = cursor.execute(sql)
# res = cursor.fetchall()
# for x in res:
#     for z in x:
#         print(z)
# print(list([z for x in res for z in x]))