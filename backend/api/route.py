from api.app import app
from etl.washer import washer
app.register_blueprint(washer)