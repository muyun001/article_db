# -*- coding: utf-8 -*-
import traceback


class BaseStore(object):
    """
    数据库基础操作
    """

    def __init__(self):
        pass

    def query(self, query_sql, connection):
        """
        数据库查询
        """
        try:
            with connection.cursor() as c:
                c.execute(query_sql)
            connection.commit()
            row = c.fetchone()
            return row
        except:
            print("query error")
            traceback.print_exc()

    def update(self, update_sql, connection):
        """
        数据更新
        """
        try:
            with connection.cursor() as c:
                c.execute(update_sql)
            connection.commit()
        except:
            print("update error")
            traceback.print_exc()

    def insert(self, insert_sql, insert_data, connection):
        """
        插入伪原创文章
        """
        try:
            with connection.cursor() as c:
                c.execute(insert_sql, tuple(insert_data.values()))
            connection.commit()
        except:
            print('insert failed')
            traceback.print_exc()


if __name__ == '__main__':
    store = BaseStore()
    # store.query()
