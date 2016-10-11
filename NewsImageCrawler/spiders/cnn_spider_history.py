import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re
import logging


month = '06'
link_list = 'assets/link_list/16/%s.list' % month

class CNN_Spider_history(scrapy.Spider):
    name = "cnn_spider_history"

    def start_requests(self):
        with open(link_list) as f:
            content = f.readlines()
        for item in content:
            url = 'http://' + item.replace('\n', '')
            yield scrapy.Request(url=url, callback=self.parse_save)

    # def parse(self, response):
    #     print '888888888888888888888888'
    #     print response.url
    #     url = response.headers['Location']
    #     print '---------------------------'
    #     print url
    #     if 'cnn' in url or 'CNN' in url:
    #         scrapy.Request(url, callback=self.parse_save)

    def parse_save(self, response):
        if 'money.cnn.com' in response.url:
            print "************************************"
            print response.url
            page = response.url.split("/")[8]
            filename = './output/cnn/16/%s/%s.html' % (month, page)
            with open(filename, 'wb') as f:
                f.write(response.xpath('//main[@class="container js-social-anchor-start"]').extract()[0])
        elif 'www.cnn.com' in response.url:
            print "************************************"
            print response.url
            page = response.url.split("/")[7]
            filename = './output/cnn/16/%s/%s.html' % (month, page)
            with open(filename, 'wb') as f:
                divs = response.xpath('//div[@class="l-container"]')
                for div in divs:
                    tmp = div.xpath('.//h1/text()').extract()
                    if not tmp:
                        pass
                    else:
                        f.write(div.extract())
                        break
