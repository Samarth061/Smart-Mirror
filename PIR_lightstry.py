import RPi.GPIO as GPIO
import time
import speech_recognition as sr
from neopixel import *

# LED strip configuration:
LED_COUNT = 10  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

# PIR sensor setup
PIR_PIN = 23  # Example GPIO pin number
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_PIN, GPIO.IN)

# Voice recognition setup
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

# Variables to track the state of the lights, motion, and last command time
lights_on = False
last_motion_time = time.time()
last_command_time = time.time()

def handle_motion():
    global lights_on, last_motion_time
    # Turn on the lights if they are currently off
    if not lights_on:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(255, 255, 255))
        strip.show()
        lights_on = True
    # Update the time of the last motion detection
    last_motion_time = time.time()

def handle_no_motion():
    global lights_on
    # Turn off the lights if they are currently on
    if lights_on:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        lights_on = False

def handle_voice_command(command):
    global lights_on, last_command_time
    if "on" in command:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(255, 255, 255))
        strip.show()
        lights_on = True
        last_command_time = time.time()
    elif "off" in command:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        lights_on = False
        last_command_time = time.time()

try:
    while True:
        if GPIO.input(PIR_PIN):
            handle_motion()
        else:
            # Check if it's time to turn off the lights
            if lights_on and time.time() - last_motion_time >= 600 and time.time() - last_command_time >= 600:
                handle_no_motion()

        with microphone as source:
            print("Listening for voice command...")
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print("Voice command:", command)
            handle_voice_command(command)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Error: ", e)

except KeyboardInterrupt:
    GPIO.cleanup()
