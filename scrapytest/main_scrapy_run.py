import os
import time

if __name__ == '__main__':
  city_crawl_units = {'bj':['dongcheng','xicheng','chaoyang','haidian','fengtai','shijingshan','tongzhou','changping','daxing',
  'yizhuangkaifaqu','shunyi','fangshan','mentougou','pinggu','huairou','miyun','yanqing'],
  'lf':['yanjiao','xianghe']}
  #city_crawl_units = {'bj':['yizhuangkaifaqu','mentougou','huairou','yanqing'],'lf':['yanjiao','xianghe']}
  spiders = ['LianjiaSpider','SecondHandSaleLianjiaSpider']
  for spider in spiders:
    for city,crawl_units in city_crawl_units.items():
      for crawl_unit in crawl_units:
        while True:
          os.system("scrapy crawl %s -a city=%s -a crawl_unit=%s" % (spider,city,crawl_unit))
          continue_status = open("tmp_continue_crawl_cmd", 'r').readline().strip()
          print("******%s" % continue_status)
          time.sleep(5)
          arr = continue_status.split(":")
          if (len(arr) > 1 and arr[1] == "False"):
            break
      