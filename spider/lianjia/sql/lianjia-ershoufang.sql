CREATE TABLE `lianjia_ershoufang` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `origin_url` varchar(256) DEFAULT NULL,
  `title` varchar(256) DEFAULT NULL,
  `hid` varchar(32) DEFAULT NULL,
  `rid` varchar(32) DEFAULT NULL,
  `price_total` bigint(10) DEFAULT NULL,
  `price_total_unit` varchar(4) DEFAULT NULL,
  `unit_price` bigint(10) DEFAULT NULL,
  `community_name` varchar(256) DEFAULT NULL,
  `area_name` varchar(256) DEFAULT NULL,
  `input_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `transaction` text,
  `cost_payment` text,
  `city` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hid` (`hid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;