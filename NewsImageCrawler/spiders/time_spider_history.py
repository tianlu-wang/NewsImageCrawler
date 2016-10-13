import scrapy
import sys
import ast
import json
reload(sys)

sys.setdefaultencoding('utf8')


time = '201601'
link_list = 'assets/htmls/time/%s.ids' % time


class Time_Spider_history(scrapy.Spider):
    name = "time_spider_history"
    out = open('output/time/list/%s' % time, 'w')  # TODO

    def start_requests(self):
        with open(link_list) as f:
            content = f.readlines()
        for item in content:
            item = item.replace('\n', '')
            url = 'https://twitter.com/i/cards/tfw/v1/%s?cardname=summary_large_image&autoplay_disabled=true&' \
                  'forward=true&earned=true&lang=en&card_height=344' % item
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        card_info = json.loads(response.xpath('//script/text()').extract_first().encode('utf-8'))
        self.out.write(card_info['card']['card_url'] + '\n')
        self.out.write(response.xpath('//div[@class="tcu-imageWrapper"]/img/@data-src').extract_first() + '\n')
        self.out.write(response.xpath('//h2/text()').extract_first() + '\n')
        self.out.write(response.xpath('//p/text()').extract_first() + '\n')
        self.out.write('\n')
