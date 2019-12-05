# -*- coding: utf-8 -*-
from DBUtils.PooledDB import PooledDB
from store.base_store import BaseStore
from pseudo_article import config
import pymysql
import traceback
import time


class PseudoStore(object):
    """
    PseudoArticle类的数据库操作
    """
    def __init__(self):
        self.base_store = BaseStore()
        self.url_API = "http://apis.5118.com/wyc/akey"
        self.header = {
            "Content-type": "application/x-www-form-urlencoded",
            "Authorization": "APIKEY {}".format(config.PSEUDO_API_KEY)
        }
        self.art_table = 'articles'  # 存储文章 article_table
        self.art_cor_table = 'article_correspond'  # 存储原文章和伪原创文章对应关系 article_correspond
        self.last_ignore_artid_table = 'last_and_ignore_artid'  # 存储已经参与伪原创的最大article_id和无需伪原创的article_id
        self.sou_art_pool = PooledDB(pymysql, 1, 5, **config.ARTICLE_SOURCE_CONFIG)
        self.pse_art_pool = PooledDB(pymysql, 1, 5, **config.ARTICLE_PSEUDO_CONFIG)

    def query_last_id(self):
        """
        查询last_id
        """
        query_last_id_sql = 'select `last_id` from {}'.format(self.last_ignore_artid_table)
        connection = self.pse_art_pool.connection()
        result = self.base_store.query(query_last_id_sql, connection)
        if result is not None:
            last_id = result[0]
        else:
            last_id = 0
            # 向表中插入一条数据
            insert_one_data = {'last_id': 0}
            keys = 'last_id'
            values = '%s'
            insert_sql = 'insert into {table}({keys}) values ({values})'.format(table=self.last_ignore_artid_table,
                                                                                       keys=keys, values=values)
            self.base_store.insert(insert_sql, insert_one_data, connection)
        return last_id

    def query_article(self):
        """
        查询文章:
        1.从article_pseudo数据库的last_and_ignore_artid表中查询到last_id;
        2.按last_id查询下一条数据
        """
        try:
            last_id = self.query_last_id()
            print('last_id:', last_id)
            # `id`, `keyword`, `media`, `title`, `abstract`, `content`, `publish_time`, `create_time`, `update_time`
            query_sql = 'select * from {} where id > {}'.format(self.art_table, last_id)
            connection = self.sou_art_pool.connection()
            result = self.base_store.query(query_sql, connection)
            return result
        except:
            print("query_article error")
            traceback.print_exc()

    def insert_article(self, result, content):
        """
        将伪原创文章插入数据库表
        """
        try:
            # `id`, `keyword`, `media`, `title`, `abstract`, `content`, `publish_time`, `create_time`, `update_time`
            insert_data = {
                'id': result[0],
                'keyword': result[1],
                'media': result[2],
                'title': result[3],
                'abstract': result[4],
                'content': content,
                'publish_time': result[6],
                'create_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                'update_time': result[8],
            }
            keys = ','.join(insert_data.keys())
            values = ','.join(['%s'] * len(insert_data))
            insert_sql = 'insert ignore into {table}({keys}) values ({values})'.format(table=self.art_table,
                                                                                       keys=keys, values=values)
            connection = self.pse_art_pool.connection()
            self.base_store.insert(insert_sql, insert_data, connection)
        except:
            print("insert_article error")
            traceback.print_exc()

    def insert_correspond(self, source_article_id):
        """
        在伪原创库,存储原文章和伪原创文章的对应关系
        1.查询伪原创文章的id
        """
        try:
            query_sql = 'select max(id) from {}'.format(self.art_table)  # 查询伪原创文章id
            connection = self.pse_art_pool.connection()
            result = self.base_store.query(query_sql, connection)

            insert_correspond_data = {
                'source_article_id': source_article_id,
                'pseudo_article_id': result[0]
            }
            keys = ','.join(insert_correspond_data.keys())
            values = ','.join(['%s'] * len(insert_correspond_data))
            insert_correspond_sql = 'insert ignore into {table}({keys}) values ({values})'.format(
                table=self.art_cor_table,
                keys=keys, values=values)
            self.base_store.insert(insert_correspond_sql, insert_correspond_data, connection)
        except:
            print('insert_correspond error')
            traceback.print_exc()

    def update_last_id(self, article_id):
        """
        更改article_pseudo.last_and_ignore_artid表的last_id
        """
        try:
            update_sql = 'update {} set last_id = {} where id > 0'.format(self.last_ignore_artid_table, article_id)
            connection = self.pse_art_pool.connection()
            self.base_store.update(update_sql, connection)
        except:
            print("update_is_used error")
            traceback.print_exc()


if __name__ == '__main__':
    pseudo_store = PseudoStore()
    # pseudo_store.update_is_used(1)
    # pseudo_store.insert_correspond(1)
    # pseudo_store.update_last_id(2)
    pseudo_store.query_last_id()