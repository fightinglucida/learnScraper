# coding:utf-8
import requests

url = "https://bbs.hupu.com/73"

headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

#print(response.content.decode())

print(response.cookies)

print(response.request.headers)