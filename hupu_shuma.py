# coding:utf-8
import time
import random
import requests
from lxml import etree

class Hupu(object):
    def __init__(self):
        self.url = "https://bbs.hupu.com/73-postdate"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }
        self.page_num = 1
        self.data_list = []
    def get_data(self,url):
        response = requests.get(url, headers = self.headers)
        return response.content
    def parse_list_data(self,data):
        html = etree.HTML(data.decode())
        el_list = html.xpath("//div[@class='bbs-sl-web-post-layout']")
        data_list = []
        for el in el_list:
            temp = {}
            parse_title = el.xpath("./div[@class='post-title']/a/text()")
            temp["title"] = parse_title[0]
            parse_link = el.xpath("./div[@class='post-title']/a/@href")
            temp["link"] = "https://bbs.hupu.com" + parse_link[0]
            parse_reply_view = el.xpath("./div[@class='post-datum']/text()")
            temp["reply"] = parse_reply_view[0]
            parse_author = el.xpath("./div[@class='post-auth']/a/text()")
            temp["author_name"] = parse_author[0]
            parse_author_link = el.xpath("./div[@class='post-auth']/a/@href")
            temp["author_link"] = parse_author_link[0]
            parse_post_time = el.xpath("./div[@class='post-time']/text()")
            temp["post_time"] = parse_post_time[0]
            data_list.append(temp)

        # el_list = html.xpath("//div[@class='post-title']/a")
        # data_list = []
        # for el in el_list:
        #     temp = {}
        #     parse_title = el.xpath("./text()")
        #     temp["title"] = parse_title[0]
        #     parse_link = el.xpath("./@href")
        #     temp["link"] = "https://bbs.hupu.com" + parse_link[0]
        #     data_list.append(temp)


        page_count_list = html.xpath("//ul[@class='hupu-rc-pagination']/li[last()-1]/a/text()")

        page_count = int(page_count_list[0])
        print("当前总页码为："+ str(page_count_list))
        if self.page_num <= page_count:
            print(self.page_num)
            self.page_num += 1
        else:
            self.page_num = 0
            return [None,None]
        next_url = self.url + '-' + str(self.page_num)

        return data_list,next_url

    def run(self):
        next_url = self.url

        while True:
            # 发送列表请求，获取网页内容
            list_page_data = self.get_data(next_url)

            # 解析列表页面的响应，提取帖子列表数据和下一页url
            data_list, next_url = self.parse_list_data(list_page_data)

            if data_list == None:
                print("data_list is None")
                print(self.page_num)
                break

            self.data_list += data_list
            time.sleep(random.randint(400, 900)/1000.0)

        print(self.data_list)

if __name__ == '__main__':
    hupu = Hupu()
    response = hupu.run()

