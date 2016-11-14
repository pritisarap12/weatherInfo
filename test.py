from app import app, views
import unittest
from flask import Flask, session
from base64 import b64encode


class TestInfoAPI(unittest.TestCase):

    def setUp(self):
        self.api = app.app.test_client()
        self.username = 'super'
        self.password = 'carer'
        self.headers = {
            'Authorization': 'Basic ' + b64encode("{0}:{1}".format(self.username, self.password))
        }

    def tearDown(self):
        pass

    def test_01_Test_Info_API(self):
     	"""Test to verify API for getting wether information
	"""

       	info = self.api.get(
            '/weather/london/20160705/2100', headers=self.headers)
        infoSlash = self.api.get(
            '/weather/london/20160705/2100/', headers=self.headers)
        self.assertEqual(info.status_code, 200, msg="Failed to fetch info")
        self.assertEqual(
            infoSlash.status_code, 200, msg="Failed to fetch info")

    def test_02_Test_Info_Not_Exist_API(self):
     	"""Test to check the API for checking
	response for non existing date and time"""

       	info = self.api.get(
            '/weather/london/20160715/2100', headers=self.headers)
        self.assertEqual(info.status_code, 200, msg="Failed to fetch info")
        infoSlash = self.api.get(
            '/weather/london/20160715/2100/', headers=self.headers)
        self.assertEqual(info.status_code, 200, msg="Failed to fetch info")
        self.assertIn('{"status": "error"', info.data.split(
            ","), msg="Failed: Should return error status")
        self.assertIn('{"status": "error"', infoSlash.data.split(
            ","), msg="Failed: Should return error status")


    def test_03_Test_Invalid_User(self):
     	"""Test to verify API for invalid
	Username or Password"""

        self.username = 'super'
        self.password = 'python'
        self.headers = {
            'Authorization': 'Basic ' + b64encode("{0}:{1}".format(self.username, self.password))
        }
        info = self.api.get(
            '/weather/london/20160705/2100', headers=self.headers)
        self.assertEqual(
            info.status_code, 401, msg="Should return 401 status code")


    def test_04_Test_Temperture_API(self):
    	"""Test to verify temperature API"""

        info = self.api.get(
            '/weather/london/20160705/2100/temperature', headers=self.headers)
        self.assertEqual(
            info.status_code, 200, msg="Failed to return temerature")


    def test_05_Test_Temperture_Kelvin_API(self):
    	"""Test to verify temperature in Kelvin API"""
        info = self.api.get(
            '/weather/london/20160705/2100/temperature/kelvin', headers=self.headers)
        self.assertEqual(
            info.status_code, 200, msg="Failed to return temerature in Kelvin")


    def test_06_Test_Temperture_Celcius_API(self):
    	"""Test to verify temperature in celcius API"""
        info = self.api.get(
            '/weather/london/20160705/2100/temperature/celcius', headers=self.headers)
        self.assertEqual(
            info.status_code, 200, msg="Failed to return temeraturein celcius")


    def test_07_Test_Temperture_Invalid_Unit_API(self):
    	"""Test to verify temperature API response fo invalid temerature unit"""

        info = self.api.get(
            '/weather/london/20160705/2100/temperature/celciu', headers=self.headers)
        self.assertEqual(info.status_code, 200)
        self.assertIn('{"status": "error"', info.data.split(
            ","), msg="Failed: Should return error status")


    def test_08_Test_Pressure_API(self):
    	"""Test to verify pressure API"""
        info = self.api.get(
            '/weather/london/20160705/2100/pressure', headers=self.headers)
        self.assertEqual(
            info.status_code, 200, msg="Failed to return pressure")


    def test_09_Test_Humidity_API(self):
    	"""Test to verify humidity API"""
        info = self.api.get(
            '/weather/london/20160705/2100/humidity', headers=self.headers)
        self.assertEqual(
            info.status_code, 200, msg="Failed to return humidity")


if __name__ == '__main__':
    unittest.main()
