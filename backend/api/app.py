from flask import Flask
from etl.washer import washer
print(__file__)
app = Flask(__name__)
app.register_blueprint(washer)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)