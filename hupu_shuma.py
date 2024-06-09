# coding:utf-8
import time
import random
import requests
import pandas as pd
from lxml import etree
from datetime import datetime

class Hupu_root(object):
    def __init__(self):
        self.rootUrl = "https://bbs.hupu.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }
        self.topic_list = {}
    def get_data(self,url):
        response = requests.get(url, headers=self.headers)
        return response.content

    def parse_topic(self, data):
        html = etree



class Hupu(object):
    def __init__(self):
        self.rootUrl = "https://bbs.hupu.com"
        self.url = "https://bbs.hupu.com/73-postdate"
        self.topic = ""
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }
        self.page_num = 1
        self.data_list = []
        self.topic_list = []
    def get_data(self,url):
        response = requests.get(url, headers = self.headers)
        return response.content
    # 将热度值由字符串值改为整数值
    def str2int(self,stringNumber):
        if 'w' in stringNumber:
            return int(float(stringNumber.replace('w', '')) * 10000)
        return int(stringNumber)
    def parse_topic(self,data):
        html = etree.HTML(data.decode())
        topic_ret = html.xpath("//div[@class='hu-pc-navigation-topic-type-popups']/a")
        print(len(topic_ret))

        topic_list = []
        for topic in topic_ret:
            temp = {}
            topic_type = topic.xpath("../../a/text()")
            temp["topic_type"] = topic_type[0]
            topic_type_url = topic.xpath("../../a/@href")
            temp["topic_type_url"] = self.rootUrl + topic_type_url[0]
            topic_name = topic.xpath("./div[@class='topic-item-name']/text()")
            temp["topic_name"] = topic_name[0]
            topic_url = topic.xpath("./@href")
            temp["topic_url"] = self.rootUrl + topic_url[0]
            topic_heat = topic.xpath("./div[@class='topic-item-heat']/text()")
            temp["topic_heat"] = self.str2int(topic_heat[0])

            topic_list.append(temp)

        self.topic_list = topic_list
        print(self.topic_list)

    def init_topic(self):
        topic_data = self.get_data(self.rootUrl)
        self.parse_topic(topic_data)

    def parse_list_data(self,data):
        html = etree.HTML(data.decode())
        data_list = []

        # 保存话题定义
        if self.topic == "":
            post_topic = html.xpath("//head/title/text()")
            self.topic = post_topic[0].split(" - ")[0]
            print(self.topic)

        # 统计页码总数
        page_count_list = html.xpath("//ul[@class='hupu-rc-pagination']/li[last()-1]/a/text()")
        page_count = int(page_count_list[0])
        if self.page_num <= page_count:
            self.page_num += 1
            next_url = self.url + '-' + str(self.page_num)
        else:
            if page_count == 0:
                next_url = self.url + '-' + str(self.page_num)
                return data_list, next_url
            else:
                self.page_num = 0
                return [None, None]

        # 解析每一条帖子的数据
        el_list = html.xpath("//div[@class='bbs-sl-web-post-layout']")
        for el in el_list:
            temp = {}
            parse_title = el.xpath("./div[@class='post-title']/a/text()")
            temp["title"] = parse_title[0]
            parse_link = el.xpath("./div[@class='post-title']/a/@href")
            temp["link"] = "https://bbs.hupu.com" + parse_link[0]
            parse_reply_view = el.xpath("./div[@class='post-datum']/text()")
            parse_reply, parse_view = parse_reply_view[0].split(' / ')
            temp["reply"] = parse_reply
            temp["view"] = parse_view

            parse_author = el.xpath("./div[@class='post-auth']/a/text()")
            temp["author_name"] = parse_author[0]
            parse_author_link = el.xpath("./div[@class='post-auth']/a/@href")
            temp["author_link"] = parse_author_link[0]
            parse_post_time = el.xpath("./div[@class='post-time']/text()")
            temp["post_time"] = parse_post_time[0]
            data_list.append(temp)
        # 抓取的内容列表数量
        post_list_count = len(el_list)

        # 总结性打印数据
        print(f"下一页：{self.page_num}\n总页码：{page_count_list}\n当前页抓取数据数量：{post_list_count}\n", )
        return data_list,next_url

    def saveData(self, data):
        # 获取当前时间
        current_time = datetime.now()
        # 格式化时间为指定格式
        formatted_time = current_time.strftime("%Y%m%d%H%M")
        filename = self.topic + "_" + formatted_time + ".xlsx"
        print(filename)
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False, engine='openpyxl')

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
        self.saveData(self.data_list)
        print(f"总计爬取并保存数据 {len(self.data_list)} 条")

if __name__ == '__main__':
    hupu = Hupu()
    response = hupu.init_topic()


