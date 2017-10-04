create database scrapy_51job DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
use scrapy_51job;
CREATE TABLE `job_table` (
  `id` int(32) NOT NULL auto_increment COMMENT '',
  `job_title` varchar(256) NOT NULL COMMENT '',
  `company_name` varchar(256) NOT NULL COMMENT '',
  `location_name` varchar(256) NOT NULL DEFAULT '' COMMENT '',
  `salary_range` varchar(256) NOT NULL DEFAULT '' COMMENT '',
  `school_level` varchar(256) NOT NULL DEFAULT '' COMMENT '',
  `experience_year` varchar(256) NOT NULL DEFAULT '' COMMENT '',
  `company_feature` varchar(256) NOT NULL DEFAULT '' COMMENT '',
  `company_size` varchar(256) NOT NULL DEFAULT '' COMMENT '',
  `job_desc` varchar(8192) NOT NULL DEFAULT '' COMMENT '',
  `city` varchar(256) NOT NULL DEFAULT '' COMMENT '',
  PRIMARY KEY (`id`)
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

--mysql> source D:\scrapytest\scrapytest\scrapytest\51job.sql
