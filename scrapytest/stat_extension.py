import logging
from scrapy import signals
from scrapy.exceptions import NotConfigured

logger = logging.getLogger(__name__)

class ContinueCrawlStatusCheck(object):
    def __init__(self, stats):
      self.stats = stats
      self.file = open("tmp_continue_crawl_cmd", 'w+')

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise

        # get the number of items from settings

        # instantiate the extension object
        ext = cls(crawler.stats)

        # connect the extension object to signals
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)

        # return the extension object
        return ext

    def spider_closed(self, spider):
        if (self.stats.get_value('item_scraped_count') < 3):
          self.file.write(spider.crawl_unit + "_continue:False")
        else:
          self.file.write(spider.crawl_unit + "_continue:True")
        self.file.close()