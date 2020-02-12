import pymongo
from pandas import DataFrame

def _connect_mongo(host, port, username=None, password=None, db='phone-number-prober'):
    """ A util for making a connection to mongo """
    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = pymongo.MongoClient(mongo_uri)
    else:
        conn = pymongo.MongoClient(host, port)
    return conn[db]


def get_all_data(collection):
    # 返回一个文档的所有数据
    db = _connect_mongo(host='localhost', port=27017)
    user_data = DataFrame(list(db[collection].find()))
    return user_data


def get_column_form_collection(collection, feature):
    # 返回某个数据集的某一列
    db = _connect_mongo(host='localhost', port=27017)
    cursor = db[collection].find({}, {'_id': 0, feature: 1})
    data = DataFrame(list(cursor))

    return data


