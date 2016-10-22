import logging
import time
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

logging.basicConfig(filename='log/twitter/twitter.log', format='%(asctime)s %(levelname)s %(message)s',
                    filemode='a', level=logging.WARNING)  # TODO: change filemode
logger = logging.getLogger('twitter_log')


def download_twitter(website, start_date, end_date):
    logging.info("WEBSITE : " + website)
    logging.info("START TIME: " + start_date)
    logging.info("end_date: " + end_date)
    api = "https://twitter.com/search?f=tweets&vertical=default&q=" \
               "from%%3A%s%%20since%%3A%s%%20until%%3A%s&src=typd" % (website, start_date, end_date)
    driver = webdriver.Chrome(executable_path='/home/tianlu/driver/chromedriver')
    driver.get(api)
    pre_resource = driver.page_source
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        if pre_resource == driver.page_source:
            break
        else:
            pre_resource = driver.page_source
    out = open('assets/twitter/' + website + '-' + start_date + '-' + end_date + '.html', 'w')
    out.write(driver.page_source.encode('utf-8', 'ignore'))
    out.close()

if __name__ == '__main__':
    start_time = time.time()
    if len(sys.argv) != 4:
        print 'USAGE: python download_twitter.py <website> <start_date> <end_date>'
        print 'get all tweets'
    else:
        website = sys.argv[1]
        start_date = sys.argv[2]
        end_date = sys.argv[3]
        download_twitter(website, start_date, end_date)
    print("--- %s seconds ---" % (time.time() - start_time))



