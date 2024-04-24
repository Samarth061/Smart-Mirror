from tkinter import *
from PIL import Image, ImageTk
from time import strftime
import requests
from datetime import datetime 
from newsapi import NewsApiClient
import psycopg2
import time
import datetime as dt #Need this for events due to some issues

root = Tk()

#Computer dimensions
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

#root.geometry("%dx%d" % (width,height))w
#root.state('zoomed')
root.title("Smart Mirror")
root.overrideredirect(True)
root.configure(background='black')#2E2E2E
root.geometry(f"{width}x{height}")

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

#Choose the current user from MirrorSync's table 
def choose_user():
    cursor.execute(
        """SELECT user_id,username FROM base_mirrorsync""",
    )
    user = cursor.fetchone()
    return user

# Get mirror display number of a user using id
def get_display(user_id):
    cursor.execute(
        """SELECT display FROM base_mirrordisplay where user_id = %s""", (user_id,)
    )
    display = cursor.fetchone()

    return display[0]

#Date and time
class Time():
    def __init__(self):
        self.x_coordinate = 1600 #Label x position
        self.y_coordinate = 58   #Label y position
        
        self.alignment = RIGHT
        #Time Label
        self.time = Label(root, font=('Roboto', 40, 'bold'), bg='black', fg='white')
        self.time.place(x=self.x_coordinate, y=self.y_coordinate)
        #Day Date Label
        self.day_date = Label(root, font=('Open Sans', 20), bg='black', fg='white', 
                              justify = self.alignment)
        self.day_date.place(x=self.x_coordinate+120, y=self.y_coordinate+65) 
        self.time_display()

    #Shows current date and time
    def time_display(self):
        self.current_date = datetime.now()
        time_now = strftime('%I:%M %p\n')
        day_date = strftime('%A\n' + '%Y-%m-%d')
        self.time.config(text=time_now)
        self.day_date.config(text=day_date)
        self.time.after(1000, self.time_display)

    def change_coordinates(self, new_x, new_y):
        # Method to change coordinates
        self.x_coordinate = new_x
        self.y_coordinate = new_y
        self.time.place(x=self.x_coordinate, y=self.y_coordinate)
        if self.alignment == RIGHT:
            self.day_date.place(x=self.x_coordinate+120, y=self.y_coordinate+65)
        else:
            self.day_date.place_configure(x=self.x_coordinate, y=self.y_coordinate+65)
    

    def change_alignment(self, alignment):
        #Method to change alignment
        if alignment == 'right':
            self.alignment = RIGHT
            self.day_date.config(justify = self.alignment)
            self.day_date.place_configure(x=self.x_coordinate+120, y=self.y_coordinate+65)
        elif alignment == 'left':
            self.alignment = LEFT
            self.day_date.config(justify = self.alignment)
            self.day_date.place_configure(x=self.x_coordinate, y=self.y_coordinate+65)

#Weather
def get_location(user_id):
        cursor.execute(
        """SELECT location FROM base_weather WHERE user_id = %s""", (user_id,)
        )
        location = cursor.fetchone()

        return location[0]

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
                "mist": "fog_light.png",
                "smoke": "fog_light.png",
                "haze" : "fog_light.png"          
            }
    
    # Get the image from saved images
    def get_image_path(self,condition):
        condition = str(condition)
        return self.weather_images.get(condition.lower(), "crescent_moon.png")
    

    def __init__(self,user_id):
        super().__init__()
        #self.bg_image = ImageTk.PhotoImage(Image.open("25501.jpg").resize((800,500)))
        self.bg_color = 'black' #'#4D99E7'
        self.x_coordinate = 10
        self.y_coordinate = 40
        #Weather Frame that holds all the individual widgets
        self.USER_ID = user_id
        self.weatherframe = LabelFrame(root,padx = 10, pady = 10, bg = 'black', borderwidth=0,width=10,height=10)
        self.weatherframe.place(x=self.x_coordinate,y=self.y_coordinate)
        
        #OpenWeather API
        self.base_url="https://api.openweathermap.org/data/2.5/weather?"
        self.api_key = "38fc658cdcc4cc6139caf2649ccc7bbb"
        self.city= get_location(self.USER_ID)
        self.complete_url=self.base_url+"appid="+self.api_key+"&q="+self.city
        self.response = requests.get(self.complete_url).json()

        #Querying all variables for current weather from OpenWeather API
        self.city = self.response['name']
        self.temp = self.response['main']['temp']
        self.temp_max = self.response['main']['temp_max']
        self.temp_min = self.response['main']['temp_min']
        self.feels_like = self.response['main']['feels_like']
        self.condition = self.response['weather'][0]['description']

        #Forecast API
        self.exclude = "minute,hourly"
        self.api_key = "38fc658cdcc4cc6139caf2649ccc7bbb"
        self.forecast_url =  f"http://api.openweathermap.org/data/2.5/forecast?q={self.city}&appid={self.api_key}&units=imperial"
        self.f_response = requests.get(self.forecast_url).json()
        #lon = response['coord']['lon']
        #lat = response['coord']['lat']

        #Condition image
        self.condition = self.response['weather'][0]['description']

        self.condition_image = ImageTk.PhotoImage(Image.open(self.get_image_path(self.condition)).resize((100,100)))
        self.condition_lbl = Label(self.weatherframe, image = self.condition_image, bg = 'black' )
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
        
        #image_label = Label(self.weatherframe, image = self.bg_image)
        #image_label.place(x=0,y=0,relwidth=1,relheight=1)

        city_lbl = Label(self.weatherframe, text = "        "+self.city , fg = 'white', 
                         bg = self.bg_color,font = city_font)
        city_lbl.grid(column = 0 , row = 0, columnspan=3)

        temp_lbl = Label(self.weatherframe, text = " " + str(tempF) + " °F", fg = 'white', 
                         bg = self.bg_color,font = temp_font, justify= LEFT)
        temp_lbl.grid(column = 1 , row = 1, columnspan= 2)

        condition_lbl = Label(self.weatherframe, text = " " +self.condition  , fg = 'white', 
                              bg = self.bg_color,font = condition_font, justify = LEFT)
        condition_lbl.grid(column = 1 , row = 2)

        temp_max_lbl = Label(self.weatherframe, text = "H: " + str(temp_max_F) + " °F\n" + "L: " + 
                             str(temp_min_F) + " °F" , fg = 'white', bg = self.bg_color,font = temp_max_font)
        temp_max_lbl.grid(column = 0 , row = 2)

    def display_weather_forecast(self,f_response):
        #Start day
        forecast_count = 0
        #How many days to show
        num_days = 4
        #This is the row that it starts from inside the weatherframe
        row = 0
        #This is the column that it starts from inside the weatherframe
        column = 3
        temp_max_font = ("Helvetica", 12)
        day_font = ("Helvetica", 14)

        for forecast in f_response['list']:
            date = datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S')
            if date.hour == 12:  # Taking only one forecast per day
                day_label = f" {date.strftime('%A')}" 
                Label(self.weatherframe,fg = 'white',bg = self.bg_color, text=" " + day_label[:4],
                      font = day_font,justify = 'center',
                      anchor = 'center').grid(row=row, column=column, padx=10, pady=5, sticky="nsew")
            
                cond = forecast['weather'][0]['description']
                cond_image = ImageTk.PhotoImage(Image.open(self.get_image_path(cond)).resize((70, 70)))
                # Create a label and set the image
                cond_lbl = Label(self.weatherframe, image=cond_image, bg=self.bg_color)
                cond_lbl.image = cond_image # Keep a reference to the image object
                cond_lbl.grid(column=column, row=row+1)

                forecast_label = f"{forecast['main']['temp']}°F \n{forecast['weather'][0]['description']}"  #temp
               
                Label(self.weatherframe,fg = 'white',bg = self.bg_color, text=forecast_label, font = temp_max_font,width =11).grid(row=row+2, column=column, padx=10, pady=5, sticky="w")
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
    def change_coordinates(self, new_x, new_y):
        # Method to change coordinates
        self.x_coordinate = new_x
        self.y_coordinate = new_y
        self.weatherframe.place(x=self.x_coordinate, y=self.y_coordinate)

#Events
def get_Events(user_id):
        cursor.execute("""SELECT topic, location, event_date, start_time, 
                       end_time FROM base_event WHERE user_id = %s ORDER BY event_date ASC,
                       start_time ASC;""", (user_id,))
    
        events = cursor.fetchall()
        return events
        

class Events(LabelFrame):

    def __init__(self,user_id):
        self.USER_ID = user_id
        super().__init__()
        self.day_font = ("Roboto", 18)
        self.date_font = ("Roboto", 21)
        self.month_font = ("Helvetica", 15)
        self.event_time_font = ("Helvetica", 15)
        self.event_details_font = ("Helvetica", 21)
        self.event_address_font = ("Helvetica", 15)

        self.x_coordinate = 10
        self.y_coordinate = 300
        self.eventframe = LabelFrame(root, padx = 10,pady = 10, bg = 'black', 
                                     fg = 'white', border=0, width =200, height = 400)
        self.eventframe.place(x=self.x_coordinate,y=self.y_coordinate)

        self.titlelabel = Label(self.eventframe, text = "Today's Events", 
                                bg = 'black', fg = 'white', font = self.event_details_font)
        #self.titlelabel.grid(row = 0, column = 0)
        self.row = 1
        self.column = 0
        self.event_count = 0
        self.get_tasks_from_database()
    
    def get_tasks_from_database(self):
        events = get_Events(self.USER_ID)
        current_date = dt.date.today()

        def is_within_next_4_days(event_date, current_date):
            # Calculate the date range for the next 4 days
            next_4_days = [current_date + dt.timedelta(days=i) for i in range(4)]

            # Check if event_date falls within the next 4 days
            return event_date in next_4_days
        def is_within_current_time(event_time, current_time):
            if event_time >= current_time:
                pass
          

        for event in events:
            event_date = dt.datetime.strptime(str(event[2]), '%Y-%m-%d %H:%M:%S+00:00').date()
            start_time = dt.datetime.strptime(str(event[3]), '%H:%M:%S')
            end_time = dt.datetime.strptime(str(event[4]), '%H:%M:%S')

            topic = event[0]
            location = event[1]
            day_name = event_date.strftime("%a")
            day_number = event_date.day
            month = event_date.strftime("%b")
            start_time = start_time.strftime('%I:%M %p')
            end_time = end_time.strftime('%I:%M %p')

            if (is_within_next_4_days(event_date, current_date)):
                event_day = Label(self.eventframe,text = day_name,bg = 'black', fg= 'white',font= self.day_font )
                event_day.grid(row = self.row, column = self.column)

                event_date = Label(self.eventframe,text = day_number,bg = 'black', fg= 'white',width=2, height=1,
                               font= self.date_font,highlightthickness=1, highlightbackground="white" )
                event_date.grid(row = self.row+1,column = self.column)

                event_month_name = Label(self.eventframe,text = month + "\n" ,bg = 'black', fg= 'white',font= self.month_font)
                event_month_name.grid(row = self.row+2,column = self.column)

                event_time = Label(self.eventframe, text = start_time + " - " + end_time,bg = 'black', fg= 'white',font=self.event_time_font, justify=LEFT)
                event_time.grid(row=self.row, column = self.column + 1,sticky="w")
        
                event_details = Label(self.eventframe, text = topic ,bg = 'black', fg= 'white',font=self.event_details_font, justify=LEFT )
                event_details.grid(row=self.row+1, column = self.column + 1,sticky = "w")

                event_address = Label(self.eventframe, text = location + "\n" ,bg = 'black', fg= 'white',font=self.event_address_font, justify=LEFT)
                event_address.grid(row=self.row+2, column = self.column + 1, sticky = "w")

                self.row += 3
                self.event_count += 1
            
            if(self.event_count == 4):
                break

            elif(event_date == None):
                event_date = Label(self.eventframe,text = "No events",bg = 'black', fg= 'white',width=2, height=1,
                               font= self.date_font,highlightthickness=1, highlightbackground="white" )
                event_date.grid(row = self.row+1,column = self.column)
        
    def change_coordinates(self, new_x, new_y):
        # Method to change coordinates
        self.x_coordinate = new_x
        self.y_coordinate = new_y
        self.eventframe.place(x=self.x_coordinate, y=self.y_coordinate)
                 
#News
def get_news(user_id):
        cursor.execute(
         """SELECT source, topic FROM base_news where user_id = %s""", (user_id,)
        )
        news = cursor.fetchone()
        return news
class News(LabelFrame):
    
    def __init__(self,user_id,*args,**kwargs):
        self.USER_ID = user_id
        #This superclass is a constructor for the News Frame
        super().__init__(*args, **kwargs)
        source = get_news(self.USER_ID)[0]
        #api_key = "0dcc3ef4f630463699f2f87b79983d75"
        self.api_key = '651d6cfbee234d5abf3802bdba9eba82'
        self.newsapi = NewsApiClient(self.api_key)
        self.params = {
            'q': '',
            'language': 'en',
            'sources' : source,
            #'country' : 'us'
        }
        self.news_articles = []
        self.current_index = 0
        self.batch_size = 4
        self.F1 = Label()

        self.x_coordinate = 1100
        self.y_coordinate = 840
        self.Newsframe = LabelFrame(root, padx = 10, pady = 10, bg = 'black', width= 200,height=100,borderwidth=0)
        self.Newsframe.place(x=self.x_coordinate, y=self.y_coordinate)

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
            self.F1 = Label(self.Newsframe, text= news, font=("helvetica", 15, "bold"), bg='black',
                         fg='white', wraplength=800)
            self.F1.grid(row=starting_row, column=0, sticky="w")    
            starting_row+=1
            self.after(20000,self.F1.destroy)
        self.after(20000, self.show_next_news)
    
    #This function fetches new batch of news
    def show_next_news(self):
        # Show the next batch of news articles
        self.current_index += self.batch_size
        if self.current_index >= len(self.news_articles):
            self.current_index = 0
        self.show_news()

    def change_coordinates(self, new_x, new_y):
        # Method to change coordinates
        self.x_coordinate = new_x
        self.y_coordinate = new_y
        self.Newsframe.place(x=self.x_coordinate, y=self.y_coordinate)

class Current_User():

    def __init__(self,info):
        self.userid = info[0]
        self.username = info[1]
        self.x_coordinate = 10
        self.y_coordinate = 0
        self.user_info = Label(root, text =  f"{self.username}" ,
                               font=('Open Sans', 10), bg='black', fg='white', 
                               justify=LEFT)
        self.user_info.place(x=self.x_coordinate, y=self.y_coordinate)
    
    def change_coordinates(self, new_x, new_y):
        # Method to change coordinates
        self.x_coordinate = new_x
        self.y_coordinate = new_y
        self.user_info.place(x=self.x_coordinate, y=self.y_coordinate)



#time - 1600,58
#Weather - 50,40
#Events - 60,300
#News - 1100,740
#current user - 10,0

if __name__ == '__main__':
    Time().change_coordinates(60,40)
    News(21).change_coordinates(60,840)
    Events(21).change_coordinates(50,300)
    Weather(21).change_coordinates(1000,40)
    Current_User(choose_user()).change_coordinates(1800,0)

    root.mainloop()



