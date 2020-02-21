import common
from sklearn.svm import LinearSVC
from sklearn.model_selection import KFold
from other.other_utils import beep
from data_processing.data_utils import prepare_data_4_model
from evaluation.evaluation import imbalanced_evaluation


def linear_kernel():
    beep()
    X, y, users_id = prepare_data_4_model(features_file='../../data/3月用户相关数据.csv',
                                          label_file='../../data/3月被投诉用户.csv')
    k_fold = KFold(n_splits=2, shuffle=True)
    clf = LinearSVC(max_iter=10000, class_weight={0: 7, 1: 10000})
    for train_indices, test_indices in k_fold.split(X):
        clf.fit(X[train_indices], y[train_indices])
        prediction = clf.predict(X[test_indices])
        print(imbalanced_evaluation(y[test_indices], prediction))
    beep()
    print('done')


def main():
    linear_kernel()


if __name__ == '__main__':
    main()
