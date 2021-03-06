import api
import re
import numpy as np
from sklearn import preprocessing
from pandas import DataFrame
from time import time
from logger.logger import log


def z_score(data):
    """
    :param data: pandas.DataFrame
    :return: pandas.DataFrame
    """
    # z-score规范化
    # pandas和numpyn计算std的方式不一样，所以结果有一点出入

    # data = (data - data.mean())/data.std()

    columns = data.columns
    data_np = np.array(data)
    data_scaled = preprocessing.scale(data_np)
    data_df = DataFrame(data_scaled, columns=columns)

    return data_df


def max_min(clean_data):
    # max-min规范化
    pass


def _is_number(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(str(num))
    if result:
        return True
    else:
        return False


def wash_data(user_data):
    start = time()
    user_data.dropna(inplace=True)

    replace_rule = {'0': 0, '1': 1, '公众': 0, '湖南长沙': 1}
    user_data.replace(replace_rule, inplace=True)
    # del_series=user_data.applymap(_is_number).all(1)
    # del_list = [i for i, x in enumerate(del_series) if x == False]
    # user_data.drop(del_list,inplace=True)

    # 剔除含有非数值型数据的行
    del_list = []
    for column in user_data.columns:
        if user_data[column].dtype == "object":
            i = 0
            for val in user_data[column]:
                if not str(val).replace(".", "").isdigit():
                    print("删除列{},第{}行数据：{}".format(column, i,val))
                    del_list.append(i)
                i += 1
    user_data.drop(del_list, inplace=True)
    end = time()
    log("去掉的行数: " + str(len(del_list)))
    log("清洗数据所用时间：" + str(end - start))
    return user_data

# def get_data(collection):
#     try:
#         user_data = load_data(collection)
#         print(user_data)
#         res = {'result':200,'data':user_data.to_json()}
#     except BaseException as e:
#         print('exception:',e)
#         res = {'result':500,'data':None}
#     finally:
#        return res
