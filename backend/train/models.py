import os
import time
import joblib

from sklearn.linear_model import SGDClassifier
from etl.data_processing import prepare_data_4_training
from config import pkl_dir
from etl.database import connect_mongo, update_data_trained
from config import model_info
from logger.logger import log
from evaluation.imbalanced_evaluation import pre_rec_fscore


models = ['sgd']


def _save_model(model, trained_info):

    # 保存训练信息到数据库
    collection = trained_info['collection_name']
    model_file_name = trained_info['pkl_name']
    db = connect_mongo(host='localhost', port=27017)
    db[model_info].insert_one(trained_info)

    # 记录到日志
    log('训练数据：' + str(trained_info))

    # 更新data-info数据库
    update_data_trained(collection, 1)

    # 保存训练模型到文件系统
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

    y_pred = clf.predict(X)
    eva = pre_rec_fscore(y_actual=y, y_predict=y_pred)

    cost_time = end - start
    model_name = 'sgd'
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())[0:10]
    model_file_name = collection + '_' + model_name + '.pkl'

    trained_info = {
        "collection_name": collection,
        "model_name": model_name,
        "pkl_name": model_file_name,
        "cost_time": cost_time,
        "precision": eva["precision"],
        "recall": eva["recall"],
        "f1_score": eva["f1_score"],
        "date": date
    }

    _save_model(model=clf, trained_info=trained_info)
