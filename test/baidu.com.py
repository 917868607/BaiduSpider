import requests
import re

url = 'https://m.baidu.com/s?from=844b&pn=50&usm=5&word=%E8%87%AA%E7%94%B1%E5%85%89jeep'
header = {
    'Host':'m.baidu.com',
    'Connection':'keep-alive',
    'Accept':'text/html',
    'Cache-Control':'private',
    'User-Agent':'Mozilla/5.0 (Linux; Android 4.4.2; OPPO R11 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
    'X-Requested-With':'XMLHttpRequest',
    'Async-Type':'xml',
    # "Referer":"https://m.baidu.com/from=844b/s?pn=10&usm=5&word=%E8%87%AA%E7%94%B1%E5%85%89jeep&sa=np&rsv_pq=11660182314235660230&rsv_t=8fd0AFMLCySzhKm5Yf3FTgh411ck%252Fsc9Sz9u2sLnx6dqplkyaaRzlTr3fA&rqid=11660182314235660230%20&adid=a1d14a09584f07c6"
    'Accept-Encoding':'gzip,deflate',
    'Accept-Language':'zh-CN,en-US;q=0.8'
}
response = requests.get(url=url,headers=header,verify=False)
print(response.text)
# with open('index.html', 'w',encoding='utf-8') as file:
#     file.write(response.text)

# str = """["吉普自由侠",["吉普自由侠怎么样","吉普自由侠胎压复位","吉普自由侠价格","吉普自由侠油耗","吉普自由侠油耗配置怎么样","吉普自由侠 180t劲能版","吉普 自由侠 180t","北京吉普自由侠"],["0;0;0;0","1;0;0;0","2;0;0;0","3;0;0;0","4;0;0;0","5;0;0;0","6;0;0;0","7;16;0;0"],["","","","","","","",""],["0"],"","suglabId_1"]
# """
# res = re.findall(re.compile(',\[(.*?)\]'),str)[0].replace('"','').split(',')
# for x in res:
#     print(x)
li = 0.522
l2 = 0.2554
print(float(li) - float(l2))