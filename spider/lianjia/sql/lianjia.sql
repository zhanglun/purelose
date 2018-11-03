create database if not exists lianjia;

use lianjia;

create table if not exists `chengjiao` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sign_at` timestamp NULL DEFAULT NULL COMMENT '签约时间',
  `sign_method` varchar(256) DEFAULT NULL COMMENT '签约方式',
  `total_price` varchar(256) DEFAULT NULL COMMENT '总价(单位：万元)',
  `unit_price` varchar(256) DEFAULT NULL COMMENT '单价(单位：元)',
  `building_structure` varchar(256) DEFAULT NULL COMMENT '结构',
  `building_floor` varchar(256) DEFAULT NULL COMMENT '楼层',
  `building_size` varchar(256) DEFAULT NULL COMMENT '建筑面积',
  `building_meta` varchar(256) DEFAULT NULL COMMENT '房屋其他信息',
  `building_style` varchar(256) DEFAULT NULL COMMENT '建筑形态',
  `building_towards` varchar(256) DEFAULT NULL COMMENT '朝向',
  `building_year` varchar(256) DEFAULT NULL COMMENT '建造年份',
  `city` varchar(256) DEFAULT NULL COMMENT '所在城市',
  `city_area` varchar(256) DEFAULT NULL COMMENT '所在城区',
  `area_name` varchar(256) DEFAULT NULL COMMENT '所在地区',
  `community_name` varchar(256) DEFAULT NULL COMMENT '所在小区',
  `community_meta` text COMMENT '该小区其他信息',
  `origin_title` varchar(256) DEFAULT NULL COMMENT '网页标题',
  `origin_url` varchar(256) DEFAULT NULL COMMENT '源网页',
  `input_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '录入时间',
  `hid` varchar(36) NOT NULL DEFAULT '' COMMENT '房屋id',
  `rid` varchar(36) NOT NULL DEFAULT '' COMMENT '小区id',
  PRIMARY KEY (`id`),
  UNIQUE KEY `hid` (`hid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
