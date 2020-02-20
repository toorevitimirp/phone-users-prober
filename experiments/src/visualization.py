"""
数据可视化
"""
import pandas as pd
import matplotlib.pyplot as plt

from sklearn import preprocessing
from data_utils import get_clean_raw_data, num_features, bool_features


def bool_feature_distribution():
    # 对label分组，考察label关于不同布尔型特征的分布
    features = '../data/3月用户相关数据.csv'
    label = '../data/3月被投诉用户.csv'
    data_all = get_clean_raw_data(features_file=features, label_file=label)

    # for col in bool_features:
    #     print(data_all.groupby('label')[col].value_counts().unstack())

    grouped = data_all.groupby('label')
    for col in bool_features:
        toplot = grouped[col].value_counts().unstack()
        print(toplot)
        print('############################')
        # toplot.plot(kind='bar')
        # plt.show()


def num_scatter_all():
    # 数值型特征之间的二维散点图，包含0和1类
    features = '../data/3月用户相关数据.csv'
    label = '../data/3月被投诉用户.csv'
    data_all = get_clean_raw_data(features_file=features, label_file=label)

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
    features = '../data/3月用户相关数据.csv'
    label = '../data/3月被投诉用户.csv'
    data_all = get_clean_raw_data(features_file=features, label_file=label)
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
    # 盒图
    features = '../data/3月用户相关数据.csv'
    label = '../data/3月被投诉用户.csv'
    data_all = get_clean_raw_data(features_file=features, label_file=label)
    data = preprocessing.scale(data_all)
    print(data)
    data = pd.DataFrame(data)
    # df = get_clean_raw_data(features_file='../data/3月用户相关数据.csv',
    #                         label_file='../data/3月被投诉用户.csv')
    # num_features,bool_features
    data.plot.box(title="Consumer spending in each country")
    plt.show()


def pie_bool_all():
    # 布尔型特征，饼图，正负两类
    features = '../data/3月用户相关数据.csv'
    label = '../data/3月被投诉用户.csv'
    data_all = get_clean_raw_data(features_file=features, label_file=label)
    bin_label = ['0', '1']
    for col in bool_features:
        df = data_all[col].value_counts()
        print(df)
        size_0 = df[0]
        size_1 = df[1]
        sizes = [size_0, size_1]
        plt.figure()
        plt.pie(sizes, labels=bin_label, autopct='%1.1f%%')
        plt.title(col + '\nlabel=0,1')
        # plt.show()
        plt.savefig('../notes/image/pie-all/' + col)


def bar_bool_0vs1_label():
    # 布尔型特征，条形图，0类中某布尔特征的分布和1类中该布尔特征的分布
    features = '../data/3月用户相关数据.csv'
    label = '../data/3月被投诉用户.csv'
    data_all = get_clean_raw_data(features_file=features, label_file=label)
    grouped = data_all.groupby('label')
    for col in bool_features:
        df = grouped[col].value_counts().unstack()
        print(df)
        l0f0 = df.iat[0, 0]  # label == 0 ,feature==0
        l0f1 = df.iat[0, 1]
        l1f0 = df.iat[1, 0]
        l1f1 = df.iat[1, 1]
        plt.figure()
        plt.suptitle(col, fontsize=14)
        index = [0, 1]

        plt.subplot(121)
        plt.title('label=0')
        plt.bar(index, [l0f0, l0f1],color=['#1F77B3', 'r'])
        # 设置数字标注
        for a, b in zip(index, [l0f0, l0f1]):
            plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=10)
        plt.xticks(index, ['0\n'+col, '1\n'+col])

        plt.subplot(122)
        plt.bar(index, [l1f0, l1f1], color=['#1F77B3','r'])
        plt.title('label=1')
        for a, b in zip(index, [l1f0, l1f1]):
            plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=10)
        plt.xticks(index, ['0\n'+col, '1\n'+col])
        plt.savefig('../notes/image/bar-0vs1-label/' + col)


def bar_bool_0vs1_feature():
    # 布尔型特征，条形图，某布尔特征为0时，label的分布;某布尔特征为1时，label的分布;
    features = '../data/3月用户相关数据.csv'
    label = '../data/3月被投诉用户.csv'
    data_all = get_clean_raw_data(features_file=features, label_file=label)
    grouped = data_all.groupby('label')
    for col in bool_features:
        df = grouped[col].value_counts().unstack()
        print(df)
        l0f0 = df.iat[0, 0]  # label == 0 ,feature==0
        l1f0 = df.iat[1, 0]
        l0f1 = df.iat[0, 1]
        l1f1 = df.iat[1, 1]
        plt.figure()
        plt.suptitle(col, fontsize=14)
        index = [0, 1]

        plt.subplot(121)
        y0 = [l0f0, l1f0]
        plt.bar(index, y0, color=['#1F77B3', 'r'])
        # 设置数字标注
        for a, b in zip(index, y0):
            plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=10)
        plt.title(col+'=0')
        plt.xticks(index, ['label=0', 'label=1'])

        plt.subplot(122)
        y1 = [l0f1, l1f1]
        plt.bar(index, y1, color=['#1F77B3','r'])
        for a, b in zip(index, y1):
            plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=10)
        plt.xticks(index, ['label=0', 'label=1'])
        plt.title(col+'=1')

        # plt.show()
        plt.savefig('../notes/image/bar-0vs1-feature/' + col)


def main():
    bar_bool_0vs1_feature()


if __name__ == '__main__':
    main()
