# MessageBoard
后端考核任务
留言板

没有任何过滤



需要的两张表

CREATE TABLE `tbl_user` (
  `user_id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_name` VARCHAR(45) DEFAULT NULL,
  `user_password` VARCHAR(300) NULL,
  PRIMARY KEY (`user_id`));

CREATE TABLE `tbl_words` (
  `words_id` int(11) NOT NULL AUTO_INCREMENT,
  `words_description` varchar(5000) DEFAULT NULL,
  `words_user_id` varchar(45) DEFAULT NULL,
  `words_date` datetime DEFAULT NULL,
  PRIMARY KEY (`words_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT character set = utf8;