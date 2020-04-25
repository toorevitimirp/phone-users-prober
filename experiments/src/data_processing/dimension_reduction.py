"""
特征选择,特征提取
"""
import common
import numpy as np
import pandas as pd
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import PCA


def variance_threshold(X, p):
    """移除那些在整个数据集中特征值为0或者为1的比例超过p的特征。试验性函数。
    :param X: 待选择的数据集
    :param p: 阈值
    :return: 选择后的数据集
    """
    print('未进行特征选择的数据形状：{}'.format(X.shape))
    sel = VarianceThreshold(threshold=(p * (1 - p)))
    X_select = sel.fit_transform(X)
    print('特征选择后的数据形状：{}'.format(X_select.shape))

    return X_select


def feature_selection():
    """
    特征选择，试验性函数。
    """
    from data_processing.data_utils import get_clean_raw_data, bool_features, num_features
    raw_data = get_clean_raw_data(features_file='../../data/3月用户相关数据.csv',
                                  label_file='../../data/3月被投诉用户.csv')
    all_features = bool_features+num_features
    p = 0.8
    X = raw_data[num_features]
    variance_threshold(X, p)

    X = raw_data[all_features]
    variance_threshold(X, p)


def pca_num_feature(X):
    """
    pca降维
    :param X: m×n的np.ndarray, 特征集
    :return: m×3的np.ndarray, 降维后的特征集
    """
    print('降维前：{}'.format(X.shape))
    pca = PCA(n_components=3)
    pca.fit(X)
    # print('variance:', pca.explained_variance_)
    # print('variance_ratio:', pca.explained_variance_ratio_)
    X_pca = pca.transform(X)
    print('降维后：{}'.format(X_pca.shape))

    # fig = plt.figure()
    # ax = Axes3D(fig)
    # ax.scatter(X_pca[:, 0], X_pca[:, 1], X_pca[:, 2])
    # plt.show()
    return X_pca


def lda_num_feature(X, y):
    """
    lda算法
    :param
    X: m×n的np.ndarray, 特征集
    :return: m×3
    的np.ndarray, 降维后的特征集
    """
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    print('降维前：{}'.format(X.shape))
    lda = LinearDiscriminantAnalysis(solver='eigen')
    lda.fit(X, y)

    X_lda = lda.transform(X)

    print('降维后：{}'.format(X_lda.shape))

    return X_lda


def features_extraction_3d(X):
    """
    pca降维
    :param y: m×1的np.ndarray, 标签
    :param X: m×n的np.ndarray, 特征集
    :return: m×3的np.ndarray, 降维后的特征集
    """
    # raw_data = get_clean_raw_data(features_file='../../data/3月用户相关数据.csv',
    #                               label_file='../../data/3月被投诉用户.csv')
    # X = raw_data[num_features]
    X_pca = pca_num_feature(X)
    # label = np.array(raw_data['label']).astype('int')
    # df = pd.DataFrame(X_pca)
    # X_extract = df.values

    # X_lda = lda_num_feature(X, y)
    # label = np.array(raw_data['label']).astype('int')
    df = pd.DataFrame(X_pca)
    X_extract = df.values

    return X_extract


# def main():
#     features_extraction_3d()
#
#
# if __name__ == '__main__':
#     main()
