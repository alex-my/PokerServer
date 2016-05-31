-- account

DROP TABLE IF EXISTS `account`;
CREATE TABLE `account` (
  `account_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Identifier',
  `uuid` varchar(128) NOT NULL DEFAULT '',
  `cid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'channel id',
  `user_name` varchar(128) NOT NULL DEFAULT '',
  `password` varchar(128) NOT NULL DEFAULT '',
  `token_key` varchar(100) NOT NULL DEFAULT '',
  `locked` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `locked_expire` int(3) unsigned NOT NULL DEFAULT '0',
  `create_time` int(10) unsigned NOT NULL DEFAULT 0,
  `last_login` int(10) unsigned NOT NULL DEFAULT 0,
  `last_logout` int(10) unsigned NOT NULL DEFAULT 0,
  `name` varchar(60) NOT NULL DEFAULT '' COMMENT '角色名称',
  `head_frame` smallint(10) NOT NULL DEFAULT '1' COMMENT '头像框',
  `head_icon` smallint(10) NOT NULL DEFAULT '1' COMMENT '头像',
  `sex` tinyint(1) DEFAULT '1' COMMENT '性别 默认男',
  `room_id` int(3) unsigned NOT NULL DEFAULT '0' COMMENT '当前进入的房间',
  `room_type` int(3) unsigned NOT NULL DEFAULT '0' COMMENT '当前进入的游戏类型',
  `gold` int(10) DEFAULT '0' COMMENT '元宝',
  `point` int(10) DEFAULT '0' COMMENT '总积分',
  PRIMARY KEY (`account_id`),
  UNIQUE KEY `idx_username` (`user_name`),
  KEY `uuid` (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=100000 DEFAULT CHARSET=utf8 COMMENT='Account';


-- room

DROP TABLE IF EXISTS `room`;

CREATE TABLE `room` (
  `room_id` int(10) unsigned NOT NULL COMMENT 'Identifier',
  `room_type` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `rounds` int(10) unsigned NOT NULL DEFAULT 0,
  `create_time` int(10) unsigned NOT NULL DEFAULT 0,
  `account_id` int(10) unsigned NOT NULL DEFAULT 0,
  `data` LONGTEXT NOT NULL,
  PRIMARY KEY (`room_id`,`room_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




