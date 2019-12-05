# -*- coding: utf8 -*-

"""
输入库
原文章数据库,可用于提供文章进行伪原创或其他.
"""
ARTICLE_SOURCE_CONFIG = {
    'host': 'mysql',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'article_source'
}

"""
输出库
伪原创文章数据库,存储经过伪原创的文章.
"""
ARTICLE_PSEUDO_CONFIG = {
    'host': 'mysql',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'article_pseudo'
}

"""
5118API的key值
"""
PSEUDO_API_KEY = '4E9402A677334B2FA9822F38B5A28B2E'
