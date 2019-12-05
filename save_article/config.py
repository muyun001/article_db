# -*- coding: utf8 -*-

"""
输入库
爬取文章数据库,文章暂存,用于向文章系统提供文章.
"""
ARTICLE_CRAWL_CONFIG = {
    'host': 'mysql',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'article_crawl'
}

"""
输出库
文章系统数据库,可用于提供文章进行伪原创或其他.
"""
ARTICLE_DB_CONFIG = {
    'host': 'mysql',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'article_source'
}