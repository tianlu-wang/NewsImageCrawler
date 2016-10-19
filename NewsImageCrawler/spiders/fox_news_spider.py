import scrapy
import re
import logging
import json

logging.basicConfig(filename='log/fox_news/fox_news.log', filemode='w', level=logging.WARNING)  # TODO: change filemode
logger = logging.getLogger('fox_news_log')

links = 'test/test.links2'  # TODO


class fox_news_Spider(scrapy.Spider):
    name = "fox_news_spider"

    def start_requests(self):
        with open(links) as f:
            contents = f.readlines()
        for item in contents:
            api = 'http://api.foxnews.com/proxy/content/v2?q=url:http%%5C://%s&format=json&fl=url,subtitle_url,' \
                  'taxonomy_path,taxonomy,section,slides,content_type,title,renditions,description,body,author,' \
                  'headline,date,image_url,list_items,export_headline,source,dateline,commenting,livefyre_config,' \
                  'native_id&api_key=fc2c0a7a-53ed-4f8f-9588-9431485db84b' % item.replace("\n", "")
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
                with open('test/'+filename+'.json', 'w') as outfile:
                    json.dump(jsonresponse, outfile)
            else:
                logging.warning("PARSE URL FAILED: " + response.url)




