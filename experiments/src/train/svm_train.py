import common
from sklearn.svm import LinearSVC
from sklearn.model_selection import KFold
from other.other_utils import beep
from data_processing.data_utils import prepare_data_4_training
from evaluation.imbalanced_evaluation import fscore
from prediction.prediction import predict_complained_users_id


def linear_kernel():
    beep()
    X, y = prepare_data_4_training(features_file='../../data/3月用户相关数据.csv',
                                   label_file='../../data/3月被投诉用户.csv')
    k_fold = KFold(n_splits=2, shuffle=True)
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


def main():
    linear_kernel()


if __name__ == '__main__':
    main()
