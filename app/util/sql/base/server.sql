-- account

DROP TABLE IF EXISTS `account`;
CREATE TABLE `account` (
  `account_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Identifier',
  `uuid` varchar(256) NOT NULL DEFAULT '',
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
  `head_frame` varchar(64) NOT NULL DEFAULT '' COMMENT '头像框',
  `head_icon` varchar(64) NOT NULL DEFAULT '' COMMENT '头像',
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


-- proxy

DROP TABLE IF EXISTS `proxy`;
CREATE TABLE `proxy` (
  `proxy_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '代理人ID',
  `account` varchar(32) NOT NULL DEFAULT '' COMMENT '账号',
  `password` varchar(32) NOT NULL DEFAULT '' COMMENT '密码',
  `level` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '级别',
  `name` varchar(32) NOT NULL DEFAULT '' COMMENT '代理人名字',
  `phone` int(10) unsigned NOT NULL DEFAULT 0,
  `address` varchar(128) NOT NULL DEFAULT '',
  `join_time` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '加入时间',
  `before_proxy_id` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '上一级代理人ID',
  `state` tinyint(1) unsigned NOT NULL DEFAULT 0 COMMENT '状态',
  PRIMARY KEY (`proxy_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8;


-- recharge

DROP TABLE IF EXISTS `recharge`;
CREATE TABLE `recharge` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '管理ID',
  `account_id` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '帐号ID',
  `proxy_id` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '代理人ID',
  `op_id` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '订单号',
  `money` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '充值金额',
  `ingot` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '转化的代币',
  `origin` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '充值来源',
  `time` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '充值时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- log: gold

DROP TABLE IF EXISTS `log_gold`;
CREATE TABLE `log_gold` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '管理ID',
  `account_id` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '帐号ID',
  `count` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '消费数量',
  `origin_id` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '消费处ID',
  `time` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '使用时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




