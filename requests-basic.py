import requests

url = 'https://www.baidu.com'

response = requests.get(url)

# response.encoding = 'utf-8'
# print(response.text)

print(len(response.content.decode()))
print(response.content.decode())