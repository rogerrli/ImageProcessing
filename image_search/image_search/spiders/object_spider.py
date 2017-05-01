from image_search.items import ImageSearchItem
import datetime
import scrapy
from scrapy.selector import Selector

class ObjectSpider(scrapy.Spider):
    name = "openCV-spider"
    start_urls = ["http://buttersafe.com"]


    def parse(self, response):
        sel = Selector(response)
        divs = response.css('div[id="comic"]')
        print("\n\nLOOKHERE\n\n")
        for div in divs:
            img = div.xpath("@src")
            print(img)
        yield ImageSearchItem(file_urls=[img])
        next = response.xpath('//a[contains(@href, "buttersafe")]/@href').extract_first()
        print(next)
        yield scrapy.Request(next, self.parse)