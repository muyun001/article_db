# -*- coding: utf8 -*-

"""
输入库
文章系统数据库,用于向各项目提供文章.
默认连接原文章数据库,伪原创数据库为"article_pseudo"
"""
ARTICLE_DB_CONFIG = {
    'host': 'mysql',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'article_source'
}

"""
输出库
tag分拣数据库,存储文章的tag标签及权重.
默认连接原文章的tag分拣数据库,伪原创数据库为"tag_sort_pseudo_article"
"""
TAG_SORT_ARTICLE_CONFIG = {
    'host': 'mysql',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'tag_sort_source_article'
}

"""
百度 API Key 和 Secret Key.
"""
BAIDU_API_KEY = "GgSQO29VEX1oFmwK2stGHsAt"
BAIDU_SECRET_KEY = "qhYxLHRcrToybRGHKNPkvuUV8sAFQczg"
