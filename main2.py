from tkinter import *
from PIL import Image, ImageTk
from time import strftime
import requests
from datetime import datetime 
from newsapi import NewsApiClient
import psycopg2
import time
import datetime as dt

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

#Database
while True:
        try:
            conn = psycopg2.connect(
                dbname="railway",
                user="postgres",
                password="b*14GGE23cbcegDcAEDa3d*cd6AC-5*-",
                host="viaduct.proxy.rlwy.net",
                port="15394",
            )
            cursor = conn.cursor()
            print("Database connection was successfull!")
            break
        except Exception as error:
            print("Connecting to database failed.")
            print("Error: ", error)
            time.sleep(2)  # let it keeps trying when failed

#Date and time
class Time():
    def __init__(self):
        self.lbl = Label(root, font=('Roboto', 40, 'bold'), bg='black', fg='white')
        self.lbl.place(x=1000, y=40)
        self.lbl2 = Label(root, font=('Open Sans', 20), bg='black', fg='white', justify=RIGHT)
        self.lbl2.place(x=1090, y=110)
        self.time_display()

    def time_display(self):
        self.current_date = datetime.now()
        time_now = strftime('%I:%M %p\n')
        day_date = strftime('%a\n' + '%Y-%m-%d')
        self.lbl.config(text=time_now)
        self.lbl2.config(text=day_date)
        self.lbl.after(1000, self.time_display)

#Weather
class Weather(LabelFrame):
    weather_images = {
                "clear sky": "sunny_light.png",
                "few clouds": "partly-sunny_light.png",
                "scattered clouds": "cloudy_light.png",
                "overcast clouds" : "cloudy_light.png",
                "broken clouds": "cloudy_light.png",
                "shower rain": "change-rainlight.png",
                "light rain" : "change-rainlight.png",
                "moderate rain" : "night-rain_light.png",
                "rain": "night-rain_light.png",
                "thunderstorm": "thunder-storms_light.png",
                "light snow" : "flurries_light.png",
                "snow": "flurries_light.png",
                "mist": "fog_light.png"
                
            }
    def get_image_path(self,condition):
        condition = str(condition)
        return self.weather_images.get(condition.lower(), "crescent_moon.png")
    
    def __init__(self):
        super().__init__()
        #self.bg_image = ImageTk.PhotoImage(Image.open("25501.jpg").resize((800,500)))
        self.bg_color = 'black' #'#4D99E7'

        self.frame1 = LabelFrame(root,padx = 10, pady = 10, bg = 'black', borderwidth=0)
        self.frame1.place(x=50,y=60)

        #Weather API
        self.base_url="https://api.openweathermap.org/data/2.5/weather?"
        self.api_key = "38fc658cdcc4cc6139caf2649ccc7bbb"
        self.city= "Mankato"
        self.complete_url=self.base_url+"appid="+self.api_key+"&q="+self.city
        self.response = requests.get(self.complete_url).json()

        #All variables for current weather
        self.city = self.response['name']
        self.temp = self.response['main']['temp']
        self.temp_max = self.response['main']['temp_max']
        self.temp_min = self.response['main']['temp_min']
        self.feels_like = self.response['main']['feels_like']
        self.condition = self.response['weather'][0]['description']

        #Forecast api
        self.exclude = "minute,hourly"
        self.api_key = "38fc658cdcc4cc6139caf2649ccc7bbb"
        self.forecast_url =  f"http://api.openweathermap.org/data/2.5/forecast?q={self.city}&appid={self.api_key}&units=imperial"
        self.f_response = requests.get(self.forecast_url).json()
        #lon = response['coord']['lon']
        #lat = response['coord']['lat']

        #Condition image
        self.condition = self.response['weather'][0]['description']
                                               
        self.condition_image = ImageTk.PhotoImage(Image.open(self.get_image_path(self.condition)).resize((90,90)))
        self.condition_lbl = Label(self.frame1, image = self.condition_image, bg = self.bg_color )
        self.condition_lbl.grid(column = 0 , row = 1)

        self.weather_images   
        self.display_current_Weather()
        self.display_weather_forecast(self.f_response)

    
    def KtoC(self,Kelvin):
        Celsius = Kelvin - 273.15
        return Celsius
    def KtoF(self,Kelvin):
        Farheneit = (Kelvin - 273.15)*9/5 + 32
        return Farheneit    
    
    def display_current_Weather(self):
        #temp in C,F
        tempC = round(self.KtoC(self.temp),1)
        tempF = round(self.KtoF(self.temp),1)
        temp_max_C = round(self.KtoC(self.temp_max),1)
        temp_max_F = round(self.KtoF(self.temp_max),1)
        temp_min_C = round(self.KtoC(self.temp_min),1)
        temp_min_F = round(self.KtoF(self.temp_min),1)
        feels_like_C = round(self.KtoC(self.feels_like),1)
        feels_like_F = round(self.KtoF(self.feels_like),1)

        #fonts
        temp_font = ("Helvetica", 50)
        feels_like_font = ("Monteserrat", 15)
        city_font = ("Helvetica", 30)
        condition_font = ("Helvetica", 20)
        temp_max_font = ("Helvetica", 12)
        
        #image_label = Label(self.frame1, image = self.bg_image)
        #image_label.place(x=0,y=0,relwidth=1,relheight=1)

        city_lbl = Label(self.frame1, text = self.city , fg = 'white', bg = self.bg_color,font = city_font)
        city_lbl.grid(column = 0 , row = 0, columnspan=3)

        temp_lbl = Label(self.frame1, text = str(tempF) + " °F", fg = 'white', bg = self.bg_color,font = temp_font, justify= LEFT)
        temp_lbl.grid(column = 1 , row = 1, columnspan= 2)

        condition_lbl = Label(self.frame1, text = self.condition  , fg = 'white', bg = self.bg_color,font = condition_font, justify = LEFT)
        condition_lbl.grid(column = 1 , row = 2)

        temp_max_lbl = Label(self.frame1, text = "H: " + str(temp_max_F) + " °F\n" + "L: " + str(temp_min_F) + " °F" , fg = 'white', bg = self.bg_color,font = temp_max_font)
        temp_max_lbl.grid(column = 0 , row = 2)

    def display_weather_forecast(self,f_response):
        forecast_count = 0
        num_days = 5
        row = 0
        column = 3
        temp_max_font = ("Helvetica", 12)
        day_font = ("Helvetica", 14)

        for forecast in f_response['list']:
            date = datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S')
            if date.hour == 12:  # Taking only one forecast per day
                day_label = f" {date.strftime('%A')}" 
                Label(self.frame1,fg = 'white',bg = self.bg_color, text="" + day_label[:4],font = day_font,justify = 'center',anchor = 'center').grid(row=row, column=column, padx=10, pady=5, sticky="w")
            
                cond = forecast['weather'][0]['description']
                cond_image = ImageTk.PhotoImage(Image.open(self.get_image_path(cond)).resize((60, 60)))
                # Create a label and set the image
                cond_lbl = Label(self.frame1, image=cond_image, bg=self.bg_color)
                cond_lbl.image = cond_image # Keep a reference to the image object
                cond_lbl.grid(column=column, row=row+1)

                forecast_label = f"{forecast['main']['temp']}°F"#temp
                forecast_label += f"\n{forecast['weather'][0]['description']}"#condition
                Label(self.frame1,fg = 'white',bg = self.bg_color, text=forecast_label[:17], font = temp_max_font).grid(row=row+2, column=column, padx=10, pady=5, sticky="w")
                column+=1

                forecast_count += 1
                if forecast_count >= num_days:
                    break
    # #Converting sunrise time to Mankato from London time
    # sunrise_london = str(datetime.utcfromtimestamp(response['sys']['sunrise']))
    # sunrise_london_datetime = datetime.fromisoformat(sunrise_london)
    # sunrise_london_datetime_utc = sunrise_london_datetime.astimezone(pytz.utc)
    # time_diff = 6
    # sunrise_manakto_datetime_utc = sunrise_london_datetime_utc - timedelta(hours=time_diff)
    # mankato_timezone = pytz.timezone("America/Chicago")
    # mankato_sunrise_datetime = sunrise_manakto_datetime_utc.astimezone(mankato_timezone)

    # #Converting sunset time to Mankato from London time
    # sunset_london = str(datetime.utcfromtimestamp(response['sys']['sunset']))
    #  sunset_london_datetime = datetime.fromisoformat(sunset_london)
    # sunset_london_datetime_utc = sunset_london_datetime.astimezone(pytz.utc)
    # time_diff = 6
    # sunset_manakto_datetime_utc = sunset_london_datetime_utc - timedelta(hours=time_diff)
    # mankato_timezone = pytz.timezone("America/Chicago")
    # mankato_sunset_datetime = sunset_manakto_datetime_utc.astimezone(mankato_timezone)
    # #mn_sunset = datetime.isoformat(mankato_sunset_datetime)
    # current_time = datetime.now()

#Events
class Events(LabelFrame):

    def __init__(self):
        super().__init__()
        self.day_font = ("Roboto", 15)
        self.date_font = ("Roboto", 18)
        self.month_font = ("Helvetica", 12)
        self.event_time_font = ("Helvetica", 12)
        self.event_details_font = ("Helvetica", 18)
        self.event_address_font = ("Helvetica", 12)

        self.labelframe = LabelFrame(root, padx = 10,pady = 10, bg = 'black', fg = 'white', border=0, width =200, height = 400)
        self.labelframe.place(x=950,y=250)

        self.row = 0
        self.column = 0
        self.get_tasks_from_database()

    def get_Events(self,user_id):
        cursor.execute("""SELECT topic, location, event_date, start_time, end_time FROM base_event WHERE user_id = %s""", (user_id,))
    
        events = cursor.fetchall()
        return events
    
    def get_tasks_from_database(self):
        events = self.get_Events(10)

        for event in events:
            event_date = dt.datetime.strptime(str(event[2]), '%Y-%m-%d %H:%M:%S+00:00')
            start_time = dt.datetime.strptime(str(event[3]), '%H:%M:%S')
            end_time = dt.datetime.strptime(str(event[4]), '%H:%M:%S')

            topic = event[0]
            location = event[1]
            day_name = event_date.strftime("%a")
            day_number = event_date.day
            month = event_date.strftime("%b")
            start_time = start_time.strftime('%I:%M %p')
            end_time = end_time.strftime('%I:%M %p')

            event_day = Label(self.labelframe,text = day_name,bg = 'black', fg= 'white',font= self.day_font )
            event_day.grid(row = self.row, column = self.column)

            event_date = Label(self.labelframe,text = day_number,bg = 'black', fg= 'white',width=2, height=1,
                               font= self.date_font,highlightthickness=1, highlightbackground="white" )
            event_date.grid(row = self.row+1,column = self.column)

            event_month_name = Label(self.labelframe,text = month + "\n" ,bg = 'black', fg= 'white',font= self.month_font)
            event_month_name.grid(row = self.row+2,column = self.column)

            event_time = Label(self.labelframe, text = start_time + " - " + end_time,bg = 'black', fg= 'white',font=self.event_time_font, justify=LEFT)
            event_time.grid(row=self.row, column = self.column + 1,sticky="w")
        
            event_details = Label(self.labelframe, text = topic ,bg = 'black', fg= 'white',font=self.event_details_font, justify=LEFT )
            event_details.grid(row=self.row+1, column = self.column + 1,sticky = "w")

            event_address = Label(self.labelframe, text = location + "\n" ,bg = 'black', fg= 'white',font=self.event_address_font, justify=LEFT)
            event_address.grid(row=self.row+2, column = self.column + 1, sticky = "w")

            self.row += 3

#News
class News(LabelFrame):
    def __init__(self,*args,**kwargs):
        #This superclass is a constructor for the News Frame
        super().__init__(*args, **kwargs)
        #api_key = "0dcc3ef4f630463699f2f87b79983d75"
        self.api_key = '651d6cfbee234d5abf3802bdba9eba82'
        self.newsapi = NewsApiClient(self.api_key)
        self.params = {
            'q': '',
            'language': 'en',
            'sources' : 'espn',
            #'country' : 'us'
        }
        self.news_articles = []
        self.current_index = 0
        self.batch_size = 4
        self.F1 = Label()

        self.Newsframe = LabelFrame(root, padx = 10, pady = 10, bg = 'black', width= 200,height=100,borderwidth=0)
        self.Newsframe.place(x=60,y=440)

        self.headline_font = ("SEOGE UI",22)
        self.news = Label(self.Newsframe, text = "Your morning News!", bg = 'black', fg = 'white', justify = LEFT,font = self.headline_font)
        self.news.grid(row = 0, column =0,sticky='w')

        self.image = Image.open('search.png').resize((30, 30))
        self.search_image = ImageTk.PhotoImage(self.image)
        # Create a label widget to display the image
        self.search = Label(self.Newsframe, image=self.search_image,bg='black')
        self.search.grid(row=1, column=0,sticky='w')
        # Keep a reference to the PhotoImage object
        self.search.image = self.search_image

        keyword_font = ('Helvetica',15)
        if 'q' not in self.params or self.params['q'] == '':
            self.keyword = Label(self.Newsframe, text="Everything", bg='black', fg='white', justify=LEFT, font=keyword_font)
            self.keyword.place(x=self.search.winfo_reqwidth() + 10, y=self.search.winfo_reqheight()+4)
        else:
            self.keyword = Label(self.Newsframe, text=self.params.get('q'), bg='black', fg='white', justify=LEFT, font=keyword_font)
            self.keyword.place(x=self.search.winfo_reqwidth() + 10, y=self.search.winfo_reqheight()+4)
        
        self.fetch_news()

    #This functions fetches the first set of news and new ones every 10 minutes
    def fetch_news(self):
        news_response = self.newsapi.get_everything(**self.params)
        if news_response['status'] == 'ok':
            self.news_articles = news_response['articles']
            self.show_news()
            # Schedule next fetch after 10 minutes (600 seconds)
            self.after(864000, self.fetch_news)  # 600,000 milliseconds = 10 minutes
        else:

            self.F1 = Label(self.Newsframe, text= str(news_response['code']), font=("helvetica", 12, "bold"), bg='black',
                         fg='white', wraplength=800)
            # Schedule next fetch after 1 minute (60 seconds)
            self.after(60000, self.fetch_news)  # 60,000 milliseconds = 1 minute

    #This function shows the actual news on the frame
    def show_news(self):
        news = ""
        starting_row =3
        
        for article in self.news_articles[self.current_index:self.current_index + self.batch_size]:
            description = article['title']
            source_name = article['source']['name']
            news = source_name + ": " + description
            #self here might be an error check it first
            self.F1 = Label(self.Newsframe, text= news, font=("helvetica", 12, "bold"), bg='black',
                         fg='white', wraplength=800)
            self.F1.grid(row=starting_row, column=0, sticky="w")    
            starting_row+=1
            self.after(5000,self.F1.destroy)
        self.after(5000, self.show_next_news)
    
    #This funciton fetches new batch of news
    def show_next_news(self):
        # Show the next batch of news articles
        self.current_index += self.batch_size
        if self.current_index >= len(self.news_articles):
            self.current_index = 0
        self.show_news()

    
#Photo Gallery
if __name__ == '__main__':
    Time()
    Weather()
    News()
    Events()

    root.mainloop()