# -*- coding: utf-8 -*-
import scrapy
import re
import json
from urllib import parse
from ..items import *
from ..untils.until import *
from ..untils.api import Emotion


class SogouiosSpider(scrapy.Spider):
    name = 'sogouios'
    allowed_domains = ['wap.sogou.com']


    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Host': 'wap.sogou.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; OPPO R11 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
            'Accept': 'text/html',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'X-Requested-With': 'com.android.browser'}
    }

    pull_url = 'https://wap.sogou.com/web/sugg.jsp?kw={}'
    start_url = 'https://m.sogou.com/web/searchList.jsp?keyword={key}&sugn=10'
    'https://m.sogou.com/web/searchList.jsp?keyword=%E8%87%AA%E7%94%B1%E5%85%89&sugn=10'
    bulit_url = 'https://m.sogou.com'
    def start_requests(self):
        keys = CheckMysql()
        for key in keys.get_key():
            yield scrapy.Request(url=self.pull_url.format(parse.quote(key)), callback=self.pull_parse,meta={'key': key})
            yield scrapy.Request(url=self.start_url.format(key=parse.quote(key)), callback=self.parse,meta={'key': key,'page':1})

    def parse(self, response):
        print('详情url', response.url)
        size1 = '0'
        comefrom = ''
        contents = ''
        for index,div in enumerate(response.xpath('//div[@class="vrResult"]')):
            index = index + 1
            if div.attrib.get('data-v',None):
                index = int(div.attrib['data-v'])
            if div.xpath('h3'):
                title = Untiles.check_str(''.join(div.xpath('h3/a//text()').extract()))
                link = div.xpath('h3/a/@href').extract_first('')
                if div.xpath('div/a[contains(@class,"img-flex")]'):
                    contents = Untiles.check_str(''.join(div.xpath('div/a[contains(@class,"img-flex")]//text()').extract()))
                    comefrom = div.xpath('div/div[contains(@class,"box-translation")]/div/text()').extract_first('').split('-')[0]
                if div.xpath('div/div/div[@class="space-small"]'):
                    for div in div.xpath('div/div/div[@class="space-small"]'):
                        title = ''.join(div.xpath('a/div[@class="text-layout"]/h4//text()').extract())
                        comefrom = div.xpath('a/div[@class="text-layout"]/div/span/text()').extract_first('')
                        contents = ''
                        link = Untiles.get_url(link)
                        check = CheckMysql()
                        link = Untiles.get_url(link)
                        res = check.select(link)
                        # check.closeMysql()
                        if res:
                            continue
                        res = Emotion.post(text=title, title='搜狗移动')
                        if '百科' in title:
                            res = 1
                            size1 = '1'
                        item = BaiduspiderItem(
                            title=title,
                            elasticsearch='搜狗移动',
                            key=response.meta['key'],
                            comefrom=comefrom,
                            link=link,
                            index=index,
                            content=contents,
                            type=res,
                            page=response.meta['page'],
                            size1=size1,
                        )
                        yield item
                    continue
                elif div.xpath('div/div[@class="article-item"]'):
                    comefrom = get_comefrom(title,code='搜狗移动搜搜')
                    title = div.xpath('div/a[@class="article-link"]/div[@class="article-layout"]/h4/text()').extract_first('')
                    link = div.xpath('div/a[@class="article-link"]/@href').extract_first('')
                    if 'http' not in link:
                        link = self.bulit_url + link
                    contents =  Untiles.check_str(''.join(div.xpath('div/a[@class="article-link"]/div[@class="img-flex"]//text()').extract()))
                    if div.xpath('div/div[@class="article-item"]/a'):
                        for a in div.xpath('div/div[@class="article-item"]/a'):
                            link = a.attrib['href']
                            title = ''.join(a.xpath('h4//text()').extract())
                            link = Untiles.get_url(link)
                            check = CheckMysql()
                            link = Untiles.get_url(link)
                            res = check.select(link)
                            # check.closeMysql()
                            if res:
                                continue
                            res = Emotion.post(text=title, title='搜狗移动')
                            if '百科' in title:
                                res = 1
                                size1 = '1'
                            if not comefrom:
                                comefrom = get_comefrom(title, code='搜狗搜索')
                            _items = BaiduspiderItem(
                                title=title,
                                elasticsearch='搜狗移动',
                                key=response.meta['key'],
                                comefrom=comefrom,
                                link=link,
                                index=index,
                                content=contents,
                                type=res,
                                page=response.meta['page'],
                                size1=size1,
                            )
                            yield _items
                        continue
            else:
                print('详情url', response.url)
                continue
            link = Untiles.get_url(link)
            check = CheckMysql()
            link = Untiles.get_url(link)
            res = check.select(link)
            # check.closeMysql()
            if res:
                continue
            res = Emotion.post(text=title, title='搜狗移动')
            if '百科' in title:
                res = 1
                size1 = '1'
            if not comefrom:
                comefrom = get_comefrom(title,code='搜狗移动搜索')
            _item = BaiduspiderItem(
                title=title,
                elasticsearch='搜狗移动',
                key=response.meta['key'],
                comefrom=comefrom,
                link=link,
                index=index,
                content=contents,
                type=res,
                page=response.meta['page'],
                size1=size1,
            )
            yield _item
        if response.xpath('//div[@class="result"]'):
            index = int(response.xpath('//div[@class="result"]/@data-v').extract_first(''))
            title = ''.join(response.xpath('//div[@class="result"]/a/h3//text()').extract())
            link = response.xpath('//div[@class="result"]/a/@href').extract_first('')
            if 'http' not in link:
                link = self.bulit_url + link
            contents = Untiles.check_str(''.join(response.xpath('//div[@class="result"]/a/div//text()').extract()))
            link = Untiles.get_url(link)
            check = CheckMysql()
            link = Untiles.get_url(link)
            res = check.select(link)
            # check.closeMysql()
            if not res:
                res = Emotion.post(text=title, title='搜狗移动')
                if '百科' in title:
                    res = 1
                    size1 = '1'
                _item_ = BaiduspiderItem(
                    title=title,
                    elasticsearch='搜狗移动',
                    key=response.meta['key'],
                    comefrom=comefrom,
                    link=link,
                    index=index,
                    content=contents,
                    type=res,
                    page=response.meta['page'],
                    size1=size1,
                )
                yield _item_

        #为您推荐
        res = response.xpath('//div[@id="J_recommend"]/p/a')
        if res:
            for a in res:
                title = a.xpath('/text()').extract_first('')
                res = Emotion.post(title)
                if res == 0:
                    negative_prob = 0.5
                    positive_prob = 0.5
                else:
                    (positive_prob, negative_prob) = res
                item_ = BaiduItem(title=title, elasticsearch='搜狗移动', key=response.meta['key'], comefrom='相关搜索',
                                 type=negative_prob, link=positive_prob)
                yield item_
        #相关搜搜
        resp = response.xpath('//div[@id="hint"]/ul/li/a')
        if resp:
            for a in resp:
                title = a.xpath('/text()').extract_first('')
                res = Emotion.post(title)
                if res == 0:
                    negative_prob = 0.5
                    positive_prob = 0.5
                else:
                    (positive_prob, negative_prob) = res
                item = BaiduItem(title=title, elasticsearch='搜狗移动', key=response.meta['key'], comefrom='相关搜索',
                                 type=negative_prob, link=positive_prob)
                yield item
        #下一页
        next_url = 'https://m.sogou.com/web/search/ajax_query.jsp?keyword={key}&p={page}'
        for page in range(2,10):
            print('正在爬取第{}页'.format(page))
            response.meta['page'] = page
            yield scrapy.Request(url=next_url.format(key=response.meta['key'],page=page),callback=self.parse,meta=response.meta)
    def pull_parse(self,response):
        string = re.search(re.compile('window.*?\((.*?)\)'),response.text).group(1)
        res = json.loads(string)
        for title in res['s']:
            res = Emotion.post(title)
            if res == 0:
                negative_prob = 0.5
                positive_prob = 0.5
            else:
                (positive_prob, negative_prob) = res
            items = PullKeyItem(
                elasticsearch='搜狗移动',
                key=response.meta['key'],
                title=title,
                type=negative_prob,
                index=positive_prob
            )
            yield items