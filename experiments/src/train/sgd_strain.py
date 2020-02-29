import common
import numpy as np
from collections import Counter
from imblearn.over_sampling import RandomOverSampler
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import KFold, cross_val_score, RandomizedSearchCV

from evaluation.imbalanced_evaluation import pre_rec_fscore
from other.other_utils import beep
from data_processing.data_utils import prepare_data_4_training, prepare_data_4_prediction
import prediction.prediction as pre
from scipy.stats import randint


def sgd():
    beep()
    X_train, y_train = prepare_data_4_training(features_file='../../data/3月用户相关数据.csv',
                                               label_file='../../data/3月被投诉用户.csv')
    X_test, y_test, _ = prepare_data_4_prediction(features_file='../../data/4月用户相关数据.csv',
                                                  label_file='../../data/4月被投诉用户.csv')

    clf = SGDClassifier(max_iter=10000, class_weight='balanced', loss="log")

    clf.fit(X_train, y_train)

    y_pred_train = clf.predict(X_train)
    y_pred_test = clf.predict(X_test)

    pre.threshold_pred(model=clf, threshold=0.3, X=X_train, y=y_train)
    # eva_train = pre_rec_fscore(y_actual=y_train, y_predict=y_pred_train)

    pre.threshold_pred(model=clf, threshold=0.6, X=X_test, y=y_test)
    # eva_test = pre_rec_fscore(y_actual=y_test, y_predict=y_pred_test)

    # pre.predict_complained_users_id(clf,
    #                                 features_file_test='../../data/4月用户相关数据.csv',
    #                                 label_file_test='../../data/4月被投诉用户.csv')
    # pre.predict_complained_users_id(clf,
    #                                 features_file_test='../../data/3月用户相关数据.csv',
    #                                 label_file_test='../../data/3月被投诉用户.csv')
    beep()

    print('done')


def main():
    sgd()


if __name__ == '__main__':
    main()
