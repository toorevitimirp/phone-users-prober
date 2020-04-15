from collections import Counter

import numpy as np

from sklearn import preprocessing
from sklearn.preprocessing import PolynomialFeatures

import common
from sklearn.svm import LinearSVC
from sklearn.model_selection import KFold

from data_processing.dimension_reduction import features_extraction_3d
from data_processing.imbalance_handle import imbalanced_handle
from other.other_utils import beep
from data_processing.data_utils import prepare_data_4_training, get_clean_raw_data, num_features
from evaluation.imbalanced_evaluation import fscore
from prediction.prediction import predict_complained_users_id


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

    # 降维
    X_extract = features_extraction_3d(X)

    # imbalanced data processing
    X_sample, y = imbalanced_handle(X_extract, y)

    # print(X_extract)

    # feature scaling -> 升维 -> feature scaling
    X_scaled = preprocessing.scale(X_sample)
    # poly = PolynomialFeatures(degree=3)
    # X_poly = poly.fit_transform(X_scaled)
    # X_scaled_poly = preprocessing.scale(X_poly)

    X_final = X_scaled
    print('最终训练集：', X_final.shape)
    print('最终比例：', Counter(y))

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
    print('原始特征维度：', X.shape)

    # 降维
    X_extract = features_extraction_3d(X)

    # feature scaling -> 升维 -> feature scaling
    X_scaled = preprocessing.scale(X_extract)
    # poly = PolynomialFeatures(degree=3)
    # X_poly = poly.fit_transform(X_scaled)
    # X_scaled_poly = preprocessing.scale(X_poly)

    X_final = X_scaled
    print('最终测试集：', X_final.shape)
    print('最终比例：', Counter(y))
    #
    # users_id = np.array(raw_data['user_id'])

    return X_final, y


def linear_kernel():
    beep()
    X, y = prepare_data_4_training(features_file='../../data/3月用户相关数据.csv',
                                   label_file='../../data/3月被投诉用户.csv')
    # k_fold = KFold(n_splits=2, shuffle=True)
    clf = LinearSVC(max_iter=10000, class_weight={0: 7, 1: 10000})
    # for train_indices, test_indices in k_fold.split(X):
    #     clf.fit(X[train_indices], y[train_indices])
    #     prediction = clf.predict(X[test_indices])
    #     print(pre_rec_fscore(y[test_indices], prediction))
    clf.fit(X, y)
    predict_complained_users_id(clf,
                                features_file_test='../../data/4月用户相关数据.csv',
                                label_file_test='../../data/4月被投诉用户.csv')
    beep()
    print('done')


def high_kernel():
    from sklearn import svm
    beep()
    X_train, y_train = _prepare_data_4_training(features_file='../../data/3月用户相关数据.csv',
                                   label_file='../../data/3月被投诉用户.csv')
    X_test, y_test = _prepare_data_4_prediction(features_file='../../data/3月用户相关数据.csv',
                                   label_file='../../data/3月被投诉用户.csv')

    clf = svm.SVC(kernel='poly')
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    fscore(y_actual=y_test, y_predict=y_pred)
    beep()


def main():
    high_kernel()


if __name__ == '__main__':
    main()
