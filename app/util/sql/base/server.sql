
DROP TABLE IF EXISTS `account`;

CREATE TABLE `account` (
  `account_id` int(10) unsigned NOT NULL COMMENT 'Identifier',
  `uuid` varchar(256) NOT NULL DEFAULT '',
  `cid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'channel id',
  `user_name` varchar(128) NOT NULL DEFAULT '',
  `password` varchar(128) NOT NULL DEFAULT '',
  `token_key` varchar(128) NOT NULL DEFAULT '',
  `locked` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `locked_expire` int(3) unsigned NOT NULL DEFAULT '0',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0',
  `last_login` int(10) unsigned NOT NULL DEFAULT '0',
  `last_logout` int(10) unsigned NOT NULL DEFAULT '0',
  `name` varchar(60) NOT NULL DEFAULT '' COMMENT '角色名称',
  `head_frame` longtext NOT NULL COMMENT '头像框',
  `head_icon` longtext NOT NULL COMMENT '头像',
  `sex` tinyint(1) DEFAULT '1' COMMENT '性别 默认男',
  `room_id` int(3) unsigned NOT NULL DEFAULT '0' COMMENT '当前进入的房间',
  `room_type` int(3) unsigned NOT NULL DEFAULT '0' COMMENT '当前进入的游戏类型',
  `gold` int(10) DEFAULT '0' COMMENT '元宝',
  `proxy_id` int(10) DEFAULT '0' COMMENT '上级ID',
  `proxy_count` int(10) DEFAULT '0' COMMENT '下级数量',
  `level` int(10) NOT NULL DEFAULT '4' COMMENT '代理等级(0-N) 0位管理员',
  `month` int(10) DEFAULT '0' COMMENT '本月月份',
  `month_recharge` int(10) DEFAULT '0' COMMENT '当月充值',
  `all_recharge` int(10) DEFAULT '0' COMMENT '总充值',
  `month_proxy_recharge` int(10) DEFAULT '0' COMMENT '代理当月充值',
  `all_proxy_recharge` int(10) DEFAULT '0' COMMENT '代理总充值',
  `poker_point` int(10) DEFAULT '0' COMMENT '扑克总积分',
  `mahjong_point` int(10) DEFAULT '0' COMMENT '麻将总积分',
  `gold_point` int(10) DEFAULT '0' COMMENT '金币总积分',
  PRIMARY KEY (`account_id`),
  UNIQUE KEY `idx_username` (`user_name`),
  KEY `uuid` (`uuid`(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Account';


DROP TABLE IF EXISTS `history`;

CREATE TABLE `history` (
  `account_id` int(10) unsigned NOT NULL,
  `data` longtext NOT NULL,
  PRIMARY KEY (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `infomation`;

CREATE TABLE `infomation` (
  `id` int(10) unsigned NOT NULL,
  `content` longtext NOT NULL,
  `desc` varchar(128) NOT NULL DEFAULT '' COMMENT '描述',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO `infomation` (`id`, `content`, `desc`)
VALUES
  (1,'..','跑马灯'),
  (2,'充','联系方式'),
  (3,'101','版本号');


DROP TABLE IF EXISTS `log_gold`;

CREATE TABLE `log_gold` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '管理ID',
  `account_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '帐号ID',
  `count` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '消费数量',
  `remain` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '剩余数量',
  `origin_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '消费处ID',
  `time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '使用时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `proxy`;

CREATE TABLE `proxy` (
  `proxy_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '代理人ID',
  `account` varchar(32) NOT NULL DEFAULT '' COMMENT '账号',
  `password` varchar(32) NOT NULL DEFAULT '' COMMENT '密码',
  `level` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '级别',
  `name` varchar(32) NOT NULL DEFAULT '' COMMENT '代理人名字',
  `phone` int(10) unsigned NOT NULL DEFAULT '0',
  `address` varchar(128) NOT NULL DEFAULT '',
  `join_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '加入时间',
  `before_proxy_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '上一级代理人ID',
  `state` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '状态',
  PRIMARY KEY (`proxy_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



DROP TABLE IF EXISTS `recharge`;

CREATE TABLE `recharge` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '管理ID',
  `account_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '帐号ID',
  `proxy_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '代理人ID',
  `op_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '订单号',
  `money` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '充值金额',
  `ingot` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '转化的代币',
  `origin` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '充值来源',
  `time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '充值时间',
  `level` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '级别',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_op_id` (`op_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


# Dump of table room
# ------------------------------------------------------------

DROP TABLE IF EXISTS `room`;

CREATE TABLE `room` (
  `room_id` int(10) unsigned NOT NULL COMMENT 'Identifier',
  `room_type` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `room_help` int(10) unsigned NOT NULL DEFAULT '0',
  `rounds` int(10) unsigned NOT NULL DEFAULT '0',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0',
  `account_id` int(10) unsigned NOT NULL DEFAULT '0',
  `data` longtext NOT NULL,
  PRIMARY KEY (`room_id`,`room_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(10) NOT NULL AUTO_INCREMENT,
  `account_id` varchar(256) NOT NULL,
  `user_name` varchar(256) NOT NULL COMMENT '用户名',
  `password` varchar(128) NOT NULL,
  `locked` tinyint(3) NOT NULL COMMENT '代理开启状态',
  `create_time` int(10) NOT NULL,
  `last_login` int(10) NOT NULL,
  `name` varchar(128) NOT NULL COMMENT '昵称',
  `head_icon` longtext NOT NULL,
  `sex` tinyint(3) NOT NULL,
  `month` int(10) DEFAULT '0' COMMENT '本月月份',
  `month_recharge` int(10) DEFAULT '0' COMMENT '当月充值',
  `all_recharge` int(10) DEFAULT '0' COMMENT '总充值',
  `month_proxy_recharge` int(10) DEFAULT '0' COMMENT '代理当月充值',
  `all_proxy_recharge` int(10) DEFAULT '0' COMMENT '代理总充值',
  `level` tinyint(3) NOT NULL COMMENT '代理等级(0-N) 0位管理员',
  `superiorId` varchar(32) NOT NULL COMMENT '上级ID',
  `insertingCoil` int(10) NOT NULL COMMENT '下线数量',
  `address` varchar(256) NOT NULL,
  `phone` varchar(12) NOT NULL,
  `card` int(32) NOT NULL,
  `city` varchar(128) NOT NULL,
  `remark` varchar(256) NOT NULL,
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `user` (`user_id`, `account_id`, `user_name`, `password`, `locked`, `create_time`, `last_login`, `name`, `head_icon`, `sex`, `month`, `month_recharge`, `all_recharge`, `month_proxy_recharge`, `all_proxy_recharge`, `level`, `superiorId`, `insertingCoil`, `address`, `phone`, `card`, `city`, `remark`)
VALUES
  (1,'admin','admin','980dfe93b9af423772dede35e286dcc2',1,1465567986,1465567986,'admin123','',1,0,0,0,0,0,0,'0',7,'0','0',0,'佛山','0');
