import scrapy
import re
from NewsImageCrawler.items import SubWebsiteItem

class CNN_Spider(scrapy.Spider):
    name = "cnn_spider"

    def start_requests(self):
        url = "http://www.cnn.com/"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        sub_websites = []
        for item in response.xpath('//li[@class="m-footer__list-item"]'):
            sub_website = SubWebsiteItem()
            sub_website['name'] = item.xpath('.//a/text()').extract_first()
            sub_website['url'] = item.xpath('.//a/@href').extract_first()
            sub_websites.append(sub_website)
        for sub_website in sub_websites:
            if re.match(r'^(http://bleacherreport.com/)', sub_website['url']):
                pass  # do nothing with bleacherreport website
            elif re.match(r'^(http|//)', sub_website['url']):
                yield scrapy.Request(sub_website['url'], callback=self.parse_money)
            else:
                yield scrapy.Request(response.urljoin(sub_website['url']), callback=self.parse_cnn)

    def parse_cnn(self, response):

    def parse_money(self, response):




