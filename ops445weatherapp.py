"""
 --------------------------------------------------------------------------------------------------------
 Capstone Project: Weather Forecast Application
 Course: OPS445
 Section: NDD
 Professor M. Rebultan
 Created By: Angelo Maroulis, Desinthan Paranthaman, Waleed Arif

 The purpose of the Weather Forecast Application is to create a simple but intuitive
 interface that will allow the end-user to interact. The end-user will be able to 
 input a location and receive the weather of the location. To receive real-time 
 weather data, the code will implement an API Key from OpenWeatherMap. OpenWeatherMap
 is a service which provides real-time data of the weather. Using the API Key, an 
 HTTP request is sent with the location provided by the end-user to OpenWeatherMap Server.
 The server will return a reply with information of the weather of the specified location. 
 --------------------------------------------------------------------------------------------------------
"""

""" 
 The following packages and modules (tkinter, configparser, PIL)  are used to provide the toolset 
 needed to develop the interface of the Weather Forecast Application. The module requests is used
 to send an HTTP request, with the API Key, for the weather of a location. The module datetime
 is used to determine the current time of where the end-user is located.
""" 
from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests
from PIL import Image, ImageTk, ImageFilter
from datetime import datetime

# The variable URL is used with the API Key to send a HTTP request to OpenWeatherMap to retrieve 
# the weather of the location provided by the end-user.
url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

# The following section of variables is to retrieve the information from the config file for the
# API Key which is required to establish a connection with OpenWeatherMap server to send an
# HTTP request and recieve a reply.
config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

"""
The purpose of the function get_weather is to create and send the HTTP request for the weather
 of the location provided by the end-user. After the connection is established and an HTTP request
 is made, a reply is sent from OpenWeatherMap to retrieve the data. The function then processes
 the data from the reply, and retrives the relevant data regarding the weather of the location. 
 The data is then stored into variables to be used for the variables.  
"""  
def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result.status_code == 200:
        json = result.json()
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        temp_fahrenheit = (temp_kelvin - 273.15) * 9 / 5 + 32
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        final = (city, country, temp_celsius, temp_fahrenheit, icon, weather)
        return final
    else:
        return None
