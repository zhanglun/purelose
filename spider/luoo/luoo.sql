
CREATE TABLE `vol` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `vol_id` int(11) NOT NULL,
  `vol_number` int(11) NOT NULL,
  `url` char(255) NOT NULL,
  `title` char(255) NOT NULL DEFAULT '',
  `description` text NOT NULL,
  `cover` char(255) NOT NULL DEFAULT '',
  `vol_prev` varchar(255) DEFAULT '',
  `vol_next` varchar(255) DEFAULT NULL,
  `track_list_id` varchar(255) DEFAULT NULL,
  `tags` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vol_number` (`vol_number`)
) ENGINE=InnoDB AUTO_INCREMENT=10004 DEFAULT CHARSET=utf8;

CREATE TABLE `track` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `track_id` int(11) NOT NULL,
  `vol_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL DEFAULT '',
  `artist` varchar(255) NOT NULL DEFAULT '',
  `album` varchar(255) NOT NULL DEFAULT '',
  `cover` varchar(255) NOT NULL DEFAULT '',
  `url` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `track_id` (`track_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;