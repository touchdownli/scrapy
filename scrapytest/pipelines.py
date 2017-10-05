# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# -*- coding: utf-8 -*-
# 引入文件
from scrapy.exceptions import DropItem
import json
import codecs

class ScrapytestPipeline(object):
    def __init__(self):
        #打开文件
        self.file = open('data.json', 'w')
        self.file = codecs.open('data.json', 'w', encoding='utf-8')
    # #该方法用于处理数据
    def process_item(self, item, spider):
        ##读取item中的数据
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # 写入文件
        self.file.write(line)
        # 返回item
        return item
        
import pymysql  
class MySQL51JobPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
        user="root",
        password="",
        port=3306,
        host="127.0.0.1",
        db="scrapy_51job",
        charset="utf8")
        self.cursor = self.conn.cursor()

    #pipeline默认调用
    def process_item(self, item, spider):
        try:
            self.cursor.execute("\
            insert into job_table(job_title, company_name, location_name, \
            salary_range, school_level,experience_year,\
            company_feature,company_size,job_desc,city) \
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (item['job_title'], item['company_name'], item['location_name'],
            item['salary_range'], item['school_level'], item['experience_year'],
            item['company_feature'], item['company_size'], item['job_desc'], item['city']))
            self.conn.commit()
        except pymysql.InternalError as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
        return item
            
    #异常处理
    def _handle_error(self, failue, item, spider):
        log.err(failure)
    #该方法在spider被开启时被调用。
    def open_spider(self, spider):
        pass
    #该方法在spider被关闭时被调用。
    def close_spider(self, spider):
        pass

class MySQLLianjiaPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
        user="root",
        password="",
        port=3306,
        host="127.0.0.1",
        db="scrapy",
        charset="utf8")
        self.cursor = self.conn.cursor()

    #pipeline默认调用
    def process_item(self, item, spider):
        try:
            self.cursor.execute("\
            insert into lianjia_house(id, layout, floor, \
            total_area,layout_structure,usable_area,\
            build_type,orientation,construction_year,\
            decoration,build_structure,heating_mode,\
            hshold_ladder_ratio,property_right_length,elevator,\
            trans_right,house_property,ownership_type,\
            community,district,business_district,\
            crawl_unit,city) \
            values(%s, %s, %s, \
              %s, %s, %s,\
              %s, %s, %s, \
              %s, %s, %s, \
              %s, %s, %s, \
              %s, %s, %s, \
              %s, %s, %s, \
              %s,%s)",
            (item['id'], item['layout'], item['floor'],
            item['total_area'], item['layout_structure'], item['usable_area'],
            item['build_type'], item['orientation'], item['construction_year'],
            item['decoration'], item['build_structure'], item['heating_mode'],
            item['hshold_ladder_ratio'], item['property_right_length'], item['elevator'],
            item['trans_right'], item['house_property'],item['ownership_type'],
            item['community'],item['district'],item['business_district'],
            item['crawl_unit'],item['city'])
            )
            # trans history
            trans_history = item['trans_history']
            for (trans_date,trans_info) in trans_history.items():
              self.cursor.execute("insert into trans_history(\
              id,trans_price,trans_date,\
              list_price,list_date,trans_age,\
              price_adjustment_times,visit_times,follow_times,\
              view_times) \
              values(\
              %s,%s,%s,\
              %s,%s,%s,\
              %s,%s,%s,\
              %s)",
              (item['id'], trans_info['trans_price'], trans_date,
               trans_info['list_price'],trans_info['list_date'],trans_info['trans_age'],
               trans_info['price_adjustment_times'],trans_info['visit_times'],trans_info['follow_times'],
               trans_info['view_times']))
            self.conn.commit()
        except pymysql.InternalError as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
        return item
            
    #异常处理
    def _handle_error(self, failue, item, spider):
        log.err(failure)
    #该方法在spider被开启时被调用。
    def open_spider(self, spider):
        pass
    #该方法在spider被关闭时被调用。
    def close_spider(self, spider):
        pass
