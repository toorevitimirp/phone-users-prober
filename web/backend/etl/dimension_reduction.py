"""
特征选择,特征提取
"""
import numpy as np
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import PCA


def pca_num_feature(X):
    """
    pca降维
    :param X: m×n的np.ndarray, 特征集
    :return: m×3的np.ndarray, 降维后的特征集
    """
    print('降维前：{}'.format(X.shape))
    pca = PCA(n_components=0.99)
    pca.fit(X)
    print('variance:', pca.explained_variance_)
    print('variance_ratio:', pca.explained_variance_ratio_)
    X_pca = pca.transform(X)
    print('降维后：{}'.format(X_pca.shape))

    return X_pca


def features_extraction_3d(X):
    """
    降维
    :param X: m×n的np.ndarray, 特征集
    :return: m×3的np.ndarray, 降维后的特征集
    """
    X_pca = pca_num_feature(X)
    X_extract = X_pca
    return X_extract
