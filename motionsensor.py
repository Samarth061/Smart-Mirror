from gpiozero import MotionSensor
import neopixel
import board
import time

# Define the number of pixels and GPIO pin for the NeoPixel
NUM_PIXELS = 150  # Change this according to your setup
PIN_PIXEL = board.D18  # Change this according to your setup

# Initialize NeoPixel strip
pixels = neopixel.NeoPixel(PIN_PIXEL, NUM_PIXELS)

# Initialize PIR sensor
pir = MotionSensor(4)  # Change GPIO pin according to your setup

def turn_on_lights():
    # Turn on NeoPixel lights
    pixels.fill((122, 122, 122))  # Red color
    pixels.show()

def turn_off_lights():
    # Turn off NeoPixel lights
    pixels.fill((0, 0, 0))  # Turn off all pixels
    pixels.show()

try:
    while True:
        pir.wait_for_motion()
        print("Motion detected!")
        turn_on_lights()
        
        # Wait for a moment to show lights
        time.sleep(200)  # Adjust this time according to your preference
        
        # Turn off lights after some time
        turn_off_lights()
        
        # Pause before re-activating the PIR sensor
        time.sleep(1)
except KeyboardInterrupt:
    print("Program stopped by user.")
finally:
    turn_off_lights()  # Ensure lights are turned off when exiting
