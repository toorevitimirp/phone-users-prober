from api.app import app
from etl.data_center import data_center
from visualization import visual
from statistic import statistic

app.register_blueprint(data_center)
app.register_blueprint(visual)
app.register_blueprint(statistic)
