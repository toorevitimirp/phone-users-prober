"""
matplotlib渲染大量数据很慢，使用pyqtgraph画的3d图
"""
import common
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np
import sys


def draw_3d(pos0, pos1):
    app = QtGui.QApplication([])
    w = gl.GLViewWidget()
    w.show()
    g = gl.GLGridItem()
    w.addItem(g)

    # generate random points from -10 to 10, z-axis positive
    sp0 = gl.GLScatterPlotItem(pos=pos0)
    w.addItem(sp0)
    # generate a color opacity gradient
    color0 = np.zeros((pos0.shape[0], 4), dtype=np.float32)
    color0[:, 0] = 1
    color0[:, 1] = 1
    color0[:, 2] = 1
    color0[:, 3] = 1
    sp0.setData(color=color0)

    sp1 = gl.GLScatterPlotItem(pos=pos1)
    w.addItem(sp1)

    # generate a color opacity gradient
    color1 = np.zeros((pos1.shape[0], 4), dtype=np.float32)
    color1[:, 0] = 1
    color1[:, 1] = 0
    color1[:, 2] = 1
    color1[:, 3] = 1
    sp0.setData(color=color1)

    t = QtCore.QTimer()
    t.start(50)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()






## Start Qt event loop unless running in interactive mode.
# if __name__ == '__main__':
#     import sys
#
#     if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#         QtGui.QApplication.instance().exec_()
