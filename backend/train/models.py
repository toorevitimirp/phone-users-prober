import os

from sklearn.linear_model import SGDClassifier
from etl.data_processing import prepare_data_4_training
from config import pkl_dir
from etl.database import connect_mongo, update_data_trained
from config import model_info
from logger.logger import log
import time
import joblib


models = ['sgd']


def _save_model(model, model_name, collection, cost_time, date):

    # 保存训练信息到数据库
    model_file_name = collection + '_' + model_name + '_' + date + '.pkl'
    db = connect_mongo(host='localhost', port=27017)
    trained_one = {
        "collection_name": collection,
        "model_name": model_name,
        "pkl_name": model_file_name,
        "cost_time": cost_time,
        "date": date
    }
    # 记录到日志
    log('训练数据：' + str(trained_one))

    db[model_info].insert_one(trained_one)

    # 更新data-info数据库
    update_data_trained(collection, 1)

    # 保存训练模型
    file_dir = pkl_dir + collection + '/'
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    model_file_name = file_dir + model_file_name
    joblib.dump(model, model_file_name)


def sgd_classifier(collection):
    X, y = prepare_data_4_training(collection)

    start = time.time()
    clf = SGDClassifier(max_iter=10000, class_weight='balanced', loss="log")
    clf.fit(X, y)
    end = time.time()
    print('done')

    cost_time = end - start
    model_name = 'sgd'
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())[0:9]
    _save_model(model=clf, model_name=model_name,
                collection=collection, cost_time=cost_time,
                date=date)
