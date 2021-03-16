# Homework_5, 词云展示
# PM 沈洪庆
# 工号 67989

import pandas as pd
from math import isnan
from wordcloud import WordCloud


class MyWC(WordCloud):
    def __init__(self, max_words, width, height):
        super().__init__(max_words=max_words, width=width, height=height)

def clean(data):
    # 去除nan，去除''，去除首尾空格
    m = data.shape[0]
    n = data.shape[1]
    data_raw = data.values
    data_ready = []
    for i in range(m):
        record = data_raw[i]
        temp = []
        for j in range(n):
            value = record[j]
            if (type(value) == str) and (value != ''):
                value = value.strip()
                temp = temp + [value]
            if (type(value) == float) and (not isnan(value)):
                temp = temp + [value]
        if temp:
            data_ready = data_ready + [temp]
    return data_ready

####################################### 主程序 #####################################

# 第一步：导入数据
data_raw = pd.read_csv('Market_Basket_Optimisation.csv', header = None)

# 第二步：数据预处理
data_ready = clean(data_raw)

# 第三步：合并所有商品
all_words = []
for goods in data_ready:
    for good in goods:
        all_words = all_words + [good]

# 第四步: 展示词云
text = ''
for value in all_words:
    text = text + ' ' + value
text = text[1:]
wordcloud = MyWC(100,2000,1200)
wordcloud.generate(text)
wordcloud.to_file("wordcloud.jpg")

# 第五步：分类统计每种商品的数量
amount = [1]*len(all_words)
temp = [all_words, amount]
df = pd.DataFrame(temp).T
df.columns=['关键词', '频率']
results = df.groupby('关键词').sum()
results.sort_values(by='频率', ascending=False, inplace=True)

# 第六步：排名前10的商品名称
df_top10 = results.iloc[range(10),:]
print(df_top10)







