import joblib
import numpy as np
from config import pkl_dir
from etl.data_processing import prepare_data_4_prediction


def _load_model(collection, model_name):
    file_dir = pkl_dir + collection + '/'
    pkl_file_name = collection + '_' + model_name + '.pkl'
    pkl_file_name = file_dir + pkl_file_name
    model = joblib.load(pkl_file_name)
    return model


def pred_complained_users(trained_collection_name, X_pred, model_name):
    """
    :param X_pred: 预测数据
    :param trained_collection_name: 训练集名称
    :param model_name: 模型名称
    :return:pandas.DataFrame
    """
    model = _load_model(collection=trained_collection_name, model_name=model_name)
    X = prepare_data_4_prediction(X_pred)
    y_pred = model.predict(X)
    # indices_complained_users = np.where(y_pred == 1)
    X_pred['labels'] = y_pred
    complained_users = X_pred[(X_pred['labels'] == 1)]
    return complained_users
