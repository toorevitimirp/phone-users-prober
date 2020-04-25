from pyod.models.knn import KNN
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
from sklearn import preprocessing
from data_processing.data_utils import get_clean_raw_data, num_features
from data_processing.dimension_reduction import features_extraction_3d
from evaluation.imbalanced_evaluation import roc_auc, fscore
from sklearn.metrics import precision_score, recall_score, f1_score

from imbalance_handle import imbalanced_handle
from other_utils import beep


def _prepare_data_4_training(features_file=None, label_file=None):
    """
    imbalanced data processing,降维，feature scaling，升维，获得模型训练能够直接用的数据
    注意处理顺序
    :param features_file:
    :param label_file:
    :return:
    """
    raw_data = get_clean_raw_data(features_file=features_file,
                                  label_file=label_file)
    # all_features = num_features + bool_features
    X = np.array(raw_data[num_features])
    y = np.array(raw_data['label'])
    print('特征集文件={},标签文件={}'.format(features_file, label_file))
    print('原始特征维度：', X.shape[1])

    # imbalanced data processing
    # X_sample, y = imbalanced_handle(X, y)
    #
    # # 降维
    # X_extract = features_extraction_3d(X)
    # # print(X_extract)
    #
    # # feature scaling -> 升维 -> feature scaling
    # X_scaled = preprocessing.scale(X_sample)
    # poly = PolynomialFeatures(degree=3)
    # X_poly = poly.fit_transform(X_scaled)
    # X_scaled_poly = preprocessing.scale(X_poly)

    X_final = X
    print('训练的特征维度：', X_final.shape[1])

    # users_id = raw_data['user_id']

    return X_final, y


def _prepare_data_4_prediction(features_file=None, label_file=None):
    """
    降维，feature scaling，升维，获得模型能够直接用的数据
    预测不需要处理imbalanced data，所以要和prepare_data_4_training分开
    :param features_file:
    :param label_file:
    :return:
    """
    raw_data = get_clean_raw_data(features_file=features_file,
                                  label_file=label_file)
    X = np.array(raw_data[num_features])
    y = np.array(raw_data['label'])
    print('特征集文件={},标签文件={}'.format(features_file, label_file))
    print('原始特征维度：', X.shape[1])
    # X_scaled = preprocessing.scale(X)
    # 降维
    # X_extract = features_extraction_3d(X)
    #
    # # feature scaling -> 升维 -> feature scaling
    # X_scaled = preprocessing.scale(X_extract)
    # poly = PolynomialFeatures(degree=3)
    # X_poly = poly.fit_transform(X_scaled)
    # X_scaled_poly = preprocessing.scale(X_poly)
    #
    # X_final = X_scaled_poly
    # print('训练的特征维度：', X_final.shape[1])
    #
    # users_id = np.array(raw_data['user_id'])
    X_final = X
    return X_final, y


def anomaly_detection():
    X_train, y_train = _prepare_data_4_training(features_file='../../data/3月用户相关数据.csv',
                                                label_file='../../data/3月被投诉用户.csv')
    X_test, y_test = _prepare_data_4_prediction(features_file='../../data/4月用户相关数据.csv',
                                                label_file='../../data/4月被投诉用户.csv')
    outlier_fraction = 0.0007
    clf = KNN(contamination=outlier_fraction)
    beep()
    clf.fit(X_train)
    y_pred = clf.predict(X_test)
    beep()
    fscore(y_actual=y_test, y_predict=y_pred)

    f1score = f1_score(y_true=y_test, y_pred=y_pred, average='binary')
    print('f1score:{}'.format(f1score))
    # roc_auc(y_actual=y_test, y_score=y_pred)


def main():
    anomaly_detection()


if __name__ == '__main__':
    main()

