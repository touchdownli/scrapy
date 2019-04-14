# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from scrapy_splash import SplashMiddleware
from scrapy.http import Request, HtmlResponse
from scrapy.selector import Selector
from scrapy_splash import SplashRequest

class SplashTestItem(scrapy.Item):
  name = scrapy.Field()
  zhuli_lr_jinge = scrapy.Field()
  cdd = scrapy.Field()

lua = '''
function main(splash)
    splash.images_enabled = false
    splash:go(splash.args.url)                                                                            
    splash:wait(2)
    js_str = string.format("var a=document.getElementById('PageNav').getElementsByTagName('a');a[%d].click();", splash.args.page_num)
    splash:runjs(js_str)
    splash:wait(2)
    return splash:html()
    end
'''  
class SplashSpider(Spider):
    name = 'scrapy_splash'
    crawl_unit = 'splash'
    url = 'http://data.eastmoney.com/bkzj/hy.html'

    # request需要封装成SplashRequest
    def start_requests(self):
        #抓第一页
        yield SplashRequest(self.url
                            , self.parse
                            , args={'wait': '1','image':0}
                            #, endpoint='execute'
                            )
        # 翻页:从第2页开始,抓第2-5页用range(1,5)
        for i in range(1, 2):
          yield SplashRequest(self.url
                        , self.parse
                        , dont_filter=True
                        , args={'wait': '1','image':0, 'lua_source':lua, 'page_num':i}
                        , endpoint='execute'
                        )
    def parse(self, response):
        item_list = []
        tr = response.xpath('//table[@id="dt_1"]/tbody/tr')
        print("tr size %d" % len(tr))
        for each_tr in tr:
          td_text = each_tr.xpath('./td')
          item = SplashTestItem()
          item['name'] = td_text[1].xpath(".//text()").extract()[0]
          item['zhuli_lr_jinge'] = td_text[4].xpath(".//text()").extract()[0]
          item['cdd'] = td_text[6].xpath(".//text()").extract()[0]
          item_list.append(item)
        return item_list