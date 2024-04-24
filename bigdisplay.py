from bigmain import Time,News,Events,Weather,Current_User
from bigmain import root,choose_user,get_display,get_location,get_Events,get_news

prev_userid = 0
prev_display = 0
prev_location = get_location(15)
prev_Events = get_Events(15)
prev_news = get_news(15) 

def default(user):   
    Time()
    News(user)
    Events(user)
    Weather(user) 
    
def display_2(user):
    Time().change_coordinates(60,40)
    News(user).change_coordinates(60,840)
    Events(user).change_coordinates(50,300)
    Weather(user).change_coordinates(1000,40)    
    
def display_3(user):
    Time()
    News(user)
    Events(user)
    Weather(user)
    
def display_4(user):
    Time()
    News(user).change_coordinates(60,800)
    Events(user)
    Weather(user)
    
def display_5(user):
    Time()
    News(user)
    Events(user)
    Weather(user)
    
def display_6(user):
    Time()
    News(user)
    Events(user)
    Weather(user)

def update_gui():
    global prev_userid,prev_display,prev_location,prev_Events,prev_news
    
    #Userid and name
    curr_info = choose_user()
    #Chooses current user and saves the user id in curr_userid
    curr_userid = curr_info[0]
    #Chooses the display style and user choices  
    curr_display = get_display(curr_userid)
    #Chooses current user location
    curr_location = get_location(curr_userid)
    #Chooses current user Events  
    curr_Events = get_Events(curr_userid)
    #Chooses current user news source
    curr_news = get_news(curr_userid)
    
    GUI_change_condition = (curr_userid != prev_userid) or (curr_display != prev_display) or (curr_location != 
                                prev_location) or (curr_Events != prev_Events) or (curr_news != prev_news)
    if(GUI_change_condition):
        #Forget all the current widgets in the root
        for widget in root.winfo_children():
            widget.destroy()

        if(curr_display == "Display 2"):
            display_2(curr_userid)
            Current_User(choose_user()).change_coordinates(1800,0)

        elif(curr_display == "Display 3"):
            display_3(curr_userid)
            Current_User(curr_info)
       
        elif(curr_display == "Display 4"):
            display_4(curr_userid)
            Current_User(curr_info)
  
        elif(curr_display == "Display 5"):
            display_5(curr_userid)
            Current_User(curr_info)
      
        elif(curr_display == "Display 6"):
            display_6(curr_userid)
            Current_User(curr_info)

        else:
            default(curr_userid)
            Current_User(curr_info)
    
    prev_userid = curr_userid 
    prev_display = curr_display
    prev_location = curr_location
    prev_Events = curr_Events
    prev_news = curr_news

    #recursive function that calls and updates the GUI
    root.after(5000, lambda : update_gui())
    
update_gui()

root.mainloop()


 