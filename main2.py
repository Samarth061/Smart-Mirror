from tkinter import *
from PIL import Image, ImageTk
from time import strftime
import requests
from datetime import datetime,timedelta
import pytz


root = Tk()

#Computer dimensions
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

#root.geometry("%dx%d" % (width,height))w
root.state('zoomed')
root.title("Smart Mirror")
root.overrideredirect(True)
root.configure(background='black')#2E2E2E
root.iconbitmap("C:/Users/samar/Downloads/IMG_0249.ico")

#Quit Button
my_button = Button(root, text="Quit" , command = root.destroy)
my_button.place(x=620, y=10)

#Date and time
def time():
    current_date = datetime.now()
    time_now = strftime('%I:%M %p\n' )
    day_date = strftime('%a\n' + '%Y-%m-%d')
    lbl.config(text=time_now)
    lbl2.config(text=day_date)
    lbl.after(1000, time)

lbl = Label(root, font=('Helvetica', 40, 'bold'), bg='black', fg='white')
lbl.place(x = 1000, y = 40)
lbl2 = Label(root, font=('Helvetica', 20), bg='black', fg='white', justify=RIGHT )
lbl2.place(x = 1090, y = 110)
time()

#Weather

bg_image = ImageTk.PhotoImage(Image.open("25501.jpg").resize((800,500)))
bg_color = 'black' #'#4D99E7'

#image icon for each condition
weather_images = {
    "clear sky": "sunny_light.png",
    "few clouds": "partly-sunny_light.png",
    "scattered clouds": "cloudy_light.png",
    "overcast clouds" : "mostly-sunny_light.png",
    "broken clouds": "cloudy_light.png",
    "shower rain": "change-rainlight.png",
    "light rain" : "change-rainlight.png",
    "rain": "night-rain_light.png",
    "thunderstorm": "thunder-storms_light.png",
    "snow": "flurries_light.png",
    "mist": "fog_light.png"
}

def get_image_path(condition):
    condition = str(condition)
    return weather_images.get(condition.lower(), "crescent_moon.png")

def KtoC(Kelvin):
    Celsius = Kelvin - 273.15
    return Celsius
def KtoF(Kelvin):
    Farheneit = (Kelvin - 273.15)*9/5 + 32
    return Farheneit

#Weather API
base_url="https://api.openweathermap.org/data/2.5/weather?"
api_key = "38fc658cdcc4cc6139caf2649ccc7bbb"
city= "Berlin"
complete_url=base_url+"appid="+api_key+"&q="+city
response = requests.get(complete_url).json()
#print(complete_url)

#lon = response['coord']['lon']
#lat = response['coord']['lat']
#Forecast api
exclude = "minute,hourly"
api_key = "38fc658cdcc4cc6139caf2649ccc7bbb"
forecast_url =  f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=imperial"
f_response = requests.get(forecast_url).json()

#print(forecast_url)

frame1 = LabelFrame(root,padx = 10, pady = 10, bg = 'black', borderwidth=0)
frame1.place(x=50,y=60)

#Converting sunrise time to Mankato from London time
sunrise_london = str(datetime.utcfromtimestamp(response['sys']['sunrise']))
sunrise_london_datetime = datetime.fromisoformat(sunrise_london)
sunrise_london_datetime_utc = sunrise_london_datetime.astimezone(pytz.utc)
time_diff = 6
sunrise_manakto_datetime_utc = sunrise_london_datetime_utc - timedelta(hours=time_diff)
mankato_timezone = pytz.timezone("America/Chicago")
mankato_sunrise_datetime = sunrise_manakto_datetime_utc.astimezone(mankato_timezone)

#Converting sunset time to Mankato from London time
sunset_london = str(datetime.utcfromtimestamp(response['sys']['sunset']))
sunset_london_datetime = datetime.fromisoformat(sunset_london)
sunset_london_datetime_utc = sunset_london_datetime.astimezone(pytz.utc)
time_diff = 6
sunset_manakto_datetime_utc = sunset_london_datetime_utc - timedelta(hours=time_diff)
mankato_timezone = pytz.timezone("America/Chicago")
mankato_sunset_datetime = sunset_manakto_datetime_utc.astimezone(mankato_timezone)
#mn_sunset = datetime.isoformat(mankato_sunset_datetime)
current_time = datetime.now()

def Weather():
   #info
   #feels_like = round(response['main']['feels_like']-273.15,1)
   city = response['name']
   temp = response['main']['temp']
   temp_max = response['main']['temp_max']
   temp_min = response['main']['temp_min']
   feels_like = response['main']['feels_like']
   condition = response['weather'][0]['description']

   #temp in C,F
   tempC = round(KtoC(temp),1)
   tempF = round(KtoF(temp),1)
   temp_max_C = round(KtoC(temp_max),1)
   temp_max_F = round(KtoF(temp_max),1)
   temp_min_C = round(KtoC(temp_min),1)
   temp_min_F = round(KtoF(temp_min),1)
   feels_like_C = round(KtoC(feels_like),1)
   feels_like_F = round(KtoF(feels_like),1)

   #fonts
   temp_font = ("Helvetica", 50)
   feels_like_font = ("Monteserrat", 15)
   city_font = ("Helvetica", 30)
   condition_font = ("Helvetica", 20)
   temp_max_font = ("Helvetica", 12)
   day_font = ("Helvetica", 14)
   

   image_label = Label(frame1, image = bg_image)
   #image_label.place(x=0,y=0,relwidth=1,relheight=1)

   temp_lbl = Label(frame1, text = str(tempF) + " °F", fg = 'white', bg = bg_color,font = temp_font, justify= LEFT)
   temp_lbl.grid(column = 1 , row = 1, columnspan= 2)

   condition_lbl = Label(frame1, text = condition  , fg = 'white', bg = bg_color,font = condition_font, justify = LEFT)
   condition_lbl.grid(column = 1 , row = 2)

   city_lbl = Label(frame1, text = city , fg = 'white', bg = bg_color,font = city_font)
   city_lbl.grid(column = 0 , row = 0, columnspan=2)

   temp_max_lbl = Label(frame1, text = "H: " + str(temp_max_F) + " °F\n" + "L: " + str(temp_min_F) + " °F" , fg = 'white', bg = bg_color,font = temp_max_font)
   temp_max_lbl.grid(column = 0 , row = 2)

   def display_weather_forecast(f_response):
    forecast_count = 0
    num_days = 5
    row = 0
    column = 3

    for forecast in f_response['list']:
        date = datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S')
        if date.hour == 12:  # Taking only one forecast per day
            day_label = f" {date.strftime('%A')}" 
            Label(frame1,fg = 'white',bg = bg_color, text="" + day_label[:4],font = day_font,justify = 'center',anchor = 'center').grid(row=row, column=column, padx=10, pady=5, sticky="w")
            
            cond = forecast['weather'][0]['description']
            cond_image = ImageTk.PhotoImage(Image.open(get_image_path(cond)).resize((60, 60)))
            # Create a label and set the image
            cond_lbl = Label(frame1, image=cond_image, bg=bg_color)
            cond_lbl.image = cond_image # Keep a reference to the image object
            cond_lbl.grid(column=column, row=row+1)

            forecast_label = f"{forecast['main']['temp']}°F"#temp
            forecast_label += f"\n{forecast['weather'][0]['description']}"#condition
            Label(frame1,fg = 'white',bg = bg_color, text=forecast_label[:17], font = temp_max_font).grid(row=row+2, column=column, padx=10, pady=5, sticky="w")
            column+=1

            forecast_count += 1
            if forecast_count >= num_days:
                break
   display_weather_forecast(f_response)


Weather()


condition = response['weather'][0]['description']
condition_image = ImageTk.PhotoImage(Image.open(get_image_path(condition)).resize((90,90)))

#sun_moon()     
condition_lbl = Label(frame1, image = condition_image, bg = bg_color )
condition_lbl.grid(column = 0 , row = 1)

#Calendar

Calendarframe = LabelFrame(root,padx = 10, pady = 10, bg = 'black', border=0, width =200, height = 400)
Calendarframe.place(x=800,y=400)
today = datetime.today()

def Cal():
    E_1t = "Event 1"
    EEvent1 = 'Basketball\n'
    EEvent2 = 'You have an Appointment tomorrow\n'

    date = str(datetime.now().date())
    Date = Label(Calendarframe, text = "Today's Events:\n" , fg ='white', bg ='black', justify=LEFT)
    Date.grid(row=0,column = 0)
    
    Event1 = Label(Calendarframe, text = E_1t + "\n" + EEvent2 , bg ='black', fg ='white', justify=LEFT)
    Event1.grid(row=1,column = 0)

Cal()

#News

type = 'sports'
api_Key = '651d6cfbee234d5abf3802bdba9eba82'
api_key = "0dcc3ef4f630463699f2f87b79983d75"
BASE_URL = f"https://newsapi.org/v2/top-headlines/"
params = {
    "sources": "cnn",  # Replace with your desired news source
    "apiKey": api_key,
}

# Making the request to the News API
response = requests.get(BASE_URL, params=params)

Newsframe = LabelFrame(root, padx = 10, pady = 10, bg = 'black', width= 200,height=100)
Newsframe.place(x=60,y=300)

def News():
    
    news_type = Label(Newsframe, text = type, bg = 'black', fg = 'white')
    news_type.pack()

    news = Label(Newsframe, text = "Headlines", bg = 'black', fg = 'white', justify = LEFT)
    news.pack()
    
    
    # Getting the response object
    if response.status_code == 200:
    # The 'response' object now contains information about the top headlines
        news_data = response.json()

    # Extracting descriptions and source names
        articles = news_data.get("articles", [])
        
        for article in articles[:3]:
            description = article.get("description")
            source_name = article.get("source", {}).get("name")
            published_at = article.get("publishedAt")
            

            F1 = Label(Newsframe, text= source_name+ ": " + description, font=("helvetica", 8, "bold"), bg='black', fg='white',wraplength=400, justify=LEFT,anchor= E)
            F1.pack()

            #print(f"Description: {description}")
            #print(f"Source Name: {source_name}")
            #print(f"Published At: {published_at}")
            #print("------")
    else:
        print(f"Error: {response.status_code} - {response.text}")
    
News()


#Photo Gallery


root.mainloop()