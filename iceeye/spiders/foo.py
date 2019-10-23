import scrapy


class FooSpider(scrapy.Spider):
    name = 'foo'

    def start_requests(self):
        urls = ['http://www.baidu.com']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response)
        #self.log(response)

