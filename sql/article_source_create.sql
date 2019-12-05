-- 创建原文章数据库
create database article_source default character set utf8;

-- 创建文章表格
CREATE TABLE article_source.articles (
    `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
    `keyword` VARCHAR(255) COLLATE UTF8_UNICODE_CI NOT NULL COMMENT '关键词',
    `media` VARCHAR(128) COLLATE UTF8_UNICODE_CI DEFAULT NULL COMMENT '文章出处,如 头条',
    `title` VARCHAR(255) COLLATE UTF8_UNICODE_CI NOT NULL COMMENT '文章标题',
    `abstract` TEXT COLLATE UTF8_UNICODE_CI DEFAULT NULL COMMENT '文章摘要',
    `content` LONGTEXT COLLATE UTF8_UNICODE_CI NOT NULL COMMENT '文章',
    `publish_time` TIMESTAMP NULL DEFAULT NULL COMMENT '文章发布时间',
    `create_time` TIMESTAMP NULL DEFAULT NULL COMMENT '抓取时间',
    `update_time` TIMESTAMP NULL DEFAULT NULL COMMENT '更新时间',
    `is_used` TINYINT(1) DEFAULT 0 COMMENT '是否已进行文章子集的分类, 默认0',
    PRIMARY KEY (`id`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 COLLATE = UTF8_UNICODE_CI;


