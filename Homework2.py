# Homework2
# SVW PM 沈洪庆
# 工号：67989

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Action 1： 汽车投诉信息采集

# 变量初始化
url_base = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-1.shtml'  # 起始页
total = 200  # 页面总数
pages = []  # 所有页面

# 第一步：逐页爬取数据
for i in range(total):
    # 生成url
    url = url_base[:-7] + str(i+1) + '.shtml'

    # 获取页面，并生成BS对象
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html = requests.get(url, headers=headers, timeout=100)
    content = html.text
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')

    # 找到完整的投诉信息框
    temp = soup.find('div', class_="tslb_b")
    tr_list = temp.find_all('tr')

    # 获取表头
    tr_list_th = tr_list[0]
    th_list = tr_list_th.find_all('th')
    head = [];
    for th in th_list:
        value = th.contents[0]
        head = head + [value]

    # 获取表内容
    tr_list_td = tr_list[1:]
    content = []
    for tr in tr_list_td:
        td_list = tr.find_all('td')
        record = []
        for i in range(len(td_list)):
            td = td_list[i]
            value = td.contents[0]
            if i in [4]:
                value = value.contents[0]
            if i in [7]:
                value = value['title']
            record = record + [value]
        content = content + [record]

    # 合并页面
    pages = pages + content

# 构建df
df = pd.DataFrame(data=pages, columns=head)


# 第二步：数据预检
# 空值检查
if df.isnull().any().any():
    print('爬取数据中发现空值！')
else:
    print('爬取数据中未发现空值。')

# 重复检查
if df.duplicated().any():
    print('爬取数据中发现重复值！')
else:
    print('爬取数据中未发现重复值。')


# 第三步：保存数据至文件
df.to_excel('spider_data_hm2.xlsx')






