from bs4 import BeautifulSoup
import logging
import sys
import os


def html_extract(html, out):
    out = open(out, 'w')
    soup = BeautifulSoup(open(html).read(), 'html.parser')
    ol = soup.find('ol', {'id': 'stream-items-id'})
    for li in ol.find_all("li"):
        try:
            item_id = li['data-item-id']
            out.write(item_id + '\n')
        except KeyError:
            logging.info('not a time line item')
    out.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'USAGE: python html_extract.py <input html>'
        print 'this script will extract news_link, image_link, title, sub_title from time twitter html'
    else:
        html = sys.argv[1]
        out = html.replace('.html', '.ids')
        html_extract(html, out)
