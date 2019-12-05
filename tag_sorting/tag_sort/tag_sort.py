# -*- coding: utf-8 -*-
from tag_sorting.errorCode import ErrorCode
from tag_sorting.tag_store.tag_sort_store import TagStore
from tag_sorting.util.basic_util import BasicUtil
import time
import json
import requests
import traceback


class TagSort(object):
    """
    原文章和伪原创文章tag的分类和检索:
    1.使用百度API获取文章的标签;
    2.存储标签;
    3.存储文章和标签的对应关系.
    """

    def __init__(self):
        self.util = BasicUtil()
        self.store = TagStore()

    def tag_sort_article(self):
        """
        标签分拣
        """
        while True:
            try:
                result = self.store.query_article()
                if result is not None:
                    data = {
                        "title": result[1],
                        "content": result[2]
                    }
                    print("article id: {}".format(result[0]))
                    response = requests.post(url=self.util.baidu_API, data=json.dumps(data), headers=self.util.header)
                    response_dict = json.loads(response.text)

                    # 如果Access token失效或过期,就重新获取
                    if "Access token invalid or no longer valid" in response_dict.values() or \
                            "Access token expired" in response_dict.values():
                        self.util.access_token = self.util.get_access_token
                        continue
                    if "error_code" not in response_dict.keys():
                        items = response_dict['items']
                        for item in items:
                            self.store.insert_tag(item['tag'])
                            self.store.insert_tagid_score(result[0], item['tag'], item['score'])
                        self.store.update_last_id(result[0])
                        time.sleep(0.5)
                    else:
                        print("Visit API ERROR!")
                        print("error_code: {}, error_msg: {}".format(response_dict['error_code'], response_dict['error_msg']))
                        error_code = int(response_dict['error_code'])
                        if error_code in ErrorCode.error_request_num_limit.keys():
                            time.sleep(60 * 30)
                        elif error_code in ErrorCode.error_4xx.keys():
                            self.store.update_last_id(result[0])
                            time.sleep(2)
                        elif error_code in ErrorCode.error_5xx.keys():
                            if "temp_result" in dir() and result == temp_result:
                                self.store.update_last_id(result[0])
                            time.sleep(2)
                        else:
                            time.sleep(2)
                    temp_result = result
                else:
                    time.sleep(60 * 5)
            except:
                print("tag_sorting error")
                traceback.print_exc()
                time.sleep(3)


if __name__ == '__main__':
    tag_sorting = TagSort()
    tag_sorting.tag_sort_article()
    # tag_sorting.reget_access_token()
    # tag_sorting.query_tag_id('seo')