import numpy as np
import pandas as pd

from visualization.d3 import draw_3d


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
