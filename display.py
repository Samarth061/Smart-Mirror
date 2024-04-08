from main import Time,News,Events,Weather,root,choose_user,get_display

def default(user):
    Time()
    News(user)
    Events(user)
    Weather(user) 
    
def display_2(user):
    Time().change_coordinates(10,10)
    News(user).change_coordinates(1,100)
    Events(user).change_coordinates(400,400)
    Weather(user).change_coordinates(600,600)
   
def display_3(user):
    Time()
    News(user)
    Events(user)
    Weather(user)
    
def display_4(user):
    Time()
    News(user)
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
    
    for widget in root.winfo_children():
        widget.place_forget()
    
    curr_userid = choose_user()
    curr_display = get_display(curr_userid)

    if(curr_display == "Display 2"):
        display_2(curr_userid)

    elif(curr_display == "Display 3"):
        display_3(curr_userid)
       
    elif(curr_display == "Display 4"):
        display_4(curr_userid)
  
    elif(curr_display == "Display 5"):
        display_5(curr_userid)
      
    elif(curr_display == "Display 6"):
        display_6(curr_userid)
    else:
        default(curr_userid)

    root.after(5000, lambda : update_gui())
    
update_gui()
root.mainloop()
