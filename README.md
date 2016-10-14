# newsbot
Newsworthy Situation Dataset

#cnn
Now the data I crawled is in HTML format, I can parse it so that I can get the text and image. But there are 3 problems:

1. some news has more than one image and some have none 
2. some news has swf flash rather than image
3. in this way, I can only crawl about 20,000 news(from the twitter)

I did find the api to get JSON data http://compositor.api.cnn.com/svc/mcs/v3/docs/h_04c706ccc154122307ee98e4fb0a82a2, however, I can't find any relation bewteen the NAME of the news and the ID in the url(h_04c706ccc154122307ee98e4fb0a82a2), which means I can't access the archived data.

For the real time spider, usually get around 90 news every day, also in html format. But I can change it into JSON by using this API:
http://compositor.api.cnn.com/svc/mcs/v3/composites/sections/cnn/health/rows:15/start:0 It would provide no more than 100(that should be rows:100/start:0) latest news.




