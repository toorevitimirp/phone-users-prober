"""
database.py采用的方案是将用户数据存在数据库，由于数据量太大，这种方案io耗时非常大。
现在采用将数据存储在csv文件中的方案
"""
import os
import shutil
import time
import pandas as pd
from config import data_info, csv_dir, model_info, pkl_dir
from api.logger import log
from etl.database import connect_mongo, get_collection_name_list
from api.logger import log
from config import db_port, db_host


db = connect_mongo(host=db_host, port=db_port)


def get_collection_info():
    res = list(db[data_info].find({}, {'_id': 0}))
    return res


def save_data(collection, user_data):
    """
    保存用户数据为csv文件
    :param collection: str，数据集的名字
    :param user_data: pandas.DataFrame, 用户数据
    :return:保存结果
    """
    length = user_data.shape[0]
    columns = list(user_data.columns)
    start = time.time()

    collection_name_list = get_collection_name_list()

    # 检查数据集合名称是否已经存在
    if collection in collection_name_list:
        return {'result': 500, 'msg': '上传失败,名称已存在'}

    try:
        file_name = csv_dir+collection+'.csv'
        user_data.to_csv(file_name, encoding='utf-8')
    except BaseException as e:
        log("exception" + str(e))
        res = {'result': 500, 'msg': '上传失败'}
        return res
    else:
        # 更新元数据集合
        try:
            info = {'name': collection, 'length': length, 'columns': columns, 'trained': 0}
            db[data_info].insert_one(info)
        except BaseException as e:
            log("exception" + str(e))
            db[collection].drop()
            res = {'result': 500, 'msg': '上传失败'}
            return res
        else:
            end = time.time()
            log("上传文件到数据库成功，花费时间：" + str(end - start))

    return {'result': 200, 'msg': '上传成功'}


def load_data(collection):
    """
    :param collection: str,数据集的名称
    :return: pandas.DataFrame
    """
    # 返回一个文档的所有数据
    # 数据上传的时候已经清洗了，不需要再清洗数据
    file_name = csv_dir+collection+'.csv'
    user_data = pd.read_csv(file_name, encoding='utf-8')
    return user_data


def get_complained_users(collection):
    """
    返回被投诉的用户的数据
    :param collection: str,数据集的名称
    :return: pandas.DataFrame
    """
    data_all = load_data(collection)
    grouped = data_all.groupby('label')
    complained_users = grouped.get_group(1)
    return complained_users


def get_series_form_collection(collection, feature):
    """
    返回某个数据集的某一列
    :param collection: str,数据集的名称
    :param feature: str,特征
    :return: pandas.Series
    """
    # cursor = db[collection].find({}, {'_id': 0, feature: 1})
    # data = pd.DataFrame(list(cursor))
    data = load_data(collection)[feature]
    return data


def del_train_info_by_collection_name(name):
    """
    删除数据时，如果数据已经被训练，那么也要删除训练好的模型
    :param name: str,数据集的名字
    :return:
    """
    where = {'collection_name': name}
    trained_models = list(db[model_info].find(where, {'_id': 0}))
    if len(trained_models) > 0:
        try:
            db[model_info].delete_many(where)
            model_file_dir = pkl_dir + name + '/'
            shutil.rmtree(model_file_dir)
        except BaseException as e:
            print('exception:', e)
            success = False
        else:
            success = True
        print('success', success)
    else:
        success = True
    return success


def del_data_by_collection_name(name):

    try:
        query = {'name': name}
        temp = list(db[data_info].find(query))[0]
        db[data_info].delete_one(query)
    except BaseException as e:
        print('exception 0:', e)
        res = {'result': 500, 'msg': '删除数据失败'}
        log('删除数据失败')
    else:
        res = {'result': 200, 'msg': '删除数据成功'}
        try:
            file_name = csv_dir + name + '.csv'
            os.remove(file_name)
            del_train_info_by_collection_name(name)
            log('删除数据集'+name)
        except BaseException as e:
            print('exception 1', e)
            db[data_info].insert_one(temp)
            res = {'result': 500, 'msg': '删除数据失败'}
    finally:
        return res

