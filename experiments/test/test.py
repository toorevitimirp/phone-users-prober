import numpy as np
import os
import pandas as pd
import pymongo
import re


def _connect_mongo(host, port, username=None, password=None, db='phone-number-prober'):
    """ A util for making a connection to mongo """
    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = pymongo.MongoClient(mongo_uri)
    else:
        conn = pymongo.MongoClient(host, port)
    return conn[db]


def describe(clean_data):
    descriptions = clean_data.describe()
    descriptions_dic = {}
    # for row in descriptions.itertuples():
    #     print(row)
    # for index, row in descriptions.iteritems():
    #     print(type(row))
    for column in descriptions.columns:
        description = {}
        i = 0
        maps = {1: "mean", 2: "std", 3: "min", 4: "25%", 5: "50%", 6: "75%", 7: "max"}
        # print(descriptions[column])
        for row in descriptions[column]:
            if i:
                description[maps[i]] = row
            i += 1
        descriptions_dic[column] = description
    return escriptions_dic


def _is_number(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(str(num))
    if result:
        return True
    else:
        return False


def test1():
    user_data = pd.read_csv('../实验数据/3月用户相关数据.csv',
                            encoding='utf-8')  # dtype={"users_3w": str,"twolow_users":str})#users_3w,twolow_users存在中文
    complain_users = pd.read_csv('../实验数据/3月被投诉用户.csv', encoding='utf-8')["user_id"]
    # user_data = pd.read_csv('../实验数据/March_features_test.csv',encoding='utf-8')
    # complain_users = pd.read_csv('../实验数据/March_labels_test.csv',encoding='utf-8')["user_id"]
    all_users_id = user_data["user_id"]

    labels = all_users_id.isin(complain_users).astype("int")
    user_data["label"] = labels
    # 剔除含有非数值型数据的行
    del_list = []
    for column in user_data.columns:
        if user_data[column].dtype == "object":
            i = 0
            for val in user_data[column]:
                if (not str(val).isdigit()) and (not i in del_list):
                    del_list.append(i)

                i += 1
    user_data.drop(del_list, inplace=True)
    user_data.dropna(inplace=True)

    describe(user_data)

    # max-min标准化
    # clean_data = (user_data-user_data.min())/(user_data.max()-user_data.min())

    # z-score标准化
    # clean_data = (user_data-user_data.mean())/(user_data.std())  

    # clean_data["label"] = labels
    # clean_data.to_csv('clean_data.csv',index=False,header=False)


def test2():
    user_data = pd.read_csv('/home/toorevitimirp/Desktop/手机用户分类模型/实验数据/March_features_test.csv', encoding='utf-8')
    complain_users = pd.read_csv('/home/toorevitimirp/Desktop/手机用户分类模型/实验数据/March_labels_test.csv', encoding='utf-8')[
        "user_id"]
    all_users_id = user_data["user_id"]
    labels = all_users_id.isin(complain_users).astype("int")
    user_data["label"] = labels


    func_str = 'max'
    func = getattr(user_data['roam_call_duration'],func_str)
    print(func)
        
    # user_data.dropna(inplace=True)
    # print(user_data['roam_users02'])
    # for val in user_data['roam_users02']:
    #     print(str(val).isdigit())
    # del_series = user_data.applymap(_is_number).all(1)
    # del_list = [i for i, x in enumerate(del_series) if x == False]
    # print(del_list)
    # db = _connect_mongo(host='localhost',port=27017)
    # clean_data = wash_data(user_data)


def test3():
    # 转换四月份数据的格式
    user_data = pd.read_csv('/home/toorevitimirp/Desktop/手机用户分类模型/实验数据/4月用户相关数据_gbk.csv', encoding='GB18030')
    width = user_data.shape[1]
    select_cols = [col for col in user_data.columns[0:width-4]]
    user_data = user_data[select_cols]
    user_data.to_csv('/home/toorevitimirp/Desktop/手机用户分类模型/App/4月用户相关数据.csv', encoding='utf-8')
    print(user_data)


def main():
    test3()


if __name__ == "__main__":
    main()
