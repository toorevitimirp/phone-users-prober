import common
import numpy as np
import pandas as pd

# def get_complained_users_id(y_prediction, user_id):
#     y_prediction = np.array(y_prediction)
#     user_id = np.array(user_id)
#
#     indices = np.where(y_prediction == 1)
#     complained_users_id = user_id[indices]
#     # print(complained_users_id)
#     return complained_users_id
from data_processing.data_utils import prepare_data_4_prediction
from evaluation.imbalanced_evaluation import pre_rec_fscore


def predict_complained_users_id(model,
                                features_file_test=None,
                                label_file_test=None):
    X_test, y_test, users_id = prepare_data_4_prediction(
        features_file=features_file_test,
        label_file=label_file_test
    )

    indices_comp_id_real = np.where(y_test == 1)
    indices_comp_id_real = np.array(indices_comp_id_real)[0]
    comp_id_real = users_id[indices_comp_id_real]

    pre_probas = model.predict_proba(X_test)
    y_pre_model = model.predict(X_test)
    # print(pre_probas)
    # print(y_pre_model)
    # print(pre_probas[indices_comp_id_real])

    y_pre_my = np.zeros(y_test.shape).astype('int')
    #
    for i, proba in enumerate(pre_probas):
        if proba[1] > 0.9:
            y_pre_my[i] = 1
    print(y_pre_my)
    #
    pre_rec_fscore(y_test, y_pre_my)
    # print(pre_proba)
    # y_test_prediction = model.predict(X_test)
    # users_id = np.array(users_id)
    # indices = np.where(y_test_prediction == 1)
    # complained_users_id = users_id[indices]
    # pre_rec_fscore(y_test, y_test_prediction)
    # print('1类数量：{}'.format(len(complained_users_id)))

    # return complained_users_id


def threshold_pred(model,
                   threshold=0.5,
                   X=None,
                   y=None):

    pre_probas = model.predict_proba(X)

    y_pre_threshold = np.zeros(y.shape).astype('int')
    #
    for i, proba in enumerate(pre_probas):
        if proba[1] > threshold:
            y_pre_threshold[i] = 1
    #
    pre_rec_fscore(y_actual=y, y_predict=y_pre_threshold)

