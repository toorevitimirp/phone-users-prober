import json

from statistic import statistic
from flask import request
from flask_cors import cross_origin
from etl.database import load_data
from pandas import DataFrame

@statistic.route('/basic', methods=['POST'])
@cross_origin()
def basic():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode('utf-8'))
        collection = json_data['collection']
        print(collection)
        maps = {
            'feature': '特征',
            'min': '最小值',
            'max': '最大值',
            'max-min': '最小值和最大值的差',
            'var': '方差',
            'std': '标准差',
            'mean': '平均值',
            'media': '中位数'
        }
        raw = load_data(collection)
        data = []
        for col in raw.columns:
            print(col)

        return {'result': 0, 'data': data}
