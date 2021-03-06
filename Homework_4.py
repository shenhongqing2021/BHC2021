# Homework_4, 关联分析
# PM 沈洪庆
# 工号 67989


from efficient_apriori import apriori
import pandas as pd
from math import isnan


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

# 第三步：关联分析
# 挖掘频繁项集和频繁规则
itemsets, rules = apriori(data_ready, min_support=0.01,  min_confidence=0.5)


# 第四步：输出分析结果
print("原始数据：")
for value in data_ready:
    print(value)

print("频繁项集：")
print(itemsets)

print("关联规则：")
for value in rules:
    print(value)
