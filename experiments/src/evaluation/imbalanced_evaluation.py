import common
import json
from sklearn import metrics
import matplotlib.pyplot as plt


def fscore(y_actual, y_predict):
    true_pos = true_neg = false_pos = false_neg = 0
    for y, y_hat in zip(y_actual, y_predict):
        if y == 1:
            if y_hat == 1:
                true_pos += 1
            elif y_hat == 0:
                false_neg += 1
            else:
                print('预测值非0,1')
        elif y == 0:
            if y_hat == 1:
                false_pos += 1
            elif y_hat == 0:
                true_neg += 1
            else:
                print('预测值非0,1')
        else:
            print('预测值非0,1')
    try:
        precision = true_pos / (true_pos + false_pos)
    except ZeroDivisionError as e:
        print(e)
        precision = 0

    try:
        recall = true_pos / (true_pos + false_neg)
    except ZeroDivisionError as e:
        print(e)
        recall = 0

    try:
        f1_score = 2 * precision * recall / (precision + recall)
    except ZeroDivisionError as e:
        print(e)
        f1_score = 0

    evaluation = {'precision': precision,
                  'recall': recall,
                  'f1_score': f1_score}
    evaluation_detail = {'true_pos': true_pos,
                         'true_neg': true_neg,
                         'false_pos': false_pos,
                         'false_neg': false_neg}
    print(json.dumps(evaluation, indent=4, ensure_ascii=False))
    print(json.dumps(evaluation_detail, indent=4, ensure_ascii=False))
    return evaluation


def roc_auc(y_actual, y_score):
    fpr, tpr, thresholds = metrics.roc_curve(y_true=y_actual, y_score=y_score)
    plt.xlabel('fpr')
    plt.ylabel('tpr')
    plt.plot(fpr, tpr)
    plt.show()
    auc = metrics.auc(fpr, tpr)
    print(thresholds)
    print('auc:{}'.format(auc))
    return auc


