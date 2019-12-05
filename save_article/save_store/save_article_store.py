# coding: utf-8
from DBUtils.PooledDB import PooledDB
from store.base_store import BaseStore
from save_article import config
import pymysql
import traceback


class SaveArticleStore(object):
    """
    SaveArticle类的数据库操作
    """

    def __init__(self):
        self.base_store = BaseStore()
        self.article = 'articles'
        self.article_crawl_pool = PooledDB(pymysql, 1, 5, **config.ARTICLE_CRAWL_CONFIG)
        self.article_db_pool = PooledDB(pymysql, 1, 5, **config.ARTICLE_DB_CONFIG)

    def query_article(self):
        """
        查询文章
        """
        try:
            query_article = 'select `unique_key`, `keyword`, `media`, `title`, `article_source`, `datetime` from {} where is_used=0'.format(
                self.article)
            connection = self.article_crawl_pool.connection()
            result = self.base_store.query(query_article, connection)
            if result is not None:
                self.update_is_used(result[0])
            return result
        except:
            print("query_article error")
            traceback.print_exc()

    def query_article_id(self):
        """
        查询article_id
        """
        try:
            query_article_id_sql = 'show table status'
            connection = self.article_db_pool.connection()
            result = self.base_store.query(query_article_id_sql, connection)
            return result[10] - 1
        except:
            print("query_article_id error")
            traceback.print_exc()

    def update_is_used(self, unique_key):
        """
        更新is_used
        """
        try:
            update_sql = "update {} set is_used=1 where unique_key='{}'".format(self.article, unique_key)
            connection = self.article_crawl_pool.connection()
            self.base_store.update(update_sql, connection)
        except:
            traceback.print_exc()

    def reset_article(self, unique_key, article_id):
        """
        将原数据库的文章改为文章系统中对应的article_id
        """
        try:
            update_sql = "update {} set article_source='article_id:{}' where unique_key='{}'".format(self.article, article_id,
                                                                                      unique_key)
            connection = self.article_crawl_pool.connection()
            self.base_store.update(update_sql, connection)
        except:
            traceback.print_exc()

    def insert_article(self, article):
        """
        插入文章
        """
        try:
            connection = self.article_db_pool.connection()
            article_data = {
                'keyword': article[1],
                'media': article[2],
                'title': article[3],
                'content': article[4],
                'create_time': article[5]
            }
            keys = ','.join(article_data.keys())
            values = ','.join(['%s'] * len(article_data))
            insert_sql = 'insert ignore into {table}({keys}) values ({values})'.format(table=self.article,
                                                                                       keys=keys,
                                                                                       values=values)
            self.base_store.insert(insert_sql, article_data, connection)
        except:
            print("insert_article error")
            traceback.print_exc()


if __name__ == '__main__':
    save = SaveArticleStore()
    # save.query_article()
    # save.query_last_id()
    save.reset_article('asdfvaaaaaa', 13)