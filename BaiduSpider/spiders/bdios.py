# -*- coding: utf-8 -*-
import scrapy
import re
import json
from ..items import *
from ..untils.api import Emotion
from urllib import parse


class BdiosSpider(scrapy.Spider):
    name = 'bdios'
    allowed_domains = ['m.baidu.com']

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Host':'m.baidu.com',
            'Connection':'keep-alive',
            'Accept':'text/html',
            'Cache-Control':'private',
            'User-Agent':'Mozilla/5.0 (Linux; Android 4.4.2; OPPO R11 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
            'Async-Type':'xml',
            'Accept-Encoding':'gzip,deflate',
            'Accept-Language':'zh-CN,en-US;q=0.8'}

    }
    url = 'https://m.baidu.com/s?from=844b&pn={page}&usm=5&word={key}'
    url1 = 'https://m.baidu.com/su?json=1&callback=jsonp2&wd={}'
    def start_requests(self):
        keys = CheckMysql()
        for key in keys.get_key():
            yield scrapy.Request(url=self.url1.format(parse.quote(key)), callback=self.pull_parse, meta={'key': key})
            for page in range(0, 100, 10):
                yield scrapy.Request(url=self.url.format(page=page,key=parse.quote(key)),callback=self.parse,meta={'key':key,'page':int(page/10 +1)})

    def parse(self, response):
        print('正在爬取{},第{}页'.format(response.meta['key'],response.meta['page']))
        size1 = '0'
        contents = ''
        for index,div in enumerate(response.xpath('//div[@id="results"]/div[contains(@class,"c-result")]')):
            if div.xpath('div[@class="c-container"]/a'):
                title = Untiles.check_str(''.join(div.xpath('div[@class="c-container"]/a//text()').extract()))
                comefrom = get_comefrom(title,code='百度移动搜搜')
                link = div.xpath('div[@class="c-container"]/a/@href').extract_first('')
                if div.xpath('div[@class="c-container"]/div[contains(@class,"c-abstract")]'):
                    contents = Untiles.check_str(''.join(div.xpath('div[@class="c-container"]/div[contains(@class,"c-abstract")]//text()').extract()))
                elif div.xpath('div[@class="c-container"]/a[contains(@class,"wa-bk-polysemy-title")]'):
                    title = Untiles.check_str(''.join(div.xpath('div[@class="c-container"]/a[contains(@class,"wa-bk-polysemy-title")]//text()').extract()))
                    link = div.xpath('div[@class="c-container"]/a[contains(@class,"wa-bk-polysemy-title")]/@href').extract_first('')
                    comefrom = get_comefrom(title,code='百度移动搜搜')
                    contents = Untiles.check_str(''.join(div.xpath('div[@class="c-container"]/a[2]//text()').extract()))
                elif div.xpath('div[@class="c-container"]/div[contains(@class,"c-gap-top-small")]'):
                    div = div.xpath('div[@class="c-container"]/div[contains(@class,"c-gap-top-small")]')
                    if div.xpath('div[@class="wa-we-tiebanewxml-list"]'):
                        """贴吧"""
                        contents = '贴吧'
                        for a in div.xpath('div[@class="wa-we-tiebanewxml-list"]/div/a'):
                            link = a.attrib['href']
                            if 'http' not in link:
                                link = 'https://m.baidu.com' + link
                            title = ''.join(a.xpath('div/div[@class="wa-we-tiebanewxml-con-left"]/p//text()').extract())
                            check = CheckMysql()
                            link = Untiles.get_url(link)
                            res = check.select(link)
                            # check.closeMysql()
                            if res:
                                continue
                            res = Emotion.post(text=title,title='百度移动')
                            item = BaiduspiderItem(
                                title=title,
                                elasticsearch='百度移动',
                                key=response.meta['key'],
                                comefrom=comefrom,
                                link=link,
                                index=index + 1,
                                content=contents,
                                type=res,
                                page=response.meta['page'],
                                size1=size1,
                            )
                            yield item
                        continue
                    elif div.xpath('div[@class="c-span8"]'):
                        contents = Untiles.check_str(''.join(div.xpath('div[@class="c-span8"]//text()').extract()))
            elif div.xpath('div[@class="c-container"]/div[@class="c-blocka"]'):
                """相关汽车"""
                for div in div.xpath('div[@class="c-container"]/b-scroll/div/div/div/div/div'):
                    title = div.xpath('a//text()').extract()
                    title = ''.join(title)
                    comefrom = get_comefrom(title,code='百度移动搜搜')
                    link = div.xpath('a/@href').extract_first('')
                    contents = ''
                    check = CheckMysql()
                    link = Untiles.get_url(link)
                    res = check.select(link)
                    # check.closeMysql()
                    if res:
                        continue
                    res = Emotion.post(text=title,title='百度移动')
                    if '百科' in title:
                        res = 1
                        size1 = '1'
                    _item = BaiduspiderItem(
                        title=title,
                        elasticsearch='百度移动',
                        key=response.meta['key'],
                        comefrom=comefrom,
                        link=link,
                        index=index + 1,
                        content=contents,
                        type=res,
                        page=response.meta['page'],
                        size1=size1,
                    )
                    yield _item
                continue
            elif div.xpath('div[@class="c-container"]/div[@class="wa-recommend-list"]'):
                """其他人还搜索"""
                for a in response.xpath('//div[@class="c-span6"]/a[@class="c-blocka"]'):
                    title = a.xpath('div/text()').extract_first('')
                    res = Emotion.post(title)
                    if res == 0:
                        negative_prob = 0.5
                        positive_prob = 0.5
                    else:
                        (positive_prob, negative_prob) = res
                    item = BaiduItem(title=title, elasticsearch='百度移动', key=response.meta['key'], comefrom='相关搜索',
                                    type=negative_prob,link=positive_prob)
                    yield item
                continue
            elif div.xpath('div[@class="c-result-content"]'):
                for div in div.xpath('div[@class="c-result-content"]'):
                    link = div.xpath('article/header/div/a/@href').extract_first('')
                    title = ''.join(div.xpath('article/header/div/a//text()').extract())
                    contents = Untiles.check_str(''.join(div.xpath('article/section//text()').extract()))
                    if div.xpath('article/section/div/header'):
                        title = ''.join(div.xpath('div[@class="c-result-content"]/article/section/div/header/a//text()').extract())
                        for x in div.xpath('div[@class="c-result-content"]/article/section/div/section/div'):
                            contents = Untiles.check_str(''.join(x.xpath('div[@data-a-2f0a8efa=""]/a[@class="c-blocka"]//text()').extract()))
                            link = x.xpath('div[@data-a-2f0a8efa=""]/a[@class="c-blocka"]/@href').extract_first('')
                            comefrom = x.xpath('div[contains(@class,"c-color-gray")]/div/a/text()').extract_first('')
                            if 'http' not in link:
                                link = 'http://m.baidu.com' + link
                            check = CheckMysql()
                            link = Untiles.get_url(link)
                            res = check.select(link)
                            # check.closeMysql()
                            if res:
                                continue
                            res = Emotion.post(text=title,title='百度移动')
                            if '百科' in title:
                                res = 1
                                size1 = '1'
                            _items = BaiduspiderItem(
                                title=title,
                                elasticsearch='百度移动',
                                key=response.meta['key'],
                                comefrom=comefrom,
                                link=link,
                                index=index + 1,
                                content=contents,
                                type=res,
                                page=response.meta['page'],
                                size1=size1,
                            )
                            yield _items
                        continue
                    if not link:
                        print(response.url)
                    if 'http' not in link:
                        link = 'http://m.baidu.com' + link
                    check = CheckMysql()
                    link = Untiles.get_url(link)
                    comefrom = get_comefrom(title,code='百度移动搜搜')
                    res = check.select(link)
                    # check.closeMysql()
                    if res:
                        continue
                    res = Emotion.post(text=title,title='百度移动')
                    if '百科' in title:
                        res = 1
                        size1 = '1'
                    _item_ = BaiduspiderItem(
                        title=title,
                        elasticsearch='百度移动',
                        key=response.meta['key'],
                        comefrom=comefrom,
                        link=link,
                        index=index + 1,
                        content=contents,
                        type=res,
                        page=response.meta['page'],
                        size1=size1,
                    )
                    yield _item_
                continue
            elif div.xpath('div[@class="c-container"]/div[contains(@class,"c-gap-top-small")]'):
                """百度百科"""
                title = ''.join(div.xpath('div[@class="c-container"]/div[contains(@class,"c-gap-top-small")]/div/a[1]//text()').extract())
                link = div.xpath('div[@class="c-container"]/div[contains(@class,"c-gap-top-small")]/div/a[1]/@href').extract_first('')
                comefrom = get_comefrom(title,code='百度移动搜搜')
                contents = ''
            else:
                print('没有标签分析',response.url)
                continue
            if 'http' not in link:
                link = 'https://m.baidu.com' + link
            check = CheckMysql()
            link = Untiles.get_url(link)
            res = check.select(link)
            # check.closeMysql()
            if res:
                continue
            res = Emotion.post(text=title,title='百度移动')
            if '百科' in title:
                res = 1
                size1 = '1'
            item = BaiduspiderItem(
                title=title,
                elasticsearch='百度移动',
                key=response.meta['key'],
                comefrom=comefrom,
                link=link,
                index=index + 1,
                content=contents,
                type=res,
                page=response.meta['page'],
                size1=size1,
            )
            yield item

        #相关搜索
        for a in response.xpath('//div[@id="reword"]/div[@class="rw-list"]/a'):
            title = a.xpath('/text()').extract_first('')
            res = Emotion.post(title)
            if not title:
                continue
            if res == 0:
                negative_prob = 0.5
                positive_prob = 0.5
            else:
                (positive_prob,negative_prob) = res
            item = BaiduItem(title=title, elasticsearch='百度移动', key=response.meta['key'], comefrom='相关搜索',
                            type=negative_prob,link=positive_prob)
            yield item

    def pull_parse(self,response):
        resp = re.search(re.compile('jsonp2.*?\((.*?)\)'),response.text).group(1)
        resp = json.loads(resp)
        for x in resp['s']:
            if not x:
                continue
            res = Emotion.post(x)
            if res == 0:
                negative_prob = 0.5
                positive_prob = 0.5
            else:
                (positive_prob, negative_prob) = res
            items = PullKeyItem(
                elasticsearch='百度移动',
                key=response.meta['key'],
                title=x,
                type=negative_prob,
                index=positive_prob
            )
            yield items