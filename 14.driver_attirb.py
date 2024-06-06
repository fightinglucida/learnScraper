# coding:utf-8
from selenium import webdriver

url = 'https://www.baidu.com'

#创建一个浏览器对象
driver = webdriver.Chrome()

driver.get(url)

print(driver.page_source)

