from flask import Flask
from flask_cors import cross_origin

app = Flask(__name__)
# 日志
from api.logger import log

# 注册路由
import api.route

# 错误处理
import api.error


@app.route('/test', methods=['GET','POST'])
@cross_origin()
def test():
    # 画图
    import matplotlib.pyplot as plt
    import numpy as np
    x = np.linspace(0, np.pi*2, 100)
    y = np.sin(x)
    plt.figure()
    plt.plot(x, y)
    
    # 转换成base64
    from io import BytesIO
    fig_file = BytesIO()
    plt.savefig(fig_file, format='png')
    fig_file.seek(0)  # rewind to beginning of file
    import base64
    # figdata_png = base64.b64encode(figfile.read())
    figdata_png = base64.b64encode(fig_file.getvalue())
    return figdata_png
    

@app.route('/maps', methods=['GET'])
@cross_origin()
def all_maps():
    return str(app.url_map)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
