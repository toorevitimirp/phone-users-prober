import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from visualization.d3 import draw_3d


def num_scatter_3d_all(X, y):
    """
    数值型特征之间的二维散点图，包含0和1类
    :return:
    """
    num_features = ['f0', 'f1', 'f2']
    df = pd.DataFrame(X, columns=num_features)
    df['label'] = pd.Series(y)
    grouped = df.groupby('label')

    label1_df = grouped.get_group(1)
    label0_df = grouped.get_group(0)
    count = 0
    for i, f1 in enumerate(num_features):
        for f2 in num_features[i + 1:]:
            ax = label0_df.plot.scatter(x=f1, y=f2, color='b', marker='x', label='label=0')
            label1_df.plot.scatter(x=f1, y=f2, color='r', marker='+', label='label=1', ax=ax)
            plt.show()
            # plt.savefig('../../notes/image/scatter-all-3d/' + f1 + '--' + f2)
            count += 1
    print('done')
    print('all:', count)


def magnifier(X, y):
    """
    数值型特征之间的二维散点图，包含0和1类
    :return:
    """
    num_features = ['f0', 'f1', 'f2']
    df = pd.DataFrame(X, columns=num_features)
    df['label'] = pd.Series(y)
    grouped = df.groupby('label')

    label0_df = grouped.get_group(0)
    label1_df = grouped.get_group(1)

    count = 0
    for ind in range(100):
        for i, f1 in enumerate(num_features):
            for f2 in num_features[i + 1:]:
                label0_x = label0_df[f1]
                label0_y = label0_df[f2]
                label1_x = label1_df[f1]
                label1_y = label1_df[f2]
                fig, ax = plt.subplots()
                index = label1_df[f1].index
                view_point_x = label1_df[f1][index[ind]]
                view_point_y = label1_df[f2][index[ind]]
                print(view_point_x, view_point_y)
                view_scope_x = 10
                view_scope_y = 10
                ax.set_xlim(view_point_x - view_scope_x, view_point_x + view_scope_x)
                ax.set_ylim(view_point_y-view_scope_y, view_point_y + view_scope_y)

                ax.scatter(x=label0_x, y=label0_y, color='b', marker='x', label='label=0')
                ax.scatter(x=label1_x, y=label1_y, color='r', marker='+', label='label=1')
                ax.set_xlabel(f1)
                ax.set_ylabel(f2)
                ax.legend()
                plt.show()
                file_name = '../../notes/image/magnifier/' + f1 + '--' + f2 + '--' + str(count)
                # plt.savefig(file_name)
                count += 1
    print('done')
    print('all:', count)


def visualization_sampled_data(X_3d, y_sampled):
    df = pd.DataFrame(X_3d)
    df['label'] = pd.Series(y_sampled)
    grouped = df.groupby('label')

    data_1 = grouped.get_group(1)
    data_0 = grouped.get_group(0)

    pos1 = data_1.drop(labels='label', axis=1)
    pos0 = data_0.drop(labels='label', axis=1)

    pos0 = np.array(pos0)
    pos1 = np.array(pos1)

    draw_3d(pos0, pos1)
