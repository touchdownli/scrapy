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

from datetime import datetime
import time
import json
import logging

class LianjiaSpider(scrapy.Spider):
  name="LianjiaSpider"
  #allowed_domains=[""]
  start_urls = []
  crawled_urls = {}
  base_url_pattern = 'https://%s.lianjia.com/chengjiao/%s/pg'
  base_url = ""
  crawled_urls_txt_name = "%s_%s_crawled_urls.txt"
  crawl_url_xpath = './/div[@class="leftContent"]/ul[@class="listContent"]/li'
  
  base_info_name_2_item_name = {
  '链家编号':'id',
  '房屋户型':'layout',
  '所在楼层':'floor',
  '建筑面积':'total_area',
  '户型结构':'layout_structure',
  '套内面积':'usable_area',
  '建筑类型':'build_type',
  '房屋朝向':'orientation',
  '建筑年代':'construction_year',
  '装修情况':'decoration',
  '建筑结构':'build_structure',
  '供暖方式':'heating_mode',
  '梯户比例':'hshold_ladder_ratio',
  '产权年限':'property_right_length',
  '配备电梯':'elevator',
  '用水类型':'water_type',
  '用电类型':'electric_type',
  '燃气价格':'gas_price',
  '交易权属':'trans_right',
  '挂牌时间':'list_date',
  '房屋用途':'house_property',
  '上次交易':'last_trans_date',
  '房屋年限':'trans_age',
  '房权所属':'ownership_type',
  '产权所属':'ownership_type',
  '抵押信息':'mortgage',
  '房本备件':'certicate'
  }

  def __init__(self, city="bj", crawl_unit="dongcheng", *args, **kwargs):
    super(scrapy.Spider, self).__init__(*args, **kwargs)
    self.base_url = self.base_url_pattern % (city, crawl_unit)
    self.city = city
    self.crawl_unit = crawl_unit
    self.start_urls = [self.base_url + "1/"]
    self.file = open(self.crawled_urls_txt_name % (crawl_unit,city), "a+")
    self.file.seek(0)
    for x in self.file.readlines():
      cols = x.strip().split(" ")
      if (len(cols) > 1):
        self.crawled_urls[cols[0]] = cols[1:]
      else:
        self.crawled_urls[cols[0]] = []
    print("crawled_urls size:%d" % len(self.crawled_urls))
    #raise Exception("stop")
  
  def closed(self, reason):
    self.file.close()
  
  def isCrawled(self, link, item):
    if link in self.crawled_urls:
      if len(self.crawled_urls[link]) > 0:
        if item['trans_date'] <= self.crawled_urls[link][0]:
          return True
      else:
        return True
    return False
  
  def parse(self, response):
    ex = response.xpath('.//div[@class="leftContent"]//div[@class="page-box fr"]/div[@class="page-box house-lst-page-box"]/@page-data').extract()
    page_data = json.loads(ex[0])
    totalPage = page_data['totalPage']
    for i in range(1,totalPage + 1):
      pg_link = self.base_url + str(i) + "/"
      yield scrapy.Request(pg_link,callback=self.parseHouseList)
      
  def parseHouseList(self,response):
    item = LianjiaItem()
    item['city'] = self.city
    item['crawl_unit'] = self.crawl_unit
    print("****",response.url)
    for box in response.xpath(self.crawl_url_xpath):
     house_link = box.xpath('.//a/@href').extract()[0]
     print("house_link:%s" % house_link)
     current_trans_date = box.xpath('.//div[@class="dealDate"]/text()').extract()[0]
     try:
      current_trans_date = time.strftime("%Y-%m-%d",time.strptime(current_trans_date,'%Y.%m.%d'))
     except:
      try:
        current_trans_date = time.strftime("%Y-%m-%d",time.strptime(current_trans_date,'%Y.%m'))
      except:
        current_trans_date = datetime.now().strftime('%Y-%m-%d')
     item['trans_date'] = current_trans_date
     
     is_crawled_success = self.isCrawled(house_link, item)
     if not is_crawled_success:
      yield scrapy.Request(house_link,callback=self.parseHousePage,meta=item,dont_filter=True)
     else:
      print("%s in crawled_urls" % house_link)
  
  def extractBaseInfo(self,response):
    item = response.meta
    
    for field in self.base_info_name_2_item_name.values():
      item[field] = ""
      
    base_infos = response.xpath('.//div[@class="introContent"]/div[@class="base"]//li')
    for li in base_infos:
      span = li.xpath('./span/text()').extract()[0].strip()
      if (span in self.base_info_name_2_item_name):
        text = li.xpath('./text()')
        if len(text) > 0:
          item[self.base_info_name_2_item_name[span]] = text.extract()[0].strip()
      else:
        logging.error("base_info field %s not in:%s" % (span,response.url))
        return False
          
    transaction = response.xpath('.//div[@class="introContent"]/div[@class="transaction"]//li')
    for li in transaction:
      spans = li.xpath('./span/text()').extract()
      span = spans[0].strip()
      if (span in self.base_info_name_2_item_name):
        text = li.xpath('./text()')
        if len(text) > 0:
          item[self.base_info_name_2_item_name[span]] = text.extract()[0].strip()
        elif len(spans) == 2:
          item[self.base_info_name_2_item_name[span]] = spans[1].strip()
      else:
        logging.error("base_info field %s not in:%s" % (span,response.url))
        return False

    return True
    
  def parseHousePage(self,response):
     if not self.extractBaseInfo(response)
        return
     
     house_title = response.xpath('.//div[@class="house-title"]/div[@class="wrapper"]')
     item['community'] = house_title.xpath('./h1/text()').extract()[0].strip().split(" ")[0]
     current_trans_date = house_title.xpath('./span/text()').extract()[0].strip().split(" ")[0]
     try:
      current_trans_date = time.strftime("%Y-%m-%d",time.strptime(current_trans_date,'%Y.%m.%d'))
     except:
      try:
        current_trans_date = time.strftime("%Y-%m-%d",time.strptime(current_trans_date,'%Y.%m'))
      except:
        current_trans_date = datetime.now().strftime('%Y-%m-%d')
     item['trans_date'] = current_trans_date
     if self.isCrawled(response.url, item):
      return
     
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
     
     self.crawled_urls[response.url] = [current_trans_date]
     self.file.write(" ".join([response.url, current_trans_date]) + "\n")
     return item

class SecondHandSaleLianjiaSpider(LianjiaSpider):
  name="SecondHandSaleLianjiaSpider"
  #bj.lianjia.com/ershoufang/chaoyang/
  base_url_pattern = 'https://%s.lianjia.com/ershoufang/%s/pg'
  crawled_urls_txt_name = "%s_%s_second_house_sale_crawled_urls.txt"
  crawl_url_xpath = './/div[@class="leftContent"]/ul[@class="sellListContent"]/li'
  def isCrawled(self, link, item):
    if link in self.crawled_urls:
      if item['list_price'] == self.crawled_urls[link][0]:
        return True
    return False
    
  def parseHouseList(self,response):
    item = LianjiaItem()
    item['city'] = self.city
    item['crawl_unit'] = self.crawl_unit
    item['crawl_date'] = datetime.now().strftime('%Y-%m-%d')
    print("****",response.url)
    for box in response.xpath(self.crawl_url_xpath):
     house_link = box.xpath('.//a/@href').extract()[0]
     print("house_link:%s" % house_link)
     item['id'] = house_link[house_link.rfind("/")+1:].split(".")[0]
     item['list_price'] = box.xpath('.//div[@class="totalPrice"]/span/text()').extract()[0]
     is_crawled_success = self.isCrawled(house_link, item)
     if not is_crawled_success:
      yield scrapy.Request(house_link,callback=self.parseHousePage,meta=item,dont_filter=True)
     else:
      print("%s in crawled_urls" % house_link)
  def parseHousePage(self,response):
     if not self.extractBaseInfo(response)
        return
     
     construction_year = response.xpath('.//div[@class="overview"]//div[@class="houseInfo"]/\
     div[@class="area"]/div[@class="subInfo"]/text()').extract()
     item['construction_year'] = construction_year[0].split("年")[0]
     if not item['construction_year'].isdigit():
        item['construction_year'] = "0000"
     
     list_price = response.xpath('.//div[@class="overview"]/div[@class="content"]/div[@class="price "]/span/text()').extract()
     item['list_price'] = list_price[0]
     
     transaction = response.xpath('.//div[@class="introContent"]/div[@class="transaction"]//ul/li')
     i = -1
     colnames = ['list_date','trans_right','last_trans_date','house_property',
     'trans_age','ownership_type','mortgage','certicate']
     for li in transaction:
       i += 1
       if i == 6:
        item[colnames[i]] = li.xpath('./span/text()').extract()[1].strip()
        continue
       text = li.xpath('./text()').extract()
       if len(text) < 1:
        text = [""]
       item[colnames[i]] = text[0].strip()
     
     community = response.xpath('.//div[@class="overview"]/div[@class="content"]//div[@class="communityName"]/a/text()').extract()[0].strip()
     item['community'] = community
     
     area = response.xpath('.//div[@class="overview"]/div[@class="content"]//\
     div[@class="areaName"]/span[@class="info"]/a/text()').extract()
     item['business_district'] = area[1].strip()
     item['district'] = area[0].strip()
     
     title_wrapper = response.xpath('.//div[@class="title-wrapper"]')
     follow_times = title_wrapper.xpath('.//span[@id="favCount"]/text()').extract()[0]
     item['follow_times'] = follow_times
     visit_times = title_wrapper.xpath('.//span[@id="cartCount"]/text()').extract()[0]
     item['visit_times'] = visit_times
     
     self.crawled_urls[response.url] = [item['list_price'],item['list_date']]
     self.file.write(" ".join([response.url,item['list_price'],item['list_date']]) + "\n")
     return item