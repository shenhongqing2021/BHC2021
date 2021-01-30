# 黑马训练营作业1
# SVW PM 沈洪庆
# 工号 67989


import pandas as pd

# Action1, 数列求和问题
def sum100():
    a = list(range(2,102,2))
    acc = sum(a)
    print('数列求和结果：', acc)

# Action2, 成绩统计
def score():
    # 构建数据框架df
    key = ['姓名','语文','数学','英语']
    scores = [('张飞', '关羽', '刘备', '典韦', '许褚'),
              (68, 95, 98, 90, 80),
              (65, 76, 86, 88, 90),
              (30, 98, 88, 77, 90)]
    dict_score = dict(zip(key,scores))
    df = pd.DataFrame(dict_score)

    # 数据处理
    df_new = df
    df_new['平均成绩'] = df.iloc[:, 1:4].mean(axis=1)
    df_new['最小成绩'] = df.iloc[:, 1:4].min(axis=1)
    df_new['最大成绩'] = df.iloc[:, 1:4].max(axis=1)
    df_new['方差'] = df.iloc[:, 1:4].var(axis=1)
    df_new['标准'] = df.iloc[:, 1:4].std(axis=1)
    df_new['总成绩'] = df.iloc[:, 1:4].sum(axis=1)


    # 显示结果
    print('成绩统计结果：\n', df)

# Action 3, 质量统计
def qtana():
    # 导入数据
    df = pd.DataFrame()
    df = pd.read_csv('car_complain.csv')
    # df.to_excel('test.xlsx')

    # 数据预处理
    df_temp = df['problem']

    # 逐行获取problem字段
    problems = []

    values = df_temp.values
    for value in values:
        list_value = value.split(',')
        for problem in list_value:
            if ((not problems) or (problem not in problems)) and (problem != '') :
                problems = problems + [problem]

    problems.sort()
    df_add = pd.DataFrame()
    for key in problems:
        df_add[key] = [0 for value in values]

    # 逐行统计problem
    for i in range(len(values)):                    # 行，values
        list_value = values[i].split(',')
        for problem in list_value:                  # 列，values
            for j in range(len(df_add.columns)):   # 列，df_add
                if problem == df_add.columns[j]:
                    df_add.iloc[i,j] = df_add.iloc[i,j] + 1

    # 构建df_merge
    df_new_left = df.iloc[:, 0:5]
    df_new_right = df.iloc[:, 6:]
    df_merge = pd.merge(df_new_left, df_add, right_index=True, left_index=True)
    df_merge = pd.merge(df_merge, df_new_right, right_index=True, left_index=True)

    # 分组统计问题数
    ## 品牌
    df_brand = df_merge.iloc[:,1:].groupby('brand').sum(numeric_only=True) # 分别统计每个问题点数量
    df_brand = df_brand.sum(axis=1)                                        # 所有问题点横向求和
    df_brand.sort_values(ascending=False, inplace=True)                    # 排序

    ## 品牌+车型
    df_brand_model = df_merge.iloc[:, 1:].groupby(['brand', 'car_model']).sum(numeric_only=True)
    df_brand_model = df_brand_model.sum( axis=1)
    df_brand_model.sort_values(ascending=False, inplace=True)

    ## 每个品牌的车型平均投诉数量： 总投诉数/总的车型数量
    list_index = list(df_brand_model.index)                                    # 获取索引
    df_model_index = pd.DataFrame(list_index)                                  # 将索引作为值
    df_model_index['problems'] = df_brand_model.values                         # 增加各车型的问题总数
    df_ave_problem_by_brand = df_model_index.groupby(0).mean()                 # 根据品牌分组求均值
    df_ave_problem_by_brand.sort_values(by='problems', inplace=True, ascending=False) # 排序
    worst_brand = df_ave_problem_by_brand.index[0]

    # 输出结果
    print('各品牌问题总数：\n',df_brand,'\n')
    print('各车型问题总数：\n', df_brand_model,'\n')
    print('各品牌车型的平均问题数量：\n', df_ave_problem_by_brand,'\n')
    print('平均车型投诉最多的品牌：', worst_brand,'\n')
    print('------------------------------------------------Finish--------------------------------------------')


#主程序

#设定打印参数
pd.set_option('display.unicode.east_asian_width', True,
              'display.max_columns', 200,
              'display.max_rows', 1000,
              'display.width', 200)

print('Action1')
sum100()
print('\n')

print('Action2')
score()
print('\n')

print('Action3')
qtana()
print('\n')