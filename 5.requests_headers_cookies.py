# coding:utf-8
import requests

url = 'https://web.okjike.com/'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

# 构建Cookie字典
temp = "_ga=GA1.2.249912192.1715341941; sid=2cd91f0f-e220-4ce3-adcb-2fa6a63ad17f; _gid=GA1.2.1912773023.1716872819; fetchRankedUpdate=1716953826546; _jid=6edfb744733b43ef94c809df306ac83a; x-jike-access-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiVHNoRVFMbWY2YjFRZ1lqSGk0K1wvdlZkZW9wWUZWZ1owY083Y21ZTFZKQ0ZaTENHMXFoZVp0REJLaGoxUEZldkJ1Zjh3ZFJYTE9vaTJnQkUxK3ZpUUNXcldPSytpUG44bFhITlhOSWJrNm5mbTJjbXphVU1FZGNITVJpYnZMNGNNdmdVaVAyQzV2Q2E3VVpiRmRuR2ttSkNFTjBlY2tSa1FVMFl3NEVUSktVaXg4U2tRaHRlQ3hhSkhENytsZzhtXC9IM0FCY0htQ3hYdkd5UXR1RzhlWDRzOWRBb3NOU2x4WlAxUFpMYll2Ymd2NkNrTDVTTUVtZzh1VjJsUjNMYzdES0w3UkZoemU1SFhCa2xubjAyQXJzeThpOGh1VnJiWFRPanhYeXJLbFk4bnRwQ29nRjlQVVdVaGtSYStlU2hCZFFQT2JnUWlPdG5mR1ozUmRXa1BFaGNDdWNSK3hGM3RqaDYzM3Z5MnYrelE9IiwidiI6MywiaXYiOiJ1dDFzTEIwVWtIUHoydGVqOTl0UHBnPT0iLCJpYXQiOjE3MTY5ODA4OTkuMTM4fQ.H_h7xd1qaiQGKas4_KSjwZ2PhqfZlCH5xBjagxaqxto; x-jike-refresh-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoidXFKcjFHanlRSkdcLzVMWHdidXF6dlB6TjBOUkJSV2h4eW1JVDVFWDdrVHBNU1ZLaVBQY2JRVDJvSkdLRWdqSHpQakFHWnpzRk94YUxHb0NNUndFdDQwb2ZUU0kzMTVIcWdFYkhkc1lUa3BBY2JTM1lHUjc5WDNmSEordU1ZUmVpZEx0REJsSittQnE1a0Z2VUhGa3U5VTdcL2MwbmdMcWR4Z2RodEY1UmQ5blE9IiwidiI6MywiaXYiOiJXSDBGaTBrMUptSlRQb2dzazQ1STh3PT0iLCJpYXQiOjE3MTY5ODA4OTkuMTM4fQ.gQXsFSchuXAPN6AT9q_Vh8xP1uttXULbjLLaOKr28i4; _gat=1; _ga_LQ23DKJDEL=GS1.2.1716980904.12.0.1716980904.60.0.0"
cookie_list = temp.split('; ')
cookies = {cookie.split('=')[0]:cookie.split('=')[-1] for cookie in cookie_list}

# cookies = {}
# for cookie in cookie_list:
#     cookies[cookie.split('=')[0]] = cookie.split('=')[-1]

print(cookies)

response = requests.get(url, headers=headers, cookies=cookies)

with open("jikeweb2.html", "wb") as f:
    f.write(response.content)