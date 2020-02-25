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
    X, y = prepare_data_4_training(features_file='../../data/3月用户相关数据.csv',
                                            label_file='../../data/3月被投诉用户.csv')
    k_fold = KFold(n_splits=5, shuffle=True)

    # 随机搜索确定class_weight
    # clf = SGDClassifier(max_iter=10000)
    # class_weight_n = 10  # class_weight列表的长度
    # class_weight_0 = np.random.uniform(low=50, high=90, size=(class_weight_n, ))
    # class_weight_1 = np.random.uniform(low=800, high=1200, size=(class_weight_n, ))
    # class_weights = [{0: c0, 1: c1} for c0, c1 in zip(class_weight_0, class_weight_1)]
    # print('class_weights：{}'.format(class_weights))
    # param_grid = {
    #     'class_weight': class_weights
    # }
    # n_iter_search = class_weight_n
    # random_search = RandomizedSearchCV(clf, param_distributions=param_grid,
    #                                    n_iter=n_iter_search, cv=k_fold, scoring='f1')
    # random_search.fit(X, y)
    # print('最佳参数：{}'.format(random_search.best_params_))
    # print('最佳分数：{}'.format(random_search.best_score_))

    # k折叠交叉验证，使用sk-learn的evaluation
    # scores = cross_val_score(clf, X, y, cv=k_fold, scoring='f1')
    # print(scores)

    clf = SGDClassifier(max_iter=10000, class_weight='balanced', loss="log")
    # k折叠交叉验证，使用自己的evaluation
    # for train_indices, test_indices in k_fold.split(X):
    #     print('训练集大小：{},测试集大小：{}'.
    #           format(len(train_indices), len(test_indices)))
    #     clf.fit(X[train_indices], y[train_indices])
    #     prediction = clf.predict(X[test_indices])
    #     pre_rec_fscore(y[test_indices], prediction)

    # 在一个数据集（eg：3月）上训练，预测另一个数据集（eg：4月）上被投诉的用户的id
    clf.fit(X, y)
    # X_test, y_test, user_id = prepare_data_4_prediction(features_file='../../data/4月用户相关数据.csv',
    #                                                     label_file='../../data/4月被投诉用户.csv')
    # pred_proba = clf.predict_proba(X_test)
    # print(pred_proba)
    pre.predict_complained_users_id(clf,
                                    features_file_test='../../data/4月用户相关数据.csv',
                                    label_file_test='../../data/4月被投诉用户.csv')
    # pre.predict_complained_users_id(clf,
    #                                 features_file_test='../../data/3月用户相关数据.csv',
    #                                 label_file_test='../../data/3月被投诉用户.csv')
    beep()

    print('done')


def main():
    sgd()


if __name__ == '__main__':
    main()
