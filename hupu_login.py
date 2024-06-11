# coding:utf-8
import requests


url = "https://passport.hupu.com/v2/login#/"

session = requests.session()

#headers
session.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

res = session.get(url)
print(res.content.decode())