import scrapy
class CourseItem(scrapy.Item):
      title=scrapy.Field()
      url=scrapy.Field()
      image_url=scrapy.Field()
      introduction=scrapy.Field()
      student=scrapy.Field()
      catycray=scrapy.Field()
      degree=scrapy.Field()
      hour=scrapy.Field()
      score=scrapy.Field()
      