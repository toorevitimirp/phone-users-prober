import common
import matplotlib.pyplot as plt
import numpy as np


class VisualEvaluation:
    @staticmethod
    def evaluation(bars, precision, recall, f1_score, auc, title):
        # bars = ['不降维,不采样', '不降维,采样', '降维,采样', '降维,不采样']
        # precision = [1, 0.45, 0.01, 1]
        # recall = [0.67, 0.69, 0.14, 0.67]
        # f1_score = [0.80, 0.54, 0.01, 0.80]
        # auc = [0.94, 0.93, 0.56, 0.94]

        x = np.arange(len(bars))
        width = 0.2

        plt.bar(x, precision, width=width, label='precision', color='darkorange')
        plt.bar(x + width, recall, width=width, label='recall', color='deepskyblue', tick_label=bars)
        plt.bar(x + 2 * width, f1_score, width=width, label='f1_score', color='green')
        plt.bar(x + 3 * width, auc, width=width, label='auc', color='yellow')

        # 显示在图形上的值
        for a, b in zip(x, precision):
            plt.text(a, b , b, ha='center', va='bottom')
        for a, b in zip(x, recall):
            plt.text(a + width, b , b, ha='center', va='bottom')
        for a, b in zip(x, f1_score):
            plt.text(a + 2 * width, b, b, ha='center', va='bottom')
        for a, b in zip(x, auc):
            plt.text(a + 3 * width, b, b, ha='center', va='bottom')

        plt.xticks()
        plt.legend()

        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        # plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示中文标签
        plt.ylabel('value')
        plt.title(title)
        plt.show()

    @staticmethod
    def time(bars, time, title):
        # bars = ['不降维,不采样', '不降维,采样', '降维,采样', '降维,不采样']
        # time = [2.71, 7.55, 2.29, 1.27]
        x = np.arange(len(bars))
        # width = 0.2

        plt.bar(x, time, label='时间', color='darkorange', tick_label=bars)

        # 显示在图形上的值
        for a, b in zip(x, time):
            plt.text(a, b, b, ha='center', va='bottom')
        # for a, b in zip(x, recall):
        #     plt.text(a + width, b, b, ha='center', va='bottom')
        # for a, b in zip(x, f1_score):
        #     plt.text(a + 2 * width, b, b, ha='center', va='bottom')
        # for a, b in zip(x, auc):
        #     plt.text(a + 3 * width, b, b, ha='center', va='bottom')
        plt.xticks()
        # plt.legend()

        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.ylabel('时间/秒')
        plt.title(title)
        plt.show()


def main():
    bars = ['随机上采样', 'SMOTE', 'SMOTE+TomekLinks','SMOTE+ENN','不采样']
    precision = [0.007, 0.002,0.003, 0.002, 0.006]
    recall = [0.92, 0.86, 0.84,0.85,0.45]
    f1_score = [0.002, 0.004, 0.005,0.005,0.013]
    auc = [0.79, 0.81, 0.82,0.80,0.81]
    time = [0.51, 0.89, 5021.20, 4849.65,0]
    title = ''
    ve = VisualEvaluation()
    ve.evaluation(bars=bars, precision=precision,
                  recall=recall, f1_score=f1_score,
                  auc=auc, title=title)
    ve.time(bars=bars, time=time, title=title)


if __name__ == '__main__':
    main()