-- account

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
  `create_time` int(10) unsigned NOT NULL DEFAULT 0,
  `last_login` int(10) unsigned NOT NULL DEFAULT 0,
  `last_logout` int(10) unsigned NOT NULL DEFAULT 0,
  `name` varchar(60) NOT NULL DEFAULT '' COMMENT '角色名称',
  `head_frame` LONGTEXT NOT NULL NOT NULL COMMENT '头像框',
  `head_icon` LONGTEXT NOT NULL COMMENT '头像',
  `sex` tinyint(1) DEFAULT '1' COMMENT '性别 默认男',
  `room_id` int(3) unsigned NOT NULL DEFAULT '0' COMMENT '当前进入的房间',
  `room_type` int(3) unsigned NOT NULL DEFAULT '0' COMMENT '当前进入的游戏类型',
  `gold` int(10) DEFAULT '0' COMMENT '元宝',
  `proxy_id` int(10) DEFAULT '0' COMMENT '上级ID',
  `month` int(10) DEFAULT '0' COMMENT '本月月份',
  `month_recharge` int(10) DEFAULT '0' COMMENT '当月充值',
  `all_recharge` int(10) DEFAULT '0' COMMENT '总充值',
  `poker_point` int(10) DEFAULT '0' COMMENT '扑克总积分',
  `mahjong_point` int(10) DEFAULT '0' COMMENT '麻将总积分',
  PRIMARY KEY (`account_id`),
  UNIQUE KEY `idx_username` (`user_name`),
  KEY `uuid` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Account';


-- room

DROP TABLE IF EXISTS `room`;

CREATE TABLE `room` (
  `room_id` int(10) unsigned NOT NULL COMMENT 'Identifier',
  `room_type` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `room_help` int(10) unsigned NOT NULL DEFAULT 0,
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_op_id` (`op_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- log: gold

DROP TABLE IF EXISTS `log_gold`;
CREATE TABLE `log_gold` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '管理ID',
  `account_id` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '帐号ID',
  `count` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '消费数量',
  `remain` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '剩余数量',
  `origin_id` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '消费处ID',
  `time` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '使用时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- game infomation
DROP TABLE IF EXISTS `infomation`;
CREATE TABLE `infomation` (
    `id` int(10) unsigned NOT NULL,
    `content` LONGTEXT NOT NULL,
    `desc` varchar(128) NOT NULL DEFAULT '' COMMENT '描述',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `infomation` (`id`, `content`, `desc`)
VALUES
  (1, '我们现在推出的免费送金币活动到6月21日截止', '跑马灯'),
  (2, '充值请联系微信账号34192391', '联系方式');


-- user

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
  `sex` tinyint(3) NOT NULL,
  `monthRecharge` int(32) NOT NULL COMMENT '当月充值',
  `totalRecharge` int(32) NOT NULL COMMENT '总充值',
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


-- play history

DROP TABLE IF EXISTS `history`;
CREATE TABLE `history` (
    `account_id` int(10) unsigned NOT NULL,
    `data` LONGTEXT NOT NULL,
    PRIMARY KEY (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

