from sense_hat import SenseHat
sense = SenseHat()
import time 
import datetime 
#from datetime import timedelta

green = (0, 255, 0) #green
yellow = (255, 255, 0) #yellow
red = (255, 0, 0) #red
blue = (0, 0, 255)
nothing = (0, 0, 0)
white = ( 255, 255, 255 )

run = 0
h_alarm = 60
alarm_air = 0
alarm_drink = 0
air_interval = 60 # test 20 Sekunden, auf 1200 Sekunden (20 Minuten) ändern
drink_interval = 20

fast = 0.05 #scroll_speed

starttime_air = time.time() # Number of seconds since Jan 01st 1970
starttime_drink = time.time()

def smiley_smile():
    R = red
    O = nothing
    smile = [
    O, O, O, O, O, O, O, O,
    O, O, R, O, O, O, R, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, R, O, O, O,
    O, R, O, O, O, O, R, O,
    O, O, R, R, R, R, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    ]
    return smile
    
def smiley_sad():
    R = red
    O = nothing
    sad = [
    O, O, O, O, O, O, O, O,
    O, O, R, O, O, O, R, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, R, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, R, R, R, R, O, O,
    O, R, O, O, O, O, R, O,
    O, O, O, O, O, O, O, O,
    ]
    return sad

sense.clear()
sense.set_pixel(0, 0, 0, 255, 0)

while True:
    for event in sense.stick.get_events():
        #Check if the joystick was pressed
        if event.action == "pressed":
            #Check which direction
            if event.direction == "up": #green / run
                print("Up")
                sense.show_message( "Hello", scroll_speed = fast )
                sense.clear(green) #Up arrow
                run = 1
                time.sleep( 5 )
            elif event.direction == "down": #red / stop run
                print("Down")
                sense.show_message( "Good Bye", scroll_speed = fast )
                sense.clear(red) #Down arrow
                run = 0
                time.sleep( 5 )
            elif event.direction == "right": #yello / pause run
                print("Right")
                sense.show_message( "Break", scroll_speed = fast )
                sense.clear(yellow) #Right arrow
                run = 0
                time.sleep( 5 )
            elif event.direction == "left": #clear / run ---> Was ist hier die Funktion?
                print("left")
                sense.show_message( "???", scroll_speed = fast )
                sense.clear()
                sense.set_pixel( 0, 0, 255, 0, 0 ) #Left arrow
                run = 0
                time.sleep( 5 )
    if run == 1:
        #run script
        print( "running" )
        #Prüfen, ob es Zeit zum Lüften ist
        now_air = time.time()
        now_drink = time.time()
        time_interval_air = now_air - starttime_air
        time_interval_drink = now_drink - starttime_drink
        print( "Time Interval Air " + str( time_interval_air ))
        print( "Time Interval Drink " + str( time_interval_drink ))
        #Lüften prüfen
        if time_interval_air >= air_interval: 
            print( "LÜFTEN" )
            alarm_air = 1
        else:
            print( "NOCH NICHT LÜFTEN" )
        #Trinken prüfen
        if time_interval_drink >= drink_interval: 
            print( "TRINKEN" )
            alarm_drink = 1
        else:
            print( "NOCH NICHT TRINKEN" )
        #Raumklima messen
        p = sense.get_pressure() #pressure
        t = sense.get_temperature() #temperature
        h = sense.get_humidity() #humidity
        print( "Pressure: " + str( p ) )
        print( "Temperature: " + str( t ) )
        print( "Humidity: " + str( h ) )
        if h >=  h_alarm: #Luftfeuchtigkeit überschritten
            alarm_air = 1
        while alarm_air == 1:
            sense.clear( red )
            time.sleep( 2 )
            sense.clear( white )
            time.sleep( 1 )
            sense.show_message( "AIR!", scroll_speed = fast )
            time.sleep( 1 )
            sense.set_pixels(smiley_sad())
            for event in sense.stick.get_events():
                #Check if the joystick was pressed
                if event.action == "pressed":
                    #Check which direction
                    if event.direction == "left": 
                        print( "Ignore: Reset alarm" )
                        sense.show_message("Ignore", scroll_speed = fast )      # Left arrow
                        starttime_air= time.time()
                        alarm_air = 0
                    elif event.direction == "right":
                        print( "Air: Reset alarm" )
                        sense.show_message("Air", scroll_speed = fast )      # Left arrow
                        #Lüften-Countdown
                        air_start = time.time()
                        airing = 1
                        while airing == 1: 
                            air_now = time.time()
                            air_time = air_now - air_start
                            if air_time >= 300: 
                                print( "Lüften beenden" )
                                sense.clear( blue )
                                sense.show_message( "Airing completed", scroll_speed = 0.05  )
                                sense.set_pixels(smiley_smile())
                                time.sleep( 3 )
                                starttime_air= time.time()
                                alarm_air = 0
                                airing = 0
                            elif air_time >= 240:
                                print( "Noch 1 Minute" )
                                sense.show_letter( "1" )
                            elif air_time >= 180:
                                print( "Noch 2 Minuten" )
                                sense.show_letter( "2" )
                            elif air_time >= 120:
                                print( "Noch 3 Minuten" )
                                sense.show_letter( "3" )
                            elif air_time >= 60:
                                print( "Noch 4 Minuten" )
                                sense.show_letter( "4" )
                            else: 
                                print( "Noch 5 Minuten" )
                                sense.show_letter( "5" )
                            time.sleep( 5 )
        while alarm_drink == 1:
            sense.clear( red )
            time.sleep( 2 )
            sense.clear( white )
            time.sleep( 1 )
            sense.show_message( "DRINK!", scroll_speed = fast )
            time.sleep( 1 )
            sense.set_pixels(smiley_sad())
            for event in sense.stick.get_events():
                #Check if the joystick was pressed
                if event.action == "pressed":
                    #Check which direction
                    if event.direction == "left": 
                        print( "Ignore: Reset alarm" )
                        sense.show_message("Ignore", scroll_speed = fast )      # Left arrow
                        starttime_drink= time.time()
                        alarm_drink = 0
                    elif event.direction == "right":
                        print( "Drink: Reset alarm" )
                        sense.show_message("Drink", scroll_speed = fast )      # Left arrow
                        #Lüften-Countdown
                        starttime_drink = time.time()
                        alarm_drink = 0
    # Wait a while and then clear the screen
    time.sleep( 1 )
    sense.clear()
    sense.set_pixel(0, 0, 0, 255, 0)
