-- 创建伪原创文章数据库
create database article_pseudo default character set utf8;

-- 创建伪原创文章表格
CREATE TABLE article_pseudo.articles (
    `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
    `keyword` VARCHAR(255) COLLATE UTF8_UNICODE_CI NOT NULL COMMENT '关键词',
    `media` VARCHAR(128) COLLATE UTF8_UNICODE_CI DEFAULT NULL COMMENT '文章出处,如 头条',
    `title` VARCHAR(255) COLLATE UTF8_UNICODE_CI NOT NULL COMMENT '文章标题',
    `abstract` TEXT COLLATE UTF8_UNICODE_CI DEFAULT NULL COMMENT '文章摘要',
    `content` LONGTEXT COLLATE UTF8_UNICODE_CI NOT NULL COMMENT '文章',
    `publish_time` TIMESTAMP NULL DEFAULT NULL COMMENT '原文章发布时间',
    `create_time` TIMESTAMP NULL DEFAULT NULL COMMENT '文章生成时间',
    `update_time` TIMESTAMP NULL DEFAULT NULL COMMENT '更新时间',
    `is_used` TINYINT(1) DEFAULT 0 COMMENT '是否已进行文章子集的分类, 默认0',
    PRIMARY KEY (`id`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 COLLATE = UTF8_UNICODE_CI;

-- 创建表格,存储伪原创文章和原文章的对应关系
CREATE TABLE article_pseudo.article_correspond (
    `pseudo_article_id` BIGINT(20) NOT NULL COMMENT '伪原创文章id',
    `source_article_id` BIGINT(20) NOT NULL COMMENT '原文章id',
    PRIMARY KEY (`pseudo_article_id`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 COLLATE = UTF8_UNICODE_CI;

-- 创建表格,存储已经参与伪原创的最大article_id和无需伪原创的article_id
CREATE TABLE article_pseudo.last_and_ignore_artid (
    `id` INT(20) NOT NULL AUTO_INCREMENT,
    `last_id` BIGINT(20) DEFAULT 0 NOT NULL COMMENT '参与伪原创原文章的最大id, 默认0',
    `ignore_article_ids` VARCHAR(255) COLLATE UTF8_UNICODE_CI DEFAULT NULL COMMENT '无需伪原创的文章id',
    PRIMARY KEY (`id`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 COLLATE = UTF8_UNICODE_CI;