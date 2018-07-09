import scrapy
import json
import requests

    
class StocksySpider(scrapy.Spider):
    name = "stocksy"
    url_main_part = "https://www.stocksy.com/search/query?format"
    url_filters = "=json&filters={\
    %%22text%%22:%%22%s+pet+-wild+-wildlife+-%s+-people+-women+-child+-girl+-boy+-face+-female+-men%%22,\
    %%22modelreleaseCount%%22:[%%220%%22],%%22searchAccess%%22:%%22public%%22,\
    %%22assetType%%22:[%%22photo_creative%%22],%%22anonymousPeople%%22:%%22false%%22}"
    url_last_part = "&%%22sort%%22=%%22popular%%22&pageSize=%d"
    
    url = url_main_part + url_filters + url_last_part
    tag = "cat"
    tag2 = "dog"
    count_per_class = 1400
    image_count = 1
    start_urls = [
        url % (tag, tag2, count_per_class)
    ]
    
     
    def parse(self, response):
        response = json.loads(response.body_as_unicode())['response']
        for i in range(response['returnedItemCount']):
            path = response['items'][i]['variations']['jpgFixedWidthDouble']['url']
            image = requests.get(path)
            with open('images/'+self.tag+'_no_people/'+ '{t}_{i}.jpg'.format(t=self.tag, i=self.image_count), 'wb') as img:
                img.write(image.content)
            self.image_count+=1
            yield {
                'image': path
            }
        if self.image_count>self.count_per_class:
            if self.tag=='cat':
                self.tag = 'dog'
                self.tag2 = 'cat'
                self.image_count = 1
                next_page = self.url % (self.tag, self.tag2, self.count_per_class)
                try:
                    yield scrapy.Request(next_page, self.parse)
                except:
                    pass