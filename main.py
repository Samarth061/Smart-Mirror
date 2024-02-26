from tkinter import *
from PIL import Image, ImageTk
from time import strftime
import requests
from datetime import datetime,timedelta
from tkcalendar import Calendar
import pytz
import textwrap


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
my_button.place(x=1000, y=600)

#Time
def time():
    time_now = strftime('%a, %I:%M %p')
    lbl.config(text=time_now)
    lbl.after(1000, time)

lbl = Label(root, font=('calibri', 40, 'bold'), bg='black', fg='white')
lbl.place(x = 900, y = 40)
time()

#Weather
def KtoC(Kelvin):
    Celsius = Kelvin - 273.15
    return Celsius
def KtoF(Kelvin):
    Farheneit = (Kelvin - 273.15)*9/5 + 32
    return Farheneit

base_url="https://api.openweathermap.org/data/2.5/weather?"
api_key = "3b23acced78f1a72b17d88d0bb41bc20"
city= "Mankato"
complete_url=base_url+"appid="+api_key+"&q="+city
response = requests.get(complete_url).json()

frame1 = LabelFrame(root,padx = 10, pady = 10, bg = 'black', borderwidth=0)
frame1.place(x=100,y=100)

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
   humidity = response['main']['humidity']
   condition = response['weather'][0]['description']
   visibility  = round(response['visibility']/1000,1)

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
   sun_emoji_font = ("TIMES NEW ROMAN",70)
   feels_like_font = ("Monteserrat", 15)
   visibility_font = ("Arial", 8)
   city_font = ("Arial", 20)
   temp_font = ("Helvetica", 20)
   condition_font = ("TIMES NEW ROMAN", 20)
   humidity_font = ("Arial", 8)
   temp_max_font = ("Helvetica", 10)
   sunrise_font = ("Arial", 8)
   sunset_font = ("Arial" , 8)
   
   #Images
   sun_emoji = "\U00002600"
   moon_emoji = "\U0001F314"

   #sun picture declared outside due to inssues within function

   condition_lbl = Label(frame1, text = condition , fg = 'white', bg = 'black',font = condition_font)
   condition_lbl.grid(column = 0 , row = 3)

   feels_like_lbl = Label(frame1, text = "Feels like " + str(feels_like_F) + " °F", fg = 'white', bg = 'black',font = feels_like_font)
   feels_like_lbl.grid(column = 0 , row = 4)

   city_lbl = Label(frame1, text = city , fg = 'white', bg = 'black',font = city_font)
   city_lbl.grid(column = 1 , row = 1)

   temp_lbl = Label(frame1, text = str(tempF) + " °F", fg = 'white', bg = 'black',font = temp_font)
   temp_lbl.grid(column = 1 , row = 2)

   temp_max_lbl = Label(frame1, text = "H: " + str(temp_max_F) + " °F\n" + "L: " + str(temp_min_F) + " °F" , fg = 'white', bg = 'black',font = temp_max_font)
   temp_max_lbl.grid(column = 1 , row = 3)

Weather()
sun = ImageTk.PhotoImage(Image.open("sunny.png"))
moon = ImageTk.PhotoImage(Image.open("crescent_moon.png"))
   
def sun_moon():
    if (current_time < mankato_sunset_datetime):
        return sun
    else:
       return moon
    
#sun_moon()     
sun_lbl = Label(frame1, image = sun,bg = 'black' )
sun_lbl.grid(column = 0 , row = 1, rowspan =2)

#Calendar

Calendarframe = LabelFrame(root,padx = 10, pady = 10, bg = 'black', border=0, width =700, height = 400)
Calendarframe.place(x=100,y=400)
today = datetime.today()

def Cal():
    EEvent1 = 'Event 1 : Basketball\n'
    EEvent2 = 'Event 2 : You have an Appointment tomorrow\n'

    #style = {"bg": "lightgray", "fg": "black", "bd": 2, "highlightthickness": 0, "selectbackground": "skyblue", "font": ("Arial", 10)}
    cal = Calendar(Calendarframe, date_pattern = 'yyyy-mm-dd', year = today.year, month=today.month, day=today.day)
    cal.place(x = 0, y =0)
    date = str(datetime.now().date())
    Date = Label(Calendarframe, text = strftime(" %a ") + date  , fg ='white', bg ='black', justify=LEFT)
    Date.place(x = 0, y =200)
    
    Event1 = Label(Calendarframe, text = EEvent1 + EEvent2 , bg ='black', fg ='white', justify=LEFT)
    Event1.place(x=300,y=0)
    

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

Newsframe = LabelFrame(root, padx = 10, pady = 10, bg = 'black', width= 100,height=100)
Newsframe.place(x=800,y=200)

def scroll_text(self):
        self.canvas.move(self.text_id, 0, -1)
        _, y = self.canvas.coords(self.text_id)
        if y + self.text_height <= 0:
            self.canvas.coords(self.text_id, 0, self.text_height)
        self.after(20, self.scroll_text)

def News():
    
    news_type = Label(Newsframe, text = type, bg = 'black', fg = 'white')
    news_type.pack()

    news = Label(Newsframe, text = "News", bg = 'black', fg = 'white',wraplength=50)
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
            

            F1 = Label(Newsframe, text= description, font=("helvetica", 8, "bold"), bg='black', fg='white',wraplength=300,justify= LEFT)
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