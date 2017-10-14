import os
import time

if __name__ == '__main__':
  crawl_units = {'bj':['dongcheng','xicheng','haidian','fengtai','shijingshan','tongzhou','changping','daxing',
  'yizhuangkaifaqu','shunyi','fangshan','mentougou','pinggu','huairou','miyun','yanqing'],
  'lf':['yanjiao','xianghe']}
  for city,crawl_units in crawl_units.items():
    for crawl_unit in crawl_units:
      while True:
        os.system("scrapy crawl LianjiaSpider -a city=%s -a crawl_unit=%s" % (city,crawl_unit))
        continue_status = open("tmp_continue_crawl_cmd", 'r').readline().strip()
        print("******%s" % continue_status)
        time.sleep(5)
        arr = continue_status.split(":")
        if (len(arr) > 1 and arr[1] == "False"):
          break
      