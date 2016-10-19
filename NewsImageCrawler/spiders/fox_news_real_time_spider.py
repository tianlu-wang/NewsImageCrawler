import scrapy
import re
import logging
import json
import os

logging.basicConfig(filename='log/fox_news/fox_news_real_time.log',
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='a', level=logging.WARNING)  # TODO: filemode shold ba append
logger = logging.getLogger('fox_news_real_time_log')

categories = ['politics', 'opinion', 'entertainment', 'tech', 'science', 'health', 'travel', 'leisure', 'world']
api = "http://api.foxnews.com/proxy/content/v2?q=content_type:%%28article%%20slideshow%%20listpage%%29%%20AND%%" \
       "20section_path:fnc/%s&sort=date%%20desc&rows=20&fl=taxonomy_path,taxonomy,section,content_type,date," \
       "description,title,url,image_url,export_headline&format=json&api_key=fc2c0a7a-53ed-4f8f-9588-9431485db84b"

api_politics = api % categories[0]
api_opinion = api % categories[1]
api_entertainment = api % categories[2]
api_tech = api % categories[3]
api_science = api % categories[4]
api_health = api % categories[5]
api_travel = api % categories[6]
api_leisure = api % categories[7]
api_world = api % categories[8]

api_sports = "http://api.foxnews.com/proxy/v8/page/module/content/v2/?refName=latest%%20news&isaPath=fnc/sports&" \
            "rows=20&fl=taxonomy_path,taxonomy,section,content_type,date,description,title,url,image_url," \
            "export_headline&format=json&api_key=fc2c0a7a-53ed-4f8f-9588-9431485db84b"
api_business = "http://api.foxnews.com/proxy/section/composite/content/v1/?isaPath=fbn&refName=home-par&format=json&" \
               "fl=taxonomy_path,taxonomy,section,content_type,date,description,title,url,image_url,export_headline&" \
               "format=json&api_key=fc2c0a7a-53ed-4f8f-9588-9431485db84b"
api_us = "http://api.foxnews.com/proxy/content/v2?q=%%28content_type:%%28article%%20slideshow%%20listpage%%29%%20AND%%" \
         "20section_path:fnc/us%%29%%20OR%%20%%28content_type:video%%20AND%%20taxonomy_path:us%%29&sort=date%%" \
         "20desc&rows=20&fl=taxonomy_path,taxonomy,section,content_type,date,description,title,url,image_url," \
         "export_headline&format=json&api_key=fc2c0a7a-53ed-4f8f-9588-9431485db84b"

apis = [api_politics, api_opinion, api_entertainment, api_tech, api_science, api_health, api_travel,
        api_leisure, api_world, api_sports, api_business, api_us]

output_path = "output/fox_news/real_time/"


class fox_news_real_time_Spider(scrapy.Spider):
    name = "fox_news_real_time_spider"

    def start_requests(self):
        for item in apis:
            yield scrapy.Request(url=item, callback=self.parse_json)

    def parse_json(self, response):
        urls = []
        try:
            jsonresponse = json.loads(response.body_as_unicode())
            docs = jsonresponse['response']['docs']
            for item in docs:
                for url in item['url']:
                    urls.append(url[7:])  # get rid of http://
        except:
            logging.error('NOT JSON RESPONSE : ' + response.url)

        for url in urls:
            api = 'http://api.foxnews.com/proxy/content/v2?q=url:http%%5C://%s&format=json&fl=url,subtitle_url,' \
                  'taxonomy_path,taxonomy,section,slides,content_type,title,renditions,description,body,author,' \
                  'headline,date,image_url,list_items,export_headline,source,dateline,commenting,livefyre_config,' \
                  'native_id&api_key=fc2c0a7a-53ed-4f8f-9588-9431485db84b' % url.replace("\n", "")
            yield scrapy.Request(url=api, callback=self.save_json)

    def save_json(self, response):
        m = re.search('http://api\.foxnews\.com/proxy/content/v2\?'
                      'q=url:http%5C://www\.foxnews\.com/.*/\d+/\d+/\d+/(.*)&format.*', response.url)
        jsonresponse = json.loads(response.body_as_unicode())
        if jsonresponse['response']['numFound'] == 0:
            logging.warning('NOT FOUND JSON: ' + response.url)
        else:
            if m:
                if '/' in m.group(1):
                    filename = m.group(1).replace("/", "")
                else:
                    filename = m.group(1)
                filepath = output_path+filename+'.json'
                if os.path.isfile(filepath):  # hope can save some time
                    pass
                else:
                    logging.info("NEW FILE!!!")
                    with open(filepath, 'w') as outfile:
                        json.dump(jsonresponse, outfile)
            else:
                logging.warning("PARSE URL FAILED: " + response.url)





