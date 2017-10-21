# -*- coding: utf-8 -*-

import scrapy
class LianjiaItem(scrapy.Item):
    layout=scrapy.Field()
    floor=scrapy.Field()
    total_area=scrapy.Field()
    layout_structure=scrapy.Field()
    usable_area=scrapy.Field()
    build_type=scrapy.Field()
    orientation=scrapy.Field()
    construction_year=scrapy.Field()
    decoration=scrapy.Field()
    build_structure=scrapy.Field()
    heating_mode=scrapy.Field()
    hshold_ladder_ratio=scrapy.Field()
    property_right_length=scrapy.Field()
    elevator=scrapy.Field()
    
    id=scrapy.Field()
    trans_right=scrapy.Field()
    list_date=scrapy.Field()
    house_property=scrapy.Field()
    trans_age=scrapy.Field()
    ownership_type=scrapy.Field()

    community=scrapy.Field()
    
    list_price=scrapy.Field()
    price_adjustment_times=scrapy.Field()
    visit_times=scrapy.Field()
    follow_times=scrapy.Field()
    view_times=scrapy.Field()
    
    trans_date=scrapy.Field()
    trans_history=scrapy.Field()

    district=scrapy.Field()
    business_district=scrapy.Field()
    crawl_unit=scrapy.Field()
    city=scrapy.Field()
    
    #second_hand_house_sale_info
    last_trans_date=scrapy.Field()
    crawl_date=scrapy.Field()
    mortgage=scrapy.Field()
    certicate=scrapy.Field()

