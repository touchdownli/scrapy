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
        db="scrapy_lianjia",
        charset="utf8")
        self.cursor = self.conn.cursor()

    #pipeline默认调用
    def process_item(self, item, spider):
        try:
            self.cursor.execute("\
            insert into house(id, layout, floor, \
            total_area,layout_structure,usalbe_area,\
            build_type,orientation,constructure_year,\
            decoration,build_structure,heating_mode,\
            hshold_ladder_ratio,property_right_length,elevator,\
            trans_right,community,house_property,\
            trans_age,ownership_type) \
            values(%s, %s, %s, \
	      %s, %s, %s,\
              %s, %s, %s, \
              %s, %s, %s, \
              %s, %s, %s, \
              %s, %s, %s, \
              %s,%s)",
            (item['id'], item['layout'], item['floor'],
            item['total_area'], item['layout_structure'], item['usable_area'],
            item['build_type'], item['orientation'], item['constructure_year'],
            item['decoration'], item['build_structure'], item['heating_mode'],
            item['hshod_ladder_ratio'], item['property_right_length'], item['elevator'],
            item['trans_right'], item['community'], item['house_property'],
            item['trans_age'], item['ownership_type']))
            # trans history
            trans_history = item['trans_history']
            '''
            self.cursor.execute("insert into trans(id,price,list_price,trans_date,list_date) \
            values(%s,%s,%s,%s,%s)",
            (item['id'], item['']))
            '''
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
