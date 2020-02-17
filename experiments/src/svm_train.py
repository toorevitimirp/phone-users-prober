import numpy as np
from sklearn import preprocessing
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_predict, KFold
from data import get_all_data
from utils import num_features, bool_features
from evaluation import imbalanced_evaluation

def prepare_data():
    raw_data = get_all_data()
    # raw_data = get_all_data(
    #     features_file='../data/March_features_test.csv',
    #     label_file='../data/March_labels_test.csv')
    all_features = num_features + bool_features
    print(all_features)
    X = np.array(raw_data[all_features])
    y = np.array(raw_data['label'])
    X_scaled = preprocessing.scale(X)
    return X_scaled, y


def linear_kernel():
    X, y = prepare_data()
    k_fold = KFold(n_splits=2, shuffle=True)
    clf = LinearSVC()
    for train_indices, test_indices in k_fold.split(X):
        clf.fit(X[train_indices], y[train_indices])
        prediction = clf.predict(X[test_indices])
        print(imbalanced_evaluation(y[test_indices], prediction))
    print('done')


def main():
    linear_kernel()


if __name__ == '__main__':
    main()
