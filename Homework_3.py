# 黑马训练营第3次作业,聚类
# PMKS 沈洪庆
# 工号 67989

# Action：汽车消费城市划分

from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn import preprocessing
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, ward
import pandas as pd

import numpy as np

# kmeans模型
def kmeans(n_clusters,train_x):
    kmeans = KMeans(n_clusters)
    kmeans.fit(train_x)
    predict_y = kmeans.predict(train_x)
    score = kmeans.score(train_x)
    return predict_y, score

################################### 主程序 #######################################


# 第一步：获取外部数据
fn = 'data.xlsx'
data = pd.read_excel(fn)
# 生成df
df = data.iloc[:, 1:]
df.index = data.iloc[:, 0]

# 第二步：相关性分析
print('相关性分析：')
column = df.shape[1]
col_corr=[]
for i in range(column-1):
    a = df.iloc[:, i]
    for j in range(i+1,column):
        b = df.iloc[:, j]
        coff = a.corr(b)
        if abs(coff) > 0.9:
            print(df.columns[i],'与',df.columns[j],'强相关，相关系数：', coff)
        if coff < -0.5:
            print(df.columns[i], '与', df.columns[j], '负相关，相关系数：', coff)

# 第三步： 归一化处理
min_max_scaler = preprocessing.MinMaxScaler()
normal_x = min_max_scaler.fit_transform(df)

gdp = normal_x[:,0]
population = normal_x[:,1]
price = normal_x[:,2]
carpecent = normal_x[:,3]

# 第四步：将强相关的维度进行合并
# 将“GDP”与“城镇人口”两个维度合并为一个新的维度，“城镇化发展水平”，develop
develop = (gdp + population)/2

# 第五步：将负相关的维度做反向处理
# 将“消费价格”指标做反响调整：x=1-x
price = 1-price

# 第六步：构建新的df
df_new = pd.DataFrame()
df_new['develop'] = develop
df_new['price'] = price
df_new['carpecent'] = carpecent

# 第七步：再次归一化
train_x = min_max_scaler.fit_transform(df_new)

# 第八步：手肘法，分析不同k值的聚合误差
range = range(2,10)
score = []
for n_clusters in range:
    # kmeans聚类分析
    # n_clusters = 4
    # predict_y = kmeans(n_clusters,train_x)[0]
    score = score+[kmeans(n_clusters,train_x)[1]]

    # df['聚类结果'] = predict_y
    # df.sort_values(by='聚类结果',inplace=True,ascending=False)
    #
    # pd.set_option('display.unicode.east_asian_width', True,
    #               'display.max_columns', 200,
    #               'display.max_rows', 1000,
    #               'display.width', 200)
    # print(df)
plt.xlabel('K')
plt.ylabel('score')
plt.plot(range, score, 'o-')
plt.show()

# 第九步：选择合适的k值进行聚合分析
# kmeans聚类分析
n_clusters = int(input('请输入需要聚合分类的K值'))
predict_y = kmeans(n_clusters,train_x)[0]
df['聚类结果'] = predict_y
df.sort_values(by='聚类结果',inplace=True,ascending=False)
pd.set_option('display.unicode.east_asian_width', True,
              'display.max_columns', 200,
              'display.max_rows', 1000,
              'display.width', 200)
print('\n',df)






