import numpy as np
from data_utils import prepare_data_4_model

# def get_complained_users_id(y_prediction, user_id):
#     y_prediction = np.array(y_prediction)
#     user_id = np.array(user_id)
#
#     indices = np.where(y_prediction == 1)
#     complained_users_id = user_id[indices]
#     # print(complained_users_id)
#     return complained_users_id
from data_utils import num_features, bool_features, prepare_data_4_model


def get_complained_users_id(model,
                            features_file_test=None,
                            label_file_test=None):
    X_test, y_test, users_id = prepare_data_4_model(features_file=features_file_test,
                                                    label_file=label_file_test)
    y_test_prediction = model.predict(X_test)

    users_id = np.array(users_id)
    indices = np.where(y_test_prediction == 1)
    complained_users_id = users_id[indices]

    print(complained_users_id)
    print(len(complained_users_id))
    return complained_users_id

