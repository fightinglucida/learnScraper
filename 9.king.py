# coding:utf-8
import requests
import json

class King(object):
    def __init__(self, word):
        self.url = ''
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }
        self.data = {
            "f":"auto",
            "t":"auto",
            "w":word
        }

    def get_data(self):
        response = requests.post(self.url, data=self.data)
        return response.content

    def parse_data(self,data):
        dict_data = json.loads(data)
        print(dict_data['content']['out'])
    def run(self):
        # 编写爬虫逻辑
        # url
        # headers
        # data字典
        # 发送请求获取响应
        response = self.get_data()
        # print(response)
        # 数据解析，json
        self.parse_data(response)

if __name__ == "__main__":
    king = King('字典')
    king.run()

    # 这个域名已经变化了，需要重新调整整个数据结构