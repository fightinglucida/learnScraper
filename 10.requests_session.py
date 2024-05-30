# coding:utf-8
import re

import requests

def login():
    #session
    session = requests.session()


    #headers
    session.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

    # url1 - 获取token
    url1 = "https://github.com/login"
        # 发送请求获取响应
    res_1 = session.get(url1).content.decode()
        # 正则提取
    token = re.findall('name="authenticity_token" value="(.*?)"', res_1)[0]


    #url2 - 登录
    url2 = 'https://github.com/session'
        # 构建表单数据
    data = {
        "commit": "Sign in",
        "utf8": "√",
    #     这里还有很多其他的参数
    }
        # 发送请求登录
    session.post(url2, data=data)

    #url3 - 验证
    url3 = 'https://github.com/'