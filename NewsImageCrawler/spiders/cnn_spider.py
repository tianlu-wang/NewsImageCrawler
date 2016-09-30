import scrapy
from NewsImageCrawler.items import SubWebsiteItem, SubSubWebsiteItem

class CNN_Spider(scrapy.Spider):
    name = "cnn_spider"

    def start_requests(self):
        url = "http://www.cnn.com/"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        sub_websites = []
        for footer_bucket in response.xpath('//li[@class="m-footer__title"]'):
            sub_sub_websites = []
            for footer_item in footer_bucket.xpath('.//li[@class="m-footer__list-item"]'):
                sub_sub_website = SubSubWebsiteItem()
                sub_sub_website['name'] = footer_item.xpath('.//a/text()').extract()
                sub_sub_website['url'] = footer_item.xpath('.//a/@href').extract()
                sub_sub_websites.append(sub_sub_website)
            sub_website = SubWebsiteItem()
            sub_website['name'] = footer_bucket.xpath('.//a[@class="m-footer__title__link"]/text()').extract()
            sub_website['sub_sub_websites'] = sub_sub_websites
            sub_websites.append(sub_website)





