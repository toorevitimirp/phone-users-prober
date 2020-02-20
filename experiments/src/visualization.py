"""
数据可视化
"""
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing

from data_utils import get_clean_raw_data, num_features, bool_features
import matplotlib.pyplot as plt

plt.style.use('ggplot')
features = '../data/3月用户相关数据.csv'
label = '../data/3月被投诉用户.csv'
data_all = get_clean_raw_data(features_file=features, label_file=label)


# path = 'https://raw.githubusercontent.com/HoijanLai/dataset/master/PoliceKillingsUS.csv'
# data_all = pd.read_csv(path, encoding='latin1')


def bool_feature_distribution():
    # 对label分组，考察label关于不同布尔型特征的分布
    # for col in bool_features:
    #     print(data_all.groupby('label')[col].value_counts().unstack())

    grouped = data_all.groupby('label')
    print(grouped['users_3w'].value_counts().unstack()[0])
    print(grouped['signs_of_mental_illness'].value_counts().unstack())
    for col in bool_features:
        toplot = grouped[col].value_counts().unstack()
        print(toplot)
        print('############################')
        # toplot.plot(kind='bar')
        # plt.show()


def num_scatter_all():
    # 数值型特征之间的二维散点图，包含0和1类
    grouped = data_all.groupby('label')
    label1_df = grouped.get_group(1)
    label0_df = grouped.get_group(0)
    count = 0
    for i, x1 in enumerate(num_features):
        for x2 in num_features[i + 1:]:
            ax = label0_df.plot.scatter(x=x1, y=x2, color='b', marker='x', label='label=0')
            label1_df.plot.scatter(x=x1, y=x2, color='r', marker='+', label='label=1', ax=ax)
            plt.savefig('../notes/image/scatter-all/' + x1 + '--' + x2)
            count += 1
            print(count)
    print('done')
    print('all:', count)


def num_scatter_1():
    # 数值型特征之间的二维散点图，只包含1类
    grouped = data_all.groupby('label')
    label1_df = grouped.get_group(1)
    count = 0
    for i, x1 in enumerate(num_features):
        for x2 in num_features[i + 1:]:
            label1_df.plot.scatter(x=x1, y=x2, color='r', marker='+', label='label=1')
            plt.savefig('../notes/image/scatter-1/' + x1 + '--' + x2)
            count += 1
            print(count)
    print('done')
    print('all:', count)


def box_plot():
    data = preprocessing.scale(data_all)
    print(data)
    data = pd.DataFrame(data)
    # df = get_clean_raw_data(features_file='../data/3月用户相关数据.csv',
    #                         label_file='../data/3月被投诉用户.csv')
    # num_features,bool_features
    data.plot.box(title="Consumer spending in each country")
    plt.show()

def main():
    box_plot()


if __name__ == '__main__':
    main()
