# -*- coding: utf-8 -*-
import scrapy
import urllib
from scrapytest.lianjia_items import LianjiaItem

try:
  import sys
  reload(sys)
  sys.setdefaultencoding('utf8')
except NameError:
  pass

class LianjiaSpider(scrapy.Spider):
  name="LianjiaSpider"
  #allowed_domains=[""]
  start_urls = []

  def __init__(self, city="bj", crawl_unit="dongcheng", *args, **kwargs):
    super(scrapy.Spider, self).__init__(*args, **kwargs)
    base_url = 'https://%s.lianjia.com/chengjiao/%s/pg' % (city, crawl_unit)
    self.city = city
    self.crawl_unit = crawl_unit
    self.start_urls = []
    for i in range(1,100):
      self.start_urls.append(base_url + str(i) + "/")

  def parse(self,response):
    item = LianjiaItem()
    item['city'] = self.city
    item['crawl_unit'] = self.crawl_unit
    print("****",response.url)
    for box in response.xpath('.//div[@class="leftContent"]/ul[@class="listContent"]/li/a'):
     house_link = box.xpath('.//@href').extract()[0]
     print("house_link:%s" % house_link)
     yield scrapy.Request(house_link,callback=self.parseHousePage,meta=item,dont_filter=False)
  
  def parseHousePage(self,response):
     item = response.meta
     base_info = response.xpath('.//div[@class="introContent"]/div[@class="base"]//li/text()').extract()
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
      if not item['construction_year'].isdigit():
        item['construction_year'] = "0000"
     else:
      print("base_info %s is none" % response.url)
     transaction = response.xpath('.//div[@class="introContent"]/div[@class="transaction"]//li/text()').extract()
     if (len(transaction) > 0):
      item['id'] = transaction[0].strip()
      item['trans_right'] = transaction[1].strip()
      item['list_date'] = transaction[2].strip()
      item['house_property'] = transaction[3].strip()
      item['trans_age'] = transaction[4].strip()
      item['ownership_type'] = transaction[5].strip()
     
     house_title = response.xpath('.//div[@class="house-title"]/div[@class="wrapper"]/h1/text()').extract()[0].strip()
     item['community'] = house_title.split(" ")[0] 
     
     msg = response.xpath('.//div[@class="info fr"]/div[@class="msg"]/span/label/text()')
     item['list_price'] = -1
     item['price_adjustment_times'] = -1
     item['visit_times'] = -1
     item['follow_times'] = -1
     item['view_times'] = -1
     if (len(msg) < 1):
      print("Info no msg for %s" % response.url)
     else:
      try:
        item['list_price'] = float(msg[0].extract())
        item['price_adjustment_times'] = int(msg[2].extract())
        item['visit_times'] = int(msg[3].extract())
        item['follow_times'] = int(msg[4].extract())
        item['view_times'] = int(msg[5].extract())
      except:
        pass

     item['trans_history'] = {}
     i = 0
     for li in response.xpath('.//div[@id="chengjiao_record"]//li'):
      trans_price = li.xpath('./span[@class="record_price"]/text()').extract()[0]
      trans_price = trans_price.strip("万")
      try:
       trans_price = float(trans_price)
      except:
       trans_price = -1
      detail = li.xpath('./p[@class="record_detail"]/text()').extract()[0]
      trans_date = detail.split(",")[-1]
      if len(trans_date) == 7: #2016-05
        trans_date += "-01"
      elif len(trans_date) == 4:
        trans_date += "-01-01"
      elif len(trans_date) != 10:
        print("Error for trans_date %s", trans_date)
        continue
      item['trans_history'][trans_date] = {} 
      item['trans_history'][trans_date]['list_price'] = -1
      item['trans_history'][trans_date]['list_date'] = "1970-01-01"
      item['trans_history'][trans_date]['trans_price'] = trans_price
      item['trans_history'][trans_date]['trans_age'] = ""
      item['trans_history'][trans_date]['price_adjustment_times'] = -1
      item['trans_history'][trans_date]['visit_times'] = -1
      item['trans_history'][trans_date]['follow_times'] = -1
      item['trans_history'][trans_date]['view_times'] = -1
      if (i==0):
       item['trans_history'][trans_date]['list_price'] = item['list_price']
       item['trans_history'][trans_date]['list_date'] = item['list_date']
       item['trans_history'][trans_date]['trans_age'] = item['trans_age']
       item['trans_history'][trans_date]['price_adjustment_times'] = item['price_adjustment_times']
       item['trans_history'][trans_date]['visit_times'] = item['visit_times']
       item['trans_history'][trans_date]['follow_times'] = item['follow_times']
       item['trans_history'][trans_date]['view_times'] = item['view_times']
      i += 1
     
     agent_a = response.xpath('.//div[@class="agent-box"]/div[@class="myAgent"]/div[@class="name"]/a/text()')
     item['district'] = agent_a[0].extract().strip()
     item['business_district'] = agent_a[1].extract().strip()
     return item
