systemctl start mariadb.service
scrapy crawl Jobspider -a city=beijing -s JOBDIR=crawls/Jobspider-1

scrapy crawl LianjiaSpider -s JOBDIR=crawls/LianjiaSpider-1
