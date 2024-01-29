from tkinter import *
from PIL import Image, ImageTk
from time import strftime
import requests
import json
import datetime as dt

root = Tk()

#Computer dimensions
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

#root.geometry("%dx%d" % (width,height))w
root.state('zoomed')
root.title("Smart Mirror")
root.overrideredirect(True)
root.configure(background='black')
root.iconbitmap("C:/Users/samar/Downloads/IMG_0249.ico")

#Quit Button
my_button = Button(root, text="Quit" , command = root.destroy)
my_button.place(x=1000, y=400)

#Time
def time():
    string = strftime('%I:%M %p')
    lbl.config(text=string)
    lbl.after(1000, time)

lbl = Label(root, font=('calibri', 40, 'bold'),
            background='black',
            foreground='white')
lbl.place(x = 1000, y = 40)
time()

#Weather

base_url="https://api.openweathermap.org/data/2.5/weather?"
api_key = "3b23acced78f1a72b17d88d0bb41bc20"
city= "London"
complete_url=base_url+"appid="+api_key+"&q="+city
response = requests.get(complete_url).json()

frame1 = LabelFrame(root, padx = 10, pady = 10, bg = 'black')
frame1.place(x=100,y=200)

def weather():
   #info
   city = response['name']
   temp = round(response['main']['temp']-273.15,1)
   temp_max = round(response['main']['temp_max']-273.15,1)
   temp_min = round(response['main']['temp_min']-273.15,1)
   feels_like = round(response['main']['feels_like']-273.15,1)
   humidity = response['main']['humidity']
   cloudy = response['weather'][0]['description']
   visibility  = round(response['visibility']/1000,1)
   sunrise = dt.datetime.utcfromtimestamp(response['sys']['sunrise']).strftime('%I:%M:%p')
   sunset = dt.datetime.utcfromtimestamp(response['sys']['sunset']).strftime('%I:%M:%p')

   #fonts
   sun_emoji_font = ("TIMES NEW ROMAN",40)
   feels_like_font = ("Arial", 8)
   visibility_font = ("Arial", 8)
   city_font = ("Arial", 10)
   temp_font = ("Arial", 16)
   cloudy_font = ("Arial", 12)
   humidity_font = ("Arial", 8)
   temp_max_font = ("Arial", 8)
   sunrise_font = ("Arial", 8)
   sunset_font = ("Arial" , 8)
   
   #Images
   sun_emoji = "\U00002600"
   moon_emoji = "\U0001F314"

   def sun_moon():
       hour = int(strftime('%H'))
       if hour > 12:
           return sun_emoji
       elif hour < 24:
            return moon_emoji
   
   sun_lbl = Label(frame1, text = sun_moon(), fg = 'white', bg = 'black',font= sun_emoji_font)
   sun_lbl.grid(column = 0 , row = 1, rowspan= 2)

   feels_like_lbl = Label(frame1, text = "Feels like " + str(feels_like) + " °C", fg = 'white', bg = 'black',font = feels_like_font)
   feels_like_lbl.grid(column = 0 , row = 3)

   visibility_lbl = Label(frame1, text = "Visibility " + str(visibility) +" km", fg = 'white', bg = 'black',font = visibility_font)
   visibility_lbl.grid(column= 0, row = 4)

   city_lbl = Label(frame1, text = city , fg = 'white', bg = 'black',font = city_font)
   city_lbl.grid(column = 1 , row = 1)

   temp_lbl = Label(frame1, text = str(temp) + " °C", fg = 'white', bg = 'black',font = temp_font)
   temp_lbl.grid(column = 1 , row = 2)

   cloudy_lbl = Label(frame1, text = cloudy  , fg = 'white', bg = 'black',font = cloudy_font)
   cloudy_lbl.grid(column = 1 , row = 3)

   humidity_lbl = Label(frame1, text = "Humidity " + str(humidity) + " %", fg = 'white', bg = 'black',font = humidity_font)
   humidity_lbl.grid(column = 1 , row = 4)

   temp_max_lbl = Label(frame1, text = "H: " + str(temp_max) + " °C\n" + "L: " + str(temp_min) + " °C" , fg = 'white', bg = 'black',font = temp_max_font)
   temp_max_lbl.grid(column = 2 , row = 1,rowspan = 2)

   sunrise_lbl = Label(frame1, text = "Sunrise: " + str(sunrise), fg = 'white', bg = 'black',font = sunrise_font)
   sunrise_lbl.grid(column = 2 , row = 3)

   sunset_lbl = Label(frame1, text = "Sunset: " + str(sunset)  , fg = 'white', bg = 'black',font = sunset_font)
   sunset_lbl.grid(column = 2 , row = 4)

weather()

print(response)



root.mainloop()