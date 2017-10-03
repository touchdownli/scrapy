import scrapy
class JobItem(scrapy.Item):
    #职位名称
    job_title=scrapy.Field()
    #公司名称
    company_name=scrapy.Field()
    #工作地点
    location_name=scrapy.Field()
    #薪水范围
    salary_range=scrapy.Field()
    #学历要求
    school_level=scrapy.Field()
    #工作年限
    experience_year=scrapy.Field()
    #公司性质
    company_feature=scrapy.Field()
    #公司规模
    company_size=scrapy.Field()
    #岗位描述
    job_desc=scrapy.Field()
    city=scrapy.Field()
      