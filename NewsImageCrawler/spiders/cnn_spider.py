import scrapy
import re
import logging
from NewsImageCrawler.items import SubWebsiteItem
from datetime import datetime


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
            logging.info("all sub websites")
            logging.info(sub_website['url'])
            if re.match(r'^(http://bleacherreport.com/)', sub_website['url']):
                pass  # do nothing with bleacherreport website
            elif re.match(r'^(http|//)', sub_website['url']):
                yield scrapy.Request(sub_website['url'], callback=self.parse_list)
            else:
                yield scrapy.Request(response.urljoin(sub_website['url']), callback=self.parse_list)

    def parse_list(self, response):
        links = response.xpath('//@href').extract()
        news_list =[]
        for link in links:
            if link.find("index.html") > -1:
                news_list.append(link)
        logging.info("all news links")
        logging.info(news_list)
        for news in news_list:
            if "money.cnn.com" in news:
                yield scrapy.Request(news, callback=self.parse_money)
            elif "www.cnn.com":
                yield scrapy.Request(response.urljoin(news), callback=self.parse_normal)
            else:
                logging.warning("some strange line")
                logging.warning(news)

    def parse_normal(self, response):
        tmp = response.xpath('//p[@class="update-time"]/text()').extract_first()
        print '*******************************'
        print tmp
        tmp = tmp.replace('Updated ', '')
        tmp = tmp.replace(' PM ET,', 'PM')
        tmp = tmp.replace(' AM ET,', 'AM')
        tmp = tmp.replace(', ', ' ')
        tmp = tmp.replace("2016 ", "2016")
        print tmp
        print '*****************************'
        time_update = datetime.strptime(tmp, '%I:%M%p %a %B %d %Y')
        delta = (datetime.now() - time_update).total_seconds()
        if delta < 3600:
            print response.url
            page = response.url.split("/")[7]
            filename = './output/cnn/16/10/%s.html' % page
            with open(filename, 'wb') as f:
                divs = response.xpath('//div[@class="l-container"]')
                for div in divs:
                    tmp = div.xpath('.//h1/text()').extract()
                    if not tmp:
                        pass
                    else:
                        f.write(div.extract())
                        break

    def parse_money(self, response):
        tmp = response.xpath('//span[@class="cnnDateStamp"]/text()').extract_first()
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        print tmp
        tmp = "*" + tmp
        tmp = tmp.replace('* ', '')
        tmp = tmp.replace(', ', ' ')
        tmp = tmp.replace(': ', ' ')
        tmp = tmp.replace(' PM ET ', 'PM')
        tmp = tmp.replace(' AM ET ', 'AM')
        print tmp
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$##'
        time_update = datetime.strptime(tmp, "%B %d %Y %I:%M%p")
        delta = (datetime.now() - time_update).total_seconds()
        if delta < 3600:
            page = response.url.split("/")[8]
            filename = './output/cnn/16/10/%s.html' % page
            with open(filename, 'wb') as f:
                f.write(response.xpath('//main[@class="container js-social-anchor-start"]').extract()[0])


