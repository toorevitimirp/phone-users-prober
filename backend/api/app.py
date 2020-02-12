from flask import Flask
from flask_cors import cross_origin

app = Flask(__name__)
# 日志
from api.logger import log

# 注册路由
import api.route

# 错误处理
import api.error


@app.route('/test', methods=['GET'])
@cross_origin()
def test():
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
    data = [
        {
            'feature': 'roam_call_duration',
            'min': 0,
            'max': 100,
            'max-min': 100,
            'var': 98,
            'std': 72,
            'mean': 59,
            'media': 56
        },
        {
            'feature': 'mon_use_days',
            'min': 0,
            'max': 100,
            'max-min': 100,
            'var': 98,
            'std': 72,
            'mean': 59,
            'media': 56
        }
    ]
    return {'result': 0, 'data': data}


@app.route('/maps', methods=['GET'])
@cross_origin()
def all_maps():
    return str(app.url_map)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
