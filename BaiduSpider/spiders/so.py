# -*- coding: utf-8 -*-
from ..items import *
from ..untils.until import *
from ..untils.api import Emotion


class SoSpider(scrapy.Spider):
    name = 'so'
    allowed_domains = ['so.com']
    urls = 'https://www.so.com'

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            "Upgrade-Insecure-Requests": "1",
             }
    }

    def start_requests(self):
        keys = CheckMysql()
        for x in keys.get_key():
            print('key', x)
            key = parse.quote(x)
            yield scrapy.Request(url='https://www.so.com/s?ie=utf-8&fr=none&src=360sou_newhome&q={}'.format(key),
                                 callback=self.parse, meta={'key': x})
            yield scrapy.Request(
                url='https://sug.so.360.cn/suggest?callback=suggest_so&encodein=utf-8&encodeout=utf-8&format=json&fields=word&word={}'.format(
                    key),
                callback=self.pull_parse)
        # keys.closeMysql()

    def parse(self, response):
        size1 = '0'
        comefrom = '360搜索'
        # 下一页
        next_link = response.xpath('//a[contains(text(),"下一页")]/@href').extract_first('')
        try:
            page = re.search(re.compile('pn=(\d+)'), next_link).group(1)
            if int(page) >= 11:
                return
        except Exception as e:
            print(response.url)
            yield scrapy.Request(
                url='https://www.so.com/s?ie=utf-8&fr=none&src=360sou_newhome&q={}'.format(response.meta['key']),
                callback=self.parse, meta=response.meta)
        else:
            # 详情
            for inde, li in enumerate(response.xpath('//ul[@class="result"]/li')):
                if li.xpath('h3/a//text()').extract():
                    """div class 包含res-rich"""
                    _title = li.xpath('h3/a//text()').extract()
                    title = Untiles.check_str(''.join(_title))
                    link = li.xpath('h3/a/@href').extract_first('')
                    divs = li.xpath('div[contains(@class,"res-rich")]/div[@class="res-comm-con"]')
                    _contents = divs.xpath('p[1]//text()').extract()
                    _come_from = divs.xpath('p[@class="res-linkinfo"]/a[@class="mingpian"]//text()').extract()
                    if li.xpath('div[contains(@class,"res-rich")]/div/span'):
                        _contents = li.xpath('div[contains(@class,"res-rich")]/div//text()').extract()
                        _come_from = li.xpath(
                            'div[contains(@class,"res-rich")]/div/p/a[@class="mingpian"]/text()').extract()
                        if _come_from == []:
                            _come_from = li.xpath('div/p[@class="res-linkinfo"]/a[@class="mingpian"]/text()').extract()
                    elif li.xpath('div[contains(@class,"res-rich")]/div/div'):
                        _contents = li.xpath('div[contains(@class,"res-rich")]//text()').extract()
                        _come_from = li.xpath(
                            'div[contains(@class,"res-rich")]/p/a[@class="mingpian"]/text()').extract()
                        if li.xpath('div[contains(@class,"res-rich")]/div[@class="clearfix"]'):
                            _come_from = li.xpath(
                                'div[contains(@class,"res-rich")]/div/div/p[@class="res-linkinfo"]/a[@class="mingpian"]/text()').extract()
                    elif li.xpath('p[@class="res-desc"]').extract():
                        title = Untiles.check_str(''.join(li.xpath('h3/a//text()').extract()))
                        link = li.xpath('h3/a/@href').extract_first()
                        _contents = li.xpath('p[@class="res-desc"]//text()').extract()
                        _come_from = li.xpath('p[@class="res-linkinfo"]/a[@class="mingpian"]/text()').extract()
                        if _come_from == []:
                            _come_from = get_comefrom(title, code='360搜索')
                    elif li.xpath('div[contains(@class,"res-rich")]/p'):
                        _come_from = li.xpath(
                            'div[contains(@class,"res-rich")]/p/a[@class="mingpian"]/text()').extract()
                        _contents = li.xpath('div[contains(@class,"res-rich")]//text()').extract()
                    if _come_from == []:
                        _come_from = get_comefrom(title, code='360搜索')
                    comefrom = Untiles.check_str(''.join(_come_from))
                    if "360百科" in title or '百度百科' in title:
                        type = 1
                        if '360百科' in title:
                            comefrom = '360百科'
                        else:
                            comefrom = '百度百科'
                        contents = Untiles.check_str(''.join(_contents))
                        _items = BaiduspiderItem(
                            elasticsearch='360PC',
                            title=title,
                            key=response.meta['key'],
                            comefrom=comefrom,
                            link=link,
                            type=type,
                            size1='1',
                            page=page,
                            index=inde,
                            content=contents
                        )
                        yield _items
                        continue
                elif li.xpath('div[contains(@class,"g-mohe")]'):
                    if li.xpath('div[contains(@class,"g-mohe")]/h3[@class="mh-t-h3"]'):
                        _a = li.xpath('div[contains(@class,"g-mohe")]/h3[@class="mh-t-h3"]/a')
                        _title = li.xpath('div[contains(@class,"g-mohe")]/h3[@class="mh-t-h3"]/a//text()').extract()
                        title = Untiles.check_str(''.join(_title))
                        _contents = li.xpath('div[contains(@class,"g-mohe")]/div//text()').extract()
                        link = _a.attrib['href']
                        comefrom = get_comefrom(title, code='360搜索')

                    elif li.xpath('div[contains(@class,"g-mohe")]/h3[@class="title"]'):
                        """图片"""
                        _a = li.xpath('div[contains(@class,"g-mohe")]/h3[@class="title"]/a')
                        link = _a.attrib['href']
                        _title = li.xpath('div[contains(@class,"g-mohe")]/h3[@class="title"]/a//text()').extract()
                        title = Untiles.check_str(''.join(_title))
                        comefrom = get_comefrom(title, code='360搜索')
                        _contents = ['图片']
                    elif li.xpath('div[contains(@class,"g-mohe")]/div/h3[@class="title"]'):
                        """最新相关信息"""
                        divs = li.xpath('div[contains(@class,"g-mohe")]/div/div[@class="cont"]')
                        link = divs.xpath('div[@class=" mh-position"]/div/a/@href').extract_first('')
                        title = divs.xpath('div[@class=" mh-position"]/div/a/@title').extract_first('')
                        _contents = divs.xpath(
                            'div[contains(@class,"mh-first")]/div[@class="mh-first-news"]/p[1]/text()').extract()
                        comefrom = divs.xpath('div[@class=" mh-position"]/div/span/text()').extract_first('')
                        for li in response.xpath('//ul[contains(@class,"mh-list")]/li'):
                            title = li.xpath('div/a/@title').extract_first('')
                            link = li.xpath('div/a/@href').extract_first('')
                            if li.xpath('a'):
                                link = li.xpath('a/@href').extract_first('')
                            comefrom = li.xpath('div/span/text()').extract_first('')
                            link = Untiles.get_url(link)
                            check = CheckMysql()
                            res = check.select(link)
                            # check.closeMysql()
                            if not link or res:
                            # if not link:
                                continue
                            ress = Emotion.post(text=title,title='360PC')
                            items = BaiduspiderItem(
                                title=title,
                                elasticsearch='360PC',
                                key=response.meta['key'],
                                comefrom=comefrom,
                                link=link,
                                index=inde + 1,
                                content='',
                                type=ress,
                                page=page,
                                size1=size1,
                            )
                            yield items
                        continue
                    elif li.xpath('div[contains(@class,"g-mohe")]/h3[@class="res-title"]'):
                        title = li.xpath('div[contains(@class,"g-mohe")]/h3[@class="res-title"]//text()').extract()
                        title = Untiles.check_str(''.join(title))
                        link = li.xpath('div[contains(@class,"g-mohe")]/h3[@class="res-title"]/a/@href').extract_first('')
                        _contents = li.xpath('div[contains(@class,"g-mohe")]/div//text()').extract()
                if not comefrom:
                    comefrom = '360搜搜'
                    print('没有comefrom', title, response.url)
                if not link:
                    return
                link = Untiles.get_url(link)
                check = CheckMysql()
                res = check.select(link)
                # check.closeMysql()
                contents = Untiles.check_str(''.join(_contents))
                if res:
                    continue
                res = Emotion.post(text=title,title='360PC')
                item = BaiduspiderItem(
                    title=title,
                    elasticsearch='360PC',
                    key=response.meta['key'],
                    comefrom=comefrom,
                    link=link,
                    index=inde + 1,
                    content=contents,
                    type=res,
                    page=page,
                    size1=size1,
                )
                yield item
            # 相关搜搜
            rele_texts = response.xpath('//div[@id="rs"]/table/tbody/tr')
            if not rele_texts:
                rele_texts = response.xpath('//div[@id="rs"]/table/tr')
            for tr in rele_texts:
                rele_title = re.findall(re.compile('<a.*?href=\"(.*?)\">(\w+)</a>'), ''.join(tr.extract()))
                for reles in rele_title:
                    rele_title = reles[1]
                    res = Emotion.post(rele_title)
                    if res == 0:
                        negative_prob = 0.5
                        positive_prob = 0.5
                    else:
                        (positive_prob, negative_prob) = res
                    item = BaiduItem(
                        elasticsearch='360PC',
                        key=response.meta['key'],
                        comefrom='相关搜索',
                        title=rele_title,
                        type=negative_prob,
                        link=positive_prob
                    )
                yield item
            print('正在爬取{}页................'.format(page))
            if 'http' not in next_link:
                next_link = self.urls + next_link
            yield scrapy.Request(url=next_link, callback=self.parse, meta=response.meta,
                                 headers={'Referer': response.url})

    def pull_parse(self, response):
        res = re.search(re.compile('suggest_so\((.*?)\)'), response.text).group(1)
        dict = json.loads(res)
        result = dict['result']
        key = dict['query']
        for obj in result:
            pull_title = obj['word']
            res = Emotion.post(pull_title)
            if res == 0:
                negative_prob = 0.5
                positive_prob = 0.5
            else:
                (positive_prob, negative_prob) = res
            items = PullKeyItem(
                elasticsearch='360PC',
                key=key,
                title=pull_title,
                type=negative_prob,
                index=positive_prob
            )
            yield items
