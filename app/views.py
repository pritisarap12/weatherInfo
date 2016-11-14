from flask_restful import Resource
from flask import jsonify, json, Response
import datetime
from flask_httpauth import HTTPBasicAuth
import requests
import configData
from requests.auth import HTTPBasicAuth as RequestAuth


auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == configData.testdata['username']:
        return configData.testdata['password']
    return None


@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access', 'status': 401})


def validateDateTime(date, time):
    """function to validate if date and time are valid"""
    historic_data = json.load(open("source/forecast.json"))
    for info in historic_data["list"]:
        if str(info["dt_txt"].split()[0].replace("-", "")) == date and str(info["dt_txt"].split()[1].replace(":", "")[:4]) == time:
            return info
    else:
        url = configData.testdata["apiUrl"]
        response = requests.get(
            url, verify=True, auth=RequestAuth(configData.testdata["apiUsername"], configData.testdata["apiPassword"]))
        if response.status_code == 200:
            data = json.loads(response.content)
            for info in data["list"]:
                if str(info["dt_txt"].split()[0].replace("-", "")) == date and str(info["dt_txt"].split()[1].replace(":", "")[:4]) == time:
                    return info
            else:
                return False

        else:
            return False


class GetWeatherInfoAPI(Resource):

    """Api to return information
        for given date and time
        """
    @auth.login_required
    def get(self, date, time):

        info = validateDateTime(date, time)
        if info:
            return {"description": info["weather"][0]["description"],
                    "temperature": str(round(info["main"]["temp"] - 273.15)) + "C",
                    "pressure": info["main"]["pressure"],
                    "humidity": str(info["main"]["humidity"]) + "%"
                    }

        else:
            return {
                "status": "error", "message": "No data for %s" % (datetime.datetime.strptime(date + time, '%Y%m%d%H%M%S'))
            }


class GetTempertureAPI(Resource):

    """Api to return temperature
        for given date and time
        """
    @auth.login_required
    def get(self, date, time, unit=None):
        info = validateDateTime(date, time)
        if info:
            if not unit or unit.lower() == "celcius":
                return {"temperature": str(round(info["main"]["temp"] - 273.15)) + "C"}
            elif unit.lower() == "kelvin":
                return {"temperature": info["main"]["temp"]}
            else:
                return {
                    "status": "error", "message": "Invalid temperature unit %s" % (unit)
                }
        else:
            return {
                "status": "error", "message": "No data for %s" % (datetime.datetime.strptime(date + time, '%Y%m%d%H%M%S'))
            }


class GetPressureAPI(Resource):

    """Api to return pressure
        for given date and time
        """
    @auth.login_required
    def get(self, date, time):
        info = validateDateTime(date, time)
        if info:
            return {"pressure": info["main"]["pressure"]}
        else:
            return {
                "status": "error", "message": "No data for %s" % (datetime.datetime.strptime(date + time, '%Y%m%d%H%M%S'))
            }


class GetHumidityAPI(Resource):

    """Api to return humidity
        for given date and time
        """
    @auth.login_required
    def get(self, date, time):
        info = validateDateTime(date, time)
        if info:
            return {"humidity": str(info["main"]["humidity"]) + "%"}
        else:
            return {
                "status": "error", "message": "No data for %s" % (datetime.datetime.strptime(date + time, '%Y%m%d%H%M%S'))
            }
