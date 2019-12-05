# coding: utf8
import requests
import json
import tag_sorting.config as config
import traceback


class BasicUtil(object):
    """
    tag分拣的基础util类
    """
    def __init__(self):
        self.access_token = self.get_access_token
        self.baidu_API = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/keyword?charset=UTF-8&access_token={}'.format(
            self.access_token)
        self.header = {"Content-Type": "application/json; charset=UTF-8"}

    @property
    def get_access_token(self):
        """
        从百度API获取access_token
        """
        try:
            AK = config.BAIDU_API_KEY
            SK = config.BAIDU_SECRET_KEY
            url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}&'.format(
                AK, SK)
            header = {"Content-Type": "application/json; charset=UTF-8"}
            response = requests.post(url=url, headers=header)
            content = response.text
            if content is not None:
                content_dict = json.loads(content)
                access_token = content_dict['access_token']
                return access_token
        except:
            print("get_access_token error")
            traceback.print_exc()


if __name__ == '__main__':
    basic_util = BasicUtil()