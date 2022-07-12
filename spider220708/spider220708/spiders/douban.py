import random

import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse

from spider220708.items import MovieItem

"""
learn https:https://www.bilibili.com/video/BV1QY411F7Vt?p=1&vd_source=b868253de0bd92751d3bfc7de7493667
"""
"""
当要进行抓包获取url时，需要在Request抓包的url
当抓包的参数params or data时，写在哪里

当数据是json时吗，pandas提供了一个比较好的包
    data_json1 = response.get('json数据中的一层')
    data_json2 = data_json1.get('json中继续往下一层')
    from pandas.io.json import json_normalize
    data = json_normalize(data_json)
    
    movie_item = MovieItem()
    movie_item['x1] = data[''].values()
    
"""
"""
在Anaconda Prompt中定位到文件位置
创建scrapy项目：scrapy startproject name
进入项目
生产具体的爬取文件：scrapy genspider name 爬取的网页名(movie.com)

运行项目，并存入csv:scrapy crawl douban -o name.csv  小数据的时候建议使用这个 要关闭其他已写的管道
"""


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']

    # start_urls = ['http://movie.douban.com/top250']

    def start_requests(self):
        # https = [
        #     {'https': '110.250.28.32:8118'},
        #     {'https': '180.123.204.78:61234'},
        #     {'https': '122.195.200.126:40049'},
        #     {'https': '47.100.7.167:8989'}
        # ]
        # http = [
        #     {'http': '120.78.95.211:8866'},
        #     {'http': '47.97.189.164:8001'},
        #     {'http': '120.78.76.107:8866'},
        #     {'http': '47.93.4.253:8888'},
        # ]
        for page in range(10):
            # meta = {'proxy': random.choice(https)}加代理
            # cookies =
            yield Request(url=f'https://movie.douban.com/top250?start={page * 25}&filter=')

    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        list_items = sel.css('#content > div > div.article > ol > li')
        for list_item in list_items:
            detail_url = list_item.css('div.info > div.hd > a::attr(href)').extract_first()

            movie_item = MovieItem()
            movie_item['title'] = list_item.css('span.title::text').extract_first()
            movie_item['rank'] = list_item.css('span.rating_num::text').extract_first()
            movie_item['subject'] = list_item.css('span.inq::text').extract_first()
            # yield movie_item
            yield Request(url=detail_url,
                          callback=self.parse_detail,
                          cb_kwargs={'item': movie_item})

    def parse_detail(self, response, **kwargs):
        movie_item = kwargs['item']
        sel = Selector(response)
        movie_item['duration'] = sel.css('span[property="v:runtime"]::attr(content)').extract_first()
        movie_item['introduce'] = sel.css('span[property="v:summary"]::text').extract_first() or ''
        yield movie_item

        # hrefs_list = sel.css('div.paginator > a::attr(href)')
        # for href in hrefs_list:
        #     url = response.urljoin(href.extract())
        #     yield Request(url=url)
