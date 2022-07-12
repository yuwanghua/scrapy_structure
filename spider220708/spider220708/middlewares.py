# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals, Request

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


def get_cookies_dict():
    cookies_str = 'bid=tIanlN-aDLA; ap_v=0,6.0; __utmc=30149280; ' \
                  '__utmz=30149280.1657504567.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none);' \
                  ' __utmc=223695111;' \
                  ' __utmz=223695111.1657504567.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none);' \
                  ' __utma=30149280.129390596.1657504567.1657504567.1657509275.2; ' \
                  '__utmb=30149280.0.10.1657509275;' \
                  ' __utma=223695111.403343429.1657504567.1657504567.1657509275.2; ' \
                  '__utmb=223695111.0.10.1657509275;' \
                  ' _pk_ses.100001.4cf6=*; ' \
                  '_pk_id.100001.4cf6=d74502907edaa0cf.1657504567.2.1657510132.1657504664.'
    cookies_dict = {}
    for item in cookies_str.split(';'):
        key, value = item.split('=', maxsplit=1)
        cookies_dict['key'] = value
    return cookies_dict

COOKIES_DICT = get_cookies_dict()

class Spider220708SpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Spider220708DownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request: Request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # 代理在中间件中解决
        # request.meta = {'proxy': ''}
        # cookie添加
        # request.cookies = COOKIES_DICT
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
