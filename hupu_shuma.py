# coding:utf-8
import time
import random
import requests
import pandas as pd
from lxml import etree
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager




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
        # 原始话题分类的列表
        self.topic_list = []
        # 按照热度排序后的话题分类列表
        self.heat_list = []


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
        self.heat_list = sorted(self.topic_list, key=lambda x: x['topic_heat'], reverse=True)
        for rank,topic in enumerate(self.heat_list, start=1):
            print(f"热度第{rank}名：{topic['topic_name']}-{topic['topic_type']}-热度值：{topic['topic_heat']}")


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
            temp["reply"] = self.str2int(parse_reply)
            temp["view"] = self.str2int(parse_view)

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

    # 获取单个帖子的楼主发布和回复信息的整合后的内容，整合为docx 或者 txt
    '''
    输出的格式为：
    # 标题：
    
    ## 楼主发布内容：
    
    
    ### 回帖人1：
    @引用内容：（如果有就写这部分，没有就不写）
    
    回帖内容：
    
    ### 回帖人2：
    @引用内容：
    
    回帖内容：
    
    
    '''
    def get_posts(self):
        # post_url = posts_url
        post_url = "https://bbs.hupu.com/626730816.html"
        base_url = post_url.split(".html")[0]

        post_content = self.get_data(post_url)

        html = etree.HTML(post_content.decode())

        # 统计页码总数
        cur_page = 1
        page_count_list = html.xpath("//ul[@class='hupu-rc-pagination']/li[last()-1]/a/text()")
        if len(page_count_list) == 2:
            page_count = int(page_count_list[0])
        else:
            page_count = 1

        post_saved_list = []
        # 提取楼主的原帖部分
        op_dict = {}
        reply_owner = html.xpath("//div[@class='index_post-wrapper__IXkg_']")
        owner_name = reply_owner[0].xpath(".//a[@class='post-user_post-user-comp-info-top-name__N3D4w']/text()")
        op_dict['OP-name'] = owner_name[0]
        owner_title = reply_owner[0].xpath(".//span[@class='post-user_post-user-comp-info-bottom-title__gtj2K']/text()")
        op_dict['OP-title'] = owner_title[0]
        # 这里的正文内容返回的是多行的P的列表，需要重新拼接
        owner_details = reply_owner[0].xpath(".//div[@class='thread-content-detail']/p/text()")
        op_dict['OP-content'] = "\n".join(owner_details)
        #print(op_dict)
        post_saved_list.append(op_dict)

        while True:
            # 提取回帖部分
            reply_array = html.xpath("//div[@class='post-reply-list_post-reply-list-wrapper__o4_81 post-reply-list-wrapper']")
            for reply_item in reply_array:
                reply_dict = {}
                # 抓取回帖人昵称
                reply_name = reply_item.xpath(".//div[@class='user-base-info']/a/text()")
                reply_dict['RP-name'] = reply_name[0]
                # 抓取引用人昵称
                reply_quote_name = reply_item.xpath(".//div[@class='index_quote-text__HggrH']/span/a/text()")
                # 抓取引用内容
                reply_quote_content = reply_item.xpath(".//div[@class='index_simple-detail-content__3FPFA']/p/text()")
                if len(reply_quote_name) > 0:
                    reply_dict['QT-name'] = reply_quote_name[0]
                    reply_dict['QT-content'] = reply_quote_content[0]
                else:
                    reply_dict['QT-name'] = ''
                    reply_dict['QT-content'] = ''
                # 抓取回帖内容
                reply_content = reply_item.xpath(
                    ".//div[@class='post-reply-list-content']//div[@class='thread-content-detail']/p/text()")
                reply_dict['RP-content'] = "\n".join(reply_content)
                # 获取完毕后,保存近最终列表
                post_saved_list.append(reply_dict)
            # 翻下一页，然后判断是否超出总的页码
            cur_page += 1
            if cur_page <= page_count:
                post_url = base_url + '-' + str(cur_page) + ".html"
                post_content = self.get_data(post_url)
                html = etree.HTML(post_content.decode())
            else:
                print(post_saved_list)
                print(f"已抓取{--cur_page}页，抓取结束")
                break








        # # 提取回帖部分
        # reply_array = html.xpath("//div[@class='post-reply-list_post-reply-list-wrapper__o4_81 post-reply-list-wrapper']")
        # for reply_item in reply_array:
        #     reply_dict = {}
        #     # 抓取回帖人昵称
        #     reply_name = reply_item.xpath(".//div[@class='user-base-info']/a/text()")
        #     reply_dict['RP-name'] = reply_name[0]
        #     # 抓取引用人昵称
        #     reply_quote_name = reply_item.xpath(".//div[@class='index_quote-text__HggrH']/span/a/text()")
        #     # 抓取引用内容
        #     reply_quote_content = reply_item.xpath(".//div[@class='index_simple-detail-content__3FPFA']/p/text()")
        #     if len(reply_quote_name) > 0:
        #         reply_dict['QT-name'] = reply_quote_name[0]
        #         reply_dict['QT-content'] = reply_quote_content[0]
        #     else:
        #         reply_dict['QT-name'] = ''
        #         reply_dict['QT-content'] = ''
        #     # 抓取回帖内容
        #     reply_content = reply_item.xpath(".//div[@class='post-reply-list-content']//div[@class='thread-content-detail']/p/text()")
        #     reply_dict['RP-content'] = "\n".join(reply_content)
        #
        #
        #
        #     print(reply_dict)



if __name__ == '__main__':
    hupu = Hupu()
    response = hupu.get_posts()


