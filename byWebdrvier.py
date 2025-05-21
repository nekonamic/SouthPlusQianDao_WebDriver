from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
from bs4 import BeautifulSoup
import requests
import time
import os

# 获取系统变量
serverKey = os.environ.get('serverKey')  # 已不再使用
ntfy_url = os.environ.get('ntfyUrl')     # 新的通知地址
cookie_json = os.environ.get('COOKIE')   # Cookie 环境变量

# 解析 COOKIE
if cookie_json:
    try:
        cookie_data = json.loads(cookie_json)
    except json.JSONDecodeError:
        print("错误：无法解析 COOKIE 环境变量为 JSON。")
        cookie_data = []
else:
    print("错误：COOKIE 环境变量未设置。")
    cookie_data = []

# 设置 Chrome 参数
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(r'/usr/local/bin/chromedriver')
web = webdriver.Chrome(service=service, options=chrome_options)

def notify(message):
    """发送通知到 ntfy 服务器"""
    if ntfy_url:
        try:
            requests.post(ntfy_url, data=message.encode('utf-8'))
        except Exception as e:
            print(f"通知发送失败: {e}")
    else:
        print(f"[通知] {message}")

def Lingqu():
    try:
        web.find_element(By.XPATH, '//*[@id="main"]/table/tbody/tr/td[1]/div[2]/table/tbody/tr[3]/td').click()
        time.sleep(2)
        try:
            web.find_element(By.XPATH, '//*[@id="both_15"]/a/img').click()
            print('日常领取成功')
            notify('日常领取成功')
        except:
            print('日常领取失败')
            notify('日常领取失败')

        try:
            web.find_element(By.XPATH, '//*[@id="both_14"]/a/img').click()
            print('周常领取成功')
            notify('周常领取成功')
        except:
            pass
    except:
        print('日常暂未刷新或领取失败')
        notify('日常暂未刷新或领取失败')

# 打开任务页面
url = 'https://www.south-plus.net/plugin.php?H_name-tasks.html.html'
web.get(url)
time.sleep(1)

# 添加 cookies
for cookie in cookie_data:
    web.add_cookie(cookie)

# 重新加载任务页
web.get(url)
time.sleep(3)

soup = BeautifulSoup(web.page_source, 'html.parser')
weekly_task_1 = soup.find('span', id='p_15')
weekly_task_2 = soup.find('span', id='p_14')

print(weekly_task_1, weekly_task_2)

if weekly_task_1 and weekly_task_2:
    web.find_element(By.XPATH, '//*[@id="p_14"]/a/img').click()
    web.find_element(By.XPATH, '//*[@id="p_15"]/a/img').click()
    print('任务已领取')
    notify('日常和周常任务已领取')
    Lingqu()
elif weekly_task_1:
    web.find_element(By.XPATH, '//*[@id="p_15"]/a/img').click()
    notify('只检测到日常任务，已领取')
    Lingqu()
elif weekly_task_2:
    web.find_element(By.XPATH, '//*[@id="p_14"]/a/img').click()
    notify('只检测到周常任务，已领取')
    Lingqu()
else:
    print('任务暂未刷新')
    notify('任务暂未刷新')

web.quit()
