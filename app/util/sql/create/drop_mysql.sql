REVOKE ALL PRIVILEGES ON * . * FROM 'bbg'@'localhost';

REVOKE ALL PRIVILEGES ON `bbg_server` . * FROM 'bbg'@'localhost';

REVOKE GRANT OPTION ON `bbg_server` . * FROM 'bbg'@'localhost';

DROP USER 'bbg'@'localhost';

DROP DATABASE IF EXISTS `bbg_server`;