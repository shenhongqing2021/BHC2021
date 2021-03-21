'''
HOMEWORK_6 时间序列预测
PM 沈洪庆
工号 67989
'''

'''####################################### 模块导入 ###########################################'''
import pandas as pd
import datetime
from matplotlib import pyplot as plt
from statsmodels.tsa.arima_model import ARMA,ARIMA




'''####################################### 类与函数定义 #######################################'''



'''####################################### 主程序 ############################################# '''

# 初始化设定
pd.set_option('display.unicode.east_asian_width', True,
              'display.max_columns', 200,
              'display.max_rows', 500,
              'display.width', 200)

# 第一步：从数据集：jetrail.csv获取数据
data_raw = pd.read_csv('train.csv', header=0)
print(data_raw)

# 第二步：对数据做简单检查与预处理
# 日期处理
datetime_pre = data_raw['Datetime'].tolist()
datetime_pre = [datetime.datetime.strptime(value[:-6], '%d-%m-%Y') for value in datetime_pre]  # 日期
data_ready = data_raw
data_ready['Datetime'] = datetime_pre
data_ready = data_ready[['Datetime','Count']]
data_ready = data_ready.groupby(by='Datetime').sum()
# 数据预览
'''
x = data_ready.index
y = data_ready['Count']
plt.plot(x,y)
plt.show()
'''
# 选取最近的365天作为模型训练的样本
data_training = data_ready.iloc[-365:,:]
# print(data_training)

# 第三步：建立预测模型，进行数据预测
# 预测时期
datetime1 = data_training.index[-1]
timedelta = datetime.timedelta(days=8)
datetime2 = datetime1 + timedelta

# 创建ARMA/ARIMA模型
model = 'arima'
if model == 'arma':
    arma = ARMA(data_training,(7,0)).fit()
    print('AIC: %0.4lf' %arma.aic)
    predict_y = arma.predict(datetime1, datetime2)

if model == 'arima':
    arima = ARIMA(data_training,(14,1,0)).fit()
    print('AIC: %0.4lf' %arima.aic)
    predict_y = arima.predict(datetime1, datetime2,typ='levels')

# 第四步：预测结果呈现
fig, ax = plt.subplots(figsize=(12, 8))
ax = data_training.Count[data_training.index[0]:].plot(ax=ax)
predict_y.plot(ax=ax)
plt.show()
