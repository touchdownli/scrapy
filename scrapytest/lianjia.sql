#CREATE DATABASE `scrapy` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `scrapy`;
#drop table lianjia_house;
CREATE TABLE `lianjia_house` (
  `id` varchar(32) NOT NULL COMMENT '链家编号',
  `layout` varchar(256) NOT NULL COMMENT '户型',
  `floor` varchar(128) NOT NULL COMMENT '楼层',
  `total_area` varchar(256) NOT NULL DEFAULT '' COMMENT '建筑面积',
  `layout_structure` varchar(256) NOT NULL DEFAULT '' COMMENT '复式、平层',
  `usable_area` varchar(256) NOT NULL DEFAULT '' COMMENT '套内面积',
  `build_type` varchar(32) NOT NULL DEFAULT '' COMMENT '塔楼',
  `orientation` varchar(32) NOT NULL DEFAULT '' COMMENT '朝向',
  `construction_year` year NOT NULL DEFAULT '0000' COMMENT '建筑年代',
  `decoration` varchar(32) NOT NULL DEFAULT '' COMMENT '精装',
  `build_structure` varchar(64) NOT NULL DEFAULT '' COMMENT '砖混、钢混',
  `heating_mode` varchar(64) NOT NULL DEFAULT '' COMMENT '供热模式',
  `hshold_ladder_ratio` varchar(128) NOT NULL DEFAULT '' COMMENT '梯户比',
  `property_right_length` varchar(64) NOT NULL DEFAULT '' COMMENT '产权年限',
  `elevator` varchar(16) NOT NULL DEFAULT '' COMMENT '有无电梯',
  `water_type` varchar(16) NOT NULL DEFAULT '' COMMENT '用水类型',
  `electric_type` varchar(16) NOT NULL DEFAULT '' COMMENT '用电类型',
  `gas_price` varchar(16) NOT NULL DEFAULT '' COMMENT '燃气价格',
  `trans_right` varchar(64) NOT NULL DEFAULT '' COMMENT '商品房，经济适用房',
  `house_property` varchar(256) NOT NULL DEFAULT '' COMMENT '公寓',
  `ownership_type` varchar(32) NOT NULL DEFAULT '' COMMENT '非共有',
  `community` varchar(32) NOT NULL DEFAULT '' COMMENT '小区名',
  `district` varchar(64) NOT NULL DEFAULT '' COMMENT '城区',
  `business_district` varchar(128) NOT NULL DEFAULT '' COMMENT '商圈',
  `crawl_unit` varchar(64) NOT NULL DEFAULT '' COMMENT '抓取相关',
  `city` varchar(64) NOT NULL DEFAULT '' COMMENT '城市',
  PRIMARY KEY (`id`)
) ENGINE = MyISAM DEFAULT CHARSET = utf8;

#drop table trans_history;
CREATE TABLE `trans_history` (
  `id` varchar(32) NOT NULL COMMENT '',
  `trans_price` float NOT NULL DEFAULT 0 COMMENT '成交价格',
  `trans_date` date NOT NULL COMMENT '成交日期',
  `list_price` float NOT NULL DEFAULT 0 COMMENT '挂牌价格',
  `list_date` date NOT NULL DEFAULT '1970-01-01' COMMENT '挂牌日期',
  `trans_age` varchar(32) NOT NULL DEFAULT '' COMMENT '成交满几年',
  `price_adjustment_times` int(8) NOT NULL DEFAULT -1 COMMENT '调价次数',
  `visit_times` int(8) NOT NULL DEFAULT -1 COMMENT '带看次数',
  `follow_times` int(8) NOT NULL DEFAULT -1 COMMENT '关注次数',
  `view_times` int(8) NOT NULL DEFAULT -1 COMMENT '浏览次数',
  PRIMARY KEY (`id`,`trans_date`)
) ENGINE = MyISAM DEFAULT CHARSET = utf8;

CREATE TABLE `second_hand_house_sale_info` (
  `id` varchar(32) NOT NULL COMMENT '',
  `list_date` date NOT NULL DEFAULT '1970-01-01' COMMENT '挂牌日期',
  `last_trans_date` date NOT NULL DEFAULT '1970-01-01' COMMENT '上次交易',
  `trans_age` varchar(32) NOT NULL DEFAULT '' COMMENT '成交满几年',
  `mortgage`  varchar(1024) NOT NULL DEFAULT '' COMMENT '抵押信息',
  `certicate` varchar(32) NOT NULL DEFAULT '' COMMENT '房本备件',
  PRIMARY KEY (`id`,`list_date`)
) ENGINE = MyISAM DEFAULT CHARSET = utf8;

CREATE TABLE `second_hand_house_price_info` (
  `id` varchar(32) NOT NULL COMMENT '',
  `list_price` float NOT NULL DEFAULT 0 COMMENT '挂牌价格',
  `crawl_date` date NOT NULL DEFAULT '1970-01-01' COMMENT '价格抓取日期',
  `visit_times` int(8) NOT NULL DEFAULT -1 COMMENT '带看次数',
  `follow_times` int(8) NOT NULL DEFAULT -1 COMMENT '关注次数',
  PRIMARY KEY (`id`,`crawl_date`)
) ENGINE = MyISAM DEFAULT CHARSET = utf8;