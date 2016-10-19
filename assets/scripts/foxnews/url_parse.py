import sys
import urllib2
import re
import logging
# python assets/scripts/foxnews/url_parse.py test/test.links1

logging.basicConfig(filename='log/fox_news/fox_news_url_parse.log', filemode='w', level=logging.INFO)  # TODO: change filemode
logger = logging.getLogger('fox_news_log')


def url_parse(links1):
    links2 = links1.replace('.links1', '.links2')
    out = open(links2, 'w')
    with open(links1) as f:
        contents = f.readlines()
    for item in contents:
        url = "http://" + item.replace("\n", "")
        try:
            response = urllib2.urlopen(url)
            url = response.url
            m = re.search('^http://www\.foxnews\.com/.*/\d+/\d+/\d+/.*\?.*', url)
            if m:
                index = url.index('?')
                url = url[7: index]  # get rid of 'http://'
                out.write(url + '\n')
            else:
                logging.warning('Non foxnews url: ' + url)
        except urllib2.HTTPError:
            logging.error("Can not find this url: " + url)
    out.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'USAGE: python html_parse1.py <input html>'
        print 'this script reads tmp link from .links1 and save real news link in .links2'
    else:
        links1 = sys.argv[1]
        url_parse(links1)