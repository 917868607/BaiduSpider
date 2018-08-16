# -*- coding: utf-8 -*-
import scrapy
from ..untils.until import *
from ..untils.api import Emotion
from ..items import *


class SogouSpider(scrapy.Spider):
    name = 'sogou'
    allowed_domains = ['sogou.com']
    bult_url = 'https://www.sogou.com/web'
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
            'Connection': 'keep-alive',
            "Upgrade-Insecure-Requests": "1"
        }
    }
    def start_requests(self):
        keys = CheckMysql()
        for x in keys.get_key():
            yield scrapy.Request(url='https://www.sogou.com/web?query={}&page=1'.format(parse.quote(x)),callback=self.parse,meta={'key':x})
            yield scrapy.Request(url='https://www.sogou.com/suggnew/ajajjson?key={}&type=web'.format(parse.quote(x)),callback=self.parse_pull,meta={'key':x})
    def parse(self, response):
        #下一页
        size1 = '0'
        next_page = response.xpath('//a[contains(text(),"下一页")]/@href').extract_first('')
        try:
            page = int(re.search(re.compile('page=(\d+)'),next_page).group(1)) - 1
        except Exception as e:
            print(e)
            with open('test/sogou.html','w',encoding='utf-8') as f:
                f.write(response.text)
            yield scrapy.Request(url=response.url,callback=self.parse,meta=response.meta)
        for index,div in enumerate(response.xpath('//div[@class="results"]/div')):
            if div.attrib['class'] == 'vrwrap':
                title = div.xpath('h3/a//text()').extract()
                if title == []:
                    for a in div.xpath('div[@class="hint-mid"]/a'):
                        title = a.xpath('text()').extract_first('')
                        res = Emotion.post(title)
                        if res == 0:
                            negative_prob = 0.5
                            positive_prob = 0.5
                        else:
                            (positive_prob, negative_prob) = res
                        item = BaiduItem(title=title,elasticsearch='搜狗PC',key=response.meta['key'],comefrom='相关搜索',type=negative_prob,link=positive_prob)
                        yield item
                    continue
                title = Untiles.check_str(''.join(title))
                comefrom = get_comefrom(title,code='搜狗搜搜')
                link = div.xpath('h3/a/@href').extract_first('')
                if 'http' not in link:
                    link = 'https://www.sogou.com' + link
                link = Untiles.get_url(link)
                if div.xpath('div[@class="strBox"]'):
                    contents = div.xpath('div[@class="strBox"]//text()').extract()
                    contents = Untiles.check_str(''.join(contents))
                elif div.xpath('div[@class="str_info_div"]'):
                    contents = div.xpath('div[@class="str_info_div"]//text()').extract()
                    contents = Untiles.check_str(''.join(contents))
                elif div.xpath('div[@class="vr-west-lake150814"]'):
                    contents = div.xpath('div[@class="vr-west-lake150814"]/p//text()').extract()
                    contents = Untiles.check_str(''.join(contents))
                elif div.xpath('div[@class="vr-car161201"]'):
                    contents = div.xpath('div[@class="vr-car161201"]//text()').extract()
                    contents = Untiles.check_str(''.join(contents))
                elif div.xpath('div[@class="str-text-info"]'):
                    contents = div.xpath('div[@class="str-text-info"]//text()').extract()
                    contents = Untiles.check_str(''.join(contents))
                elif div.xpath('div[contains(@class,"str-pd-box")]'):
                    """相关内容"""
                    title = div.xpath('div[contains(@class,"str-pd-box")]/p[contains(@class,"str_time")]/a/text()').extract()
                    title = Untiles.check_str(''.join(title))
                    link = div.xpath('div[contains(@class,"str-pd-box")]/p[contains(@class,"str_time")]/a/@href').extract_first()
                    if 'http' not in link:
                        link = 'https://www.sogou.com' + link
                    link = Untiles.get_url(link)
                    contents = div.xpath('div[contains(@class,"str-pd-box")]/p[contains(@class,"str_info")]//text()').extract()
                    contents = Untiles.check_str(''.join(contents))
                    comefrom = ''.join(div.xpath('div[contains(@class,"str-pd-box")]/p[3]//text()').extract())
                    title1 = div.xpath('div[contains(@class,"str-pd-box")]/ul/li/a//text()').extract()
                    title1 = Untiles.check_str(''.join(title1))
                    link1 = div.xpath('div[contains(@class,"str-pd-box")]/ul/li/a/@href').extract_first('')
                    comefrom1 = div.xpath('div[contains(@class,"str-pd-box")]/ul/li/strong/text()').extract_first('')
                    if 'http' not in link1:
                        link1 = 'https://www.sogou.com' + link1
                    link1 = Untiles.get_url(link1)
                    check = CheckMysql()
                    res = check.select(link)
                    ress = check.select(link1)
                    # check.closeMysql()
                    if res:
                        continue
                    if ress:
                        continue
                    res = Emotion.post(text=title,title='搜狗PC')
                    item = BaiduspiderItem(
                        title=title,elasticsearch='搜狗PC',key=response.meta['key'],comefrom=comefrom,link=link,
                        index=index + 1,content=contents,type=res,page=page,size1=size1)
                    ress = Emotion.post(text=title,title='搜狗PC')
                    itemm = BaiduspiderItem(
                        title=title1,elasticsearch='搜狗PC',key=response.meta['key'],comefrom=comefrom1,link=link1,
                        index=index + 1,content=contents,type=ress,page=page,size1=size1)
                    yield item
                    yield itemm
                    continue
                elif div.xpath('div[@class="vr-skin150825"]'):
                    contents = div.xpath('div[@class="vr-skin150825"]//text()').extract()
                    contents = Untiles.check_str(''.join(contents))
                elif div.xpath('div[@class="str-box-v4"]'):
                    for li in div.xpath('div[@class="str-box-v4"]/ul[@class="bar-list"]/li'):
                        title = li.xpath('a//text()').extract()
                        title = Untiles.check_str(''.join(title))
                        link = li.xpath('a/@href').extract_first('')
                        if 'http' not in link:
                            link = 'https://www.sogou.com' + link
                        link = Untiles.get_url(link)
                        contents = ''
                        check = CheckMysql()
                        res = check.select(link)
                        # check.closeMysql()
                        if res:
                            continue

                        res = Emotion.post(text=title,title='搜狗PC')
                        _item = BaiduspiderItem(
                            title=title, elasticsearch='搜狗PC', key=response.meta['key'], comefrom=comefrom, link=link,
                            index=index + 1, content=contents, type=res, page=page, size1=size1)
                        yield _item
                    continue
            elif div.attrib.get('class','re') == 'rb':
                title = div.xpath('h3/a//text()').extract()
                title = ''.join(title)
                comefrom = get_comefrom(title,code='搜狗搜搜')
                link = div.xpath('h3/a/@href').extract_first('')
                if 'http' not in link:
                    link = 'https://www.sogou.com' + link
                link = Untiles.get_url(link)
                contents = div.xpath('div[@class="ft"]//text()').extract()
                contents = Untiles.check_str(''.join(contents))
            if not title:
                with open('test/sogou.html','w',encoding='utf-8') as f:
                    f.write(response.text)
                print('hahah')
            check = CheckMysql()
            res = check.select(link)
            # check.closeMysql()
            if res:
                continue
            res = Emotion.post(text=title,title='搜狗PC')
            if '百科' in title:
                res = 1
                size1 = '1'
            item = BaiduspiderItem(
                title=title,
                elasticsearch='搜狗PC',
                key=response.meta['key'],
                comefrom=comefrom,
                link=link,
                index=index + 1,
                content=contents,
                type=res,
                page=page,
                size1=size1,
            )
            yield item
        #相关搜搜
        trs = response.xpath('//table[@id="hint_container"]/tr')
        for title in [td.xpath('p/a/text()').extract_first('') for tr in trs for td in tr.xpath('td')]:
            res = Emotion.post(title)
            if res == 0:
                negative_prob = 0.5
                positive_prob = 0.5
            else:
                (positive_prob, negative_prob) = res
            items = BaiduItem(title=title, elasticsearch='搜狗PC', key=response.meta['key'], comefrom='相关搜索',
                             type=negative_prob,link=positive_prob)
            yield items
        print('开始爬取关键词{key},第{page}页'.format(key=response.meta['key'],page=re.search(re.compile('page=(\d+)'),next_page).group(1)))
        if page == 10:
            return
        if 'https' not in next_page:
            next_page = self.bult_url + next_page
        yield  scrapy.Request(url=next_page,callback=self.parse,meta=response.meta,headers={'Referer':response.url})

    def parse_pull(self,response):
        key = response.meta['key']
        print('关键字',key)
        str = re.search(re.compile('window.*?\((.*?),-1'),response.text).group(1)
        list1 = re.findall(re.compile(',\[(.*?)\]'), str)[0].replace('"', '').split(',')
        for x in list1:
            res = Emotion.post(x)
            if res == 0:
                negative_prob = 0.5
                positive_prob = 0.5
            else:
                (positive_prob, negative_prob) = res
            items = PullKeyItem(elasticsearch='搜狗PC',key=response.meta['key'],title=x,type=negative_prob,index=positive_prob)
            yield items