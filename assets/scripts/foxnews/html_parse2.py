from bs4 import BeautifulSoup
import sys
import time
import re
# only for tweet before 2011/06/11
# python assets/scripts/foxnews/html_parse2.py test/test.html


def html_parse2(html, out):
    soup = BeautifulSoup(open(html).read(), 'html.parser')
    for span in soup.find_all('span', attrs={'class', 'js-display-url'}):
        # print span.text + '\n'
        out.write(span.text + '\n')
    for div in soup.find_all('div', attrs={'class', 'js-tweet-text-container'}):
        s = div.find("p").text
        s = s.encode('utf-8', 'ignore')
        m = re.search('.*http://(.*)', s)
        if m:
            out.write(m.group(1) + '\n')
    out.close()

if __name__ == '__main__':
    start_time = time.time()
    if len(sys.argv) != 2:
        print 'USAGE: python html_parse1.py <input html>'
        print 'this script will extract all news links in a html file'
    else:
        html = sys.argv[1]
        out = html.replace('.html', '.links1')
        out = open(out, 'w')
        html_parse2(html, out)
    print("--- %s seconds ---" % (time.time() - start_time))