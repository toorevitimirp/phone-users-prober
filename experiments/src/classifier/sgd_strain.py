import common
from sklearn.linear_model import SGDClassifier
import numpy as np
import pandas as pd
from data_processing.data_utils import get_clean_raw_data, num_features
from sklearn import preprocessing
from sklearn.preprocessing import PolynomialFeatures
from data_processing.dimension_reduction import features_extraction_3d
from data_processing.imbalance_handle import imbalanced_handle
from evaluation.imbalanced_evaluation import fscore, roc_auc
from sklearn import tree
from time import time


# def sgd():
#     beep()
#     X_train, y_train = prepare_data_4_training(features_file='../../data/3月用户相关数据.csv',
#                                                label_file='../../data/3月被投诉用户.csv')
#     X_test, y_test, _ = prepare_data_4_prediction(features_file='../../data/4月用户相关数据.csv',
#                                                   label_file='../../data/4月被投诉用户.csv')
#
#     clf = SGDClassifier(max_iter=10000, class_weight='balanced', loss="log")
#
#     clf.fit(X_train, y_train)
#
#     y_score_train = clf.predict_proba(X_train)
#     y_score_test = clf.predict_proba(X_test)
#
#     y_pred_test = clf.predict(X_test)
#     fscore(y_actual=y_test, y_predict=y_pred_test)
#     # roc_auc(y_actual=y_train, y_score=y_score_train[:, 1])
#     roc_auc(y_actual=y_test, y_score=y_score_test[:, 1])
#     # pre.threshold_pred(model=clf, threshold=0.3, X=X_train, y=y_train)
#     # # eva_train = pre_rec_fscore(y_actual=y_train, y_predict=y_pred_train)
#     #
#     # pre.threshold_pred(model=clf, threshold=0.6, X=X_test, y=y_test)
#     # eva_test = pre_rec_fscore(y_actual=y_test, y_predict=y_pred_test)
#
#     # pre.predict_complained_users_id(clf,
#     #                                 features_file_test='../../data/4月用户相关数据.csv',
#     #                                 label_file_test='../../data/4月被投诉用户.csv')
#     # pre.predict_complained_users_id(clf,
#     #                                 features_file_test='../../data/3月用户相关数据.csv',
#     #                                 label_file_test='../../data/3月被投诉用户.csv')
#     beep()
#
#     print('done')

class SGD:
    def __init__(self,
                 features_file_train,
                 label_file_train,
                 features_file_test,
                 label_file_test):
        self.clf = SGDClassifier(class_weight='balanced', loss="log")

        self.cost_time = -1

        self.features_file_train = features_file_train
        self.label_file_train = label_file_train
        self.features_file_test = features_file_test
        self.label_file_test = label_file_test

        self.X_train, self.y_train = self._prepare_data(training=True)
        self.X_test, self.y_test = self._prepare_data(training=False)

    def _prepare_data(self, training=True):
        raw_data = get_clean_raw_data(features_file=self.features_file_train,
                                      label_file=self.label_file_train)
        # all_features = num_features + bool_features
        X = np.array(raw_data[num_features])
        y = np.array(raw_data['label'])
        print('原始特征维度：', X.shape[1])

        # imbalanced data processing
        # if training:
        #     X, y = imbalanced_handle(X, y)

        # 降维
        X = features_extraction_3d(X)

        # feature scaling -> 升维 -> feature scaling
        # X = preprocessing.scale(X)
        # poly = PolynomialFeatures()
        # X = poly.fit_transform(X)
        # X = preprocessing.scale(X)

        X_final = X
        print('最终数据集的特征维度：', X_final.shape[1])

        return X_final, y

    def run(self):
        start = time()
        self.clf.fit(self.X_train, self.y_train)
        end = time()
        self.cost_time = end - start
        y_score_test = self.clf.predict_proba(self.X_test)

        y_pred_test = self.clf.predict(self.X_test)

        roc_auc(y_actual=self.y_test, y_score=y_score_test[:, 1])
        fscore(y_actual=self.y_test, y_predict=y_pred_test)

        # self._print_importances()
        # self._visual()


def main():
    features_file_train = '../../data/3月用户相关数据.csv'
    label_file_train = '../../data/3月被投诉用户.csv'
    features_file_test = '../../data/4月用户相关数据.csv'
    label_file_test = '../../data/4月被投诉用户.csv'

    model = SGD(features_file_train=features_file_train,
                label_file_train=label_file_train,
                features_file_test=features_file_test,
                label_file_test=label_file_test)

    model.run()
    print('消耗时间:{}'.format(model.cost_time))


if __name__ == '__main__':
    main()