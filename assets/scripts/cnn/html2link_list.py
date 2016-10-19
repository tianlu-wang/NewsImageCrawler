from bs4 import BeautifulSoup
import sys
import os


def html2link_list(html, out):
    soup = BeautifulSoup(open(html).read(), 'html.parser')
    for span in soup.find_all('span', attrs={'class', 'js-display-url'}):
        # print span.text
        if 'cnn' in span.text or 'CNN' in span.text:
            out.write(span.text + '\n')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'USAGE: python html2link_list.py <input html> <output file>'
        print 'this script will extract all cnn news links in a html file'
    else:
        html = sys.argv[1]
        out = sys.argv[2]
        out = html.replace('htmls', 'link_list')
        out = out.replace('html', 'list')
        out = open(out, 'w')
        html2link_list(html, out)