import pymongo,json,time,os
from  api.logger import log
from pandas import DataFrame
def _connect_mongo(host, port, username=None, password=None,db='phone-number-prober'):
    """ A util for making a connection to mongo """
    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = pymongo.MongoClient(mongo_uri)
    else:
        conn = pymongo.MongoClient(host, port)
    return conn[db]
# client = pymongo.MongoClient('mongodb://localhost:27017/')
# db = client['phone-number-prober']
# print(collist)
def save_file(collection,user_data):
    start = time.time()
    db = _connect_mongo(host='localhost',port=27017)

    collist = db.list_collection_names()
    if collection in collist:
        return {'result':500,'msg':'上传失败名称已存在'}
    db[collection].insert_many(json.loads(user_data))
    end = time.time()
    log("上传文件到数据库成功，花费时间："+str(end-start))
    return {'result':200,'msg':'上传成功'}

def load_data(collection):
    db = _connect_mongo(host='localhost',port=27017)
    user_data = DataFrame(list(db[collection].find()))
    return user_data

def get_collection_names():
    db = _connect_mongo(host='localhost',port=27017)
    collections = db.list_collection_names()
    results = []
    for collection in collections:
        result = {collection:db[collection].find().count()}
        results.append(result)
    return results
