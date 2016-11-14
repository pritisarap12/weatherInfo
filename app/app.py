import views
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

api.add_resource(views.GetWeatherInfoAPI,
                 '/weather/london/<date>/<time>', strict_slashes=False, endpoint="info")
api.add_resource(views.GetPressureAPI,
                 '/weather/london/<date>/<time>/pressure', strict_slashes=False, endpoint="pressure")
api.add_resource(views.GetHumidityAPI,
                 '/weather/london/<date>/<time>/humidity', strict_slashes=False, endpoint="humidity")
api.add_resource(views.GetTempertureAPI,
                 '/weather/london/<date>/<time>/temperature', strict_slashes=False, endpoint="temp")
api.add_resource(views.GetTempertureAPI,
                 '/weather/london/<date>/<time>/temperature/<unit>', strict_slashes=False, endpoint="temperature")
