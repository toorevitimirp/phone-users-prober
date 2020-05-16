import common
import torch
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
from data_processing.data_utils import get_clean_raw_data, num_features
from sklearn import preprocessing
from sklearn.preprocessing import PolynomialFeatures
from data_processing.dimension_reduction import features_extraction_3d
from data_processing.imbalance_handle import imbalanced_handle
from evaluation.imbalanced_evaluation import fscore, roc_auc
from time import time
from other_utils import beep


class Data:
    def __init__(self, features_file_train,
                 label_file_train,
                 features_file_test,
                 label_file_test):
        self.features_file_train = features_file_train
        self.label_file_train = label_file_train
        self.features_file_test = features_file_test
        self.label_file_test = label_file_test

    def get_train_data(self):
        raw_data = get_clean_raw_data(features_file=self.features_file_train,
                                      label_file=self.label_file_train)
        X = np.array(raw_data[num_features])
        y = np.array(raw_data['label'])

        # imbalanced data processing
        # X, y = imbalanced_handle(X, y)

        # 降维
        # X = features_extraction_3d(X)
        X, y = Variable(torch.from_numpy(X)), Variable(torch.from_numpy(y))
        X_final = X

        return X_final, y

    def get_test_data(self):
        raw_data = get_clean_raw_data(features_file=self.features_file_test,
                                      label_file=self.label_file_test)
        X = np.array(raw_data[num_features])
        y = np.array(raw_data['label'])

        # 降维
        # X = features_extraction_3d(X)
        X, y = Variable(torch.from_numpy(X)), Variable(torch.from_numpy(y))
        X_final = X

        return X_final, y


class Net(torch.nn.Module):
    def __init__(self, n_features, n_hidden, n_output):
        super(Net, self).__init__()
        self.hidden = torch.nn.Linear(n_features, n_hidden)
        self.predict = torch.nn.Linear(n_hidden, n_output)

    def forward(self, x):
        x = F.softmax(self.hidden(x))
        x = self.predict(x)
        return x


def main():
    features_file_train = '../../data/3月用户相关数据.csv'
    label_file_train = '../../data/3月被投诉用户.csv'
    features_file_test = '../../data/4月用户相关数据.csv'
    label_file_test = '../../data/4月被投诉用户.csv'

    data = Data(features_file_train=features_file_train,
                label_file_train=label_file_train,
                features_file_test=features_file_test,
                label_file_test=label_file_test)

    X_train, y_train = data.get_train_data()
    X_test, y_test = data.get_test_data()

    n_features = X_train.shape[1]
    n_hidden = 10
    n_output = 2
    net = Net(n_features, n_hidden, n_output)

    optimizer = torch.optim.SGD(net.parameters(), lr=0.02)
    loss_func = torch.nn.CrossEntropyLoss()

    n = 100
    for i in range(n):
        out = net(X_train)
        loss = loss_func(out, y_train)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        prediction = torch.max(F.softmax(out), 1)[1]
        print(prediction)
        # print(loss.data)


if __name__ == '__main__':
    main()
