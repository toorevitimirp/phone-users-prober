import pandas as pd
import matplotlib.pyplot as plt
from utils import get_all_data, num_features, bool_features

plt.style.use('ggplot')
features = './data/3月用户相关数据.csv'
label = './data/3月被投诉用户.csv'
data_all = get_all_data(features_file=features, label_file=label)
# path = 'https://raw.githubusercontent.com/HoijanLai/dataset/master/PoliceKillingsUS.csv'
# data_all = pd.read_csv(path, encoding='latin1')


def bar_plot():
    # for col in bool_features:
    #     print(data_all.groupby('label')[col].value_counts().unstack())

    grouped = data_all.groupby('label')
    # print(grouped['signs_of_mental_illness'].value_counts().unstack())
    for col in bool_features:
        toplot = grouped[col].value_counts().unstack()
        print(toplot)
        print('############################')
        toplot.plot(kind='bar')
        plt.show()


def main():
    bar_plot()


if __name__ == '__main__':
    main()
