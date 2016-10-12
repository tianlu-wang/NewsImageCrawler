import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf8')


year = '2013'
link_list = 'assets/link_list/%s.list' % year

class Time_Spider_history(scrapy.Spider):
    name = "time_spider_history"

    def start_requests(self):
        with open(link_list) as f:
            content = f.readlines()
        for item in content:
            url = 'http://' + item.replace('\n', '')
            yield scrapy.Request(url=url, callback=self.parse_save)

    def parse_save(self, response):
        if 'money.cnn.com' in response.url:
            print "************************************"
            print response.url
            page = response.url.split("/")[8]
            filename = './output/cnn/%s/%s.html' % (year, page)
            with open(filename, 'wb') as f:
                f.write(response.xpath('//main[@class="container js-social-anchor-start"]').extract()[0])
        elif 'www.cnn.com' in response.url:
            print "************************************"
            print response.url
            page = response.url.split("/")[7]
            filename = './output/cnn/%s/%s.html' % (year, page)
            with open(filename, 'wb') as f:
                divs = response.xpath('//div[@class="l-container"]')
                for div in divs:
                    tmp = div.xpath('.//h1/text()').extract()
                    if not tmp:
                        pass
                    else:
                        f.write(div.extract())
                        break
