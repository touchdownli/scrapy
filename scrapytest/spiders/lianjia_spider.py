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

from datetime import datetime,timedelta
import time
import json
import logging
import re

class LianjiaSpider(scrapy.Spider):
  name="LianjiaSpider"
  #allowed_domains=[""]
  start_urls = []
  crawled_urls = {}
  base_url_pattern = 'https://%s.ke.com/chengjiao/%s/pg'
  base_url = ""
  crawled_urls_txt_name = "%s_%s_crawled_urls.txt"
  crawl_url_xpath = './/div[@class="leftContent"]//ul[@class="listContent"]/li'
  
  base_info_name_2_item_name = {
  '链家编号':'id',
  '房屋户型':'layout',
  '所在楼层':'floor',
  '建筑面积':'total_area',
  '户型结构':'layout_structure',
  '套内面积':'usable_area',
  '建筑类型':'build_type',
  '别墅类型':'build_type',
  '房屋朝向':'orientation',
  '建筑年代':'construction_year',
  '建成年代':'construction_year',
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
    #logging.basicConfig(format="%(asctime)s %(name)s %(funcName)s:%(lineno)d %(levelname)s %(message)s")
    self.base_url = self.base_url_pattern % (city, crawl_unit)
    self.city = city
    self.crawl_unit = crawl_unit
    self.start_urls = [self.base_url + "1/"]
    self.file = open(self.crawled_urls_txt_name % (crawl_unit,city), "a+")
    self.file.seek(0)
    
    self.total_pages_ = 0
    self.page_index_ = 0
    
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
        now_trans_date = datetime.strptime(item['trans_date'],'%Y-%m-%d')
        crawled_trans_date = datetime.strptime(self.crawled_urls[link][0],'%Y-%m-%d')
        diff = now_trans_date - crawled_trans_date
        if diff.days < 30:
          return True
      else:
        return False
    return False
  
  def parse(self, response):
    ex = response.xpath('.//div[@class="leftContent"]//div[@class="page-box fr"]/div[@class="page-box house-lst-page-box"]/@page-data').extract()
    totalPage = 1
    try:
      page_data = json.loads(ex[0])
      totalPage = page_data['totalPage']
    except:
      pass
    
    self.total_pages_ = totalPage
    self.page_index_ = 1
    for i in range(1,1 + 1):
      pg_link = self.base_url + str(i) + "/"
      yield scrapy.Request(pg_link,callback=self.parseHouseList)
      
  def parseHouseList(self,response):
    item = LianjiaItem()
    item['city'] = self.city
    item['crawl_unit'] = self.crawl_unit
    print("****",response.url)
    now_date = datetime.now()
    min_date = now_date
    for box in response.xpath(self.crawl_url_xpath):
     house_link = box.xpath('.//a/@href').extract()[0]
     print("parseHouseList:%s" % house_link)
     community = box.xpath('.//a/text()').extract()[0].strip().split(" ")[0]
     current_trans_date = box.xpath('.//div[@class="dealDate"]/text()').extract()[0].strip("\"").strip()
     try:
      current_trans_date = datetime.strptime(current_trans_date,'%Y.%m.%d')
     except:
      try:
        current_trans_date = datetime.strptime(current_trans_date,'%Y.%m')
      except:
        current_trans_date = now_date
     
     if min_date > current_trans_date:
      min_date = current_trans_date
      
     item['trans_date'] = datetime.strftime(current_trans_date, '%Y-%m-%d')
     item['community'] = community
     is_crawled_success = self.isCrawled(house_link, item)
     if not is_crawled_success:
      yield scrapy.Request(house_link,callback=self.parseHousePage,meta=item,dont_filter=True)
     else:
      print("%s in crawled_urls" % house_link)
    if now_date - min_date < timedelta(days=60):
      self.page_index_ += 1
      if (self.page_index_ <= self.total_pages_):
        pg_link = self.base_url + str(self.page_index_) + "/"
        print("%s crawl house list" % pg_link)
        yield scrapy.Request(pg_link,callback=self.parseHouseList)
      
  def extractBaseInfo(self,response):
    item = response.meta
    for field in self.base_info_name_2_item_name.values():
      item[field] = ""
      
    house_link = response.url
    item['id'] = house_link[house_link.rfind("/")+1:].split(".")[0]
    
    base_infos = response.xpath('.//div[@class="introContent"]/div[@class="base"]//li')
    for li in base_infos:
      span = li.xpath('./span/text()').extract()[0].strip()
      if (span in self.base_info_name_2_item_name):
        text = li.xpath('./text()')
        if len(text) > 0:
          item[self.base_info_name_2_item_name[span]] = text.extract()[0].strip()
      else:
        logging.warn("base_info field %s not in:%s" % (span,response.url))
        #return False
          
    transaction = response.xpath('.//div[@class="introContent"]/div[@class="transaction"]//li')
    for li in transaction:
      spans = li.xpath('./span/text()').extract()
      span = spans[0].strip()
      if (span in self.base_info_name_2_item_name):
        text = li.xpath('./text()')
        if len(spans) == 2:
          item[self.base_info_name_2_item_name[span]] = spans[1].strip()
        elif len(text) > 0:
          item[self.base_info_name_2_item_name[span]] = text.extract()[0].strip()
      else:
        logging.error("base_info field %s not in defined fields:%s" % (span,response.url))

    #value type confirm
    if not item['construction_year'].isdigit():
      item['construction_year'] = '0000'
    
    try:
      time.strptime(item['last_trans_date'],'%Y-%m-%d')
    except:
      item['last_trans_date'] = '1970-01-01'
    return True
    
  def parseHousePage(self,response):
     if not self.extractBaseInfo(response):
        return
     item = response.meta
     '''
     house_title = response.xpath('.//div[@class="house-title"]/')
     community = house_title.extract()
     print("com:%s" % community)
     item['community'] = community[0].strip().split(" ")[0]
     
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
    '''
     current_trans_date = item['trans_date']

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
      trans_date = detail.split(",")[-1].strip()
      if len(trans_date) == 7: #2016-05
        trans_date += "-01"
      elif len(trans_date) == 4:
        trans_date += "-01-01"
      elif len(trans_date) != 10:
        print("Error for trans_date %s" % trans_date)
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
       try:
        time.strptime(item['list_date'],'%Y-%m-%d')
       except:
        item['list_date'] = "1970-01-01"
       current_trans_date = trans_date
       item['trans_history'][trans_date]['list_date'] = item['list_date']
       item['trans_history'][trans_date]['trans_age'] = item['trans_age']
       item['trans_history'][trans_date]['price_adjustment_times'] = item['price_adjustment_times']
       item['trans_history'][trans_date]['visit_times'] = item['visit_times']
       item['trans_history'][trans_date]['follow_times'] = item['follow_times']
       item['trans_history'][trans_date]['view_times'] = item['view_times']
      i += 1
     
     agent_a = response.xpath('.//div[@class="agent-box"]/div[@class="myAgent"]/div[@class="name"]/a/text()')
     try:
      item['district'] = agent_a[0].extract().strip()
     except:
      pass
     try:
      item['business_district'] = agent_a[1].extract().strip()
     except:
      pass
     
     self.crawled_urls[response.url] = [current_trans_date]
     self.file.write(" ".join([response.url, current_trans_date]) + "\n")
     return item

class SecondHandSaleLianjiaSpider(LianjiaSpider):
  name="SecondHandSaleLianjiaSpider"
  #bj.lianjia.com/ershoufang/chaoyang/
  base_url_pattern = 'https://%s.ke.com/ershoufang/%s/pg'
  crawled_urls_txt_name = "%s_%s_second_house_sale_crawled_urls.txt"
  crawl_url_xpath = './/div[@class="leftContent"]/ul[@class="sellListContent"]//li[@class="clear"]'
  re_visit_times = re.compile(r'(\d+)次带看')
  def isCrawled(self, link, item):
    if link in self.crawled_urls:
      if item['list_price'] == self.crawled_urls[link][0]:
        if not item['visit_times'] or (len(self.crawled_urls[link]) > 2 and item['visit_times'] == self.crawled_urls[link][2]):
          return True
    return False
    
  def parseHouseList(self,response):
    item = LianjiaItem()
    item['city'] = self.city
    item['crawl_unit'] = self.crawl_unit
    item['crawl_date'] = datetime.now().strftime('%Y-%m-%d')
    #logging.info(response.text)
    url_boxs = response.xpath(self.crawl_url_xpath)
    print("response:%s,url cnt:%d" % (response.url,len(url_boxs)))
    for box in url_boxs:
     house_link = box.xpath('.//a/@href').extract()[0]
     print("parseHouseList:%s" % house_link)
     #item['list_price'] = box.xpath('.//div[@class="followInfo"]//div[@class="totalPrice"]/span/text()').extract()[0]
     item['list_price'] = box.xpath('.//div[@class="priceInfo"]//div[@class="totalPrice"]/span/text()').extract()[0]
     reg_ret = self.re_visit_times.search(box.xpath('.//div[@class="followInfo"]/text()').extract()[0])
     if reg_ret:
      item['visit_times'] = reg_ret.group(1)
     else:
      item['visit_times'] = None
     is_crawled_success = self.isCrawled(house_link, item)
     if not is_crawled_success:
      yield scrapy.Request(house_link,callback=self.parseHousePage,meta=item,dont_filter=True)
     else:
      print("%s in crawled_urls" % house_link)
    if self.page_index_ < 50:
      self.page_index_ += 1
      if (self.page_index_ <= self.total_pages_):
        pg_link = self.base_url + str(self.page_index_) + "/"
        print("request:%s" % pg_link)
        yield scrapy.Request(pg_link,callback=self.parseHouseList)
        
  def parseHousePage(self,response):
     if not self.extractBaseInfo(response):
        return
     
     item = response.meta

     construction_year = response.xpath('.//div[@class="overview"]//div[@class="houseInfo"]/\
     div[@class="area"]/div[@class="subInfo"]/text()').extract()
     item['construction_year'] = "0000"
     try:
      item['construction_year'] = construction_year[0].split("年")[0]
     except:
      pass
     if not item['construction_year'].isdigit():
        item['construction_year'] = "0000"
     
     list_price = response.xpath('.//div[@class="overview"]/div[@class="content"]/div[@class="price "]/span/text()').extract()
     item['list_price'] = list_price[0]
     
     community = response.xpath('.//div[@class="overview"]/div[@class="content"]//div[@class="communityName"]/a/text()').extract()[0].strip()
     item['community'] = community
     
     area = response.xpath('.//div[@class="overview"]/div[@class="content"]//\
     div[@class="areaName"]/span[@class="info"]/a/text()').extract()
     #area = response.xpath('.//div[@class="myAgent"]/div[@class="name"]/a/text()').extract()
     item['business_district'] = area[1].strip()
     item['district'] = area[0].strip()
     
     title_wrapper = response.xpath('.//div[@class="title-wrapper"]')
     follow_times = title_wrapper.xpath('.//span[@id="favCount"]/text()').extract()[0]
     item['follow_times'] = follow_times
     try:
      visit_times = title_wrapper.xpath('.//span[@id="cartCount"]/text()').extract()[0]
      item['visit_times'] = visit_times
     except:
      pass
     
     self.crawled_urls[response.url] = [item['list_price'],item['list_date'],item['visit_times']]
     self.file.write(" ".join([response.url,item['list_price'],item['list_date'],item['visit_times']]) + "\n")
     return item