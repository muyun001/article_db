-- 创建tag分检数据库
create database tag_sort_source_article default character set utf8;

-- 创建tags表
CREATE TABLE tag_sort_source_article.tags (
    `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
    `tag` VARCHAR(255) COLLATE UTF8_UNICODE_CI NOT NULL COMMENT '标签',
    PRIMARY KEY (`id`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 COLLATE = UTF8_UNICODE_CI;
-- 创建唯一索引
ALTER TABLE tag_sort_source_article.tags ADD UNIQUE (tag);

-- 创建文章和tag的对应关系表
CREATE TABLE tag_sort_source_article.tag_article_correspond (
    `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
    `article_id` BIGINT(20) NOT NULL COMMENT '文章id',
    `tag_id` BIGINT(20) NOT NULL COMMENT '标签id',
    `score` DECIMAL(7, 6) NOT NULL COMMENT '权重',
    PRIMARY KEY (`id`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 COLLATE = UTF8_UNICODE_CI;
-- 创建唯一索引
-- ALTER TABLE tag_sort_source_article.tag_article_correspond ADD UNIQUE (tag_id, article_id);

-- 存储已经参与tag分类的最大文章id和无需伪原创的文章id
CREATE TABLE tag_sort_source_article.last_and_ignore_artid (
    `id` INT(20) NOT NULL AUTO_INCREMENT,
    `last_id` BIGINT(20) DEFAULT 0 NOT NULL COMMENT '参与tag分类的文章的最大id, 默认0',
    `ignore_article_ids` VARCHAR(255) COLLATE UTF8_UNICODE_CI DEFAULT NULL COMMENT '无需tag分类的文章id',
    PRIMARY KEY (`id`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8 COLLATE = UTF8_UNICODE_CI;