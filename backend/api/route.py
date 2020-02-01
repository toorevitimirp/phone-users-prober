from api.app import app
from etl.data_center import data_center

app.register_blueprint(data_center)