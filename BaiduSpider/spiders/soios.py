# -*- coding: utf-8 -*-
import scrapy
import json
from urllib import parse
from ..untils.until import *
from ..untils.api import Emotion
from ..items import *


class SoiosSpider(scrapy.Spider):
    name = 'soios'
    allowed_domains = ['m.so.com']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Host':'m.so.com',
            'Connection':'keep-alive',
            'User-Agent':'Mozilla/5.0 (Linux; Android 4.4.2; OPPO R11 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
            'Accept':'*/*',
            'Accept-Encoding':'gzip,deflate',
            'Accept-Language':'zh-CN,en-US;q=0.8',
            'X-Requested-With':'com.android.browser'}
    }
    start_url = 'https://m.so.com/nextpage?q={key}&src=suggest_history&srcg=home_next&pn={page}&ajax=1'
    pull_url = 'https://m.so.com/suggest/mso?kw={key}&caller=strict&sensitive=strict&count=10'
    bulit_url = 'https://m.so.com'
    def start_requests(self):
        keys = CheckMysql()
        for key in keys.get_key():
            yield scrapy.Request(url=self.pull_url.format(key=parse.quote(key)), callback=self.pull_parse,meta={'key': key})
            for x in range(0, 10):
                yield scrapy.Request(url=self.start_url.format(key=parse.quote(key),page=x),callback=self.parse,meta={'key':key,'page':int(int(x)+1)})

    def parse(self, response):
        print(response.url)
        size1 = '0'
        print('正在爬取{},第{}页'.format(response.meta['key'],response.meta['page']))
        for index,div in enumerate(response.xpath('//div[contains(@class,"res-list")]')):
            if div.xpath('a[@class="title"]'):
                title = ''.join(div.xpath('a[@class="title"]//text()').extract())
                link = div.xpath('a[@class="title"]/@href').extract_first('')
                contents = Untiles.check_str(''.join(div.xpath('div[@class="mohe-cont"]//text()').extract()))
                if 'http' not in link:
                    link = self.bulit_url + link
                comefrom = get_comefrom(title,code='360移动搜搜')
            elif div.xpath('a[@class="alink"]'):
                title = ''.join(div.xpath('a[@class="alink"]/h3//text()').extract())
                link = div.xpath('a[@class="alink"][1]/@href').extract_first('')
                if 'http' not in link:
                    link = self.bulit_url + link
                contents = Untiles.check_str(''.join(div.xpath('a[@class="alink"]/div/div[contains(@class,"con")]//text()').extract()))
                comefrom = div.xpath('div[@class="res-supplement"]/cite/span/text()').extract_first('')
            elif div.xpath('div[@class="mso-guide"]/div/div/ul/li'):
                for x in div.xpath('div[@class="mso-guide"]/div/div/ul/li'):
                    title = x.xpath('div/a/text()').extract_first('')
                    """相关搜索"""
                    res = Emotion.post(title)
                    if res == 0:
                        negative_prob = 0.5
                        positive_prob = 0.5
                    else:
                        (positive_prob, negative_prob) = res
                    _item_ = BaiduItem(title=title, elasticsearch='360移动', key=response.meta['key'], comefrom='相关搜索',
                                      type=negative_prob, link=positive_prob)
                    yield _item_
                continue
            else:
                print(response.url)
                print('哈哈')
            link = Untiles.get_url(link)
            check = CheckMysql()
            link = Untiles.get_url(link)
            res = check.select(link)
            # check.closeMysql()
            if res:
                continue
            res = Emotion.post(text=title, title='百度移动')
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
        #为你推荐
        for ti in response.xpath('//div[@id="main"]/div[@class="top-rec"]/div[@class="rec-list"]/a/text()').extract():
            if not ti:
                continue
            res = Emotion.post(ti)
            if res == 0:
                negative_prob = 0.5
                positive_prob = 0.5
            else:
                (positive_prob, negative_prob) = res
            _item = BaiduItem(title=ti, elasticsearch='360移动', key=response.meta['key'], comefrom='相关搜索',
                             type=negative_prob, link=positive_prob)
            yield _item

        #相关搜索
        for x in response.xpath('//div[@class="related-search-waterflow"]/ul/li'):
            title = x.xpath('div/a/text()').extract_first('')
            if not title:
                continue
            res = Emotion.post(title)
            if res == 0:
                negative_prob = 0.5
                positive_prob = 0.5
            else:
                (positive_prob,negative_prob) = res
            item = BaiduItem(title=title, elasticsearch='360移动', key=response.meta['key'], comefrom='相关搜索',
                             type=negative_prob,link=positive_prob)
            yield item
    def pull_parse(self,response):
        resp = json.loads(response.text)
        if resp['errno'] == '0':
            for x in resp['data']['sug']:
                title = x['word']
                res = Emotion.post(title)
                if res == 0:
                    negative_prob = 0.5
                    positive_prob = 0.5
                else:
                    (positive_prob, negative_prob) = res
                items = PullKeyItem(
                    elasticsearch='360移动',
                    key=response.meta['key'],
                    title=title,
                    type=negative_prob,
                    index=positive_prob
                )
                yield items