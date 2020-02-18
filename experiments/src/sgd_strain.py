from collections import Counter
import numpy as np
from imblearn.over_sampling import RandomOverSampler
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_predict, KFold
from other_utils import beep
from data_utils import num_features, bool_features, prepare_data_4_model
from evaluation import imbalanced_evaluation
import prediction as pre


def sampling(X, y):
    """
    上、下采样
    :return:
    """
    print('原始类比例：{}'.format(Counter(y)))

    #  朴素随机过采样
    ros = RandomOverSampler(random_state=0)
    X_over_resampled, y_over_resampled = ros.fit_sample(X, y)
    print('朴素随机过采样后的类比例：{}'.format(Counter(y_over_resampled)))

    # return X_resampled, y_resampled


def sgd():
    beep()
    X, y, user_id = prepare_data_4_model(features_file='../data/3月用户相关数据.csv',
                                         label_file='../data/3月被投诉用户.csv')
    k_fold = KFold(n_splits=5, shuffle=True)
    clf = SGDClassifier(max_iter=10000, class_weight={0: 7, 1: 8000})
    # for train_indices, test_indices in k_fold.split(X):
    #     print('训练集大小：{},测试集大小：{}'.
    #           format(len(train_indices), len(test_indices)))
    #     clf.fit(X[train_indices], y[train_indices])
    #     prediction = clf.predict(X[test_indices])
    #     evaluation = imbalanced_evaluation(y[test_indices], prediction)
    #     get_complained_users_id(prediction, user_id)
    clf.fit(X, y)
    pre.get_complained_users_id(clf,
                                features_file_test='../data/4月用户相关数据.csv',
                                label_file_test='../data/4月被投诉用户.csv')
    beep()

    print('done')


def main():
    sgd()


if __name__ == '__main__':
    main()
