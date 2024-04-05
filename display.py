import time
from main import Time,News,Events,Weather,root,curr_user,get_display

curr_display = get_display(curr_user)
print(curr_display)

def default(user):
    Time()
    News(user)
    Events(user)
    Weather(user)
    root.mainloop()

def display_2(user):
    Time()
    News(user)
    Events(user)
    Weather(user)
    root.mainloop()

def display_3(user):
    Time()
    News(user)
    Events(user)
    Weather(user)
    root.mainloop()

def display_4(user):
    Time()
    News(user)
    Events(user)
    Weather(user)
    root.mainloop()

def display_5(user):
    Time()
    News(user)
    Events(user)
    Weather(user)
    root.mainloop()

def display_6(user):
    Time()
    News(user)
    Events(user)
    Weather(user)
    root.mainloop()

if(curr_display == "Display 2"):
    display_2(curr_user)
elif(curr_display == "Display 3"):
    display_3(curr_user)
elif(curr_display == "Display 4"):
    display_4(curr_user)
elif(curr_display == "Display 5"):
    display_5(curr_user)
elif(curr_display == "Display 6"):
    display_6(curr_user)
else:
    default(curr_user)









