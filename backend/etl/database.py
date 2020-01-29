import pymongo
import json
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
    db = _connect_mongo(host='localhost',port=27017)

    collist = db. list_collection_names()
    if collection in collist:
        return {'result':False,'msg':'名称已存在'}
    db[collection].insert_many(json.loads(user_data))
    return {'result':True,'msg':'上传成功'}
    

def main():
    save_file()

if __name__ == "__main__":
    main()