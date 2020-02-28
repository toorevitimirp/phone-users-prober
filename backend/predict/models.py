import joblib

from config import pkl_dir
from etl.data_processing import prepare_data_4_prediction
from evaluation.imbalanced_evaluation import pre_rec_fscore


def _load_model(collection, model_name):
    file_dir = pkl_dir + collection + '/'
    pkl_file_name = collection + '_' + model_name + '.pkl'
    pkl_file_name = file_dir + pkl_file_name
    model = joblib.load(pkl_file_name)
    return model


def pred_complained_users(trained, pred, model_name):
    """
    :param trained: 训练集
    :param pred: 测试集
    :param model_name: 模型名称
    :return:
    """
    model = _load_model(collection=trained, model_name=model_name)
    X, y, _ = prepare_data_4_prediction(pred)
    y_pred = model.predict(X)
    eva = pre_rec_fscore(y_actual=y, y_predict=y_pred)
    return eva