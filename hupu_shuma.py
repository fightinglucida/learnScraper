# coding:utf-8
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

        el_list = html.xpath("//div[@class='post-title']/a")
        data_list = []
        for el in el_list:
            temp = {}
            temp["title"] = el.xpath("//text()")
            print(temp["title"])
            temp["link"] = "https://bbs.hupu.com" + str(el.xpath("//@href"))
            print(temp["link"])
            data_list.append(temp)
        page_count = int(html.xpath("//ul[@class='hupu-rc-pagination']/li[last()-1]/a/text()"))
        if self.page_num < page_count:
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
                break

            self.data_list += data_list

        print(self.data_list)

if __name__ == '__main__':
    hupu = Hupu()
    response = hupu.run()















# url = "https://bbs.hupu.com/73-postdate"
#
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
# }
#
# response = requests.get(url, headers = headers)
#
# html = etree.HTML(response.content.decode())
#
# dict_tweet = {}
#
# print(html.xpath("//div[@class='post-title']/a/text()"))
#
# print(html.xpath("//div[@class='post-title']/a/@href"))

# with open('hupu_shuma_new.html', 'wb') as f:
#     f.write(response.content)