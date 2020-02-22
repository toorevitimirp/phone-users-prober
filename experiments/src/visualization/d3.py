import common
import pyqtgraph.opengl as gl
import numpy as np
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pyqtgraph.Qt import QtCore, QtGui
from pandas import DataFrame


def draw_3d(pos0, pos1):
    """
    :param pos0: 0类数据,m×3
    :param pos1: 1类数据,m×3
    :return:
    """
    app = QtGui.QApplication([])
    w = gl.GLViewWidget()
    w.show()
    # 增加网格后渲染速度很慢
    # grid_size = QtGui.QVector3D(50000, 50000, 1000)
    # g = gl.GLGridItem(size=grid_size)
    # w.addItem(g)

    # generate random points from -10 to 10, z-axis positive
    sp0 = gl.GLScatterPlotItem(pos=pos0)
    w.addItem(sp0)
    # generate a color opacity gradient
    color0 = np.zeros((pos0.shape[0], 4), dtype=np.float32)
    color0[:, 0] = 0
    color0[:, 1] = 0
    color0[:, 2] = 1
    color0[:, 3] = 1
    sp0.setData(color=color0)

    # pos1 = np.random.randint(0, 10, size=(1000, 3))
    sp1 = gl.GLScatterPlotItem(pos=pos1)
    w.addItem(sp1)

    # generate a color opacity gradient
    color1 = np.zeros((pos1.shape[0], 4), dtype=np.float32)
    color1[:, 0] = 1
    color1[:, 1] = 0
    color1[:, 2] = 0
    color1[:, 3] = 1
    sp1.setData(color=color1)

    t = QtCore.QTimer()
    t.start(50)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()


def pca_visual(X_pca, label):
    """
    pca降维后可视化
    :param X_pca:
    :param label:
    :return:
    """
    data_all = DataFrame(X_pca)
    data_all['label'] = label
    grouped = data_all.groupby('label')
    data_0 = grouped.get_group(0)
    data_1 = grouped.get_group(1)

    pos0 = data_0.drop(labels='label', axis=1)
    pos1 = data_1.drop(labels='label', axis=1)

    pos0 = np.array(pos0)
    pos1 = np.array(pos1)

    # fig = plt.figure()
    # ax = Axes3D(fig)
    # ax.scatter(pos0[:, 0], pos0[:, 1], pos0[:, 2], s=1, c='b')
    # ax.scatter(pos1[:, 0], pos1[:, 1], pos1[:, 2], s=20, c='r')
    # plt.show()
    # draw_3d 渲染速度快，但是效果非常不好
    draw_3d(pos0, pos1)