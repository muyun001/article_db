# -*- coding: utf-8 -*-
from DBUtils.PooledDB import PooledDB
from store.base_store import BaseStore
from tag_sorting import config
import pymysql
import traceback


class TagStore(object):
    """
    TagSort类的数据库操作
    """
    def __init__(self):
        self.base_store = BaseStore()
        self.article_table = 'articles'
        self.tag_table = 'tags'  # 存储标签
        self.art_cor_table = 'tag_article_correspond'  # 存储原文章和伪原创文章对应关系 tag_article_correspond
        self.last_ignore_artid_table = 'last_and_ignore_artid'  # 存储已经参与伪原创的最大article_id和无需伪原创的article_id
        self.article_pool = PooledDB(pymysql, 1, 5, **config.ARTICLE_DB_CONFIG)
        self.tag_pool = PooledDB(pymysql, 1, 5, **config.TAG_SORT_ARTICLE_CONFIG)

    def query_last_id(self):
        """
        查询last_id
        """
        query_last_id_sql = 'select `last_id` from {}'.format(self.last_ignore_artid_table)
        connection = self.tag_pool.connection()
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
        从last_id开始查询文章
        """
        try:
            last_id = self.query_last_id()
            query_sql = "select `id`, `title`, `content` from {} where id > {} and title != ''".format(self.article_table, last_id)
            connection = self.article_pool.connection()
            result = self.base_store.query(query_sql, connection)
            return result
        except:
            print("query_article error")
            traceback.print_exc()

    def query_tag_id(self, tag):
        """
        查询tag_id
        """
        try:
            query_tag_id_sql = 'select `id` from {} where tag="{}"'.format(self.tag_table, tag)
            connection = self.tag_pool.connection()
            result = self.base_store.query(query_tag_id_sql, connection)
            return result
        except:
            print("query_tag_id error")
            traceback.print_exc()

    def insert_tag(self, tag):
        """
        存储tag
        """
        try:
            insert_tag_data = {"tag": tag}
            keys = ','.join(insert_tag_data.keys())
            values = ','.join(['%s'] * len(insert_tag_data))
            insert_tag_sql = 'insert ignore into {table}({keys}) values ({values})'.format(table=self.tag_table,
                                                                                           keys=keys, values=values)
            connection = self.tag_pool.connection()
            self.base_store.insert(insert_tag_sql, insert_tag_data, connection)
        except:
            print("insert_tag error")
            traceback.print_exc()

    def insert_tagid_score(self, article_id, tag, score):
        """
        将article_id,tag和score的对应关系存储数据库
        """
        try:
            tag_id = self.query_tag_id(tag)
            insert_tag_article_data = {
                "article_id": article_id,
                "tag_id": tag_id[0],
                "score": score
            }
            keys = ','.join(insert_tag_article_data.keys())
            values = ','.join(['%s'] * len(insert_tag_article_data))
            insert_tag_articleid_sql = 'insert ignore into {table}({keys}) values ({values})'.format(
                table=self.art_cor_table,
                keys=keys, values=values)
            connection = self.tag_pool.connection()
            self.base_store.insert(insert_tag_articleid_sql, insert_tag_article_data, connection)
        except:
            print("insert_tagid_score error")
            traceback.print_exc()

    def update_last_id(self, article_id):
        """
        更改last_id
        """
        try:
            update_sql = 'update {} set last_id = {} where id > 0'.format(self.last_ignore_artid_table, article_id)
            connection = self.tag_pool.connection()
            self.base_store.update(update_sql, connection)
        except:
            print("update_is_used error")
            traceback.print_exc()


if __name__ == '__main__':
    tag_store = TagStore('source')
    tag_store.query_article()