import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf8')


year = '2013'
link_list = 'assets/link_list/time/test.list'


class Time_Spider_history(scrapy.Spider):
    name = "time_spider_history"

    def start_requests(self):
        with open(link_list) as f:
            content = f.readlines()
        for item in content:
            url = 'curl "https://twitter.com/i/cards/tfw/v1/%s?cardname=summary_large_image&autoplay_' \
                  'disabled=true&forward=true&earned=true&lang=en&card_height=344' % item
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print response
