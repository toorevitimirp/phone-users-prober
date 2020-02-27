import json
import os

import pymongo
import time
from pandas import DataFrame
from logger.logger import log
from config import data_info, model_info, db_host, db_port, pkl_dir


def connect_mongo(host, port, username=None, password=None, db='phone-number-prober'):
    """ A util for making a connection to mongo """
    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = pymongo.MongoClient(mongo_uri)
    else:
        conn = pymongo.MongoClient(host, port)
    return conn[db]


db = connect_mongo(host=db_host, port=db_port)


def save_data(collection, user_data, columns, length):
    start = time.time()
    # print(type(user_data))
    # db = connect_mongo(host='localhost', port=27017)

    collist = db.list_collection_names()
    if collection in collist:
        return {'result': 500, 'msg': '上传失败,名称已存在'}

    # try:
    #     db[collection].insert_many(json.loads(user_data))
    # except BaseException as e:
    #     log("exception",e)
    # else:
    #     info = {}
    #     db[collection].insert_many(json.loads(user_data))
    try:
        db[collection].insert_many(json.loads(user_data))
    except BaseException as e:
        log("exception" + str(e))
        res = {'result': 500, 'msg': '上传失败'}
        return res
    else:
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
    # 返回一个文档的所有数据
    # db = connect_mongo(host='localhost', port=27017)
    user_data = DataFrame(list(db[collection].find()))
    return user_data


def get_complained_users(collection):
    # 返回被投诉的用户的数据
    # db = connect_mongo(host='localhost', port=27017)
    complained_users = DataFrame(list(db[collection].find({'label': 1}, {'_id': 0})))
    return complained_users


def get_series_form_collection(collection, feature):
    # 返回某个数据集的某一列
    # db = connect_mongo(host='localhost', port=27017)
    cursor = db[collection].find({}, {'_id': 0, feature: 1})
    data = DataFrame(list(cursor))

    return data


def get_collection_info():
    # db = connect_mongo(host='localhost', port=27017)
    res = list(db[data_info].find({}, {'_id': 0}))
    return res


def get_collection_name_list():
    """
    获取所有已经存在的数据库的名称
    :return: str list
    """
    # db = connect_mongo(host='localhost', port=27017)
    name_dicts = list(db[data_info].find({}, {'_id': 0, 'name': 1}))
    res = [name_dict['name'] for name_dict in name_dicts]
    return res


def get_train_info_by_model(model):
    """
    根据模型名称获取所有训练信息
    :param model: str,模型名称
    :return: dict list
    """
    # db = connect_mongo(host='localhost', port=27017)
    query = {'model_name': model}
    res = db[model_info].find(query, {'_id': 0})
    return list(res)


def get_train_info_by_model_collection(model, collection):
    """
    根据模型名称和数据集名称获取训练信息
    :param model: str,模型名称
    :param collection:str,数据集名称
    :return: dict
    """
    # db = connect_mongo(host='localhost', port=27017)
    query = {'model_name': model, 'collection_name': collection}
    res = list(db[model_info].find(query, {'_id': 0}))[0]
    return res


def is_trained_model_collection(model_name, collection):
    """
    查询是否已经存在由某个模型（model_name）训练的数据集（collection）
    :param model_name: str，模型名称
    :param collection: str，数据集名称
    :return: bool，是否已经训练
    """
    # db = connect_mongo(host='localhost', port=27017)
    query = {'model_name': model_name, 'collection_name': collection}
    li = list(db[model_info].find(query, {'_id': 0}))
    trained = not (len(li) == 0)
    return trained


def update_data_trained(collection, flag):
    """
    更新data-info中某数据集（collection）的trained为1
    :param flag: 0 or 1
    :param collection: str 数据集的名称
    :return:
    """
    where = {"name": collection}
    update = {"$set": {"trained": flag}}
    # db = connect_mongo(host='localhost', port=27017)
    res = db[data_info].update_one(where, update)


def del_train_info_by_collection_name(name):
    where = {'collection_name': name}
    try:
        db[model_info].delete_many(where)
        model_file = pkl_dir + name + '/'
        os.remove(model_file)
    except BaseException as e:
        print('exception:', e)
        success = False
    else:
        success = True
    return success


def del_data_by_collection_name(name):
    #  应该先删除元数据，这样的话如果元数据删除失败了，恢复数据会比较方便

    try:
        # db = connect_mongo(host='localhost', port=27017)
        query = {'name': name}
        temp = list(db[data_info].find(query))[0]
        db[data_info].delete_one(query)
    except BaseException as e:
        print('exception:', e)
        res = {'result': 500, 'msg': '删除数据失败'}
    else:
        res = {'result': 200, 'msg': '删除数据成功'}
        try:
            db[name].drop()
            del_train_info_by_collection_name(name)
            log('删除数据集' + name)
            res = {'result': 200, 'msg': '删除数据成功'}
        except BaseException as e:
            print('exception', e)
            db[data_info].insert_one(temp)
            res = {'result': 500, 'msg': '删除数据失败'}
    finally:
        return res

