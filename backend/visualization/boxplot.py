import json

from flask import request
from flask_cors import cross_origin
from visualization import visual
from etl.database import get_series_form_collection
from pandas import DataFrame


@visual.route('/boxplot', methods=['POST'])
@cross_origin()
def box_plot():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode('utf-8'))
        collection = json_data['collection']
        feature = json_data['feature']

        raw = get_series_form_collection(collection, feature)
        desc = raw.describe()[feature]
        print(desc)
        data = []
        try:
            data.append(desc['max'])
            data.append(desc['75%'])
            data.append(desc['75%'])
            data.append(desc['25%'])
            data.append(desc['min'])
        except BaseException as e:
            res = {'code': '0', 'msg': str(e), 'data': None}
        else:
            print(data)
            res = {'code': '1', 'msg': '获取数据成功', 'data': data}
        finally:
            return res


def describe(data):
    pass
    descriptions = data.describe()
    descriptions_dic = {}
    # for row in descriptions.itertuples():
    #     print(row)
    # for index, row in descriptions.iteritems():
    #     print(type(row))
    for column in descriptions.columns:
        description = {}
        i = 0
        maps = {1: "mean", 2: "std", 3: "min", 4: "25%", 5: "50%", 6: "75%", 7: "max"}
        # print(descriptions[column])
        for row in descriptions[column]:
            if i:
                description[maps[i]] = row
            i += 1
        descriptions_dic[column] = description
    return descriptions_dic
