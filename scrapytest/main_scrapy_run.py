import os
import sys
import time
import urllib.request
from lxml import etree as etree
def wget(city):
  city_base_url = "https://%s.lianjia.com/ershoufang"
  response = urllib.request.urlopen(city_base_url % city)
  html = response.read()
  html_src = etree.HTML(html)
  hrefs = html_src.findall('.//div[@class="position"]//div[@data-role="ershoufang"]//a')
  crawl_units = []
  for href in hrefs:
    crawl_unit = href.get("href").split("/")[-2]
    crawl_units.append(crawl_unit)
  return crawl_units
  
def craw(city, crawl_unit):
  while True:
    os.system("scrapy crawl --logfile=%s.log -L INFO %s -a city=%s -a crawl_unit=%s" % (spider,spider,city,crawl_unit))
    f = open("tmp_continue_crawl_cmd", 'r')
    continue_status = f.readline().strip()
    f.close()
    print("******%s" % continue_status)
    time.sleep(5)
    arr = continue_status.split(":")
    if (len(arr) > 1 and arr[1] == "False"):
      break

if __name__ == '__main__':
  city_crawl_units = {'bj':['dongcheng','xicheng','chaoyang','haidian','fengtai','shijingshan','tongzhou','changping','daxing',
    'yizhuangkaifaqu','shunyi','fangshan','mentougou','pinggu','huairou','miyun','yanqing'],
  'lf':['yanjiao','xianghe'],
  'cd':['jinjiang','qingyang','wuhou','gaoxin7','chenghua','jinniu','tianfuxinqu',
    'gaoxinxi1','shuangliu','wenjiang','pidou','longquanyi','xindou'],
  'cq':['jiangbei','yubei','nanan','banan','shapingba','jiulongpo','yuzhong','dadukou','jiangjing'],
  'sz':['luohuqu','futianqu','nanshanqu','yantianqu','baoanqu','longgangqu',
    'longhuaqu','guangmingxinqu','pingshanqu','dapengxinqu'],
  'nj':['gulou','jianye','qinhuai','xuanwu','yuhuatai','qixia','jiangning','pukou','liuhe','lishui','gaochun'],
  'hz':['xihu','xiacheng','jianggan','gongshu','shangcheng','binjiang','yuhang','xiaoshan','xiasha'],
  'gz':['tianhe','yuexiu','liwan','haizhu','panyu','baiyun','huangpugz','conghua','zengcheng','huadou','nansha'],
  'xa':['beilin','weiyang','baqiao','xinchengqu','lintong','yanliang','changan4','lianhu','yanta','lantian','huxian','zhouzhi','gaoling1','xixianxinqu']}
  spiders = ['LianjiaSpider','SecondHandSaleLianjiaSpider']
  focus_cities = ['bj','lf','cd','nj','sz','hz','gz','xa']
  other_cities = ['wh','xm','zh','tj','zz','jn','dl','qd','cq']
  total_cities = focus_cities + other_cities
  city_map = {"total":total_cities,"focus":focus_cities,"other":other_cities}
  city_group = total_cities
  if len(sys.argv) == 1:
    print("Usage:python main_scrapy_run.py [total|'city' [trans|second]]")
    exit(0)
  if (len(sys.argv) > 1 and sys.argv[1] != 'total'):
    city_group = [sys.argv[1]]
  if (len(sys.argv) > 2):
    if (sys.argv[2] == "trans"):
      spiders = ['LianjiaSpider']
    elif (sys.argv[2] == "second"):
      spiders = ['SecondHandSaleLianjiaSpider']
  if not city_group:
    print("city_group param error %s" % sys.argv[1])
    exit(0)
  for city in city_group:
    if city in city_crawl_units:
      crawl_units = city_crawl_units[city]
    else:
      crawl_units = wget(city)
    for spider in spiders:
      for crawl_unit in crawl_units:
        craw(city, crawl_unit)
