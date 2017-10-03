# -*- coding: utf-8 -*-
import scrapy
import urllib
from scrapytest.JobItems import JobItem
class Jobspider(scrapy.Spider):
  name="Jobspider"
  #allowed_domains=["www.51job.com"]
  start_urls=[]

  def __init__(self, city="beijing", *args, **kwargs):
    super(scrapy.Spider, self).__init__(*args, **kwargs)
    self.city=city
    base_url = 'http://jobs.51job.com/%s/p' % city
    for x in range(2,5001):
      page = base_url+str(x)
      self.start_urls.append(page)
  def parse(self,response):
    #print(response)
    item=JobItem()
    item['city']=self.city
    #print("****",response.body)
    for box in response.xpath('.//div[@class="mcon"]//div[@class="e"]'):
     #print (box.xpath('.//div[@class="e"]/p[1]/span[1]')) 
     #获取职业名称     
     #item['job_title'] = box.xpath('./p[1]/span[1]/a')[0].xpath('string(.)').extract()[0]
     jt = box.xpath('./p[@class="info"]/span[@class="title"]/a[1]/text()').extract()
     if (len(jt) > 0):
      item['job_title'] = jt[0]
     #获取公司名称
     cn = box.xpath('./p[@class="info"]/a[@class="name"]/text()').extract()
     if (len(cn) > 0):
      item['company_name']=cn[0]
     #获取工作地点
     ln = box.xpath('./p[@class="info"]/span[@class="location name"]/text()').extract()
     if (len(ln) > 0):
      item['location_name']=ln[0]
     # 获取薪水范围
     sr = box.xpath('./p[@class="info"]/span[@class="location"]/text()').extract()
     if (len(sr) > 0):
      item['salary_range']=sr[0] 
     # 获取学历要求
     sl = box.xpath('./p[@class="order"]/text()[1]').extract()
     if (len(sl) > 0):
      item['school_level']=sl[0]
     # 获取工作经验
     ey = box.xpath('./p[@class="order"]/text()[2]').extract()
     if (len(ey) > 0):
      item['experience_year']=ey[0]
     # 获取公司性质
     cf = box.xpath('./p[@class="order"]/text()[3]').extract()
     if (len(cf) > 0):
      item['company_feature']=cf[0]
     # 获取公司规模
     cs = box.xpath('./p[@class="order"]/text()[4]').extract()
     if (len(cs) > 0):
      item['company_size']=cs[0]
     # 获取工作描述
     jd = box.xpath('./p[@class="text"]/text()').extract()
     if (len(jd) > 0):
      item['job_desc'] = jd[0].strip()
     yield item
