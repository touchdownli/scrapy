# -*- coding: utf-8 -*-
import scrapy
import urllib
from scrapytest.lianjia_items import LianjiaItem

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class LianjiaSpider(scrapy.Spider):
  name="LianjiaSpider"
  #allowed_domains=[""]
  start_urls = []

  def __init__(self, district="dongcheng", *args, **kwargs):
    super(scrapy.Spider, self).__init__(*args, **kwargs)
    self.district = district 
    self.start_urls = ['https://bj.lianjia.com/chengjiao/%s' % district] 

  def parse(self,response):
    item = LianjiaItem()
    item['district'] = self.district
    #print("****",response.body)
    for box in response.xpath('.//div[@class="leftContent"]/ul[@class="listContent"]/li/a'):
     house_link = box.xpath('.//@href').extract()[0]
     print(house_link)
     yield scrapy.Request(house_link,callback=self.parseHousePage,meta=item)
  
  from decimal import Decimal
  def parseHousePage(self,response):
     item = response.meta
     base_info = response.xpath('.//div[@class="introContent"]/div[@class="base"]//li').extract()
     if (len(base_info) > 0):
      item['layout'] = base_info[0].strip()
      item['floor'] = base_info[1].strip()
      item['total_area'] = base_info[2].strip()
      item['layout_structure'] = base_info[3].strip()
      item['usable_area'] = base_info[4].strip()
      item['build_type'] = base_info[5].strip()
      item['orientation'] = base_info[6].strip()
      item['construction_year'] = base_info[7].strip()
      item['decoration'] = base_info[8].strip()
      item['build_structure'] = base_info[9].strip()
      item['heating_mode'] = base_info[10].strip()
      item['hshold_ladder_ratio'] = base_info[11].strip()
      item['property_right_length'] = base_info[12].strip()
      item['elevator'] = base_info[13].strip()

     transaction = response.xpath('.//div[@class="introContent"]/div[@class="transaction"]//li').extract()
     if (len(transaction) > 0):
      item['id'] = transaction[0]
      item['trans_right'] = transaction[1]
      item['list_date'] = transaction[2]
      item['house_property'] = transaction[3]
      item['trans_age'] = transaction[4]
      item['ownership_type'] = transaction[5]
     
     house_title = response.xpath('.//div[@class="house-title"]//h1/text()').extract().strip()
     item['community'] = house_title.split(" ")[0] 
     
     list_price = response.xpath('.//div[@class="info fr"]/div[@class="msg"]/span/label/text()')[0]
     item['list_price'] = list_price.extract()

     item['trans_history'] = {}
     i = 0
     for li in response.xpath('.//div[@id="chengjiao_record"]//li'):
      price = li.xpath('./span[@class="record_price"]/text()').extract()[0]
      price = price.strip("万")
      try:
       price = Decimal(price)
      except BaseException, e:
       price = -1
      detail = li.xpath('./p[@class="record_detail"]/text()').extract()[0]
      date = detail.split(",")[-1]
      item['trans_history'][date] = {} 
      item['trans_history'][date]['list_price'] = 0
      item['trans_history'][date]['price'] = price
      if (i==0):
       item['trans_history'][date]['list_price'] = item['list_price']
      ++i

     yield item
