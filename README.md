# newsbot
Newsworthy Situation Dataset

#cnn
Now the data I crawled is in HTML format, I can parse it so that I can get the text and image. But there are 3 problems:

1. some news has more than one image and some have none 
2. some news has swf flash rather than image
3. in this way, I can only crawl about 20,000 news(from the twitter)

I did find the api to get JSON data, however, I can only

For the real time spider, usually get around 90 news every day, also in html format. But I can change it into JSON by using this API:
http://compositor.api.cnn.com/svc/mcs/v3/composites/sections/cnn/health/rows:15/start:0




