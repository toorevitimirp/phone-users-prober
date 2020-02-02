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
def test():
    return str(app.url_map)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
