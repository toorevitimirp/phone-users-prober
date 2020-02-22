import common
import numpy as np

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


def get_complained_users_id(model,
                            features_file_test=None,
                            label_file_test=None):
    X_test, y_test, users_id = prepare_data_4_prediction(features_file=features_file_test,
                                                         label_file=label_file_test)
    y_test_prediction = model.predict(X_test)

    users_id = np.array(users_id)
    indices = np.where(y_test_prediction == 1)
    complained_users_id = users_id[indices]

    pre_rec_fscore(y_test, y_test_prediction)
    print('1类数量：{}'.format(len(complained_users_id)))
    return complained_users_id

