import imblearn.ensemble as ens
import numpy as np
from data_utils import num_features
from sklearn import preprocessing
from sklearn.preprocessing import PolynomialFeatures
from data_processing.dimension_reduction import features_extraction_3d
from data_processing.data_utils import get_clean_raw_data, prepare_data_4_prediction
from evaluation.imbalanced_evaluation import fscore
from other_utils import beep


def _prepare_data_4_enesemble(features_file, label_file):
    raw_data = get_clean_raw_data(features_file=features_file, label_file=label_file)

    X = np.array(raw_data[num_features])
    y = np.array(raw_data['label'])
    print('特征集文件={},标签文件={}'.format(features_file, label_file))
    print('原始特征维度：', X.shape[1])

    # 降维
    X_extract = features_extraction_3d(X)

    # feature scaling -> 升维 -> feature scaling
    X_scaled = preprocessing.scale(X_extract)
    poly = PolynomialFeatures(degree=3)
    X_poly = poly.fit_transform(X_scaled)
    X_scaled_poly = preprocessing.scale(X_poly)

    X_final = X_scaled_poly
    print('训练的特征维度：', X_final.shape[1])

    return X_final, y


def ensemble(model, features_file_train, label_file_train,
             features_file_test, label_file_test):
    from sklearn.metrics import balanced_accuracy_score
    from sklearn.ensemble import BaggingClassifier
    from sklearn.tree import DecisionTreeClassifier
    beep()
    X_test, y_test, users_id = prepare_data_4_prediction(features_file=features_file_test,
                                                         label_file=label_file_test)
    X, y = _prepare_data_4_enesemble(features_file=features_file_train, label_file=label_file_train)
    bc = BaggingClassifier(base_estimator=DecisionTreeClassifier(),
                           random_state=0)

    # model.fit(X, y)
    # y_pred = model.predict(X_test)
    # pre_rec_fscore(y_actual=y_test, y_predict=y_pred)

    bc.fit(X, y)

    y_pred = bc.predict(X_test)
    print(balanced_accuracy_score(y_test, y_pred))
    fscore(y_actual=y_test, y_predict=y_pred)
    beep()


def main():
    features_file_train = '../../data/3月用户相关数据.csv'
    label_file_tran = '../../data/3月被投诉用户.csv'
    features_file_test = '../../data/4月用户相关数据.csv'
    label_file_test = '../../data/4月被投诉用户.csv'
    models = ["BalancedBaggingClassifier", "BalancedRandomForestClassifier",
              "EasyEnsembleClassifier", "RUSBoostClassifier"]
    model = ens.BalancedRandomForestClassifier()
    ensemble(
        model=model,
        features_file_train=features_file_train,
        label_file_train=label_file_tran,
        features_file_test=features_file_test,
        label_file_test=label_file_test
    )


if __name__ == '__main__':
    main()
