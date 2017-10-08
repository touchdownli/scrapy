import os
import time

if __name__ == '__main__':
  #crawl_units = ['yizhuangkaifaqu','shunyi','fangshan','mentougou','pinggu','huairou','miyun','yanqing']
  crawl_units = ['yanjiao','xianghe']
  for crawl_unit in crawl_units:
    while True:
      os.system("scrapy crawl LianjiaSpider -a city=lf -a crawl_unit=%s" % crawl_unit)
      continue_status = open("tmp_continue_crawl_cmd", 'r').readline().strip()
      print("******%s" % continue_status)
      time.sleep(5)
      arr = continue_status.split(":")
      if (len(arr) > 1 and arr[1] == "False"):
        break
      