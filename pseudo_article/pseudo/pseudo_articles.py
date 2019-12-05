# -*- coding: utf-8 -*-
from pseudo_article.errorCode import ErrorCode
from pseudo_article.pseudo_store.pseudo_article_store import PseudoStore
import time
import json
import requests
import traceback


class PseudoArticle(object):
    """
    1.从数据库表获取原文章;
    2.调用5118接口将原文章转为伪原创文章;
    3.将伪原创文章保存到数据库表.
    """

    def __init__(self):
        self.store = PseudoStore()

    def pseudo_article(self):
        print('-- start to pseudo articles --')
        while True:
            try:
                result = self.store.query_article()
                if result is not None:
                    content = result[5].replace('\'', '\'\'')
                    article_source = 'txt={}&th=3'.format(content)
                    try:
                        response = requests.post(self.store.url_API, data=article_source, headers=self.store.header)
                    except:
                        response = requests.post(self.store.url_API, data=article_source.encode('utf-8'), headers=self.store.header)
                    response_dict = json.loads(response.text)
                    if response_dict['errmsg'] == '':
                        article_pseudo = response_dict['data']  # 伪原创文章
                        if article_pseudo.strip() != '<p>' and article_pseudo.strip() != '':
                            self.store.insert_article(result, article_pseudo)  # 存储伪原创文章
                            self.store.insert_correspond(result[0])  # 存储新-伪文章对应关系
                        self.store.update_last_id(result[0])  # 更新last_id
                        time.sleep(3)
                    else:
                        print(response_dict['errcode'], response_dict['errmsg'])
                        error_code = int(response_dict['errcode'])
                        if error_code in ErrorCode.error_request_num_limit.keys():
                            time.sleep(60 * 30)
                        elif error_code in ErrorCode.error_4xx.keys():
                            self.store.update_last_id(result[0])
                            time.sleep(5)
                        elif error_code in ErrorCode.error_5xx.keys():
                            if "temp_result" in dir() and result == temp_result:
                                self.store.update_last_id(result[0])
                            time.sleep(5)
                        else:
                            time.sleep(5)
                    temp_result = result
                else:
                    time.sleep(60 * 5)
            except:
                print("pseudo_article error")
                traceback.print_exc()


if __name__ == '__main__':
    pseudo_article = PseudoArticle()
    pseudo_article.pseudo_article()
