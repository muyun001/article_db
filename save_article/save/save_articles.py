# coding: utf-8
from save_article.save_store.save_article_store import SaveArticleStore
import time
import traceback


class SaveArticle(object):
    """
    从"文章抓取数据库"读取文章,存储到文章系统
    """

    def __init__(self):
        self.store = SaveArticleStore()

    def save_article(self):
        while True:
            try:
                article = self.store.query_article()
                if article is not None:
                    print("article unique_key:", article[0])
                    self.store.insert_article(article)

                    # 将读取后的文章换成对应的article_id
                    article_id = self.store.query_article_id()
                    self.store.reset_article(article[0], article_id)
                else:
                    time.sleep(60)
            except:
                print("save_article error")
                traceback.print_exc()
                time.sleep(3)


if __name__ == '__main__':
    save_article = SaveArticle()
    save_article.save_article()
