from api.app import app
from etl.data_center import data_center
from visualization import visual
from statistic import statistic
from train import train
from predict import predict

app.register_blueprint(data_center)
app.register_blueprint(visual)
app.register_blueprint(statistic)
app.register_blueprint(train)
app.register_blueprint(predict)
