from bs4 import BeautifulSoup
import sys


# python assets/scripts/foxnews/html_parse1.py test/test.html

def html_parse1(html, out):
    soup = BeautifulSoup(open(html).read(), 'html.parser')
    for span in soup.find_all('span', attrs={'class', 'js-display-url'}):
        out.write(span.text + '\n')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'USAGE: python html_parse1.py <input html>'
        print 'this script will extract all news links in a html file'
    else:
        html = sys.argv[1]
        out = html.replace('.html', '.links1')
        # out = out.replace('html', 'list')
        out = open(out, 'w')
        html_parse1(html, out)