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


class DecisionTree:

    def __init__(self,
                 features_file_train,
                 label_file_train,
                 features_file_test,
                 label_file_test):
        self.clf = tree.DecisionTreeClassifier(criterion='gini')

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
        if training:
            X, y = imbalanced_handle(X, y)

        # 降维
        # X = features_extraction_3d(X)

        # feature scaling -> 升维 -> feature scaling
        # X = preprocessing.scale(X)
        # poly = PolynomialFeatures()
        # X = poly.fit_transform(X)
        # X = preprocessing.scale(X)

        X_final = X
        print('最终数据集的特征维度：', X_final.shape[1])

        return X_final, y

    def _visual_tree(self):
        import os
        dot_data = tree.export_graphviz(self.clf, out_file='tree.dot')
        os.system('dot -Tpng tree.dot -o tree.png')

    def _print_importances(self):
        if self.X_train.shape[1] == 21:
            features_importances = zip(num_features, self.clf.feature_importances_)
        else:
            features_importances = zip(['f0', 'f1', 'f2'], self.clf.feature_importances_)

        for i in features_importances:
            print(i)

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

    model = DecisionTree(features_file_train=features_file_train,
                         label_file_train=label_file_train,
                         features_file_test=features_file_test,
                         label_file_test=label_file_test)

    model.run()
    print('消耗时间:{}'.format(model.cost_time))


if __name__ == '__main__':
    main()