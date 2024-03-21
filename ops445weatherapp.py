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

"""
 The function get_background_image is used to determine the background image for the interface.
 The background image is determined by the current time of the end-user at their location. 
 The hour of the time is used to determine whether the background image display either day
 or night. If the current hour is greather than 7 (7:00AM) but less than 19 (7:00PM), then
 the background image is daytime. If not, than the background image is night. 
""" 
def get_background_image():
    now = datetime.now()
    current_hour = now.hour
    if current_hour >= 7 and current_hour < 19:
        return 'weather_icons/daytime.png'
    else:
        return 'weather_icons/night.png'

"""
 The function search is used to retrieve the location from the end-user. The input is stored in
 a variable which is then called in a variable weather. The weather variable calls the get_weather
 function using the city variable as the parameter. If the weather data is  able to be retrieved
 from OpenWeatherMap, the information is displayed on the interface along with the mataching
 images which correspond with the weather. However, if the weather data can not be retrieved 
 it is because the location provided by the end-user does not exist. A message is displayed on the
 interface telling the end-user the location provided could not be found.
"""
def search():
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        location_lbl['text'] = '{}, {}'.format(weather[0], weather[1])
        background_image_path = get_background_image()
        img = Image.open(background_image_path)  # Load the background image
        img = img.filter(ImageFilter.BLUR)  # blur

        # Resized weather icon
        icon_size = min(img.size) // 5

        
        weather_icon = Image.open('weather_icons/{}.png'.format(weather[4]))
        weather_icon = weather_icon.resize((icon_size, icon_size))

        
        icon_position = ((img.width - weather_icon.width) // 2, (img.height - weather_icon.height) // 2)

        
        img.paste(weather_icon, icon_position, weather_icon)

        photo = ImageTk.PhotoImage(img)
        photo = ImageTk.PhotoImage(img)
        background_label.config(image=photo)  # image background
        background_label.image = photo
     
        temp_lbl['text'] = '{:.2f}°C {:.2f}°F'.format(weather[2], weather[3])
        weather_lbl['text'] = weather[5]
    else:
        messagebox.showerror('Error', 'Cannot find city {}'.format(city))

"""
 The following section is to create the visual and interfactive elements of the Weather Forecast Application 
 which the end-user will be engaing with. The visual elements is to create an interace which does interests the
 end-user and makes them want to engaage with the application. Overall, this section will create the interface which is 
 front-end that the end-user interacts with. 
""" 
app = Tk()
app.title("Final Project Weather App")
app.geometry('700x350')

background_label = Label(app, bg='white', bd=0)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

weather_icon_label = Label(app, bg='white')
weather_icon_label.pack()

city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()

search_btn = Button(app, text='Search weather', width=12, command=search)
search_btn.pack()


location_lbl = Label(app, text='', font=('bold', 20))
location_lbl.pack()

temp_lbl = Label(app, text='', bg='white')
temp_lbl.pack()

weather_lbl = Label(app, text='', bg='white')
weather_lbl.pack()

background_image_path = get_background_image()
img = Image.open(background_image_path)
img = img.filter(ImageFilter.BLUR)  # blur
photo = ImageTk.PhotoImage(img)
background_label.config(image=photo)  
background_label.image = photo

"""
 The command app.mainloop() is used to ensure the application remains in an infinite loop. 
 The command which is part of the tkinter package, ensures that the application is in a loop
 and will not time-out. Furthermore, the application is in loop to allow the end-user to 
 interact with the application after it has searched for a location; allowing multiple
 searches.
""" 
app.mainloop()
