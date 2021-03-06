import numpy as np
from sklearn import preprocessing
from sklearn.ensemble import IsolationForest

from data_processing.data_utils import get_clean_raw_data, num_features
from data_processing.dimension_reduction import features_extraction_3d
from evaluation.imbalanced_evaluation import roc_auc, fscore
from time import time


class IF:
    def __init__(self):
        super()

    def _prepare_data(self, features_file=None,
                      label_file=None):
        raw_data = get_clean_raw_data(features_file=features_file,
                                      label_file=label_file)
        X = np.array(raw_data[num_features])
        y = np.array(raw_data['label'])

        # 降维
        # X_extract = features_extraction_3d(X)

        # X_scaled = preprocessing.scale(X_extract)

        # X_final = X_scaled
        X_final = X
        return X_final, y

    def anomaly_detection(self):
        X_train, y_train = self._prepare_data(features_file='../../data/3月用户相关数据.csv',
                                         label_file='../../data/3月被投诉用户.csv')
        X_test, y_test = self._prepare_data(features_file='../../data/4月用户相关数据.csv',
                                       label_file='../../data/4月被投诉用户.csv')
        # outliers_fraction = 0.0007
        clf = IsolationForest()
        start = time()
        clf.fit(X_train)
        end = time()
        cost_time = end - start
        print('消耗时间:{}'.format(cost_time))
        y_pred = clf.predict(X_test)
        # 孤立森林的预测结果中，-1表示异常，1表示正常
        for i, _ in enumerate(y_pred):
            if _ == -1:
                y_pred[i] = 1
            elif _ == 1:
                y_pred[i] = 0
            else:
                print('预测结果非-1,1')

        fscore(y_actual=y_test, y_predict=y_pred)
        y_score = clf.decision_function(X_test)
        roc_auc(y_actual=y_test, y_score=y_score)


def main():
    model = IF()
    model.anomaly_detection()


if __name__ == '__main__':
    main()