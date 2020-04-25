import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import PolynomialFeatures

from visualization.d3 import draw_3d
from data_processing.data_utils import get_clean_raw_data, num_features
from data_processing.dimension_reduction import features_extraction_3d
from data_processing.imbalance_handle import imbalanced_handle
from evaluation.imbalanced_evaluation import roc_auc, fscore


def _prepare_data_4_training(features_file=None, label_file=None):
    """
    注意处理顺序
    :param features_file:
    :param label_file:
    :return:
    """
    raw_data = get_clean_raw_data(features_file=features_file,
                                  label_file=label_file)
    X = np.array(raw_data[num_features])
    y = np.array(raw_data['label'])

    # imbalanced data processing
    X_sample, y = imbalanced_handle(X, y)

    # 降维
    X_extract = features_extraction_3d(X_sample)

    X_final = X_extract

    return X_final, y


def _prepare_data_4_prediction(features_file=None, label_file=None):
    """
    预测不需要处理imbalanced data，所以要和prepare_data_4_training分开
    :param features_file:
    :param label_file:
    :return:
    """
    raw_data = get_clean_raw_data(features_file=features_file,
                                  label_file=label_file)
    X = np.array(raw_data[num_features])
    y = np.array(raw_data['label'])

    # 降维
    X_extract = features_extraction_3d(X)

    X_scaled = preprocessing.scale(X_extract)

    users_id = np.array(raw_data['user_id'])

    X_final = X_scaled
    return X_final, y, users_id


def inspect():
    X, y, users_id = _prepare_data_4_prediction(features_file='../../data/4月用户相关数据.csv',
                                                label_file='../../data/4月被投诉用户.csv')

    X_anomal = X[np.where(y == 1)]
    X_normal = X[np.where(y == 0)]
    # print(np.max(X_anomal))
    # print(np.max(X_normal))
    #
    # print(np.min(X_anomal))
    # print(np.min(X_normal))
    print(np.shape(X_normal))
    print(X_anomal)
    draw_3d(X_normal, X_anomal)


def anomaly_detection():
    X_train, y_train = _prepare_data_4_training(features_file='../../data/3月用户相关数据.csv',
                                                label_file='../../data/3月被投诉用户.csv')
    X_test, y_test, _ = _prepare_data_4_prediction(features_file='../../data/4月用户相关数据.csv',
                                                   label_file='../../data/4月被投诉用户.csv')
    m_train, n = np.shape(X_train)
    mu = np.sum(X_train, 0) / m_train
    delta = X_train - mu
    sigma2 = np.sum(np.square(delta), 0) / m_train
    m_test = np.shape(X_test)[0]
    p = np.zeros(m_test)
    for i in range(m_test):
        x = X_test[i, :]
        coe = np.sqrt(2 * np.pi) * np.sqrt(sigma2)
        delta2 = np.square(x - mu)
        k = np.exp(-delta2 / 2 / sigma2) / coe
        p[i] = np.prod(k)

    indices = np.where(y_test == 1)
    # print(p)
    # print('indies: ',p[indices])
    y_pre = np.zeros(m_test)
    threshold = 3.5e-014
    for i, pi in enumerate(p):
        if pi < threshold:
            y_pre[i] = 1
    fscore(y_actual=y_test, y_predict=y_pre)
    roc_auc(y_actual=y_test, y_score=p)


if __name__ == '__main__':
    anomaly_detection()
