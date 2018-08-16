# -*- coding: utf-8 -*-
import re
import scrapy
import json
from urllib import parse

from ..items import *
from ..untils.api import Emotion
from BaiduSpider.untils.until import Untiles
import datetime
import time



class BdSpider(scrapy.Spider):
    name = 'bd'
    allowed_domains = ['baidu.com']
    basic_url = 'https://www.baidu.com'
    url = 'http://www.baidu.com/s?wd={}&pn=0'
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive'
        }
    }
    def start_requests(self):
        keys = CheckMysql()
        for x in keys.get_key():
            print('key', x)
            key = parse.quote(x)
            yield scrapy.Request(url=self.url.format(key),callback=self.parse,meta={'key':x})
    def parse(self, response):
        size1 = '0'
        content = []
        # sid = re.search(re.compile('bds.comm.sid = (.*?)\;'),response.text).group(1)
        """获取pull下拉 time13"""
        url = 'https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd={key}' \
              '&sugmode=2&json=1&p=3' \
              '&req=2&bs={bs}&csor=3' \
              '&cb=jQuery1102035704388508109774_1533440813598&' \
              '_={time}'.format(
                    key=parse.quote(response.meta['key']),

                    bs=parse.quote(response.meta['key']),
                    time=now_to_timestamp(13)
        )
        yield scrapy.Request(url=url,callback=self.pull_parse,meta=response.meta)
        divs = response.xpath('//div[@id="content_left"]/div[contains(@class,"c-container")]')
        next_link = response.xpath("//a[contains(text(),'下一页')]/@href").extract_first('')
        try:
            page = re.search(re.compile('&pn=(\d+)'), next_link).group(1)
        except Exception as e:
            print(response.url)
            # with open('test/baidu.html', 'w', encoding='utf-8') as f:
            #     f.write(response.text)
            print(e)
            yield scrapy.Request(url=response.url,callback=self.parse,meta=response.meta)
            return
        if int(page) / 10 >= 10:
            return
        page = int(page) / 10
        for index,div in enumerate(divs):
            index = index + 1
            title = div.xpath('h3/a//text()').extract()
            try:
                small_title = title[-1]
            except Exception as e:
                if not title:
                    continue
            small_title = get_comefrom(small_title,code='百度搜索')
            _title = ''.join(title)
            link = div.xpath('h3/a/@href').extract_first()
            if div.xpath('div[contains(@class,"c-gap-top-small")]').extract():
                content = div.xpath('div[contains(@class,"c-row")]/div[contains(@class,"c-span18")]//text()').extract()
            if div.xpath('div[@class="c-row"]'):
                """百度百科为正"""
                content = div.xpath('div[@class="c-row"]/div[contains(@class,"c-span-last")]/p[1]//text()').extract()
                content = Untiles.check_str(''.join(content))
                link = div.xpath('h3/a/@href').extract_first('')
            # 下一页
            """div class c-offset"""
            if div.xpath('div[contains(@class,"c-offset")]'):
                offsets = div.xpath('div[@class="c-offset"]')
                for off in offsets.xpath('div[contains(@class,"c-row")]'):
                    content = '最新相关信息'
                    """缺少比如自由光相关信息"""
                    title = off.xpath('a//text()').extract()
                    title = Untiles.check_str(''.join(title))
                    if not title:
                        title = Untiles.check_str(''.join(offsets.xpath('div[@class="c-gap-bottom-small"]/a//text()').extract()))
                        link = offsets.xpath('div[@class="c-gap-bottom-small"]/a/@href').extract_first('')
                        content = Untiles.check_str(off.xpath('div/text()').extract_first(''))
                        small_title = off.xpath('div/span[1]/text()').extract_first('')
                    else:
                        link = off.xpath('a/@href').extract_first('')
                        o_smalltitle1 = off.xpath('span[2]/text()').extract()
                        small_title = Untiles.check_str(''.join(o_smalltitle1))
                    if '前' in small_title:
                        small_title = small_title.split('前')[-1]
                    if 'http' not in link:
                        link = self.basic_url + link
                    link = Untiles.get_url(link)
                    _check = CheckMysql()
                    res = _check.select(link)
                    # _check.closeMysql()
                    if res:
                        continue
                    # if not title:
                    #     with open('test/baidu.html','w',encoding='utf-8') as f:
                    #         f.write(response.text)
                    resp = Emotion.post(title,title='百度PC')
                    _itemm = BaiduspiderItem(title=title, elasticsearch='百度PC',
                                            key=response.meta['key'], comefrom=small_title,
                                            link=link, index=index, content=content,
                                            type=resp, page=page, size1=size1)
                    yield _itemm
                continue
            if div.xpath('div[@class="c-abstract"]'):
                content = div.xpath('div[@class="c-abstract"]//text()').extract()
            if '贴吧' in _title:
                """百度贴吧"""
                res = div.xpath('table/tbody/tr/td[contains(@class,"op-tieba-general-firsttd")]')
                for a in res:
                    title = ''.join(a.xpath('a//text()').extract())
                    link1 = a.xpath('a/@href').extract_first('')
                    content = '贴吧'
                    small_title = '百度贴吧'
                    if 'http' not in link1:
                        link1 = self.basic_url + link1
                    link1 = Untiles.get_url(link1)
                    _check = CheckMysql()
                    res = _check.select(link1)
                    # _check.closeMysql()
                    if res:
                        continue
                    resp = Emotion.post(title,title='百度PC')
                    itemm = BaiduspiderItem(title=title, elasticsearch='百度PC',
                                           key=response.meta['key'], comefrom=small_title,
                                           link=link1, index=index, content=content,
                                           type=resp, page=page, size1=size1)
                    yield itemm
                continue
            title = Untiles.check_str(''.join(title))
            content = Untiles.check_str(''.join(content))
            small_title = Untiles.check_str(''.join(small_title))
            url = Untiles.get_url(link)
            _check = CheckMysql()
            try:
                res = _check.select(url)
            except Exception as e:
                print(url)
                print(link)
                url = Untiles.get_url(link)
                res = _check.select(url)
            # _check.closeMysql()
            if res:
                continue
            resp = Emotion.post(title,title='百度PC')
            if "百科" in title:
                resp = 1
                size1 = '1'
            item = BaiduspiderItem(title=title, elasticsearch='百度PC',
                                   key=response.meta['key'], comefrom=small_title,
                                   link=url, index=index, content=content,
                                   type=resp, page=page,size1=size1)
            yield item

        #相关搜索
        divs = response.xpath('//div[@id="rs"]/table').extract_first('')
        con_list = re.findall(re.compile('<a href="(.*?)">(.*?)</'),divs)
        for x in con_list:
            x_title = x[1]
            res = Emotion.post(x_title)
            if res == 0:
                negative_prob = 0.5
                positive_prob = 0.5
            else:
                (positive_prob, negative_prob) = res
            items = BaiduItem(
                elasticsearch="百度PC",
                key=response.meta['key'],
                comefrom="相关搜索",
                title=x_title,
                type=negative_prob,
                link=positive_prob
            )
            yield items

        if "http" not in next_link:
            print('正在爬取第{}页............'.format(page))
            next_link = self.basic_url + next_link
        yield scrapy.Request(url=next_link,callback=self.parse,headers={'Referer':response.url},meta=response.meta)

    def pull_parse(self,response):
        """下拉搜搜"""
        res = re.search(re.compile('jQ.*?\((.*?)\)'),response.text).group(1)
        resp = json.loads(res)
        for x in resp['s']:
            res = Emotion.post(x)
            if res == 0:
                negative_prob = 0.5
                positive_prob = 0.5
            else:
                (positive_prob, negative_prob) = res
            itemss = PullKeyItem(elasticsearch='百度PC',
                                 key=response.meta['key'],
                                 title=x,
                                 type=negative_prob,
                                 index=positive_prob)
            yield itemss



