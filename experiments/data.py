import pandas as pd

from washer import wash_data


def get_all_data(features_file='./data/3月用户相关数据.csv', label_file='./data/3月被投诉用户.csv'):
    user_data = pd.read_csv(features_file, encoding='utf-8')
    complain_users = pd.read_csv(label_file, encoding='utf-8')["user_id"]

    all_users_id = user_data["user_id"]
    labels = all_users_id.isin(complain_users).astype("int")
    user_data["label"] = labels

    clean_data = wash_data(user_data)
    return clean_data
