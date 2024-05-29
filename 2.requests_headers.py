
import requests

url = 'https://www.baidu.com'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

response1 = requests.get(url, headers=headers)

print(len(response1.content.decode()))
print(response1.content.decode())